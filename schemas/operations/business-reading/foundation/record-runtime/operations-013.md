# Record lifecycle and persistence · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Data import

[Record definition](../../../../data/record-types/data_import.json)

<a id="op-d1ede0f47489f8"></a>
### Import File.initialize

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_import_file_initialize`

**Inputs** self, doctype, file, template\_options = no value, import\_type = no value, data\_import\_name (named only, default no value), reference\_doctype (named only, default no value), console (named only, default false), use\_sniffer (named only, default false), custom\_delimiters (named only, default false), delimiter\_options (named only, default no value), tree\_parent\_overrides (named only, default no value).

**Record and data access** read “File” via exists · resolve a document from “File” via get\_doc.

**Explicit failure paths** validation helper — translated “Invalid template file for import”.

**Local steps**

- Set self.doctype from doctype.
- Set self.reference\_doctype from (reference\_doctype or doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in reference\_doctype → doctype.
- Set self.tree\_parent\_overrides from mapping of cint(row) → value for tuple(row, value) drawn from (Platform.parse\_json((tree\_parent\_overrides or “{}”)) or mapping()).items().
  - Draw tuple(row, value) from (Platform.parse\_json((tree\_parent\_overrides or “{}”)) or mapping()).items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json((tree\_parent\_overrides or “{}”)) → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in tree\_parent\_overrides → “{}”.
- Set self.template\_options from (template\_options or Platform.\_dict(column\_to\_field\_map = Platform.\_dict())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in template\_options → Platform.\_dict(column\_to\_field\_map = Platform.\_dict()).
- Set self.column\_to\_field\_map from self.template\_options.column\_to\_field\_map.
- Set self.column\_to\_date\_format\_map from (self.template\_options.get(“column\_to\_date\_format\_map”) or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.template\_options.get(“column\_to\_date\_format\_map”) → Platform.\_dict().
- Set self.import\_type from import\_type.
- Bind dependencies build\_lookup\_for\_data\_import.
- Set self.value\_lookup from build\_lookup\_for\_data\_import(data\_import\_name, self.reference\_doctype).
- Set self.warnings from list().
- Set self.console from console.
- Set self.use\_sniffer from use\_sniffer.
- Set self.custom\_delimiters from custom\_delimiters.
- Set self.delimiter\_options from delimiter\_options.
- Set self.file\_doc, self.file\_path, self.google\_sheets\_url from no value.
- If isinstance(file, str).
  - If Platform.db.exists(“File”, mapping(“file\_url” → file)).
    - Set self.file\_doc from Platform.get\_doc(“File”, mapping(“file\_url” → file)).
  - Otherwise.
    - If “docs.google.com/spreadsheets” belongs to file.
      - Set self.google\_sheets\_url from file.
    - Otherwise.
      - If os.path.exists(file).
        - Set self.file\_path from file.
- If (not self.file\_doc and not self.file\_path and not self.google\_sheets\_url).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.file\_doc → not self.file\_path → not self.google\_sheets\_url.
  - Call the validation error handler Platform.throw(translated “Invalid template file for import”).
- Set self.raw\_data from self.get\_data\_from\_template\_file().
- Evaluate self.parse\_data\_from\_template().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get data from template file](operations-013.md#op-99c3308f42628f), [parse data from template](operations-013.md#op-515adbcf63188e).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L37) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1233) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1226)

<a id="op-99c3308f42628f"></a>
### Import File.get data from template file

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_import_file_get_data_from_template_file`

**Inputs** self.

**Explicit results** self.read\_content(content, extension).

**Explicit failure paths** validation helper — translated “Invalid or corrupted content for import”.

**Local steps**

- Set content from no value.
- Set extension from no value.
- If self.file\_doc.
  - Set parts from self.file\_doc.get\_extension().
  - Set extension from parts at 1.
  - Set content from self.file\_doc.get\_content().
  - Set extension from extension.lstrip(“.”).
- Otherwise.
  - If self.file\_path.
    - Set tuple(content, extension) from self.read\_file(self.file\_path).
  - Otherwise.
    - If self.google\_sheets\_url.
      - Set content from get\_csv\_content\_from\_google\_sheets(self.google\_sheets\_url).
      - Set extension from “csv”.
