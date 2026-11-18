# Forms, reports and navigation · operations 53

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Reportview

<a id="op-c21118cda6e594"></a>
### Compress

`operation_foundation_desk_reportview_business_behavior_compress`

**Inputs** data, args = no value.

**Explicit results** data · mapping(“keys” → keys, “values” → values, “user\_info” → user\_info).

**Local steps**

- Bind dependencies add\_total\_row.
- Set user\_info from mapping().
- If not data.
  - Return data.
- If args is identical to no value.
  - Set args from mapping().
- Set values from list().
- Set keys from list(data at 0).
- For each row in data.
  - Evaluate values.append(list of row.get(key) for key drawn from keys).
    - Draw key from keys.
  - If row.get(“\_assign”, empty text).
    - For each user in json.loads(row.\_assign).
      - Evaluate add\_user\_info(user, user\_info).
- If args.get(“add\_total\_row”).
  - Set meta from Platform.get\_meta(args.doctype).
  - Set values from add\_total\_row(values, keys, meta).
- Return mapping(“keys” → keys, “values” → values, “user\_info” → user\_info).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0213.json#L334) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L932) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1374)

<a id="op-e4e7cab560a901"></a>
### Save report

`operation_foundation_desk_reportview_business_behavior_save_report`

**Inputs** name, doctype, report\_settings.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Record and data access** read “Report” via exists · resolve a document from “Report” via get\_doc.

**State and service calls** request new\_doc for “Report” · call save on report · msgprint with translated “Report {0} saved”.format(Platform.bold(report.name)).

**Explicit results** report.name.

**Explicit failure paths** validation helper — translated “Standard Reports cannot be edited” · validation helper — translated “Only reports of type Report Builder can be edited” · validation helper with Platform.PermissionError — translated “Insufficient Permissions for editing Report” · validation helper with Platform.PermissionError — translated “You don't have permission to create Report records.” · validation helper with Platform.PermissionError — translated “You don't have permission to create report for {0}”.format(translated doctype).

**Local steps**

- If Platform.db.exists(“Report”, name).
  - Set report from Platform.get\_doc(“Report”, name).
  - If report.is\_standard equals “Yes”.
    - Call the validation error handler Platform.throw(translated “Standard Reports cannot be edited”).
  - If report.report\_type differs from “Report Builder”.
    - Call the validation error handler Platform.throw(translated “Only reports of type Report Builder can be edited”).
  - If (report.owner differs from Platform.session.user and not Platform.has\_permission(“Report”, “write”, doc = report)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in report.owner differs from Platform.session.user → not Platform.has\_permission(“Report”, “write”, doc = report).
    - Call the validation error handler Platform.throw(translated “Insufficient Permissions for editing Report”, Platform.PermissionError).
- Otherwise.
  - If not Platform.has\_permission(“Report”, “create”).
    - Call the validation error handler Platform.throw(translated “You don't have permission to create Report records.”, Platform.PermissionError).
  - If not Platform.has\_permission(doctype, “read”).
    - Call the validation error handler Platform.throw(translated “You don't have permission to create report for {0}”.format(translated doctype), Platform.PermissionError).
  - Set report from Platform.new\_doc(“Report”).
  - Set report.report\_name from name.
  - Set report.ref\_doctype from doctype.
- Set settings from json.loads(report\_settings).
- If (isinstance(settings, dict) and isinstance(group\_by bound to settings.get(“group\_by”), dict)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(settings, dict) → isinstance(group\_by bound to settings.get(“group\_by”), dict).
  - Evaluate \_validate\_group\_by\_args(group\_by, report.ref\_doctype).
- Set report.report\_type from “Report Builder”.
- Set report.json from report\_settings.
- Evaluate report.save(ignore\_permissions = true).
- Evaluate Platform.msgprint(translated “Report {0} saved”.format(Platform.bold(report.name)), indicator = “green”, alert = true).
- Return report.name.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Report”, “write”, doc = report), Platform.has\_permission(“Report”, “create”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L63) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L961) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1401)

<a id="op-ec776b14d8b202"></a>
### Delete report

`operation_foundation_desk_reportview_business_behavior_delete_report`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “DELETE”)).

**Record and data access** resolve a document from “Report” via get\_doc.

**State and service calls** msgprint with translated “Report {0} deleted”.format(Platform.bold(report.name)).

