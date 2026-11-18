# Record lifecycle and persistence · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Data export

[Record definition](../../../../data/record-types/data_export.json)

<a id="op-9a68e775acf0b9"></a>
### Data Exporter.initialize

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_initialize`

**Inputs** self, doctype = no value, parent\_doctype = no value, all\_doctypes = true, with\_data = false, select\_columns = no value, file\_type = “CSV”, template = false, filters = no value, export\_without\_column\_meta = false.

**Local steps**

- Set self.doctype from doctype.
- Set self.parent\_doctype from parent\_doctype.
- Set self.all\_doctypes from all\_doctypes.
- Set self.with\_data from cint(with\_data).
- Set self.select\_columns from select\_columns.
- Set self.file\_type from file\_type.
- Set self.template from template.
- Set self.filters from filters.
- Set self.export\_without\_column\_meta from export\_without\_column\_meta.
- Set self.data\_keys from get\_data\_keys().
- Evaluate self.prepare\_args().

If control reaches the end, it returns no value.

**Methods declared on this owner** [prepare args](operations-009.md#op-d6f64471b49109).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L2240) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1136) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1131)

<a id="op-d6f64471b49109"></a>
### Data Exporter.prepare args

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_prepare_arguments`

**Inputs** self.

**Local steps**

- If self.select\_columns.
  - Set self.select\_columns from parse\_json(self.select\_columns).
- If self.filters.
  - Set self.filters from parse\_json(self.filters).
- Set self.docs\_to\_export from mapping().
- If self.doctype.
  - If isinstance(self.doctype, str).
    - Set self.doctype from list(self.doctype).
  - If len(self.doctype) &gt; 1.
    - Set self.docs\_to\_export from self.doctype at 1.
  - Set self.doctype from self.doctype at 0.
- If not self.parent\_doctype.
  - Set self.parent\_doctype from self.doctype.
- Set self.column\_start\_end from mapping().
- If self.all\_doctypes.
  - Set self.child\_doctypes from list of dict(doctype = df.options, parentfield = df.fieldname) for df drawn from Platform.get\_meta(self.doctype).get\_table\_fields().
    - Draw df from Platform.get\_meta(self.doctype).get\_table\_fields().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L2579) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1137) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1132)

<a id="op-13d8d8c9cddaae"></a>
### Data Exporter.build response

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_build_response`

**Inputs** self.

**Local steps**

- Set self.writer from UnicodeWriter().
- Set self.name\_field from “parent” when self.parent\_doctype differs from self.doctype, otherwise “name”.
  - Value choice on self.parent\_doctype differs from self.doctype — true gives “parent”, false gives “name”.
- If self.template.
  - Evaluate self.add\_main\_header().
- If not self.export\_without\_column\_meta.
  - Evaluate self.writer.writerow(list(empty text)).
- Set self.tablerow from list(self.data\_keys.doctype).
- Set self.labelrow from list(translated “Column Labels:”).
- Set self.fieldrow from list(self.data\_keys.columns).
- Set self.mandatoryrow from list(translated “Mandatory:”).
- Set self.typerow from list(translated “Type:”).
- Set self.inforow from list(translated “Info:”).
- Set self.columns from list().
- Evaluate self.build\_field\_columns(self.doctype).
- If self.all\_doctypes.
  - For each d in self.child\_doctypes.
    - Evaluate self.append\_empty\_field\_column().
    - If ((self.select\_columns and self.select\_columns.get(d at “doctype”, no value)) or not self.select\_columns).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.select\_columns and self.select\_columns.get(d at “doctype”, no value)) → not self.select\_columns.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.select\_columns → self.select\_columns.get(d at “doctype”, no value).
      - Evaluate self.build\_field\_columns(d at “doctype”, d at “parentfield”).
- Evaluate self.add\_field\_headings().
- Evaluate self.add\_data().
- If (self.with\_data and not self.data).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.with\_data → not self.data.
  - Evaluate Platform.respond\_as\_web\_page(translated “No Data”, translated “There is no data to be exported”, indicator\_color = “orange”).
- If self.file\_type equals “Excel”.
  - Evaluate self.build\_response\_as\_excel().
- Otherwise.
  - Set Platform.response at “result” from cstr(self.writer.getvalue()).
  - Set Platform.response at “type” from “csv”.
  - Set Platform.response at “doctype” from self.doctype.

If control reaches the end, it returns no value.

**Methods declared on this owner** [add main header](operations-009.md#op-f79c580e23de78), [build field columns](operations-009.md#op-90f1c07aef16d4), [append empty field column](operations-009.md#op-f08909bf1782cd), [add field headings](operations-009.md#op-544062432220c3), [add data](operations-009.md#op-d832d2315d367b), [build response as excel](operations-009.md#op-b40290a27275b7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L3059) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1133) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1128)

<a id="op-f79c580e23de78"></a>
### Data Exporter.add main header

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_add_main_header`

