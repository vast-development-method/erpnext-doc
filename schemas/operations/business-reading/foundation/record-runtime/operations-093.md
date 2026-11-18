# Record lifecycle and persistence · operations 93

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Server script

[Record definition](../../../../data/record-types/server_script.json)

<a id="op-b1f1e1b056cdeb"></a>
### Enabled

`operation_foundation_core_record_definitions_server_script_business_behavior_enabled`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (bool bitwise or no value).

**Explicit results** is\_safe\_exec\_enabled().

**Local steps**

- If Platform.has\_permission(“Server Script”).
  - Return is\_safe\_exec\_enabled().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Server Script”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L3861) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L376) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L540)

<a id="op-475d7a5b07881d"></a>
### Run server script for doc event

`operation_foundation_core_record_definitions_server_script_server_script_utils_business_behavior_run_server_script_for_record_event`

**Inputs** doc, event.

**Record and data access** resolve a document from “Server Script” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- If event does not belong to EVENT\_MAP.
  - Return no value.
- If Platform.flags.in\_install.
  - Return no value.
- If Platform.flags.in\_migrate.
  - Return no value.
- Set scripts from get\_server\_script\_map().get(doc.doctype, mapping()).get(EVENT\_MAP at event, no value).
- If scripts.
  - For each script\_name in scripts.
    - Evaluate Platform.get\_cached\_doc(“Server Script”, script\_name).execute\_doc(doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Server Script”, script\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L3961) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L394) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L558)

<a id="op-f7c07242ee98c6"></a>
### Get server script map

`operation_foundation_core_record_definitions_server_script_server_script_utils_business_behavior_get_server_script_map`

**Inputs** no declared parameters.

**Record and data access** read “Server Script” via get\_all.

**Explicit results** mapping() · script\_map.

**Local steps**

- If (Platform.flags.in\_patch and not Platform.db.table\_exists(“Server Script”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.in\_patch → not Platform.db.table\_exists(“Server Script”).
  - Return mapping().
- Set script\_map from Platform.client\_cache.get\_value(“server\_script\_map”).
- If script\_map is identical to no value.
  - Set script\_map from mapping(“permission\_query” → mapping()).
  - Set enabled\_server\_scripts from Platform.get\_all(“Server Script”, fields = tuple(“name”, “reference\_doctype”, “doctype\_event”, “api\_method”, …), filters = mapping(“disabled” → 0)).
  - For each script in enabled\_server\_scripts.
    - If script.script\_type equals “DocType Event”.
      - Evaluate script\_map.setdefault(script.reference\_doctype, mapping()).setdefault(script.doctype\_event, list()).append(script.name).
    - Otherwise.
      - If script.script\_type equals “Permission Query”.
        - Set script\_map at “permission\_query” at script.reference\_doctype from script.name.
      - Otherwise.
        - Set script\_map.setdefault(“\_api”, mapping()) at script.api\_method from script.name.
  - Evaluate Platform.client\_cache.set\_value(“server\_script\_map”, script\_map).
- Return script\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L4220) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L393) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L557)

## Record · Session default settings

[Record definition](../../../../data/record-types/session_default_settings.json)

<a id="op-3318d1d753a312"></a>
### Get session default values

`operation_foundation_core_record_definitions_session_default_settings_business_behavior_get_session_default_values`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0106.json#L3248) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L412) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L576)

<a id="op-b52eee06ee0ee4"></a>
### Set session default values

`operation_foundation_core_record_definitions_session_default_settings_business_behavior_set_session_default_values`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** default\_values.

**Explicit result forms** a scalar literal, no value.

**Local structure** 0 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0106.json#L3591) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L413) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L577)

<a id="op-099ff1a3179d45"></a>
### Clear session defaults

`operation_foundation_core_record_definitions_session_default_settings_business_behavior_clear_session_defaults`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0106.json#L3802) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L411) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L575)

## Service · Setup db

