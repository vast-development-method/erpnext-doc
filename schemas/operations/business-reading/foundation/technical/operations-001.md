# Site operations and diagnostics · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Apps

<a id="op-aa9148a7eb2d4a"></a>
### Get docked apps

`operation_foundation_apps_business_behavior_get_docked_apps`

**Inputs** no declared parameters.

**Wrappers, in declaration order** request\_cache.

**Declared result** set at str.

**Explicit results** set(get\_app\_rail\_host\_map()).

**Local steps**

- Bind dependencies get\_app\_rail\_host\_map.
- Return set(get\_app\_rail\_host\_map()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0008.json#L6963) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L109) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L86)

<a id="op-38364015f04c58"></a>
### Get apps

`operation_foundation_apps_business_behavior_get_apps`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), request\_cache.

**Explicit results** app\_list.

**Local steps**

- Set apps from Platform.get\_installed\_apps().
- Set app\_list from list().
- For each app in apps.
  - If (app does not belong to get\_setup\_wizard\_completed\_apps() and app does not belong to get\_setup\_wizard\_not\_required\_apps() and “System Manager” does not belong to Platform.get\_roles()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in app does not belong to get\_setup\_wizard\_completed\_apps() → app does not belong to get\_setup\_wizard\_not\_required\_apps() → “System Manager” does not belong to Platform.get\_roles().
    - Continue with the next iteration or loop test.
  - If app equals “Platform”.
    - Continue with the next iteration or loop test.
  - Set app\_details from Platform.get\_hooks(“add\_to\_apps\_screen”, app\_name = app).
  - If not len(app\_details).
    - Continue with the next iteration or loop test.
  - For each app\_detail in app\_details.
    - Attempt the following.
      - Set has\_permission\_path from app\_detail.get(“has\_permission”).
      - If (has\_permission\_path and not Platform.get\_attr(has\_permission\_path)()).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_permission\_path → not Platform.get\_attr(has\_permission\_path)().
        - Continue with the next iteration or loop test.
      - Evaluate app\_list.append(mapping(“name” → app, “logo” → app\_detail.get(“logo”), “title” → translated app\_detail.get(“title”), “route” → app\_detail.get(“route”), …)).
        - Value choice on app\_detail.get(“setup\_wizard\_text”) — true gives translated app\_detail at “setup\_wizard\_text”, false gives no value.
    - On failure (Exception).
      - Evaluate Platform.log\_error(formatted text Failed to call has\_permission hook ({has\_permission\_path}) for {app}).
- Return app\_list.

**Values supplied outside this operation** effective access from Platform.get\_roles() · selected callable from Platform.get\_hooks(“add\_to\_apps\_screen”, app\_name = app), Platform.get\_attr(has\_permission\_path).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L25) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L106) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L84)

<a id="op-d8c8db9de64703"></a>
### Get route

`operation_foundation_apps_business_behavior_get_route`

**Inputs** app\_name.

**Explicit results** “/apps” · app.get(“route”) when (app and app.get(“route”)), otherwise “/apps”.

**Local steps**

- If app\_name does not belong to Platform.get\_installed\_apps().
  - Return “/apps”.
- Set apps from Platform.get\_hooks(“add\_to\_apps\_screen”, app\_name = app\_name).
- Set app from next(generator of app for app drawn from apps where app.get(“name”) equals app\_name, no value).
  - Draw app from apps, keep a combination only if (app.get(“name”) equals app\_name).
- Return app.get(“route”) when (app and app.get(“route”)), otherwise “/apps”.
  - Value choice on (app and app.get(“route”)) — true gives app.get(“route”), false gives “/apps”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in app → app.get(“route”).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“add\_to\_apps\_screen”, app\_name = app\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L26) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L112) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L88)

<a id="op-acb52987ff8970"></a>
### Is desk apps

`operation_foundation_apps_business_behavior_is_desk_apps`

**Inputs** apps.

**Explicit results** false · true.

**Local steps**

- For each app in apps.
  - Set route from app.get(“route”).
  - If (route and not re.match(DESK\_APP\_PATTERN, route)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in route → not re.match(DESK\_APP\_PATTERN, route).
    - Return false.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L944) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L113) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L89)

<a id="op-dab56e35910524"></a>
### Get default path

`operation_foundation_apps_business_behavior_get_default_path`

**Inputs** no declared parameters.

**Record and data access** read “User” via get\_cached\_value.

**Explicit results** no value · get\_route(system\_default\_app) · get\_route(user\_default\_app) · (\_apps at 0.get(“route”) or “/desk”) · “/desk” · 1 additional forms in the steps below.

