# Record lifecycle and persistence · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Data import

[Record definition](../../../../data/record-types/data_import.json)

<a id="op-f88eb4157ebfbb"></a>
### Get export filters

`operation_foundation_binding_foundation_core_doctype_data_import_exporter_get_export_filters`

**Inputs** doctype, filters = no value.

**Explicit results** filters · list(expanded (filters or list()), list(“owner”, “=”, Platform.session.user)).

**Local steps**

- If Platform.permissions.can\_export(doctype).
  - Return filters.
- Evaluate Platform.permissions.can\_export(doctype, raise\_exception = true, is\_owner = true).
- Set filters from Platform.parse\_json(filters).
- If isinstance(filters, dict).
  - Set filters from list of make\_filter\_tuple(doctype, k, v) for tuple(k, v) drawn from filters.items().
    - Draw tuple(k, v) from filters.items().
- Return list(expanded (filters or list()), list(“owner”, “=”, Platform.session.user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → list().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L143) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L625) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L601)

<a id="op-9d57fb54cf1135"></a>
### Exporter.initialize

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_initialize`

**Inputs** self, doctype, export\_fields = no value, export\_data = false, export\_filters = no value, export\_page\_length = no value, file\_type = “CSV”, order\_by = no value.

**Local steps**

- Set self.doctype from doctype.
- Set self.meta from Platform.get\_meta(doctype).
- Set self.export\_fields from export\_fields.
- Set self.export\_filters from export\_filters.
- Set self.export\_page\_length from export\_page\_length.
- Set self.file\_type from file\_type.
- Set self.order\_by from order\_by.
- Set self.csv\_array from list().
- Set self.provider from self.get\_import\_provider().
- Set self.provider\_tables from self.get\_provider\_tables().
- Set self.exportable\_fields from self.get\_all\_exportable\_fields().
- Set self.fields from self.serialize\_exportable\_fields().
- Evaluate self.add\_header().
- If export\_data.
  - Set self.data from self.get\_data\_to\_export().
- Otherwise.
  - Set self.data from list().
- Evaluate self.add\_data().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get import provider](operations-011.md#op-65b56e331a35d2), [get provider tables](operations-011.md#op-c54ab7f317ed85), [get all exportable fields](operations-011.md#op-d38dcfe0419b26), [serialize exportable fields](operations-011.md#op-6ef491e089cd23), [add header](operations-011.md#op-b81861a01b4670), [get data to export](operations-011.md#op-0ab30dfbcfe89d), [add data](operations-011.md#op-4233350c553722).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L19) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1189) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1183)

<a id="op-65b56e331a35d2"></a>
### Exporter.get import provider

`operation_foundation_binding_foundation_core_doctype_data_import_exporter_exporter_get_import_provider`

**Inputs** self.

**Explicit results** get\_import\_provider(self.doctype).

**Local steps**

- Bind dependencies get\_import\_provider.
- Return get\_import\_provider(self.doctype).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L140) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L622) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L598)

<a id="op-c54ab7f317ed85"></a>
### Exporter.get provider tables

`operation_foundation_binding_foundation_core_doctype_data_import_exporter_exporter_get_provider_tables`

**Inputs** self.

**Explicit results** mapping of table at “fieldname” → table for table drawn from ((schema or mapping()).get(“child\_tables”) or list()) where not self.meta.get\_field(table at “fieldname”).

**Local steps**

- Set schema from self.provider.get\_import\_fields() when self.provider, otherwise no value.
  - Value choice on self.provider — true gives self.provider.get\_import\_fields(), false gives no value.
- Return mapping of table at “fieldname” → table for table drawn from ((schema or mapping()).get(“child\_tables”) or list()) where not self.meta.get\_field(table at “fieldname”).
  - Draw table from ((schema or mapping()).get(“child\_tables”) or list()), keep a combination only if (not self.meta.get\_field(table at “fieldname”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (schema or mapping()).get(“child\_tables”) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in schema → mapping().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L142) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L624) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L600)

<a id="op-d38dcfe0419b26"></a>
### Exporter.get all exportable fields

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_get_all_exportable_fields`

**Inputs** self.

