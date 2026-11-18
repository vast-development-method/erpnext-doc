# Site operations and diagnostics · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Site

<a id="op-c827de99edb7b7"></a>
### Add db index

`operation_foundation_commands_site_business_behavior_add_database_index`

**Inputs** context, doctype, column.

**Wrappers, in declaration order** click.command(“add-database-index”), click.option(“--doctype”, help = “DocType on which index needs to be added”), click.option(“--column”, multiple = true, help = “Column to index. Multiple columns will create multi-column index in given order. To create a multiple, singl …”), pass\_context.

**State and service calls** request add\_index on doctype · commit.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Set columns from column.
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Attempt the following.
    - Evaluate Platform.db.add\_index(doctype, columns).
    - Evaluate Platform.db.commit().
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0022.json#L6851) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L516) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L598)

<a id="op-32f86a2c286ac8"></a>
### Describe database table

`operation_foundation_commands_site_business_behavior_describe_database_table`

**Inputs** context, doctype, column.

**Wrappers, in declaration order** click.command(“describe-database-table”), click.option(“--doctype”, help = “DocType to describe”), click.option(“--column”, multiple = true, help = “Explicitly fetch accurate cardinality from table data. This can be quite slow on large tables.”), pass\_context.

**Explicit failure paths** click.UsageError(“--doctype &lt;doctype&gt; is required”) · SiteNotSpecifiedError.

**Local steps**

- If doctype is identical to no value.
  - Raise click.UsageError(“--doctype &lt;doctype&gt; is required”).
- Bind dependencies json.
- Bind dependencies \_fetch\_table\_stats.
- For each site in context.sites.
  - Evaluate Platform.init(site = site).
  - Evaluate Platform.connect().
  - Attempt the following.
    - Set data from \_fetch\_table\_stats(doctype, column).
    - Evaluate print(json.dumps(data, indent = 2)).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0022.json#L7185) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L526) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L608)

<a id="op-104f65e06994c0"></a>
### Add system manager

`operation_foundation_commands_site_business_behavior_add_system_manager`

**Inputs** context, email, first\_name, last\_name, send\_welcome\_email, password.

**Wrappers, in declaration order** click.command(“add-system-manager”), click.argument(“email”), click.option(“--first-name”), click.option(“--last-name”), click.option(“--password”), click.option(“--send-welcome-email”, default = false, is\_flag = true), pass\_context.

**State and service calls** commit.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies Platform.utils.user.
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Attempt the following.
    - Evaluate Platform.utils.user.add\_system\_manager(email, first\_name, last\_name, send\_welcome\_email, …).
    - Evaluate Platform.db.commit().
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0022.json#L7597) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L518) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L600)

<a id="op-85c747749a8291"></a>
### Add user for sites

`operation_foundation_commands_site_business_behavior_add_user_for_sites`

**Inputs** context, email, first\_name, last\_name, user\_type, send\_welcome\_email, password, add\_role.

**Wrappers, in declaration order** click.command(“add-user”), click.argument(“email”), click.option(“--first-name”), click.option(“--last-name”), click.option(“--password”), click.option(“--user-type”), click.option(“--add-role”, multiple = true), click.option(“--send-welcome-email”, default = false, is\_flag = true), pass\_context.

**State and service calls** commit.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies Platform.utils.user.
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Attempt the following.
    - Evaluate add\_new\_user(email, first\_name, last\_name, user\_type, …).
    - Evaluate Platform.db.commit().
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L520) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L602)

<a id="op-2b7a15430861f8"></a>
### Disable user

`operation_foundation_commands_site_business_behavior_disable_user`

**Inputs** context, email.

**Wrappers, in declaration order** click.command(“disable-user”), click.argument(“email”), pass\_context.

**Record and data access** resolve a document from “User” via get\_doc.

**State and service calls** call save on user · commit.

**Local steps**

