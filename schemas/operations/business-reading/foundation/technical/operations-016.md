# Site operations and diagnostics · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Site

<a id="op-4d2b0973f55786"></a>
### Browse

`operation_foundation_commands_site_business_behavior_browse`

**Inputs** context, site, user = no value, session\_end = no value, user\_for\_audit = no value.

**Wrappers, in declaration order** click.command(“browse”), click.argument(“site”, required = false), click.option(“--user”, required = false, help = “Login as user”), click.option(“--session-end”, required = false, help = “Session end (in ISO8601 format and timezone-aware - 2025-01-24T12:26:29.200853+00:00)”), click.option(“--user-for-audit”, required = false, help = “The user to mention in audit trail”), pass\_context.

**Record and data access** read “User” via exists.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies CookieManager, LoginManager.
- Set site from (get\_site(context, raise\_err = false) or site).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_site(context, raise\_err = false) → site.
- If not site.
  - Raise SiteNotSpecifiedError.
- If site does not belong to Platform.utils.get\_sites().
  - Evaluate click.echo(formatted text  Site named {click.style(site, bold = true)} doesn't exist , err = true).
  - Evaluate sys.exit(1).
- Evaluate Platform.init(site).
- Evaluate Platform.connect().
- Set sid from empty text.
- If user.
  - If not Platform.db.exists(“User”, user).
    - Evaluate click.echo(formatted text User {user} does not exist).
    - Evaluate sys.exit(1).
  - If (Platform.conf.developer\_mode or user equals “Administrator”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.developer\_mode → user equals “Administrator”.
    - Evaluate Platform.utils.set\_request(path = “/”).
    - Set Platform.local.cookie\_manager from CookieManager().
    - Set Platform.local.login\_manager from LoginManager().
    - Evaluate Platform.local.login\_manager.login\_as(user, session\_end, user\_for\_audit).
    - Set sid from formatted text /app?sid={Platform.session.sid}.
  - Otherwise.
    - Evaluate click.echo(“Please enable developer mode to login as a user”).
- Set url from formatted text {Platform.utils.get\_site\_url(site)}{sid}.
- If user equals “Administrator”.
  - Evaluate click.echo(formatted text Login URL: {url}).
- Evaluate click.launch(url).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L122) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L522) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L604)

<a id="op-435e3066190763"></a>
### Start recording

`operation_foundation_commands_site_business_behavior_start_recording`

**Inputs** context.

