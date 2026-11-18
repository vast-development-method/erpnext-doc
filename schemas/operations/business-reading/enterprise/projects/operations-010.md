# Projects and time · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Project

[Record definition](../../../../data/record-types/project.json)

<a id="op-8a23309eb310bd"></a>
### Project Overview.can be late

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_can_be_late`

**Inputs** self, task.

**Declared result** bool.

**Explicit results** bool((task.due\_date and task.completed\_on)).

**Local steps**

- Return bool((task.due\_date and task.completed\_on)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in task.due\_date → task.completed\_on.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L191) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1316)

<a id="op-975105b1bebb7e"></a>
### Project Overview.finished late

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_finished_late`

**Inputs** self, task.

**Declared result** bool.

**Explicit results** (self.can\_be\_late(task) and self.completed\_date(task) &gt; task.due\_date).

**Local steps**

- Return (self.can\_be\_late(task) and self.completed\_date(task) &gt; task.due\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.can\_be\_late(task) → self.completed\_date(task) &gt; task.due\_date.

**Methods declared on this owner** [can be late](operations-010.md#op-8a23309eb310bd), [completed date](operations-010.md#op-04d756e1180838).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L196) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L311) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1321)

<a id="op-04d756e1180838"></a>
### Project Overview.completed date

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_completed_date`

**Inputs** self, task.

**Declared result** date.

**Explicit results** getdate((task.completed\_on or task.modified)).

**Local steps**

- Return getdate((task.completed\_on or task.modified)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in task.completed\_on → task.modified.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L193) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1318)

<a id="op-4885ce69337f26"></a>
### Project Overview.days late

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_days_late`

**Inputs** self, task.

**Declared result** int.

**Explicit results** date\_diff(self.today, task.due\_date).

**Local steps**

- Return date\_diff(self.today, task.due\_date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L194) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1319)

<a id="op-7f178daa86995d"></a>
### Project Overview.blocked tasks

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_blocked_tasks`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** set at str.

**Record and data access** read “Task Depends On” via get\_all · read “Task” via get\_all.

**Explicit results** set() · set of row.parent for row drawn from dependencies where (row.task belongs to unfinished and unfinished at row.task differs from row.parent).

**Local steps**

- If not self.open\_tasks.
  - Return set().
- Set dependencies from Platform.get\_all(“Task Depends On”, filters = mapping(“parenttype” → “Task”, “parent” → list(“in”, list of task.name for task drawn from self.open\_tasks)), fields = list(“parent”, “task”)).
  - Draw task from self.open\_tasks.
- If not dependencies.
  - Return set().
- Set unfinished from mapping of task.name → task.parent\_task for task drawn from Platform.get\_all(“Task”, filters = mapping(“name” → list(“in”, list(set of nested operand in the contract.task for row drawn from dependencies)), ….
  - Draw task from Platform.get\_all(“Task”, filters = mapping(“name” → list(“in”, list(set of row.task for row drawn from dependencies)), “status” → list(“not in”, CLOSED\_STATUSES)), fields = list(“name”, “parent\_task”)).
  - Draw row from dependencies.
- Return set of row.parent for row drawn from dependencies where (row.task belongs to unfinished and unfinished at row.task differs from row.parent).
  - Draw row from dependencies, keep a combination only if ((row.task belongs to unfinished and unfinished at row.task differs from row.parent)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.task belongs to unfinished → unfinished at row.task differs from row.parent.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L189) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L304) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1314)

<a id="op-a8814576712a32"></a>
### Project Overview.open tasks

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_open_tasks`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** list at Platform.\_dict.

**Explicit results** list of task for task drawn from self.tasks where not task.is\_closed.

**Local steps**

- Return list of task for task drawn from self.tasks where not task.is\_closed.
  - Draw task from self.tasks, keep a combination only if (not task.is\_closed).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L208) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L323) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1333)

