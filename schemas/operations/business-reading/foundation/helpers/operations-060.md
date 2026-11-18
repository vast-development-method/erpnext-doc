# Shared value and file services · operations 60

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Weasyprint legacy

<a id="op-fc12226d51297a"></a>
### Print Format Generator.process zones

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_process_zones`

**Inputs** self, layout.

**Explicit results** layout.

**Local steps**

- For each key in tuple(“header”, “footer”).
  - Set zone from unwrap\_zone(layout.get(key)).
  - If isinstance(zone, dict).
    - Evaluate self.set\_field\_renderers(mapping(“sections” → list(zone))).
    - Set zone from ((“{% raw %}” + Platform.render\_template(formatted text {TEMPLATE\_DIR}/zone.html, mapping(“zone” → zone, “doc” → self.doc, “legacy” → true))) + “{% endraw %}”).
  - Set layout at key from zone.
- Return layout.

**Methods declared on this owner** [set field renderers](operations-059.md#op-03052198a1d4b8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L56) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L361) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L449)

<a id="op-787ce2fb81d2b6"></a>
### Print Format Generator.process margin texts

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_process_margin_texts`

**Inputs** self, layout.

**Explicit results** layout.

**Local steps**

- Set margin\_texts from list(“top\_left”, “top\_center”, “top\_right”, “bottom\_left”, …).
- For each key in margin\_texts.
  - Set text from layout.get((“text\_” + key)).
  - If (text and “{{” belongs to text).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in text → “{{” belongs to text.
    - Set layout at (“text\_” + key) from Platform.render\_template(text, self.context).
- Return layout.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L55) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L360) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L448)

<a id="op-778f6729a9e47d"></a>
### Print Format Generator.get element

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_get_element`

**Inputs** boxes, element.

**Wrappers, in declaration order** staticmethod.

**Explicit results** box · PrintFormatGenerator.get\_element(box.all\_children(), element).

**Local steps**

- For each box in boxes.
  - If box.element\_tag equals element.
    - Return box.
  - Return PrintFormatGenerator.get\_element(box.all\_children(), element).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L48) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L353) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L441)

<a id="op-01e53d0744d34a"></a>
### Encrypt pdf

`operation_foundation_binding_foundation_utils_weasyprint_legacy_encrypt_pdf`

**Control responsibility** Protected data and signing. Key ownership, the selected cryptographic provider and verification status govern the protected data.

**Declared inputs** pdf, password.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L38) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L343) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L431)

<a id="op-466036928588f8"></a>
### Import weasyprint

`operation_foundation_binding_foundation_utils_weasyprint_legacy_import_weasyprint`

**Inputs** no declared parameters.

**Explicit results** tuple(HTML, CSS).

**Explicit failure paths** validation helper — message.

**Local steps**

- Attempt the following.
  - Bind dependencies CSS, HTML.
  - Return tuple(HTML, CSS).
- On failure (OSError).
  - Set message from whitespace '\\n'.join(list(“WeasyPrint depends on additional system dependencies.”, “Follow instructions specific to your operating system:”, text in the contract)).
  - Evaluate click.secho(message, fg = “yellow”).
  - Call the validation error handler Platform.throw(message).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L42) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L347) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L435)

## Service · Xlsxutils

<a id="op-fdd2741a6bea16"></a>
### XLSXMetadata.get column

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_metadata_get_column`

**Inputs** self, fieldname.

**Declared result** (dict bitwise or no value).

**Explicit results** next(generator of col for col drawn from self.column\_map.values() where col.get(“fieldname”) equals fieldname, no value).

**Local steps**

- Return next(generator of col for col drawn from self.column\_map.values() where col.get(“fieldname”) equals fieldname, no value).
  - Draw col from self.column\_map.values(), keep a combination only if (col.get(“fieldname”) equals fieldname).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L3318) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L125) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1073)

<a id="op-221c9e1bcf8e2b"></a>
### XLSXMetadata.get header index

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_metadata_get_header_index`

**Inputs** self.

**Declared result** int.

**Explicit results** (count + 1) when count, otherwise 0.

**Local steps**

- Set count from len(self.applied\_filters\_map).
- Return (count + 1) when count, otherwise 0.
  - Value choice on count — true gives (count + 1), false gives 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L3464) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L127) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1075)

<a id="op-9f3e66db13b724"></a>
### XLSXMetadata.get first row index

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_metadata_get_first_row_index`

**Inputs** self.

**Declared result** int.

