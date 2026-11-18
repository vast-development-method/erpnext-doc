# Employment and attendance · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Interview feedback

[Record definition](../../../../data/record-types/interview_feedback.json)

<a id="op-2c62b03df86de0"></a>
### Get applicable interviewers

`operation_workforce_human_resources_record_definitions_interview_feedback_business_behavior_get_applicable_interviewers`

**Inputs** interview.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Record and data access** read “Interview Detail” via get\_all.

**Explicit results** Platform.get\_all(“Interview Detail”, filters = mapping(“parent” → interview), pluck = “interviewer”).

**Local steps**

- Evaluate Platform.has\_permission(“Interview”, “read”, interview, throw = true).
- Return Platform.get\_all(“Interview Detail”, filters = mapping(“parent” → interview), pluck = “interviewer”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Interview”, “read”, interview, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L3677) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L878) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L858)

## Record · Interview round

<a id="op-a775702c27dcb7"></a>
### Create interview

`operation_workforce_binding_workforce_hr_doctype_interview_round_interview_round_create_interview`

**Inputs** interview\_round.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Record and data access** resolve a document from “Interview Round” via get\_doc.

**State and service calls** request new\_doc for “Interview”.

**Explicit results** interview.

**Local steps**

- Set doc from Platform.get\_doc(“Interview Round”, interview\_round).
- Set interview from Platform.new\_doc(“Interview”).
- Set interview.interview\_round from doc.name.
- Set interview.designation from doc.designation.
- If doc.interviewers.
  - Set interview.interview\_details from list().
  - For each d in doc.interviewers.
    - Evaluate interview.append(“interview\_details”, mapping(“interviewer” → d.user)).
- Return interview.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L63) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L114) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L114)

## Record · Interview type

[Record definition](../../../../data/record-types/interview_type.json)

<a id="op-aa3b6f34d503b1"></a>
### Create interview

`operation_workforce_human_resources_record_definitions_interview_type_business_behavior_create_interview`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** Document.

**Record and data access** resolve a document from “Interview Type” via get\_doc.

**State and service calls** request new\_doc for “Interview”.

**Explicit results** interview.

**Local steps**

- Evaluate Platform.has\_permission(“Interview”, ptype = “create”, throw = true).
- Evaluate Platform.has\_permission(“Interview Type”, ptype = “read”, doc = docname, throw = true).
- Set interview\_type from Platform.get\_doc(“Interview Type”, docname).
- Set interview from Platform.new\_doc(“Interview”).
- Set interview.interview\_type from interview\_type.name.
- Set interview.designation from interview\_type.designation.
- If interview\_type.interviewers.
  - Set interview.interview\_details from list().
  - For each d in interview\_type.interviewers.
    - Evaluate interview.append(“interview\_details”, mapping(“interviewer” → d.user)).
- Return interview.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Interview”, ptype = “create”, throw = true), Platform.has\_permission(“Interview Type”, ptype = “read”, doc = docname, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L36) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L905) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L885)

## Record · Job applicant

[Record definition](../../../../data/record-types/job_applicant.json)

<a id="op-06f09698e901a6"></a>
### Job Applicant.onload

`operation_workforce_human_resources_record_definitions_job_applicant_business_behavior_job_applicant_onload`

**Inputs** self.

**Record and data access** read “Job Offer” via get\_all · read “Employee” via get\_value.

**Local steps**

- Set job\_offer from Platform.get\_all(“Job Offer”, filters = mapping(“job\_applicant” → self.name, “docstatus” → list(“!=”, 2))).
- If job\_offer.
  - Evaluate self.set\_onload(“job\_offer”, job\_offer at 0.name).
- Set employee from (Platform.db.get\_value(“Employee”, mapping(“job\_applicant” → self.name), “name”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Employee”, mapping(“job\_applicant” → self.name), “name”) → empty text.
- Evaluate self.set\_onload(“employee”, employee).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L5566) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L912) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L892)

