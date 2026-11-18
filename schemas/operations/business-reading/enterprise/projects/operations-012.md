# Projects and time · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Project wise stock tracking

<a id="op-7e210926d940ba"></a>
### Execute

`operation_enterprise_projects_report_project_wise_stock_tracking_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_columns().
- Set proj\_details from get\_project\_details().
- Set pr\_item\_map from get\_purchased\_items\_cost().
- Set se\_item\_map from get\_issued\_items\_cost().
- Set dn\_item\_map from get\_delivered\_items\_cost().
- Set data from list().
- For each project in proj\_details.
  - Evaluate data.append(list(project.name, pr\_item\_map.get(project.name, 0), se\_item\_map.get(project.name, 0), dn\_item\_map.get(project.name, 0), …)).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0611.json#L6010) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1427) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L864)

<a id="op-3bb62cbcb3d721"></a>
### Get columns

`operation_enterprise_projects_report_project_wise_stock_tracking_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list((translated “Project Id” + “:Link/Project:140”), (translated “Cost of Purchased Items” + “:Currency:160”), (translated “Cost of Issued Items” + “:Currency:160”), (translated “Cost of Delivered Items”  ….

**Local steps**

- Return list((translated “Project Id” + “:Link/Project:140”), (translated “Cost of Purchased Items” + “:Currency:160”), (translated “Cost of Issued Items” + “:Currency:160”), (translated “Cost of Delivered Items”  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0611.json#L6379) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L865)

<a id="op-b663105e161b16"></a>
### Get project details

`operation_enterprise_projects_report_project_wise_stock_tracking_business_behavior_get_project_details`

**Inputs** no declared parameters.

**Record and data access** read “Project” via get\_all.

**Explicit results** Platform.get\_all(“Project”, filters = mapping(“docstatus” → list(“&lt;”, 2)), fields = list(“name”, “project\_name”, “status”, “company”, …)).

**Local steps**

- Return Platform.get\_all(“Project”, filters = mapping(“docstatus” → list(“&lt;”, 2)), fields = list(“name”, “project\_name”, “status”, “company”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0611.json#L6696) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L868)

<a id="op-bd19f9bd1666f9"></a>
### Get purchased items cost

`operation_enterprise_projects_report_project_wise_stock_tracking_business_behavior_get_purchased_items_cost`

**Inputs** no declared parameters.

**Record and data access** read “Purchase Receipt Item” via get\_all.

**Explicit results** sum\_amount\_by\_project((pr\_items + pi\_items)).

**Local steps**

- Set pr\_items from Platform.get\_all(“Purchase Receipt Item”, filters = mapping(“project” → list(“is”, “set”), “docstatus” → 1), fields = list(“project”, mapping(“SUM” → “base\_net\_amount”, “as” → “amount”)), group\_by = “project”).
- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set pi\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set pi\_items from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
- Return sum\_amount\_by\_project((pr\_items + pi\_items)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L869)

<a id="op-b44d49774ac9bc"></a>
### Get issued items cost

`operation_enterprise_projects_report_project_wise_stock_tracking_business_behavior_get_issued_items_cost`

**Inputs** no declared parameters.

**Explicit results** se\_item\_map.

**Local steps**

- Set se from Platform.qb.DocType(“Stock Entry”).
- Set se\_item from Platform.qb.DocType(“Stock Entry Detail”).
- Set project from Coalesce(NullIf(se\_item.project, empty text), se.project).
- Set se\_items from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
- Set se\_item\_map from mapping().
- For each item in se\_items.
  - Evaluate se\_item\_map.setdefault(item.project, item.amount).
- Return se\_item\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L867)

<a id="op-eede39a0dc3441"></a>
### Get delivered items cost

`operation_enterprise_projects_report_project_wise_stock_tracking_business_behavior_get_delivered_items_cost`

**Inputs** no declared parameters.

**Explicit results** dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(project).run()).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set dn\_item from Platform.qb.DocType(“Delivery Note Item”).
- Set si\_item from Platform.qb.DocType(“Sales Invoice Item”).
- Set project from Coalesce(NullIf(dn\_item.project, empty text), NullIf(si\_item.project, empty text), sle.project).
- Return dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(project).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L866)

<a id="op-10af45708e24fc"></a>
### Sum amount by project

`operation_enterprise_binding_enterprise_projects_report_project_wise_stock_tracking_project_wise_stock_tracking_sum_amount_by_project`

**Inputs** rows.

**Explicit results** amounts.

**Local steps**

- Set amounts from mapping().
- For each row in rows.
  - Set amounts at row.project from (amounts.get(row.project, 0) + row.amount).
- Return amounts.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L254) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1379)

## Record · Task

[Record definition](../../../../data/record-types/task.json)

<a id="op-82884036737dd8"></a>
### Task.get customer details

`operation_enterprise_projects_record_definitions_task_business_behavior_task_get_customer_details`

**Inputs** self.

**Record and data access** execute query text (SELECT, Customer).

**Explicit results** ret.

**Local steps**

- Set cust from Platform.db.sql(query text (SELECT, Customer), self.customer).
- If cust.
  - Set ret from mapping(“customer\_name” → ((cust and cust at 0 at 0) or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (cust and cust at 0 at 0) → empty text.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cust → cust at 0 at 0.
  - Return ret.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L751)

<a id="op-fb053d2600b1ea"></a>
### Task.validate

`operation_enterprise_projects_record_definitions_task_business_behavior_task_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_parent\_project().
- Evaluate self.validate\_children\_project().
- Evaluate self.validate\_dates().
- Evaluate self.validate\_progress().
- Evaluate self.validate\_status().
- Evaluate self.clear\_completion\_on\_reopen().
- Evaluate self.update\_depends\_on().
- Evaluate self.validate\_dependencies\_for\_template\_task().
- Evaluate self.validate\_completed\_on().
- Evaluate self.set\_default\_end\_date\_if\_missing().
- Evaluate self.set\_default\_weight().
- Evaluate self.validate\_parent\_is\_group().
- Evaluate self.validate\_parent\_not\_completed().
- Evaluate self.validate\_web\_form\_project\_permission().
- Evaluate self.validate\_project\_access().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate parent project](operations-012.md#op-e14ed65b745aa9), [validate children project](operations-013.md#op-617a884b87b94b), [validate dates](operations-012.md#op-d2018b5d33f97f), [validate progress](operations-012.md#op-2b8e3f23e5c5d2), [validate status](operations-012.md#op-b668e1a78e5c9e), [clear completion on reopen](operations-012.md#op-5641c3e4ec50d9), [update depends on](operations-013.md#op-6d000a14df5b92), [validate dependencies for template task](operations-012.md#op-ff142c2e6aa08b), [validate completed on](operations-012.md#op-e2e5a75058674b), [set default end date if missing](operations-012.md#op-8e885070f08a67), [set default weight](operations-012.md#op-f0b4d01b39c91d), [validate parent is group](operations-012.md#op-d9139ac50101c5), [validate parent not completed](operations-013.md#op-6a700f8b5fbc39), [validate web form project permission](operations-013.md#op-2470a98313d2eb), [validate project access](operations-013.md#op-250d61ff8b684a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1310) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L764)

<a id="op-d2018b5d33f97f"></a>
### Task.validate dates

`operation_enterprise_projects_record_definitions_task_business_behavior_task_validate_dates`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_from\_to\_dates(“exp\_start\_date”, “exp\_end\_date”).
- Evaluate self.validate\_from\_to\_dates(“act\_start\_date”, “act\_end\_date”).
- Evaluate self.validate\_parent\_expected\_end\_date().
- Evaluate self.validate\_parent\_project\_dates().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate parent expected end date](operations-012.md#op-0e8eb36f522c0f), [validate parent project dates](operations-012.md#op-c6ea31b0833121).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0604.json#L5886) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1312) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L766)

<a id="op-f0b4d01b39c91d"></a>
### Task.set default weight

`operation_enterprise_binding_enterprise_projects_doctype_task_task_task_set_default_weight`

**Inputs** self.

**Record and data access** read “Task Type” via get\_cached\_value.

**Local steps**

- Set type\_changed\_alone from (self.has\_value\_changed(“type”) and not self.has\_value\_changed(“task\_weight”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_value\_changed(“type”) → not self.has\_value\_changed(“task\_weight”).
- If (self.type and (self.task\_weight is identical to no value or type\_changed\_alone)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.type → (self.task\_weight is identical to no value or type\_changed\_alone).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.task\_weight is identical to no value → type\_changed\_alone.
  - Set self.task\_weight from Platform.get\_cached\_value(“Task Type”, self.type, “weight”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Task Type”, self.type, “weight”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L237) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1362)

<a id="op-8e885070f08a67"></a>
### Task.set default end date if missing

`operation_enterprise_projects_record_definitions_task_business_behavior_task_set_default_end_date_if_missing`

**Inputs** self.

**Local steps**

- If (self.exp\_start\_date and self.expected\_time and not self.exp\_end\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.exp\_start\_date → self.expected\_time → not self.exp\_end\_date.
  - Set self.exp\_end\_date from add\_to\_date(self.exp\_start\_date, hours = self.expected\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0604.json#L6031) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1303) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L757)

<a id="op-0e8eb36f522c0f"></a>
### Task.validate parent expected end date

`operation_enterprise_projects_record_definitions_task_business_behavior_task_validate_parent_expected_end_date`

**Inputs** self.

**Record and data access** read “Task” via get\_value.

**Explicit results** no value.

**Local steps**

- If (not self.parent\_task or not self.exp\_end\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.parent\_task → not self.exp\_end\_date.
  - Return no value.
- Set parent\_exp\_end\_date from Platform.db.get\_value(“Task”, self.parent\_task, “exp\_end\_date”).
- If not parent\_exp\_end\_date.
  - Return no value.
- If getdate(self.exp\_end\_date) &gt; getdate(parent\_exp\_end\_date).
  - Evaluate self.report\_date\_conflict(translated “Expected End Date should be less than or equal to parent task's Expected End Date {0}.”.format(format\_date(parent\_exp\_end\_date)), “exp\_end\_date”, “parent\_task”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [report date conflict](operations-012.md#op-1e84127ec03e29).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1315) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L769)

<a id="op-c6ea31b0833121"></a>
### Task.validate parent project dates

`operation_enterprise_projects_record_definitions_task_business_behavior_task_validate_parent_project_dates`

**Inputs** self.

**Record and data access** read “Project” via get\_value.

**Explicit results** no value.

**Local steps**

- If (not self.project or Platform.in\_test).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.project → Platform.in\_test.
  - Return no value.
- Set tuple(project\_start\_date, project\_end\_date) from Platform.db.get\_value(“Project”, self.project, list(“expected\_start\_date”, “expected\_end\_date”)).
- For each fieldname in tuple(“exp\_start\_date”, “exp\_end\_date”).
  - Set task\_date from self.get(fieldname).
  - If not task\_date.
    - Continue with the next iteration or loop test.
  - Set task\_date from getdate(task\_date).
  - If (project\_end\_date and date\_diff(getdate(project\_end\_date), task\_date) &lt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in project\_end\_date → date\_diff(getdate(project\_end\_date), task\_date) &lt; 0.
    - Evaluate self.report\_date\_conflict(translated “{0}'s {1} cannot be after {2}'s Expected End Date.”.format(get\_link\_to\_form(“Task”, self.name), translated self.meta.get\_label(fieldname), get\_link\_to\_form(“Project”,  ….
  - If (project\_start\_date and date\_diff(task\_date, getdate(project\_start\_date)) &lt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in project\_start\_date → date\_diff(task\_date, getdate(project\_start\_date)) &lt; 0.
    - Evaluate self.report\_date\_conflict(translated “{0}'s {1} cannot be before {2}'s Expected Start Date.”.format(get\_link\_to\_form(“Task”, self.name), translated self.meta.get\_label(fieldname), get\_link\_to\_form(“Project ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [report date conflict](operations-012.md#op-1e84127ec03e29).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1317) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L771)

<a id="op-1e84127ec03e29"></a>
### Task.report date conflict

`operation_enterprise_binding_enterprise_projects_doctype_task_task_task_report_date_conflict`

**Inputs** self, message, remaining positional values fieldnames.

**State and service calls** msgprint with translated “{0} was moved after the task it depends on. {1}”.format(get\_link\_to\_form(“Task”, self.name), message).

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.exceptions.InvalidDates — message.

**Local steps**

- If not self.flags.rescheduled.
  - If (self.is\_new() or any(generator of self.has\_value\_changed(fieldname) for fieldname drawn from fieldnames)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → any(generator of self.has\_value\_changed(fieldname) for fieldname drawn from fieldnames).
    - Draw fieldname from fieldnames.
    - Call the validation error handler Platform.throw(message, Platform.exceptions.InvalidDates).
  - Return no value.
- Evaluate Platform.msgprint(translated “{0} was moved after the task it depends on. {1}”.format(get\_link\_to\_form(“Task”, self.name), message), title = translated “Schedule Conflict”, indicator = “orange”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L236) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1361)

<a id="op-b668e1a78e5c9e"></a>
### Task.validate status

`operation_enterprise_projects_record_definitions_task_business_behavior_task_validate_status`

**Inputs** self.

**Record and data access** read “Task” via get\_value.

**Explicit failure paths** validation helper — translated “Cannot complete task {0} as its dependant task {1} are not completed / cancelled.”.format(Platform.bold(self.name), Platform.bold(d.task)).

**Local steps**

- If (self.is\_template and self.status differs from “Template”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_template → self.status differs from “Template”.
  - Set self.status from “Template”.
- If (self.status equals “Template” and not self.is\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Template” → not self.is\_template.
  - Set self.status from “Open”.
- If (self.status equals “Overdue” and not self.is\_overdue).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Overdue” → not self.is\_overdue.
  - Set self.status from “Working” when self.actual\_time, otherwise “Open”.
    - Value choice on self.actual\_time — true gives “Working”, false gives “Open”.
- If (self.status differs from self.get\_db\_value(“status”) and self.status equals “Completed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status differs from self.get\_db\_value(“status”) → self.status equals “Completed”.
  - For each d in self.depends\_on.
    - If Platform.db.get\_value(“Task”, d.task, “status”) does not belong to tuple(“Completed”, “Cancelled”).
      - Call the validation error handler Platform.throw(translated “Cannot complete task {0} as its dependant task {1} are not completed / cancelled.”.format(Platform.bold(self.name), Platform.bold(d.task))).
  - If not self.completed\_on.
    - Set self.completed\_on from today().
  - Evaluate close\_all\_assignments(self.doctype, self.name, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1320) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L774)

<a id="op-2b8e3f23e5c5d2"></a>
### Task.validate progress

`operation_enterprise_projects_record_definitions_task_business_behavior_task_validate_progress`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Progress % for a task must be between 0 and 100.”.

**Local steps**

- If not 0 ≤ flt(self.progress) ≤ 100.
  - Compare adjacent operands in order, stopping at the first false comparison in 0 ≤ flt(self.progress) ≤ 100.
  - Call the validation error handler Platform.throw(translated “Progress % for a task must be between 0 and 100.”).
- <a id="op-2b8e3f23e5c5d2-guard-5"></a>If self.status equals “Completed”.
  - Set self.progress from 100.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Completed”, self.status = “Completed” selects the branch that assigns 100 to self.progress. With self.status = “Open”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-2b8e3f23e5c5d2-guard-5)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1319) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L773)

<a id="op-5641c3e4ec50d9"></a>
### Task.clear completion on reopen

`operation_enterprise_binding_enterprise_projects_doctype_task_task_task_clear_completion_on_reopen`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.get\_value\_before\_save(“status”) differs from “Completed” or self.status belongs to tuple(“Completed”, “Cancelled”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_value\_before\_save(“status”) differs from “Completed” → self.status belongs to tuple(“Completed”, “Cancelled”).
  - Return no value.
- Set self.completed\_on from no value.
- Set self.completed\_by from no value.
- If not self.has\_value\_changed(“progress”).
  - Set self.progress from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L232) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1357)

<a id="op-ff142c2e6aa08b"></a>
### Task.validate dependencies for template task

`operation_enterprise_projects_record_definitions_task_business_behavior_task_validate_dependencies_for_template_task`

**Inputs** self.

**Local steps**

- If self.is\_template.
  - Evaluate self.validate\_parent\_template\_task().
  - Evaluate self.validate\_depends\_on\_tasks().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate parent template task](operations-012.md#op-b48ea15e949f11), [validate depends on tasks](operations-012.md#op-904520b3f5c1b3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0605.json#L1315) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1313) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L767)

<a id="op-b48ea15e949f11"></a>
### Task.validate parent template task

`operation_enterprise_projects_record_definitions_task_business_behavior_task_validate_parent_template_task`

**Inputs** self.

**Record and data access** read “Task” via get\_value.

**Explicit failure paths** validation helper — translated “Parent Task {0} is not a Template Task”.format(get\_link\_to\_form(“Task”, self.parent\_task)).

**Local steps**

- If self.parent\_task.
  - If not Platform.db.get\_value(“Task”, self.parent\_task, “is\_template”).
    - Call the validation error handler Platform.throw(translated “Parent Task {0} is not a Template Task”.format(get\_link\_to\_form(“Task”, self.parent\_task))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0605.json#L1400) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L772)

<a id="op-904520b3f5c1b3"></a>
### Task.validate depends on tasks

`operation_enterprise_projects_record_definitions_task_business_behavior_task_validate_depends_on_tasks`

**Inputs** self.

**Record and data access** read “Task” via get\_value.

**Explicit failure paths** validation helper — translated “Dependent Task {0} is not a Template Task”.format(get\_link\_to\_form(“Task”, task.task)).

**Local steps**

- If self.depends\_on.
  - For each task in self.depends\_on.
    - If not Platform.db.get\_value(“Task”, task.task, “is\_template”).
      - Call the validation error handler Platform.throw(translated “Dependent Task {0} is not a Template Task”.format(get\_link\_to\_form(“Task”, task.task))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0605.json#L1584) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1314) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L768)

<a id="op-e2e5a75058674b"></a>
### Task.validate completed on

`operation_enterprise_projects_record_definitions_task_business_behavior_task_validate_completed_on`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Completed On cannot be greater than Today”.

**Local steps**

- If (self.completed\_on and getdate(self.completed\_on) &gt; getdate()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.completed\_on → getdate(self.completed\_on) &gt; getdate().
  - Call the validation error handler Platform.throw(translated “Completed On cannot be greater than Today”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0605.json#L1787) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1311) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L765)

<a id="op-d9139ac50101c5"></a>
### Task.validate parent is group

`operation_enterprise_projects_record_definitions_task_business_behavior_task_validate_parent_is_group`

**Inputs** self.

**Record and data access** read “Task” via get\_value.

**Explicit failure paths** validation helper with ParentIsGroupError — translated “Parent Task {0} must be a Group Task”.format(get\_link\_to\_form(“Task”, self.parent\_task)).

**Local steps**

- If self.parent\_task.
  - If not Platform.db.get\_value(“Task”, self.parent\_task, “is\_group”).
    - Call the validation error handler Platform.throw(translated “Parent Task {0} must be a Group Task”.format(get\_link\_to\_form(“Task”, self.parent\_task)), ParentIsGroupError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0605.json#L1919) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1316) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L770)

<a id="op-e14ed65b745aa9"></a>
### Task.validate parent project

`operation_enterprise_binding_enterprise_projects_doctype_task_task_task_validate_parent_project`

**Inputs** self.

**Record and data access** read “Task” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Parent Task {0} is not in Project {1}. Pick a group task of the same project.”.format(get\_link\_to\_form(“Task”, self.parent\_task), Platform.bold(self.project)).

**Local steps**

- If (not self.parent\_task or not (self.has\_value\_changed(“parent\_task”) or self.has\_value\_changed(“project”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.parent\_task → not (self.has\_value\_changed(“parent\_task”) or self.has\_value\_changed(“project”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“parent\_task”) → self.has\_value\_changed(“project”).
  - Return no value.
- Set tuple(parent\_project, parent\_company) from Platform.db.get\_value(“Task”, self.parent\_task, list(“project”, “company”)).
- If (not self.project and parent\_project).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.project → parent\_project.
  - Set tuple(self.project, self.company) from tuple(parent\_project, parent\_company).
- Otherwise.
  - If (self.project or no value) differs from (parent\_project or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.project → no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_project → no value.
    - Call the validation error handler Platform.throw(translated “Parent Task {0} is not in Project {1}. Pick a group task of the same project.”.format(get\_link\_to\_form(“Task”, self.parent\_task), Platform.bold(self.project)), title = translated ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L241) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1366)