**Inputs** self.

**Local steps**

- Evaluate self.writer.writerow(list(translated “Data Import Template”)).
- Evaluate self.writer.writerow(list(self.data\_keys.main\_table, self.doctype)).
- If self.parent\_doctype differs from self.doctype.
  - Evaluate self.writer.writerow(list(self.data\_keys.parent\_table, self.parent\_doctype)).
- Otherwise.
  - Evaluate self.writer.writerow(list(empty text)).
- Evaluate self.writer.writerow(list(empty text)).
- Evaluate self.writer.writerow(list(translated “Notes:”)).
- Evaluate self.writer.writerow(list(translated “Please do not change the template headings.”)).
- Evaluate self.writer.writerow(list(translated “First data column must be blank.”)).
- Evaluate self.writer.writerow(list(translated “If you are uploading new records, leave the "name" (ID) column blank.”)).
- Evaluate self.writer.writerow(list(translated “If you are uploading new records, "Naming Series" becomes mandatory, if present.”)).
- Evaluate self.writer.writerow(list(translated “Only mandatory fields are necessary for new records. You can delete non-mandatory columns if you wish.”)).
- Evaluate self.writer.writerow(list(translated “For updating, you can update only selective columns.”)).
- Evaluate self.writer.writerow(list(translated “You can only upload upto 5000 records in one go. (may be less in some cases)”)).
- If self.name\_field equals “parent”.
  - Evaluate self.writer.writerow(list(translated “"Parent" signifies the parent table in which this row must be added”)).
  - Evaluate self.writer.writerow(list(translated “If you are updating, please select "Overwrite" else existing rows will not be deleted.”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L3988) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1128) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1123)

