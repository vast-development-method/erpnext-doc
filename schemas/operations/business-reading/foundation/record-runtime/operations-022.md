# Record lifecycle and persistence · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Database

<a id="op-d15cff8f5cab71"></a>
### Maria DBException Util.is duplicate entry

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_duplicate_entry`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.DUP\_ENTRY).

**Local steps**

- Return (e.args and e.args at 0 equals ER.DUP\_ENTRY).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.DUP\_ENTRY.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L951) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1223) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1342)

<a id="op-43edeb7836cc74"></a>
### Maria DBException Util.is access denied

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_access_denied`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.ACCESS\_DENIED\_ERROR).

**Local steps**

- Return (e.args and e.args at 0 equals ER.ACCESS\_DENIED\_ERROR).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.ACCESS\_DENIED\_ERROR.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L1041) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1218) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1337)

<a id="op-e20021e1ec41c8"></a>
### Maria DBException Util.cant drop field or key

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_cant_drop_field_or_key`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.CANT\_DROP\_FIELD\_OR\_KEY).

**Local steps**

- Return (e.args and e.args at 0 equals ER.CANT\_DROP\_FIELD\_OR\_KEY).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.CANT\_DROP\_FIELD\_OR\_KEY.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L1131) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1217) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1336)

<a id="op-355a9188993f6b"></a>
### Maria DBException Util.is syntax error

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_syntax_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.PARSE\_ERROR).

**Local steps**

- Return (e.args and e.args at 0 equals ER.PARSE\_ERROR).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.PARSE\_ERROR.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L1221) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1231) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1350)

<a id="op-9fc82d0c9a6af7"></a>
### Maria DBException Util.is statement timeout

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_statement_timeout`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals 1969).

**Local steps**

- Return (e.args and e.args at 0 equals 1969).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals 1969.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L1311) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1230) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1349)

<a id="op-45bca6d02f8b78"></a>
### Maria DBException Util.is data too long

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_data_too_long`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.DATA\_TOO\_LONG).

**Local steps**

- Return (e.args and e.args at 0 equals ER.DATA\_TOO\_LONG).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.DATA\_TOO\_LONG.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L1397) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1219) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1338)

<a id="op-327bfc323a771f"></a>
### Maria DBException Util.is data truncated

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_data_truncated`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.TRUNCATED\_WRONG\_VALUE).

**Local steps**

- Return (e.args and e.args at 0 equals ER.TRUNCATED\_WRONG\_VALUE).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.TRUNCATED\_WRONG\_VALUE.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L130) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1220) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1339)

<a id="op-92f4fa68d0041b"></a>
### Maria DBException Util.is db table size limit

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_database_table_size_limit`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (e.args and e.args at 0 equals ER.TOO\_BIG\_ROWSIZE).

**Local steps**

- Return (e.args and e.args at 0 equals ER.TOO\_BIG\_ROWSIZE).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.args → e.args at 0 equals ER.TOO\_BIG\_ROWSIZE.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L1590) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1221) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1340)

<a id="op-cba799b1587a90"></a>
### Maria DBException Util.is primary key violation

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_primary_key_violation`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (MariaDBDatabase.is\_duplicate\_entry(e) and “PRIMARY” belongs to cstr(e.args at 1) and isinstance(e, pymysql.IntegrityError)).

**Local steps**

- Return (MariaDBDatabase.is\_duplicate\_entry(e) and “PRIMARY” belongs to cstr(e.args at 1) and isinstance(e, pymysql.IntegrityError)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in MariaDBDatabase.is\_duplicate\_entry(e) → “PRIMARY” belongs to cstr(e.args at 1) → isinstance(e, pymysql.IntegrityError).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L1680) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1228) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1347)

<a id="op-fc9b10b7f9ce0a"></a>
### Maria DBException Util.is unique key violation

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_unique_key_violation`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** (MariaDBDatabase.is\_duplicate\_entry(e) and “Duplicate” belongs to cstr(e.args at 1) and isinstance(e, pymysql.IntegrityError)).

**Local steps**

- Return (MariaDBDatabase.is\_duplicate\_entry(e) and “Duplicate” belongs to cstr(e.args at 1) and isinstance(e, pymysql.IntegrityError)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in MariaDBDatabase.is\_duplicate\_entry(e) → “Duplicate” belongs to cstr(e.args at 1) → isinstance(e, pymysql.IntegrityError).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L1818) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1234) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1353)

<a id="op-9a3f186766c9ee"></a>
### Maria DBException Util.is interface error

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_exception_utility_is_interface_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** isinstance(e, pymysql.InterfaceError).

**Local steps**

- Return isinstance(e, pymysql.InterfaceError).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L1956) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1225) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1344)

<a id="op-7b85730ba79b3a"></a>
### Maria DBConnection Util.get connection

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_connection_utility_get_connection`

**Inputs** self.

**Explicit results** conn.

**Local steps**

- Set conn from self.\_get\_connection().
- Set conn.auto\_reconnect from true.
- Return conn.

