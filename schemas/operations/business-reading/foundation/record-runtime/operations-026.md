# Record lifecycle and persistence · operations 26

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Database

<a id="op-aaaac83a6e5d5e"></a>
### Postgres Database.unbuffered cursor

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_unbuffered_cursor`

**Inputs** self.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Attempt the following.
  - If not self.\_conn.
    - Evaluate self.connect().
  - Set original\_cursor from self.\_cursor.
  - Set new\_cursor, self.\_cursor from self.\_conn.cursor(name = “ss\_cursor”).
  - yield no value.
- On exit, including pending return or failure.
  - Set self.\_cursor from original\_cursor.
  - Evaluate new\_cursor.close().

On ordinary fall-through the sequence ends.

**Methods declared on this owner** [connect](operations-024.md#op-fc040aa546afd5).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L6647) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1161) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1284)

<a id="op-07dabf515d18ee"></a>
### Modify query

`operation_foundation_database_relational_storage_database_business_behavior_2_modify_query`

**Inputs** query.

**Explicit results** PG\_TRANSFORM\_PATTERN.sub(“\\1 '\\2'”, query).

**Local steps**

- Set query from convert\_backtick\_identifiers(str(query)).
- Set query from replace\_locate\_with\_strpos(query).
- Set query from FROM\_TAB\_PATTERN.sub(“from "tab\\1"”, query).
- Return PG\_TRANSFORM\_PATTERN.sub(“\\1 '\\2'”, query).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L113) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1117) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1249)

<a id="op-40e15b9158703d"></a>
### Modify values

`operation_foundation_database_relational_storage_database_business_behavior_2_modify_values`

**Inputs** values.

**Explicit results** values.

**Local steps**

- Bind local operation modify\_value for subsequent calls.
- If (not values or values equals EmptyQueryValues).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not values → values equals EmptyQueryValues.
  - Return values.
- If isinstance(values, dict).
  - For each tuple(k, v) in values.items().
    - Set values at k from modify\_value(v).
- Otherwise.
  - If isinstance(values, (tuple bitwise or list)).
    - Set new\_values from list().
    - For each val in values.
      - Evaluate new\_values.append(modify\_value(val)).
    - Set values from new\_values.
  - Otherwise.
    - Set values from modify\_value(values).
- Return values.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L114) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1118) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1250)

<a id="op-25960b89ac1170"></a>
### Modify values.modify value

`operation_foundation_database_relational_storage_database_business_behavior_2_modify_values_modify_value`

**Inputs** value.

**Explicit results** value.

**Local steps**

- If isinstance(value, (list bitwise or tuple)).
  - Set value from tuple(modify\_values(value)).
- Otherwise.
  - If isinstance(value, int).
    - Set value from str(value).
- Return value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L115) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1119) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1251)

<a id="op-a7ef52be2b70bc"></a>
### Replace locate with strpos

`operation_foundation_database_relational_storage_database_business_behavior_2_replace_locate_with_strpos`

**Inputs** query.

**Explicit results** query.

**Local steps**

- If LOCATE\_QUERY\_PATTERN.search(query).
  - Set query from LOCATE\_SUB\_PATTERN.sub(“strpos(\\2\\3, \\1)”, query).
- Return query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0137.json#L2409) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1181) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1303)

<a id="op-6d9144afc4527c"></a>
### SQLite Exception Util.is deadlocked

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_deadlocked`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “database is locked” belongs to str(e).

**Local steps**

- Return “database is locked” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5068) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1395) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1502)

<a id="op-5e82ad4df85a9d"></a>
### SQLite Exception Util.is timedout

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_timedout`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “database is locked” belongs to str(e).

**Local steps**

- Return “database is locked” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5142) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1406) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1513)

<a id="op-6505d3bdda313b"></a>
### SQLite Exception Util.is read only mode error

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_read_only_mode_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “attempt to write a readonly database” belongs to str(e).

**Local steps**

- Return “attempt to write a readonly database” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5216) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1402) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1509)

<a id="op-f7999bd98e813e"></a>
### SQLite Exception Util.is table missing

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_table_missing`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “no such table” belongs to str(e).

**Local steps**

- Return “no such table” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5290) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1405) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1512)

<a id="op-cff7abfe051256"></a>
### SQLite Exception Util.is missing column

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_missing_column`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “no such column” belongs to str(e).

**Local steps**

- Return “no such column” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5364) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1399) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1506)

<a id="op-0f0241d50d006a"></a>
### SQLite Exception Util.is duplicate fieldname

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_duplicate_fieldname`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “duplicate column name” belongs to str(e).

**Local steps**

- Return “duplicate column name” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5438) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1397) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1504)

<a id="op-fd3a9f6af74080"></a>
### SQLite Exception Util.is duplicate entry

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_duplicate_entry`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “UNIQUE constraint failed” belongs to str(e).

**Local steps**

- Return “UNIQUE constraint failed” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5512) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1396) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1503)

<a id="op-4e948f2b3f8534"></a>
### SQLite Exception Util.is access denied

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_access_denied`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “access denied” belongs to str(e).

