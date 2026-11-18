# Site operations and diagnostics · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Installer

<a id="op-4a41653b1af8aa"></a>
### Update config file

`operation_foundation_installer_business_behavior_update_configuration_file`

**Inputs** key, value, config\_file.

**Local steps**

- Within open(config\_file) bound as f.
  - Set site\_config from json.loads(f.read()).
- If value belongs to tuple(“0”, “1”).
  - Set value from int(value).
- If value equals “false”.
  - Set value from false.
- If value equals “true”.
  - Set value from true.
- If value equals “None”.
  - If key belongs to site\_config.
    - Remove site\_config at key.
- Otherwise.
  - Set site\_config at key from value.
- Within open(config\_file, “w”) bound as f.
  - Evaluate f.write(json.dumps(site\_config, indent = 1, sort\_keys = true)).
- If hasattr(Platform.local, “conf”).
  - Set Platform.local.conf at key from value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L1454) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1812) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L550)

<a id="op-776989461e85ab"></a>
### Get site config path

`operation_foundation_installer_business_behavior_get_site_configuration_path`

**Inputs** no declared parameters.

**Explicit results** os.path.join(Platform.local.site\_path, “site\_config.json”).

**Local steps**

- Return os.path.join(Platform.local.site\_path, “site\_config.json”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L1935) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1784) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L524)

<a id="op-a553e0949868c0"></a>
### Get conf params

`operation_foundation_installer_business_behavior_get_configuration_parameters`

**Inputs** db\_name = no value, db\_password = no value.

**Explicit results** mapping(“db\_name” → db\_name, “db\_password” → db\_password).

**Explicit failure paths** Exception(“Database Name Required”).

**Local steps**

- If not db\_name.
  - Set db\_name from input(“Database Name: ”).
  - If not db\_name.
    - Raise Exception(“Database Name Required”).
- If not db\_password.
  - Bind dependencies random\_string.
  - Set db\_password from random\_string(16).
- Return mapping(“db\_name” → db\_name, “db\_password” → db\_password).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L1997) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1780) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L520)

<a id="op-3b25131e7426ec"></a>
### Clear site locks

`operation_foundation_installer_business_behavior_clear_site_locks`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies shutil.
- Bind dependencies Path.
- Set path from Path(Platform.get\_site\_path(“locks”)).
- Evaluate shutil.rmtree(path, ignore\_errors = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L2197) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1768) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L510)

<a id="op-fcba7ba2ce8b78"></a>
### Make site dirs

`operation_foundation_installer_business_behavior_make_site_dirs`

**Inputs** no declared parameters.

**Local steps**

- For each dir\_path in list(os.path.join(“public”, “files”), os.path.join(“private”, “backups”), os.path.join(“private”, “files”), “locks”, …).
  - Set path from Platform.get\_site\_path(dir\_path).
  - Evaluate os.makedirs(path, exist\_ok = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L2314) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1795) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L535)

<a id="op-17563fa8c549d4"></a>
### Add module defs

`operation_foundation_installer_business_behavior_add_module_defs`

**Inputs** app, ignore\_if\_duplicate = false.

**State and service calls** request new\_doc for “Module Def” · call insert on d.

**Local steps**

- Set modules from Platform.get\_module\_list(app).
- For each module in modules.
  - Evaluate rename\_conflicting\_custom\_module(module, app).
  - Set d from Platform.new\_doc(“Module Def”).
  - Set d.app\_name from app.
  - Set d.module\_name from module.
  - Evaluate d.insert(ignore\_permissions = true, ignore\_if\_duplicate = ignore\_if\_duplicate).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L2520) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1765) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L507)

<a id="op-ffc59484b65e18"></a>
### Sync module defs

`operation_foundation_installer_business_behavior_sync_module_defs`

**Inputs** no declared parameters.

**Declared result** list at str.

**Record and data access** read “Module Def” via get\_all.

**State and service calls** request set\_value on “Module Def” · request new\_doc for “Module Def” · call insert on doc.

**Explicit results** added.

**Local steps**

- Set existing from mapping of row.name → row for row drawn from Platform.get\_all(“Module Def”, fields = list(“name”, “app\_name”, “custom”)).
  - Draw row from Platform.get\_all(“Module Def”, fields = list(“name”, “app\_name”, “custom”)).
