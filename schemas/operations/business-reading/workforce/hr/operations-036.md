# Employment and attendance · operations 36

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Recruitment analytics

<a id="op-5b6033fb5307cd"></a>
### Get child row

`operation_workforce_human_resources_report_recruitment_analytics_business_behavior_get_child_row`

**Inputs** jo, jo\_ja\_map, ja\_joff\_map.

**Explicit results** data.

**Local steps**

- Set data from list().
- If jo belongs to jo\_ja\_map.keys().
  - For each ja in jo\_ja\_map at jo.
    - Set row from mapping(“indent” → 1, “job\_applicant” → ja.name, “applicant\_name” → ja.applicant\_name, “application\_status” → ja.status).
    - If ja.name belongs to ja\_joff\_map.keys().
      - Set jo\_detail from ja\_joff\_map at ja.name at 0.
      - Set row at “job\_offer” from jo\_detail.name.
      - Set row at “job\_offer\_status” from jo\_detail.status.
      - Set row at “offer\_date” from jo\_detail.offer\_date.strftime(“%d-%m-%Y”).
      - Set row at “designation” from jo\_detail.designation.
    - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0092.json#L5660) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L82) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L431)

<a id="op-3c72ebb53e12fa"></a>
### Get staffing plan

`operation_workforce_human_resources_report_recruitment_analytics_business_behavior_get_staffing_plan`

**Inputs** filters.

**Explicit results** staffing\_plan.

**Local steps**

- Set StaffingPlan from Platform.qb.DocType(“Staffing Plan”).
- Set StaffingPlanDetail from Platform.qb.DocType(“Staffing Plan Detail”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.to\_date &gt; nested operand in the contract.on\_date).where(StaffingPlan.company equals filters.company).sele ….
- Set staffing\_plan from query.run(as\_dict = true).
- Return staffing\_plan.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0092.json#L6091) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L89) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L438)

<a id="op-74b4adf2fcad0c"></a>
### Get job opening

`operation_workforce_human_resources_report_recruitment_analytics_business_behavior_get_job_opening`

**Inputs** sp\_list, filters.

**Record and data access** read “Job Opening” via get\_all.

**Explicit results** tuple(sp\_jo\_map, jo\_list).

**Local steps**

- Set job\_opening\_filters from list(list(“staffing\_plan”, “IN”, sp\_list), list(“company”, “=”, filters.company)).
- Set job\_openings from Platform.get\_all(“Job Opening”, filters = job\_opening\_filters, fields = list(“name”, “staffing\_plan”)).
- Set sp\_jo\_map from mapping().
- Set jo\_list from list().
- For each openings in job\_openings.
  - If openings.staffing\_plan does not belong to sp\_jo\_map.keys().
    - Set sp\_jo\_map at openings.staffing\_plan from list(openings).
  - Otherwise.
    - Evaluate sp\_jo\_map at openings.staffing\_plan.append(openings).
  - Evaluate jo\_list.append(openings.name).
- Return tuple(sp\_jo\_map, jo\_list).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0092.json#L6470) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L87) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L436)

<a id="op-b50243ed411fe9"></a>
### Get job applicant

`operation_workforce_human_resources_report_recruitment_analytics_business_behavior_get_job_applicant`

**Inputs** jo\_list.

**Record and data access** read “Job Applicant” via get\_all.

**Explicit results** tuple(jo\_ja\_map, ja\_list).

**Local steps**

- Set jo\_ja\_map from mapping().
- Set ja\_list from list().
- Set applicants from Platform.get\_all(“Job Applicant”, filters = list(list(“job\_title”, “IN”, jo\_list)), fields = list(“name”, “job\_title”, “applicant\_name”, “status”)).
- For each applicant in applicants.
  - If applicant.job\_title does not belong to jo\_ja\_map.keys().
    - Set jo\_ja\_map at applicant.job\_title from list(applicant).
  - Otherwise.
    - Evaluate jo\_ja\_map at applicant.job\_title.append(applicant).
  - Evaluate ja\_list.append(applicant.name).
- Return tuple(jo\_ja\_map, ja\_list).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0092.json#L6832) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L85) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L434)

<a id="op-6725a4025f759c"></a>
### Get job offer

