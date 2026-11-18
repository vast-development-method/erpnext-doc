# Site operations and diagnostics · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Testing

<a id="op-902920db2cbd99"></a>
### Yarn add

`operation_foundation_binding_foundation_commands_testing_yarn_add`

**Inputs** Platform\_path, packages.

**Local steps**

- Set package\_json\_path from os.path.join(Platform\_path, “package.json”).
- Within open(package\_json\_path) bound as f.
  - Set package\_json\_contents from f.read().
- Evaluate Platform.commands.popen(formatted text yarn add {packages} --no-lockfile, cwd = Platform\_path, raise\_err = true).
- Within open(package\_json\_path, “w”) bound as f.
  - Evaluate f.write(package\_json\_contents).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L117) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L599) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L575)

<a id="op-7c52cb3bcdcf1a"></a>
### Run ui tests

`operation_foundation_commands_testing_business_behavior_run_user_interface_tests`

**Inputs** context, app, headless = false, browser = no value, parallel\_site = tuple(), runnerargs = no value, spec = no value, parallel = false, with\_coverage = false, ci\_build\_id = no value.

**Wrappers, in declaration order** click.command(“run-ui-tests”, context\_settings = dict(ignore\_unknown\_options = true)), click.argument(“app”), click.argument(“runnerargs”, nargs = negative 1, type = click.UNPROCESSED), click.option(“--headless”, is\_flag = true, help = “Run UI Test in headless mode”), click.option(“--browser”, help = “Browser to run tests in: chromium, firefox or webkit”), click.option(“--parallel-site”, multiple = true, help = “Additional site to run tests on in parallel. Each site gets its own worker”), click.option(“--spec”, type = click.Path(dir\_okay = false, file\_okay = true), help = “Spec file to run”), click.option(“--parallel”, is\_flag = true, hidden = true), click.option(“--with-coverage”, is\_flag = true, hidden = true), click.option(“--ci-build-id”, hidden = true), pass\_context.

**Explicit failure paths** click.exceptions.Exit(1).

**Local steps**

- Set site from get\_site(context).
- Evaluate Platform.init(site).
- Set app\_base\_path from Platform.get\_app\_source\_path(app).
- Set Platform\_path from Platform.get\_app\_source\_path(“Platform”).
- If \_has\_config(app\_base\_path, “playwright”).
  - Set runner from \_run\_playwright.
- Otherwise.
  - If \_has\_config(app\_base\_path, “cypress”).
    - Evaluate click.secho(compatibility advisory text in the contract, fg = “yellow”).
    - Set runner from partial(\_run\_cypress, parallel = parallel, with\_coverage = with\_coverage, ci\_build\_id = ci\_build\_id).
  - Otherwise.
    - Evaluate click.secho(formatted text {app} has no playwright or cypress config, fg = “red”).
    - Raise click.exceptions.Exit(1).
- If (runner is identical to \_run\_playwright and (parallel or with\_coverage or ci\_build\_id)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in runner is identical to \_run\_playwright → (parallel or with\_coverage or ci\_build\_id).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parallel → with\_coverage → ci\_build\_id.
  - Evaluate click.secho(“--parallel, --with-coverage and --ci-build-id only apply to Cypress and are ignored”, fg = “yellow”).
- Attempt the following.
  - Evaluate runner(site = site, app\_base\_path = app\_base\_path, Platform\_path = Platform\_path, headless = headless, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in runnerargs → list().
- On failure (subprocess.CalledProcessError) bound to e.
  - Evaluate click.secho(“UI tests failed”, fg = “red”).
  - Raise click.exceptions.Exit(1) with cause e.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L134) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L648) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L722)

<a id="op-4120d6db4442e0"></a>
### Run playwright

`operation_foundation_binding_foundation_commands_testing_run_playwright`

**Inputs** site, app\_base\_path, Platform\_path, headless, browser, spec, parallel\_site, runnerargs.

