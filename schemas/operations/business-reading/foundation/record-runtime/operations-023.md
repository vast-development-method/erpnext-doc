# Record lifecycle and persistence · operations 23

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Database

<a id="op-7175db57f31280"></a>
### Maria DBDatabase.rename table

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_rename_table`

**Inputs** self, old\_name, new\_name.

**Declared result** (list bitwise or tuple).

**Explicit results** self.sql(formatted text RENAME TABLE ′{old\_name}′ TO ′{new\_name}′).

**Local steps**

- Set old\_name from get\_table\_name(old\_name).
- Set new\_name from get\_table\_name(new\_name).
- Return self.sql(formatted text RENAME TABLE ′{old\_name}′ TO ′{new\_name}′).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L4528) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1213) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1332)

<a id="op-0881f268f40864"></a>
### Maria DBDatabase.describe

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_describe`

**Inputs** self, doctype.

**Declared result** (list bitwise or tuple).

**Explicit results** self.sql(formatted text DESC ′{table\_name}′).

**Local steps**

- Set table\_name from get\_table\_name(doctype).
- Return self.sql(formatted text DESC ′{table\_name}′).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L4707) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1197) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1316)

<a id="op-03710f7312b385"></a>
### Maria DBDatabase.change column type

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_change_column_type`

**Inputs** self, doctype, column, type, nullable = false.

**Declared result** (list bitwise or tuple).

**Explicit results** self.sql\_ddl(formatted text ALTER TABLE ′{table\_name}′ MODIFY ′{column}′ {type} {null\_constraint}).

**Local steps**

- Set table\_name from get\_table\_name(doctype).
- Set null\_constraint from “NOT NULL” when not nullable, otherwise empty text.
  - Value choice on not nullable — true gives “NOT NULL”, false gives empty text.
- Return self.sql\_ddl(formatted text ALTER TABLE ′{table\_name}′ MODIFY ′{column}′ {type} {null\_constraint}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L4833) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1192) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1311)

<a id="op-1c537ca97e09ab"></a>
### Maria DBDatabase.rename column

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_rename_column`

**Inputs** self, doctype, old\_column\_name, new\_column\_name.

**Local steps**

- Set current\_data\_type from self.get\_column\_type(doctype, old\_column\_name).
- Set table\_name from get\_table\_name(doctype).
- Evaluate Platform.db.sql\_ddl(formatted text ALTER TABLE ′{table\_name}′  CHANGE COLUMN ′{old\_column\_name}′  ′{new\_column\_name}′  {current\_data\_type}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get column type](operations-023.md#op-cc378818b8581b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L5068) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1212) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1331)

<a id="op-ee0f2dc6117b25"></a>
### Maria DBDatabase.create auth table

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_create_authentication_table`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L5276) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1194) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1313)

<a id="op-0b5a9a5f423ec5"></a>
### Maria DBDatabase.create global search table

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_create_global_search_table`

**Inputs** self.

**Local steps**

- If “\_\_global\_search” does not belong to self.get\_tables().
  - Evaluate self.sql(formatted text create table \_\_global\_search(  doctype varchar(100),  name varchar({self.VARCHAR\_LEN}),  title varchar({self.VARCHAR\_LEN}),  content text,).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get tables](operations-023.md#op-48b4bf4981910b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L5330) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1195) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1314)

<a id="op-17547d8b5644f3"></a>
### Maria DBDatabase.create user settings table

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_create_user_settings_table`

**Inputs** self.

**Local steps**

- Evaluate self.sql\_ddl(query text (CREATE)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L5487) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1196) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1315)

<a id="op-bfdd7973711284"></a>
### Maria DBDatabase.get on duplicate update

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_get_on_duplicate_update`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** “ON DUPLICATE key UPDATE ”.

**Local steps**

- Return “ON DUPLICATE key UPDATE ”.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L5541) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1204) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1323)

<a id="op-3abf426f919d39"></a>
### Maria DBDatabase.get table columns description

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_get_table_columns_description`

**Inputs** self, table\_name.

**Explicit results** self.sql(query text (SELECT), mapping(“table\_name” → table\_name, “schema” → self.cur\_db\_name), as\_dict = 1).

**Local steps**

- Return self.sql(query text (SELECT), mapping(“table\_name” → table\_name, “schema” → self.cur\_db\_name), as\_dict = 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L129) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1206) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1325)

<a id="op-cc378818b8581b"></a>
### Maria DBDatabase.get column type

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_get_column_type`

