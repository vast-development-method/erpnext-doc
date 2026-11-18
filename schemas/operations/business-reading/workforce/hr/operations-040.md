# Employment and attendance · operations 40

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Shift type

[Record definition](../../../../data/record-types/shift_type.json)

<a id="op-d1ba1cae8d9adf"></a>
### Shift Type.process auto attendance

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_process_auto_attendance`

**Inputs** self, is\_manually\_triggered = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** (no value bitwise or str).

**State and service calls** enqueue with self.\_process.

**Explicit results** no value · translated “Attendance marking has been queued. It may take a few minutes. You can monitor the job status {0}”.format(get\_link\_to\_form(“RQ Job”, job.id, label = translated “here”)) · translated “Attendance has been marked as per employee check-ins.” · translated “An error occurred during marking attendance. Refer the full error log {0}”.format(get\_link\_to\_form(“Error Log”, error\_log.name, label = translated “here”)).

**Local steps**

- Evaluate self.check\_permission(“write”).
- If self.has\_incorrect\_shift\_config().
  - Return no value.
- Set logs from self.get\_employee\_checkins().
- If is\_manually\_triggered.
  - If (len(logs) &gt; 1000 or Platform.flags.test\_bg\_job).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(logs) &gt; 1000 → Platform.flags.test\_bg\_job.
    - Set job\_id from (“process\_auto\_attendance\_” + self.name).
    - Set job from Platform.enqueue(self.\_process, logs = logs, timeout = 1200, job\_id = job\_id, deduplicate = true).
    - Return translated “Attendance marking has been queued. It may take a few minutes. You can monitor the job status {0}”.format(get\_link\_to\_form(“RQ Job”, job.id, label = translated “here”)).
  - Otherwise.
    - Attempt the following.
      - Evaluate self.\_process(logs).
      - Return translated “Attendance has been marked as per employee check-ins.”.
    - On failure (Exception) bound to e.
      - Set error\_log from Platform.log\_error(e).
      - Return translated “An error occurred during marking attendance. Refer the full error log {0}”.format(get\_link\_to\_form(“Error Log”, error\_log.name, label = translated “here”)).
- Otherwise.
  - Evaluate self.\_process(logs).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has incorrect shift config](operations-040.md#op-2cc2b9340889e5), [get employee checkins](operations-040.md#op-c9a0fc76d1da82), [process](operations-040.md#op-5b6ed05d1ded43).

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · service or queued work from Platform.enqueue(self.\_process, logs = logs, timeout = 1200, job\_id = job\_id, deduplicate = true).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L70) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1542) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L155)

<a id="op-2cc2b9340889e5"></a>
### Shift Type.has incorrect shift config

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_has_incorrect_shift_configuration`

**Inputs** self.

**Explicit results** (not cint(self.enable\_auto\_attendance) or not self.process\_attendance\_after or not self.last\_sync\_of\_checkin).

**Local steps**

- Return (not cint(self.enable\_auto\_attendance) or not self.process\_attendance\_after or not self.last\_sync\_of\_checkin).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not cint(self.enable\_auto\_attendance) → not self.process\_attendance\_after → not self.last\_sync\_of\_checkin.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L3085) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1536) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L149)

