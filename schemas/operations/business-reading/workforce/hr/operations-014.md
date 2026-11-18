# Employment and attendance · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Employee separation

[Record definition](../../../../data/record-types/employee_separation.json)

<a id="op-29ae5dbe52f4d5"></a>
### Employee Separation.validate

`operation_workforce_human_resources_record_definitions_employee_separation_business_behavior_employee_separation_validate`

**Inputs** self.

**Local steps**

- Evaluate super().validate().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L3972) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L655) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L635)

<a id="op-ea519cc7cf8a93"></a>
### Employee Separation.on submit

`operation_workforce_human_resources_record_definitions_employee_separation_business_behavior_employee_separation_on_submit`

**Inputs** self.

**Local steps**

- Evaluate super().on\_submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L4028) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L653) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L633)

<a id="op-9da7825d1ce39e"></a>
### Employee Separation.on update after submit

`operation_workforce_human_resources_record_definitions_employee_separation_business_behavior_employee_separation_on_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.create\_task\_and\_notify\_user().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L4084) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L654) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L634)

<a id="op-18bf1f5071415b"></a>
### Employee Separation.on cancel

`operation_workforce_human_resources_record_definitions_employee_separation_business_behavior_employee_separation_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate super().on\_cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L4133) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L652) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L632)

## Record · Employee separation template

[Record definition](../../../../data/record-types/employee_separation_template.json)

<a id="op-1ec16ce96ae62c"></a>
### Get data

`operation_workforce_human_resources_record_definitions_employee_separation_template_employee_separation_template_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “employee\_separation\_template”, “transactions” → list(mapping(“items” → list(“Employee Separation”)))).

**Local steps**

- Return mapping(“fieldname” → “employee\_separation\_template”, “transactions” → list(mapping(“items” → list(“Employee Separation”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L4812) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L656) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L636)

## Record · Employee transfer

[Record definition](../../../../data/record-types/employee_transfer.json)

<a id="op-a2f95431d95c66"></a>
### Employee Transfer.before submit

`operation_workforce_human_resources_record_definitions_employee_transfer_business_behavior_employee_transfer_before_submit`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.DocstatusTransitionError — translated “Employee Transfer cannot be submitted before Transfer Date”.

**Local steps**

- If getdate(self.transfer\_date) &gt; getdate().
  - Call the validation error handler Platform.throw(translated “Employee Transfer cannot be submitted before Transfer Date”, Platform.DocstatusTransitionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L4906) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L659) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L639)

<a id="op-8eb27a3df71e49"></a>
### Employee Transfer.on submit

`operation_workforce_human_resources_record_definitions_employee_transfer_business_behavior_employee_transfer_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “Employee” via get\_doc.

**State and service calls** request copy\_doc for employee · call db\_set on employee · call insert on new\_employee · call db\_set on self · call save on employee.

**Local steps**

- Set employee from Platform.get\_doc(“Employee”, self.employee).
- If self.create\_new\_employee\_id.
  - Set new\_employee from Platform.copy\_doc(employee).
  - Set new\_employee.name from no value.
  - Set new\_employee.employee\_number from no value.
  - Set new\_employee from update\_employee\_work\_history(new\_employee, self.transfer\_details, date = self.transfer\_date).
  - If (self.new\_company and self.company differs from self.new\_company).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.new\_company → self.company differs from self.new\_company.
    - Set new\_employee.internal\_work\_history from list().
    - Set new\_employee.date\_of\_joining from self.transfer\_date.
    - Set new\_employee.company from self.new\_company.
  - If (employee.user\_id and not self.validate\_user\_in\_details()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in employee.user\_id → not self.validate\_user\_in\_details().
    - Set new\_employee.user\_id from employee.user\_id.
    - Evaluate employee.db\_set(“user\_id”, empty text).
  - Evaluate new\_employee.insert().
  - Evaluate self.db\_set(“new\_employee\_id”, new\_employee.name).
  - Evaluate employee.db\_set(“relieving\_date”, self.transfer\_date).
  - Evaluate employee.db\_set(“status”, “Left”).
- Otherwise.
  - Set employee from update\_employee\_work\_history(employee, self.transfer\_details, date = self.transfer\_date).
  - If (self.new\_company and self.company differs from self.new\_company).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.new\_company → self.company differs from self.new\_company.
    - Set employee.company from self.new\_company.
    - Set employee.date\_of\_joining from self.transfer\_date.
  - Evaluate employee.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate user in details](operations-014.md#op-e87adc8b1d338c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L5032) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L661) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L641)

<a id="op-e7ca9c50220850"></a>
### Employee Transfer.on cancel

`operation_workforce_human_resources_record_definitions_employee_transfer_business_behavior_employee_transfer_on_cancel`

**Inputs** self.

**Record and data access** resolve a document from “Employee” via get\_doc.

**State and service calls** call save on employee.

**Explicit failure paths** validation helper — translated “Please delete the Employee {0} to cancel this document”.format(formatted text &lt;a href='/app/Form/Employee/{self.new\_employee\_id}'&gt;{self.new\_employee\_id}&lt;/a&gt;).

**Local steps**

- Set employee from Platform.get\_doc(“Employee”, self.employee).
- If self.create\_new\_employee\_id.
  - If self.new\_employee\_id.
    - Call the validation error handler Platform.throw(translated “Please delete the Employee {0} to cancel this document”.format(formatted text &lt;a href='/app/Form/Employee/{self.new\_employee\_id}'&gt;{self.new\_employee\_id}&lt;/a&gt;)).
  - Set employee.status from “Active”.
  - Set employee.relieving\_date from empty text.
- Otherwise.
  - Set employee from update\_employee\_work\_history(employee, self.transfer\_details, date = self.transfer\_date, cancel = true).
- If self.new\_company differs from self.company.
  - Set employee.company from self.company.
- Evaluate employee.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L5706) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L660) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L640)