**Explicit results** min(self.row\_map.keys()) when self.row\_map, otherwise 0.

**Local steps**

- Return min(self.row\_map.keys()) when self.row\_map, otherwise 0.
  - Value choice on self.row\_map — true gives min(self.row\_map.keys()), false gives 0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L3552) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L126) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1074)

<a id="op-e7f676dbbb30ed"></a>
### XLSXMetadata.get last row index

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_metadata_get_last_row_index`

**Inputs** self.

**Declared result** int.

**Explicit results** max(self.row\_map.keys()) when self.row\_map, otherwise 0.

**Local steps**

- Return max(self.row\_map.keys()) when self.row\_map, otherwise 0.
  - Value choice on self.row\_map — true gives max(self.row\_map.keys()), false gives 0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L3634) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L128) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1076)

<a id="op-b868f3c682d8cc"></a>
### XLSXStyle Builder.initialize

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_initialize`

**Inputs** self, metadata, default\_styling = true.

**Local steps**

- Set self.metadata from metadata.
- Set self.field\_index\_map from mapping of col.get(“fieldname”) → idx for tuple(idx, col) drawn from self.metadata.column\_map.items() where col.get(“fieldname”).
  - Draw tuple(idx, col) from self.metadata.column\_map.items(), keep a combination only if (col.get(“fieldname”)).
- Set self.styles from list().
- Set self.column\_styles from mapping().
- Set self.row\_styles from mapping().
- Set self.cell\_styles from mapping().
- Set self.result from mapping(“styles” → self.styles, “column\_styles” → self.column\_styles, “row\_styles” → self.row\_styles, “cell\_styles” → self.cell\_styles).
- Set self.header\_index from self.metadata.get\_header\_index().
- Set self.first\_row\_index from self.metadata.get\_first\_row\_index().
- Set self.last\_row\_index from self.metadata.get\_last\_row\_index().
- Set self.row\_is\_dict from isinstance(self.metadata.row\_map.get(self.first\_row\_index), dict).
- Evaluate self.\_register\_common\_styles().
- If default\_styling.
  - Evaluate self.apply\_default\_styles().

If control reaches the end, it returns no value.

**Methods declared on this owner** [register common styles](operations-060.md#op-f28a7871bdb5df), [apply default styles](operations-060.md#op-6e0c7c75c34b60).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L3716) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L146) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1094)

<a id="op-f28a7871bdb5df"></a>
### XLSXStyle Builder.register common styles

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_register_common_styles`

**Inputs** self.

**Local steps**

- Set self.bold\_style\_id from self.register\_style(mapping(“bold” → true)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [register style](operations-060.md#op-839f0424cd4b55).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L4259) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L147) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1095)

<a id="op-839f0424cd4b55"></a>
### XLSXStyle Builder.register style

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_register_style`

**Inputs** self, style.

**Declared result** int.

**Explicit results** style\_id.

**Explicit failure paths** validation helper — translated “Cannot register an empty XLSX style”.

**Local steps**

- If not style.
  - Call the validation error handler Platform.throw(translated “Cannot register an empty XLSX style”).
- Set style\_id from len(self.styles).
- Evaluate self.styles.append(style).
- Return style\_id.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L4342) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L148) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1096)

<a id="op-860c3c58bfb286"></a>
### XLSXStyle Builder.style column

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_style_column`

**Inputs** self, col\_idx, style\_id.

**Explicit results** self.

**Local steps**

- If col\_idx does not belong to self.column\_styles.
  - Set self.column\_styles at col\_idx from list().
- Evaluate self.column\_styles at col\_idx.append(style\_id).
- Return self.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L4504) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L150) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1098)

<a id="op-0fe78f6eece624"></a>
### XLSXStyle Builder.style row

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_style_row`

**Inputs** self, row\_idx, style\_id.

**Explicit results** self.

**Local steps**

- If row\_idx does not belong to self.row\_styles.
  - Set self.row\_styles at row\_idx from list().
- Evaluate self.row\_styles at row\_idx.append(style\_id).
- Return self.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L4650) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L153) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1101)

<a id="op-8b3d620a61a86e"></a>
### XLSXStyle Builder.style cell

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_style_cell`

**Inputs** self, row\_idx, col\_idx, style\_id.

**Explicit results** self.

**Local steps**

- Set key from tuple(row\_idx, col\_idx).
- Set cell\_styles from self.cell\_styles.
- If key does not belong to cell\_styles.
  - Set cell\_styles at key from list().
- Evaluate cell\_styles at key.append(style\_id).
- Return self.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L4796) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L149) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1097)

<a id="op-6e0c7c75c34b60"></a>
### XLSXStyle Builder.apply default styles

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_apply_default_styles`