**Explicit results** exportable\_fields.

**Local steps**

- Set permitted\_levels from set(self.meta.get\_permlevel\_access(“read”)).
- Set child\_table\_fields from list of df.fieldname for df drawn from self.meta.fields where (df.fieldtype belongs to table\_fieldtypes and (not nested operand in the contract.meta.get\_permissions() or df.permlevel belongs to permitted\_levels)).
  - Draw df from self.meta.fields, keep a combination only if ((df.fieldtype belongs to table\_fieldtypes and (not self.meta.get\_permissions() or df.permlevel belongs to permitted\_levels))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype belongs to table\_fieldtypes → (not self.meta.get\_permissions() or df.permlevel belongs to permitted\_levels).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.meta.get\_permissions() → df.permlevel belongs to permitted\_levels.
- Set meta from Platform.get\_meta(self.doctype).
- Set exportable\_fields from Platform.\_dict(mapping()).
- For each tuple(key, fieldnames) in self.export\_fields.items().
  - If key equals self.doctype.
    - Set exportable\_fields at key from self.get\_exportable\_fields(key, fieldnames).
  - Otherwise.
    - If key belongs to child\_table\_fields.
      - Set child\_df from meta.get\_field(key).
      - Set child\_doctype from child\_df.options.
      - Set exportable\_fields at key from self.get\_exportable\_fields(child\_doctype, fieldnames).
    - Otherwise.
      - If key belongs to self.provider\_tables.
        - Set exportable\_fields at key from list of Platform.\_dict(df) for df drawn from self.provider\_tables at key at “fields” where (df at “fieldname” belongs to fieldnames and df.get(“fieldtype”) does not belong to (display\_fieldtypes + no\_value\_fields)).
          - Draw df from self.provider\_tables at key at “fields”, keep a combination only if ((df at “fieldname” belongs to fieldnames and df.get(“fieldtype”) does not belong to (display\_fieldtypes + no\_value\_fields))).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in df at “fieldname” belongs to fieldnames → df.get(“fieldtype”) does not belong to (display\_fieldtypes + no\_value\_fields).
- Return exportable\_fields.

**Methods declared on this owner** [get exportable fields](operations-011.md#op-2a05d90b19eaff).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L16) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1180) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1174)

<a id="op-6ef491e089cd23"></a>
### Exporter.serialize exportable fields

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_serialize_exportable_fields`

**Inputs** self.

**Explicit results** fields.

**Local steps**

- Set fields from list().
- For each tuple(key, exportable\_fields) in self.exportable\_fields.items().
  - For each \_df in exportable\_fields.
    - If isinstance(\_df, Platform.core.doctype.docfield.docfield.DocField).
      - Set df from \_df.as\_dict().
    - Otherwise.
      - Set df from \_df.copy().
    - Set df.is\_child\_table\_field from key differs from self.doctype.
    - If df.is\_child\_table\_field.
      - Set df.child\_table\_df from (self.meta.get\_field(key) or Platform.\_dict(fieldname = key, label = self.provider\_tables at key.get(“label”))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.meta.get\_field(key) → Platform.\_dict(fieldname = key, label = self.provider\_tables at key.get(“label”)).
    - Evaluate fields.append(df).
- Return fields.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L20) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1190) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1184)

<a id="op-2a05d90b19eaff"></a>
### Exporter.get exportable fields

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_get_exportable_fields`

**Inputs** self, doctype, fieldnames.

**Explicit results** (fields or list()).

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set permitted\_fields from set(get\_permitted\_fields(doctype, parenttype = self.doctype when meta.istable, otherwise no value)).
  - Value choice on meta.istable — true gives self.doctype, false gives no value.
- Bind local operation is\_exportable for subsequent calls.
- Set name\_field from Platform.\_dict(mapping(“fieldtype” → “Data”, “fieldname” → “name”, “label” → “ID”, “reqd” → 1, …)).
- Set fields from list of meta.get\_field(fieldname) for fieldname drawn from fieldnames where fieldname belongs to permitted\_fields.
  - Draw fieldname from fieldnames, keep a combination only if (fieldname belongs to permitted\_fields).
- Set fields from list of df for df drawn from fields where is\_exportable(df).
  - Draw df from fields, keep a combination only if (is\_exportable(df)).
- If “name” belongs to fieldnames.
  - Set fields from list(name\_field, expanded fields).
- Return (fields or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fields → list().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L7180) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1186) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1180)