<a id="op-5b6ed05d1ded43"></a>
### Shift Type.process

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_process`

**Inputs** self, logs.

**State and service calls** commit.

**Local steps**

- Set group\_key from deferred anonymous expression.
- For each tuple(key, group) in groupby(sorted(logs, key = group\_key), key = group\_key).
  - Set single\_shift\_logs from list(group).
  - Set attendance\_date from key at 1.date().
  - Set employee from key at 0.
  - If not self.should\_mark\_attendance(employee, attendance\_date).
    - Continue with the next iteration or loop test.
  - Set working\_hours\_threshold\_for\_half\_day from flt(self.working\_hours\_threshold\_for\_half\_day).
  - Set working\_hours\_threshold\_for\_absent from flt(self.working\_hours\_threshold\_for\_absent).
  - If self.is\_half\_holiday(employee, attendance\_date).
    - Set working\_hours\_threshold\_for\_half\_day from (flt(self.working\_hours\_threshold\_for\_half\_day) ÷ 2).
    - Set working\_hours\_threshold\_for\_absent from (flt(self.working\_hours\_threshold\_for\_absent) ÷ 2).
  - Set overtime\_type from single\_shift\_logs at 0.get(“overtime\_type”).
  - Set tuple(attendance\_status, working\_hours, late\_entry, early\_exit, …) from self.get\_attendance(single\_shift\_logs, working\_hours\_threshold\_for\_absent, working\_hours\_threshold\_for\_half\_day).
  - Evaluate mark\_attendance\_and\_link\_log(single\_shift\_logs, attendance\_status, attendance\_date, working\_hours, …).
- If not Platform.in\_test.
  - Evaluate Platform.db.commit().
- Set assigned\_employees from self.get\_assigned\_employees(self.process\_attendance\_after, true).
- For each batch in create\_batch(assigned\_employees, EMPLOYEE\_CHUNK\_SIZE).
  - For each employee in batch.
    - Evaluate self.mark\_absent\_for\_dates\_with\_no\_attendance(employee).
    - Evaluate self.mark\_absent\_for\_half\_day\_dates(employee).
  - If not Platform.in\_test.
    - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [should mark attendance](operations-040.md#op-74ec52d40d5a20), [is half holiday](operations-040.md#op-82a0d1362f5def), [get attendance](operations-040.md#op-343f5835e91380), [get assigned employees](operations-040.md#op-a53345c07c9ea1), [mark absent for dates with no attendance](operations-040.md#op-b9d0caf270cc13), [mark absent for half day dates](operations-040.md#op-b4607870fba786).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L3175) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1541) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L154)

<a id="op-82a0d1362f5def"></a>
### Shift Type.is half holiday

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_is_half_holiday`

**Inputs** self, employee, attendance\_date.

**Explicit results** true · false.

**Local steps**

- Set holiday\_list from self.get\_holiday\_list(employee, attendance\_date).
- If is\_half\_holiday(holiday\_list, attendance\_date).
  - Return true.
- Return false.

