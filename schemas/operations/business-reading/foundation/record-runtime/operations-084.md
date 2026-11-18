# Record lifecycle and persistence · operations 84

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Rename doc

<a id="op-5a5fb81913adaf"></a>
### Bulk rename

`operation_foundation_model_rename_record_business_behavior_bulk_rename`

**Inputs** doctype, rows = no value, via\_console = false.

**Declared result** (list at str bitwise or no value).

**State and service calls** commit · rollback · enqueue with “Platform.utils.global\_search.rebuild\_for\_doctype”.

**Explicit results** rename\_log.

**Explicit failure paths** validation helper — translated “Please select a valid csv file with data” · validation helper — translated “Maximum {0} rows allowed”.format(max\_rows).

**Local steps**

- If not rows.
  - Call the validation error handler Platform.throw(translated “Please select a valid csv file with data”).
- If not via\_console.
  - Set max\_rows from 500.
  - If len(rows) &gt; max\_rows.
    - Call the validation error handler Platform.throw(translated “Maximum {0} rows allowed”.format(max\_rows)).
- Set rename\_log from list().
- For each row in rows.
  - If (len(row) &gt; 1 and row at 0 and row at 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(row) &gt; 1 → row at 0 → row at 1.
    - Set merge from (len(row) &gt; 2 and (row at 2 equals “1” or row at 2.lower() equals “true”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(row) &gt; 2 → (row at 2 equals “1” or row at 2.lower() equals “true”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row at 2 equals “1” → row at 2.lower() equals “true”.
    - Attempt the following.
      - If rename\_doc(doctype, row at 0, row at 1, merge = merge, rebuild\_search = false).
        - Set msg from translated “Successful: {0} to {1}”.format(row at 0, row at 1).
        - Evaluate Platform.db.commit().
      - Otherwise.
        - Set msg from no value.
    - On failure (Exception) bound to e.
      - Set msg from translated “\*\* Failed: {0} to {1}: {2}”.format(row at 0, row at 1, repr(e)).
      - Evaluate Platform.db.rollback().
    - If msg.
      - If via\_console.
        - Evaluate print(msg).
      - Otherwise.
        - Evaluate rename\_log.append(msg).
- Evaluate Platform.enqueue(“Platform.utils.global\_search.rebuild\_for\_doctype”, doctype = doctype).
- If not via\_console.
  - Return rename\_log.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.utils.global\_search.rebuild\_for\_doctype”, doctype = doctype).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L8) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L688) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1273)

<a id="op-8a8d221ae81c30"></a>
### Update linked doctypes

`operation_foundation_model_utils_rename_record_business_behavior_update_linked_record_types`

**Inputs** doctype, docname, linked\_to, value, ignore\_doctypes = no value.

**State and service calls** request set\_value on d.doctype.

**Local steps**

- Set linked\_doctype\_info\_list from get\_fetch\_fields(doctype, linked\_to, ignore\_doctypes).
- For each d in linked\_doctype\_info\_list.
  - Evaluate Platform.db.set\_value(d.doctype, mapping(d.master\_fieldname → docname, d.linked\_to\_fieldname → tuple(“!=”, value)), d.linked\_to\_fieldname, value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L6631) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L751) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1333)

<a id="op-e3fefbffe11f06"></a>
### Get fetch fields

`operation_foundation_model_utils_rename_record_business_behavior_get_fetch_fields`

**Inputs** doctype, linked\_to, ignore\_doctypes = no value.

**Declared result** list at dict.

**Explicit results** out.

**Local steps**

- Set out from list().
- Set master\_list from get\_link\_fields(doctype).
- Set linked\_to\_list from get\_link\_fields(linked\_to).
- Set product\_list from product(master\_list, linked\_to\_list).
- For each d in product\_list.
  - Set linked\_doctype\_info from Platform.\_dict().
  - If (d at 0 at “parent” equals d at 1 at “parent” and (not ignore\_doctypes or d at 0 at “parent” does not belong to ignore\_doctypes) and not d at 1 at “issingle”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d at 0 at “parent” equals d at 1 at “parent” → (not ignore\_doctypes or d at 0 at “parent” does not belong to ignore\_doctypes) → not d at 1 at “issingle”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not ignore\_doctypes → d at 0 at “parent” does not belong to ignore\_doctypes.
    - Set linked\_doctype\_info.doctype from d at 0 at “parent”.
    - Set linked\_doctype\_info.master\_fieldname from d at 0 at “fieldname”.
    - Set linked\_doctype\_info.linked\_to\_fieldname from d at 1 at “fieldname”.
    - Evaluate out.append(linked\_doctype\_info).
- Return out.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L6864) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L750) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1332)