- If not content.
  - Call the validation error handler Platform.throw(translated “Invalid or corrupted content for import”).
- If not extension.
  - Set extension from “csv”.
- If content.
  - Return self.read\_content(content, extension).

If control reaches the end, it returns no value.

**Methods declared on this owner** [read file](operations-013.md#op-3e01086656ce87), [read content](operations-013.md#op-0b22765db707b8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L1836) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1229) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1222)

<a id="op-515adbcf63188e"></a>
### Import File.parse data from template

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_import_file_parse_data_from_template`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Import template should contain a Header and atleast one row.”.

**Local steps**

- Set header from no value.
- Set data from list().
- For each tuple(i, row) in enumerate(self.raw\_data).
  - If all(generator of v belongs to INVALID\_VALUES for v drawn from row).
    - Draw v from row.
    - Continue with the next iteration or loop test.
  - If not header.
    - Set header from Header(i, row, self.doctype, self.raw\_data at slice (i + 1) to no value, …).
  - Otherwise.
    - Set row\_obj from Row(i, row, self.doctype, header, …).
    - Evaluate data.append(row\_obj).
- Set self.header from header.
- Set self.columns from self.header.columns.
- Set self.data from data.
- Set meta from Platform.get\_meta(self.doctype).
- Set self.header.id\_fieldname from \_get\_id\_fieldname\_from\_meta(meta).
- Set self.header.tree\_alias\_field from \_get\_tree\_alias\_field\_from\_meta(meta).
- Set tuple(self.header.import\_ids, self.header.import\_aliases) from \_build\_import\_reference\_sets(self, self.header.id\_fieldname, self.header.tree\_alias\_field).
- Set self.header.import\_refs from (self.header.import\_ids bitwise or self.header.import\_aliases).
- Evaluate self.\_refresh\_self\_referential\_link\_validation().
- Evaluate self.\_\_dict\_\_.pop(“\_tree\_preview\_cache”, no value).
- If len(data) &lt; 1.
  - Call the validation error handler Platform.throw(translated “Import template should contain a Header and atleast one row.”, title = translated “Template Error”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [refresh self referential link validation](operations-013.md#op-a372729cbd5f63).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L38) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1234) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1227)

<a id="op-a372729cbd5f63"></a>
### Import File.refresh self referential link validation

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_import_file_refresh_self_referential_link_validation`

**Inputs** self.

**Local steps**

- Bind dependencies warn\_invalid\_link\_select\_values.
- Set alias\_field from self.header.tree\_alias\_field.
- If alias\_field.
  - Set link\_values from set().
  - For each col in self.header.columns.
    - If (not col.df or col.skip\_import or col.df.fieldtype differs from “Link”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not col.df → col.skip\_import → col.df.fieldtype differs from “Link”.
      - Continue with the next iteration or loop test.
    - If col.df.options differs from self.doctype.
      - Continue with the next iteration or loop test.
    - For each value in col.column\_values.
      - If value does not belong to INVALID\_VALUES.
        - Evaluate link\_values.add(cstr(value).strip()).
  - If link\_values.
    - Update self.header.import\_refs using bitwise or \_get\_existing\_tree\_parent\_refs(self.doctype, link\_values, alias\_field).
- For each col in self.header.columns.
  - If (not col.df or col.skip\_import or col.df.fieldtype differs from “Link”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not col.df → col.skip\_import → col.df.fieldtype differs from “Link”.
    - Continue with the next iteration or loop test.
  - If col.df.options differs from self.doctype.
    - Continue with the next iteration or loop test.
  - Set col.import\_refs from self.header.import\_refs.
  - Set col.invalid\_value\_items from no value.
  - Set col.warnings from list of w for w drawn from col.warnings where w.get(“type”) differs from “value\_mapping”.
    - Draw w from col.warnings, keep a combination only if (w.get(“type”) differs from “value\_mapping”).
  - Evaluate warn\_invalid\_link\_select\_values(col).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L3010) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1238) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1231)