<a id="op-eec426275b6dea"></a>
### Job Applicant.autoname

`operation_workforce_human_resources_record_definitions_job_applicant_business_behavior_job_applicant_autoname`

**Inputs** self.

**Record and data access** read “Job Applicant” via exists.

**Local steps**

- Set self.name from self.email\_id.
- If Platform.db.exists(“Job Applicant”, self.name).
  - Set self.name from append\_number\_if\_name\_exists(“Job Applicant”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L5862) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L910) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L890)

<a id="op-7a9a6ad047b753"></a>
### Job Applicant.validate

`operation_workforce_human_resources_record_definitions_job_applicant_business_behavior_job_applicant_validate`

**Inputs** self.

**Local steps**

- If self.email\_id.
  - Evaluate validate\_email\_address(self.email\_id, true).
- If self.employee\_referral.
  - Evaluate self.set\_status\_for\_employee\_referral().
- If (not self.applicant\_name and self.email\_id).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.applicant\_name → self.email\_id.
  - Set guess from self.email\_id.split(“@”) at 0.
  - Set self.applicant\_name from one space.join(list of p.capitalize() for p drawn from guess.split(“.”)).
    - Draw p from guess.split(“.”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status for employee referral](operations-021.md#op-3161f9f5b3ec39).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L6010) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L914) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L894)

<a id="op-59667c695a7942"></a>
### Job Applicant.before insert

`operation_workforce_human_resources_record_definitions_job_applicant_business_behavior_job_applicant_before_insert`

**Inputs** self.

**Record and data access** read “Job Opening” via get\_value · read “Job Applicant” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot create a Job Applicant against a closed Job Opening” · validation helper with DuplicationError — translated “You have already applied for this position.”.

**Local steps**

- If self.job\_title.
  - Set job\_opening from Platform.db.get\_value(“Job Opening”, self.job\_title, list(“status”, “prevent\_duplicate\_applicant”), as\_dict = true).
  - If not job\_opening.
    - Return no value.
  - If job\_opening.status equals “Closed”.
    - Call the validation error handler Platform.throw(translated “Cannot create a Job Applicant against a closed Job Opening”, title = translated “Not Allowed”).
  - If (job\_opening.prevent\_duplicate\_applicant and self.email\_id).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in job\_opening.prevent\_duplicate\_applicant → self.email\_id.
    - If Platform.db.exists(“Job Applicant”, mapping(“email\_id” → self.email\_id, “job\_title” → self.job\_title)).
      - Call the validation error handler Platform.throw(translated “You have already applied for this position.”, exc = DuplicationError, title = translated “Duplicate Application”).
- If (Platform.flags.in\_web\_form and not self.source).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.in\_web\_form → not self.source.
  - Set self.source from “Website Listing”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L6269) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L911) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L891)

<a id="op-3161f9f5b3ec39"></a>
### Job Applicant.set status for employee referral

`operation_workforce_human_resources_record_definitions_job_applicant_business_behavior_job_applicant_set_status_for_employee_referral`

**Inputs** self.

**Record and data access** resolve a document from “Employee Referral” via get\_doc.

**State and service calls** call db\_set on emp\_ref.

**Local steps**

- Set emp\_ref from Platform.get\_doc(“Employee Referral”, self.employee\_referral).
- If self.status belongs to list(“Open”, “Replied”, “Hold”).
  - Evaluate emp\_ref.db\_set(“status”, “In Process”).
- Otherwise.
  - If self.status belongs to list(“Accepted”, “Rejected”).
    - Evaluate emp\_ref.db\_set(“status”, self.status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L6735) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L913) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L893)

<a id="op-892ac71bc7ff56"></a>
### Make employee

