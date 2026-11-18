# Supporting services · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Projects

<a id="op-7c27e07493a6ea"></a>
### Get timesheets

`operation_enterprise_templates_pages_projects_business_behavior_get_timesheets`

**Inputs** project, start = 0, search = no value.

**Record and data access** read “Timesheet Detail” via get\_all · read “Timesheet” via get\_all.

**Explicit results** timesheets.

**Local steps**

- Set filters from mapping(“project” → project).
- If search.
  - Set filters at “activity\_type” from tuple(“like”, formatted text %{search}%).
- Set timesheets from Platform.get\_all(“Timesheet Detail”, filters = filters, fields = list(“project”, “activity\_type”, “from\_time”, “to\_time”, …), limit\_start = start, limit\_page\_length = 10).
- For each timesheet in timesheets.
  - Set info from Platform.get\_all(“Timesheet”, filters = mapping(“name” → timesheet.parent), fields = list(“name”, “status”, “modified”, “modified\_by”), limit\_start = start, limit\_page\_length = 10).
  - If len(info).
    - Evaluate timesheet.update(info at 0).
- Return timesheets.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0977.json#L3305) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1352)

<a id="op-785fdfe8b0ff30"></a>
### Get timesheet html

`operation_enterprise_templates_pages_projects_business_behavior_get_timesheet_document_markup`

**Inputs** project, start = 0.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** Platform.render\_template(“Enterprise/templates/includes/projects/project\_timesheets.html”, mapping(“doc” → mapping(“timesheets” → get\_timesheets(project, start))), is\_path = true).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not permitted to view the timesheets of this project.”.

**Local steps**

- Set project\_user from validate\_and\_get\_project\_user(project = project).
- If (not project\_user or project\_user.hide\_timesheets).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not project\_user → project\_user.hide\_timesheets.
  - Call the validation error handler Platform.throw(translated “You are not permitted to view the timesheets of this project.”, Platform.PermissionError).
- Return Platform.render\_template(“Enterprise/templates/includes/projects/project\_timesheets.html”, mapping(“doc” → mapping(“timesheets” → get\_timesheets(project, start))), is\_path = true).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1351)

<a id="op-2d59117c1f85cc"></a>
### Get attachments

`operation_enterprise_templates_pages_projects_business_behavior_get_attachments`

**Inputs** project.

**Record and data access** read “File” via get\_all.

**Explicit results** Platform.get\_all(“File”, filters = mapping(“attached\_to\_name” → project, “attached\_to\_doctype” → “Project”, “is\_private” → 0), fields = list(“file\_name”, “file\_url”, “file\_size”)).

**Local steps**

- Return Platform.get\_all(“File”, filters = mapping(“attached\_to\_name” → project, “attached\_to\_doctype” → “Project”, “is\_private” → 0), fields = list(“file\_name”, “file\_url”, “file\_size”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0977.json#L3961) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1347)

<a id="op-db2d04828b366d"></a>
### Validate and get project user

`operation_enterprise_templates_pages_projects_business_behavior_validate_and_get_project_user`

**Inputs** project.

**Record and data access** resolve a document from “Project” via get\_doc.

**Explicit results** project\_user.

**Local steps**

- Set project\_doc from Platform.get\_doc(“Project”, project).
- If not (is\_website\_user() and has\_website\_permission(project\_doc, “read”, Platform.session.user)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_website\_user() → has\_website\_permission(project\_doc, “read”, Platform.session.user).
  - Evaluate project\_doc.check\_permission().
- Set project\_user from next(generator of d for d drawn from project\_doc.users where d.user equals Platform.session.user, no value).
  - Draw d from project\_doc.users, keep a combination only if (d.user equals Platform.session.user).
- Return project\_user.

**Values supplied outside this operation** effective access from project\_doc.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1353)

## Service · Query

<a id="op-d732e5ae5e2f66"></a>
### Get user permission conditions qb

`operation_enterprise_binding_enterprise_utilities_query_get_user_permission_conditions_qb`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, table.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L58) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1339)

<a id="op-b0fd037a176a46"></a>
### Get child user permission conditions qb

`operation_enterprise_binding_enterprise_utilities_query_get_child_user_permission_conditions_qb`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, table.

**Explicit result forms** a structured result, a value selected from the current context.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L56) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1337)

<a id="op-572b06f00db6c3"></a>
### Get refused link conditions

`operation_enterprise_binding_enterprise_utilities_query_get_refused_link_conditions`

**Inputs** child, child\_doctype, doctype, user\_permissions.

**Explicit results** conditions.

**Local steps**