**Local steps**

- Set node\_modules\_path from os.path.join(Platform\_path, “node\_modules”).
- Set playwright\_path from os.path.join(node\_modules\_path, “.bin”, “playwright”).
- If not os.path.exists(playwright\_path).
  - Evaluate click.secho(“Installing Playwright...”, fg = “yellow”).
  - Evaluate \_yarn\_add(Platform\_path, formatted text @playwright/test@{PLAYWRIGHT\_VERSION}).
- Set with\_deps from “--with-deps ” when os.environ.get(“CI”), otherwise empty text.
  - Value choice on os.environ.get(“CI”) — true gives “--with-deps ”, false gives empty text.
- Evaluate Platform.commands.popen(formatted text {playwright\_path} install {with\_deps}{(browser or “chromium”)}, cwd = Platform\_path, raise\_err = true).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in browser → “chromium”.
- Set command from list(playwright\_path, “test”).
- If not headless.
  - Evaluate command.append(“--ui”).
- If browser.
  - Evaluate command.append(formatted text --browser={browser}).
- If spec.
  - Evaluate command.append(spec).
- Evaluate command.extend(runnerargs).
- Set env from mapping(“BASE\_URL” → Platform.utils.get\_site\_url(site), “NODE\_PATH” → node\_modules\_path).
- If parallel\_site.
  - Set env at “PARALLEL\_BASE\_URLS” from “,”.join(generator of \_get\_site\_url(s) for s drawn from parallel\_site).
    - Draw s from parallel\_site.
- If admin\_password bound to Platform.get\_conf().admin\_password.
  - Set env at “ADMIN\_PASSWORD” from admin\_password.
- Evaluate click.secho(“Running Playwright...”, fg = “yellow”).
- Evaluate Platform.commands.popen(shlex.join(command), cwd = app\_base\_path, env = env, raise\_err = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L116) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L598) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L574)

<a id="op-11adab6ce42260"></a>
### Run cypress

`operation_foundation_binding_foundation_commands_testing_run_cypress`

**Inputs** site, app\_base\_path, Platform\_path, headless, browser, spec, parallel\_site, runnerargs, parallel = false, with\_coverage = false, ci\_build\_id = no value.

**Local steps**

- Set node\_modules\_path from os.path.join(Platform\_path, “node\_modules”).
- Set cypress\_path from os.path.join(node\_modules\_path, “.bin”, “cypress”).
- Set installed from all(generator of os.path.exists(os.path.join(node\_modules\_path, name)) for name drawn from CYPRESS\_PACKAGES).
  - Draw name from CYPRESS\_PACKAGES.
- If not (os.path.exists(cypress\_path) and installed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.exists(cypress\_path) → installed.
  - Evaluate click.secho(“Installing Cypress...”, fg = “yellow”).
  - Set packages from one space.join(generator of formatted text {name}@{version} when version, otherwise name for tuple(name, version) drawn from CYPRESS\_PACKAGES.items()).
    - Draw tuple(name, version) from CYPRESS\_PACKAGES.items().
    - Value choice on version — true gives formatted text {name}@{version}, false gives name.
  - Evaluate \_yarn\_add(Platform\_path, packages).
- Set command from list(cypress\_path, “run”, “--browser”, (browser or “chrome”)) when headless, otherwise list(cypress\_path, “open”).
  - Value choice on headless — true gives list(cypress\_path, “run”, “--browser”, (browser or “chrome”)), false gives list(cypress\_path, “open”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in browser → “chrome”.
- If (headless and spec).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in headless → spec.
  - Evaluate command.extend(list(“--spec”, spec)).
- If os.environ.get(“CYPRESS\_RECORD\_KEY”).
  - Evaluate command.append(“--record”).
- If parallel.
  - Evaluate command.append(“--parallel”).
- If ci\_build\_id.
  - Evaluate command.extend(list(“--ci-build-id”, ci\_build\_id)).
- Evaluate command.extend(runnerargs).
- Set env from mapping(“CYPRESS\_baseUrl” → Platform.utils.get\_site\_url(site), “CYPRESS\_CLOUD\_PARALLEL” → “1” when parallel, otherwise “0”, “CYPRESS\_coverage” → str(with\_coverage).lower(), “NODE\_PATH” → node\_modules\_path).
  - Value choice on parallel — true gives “1”, false gives “0”.
- If admin\_password bound to Platform.get\_conf().admin\_password.
  - Set env at “CYPRESS\_adminPassword” from admin\_password.
- Evaluate click.secho(“Running Cypress...”, fg = “yellow”).
- Evaluate Platform.commands.popen(shlex.join(command), cwd = app\_base\_path, env = env, raise\_err = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L115) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L597) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L573)

