# Projects and time · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Project

[Record definition](../../../../data/record-types/project.json)

<a id="op-d080db46222335"></a>
### Get projects for collect progress

`operation_enterprise_projects_record_definitions_project_business_behavior_get_projects_for_collect_progress`

**Inputs** frequency, fields.

**Record and data access** read “Project” via get\_all.

**Explicit results** Platform.get\_all(“Project”, fields = fields, filters = mapping(“collect\_progress” → 1, “frequency” → frequency, “status” → “Open”)).

**Local steps**

- Evaluate fields.extend(list(“name”)).
- Return Platform.get\_all(“Project”, fields = fields, filters = mapping(“collect\_progress” → 1, “frequency” → frequency, “status” → “Open”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0602.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1202) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L672)

<a id="op-d2980045e7add1"></a>
### Send project update email to users

`operation_enterprise_projects_record_definitions_project_business_behavior_send_project_update_email_to_users`

**Inputs** project.

**Record and data access** resolve a document from “Project” via get\_doc · resolve a document from mapping(“doctype” → “Project Update”, “project” → project, “sent” → 0, “date” → today(), …) via get\_doc · read “Email Account” via get\_value.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Project Update”, “project” → project, “sent” → 0, “date” → today(), …)) · sendmail.

**Explicit results** no value.

**Local steps**

- Set doc from Platform.get\_doc(“Project”, project).
- If (is\_holiday(doc.holiday\_list) or not doc.users).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_holiday(doc.holiday\_list) → not doc.users.
  - Return no value.
- Set project\_update from Platform.get\_doc(mapping(“doctype” → “Project Update”, “project” → project, “sent” → 0, “date” → today(), …)).insert().
- Set incoming\_email\_account from Platform.db.get\_value(“Email Account”, dict(enable\_incoming = 1, default\_incoming = 1), “email\_id”).
- Evaluate Platform.sendmail(recipients = get\_users\_email(doc), message = doc.message, subject = doc.subject, reference\_doctype = project\_update.doctype, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today() · service or queued work from Platform.sendmail(recipients = get\_users\_email(doc), message = doc.message, subject = doc.subject, reference\_doctype = project\_update.doctype, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0602.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L706)

<a id="op-b7d3b6c7f6d2ff"></a>
### Collect project status

`operation_enterprise_projects_record_definitions_project_business_behavior_collect_project_status`

**Inputs** no declared parameters.

**Record and data access** read “Project Update” via get\_all · resolve a document from “Project Update” via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- For each data in Platform.get\_all(“Project Update”, mapping(“date” → today(), “sent” → 0)).
  - Set doc from Platform.get\_doc(“Project Update”, data.name).
  - Set new\_replies from get\_uncollected\_replies(doc).
  - If new\_replies.
    - For each reply in new\_replies.
      - Evaluate doc.append(“users”, reply).
    - Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L664)

<a id="op-7a9f0f581725aa"></a>
### Get uncollected replies

`operation_enterprise_binding_enterprise_projects_doctype_project_project_get_uncollected_replies`

**Inputs** project\_update.

**Explicit results** new\_replies.

**Local steps**

- Set collected from Counter(generator of tuple(row.user, row.project\_status) for row drawn from project\_update.users).
  - Draw row from project\_update.users.
- Set new\_replies from list().
- For each reply in get\_project\_update\_replies(project\_update.name).
  - Set key from tuple(reply at “user”, reply at “project\_status”).
  - If collected at key.
    - Update collected at key using − 1.
  - Otherwise.
    - Evaluate new\_replies.append(reply).
- Return new\_replies.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L272) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1282)

<a id="op-b48bec8f6e5f22"></a>
### Get project update replies

`operation_enterprise_binding_enterprise_projects_doctype_project_project_get_project_update_replies`

**Inputs** project\_update.

**Record and data access** read “Communication” via get\_all · read “User” via get\_value.

**Explicit results** users.

**Local steps**

