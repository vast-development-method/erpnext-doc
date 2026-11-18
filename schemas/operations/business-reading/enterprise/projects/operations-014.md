# Projects and time · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Task

[Record definition](../../../../data/record-types/task.json)

<a id="op-694d37a86c93cd"></a>
### Set multiple status

`operation_enterprise_projects_record_definitions_task_business_behavior_set_multiple_status`

**Inputs** names, status.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Task” via get\_doc.

**State and service calls** call save on task.

**Local steps**

- Set names from json.loads(names).
- For each name in names.
  - Set task from Platform.get\_doc(“Task”, name).
  - Set task.status from status.
  - Evaluate task.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1292) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L747)

<a id="op-c62053c2bdc269"></a>
### Set tasks as overdue

`operation_enterprise_projects_record_definitions_task_business_behavior_set_tasks_as_overdue`

**Inputs** no declared parameters.

**Record and data access** read “Task” via get\_all · resolve a document from “Task” via get\_doc.

**Local steps**

- Set tasks from Platform.get\_all(“Task”, filters = mapping(“status” → list(“not in”, list(“Cancelled”, “Completed”, “Template”))), fields = list(“name”, “status”, “review\_date”)).
- For each task in tasks.
  - If task.status equals “Pending Review”.
    - If getdate(task.review\_date) &gt; getdate(today()).
      - Continue with the next iteration or loop test.
  - Evaluate Platform.get\_doc(“Task”, task.name).update\_status().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1293) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L748)

<a id="op-aba7f8c7428e5d"></a>
### Make timesheet

`operation_enterprise_projects_record_definitions_task_business_behavior_make_timesheet`

**Inputs** source\_name, target\_doc = no value, ignore\_permissions = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Set doclist from get\_mapped\_doc(“Task”, source\_name, mapping(“Task” → mapping(“doctype” → “Timesheet”)), target\_doc, postprocess = set\_missing\_values, ignore\_permissions = ignore\_permissions).
- Return doclist.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1289) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L744)

<a id="op-88d85c32aedd54"></a>
### Make timesheet.set missing values

`operation_enterprise_projects_record_definitions_task_business_behavior_make_timesheet_set_missing_values`

**Inputs** source, target.

**Local steps**

- Set target.parent\_project from source.project.
- Evaluate target.append(“time\_logs”, mapping(“hours” → source.actual\_time, “completed” → source.status equals “Completed”, “project” → source.project, “task” → source.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1290) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L745)

<a id="op-1e6b4fd6bfb3a8"></a>
### Get children

`operation_enterprise_projects_record_definitions_task_business_behavior_get_children`

**Inputs** doctype, parent, task = no value, project = no value, is\_root = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_list.

**Explicit results** tasks.

**Local steps**

- Set filters from list(list(“docstatus”, “&lt;”, “2”)).
- If task.
  - Evaluate filters.append(list(“parent\_task”, “=”, task)).
- Otherwise.
  - If (parent and not is\_root).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent → not is\_root.
    - Evaluate filters.append(list(“parent\_task”, “=”, parent)).
  - Otherwise.
    - Bind dependencies Field, functions.
    - Evaluate filters.append(functions.IfNull(Field(“parent\_task”), empty text) equals empty text).
- If project.
  - Evaluate filters.append(list(“project”, “=”, project)).
- Set tasks from Platform.get\_list(doctype, fields = list(“name as value”, “subject as title”, “is\_group as expandable”), filters = filters, order\_by = “name”).
- Return tasks.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1287) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L742)

<a id="op-7901a00562caeb"></a>
### Add node

`operation_enterprise_projects_record_definitions_task_business_behavior_add_runtime_process`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from args via get\_doc.

**State and service calls** call insert on Platform.get\_doc(args).

**Local steps**

- Bind dependencies make\_tree\_args.
- Set args from Platform.form\_dict.
- Evaluate args.update(mapping(“name\_field” → “subject”)).
- Set args from make\_tree\_args(expanded names args).
- If (args.parent\_task equals “All Tasks” or args.parent\_task equals args.project).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.parent\_task equals “All Tasks” → args.parent\_task equals args.project.
  - Set args.parent\_task from no value.
- Evaluate Platform.get\_doc(args).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0606.json#L1121) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1285) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L740)