- Set site from get\_site(context).
- Within Platform.init\_site(site).
  - Evaluate Platform.connect().
  - Set user from Platform.get\_doc(“User”, email).
  - Set user.enabled from 0.
  - Evaluate user.save(ignore\_permissions = true).
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L481) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L528) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L609)

<a id="op-959094eaf9541e"></a>
### Migrate

`operation_foundation_commands_site_business_behavior_migrate`

**Inputs** context, skip\_failing = false, skip\_search\_index = false, skip\_fixtures = false.

**Wrappers, in declaration order** click.command(“migrate”), click.option(“--skip-failing”, is\_flag = true, help = “Skip patches that fail to run”), click.option(“--skip-search-index”, is\_flag = true, help = “Skip search indexing for web documents”), click.option(“--skip-fixtures”, is\_flag = true, help = “Skip loading fixtures”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies SiteMigration.
- For each site in context.sites.
  - Evaluate click.secho(formatted text Migrating {site}, fg = “green”).
  - Attempt the following.
    - Evaluate SiteMigration(skip\_failing = skip\_failing, skip\_search\_index = skip\_search\_index, skip\_fixtures = skip\_fixtures).run(site = site).
  - On exit, including pending return or failure.
    - Evaluate print().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L760) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L539) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L618)

<a id="op-0d648bb7cfc3a5"></a>
### Migrate to

`operation_foundation_commands_site_business_behavior_migrate_to`

**Inputs** no declared parameters.

**Wrappers, in declaration order** click.command(“migrate-to”).

**Local steps**

- Bind dependencies migrate\_to.
- Evaluate migrate\_to().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L1164) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L540) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L619)

<a id="op-d825cc05b7c4c1"></a>
### Run patch

`operation_foundation_commands_site_business_behavior_run_patch`

**Inputs** context, module, force.

**Wrappers, in declaration order** click.command(“run-patch”), click.argument(“module”), click.option(“--force”, is\_flag = true), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies Platform.modules.patch\_handler.
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - Attempt the following.
    - Evaluate Platform.connect().
    - Evaluate Platform.modules.patch\_handler.run\_single(module, force = (force or context.force)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in force → context.force.
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L1232) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L554) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L632)

<a id="op-940b386e26436d"></a>
### Reload doc

`operation_foundation_commands_site_business_behavior_reload_record`

**Inputs** context, module, doctype, docname.

**Wrappers, in declaration order** click.command(“reload-doc”), click.argument(“module”), click.argument(“doctype”), click.argument(“docname”), pass\_context.

**State and service calls** commit.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate Platform.reload\_doc(module, doctype, docname, force = context.force).
    - Evaluate Platform.db.commit().
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L1545) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L547) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L626)

<a id="op-f789d2a60dacb9"></a>
### Reload doctype

`operation_foundation_commands_site_business_behavior_reload_record_type`

**Inputs** context, doctype.

**Wrappers, in declaration order** click.command(“reload-doctype”), click.argument(“doctype”), pass\_context.

**State and service calls** commit.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate Platform.reload\_doctype(doctype, force = context.force).
    - Evaluate Platform.db.commit().
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L1895) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L548) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L627)

<a id="op-7bf2f558bc6711"></a>
### Add to hosts

`operation_foundation_commands_site_business_behavior_add_to_hosts`

**Inputs** context.

**Wrappers, in declaration order** click.command(“add-to-hosts”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- For each site in context.sites.
  - Evaluate Platform.commands.popen(formatted command or address in the contract).
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L2175) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L519) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L601)

<a id="op-43aa87d1263af9"></a>
### Use

`operation_foundation_commands_site_business_behavior_use`

**Inputs** site, sites\_path = “.”.

**Wrappers, in declaration order** click.command(“use”), click.argument(“site”).

**Local steps**

- Evaluate use(site, sites\_path = sites\_path).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L2350) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L566) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L644)

<a id="op-a5aa202936d21e"></a>
### Use

`operation_foundation_commands_site_business_behavior_use_2`

**Inputs** site, sites\_path = “.”.

**Local steps**