- Set replies from Platform.get\_all(“Communication”, fields = list(“content”, “text\_content”, “sender”), filters = dict(reference\_doctype = “Project Update”, reference\_name = project\_update, communication\_type = “Communicati ….
- Set users from list().
- For each d in replies.
  - Set user\_data from Platform.db.get\_value(“User”, mapping(“email” → d.sender), list(“full\_name”, “user\_image”, “name”), as\_dict = true).
  - If not user\_data.
    - Continue with the next iteration or loop test.
  - Evaluate users.append(mapping(“user” → user\_data.name, “full\_name” → user\_data.full\_name, “image” → user\_data.user\_image, “project\_status” → sanitize\_html(Platform.utils.md\_to\_html((nested operand in the contract.p ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in EmailReplyParser.parse\_reply(d.text\_content) → d.content.
- Return users.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L270) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1280)

<a id="op-999dac4bb2b959"></a>
### Send project status email to users

`operation_enterprise_projects_record_definitions_project_business_behavior_send_project_status_email_to_users`

**Inputs** no declared parameters.

**Record and data access** read “Project Update” via get\_all · resolve a document from “Project Update” via get\_doc · resolve a document from “Project” via get\_doc.

**State and service calls** sendmail · call db\_set on doc.

**Local steps**

- Set yesterday from add\_days(today(), negative 1).
- For each d in Platform.get\_all(“Project Update”, mapping(“date” → yesterday, “sent” → 0)).
  - Set doc from Platform.get\_doc(“Project Update”, d.name).
  - Set project\_doc from Platform.get\_doc(“Project”, doc.project).
  - Set args from mapping(“users” → doc.users, “title” → translated “Project Summary for {0}”.format(yesterday)).
  - Evaluate Platform.sendmail(recipients = get\_users\_email(project\_doc), template = “daily\_project\_summary”, args = args, subject = translated “Daily Project Summary for {0}”.format(d.name), …).
  - Evaluate doc.db\_set(“sent”, 1).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today() · service or queued work from Platform.sendmail(recipients = get\_users\_email(project\_doc), template = “daily\_project\_summary”, args = args, subject = translated “Daily Project Summary for {0}”.format(d.name), …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0602.json#L1264) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L705)

<a id="op-a00f5e05a95ccb"></a>
### Update project sales billing

`operation_enterprise_projects_record_definitions_project_business_behavior_update_project_sales_billing`

**Inputs** no declared parameters.

**Record and data access** read “Selling Settings” via get\_single\_value · read “Project” via get\_all · resolve a document from “Project” via get\_doc.

**State and service calls** call save on Platform.get\_doc(“Project”, project.name).

**Explicit results** no value.

**Local steps**

- Set sales\_update\_frequency from Platform.get\_single\_value(“Selling Settings”, “sales\_update\_frequency”).
- If sales\_update\_frequency equals “Each Transaction”.
  - Return no value.
- Otherwise.
  - If (sales\_update\_frequency equals “Monthly” and Platform.utils.now\_datetime().day differs from 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sales\_update\_frequency equals “Monthly” → Platform.utils.now\_datetime().day differs from 1.
    - Return no value.
- For each project in Platform.get\_all(“Project”, filters = mapping(“status” → list(“!=”, “Cancelled”))).
  - Evaluate Platform.get\_doc(“Project”, project.name).save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “sales\_update\_frequency”) · clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0602.json#L1736) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1243) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L710)

<a id="op-b3e5436f6f1754"></a>
### Create kanban board if not exists

`operation_enterprise_projects_record_definitions_project_business_behavior_create_kanban_board_if_not_exists`

**Inputs** project.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Record and data access** resolve a document from “Project” via get\_doc.

**Explicit results** board · quick\_kanban\_board(“Task”, board\_name, “status”, project.name).name.

**Local steps**

- Bind dependencies quick\_kanban\_board.
- Bind dependencies append\_number\_if\_name\_exists.
- Set project from Platform.get\_doc(“Project”, project).
- Evaluate project.check\_permission(“read”).
- If board bound to get\_project\_kanban\_board(project.name).
  - Return board.
- Set board\_name from append\_number\_if\_name\_exists(“Kanban Board”, project.project\_name).
- Return quick\_kanban\_board(“Task”, board\_name, “status”, project.name).name.

**Values supplied outside this operation** effective access from project.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L666)

<a id="op-2e8d0746c9dabc"></a>
### Get project kanban board

`operation_enterprise_binding_enterprise_projects_doctype_project_project_get_project_kanban_board`

**Inputs** project.

**Declared result** (str bitwise or no value).

**Record and data access** read “Kanban Board” via get\_list.

**Explicit results** board.name.

**Local steps**

- For each board in Platform.get\_list(“Kanban Board”, filters = mapping(“reference\_doctype” → “Task”), fields = list(“name”, “filters”)).
  - Set filters from Platform.parse\_json((board.filters or “&#91;&#93;”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in board.filters → “&#91;&#93;”.
  - If any(generator of (isinstance(f, list) and f at slice 1 to 4 equals list(“project”, “=”, project)) for f drawn from filters).
    - Draw f from filters.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(f, list) → f at slice 1 to 4 equals list(“project”, “=”, project).
    - Return board.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L268) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1278)

<a id="op-c8d6aa441ab942"></a>
### Get project tasks

`operation_enterprise_binding_enterprise_projects_doctype_project_project_get_project_tasks`

**Inputs** project, sort\_by = “creation”, sort\_order = “asc”, start = 0, page\_length = 50, txt = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** query.run(as\_dict = true).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted” · validation helper — translated “Tasks cannot be sorted by {0} {1}”.format(sort\_by, sort\_order).

**Local steps**

- If not Platform.has\_permission(“Project”, “read”, doc = project).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set sortable from (set(Platform.model.get\_permitted\_fields(“Task”)) − set(Platform.model.optional\_fields)).
- If (sort\_by does not belong to sortable or sort\_order does not belong to tuple(“asc”, “desc”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sort\_by does not belong to sortable → sort\_order does not belong to tuple(“asc”, “desc”).
  - Call the validation error handler Platform.throw(translated “Tasks cannot be sorted by {0} {1}”.format(sort\_by, sort\_order)).
- Set Task from Platform.qb.DocType(“Task”).
- Set df from Platform.get\_meta(“Task”).get\_field(sort\_by).
- Set sort\_field from Task at sort\_by.
- Set is\_empty from sort\_field.isnull().
- If (df and df.fieldtype does not belong to tuple(expanded Platform.model.numeric\_fieldtypes, expanded Platform.model.datetime\_fields)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype does not belong to tuple(expanded Platform.model.numeric\_fieldtypes, expanded Platform.model.datetime\_fields).
  - Set is\_empty from (is\_empty bitwise or sort\_field equals empty text).
- If (df and df.fieldtype equals “Select” and df.options).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype equals “Select” → df.options.
  - Set rank from Case().
  - For each tuple(position, option) in enumerate(df.options.split(whitespace '\\n')).
    - Set rank from rank.when(Task at sort\_by equals option, position).
  - Set sort\_field from rank.
- Set query from nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(Task.creation).limit(page\_length).offset(start).
  - Value choice on sort\_order equals “desc” — true gives Order.desc, false gives Order.asc.
- If txt.
  - Set query from query.where((Task.subject.like(formatted text %{txt}%) bitwise or Task.name.like(formatted text %{txt}%))).
- Return query.run(as\_dict = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Project”, “read”, doc = project).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L269) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1279)

<a id="op-7c0e6612992c70"></a>
### Set project status

`operation_enterprise_projects_record_definitions_project_business_behavior_set_project_status`

**Inputs** project, status.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Project” via get\_doc · resolve a document from “Task” via get\_doc.

**State and service calls** call save on task · call save on project.

**Explicit failure paths** validation helper — translated “Status must be Cancelled or Completed”.

**Local steps**

- If status does not belong to tuple(“Completed”, “Cancelled”).
  - Call the validation error handler Platform.throw(translated “Status must be Cancelled or Completed”).
- Set project from Platform.get\_doc(“Project”, project).
- Evaluate project.check\_permission(“write”).
- For each task\_name in get\_tasks\_in\_dependency\_order(project.name, status).
  - Set task from Platform.get\_doc(“Task”, task\_name).
  - Set task.status from status.
  - Set task.flags.ignore\_reschedule from true.
  - Evaluate task.save(ignore\_permissions = true).
- Set project.status from status.
- Evaluate project.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from project.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1240) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L707)

<a id="op-20932d0832e82c"></a>
### Get tasks in dependency order

`operation_enterprise_binding_enterprise_projects_doctype_project_project_get_tasks_in_dependency_order`

**Inputs** project, status.

**Declared result** list at str.

**Record and data access** read “Task” via get\_all · read “Task Depends On” via get\_all.

**Explicit results** list() · list of task for task drawn from TopologicalSorter(dependencies).static\_order() where task belongs to dependencies.

**Local steps**

- Set tasks from Platform.get\_all(“Task”, filters = mapping(“project” → project, “status” → list(“!=”, status)), pluck = “name”).
- If not tasks.
  - Return list().
- Set dependencies from mapping of task → set() for task drawn from tasks.
  - Draw task from tasks.
- For each row in Platform.get\_all(“Task Depends On”, filters = mapping(“parenttype” → “Task”, “parent” → list(“in”, tasks)), fields = list(“parent”, “task”)).
  - Evaluate dependencies at row.parent.add(row.task).
- Return list of task for task drawn from TopologicalSorter(dependencies).static\_order() where task belongs to dependencies.
  - Draw task from TopologicalSorter(dependencies).static\_order(), keep a combination only if (task belongs to dependencies).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L271) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1281)

<a id="op-b39942dc359fa2"></a>
### Get holiday list

`operation_enterprise_projects_record_definitions_project_business_behavior_get_holiday_list`

**Inputs** company = no value.

**Record and data access** read “Company” via get\_all · read “Company” via get\_cached\_value.

**Explicit results** holiday\_list.

**Explicit failure paths** validation helper — translated “Please set a default Holiday List for Company {0}”.format(Platform.bold(get\_default\_company())).

**Local steps**

- If not company.
  - Set company from (get\_default\_company() or Platform.get\_all(“Company”) at 0.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_default\_company() → Platform.get\_all(“Company”) at 0.name.
- Set holiday\_list from Platform.get\_cached\_value(“Company”, company, “default\_holiday\_list”).
- If not holiday\_list.
  - Call the validation error handler Platform.throw(translated “Please set a default Holiday List for Company {0}”.format(Platform.bold(get\_default\_company()))).
- Return holiday\_list.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_holiday\_list”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1199) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L669)

<a id="op-103c7b672b9782"></a>
### Get users email

`operation_enterprise_projects_record_definitions_project_business_behavior_get_users_email`

**Inputs** doc.

**Record and data access** read “User” via get\_value.

**Explicit results** list of d.email for d drawn from doc.users where Platform.db.get\_value(“User”, d.user, “enabled”).

**Local steps**

- Return list of d.email for d drawn from doc.users where Platform.db.get\_value(“User”, d.user, “enabled”).
  - Draw d from doc.users, keep a combination only if (Platform.db.get\_value(“User”, d.user, “enabled”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0602.json#L2889) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1204) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L674)

<a id="op-1b081bf1261beb"></a>
### Update purchase cost

`operation_enterprise_binding_enterprise_projects_doctype_project_project_update_purchase_cost`

**Inputs** projects.

**Record and data access** resolve a document from “Project” via get\_doc.

**Local steps**

- For each name in projects.
  - Set project from Platform.get\_doc(“Project”, name, for\_update = true).
  - Evaluate project.update\_purchase\_costing().
  - Evaluate project.db\_set\_cost(“total\_purchase\_cost”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L229) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1354)

<a id="op-3637ac1b4fbf02"></a>
### Update consumed material cost

`operation_enterprise_binding_enterprise_projects_doctype_project_project_update_consumed_material_cost`

**Inputs** projects.

**Record and data access** resolve a document from “Project” via get\_doc.

**Local steps**

- For each name in projects.
  - Set project from Platform.get\_doc(“Project”, name, for\_update = true).
  - Evaluate project.set\_consumed\_material\_cost().
  - Evaluate project.db\_set\_cost(“total\_consumed\_material\_cost”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L227) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1352)

<a id="op-43dddcc7dadc2d"></a>
### Update consumed material cost for vouchers

`operation_enterprise_binding_enterprise_projects_doctype_project_project_update_consumed_material_cost_for_vouchers`

**Inputs** vouchers.

**Local steps**

- Set sle from qb.DocType(“Stock Ledger Entry”).
- Set projects from set().
- For each voucher\_nos in create\_batch(list of voucher\_no for tuple(\_voucher\_type, voucher\_no) drawn from vouchers, 1000).
  - Draw tuple(\_voucher\_type, voucher\_no) from vouchers.
  - Evaluate projects.update(nested operand in the contract.distinct().where((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract()) bitwise and neste ….
- Evaluate update\_consumed\_material\_cost(projects).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L228) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1353)

<a id="op-3d297b41e45964"></a>
### Update costing and billing

`operation_enterprise_projects_record_definitions_project_business_behavior_update_costing_and_billing`

**Inputs** project = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Project” via get\_doc.

**State and service calls** call db\_update on project.

**Local steps**

- Set project from Platform.get\_doc(“Project”, project).
- Evaluate project.check\_permission(“write”).
- Evaluate project.set\_consumed\_material\_cost().
- Evaluate project.update\_costing().
- Evaluate project.db\_update().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from project.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L709)