<a id="op-90f1c07aef16d4"></a>
### Data Exporter.build field columns

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_build_field_columns`

**Inputs** self, dt, parentfield = no value.

**Local steps**

- Set meta from Platform.get\_meta(dt).
- Set tablecolumns from list().
- Set table\_name from (“tab” + dt).
- For each f in Platform.db.get\_table\_columns\_description(table\_name).
  - Set field from meta.get\_field(f.name).
  - If f.name belongs to list(“owner”, “creation”).
    - Set std\_field from next(generator of x for x drawn from Platform.model.std\_fields where x at “fieldname” equals f.name, no value).
      - Draw x from Platform.model.std\_fields, keep a combination only if (x at “fieldname” equals f.name).
    - If std\_field.
      - Set field from Platform.\_dict(mapping(“fieldname” → std\_field.get(“fieldname”), “label” → std\_field.get(“label”), “fieldtype” → std\_field.get(“fieldtype”), “options” → std\_field.get(“options”), …)).
  - If (field and ((self.select\_columns and f.name belongs to self.select\_columns at dt) or not self.select\_columns)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field → ((self.select\_columns and f.name belongs to self.select\_columns at dt) or not self.select\_columns).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.select\_columns and f.name belongs to self.select\_columns at dt) → not self.select\_columns.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.select\_columns → f.name belongs to self.select\_columns at dt.
    - Evaluate tablecolumns.append(field).
- Evaluate tablecolumns.sort(key = deferred anonymous expression).
- Set \_column\_start\_end from Platform.\_dict(start = 0).
- If dt equals self.doctype.
  - If ((meta.get(“autoname”) and nested operand in the contract.get(“autoname”).lower() equals “prompt”) or self.with\_data).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (meta.get(“autoname”) and meta.get(“autoname”).lower() equals “prompt”) → self.with\_data.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.get(“autoname”) → meta.get(“autoname”).lower() equals “prompt”.
    - Evaluate self.\_append\_name\_column().
  - If (meta.get(“istable”) and not self.with\_data).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.get(“istable”) → not self.with\_data.
    - Evaluate self.append\_field\_column(Platform.\_dict(mapping(“fieldname” → “parent”, “parent” → empty text, “label” → “Parent”, “fieldtype” → “Data”, …)), true).
  - Set \_column\_start\_end from Platform.\_dict(start = 0).
- Otherwise.
  - Set \_column\_start\_end from Platform.\_dict(start = len(self.columns)).
  - If self.with\_data.
    - Evaluate self.\_append\_name\_column(dt).
- For each docfield in tablecolumns.
  - Evaluate self.append\_field\_column(docfield, true).
- For each docfield in tablecolumns.
  - Evaluate self.append\_field\_column(docfield, false).
- If (len(self.columns) − \_column\_start\_end.start) equals 1.
  - Evaluate self.append\_empty\_field\_column().
- Set self.tablerow at (\_column\_start\_end.start + 1) from dt.
- If parentfield.
  - Set self.tablerow at (\_column\_start\_end.start + 2) from parentfield.
- Set \_column\_start\_end.end from (len(self.columns) + 1).
- Set self.column\_start\_end at tuple(dt, parentfield) from \_column\_start\_end.

If control reaches the end, it returns no value.

**Methods declared on this owner** [append name column](operations-009.md#op-6bbd947cd741ab), [append field column](operations-009.md#op-5e976999e8ab9c), [append empty field column](operations-009.md#op-f08909bf1782cd).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L4724) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1132) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1127)

<a id="op-5e976999e8ab9c"></a>
### Data Exporter.append field column

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_append_field_column`

**Inputs** self, docfield, for\_mandatory.

**Explicit results** no value.

**Local steps**

- If not docfield.
  - Return no value.
- If (for\_mandatory and not docfield.reqd).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_mandatory → not docfield.reqd.
  - Return no value.
- If (not for\_mandatory and docfield.reqd).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not for\_mandatory → docfield.reqd.
  - Return no value.
- If docfield.fieldname belongs to tuple(“parenttype”, “trash\_reason”).
  - Return no value.
- If docfield.hidden.
  - Return no value.