<a id="op-93b48a1e2292e0"></a>
### Import File.get data for import preview

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_import_file_get_data_for_import_preview`

**Inputs** self.

**Explicit results** out.

**Local steps**

- Set columns from list(Platform.\_dict(mapping(“header\_title” → translated “Sr. No”, “skip\_import” → true))).
- Update columns using + list of col.as\_dict() for col drawn from self.columns.
  - Draw col from self.columns.
- For each col in columns.
  - If col.df.
    - Set col.df from mapping(“fieldtype” → col.df.fieldtype, “fieldname” → col.df.fieldname, “label” → col.df.label, “options” → col.df.options, …).
- Set data from list of list(row.row\_number, expanded row.as\_list()) for row drawn from self.data.
  - Draw row from self.data.
- Set tree\_preview from self.get\_tree\_preview().
- Set out from Platform.\_dict().
- Set out.data from data.
- Set out.columns from columns.
- Set out.warnings from self.get\_warnings().
- If tree\_preview.
  - Set out.tree\_preview from tree\_preview.
  - Update out.warnings using + tree\_preview.tree\_warnings.
- Set total\_number\_of\_rows from len(out.data).
- Set out.total\_number\_of\_rows from total\_number\_of\_rows.
- If total\_number\_of\_rows &gt; MAX\_ROWS\_IN\_PREVIEW.
  - Set out.data from out.data at slice no value to MAX\_ROWS\_IN\_PREVIEW.
  - Set out.max\_rows\_exceeded from true.
  - Set out.max\_rows\_in\_preview from MAX\_ROWS\_IN\_PREVIEW.
  - Set warned from set of cint(w.get(“row”)) for w drawn from out.warnings where w.get(“row”).
    - Draw w from out.warnings, keep a combination only if (w.get(“row”)).
  - Set out.warning\_rows from list of row for row drawn from data at slice MAX\_ROWS\_IN\_PREVIEW to no value where row at 0 belongs to warned.
    - Draw row from data at slice MAX\_ROWS\_IN\_PREVIEW to no value, keep a combination only if (row at 0 belongs to warned).
- Return out.

**Methods declared on this owner** [get tree preview](operations-013.md#op-6ae13a80037fd8), [get warnings](operations-013.md#op-9d9458ef776c6d).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L34) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1228) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1221)

<a id="op-aedf0c394f3f3a"></a>
### Import File.get payloads for import

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_import_file_get_payloads_for_import`

**Inputs** self.

**Explicit results** sort\_tree\_payloads(payloads, self.doctype, self.import\_type).

**Local steps**

- Evaluate self.apply\_tree\_overrides().
- Set payloads from list().
- Set data from list(self.data).
- While data.
  - Set tuple(doc, rows, data) from self.parse\_next\_row\_for\_import(data).
  - Evaluate payloads.append(Platform.\_dict(doc = doc, rows = rows)).
- Return sort\_tree\_payloads(payloads, self.doctype, self.import\_type).

**Methods declared on this owner** [apply tree overrides](operations-013.md#op-7a41ef32f17e31), [parse next row for import](operations-013.md#op-c8107d761fa63d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L35) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1230) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1223)

<a id="op-7a41ef32f17e31"></a>
### Import File.apply tree overrides

`operation_foundation_binding_foundation_core_doctype_data_import_importer_importfile_apply_tree_overrides`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set overrides from self.tree\_parent\_overrides.
- If not overrides.
  - Return no value.
- Set tuple(\_parent\_field, parent\_column, \_is\_group\_field, is\_group\_column) from \_get\_tree\_columns(self).
- Bind local operation set\_cell for subsequent calls.
- For each row in self.data.
  - Set override from overrides.get(row.row\_number).
  - If not override.
    - Continue with the next iteration or loop test.
  - If “parent” belongs to override.
    - Evaluate set\_cell(row, parent\_column, override.get(“parent”)).
  - If “is\_group” belongs to override.
    - Evaluate set\_cell(row, is\_group\_column, cint(override.get(“is\_group”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L157) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L639) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L615)

<a id="op-b22c0b13467334"></a>
### Import File.apply tree overrides.set cell

`operation_foundation_binding_foundation_core_doctype_data_import_importer_importfile_apply_tree_overrides_set_cell`

**Inputs** row, column, value.

**Explicit results** no value.

**Local steps**

- If not column.
  - Return no value.
- While len(row.data) ≤ column.index.
  - Evaluate row.data.append(no value).
- Set row.data at column.index from value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L158) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L640) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L616)