<a id="op-c566aa1697c34f"></a>
### Exporter.get exportable fields.is exportable

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_get_exportable_fields_is_exportable`

**Inputs** df.

**Explicit results** (df and df.fieldtype does not belong to (display\_fieldtypes + no\_value\_fields)).

**Local steps**

- Return (df and df.fieldtype does not belong to (display\_fieldtypes + no\_value\_fields)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype does not belong to (display\_fieldtypes + no\_value\_fields).

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L7679) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1187) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1181)

<a id="op-0ab30dfbcfe89d"></a>
### Exporter.get data to export

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_get_data_to_export`

**Inputs** self.

**Local steps**

- Set table\_fields from list of f for f drawn from self.exportable\_fields where f differs from self.doctype.
  - Draw f from self.exportable\_fields, keep a combination only if (f differs from self.doctype).
- For each doc in self.get\_data\_as\_docs().
  - Set rows from list().
  - Set rows from self.add\_data\_row(no value, doc, rows, 0).
  - For each f in table\_fields.
    - For each tuple(i, child\_row) in enumerate((doc.get(f) or list())).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(f) → list().
      - Set rows from self.add\_data\_row(f, child\_row, rows, i).
  - yield values from rows.

On ordinary fall-through the sequence ends.

**Methods declared on this owner** [get data as docs](operations-011.md#op-4f3c09643b5f0d), [add data row](operations-011.md#op-c5d155ea6f5c84).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L18) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1185) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1179)

<a id="op-c5d155ea6f5c84"></a>
### Exporter.add data row

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_add_data_row`

**Inputs** self, table\_fieldname, doc, rows, row\_idx.

**Explicit results** rows.

**Local steps**

- If len(rows) &lt; (row\_idx + 1).
  - Evaluate rows.append((list(empty text) × len(self.fields))).
- Set row from rows at row\_idx.
- For each tuple(i, df) in enumerate(self.fields).
  - If df.is\_child\_table\_field.
    - If df.child\_table\_df.fieldname differs from table\_fieldname.
      - Continue with the next iteration or loop test.
  - Otherwise.
    - If table\_fieldname.
      - Continue with the next iteration or loop test.
  - Set value from doc.get(df.fieldname, no value).
  - If df.fieldtype equals “Duration”.
    - Set value from format\_duration(flt(value), df.hide\_days).
  - If (df.fieldtype equals “Text Editor” and value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Text Editor” → value.
    - Set value from Platform.core.utils.html2text(value).
  - Set row at i from value.
- Return rows.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L14) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1177) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1171)

<a id="op-4f3c09643b5f0d"></a>
### Exporter.get data as docs

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_get_data_as_records`

**Inputs** self.

**Record and data access** read self.doctype via get\_list · read child\_table\_doctype via get\_list.

**Local steps**

- Bind local operation format\_column\_name for subsequent calls.
- Set filters from get\_export\_filters(self.doctype, self.export\_filters).
- If self.meta.is\_nested\_set().
  - Set order\_by from “lft ASC”.
- Otherwise.
  - If self.order\_by.
    - Set order\_by from self.order\_by.
  - Otherwise.
    - Set order\_by from “creation DESC”.
- Set parent\_fields from list of format\_column\_name(df) for df drawn from self.fields where df.parent equals self.doctype.
  - Draw df from self.fields, keep a combination only if (df.parent equals self.doctype).
- Set parent\_data from Platform.db.get\_list(self.doctype, filters = filters, fields = list(“name”, “owner”, expanded parent\_fields), limit\_page\_length = self.export\_page\_length, order\_by = order\_by, …).
- Set parent\_names from list of p.name for p drawn from parent\_data.
  - Draw p from parent\_data.
- Set child\_data from mapping().
- For each key in self.exportable\_fields.
  - If (key equals self.doctype or key belongs to self.provider\_tables).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in key equals self.doctype → key belongs to self.provider\_tables.
    - Continue with the next iteration or loop test.
  - Set child\_table\_df from self.meta.get\_field(key).
  - Set child\_table\_doctype from child\_table\_df.options.
  - Set child\_fields from list(“name”, “idx”, “parent”, “parentfield”, …).
    - Draw df from self.fields, keep a combination only if (df.parent equals child\_table\_doctype).
  - Set data from Platform.get\_list(child\_table\_doctype, parent\_doctype = self.doctype, filters = mapping(“parent” → tuple(“in”, parent\_names), “parentfield” → child\_table\_df.fieldname, “parenttype” → self.doctype), fields  ….
  - Set child\_data at key from data.
- Set grouped\_children\_data from self.group\_children\_data\_by\_parent(child\_data).
- Set provider\_rows from self.get\_provider\_rows(parent\_names).
- For each doc in parent\_data.
  - Set related\_children\_docs from grouped\_children\_data.get(str(doc.name), mapping()).
  - yield mapping(expand doc, expand related\_children\_docs, expand provider\_rows.get(doc.name, mapping())).

On ordinary fall-through the sequence ends.

**Methods declared on this owner** [group children data by parent](operations-011.md#op-3dac9c1907bd82), [get provider rows](operations-011.md#op-9e558a71fbb3c7).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L17) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1183) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1177)

<a id="op-a6b15e80326c58"></a>
### Exporter.get data as docs.format column name

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_get_data_as_records_format_column_name`

**Inputs** df.

**Explicit results** formatted text ′tab{df.parent}′.′{df.fieldname}′.

**Local steps**

- Return formatted text ′tab{df.parent}′.′{df.fieldname}′.

[Applicable decision contract](../../../foundation-decision-contracts/part-0051.json#L2204) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1184) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1178)

<a id="op-9e558a71fbb3c7"></a>
### Exporter.get provider rows

`operation_foundation_binding_foundation_core_doctype_data_import_exporter_exporter_get_provider_rows`

**Inputs** self, parent\_names.

**Explicit results** mapping() · (self.provider.get\_export\_rows(parent\_names, tables) or mapping()).

**Local steps**

- Set tables from mapping of key → list of df.fieldname for df drawn from fields for tuple(key, fields) drawn from self.exportable\_fields.items() where (key belongs to self.provider\_tables and fields).
  - Draw tuple(key, fields) from self.exportable\_fields.items(), keep a combination only if ((key belongs to self.provider\_tables and fields)).
  - Draw df from fields.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in key belongs to self.provider\_tables → fields.
- If not (parent\_names and tables).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_names → tables.
  - Return mapping().
- Return (self.provider.get\_export\_rows(parent\_names, tables) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.provider.get\_export\_rows(parent\_names, tables) → mapping().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L141) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L623) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L599)

<a id="op-b81861a01b4670"></a>
### Exporter.add header

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_add_header`

**Inputs** self.

**Local steps**

- Set header from list().
- For each df in self.fields.
  - Set is\_parent from not df.is\_child\_table\_field.
  - If is\_parent.
    - Set label from translated (df.label or df.fieldname).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label → df.fieldname.
  - Otherwise.
    - Set label from formatted text {translated (df.label or df.fieldname)} ({translated (df.child\_table\_df.label or df.child\_table\_df.fieldname)}).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label → df.fieldname.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.child\_table\_df.label → df.child\_table\_df.fieldname.
  - If label belongs to header.
    - If is\_parent.
      - Set label from formatted text {df.fieldname}.
    - Otherwise.
      - Set label from formatted text {df.child\_table\_df.fieldname}.{df.fieldname}.
  - Evaluate header.append(label).
- Evaluate self.csv\_array.append(header).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L15) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1178) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1172)

