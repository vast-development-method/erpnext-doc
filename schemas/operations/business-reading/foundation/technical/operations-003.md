# Site operations and diagnostics · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Cache manager

<a id="op-3be08af38611ec"></a>
### Clear cache

`operation_foundation_cache_manager_business_behavior_clear_cache`

**Inputs** user = no value, doctype = no value.

**Local steps**

- Bind dependencies Platform.cache\_manager.
- Bind dependencies Platform.utils.caching.
- Bind dependencies clear\_routing\_cache.
- If doctype.
  - Evaluate Platform.cache\_manager.clear\_doctype\_cache(doctype).
  - Evaluate reset\_metadata\_version().
- Otherwise.
  - If user.
    - Evaluate Platform.cache\_manager.clear\_user\_cache(user).
  - Otherwise.
    - Set keys\_to\_delete from set(Platform.cache.get\_keys(empty text)).
    - For each key in Platform.get\_hooks(“persistent\_cache\_keys”).
      - Evaluate keys\_to\_delete.difference\_update(Platform.cache.get\_keys(key)).
    - Evaluate Platform.cache.delete\_value(list(keys\_to\_delete), make\_keys = false).
    - Evaluate Platform.cache.delete\_value(bench\_cache\_keys, shared = true).
    - Evaluate reset\_metadata\_version().
    - Set Platform.local.cache from mapping().
    - Set Platform.local.valid\_columns from mapping().
    - Set Platform.local.new\_doc\_templates from mapping().
    - For each fn in Platform.get\_hooks(“clear\_cache”).
      - Evaluate Platform.get\_attr(fn)().
- If ((not doctype and not user) or doctype equals “DocType”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not doctype and not user) → doctype equals “DocType”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doctype → not user.
  - Evaluate Platform.utils.caching.\_SITE\_CACHE.clear().
  - Evaluate Platform.client\_cache.clear\_cache().
- Set Platform.local.role\_permissions from mapping().
- If hasattr(Platform.local, “request\_cache”).
  - Evaluate Platform.local.request\_cache.clear().
- If hasattr(Platform.local, “system\_settings”).
  - Remove Platform.local.system\_settings.
- If hasattr(Platform.local, “website\_settings”).
  - Remove Platform.local.website\_settings.
- Evaluate clear\_routing\_cache().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“persistent\_cache\_keys”), Platform.get\_hooks(“clear\_cache”) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L578) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L451) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L536)

<a id="op-020184f82aa205"></a>
### Reset metadata version

`operation_foundation_cache_manager_business_behavior_reset_metadata_version`

**Inputs** no declared parameters.

**Explicit results** v.

**Local steps**

- Set v from Platform.generate\_hash().
- Evaluate Platform.client\_cache.set\_value(“metadata\_version”, v).
- Return v.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L1402) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L463) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L548)

## Service · Commands

<a id="op-c1b130d990d233"></a>
### Pass context

`operation_foundation_commands_initialize_business_behavior_pass_context`

**Inputs** f.

**Explicit results** click.pass\_context(\_func).

**Local steps**

- Bind local operation \_func for subsequent calls.
- Return click.pass\_context(\_func).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L2208) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L498) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L581)

<a id="op-d8fde1f2256357"></a>
### Pass context.func

`operation_foundation_commands_initialize_business_behavior_pass_context_function`

**Inputs** ctx, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(f).

**Explicit results** ret.

**Explicit failure paths** click.UsageError(e, ctx).

**Local steps**

- Set profile from ctx.obj.profile.
- If profile.
  - Bind dependencies cProfile.
  - Set pr from cProfile.Profile().
  - Evaluate pr.enable().
- Attempt the following.
  - Set ret from f(ctx.obj, expanded args, expanded names kwargs).
- On failure (tuple(Platform.exceptions.SiteNotSpecifiedError, Platform.exceptions.IncorrectSitePath, Platform.exceptions.CommandFailedError)) bound to e.
  - Raise click.UsageError(e, ctx) with cause e.
- If profile.
  - Evaluate pr.disable().
  - Set s from StringIO().
  - Bind dependencies pstats.
  - Set ps from pstats.Stats(pr, stream = s).sort\_stats(“cumtime”, “tottime”, “ncalls”).
  - Evaluate ps.print\_stats().
  - For each line in s.getvalue().splitlines() at slice no value to 100.
    - Evaluate print(line).
