# Record lifecycle and persistence · operations 90

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Schema

<a id="op-65725b2eb34f2f"></a>
### Duck DBTable.get docfields

`operation_foundation_database_duckdb_schema_business_behavior_duck_database_table_get_record_fields`

**Inputs** self.

**Explicit results** fields.

**Local steps**

- Set fields from self.meta.get\_fieldnames\_with\_value(with\_field\_meta = true).
- If not self.meta.get(“istable”).
  - For each fieldname in Platform.db.OPTIONAL\_COLUMNS.
    - Evaluate fields.append(mapping(“fieldname” → fieldname, “fieldtype” → “Text”)).
  - If self.meta.get(“track\_seen”).
    - Evaluate fields.append(mapping(“fieldname” → “\_seen”, “fieldtype” → “Text”)).
- Evaluate fields.append(mapping(“fieldname” → “amended\_from”, “fieldtype” → “Data”)).
- Return fields.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L6116) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1001) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1142)

<a id="op-ada5371937b56f"></a>
### Duck DBTable.get columns from docfields

`operation_foundation_database_duckdb_schema_business_behavior_duck_database_table_get_columns_from_record_fields`

**Inputs** self.

**Local steps**

- For each field in self.\_get\_docfields().
  - If field.get(“is\_virtual”).
    - Continue with the next iteration or loop test.
  - Set self.columns at field.get(“fieldname”) from DuckDBColumn(table = self, fieldname = field.get(“fieldname”), fieldtype = field.get(“fieldtype”), length = field.get(“length”), …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get docfields](operations-090.md#op-65725b2eb34f2f).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L6459) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1000) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1141)

<a id="op-386bded7ad1b91"></a>
### Duck DBTable.get all columns

`operation_foundation_database_duckdb_schema_business_behavior_duck_database_table_get_all_columns`

**Inputs** self.

**Explicit results** columns.

**Local steps**

- Set fields from list(mapping(“fieldname” → “name”, “fieldtype” → “Data”), mapping(“fieldname” → “creation”, “fieldtype” → “Datetime”), mapping(“fieldname” → “modified”, “fieldtype” → “Datetime”), mapping(“fieldname” → “mo ….
- Evaluate fields.extend(self.\_get\_docfields()).
- If self.meta.get(“istable”, default = 0).
  - Evaluate fields.extend(list(mapping(“fieldname” → “parent”, “fieldtype” → “Data”), mapping(“fieldname” → “parentfield”, “fieldtype” → “Data”), mapping(“fieldname” → “parenttype”, “fieldtype” → “Data”))).
- Set columns from OrderedDict().
- For each field in fields.
  - If field.get(“is\_virtual”).
    - Continue with the next iteration or loop test.
  - Set columns at field.get(“fieldname”) from DuckDBColumn(table = self, fieldname = field.get(“fieldname”), fieldtype = field.get(“fieldtype”), length = field.get(“length”), …).
- Return columns.

**Methods declared on this owner** [get docfields](operations-090.md#op-65725b2eb34f2f).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L6875) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L997) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1138)

<a id="op-34f23fa39924a0"></a>
### Duck DBTable.create

`operation_foundation_database_duckdb_schema_business_behavior_duck_database_table_create`

**Inputs** self, conn.

**Local steps**

- Set all\_columns from “,”.join(self.get\_all\_column\_definitions()).
- Set query from formatted text create table "{self.table\_name}" ({all\_columns}).
- Evaluate conn.sql(query).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get all column definitions](operations-089.md#op-8aa644e3032fad).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L995) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1136)

<a id="op-47b9466d411e1a"></a>
### Duck DBTable.get arrow schema

`operation_foundation_database_duckdb_schema_business_behavior_duck_database_table_get_arrow_schema`

**Inputs** self.

**Explicit results** pa.schema(fields).

**Local steps**

- Bind dependencies pa.
- Bind dependencies get\_pyarrow\_type\_map.
- Set arrow\_typemap from get\_pyarrow\_type\_map().
- Set fields from list of tuple(v.fieldname, arrow\_typemap at v.fieldtype) for v drawn from self.get\_all\_columns().values().
  - Draw v from self.get\_all\_columns().values().
- Return pa.schema(fields).

**Methods declared on this owner** [get all columns](operations-090.md#op-386bded7ad1b91).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0132.json#L162) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L998) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1139)

<a id="op-c5ffecf9d1b425"></a>
### Maria DBTable.create

`operation_foundation_database_relational_storage_schema_business_behavior_maria_database_table_create`

**Inputs** self.

**Local steps**

- Set additional\_definitions from list().
- Set engine from (self.meta.get(“engine”) or “InnoDB”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.meta.get(“engine”) → “InnoDB”.
- Set varchar\_len from Platform.db.VARCHAR\_LEN.
- Set name\_column from formatted text name varchar({varchar\_len}) primary key.
- Set column\_defs from self.get\_column\_definitions().
- If column\_defs.
  - Update additional\_definitions using + column\_defs.
- Set index\_defs from self.get\_index\_definitions().
- If index\_defs.
  - Update additional\_definitions using + index\_defs.
- If self.meta.get(“istable”, default = 0).
  - Update additional\_definitions using + list(formatted text parent varchar({varchar\_len}), formatted text parentfield varchar({varchar\_len}), formatted text parenttype varchar({varchar\_len}), “index parent(parent)”).
- Otherwise.
  - Evaluate additional\_definitions.append(“index creation(creation)”).
  - If self.meta.sort\_field equals “modified”.
    - Evaluate additional\_definitions.append(“index modified(modified)”).
- If (not self.meta.issingle and self.meta.autoname equals “autoincrement”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.meta.issingle → self.meta.autoname equals “autoincrement”.
  - Evaluate Platform.db.create\_sequence(self.doctype, check\_not\_exists = true).
  - Set name\_column from “name bigint primary key”.
- Otherwise.
  - If (not self.meta.issingle and self.meta.autoname equals “UUID”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.meta.issingle → self.meta.autoname equals “UUID”.
    - Set name\_column from “name uuid primary key”.
- Set additional\_definitions from “,\\n”.join(additional\_definitions).
- Set query from formatted text create table ′{self.table\_name}′ (  {name\_column},  creation datetime(6),  modified datetime(6),  modified\_by varchar({varchar\_len}),  owner.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.meta.get(“row\_format”) → “Dynamic”.
- Evaluate Platform.db.sql\_ddl(query).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0134.json#L3671) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1300) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1413)

<a id="op-a9b9d19eab4c99"></a>
### Maria DBTable.alter

`operation_foundation_database_relational_storage_schema_business_behavior_maria_database_table_alter`

**Inputs** self.

**Explicit failure paths** propagate active failure.

**Local steps**

- For each col in self.columns.values().
  - Evaluate col.build\_for\_alter\_table(self.current\_columns.get(col.fieldname.lower())).
- Set add\_column\_query from list of formatted text ADD COLUMN ′{col.fieldname}′ {col.get\_definition()} for col drawn from self.add\_column.
  - Draw col from self.add\_column.
- Set columns\_to\_modify from set(((self.change\_type + self.set\_default) + self.change\_nullability)).
- Set modify\_column\_query from list of formatted text MODIFY ′{col.fieldname}′ {col.get\_definition(for\_modification = true)} for col drawn from columns\_to\_modify.
  - Draw col from columns\_to\_modify.
- If alter\_pk bound to self.alter\_primary\_key().
  - Evaluate modify\_column\_query.append(alter\_pk).
- Evaluate modify\_column\_query.extend(list of formatted text ADD UNIQUE INDEX IF NOT EXISTS {col.fieldname} (′{col.fieldname}′) for col drawn from self.add\_unique).
  - Draw col from self.add\_unique.
- Set add\_index\_query from list of formatted text ADD INDEX ′{col.fieldname}\_index′(′{col.fieldname}′) for col drawn from self.add\_index where not Platform.db.get\_column\_index(self.table\_name, col.fieldname, unique = false).
  - Draw col from self.add\_index, keep a combination only if (not Platform.db.get\_column\_index(self.table\_name, col.fieldname, unique = false)).
- If (self.meta.sort\_field equals “modified” and not Platform.db.get\_column\_index(self.table\_name, “modified”, unique = false)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.sort\_field equals “modified” → not Platform.db.get\_column\_index(self.table\_name, “modified”, unique = false).
  - Evaluate add\_index\_query.append(“ADD INDEX ′modified′(′modified′)”).
- Set meta\_columns from set(self.columns.keys()).
- Set db\_columns from set(self.current\_columns.keys()).
- For each col in db\_columns.
  - If (col does not belong to meta\_columns and col does not belong to Platform.db.DEFAULT\_COLUMNS and col does not belong to Platform.db.OPTIONAL\_COLUMNS and not self.current\_columns at col.is\_generated).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in col does not belong to meta\_columns → col does not belong to Platform.db.DEFAULT\_COLUMNS → col does not belong to Platform.db.OPTIONAL\_COLUMNS → not self.current\_columns at col.is\_generated.
    - Set has\_unique from Platform.db.get\_column\_index(self.table\_name, col, unique = true).
    - If not has\_unique.
      - Continue with the next iteration or loop test.
    - Set current\_col from self.current\_columns.get(col).
    - Set deleted\_col from DbColumn(table = self, fieldname = current\_col.name, fieldtype = current\_col.type, length = no value, …).
    - Evaluate self.drop\_unique.append(deleted\_col).
- Set drop\_index\_query from list().
- For each col in set(expanded self.drop\_index, expanded self.drop\_unique).
  - If col.fieldname equals “name”.
    - Continue with the next iteration or loop test.
  - Set current\_column from self.current\_columns.get(col.fieldname.lower()).
  - Set unique\_constraint\_changed from current\_column.unique differs from col.unique.
  - If (unique\_constraint\_changed and not col.unique).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in unique\_constraint\_changed → not col.unique.
    - If unique\_index bound to Platform.db.get\_column\_index(self.table\_name, col.fieldname, unique = true).
      - Evaluate drop\_index\_query.append(formatted text DROP INDEX ′{unique\_index.Key\_name}′).
  - Set index\_constraint\_changed from current\_column.index differs from col.set\_index.
  - If (index\_constraint\_changed and not col.set\_index).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in index\_constraint\_changed → not col.set\_index.
    - If index\_record bound to Platform.db.get\_column\_index(self.table\_name, col.fieldname, unique = false).
      - Evaluate drop\_index\_query.append(formatted text DROP INDEX ′{index\_record.Key\_name}′).
- Set drop\_index\_query from list(dict.fromkeys(drop\_index\_query)).
- For each col in self.change\_nullability.
  - If col.not\_nullable.
    - Attempt the following.
      - Set table from Platform.qb.DocType(self.doctype).
      - Evaluate nested operand in the contract(nested operand in the contract).set(col.fieldname, (nested operand in the contract.default or nested operand in the contract(nested operand in the contract))).where(table at  ….run().
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.default → get\_not\_null\_defaults(col.fieldtype).
    - On failure (Exception).
      - Evaluate print(formatted text Failed to update data in {self.table\_name} for {col.fieldname}).
      - Propagate the active failure.
- Evaluate self.run\_alter(add\_column\_query).
- Evaluate self.run\_alter(drop\_index\_query).
- Evaluate self.run\_alter(modify\_column\_query).
- Evaluate self.run\_alter(add\_index\_query).

If control reaches the end, it returns no value.

**Methods declared on this owner** [alter primary key](operations-090.md#op-42f5fc0dd146f5), [run alter](operations-090.md#op-ff3cfc79d0ece2).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L4) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1298) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1411)

<a id="op-ff3cfc79d0ece2"></a>
### Maria DBTable.run alter

`operation_foundation_database_relational_storage_schema_business_behavior_maria_database_table_run_alter`

**Inputs** self, query\_parts, coerce\_blanks = true.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} field cannot be set as unique in {1}, as there are non-unique existing values”.format(fieldname, self.table\_name) · validation helper — translated “Cannot change field type in {0}: some existing values cannot be converted to the new type”.format(self.doctype) · propagate active failure.

**Local steps**

- If not query\_parts.
  - Return no value.
- Set query from formatted text ALTER TABLE ′{self.table\_name}′ {“, ”.join(query\_parts)}.
- Attempt the following.
  - Evaluate Platform.db.sql\_ddl(query).
- On failure (Exception) bound to e.
  - Evaluate print(formatted text Failed to alter schema using query: {query}).
  - If Platform.db.is\_duplicate\_entry(e).
    - Set fieldname from str(e).split(“'”) at negative 2.
    - Call the validation error handler Platform.throw(translated “{0} field cannot be set as unique in {1}, as there are non-unique existing values”.format(fieldname, self.table\_name)).
  - If Platform.db.is\_data\_truncated(e).
    - If (Platform.flags.in\_migrate and coerce\_blanks and self.set\_blank\_values\_to\_default()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.in\_migrate → coerce\_blanks → self.set\_blank\_values\_to\_default().
      - Evaluate self.run\_alter(query\_parts, coerce\_blanks = false).
      - Return no value.
    - Call the validation error handler Platform.throw(translated “Cannot change field type in {0}: some existing values cannot be converted to the new type”.format(self.doctype), title = translated “Incompatible Values”).
  - Propagate the active failure.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set blank values to default](operations-090.md#op-e06bab2636361c).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0134.json#L6567) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1301) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1414)

<a id="op-e06bab2636361c"></a>
### Maria DBTable.set blank values to default

`operation_foundation_database_relational_storage_schema_business_behavior_maria_database_table_set_blank_values_to_default`

**Inputs** self.

**Declared result** bool.

**Explicit results** updated.

**Local steps**

- Set updated from false.
- For each col in self.change\_type.
  - If col.fieldtype does not belong to Platform.model.numeric\_fieldtypes.
    - Continue with the next iteration or loop test.
  - Set current\_column from self.current\_columns.get(col.fieldname.lower()).
  - If (not current\_column or not current\_column.type.startswith(tuple(“varchar”, “char”, “text”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not current\_column → not current\_column.type.startswith(tuple(“varchar”, “char”, “text”)).
    - Continue with the next iteration or loop test.
  - Set table from Platform.qb.DocType(self.doctype).
  - Set field from table at col.fieldname.
  - Set is\_blank from Trim(field) equals empty text.
  - If not nested operand in the contract.where(is\_blank).limit(1).run().
    - Continue with the next iteration or loop test.
  - Evaluate nested operand in the contract(nested operand in the contract).set(col.fieldname, (nested operand in the contract.default or nested operand in the contract(nested operand in the contract))).where(is\_blank).run().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.default → get\_not\_null\_defaults(col.fieldtype).
  - Set updated from true.
- Return updated.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0134.json#L7156) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1302) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1415)

<a id="op-42f5fc0dd146f5"></a>
### Maria DBTable.alter primary key

`operation_foundation_database_relational_storage_schema_business_behavior_maria_database_table_alter_primary_key`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Record and data access** read self.doctype via get\_value.

**Explicit results** “modify name uuid” · formatted text modify name varchar({Platform.db.VARCHAR\_LEN}).

**Explicit failure paths** validation helper — translated “Primary key of doctype {0} can not be changed as there are existing values.”.format(self.doctype).

**Local steps**

- Set autoname from self.meta.autoname.
- If (autoname equals “UUID” and Platform.db.get\_column\_type(self.doctype, “name”) differs from “uuid”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in autoname equals “UUID” → Platform.db.get\_column\_type(self.doctype, “name”) differs from “uuid”.
  - If not Platform.db.get\_value(self.doctype, mapping(), order\_by = no value).
    - Return “modify name uuid”.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Primary key of doctype {0} can not be changed as there are existing values.”.format(self.doctype)).
- If (autoname differs from “UUID” and Platform.db.get\_column\_type(self.doctype, “name”) equals “uuid”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in autoname differs from “UUID” → Platform.db.get\_column\_type(self.doctype, “name”) equals “uuid”.
  - Return formatted text modify name varchar({Platform.db.VARCHAR\_LEN}).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0134.json#L7693) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1299) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1412)

<a id="op-2c7e2c6531e0bd"></a>
### Postgres Table.create

`operation_foundation_database_relational_storage_schema_business_behavior_2_relational_database_table_create`

**Inputs** self.

**State and service calls** execute a supplied database query · commit.

**Local steps**

- Set varchar\_len from Platform.db.VARCHAR\_LEN.
- Set name\_column from formatted text name varchar({varchar\_len}) primary key.
- Set additional\_definitions from empty text.
- Set column\_defs from self.get\_column\_definitions().
- If column\_defs.
  - Update additional\_definitions using + “,\\n”.join(column\_defs).
- If self.meta.get(“istable”, default = 0).
  - If column\_defs.
    - Update additional\_definitions using + “,\\n”.
  - Update additional\_definitions using + “,\\n”.join(tuple(formatted text parent varchar({varchar\_len}), formatted text parentfield varchar({varchar\_len}), formatted text parenttype varchar({varchar\_len}))).
- If (not self.meta.issingle and self.meta.autoname equals “autoincrement”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.meta.issingle → self.meta.autoname equals “autoincrement”.
  - Evaluate Platform.db.create\_sequence(self.doctype, check\_not\_exists = true).
  - Set name\_column from “name bigint primary key”.
- Otherwise.
  - If (not self.meta.issingle and self.meta.autoname equals “UUID”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.meta.issingle → self.meta.autoname equals “UUID”.
    - Set name\_column from “name uuid primary key”.
- Evaluate Platform.db.sql(formatted text create table ′{self.table\_name}′ (  {name\_column},  creation timestamp(6),  modified timestamp(6),  modified\_by varchar({varchar\_len}),  own).
- Evaluate self.create\_indexes().
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create indexes](operations-090.md#op-b3846d4834452c).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0137.json#L3388) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1296) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1409)

<a id="op-b3846d4834452c"></a>
### Postgres Table.create indexes

`operation_foundation_database_relational_storage_schema_business_behavior_2_relational_database_table_create_indexes`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Local steps**

- Set create\_index\_query from empty text.
- For each col in self.columns.values().
  - If (col.set\_index and col.fieldtype belongs to Platform.db.type\_map and nested operand in the contract.db.type\_map.get(col.fieldtype) at 0 does not belong to tuple(“text”, “longtext”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.set\_index → col.fieldtype belongs to Platform.db.type\_map → Platform.db.type\_map.get(col.fieldtype) at 0 does not belong to tuple(“text”, “longtext”).
    - Update create\_index\_query using + formatted text CREATE INDEX IF NOT EXISTS "{col.fieldname}" ON ′{self.table\_name}′(′{col.fieldname}′);.
- If create\_index\_query.
  - Evaluate Platform.db.sql(create\_index\_query).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L3) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1297) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1410)

<a id="op-447e7698ecf298"></a>
### Postgres Table.alter

`operation_foundation_database_relational_storage_schema_business_behavior_2_relational_database_table_alter`

**Inputs** self.

**Record and data access** execute query text (SELECT).

**State and service calls** execute a supplied database query.

**Explicit failure paths** propagate active failure · validation helper — str(e) · validation helper — translated “{0} field cannot be set as unique in {1}, as there are non-unique existing values”.format(fieldname, self.table\_name) · e.

**Local steps**

- For each col in self.columns.values().
  - Evaluate col.build\_for\_alter\_table(self.current\_columns.get(col.fieldname.lower())).
- Set query from list of formatted text ADD COLUMN ′{col.fieldname}′ {col.get\_definition()} for col drawn from self.add\_column.
  - Draw col from self.add\_column.
- Set new\_column\_names from set of col.fieldname for col drawn from self.add\_column.
  - Draw col from self.add\_column.
- For each col in self.change\_type.
  - Set using\_clause from empty text.
  - If col.fieldtype belongs to “Datetime”.
    - Set using\_clause from formatted text USING {col.fieldname}::timestamp without time zone.
  - Otherwise.
    - If col.fieldtype equals “Check”.
      - Set using\_clause from formatted text USING {col.fieldname}::smallint.
  - Evaluate query.append(“ALTER COLUMN ′{}′ TYPE {} {}”.format(col.fieldname, get\_definition(col.fieldtype, precision = col.precision, length = col.length), using\_clause)).
- If alter\_pk bound to self.alter\_primary\_key().
  - Evaluate query.append(alter\_pk).
- For each col in self.set\_default.
  - If col.fieldname equals “name”.
    - Continue with the next iteration or loop test.
  - If col.fieldtype belongs to tuple(“Check”, “Int”).
    - Set col\_default from cint(col.default).
  - Otherwise.
    - If col.fieldtype belongs to tuple(“Currency”, “Float”, “Percent”).
      - Set col\_default from flt(col.default).
    - Otherwise.
      - If not col.default.
        - Set col\_default from “NULL”.
      - Otherwise.
        - Set col\_default from formatted text {Platform.db.escape(col.default)}.
  - Evaluate query.append(formatted text ALTER COLUMN ′{col.fieldname}′ SET DEFAULT {col\_default}).
- Set create\_contraint\_query from empty text.
- For each col in self.add\_index.
  - Update create\_contraint\_query using + formatted text CREATE INDEX IF NOT EXISTS "{col.fieldname}" ON ′{self.table\_name}′(′{col.fieldname}′);.
- For each col in self.add\_unique.
  - If col.fieldname does not belong to new\_column\_names.
    - Update create\_contraint\_query using + “CREATE UNIQUE INDEX IF NOT EXISTS "unique\_{index\_name}" ON ′{table\_name}′(′{field}′);”.format(index\_name = col.fieldname, table\_name = self.table\_name, field = col.fieldname).
- Set meta\_columns from set(self.columns.keys()).
- Set db\_columns from set(self.current\_columns.keys()).
- For each col in db\_columns.
  - If (col does not belong to meta\_columns and col does not belong to Platform.db.DEFAULT\_COLUMNS and col does not belong to Platform.db.OPTIONAL\_COLUMNS).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in col does not belong to meta\_columns → col does not belong to Platform.db.DEFAULT\_COLUMNS → col does not belong to Platform.db.OPTIONAL\_COLUMNS.
    - Set has\_unique\_index from Platform.db.sql(query text (SELECT), tuple(self.table\_name, formatted text {self.table\_name}\_{col}\_key, formatted text unique\_{col})).
    - If not has\_unique\_index.
      - Continue with the next iteration or loop test.
    - Set current\_col from self.current\_columns.get(col).
    - Set deleted\_col from DbColumn(table = self, fieldname = current\_col.name, fieldtype = current\_col.type, length = no value, …).
    - Evaluate self.drop\_unique.append(deleted\_col).
- Set drop\_contraint\_query from empty text.
- For each col in self.drop\_index.
  - If col.fieldname differs from “name”.
    - Update drop\_contraint\_query using + formatted text DROP INDEX IF EXISTS "{col.fieldname}" ;.
- For each col in self.drop\_unique.
  - If col.fieldname differs from “name”.
    - Set unique\_constraint\_exists from Platform.db.sql(query text (SELECT), tuple(formatted text {self.table\_name}\_{col.fieldname}\_key)).
    - If unique\_constraint\_exists.
      - Update drop\_contraint\_query using + formatted text ALTER TABLE "{self.table\_name}" DROP CONSTRAINT IF EXISTS "{self.table\_name}\_{col.fieldname}\_key" ;.
    - Set unique\_index\_exists from Platform.db.sql(query text (SELECT), tuple(self.table\_name, formatted text unique\_{col.fieldname})).
    - If unique\_index\_exists.
      - Update drop\_contraint\_query using + formatted text DROP INDEX IF EXISTS "unique\_{col.fieldname}" ;.
- Set change\_nullability from list().
- For each col in self.change\_nullability.
  - Set default from (col.default or get\_not\_null\_defaults(col.fieldtype)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.default → get\_not\_null\_defaults(col.fieldtype).
  - If isinstance(default, str).
    - Set default from Platform.db.escape(default).
  - Evaluate change\_nullability.append(formatted text ALTER COLUMN "{col.fieldname}" {“SET” when col.not\_nullable, otherwise “DROP”} NOT NULL).
    - Value choice on col.not\_nullable — true gives “SET”, false gives “DROP”.
  - Evaluate change\_nullability.append(formatted text ALTER COLUMN "{col.fieldname}" SET DEFAULT {default}).
  - If col.not\_nullable.
    - Attempt the following.
      - Set table from Platform.qb.DocType(self.doctype).
      - Evaluate nested operand in the contract(nested operand in the contract).set(col.fieldname, (nested operand in the contract.default or nested operand in the contract(nested operand in the contract))).where(table at  ….run().
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.default → get\_not\_null\_defaults(col.fieldtype).
    - On failure (Exception).
      - Evaluate print(formatted text Failed to update data in {self.table\_name} for {col.fieldname}).
      - Propagate the active failure.
- Attempt the following.
  - If query.
    - Set final\_alter\_query from query text (ALTER).format(self.table\_name, “, ”.join(query)).
    - Evaluate Platform.db.sql(final\_alter\_query).
  - If change\_nullability.
    - Evaluate Platform.db.sql(formatted text ALTER TABLE ′{self.table\_name}′ {“,”.join(change\_nullability)}).
  - If create\_contraint\_query.
    - Evaluate Platform.db.sql(create\_contraint\_query).
  - If drop\_contraint\_query.
    - Evaluate Platform.db.sql(drop\_contraint\_query).
- On failure (Exception) bound to e.
  - If Platform.db.is\_duplicate\_fieldname(e).
    - Call the validation error handler Platform.throw(str(e)).
  - Otherwise.
    - If Platform.db.is\_duplicate\_entry(e).
      - Set fieldname from str(e).split(“'”) at negative 2.
      - Call the validation error handler Platform.throw(translated “{0} field cannot be set as unique in {1}, as there are non-unique existing values”.format(fieldname, self.table\_name)).
    - Otherwise.
      - Raise e.

If control reaches the end, it returns no value.

**Methods declared on this owner** [alter primary key](operations-090.md#op-d4e51841f8de45).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L2) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1294) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1407)

<a id="op-d4e51841f8de45"></a>
### Postgres Table.alter primary key

`operation_foundation_database_relational_storage_schema_business_behavior_2_relational_database_table_alter_primary_key`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Record and data access** read self.doctype via get\_value.

**Explicit results** “alter column ′name′ TYPE uuid USING name::uuid” · formatted text alter column ′name′ TYPE varchar({Platform.db.VARCHAR\_LEN}).

**Explicit failure paths** validation helper — translated “Primary key of doctype {0} can not be changed as there are existing values.”.format(self.doctype).

**Local steps**

- Set autoname from self.meta.autoname.
- If (autoname equals “UUID” and Platform.db.get\_column\_type(self.doctype, “name”) differs from “uuid”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in autoname equals “UUID” → Platform.db.get\_column\_type(self.doctype, “name”) differs from “uuid”.
  - If not Platform.db.get\_value(self.doctype, mapping(), order\_by = no value).
    - Return “alter column ′name′ TYPE uuid USING name::uuid”.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Primary key of doctype {0} can not be changed as there are existing values.”.format(self.doctype)).
- If (autoname differs from “UUID” and Platform.db.get\_column\_type(self.doctype, “name”) equals “uuid”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in autoname differs from “UUID” → Platform.db.get\_column\_type(self.doctype, “name”) equals “uuid”.
  - Return formatted text alter column ′name′ TYPE varchar({Platform.db.VARCHAR\_LEN}).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0138.json#L4328) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1295) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1408)

<a id="op-0246181e8bcfce"></a>
### DBTable.initialize

`operation_foundation_database_schema_business_behavior_database_table_initialize`

**Inputs** self, doctype, meta = no value.

**Local steps**

- Set self.doctype from doctype.
- Set self.table\_name from formatted text tab{doctype}.
- Set self.meta from (meta or Platform.get\_meta(doctype, false)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta → Platform.get\_meta(doctype, false).
- Set self.columns from mapping().
- Set self.current\_columns from mapping().
- Set self.add\_column from list().
- Set self.change\_type from list().
- Set self.change\_name from list().
- Set self.change\_nullability from list().
- Set self.add\_unique from list().
- Set self.add\_index from list().
- Set self.drop\_unique from list().
- Set self.drop\_index from list().
- Set self.set\_default from list().
- Evaluate self.get\_columns\_from\_docfields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get columns from docfields](operations-090.md#op-7779c04f83de15).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L6804) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1331) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1442)

<a id="op-955d3a672a6552"></a>
### DBTable.sync

`operation_foundation_database_schema_business_behavior_database_table_sync`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.meta.get(“is\_virtual”).
  - Return no value.
- If self.is\_new().
  - Evaluate self.create().
- Otherwise.
  - Evaluate Platform.client\_cache.delete\_value(formatted text table\_columns::{self.table\_name}).
  - Evaluate self.alter().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is new](operations-090.md#op-78d95086a91612), [create](operations-090.md#op-d6563b2c25508a), [alter](operations-090.md#op-6adab5ed7d091c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L7157) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1334) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1445)

<a id="op-d6563b2c25508a"></a>
### DBTable.create

`operation_foundation_database_schema_business_behavior_database_table_create`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0144.json#L7341) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1327) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1438)

<a id="op-42c88092714eda"></a>
### DBTable.get column definitions

`operation_foundation_database_schema_business_behavior_database_table_get_column_definitions`

**Inputs** self.

**Explicit results** ret.

**Local steps**

- Set column\_list from list(expanded Platform.db.DEFAULT\_COLUMNS).
- Set ret from list().
- For each k in list(self.columns).
  - If k does not belong to column\_list.
    - Set d from self.columns at k.get\_definition().
    - If d.
      - Evaluate ret.append((((“′” + k) + “′ ”) + d)).
      - Evaluate column\_list.append(k).
- Return ret.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1328) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1439)

<a id="op-56a3dd2d78988f"></a>
### DBTable.get index definitions

`operation_foundation_database_schema_business_behavior_database_table_get_index_definitions`

**Inputs** self.

**Explicit results** list of ((((“index ′” + key) + “′(′”) + key) + “′)”) for tuple(key, col) drawn from self.columns.items() where (col.set\_index and not col.unique and col.fieldtype belongs to Platform.db.type\_map and nested ….

**Local steps**

- Return list of ((((“index ′” + key) + “′(′”) + key) + “′)”) for tuple(key, col) drawn from self.columns.items() where (col.set\_index and not col.unique and col.fieldtype belongs to Platform.db.type\_map and nested ….
  - Draw tuple(key, col) from self.columns.items(), keep a combination only if ((col.set\_index and not col.unique and col.fieldtype belongs to Platform.db.type\_map and nested operand in the contract.db.type\_map.get(col.fieldtype) at 0 does not belong to tuple(“text”, “longtext”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.set\_index → not col.unique → col.fieldtype belongs to Platform.db.type\_map → Platform.db.type\_map.get(col.fieldtype) at 0 does not belong to tuple(“text”, “longtext”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L254) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1330) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1441)

<a id="op-7779c04f83de15"></a>
### DBTable.get columns from docfields

`operation_foundation_database_schema_business_behavior_database_table_get_columns_from_record_fields`

**Inputs** self.

**Local steps**

- Set fields from self.meta.get\_fieldnames\_with\_value(with\_field\_meta = true).
- If not self.meta.get(“istable”).
  - For each fieldname in Platform.db.OPTIONAL\_COLUMNS.
    - Evaluate fields.append(mapping(“fieldname” → fieldname, “fieldtype” → “Text”)).
  - If self.meta.get(“track\_seen”).
    - Evaluate fields.append(mapping(“fieldname” → “\_seen”, “fieldtype” → “Text”)).
- For each field in fields.
  - If field.get(“is\_virtual”).
    - Continue with the next iteration or loop test.
  - Set self.columns at field.get(“fieldname”) from DbColumn(table = self, fieldname = field.get(“fieldname”), fieldtype = field.get(“fieldtype”), length = field.get(“length”), …).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L481) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1329) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1440)

<a id="op-df0a04f96fb3bf"></a>
### DBTable.validate

`operation_foundation_database_schema_business_behavior_database_table_validate`

**Inputs** self.

**State and service calls** execute a supplied database query · msgprint with info\_message.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Fieldname is limited to 64 characters ({0})”.format(Platform.bold(col.fieldname)) · validation helper — translated “Length of {0} should be between 1 and 1000”.format(col.fieldname) · propagate active failure.

**Local steps**

- If self.is\_new().
  - Return no value.
- Evaluate self.setup\_table\_columns().
- Set columns from list of Platform.\_dict(mapping(“fieldname” → f, “fieldtype” → “Data”)) for f drawn from Platform.db.STANDARD\_VARCHAR\_COLUMNS.
  - Draw f from Platform.db.STANDARD\_VARCHAR\_COLUMNS.
- If self.meta.get(“istable”).
  - Update columns using + list of Platform.\_dict(mapping(“fieldname” → f, “fieldtype” → “Data”)) for f drawn from Platform.db.CHILD\_TABLE\_COLUMNS.
    - Draw f from Platform.db.CHILD\_TABLE\_COLUMNS.
- Update columns using + self.columns.values().
- For each col in columns.
  - If len(col.fieldname) ≥ 64.
    - Call the validation error handler Platform.throw(translated “Fieldname is limited to 64 characters ({0})”.format(Platform.bold(col.fieldname))).
  - If “varchar” belongs to Platform.db.type\_map.get(col.fieldtype, tuple()).
    - Set new\_length from (cint(col.length) or cint(Platform.db.VARCHAR\_LEN)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(col.length) → cint(Platform.db.VARCHAR\_LEN).
    - If not 1 ≤ new\_length ≤ 1000.
      - Compare adjacent operands in order, stopping at the first false comparison in 1 ≤ new\_length ≤ 1000.
      - Call the validation error handler Platform.throw(translated “Length of {0} should be between 1 and 1000”.format(col.fieldname)).
    - Set current\_col from self.current\_columns.get(col.fieldname, mapping()).
    - If not current\_col.
      - Continue with the next iteration or loop test.
    - Set current\_type from self.current\_columns at col.fieldname at “type”.
    - Set current\_length from VARCHAR\_CAST\_PATTERN.findall(current\_type).
    - If not current\_length.
      - Continue with the next iteration or loop test.
    - Set current\_length from current\_length at 0.
    - If cint(current\_length) &gt; cint(new\_length).
      - Attempt the following.
        - Set max\_length from Platform.db.sql(formatted text SELECT MAX(CHAR\_LENGTH(′{col.fieldname}′)) FROM ′tab{self.doctype}′).
      - On failure (Platform.db.InternalError) bound to e.
        - If Platform.db.is\_missing\_column(e).
          - Continue with the next iteration or loop test.
        - Propagate the active failure.
      - If (max\_length and max\_length at 0 at 0 and max\_length at 0 at 0 &gt; new\_length).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_length → max\_length at 0 at 0 → max\_length at 0 at 0 &gt; new\_length.
        - If col.fieldname belongs to self.columns.
          - Set self.columns at col.fieldname.length from current\_length.
        - Set info\_message from translated “Reverting length to {0} for '{1}' in '{2}'. Setting the length as {3} will cause truncation of data.”.format(current\_length, col.fieldname, self.doctype, new\_length).
        - Evaluate Platform.msgprint(info\_message).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is new](operations-090.md#op-78d95086a91612), [setup table columns](operations-090.md#op-acad03e5a31ea3).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L1128) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1335) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1446)

<a id="op-78d95086a91612"></a>
### DBTable.is new

`operation_foundation_database_schema_business_behavior_database_table_is_new`

**Inputs** self.

**Explicit results** self.table\_name does not belong to Platform.db.get\_tables().

**Local steps**

- Return self.table\_name does not belong to Platform.db.get\_tables().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L2352) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1332) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1443)

<a id="op-acad03e5a31ea3"></a>
### DBTable.setup table columns

`operation_foundation_database_schema_business_behavior_database_table_setup_table_columns`

**Inputs** self.

**Local steps**

- For each c in Platform.db.get\_table\_columns\_description(self.table\_name).
  - Set self.current\_columns at c.name.lower() from c.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L2421) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1333) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1444)

<a id="op-6adab5ed7d091c"></a>
### DBTable.alter

`operation_foundation_database_schema_business_behavior_database_table_alter`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L2532) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1326) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1437)
