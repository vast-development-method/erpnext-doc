# Projects and time · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Project

[Record definition](../../../../data/record-types/project.json)

<a id="op-5038054c4625a6"></a>
### Work date

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_work_date`

**Inputs** detail.

**Declared result** Term.

**Explicit results** Coalesce(detail.from\_time, detail.to\_time).

**Local steps**

- Return Coalesce(detail.from\_time, detail.to\_time).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L265) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1275)

<a id="op-2dfecfe57af957"></a>
### Sum amount

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_sum_amount`

**Inputs** query, amount, posting\_date = no value, by\_month = false.

**Declared result** (float bitwise or MonthlyAmounts).

**Explicit results** flt(nested operand in the contract.select(nested operand in the contract(nested operand in the contract)).run() at 0 at 0) · mapping of formatted text {int(row.year)}-{int(row.month)} → flt(row.amount) for row drawn from rows.

**Local steps**

- If not by\_month.
  - Return flt(nested operand in the contract.select(nested operand in the contract(nested operand in the contract)).run() at 0 at 0).
- Set year from Extract(DatePart.year, posting\_date).
- Set month from Extract(DatePart.month, posting\_date).
- Set rows from query.select(nested operand in the contract.as\_(“year”), nested operand in the contract.as\_(“month”), nested operand in the contract.as\_(“amount”)).groupby(year, month).run(as\_dict = true).
- Return mapping of formatted text {int(row.year)}-{int(row.month)} → flt(row.amount) for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L263) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1273)

<a id="op-2647bed1f45483"></a>
### Combine

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_combine`

**Inputs** first, second, sign = 1.

**Declared result** (float bitwise or MonthlyAmounts).

**Explicit results** (first + (sign × second)) · months.

**Local steps**

- If not isinstance(first, dict).
  - Return (first + (sign × second)).
- Set months from dict(first).
- For each tuple(key, amount) in second.items().
  - Set months at key from (months.get(key, 0.0) + (sign × amount)).
- Return months.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1254)

<a id="op-eb91715cc278eb"></a>
### Project.onload

`operation_enterprise_projects_record_definitions_project_business_behavior_project_onload`

**Inputs** self.

**Record and data access** execute query text (SELECT, Timesheet Detail).

**Local steps**

- Evaluate self.set\_onload(“activity\_summary”, Platform.db.sql(query text (SELECT, Timesheet Detail), self.name, as\_dict = true)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1226) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L693)

<a id="op-1083e1781aef05"></a>
### Project.before print

`operation_enterprise_projects_record_definitions_project_business_behavior_project_before_print`

**Inputs** self, settings = no value.

**Local steps**

- Evaluate self.onload().

If control reaches the end, it returns no value.

**Methods declared on this owner** [onload](operations-006.md#op-eb91715cc278eb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0600.json#L957) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1209) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L679)

<a id="op-180d2a3653325c"></a>
### Project.validate

`operation_enterprise_projects_record_definitions_project_business_behavior_project_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_project\_template().
- If not self.is\_new().
  - Evaluate self.control\_access\_for\_project\_users().