- Return ret.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L2742) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L499) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L582)

<a id="op-4a0ca7e7c3d9a3"></a>
### Get site

`operation_foundation_commands_initialize_business_behavior_get_site`

**Inputs** context, raise\_err = true.

**Explicit results** context.sites at 0 · no value.

**Explicit failure paths** Platform.SiteNotSpecifiedError.

**Local steps**

- Attempt the following.
  - Return context.sites at 0.
- On failure (tuple(IndexError, TypeError)).
  - If raise\_err.
    - Raise Platform.SiteNotSpecifiedError.
  - Return no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L3236) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L497) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L580)

<a id="op-f7431ae90e8df5"></a>
### Popen

`operation_foundation_commands_initialize_business_behavior_popen`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** command, args, kwargs.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** CalledProcessError.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L3356) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L500) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L583)

<a id="op-4d720cd8d9b702"></a>
### Popen.set low prio

`operation_foundation_commands_initialize_business_behavior_popen_set_low_prio`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies psutil.
- If psutil.LINUX.
  - Evaluate psutil.Process().nice(19).
  - Evaluate psutil.Process().ionice(psutil.IOPRIO\_CLASS\_IDLE).
- Otherwise.
  - If psutil.WINDOWS.
    - Evaluate psutil.Process().nice(psutil.IDLE\_PRIORITY\_CLASS).
    - Evaluate psutil.Process().ionice(psutil.IOPRIO\_VERYLOW).
  - Otherwise.
    - Evaluate psutil.Process().nice(19).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L4014) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L501) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L584)

<a id="op-95f355bc609ebe"></a>
### Call command

`operation_foundation_commands_initialize_business_behavior_call_command`

**Inputs** cmd, context.

**Explicit results** click.Context(cmd, obj = context).forward(cmd).

**Local steps**

- Return click.Context(cmd, obj = context).forward(cmd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L4252) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L495) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L578)

<a id="op-92f297f5dc696d"></a>
### Get commands

`operation_foundation_commands_initialize_business_behavior_get_commands`

**Inputs** no declared parameters.

**Explicit results** all\_commands.

**Local steps**

- Bind dependencies flow\_commands.
- Bind dependencies studio\_commands.
- Bind dependencies gettext\_commands.
- Bind dependencies redis\_commands.
- Bind dependencies scheduler\_commands.
- Bind dependencies site\_commands.
- Bind dependencies testing\_commands.
- Bind dependencies translate\_commands.
- Bind dependencies utils\_commands.
- Set clickable\_link from text in the contract.
- Set all\_commands from (((((((nested operand in the contract + nested operand in the contract) + translate\_commands) + gettext\_commands) + utils\_commands) + redis\_commands) + studio\_commands) + flow\_commands).
- For each command in all\_commands.
  - If not command.help.
    - Set command.help from formatted text Refer to {clickable\_link}.
- Return all\_commands.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L120) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L496) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L579)

## Service · Config

<a id="op-c36bad25eee807"></a>
### Get site config

`operation_foundation_configuration_business_behavior_get_site_configuration`

**Inputs** sites\_path = no value, site\_path = no value, cached (named only, default false).

**Declared result** \_dict at tuple(str, Any).

**Explicit results** \_cached\_get\_site\_config(sites\_path, site\_path).copy() · \_get\_site\_config(sites\_path, site\_path).

**Local steps**

