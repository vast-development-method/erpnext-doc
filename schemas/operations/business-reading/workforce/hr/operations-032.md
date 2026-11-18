# Employment and attendance · operations 32

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Leave policy assignment

[Record definition](../../../../data/record-types/leave_policy_assignment.json)

<a id="op-ed95f08eda0701"></a>
### Create assignment for multiple employees

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_create_assignment_for_multiple_employees`

**Inputs** employees, data.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** list at str.

**State and service calls** savepoint savepoint · call submit on assignment · rollback.

**Explicit results** docs\_name.

**Local steps**

- If isinstance(employees, str).
  - Set employees from json.loads(employees).
- If isinstance(data, str).
  - Set data from Platform.\_dict(json.loads(data)).
- Set docs\_name from list().
- Set failed from list().
- For each employee in employees.
  - Set savepoint from “before\_assignment\_submission”.
  - Attempt the following.
    - Evaluate Platform.db.savepoint(savepoint).
    - Set assignment from create\_assignment(employee, Platform.\_dict(data)).
    - Evaluate assignment.submit().
  - On failure (Exception).
    - Evaluate Platform.db.rollback(save\_point = savepoint).
    - Evaluate Platform.log\_error(title = “Leave Policy Assignment failed”, reference\_doctype = “Leave Policy Assignment”, reference\_name = employee).
    - Evaluate failed.append(employee).
    - Continue with the next iteration or loop test.
  - Evaluate docs\_name.append(assignment.name).
- If failed.
  - Evaluate show\_assignment\_submission\_status(failed).
- Return docs\_name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0062.json#L3008) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1345) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1321)

<a id="op-ba8538f7240b9e"></a>
### Create assignment

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_create_assignment`

**Inputs** employee, data.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** Document.

**State and service calls** request new\_doc for “Leave Policy Assignment” · call save on assignment.

**Explicit results** assignment.

**Local steps**

- Set assignment from Platform.new\_doc(“Leave Policy Assignment”).
- Set assignment.employee from employee.
- Set assignment.assignment\_based\_on from (data.assignment\_based\_on or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.assignment\_based\_on → no value.
- Set assignment.leave\_policy from data.leave\_policy.
- Set assignment.effective\_from from (getdate(data.effective\_from) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate(data.effective\_from) → no value.
- Set assignment.effective\_to from (getdate(data.effective\_to) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate(data.effective\_to) → no value.
- Set assignment.leave\_period from (data.leave\_period or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.leave\_period → no value.
- Set assignment.carry\_forward from data.carry\_forward.
- Evaluate assignment.save().
- Return assignment.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0062.json#L3598) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1344) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1320)

<a id="op-5694a522ddcc7f"></a>
### Show assignment submission status

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_show_assignment_submission_status`

**Inputs** failed\_employees.

**State and service calls** msgprint with msg.

**Local steps**

- Evaluate Platform.clear\_messages().
- Set employee\_links from list of get\_link\_to\_form(“Employee”, employee) for employee drawn from failed\_employees.
  - Draw employee from failed\_employees.
- Set msg from translated “Leave policy could not be assigned to the following employees:”.
- Update msg using + ((one space + comma\_and(employee\_links, false)) + text in the contract).
- Update msg using + translated “Check {0} for more details”.format(text in the contract).format(translated “Error Log”).
- Evaluate Platform.msgprint(msg, indicator = “red”, title = translated “Assignment Failed”, is\_minimizable = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0062.json#L3948) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1362) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1338)

<a id="op-2d535f83045e0e"></a>
### Get leave type details

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_get_leave_type_details`

**Inputs** no declared parameters.

**Record and data access** read “Leave Type” via get\_all.

**Explicit results** leave\_type\_details.

**Local steps**

- Set leave\_type\_details from Platform.\_dict().
- Set leave\_types from Platform.get\_all(“Leave Type”, fields = list(“name”, “is\_lwp”, “is\_earned\_leave”, “is\_compensatory”, …)).
- For each d in leave\_types.
  - Evaluate leave\_type\_details.setdefault(d.name, d).
- Return leave\_type\_details.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L59) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1346) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1322)

<a id="op-f1f931a97731f6"></a>
### Get data

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_leave_policy_assignment_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “leave\_policy\_assignment”, “transactions” → list(mapping(“label” → translated “Leaves”, “items” → list(“Leave Allocation”)))).

**Local steps**

