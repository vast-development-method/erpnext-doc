# Shared value and file services · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Backups

<a id="op-5758ef8a3f5bba"></a>
### Get backup path

`operation_foundation_utils_backups_business_behavior_get_backup_path`

**Inputs** no declared parameters.

**Explicit results** Platform.utils.get\_site\_path(conf.get(“backup\_path”, “private/backups”)).

**Local steps**

- Return Platform.utils.get\_site\_path(conf.get(“backup\_path”, “private/backups”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L1139) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L901) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1526)

<a id="op-6782c6872e89a6"></a>
### Get backup encryption key

`operation_foundation_utils_backups_business_behavior_get_backup_encryption_key`

**Control responsibility** Protected data and signing. Key ownership, the selected cryptographic provider and verification status govern the protected data.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L1209) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L900) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1525)

<a id="op-f1a7a3abf1321d"></a>
### Get or generate backup encryption key

`operation_foundation_utils_backups_business_behavior_get_or_generate_backup_encryption_key`

**Control responsibility** Protected data and signing. Key ownership, the selected cryptographic provider and verification status govern the protected data.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L1288) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L902) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1527)

<a id="op-6c067172a14e98"></a>
### Decrypt backup

`operation_foundation_utils_backups_business_behavior_decrypt_backup`

**Control responsibility** Protected data and signing. Key ownership, the selected cryptographic provider and verification status govern the protected data.

**Declared inputs** file\_path, passphrase.

**Explicit result forms** no value.

**Observed service boundaries** record lookup.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L1436) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L897) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1522)

<a id="op-1f144586bc74a3"></a>
### Backup

`operation_foundation_utils_backups_business_behavior_backup`

**Inputs** with\_files = false, backup\_path\_db = no value, backup\_path\_files = no value, backup\_path\_private\_files = no value, backup\_path\_conf = no value.

**Explicit results** mapping(“backup\_path\_db” → odb.backup\_path\_db, “backup\_path\_files” → odb.backup\_path\_files, “backup\_path\_private\_files” → odb.backup\_path\_private\_files).

**Local steps**

- Set odb from scheduled\_backup(ignore\_files = not with\_files, backup\_path\_db = backup\_path\_db, backup\_path\_files = backup\_path\_files, backup\_path\_private\_files = backup\_path\_private\_files, …).
- Return mapping(“backup\_path\_db” → odb.backup\_path\_db, “backup\_path\_files” → odb.backup\_path\_files, “backup\_path\_private\_files” → odb.backup\_path\_private\_files).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L1994) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L874) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1499)

## Service · Bench helper

<a id="op-9e90f272258b0f"></a>
### Platform Click Wrapper

`operation_foundation_utils_bench_helper_business_behavior_foundation_command_dispatch_wrapper`

**Inputs** cls, handler.

**Explicit results** Cls.

**Local steps**

- Bind local type Cls (class body executes during definition).
- Return Cls.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L2209) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L908) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1533)

<a id="op-96d8f511a0d1d6"></a>
### Platform Click Wrapper.Cls.get command

`operation_foundation_utils_bench_helper_business_behavior_foundation_command_dispatch_wrapper_cls_get_command`

**Inputs** self, ctx, cmd\_name.

**Explicit results** rv.

**Explicit failure paths** click.NoSuchOption(cmd\_name, possibilities = possibilities, message = formatted text No such command: {cmd\_name}.).

**Local steps**

- Set rv from super().get\_command(ctx, cmd\_name).
- If rv is distinct from no value.
  - Return rv.
- Set all\_commands from self.list\_commands(ctx).
- Bind dependencies get\_close\_matches.
- Set possibilities from get\_close\_matches(cmd\_name, all\_commands).
- Raise click.NoSuchOption(cmd\_name, possibilities = possibilities, message = formatted text No such command: {cmd\_name}.).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L2904) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L909) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1534)