- Set sites\_path from (sites\_path or getattr(Platform.local, “sites\_path”, “.”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sites\_path → getattr(Platform.local, “sites\_path”, “.”).
- Set site\_path from (site\_path or getattr(Platform.local, “site\_path”, no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in site\_path → getattr(Platform.local, “site\_path”, no value).
- If cached.
  - Return \_cached\_get\_site\_config(sites\_path, site\_path).copy().
- Otherwise.
  - Return \_get\_site\_config(sites\_path, site\_path).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “sites\_path”, “.”), getattr(Platform.local, “site\_path”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0031.json#L7024) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L707) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L780)

<a id="op-a5ca5798409406"></a>
### Get site config

`operation_foundation_configuration_business_behavior_get_site_configuration_2`

**Inputs** sites\_path, site\_path.

**Declared result** \_dict at tuple(str, Any).

**Explicit results** config.

**Explicit failure paths** propagate active failure · IncorrectSitePath(error\_msg).

**Local steps**

- Set config from \_dict().
- Set common\_config from get\_common\_site\_config(sites\_path).
- If sites\_path.
  - Evaluate config.update(common\_config).
- If site\_path.
  - Set site\_config from os.path.join(site\_path, “site\_config.json”).
  - If os.path.exists(site\_config).
    - Attempt the following.
      - Evaluate config.update(get\_file\_json(site\_config)).
    - On failure (Exception) bound to error.
      - Evaluate click.secho(formatted text {Platform.local.site}/site\_config.json is invalid, fg = “red”).
      - Evaluate print(error).
      - Propagate the active failure.
  - Otherwise.
    - If (Platform.local.site and not Platform.local.flags.new\_site).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.local.site → not Platform.local.flags.new\_site.
      - Set error\_msg from formatted text {Platform.local.site} does not exist..
      - If common\_config.developer\_mode.
        - Bind dependencies get\_sites.
        - Set all\_sites from get\_sites().
        - Update error\_msg using + “\\n\\nSites on this bench:\\n”.
        - Update error\_msg using + whitespace '\\n'.join(generator of formatted text \* {site} for site drawn from all\_sites).
          - Draw site from all\_sites.
      - Raise IncorrectSitePath(error\_msg).
- Bind local operation db\_default\_ports for subsequent calls.
- Evaluate \_apply\_common\_env\_overrides(config).
- Set config at “db\_type” from (os.environ.get(“Platform\_DB\_TYPE”) or config.get(“db\_type”) or “mariadb”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.environ.get(“Platform\_DB\_TYPE”) → config.get(“db\_type”) → “mariadb”.
- If config at “db\_type” belongs to tuple(“mariadb”, “postgres”).
  - Set config at “db\_socket” from (os.environ.get(“Platform\_DB\_SOCKET”) or config.get(“db\_socket”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.environ.get(“Platform\_DB\_SOCKET”) → config.get(“db\_socket”).
  - Set config at “db\_host” from (os.environ.get(“Platform\_DB\_HOST”) or config.get(“db\_host”) or “127.0.0.1”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.environ.get(“Platform\_DB\_HOST”) → config.get(“db\_host”) → “127.0.0.1”.
  - Set config at “db\_port” from int((os.environ.get(“Platform\_DB\_PORT”) or config.get(“db\_port”) or db\_default\_ports(config at “db\_type”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.environ.get(“Platform\_DB\_PORT”) → config.get(“db\_port”) → db\_default\_ports(config at “db\_type”).
  - Set config at “db\_user” from (os.environ.get(“Platform\_DB\_USER”) or config.get(“db\_user”) or config.get(“db\_name”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.environ.get(“Platform\_DB\_USER”) → config.get(“db\_user”) → config.get(“db\_name”).
  - Set config at “db\_password” from (os.environ.get(“Platform\_DB\_PASSWORD”) or config.get(“db\_password”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.environ.get(“Platform\_DB\_PASSWORD”) → config.get(“db\_password”).
- Set config at “db\_name” from (os.environ.get(“Platform\_DB\_NAME”) or config.get(“db\_name”) or config at “db\_user”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.environ.get(“Platform\_DB\_NAME”) → config.get(“db\_name”) → config at “db\_user”.
- If extra\_config bound to config.get(“extra\_config”).
  - If isinstance(extra\_config, str).
    - Set extra\_config from list(extra\_config).
  - For each hook in extra\_config.
    - Attempt the following.
      - Set tuple(module, method) from hook.rsplit(“.”, 1).
      - Update config using bitwise or getattr(importlib.import\_module(module), method)().
    - On failure (Exception).
      - Evaluate print(formatted text Config hook {hook} failed).
      - Evaluate traceback.print\_exc().
- Return config.

**Values supplied outside this operation** selected callable from getattr(importlib.import\_module(module), method).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L708) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L781)

<a id="op-82ec0c28f21e25"></a>
### Get site config.db default ports

`operation_foundation_configuration_business_behavior_get_site_configuration_database_default_ports`

**Inputs** db\_type.

**Explicit results** MariaDBDatabase.default\_port · PostgresDatabase.default\_port.

**Explicit failure paths** ValueError(formatted text Unsupported db\_type={db\_type}).

**Local steps**

- If db\_type equals “mariadb”.
  - Bind dependencies MariaDBDatabase.
  - Return MariaDBDatabase.default\_port.
- Otherwise.
  - If db\_type equals “postgres”.
    - Bind dependencies PostgresDatabase.
    - Return PostgresDatabase.default\_port.
- Raise ValueError(formatted text Unsupported db\_type={db\_type}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L1589) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L709) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L782)

<a id="op-ba07a00e65f255"></a>
### Get common site config

`operation_foundation_configuration_business_behavior_get_common_site_configuration`

**Inputs** sites\_path = no value, cached = false.

**Declared result** \_dict at tuple(str, Any).

**Explicit results** \_cached\_get\_common\_site\_config(sites\_path).copy() · \_get\_common\_site\_config(sites\_path).

**Local steps**

- Set sites\_path from (sites\_path or getattr(Platform.local, “sites\_path”, “.”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sites\_path → getattr(Platform.local, “sites\_path”, “.”).
- If cached.
  - Return \_cached\_get\_common\_site\_config(sites\_path).copy().
- Otherwise.
  - Return \_get\_common\_site\_config(sites\_path).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “sites\_path”, “.”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L1747) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L704) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L777)

<a id="op-aa1c8f43ca12f0"></a>
### Apply common env overrides

`operation_foundation_configuration_business_behavior_apply_common_env_overrides`

**Inputs** config.

**Declared result** no value.

**Local steps**

- Set config at “redis\_queue” from (os.environ.get(“Platform\_REDIS\_QUEUE”) or config.get(“redis\_queue”) or “redis://127.0.0.1:11311”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.environ.get(“Platform\_REDIS\_QUEUE”) → config.get(“redis\_queue”) → “redis://127.0.0.1:11311”.
- Set config at “redis\_cache” from (os.environ.get(“Platform\_REDIS\_CACHE”) or config.get(“redis\_cache”) or “redis://127.0.0.1:13311”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.environ.get(“Platform\_REDIS\_CACHE”) → config.get(“redis\_cache”) → “redis://127.0.0.1:13311”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L1932) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L702) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L775)

<a id="op-b9f35cc50c7462"></a>
### Get common site config

`operation_foundation_configuration_business_behavior_get_common_site_configuration_2`

**Inputs** sites\_path.

**Declared result** \_dict at tuple(str, Any).

**Explicit results** config.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set common\_site\_config from os.path.join(sites\_path, “common\_site\_config.json”).
- Set config from \_dict().
- If os.path.exists(common\_site\_config).
  - Attempt the following.
    - Set config from \_dict(get\_file\_json(common\_site\_config)).
  - On failure (Exception) bound to error.
    - Evaluate click.secho(“common\_site\_config.json is invalid”, fg = “red”).
    - Evaluate print(error).
    - Propagate the active failure.
- Evaluate \_apply\_common\_env\_overrides(config).
- Return config.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L2121) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L705) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L778)

<a id="op-7d81c51fbdc301"></a>
### Clear site config cache

`operation_foundation_configuration_business_behavior_clear_site_configuration_cache`

**Inputs** no declared parameters.

**Local steps**

- Evaluate \_cached\_get\_common\_site\_config.clear\_cache().
- Evaluate \_cached\_get\_site\_config.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L2409) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L703) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L776)

<a id="op-72ee35b3d3c608"></a>
### Get conf

`operation_foundation_configuration_business_behavior_get_configuration`

**Inputs** site = no value.

**Declared result** \_dict at tuple(str, Any).

**Explicit results** Platform.local.conf · get\_common\_site\_config(sites\_path).

**Local steps**

- If hasattr(Platform.local, “conf”).
  - Return Platform.local.conf.
- Set sites\_path from os.environ.get(“SITES\_PATH”, “.”).
- If site.
  - Within Platform.init\_site(site).
    - Return Platform.local.conf.
- Otherwise.
  - Return get\_common\_site\_config(sites\_path).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L2468) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L706) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L779)

## Service · Coverage

<a id="op-267fbe7aa9ce19"></a>
### Code Coverage.initialize

`operation_foundation_coverage_business_behavior_code_coverage_initialize`

**Inputs** self, with\_coverage, app, outfile = “coverage.xml”.

**Local steps**

- Set self.with\_coverage from with\_coverage.
- Set self.app from (app or “Platform”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app → “Platform”.
- Set self.outfile from outfile.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L607) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L777) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L925)

<a id="op-334d884cb4b6df"></a>
### Code Coverage.enter context

`operation_foundation_coverage_business_behavior_code_coverage_enter`

**Inputs** self.

**Explicit results** self.

**Local steps**

- If self.with\_coverage.
  - Bind dependencies os.
  - Bind dependencies Coverage.
  - Bind dependencies get\_bench\_path.
  - Set source\_path from os.path.join(get\_bench\_path(), “apps”, self.app).
  - Set omit from STANDARD\_EXCLUSIONS at slice no value to no value.
  - If self.app equals “Platform”.
    - Evaluate omit.extend(Platform\_EXCLUSIONS).
  - Set self.coverage from Coverage(source = list(source\_path), omit = omit, include = STANDARD\_INCLUSIONS).
  - Evaluate self.coverage.start().
- Return self.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L69) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L775) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L923)

