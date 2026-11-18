# Record lifecycle and persistence · operations 25

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Database

<a id="op-9f02be2ab06ad1"></a>
### Postgres Database.sql

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_database_query`

**Inputs** self, query, values = EmptyQueryValues, remaining positional values args, remaining named values kwargs.

**Explicit results** super().sql(modify\_query(query), modify\_values(values), expanded args, expanded names kwargs).

**Local steps**

- Return super().sql(modify\_query(query), modify\_values(values), expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L7517) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1132) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1260)

<a id="op-3599199d6a80f9"></a>
### Postgres Database.lazy mogrify

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_lazy_mogrify`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Declared result** str.

**Explicit results** self.last\_query.

**Local steps**

- Return self.last\_query.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L7655) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1152) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1278)

<a id="op-65c0b578f98bfc"></a>
### Postgres Database.get tables

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_get_tables`

**Inputs** self, cached = true.

**Explicit results** list of d at 0 for d drawn from self.sql(query text (SELECT), tuple(self.cur\_db\_name, self.db\_schema)).

**Local steps**

- Return list of d at 0 for d drawn from self.sql(query text (SELECT), tuple(self.cur\_db\_name, self.db\_schema)).
  - Draw d from self.sql(query text (SELECT), tuple(self.cur\_db\_name, self.db\_schema)).

**Methods declared on this owner** [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L123) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1146) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1273)

<a id="op-a25241d081d093"></a>
### Postgres Database.get db table columns

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_get_database_table_columns`

**Inputs** self, table.

**Declared result** list at str.

**Explicit results** columns.

**Local steps**

- Set key from formatted text table\_columns::{table}.
- If columns bound to Platform.client\_cache.get\_value(key) is distinct from no value.
  - Return columns.
- Set information\_schema from Platform.qb.Schema(“information\_schema”).
- Set columns from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.columns.column\_name).where((nested operand in the contract.columns.table\_name equals table bitwise and n ….
- Evaluate Platform.client\_cache.set\_value(key, columns).
- Return columns.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L434) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1143) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1270)

<a id="op-b18ef50cc152cf"></a>
### Postgres Database.format date

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_format_date`

**Inputs** self, date.

**Explicit results** “0001-01-01” · date.

**Local steps**

- If not date.
  - Return “0001-01-01”.
- If not isinstance(date, str).
  - Set date from date.strftime(“%Y-%m-%d”).
- Return date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L789) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1137) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1265)

<a id="op-314d4dafc2d192"></a>
### Postgres Database.is type number

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_is_type_number`

**Inputs** code.

**Wrappers, in declaration order** staticmethod.

**Explicit results** code equals psycopg2.NUMBER.

**Local steps**

- Return code equals psycopg2.NUMBER.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L914) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1150) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1276)

<a id="op-e55112b505276b"></a>
### Postgres Database.is type datetime

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_is_type_datetime`

**Inputs** code.

**Wrappers, in declaration order** staticmethod.

**Explicit results** code equals psycopg2.DATETIME.

**Local steps**

- Return code equals psycopg2.DATETIME.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L972) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1149) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1275)

<a id="op-559978c45ef72a"></a>
### Postgres Database.rename table

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_rename_table`

**Inputs** self, old\_name, new\_name.

**Declared result** (list bitwise or tuple).

**Explicit results** self.sql(formatted text ALTER TABLE ′{old\_name}′ RENAME TO ′{new\_name}′).

**Local steps**

- Set old\_name from get\_table\_name(old\_name).
- Set new\_name from get\_table\_name(new\_name).
- Return self.sql(formatted text ALTER TABLE ′{old\_name}′ RENAME TO ′{new\_name}′).

**Methods declared on this owner** [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L1030) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1155) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1280)

<a id="op-968ffc8a5a238e"></a>
### Postgres Database.describe

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_describe`

**Inputs** self, doctype.

**Declared result** (list bitwise or tuple).

**Explicit results** self.sql(formatted text SELECT COLUMN\_NAME FROM information\_schema.COLUMNS WHERE TABLE\_NAME = '{table\_name}' and table\_schema='{Platform.conf.get(“db\_schema”, “public”)}').

**Local steps**

- Set table\_name from get\_table\_name(doctype).
- Return self.sql(formatted text SELECT COLUMN\_NAME FROM information\_schema.COLUMNS WHERE TABLE\_NAME = '{table\_name}' and table\_schema='{Platform.conf.get(“db\_schema”, “public”)}').

**Methods declared on this owner** [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L119) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1134) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1262)

<a id="op-123af13d176173"></a>
### Postgres Database.change column type

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_change_column_type`