<a id="op-c8107d761fa63d"></a>
### Import File.parse next row for import

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_import_file_parse_next_row_for_import`

**Inputs** self, data.

**Explicit results** tuple(doc, rows, data at slice len(rows) to no value).

**Local steps**

- Set doctypes from self.header.doctypes.
- Set first\_row from data at 0.
- Set rows from list(first\_row).
- If len(doctypes) &gt; 1.
  - Set parent\_column\_indexes from self.header.get\_column\_indexes(self.doctype).
  - Set data\_without\_first\_row from data at slice 1 to no value.
  - For each row in data\_without\_first\_row.
    - Set row\_values from row.get\_values(parent\_column\_indexes).
    - If all(generator of v belongs to INVALID\_VALUES for v drawn from row\_values).
      - Draw v from row\_values.
      - Evaluate rows.append(row).
      - Continue with the next iteration or loop test.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Set parent\_doc from no value.
- For each row in rows.
  - For each tuple(doctype, table\_df) in doctypes.
    - If (doctype equals self.doctype and not parent\_doc).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals self.doctype → not parent\_doc.
      - Set parent\_doc from row.parse\_doc(doctype).
    - If (doctype differs from self.doctype and table\_df).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype differs from self.doctype → table\_df.
      - Set child\_doc from row.parse\_doc(doctype, parent\_doc, table\_df).
      - If child\_doc is identical to no value.
        - Continue with the next iteration or loop test.
      - If parent\_doc is identical to no value.
        - Set parent\_doc from row.\_parse\_doc(self.doctype, list(), list()).
      - Set parent\_doc at table\_df.fieldname from parent\_doc.get(table\_df.fieldname, list()).
      - Evaluate parent\_doc at table\_df.fieldname.append(child\_doc).
- Set doc from parent\_doc.
- Return tuple(doc, rows, data at slice len(rows) to no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L39) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1235) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1228)

<a id="op-9d9458ef776c6d"></a>
### Import File.get warnings

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_import_file_get_warnings`

**Inputs** self.

**Explicit results** warnings.

**Local steps**

- Set warnings from list().
- Update warnings using + self.warnings.
- For each col in self.header.columns.
  - Update warnings using + col.warnings.
- For each row in self.data.
  - Update warnings using + row.warnings.
- Update warnings using + self.\_get\_provider\_warnings().
- Return warnings.

**Methods declared on this owner** [get provider warnings](operations-013.md#op-4fb6c928740cda).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L36) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1232) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1225)

<a id="op-4fb6c928740cda"></a>
### Import File.get provider warnings

`operation_foundation_binding_foundation_core_doctype_data_import_importer_importfile_get_provider_warnings`

**Inputs** self.

**Explicit results** self.\_provider\_warnings.

**Local steps**

- If “\_provider\_warnings” does not belong to self.\_\_dict\_\_.
  - Bind dependencies get\_import\_provider.
  - Set provider from get\_import\_provider(self.reference\_doctype).
  - Set warnings from (provider.validate(self) or list()) when provider, otherwise list().
    - Value choice on provider — true gives (provider.validate(self) or list()), false gives list().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in provider.validate(self) → list().
  - For each warning in warnings.
    - Set warning at “message” from clean\_html(cstr(warning.get(“message”))).
  - Set self.\_provider\_warnings from warnings.
- Return self.\_provider\_warnings.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L159) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L641) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L617)

<a id="op-d2a2e1b76294f7"></a>
### Import File.get all warnings

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_import_file_get_all_warnings`

**Inputs** self.

**Explicit results** warnings.

**Local steps**

- Set warnings from self.get\_warnings().
- Set tree\_preview from self.get\_tree\_preview().
- If tree\_preview.
  - Update warnings using + tree\_preview.tree\_warnings.
- Return warnings.

**Methods declared on this owner** [get warnings](operations-013.md#op-9d9458ef776c6d), [get tree preview](operations-013.md#op-6ae13a80037fd8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L5535) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1227) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1220)

<a id="op-6ae13a80037fd8"></a>
### Import File.get tree preview

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_import_file_get_tree_preview`