## Service · Rename field

<a id="op-3ebfd5f877d801"></a>
### Rename field

`operation_foundation_model_utils_rename_field_business_behavior_rename_field`

**Inputs** doctype, old\_fieldname, new\_fieldname, validate = true.

**State and service calls** execute query text (UPDATE).format(new\_field.options.split(whitespace '\\n', 1) at 0, “%s”, “%s”) · execute query text (UPDATE, Singles) · execute a supplied database query.

**Explicit results** no value.

**Local steps**

- Set meta from Platform.get\_meta(doctype, cached = false).
- Set new\_field from meta.get\_field(new\_fieldname).
- If validate.
  - If not new\_field.
    - Evaluate print((((“rename\_field: ” + new\_fieldname) + “ not found in ”) + doctype)).
    - Return no value.
  - If (not meta.issingle and not Platform.db.has\_column(doctype, old\_fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not meta.issingle → not Platform.db.has\_column(doctype, old\_fieldname).
    - Evaluate print((((“rename\_field: ” + old\_fieldname) + “ not found in table for: ”) + doctype)).
    - Return no value.
- If new\_field.fieldtype belongs to table\_fields.
  - Evaluate Platform.db.sql(query text (UPDATE).format(new\_field.options.split(whitespace '\\n', 1) at 0, “%s”, “%s”), tuple(new\_fieldname, old\_fieldname)).
- Otherwise.
  - If new\_field.fieldtype does not belong to no\_value\_fields.
    - If meta.issingle.
      - Evaluate Platform.db.sql(query text (UPDATE, Singles), tuple(new\_fieldname, doctype, old\_fieldname)).
    - Otherwise.
      - Evaluate Platform.db.sql(formatted text update ′tab{doctype}′ set ′{new\_fieldname}′=′{old\_fieldname}′).
    - Evaluate update\_reports(doctype, old\_fieldname, new\_fieldname).
    - Evaluate update\_users\_report\_view\_settings(doctype, old\_fieldname, new\_fieldname).
    - If new\_field.fieldtype equals “Password”.
      - Evaluate rename\_password\_field(doctype, old\_fieldname, new\_fieldname).
- Evaluate update\_property\_setters(doctype, old\_fieldname, new\_fieldname).
- Evaluate update\_user\_settings(doctype, old\_fieldname, new\_fieldname).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L744) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1326)

<a id="op-2def6c8143c952"></a>
### Update reports

`operation_foundation_model_utils_rename_field_business_behavior_update_reports`

**Inputs** doctype, old\_fieldname, new\_fieldname.

**Record and data access** execute query text (SELECT, Report).

**State and service calls** execute query text (UPDATE, Report).

**Local steps**

- Bind local operation \_get\_new\_sort\_by for subsequent calls.
- Set reports from Platform.db.sql(query text (SELECT, Report), tuple(“%{}%”.format(old\_fieldname), “%{}%”.format(doctype)), as\_dict = true).
- For each r in reports.
  - Set report\_dict from json.loads(r.json).
  - Set new\_filters from list().
  - If report\_dict.get(“filters”).
    - For each f in report\_dict.get(“filters”).
      - If (f and len(f) &gt; 1 and f at 0 equals doctype and f at 1 equals old\_fieldname).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in f → len(f) &gt; 1 → f at 0 equals doctype → f at 1 equals old\_fieldname.
        - Evaluate new\_filters.append(list(doctype, new\_fieldname, f at 2, f at 3)).
        - Set report\_dict at “updated” from true.
      - Otherwise.
        - Evaluate new\_filters.append(f).
  - Set new\_columns from list().
  - If report\_dict.get(“columns”).
    - For each c in report\_dict.get(“columns”).
      - If (c and len(c) &gt; 1 and c at 0 equals old\_fieldname and c at 1 equals doctype).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in c → len(c) &gt; 1 → c at 0 equals old\_fieldname → c at 1 equals doctype.
        - Evaluate new\_columns.append(list(new\_fieldname, doctype)).
        - Set report\_dict at “updated” from true.
      - Otherwise.
        - Evaluate new\_columns.append(c).
  - Set new\_sort\_by from \_get\_new\_sort\_by(report\_dict, r, “sort\_by”).
  - Set new\_sort\_by\_next from \_get\_new\_sort\_by(report\_dict, r, “sort\_by\_next”).
  - If report\_dict.get(“updated”).
    - Set new\_val from json.dumps(mapping(“filters” → new\_filters, “columns” → new\_columns, “sort\_by” → new\_sort\_by, “sort\_order” → report\_dict.get(“sort\_order”), …)).
    - Evaluate Platform.db.sql(query text (UPDATE, Report), tuple(new\_val, r.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L855) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L746) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1328)