- If (self.select\_columns and docfield.fieldname does not belong to self.select\_columns.get(docfield.parent, list()) and docfield.fieldname differs from “name”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.select\_columns → docfield.fieldname does not belong to self.select\_columns.get(docfield.parent, list()) → docfield.fieldname differs from “name”.
  - Return no value.
- Evaluate self.tablerow.append(empty text).
- Evaluate self.fieldrow.append(docfield.fieldname).
- Evaluate self.labelrow.append(\_(docfield.label, context = docfield.parent)).
- Evaluate self.mandatoryrow.append(((docfield.reqd and “Yes”) or “No”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (docfield.reqd and “Yes”) → “No”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in docfield.reqd → “Yes”.
- Evaluate self.typerow.append(docfield.fieldtype).
- Evaluate self.inforow.append(self.getinforow(docfield)).
- Evaluate self.columns.append(docfield.fieldname).

If control reaches the end, it returns no value.

**Methods declared on this owner** [getinforow](operations-009.md#op-9f72e1e16f6b6a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L6232) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1130) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1125)

<a id="op-f08909bf1782cd"></a>
### Data Exporter.append empty field column

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_append_empty_field_column`

**Inputs** self.

**Local steps**

- Evaluate self.tablerow.append(“~”).
- Evaluate self.fieldrow.append(“~”).
- Evaluate self.labelrow.append(empty text).
- Evaluate self.mandatoryrow.append(empty text).
- Evaluate self.typerow.append(empty text).
- Evaluate self.inforow.append(empty text).
- Evaluate self.columns.append(empty text).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L6817) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1129) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1124)

<a id="op-9f72e1e16f6b6a"></a>
### Data Exporter.getinforow

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_getinforow`

**Inputs** docfield.

**Wrappers, in declaration order** staticmethod.

**Explicit results** empty text · (translated “One of” + “: {}”.format(“, ”.join(filter(no value, nested operand in the contract.options.split(whitespace '\\n'))))) · “Valid {}”.format(docfield.options) · “Integer” · “0 or 1” · 2 additional forms in the steps below.

**Local steps**

- If docfield.fieldtype equals “Select”.
  - If not docfield.options.
    - Return empty text.
  - Otherwise.
    - Return (translated “One of” + “: {}”.format(“, ”.join(filter(no value, nested operand in the contract.options.split(whitespace '\\n'))))).
- Otherwise.
  - If docfield.fieldtype equals “Link”.
    - Return “Valid {}”.format(docfield.options).
  - Otherwise.
    - If docfield.fieldtype equals “Int”.
      - Return “Integer”.
    - Otherwise.
      - If docfield.fieldtype equals “Check”.
        - Return “0 or 1”.
      - Otherwise.
        - If docfield.fieldtype belongs to list(“Date”, “Datetime”).
          - Return cstr(Platform.defaults.get\_defaults().date\_format).
        - Otherwise.
          - If hasattr(docfield, “info”).
            - Return docfield.info.
          - Otherwise.
            - Return empty text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L7037) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1135) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1130)

<a id="op-544062432220c3"></a>
### Data Exporter.add field headings

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_add_field_headings`

**Inputs** self.

**Local steps**

- If not self.export\_without\_column\_meta.
  - Evaluate self.writer.writerow(self.tablerow).
- Evaluate self.writer.writerow(self.labelrow).
- If not self.export\_without\_column\_meta.
  - Evaluate self.writer.writerow(self.fieldrow).
  - Evaluate self.writer.writerow(self.mandatoryrow).
  - Evaluate self.writer.writerow(self.typerow).
  - Evaluate self.writer.writerow(self.inforow).
- If self.template.
  - Evaluate self.writer.writerow(list(self.data\_keys.data\_separator)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L7465) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1127) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1122)

<a id="op-d832d2315d367b"></a>
### Data Exporter.add data

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_add_data`

**Inputs** self.

**Record and data access** read self.doctype via get\_list.

**Explicit results** no value.

**Local steps**

- Bind dependencies DocType.
- If (self.template and not self.with\_data).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.template → not self.with\_data.
  - Return no value.
- Set filters from self.filters.
- If not Platform.permissions.can\_export(self.parent\_doctype).
  - Evaluate Platform.permissions.can\_export(self.parent\_doctype, raise\_exception = true, is\_owner = true).
  - If isinstance(filters, dict).
    - Set filters from mapping(expand filters, “owner” → Platform.session.user).
  - Otherwise.
    - Set filters from list(expanded (filters or list()), list(“owner”, “=”, Platform.session.user)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → list().
- Set order\_by from no value.
- Set table\_columns from Platform.db.get\_table\_columns(self.parent\_doctype).
- If (“lft” belongs to table\_columns and “rgt” belongs to table\_columns).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “lft” belongs to table\_columns → “rgt” belongs to table\_columns.
  - Set order\_by from formatted text ′tab{self.parent\_doctype}′.′lft′ asc.
- Set self.data from Platform.get\_list(self.doctype, fields = list(“\*”), filters = filters, limit\_page\_length = no value, order\_by = order\_by).
- For each doc in self.data.
  - Set op from self.docs\_to\_export.get(“op”).
  - Set names from self.docs\_to\_export.get(“name”).
  - If (names and op).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in names → op.
    - If (op equals “=” and doc.name does not belong to names).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in op equals “=” → doc.name does not belong to names.
      - Continue with the next iteration or loop test.
    - Otherwise.
      - If (op equals “!=” and doc.name belongs to names).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in op equals “!=” → doc.name belongs to names.
        - Continue with the next iteration or loop test.
  - Otherwise.
    - If names.
      - Attempt the following.
        - Set sflags from self.docs\_to\_export.get(“flags”, “I,U”).upper().
        - Set flags from 0.
        - For each a in re.split(“\\W+”, sflags).
          - Set flags from (flags bitwise or reflags.get(a, 0)).
        - Set c from re.compile(names, flags).
        - Set m from c.match(doc.name).
        - If not m.
          - Continue with the next iteration or loop test.
      - On failure (Exception).
        - If doc.name does not belong to names.
          - Continue with the next iteration or loop test.
  - Set rows from list().
  - Evaluate self.add\_data\_row(rows, self.doctype, no value, doc, …).
  - If self.all\_doctypes.
    - For each c in self.child\_doctypes.
      - If is\_virtual\_doctype(c at “doctype”).
        - Continue with the next iteration or loop test.
      - Set child\_doctype\_table from DocType(c at “doctype”).
      - Set data\_row from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.parent equals nested operand in the contract.name).where(child\_doctype\_table.parentfield equals c at “par ….
      - For each tuple(ci, child) in enumerate(data\_row.run(as\_dict = true)).
        - Evaluate self.add\_data\_row(rows, c at “doctype”, c at “parentfield”, child, …).
  - For each row in rows.
    - Evaluate self.writer.writerow(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add data row](operations-009.md#op-64b8f1351dd099).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1125) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1120)

<a id="op-64b8f1351dd099"></a>
### Data Exporter.add data row

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_add_data_row`

**Inputs** self, rows, dt, parentfield, doc, rowidx.

**Local steps**

- Set d from doc.copy().
- Set meta from Platform.get\_meta(dt).
- If self.all\_doctypes.
  - Set d.name from formatted text "{d.name}".
- If len(rows) &lt; (rowidx + 1).
  - Evaluate rows.append((list(empty text) × (len(self.columns) + 1))).
- Set row from rows at rowidx.
- Set \_column\_start\_end from self.column\_start\_end.get(tuple(dt, parentfield)).
- If \_column\_start\_end.
  - For each tuple(i, c) in enumerate(self.columns at slice \_column\_start\_end.start to \_column\_start\_end.end).
    - Set df from meta.get\_field(c).
    - Set fieldtype from df.fieldtype when df, otherwise “Data”.
      - Value choice on df — true gives df.fieldtype, false gives “Data”.
    - Set value from d.get(c, empty text).
    - If value.
      - If fieldtype equals “Date”.
        - Set value from formatdate(value).
      - Otherwise.
        - If fieldtype equals “Datetime”.
          - Set value from format\_datetime(value).
        - Otherwise.
          - If fieldtype equals “Duration”.
            - Set value from format\_duration(value, df.hide\_days).
          - Otherwise.
            - If (fieldtype equals “Text Editor” and value).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype equals “Text Editor” → value.
              - Set value from Platform.core.utils.html2text(value).
    - Set row at ((\_column\_start\_end.start + i) + 1) from value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L1333) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1126) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1121)

<a id="op-b40290a27275b7"></a>
### Data Exporter.build response as excel

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_build_response_as_excel`

**Inputs** self.

**Local steps**

- Bind dependencies provide\_binary\_file.
- Bind dependencies make\_xlsx.
- Set filename from Platform.generate\_hash(length = 10).
- Within open(filename, “wb”) bound as f.
  - Evaluate f.write(cstr(nested operand in the contract.writer.getvalue()).encode(“utf-8”)).
- Set f from open(filename).
- Set reader from csv.reader(f).
- Set xlsx\_file from make\_xlsx(reader, “Data Import Template” when self.template, otherwise “Data Export”).
  - Value choice on self.template — true gives “Data Import Template”, false gives “Data Export”.
- Evaluate f.close().
- Evaluate os.remove(filename).
- Evaluate provide\_binary\_file(self.doctype, “xlsx”, xlsx\_file.getvalue()).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 10).

**Boundaries to resolve** late-bound calls, callee failures, file state, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L2115) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1134) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1129)

