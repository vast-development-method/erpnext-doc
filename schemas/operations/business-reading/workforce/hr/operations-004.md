# Employment and attendance · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Attendance

[Record definition](../../../../data/record-types/attendance.json)

<a id="op-58c42fcf8ea604"></a>
### Attendance.get overlapping shift attendance

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_get_overlapping_shift_attendance`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping() · d.

**Local steps**

- If not self.shift.
  - Return mapping().
- Set Attendance from Platform.qb.DocType(“Attendance”).
- Set same\_date\_attendance from nested operand in the contract(nested operand in the contract).select(Attendance.name, Attendance.shift).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nes ….
- For each d in same\_date\_attendance.
  - If has\_overlapping\_timings(self.shift, d.shift).
    - Return d.
- Return mapping().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L2609) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L369) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L366)

<a id="op-0a7746d1001f6d"></a>
### Attendance.validate employee status

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_validate_employee_status`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “Cannot mark attendance for an Inactive employee {0}”.format(self.employee).

**Local steps**

- If Platform.db.get\_value(“Employee”, self.employee, “status”) equals “Inactive”.
  - Call the validation error handler Platform.throw(translated “Cannot mark attendance for an Inactive employee {0}”.format(self.employee)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L3003) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L378) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L375)

<a id="op-229f2015e27252"></a>
### Attendance.check leave record

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_check_leave_record`

**Inputs** self.

**State and service calls** msgprint with translated “Employee {0} on Half day on {1}”.format(self.employee, format\_date(self.attendance\_date)) · msgprint with translated “Employee {0} is on Leave on {1}”.format(self.employee, format\_date(self.attendance\_date)) · msgprint with translated “No leave record found for employee {0} on {1}”.format(self.employee, format\_date(self.attendance\_date)).

**Local steps**

- Set LeaveApplication from Platform.qb.DocType(“Leave Application”).
- Set leave\_record from nested operand in the contract(nested operand in the contract).select(LeaveApplication.leave\_type, LeaveApplication.half\_day, LeaveApplication.half\_day\_date, LeaveApplication.name).where(((((nested operand ….
- If leave\_record.
  - For each d in leave\_record.
    - Set self.leave\_type from d.leave\_type.
    - Set self.leave\_application from d.name.
    - If d.half\_day\_date equals getdate(self.attendance\_date).
      - Set self.status from “Half Day”.
      - Evaluate Platform.msgprint(translated “Employee {0} on Half day on {1}”.format(self.employee, format\_date(self.attendance\_date))).
    - Otherwise.
      - Set self.status from “On Leave”.
      - Evaluate Platform.msgprint(translated “Employee {0} is on Leave on {1}”.format(self.employee, format\_date(self.attendance\_date))).
- If self.status belongs to tuple(“On Leave”, “Half Day”).
  - If not leave\_record.
    - Set self.modify\_half\_day\_status from 0.
    - Set self.half\_day\_status from “Absent”.
    - Evaluate Platform.msgprint(translated “No leave record found for employee {0} on {1}”.format(self.employee, format\_date(self.attendance\_date)), alert = 1).
- Otherwise.
  - If self.leave\_type.
    - Set self.leave\_type from no value.
    - Set self.leave\_application from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L3158) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L367) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L364)

<a id="op-9cb8cfa0250469"></a>
### Attendance.validate employee

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_validate_employee`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Employee {0} is not active or does not exist”.format(self.employee).

**Local steps**

- Set Employee from Platform.qb.DocType(“Employee”).
- Set emp from nested operand in the contract(nested operand in the contract).select(Employee.name).where((Employee.name equals self.employee bitwise and Employee.status equals “Active”)).run().
- If not emp.
  - Call the validation error handler Platform.throw(translated “Employee {0} is not active or does not exist”.format(self.employee)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L3992) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L377) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L374)

