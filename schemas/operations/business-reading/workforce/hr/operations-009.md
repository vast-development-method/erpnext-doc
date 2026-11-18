# Employment and attendance · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Employee checkin

[Record definition](../../../../data/record-types/employee_checkin.json)

<a id="op-29051a521d1151"></a>
### Handle attendance exception

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_handle_attendance_exception`

**Inputs** log\_names, error\_message.

**State and service calls** rollback.

**Local steps**

- Evaluate Platform.db.rollback(save\_point = “attendance\_creation”).
- Evaluate Platform.clear\_messages().
- Evaluate skip\_attendance\_in\_checkins(log\_names).
- Evaluate add\_comment\_in\_checkins(log\_names, error\_message).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0020.json#L2867) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L556) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L536)

<a id="op-51e6151f7027e3"></a>
### Add comment in checkins

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_add_comment_in_checkins`

**Inputs** log\_names, error\_message.

**Record and data access** resolve a document from mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → “Employee Checkin”, “reference\_name” → name, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → “Employee Checkin”, “reference\_name” → name, …)).

**Local steps**

- Set text from “{prefix}&lt;br&gt;{error\_message}”.format(prefix = Platform.bold(translated “Reason for skipping auto attendance:”), error\_message = error\_message).
- For each name in log\_names.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → “Employee Checkin”, “reference\_name” → name, …)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0020.json#L3014) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L540) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L520)

<a id="op-6250214ab24296"></a>
### Skip attendance in checkins

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_skip_attendance_in_checkins`

**Inputs** log\_names.

**Local steps**

- Set EmployeeCheckin from Platform.qb.DocType(“Employee Checkin”).
- Evaluate nested operand in the contract(nested operand in the contract).set(“skip\_auto\_attendance”, 1).where(EmployeeCheckin.name.isin(log\_names)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0020.json#L3293) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L558) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L538)

<a id="op-5572e4ec05e2aa"></a>
### Update attendance in checkins

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_update_attendance_in_checkins`

**Inputs** log\_names, attendance\_id.

**Local steps**

- Set EmployeeCheckin from Platform.qb.DocType(“Employee Checkin”).
- Evaluate nested operand in the contract(nested operand in the contract).set(“attendance”, attendance\_id).where(EmployeeCheckin.name.isin(log\_names)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0020.json#L3468) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L560) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L540)

<a id="op-a348b37442a86a"></a>
### Calculate time difference

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_calculate_time_difference`

**Inputs** start\_time, end\_time.

**Explicit results** round((time\_difference.total\_seconds() ÷ 3600), 2).

**Local steps**

- If end\_time &lt; start\_time.
  - Update end\_time using + timedelta(days = 1).
- Set time\_difference from abs((start\_time − end\_time)).
- Return round((time\_difference.total\_seconds() ÷ 3600), 2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0020.json#L3655) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L543) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L523)

## Report · Employee exits

<a id="op-e75ff971c08f9d"></a>
### Execute

`operation_workforce_human_resources_report_employee_exits_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart, …).

**Local steps**

