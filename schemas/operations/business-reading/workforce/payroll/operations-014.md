# Payroll and benefits · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Salary slip

[Record definition](../../../../data/record-types/salary_slip.json)

<a id="op-1f3736ca34cfca"></a>
### Salary Slip.on cancel

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status().
- Evaluate self.update\_status().
- Evaluate self.update\_payment\_status\_for\_gratuity\_and\_leave\_encashment().
- Evaluate delete\_employee\_benefit\_ledger\_entry(“salary\_slip”, self.name).
- Evaluate cancel\_loan\_repayment\_entry(self).
- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-017.md#op-8f7c324ed09168), [update status](operations-017.md#op-36eafe6a75c344), [update payment status for gratuity and leave encashment](operations-013.md#op-d8536c9e4c68e9), [publish update](operations-014.md#op-1e188e80fae523).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L5529) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L709) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1056)

<a id="op-1e188e80fae523"></a>
### Salary Slip.publish update

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_publish_update`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**State and service calls** publish realtime.

**Local steps**

- Set employee\_user from Platform.db.get\_value(“Employee”, self.employee, “user\_id”, cache = true).
- Evaluate Platform.publish\_realtime(event = “Workforce:update\_salary\_slips”, message = mapping(“employee” → self.employee), user = employee\_user, after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(event = “Workforce:update\_salary\_slips”, message = mapping(“employee” → self.employee), user = employee\_user, after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L5697) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L717) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1064)

<a id="op-de61ac9b5a2f99"></a>
### Salary Slip.on trash

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_on_trash`

**Inputs** self.

**Local steps**

- Bind dependencies revert\_series\_if\_last.
- If not self.has\_custom\_naming\_series.
  - Evaluate revert\_series\_if\_last(self.default\_series, self.name).
- Evaluate delete\_employee\_benefit\_ledger\_entry(“salary\_slip”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L5869) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L712) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1059)

<a id="op-c997b531df6d34"></a>
### Salary Slip.get status

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_status`

**Inputs** self.

**Explicit results** “Cancelled” · “Withheld” · “Draft” · “Submitted”.

**Local steps**

- If self.docstatus equals 2.
  - Return “Cancelled”.
- Otherwise.
  - If self.salary\_withholding.
    - Return “Withheld”.
  - Otherwise.
    - If self.docstatus equals 0.
      - Return “Draft”.
    - Otherwise.
      - <a id="op-c997b531df6d34-guard-9"></a>If self.docstatus equals 1.
        - Return “Submitted”.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 1, self.docstatus = 1 (submitted) selects the branch that returns “Submitted”. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c997b531df6d34-guard-9)

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L5998) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L695) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1042)

<a id="op-f903fb01864c34"></a>
### Salary Slip.validate dates

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please set the Date Of Joining for employee {0}”.format(Platform.bold(self.employee\_name)) · validation helper — translated “Cannot create Salary Slip for Employee joining after Payroll Period” · validation helper — translated “Cannot create Salary Slip for Employee who has left before Payroll Period”.

**Local steps**

- Evaluate self.validate\_from\_to\_dates(“start\_date”, “end\_date”).
- If not self.joining\_date.
  - Call the validation error handler Platform.throw(translated “Please set the Date Of Joining for employee {0}”.format(Platform.bold(self.employee\_name))).
- If date\_diff(self.end\_date, self.joining\_date) &lt; 0.
  - Call the validation error handler Platform.throw(translated “Cannot create Salary Slip for Employee joining after Payroll Period”).
- If (self.relieving\_date and date\_diff(self.relieving\_date, self.start\_date) &lt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.relieving\_date → date\_diff(self.relieving\_date, self.start\_date) &lt; 0.
  - Call the validation error handler Platform.throw(translated “Cannot create Salary Slip for Employee who has left before Payroll Period”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L6151) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L734) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1081)

<a id="op-2346ceaeee2d22"></a>
### Salary Slip.is rounding total disabled

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_is_rounding_total_disabled`

**Inputs** self.