<a id="op-27d834056222dd"></a>
### Get data

`operation_enterprise_projects_record_definitions_project_project_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“heatmap” → true, “heatmap\_message” → translated “This is based on the Time Sheets created against this project”, “fieldname” → “project”, “transactions” → list(mapping(“label” → translated “Projec ….

**Local steps**

- Return mapping(“heatmap” → true, “heatmap\_message” → translated “This is based on the Time Sheets created against this project”, “fieldname” → “project”, “transactions” → list(mapping(“label” → translated “Projec ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1245) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L712)

<a id="op-b32346012832a5"></a>
### Get project overview

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_get_project_overview`

**Inputs** project.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** ProjectOverview(project).build().

**Local steps**

- Evaluate check\_access(project).
- Return ProjectOverview(project).build().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L284) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1294)

<a id="op-84c3ec92f63322"></a>
### Check access

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_check_access`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** project.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L283) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1293)

<a id="op-b72c0668cd5611"></a>
### Project Overview.initialize

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_init`

**Inputs** self, project.

**Record and data access** read “Project” via get\_value.

**Local steps**

- Set self.project from Platform.db.get\_value(“Project”, project, PROJECT\_FIELDS, as\_dict = true).
- Set self.hidden\_fields from set().
- If Platform.session.user differs from “Administrator”.
  - Set permitted from set(get\_permitted\_fields(“Project”, permission\_type = “read”)).
  - Set self.hidden\_fields from set of field for field drawn from PROJECT\_FIELDS where field does not belong to permitted.
    - Draw field from PROJECT\_FIELDS, keep a combination only if (field does not belong to permitted).