**Inputs** self, currency\_formatting = true.

**Explicit results** self.

**Local steps**

- Evaluate self.style\_header().
- If self.metadata.applied\_filters\_map.
  - Evaluate self.style\_filters().
- If self.metadata.has\_total\_row.
  - Evaluate self.style\_total\_row().
- If self.metadata.has\_indentation.
  - Evaluate self.apply\_indentations().
- Evaluate self.apply\_default\_fieldtype\_formats(currency\_formatting).
- Return self.

**Methods declared on this owner** [style header](operations-060.md#op-1f2731042d76d5), [style filters](operations-060.md#op-996874550b9dda), [style total row](operations-060.md#op-8224b551b1eaaf), [apply indentations](operations-060.md#op-0e362ce4bafe65), [apply default fieldtype formats](operations-060.md#op-72b69821b8d1b0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L4981) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L136) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1084)

<a id="op-1f2731042d76d5"></a>
### XLSXStyle Builder.style header

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_style_header`

**Inputs** self.

**Explicit results** self.

**Local steps**

- Set header\_index from self.header\_index.
- Evaluate self.style\_row(header\_index, self.bold\_style\_id).
- Set right\_align from self.register\_style(mapping(“align” → “right”)).
- Set left\_align from self.register\_style(mapping(“align” → “left”)).
- For each tuple(col\_idx, col) in self.metadata.column\_map.items().
  - Evaluate self.style\_cell(header\_index, col\_idx, right\_align when col.get(“fieldtype”) belongs to self.RIGHT\_ALIGN\_FIELDTYPES, otherwise left\_align).
    - Value choice on col.get(“fieldtype”) belongs to self.RIGHT\_ALIGN\_FIELDTYPES — true gives right\_align, false gives left\_align.
- Return self.

**Methods declared on this owner** [style row](operations-060.md#op-0fe78f6eece624), [register style](operations-060.md#op-839f0424cd4b55), [style cell](operations-060.md#op-8b3d620a61a86e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L5194) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L152) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1100)

<a id="op-996874550b9dda"></a>
### XLSXStyle Builder.style filters

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_style_filters`

**Inputs** self.

**Explicit results** self.

**Local steps**

- For each row\_idx in self.metadata.applied\_filters\_map.keys().
  - Evaluate self.style\_cell(row\_idx, 0, self.bold\_style\_id).
- Return self.

**Methods declared on this owner** [style cell](operations-060.md#op-8b3d620a61a86e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L5507) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L151) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1099)

<a id="op-0e362ce4bafe65"></a>
### XLSXStyle Builder.apply indentations

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_apply_indentations`

**Inputs** self, col\_idx = 0, field = “indent”, pt = 2.

**Explicit results** self.

**Local steps**

- If not self.row\_is\_dict.
  - Return self.
- Bind local operation register\_indent\_style for subsequent calls.
- Set last\_row\_index from self.last\_row\_index.
- Set skip\_last\_row from self.metadata.has\_total\_row.
- Set style\_cell from self.style\_cell.
- For each tuple(row\_idx, row) in self.metadata.row\_map.items().
  - If (skip\_last\_row and row\_idx equals last\_row\_index).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in skip\_last\_row → row\_idx equals last\_row\_index.
    - Continue with the next iteration or loop test.
  - If indent bound to row.get(field).
    - Evaluate style\_cell(row\_idx, col\_idx, register\_indent\_style(cint(indent))).
- Return self.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L17) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L137) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1085)

<a id="op-96a74f29c43c1a"></a>
### XLSXStyle Builder.apply indentations.register indent style

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_apply_indentations_register_indent_style`

**Inputs** indent.

**Wrappers, in declaration order** functools.cache.

**Declared result** int.

**Explicit results** self.register\_style(mapping(“align” → “left”, “indent” → (indent × pt))).

**Local steps**

- Return self.register\_style(mapping(“align” → “left”, “indent” → (indent × pt))).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L6038) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L138) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1086)