<a id="op-6e9d652b897e94"></a>
### Get mariadb variables

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_get_relational_database_variables`

**Inputs** no declared parameters.

**State and service calls** execute a supplied database query.

**Explicit results** Platform.\_dict(Platform.db.sql(“show variables”)).

**Local steps**

- Return Platform.\_dict(Platform.db.sql(“show variables”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1313) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1424)

<a id="op-bff82f15502352"></a>
### Get mariadb version

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_get_relational_database_version`

**Inputs** version\_string = empty text.

**Explicit results** version.rsplit(“.”, 1).

**Local steps**

- Set version\_string from (version\_string or get\_mariadb\_variables().get(“version”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in version\_string → get\_mariadb\_variables().get(“version”).
- Set version from version\_string.split(“-”, 1) at 0.
- Return version.rsplit(“.”, 1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L72) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1314) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1425)

<a id="op-93f303d84516da"></a>
### Setup database

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_setup_database`

**Inputs** force, verbose, mariadb\_user\_host\_login\_scope = no value.

**Local steps**

- Set Platform.local.session from Platform.\_dict(mapping(“user” → “Administrator”)).
- Set db\_user from Platform.conf.db\_user.
- Set db\_name from Platform.local.conf.db\_name.
- Set root\_conn from get\_root\_connection().
- Set dbman from DbManager(root\_conn).
- Set dbman\_kwargs from mapping().
- If mariadb\_user\_host\_login\_scope is distinct from no value.
  - Set dbman\_kwargs at “host” from mariadb\_user\_host\_login\_scope.
- Evaluate dbman.create\_user(db\_user, Platform.conf.db\_password, expanded names dbman\_kwargs).
- If verbose.
  - Evaluate print(formatted text Created or updated user {db\_user}).
- If (force or db\_name does not belong to dbman.get\_database\_list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in force → db\_name does not belong to dbman.get\_database\_list().
  - Evaluate dbman.drop\_database(db\_name).
- Otherwise.
  - Evaluate print(formatted text Database {db\_name} already exists, please drop it manually or pass ′--force′.).
  - Evaluate sys.exit(1).
- Evaluate dbman.create\_database(db\_name).
- If verbose.
  - Evaluate print(“Created database {}”.format(db\_name)).
- Evaluate dbman.grant\_all\_privileges(db\_name, db\_user, expanded names dbman\_kwargs).
- Evaluate dbman.flush\_privileges().
- If verbose.
  - Evaluate print(formatted text Granted privileges to user {db\_user} and database {db\_name}).
- Evaluate root\_conn.close().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L233) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1317) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1428)

<a id="op-e69ebf718488b7"></a>
### Drop user and database

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_drop_user_and_database`

**Inputs** db\_name, db\_user.

**Local steps**

- Set Platform.local.db from get\_root\_connection().
- Set dbman from DbManager(Platform.local.db).
- Evaluate dbman.drop\_database(db\_name).
- Evaluate dbman.delete\_user(db\_user, host = “%”).
- Evaluate dbman.delete\_user(db\_user).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L898) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1312) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1423)

<a id="op-79f668e4e83bc2"></a>
### Bootstrap database

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_bootstrap_database`

**Inputs** verbose, source\_sql = no value.

**Local steps**

- Bind dependencies sys.
- Evaluate Platform.connect().
- Evaluate check\_compatible\_versions().
- Evaluate import\_db\_from\_sql(source\_sql, verbose).
- Evaluate Platform.connect().
- If “tabDefaultValue” does not belong to Platform.db.get\_tables(cached = false).
  - Bind dependencies secho.
  - Evaluate secho(multiline text in the contract, fg = “red”).
  - Evaluate sys.exit(1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L1078) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1310) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1421)

<a id="op-6a053e930c689a"></a>
### Import db from sql

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_import_database_from_database_query`

**Inputs** source\_sql = no value, verbose = false.

**Local steps**

- If verbose.
  - Evaluate print(“Starting database import...”).
- Set db\_name from Platform.conf.db\_name.
- If not source\_sql.
  - Set source\_sql from os.path.join(os.path.dirname(\_\_file\_\_), “framework\_mariadb.sql”).
