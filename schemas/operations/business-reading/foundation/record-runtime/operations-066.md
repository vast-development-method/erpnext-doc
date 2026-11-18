# Record lifecycle and persistence · operations 66

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Mysqlclient

<a id="op-816f41d4aeab65"></a>
### Maria DBDatabase.get column type

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_get_column_type`

**Inputs** self, doctype, column.

**Explicit results** nested operand in the contract.select(nested operand in the contract.column\_type).where(((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equ … at 0.

**Local steps**

- Set information\_schema from Platform.qb.Schema(“information\_schema”).
- Set table from get\_table\_name(doctype).
- Return nested operand in the contract.select(nested operand in the contract.column\_type).where(((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equ … at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L7402) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1256) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1373)

<a id="op-ff82f844118942"></a>
### Maria DBDatabase.has index

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_has_index`

**Inputs** self, table\_name, index\_name.

**Explicit results** self.sql(formatted text SHOW INDEX FROM ′{table\_name}′  WHERE Key\_name='{index\_name}').

**Local steps**

- Return self.sql(formatted text SHOW INDEX FROM ′{table\_name}′  WHERE Key\_name='{index\_name}').

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0133.json#L7687) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1263) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1380)

<a id="op-7e5788811a2693"></a>
### Maria DBDatabase.get column index

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_get_column_index`

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

[Applicable decision contract](../../../foundation-decision-contracts/part-0134.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1255) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1372)

<a id="op-fdebb0f82c6ec5"></a>
### Maria DBDatabase.add index

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_add_index`

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