**Inputs** self, doctype, column, type, nullable = false, use\_cast = false.

**Declared result** (list bitwise or tuple).

**Explicit results** self.sql\_ddl(formatted text ALTER TABLE "{table\_name}"  ALTER COLUMN "{column}" TYPE {type} {using\_cast},  ALTER COLUMN "{column}" {null\_constraint}).

**Local steps**

- Set table\_name from get\_table\_name(doctype).
- Set null\_constraint from “SET NOT NULL” when not nullable, otherwise “DROP NOT NULL”.
  - Value choice on not nullable — true gives “SET NOT NULL”, false gives “DROP NOT NULL”.
- Set using\_cast from formatted text using "{column}"::{type} when use\_cast, otherwise empty text.
  - Value choice on use\_cast — true gives formatted text using "{column}"::{type}, false gives empty text.
- Return self.sql\_ddl(formatted text ALTER TABLE "{table\_name}"  ALTER COLUMN "{column}" TYPE {type} {using\_cast},  ALTER COLUMN "{column}" {null\_constraint}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L1383) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1125) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1254)

<a id="op-26801135b5dc6a"></a>
### Postgres Database.rename column

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_rename_column`

**Inputs** self, doctype, old\_column\_name, new\_column\_name.

**Local steps**

- Set table\_name from get\_table\_name(doctype).
- Evaluate Platform.db.sql\_ddl(formatted text ALTER TABLE ′{table\_name}′ RENAME COLUMN ′{old\_column\_name}′ TO ′{new\_column\_name}′).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L1719) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1154) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1279)

<a id="op-d05fc55dac7f91"></a>
### Postgres Database.create auth table

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_create_authentication_table`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L1891) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1129) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1257)

<a id="op-462b52100e2c8e"></a>
### Postgres Database.create global search table

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_create_global_search_table`

**Inputs** self.

**Local steps**

- If “\_\_global\_search” does not belong to self.get\_tables().
  - Evaluate self.sql(formatted text create table "\_\_global\_search"(  doctype varchar(100),  name varchar({self.VARCHAR\_LEN}),  title varchar({self.VARCHAR\_LEN}),  content tex).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get tables](operations-025.md#op-65c0b578f98bfc), [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L118) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1130) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1258)

<a id="op-6119fc9a019b6b"></a>
### Postgres Database.create user settings table

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_create_user_settings_table`

**Inputs** self.

**Local steps**

- Evaluate self.sql\_ddl(query text (CREATE)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L2122) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1131) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1259)

<a id="op-ee5763f732c09b"></a>
### Postgres Database.updatedb

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_updatedb`

**Inputs** self, doctype, meta = no value.

**Explicit failure paths** Exception(formatted text Wrong doctype {doctype} in updatedb).

**Local steps**

- Set res from self.sql(formatted text select issingle from ′tabDocType′ where name='{doctype}').
- If not res.
  - Raise Exception(formatted text Wrong doctype {doctype} in updatedb).
- If not res at 0 at 0.
  - Set db\_table from PostgresTable(doctype, meta).
  - Evaluate db\_table.validate().
  - Evaluate db\_table.sync().
  - Evaluate self.commit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L2176) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1162) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1285)

<a id="op-120d25dffde0f9"></a>
### Postgres Database.get on duplicate update

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_get_on_duplicate_update`

**Inputs** key = “name”.

**Wrappers, in declaration order** staticmethod.

**Explicit results** formatted text ON CONFLICT ("{key}") DO UPDATE SET.

**Local steps**

- If isinstance(key, list).
  - Set key from “", "”.join(key).
- Return formatted text ON CONFLICT ("{key}") DO UPDATE SET.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L2481) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1144) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1271)

<a id="op-98dc491d8b69ee"></a>
### Postgres Database.check implicit commit

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_check_implicit_commit`

**Inputs** self, query, query\_type.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L2627) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1126) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1255)

<a id="op-f882e7ccc74d2e"></a>
### Postgres Database.has index

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_has_index`