**Local steps**

- Set apps from get\_apps().
- Set \_apps from list of app for app drawn from apps where app.get(“name”) differs from “Platform”.
  - Draw app from apps, keep a combination only if (app.get(“name”) differs from “Platform”).
- If len(\_apps) equals 0.
  - Return no value.
- Set system\_default\_app from Platform.get\_system\_settings(“default\_app”).
- Set user\_default\_app from Platform.get\_cached\_value(“User”, Platform.session.user, “default\_app”).
- If (system\_default\_app and not user\_default\_app).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in system\_default\_app → not user\_default\_app.
  - Return get\_route(system\_default\_app).
- Otherwise.
  - If user\_default\_app.
    - Return get\_route(user\_default\_app).
- If len(\_apps) equals 1.
  - Return (\_apps at 0.get(“route”) or “/desk”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_apps at 0.get(“route”) → “/desk”.
- Otherwise.
  - If is\_desk\_apps(\_apps).
    - Return “/desk”.
- Return “/apps”.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“default\_app”), Platform.get\_cached\_value(“User”, Platform.session.user, “default\_app”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L1082) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L107) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L85)

<a id="op-fe1ecfa3b101c9"></a>
### Set app as default

`operation_foundation_apps_business_behavior_set_application_as_default`

**Inputs** app\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “User” via get\_value.

**State and service calls** request set\_value on “User”.

**Explicit failure paths** validation helper — translated “App {} is not installed”.format(Platform.bold(app\_name)).

**Local steps**

- If app\_name does not belong to Platform.get\_installed\_apps().
  - Call the validation error handler Platform.throw(translated “App {} is not installed”.format(Platform.bold(app\_name))).
- If Platform.db.get\_value(“User”, Platform.session.user, “default\_app”) equals app\_name.
  - Evaluate Platform.db.set\_value(“User”, Platform.session.user, “default\_app”, empty text).
- Otherwise.
  - Evaluate Platform.db.set\_value(“User”, Platform.session.user, “default\_app”, app\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L27) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L114) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L90)

<a id="op-e772bde6529564"></a>
### Get incomplete setup route

`operation_foundation_apps_business_behavior_get_incomplete_setup_route`

**Inputs** current\_app, app\_route.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** app\_route · “app” · route.

**Local steps**

- Set pending\_apps from get\_apps\_with\_incomplete\_dependencies(current\_app).
- If not pending\_apps.
  - Return app\_route.
- For each app in pending\_apps.
  - If app equals “Platform”.
    - Return “app”.
  - Set app\_details from Platform.get\_hooks(“add\_to\_apps\_screen”, app\_name = app).
  - If not app\_details.
    - Continue with the next iteration or loop test.
  - If route bound to app\_details at 0.get(“route”).
    - Return route.
- Return app\_route.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“add\_to\_apps\_screen”, app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L1960) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L110) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L87)

## Service · Bundler

<a id="op-7a2d0a8b34dadb"></a>
### Download file

`operation_foundation_binding_foundation_bundler_download_file`

**Inputs** url, prefix.

**Explicit results** local\_filename.

**Local steps**

- Bind dependencies get.
- Set filename from urlparse(url).path.split(“/”) at negative 1.
- Set local\_filename from os.path.join(prefix, filename).
- Within get(url, stream = true, allow\_redirects = true) bound as r.
  - Evaluate r.raise\_for\_status().
  - Within open(local\_filename, “wb”) bound as f.
    - For each chunk in r.iter\_content(chunk\_size = 8192).
      - Evaluate f.write(chunk).
- Return local\_filename.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L104) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L586) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L562)

<a id="op-d03ef10bac5aa1"></a>
### Build missing files

`operation_foundation_binding_foundation_bundler_build_missing_files`

**Inputs** no declared parameters.

**Local steps**

- Set missing\_assets from list().
- Set current\_asset\_files from list().
- For each type in list(“css”, “js”).
  - Set folder from os.path.join(sites\_path, “assets”, “Platform”, “dist”, …).
  - Evaluate current\_asset\_files.extend(os.listdir(folder)).
- Set development from (Platform.local.conf.developer\_mode or Platform.\_dev\_server).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.conf.developer\_mode → Platform.\_dev\_server.
- Set build\_mode from “development” when development, otherwise “production”.
  - Value choice on development — true gives “development”, false gives “production”.