<a id="op-6bbd947cd741ab"></a>
### Data Exporter.append name column

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_data_exporter_append_name_column`

**Inputs** self, dt = no value.

**Local steps**

- Evaluate self.append\_field\_column(Platform.\_dict(mapping(“fieldname” → “name” when dt, otherwise self.name\_field, “parent” → (dt or empty text), “label” → “ID”, “fieldtype” → “Data”, …)), true).
  - Value choice on dt — true gives “name”, false gives self.name\_field.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in dt → empty text.

If control reaches the end, it returns no value.

**Methods declared on this owner** [append field column](operations-009.md#op-5e976999e8ab9c).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L2488) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1131) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1126)

## Record · Data import

[Record definition](../../../../data/record-types/data_import.json)

<a id="op-892abee023aa5f"></a>
### Value mapping state

`operation_foundation_binding_foundation_core_doctype_data_import_data_import_value_mapping_state`

**Inputs** doc.

**Declared result** list at tuple at tuple(str, str, str, str).

**Explicit results** sorted(generator of tuple((row.fieldname or empty text), (row.parent\_field or empty text), (row.source\_value or empty text), (nested operand in the contract.target\_value or empty text).strip()) for row drawn from …).

**Local steps**

- Return sorted(generator of tuple((row.fieldname or empty text), (row.parent\_field or empty text), (row.source\_value or empty text), (nested operand in the contract.target\_value or empty text).strip()) for row drawn from …).
  - Draw row from (doc.get(“value\_mappings”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.fieldname → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.parent\_field → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.source\_value → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.target\_value → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“value\_mappings”) → list().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L139) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L621) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L597)

<a id="op-20524acba1f334"></a>
### Import source fingerprint

`operation_foundation_binding_foundation_core_doctype_data_import_data_import_import_source_fingerprint`

**Inputs** doc.

**Declared result** str.

**Explicit results** “\|”.join(list(cstr(doc.import\_file), cstr(doc.google\_sheets\_url), cstr(cint(doc.use\_csv\_sniffer)), cstr(cint(doc.custom\_delimiters)), …)).

**Local steps**

- Return “\|”.join(list(cstr(doc.import\_file), cstr(doc.google\_sheets\_url), cstr(cint(doc.use\_csv\_sniffer)), cstr(cint(doc.custom\_delimiters)), …)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L138) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L620) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L596)

<a id="op-577ed876398558"></a>
### Data Import.validate

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_validate`

