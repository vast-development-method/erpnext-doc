# Employment and attendance · operations 34

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Workspace · Organizational chart

<a id="op-f6fc4098f1dcf2"></a>
### Get nodes

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_nodes`

**Inputs** company, companies, employees.

**Declared result** list at Platform.\_dict.

**Explicit results** list() · list of Platform.\_dict(get\_person(employee, leave\_status, can\_email), reports = len(teams.get(employee.name, list())), team = list of mapping(“id” → member.name, “name” → member.employee\_name, “image” → me ….

**Local steps**

- If not employees.
  - Return list().
- Set names from list of employee.name for employee drawn from employees.
  - Draw employee from employees.
- Set teams from mapping().
- For each member in get\_employees(company, mapping(“reports\_to” → list(“in”, names)), fields = list(“name”, “employee\_name”, “image”, “reports\_to”)).
  - Evaluate teams.setdefault(member.reports\_to, list()).append(member).
- Set managers from get\_managers((set of employee.reports\_to for employee drawn from employees − set(no value, empty text))).
  - Draw employee from employees.
- Set visible\_managers from mapping of name → manager for tuple(name, manager) drawn from managers.items() where is\_visible(manager, companies).
  - Draw tuple(name, manager) from managers.items(), keep a combination only if (is\_visible(manager, companies)).
- Set leave\_status from get\_leave\_status((mapping of name → company for name drawn from names bitwise or mapping of manager.name → manager.company for manager drawn from visible\_managers.values())).
  - Draw name from names.
  - Draw manager from visible\_managers.values().
- Set can\_email from get\_email\_access((names + list(visible\_managers))).
- Return list of Platform.\_dict(get\_person(employee, leave\_status, can\_email), reports = len(teams.get(employee.name, list())), team = list of mapping(“id” → member.name, “name” → member.employee\_name, “image” → me ….
  - Draw employee from employees.
  - Draw member from teams.get(employee.name, list()) at slice no value to TEAM\_PREVIEW\_SIZE.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L143) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L194) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L194)

<a id="op-5a2d1775aa285f"></a>
### Get manager card

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_manager_card`

**Inputs** manager, companies, leave\_status, can\_email.

**Declared result** (Platform.\_dict bitwise or no value).

**Explicit results** no value · Platform.\_dict(get\_person(manager, leave\_status, can\_email), company = manager.company) · Platform.\_dict(id = manager.name, name = manager.employee\_name, image = manager.image, company = manager.company).

**Local steps**

- If not manager.
  - Return no value.
- If is\_visible(manager, companies).
  - Return Platform.\_dict(get\_person(manager, leave\_status, can\_email), company = manager.company).
- Return Platform.\_dict(id = manager.name, name = manager.employee\_name, image = manager.image, company = manager.company).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L141) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L192) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L192)

<a id="op-aca1f8e6038a99"></a>
### Is visible

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_is_visible`

**Inputs** manager, companies.

**Declared result** bool.

**Explicit results** (manager.status equals “Active” and manager.company belongs to companies).

**Local steps**

- Return (manager.status equals “Active” and manager.company belongs to companies).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in manager.status equals “Active” → manager.company belongs to companies.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L150) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L201) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L201)

<a id="op-44de20f89b4cd8"></a>
### Get email access

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_email_access`

**Inputs** names.

**Declared result** set at str.

**Record and data access** read “Employee” via get\_list.

**Explicit results** set() · set(Platform.get\_list(“Employee”, filters = mapping(“name” → list(“in”, names)), pluck = “name”, limit = 0)).

**Local steps**

- If not Platform.has\_permission(“Employee”, ptype = “email”).
  - Return set().
- Return set(Platform.get\_list(“Employee”, filters = mapping(“name” → list(“in”, names)), pluck = “name”, limit = 0)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, ptype = “email”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L137) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L188) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L188)

<a id="op-1eed5c2ef10570"></a>
### Get person

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_person`

**Inputs** employee, leave\_status, can\_email.

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(id = employee.name, name = employee.employee\_name, image = employee.image, designation = employee.designation, …).

**Local steps**

- Return Platform.\_dict(id = employee.name, name = employee.employee\_name, image = employee.image, designation = employee.designation, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L145) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L196) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L196)

<a id="op-67f07931371292"></a>
### Get managers

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_managers`