- Set tuple(added, repaired) from tuple(list(), list()).
- For each app in Platform.get\_installed\_apps().
  - For each module in Platform.get\_module\_list(app).
    - Set row from existing.get(module).
    - If (row and not row.custom).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row → not row.custom.
      - If not row.app\_name.
        - Evaluate Platform.db.set\_value(“Module Def”, module, “app\_name”, app, update\_modified = false).
        - Set row.app\_name from app.
        - Evaluate repaired.append(module).
      - Continue with the next iteration or loop test.
    - Evaluate rename\_conflicting\_custom\_module(module, app).
    - Set doc from Platform.new\_doc(“Module Def”).
    - Set doc.app\_name from app.
    - Set doc.module\_name from module.
    - Evaluate doc.insert(ignore\_permissions = true, ignore\_if\_duplicate = true).
    - Set existing at module from doc.
    - Evaluate added.append(module).
- If repaired.
  - Evaluate print(formatted text Placed modules that had no app: {comma\_and(repaired, add\_quotes = false)}).
- Return added.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L2739) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1811) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L549)

<a id="op-c3147f307aad8f"></a>
### Rename conflicting custom module

`operation_foundation_installer_business_behavior_rename_conflicting_custom_module`

**Inputs** module, app.

**Declared result** (str bitwise or no value).

**Record and data access** read “Module Def” via get\_value · read “Sidebar” via get\_value.

**State and service calls** msgprint with message.

**Explicit results** no value · new\_name.

**Local steps**

- If not Platform.db.get\_value(“Module Def”, module, “custom”).
  - Return no value.
- Bind dependencies rename\_doc.
- Set new\_name from available\_module\_name(module).
- Evaluate rename\_doc(doctype = “Module Def”, old = module, new = new\_name, force = true, …).
- If held bound to Platform.db.get\_value(“Sidebar”, mapping(“title” → module), “name”).
  - Evaluate rename\_doc(doctype = “Sidebar”, old = held, new = new\_name, force = true, …).
- Set message from translated “Module {0} is now shipped by {1}; this site's module of that name is now {2}.”.format(module, app, new\_name).
- Evaluate click.secho(formatted text \* {message}, fg = “yellow”).
- Evaluate Platform.msgprint(message, title = translated “Custom Module Renamed”, indicator = “orange”).
- Return new\_name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L3398) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1807) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L546)

<a id="op-b7e4968dd9a9a8"></a>
### Reclaim module name for its app

`operation_foundation_installer_business_behavior_reclaim_module_name_for_its_application`

**Inputs** module.

**Declared result** (str bitwise or no value).

**Explicit results** rename\_conflicting\_custom\_module(module, app) when app, otherwise no value.

**Local steps**

- Set app from Platform.local.module\_app.get(Platform.scrub(module)).
- Return rename\_conflicting\_custom\_module(module, app) when app, otherwise no value.
  - Value choice on app — true gives rename\_conflicting\_custom\_module(module, app), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L3936) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1802) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L541)

<a id="op-fd05badd90e19a"></a>
### Available module name

`operation_foundation_installer_business_behavior_available_module_name`

**Inputs** module.

**Declared result** str.

**Record and data access** read “Module Def” via exists.

**Explicit results** candidate.

**Local steps**

- Set candidate from formatted text {module} (Custom).
- Set suffix from 1.
- While Platform.db.exists(“Module Def”, candidate).
  - Update suffix using + 1.
  - Set candidate from formatted text {module} (Custom {suffix}).
- Return candidate.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L4073) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1767) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L509)

<a id="op-ad6c2a3c779c35"></a>
### Get app owned modules

`operation_foundation_installer_business_behavior_get_application_owned_modules`

**Inputs** app\_name.

**Declared result** list at str.

**Record and data access** read “Module Def” via get\_all.

**Explicit results** Platform.get\_all(“Module Def”, filters = mapping(“app\_name” → app\_name, “custom” → 0), pluck = “name”).

**Local steps**

- Return Platform.get\_all(“Module Def”, filters = mapping(“app\_name” → app\_name, “custom” → 0), pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L4255) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1778) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L518)

<a id="op-59f3c442690dc4"></a>
### Release custom module placements

`operation_foundation_installer_business_behavior_release_custom_module_placements`

**Inputs** app\_name, dry\_run = false.

**Declared result** list at str.

**Record and data access** read “Module Def” via get\_all.

**State and service calls** request set\_value on “Module Def”.

**Explicit results** modules.

**Local steps**

- Set modules from Platform.get\_all(“Module Def”, filters = mapping(“app\_name” → app\_name, “custom” → 1), pluck = “name”).
- For each module in modules.
  - Evaluate print(formatted text \* releasing custom Module Def '{module}' from '{app\_name}'...).
  - If not dry\_run.
    - Evaluate Platform.db.set\_value(“Module Def”, module, “app\_name”, no value).
- Return modules.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L4390) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1803) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L542)

<a id="op-2ed61f13ba2515"></a>
### Remove missing apps

