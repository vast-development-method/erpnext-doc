# Shared value and file services · operations 61

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Xlsxutils

<a id="op-3fc93e8ee389f4"></a>
### XLSXStyle Builder.apply currency fieldtype formats.parse options

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_apply_currency_fieldtype_formats_parse_options`

**Inputs** options.

**Wrappers, in declaration order** functools.cache.

**Declared result** tuple.

**Explicit results** parts when len(parts) equals 3, otherwise tuple(no value, no value, no value).

**Local steps**

- Set parts from options.split(“:”).
- Return parts when len(parts) equals 3, otherwise tuple(no value, no value, no value).
  - Value choice on len(parts) equals 3 — true gives parts, false gives tuple(no value, no value, no value).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L1242) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L133) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1081)

<a id="op-3effa826b6049c"></a>
### XLSXStyle Builder.apply currency fieldtype formats.register currency style

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_apply_currency_fieldtype_formats_register_currency_style`

**Inputs** currency.

**Wrappers, in declaration order** functools.cache.

**Declared result** int.

**Explicit results** self.register\_style(mapping(“num\_format” → self.get\_number\_format(“Currency”, currency))).

**Local steps**

- Return self.register\_style(mapping(“num\_format” → self.get\_number\_format(“Currency”, currency))).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L1370) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L134) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1082)

<a id="op-ab4f2863c7c5ea"></a>
### XLSXStyle Builder.apply currency fieldtype formats.get row value

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_apply_currency_fieldtype_formats_get_row_value`

**Inputs** row, field.

**Explicit results** row.get(field).

**Local steps**

- Return row.get(field).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0549.json#L1173) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L130) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1078)

<a id="op-b3d80deaaadefe"></a>
### XLSXStyle Builder.apply currency fieldtype formats.get row value

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_apply_currency_fieldtype_formats_get_row_value_2`

**Inputs** row, field.

**Explicit results** row at idx when idx is distinct from no value, otherwise no value.

**Local steps**

- Set idx from \_field\_index\_get(field).
- Return row at idx when idx is distinct from no value, otherwise no value.
  - Value choice on idx is distinct from no value — true gives row at idx, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0549.json#L1234) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L131) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1079)

<a id="op-e6231fe968dfed"></a>
### XLSXStyle Builder.get currency symbol info

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_get_currency_symbol_info`

**Inputs** currency.

**Wrappers, in declaration order** staticmethod.

**Declared result** tuple at tuple(str, bool).

**Record and data access** read “Currency” via get\_value.

**Explicit results** tuple(empty text, false) · tuple((symbol or currency), bool(on\_right)).

**Local steps**

- If (not currency or Platform.db.get\_default(“hide\_currency\_symbol”) belongs to tuple(“1”, “Yes”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not currency → Platform.db.get\_default(“hide\_currency\_symbol”) belongs to tuple(“1”, “Yes”).
  - Return tuple(empty text, false).
- Set tuple(symbol, on\_right) from Platform.db.get\_value(“Currency”, currency, list(“symbol”, “symbol\_on\_right”)).
- Return tuple((symbol or currency), bool(on\_right)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in symbol → currency.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L1481) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L141) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1089)

<a id="op-1b52352db7d837"></a>
### XLSXStyle Builder.build currency format

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_build_currency_format`

**Inputs** format\_string, currency\_symbol = no value, symbol\_on\_right = false.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** format\_string · formatted text {format\_string}" {currency\_symbol}";-{format\_string}" {currency\_symbol}" · formatted text "{currency\_symbol} "{format\_string};"{currency\_symbol} "-{format\_string}.

**Local steps**

- If not currency\_symbol.
  - Return format\_string.
- If symbol\_on\_right.
  - Return formatted text {format\_string}" {currency\_symbol}";-{format\_string}" {currency\_symbol}".
- Return formatted text "{currency\_symbol} "{format\_string};"{currency\_symbol} "-{format\_string}.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L1745) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L139) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1087)