**Inputs** names.

**Declared result** dict at tuple(str, Platform.\_dict).

**Record and data access** read “Employee” via get\_all.

**Explicit results** mapping() · mapping of manager.name → manager for manager drawn from Platform.get\_all(“Employee”, filters = mapping(“name” → list(“in”, list(names))), fields = list(expanded NODE\_FIELDS, “company”, “status”), limit = 0).

**Local steps**

- If not names.
  - Return mapping().
- Return mapping of manager.name → manager for manager drawn from Platform.get\_all(“Employee”, filters = mapping(“name” → list(“in”, list(names))), fields = list(expanded NODE\_FIELDS, “company”, “status”), limit = 0).
  - Draw manager from Platform.get\_all(“Employee”, filters = mapping(“name” → list(“in”, list(names))), fields = list(expanded NODE\_FIELDS, “company”, “status”), limit = 0).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L142) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L193) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L193)

<a id="op-b4d6eada1b5d1e"></a>
### Get leave status

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_leave_status`

**Inputs** employee\_company\_map.

**Declared result** dict at tuple(str, dict).

**Record and data access** read “Leave Application” via get\_all.

**Explicit results** mapping() · leave\_status.

**Local steps**

- Set today from getdate().
- Set lookahead\_end from add\_days(today, RETURN\_LOOKAHEAD\_DAYS).
- Set leaves from mapping().
- For each leave in Platform.get\_all(“Leave Application”, filters = mapping(“employee” → list(“in”, list(employee\_company\_map)), “status” → “Approved”, “docstatus” → 1, “from\_date” → list(“&lt;=”, lookahead\_end), …), fields = li ….
  - Evaluate leaves.setdefault(leave.employee, list()).append(leave).
- Set on\_leave from mapping of employee → employee\_leaves for tuple(employee, employee\_leaves) drawn from leaves.items() where get\_leave\_on(today, employee\_leaves).
  - Draw tuple(employee, employee\_leaves) from leaves.items(), keep a combination only if (get\_leave\_on(today, employee\_leaves)).
- If not on\_leave.
  - Return mapping().
- Set holidays from get\_holidays\_in\_ranges\_map(get\_holiday\_list\_ranges\_for\_employees(mapping of employee → employee\_company\_map at employee for employee drawn from on\_leave, add\_days(today, 1), lookahead\_end)).
  - Draw employee from on\_leave.
- Set leave\_status from mapping().
- For each tuple(employee, employee\_leaves) in on\_leave.items().
  - If is\_half\_day(get\_leave\_on(today, employee\_leaves), today).
    - Set leave\_status at employee from mapping(“half\_day” → true, “back\_on” → no value).
    - Continue with the next iteration or loop test.
  - Set holiday\_dates from set of holiday.holiday\_date for holiday drawn from holidays.get(employee, list()).
    - Draw holiday from holidays.get(employee, list()).
  - Set back\_on from add\_days(today, 1).
  - While (back\_on ≤ lookahead\_end and (back\_on belongs to holiday\_dates or is\_on\_full\_leave(back\_on, employee\_leaves))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in back\_on ≤ lookahead\_end → (back\_on belongs to holiday\_dates or is\_on\_full\_leave(back\_on, employee\_leaves)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in back\_on belongs to holiday\_dates → is\_on\_full\_leave(back\_on, employee\_leaves).
    - Set back\_on from add\_days(back\_on, 1).
  - Set leave\_status at employee from mapping(“half\_day” → false, “back\_on” → back\_on when back\_on ≤ lookahead\_end, otherwise no value).
    - Value choice on back\_on ≤ lookahead\_end — true gives back\_on, false gives no value.
- Return leave\_status.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L140) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L191) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L191)

<a id="op-a7102af8234f2d"></a>
### Get leave on

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_leave_on`

**Inputs** day, leaves.

**Declared result** (Platform.\_dict bitwise or no value).

**Explicit results** next(generator of leave for leave drawn from leaves where leave.from\_date ≤ day ≤ leave.to\_date, no value).

**Local steps**

- Return next(generator of leave for leave drawn from leaves where leave.from\_date ≤ day ≤ leave.to\_date, no value).
  - Draw leave from leaves, keep a combination only if (leave.from\_date ≤ day ≤ leave.to\_date).
  - Compare adjacent operands in order, stopping at the first false comparison in leave.from\_date ≤ day ≤ leave.to\_date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L139) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L190) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L190)