<a id="op-50887b2705c446"></a>
### Attendance.unlink attendance from checkins

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_unlink_attendance_from_checkins`

**Inputs** self.

**State and service calls** msgprint.

**Local steps**

- Set EmployeeCheckin from Platform.qb.DocType(“Employee Checkin”).
- Set linked\_logs from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.attendance equals nested operand in the contract.name).for\_update().run(as\_dict = true).
- If linked\_logs.
  - Evaluate nested operand in the contract(nested operand in the contract).set(“attendance”, empty text).where(EmployeeCheckin.attendance equals self.name).run().
  - Evaluate Platform.msgprint(msg = translated “Unlinked Attendance record from Employee Checkins: {}”.format(“, ”.join(generator of get\_link\_to\_form(“Employee Checkin”, log.name) for log drawn from linked\_logs)), tit ….
    - Draw log from linked\_logs.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L4263) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L373) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L370)

<a id="op-fed2a386b63772"></a>
### Attendance.on update

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-004.md#op-ed250f3fd575ad).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L4744) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L371) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L368)

<a id="op-1c62f58be4b053"></a>
### Attendance.after delete

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_after_delete`

**Inputs** self.

**Local steps**

- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-004.md#op-ed250f3fd575ad).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L4795) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L365) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L362)

<a id="op-ed250f3fd575ad"></a>
### Attendance.publish update

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_publish_update`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Local steps**

- Set employee\_user from Platform.db.get\_value(“Employee”, self.employee, “user\_id”, cache = true).
- Evaluate Workforce.refetch\_resource(“Workforce:attendance\_calendar\_events”, employee\_user).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L4846) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L372) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L369)

<a id="op-1d5f415e940718"></a>
### Get events

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_get_events`

**Inputs** start, end, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Employee” via get\_value.

**Explicit results** list() · attendance\_records.

**Local steps**

- Set employee from Platform.db.get\_value(“Employee”, mapping(“user\_id” → Platform.session.user)).
- If not employee.
  - Return list().
- If isinstance(filters, str).
  - Bind dependencies json.
  - Set filters from json.loads(filters).
- If not filters.
  - Set filters from list().
- Evaluate filters.append(list(“attendance\_date”, “between”, list(get\_datetime(start).date(), get\_datetime(end).date()))).
- Set attendance\_records from add\_attendance(filters).
- Evaluate add\_holidays(attendance\_records, start, end, employee).
- Return attendance\_records.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L8) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L381) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L378)

<a id="op-04b53a5f7ba981"></a>
### Add attendance

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_add_attendance`

**Inputs** filters.

**Record and data access** read “Attendance” via get\_list.

**Explicit results** attendance.

**Local steps**

- Set attendance from Platform.get\_list(“Attendance”, fields = list(“name”, ValueWrapper(“Attendance”).as\_(“doctype”), “attendance\_date”, “employee\_name”, …), filters = filters).
- For each record in attendance.
  - Set record at “title” from formatted text {record at “employee\_name”} : {record at “status”}.
- Return attendance.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L7) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L363) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L360)

<a id="op-ea616f88a911d3"></a>
### Add holidays

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_add_holidays`

**Inputs** events, start, end, employee = no value.

**Explicit results** no value.

**Local steps**

- Set holidays from get\_holidays\_for\_employee(employee, start, end).
- If not holidays.
  - Return no value.
- For each holiday in holidays.
  - Evaluate events.append(mapping(“doctype” → “Holiday”, “attendance\_date” → holiday.holiday\_date, “title” → ((translated “Holiday” + “: ”) + cstr(holiday.description)), “name” → holiday.name, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L5768) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L364) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L361)