<a id="op-72cb71d1a25cb7"></a>
### Update reports.get new sort by

`operation_foundation_model_utils_rename_field_business_behavior_update_reports_get_new_sort_by`

**Inputs** report\_dict, report, key.

**Explicit results** sort\_by.

**Local steps**

- Set sort\_by from (report\_dict.get(key) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in report\_dict.get(key) → empty text.
- If sort\_by.
  - Set sort\_by from sort\_by.split(“.”).
  - If len(sort\_by) &gt; 1.
    - If (sort\_by at 0 equals doctype and sort\_by at 1 equals old\_fieldname).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sort\_by at 0 equals doctype → sort\_by at 1 equals old\_fieldname.
      - Set sort\_by from ((doctype + “.”) + new\_fieldname).
      - Set report\_dict at “updated” from true.
  - Otherwise.
    - If (report.ref\_doctype equals doctype and sort\_by at 0 equals old\_fieldname).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in report.ref\_doctype equals doctype → sort\_by at 0 equals old\_fieldname.
      - Set sort\_by from ((doctype + “.”) + new\_fieldname).
      - Set report\_dict at “updated” from true.
  - If isinstance(sort\_by, list).
    - Set sort\_by from “.”.join(sort\_by).
- Return sort\_by.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L2387) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L747) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1329)

<a id="op-d5a17b555d0022"></a>
### Update users report view settings

`operation_foundation_model_utils_rename_field_business_behavior_update_users_report_view_settings`

**Inputs** doctype, ref\_fieldname, new\_fieldname.

**Record and data access** execute query text (SELECT, Default Value).

**State and service calls** execute query text (UPDATE, Default Value).format(“%s”, “%s”).

**Local steps**

- Set user\_report\_cols from Platform.db.sql(query text (SELECT, Default Value)).
- For each tuple(key, value) in user\_report\_cols.
  - Set new\_columns from list().
  - Set columns\_modified from false.
  - For each tuple(field, field\_doctype) in json.loads(value).
    - If (field equals ref\_fieldname and field\_doctype equals doctype).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in field equals ref\_fieldname → field\_doctype equals doctype.
      - Evaluate new\_columns.append(list(new\_fieldname, field\_doctype)).
      - Set columns\_modified from true.
    - Otherwise.
      - Evaluate new\_columns.append(list(field, field\_doctype)).
  - If columns\_modified.
    - Evaluate Platform.db.sql(query text (UPDATE, Default Value).format(“%s”, “%s”), tuple(json.dumps(new\_columns), key)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L2818) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L749) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1331)

<a id="op-3855e13659da1c"></a>
### Update property setters

`operation_foundation_model_utils_rename_field_business_behavior_update_property_setters`

**Inputs** doctype, old\_fieldname, new\_fieldname.

**State and service calls** execute query text (UPDATE, Property Setter) · execute a supplied database query.

**Local steps**

- Evaluate Platform.db.sql(query text (UPDATE, Property Setter), tuple(new\_fieldname, doctype, old\_fieldname)).
- Evaluate Platform.db.sql(“update ′tabCustom Field′ set insert\_after=%s\\n\\t\\twhere insert\_after=%s and dt=%s”, tuple(new\_fieldname, old\_fieldname, doctype)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L3274) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L745) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1327)

<a id="op-3c21bbf6108496"></a>
### Update user settings

