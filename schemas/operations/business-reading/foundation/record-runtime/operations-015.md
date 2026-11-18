# Record lifecycle and persistence · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Data import

[Record definition](../../../../data/record-types/data_import.json)

<a id="op-1daf1bf9082fdf"></a>
### Header.get column indexes.is table field

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_header_get_column_indexes_is_table_field`

**Inputs** df.

**Explicit results** df.child\_table\_df.fieldname equals tablefield.fieldname · true.

**Local steps**

- If tablefield.
  - Return df.child\_table\_df.fieldname equals tablefield.fieldname.
- Return true.

[Applicable decision contract](../../../foundation-decision-contracts/part-0055.json#L4101) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1224) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1217)

<a id="op-bfbcce99f6efaf"></a>
### Header.get columns

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_header_get_columns`

**Inputs** self, indexes.

**Explicit results** list of self.columns at i for i drawn from indexes.

**Local steps**

- Return list of self.columns at i for i drawn from indexes.
  - Draw i from indexes.

[Applicable decision contract](../../../foundation-decision-contracts/part-0055.json#L4179) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1225) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1218)

<a id="op-15dc1e03f23fc9"></a>
### Column.initialize

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_column_initialize`

**Inputs** self, index, header, doctype, column\_values, map\_to\_field = no value, seen = no value, value\_row\_numbers = no value, date\_format\_override = no value.

**Local steps**

- If seen is identical to no value.
  - Set seen from list().
- Set self.index from index.
- Set self.column\_number from (index + 1).
- Set self.doctype from doctype.
- Set self.header\_title from header.
- Set self.column\_values from column\_values.
- Set self.value\_row\_numbers from (value\_row\_numbers or list(range(2, (len(column\_values) + 2)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in value\_row\_numbers → list(range(2, (len(column\_values) + 2))).
- Set self.map\_to\_field from map\_to\_field.
- Set self.seen from seen.
- Set self.invalid\_value\_items from no value.
- Set self.date\_format\_override from date\_format\_override.
- Set self.date\_format from no value.
- Set self.df from no value.
- Set self.skip\_import from no value.
- Set self.warnings from list().
- Set self.meta from Platform.get\_meta(doctype).
- Evaluate self.parse().
- Evaluate self.validate\_values().

If control reaches the end, it returns no value.

**Methods declared on this owner** [parse](operations-015.md#op-dacc2d35892b78), [validate values](operations-015.md#op-417df85cb7bf5d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L26) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1200) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1194)

<a id="op-dacc2d35892b78"></a>
### Column.parse

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_column_parse`

**Inputs** self.

**Local steps**

- Set header\_title from self.header\_title.
- Set column\_number from str(self.column\_number).
- Set skip\_import from false.
- If (self.map\_to\_field and self.map\_to\_field differs from “Don't Import”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.map\_to\_field → self.map\_to\_field differs from “Don't Import”.
  - Set df from get\_df\_for\_column\_header(self.doctype, self.map\_to\_field).
  - If not df.
    - Evaluate self.warnings.append(mapping(“message” → translated “Could not map column {0} to field {1}”.format(column\_number, escape\_html(cstr(self.map\_to\_field))), “type” → “info”)).
- Otherwise.
  - Set df from get\_df\_for\_column\_header(self.doctype, header\_title).
- If not df.
  - Set skip\_import from true.
- Otherwise.
  - Set skip\_import from false.
- If header\_title belongs to self.seen.
  - Evaluate self.warnings.append(mapping(“col” → column\_number, “message” → translated “Skipping Duplicate Column {0}”.format(Platform.bold(escape\_html(header\_title))), “type” → “info”)).
  - Set df from no value.
  - Set skip\_import from true.
- Otherwise.
  - If self.map\_to\_field equals “Don't Import”.
    - Set skip\_import from true.
    - Evaluate self.warnings.append(mapping(“col” → column\_number, “message” → translated “Skipping column {0}”.format(Platform.bold(escape\_html(header\_title))), “type” → “info”)).
  - Otherwise.
    - If (header\_title and not df).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in header\_title → not df.
      - Evaluate self.warnings.append(mapping(“col” → column\_number, “message” → translated “"{0}" does not match any field. Map it in the Preview step, otherwise it will be ignored.”.format(Platform.bold(escape\_html(heade ….
    - Otherwise.
      - If (not header\_title and not df).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not header\_title → not df.
        - Evaluate self.warnings.append(mapping(“col” → column\_number, “message” → translated “Skipping Untitled Column”, “type” → “info”)).
- Set self.df from df.
- Set self.skip\_import from skip\_import.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L27) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1201) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1195)

<a id="op-51003b431fca8d"></a>
### Column.guess date format for column

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_column_guess_date_format_for_column`

**Inputs** self.

**Explicit results** no value · most\_common\_date\_format.

**Local steps**

- Bind local operation guess\_date\_format for subsequent calls.
- Set format\_by\_value from mapping of d → guess\_date\_format(d) for d drawn from set(self.column\_values).
  - Draw d from set(self.column\_values).
- Set date\_formats from list of format\_by\_value at d for d drawn from self.column\_values.
  - Draw d from self.column\_values.
- Set date\_formats from list of d for d drawn from date\_formats where d.
  - Draw d from date\_formats, keep a combination only if (d).
- If not date\_formats.
  - Return no value.
- Set unique\_date\_formats from set(date\_formats).
- Set most\_common\_date\_format from max(unique\_date\_formats, key = date\_formats.count).
- If len(unique\_date\_formats) &gt; 1.
  - Set message from translated “The column {0} has {1} different date formats. Automatically setting {2} as the default format as it is the  …”.
  - Set user\_date\_format from get\_user\_format(most\_common\_date\_format).
  - Evaluate self.warnings.append(mapping(“col” → self.column\_number, “message” → message.format(Platform.bold(escape\_html(self.header\_title)), len(unique\_date\_formats), Platform.bold(user\_date\_format)), “type” → “info”)).
- Return most\_common\_date\_format.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L25) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1198) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1192)

<a id="op-4e820dd7f189ae"></a>
### Column.guess date format for column.guess date format

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_column_guess_date_format_for_column_guess_date_format`

**Inputs** d.

**Explicit results** “%Y-%m-%d” · “%Y-%m-%d %H:%M:%S” · “%H:%M:%S” · Platform.utils.guess\_date\_format(d).

**Local steps**

- If isinstance(d, ((datetime bitwise or date) bitwise or time)).
  - If self.df.fieldtype equals “Date”.
    - Return “%Y-%m-%d”.
  - If self.df.fieldtype equals “Datetime”.
    - Return “%Y-%m-%d %H:%M:%S”.
  - If self.df.fieldtype equals “Time”.
    - Return “%H:%M:%S”.
- If isinstance(d, str).
  - Return Platform.utils.guess\_date\_format(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0055.json#L6408) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1199) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1193)

<a id="op-417df85cb7bf5d"></a>
### Column.validate values

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_column_validate_values`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.df.
  - Return no value.
- If self.skip\_import.
  - Return no value.
- If not any(self.column\_values).
  - Return no value.
- If self.df.fieldtype belongs to tuple(“Link”, “Select”).
  - Bind dependencies warn\_invalid\_link\_select\_values.
  - Evaluate warn\_invalid\_link\_select\_values(self).
- Otherwise.
  - If self.df.fieldtype belongs to tuple(“Date”, “Time”, “Datetime”).
    - Set self.date\_format from (self.date\_format\_override or self.guess\_date\_format\_for\_column()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.date\_format\_override → self.guess\_date\_format\_for\_column().
    - If not self.date\_format.
      - If self.df.fieldtype equals “Time”.
        - Set self.date\_format from “%H:%M:%S”.
        - Set date\_format from “HH:mm:ss”.
      - Otherwise.
        - Set self.date\_format from “%Y-%m-%d”.
        - Set date\_format from “yyyy-mm-dd”.
      - Set message from translated “{0} format could not be determined from the values in this column. Defaulting to {1}.”.
      - Evaluate self.warnings.append(mapping(“col” → self.column\_number, “message” → message.format(self.df.fieldtype, date\_format), “type” → “info”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [guess date format for column](operations-015.md#op-51003b431fca8d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L28) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1202) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1196)

<a id="op-2be098b2d0132f"></a>
### Column.as dict

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_column_as_mapping`

**Inputs** self.

**Explicit results** d.

**Local steps**

- Set d from Platform.\_dict().
- Set d.index from self.index.
- Set d.column\_number from self.column\_number.
- Set d.doctype from self.doctype.
- Set d.header\_title from self.header\_title.
- Set d.map\_to\_field from self.map\_to\_field.
- Set d.date\_format from self.date\_format.
- Set d.df from self.df.
- If hasattr(self.df, “is\_child\_table\_field”).
  - Set d.is\_child\_table\_field from self.df.is\_child\_table\_field.
  - Set d.child\_table\_df from self.df.child\_table\_df.
- Set d.skip\_import from self.skip\_import.
- Set d.warnings from self.warnings.
- Return d.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0056.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1197) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1191)

<a id="op-80a94fb4b120f6"></a>
### Hashable Table DF.hash

`operation_foundation_binding_foundation_core_doctype_data_import_importer_hashabletabledf_hash`

**Inputs** self.

**Explicit results** hash(tuple(self.get(“fieldname”), self.get(“options”))).

**Local steps**

- Return hash(tuple(self.get(“fieldname”), self.get(“options”))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L153) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L635) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L611)

<a id="op-ee7a0d88ce1891"></a>
### Build fields dict from schema

`operation_foundation_binding_foundation_core_doctype_data_import_importer_build_fields_dict_from_schema`

**Inputs** parent\_doctype, schema.

**Explicit results** out.

**Local steps**

- Set out from mapping().
- Set groups from list(tuple(parent\_doctype, no value, (schema.get(“fields”) or list()))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in schema.get(“fields”) → list().
- For each ct in (schema.get(“child\_tables”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in schema.get(“child\_tables”) → list().
  - Set child\_fields from (ct.get(“fields”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ct.get(“fields”) → list().
  - Set child\_doctype from (child\_fields at 0.get(“parent”) when child\_fields, otherwise no value or ct.get(“fieldname”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in child\_fields at 0.get(“parent”) when child\_fields, otherwise no value → ct.get(“fieldname”).
    - Value choice on child\_fields — true gives child\_fields at 0.get(“parent”), false gives no value.
  - Set table\_df from \_HashableTableDF(fieldname = ct at “fieldname”, label = (ct.get(“label”) or ct at “fieldname”), options = child\_doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ct.get(“label”) → ct at “fieldname”.
  - Evaluate groups.append(tuple(child\_doctype, table\_df, child\_fields)).
- For each tuple(doctype, table\_df, fields) in groups.
  - Set is\_parent from table\_df is identical to no value.
  - Set table\_ref from (table\_df.label or table\_df.fieldname) when table\_df, otherwise no value.
    - Value choice on table\_df — true gives (table\_df.label or table\_df.fieldname), false gives no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in table\_df.label → table\_df.fieldname.
  - Set translated\_table\_label from translated table\_ref when table\_ref, otherwise no value.
    - Value choice on table\_ref — true gives translated table\_ref, false gives no value.
  - Set name\_df from Platform.\_dict(mapping(“fieldtype” → “Data”, “fieldname” → “name”, “label” → “ID”, “reqd” → 1, …)).
  - If is\_parent.
    - Set name\_headers from tuple(“name”, “ID”, translated “ID”).
  - Otherwise.
    - Set name\_headers from tuple(formatted text {table\_df.fieldname}.name, formatted text ID ({table\_ref}), “{} ({})”.format(translated “ID”, translated\_table\_label)).
    - Set name\_df.is\_child\_table\_field from true.
    - Set name\_df.child\_table\_df from table\_df.
  - For each header in name\_headers.
    - Set out at header from name\_df.
  - For each df in fields.
    - Set df from Platform.\_dict(df).
    - If (df.fieldtype or “Data”) belongs to no\_value\_fields.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype → “Data”.
      - Continue with the next iteration or loop test.
    - Set label from (df.label or empty text).strip().
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label → empty text.
    - Set translated\_label from translated label.
    - Set prefer\_plain\_label from bool(df.get(“prefer\_plain\_label”)).
    - Set import\_labels from list((df.get(“import\_labels”) or list())).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“import\_labels”) → list().
    - If is\_parent.
      - For each header in tuple(label, translated\_label).
        - If header does not belong to out.
          - Set out at header from df.
      - For each header in tuple(df.fieldname, formatted text {label} ({df.fieldname}), formatted text {translated\_label} ({df.fieldname})).
        - Set out at header from df.
    - Otherwise.
      - Set new\_df from Platform.\_dict(df.copy()).
      - Set new\_df.is\_child\_table\_field from true.
      - Set new\_df.child\_table\_df from table\_df.
      - If prefer\_plain\_label.
        - For each header in tuple(label, translated\_label, df.fieldname).
          - If header.
            - Set out at header from new\_df.
      - For each alias in import\_labels.
        - If alias.
          - Set out at alias from new\_df.
      - For each header in tuple(formatted text {table\_df.fieldname}.{df.fieldname}, formatted text {label} ({table\_ref}), formatted text {translated\_label} ({translated\_table\_label})).
        - Set out at header from new\_df.
- Return out.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L149) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L631) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L607)

<a id="op-6277497f4b2957"></a>
### Build fields dict for column matching

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_build_fields_mapping_for_column_matching`

**Inputs** parent\_doctype.

**Explicit results** \_build\_fields\_dict\_from\_schema(parent\_doctype, schema) · out.

**Local steps**

- Bind dependencies get\_import\_provider.
- Set provider from get\_import\_provider(parent\_doctype).
- If (provider and schema bound to provider.get\_import\_fields()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in provider → schema bound to provider.get\_import\_fields().
  - Return \_build\_fields\_dict\_from\_schema(parent\_doctype, schema).
- Bind local operation get\_standard\_fields for subsequent calls.
- Set parent\_meta from Platform.get\_meta(parent\_doctype).
- Set out from mapping().
- Set doctypes from (list(tuple(parent\_doctype, no value)) + list of tuple(df.options, df) for df drawn from parent\_meta.get\_table\_fields()).
  - Draw df from parent\_meta.get\_table\_fields().
- For each tuple(doctype, table\_df) in doctypes.
  - Set table\_ref from (table\_df.label or table\_df.fieldname) when table\_df, otherwise no value.
    - Value choice on table\_df — true gives (table\_df.label or table\_df.fieldname), false gives no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in table\_df.label → table\_df.fieldname.
  - Set translated\_table\_label from translated table\_ref when table\_ref, otherwise no value.
    - Value choice on table\_ref — true gives translated table\_ref, false gives no value.
  - Set name\_df from Platform.\_dict(mapping(“fieldtype” → “Data”, “fieldname” → “name”, “label” → “ID”, “reqd” → 1, …)).
  - If doctype equals parent\_doctype.
    - Set name\_headers from tuple(“name”, “ID”, translated “ID”).
  - Otherwise.
    - Set name\_headers from tuple(formatted text {table\_df.fieldname}.name, formatted text ID ({table\_ref}), “{} ({})”.format(translated “ID”, translated\_table\_label)).
    - Set name\_df.is\_child\_table\_field from true.
    - Set name\_df.child\_table\_df from table\_df.
  - For each header in name\_headers.
    - Set out at header from name\_df.
  - Set fields from (get\_standard\_fields(doctype) + Platform.get\_meta(doctype).fields).
  - For each df in fields.
    - Set fieldtype from (df.fieldtype or “Data”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype → “Data”.
    - If fieldtype belongs to no\_value\_fields.
      - Continue with the next iteration or loop test.
    - Set label from (df.label or empty text).strip().
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label → empty text.
    - Set translated\_label from translated label.
    - If parent\_doctype equals doctype.
      - For each header in tuple(label, translated\_label).
        - If header does not belong to out.
          - Set out at header from df.
      - For each header in tuple(df.fieldname, formatted text {label} ({df.fieldname}), formatted text {translated\_label} ({df.fieldname})).
        - Set out at header from df.
    - Otherwise.
      - If isinstance(df, dict).
        - Set new\_df from Platform.\_dict(df.copy()).
      - Otherwise.
        - Set new\_df from df.as\_dict().
      - Set new\_df.is\_child\_table\_field from true.
      - Set new\_df.child\_table\_df from table\_df.
      - For each header in tuple(formatted text {table\_df.fieldname}.{df.fieldname}, formatted text {label} ({table\_ref}), formatted text {translated\_label} ({translated\_table\_label})).
        - Set out at header from new\_df.
- Set autoname\_field from get\_autoname\_field(parent\_doctype).
- If autoname\_field.
  - For each header in tuple(formatted text ID ({autoname\_field.label}), “{} ({})”.format(translated “ID”, translated autoname\_field.label), “ID”, translated “ID”, …).
    - Set out at header from autoname\_field.
- Return out.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L23) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1193) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1187)

<a id="op-a5445ffe7b5c6d"></a>
### Build fields dict for column matching.get standard fields

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_build_fields_mapping_for_column_matching_get_standard_fields`

**Inputs** doctype.

**Explicit results** out.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- If meta.istable.
  - Set standard\_fields from list(mapping(“label” → “Parent”, “fieldname” → “parent”), mapping(“label” → “Parent Type”, “fieldname” → “parenttype”), mapping(“label” → “Parent Field”, “fieldname” → “parentfield”), mapping(“label” → “Ro ….
- Otherwise.
  - Set standard\_fields from list(mapping(“label” → “Owner”, “fieldname” → “owner”), mapping(“label” → “Document Status”, “fieldname” → “docstatus”, “fieldtype” → “Int”)).
- Set out from list().
- For each df in standard\_fields.
  - Set df from Platform.\_dict(df).
  - Set df.parent from doctype.
  - Evaluate out.append(df).
- Return out.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0056.json#L2256) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1194) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1188)

<a id="op-1fe8a44f192b9d"></a>
### Get df for column header

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_df_for_column_header`

**Inputs** doctype, header.

**Explicit results** \_get\_fields\_dict(doctype, Platform.session.user).get(header).

**Local steps**

- Return \_get\_fields\_dict(doctype, Platform.session.user).get(header).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L29) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1207) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1201)

<a id="op-14a9c4c8ed32d8"></a>
### Get fields dict

`operation_foundation_binding_foundation_core_doctype_data_import_importer_get_fields_dict`

**Inputs** doctype, user.

**Wrappers, in declaration order** request\_cache.

**Explicit results** build\_fields\_dict\_for\_column\_matching(doctype).

**Local steps**

- Return build\_fields\_dict\_for\_column\_matching(doctype).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L150) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L632) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L608)

<a id="op-431356facbd8fc"></a>
### Get id field

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_identifier_field`

**Inputs** doctype.

**Explicit results** autoname\_field · Platform.\_dict(mapping(“label” → “ID”, “fieldname” → “name”, “fieldtype” → “Data”)).

**Local steps**

- Set autoname\_field from get\_autoname\_field(doctype).
- If autoname\_field.
  - Return autoname\_field.
- Return Platform.\_dict(mapping(“label” → “ID”, “fieldname” → “name”, “fieldtype” → “Data”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0056.json#L2916) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1211) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1204)

<a id="op-8be53fda2c5953"></a>
### Get autoname field

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_autoname_field`

**Inputs** doctype.

**Explicit results** meta.get\_field(fieldname).

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- If (meta.autoname and meta.autoname.startswith(“field:”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.autoname → meta.autoname.startswith(“field:”).
  - Set fieldname from meta.autoname at slice len(“field:”) to no value.
  - Return meta.get\_field(fieldname).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0056.json#L3069) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1206) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1200)

<a id="op-e1344dd3820059"></a>
### Get item at index

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_item_at_index`

**Inputs** \_list, i, default = no value.

**Explicit results** a.

**Local steps**

- Attempt the following.
  - Set a from \_list at i.
- On failure (IndexError).
  - Set a from default.
- Return a.

[Applicable decision contract](../../../foundation-decision-contracts/part-0056.json#L3241) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1214) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1207)

<a id="op-c8c063d01fe982"></a>
### Get user format

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_user_format`

**Inputs** date\_format.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract).replace(“%y”, “yy”).replace(“%m”, “mm”).replace(“%d”, “dd”).

**Local steps**

- Return nested operand in the contract(nested operand in the contract, nested operand in the contract).replace(“%y”, “yy”).replace(“%m”, “mm”).replace(“%d”, “dd”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0056.json#L3348) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1220) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1213)

<a id="op-ba4d28ae117601"></a>
### Df as json

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_df_as_structured_data`

**Inputs** df.

**Explicit results** mapping(“fieldname” → df.fieldname, “fieldtype” → df.fieldtype, “label” → df.label, “options” → df.options, …).

**Local steps**

- Return mapping(“fieldname” → df.fieldname, “fieldtype” → df.fieldtype, “label” → df.label, “options” → df.options, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0056.json#L3464) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1204) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1198)

<a id="op-10475d6f2e0fc7"></a>
### Get select options

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_select_options`

**Inputs** df.

**Explicit results** list of d for d drawn from (df.options or empty text).split(whitespace '\\n') where d.

**Local steps**

- Return list of d for d drawn from (df.options or empty text).split(whitespace '\\n') where d.
  - Draw d from (df.options or empty text).split(whitespace '\\n'), keep a combination only if (d).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.options → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0056.json#L3624) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1215) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1208)

<a id="op-ebbf3da9f57fd4"></a>
### Create import log

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_create_import_log`

**Inputs** data\_import, log\_index, log\_details.

**Record and data access** resolve a document from mapping(“doctype” → “Data Import Log”, “log\_index” → log\_index, “success” → log\_details.get(“success”), “data\_import” → data\_import, …) via get\_doc.

**State and service calls** call db\_insert on Platform.get\_doc(mapping(“doctype” → “Data Import Log”, “log\_index” → log\_index, “success” → log\_details.get(“success”), “data\_import” → data\_import, …)).

**Local steps**

- Evaluate Platform.get\_doc(mapping(“doctype” → “Data Import Log”, “log\_index” → log\_index, “success” → log\_details.get(“success”), “data\_import” → data\_import, …)).db\_insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0056.json#L3715) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1203) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1197)

<a id="op-a8384c8e0b0b2a"></a>
### Get parent field

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_get_parent_field`

**Inputs** df.

**Declared result** (str bitwise or no value).

**Explicit results** df.child\_table\_df.fieldname · no value.

**Local steps**

- If (getattr(df, “is\_child\_table\_field”, false) and getattr(df, “child\_table\_df”, no value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(df, “is\_child\_table\_field”, false) → getattr(df, “child\_table\_df”, no value).
  - Return df.child\_table\_df.fieldname.
- Return no value.

**Values supplied outside this operation** selected callable from getattr(df, “is\_child\_table\_field”, false), getattr(df, “child\_table\_df”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0059.json#L7583) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1350) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1341)

<a id="op-bb05919966d02a"></a>
### Get field key

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_get_field_key`

**Inputs** reference\_doctype, fieldname, parent\_field = no value.

**Declared result** str.

**Explicit results** formatted text {reference\_doctype}.{parent\_field}.{fieldname} · formatted text {reference\_doctype}.{fieldname}.

**Local steps**

- If parent\_field.
  - Return formatted text {reference\_doctype}.{parent\_field}.{fieldname}.
- Return formatted text {reference\_doctype}.{fieldname}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0059.json#L7703) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1345) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1336)

<a id="op-8ff91bb0097e33"></a>
### Get field key from df

`operation_foundation_core_record_definitions_data_import_value_mapping_business_behavior_get_field_key_from_df`

**Inputs** df, reference\_doctype.

**Declared result** str.

**Explicit results** get\_field\_key(reference\_doctype, df.fieldname, get\_parent\_field(df)).

**Local steps**

- Return get\_field\_key(reference\_doctype, df.fieldname, get\_parent\_field(df)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0059.json#L7868) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1346) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1337)
