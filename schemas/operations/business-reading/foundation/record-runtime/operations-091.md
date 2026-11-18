# Record lifecycle and persistence · operations 91

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Schema

<a id="op-46411757c99817"></a>
### Db Column.initialize

`operation_foundation_database_schema_business_behavior_database_column_initialize`

**Inputs** self, table (named only), fieldname (named only), fieldtype (named only), length (named only), default (named only), set\_index (named only), options (named only), unique (named only), precision (named only), not\_nullable (named only).

**Local steps**

- Set self.table from table.
- Set self.fieldname from fieldname.
- Set self.fieldtype from fieldtype.
- Set self.length from length.
- Set self.set\_index from set\_index.
- Set self.default from default.
- Set self.options from options.
- Set self.unique from unique.
- Set self.precision from precision.
- Set self.not\_nullable from not\_nullable.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L2565) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1325) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1436)

<a id="op-d3727e2876dd08"></a>
### Db Column.get definition

`operation_foundation_database_schema_business_behavior_database_column_get_definition`

**Inputs** self, for\_modification = false.

**Explicit results** column\_def.

**Local steps**

- Set column\_def from get\_definition(self.fieldtype, precision = self.precision, length = self.length, options = self.options).
- If not column\_def.
  - Return column\_def.
- Set null from true.
- Set default from no value.
- Set unique from false.
- If self.fieldtype belongs to NOT\_NULL\_TYPES.
  - Set null from false.
- If self.fieldtype belongs to tuple(“Check”, “Int”).
  - Set default from cint(self.default).
