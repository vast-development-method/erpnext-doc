# Site operations and diagnostics · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-8e12d05b7d0abc"></a>
### Export csv

`operation_foundation_commands_utils_business_behavior_export_comma_separated_values`

**Inputs** context, doctype, path.

**Wrappers, in declaration order** click.command(“export-csv”), click.argument(“doctype”), click.argument(“path”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies export\_csv.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate export\_csv(doctype, path).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L143) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L670) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L744)

<a id="op-00b56abd93f137"></a>
### Export fixtures

`operation_foundation_commands_utils_business_behavior_export_fixtures`

**Inputs** context, app = no value.

**Wrappers, in declaration order** click.command(“export-fixtures”), click.option(“--app”, default = no value, help = “Export fixtures of a specific app”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies export\_fixtures.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate export\_fixtures(app = app).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0029.json#L7885) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L671) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L745)

<a id="op-f70a4e2574ad97"></a>
### Convert sidebar fixtures

`operation_foundation_commands_utils_business_behavior_convert_sidebar_fixtures`

**Inputs** context, app = no value, dry\_run = false.

**Wrappers, in declaration order** click.command(“convert-sidebar-fixtures”), click.option(“--app”, default = no value, help = “Convert one app's fixtures; omit for every installed app”), click.option(“--dry-run”, is\_flag = true, default = false, help = “Report what would be written”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies apps\_with\_old\_fixtures, convert\_app.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - If (app and app does not belong to Platform.get\_installed\_apps()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in app → app does not belong to Platform.get\_installed\_apps().
      - Evaluate click.secho(formatted text {app} is not installed on {site}., fg = “red”).
      - Continue with the next iteration or loop test.
    - Set apps from list(app) when app, otherwise sorted(apps\_with\_old\_fixtures()).
      - Value choice on app — true gives list(app), false gives sorted(apps\_with\_old\_fixtures()).
    - If not apps.
      - Evaluate click.secho(“No installed app still ships the old sidebar fixtures.”, fg = “green”).
    - For each name in apps.
      - Evaluate click.secho(formatted text  {name}, bold = true).
      - Set results from convert\_app(name, dry\_run = dry\_run).
      - If not results.
        - Evaluate click.echo(“  nothing to convert”).
      - For each result in results.
        - Set colour from mapping(“converted” → “green”, “already converted” → “cyan”).get(result at “state”, “yellow”).
        - Evaluate click.secho(formatted text   {result at “state”} {(result at “module” or result at “path”)}, fg = colour).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at “module” → result at “path”.
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0030.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L663) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L737)

<a id="op-4d91f885eeee17"></a>
### Import doc

`operation_foundation_commands_utils_business_behavior_import_record`

**Inputs** context, path, force = false.

**Wrappers, in declaration order** click.command(“import-doc”), click.argument(“path”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies import\_doc.
- If not os.path.exists(path).
  - Set path from os.path.join(“..”, path).
- If not os.path.exists(path).
  - Evaluate print(formatted text Invalid path {path}).
  - Evaluate sys.exit(1).
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate import\_doc(path).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L145) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L675) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L749)

<a id="op-d93c2a4c3720e8"></a>
### Data import

`operation_foundation_commands_utils_business_behavior_data_import`

**Inputs** context, file\_path, doctype, import\_type = no value, submit\_after\_import = false, mute\_emails = true.

**Wrappers, in declaration order** click.command(“data-import”), click.option(“--file”, “file\_path”, type = click.Path(exists = true, dir\_okay = false, resolve\_path = true), required = true, help = “Path to import file (.csv, .xlsx). Consider that relative paths will re …, click.option(“--doctype”, type = str, required = true), click.option(“--type”, “import\_type”, type = click.Choice(list(“Insert”, “Update”, “Upsert”), case\_sensitive = false), default = “Insert”, help = “Insert New Records, Update Existing Records, or Insert or  …, click.option(“--submit-after-import”, default = false, is\_flag = true, help = “Submit document after importing it”), click.option(“--mute-emails”, default = true, is\_flag = true, help = “Mute emails during import”), pass\_context.

**Local steps**

- Bind dependencies import\_file.
- Set site from get\_site(context).
- Evaluate Platform.init(site).
- Evaluate Platform.connect().
- Evaluate import\_file(doctype, file\_path, import\_type, submit\_after\_import, console = true).
- Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0030.json#L1314) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L665) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L739)

<a id="op-586bb9d140087a"></a>
### Bulk rename

`operation_foundation_commands_utils_business_behavior_bulk_rename`

**Inputs** context, doctype, path.

**Wrappers, in declaration order** click.command(“bulk-rename”), click.argument(“doctype”), click.argument(“path”), pass\_context.

**Local steps**

- Bind dependencies bulk\_rename.
- Bind dependencies read\_csv\_content.
- Set site from get\_site(context).
- Within open(path) bound as csvfile.
  - Set rows from read\_csv\_content(csvfile.read()).
- Evaluate Platform.init(site).
- Evaluate Platform.connect().
- Evaluate bulk\_rename(doctype, rows, via\_console = true).
- Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L140) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L658) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L732)