<a id="op-4233350c553722"></a>
### Exporter.add data

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_add_data`

**Inputs** self.

**Local steps**

- Update self.csv\_array using + self.data.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0051.json#L2756) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1176) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1170)

<a id="op-69b628504ff8ec"></a>
### Exporter.get csv array

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_get_comma_separated_values_array`

**Inputs** self.

**Explicit results** self.csv\_array.

**Local steps**

- Return self.csv\_array.

[Applicable decision contract](../../../foundation-decision-contracts/part-0051.json#L2806) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1181) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1175)

<a id="op-01240c8a03f6f1"></a>
### Exporter.get csv array for export

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_get_comma_separated_values_array_for_export`

**Inputs** self.

**Explicit results** csv\_array.

**Local steps**

- Set csv\_array from self.csv\_array.
- If not self.data.
  - Update csv\_array using + (list(list()) × 2).
- Return csv\_array.

[Applicable decision contract](../../../foundation-decision-contracts/part-0051.json#L2847) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1182) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1176)

<a id="op-7946de329ef9c5"></a>
### Exporter.build response

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_build_response`

**Inputs** self.

**Local steps**

- If self.file\_type equals “CSV”.
  - Evaluate build\_csv\_response(self.get\_csv\_array\_for\_export(), translated self.doctype).
- Otherwise.
  - If self.file\_type equals “Excel”.
    - Set data from self.get\_csv\_array\_for\_export().
    - Set styles from get\_default\_xlsx\_styles(columns = self.fields, data = data at slice 1 to no value, currency\_formatting = false).
    - Evaluate build\_xlsx\_response(data, translated self.doctype, styles = styles).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get csv array for export](operations-011.md#op-01240c8a03f6f1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0051.json#L2944) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1179) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1173)

<a id="op-3dac9c1907bd82"></a>
### Exporter.group children data by parent

`operation_foundation_core_record_definitions_data_import_exporter_business_behavior_exporter_group_children_data_by_parent`

**Inputs** self, children\_data.

**Explicit results** groupby\_metric(children\_data, key = “parent”).

**Local steps**

- Return groupby\_metric(children\_data, key = “parent”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0051.json#L3235) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1188) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1182)

<a id="op-d5efc308fc9cd2"></a>
### Import Provider.get import fields

`operation_foundation_binding_foundation_core_doctype_data_import_import_provider_importprovider_get_import_fields`

**Inputs** self.

**Declared result** (dict bitwise or no value).

**Explicit results** no value.

**Local steps**

- Return no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L146) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L628) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L604)