- Bind dependencies update\_site\_config.
- If os.path.exists(os.path.join(sites\_path, site)).
  - Set sites\_path from os.getcwd().
  - Set conifg from os.path.join(sites\_path, “common\_site\_config.json”).
  - Evaluate update\_site\_config(“default\_site”, site, validate = false, site\_config\_path = conifg).
  - Evaluate print(formatted text Current Site set to {site}).
- Otherwise.
  - Evaluate print(formatted text Site {site} does not exist).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L2466) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L567) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L645)

<a id="op-512c149f656f74"></a>
### Backup

`operation_foundation_commands_site_business_behavior_backup`

**Inputs** context, with\_files = false, backup\_path = no value, backup\_path\_db = no value, backup\_path\_files = no value, backup\_path\_private\_files = no value, backup\_path\_conf = no value, ignore\_backup\_conf = false, verbose = false, compress = false, include = empty text, exclude = empty text, old\_backup\_metadata = false.

**Wrappers, in declaration order** click.command(“backup”), click.option(“--with-files”, default = false, is\_flag = true, help = “Take backup with files”), click.option(“--include”, “--only”, “-i”, default = empty text, type = str, help = “Specify the DocTypes to backup seperated by commas”), click.option(“--exclude”, “-e”, default = empty text, type = str, help = “Specify the DocTypes to not backup seperated by commas”), click.option(“--backup-path”, default = no value, help = “Set path for saving all the files in this operation”), click.option(“--backup-path-db”, default = no value, help = “Set path for saving database file”), click.option(“--backup-path-files”, default = no value, help = “Set path for saving public file”), click.option(“--backup-path-private-files”, default = no value, help = “Set path for saving private file”), click.option(“--backup-path-conf”, default = no value, help = “Set path for saving config file”), click.option(“--ignore-backup-conf”, default = false, is\_flag = true, help = “Ignore excludes/includes set in config”), click.option(“--verbose”, default = false, is\_flag = true, help = “Add verbosity”), click.option(“--compress”, default = false, is\_flag = true, help = “Compress private and public files”), click.option(“--old-backup-metadata”, default = false, is\_flag = true, help = “Use older backup metadata”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies scheduled\_backup.
- Set verbose from (verbose or context.verbose).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in verbose → context.verbose.
- Set exit\_code from 0.
- Set rollback\_callback from no value.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Set rollback\_callback from CallbackManager().
    - Set odb from scheduled\_backup(ignore\_files = not with\_files, backup\_path = backup\_path, backup\_path\_db = backup\_path\_db, backup\_path\_files = backup\_path\_files, …).
  - On failure (Exception).
    - Evaluate click.secho(formatted text Backup failed for Site {site}. Database or site\_config.json may be corrupted, fg = “red”).
    - If rollback\_callback.
      - Evaluate rollback\_callback.run().
      - Set rollback\_callback from no value.
    - If verbose.
      - Evaluate print(Platform.get\_traceback(with\_context = true)).
    - Set exit\_code from 1.
    - Continue with the next iteration or loop test.
  - If (Platform.get\_system\_settings(“encrypt\_backup”) and Platform.get\_site\_config().encryption\_key).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_system\_settings(“encrypt\_backup”) → Platform.get\_site\_config().encryption\_key.
    - Evaluate click.secho(“Backup encryption is turned on. Please note the backup encryption key.”, fg = “yellow”).
  - Evaluate odb.print\_summary().
  - Evaluate click.secho(“Backup for Site {} has been successfully completed{}”.format(site, “ with files” when with\_files, otherwise empty text), fg = “green”).
    - Value choice on with\_files — true gives “ with files”, false gives empty text.
  - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.
- Evaluate sys.exit(exit\_code).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“encrypt\_backup”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L121) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L521) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L603)

<a id="op-510c31824a8e55"></a>
### Remove from installed apps

`operation_foundation_commands_site_business_behavior_remove_from_installed_apps`

**Inputs** context, app.

