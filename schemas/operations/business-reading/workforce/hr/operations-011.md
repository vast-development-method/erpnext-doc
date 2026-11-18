# Employment and attendance · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Employee onboarding

[Record definition](../../../../data/record-types/employee_onboarding.json)

<a id="op-585233c5e91342"></a>
### Employee Onboarding.set employee

`operation_workforce_human_resources_record_definitions_employee_onboarding_business_behavior_employee_onboarding_set_employee`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Local steps**

- If not self.employee.
  - Set self.employee from Platform.db.get\_value(“Employee”, mapping(“job\_offer” → self.job\_offer), “name”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0023.json#L5785) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L605) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L585)

<a id="op-1a78489534abbf"></a>
### Employee Onboarding.validate duplicate employee onboarding

`operation_workforce_human_resources_record_definitions_employee_onboarding_business_behavior_employee_onboarding_validate_duplicate_employee_onboarding`

**Inputs** self.

**Record and data access** read “Employee Onboarding” via exists.

**Explicit failure paths** validation helper — translated “Employee Onboarding: {0} already exists for Job Offer: {1}”.format(Platform.bold(emp\_onboarding), Platform.bold(self.job\_offer)).

**Local steps**

- Set emp\_onboarding from Platform.db.exists(“Employee Onboarding”, mapping(“job\_offer” → self.job\_offer, “docstatus” → tuple(“!=”, 2))).
- If (emp\_onboarding and emp\_onboarding differs from self.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in emp\_onboarding → emp\_onboarding differs from self.name.
  - Call the validation error handler Platform.throw(translated “Employee Onboarding: {0} already exists for Job Offer: {1}”.format(Platform.bold(emp\_onboarding), Platform.bold(self.job\_offer))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0023.json#L5910) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L607) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L587)

<a id="op-49361b686d2713"></a>
### Employee Onboarding.validate employee creation

`operation_workforce_human_resources_record_definitions_employee_onboarding_business_behavior_employee_onboarding_validate_employee_creation`

**Inputs** self.

**Record and data access** read “Task” via get\_value.

**Explicit failure paths** validation helper — translated “Submit this to create the Employee record” · validation helper with IncompleteTaskError — translated “All the mandatory tasks for employee creation are not completed yet.”.

**Local steps**

- If self.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Submit this to create the Employee record”).
- Otherwise.
  - For each activity in self.activities.
    - If not activity.required\_for\_employee\_creation.
      - Continue with the next iteration or loop test.
    - Otherwise.
      - Set task\_status from Platform.db.get\_value(“Task”, activity.task, “status”).
      - If task\_status does not belong to list(“Completed”, “Cancelled”).
        - Call the validation error handler Platform.throw(translated “All the mandatory tasks for employee creation are not completed yet.”, IncompleteTaskError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0023.json#L6166) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L608) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L588)

<a id="op-3304213ef5a173"></a>
### Employee Onboarding.on submit

`operation_workforce_human_resources_record_definitions_employee_onboarding_business_behavior_employee_onboarding_on_submit`

**Inputs** self.

**Local steps**

- Evaluate super().on\_submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0023.json#L6432) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L603) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L583)

<a id="op-9628770713e0be"></a>
### Employee Onboarding.on update after submit

`operation_workforce_human_resources_record_definitions_employee_onboarding_business_behavior_employee_onboarding_on_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.create\_task\_and\_notify\_user().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0023.json#L6488) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L604) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L584)

<a id="op-070c466b514f85"></a>
### Employee Onboarding.on cancel

`operation_workforce_human_resources_record_definitions_employee_onboarding_business_behavior_employee_onboarding_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate super().on\_cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0023.json#L6537) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L602) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L582)

<a id="op-bd4c0be627260f"></a>
### Employee Onboarding.mark onboarding as completed

`operation_workforce_human_resources_record_definitions_employee_onboarding_business_behavior_employee_onboarding_mark_onboarding_as_completed`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** request set\_value on “Task” · request set\_value on “Project” · call save on self.

**Local steps**

- Evaluate self.check\_permission(“write”).
- For each activity in self.activities.
  - Evaluate Platform.db.set\_value(“Task”, activity.task, “status”, “Completed”).
- Evaluate Platform.db.set\_value(“Project”, self.project, “status”, “Completed”).
- Set self.boarding\_status from “Completed”.
- Evaluate self.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0023.json#L6593) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L601) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L581)

<a id="op-e2db14843d6859"></a>
### Make employee

`operation_workforce_human_resources_record_definitions_employee_onboarding_business_behavior_make_employee`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Record and data access** resolve a document from “Employee Onboarding” via get\_doc.

**Explicit results** doc.

**Local steps**

- Set doc from Platform.get\_doc(“Employee Onboarding”, source\_name).
- Evaluate doc.validate\_employee\_creation().
- Bind local operation set\_missing\_values for subsequent calls.
- Set doc from get\_mapped\_doc(“Employee Onboarding”, source\_name, mapping(“Employee Onboarding” → mapping(“doctype” → “Employee”, “field\_map” → mapping(“first\_name” → “employee\_name”, “employee\_grade” → “grade”))), target\_doc, …).
- Return doc.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L609) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L589)

<a id="op-d4e89ddf77ae80"></a>
### Make employee.set missing values

`operation_workforce_human_resources_record_definitions_employee_onboarding_business_behavior_make_employee_set_missing_values`

**Inputs** source, target.

**Record and data access** read “Job Offer” via get\_value.

**Local steps**

- Set target.personal\_email from Platform.db.get\_value(“Job Offer”, source.job\_offer, “applicant\_email”).
- Set target.job\_offer from source.job\_offer.
- Set target.status from “Active”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L421) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L610) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L590)

