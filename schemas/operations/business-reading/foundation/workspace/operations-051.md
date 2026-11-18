# Forms, reports and navigation · operations 51

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Query report

<a id="op-1ee520b75d51d0"></a>
### Get xlsx styles

`operation_foundation_desk_query_report_business_behavior_get_spreadsheet_workbook_styles`

**Inputs** metadata, report\_name = no value.

**Declared result** (dict bitwise or no value).

**Record and data access** resolve a document from “Report” via get\_doc.

**Explicit results** styles.

**Local steps**

- Bind dependencies XLSXStyleBuilder.
- Set styles from no value.
- If report\_name.
  - Set report from Platform.get\_doc(“Report”, report\_name).
  - Set styles from report.get\_xlsx\_styles\_from\_module(metadata).
- If not styles.
  - Set styles from XLSXStyleBuilder(metadata).result.
- Return styles.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0210.json#L6951) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1927) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L407)

<a id="op-f23f06b7a75eaf"></a>
### Add total row

`operation_foundation_desk_query_report_business_behavior_add_total_row`

**Inputs** result, columns, meta = no value, is\_tree = false, parent\_field = no value.

**Declared result** list at (dict bitwise or list at Any).

**Explicit results** result.

**Local steps**

- Set total\_row from (list(empty text) × len(columns)).
- Set has\_percent from list().
- Set is\_row\_dict from isinstance(result at 0, dict) when result, otherwise false.
  - Value choice on result — true gives isinstance(result at 0, dict), false gives false.