<a id="op-4b6aee988ec197"></a>
### Mark attendance

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_mark_attendance`

**Inputs** employee, attendance\_date, status, shift = no value, leave\_type = no value, late\_entry = false, early\_exit = false, half\_day\_status = no value.

**State and service calls** savepoint savepoint · request new\_doc for “Attendance” · call insert on attendance · call submit on attendance · rollback.

**Explicit results** no value · attendance.name.

**Local steps**

- Set savepoint from “attendance\_creation”.
- Attempt the following.
  - Evaluate Platform.db.savepoint(savepoint).
  - Set attendance from Platform.new\_doc(“Attendance”).
  - Evaluate attendance.update(mapping(“doctype” → “Attendance”, “employee” → employee, “attendance\_date” → attendance\_date, “status” → status, …)).
  - Evaluate attendance.insert().
  - Evaluate attendance.submit().
- On failure (tuple(DuplicateAttendanceError, OverlappingShiftAttendanceError)).
  - Evaluate Platform.db.rollback(save\_point = savepoint).
  - Return no value.
- Return attendance.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L6061) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L383) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L380)

<a id="op-71c6a541303fef"></a>
### Validate employee access

`operation_workforce_binding_workforce_hr_doctype_attendance_attendance_validate_employee_access`

**Inputs** employees, company = no value.

**Declared result** no value.

**Record and data access** read “Employee” via get\_list.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Employee must be a non-empty string.” · validation helper with Platform.PermissionError — translated “You do not have access to Employee {0}”.format(“, ”.join(generator of Platform.bold(e) for e drawn from denied)) · validation helper — translated “Employee {0} does not belong to Company {1}”.format(“, ”.join(generator of Platform.bold(e) for e drawn from mismatched), Platform.bold(company)).

**Local steps**

- If not employees.
  - Return no value.
- If any(generator of (not isinstance(e, str) or not e) for e drawn from employees).
  - Draw e from employees.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(e, str) → not e.
  - Call the validation error handler Platform.throw(translated “Employee must be a non-empty string.”, Platform.ValidationError).
- Set employees from list(dict.fromkeys(employees)).
- Set accessible from Platform.get\_list(“Employee”, filters = mapping(“name” → list(“in”, employees)), fields = list(“name”, “company”), limit = 0).
- Set company\_map from mapping of d.name → d.company for d drawn from accessible.
  - Draw d from accessible.
- If denied bound to list of e for e drawn from employees where e does not belong to company\_map.
  - Draw e from employees, keep a combination only if (e does not belong to company\_map).
  - Call the validation error handler Platform.throw(translated “You do not have access to Employee {0}”.format(“, ”.join(generator of Platform.bold(e) for e drawn from denied)), Platform.PermissionError).
    - Draw e from denied.
- If (company and mismatched bound to list of e for tuple(e, c) drawn from company\_map.items() where c differs from company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → mismatched bound to list of e for tuple(e, c) drawn from company\_map.items() where c differs from company.
  - Draw tuple(e, c) from company\_map.items(), keep a combination only if (c differs from company).
  - Call the validation error handler Platform.throw(translated “Employee {0} does not belong to Company {1}”.format(“, ”.join(generator of Platform.bold(e) for e drawn from mismatched), Platform.bold(company))).
    - Draw e from mismatched.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L41) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L92) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L92)

<a id="op-d223922bd97bc9"></a>
### Mark bulk attendance

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_mark_bulk_attendance`

**Inputs** data.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** enqueue with process\_bulk\_attendance\_in\_batches · msgprint with message · msgprint with translated “Attendance marked successfully.”.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Employee must be a non-empty string.” · validation helper with Platform.ValidationError — translated “Unmarked days must be a list of dates.” · validation helper — translated “Please select a date.”.

**Local steps**

- Bind dependencies json.
- If isinstance(data, str).
  - Set data from json.loads(data).
- Set data from Platform.\_dict(data).
- If (not isinstance(data.employee, str) or not data.employee).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(data.employee, str) → not data.employee.
  - Call the validation error handler Platform.throw(translated “Employee must be a non-empty string.”, Platform.ValidationError).
- If not isinstance(data.unmarked\_days, list).
  - Call the validation error handler Platform.throw(translated “Unmarked days must be a list of dates.”, Platform.ValidationError).
- Evaluate Platform.has\_permission(“Attendance”, “create”, throw = true).
- Evaluate validate\_employee\_access(list(data.employee)).
- If not data.unmarked\_days.
  - Call the validation error handler Platform.throw(translated “Please select a date.”).
  - Return no value.
- If (len(data.unmarked\_days) &gt; 10 or Platform.flags.test\_bg\_job).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(data.unmarked\_days) &gt; 10 → Platform.flags.test\_bg\_job.
  - Set job\_id from formatted text process\_bulk\_attendance\_for\_employee\_{data.employee}.
  - Set job from Platform.enqueue(process\_bulk\_attendance\_in\_batches, data = data, job\_id = job\_id, timeout = 600, deduplicate = true).
  - If job.
    - Set message from translated “Bulk attendance marking is queued with a background job. It may take a while. You can monitor the job status {0}”.format(get\_link\_to\_form(“RQ Job”, job.id, label = “here”)).
  - Otherwise.
    - Set message from translated “Bulk attendance marking is already in progress for employee {0}. You can monitor the job status {1}”.format(Platform.bold(data.employee), get\_link\_to\_form(“RQ Job”, get\_job(job\_id).id, label = “here”)).
  - Evaluate Platform.msgprint(message, allow\_dangerous\_html = true).
