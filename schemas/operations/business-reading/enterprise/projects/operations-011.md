# Projects and time · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Project

[Record definition](../../../../data/record-types/project.json)

<a id="op-f7f56d01224131"></a>
### Planned Vs Completed.today index

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_today_index`

**Inputs** self, dates.

**Declared result** (int bitwise or no value).

**Explicit results** no value · dates.index(self.today).

**Local steps**

- If (self.project.status belongs to CLOSED\_PROJECT\_STATUSES or self.today does not belong to dates).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.project.status belongs to CLOSED\_PROJECT\_STATUSES → self.today does not belong to dates.
  - Return no value.
- Return dates.index(self.today).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L184) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L299) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1309)

<a id="op-ee4319f34cf656"></a>
### Planned Vs Completed.axis dates

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_axis_dates`

**Inputs** self.

**Declared result** list at date.

**Explicit results** list of getdate(add\_days(anchor, (offset × step))) for offset drawn from range(negative steps\_before, (steps\_after + 1)).

**Local steps**

- Set span from date\_diff(self.axis\_end, self.axis\_start).
- Set step from (STEP\_DAYS × max(1, ceil((span ÷ (STEP\_DAYS × MAX\_POINTS))))).
- Set anchor from self.axis\_start.
- If (self.project.status does not belong to CLOSED\_PROJECT\_STATUSES and self.axis\_start ≤ self.today ≤ self.axis\_end).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.project.status does not belong to CLOSED\_PROJECT\_STATUSES → self.axis\_start ≤ self.today ≤ self.axis\_end.
  - Compare adjacent operands in order, stopping at the first false comparison in self.axis\_start ≤ self.today ≤ self.axis\_end.
  - Set anchor from self.today.
- Set steps\_before from ceil((date\_diff(anchor, self.axis\_start) ÷ step)).
- Set steps\_after from ceil((date\_diff(self.axis\_end, anchor) ÷ step)).
- Return list of getdate(add\_days(anchor, (offset × step))) for offset drawn from range(negative steps\_before, (steps\_after + 1)).
  - Draw offset from range(negative steps\_before, (steps\_after + 1)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L285) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1295)

<a id="op-33f656009d0ec2"></a>
### Planned Vs Completed.axis start

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_axis_start`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** date.

**Explicit results** min(starts, default = self.today).

**Local steps**

- If self.project.expected\_start\_date.
  - Set starts from list(getdate(self.project.expected\_start\_date)).
- Otherwise.
  - Set starts from list(self.task\_dates).
- Update starts using + list of self.closed\_date(task) for task drawn from self.tasks where task.status equals “Completed”.
  - Draw task from self.tasks, keep a combination only if (task.status equals “Completed”).
- If self.project.status does not belong to CLOSED\_PROJECT\_STATUSES.
  - Evaluate starts.append(self.today).
- Return min(starts, default = self.today).

**Methods declared on this owner** [closed date](operations-011.md#op-b9b63484807b22).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L287) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1297)

<a id="op-faed77b6ee5925"></a>
### Planned Vs Completed.axis end

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_axis_end`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** date.

**Explicit results** max(ends).

**Local steps**

- Set ends from list(expanded self.task\_dates, self.axis\_start).
- If self.project.expected\_end\_date.
  - Evaluate ends.append(getdate(self.project.expected\_end\_date)).
- If self.project.status does not belong to CLOSED\_PROJECT\_STATUSES.
  - Evaluate ends.append(self.today).
- Return max(ends).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L286) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1296)

<a id="op-1ba4e67a088f5b"></a>
### Planned Vs Completed.task dates

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_task_dates`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** list at date.

**Explicit results** dates.

**Local steps**

- Set dates from list of task.due\_date for task drawn from self.tasks where task.due\_date.
  - Draw task from self.tasks, keep a combination only if (task.due\_date).
- Update dates using + list of getdate(task.exp\_start\_date) for task drawn from self.tasks where task.exp\_start\_date.
  - Draw task from self.tasks, keep a combination only if (task.exp\_start\_date).
- Update dates using + list of self.closed\_date(task) for task drawn from self.tasks where task.status equals “Completed”.
  - Draw task from self.tasks, keep a combination only if (task.status equals “Completed”).
- Return dates.

**Methods declared on this owner** [closed date](operations-011.md#op-b9b63484807b22).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L183) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1308)

<a id="op-4304f7665b6998"></a>
### Planned Vs Completed.has plan

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_has_plan`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** bool.