**Explicit failure paths** validation helper — translated “Standard Reports cannot be deleted” · validation helper — translated “Only reports of type Report Builder can be deleted” · validation helper with Platform.PermissionError — translated “Insufficient Permissions for deleting Report”.

**Local steps**

- Set report from Platform.get\_doc(“Report”, name).
- If report.is\_standard equals “Yes”.
  - Call the validation error handler Platform.throw(translated “Standard Reports cannot be deleted”).
- If report.report\_type differs from “Report Builder”.
  - Call the validation error handler Platform.throw(translated “Only reports of type Report Builder can be deleted”).
- If (report.owner differs from Platform.session.user and not Platform.has\_permission(“Report”, “delete”, doc = report)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in report.owner differs from Platform.session.user → not Platform.has\_permission(“Report”, “delete”, doc = report).
  - Call the validation error handler Platform.throw(translated “Insufficient Permissions for deleting Report”, Platform.PermissionError).
- Evaluate report.delete(ignore\_permissions = true).
- Evaluate Platform.msgprint(translated “Report {0} deleted”.format(Platform.bold(report.name)), indicator = “green”, alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Report”, “delete”, doc = report).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L52) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L935) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1377)

<a id="op-19496c5e9865cd"></a>
### Export query

`operation_foundation_desk_reportview_business_behavior_export_query`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Record and data access** read “User” via get\_cached\_value.

**State and service calls** enqueue with “Platform.desk.reportview.run\_report\_view\_export\_job” · msgprint with translated “Your report is being generated in the background. You will receive an email on {0} with a download link once …”.format(user\_email).

**Explicit results** no value · \_export\_query(form\_params, csv\_params).

**Local steps**

- Bind dependencies pop\_csv\_params.
- Set form\_params from get\_form\_params().
- Set form\_params at “limit\_page\_length” from no value.
- Set form\_params at “as\_list” from true.
- Set csv\_params from pop\_csv\_params(form\_params).
- Evaluate form\_params.pop(“with\_link\_titles”, no value).
- Set export\_in\_background from int(form\_params.pop(“export\_in\_background”, 0)).
- If export\_in\_background.
  - Set user from Platform.session.user.
  - Set user\_email from Platform.get\_cached\_value(“User”, user, “email”).
  - Evaluate Platform.enqueue(“Platform.desk.reportview.run\_report\_view\_export\_job”, user\_email = user\_email, form\_params = form\_params, csv\_params = csv\_params, queue = “long”, …).
  - Evaluate Platform.msgprint(translated “Your report is being generated in the background. You will receive an email on {0} with a download link once …”.format(user\_email)).
  - Return no value.
- Return \_export\_query(form\_params, csv\_params).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“User”, user, “email”) · service or queued work from Platform.enqueue(“Platform.desk.reportview.run\_report\_view\_export\_job”, user\_email = user\_email, form\_params = form\_params, csv\_params = csv\_params, queue = “long”, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L53) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L937) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1379)

<a id="op-a835d6ad88e479"></a>
### Run report view export job

`operation_foundation_desk_reportview_business_behavior_run_report_view_export_job`

**Inputs** user\_email, form\_params, csv\_params.

**Local steps**