**Methods declared on this owner** [get connection](operations-022.md#op-715d323ba1de37).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L2024) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1184) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1305)

<a id="op-715d323ba1de37"></a>
### Maria DBConnection Util.get connection

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_connection_utility_get_connection_2`

**Inputs** self.

**Explicit results** self.create\_connection().

**Local steps**

- Return self.create\_connection().

**Methods declared on this owner** [create connection](operations-022.md#op-3c36b164447255).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L2105) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1185) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1306)

<a id="op-3c36b164447255"></a>
### Maria DBConnection Util.create connection

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_connection_utility_create_connection`

**Inputs** self.

**Explicit results** pymysql.connect(expanded names self.get\_connection\_settings()).

**Local steps**

- Return pymysql.connect(expanded names self.get\_connection\_settings()).

**Methods declared on this owner** [get connection settings](operations-022.md#op-8f3719e87ff90a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L2156) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1183) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1304)

<a id="op-c1955d6e71e8f2"></a>
### Maria DBConnection Util.set execution timeout

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_connection_utility_set_execution_timeout`

**Inputs** self, seconds.

**Local steps**

- Evaluate self.sql(“set session max\_statement\_time = %s”, float(seconds)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L127) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1187) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1308)

<a id="op-119fac33c263e3"></a>
### Maria DBConnection Util.get execution timeout

`operation_foundation_binding_foundation_database_mariadb_database_mariadbconnectionutil_get_execution_timeout`

**Inputs** self.

**Declared result** float.

**Explicit results** self.sql(“select @@session.max\_statement\_time”) at 0 at 0.

**Local steps**

- Return self.sql(“select @@session.max\_statement\_time”) at 0 at 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L200) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L682) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L658)

<a id="op-8f3719e87ff90a"></a>
### Maria DBConnection Util.get connection settings

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_connection_utility_get_connection_settings`

**Inputs** self.

**Declared result** dict.

**Explicit results** conn\_settings.

**Local steps**

- Set conn\_settings from mapping(“user” → self.user, “conv” → self.CONVERSION\_MAP, “charset” → “utf8mb4”, “collation” → “utf8mb4\_unicode\_ci”, …).
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

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L2445) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1186) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1307)

<a id="op-98887331e9ad30"></a>
### Maria DBDatabase.setup type map

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_setup_type_map`

**Inputs** self.

**Local steps**

- Set self.db\_type from “mariadb”.
- Set self.type\_map from mapping(“Currency” → tuple(“decimal”, “21,9”), “Int” → tuple(“int”, “11”), “Long Int” → tuple(“bigint”, “20”), “Float” → tuple(“decimal”, “21,9”), …).

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L2975) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1214) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1333)

<a id="op-0ec84507b3d9e4"></a>
### Maria DBDatabase.get database size

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_get_database_size`

**Inputs** self.

**Explicit results** db\_size at 0.get(“database\_size”).

**Local steps**

- Set db\_size from self.sql(query text (SELECT), self.cur\_db\_name, as\_dict = true).
- Return db\_size at 0.get(“database\_size”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L3786) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1203) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1322)

<a id="op-57a8bc7065f264"></a>
### Maria DBDatabase.log query

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_log_query`

**Inputs** self, query, query\_type, values, debug.

**Explicit results** mogrified\_query.

**Local steps**

- Set mogrified\_query from self.\_cursor.\_executed.
- Set self.last\_query from mogrified\_query.
- Evaluate self.\_log\_query(mogrified\_query, query\_type, debug, query).
- Return mogrified\_query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L3981) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1211) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1330)

<a id="op-eae58cbc75b8de"></a>
### Maria DBDatabase.clean up

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_clean_up`

**Inputs** self.

**Local steps**

- Set self.\_cursor.\_result from no value.
- Set self.\_cursor.\_rows from no value.
- Set self.\_cursor.connection.\_result from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L4120) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1193) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1312)

<a id="op-0beb8c98857009"></a>
### Maria DBDatabase.escape

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_escape`

**Inputs** s, percent = true.

**Wrappers, in declaration order** staticmethod.

**Explicit results** ((“'” + s) + “'”).

**Local steps**

- Set s from Platform.as\_unicode(escape\_string(Platform.as\_unicode(s)), “utf-8”).replace(“′”, “\\′”).
- If percent.
  - Set s from s.replace(“%”, “%%”).
- Return ((“'” + s) + “'”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L4214) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1198) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1317)

<a id="op-41ff04b911d458"></a>
### Maria DBDatabase.is type number

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_is_type_number`

**Inputs** code.

**Wrappers, in declaration order** staticmethod.

**Explicit results** code equals pymysql.NUMBER.

**Local steps**

- Return code equals pymysql.NUMBER.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L4412) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1210) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1329)

<a id="op-2913d2a0b15492"></a>
### Maria DBDatabase.is type datetime

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_is_type_datetime`

**Inputs** code.

**Wrappers, in declaration order** staticmethod.

**Explicit results** code equals pymysql.DATETIME.

**Local steps**

- Return code equals pymysql.DATETIME.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L4470) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1209) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1328)