`operation_workforce_human_resources_report_recruitment_analytics_business_behavior_get_job_offer`

**Inputs** ja\_list, filters = no value.

**Record and data access** read “Job Offer” via get\_all.

**Explicit results** ja\_joff\_map.

**Local steps**

- Set ja\_joff\_map from mapping().
- Set job\_offer\_filters from list(list(“job\_applicant”, “IN”, ja\_list), list(“company”, “=”, filters.company)).
- Set offers from Platform.get\_all(“Job Offer”, filters = job\_offer\_filters, fields = list(“name”, “job\_applicant”, “status”, “offer\_date”, …)).
- For each offer in offers.
  - If offer.job\_applicant does not belong to ja\_joff\_map.keys().
    - Set ja\_joff\_map at offer.job\_applicant from list(offer).
  - Otherwise.
    - Evaluate ja\_joff\_map at offer.job\_applicant.append(offer).
- Return ja\_joff\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L86) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L435)

## Record · Shift assignment

[Record definition](../../../../data/record-types/shift_assignment.json)

<a id="op-a061724746d69d"></a>
### Shift Assignment.validate

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_shift_assignment_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- If self.end\_date.
  - Evaluate self.validate\_from\_to\_dates(“start\_date”, “end\_date”).
- Evaluate self.validate\_overlapping\_shifts().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overlapping shifts](operations-036.md#op-88b9cf28ac9dd5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L2243) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1449) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L63)

<a id="op-df349ea71b1015"></a>
### Shift Assignment.on update after submit

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_shift_assignment_on_update_after_submit`

**Inputs** self.

**Local steps**

- If self.end\_date.
  - Evaluate self.validate\_from\_to\_dates(“start\_date”, “end\_date”).
- Evaluate self.validate\_overlapping\_shifts().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overlapping shifts](operations-036.md#op-88b9cf28ac9dd5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L2371) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1447) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L61)

<a id="op-1cca632b146e1f"></a>
### Shift Assignment.on cancel

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_shift_assignment_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.validate\_employee\_checkin().
- Evaluate self.validate\_attendance().
- Evaluate self.db\_set(“status”, “Inactive”, update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate employee checkin](operations-036.md#op-bdf01169941f13), [validate attendance](operations-036.md#op-c586b8d0095d1d).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L2474) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1446) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L60)

<a id="op-bdf01169941f13"></a>
### Shift Assignment.validate employee checkin

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_shift_assignment_validate_employee_checkin`

**Inputs** self.

**Record and data access** read “Employee Checkin” via get\_all.

**Explicit failure paths** validation helper — translated “Cannot cancel Shift Assignment: {0} as it is linked to Employee Checkin: {1}”.format(self.name, get\_link\_to\_form(“Employee Checkin”, checkins at 0)).

**Local steps**

- Set checkins from Platform.get\_all(“Employee Checkin”, filters = mapping(“employee” → self.employee, “shift” → self.shift\_type, “time” → list(“between”, list(self.start\_date, self.end\_date))), pluck = “name”).
- If checkins.
  - Call the validation error handler Platform.throw(translated “Cannot cancel Shift Assignment: {0} as it is linked to Employee Checkin: {1}”.format(self.name, get\_link\_to\_form(“Employee Checkin”, checkins at 0))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L2588) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1451) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L65)

<a id="op-c586b8d0095d1d"></a>
### Shift Assignment.validate attendance

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_shift_assignment_validate_attendance`

**Inputs** self.

**Record and data access** read “Attendance” via get\_all.

**Explicit failure paths** validation helper — translated “Cannot cancel Shift Assignment: {0} as it is linked to Attendance: {1}”.format(self.name, get\_link\_to\_form(“Attendance”, attendances at 0)).

**Local steps**

- Set attendances from Platform.get\_all(“Attendance”, filters = mapping(“employee” → self.employee, “shift” → self.shift\_type, “attendance\_date” → list(“between”, list(self.start\_date, self.end\_date))), pluck = “name”).
- If attendances.
  - Call the validation error handler Platform.throw(translated “Cannot cancel Shift Assignment: {0} as it is linked to Attendance: {1}”.format(self.name, get\_link\_to\_form(“Attendance”, attendances at 0))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L2868) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1450) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L64)

<a id="op-88b9cf28ac9dd5"></a>
### Shift Assignment.validate overlapping shifts

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_shift_assignment_validate_overlapping_shifts`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- <a id="op-88b9cf28ac9dd5-guard-2"></a>If self.status equals “Inactive”.
  - Return no value.