- For each tuple(col\_idx, col) in enumerate(columns).
  - Set tuple(fieldtype, options, fieldname) from tuple(no value, no value, no value).
  - If isinstance(col, str).
    - If meta.
      - Set field from meta.get\_field(col).
      - If field.
        - Set fieldtype from meta.get\_field(col).fieldtype.
        - Set fieldname from meta.get\_field(col).fieldname.
    - Otherwise.
      - Set col from col.split(“:”).
      - If len(col) &gt; 1.
        - If col at 1.
          - Set fieldtype from col at 1.
          - If “/” belongs to fieldtype.
            - Set tuple(fieldtype, options) from fieldtype.split(“/”).
        - Otherwise.
          - Set fieldtype from “Data”.
  - Otherwise.
    - Set fieldtype from col.get(“fieldtype”).
    - Set fieldname from col.get(“fieldname”).
    - Set options from col.get(“options”).
  - For each row in result.
    - If (not is\_row\_dict and col\_idx ≥ len(row)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_row\_dict → col\_idx ≥ len(row).
      - Continue with the next iteration or loop test.
    - Set cell from row.get(fieldname) when is\_row\_dict, otherwise row at col\_idx.
      - Value choice on is\_row\_dict — true gives row.get(fieldname), false gives row at col\_idx.
    - If fieldtype is identical to no value.
      - If isinstance(cell, int).
        - Set fieldtype from “Int”.
      - Otherwise.
        - If isinstance(cell, float).
          - Set fieldtype from “Float”.
    - If (fieldtype belongs to list(“Currency”, “Int”, “Float”, “Percent”, …) and flt(cell)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype belongs to list(“Currency”, “Int”, “Float”, “Percent”, …) → flt(cell).
      - If not (is\_tree and row.get(parent\_field)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_tree → row.get(parent\_field).
        - Set total\_row at col\_idx from (flt(total\_row at col\_idx) + flt(cell)).
    - If (fieldtype equals “Percent” and col\_idx does not belong to has\_percent).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype equals “Percent” → col\_idx does not belong to has\_percent.
      - Evaluate has\_percent.append(col\_idx).
    - If (fieldtype equals “Time” and cell).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype equals “Time” → cell.
      - If not total\_row at col\_idx.
        - Set total\_row at col\_idx from timedelta(hours = 0, minutes = 0, seconds = 0).
      - Set total\_row at col\_idx from (total\_row at col\_idx + cell).
  - If (fieldtype equals “Link” and options equals “Currency”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype equals “Link” → options equals “Currency”.
    - Set total\_row at col\_idx from result at 0.get(fieldname) when is\_row\_dict, otherwise result at 0 at col\_idx.
      - Value choice on is\_row\_dict — true gives result at 0.get(fieldname), false gives result at 0 at col\_idx.
- For each col\_idx in has\_percent.
  - Set total\_row at col\_idx from (flt(total\_row at col\_idx) ÷ len(result)).
- Set first\_col\_fieldtype from no value.
- If isinstance(columns at 0, str).
  - Set first\_col from columns at 0.split(“:”).
  - If len(first\_col) &gt; 1.
    - Set first\_col\_fieldtype from first\_col at 1.split(“/”, 1) at 0.
- Otherwise.
  - Set first\_col\_fieldtype from columns at 0.get(“fieldtype”).
- Set unsupported\_col\_types from tuple(“Currency”, “Int”, “Float”, “Percent”, …).
- If first\_col\_fieldtype does not belong to unsupported\_col\_types.
  - Set total\_row at 0 from translated “Total”.
- Evaluate result.append(total\_row).
- Return result.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0211.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1907) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L387)

<a id="op-44f36ea6f4cdd3"></a>
### Get data for custom field

`operation_foundation_desk_query_report_business_behavior_get_data_for_custom_field`

**Inputs** doctype, field, names = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_list.

**Explicit results** Platform.\_dict(Platform.get\_list(doctype, filters = filters, fields = list(“name”, field), as\_list = 1)).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Permitted to read {0}”.format(translated doctype).

**Local steps**

- If not Platform.has\_permission(doctype, “read”).
  - Call the validation error handler Platform.throw(translated “Not Permitted to read {0}”.format(translated doctype), Platform.PermissionError).
- Set filters from mapping().
- If names.
  - If isinstance(names, (str bitwise or bytearray)).
    - Set names from Platform.json.loads(names).
  - Evaluate filters.update(mapping(“name” → list(“in”, names))).
- Return Platform.\_dict(Platform.get\_list(doctype, filters = filters, fields = list(“name”, field), as\_list = 1)).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0211.json#L1799) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1916) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L396)

<a id="op-f4a7e606f7707f"></a>
### Get data for custom report

`operation_foundation_desk_query_report_business_behavior_get_data_for_custom_report`

**Inputs** columns, result.

**Explicit results** doc\_field\_value\_map.

**Local steps**

- Set doc\_field\_value\_map from mapping().
- For each column in columns.
  - If link\_field bound to column.get(“link\_field”).
    - If isinstance(link\_field, str).
      - Set link\_field from Platform.\_dict(mapping(“fieldname” → link\_field, “names” → list())).
    - Set fieldname from column.get(“fieldname”).
    - Set doctype from column.get(“doctype”).
    - Set row\_key from link\_field.get(“fieldname”).
    - Set names from list().
    - For each row in result.
      - If row.get(row\_key).
        - Evaluate names.append(row.get(row\_key)).
    - Set names from list(set(names)).
    - If names.
      - Set doc\_field\_value\_map at tuple(doctype, fieldname) from get\_data\_for\_custom\_field(doctype, fieldname.split(“-”) at 0, names).
- Return doc\_field\_value\_map.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L97) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1917) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L397)

<a id="op-20a7e7f99e1ac8"></a>
### Save report

`operation_foundation_desk_query_report_business_behavior_save_report`

**Inputs** reference\_report, report\_name, columns, filters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Report” via exists · resolve a document from “Report” via get\_doc · resolve a document from mapping(“doctype” → “Report”, “report\_name” → report\_name, “json” → formatted text {"columns":{columns},"filters":{filters}}, “ref\_doctype” → report\_doc.ref\_doctype, …) via get\_doc.

**State and service calls** call save on report · msgprint with translated “Report updated successfully” · call insert on Platform.get\_doc(mapping(“doctype” → “Report”, “report\_name” → report\_name, “json” → formatted text {"columns":{columns},"filters":{filters}}, “ref\_doctype” → report\_doc.ref\_doctype, …)) · msgprint with translated “{0} saved successfully”.format(translated new\_report.name).

**Explicit results** docname · new\_report.name.

**Local steps**

