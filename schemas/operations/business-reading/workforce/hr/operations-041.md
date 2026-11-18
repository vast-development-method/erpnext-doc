# Employment and attendance · operations 41

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Staffing plan

[Record definition](../../../../data/record-types/staffing_plan.json)

<a id="op-58f880d107cd65"></a>
### Staffing Plan.validate overlap

`operation_workforce_human_resources_record_definitions_staffing_plan_business_behavior_staffing_plan_validate_overlap`

**Inputs** self, staffing\_plan\_detail.

**Explicit failure paths** validation helper — translated “Staffing Plan {0} already exist for designation {1}”.format(overlap at 0 at 0, staffing\_plan\_detail.designation).

**Local steps**

- Set spd from Platform.qb.DocType(“Staffing Plan Detail”).
- Set sp from Platform.qb.DocType(“Staffing Plan”).
- Set overlap from nested operand in the contract(nested operand in the contract).select(spd.parent).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the cont ….run().
- If (overlap and overlap at 0 at 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in overlap → overlap at 0 at 0.
  - Call the validation error handler Platform.throw(translated “Staffing Plan {0} already exist for designation {1}”.format(overlap at 0 at 0, staffing\_plan\_detail.designation)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0076.json#L4136) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1596) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L205)

<a id="op-d114cdf0a09925"></a>
### Staffing Plan.validate with parent plan

`operation_workforce_human_resources_record_definitions_staffing_plan_business_behavior_staffing_plan_validate_with_parent_plan`

**Inputs** self, staffing\_plan\_detail.

**Record and data access** read “Company” via get\_cached\_value · read “Staffing Plan” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with ParentCompanyError — translated “You can only plan for upto {0} vacancies and budget {1} for {2} as per staffing plan {3} for parent company {4}.”.format(cint(parent\_plan\_details at 0.vacancies), parent\_plan\_details at 0.total … · validation helper — translated “{0} vacancies and {1} budget for {2} already planned for subsidiary companies of {3}. You can only plan for  …”.format(cint(all\_sibling\_details.vacancies), all\_sibling\_details.total\_estimated\_c ….

**Local steps**

- If not Platform.get\_cached\_value(“Company”, self.company, “parent\_company”).
  - Return no value.
- Set parent\_plan\_details from get\_active\_staffing\_plan\_details(self.company, staffing\_plan\_detail.designation, self.from\_date, self.to\_date).
- If not parent\_plan\_details.
  - Return no value.
- Set parent\_company from Platform.db.get\_value(“Staffing Plan”, parent\_plan\_details at 0.name, “company”).
- If (cint(staffing\_plan\_detail.vacancies) &gt; cint(parent\_plan\_details at 0.vacancies) or flt(staffing\_plan\_detail.total\_estimated\_cost) &gt; flt(parent\_plan\_details at 0.total\_estimated\_cost)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(staffing\_plan\_detail.vacancies) &gt; cint(parent\_plan\_details at 0.vacancies) → flt(staffing\_plan\_detail.total\_estimated\_cost) &gt; flt(parent\_plan\_details at 0.total\_estimated\_cost).
  - Call the validation error handler Platform.throw(translated “You can only plan for upto {0} vacancies and budget {1} for {2} as per staffing plan {3} for parent company {4}.”.format(cint(parent\_plan\_details at 0.vacancies), parent\_plan\_det ….
- Set tuple(lft, rgt) from Platform.get\_cached\_value(“Company”, parent\_company, list(“lft”, “rgt”)).
- Set spd from Platform.qb.DocType(“Staffing Plan Detail”).
- Set sp from Platform.qb.DocType(“Staffing Plan”).
- Set company from Platform.qb.DocType(“Company”).
- Set all\_sibling\_details from nested operand in the contract.select(nested operand in the contract(nested operand in the contract), nested operand in the contract(nested operand in the contract)).where((((nested operand in the contract … at 0.
- If (cint(parent\_plan\_details at 0.vacancies) &lt; (cint(staffing\_plan\_detail.vacancies) + cint(all\_sibling\_details.vacancies)) or flt(parent\_plan\_details at 0.total\_estimated\_cost) &lt; (flt(staffing\_plan\_detail.to ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(parent\_plan\_details at 0.vacancies) &lt; (cint(staffing\_plan\_detail.vacancies) + cint(all\_sibling\_details.vacancies)) → flt(parent\_plan\_details at 0.total\_estimated\_cost) &lt; (flt(staffing\_plan\_detail.total\_estimated\_cost) + flt(all\_sibling\_details.total\_estimated\_cost)).
  - Call the validation error handler Platform.throw(translated “{0} vacancies and {1} budget for {2} already planned for subsidiary companies of {3}. You can only plan for  …”.format(cint(all\_sibling\_details.vacancies), all\_sibling\_details.to ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “parent\_company”), Platform.get\_cached\_value(“Company”, parent\_company, list(“lft”, “rgt”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0076.json#L4627) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1598) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L207)

<a id="op-325d1a59b58be5"></a>
### Staffing Plan.validate with subsidiary plans

`operation_workforce_human_resources_record_definitions_staffing_plan_business_behavior_staffing_plan_validate_with_subsidiary_plans`

**Inputs** self, staffing\_plan\_detail.

**Explicit failure paths** validation helper with SubsidiaryCompanyError — translated “Subsidiary companies have already planned for {1} vacancies at a budget of {2}. Staffing Plan for {0} should …”.format(self.company, cint(children\_details.vacancies), children\_details.total\_est ….

**Local steps**

- Set spd from Platform.qb.DocType(“Staffing Plan Detail”).
- Set sp from Platform.qb.DocType(“Staffing Plan”).
- Set company from Platform.qb.DocType(“Company”).
- Set children\_details from nested operand in the contract.select(nested operand in the contract(nested operand in the contract), nested operand in the contract(nested operand in the contract)).where((((nested operand in the contract … at 0.
- If ((children\_details and cint(staffing\_plan\_detail.vacancies) &lt; cint(children\_details.vacancies)) or flt(staffing\_plan\_detail.total\_estimated\_cost) &lt; flt(children\_details.total\_estimated\_cost)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (children\_details and cint(staffing\_plan\_detail.vacancies) &lt; cint(children\_details.vacancies)) → flt(staffing\_plan\_detail.total\_estimated\_cost) &lt; flt(children\_details.total\_estimated\_cost).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in children\_details → cint(staffing\_plan\_detail.vacancies) &lt; cint(children\_details.vacancies).
  - Call the validation error handler Platform.throw(translated “Subsidiary companies have already planned for {1} vacancies at a budget of {2}. Staffing Plan for {0} should …”.format(self.company, cint(children\_details.vacancies), children\_de ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0076.json#L6101) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1599) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L208)

<a id="op-a286440756d789"></a>
### Staffing Plan.set job requisitions

`operation_workforce_human_resources_record_definitions_staffing_plan_business_behavior_staffing_plan_set_job_requisitions`

**Inputs** self, job\_reqs.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Record and data access** read “Job Requisition” via get\_list.

**Explicit results** self.

**Local steps**

- If job\_reqs.
  - Set requisitions from Platform.db.get\_list(“Job Requisition”, filters = mapping(“name” → list(“in”, job\_reqs)), fields = list(“designation”, “no\_of\_positions”, “expected\_compensation”)).
  - Set self.staffing\_details from list().
  - For each req in requisitions.
    - Set current\_count from get\_designation\_counts(req.designation, self.company) at “employee\_count”.
    - Evaluate self.append(“staffing\_details”, mapping(“designation” → req.designation, “vacancies” → req.no\_of\_positions, “estimated\_cost\_per\_position” → req.expected\_compensation, “number\_of\_positions” → (cint(current\_ ….
- Return self.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0077.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1591) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L200)

<a id="op-8e7bd63e1d8f32"></a>
### Get designation counts

`operation_workforce_human_resources_record_definitions_staffing_plan_business_behavior_get_designation_counts`

**Inputs** designation, company, job\_opening = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (dict bitwise or bool).

**Record and data access** read “Employee” via count · read “Job Opening” via count.

**Explicit results** false · mapping(“employee\_count” → employee\_count, “job\_openings” → job\_openings).

**Local steps**

- If not designation.
  - Return false.
- Set company\_set from get\_descendants\_of(“Company”, company).
- Evaluate company\_set.append(company).
- Set employee\_count from Platform.db.count(“Employee”, mapping(“designation” → designation, “status” → “Active”, “company” → tuple(“in”, company\_set))).
- Set filters from mapping(“designation” → designation, “status” → “Open”, “company” → tuple(“in”, company\_set)).
- If job\_opening.
  - Set filters at “name” from tuple(“!=”, job\_opening).
- Set job\_openings from Platform.db.count(“Job Opening”, filters).
- Return mapping(“employee\_count” → employee\_count, “job\_openings” → job\_openings).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0077.json#L438) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1590) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L199)

<a id="op-cdb73d00321858"></a>
### Get active staffing plan details

`operation_workforce_human_resources_record_definitions_staffing_plan_business_behavior_get_active_staffing_plan_details`

**Inputs** company, designation, from\_date = no value, to\_date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (list at dict bitwise or no value).

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** staffing\_plan when staffing\_plan, otherwise no value.

**Explicit failure paths** validation helper — translated “Please select Company and Designation”.

**Local steps**

- Evaluate Platform.has\_permission(“Staffing Plan”, “read”, throw = true).
- If from\_date is identical to no value.
  - Set from\_date from getdate(nowdate()).
- If to\_date is identical to no value.
  - Set to\_date from getdate(nowdate()).
- If (not company or not designation).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not company → not designation.
  - Call the validation error handler Platform.throw(translated “Please select Company and Designation”).
- Set spd from Platform.qb.DocType(“Staffing Plan Detail”).
- Set sp from Platform.qb.DocType(“Staffing Plan”).
- Set staffing\_plan from nested operand in the contract(nested operand in the contract).select(sp.name, spd.vacancies, spd.total\_estimated\_cost).where(((((nested operand in the contract bitwise and nested operand in the contract)  ….
- If not staffing\_plan.
  - Set parent\_company from Platform.get\_cached\_value(“Company”, company, “parent\_company”).
  - If parent\_company.
    - Set staffing\_plan from get\_active\_staffing\_plan\_details(parent\_company, designation, from\_date, to\_date).
- Return staffing\_plan when staffing\_plan, otherwise no value.
  - Value choice on staffing\_plan — true gives staffing\_plan, false gives no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Staffing Plan”, “read”, throw = true) · clock or generated value from nowdate() · configured or stored value from Platform.get\_cached\_value(“Company”, company, “parent\_company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0077.json#L906) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1589) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L198)

<a id="op-bab19b8ed739b4"></a>
### Get data

`operation_workforce_human_resources_record_definitions_staffing_plan_staffing_plan_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “staffing\_plan”, “transactions” → list(mapping(“items” → list(“Job Opening”)))).

**Local steps**

- Return mapping(“fieldname” → “staffing\_plan”, “transactions” → list(mapping(“items” → list(“Job Opening”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0077.json#L1766) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1600) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L209)

## Record · Training event

[Record definition](../../../../data/record-types/training_event.json)

<a id="op-19cd793d9870e8"></a>
### Training Event.validate

`operation_workforce_human_resources_record_definitions_training_event_business_behavior_training_event_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_employee\_emails().
- Evaluate self.validate\_period().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set employee emails](operations-041.md#op-915a0e9f2ad239), [validate period](operations-041.md#op-f65045179d9ac3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0077.json#L5103) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1610) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L219)

<a id="op-6492fe8f777772"></a>
### Training Event.on update after submit

`operation_workforce_human_resources_record_definitions_training_event_business_behavior_training_event_on_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status\_for\_attendees().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status for attendees](operations-041.md#op-f51124627cb8bf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0077.json#L5174) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1607) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L216)

<a id="op-915a0e9f2ad239"></a>
### Training Event.set employee emails

`operation_workforce_human_resources_record_definitions_training_event_business_behavior_training_event_set_employee_emails`

**Inputs** self.

**Local steps**

- Set self.employee\_emails from “, ”.join(get\_employee\_emails(list of d.employee for d drawn from self.employees)).
  - Draw d from self.employees.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0077.json#L5225) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1608) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L217)

<a id="op-f65045179d9ac3"></a>
### Training Event.validate period

`operation_workforce_human_resources_record_definitions_training_event_business_behavior_training_event_validate_period`

**Inputs** self.

**Explicit failure paths** validation helper — translated “End time cannot be before start time”.

**Local steps**

- If time\_diff\_in\_seconds(self.end\_time, self.start\_time) ≤ 0.
  - Call the validation error handler Platform.throw(translated “End time cannot be before start time”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0077.json#L5330) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1611) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L220)

<a id="op-f51124627cb8bf"></a>
### Training Event.set status for attendees

`operation_workforce_human_resources_record_definitions_training_event_business_behavior_training_event_set_status_for_attendees`

**Inputs** self.

**Local steps**

- If self.event\_status equals “Completed”.
  - For each employee in self.employees.
    - If (employee.attendance equals “Present” and employee.status differs from “Feedback Submitted”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in employee.attendance equals “Present” → employee.status differs from “Feedback Submitted”.
      - Set employee.status from “Completed”.
- Otherwise.
  - If self.event\_status equals “Scheduled”.
    - For each employee in self.employees.
      - Set employee.status from “Open”.
- Evaluate self.db\_update\_all().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0077.json#L5448) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1609) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L218)

<a id="op-b352e664376b51"></a>
### Get data

`operation_workforce_human_resources_record_definitions_training_event_training_event_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “training\_event”, “transactions” → list(mapping(“items” → list(“Training Result”, “Training Feedback”)))).

**Local steps**

- Return mapping(“fieldname” → “training\_event”, “transactions” → list(mapping(“items” → list(“Training Result”, “Training Feedback”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0077.json#L5674) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1616) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L225)

## Record · Training feedback

[Record definition](../../../../data/record-types/training_feedback.json)

<a id="op-12f7bf7332affb"></a>
### Training Feedback.validate

`operation_workforce_human_resources_record_definitions_training_feedback_business_behavior_training_feedback_validate`

**Inputs** self.

**Record and data access** resolve a document from “Training Event” via get\_doc · read “Training Event Employee” via get\_value.

**Explicit failure paths** validation helper — translated “{0} must be submitted”.format(translated “Training Event”) · validation helper — translated “Employee {0} not found in Training Event Participants.”.format(Platform.bold(self.employee\_name)) · validation helper — translated “Feedback cannot be recorded for an absent Employee.”.

**Local steps**

- Set training\_event from Platform.get\_doc(“Training Event”, self.training\_event).
- <a id="op-12f7bf7332affb-guard-3"></a>If training\_event.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “{0} must be submitted”.format(translated “Training Event”)).
- Set emp\_event\_details from Platform.db.get\_value(“Training Event Employee”, mapping(“parent” → self.training\_event, “employee” → self.employee), list(“name”, “attendance”), as\_dict = true).
- If not emp\_event\_details.
  - Call the validation error handler Platform.throw(translated “Employee {0} not found in Training Event Participants.”.format(Platform.bold(self.employee\_name))).
- If emp\_event\_details.attendance equals “Absent”.
  - Call the validation error handler Platform.throw(translated “Feedback cannot be recorded for an absent Employee.”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison training\_event.docstatus differs from 1, training\_event.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “{0} must be submitted”.format(translated “Training Event”). With training\_event.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-12f7bf7332affb-guard-3)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0077.json#L6827) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1619) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L228)

<a id="op-7b0e8a38efe176"></a>
### Training Feedback.on submit

`operation_workforce_human_resources_record_definitions_training_feedback_business_behavior_training_feedback_on_submit`

**Inputs** self.

**Record and data access** read “Training Event Employee” via get\_value.

**State and service calls** request set\_value on “Training Event Employee”.

**Local steps**

- Set employee from Platform.db.get\_value(“Training Event Employee”, mapping(“parent” → self.training\_event, “employee” → self.employee)).
- If employee.
  - Evaluate Platform.db.set\_value(“Training Event Employee”, employee, “status”, “Feedback Submitted”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0077.json#L7267) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1618) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L227)

<a id="op-a5b7a53f219f9a"></a>
### Training Feedback.on cancel

`operation_workforce_human_resources_record_definitions_training_feedback_business_behavior_training_feedback_on_cancel`

**Inputs** self.

**Record and data access** read “Training Event Employee” via get\_value.

**State and service calls** request set\_value on “Training Event Employee”.

**Local steps**

- Set employee from Platform.db.get\_value(“Training Event Employee”, mapping(“parent” → self.training\_event, “employee” → self.employee)).
- If employee.
  - Evaluate Platform.db.set\_value(“Training Event Employee”, employee, “status”, “Completed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0078.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1617) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L226)

## Service · Training feedback

<a id="op-d3f00f7285ce40"></a>
### Get context

`operation_workforce_human_resources_notification_training_feedback_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L1987) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L304) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L304)

## Record · Training program

[Record definition](../../../../data/record-types/training_program.json)

<a id="op-f4077093d11e98"></a>
### Get data

`operation_workforce_human_resources_record_definitions_training_program_training_program_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “training\_program”, “transactions” → list(mapping(“label” → translated “Training Events”, “items” → list(“Training Event”)))).

**Local steps**

- Return mapping(“fieldname” → “training\_program”, “transactions” → list(mapping(“label” → translated “Training Events”, “items” → list(“Training Event”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0078.json#L179) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1624) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L233)

## Record · Training result

[Record definition](../../../../data/record-types/training_result.json)

<a id="op-0e948f65ad6af6"></a>
### Training Result.validate

`operation_workforce_human_resources_record_definitions_training_result_business_behavior_training_result_validate`

**Inputs** self.

**Record and data access** resolve a document from “Training Event” via get\_doc.

**Explicit failure paths** validation helper — translated “{0} must be submitted”.format(translated “Training Event”).

**Local steps**

- Set training\_event from Platform.get\_doc(“Training Event”, self.training\_event).
- <a id="op-0e948f65ad6af6-guard-3"></a>If training\_event.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “{0} must be submitted”.format(translated “Training Event”)).
- Evaluate self.validate\_duplicate\_result().
- Set self.employee\_emails from “, ”.join(get\_employee\_emails(list of d.employee for d drawn from self.employees)).
  - Draw d from self.employees.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison training\_event.docstatus differs from 1, training\_event.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “{0} must be submitted”.format(translated “Training Event”). With training\_event.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-0e948f65ad6af6-guard-3)

**Methods declared on this owner** [validate duplicate result](operations-041.md#op-4d944a8c3738c2).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L72) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1627) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L236)

<a id="op-4d944a8c3738c2"></a>
### Training Result.validate duplicate result

`operation_workforce_binding_workforce_hr_doctype_training_result_training_result_trainingresult_validate_duplicate_result`

**Inputs** self.

**Record and data access** read “Training Result” via exists.

**Explicit failure paths** validation helper with Platform.UniqueValidationError — translated “Training Result {0} already exists for Training Event {1}”.format(get\_link\_to\_form(“Training Result”, result), Platform.bold(self.training\_event)).

**Local steps**

- If result bound to Platform.db.exists(“Training Result”, mapping(“training\_event” → self.training\_event, “docstatus” → tuple(“!=”, 2), “name” → tuple(“!=”, self.name))).
  - Call the validation error handler Platform.throw(translated “Training Result {0} already exists for Training Event {1}”.format(get\_link\_to\_form(“Training Result”, result), Platform.bold(self.training\_event)), Platform.UniqueValidationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L86) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L137) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L137)

<a id="op-b2023b010d0428"></a>
### Training Result.on submit

`operation_workforce_human_resources_record_definitions_training_result_business_behavior_training_result_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “Training Event” via get\_doc.

**State and service calls** call save on training\_event.

**Local steps**

- Set training\_event from Platform.get\_doc(“Training Event”, self.training\_event).
- Set training\_event.status from “Completed”.
- For each e in self.employees.
  - For each e1 in training\_event.employees.
    - If e1.employee equals e.employee.
      - Set e1.status from “Completed”.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Evaluate training\_event.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0078.json#L550) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1626) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L235)

<a id="op-db828946748909"></a>
### Get employees

`operation_workforce_human_resources_record_definitions_training_result_business_behavior_get_employees`

**Inputs** training\_event.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Training Event” via get\_doc.

**Explicit results** Platform.get\_doc(“Training Event”, training\_event).employees.

**Local steps**

- Evaluate Platform.has\_permission(“Training Event”, “read”, training\_event, throw = true).
- Return Platform.get\_doc(“Training Event”, training\_event).employees.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Training Event”, “read”, training\_event, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0078.json#L746) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1625) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L234)

## Service · Training scheduled

<a id="op-75465b2808d077"></a>
### Get context

`operation_workforce_human_resources_notification_training_scheduled_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L2020) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L305) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L305)

## Record · Travel request

[Record definition](../../../../data/record-types/travel_request.json)

<a id="op-9a3164235b398f"></a>
### Travel Request.validate

`operation_workforce_human_resources_record_definitions_travel_request_business_behavior_travel_request_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0078.json#L891) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1628) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L237)