**Inputs** self.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If (not (self.import\_file or self.google\_sheets\_url) or (doc\_before\_save and doc\_before\_save.import\_file differs from self.import\_file) or (doc\_before\_save and doc\_before\_save.google\_sheets\_url differs from s ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not (self.import\_file or self.google\_sheets\_url) → (doc\_before\_save and doc\_before\_save.import\_file differs from self.import\_file) → (doc\_before\_save and doc\_before\_save.google\_sheets\_url differs from self.google\_sheets\_url).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.import\_file → self.google\_sheets\_url.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save → doc\_before\_save.import\_file differs from self.import\_file.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save → doc\_before\_save.google\_sheets\_url differs from self.google\_sheets\_url.
  - Set self.template\_options from empty text.
  - Set self.template\_warnings from empty text.
  - Set self.value\_mappings from list().
  - Set self.skipped\_rows from list().
  - Set self.tree\_parent\_overrides from empty text.
- If (doc\_before\_save and doc\_before\_save.reference\_doctype differs from self.reference\_doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save → doc\_before\_save.reference\_doctype differs from self.reference\_doctype.
  - Set self.tree\_parent\_overrides from empty text.
- Evaluate self.clear\_stale\_template\_warnings(doc\_before\_save).
- Evaluate self.set\_delimiters\_flag().
- Evaluate self.validate\_doctype().
- Evaluate self.validate\_google\_sheets\_url().
- Set importer from self.get\_importer() when (self.import\_file or self.google\_sheets\_url), otherwise no value.
  - Value choice on (self.import\_file or self.google\_sheets\_url) — true gives self.get\_importer(), false gives no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.import\_file → self.google\_sheets\_url.
- If importer.
  - Evaluate self.set\_payload\_count(importer).
  - Evaluate self.warn\_if\_no\_column\_matches(importer).
  - Set mappings\_before\_sync from \_value\_mapping\_state(self).
  - Evaluate self.sync\_value\_mappings\_from\_import(importer).
  - If (self.template\_warnings and \_value\_mapping\_state(self) differs from mappings\_before\_sync).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.template\_warnings → \_value\_mapping\_state(self) differs from mappings\_before\_sync.
    - Set self.template\_warnings from empty text.
- Otherwise.
  - Evaluate self.set\_payload\_count().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear stale template warnings](operations-009.md#op-43347a8d2ec5f4), [set delimiters flag](operations-009.md#op-aac94134fb0991), [validate doctype](operations-009.md#op-ee13610b424bf2), [validate google sheets url](operations-009.md#op-202a380c3e629f), [get importer](operations-010.md#op-b85e1beed3a806), [set payload count](operations-009.md#op-ec2acae8f75aae), [warn if no column matches](operations-009.md#op-6e851569aa83af), [sync value mappings from import](operations-009.md#op-ab9785c2024652).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L8) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1157) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1151)

<a id="op-6e851569aa83af"></a>
### Data Import.warn if no column matches

`operation_foundation_binding_foundation_core_doctype_data_import_data_import_dataimport_warn_if_no_column_matches`

**Inputs** self, importer.

**Declared result** no value.

**State and service calls** msgprint with translated “None of the columns in your file match {0}. Check that it is the right file; if it is, map its columns to {0 …”.format(translated self.reference\_doctype).

**Explicit results** no value.

**Local steps**

- If self.reference\_doctype belongs to generator of doctype for tuple(doctype, table\_df) drawn from importer.import\_file.header.doctypes.
  - Draw tuple(doctype, table\_df) from importer.import\_file.header.doctypes.
  - Return no value.
- Evaluate Platform.msgprint(translated “None of the columns in your file match {0}. Check that it is the right file; if it is, map its columns to {0 …”.format(translated self.reference\_doctype), alert = true, indica ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L135) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L617) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L593)

<a id="op-43347a8d2ec5f4"></a>
### Data Import.clear stale template warnings

`operation_foundation_binding_foundation_core_doctype_data_import_data_import_dataimport_clear_stale_template_warnings`

**Inputs** self, doc\_before\_save.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If (not self.template\_warnings or not doc\_before\_save).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.template\_warnings → not doc\_before\_save.
  - Return no value.
- If \_import\_source\_fingerprint(self) differs from \_import\_source\_fingerprint(doc\_before\_save).
  - Set self.template\_warnings from empty text.
  - Return no value.
- If \_value\_mapping\_state(self) differs from \_value\_mapping\_state(doc\_before\_save).
  - Set self.template\_warnings from empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L134) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L616) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L592)