**Wrappers, in declaration order** click.command(“remove-from-installed-apps”), click.argument(“app”), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Evaluate ensure\_app\_not\_Platform(app).
- Bind dependencies remove\_from\_installed\_apps.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate remove\_from\_installed\_apps(app).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L4475) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L549) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L628)

<a id="op-1d88d56a731a91"></a>
### Uninstall

`operation_foundation_commands_site_business_behavior_uninstall`

**Inputs** context, app, dry\_run, yes, no\_backup, force.

**Wrappers, in declaration order** click.command(“uninstall-app”), click.argument(“app”), click.option(“--yes”, “-y”, help = “To bypass confirmation prompt for uninstalling the app”, is\_flag = true, default = false), click.option(“--dry-run”, help = “List all doctypes that will be deleted”, is\_flag = true, default = false), click.option(“--no-backup”, help = “Do not backup the site”, is\_flag = true, default = false), click.option(“--force”, help = “Force remove app from site”, is\_flag = true, default = false), pass\_context.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Evaluate ensure\_app\_not\_Platform(app).
- Bind dependencies remove\_app.
- Bind dependencies filelock.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Within filelock(“uninstall\_app”).
      - Evaluate remove\_app(app\_name = app, dry\_run = dry\_run, yes = yes, no\_backup = no\_backup, …).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L5258) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L565) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L643)

<a id="op-a22a5923be4d38"></a>
### Drop site

`operation_foundation_commands_site_business_behavior_drop_site`

**Inputs** site, db\_root\_username = “root”, db\_root\_password = no value, archived\_sites\_path = no value, force = false, no\_backup = false.

**Wrappers, in declaration order** click.command(“drop-site”), click.argument(“site”), click.option(“--db-root-username”, “--mariadb-root-username”, “--root-login”, help = “Root username for MariaDB or PostgreSQL, Default is "root"”), click.option(“--db-root-password”, “--mariadb-root-password”, “--root-password”, help = “Root password for MariaDB or PostgreSQL”), click.option(“--archived-sites-path”), click.option(“--no-backup”, is\_flag = true, default = false), click.option(“--force”, help = “Force drop-site even if an error is encountered”, is\_flag = true, default = false).

**Local steps**

- Evaluate \_drop\_site(site, db\_root\_username, db\_root\_password, archived\_sites\_path, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L123) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L529) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L610)

<a id="op-04f09139d6bfe3"></a>
### Drop site

`operation_foundation_commands_site_business_behavior_drop_site_2`

**Inputs** site, db\_root\_username = no value, db\_root\_password = no value, archived\_sites\_path = no value, force = false, no\_backup = false.

**Local steps**

- Bind dependencies drop\_user\_and\_database.
- Bind dependencies scheduled\_backup.
- Evaluate Platform.init(site).
- Evaluate Platform.connect().
- Attempt the following.
  - If not no\_backup.
    - Evaluate click.secho(formatted text Taking backup of {site}, fg = “green”).
    - Set odb from scheduled\_backup(ignore\_files = false, ignore\_conf = true, force = true, verbose = true).
    - Evaluate odb.print\_summary().
- On failure (Exception) bound to err.
  - If force.
    - Take no action here.
  - Otherwise.
    - Set messages from list((“=” × 80), formatted text Error: The operation has stopped because backup of {site}'s database failed., formatted text Reason: {err} , “Fix the issue and try again.”, …).
    - Evaluate click.echo(whitespace '\\n'.join(messages)).
    - Evaluate sys.exit(1).
- Evaluate click.secho(“Dropping site database and user”, fg = “green”).
- Set Platform.flags.root\_login from db\_root\_username.
- Set Platform.flags.root\_password from db\_root\_password.
- Evaluate drop\_user\_and\_database(Platform.conf.db\_name, Platform.conf.db\_user).
- Set archived\_sites\_path from (archived\_sites\_path or os.path.join(Platform.utils.get\_bench\_path(), “archived”, “sites”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in archived\_sites\_path → os.path.join(Platform.utils.get\_bench\_path(), “archived”, “sites”).
- Set archived\_sites\_path from os.path.realpath(archived\_sites\_path).
- Evaluate click.secho(formatted text Moving site to archive under {archived\_sites\_path}, fg = “green”).
- Evaluate os.makedirs(archived\_sites\_path, exist\_ok = true).
- Evaluate move(archived\_sites\_path, site).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L6227) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L530) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L611)