- Set assets\_json from Platform.read\_file(“assets/assets.json”).
- If assets\_json.
  - Set assets\_json from Platform.parse\_json(assets\_json).
  - For each tuple(bundle\_file, output\_file) in assets\_json.items().
    - If not output\_file.startswith(“/assets/Platform”).
      - Continue with the next iteration or loop test.
    - If os.path.basename(output\_file) does not belong to current\_asset\_files.
      - Evaluate missing\_assets.append(bundle\_file).
  - If missing\_assets.
    - Evaluate click.secho(“\\nBuilding missing assets...\\n”, fg = “yellow”).
    - Set files\_to\_build from list of (“Platform/” + name) for name drawn from missing\_assets.
      - Draw name from missing\_assets.
    - Evaluate bundle(build\_mode, files = files\_to\_build).
- Otherwise.
  - Evaluate bundle(build\_mode, apps = “Platform”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L103) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L585) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L561)

<a id="op-27e2d2fe2bb318"></a>
### Get assets link

`operation_foundation_binding_foundation_bundler_get_assets_link`

**Inputs** Platform\_head.

**Declared result** str.

**Explicit results** url.

**Explicit failure paths** AssetsDontExistError(formatted text Assets for {reference} don't exist).

**Local steps**

- Bind dependencies requests.
- Set tag from getoutput(“cd ../apps/Platform &amp;&amp; git show-ref --tags -d \| grep {} \| sed -e 's,.\* refs/tags/,,' -e 's/\\^{{}}//'”.format(Platform\_head)).
- If tag.
  - Set url from formatted command or address in the contract.
- Otherwise.
  - Set url from formatted command or address in the contract.
- If not requests.head(url).
  - Set reference from formatted text Release {tag} when tag, otherwise formatted text Commit {Platform\_head}.
    - Value choice on tag — true gives formatted text Release {tag}, false gives formatted text Commit {Platform\_head}.
  - Raise AssetsDontExistError(formatted text Assets for {reference} don't exist).
- Return url.

**Values supplied outside this operation** service or queued work from requests.head(url).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L107) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L589) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L565)

<a id="op-3c175a6f55a856"></a>
### Fetch assets

`operation_foundation_binding_foundation_bundler_fetch_assets`

**Inputs** url, Platform\_head.

**Explicit results** assets\_archive.

**Explicit failure paths** AssetsNotDownloadedError(formatted text Assets could not be retrived from {url}).

**Local steps**

- Evaluate click.secho(“Retrieving assets...”, fg = “yellow”).
- Set prefix from mkdtemp(prefix = “Platform-assets-”, suffix = Platform\_head).
- Set assets\_archive from download\_file(url, prefix).
- If not assets\_archive.
  - Raise AssetsNotDownloadedError(formatted text Assets could not be retrived from {url}).
- Evaluate click.echo((click.style(“✔”, fg = “green”) + formatted text  Downloaded Platform assets from {url})).
- Return assets\_archive.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L106) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L588) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L564)

<a id="op-de19c2c561c1f2"></a>
### Setup assets

`operation_foundation_binding_foundation_bundler_setup_assets`

**Inputs** assets\_archive.

**Explicit results** directories\_created.

**Local steps**

- Bind dependencies tarfile.
- Set directories\_created from set().
- Evaluate click.secho(“\\nExtracting assets...\\n”, fg = “yellow”).
- Within tarfile.open(assets\_archive) bound as tar.
  - For each file in tar.
    - If not file.isdir().
      - Set dest from (“.” + file.name.replace(“./Platform-bench/sites”, empty text)).
      - Set asset\_directory from os.path.dirname(dest).
      - Set show from dest.replace(“./assets/”, empty text).
      - If asset\_directory does not belong to directories\_created.
        - If not os.path.exists(asset\_directory).
          - Evaluate os.makedirs(asset\_directory, exist\_ok = true).
        - Evaluate directories\_created.add(asset\_directory).
      - Evaluate tar.makefile(file, dest).
      - Evaluate click.echo((click.style(“✔”, fg = “green”) + formatted text  Restored {show})).
- Return directories\_created.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L110) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L592) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L568)

<a id="op-5589743ef8a3f6"></a>
### Download Platform assets

`operation_foundation_binding_foundation_bundler_download_foundation_assets`

**Inputs** verbose = true.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Set Platform\_head from getoutput(“cd ../apps/Platform &amp;&amp; git rev-parse HEAD”).
- If not Platform\_head.
  - Return false.
- Attempt the following.
  - Set url from get\_assets\_link(Platform\_head).
  - Set assets\_archive from fetch\_assets(url, Platform\_head).
  - Evaluate setup\_assets(assets\_archive).
  - Evaluate build\_missing\_files().
  - Return true.