- Return mapping(“fieldname” → “leave\_policy\_assignment”, “transactions” → list(mapping(“label” → translated “Leaves”, “items” → list(“Leave Allocation”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0062.json#L4510) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1363) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1339)

## Record · Leave type

[Record definition](../../../../data/record-types/leave_type.json)

<a id="op-6a13527938fca4"></a>
### Leave Type.validate

`operation_workforce_human_resources_record_definitions_leave_type_business_behavior_leave_type_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_lwp().
- Evaluate self.validate\_leave\_types().
- Evaluate self.validate\_allocated\_earned\_leave().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate lwp](operations-032.md#op-2664b063c8393e), [validate leave types](operations-032.md#op-892107d26ed0ca), [validate allocated earned leave](operations-032.md#op-95501c2a66e062).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0063.json#L6493) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1381) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1357)

<a id="op-2664b063c8393e"></a>
### Leave Type.validate lwp

`operation_workforce_human_resources_record_definitions_leave_type_business_behavior_leave_type_validate_leave_without_pay`

**Inputs** self.

**Record and data access** read “Leave Allocation” via get\_all.

**Explicit failure paths** validation helper — translated “Leave application is linked with leave allocations {0}. Leave application cannot be set as leave without pay”.format(“, ”.join(leave\_allocation)).

**Local steps**

- If self.is\_lwp.
  - Set leave\_allocation from Platform.get\_all(“Leave Allocation”, filters = mapping(“leave\_type” → self.name, “from\_date” → tuple(“&lt;=”, today()), “to\_date” → tuple(“&gt;=”, today())), fields = list(“name”)).
  - Set leave\_allocation from list of l at “name” for l drawn from leave\_allocation.
    - Draw l from leave\_allocation.
  - If leave\_allocation.
    - Call the validation error handler Platform.throw(translated “Leave application is linked with leave allocations {0}. Leave application cannot be set as leave without pay”.format(“, ”.join(leave\_allocation))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../workforce-decision-contracts/part-0063.json#L6584) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1384) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1360)

<a id="op-892107d26ed0ca"></a>
### Leave Type.validate leave types

`operation_workforce_human_resources_record_definitions_leave_type_business_behavior_leave_type_validate_leave_types`

**Inputs** self.

**Explicit failure paths** validation helper — msg · validation helper — translated “Leave Type can either be without pay or partial pay” · validation helper — translated “The fraction of Daily Salary per Leave should be between 0 and 1”.

**Local steps**

- If (self.is\_compensatory and self.is\_earned\_leave).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_compensatory → self.is\_earned\_leave.
  - Set msg from (translated “Leave Type can either be compensatory or earned leave.” + text in the contract).
  - Update msg using + (translated “Earned Leaves are allocated as per the configured frequency via scheduler.” + text in the contract).
  - Update msg using + translated “Whereas allocation for Compensatory Leaves is automatically created or updated on submission of Compensatory …”.
  - Update msg using + text in the contract.
  - Update msg using + translated “Disable {0} or {1} to proceed.”.format(bold(translated “Is Compensatory Leave”), bold(translated “Is Earned Leave”)).
  - Call the validation error handler Platform.throw(msg, title = translated “Not Allowed”).
- If (self.is\_lwp and self.is\_ppl).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_lwp → self.is\_ppl.
  - Call the validation error handler Platform.throw(translated “Leave Type can either be without pay or partial pay”, title = translated “Not Allowed”).
- If (self.is\_ppl and (self.fraction\_of\_daily\_salary\_per\_leave &lt; 0 or self.fraction\_of\_daily\_salary\_per\_leave &gt; 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_ppl → (self.fraction\_of\_daily\_salary\_per\_leave &lt; 0 or self.fraction\_of\_daily\_salary\_per\_leave &gt; 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.fraction\_of\_daily\_salary\_per\_leave &lt; 0 → self.fraction\_of\_daily\_salary\_per\_leave &gt; 1.
  - Call the validation error handler Platform.throw(translated “The fraction of Daily Salary per Leave should be between 0 and 1”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1383) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1359)

<a id="op-95501c2a66e062"></a>
### Leave Type.validate allocated earned leave

`operation_workforce_human_resources_record_definitions_leave_type_business_behavior_leave_type_validate_allocated_earned_leave`

**Inputs** self.

**Record and data access** read “Leave Allocation” via exists.

**State and service calls** msgprint.

**Local steps**

- Set old\_configuration from self.get\_doc\_before\_save().
- If (old\_configuration and old\_configuration.is\_earned\_leave and old\_configuration.max\_leaves\_allowed &gt; self.max\_leaves\_allowed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_configuration → old\_configuration.is\_earned\_leave → old\_configuration.max\_leaves\_allowed &gt; self.max\_leaves\_allowed.
  - Set earned\_leave\_allocation\_exists from Platform.db.exists(“Leave Allocation”, mapping(“leave\_type” → self.name, “from\_date” → tuple(“&lt;=”, today()), “to\_date” → tuple(“&gt;=”, today())), cache = true).
  - If earned\_leave\_allocation\_exists.
    - Evaluate Platform.msgprint(title = translated “Leave Allocation Exists”, msg = translated “Reducing maximum leaves allowed after allocation may cause scheduler to allocate incorrect number of earned  …”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L514) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1382) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1358)

<a id="op-00d713dedb0c9a"></a>
### Leave Type.clear cache

`operation_workforce_human_resources_record_definitions_leave_type_business_behavior_leave_type_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Bind dependencies LEAVE\_TYPE\_MAP.
- Evaluate Platform.cache().delete\_value(LEAVE\_TYPE\_MAP).
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L838) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1380) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1356)

<a id="op-15edf23a4cdf75"></a>
### Get data

`operation_workforce_human_resources_record_definitions_leave_type_leave_type_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “leave\_type”, “transactions” → list(mapping(“items” → list(“Leave Allocation”, “Leave Application”)), mapping(“items” → list(“Attendance”, “Leave Encashment”)))).

**Local steps**

- Return mapping(“fieldname” → “leave\_type”, “transactions” → list(mapping(“items” → list(“Leave Allocation”, “Leave Application”)), mapping(“items” → list(“Attendance”, “Leave Encashment”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L938) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1385) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1361)

## Report · Monthly attendance sheet

<a id="op-07c898ad4a7aba"></a>
### Execute

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_execute`

**Inputs** filters = no value.

**Declared result** tuple.

**State and service calls** msgprint with translated “No attendance records found.” · msgprint with translated “No attendance records found for this criteria.”.

**Explicit results** tuple(list(), list(), no value, no value) · tuple(columns, list(), no value, no value) · tuple(columns, data, message, chart).

**Explicit failure paths** validation helper — translated “Please select Filter Based On” · validation helper — translated “Please select month and year.” · validation helper — translated “Please set the date range.” · validation helper — translated “Start date cannot be greater than end date.” · validation helper — translated “Please set a date range less than 90 days.” · 1 additional forms in the steps below.

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- If not filters.filter\_based\_on.
  - Call the validation error handler Platform.throw(translated “Please select Filter Based On”).
- If (filters.filter\_based\_on equals “Month” and not (filters.month and filters.year)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.filter\_based\_on equals “Month” → not (filters.month and filters.year).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.month → filters.year.
  - Call the validation error handler Platform.throw(translated “Please select month and year.”).
- If filters.filter\_based\_on equals “Date Range”.
  - If not (filters.start\_date and filters.end\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.start\_date → filters.end\_date.
    - Call the validation error handler Platform.throw(translated “Please set the date range.”).
  - If getdate(filters.start\_date) &gt; getdate(filters.end\_date).
    - Call the validation error handler Platform.throw(translated “Start date cannot be greater than end date.”).
  - If date\_diff(filters.end\_date, filters.start\_date) &gt; 90.
    - Call the validation error handler Platform.throw(translated “Please set a date range less than 90 days.”).
- If not filters.company.
  - Call the validation error handler Platform.throw(translated “Please select company.”).
- If filters.company.
  - Set filters.companies from list(filters.company).
  - If filters.include\_company\_descendants.
    - Evaluate filters.companies.extend(get\_descendants\_of(“Company”, filters.company)).
- Set attendance\_map from get\_attendance\_map(filters).
- If not attendance\_map.
  - Evaluate Platform.msgprint(translated “No attendance records found.”, alert = true, indicator = “orange”).
  - Return tuple(list(), list(), no value, no value).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters, attendance\_map).
- If not data.
  - Evaluate Platform.msgprint(translated “No attendance records found for this criteria.”, alert = true, indicator = “orange”).
  - Return tuple(columns, list(), no value, no value).
- Set message from get\_message() when not filters.summarized\_view, otherwise empty text.
  - Value choice on not filters.summarized\_view — true gives get\_message(), false gives empty text.
- Set chart from get\_chart\_data(attendance\_map, filters).
- Return tuple(columns, data, message, chart).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0087.json#L3483) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L20) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L369)

<a id="op-132a8d7f90932d"></a>
### Get message

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_message`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** message.

**Local steps**

- Set message from empty text.
- Set colors from list(“green”, “red”, “orange”, “#914EE3”, …).
- Set count from 0.
- For each tuple(status, abbr) in status\_map.items().
  - Update message using + formatted text   &lt;span style='border-left: 2px solid {colors at count}; padding-right: 12px; padding-left: 5px; margin-right: 3px;'&gt;  {translated status} - {abb.
  - Update count using + 1.
- Return message.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0087.json#L4531) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L40) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L389)

<a id="op-1c0d9119bba326"></a>
### Get columns

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_columns`

**Inputs** filters.

**Declared result** list at dict.

**Explicit results** columns.

**Local steps**

- Set columns from list().
- If filters.group\_by.
  - Set options\_mapping from mapping(“Branch” → “Branch”, “Grade” → “Employee Grade”, “Department” → “Department”, “Designation” → “Designation”).
  - Set options from options\_mapping.get(filters.group\_by).
  - Evaluate columns.append(mapping(“label” → translated filters.group\_by, “fieldname” → Platform.scrub(filters.group\_by), “fieldtype” → “Link”, “options” → options, …)).
- Evaluate columns.extend(list(mapping(“label” → translated “Employee”, “fieldname” → “employee”, “fieldtype” → “Link”, “options” → “Employee”, …), mapping(“label” → translated “Employee Name”, “fieldname” → “employe ….
- If filters.summarized\_view.
  - Evaluate columns.extend(list(mapping(“label” → translated “Total Present”, “fieldname” → “total\_present”, “fieldtype” → “Float”, “width” → 110), mapping(“label” → translated “Total Leaves”, “fieldname” → “total\_lea ….
  - Evaluate columns.extend(get\_columns\_for\_leave\_types()).
  - Evaluate columns.extend(list(mapping(“label” → translated “Total Late Entries”, “fieldname” → “total\_late\_entries”, “fieldtype” → “Float”, “width” → 140), mapping(“label” → translated “Total Early Exits”, “fieldnam ….
- Otherwise.
  - Evaluate columns.append(mapping(“label” → translated “Shift”, “fieldname” → “shift”, “fieldtype” → “Data”, “width” → 120)).
  - Evaluate columns.extend(get\_columns\_for\_days(filters)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0087.json#L4766) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L28) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L377)

<a id="op-7f13d0e484c4d6"></a>
### Get columns for leave types

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_columns_for_leave_types`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Record and data access** read “Leave Type” via get\_all.

**Explicit results** types.

**Local steps**

- Set leave\_types from Platform.db.get\_all(“Leave Type”, pluck = “name”).
- Set types from list().
- For each entry in leave\_types.
  - Evaluate types.append(mapping(“label” → entry, “fieldname” → Platform.scrub(entry), “fieldtype” → “Float”, “width” → 120)).
- Return types.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0087.json#L6160) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L30) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L379)

<a id="op-680c3800d45a5f"></a>
### Get columns for days

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_columns_for_days`

**Inputs** filters.

**Declared result** list at dict.

**Explicit results** days.

**Local steps**

- Set days from list().
- Set dates\_in\_period from get\_dates\_in\_period(filters).
- For each d in dates\_in\_period.
  - Set d from getdate(d).
  - Set abbr\_weekday from day\_abbr at d.weekday().
  - Set label from formatted text {d.day} {abbr\_weekday}.
  - Evaluate days.append(mapping(“label” → label, “fieldtype” → “Data”, “fieldname” → d.strftime(“%d-%m-%Y”), “width” → 65)).
- Return days.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0087.json#L6390) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L29) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L378)

<a id="op-8fe315324d95d0"></a>
### Get dates in period

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_dates_in_period`

**Inputs** filters.

**Declared result** list at str.

**Explicit results** dates\_in\_period.

**Local steps**

- Set dates\_in\_period from list().
- If filters.filter\_based\_on equals “Month”.
  - Set total\_days from get\_total\_days\_in\_month(filters).
  - Set dates\_in\_period from list of formatted text {cstr(filters.year)}-{cstr(filters.month)}-{cstr(day)} for day drawn from range(1, (total\_days + 1)).
    - Draw day from range(1, (total\_days + 1)).
- If filters.filter\_based\_on equals “Date Range”.
  - Set dates\_in\_period from get\_date\_range(filters.start\_date, filters.end\_date).
- Return dates\_in\_period.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0087.json#L6707) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L34) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L383)

<a id="op-a4f31b80020c11"></a>
### Get total days in month

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_total_days_in_month`

**Inputs** filters.

**Declared result** int.

**Explicit results** monthrange(cint(filters.year), cint(filters.month)) at 1.

**Local steps**

- Return monthrange(cint(filters.year), cint(filters.month)) at 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0087.json#L7039) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L42) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L391)

<a id="op-58e4925e6406fb"></a>
### Get date condition

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_date_condition`

**Inputs** docfield, filters.

**Declared result** Criterion.

**Explicit results** (Extract(“month”, docfield) equals filters.month bitwise and Extract(“year”, docfield) equals filters.year) · (docfield ≥ filters.start\_date bitwise and docfield ≤ filters.end\_date).

**Local steps**

- If filters.filter\_based\_on equals “Month”.
  - Return (Extract(“month”, docfield) equals filters.month bitwise and Extract(“year”, docfield) equals filters.year).
- If filters.filter\_based\_on equals “Date Range”.
  - Return (docfield ≥ filters.start\_date bitwise and docfield ≤ filters.end\_date).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0087.json#L7143) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L32) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L381)

<a id="op-0ae3c3580541c9"></a>
### Get data

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_data`

**Inputs** filters, attendance\_map.

**Declared result** list at dict.

**Explicit results** data.

**Local steps**

- Set tuple(employee\_details, group\_by\_param\_values) from get\_employee\_related\_details(filters).
- If filters.group\_by.
  - Set ungrouped\_employee\_details from mapping().
  - For each details in employee\_details.values().
    - Evaluate ungrouped\_employee\_details.update(details).
- Otherwise.
  - Set ungrouped\_employee\_details from employee\_details.
- Set employee\_holiday\_map from get\_employee\_holiday\_map(ungrouped\_employee\_details, filters).
- Set data from list().
- If filters.group\_by.
  - Set group\_by\_column from Platform.scrub(filters.group\_by).
  - For each value in group\_by\_param\_values.
    - If not value.
      - Continue with the next iteration or loop test.
    - Set records from get\_rows(employee\_details at value, filters, employee\_holiday\_map, attendance\_map).
    - If records.
      - Evaluate data.append(mapping(group\_by\_column → value)).
      - Evaluate data.extend(records).
- Otherwise.
  - Set data from get\_rows(employee\_details, filters, employee\_holiday\_map, attendance\_map).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0088.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L31) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L380)

<a id="op-6d7cb004c49a34"></a>
### Get attendance map

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_attendance_map`

**Inputs** filters.

**Declared result** dict.

**Explicit results** attendance\_map.

**Local steps**

- Set attendance\_list from get\_attendance\_records(filters).
- Set attendance\_map from mapping().
- Set leave\_map from mapping().
- For each d in attendance\_list.
  - If d.status equals “On Leave”.
    - Evaluate leave\_map.setdefault(d.employee, mapping()).setdefault(d.shift, list()).append(d.attendance\_date).
    - Continue with the next iteration or loop test.
  - If d.shift is identical to no value.
    - Set d.shift from empty text.
  - Evaluate attendance\_map.setdefault(d.employee, mapping()).setdefault(d.shift, mapping()).
  - Set attendance\_map at d.employee at d.shift at d.attendance\_date from d.status.
- For each tuple(employee, leave\_days) in leave\_map.items().
  - For each tuple(assigned\_shift, dates) in leave\_days.items().
    - If employee does not belong to attendance\_map.
      - Evaluate attendance\_map.setdefault(employee, mapping()).setdefault(assigned\_shift, mapping()).
    - For each d in dates.
      - For each shift in attendance\_map at employee.keys().
        - Set attendance\_map at employee at shift at d from “On Leave”.
- Return attendance\_map.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0088.json#L478) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L21) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L370)

<a id="op-3eb99028962b3d"></a>
### Get attendance records

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_attendance_records`

**Inputs** filters.

**Declared result** list at dict.

**Explicit results** query.run(as\_dict = 1).

**Local steps**

- Set Attendance from Platform.qb.DocType(“Attendance”).
- Set Employee from Platform.qb.DocType(“Employee”).
- Set attendance\_date\_condition from get\_date\_condition(Attendance.attendance\_date, filters).
- Set status from nested operand in the contract().when((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand in the contract), “Half Day/Othe ….
- Set query from nested operand in the contract.qb.from\_(Attendance).select(Attendance.employee, Attendance.attendance\_date, status.as\_(“status”), Attendance.shift).where(((Attendance.docstatus equals 1 bitwise and Attenda ….
- If filters.employee.
  - Set query from query.where(Attendance.employee equals filters.employee).
- If (filters.department or filters.branch or filters.status or filters.employment\_type).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.department → filters.branch → filters.status → filters.employment\_type.
  - Set query from query.join(Employee).on(Attendance.employee equals Employee.name).
  - If (filters.department and filters.department differs from “All Departments”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.department → filters.department differs from “All Departments”.
    - Set query from query.where(Employee.department equals filters.department).
  - If filters.branch.
    - Set query from query.where(Employee.branch equals filters.branch).
  - If filters.status.
    - Set query from query.where(Employee.status equals filters.status).
  - If filters.employment\_type.
    - Set query from query.where(Employee.employment\_type equals filters.employment\_type).
- Set query from query.orderby(Attendance.employee, Attendance.attendance\_date).
- Return query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L78) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L22) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L371)

<a id="op-9a289907da1bd5"></a>
### Get employee related details

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_employee_related_details`

**Inputs** filters.

**Declared result** tuple at tuple(dict, list).

**Explicit results** tuple(emp\_map, group\_by\_param\_values).

**Local steps**

- Set Employee from Platform.qb.DocType(“Employee”).
- Set joining\_date\_condition from get\_date\_condition(Employee.date\_of\_joining, filters).
- Set query from nested operand in the contract.qb.from\_(Employee).select(Employee.name, Employee.employee\_name, Employee.designation, Employee.grade, …).where(Employee.company.isin(filters.companies)).
- If filters.employee.
  - Set query from query.where(Employee.name equals filters.employee).
- If (filters.department and filters.department differs from “All Departments”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.department → filters.department differs from “All Departments”.
  - Set query from query.where(Employee.department equals filters.department).
- If filters.branch.
  - Set query from query.where(Employee.branch equals filters.branch).
- If filters.status.
  - Set query from query.where(Employee.status equals filters.status).
- If filters.employment\_type.
  - Set query from query.where(Employee.employment\_type equals filters.employment\_type).
- Set group\_by from filters.group\_by.
- If group\_by.
  - Set group\_by from group\_by.lower().
  - Set query from query.orderby(group\_by).
- Set employee\_details from query.run(as\_dict = true).
- Set group\_by\_param\_values from list().
- Set emp\_map from mapping().
- If group\_by.
  - Set group\_key from deferred anonymous expression.
  - For each tuple(parameter, employees) in groupby(sorted(employee\_details, key = group\_key), key = group\_key).
    - Evaluate group\_by\_param\_values.append(parameter).
    - Evaluate emp\_map.setdefault(parameter, Platform.\_dict()).
    - For each emp in employees.
      - Set emp\_map at parameter at emp.name from emp.
- Otherwise.
  - For each emp in employee\_details.
    - Set emp\_map at emp.name from emp.
- Return tuple(emp\_map, group\_by\_param\_values).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L80) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L36) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L385)

<a id="op-d4c6e0d0cbecb3"></a>
### Get employee holiday map

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_employee_holiday_map`

**Inputs** employee\_details, filters.

**Declared result** dict at tuple(str, list at dict).

**Explicit results** mapping() · get\_holidays\_in\_ranges\_map(employee\_holiday\_list\_ranges).

**Local steps**

- If not employee\_details.
  - Return mapping().
- Set tuple(start\_date, end\_date) from get\_date\_range\_from\_filters(filters).
- Set employee\_holiday\_list\_ranges from get\_holiday\_list\_ranges\_for\_employees(mapping of employee → details.get(“company”) for tuple(employee, details) drawn from employee\_details.items(), start\_date, end\_date).
  - Draw tuple(employee, details) from employee\_details.items().
- Return get\_holidays\_in\_ranges\_map(employee\_holiday\_list\_ranges).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L79) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L35) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L384)