<a id="op-e87adc8b1d338c"></a>
### Employee Transfer.validate user in details

`operation_workforce_human_resources_record_definitions_employee_transfer_business_behavior_employee_transfer_validate_user_in_details`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- For each item in self.transfer\_details.
  - If (item.fieldname equals “user\_id” and item.new differs from item.current).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.fieldname equals “user\_id” → item.new differs from item.current.
    - Return true.
- Return false.

[Applicable decision contract](../../../workforce-decision-contracts/part-0025.json#L6070) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L662) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L642)

## Service · Employees by age

<a id="op-26ce3b282959fa"></a>
### Get data

`operation_workforce_human_resources_dashboard_chart_source_employees_by_age_business_behavior_get_data`

**Inputs** chart\_name = no value, chart = no value, no\_cache = no value, filters = no value, from\_date = no value, to\_date = no value, timespan = no value, time\_interval = no value, heatmap\_year = no value.

**Wrappers, in declaration order** Platform.whitelist(), cache\_source.

**Declared result** dict at tuple(str, list).

**Record and data access** read “Employee” via get\_list.

**Explicit results** mapping(“labels” → age\_range, “datasets” → list(mapping(“name” → translated “Employees”, “values” → values))).

**Local steps**

- If filters.
  - Set filters from Platform.parse\_json(filters).
- Set employees from Platform.db.get\_list(“Employee”, filters = mapping(“company” → filters.get(“company”), “status” → “Active”), pluck = “date\_of\_birth”).
- Set age\_list from get\_age\_list(employees).
- Set ranges from get\_ranges().
- Set tuple(age\_range, values) from get\_employees\_by\_age(age\_list, ranges).
- Return mapping(“labels” → age\_range, “datasets” → list(mapping(“name” → translated “Employees”, “values” → values))).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L298) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L298)

<a id="op-ff756f8cb751fc"></a>
### Get ranges

`operation_workforce_human_resources_dashboard_chart_source_employees_by_age_business_behavior_get_ranges`

**Inputs** no declared parameters.

**Declared result** list at tuple at tuple(int, int).

**Explicit results** ranges.

**Local steps**

- Set ranges from list().
- For each i in range(15, 80, 5).
  - Evaluate ranges.append(tuple(i, (i + 4))).
- Evaluate ranges.append(80).
- Return ranges.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L598) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L300) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L300)

<a id="op-d6f6a9a91e6bdb"></a>
### Get age list

`operation_workforce_human_resources_dashboard_chart_source_employees_by_age_business_behavior_get_age_list`

**Inputs** employees.

**Declared result** list at int.

**Explicit results** age\_list.

**Local steps**

- Set age\_list from list().
- For each dob in employees.
  - If not dob.
    - Continue with the next iteration or loop test.
  - Set age from relativedelta(getdate(), getdate(dob)).years.
  - Evaluate age\_list.append(age).
- Return age\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L765) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L297) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L297)

<a id="op-fc01a378789230"></a>
### Get employees by age

`operation_workforce_human_resources_dashboard_chart_source_employees_by_age_business_behavior_get_employees_by_age`