## Record · Employee onboarding template

[Record definition](../../../../data/record-types/employee_onboarding_template.json)

<a id="op-d0e53fed89aae5"></a>
### Get data

`operation_workforce_human_resources_record_definitions_employee_onboarding_template_employee_onboarding_template_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “employee\_onboarding\_template”, “transactions” → list(mapping(“items” → list(“Employee Onboarding”)))).

**Local steps**

- Return mapping(“fieldname” → “employee\_onboarding\_template”, “transactions” → list(mapping(“items” → list(“Employee Onboarding”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L3189) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L611) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L591)

## Record · Employee performance feedback

[Record definition](../../../../data/record-types/employee_performance_feedback.json)

<a id="op-6d8d695e83e76d"></a>
### Employee Performance Feedback.validate

`operation_workforce_human_resources_record_definitions_employee_performance_feedback_business_behavior_employee_performance_feedback_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_appraisal\_cycle(self.appraisal\_cycle).
- Evaluate self.validate\_employee().
- Evaluate self.validate\_appraisal().
- Evaluate self.validate\_total\_weightage(“feedback\_ratings”, “Feedback Ratings”).
- Evaluate self.set\_total\_score().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate employee](operations-011.md#op-3e34f31e37d38f), [validate appraisal](operations-011.md#op-f66eb37e967cd5), [set total score](operations-011.md#op-5acc649e182333).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L3283) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L623) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L603)

<a id="op-ee31164d849a47"></a>
### Employee Performance Feedback.on submit

`operation_workforce_human_resources_record_definitions_employee_performance_feedback_business_behavior_employee_performance_feedback_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_avg\_feedback\_score\_in\_appraisal().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update avg feedback score in appraisal](operations-011.md#op-260f22f2637fce).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L3432) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L619) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L599)

<a id="op-6c034f174c3efc"></a>
### Employee Performance Feedback.on cancel

`operation_workforce_human_resources_record_definitions_employee_performance_feedback_business_behavior_employee_performance_feedback_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_avg\_feedback\_score\_in\_appraisal().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update avg feedback score in appraisal](operations-011.md#op-260f22f2637fce).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L3483) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L618) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L598)

<a id="op-3e34f31e37d38f"></a>
### Employee Performance Feedback.validate employee

`operation_workforce_human_resources_record_definitions_employee_performance_feedback_business_behavior_employee_performance_feedback_validate_employee`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Employees cannot give feedback to themselves. Use {0} instead: {1}”.format(Platform.bold(translated “Self Appraisal”), get\_link\_to\_form(“Appraisal”, self.appraisal)).

**Local steps**

- If self.employee equals self.reviewer.
  - Call the validation error handler Platform.throw(translated “Employees cannot give feedback to themselves. Use {0} instead: {1}”.format(Platform.bold(translated “Self Appraisal”), get\_link\_to\_form(“Appraisal”, self.appraisal))).
- Evaluate validate\_active\_employee(self.employee).
- Evaluate validate\_active\_employee(self.reviewer).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L3534) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L625) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L605)

<a id="op-f66eb37e967cd5"></a>
### Employee Performance Feedback.validate appraisal

`operation_workforce_human_resources_record_definitions_employee_performance_feedback_business_behavior_employee_performance_feedback_validate_appraisal`

**Inputs** self.

**Record and data access** read “Appraisal” via get\_value.

**Explicit failure paths** validation helper — translated “Appraisal {0} does not belong to Employee {1}”.format(self.appraisal, self.employee).