<a id="op-a8a2ec4dd463ad"></a>
### Add multiple tasks

`operation_enterprise_projects_record_definitions_task_business_behavior_add_multiple_tasks`

**Inputs** data, parent, project = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Task” via get\_value · resolve a document from new\_doc via get\_doc.

**State and service calls** call insert on new\_task.

**Local steps**

- Set data from json.loads(data).
- Set is\_root from parent belongs to tuple(“All Tasks”, project).
- Set new\_doc from mapping(“doctype” → “Task”, “parent\_task” → no value when is\_root, otherwise parent, “project” → project when is\_root, otherwise Platform.db.get\_value(“Task”, parent, “project”)).
  - Value choice on is\_root — true gives no value, false gives parent.
  - Value choice on is\_root — true gives project, false gives Platform.db.get\_value(“Task”, parent, “project”).
- For each d in data.
  - If not d.get(“subject”).
    - Continue with the next iteration or loop test.
  - Set new\_doc at “subject” from d.get(“subject”).
  - Set new\_task from Platform.get\_doc(new\_doc).
  - Evaluate new\_task.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1284) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L739)

<a id="op-d8d139fd055c4c"></a>
### On doctype update

`operation_enterprise_projects_record_definitions_task_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Task”.

**Local steps**

- Evaluate Platform.db.add\_index(“Task”, list(“lft”, “rgt”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0606.json#L1812) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1291) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L746)

<a id="op-fcd6f2f3503f91"></a>
### Get data

`operation_enterprise_projects_record_definitions_task_task_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “task”, “transactions” → list(mapping(“label” → translated “Activity”, “items” → list(“Timesheet”)))).

**Local steps**