<a id="op-ab9785c2024652"></a>
### Data Import.sync value mappings from import

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_sync_value_mappings_from_import`

**Inputs** self, importer = no value.

**Declared result** bool.

**Explicit results** false · sync\_value\_mappings(self, importer.import\_file).

**Local steps**

- If not (self.import\_file or self.google\_sheets\_url).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.import\_file → self.google\_sheets\_url.
  - Return false.
- Bind dependencies sync\_value\_mappings.
- If importer is identical to no value.
  - Set importer from self.get\_importer().
- Return sync\_value\_mappings(self, importer.import\_file).

**Methods declared on this owner** [get importer](operations-010.md#op-b85e1beed3a806).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L5240) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1156) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1150)

<a id="op-aac94134fb0991"></a>
### Data Import.set delimiters flag

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_set_delimiters_flag`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not (self.import\_file or self.google\_sheets\_url).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.import\_file → self.google\_sheets\_url.
  - Return no value.
- If (self.custom\_delimiters and self.delimiter\_options).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.custom\_delimiters → self.delimiter\_options.
  - Set Platform.flags.delimiter\_options from self.delimiter\_options.
- Otherwise.
  - If self.use\_csv\_sniffer.
    - Set Platform.flags.delimiter\_options from (self.delimiter\_options or “,;\\t\|”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.delimiter\_options → “,;\\t\|”.
  - Otherwise.
    - Set Platform.flags.delimiter\_options from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L5420) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1153) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1147)