- Bind dependencies send\_report\_email.
- Set tuple(report\_name, file\_extension, content) from \_export\_query(form\_params, csv\_params, populate\_response = false).
- Evaluate send\_report\_email(user\_email, report\_name, file\_extension, content, attached\_to\_name = report\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0213.json#L2739) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L960) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1400)

<a id="op-8edb74f1e89b6d"></a>
### Export query

`operation_foundation_desk_reportview_business_behavior_export_query_2`

**Inputs** form\_params, csv\_params, populate\_response = true.

**Explicit results** tuple(title, file\_extension, content).

**Explicit failure paths** Platform.PermissionError(translated “You are not allowed to export {} doctype”.format(doctype)).

**Local steps**

- Bind dependencies get\_csv\_bytes, provide\_binary\_file.
- Bind dependencies get\_default\_xlsx\_styles, handle\_html, make\_xlsx.
- Set doctype from form\_params.pop(“doctype”).
- Set owner\_field from formatted text ′tab{doctype}′.′owner′.
- If isinstance(form\_params at “fields”, list).
  - Evaluate form\_params at “fields”.append(owner\_field).
- Otherwise.
  - If isinstance(form\_params at “fields”, tuple).
    - Set form\_params at “fields” from (form\_params at “fields” + tuple(owner\_field)).
- Set file\_format\_type from form\_params.pop(“file\_format\_type”).
- Set title from form\_params.pop(“title”, doctype).
- Set add\_totals\_row from 1 when form\_params.pop(“add\_totals\_row”, no value) equals “1”, otherwise no value.
  - Value choice on form\_params.pop(“add\_totals\_row”, no value) equals “1” — true gives 1, false gives no value.
- Set translate\_values from 1 when form\_params.pop(“translate\_values”, no value) equals “1”, otherwise no value.
  - Value choice on form\_params.pop(“translate\_values”, no value) equals “1” — true gives 1, false gives no value.
- Set visible\_names from form\_params.pop(“visible\_names”, no value).
- If isinstance(visible\_names, str).
  - Set visible\_names from Platform.parse\_json(visible\_names).
- If not (isinstance(visible\_names, list) and visible\_names).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(visible\_names, list) → visible\_names.
  - Set visible\_names from no value.
- If selection bound to form\_params.pop(“selected\_items”, no value).
  - Set form\_params at “filters” from mapping(“name” → tuple(“in”, json.loads(selection))).
- If visible\_names.
  - Set form\_params at “filters” from mapping(“name” → tuple(“in”, visible\_names)).
  - Set form\_params at “order\_by” from no value.
  - Evaluate form\_params.pop(“page\_length”, no value).
  - Evaluate form\_params.pop(“limit\_page\_length”, no value).
  - Evaluate form\_params.pop(“start”, no value).
- Evaluate make\_access\_log(doctype = doctype, file\_type = file\_format\_type, report\_name = form\_params.report\_name, filters = form\_params.filters).
- Set db\_query from DatabaseQuery(doctype).
- Set ret from db\_query.execute(expanded names form\_params).
- If visible\_names.
  - Set ret from \_reorder\_by\_visible\_names(ret, form\_params.get(“fields”, list()), doctype, visible\_names).
- If not Platform.permissions.can\_export(doctype).
  - If Platform.permissions.can\_export(doctype, is\_owner = true).
    - For each row in ret.
      - If row at negative 1 differs from Platform.session.user.
        - Raise Platform.PermissionError(translated “You are not allowed to export {} doctype”.format(doctype)).
  - Otherwise.
    - Raise Platform.PermissionError(translated “You are not allowed to export {} doctype”.format(doctype)).
- If add\_totals\_row.
  - Set ret from append\_totals\_row(ret).
- Set fields\_info from get\_field\_info(db\_query.fields, doctype).
- Set labels from list of info at “label” for info drawn from fields\_info.
  - Draw info from fields\_info.
- Set sr\_label from translated “Sr”.
- Set data from list(list(sr\_label, expanded labels)).
- Set processed\_data from list().
- If (Platform.local.lang equals “en” or not translate\_values).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.lang equals “en” → not translate\_values.
  - Evaluate data.extend(generator of list((i + 1), expanded list(row)) for tuple(i, row) drawn from enumerate(ret)).
    - Draw tuple(i, row) from enumerate(ret).
- Otherwise.
  - If translate\_values.
    - Set translatable\_fields from list of field at “translatable” for field drawn from fields\_info.
      - Draw field from fields\_info.
    - Set processed\_data from list().
    - For each tuple(i, row) in enumerate(ret).
      - Set processed\_row from (list((i + 1)) + list of translated value when translatable\_fields at idx, otherwise value for tuple(idx, value) drawn from enumerate(row)).
        - Draw tuple(idx, value) from enumerate(row).
        - Value choice on translatable\_fields at idx — true gives translated value, false gives value.
      - Evaluate processed\_data.append(processed\_row).
    - Evaluate data.extend(processed\_data).
- Set data from handle\_duration\_fieldtype\_values(doctype, data, db\_query.fields).
- If file\_format\_type equals “CSV”.
  - Set file\_extension from “csv”.
  - Set content from get\_csv\_bytes(list of list of handle\_html(v) when isinstance(v, str), otherwise v for v drawn from r for r drawn from data, csv\_params).
    - Draw r from data.
    - Draw v from r.
    - Value choice on isinstance(v, str) — true gives handle\_html(v), false gives v.
- Otherwise.
  - If file\_format\_type equals “Excel”.
    - Set file\_extension from “xlsx”.
    - Set styles from get\_default\_xlsx\_styles(columns = list(mapping(“fieldname” → “sr”, “label” → sr\_label, “fieldtype” → “Int”), expanded fields\_info), data = data at slice 1 to no value, has\_total\_row = bool(add\_totals\_row)).
    - Set content from make\_xlsx(data, doctype, styles = styles).getvalue().
- If not populate\_response.
  - Return tuple(title, file\_extension, content).
- Evaluate provide\_binary\_file(translated title, file\_extension, content).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L54) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L938) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1380)