**Explicit results** (dated × 2) ≥ len(self.tasks).

**Local steps**

- Set dated from sum(generator of 1 for task drawn from self.tasks where task.due\_date).
  - Draw task from self.tasks, keep a combination only if (task.due\_date).
- Return (dated × 2) ≥ len(self.tasks).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L291) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1301)

<a id="op-b71fedd04dbd06"></a>
### Planned Vs Completed.planned date

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_planned_date`

**Inputs** self, task.

**Declared result** date.

**Explicit results** task.due\_date · getdate(self.project.expected\_end\_date) · self.axis\_end.

**Local steps**

- If task.due\_date.
  - Return task.due\_date.
- If self.project.expected\_end\_date.
  - Return getdate(self.project.expected\_end\_date).
- Return self.axis\_end.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1305)

<a id="op-b9b63484807b22"></a>
### Planned Vs Completed.closed date

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_closed_date`

**Inputs** self, task.

**Declared result** date.

**Explicit results** min(closed\_on, self.axis\_end) · closed\_on.

**Local steps**

- Set closed\_on from getdate((task.completed\_on or task.modified)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in task.completed\_on → task.modified.
- If task.status equals “Cancelled”.
  - Return min(closed\_on, self.axis\_end).
- Return closed\_on.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L289) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1299)

<a id="op-1d87da27535f13"></a>
### Planned Vs Completed.weights

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_weights`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** dict at tuple(str, float).

**Explicit results** dict.fromkeys(weights, 1.0) · weights.

**Local steps**

- Set weights from mapping of task.name → flt(task.task\_weight) for task drawn from self.tasks.
  - Draw task from self.tasks.
- If (self.method differs from “Task Weight” or not sum(weights.values())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.method differs from “Task Weight” → not sum(weights.values()).
  - Return dict.fromkeys(weights, 1.0).
- Return weights.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L185) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L300) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1310)

<a id="op-427b14beda3a6d"></a>
### Get unbilled time

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_unbilled_get_unbilled_time`

**Inputs** project.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · mapping(“currency” → Platform.defaults.get\_global\_default(“currency”), “amount” → sum(generator of flt(log.base\_billing\_amount) for log drawn from logs), “hours” → sum(generator of flt(log.billing\_hours) f ….

**Local steps**

- If not Platform.has\_permission(“Timesheet”, “read”).
  - Return no value.
- Set permitted from get\_permitted\_fields(“Timesheet Detail”, parenttype = “Timesheet”, permission\_type = “read”).
- If “base\_billing\_amount” does not belong to permitted.
  - Return no value.
- Set logs from unbilled\_time\_logs(project).
- Return mapping(“currency” → Platform.defaults.get\_global\_default(“currency”), “amount” → sum(generator of flt(log.base\_billing\_amount) for log drawn from logs), “hours” → sum(generator of flt(log.billing\_hours) f ….
  - Draw log from logs.
  - Value choice on “billing\_hours” belongs to permitted — true gives sum(generator of flt(log.billing\_hours) for log drawn from logs), false gives no value.
  - Draw log from logs.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Timesheet”, “read”).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L221) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1346)

<a id="op-ecbd35e321a62e"></a>
### Unbilled time logs

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_unbilled_unbilled_time_logs`

**Inputs** project.

**Declared result** list at Platform.\_dict.

**Record and data access** read “Timesheet” via get\_list · read “Timesheet Detail” via get\_all.

**Explicit results** list() · Platform.get\_all(“Timesheet Detail”, filters = mapping(“parenttype” → “Timesheet”, “parent” → list(“in”, timesheets), “project” → project, “is\_billable” → 1, …), fields = list(“base\_billing\_amount”, “billi ….

**Local steps**

- Set timesheets from Platform.get\_list(“Timesheet”, filters = list(list(“Timesheet Detail”, “project”, “=”, project), list(“docstatus”, “=”, 1)), pluck = “name”, distinct = true, limit\_page\_length = 0).
- If not timesheets.
  - Return list().
- Return Platform.get\_all(“Timesheet Detail”, filters = mapping(“parenttype” → “Timesheet”, “parent” → list(“in”, timesheets), “project” → project, “is\_billable” → 1, …), fields = list(“base\_billing\_amount”, “billi ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L222) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1347)

## Report · Project summary

<a id="op-22829e6670df39"></a>
### Execute

`operation_enterprise_projects_report_project_summary_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “Project” via get\_list.

**Explicit results** tuple(columns, data, no value, chart, …).

**Local steps**

- Set columns from get\_columns().
- Set data from Platform.get\_list(“Project”, filters = filters, fields = list(“name”, “project\_name”, “status”, “percent\_complete”, …), order\_by = “expected\_end\_date”).
- Evaluate set\_task\_counts(data).
- Set chart from get\_chart\_data(data).
- Set report\_summary from get\_report\_summary(data).
- Return tuple(columns, data, no value, chart, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1417) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L858)