<a id="op-c4978bbf2903ad"></a>
### Move

`operation_foundation_commands_site_business_behavior_move`

**Inputs** dest\_dir, site.

**Explicit results** final\_new\_path.

**Explicit failure paths** Exception(“destination is not a directory or does not exist”).

**Local steps**

- If not os.path.isdir(dest\_dir).
  - Raise Exception(“destination is not a directory or does not exist”).
- Evaluate Platform.init(site).
- Set old\_path from Platform.utils.get\_site\_path().
- Set new\_path from os.path.join(dest\_dir, site).
- Set site\_dump\_exists from true.
- Set count from 0.
- While site\_dump\_exists.
  - Set final\_new\_path from (new\_path + str((count or empty text))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in count → empty text.
  - Set site\_dump\_exists from os.path.exists(final\_new\_path).
  - Update count using + 1.
- Evaluate shutil.move(old\_path, final\_new\_path).
- Evaluate Platform.destroy().
- Return final\_new\_path.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L7043) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L541) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L620)

<a id="op-db98c8d00cbc31"></a>
### Set password

`operation_foundation_commands_site_business_behavior_set_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** context, user, password, logout\_all\_sessions.

**Locally raised failures** SiteNotSpecifiedError.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L7410) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L557) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L635)

<a id="op-3d0c16f306ee4e"></a>
### Set admin password

`operation_foundation_commands_site_business_behavior_set_admin_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** context, admin\_password, logout\_all\_sessions.

**Locally raised failures** SiteNotSpecifiedError.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0023.json#L7689) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L555) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L633)

<a id="op-05109451f9835e"></a>
### Set user password

`operation_foundation_commands_site_business_behavior_set_user_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** site, user, password, logout\_all\_sessions.

**Observed service boundaries** record lookup, record mutation request, transaction control.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L130) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L558) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L636)

<a id="op-1603fac76d2f4b"></a>
### Set last active for user

`operation_foundation_commands_site_business_behavior_set_last_active_for_user`

**Inputs** context, user = no value.

**Wrappers, in declaration order** click.command(“set-last-active-for-user”), click.option(“--user”, help = “Setup last active date for user”), pass\_context.

**State and service calls** request set\_value on “User” · commit.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_system\_users.
- Bind dependencies now\_datetime.
- Set site from get\_site(context).
- Within Platform.init\_site(site).
  - Evaluate Platform.connect().
  - If not user.
    - Set user from get\_system\_users(limit = 1).
    - If len(user) &gt; 0.
      - Set user from user at 0.
    - Otherwise.
      - Return no value.
  - Evaluate Platform.db.set\_value(“User”, user, “last\_active”, now\_datetime()).
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0024.json#L391) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L556) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L634)

<a id="op-e1f6b39891dcc6"></a>
### Publish realtime

`operation_foundation_commands_site_business_behavior_publish_realtime`

**Inputs** context, event, message, room, user, doctype, docname, after\_commit.

**Wrappers, in declaration order** click.command(“publish-realtime”), click.argument(“event”), click.option(“--message”), click.option(“--room”), click.option(“--user”), click.option(“--doctype”), click.option(“--docname”), click.option(“--after-commit”), pass\_context.

**State and service calls** commit.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies publish\_realtime.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate publish\_realtime(event, message = message, room = room, user = user, doctype = doctype, …).
    - Evaluate Platform.db.commit().
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from publish\_realtime(event, message = message, room = room, user = user, doctype = doctype, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0024.json#L776) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L544) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L623)