## Service · Translate

<a id="op-f5609b81f8f2ef"></a>
### Build message files

`operation_foundation_commands_translate_business_behavior_build_message_files`

**Inputs** context.

**Wrappers, in declaration order** click.command(“build-message-files”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies Platform.translate.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate Platform.translate.rebuild\_all\_translation\_files().
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L650) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L724)

<a id="op-b6ce61a3002fbf"></a>
### New language

`operation_foundation_commands_translate_business_behavior_new_language`

**Inputs** context, lang\_code, app.

**Wrappers, in declaration order** click.command(“new-language”), click.argument(“lang\_code”), click.argument(“app”), pass\_context.

**Explicit failure paths** Exception(“--site is required”).

**Local steps**

- Bind dependencies Platform.translate.
- If not context.sites.
  - Raise Exception(“--site is required”).
- Evaluate Platform.init(site = context.sites at 0).
- Evaluate Platform.connect().
- Evaluate Platform.translate.write\_translations\_file(app, lang\_code).
- Evaluate print(formatted text File created at ./apps/{app}/{app}/translations/{lang\_code}.csv).
- Evaluate print(“You will need to add the language in Platform/geo/languages.csv, if you haven't done it already.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L217) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L654) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L728)

<a id="op-7e03f062c1d892"></a>
### Get untranslated

`operation_foundation_commands_translate_business_behavior_get_untranslated`

**Inputs** context, lang, untranslated\_file, app = “\_ALL\_APPS”, all = no value.

**Wrappers, in declaration order** click.command(“get-untranslated”), click.option(“--app”, default = “\_ALL\_APPS”), click.argument(“lang”), click.argument(“untranslated\_file”), click.option(“--all”, default = false, is\_flag = true, help = “Get all message strings”), pass\_context.

**Local steps**

- Bind dependencies Platform.translate.
- Set site from get\_site(context).
- Attempt the following.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Evaluate Platform.translate.get\_untranslated(lang, untranslated\_file, get\_all = all, app = app).
- On exit, including pending return or failure.
  - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L135) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L651) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L725)

<a id="op-9cbc948a87f09c"></a>
### Update translations

`operation_foundation_commands_translate_business_behavior_update_translations`

**Inputs** context, lang, untranslated\_file, translated\_file, app = “\_ALL\_APPS”.

**Wrappers, in declaration order** click.command(“update-translations”), click.option(“--app”, default = “\_ALL\_APPS”), click.argument(“lang”), click.argument(“untranslated\_file”), click.argument(“translated-file”), pass\_context.

**Local steps**

- Bind dependencies Platform.translate.
- Set site from get\_site(context).
- Attempt the following.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Evaluate Platform.translate.update\_translations(lang, untranslated\_file, translated\_file, app = app).
- On exit, including pending return or failure.
  - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L137) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L655) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L729)

<a id="op-97d472df58c2a6"></a>
### Import translations

`operation_foundation_commands_translate_business_behavior_import_translations`

**Inputs** context, lang, path.

