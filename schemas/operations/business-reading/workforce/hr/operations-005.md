# Employment and attendance · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Attendance request

[Record definition](../../../../data/record-types/attendance_request.json)

<a id="op-5f1356bfcbb55f"></a>
### Attendance Request.get shifts by date

`operation_workforce_binding_workforce_hr_doctype_attendance_request_attendance_request_attendancerequest_get_shifts_by_date`

**Inputs** self.

**Declared result** tuple at tuple(dict, set).

**Record and data access** read “Shift Assignment” via get\_all · read “Employee” via get\_value.

**Explicit results** tuple(shifts\_by\_date, allowed\_shifts).

**Local steps**

- Set assignments from Platform.get\_all(“Shift Assignment”, filters = mapping(“docstatus” → 1, “employee” → self.employee, “start\_date” → tuple(“&lt;=”, self.to\_date)), or\_filters = list(list(“end\_date”, “&gt;=”, self.from\_date), list ….
- Set default\_shift from Platform.db.get\_value(“Employee”, self.employee, “default\_shift”).
- Set today from getdate().
- Set shifts\_by\_date from mapping().
- Set allowed\_shifts from set(default\_shift) when default\_shift, otherwise set().
  - Value choice on default\_shift — true gives set(default\_shift), false gives set().
- For each day in range((date\_diff(self.to\_date, self.from\_date) + 1)).
  - Set date from getdate(add\_days(self.from\_date, day)).
  - If ((not self.include\_holidays and is\_holiday(self.employee, date)) or self.has\_leave\_record(date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not self.include\_holidays and is\_holiday(self.employee, date)) → self.has\_leave\_record(date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.include\_holidays → is\_holiday(self.employee, date).
    - Continue with the next iteration or loop test.
  - Set assigned from list of assignment for assignment drawn from assignments where (getdate(assignment.start\_date) ≤ date and (not assignment.end\_date or date ≤ getdate(assignment.end\_date))).
    - Draw assignment from assignments, keep a combination only if ((getdate(assignment.start\_date) ≤ date and (not assignment.end\_date or date ≤ getdate(assignment.end\_date)))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(assignment.start\_date) ≤ date → (not assignment.end\_date or date ≤ getdate(assignment.end\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not assignment.end\_date → date ≤ getdate(assignment.end\_date).
  - Set shifts from set of assignment.shift\_type for assignment drawn from assigned where (assignment.status equals “Active” or (assignment.end\_date and getdate(assignment.end\_date) &lt; today)).
    - Draw assignment from assigned, keep a combination only if ((assignment.status equals “Active” or (assignment.end\_date and getdate(assignment.end\_date) &lt; today))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in assignment.status equals “Active” → (assignment.end\_date and getdate(assignment.end\_date) &lt; today).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in assignment.end\_date → getdate(assignment.end\_date) &lt; today.
  - Set shifts\_by\_date at date from (shifts or set(default\_shift) when default\_shift, otherwise set()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in shifts → set(default\_shift) when default\_shift, otherwise set().
    - Value choice on default\_shift — true gives set(default\_shift), false gives set().
  - Evaluate allowed\_shifts.update(generator of assignment.shift\_type for assignment drawn from assigned).
    - Draw assignment from assigned.
- Return tuple(shifts\_by\_date, allowed\_shifts).

**Methods declared on this owner** [has leave record](operations-005.md#op-7cd0775d761560).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L42) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L93) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L93)

<a id="op-228ddfa6e4df3c"></a>
### Attendance Request.validate request overlap

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_validate_request_overlap`

**Inputs** self.

**Local steps**

- If not self.name.
  - Set self.name from “New Attendance Request”.
- Set Request from Platform.qb.DocType(“Attendance Request”).
- Set query from nested operand in the contract.qb.from\_(Request).select(Request.name).where(((((nested operand in the contract.employee equals nested operand in the contract.employee bitwise and nested operand in the cont ….
- If self.shift.
  - Set query from query.where(Request.shift equals self.shift).
- Set overlapping\_request from query.run(as\_dict = true).
- If overlapping\_request.
  - Evaluate self.throw\_overlap\_error(overlapping\_request at 0.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [throw overlap error](operations-005.md#op-d28ea66294214e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L2717) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L406) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L402)

<a id="op-d28ea66294214e"></a>
### Attendance Request.throw overlap error

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_throw_overlap_error`

**Inputs** self, overlapping\_request.

**Explicit failure paths** validation helper with OverlappingAttendanceRequestError — msg.

**Local steps**

- Set msg from translated “Employee {0} already has an Attendance Request {1} that overlaps with this period”.format(Platform.bold(self.employee), get\_link\_to\_form(“Attendance Request”, overlapping\_request)).
- Call the validation error handler Platform.throw(msg, title = translated “Overlapping Attendance Request”, exc = OverlappingAttendanceRequestError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L3174) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L402) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L398)

<a id="op-d901c6538d68cd"></a>
### Attendance Request.onload

`operation_workforce_binding_workforce_hr_doctype_attendance_request_attendance_request_attendancerequest_onload`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.docstatus differs from 0 or not self.shift).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus differs from 0 → not self.shift.
  - Return no value.
- Set allowed\_shifts from self.get\_shifts\_by\_date() at 1.
- If self.shift belongs to allowed\_shifts.
  - Return no value.
- Evaluate self.set\_onload(“shift\_warning”, mapping(“message” → self.get\_unassigned\_shift\_message(allowed\_shifts), “indicator” → “red” when allowed\_shifts, otherwise “orange”)).
  - Value choice on allowed\_shifts — true gives “red”, false gives “orange”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get shifts by date](operations-005.md#op-5f1356bfcbb55f), [get unassigned shift message](operations-004.md#op-0657547e19ffb4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L44) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L95) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L95)

<a id="op-249dbaab411aac"></a>
### Attendance Request.on submit

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.create\_attendance\_records().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create attendance records](operations-005.md#op-015f024c17af69).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L3369) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L397) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L393)

<a id="op-bff7d7a7595be9"></a>
### Attendance Request.on cancel

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_on_cancel`

**Inputs** self.

**Record and data access** read “Attendance” via get\_all · resolve a document from “Attendance” via get\_doc.

**State and service calls** call cancel on attendance\_obj.

**Local steps**

- Set attendance\_list from Platform.get\_all(“Attendance”, mapping(“employee” → self.employee, “attendance\_request” → self.name, “docstatus” → 1)).
- If attendance\_list.
  - For each attendance in attendance\_list.
    - Set attendance\_obj from Platform.get\_doc(“Attendance”, attendance at “name”).
    - Evaluate attendance\_obj.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L3420) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L396) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L392)

<a id="op-015f024c17af69"></a>
### Attendance Request.create attendance records

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_create_attendance_records`

**Inputs** self.

**Local steps**

- Set request\_days from (date\_diff(self.to\_date, self.from\_date) + 1).
- For each day in range(request\_days).
  - Set attendance\_date from add\_days(self.from\_date, day).
  - If self.should\_mark\_attendance(attendance\_date).
    - Evaluate self.create\_or\_update\_attendance(attendance\_date).

If control reaches the end, it returns no value.

**Methods declared on this owner** [should mark attendance](operations-005.md#op-6e784bdb6beb15), [create or update attendance](operations-005.md#op-eabc15c9e0ebda).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L3644) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L388) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L385)

<a id="op-eabc15c9e0ebda"></a>
### Attendance Request.create or update attendance

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_create_or_update_attendance`

**Inputs** self, date.

**State and service calls** call db\_set on doc · msgprint with translated “Updated status from {0} to {1} for date {2} in the attendance record {3}”.format(Platform.bold(old\_status), Platform.bold(status), Platform.bold(format\_date(date)), get\_link\_to\_form(“Attendance … · msgprint with translated “Updated Status for Other Half from {0} to {1} for date {2} in the attendance record {3}”.format(Platform.bold(old\_half\_day\_status), Platform.bold(“Present”), Platform.bold(format\_date(date)), g … · request new\_doc for “Attendance” · call insert on doc · 1 additional forms in the steps below.

**Local steps**

- Set doc from self.get\_attendance\_doc(date).
- Set status from self.get\_attendance\_status(date).
- If doc.
  - Set old\_status from doc.status.
  - Set shift from mapping(“shift” → self.shift) when (self.shift and not doc.shift), otherwise mapping().
    - Value choice on (self.shift and not doc.shift) — true gives mapping(“shift” → self.shift), false gives mapping().
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.shift → not doc.shift.
  - If old\_status differs from status.
    - Evaluate doc.db\_set(mapping(“status” → status, “attendance\_request” → self.name, expand shift)).
    - If status equals “Half Day”.
      - Evaluate doc.db\_set(“half\_day\_status”, “Absent”).
      - Set text from translated “Changed the status from {0} to {1} and Status for Other Half to {2} via Attendance Request”.format(Platform.bold(old\_status), Platform.bold(status), Platform.bold(“Absent”)).
    - Otherwise.
      - Set text from translated “Changed the status from {0} to {1} via Attendance Request”.format(Platform.bold(old\_status), Platform.bold(status)).
    - Evaluate doc.add\_comment(comment\_type = “Info”, text = text).
    - Evaluate Platform.msgprint(translated “Updated status from {0} to {1} for date {2} in the attendance record {3}”.format(Platform.bold(old\_status), Platform.bold(status), Platform.bold(format\_date(date)), get\_link\_t ….
  - Otherwise.
    - If (status equals “Half Day” and doc.half\_day\_status equals “Absent” and self.half\_day).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in status equals “Half Day” → doc.half\_day\_status equals “Absent” → self.half\_day.
      - Set old\_half\_day\_status from doc.half\_day\_status.
      - Evaluate doc.db\_set(mapping(“half\_day\_status” → “Present”, “attendance\_request” → self.name, expand shift)).
      - Set text from translated “Changed the Status for Other Half from {0} to {1} via Attendance Request as the status is Half Day”.format(Platform.bold(old\_half\_day\_status), Platform.bold(“Present”)).
      - Evaluate doc.add\_comment(comment\_type = “Info”, text = text).
      - Evaluate Platform.msgprint(translated “Updated Status for Other Half from {0} to {1} for date {2} in the attendance record {3}”.format(Platform.bold(old\_half\_day\_status), Platform.bold(“Present”), Platform.bold(for ….
- Otherwise.
  - Set doc from Platform.new\_doc(“Attendance”).
  - Set doc.employee from self.employee.
  - Set doc.attendance\_date from date.
  - Set doc.shift from self.shift.
  - Set doc.company from self.company.
  - Set doc.attendance\_request from self.name.
  - Set doc.status from status.
  - Set doc.half\_day\_status from “Absent” when status equals “Half Day”, otherwise no value.
    - Value choice on status equals “Half Day” — true gives “Absent”, false gives no value.
  - Evaluate doc.insert(ignore\_permissions = true).
  - Evaluate doc.submit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get attendance doc](operations-005.md#op-f2b71fa573d05e), [get attendance status](operations-005.md#op-104bbf07798daf).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L10) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L389) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L386)

<a id="op-6e784bdb6beb15"></a>
### Attendance Request.should mark attendance

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_should_mark_attendance`

**Inputs** self, attendance\_date.

**Declared result** bool.

**State and service calls** msgprint with translated “Attendance not submitted for {0} as it is a Holiday.”.format(Platform.bold(format\_date(attendance\_date))) · msgprint with translated “Attendance not submitted for {0} as {1} is on leave.”.format(Platform.bold(format\_date(attendance\_date)), Platform.bold(self.employee)).

**Explicit results** false · true.

**Local steps**

- If (not self.include\_holidays and is\_holiday(self.employee, attendance\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.include\_holidays → is\_holiday(self.employee, attendance\_date).
  - Evaluate Platform.msgprint(translated “Attendance not submitted for {0} as it is a Holiday.”.format(Platform.bold(format\_date(attendance\_date)))).
  - Return false.
- If self.has\_leave\_record(attendance\_date).
  - Evaluate Platform.msgprint(translated “Attendance not submitted for {0} as {1} is on leave.”.format(Platform.bold(format\_date(attendance\_date)), Platform.bold(self.employee))).
  - Return false.
- Return true.

**Methods declared on this owner** [has leave record](operations-005.md#op-7cd0775d761560).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L5181) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L400) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L396)

<a id="op-7cd0775d761560"></a>
### Attendance Request.has leave record

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_has_leave_record`

**Inputs** self, attendance\_date.

**Declared result** (str bitwise or no value).

**Record and data access** read “Leave Application” via get\_all.

**Explicit results** leaves at 0.name when leaves, otherwise no value.

**Local steps**

- Set leaves from Platform.get\_all(“Leave Application”, filters = mapping(“employee” → self.employee, “docstatus” → 1, “from\_date” → tuple(“&lt;=”, attendance\_date), “to\_date” → tuple(“&gt;=”, attendance\_date), …), fields = list( ….
- If (self.half\_day and self.half\_day\_date and getdate(self.half\_day\_date) equals getdate(attendance\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.half\_day → self.half\_day\_date → getdate(self.half\_day\_date) equals getdate(attendance\_date).
  - Set half\_day\_leaves from list of leave for leave drawn from leaves where (leave.half\_day and leave.half\_day\_date and getdate(leave.half\_day\_date) equals getdate(attendance\_date)).
    - Draw leave from leaves, keep a combination only if ((leave.half\_day and leave.half\_day\_date and getdate(leave.half\_day\_date) equals getdate(attendance\_date))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in leave.half\_day → leave.half\_day\_date → getdate(leave.half\_day\_date) equals getdate(attendance\_date).
  - If len(half\_day\_leaves) equals 1.
    - Evaluate leaves.remove(half\_day\_leaves at 0).
- Return leaves at 0.name when leaves, otherwise no value.
  - Value choice on leaves — true gives leaves at 0.name, false gives no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L13) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L395) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L391)

<a id="op-f2b71fa573d05e"></a>
### Attendance Request.get attendance doc

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_get_attendance_record`

**Inputs** self, attendance\_date.

**Declared result** (str bitwise or no value).

**Record and data access** read “Attendance” via get\_all · resolve a document from “Attendance” via get\_doc.

**Explicit results** Platform.get\_doc(“Attendance”, attendance at 0) when attendance, otherwise no value.

**Local steps**

- Set shift\_filters from list(list(“shift”, “is”, “not set”)).
- If self.shift.
  - Evaluate shift\_filters.append(list(“shift”, “=”, self.shift)).
- Set attendance from Platform.get\_all(“Attendance”, filters = mapping(“employee” → self.employee, “attendance\_date” → attendance\_date, “docstatus” → tuple(“!=”, 2)), or\_filters = shift\_filters, pluck = “name”, limit = 1).
- Return Platform.get\_doc(“Attendance”, attendance at 0) when attendance, otherwise no value.
  - Value choice on attendance — true gives Platform.get\_doc(“Attendance”, attendance at 0), false gives no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L12) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L391) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L388)

<a id="op-104bbf07798daf"></a>
### Attendance Request.get attendance status

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_get_attendance_status`

**Inputs** self, attendance\_date.

**Declared result** str.

**Explicit results** “Half Day” · “Work From Home” · “Present”.

**Local steps**

- If (self.half\_day and date\_diff(getdate(self.half\_day\_date), getdate(attendance\_date)) equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.half\_day → date\_diff(getdate(self.half\_day\_date), getdate(attendance\_date)) equals 0.
  - Return “Half Day”.
- Otherwise.
  - <a id="op-104bbf07798daf-guard-4"></a>If self.reason equals “Work From Home”.
    - Return “Work From Home”.
  - Otherwise.
    - Return “Present”.

**Derived branch illustrations**

- At the comparison self.reason equals “Work From Home”, self.reason = “Work From Home” selects the branch that returns “Work From Home”. With self.reason = “On Duty”, the alternative returns “Present”. [Local guard](#op-104bbf07798daf-guard-4)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L6219) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L392) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L389)

<a id="op-13c681d23aec21"></a>
### Attendance Request.status unchanged

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_status_unchanged`

**Inputs** self, attendance\_date.

**Explicit results** false · true.

**Local steps**

- Set new\_status from self.get\_attendance\_status(attendance\_date).
- Set attendance\_doc from self.get\_attendance\_doc(attendance\_date).
- If (attendance\_doc and attendance\_doc.status equals new\_status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in attendance\_doc → attendance\_doc.status equals new\_status.
  - If (new\_status equals “Half Day” and self.half\_day and attendance\_doc.half\_day\_status equals “Absent”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_status equals “Half Day” → self.half\_day → attendance\_doc.half\_day\_status equals “Absent”.
    - Return false.
  - Return true.
- Return false.

**Methods declared on this owner** [get attendance status](operations-005.md#op-104bbf07798daf), [get attendance doc](operations-005.md#op-f2b71fa573d05e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L6398) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L401) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L397)

<a id="op-0b7829cc2f8e0d"></a>
### Attendance Request.on update

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-005.md#op-e3f0cee09da102).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L6611) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L398) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L394)

<a id="op-8f376fb018dc5a"></a>
### Attendance Request.after delete

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_after_delete`

**Inputs** self.

**Local steps**

- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-005.md#op-e3f0cee09da102).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L6662) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L387) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L384)

<a id="op-e3f0cee09da102"></a>
### Attendance Request.publish update

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_publish_update`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Local steps**

- Set employee\_user from Platform.db.get\_value(“Employee”, self.employee, “user\_id”, cache = true).
- Evaluate Workforce.refetch\_resource(“Workforce:my\_attendance\_requests”, employee\_user).
- Evaluate Workforce.refetch\_resource(“Workforce:team\_attendance\_requests”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L6713) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L399) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L395)

<a id="op-2d11fbc4d191ac"></a>
### Attendance Request.get attendance warnings

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_get_attendance_warnings`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list.

**Explicit results** attendance\_warnings.

**Local steps**

- Set attendance\_warnings from list().
- Set request\_days from (date\_diff(self.to\_date, self.from\_date) + 1).
- For each day in range(request\_days).
  - Set attendance\_date from add\_days(self.from\_date, day).
  - If (not self.include\_holidays and is\_holiday(self.employee, attendance\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.include\_holidays → is\_holiday(self.employee, attendance\_date).
    - Evaluate attendance\_warnings.append(mapping(“date” → attendance\_date, “reason” → “Holiday”, “action” → “Skip”)).
  - Otherwise.
    - If self.has\_leave\_record(attendance\_date).
      - Evaluate attendance\_warnings.append(mapping(“date” → attendance\_date, “reason” → “On Leave”, “action” → “Skip”)).
    - Otherwise.
      - If self.status\_unchanged(attendance\_date).
        - Evaluate attendance\_warnings.append(mapping(“date” → attendance\_date, “reason” → “Attendance status unchanged”, “action” → “Skip”)).
      - Otherwise.
        - Set attendance from self.get\_attendance\_doc(attendance\_date).
        - If attendance.
          - Evaluate attendance\_warnings.append(mapping(“date” → attendance\_date, “reason” → “Attendance already marked”, “record” → attendance.name, “action” → “Overwrite”)).
- Return attendance\_warnings.

**Methods declared on this owner** [has leave record](operations-005.md#op-7cd0775d761560), [status unchanged](operations-005.md#op-13c681d23aec21), [get attendance doc](operations-005.md#op-f2b71fa573d05e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0012.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L393) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L390)

<a id="op-114cceac586dbf"></a>
### Get data

`operation_workforce_human_resources_record_definitions_attendance_request_attendance_request_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “attendance\_request”, “transactions” → list(mapping(“items” → list(“Attendance”)))).

**Local steps**

- Return mapping(“fieldname” → “attendance\_request”, “transactions” → list(mapping(“items” → list(“Attendance”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0012.json#L644) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L386) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L383)

## Record · Bank details change request

<a id="op-44dbaac1e1c15e"></a>
### Bank Details Change Request.validate

`operation_workforce_binding_workforce_hr_doctype_bank_details_change_request_bank_details_change_request_bankdetailschangerequest_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate self.validate\_status\_change().
- Evaluate self.validate\_open\_request().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate status change](operations-005.md#op-4188cbc9536cc5), [validate open request](operations-005.md#op-b3654fdc31f765).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L49) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L100) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L100)

<a id="op-4188cbc9536cc5"></a>
### Bank Details Change Request.validate status change

`operation_workforce_binding_workforce_hr_doctype_bank_details_change_request_bank_details_change_request_bankdetailschangerequest_validate_status_change`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Set the status to Open, or discard the request to cancel it” · validation helper — translated “Give a rejection reason, so {0} knows what to do next”.format(Platform.bold((self.employee\_name or self.employee))) · validation helper with Platform.PermissionError — translated “Only HR can approve or reject a Bank Details Change Request”.

**Local steps**

- <a id="op-4188cbc9536cc5-guard-3"></a>If self.status equals “Cancelled”.
  - Call the validation error handler Platform.throw(translated “Set the status to Open, or discard the request to cancel it”).
- If (self.status equals “Rejected” and not (self.rejection\_reason or empty text).strip()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Rejected” → not (self.rejection\_reason or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.rejection\_reason → empty text.
  - Call the validation error handler Platform.throw(translated “Give a rejection reason, so {0} knows what to do next”.format(Platform.bold((self.employee\_name or self.employee))), title = translated “Rejection Reason Missing”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.employee\_name → self.employee.
- If (self.status belongs to tuple(“Approved”, “Rejected”) and not Platform.has\_permission(self.doctype, “submit”, self)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status belongs to tuple(“Approved”, “Rejected”) → not Platform.has\_permission(self.doctype, “submit”, self).
  - Call the validation error handler Platform.throw(translated “Only HR can approve or reject a Bank Details Change Request”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Cancelled”, self.status = “Cancelled” selects the branch that calls the validation-error handler with translated “Set the status to Open, or discard the request to cancel it”. With self.status = “Open”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-4188cbc9536cc5-guard-3)

**Values supplied outside this operation** effective access from Platform.has\_permission(self.doctype, “submit”, self).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L51) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L102) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L102)

<a id="op-b3654fdc31f765"></a>
### Bank Details Change Request.validate open request

`operation_workforce_binding_workforce_hr_doctype_bank_details_change_request_bank_details_change_request_bankdetailschangerequest_validate_open_request`

**Inputs** self.

**Record and data access** read self.doctype via exists.

**Explicit failure paths** validation helper — translated “{0} already has an open request {1}”.format(Platform.bold((self.employee\_name or self.employee)), get\_link\_to\_form(self.doctype, open\_request)).

**Local steps**

- Set open\_request from Platform.db.exists(self.doctype, mapping(“employee” → self.employee, “docstatus” → 0, “name” → list(“!=”, (self.name or empty text)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → empty text.
- If open\_request.
  - Call the validation error handler Platform.throw(translated “{0} already has an open request {1}”.format(Platform.bold((self.employee\_name or self.employee)), get\_link\_to\_form(self.doctype, open\_request)), title = translated “Open Request Exists”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.employee\_name → self.employee.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L50) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L101) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L101)

<a id="op-84644345354b1f"></a>
### Bank Details Change Request.after insert

`operation_workforce_binding_workforce_hr_doctype_bank_details_change_request_bank_details_change_request_bankdetailschangerequest_after_insert`

**Inputs** self.

**Local steps**

- Evaluate notify\_hr(self, translated “{0} asked to change their salary account”.format(escape\_html(self.employee\_name)), formatted text &lt;p&gt;{translated “New bank”}: {escape\_html((self.bank\_name or “-”))}&lt;/p&gt;&lt;p&gt;{trans ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.bank\_name → “-”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.reason → “-”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L45) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L96) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L96)

<a id="op-6e22f52fc7c15a"></a>
### Bank Details Change Request.on discard

`operation_workforce_binding_workforce_hr_doctype_bank_details_change_request_bank_details_change_request_bankdetailschangerequest_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L46) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L97) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L97)

<a id="op-27131087f69c5b"></a>
### Bank Details Change Request.on submit

`operation_workforce_binding_workforce_hr_doctype_bank_details_change_request_bank_details_change_request_bankdetailschangerequest_on_submit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Approve or reject the request before submitting it”.

**Local steps**

- <a id="op-27131087f69c5b-guard-2"></a>If self.status does not belong to tuple(“Approved”, “Rejected”).
  - Call the validation error handler Platform.throw(translated “Approve or reject the request before submitting it”).
- If self.status equals “Approved”.
  - Evaluate self.update\_employee().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status does not belong to tuple(“Approved”, “Rejected”), self.status = “Open” selects the branch that calls the validation-error handler with translated “Approve or reject the request before submitting it”. With self.status = “Approved”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-27131087f69c5b-guard-2)

**Methods declared on this owner** [update employee](operations-006.md#op-ec088aacbc1f40).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L47) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L98) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L98)
