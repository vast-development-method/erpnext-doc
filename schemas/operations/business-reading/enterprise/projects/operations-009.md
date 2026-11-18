# Projects and time · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Project

[Record definition](../../../../data/record-types/project.json)

<a id="op-3145176a233b38"></a>
### Project Overview.milestone

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_milestone`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“next” → self.milestone\_details(upcoming at 0) when upcoming, otherwise no value, “all\_met” → (bool(milestones) and not upcoming)).

**Local steps**

- Set milestones from list of task for task drawn from self.tasks where task.is\_milestone.
  - Draw task from self.tasks, keep a combination only if (task.is\_milestone).
- Set upcoming from sorted(generator of task for task drawn from milestones where task.status does not belong to CLOSED\_STATUSES, key = deferred anonymous expression).
  - Draw task from milestones, keep a combination only if (task.status does not belong to CLOSED\_STATUSES).
- Return mapping(“next” → self.milestone\_details(upcoming at 0) when upcoming, otherwise no value, “all\_met” → (bool(milestones) and not upcoming)).
  - Value choice on upcoming — true gives self.milestone\_details(upcoming at 0), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(milestones) → not upcoming.

**Methods declared on this owner** [milestone details](operations-009.md#op-8a03a5f73efaa8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L203) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1328)

<a id="op-3b17c6560d75ce"></a>
### Project Overview.planned vs completed

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_planned_vs_completed`

**Inputs** self.

**Declared result** dict.

**Explicit results** PlannedVsCompleted(self.project, self.tasks, self.today).build().

**Local steps**

- Return PlannedVsCompleted(self.project, self.tasks, self.today).build().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L210) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L325) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1335)

<a id="op-7a1464c65b8ddc"></a>
### Project Overview.tasks by status

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_tasks_by_status`

**Inputs** self.

**Declared result** dict.

**Explicit results** TaskBreakdown(self).by\_status().

**Local steps**

- Return TaskBreakdown(self).by\_status().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L217) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1342)

<a id="op-46f195bd7314e1"></a>
### Project Overview.workload

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_workload`

**Inputs** self.

**Declared result** dict.

**Explicit results** TaskBreakdown(self).by\_assignee().

**Local steps**

- Return TaskBreakdown(self).by\_assignee().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L220) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1345)

<a id="op-7993e35076dfa7"></a>
### Project Overview.tasks by delivery

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_tasks_by_delivery`

**Inputs** self.

**Declared result** (dict bitwise or no value).

**Explicit results** TaskBreakdown(self).by\_delivery() when self.is\_closed, otherwise no value.

**Local steps**

- Return TaskBreakdown(self).by\_delivery() when self.is\_closed, otherwise no value.
  - Value choice on self.is\_closed — true gives TaskBreakdown(self).by\_delivery(), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L216) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1341)

<a id="op-e9b40c9d981ca2"></a>
### Project Overview.completed by assignee

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_completed_by_assignee`

**Inputs** self.

**Declared result** (dict bitwise or no value).

**Explicit results** TaskBreakdown(self).by\_completer() when self.is\_closed, otherwise no value.

**Local steps**

- Return TaskBreakdown(self).by\_completer() when self.is\_closed, otherwise no value.
  - Value choice on self.is\_closed — true gives TaskBreakdown(self).by\_completer(), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L192) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1317)

<a id="op-07a40db4cbd2c8"></a>
### Project Overview.unbilled

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_unbilled`

**Inputs** self.

**Declared result** (dict bitwise or no value).

**Explicit results** get\_unbilled\_time(self.project.name).

**Local steps**

- Return get\_unbilled\_time(self.project.name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L218) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1343)

<a id="op-5ae6637fa6174f"></a>
### Project Overview.profitability

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_profitability`

**Inputs** self.

**Declared result** (dict bitwise or no value).

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value · mapping(“currency” → Platform.get\_cached\_value(“Company”, self.project.company, “default\_currency”), “billed” → billed, “cost” → (billed − margin), “margin” → margin, …).

**Local steps**

- If self.hidden\_fields.intersection(MARGIN\_FIELDS).
  - Return no value.