- Evaluate DbManager(Platform.local.db).restore\_database(verbose, db\_name, source\_sql, Platform.conf.db\_user, …).
- If verbose.
  - Evaluate print(“Imported from database {}”.format(source\_sql)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L1319) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1316) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1427)

<a id="op-471968527ebcce"></a>
### Check compatible versions

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_check_compatible_versions`

**Inputs** no declared parameters.

**Local steps**

- Attempt the following.
  - Set version from get\_mariadb\_version().
  - Set version\_tuple from tuple(generator of int(v) for v drawn from version at 0.split(“.”)).
    - Draw v from version at 0.split(“.”).
  - If version\_tuple &lt; tuple(10, 6).
    - Evaluate click.secho(formatted text Warning: MariaDB version {version} is older than 10.6 which is not supported by Platform, fg = “yellow”).
  - Otherwise.
    - If version\_tuple &gt; tuple(11, 8).
      - Evaluate click.secho(formatted text Warning: MariaDB version {version} is newer than 11.8 which is not yet tested with Platform Framework., fg = “yellow”).
- On failure (Exception).
  - Evaluate click.secho(“MariaDB version compatibility checks failed, make sure you're running a supported version.”, fg = “yellow”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L1604) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1311) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1422)

<a id="op-2ec03a7791c7fb"></a>
### Get root connection

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_get_root_connection`

**Inputs** no declared parameters.

**Explicit results** Platform.local.flags.root\_connection.

**Local steps**