`operation_workforce_human_resources_record_definitions_job_applicant_business_behavior_make_employee`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Explicit results** get\_mapped\_doc(“Job Applicant”, source\_name, mapping(“Job Applicant” → mapping(“doctype” → “Employee”, “field\_map” → mapping(“applicant\_name” → “first\_name”, “email\_id” → “personal\_email”, “phone\_number” → ….

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Return get\_mapped\_doc(“Job Applicant”, source\_name, mapping(“Job Applicant” → mapping(“doctype” → “Employee”, “field\_map” → mapping(“applicant\_name” → “first\_name”, “email\_id” → “personal\_email”, “phone\_number” → ….

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L915) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L895)

<a id="op-3ef52627c34bfb"></a>
### Make employee.set missing values

`operation_workforce_human_resources_record_definitions_job_applicant_business_behavior_make_employee_set_missing_values`

**Inputs** source, target.

**Record and data access** read “Job Opening” via get\_value.

**Explicit results** no value.

**Local steps**

- Set target.employee\_name from source.applicant\_name.
- If not source.job\_title.
  - Return no value.
- Set job\_opening from Platform.db.get\_value(“Job Opening”, source.job\_title, list(“company”, “department”, “employment\_type”), as\_dict = true).
- If not job\_opening.
  - Return no value.
- If job\_opening.company.
  - Set target.company from job\_opening.company.
- If job\_opening.department.
  - Set target.department from job\_opening.department.
- If job\_opening.employment\_type.
  - Set target.employment\_type from job\_opening.employment\_type.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L576) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L916) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L896)

<a id="op-c26a0e02af3e52"></a>
### Create kanban board

`operation_workforce_human_resources_record_definitions_job_applicant_business_behavior_create_kanban_board`

**Inputs** board\_name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Record and data access** read “Kanban Board” via exists · resolve a document from “Kanban Board” via get\_doc.

**State and service calls** request new\_doc for “Kanban Board” · call insert on board.

**Explicit results** Platform.get\_doc(“Kanban Board”, board\_name).as\_dict() · board.as\_dict().

**Local steps**

- Evaluate Platform.has\_permission(“Job Applicant”, throw = true).
- If Platform.db.exists(“Kanban Board”, board\_name).
  - Return Platform.get\_doc(“Kanban Board”, board\_name).as\_dict().
- Set board from Platform.new\_doc(“Kanban Board”).
- Set board.kanban\_board\_name from board\_name.
- Set board.reference\_doctype from “Job Applicant”.
- Set board.field\_name from “status”.
- Set board.private from 0.
- Set board.fields from json.dumps(list(“designation”, “applicant\_rating”)).
- Set board.show\_labels from 1.
- For each col in KANBAN\_COLUMNS.
  - Evaluate board.append(“columns”, mapping(“column\_name” → col at “column\_name”, “indicator” → col.get(“indicator”, empty text), “status” → “Active”)).
- Evaluate board.insert(ignore\_permissions = true).
- Return board.as\_dict().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Applicant”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L872) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L907) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L887)

<a id="op-8305e55234c8e3"></a>
### Create interview

`operation_workforce_human_resources_record_definitions_job_applicant_business_behavior_create_interview`

**Inputs** job\_applicant, interview\_type.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** Document.

**Record and data access** resolve a document from “Job Applicant” via get\_doc · read “Interview Type” via get\_value.

**State and service calls** request new\_doc for “Interview”.

**Explicit results** interview.

**Explicit failure paths** validation helper — translated “Interview Type {0} is only applicable for the Designation {1}”.format(interview\_type, round\_designation).

**Local steps**