<a id="op-83ffbcf0e8d549"></a>
### Code Coverage.exit context

`operation_foundation_coverage_business_behavior_code_coverage_exit`

**Inputs** self, exc\_type, exc\_value, traceback.

**State and service calls** call save on self.coverage.

**Local steps**

- If self.with\_coverage.
  - Evaluate self.coverage.stop().
  - Evaluate self.coverage.save().
  - Evaluate self.coverage.xml\_report(outfile = self.outfile).
  - Evaluate print(“Saved Coverage”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L1033) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L776) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L924)

## Service · Discovery

<a id="op-7c1583f225f3c4"></a>
### Discover all tests

`operation_foundation_testing_discovery_business_behavior_discover_all_tests`

**Inputs** apps, runner.

**Wrappers, in declaration order** debug\_timer.

**Declared result** “TestRunner”.

**Explicit results** runner.

**Explicit failure paths** TestRunnerError(formatted text Failed to discover tests for {apps}: {e}).

**Local steps**

- Evaluate logger.debug(formatted text Discovering tests for apps: {apps}).
- If isinstance(apps, str).
  - Set apps from list(apps).
- Attempt the following.
  - For each app in apps.
    - Set app\_path from Path(Platform.get\_app\_path(app)).
    - For each tuple(path, folders, files) in os.walk(app\_path).
      - Set folders at slice no value to no value from list of f for f drawn from folders where not f.startswith(“.”).
        - Draw f from folders, keep a combination only if (not f.startswith(“.”)).
      - For each dontwalk in tuple(“node\_modules”, “locals”, “public”, “\_\_pycache\_\_”).
        - If dontwalk belongs to folders.
          - Evaluate folders.remove(dontwalk).
      - If os.path.sep.join(list(“doctype”, “doctype”, “boilerplate”)) belongs to path.
        - Continue with the next iteration or loop test.
      - Set path from Path(path).
      - For each file in list of path.joinpath(filename) for filename drawn from files where (filename.startswith(“test\_”) and filename.endswith(“.py”) and filename differs from “test\_runner.py”).
        - Draw filename from files, keep a combination only if ((filename.startswith(“test\_”) and filename.endswith(“.py”) and filename differs from “test\_runner.py”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in filename.startswith(“test\_”) → filename.endswith(“.py”) → filename differs from “test\_runner.py”.
        - Set module\_name from formatted text {“.”.join(file.relative\_to(app\_path.parent).parent.parts)}.{file.stem}.
        - Evaluate \_add\_module\_tests(runner, app, module\_name).
- On failure (Exception) bound to e.
  - Evaluate logger.error(formatted text Error discovering all tests for {apps}: {e}).
  - Raise TestRunnerError(formatted text Failed to discover tests for {apps}: {e}) with cause e.
- Return runner.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L1424) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1924) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L598)