**Inputs** age\_list, ranges.

**Declared result** tuple at tuple(list at str, list at int).

**Explicit results** tuple(age\_range, values).

**Local steps**

- Set age\_range from list().
- Set values from list().
- For each bracket in ranges.
  - If isinstance(bracket, int).
    - Evaluate age\_range.append(formatted text {bracket}+).
  - Otherwise.
    - Evaluate age\_range.append(formatted text {bracket at 0}-{bracket at 1}).
  - Set count from 0.
  - For each age in age\_list.
    - If ((isinstance(bracket, int) and age ≥ bracket) or (isinstance(bracket, tuple) and bracket at 0 ≤ age ≤ bracket at 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (isinstance(bracket, int) and age ≥ bracket) → (isinstance(bracket, tuple) and bracket at 0 ≤ age ≤ bracket at 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(bracket, int) → age ≥ bracket.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(bracket, tuple) → bracket at 0 ≤ age ≤ bracket at 1.
      - Compare adjacent operands in order, stopping at the first false comparison in bracket at 0 ≤ age ≤ bracket at 1.
      - Update count using + 1.
  - Evaluate values.append(count).
- Return tuple(age\_range, values).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L939) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L299) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L299)

## Report · Employees working on a holiday

<a id="op-7054950be505cd"></a>
### Execute

`operation_workforce_human_resources_report_employees_working_on_a_holiday_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0086.json#L2034) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L4) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L353)

<a id="op-bb841d0eecb940"></a>
### Get columns

`operation_workforce_human_resources_report_employees_working_on_a_holiday_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Employee”, “fieldtype” → “Link”, “fieldname” → “employee”, “options” → “Employee”, …), mapping(“label” → translated “Employee Name”, “fieldtype” → “Data”, “width” → 0, “h ….

**Local steps**

- Return list(mapping(“label” → translated “Employee”, “fieldtype” → “Link”, “fieldname” → “employee”, “options” → “Employee”, …), mapping(“label” → translated “Employee Name”, “fieldtype” → “Data”, “width” → 0, “h ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0086.json#L2160) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L5) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L354)

<a id="op-4918aa7a2dfa0b"></a>
### Get data

`operation_workforce_human_resources_report_employees_working_on_a_holiday_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Employee” via get\_list.

**Explicit results** list() · list of list(row.employee, row.employee\_name, row.attendance\_date, row.status, …) for row drawn from attendance where holiday bound to holiday\_map.get(tuple(row.employee, getdate(row.attendance\_date))).

**Local steps**

- Set employee\_filters from mapping(“company” → filters.company).
- If filters.department.
  - Set employee\_filters at “department” from filters.department.
- Set employees from Platform.get\_list(“Employee”, filters = employee\_filters, fields = list(“name”, “company”)).
- Set holiday\_list\_ranges from get\_holiday\_list\_ranges\_for\_employees(mapping of employee.name → employee.company for employee drawn from employees, filters.from\_date, filters.to\_date).
  - Draw employee from employees.
- Set holiday\_map from mapping of tuple(employee, getdate(holiday.holiday\_date)) → holiday for tuple(employee, holidays) drawn from get\_holidays\_in\_ranges\_map(holiday\_list\_ranges).items(), then holiday drawn from holidays where  ….
  - Draw tuple(employee, holidays) from get\_holidays\_in\_ranges\_map(holiday\_list\_ranges).items().
  - Draw holiday from holidays, keep a combination only if ((not filters.holiday\_list or holiday.parent equals filters.holiday\_list)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not filters.holiday\_list → holiday.parent equals filters.holiday\_list.
- If not holiday\_map.
  - Return list().
- Set Attendance from Platform.qb.DocType(“Attendance”).
- Set attendance from nested operand in the contract(nested operand in the contract).orderby(Attendance.employee).orderby(Attendance.attendance\_date).run(as\_dict = true).
  - Draw tuple(employee, \_) from holiday\_map.
- Return list of list(row.employee, row.employee\_name, row.attendance\_date, row.status, …) for row drawn from attendance where holiday bound to holiday\_map.get(tuple(row.employee, getdate(row.attendance\_date))).
  - Draw row from attendance, keep a combination only if (holiday bound to holiday\_map.get(tuple(row.employee, getdate(row.attendance\_date)))).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L77) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L6) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L355)

## Record · Exit interview

[Record definition](../../../../data/record-types/exit_interview.json)

<a id="op-6fe6d29646d975"></a>
### Exit Interview.validate

`operation_workforce_human_resources_record_definitions_exit_interview_business_behavior_exit_interview_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_relieving\_date().
- Evaluate self.validate\_duplicate\_interview().
- Evaluate self.set\_employee\_email().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate relieving date](operations-014.md#op-6e744450cfd48d), [validate duplicate interview](operations-014.md#op-0ad27acf603acb), [set employee email](operations-014.md#op-313be1733e2576).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L1453) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L675) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L655)

<a id="op-6e744450cfd48d"></a>
### Exit Interview.validate relieving date

`operation_workforce_human_resources_record_definitions_exit_interview_business_behavior_exit_interview_validate_relieving_date`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “Please set the relieving date for employee {0}”.format(get\_link\_to\_form(“Employee”, self.employee)).

**Local steps**

- If not Platform.db.get\_value(“Employee”, self.employee, “relieving\_date”).
  - Call the validation error handler Platform.throw(translated “Please set the relieving date for employee {0}”.format(get\_link\_to\_form(“Employee”, self.employee)), title = translated “Relieving Date Missing”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L1544) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L677) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L657)

<a id="op-0ad27acf603acb"></a>
### Exit Interview.validate duplicate interview

`operation_workforce_human_resources_record_definitions_exit_interview_business_behavior_exit_interview_validate_duplicate_interview`

**Inputs** self.

**Record and data access** read “Exit Interview” via exists.

**Explicit failure paths** validation helper with Platform.DuplicateEntryError — translated “Exit Interview {0} already exists for Employee: {1}”.format(get\_link\_to\_form(“Exit Interview”, doc), Platform.bold(self.employee)).

**Local steps**

- Set doc from Platform.db.exists(“Exit Interview”, mapping(“employee” → self.employee, “name” → tuple(“!=”, self.name), “docstatus” → tuple(“!=”, 2))).
- If doc.
  - Call the validation error handler Platform.throw(translated “Exit Interview {0} already exists for Employee: {1}”.format(get\_link\_to\_form(“Exit Interview”, doc), Platform.bold(self.employee)), Platform.DuplicateEntryError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L1738) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L676) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L656)