- For each field in self.hidden\_fields.
  - Set self.project at field from no value.
- Set self.today from getdate().
- Set self.due\_soon\_until from add\_days(self.today, DUE\_SOON\_DAYS).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L198) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L313) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1323)

<a id="op-ed071e45cbe8f9"></a>
### Project Overview.build

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_build`

**Inputs** self.

**Declared result** dict.

**Explicit results** payload.

**Local steps**

- Set payload from mapping(“project” → self.project.name, “as\_of” → str(self.today), “errors” → mapping()).
- For each section in self.SECTIONS.
  - Attempt the following.
    - Set payload at section from getattr(self, section)().
  - On failure (Exception).
    - Set payload at section from no value.
    - Set payload at “errors” at section from 1.
    - Evaluate Platform.log\_error(title = (“Project Overview: ” + section)).
- Return payload.

**Values supplied outside this operation** selected callable from getattr(self, section).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1315)

<a id="op-28745ddcce1d74"></a>
### Project Overview.summary

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_summary`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“has\_tasks” → bool(self.tasks), “all\_cancelled” → (bool(self.tasks) and all(generator of task.status equals “Cancelled” for task drawn from self.tasks)), “task\_count” → len(self.tasks)).

**Local steps**

- Return mapping(“has\_tasks” → bool(self.tasks), “all\_cancelled” → (bool(self.tasks) and all(generator of task.status equals “Cancelled” for task drawn from self.tasks)), “task\_count” → len(self.tasks)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(self.tasks) → all(generator of task.status equals “Cancelled” for task drawn from self.tasks).
  - Draw task from self.tasks.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L214) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L329) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1339)