- Set columns from get\_columns().
- Set data from get\_data(filters).
- Set chart from get\_chart\_data(data).
- Set report\_summary from get\_report\_summary(data).
- Return tuple(columns, data, no value, chart, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0081.json#L6010) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1683) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L289)

<a id="op-c662524eae64cb"></a>
### Get columns

`operation_workforce_human_resources_report_employee_exits_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Employee”, “fieldname” → “employee”, “fieldtype” → “Link”, “options” → “Employee”, …), mapping(“label” → translated “Employee Name”, “fieldname” → “employee\_name”, “field ….

**Local steps**

- Return list(mapping(“label” → translated “Employee”, “fieldname” → “employee”, “fieldtype” → “Link”, “options” → “Employee”, …), mapping(“label” → translated “Employee Name”, “fieldname” → “employee\_name”, “field ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0082.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1685) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L291)

<a id="op-adbf148c4fef38"></a>
### Get data

`operation_workforce_human_resources_report_employee_exits_business_behavior_get_data`

**Inputs** filters.

**Explicit results** result.

**Local steps**

- Set employee from Platform.qb.DocType(“Employee”).
- Set interview from Platform.qb.DocType(“Exit Interview”).
- Set fnf from Platform.qb.DocType(“Full and Final Statement”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).distinct().where(((nested operand in the co ….
- Set query from get\_conditions(filters, query, employee, interview, …).
- Set result from query.run(as\_dict = true).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0082.json#L1136) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1687) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L293)

<a id="op-bec4565a1ee584"></a>
### Get conditions

`operation_workforce_human_resources_report_employee_exits_business_behavior_get_conditions`

**Inputs** filters, query, employee, interview, fnf.

**Explicit results** query.

**Local steps**

- If (filters.get(“from\_date”) and filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“from\_date”) → filters.get(“to\_date”).
  - Set query from query.where(employee.relieving\_date at slice getdate(filters.get(“from\_date”)) to getdate(filters.get(“to\_date”))).
- Otherwise.
  - If filters.get(“from\_date”).
    - Set query from query.where(employee.relieving\_date ≥ filters.get(“from\_date”)).
  - Otherwise.
    - If filters.get(“to\_date”).
      - Set query from query.where(employee.relieving\_date ≤ filters.get(“to\_date”)).
- If filters.get(“company”).
  - Set query from query.where(employee.company equals filters.get(“company”)).
- If filters.get(“department”).
  - Set query from query.where(employee.department equals filters.get(“department”)).
- If filters.get(“designation”).
  - Set query from query.where(employee.designation equals filters.get(“designation”)).
- If filters.get(“employee”).
  - Set query from query.where(employee.name equals filters.get(“employee”)).
- If filters.get(“reports\_to”).
  - Set query from query.where(employee.reports\_to equals filters.get(“reports\_to”)).
- If filters.get(“interview\_status”).
  - Set query from query.where(interview.status equals filters.get(“interview\_status”)).
- If filters.get(“final\_decision”).
  - Set query from query.where(interview.employee\_status equals filters.get(“final\_decision”)).
- If filters.get(“exit\_interview\_pending”).
  - Set query from query.where((interview.name equals empty text bitwise or interview.name.isnull())).
- If filters.get(“questionnaire\_pending”).
  - Set query from query.where((interview.reference\_document\_name equals empty text bitwise or interview.reference\_document\_name.isnull())).
- If filters.get(“fnf\_pending”).
  - Set query from query.where((fnf.name equals empty text bitwise or fnf.name.isnull())).
- Return query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0082.json#L2119) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1686) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L292)

<a id="op-f67ce7b2a8429b"></a>
### Get chart data

`operation_workforce_human_resources_report_employee_exits_business_behavior_get_chart_data`

**Inputs** data.

**Explicit results** no value · chart.

**Local steps**

- If not data.
  - Return no value.
- Set retained from 0.
- Set exit\_confirmed from 0.
- Set pending from 0.
- For each entry in data.
  - If entry.employee\_status equals “Employee Retained”.
    - Update retained using + 1.
  - Otherwise.
    - If entry.employee\_status equals “Exit Confirmed”.
      - Update exit\_confirmed using + 1.
    - Otherwise.
      - Update pending using + 1.
- Set chart from mapping(“data” → mapping(“labels” → list(translated “Retained”, translated “Exit Confirmed”, translated “Decision Pending”), “datasets” → list(mapping(“name” → translated “Employee Status”, “values” → list ….
- Return chart.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0082.json#L3478) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1684) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L290)

<a id="op-b0b3802c4382a1"></a>
### Get report summary

`operation_workforce_human_resources_report_employee_exits_business_behavior_get_report_summary`

**Inputs** data.

**Explicit results** no value · list(mapping(“value” → total\_resignations, “label” → translated “Total Resignations”, “indicator” → “Red” when total\_resignations &gt; 0, otherwise “Green”, “datatype” → “Int”), mapping(“value” → interviews\_p ….

**Local steps**

- If not data.
  - Return no value.
- Set total\_resignations from len(data).
- Set interviews\_pending from len(list of entry.name for entry drawn from data where not entry.exit\_interview).
  - Draw entry from data, keep a combination only if (not entry.exit\_interview).
- Set fnf\_pending from len(list of entry.name for entry drawn from data where not entry.full\_and\_final\_statement).
  - Draw entry from data, keep a combination only if (not entry.full\_and\_final\_statement).
- Set questionnaires\_pending from len(list of entry.name for entry drawn from data where not entry.questionnaire).
  - Draw entry from data, keep a combination only if (not entry.questionnaire).
- Return list(mapping(“value” → total\_resignations, “label” → translated “Total Resignations”, “indicator” → “Red” when total\_resignations &gt; 0, otherwise “Green”, “datatype” → “Int”), mapping(“value” → interviews\_p ….
  - Value choice on total\_resignations &gt; 0 — true gives “Red”, false gives “Green”.
  - Value choice on interviews\_pending &gt; 0 — true gives “Blue”, false gives “Green”.
  - Value choice on fnf\_pending &gt; 0 — true gives “Blue”, false gives “Green”.
  - Value choice on questionnaires\_pending &gt; 0 — true gives “Blue”, false gives “Green”.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0082.json#L3885) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1688) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L294)

## Record · Employee grade

[Record definition](../../../../data/record-types/employee_grade.json)

<a id="op-b44d28c5f0c62f"></a>
### Get data

`operation_workforce_human_resources_record_definitions_employee_grade_employee_grade_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“transactions” → list(mapping(“items” → list(“Employee”)), mapping(“items” → list(“Employee Onboarding Template”, “Employee Separation Template”)))).

