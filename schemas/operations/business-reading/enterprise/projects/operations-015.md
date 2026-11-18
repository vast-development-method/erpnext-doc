# Projects and time · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Timesheet

[Record definition](../../../../data/record-types/timesheet.json)

<a id="op-95c187dc5fb019"></a>
### Timesheet.on submit

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_mandatory\_fields().
- Evaluate self.update\_task\_and\_project().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate mandatory fields](operations-015.md#op-2b8050089f07de), [update task and project](operations-015.md#op-10ffe78ba34336).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L5390) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L804)

<a id="op-2b8050089f07de"></a>
### Timesheet.validate mandatory fields

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_validate_mandatory_fields`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: From Time and To Time is mandatory.”.format(data.idx) · validation helper — translated “Row {0}: Activity Type is mandatory.”.format(data.idx) · validation helper — translated “Row {0}: Hours value must be greater than zero.”.format(data.idx).

**Local steps**

- For each data in self.time\_logs.
  - If (not data.from\_time and not data.to\_time).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not data.from\_time → not data.to\_time.
    - Call the validation error handler Platform.throw(translated “Row {0}: From Time and To Time is mandatory.”.format(data.idx)).
  - If (not data.activity\_type and self.employee).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not data.activity\_type → self.employee.
    - Call the validation error handler Platform.throw(translated “Row {0}: Activity Type is mandatory.”.format(data.idx)).
  - If flt(data.hours) equals 0.0.
    - Call the validation error handler Platform.throw(translated “Row {0}: Hours value must be greater than zero.”.format(data.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L5461) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L816)

<a id="op-10ffe78ba34336"></a>
### Timesheet.update task and project

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_update_task_and_project`

**Inputs** self.

**Record and data access** resolve a document from “Task” via get\_doc · resolve a document from “Project” via get\_doc.

**State and service calls** call save on task · call save on project\_doc.

**Local steps**

- Set tuple(tasks, projects) from tuple(list(), list()).
- For each data in self.time\_logs.
  - If (data.task and data.task does not belong to tasks).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.task → data.task does not belong to tasks.
    - Set task from Platform.get\_doc(“Task”, data.task).
    - Evaluate task.update\_time\_and\_costing().
    - Set task.status from get\_task\_status(task).
    - Evaluate task.save(ignore\_permissions = true).
    - Evaluate tasks.append(data.task).
  - If (data.project and data.project does not belong to projects).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.project → data.project does not belong to projects.
    - Evaluate projects.append(data.project).
- For each project in projects.
  - Set project\_doc from Platform.get\_doc(“Project”, project).
  - Evaluate project\_doc.update\_project().
  - Evaluate project\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1363) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L812)

<a id="op-28ebcaeecd7541"></a>
### Timesheet.validate dates

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_validate_dates`

**Inputs** self.

**Local steps**

- For each time\_log in self.time\_logs.
  - Evaluate time\_log.validate\_dates().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L6319) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L815)

<a id="op-d1f6367f06778d"></a>
### Timesheet.validate time logs

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_validate_time_logs`

**Inputs** self.

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- Set saved\_activity\_types from mapping of row.name → row.activity\_type for row drawn from previous.time\_logs when (previous and previous.docstatus equals 1), otherwise mapping().
  - Value choice on (previous and previous.docstatus equals 1) — true gives mapping of row.name → row.activity\_type for row drawn from previous.time\_logs, false gives mapping().
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous → previous.docstatus equals 1.
  - Draw row from previous.time\_logs.