**Methods declared on this owner** [has index](operations-066.md#op-ff82f844118942).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L132) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1244) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1362)

<a id="op-c1cafe4c58bbbb"></a>
### Maria DBDatabase.add unique

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_add_unique`

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

[Applicable decision contract](../../../foundation-decision-contracts/part-0134.json#L1285) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1245) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1363)

<a id="op-2e1ee43f846a41"></a>
### Maria DBDatabase.updatedb

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_updatedb`

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

[Applicable decision contract](../../../foundation-decision-contracts/part-0134.json#L1625) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1271) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1388)

<a id="op-046b226355ac17"></a>
### Maria DBDatabase.get database list

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_get_database_list`

**Inputs** self.

**Explicit results** self.sql(“SHOW DATABASES”, pluck = true).

**Local steps**

- Return self.sql(“SHOW DATABASES”, pluck = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0134.json#L1914) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1257) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1374)

<a id="op-868064afcfd708"></a>
### Maria DBDatabase.get tables

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_get_tables`

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

[Applicable decision contract](../../../foundation-decision-contracts/part-0134.json#L1978) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1262) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1379)

<a id="op-73b10828daf716"></a>
### Maria DBDatabase.get row size

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_get_row_size`

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

[Applicable decision contract](../../../foundation-decision-contracts/part-0134.json#L2314) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1260) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1377)

<a id="op-242561d1de305e"></a>
### Maria DBDatabase.unbuffered cursor

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_unbuffered_cursor`

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

[Applicable decision contract](../../../foundation-decision-contracts/part-0134.json#L3282) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1270) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1387)

<a id="op-7304c38452addc"></a>
### Maria DBDatabase.estimate count

`operation_foundation_database_relational_storage_mysqlclient_business_behavior_maria_database_database_estimate_count`

**Inputs** self, table.

**Declared result** int.

**Explicit results** cint(count at 0 at 0) when count, otherwise 0.

**Local steps**

- Bind dependencies cint.
- Set count from self.sql(query text (SELECT), tuple(table, Platform.db.cur\_db\_name)).
- Return cint(count at 0 at 0) when count, otherwise 0.
  - Value choice on count — true gives cint(count at 0 at 0), false gives 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0134.json#L3476) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1254) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1371)

## Service · Naming

<a id="op-036c70ac28eb67"></a>
### Naming Series.initialize

`operation_foundation_model_naming_business_behavior_naming_series_initialize`

**Inputs** self, series.

**Local steps**

- Set self.series from series.
- If “#” does not belong to self.series.
  - Update self.series using + “.#####”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L123) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L600) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1196)

<a id="op-14490146142334"></a>
### Naming Series.validate

`operation_foundation_model_naming_business_behavior_naming_series_validate`

**Inputs** self.

**Explicit failure paths** validation helper with InvalidNamingSeriesError — translated “Invalid naming series {}: dot (.) missing”.format(Platform.bold(self.series)) · validation helper with InvalidNamingSeriesError — translated “Special Characters except '-', '#', '.', '/', '{{' and '}}' not allowed in naming series {0}”.format(Platform.bold(self.series)) · validation helper with InvalidNamingSeriesError — translated “Invalid naming series {}: dot (.) missing before the numeric placeholders. Kindly use a format like &lt;b&gt;ABCD. …”.format(Platform.bold(self.series)).

**Local steps**

- If “.” does not belong to self.series.
  - Call the validation error handler Platform.throw(translated “Invalid naming series {}: dot (.) missing”.format(Platform.bold(self.series)), exc = InvalidNamingSeriesError).
- If not NAMING\_SERIES\_PATTERN.match(self.series).
  - Call the validation error handler Platform.throw(translated “Special Characters except '-', '#', '.', '/', '{{' and '}}' not allowed in naming series {0}”.format(Platform.bold(self.series)), exc = InvalidNamingSeriesError).
- If (“#” belongs to self.series and “.#” does not belong to self.series).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “#” belongs to self.series → “.#” does not belong to self.series.
  - Call the validation error handler Platform.throw(translated “Invalid naming series {}: dot (.) missing before the numeric placeholders. Kindly use a format like &lt;b&gt;ABCD. …”.format(Platform.bold(self.series)), exc = InvalidNamingSeriesError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L6272) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L602) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1198)

<a id="op-2495817a884900"></a>
### Naming Series.generate next name

`operation_foundation_model_naming_business_behavior_naming_series_generate_next_name`

**Inputs** self, doc, ignore\_validate (named only, default false).

**Declared result** str.

**Explicit results** parse\_naming\_series(parts, doc = doc).

**Local steps**

- If not ignore\_validate.
  - Evaluate self.validate().
- Set parts from self.series.split(“.”).
- Return parse\_naming\_series(parts, doc = doc).

**Methods declared on this owner** [validate](operations-066.md#op-14490146142334).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L6672) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L594) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1190)

<a id="op-eab9bb9401dcee"></a>
### Naming Series.get prefix

`operation_foundation_model_naming_business_behavior_naming_series_get_prefix`

**Inputs** self, doc = no value.

**Declared result** str.

**Explicit results** prefix.

**Explicit failure paths** validation helper — translated “Invalid Naming Series: {}”.format(self.series).

**Local steps**

- Set prefix from no value.
- Bind local operation fake\_counter\_backend for subsequent calls.
- Evaluate parse\_naming\_series(self.series, doc = doc, number\_generator = fake\_counter\_backend).
- If prefix is identical to no value.
  - Call the validation error handler Platform.throw(translated “Invalid Naming Series: {}”.format(self.series)).
- Return prefix.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L122) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L596) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1192)

<a id="op-afd61c02e0d412"></a>
### Naming Series.get prefix.fake counter backend

`operation_foundation_model_naming_business_behavior_naming_series_get_prefix_fake_counter_backend`

**Inputs** partial\_series, digits.

**Explicit results** (“#” × digits).

**Local steps**

- Use enclosing bindings prefix.
- Set prefix from partial\_series.
- Return (“#” × digits).

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L7059) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L597) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1193)

<a id="op-aedf3f9d41a680"></a>
### Naming Series.get preview

`operation_foundation_model_naming_business_behavior_naming_series_get_preview`

**Inputs** self, doc = no value.