**Inputs** self, doctype, column.

**Explicit results** nested operand in the contract.select(nested operand in the contract.column\_type).where(((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equ … at 0.

**Local steps**

- Set information\_schema from Platform.qb.Schema(“information\_schema”).
- Set table from get\_table\_name(doctype).
- Return nested operand in the contract.select(nested operand in the contract.column\_type).where(((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equ … at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L5682) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1201) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1320)

<a id="op-cdaa8158a09467"></a>
### Maria DBDatabase.has index

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_has_index`

**Inputs** self, table\_name, index\_name.

**Explicit results** self.sql(formatted text SHOW INDEX FROM ′{table\_name}′  WHERE Key\_name='{index\_name}').

**Local steps**

- Return self.sql(formatted text SHOW INDEX FROM ′{table\_name}′  WHERE Key\_name='{index\_name}').

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L5967) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1208) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1327)

<a id="op-c8b554ddba147a"></a>
### Maria DBDatabase.get column index

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_get_column_index`

**Inputs** self, table\_name, fieldname, unique = false.

**Declared result** (Platform.\_dict bitwise or no value).

**Explicit results** index.

**Local steps**

- Set indexes from self.sql(formatted text SHOW INDEX FROM ′{table\_name}′  WHERE Column\_name = BINARY "{fieldname}"  AND Seq\_in\_index = 1  AND Non\_unique={int(not unique)}  AND I, as\_dict = true).
- For each index in indexes.
  - Set clustered\_index from self.sql(formatted text SHOW INDEX FROM ′{table\_name}′  WHERE Key\_name = "{index.Key\_name}"  AND Seq\_in\_index = 2  , as\_dict = true).
  - If not clustered\_index.
    - Return index.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L6070) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1200) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1319)

<a id="op-eb5a3810dba2ca"></a>
### Maria DBDatabase.add index

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_add_index`

**Inputs** self, doctype, fields, index\_name = no value.

**Local steps**

- Bind dependencies make\_property\_setter.
- Set index\_name from (index\_name or self.get\_index\_name(fields)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in index\_name → self.get\_index\_name(fields).
- Set table\_name from get\_table\_name(doctype).
- If not self.has\_index(table\_name, index\_name).
  - Evaluate self.commit().
  - Evaluate self.sql(query text (ALTER).format(table\_name, index\_name, “, ”.join(fields))).
  - If (len(fields) equals 1 and not (Platform.flags.in\_install or Platform.flags.in\_migrate)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(fields) equals 1 → not (Platform.flags.in\_install or Platform.flags.in\_migrate).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_migrate.
    - Evaluate make\_property\_setter(doctype, fields at 0, property = “search\_index”, value = “1”, property\_type = “Check”, for\_doctype = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has index](operations-023.md#op-cdaa8158a09467).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L128) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1189) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1309)

<a id="op-d5a287ff01a687"></a>
### Maria DBDatabase.add unique

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_add_unique`

**Inputs** self, doctype, fields, constraint\_name = no value.

**Local steps**

- If isinstance(fields, str).
  - Set fields from list(fields).
- If not constraint\_name.
  - Set constraint\_name from (“unique\_” + “\_”.join(fields)).
- If not self.sql(query text (SELECT), tuple((“tab” + doctype), constraint\_name)).
  - Evaluate self.commit().
  - Evaluate self.sql(query text (ALTER).format(doctype, constraint\_name, “, ”.join(fields))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L7349) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1190) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1310)

<a id="op-f54dd82b91b8a5"></a>
### Maria DBDatabase.updatedb

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_updatedb`

**Inputs** self, doctype, meta = no value.

**Explicit failure paths** Exception(formatted text Wrong doctype {doctype} in updatedb).

**Local steps**

- Set res from self.sql(query text (SELECT, Doc Type), tuple(doctype)).
- If not res.
  - Raise Exception(formatted text Wrong doctype {doctype} in updatedb).
- If not res at 0 at 0.
  - Set db\_table from MariaDBTable(doctype, meta).
  - Evaluate db\_table.validate().
  - Evaluate db\_table.sync().
  - Evaluate self.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L7689) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1216) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1335)

<a id="op-39619461176f00"></a>
### Maria DBDatabase.get database list

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_get_database_list`

