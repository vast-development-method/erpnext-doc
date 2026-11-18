# Record lifecycle and persistence · operations 24

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Database

<a id="op-698c43d5f6e44b"></a>
### Postgres Exception Util.is table missing

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_table_missing`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** getattr(e, “pgcode”, no value) equals UNDEFINED\_TABLE.

**Local steps**

- Return getattr(e, “pgcode”, no value) equals UNDEFINED\_TABLE.

**Values supplied outside this operation** selected callable from getattr(e, “pgcode”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L4248) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1178) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1300)

<a id="op-da7fde4adaa2ae"></a>
### Postgres Exception Util.is missing table

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_missing_table`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** PostgresDatabase.is\_table\_missing(e).

**Local steps**

- Return PostgresDatabase.is\_table\_missing(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L4322) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1173) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1295)

<a id="op-1719bc81686a66"></a>
### Postgres Exception Util.is missing column

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_missing_column`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** getattr(e, “pgcode”, no value) equals UNDEFINED\_COLUMN.

**Local steps**

- Return getattr(e, “pgcode”, no value) equals UNDEFINED\_COLUMN.

**Values supplied outside this operation** selected callable from getattr(e, “pgcode”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L4381) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1172) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1294)

<a id="op-bb578e0da3f550"></a>
### Postgres Exception Util.is access denied

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_access_denied`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** getattr(e, “pgcode”, no value) equals INSUFFICIENT\_PRIVILEGE.

**Local steps**

- Return getattr(e, “pgcode”, no value) equals INSUFFICIENT\_PRIVILEGE.

**Values supplied outside this operation** selected callable from getattr(e, “pgcode”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L4455) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1164) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1287)

<a id="op-2a5d5e5f9b525a"></a>
### Postgres Exception Util.cant drop field or key

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_cant_drop_field_or_key`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** getattr(e, “pgcode”, no value) equals CLASS\_INTEGRITY\_CONSTRAINT\_VIOLATION.

**Local steps**

- Return getattr(e, “pgcode”, no value) equals CLASS\_INTEGRITY\_CONSTRAINT\_VIOLATION.

**Values supplied outside this operation** selected callable from getattr(e, “pgcode”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L4529) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1163) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1286)

<a id="op-5a58205c045c9e"></a>
### Postgres Exception Util.is duplicate entry

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_duplicate_entry`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** getattr(e, “pgcode”, no value) equals UNIQUE\_VIOLATION.

**Local steps**

- Return getattr(e, “pgcode”, no value) equals UNIQUE\_VIOLATION.

**Values supplied outside this operation** selected callable from getattr(e, “pgcode”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L4603) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1169) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1291)

<a id="op-e16bb86d6c3415"></a>
### Postgres Exception Util.is primary key violation

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_primary_key_violation`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** (getattr(e, “pgcode”, no value) equals UNIQUE\_VIOLATION and “\_pkey” belongs to cstr(e.args at 0)).

**Local steps**

- Return (getattr(e, “pgcode”, no value) equals UNIQUE\_VIOLATION and “\_pkey” belongs to cstr(e.args at 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(e, “pgcode”, no value) equals UNIQUE\_VIOLATION → “\_pkey” belongs to cstr(e.args at 0).

**Values supplied outside this operation** selected callable from getattr(e, “pgcode”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L4677) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1174) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1296)

<a id="op-c1240fcd264493"></a>
### Postgres Exception Util.is unique key violation

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_unique_key_violation`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** (getattr(e, “pgcode”, no value) equals UNIQUE\_VIOLATION and “\_key” belongs to cstr(e.args at 0)).

**Local steps**

- Return (getattr(e, “pgcode”, no value) equals UNIQUE\_VIOLATION and “\_key” belongs to cstr(e.args at 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(e, “pgcode”, no value) equals UNIQUE\_VIOLATION → “\_key” belongs to cstr(e.args at 0).

**Values supplied outside this operation** selected callable from getattr(e, “pgcode”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L126) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1180) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1302)

<a id="op-ed9cd504d09f49"></a>
### Postgres Exception Util.is duplicate fieldname

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_duplicate_fieldname`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** getattr(e, “pgcode”, no value) equals DUPLICATE\_COLUMN.

**Local steps**

- Return getattr(e, “pgcode”, no value) equals DUPLICATE\_COLUMN.

**Values supplied outside this operation** selected callable from getattr(e, “pgcode”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L4892) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1170) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1292)

<a id="op-db148b5f0669f2"></a>
### Postgres Exception Util.is statement timeout

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_statement_timeout`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** (PostgresDatabase.is\_timedout(e) or isinstance(e, Platform.QueryTimeoutError)).

**Local steps**

- Return (PostgresDatabase.is\_timedout(e) or isinstance(e, Platform.QueryTimeoutError)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in PostgresDatabase.is\_timedout(e) → isinstance(e, Platform.QueryTimeoutError).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L4966) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1176) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1298)

<a id="op-67c3e428117d94"></a>
### Postgres Exception Util.is data too long

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_data_too_long`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** getattr(e, “pgcode”, no value) equals STRING\_DATA\_RIGHT\_TRUNCATION.

**Local steps**

- Return getattr(e, “pgcode”, no value) equals STRING\_DATA\_RIGHT\_TRUNCATION.

**Values supplied outside this operation** selected callable from getattr(e, “pgcode”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L5055) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1165) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1288)

<a id="op-fb9235a4cca108"></a>
### Postgres Exception Util.is db table size limit

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_database_table_size_limit`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** false.