<a id="op-fc22248ede6b63"></a>
### Discover doctype tests

`operation_foundation_testing_discovery_business_behavior_discover_record_type_tests`

**Inputs** doctypes, runner, app, force = false.

**Wrappers, in declaration order** debug\_timer.

**Declared result** “TestRunner”.

**Record and data access** read “DocType” via get\_value · read “Module Def” via get\_value.

**State and service calls** request delete on doctype.

**Explicit results** runner.

**Explicit failure paths** TestRunnerError(formatted text Invalid doctype {doctype}) · TestRunnerError(formatted text Mismatch between specified app '{app}' and doctype app '{doctype\_app}') · TestRunnerError(formatted text Failed to discover tests for {doctype}: {e}).

**Local steps**

- If isinstance(doctypes, str).
  - Set doctypes from list(doctypes).
- Set \_app from app.
- For each doctype in doctypes.
  - Attempt the following.
    - Set module from Platform.db.get\_value(“DocType”, doctype, “module”).
    - If not module.
      - Raise TestRunnerError(formatted text Invalid doctype {doctype}).
    - Set doctype\_app from Platform.db.get\_value(“Module Def”, module, “app\_name”).
    - If app is identical to no value.
      - Set \_app from doctype\_app.
    - Otherwise.
      - If doctype\_app differs from app.
        - Raise TestRunnerError(formatted text Mismatch between specified app '{app}' and doctype app '{doctype\_app}').
    - Set test\_module from Platform.modules.utils.get\_module\_name(doctype, module, “test\_”).
    - Evaluate (force and Platform.db.delete(doctype)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in force → Platform.db.delete(doctype).
    - Evaluate \_add\_module\_tests(runner, \_app, test\_module).
  - On failure (Exception) bound to e.
    - Evaluate logger.error(formatted text Error discovering tests for {doctype}: {e}).
    - Raise TestRunnerError(formatted text Failed to discover tests for {doctype}: {e}) with cause e.
- Return runner.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L2290) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1926) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L600)