- Evaluate Platform.has\_permission(“Interview”, ptype = “create”, throw = true).
- Evaluate Platform.has\_permission(“Job Applicant”, ptype = “read”, doc = job\_applicant, throw = true).
- Set doc from Platform.get\_doc(“Job Applicant”, job\_applicant).
- Set round\_designation from Platform.db.get\_value(“Interview Type”, interview\_type, “designation”).
- If (round\_designation and doc.designation and round\_designation differs from doc.designation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in round\_designation → doc.designation → round\_designation differs from doc.designation.
  - Call the validation error handler Platform.throw(translated “Interview Type {0} is only applicable for the Designation {1}”.format(interview\_type, round\_designation)).
- Set interview from Platform.new\_doc(“Interview”).
- Set interview.interview\_type from interview\_type.
- Set interview.job\_applicant from doc.name.
- Set interview.designation from doc.designation.
- Set interview.resume\_link from doc.resume\_link.
- Set interview.job\_opening from doc.job\_title.
- Set interviewers from get\_interviewers(interview\_type).
- For each d in interviewers.
  - Evaluate interview.append(“interview\_details”, mapping(“interviewer” → d.interviewer)).
- Return interview.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Interview”, ptype = “create”, throw = true), Platform.has\_permission(“Job Applicant”, ptype = “read”, doc = job\_applicant, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L37) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L906) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L886)

<a id="op-5ff31a0c349401"></a>
### Schedule interview

`operation_workforce_human_resources_record_definitions_job_applicant_business_behavior_schedule_interview`

**Inputs** job\_applicant, interview\_type, scheduled\_on, from\_time = no value, to\_time = no value, interviewers = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** str.

**Record and data access** resolve a document from “Job Applicant” via get\_doc · read “Interview Type” via get\_value.

**State and service calls** request new\_doc for “Interview” · call insert on interview.

**Explicit results** interview.name.

**Explicit failure paths** validation helper — translated “Interview Type {0} is only applicable for Designation {1}”.format(Platform.bold(interview\_type), Platform.bold(round\_designation)).

**Local steps**

- Evaluate Platform.has\_permission(“Interview”, ptype = “create”, throw = true).
- Evaluate Platform.has\_permission(“Job Applicant”, ptype = “read”, doc = job\_applicant, throw = true).
- Set applicant from Platform.get\_doc(“Job Applicant”, job\_applicant).
- Set round\_designation from Platform.db.get\_value(“Interview Type”, interview\_type, “designation”).
- If (round\_designation and applicant.designation and round\_designation differs from applicant.designation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in round\_designation → applicant.designation → round\_designation differs from applicant.designation.
  - Call the validation error handler Platform.throw(translated “Interview Type {0} is only applicable for Designation {1}”.format(Platform.bold(interview\_type), Platform.bold(round\_designation))).
- Set interview from Platform.new\_doc(“Interview”).
- Set interview.interview\_type from interview\_type.
- Set interview.job\_applicant from applicant.name.
- Set interview.designation from applicant.designation.
- Set interview.resume\_link from applicant.resume\_link.
- Set interview.job\_opening from applicant.job\_title.
- Set interview.scheduled\_on from scheduled\_on.
- Set interview.from\_time from from\_time.
- Set interview.to\_time from to\_time.
- If isinstance(interviewers, str).
  - Set interviewers from json.loads(interviewers).
- For each entry in (interviewers or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in interviewers → list().
  - If entry.get(“interviewer”).
    - Evaluate interview.append(“interview\_details”, mapping(“interviewer” → entry at “interviewer”)).
- Evaluate interview.insert(ignore\_permissions = true).
- Return interview.name.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Interview”, ptype = “create”, throw = true), Platform.has\_permission(“Job Applicant”, ptype = “read”, doc = job\_applicant, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L1928) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L917) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L897)

<a id="op-3298451fc2be92"></a>
### Get interview details

`operation_workforce_human_resources_record_definitions_job_applicant_business_behavior_get_interview_details`

**Inputs** job\_applicant.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Interview” via get\_all.

**Explicit results** no value · mapping(“interviews” → interview\_detail\_map, “stars” → number\_of\_stars).

**Local steps**

- Evaluate Platform.has\_permission(“Job Applicant”, “read”, job\_applicant, throw = true).
- Set interview\_details from Platform.db.get\_all(“Interview”, filters = mapping(“job\_applicant” → job\_applicant, “docstatus” → list(“!=”, 2)), fields = list(“name”, “interview\_type”, “scheduled\_on”, “average\_rating”, …)).
- If not interview\_details.
  - Return no value.