- For each time\_log in self.time\_logs.
  - Evaluate time\_log.set\_to\_time().
  - Evaluate self.validate\_overlap(time\_log).
  - Evaluate time\_log.set\_project().
  - Evaluate time\_log.validate\_parent\_project(self.parent\_project).
  - Evaluate time\_log.validate\_task\_project().
  - If time\_log.activity\_type differs from saved\_activity\_types.get(time\_log.name).
    - Evaluate time\_log.validate\_activity\_type().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overlap](operations-015.md#op-e53eac016a440a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L820)

<a id="op-90f743b2402c83"></a>
### Timesheet.get time logs that change totals

`operation_enterprise_binding_enterprise_projects_doctype_timesheet_timesheet_timesheet_get_time_logs_that_change_totals`

**Inputs** self.

**Explicit results** (changed + list(saved\_rows.values())).

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- Set saved\_rows from mapping of row.name → row for row drawn from previous.time\_logs when previous, otherwise mapping().
  - Value choice on previous — true gives mapping of row.name → row for row drawn from previous.time\_logs, false gives mapping().
  - Draw row from previous.time\_logs.
- Set changed from list().
- For each row in self.time\_logs.
  - Set saved\_row from saved\_rows.pop(row.name, no value).
  - If get\_values\_used\_in\_totals(row) differs from get\_values\_used\_in\_totals(saved\_row).
    - Evaluate changed.extend(generator of log for log drawn from tuple(row, saved\_row) where log).
      - Draw log from tuple(row, saved\_row), keep a combination only if (log).
- Return (changed + list(saved\_rows.values())).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L249) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L364) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1374)

<a id="op-e675c3610dd57a"></a>
### Timesheet.check task and project access

`operation_enterprise_binding_enterprise_projects_doctype_timesheet_timesheet_timesheet_check_task_and_project_access`

**Inputs** self, time\_logs.

**Record and data access** read “Task” via get\_all.

**Explicit results** no value.

**Local steps**

- If self.flags.ignore\_permissions.
  - Return no value.
- Set tasks from set of log.task for log drawn from time\_logs where log.task.
  - Draw log from time\_logs, keep a combination only if (log.task).
- Set projects from set of log.project for log drawn from time\_logs where log.project.
  - Draw log from time\_logs, keep a combination only if (log.project).
- If tasks.
  - Evaluate projects.update(generator of project for project drawn from Platform.get\_all(“Task”, filters = mapping(“name” → list(“in”, list(tasks))), pluck = “project”) where project).
    - Draw project from Platform.get\_all(“Task”, filters = mapping(“name” → list(“in”, list(tasks))), pluck = “project”), keep a combination only if (project).
- For each task in tasks.
  - Evaluate require\_permission(“Task”, task, “select”).
- For each project in projects.
  - Evaluate require\_permission(“Project”, project, “select”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L248) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L363) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1373)

<a id="op-e53eac016a440a"></a>
### Timesheet.validate overlap

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_validate_overlap`

**Inputs** self, data.

**Record and data access** read “Projects Settings” via get\_single.

**Local steps**

- Set settings from Platform.get\_single(“Projects Settings”).
- Evaluate self.validate\_overlap\_for(“user”, data, self.user, settings.ignore\_user\_time\_overlap).
- Evaluate self.validate\_overlap\_for(“employee”, data, self.employee, settings.ignore\_employee\_time\_overlap).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overlap for](operations-015.md#op-68031d5477afa2).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L6544) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L817)

<a id="op-c25ded57bd7876"></a>
### Timesheet.set project

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_set_project`

**Inputs** self, data.

**Wrappers, in declaration order** deprecated.

**Local steps**

- Evaluate data.set\_project().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L6716) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L807)

<a id="op-6c623c4258248d"></a>
### Timesheet.validate project

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_validate_project`

**Inputs** self, data.

**Wrappers, in declaration order** deprecated.

**Local steps**

- Evaluate data.validate\_parent\_project(self.parent\_project).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L6785) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L819)

<a id="op-68031d5477afa2"></a>
### Timesheet.validate overlap for

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_validate_overlap_for`

**Inputs** self, fieldname, args, value, ignore\_validation = false.

**Explicit results** no value.

**Explicit failure paths** validation helper with OverlapError — translated “Row {0}: From Time and To Time of {1} is overlapping with {2}”.format(args.idx, self.name, existing.name).

**Local steps**

