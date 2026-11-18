# Employment and attendance · operations 35

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Overtime slip

[Record definition](../../../../data/record-types/overtime_slip.json)

<a id="op-83b092d099411d"></a>
### Overtime Slip.make salary slip

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_make_salary_slip`

**Inputs** self, salary\_structure.

**Explicit results** make\_salary\_slip(salary\_structure, employee = self.employee, posting\_date = self.start\_date).

**Local steps**

- Bind dependencies make\_salary\_slip.
- Return make\_salary\_slip(salary\_structure, employee = self.employee, posting\_date = self.start\_date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L6559) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1401) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L15)

<a id="op-0cd50118ac589b"></a>
### Overtime Slip.calculate overtime amount

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_calculate_overtime_amount`

**Inputs** self, overtime\_type, applicable\_hourly\_rate, overtime\_duration, overtime\_date, holiday\_date\_map.

**Explicit results** 0.0 · amount.

**Local steps**

- Set overtime\_details from self.overtime\_types.get(overtime\_type).
- If not overtime\_details.
  - Return 0.0.
- <a id="op-0cd50118ac589b-guard-11"></a>If applicable\_hourly\_rate ≤ 0.
  - Return 0.0.
- Set overtime\_date\_str from cstr(overtime\_date).
- Set multiplier from overtime\_details.get(“standard\_multiplier”, 1).
- Set holiday\_info from holiday\_date\_map.get(overtime\_date\_str).
- If holiday\_info.
  - If (overtime\_details.get(“applicable\_for\_weekend”) and holiday\_info.weekly\_off).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in overtime\_details.get(“applicable\_for\_weekend”) → holiday\_info.weekly\_off.
    - Set multiplier from overtime\_details.get(“weekend\_multiplier”, multiplier).
  - Otherwise.
    - If (overtime\_details.get(“applicable\_for\_public\_holiday”) and not holiday\_info.weekly\_off).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in overtime\_details.get(“applicable\_for\_public\_holiday”) → not holiday\_info.weekly\_off.
      - Set multiplier from overtime\_details.get(“public\_holiday\_multiplier”, multiplier).
- Set amount from ((overtime\_duration × applicable\_hourly\_rate) × multiplier).
- Return amount.

**Derived branch illustrations**

- At the comparison applicable\_hourly\_rate ≤ 0, applicable\_hourly\_rate = 0 selects the branch that returns 0.0. With applicable\_hourly\_rate = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-0cd50118ac589b-guard-11)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0064.json#L6653) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1391) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L5)

<a id="op-9a2b33a4dfe890"></a>
### Overtime Slip.get holiday map

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_get_holiday_map`

**Inputs** self.

**Explicit results** holiday\_date\_map.

**Local steps**

- Bind dependencies get\_holiday\_dates\_between\_range.
- Set holiday\_dates from get\_holiday\_dates\_between\_range(self.employee, self.start\_date, self.end\_date, select\_weekly\_offs = true, as\_dict = true).
- Set holiday\_date\_map from mapping().
- For each holiday\_date in holiday\_dates.
  - Set holiday\_date\_map at cstr(holiday\_date.holiday\_date) from holiday\_date.
- Return holiday\_date\_map.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L62) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1398) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L12)

<a id="op-08f84df260d8ae"></a>
### Overtime Slip.get overtime type details

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_overtime_slip_get_overtime_type_details`

**Inputs** self, name.

**Record and data access** read “Overtime Type” via get\_value · read “Overtime Salary Component” via get\_all.

**Explicit results** details.

**Local steps**

- Set details from Platform.get\_value(“Overtime Type”, filters = mapping(“name” → name), fieldname = list(“name”, “standard\_multiplier”, “weekend\_multiplier”, “public\_holiday\_multiplier”, …), as\_dict = true).
- Set components from list().
- If details.overtime\_calculation\_method equals “Salary Component Based”.
  - Set components from Platform.get\_all(“Overtime Salary Component”, filters = mapping(“parent” → name), fields = list(“salary\_component”)).
  - Set components from list of data.salary\_component for data drawn from components.
    - Draw data from components.
- Set details at “components” from components.
- Return details.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0065.json#L220) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1400) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L14)