<a id="op-0a4d6cc8969bcc"></a>
### Is half day

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_is_half_day`

**Inputs** leave, day.

**Declared result** bool.

**Explicit results** (bool(leave.half\_day) and (leave.from\_date equals leave.to\_date or leave.half\_day\_date equals day)).

**Local steps**

- Return (bool(leave.half\_day) and (leave.from\_date equals leave.to\_date or leave.half\_day\_date equals day)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(leave.half\_day) → (leave.from\_date equals leave.to\_date or leave.half\_day\_date equals day).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in leave.from\_date equals leave.to\_date → leave.half\_day\_date equals day.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L147) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L198) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L198)

<a id="op-9d67dafb3ca3f6"></a>
### Is on full leave

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_is_on_full_leave`

**Inputs** day, leaves.

**Declared result** bool.

**Explicit results** (bool(leave) and not is\_half\_day(leave, day)).

**Local steps**

- Set leave from get\_leave\_on(day, leaves).
- Return (bool(leave) and not is\_half\_day(leave, day)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(leave) → not is\_half\_day(leave, day).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L148) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L199) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L199)

## Record · Overtime slip

[Record definition](../../../../data/record-types/overtime_slip.json)

<a id="op-20fdbfcce70cc7"></a>
### Overtime Slip.validate

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Start date cannot be greater than end date”.

**Local steps**

- If not (self.start\_date or self.end\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.start\_date → self.end\_date.
  - Evaluate self.get\_frequency\_and\_dates().
- If self.start\_date &gt; self.end\_date.
  - Call the validation error handler Platform.throw(translated “Start date cannot be greater than end date”).
- Evaluate self.validate\_overlap().
- Evaluate self.validate\_overtime\_date\_and\_duration().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get frequency and dates](operations-034.md#op-188b8c2ad51d87), [validate overlap](operations-034.md#op-ca1da7698482b2), [validate overtime date and duration](operations-034.md#op-1dd0334b51b68c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L1772) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1404) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L18)

<a id="op-43865a16ff4f29"></a>
### Overtime Slip.on submit

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.process\_overtime\_slip().

If control reaches the end, it returns no value.

**Methods declared on this owner** [process overtime slip](operations-034.md#op-0a3db7edbed725).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L1964) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1402) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L16)

<a id="op-ca1da7698482b2"></a>
### Overtime Slip.validate overlap

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_validate_overlap`

**Inputs** self.

**Record and data access** read “Overtime Slip” via get\_all.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set overtime\_slips from Platform.db.get\_all(“Overtime Slip”, filters = mapping(“docstatus” → tuple(“!=”, 2), “employee” → self.employee, “end\_date” → tuple(“&gt;=”, self.start\_date), “start\_date” → tuple(“&lt;=”, self.end\_date), …)).
- If len(overtime\_slips).
  - Set form\_link from get\_link\_to\_form(“Overtime Slip”, overtime\_slips at 0.name).
  - Set msg from translated “Overtime Slip:{0} has been created between {1} and {2}”.format(bold(form\_link), bold(self.start\_date), bold(self.end\_date)).
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L2015) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1405) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L19)

<a id="op-1dd0334b51b68c"></a>
### Overtime Slip.validate overtime date and duration

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_validate_overtime_date_and_duration`

**Inputs** self.

**Record and data access** read “Overtime Type” via get\_value.

**Explicit failure paths** validation helper — translated “Date {0} is repeated in Overtime Details”.format(detail.date) · validation helper — translated “Overtime Duration for {0} is greater than Maximum Overtime Hours Allowed”.format(detail.date).

**Local steps**

- Set dates from set().
- Set overtime\_type\_cache from mapping().
- For each detail in self.overtime\_details.
  - If detail.date belongs to dates.
    - Call the validation error handler Platform.throw(translated “Date {0} is repeated in Overtime Details”.format(detail.date)).
  - Evaluate dates.add(detail.date).
  - If detail.reference\_document.
    - Continue with the next iteration or loop test.
  - If detail.overtime\_type does not belong to overtime\_type\_cache.
    - Set overtime\_type\_cache at detail.overtime\_type from Platform.db.get\_value(“Overtime Type”, detail.overtime\_type, “maximum\_overtime\_hours\_allowed”).
  - Set maximum\_overtime\_hours from overtime\_type\_cache at detail.overtime\_type.
  - If maximum\_overtime\_hours.
    - If detail.overtime\_duration &gt; maximum\_overtime\_hours.
      - Call the validation error handler Platform.throw(translated “Overtime Duration for {0} is greater than Maximum Overtime Hours Allowed”.format(detail.date)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L2425) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1406) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L20)

