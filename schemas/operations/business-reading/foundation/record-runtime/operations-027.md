# Record lifecycle and persistence · operations 27

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Database

<a id="op-cf59b9c03f54cf"></a>
### SQLite Database.get db path

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_get_database_path`

**Inputs** self.

**Explicit results** ((Path(Platform.get\_site\_path()) ÷ “db”) ÷ formatted text {self.cur\_db\_name}.db).

**Local steps**

- Return ((Path(Platform.get\_site\_path()) ÷ “db”) ÷ formatted text {self.cur\_db\_name}.db).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L7154) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1372) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1480)

<a id="op-d56d0fe4530caa"></a>
### SQLite Database.set execution timeout

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_set_execution_timeout`

**Inputs** self, seconds.

**Local steps**

- Evaluate self.sql(formatted text PRAGMA busy\_timeout = {round((seconds × 1000))}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L13) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1386) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1494)

<a id="op-8baa554d2f84c6"></a>
### SQLite Database.get execution timeout

`operation_foundation_binding_foundation_database_sqlite_database_sqlitedatabase_get_execution_timeout`

**Inputs** self.

**Declared result** float.

**Explicit results** (self.sql(“PRAGMA busy\_timeout”) at 0 at 0 ÷ 1000).

**Local steps**

- Return (self.sql(“PRAGMA busy\_timeout”) at 0 at 0 ÷ 1000).

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L207) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L689) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L665)

<a id="op-4189ffcd7a8874"></a>
### SQLite Database.setup type map

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_setup_type_map`

**Inputs** self.

**Local steps**

- Set self.db\_type from “sqlite”.
- Set self.type\_map from mapping(“Currency” → tuple(“REAL”, no value), “Int” → tuple(“INTEGER”, no value), “Long Int” → tuple(“INTEGER”, no value), “Float” → tuple(“REAL”, no value), …).

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L7401) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1388) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1495)

<a id="op-c16c639b06b6ab"></a>
### SQLite Database.get database size

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_get_database_size`

**Inputs** self.

**Explicit results** (os.path.getsize(self.get\_db\_path()) ÷ (1024 × 1024)).

**Local steps**

- Bind dependencies os.
- Return (os.path.getsize(self.get\_db\_path()) ÷ (1024 × 1024)).

**Methods declared on this owner** [get db path](operations-027.md#op-cf59b9c03f54cf).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L8127) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1373) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1481)

<a id="op-1a7eb0cdd87fa6"></a>
### SQLite Database.clean up

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_clean_up`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L8225) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1355) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1464)

<a id="op-868a2b87b9061b"></a>
### SQLite Database.escape

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_escape`

**Inputs** s, percent = true.

**Wrappers, in declaration order** staticmethod.

**Explicit results** ((“'” + s) + “'”).

**Local steps**

- Set s from s.replace(“'”, “''”).
- If percent.
  - Set s from s.replace(“%”, “%%”).
- Return ((“'” + s) + “'”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1365) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1473)

<a id="op-312163e598a17c"></a>
### SQLite Database.is type number

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_is_type_number`

**Inputs** code.

**Wrappers, in declaration order** staticmethod.

**Explicit results** code belongs to tuple(sqlite3.NUMERIC, sqlite3.INTEGER, sqlite3.REAL).

**Local steps**

- Return code belongs to tuple(sqlite3.NUMERIC, sqlite3.INTEGER, sqlite3.REAL).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L151) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1381) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1489)

<a id="op-e7dff286b1d73f"></a>
### SQLite Database.is type datetime

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_is_type_datetime`

**Inputs** code.

**Wrappers, in declaration order** staticmethod.

**Explicit results** code equals sqlite3.TEXT.

**Local steps**

- Return code equals sqlite3.TEXT.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L230) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1380) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1488)