- Return mapping(“fieldname” → “task”, “transactions” → list(mapping(“label” → translated “Activity”, “items” → list(“Timesheet”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0606.json#L1890) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1322) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L776)

## Service · Tasks

<a id="op-aed06f9a82c199"></a>
### Get context

`operation_enterprise_projects_web_form_tasks_business_behavior_get_context`

**Inputs** context.

**Local steps**

- If project bound to Platform.form\_dict.project.
  - Set title from Platform.utils.data.escape\_html(project).
  - Set route from (“/projects?” + urllib.parse.urlencode(mapping(“project” → project))).
  - Set context.parents from list(mapping(“title” → title, “route” → route)).
  - Set context.success\_url from route.
- Otherwise.
  - If (context.doc and project bound to context.doc.get(“project”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in context.doc → project bound to context.doc.get(“project”).
    - Set title from Platform.utils.data.escape\_html(project).
    - Set route from (“/projects?” + urllib.parse.urlencode(mapping(“project” → project))).
    - Set context.parents from list(mapping(“title” → title, “route” → route)).
    - Set context.success\_url from route.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0613.json#L3817) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L881)

## Record · Timesheet

[Record definition](../../../../data/record-types/timesheet.json)

<a id="op-b420fb9fffbffa"></a>
### Timesheet.validate

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status().
- Evaluate self.set\_user().
- Evaluate self.validate\_dates().
- Evaluate self.calculate\_hours().
- Evaluate self.validate\_time\_logs().
- Evaluate self.check\_task\_and\_project\_access(self.time\_logs).
- Evaluate self.validate\_tasks\_not\_cancelled().
- Evaluate self.update\_cost().
- Evaluate self.calculate\_total\_amounts().
- Evaluate self.calculate\_percentage\_billed().
- Evaluate self.set\_dates().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-014.md#op-e552a91bab8e0b), [set user](operations-014.md#op-267bc1990cd759), [validate dates](operations-015.md#op-28ebcaeecd7541), [calculate hours](operations-014.md#op-22633b3693277b), [validate time logs](operations-015.md#op-d1f6367f06778d), [check task and project access](operations-015.md#op-e675c3610dd57a), [validate tasks not cancelled](operations-014.md#op-5c455a668fec95), [update cost](operations-015.md#op-4a015958314da8), [calculate total amounts](operations-014.md#op-7d1b2022cf1434), [calculate percentage billed](operations-014.md#op-d969c281b535f7), [set dates](operations-014.md#op-b88412eb8548af).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L814)

<a id="op-5c455a668fec95"></a>
### Timesheet.validate tasks not cancelled

`operation_enterprise_binding_enterprise_projects_doctype_timesheet_timesheet_timesheet_validate_tasks_not_cancelled`

**Inputs** self.

**Record and data access** read “Task” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot log time against cancelled Tasks: {0}”.format(“, ”.join(cancelled\_tasks)).

**Local steps**

- Set tasks from list of log.task for log drawn from self.time\_logs where log.task.
  - Draw log from self.time\_logs, keep a combination only if (log.task).
- If not tasks.
  - Return no value.
- Set cancelled\_tasks from Platform.get\_all(“Task”, filters = mapping(“name” → list(“in”, tasks), “status” → “Cancelled”), pluck = “name”).
- If cancelled\_tasks.
  - Call the validation error handler Platform.throw(translated “Cannot log time against cancelled Tasks: {0}”.format(“, ”.join(cancelled\_tasks))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L251) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1376)

<a id="op-b7e88e69fc7fd4"></a>
### Timesheet.on discard

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L3521) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L803)

<a id="op-8ff4ec19996357"></a>
### Timesheet.before update after submit

`operation_enterprise_binding_enterprise_projects_doctype_timesheet_timesheet_timesheet_before_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.check\_task\_and\_project\_access(self.get\_time\_logs\_that\_change\_totals()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check task and project access](operations-015.md#op-e675c3610dd57a), [get time logs that change totals](operations-015.md#op-90f743b2402c83).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L247) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1372)

<a id="op-18cd896d2a8cbf"></a>
### Timesheet.on update after submit

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_on_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_mandatory\_fields().
- Evaluate self.update\_task\_and\_project().
- Evaluate self.validate\_time\_logs().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate mandatory fields](operations-015.md#op-2b8050089f07de), [update task and project](operations-015.md#op-10ffe78ba34336), [validate time logs](operations-015.md#op-d1f6367f06778d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L3584) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L805)

<a id="op-22633b3693277b"></a>
### Timesheet.calculate hours

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_calculate_hours`

**Inputs** self.

**Local steps**

- For each row in self.time\_logs.
  - If (row.to\_time and row.from\_time).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.to\_time → row.from\_time.
    - Evaluate row.calculate\_hours().
    - Evaluate row.validate\_billing\_hours().
    - Evaluate row.update\_billing\_hours().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L3675) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L797)

<a id="op-7d1b2022cf1434"></a>
### Timesheet.calculate total amounts

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_calculate_total_amounts`

**Inputs** self.

**Local steps**

- Set self.total\_hours from 0.0.
- Set self.total\_billable\_hours from 0.0.
- Set self.total\_billed\_hours from 0.0.
- Set self.total\_billable\_amount, self.base\_total\_billable\_amount from 0.0.
- Set self.total\_costing\_amount, self.base\_total\_costing\_amount from 0.0.
- Set self.total\_billed\_amount, self.base\_total\_billed\_amount from 0.0.
- For each d in self.get(“time\_logs”).
  - Evaluate d.update\_billing\_hours().
  - Evaluate self.update\_time\_rates(d).
  - Update self.total\_hours using + flt(d.hours).
  - Update self.total\_costing\_amount using + flt(d.costing\_amount).
  - Update self.base\_total\_costing\_amount using + flt(d.base\_costing\_amount).
  - If d.is\_billable.
    - Update self.total\_billable\_hours using + flt(d.billing\_hours).
    - Update self.total\_billable\_amount using + flt(d.billing\_amount).
    - Update self.base\_total\_billable\_amount using + flt(d.base\_billing\_amount).
    - Update self.total\_billed\_amount using + flt(d.billing\_amount) when d.sales\_invoice, otherwise 0.0.
      - Value choice on d.sales\_invoice — true gives flt(d.billing\_amount), false gives 0.0.
    - Update self.base\_total\_billed\_amount using + flt(d.base\_billing\_amount) when d.sales\_invoice, otherwise 0.0.
      - Value choice on d.sales\_invoice — true gives flt(d.base\_billing\_amount), false gives 0.0.
    - Update self.total\_billed\_hours using + flt(d.billing\_hours) when d.sales\_invoice, otherwise 0.0.
      - Value choice on d.sales\_invoice — true gives flt(d.billing\_hours), false gives 0.0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [update time rates](operations-015.md#op-45b12a03842ca1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L3807) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L799)

<a id="op-d969c281b535f7"></a>
### Timesheet.calculate percentage billed

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_calculate_percentage_billed`

**Inputs** self.

**Local steps**

- Set self.per\_billed from 0.
- If (self.total\_billed\_amount &gt; 0 and self.total\_billable\_amount &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.total\_billed\_amount &gt; 0 → self.total\_billable\_amount &gt; 0.
  - Set self.per\_billed from ((self.total\_billed\_amount × 100) ÷ self.total\_billable\_amount).
- Otherwise.
  - If (self.total\_billed\_hours &gt; 0 and self.total\_billable\_hours &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.total\_billed\_hours &gt; 0 → self.total\_billable\_hours &gt; 0.
    - Set self.per\_billed from ((self.total\_billed\_hours × 100) ÷ self.total\_billable\_hours).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L4383) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L798)

<a id="op-c70ae3cf17a40f"></a>
### Timesheet.update billing hours

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_update_billing_hours`

**Inputs** self, args.

**Wrappers, in declaration order** deprecated.

**Local steps**

- Evaluate args.update\_billing\_hours().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L4623) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L810)

<a id="op-e552a91bab8e0b"></a>
### Timesheet.set status

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_set_status`

**Inputs** self.

**Local steps**

- Set self.status from mapping(“0” → “Draft”, “1” → “Submitted”, “2” → “Cancelled”) at str((self.docstatus or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus → 0.
- If flt(self.per\_billed, self.precision(“per\_billed”)) ≥ 100.0.
  - Set self.status from “Billed”.
- If 0.0 &lt; flt(self.per\_billed, self.precision(“per\_billed”)) &lt; 100.0.
  - Compare adjacent operands in order, stopping at the first false comparison in 0.0 &lt; flt(self.per\_billed, self.precision(“per\_billed”)) &lt; 100.0.
  - Set self.status from “Partially Billed”.
- If self.sales\_invoice.
  - Set self.status from “Completed”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L4692) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L808)

<a id="op-267bc1990cd759"></a>
### Timesheet.set user

`operation_enterprise_binding_enterprise_projects_doctype_timesheet_timesheet_timesheet_set_user`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Local steps**

- Set self.user from Platform.db.get\_value(“Employee”, self.employee, “user\_id”) when self.employee, otherwise self.owner.
  - Value choice on self.employee — true gives Platform.db.get\_value(“Employee”, self.employee, “user\_id”), false gives self.owner.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L250) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1375)