<a id="op-7670c53fb1f302"></a>
### XLSXStyle Builder.get number format

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_get_number_format`

**Inputs** fieldtype, currency = no value.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** XLSXStyleBuilder.\_build\_currency\_format(format\_str, currency\_symbol, symbol\_on\_right) · formatted text {format\_str}"%"  when fieldtype equals “Percent”, otherwise format\_str · “General”.

**Local steps**

- Bind dependencies \_get\_format.
- Set number\_format from \_get\_format().
- Set thousands\_sep from number\_format.thousands\_separator.
- Set precision from number\_format.precision.
- If fieldtype equals “Currency”.
  - Set currency\_precision from get\_currency\_precision().
  - Set precision from currency\_precision when currency\_precision is distinct from no value, otherwise precision.
    - Value choice on currency\_precision is distinct from no value — true gives currency\_precision, false gives precision.
  - Set format\_str from XLSXStyleBuilder.\_build\_number\_format(thousands\_sep, precision).
  - Set tuple(currency\_symbol, symbol\_on\_right) from XLSXStyleBuilder.\_get\_currency\_symbol\_info(currency).
  - Return XLSXStyleBuilder.\_build\_currency\_format(format\_str, currency\_symbol, symbol\_on\_right).
- Otherwise.
  - If fieldtype belongs to tuple(“Float”, “Percent”).
    - Set precision from (cint(Platform.db.get\_default(“float\_precision”)) or precision).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → precision.
    - Set format\_str from XLSXStyleBuilder.\_build\_number\_format(thousands\_sep, precision).
    - Return formatted text {format\_str}"%"  when fieldtype equals “Percent”, otherwise format\_str.
      - Value choice on fieldtype equals “Percent” — true gives formatted text {format\_str}"%" , false gives format\_str.
- Return “General”.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L18) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L144) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1092)

<a id="op-574c8342b52743"></a>
### XLSXStyle Builder.build number format

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_build_number_format`

**Inputs** thousands\_sep, precision = 0.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** formatted text {integer\_part}{decimal\_part}.

**Local steps**

- Set integer\_part from “#,##0” when thousands\_sep, otherwise “#0”.
  - Value choice on thousands\_sep — true gives “#,##0”, false gives “#0”.
- Set decimal\_part from (“.” + (“0” × precision)) when precision &gt; 0, otherwise empty text.
  - Value choice on precision &gt; 0 — true gives (“.” + (“0” × precision)), false gives empty text.
- Return formatted text {integer\_part}{decimal\_part}.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L2529) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L140) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1088)

<a id="op-4d1603953e23f3"></a>
### XLSXStyle Builder.get date format

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_get_date_format`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** Platform.get\_system\_settings(“date\_format”).

**Local steps**

- Return Platform.get\_system\_settings(“date\_format”).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“date\_format”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L2693) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L142) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1090)

<a id="op-5007afbfba2f99"></a>
### XLSXStyle Builder.get time format

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_get_time_format`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** Platform.get\_system\_settings(“time\_format”).

**Local steps**

- Return Platform.get\_system\_settings(“time\_format”).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“time\_format”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L2751) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L145) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1093)

<a id="op-46dfb3bc18f5d6"></a>
### XLSXStyle Builder.get datetime format

`operation_foundation_utils_xlsxutils_business_behavior_spreadsheet_workbook_style_builder_get_datetime_format`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** formatted text {XLSXStyleBuilder.get\_date\_format()} {XLSXStyleBuilder.get\_time\_format()}.

**Local steps**

- Return formatted text {XLSXStyleBuilder.get\_date\_format()} {XLSXStyleBuilder.get\_time\_format()}.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L2809) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L143) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1091)

<a id="op-26964a915178a0"></a>
### Get default xlsx styles

`operation_foundation_utils_xlsxutils_business_behavior_get_default_spreadsheet_workbook_styles`

**Inputs** columns, data, applied\_filters = no value, has\_total\_row (named only, default false), has\_indentation (named only, default false), currency\_formatting (named only, default true).

**Declared result** dict.

**Explicit results** XLSXStyleBuilder(metadata, default\_styling = false).apply\_default\_styles(currency\_formatting).result.