**Local steps**

- Set employee from Platform.db.get\_value(“Appraisal”, self.appraisal, “employee”).
- If employee differs from self.employee.
  - Call the validation error handler Platform.throw(translated “Appraisal {0} does not belong to Employee {1}”.format(self.appraisal, self.employee)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L3762) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L624) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L604)

<a id="op-5acc649e182333"></a>
### Employee Performance Feedback.set total score

`operation_workforce_human_resources_record_definitions_employee_performance_feedback_business_behavior_employee_performance_feedback_set_total_score`

**Inputs** self.

**Local steps**

- Set total from 0.
- For each entry in self.feedback\_ratings.
  - Set score from ((flt(entry.rating) × 5) × flt((entry.per\_weightage ÷ 100))).
  - Update total using + flt(score).
- Set self.total\_score from flt(total, self.precision(“total\_score”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L3942) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L621) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L601)

<a id="op-260f22f2637fce"></a>
### Employee Performance Feedback.update avg feedback score in appraisal

`operation_workforce_human_resources_record_definitions_employee_performance_feedback_business_behavior_employee_performance_feedback_update_average_feedback_score_in_appraisal`

**Inputs** self.

**Record and data access** resolve a document from “Appraisal” via get\_doc.

**Explicit results** no value.

**Local steps**

- If not self.appraisal.
  - Return no value.
- Set appraisal from Platform.get\_doc(“Appraisal”, self.appraisal).
- Evaluate appraisal.calculate\_avg\_feedback\_score(update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L4151) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L622) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L602)

<a id="op-5044a3fe0d0624"></a>
### Employee Performance Feedback.set feedback criteria

`operation_workforce_human_resources_record_definitions_employee_performance_feedback_business_behavior_employee_performance_feedback_set_feedback_criteria`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Appraisal” via get\_value · resolve a document from “Appraisal Template” via get\_doc.

**Explicit results** no value · self.

**Local steps**

- If not self.appraisal.
  - Return no value.
- Set template from Platform.db.get\_value(“Appraisal”, self.appraisal, “appraisal\_template”).
- Set template from Platform.get\_doc(“Appraisal Template”, template).
- Evaluate self.set(“feedback\_ratings”, list()).
- For each entry in template.rating\_criteria.
  - Evaluate self.append(“feedback\_ratings”, mapping(“criteria” → entry.criteria, “per\_weightage” → entry.per\_weightage)).
- Return self.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0024.json#L4276) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L620) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L600)

## Workspace · Employee profile

<a id="op-56b7d413306ad7"></a>
### Get profile

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_profile`

**Inputs** employee = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** profile.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You do not have an employee record” · validation helper — translated “Employee {0} not found”.format(Platform.bold(employee)).

**Local steps**

- Set employee from (employee or get\_user\_employee()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee → get\_user\_employee().
- If not employee.
  - Call the validation error handler Platform.throw(translated “You do not have an employee record”, Platform.PermissionError).
- Set person from get\_person(employee).
- If not person.
  - Call the validation error handler Platform.throw(translated “Employee {0} not found”.format(Platform.bold(employee))).
- Set private from Platform.has\_permission(“Employee”, “read”, doc = employee).
- If not private.
  - Evaluate check\_access(person).
- Set is\_self from (bool(person.user\_id) and person.user\_id equals Platform.session.user).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(person.user\_id) → person.user\_id equals Platform.session.user.
- Set can\_manage from false.
- If private.
  - Set can\_manage from Platform.has\_permission(“Employee”, “write”, doc = employee).
- Set profile from mapping(“card” → get\_card(person, private), “sections” → get\_sections(employee), “is\_self” → is\_self, “can\_edit” → is\_self, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_self → can\_manage.
- If private.
  - Set profile at “private” from get\_private(employee).
  - Set profile at “can\_review” from dict.fromkeys(REQUESTS, false).
  - Set profile at “can\_assign\_assets” from false.
  - If not is\_self.
    - For each doctype in REQUESTS.
      - Set profile at “can\_review” at doctype from Platform.has\_permission(doctype, “submit”).
    - Set profile at “can\_assign\_assets” from Platform.has\_permission(“Asset Movement”, “create”).
- If (is\_self or can\_manage).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_self → can\_manage.
  - Set profile at “options” from get\_options(person.company, can\_manage).
- Return profile.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, doc = employee), Platform.has\_permission(“Employee”, “write”, doc = employee) and 2 further calls.

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L112) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L163) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L163)

<a id="op-eed7f77ab4ebaf"></a>
### Get person

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_person`

**Inputs** employee.