<a id="op-5a925b3243f978"></a>
### Reorder by visible names

`operation_foundation_desk_reportview_business_behavior_reorder_by_visible_names`

**Inputs** ret, fields, doctype, visible\_names.

**Explicit results** ret · reordered.

**Local steps**

- Set name\_field from formatted text ′tab{doctype}′.′name′.
- Set name\_idx from no value.
- For each tuple(i, field) in enumerate(fields).
  - If not isinstance(field, str).
    - Continue with the next iteration or loop test.
  - If (field equals name\_field or field equals “name”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in field equals name\_field → field equals “name”.
    - Set name\_idx from i.
    - Leave the innermost loop without its normal-exhaustion alternative.
- If name\_idx is identical to no value.
  - Return ret.
- Set rows\_by\_name from mapping().
- For each row in ret.
  - Evaluate rows\_by\_name.setdefault(row at name\_idx, deque()).append(row).
- Set reordered from list().
- For each name in visible\_names.
  - Set group from rows\_by\_name.get(name).
  - If group.
    - Evaluate reordered.append(group.popleft()).
- Return reordered.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L62) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L959) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1399)

<a id="op-2f63b3930d977c"></a>
### Append totals row

`operation_foundation_desk_reportview_business_behavior_append_totals_row`

**Inputs** data.

**Explicit results** data.

**Local steps**

- If not data.
  - Return data.
- Set data from list(data).
- Set totals from list().
- Evaluate totals.extend((list(empty text) × len(data at 0))).
- For each row in data.
  - For each i in range(len(row)).
    - If isinstance(row at i, (float bitwise or int)).
      - Set totals at i from ((totals at i or 0) + row at i).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in totals at i → 0.
- If not isinstance(totals at 0, (int bitwise or float)).
  - Set totals at 0 from “Total”.
- Evaluate data.append(totals).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L50) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L929) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1371)

<a id="op-f447591fcc25bf"></a>
### Get field info

`operation_foundation_desk_reportview_business_behavior_get_field_info`

**Inputs** fields, parent\_doctype.

**Explicit results** field\_info.

**Local steps**