**Local steps**

- Set applied\_filters from (applied\_filters or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in applied\_filters → list().
- Set header\_index from (len(applied\_filters) + 1) when applied\_filters, otherwise 0.
  - Value choice on applied\_filters — true gives (len(applied\_filters) + 1), false gives 0.
- Set applied\_filters\_map from dict(enumerate(applied\_filters)).
- Set column\_map from dict(enumerate(columns)).
- Set row\_map from dict(enumerate(data, start = (header\_index + 1))).
- Set metadata from XLSXMetadata(column\_map = column\_map, row\_map = row\_map, applied\_filters\_map = applied\_filters\_map, has\_total\_row = has\_total\_row, …).
- Return XLSXStyleBuilder(metadata, default\_styling = false).apply\_default\_styles(currency\_formatting).result.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L2899) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L116) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1064)

<a id="op-17b9bdb152c4a2"></a>
### Make xlsx

`operation_foundation_utils_xlsxutils_business_behavior_make_spreadsheet_workbook`

**Inputs** data, sheet\_name, wb = no value, column\_widths = no value, styles = no value.

**Declared result** (BytesIO bitwise or no value).

**Explicit results** no value · xlsx\_file.

**Local steps**

- Set column\_widths from (column\_widths or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in column\_widths → list().
- Set styles from (styles or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in styles → mapping().
- Set xlsx\_file from no value.
- Set created\_wb from false.
- If wb is identical to no value.
  - Set xlsx\_file from BytesIO().
  - Set options from mapping(“constant\_memory” → true).
  - If not styles.
    - Set options at “default\_date\_format” from XLSXStyleBuilder.get\_datetime\_format().
  - Set wb from xlsxwriter.Workbook(xlsx\_file, options).
  - Set created\_wb from true.
- Set ws from wb.add\_worksheet(get\_sanitized\_sheet\_name(sheet\_name)).
- Bind local operation \_extract\_ids for subsequent calls.
- Set style\_registry from (styles.get(“styles”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in styles.get(“styles”) → list().
- Set col\_style\_ids from \_extract\_ids(“column\_styles”).
- Set row\_style\_ids from \_extract\_ids(“row\_styles”).
- Set cell\_style\_ids from \_extract\_ids(“cell\_styles”).
- Set styling\_enabled from bool((col\_style\_ids or row\_style\_ids or cell\_style\_ids)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in col\_style\_ids → row\_style\_ids → cell\_style\_ids.
- If not styling\_enabled.
  - Evaluate ws.set\_row(0, cell\_format = wb.add\_format(mapping(“bold” → true))).
- Bind local operation resolve\_style\_ids for subsequent calls.
- Bind local operation get\_format for subsequent calls.
- Set excel\_time\_format from XLSXStyleBuilder.get\_time\_format().
- Bind local operation get\_time\_cell\_format for subsequent calls.
- For each tuple(i, column\_width) in enumerate(column\_widths).
  - If column\_width.
    - Evaluate ws.set\_column(i, i, column\_width).
- For each tuple(col\_idx, style\_ids) in col\_style\_ids.items().
  - Evaluate ws.set\_column(col\_idx, col\_idx, cell\_format = get\_format(style\_ids)).
- For each tuple(row\_idx, style\_ids) in sorted(row\_style\_ids.items()).
  - Evaluate ws.set\_row(row\_idx, cell\_format = get\_format(style\_ids)).
- Set cell\_formats from mapping().
- For each tuple(pos, cell\_ids) in cell\_style\_ids.items().
  - Set tuple(row\_idx, col\_idx) from pos.
  - Set col\_ids from col\_style\_ids.get(col\_idx, tuple()).
  - Set row\_ids from row\_style\_ids.get(row\_idx, tuple()).
  - Set cell\_formats at pos from get\_format(((col\_ids + row\_ids) + cell\_ids)).
- For each tuple(row\_idx, row\_ids) in row\_style\_ids.items().
  - For each tuple(col\_idx, col\_ids) in col\_style\_ids.items().
    - Set pos from tuple(row\_idx, col\_idx).
    - If pos does not belong to cell\_formats.
      - Set cell\_formats at pos from get\_format((col\_ids + row\_ids)).
- Set handle\_html\_content from sheet\_name does not belong to set(“Data Import Template”, “Data Export”).
- Set illegal\_chars\_search from ILLEGAL\_CHARACTERS\_RE.search.
- Set illegal\_chars\_sub from ILLEGAL\_CHARACTERS\_RE.sub.
- Set write from ws.write.
- Set write\_string from ws.write\_string.
- Set has\_cell\_formats from bool(cell\_formats).
- Set get\_cell\_format from cell\_formats.get.
- For each tuple(row\_idx, row) in enumerate(data).
  - For each tuple(col\_idx, value) in enumerate(row).
    - Set is\_formula\_like from false.
    - If isinstance(value, str).
      - If handle\_html\_content.
        - Set value from handle\_html(value).
      - If illegal\_chars\_search(value).
        - Set value from illegal\_chars\_sub(empty text, value).
      - Set is\_formula\_like from value.startswith(FORMULA\_TRIGGER\_CHARS).
    - Set cell\_format from get\_cell\_format(tuple(row\_idx, col\_idx)) when has\_cell\_formats, otherwise no value.
      - Value choice on has\_cell\_formats — true gives get\_cell\_format(tuple(row\_idx, col\_idx)), false gives no value.
    - If isinstance(value, (datetime.time bitwise or datetime.timedelta)).
      - Set cell\_format from get\_time\_cell\_format(((col\_style\_ids.get(col\_idx, tuple()) + row\_style\_ids.get(row\_idx, tuple())) + cell\_style\_ids.get(tuple(row\_idx, col\_idx), tuple())), “&#91;h&#93;:mm:ss” when isinstance(value, datetime.timede ….
        - Value choice on isinstance(value, datetime.timedelta) — true gives “&#91;h&#93;:mm:ss”, false gives excel\_time\_format.
    - If is\_formula\_like.
      - Evaluate write\_string(row\_idx, col\_idx, value, cell\_format).
    - Otherwise.
      - Evaluate write(row\_idx, col\_idx, value, cell\_format).
- If not created\_wb.
  - Return no value.
- Evaluate wb.close().
- Evaluate xlsx\_file.seek(0).
- Return xlsx\_file.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L15) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L119) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1067)

<a id="op-2e7268561cceaa"></a>
### Make xlsx.extract ids

`operation_foundation_utils_xlsxutils_business_behavior_make_spreadsheet_workbook_extract_identifiers`

**Inputs** key.

**Declared result** dict.

**Explicit results** mapping of k → tuple(v) for tuple(k, v) drawn from (styles.get(key) or mapping()).items() where v.

**Local steps**

- Return mapping of k → tuple(v) for tuple(k, v) drawn from (styles.get(key) or mapping()).items() where v.
  - Draw tuple(k, v) from (styles.get(key) or mapping()).items(), keep a combination only if (v).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in styles.get(key) → mapping().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L5527) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L120) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1068)