**Inputs** self, table\_name, index\_name.

**Explicit results** self.sql(query text (SELECT), tuple(table\_name, self.db\_schema, index\_name)).

**Local steps**

- Return self.sql(query text (SELECT), tuple(table\_name, self.db\_schema, index\_name)).

**Methods declared on this owner** [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L2674) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1147) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1274)

<a id="op-0fe16b59172b65"></a>
### Postgres Database.add index

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_add_index`

**Inputs** self, doctype, fields, index\_name = no value.

**Local steps**

- Set table\_name from get\_table\_name(doctype).
- Set index\_name from (index\_name or self.get\_index\_name(fields)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in index\_name → self.get\_index\_name(fields).
- Set fields\_str from “", "”.join(generator of re.sub(“\\(.\*\\)”, empty text, field) for field drawn from fields).
  - Draw field from fields.
- Evaluate self.sql\_ddl(formatted text CREATE INDEX IF NOT EXISTS "{index\_name}" ON "{self.db\_schema}"."{table\_name}" ("{fields\_str}")).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L116) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1120) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1252)

<a id="op-89af495a47f5c7"></a>
### Postgres Database.add unique

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_add_unique`

**Inputs** self, doctype, fields, constraint\_name = no value.

**Local steps**

- If isinstance(fields, str).
  - Set fields from list(fields).
- If not constraint\_name.
  - Set constraint\_name from (“unique\_” + “\_”.join(fields)).
- If not self.sql(query text (SELECT), tuple((“tab” + doctype), self.db\_schema, constraint\_name)).
  - Evaluate self.commit().
  - Evaluate self.sql(nested operand in the contract.SQL(query text (ALTER)).format(schema = sql.Identifier(self.db\_schema), table = sql.Identifier((“tab” + doctype)), constraint = sql.Identifier(constraint\_name), fiel ….
    - Draw field from fields.

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L117) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1121) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1253)

<a id="op-b5313a0653eacd"></a>
### Postgres Database.get table columns description

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_get_table_columns_description`

**Inputs** self, table\_name.

**Explicit results** self.sql(formatted text   SELECT a.column\_name AS name,  CASE LOWER(a.data\_type)  WHEN 'character varying' THEN CONCAT('varchar(', a.character\_maximum\_length ,')')  , as\_dict = 1).

**Local steps**

- Return self.sql(formatted text   SELECT a.column\_name AS name,  CASE LOWER(a.data\_type)  WHEN 'character varying' THEN CONCAT('varchar(', a.character\_maximum\_length ,')')  , as\_dict = 1).

**Methods declared on this owner** [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L122) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1145) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1272)

<a id="op-2ac9f44d47cece"></a>
### Postgres Database.get column type

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_get_column_type`

**Inputs** self, doctype, column.

**Explicit results** nested operand in the contract.select(nested operand in the contract.data\_type).where(((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equal … at 0.

**Local steps**

- Set information\_schema from Platform.qb.Schema(“information\_schema”).
- Set table from get\_table\_name(doctype).
- Return nested operand in the contract.select(nested operand in the contract.data\_type).where(((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equal … at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L6020) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1139) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1266)

<a id="op-85a3f9e8d3c1a1"></a>
### Postgres Database.get database list

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_get_database_list`

**Inputs** self.

**Explicit results** self.sql(query text (SELECT), pluck = true).

**Local steps**

- Return self.sql(query text (SELECT), pluck = true).

**Methods declared on this owner** [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0136.json#L6305) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1141) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1268)

<a id="op-479aec53785487"></a>
### Postgres Database.estimate count

`operation_foundation_database_relational_storage_database_business_behavior_2_relational_database_database_estimate_count`

**Inputs** self, table.

**Declared result** int.

**Explicit results** cint(count at 0 at 0) when count, otherwise 0.

**Local steps**

- Bind dependencies cint.
- Set count from self.sql(query text (SELECT), tuple(table, self.db\_schema)).
- Return cint(count at 0 at 0) when count, otherwise 0.
  - Value choice on count — true gives cint(count at 0 at 0), false gives 0.

**Methods declared on this owner** [sql](operations-025.md#op-9f02be2ab06ad1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L120) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1136) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1264)