**Record and data access** read “Payroll Settings” via get\_single\_value.

**Explicit results** cint(Platform.db.get\_single\_value(“Payroll Settings”, “disable\_rounded\_total”)).

**Local steps**

- Return cint(Platform.db.get\_single\_value(“Payroll Settings”, “disable\_rounded\_total”)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Payroll Settings”, “disable\_rounded\_total”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L6498) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L707) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1054)

<a id="op-b1fbcb4b6d5294"></a>
### Salary Slip.check existing

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_check_existing`

**Inputs** self.

**Record and data access** read “Timesheet” via get\_value.

**Explicit failure paths** validation helper — translated “Salary Slip of employee {0} already created for this period”.format(self.employee) · validation helper — translated “Salary Slip of employee {0} already created for time sheet {1}”.format(self.employee, data.time\_sheet).

**Local steps**

- If not self.salary\_slip\_based\_on\_timesheet.
  - Set ss from Platform.qb.DocType(“Salary Slip”).
  - Set query from nested operand in the contract.qb.from\_(ss).select(ss.name).where(((((nested operand in the contract.start\_date equals nested operand in the contract.start\_date bitwise and nested operand in the contract.e ….
  - If self.payroll\_entry.
    - Set query from query.where(ss.payroll\_entry equals self.payroll\_entry).
  - Set ret\_exist from query.run().
  - If ret\_exist.
    - Call the validation error handler Platform.throw(translated “Salary Slip of employee {0} already created for this period”.format(self.employee)).
- Otherwise.
  - For each data in self.timesheets.
    - If Platform.db.get\_value(“Timesheet”, data.time\_sheet, “status”) equals “Payrolled”.
      - Call the validation error handler Platform.throw(translated “Salary Slip of employee {0} already created for time sheet {1}”.format(self.employee, data.time\_sheet)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L6585) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L647) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L994)

<a id="op-2218a2becf449f"></a>
### Salary Slip.get date details

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_date_details`

**Inputs** self.

**Local steps**

- If not self.end\_date.
  - Set date\_details from get\_start\_end\_dates(self.payroll\_frequency, (self.start\_date or self.posting\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.start\_date → self.posting\_date.
  - Set self.start\_date from date\_details.start\_date.
  - Set self.end\_date from date\_details.end\_date.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0124.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L672) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1019)

<a id="op-0e4be42cf0a378"></a>
### Salary Slip.get emp and working day details

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_employee_and_working_day_details`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Local steps**

- If self.employee.
  - Evaluate self.set(“earnings”, list()).
  - Evaluate self.set(“deductions”, list()).
  - Evaluate self.set(“employer\_contributions”, list()).
  - If hasattr(self, “loans”).
    - Evaluate self.set(“loans”, list()).
  - If self.payroll\_frequency.
    - Evaluate self.get\_date\_details().
  - Evaluate self.validate\_dates().
  - Evaluate self.get\_working\_days\_details().
  - Set struct from self.check\_sal\_struct().
  - If struct.
    - Bind dependencies make\_salary\_slip.
    - Set timesheet\_config from self.\_get\_ssa\_doc().get\_timesheet\_config().
    - Set self.salary\_slip\_based\_on\_timesheet from timesheet\_config.based\_on\_timesheet.
    - If self.salary\_slip\_based\_on\_timesheet.
      - Set self.\_timesheet\_component from timesheet\_config.timesheet\_component.
      - Evaluate self.set\_time\_sheet().
      - Evaluate self.add\_timesheet\_earning\_component(timesheet\_config).
    - Evaluate make\_salary\_slip(self.salary\_structure, self).
  - Evaluate process\_loan\_interest\_accrual\_and\_demand(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get date details](operations-014.md#op-2218a2becf449f), [validate dates](operations-014.md#op-f903fb01864c34), [get working days details](operations-014.md#op-263c6d91c048e3), [check sal struct](operations-014.md#op-5540c4ac534bee), [get ssa doc](operations-015.md#op-20bb18cb8a0757), [set time sheet](operations-014.md#op-eafc67c2a996ba), [add timesheet earning component](operations-014.md#op-791f86e708582d).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0124.json#L150) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L675) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1022)

<a id="op-eafc67c2a996ba"></a>
### Salary Slip.set time sheet

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_set_time_sheet`