<a id="op-86ff504805a6f4"></a>
### Import Provider.validate

`operation_foundation_binding_foundation_core_doctype_data_import_import_provider_importprovider_validate`

**Inputs** self, import\_file.

**Declared result** list at dict.

**Explicit results** list().

**Local steps**

- Return list().

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L148) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L630) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L606)

<a id="op-eaab6381e35f1d"></a>
### Import Provider.import row

`operation_foundation_binding_foundation_core_doctype_data_import_import_provider_importprovider_import_row`

**Inputs** self, importer, doc.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L147) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L629) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L605)

<a id="op-574929f8734576"></a>
### Import Provider.get export rows

`operation_foundation_binding_foundation_core_doctype_data_import_import_provider_importprovider_get_export_rows`

**Inputs** self, names, tables.

**Declared result** dict at tuple(str, dict at tuple(str, list)).

**Explicit results** mapping().

**Local steps**

- Return mapping().

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L145) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L627) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L603)

<a id="op-f3c06514a6f37f"></a>
### Get import provider

`operation_foundation_binding_foundation_core_doctype_data_import_import_provider_get_import_provider`

**Inputs** doctype.

**Declared result** (ImportProvider bitwise or no value).

**Explicit results** no value · provider.

**Local steps**

- If not doctype.
  - Return no value.
- Set hooks from Platform.get\_hooks(“data\_import\_providers”).
- If not isinstance(hooks, dict).
  - Return no value.
- Set paths from hooks.get(doctype).
- If not paths.
  - Return no value.
- Set provider from Platform.get\_attr(paths at negative 1 when isinstance(paths, (list bitwise or tuple)), otherwise paths)().
  - Value choice on isinstance(paths, (list bitwise or tuple)) — true gives paths at negative 1, false gives paths.
- Set provider.doctype from doctype.
- Return provider.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“data\_import\_providers”), Platform.get\_attr(paths at negative 1 when isinstance(paths, (list bitwise or tuple)), otherwise paths).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L144) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L626) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L602)