- Bind dependencies get\_default\_df.
- Set field\_info from list().
- For each field in fields.
  - Set df from no value.
  - Set doctype from no value.
  - Attempt the following.
    - Set tuple(doctype, fieldname) from parse\_field(field).
  - On failure (ValueError).
    - If isinstance(field, dict).
      - Set fieldname from next(generator of f for f drawn from field where f differs from “as”).
        - Draw f from field, keep a combination only if (f differs from “as”).
    - Otherwise.
      - Set fieldname from field.split(“(”, 1) at 0.
    - Set fieldname from fieldname.capitalize().
  - Set doctype from (doctype or parent\_doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → parent\_doctype.
  - Set options from no value.
  - If (doctype equals parent\_doctype and fieldname equals “name”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals parent\_doctype → fieldname equals “name”.
    - Set label from \_(“ID”, context = “Label of name column in report”).
    - Set fieldtype from “Data”.
    - Set translatable from true.
  - Otherwise.
    - Set meta from Platform.get\_meta(doctype).
    - Set df from (meta.get\_field(fieldname) or get\_default\_df(fieldname)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.get\_field(fieldname) → get\_default\_df(fieldname).
    - If df.
      - Set fieldname from df.fieldname.
      - Set label from translated df.label when df.label, otherwise (meta.get\_label(fieldname) or empty text).
        - Value choice on df.label — true gives translated df.label, false gives (meta.get\_label(fieldname) or empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.get\_label(fieldname) → empty text.
      - Set fieldtype from df.fieldtype.
      - Set translatable from (df.translatable or false).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.translatable → false.
      - Set options from df.options.
      - If (df.fieldtype equals “Link” and options and Platform.get\_meta(options).translated\_doctype).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Link” → options → Platform.get\_meta(options).translated\_doctype.
        - Set translatable from true.
    - Otherwise.
      - Set label from translated Platform.unscrub(fieldname).
      - Set fieldtype from “Data”.
      - Set translatable from false.
    - If doctype differs from parent\_doctype.
      - Update label using + formatted text  ({translated doctype}).
  - Evaluate field\_info.append(mapping(“fieldname” → fieldname, “label” → label, “fieldtype” → fieldtype, “translatable” → translatable, …)).
- Return field\_info.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L57) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L943) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1384)

<a id="op-3d1ad9084e716c"></a>
### Handle duration fieldtype values

`operation_foundation_desk_reportview_business_behavior_handle_duration_fieldtype_values`

**Inputs** parent\_doctype, data, fields.

**Explicit results** data.

**Local steps**

- For each field in fields.
  - Attempt the following.
    - Set tuple(doctype, fieldname) from parse\_field(field).
  - On failure (ValueError).
    - Continue with the next iteration or loop test.
  - Set doctype from (doctype or parent\_doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → parent\_doctype.
  - Set df from Platform.get\_meta(doctype).get\_field(fieldname).
  - If (df and df.fieldtype equals “Duration”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype equals “Duration”.
    - Set index from (fields.index(field) + 1).
    - For each i in range(1, len(data)).
      - Set val\_in\_seconds from data at i at index.
      - If val\_in\_seconds.
        - Set duration\_val from format\_duration(val\_in\_seconds, df.hide\_days).
        - Set data at i at index from duration\_val.
- Return data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0213.json#L6936) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L953) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1394)

<a id="op-c545562304b5af"></a>
### Parse field

`operation_foundation_desk_reportview_business_behavior_parse_field`

**Inputs** field.

**Declared result** tuple at tuple((str bitwise or no value), str).

**Explicit results** tuple(table at slice 4 to negative 1, column.strip(“′”)) · tuple(no value, key.strip(“′”)).

**Explicit failure paths** ValueError.

**Local steps**

- If isinstance(field, dict).
  - Raise ValueError.
- Set key from field.split(“ as ”, 1) at 0.
- If key.startswith(tuple(“count(”, “sum(”, “avg(”)).
  - Raise ValueError.
- If “.” belongs to key.
  - Set tuple(table, column) from key.split(“.”, 2) at slice no value to 2.
  - Return tuple(table at slice 4 to negative 1, column.strip(“′”)).
- Return tuple(no value, key.strip(“′”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0213.json#L7346) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L956) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1396)

<a id="op-b48c4c8426e2c3"></a>
### Delete items

`operation_foundation_desk_reportview_business_behavior_delete_items`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “DELETE”)).

**State and service calls** enqueue with “Platform.desk.reportview.delete\_bulk”.

**Explicit results** no value · delete\_bulk(doctype, items).

**Local steps**

- Bind dependencies json.
- Set items from sorted(json.loads(Platform.form\_dict.get(“items”)), reverse = true).
- Set doctype from Platform.form\_dict.get(“doctype”).
- If len(items) &gt; 10.
  - Evaluate Platform.enqueue(“Platform.desk.reportview.delete\_bulk”, doctype = doctype, items = items).
  - Return no value.
- Return delete\_bulk(doctype, items).

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.desk.reportview.delete\_bulk”, doctype = doctype, items = items).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L51) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L934) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1376)

<a id="op-69d001fbe0ed7b"></a>
### Delete bulk

`operation_foundation_desk_reportview_business_behavior_delete_bulk`

**Inputs** doctype, items.

**State and service calls** request delete\_doc for doctype · publish realtime with “progress” · commit · rollback · msgprint with translated “Failed to delete {0} documents: {1}”.format(len(undeleted\_items), “, ”.join(undeleted\_items)) · 1 additional forms in the steps below.

**Explicit results** delete\_bulk(doctype, undeleted\_items) · undeleted\_items · list().

**Local steps**

- Set undeleted\_items from list().
- For each tuple(i, d) in enumerate(items).
  - Attempt the following.
    - Set Platform.flags.in\_bulk\_delete from true.
    - Evaluate Platform.delete\_doc(doctype, d).
    - If len(items) ≥ 5.
      - Evaluate Platform.publish\_realtime(“progress”, dict(progress = list((i + 1), len(items)), title = translated “Deleting {0}”.format(translated doctype), description = d), user = Platform.session.user).
    - Evaluate Platform.db.commit().
  - On failure (Exception).
    - Evaluate undeleted\_items.append(d).
    - Evaluate Platform.db.rollback().
- If (undeleted\_items and len(items) differs from len(undeleted\_items)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in undeleted\_items → len(items) differs from len(undeleted\_items).
  - Evaluate Platform.clear\_messages().
  - Return delete\_bulk(doctype, undeleted\_items).
- Otherwise.
  - If undeleted\_items.
    - Evaluate Platform.msgprint(translated “Failed to delete {0} documents: {1}”.format(len(undeleted\_items), “, ”.join(undeleted\_items)), realtime = true, title = translated “Bulk Operation Failed”).
    - Return undeleted\_items.
- Evaluate Platform.msgprint(translated “Deleted {0} records from {1} doctype”.format(len(items), doctype), realtime = true, title = translated “Bulk Operation Successful”).
- Return list().

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“progress”, dict(progress = list((i + 1), len(items)), title = translated “Deleting {0}”.format(translated doctype), description = d), user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0214.json#L1654) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L933) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1375)

<a id="op-7856cac621e7eb"></a>
### Get sidebar stats

`operation_foundation_desk_reportview_business_behavior_get_sidebar_stats`

**Inputs** stats, doctype, filters = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Explicit results** mapping(“stats” → data).

**Local steps**

- If filters is identical to no value.
  - Set filters from list().
- If is\_virtual\_doctype(doctype).
  - Set controller from get\_controller(doctype).
  - Set args from mapping(“stats” → stats, “filters” → filters).
  - Set data from Platform.call(controller.get\_stats, args = args, expanded names args).
- Otherwise.
  - Set data from get\_stats(stats, doctype, filters).
- Return mapping(“stats” → data).

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0214.json#L2400) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L951) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1392)

<a id="op-e827bda5519cbd"></a>
### Get stats

`operation_foundation_desk_reportview_business_behavior_get_stats`

**Inputs** stats, doctype, filters = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Record and data access** read doctype via get\_list.

**Explicit results** results.

**Local steps**

- Bind dependencies json.
- If filters is identical to no value.
  - Set filters from list().
- Set columns from json.loads(stats).
- If filters.
  - Set filters from json.loads(filters).
- Set results from mapping().
- Attempt the following.
  - Set db\_columns from Platform.db.get\_table\_columns(doctype).
- On failure (tuple(Platform.db.InternalError, Platform.db.ProgrammingError)).
  - Set db\_columns from list().
- For each column in columns.
  - If column does not belong to db\_columns.
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set tag\_count from Platform.get\_list(doctype, fields = list(column, mapping(“COUNT” → “\*”)), filters = list(expanded filters, list(column, “!=”, empty text)), group\_by = column, as\_list = true, …).
    - If column equals “\_user\_tags”.
      - Set results at column from scrub\_user\_tags(tag\_count).
      - Set no\_tag\_count from Platform.get\_list(doctype, fields = list(column, mapping(“COUNT” → “1”, “as” → “count”)), filters = list(expanded filters, list(column, “in”, tuple(empty text, “,”))), group\_by = column, order\_by = column).
      - Set no\_tag\_count from no\_tag\_count at 0.get(“count”, 0) when no\_tag\_count, otherwise 0.
        - Value choice on no\_tag\_count — true gives no\_tag\_count at 0.get(“count”, 0), false gives 0.
      - Evaluate results at column.append(list(translated “No Tags”, no\_tag\_count)).
    - Otherwise.
      - Set results at column from tag\_count.
  - On failure (Platform.db.SQLError).
    - Take no action here.
  - On failure (Platform.db.InternalError).
    - Take no action here.
- Return results.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L60) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L952) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1393)

<a id="op-18c2e7c3104b8f"></a>
### Get filter dashboard data

`operation_foundation_desk_reportview_business_behavior_get_filter_dashboard_data`

**Inputs** stats, doctype, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_list.

**Explicit results** stats.

**Local steps**

- Bind dependencies json.
- Set tags from json.loads(stats).
- Set filters from json.loads((filters or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → list().
- Set stats from mapping().
- Set columns from Platform.db.get\_table\_columns(doctype).
- For each tag in tags.
  - If tag at “name” does not belong to columns.
    - Continue with the next iteration or loop test.
  - Set tagcount from list().
  - If tag at “type” does not belong to list(“Date”, “Datetime”).
    - Bind dependencies Field, functions.
    - Set tagcount from Platform.get\_list(doctype, fields = list(tag at “name”, mapping(“COUNT” → “\*”)), filters = list(expanded filters, functions.IfNull(Field(tag at “name”), empty text) differs from empty text), group\_by = tag ….
  - If (tag at “type” does not belong to list(“Check”, “Select”, “Date”, “Datetime”, …) and tag at “name” does not belong to list(“docstatus”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in tag at “type” does not belong to list(“Check”, “Select”, “Date”, “Datetime”, …) → tag at “name” does not belong to list(“docstatus”).
    - Set stats at tag at “name” from list(tagcount).
    - If stats at tag at “name”.
      - Set data from list(“No Data”, Platform.get\_list(doctype, fields = list(tag at “name”, mapping(“COUNT” → “\*”)), filters = list(expanded filters, nested operand in the contract.format(nested operand in the contract at nes ….
      - If (data and data at 1 differs from 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → data at 1 differs from 0.
        - Evaluate stats at tag at “name”.append(data).
  - Otherwise.
    - Set stats at tag at “name” from tagcount.
- Return stats.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L58) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L944) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1385)

<a id="op-e773bbc4eb90f5"></a>
### Scrub user tags

`operation_foundation_desk_reportview_business_behavior_scrub_user_tags`

**Inputs** tagcount.

**Explicit results** list of list(tag, rdict at tag) for tag drawn from rdict.

**Local steps**

- Set rdict from mapping().
- Set tagdict from dict(tagcount).
- For each t in tagdict.
  - If not t.
    - Continue with the next iteration or loop test.
  - Set alltags from t.split(“,”).
  - For each tag in alltags.
    - If tag.
      - If tag does not belong to rdict.
        - Set rdict at tag from 0.
      - Update rdict at tag using + tagdict at t.
- Return list of list(tag, rdict at tag) for tag drawn from rdict.
  - Draw tag from rdict.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0214.json#L4668) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L962) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1402)

<a id="op-246f79d2c233f1"></a>
### Get match cond

`operation_foundation_desk_reportview_business_behavior_get_match_cond`

**Inputs** doctype, as\_condition = true.

**Explicit results** cond · ((“ and (” + cond) + “)”) when cond, otherwise empty text.replace(“%”, “%%”).

**Local steps**

- Bind dependencies Engine.
- Set engine from Engine().
- Evaluate engine.get\_query(doctype, db\_query\_compat = true).
- Set cond from engine.build\_match\_conditions(as\_condition = as\_condition).
- If not as\_condition.
  - Return cond.
- Return ((“ and (” + cond) + “)”) when cond, otherwise empty text.replace(“%”, “%%”).
  - Value choice on cond — true gives ((“ and (” + cond) + “)”), false gives empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0214.json#L4932) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L948) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1389)

<a id="op-4cd921baac3998"></a>
### Build match conditions

`operation_foundation_desk_reportview_business_behavior_build_match_conditions`

**Inputs** doctype, user = no value, as\_condition = true.

**Explicit results** match\_conditions.replace(“%”, “%%”) · match\_conditions.

**Local steps**

- Bind dependencies Engine.
- Set engine from Engine().
- Evaluate engine.get\_query(doctype, user = user, db\_query\_compat = true).
- Set match\_conditions from engine.build\_match\_conditions(as\_condition = as\_condition).
- If as\_condition.
  - Return match\_conditions.replace(“%”, “%%”).
- Return match\_conditions.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0214.json#L5146) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L930) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1372)

<a id="op-65ea3e19f793ca"></a>
### Get filters cond

`operation_foundation_desk_reportview_business_behavior_get_filters_cond`

**Inputs** doctype, filters, conditions, ignore\_permissions = no value, with\_match\_conditions = false.

**Explicit results** cond.

**Local steps**

- If isinstance(filters, str).
  - Set filters from json.loads(filters).
- If filters.
  - Set flt from filters.
  - If isinstance(filters, dict).
    - Set filters from filters.items().
    - Set flt from list().
    - For each f in filters.
      - If (isinstance(f at 1, str) and f at 1 at 0 equals “!”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(f at 1, str) → f at 1 at 0 equals “!”.
        - Evaluate flt.append(list(doctype, f at 0, “!=”, f at 1 at slice 1 to no value)).
      - Otherwise.
        - If (isinstance(f at 1, (list bitwise or tuple)) and f at 1 at 0.lower() belongs to tuple(“=”, “&gt;”, “&lt;”, “&gt;=”, …)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(f at 1, (list bitwise or tuple)) → f at 1 at 0.lower() belongs to tuple(“=”, “&gt;”, “&lt;”, “&gt;=”, …).
          - Evaluate flt.append(list(doctype, f at 0, f at 1 at 0, f at 1 at 1)).
        - Otherwise.
          - Evaluate flt.append(list(doctype, f at 0, “=”, f at 1)).
  - Bind dependencies Engine.
  - Set engine from Engine().
  - Evaluate engine.get\_query(doctype, ignore\_permissions = ignore\_permissions, db\_query\_compat = true).
  - If with\_match\_conditions.
    - If match\_cond bound to engine.build\_match\_conditions().
      - Evaluate conditions.append(match\_cond).
  - Evaluate engine.build\_filter\_conditions(flt, conditions).
  - Set cond from (“ and ” + “ and ”.join(conditions)) when conditions, otherwise empty text.
    - Value choice on conditions — true gives (“ and ” + “ and ”.join(conditions)), false gives empty text.
- Otherwise.
  - Set cond from empty text.
- Return cond.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L59) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L945) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1386)

## Service · Robots

<a id="op-ccd00055a6432f"></a>
### Get context

`operation_foundation_public_pages_robots_business_behavior_get_context`

**Inputs** context.

**Record and data access** read “Website Settings” via get\_single\_value.

**Explicit results** mapping(“robots\_txt” → robots\_txt).

**Local steps**

- Set robots\_txt from (Platform.db.get\_single\_value(“Website Settings”, “robots\_txt”) or (Platform.local.conf.robots\_txt and Platform.read\_file(Platform.local.conf.robots\_txt)) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“Website Settings”, “robots\_txt”) → (Platform.local.conf.robots\_txt and Platform.read\_file(Platform.local.conf.robots\_txt)) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.local.conf.robots\_txt → Platform.read\_file(Platform.local.conf.robots\_txt).
- Return mapping(“robots\_txt” → robots\_txt).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Website Settings”, “robots\_txt”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L456) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1386) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L88)

## Record · Route history

[Record definition](../../../../data/record-types/route_history.json)

<a id="op-72341431ae94a9"></a>
### Route History.clear old logs

`operation_foundation_desk_record_definitions_route_history_business_behavior_route_history_clear_old_logs`

**Inputs** days = 30.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on table.

**Local steps**

- Bind dependencies Interval.
- Bind dependencies Now.
- Set table from Platform.qb.DocType(“Route History”).
- Evaluate Platform.db.delete(table, filters = table.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0180.json#L6494) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L528) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L984)

<a id="op-785630f522700b"></a>
### Deferred insert

`operation_foundation_desk_record_definitions_route_history_business_behavior_deferred_insert`

**Inputs** routes.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set routes from list of mapping(“user” → Platform.session.user, “route” → route.get(“route”), “creation” → route.get(“creation”)) for route drawn from Platform.parse\_json(routes).
  - Draw route from Platform.parse\_json(routes).
- Evaluate \_deferred\_insert(“Route History”, routes).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0180.json#L6679) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L525) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L982)

<a id="op-39e93c7b48f1e6"></a>
### Frequently visited links

`operation_foundation_desk_record_definitions_route_history_business_behavior_frequently_visited_links`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Route History” via get\_all.

**Explicit results** Platform.get\_all(“Route History”, fields = list(“route”, mapping(“COUNT” → “name”, “as” → “count”)), filters = mapping(“user” → Platform.session.user), group\_by = “route”, order\_by = “count desc”, …).

**Local steps**

- Return Platform.get\_all(“Route History”, fields = list(“route”, mapping(“COUNT” → “name”, “as” → “count”)), filters = mapping(“user” → Platform.session.user), group\_by = “route”, order\_by = “count desc”, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L25) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L526) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L983)