`operation_foundation_installer_business_behavior_remove_missing_apps`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies importlib.
- Set apps from tuple(“Platform\_subscription”, “shopping\_cart”).
- Set installed\_apps from json.loads((Platform.db.get\_global(“installed\_apps”) or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_global(“installed\_apps”) → “&#91;&#93;”.
- For each app in apps.
  - If app belongs to installed\_apps.
    - Attempt the following.
      - Evaluate importlib.import\_module(app).
    - On failure (ImportError).
      - Evaluate installed\_apps.remove(app).
      - Evaluate Platform.db.set\_global(“installed\_apps”, json.dumps(installed\_apps)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L4686) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1806) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L545)

<a id="op-b9cf128a818224"></a>
### Convert archive content

`operation_foundation_installer_business_behavior_convert_archive_content`

**Inputs** sql\_file\_path.

**Explicit results** no value.

**Local steps**

- If Platform.conf.db\_type equals “mariadb”.
  - Bind dependencies Path.
  - Bind dependencies random\_string.
  - Set version from \_guess\_mariadb\_version().
  - If (not version or (version ≤ tuple(10, 6, 0) or version ≥ tuple(10, 6, 6))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not version → (version ≤ tuple(10, 6, 0) or version ≥ tuple(10, 6, 6)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in version ≤ tuple(10, 6, 0) → version ≥ tuple(10, 6, 6).
    - Return no value.
  - Evaluate click.secho(“MariaDB version being used does not support ROW\_FORMAT=COMPRESSED, converting into DYNAMIC format.”, fg = “yellow”).
  - Set old\_sql\_file\_path from Path(formatted text {sql\_file\_path}\_{random\_string(10)}).
  - Set sql\_file\_path from Path(sql\_file\_path).
  - Evaluate os.rename(sql\_file\_path, old\_sql\_file\_path).
  - Evaluate sql\_file\_path.touch().
  - Within open(old\_sql\_file\_path) bound as r, open(sql\_file\_path, “a”) bound as w.
    - For each line in r.
      - Evaluate w.write(line.replace(“ROW\_FORMAT=COMPRESSED”, “ROW\_FORMAT=DYNAMIC”)).
  - Evaluate old\_sql\_file\_path.unlink().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L4950) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1769) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L511)

<a id="op-0886457af4f7db"></a>
### Guess mariadb version

`operation_foundation_installer_business_behavior_guess_relational_database_version`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L5441) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1785) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L525)

<a id="op-6eb78e8b74f3ac"></a>
### Extract files

`operation_foundation_installer_business_behavior_extract_files`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** site\_name, file\_path.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** active or constructed exception.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L37) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1775) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L515)

<a id="op-863a8bbc39a731"></a>
### Is downgrade

`operation_foundation_installer_business_behavior_is_downgrade`

**Inputs** sql\_file\_path, verbose = false.

**Explicit results** false · is\_downgrade.

**Local steps**

- If Platform.conf.db\_type differs from “mariadb”.
  - Return false.
- Set backup\_version from (get\_backup\_version(sql\_file\_path) or get\_old\_backup\_version(sql\_file\_path)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_backup\_version(sql\_file\_path) → get\_old\_backup\_version(sql\_file\_path).
- Set current\_version from Version(Platform.\_\_version\_\_).
- If backup\_version is identical to no value.
  - Return false.
- Set is\_downgrade from backup\_version &gt; current\_version.
- If (verbose and is\_downgrade).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in verbose → is\_downgrade.
  - Evaluate print(formatted text Your site is currently on Platform {current\_version} and your backup is {backup\_version}.).
- Return is\_downgrade.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L6123) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1789) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L529)

<a id="op-ae747845f2df6a"></a>
### Get old backup version

`operation_foundation_installer_business_behavior_get_old_backup_version`

**Inputs** sql\_file\_path.

**Declared result** (Version bitwise or no value).

**Explicit results** Version(match at 1) · no value.

**Local steps**

- Set header from get\_db\_dump\_header(sql\_file\_path).split(whitespace '\\n').
- If match bound to re.search(“Platform (\\d+\\.\\d+\\.\\d+)”, header at 0).
  - Return Version(match at 1).
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L6417) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1783) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L523)

<a id="op-2e2b676156d28b"></a>
### Get backup version

`operation_foundation_installer_business_behavior_get_backup_version`

**Inputs** sql\_file\_path.

**Declared result** (Version bitwise or no value).

**Explicit results** Version(parser at “Platform” at “version”) · no value.

**Local steps**