<a id="op-ee13610b424bf2"></a>
### Data Import.validate doctype

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_validate_record_type`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Importing {0} is not allowed.”.format(self.reference\_doctype) · validation helper — translated “Data Import is not allowed for {0}. Enable 'Allow Import' in DocType settings.”.format(self.reference\_doctype) · validation helper with Platform.PermissionError — translated “You do not have import permission for {0}”.format(self.reference\_doctype).

**Local steps**

- If self.reference\_doctype belongs to BLOCKED\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “Importing {0} is not allowed.”.format(self.reference\_doctype)).
- Set meta from Platform.get\_meta(self.reference\_doctype).
- If not cint(meta.allow\_import).
  - Call the validation error handler Platform.throw(translated “Data Import is not allowed for {0}. Enable 'Allow Import' in DocType settings.”.format(self.reference\_doctype)).
- If not Platform.has\_permission(self.reference\_doctype, “import”).
  - Call the validation error handler Platform.throw(translated “You do not have import permission for {0}”.format(self.reference\_doctype), Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(self.reference\_doctype, “import”).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L5612) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1159) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1153)

<a id="op-202a380c3e629f"></a>
### Data Import.validate google sheets url

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_validate_google_sheets_resource_address`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.google\_sheets\_url.
  - Return no value.
- Evaluate validate\_google\_sheets\_url(self.google\_sheets\_url).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L5959) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1158) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1152)

<a id="op-ec2acae8f75aae"></a>
### Data Import.set payload count

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_set_payload_count`

**Inputs** self, importer = no value.

**Local steps**

- If self.import\_file.
  - If importer is identical to no value.
    - Set importer from self.get\_importer().
  - Set payloads from importer.import\_file.get\_payloads\_for\_import().
  - Set self.payload\_count from len(payloads).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get importer](operations-010.md#op-b85e1beed3a806).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L6039) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1154) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1148)

<a id="op-9e6755ba1e2682"></a>
### Data Import.get preview from template

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_get_preview_from_template`

**Inputs** self, import\_file = no value, google\_sheets\_url = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value · self.get\_importer().get\_data\_for\_import\_preview().

**Local steps**

- If import\_file.
  - Set self.import\_file from import\_file.
- If google\_sheets\_url.
  - Set self.google\_sheets\_url from google\_sheets\_url.
- If not (self.import\_file or self.google\_sheets\_url).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.import\_file → self.google\_sheets\_url.
  - Return no value.
- Evaluate self.set\_delimiters\_flag().
- Return self.get\_importer().get\_data\_for\_import\_preview().

**Methods declared on this owner** [set delimiters flag](operations-009.md#op-aac94134fb0991), [get importer](operations-010.md#op-b85e1beed3a806).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L7) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1151) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1145)