<a id="op-17df23270f820c"></a>
### SQLite Database.rename table

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_rename_table`

**Inputs** self, old\_name, new\_name.

**Declared result** (list bitwise or tuple).

**Explicit results** self.sql(formatted text ALTER TABLE ′{old\_name}′ RENAME TO ′{new\_name}′).

**Local steps**

- Set old\_name from get\_table\_name(old\_name).
- Set new\_name from get\_table\_name(new\_name).
- Return self.sql(formatted text ALTER TABLE ′{old\_name}′ RENAME TO ′{new\_name}′).

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L288) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1384) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1492)

<a id="op-6071e6d2a946e6"></a>
### SQLite Database.describe

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_describe`

**Inputs** self, doctype.

**Declared result** (list bitwise or tuple).

**Explicit results** self.sql(formatted text PRAGMA table\_info(′{table\_name}′)).

**Local steps**

- Set table\_name from get\_table\_name(doctype).
- Return self.sql(formatted text PRAGMA table\_info(′{table\_name}′)).

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L468) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1364) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1472)

<a id="op-dedc9e53cead11"></a>
### SQLite Database.change column type

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_change_column_type`

**Inputs** self, doctype, column, type, nullable = false.

**Declared result** (list bitwise or tuple).

**Explicit failure paths** Platform.InvalidColumnName(formatted text Column {column} does not exist in table {table\_name}).

**Local steps**

- Set table\_name from get\_table\_name(doctype).
- Set temp\_table from formatted text {table\_name}\_new.
- Set columns from list().
- Set column\_exists from false.
- For each col in self.sql(formatted text PRAGMA table\_info(′{table\_name}′), as\_dict = 1).
  - If col at “name” equals column.
    - Set column\_exists from true.
    - Set null\_str from empty text when nullable, otherwise “ NOT NULL”.
      - Value choice on nullable — true gives empty text, false gives “ NOT NULL”.
    - Evaluate columns.append(formatted text ′{col at “name”}′ {type}{null\_str}).
  - Otherwise.
    - Set null\_str from empty text when col at “notnull” equals 0, otherwise “ NOT NULL”.
      - Value choice on col at “notnull” equals 0 — true gives empty text, false gives “ NOT NULL”.
    - Evaluate columns.append(formatted text ′{col at “name”}′ {col at “type”}{null\_str}).
- If not column\_exists.
  - Raise Platform.InvalidColumnName(formatted text Column {column} does not exist in table {table\_name}).
- Set create\_table from formatted text CREATE TABLE ′{temp\_table}′ ( {“,”.join(columns)} ).
- Evaluate self.sql\_ddl(create\_table).
- Set column\_names from list of formatted text ′{col at “name”}′ for col drawn from self.sql(formatted text PRAGMA table\_info(′{table\_name}′), as\_dict = 1).
  - Draw col from self.sql(formatted text PRAGMA table\_info(′{table\_name}′), as\_dict = 1).
- Set column\_list from “, ”.join(column\_names).
- Evaluate self.sql\_ddl(formatted text INSERT INTO ′{temp\_table}′ SELECT {column\_list} FROM ′{table\_name}′).
- Evaluate self.sql\_ddl(formatted text DROP TABLE ′{table\_name}′).
- Evaluate self.sql\_ddl(formatted text ALTER TABLE ′{temp\_table}′ RENAME TO ′{table\_name}′).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f), [sql ddl](operations-028.md#op-917f1d832686e5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L595) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1353) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1462)

<a id="op-b3730c3f9e82b2"></a>
### SQLite Database.rename column

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_rename_column`

**Inputs** self, doctype, old\_column\_name, new\_column\_name.

**Explicit failure paths** Platform.InvalidColumnName(formatted text Column {old\_column\_name} does not exist in table {table\_name}).

**Local steps**