- Set interview\_detail\_map from mapping().
- Set meta from Platform.get\_meta(“Interview”).
- Set number\_of\_stars from (meta.get\_options(“average\_rating”) or 5).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.get\_options(“average\_rating”) → 5.
- For each detail in interview\_details.
  - Set detail.average\_rating from (detail.average\_rating × number\_of\_stars) when detail.average\_rating, otherwise 0.
    - Value choice on detail.average\_rating — true gives (detail.average\_rating × number\_of\_stars), false gives 0.
  - Set interview\_detail\_map at detail.name from detail.
- Return mapping(“interviews” → interview\_detail\_map, “stars” → number\_of\_stars).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Applicant”, “read”, job\_applicant, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L2853) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L909) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L889)

<a id="op-35a625a8f0aed8"></a>
### Get applicant to hire percentage

`operation_workforce_human_resources_record_definitions_job_applicant_business_behavior_get_applicant_to_hire_percentage`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Job Applicant” via count.

**Explicit results** mapping(“value” → ((flt(total\_hired) ÷ flt(total\_applicants)) × 100) when total\_applicants, otherwise 0, “fieldtype” → “Percent”).

**Local steps**

- Evaluate Platform.has\_permission(“Job Applicant”, throw = true).
- Set total\_applicants from Platform.db.count(“Job Applicant”).
- Set total\_hired from Platform.db.count(“Job Applicant”, filters = mapping(“status” → “Accepted”)).
- Return mapping(“value” → ((flt(total\_hired) ÷ flt(total\_applicants)) × 100) when total\_applicants, otherwise 0, “fieldtype” → “Percent”).
  - Value choice on total\_applicants — true gives ((flt(total\_hired) ÷ flt(total\_applicants)) × 100), false gives 0.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Applicant”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L3335) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L908) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L888)

<a id="op-02226dda8d0f6e"></a>
### Get data

`operation_workforce_human_resources_record_definitions_job_applicant_job_applicant_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “job\_applicant”, “transactions” → list(mapping(“items” → list(“Employee”, “Employee Onboarding”)), mapping(“items” → list(“Job Offer”)), mapping(“items” → list(“Interview”)))).

**Local steps**

- Return mapping(“fieldname” → “job\_applicant”, “transactions” → list(mapping(“items” → list(“Employee”, “Employee Onboarding”)), mapping(“items” → list(“Job Offer”)), mapping(“items” → list(“Interview”)))).

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L38) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L918) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L898)

## Service · Job application

<a id="op-90eeefbcc3bcf4"></a>
### Get context

`operation_workforce_human_resources_web_form_job_application_business_behavior_get_context`

**Inputs** context.

**Record and data access** read “Job Opening” via get\_value.

**Explicit results** no value.

**Local steps**

- Set job\_opening from Platform.form\_dict.job\_title.
- If (not job\_opening or not isinstance(job\_opening, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not job\_opening → not isinstance(job\_opening, str).
  - Return no value.
- Set context.web\_form\_doc.job\_opening\_title from Platform.db.get\_value(“Job Opening”, mapping(“name” → job\_opening, “publish” → 1), “job\_title”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L87) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L177) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L526)

## Record · Job offer

[Record definition](../../../../data/record-types/job_offer.json)

<a id="op-3bc6398168a8f5"></a>
### Job Offer.onload

`operation_workforce_human_resources_record_definitions_job_offer_business_behavior_job_offer_onload`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Local steps**

- Set employee from (Platform.db.get\_value(“Employee”, mapping(“job\_offer” → self.name), “name”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Employee”, mapping(“job\_offer” → self.name), “name”) → empty text.
- Evaluate self.set\_onload(“employee”, employee).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0038.json#L5480) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L928) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L908)

<a id="op-07b5bef88deafe"></a>
### Job Offer.validate

`operation_workforce_human_resources_record_definitions_job_offer_business_behavior_job_offer_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status().
- Evaluate self.validate\_vacancies().
- Evaluate self.validate\_duplicate\_job\_offer().
- Evaluate self.set\_compensation().
- Evaluate self.set\_leave\_details().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-021.md#op-2e91cddee7b1d0), [validate vacancies](operations-022.md#op-d266fd1390f97c), [validate duplicate job offer](operations-022.md#op-d32a1914e8aea1), [set compensation](operations-022.md#op-138b65c5b06d29), [set leave details](operations-021.md#op-cbfa9cf3976e2f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L39) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L929) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L909)