- Otherwise.
  - Evaluate process\_bulk\_attendance\_in\_batches(data).
  - Evaluate Platform.msgprint(translated “Attendance marked successfully.”, alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Attendance”, “create”, throw = true) · service or queued work from Platform.enqueue(process\_bulk\_attendance\_in\_batches, data = data, job\_id = job\_id, timeout = 600, deduplicate = true).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L9) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L384) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L381)

<a id="op-8aa793c7b990df"></a>
### Process bulk attendance in batches

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_process_bulk_attendance_in_batches`

**Inputs** data, chunk\_size = 20.

**Record and data access** resolve a document from doc\_dict via get\_doc.

**State and service calls** savepoint savepoint · call insert on Platform.get\_doc(doc\_dict) · call submit on attendance · rollback · commit.

**Local steps**

- Set savepoint from “mark\_bulk\_attendance”.
- For each days in create\_batch(data.unmarked\_days, chunk\_size).
  - For each attendance\_date in days.
    - Attempt the following.
      - Evaluate Platform.db.savepoint(savepoint).
      - Set doc\_dict from mapping(“doctype” → “Attendance”, “employee” → data.employee, “attendance\_date” → getdate(attendance\_date), “status” → data.status, …).
        - Value choice on data.status equals “Half Day” — true gives “Absent”, false gives no value.
      - Set attendance from Platform.get\_doc(doc\_dict).insert().
      - Evaluate attendance.submit().
    - On failure (tuple(DuplicateAttendanceError, OverlappingShiftAttendanceError, Exception)).
      - If not Platform.flags.in\_test.
        - Evaluate Platform.db.rollback(save\_point = savepoint).
      - Continue with the next iteration or loop test.
  - If not Platform.flags.in\_test.
    - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0010.json#L714) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L385) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L382)

<a id="op-8d023c3328b4de"></a>
### Get unmarked days

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_get_unmarked_days`

**Inputs** employee, from\_date, to\_date, exclude\_holidays = 0.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list.

**Record and data access** read “Employee” via get\_cached\_value · read “Attendance” via get\_all.

**Explicit results** unmarked\_days.

**Local steps**