- Set table\_name from get\_table\_name(doctype).
- Set temp\_table from formatted text {table\_name}\_new.
- Set columns from list().
- Set column\_exists from false.
- For each col in self.sql(formatted text PRAGMA table\_info(′{table\_name}′), as\_dict = 1).
  - If col at “name” equals old\_column\_name.
    - Set column\_exists from true.
    - Set null\_str from empty text when col at “notnull” equals 0, otherwise “ NOT NULL”.
      - Value choice on col at “notnull” equals 0 — true gives empty text, false gives “ NOT NULL”.
    - Evaluate columns.append(formatted text ′{new\_column\_name}′ {col at “type”}{null\_str}).
  - Otherwise.
    - Set null\_str from empty text when col at “notnull” equals 0, otherwise “ NOT NULL”.
      - Value choice on col at “notnull” equals 0 — true gives empty text, false gives “ NOT NULL”.
    - Evaluate columns.append(formatted text ′{col at “name”}′ {col at “type”}{null\_str}).
- If not column\_exists.
  - Raise Platform.InvalidColumnName(formatted text Column {old\_column\_name} does not exist in table {table\_name}).
- Set create\_table from formatted text CREATE TABLE ′{temp\_table}′ ( {“,”.join(columns)} ).
- Evaluate self.sql\_ddl(create\_table).
- Set column\_names from list().
- For each col in self.sql(formatted text PRAGMA table\_info(′{table\_name}′), as\_dict = 1).
  - If col at “name” equals old\_column\_name.
    - Evaluate column\_names.append(formatted text ′{old\_column\_name}′ as ′{new\_column\_name}′).
  - Otherwise.
    - Evaluate column\_names.append(formatted text ′{col at “name”}′).
- Set column\_list from “, ”.join(column\_names).
- Evaluate self.sql\_ddl(formatted text INSERT INTO ′{temp\_table}′ SELECT {column\_list} FROM ′{table\_name}′).
- Evaluate self.sql\_ddl(formatted text DROP TABLE ′{table\_name}′).
- Evaluate self.sql\_ddl(formatted text ALTER TABLE ′{temp\_table}′ RENAME TO ′{table\_name}′).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f), [sql ddl](operations-028.md#op-917f1d832686e5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L1604) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1383) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1491)

<a id="op-d9c51bcb7a5fb6"></a>
### SQLite Database.create auth table

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_create_authentication_table`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L2716) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1357) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1466)

<a id="op-66cafb5f665ce9"></a>
### SQLite Database.create global search table

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_create_global_search_table`

**Inputs** self.

**Local steps**

- If “\_\_global\_search” does not belong to self.get\_tables().
  - Evaluate self.sql(multiline text in the contract).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get tables](operations-028.md#op-a96ce0d6b76a70), [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L2772) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1359) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1468)

<a id="op-4595d01a5c92a0"></a>
### SQLite Database.create user settings table

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_create_user_settings_table`

**Inputs** self.

**Local steps**

- Evaluate self.sql\_ddl(query text (CREATE)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql ddl](operations-028.md#op-917f1d832686e5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L2863) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1361) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1469)

<a id="op-98af3d0f416bd9"></a>
### SQLite Database.get on duplicate update

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_get_on_duplicate_update`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** “ON CONFLICT DO UPDATE SET ”.

**Local steps**

- Return “ON CONFLICT DO UPDATE SET ”.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L3005) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1375) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1483)

<a id="op-dbad93cd41983d"></a>
### SQLite Database.get table columns description

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_get_table_columns_description`

**Inputs** self, table\_name.

**Explicit results** self.sql(formatted text PRAGMA table\_info(′{table\_name}′), as\_dict = 1).

**Local steps**

- Return self.sql(formatted text PRAGMA table\_info(′{table\_name}′), as\_dict = 1).

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L3053) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1377) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1485)

<a id="op-a6112a61afbc9d"></a>
### SQLite Database.get column type

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_get_column_type`

**Inputs** self, doctype, column.

**Explicit results** row at “type” · no value.

**Local steps**

- Set table\_name from get\_table\_name(doctype).
- Set result from self.sql(formatted text PRAGMA table\_info(′{table\_name}′), as\_dict = 1).
- For each row in result.
  - If row at “name” equals column.
    - Return row at “type”.
- Return no value.

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L3146) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1369) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1477)