**Inputs** self.

**Explicit results** self.sql(“SHOW DATABASES”, pluck = true).

**Local steps**

- Return self.sql(“SHOW DATABASES”, pluck = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1202) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1321)

<a id="op-48b4bf4981910b"></a>
### Maria DBDatabase.get tables

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_get_tables`

**Inputs** self, cached = true.

**Explicit results** tables.

**Local steps**

- Set to\_query from not cached.
- If cached.
  - Set tables from Platform.client\_cache.get\_value(“db\_tables”).
  - Set to\_query from not tables.
- If to\_query.
  - Set information\_schema from Platform.qb.Schema(“information\_schema”).
  - Set tables from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.tables.table\_name).where(information\_schema.tables.table\_schema equals Platform.db.cur\_db\_name).run(pluck = true).
  - Evaluate Platform.client\_cache.set\_value(“db\_tables”, tables).
- Return tables.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L70) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1207) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1326)

<a id="op-86b39052029aef"></a>
### Maria DBDatabase.get row size

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_get_row_size`

**Inputs** self, doctype.

**Declared result** int.

**Record and data access** execute query text (SELECT).

**Explicit results** int(est\_row\_size at 0 at 0).

**Local steps**

- Set est\_row\_size from Platform.db.sql(query text (SELECT), tuple(get\_table\_name(doctype))).
- If est\_row\_size.
  - Return int(est\_row\_size at 0 at 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L406) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1205) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1324)

<a id="op-e5bea6bb3b2bc1"></a>
### Maria DBDatabase.unbuffered cursor

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_unbuffered_cursor`

**Inputs** self.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Bind dependencies SSCursor.
- Attempt the following.
  - If not self.\_conn.
    - Evaluate self.connect().
  - Set original\_cursor from self.\_cursor.
  - Set new\_cursor, self.\_cursor from self.\_conn.cursor(SSCursor).
  - yield no value.
- On exit, including pending return or failure.
  - Set self.\_cursor from original\_cursor.
  - Evaluate new\_cursor.close().

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L1374) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1215) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1334)

<a id="op-4a66e3ea837936"></a>
### Maria DBDatabase.estimate count

`operation_foundation_database_relational_storage_database_business_behavior_maria_database_database_estimate_count`

**Inputs** self, table.

**Declared result** int.

**Explicit results** cint(count at 0 at 0) when count, otherwise 0.

**Local steps**

- Bind dependencies cint.
- Set count from self.sql(query text (SELECT), tuple(table, Platform.db.cur\_db\_name)).
- Return cint(count at 0 at 0) when count, otherwise 0.
  - Value choice on count — true gives cint(count at 0 at 0), false gives 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L1568) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1199) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1318)

<a id="op-7e23e0ec69baa0"></a>
### Postgres Exception Util.is deadlocked

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_deadlocked`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** getattr(e, “pgcode”, no value) equals DEADLOCK\_DETECTED.

**Local steps**

- Return getattr(e, “pgcode”, no value) equals DEADLOCK\_DETECTED.

**Values supplied outside this operation** selected callable from getattr(e, “pgcode”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L125) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1168) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1290)

<a id="op-3870df68acdeb0"></a>
### Postgres Exception Util.is timedout

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_timedout`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** isinstance(e, (psycopg2.extensions.QueryCanceledError bitwise or LockNotAvailable)).

**Local steps**

- Return isinstance(e, (psycopg2.extensions.QueryCanceledError bitwise or LockNotAvailable)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L4053) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1179) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1301)

<a id="op-a475a7cd878b27"></a>
### Postgres Exception Util.is read only mode error

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_read_only_mode_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** isinstance(e, ReadOnlySqlTransaction).

**Local steps**

- Return isinstance(e, ReadOnlySqlTransaction).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L4128) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1175) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1297)

<a id="op-a8620c99a95fcb"></a>
### Postgres Exception Util.is syntax error

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_exception_utility_is_syntax_error`

**Inputs** e.

**Wrappers, in declaration order** staticmethod.

**Explicit results** isinstance(e, SyntaxError).

**Local steps**

- Return isinstance(e, SyntaxError).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L4189) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1177) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1299)