- If (not value or ignore\_validation).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not value → ignore\_validation.
  - Return no value.
- Set existing from self.get\_overlap\_for(fieldname, args, value).
- If existing.
  - Call the validation error handler Platform.throw(translated “Row {0}: From Time and To Time of {1} is overlapping with {2}”.format(args.idx, self.name, existing.name), OverlapError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get overlap for](operations-015.md#op-98f16323358b41).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0608.json#L6863) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L818)

<a id="op-98f16323358b41"></a>
### Timesheet.get overlap for

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_get_overlap_for`

**Inputs** self, fieldname, args, value.

**Explicit results** self · existing at 0 when existing, otherwise no value.

**Local steps**

- Set timesheet from Platform.qb.DocType(“Timesheet”).
- Set timelog from Platform.qb.DocType(“Timesheet Detail”).
- Set from\_time from get\_datetime(args.from\_time).
- Set to\_time from get\_datetime(args.to\_time).
- Set existing from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“name”), nested operand in the contract.as\_(“from\_time”), nested operand in the contract.as\_(“to\_tim ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.name → “No Name”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.parent → “No Name”.
- If self.check\_internal\_overlap(fieldname, args).
  - Return self.
- Return existing at 0 when existing, otherwise no value.
  - Value choice on existing — true gives existing at 0, false gives no value.

**Methods declared on this owner** [check internal overlap](operations-015.md#op-3486178b968935).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0609.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L801)

<a id="op-3486178b968935"></a>
### Timesheet.check internal overlap

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_check_internal_overlap`

**Inputs** self, fieldname, args.

**Explicit results** true · false.

**Local steps**

- For each time\_log in self.time\_logs.
  - If not (time\_log.from\_time and time\_log.to\_time and args.from\_time and args.to\_time).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in time\_log.from\_time → time\_log.to\_time → args.from\_time → args.to\_time.
    - Continue with the next iteration or loop test.
  - Set from\_time from get\_datetime(time\_log.from\_time).
  - Set to\_time from get\_datetime(time\_log.to\_time).
  - Set args\_from\_time from get\_datetime(args.from\_time).
  - Set args\_to\_time from get\_datetime(args.to\_time).
  - If (args.get(fieldname) equals time\_log.get(fieldname) and args.idx differs from time\_log.idx and ((args\_from\_time &gt; from\_time and args\_from\_time &lt; to\_time) or (args\_to\_time &gt; from\_time and args\_to\_time &lt; to\_ ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(fieldname) equals time\_log.get(fieldname) → args.idx differs from time\_log.idx → ((args\_from\_time &gt; from\_time and args\_from\_time &lt; to\_time) or (args\_to\_time &gt; from\_time and args\_to\_time &lt; to\_time) or (args\_from\_time ≤ from\_time and args\_to\_time ≥ to\_time)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (args\_from\_time &gt; from\_time and args\_from\_time &lt; to\_time) → (args\_to\_time &gt; from\_time and args\_to\_time &lt; to\_time) → (args\_from\_time ≤ from\_time and args\_to\_time ≥ to\_time).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args\_from\_time &gt; from\_time → args\_from\_time &lt; to\_time.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args\_to\_time &gt; from\_time → args\_to\_time &lt; to\_time.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args\_from\_time ≤ from\_time → args\_to\_time ≥ to\_time.
    - Return true.
- Return false.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0609.json#L756) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L800)

<a id="op-4a015958314da8"></a>
### Timesheet.update cost

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_update_cost`

**Inputs** self.

**Local steps**

- For each time\_log in self.time\_logs.
  - Evaluate time\_log.update\_cost(self.employee, self.currency, self.exchange\_rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L811)

<a id="op-45b12a03842ca1"></a>
### Timesheet.update time rates

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_update_time_rates`

**Inputs** self, ts\_detail.

**Local steps**

- If not ts\_detail.is\_billable.
  - Set ts\_detail.billing\_rate from 0.0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0609.json#L1292) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1364) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L813)

<a id="op-38238d04a1c3da"></a>
### Timesheet.unlink sales invoice

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_timesheet_unlink_sales_invoice`

**Inputs** self, sales\_invoice.

**Local steps**

- For each time\_log in self.time\_logs.
  - If time\_log.sales\_invoice equals sales\_invoice.
    - Set time\_log.sales\_invoice from no value.
- Evaluate self.calculate\_total\_amounts().
- Evaluate self.calculate\_percentage\_billed().
- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate total amounts](operations-014.md#op-7d1b2022cf1434), [calculate percentage billed](operations-014.md#op-d969c281b535f7), [set status](operations-014.md#op-e552a91bab8e0b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0609.json#L1364) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L809)

<a id="op-ed9640d68e7df0"></a>
### Get values used in totals

`operation_enterprise_binding_enterprise_projects_doctype_timesheet_timesheet_get_values_used_in_totals`

**Inputs** time\_log.

**Declared result** (tuple bitwise or no value).

**Explicit results** no value · tuple((time\_log.task or no value), (time\_log.project or no value), get\_datetime(time\_log.from\_time) when time\_log.from\_time, otherwise no value, get\_datetime(time\_log.to\_time) when time\_log.to\_time, otherw ….

**Local steps**

- If not time\_log.
  - Return no value.
- Return tuple((time\_log.task or no value), (time\_log.project or no value), get\_datetime(time\_log.from\_time) when time\_log.from\_time, otherwise no value, get\_datetime(time\_log.to\_time) when time\_log.to\_time, otherw ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in time\_log.task → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in time\_log.project → no value.
  - Value choice on time\_log.from\_time — true gives get\_datetime(time\_log.from\_time), false gives no value.
  - Value choice on time\_log.to\_time — true gives get\_datetime(time\_log.to\_time), false gives no value.
  - Draw fieldname from tuple(“hours”, “costing\_amount”, “billing\_amount”, “base\_costing\_amount”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L246) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1371)

<a id="op-1c33b6b19f5315"></a>
### Get task status

`operation_enterprise_binding_enterprise_projects_doctype_timesheet_timesheet_get_task_status`

**Inputs** task.

**Declared result** str.

**Record and data access** read “Timesheet Detail” via get\_all.

**Explicit results** task.status · “Open” · “Completed” when any(completed), otherwise “Working”.

**Local steps**

- If task.status belongs to tuple(“Completed”, “Cancelled”).
  - Return task.status.
- Set completed from Platform.get\_all(“Timesheet Detail”, filters = mapping(“task” → task.name, “docstatus” → 1, “parenttype” → “Timesheet”), pluck = “completed”).
- If not completed.
  - Return “Open”.
- Return “Completed” when any(completed), otherwise “Working”.
  - Value choice on any(completed) — true gives “Completed”, false gives “Working”.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L245) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1370)

<a id="op-46bfc1d9b5ef2e"></a>
### Get projectwise timesheet data

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_get_projectwise_timesheet_data`

**Inputs** project = no value, parent = no value, from\_time = no value, to\_time = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Timesheet” via get\_list · read “Project” via get\_list.

**Explicit results** list() · query.orderby(tsd.from\_time).run(as\_dict = 1).

**Local steps**

- Set tsd from Platform.qb.DocType(“Timesheet Detail”).
- Set ts from Platform.qb.DocType(“Timesheet”).
- Set allowed\_timesheets from Platform.get\_list(“Timesheet”, pluck = “name”).
- Set allowed\_projects from Platform.get\_list(“Project”, pluck = “name”).
- If not allowed\_timesheets.
  - Return list().
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(tsd.name.as\_(“name”), tsd.parent.as\_(“time\_sheet”) ….
- If allowed\_projects.
  - Set query from query.where((tsd.project.isin(allowed\_projects) bitwise or Coalesce(tsd.project, empty text) equals empty text)).
- Otherwise.
  - Set query from query.where(Coalesce(tsd.project, empty text) equals empty text).
- If project.
  - Set query from query.where(tsd.project equals project).
- If parent.
  - Set query from query.where(tsd.parent equals parent).
- If (from\_time and to\_time).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_time → to\_time.
  - Set query from query.where(Date(tsd.from\_time).between(from\_time, to\_time)).
- Return query.orderby(tsd.from\_time).run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L790)

<a id="op-b39cdb2619899c"></a>
### Get timesheet detail rate

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_get_timesheet_detail_rate`

**Inputs** timelog, currency.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Timesheet” via get\_list.

**Explicit results** 0.0 · (timelog\_detail.billing\_amount × exchange\_rate) · timelog\_detail.billing\_amount.

**Local steps**

- Set allowed\_timesheets from Platform.get\_list(“Timesheet”, pluck = “name”).
- If not allowed\_timesheets.
  - Return 0.0.
- Set ts from Platform.qb.DocType(“Timesheet”).
- Set ts\_detail from Platform.qb.DocType(“Timesheet Detail”).
- Set timelog\_detail from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bi ….
- If not timelog\_detail.
  - Return 0.0.
- Set timelog\_detail from timelog\_detail at 0.
- If timelog\_detail.currency.
  - Set exchange\_rate from get\_exchange\_rate(timelog\_detail.currency, currency).
  - Return (timelog\_detail.billing\_amount × exchange\_rate).
- Return timelog\_detail.billing\_amount.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L793)

<a id="op-c1aba79f2444d4"></a>
### Get timesheet

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_get_timesheet`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Timesheet” via get\_list.

**Explicit results** list() · nested operand in the contract(nested operand in the contract).limit(page\_len).offset(start).run().

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set allowed\_timesheets from Platform.get\_list(“Timesheet”, pluck = “name”).
- If not allowed\_timesheets.
  - Return list().
- Set tsd from Platform.qb.DocType(“Timesheet Detail”).
- Set ts from Platform.qb.DocType(“Timesheet”).
- Set query from nested operand in the contract(nested operand in the contract).select(tsd.parent).distinct().where(((((nested operand in the contract.isin(list(nested operand in the contract, nested operand in the contrac ….
- If filters.get(“project”).
  - Set query from query.where(tsd.project equals filters.get(“project”)).
- Return nested operand in the contract(nested operand in the contract).limit(page\_len).offset(start).run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L791)

<a id="op-e4e81a561a25fe"></a>
### Get timesheet data

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_get_timesheet_data`

**Inputs** name, project = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Timesheet” via get\_list.

**Explicit results** mapping(“billing\_hours” → data at 0.billing\_hours when data, otherwise no value, “billing\_amount” → data at 0.billing\_amt when data, otherwise no value, “timesheet\_detail” → data at 0.name when (data and p ….

**Local steps**

- Set data from no value.
- If project.
  - Set data from get\_projectwise\_timesheet\_data(project, name).
- Otherwise.
  - Set data from Platform.get\_list(“Timesheet”, fields = list(mapping(“SUB” → list(“total\_billable\_amount”, “total\_billed\_amount”), “as” → “billing\_amt”), “total\_billable\_hours as billing\_hours”), filters = mapping(“name” → name)).
- Return mapping(“billing\_hours” → data at 0.billing\_hours when data, otherwise no value, “billing\_amount” → data at 0.billing\_amt when data, otherwise no value, “timesheet\_detail” → data at 0.name when (data and p ….
  - Value choice on data — true gives data at 0.billing\_hours, false gives no value.
  - Value choice on data — true gives data at 0.billing\_amt, false gives no value.
  - Value choice on (data and project and project differs from empty text) — true gives data at 0.name, false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → project → project differs from empty text.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L792)

<a id="op-9b43d0280a4c46"></a>
### Make sales invoice

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_make_sales_invoice`

**Inputs** source\_name, item\_code = no value, customer = no value, currency = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Timesheet” via get\_doc · read “Customer” via get\_value.

**State and service calls** request new\_doc for “Sales Invoice”.

**Explicit results** target.

**Explicit failure paths** validation helper — translated “Invoice can't be made for zero billing hour” · validation helper — translated “Invoice already created for all billing hours”.

**Local steps**

- Set target from Platform.new\_doc(“Sales Invoice”).
- Set timesheet from Platform.get\_doc(“Timesheet”, source\_name).
- Evaluate timesheet.check\_permission(“read”).
- If not timesheet.total\_billable\_hours.
  - Call the validation error handler Platform.throw(translated “Invoice can't be made for zero billing hour”).
- If timesheet.total\_billable\_hours equals timesheet.total\_billed\_hours.
  - Call the validation error handler Platform.throw(translated “Invoice already created for all billing hours”).
- Set hours from (flt(timesheet.total\_billable\_hours) − flt(timesheet.total\_billed\_hours)).
- Set billing\_amount from (flt(timesheet.total\_billable\_amount) − flt(timesheet.total\_billed\_amount)).
- Set billing\_rate from (billing\_amount ÷ hours).
- Set projects from set of log.project for log drawn from timesheet.time\_logs where (log.is\_billable and not log.sales\_invoice).
  - Draw log from timesheet.time\_logs, keep a combination only if ((log.is\_billable and not log.sales\_invoice)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in log.is\_billable → not log.sales\_invoice.
- Set target.company from timesheet.company.
- Set target.project from (timesheet.parent\_project or projects.pop() when len(projects) equals 1, otherwise no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in timesheet.parent\_project → projects.pop() when len(projects) equals 1, otherwise no value.
  - Value choice on len(projects) equals 1 — true gives projects.pop(), false gives no value.
- If customer.
  - Set target.customer from customer.
  - Set default\_price\_list from Platform.get\_value(“Customer”, customer, “default\_price\_list”).
  - If default\_price\_list.
    - Set target.selling\_price\_list from default\_price\_list.
- If currency.
  - Set target.currency from currency.
- If item\_code.
  - Evaluate target.append(“items”, mapping(“item\_code” → item\_code, “qty” → hours, “rate” → billing\_rate)).
- For each time\_log in timesheet.time\_logs.
  - If (time\_log.is\_billable and not time\_log.sales\_invoice).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in time\_log.is\_billable → not time\_log.sales\_invoice.
    - Evaluate target.append(“timesheets”, mapping(“time\_sheet” → timesheet.name, “project\_name” → time\_log.project\_name, “from\_time” → time\_log.from\_time, “to\_time” → time\_log.to\_time, …)).
- Evaluate target.run\_method(“calculate\_billing\_amount\_for\_timesheet”).
- Evaluate target.run\_method(“set\_missing\_values”).
- Return target.

**Values supplied outside this operation** effective access from timesheet.check\_permission(“read”) · selected callable from target.run\_method(“calculate\_billing\_amount\_for\_timesheet”), target.run\_method(“set\_missing\_values”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L795)

<a id="op-9346afa3febb2b"></a>
### Get activity cost

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_get_activity_cost`

**Inputs** employee = no value, activity\_type = no value, currency = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_activity\_cost(employee = employee, activity\_type = activity\_type, currency = currency).

**Local steps**

- If not Platform.has\_permission(“Timesheet”, “read”).
  - Evaluate \_refuse().
- Set activity\_type from cstr(activity\_type).
- If (not activity\_type or not Platform.has\_permission(“Activity Type”, “select”, doc = activity\_type)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not activity\_type → not Platform.has\_permission(“Activity Type”, “select”, doc = activity\_type).
  - Evaluate \_refuse().
- If employee.
  - Set employee from cstr(employee).
  - If not Platform.has\_permission(“Employee”, “select”, doc = employee).
    - Evaluate \_refuse().
- Return \_get\_activity\_cost(employee = employee, activity\_type = activity\_type, currency = currency).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Timesheet”, “read”), Platform.has\_permission(“Activity Type”, “select”, doc = activity\_type) and 1 further calls.

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L787)