- Set report\_doc from get\_report\_doc(reference\_report).
- Set docname from Platform.db.exists(“Report”, mapping(“report\_name” → report\_name, “is\_standard” → “No”, “report\_type” → “Custom Report”)).
- If docname.
  - Set report from Platform.get\_doc(“Report”, docname).
  - Set existing\_jd from Platform.parse\_json((report.json or “{}”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in report.json → “{}”.
  - Set existing\_jd at “columns” from Platform.parse\_json(columns).
  - Set existing\_jd at “filters” from Platform.parse\_json(filters).
  - Evaluate report.update(mapping(“json” → json.dumps(existing\_jd, separators = tuple(“,”, “:”)))).
  - Evaluate report.save().
  - Evaluate Platform.msgprint(translated “Report updated successfully”).
  - Return docname.
- Otherwise.
  - Set new\_report from Platform.get\_doc(mapping(“doctype” → “Report”, “report\_name” → report\_name, “json” → formatted text {"columns":{columns},"filters":{filters}}, “ref\_doctype” → report\_doc.ref\_doctype, …)).insert(ignore\_perm ….
  - Evaluate Platform.msgprint(translated “{0} saved successfully”.format(translated new\_report.name)).
  - Return new\_report.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L104) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1935) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L415)

<a id="op-9221a4a4c15ab6"></a>
### Get filtered data

`operation_foundation_desk_query_report_business_behavior_get_filtered_data`

**Inputs** ref\_doctype, columns, data, user.

**Explicit results** result.

**Local steps**

- Set result from list().
- Set linked\_doctypes from get\_linked\_doctypes(columns, data).
- Set match\_filters\_per\_doctype from get\_user\_match\_filters(linked\_doctypes, user = user).
- Set shared from Platform.share.get\_shared(ref\_doctype, user).
- Set columns\_dict from get\_columns\_dict(columns).
- Set ref\_doctype\_meta from Platform.get\_meta(ref\_doctype).
- Set role\_permissions from get\_role\_permissions(ref\_doctype\_meta, user).
- Set if\_owner from role\_permissions.get(“if\_owner”, mapping()).get(“report”).
- If ref\_doctype\_meta.get\_masked\_fields().
  - Bind dependencies mask\_field\_value.
  - For each field in ref\_doctype\_meta.get\_masked\_fields().
    - For each row in data.
      - Set val from row.get(field.fieldname).
      - Set row at field.fieldname from mask\_field\_value(field, val).
- If match\_filters\_per\_doctype.
  - For each row in data.
    - If (linked\_doctypes.get(ref\_doctype) and shared and row.get(linked\_doctypes at ref\_doctype) belongs to shared).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in linked\_doctypes.get(ref\_doctype) → shared → row.get(linked\_doctypes at ref\_doctype) belongs to shared.
      - Evaluate result.append(row).
    - Otherwise.
      - If has\_match(row, linked\_doctypes, match\_filters\_per\_doctype, ref\_doctype, …).
        - Evaluate result.append(row).
- Otherwise.
  - Set result from list(data).
- Return result.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L98) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1918) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L398)

<a id="op-b3ce3a12ac8332"></a>
### Has match

`operation_foundation_desk_query_report_business_behavior_has_match`

**Inputs** row, linked\_doctypes, doctype\_match\_filters, ref\_doctype, if\_owner, columns\_dict, user.

**Record and data access** read dt via exists.

**Explicit results** resultant\_match.

**Local steps**

- Set resultant\_match from true.
- If not row.
  - Return resultant\_match.