<a id="op-8054d42b21d97f"></a>
### SQLite Database.has index

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_has_index`

**Inputs** self, table\_name, index\_name.

**Explicit results** self.sql(formatted text SELECT \* FROM pragma\_index\_list(′{table\_name}′) WHERE name = '{index\_name}').

**Local steps**

- Return self.sql(formatted text SELECT \* FROM pragma\_index\_list(′{table\_name}′) WHERE name = '{index\_name}').

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L3353) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1379) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1487)

<a id="op-7a2c3358d955b8"></a>
### SQLite Database.get column index

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_get_column_index`

**Inputs** self, table\_name, fieldname, unique = false.

**Declared result** (Platform.\_dict bitwise or no value).

**Explicit results** index.

**Local steps**

- Set indexes from self.sql(formatted text PRAGMA index\_list(′{table\_name}′), as\_dict = true).
- For each index in indexes.
  - Set index\_info from self.sql(formatted text PRAGMA index\_info(′{index at “name”}′), as\_dict = true).
  - If (index\_info and index\_info at 0 at “name” equals fieldname).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in index\_info → index\_info at 0 at “name” equals fieldname.
    - Return index.

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L3483) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1368) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1476)

<a id="op-61371897ba07f8"></a>
### SQLite Database.add index

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_add_index`

**Inputs** self, doctype, fields, index\_name = no value.

**Local steps**

- Bind dependencies make\_property\_setter.
- Set fields from list of re.sub(“\\(.\*?\\)”, empty text, field) for field drawn from fields.
  - Draw field from fields.
- Set index\_name from (index\_name or self.get\_index\_name(fields)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in index\_name → self.get\_index\_name(fields).
- Set table\_name from get\_table\_name(doctype).
- Evaluate self.commit().
- Evaluate self.sql(formatted text CREATE INDEX IF NOT EXISTS ′{index\_name}′ ON ′{table\_name}′ ({“, ”.join(fields)})).
- If (len(fields) equals 1 and not (Platform.flags.in\_install or Platform.flags.in\_migrate)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(fields) equals 1 → not (Platform.flags.in\_install or Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_migrate.
  - Evaluate make\_property\_setter(doctype, fields at 0, property = “search\_index”, value = “1”, property\_type = “Check”, for\_doctype = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [commit](operations-028.md#op-7d35792a43af93), [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L10) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1350) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1459)

<a id="op-b12be799a32760"></a>
### SQLite Database.add unique

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_add_unique`

**Inputs** self, doctype, fields, constraint\_name = no value.

**Local steps**

- If isinstance(fields, str).
  - Set fields from list(fields).
- If not constraint\_name.
  - Set constraint\_name from formatted text unique\_{“\_”.join(fields)}.
- Set table\_name from get\_table\_name(doctype).
- Set columns from “, ”.join(fields).
- Set sql\_create\_unique from formatted text CREATE UNIQUE INDEX IF NOT EXISTS ′{constraint\_name}′ ON ′{table\_name}′ ({columns}).
- Evaluate self.commit().
- Evaluate self.sql(sql\_create\_unique).

If control reaches the end, it returns no value.

**Methods declared on this owner** [commit](operations-028.md#op-7d35792a43af93), [sql](operations-028.md#op-8d967b1a400a8f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L4283) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1351) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1460)

<a id="op-4ea0813e56928f"></a>
### SQLite Database.updatedb

`operation_foundation_database_sqlite_database_business_behavior_supplier_quotation_lite_database_updatedb`

**Inputs** self, doctype, meta = no value.

**Explicit failure paths** Exception(formatted text Wrong doctype {doctype} in updatedb).

**Local steps**

- Set res from self.sql(query text (SELECT, Doc Type), tuple(doctype)).
- If not res.
  - Raise Exception(formatted text Wrong doctype {doctype} in updatedb).
- If not res at 0 at 0.
  - Set db\_table from SQLiteTable(doctype, meta).
  - Evaluate db\_table.validate().
  - Evaluate db\_table.sync().
  - Evaluate self.commit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-028.md#op-8d967b1a400a8f), [commit](operations-028.md#op-7d35792a43af93).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0147.json#L4605) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1390) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1497)