**Declared result** list at str.

**Explicit results** generated\_names.

**Local steps**

- Set generated\_names from list().
- For each count in range(1, 4).
  - Bind local operation fake\_counter for subsequent calls.
  - Evaluate generated\_names.append(parse\_naming\_series(self.series, doc = doc, number\_generator = fake\_counter)).
- Return generated\_names.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L7131) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L598) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1194)

<a id="op-5c07fa4bc4cc21"></a>
### Naming Series.get preview.fake counter

`operation_foundation_model_naming_business_behavior_naming_series_get_preview_fake_counter`

**Inputs** \_prefix, digits.

**Explicit results** str(count).zfill(digits).

**Local steps**

- Return str(count).zfill(digits).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L6493) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L599) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1195)

<a id="op-c63d62b08a1531"></a>
### Naming Series.update counter

`operation_foundation_model_naming_business_behavior_naming_series_update_counter`

**Inputs** self, new\_count, doc = no value.

**Declared result** no value.

**Record and data access** read “Series” via get\_value.

**State and service calls** call insert on Platform.qb.into(Series).

**Local steps**

- Set Series from Platform.qb.DocType(“Series”).
- Set prefix from self.get\_prefix(doc).
- If Platform.db.get\_value(“Series”, prefix, “name”, order\_by = “name”) is identical to no value.
  - Evaluate nested operand in the contract(nested operand in the contract).insert(prefix, 0).columns(“name”, “current”).run().