- Evaluate Platform.has\_permission(“Employee”, “read”, employee, throw = true).
- Set tuple(joining\_date, relieving\_date) from Platform.get\_cached\_value(“Employee”, employee, list(“date\_of\_joining”, “relieving\_date”)).
- Set from\_date from max(getdate(from\_date), (joining\_date or getdate(from\_date))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in joining\_date → getdate(from\_date).
- Set to\_date from min(getdate(to\_date), (relieving\_date or getdate(to\_date))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in relieving\_date → getdate(to\_date).
- Set records from Platform.get\_all(“Attendance”, fields = list(“attendance\_date”, “employee”), filters = list(list(“attendance\_date”, “&gt;=”, from\_date), list(“attendance\_date”, “&lt;=”, to\_date), list(“employee”, “=”, employee) ….
- Set marked\_days from list of getdate(record.attendance\_date) for record drawn from records.
  - Draw record from records.
- If cint(exclude\_holidays).
  - Set holiday\_dates from get\_holiday\_dates\_between\_range(employee, from\_date, to\_date, raise\_exception\_for\_holiday\_list = false).
  - Set holidays from list of getdate(record) for record drawn from holiday\_dates.
    - Draw record from holiday\_dates.
  - Evaluate marked\_days.extend(holidays).
- Set unmarked\_days from list().
- While from\_date ≤ to\_date.
  - If from\_date does not belong to marked\_days.
    - Evaluate unmarked\_days.append(from\_date).
  - Set from\_date from add\_days(from\_date, 1).
- Return unmarked\_days.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee, throw = true) · configured or stored value from Platform.get\_cached\_value(“Employee”, employee, list(“date\_of\_joining”, “relieving\_date”)).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0010.json#L1208) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L382) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L379)

<a id="op-9190cf9756a411"></a>
### Get employee shift

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_get_employee_shift`

**Inputs** employee, for\_date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (str bitwise or no value).

**Record and data access** read “Shift Assignment” via get\_all · read “Employee” via get\_value.

**Explicit results** no value · shifts at 0.shift\_type · default\_shift.

**Local steps**

- If not employee.
  - Return no value.
- If (employee and not Platform.has\_permission(“Employee”, “read”, employee)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in employee → not Platform.has\_permission(“Employee”, “read”, employee).
  - Return no value.
- If not for\_date.
  - Set for\_date from nowdate().
- Set for\_date from getdate(for\_date).
- If not Platform.has\_permission(“Shift Assignment”, “read”).
  - Return no value.
- Set shifts from Platform.get\_all(“Shift Assignment”, filters = mapping(“employee” → employee, “docstatus” → 1, “status” → “Active”, “start\_date” → tuple(“&lt;=”, for\_date)), fields = list(“shift\_type”, “start\_date”), order\_b ….
- If shifts.
  - Return shifts at 0.shift\_type.
- Set default\_shift from Platform.db.get\_value(“Employee”, employee, “default\_shift”).
- If default\_shift.
  - Return default\_shift.
- Return no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee), Platform.has\_permission(“Shift Assignment”, “read”) · clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0010.json#L2056) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L380) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L377)

<a id="op-b0cc97a5ad5d53"></a>
### Get data

`operation_workforce_human_resources_record_definitions_attendance_attendance_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “attendance”, “transactions” → list(mapping(“label” → empty text, “items” → list(“Employee Checkin”)))).

**Local steps**

- Return mapping(“fieldname” → “attendance”, “transactions” → list(mapping(“label” → empty text, “items” → list(“Employee Checkin”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0010.json#L2617) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L362) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L359)

## Record · Attendance request

[Record definition](../../../../data/record-types/attendance_request.json)

<a id="op-587034e906a211"></a>
### Attendance Request.validate

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate validate\_dates(self, self.from\_date, self.to\_date, false).
- Evaluate self.validate\_shifts().
- Evaluate self.validate\_half\_day().
- Evaluate self.validate\_request\_overlap().
- Evaluate self.validate\_no\_attendance\_to\_create().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate shifts](operations-004.md#op-e154831bec4d26), [validate half day](operations-004.md#op-3a32443dd45b74), [validate request overlap](operations-005.md#op-228ddfa6e4df3c), [validate no attendance to create](operations-004.md#op-17798ce7100041).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L1490) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L403) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L399)

<a id="op-3a32443dd45b74"></a>
### Attendance Request.validate half day

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_validate_half_day`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Half day date should be in between from date and to date”.

**Local steps**

- If self.half\_day.
  - If not getdate(self.from\_date) ≤ getdate(self.half\_day\_date) ≤ getdate(self.to\_date).
    - Compare adjacent operands in order, stopping at the first false comparison in getdate(self.from\_date) ≤ getdate(self.half\_day\_date) ≤ getdate(self.to\_date).
    - Call the validation error handler Platform.throw(translated “Half day date should be in between from date and to date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L1667) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L404) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L400)

<a id="op-17798ce7100041"></a>
### Attendance Request.validate no attendance to create

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_validate_number_attendance_to_create`

**Inputs** self.

**State and service calls** msgprint.

**Local steps**

- Set attendance\_warnings from self.get\_attendance\_warnings().
- Set attendance\_request\_days from (date\_diff(self.to\_date, self.from\_date) + 1).
- If (len(attendance\_warnings) equals attendance\_request\_days and not any(generator of warning at “action” equals “Overwrite” for warning drawn from attendance\_warnings)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(attendance\_warnings) equals attendance\_request\_days → not any(generator of warning at “action” equals “Overwrite” for warning drawn from attendance\_warnings).
  - Draw warning from attendance\_warnings.
  - Set message\_table from list(list(translated “Date”, translated “Reason”, translated “Action”)).
  - For each warning in attendance\_warnings.
    - Evaluate message\_table.append(list(format\_date(warning at “date”), translated warning at “reason”, translated warning at “action”)).
  - Evaluate Platform.msgprint(title = translated “No attendance records to create due to following reasons”, msg = message\_table, as\_table = true, raise\_exception = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get attendance warnings](operations-005.md#op-2d11fbc4d191ac).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0011.json#L1836) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L405) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L401)

<a id="op-e154831bec4d26"></a>
### Attendance Request.validate shifts

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_validate_shifts`

**Inputs** self.

**State and service calls** msgprint with msg.

**Explicit failure paths** validation helper — translated “There are multiple shifts assigned to the employee for the same period. Please mention the shift” · validation helper — msg.

**Local steps**

- Set tuple(shifts\_by\_date, allowed\_shifts) from self.get\_shifts\_by\_date().
- Set shifts from self.get\_active\_shifts(shifts\_by\_date).
- If not self.shift.
  - If len(shifts) equals 1.
    - Set self.shift from shifts at 0.
  - Otherwise.
    - <a id="op-e154831bec4d26-guard-9"></a>If len(shifts) &gt; 1.
      - Call the validation error handler Platform.throw(translated “There are multiple shifts assigned to the employee for the same period. Please mention the shift”).
- Otherwise.
  - If self.shift does not belong to allowed\_shifts.
    - Set msg from self.get\_unassigned\_shift\_message(allowed\_shifts).
    - If allowed\_shifts.
      - Call the validation error handler Platform.throw(msg, title = translated “Invalid Shift”).
    - Otherwise.
      - <a id="op-e154831bec4d26-guard-19"></a>If self.docstatus equals 0.
        - Evaluate Platform.msgprint(msg, title = translated “Shift Not Assigned”, indicator = “orange”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(shifts) &gt; 1, length of shifts = 2 selects the branch that calls the validation-error handler with translated “There are multiple shifts assigned to the employee for the same period. Please mention the shift”. With length of shifts = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e154831bec4d26-guard-9)
- At the comparison self.docstatus equals 0, self.docstatus = 0 (draft) selects the branch that requests a message with msg. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e154831bec4d26-guard-19)

**Methods declared on this owner** [get shifts by date](operations-005.md#op-5f1356bfcbb55f), [get active shifts](operations-004.md#op-111db7d41a338f), [get unassigned shift message](operations-004.md#op-0657547e19ffb4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L14) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L407) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L403)

<a id="op-0657547e19ffb4"></a>
### Attendance Request.get unassigned shift message

`operation_workforce_binding_workforce_hr_doctype_attendance_request_attendance_request_attendancerequest_get_unassigned_shift_message`

**Inputs** self, shifts.

**Declared result** str.

**Explicit results** ((msg + one space) + translated “Please select {0}.”.format(comma\_or(list of Platform.bold(shift) for shift drawn from sorted(shifts), add\_quotes = false))) · ((msg + one space) + translated “On submission, attendance will be marked under this shift.”).

**Local steps**

- Set msg from translated “Shift {0} is not assigned to Employee {1} for this period.”.format(Platform.bold(self.shift), Platform.bold(self.employee)).
- If shifts.
  - Return ((msg + one space) + translated “Please select {0}.”.format(comma\_or(list of Platform.bold(shift) for shift drawn from sorted(shifts), add\_quotes = false))).
    - Draw shift from sorted(shifts).
- Return ((msg + one space) + translated “On submission, attendance will be marked under this shift.”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L43) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L94) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L94)

<a id="op-111db7d41a338f"></a>
### Attendance Request.get active shifts

`operation_workforce_human_resources_record_definitions_attendance_request_business_behavior_attendance_request_get_active_shifts`

**Inputs** self, shifts\_by\_date.

**Declared result** list at str.

**Explicit results** sorted(set.intersection(expanded dates\_with\_shift)) when dates\_with\_shift, otherwise list().

**Local steps**

- Set dates\_with\_shift from list of shifts for shifts drawn from shifts\_by\_date.values() where shifts.
  - Draw shifts from shifts\_by\_date.values(), keep a combination only if (shifts).
- Return sorted(set.intersection(expanded dates\_with\_shift)) when dates\_with\_shift, otherwise list().
  - Value choice on dates\_with\_shift — true gives sorted(set.intersection(expanded dates\_with\_shift)), false gives list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L11) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L390) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L387)