<a id="op-1a6c709183a8be"></a>
### Platform Click Wrapper.Cls.make context

`operation_foundation_utils_bench_helper_business_behavior_foundation_command_dispatch_wrapper_cls_make_context`

**Inputs** self, info\_name, args, parent = no value, remaining named values extra.

**Explicit results** super().make\_context(info\_name, args, parent = parent, expanded names extra).

**Explicit failure paths** e.

**Local steps**

- Attempt the following.
  - Return super().make\_context(info\_name, args, parent = parent, expanded names extra).
- On failure (tuple(click.ClickException, click.exceptions.Exit, click.exceptions.Abort)) bound to e.
  - Raise e.
- On failure (Exception) bound to exc.
  - Evaluate handler(self, info\_name, exc).
  - Evaluate sys.exit(1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L3152) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L911) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1536)

<a id="op-5b2ddd4abaf81a"></a>
### Platform Click Wrapper.Cls.invoke

`operation_foundation_utils_bench_helper_business_behavior_foundation_command_dispatch_wrapper_cls_invoke`

**Inputs** self, ctx.

**Explicit results** super().invoke(ctx).

**Explicit failure paths** e.

**Local steps**

- Attempt the following.
  - Return super().invoke(ctx).
- On failure (tuple(click.ClickException, click.exceptions.Exit, click.exceptions.Abort)) bound to e.
  - Raise e.
- On failure (Exception) bound to exc.
  - Evaluate handler(self, ctx.info\_name, exc).
  - Evaluate sys.exit(1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L3389) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L910) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1535)

<a id="op-5dcb4991e74a97"></a>
### Handle exception

`operation_foundation_utils_bench_helper_business_behavior_handle_exception`

**Inputs** cmd, info\_name, exc.

**Local steps**

- Evaluate click.echo(traceback.format\_exc()).
- Evaluate click.echo(exc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L3586) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L919) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1544)

<a id="op-37c6ae95d31205"></a>
### Main

`operation_foundation_utils_bench_helper_business_behavior_main`

**Inputs** no declared parameters.

**Local steps**

- Set commands from get\_app\_groups().
- Evaluate commands.update(mapping(“get-Platform-commands” → get\_Platform\_commands, “get-Platform-help” → get\_Platform\_help)).
- Evaluate PlatformClickWrapper(click.Group, handle\_exception)(commands = commands)(prog\_name = “bench”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L3687) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L920) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1545)

<a id="op-c2e54e1ead7bb8"></a>
### Get app groups

`operation_foundation_utils_bench_helper_business_behavior_get_application_groups`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, (click.Group bitwise or click.Command)).

**Explicit results** dict(Platform = click.group(name = “Platform”, commands = commands, cls = PlatformClickWrapper(click.Group, handle\_exception))(app\_group)).

**Local steps**

- Set commands from mapping().
- For each app in get\_apps().
  - If app\_commands bound to get\_app\_commands(app).
    - Update commands using bitwise or app\_commands.
- Return dict(Platform = click.group(name = “Platform”, commands = commands, cls = PlatformClickWrapper(click.Group, handle\_exception))(app\_group)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L3841) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L914) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1539)

<a id="op-49074b1b7cb9ac"></a>
### Get app group

`operation_foundation_utils_bench_helper_business_behavior_get_application_group`

**Inputs** app.

**Declared result** click.Group.

**Explicit results** click.group(name = app, commands = app\_commands, cls = PlatformClickWrapper(click.Group, handle\_exception))(app\_group).

**Local steps**

- If app\_commands bound to get\_app\_commands(app).
  - Return click.group(name = app, commands = app\_commands, cls = PlatformClickWrapper(click.Group, handle\_exception))(app\_group).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L4069) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L913) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1538)

<a id="op-f1acf95ddcabf6"></a>
### App group

`operation_foundation_utils_bench_helper_business_behavior_application_group`

**Inputs** ctx, site = false, force = false, verbose = false, profile = false.