**Wrappers, in declaration order** click.command(“import-translations”), click.argument(“lang”), click.argument(“path”), pass\_context.

**Local steps**

- Bind dependencies Platform.translate.
- Set site from get\_site(context).
- Attempt the following.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Evaluate Platform.translate.import\_translations(lang, path).
- On exit, including pending return or failure.
  - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L136) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L652) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L726)

<a id="op-cf1becfddbddad"></a>
### Migrate translations

`operation_foundation_commands_translate_business_behavior_migrate_translations`

**Inputs** context, source\_app, target\_app.

**Wrappers, in declaration order** click.command(“migrate-translations”), click.argument(“source-app”), click.argument(“target-app”), pass\_context.

**Local steps**

- Bind dependencies Platform.translate.
- Set site from get\_site(context).
- Attempt the following.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Evaluate Platform.translate.migrate\_translations(source\_app, target\_app).
- On exit, including pending return or failure.
  - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L1717) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L653) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L727)

## Service · Utils

<a id="op-3aa46b98434949"></a>
### Build

`operation_foundation_commands_utils_business_behavior_build`

**Inputs** app = no value, apps = no value, hard\_link = false, production = false, verbose = false, force = false, save\_metafiles = false, using\_cached = false.

**Wrappers, in declaration order** click.command(“build”), click.option(“--app”, help = “Build assets for app”), click.option(“--apps”, help = “Build assets for specific apps”), click.option(“--hard-link”, is\_flag = true, default = false, help = “Copy the files instead of symlinking”, envvar = “Platform\_HARD\_LINK\_ASSETS”), click.option(“--production”, is\_flag = true, default = false, help = “Build assets in production mode”), click.option(“--verbose”, is\_flag = true, default = false, help = “Verbose”), click.option(“--force”, is\_flag = true, default = false, help = “Force build assets instead of downloading available”), click.option(“--save-metafiles”, is\_flag = true, default = false, help = text in the contract), click.option(“--using-cached”, is\_flag = true, default = false, envvar = “USING\_CACHED”, help = “Skips build and uses cached build artifacts (cache is set by Bench). Ignored if developer\_mode enabled.”).

**Local steps**

- Bind dependencies build\_framework\_islands, bundle, download\_Platform\_assets.
- Bind dependencies compile\_translations.
- Bind dependencies filelock.
- Evaluate Platform.init(empty text).
- If (not apps and app).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not apps → app.
  - Set apps from app.
- Within filelock(“bench\_build”, is\_global = true, timeout = 10).
  - If not (force or apps or os.environ.get(“CI”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in force → apps → os.environ.get(“CI”).
    - Set skip\_Platform from download\_Platform\_assets(verbose = verbose).
  - Otherwise.
    - Set skip\_Platform from false.
  - Set development from (Platform.local.conf.developer\_mode or Platform.\_dev\_server).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.conf.developer\_mode → Platform.\_dev\_server.
  - Set esbuild\_target from (Platform.local.conf.get(“esbuild\_target”) or os.environ.get(“ESBUILD\_TARGET”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.conf.get(“esbuild\_target”) → os.environ.get(“ESBUILD\_TARGET”).
  - Set mode from “development” when development, otherwise “production”.
    - Value choice on development — true gives “development”, false gives “production”.
  - If production.
    - Set mode from “production”.
  - If development.
    - Set using\_cached from false.
  - Evaluate bundle(mode, apps = apps, hard\_link = hard\_link, verbose = verbose, skip\_Platform = skip\_Platform, …).
  - Evaluate build\_framework\_islands(production = mode equals “production”).
  - If (apps and isinstance(apps, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in apps → isinstance(apps, str).
    - Set apps from apps.split(“,”).
  - If not apps.
    - Set apps from Platform.get\_all\_apps().
  - For each app in apps.
    - Evaluate print(“Compiling translations for”, app).
    - Evaluate compile\_translations(app, force = force).
  - Evaluate run\_after\_build\_hook(apps).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L139) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L657) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L731)

<a id="op-288e969ec03aa7"></a>
### Run after build hook

`operation_foundation_commands_utils_business_behavior_run_after_build_hook`

**Inputs** built\_apps.

**Local steps**

- Bind dependencies import\_module.
- Bind local operation \_get\_method for subsequent calls.
- For each app in built\_apps.
  - For each fn in Platform.get\_hooks(“after\_build”, app\_name = app).
    - Evaluate \_get\_method(fn)().
- For each app in Platform.get\_all\_apps().
  - For each fn in Platform.get\_hooks(“after\_app\_build”, app\_name = app).
    - Evaluate \_get\_method(fn)(built\_apps).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“after\_build”, app\_name = app), Platform.get\_hooks(“after\_app\_build”, app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L3060) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L684) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L758)

