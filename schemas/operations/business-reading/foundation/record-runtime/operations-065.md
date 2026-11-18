# Record lifecycle and persistence · operations 65

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Mysqlclient

<a id="op-b651883c1ddeea"></a>
### Maria DBConnection Util.get connection

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_connection_utility_get_connection_2`

**Inputs** self.

**Declared result** “MySQLdb.Connection”.

**Explicit results** self.create\_connection().

**Local steps**

- Return self.create\_connection().

**Methods declared on this owner** [create connection](operations-065.md#op-a661c8d88afc9d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L3512) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1240) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1359)

<a id="op-a661c8d88afc9d"></a>
### Maria DBConnection Util.create connection

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_connection_utility_create_connection`

**Inputs** self.

**Explicit results** MySQLdb.connect(expanded names self.get\_connection\_settings()).

**Local steps**

- Return MySQLdb.connect(expanded names self.get\_connection\_settings()).

**Methods declared on this owner** [get connection settings](operations-065.md#op-cfc6c00edd7486).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L3568) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1238) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1357)

<a id="op-68fba79b952173"></a>
### Maria DBConnection Util.set execution timeout

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_connection_utility_set_execution_timeout`

**Inputs** self, seconds.

**Local steps**

- Evaluate self.sql(“set session max\_statement\_time = %s”, float(seconds)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L131) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1242) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1361)

<a id="op-4b7fe92e750232"></a>
### Maria DBConnection Util.get execution timeout

`operation_foundation_binding_foundation_database_mariadb_mysqlclient_mariadbconnectionutil_get_execution_timeout`

**Inputs** self.

**Declared result** float.

**Explicit results** self.sql(“select @@session.max\_statement\_time”) at 0 at 0.

**Local steps**

- Return self.sql(“select @@session.max\_statement\_time”) at 0 at 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L201) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L683) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L659)

<a id="op-cfc6c00edd7486"></a>
### Maria DBConnection Util.get connection settings

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_connection_utility_get_connection_settings`

**Inputs** self.

**Declared result** dict.

**Explicit results** conn\_settings.

**Local steps**

- Set conn\_settings from mapping(“user” → self.user, “conv” → self.CONVERSION\_MAP, “charset” → “utf8mb4”, “use\_unicode” → true, …).
- If self.cur\_db\_name.
  - Set conn\_settings at “database” from self.cur\_db\_name.
- If self.socket.
  - Set conn\_settings at “unix\_socket” from self.socket.
- Otherwise.
  - Set conn\_settings at “host” from self.host.
  - If self.port.
    - Set conn\_settings at “port” from int(self.port).
- If self.password.
  - Set conn\_settings at “password” from self.password.
- If Platform.conf.db\_ssl\_ca.
  - Set ssl\_config from mapping(“ca” → Platform.conf.db\_ssl\_ca, “check\_hostname” → Platform.conf.db\_ssl\_check\_hostname).
  - If (Platform.conf.db\_ssl\_cert and Platform.conf.db\_ssl\_key).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.db\_ssl\_cert → Platform.conf.db\_ssl\_key.
    - Evaluate ssl\_config.update(mapping(“cert” → Platform.conf.db\_ssl\_cert, “key” → Platform.conf.db\_ssl\_key)).
  - Set conn\_settings at “ssl” from ssl\_config.
- Return conn\_settings.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L3857) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1241) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1360)

<a id="op-bc7ffae600f834"></a>
### Escape frozenset

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_escape_frozenset`

**Inputs** obj, mapping = no value.

**Explicit results** Platform.local.db.\_conn.literal(tuple(obj)).

**Local steps**

- Return Platform.local.db.\_conn.literal(tuple(obj)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L4387) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1235) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1354)

<a id="op-54837d51a8a4f0"></a>
### Escape timedelta

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_escape_timedelta`

**Inputs** obj, mapping = no value.

**Explicit results** fmt.format((((\_seconds floor divide 3600) modulo or format 24) + (obj.days × 24)), ((\_seconds floor divide 60) modulo or format 60), (\_seconds modulo or format 60), obj.microseconds).