<a id="op-2e91cddee7b1d0"></a>
### Job Offer.set status

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_joboffer_set_status`

**Inputs** self.

**Local steps**

- If (self.docstatus equals 0 and self.status belongs to tuple(no value, empty text, “Ready to Send”, “Awaiting Response”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 0 → self.status belongs to tuple(no value, empty text, “Ready to Send”, “Awaiting Response”).
  - Set self.status from “Draft”.
- Otherwise.
  - If (self.docstatus equals 1 and self.status belongs to tuple(no value, empty text, “Draft”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → self.status belongs to tuple(no value, empty text, “Draft”).
    - Set self.status from “Ready to Send”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L81) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L132) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L132)

<a id="op-2b9f22edcc653b"></a>
### Job Offer.on communication update

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_joboffer_on_communication_update`

**Inputs** self, communication.

**State and service calls** call db\_set on self.

**Local steps**

- If (self.docstatus equals 1 and self.status equals “Ready to Send” and communication.communication\_type equals “Communication” and communication.sent\_or\_received equals “Sent” and self.is\_addressed\_to\_applica ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → self.status equals “Ready to Send” → communication.communication\_type equals “Communication” → communication.sent\_or\_received equals “Sent” → self.is\_addressed\_to\_applicant(communication).
  - Evaluate self.db\_set(“status”, “Awaiting Response”).
- Evaluate update\_parent\_document\_on\_communication(communication).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is addressed to applicant](operations-021.md#op-aa7f57abe0a97a).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L78) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L129) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L129)

<a id="op-aa7f57abe0a97a"></a>
### Job Offer.is addressed to applicant

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_joboffer_is_addressed_to_applicant`

**Inputs** self, communication.

**Declared result** bool.

**Explicit results** (self.applicant\_email or empty text).lower() belongs to recipients.

**Local steps**

- Set recipients from set of parse\_addr(email) at 1.lower() for email drawn from split\_emails((communication.recipients or empty text)).
  - Draw email from split\_emails((communication.recipients or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in communication.recipients → empty text.
- Return (self.applicant\_email or empty text).lower() belongs to recipients.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.applicant\_email → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L77) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L128) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L128)

<a id="op-cbfa9cf3976e2f"></a>
### Job Offer.set leave details

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_joboffer_set_leave_details`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Evaluate self.set(“leave\_allocations”, get\_leave\_allocations(self.leave\_policy)).
- If not self.holiday\_list\_changed().
  - Return no value.
- Set summary from get\_holiday\_summary(self.holiday\_list).
- Set self.weekly\_off\_days from summary at “weekly\_off\_days”.
- Set self.total\_public\_holidays from summary at “total\_public\_holidays”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [holiday list changed](operations-021.md#op-9b9980bfc30021).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L80) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L131) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L131)

<a id="op-9b9980bfc30021"></a>
### Job Offer.holiday list changed

`operation_workforce_binding_workforce_hr_doctype_job_offer_job_offer_joboffer_holiday_list_changed`

**Inputs** self.

**Declared result** bool.

**Explicit results** (not previous or previous.holiday\_list differs from self.holiday\_list).

**Local steps**

- Set previous from self.doc\_before\_save().
- Return (not previous or previous.holiday\_list differs from self.holiday\_list).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not previous → previous.holiday\_list differs from self.holiday\_list.

**Methods declared on this owner** [doc before save](operations-022.md#op-fed3df8ef76c73).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L76) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L127) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L127)