- If not Platform.local.flags.root\_connection.
  - Bind dependencies getpass.
  - If not Platform.flags.root\_login.
    - Set Platform.flags.root\_login from (Platform.conf.get(“mariadb\_root\_login”) or Platform.conf.get(“root\_login”) or (sys.\_\_stdin\_\_.isatty() and input(“Enter mysql super user &#91;root&#93;: ”)) or “root”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“mariadb\_root\_login”) → Platform.conf.get(“root\_login”) → (sys.\_\_stdin\_\_.isatty() and input(“Enter mysql super user &#91;root&#93;: ”)) → “root”.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sys.\_\_stdin\_\_.isatty() → input(“Enter mysql super user &#91;root&#93;: ”).
  - If not Platform.flags.root\_password.
    - Set Platform.flags.root\_password from (Platform.conf.get(“mariadb\_root\_password”) or Platform.conf.get(“root\_password”) or getpass(“MySQL root password: ”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“mariadb\_root\_password”) → Platform.conf.get(“root\_password”) → getpass(“MySQL root password: ”).
  - Set Platform.local.flags.root\_connection from Platform.database.get\_db(socket = Platform.conf.db\_socket, host = Platform.conf.db\_host, port = Platform.conf.db\_port, user = Platform.flags.root\_login, …).
- Return Platform.local.flags.root\_connection.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L1948) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1315) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1426)

<a id="op-bb97aa6f700df5"></a>
### Setup database

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_2_setup_database`

**Inputs** no declared parameters.

**Local steps**

- Set root\_conn from get\_root\_connection().
- Evaluate root\_conn.commit().
- Evaluate root\_conn.sql(“end”).
- Evaluate root\_conn.sql(formatted text DROP DATABASE IF EXISTS "{Platform.conf.db\_name}").
- If root\_conn.sql(formatted text SELECT 1 FROM pg\_roles WHERE rolname='{Platform.conf.db\_user}').
  - Evaluate root\_conn.sql(formatted text ALTER USER "{Platform.conf.db\_user}" WITH PASSWORD '{Platform.conf.db\_password}').
- Otherwise.
  - Evaluate root\_conn.sql(formatted text CREATE USER "{Platform.conf.db\_user}" WITH PASSWORD '{Platform.conf.db\_password}').
- Evaluate root\_conn.sql(formatted text CREATE DATABASE "{Platform.conf.db\_name}").
- Evaluate root\_conn.sql(formatted text GRANT ALL PRIVILEGES ON DATABASE "{Platform.conf.db\_name}" TO "{Platform.conf.db\_user}").
- If psql\_version bound to root\_conn.sql(“SHOW server\_version\_num”, as\_dict = true).
  - Set semver\_version\_num from (psql\_version at 0.get(“server\_version\_num”) or “140000”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in psql\_version at 0.get(“server\_version\_num”) → “140000”.
  - If cint(semver\_version\_num) &gt; 150000.
    - Evaluate root\_conn.sql(formatted text ALTER DATABASE "{Platform.conf.db\_name}" OWNER TO "{Platform.conf.db\_user}").
- Evaluate root\_conn.close().
- Set db\_conn from Platform.database.get\_db(socket = Platform.conf.db\_socket, host = Platform.conf.db\_host, port = Platform.conf.db\_port, user = Platform.flags.root\_login, …).
- Attempt the following.
  - Evaluate db\_conn.commit().
  - Evaluate db\_conn.sql(“end”).
  - Evaluate db\_conn.sql(formatted text GRANT ALL ON SCHEMA {db\_conn.db\_schema} TO "{Platform.conf.db\_user}").
- On exit, including pending return or failure.
  - Evaluate db\_conn.close().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L5) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1309) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1420)

<a id="op-bd360cb5f0ebca"></a>
### Bootstrap database

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_2_bootstrap_database`

**Inputs** verbose, source\_sql = no value.

**Local steps**

- Evaluate Platform.connect().
- Evaluate import\_db\_from\_sql(source\_sql, verbose).
- Evaluate Platform.connect().
- If “tabDefaultValue” does not belong to Platform.db.get\_tables().
  - Bind dependencies sys.
  - Bind dependencies secho.
  - Evaluate secho(multiline text in the contract, fg = “red”).
  - Evaluate sys.exit(1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0138.json#L6768) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1303) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1416)

<a id="op-b5ddef5ae77c90"></a>
### Import db from sql

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_2_import_database_from_database_query`

**Inputs** source\_sql = no value, verbose = false.

**Local steps**

- If verbose.
  - Evaluate print(“Starting database import...”).
- Set db\_name from Platform.conf.db\_name.
- If not source\_sql.
  - Set source\_sql from os.path.join(os.path.dirname(\_\_file\_\_), “framework\_postgres.sql”).
- Evaluate DbManager(Platform.local.db).restore\_database(verbose, db\_name, source\_sql, Platform.conf.db\_user, …).
- If verbose.
  - Evaluate print(“Imported from database {}”.format(source\_sql)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0138.json#L6983) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1307) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1419)

<a id="op-c64db9fc2947ce"></a>
### Get root connection

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_2_get_root_connection`

**Inputs** no declared parameters.

**Explicit results** Platform.local.flags.root\_connection.

**Local steps**

- If not Platform.local.flags.root\_connection.
  - Bind dependencies sys.
  - Bind dependencies getpass.
  - If not Platform.flags.root\_login.
    - Set Platform.flags.root\_login from (Platform.conf.get(“postgres\_root\_login”) or Platform.conf.get(“root\_login”) or (sys.\_\_stdin\_\_.isatty() and input(“Enter postgres super user &#91;postgres&#93;: ”)) or “postgres”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“postgres\_root\_login”) → Platform.conf.get(“root\_login”) → (sys.\_\_stdin\_\_.isatty() and input(“Enter postgres super user &#91;postgres&#93;: ”)) → “postgres”.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sys.\_\_stdin\_\_.isatty() → input(“Enter postgres super user &#91;postgres&#93;: ”).
  - If not Platform.flags.root\_password.
    - Set Platform.flags.root\_password from (Platform.conf.get(“postgres\_root\_password”) or Platform.conf.get(“root\_password”) or getpass(“Postgres super user password: ”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“postgres\_root\_password”) → Platform.conf.get(“root\_password”) → getpass(“Postgres super user password: ”).
  - Set Platform.local.flags.root\_connection from Platform.database.get\_db(socket = Platform.conf.db\_socket, host = Platform.conf.db\_host, port = Platform.conf.db\_port, user = Platform.flags.root\_login, …).
- Return Platform.local.flags.root\_connection.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0139.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1305) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1418)

<a id="op-3fac2686e51c7e"></a>
### Drop user and database

`operation_foundation_database_relational_storage_setup_persistent_records_business_behavior_2_drop_user_and_database`

**Inputs** db\_name, db\_user.

**Local steps**

- Set root\_conn from get\_root\_connection().
- Evaluate root\_conn.commit().
- Evaluate root\_conn.sql(query text (SELECT), tuple(db\_name)).
- Evaluate root\_conn.sql(“end”).
- Evaluate root\_conn.sql(formatted text DROP DATABASE IF EXISTS {db\_name}).
- Evaluate root\_conn.sql(formatted text DROP USER IF EXISTS {db\_user}).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0139.json#L490) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1304) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1417)

<a id="op-911ac4e06f6ae6"></a>
### Get sqlite version

`operation_foundation_database_sqlite_setup_persistent_records_business_behavior_get_sqlite_version`

**Inputs** no declared parameters.

**Declared result** str.

**State and service calls** execute a supplied database query.

**Explicit results** Platform.db.sql(“select sqlite\_version()”) at 0 at 0.

**Local steps**

- Return Platform.db.sql(“select sqlite\_version()”) at 0 at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L3324) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1415) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1522)

<a id="op-dad815fd1d4c92"></a>
### Setup database

`operation_foundation_database_sqlite_setup_persistent_records_business_behavior_setup_database`

**Inputs** force, verbose.

**Local steps**

- Set Platform.local.session from Platform.\_dict(mapping(“user” → “Administrator”)).
- Set root\_conn from get\_root\_connection().
- Evaluate root\_conn.close().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L3390) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1416) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1523)