**Inputs** self.

**Local steps**

- Evaluate self.set(“timesheets”, list()).
- Set Timesheet from Platform.qb.DocType(“Timesheet”).
- Set timesheets from nested operand in the contract(nested operand in the contract).select(Timesheet.star).where(((nested operand in the contract.employee equals nested operand in the contract.employee bitwise and nested opera ….
- For each data in timesheets.
  - Evaluate self.append(“timesheets”, mapping(“time\_sheet” → data.name, “working\_hours” → data.total\_hours)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0124.json#L666) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L727) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1074)

<a id="op-5540c4ac534bee"></a>
### Salary Slip.check sal struct

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_check_selling_struct`

**Inputs** self.

**State and service calls** msgprint with translated “No active or default Salary Structure found for employee {0} for the given dates”.format(self.employee).

**Explicit results** self.salary\_structure.

**Local steps**

- Set ss from Platform.qb.DocType(“Salary Structure”).
- Set ssa from Platform.qb.DocType(“Salary Structure Assignment”).
- Set query from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and (nested operand in the contract bitwise or nest ….
- If (not self.salary\_slip\_based\_on\_timesheet and self.payroll\_frequency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.salary\_slip\_based\_on\_timesheet → self.payroll\_frequency.
  - Set query from query.where(ss.payroll\_frequency equals self.payroll\_frequency).
- Set st\_name from query.run().
- If st\_name.
  - Set self.salary\_structure from st\_name at 0 at 0.
  - Return self.salary\_structure.
- Otherwise.
  - Set self.salary\_structure from no value.
  - Evaluate Platform.msgprint(translated “No active or default Salary Structure found for employee {0} for the given dates”.format(self.employee), title = translated “Salary Structure Missing”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0124.json#L1079) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L649) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L996)

<a id="op-791f86e708582d"></a>
### Salary Slip.add timesheet earning component

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_add_timesheet_earning_component`

**Inputs** self, timesheet\_config.

**Local steps**

- Set self.hour\_rate from flt(timesheet\_config.hour\_rate).
- Set self.base\_hour\_rate from (flt(self.hour\_rate) × flt(self.exchange\_rate)).
- Set self.total\_working\_hours from (sum(list of (d.working\_hours or 0.0) for d drawn from self.timesheets) or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sum(list of (d.working\_hours or 0.0) for d drawn from self.timesheets) → 0.0.
  - Draw d from self.timesheets.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.working\_hours → 0.0.
- Set wages\_amount from (self.hour\_rate × self.total\_working\_hours).
- Evaluate self.add\_earning\_for\_hourly\_wages(self, timesheet\_config.timesheet\_component, wages\_amount).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add earning for hourly wages](operations-014.md#op-6d5e66e9df6d67).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0124.json#L1792) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L636) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L983)

<a id="op-6d5e66e9df6d67"></a>
### Salary Slip.add earning for hourly wages

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_add_earning_for_hourly_wages`

**Inputs** self, doc, salary\_component, amount.

**Local steps**

- Set row\_exists from false.
- For each row in doc.earnings.
  - If row.salary\_component equals salary\_component.
    - Set row.amount from amount.
    - Set row\_exists from true.
    - Leave the innermost loop without its normal-exhaustion alternative.
- If not row\_exists.
  - Set wages\_row from get\_salary\_component\_data(salary\_component).
  - Set wages\_amount from (self.hour\_rate × self.total\_working\_hours).
  - Evaluate self.update\_component\_row(wages\_row, wages\_amount, “earnings”, default\_amount = wages\_amount).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update component row](operations-016.md#op-36d2d47c0e70e2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0124.json#L2060) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L630) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L977)

<a id="op-263c6d91c048e3"></a>
### Salary Slip.get working days details

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_working_days_details`

**Inputs** self, lwp = no value, for\_preview = 0, lwp\_days\_corrected = no value.

**Record and data access** read “Payroll Settings” via get\_cached\_value.

**State and service calls** msgprint with translated “Leave Without Pay does not match with approved {} records”.format(payroll\_settings.payroll\_based\_on).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “There are more holidays than working days this month.” · validation helper — translated “Please set Payroll based on in Payroll settings”.

**Local steps**

- Set payroll\_settings from Platform.get\_cached\_value(“Payroll Settings”, no value, tuple(“payroll\_based\_on”, “include\_holidays\_in\_total\_working\_days”, “consider\_marked\_attendance\_on\_holidays”, “daily\_wages\_fraction\_for\_half\_day”, …) ….
- Set consider\_marked\_attendance\_on\_holidays from (payroll\_settings.include\_holidays\_in\_total\_working\_days and payroll\_settings.consider\_marked\_attendance\_on\_holidays).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in payroll\_settings.include\_holidays\_in\_total\_working\_days → payroll\_settings.consider\_marked\_attendance\_on\_holidays.
- Set daily\_wages\_fraction\_for\_half\_day from (flt(payroll\_settings.daily\_wages\_fraction\_for\_half\_day) or 0.5).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(payroll\_settings.daily\_wages\_fraction\_for\_half\_day) → 0.5.
- Set working\_days from (date\_diff(self.end\_date, self.start\_date) + 1).
- If for\_preview.
  - Set self.total\_working\_days from working\_days.
  - Set self.payment\_days from working\_days.
  - Return no value.
- Set holidays from self.get\_holidays\_for\_employee(self.start\_date, self.end\_date).
- Set half\_day\_holidays from list() when cint(payroll\_settings.include\_holidays\_in\_total\_working\_days), otherwise self.get\_half\_day\_holidays\_for\_employee(self.start\_date, self.end\_date).
  - Value choice on cint(payroll\_settings.include\_holidays\_in\_total\_working\_days) — true gives list(), false gives self.get\_half\_day\_holidays\_for\_employee(self.start\_date, self.end\_date).
- Set full\_day\_holidays from list of date for date drawn from holidays where date does not belong to half\_day\_holidays.
  - Draw date from holidays, keep a combination only if (date does not belong to half\_day\_holidays).
- Set working\_days\_list from list of add\_days(getdate(self.start\_date), days = day) for day drawn from range(0, working\_days).
  - Draw day from range(0, working\_days).
- If not cint(payroll\_settings.include\_holidays\_in\_total\_working\_days).
  - Set working\_days\_list from list of i for i drawn from working\_days\_list where i does not belong to full\_day\_holidays.
    - Draw i from working\_days\_list, keep a combination only if (i does not belong to full\_day\_holidays).
  - Update working\_days using − (len(full\_day\_holidays) + (HALF\_DAY\_HOLIDAY\_FRACTION × len(half\_day\_holidays))).
  - <a id="op-263c6d91c048e3-guard-43"></a>If working\_days &lt; 0.
    - Call the validation error handler Platform.throw(translated “There are more holidays than working days this month.”).
- If not payroll\_settings.payroll\_based\_on.
  - Call the validation error handler Platform.throw(translated “Please set Payroll based on in Payroll settings”).
- If payroll\_settings.payroll\_based\_on equals “Attendance”.
  - Set tuple(actual\_lwp, absent) from self.calculate\_lwp\_ppl\_and\_absent\_days\_based\_on\_attendance(full\_day\_holidays, half\_day\_holidays, daily\_wages\_fraction\_for\_half\_day, consider\_marked\_attendance\_on\_holidays).
  - Set self.absent\_days from absent.
- Otherwise.
  - Set actual\_lwp from self.calculate\_lwp\_or\_ppl\_based\_on\_leave\_application(full\_day\_holidays, half\_day\_holidays, working\_days\_list, daily\_wages\_fraction\_for\_half\_day).
- If not lwp.
  - Set lwp from actual\_lwp.
- Otherwise.
  - If lwp differs from actual\_lwp.
    - Evaluate Platform.msgprint(translated “Leave Without Pay does not match with approved {} records”.format(payroll\_settings.payroll\_based\_on)).
- Set self.leave\_without\_pay from lwp.
- Set self.total\_working\_days from working\_days.
- Set payment\_days from self.get\_payment\_days(payroll\_settings.include\_holidays\_in\_total\_working\_days).
- If flt(payment\_days) &gt; flt(lwp).
  - Set self.payment\_days from (flt(payment\_days) − flt(lwp)).
  - If payroll\_settings.payroll\_based\_on equals “Attendance”.
    - Update self.payment\_days using − flt(absent).
  - Set consider\_unmarked\_attendance\_as from (payroll\_settings.consider\_unmarked\_attendance\_as or “Present”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in payroll\_settings.consider\_unmarked\_attendance\_as → “Present”.
  - If payroll\_settings.payroll\_based\_on equals “Attendance”.
    - If consider\_unmarked\_attendance\_as equals “Absent”.
      - Set unmarked\_days from self.get\_unmarked\_days(payroll\_settings.include\_holidays\_in\_total\_working\_days, full\_day\_holidays, half\_day\_holidays).
      - Update self.absent\_days using + unmarked\_days.
      - Update self.payment\_days using − unmarked\_days.
    - Set half\_absent\_days from self.get\_half\_absent\_days(consider\_marked\_attendance\_on\_holidays, full\_day\_holidays).
    - Update self.absent\_days using + (half\_absent\_days × daily\_wages\_fraction\_for\_half\_day).
    - Update self.payment\_days using − (half\_absent\_days × daily\_wages\_fraction\_for\_half\_day).
- Otherwise.
  - Set self.payment\_days from 0.
- If (lwp\_days\_corrected and lwp\_days\_corrected &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in lwp\_days\_corrected → lwp\_days\_corrected &gt; 0.
  - If verify\_lwp\_days\_corrected(self.employee, self.start\_date, self.end\_date, lwp\_days\_corrected).
    - Update self.payment\_days using + lwp\_days\_corrected.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison working\_days &lt; 0, working\_days = -1 selects the branch that calls the validation-error handler with translated “There are more holidays than working days this month.”. With working\_days = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-263c6d91c048e3-guard-43)

**Methods declared on this owner** [get holidays for employee](operations-014.md#op-cdf200863f5c94), [get half day holidays for employee](operations-014.md#op-874e761a69f50b), [calculate lwp ppl and absent days based on attendance](operations-015.md#op-3adeb8bf85f790), [calculate lwp or ppl based on leave application](operations-014.md#op-289b4899679275), [get payment days](operations-014.md#op-95e273c9e7b85c), [get unmarked days](operations-014.md#op-c1a809698f6e86), [get half absent days](operations-014.md#op-b0edccee52ce6d).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Payroll Settings”, no value, tuple(“payroll\_based\_on”, “include\_holidays\_in\_total\_working\_days”, “consider\_marked\_attendance\_on\_holidays”, “daily\_wages\_fraction\_for\_half\_day”, …) ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L117) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L702) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1049)

<a id="op-c1a809698f6e86"></a>
### Salary Slip.get unmarked days

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_unmarked_days`

**Inputs** self, include\_holidays\_in\_total\_working\_days, holidays = no value, half\_day\_holidays = no value.

**Declared result** float.

**Explicit results** unmarked\_days.

**Local steps**

- Set unmarked\_days from ((self.total\_working\_days − self.\_get\_days\_outside\_period(include\_holidays\_in\_total\_working\_days, holidays, half\_day\_holidays)) − self.\_get\_marked\_attendance\_days(holidays, half\_day\_holidays)).
- If (include\_holidays\_in\_total\_working\_days and holidays).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in include\_holidays\_in\_total\_working\_days → holidays.
  - Update unmarked\_days using − self.\_get\_number\_of\_holidays(holidays).
- Return unmarked\_days.

**Methods declared on this owner** [get days outside period](operations-014.md#op-6bc8c1db87dd33), [get marked attendance days](operations-014.md#op-436e40f9a3576e), [get number of holidays](operations-014.md#op-5253d38c07e835).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L116) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L701) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1048)

<a id="op-b0edccee52ce6d"></a>
### Salary Slip.get half absent days

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_half_absent_days`

**Inputs** self, consider\_marked\_attendance\_on\_holidays, holidays.

**Explicit results** query.run() at 0 at 0.

**Local steps**

- Set Attendance from Platform.qb.DocType(“Attendance”).
- Set query from nested operand in the contract.qb.from\_(Attendance).select(Count(“\*”)).where(((((nested operand in the contract.between(nested operand in the contract.actual\_start\_date, nested operand in the contract.actu ….
- If (not consider\_marked\_attendance\_on\_holidays and holidays).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not consider\_marked\_attendance\_on\_holidays → holidays.
  - Set query from query.where(Attendance.attendance\_date.notin(holidays)).
- Return query.run() at 0 at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0124.json#L4010) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L681) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1028)

<a id="op-6bc8c1db87dd33"></a>
### Salary Slip.get days outside period

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_days_outside_period`

**Inputs** self, include\_holidays\_in\_total\_working\_days, holidays = no value, half\_day\_holidays = no value.

**Explicit results** days.

**Local steps**

- Set half\_day\_holidays from (half\_day\_holidays or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in half\_day\_holidays → list().
- Bind local operation \_get\_days for subsequent calls.
- Set days from 0.
- If self.actual\_start\_date differs from self.start\_date.
  - Update days using + \_get\_days(self.start\_date, add\_days(self.joining\_date, negative 1)).
- If self.actual\_end\_date differs from self.end\_date.
  - Update days using + \_get\_days(add\_days(self.relieving\_date, 1), self.end\_date).
- Return days.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L110) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L673) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1020)

<a id="op-10c07b7d74aed5"></a>
### Salary Slip.get days outside period.get days

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_days_outside_period_get_days`

**Inputs** start\_date, end\_date.

**Explicit results** no\_of\_days · days.

**Local steps**

- Set no\_of\_days from (date\_diff(end\_date, start\_date) + 1).
- If include\_holidays\_in\_total\_working\_days.
  - Return no\_of\_days.
- Otherwise.
  - Set days from 0.
  - Set end\_date from getdate(end\_date).
  - For each day in range(no\_of\_days).
    - Set date from add\_days(end\_date, negative day).
    - If date belongs to half\_day\_holidays.
      - Update days using + HALF\_DAY\_HOLIDAY\_FRACTION.
    - Otherwise.
      - If date does not belong to holidays.
        - Update days using + 1.
  - Return days.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L111) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L674) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1021)

<a id="op-5253d38c07e835"></a>
### Salary Slip.get number of holidays

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_number_of_holidays`

**Inputs** self, holidays = no value.

**Declared result** float.

**Explicit results** no\_of\_holidays.

**Local steps**

- Set no\_of\_holidays from 0.
- Set actual\_end\_date from getdate(self.actual\_end\_date).
- For each days in range((date\_diff(self.actual\_end\_date, self.actual\_start\_date) + 1)).
  - Set date from add\_days(actual\_end\_date, negative days).
  - If date belongs to holidays.
    - Update no\_of\_holidays using + 1.
- Return no\_of\_holidays.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0124.json#L5130) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L690) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1037)

<a id="op-436e40f9a3576e"></a>
### Salary Slip.get marked attendance days

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_marked_attendance_days`

**Inputs** self, holidays = no value, half\_day\_holidays = no value.

**Declared result** float.

**Explicit results** marked\_days.

**Local steps**

- Set Attendance from Platform.qb.DocType(“Attendance”).
- Set query from nested operand in the contract.qb.from\_(Attendance).select(Count(“\*”)).where(((Attendance.attendance\_date.between(self.actual\_start\_date, self.actual\_end\_date) bitwise and Attendance.employee equals self.e ….
- If holidays.
  - Set query from query.where(Attendance.attendance\_date.notin(holidays)).
- Set marked\_days from query.run() at 0 at 0.
- If half\_day\_holidays.
  - Update marked\_days using − (HALF\_DAY\_HOLIDAY\_FRACTION × nested operand in the contract.where(nested operand in the contract(nested operand in the contract)).run() at 0 at 0).
- Return marked\_days.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L114) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L688) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1035)

<a id="op-95e273c9e7b85c"></a>
### Salary Slip.get payment days

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_payment_days`

**Inputs** self, include\_holidays\_in\_total\_working\_days.

**Record and data access** read “Employee” via get\_value.

**Explicit results** 0 · payment\_days.

**Explicit failure paths** validation helper — translated “Employee {0} relieved on {1} must be set as 'Left'”.format(get\_link\_to\_form(“Employee”, self.employee), formatdate(self.relieving\_date)).

**Local steps**

- If (self.joining\_date and self.joining\_date &gt; getdate(self.end\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.joining\_date → self.joining\_date &gt; getdate(self.end\_date).
  - Return 0.
- If self.relieving\_date.
  - Set employee\_status from Platform.db.get\_value(“Employee”, self.employee, “status”).
  - If (self.relieving\_date &lt; getdate(self.start\_date) and employee\_status differs from “Left”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.relieving\_date &lt; getdate(self.start\_date) → employee\_status differs from “Left”.
    - Call the validation error handler Platform.throw(translated “Employee {0} relieved on {1} must be set as 'Left'”.format(get\_link\_to\_form(“Employee”, self.employee), formatdate(self.relieving\_date))).
- Set payment\_days from (date\_diff(self.actual\_end\_date, self.actual\_start\_date) + 1).
- If not cint(include\_holidays\_in\_total\_working\_days).
  - Set holidays from self.get\_holidays\_for\_employee(self.actual\_start\_date, self.actual\_end\_date).
  - Set half\_day\_holidays from self.get\_half\_day\_holidays\_for\_employee(self.actual\_start\_date, self.actual\_end\_date).
  - Update payment\_days using − (len(holidays) − (HALF\_DAY\_HOLIDAY\_FRACTION × len(half\_day\_holidays))).
- Return payment\_days.

**Methods declared on this owner** [get holidays for employee](operations-014.md#op-cdf200863f5c94), [get half day holidays for employee](operations-014.md#op-874e761a69f50b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L115) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L692) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1039)

<a id="op-cdf200863f5c94"></a>
### Salary Slip.get holidays for employee

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_holidays_for_employee`

**Inputs** self, start\_date, end\_date.

**Explicit results** list of holiday\_date for holidays drawn from holidays\_by\_range.values(), then holiday\_date drawn from holidays.

**Local steps**

- Set holidays\_by\_range from mapping().
- Set uncached\_ranges from mapping().
- For each holiday\_list\_range in get\_holiday\_list\_ranges\_for\_employee(self.employee, start\_date, end\_date).
  - Set key from “{holiday\_list}:{from\_date}:{to\_date}”.format(expanded names holiday\_list\_range).
  - Set holidays\_by\_range at key from Platform.cache().hget(HOLIDAYS\_BETWEEN\_DATES, key).
  - If not holidays\_by\_range at key.
    - Set uncached\_ranges at key from list(holiday\_list\_range).
- If uncached\_ranges.
  - Set fetched from get\_holidays\_in\_ranges\_map(uncached\_ranges).
  - For each key in uncached\_ranges.
    - Set holidays\_by\_range at key from list of holiday.holiday\_date for holiday drawn from fetched.get(key, list()).
      - Draw holiday from fetched.get(key, list()).
    - Evaluate Platform.cache().hset(HOLIDAYS\_BETWEEN\_DATES, key, holidays\_by\_range at key).
- Return list of holiday\_date for holidays drawn from holidays\_by\_range.values(), then holiday\_date drawn from holidays.
  - Draw holidays from holidays\_by\_range.values().
  - Draw holiday\_date from holidays.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L112) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L682) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1029)

<a id="op-874e761a69f50b"></a>
### Salary Slip.get half day holidays for employee

`operation_workforce_binding_workforce_payroll_doctype_salary_slip_salary_slip_salaryslip_get_half_day_holidays_for_employee`

**Inputs** self, start\_date, end\_date.

**Explicit results** half\_day\_holidays.

**Local steps**

- Set half\_day\_holidays from list().
- For each holiday\_list\_range in get\_holiday\_list\_ranges\_for\_employee(self.employee, start\_date, end\_date).
  - Set key from “half\_day:{holiday\_list}:{from\_date}:{to\_date}”.format(expanded names holiday\_list\_range).
  - Set holiday\_dates from Platform.cache().hget(HOLIDAYS\_BETWEEN\_DATES, key).
  - If holiday\_dates is identical to no value.
    - Set holiday\_dates from get\_holiday\_dates\_between(holiday\_list\_range.holiday\_list, holiday\_list\_range.from\_date, holiday\_list\_range.to\_date, only\_half\_days = true).
    - Evaluate Platform.cache().hset(HOLIDAYS\_BETWEEN\_DATES, key, holiday\_dates).
  - Evaluate half\_day\_holidays.extend(holiday\_dates).
- Return half\_day\_holidays.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L178) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L229) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L229)

<a id="op-289b4899679275"></a>
### Salary Slip.calculate lwp or ppl based on leave application

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_calculate_leave_without_pay_or_partially_paid_leave_based_on_leave_application`

**Inputs** self, holidays, half\_day\_holidays, working\_days\_list, daily\_wages\_fraction\_for\_half\_day.

**Explicit results** lwp.

**Local steps**

- Set lwp from 0.
- Set leaves from get\_lwp\_or\_ppl\_for\_date\_range(self.employee, self.start\_date, self.end\_date).
- For each d in working\_days\_list.
  - If (self.relieving\_date and d &gt; self.relieving\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.relieving\_date → d &gt; self.relieving\_date.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set leave from leaves.get(d).
  - If not leave.
    - Continue with the next iteration or loop test.
  - If (not leave.include\_holiday and getdate(d) belongs to holidays).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not leave.include\_holiday → getdate(d) belongs to holidays.
    - Continue with the next iteration or loop test.
  - Set equivalent\_lwp\_count from 0.
  - Set fraction\_of\_daily\_salary\_per\_leave from flt(leave.fraction\_of\_daily\_salary\_per\_leave).
  - Set is\_half\_day\_leave from false.
  - If (cint(leave.half\_day) and (leave.half\_day\_date equals d or leave.from\_date equals leave.to\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(leave.half\_day) → (leave.half\_day\_date equals d or leave.from\_date equals leave.to\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in leave.half\_day\_date equals d → leave.from\_date equals leave.to\_date.
    - Set is\_half\_day\_leave from true.
  - Set equivalent\_lwp\_count from (1 − daily\_wages\_fraction\_for\_half\_day) when is\_half\_day\_leave, otherwise 1.
    - Value choice on is\_half\_day\_leave — true gives (1 − daily\_wages\_fraction\_for\_half\_day), false gives 1.
  - If cint(leave.is\_ppl).
    - Update equivalent\_lwp\_count using × (1 − fraction\_of\_daily\_salary\_per\_leave) when fraction\_of\_daily\_salary\_per\_leave, otherwise 1.
      - Value choice on fraction\_of\_daily\_salary\_per\_leave — true gives (1 − fraction\_of\_daily\_salary\_per\_leave), false gives 1.
  - If (not leave.include\_holiday and getdate(d) belongs to half\_day\_holidays).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not leave.include\_holiday → getdate(d) belongs to half\_day\_holidays.
    - Update equivalent\_lwp\_count using × HALF\_DAY\_HOLIDAY\_FRACTION.
  - Update lwp using + equivalent\_lwp\_count.
- Return lwp.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L104) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L640) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L987)