**Declared result** (Platform.\_dict bitwise or no value).

**Record and data access** read “Employee” via get\_all.

**Explicit results** person at 0 when person, otherwise no value.

**Local steps**

- Set person from Platform.get\_all(“Employee”, filters = mapping(“name” → employee), fields = CARD\_FIELDS, limit = 1).
- Return person at 0 when person, otherwise no value.
  - Value choice on person — true gives person at 0, false gives no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L110) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L161) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L161)

<a id="op-98273d6adb04da"></a>
### Get options

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_options`

**Inputs** company, can\_manage.

**Declared result** dict.

**Record and data access** read “Gender” via get\_all · read “Asset Category” via get\_all · read “Employee Document Type” via get\_all · read meta.get\_field(field).options via get\_all · read “Department” via get\_all.

**Explicit results** options.

**Local steps**

- Set meta from Platform.get\_meta(“Employee”).
- Set options from mapping of field → list of option for option drawn from (nested operand in the contract(nested operand in the contract).options or empty text).split(whitespace '\\n') where option for field drawn from tuple ….
  - Draw field from tuple(“blood\_group”, “marital\_status”).
  - Draw option from (meta.get\_field(field).options or empty text).split(whitespace '\\n'), keep a combination only if (option).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.get\_field(field).options → empty text.
- Set options at “gender” from Platform.get\_all(“Gender”, pluck = “name”, order\_by = “name”).
- Set options at “asset\_categories” from Platform.get\_all(“Asset Category”, pluck = “name”, order\_by = “name”).
- Set options at “document\_types” from Platform.get\_all(“Employee Document Type”, fields = list(“name”, “has\_number”, “has\_expiry”), order\_by = “name”).
- If can\_manage.
  - For each field in tuple(“branch”, “employment\_type”, “grade”, “default\_shift”).
    - Set options at field from Platform.get\_all(meta.get\_field(field).options, pluck = “name”, order\_by = “name”, limit = MAX\_OPTIONS).
  - Set options at “department” from Platform.get\_all(“Department”, filters = mapping(“company” → company, “is\_group” → 0), fields = list(“name as value”, “department\_name as label”), order\_by = “department\_name”, limit = MAX\_OPTIONS).
- Return options.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L106) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L157) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L157)

<a id="op-fc3f549a62ba40"></a>
### Check access

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_check_access`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** person.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L91) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L142) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L142)

<a id="op-ad242619ea0335"></a>
### Get card

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_card`

**Inputs** person, private.

**Declared result** dict.

**Record and data access** read “Employee” via get\_value · read “Employee” via count · read “HR Settings” via get\_single\_value.

**Explicit results** mapping(“id” → person.name, “name” → person.employee\_name, “image” → person.image, “designation” → person.designation, …).

**Local steps**

- Set manager from Platform.db.get\_value(“Employee”, mapping(“name” → person.reports\_to, “status” → “Active”), list(“name as id”, “employee\_name as name”, “image”), as\_dict = true) when person.reports\_to, otherwise no value.
  - Value choice on person.reports\_to — true gives Platform.db.get\_value(“Employee”, mapping(“name” → person.reports\_to, “status” → “Active”), list(“name as id”, “employee\_name as name”, “image”), as\_dict = true), false gives no value.
- Return mapping(“id” → person.name, “name” → person.employee\_name, “image” → person.image, “designation” → person.designation, …).
  - Value choice on (private or cint(Platform.db.get\_single\_value(“HR Settings”, “send\_birthday\_reminders”))) — true gives get\_birthday(person.date\_of\_birth), false gives no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in private → cint(Platform.db.get\_single\_value(“HR Settings”, “send\_birthday\_reminders”)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “send\_birthday\_reminders”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L101) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L152) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L152)

<a id="op-038ff43a72d597"></a>
### Get tenure

`operation_workforce_binding_workforce_hr_page_employee_profile_employee_profile_get_tenure`

**Inputs** date\_of\_joining.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · mapping(“years” → (months floor divide 12)) · mapping(“months” → max(months, 0), “days” → date\_diff(getdate(), date\_of\_joining)).

**Local steps**

- If (not date\_of\_joining or getdate(date\_of\_joining) &gt; getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not date\_of\_joining → getdate(date\_of\_joining) &gt; getdate().
  - Return no value.
- Set months from (month\_diff(getdate(), date\_of\_joining) − 1).
- If months ≥ 12.
  - Return mapping(“years” → (months floor divide 12)).
- Return mapping(“months” → max(months, 0), “days” → date\_diff(getdate(), date\_of\_joining)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L115) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L166) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L166)