<a id="op-f7db17c2b97979"></a>
### Make xlsx.resolve style ids

`operation_foundation_utils_xlsxutils_business_behavior_make_spreadsheet_workbook_resolve_style_identifiers`

**Inputs** style\_ids.

**Declared result** dict.

**Explicit results** style\_registry at style\_ids at 0 · result.

**Local steps**

- If len(style\_ids) equals 1.
  - Return style\_registry at style\_ids at 0.
- Set result from mapping().
- For each sid in style\_ids.
  - Evaluate result.update(style\_registry at sid).
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L5657) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L122) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1070)

<a id="op-1c2e9be9bd8d3e"></a>
### Make xlsx.get format

`operation_foundation_utils_xlsxutils_business_behavior_make_spreadsheet_workbook_get_format`

**Inputs** style\_ids.

**Wrappers, in declaration order** functools.cache.

**Declared result** Format.

**Explicit results** wb.add\_format(resolve\_style\_ids(style\_ids)).

**Local steps**

- Return wb.add\_format(resolve\_style\_ids(style\_ids)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L5832) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L121) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1069)

<a id="op-b8efe0b6f0b113"></a>
### Make xlsx.get time cell format

`operation_foundation_binding_foundation_utils_xlsxutils_make_xlsx_get_time_cell_format`