- Set overlapping\_dates from self.get\_overlapping\_dates().
- If len(overlapping\_dates).
  - Evaluate self.validate\_same\_date\_multiple\_shifts(overlapping\_dates).
  - For each d in overlapping\_dates.
    - If has\_overlapping\_timings(self.shift\_type, d.shift\_type).
      - Evaluate self.throw\_overlap\_error(d).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Inactive”, self.status = “Inactive” selects the branch that returns no value. With self.status = “Active”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-88b9cf28ac9dd5-guard-2)

**Methods declared on this owner** [get overlapping dates](operations-036.md#op-6ed97be1884e51), [validate same date multiple shifts](operations-036.md#op-a129b0f009935c), [throw overlap error](operations-036.md#op-39973ca747ccdb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L3148) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1452) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L66)

<a id="op-a129b0f009935c"></a>
### Shift Assignment.validate same date multiple shifts

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_shift_assignment_validate_same_date_multiple_shifts`

**Inputs** self, overlapping\_dates.

**Record and data access** read “HR Settings” via get\_single\_value.

**State and service calls** msgprint with translated “Warning: {0} already has an active Shift Assignment {1} for some/all of these dates.”.format(Platform.bold(self.employee), get\_link\_to\_form(“Shift Assignment”, overlapping\_dates at 0.name)).

**Explicit failure paths** validation helper with MultipleShiftError.

**Local steps**

- If cint(Platform.db.get\_single\_value(“HR Settings”, “allow\_multiple\_shift\_assignments”)).
  - If not self.docstatus.
    - Evaluate Platform.msgprint(translated “Warning: {0} already has an active Shift Assignment {1} for some/all of these dates.”.format(Platform.bold(self.employee), get\_link\_to\_form(“Shift Assignment”, overlapping\_dat ….
- Otherwise.
  - Set msg from translated “{0} already has an active Shift Assignment {1} for some/all of these dates.”.format(Platform.bold(self.employee), get\_link\_to\_form(“Shift Assignment”, overlapping\_dates at 0.name)).
  - Update msg using + text in the contract.
  - Update msg using + translated “To allow this, enable {0} under {1}.”.format(Platform.bold(translated “Allow Multiple Shift Assignments for Same Date”), get\_link\_to\_form(“HR Settings”, “HR Settings”)).
  - Call the validation error handler Platform.throw(title = translated “Multiple Shift Assignments”, msg = msg, exc = MultipleShiftError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “allow\_multiple\_shift\_assignments”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L3361) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1453) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L67)

<a id="op-6ed97be1884e51"></a>
### Shift Assignment.get overlapping dates

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_shift_assignment_get_overlapping_dates`

**Inputs** self.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- If not self.name.
  - Set self.name from “New Shift Assignment”.
- Set shift from Platform.qb.DocType(“Shift Assignment”).
- Set query from nested operand in the contract.qb.from\_(shift).select(shift.name, shift.shift\_type, shift.docstatus, shift.status).where(((((nested operand in the contract.employee equals nested operand in the contract.em ….
- If self.end\_date.
  - Set query from query.where(shift.start\_date ≤ self.end\_date).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L3872) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1445) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L59)

<a id="op-39973ca747ccdb"></a>
### Shift Assignment.throw overlap error

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_shift_assignment_throw_overlap_error`

**Inputs** self, shift\_details.

**Explicit failure paths** validation helper with OverlappingShiftError — msg.

**Local steps**

- Set shift\_details from Platform.\_dict(shift\_details).
- If (shift\_details.docstatus equals 1 and shift\_details.status equals “Active”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in shift\_details.docstatus equals 1 → shift\_details.status equals “Active”.
  - Set msg from translated “Employee {0} already has an active Shift {1}: {2} that overlaps within this period.”.format(Platform.bold(self.employee), Platform.bold(shift\_details.shift\_type), get\_link\_to\_form(“Shift Assign ….
  - Call the validation error handler Platform.throw(msg, title = translated “Overlapping Shifts”, exc = OverlappingShiftError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L4317) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1448) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L62)

<a id="op-80248a5a7e7133"></a>
### Has overlapping timings

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_has_overlapping_timings`

**Inputs** shift\_1, shift\_2.

**Declared result** bool.

**Record and data access** read “Shift Type” via get\_value.

**Explicit results** (s1.end\_time &gt; s2.start\_time and s1.start\_time &lt; s2.end\_time).

**Local steps**

- Set s1 from Platform.db.get\_value(“Shift Type”, shift\_1, list(“start\_time”, “end\_time”), as\_dict = true).
- Set s2 from Platform.db.get\_value(“Shift Type”, shift\_2, list(“start\_time”, “end\_time”), as\_dict = true).
- For each d in list(s1, s2).
  - If d.end\_time ≤ d.start\_time.
    - Update d.end\_time using + timedelta(days = 1).
- Return (s1.end\_time &gt; s2.start\_time and s1.start\_time &lt; s2.end\_time).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in s1.end\_time &gt; s2.start\_time → s1.start\_time &lt; s2.end\_time.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L4619) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1439) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L53)

