# Employment and attendance · operations 23

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Job offer

[Record definition](../../../../data/record-types/job_offer.json)

<a id="op-c8fbd9510b54f1"></a>
### Get leave allocations

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_get_leave_allocations`

**Inputs** leave\_policy = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** list() · nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….

**Local steps**

- Evaluate Platform.has\_permission(“Job Offer”, throw = true).
- If not leave\_policy.
  - Return list().
- Set LeavePolicyDetail from Platform.qb.DocType(“Leave Policy Detail”).
- Set LeaveType from Platform.qb.DocType(“Leave Type”).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Offer”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L73) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L124) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L124)

<a id="op-8c83b3a498f1c7"></a>
### Get holiday summary

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_get_holiday_summary`

**Inputs** holiday\_list = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Holiday” via get\_all.

**Explicit results** mapping(“weekly\_off\_days” → empty text, “total\_public\_holidays” → 0) · mapping(“weekly\_off\_days” → “, ”.join(generator of translated day for day drawn from sorted(off\_days, key = weekdays.index)), “total\_public\_holidays” → sum(generator of 1 for holiday drawn from holidays wh ….

**Local steps**

- Evaluate Platform.has\_permission(“Job Offer”, throw = true).
- If not holiday\_list.
  - Return mapping(“weekly\_off\_days” → empty text, “total\_public\_holidays” → 0).
- Set holidays from Platform.get\_all(“Holiday”, filters = mapping(“parent” → holiday\_list, “parenttype” → “Holiday List”), fields = list(“holiday\_date”, “weekly\_off”)).
- Set weekdays from get\_weekdays().
- Set off\_days from set of get\_weekday(holiday.holiday\_date) for holiday drawn from holidays where holiday.weekly\_off.
  - Draw holiday from holidays, keep a combination only if (holiday.weekly\_off).
- Return mapping(“weekly\_off\_days” → “, ”.join(generator of translated day for day drawn from sorted(off\_days, key = weekdays.index)), “total\_public\_holidays” → sum(generator of 1 for holiday drawn from holidays wh ….
  - Draw day from sorted(off\_days, key = weekdays.index).
  - Draw holiday from holidays, keep a combination only if (not holiday.weekly\_off).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Offer”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L72) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L123) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L123)

## Record · Job opening

[Record definition](../../../../data/record-types/job_opening.json)

<a id="op-9480f5a39da117"></a>
### Job Opening.autoname

`operation_workforce_human_resources_record_definitions_job_opening_business_behavior_job_opening_autoname`

**Inputs** self.

**Local steps**

- Evaluate set\_name\_from\_naming\_options(Platform.get\_meta(self.doctype).autoname, self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0039.json#L6222) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L951) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L931)

<a id="op-b520cec5f41a32"></a>
### Job Opening.validate

`operation_workforce_human_resources_record_definitions_job_opening_business_behavior_job_opening_validate`

**Inputs** self.

**Local steps**

- If not self.route.
  - Set self.route from formatted text jobs/{Platform.scrub(self.company)}/{Platform.scrub(self.job\_title).replace(“\_”, “-”)}.
- Evaluate self.update\_closing\_date().
- Evaluate self.validate\_dates().
- Evaluate self.validate\_current\_vacancies().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update closing date](operations-023.md#op-ae7585427d27ee), [validate dates](operations-023.md#op-d292f6700b613a), [validate current vacancies](operations-023.md#op-e0e74096e759dc).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0039.json#L6303) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L958) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L938)

<a id="op-bbb7a724668e14"></a>
### Job Opening.on update

`operation_workforce_human_resources_record_definitions_job_opening_business_behavior_job_opening_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.update\_job\_requisition\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update job requisition status](operations-023.md#op-f7b824d42208f9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0039.json#L6524) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L955) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L935)

<a id="op-ae7585427d27ee"></a>
### Job Opening.update closing date

`operation_workforce_human_resources_record_definitions_job_opening_business_behavior_job_opening_update_closing_date`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set old\_doc from self.get\_doc\_before\_save().
- If not old\_doc.
  - Return no value.
- If (old\_doc.status equals “Open” and self.status equals “Closed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_doc.status equals “Open” → self.status equals “Closed”.
  - Set self.closes\_on from no value.
  - If not self.closed\_on.
    - Set self.closed\_on from getdate().
- Otherwise.
  - If (old\_doc.status equals “Closed” and self.status equals “Open”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_doc.status equals “Closed” → self.status equals “Open”.
    - Set self.closed\_on from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0039.json#L6575) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L956) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L936)

<a id="op-d292f6700b613a"></a>
### Job Opening.validate dates

`operation_workforce_human_resources_record_definitions_job_opening_business_behavior_job_opening_validate_dates`

**Inputs** self.

**Local steps**

- If self.status equals “Open”.
  - Evaluate self.validate\_from\_to\_dates(“posted\_on”, “closes\_on”).
- If self.status equals “Closed”.
  - Evaluate self.validate\_from\_to\_dates(“posted\_on”, “closed\_on”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0039.json#L6832) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L960) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L940)

<a id="op-14a0bc79a136c2"></a>
### Job Opening.get close warning

`operation_workforce_human_resources_record_definitions_job_opening_business_behavior_job_opening_get_close_warning`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value · translated “Closing this Job Opening for {1} may not be according to the Staffing Plan {0}.&lt;br&gt;&lt;br&gt;Do you want to close  …”.format(Platform.bold(get\_link\_to\_form(“Staffing Plan”, self.staffing\_plan)), Plat ….

**Local steps**

- If not self.is\_opening\_being\_closed().
  - Return no value.
- If not self.staffing\_plan.
  - Return no value.
- Return translated “Closing this Job Opening for {1} may not be according to the Staffing Plan {0}.&lt;br&gt;&lt;br&gt;Do you want to close  …”.format(Platform.bold(get\_link\_to\_form(“Staffing Plan”, self.staffing\_plan)), Plat ….

**Methods declared on this owner** [is opening being closed](operations-023.md#op-2504d2e124ed63).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0039.json#L6988) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L952) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L932)

<a id="op-e0e74096e759dc"></a>
### Job Opening.validate current vacancies

`operation_workforce_human_resources_record_definitions_job_opening_business_behavior_job_opening_validate_current_vacancies`

**Inputs** self.

**Record and data access** read “Staffing Plan Detail” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Job Openings for the designation {0} are already open or the hiring is complete as per the Staffing Plan {1}”.format(Platform.bold(self.designation), get\_link\_to\_form(“Staffing Plan”, self.staf ….

**Local steps**

- <a id="op-e0e74096e759dc-guard-2"></a>If self.status equals “Closed”.
  - Return no value.
- If not self.staffing\_plan.
  - Set staffing\_plan from get\_active\_staffing\_plan\_details(self.company, self.designation).
  - If staffing\_plan.
    - Set self.staffing\_plan from staffing\_plan at 0.name.
    - Set self.planned\_vacancies from staffing\_plan at 0.vacancies.
- Otherwise.
  - If not self.planned\_vacancies.
    - Set self.planned\_vacancies from Platform.db.get\_value(“Staffing Plan Detail”, mapping(“parent” → self.staffing\_plan, “designation” → self.designation), “vacancies”).
- If (self.staffing\_plan and self.planned\_vacancies).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.staffing\_plan → self.planned\_vacancies.
  - Set designation\_counts from get\_designation\_counts(self.designation, self.company, self.name).
  - Set current\_count from (designation\_counts at “employee\_count” + designation\_counts at “job\_openings”).
  - Set number\_of\_positions from Platform.db.get\_value(“Staffing Plan Detail”, mapping(“parent” → self.staffing\_plan, “designation” → self.designation), “number\_of\_positions”).
  - If number\_of\_positions ≤ current\_count.
    - Call the validation error handler Platform.throw(translated “Job Openings for the designation {0} are already open or the hiring is complete as per the Staffing Plan {1}”.format(Platform.bold(self.designation), get\_link\_to\_form(“Staffing P ….

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Closed”, self.status = “Closed” selects the branch that returns no value. With self.status = “Open”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e0e74096e759dc-guard-2)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L959) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L939)

<a id="op-2504d2e124ed63"></a>
### Job Opening.is opening being closed

`operation_workforce_human_resources_record_definitions_job_opening_business_behavior_job_opening_is_opening_being_closed`

**Inputs** self.

**Record and data access** read self.doctype via get\_value.

**Explicit results** false · Platform.db.get\_value(self.doctype, self.name, “status”) equals “Open”.

**Local steps**

- If (self.is\_new() or self.status differs from “Closed”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.status differs from “Closed”.
  - Return false.
- Return Platform.db.get\_value(self.doctype, self.name, “status”) equals “Open”.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L667) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L954) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L934)

<a id="op-f7b824d42208f9"></a>
### Job Opening.update job requisition status

`operation_workforce_human_resources_record_definitions_job_opening_business_behavior_job_opening_update_job_requisition_status`

**Inputs** self.

**Record and data access** resolve a document from “Job Requisition” via get\_doc.

**State and service calls** call save on job\_requisition.

**Local steps**

- If (self.status equals “Closed” and self.job\_requisition).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Closed” → self.job\_requisition.
  - Set job\_requisition from Platform.get\_doc(“Job Requisition”, self.job\_requisition).
  - Set job\_requisition.status from “Filled”.
  - Set job\_requisition.completed\_on from (self.closed\_on or job\_requisition.completed\_on or getdate()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.closed\_on → job\_requisition.completed\_on → getdate().
  - Set job\_requisition.flags.ignore\_permissions from true.
  - Set job\_requisition.flags.ignore\_mandatory from true.
  - Evaluate job\_requisition.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L40) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L957) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L937)

<a id="op-144fc909bd182c"></a>
### Job Opening.get context

`operation_workforce_human_resources_record_definitions_job_opening_business_behavior_job_opening_get_context`

**Inputs** self, context.

**Record and data access** read “Job Applicant” via count.

**Local steps**

- Set context.no\_of\_applications from Platform.db.count(“Job Applicant”, mapping(“job\_title” → self.name)).
- Set context.parents from list(mapping(“route” → “jobs”, “title” → translated “All Jobs”)).
- Set context.posted\_on from pretty\_date(self.posted\_on).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L1031) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L953) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L933)

<a id="op-2aed9d5dd7e973"></a>
### Close expired job openings

`operation_workforce_human_resources_record_definitions_job_opening_business_behavior_close_expired_job_openings`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Job Opening” via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Set today from getdate().
- Set Opening from Platform.qb.DocType(“Job Opening”).
- Set openings from nested operand in the contract(nested operand in the contract).select(Opening.name).where(((nested operand in the contract.status equals “Open” bitwise and nested operand in the contract.isnotnull()) bitwi ….
- For each d in openings.
  - Set doc from Platform.get\_doc(“Job Opening”, d).
  - Set doc.status from “Closed”.
  - Set doc.flags.ignore\_permissions from true.
  - Set doc.flags.ignore\_mandatory from true.
  - Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L1243) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L950) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L930)

<a id="op-8f9d1b47600e53"></a>
### Get data

`operation_workforce_human_resources_record_definitions_job_opening_job_opening_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “job\_title”, “transactions” → list(mapping(“items” → list(“Job Applicant”)))).

**Local steps**

- Return mapping(“fieldname” → “job\_title”, “transactions” → list(mapping(“items” → list(“Job Applicant”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L1612) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L961) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L941)

## Record · Job opening template

[Record definition](../../../../data/record-types/job_opening_template.json)

<a id="op-e3c0950ba38b1f"></a>
### Create job opening from template

`operation_workforce_human_resources_record_definitions_job_opening_template_business_behavior_create_job_opening_from_template`

**Inputs** source.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**State and service calls** request new\_doc for “Job Opening”.

**Explicit results** doc.

**Local steps**

- Set target\_doc from Platform.new\_doc(“Job Opening”).
- Bind local operation set\_missing\_values for subsequent calls.
- Set doc from get\_mapped\_doc(“Job Opening Template”, source, mapping(“Job Opening Template” → mapping(“doctype” → “Job Opening”), “field\_map” → mapping(“name” → “job\_opening\_template”)), target\_doc, …).
- Return doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L3994) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L962) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L942)