- Bind dependencies get\_allowed\_docs\_for\_doctype.
- Bind dependencies IfNull.
- Set strict from Platform.get\_system\_settings(“apply\_strict\_user\_permissions”).
- Set conditions from list().
- For each field in Platform.get\_meta(child\_doctype).get\_link\_fields().
  - If field.ignore\_user\_permissions.
    - Continue with the next iteration or loop test.
  - Set allowed from get\_allowed\_docs\_for\_doctype(user\_permissions.get(field.options, list()), doctype).
  - If allowed.
    - Set value from IfNull(child at field.fieldname, empty text).
    - Evaluate conditions.append(value.notin(allowed) when strict, otherwise (value differs from empty text bitwise and value.notin(allowed))).
      - Value choice on strict — true gives value.notin(allowed), false gives (value differs from empty text bitwise and value.notin(allowed)).
- Return conditions.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“apply\_strict\_user\_permissions”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L57) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1338)

## Service · Regional

<a id="op-9392e49e66b9f5"></a>
### Temporary flag

`operation_enterprise_utilities_regional_business_behavior_temporary_flag`

**Inputs** flag\_name, value.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Set flags from Platform.local.flags.
- Set flags at flag\_name from value.
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Evaluate flags.pop(flag\_name, no value).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0990.json#L3496) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L301) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L91)

## Record · Rename tool

[Record definition](../../../../data/record-types/rename_tool.json)

<a id="op-1a227c5b1c6f4c"></a>
### Get doctypes

`operation_enterprise_utilities_record_definitions_rename_tool_business_behavior_get_record_types`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), deprecated.

**Record and data access** read “DocType” via get\_all.

**Explicit results** Platform.get\_all(“DocType”, filters = mapping(“allow\_rename” → 1, “module” → list(“!=”, “Core”)), order\_by = “name”, pluck = “name”).

**Local steps**

- Evaluate Platform.has\_permission(“Rename Tool”, throw = true).
- Return Platform.get\_all(“DocType”, filters = mapping(“allow\_rename” → 1, “module” → list(“!=”, “Core”)), order\_by = “name”, pluck = “name”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Rename Tool”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L285) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L76)

<a id="op-0e294a5b39e93b"></a>
### Upload

`operation_enterprise_utilities_record_definitions_rename_tool_business_behavior_upload`

**Inputs** select\_doctype = no value, file\_to\_rename = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** enqueue with select\_doctype.

**Local steps**

- If not select\_doctype.
  - Set select\_doctype from Platform.form\_dict.select\_doctype.
- Evaluate validate\_access(select\_doctype).
- Set file from get\_file\_to\_rename(file\_to\_rename).
- Set rows from read\_csv\_content(file.get\_content()).
- For each i in range(0, len(rows), 500).
  - Evaluate Platform.enqueue(method = rename\_rows, queue = “long”, doctype = select\_doctype, rows = rows at slice i to (i + 500), …).
- Evaluate delete\_file\_to\_rename(file).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(method = rename\_rows, queue = “long”, doctype = select\_doctype, rows = rows at slice i to (i + 500), …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L286) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L77)

<a id="op-dd0835bd53d518"></a>
### Validate access

`operation_enterprise_binding_enterprise_utilities_doctype_rename_tool_rename_tool_validate_access`

**Inputs** doctype.

**Declared result** no value.

**Record and data access** read “DocType” via exists.

**Explicit failure paths** validation helper — translated “{0} cannot be renamed with the Rename Tool”.format(doctype) · Platform.PermissionError.

**Local steps**

- Evaluate Platform.has\_permission(“Rename Tool”, “write”, throw = true).
- Set filters from mapping(“name” → doctype, “allow\_rename” → 1, “module” → list(“!=”, “Core”)).
- If (not doctype or not Platform.db.exists(“DocType”, filters)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype → not Platform.db.exists(“DocType”, filters).
  - Call the validation error handler Platform.throw(translated “{0} cannot be renamed with the Rename Tool”.format(doctype)).
- If not Platform.has\_permission(doctype, “write”).
  - Raise Platform.PermissionError.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Rename Tool”, “write”, throw = true), Platform.has\_permission(doctype, “write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L32) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1313)

<a id="op-95865b234e3909"></a>
### Rename rows

`operation_enterprise_binding_enterprise_utilities_doctype_rename_tool_rename_tool_rename_rows`

**Inputs** doctype, rows.

**Declared result** no value.

**Local steps**

- Set failed\_prefix from translated “\*\* Failed: {0} to {1}: {2}”.split(“{0}”) at 0.
- Set failed from list of line for line drawn from bulk\_rename(doctype, rows = rows) where line.startswith(failed\_prefix).
  - Draw line from bulk\_rename(doctype, rows = rows), keep a combination only if (line.startswith(failed\_prefix)).
- If failed.
  - Evaluate notify\_failed\_rows(doctype, failed, len(rows)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L31) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1312)