<a id="op-140ddc5022c53a"></a>
### Run after build hook.get method

`operation_foundation_commands_utils_business_behavior_run_after_build_hook_get_method`

**Inputs** fn.

**Explicit results** getattr(import\_module(modulename), methodname).

**Local steps**

- Set modulename from “.”.join(fn.split(“.”) at slice no value to negative 1).
- Set methodname from fn.split(“.”) at negative 1.
- Return getattr(import\_module(modulename), methodname).

**Values supplied outside this operation** selected callable from getattr(import\_module(modulename), methodname).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L3460) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L685) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L759)

<a id="op-750ed7b48c466c"></a>
### Watch

`operation_foundation_commands_utils_business_behavior_watch`

**Inputs** apps = no value.

**Wrappers, in declaration order** click.command(“watch”), click.option(“--apps”, help = “Watch assets for specific apps”).

**Local steps**

- Bind dependencies watch.
- Evaluate Platform.init(empty text).
- Evaluate watch(apps).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L3630) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L694) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L768)

<a id="op-ab7288bb8ebef7"></a>
### Clear cache

`operation_foundation_commands_utils_business_behavior_clear_cache`

**Inputs** context.

**Wrappers, in declaration order** click.command(“clear-cache”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies Platform.sessions.
- Bind dependencies clear\_website\_cache.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate Platform.clear\_cache().
    - Evaluate clear\_website\_cache().
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L3770) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L659) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L733)

<a id="op-e01c578762236f"></a>
### Clear website cache

`operation_foundation_commands_utils_business_behavior_clear_website_cache`

**Inputs** context.

**Wrappers, in declaration order** click.command(“clear-website-cache”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies clear\_website\_cache.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate clear\_website\_cache().
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L4001) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L660) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L734)

<a id="op-386e9a637262ce"></a>
### Destroy all sessions

`operation_foundation_commands_utils_business_behavior_destroy_all_sessions`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** context, reason.

**Locally raised failures** SiteNotSpecifiedError.

**Observed service boundaries** transaction control.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L4211) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L667) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L741)

<a id="op-0ca0cf1da945a5"></a>
### Show config

`operation_foundation_commands_utils_business_behavior_show_configuration`

**Inputs** context, format.

**Wrappers, in declaration order** click.command(“show-config”), click.option(“--format”, “-f”, type = click.Choice(list(“text”, “json”)), default = “text”), pass\_context.

**State and service calls** call insert on data.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- If not context.sites.
  - Raise SiteNotSpecifiedError.
- Set sites\_config from mapping().
- Set sites\_path from os.getcwd().
- Bind dependencies render\_table.
- Bind local operation transform\_config for subsequent calls.
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - If (len(context.sites) differs from 1 and format equals “text”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(context.sites) differs from 1 → format equals “text”.
    - If context.sites.index(site) differs from 0.
      - Evaluate click.echo().
    - Evaluate click.secho(formatted text Site {site}, fg = “yellow”).
  - Set configuration from Platform.get\_site\_config(sites\_path = sites\_path, site\_path = site).
  - If format equals “text”.
    - Set data from transform\_config(configuration).
    - Evaluate data.insert(0, list(“Config”, “Value”)).
    - Evaluate render\_table(data).
  - If format equals “json”.
    - Set sites\_config at site from configuration.
  - Evaluate Platform.destroy().
- If format equals “json”.
  - Evaluate click.echo(Platform.as\_json(sites\_config)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L4479) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L689) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L763)