<a id="op-188b8c2ad51d87"></a>
### Overtime Slip.get frequency and dates

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_get_frequency_and_dates`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Salary Structure” via get\_value · read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “Salary Structure not assigned for employee {0} for date {1}”.format(self.employee, self.start\_date).

**Local steps**

- Set date from self.posting\_date.
- Set salary\_structure from get\_assigned\_salary\_structure(self.employee, date).
- If salary\_structure.
  - Set payroll\_frequency from Platform.db.get\_value(“Salary Structure”, salary\_structure, “payroll\_frequency”).
  - Set date\_details from get\_start\_end\_dates(payroll\_frequency, date, Platform.db.get\_value(“Employee”, self.employee, “company”)).
  - Set self.start\_date from date\_details.start\_date.
  - Set self.end\_date from date\_details.end\_date.
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Salary Structure not assigned for employee {0} for date {1}”.format(self.employee, self.start\_date)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L2846) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1397) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L11)

<a id="op-4f9c930fb29041"></a>
### Overtime Slip.get emp and overtime details

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_get_employee_and_overtime_details`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call save on self.

**Local steps**

- Set records from self.get\_attendance\_records().
- If len(records).
  - Evaluate self.create\_overtime\_details\_row\_for\_attendance(records).
- If len(self.overtime\_details).
  - Set total\_overtime\_duration from 0.0.
  - For each detail in self.overtime\_details.
    - If detail.overtime\_duration is distinct from no value.
      - Update total\_overtime\_duration using + detail.overtime\_duration.
  - Set self.total\_overtime\_duration from total\_overtime\_duration.
- Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get attendance records](operations-034.md#op-d71143177ee7c0), [create overtime details row for attendance](operations-034.md#op-f1b1d1650d12f2).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L3195) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1396) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L10)

<a id="op-f1b1d1650d12f2"></a>
### Overtime Slip.create overtime details row for attendance

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_create_overtime_details_row_for_attendance`

**Inputs** self, records.

**Record and data access** read “Overtime Type” via get\_value.

**Local steps**

- Set self.overtime\_details from list().
- Set overtime\_type\_cache from mapping().
- For each record in records.
  - If record.overtime\_type does not belong to overtime\_type\_cache.
    - Set overtime\_type\_cache at record.overtime\_type from Platform.db.get\_value(“Overtime Type”, record.overtime\_type, “maximum\_overtime\_hours\_allowed”).
  - Set maximum\_overtime\_hours\_allowed from overtime\_type\_cache at record.overtime\_type.
  - Set overtime\_duration from (record.actual\_overtime\_duration or 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in record.actual\_overtime\_duration → 0.0.
  - If maximum\_overtime\_hours\_allowed &gt; 0.
    - Set overtime\_duration from overtime\_duration when maximum\_overtime\_hours\_allowed &gt; overtime\_duration, otherwise maximum\_overtime\_hours\_allowed.
      - Value choice on maximum\_overtime\_hours\_allowed &gt; overtime\_duration — true gives overtime\_duration, false gives maximum\_overtime\_hours\_allowed.
  - If overtime\_duration &gt; 0.
    - Evaluate self.append(“overtime\_details”, mapping(“reference\_document” → record.name, “date” → record.attendance\_date, “overtime\_type” → record.overtime\_type, “overtime\_duration” → overtime\_duration, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L3467) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1393) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L7)

<a id="op-d71143177ee7c0"></a>
### Overtime Slip.get attendance records

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_get_attendance_records`

**Inputs** self.

**Record and data access** read “Attendance” via get\_all.

**Explicit results** records.

**Explicit failure paths** validation helper — translated “No attendance records found for employee {0} between {1} and {2}”.format(self.employee, self.start\_date, self.end\_date).

**Local steps**

- Set records from list().
- If (self.start\_date and self.end\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.start\_date → self.end\_date.
  - Set records from Platform.get\_all(“Attendance”, fields = list(“name”, “attendance\_date”, “overtime\_type”, “actual\_overtime\_duration”, …), filters = mapping(“employee” → self.employee, “docstatus” → 1, “attendance\_date” → t ….
  - If not len(records).
    - Call the validation error handler Platform.throw(translated “No attendance records found for employee {0} between {1} and {2}”.format(self.employee, self.start\_date, self.end\_date)).
- Return records.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L3904) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1395) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L9)

<a id="op-0a3db7edbed725"></a>
### Overtime Slip.process overtime slip

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_process_overtime_slip`

**Inputs** self.

**Record and data access** read “System Settings” via get\_single\_value.

**Local steps**

- Set overtime\_components from self.get\_overtime\_component\_amounts().
- Set precision from (Platform.db.get\_single\_value(“System Settings”, “currency\_precision”) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“System Settings”, “currency\_precision”) → 2.
- For each tuple(component, total\_amount) in overtime\_components.items().
  - Evaluate self.create\_additional\_salary(component, total\_amount, precision).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get overtime component amounts](operations-034.md#op-101ca5f5c018ff), [create additional salary](operations-034.md#op-52df0f2f32d001).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “currency\_precision”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L4333) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1403) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L17)

<a id="op-52df0f2f32d001"></a>
### Overtime Slip.create additional salary

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_create_additional_salary`

**Inputs** self, salary\_component, total\_amount, precision = no value.

**Record and data access** resolve a document from mapping(“doctype” → “Additional Salary”, “company” → self.company, “employee” → self.employee, “salary\_component” → salary\_component, …) via get\_doc.

**State and service calls** call submit on additional\_salary.

**Local steps**

- If total\_amount &gt; 0.
  - Set additional\_salary from Platform.get\_doc(mapping(“doctype” → “Additional Salary”, “company” → self.company, “employee” → self.employee, “salary\_component” → salary\_component, …)).
  - Evaluate additional\_salary.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L4516) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1392) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L6)

<a id="op-101ca5f5c018ff"></a>
### Overtime Slip.get overtime component amounts

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_get_overtime_component_amounts`

**Inputs** self.

**Explicit results** mapping() · overtime\_components.

**Local steps**

- If not self.overtime\_details.
  - Return mapping().
- Set unique\_overtime\_types from set of detail.overtime\_type for detail drawn from self.overtime\_details.
  - Draw detail from self.overtime\_details.
- Set self.overtime\_types from self.\_bulk\_load\_overtime\_types(unique\_overtime\_types).
- Set holiday\_date\_map from self.get\_holiday\_map().
- Set overtime\_components from mapping().
- For each overtime\_detail in self.overtime\_details.
  - Set overtime\_type from overtime\_detail.overtime\_type.
  - Set applicable\_hourly\_rate from self.\_get\_applicable\_hourly\_rate(overtime\_type, overtime\_detail.get(“standard\_working\_hours”)).
  - Set overtime\_amount from self.calculate\_overtime\_amount(overtime\_type, applicable\_hourly\_rate, overtime\_detail.overtime\_duration, overtime\_detail.date, …).
  - Set salary\_component from self.overtime\_types at overtime\_type at “overtime\_salary\_component”.
  - Set overtime\_components at salary\_component from (overtime\_components.get(salary\_component, 0) + overtime\_amount).
- Return overtime\_components.

**Methods declared on this owner** [bulk load overtime types](operations-034.md#op-22f1ad42311b7e), [get holiday map](operations-035.md#op-9a2b33a4dfe890), [get applicable hourly rate](operations-034.md#op-3e3845d2a6ee65), [calculate overtime amount](operations-035.md#op-0cd50118ac589b).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L4829) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1399) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L13)

<a id="op-22f1ad42311b7e"></a>
### Overtime Slip.bulk load overtime types

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_bulk_load_overtime_types`

**Inputs** self, overtime\_type\_names.

**Record and data access** read “Overtime Type” via get\_all · read “Overtime Salary Component” via get\_all.

**Explicit results** mapping() · overtime\_types.

**Local steps**