<a id="op-bb9cc3247a0bcd"></a>
### Database

`operation_foundation_commands_utils_business_behavior_database`

**Inputs** context, extra\_args.

**Wrappers, in declaration order** click.command(“db-console”, context\_settings = EXTRA\_ARGS\_CTX), click.argument(“extra\_args”, nargs = negative 1), pass\_context.

**Local steps**

- Set site from get\_site(context).
- Evaluate Platform.init(site).
- Evaluate \_enter\_console(extra\_args = extra\_args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0030.json#L2268) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L666) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L740)

<a id="op-4b78e21ae5bc8a"></a>
### Mariadb

`operation_foundation_commands_utils_business_behavior_relational_database`

**Inputs** context, extra\_args.

**Wrappers, in declaration order** click.command(“mariadb”, context\_settings = EXTRA\_ARGS\_CTX), click.argument(“extra\_args”, nargs = negative 1), pass\_context.

**Local steps**

- Set site from get\_site(context).
- Evaluate Platform.init(site).
- Set Platform.conf.db\_type from “mariadb”.
- Evaluate \_enter\_console(extra\_args = extra\_args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0030.json#L2460) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L680) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L754)

<a id="op-20dc83ddfcbde8"></a>
### Postgres

`operation_foundation_commands_utils_business_behavior_relational_database_2`

**Inputs** context, extra\_args.

**Wrappers, in declaration order** click.command(“postgres”, context\_settings = EXTRA\_ARGS\_CTX), click.argument(“extra\_args”, nargs = negative 1), pass\_context.

**Local steps**

- Set site from get\_site(context).
- Evaluate Platform.init(site).
- Set Platform.conf.db\_type from “postgres”.
- Evaluate \_enter\_console(extra\_args = extra\_args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0030.json#L2673) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L681) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L755)

<a id="op-b4e8e283f958b9"></a>
### Sqlite

`operation_foundation_commands_utils_business_behavior_sqlite`

**Inputs** context, extra\_args.

**Wrappers, in declaration order** click.command(“sqlite”, context\_settings = EXTRA\_ARGS\_CTX), click.argument(“extra\_args”, nargs = negative 1), pass\_context.

**Local steps**

- Set site from get\_site(context).
- Evaluate Platform.init(site).
- Set Platform.conf.db\_type from “sqlite”.
- Evaluate \_enter\_console(extra\_args = extra\_args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0030.json#L2886) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L691) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L765)

<a id="op-666d0e0582b1c7"></a>
### Enter console

`operation_foundation_commands_utils_business_behavior_enter_console`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** extra\_args.

**Observed service boundaries** validation or user-notification service.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0030.json#L3099) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L668) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L742)

<a id="op-7190f306004f16"></a>
### Jupyter

`operation_foundation_commands_utils_business_behavior_jupyter`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** context.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0030.json#L3683) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L676) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L750)

<a id="op-679593fc41e202"></a>
### Console cleanup

`operation_foundation_commands_utils_business_behavior_console_cleanup`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Observed service boundaries** transaction control.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0030.json#L4335) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L662) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L736)

<a id="op-7e043c66289d70"></a>
### Store logs

`operation_foundation_commands_utils_business_behavior_store_logs`

**Inputs** terminal.

**Declared result** no value.

**Local steps**

- Bind dependencies suppress.
- Set Platform.log\_level from 20.
- Within suppress(Exception).
  - Set logger from Platform.logger(“ipython”).
  - Evaluate logger.info(“=== bench console session ===”).
  - For each line in terminal.history\_manager.get\_range().
    - Evaluate logger.info(line at 2).
  - Evaluate logger.info(“=== session end ===”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0030.json#L4415) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L692) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L766)

<a id="op-85bf6131f82495"></a>
### Console

`operation_foundation_commands_utils_business_behavior_console`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** context, autoreload.

**Local structure** 2 condition or selection sites, 1 statement loops and 2 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L141) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L661) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L735)

<a id="op-c1f8603acf81a7"></a>
### Transform database

`operation_foundation_commands_utils_business_behavior_transform_database`

**Inputs** context, table, engine, row\_format, failfast.

**Wrappers, in declaration order** click.command(“transform-database”, help = “Change tables' internal settings changing engine and row formats”), click.option(“--table”, required = true, help = “Comma separated name of tables to convert. To convert all tables, pass 'all'”), click.option(“--engine”, default = no value, type = click.Choice(list(“InnoDB”, “MyISAM”)), help = “Choice of storage engine for said table(s)”), click.option(“--row\_format”, default = no value, type = click.Choice(list(“DYNAMIC”, “COMPACT”, “REDUNDANT”, “COMPRESSED”)), help = “Set ROW\_FORMAT parameter for said table(s)”), click.option(“--failfast”, is\_flag = true, default = false, help = “Exit on first failure occurred”), pass\_context.

**State and service calls** execute a supplied database query.

**Local steps**

- Set site from get\_site(context).
- Set check\_table from list().
- Set add\_line from false.
- Set skipped from 0.
- Evaluate Platform.init(site).
- If Platform.conf.db\_type differs from “mariadb”.
  - Evaluate click.secho(“This command only has support for MariaDB databases at this point”, fg = “yellow”).
  - Evaluate sys.exit(1).
- If not (engine or row\_format).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in engine → row\_format.
  - Evaluate click.secho(“Values for ′--engine′ or ′--row\_format′ must be set”).
  - Evaluate sys.exit(1).
- Evaluate Platform.connect().
- If table equals “all”.
  - Set information\_schema from Platform.qb.Schema(“information\_schema”).
  - Set queried\_tables from nested operand in the contract(nested operand in the contract).select(“table\_name”).where((nested operand in the contract.tables.row\_format differs from row\_format bitwise and nested operand in the contrac ….run().
  - Set tables from list of x at 0 for x drawn from queried\_tables.
    - Draw x from queried\_tables.
- Otherwise.
  - Set tables from list of x.strip() for x drawn from table.split(“,”).
    - Draw x from table.split(“,”).
- Set total from len(tables).
- For each tuple(current, table) in enumerate(tables).
  - Set values\_to\_set from empty text.
  - If engine.
    - Update values\_to\_set using + formatted text  ENGINE={engine}.
  - If row\_format.
    - Update values\_to\_set using + formatted text  ROW\_FORMAT={row\_format}.
  - Attempt the following.
    - Evaluate Platform.db.sql(formatted text ALTER TABLE ′{table}′{values\_to\_set}).
    - Evaluate update\_progress\_bar(“Updating table schema”, (current − skipped), total).
    - Set add\_line from true.
  - On failure (Exception) bound to e.
    - Evaluate check\_table.append(list(table, e.args)).
    - Update skipped using + 1.
    - If failfast.
      - Leave the innermost loop without its normal-exhaustion alternative.
- If add\_line.
  - Evaluate print().
- For each errored\_table in check\_table.
  - Set tuple(table, err) from errored\_table.
  - Set err\_msg from formatted text {table}: ERROR {err at 0}: {err at 1}.
  - Evaluate click.secho(err\_msg, fg = “yellow”).
- Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0030.json#L5406) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L693) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L767)

<a id="op-e120a2aa51990c"></a>
### Serve

`operation_foundation_commands_utils_business_behavior_serve`

**Inputs** context, port = no value, profile = false, proxy = false, no\_reload = false, no\_threading = false, sites\_path = “.”, site = no value, with\_coverage = false.

**Wrappers, in declaration order** click.command(“serve”), click.option(“--port”, default = 8000), click.option(“--profile”, is\_flag = true, default = false), click.option(“--proxy”, is\_flag = true, default = false, help = “The development server may be run behind a proxy, e.g. ngrok / localtunnel”), click.option(“--noreload”, “no\_reload”, is\_flag = true, default = false), click.option(“--nothreading”, “no\_threading”, is\_flag = true, default = false), click.option(“--with-coverage”, is\_flag = true, default = false), pass\_context.

**Local steps**

- Bind dependencies Platform.app.
- If not context.sites.
  - Set site from no value.
- Otherwise.
  - Set site from context.sites at 0.
- Within CodeCoverage(with\_coverage, “Platform”).
  - If with\_coverage.
    - Set no\_threading from true.
    - Set no\_reload from true.
  - Evaluate Platform.app.serve(port = port, profile = profile, proxy = proxy, no\_reload = no\_reload, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L148) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L686) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L760)

<a id="op-bde28a25460264"></a>
### Request

`operation_foundation_commands_utils_business_behavior_request`

**Inputs** context, args = no value, path = no value.

**Wrappers, in declaration order** click.command(“request”), click.option(“--args”, help = “arguments like ′?cmd=test&amp;key=value′ or ′/api/request/method?..′”), click.option(“--path”, help = “path to request JSON”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies Platform.api.
- Bind dependencies Platform.handler.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - If args.
      - If “?” belongs to args.
        - Set Platform.local.form\_dict from Platform.\_dict(list of a.split(“=”) for a drawn from nested operand in the contract.split(“?”) at negative 1.split(“&amp;”)).
          - Draw a from args.split(“?”) at negative 1.split(“&amp;”).
      - Otherwise.
        - Set Platform.local.form\_dict from Platform.\_dict().
      - If args.startswith(“/api/method”).
        - Set Platform.local.form\_dict.cmd from args.split(“?”, 1) at 0.split(“/”) at negative 1.
    - Otherwise.
      - If path.
        - Within open(os.path.join(“..”, path)) bound as f.
          - Set args from json.loads(f.read()).
        - Set Platform.local.form\_dict from Platform.\_dict(args).
    - Evaluate Platform.handler.execute\_cmd(Platform.form\_dict.cmd).
    - Evaluate print(Platform.response).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L147) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L682) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L756)

<a id="op-cbad0ce8d975e1"></a>
### Make app

`operation_foundation_commands_utils_business_behavior_make_application`

**Inputs** destination, app\_name, no\_git = false.

**Wrappers, in declaration order** click.command(“make-app”), click.argument(“destination”), click.argument(“app\_name”), click.option(“--no-git”, is\_flag = true, default = false, help = “Do not initialize git repository for the app”).

**Local steps**

- Bind dependencies get\_sites.
- If app\_name belongs to get\_sites().
  - Evaluate click.secho(formatted text Your bench has a site called {app\_name}, please choose another name for the app., fg = “red”).
  - Evaluate sys.exit(1).
- Bind dependencies make\_boilerplate.
- Evaluate make\_boilerplate(destination, app\_name, no\_git = no\_git).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L146) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L678) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L752)