**Inputs** style\_ids, num\_format.

**Wrappers, in declaration order** functools.cache.

**Declared result** Format.

**Explicit results** wb.add\_format(style).

**Local steps**

- Set style from dict(resolve\_style\_ids(style\_ids)).
- Evaluate style.setdefault(“num\_format”, num\_format).
- Return wb.add\_format(style).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L62) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L367) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L455)

<a id="op-fd13e4266a13b5"></a>
### Get sanitized sheet name

`operation_foundation_utils_xlsxutils_business_behavior_get_sanitized_sheet_name`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** name.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L5934) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L117) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1065)

<a id="op-6509860462cd76"></a>
### Handle html

`operation_foundation_utils_xlsxutils_business_behavior_handle_document_markup`

**Inputs** data.

**Declared result** str.

**Explicit results** data · value.replace(whitespace '  \\n', “, ”).replace(whitespace '\\n', one space).replace(“# ”, “, ”).

**Local steps**

- If (“&lt;” does not belong to data or “&gt;” does not belong to data).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “&lt;” does not belong to data → “&gt;” does not belong to data.
  - Return data.
- Set h from unescape\_html((data or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data → empty text.
- Attempt the following.
  - Set value from html2text(h, strip\_links = true, wrap = false).
- On failure (Exception).
  - Return data.
- Return value.replace(whitespace '  \\n', “, ”).replace(whitespace '\\n', one space).replace(“# ”, “, ”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L6015) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L118) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1066)

<a id="op-70d69de84155c0"></a>
### Read xlsx file from attached file

`operation_foundation_utils_xlsxutils_business_behavior_read_spreadsheet_workbook_file_from_attached_file`

**Inputs** file\_url = no value, fcontent = no value, filepath = no value, read\_only (named only, default false).

**Record and data access** resolve a document from “File” via get\_doc.

**Explicit results** no value · rows.

**Local steps**

- If file\_url.
  - Set \_file from Platform.get\_doc(“File”, mapping(“file\_url” → file\_url)).
  - Set filename from \_file.get\_full\_path().
- Otherwise.
  - If fcontent.
    - Set filename from BytesIO(fcontent).
  - Otherwise.
    - If filepath.
      - Set filename from filepath.
    - Otherwise.
      - Return no value.
- Bind dependencies load\_workbook.
- Set rows from list().
- Set wb1 from load\_workbook(filename = filename, data\_only = true, read\_only = read\_only).
- Set ws1 from wb1.active.
- For each row in ws1.iter\_rows().
  - Evaluate rows.append(list of cell.value for cell drawn from row).
    - Draw cell from row.
- If read\_only.
  - Evaluate wb1.close().
- Return rows.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L16) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L123) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1071)

<a id="op-aead0b6cfdaf57"></a>
### Read xls file from attached file

`operation_foundation_utils_xlsxutils_business_behavior_read_spreadsheet_workbook_file_from_attached_file_2`

**Inputs** content.

**Explicit results** list of sheet.row\_values(i) for i drawn from range(sheet.nrows).

**Local steps**

- Set book from xlrd.open\_workbook(file\_contents = content).
- Set sheets from book.sheets().
- Set sheet from sheets at 0.
- Return list of sheet.row\_values(i) for i drawn from range(sheet.nrows).
  - Draw i from range(sheet.nrows).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L6688) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L124) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1072)

<a id="op-8db7ba20642f40"></a>
### Build xlsx response

`operation_foundation_utils_xlsxutils_business_behavior_build_spreadsheet_workbook_response`

**Inputs** data, filename, styles = no value.

**Local steps**

- Bind dependencies provide\_binary\_file.
- Evaluate provide\_binary\_file(filename, “xlsx”, make\_xlsx(data, filename, styles = styles).getvalue()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L6854) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L115) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1063)