<a id="op-45a18465c40449"></a>
### Notify failed rows

`operation_enterprise_binding_enterprise_utilities_doctype_rename_tool_rename_tool_notify_failed_rows`

**Inputs** doctype, failed, total.

**Declared result** no value.

**Record and data access** resolve a document from mapping(“doctype” → “Notification Log”, “for\_user” → Platform.session.user, “type” → “Alert”, “subject” → subject, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Notification Log”, “for\_user” → Platform.session.user, “type” → “Alert”, “subject” → subject, …)).

**Local steps**

- Set subject from translated “Rename Tool: {0} of {1} {2} rows could not be renamed”.format(len(failed), total, translated doctype).
- Evaluate Platform.get\_doc(mapping(“doctype” → “Notification Log”, “for\_user” → Platform.session.user, “type” → “Alert”, “subject” → subject, …)).insert(ignore\_permissions = true).
  - Draw line from failed.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L30) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1311)

<a id="op-77d15c8700d2ad"></a>
### Delete file to rename

`operation_enterprise_binding_enterprise_utilities_doctype_rename_tool_rename_tool_delete_file_to_rename`

**Inputs** file.

**Declared result** no value.

**Record and data access** read “Rename Tool” via get\_single\_value.

**State and service calls** request set\_single\_value on “Rename Tool”.

**Local steps**

- If Platform.db.get\_single\_value(“Rename Tool”, “file\_to\_rename”) equals file.file\_url.
  - Evaluate Platform.db.set\_single\_value(“Rename Tool”, “file\_to\_rename”, no value).
- Evaluate file.delete().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Rename Tool”, “file\_to\_rename”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L28) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1309)

<a id="op-4067e38e45c9fd"></a>
### Get file to rename

`operation_enterprise_binding_enterprise_utilities_doctype_rename_tool_rename_tool_get_file_to_rename`

**Inputs** file\_url.

**Declared result** Document.

**Record and data access** read “File” via get\_value · resolve a document from “File” via get\_doc.

**Explicit results** Platform.get\_doc(“File”, file\_name).

**Explicit failure paths** validation helper — translated “Please attach a CSV file to rename”.

**Local steps**

- Set filters from mapping(“attached\_to\_doctype” → “Rename Tool”, “attached\_to\_name” → “Rename Tool”).
- If file\_url.
  - Set filters at “file\_url” from file\_url.
- Set file\_name from Platform.db.get\_value(“File”, filters, “name”, order\_by = “creation desc”).
- If not file\_name.
  - Call the validation error handler Platform.throw(translated “Please attach a CSV file to rename”).
- Return Platform.get\_doc(“File”, file\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L29) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1310)

## Service · Rfq

<a id="op-787e1dd25e66fc"></a>
### Get context