<a id="op-6e0e1aa570b86b"></a>
### Bootstrap database

`operation_foundation_database_sqlite_setup_persistent_records_business_behavior_bootstrap_database`

**Inputs** verbose, source\_db = no value.

**Local steps**

- Bind dependencies sys.
- Evaluate copy\_db(source\_db, verbose).
- Evaluate Platform.connect().
- If “tabDefaultValue” does not belong to Platform.db.get\_tables(cached = false).
  - Bind dependencies secho.
  - Evaluate secho(multiline text in the contract, fg = “red”).
  - Evaluate sys.exit(1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L3523) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1411) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1518)

<a id="op-98932c29ab5525"></a>
### Copy db

`operation_foundation_database_sqlite_setup_persistent_records_business_behavior_copy_database`

**Inputs** db\_file = no value, verbose = false.

**Local steps**

- If verbose.
  - Evaluate print(“Starting database import...”).
- Set db\_name from Platform.conf.db\_name.
- If not db\_file.
  - Set db\_file from os.path.join(os.path.dirname(\_\_file\_\_), “framework\_sqlite.db”).
- Set db\_path from Path(db\_file).
- If not db\_path.exists().
  - Evaluate click.secho(formatted text Database {db\_path.as\_posix()} does not exist, fg = “red”).
  - Evaluate sys.exit(1).
- Set destination\_db\_folder from (Path(Platform.get\_site\_path()) ÷ “db”).
- If not destination\_db\_folder.exists().
  - Evaluate destination\_db\_folder.mkdir().
- Set destination\_db\_path from (destination\_db\_folder ÷ formatted text {db\_name}.db).
- If db\_path.suffix equals “.gz”.
  - Bind dependencies gzip.
  - Within gzip.open(db\_file, “rb”) bound as input, open(destination\_db\_path, “wb”) bound as output.
    - Evaluate shutil.copyfileobj(input, output).
- Otherwise.
  - Evaluate shutil.copy(db\_path, destination\_db\_path).
- If verbose.
  - Evaluate print(“Imported from database {}”.format(db\_path)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L3729) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1412) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1519)

<a id="op-87457ba391f97e"></a>
### Drop database

`operation_foundation_database_sqlite_setup_persistent_records_business_behavior_drop_database`

**Inputs** db\_name.

**Local steps**

- Evaluate Path(db\_name).unlink(missing\_ok = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L4354) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1413) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1520)