<a id="op-231231d862de7a"></a>
### Get events

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_events`

**Inputs** start, end, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Employee” via get\_value.

**Explicit results** get\_shift\_events(assignments).

**Local steps**

- Set employee from Platform.db.get\_value(“Employee”, mapping(“user\_id” → Platform.session.user), list(“name”, “company”), as\_dict = true).
- If employee.
  - Set employee from employee.name.
- Otherwise.
  - Set employee from empty text.
- Set assignments from get\_shift\_assignments(start, end, filters).
- Return get\_shift\_events(assignments).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L4962) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1426) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L40)

<a id="op-53cfbc9cffdc44"></a>
### Mark expired shift assignments as inactive

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_mark_expired_shift_assignments_as_inactive`

**Inputs** no declared parameters.

**State and service calls** request set\_value on “Shift Assignment”.

**Local steps**

- Set yesterday from add\_days(getdate(), negative 1).
- Set shift\_assignment from Platform.qb.DocType(“Shift Assignment”).
- Set expired\_assignments from nested operand in the contract(nested operand in the contract).select(shift\_assignment.name).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the  ….
- For each assignment in expired\_assignments.
  - Evaluate Platform.db.set\_value(“Shift Assignment”, assignment, “status”, “Inactive”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L5271) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1444) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L58)

<a id="op-f845f8dc42dc28"></a>
### Get shift assignments

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_shift_assignments`

**Inputs** start, end, filters = no value.

**Declared result** list at dict.

**Record and data access** read “Shift Assignment” via get\_list.

**Explicit results** Platform.get\_list(“Shift Assignment”, filters = filters, or\_filters = or\_filters, fields = list(“name”, “start\_date”, “end\_date”, “employee\_name”, …)).

**Local steps**

- Bind dependencies json.
- If isinstance(filters, str).
  - Set filters from json.loads(filters).
- If not filters.
  - Set filters from list().
- Evaluate filters.extend(list(list(“start\_date”, “&lt;=”, end), list(“docstatus”, “=”, 1))).
- Set or\_filters from list(list(“end\_date”, “&gt;=”, start), list(“end\_date”, “is”, “not set”)).
- Return Platform.get\_list(“Shift Assignment”, filters = filters, or\_filters = or\_filters, fields = list(“name”, “start\_date”, “end\_date”, “employee\_name”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L5620) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1429) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L43)

<a id="op-5ffce3dd54c960"></a>
### Get shift events

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_shift_events`

**Inputs** assignments.

**Declared result** list at dict.

**Explicit results** events.

**Local steps**

- Set events from list().
- Set shift\_timing\_map from get\_shift\_type\_timing(list of d.shift\_type for d drawn from assignments).
  - Draw d from assignments.