**Inputs** self.

**Explicit results** self.\_tree\_preview\_cache.

**Local steps**

- If “\_tree\_preview\_cache” does not belong to self.\_\_dict\_\_.
  - Set self.\_tree\_preview\_cache from build\_tree\_preview(self).
- Return self.\_tree\_preview\_cache.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L5651) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1231) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1224)

<a id="op-3e01086656ce87"></a>
### Import File.read file

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_import_file_read_file`

**Inputs** self, file\_path.

**Record and data access** read “File” via get\_value · resolve a document from “File” via get\_doc.

**Explicit results** tuple(file\_content, extn).

**Local steps**

- Set extn from os.path.splitext(file\_path) at 1 at slice 1 to no value.
- Set file\_content from no value.
- If self.console.
  - Set file\_content from Platform.read\_file(file\_path, true).
  - Return tuple(file\_content, extn).
- Set file\_name from Platform.db.get\_value(“File”, mapping(“file\_url” → file\_path)).
- If file\_name.
  - Set file from Platform.get\_doc(“File”, file\_name).
  - Set file\_content from file.get\_content().
- Return tuple(file\_content, extn).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L5750) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1237) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1230)

<a id="op-0b22765db707b8"></a>
### Import File.read content

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_import_file_read_content`

**Inputs** self, content, extension.

**Explicit results** data.

**Explicit failure paths** validation helper — translated “Import template should be of type .csv, .xlsx or .xls”.

**Local steps**

- Set error\_title from translated “Template Error”.
- If extension does not belong to tuple(“csv”, “xlsx”, “xls”).
  - Call the validation error handler Platform.throw(translated “Import template should be of type .csv, .xlsx or .xls”, title = error\_title).
- If extension equals “csv”.
  - Set data from read\_csv\_content(content, use\_sniffer = self.use\_sniffer, delimiter = \_get\_fixed\_csv\_delimiter(self.custom\_delimiters, self.delimiter\_options)).
- Otherwise.
  - If extension equals “xlsx”.
    - Set data from read\_xlsx\_file\_from\_attached\_file(fcontent = content, read\_only = true).
  - Otherwise.
    - If extension equals “xls”.
      - Set data from read\_xls\_file\_from\_attached\_file(content).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L6071) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1236) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1229)

<a id="op-91a8d365b7ff5a"></a>
### Get value row map

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_value_row_map`

**Inputs** column\_values, value\_row\_numbers.

**Explicit results** mapping of value → sorted(rows) for tuple(value, rows) drawn from value\_rows.items().

**Local steps**

- Set value\_rows from mapping().
- For each tuple(value, row\_number) in zip(column\_values, value\_row\_numbers, strict = false).
  - If value belongs to INVALID\_VALUES.
    - Continue with the next iteration or loop test.
  - Evaluate value\_rows.setdefault(cstr(value), set()).add(row\_number).
- Return mapping of value → sorted(rows) for tuple(value, rows) drawn from value\_rows.items().
  - Draw tuple(value, rows) from value\_rows.items().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L32) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1221) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1214)

<a id="op-af09cb900813c0"></a>
### Format row numbers for warning

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_format_row_numbers_for_warning`

**Inputs** rows, max\_shown = 6.

**Declared result** str.

**Explicit results** “, ”.join(generator of str(r) for r drawn from rows) · formatted text {“, ”.join(generator of str(r) for r drawn from rows at slice no value to max\_shown)}, ... {rows at negative 1}.

**Local steps**

- If len(rows) ≤ max\_shown.
  - Return “, ”.join(generator of str(r) for r drawn from rows).
    - Draw r from rows.
- Return formatted text {“, ”.join(generator of str(r) for r drawn from rows at slice no value to max\_shown)}, ... {rows at negative 1}.
  - Draw r from rows at slice no value to max\_shown.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L6741) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1205) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1199)