<a id="op-f9506bcbd01a4a"></a>
### Set task counts

`operation_enterprise_binding_enterprise_projects_report_project_summary_project_summary_set_task_counts`

**Inputs** projects.

**Record and data access** read “Task” via get\_all.

**Explicit results** no value.

**Local steps**

- If not projects.
  - Return no value.
- Set task\_counts from Platform.get\_all(“Task”, filters = mapping(“project” → list(“in”, list of project.name for project drawn from projects)), fields = list(“project”, “status”, mapping(“COUNT” → “\*”, “as” → “count”)), group\_b ….
  - Draw project from projects.
- For each project in projects.
  - Set counts from mapping of row.status → row.count for row drawn from task\_counts where row.project equals project.name.
    - Draw row from task\_counts, keep a combination only if (row.project equals project.name).
  - Set project at “total\_tasks” from sum(counts.values()).
  - Set project at “completed\_tasks” from counts.get(“Completed”, 0).
  - Set project at “overdue\_tasks” from counts.get(“Overdue”, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L253) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1378)

<a id="op-6f68f63a58f4dd"></a>
### Get columns

`operation_enterprise_projects_report_project_summary_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “name”, “label” → translated “Project”, “fieldtype” → “Link”, “options” → “Project”, …), mapping(“fieldname” → “project\_name”, “label” → translated “Project Name”, “width” → 200) ….

**Local steps**

- Return list(mapping(“fieldname” → “name”, “label” → translated “Project”, “fieldtype” → “Link”, “options” → “Project”, …), mapping(“fieldname” → “project\_name”, “label” → translated “Project Name”, “width” → 200) ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0611.json#L2565) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1419) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L860)

<a id="op-72ea0e0eb84392"></a>
### Get chart data

`operation_enterprise_projects_report_project_summary_business_behavior_get_chart_data`

**Inputs** data.

**Explicit results** mapping(“data” → mapping(“labels” → labels at slice no value to 30, “datasets” → list(mapping(“name” → translated “Overdue”, “values” → overdue at slice no value to 30), mapping(“name” → translated “Comple ….

**Local steps**

- Set labels from list().
- Set total from list().
- Set completed from list().
- Set overdue from list().
- For each project in data.
  - Evaluate labels.append(project.project\_name).
  - Evaluate total.append(project.total\_tasks).
  - Evaluate completed.append(project.completed\_tasks).
  - Evaluate overdue.append(project.overdue\_tasks).
- Return mapping(“data” → mapping(“labels” → labels at slice no value to 30, “datasets” → list(mapping(“name” → translated “Overdue”, “values” → overdue at slice no value to 30), mapping(“name” → translated “Comple ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0611.json#L3483) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1418) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L859)

<a id="op-f83d0c6ab8e3e6"></a>
### Get report summary

`operation_enterprise_projects_report_project_summary_business_behavior_get_report_summary`

**Inputs** data.

**Explicit results** no value · list(mapping(“value” → avg\_completion, “indicator” → “Green” when avg\_completion &gt; 50, otherwise “Red”, “label” → translated “Average Completion”, “datatype” → “Percent”), mapping(“value” → total, “indicat ….

**Local steps**

- If not data.
  - Return no value.
- Set avg\_completion from (sum(generator of project.percent\_complete for project drawn from data) ÷ len(data)).
  - Draw project from data.
- Set total from sum(list of project.total\_tasks for project drawn from data).
  - Draw project from data.
- Set total\_overdue from sum(list of project.overdue\_tasks for project drawn from data).
  - Draw project from data.
- Set completed from sum(list of project.completed\_tasks for project drawn from data).
  - Draw project from data.
- Return list(mapping(“value” → avg\_completion, “indicator” → “Green” when avg\_completion &gt; 50, otherwise “Red”, “label” → translated “Average Completion”, “datatype” → “Percent”), mapping(“value” → total, “indicat ….
  - Value choice on avg\_completion &gt; 50 — true gives “Green”, false gives “Red”.
  - Value choice on total\_overdue equals 0 — true gives “Green”, false gives “Red”.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0611.json#L4001) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L861)

## Record · Project template

[Record definition](../../../../data/record-types/project_template.json)

<a id="op-a1d968c2796500"></a>
### Project Template.validate

`operation_enterprise_projects_record_definitions_project_template_business_behavior_project_template_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_template\_tasks().
- Evaluate self.validate\_dependencies().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate template tasks](operations-011.md#op-1b1c29cbcb5bb9), [validate dependencies](operations-011.md#op-1333d5990de34d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L714)

<a id="op-1b1c29cbcb5bb9"></a>
### Project Template.validate template tasks

`operation_enterprise_binding_enterprise_projects_doctype_project_template_project_template_projecttemplate_validate_template_tasks`

**Inputs** self.

**Record and data access** read “Task” via get\_all.

**Explicit failure paths** validation helper — translated “Row {0}: Task {1} is not a Template Task”.format(row.idx, get\_link\_to\_form(“Task”, task.name)) · validation helper — translated “Row {0}: Task {1} ends after its parent task {2}”.format(row.idx, get\_link\_to\_form(“Task”, task.name), get\_link\_to\_form(“Task”, parent.name)).

**Local steps**

- Set tasks from mapping of task.name → task for task drawn from Platform.get\_all(“Task”, filters = mapping(“name” → list(“in”, list of row.task for row drawn from self.tasks)), fields = list(“name”, “is\_template”, “parent ….
  - Draw task from Platform.get\_all(“Task”, filters = mapping(“name” → list(“in”, list of row.task for row drawn from self.tasks)), fields = list(“name”, “is\_template”, “parent\_task”, “start”, …)).
  - Draw row from self.tasks.
- For each row in self.tasks.
  - Set task from tasks at row.task.
  - If not task.is\_template.
    - Call the validation error handler Platform.throw(translated “Row {0}: Task {1} is not a Template Task”.format(row.idx, get\_link\_to\_form(“Task”, task.name))).
  - Set parent from tasks.get(task.parent\_task).
  - If (parent and (task.start + task.duration) &gt; (parent.start + parent.duration)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent → (task.start + task.duration) &gt; (parent.start + parent.duration).
    - Call the validation error handler Platform.throw(translated “Row {0}: Task {1} ends after its parent task {2}”.format(row.idx, get\_link\_to\_form(“Task”, task.name), get\_link\_to\_form(“Task”, parent.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L230) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1355)

<a id="op-1333d5990de34d"></a>
### Project Template.validate dependencies

`operation_enterprise_projects_record_definitions_project_template_business_behavior_project_template_validate_dependencies`

**Inputs** self.

**Record and data access** resolve a document from “Task” via get\_doc.

**Explicit failure paths** validation helper — translated “Task {0} depends on Task {1}. Please add Task {1} to the Tasks list.”.format(Platform.bold(task\_details\_format), Platform.bold(dependency\_task\_format)).

**Local steps**

- For each task in self.tasks.
  - Set task\_details from Platform.get\_doc(“Task”, task.task).
  - If task\_details.depends\_on.
    - For each dependency\_task in task\_details.depends\_on.
      - If not self.check\_dependent\_task\_presence(dependency\_task.task).
        - Set task\_details\_format from get\_link\_to\_form(“Task”, task\_details.name).
        - Set dependency\_task\_format from get\_link\_to\_form(“Task”, dependency\_task.task).
        - Call the validation error handler Platform.throw(translated “Task {0} depends on Task {1}. Please add Task {1} to the Tasks list.”.format(Platform.bold(task\_details\_format), Platform.bold(dependency\_task\_format))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check dependent task presence](operations-011.md#op-4d8c92494a89cd).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0604.json#L1670) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L715)

<a id="op-4d8c92494a89cd"></a>
### Project Template.check dependent task presence

`operation_enterprise_projects_record_definitions_project_template_business_behavior_project_template_check_dependent_task_presence`

**Inputs** self, task.

**Explicit results** true · false.

**Local steps**

- For each task\_details in self.tasks.
  - If task\_details.task equals task.
    - Return true.
- Return false.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0604.json#L2007) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L713)

<a id="op-c570f4b4b10f80"></a>
### Get data

`operation_enterprise_projects_record_definitions_project_template_project_template_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “project\_template”, “transactions” → list(mapping(“items” → list(“Project”)))).

**Local steps**

- Return mapping(“fieldname” → “project\_template”, “transactions” → list(mapping(“items” → list(“Project”)))).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0604.json#L2103) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L716)

## Record · Project type

[Record definition](../../../../data/record-types/project_type.json)

<a id="op-0afda22b35ec83"></a>
### Project Type.on trash

`operation_enterprise_projects_record_definitions_project_type_business_behavior_project_type_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “You cannot delete Project Type 'External'”.

**Local steps**

- If self.name equals “External”.
  - Call the validation error handler Platform.throw(translated “You cannot delete Project Type 'External'”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0604.json#L3005) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1280) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L735)

## Record · Project update

[Record definition](../../../../data/record-types/project_update.json)

<a id="op-4f7da9a11f1c29"></a>
### Daily reminder

`operation_enterprise_projects_record_definitions_project_update_business_behavior_daily_reminder`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Holiday” via exists · read “Project” via get\_all · read “Project Update” via count · read “Project Update” via get\_all.

**Local steps**

- Evaluate Platform.only\_for(“Projects Manager”).
- Set holiday\_today from Platform.db.exists(“Holiday”, mapping(“holiday\_date” → today())).
- Set projects from Platform.get\_all(“Project”, fields = list(“name”, “project\_name”, “frequency”, “expected\_start\_date”, …), limit\_page\_length = 0).
- For each project in projects.
  - Set project\_id from project.name.
  - Set frequency from project.frequency.
  - Set date\_start from project.expected\_start\_date.
  - Set date\_end from project.expected\_end\_date.
  - Set progress from project.percent\_complete.
  - Set number\_of\_drafts from Platform.db.count(“Project Update”, mapping(“project” → project\_id, “docstatus” → 0)).
  - Set update from Platform.get\_all(“Project Update”, filters = mapping(“project” → project\_id, “date” → add\_days(today(), negative 1)), fields = list(“name”, “date”, “time”), as\_list = true).
  - Evaluate email\_sending(project\_id, project.project\_name, frequency, date\_start, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“Projects Manager”) · clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0604.json#L3103) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1281) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L736)

<a id="op-f03b0f45391910"></a>
### Email sending

`operation_enterprise_projects_record_definitions_project_update_business_behavior_email_sending`

**Inputs** project\_id, project\_name, frequency, date\_start, date\_end, progress, number\_of\_drafts, update, holiday\_today.

**Record and data access** read “Project User” via get\_all.

**State and service calls** sendmail.

**Local steps**

- Set msg from (((((((nested operand in the contract + nested operand in the contract) + nested operand in the contract(nested operand in the contract)) + “&lt;/p&gt;”) + “&lt;/p&gt;&lt;p&gt;Number of drafts:”) + one space) + str(number\_o ….
- Update msg using + “&lt;/u&gt;&lt;/b&gt;&lt;/p&gt;&lt;table class='table table-bordered'&gt;&lt;tr&gt;\\n                &lt;th&gt;Project ID&lt;/th&gt;&lt;th&gt;Date Updated&lt;/t …”.
- For each updates in update.
  - Update msg using + ((((((text in the contract + nested operand in the contract(nested operand in the contract)) + “&lt;/td&gt;&lt;td&gt;”) + str(updates at 1)) + “&lt;/td&gt;&lt;td&gt;”) + str(updates at 2)) + “&lt;/td&gt;&lt;/tr&gt;”).
- Update msg using + “&lt;/table&gt;”.
- If not holiday\_today.
  - Set recipients from Platform.get\_all(“Project User”, filters = mapping(“parent” → project\_id), pluck = “user”, limit\_page\_length = 0).
  - For each user in recipients.
    - Evaluate Platform.sendmail(recipients = list(user), subject = Platform.\_(((project\_name + one space) + “Summary”)), message = msg).
- Otherwise.
  - Take no action here.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = list(user), subject = Platform.\_(((project\_name + one space) + “Summary”)), message = msg).

**Boundaries to resolve** stored data, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0604.json#L3736) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1282) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L737)