- On failure (AssetsDontExistError) bound to e.
  - Evaluate click.secho(str(e), fg = “yellow”).
- On failure (Exception) bound to e.
  - Evaluate click.secho(str(e), fg = “red”).
- On exit, including pending return or failure.
  - Attempt the following.
    - Evaluate shutil.rmtree(os.path.dirname(assets\_archive)).
  - On failure (Exception).
    - Take no action here.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L105) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L587) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L563)

<a id="op-62a3e621c01ef6"></a>
### Symlink

`operation_foundation_bundler_business_behavior_symlink`

**Inputs** target, link\_name, overwrite = false.

**Explicit results** os.symlink(target, link\_name).

**Explicit failure paths** IsADirectoryError(formatted text Cannot symlink over existing directory: '{link\_name}') · propagate active failure.

**Local steps**

- If not overwrite.
  - Return os.symlink(target, link\_name).
- While true.
  - Set temp\_link\_name from formatted text tmp{Platform.generate\_hash()}.
  - Attempt the following.
    - Evaluate os.symlink(target, temp\_link\_name).
    - Leave the innermost loop without its normal-exhaustion alternative.
  - On failure (FileExistsError).
    - Take no action here.
- Attempt the following.
  - If os.path.isdir(link\_name).
    - Raise IsADirectoryError(formatted text Cannot symlink over existing directory: '{link\_name}').
  - Attempt the following.
    - Evaluate shutil.move(temp\_link\_name, link\_name).
  - On failure (AttributeError).
    - Evaluate os.renames(temp\_link\_name, link\_name).
- On failure (Exception).
  - If os.path.islink(temp\_link\_name).
    - Evaluate os.remove(temp\_link\_name).
  - Propagate the active failure.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash().

**Boundaries to resolve** late-bound calls, callee failures, file state, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L6711) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L444) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L530)

<a id="op-efed4ab8548448"></a>
### Setup

`operation_foundation_bundler_business_behavior_setup`

**Inputs** no declared parameters.

**Local steps**

- Use module bindings app\_paths, assets\_path.
- Set pymodules from list().
- For each app in Platform.get\_all\_apps(true).
  - Attempt the following.
    - Evaluate pymodules.append(Platform.get\_module(app)).
  - On failure (ImportError).
    - Take no action here.
- Set app\_paths from list of os.path.dirname(pymodule.\_\_file\_\_) for pymodule drawn from pymodules.
  - Draw pymodule from pymodules.
- Set assets\_path from os.path.join(Platform.local.sites\_path, “assets”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L7138) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L442) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L528)

<a id="op-6d13823768097a"></a>
### Bundle

`operation_foundation_bundler_business_behavior_bundle`

**Inputs** mode, apps = no value, hard\_link = false, verbose = false, skip\_Platform = false, files = no value, save\_metafiles = false, using\_cached = false, esbuild\_target = no value.

**Local steps**

- Evaluate setup().
- Evaluate make\_asset\_dirs(hard\_link = hard\_link).
- Set mode from “production” when mode equals “production”, otherwise “build”.
  - Value choice on mode equals “production” — true gives “production”, false gives “build”.
- Set command from formatted text yarn run {mode}.
- If apps.
  - Update command using + formatted text  --apps {apps}.
- If esbuild\_target.
  - Update command using + formatted text  --esbuild-target {esbuild\_target}.
- If skip\_Platform.
  - Update command using + “ --skip\_Platform”.
- If files.
  - Update command using + “ --files {files}”.format(files = “,”.join(files)).
- If using\_cached.
  - Update command using + “ --using-cached”.
- Otherwise.
  - Update command using + “ --run-build-command”.
- If save\_metafiles.
  - Update command using + “ --save-metafiles”.
- Evaluate check\_node\_executable().
- Set Platform\_app\_path from Platform.get\_app\_source\_path(“Platform”).
- Evaluate Platform.commands.popen(command, cwd = Platform\_app\_path, env = get\_node\_env(), raise\_err = true).
- Within suppress(Exception).
  - Evaluate Platform.cache.flushdb().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L103) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L431) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L518)

<a id="op-eb53e6f88781e0"></a>
### Watch

`operation_foundation_bundler_business_behavior_watch`

**Inputs** apps = no value.

**Local steps**

- Evaluate setup().
- Set command from “yarn run watch”.
- If apps.
  - Update command using + formatted text  --apps {apps}.
- Set live\_reload from Platform.utils.cint(os.environ.get(“LIVE\_RELOAD”, Platform.conf.live\_reload)).
- If live\_reload.
  - Update command using + “ --live-reload”.