- Otherwise.
  - If self.fieldtype belongs to tuple(“Currency”, “Float”, “Percent”).
    - Set default from flt(self.default).
  - Otherwise.
    - If (self.default and self.default does not belong to Platform.db.DEFAULT\_SHORTCUTS and not cstr(self.default).startswith(“:”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.default → self.default does not belong to Platform.db.DEFAULT\_SHORTCUTS → not cstr(self.default).startswith(“:”).
      - Set default from Platform.db.escape(self.default).
- If (self.not\_nullable and null).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.not\_nullable → null.
  - If default is identical to no value.
    - Set default from get\_not\_null\_defaults(self.fieldtype).
    - If isinstance(default, str).
      - Set default from Platform.db.escape(default).
  - Set null from false.
- If (self.unique and not for\_modification and column\_def does not belong to tuple(“text”, “longtext”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.unique → not for\_modification → column\_def does not belong to tuple(“text”, “longtext”).
  - Set unique from true.
- If not null.
  - Update column\_def using + “ NOT NULL”.
- If default is distinct from no value.
  - Update column\_def using + formatted text  DEFAULT {default}.
- If unique.
  - Update column\_def using + “ UNIQUE”.
- Return column\_def.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L2835) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1324) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1435)

<a id="op-fa8742e3a4bc0e"></a>
### Db Column.build for alter table

`operation_foundation_database_schema_business_behavior_database_column_build_for_alter_table`

**Inputs** self, current\_def.

**Explicit results** no value.

**Local steps**

- Set column\_type from get\_definition(self.fieldtype, self.precision, self.length).
- If not column\_type.
  - Return no value.
- If not current\_def.
  - Set self.fieldname from validate\_column\_name(self.fieldname).
  - Evaluate self.table.add\_column.append(self).
  - If column\_type does not belong to tuple(“text”, “longtext”).
    - If self.unique.
      - Evaluate self.table.add\_unique.append(self).
    - If self.set\_index.
      - Evaluate self.table.add\_index.append(self).
  - Return no value.
- If (current\_def at “type” differs from column\_type and not (current\_def at “type” equals “longtext” and column\_type equals “json” and Platform.db.db\_type equals “mariadb”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_def at “type” differs from column\_type → not (current\_def at “type” equals “longtext” and column\_type equals “json” and Platform.db.db\_type equals “mariadb”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_def at “type” equals “longtext” → column\_type equals “json” → Platform.db.db\_type equals “mariadb”.
  - Evaluate self.table.change\_type.append(self).
- If ((self.unique and not current\_def.get(“unique”)) and column\_type does not belong to tuple(“text”, “longtext”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.unique and not current\_def.get(“unique”)) → column\_type does not belong to tuple(“text”, “longtext”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.unique → not current\_def.get(“unique”).
  - Evaluate self.table.add\_unique.append(self).
- Otherwise.
  - If ((current\_def.get(“unique”) and not self.unique) and column\_type does not belong to tuple(“text”, “longtext”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (current\_def.get(“unique”) and not self.unique) → column\_type does not belong to tuple(“text”, “longtext”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_def.get(“unique”) → not self.unique.
    - Evaluate self.table.drop\_unique.append(self).
- If (self.default\_changed(current\_def) and self.default does not belong to Platform.db.DEFAULT\_SHORTCUTS and not cstr(self.default).startswith(“:”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.default\_changed(current\_def) → self.default does not belong to Platform.db.DEFAULT\_SHORTCUTS → not cstr(self.default).startswith(“:”).
  - Evaluate self.table.set\_default.append(self).
- If (self.not\_nullable is distinct from no value and self.not\_nullable differs from current\_def.get(“not\_nullable”) and self.fieldtype does not belong to NOT\_NULL\_TYPES).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.not\_nullable is distinct from no value → self.not\_nullable differs from current\_def.get(“not\_nullable”) → self.fieldtype does not belong to NOT\_NULL\_TYPES.
  - Evaluate self.table.change\_nullability.append(self).
- If ((current\_def.get(“index”) and not self.set\_index) and column\_type does not belong to tuple(“text”, “longtext”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (current\_def.get(“index”) and not self.set\_index) → column\_type does not belong to tuple(“text”, “longtext”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_def.get(“index”) → not self.set\_index.
  - Evaluate self.table.drop\_index.append(self).
- Otherwise.
  - If ((not current\_def.get(“index”) and self.set\_index) and column\_type does not belong to tuple(“text”, “longtext”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not current\_def.get(“index”) and self.set\_index) → column\_type does not belong to tuple(“text”, “longtext”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not current\_def.get(“index”) → self.set\_index.
    - Evaluate self.table.add\_index.append(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [default changed](operations-091.md#op-e2c77af01de490).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L3635) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1319) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1430)

<a id="op-e2c77af01de490"></a>
### Db Column.default changed

`operation_foundation_database_schema_business_behavior_database_column_default_changed`

**Inputs** self, current\_def.

**Explicit results** self.default\_changed\_for\_decimal(current\_def) · self.default\_changed\_for\_time(cur\_default, new\_default) · cur\_default differs from new\_default.

**Local steps**

- If “decimal” belongs to current\_def at “type”.
  - Return self.default\_changed\_for\_decimal(current\_def).
- Otherwise.
  - Set cur\_default from current\_def.get(“default”).
  - Set new\_default from self.default.
  - If (cur\_default equals “NULL” or cur\_default is identical to no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cur\_default equals “NULL” → cur\_default is identical to no value.
    - Set cur\_default from no value.
  - Otherwise.
    - Set cur\_default from cur\_default.lstrip(“'”).rstrip(“'”).replace(“\\\\”, “\\”).
  - Set fieldtype from self.fieldtype.
  - Set db\_field\_type from Platform.db.type\_map.get(fieldtype).
  - If fieldtype belongs to list(“Int”, “Check”).
    - Set cur\_default from cint(cur\_default).
    - Set new\_default from cint(new\_default).
  - Otherwise.
    - If fieldtype belongs to list(“Currency”, “Float”, “Percent”).
      - Set cur\_default from flt(cur\_default).
      - Set new\_default from flt(new\_default).
    - Otherwise.
      - If fieldtype equals “Time”.
        - Return self.default\_changed\_for\_time(cur\_default, new\_default).
      - Otherwise.
        - If (db\_field\_type and db\_field\_type at 0 belongs to tuple(“varchar”, “longtext”, “text”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in db\_field\_type → db\_field\_type at 0 belongs to tuple(“varchar”, “longtext”, “text”).
          - Set new\_default from cstr(new\_default).
          - If not current\_def.get(“not\_nullable”).
            - Set cur\_default from cstr(cur\_default).
  - Return cur\_default differs from new\_default.

**Methods declared on this owner** [default changed for decimal](operations-091.md#op-5980d2a8452b18), [default changed for time](operations-091.md#op-a11079a0757be8).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L4800) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1320) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1431)

<a id="op-5980d2a8452b18"></a>
### Db Column.default changed for decimal

`operation_foundation_database_schema_business_behavior_database_column_default_changed_for_decimal`

**Inputs** self, current\_def.

**Explicit results** false · true · float(cur\_default) differs from float(self.default).

**Local steps**

- Set cur\_default from current\_def at “default”.
- If cur\_default equals “NULL”.
  - Set cur\_default from no value.
- Attempt the following.
  - If (cur\_default belongs to tuple(empty text, no value) and self.default belongs to tuple(empty text, no value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cur\_default belongs to tuple(empty text, no value) → self.default belongs to tuple(empty text, no value).
    - Return false.
  - Otherwise.
    - If (flt(cur\_default) equals 0.0 and flt(self.default) equals 0.0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(cur\_default) equals 0.0 → flt(self.default) equals 0.0.
      - Return false.
    - Otherwise.
      - If cur\_default belongs to tuple(empty text, no value).
        - Attempt the following.
          - Evaluate float(self.default).
          - Return true.
        - On failure (ValueError).
          - Return false.
      - Otherwise.
        - If self.default belongs to tuple(empty text, no value).
          - Return true.
        - Otherwise.
          - Return float(cur\_default) differs from float(self.default).
- On failure (TypeError).
  - Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L5510) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1321) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1432)

<a id="op-a11079a0757be8"></a>
### Db Column.default changed for time

`operation_foundation_database_schema_business_behavior_database_column_default_changed_for_time`

**Inputs** self, cur\_default, new\_default.

**Explicit results** cur differs from new.

**Local steps**

- Bind dependencies datetime.
- Bind local operation normalize\_time for subsequent calls.
- Set cur from normalize\_time(cur\_default).
- Set new from normalize\_time(new\_default).
- Return cur differs from new.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L5960) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1322) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1433)

<a id="op-6c0e8403262bfe"></a>
### Db Column.default changed for time.normalize time

`operation_foundation_database_schema_business_behavior_database_column_default_changed_for_time_normalize_time`

**Inputs** val.

**Explicit results** no value · datetime.strptime(val, fmt).time().strftime(“%H:%M:%S.%f”) · val.

**Local steps**

- If not val.
  - Return no value.
- For each fmt in tuple(“%H:%M:%S.%f”, “%H:%M:%S”, “%H:%M”).
  - Attempt the following.
    - Return datetime.strptime(val, fmt).time().strftime(“%H:%M:%S.%f”).
  - On failure (ValueError).
    - Continue with the next iteration or loop test.
- Return val.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L6247) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1323) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1434)

<a id="op-1847b65f35da16"></a>
### Validate column name

`operation_foundation_database_schema_business_behavior_validate_column_name`

**Inputs** n.

**Explicit results** n.

**Explicit failure paths** validation helper with Platform.db.InvalidColumnName — translated “Fieldname {0} cannot have special characters like {1}”.format(Platform.bold(cstr(n)), special\_characters).

**Local steps**

- If special\_characters bound to SPECIAL\_CHAR\_PATTERN.findall(n).
  - Set special\_characters from “, ”.join(generator of formatted text "{c}" for c drawn from special\_characters).
    - Draw c from special\_characters.
  - Call the validation error handler Platform.throw(translated “Fieldname {0} cannot have special characters like {1}”.format(Platform.bold(cstr(n)), special\_characters), Platform.db.InvalidColumnName).
- Return n.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L6410) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1338) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1449)

<a id="op-fa6407f059bf77"></a>
### Validate column length

`operation_foundation_database_schema_business_behavior_validate_column_length`

**Inputs** fieldname.

**Explicit failure paths** validation helper — translated “Fieldname is limited to 64 characters ({0})”.format(fieldname).

**Local steps**

- If len(fieldname) &gt; Platform.db.MAX\_COLUMN\_LENGTH.
  - Call the validation error handler Platform.throw(translated “Fieldname is limited to 64 characters ({0})”.format(fieldname)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0145.json#L6652) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1337) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1448)

<a id="op-c577ef80d337f8"></a>
### Get definition

`operation_foundation_database_schema_business_behavior_get_definition`

**Inputs** fieldtype, precision = no value, length = no value, options (named only, default no value), duckdb (named only, default false).

**Record and data access** read “DocType” via exists.

**Explicit results** no value · coltype.

**Local steps**

- If duckdb.
  - Bind dependencies get\_type\_map.
  - Set d from get\_type\_map().get(fieldtype).
- Otherwise.
  - Set d from Platform.db.type\_map.get(fieldtype).
- If (fieldtype equals “Link” and options and Platform.db.exists(“DocType”, options) and Platform.get\_meta(options).autoname equals “UUID”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype equals “Link” → options → Platform.db.exists(“DocType”, options) → Platform.get\_meta(options).autoname equals “UUID”.
  - Set d from tuple(“uuid”, no value).
- If not d.
  - Return no value.
- If (fieldtype equals “Int” and length and length &gt; 11).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype equals “Int” → length → length &gt; 11.
  - Set d from Platform.db.type\_map.get(“Long Int”).
- Set coltype from d at 0.
- Set size from d at 1 when d at 1, otherwise no value.
  - Value choice on d at 1 — true gives d at 1, false gives no value.
- If size.
  - If fieldtype belongs to CONFIGURABLE\_DECIMAL\_TYPES.
    - Set width from length when length, otherwise DEFAULT\_DECIMAL\_LENGTH.
      - Value choice on length — true gives length, false gives DEFAULT\_DECIMAL\_LENGTH.
    - Set precision\_is\_set from precision does not belong to tuple(no value, empty text).
    - Set precision from precision when precision\_is\_set, otherwise DEFAULT\_DECIMAL\_PRECISION.
      - Value choice on precision\_is\_set — true gives precision, false gives DEFAULT\_DECIMAL\_PRECISION.
    - If cint(precision) &gt; cint(width).
      - Set precision from width.
    - Set size from formatted text {cint(width)},{cint(precision)}.
  - If length.
    - If coltype equals “varchar”.
      - If cint(length) &lt; 64.
        - Set length from 64.
      - Set size from length.
    - Otherwise.
      - If (coltype equals “int” and length &lt; 11).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in coltype equals “int” → length &lt; 11.
        - Set size from length.
- If size is distinct from no value.
  - Set coltype from formatted text {coltype}({size}).
- Return coltype.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1336) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1447)

<a id="op-70a60cf756d3e2"></a>
### Add column

`operation_foundation_database_schema_business_behavior_add_column`

**Inputs** doctype, column\_name, fieldtype, precision = no value, length = no value, default = no value, not\_null = false.

**State and service calls** commit · execute a supplied database query.

**Explicit results** no value.

**Local steps**

- Evaluate Platform.db.commit().
- If Platform.db.db\_type equals “sqlite”.
  - If column\_name belongs to Platform.db.get\_table\_columns(doctype).
    - Return no value.
  - Set query from query text (ALTER).format(doctype, column\_name, get\_definition(fieldtype, precision, length)).
- Otherwise.
  - Set query from query text (ALTER).format(doctype, column\_name, get\_definition(fieldtype, precision, length)).
- If not\_null.
  - Update query using + “ not null”.
- If default.
  - Update query using + formatted text  default '{default}'.
- Evaluate Platform.db.sql(query).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L970) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1318) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1429)

<a id="op-90df8f01779647"></a>
### SQLite Table.create

`operation_foundation_database_sqlite_schema_business_behavior_supplier_quotation_lite_table_create`

**Inputs** self.

**Local steps**

- Set additional\_definitions from list().
- Set name\_column from “name TEXT PRIMARY KEY”.
- Set column\_defs from self.get\_column\_definitions().
- If column\_defs.
  - Update additional\_definitions using + column\_defs.
- Set index\_defs from list().
- If self.meta.get(“istable”, default = 0).
  - Evaluate additional\_definitions.extend(list(“parent TEXT”, “parentfield TEXT”, “parenttype TEXT”)).
  - Evaluate index\_defs.append(formatted text CREATE INDEX ′{self.table\_name}\_parent\_idx′ ON ′{self.table\_name}′(parent)).
- Otherwise.
  - Evaluate index\_defs.append(formatted text CREATE INDEX ′{self.table\_name}\_creation\_idx′ ON ′{self.table\_name}′(creation)).
  - If self.meta.sort\_field equals “modified”.
    - Evaluate index\_defs.append(formatted text CREATE INDEX ′{self.table\_name}\_modified\_idx′ ON ′{self.table\_name}′(modified)).
- If (not self.meta.issingle and self.meta.autoname equals “autoincrement”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.meta.issingle → self.meta.autoname equals “autoincrement”.
  - Set name\_column from “name INTEGER PRIMARY KEY AUTOINCREMENT”.
- Otherwise.
  - If (not self.meta.issingle and self.meta.autoname equals “UUID”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.meta.issingle → self.meta.autoname equals “UUID”.
    - Set name\_column from “name TEXT PRIMARY KEY”.
- Set additional\_definitions from “,\\n”.join(additional\_definitions).
- Set create\_table\_query from formatted text CREATE TABLE ′{self.table\_name}′ (  {name\_column},  creation DATETIME,  modified DATETIME,  modified\_by TEXT,  owner TEXT,  docstatus INTE.
- Evaluate Platform.db.sql\_ddl(create\_table\_query).
- For each index\_query in index\_defs.
  - Evaluate Platform.db.sql\_ddl(index\_query).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L659) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1410) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1517)

<a id="op-36c0625b5e1e2f"></a>
### SQLite Table.alter

`operation_foundation_database_sqlite_schema_business_behavior_supplier_quotation_lite_table_alter`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Explicit results** no value.

**Local steps**

- For each col in self.columns.values().
  - Evaluate col.build\_for\_alter\_table(self.current\_columns.get(col.fieldname.lower())).
- For each col in self.add\_column.
  - Evaluate Platform.db.sql\_ddl(formatted text ALTER TABLE ′{self.table\_name}′ ADD COLUMN ′{col.fieldname}′ {col.get\_definition()}).
- If not (self.change\_type or self.set\_default or self.change\_nullability or self.add\_index or self.add\_unique or self.drop\_index or self.drop\_unique).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.change\_type → self.set\_default → self.change\_nullability → self.add\_index → self.add\_unique → self.drop\_index → self.drop\_unique.
  - Return no value.
- Set existing\_columns from list().
- For each column in Platform.db.sql(formatted text PRAGMA table\_info(′{self.table\_name}′), as\_dict = 1).
  - Evaluate existing\_columns.append(formatted text ′{column.name}′ {column.type}).
- Set columns from existing\_columns.copy().
- Set columns\_to\_modify from set(((self.change\_type + self.set\_default) + self.change\_nullability)).
- For each col in columns\_to\_modify.
  - For each tuple(i, column) in enumerate(columns).
    - If column.startswith(formatted text ′{col.fieldname}′).
      - Set columns at i from formatted text ′{col.fieldname}′ {col.get\_definition(for\_modification = true)}.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Set temp\_table from formatted text {self.table\_name}\_new.
- Set create\_table from formatted text CREATE TABLE ′{temp\_table}′ ( {“,”.join(columns)} ).
- Evaluate Platform.db.sql\_ddl(create\_table).
- Set existing\_columns from list of col.split() at 0 for col drawn from existing\_columns.
  - Draw col from existing\_columns.
- Set column\_list from “, ”.join(existing\_columns).
- Evaluate Platform.db.sql\_ddl(formatted text INSERT INTO ′{temp\_table}′ SELECT {column\_list} FROM ′{self.table\_name}′).
- Evaluate Platform.db.sql\_ddl(formatted text DROP TABLE ′{self.table\_name}′).
- Evaluate Platform.db.sql\_ddl(formatted text ALTER TABLE ′{temp\_table}′ RENAME TO ′{self.table\_name}′).
- Set index\_queries from list().
- If self.add\_unique.
  - Evaluate index\_queries.extend(generator of formatted text CREATE UNIQUE INDEX IF NOT EXISTS ′{col.fieldname}′ ON ′{self.table\_name}′ (′{col.fieldname}′) for col drawn from self.add\_unique).
    - Draw col from self.add\_unique.
- If self.add\_index.
  - Evaluate index\_queries.extend(generator of formatted text CREATE INDEX IF NOT EXISTS ′{col.fieldname}\_index′ ON ′{self.table\_name}′ (′{col.fieldname}′) for col drawn from self.add\_index where not Platform.db.get\_co ….
    - Draw col from self.add\_index, keep a combination only if (not Platform.db.get\_column\_index(self.table\_name, col.fieldname, unique = false)).
- If (self.meta.sort\_field equals “modified” and not Platform.db.get\_column\_index(self.table\_name, “modified”, unique = false)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.sort\_field equals “modified” → not Platform.db.get\_column\_index(self.table\_name, “modified”, unique = false).
  - Evaluate index\_queries.append(formatted text CREATE INDEX IF NOT EXISTS ′modified′ ON ′{self.table\_name}′ (′modified′)).
- For each query in index\_queries.
  - Evaluate Platform.db.sql\_ddl(query).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L1383) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1408) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1515)

<a id="op-da462b7739d0e1"></a>
### SQLite Table.alter primary key

`operation_foundation_database_sqlite_schema_business_behavior_supplier_quotation_lite_table_alter_primary_key`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Record and data access** read self.doctype via get\_value.

**Explicit results** “ALTER COLUMN name TEXT”.

**Explicit failure paths** validation helper — translated “Primary key of doctype {0} can not be changed as there are existing values.”.format(self.doctype).

**Local steps**

- Set autoname from self.meta.autoname.
- If (autoname equals “UUID” and Platform.db.get\_column\_type(self.doctype, “name”) differs from “TEXT”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in autoname equals “UUID” → Platform.db.get\_column\_type(self.doctype, “name”) differs from “TEXT”.
  - If not Platform.db.get\_value(self.doctype, mapping(), order\_by = no value).
    - Return “ALTER COLUMN name TEXT”.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Primary key of doctype {0} can not be changed as there are existing values.”.format(self.doctype)).
- If (autoname differs from “UUID” and Platform.db.get\_column\_type(self.doctype, “name”) equals “TEXT”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in autoname differs from “UUID” → Platform.db.get\_column\_type(self.doctype, “name”) equals “TEXT”.
  - Return “ALTER COLUMN name TEXT”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L2983) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1409) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1516)

## Record · Security settings

[Record definition](../../../../data/record-types/security_settings.json)

<a id="op-f19aeb6ef8d0bb"></a>
### Security Settings.security txt

`operation_foundation_core_record_definitions_security_settings_business_behavior_security_settings_security_text_resource`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** (whitespace '\\n\\n'.join(list(self.public\_policy\_section, self.public\_contacts\_section, self.public\_languages\_section, self.public\_expires\_section)) + whitespace '\\n').

**Local steps**

- Return (whitespace '\\n\\n'.join(list(self.public\_policy\_section, self.public\_contacts\_section, self.public\_languages\_section, self.public\_expires\_section)) + whitespace '\\n').

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L1099) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L340) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L504)

<a id="op-31486b0637469d"></a>
### Security Settings.public policy section

`operation_foundation_core_record_definitions_security_settings_business_behavior_security_settings_public_policy_section`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** formatted text # Read our security policy before reporting an issue Policy: {value}.

**Local steps**

- Set value from (self.public\_policy or text in the contract).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.public\_policy → text in the contract.
- Return formatted text # Read our security policy before reporting an issue Policy: {value}.

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L1199) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L339) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L503)

<a id="op-5dfbbd3c52e2e0"></a>
### Security Settings.public contacts section

`operation_foundation_core_record_definitions_security_settings_business_behavior_security_settings_public_contacts_section`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** formatted text # Our security address {value}.

**Local steps**

- Set contacts from (list of self.with\_protocol(c.contact, c.type) for c drawn from self.public\_contacts or list(text in the contract)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of self.with\_protocol(c.contact, c.type) for c drawn from self.public\_contacts → list(text in the contract).
  - Draw c from self.public\_contacts.
- Set value from whitespace '\\n'.join(generator of formatted text Contact: {c} for c drawn from contacts).
  - Draw c from contacts.
- Return formatted text # Our security address {value}.

**Methods declared on this owner** [with protocol](operations-091.md#op-1bab800ec0fe9b).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L1289) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L336) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L500)

<a id="op-0c33e6e137c8a4"></a>
### Security Settings.public languages section

`operation_foundation_core_record_definitions_security_settings_business_behavior_security_settings_public_languages_section`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** formatted text # We prefer talking in Preferred-Languages: {value}.

**Local steps**

- Set langs from (list of l.language for l drawn from self.public\_languages or list(“en”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of l.language for l drawn from self.public\_languages → list(“en”).
  - Draw l from self.public\_languages.
- Set value from “, ”.join(langs).
- Return formatted text # We prefer talking in Preferred-Languages: {value}.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L1497) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L338) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L502)

<a id="op-0f258fd464ed19"></a>
### Security Settings.public expires section

`operation_foundation_core_record_definitions_security_settings_business_behavior_security_settings_public_expires_section`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** formatted text Expires: {value}.

**Local steps**

- Set expires from (self.public\_expires or Platform.utils.add\_years(Platform.utils.now\_datetime(), 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.public\_expires → Platform.utils.add\_years(Platform.utils.now\_datetime(), 1).
- If isinstance(expires, str).
  - Set expires from datetime.fromisoformat(expires).
- Set expires from expires.replace(microsecond = 0, tzinfo = ZoneInfo(get\_system\_timezone())).astimezone(UTC).
- Set value from expires.strftime(“%Y-%m-%dT%H:%M:%SZ”).
- Return formatted text Expires: {value}.

**Values supplied outside this operation** clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L1639) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L337) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L501)

<a id="op-1bab800ec0fe9b"></a>
### Security Settings.with protocol

`operation_foundation_core_record_definitions_security_settings_business_behavior_security_settings_with_protocol`

**Inputs** self, url, type\_.

**Declared result** str.

**Explicit results** formatted text mailto:{url} · formatted text tel:{url} · url.

**Local steps**

- Select the first matching pattern against type\_.
  - Pattern “Email”.
    - If not url.startswith(“mailto:”).
      - Return formatted text mailto:{url}.
  - Pattern “Phone”.
    - If not url.startswith(“tel:”).
      - Return formatted text tel:{url}.
- Return url.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L1929) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L345) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L509)

<a id="op-1f8dddbfc80901"></a>
### Security Settings.validate

`operation_foundation_core_record_definitions_security_settings_business_behavior_security_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_public\_policy().
- Evaluate self.validate\_public\_contacts().
- Evaluate self.validate\_expires().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate public policy](operations-091.md#op-db8d10bf0320ad), [validate public contacts](operations-091.md#op-b103394724ba76), [validate expires](operations-091.md#op-934019df85c6a3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L2137) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L341) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L505)

<a id="op-db8d10bf0320ad"></a>
### Security Settings.validate public policy

`operation_foundation_core_record_definitions_security_settings_business_behavior_security_settings_validate_public_policy`

**Inputs** self.

**Explicit failure paths** validation helper — translated text in the contract.

**Local steps**

- If self.public\_policy.
  - If not self.public\_policy.startswith(text in the contract).
    - Call the validation error handler Platform.throw(translated text in the contract).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L2228) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L344) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L508)

<a id="op-b103394724ba76"></a>
### Security Settings.validate public contacts

`operation_foundation_core_record_definitions_security_settings_business_behavior_security_settings_validate_public_contacts`

**Inputs** self.

**Explicit failure paths** validation helper — translated text in the contract.

**Local steps**

- For each contact in self.public\_contacts.
  - Select the first matching pattern against contact.type.
    - Pattern “Email”.
      - Evaluate validate\_email\_address(contact.contact, throw = true).
    - Pattern “Phone”.
      - Evaluate validate\_phone\_number(contact.contact, throw = true).
    - Pattern “Website”.
      - Evaluate validate\_url(contact.contact, throw = true).
      - If not contact.contact.startswith(text in the contract).
        - Call the validation error handler Platform.throw(translated text in the contract).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L2345) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L343) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L507)

<a id="op-934019df85c6a3"></a>
### Security Settings.validate expires

`operation_foundation_core_record_definitions_security_settings_business_behavior_security_settings_validate_expires`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Expiration date must be in the future”.

**Local steps**

- If self.public\_expires.
  - Set expires from self.public\_expires.
  - If isinstance(expires, str).
    - Set expires from datetime.fromisoformat(expires).
  - If expires ≤ now\_datetime().
    - Call the validation error handler Platform.throw(translated “Expiration date must be in the future”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L2633) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L342) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L506)