<a id="op-db100f6fcbf0dd"></a>
### Project Overview.tasks

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_tasks`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** list at Platform.\_dict.

**Record and data access** read “Task” via get\_list.

**Explicit results** tasks.

**Local steps**

- Set tasks from Platform.get\_list(“Task”, filters = mapping(“project” → self.project.name, “is\_template” → 0, “status” → list(“!=”, “Template”)), fields = list(“name”, “subject”, “status”, “priority”, …), limit\_page\_length = 0).
- For each task in tasks.
  - Set task.due\_date from getdate(task.exp\_end\_date) when task.exp\_end\_date, otherwise no value.
    - Value choice on task.exp\_end\_date — true gives getdate(task.exp\_end\_date), false gives no value.
  - Set task.assigned\_to from json.loads((task.\_assign or “&#91;&#93;”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in task.\_assign → “&#91;&#93;”.
  - Set task.is\_closed from task.status belongs to CLOSED\_STATUSES.
- Return tasks.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L215) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1340)

<a id="op-e11c816d346fe1"></a>
### Task Breakdown.initialize

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_breakdown_taskbreakdown_init`

**Inputs** self, overview.

**Local steps**

- Set self.overview from overview.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L279) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1289)

<a id="op-5dfed1369e1a99"></a>
### Task Breakdown.by status

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_breakdown_taskbreakdown_by_status`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“statuses” → list of mapping(“status” → status, “count” → len(tasks at status), “tasks” → tasks at status) for status drawn from tuple(expanded TASK\_STATUSES, expanded custom) where status belongs  ….

**Local steps**

- Set tasks from mapping().
- For each task in self.overview.tasks.
  - Evaluate tasks.setdefault(self.status(task), list()).append(task.name).
- Set custom from sorted(generator of status for status drawn from tasks where status does not belong to TASK\_STATUSES).
  - Draw status from tasks, keep a combination only if (status does not belong to TASK\_STATUSES).
- Return mapping(“statuses” → list of mapping(“status” → status, “count” → len(tasks at status), “tasks” → tasks at status) for status drawn from tuple(expanded TASK\_STATUSES, expanded custom) where status belongs  ….
  - Draw status from tuple(expanded TASK\_STATUSES, expanded custom), keep a combination only if (status belongs to tasks).

**Methods declared on this owner** [status](operations-010.md#op-d423848ed55632).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L278) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1288)

<a id="op-8596796c28da82"></a>
### Task Breakdown.by assignee

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_breakdown_taskbreakdown_by_assignee`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“rows” → sorted(rows.values(), key = deferred anonymous expression)).

**Local steps**

- Set rows from mapping().
- For each task in self.workload\_tasks.
  - For each user in (task.assigned\_to or list(no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in task.assigned\_to → list(no value).
    - Set row from rows.setdefault(user, mapping(“user” → user, “open” → 0, “overdue” → 0, “tasks” → list())).
    - Update row at “open” using + 1.
    - Update row at “overdue” using + self.overview.is\_overdue(task).
    - Evaluate row at “tasks”.append(task.name).
- Return mapping(“rows” → sorted(rows.values(), key = deferred anonymous expression)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L275) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1285)

<a id="op-b0f8bec5928605"></a>
### Task Breakdown.by delivery

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_breakdown_taskbreakdown_by_delivery`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“outcomes” → list of mapping(“outcome” → outcome, “count” → len(tasks at outcome), “tasks” → tasks at outcome) for outcome drawn from DELIVERY\_OUTCOMES where outcome belongs to tasks, “total” → len ….

**Local steps**

- Set tasks from mapping().
- For each task in self.overview.tasks.
  - Evaluate tasks.setdefault(self.outcome(task), list()).append(task.name).
- Return mapping(“outcomes” → list of mapping(“outcome” → outcome, “count” → len(tasks at outcome), “tasks” → tasks at outcome) for outcome drawn from DELIVERY\_OUTCOMES where outcome belongs to tasks, “total” → len ….
  - Draw outcome from DELIVERY\_OUTCOMES, keep a combination only if (outcome belongs to tasks).

**Methods declared on this owner** [outcome](operations-010.md#op-8bc632ab1d7dad).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L277) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1287)

<a id="op-16af37b4582503"></a>
### Task Breakdown.by completer

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_breakdown_taskbreakdown_by_completer`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“rows” → sorted(rows.values(), key = deferred anonymous expression)).