**Local steps**

- Set \_seconds from obj.seconds.
- If obj.microseconds.
  - Set fmt from “'{0:02d}:{1:02d}:{2:02d}.{3:06d}'”.
- Otherwise.
  - Set fmt from “'{0:02d}:{1:02d}:{2:02d}'”.
- Return fmt.format((((\_seconds floor divide 3600) modulo or format 24) + (obj.days × 24)), ((\_seconds floor divide 60) modulo or format 60), (\_seconds modulo or format 60), obj.microseconds).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L4475) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1237) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1356)

<a id="op-456c51e5d9bebe"></a>
### Escape dict

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_escape_mapping`

**Inputs** obj, mapping = no value.

**Explicit failure paths** TypeError(“dict can not be used as parameter”).

**Local steps**

- Raise TypeError(“dict can not be used as parameter”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L4673) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1236) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1355)

<a id="op-fa10659b53397a"></a>
### Maria DBDatabase.setup type map

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_setup_type_map`

**Inputs** self.

**Local steps**

- Set self.db\_type from “mariadb”.
- Set self.type\_map from mapping(“Currency” → tuple(“decimal”, “21,9”), “Int” → tuple(“int”, “11”), “Long Int” → tuple(“bigint”, “20”), “Float” → tuple(“decimal”, “21,9”), …).

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L4738) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1269) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1386)

<a id="op-413ed879d2c3a8"></a>
### Maria DBDatabase.get database size

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_get_database_size`

**Inputs** self.

**Explicit results** db\_size at 0.get(“database\_size”).

**Local steps**

- Set db\_size from self.sql(query text (SELECT), self.cur\_db\_name, as\_dict = true).
- Return db\_size at 0.get(“database\_size”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L5549) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1258) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1375)

<a id="op-f273e4fa84e286"></a>
### Maria DBDatabase.log query

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_log_query`

**Inputs** self, query, query\_type, values, debug.

**Explicit results** mogrified\_query.

**Local steps**

- Set mogrified\_query from self.\_cursor.\_executed.decode().
- Set self.last\_query from mogrified\_query.
- Evaluate self.\_log\_query(mogrified\_query, query\_type, debug, query).
- Return mogrified\_query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L5744) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1266) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1383)

<a id="op-3189ad0f175d93"></a>
### Maria DBDatabase.clean up

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_clean_up`

**Inputs** self.

**Local steps**

- Set self.\_cursor.\_rows from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L5894) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1248) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1365)

<a id="op-015749c2ba40c0"></a>
### Maria DBDatabase.escape

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_escape`

**Inputs** s, percent = true.

**Wrappers, in declaration order** staticmethod.

**Explicit results** ((“'” + s) + “'”).

**Local steps**

- Set s from Platform.as\_unicode(escape\_string(s)).replace(“′”, “\\′”) when s, otherwise empty text.
  - Value choice on s — true gives Platform.as\_unicode(escape\_string(s)).replace(“′”, “\\′”), false gives empty text.
- If percent.
  - Set s from s.replace(“%”, “%%”).
- Return ((“'” + s) + “'”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L5944) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1253) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1370)

<a id="op-5b62170a5f0926"></a>
### Maria DBDatabase.is type number

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_is_type_number`

**Inputs** code.

**Wrappers, in declaration order** staticmethod.

**Explicit results** code equals MySQLdb.NUMBER.

**Local steps**

- Return code equals MySQLdb.NUMBER.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L6132) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1265) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1382)

<a id="op-ae77f187f122f5"></a>
### Maria DBDatabase.is type datetime

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_is_type_datetime`

**Inputs** code.

**Wrappers, in declaration order** staticmethod.

**Explicit results** code equals MySQLdb.DATETIME.

**Local steps**

- Return code equals MySQLdb.DATETIME.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L6190) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1264) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1381)