<a id="op-a4cee13591f10b"></a>
### Create patch

`operation_foundation_commands_utils_business_behavior_create_patch`

**Inputs** no declared parameters.

**Wrappers, in declaration order** click.command(“create-patch”).

**Local steps**

- Bind dependencies PatchCreator.
- Set pc from PatchCreator().
- Evaluate pc.fetch\_user\_inputs().
- Evaluate pc.create\_patch\_file().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0031.json#L1185) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L664) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L738)

<a id="op-1f6c0a36b5fa7b"></a>
### Set config

`operation_foundation_commands_utils_business_behavior_set_configuration`

**Inputs** context, key, value, global\_ = false, parse = false.

**Wrappers, in declaration order** click.command(“set-config”), click.argument(“key”), click.argument(“value”), click.option(“-g”, “--global”, “global\_”, is\_flag = true, default = false, help = “Set value in bench config”), click.option(“-p”, “--parse”, is\_flag = true, default = false, help = “Evaluate as Python Object”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies update\_site\_config.
- If parse.
  - Bind dependencies ast.
  - Set value from ast.literal\_eval(value).
- If global\_.
  - Set sites\_path from os.getcwd().
  - Set common\_site\_config\_path from os.path.join(sites\_path, “common\_site\_config.json”).
  - Evaluate update\_site\_config(key, value, validate = false, site\_config\_path = common\_site\_config\_path).
- Otherwise.
  - If not context.sites.
    - Raise SiteNotSpecifiedError.
  - For each site in context.sites.
    - Evaluate Platform.init(site).
    - Evaluate update\_site\_config(key, value, validate = false).
    - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0031.json#L1295) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L687) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L761)

<a id="op-11bf3fdf7448cf"></a>
### Get version

`operation_foundation_commands_utils_business_behavior_get_version`

**Inputs** output.

**Wrappers, in declaration order** click.command(“version”), click.option(“-f”, “--format”, “output”, type = click.Choice(list(“plain”, “table”, “json”, “legacy”)), help = “Output format”, default = “plain”).

**Local steps**

- Bind dependencies Repo.
- Bind dependencies InvalidGitRepositoryError.
- Bind dependencies get\_app\_branch.
- Bind dependencies render\_table.
- Evaluate Platform.init(empty text).
- Set data from list().
- For each app in sorted(Platform.get\_all\_apps()).
  - Set module from Platform.get\_module(app).
  - Set app\_hooks from Platform.get\_module((app + “.hooks”)).
  - Set app\_info from Platform.\_dict().
  - Attempt the following.
    - Set app\_info.commit from Repo(nested operand in the contract.get\_app\_source\_path(app)).head.object.hexsha at slice no value to 7.
  - On failure (InvalidGitRepositoryError).
    - Set app\_info.commit from empty text.
  - Set app\_info.app from app.
  - Set app\_info.branch from get\_app\_branch(app).
  - Set app\_info.version from (getattr(app\_hooks, formatted text {app\_info.branch}\_version, no value) or module.\_\_version\_\_).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(app\_hooks, formatted text {app\_info.branch}\_version, no value) → module.\_\_version\_\_.
  - Evaluate data.append(app\_info).
- Evaluate mapping(“legacy” → deferred anonymous expression, “plain” → deferred anonymous expression, “table” → deferred anonymous expression, “json” → deferred anonymous expression) at output().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(app\_hooks, formatted text {app\_info.branch}\_version, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0031.json#L1848) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L674) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L748)

<a id="op-4b9e3d9b73ef84"></a>
### Rebuild global search

`operation_foundation_commands_utils_business_behavior_rebuild_global_search`

**Inputs** context, static\_pages = false.

**Wrappers, in declaration order** click.command(“rebuild-global-search”), click.option(“--static-pages”, is\_flag = true, default = false, help = “Rebuild global search for static pages”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies add\_route\_to\_global\_search, get\_doctypes\_with\_global\_search, get\_routes\_to\_index, rebuild\_for\_doctype, sync\_global\_search.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - If static\_pages.
      - Set routes from get\_routes\_to\_index().
      - For each tuple(i, route) in enumerate(routes).
        - Evaluate add\_route\_to\_global\_search(route).
        - Set Platform.local.request from no value.
        - Evaluate update\_progress\_bar(“Rebuilding Global Search”, i, len(routes)).
      - Evaluate sync\_global\_search().
    - Otherwise.
      - Set doctypes from get\_doctypes\_with\_global\_search().
      - For each tuple(i, doctype) in enumerate(doctypes).
        - Evaluate rebuild\_for\_doctype(doctype).
        - Evaluate update\_progress\_bar(“Rebuilding Global Search”, i, len(doctypes)).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0031.json#L2887) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L679) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L753)

<a id="op-3794088f7f8ad3"></a>
### List sites

`operation_foundation_commands_utils_business_behavior_list_sites`

**Inputs** context, output\_json = false.

**Wrappers, in declaration order** click.command(“list-sites”), click.option(“--json”, “output\_json”, is\_flag = true, help = “Output in JSON format”), pass\_context.

**Local steps**

- Set site\_dir from os.getcwd().
- Set common\_site\_config\_path from os.path.join(site\_dir, “common\_site\_config.json”).
- Set default\_site from no value.
- If os.path.exists(common\_site\_config\_path).
  - Within open(common\_site\_config\_path) bound as f.
    - Set config from json.load(f).
    - Set default\_site from config.get(“default\_site”).
- Set sites from list of site for site drawn from os.listdir(site\_dir) where (os.path.isdir(os.path.join(site\_dir, site)) and not site.startswith(“.”) and os.path.exists(os.path.join(site\_dir, site, “site\_config.json”))).
  - Draw site from os.listdir(site\_dir), keep a combination only if ((os.path.isdir(os.path.join(site\_dir, site)) and not site.startswith(“.”) and os.path.exists(os.path.join(site\_dir, site, “site\_config.json”)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.isdir(os.path.join(site\_dir, site)) → not site.startswith(“.”) → os.path.exists(os.path.join(site\_dir, site, “site\_config.json”)).
- If output\_json.
  - Evaluate click.echo(json.dumps(sites)).
- Otherwise.
  - If sites.
    - Evaluate click.echo(“Available sites:”).
    - For each site in sites.
      - If site equals default\_site.
        - Evaluate click.echo(formatted text \* {site}).
      - Otherwise.
        - Evaluate click.echo(formatted text   {site}).
  - Otherwise.
    - Evaluate click.echo(“No sites found”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0031.json#L3432) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L677) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L751)
