# Web content and issued documents · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Print format

[Record definition](../../../../data/record-types/print_format.json)

<a id="op-9763e220270532"></a>
### Convert classic to beta.new column

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_convert_classic_to_beta_new_column`

**Inputs** no declared parameters.

**Local steps**

- If not state.section.
  - Evaluate new\_section().
- Set state.column from mapping(“label” → empty text, “fields” → list()).
- Evaluate state.section at “columns”.append(state.column).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0313.json#L4004) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1220) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1762)

<a id="op-3d0b0116b5d7d2"></a>
### Convert classic to beta.add field

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_convert_classic_to_beta_add_field`

**Inputs** field.

**Local steps**

- If not state.column.
  - Evaluate new\_column().
- Evaluate state.column at “fields”.append(field).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0313.json#L4155) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1219) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1761)

<a id="op-bb6991b5ca5e30"></a>
### Convert table columns

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_convert_table_columns`

**Inputs** df, meta\_df, dropped.

**Declared result** list.

**Explicit results** distribute\_widths(columns).

**Local steps**

- Set child\_meta from Platform.get\_meta(meta\_df.options).
- Set columns from list(mapping(“label” → “Sr”, “fieldname” → “idx”, “fieldtype” → “Int”, “options” → no value, …)).
- If df.get(“visible\_columns”).
  - For each col in df.visible\_columns.
    - Set col from Platform.\_dict(col).
    - If cint(col.print\_hide).
      - Continue with the next iteration or loop test.
    - Set child\_df from child\_meta.get\_field(col.fieldname).
    - If not child\_df.
      - Evaluate dropped.append(formatted text {meta\_df.fieldname}.{col.fieldname}).
      - Continue with the next iteration or loop test.
    - Evaluate columns.append(mapping(“label” → (child\_df.label or child\_df.fieldname), “fieldname” → child\_df.fieldname, “fieldtype” → child\_df.fieldtype, “options” → child\_df.options, …)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in child\_df.label → child\_df.fieldname.
- Otherwise.
  - Set child\_fields from list of child\_df for child\_df drawn from child\_meta.fields where (child\_df.fieldtype does not belong to tuple(“Section Break”, “Column Break”, “Tab Break”) and not cint(child\_df.print\_hide)).
    - Draw child\_df from child\_meta.fields, keep a combination only if ((child\_df.fieldtype does not belong to tuple(“Section Break”, “Column Break”, “Tab Break”) and not cint(child\_df.print\_hide))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in child\_df.fieldtype does not belong to tuple(“Section Break”, “Column Break”, “Tab Break”) → not cint(child\_df.print\_hide).
  - If len(child\_fields) &gt; MAX\_DEFAULT\_TABLE\_COLUMNS.
    - Set child\_fields from (list of df for df drawn from child\_fields where (cint(df.in\_list\_view) or cint(df.reqd) or df.fieldtype equals “Text Editor”) or child\_fields).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of df for df drawn from child\_fields where (cint(df.in\_list\_view) or cint(df.reqd) or df.fieldtype equals “Text Editor”) → child\_fields.
      - Draw df from child\_fields, keep a combination only if ((cint(df.in\_list\_view) or cint(df.reqd) or df.fieldtype equals “Text Editor”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(df.in\_list\_view) → cint(df.reqd) → df.fieldtype equals “Text Editor”.
  - For each child\_df in child\_fields.
    - Evaluate columns.append(mapping(“label” → (child\_df.label or child\_df.fieldname), “fieldname” → child\_df.fieldname, “fieldtype” → child\_df.fieldtype, “options” → child\_df.options, …)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in child\_df.label → child\_df.fieldname.
- Return distribute\_widths(columns).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L61) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1223) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1765)

<a id="op-ffa76e2ab16a87"></a>
### Parse print width

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_parse_print_width`

**Inputs** print\_width.

**Declared result** (float bitwise or no value).

**Explicit results** no value · float(print\_width at slice no value to negative 1) · round(((float(print\_width at slice no value to negative nested operand in the contract) ÷ ASSUMED\_BODY\_WIDTH\_PX) × 100), 2) · float(print\_width).

**Local steps**

- If not print\_width.
  - Return no value.