<a id="op-4d5641d13566b5"></a>
### Maria DBDatabase.rename table

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_rename_table`

**Inputs** self, old\_name, new\_name.

**Declared result** (list bitwise or tuple).

**Explicit results** self.sql(formatted text RENAME TABLE ′{old\_name}′ TO ′{new\_name}′).

**Local steps**

- Set old\_name from get\_table\_name(old\_name).
- Set new\_name from get\_table\_name(new\_name).
- Return self.sql(formatted text RENAME TABLE ′{old\_name}′ TO ′{new\_name}′).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L6248) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1268) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1385)

<a id="op-24e2e0906a998f"></a>
### Maria DBDatabase.describe

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_describe`

**Inputs** self, doctype.

**Declared result** (list bitwise or tuple).

**Explicit results** self.sql(formatted text DESC ′{table\_name}′).

**Local steps**

- Set table\_name from get\_table\_name(doctype).
- Return self.sql(formatted text DESC ′{table\_name}′).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L6427) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1252) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1369)

<a id="op-a45eb0de7779b8"></a>
### Maria DBDatabase.change column type

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_change_column_type`

**Inputs** self, doctype, column, type, nullable = false.

**Declared result** (list bitwise or tuple).

**Explicit results** self.sql\_ddl(formatted text ALTER TABLE ′{table\_name}′ MODIFY ′{column}′ {type} {null\_constraint}).

**Local steps**

- Set table\_name from get\_table\_name(doctype).
- Set null\_constraint from “NOT NULL” when not nullable, otherwise empty text.
  - Value choice on not nullable — true gives “NOT NULL”, false gives empty text.
- Return self.sql\_ddl(formatted text ALTER TABLE ′{table\_name}′ MODIFY ′{column}′ {type} {null\_constraint}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L6553) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1247) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1364)

<a id="op-e98193f36b6c92"></a>
### Maria DBDatabase.rename column

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_rename_column`

**Inputs** self, doctype, old\_column\_name, new\_column\_name.

**Local steps**

- Set current\_data\_type from self.get\_column\_type(doctype, old\_column\_name).
- Set table\_name from get\_table\_name(doctype).
- Evaluate Platform.db.sql\_ddl(formatted text ALTER TABLE ′{table\_name}′  CHANGE COLUMN ′{old\_column\_name}′  ′{new\_column\_name}′  {current\_data\_type}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get column type](operations-066.md#op-816f41d4aeab65).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L6788) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1267) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1384)

<a id="op-2db63a54c1e9a9"></a>
### Maria DBDatabase.create auth table

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_create_authentication_table`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L6996) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1249) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1366)

<a id="op-f07b5d81459685"></a>
### Maria DBDatabase.create global search table

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_create_global_search_table`

**Inputs** self.

**Local steps**

- If “\_\_global\_search” does not belong to self.get\_tables().
  - Evaluate self.sql(formatted text create table \_\_global\_search(  doctype varchar(100),  name varchar({self.VARCHAR\_LEN}),  title varchar({self.VARCHAR\_LEN}),  content text,).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get tables](operations-066.md#op-868064afcfd708).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L7050) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1250) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1367)

<a id="op-0b8fed56b7a3ec"></a>
### Maria DBDatabase.create user settings table

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_create_user_settings_table`

**Inputs** self.

**Local steps**

- Evaluate self.sql\_ddl(query text (CREATE)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L7207) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1251) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1368)

<a id="op-4c6f9e7c457447"></a>
### Maria DBDatabase.get on duplicate update

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_get_on_duplicate_update`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** “ON DUPLICATE key UPDATE ”.

**Local steps**

- Return “ON DUPLICATE key UPDATE ”.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L7261) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1259) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1376)

<a id="op-6dd8b310e9ada1"></a>
### Maria DBDatabase.get table columns description

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_get_table_columns_description`

**Inputs** self, table\_name.

**Explicit results** self.sql(query text (SELECT), mapping(“table\_name” → table\_name, “schema” → self.cur\_db\_name), as\_dict = 1).

**Local steps**

- Return self.sql(query text (SELECT), mapping(“table\_name” → table\_name, “schema” → self.cur\_db\_name), as\_dict = 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L133) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1261) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1378)
