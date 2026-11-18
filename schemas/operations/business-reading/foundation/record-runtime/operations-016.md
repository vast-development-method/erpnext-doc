# Record lifecycle and persistence · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Data import

[Record definition](../../../../data/record-types/data_import.json)

<a id="op-6f88455d3940f0"></a>
### Normalize source value

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_normalize_source_value`

**Inputs** value.

**Declared result** str.

**Explicit results** cstr(value).strip().

**Local steps**

- Return cstr(value).strip().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0060.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1354) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1345)

<a id="op-21d3f0f6ea07c4"></a>
### Build lookup from mappings

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_build_lookup_from_mappings`

**Inputs** mappings, reference\_doctype = no value.

**Declared result** dict at tuple(str, dict at tuple(str, str)).

**Explicit results** lookup.

**Local steps**

- Set lookup from mapping().
- For each row in mappings.
  - Set row from Platform.\_dict(row).
  - Set ref from (row.reference\_doctype or reference\_doctype or row.parenttype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.reference\_doctype → reference\_doctype → row.parenttype.
  - Set tuple(source, target) from tuple(normalize\_source\_value(row.source\_value), (row.target\_value or empty text).strip()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.target\_value → empty text.
  - If wants\_new\_record(row).
    - Set target from source.
  - If not (ref and row.fieldname and source and target).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref → row.fieldname → source → target.
    - Continue with the next iteration or loop test.
  - Set key from get\_field\_key(ref, row.fieldname, (row.parent\_field or no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.parent\_field → no value.
  - Set lookup.setdefault(key, mapping()) at source from target.
- Return lookup.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L52) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1341) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1332)

<a id="op-af769653ab098c"></a>
### Build lookup for data import

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_build_lookup_for_data_import`

**Inputs** data\_import\_name, reference\_doctype.

**Declared result** dict at tuple(str, dict at tuple(str, str)).

**Record and data access** read “Data Import” via exists · read “Data Import Value Mapping” via get\_all.

**Explicit results** mapping() · build\_lookup\_from\_mappings(rows, reference\_doctype).

**Local steps**

- If (not data\_import\_name or not Platform.db.exists(“Data Import”, data\_import\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not data\_import\_name → not Platform.db.exists(“Data Import”, data\_import\_name).
  - Return mapping().
- Set rows from Platform.get\_all(“Data Import Value Mapping”, filters = mapping(“parent” → data\_import\_name), fields = list(“fieldname”, “parent\_field”, “source\_value”, “target\_value”, …)).
- Return build\_lookup\_from\_mappings(rows, reference\_doctype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L51) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1340) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1331)

<a id="op-c644d544f7eebf"></a>
### Get create field

`operation_foundation_binding_foundation_core_doctype_data_import_value_mapping_get_create_field`

**Inputs** doctype.

**Declared result** (str bitwise or no value).

**Explicit results** no value · fieldname.

**Local steps**

- Bind dependencies no\_value\_fields.
- Set meta from Platform.get\_meta(doctype).
- If (meta.issingle or meta.istable or not (meta.autoname or empty text).startswith(“field:”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.issingle → meta.istable → not (meta.autoname or empty text).startswith(“field:”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.autoname → empty text.
  - Return no value.
- Set fieldname from meta.autoname at slice len(“field:”) to no value.strip().
- For each df in meta.fields.
  - If (df.reqd and df.fieldname differs from fieldname and df.default belongs to INVALID\_VALUES and df.fieldtype does not belong to no\_value\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.reqd → df.fieldname differs from fieldname → df.default belongs to INVALID\_VALUES → df.fieldtype does not belong to no\_value\_fields.
    - Return no value.
- If not Platform.has\_permission(doctype, “create”).
  - Return no value.
- Return fieldname.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “create”).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L164) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L646) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L622)

<a id="op-9e4c6655d49ae6"></a>
### Wants new record

`operation_foundation_binding_foundation_core_doctype_data_import_value_mapping_wants_new_record`

**Inputs** row.

**Declared result** bool.

**Explicit results** (not (row.target\_value or empty text).strip() and bool((cint(row.create\_new) and cint(row.can\_create)))).

**Local steps**

- Return (not (row.target\_value or empty text).strip() and bool((cint(row.create\_new) and cint(row.can\_create)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not (row.target\_value or empty text).strip() → bool((cint(row.create\_new) and cint(row.can\_create))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.target\_value → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(row.create\_new) → cint(row.can\_create).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L166) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L648) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L624)

<a id="op-9b7eff7eac1a45"></a>
### Create missing link records

`operation_foundation_binding_foundation_core_doctype_data_import_value_mapping_create_missing_link_records`

**Inputs** data\_import.

**Declared result** no value.

**Record and data access** read row.link\_doctype via exists · resolve a document from mapping(“doctype” → row.link\_doctype, fieldname → value) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → row.link\_doctype, fieldname → value)) · commit · rollback.

**Local steps**

- Set skipped\_rows from get\_skipped\_row\_numbers(data\_import).
- For each row in (data\_import.get(“value\_mappings”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data\_import.get(“value\_mappings”) → list().
  - If (not wants\_new\_record(row) or all\_rows\_skipped(row, skipped\_rows)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not wants\_new\_record(row) → all\_rows\_skipped(row, skipped\_rows).
    - Continue with the next iteration or loop test.
  - Set value from normalize\_source\_value(row.source\_value).
  - Set fieldname from get\_create\_field(row.link\_doctype).
  - If (not fieldname or Platform.db.exists(row.link\_doctype, value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not fieldname → Platform.db.exists(row.link\_doctype, value).
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Evaluate Platform.get\_doc(mapping(“doctype” → row.link\_doctype, fieldname → value)).insert().
    - Evaluate Platform.db.commit().
  - On failure (Exception).
    - Evaluate Platform.db.rollback().
    - Evaluate Platform.clear\_messages().
    - Evaluate Platform.logger(“data\_import”).error(formatted text Data Import {data\_import.name}: could not create {row.link\_doctype} {value}, exc\_info = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L163) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L645) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L621)

<a id="op-f7e661e3120929"></a>
### All rows skipped

`operation_foundation_binding_foundation_core_doctype_data_import_value_mapping_all_rows_skipped`

**Inputs** row, skipped\_rows.

**Declared result** bool.

**Explicit results** (bool(row\_numbers) and row\_numbers ≤ skipped\_rows).

**Local steps**

- Set row\_numbers from set of cint(n) for n drawn from Platform.parse\_json((row.row\_numbers or “&#91;&#93;”)).
  - Draw n from Platform.parse\_json((row.row\_numbers or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.row\_numbers → “&#91;&#93;”.
- Return (bool(row\_numbers) and row\_numbers ≤ skipped\_rows).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(row\_numbers) → row\_numbers ≤ skipped\_rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L162) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L644) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L620)

<a id="op-4ca8d3ed80f413"></a>
### Get skipped row numbers

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_get_skipped_row_numbers`

**Inputs** data\_import.

**Declared result** set at int.

**Record and data access** read “Data Import Skipped Row” via get\_all.

**Explicit results** set() · set of cint(r) for r drawn from rows · set of cint(row.row\_number) for row drawn from skipped\_rows.

**Local steps**

- If (not data\_import or not getattr(data\_import, “name”, no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not data\_import → not getattr(data\_import, “name”, no value).
  - Return set().
- Set skipped\_rows from getattr(data\_import, “skipped\_rows”, no value).
- If skipped\_rows is identical to no value.
  - Set rows from Platform.get\_all(“Data Import Skipped Row”, filters = mapping(“parent” → data\_import.name), pluck = “row\_number”).
  - Return set of cint(r) for r drawn from rows.
    - Draw r from rows.
- Return set of cint(row.row\_number) for row drawn from skipped\_rows.
  - Draw row from skipped\_rows.

**Values supplied outside this operation** selected callable from getattr(data\_import, “name”, no value), getattr(data\_import, “skipped\_rows”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0060.json#L757) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1351) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1342)

<a id="op-3d1b08baad5e69"></a>
### Get field map

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_get_field_map`

**Inputs** col, lookup, reference\_doctype.

**Declared result** dict at tuple(str, str).

**Explicit results** (lookup or mapping()).get(get\_field\_key\_from\_df(col.df, reference\_doctype), mapping()).

**Local steps**

- Return (lookup or mapping()).get(get\_field\_key\_from\_df(col.df, reference\_doctype), mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in lookup → mapping().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0060.json#L1088) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1347) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1338)

<a id="op-11188286812c05"></a>
### Get column invalid items

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_get_column_invalid_items`

**Inputs** col.

**Declared result** list at dict.

**Explicit results** items · get\_invalid\_link\_select\_items(col).

**Local steps**

- Set items from getattr(col, “invalid\_value\_items”, no value).
- If items is distinct from no value.
  - Return items.
- Return get\_invalid\_link\_select\_items(col).

**Values supplied outside this operation** selected callable from getattr(col, “invalid\_value\_items”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0060.json#L1228) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1344) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1335)

<a id="op-2376f5f20d774a"></a>
### Resolve import value

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_resolve_import_value`

**Inputs** value, df, reference\_doctype, lookup.

**Declared result** str.

**Explicit results** value · lookup.get(get\_field\_key\_from\_df(df, reference\_doctype), mapping()).get(source, value).

**Local steps**

- If value belongs to INVALID\_VALUES.
  - Return value.
- Set source from normalize\_source\_value(value).
- Return lookup.get(get\_field\_key\_from\_df(df, reference\_doctype), mapping()).get(source, value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0060.json#L1353) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1356) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1346)

<a id="op-81957c8bc0383e"></a>
### Get invalid link select items

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_get_invalid_link_select_items`

**Inputs** col.

**Declared result** list at dict.

**Record and data access** read col.df.options via get\_all.

**Explicit results** list() · list of mapping(“source” → k, “rows” → value\_rows at k) for k drawn from invalid\_keys.

**Local steps**

- Bind dependencies get\_select\_options, get\_value\_row\_map.
- If (not col.df or col.skip\_import or not any(col.column\_values)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not col.df → col.skip\_import → not any(col.column\_values).
  - Return list().
- Set value\_rows from get\_value\_row\_map(col.column\_values, col.value\_row\_numbers).
- If col.df.fieldtype equals “Link”.
  - Set transform from deferred anonymous expression when Platform.db.db\_type equals “mariadb”, otherwise cstr.
    - Value choice on Platform.db.db\_type equals “mariadb” — true gives deferred anonymous expression, false gives cstr.
  - Set exists from set of transform(d.name) for d drawn from Platform.get\_all(col.df.options, filters = mapping(“name” → tuple(“in”, list(set of nested operand in the contract(nested operand in the contract) for k drawn from ….
    - Draw d from Platform.get\_all(col.df.options, filters = mapping(“name” → tuple(“in”, list(set of transform(k) for k drawn from value\_rows)))).
    - Draw k from value\_rows.
  - Set import\_refs from getattr(col, “import\_refs”, no value).
  - Set allow\_same\_file\_parents from (col.df.options equals col.doctype and import\_refs).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.df.options equals col.doctype → import\_refs.
  - Set invalid\_keys from list().
  - For each key in value\_rows.
    - If transform(key) belongs to exists.
      - Continue with the next iteration or loop test.
    - Set normalized\_key from normalize\_source\_value(key).
    - If (allow\_same\_file\_parents and normalized\_key belongs to import\_refs).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in allow\_same\_file\_parents → normalized\_key belongs to import\_refs.
      - Continue with the next iteration or loop test.
    - Evaluate invalid\_keys.append(key).
- Otherwise.
  - If col.df.fieldtype equals “Select”.
    - Set options from get\_select\_options(col.df).
    - If not options.
      - Return list().
    - Set invalid\_keys from list of k for k drawn from value\_rows where normalize\_source\_value(k) does not belong to options.
      - Draw k from value\_rows, keep a combination only if (normalize\_source\_value(k) does not belong to options).
  - Otherwise.
    - Return list().
- Return list of mapping(“source” → k, “rows” → value\_rows at k) for k drawn from invalid\_keys.
  - Draw k from invalid\_keys.

**Values supplied outside this operation** selected callable from getattr(col, “import\_refs”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0060.json#L1539) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1348) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1339)

<a id="op-0dafd486e7df40"></a>
### Get unmapped invalid values for column

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_get_unmapped_invalid_values_for_column`

**Inputs** col, lookup, reference\_doctype, skipped\_rows = no value.

**Declared result** list at dict.

**Explicit results** unmapped · list of item for item drawn from unmapped where any(generator of cint(row) does not belong to skipped\_rows for row drawn from item at “rows”).

**Local steps**

- Set field\_map from get\_field\_map(col, lookup, reference\_doctype).
- Set unmapped from list of item for item drawn from get\_column\_invalid\_items(col) where normalize\_source\_value(item at “source”) does not belong to field\_map.
  - Draw item from get\_column\_invalid\_items(col), keep a combination only if (normalize\_source\_value(item at “source”) does not belong to field\_map).
- If not skipped\_rows.
  - Return unmapped.
- Return list of item for item drawn from unmapped where any(generator of cint(row) does not belong to skipped\_rows for row drawn from item at “rows”).
  - Draw item from unmapped, keep a combination only if (any(generator of cint(row) does not belong to skipped\_rows for row drawn from item at “rows”)).
  - Draw row from item at “rows”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0060.json#L2403) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1352) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1343)

<a id="op-a9caf5135c19d5"></a>
### Get blocking warnings

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_get_blocking_warnings`

**Inputs** warnings, import\_file, data\_import = no value.

**Declared result** list.

**Explicit results** blocking.

**Local steps**

- Set cols from mapping of c.column\_number → c for c drawn from import\_file.header.columns.
  - Draw c from import\_file.header.columns.
- Set skipped\_rows from get\_skipped\_row\_numbers(data\_import).
- Set blocking from list().
- For each warning in warnings.
  - If warning.get(“type”) equals “info”.
    - Continue with the next iteration or loop test.
  - If (skipped\_rows and warning.get(“row”) and cint(warning.get(“row”)) belongs to skipped\_rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in skipped\_rows → warning.get(“row”) → cint(warning.get(“row”)) belongs to skipped\_rows.
    - Continue with the next iteration or loop test.
  - If warning.get(“type”) equals “value\_mapping”.
    - Set col from cols.get(cint(warning.get(“col”))).
    - If (col and get\_unmapped\_invalid\_values\_for\_column(col, import\_file.value\_lookup, import\_file.reference\_doctype, skipped\_rows)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in col → get\_unmapped\_invalid\_values\_for\_column(col, import\_file.value\_lookup, import\_file.reference\_doctype, skipped\_rows).
      - Evaluate blocking.append(warning).
    - Continue with the next iteration or loop test.
  - If (warning.get(“type”) equals “duplicate\_id” and skipped\_rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in warning.get(“type”) equals “duplicate\_id” → skipped\_rows.
    - Set rows from (warning.get(“rows”) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in warning.get(“rows”) → list().
    - If (len(rows) &gt; 1 and all(generator of cint(row) belongs to skipped\_rows for row drawn from rows at slice 1 to no value)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(rows) &gt; 1 → all(generator of cint(row) belongs to skipped\_rows for row drawn from rows at slice 1 to no value).
      - Draw row from rows at slice 1 to no value.
      - Continue with the next iteration or loop test.
  - Evaluate blocking.append(warning).
- Return blocking.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L54) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1343) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1334)

<a id="op-863fe1c655d35a"></a>
### Get mapping hints

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_get_mapping_hints`

**Inputs** import\_file, reference\_doctype, lookup.

**Declared result** dict.

**Explicit results** hints.

**Local steps**

- Bind dependencies get\_select\_options.
- Set hints from mapping().
- For each col in import\_file.header.columns.
  - If not col.df.
    - Continue with the next iteration or loop test.
  - Set items from get\_column\_invalid\_items(col).
  - If not items.
    - Continue with the next iteration or loop test.
  - Set field\_map from get\_field\_map(col, lookup, reference\_doctype).
  - Set parent\_field from (get\_parent\_field(col.df) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_parent\_field(col.df) → empty text.
  - Set select\_options from get\_select\_options(col.df) when col.df.fieldtype equals “Select”, otherwise list().
    - Value choice on col.df.fieldtype equals “Select” — true gives get\_select\_options(col.df), false gives list().
  - Set can\_create from (col.df.fieldtype equals “Link” and bool(get\_create\_field(col.df.options))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.df.fieldtype equals “Link” → bool(get\_create\_field(col.df.options)).
  - Set hints at cstr(col.column\_number) from list of mapping(“column” → col.column\_number, “fieldname” → col.df.fieldname, “parent\_field” → parent\_field, “fieldtype” → col.df.fieldtype, …) for item drawn from items.
    - Draw item from items.
    - Value choice on col.df.fieldtype equals “Link” — true gives col.df.options, false gives no value.
- Return hints.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L55) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1349) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1340)

<a id="op-ef30e6775eb25f"></a>
### Warn invalid link select values

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_warn_invalid_link_select_values`

**Inputs** col.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Bind dependencies format\_row\_numbers\_for\_warning, get\_select\_options.
- Set items from get\_invalid\_link\_select\_items(col).
- Set col.invalid\_value\_items from items.
- If not items.
  - Return no value.
- Set lines from list().
- Set options\_string from no value.
- If col.df.fieldtype equals “Select”.
  - Set select\_options from get\_select\_options(col.df).
  - If select\_options.
    - Set options\_string from “, ”.join(select\_options).
- For each item in items.
  - Set source from escape\_html(item at “source”).
  - Set rows\_str from format\_row\_numbers\_for\_warning(item at “rows”).
  - Set row\_label from translated “row {0}”.format(rows\_str) when len(item at “rows”) equals 1, otherwise translated “rows {0}”.format(rows\_str).
    - Value choice on len(item at “rows”) equals 1 — true gives translated “row {0}”.format(rows\_str), false gives translated “rows {0}”.format(rows\_str).
  - If col.df.fieldtype equals “Link”.
    - Set line from translated “"{0}" is not a valid {1} — {2}”.format(Platform.bold(source), Platform.bold(col.df.label), row\_label).
  - Otherwise.
    - Set line from translated “"{0}" is not valid — {1}”.format(Platform.bold(source), row\_label).
  - Evaluate lines.append(line).
- If (col.df.fieldtype equals “Select” and options\_string and lines).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.df.fieldtype equals “Select” → options\_string → lines.
  - Set allowed from translated “Allowed: {0}”.format(Platform.bold(options\_string)).
  - Set lines at negative 1 from formatted text {lines at negative 1}&lt;br&gt;&lt;span class='text-muted'&gt;{allowed}&lt;/span&gt;.
- Set message from text in the contract.join(lines).
- Evaluate col.warnings.append(mapping(“col” → col.column\_number, “message” → message, “type” → “value\_mapping”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L57) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1358) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1348)

<a id="op-ec72739af1d5ed"></a>
### Mapping row key

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_mapping_row_key`

**Inputs** row.

**Declared result** str.

**Explicit results** formatted text {row.get(“column”)}\|{row.get(“fieldname”)}\|{(row.get(“parent\_field”) or empty text)}\|{row.get(“source\_value”)}.

**Local steps**

- Return formatted text {row.get(“column”)}\|{row.get(“fieldname”)}\|{(row.get(“parent\_field”) or empty text)}\|{row.get(“source\_value”)}.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“parent\_field”) → empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0060.json#L4803) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1353) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1344)

<a id="op-d9641f362b053f"></a>
### Row count label

`operation_foundation_binding_foundation_core_doctype_data_import_value_mapping_row_count_label`

**Inputs** rows.

**Declared result** str.

**Explicit results** empty text · cstr(len(rows)).

**Local steps**

- If not rows.
  - Return empty text.
- Return cstr(len(rows)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L165) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L647) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L623)

<a id="op-c70e96b4d7cb5f"></a>
### Child row from hint

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_child_row_from_hint`

**Inputs** item, columns.

**Declared result** dict.

**Explicit results** mapping(“column” → column\_number, “column\_label” → column\_label, “fieldname” → item.fieldname, “parent\_field” → (item.parent\_field or empty text), …).

**Local steps**

- Set item from Platform.\_dict(item).
- Set column\_number from item.column.
- Set col from columns.get(column\_number).
- Set column\_label from (col.header\_title when col, otherwise no value or translated “Column {0}”.format(column\_number)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.header\_title when col, otherwise no value → translated “Column {0}”.format(column\_number).
  - Value choice on col — true gives col.header\_title, false gives no value.
- Set rows from (item.rows or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.rows → list().
- Set select\_options from (item.select\_options or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.select\_options → list().
- Return mapping(“column” → column\_number, “column\_label” → column\_label, “fieldname” → item.fieldname, “parent\_field” → (item.parent\_field or empty text), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.parent\_field → empty text.
  - Value choice on select\_options — true gives whitespace '\\n'.join(select\_options), false gives empty text.
  - Value choice on item.can\_create — true gives 1, false gives 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.target\_value → empty text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L53) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1342) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1333)

<a id="op-d828901ea8c292"></a>
### Sync value mappings

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_sync_value_mappings`

**Inputs** doc, import\_file, lookup = no value.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- Set mapping\_hints from get\_mapping\_hints(import\_file, doc.reference\_doctype, (lookup or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in lookup → mapping().
- Set items from list of item for hints drawn from mapping\_hints.values(), then item drawn from hints.
  - Draw hints from mapping\_hints.values().
  - Draw item from hints.
- Set columns from mapping of col.column\_number → col for col drawn from import\_file.header.columns.
  - Draw col from import\_file.header.columns.
- If not items.
  - If doc.get(“value\_mappings”).
    - Evaluate doc.set(“value\_mappings”, list()).
    - Return true.
  - Return false.
- Set existing from mapping of mapping\_row\_key(row) → row for row drawn from (doc.get(“value\_mappings”) or list()).
  - Draw row from (doc.get(“value\_mappings”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“value\_mappings”) → list().
- Set new\_rows from list().
- For each item in items.
  - Set key from mapping\_row\_key(item).
  - Set data from child\_row\_from\_hint(item, columns).
  - Set row from existing.get(key).
  - If row.
    - Set data at “target\_value” from (row.target\_value or empty text).strip().
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.target\_value → empty text.
    - Set data at “create\_new” from cint(row.create\_new) when data at “can\_create”, otherwise 0.
      - Value choice on data at “can\_create” — true gives cint(row.create\_new), false gives 0.
  - Evaluate new\_rows.append(data).
- Set current\_rows from list of mapping(“column” → row.column, “fieldname” → row.fieldname, “parent\_field” → (row.parent\_field or empty text), “source\_value” → row.source\_value, …) for row drawn from (doc.get(“value\_mappings”) or list()).
  - Draw row from (doc.get(“value\_mappings”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.parent\_field → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.target\_value → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“value\_mappings”) → list().
- If new\_rows equals current\_rows.
  - Return false.
- Evaluate doc.set(“value\_mappings”, list()).
- For each row in new\_rows.
  - Evaluate doc.append(“value\_mappings”, row).
- Return true.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L56) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1357) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1347)

## Service · Database

<a id="op-ebe161d95e0b0f"></a>
### Setup database

`operation_foundation_database_initialize_business_behavior_setup_database`

**Inputs** force, verbose = no value, mariadb\_user\_host\_login\_scope = no value.

**Explicit results** Platform.database.mariadb.setup\_db.setup\_database(force, verbose, mariadb\_user\_host\_login\_scope) · Platform.database.sqlite.setup\_db.setup\_database(force, verbose) · Platform.database.postgres.setup\_db.setup\_database().

**Local steps**

- Bind dependencies Platform.
- If Platform.conf.db\_type equals “mariadb”.
  - Bind dependencies Platform.database.mariadb.setup\_db.
  - Return Platform.database.mariadb.setup\_db.setup\_database(force, verbose, mariadb\_user\_host\_login\_scope).
- Otherwise.
  - If Platform.conf.db\_type equals “sqlite”.
    - Bind dependencies Platform.database.sqlite.setup\_db.
    - Return Platform.database.sqlite.setup\_db.setup\_database(force, verbose).
  - Otherwise.
    - Bind dependencies Platform.database.postgres.setup\_db.
    - Return Platform.database.postgres.setup\_db.setup\_database().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L5125) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1010) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1151)

<a id="op-40957fc0283d9d"></a>
### Bootstrap database

`operation_foundation_database_initialize_business_behavior_bootstrap_database`

**Inputs** verbose = no value, source\_sql = no value.

**Explicit results** Platform.database.mariadb.setup\_db.bootstrap\_database(verbose, source\_sql) · Platform.database.sqlite.setup\_db.bootstrap\_database(verbose, source\_sql) · Platform.database.postgres.setup\_db.bootstrap\_database(verbose, source\_sql).

**Local steps**

- Bind dependencies Platform.
- If Platform.conf.db\_type equals “mariadb”.
  - Bind dependencies Platform.database.mariadb.setup\_db.
  - Return Platform.database.mariadb.setup\_db.bootstrap\_database(verbose, source\_sql).
- Otherwise.
  - If Platform.conf.db\_type equals “sqlite”.
    - Bind dependencies Platform.database.sqlite.setup\_db.
    - Return Platform.database.sqlite.setup\_db.bootstrap\_database(verbose, source\_sql).
  - Otherwise.
    - Bind dependencies Platform.database.postgres.setup\_db.
    - Return Platform.database.postgres.setup\_db.bootstrap\_database(verbose, source\_sql).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L5389) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1004) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1145)

<a id="op-2e2153afd4958b"></a>
### Drop user and database

`operation_foundation_database_initialize_business_behavior_drop_user_and_database`

**Inputs** db\_name, db\_user.

**Explicit results** Platform.database.mariadb.setup\_db.drop\_user\_and\_database(db\_name, db\_user) · Platform.database.sqlite.setup\_db.drop\_database(db\_name) · Platform.database.postgres.setup\_db.drop\_user\_and\_database(db\_name, db\_user).

**Local steps**

- Bind dependencies Platform.
- If Platform.conf.db\_type equals “mariadb”.
  - Bind dependencies Platform.database.mariadb.setup\_db.
  - Return Platform.database.mariadb.setup\_db.drop\_user\_and\_database(db\_name, db\_user).
- Otherwise.
  - If Platform.conf.db\_type equals “sqlite”.
    - Bind dependencies Platform.database.sqlite.setup\_db.
    - Return Platform.database.sqlite.setup\_db.drop\_database(db\_name).
  - Otherwise.
    - Bind dependencies Platform.database.postgres.setup\_db.
    - Return Platform.database.postgres.setup\_db.drop\_user\_and\_database(db\_name, db\_user).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L5651) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1006) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1147)

<a id="op-972a01223a2e31"></a>
### Get db

`operation_foundation_database_initialize_business_behavior_get_database`

**Inputs** socket = no value, host = no value, user = no value, password = no value, port = no value, cur\_db\_name = no value.

**Explicit results** Platform.database.postgres.database.PostgresDatabase(socket, host, user, password, …) · Platform.database.sqlite.database.SQLiteDatabase(cur\_db\_name = cur\_db\_name) · Platform.database.mariadb.mysqlclient.MariaDBDatabase(socket, host, user, password, …) · Platform.database.mariadb.database.MariaDBDatabase(socket, host, user, password, …).

**Local steps**

- Bind dependencies Platform.
- Set conf from Platform.local.conf.
- If conf.db\_type equals “postgres”.
  - Bind dependencies Platform.database.postgres.database.
  - Return Platform.database.postgres.database.PostgresDatabase(socket, host, user, password, …).
- Otherwise.
  - If conf.db\_type equals “sqlite”.
    - Bind dependencies Platform.database.sqlite.database.
    - Return Platform.database.sqlite.database.SQLiteDatabase(cur\_db\_name = cur\_db\_name).
  - Otherwise.
    - If conf.get(“use\_mysqlclient”, 1).
      - Bind dependencies Platform.database.mariadb.mysqlclient.
      - Return Platform.database.mariadb.mysqlclient.MariaDBDatabase(socket, host, user, password, …).
    - Otherwise.
      - Bind dependencies Platform.database.mariadb.database.
      - Return Platform.database.mariadb.database.MariaDBDatabase(socket, host, user, password, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L5903) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1008) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1149)