**Wrappers, in declaration order** click.command(“start-recording”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies Platform.recorder.
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - Evaluate Platform.set\_user(“Administrator”).
  - Evaluate Platform.recorder.start().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0024.json#L2504) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L560) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L638)

<a id="op-6c24bd3018a6da"></a>
### Stop recording

`operation_foundation_commands_site_business_behavior_stop_recording`

**Inputs** context.

**Wrappers, in declaration order** click.command(“stop-recording”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies Platform.recorder.
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - Evaluate Platform.set\_user(“Administrator”).
  - Evaluate Platform.recorder.stop().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0024.json#L2692) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L561) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L639)

<a id="op-c693beef2bc97f"></a>
### Start ngrok

`operation_foundation_commands_site_business_behavior_start_ngrok`

**Inputs** context, bind\_tls, use\_default\_authtoken.

**Wrappers, in declaration order** click.command(“ngrok”), click.option(“--bind-tls”, is\_flag = true, default = false, help = “Returns a reference to the https tunnel.”), click.option(“--use-default-authtoken”, is\_flag = true, default = false, help = “Use the auth token present in ngrok's config.”), pass\_context.

**Local steps**

- Bind dependencies ngrok.
- Set site from get\_site(context).
- Evaluate Platform.init(site).
- Set ngrok\_authtoken from Platform.conf.ngrok\_authtoken.
- If not use\_default\_authtoken.
  - If not ngrok\_authtoken.
    - Evaluate click.echo(formatted command or address in the contract).
    - Evaluate sys.exit(1).
  - Evaluate ngrok.set\_auth\_token(ngrok\_authtoken).
- Set port from Platform.conf.http\_port.
- If (not port and Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not port → Platform.conf.developer\_mode.
  - Set port from Platform.conf.webserver\_port.
- Set tunnel from ngrok.connect(addr = str(port), host\_header = site, bind\_tls = bind\_tls).
- Evaluate print(formatted text Public URL: {tunnel.public\_url}).
- Evaluate print(text in the contract).
- Set ngrok\_process from ngrok.get\_ngrok\_process().
- Attempt the following.
  - Evaluate ngrok\_process.proc.wait().
- On failure (KeyboardInterrupt).
  - Evaluate print(“Shutting down server...”).
  - Evaluate Platform.destroy().
  - Evaluate ngrok.kill().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0024.json#L2880) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L559) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L637)

<a id="op-656822cf18b6d1"></a>
### Build search index

`operation_foundation_commands_site_business_behavior_build_search_index`

**Inputs** context.

**Wrappers, in declaration order** click.command(“build-search-index”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies build\_index\_for\_all\_routes.
- Set site from get\_site(context).
- If not site.
  - Raise SiteNotSpecifiedError.
- Evaluate print(formatted text Building search index for {site}).
- Evaluate Platform.init(site).
- Evaluate Platform.connect().
- Attempt the following.
  - Evaluate build\_index\_for\_all\_routes().
- On exit, including pending return or failure.
  - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0024.json#L3594) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L523) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L605)

<a id="op-f5ffa2a2826e64"></a>
### Clear log table

`operation_foundation_commands_site_business_behavior_clear_log_table`

**Inputs** context, doctype, days, no\_backup.

**Wrappers, in declaration order** click.command(“clear-log-table”), click.option(“--doctype”, required = true, type = str, help = “Log DocType”), click.option(“--days”, type = int, help = “Keep records for days”), click.option(“--no-backup”, is\_flag = true, default = false, help = “Do not backup the table”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError · Platform.ValidationError(formatted text Unsupported logging DocType: {doctype}).

**Local steps**

- Bind dependencies clear\_logs.
- Bind dependencies scheduled\_backup.
- If not context.sites.
  - Raise SiteNotSpecifiedError.
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - If doctype does not belong to Platform.get\_hooks(“default\_log\_clearing\_doctypes”, mapping()).
    - Raise Platform.ValidationError(formatted text Unsupported logging DocType: {doctype}).
  - If not no\_backup.
    - Evaluate scheduled\_backup(ignore\_conf = false, include\_doctypes = doctype, ignore\_files = true, force = true).
    - Evaluate click.echo(formatted text Backed up {doctype}).
  - Attempt the following.
    - Evaluate click.echo(formatted text Copying {doctype} records from last {days} days to temporary table.).
    - Evaluate clear\_logs(doctype, days = days).
  - On failure (Exception) bound to e.
    - Evaluate click.echo(formatted text Log cleanup for {doctype} failed: {e}).
    - Evaluate sys.exit(1).
  - When the protected block completes normally.
    - Evaluate click.secho(formatted text Cleared {doctype} records older than {days} days, fg = “green”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“default\_log\_clearing\_doctypes”, mapping()).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0024.json#L3838) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L525) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L607)

<a id="op-506750bbf4324f"></a>
### Trim database

`operation_foundation_commands_site_business_behavior_trim_database`

**Inputs** context, dry\_run, format, no\_backup, yes = false.

**Wrappers, in declaration order** click.command(“trim-database”), click.option(“--dry-run”, is\_flag = true, default = false, help = “Show what would be deleted”), click.option(“--format”, “-f”, default = “text”, type = click.Choice(list(“json”, “text”)), help = “Output format”), click.option(“--no-backup”, is\_flag = true, default = false, help = “Do not backup the site”), click.option(“--yes”, “-y”, help = “To bypass confirmation prompt.”, is\_flag = true, default = false), pass\_context.

**Record and data access** read “DocType” via get\_all.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- If not context.sites.
  - Raise SiteNotSpecifiedError.
- Bind dependencies scheduled\_backup.
- Set ALL\_DATA from mapping().
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Set TABLES\_TO\_DROP from list().
  - Set STANDARD\_TABLES from get\_standard\_tables().
  - Set information\_schema from Platform.qb.Schema(“information\_schema”).
  - Set table\_name from Platform.qb.Field(“table\_name”).as\_(“name”).
  - Set database\_tables from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.table\_schema equals nested operand in the contract.db\_name).where(information\_schema.tables.table\_type eq ….
  - Set doctype\_tables from Platform.get\_all(“DocType”, pluck = “name”).
  - For each table\_name in database\_tables.
    - If not table\_name.startswith(“tab”).
      - Continue with the next iteration or loop test.
    - If (table\_name.replace(“tab”, empty text, 1) does not belong to doctype\_tables and table\_name does not belong to STANDARD\_TABLES).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in table\_name.replace(“tab”, empty text, 1) does not belong to doctype\_tables → table\_name does not belong to STANDARD\_TABLES.
      - Evaluate TABLES\_TO\_DROP.append(table\_name).
  - If not TABLES\_TO\_DROP.
    - If format equals “text”.
      - Evaluate click.secho(formatted text {site}: No ghost tables, fg = “green”).
  - Otherwise.
    - If format equals “text”.
      - Evaluate print(formatted text {site}: Following tables will be dropped:).
      - Evaluate print(whitespace '\\n'.join(generator of formatted text \* {dt} for dt drawn from TABLES\_TO\_DROP)).
        - Draw dt from TABLES\_TO\_DROP.
    - If dry\_run.
      - Continue with the next iteration or loop test.
    - If not yes.
      - Evaluate click.confirm(“Do you want to continue?”, abort = true).
    - If not no\_backup.
      - If format equals “text”.
        - Evaluate print(formatted text Backing Up Tables: {“, ”.join(TABLES\_TO\_DROP)}).
      - Set odb from scheduled\_backup(ignore\_conf = false, include\_doctypes = “,”.join(generator of x.replace(“tab”, empty text, 1) for x drawn from TABLES\_TO\_DROP), ignore\_files = true, force = true).
        - Draw x from TABLES\_TO\_DROP.
      - If format equals “text”.
        - Evaluate odb.print\_summary().
        - Evaluate print(“\\nTrimming Database”).
    - For each table in TABLES\_TO\_DROP.
      - If format equals “text”.
        - Evaluate print(formatted text \* Dropping Table '{table}'...).
      - Evaluate Platform.db.sql\_ddl(formatted text drop table ′{table}′).
    - Set ALL\_DATA at Platform.local.site from TABLES\_TO\_DROP.
  - Evaluate Platform.destroy().
- If format equals “json”.
  - Bind dependencies json.
  - Evaluate print(json.dumps(ALL\_DATA, indent = 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0024.json#L4611) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L563) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L641)

<a id="op-c4a24b1cfa0a4a"></a>
### Get standard tables

`operation_foundation_commands_site_business_behavior_get_standard_tables`

**Inputs** no declared parameters.

**Explicit results** tables.

**Local steps**

- Bind dependencies re.
- Set tables from list().
- Set sql\_file from os.path.join(“..”, “apps”, “Platform”, “Platform”, …).
- Set content from open(sql\_file).read().splitlines().
- For each line in content.
  - Set table\_found from re.search(query text (CREATE), line).
  - If table\_found.
    - Evaluate tables.append(table\_found.group(2)).
- Return tables.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0024.json#L6293) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L534) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L613)

<a id="op-c8cf18816c22dc"></a>
### Trim tables

`operation_foundation_commands_site_business_behavior_trim_tables`

**Inputs** context, dry\_run, format, no\_backup.

**Wrappers, in declaration order** click.command(“trim-tables”), click.option(“--dry-run”, is\_flag = true, default = false, help = “Show what would be deleted”), click.option(“--format”, “-f”, default = “table”, type = click.Choice(list(“json”, “table”)), help = “Output format”), click.option(“--no-backup”, is\_flag = true, default = false, help = “Do not backup the site”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- If not context.sites.
  - Raise SiteNotSpecifiedError.
- Bind dependencies trim\_tables.
- Bind dependencies scheduled\_backup.
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - If not (no\_backup or dry\_run).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in no\_backup → dry\_run.
    - Evaluate click.secho(formatted text Taking backup for {Platform.local.site}, fg = “green”).
    - Set odb from scheduled\_backup(ignore\_files = false, force = true).
    - Evaluate odb.print\_summary().
  - Attempt the following.
    - Set trimmed\_data from trim\_tables(dry\_run = dry\_run, quiet = format equals “json”).
    - If (format equals “table” and not dry\_run).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in format equals “table” → not dry\_run.
      - Evaluate click.secho(formatted text The following data have been removed from {Platform.local.site}, fg = “green”).
    - Evaluate handle\_data(trimmed\_data, format = format).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0024.json#L6593) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L564) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L642)

<a id="op-074a852190df5f"></a>
### Handle data

`operation_foundation_commands_site_business_behavior_handle_data`

**Inputs** data, format = “json”.

**Local steps**

- If format equals “json”.
  - Bind dependencies json.
  - Evaluate print(json.dumps(mapping(Platform.local.site → data), indent = 1, sort\_keys = true)).
- Otherwise.
  - Bind dependencies render\_table.
  - Set data from (list(list(“DocType”, “Fields”)) + list of list(table, “, ”.join(columns)) for tuple(table, columns) drawn from data.items()).
    - Draw tuple(table, columns) from data.items().
  - Evaluate render\_table(data).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0024.json#L7329) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L535) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L614)

<a id="op-1c366863c229a7"></a>
### Add new user

`operation_foundation_commands_site_business_behavior_add_new_user`

**Inputs** email, first\_name = no value, last\_name = no value, user\_type = “System User”, send\_welcome\_email = false, password = no value, role = no value.

**State and service calls** request new\_doc for “User” · call insert on user.

**Local steps**

- Set user from Platform.new\_doc(“User”).
- Evaluate user.update(mapping(“name” → email, “email” → email, “enabled” → 1, “first\_name” → (first\_name or email), …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in first\_name → email.
  - Value choice on send\_welcome\_email — true gives 1, false gives 0.
- Evaluate user.insert().
- Evaluate user.add\_roles(expanded role).
- If password.
  - Bind dependencies update\_password.
  - Evaluate update\_password(user = user.name, pwd = password).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0024.json#L7625) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L517) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L599)

<a id="op-44f772526ae733"></a>
### Ensure app not Platform

`operation_foundation_commands_site_business_behavior_ensure_application_not_foundation`

**Inputs** app.

**Declared result** no value.

**Local steps**

- If app equals “Platform”.
  - Evaluate click.secho(“You cannot remove or uninstall the app ′Platform′”, fg = “red”).
  - Evaluate sys.exit(1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0025.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L532) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L612)

<a id="op-b78e949648e0d2"></a>
### Bypass patch

`operation_foundation_commands_site_business_behavior_bypass_patch`

**Inputs** context, patch\_name, yes.

**Wrappers, in declaration order** click.command(“bypass-patch”), click.argument(“patch\_name”), click.option(“--yes”, “-y”, is\_flag = true, default = false, help = “Pass --yes to skip confirmation”), pass\_context.

**State and service calls** commit.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies update\_patch\_log.
- If not context.sites.
  - Raise SiteNotSpecifiedError.
- If not yes.
  - Evaluate click.confirm(formatted text This will bypass the patch {patch\_name} forever and register it as successful. Are you sure you want to continue?, abort = true).
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Attempt the following.
    - Evaluate update\_patch\_log(patch\_name).
    - Evaluate Platform.db.commit().
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0025.json#L120) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L524) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L606)

<a id="op-77f577b3edfed7"></a>
### Sync desktop icons

`operation_foundation_commands_site_business_behavior_sync_desktop_icons`

**Inputs** context.

**Wrappers, in declaration order** click.command(“sync-desktop-icons”), pass\_context.

**Local steps**

- Bind dependencies import\_desktop\_icon\_fixtures.
- Bind dependencies is\_desktop\_icons\_page.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - If not is\_desktop\_icons\_page().
      - Evaluate click.secho(formatted text {site} is on the Apps desktop and holds no icon rows; switch Desktop Settings -&gt; Desktop Page to sync icons., fg = “yellow”).
      - Continue with the next iteration or loop test.
    - Evaluate click.secho(formatted text Syncing icons for {site}).
    - Evaluate import\_desktop\_icon\_fixtures(force = true).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0025.json#L520) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L562) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L640)

## Service · Testing

<a id="op-2496d044448bf7"></a>
### Main

`operation_foundation_commands_testing_business_behavior_main`

**Inputs** site = no value, app = no value, module = no value, doctype = no value, module\_def = no value, verbose = false, tests = tuple(), force = false, profile = false, junit\_xml\_output = no value, doctype\_list\_path = no value, failfast = false, case = no value, skip\_before\_tests = false, debug = false, debug\_exceptions = no value, selected\_categories = no value, lightmode = false.

**Declared result** no value.

**Explicit results** no value · results.

**Explicit failure paths** click.UsageError(“Error: The following arguments are mutually exclusive: doctype, doctype\_list\_path, module\_def, and module. P …”).

**Local steps**

- If lightmode.
  - Bind dependencies TestParameters.
  - Set test\_params from TestParameters(site = site, app = app, module = module, doctype = doctype, …).
  - Evaluate run\_tests\_in\_light\_mode(test\_params).
  - Return no value.
- Bind dependencies logging.
- Bind dependencies TestConfig, TestRunner, discover\_all\_tests, discover\_doctype\_tests, discover\_module\_tests.
- Bind dependencies \_cleanup\_after\_tests, \_initialize\_test\_environment.
- Bind dependencies \_clear\_test\_log.
- Evaluate \_clear\_test\_log().
- If (debug and not debug\_exceptions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in debug → not debug\_exceptions.
  - Set debug\_exceptions from tuple(Exception).
- Set testing\_module\_logger from logging.getLogger(“Platform.testing”).
- Evaluate testing\_module\_logger.setLevel(logging.DEBUG when verbose, otherwise logging.INFO).
  - Value choice on verbose — true gives logging.DEBUG, false gives logging.INFO.
- Set start\_time from time.time().
- Set exclusive\_args from list(doctype, doctype\_list\_path, module\_def, module).
- If sum(generator of arg is distinct from no value for arg drawn from exclusive\_args) &gt; 1.
  - Draw arg from exclusive\_args.
  - Raise click.UsageError(“Error: The following arguments are mutually exclusive: doctype, doctype\_list\_path, module\_def, and module. P …”).
- Set debug\_params from list().
- For each param\_name in list(“site”, “app”, “module”, “doctype”, …).
  - Set param\_value from locals() at param\_name.
  - If param\_value is distinct from no value.
    - Evaluate debug\_params.append(formatted text {param\_name}={param\_value}).
- If debug\_params.
  - Evaluate click.secho(formatted text Starting test run with parameters: {“, ”.join(debug\_params)}, fg = “cyan”, bold = true).
  - Evaluate testing\_module\_logger.info(formatted text started with: {“, ”.join(debug\_params)}).
- Otherwise.
  - Evaluate click.secho(“Starting test run with no specific parameters”, fg = “cyan”, bold = true).
  - Evaluate testing\_module\_logger.info(“started with no specific parameters”).
- For each handler in testing\_module\_logger.handlers.
  - If file bound to getattr(handler, “baseFilename”, no value).
    - Evaluate click.secho(formatted text View detailed logs{“ (using --verbose)” when not verbose, otherwise empty text}: {click.style(file, bold = true)}).
      - Value choice on not verbose — true gives “ (using --verbose)”, false gives empty text.
- Set test\_config from TestConfig(profile = profile, failfast = failfast, tests = tests, case = case, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in selected\_categories → list().
- Evaluate \_initialize\_test\_environment(site, test\_config).
- Set xml\_output\_file from \_setup\_xml\_output(junit\_xml\_output).
- Attempt the following.
  - Set runner from TestRunner(verbosity = 2 when testing\_module\_logger.getEffectiveLevel() &lt; logging.INFO, otherwise 1, tb\_locals = testing\_module\_logger.getEffectiveLevel() ≤ logging.INFO, cfg = test\_config, buffer = not debug).
    - Value choice on testing\_module\_logger.getEffectiveLevel() &lt; logging.INFO — true gives 2, false gives 1.
  - If (doctype or doctype\_list\_path).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → doctype\_list\_path.
    - Set doctype from \_load\_doctype\_list(doctype\_list\_path) when doctype\_list\_path, otherwise doctype.
      - Value choice on doctype\_list\_path — true gives \_load\_doctype\_list(doctype\_list\_path), false gives doctype.
    - Evaluate discover\_doctype\_tests(doctype, runner, app, force).
  - Otherwise.
    - If module\_def.
      - Evaluate \_run\_module\_def\_tests(app, module\_def, runner, force).
    - Otherwise.
      - If module.
        - Evaluate discover\_module\_tests(module, runner, app).
      - Otherwise.
        - Set apps from list(app) when app, otherwise Platform.get\_installed\_apps().
          - Value choice on app — true gives list(app), false gives Platform.get\_installed\_apps().
        - Evaluate discover\_all\_tests(apps, runner).
  - Set results from list().
  - Use module bindings unittest\_runner.
  - For each tuple(app, category, suite) in runner.iterRun().
    - Evaluate click.secho(formatted text  Running {suite.countTestCases()} {category} tests for {app}, fg = “cyan”, bold = true).
    - Set main\_runner from unittest\_runner when (junit\_xml\_output and unittest\_runner), otherwise runner.
      - Value choice on (junit\_xml\_output and unittest\_runner) — true gives unittest\_runner, false gives runner.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in junit\_xml\_output → unittest\_runner.
    - Set res from main\_runner.run(suite).
    - Evaluate results.append(list(app, category, res)).
  - Set success from all(generator of r.wasSuccessful() for tuple(\_, \_, r) drawn from results).
    - Draw tuple(\_, \_, r) from results.
  - If not success.
    - Evaluate sys.exit(1).
  - Return results.
- On exit, including pending return or failure.
  - Evaluate \_cleanup\_after\_tests().
  - If xml\_output\_file.
    - Evaluate xml\_output\_file.close().
  - Set end\_time from time.time().
  - Evaluate testing\_module\_logger.debug(formatted text Total test run time: {(end\_time − start\_time)} seconds).

**Values supplied outside this operation** selected callable from getattr(handler, “baseFilename”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L131) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L642) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L717)

<a id="op-466b7d5e405e63"></a>
### Run tests in light mode

`operation_foundation_commands_testing_business_behavior_run_tests_in_light_mode`

**Inputs** test\_params.

**Local steps**

- Bind dependencies cProfile.
- Bind dependencies pstats.
- Bind dependencies StringIO.
- Bind dependencies PlatformTestLoader.
- Bind dependencies PlatformTestResult.
- Bind dependencies toggle\_test\_mode.
- Evaluate Platform.init(test\_params.site).
- If not Platform.db.
  - Evaluate Platform.connect().
- Use module bindings scheduler\_disabled\_by\_user.
- Set scheduler\_disabled\_by\_user from Platform.utils.scheduler.is\_scheduler\_disabled(verbose = false).
- If not scheduler\_disabled\_by\_user.
  - Evaluate Platform.utils.scheduler.disable\_scheduler().
- Evaluate Platform.clear\_cache().
- Evaluate toggle\_test\_mode(true).
- Set suite from PlatformTestLoader().discover\_tests(test\_params).
- If test\_params.profile.
  - Set pr from cProfile.Profile().
  - Evaluate pr.enable().
- Set result from unittest.TextTestRunner(failfast = test\_params.failfast, resultclass = PlatformTestResult).run(suite).
- If test\_params.profile.
  - Evaluate pr.disable().
  - Set s from StringIO().
  - Set ps from pstats.Stats(pr, stream = s).sort\_stats(“cumulative”).
  - Evaluate ps.print\_stats().
  - Evaluate print(s.getvalue()).
- If not result.wasSuccessful().
  - Evaluate sys.exit(1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0028.json#L2564) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L647) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L721)

<a id="op-dd088943cda19d"></a>
### Setup xml output

`operation_foundation_commands_testing_business_behavior_setup_extensible_markup_output`

**Inputs** junit\_xml\_output.

**Explicit results** xml\_output\_file · no value.

**Local steps**

- Use module bindings unittest\_runner.
- Bind dependencies unittest.
- If junit\_xml\_output.
  - Set xml\_output\_file from open(junit\_xml\_output, “wb”).
  - Attempt the following.
    - Bind dependencies xmlrunner.
    - Set unittest\_runner from xmlrunner.XMLTestRunner(output = xml\_output\_file).
  - On failure (ImportError).
    - Evaluate print(“xmlrunner not found. Please install it to use XML output.”).
    - Set unittest\_runner from unittest.TextTestRunner().
  - Return xml\_output\_file.
- Otherwise.
  - Set unittest\_runner from unittest.TextTestRunner().
  - Return no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0028.json#L3212) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L649) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L723)

<a id="op-54c50ab9e4c253"></a>
### Load doctype list

`operation_foundation_commands_testing_business_behavior_load_record_type_list`

**Inputs** doctype\_list\_path.

**Explicit results** f.read().strip().splitlines().

**Local steps**

- Set tuple(app, path) from doctype\_list\_path.split(os.path.sep, 1).
- Within open(Platform.get\_app\_path(app, path)) bound as f.
  - Return f.read().strip().splitlines().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0028.json#L3443) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L641) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L716)

<a id="op-2666077c1601b9"></a>
### Run module def tests

`operation_foundation_commands_testing_business_behavior_run_module_def_tests`

**Inputs** app, module\_def, runner, force.

**Declared result** “TestRunner”.

**Explicit results** discover\_doctype\_tests(doctypes, runner, app, force).

**Local steps**

- Bind dependencies discover\_doctype\_tests.
- Set doctypes from \_get\_doctypes\_for\_module\_def(app, module\_def).
- Return discover\_doctype\_tests(doctypes, runner, app, force).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0028.json#L3614) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L644) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L718)

<a id="op-e8ca8cc22bd8bc"></a>
### Get doctypes for module def

`operation_foundation_commands_testing_business_behavior_get_record_types_for_module_def`

**Inputs** app, module\_def.

**Record and data access** read “DocType” via get\_list.

**Explicit results** doctypes.

**Local steps**

- Set doctypes from list().
- Set doctypes\_ from Platform.get\_list(“DocType”, filters = mapping(“module” → module\_def, “istable” → 0), fields = list(“name”, “module”), as\_list = true).
- Bind dependencies get\_module\_name.
- For each tuple(doctype, module) in doctypes\_.
  - Set test\_module from get\_module\_name(doctype, module, “test\_”, app = app).
  - Attempt the following.
    - Bind dependencies importlib.
    - Evaluate importlib.import\_module(test\_module).
    - Evaluate doctypes.append(doctype).
  - On failure (Exception).
    - Take no action here.
- Return doctypes.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0028.json#L3752) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L640) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L715)

<a id="op-23de10fe2160bc"></a>
### Run tests

`operation_foundation_commands_testing_business_behavior_run_tests`

**Inputs** context, app = no value, module = no value, doctype = no value, module\_def = no value, test = tuple(), profile = false, coverage = false, junit\_xml\_output = false, doctype\_list\_path = no value, skip\_test\_records = false, skip\_before\_tests = false, failfast = false, case = no value, test\_category = “all”, lightmode = false, debug = false.

**Wrappers, in declaration order** click.command(“run-tests”), click.option(“--app”, help = “For App”), click.option(“--doctype”, help = “For DocType”), click.option(“--module-def”, help = “For all Doctypes in Module Def”), click.option(“--case”, help = “Select particular TestCase”), click.option(“--doctype-list-path”, help = “Path to .txt file for list of doctypes. Example Enterprise/tests/server/agriculture.txt”), click.option(“--test”, multiple = true, help = “Specific test”), click.option(“--module”, help = “Run tests in a module”), click.option(“--debug”, is\_flag = true, default = false, help = “Disable buffer and attach to pdb on breakpoint or exception”), click.option(“--profile”, is\_flag = true, default = false), click.option(“--coverage”, is\_flag = true, default = false), click.option(“--skip-test-records”, is\_flag = true, default = false, help = “DEPRECATED”), click.option(“--skip-before-tests”, is\_flag = true, default = false, help = “Don't run before tests hook”), click.option(“--junit-xml-output”, help = “Destination file path for junit xml report”), click.option(“--failfast”, is\_flag = true, default = false, help = “Stop the test run on the first error or failure”), click.option(“--test-category”, type = click.Choice(list(“unit”, “integration”, “all”)), default = “all”, help = “Select test category to run”), click.option(“--lightmode”, is\_flag = true, default = false), pass\_context.

**Explicit results** no value.

**Local steps**

- Bind dependencies CodeCoverage.
- Within CodeCoverage(coverage, app).
  - Bind dependencies Platform.
  - Set tests from test.
  - Set site from get\_site(context).
  - Evaluate Platform.init(site).
  - Set allow\_tests from Platform.conf.allow\_tests.
  - If not (allow\_tests or os.environ.get(“CI”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in allow\_tests → os.environ.get(“CI”).
    - Evaluate click.secho(“Testing is disabled for the site!”, bold = true).
    - Evaluate click.secho(“You can enable tests by entering following command:”).
    - Evaluate click.secho(formatted text bench --site {site} set-config allow\_tests true, fg = “green”).
    - Return no value.
  - If skip\_test\_records.
    - Evaluate click.secho(“--skip-test-records is deprecated and without effect!”, bold = true).
    - Evaluate click.secho(“All records are loaded lazily on first use, so the flag is useless, now.”).
    - Evaluate click.secho(“Simply remove the flag.”, fg = “green”).
    - Return no value.
  - Evaluate main(site, app, module, doctype, tests = tests, force = context.force, profile = profile, junit\_xml\_output = junit\_xml\_output, …).
    - Value choice on test\_category equals “all” — true gives list(), false gives test\_category.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L133) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L646) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L720)

<a id="op-d5c299067fdc61"></a>
### Run parallel tests

`operation_foundation_commands_testing_business_behavior_run_parallel_tests`

**Inputs** context, app, build\_number, total\_builds, with\_coverage = false, use\_orchestrator = false, dry\_run = false, lightmode = false.

**Wrappers, in declaration order** click.command(“run-parallel-tests”), click.option(“--app”, help = “For App”, default = “Platform”), click.option(“--build-number”, help = “Build number”, default = 1), click.option(“--total-builds”, help = “Total number of builds”, default = 1), click.option(“--with-coverage”, is\_flag = true, help = “Build coverage file”, envvar = “CAPTURE\_COVERAGE”), click.option(“--use-orchestrator”, is\_flag = true, help = “Use orchestrator to run parallel tests”), click.option(“--dry-run”, is\_flag = true, default = false, help = “Dont actually run tests”), click.option(“--lightmode”, is\_flag = true, default = false, help = “Skips all before test setup”), pass\_context.

**Local steps**

- Bind dependencies activate\_by\_import.
- Bind dependencies CodeCoverage.
- Within CodeCoverage(with\_coverage, app) bound as cc.
  - Set site from get\_site(context).
  - If use\_orchestrator.
    - Bind dependencies ParallelTestWithOrchestrator.
    - Set runner from ParallelTestWithOrchestrator(app, site = site).
  - Otherwise.
    - Bind dependencies ParallelTestRunner.
    - Set runner from ParallelTestRunner(app, site = site, build\_number = build\_number, total\_builds = total\_builds, dry\_run = dry\_run, …).
  - Set mode from “Orchestrator” when use\_orchestrator, otherwise “Parallel”.
    - Value choice on use\_orchestrator — true gives “Orchestrator”, false gives “Parallel”.
  - Set banner from formatted text   ╔════════════════════════════════════════════╗  ║   Parallel Test Runner Execution Summary   ║  ╠════════════════════════════════════════════╣.
  - If cc.with\_coverage.
    - Update banner using + “\\n\\t\\t\\t║ Coverage Rep.:  {cc.outfile:&lt;26} ║”.
  - Update banner using + “\\n\\t\\t╚════════════════════════════════════════════╝\\n\\t\\t”.
  - Evaluate print(banner).
  - Evaluate runner.setup\_and\_run().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L132) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L645) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L719)

<a id="op-8605cfa0c45f7d"></a>
### Get site url

`operation_foundation_binding_foundation_commands_testing_get_site_url`

**Inputs** site.

**Declared result** str.

**Explicit results** (conf.host\_name or formatted command or address in the contract).

**Local steps**

- Set conf from Platform.get\_site\_config(site\_path = os.path.join(Platform.local.sites\_path, site)).
- Return (conf.host\_name or formatted command or address in the contract).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.host\_name → formatted command or address in the contract.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L113) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L595) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L571)

<a id="op-aa70baa17fd458"></a>
### Has config

`operation_foundation_binding_foundation_commands_testing_has_config`

**Inputs** app\_path, name.

**Declared result** bool.

**Explicit results** any(generator of os.path.exists(os.path.join(app\_path, formatted text {name}.config.{ext})) for ext drawn from tuple(“js”, “ts”, “mjs”, “cjs”, …)).

**Local steps**

- Return any(generator of os.path.exists(os.path.join(app\_path, formatted text {name}.config.{ext})) for ext drawn from tuple(“js”, “ts”, “mjs”, “cjs”, …)).
  - Draw ext from tuple(“js”, “ts”, “mjs”, “cjs”, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L114) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L596) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L572)