- Set print\_width from str(print\_width).strip().
- Attempt the following.
  - If print\_width.endswith(“%”).
    - Return float(print\_width at slice no value to negative 1).
  - If print\_width.endswith(“px”).
    - Return round(((float(print\_width at slice no value to negative nested operand in the contract) ÷ ASSUMED\_BODY\_WIDTH\_PX) × 100), 2).
  - Return float(print\_width).
- On failure (ValueError).
  - Return no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0313.json#L5047) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1233) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1773)

<a id="op-83edc3db144d2f"></a>
### Distribute widths

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_distribute_widths`

**Inputs** columns.

**Declared result** list.

**Explicit results** columns.

**Local steps**

- For each col in columns.
  - If (col.get(“width”) or 0) &lt; 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“width”) → 0.
    - Set col at “width” from no value.
- Set unsized from list of col for col drawn from columns where not col at “width”.
  - Draw col from columns, keep a combination only if (not col at “width”).
- Set assigned from sum(generator of col at “width” for col drawn from columns where col at “width”).
  - Draw col from columns, keep a combination only if (col at “width”).
- If unsized.
  - Set share from (max((100 − assigned), (DEFAULT\_COLUMN\_WIDTH\_PCT × len(unsized))) ÷ len(unsized)).
  - For each col in unsized.
    - Set col at “width” from round(share, 2).
- Set total from sum(generator of col at “width” for col drawn from columns).
  - Draw col from columns.
- If total &gt; 100.
  - For each col in columns.
    - Set col at “width” from round(((col at “width” ÷ total) × 100), 2).
- Return columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0313.json#L5348) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1227) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1769)

<a id="op-eb401f66999d0f"></a>
### Missing numeric defaults

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_missing_numeric_defaults`

**Inputs** values.

**Declared result** dict.

**Explicit results** mapping of f → flt(meta.get\_field(f).default) for f drawn from fields where not values.get(f).

**Local steps**

- Set meta from Platform.get\_meta(“Print Format”).
- Set fields from list(NUMERIC\_DEFAULT\_FIELDS).
- If any(generator of values.get(f) for f drawn from MARGIN\_FIELDS).
  - Draw f from MARGIN\_FIELDS.
  - Set fields from list of f for f drawn from fields where f does not belong to MARGIN\_FIELDS.
    - Draw f from fields, keep a combination only if (f does not belong to MARGIN\_FIELDS).