- Evaluate nested operand in the contract(nested operand in the contract).set(Series.current, cint(new\_count)).where(Series.name equals prefix).run().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get prefix](operations-066.md#op-eab9bb9401dcee).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L124) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L601) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1197)

<a id="op-7636cbdae09b62"></a>
### Naming Series.get current value

`operation_foundation_model_naming_business_behavior_naming_series_get_current_value`

**Inputs** self, doc = no value.

**Declared result** int.

**Record and data access** read “Series” via get\_value.

**Explicit results** cint(Platform.db.get\_value(“Series”, prefix, “current”, order\_by = “name”, for\_update = true)).

**Local steps**

- Set prefix from self.get\_prefix(doc).
- Return cint(Platform.db.get\_value(“Series”, prefix, “current”, order\_by = “name”, for\_update = true)).

**Methods declared on this owner** [get prefix](operations-066.md#op-eab9bb9401dcee).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L121) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L595) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1191)

<a id="op-540d271e3c3e20"></a>
### Set new name

`operation_foundation_model_naming_business_behavior_set_new_name`

**Inputs** doc.

**Explicit results** no value.

**Explicit failure paths** validation helper with InvalidUUIDValue — translated “Invalid value specified for UUID: {}”.format(doc.name).

**Local steps**

- Evaluate doc.run\_method(“before\_naming”).
- Set meta from Platform.get\_meta(doc.doctype).
- Set autoname from (meta.autoname or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.autoname → empty text.
- If (autoname.lower() does not belong to tuple(“prompt”, “uuid”) and not Platform.flags.in\_import).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in autoname.lower() does not belong to tuple(“prompt”, “uuid”) → not Platform.flags.in\_import.
  - Set doc.name from no value.
- If is\_autoincremented(doc.doctype, meta).
  - Set doc.name from Platform.db.get\_next\_sequence\_val(doc.doctype).
  - Return no value.
- If meta.autoname equals “UUID”.
  - If not doc.name.
    - Set doc.name from str(uuid7()).
  - Otherwise.
    - If isinstance(doc.name, UUID).
      - Set doc.name from str(doc.name).
    - Otherwise.
      - If isinstance(doc.name, str).
        - Attempt the following.
          - Evaluate UUID(doc.name).
        - On failure (ValueError).
          - Call the validation error handler Platform.throw(translated “Invalid value specified for UUID: {}”.format(doc.name), InvalidUUIDValue).
  - Return no value.
- If getattr(doc, “amended\_from”, no value).
  - Evaluate \_set\_amended\_name(doc).
  - If doc.name.
    - Return no value.
- Otherwise.
  - If getattr(doc.meta, “issingle”, false).
    - Set doc.name from doc.doctype.
- If not doc.name.
  - Evaluate set\_naming\_from\_document\_naming\_rule(doc).
- If not doc.name.
  - Evaluate doc.run\_method(“autoname”).
- If (not doc.name and autoname).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.name → autoname.
  - Evaluate set\_name\_from\_naming\_options(autoname, doc).
- If not doc.name.
  - Set doc.name from make\_autoname(“hash”, doc.doctype).
- Set doc.name from validate\_name(doc.doctype, doc.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from doc.run\_method(“before\_naming”), getattr(doc, “amended\_from”, no value) and 2 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0286.json#L513) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L611) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1206)

<a id="op-a0185e31849795"></a>
### Is autoincremented

`operation_foundation_model_naming_business_behavior_is_autoincremented`

**Inputs** doctype, meta = no value.

**Declared result** bool.

**Explicit results** (not getattr(meta, “issingle”, false) and meta.autoname equals “autoincrement”).

**Local steps**

- If not meta.
  - Set meta from Platform.get\_meta(doctype).
- Return (not getattr(meta, “issingle”, false) and meta.autoname equals “autoincrement”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not getattr(meta, “issingle”, false) → meta.autoname equals “autoincrement”.

**Values supplied outside this operation** selected callable from getattr(meta, “issingle”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0286.json#L1482) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L592) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1188)

<a id="op-bf373400d00909"></a>
### Set name from naming options

`operation_foundation_model_naming_business_behavior_set_name_from_naming_options`

**Inputs** autoname, doc.

**Explicit failure paths** validation helper — translated “{0} is required”.format(doc.meta.get\_label(fieldname)).

**Local steps**

- Set \_autoname from autoname.lower().
- If \_autoname.startswith(“field:”).
  - Set doc.name from \_field\_autoname(autoname, doc).
  - If not doc.name.
    - Set fieldname from autoname at slice 6 to no value.
    - Call the validation error handler Platform.throw(translated “{0} is required”.format(doc.meta.get\_label(fieldname))).
- Otherwise.
  - If \_autoname.startswith(“naming\_series:”).
    - Evaluate set\_name\_by\_naming\_series(doc).
  - Otherwise.
    - If \_autoname.startswith(“prompt”).
      - Evaluate \_prompt\_autoname(autoname, doc).
    - Otherwise.
      - If \_autoname.startswith(“format:”).
        - Set doc.name from \_format\_autoname(autoname, doc).
      - Otherwise.
        - If “#” belongs to autoname.
          - Set doc.name from make\_autoname(autoname, doc = doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L125) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L608) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1204)

<a id="op-1c2f406b3e42e3"></a>
### Set naming from document naming rule

`operation_foundation_model_naming_business_behavior_set_naming_from_document_naming_rule`

**Inputs** doc.

**Record and data access** resolve a document from “Document Naming Rule” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- Bind dependencies DOCTYPES\_FOR\_DOCTYPE.
- Set IGNORED\_DOCTYPES from set(expanded log\_types, expanded DOCTYPES\_FOR\_DOCTYPE, “DefaultValue”, “Patch Log”).
- If doc.doctype belongs to IGNORED\_DOCTYPES.
  - Return no value.
- Set document\_naming\_rules from Platform.cache\_manager.get\_doctype\_map(“Document Naming Rule”, doc.doctype, filters = mapping(“document\_type” → doc.doctype, “disabled” → 0), order\_by = “priority desc”).
- For each d in document\_naming\_rules.
  - Evaluate Platform.get\_cached\_doc(“Document Naming Rule”, d.name).apply(doc).
  - If doc.name.
    - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Document Naming Rule”, d.name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L126) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L610) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1205)