<a id="op-c0d09aecc3f861"></a>
### Get id fieldname from meta

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_identifier_fieldname_from_meta`

**Inputs** meta.

**Declared result** str.

**Explicit results** meta.autoname at slice 6 to no value · “name”.

**Local steps**

- If (meta.autoname and meta.autoname.startswith(“field:”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.autoname → meta.autoname.startswith(“field:”).
  - Return meta.autoname at slice 6 to no value.
- Return “name”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L6987) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1212) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1205)

<a id="op-b9f7ef68f55d4b"></a>
### Get tree alias field from meta

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_tree_alias_field_from_meta`

**Inputs** meta.

**Declared result** (str bitwise or no value).

**Explicit results** no value · meta.title\_field · field.fieldname.

**Local steps**

- If not meta.is\_nested\_set().
  - Return no value.
- If (meta.autoname and meta.autoname.startswith(“field:”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.autoname → meta.autoname.startswith(“field:”).
  - Return no value.
- If (meta.title\_field and meta.title\_field differs from \_get\_id\_fieldname\_from\_meta(meta)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.title\_field → meta.title\_field differs from \_get\_id\_fieldname\_from\_meta(meta).
  - Return meta.title\_field.
- For each field in meta.fields.
  - If (field.fieldtype equals “Data” and field.reqd).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype equals “Data” → field.reqd.
    - Return field.fieldname.
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L31) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1216) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1209)

<a id="op-40a8e3175b269a"></a>
### Get tree alias fieldname

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_tree_alias_fieldname`

**Inputs** doctype.

**Explicit results** \_get\_tree\_alias\_field\_from\_meta(Platform.get\_meta(doctype)).

**Local steps**

- Return \_get\_tree\_alias\_field\_from\_meta(Platform.get\_meta(doctype)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L7289) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1217) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1210)

<a id="op-6610e8daa539f4"></a>
### Uses tree alias references

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_uses_tree_alias_references`

**Inputs** doctype.

**Explicit results** bool(get\_tree\_alias\_fieldname(doctype)).

**Local steps**

- Return bool(get\_tree\_alias\_fieldname(doctype)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L7358) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1272) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1264)

<a id="op-0616a884205160"></a>
### Get tree node key

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_tree_runtime_process_key`

**Inputs** doc, id\_fieldname, alias\_field = no value.

**Explicit results** cstr(node\_id).strip() · cstr(alias).strip() · no value.

**Local steps**

- Set node\_id from doc.get(id\_fieldname).
- If node\_id does not belong to INVALID\_VALUES.
  - Return cstr(node\_id).strip().
- If alias\_field.
  - Set alias from doc.get(alias\_field).
  - If alias does not belong to INVALID\_VALUES.
    - Return cstr(alias).strip().
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L7423) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1219) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1212)

<a id="op-8f60b426f938cb"></a>
### Is same file tree reference

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_is_same_file_tree_reference`

**Inputs** value, header.

**Declared result** bool.

**Explicit results** bool((import\_refs and cstr(value).strip() belongs to import\_refs)).

**Local steps**

- Set import\_refs from getattr(header, “import\_refs”, no value).
- Return bool((import\_refs and cstr(value).strip() belongs to import\_refs)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in import\_refs → cstr(value).strip() belongs to import\_refs.

**Values supplied outside this operation** selected callable from getattr(header, “import\_refs”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L7651) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1258) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1251)

<a id="op-8212ac43fd8c8b"></a>
### Get import column index

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_import_column_index`

**Inputs** columns, fieldname.

**Explicit results** column.index when column, otherwise no value.

**Local steps**

- Set column from next(generator of col for col drawn from columns where (col.df and col.df.fieldname equals fieldname and not col.skip\_import), no value).
  - Draw col from columns, keep a combination only if ((col.df and col.df.fieldname equals fieldname and not col.skip\_import)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.df → col.df.fieldname equals fieldname → not col.skip\_import.
- Return column.index when column, otherwise no value.
  - Value choice on column — true gives column.index, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L7790) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1213) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1206)