**Wrappers, in declaration order** click.option(“--site”), click.option(“--profile”, is\_flag = true, default = false, help = “Profile”), click.option(“--verbose”, is\_flag = true, default = false, help = “Verbose”), click.option(“--force”, is\_flag = true, default = false, help = “Force”), click.pass\_context.

**Local steps**

- Set ctx.obj from CliCtxObj(sites = get\_sites(site), force = force, verbose = verbose, profile = profile).
- If ctx.info\_name equals “Platform”.
  - Set ctx.info\_name from empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L4219) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L907) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1532)

<a id="op-14c257b5f83fdb"></a>
### Get sites

`operation_foundation_utils_bench_helper_business_behavior_get_sites`

**Inputs** site\_arg.

**Declared result** list at str.

**Explicit results** Platform.utils.get\_sites() · list(site\_arg) · list(env\_site) · list(default\_site) · list().

**Local steps**

- If site\_arg equals “all”.
  - Return Platform.utils.get\_sites().
- Otherwise.
  - If site\_arg.
    - Return list(site\_arg).
  - Otherwise.
    - If env\_site bound to os.environ.get(“Platform\_SITE”).
      - Return list(env\_site).
    - Otherwise.
      - If default\_site bound to Platform.get\_conf().default\_site.
        - Return list(default\_site).
      - Otherwise.
        - If (site bound to Platform.read\_file(“currentsite.txt”) and site.strip()).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in site bound to Platform.read\_file(“currentsite.txt”) → site.strip().
          - Evaluate click.secho(dedent(formatted text   WARNING: currentsite.txt is not supported anymore for setting default site. Use following command to set it as default site.  $ bench use {site}), fg = “red”).
- Return list().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L4583) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L918) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1543)

<a id="op-4fc5fe4e6fda7d"></a>
### Get app commands

`operation_foundation_utils_bench_helper_business_behavior_get_application_commands`

**Inputs** app.

**Declared result** dict.

**Explicit results** ret.

**Local steps**

- Set ret from mapping().
- Attempt the following.
  - Set app\_command\_module from importlib.import\_module(formatted text {app}.commands).
- On failure (ModuleNotFoundError) bound to e.
  - If e.name equals formatted text {app}.commands.
    - Return ret.
  - Evaluate traceback.print\_exc().
  - Return ret.
- On failure (Exception).
  - Evaluate traceback.print\_exc().
  - Return ret.
- For each command in getattr(app\_command\_module, “commands”, list()).
  - Set ret at command.name from command.
- Return ret.

**Values supplied outside this operation** selected callable from getattr(app\_command\_module, “commands”, list()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L4916) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L912) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1537)

<a id="op-0dcfe404032f19"></a>
### Get Platform commands

`operation_foundation_utils_bench_helper_business_behavior_get_foundation_commands`

**Inputs** no declared parameters.

**Wrappers, in declaration order** click.command(“get-Platform-commands”).

**Local steps**

- Set commands from list(get\_app\_commands(“Platform”)).
- For each app in get\_apps().
  - Set app\_commands from get\_app\_commands(app).
  - If app\_commands.
    - Evaluate commands.extend(list(app\_commands)).
- Evaluate print(json.dumps(commands)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L5210) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L916) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1541)

<a id="op-f0b86180027d37"></a>
### Get Platform help

`operation_foundation_utils_bench_helper_business_behavior_get_foundation_help`

**Inputs** no declared parameters.

**Wrappers, in declaration order** click.command(“get-Platform-help”).

**Local steps**

- Evaluate print(click.Context(get\_app\_groups() at “Platform”).get\_help()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L5423) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L917) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1542)

<a id="op-ec39b390178e5c"></a>
### Get apps

`operation_foundation_utils_bench_helper_business_behavior_get_apps`

**Inputs** no declared parameters.

**Explicit results** Platform.get\_all\_apps(with\_internal\_apps = false, sites\_path = “.”).