<a id="op-b88412eb8548af"></a>
### Timesheet.set dates

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_set_dates`

**Inputs** self.

**Local steps**

- If (self.docstatus &lt; 2 and self.time\_logs).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus &lt; 2 → self.time\_logs.
  - Set start\_date from min(generator of getdate(d.from\_time) for d drawn from self.time\_logs).
    - Draw d from self.time\_logs.
  - Set end\_date from max(generator of getdate(d.to\_time) for d drawn from self.time\_logs).
    - Draw d from self.time\_logs.
  - If (start\_date and end\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in start\_date → end\_date.
    - Set self.start\_date from getdate(start\_date).
    - Set self.end\_date from getdate(end\_date).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L5007) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L806)

<a id="op-22d636f7e0980a"></a>
### Timesheet.before cancel

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_before_cancel`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Time logs cannot be changed when a Timesheet is cancelled.”.

**Local steps**

- Evaluate self.set\_status().
- If self.get\_time\_logs\_that\_change\_totals().
  - Call the validation error handler Platform.throw(translated “Time logs cannot be changed when a Timesheet is cancelled.”, title = translated “Cannot Cancel Timesheet”).
- Evaluate self.check\_task\_and\_project\_access(self.time\_logs).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-014.md#op-e552a91bab8e0b), [get time logs that change totals](operations-015.md#op-90f743b2402c83), [check task and project access](operations-015.md#op-e675c3610dd57a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L796)

<a id="op-ce5a613c8afa31"></a>
### Timesheet.on cancel

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_task\_and\_project().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update task and project](operations-015.md#op-10ffe78ba34336).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L5339) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L802)