- Set billed from flt(self.project.total\_billed\_amount).
- Set margin from flt(self.project.gross\_margin).
- Return mapping(“currency” → Platform.get\_cached\_value(“Company”, self.project.company, “default\_currency”), “billed” → billed, “cost” → (billed − margin), “margin” → margin, …).
  - Value choice on billed — true gives flt(self.project.per\_gross\_margin, 1), false gives no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.project.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L212) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1337)

<a id="op-7dd1c0deba49c8"></a>
### Project Overview.stats

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_stats`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“open\_tasks” → self.open\_task\_stats(), “overdue” → self.overdue\_stats(), “hours” → self.hours\_stats()).

**Local steps**

- Return mapping(“open\_tasks” → self.open\_task\_stats(), “overdue” → self.overdue\_stats(), “hours” → self.hours\_stats()).

**Methods declared on this owner** [open task stats](operations-009.md#op-1b3961df951111), [overdue stats](operations-009.md#op-fbdaea5ae7d188), [hours stats](operations-009.md#op-ad6830ff159a6a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L213) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1338)

<a id="op-52b51058199e05"></a>
### Project Overview.delivery

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_delivery`

**Inputs** self.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · mapping(“status” → self.project.status, “percent\_complete” → flt(self.project.percent\_complete, 1), “finished\_on” → finished\_on, “planned\_end” → planned\_end, …).

**Local steps**

- If not self.is\_closed.
  - Return no value.
- Set completed from list of task for task drawn from self.tasks where task.status equals “Completed”.
  - Draw task from self.tasks, keep a combination only if (task.status equals “Completed”).
- Set finished\_on from max(generator of self.completed\_date(task) for task drawn from completed, default = no value).
  - Draw task from completed.
- Set planned\_end from getdate(self.project.expected\_end\_date) when self.project.expected\_end\_date, otherwise no value.
  - Value choice on self.project.expected\_end\_date — true gives getdate(self.project.expected\_end\_date), false gives no value.
- Set rated from list of task for task drawn from completed where self.can\_be\_late(task).
  - Draw task from completed, keep a combination only if (self.can\_be\_late(task)).
- Return mapping(“status” → self.project.status, “percent\_complete” → flt(self.project.percent\_complete, 1), “finished\_on” → finished\_on, “planned\_end” → planned\_end, …).
  - Value choice on (finished\_on and planned\_end) — true gives date\_diff(finished\_on, planned\_end), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in finished\_on → planned\_end.
  - Draw task from self.tasks, keep a combination only if (task.status equals “Cancelled”).
  - Draw task from rated, keep a combination only if (self.finished\_late(task)).