<a id="op-4bef27f5288b8e"></a>
### Filter employees for overtime slip creation

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_filter_employees_for_overtime_slip_creation`

**Inputs** start\_date, end\_date, employees, limit = no value.

**Explicit results** list() · eligible\_employees.

**Local steps**

- If not employees.
  - Return list().
- If not isinstance(employees, list).
  - Set employees from json.loads(employees).
- Set OvertimeSlip from Platform.qb.DocType(“Overtime Slip”).
- Set Attendance from Platform.qb.DocType(“Attendance”).
- Set employees\_with\_overtime\_attendance from nested operand in the contract(nested operand in the contract).distinct().where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equ ….
- If not employees\_with\_overtime\_attendance.
  - Return list().
- Set employees\_with\_existing\_overtime\_slips from nested operand in the contract(nested operand in the contract).distinct().where((((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contract differs from nes ….
- Set eligible\_employees from list((set(employees\_with\_overtime\_attendance) − set(employees\_with\_existing\_overtime\_slips))).
- Return eligible\_employees.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0065.json#L604) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1388) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L2)

<a id="op-db220cd86cd1c3"></a>
### Create overtime slips for employees

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_create_overtime_slips_for_employees`

**Inputs** employees, args.

**Record and data access** read “Employee” via get\_value · resolve a document from emp\_args via get\_doc · resolve a document from “Payroll Entry” via get\_doc.

**State and service calls** msgprint with translated “Overtime Slip created for {0} employee(s)”.format(count) · msgprint · call db\_set on Platform.get\_doc(“Payroll Entry”, args.get(“payroll\_entry”)) · publish realtime with “completed\_overtime\_slip\_creation”.

**Local steps**

- Set count from 0.
- Set errors from list().
- For each emp in employees.
  - Set emp\_args from args.copy().
  - Set relieving\_date from Platform.db.get\_value(“Employee”, emp, “relieving\_date”).
  - Set relieving\_date from getdate(relieving\_date) when relieving\_date, otherwise no value.
    - Value choice on relieving\_date — true gives getdate(relieving\_date), false gives no value.
  - If (relieving\_date and relieving\_date &lt; getdate(emp\_args.get(“end\_date”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in relieving\_date → relieving\_date &lt; getdate(emp\_args.get(“end\_date”)).
    - Set emp\_args at “start\_date” from getdate(emp\_args.get(“start\_date”)).
    - Set emp\_args at “end\_date” from relieving\_date.
  - Evaluate emp\_args.update(mapping(“doctype” → “Overtime Slip”, “employee” → emp)).
  - Attempt the following.
    - Evaluate Platform.get\_doc(emp\_args).get\_emp\_and\_overtime\_details().
    - Update count using + 1.
  - On failure (Exception) bound to e.
    - Evaluate Platform.clear\_last\_message().
    - Evaluate errors.append(translated “Employee {0} : {1}”.format(emp, str(e))).
    - Evaluate Platform.log\_error(Platform.get\_traceback(), translated “Overtime Slip Creation Error for {0}”.format(emp)).
- If count.
  - Evaluate Platform.msgprint(translated “Overtime Slip created for {0} employee(s)”.format(count), indicator = “green”, title = translated “Overtime Slips Created”).
- If errors.
  - Set error\_list\_html from empty text.join(generator of formatted text &lt;li&gt;{err}&lt;/li&gt; for err drawn from errors).
    - Draw err from errors.
  - Evaluate Platform.msgprint(title = translated “Overtime Slip Creation Failed”, msg = formatted text &lt;ul&gt;{error\_list\_html}&lt;/ul&gt;, indicator = “red”).
- Set status from “Failed” when errors, otherwise “Draft”.
  - Value choice on errors — true gives “Failed”, false gives “Draft”.
- Evaluate Platform.get\_doc(“Payroll Entry”, args.get(“payroll\_entry”)).db\_set(mapping(“status” → status)).
- Evaluate Platform.publish\_realtime(“completed\_overtime\_slip\_creation”, user = Platform.session.user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“completed\_overtime\_slip\_creation”, user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0065.json#L1350) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1387) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1363)

<a id="op-61bf124e6c1f46"></a>
### Submit overtime slips for employees

`operation_workforce_human_resources_record_definitions_overtime_slip_business_behavior_submit_overtime_slips_for_employees`

**Inputs** overtime\_slips, payroll\_entry.

**Record and data access** resolve a document from “Overtime Slip” via get\_doc · resolve a document from “Payroll Entry” via get\_doc.

**State and service calls** call submit on doc · msgprint with translated “Overtime Slips submitted for {0} employee(s)”.format(count) · msgprint · call db\_set on Platform.get\_doc(“Payroll Entry”, payroll\_entry) · publish realtime with “completed\_overtime\_slip\_submission”.

**Local steps**

- Set count from 0.
- Set errors from list().
- For each overtime\_slip in overtime\_slips.
  - Attempt the following.
    - Set doc from Platform.get\_doc(“Overtime Slip”, overtime\_slip).
    - Set doc.submitted\_via\_payroll\_entry from 1.
    - Evaluate doc.submit().
    - Update count using + 1.
  - On failure (Exception) bound to e.
    - Evaluate Platform.clear\_last\_message().
    - Evaluate errors.append(translated “{0} : {1}”.format(overtime\_slip, str(e))).
    - Evaluate Platform.log\_error(Platform.get\_traceback(), translated “Overtime Slip Submission Error for {0}”.format(overtime\_slip)).
- If count.
  - Evaluate Platform.msgprint(translated “Overtime Slips submitted for {0} employee(s)”.format(count), indicator = “green”, title = translated “Overtime Slip Submitted”).
- If errors.
  - Set error\_list\_html from empty text.join(generator of formatted text &lt;li&gt;{err}&lt;/li&gt; for err drawn from errors).
    - Draw err from errors.
  - Evaluate Platform.msgprint(title = translated “Overtime Slip Submission Failed”, msg = formatted text &lt;ul&gt;{error\_list\_html}&lt;/ul&gt;, indicator = “red”).
- Set status from “Failed” when errors, otherwise “Draft”.
  - Value choice on errors — true gives “Failed”, false gives “Draft”.
- Set payroll\_entry from Platform.get\_doc(“Payroll Entry”, payroll\_entry).db\_set(mapping(“status” → status)).
- Evaluate Platform.publish\_realtime(“completed\_overtime\_slip\_submission”, user = Platform.session.user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“completed\_overtime\_slip\_submission”, user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L63) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1407) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L21)

## Record · Overtime type

[Record definition](../../../../data/record-types/overtime_type.json)

<a id="op-a17f349f26a6c5"></a>
### Overtime Type.validate

`operation_workforce_human_resources_record_definitions_overtime_type_business_behavior_overtime_type_validate`

**Inputs** self.

**Local steps**

- If self.overtime\_calculation\_method equals “Salary Component Based”.
  - Evaluate self.validate\_applicable\_components().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate applicable components](operations-035.md#op-af0ec5afa4fc10).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L933) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1415) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L29)

<a id="op-af0ec5afa4fc10"></a>
### Overtime Type.validate applicable components

`operation_workforce_human_resources_record_definitions_overtime_type_business_behavior_overtime_type_validate_applicable_components`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Select Applicable Components for Overtime Type”.

**Local steps**

- If not len(self.applicable\_salary\_component).
  - Call the validation error handler Platform.throw(translated “Select Applicable Components for Overtime Type”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L1010) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1416) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L30)