- Evaluate self.send\_welcome\_email().
- Evaluate self.update\_costing().
- Evaluate self.update\_percent\_complete().
- Evaluate self.validate\_from\_to\_dates(“expected\_start\_date”, “expected\_end\_date”).
- Evaluate self.validate\_from\_to\_dates(“actual\_start\_date”, “actual\_end\_date”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate project template](operations-006.md#op-0f1326fae48bd8), [control access for project users](operations-007.md#op-1810b84baae99e), [send welcome email](operations-007.md#op-6b27d217b87388), [update costing](operations-006.md#op-439dd895cc3898), [update percent complete](operations-006.md#op-cc5e7af8d673ee).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1237) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L704)

<a id="op-0f1326fae48bd8"></a>
### Project.validate project template

`operation_enterprise_binding_enterprise_projects_doctype_project_project_project_validate_project_template`

**Inputs** self.

**Record and data access** read “Project Template” via get\_value.

**Explicit failure paths** validation helper — translated “Project Template {0} is disabled”.format(Platform.bold(self.project\_template)).

**Local steps**

- If (self.project\_template and self.has\_value\_changed(“project\_template”) and Platform.db.get\_value(“Project Template”, self.project\_template, “disabled”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.project\_template → self.has\_value\_changed(“project\_template”) → Platform.db.get\_value(“Project Template”, self.project\_template, “disabled”).
  - Call the validation error handler Platform.throw(translated “Project Template {0} is disabled”.format(Platform.bold(self.project\_template))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L226) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1351)

<a id="op-9f67c97c737913"></a>
### Project.copy from template

`operation_enterprise_projects_record_definitions_project_business_behavior_project_copy_from_template`

**Inputs** self.

**Record and data access** read “Task” via get\_all · resolve a document from “Project Template” via get\_doc · resolve a document from “Task” via get\_doc.

**Local steps**

- If (self.project\_template and not Platform.db.get\_all(“Task”, dict(project = self.name), limit = 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.project\_template → not Platform.db.get\_all(“Task”, dict(project = self.name), limit = 1).
  - If not self.expected\_start\_date.
    - Set self.expected\_start\_date from today().
  - Set template from Platform.get\_doc(“Project Template”, self.project\_template).
  - If not self.project\_type.
    - Set self.project\_type from template.project\_type.
  - Set project\_tasks from list().
  - Set tmp\_task\_details from list().
  - For each task in template.tasks.
    - Set template\_task\_details from Platform.get\_doc(“Task”, task.task).
    - Evaluate tmp\_task\_details.append(template\_task\_details).
    - Set task from self.create\_task\_from\_template(template\_task\_details).
    - Evaluate project\_tasks.append(task).
  - Evaluate self.dependency\_mapping(tmp\_task\_details, project\_tasks).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create task from template](operations-006.md#op-1df6a100b400aa), [dependency mapping](operations-006.md#op-cb84bbda424669).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1218) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L688)

<a id="op-1df6a100b400aa"></a>
### Project.create task from template

`operation_enterprise_projects_record_definitions_project_business_behavior_project_create_task_from_template`

**Inputs** self, task\_details.

**Record and data access** resolve a document from “Task” via get\_doc.

**State and service calls** call insert on Platform.get\_doc(doctype = “Task”, subject = task\_details.subject, project = self.name, status = “Open”, …).

**Explicit results** Platform.get\_doc(doctype = “Task”, subject = task\_details.subject, project = self.name, status = “Open”, …).insert().

**Local steps**

- Return Platform.get\_doc(doctype = “Task”, subject = task\_details.subject, project = self.name, status = “Open”, …).insert().

**Methods declared on this owner** [calculate start date](operations-006.md#op-df1cefd5c2b912), [calculate end date](operations-006.md#op-c179244df63c69).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0600.json#L1802) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1219) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L689)

<a id="op-df1cefd5c2b912"></a>
### Project.calculate start date

`operation_enterprise_projects_record_definitions_project_business_behavior_project_calculate_start_date`

**Inputs** self, task\_details.

**Explicit results** self.start\_date.

**Local steps**

- Set self.start\_date from add\_days(self.expected\_start\_date, task\_details.start).
- Set self.start\_date from self.update\_if\_holiday(self.start\_date).
- Return self.start\_date.

**Methods declared on this owner** [update if holiday](operations-006.md#op-0cd70bf6fbc10b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0600.json#L2082) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L682)

<a id="op-c179244df63c69"></a>
### Project.calculate end date

`operation_enterprise_projects_record_definitions_project_business_behavior_project_calculate_end_date`

**Inputs** self, task\_details.

**Explicit results** self.update\_if\_holiday(self.end\_date).

**Local steps**

- Set self.end\_date from add\_days(self.start\_date, task\_details.duration).
- Return self.update\_if\_holiday(self.end\_date).

**Methods declared on this owner** [update if holiday](operations-006.md#op-0cd70bf6fbc10b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0600.json#L2213) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L680)

<a id="op-0cd70bf6fbc10b"></a>
### Project.update if holiday

`operation_enterprise_projects_record_definitions_project_business_behavior_project_update_if_holiday`

**Inputs** self, date.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** date.

**Local steps**

- Set holiday\_list from (self.holiday\_list or Platform.get\_cached\_value(“Company”, self.company, “default\_holiday\_list”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.holiday\_list → Platform.get\_cached\_value(“Company”, self.company, “default\_holiday\_list”).
- While is\_holiday(holiday\_list, date).
  - Set date from add\_days(date, 1).
- Return date.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_holiday\_list”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1232) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L699)

<a id="op-cb84bbda424669"></a>
### Project.dependency mapping

`operation_enterprise_projects_record_definitions_project_business_behavior_project_dependency_mapping`

**Inputs** self, template\_tasks, project\_tasks.

**Record and data access** resolve a document from “Task” via get\_doc.

**Local steps**

- For each project\_task in project\_tasks.
  - Set template\_task from Platform.get\_doc(“Task”, project\_task.template\_task).
  - Evaluate self.check\_depends\_on\_value(template\_task, project\_task, project\_tasks).
  - Evaluate self.check\_for\_parent\_tasks(template\_task, project\_task, project\_tasks).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check depends on value](operations-006.md#op-4c8b1b60a651b2), [check for parent tasks](operations-006.md#op-296113a08d52e6).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0600.json#L2472) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1220) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L690)

<a id="op-39d3b89b5dfde8"></a>
### Project.set consumed material cost

`operation_enterprise_projects_record_definitions_project_business_behavior_project_set_consumed_material_cost`

**Inputs** self.

**Local steps**

- Set self.total\_consumed\_material\_cost from ProjectCostQueries(self.name).material\_cost().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L695)

<a id="op-4c8b1b60a651b2"></a>
### Project.check depends on value

`operation_enterprise_projects_record_definitions_project_business_behavior_project_check_depends_on_value`

**Inputs** self, template\_task, project\_task, project\_tasks.

**State and service calls** call save on project\_task.

**Local steps**

- If (template\_task.get(“depends\_on”) and not project\_task.get(“depends\_on”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in template\_task.get(“depends\_on”) → not project\_task.get(“depends\_on”).
  - Set project\_template\_map from mapping of pt.template\_task → pt for pt drawn from project\_tasks.
    - Draw pt from project\_tasks.
  - For each child\_task in template\_task.get(“depends\_on”).
    - If (project\_template\_map and project\_template\_map.get(child\_task.task)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in project\_template\_map → project\_template\_map.get(child\_task.task).
      - Evaluate project\_task.reload().
      - Evaluate project\_task.append(“depends\_on”, mapping(“task” → project\_template\_map.get(child\_task.task).name)).
      - Evaluate project\_task.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0600.json#L3322) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L683)

<a id="op-296113a08d52e6"></a>
### Project.check for parent tasks

`operation_enterprise_projects_record_definitions_project_business_behavior_project_check_for_parent_tasks`

**Inputs** self, template\_task, project\_task, project\_tasks.

**State and service calls** call save on project\_task.

**Local steps**

- If (template\_task.get(“parent\_task”) and not project\_task.get(“parent\_task”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in template\_task.get(“parent\_task”) → not project\_task.get(“parent\_task”).
  - For each pt in project\_tasks.
    - If pt.template\_task equals template\_task.parent\_task.
      - Set project\_task.parent\_task from pt.name.
      - Evaluate project\_task.save().
      - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0600.json#L3664) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L684)

<a id="op-311aee36c23bf5"></a>
### Project.is row updated

`operation_enterprise_projects_record_definitions_project_business_behavior_project_is_row_updated`

**Inputs** self, row, existing\_task\_data, fields.

**Explicit results** true.

**Local steps**

- If (self.get(“\_\_islocal”) or not existing\_task\_data).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“\_\_islocal”) → not existing\_task\_data.
  - Return true.
- Set d from existing\_task\_data.get(row.task\_id, mapping()).
- For each field in fields.
  - If row.get(field) differs from d.get(field).
    - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0600.json#L3871) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1223) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L691)

<a id="op-699b62337ff963"></a>
### Project.update project

`operation_enterprise_projects_record_definitions_project_business_behavior_project_update_project`

**Inputs** self.

**State and service calls** call db\_update on self.

**Local steps**

- Evaluate self.update\_percent\_complete().
- Evaluate self.update\_costing().
- Evaluate self.db\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update percent complete](operations-006.md#op-cc5e7af8d673ee), [update costing](operations-006.md#op-439dd895cc3898).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0600.json#L4083) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L701)

<a id="op-cc6a69f581699c"></a>
### Project.after insert

`operation_enterprise_projects_record_definitions_project_business_behavior_project_after_insert`

**Inputs** self.

**State and service calls** request set\_value on “Sales Order” · call db\_set on self.

**Local steps**

- Evaluate self.copy\_from\_template().
- If self.sales\_order.
  - Evaluate Platform.db.set\_value(“Sales Order”, self.sales\_order, “project”, self.name).
  - Evaluate self.update\_sales\_amount().
  - Evaluate self.db\_set(“total\_sales\_amount”, self.total\_sales\_amount).
- Evaluate self.control\_access\_for\_project\_users().

If control reaches the end, it returns no value.

**Methods declared on this owner** [copy from template](operations-006.md#op-9f67c97c737913), [update sales amount](operations-007.md#op-6921967d707bcc), [control access for project users](operations-007.md#op-1810b84baae99e).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1207) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L677)

<a id="op-e1a0c4e75f6e34"></a>
### Project.on trash

`operation_enterprise_projects_record_definitions_project_business_behavior_project_on_trash`

**Inputs** self.

**State and service calls** request set\_value on “Sales Order”.

**Local steps**

- Evaluate Platform.db.set\_value(“Sales Order”, mapping(“project” → self.name), “project”, empty text).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0600.json#L4557) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L692)

<a id="op-cc5e7af8d673ee"></a>
### Project.update percent complete

`operation_enterprise_projects_record_definitions_project_business_behavior_project_update_percent_complete`

**Inputs** self.

**Record and data access** read “Task” via get\_all · read “Task” via count · execute query text (SELECT, Task).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “% Complete must be between 0 and 100”.

**Local steps**

- If self.status equals “Completed”.
  - If len(Platform.get\_all(“Task”, dict(project = self.name))) equals 0.
    - Set self.percent\_complete\_method from “Manual”.
    - Set self.percent\_complete from 100.
- If self.percent\_complete\_method equals “Manual”.
  - If self.status equals “Completed”.
    - Set self.percent\_complete from 100.
  - Otherwise.
    - If (flt(self.percent\_complete) &lt; 0 or flt(self.percent\_complete) &gt; 100).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.percent\_complete) &lt; 0 → flt(self.percent\_complete) &gt; 100.
      - Call the validation error handler Platform.throw(translated “% Complete must be between 0 and 100”).
  - Return no value.
- Set total from Platform.db.count(“Task”, dict(project = self.name)).
- If not total.
  - Set self.percent\_complete from 0.
- Otherwise.
  - If ((self.percent\_complete\_method equals “Task Completion” and total &gt; 0) or (not self.percent\_complete\_method and total &gt; 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.percent\_complete\_method equals “Task Completion” and total &gt; 0) → (not self.percent\_complete\_method and total &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.percent\_complete\_method equals “Task Completion” → total &gt; 0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.percent\_complete\_method → total &gt; 0.
    - Set completed from Platform.db.sql(query text (SELECT, Task), self.name) at 0 at 0.
    - Set self.percent\_complete from flt(((flt(completed) ÷ total) × 100), 2).
  - If (self.percent\_complete\_method belongs to tuple(“Task Progress”, “Task Weight”) and total &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.percent\_complete\_method belongs to tuple(“Task Progress”, “Task Weight”) → total &gt; 0.
    - Set self.percent\_complete from flt(self.get\_task\_progress(), 2).
- <a id="op-cc5e7af8d673ee-guard-35"></a>If self.status belongs to tuple(“Cancelled”, “On hold”).
  - Return no value.
- Evaluate self.validate\_completed\_status().
- Set self.status from “Completed” when self.percent\_complete equals 100, otherwise “Open”.
  - Value choice on self.percent\_complete equals 100 — true gives “Completed”, false gives “Open”.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status belongs to tuple(“Cancelled”, “On hold”), self.status = “On hold” selects the branch that returns no value. With self.status = “Open”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-cc5e7af8d673ee-guard-35)

**Methods declared on this owner** [get task progress](operations-006.md#op-bfe05e4f697b53), [validate completed status](operations-006.md#op-cc344c73167078).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L700)

<a id="op-cc344c73167078"></a>
### Project.validate completed status

`operation_enterprise_binding_enterprise_projects_doctype_project_project_project_validate_completed_status`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Project {0} is only {1} complete. Complete or cancel its tasks first.”.format(Platform.bold(self.name), Platform.format(self.percent\_complete, mapping(“fieldtype” → “Percent”))).

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- If (not previous or previous.status equals “Completed” or self.status differs from “Completed”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not previous → previous.status equals “Completed” → self.status differs from “Completed”.
  - Return no value.
- If flt(self.percent\_complete) &lt; 100.
  - Call the validation error handler Platform.throw(translated “Project {0} is only {1} complete. Complete or cancel its tasks first.”.format(Platform.bold(self.name), Platform.format(self.percent\_complete, mapping(“fieldtype” → “Percent”))), ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L225) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1350)

<a id="op-bfe05e4f697b53"></a>
### Project.get task progress

`operation_enterprise_binding_enterprise_projects_doctype_project_project_project_get_task_progress`

**Inputs** self.

**Declared result** float.

**Record and data access** read “Task” via get\_all.

**Explicit results** (sum(generator of (p × w) for tuple(p, w) drawn from zip(progress, weights, strict = true)) ÷ sum(weights)).

**Local steps**

- Set tasks from Platform.get\_all(“Task”, filters = mapping(“project” → self.name), fields = list(“status”, “progress”, “task\_weight”)).
- Set weights from list of flt(task.task\_weight) for task drawn from tasks.
  - Draw task from tasks.
- If (self.percent\_complete\_method differs from “Task Weight” or not sum(weights)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.percent\_complete\_method differs from “Task Weight” → not sum(weights).
  - Set weights from (list(1) × len(tasks)).
- Set progress from list of 100 when task.status belongs to tuple(“Completed”, “Cancelled”), otherwise flt(task.progress) for task drawn from tasks.
  - Draw task from tasks.
  - Value choice on task.status belongs to tuple(“Completed”, “Cancelled”) — true gives 100, false gives flt(task.progress).
- Return (sum(generator of (p × w) for tuple(p, w) drawn from zip(progress, weights, strict = true)) ÷ sum(weights)).
  - Draw tuple(p, w) from zip(progress, weights, strict = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L224) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1349)

<a id="op-439dd895cc3898"></a>
### Project.update costing

`operation_enterprise_projects_record_definitions_project_business_behavior_project_update_costing`

**Inputs** self.

**Local steps**

- Bind dependencies Max, Min.
- Set TimesheetDetail from Platform.qb.DocType(“Timesheet Detail”).
- Set from\_time\_sheet from nested operand in the contract.select(nested operand in the contract(nested operand in the contract), nested operand in the contract(nested operand in the contract), nested operand in the contract(nested o … at 0.
- Set self.actual\_start\_date from from\_time\_sheet.start\_date.
- Set self.actual\_end\_date from from\_time\_sheet.end\_date.
- Set self.total\_costing\_amount from from\_time\_sheet.base\_costing\_amount.
- Set self.total\_billable\_amount from from\_time\_sheet.base\_billing\_amount.
- Set self.actual\_time from from\_time\_sheet.time.
- Evaluate self.update\_purchase\_costing().
- Evaluate self.update\_sales\_amount().
- Evaluate self.update\_billed\_amount().
- Evaluate self.calculate\_gross\_margin().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update purchase costing](operations-007.md#op-dd61aefc751a73), [update sales amount](operations-007.md#op-6921967d707bcc), [update billed amount](operations-007.md#op-43d0dee8ca9c2a), [calculate gross margin](operations-007.md#op-7c73872c8cec2a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L698)