**Local steps**

- Return “access denied” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5586) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1392) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1499)

<a id="op-5889df61b4ace7"></a>
### SQLite Exception Util.cant drop field or key

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_cant_drop_field_or_key`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “cannot drop” belongs to str(e).

**Local steps**

- Return “cannot drop” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5660) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1391) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1498)

<a id="op-1642f8400458d7"></a>
### SQLite Exception Util.is syntax error

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_syntax_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “syntax error” belongs to str(e).

**Local steps**

- Return “syntax error” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5734) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1404) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1511)

<a id="op-13794e50eaa4cd"></a>
### SQLite Exception Util.is statement timeout

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_statement_timeout`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “statement timeout” belongs to str(e).

**Local steps**

- Return “statement timeout” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5808) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1403) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1510)

<a id="op-4d6e06b030d606"></a>
### SQLite Exception Util.is data too long

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_data_too_long`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “string or blob too big” belongs to str(e).

**Local steps**

- Return “string or blob too big” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5882) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1393) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1500)

<a id="op-5130b6d4bdcfc3"></a>
### SQLite Exception Util.is db table size limit

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_database_table_size_limit`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** “too many columns” belongs to str(e).

**Local steps**

- Return “too many columns” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L5956) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1394) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1501)

<a id="op-73a9d900fdcab2"></a>
### SQLite Exception Util.is primary key violation

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_primary_key_violation`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** e.sqlite\_errorcode equals 1555 · “UNIQUE constraint failed” belongs to str(e).

**Local steps**

- If hasattr(e, “sqlite\_errorcode”).
  - Return e.sqlite\_errorcode equals 1555.
- Return “UNIQUE constraint failed” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L6030) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1401) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1508)

<a id="op-f1ca5346a5b8fb"></a>
### SQLite Exception Util.is unique key violation

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_unique_key_violation`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** e.sqlite\_errorcode equals 2067 · “UNIQUE constraint failed” belongs to str(e).

**Local steps**

- If hasattr(e, “sqlite\_errorcode”).
  - Return e.sqlite\_errorcode equals 2067.
- Return “UNIQUE constraint failed” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L6153) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1407) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1514)

<a id="op-878b2e58b73660"></a>
### SQLite Exception Util.is interface error

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_interface_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** isinstance(e, sqlite3.InterfaceError).

**Local steps**

- Return isinstance(e, sqlite3.InterfaceError).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L6276) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1398) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1505)

<a id="op-8741dac8ee8d60"></a>
### SQLite Exception Util.is nested transaction error

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_exception_utility_is_nested_transaction_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** “cannot start a transaction within a transaction” belongs to str(e).

**Local steps**

- Return “cannot start a transaction within a transaction” belongs to str(e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L6344) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1400) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1507)

<a id="op-a3ce78ad9016d1"></a>
### SQLite Database.get connection

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_get_connection`

**Inputs** self, read\_only = false.

**Explicit results** conn.

**Local steps**

- Set conn from self.create\_connection(read\_only).
- Evaluate conn.create\_function(“regexp”, 2, regexp).
- Evaluate conn.create\_function(“regexp\_replace”, 3, regexp\_replace).
- Set pragmas from mapping(“journal\_mode” → “WAL”, “synchronous” → “NORMAL”, “busy\_timeout” → 5000).
- Set cursor from conn.cursor().
- For each tuple(pragma, value) in pragmas.items().
  - Evaluate cursor.execute(formatted text PRAGMA {pragma}={value}).
- Evaluate cursor.close().
- Return conn.

**Methods declared on this owner** [create connection](operations-026.md#op-a811c2cd4cc977).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L6416) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1370) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1478)

<a id="op-a811c2cd4cc977"></a>
### SQLite Database.create connection

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_create_connection`

**Inputs** self, read\_only = false.

**Explicit results** sqlite3.connect(formatted text file:{db\_path}?mode=ro, uri = true, detect\_types = sqlite3.PARSE\_DECLTYPES, timeout = 15) · sqlite3.connect(db\_path, detect\_types = sqlite3.PARSE\_DECLTYPES, timeout = 15).

**Local steps**

- Set db\_path from self.get\_db\_path().
- Evaluate sqlite3.register\_converter(“timestamp”, deferred anonymous expression).
- Evaluate sqlite3.register\_converter(“date”, deferred anonymous expression).
- Evaluate sqlite3.register\_converter(“time”, deferred anonymous expression).
- If read\_only.
  - Return sqlite3.connect(formatted text file:{db\_path}?mode=ro, uri = true, detect\_types = sqlite3.PARSE\_DECLTYPES, timeout = 15).
- Return sqlite3.connect(db\_path, detect\_types = sqlite3.PARSE\_DECLTYPES, timeout = 15).

**Methods declared on this owner** [get db path](operations-027.md#op-cf59b9c03f54cf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L6741) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1358) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1467)