**Methods declared on this owner** [completed date](operations-010.md#op-04d756e1180838), [can be late](operations-010.md#op-8a23309eb310bd), [finished late](operations-010.md#op-975105b1bebb7e).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L195) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L310) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1320)

<a id="op-5e0bc4f6c4538b"></a>
### Project Overview.needs attention

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_needs_attention`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“total” → len(flagged), “tasks” → list of self.attention\_row(reason, task) for tuple(reason, task) drawn from flagged at slice no value to ATTENTION\_LIMIT, “due\_soon\_days” → DUE\_SOON\_DAYS).

**Local steps**

- Set reasons from mapping of task.name → self.attention\_reason(task) for task drawn from self.open\_tasks.
  - Draw task from self.open\_tasks.
- Set flagged from sorted(generator of tuple(reasons at task.name, task) for task drawn from self.open\_tasks where reasons at task.name, key = deferred anonymous expression).
  - Draw task from self.open\_tasks, keep a combination only if (reasons at task.name).
- Return mapping(“total” → len(flagged), “tasks” → list of self.attention\_row(reason, task) for tuple(reason, task) drawn from flagged at slice no value to ATTENTION\_LIMIT, “due\_soon\_days” → DUE\_SOON\_DAYS).
  - Draw tuple(reason, task) from flagged at slice no value to ATTENTION\_LIMIT.

**Methods declared on this owner** [attention reason](operations-009.md#op-204ea6cee01f76), [attention row](operations-009.md#op-7248e0affbc08e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L205) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L320) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1330)

<a id="op-dd78ebffe8401b"></a>
### Project Overview.loose ends

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_loose_ends`

**Inputs** self.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · mapping(“total” → len(tasks), “tasks” → list of self.attention\_row(self.workflow\_status(task), task) for task drawn from tasks at slice no value to ATTENTION\_LIMIT).

**Local steps**

- If not self.is\_closed.
  - Return no value.
- Set tasks from sorted(self.open\_tasks, key = deferred anonymous expression).
- Return mapping(“total” → len(tasks), “tasks” → list of self.attention\_row(self.workflow\_status(task), task) for task drawn from tasks at slice no value to ATTENTION\_LIMIT).
  - Draw task from tasks at slice no value to ATTENTION\_LIMIT.

**Methods declared on this owner** [attention row](operations-009.md#op-7248e0affbc08e), [workflow status](operations-009.md#op-1c53300a403fc0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L202) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L317) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1327)

<a id="op-8a03a5f73efaa8"></a>
### Project Overview.milestone details

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_milestone_details`

**Inputs** self, task.

**Declared result** dict.

**Explicit results** mapping(“task” → task.name, “subject” → task.subject, “due\_date” → task.due\_date, “days\_left” → date\_diff(task.due\_date, self.today) when task.due\_date, otherwise no value).

**Local steps**

- Return mapping(“task” → task.name, “subject” → task.subject, “due\_date” → task.due\_date, “days\_left” → date\_diff(task.due\_date, self.today) when task.due\_date, otherwise no value).
  - Value choice on task.due\_date — true gives date\_diff(task.due\_date, self.today), false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L204) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L319) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1329)

<a id="op-1b3961df951111"></a>
### Project Overview.open task stats

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_open_task_stats`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“count” → len(self.open\_tasks), “due\_soon” → sum(generator of 1 for task drawn from self.open\_tasks where self.is\_due\_soon(task)), “due\_soon\_days” → DUE\_SOON\_DAYS).

**Local steps**

- Return mapping(“count” → len(self.open\_tasks), “due\_soon” → sum(generator of 1 for task drawn from self.open\_tasks where self.is\_due\_soon(task)), “due\_soon\_days” → DUE\_SOON\_DAYS).
  - Draw task from self.open\_tasks, keep a combination only if (self.is\_due\_soon(task)).

**Methods declared on this owner** [is due soon](operations-009.md#op-2aab3370adc38d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L207) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L322) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1332)

<a id="op-fbdaea5ae7d188"></a>
### Project Overview.overdue stats

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_overdue_stats`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“count” → len(overdue), “oldest\_days\_late” → max(generator of self.days\_late(task) for task drawn from overdue, default = 0), “tasks” → list of task.name for task drawn from overdue).

**Local steps**

- Set overdue from list of task for task drawn from self.open\_tasks where self.is\_overdue(task).
  - Draw task from self.open\_tasks, keep a combination only if (self.is\_overdue(task)).
- Return mapping(“count” → len(overdue), “oldest\_days\_late” → max(generator of self.days\_late(task) for task drawn from overdue, default = 0), “tasks” → list of task.name for task drawn from overdue).
  - Draw task from overdue.
  - Draw task from overdue.

**Methods declared on this owner** [is overdue](operations-009.md#op-721e05b2c9617b), [days late](operations-010.md#op-4885ce69337f26).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L209) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L324) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1334)

<a id="op-ad6830ff159a6a"></a>
### Project Overview.hours stats

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_hours_stats`

**Inputs** self.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · mapping(“logged” → flt(self.project.actual\_time), “expected” → expected).

**Local steps**

- If “actual\_time” belongs to self.hidden\_fields.
  - Return no value.
- Set expected from sum(generator of flt(task.expected\_time) for task drawn from self.tasks where (task.status differs from “Cancelled” and not task.is\_group)).
  - Draw task from self.tasks, keep a combination only if ((task.status differs from “Cancelled” and not task.is\_group)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in task.status differs from “Cancelled” → not task.is\_group.
- Return mapping(“logged” → flt(self.project.actual\_time), “expected” → expected).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L197) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L312) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1322)

<a id="op-204ea6cee01f76"></a>
### Project Overview.attention reason

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_attention_reason`

**Inputs** self, task.

**Declared result** (str bitwise or no value).

**Explicit results** “Overdue” · “Blocked” · “Unassigned” · “Due Soon” · no value.

**Local steps**

- If self.is\_overdue(task).
  - Return “Overdue”.
- If task.name belongs to self.blocked\_tasks.
  - Return “Blocked”.
- If (not task.assigned\_to and not task.is\_group).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not task.assigned\_to → not task.is\_group.
  - Return “Unassigned”.
- If self.is\_due\_soon(task).
  - Return “Due Soon”.
- Return no value.

**Methods declared on this owner** [is overdue](operations-009.md#op-721e05b2c9617b), [is due soon](operations-009.md#op-2aab3370adc38d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L187) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L302) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1312)

<a id="op-7248e0affbc08e"></a>
### Project Overview.attention row

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_attention_row`