- Return mapping of f → flt(meta.get\_field(f).default) for f drawn from fields where not values.get(f).
  - Draw f from fields, keep a combination only if (not values.get(f)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0313.json#L5905) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1232) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1772)

<a id="op-22adec9c988658"></a>
### Convert print format

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_convert_print_format`

**Inputs** doc.

**Explicit results** no value · dropped.

**Local steps**

- If (doc.custom\_format or doc.raw\_printing or renders\_from\_file(doc)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.custom\_format → doc.raw\_printing → renders\_from\_file(doc).
  - Return no value.
- Set backup from parse\_classic\_backup(doc.classic\_format\_data).
- If backup.
  - Set format\_data from backup at “format\_data”.
  - Set fields from backup at “fields”.
- Otherwise.
  - Attempt the following.
    - Set format\_data from json.loads(doc.format\_data) when doc.format\_data, otherwise list().
      - Value choice on doc.format\_data — true gives json.loads(doc.format\_data), false gives list().
  - On failure (ValueError).
    - Return no value.
  - Set fields from mapping of f → doc.get(f) for f drawn from CONVERTED\_FIELDS.
    - Draw f from CONVERTED\_FIELDS.
- If not isinstance(format\_data, list).
  - Return no value.
- Set meta from Platform.get\_meta(doc.doc\_type).
- If format\_data.
  - Set tuple(layout, dropped) from convert\_classic\_to\_beta(format\_data, meta, doc).
  - Evaluate repair\_layout(layout).
- Otherwise.
  - Set tuple(layout, dropped) from tuple(create\_default\_layout(meta), list()).
- Set doc.classic\_format\_data from json.dumps(mapping(“format\_data” → format\_data, “fields” → fields), indent = 1).
- Set doc.format\_data from json.dumps(layout, indent = 1).
- Set doc.print\_format\_builder from 0.
- Set doc.print\_format\_builder\_beta from 1.
- For each tuple(fieldname, value) in missing\_numeric\_defaults(doc).items().
  - Evaluate doc.set(fieldname, value).
- Set doc.pdf\_generator from “chrome”.
- If (not doc.page\_number or doc.page\_number equals “Hide”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.page\_number → doc.page\_number equals “Hide”.
  - Set doc.page\_number from “Bottom Center”.
- Return dropped.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L60) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1222) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1764)

<a id="op-5929fa7ec0cc6e"></a>
### Conversion values

`operation_foundation_binding_foundation_printing_doctype_print_format_classic_converter_conversion_values`

**Inputs** doc.

**Declared result** dict.

**Explicit results** mapping of f → doc.get(f) for f drawn from CONVERSION\_VALUE\_FIELDS.

**Local steps**

- Return mapping of f → doc.get(f) for f drawn from CONVERSION\_VALUE\_FIELDS.
  - Draw f from CONVERSION\_VALUE\_FIELDS.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L220) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1676) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1652)

<a id="op-7f39e38d27297d"></a>
### Parse classic backup

`operation_foundation_binding_foundation_printing_doctype_print_format_classic_converter_parse_classic_backup`

**Inputs** classic\_format\_data.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · mapping(“format\_data” → backup, “fields” → mapping()) · mapping(“format\_data” → backup at “format\_data”, “fields” → (backup.get(“fields”) or mapping())).

**Local steps**

- If not classic\_format\_data.
  - Return no value.
- Attempt the following.
  - Set backup from json.loads(classic\_format\_data).
- On failure (ValueError).
  - Return no value.
- If isinstance(backup, list).
  - Return mapping(“format\_data” → backup, “fields” → mapping()).
- If (not isinstance(backup, dict) or not isinstance(backup.get(“format\_data”), list)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(backup, dict) → not isinstance(backup.get(“format\_data”), list).
  - Return no value.
- Return mapping(“format\_data” → backup at “format\_data”, “fields” → (backup.get(“fields”) or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in backup.get(“fields”) → mapping().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L222) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1678) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1654)

<a id="op-1c3d78164bf21a"></a>
### Restore classic format

`operation_foundation_binding_foundation_printing_doctype_print_format_classic_converter_restore_classic_format`

**Inputs** doc.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Set backup from parse\_classic\_backup(doc.classic\_format\_data).
- If not backup.
  - Return false.
- Set doc.format\_data from json.dumps(backup at “format\_data”, indent = 1).
- For each fieldname in CONVERTED\_FIELDS.
  - If fieldname belongs to backup at “fields”.
    - Evaluate doc.set(fieldname, backup at “fields” at fieldname).
- Set doc.classic\_format\_data from no value.
- Set doc.print\_format\_builder from 1.
- Set doc.print\_format\_builder\_beta from 0.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L225) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1681) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1657)

<a id="op-74cbaf9a5294f2"></a>
### Repair layout

`operation_foundation_binding_foundation_printing_doctype_print_format_classic_converter_repair_layout`

**Inputs** layout.

**Declared result** bool.

**Explicit results** false · changed.

**Local steps**

- If not isinstance(layout, dict).
  - Return false.
- Set changed from false.
- Set zones from list(layout.get(“header”), layout.get(“footer”), expanded (layout.get(“sections”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in layout.get(“sections”) → list().
- For each zone in zones.
  - For each column in (zone or mapping()).get(“columns”, list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in zone → mapping().
    - For each field in column.get(“fields”, list()).
      - If widen\_serial\_column(field.get(“table\_columns”)).
        - Set changed from true.
- If add\_section\_spacing(layout).
  - Set changed from true.
- Return changed.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L224) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1680) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1656)

<a id="op-321774b6ca53b2"></a>
### Add section spacing

`operation_foundation_binding_foundation_printing_doctype_print_format_classic_converter_add_section_spacing`

**Inputs** layout.

**Declared result** bool.

**Explicit results** false · bool(sections).

**Local steps**

- Set sections from list of s for s drawn from (layout.get(“sections”) or list()) at slice 1 to no value where isinstance(s, dict).
  - Draw s from (layout.get(“sections”) or list()) at slice 1 to no value, keep a combination only if (isinstance(s, dict)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in layout.get(“sections”) → list().
- If any(generator of (s.get(“margin”) or s.get(“padding”)) for s drawn from sections).
  - Draw s from sections.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in s.get(“margin”) → s.get(“padding”).
  - Return false.
- For each section in sections.
  - Set section at “margin” from mapping(“top” → CONVERTED\_SECTION\_GAP\_PX, “right” → 0, “bottom” → 0, “left” → 0).
- Return bool(sections).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L219) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1675) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1651)

<a id="op-63b495d94aed41"></a>
### Widen serial column

`operation_foundation_binding_foundation_printing_doctype_print_format_classic_converter_widen_serial_column`

**Inputs** table\_columns.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- If not table\_columns.
  - Return false.
- Set sr from table\_columns at 0.
- Set width from sr.get(“width”).
- If (sr.get(“fieldname”) differs from “idx” or not width or width ≥ DEFAULT\_COLUMN\_WIDTH\_PCT).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sr.get(“fieldname”) differs from “idx” → not width → width ≥ DEFAULT\_COLUMN\_WIDTH\_PCT.
  - Return false.
- Set others from sum(generator of (col.get(“width”) or 0) for col drawn from table\_columns at slice 1 to no value).
  - Draw col from table\_columns at slice 1 to no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“width”) → 0.
- If others.
  - Set factor from ((others − (DEFAULT\_COLUMN\_WIDTH\_PCT − width)) ÷ others).
  - For each col in table\_columns at slice 1 to no value.
    - If col.get(“width”).
      - Set col at “width” from round((col at “width” × factor), 2).
- Set sr at “width” from DEFAULT\_COLUMN\_WIDTH\_PCT.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L227) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1683) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1659)

<a id="op-745a01b2a9add1"></a>
### Is printable docfield

`operation_foundation_binding_foundation_printing_doctype_print_format_classic_converter_is_printable_docfield`

**Inputs** df.

**Declared result** bool.

**Explicit results** (df.fieldtype does not belong to no\_value\_fields or df.fieldtype belongs to tuple(“Table”, “Table MultiSelect”)).

**Local steps**

- Return (df.fieldtype does not belong to no\_value\_fields or df.fieldtype belongs to tuple(“Table”, “Table MultiSelect”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype does not belong to no\_value\_fields → df.fieldtype belongs to tuple(“Table”, “Table MultiSelect”).

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L221) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1677) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1653)

<a id="op-14a37079a6ddff"></a>
### Create default layout

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_create_default_layout`

**Inputs** meta.

**Declared result** dict.

**Explicit results** layout.

**Local steps**

- Set layout from mapping(“header” → mapping(“columns” → list(mapping(“label” → empty text, “fields” → list(mapping(“label” → empty text, “fieldname” → “print\_heading\_template”, “fieldtype” → “HTML”, “html” → DEFAULT\_PRINT\_ ….
- Set state from Platform.\_dict(section = no value, column = no value, skip = false).
- Bind local operation new\_section for subsequent calls.
- Bind local operation new\_column for subsequent calls.
- For each df in meta.fields.
  - If not df.fieldname.
    - Continue with the next iteration or loop test.
  - If df.fieldtype equals “Section Break”.
    - Set state.skip from bool(cint(df.print\_hide)).
    - If state.skip.
      - Set state.section, state.column from no value.
    - Otherwise.
      - Evaluate new\_section(df).
  - Otherwise.
    - If state.skip.
      - Continue with the next iteration or loop test.
    - Otherwise.
      - If df.fieldtype equals “Column Break”.
        - Evaluate new\_column(df).
      - Otherwise.
        - If (df.label and is\_printable\_docfield(df)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.label → is\_printable\_docfield(df).
          - If not state.column.
            - Evaluate new\_column().
          - If cint(df.print\_hide).
            - Continue with the next iteration or loop test.
          - Set field from mapping(“label” → df.label, “fieldname” → df.fieldname, “fieldtype” → df.fieldtype, “options” → df.options).
          - If df.fieldtype equals “Table”.
            - Set field at “show\_label” from “hide”.
            - Set field at “table\_columns” from convert\_table\_columns(Platform.\_dict(fieldname = df.fieldname), df, list()).
          - Evaluate state.column at “fields”.append(field).
          - Set state.section at “has\_fields” from true.
- Set layout at “sections” from list of s for s drawn from layout at “sections” where s.get(“has\_fields”).
  - Draw s from layout at “sections”, keep a combination only if (s.get(“has\_fields”)).
- For each section in layout at “sections”.
  - Evaluate section.pop(“has\_fields”, no value).
- Return layout.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L62) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1224) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1766)

<a id="op-df14ce589b47cc"></a>
### Create default layout.new section

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_create_default_layout_new_section`

**Inputs** df = no value.

**Local steps**

- Set state.section from mapping(“label” → (df.label when df, otherwise empty text or empty text), “columns” → list(), “has\_fields” → false).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label when df, otherwise empty text → empty text.
  - Value choice on df — true gives df.label, false gives empty text.
- Set state.column from no value.
- Evaluate layout at “sections”.append(state.section).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0314.json#L1375) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1226) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1768)

<a id="op-f7e8d774b8a0e0"></a>
### Create default layout.new column

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_create_default_layout_new_column`

**Inputs** df = no value.

**Local steps**

- If not state.section.
  - Evaluate new\_section().
- Set state.column from mapping(“label” → (df.label when df, otherwise empty text or empty text), “fields” → list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label when df, otherwise empty text → empty text.
  - Value choice on df — true gives df.label, false gives empty text.
- Evaluate state.section at “columns”.append(state.column).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0314.json#L1545) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1225) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1767)

<a id="op-08ed5f7be63513"></a>
### Get beta layout

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_get_beta_layout`

**Inputs** print\_format.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** resolve a document from “Print Format” via get\_doc.

**Explicit results** mapping(“layout” → json.loads(doc.format\_data), “dropped” → dropped, “values” → conversion\_values(doc)).

**Explicit failure paths** validation helper — Platform.\_(“{0} is not a classic print format”).format(print\_format).

**Local steps**

- Set doc from Platform.get\_doc(“Print Format”, print\_format).
- Evaluate doc.check\_permission(“write”).
- Set dropped from convert\_print\_format(doc).
- If dropped is identical to no value.
  - Call the validation error handler Platform.throw(Platform.\_(“{0} is not a classic print format”).format(print\_format)).
- Return mapping(“layout” → json.loads(doc.format\_data), “dropped” → dropped, “values” → conversion\_values(doc)).

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L63) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1228) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1770)

<a id="op-f8097cd8e40bef"></a>
### Print Format.onload

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_onload`

**Inputs** self.

**Record and data access** read “Print Format Field Template” via get\_all.

**Local steps**

- Set templates from Platform.get\_all(“Print Format Field Template”, fields = list(“template”, “field”, “name”), or\_filters = list(list(“document\_type”, “=”, self.doc\_type), list(“document\_type”, “is”, “not set”)), order\_by =  ….
- Evaluate self.set\_onload(“print\_templates”, templates).
- Bind dependencies renders\_from\_file.
- Bind dependencies resolve\_pdf\_generator.
- Evaluate self.set\_onload(“renders\_from\_file”, renders\_from\_file(self)).
- Evaluate self.set\_onload(“pdf\_generator”, resolve\_pdf\_generator(self)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L54) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1208) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1750)

<a id="op-0bc274ee7d119b"></a>
### Print Format.before save

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_before_save`

**Inputs** self.

**Local steps**

- If self.print\_format\_for equals “Report”.
  - Set self.custom\_format from 1.
- If (self.print\_format\_builder\_beta and not self.custom\_format and self.pdf\_generator does not belong to STORED\_RENDERERS).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.print\_format\_builder\_beta → not self.custom\_format → self.pdf\_generator does not belong to STORED\_RENDERERS.
  - Set self.pdf\_generator from “chrome”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L51) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1201) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1744)

<a id="op-aec72b1beecf8b"></a>
### Print Format.get html

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_get_document_markup`

**Inputs** self, docname, letterhead = no value.

**Explicit results** get\_html(self.doc\_type, docname, self.name, letterhead).

**Local steps**

- Return get\_html(self.doc\_type, docname, self.name, letterhead).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0314.json#L3633) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1205) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1747)

<a id="op-78ee40314daf52"></a>
### Print Format.download pdf

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_download_portable_document`

**Inputs** self, docname, letterhead = no value.

**Explicit results** download\_pdf(self.doc\_type, docname, self.name, letterhead).

**Local steps**

- Return download\_pdf(self.doc\_type, docname, self.name, letterhead).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0314.json#L3724) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1203) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1745)

<a id="op-e98ba0758d2572"></a>
### Print Format.validate

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_validate`

**Inputs** self.

**Record and data access** read “Print Format” via get\_value · read doc\_type via get\_value.

**Explicit failure paths** validation helper — Platform.\_(“Standard Print Format cannot be updated”) · validation helper with Platform.MandatoryError — translated “{0} are required”.format(Platform.bold(translated “Raw Commands”)) · validation helper with Platform.MandatoryError — translated “{0} is required”.format(Platform.bold(translated “HTML”)) · validation helper with Platform.MandatoryError — translated “{0} is required”.format(Platform.bold(translated “Report”)).

**Local steps**

- If (self.standard equals “Yes” and not Platform.local.conf.get(“developer\_mode”) and not Platform.flags.in\_migrate and not Platform.flags.in\_install and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.standard equals “Yes” → not Platform.local.conf.get(“developer\_mode”) → not Platform.flags.in\_migrate → not Platform.flags.in\_install → not Platform.in\_test.
  - Call the validation error handler Platform.throw(Platform.\_(“Standard Print Format cannot be updated”)).
- Set self.old\_doc\_type from Platform.db.get\_value(“Print Format”, self.name, “doc\_type”).
- Evaluate self.extract\_images().
- If not self.module.
  - Set doc\_type from “DocType” when self.print\_format\_for equals “DocType”, otherwise “Report”.
    - Value choice on self.print\_format\_for equals “DocType” — true gives “DocType”, false gives “Report”.
  - Set document\_name from self.doc\_type when self.print\_format\_for equals “DocType”, otherwise self.report.
    - Value choice on self.print\_format\_for equals “DocType” — true gives self.doc\_type, false gives self.report.
  - Set self.module from Platform.db.get\_value(doc\_type, document\_name, “module”).
- If (self.html and self.print\_format\_type differs from “JS”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.html → self.print\_format\_type differs from “JS”.
  - Evaluate validate\_template(self.html).
- If (self.custom\_format and self.raw\_printing and not self.raw\_commands).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.custom\_format → self.raw\_printing → not self.raw\_commands.
  - Call the validation error handler Platform.throw(translated “{0} are required”.format(Platform.bold(translated “Raw Commands”)), Platform.MandatoryError).
- If (self.custom\_format and not self.html and not self.raw\_printing).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.custom\_format → not self.html → not self.raw\_printing.
  - Call the validation error handler Platform.throw(translated “{0} is required”.format(Platform.bold(translated “HTML”)), Platform.MandatoryError).
- If (self.print\_format\_for equals “Report” and not self.report).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.print\_format\_for equals “Report” → not self.report.
  - Call the validation error handler Platform.throw(translated “{0} is required”.format(Platform.bold(translated “Report”)), Platform.MandatoryError).
- Evaluate self.validate\_colors().
- Evaluate self.validate\_conditions().
- Evaluate self.validate\_no\_classic\_layout().
- Evaluate self.validate\_weasyprint\_choice().
- Evaluate self.validate\_weasyprint\_layout().
- Evaluate self.validate\_typst\_renderer().
- Evaluate self.validate\_plutoprint\_renderer().

If control reaches the end, it returns no value.

**Methods declared on this owner** [extract images](operations-009.md#op-07a1dce55f6ed5), [validate colors](operations-009.md#op-3270778bd2957e), [validate conditions](operations-009.md#op-b94135b3406924), [validate no classic layout](operations-008.md#op-ebbbaba7a737de), [validate weasyprint choice](operations-009.md#op-b73420741a6940), [validate weasyprint layout](operations-009.md#op-f9f98d00d4a8cb), [validate typst renderer](operations-009.md#op-ac806f5ba142f0), [validate plutoprint renderer](operations-009.md#op-b54104075fb6f3).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L55) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1210) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1752)

<a id="op-ebbbaba7a737de"></a>
### Print Format.validate no classic layout

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_printformat_validate_no_classic_layout`

**Inputs** self.

**Explicit failure paths** validation helper — classic\_layout\_message().

**Local steps**

- Bind dependencies is\_classic\_layout.
- Bind dependencies classic\_layout\_message.
- If (self.print\_format\_builder\_beta and is\_classic\_layout(self.format\_data)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.print\_format\_builder\_beta → is\_classic\_layout(self.format\_data).
  - Call the validation error handler Platform.throw(classic\_layout\_message()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L6) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1693) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1669)