## Report · Project profitability

<a id="op-d285e462c7e4a8"></a>
### Execute

`operation_workforce_human_resources_report_project_profitability_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, charts).

**Local steps**

- Set data from get\_data(filters).
- Set columns from get\_columns().
- Set charts from get\_chart\_data(data).
- Return tuple(columns, data, no value, charts).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0091.json#L5976) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L72) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L421)

<a id="op-9ded317ae407d8"></a>
### Get data

`operation_workforce_human_resources_report_project_profitability_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set data from get\_rows(filters).
- Set data from calculate\_cost\_and\_profit(data).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0091.json#L6109) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L75) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L424)

<a id="op-f81e14cda24265"></a>
### Get rows

`operation_workforce_human_resources_report_project_profitability_business_behavior_get_rows`

**Inputs** filters.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set Timesheet from Platform.qb.DocType(“Timesheet”).
- Set SalarySlip from Platform.qb.DocType(“Salary Slip”).
- Set SalesInvoice from Platform.qb.DocType(“Sales Invoice”).
- Set SalesInvoiceTimesheet from Platform.qb.DocType(“Sales Invoice Timesheet”).
- Set SalarySlipTimesheet from Platform.qb.DocType(“Salary Slip Timesheet”).
- Set query from nested operand in the contract(nested operand in the contract).select(SalesInvoice.customer\_name, SalesInvoice.base\_grand\_total, nested operand in the contract.as\_(“voucher\_no”), Timesheet.employee, …).dis ….
- If filters.get(“company”).
  - Set query from query.where(Timesheet.company equals filters.get(“company”)).
- If filters.get(“start\_date”).
  - Set query from query.where(Timesheet.start\_date ≥ filters.get(“start\_date”)).
- If filters.get(“end\_date”).
  - Set query from query.where(Timesheet.end\_date ≤ filters.get(“end\_date”)).