**Local steps**

- Set completed from list of task for task drawn from self.overview.tasks where (task.status equals “Completed” and not task.is\_group).
  - Draw task from self.overview.tasks, keep a combination only if ((task.status equals “Completed” and not task.is\_group)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in task.status equals “Completed” → not task.is\_group.
- Set assignees from self.assignees(completed).
- Set rows from mapping().
- For each task in completed.
  - For each user in (sorted(assignees at task.name) or list(no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sorted(assignees at task.name) → list(no value).
    - Set row from rows.setdefault(user, mapping(“user” → user, “completed” → 0, “late” → 0, “tasks” → list())).
    - Update row at “completed” using + 1.
    - Update row at “late” using + self.overview.finished\_late(task).
    - Evaluate row at “tasks”.append(task.name).
- Return mapping(“rows” → sorted(rows.values(), key = deferred anonymous expression)).

**Methods declared on this owner** [assignees](operations-010.md#op-27e7703cfc4114).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L276) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1286)

<a id="op-27e7703cfc4114"></a>
### Task Breakdown.assignees

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_breakdown_taskbreakdown_assignees`

**Inputs** self, tasks.

**Declared result** dict at tuple(str, set at str).

**Record and data access** read “ToDo” via get\_all.

**Explicit results** people.

**Local steps**

- Set people from mapping of task.name → set(task.assigned\_to) for task drawn from tasks.
  - Draw task from tasks.
- If not tasks.
  - Return people.
- For each todo in Platform.get\_all(“ToDo”, filters = mapping(“reference\_type” → “Task”, “reference\_name” → list(“in”, list(people)), “status” → list(“!=”, “Cancelled”)), fields = list(“reference\_name”, “allocated\_to”)).
  - Evaluate people at todo.reference\_name.add(todo.allocated\_to).
- Return people.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L274) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1284)

<a id="op-8bc632ab1d7dad"></a>
### Task Breakdown.outcome

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_breakdown_taskbreakdown_outcome`

**Inputs** self, task.

**Declared result** str.

**Explicit results** “Cancelled” · “Still Open” · “No Due Date” · “Late” when self.overview.finished\_late(task), otherwise “On Time”.

**Local steps**

- If task.status equals “Cancelled”.
  - Return “Cancelled”.
- If task.status differs from “Completed”.
  - Return “Still Open”.
- If not self.overview.can\_be\_late(task).
  - Return “No Due Date”.
- Return “Late” when self.overview.finished\_late(task), otherwise “On Time”.
  - Value choice on self.overview.finished\_late(task) — true gives “Late”, false gives “On Time”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L280) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1290)

<a id="op-d423848ed55632"></a>
### Task Breakdown.status

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_breakdown_taskbreakdown_status`

**Inputs** self, task.

**Declared result** str.

**Explicit results** task.status when task.is\_closed, otherwise self.overview.open\_status(task).

**Local steps**

- Return task.status when task.is\_closed, otherwise self.overview.open\_status(task).
  - Value choice on task.is\_closed — true gives task.status, false gives self.overview.open\_status(task).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L281) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1291)

<a id="op-7266cf3d86d7dc"></a>
### Task Breakdown.workload tasks

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_breakdown_taskbreakdown_workload_tasks`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** list at Platform.\_dict.

**Explicit results** list of task for task drawn from self.overview.open\_tasks where not task.is\_group.

**Local steps**

- Return list of task for task drawn from self.overview.open\_tasks where not task.is\_group.
  - Draw task from self.overview.open\_tasks, keep a combination only if (not task.is\_group).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L282) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1292)