**Local steps**

- Return false.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L5216) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1167) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1289)

<a id="op-6085bce3487a28"></a>
### Postgres Exception Util.is interface error

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_interface_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** isinstance(e, InterfaceError).

**Local steps**

- Return isinstance(e, InterfaceError).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L5260) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1171) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1293)

<a id="op-030b1a7779e0ca"></a>
### Postgres Database.setup type map

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_setup_type_map`

**Inputs** self.

**Local steps**

- Set self.db\_type from “postgres”.
- Set self.type\_map from mapping(“Currency” → tuple(“decimal”, “21,9”), “Int” → tuple(“int”, no value), “Long Int” → tuple(“bigint”, no value), “Float” → tuple(“decimal”, “21,9”), …).

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L5319) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1158) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1282)

<a id="op-eb0530d44edd06"></a>
### Postgres Database.last query

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_last_query`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** LazyDecode(self.\_cursor.query).

**Local steps**

- Return LazyDecode(self.\_cursor.query).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L6131) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1151) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1277)

<a id="op-b0fa229b94ed2e"></a>
### Postgres Database.db schema

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_database_schema`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** nested operand in the contract.conf.get(“db\_schema”, “public”).replace(“'”, empty text).replace(“"”, empty text).

**Local steps**

- Return nested operand in the contract.conf.get(“db\_schema”, “public”).replace(“'”, empty text).replace(“"”, empty text).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L6194) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1133) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1261)

<a id="op-fc040aa546afd5"></a>
### Postgres Database.connect

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_connect`

**Inputs** self.

**Local steps**

- Evaluate super().connect().
- Evaluate self.\_cursor.execute(“SET search\_path TO %s”, tuple(self.db\_schema)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L6305) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1128) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1256)

<a id="op-aadfd52bc4dbf5"></a>
### Postgres Database.get connection

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_get_connection`

**Inputs** self.

**Explicit results** conn.

**Local steps**

- Set conn\_settings from mapping(“dbname” → self.cur\_db\_name, “user” → self.user, “host” → (self.host or self.socket)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.host → self.socket.
- If self.password.
  - Set conn\_settings at “password” from self.password.
- If (not self.socket and self.port).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.socket → self.port.
  - Set conn\_settings at “port” from self.port.
- Set conn from psycopg2.connect(expanded names conn\_settings).
- Evaluate conn.set\_isolation\_level(ISOLATION\_LEVEL\_REPEATABLE\_READ).
- Return conn.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L121) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1140) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1267)

<a id="op-1b263c65701216"></a>
### Postgres Database.set execution timeout

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_set_execution_timeout`

**Inputs** self, seconds.

**Local steps**

- Evaluate self.sql(“set local statement\_timeout = %s”, round((seconds × 1000))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L124) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1156) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1281)

<a id="op-fbf328b659f29d"></a>
### Postgres Database.get execution timeout

`operation_foundation_binding_foundation_database_postgres_database_postgresdatabase_get_execution_timeout`

**Inputs** self.

**Declared result** float.

**Explicit results** self.sql(query) at 0 at 0.

**Local steps**

- Set query from query text (SELECT).
- Return self.sql(query) at 0 at 0.

**Methods declared on this owner** [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L203) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L685) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L661)

<a id="op-c14e393cbc5440"></a>
### Postgres Database.execution timeout

`operation_foundation_binding_foundation_database_postgres_database_postgresdatabase_execution_timeout`

**Inputs** self, seconds.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Set previous\_timeout from self.get\_execution\_timeout().
- Evaluate self.set\_execution\_timeout(seconds).
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - If self.\_conn.get\_transaction\_status() differs from TRANSACTION\_STATUS\_INERROR.
    - Evaluate self.set\_execution\_timeout(previous\_timeout).

On ordinary fall-through the sequence ends.

**Methods declared on this owner** [get execution timeout](operations-024.md#op-fbf328b659f29d), [set execution timeout](operations-024.md#op-1b263c65701216).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L202) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L684) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L660)

<a id="op-1f1fd891b6c418"></a>
### Postgres Database.escape

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_escape`

**Inputs** self, s, percent = true.

**Explicit results** str(psycopg2.extensions.QuotedString(s)).

**Local steps**

- If isinstance(s, bytes).
  - Set s from s.decode(“utf-8”).
- If s is identical to no value.
  - Set s from empty text.
- If percent.
  - Set s from s.replace(“%”, “%%”).
- Set s from s.encode(“utf-8”).
- Return str(psycopg2.extensions.QuotedString(s)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L7026) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1135) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1263)

<a id="op-322e17c3ce8573"></a>
### Postgres Database.get database size

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_get_database_size`

**Inputs** self.

**Explicit results** db\_size at 0.get(“database\_size”).

**Local steps**

- Set db\_size from self.sql(“SELECT (pg\_database\_size(%s) / 1024 / 1024) as database\_size”, self.cur\_db\_name, as\_dict = true).
- Return db\_size at 0.get(“database\_size”).

**Methods declared on this owner** [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L7275) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1142) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1269)

<a id="op-123f9a13e7ede4"></a>
### Postgres Database.transform result

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_transform_result`

**Inputs** self, result.

**Declared result** tuple at tuple.

**Explicit results** tuple(result) when isinstance(result, list), otherwise result.

**Local steps**

- Return tuple(result) when isinstance(result, list), otherwise result.
  - Value choice on isinstance(result, list) — true gives tuple(result), false gives result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L7386) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1160) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1283)