<a id="op-3db63693120998"></a>
### Create job opening from template.set missing values

`operation_workforce_human_resources_record_definitions_job_opening_template_business_behavior_create_job_opening_from_template_set_missing_values`

**Inputs** source\_doc, target\_doc.

**Local steps**

- Set target\_doc.job\_title from source\_doc.designation.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L4267) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L963) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L943)

## Record · Job requisition

[Record definition](../../../../data/record-types/job_requisition.json)

<a id="op-e1a8c632e415ec"></a>
### Job Requisition.validate

`operation_workforce_human_resources_record_definitions_job_requisition_business_behavior_job_requisition_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_time\_to\_fill().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set time to fill](operations-023.md#op-69c6b799bb10b3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L4325) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L974) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L954)

<a id="op-69c6b799bb10b3"></a>
### Job Requisition.set time to fill

`operation_workforce_human_resources_record_definitions_job_requisition_business_behavior_job_requisition_set_time_to_fill`

**Inputs** self.

**Local steps**

- If (self.status equals “Filled” and self.completed\_on).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Filled” → self.completed\_on.
  - Set self.time\_to\_fill from time\_diff\_in\_seconds(self.completed\_on, self.posting\_date).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L4376) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L973) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L953)

<a id="op-f4bbf8e19d8ef6"></a>
### Job Requisition.check duplicate job requisition

`operation_workforce_human_resources_record_definitions_job_requisition_business_behavior_job_requisition_check_duplicate_job_requisition`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Job Requisition” via exists.

**Explicit results** Platform.db.exists(“Job Requisition”, mapping(“designation” → self.designation, “department” → self.department, “requested\_by” → self.requested\_by, “status” → tuple(“not in”, list(“Cancelled”, “Filled”)), …)).

**Local steps**

- Return Platform.db.exists(“Job Requisition”, mapping(“designation” → self.designation, “department” → self.department, “requested\_by” → self.requested\_by, “status” → tuple(“not in”, list(“Cancelled”, “Filled”)), …)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L4490) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L972) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L952)

<a id="op-b7bd2e3e3bf779"></a>
### Job Requisition.associate job opening

`operation_workforce_human_resources_record_definitions_job_requisition_business_behavior_job_requisition_associate_job_opening`

**Inputs** self, job\_opening.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**State and service calls** request set\_value on “Job Opening” · msgprint with translated “Job Requisition {0} has been associated with Job Opening {1}”.format(Platform.bold(self.name), get\_link\_to\_form(“Job Opening”, job\_opening)).

**Local steps**

- Evaluate Platform.has\_permission(“Job Opening”, “write”, job\_opening, throw = true).
- Evaluate Platform.db.set\_value(“Job Opening”, job\_opening, mapping(“job\_requisition” → self.name, “vacancies” → self.no\_of\_positions)).
- Evaluate Platform.msgprint(translated “Job Requisition {0} has been associated with Job Opening {1}”.format(Platform.bold(self.name), get\_link\_to\_form(“Job Opening”, job\_opening)), title = translated “Job Opening A ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Opening”, “write”, job\_opening, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L4702) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L971) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L951)

<a id="op-7824557abc1616"></a>
### Make job opening

`operation_workforce_human_resources_record_definitions_job_requisition_business_behavior_make_job_opening`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Explicit results** get\_mapped\_doc(“Job Requisition”, source\_name, mapping(“Job Requisition” → mapping(“doctype” → “Job Opening”), “field\_map” → mapping(“designation” → “designation”, “name” → “job\_requisition”, “department”  ….

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Return get\_mapped\_doc(“Job Requisition”, source\_name, mapping(“Job Requisition” → mapping(“doctype” → “Job Opening”), “field\_map” → mapping(“designation” → “designation”, “name” → “job\_requisition”, “department”  ….

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L5049) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L975) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L955)

<a id="op-47a1b2fe8a8c5b"></a>
### Make job opening.set missing values

`operation_workforce_human_resources_record_definitions_job_requisition_business_behavior_make_job_opening_set_missing_values`

**Inputs** source, target.

**Record and data access** read “Company” via get\_value.

**Local steps**

- Set target.job\_title from source.designation.
- Set target.status from “Open”.
- Set target.currency from Platform.db.get\_value(“Company”, source.company, “default\_currency”).
- Set target.lower\_range from source.expected\_compensation.
- Set target.description from source.description.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L5479) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L976) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L956)

<a id="op-0da168a05a4b16"></a>
### Get avg time to fill

`operation_workforce_human_resources_record_definitions_job_requisition_business_behavior_get_average_time_to_fill`

**Inputs** company = no value, department = no value, designation = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Job Requisition” via get\_list.

**Explicit results** format\_duration(avg\_time\_to\_fill) when avg\_time\_to\_fill, otherwise 0.

**Local steps**

- Set filters from mapping(“status” → “Filled”).
- If company.
  - Set filters at “company” from company.
- If department.
  - Set filters at “department” from department.
- If designation.
  - Set filters at “designation” from designation.
- Set avg\_time\_to\_fill from Platform.db.get\_list(“Job Requisition”, filters = filters, fields = list(mapping(“AVG” → “time\_to\_fill”, “as” → “average\_time”))) at 0.average\_time.
- Return format\_duration(avg\_time\_to\_fill) when avg\_time\_to\_fill, otherwise 0.
  - Value choice on avg\_time\_to\_fill — true gives format\_duration(avg\_time\_to\_fill), false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L5656) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L970) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L950)

## Record · Leave adjustment

[Record definition](../../../../data/record-types/leave_adjustment.json)

<a id="op-3094530aa94488"></a>
### Leave Adjustment.before validate

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_leave_adjustment_before_validate`

**Inputs** self.

**Record and data access** read “System Settings” via get\_single\_value.

**Local steps**

- Set system\_precision from (cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)) or 3).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)) → 3.
- Set precision from (self.precision(“leaves\_to\_adjust”) or system\_precision).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.precision(“leaves\_to\_adjust”) → system\_precision.
- Set self.leaves\_to\_adjust from flt(self.leaves\_to\_adjust, precision).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0040.json#L7170) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L985) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L965)