- If filters.get(“customer”).
  - Set query from query.where(SalesInvoice.customer equals filters.get(“customer”)).
- If filters.get(“employee”).
  - Set query from query.where(Timesheet.employee equals filters.get(“employee”)).
- If filters.get(“project”).
  - Set query from query.where(Timesheet.parent\_project equals filters.get(“project”)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L82) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L76) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L425)

<a id="op-7dc1fcdb864f2b"></a>
### Calculate cost and profit

`operation_workforce_human_resources_report_project_profitability_business_behavior_calculate_cost_and_profit`

**Inputs** data.

**Explicit results** data.

**Explicit failure paths** validation helper.

**Local steps**

- Set standard\_working\_hours from get\_standard\_working\_hours().
- Set precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- For each row in data.
  - If flt(row.total\_working\_days) ≤ 0.
    - Call the validation error handler Platform.throw(title = translated “Error in calculating project profitability”, msg = translated “Total Working Days must be greater than zero. Please review Salary Slip {0}.”.format(Platform.utils.get\_lin ….
  - Set row.utilization from flt((flt(row.total\_billed\_hours) ÷ (flt(row.total\_working\_days) × flt(standard\_working\_hours))), precision).
  - Set row.fractional\_cost from flt((flt(row.base\_gross\_pay) × flt(row.utilization)), precision).
  - Set row.profit from flt((flt(row.base\_grand\_total) − (flt(row.base\_gross\_pay) × flt(row.utilization))), precision).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L81) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L71) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L420)

<a id="op-451b23a84aa85f"></a>
### Get standard working hours

`operation_workforce_human_resources_report_project_profitability_business_behavior_get_standard_working_hours`

**Inputs** no declared parameters.

**Declared result** (float bitwise or no value).

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** standard\_working\_hours.