- If not overtime\_type\_names.
  - Return mapping().
- Set overtime\_types\_data from Platform.get\_all(“Overtime Type”, filters = mapping(“name” → list(“in”, list(overtime\_type\_names))), fields = list(“name”, “standard\_multiplier”, “weekend\_multiplier”, “public\_holiday\_multiplier”, …)).
- Set overtime\_types from mapping().
- Set salary\_component\_based\_types from list().
- For each ot\_data in overtime\_types\_data.
  - Set overtime\_types at ot\_data.name from ot\_data.
  - If ot\_data.overtime\_calculation\_method equals “Salary Component Based”.
    - Evaluate salary\_component\_based\_types.append(ot\_data.name).
- If salary\_component\_based\_types.
  - Set salary\_components\_data from Platform.get\_all(“Overtime Salary Component”, filters = mapping(“parent” → list(“in”, salary\_component\_based\_types)), fields = list(“parent”, “salary\_component”)).
  - Set components\_by\_parent from mapping().
  - For each comp\_data in salary\_components\_data.
    - If comp\_data.parent does not belong to components\_by\_parent.
      - Set components\_by\_parent at comp\_data.parent from list().
    - Evaluate components\_by\_parent at comp\_data.parent.append(comp\_data.salary\_component).
  - For each ot\_type in salary\_component\_based\_types.
    - Set overtime\_types at ot\_type at “components” from components\_by\_parent.get(ot\_type, list()).
- Return overtime\_types.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L5237) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1389) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L3)

<a id="op-3e3845d2a6ee65"></a>
### Overtime Slip.get applicable hourly rate

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_get_applicable_hourly_rate`

**Inputs** self, overtime\_type, standard\_working\_hours = 0.

**Explicit results** applicable\_hourly\_rate.

**Local steps**

- Set overtime\_details from self.overtime\_types at overtime\_type.
- Set overtime\_calculation\_method from overtime\_details at “overtime\_calculation\_method”.
- Set applicable\_hourly\_rate from 0.0.
- If overtime\_calculation\_method equals “Fixed Hourly Rate”.
  - Set applicable\_hourly\_rate from overtime\_details.get(“hourly\_rate”, 0.0).
- Otherwise.
  - If overtime\_calculation\_method equals “Salary Component Based”.
    - Set applicable\_hourly\_rate from self.\_calculate\_component\_based\_hourly\_rate(overtime\_type, standard\_working\_hours).
- Return applicable\_hourly\_rate.

**Methods declared on this owner** [calculate component based hourly rate](operations-034.md#op-f9c0559479533d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L5894) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1394) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L8)

<a id="op-f9c0559479533d"></a>
### Overtime Slip.calculate component based hourly rate

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_calculate_component_based_hourly_rate`

**Inputs** self, overtime\_type, standard\_working\_hours.

**Explicit results** 0.0 · (applicable\_daily\_amount ÷ standard\_working\_hours).

**Local steps**

- Set components from (self.overtime\_types at overtime\_type at “components” or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.overtime\_types at overtime\_type at “components” → list().
- If not hasattr(self, “\_cached\_salary\_slip”).
  - Set salary\_structure from get\_assigned\_salary\_structure(self.employee, self.start\_date).
  - Set self.\_cached\_salary\_slip from self.\_make\_salary\_slip(salary\_structure).
- If (not components or not hasattr(self, “\_cached\_salary\_slip”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not components → not hasattr(self, “\_cached\_salary\_slip”).
  - Return 0.0.
- Set component\_amount from sum(generator of data.amount for data drawn from self.\_cached\_salary\_slip.earnings where (data.salary\_component belongs to components and not data.get(“additional\_salary”, no value))).
  - Draw data from self.\_cached\_salary\_slip.earnings, keep a combination only if ((data.salary\_component belongs to components and not data.get(“additional\_salary”, no value))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.salary\_component belongs to components → not data.get(“additional\_salary”, no value).
- Set payment\_days from max(self.\_cached\_salary\_slip.payment\_days, 1).
- Set applicable\_daily\_amount from (component\_amount ÷ payment\_days).
- Return (applicable\_daily\_amount ÷ standard\_working\_hours).

**Methods declared on this owner** [make salary slip](operations-035.md#op-83b092d099411d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L6131) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1390) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L4)