- For each d in assignments.
  - Set daily\_event\_start from d.start\_date.
  - Set daily\_event\_end from (d.end\_date or getdate()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.end\_date → getdate().
  - Set shift\_start from shift\_timing\_map at d.shift\_type at “start\_time”.
  - Set shift\_end from shift\_timing\_map at d.shift\_type at “end\_time”.
  - Set delta from timedelta(days = 1).
  - While daily\_event\_start ≤ daily\_event\_end.
    - Set start\_timing from (Platform.utils.get\_datetime(daily\_event\_start) + shift\_start).
    - If shift\_start &gt; shift\_end.
      - Set end\_timing from ((Platform.utils.get\_datetime(daily\_event\_start) + shift\_end) + delta).
    - Otherwise.
      - Set end\_timing from (Platform.utils.get\_datetime(daily\_event\_start) + shift\_end).
    - Set event from mapping(“name” → d.name, “doctype” → “Shift Assignment”, “start\_date” → start\_timing, “end\_date” → end\_timing, …).
    - If event does not belong to events.
      - Evaluate events.append(event).
    - Update daily\_event\_start using + delta.
- Return events.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L6054) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1431) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L45)

<a id="op-6d5503c33925c2"></a>
### Get shift type timing

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_shift_type_timing`

**Inputs** shift\_types.

**Record and data access** read “Shift Type” via get\_all.

**Explicit results** shift\_timing\_map.

**Local steps**

- Set shift\_timing\_map from mapping().
- Set data from Platform.get\_all(“Shift Type”, filters = list(list(“name”, “in”, shift\_types)), fields = list(“name”, “start\_time”, “end\_time”)).
- For each d in data.
  - Set shift\_timing\_map at d.name from d.
- Return shift\_timing\_map.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L6787) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1436) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L50)

<a id="op-e4ac8cdde14dab"></a>
### Get valid shifts for time

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_valid_shifts_for_time`

**Inputs** shifts, for\_timestamp.

**Declared result** list at dict.

**Explicit results** valid\_shifts.

**Local steps**

- Set valid\_shifts from list().
- For each assignment in shifts.
  - Set shift\_details from get\_shift\_details(assignment.shift\_type, for\_timestamp = for\_timestamp).
  - Set shift\_details.overtime\_type from (assignment.overtime\_type or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in assignment.overtime\_type → no value.
  - If \_is\_shift\_outside\_assignment\_period(shift\_details, assignment).
    - Continue with the next iteration or loop test.
  - If \_is\_timestamp\_within\_shift(shift\_details, for\_timestamp).
    - Evaluate valid\_shifts.append(shift\_details).
- Evaluate valid\_shifts.sort(key = deferred anonymous expression).
- Evaluate \_adjust\_overlapping\_shifts(valid\_shifts).
- Return valid\_shifts.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1438) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L52)

<a id="op-451061735aaed3"></a>
### Get shift for time

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_shift_for_time`

**Inputs** shifts, for\_timestamp.

**Declared result** dict.

**Explicit results** get\_exact\_shift(get\_valid\_shifts\_for\_time(shifts, for\_timestamp), for\_timestamp).

**Local steps**

- Return get\_exact\_shift(get\_valid\_shifts\_for\_time(shifts, for\_timestamp), for\_timestamp).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L334) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1432) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L46)

<a id="op-6b78fe0fb2d36b"></a>
### Is shift outside assignment period

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_is_shift_outside_assignment_period`

**Inputs** shift\_details, assignment.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- Set is\_midnight\_shift from shift\_details.actual\_start.time() &gt; shift\_details.actual\_end.time().
- If \_is\_shift\_start\_before\_assignment(shift\_details, assignment, is\_midnight\_shift).
  - Return true.
- If (assignment.end\_date and \_is\_shift\_end\_after\_assignment(shift\_details, assignment, is\_midnight\_shift)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in assignment.end\_date → \_is\_shift\_end\_after\_assignment(shift\_details, assignment, is\_midnight\_shift).
  - Return true.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L437) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1441) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L55)

<a id="op-9cee64721be1b6"></a>
### Is shift start before assignment

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_is_shift_start_before_assignment`

**Inputs** shift\_details, assignment, is\_midnight\_shift.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If shift\_details.actual\_start.date() &lt; assignment.start\_date.
  - If not is\_midnight\_shift.
    - Return true.
  - If shift\_details.actual\_start.date() equals shift\_details.start\_datetime.date().
    - Return true.
  - Set prev\_assignment\_day from add\_days(assignment.start\_date, negative 1).
  - If shift\_details.actual\_start.date() differs from prev\_assignment\_day.
    - Return true.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L642) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1442) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L56)