**Explicit failure paths** validation helper — translated “The metrics for this report are calculated based on the {0}. Please set {0} in {1}.”.format(Platform.bold(translated “Standard Working Hours”), Platform.utils.get\_link\_to\_form(“HR Settings”, “H ….

**Local steps**

- Set standard\_working\_hours from Platform.db.get\_single\_value(“HR Settings”, “standard\_working\_hours”).
- If not standard\_working\_hours.
  - Call the validation error handler Platform.throw(translated “The metrics for this report are calculated based on the {0}. Please set {0} in {1}.”.format(Platform.bold(translated “Standard Working Hours”), Platform.utils.get\_link\_to\_form(“H ….
- Return standard\_working\_hours.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “standard\_working\_hours”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L83) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L77) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L426)

<a id="op-0116d834286024"></a>
### Get chart data

`operation_workforce_human_resources_report_project_profitability_business_behavior_get_chart_data`

**Inputs** data.

**Explicit results** no value · charts.

**Local steps**

- If not data.
  - Return no value.
- Set labels from list().
- Set utilization from list().
- For each entry in data.
  - Evaluate labels.append(formatted text {entry.get(“employee\_name”)} - {entry.get(“end\_date”)}).
  - Evaluate utilization.append(entry.get(“utilization”)).
- Set charts from mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → “Utilization”, “values” → utilization))), “type” → “bar”, “colors” → list(“#84BDD5”)).
- Return charts.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0092.json#L647) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L73) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L422)

<a id="op-5bb9604faac922"></a>
### Get columns

`operation_workforce_human_resources_report_project_profitability_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “customer\_name”, “label” → translated “Customer”, “fieldtype” → “Link”, “options” → “Customer”, …), mapping(“fieldname” → “employee”, “label” → translated “Employee”, “fieldtype” ….

**Local steps**

- Return list(mapping(“fieldname” → “customer\_name”, “label” → translated “Customer”, “fieldtype” → “Link”, “options” → “Customer”, …), mapping(“fieldname” → “employee”, “label” → translated “Employee”, “fieldtype” ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0092.json#L998) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L74) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L423)

## Record · Pwa notification

<a id="op-e0d75209658bb5"></a>
### PWANotification.on update

`operation_workforce_human_resources_record_definitions_pwa_notification_business_behavior_progressive_web_application_notification_on_update`

**Inputs** self.

**Local steps**

- Evaluate Workforce.refetch\_resource(“Workforce:notifications”, self.to\_user).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L1631) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1420) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L34)

<a id="op-3b73135da2b7cb"></a>
### PWANotification.after insert

`operation_workforce_human_resources_record_definitions_pwa_notification_business_behavior_progressive_web_application_notification_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.send\_push\_notification().

If control reaches the end, it returns no value.

**Methods declared on this owner** [send push notification](operations-035.md#op-72168c69474a68).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L1695) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1418) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L32)

<a id="op-72168c69474a68"></a>
### PWANotification.send push notification

`operation_workforce_human_resources_record_definitions_pwa_notification_business_behavior_progressive_web_application_notification_send_push_notification`

**Inputs** self.

**Local steps**

- Attempt the following.
  - Bind dependencies PushNotification.
  - Set push\_notification from PushNotification(“Workforce”).
  - If push\_notification.is\_enabled().
    - Evaluate push\_notification.send\_notification\_to\_user(self.to\_user, self.reference\_document\_type, self.message, link = self.get\_notification\_link(), icon = formatted text {Platform.utils.get\_url()}/assets/Workforce/ ….
- On failure (ImportError).
  - Take no action here.
- On failure (Exception).
  - Evaluate self.log\_error(formatted text Error sending push notification: {self.name}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get notification link](operations-035.md#op-72f04afe9133f1).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L1746) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1421) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L35)

<a id="op-72f04afe9133f1"></a>
### PWANotification.get notification link

`operation_workforce_human_resources_record_definitions_pwa_notification_business_behavior_progressive_web_application_notification_get_notification_link`

**Inputs** self.

**Explicit results** formatted text {base\_url}/leave-applications/{self.reference\_document\_name} · formatted text {base\_url}/expense-claims/{self.reference\_document\_name} · base\_url.

**Local steps**

- Set base\_url from formatted text {Platform.utils.get\_url()}/Workforce.
- If self.reference\_document\_type equals “Leave Application”.
  - Return formatted text {base\_url}/leave-applications/{self.reference\_document\_name}.
- Otherwise.
  - If self.reference\_document\_type equals “Expense Claim”.
    - Return formatted text {base\_url}/expense-claims/{self.reference\_document\_name}.
- Return base\_url.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0066.json#L2020) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1419) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L33)

## Report · Recruitment analytics

<a id="op-7972d8278126e3"></a>
### Execute

`operation_workforce_human_resources_report_recruitment_analytics_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set filters from Platform.\_dict(filters).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0092.json#L3987) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L81) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L430)

<a id="op-ff567a0e5e305b"></a>
### Get columns

`operation_workforce_human_resources_report_recruitment_analytics_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Staffing Plan”, “fieldtype” → “Link”, “fieldname” → “staffing\_plan”, “options” → “Staffing Plan”, …), mapping(“label” → translated “Job Opening”, “fieldtype” → “Link”, “f ….

**Local steps**

- Return list(mapping(“label” → translated “Staffing Plan”, “fieldtype” → “Link”, “fieldname” → “staffing\_plan”, “options” → “Staffing Plan”, …), mapping(“label” → translated “Job Opening”, “fieldtype” → “Link”, “f ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0092.json#L4143) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L83) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L432)

<a id="op-38632b7ef3d651"></a>
### Get data

`operation_workforce_human_resources_report_recruitment_analytics_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set staffing\_plan\_details from get\_staffing\_plan(filters).
- Set staffing\_plan\_list from list(set(list of details at “name” for details drawn from staffing\_plan\_details)).
  - Draw details from staffing\_plan\_details.
- Set tuple(sp\_jo\_map, jo\_list) from get\_job\_opening(staffing\_plan\_list, filters).
- Set tuple(jo\_ja\_map, ja\_list) from get\_job\_applicant(jo\_list).
- Set ja\_joff\_map from get\_job\_offer(ja\_list, filters).
- For each sp in sp\_jo\_map.keys().
  - Set parent\_row from get\_parent\_row(sp\_jo\_map, sp, jo\_ja\_map, ja\_joff\_map).
  - Update data using + parent\_row.
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0092.json#L5062) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L84) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L433)

<a id="op-6d3d39d1bb7c29"></a>
### Get parent row

`operation_workforce_human_resources_report_recruitment_analytics_business_behavior_get_parent_row`

**Inputs** sp\_jo\_map, sp, jo\_ja\_map, ja\_joff\_map.

**Explicit results** data.

**Local steps**

- Set data from list().
- If sp belongs to sp\_jo\_map.keys().
  - For each jo in sp\_jo\_map at sp.
    - Set row from mapping(“staffing\_plan” → sp, “job\_opening” → jo at “name”).
    - Evaluate data.append(row).
    - Set child\_row from get\_child\_row(jo at “name”, jo\_ja\_map, ja\_joff\_map).
    - Update data using + child\_row.
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0092.json#L5392) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L88) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L437)