- For each tuple(doctype, filter\_list) in doctype\_match\_filters.items().
  - Set matched\_for\_doctype from false.
  - If (doctype equals ref\_doctype and if\_owner).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals ref\_doctype → if\_owner.
    - Set idx from linked\_doctypes.get(“User”).
    - If (idx is distinct from no value and row at idx equals user and columns\_dict at idx equals columns\_dict.get(“owner”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in idx is distinct from no value → row at idx equals user → columns\_dict at idx equals columns\_dict.get(“owner”).
      - Set matched\_for\_doctype from true.
  - If not matched\_for\_doctype.
    - For each match\_filters in filter\_list.
      - Set match from true.
      - For each tuple(dt, idx) in linked\_doctypes.items().
        - If (dt equals “User” and columns\_dict at idx equals columns\_dict.get(“owner”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt equals “User” → columns\_dict at idx equals columns\_dict.get(“owner”).
          - Continue with the next iteration or loop test.
        - Set cell\_value from no value.
        - If isinstance(row, dict).
          - Set cell\_value from row.get(idx).
        - Otherwise.
          - If isinstance(row, (list bitwise or tuple)).
            - Set cell\_value from row at idx.
        - If (dt belongs to match\_filters and cell\_value does not belong to match\_filters.get(dt) and Platform.db.exists(dt, cell\_value)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt belongs to match\_filters → cell\_value does not belong to match\_filters.get(dt) → Platform.db.exists(dt, cell\_value).
          - Set match from false.
          - Leave the innermost loop without its normal-exhaustion alternative.
        - If match.
          - Set match from has\_unrestricted\_read\_access(doctype = ref\_doctype, user = Platform.session.user).
      - Set matched\_for\_doctype from (matched\_for\_doctype or match).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in matched\_for\_doctype → match.
      - If matched\_for\_doctype.
        - Leave the innermost loop without its normal-exhaustion alternative.
  - Set resultant\_match from (resultant\_match and matched\_for\_doctype).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in resultant\_match → matched\_for\_doctype.
  - If not resultant\_match.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return resultant\_match.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0211.json#L4305) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1929) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L409)

<a id="op-bcf055ee2b28e2"></a>
### Has unrestricted read access

`operation_foundation_desk_query_report_business_behavior_has_unrestricted_read_access`

**Inputs** doctype, user.

**Wrappers, in declaration order** request\_cache.

**Record and data access** read “DocPerm” via exists · read “Custom DocPerm” via exists.

**Explicit results** has\_perm.

**Local steps**

- Set roles from get\_roles(user).
- Set permission\_filters from mapping(“parent” → doctype, “role” → list(“in”, roles), “permlevel” → 0, “read” → 1, …).
- Set standard\_perm\_exists from Platform.db.exists(“DocPerm”, permission\_filters).
- Set custom\_perm\_exists from Platform.db.exists(“Custom DocPerm”, permission\_filters).
- Set has\_perm from bool((custom\_perm\_exists or standard\_perm\_exists)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in custom\_perm\_exists → standard\_perm\_exists.
- Return has\_perm.

**Values supplied outside this operation** effective access from get\_roles(user).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0211.json#L5159) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1930) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L410)

<a id="op-3f1a2a7a46f021"></a>
### Get linked doctypes

`operation_foundation_desk_query_report_business_behavior_get_linked_record_types`

**Inputs** columns, data.

**Explicit results** linked\_doctypes.

**Local steps**

- Set linked\_doctypes from mapping().
- Set columns\_dict from get\_columns\_dict(columns).
- For each idx in range(len(columns)).
  - Set df from columns\_dict at idx.
  - If df.get(“fieldtype”) equals “Link”.
    - If (data and isinstance(data at 0, (list bitwise or tuple))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → isinstance(data at 0, (list bitwise or tuple)).
      - Set linked\_doctypes at df at “options” from idx.
    - Otherwise.
      - Set linked\_doctypes at df at “options” from df at “fieldname”.
- Set columns\_with\_value from list().
- For each row in data.
  - If row.
    - If len(row) differs from len(columns\_with\_value).
      - If isinstance(row, (list bitwise or tuple)).
        - Set row from enumerate(row).
      - Otherwise.
        - If isinstance(row, dict).
          - Set row from row.items().
      - For each tuple(col, val) in row.
        - If (val and col does not belong to columns\_with\_value).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in val → col does not belong to columns\_with\_value.
          - Evaluate columns\_with\_value.append(col).
- Set items from list(linked\_doctypes.items()).
- For each tuple(doctype, key) in items.
  - If key does not belong to columns\_with\_value.
    - Remove linked\_doctypes at doctype.
- Return linked\_doctypes.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0211.json#L5458) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1919) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L399)

<a id="op-81e0131800b17a"></a>
### Get columns dict

`operation_foundation_desk_query_report_business_behavior_get_columns_mapping`

**Inputs** columns.

**Explicit results** columns\_dict.

**Local steps**

- Set columns\_dict from Platform.\_dict().
- For each tuple(idx, col) in enumerate(columns).
  - Set col\_dict from get\_column\_as\_dict(col).
  - Set columns\_dict at idx from col\_dict.
  - Set columns\_dict at col\_dict at “fieldname” from col\_dict.
- Return columns\_dict.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0211.json#L6141) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1915) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L395)

<a id="op-068d9d0e6e69f0"></a>
### Get column as dict

`operation_foundation_desk_query_report_business_behavior_get_column_as_mapping`

**Inputs** col.

**Explicit results** col\_dict.

**Local steps**

- Set col\_dict from Platform.\_dict().
- If isinstance(col, str).
  - Set col from col.split(“:”).
  - If len(col) &gt; 1.
    - If “/” belongs to col at 1.
      - Set tuple(col\_dict at “fieldtype”, col\_dict at “options”) from col at 1.split(“/”).
    - Otherwise.
      - Set col\_dict at “fieldtype” from col at 1.
    - If len(col) equals 3.
      - Set col\_dict at “width” from col at 2.
  - Set col\_dict at “label” from col at 0.
  - Set col\_dict at “fieldname” from Platform.scrub(col at 0).
- Otherwise.
  - Evaluate col\_dict.update(col).
  - If “fieldname” does not belong to col\_dict.
    - Set col\_dict at “fieldname” from Platform.scrub(col\_dict at “label”).
- Return col\_dict.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0211.json#L6319) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1914) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L394)

<a id="op-c8c9fcef57d2a1"></a>
### Get user match filters

`operation_foundation_desk_query_report_business_behavior_get_user_match_filters`

**Inputs** doctypes, user.

**Explicit results** match\_filters.

**Local steps**

- Set match\_filters from mapping().
- For each dt in doctypes.
  - Set filter\_list from Platform.desk.reportview.build\_match\_conditions(dt, user, false).
  - If filter\_list.
    - Set match\_filters at dt from filter\_list.
- Return match\_filters.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0211.json#L6849) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1928) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L408)

<a id="op-4ad9bc8263f888"></a>
### Validate filters permissions

`operation_foundation_desk_query_report_business_behavior_validate_filters_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** report\_name, filters, user, js\_filters.

**Explicit result forms** no value.

**Observed service boundaries** effective access lookup, record lookup, validation or user-notification service.

**Local structure** 7 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1938) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L418)

<a id="op-14b8533a904c19"></a>
### Translate report data

`operation_foundation_desk_query_report_business_behavior_translate_report_data`

**Inputs** data, total\_row.

**Explicit results** data.

**Local steps**

- For each d in data at slice no value to negative 1 when total\_row, otherwise data.
  - Value choice on total\_row — true gives data at slice no value to negative 1, false gives data.
  - For each tuple(field, value) in d.items().
    - If isinstance(value, str).
      - Set d at field from translated value.
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0212.json#L738) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1936) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L416)

## Service · Realtime

<a id="op-cd19c4bc357651"></a>
### Publish doc change

`operation_foundation_binding_foundation_studio_realtime_publish_doc_change`

**Inputs** doctype, name, studio\_app = no value, source = no value.

**State and service calls** publish realtime with “studio\_doc\_update”.

**Explicit results** no value.

**Local steps**

- If (Platform.flags.in\_migrate or Platform.flags.in\_install or Platform.flags.in\_patch).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_migrate → Platform.flags.in\_install → Platform.flags.in\_patch.
  - Return no value.
- Evaluate Platform.publish\_realtime(“studio\_doc\_update”, mapping(“doctype” → doctype, “name” → name, “studio\_app” → studio\_app, “source” → (source or “disk” when Platform.flags.in\_import, otherwise “save”)), room =  ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source → “disk” when Platform.flags.in\_import, otherwise “save”.
  - Value choice on Platform.flags.in\_import — true gives “disk”, false gives “save”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“studio\_doc\_update”, mapping(“doctype” → doctype, “name” → name, “studio\_app” → studio\_app, “source” → (source or “disk” when Platform.flags.in\_import, otherwise “save”)), room =  ….

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L258) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L65) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L153)

## Service · Registry

<a id="op-871556ca12d813"></a>
### Tool.schema

`operation_foundation_binding_foundation_studio_ai_agent_registry_tool_schema`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“type” → “function”, “function” → mapping(“name” → self.name, “description” → self.description, “parameters” → self.parameters)).

**Local steps**

- Return mapping(“type” → “function”, “function” → mapping(“name” → self.name, “description” → self.description, “parameters” → self.parameters)).

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L81) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1768) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1744)

<a id="op-9d6707d65780f1"></a>
### Tool Registry.initialize

`operation_foundation_binding_foundation_studio_ai_agent_registry_toolregistry_init`

**Inputs** self.

**Local steps**

- Set self.\_tools from mapping().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L84) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1771) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1747)

<a id="op-4f729ac3e9c79c"></a>
### Tool Registry.register

`operation_foundation_binding_foundation_studio_ai_agent_registry_toolregistry_register`

**Inputs** self, tool.

**Declared result** Tool.

**Explicit results** tool.

**Local steps**

- Set self.\_tools at tool.name from tool.
- Return tool.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L86) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1773) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1749)

<a id="op-904b3261c0f6bc"></a>
### Tool Registry.extend

`operation_foundation_binding_foundation_studio_ai_agent_registry_toolregistry_extend`

**Inputs** self, tools.

**Declared result** no value.

**Local steps**

- For each tool in tools.
  - Evaluate self.register(tool).

If control reaches the end, it returns no value.

**Methods declared on this owner** [register](operations-051.md#op-4f729ac3e9c79c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L82) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1769) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1745)

<a id="op-eba839d241ec75"></a>
### Tool Registry.get

`operation_foundation_binding_foundation_studio_ai_agent_registry_toolregistry_get`

**Inputs** self, name.

**Declared result** (Tool bitwise or no value).

**Explicit results** self.\_tools.get(name).

**Local steps**

- Return self.\_tools.get(name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L83) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1770) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1746)

<a id="op-d7ba8a6faee948"></a>
### Tool Registry.side

`operation_foundation_binding_foundation_studio_ai_agent_registry_toolregistry_side`

**Inputs** self, name.

**Declared result** ToolSide.

**Explicit results** tool.side when tool, otherwise “client”.

**Local steps**

- Set tool from self.\_tools.get(name).
- Return tool.side when tool, otherwise “client”.
  - Value choice on tool — true gives tool.side, false gives “client”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L88) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1775) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1751)

<a id="op-89751d23c88a60"></a>
### Tool Registry.schemas

`operation_foundation_binding_foundation_studio_ai_agent_registry_toolregistry_schemas`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** list of tool.schema() for tool drawn from self.\_tools.values().

**Local steps**

- Return list of tool.schema() for tool drawn from self.\_tools.values().
  - Draw tool from self.\_tools.values().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L87) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1774) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1750)

<a id="op-9e7112ca8aa887"></a>
### Tool Registry.names

`operation_foundation_binding_foundation_studio_ai_agent_registry_toolregistry_names`

**Inputs** self.

**Declared result** list at str.

**Explicit results** list(self.\_tools).

**Local steps**

- Return list(self.\_tools).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L85) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1772) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1748)

<a id="op-61e4a6b9b4ad69"></a>
### Build shared registry

`operation_foundation_binding_foundation_studio_ai_agent_registry_build_shared_registry`

**Inputs** no declared parameters.

**Declared result** ToolRegistry.

**Explicit results** registry.

**Local steps**

- Bind dependencies bindings, blocks, conversation, data, generate, interactivity, introspect, query.
- Set registry from ToolRegistry().
- Evaluate registry.extend(generate.TOOLS).
- Evaluate registry.extend(blocks.TOOLS).
- Evaluate registry.extend(query.TOOLS).
- Evaluate registry.extend(conversation.TOOLS).
- Evaluate registry.extend(introspect.TOOLS).
- Evaluate registry.extend(data.TOOLS).
- Evaluate registry.extend(bindings.TOOLS).
- Evaluate registry.extend(interactivity.TOOLS).
- Return registry.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L78) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1765) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1741)