**Inputs** self, reason, task.

**Declared result** dict.

**Explicit results** mapping(“task” → task.name, “subject” → task.subject, “reason” → reason, “assigned\_to” → task.assigned\_to, …).

**Local steps**

- Return mapping(“task” → task.name, “subject” → task.subject, “reason” → reason, “assigned\_to” → task.assigned\_to, …).
  - Value choice on self.is\_overdue(task) — true gives self.days\_late(task), false gives 0.

**Methods declared on this owner** [is overdue](operations-009.md#op-721e05b2c9617b), [days late](operations-010.md#op-4885ce69337f26).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L303) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1313)

<a id="op-650ca7af670169"></a>
### Project Overview.open status

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_open_status`

**Inputs** self, task.

**Declared result** str.

**Explicit results** “Overdue” when self.is\_overdue(task), otherwise self.workflow\_status(task).

**Local steps**

- Return “Overdue” when self.is\_overdue(task), otherwise self.workflow\_status(task).
  - Value choice on self.is\_overdue(task) — true gives “Overdue”, false gives self.workflow\_status(task).

**Methods declared on this owner** [is overdue](operations-009.md#op-721e05b2c9617b), [workflow status](operations-009.md#op-1c53300a403fc0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L206) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L321) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1331)

<a id="op-1c53300a403fc0"></a>
### Project Overview.workflow status

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_workflow_status`

**Inputs** self, task.

**Declared result** str.

**Explicit results** “Open” when task.status equals “Overdue”, otherwise task.status.

**Local steps**

- Return “Open” when task.status equals “Overdue”, otherwise task.status.
  - Value choice on task.status equals “Overdue” — true gives “Open”, false gives task.status.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L219) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1344)

<a id="op-e85cbfe65b1161"></a>
### Project Overview.priority rank

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_priority_rank`

**Inputs** self, task.

**Declared result** int.

**Explicit results** TASK\_PRIORITIES.index(task.priority) · len(TASK\_PRIORITIES).

**Local steps**

- If task.priority belongs to TASK\_PRIORITIES.
  - Return TASK\_PRIORITIES.index(task.priority).
- Return len(TASK\_PRIORITIES).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L211) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1336)

<a id="op-721e05b2c9617b"></a>
### Project Overview.is overdue

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_is_overdue`

**Inputs** self, task.

**Declared result** bool.

**Explicit results** false · not (awaiting\_review and getdate(task.review\_date) &gt; self.today).

**Local steps**

- If (not task.due\_date or task.due\_date ≥ self.today).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not task.due\_date → task.due\_date ≥ self.today.
  - Return false.
- Set awaiting\_review from (task.status equals “Pending Review” and task.review\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in task.status equals “Pending Review” → task.review\_date.
- Return not (awaiting\_review and getdate(task.review\_date) &gt; self.today).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in awaiting\_review → getdate(task.review\_date) &gt; self.today.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L201) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L316) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1326)

<a id="op-2aab3370adc38d"></a>
### Project Overview.is due soon

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_is_due_soon`

**Inputs** self, task.

**Declared result** bool.

**Explicit results** (bool(task.due\_date) and self.today ≤ task.due\_date ≤ self.due\_soon\_until).

**Local steps**

- Return (bool(task.due\_date) and self.today ≤ task.due\_date ≤ self.due\_soon\_until).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(task.due\_date) → self.today ≤ task.due\_date ≤ self.due\_soon\_until.
  - Compare adjacent operands in order, stopping at the first false comparison in self.today ≤ task.due\_date ≤ self.due\_soon\_until.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L200) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L315) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1325)

<a id="op-9876f463052ce7"></a>
### Project Overview.is closed

`operation_enterprise_binding_enterprise_projects_doctype_project_project_overview_projectoverview_is_closed`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** bool.

**Explicit results** self.project.status belongs to CLOSED\_STATUSES.

**Local steps**

- Return self.project.status belongs to CLOSED\_STATUSES.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L199) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L314) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1324)