<a id="op-64d50e61fa3a90"></a>
### Planned Vs Completed.initialize

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_init`

**Inputs** self, project, tasks, today.

**Local steps**

- Set self.project from project.
- Set self.tasks from tasks.
- Set self.today from today.
- Set self.method from project.percent\_complete\_method.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L292) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1302)

<a id="op-cccf553bb46a22"></a>
### Planned Vs Completed.build

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_build`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“method” → self.method, “points” → list()) · mapping(“method” → self.method, “points” → list of self.point(on, on equals latest) for on drawn from dates, “today\_index” → self.today\_index(dates), “has\_plan” → self.has\_plan, …).

**Local steps**

- If (self.method equals “Manual” or self.project.status equals “Cancelled” or all(generator of task.status equals “Cancelled” for task drawn from self.tasks)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.method equals “Manual” → self.project.status equals “Cancelled” → all(generator of task.status equals “Cancelled” for task drawn from self.tasks).
  - Draw task from self.tasks.
  - Return mapping(“method” → self.method, “points” → list()).
- Set dates from self.axis\_dates().
- Set latest from max(generator of on for on drawn from dates where on ≤ self.today, default = no value).
  - Draw on from dates, keep a combination only if (on ≤ self.today).
- Return mapping(“method” → self.method, “points” → list of self.point(on, on equals latest) for on drawn from dates, “today\_index” → self.today\_index(dates), “has\_plan” → self.has\_plan, …).
  - Draw on from dates.
  - Draw task from self.tasks, keep a combination only if (not task.due\_date).
  - Draw task from self.tasks, keep a combination only if ((task.status equals “Completed” and not task.completed\_on)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in task.status equals “Completed” → not task.completed\_on.
  - Value choice on (self.project.status equals “Completed” and self.has\_plan) — true gives self.worst\_gap(), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.project.status equals “Completed” → self.has\_plan.

**Methods declared on this owner** [axis dates](operations-011.md#op-ee4319f34cf656), [point](operations-010.md#op-f252f42451894a), [today index](operations-011.md#op-f7f56d01224131), [worst gap](operations-010.md#op-2e7bb065cae8cb).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L288) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1298)

<a id="op-2e7bb065cae8cb"></a>
### Planned Vs Completed.worst gap

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_worst_gap`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“points” → flt(worst, 1), “date” → str(worst\_on) when worst\_on, otherwise no value).

**Local steps**

- Set total from sum(self.weights.values()).
- Set planned from sorted(generator of tuple(self.planned\_date(task), self.weights at task.name) for task drawn from self.tasks).
  - Draw task from self.tasks.
- Set completed from sorted(generator of tuple(self.closed\_date(task), self.weights at task.name) for task drawn from self.tasks where task.is\_closed).
  - Draw task from self.tasks, keep a combination only if (task.is\_closed).
- Set tuple(worst, worst\_on) from tuple(0, no value).
- Set planned\_weight, completed\_weight from 0.
- Set done from 0.
- For each tuple(on, due) in groupby(planned, key = itemgetter(0)).
  - If on &gt; self.today.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Update planned\_weight using + sum(generator of weight for tuple(\_, weight) drawn from due).
    - Draw tuple(\_, weight) from due.
  - While (done &lt; len(completed) and completed at done at 0 ≤ on).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in done &lt; len(completed) → completed at done at 0 ≤ on.
    - Update completed\_weight using + completed at done at 1.
    - Update done using + 1.
  - Set gap from (((planned\_weight − completed\_weight) ÷ total) × 100) when total, otherwise 0.
    - Value choice on total — true gives (((planned\_weight − completed\_weight) ÷ total) × 100), false gives 0.
  - If gap &gt; worst.
    - Set tuple(worst, worst\_on) from tuple(gap, on).
- Return mapping(“points” → flt(worst, 1), “date” → str(worst\_on) when worst\_on, otherwise no value).
  - Value choice on worst\_on — true gives str(worst\_on), false gives no value.

**Methods declared on this owner** [planned date](operations-011.md#op-b71fedd04dbd06), [closed date](operations-011.md#op-b9b63484807b22).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L301) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1311)

<a id="op-f252f42451894a"></a>
### Planned Vs Completed.point

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_point`

**Inputs** self, on, is\_latest.

**Declared result** dict.

**Explicit results** mapping(“date” → str(on), “planned” → self.percent(self.planned\_weight(on)) when self.has\_plan, otherwise no value, “completed” → completed).

**Local steps**

- Set completed from no value.
- If on ≤ self.today.
  - Set completed from self.percent(self.completed\_weight(self.today when is\_latest, otherwise on, is\_latest)).
    - Value choice on is\_latest — true gives self.today, false gives on.
- Return mapping(“date” → str(on), “planned” → self.percent(self.planned\_weight(on)) when self.has\_plan, otherwise no value, “completed” → completed).
  - Value choice on self.has\_plan — true gives self.percent(self.planned\_weight(on)), false gives no value.

**Methods declared on this owner** [percent](operations-010.md#op-8028887acd956e), [completed weight](operations-010.md#op-5bffc381ef392f), [planned weight](operations-010.md#op-93ff106dc7b893).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L182) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1307)

<a id="op-93ff106dc7b893"></a>
### Planned Vs Completed.planned weight

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_planned_weight`

**Inputs** self, on.

**Declared result** float.

**Explicit results** sum(generator of self.weights at task.name for task drawn from self.tasks where self.planned\_date(task) ≤ on).

**Local steps**

- Return sum(generator of self.weights at task.name for task drawn from self.tasks where self.planned\_date(task) ≤ on).
  - Draw task from self.tasks, keep a combination only if (self.planned\_date(task) ≤ on).

**Methods declared on this owner** [planned date](operations-011.md#op-b71fedd04dbd06).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1306)

<a id="op-5bffc381ef392f"></a>
### Planned Vs Completed.completed weight

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_completed_weight`

**Inputs** self, on, with\_progress.

**Declared result** float.

**Explicit results** (done + self.open\_progress when with\_progress, otherwise 0).

**Local steps**

- Set done from sum(generator of self.weights at task.name for task drawn from self.tasks where (task.is\_closed and self.closed\_date(task) ≤ on)).
  - Draw task from self.tasks, keep a combination only if ((task.is\_closed and self.closed\_date(task) ≤ on)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in task.is\_closed → self.closed\_date(task) ≤ on.
- Return (done + self.open\_progress when with\_progress, otherwise 0).
  - Value choice on with\_progress — true gives self.open\_progress, false gives 0.

**Methods declared on this owner** [closed date](operations-011.md#op-b9b63484807b22).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L290) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1300)

<a id="op-76d77155c7b41d"></a>
### Planned Vs Completed.open progress

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_open_progress`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** float.

**Explicit results** 0 · sum(generator of ((self.weights at task.name × flt(task.progress)) ÷ 100) for task drawn from self.tasks where not task.is\_closed).

**Local steps**

- If self.method equals “Task Completion”.
  - Return 0.
- Return sum(generator of ((self.weights at task.name × flt(task.progress)) ÷ 100) for task drawn from self.tasks where not task.is\_closed).
  - Draw task from self.tasks, keep a combination only if (not task.is\_closed).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L293) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1303)

<a id="op-8028887acd956e"></a>
### Planned Vs Completed.percent

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_progress_plannedvscompleted_percent`

**Inputs** self, weight.

**Declared result** float.

**Explicit results** flt(((weight ÷ total) × 100), 1) when total, otherwise 0.

**Local steps**

- Set total from sum(self.weights.values()).
- Return flt(((weight ÷ total) × 100), 1) when total, otherwise 0.
  - Value choice on total — true gives flt(((weight ÷ total) × 100), 1), false gives 0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L294) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1304)