- Set header from get\_db\_dump\_header(sql\_file\_path).split(whitespace '\\n').
- Set metadata from empty text.
- If “begin Platform metadata” belongs to header at 0.
  - For each line in header at slice 1 to no value.
    - If “end Platform metadata” belongs to line.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Update metadata using + (line.replace(“--”, empty text).strip() + whitespace '\\n').
  - Set parser from configparser.ConfigParser().
  - Evaluate parser.read\_string(metadata).
  - Return Version(parser at “Platform” at “version”).
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L6583) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1779) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L519)

<a id="op-d61f7546da20a8"></a>
### Is partial

`operation_foundation_installer_business_behavior_is_partial`

**Inputs** sql\_file\_path.

**Declared result** bool.

**Explicit results** false · “Partial Backup” belongs to header.

**Local steps**

- If Platform.conf.db\_type equals “sqlite”.
  - Return false.
- Set header from get\_db\_dump\_header(sql\_file\_path).
- Return “Partial Backup” belongs to header.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L6913) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1790) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L530)

<a id="op-c5a9c8e30fae66"></a>
### Partial restore

`operation_foundation_installer_business_behavior_partial_restore`

**Inputs** sql\_file\_path, verbose = false.

**Explicit results** no value.

**Local steps**

- If Platform.conf.db\_type equals “mariadb”.
  - Bind dependencies import\_db\_from\_sql.
- Otherwise.
  - If Platform.conf.db\_type equals “postgres”.
    - Bind dependencies warnings.
    - Bind dependencies import\_db\_from\_sql.
    - Set warn from click.style(“Delete the tables you want to restore manually before attempting partial restore operation for PostgreSQL databases”, fg = “yellow”).
    - Evaluate warnings.warn(warn, stacklevel = 2).
  - Otherwise.
    - Evaluate click.secho(“Unsupported database type”, fg = “red”).
    - Return no value.
- Evaluate import\_db\_from\_sql(source\_sql = sql\_file\_path, verbose = verbose).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L7034) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1799) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L539)

<a id="op-025bce1a56608c"></a>
### Validate database sql

`operation_foundation_installer_business_behavior_validate_database_database_query`

**Inputs** path, \_raise = true.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.ExecutableNotFound — formatted text ′{executable\_name}′ not found in PATH! This is required to take a backup. · Platform.InvalidDatabaseFile.

**Local steps**

- If path.endswith(“.gz”).
  - Set executable\_name from “zgrep”.
- Otherwise.
  - Set executable\_name from “grep”.
- If os.path.getsize(path).
  - If executable bound to which(executable\_name) is identical to no value.
    - Call the validation error handler Platform.throw(formatted text ′{executable\_name}′ not found in PATH! This is required to take a backup., exc = Platform.ExecutableNotFound).
  - Attempt the following.
    - Evaluate Platform.utils.execute\_in\_shell(formatted text {executable} -m1 \_\_Auth {path}, check\_exit\_code = true).
    - Return no value.
  - On failure (Exception).
    - Set error\_message from “Table ′\_\_Auth′ not found in file.”.
- Otherwise.
  - Set error\_message from formatted text {path} is an empty file!.
- If error\_message.
  - Evaluate click.secho(error\_message, fg = “red”).
- If \_raise.
  - Raise Platform.InvalidDatabaseFile.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L7312) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1814) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L552)

<a id="op-6b436b9f1b1aad"></a>
### Get db dump header

`operation_foundation_installer_business_behavior_get_database_dump_header`

**Inputs** file\_path, file\_bytes = 256.

**Declared result** str.

**Explicit results** f.read(file\_bytes).decode().

**Local steps**

- If file\_path.endswith(“.gz”).
  - Within gzip.open(file\_path, “rb”) bound as f.
    - Return f.read(file\_bytes).decode().
- Within open(file\_path, “rb”) bound as f.
  - Return f.read(file\_bytes).decode().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L7753) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1781) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L521)

## Service · Loader

<a id="op-fe92ff8c090474"></a>
### Platform Test Loader.recursive load suites in pymodule

`operation_foundation_testing_loader_business_behavior_foundation_test_loader_recursive_load_suites_in_pymodule`

**Inputs** self, suite.

**Local steps**

- Set suites\_queue from deque(list(suite)).
- While suites\_queue.
  - Set suite from suites\_queue.popleft().
  - For each elem in suite.
    - If elem.countTestCases().
      - If isinstance(elem, unittest.TestSuite).
        - Evaluate suites\_queue.append(elem).
      - Otherwise.
        - If isinstance(elem, unittest.TestCase).
          - If self.params.tests.
            - If elem.\_testMethodName belongs to self.params.tests.
              - Evaluate self.testsuite.addTest(elem).
          - Otherwise.
            - Evaluate self.testsuite.addTest(elem).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L47) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1938) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L612)