<a id="op-a2992132dcfe6e"></a>
### Show config.transform config

`operation_foundation_commands_utils_business_behavior_show_configuration_transform_configuration`

**Inputs** config, prefix = no value.

**Explicit results** site\_config.

**Local steps**

- Set prefix from formatted text {prefix}. when prefix, otherwise empty text.
  - Value choice on prefix — true gives formatted text {prefix}., false gives empty text.
- Set site\_config from list().
- For each tuple(conf, value) in config.items().
  - If isinstance(value, dict).
    - Update site\_config using + transform\_config(value, prefix = formatted text {prefix}{conf}).
  - Otherwise.
    - Set log\_value from json.dumps(value) when isinstance(value, list), otherwise value.
      - Value choice on isinstance(value, list) — true gives json.dumps(value), false gives value.
    - Update site\_config using + list(list(formatted text {prefix}{conf}, log\_value)).
- Return site\_config.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L5504) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L690) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L764)

<a id="op-53555cce4fc75e"></a>
### Reset perms

`operation_foundation_commands_utils_business_behavior_reset_perms`

**Inputs** context.

**Wrappers, in declaration order** click.command(“reset-perms”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies reset\_perms.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - For each d in Platform.db.sql\_list(query text (SELECT, Doc Type)).
      - Evaluate Platform.clear\_cache(doctype = d).
      - Evaluate reset\_perms(d).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L5832) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L683) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L757)

<a id="op-c42be067c7e8f4"></a>
### Execute

`operation_foundation_commands_utils_business_behavior_execute`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** context, method, args, kwargs, profile.

**Locally raised failures** SiteNotSpecifiedError.

**Observed service boundaries** transaction control.

**Local structure** 8 condition or selection sites, 1 statement loops and 2 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L142) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L669) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L743)

<a id="op-6151305eede67e"></a>
### Add to email queue

`operation_foundation_commands_utils_business_behavior_add_to_email_queue`

**Inputs** context, email\_path.

**Wrappers, in declaration order** click.command(“add-to-email-queue”), click.argument(“email-path”), pass\_context.

**State and service calls** sendmail · commit.

**Local steps**

- Set site from get\_site(context).
- If os.path.isdir(email\_path).
  - Within Platform.init\_site(site).
    - Evaluate Platform.connect().
    - For each email in os.listdir(email\_path).
      - Within open(os.path.join(email\_path, email)) bound as email\_data.
        - Set kwargs from json.load(email\_data).
        - Set kwargs at “delayed” from true.
        - Evaluate Platform.sendmail(expanded names kwargs).
        - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(expanded names kwargs).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L138) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L656) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L730)

<a id="op-d532a27035dfdd"></a>
### Export doc

`operation_foundation_commands_utils_business_behavior_export_record`

**Inputs** context, doctype, docname.

**Wrappers, in declaration order** click.command(“export-doc”), click.argument(“doctype”), click.argument(“docname”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies Platform.modules.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate Platform.modules.export\_doc(doctype, docname).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L6899) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L672) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L746)

<a id="op-116171d7c65f48"></a>
### Export json

`operation_foundation_commands_utils_business_behavior_export_structured_data`

**Inputs** context, doctype, path, name = no value.

**Wrappers, in declaration order** click.command(“export-json”), click.argument(“doctype”), click.argument(“path”), click.option(“--name”, help = “Export only one document”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies export\_json.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate export\_json(doctype, path, name = name).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L144) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L673) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L747)