- Evaluate check\_node\_executable().
- Set Platform\_app\_path from Platform.get\_app\_source\_path(“Platform”).
- Set islands from list().
- If Platform.commands.popen(island\_build\_command(“install-toolchain.js”), cwd = Platform\_app\_path, env = get\_node\_env()).
  - Evaluate click.secho(“The island toolchain did not install, so islands are not watched.”, fg = “yellow”).
- Otherwise.
  - Set islands from list of watch\_islands(script) for script drawn from tuple(“build-framework.js”, “build-pages.js”).
    - Draw script from tuple(“build-framework.js”, “build-pages.js”).
- Set watchers from list(expanded islands, watch\_studio\_editor()).
- Attempt the following.
  - Evaluate Platform.commands.popen(command, cwd = Platform\_app\_path, env = get\_node\_env()).
- On exit, including pending return or failure.
  - For each process in watchers.
    - If process.
      - Evaluate process.terminate().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L106) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L446) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L532)

<a id="op-9ee8af2ed7fd28"></a>
### Island build command

`operation_foundation_binding_foundation_bundler_island_build_command`

**Inputs** script, production = false, watch = false.

**Declared result** str.

**Explicit results** command.

**Local steps**

- Set script from os.path.join(Platform.get\_app\_source\_path(“Platform”), “ui”, “vite”, “island”, …).
- Set command from formatted text node {shlex.quote(script)}.
- If production.
  - Update command using + “ --production”.
- If watch.
  - Update command using + “ --watch”.
- Return command.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L108) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L590) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L566)

<a id="op-881b18fe242837"></a>
### Build framework islands

`operation_foundation_binding_foundation_bundler_build_framework_islands`

**Inputs** production = false.

**Explicit failure paths** click.ClickException(formatted text The framework island build failed ({command}). Desk cannot draw its charts until this passes. If the island toolchain did not install, run: yarn insta).

**Local steps**

- Set Platform\_app\_path from Platform.get\_app\_source\_path(“Platform”).
- Set command from island\_build\_command(“build-framework.js”, production = production).
- If Platform.commands.popen(command, cwd = Platform\_app\_path, env = get\_node\_env()).
  - Set toolchain from os.path.join(Platform\_app\_path, “island-toolchain”).
  - Raise click.ClickException(formatted text The framework island build failed ({command}). Desk cannot draw its charts until this passes. If the island toolchain did not install, run: yarn insta).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L102) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L584) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L560)

<a id="op-cffe477ba7763b"></a>
### Build page islands

`operation_foundation_bundler_business_behavior_build_page_islands`

**Inputs** built\_apps = no value.

**Local steps**

- Set development from (Platform.local.conf.developer\_mode or Platform.\_dev\_server).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.conf.developer\_mode → Platform.\_dev\_server.
- Set command from island\_build\_command(“build-pages.js”, production = not development).
- If Platform.commands.popen(command, cwd = Platform.get\_app\_source\_path(“Platform”), env = get\_node\_env()).
  - Evaluate click.secho(formatted text The page-island build failed ({command}). Every Platform UI page shows its unbuilt state until this passes., fg = “red”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L102) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L430) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L517)

<a id="op-2ff43c1ce52387"></a>
### Watch studio editor

`operation_foundation_binding_foundation_bundler_watch_studio_editor`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** no value, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L112) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L594) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L570)

<a id="op-240f5476e1b6f3"></a>
### Watch islands

`operation_foundation_binding_foundation_bundler_watch_islands`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** script.

**Explicit result forms** no value, the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L111) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L593) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L569)

<a id="op-aaf914f634709c"></a>
### Check node executable

`operation_foundation_bundler_business_behavior_check_runtime_process_executable`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L1674) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L432) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L519)

<a id="op-0ee637d9a1c0c2"></a>
### Get node env

`operation_foundation_bundler_business_behavior_get_runtime_process_env`

**Inputs** no declared parameters.

**Explicit results** mapping(“NODE\_OPTIONS” → node\_options).

**Local steps**

- Set node\_options from os.environ.get(“NODE\_OPTIONS”, empty text).
- If (“--max-old-space-size” does not belong to node\_options and “--max\_old\_space\_size” does not belong to node\_options).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “--max-old-space-size” does not belong to node\_options → “--max\_old\_space\_size” does not belong to node\_options.
  - Set node\_options from formatted text {node\_options} --max\_old\_space\_size={get\_safe\_max\_old\_space\_size()}.strip().
- Return mapping(“NODE\_OPTIONS” → node\_options).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L104) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L436) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L523)