<a id="op-8224b551b1eaaf"></a>
### XLSXStyle Builder.style total row

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_style_total_row`

**Inputs** self.

**Explicit results** self.style\_row(self.last\_row\_index, self.bold\_style\_id).

**Local steps**

- Return self.style\_row(self.last\_row\_index, self.bold\_style\_id).

**Methods declared on this owner** [style row](operations-060.md#op-0fe78f6eece624).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L6151) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L154) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1102)

<a id="op-72b69821b8d1b0"></a>
### XLSXStyle Builder.apply default fieldtype formats

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_apply_default_fieldtype_formats`

**Inputs** self, currency\_formatting = true.

**Explicit results** self.

**Local steps**

- Set formats from mapping(“Float” → self.register\_style(mapping(“num\_format” → self.get\_number\_format(“Float”))), “Percent” → self.register\_style(mapping(“num\_format” → self.get\_number\_format(“Percent”))), “Date” → self.reg ….
- For each tuple(idx, col) in self.metadata.column\_map.items().
  - Set style\_id from formats.get(col.get(“fieldtype”)).
  - If style\_id is distinct from no value.
    - Evaluate self.style\_column(idx, style\_id).
- If currency\_formatting.
  - Evaluate self.apply\_currency\_fieldtype\_formats().
- Return self.

**Methods declared on this owner** [register style](operations-060.md#op-839f0424cd4b55), [get number format](operations-061.md#op-7670c53fb1f302), [get date format](operations-061.md#op-4d1603953e23f3), [get time format](operations-061.md#op-5007afbfba2f99), [get datetime format](operations-061.md#op-46dfb3bc18f5d6), [style column](operations-060.md#op-860c3c58bfb286), [apply currency fieldtype formats](operations-060.md#op-0503680870293f).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L6219) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L135) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1083)

<a id="op-0503680870293f"></a>
### XLSXStyle Builder.apply currency fieldtype formats

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_apply_currency_fieldtype_formats`

**Inputs** self.

**Explicit results** self.

**Local steps**

- Set currency\_options from mapping of col\_idx → col.get(“options”) for tuple(col\_idx, col) drawn from self.metadata.column\_map.items() where col.get(“fieldtype”) equals “Currency”.
  - Draw tuple(col\_idx, col) from self.metadata.column\_map.items(), keep a combination only if (col.get(“fieldtype”) equals “Currency”).
- If not currency\_options.
  - Return self.
- Set default\_currency from Platform.db.get\_default(“currency”).
- Set last\_row\_index from self.last\_row\_index.
- Set skip\_last\_row from self.metadata.has\_total\_row.
- Set currency\_options\_items from currency\_options.items().
- Set style\_cell from self.style\_cell.
- Bind local operation \_get\_value for subsequent calls.
- Bind local operation parse\_options for subsequent calls.
- Bind local operation register\_currency\_style for subsequent calls.
- If self.row\_is\_dict.
  - Bind local operation get\_row\_value for subsequent calls.
- Otherwise.
  - Set \_field\_index\_get from self.field\_index\_map.get.
  - Bind local operation get\_row\_value for subsequent calls.
- For each tuple(row\_idx, row) in self.metadata.row\_map.items().
  - If (skip\_last\_row and row\_idx equals last\_row\_index).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in skip\_last\_row → row\_idx equals last\_row\_index.
    - Continue with the next iteration or loop test.
  - For each tuple(col\_idx, options) in currency\_options\_items.
    - Set currency from no value.
    - If options.
      - If “:” does not belong to options.
        - Set currency from get\_row\_value(row, options).
      - Otherwise.
        - Set tuple(doctype, link\_field, currency\_field) from parse\_options(options).
        - If (doctype is distinct from no value and link\_value bound to get\_row\_value(row, link\_field)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype is distinct from no value → link\_value bound to get\_row\_value(row, link\_field).
          - Set currency from \_get\_value(doctype, link\_value, currency\_field).
    - Evaluate style\_cell(row\_idx, col\_idx, register\_currency\_style((currency or default\_currency))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in currency → default\_currency.
- Return self.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L6) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L129) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1077)

<a id="op-aae13327c85803"></a>
### XLSXStyle Builder.apply currency fieldtype formats.get value

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_apply_currency_fieldtype_formats_get_value`

**Inputs** doctype, docname, fieldname.

**Wrappers, in declaration order** functools.cache.

**Declared result** (str bitwise or no value).

**Record and data access** read doctype via get\_value.

**Explicit results** Platform.db.get\_value(doctype, docname, fieldname).

**Local steps**

- Return Platform.db.get\_value(doctype, docname, fieldname).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L1128) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L132) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1080)
