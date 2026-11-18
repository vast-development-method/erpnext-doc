# Projects and time · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Task

[Record definition](../../../../data/record-types/task.json)

<a id="op-250d61ff8b684a"></a>
### Task.validate project access

`operation_enterprise_binding_enterprise_projects_doctype_task_task_task_validate_project_access`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.has\_value\_changed(“project”).
  - Set projects from list(self.get\_value\_before\_save(“project”)).
  - If not Platform.flags.in\_web\_form.
    - Evaluate projects.append(self.project).
- Otherwise.
  - If any(generator of self.has\_value\_changed(fieldname) for fieldname drawn from tuple(“status”, “progress”, “task\_weight”)).
    - Draw fieldname from tuple(“status”, “progress”, “task\_weight”).
    - Set projects from list(self.project).
  - Otherwise.
    - Return no value.
- If Platform.flags.in\_web\_form.
  - Evaluate self.check\_project\_access(expanded projects, allow\_project\_users = true).
- Otherwise.
  - If not self.flags.ignore\_permissions.
    - Evaluate self.check\_project\_access(expanded projects).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check project access](operations-013.md#op-3927c11d300f6f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L242) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1367)

<a id="op-3927c11d300f6f"></a>
### Task.check project access

`operation_enterprise_binding_enterprise_projects_doctype_task_task_task_check_project_access`

**Inputs** self, remaining positional values projects, allow\_project\_users (named only, default false).

**Local steps**

- For each project in set of project for project drawn from projects where project.
  - Draw project from projects, keep a combination only if (project).
  - If not (allow\_project\_users and self.has\_webform\_permission(project)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in allow\_project\_users → self.has\_webform\_permission(project).
    - Evaluate require\_permission(“Project”, project, “select”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has webform permission](operations-013.md#op-79be61d4a38561).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L231) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1356)

<a id="op-617a884b87b94b"></a>
### Task.validate children project

`operation_enterprise_binding_enterprise_projects_doctype_task_task_task_validate_children_project`

**Inputs** self.

**Record and data access** read “Task” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Task {0} has child tasks in another project. Move them out of this group first.”.format(get\_link\_to\_form(“Task”, self.name)).

**Local steps**

- If (self.is\_new() or not self.has\_value\_changed(“project”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.has\_value\_changed(“project”).
  - Return no value.
- Set child\_projects from Platform.get\_all(“Task”, filters = mapping(“parent\_task” → self.name), pluck = “project”, distinct = true).
- If any(generator of (project or no value) differs from (self.project or no value) for project drawn from child\_projects).
  - Draw project from child\_projects.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in project → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.project → no value.
  - Call the validation error handler Platform.throw(translated “Task {0} has child tasks in another project. Move them out of this group first.”.format(get\_link\_to\_form(“Task”, self.name)), title = translated “Invalid Project”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L239) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1364)

<a id="op-6a700f8b5fbc39"></a>
### Task.validate parent not completed

`operation_enterprise_binding_enterprise_projects_doctype_task_task_task_validate_parent_not_completed`

**Inputs** self.

**Record and data access** read “Task” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot add an open task under completed Parent Task {0}.”.format(get\_link\_to\_form(“Task”, self.parent\_task)).

**Local steps**

- If (not self.parent\_task or self.status belongs to tuple(“Completed”, “Cancelled”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.parent\_task → self.status belongs to tuple(“Completed”, “Cancelled”).
  - Return no value.
- If (self.has\_value\_changed(“parent\_task”) and Platform.db.get\_value(“Task”, self.parent\_task, “status”) equals “Completed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_value\_changed(“parent\_task”) → Platform.db.get\_value(“Task”, self.parent\_task, “status”) equals “Completed”.
  - Call the validation error handler Platform.throw(translated “Cannot add an open task under completed Parent Task {0}.”.format(get\_link\_to\_form(“Task”, self.parent\_task))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L240) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1365)

<a id="op-6d000a14df5b92"></a>
### Task.update depends on

`operation_enterprise_projects_record_definitions_task_business_behavior_task_update_depends_on`

**Inputs** self.

**Local steps**

- Set depends\_on\_tasks from empty text.
- For each d in self.depends\_on.
  - If (d.task and d.task does not belong to depends\_on\_tasks).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.task → d.task does not belong to depends\_on\_tasks.
    - Update depends\_on\_tasks using + (d.task + “,”).
- Set self.depends\_on\_tasks from depends\_on\_tasks.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0605.json#L2107) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L759)

<a id="op-e6e8a8c71369b5"></a>
### Task.update nsm model

`operation_enterprise_projects_record_definitions_task_business_behavior_task_update_nested_set_model_model`

**Inputs** self.

**Local steps**

- Evaluate Platform.utils.nestedset.update\_nsm(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0605.json#L2250) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L760)

<a id="op-c29781a680451d"></a>
### Task.on update

`operation_enterprise_projects_record_definitions_task_business_behavior_task_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.update\_nsm\_model().
- Evaluate self.check\_recursion().
- Evaluate self.remove\_from\_previous\_parent\_depends\_on().
- Evaluate self.reschedule\_dependent\_tasks().
- Evaluate self.update\_project().
- Evaluate self.update\_previous\_project().
- Evaluate self.unassign\_todo().
- Evaluate self.populate\_depends\_on().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update nsm model](operations-013.md#op-e6e8a8c71369b5), [check recursion](operations-013.md#op-90ee7106098abd), [remove from previous parent depends on](operations-013.md#op-7e88e2bf7aff9f), [reschedule dependent tasks](operations-013.md#op-55b4fc3c86265d), [update project](operations-013.md#op-d0884ad73ba398), [update previous project](operations-013.md#op-7698913e0933ae), [unassign todo](operations-013.md#op-ec4031dc384a02), [populate depends on](operations-013.md#op-4d9c35465fa36e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1299) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L754)

<a id="op-ec4031dc384a02"></a>
### Task.unassign todo

`operation_enterprise_projects_record_definitions_task_business_behavior_task_unassign_todo`

**Inputs** self.

**Local steps**

- If self.status equals “Completed”.
  - Evaluate close\_all\_assignments(self.doctype, self.name, ignore\_permissions = true).
- If self.status equals “Cancelled”.
  - Evaluate clear(self.doctype, self.name, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1304) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L758)

<a id="op-eb699d7fac7e2e"></a>
### Task.update time and costing

`operation_enterprise_projects_record_definitions_task_business_behavior_task_update_time_and_costing`

**Inputs** self.

**Local steps**

- Set TimesheetDetail from Platform.qb.DocType(“Timesheet Detail”).
- Set tl from nested operand in the contract.select(nested operand in the contract(nested operand in the contract), nested operand in the contract(nested operand in the contract), nested operand in the contract(nested o … at 0.
- Set self.total\_costing\_amount from tl.base\_costing\_amount.
- Set self.total\_billing\_amount from tl.base\_billing\_amount.
- Set self.actual\_time from tl.time.
- Set self.act\_start\_date from tl.start\_date.
- Set self.act\_end\_date from tl.end\_date.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0605.json#L2618) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L763)

<a id="op-d0884ad73ba398"></a>
### Task.update project

`operation_enterprise_projects_record_definitions_task_business_behavior_task_update_project`

**Inputs** self.

**Record and data access** resolve a document from “Project” via get\_cached\_doc.

**Local steps**

- If (self.project and not self.flags.from\_project).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.project → not self.flags.from\_project.
  - Evaluate Platform.get\_cached\_doc(“Project”, self.project).update\_project().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Project”, self.project).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0605.json#L3204) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L761)

<a id="op-7698913e0933ae"></a>
### Task.update previous project

`operation_enterprise_binding_enterprise_projects_doctype_task_task_task_update_previous_project`

**Inputs** self.

**Record and data access** resolve a document from “Project” via get\_cached\_doc.

**Local steps**

- Set previous\_project from self.get\_value\_before\_save(“project”).
- If (previous\_project and previous\_project differs from self.project).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_project → previous\_project differs from self.project.
  - Evaluate Platform.get\_cached\_doc(“Project”, previous\_project).update\_project().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Project”, previous\_project).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L238) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1363)

<a id="op-90ee7106098abd"></a>
### Task.check recursion

`operation_enterprise_projects_record_definitions_task_business_behavior_task_check_recursion`

**Inputs** self.

**Record and data access** execute query text (SELECT, Task Depends).format(d at 0, d at 1, “%s”).

**Explicit results** no value.

**Explicit failure paths** validation helper with CircularReferenceError — translated “Circular Reference Error”.

**Local steps**

- If self.flags.ignore\_recursion\_check.
  - Return no value.
- Set check\_list from list(list(“task”, “parent”), list(“parent”, “task”)).
- For each d in check\_list.
  - Set tuple(task\_list, count) from tuple(list(self.name), 0).
  - While len(task\_list) &gt; count.
    - Set tasks from Platform.db.sql(query text (SELECT, Task Depends).format(d at 0, d at 1, “%s”), cstr(task\_list at count)).
    - Set count from (count + 1).
    - For each b in tasks.
      - If b at 0 equals self.name.
        - Call the validation error handler Platform.throw(translated “Circular Reference Error”, CircularReferenceError).
      - If b at 0.
        - Evaluate task\_list.append(b at 0).
    - <a id="op-90ee7106098abd-guard-19"></a>If count equals 15.
      - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison count equals 15, count = 15 selects the branch that exits the enclosing loop. With count = 16, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-90ee7106098abd-guard-19)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L750)

<a id="op-55b4fc3c86265d"></a>
### Task.reschedule dependent tasks

`operation_enterprise_projects_record_definitions_task_business_behavior_task_reschedule_dependent_tasks`

**Inputs** self.

**Record and data access** read “Task Depends On” via get\_all · read “Task” via get\_all · resolve a document from “Task” via get\_doc.

**State and service calls** call save on task.

**Explicit results** no value.

**Local steps**

- Set end\_date from (self.exp\_end\_date or self.act\_end\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.exp\_end\_date → self.act\_end\_date.
- If (not end\_date or self.flags.ignore\_reschedule).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not end\_date → self.flags.ignore\_reschedule.
  - Return no value.
- Set dependent\_parents from Platform.get\_all(“Task Depends On”, filters = mapping(“task” → self.name, “parent” → list(“!=”, (self.parent\_task or empty text))), pluck = “parent”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.parent\_task → empty text.
- If not dependent\_parents.
  - Return no value.
- For each task\_name in Platform.get\_all(“Task”, filters = mapping(“project” → self.project, “name” → list(“in”, dependent\_parents)), pluck = “name”).
  - Set task from Platform.get\_doc(“Task”, task\_name).
  - If (task.exp\_start\_date and task.exp\_end\_date and task.exp\_start\_date &lt; get\_datetime(end\_date) and task.status belongs to tuple(“Open”, “Working”, “Overdue”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in task.exp\_start\_date → task.exp\_end\_date → task.exp\_start\_date &lt; get\_datetime(end\_date) → task.status belongs to tuple(“Open”, “Working”, “Overdue”).
    - Set task\_duration from date\_diff(task.exp\_end\_date, task.exp\_start\_date).
    - Set task.exp\_start\_date from add\_days(end\_date, 1).
    - Set task.exp\_end\_date from add\_days(task.exp\_start\_date, task\_duration).
    - Set task.flags.ignore\_recursion\_check from true.
    - Set task.flags.rescheduled from true.
    - Evaluate task.save(ignore\_permissions = self.flags.ignore\_permissions).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1302) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L756)

<a id="op-79be61d4a38561"></a>
### Task.has webform permission

`operation_enterprise_projects_record_definitions_task_business_behavior_task_has_webform_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, project.

**Explicit result forms** Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L752)

<a id="op-2470a98313d2eb"></a>
### Task.validate web form project permission

`operation_enterprise_projects_record_definitions_task_business_behavior_task_validate_web_form_project_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0605.json#L4737) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1321) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L775)

<a id="op-4d9c35465fa36e"></a>
### Task.populate depends on

`operation_enterprise_projects_record_definitions_task_business_behavior_task_populate_depends_on`

**Inputs** self.

**Record and data access** resolve a document from “Task” via get\_doc.

**State and service calls** call save on parent.

**Local steps**

- If self.parent\_task.
  - Set parent from Platform.get\_doc(“Task”, self.parent\_task).
  - If self.name does not belong to list of row.task for row drawn from parent.depends\_on.
    - Draw row from parent.depends\_on.
    - Evaluate parent.append(“depends\_on”, mapping(“doctype” → “Task Depends On”, “task” → self.name, “subject” → self.subject)).
    - Evaluate parent.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0605.json#L5029) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1300) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L755)

<a id="op-7e88e2bf7aff9f"></a>
### Task.remove from previous parent depends on

`operation_enterprise_binding_enterprise_projects_doctype_task_task_task_remove_from_previous_parent_depends_on`

**Inputs** self.

**Local steps**

- Set previous\_parent from self.get\_value\_before\_save(“parent\_task”).
- If previous\_parent differs from self.parent\_task.
  - Evaluate self.remove\_from\_parent\_depends\_on(previous\_parent).

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove from parent depends on](operations-013.md#op-407385baaa6f5a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L235) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1360)

<a id="op-407385baaa6f5a"></a>
### Task.remove from parent depends on

`operation_enterprise_binding_enterprise_projects_doctype_task_task_task_remove_from_parent_depends_on`

**Inputs** self, parent\_task.

**Record and data access** resolve a document from “Task” via get\_doc.

**State and service calls** call save on parent.

**Explicit results** no value.

**Local steps**

- If not parent\_task.
  - Return no value.
- Set parent from Platform.get\_doc(“Task”, parent\_task).
- Set rows from list of row for row drawn from parent.depends\_on where row.task differs from self.name.
  - Draw row from parent.depends\_on, keep a combination only if (row.task differs from self.name).
- If len(rows) differs from len(parent.depends\_on).
  - Evaluate parent.set(“depends\_on”, rows).
  - Evaluate parent.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L234) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1359)

<a id="op-858aa91c28235c"></a>
### Task.on trash

`operation_enterprise_projects_record_definitions_task_business_behavior_task_on_trash`

**Inputs** self.

**Record and data access** read “Task” via exists.

**Local steps**

- If Platform.db.exists(“Task”, mapping(“parent\_task” → self.name)).
  - Evaluate throw(translated “Child Task exists for this Task. You can not delete this Task.”).
- Evaluate self.check\_project\_access(self.project, allow\_project\_users = true).
- Evaluate self.remove\_from\_parent\_depends\_on(self.parent\_task).
- Evaluate self.update\_nsm\_model().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check project access](operations-013.md#op-3927c11d300f6f), [remove from parent depends on](operations-013.md#op-407385baaa6f5a), [update nsm model](operations-013.md#op-e6e8a8c71369b5).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L753)

<a id="op-ecbdc31d714246"></a>
### Task.after delete

`operation_enterprise_projects_record_definitions_task_business_behavior_task_after_delete`

**Inputs** self.

**Local steps**

- Evaluate self.update\_project().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update project](operations-013.md#op-d0884ad73ba398).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0605.json#L5400) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1294) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L749)

<a id="op-abfab3dcdf8147"></a>
### Task.is overdue

`operation_enterprise_binding_enterprise_projects_doctype_task_task_task_is_overdue`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** bool.

**Explicit results** (bool(self.exp\_end\_date) and getdate(self.exp\_end\_date) &lt; getdate()).

**Local steps**

- Return (bool(self.exp\_end\_date) and getdate(self.exp\_end\_date) &lt; getdate()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(self.exp\_end\_date) → getdate(self.exp\_end\_date) &lt; getdate().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L233) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1358)

<a id="op-39c6d10acabb00"></a>
### Task.update status

`operation_enterprise_projects_record_definitions_task_business_behavior_task_update_status`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- If (self.status does not belong to tuple(“Cancelled”, “Completed”) and self.is\_overdue).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status does not belong to tuple(“Cancelled”, “Completed”) → self.is\_overdue.
  - Evaluate self.db\_set(“status”, “Overdue”, update\_modified = false).
  - Evaluate self.update\_project().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update project](operations-013.md#op-d0884ad73ba398).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L762)

<a id="op-e372ce72401345"></a>
### Check if child exists

`operation_enterprise_projects_record_definitions_task_business_behavior_check_if_child_exists`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Task” via get\_doc · read “Task” via get\_all.

**Explicit results** child\_tasks.

**Local steps**

- Evaluate Platform.get\_doc(“Task”, name).check\_permission(“read”).
- Set child\_tasks from Platform.get\_all(“Task”, filters = mapping(“parent\_task” → name)).
- Set child\_tasks from list of get\_link\_to\_form(“Task”, task.name) for task drawn from child\_tasks.
  - Draw task from child\_tasks.
- Return child\_tasks.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1286) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L741)

<a id="op-68735347e03b73"></a>
### Get project

`operation_enterprise_projects_record_definitions_task_business_behavior_get_project`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**State and service calls** execute a supplied database query.

**Explicit results** Platform.db.sql(formatted text  select name {search\_columns} from ′tabProject′  where %(key)s like %(txt)s  %(mcond)s  {search\_cond}  order by name  limit %(page\_len)s offset, mapping(“key” → search ….

**Local steps**

- Bind dependencies get\_match\_cond.
- Set meta from Platform.get\_meta(doctype).
- Set searchfields from meta.get\_search\_fields().
- Set search\_columns from (“, ” + “, ”.join(searchfields)) when searchfields, otherwise empty text.
  - Value choice on searchfields — true gives (“, ” + “, ”.join(searchfields)), false gives empty text.
- Set search\_cond from (“ or ” + “ or ”.join(generator of (field + “ like %(txt)s”) for field drawn from searchfields)).
  - Draw field from searchfields.
- Return Platform.db.sql(formatted text  select name {search\_columns} from ′tabProject′  where %(key)s like %(txt)s  %(mcond)s  {search\_cond}  order by name  limit %(page\_len)s offset, mapping(“key” → search ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1288) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L743)