**Local steps**

- Return mapping(“transactions” → list(mapping(“items” → list(“Employee”)), mapping(“items” → list(“Employee Onboarding Template”, “Employee Separation Template”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0023.json#L4214) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L594) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L574)

## Record · Employee grievance

[Record definition](../../../../data/record-types/employee_grievance.json)

<a id="op-cbc214872da576"></a>
### Employee Grievance.on submit

`operation_workforce_human_resources_record_definitions_employee_grievance_business_behavior_employee_grievance_on_submit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Only Employee Grievance with status {0} or {1} can be submitted”.format(bold(translated “Invalid”), bold(translated “Resolved”)).

**Local steps**

- <a id="op-cbc214872da576-guard-2"></a>If self.status does not belong to list(“Invalid”, “Resolved”).
  - Call the validation error handler Platform.throw(translated “Only Employee Grievance with status {0} or {1} can be submitted”.format(bold(translated “Invalid”), bold(translated “Resolved”))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status does not belong to list(“Invalid”, “Resolved”), self.status = “Open” selects the branch that calls the validation-error handler with translated “Only Employee Grievance with status {0} or {1} can be submitted”.format(bold(translated “Invalid”), bold(translated “Resolved”)). With self.status = “Resolved”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-cbc214872da576-guard-2)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0023.json#L4327) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L596) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L576)

<a id="op-2ece6fcec3b980"></a>
### Employee Grievance.on discard

`operation_workforce_human_resources_record_definitions_employee_grievance_business_behavior_employee_grievance_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0023.json#L4506) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L595) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L575)

## Report · Employee hours utilization based on timesheet

<a id="op-3e1e37252de7bb"></a>
### Execute

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** EmployeeHoursReport(filters).run().

**Local steps**

- Return EmployeeHoursReport(filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0083.json#L1128) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1708) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L314)

<a id="op-2f62faa65e1075"></a>
### Employee Hours Report.initialize

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set self.from\_date from getdate(self.filters.from\_date).
- Set self.to\_date from getdate(self.filters.to\_date).
- Evaluate self.validate\_dates().
- Evaluate self.validate\_standard\_working\_hours().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dates](operations-009.md#op-3690a69f2091da), [validate standard working hours](operations-009.md#op-87d0151f0a48e1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0083.json#L1192) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1703) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L309)

<a id="op-3690a69f2091da"></a>
### Employee Hours Report.validate dates

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “From Date must come before To Date”.

**Local steps**

- Set self.day\_span from (self.to\_date − self.from\_date).days.
- If self.day\_span ≤ 0.
  - Call the validation error handler Platform.throw(translated “From Date must come before To Date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0083.json#L1394) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1706) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L312)

<a id="op-87d0151f0a48e1"></a>
### Employee Hours Report.validate standard working hours

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_validate_standard_working_hours`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set self.standard\_working\_hours from Platform.db.get\_single\_value(“HR Settings”, “standard\_working\_hours”).
- If not self.standard\_working\_hours.
  - Set msg from translated “The metrics for this report are calculated based on {0}. Please set {0} in {1}.”.format(Platform.bold(translated “Standard Working Hours”), Platform.utils.get\_link\_to\_form(“HR Settings”, “HR Settings”)).
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “standard\_working\_hours”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L75) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1707) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L313)

<a id="op-a2ed22ee9d150e"></a>
### Employee Hours Report.run

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_run`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data, no value, self.chart, …).

**Local steps**

- Evaluate self.generate\_columns().
- Evaluate self.generate\_data().
- Evaluate self.generate\_report\_summary().
- Evaluate self.generate\_chart\_data().
- Return tuple(self.columns, self.data, no value, self.chart, …).

**Methods declared on this owner** [generate columns](operations-009.md#op-ff4f2bc009ac32), [generate data](operations-009.md#op-866acad63d9878), [generate report summary](operations-010.md#op-845474132ab91b), [generate chart data](operations-010.md#op-d09d9c26568ead).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0083.json#L1789) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1704) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L310)

<a id="op-ff4f2bc009ac32"></a>
### Employee Hours Report.generate columns

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_generate_columns`

**Inputs** self.

**Local steps**

- Set self.columns from list(mapping(“label” → translated “Employee”, “options” → “Employee”, “fieldname” → “employee”, “fieldtype” → “Link”, …), mapping(“label” → translated “Department”, “options” → “Department”, “fieldname” →  ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0083.json#L1943) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1698) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L304)

<a id="op-866acad63d9878"></a>
### Employee Hours Report.generate data

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_generate_data`

**Inputs** self.

**Local steps**

- Evaluate self.generate\_filtered\_time\_logs().
- Evaluate self.generate\_stats\_by\_employee().
- Evaluate self.set\_employee\_department\_and\_name().
- If self.filters.department.
  - Evaluate self.filter\_stats\_by\_department().
- Evaluate self.calculate\_utilizations().
- Set self.data from list().
- For each tuple(emp, data) in self.stats\_by\_employee.items().
  - Set row from Platform.\_dict().
  - Set row at “employee” from emp.
  - Evaluate row.update(data).
  - Evaluate self.data.append(row).
- Evaluate self.data.sort(key = deferred anonymous expression, reverse = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [generate filtered time logs](operations-009.md#op-c7191048b14262), [generate stats by employee](operations-009.md#op-60075505a15e61), [set employee department and name](operations-010.md#op-5e30789403d073), [filter stats by department](operations-009.md#op-7083aefb8d57ec), [calculate utilizations](operations-010.md#op-9b520b294e23f2).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0083.json#L2716) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1699) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L305)

<a id="op-7083aefb8d57ec"></a>
### Employee Hours Report.filter stats by department

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_filter_stats_by_department`

**Inputs** self.

**Local steps**

- Set filtered\_data from Platform.\_dict().
- For each tuple(emp, data) in self.stats\_by\_employee.items().
  - If data at “department” equals self.filters.department.
    - Set filtered\_data at emp from data.
- Set self.stats\_by\_employee from filtered\_data.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0083.json#L3081) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1696) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L302)

<a id="op-c7191048b14262"></a>
### Employee Hours Report.generate filtered time logs

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_generate_filtered_time_logs`

**Inputs** self.

**Local steps**

- Set Timesheet from Platform.qb.DocType(“Timesheet”).
- Set TimesheetDetail from Platform.qb.DocType(“Timesheet Detail”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.docstatus equals 1).where(Timesheet.start\_date at slice self.from\_date to self.to\_date).where(Timesheet.e ….
- For each field in tuple(“employee”, “company”).
  - If self.filters.get(field).
    - Set query from query.where(Timesheet at field equals self.filters.get(field)).
- If self.filters.get(“project”).
  - Set query from query.where(TimesheetDetail.project equals self.filters.get(“project”)).
- Set self.filtered\_time\_logs from query.run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L74) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1700) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L306)

<a id="op-60075505a15e61"></a>
### Employee Hours Report.generate stats by employee

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_generate_stats_by_employee`

**Inputs** self.

**Local steps**

- Set self.stats\_by\_employee from Platform.\_dict().
- For each tuple(emp, hours, is\_billable, \_\_) in self.filtered\_time\_logs.
  - Evaluate self.stats\_by\_employee.setdefault(emp, Platform.\_dict()).setdefault(“billed\_hours”, 0.0).
  - Evaluate self.stats\_by\_employee at emp.setdefault(“non\_billed\_hours”, 0.0).
  - If is\_billable.
    - Update self.stats\_by\_employee at emp at “billed\_hours” using + flt(hours, 2).
  - Otherwise.
    - Update self.stats\_by\_employee at emp at “non\_billed\_hours” using + flt(hours, 2).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0083.json#L3957) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1702) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L308)