`operation_foundation_model_utils_rename_field_business_behavior_update_user_settings`

**Inputs** doctype, old\_fieldname, new\_fieldname.

**Record and data access** execute query text (SELECT).

**Local steps**

- Evaluate sync\_user\_settings().
- Set user\_settings from Platform.db.sql(query text (SELECT), tuple(doctype, formatted text %{old\_fieldname}%), as\_dict = 1).
- For each user\_setting in user\_settings.
  - Evaluate update\_user\_settings\_data(user\_setting, “docfield”, old\_fieldname, new\_fieldname).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L3508) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L748) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1330)

## Record · Report

[Record definition](../../../../data/record-types/report.json)

<a id="op-4f7323cd0b975f"></a>
### Execute

`operation_foundation_core_record_definitions_report_boilerplate_controller_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_columns().
- Set data from get\_data().
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6482) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L193) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L372)

<a id="op-281af41bfd9226"></a>
### Execute snapshot report

`operation_foundation_core_record_definitions_report_boilerplate_controller_business_behavior_execute_snapshot_report`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Bind dependencies get\_latest\_sync.
- Set columns from get\_columns().
- Set data from get\_data().
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6589) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L194) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L373)

<a id="op-eaa123e07e93de"></a>
### Get columns

`operation_foundation_core_record_definitions_report_boilerplate_controller_business_behavior_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(set(mapping(“label” → translated “Column 1”, “fieldname” → “column\_1”, “fieldtype” → “Data”)), set(mapping(“label” → translated “Column 2”, “fieldname” → “column\_2”, “fieldtype” → “Int”))).

**Local steps**

- Return list(set(mapping(“label” → translated “Column 1”, “fieldname” → “column\_1”, “fieldtype” → “Data”)), set(mapping(“label” → translated “Column 2”, “fieldname” → “column\_2”, “fieldtype” → “Int”))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6706) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L195) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L374)

<a id="op-cfb9774f5e2161"></a>
### Get data

`operation_foundation_core_record_definitions_report_boilerplate_controller_business_behavior_get_data`

**Inputs** no declared parameters.

**Declared result** list at list.

**Explicit results** list(list(“Row 1”, 1), list(“Row 2”, 2)).

**Local steps**

- Return list(list(“Row 1”, 1), list(“Row 2”, 2)).

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6892) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L196) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L375)

<a id="op-749f8671daf953"></a>
### Report.validate

`operation_foundation_core_record_definitions_report_business_behavior_report_validate`

**Inputs** self.

**Record and data access** read “DocType” via get\_value · read “Report” via get\_value.

**Explicit failure paths** validation helper — translated “Cannot edit a standard report. Please duplicate and create a new report”.

**Local steps**

- If not self.module.
  - Set self.module from Platform.db.get\_value(“DocType”, self.ref\_doctype, “module”).
- If not self.is\_standard.
  - Set self.is\_standard from “No”.
  - If (Platform.session.user equals “Administrator” and getattr(Platform.local.conf, “developer\_mode”, 0) equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user equals “Administrator” → getattr(Platform.local.conf, “developer\_mode”, 0) equals 1.
    - Set self.is\_standard from “Yes”.
- If self.is\_standard equals “No”.
  - If self.report\_type does not belong to tuple(“Report Builder”, “Custom Report”).
    - Evaluate Platform.only\_for(“Script Manager”, true).
  - If Platform.db.get\_value(“Report”, self.name, “is\_standard”) equals “Yes”.
    - Call the validation error handler Platform.throw(translated “Cannot edit a standard report. Please duplicate and create a new report”).
- If self.is\_standard equals “Yes”.
  - Evaluate self.validate\_standard\_report().
  - Set self.letter\_head from no value.
- If self.report\_type equals “Report Builder”.
  - Evaluate self.update\_report\_json().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate standard report](operations-085.md#op-a1f5034a8f4d15), [update report json](operations-085.md#op-1c28cca06e6173).

**Values supplied outside this operation** selected callable from getattr(Platform.local.conf, “developer\_mode”, 0) · effective access from Platform.only\_for(“Script Manager”, true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L25) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L235) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L411)

<a id="op-6cded45104d5c6"></a>
### Report.before insert