**Local steps**

- Return Platform.get\_all\_apps(with\_internal\_apps = false, sites\_path = “.”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L5530) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L915) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1540)

## Service · Boilerplate

<a id="op-5493879f816bbd"></a>
### Make boilerplate

`operation_foundation_utils_boilerplate_business_behavior_make_boilerplate`

**Inputs** dest, app\_name, no\_git = false.

**Explicit results** no value.

**Local steps**

- If not os.path.exists(dest).
  - Evaluate print(“Destination directory does not exist”).
  - Return no value.
- Set app\_name from Platform.scrub(app\_name).
- Set hooks from \_get\_user\_inputs(app\_name).
- Evaluate \_create\_app\_boilerplate(dest, hooks, no\_git = no\_git).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L5590) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L929) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1554)

<a id="op-5eb47123775f47"></a>
### Get user inputs

`operation_foundation_utils_boilerplate_business_behavior_get_user_inputs`

**Inputs** app\_name.

**Explicit results** hooks.

**Local steps**

- Set app\_name from Platform.scrub(app\_name).
- Set hooks from Platform.\_dict().
- Set hooks.app\_name from app\_name.
- Set app\_title from hooks.app\_name.replace(“\_”, one space).title().
- Set new\_app\_config from mapping(“app\_title” → mapping(“prompt” → “App Title”, “default” → app\_title, “validator” → is\_valid\_title), “app\_description” → mapping(“prompt” → “App Description”), “app\_publisher” → mapping(“prompt” → “ ….
- For each tuple(property, config) in new\_app\_config.items().
  - Set value from no value.
  - Set input\_type from config.get(“type”, str).
  - While value is identical to no value.
    - If input\_type is identical to bool.
      - Set value from click.confirm(config at “prompt”, default = config.get(“default”)).
    - Otherwise.
      - Set value from click.prompt(config at “prompt”, default = config.get(“default”), type = input\_type).
    - If validator\_function bound to config.get(“validator”).
      - If not validator\_function(value).
        - Set value from no value.
  - Set hooks at property from value.
- Return hooks.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L5793) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L926) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1551)

<a id="op-8d8bd338a372fe"></a>
### Is valid email

`operation_foundation_utils_boilerplate_business_behavior_is_valid_email`

**Inputs** email.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Bind dependencies Address.
- Attempt the following.
  - Evaluate Address(addr\_spec = email).
- On failure (Exception).
  - Evaluate print(“App Email should be a valid email address.”).
  - Return false.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L6648) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L927) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1552)

<a id="op-33c32bcac6dd5c"></a>
### Is valid title

`operation_foundation_utils_boilerplate_business_behavior_is_valid_title`

**Inputs** title.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- If not APP\_TITLE\_PATTERN.match(title).
  - Evaluate print(“App Title should start with a letter and it can only consist of letters, numbers, spaces and underscores”).
  - Return false.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L6768) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L928) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1553)

<a id="op-1f9708804ae1f8"></a>
### Get license options

`operation_foundation_utils_boilerplate_business_behavior_get_license_options`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** list(“agpl-3.0”, “gpl-3.0”, “mit”, “custom”) · list of licencse.lower() for licencse drawn from ids.

**Local steps**

- Set url from text in the contract.
- Attempt the following.
  - Set res from requests.get(url = url).
- On failure (requests.exceptions.RequestException).
  - Return list(“agpl-3.0”, “gpl-3.0”, “mit”, “custom”).
- If res.status\_code equals 200.
  - Set res from res.json().
  - Set ids from list of r.get(“spdx\_id”) for r drawn from res.
    - Draw r from res.
  - Return list of licencse.lower() for licencse drawn from ids.
    - Draw licencse from ids.
- Return list(“agpl-3.0”, “gpl-3.0”, “mit”, “custom”).

**Values supplied outside this operation** service or queued work from requests.get(url = url).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L6864) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L924) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1549)