<a id="op-cfc04271a44f4a"></a>
### Discover module tests

`operation_foundation_testing_discovery_business_behavior_discover_module_tests`

**Inputs** modules, runner, app.

**Wrappers, in declaration order** debug\_timer.

**Declared result** “TestRunner”.

**Explicit results** runner.

**Explicit failure paths** TestRunnerError(formatted text Mismatch between specified app '{app}' and module app '{module\_app}') · TestRunnerError(formatted text Failed to discover tests for {module}: {e}).

**Local steps**

- If isinstance(modules, str).
  - Set modules from list(modules).
- Set \_app from app.
- Attempt the following.
  - For each module in modules.
    - Set module\_app from module.split(“.”) at 0.
    - If app is identical to no value.
      - Set \_app from module\_app.
    - Otherwise.
      - If app differs from module\_app.
        - Raise TestRunnerError(formatted text Mismatch between specified app '{app}' and module app '{module\_app}').
    - Evaluate \_add\_module\_tests(runner, \_app, module).
- On failure (Exception) bound to e.
  - Evaluate logger.error(formatted text Error discovering tests for {module}: {e}).
  - Raise TestRunnerError(formatted text Failed to discover tests for {module}: {e}) with cause e.
- Return runner.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L2973) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1925) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L599)

<a id="op-0b7b31a6f235d2"></a>
### Add module tests

`operation_foundation_testing_discovery_business_behavior_add_module_tests`

**Inputs** runner, app, module.

**Local steps**

- Set module from importlib.import\_module(module).
- If runner.cfg.case.
  - Set test\_suite from unittest.TestLoader().loadTestsFromTestCase(getattr(module, runner.cfg.case)).
- Otherwise.
  - Set test\_suite from unittest.TestLoader().loadTestsFromModule(module).
- For each test in runner.\_iterate\_suite(test\_suite).
  - If (runner.cfg.tests and test.\_testMethodName does not belong to runner.cfg.tests).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in runner.cfg.tests → test.\_testMethodName does not belong to runner.cfg.tests.
    - Continue with the next iteration or loop test.
  - Select the first matching pattern against test.
    - Pattern instance of IntegrationTestCase.
      - Set category from “integration”.
    - Pattern instance of UnitTestCase.
      - Set category from “unit”.
    - Pattern any value.
      - Set category from “unspecified-category”.
      - If any(generator of b.\_\_name\_\_ equals “PlatformTestCase” for b drawn from test.\_\_class\_\_.\_\_bases\_\_).
        - Draw b from test.\_\_class\_\_.\_\_bases\_\_.
        - Bind dependencies deprecation\_warning.
        - Evaluate record a compatibility advisory for the invoked interface.
        - Set category from “old-Platform-test-class-category”.
  - If (runner.cfg.selected\_categories and category does not belong to runner.cfg.selected\_categories).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in runner.cfg.selected\_categories → category does not belong to runner.cfg.selected\_categories.
    - Continue with the next iteration or loop test.
  - Evaluate runner.per\_app\_categories at app at category.addTest(test).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(module, runner.cfg.case).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L44) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1923) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L597)