`operation_foundation_core_record_definitions_report_business_behavior_report_before_insert`

**Inputs** self.

**Local steps**

- Evaluate self.set\_doctype\_roles().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set doctype roles](operations-084.md#op-3c4df2519d2230).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L662) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L205) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L381)

<a id="op-6ff4c59f374633"></a>
### Report.on update

`operation_foundation_core_record_definitions_report_business_behavior_report_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.export\_doc().

If control reaches the end, it returns no value.

**Methods declared on this owner** [export doc](operations-085.md#op-0441bbb1310b0c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L713) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L228) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L404)

<a id="op-02c0df55abcef7"></a>
### Report.before export

`operation_foundation_core_record_definitions_report_business_behavior_report_before_export`

**Inputs** self, doc.

**Local steps**

- Set doc.letter\_head from no value.
- Set doc.prepared\_report from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L16) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L204) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L380)

<a id="op-56c81304df8b3e"></a>
### Report.on trash

`operation_foundation_core_record_definitions_report_business_behavior_report_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “You are not allowed to delete Standard Report”.

**Local steps**

- If self.is\_standard equals “Yes”.
  - If (not cint(getattr(Platform.local.conf, “developer\_mode”, 0)) and not Platform.flags.in\_migrate and not Platform.flags.in\_patch).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(getattr(Platform.local.conf, “developer\_mode”, 0)) → not Platform.flags.in\_migrate → not Platform.flags.in\_patch.
    - Call the validation error handler Platform.throw(translated “You are not allowed to delete Standard Report”).
  - If (Platform.conf.developer\_mode and not Platform.flags.in\_test).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → not Platform.flags.in\_test.
    - Evaluate Platform.db.after\_commit(self.delete\_report\_folder).
- Evaluate delete\_custom\_role(“report”, self.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local.conf, “developer\_mode”, 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L818) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L227) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L403)

<a id="op-382d8651804357"></a>
### Report.clear cache

`operation_foundation_core_record_definitions_report_business_behavior_report_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Bind dependencies clear\_computed\_base\_for.
- Evaluate self.update\_report\_cache().
- Evaluate clear\_computed\_base\_for(self).
- Return super().clear\_cache().

**Methods declared on this owner** [update report cache](operations-084.md#op-1b89fc439119a9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L1116) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L208) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L384)

<a id="op-1b89fc439119a9"></a>
### Report.update report cache

`operation_foundation_core_record_definitions_report_business_behavior_report_update_report_cache`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache.delete\_key(“bootinfo”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L1222) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L233) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L409)

<a id="op-5f4f31805b0e9e"></a>
### Report.delete report folder

`operation_foundation_core_record_definitions_report_business_behavior_report_delete_report_folder`

**Inputs** self.

**Local steps**

- Bind dependencies delete\_folder.
- Evaluate delete\_folder(self.module, “Report”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L1280) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L210) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L386)

<a id="op-cf01259680fb8c"></a>
### Report.get permission log options

`operation_foundation_core_record_definitions_report_business_behavior_report_get_permission_log_options`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, event.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L1363) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L221) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L397)

<a id="op-55cfa4e81539cb"></a>
### Report.get columns

`operation_foundation_core_record_definitions_report_business_behavior_report_get_columns`

**Inputs** self.

**Explicit results** list of d.as\_dict(no\_default\_fields = true, no\_child\_table\_fields = true) for d drawn from self.columns.

**Local steps**

- Return list of d.as\_dict(no\_default\_fields = true, no\_child\_table\_fields = true) for d drawn from self.columns.
  - Draw d from self.columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L1437) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L218) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L394)

<a id="op-3c4df2519d2230"></a>
### Report.set doctype roles

`operation_foundation_core_record_definitions_report_business_behavior_report_set_record_type_roles`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- If (not self.get(“roles”) and self.is\_standard equals “No”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(“roles”) → self.is\_standard equals “No”.
  - Set meta from Platform.get\_meta(self.ref\_doctype).
  - If not meta.istable.
    - Set roles from list of mapping(“role” → d.role) for d drawn from meta.permissions where d.permlevel equals 0.
      - Draw d from meta.permissions, keep a combination only if (d.permlevel equals 0).
    - Evaluate self.set(“roles”, roles).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L1527) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L231) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L407)