<a id="op-313be1733e2576"></a>
### Exit Interview.set employee email

`operation_workforce_human_resources_record_definitions_exit_interview_business_behavior_exit_interview_set_employee_email`

**Inputs** self.

**Record and data access** resolve a document from “Employee” via get\_doc.

**Local steps**

- Set employee from Platform.get\_doc(“Employee”, self.employee).
- Set self.email from get\_employee\_email(employee).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L2011) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L673) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L653)

<a id="op-07edf9873a4951"></a>
### Exit Interview.on submit

`operation_workforce_human_resources_record_definitions_exit_interview_business_behavior_exit_interview_on_submit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Only Completed documents can be submitted”.

**Local steps**

- <a id="op-07edf9873a4951-guard-2"></a>If self.status differs from “Completed”.
  - Call the validation error handler Platform.throw(translated “Only Completed documents can be submitted”).
- Evaluate self.update\_interview\_date\_in\_employee().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status differs from “Completed”, self.status = “Pending” selects the branch that calls the validation-error handler with translated “Only Completed documents can be submitted”. With self.status = “Completed”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-07edf9873a4951-guard-2)

**Methods declared on this owner** [update interview date in employee](operations-014.md#op-fc060c5bf61667).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L2116) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L672) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L652)

<a id="op-04a9ed1a897318"></a>
### Exit Interview.on cancel

`operation_workforce_human_resources_record_definitions_exit_interview_business_behavior_exit_interview_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.update\_interview\_date\_in\_employee().
- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update interview date in employee](operations-014.md#op-fc060c5bf61667).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L2232) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L670) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L650)

<a id="op-a9998f7404da38"></a>
### Exit Interview.on discard

`operation_workforce_human_resources_record_definitions_exit_interview_business_behavior_exit_interview_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L2316) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L671) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L651)

<a id="op-fc060c5bf61667"></a>
### Exit Interview.update interview date in employee

`operation_workforce_human_resources_record_definitions_exit_interview_business_behavior_exit_interview_update_interview_date_in_employee`

**Inputs** self.

**State and service calls** request set\_value on “Employee”.

**Local steps**

- If self.docstatus equals 1.
  - Evaluate Platform.db.set\_value(“Employee”, self.employee, “held\_on”, self.date).
- Otherwise.
  - If self.docstatus equals 2.
    - Evaluate Platform.db.set\_value(“Employee”, self.employee, “held\_on”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0026.json#L2379) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L674) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L654)