**Methods declared on this owner** [get holiday list](operations-040.md#op-7f82d38a523dcb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L4000) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1538) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L151)

<a id="op-c9a0fc76d1da82"></a>
### Shift Type.get employee checkins

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_get_employee_checkins`

**Inputs** self.

**Declared result** list at dict.

**Record and data access** read “Employee Checkin” via get\_all.

**Explicit results** Platform.get\_all(“Employee Checkin”, fields = list(“name”, “employee”, “log\_type”, “time”, …), filters = mapping(“skip\_auto\_attendance” → 0, “attendance” → tuple(“is”, “not set”), “time” → tuple(“&gt;=”, self ….

**Local steps**

- Return Platform.get\_all(“Employee Checkin”, fields = list(“name”, “employee”, “log\_type”, “time”, …), filters = mapping(“skip\_auto\_attendance” → 0, “attendance” → tuple(“is”, “not set”), “time” → tuple(“&gt;=”, self ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L4122) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1528) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L141)

<a id="op-343f5835e91380"></a>
### Shift Type.get attendance

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_get_attendance`

**Inputs** self, logs, working\_hours\_threshold\_for\_absent, working\_hours\_threshold\_for\_half\_day.

**Explicit results** tuple(“Absent”, total\_working\_hours, late\_entry, early\_exit, …) · tuple(“Half Day”, total\_working\_hours, late\_entry, early\_exit, …) · tuple(“Present”, total\_working\_hours, late\_entry, early\_exit, …).

**Local steps**

- Set late\_entry, early\_exit from false.
- Set tuple(total\_working\_hours, in\_time, out\_time) from calculate\_working\_hours(logs, self.determine\_check\_in\_and\_check\_out, self.working\_hours\_calculation\_based\_on).
- If (cint(self.enable\_late\_entry\_marking) and in\_time and in\_time &gt; (logs at 0.shift\_start + timedelta(minutes = cint(self.late\_entry\_grace\_period)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.enable\_late\_entry\_marking) → in\_time → in\_time &gt; (logs at 0.shift\_start + timedelta(minutes = cint(self.late\_entry\_grace\_period))).
  - Set late\_entry from true.
- If (cint(self.enable\_early\_exit\_marking) and out\_time and out\_time &lt; (logs at 0.shift\_end − timedelta(minutes = cint(self.early\_exit\_grace\_period)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.enable\_early\_exit\_marking) → out\_time → out\_time &lt; (logs at 0.shift\_end − timedelta(minutes = cint(self.early\_exit\_grace\_period))).
  - Set early\_exit from true.
- If (working\_hours\_threshold\_for\_absent and total\_working\_hours &lt; working\_hours\_threshold\_for\_absent).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in working\_hours\_threshold\_for\_absent → total\_working\_hours &lt; working\_hours\_threshold\_for\_absent.
  - Return tuple(“Absent”, total\_working\_hours, late\_entry, early\_exit, …).
- If (working\_hours\_threshold\_for\_half\_day and total\_working\_hours &lt; working\_hours\_threshold\_for\_half\_day).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in working\_hours\_threshold\_for\_half\_day → total\_working\_hours &lt; working\_hours\_threshold\_for\_half\_day.
  - Return tuple(“Half Day”, total\_working\_hours, late\_entry, early\_exit, …).
- Return tuple(“Present”, total\_working\_hours, late\_entry, early\_exit, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L4461) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1526) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L139)

<a id="op-b9d0caf270cc13"></a>
### Shift Type.mark absent for dates with no attendance

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_mark_absent_for_dates_with_number_attendance`

**Inputs** self, employee.

**Record and data access** resolve a document from mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → “Attendance”, “reference\_name” → attendance, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → “Attendance”, “reference\_name” → attendance, …)).

**Local steps**

- Set start\_time from get\_time(self.start\_time).
- Set dates from self.get\_dates\_for\_attendance(employee).
- For each date in dates.
  - Set timestamp from datetime.combine(date, start\_time).
  - Set shift\_details from get\_employee\_shift(employee, timestamp, true).
  - If (shift\_details and shift\_details.shift\_type.name equals self.name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in shift\_details → shift\_details.shift\_type.name equals self.name.
    - Set attendance from mark\_attendance(employee, date, “Absent”, self.name).
    - If not attendance.
      - Continue with the next iteration or loop test.
    - Evaluate Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → “Attendance”, “reference\_name” → attendance, …)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get dates for attendance](operations-040.md#op-2595a00751116b).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L4985) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1539) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L152)

<a id="op-2595a00751116b"></a>
### Shift Type.get dates for attendance

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_get_dates_for_attendance`

**Inputs** self, employee.

**Declared result** list at str.

**Explicit results** list() · sorted(((set(date\_range) − set(holiday\_dates)) − set(marked\_attendance\_dates))).

**Local steps**

- Set tuple(start\_date, end\_date) from self.get\_start\_and\_end\_dates(employee).
- If start\_date is identical to no value.
  - Return list().
- Set date\_range from get\_date\_range(start\_date, end\_date).
- If self.holiday\_list.
  - Set holiday\_dates from get\_holiday\_dates\_between(self.holiday\_list, start\_date, end\_date).
- Otherwise.
  - Set holiday\_dates from get\_holiday\_dates\_between\_range(employee, start\_date, end\_date, raise\_exception\_for\_holiday\_list = false).
- Set marked\_attendance\_dates from self.get\_marked\_attendance\_dates\_between(employee, start\_date, end\_date).
- Return sorted(((set(date\_range) − set(holiday\_dates)) − set(marked\_attendance\_dates))).

**Methods declared on this owner** [get start and end dates](operations-040.md#op-d58e1ef16018a1), [get marked attendance dates between](operations-040.md#op-513fc66e777e72).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L67) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1527) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L140)

<a id="op-d58e1ef16018a1"></a>
### Shift Type.get start and end dates

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_get_start_and_end_dates`

**Inputs** self, employee.

**Record and data access** read “Employee” via get\_cached\_value.

**Explicit results** tuple(no value, no value) · tuple(start\_date, end\_date).

**Local steps**

- Set tuple(date\_of\_joining, relieving\_date, employee\_creation) from Platform.get\_cached\_value(“Employee”, employee, list(“date\_of\_joining”, “relieving\_date”, “creation”)).
- If not date\_of\_joining.
  - Set date\_of\_joining from employee\_creation.date().
- Set start\_date from max(getdate(self.process\_attendance\_after), date\_of\_joining).
- Set end\_date from no value.
- Set shift\_details from get\_shift\_details(self.name, get\_datetime(self.last\_sync\_of\_checkin)).
- Set last\_shift\_time from shift\_details.actual\_end when shift\_details, otherwise get\_datetime(self.last\_sync\_of\_checkin).
  - Value choice on shift\_details — true gives shift\_details.actual\_end, false gives get\_datetime(self.last\_sync\_of\_checkin).
- Set ref\_time from (last\_shift\_time − timedelta(days = 1)).
- Set prev\_shift from get\_employee\_shift(employee, ref\_time, true, “reverse”).
- If (prev\_shift and prev\_shift.shift\_type.name differs from self.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in prev\_shift → prev\_shift.shift\_type.name differs from self.name.
  - Set prev\_shift from (self.get\_scheduled\_shift\_at(employee, ref\_time) or prev\_shift).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_scheduled\_shift\_at(employee, ref\_time) → prev\_shift.
- If (prev\_shift and prev\_shift.shift\_type.name equals self.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in prev\_shift → prev\_shift.shift\_type.name equals self.name.
  - Set end\_date from min(prev\_shift.start\_datetime.date(), relieving\_date) when relieving\_date, otherwise prev\_shift.start\_datetime.date().
    - Value choice on relieving\_date — true gives min(prev\_shift.start\_datetime.date(), relieving\_date), false gives prev\_shift.start\_datetime.date().
- Otherwise.
  - Return tuple(no value, no value).
- Return tuple(start\_date, end\_date).

**Methods declared on this owner** [get scheduled shift at](operations-040.md#op-9afef72fcf1b8a).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Employee”, employee, list(“date\_of\_joining”, “relieving\_date”, “creation”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L68) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1534) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L147)

<a id="op-9afef72fcf1b8a"></a>
### Shift Type.get scheduled shift at

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_get_scheduled_shift_at`

**Inputs** self, employee, for\_timestamp.

**Declared result** (dict bitwise or no value).

**Explicit results** next(generator of shift for shift drawn from shifts where shift.shift\_type.name equals self.name, no value).

**Local steps**

- Set shifts from get\_valid\_shifts\_for\_time(get\_shifts\_for\_date(employee, for\_timestamp), for\_timestamp).
- Return next(generator of shift for shift drawn from shifts where shift.shift\_type.name equals self.name, no value).
  - Draw shift from shifts, keep a combination only if (shift.shift\_type.name equals self.name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L6439) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1532) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L145)

<a id="op-513fc66e777e72"></a>
### Shift Type.get marked attendance dates between

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_get_marked_attendance_dates_between`

**Inputs** self, employee, start\_date, end\_date.

**Declared result** list at str.

**Explicit results** nested operand in the contract(nested operand in the contract).select(Attendance.attendance\_date).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in ….

**Local steps**

- Set Attendance from Platform.qb.DocType(“Attendance”).
- Return nested operand in the contract(nested operand in the contract).select(Attendance.attendance\_date).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L6627) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1530) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L143)

<a id="op-a53345c07c9ea1"></a>
### Shift Type.get assigned employees

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_get_assigned_employees`

**Inputs** self, from\_date, consider\_default\_shift = false.

**Declared result** list at str.

**Record and data access** read “Shift Assignment” via get\_all · read “Employee” via get\_all.

**Explicit results** list((set(assigned\_employees) − set(inactive\_employees))).

**Local steps**

- Set filters from mapping(“shift\_type” → self.name, “docstatus” → “1”, “status” → “Active”).
- Set or\_filters from list(list(“end\_date”, “&gt;=”, from\_date), list(“end\_date”, “is”, “not set”)).
- Set assigned\_employees from Platform.get\_all(“Shift Assignment”, filters = filters, or\_filters = or\_filters, pluck = “employee”).
- If consider\_default\_shift.
  - Set default\_shift\_employees from Platform.get\_all(“Employee”, filters = mapping(“default\_shift” → self.name, “status” → “Active”), pluck = “name”).
  - Set assigned\_employees from set((assigned\_employees + default\_shift\_employees)).
- Set inactive\_employees from Platform.db.get\_all(“Employee”, mapping(“status” → “Inactive”), pluck = “name”).
- Return list((set(assigned\_employees) − set(inactive\_employees))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0073.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1525) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L138)

<a id="op-7f82d38a523dcb"></a>
### Shift Type.get holiday list

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_get_holiday_list`

**Inputs** self, employee, date = no value.

**Declared result** str.

**Explicit results** holiday\_list\_name.

**Local steps**

- Set holiday\_list\_name from (self.holiday\_list or get\_holiday\_list\_for\_employee(employee, false, as\_on = date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.holiday\_list → get\_holiday\_list\_for\_employee(employee, false, as\_on = date).
- Return holiday\_list\_name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0073.json#L527) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1529) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L142)

<a id="op-74ec52d40d5a20"></a>
### Shift Type.should mark attendance

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_should_mark_attendance`

**Inputs** self, employee, attendance\_date.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If self.mark\_auto\_attendance\_on\_holidays.
  - Return true.
- Set holiday\_list from self.get\_holiday\_list(employee, attendance\_date).
- If is\_holiday(holiday\_list, attendance\_date).
  - Return false.
- Return true.

**Methods declared on this owner** [get holiday list](operations-040.md#op-7f82d38a523dcb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0073.json#L645) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1543) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L156)

<a id="op-b4607870fba786"></a>
### Shift Type.mark absent for half day dates

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_mark_absent_for_half_day_dates`

**Inputs** self, employee.

**Record and data access** read “Attendance” via get\_all · resolve a document from mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → “Attendance”, “reference\_name” → attendance.name, …) via get\_doc.

**State and service calls** request set\_value on “Attendance” · call insert on Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → “Attendance”, “reference\_name” → attendance.name, …)).

**Local steps**

- Set half\_day\_attendances from Platform.get\_all(“Attendance”, filters = mapping(“employee” → employee, “status” → “Half Day”, “modify\_half\_day\_status” → 1, “attendance\_date” → list(“&lt;=”, getdate(self.last\_sync\_of\_checkin))), fields = li ….
- Set start\_time from get\_time(self.start\_time).
- Set last\_sync\_of\_checkin from get\_datetime(self.last\_sync\_of\_checkin).
- For each attendance in half\_day\_attendances.
  - Set timestamp from datetime.combine(attendance.attendance\_date, start\_time).
  - Set shift\_details from get\_employee\_shift(employee, timestamp, true).
  - If (shift\_details and shift\_details.shift\_type.name equals self.name and shift\_details.actual\_end &lt; last\_sync\_of\_checkin).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in shift\_details → shift\_details.shift\_type.name equals self.name → shift\_details.actual\_end &lt; last\_sync\_of\_checkin.
    - Evaluate Platform.db.set\_value(“Attendance”, attendance.name, mapping(“shift” → self.name, “half\_day\_status” → “Absent”, “modify\_half\_day\_status” → 0)).
    - Evaluate Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → “Attendance”, “reference\_name” → attendance.name, …)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L69) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1540) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L153)

<a id="op-d977d5fb21e1da"></a>
### Update last sync of checkin

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_update_last_sync_of_checkin`

**Inputs** no declared parameters.

**Record and data access** read “Shift Type” via get\_all.

**State and service calls** request set\_value on “Shift Type”.

**Local steps**

- Set shifts from Platform.get\_all(“Shift Type”, filters = mapping(“enable\_auto\_attendance” → 1, “auto\_update\_last\_sync” → 1), fields = list(“name”, “last\_sync\_of\_checkin”, “start\_time”, “end\_time”)).
- Set current\_datetime from (Platform.flags.current\_datetime or get\_datetime()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.current\_datetime → get\_datetime().
- For each shift in shifts.
  - Set shift\_end from get\_actual\_shift\_end(shift, current\_datetime).
  - Set update\_last\_sync from no value.
  - If shift.last\_sync\_of\_checkin.
    - If get\_datetime(shift.last\_sync\_of\_checkin) &lt; shift\_end &lt; current\_datetime.
      - Compare adjacent operands in order, stopping at the first false comparison in get\_datetime(shift.last\_sync\_of\_checkin) &lt; shift\_end &lt; current\_datetime.
      - Set update\_last\_sync from true.
  - Otherwise.
    - If shift\_end &lt; current\_datetime.
      - Set update\_last\_sync from true.
  - If update\_last\_sync.
    - Evaluate Platform.db.set\_value(“Shift Type”, shift.name, “last\_sync\_of\_checkin”, (shift\_end + timedelta(minutes = 1))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0073.json#L1436) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1550) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L162)

<a id="op-03cbe3554ad1dc"></a>
### Get actual shift end

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_get_actual_shift_end`

**Inputs** shift, current\_datetime.

**Explicit results** actual\_shift\_end.

**Local steps**

- Set time\_within\_shift from datetime.combine(current\_datetime.date(), get\_time(shift.start\_time)).
- Set shift\_details from get\_shift\_details(shift.name, time\_within\_shift).
- Set actual\_shift\_start from shift\_details at “actual\_start”.
- Set actual\_shift\_end from shift\_details at “actual\_end”.
- If (actual\_shift\_start.date() &lt; actual\_shift\_end.date() or current\_datetime &lt; actual\_shift\_start).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in actual\_shift\_start.date() &lt; actual\_shift\_end.date() → current\_datetime &lt; actual\_shift\_start.
  - Set actual\_shift\_end from add\_days(actual\_shift\_end, negative 1).
- Return actual\_shift\_end.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0073.json#L1882) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1523) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L136)

<a id="op-9a03fe78c07e81"></a>
### Process auto attendance for all shifts

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_process_auto_attendance_for_all_shifts`

**Inputs** no declared parameters.

**Record and data access** read “Shift Type” via get\_all · resolve a document from “Shift Type” via get\_cached\_doc.

**Local steps**

- Set shift\_list from Platform.get\_all(“Shift Type”, filters = mapping(“enable\_auto\_attendance” → “1”), pluck = “name”).
- For each shift in shift\_list.
  - Set doc from Platform.get\_cached\_doc(“Shift Type”, shift).
  - Evaluate doc.process\_auto\_attendance().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Shift Type”, shift).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0073.json#L2168) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1524) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L137)

<a id="op-4c0b18b8331256"></a>
### Get data

`operation_workforce_human_resources_record_definitions_shift_type_shift_type_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “shift”, “non\_standard\_fieldnames” → mapping(“Shift Request” → “shift\_type”, “Shift Assignment” → “shift\_type”), “transactions” → list(mapping(“items” → list(“Attendance”, “Employee C ….

**Local steps**

- Return mapping(“fieldname” → “shift”, “non\_standard\_fieldnames” → mapping(“Shift Request” → “shift\_type”, “Shift Assignment” → “shift\_type”), “transactions” → list(mapping(“items” → list(“Attendance”, “Employee C ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0073.json#L2340) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1551) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L163)

## Record · Staffing plan

[Record definition](../../../../data/record-types/staffing_plan.json)

<a id="op-2e23438c532c98"></a>
### Staffing Plan.validate

`operation_workforce_human_resources_record_definitions_staffing_plan_business_behavior_staffing_plan_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_period().
- Evaluate self.validate\_details().
- Evaluate self.set\_total\_estimated\_budget().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate period](operations-040.md#op-dbbaf5f478b7dd), [validate details](operations-040.md#op-0904d8455dacdf), [set total estimated budget](operations-040.md#op-d494100b15f8ed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0076.json#L3335) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1594) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L203)

<a id="op-dbbaf5f478b7dd"></a>
### Staffing Plan.validate period

`operation_workforce_human_resources_record_definitions_staffing_plan_business_behavior_staffing_plan_validate_period`

**Inputs** self.

**Explicit failure paths** validation helper — translated “From Date cannot be greater than To Date”.

**Local steps**

- If (self.from\_date and self.to\_date and self.from\_date &gt; self.to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_date → self.to\_date → self.from\_date &gt; self.to\_date.
  - Call the validation error handler Platform.throw(translated “From Date cannot be greater than To Date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0076.json#L3426) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1597) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L206)

<a id="op-0904d8455dacdf"></a>
### Staffing Plan.validate details

`operation_workforce_human_resources_record_definitions_staffing_plan_business_behavior_staffing_plan_validate_details`

**Inputs** self.

**Local steps**

- For each detail in self.get(“staffing\_details”).
  - Evaluate self.validate\_overlap(detail).
  - Evaluate self.validate\_with\_subsidiary\_plans(detail).
  - Evaluate self.validate\_with\_parent\_plan(detail).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overlap](operations-041.md#op-58f880d107cd65), [validate with subsidiary plans](operations-041.md#op-325d1a59b58be5), [validate with parent plan](operations-041.md#op-d114cdf0a09925).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0076.json#L3548) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1595) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L204)

<a id="op-d494100b15f8ed"></a>
### Staffing Plan.set total estimated budget

`operation_workforce_human_resources_record_definitions_staffing_plan_business_behavior_staffing_plan_set_total_estimated_budget`

**Inputs** self.

**Local steps**

- Set self.total\_estimated\_budget from 0.
- For each detail in self.get(“staffing\_details”).
  - Set designation\_counts from get\_designation\_counts(detail.designation, self.company).
  - Set detail.current\_count from designation\_counts at “employee\_count”.
  - Set detail.current\_openings from designation\_counts at “job\_openings”.
  - Evaluate self.set\_number\_of\_positions(detail).
  - Set detail.total\_estimated\_cost from 0.
  - If detail.number\_of\_positions &gt; 0.
    - If (detail.vacancies and detail.estimated\_cost\_per\_position).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in detail.vacancies → detail.estimated\_cost\_per\_position.
      - Set detail.total\_estimated\_cost from (cint(detail.vacancies) × flt(detail.estimated\_cost\_per\_position)).
  - Update self.total\_estimated\_budget using + detail.total\_estimated\_cost.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set number of positions](operations-040.md#op-150e3285b2f507).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0076.json#L3691) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1593) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L202)

<a id="op-150e3285b2f507"></a>
### Staffing Plan.set number of positions

`operation_workforce_human_resources_record_definitions_staffing_plan_business_behavior_staffing_plan_set_number_of_positions`

**Inputs** self, detail.

**Local steps**

- Set detail.number\_of\_positions from (cint(detail.vacancies) + cint(detail.current\_count)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0076.json#L4038) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1592) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L201)