`operation_enterprise_templates_pages_rfq_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from Platform.form\_dict.doctype via get\_doc.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Permitted”.

**Local steps**

- Set context.no\_cache from 1.
- Set context.show\_sidebar from true.
- Set context.doc from Platform.get\_doc(Platform.form\_dict.doctype, Platform.form\_dict.name).
- If context.doc.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).
- Set context.parents from Platform.form\_dict.parents.
- Set context.doc.supplier from get\_supplier().
- Set context.doc.rfq\_links from get\_link\_quotation(context.doc.supplier, context.doc.name).
- Evaluate unauthorized\_user(context.doc.supplier).
- Evaluate update\_supplier\_details(context).
- Set context.portal\_doc from get\_portal\_doc(context.doc).
- Set context at “title” from Platform.form\_dict.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1355)

<a id="op-dc40fa44494a63"></a>
### Get portal doc

`operation_enterprise_binding_enterprise_templates_pages_rfq_get_portal_doc`

**Inputs** rfq.

**Declared result** dict.

**Explicit results** mapping(“name” → rfq.name, “items” → items).

**Local steps**

- Set items from list of mapping(“name” → item.name, “idx” → item.idx, “qty” → item.qty, “rate” → 0) for item drawn from rfq.items.
  - Draw item from rfq.items.
- Return mapping(“name” → rfq.name, “items” → items).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L24) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1305)

<a id="op-d2d9112e8ee9c5"></a>
### Get supplier

`operation_enterprise_templates_pages_rfq_business_behavior_get_supplier`

**Inputs** no declared parameters.

**Explicit results** empty text · next(generator of supplier for supplier drawn from suppliers where check\_supplier\_has\_docname\_access(supplier), suppliers at 0).

**Local steps**

- Set doctype from Platform.form\_dict.doctype.
- Set parties\_doctype from “Request for Quotation Supplier” when doctype equals “Request for Quotation”, otherwise doctype.
  - Value choice on doctype equals “Request for Quotation” — true gives “Request for Quotation Supplier”, false gives doctype.
- Set tuple(customers, suppliers) from get\_customers\_suppliers(parties\_doctype, Platform.session.user).
- If not suppliers.
  - Return empty text.
- Return next(generator of supplier for supplier drawn from suppliers where check\_supplier\_has\_docname\_access(supplier), suppliers at 0).
  - Draw supplier from suppliers, keep a combination only if (check\_supplier\_has\_docname\_access(supplier)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1357)

<a id="op-24abc2649e99a9"></a>
### Check supplier has docname access

`operation_enterprise_templates_pages_rfq_business_behavior_check_supplier_has_record_name_access`

**Inputs** supplier.

**Explicit results** status.

**Local steps**

- Set status from true.
- If Platform.form\_dict.name does not belong to Platform.db.sql\_list(query text (SELECT, Request for Quotation Supplier), tuple(supplier)).
  - Set status from false.
- Return status.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1354)

<a id="op-b0234751adb1e8"></a>
### Unauthorized user

`operation_enterprise_templates_pages_rfq_business_behavior_unauthorized_user`

**Inputs** supplier.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Permitted”.

**Local steps**

- Set status from (check\_supplier\_has\_docname\_access(supplier) or false).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in check\_supplier\_has\_docname\_access(supplier) → false.
- If status is identical to false.
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0977.json#L4942) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1358)

<a id="op-4fd7e33b7f8f98"></a>
### Update supplier details

`operation_enterprise_templates_pages_rfq_business_behavior_update_supplier_details`

**Inputs** context.

**Record and data access** resolve a document from “Supplier” via get\_doc · read “Company” via get\_cached\_value · read “Currency” via get\_value.

**Local steps**

- Set supplier\_doc from Platform.get\_doc(“Supplier”, context.doc.supplier).
- Set context.doc.currency from (supplier\_doc.default\_currency or Platform.get\_cached\_value(“Company”, context.doc.company, “default\_currency”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in supplier\_doc.default\_currency → Platform.get\_cached\_value(“Company”, context.doc.company, “default\_currency”).
- Set context.doc.currency\_symbol from Platform.db.get\_value(“Currency”, context.doc.currency, “symbol”, cache = true).
- Set context.doc.number\_format from Platform.db.get\_value(“Currency”, context.doc.currency, “number\_format”, cache = true).
- Set context.doc.buying\_price\_list from (supplier\_doc.default\_price\_list or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in supplier\_doc.default\_price\_list → empty text.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, context.doc.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0977.json#L5079) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1359)

<a id="op-1001c443e2afd2"></a>
### Get link quotation

`operation_enterprise_templates_pages_rfq_business_behavior_get_link_quotation`

**Inputs** supplier, rfq.

**Record and data access** execute query text (SELECT, Supplier Quotation Item).

**Explicit results** (quotation or no value).

**Local steps**

- Set quotation from Platform.db.sql(query text (SELECT, Supplier Quotation Item), mapping(“name” → rfq, “supplier” → supplier), as\_dict = 1).
- For each data in quotation.
  - Set data.transaction\_date from formatdate(data.transaction\_date).
- Return (quotation or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in quotation → no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1356)

## Service · Search help

<a id="op-892f9139069819"></a>
### Get context

`operation_enterprise_templates_pages_search_help_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Set context.no\_cache from 1.
- If Platform.form\_dict.q.
  - Set query from str(utils.escape(sanitize\_html(Platform.form\_dict.q))).
  - Set context.title from translated “Help Results for”.
  - Set context.query from query.
  - Set context.route from “/search\_help”.
  - Set d from Platform.\_dict().
  - Set d.results\_sections from get\_help\_results\_sections(query).
  - Evaluate context.update(d).
- Otherwise.
  - Set context.title from translated “Docs Search”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0977.json#L5908) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1360)

<a id="op-4d7f83e8cb0e25"></a>
### Get help results sections

`operation_enterprise_templates_pages_search_help_business_behavior_get_help_results_sections`

**Inputs** text.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Record and data access** resolve a document from “Support Settings” via get\_doc.

**Explicit results** out.

**Local steps**

- Set out from list().
- Set settings from Platform.get\_doc(“Support Settings”, “Support Settings”).
- For each api in settings.search\_apis.
  - Set results from list().
  - If api.source\_type equals “API”.
    - Set response\_json from get\_response(api, text).
    - Set topics\_data from get\_topics\_data(api, response\_json).
    - Set results from prepare\_api\_results(api, topics\_data).
  - Otherwise.
    - Set doctype from api.source\_doctype.
    - Set raw from search(text, 0, 20, doctype).
    - Set results from prepare\_doctype\_results(api, raw).
  - If results.
    - Evaluate out.append(mapping(“title” → api.source\_name, “results” → results)).
- Return out.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1361)
