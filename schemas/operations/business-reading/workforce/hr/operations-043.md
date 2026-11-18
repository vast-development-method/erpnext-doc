# Employment and attendance · operations 43

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-7c2de245597aab"></a>
### Log allocation error

`operation_workforce_human_resources_utils_business_behavior_log_allocation_error`

**Inputs** allocation\_name, error.

**Local steps**

- Set error\_log from Platform.log\_error(error, reference\_doctype = “Leave Allocation”).
- Set text from translated “{0}. Check error log for more details.”.format(error\_log.method).
- Set earned\_leave\_schedule from qb.DocType(“Earned Leave Schedule”).
- Set today from (getdate(Platform.flags.current\_date) or getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate(Platform.flags.current\_date) → getdate().
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(earned\_leave\_schedule.failed, 1).set(earned\_leave\_schedule.failure\_reason, text).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L6155) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L159) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L508)

<a id="op-aea82a48534718"></a>
### Send email for failed allocations

`operation_workforce_human_resources_utils_business_behavior_send_email_for_failed_allocations`

**Inputs** failed\_allocations.

**State and service calls** sendmail.

**Local steps**

- Set allocations from comma\_and(list of get\_link\_to\_form(“Leave Allocation”, x) for x drawn from failed\_allocations).
  - Draw x from failed\_allocations.
- Set User from Platform.qb.DocType(“User”).
- Set HasRole from Platform.qb.DocType(“Has Role”).
- Set query from nested operand in the contract(nested operand in the contract).select(HasRole.parent).distinct().where(((HasRole.parenttype equals “User” bitwise and User.enabled equals 1) bitwise and HasRole.role equals  ….
- Set hr\_managers from query.run(pluck = true).
- Evaluate Platform.sendmail(recipients = hr\_managers, subject = translated “Failure of Automatic Allocation of Earned Leaves”, message = translated “Automatic Leave Allocation has failed for the following Earned Lea ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = hr\_managers, subject = translated “Failure of Automatic Allocation of Earned Leaves”, message = translated “Automatic Leave Allocation has failed for the following Earned Lea ….

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L6534) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L162) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L511)

<a id="op-06aeeac1c8d69e"></a>
### Get monthly earned leave

`operation_workforce_human_resources_utils_business_behavior_get_monthly_earned_leave`

**Inputs** date\_of\_joining, annual\_leaves, frequency, rounding, period\_start\_date = no value, period\_end\_date = no value, pro\_rated = true.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** earned\_leaves.

**Local steps**

- Set earned\_leaves from 0.0.
- Set divide\_by\_frequency from mapping(“Yearly” → 1, “Half-Yearly” → 2, “Quarterly” → 4, “Monthly” → 12).
- If annual\_leaves.
  - Set earned\_leaves from (flt(annual\_leaves) ÷ divide\_by\_frequency at frequency).
  - If pro\_rated.
    - If not (period\_start\_date or period\_end\_date).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in period\_start\_date → period\_end\_date.
      - Set today\_date from (Platform.flags.current\_date or getdate()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.current\_date → getdate().
      - Set tuple(period\_start\_date, period\_end\_date) from get\_sub\_period\_start\_and\_end(today\_date, frequency).
    - Set earned\_leaves from calculate\_pro\_rated\_leaves(earned\_leaves, date\_of\_joining, period\_start\_date, period\_end\_date, is\_earned\_leave = true).
  - Set earned\_leaves from round\_earned\_leaves(earned\_leaves, rounding).
- Return earned\_leaves.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L149) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L498)

<a id="op-fd19f268d789ee"></a>
### Get sub period start and end

`operation_workforce_human_resources_utils_business_behavior_get_subordinate_period_start_and_end`

**Inputs** date, frequency, effective\_from = no value.

**Explicit results** get\_half\_year\_periods(date, effective\_from) · mapping(“Monthly” → tuple(get\_first\_day(date), get\_last\_day(date)), “Quarterly” → tuple(get\_quarter\_start(date), get\_quarter\_ending(date)), “Half-Yearly” → tuple(get\_semester\_start(date), get\_semester\_end( ….

**Local steps**

- If (frequency equals “Half-Yearly” and effective\_from).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in frequency equals “Half-Yearly” → effective\_from.
  - Return get\_half\_year\_periods(date, effective\_from).
- Return mapping(“Monthly” → tuple(get\_first\_day(date), get\_last\_day(date)), “Quarterly” → tuple(get\_quarter\_start(date), get\_quarter\_ending(date)), “Half-Yearly” → tuple(get\_semester\_start(date), get\_semester\_end( ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L522) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L156) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L505)

<a id="op-5195ce297a255b"></a>
### Round earned leaves

`operation_workforce_human_resources_utils_business_behavior_round_earned_leaves`

**Inputs** earned\_leaves, rounding.

**Explicit results** earned\_leaves.

**Local steps**

- If not rounding.
  - Return earned\_leaves.
- If rounding equals “0.25”.
  - Set earned\_leaves from (round((earned\_leaves × 4)) ÷ 4).
- Otherwise.
  - If rounding equals “0.5”.
    - Set earned\_leaves from (round((earned\_leaves × 2)) ÷ 2).
  - Otherwise.
    - Set earned\_leaves from round(earned\_leaves).
- Return earned\_leaves.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L834) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L161) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L510)

<a id="op-235cb2ee5d4674"></a>
### Get leave allocations

`operation_workforce_human_resources_utils_business_behavior_get_leave_allocations`

**Inputs** date, leave\_type.

**Explicit results** (query.run(as\_dict = 1) or list()).

**Local steps**

- Set employee from Platform.qb.DocType(“Employee”).
- Set leave\_allocation from Platform.qb.DocType(“Leave Allocation”).
- Set earned\_leave\_schedule from Platform.qb.DocType(“Earned Leave Schedule”).
- Set query from nested operand in the contract(nested operand in the contract).select(leave\_allocation.name, leave\_allocation.employee, leave\_allocation.from\_date, leave\_allocation.to\_date, …).where(((((nested operand in  ….
- Return (query.run(as\_dict = 1) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run(as\_dict = 1) → list().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L1051) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L146) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L495)

<a id="op-1af3fe012661dd"></a>
### Get earned leaves

`operation_workforce_human_resources_utils_business_behavior_get_earned_leaves`

**Inputs** no declared parameters.

**Record and data access** read “Leave Type” via get\_all.

**Explicit results** Platform.get\_all(“Leave Type”, fields = list(“name”, “max\_leaves\_allowed”, “earned\_leave\_frequency”, “rounding”, …), filters = mapping(“is\_earned\_leave” → 1)).

**Local steps**

- Return Platform.get\_all(“Leave Type”, fields = list(“name”, “max\_leaves\_allowed”, “earned\_leave\_frequency”, “rounding”, …), filters = mapping(“is\_earned\_leave” → 1)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L1677) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L137) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L486)

<a id="op-cbd104682d8c7a"></a>
### Create additional leave ledger entry

`operation_workforce_human_resources_utils_business_behavior_create_additional_leave_ledger_entry`

**Inputs** allocation, leaves, date.

**Local steps**

- Set allocation.new\_leaves\_allocated from leaves.
- Set allocation.from\_date from date.
- Set allocation.unused\_leaves from 0.
- Evaluate allocation.create\_leave\_ledger\_entry().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L1812) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L131) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L480)

<a id="op-616bbe64c64b75"></a>
### Get expected allocation date for period

`operation_workforce_human_resources_utils_business_behavior_get_expected_allocation_date_for_period`

**Inputs** frequency, allocate\_on\_day, date, date\_of\_joining = no value, effective\_from = no value.

**Explicit results** mapping(“Monthly” → mapping(“First Day” → get\_first\_day(date), “Last Day” → get\_last\_day(date), “Date of Joining” → doj), “Quarterly” → mapping(“First Day” → get\_quarter\_start(date), “Last Day” → get\_quart ….

**Local steps**

- Attempt the following.
  - Set doj from date\_of\_joining.replace(month = date.month, year = date.year).
- On failure (tuple(ValueError, AttributeError)).
  - Set doj from datetime.date(date.year, date.month, calendar.monthrange(date.year, date.month) at 1).
- If (frequency equals “Half-Yearly” and effective\_from).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in frequency equals “Half-Yearly” → effective\_from.
  - Set tuple(period\_start, period\_end) from get\_half\_year\_periods(date, effective\_from).
  - Set half\_yearly\_dates from mapping(“First Day” → period\_start, “Last Day” → period\_end).
- Otherwise.
  - Set half\_yearly\_dates from mapping(“First Day” → get\_semester\_start(date), “Last Day” → get\_semester\_end(date)).
- Return mapping(“Monthly” → mapping(“First Day” → get\_first\_day(date), “Last Day” → get\_last\_day(date), “Date of Joining” → doj), “Quarterly” → mapping(“First Day” → get\_quarter\_start(date), “Last Day” → get\_quart ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L1926) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L141) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L490)

<a id="op-9cf7d84d7a4643"></a>
### Get salary assignments

`operation_workforce_human_resources_utils_business_behavior_get_salary_assignments`

**Inputs** employee, payroll\_period.

**Record and data access** read “Payroll Period” via get\_value · read “Salary Structure Assignment” via get\_all.

**Explicit results** assignments.

**Local steps**

- Set tuple(start\_date, end\_date) from Platform.db.get\_value(“Payroll Period”, payroll\_period, list(“start\_date”, “end\_date”)).
- Set assignments from Platform.get\_all(“Salary Structure Assignment”, filters = mapping(“employee” → employee, “docstatus” → 1, “from\_date” → list(“between”, tuple(start\_date, end\_date))), fields = list(“\*”), order\_by = “from\_date”).
- If (not assignments or getdate(assignments at 0.from\_date) &gt; getdate(start\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not assignments → getdate(assignments at 0.from\_date) &gt; getdate(start\_date).
  - Set past\_assignment from Platform.get\_all(“Salary Structure Assignment”, filters = mapping(“employee” → employee, “docstatus” → 1, “from\_date” → list(“&lt;”, start\_date)), fields = list(“\*”), order\_by = “from\_date desc”, limit = 1).
  - If past\_assignment.
    - Set assignments from (past\_assignment + assignments).
- Return assignments.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L2545) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L152) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L501)

<a id="op-3270a4c363a883"></a>
### Get sal slip total benefit given

`operation_workforce_human_resources_utils_business_behavior_get_selling_slip_total_benefit_given`

**Inputs** employee, payroll\_period, component = false.

**Explicit results** total\_given\_benefit\_amount.

**Local steps**

- Set total\_given\_benefit\_amount from 0.
- Set start\_date from payroll\_period.start\_date.
- Set end\_date from payroll\_period.end\_date.
- Set ss from Platform.qb.DocType(“Salary Slip”).
- Set sd from Platform.qb.DocType(“Salary Detail”).
- Set query from nested operand in the contract(nested operand in the contract).from\_(sd).select(Sum(nested operand in the contract.amount).as\_(“total\_amount”)).where(((((((nested operand in the contract bitwise and nested ….
- If component.
  - Set query from query.where(sd.salary\_component equals component).
- Set sum\_of\_given\_benefit from query.run(as\_dict = true).
- If (sum\_of\_given\_benefit and flt(sum\_of\_given\_benefit at 0.total\_amount) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sum\_of\_given\_benefit → flt(sum\_of\_given\_benefit at 0.total\_amount) &gt; 0.
  - Set total\_given\_benefit\_amount from sum\_of\_given\_benefit at 0.total\_amount.
- Return total\_given\_benefit\_amount.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L3046) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L153) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L502)

<a id="op-45ca1e71b3a6bd"></a>
### Get holiday dates for employee

`operation_workforce_human_resources_utils_business_behavior_get_holiday_dates_for_employee`

**Inputs** employee, start\_date, end\_date.

**Explicit results** list of cstr(h.holiday\_date) for h drawn from holidays.

**Local steps**

- Set holidays from get\_holidays\_for\_employee(employee, start\_date, end\_date).
- Return list of cstr(h.holiday\_date) for h drawn from holidays.
  - Draw h from holidays.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L3780) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L144) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L493)

<a id="op-0ad6205f5710e6"></a>
### Get holidays for employee

`operation_workforce_human_resources_utils_business_behavior_get_holidays_for_employee`

**Inputs** employee, start\_date, end\_date, raise\_exception = true, only\_non\_weekly = false.

**Explicit results** get\_holidays\_in\_ranges(holiday\_list\_ranges, skip\_weekly\_offs = only\_non\_weekly).

**Local steps**

- Bind dependencies get\_holiday\_list\_ranges\_for\_employee, get\_holidays\_in\_ranges.
- Set holiday\_list\_ranges from get\_holiday\_list\_ranges\_for\_employee(employee, start\_date, end\_date, raise\_exception = raise\_exception).
- Return get\_holidays\_in\_ranges(holiday\_list\_ranges, skip\_weekly\_offs = only\_non\_weekly).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L85) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L145) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L494)

<a id="op-e333a96416d729"></a>
### Calculate annual eligible hra exemption

`operation_workforce_human_resources_utils_business_behavior_calculate_annual_eligible_hra_exemption`

**Inputs** doc.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Explicit results** mapping().

**Local steps**

- Return mapping().

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L4223) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L126) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L475)

<a id="op-d413f695f630a2"></a>
### Calculate hra exemption for period

`operation_workforce_human_resources_utils_business_behavior_calculate_hra_exemption_for_period`

**Inputs** doc.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Explicit results** mapping().

**Local steps**

- Return mapping().

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L4269) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L127) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L476)

<a id="op-4ebc6f168d237b"></a>
### Calculate tax with marginal relief

`operation_workforce_human_resources_utils_business_behavior_calculate_tax_with_marginal_relief`

**Inputs** tax\_slab, tax\_amount, annual\_taxable\_earning.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Explicit results** no value.

**Local steps**

- Return no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L4315) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L128) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L477)

<a id="op-3fa648aab3e83b"></a>
### Get previous claimed amount

`operation_workforce_human_resources_utils_business_behavior_get_previous_claimed_amount`

**Inputs** employee, payroll\_period, non\_pro\_rata = false, component = false.

**Explicit results** total\_claimed\_amount.

**Local steps**

- Set total\_claimed\_amount from 0.
- Set ebc from Platform.qb.DocType(“Employee Benefit Claim”).
- Set query from nested operand in the contract.qb.from\_(ebc).select(Sum(nested operand in the contract.claimed\_amount).as\_(“total\_amount”)).where(((ebc.employee equals employee bitwise and ebc.docstatus equals 1) bitwise  ….
- If non\_pro\_rata.
  - Set query from query.where(ebc.pay\_against\_benefit\_claim equals 1).
- If component.
  - Set query from query.where(ebc.earning\_component equals component).
- Set sum\_of\_claimed\_amount from query.run(as\_dict = true).
- If (sum\_of\_claimed\_amount and flt(sum\_of\_claimed\_amount at 0.total\_amount) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sum\_of\_claimed\_amount → flt(sum\_of\_claimed\_amount at 0.total\_amount) &gt; 0.
  - Set total\_claimed\_amount from sum\_of\_claimed\_amount at 0.total\_amount.
- Return total\_claimed\_amount.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L4374) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L150) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L499)

<a id="op-621dda6e7eb802"></a>
### Share doc with approver

`operation_workforce_human_resources_utils_business_behavior_share_record_with_approver`

**Inputs** doc, user.

**State and service calls** msgprint with translated “Shared document with the user {0} with 'Submit' permission”.format(user).

**Explicit results** no value.

**Local steps**

- If not user.
  - Return no value.
- If not Platform.has\_permission(doc = doc, ptype = “submit”, user = user).
  - Evaluate Platform.share.add\_docshare(doc.doctype, doc.name, user, submit = 1, flags = mapping(“ignore\_share\_permission” → true)).
  - Evaluate Platform.msgprint(translated “Shared document with the user {0} with 'Submit' permission”.format(user), alert = true).
- Set doc\_before\_save from doc.get\_doc\_before\_save().
- If doc\_before\_save.
  - Set approvers from mapping(“Leave Application” → “leave\_approver”, “Expense Claim” → “expense\_approver”, “Shift Request” → “approver”).
  - Set approver from approvers.get(doc.doctype).
  - If doc\_before\_save.get(approver) differs from doc.get(approver).
    - Evaluate Platform.share.remove(doc.doctype, doc.name, doc\_before\_save.get(approver)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doc = doc, ptype = “submit”, user = user).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L4896) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L165) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L514)

<a id="op-e93a2e5f8faafd"></a>
### Validate active employee

`operation_workforce_human_resources_utils_business_behavior_validate_active_employee`

**Inputs** employee, method = no value.

**Record and data access** read “Employee” via get\_value.

**Explicit failure paths** validation helper with InactiveEmployeeStatusError — translated “Transactions cannot be created for an Inactive Employee {0}.”.format(get\_link\_to\_form(“Employee”, employee)).

**Local steps**

- If isinstance(employee, (dict bitwise or Document)).
  - Set employee from employee.get(“employee”).
- If (employee and Platform.db.get\_value(“Employee”, employee, “status”) equals “Inactive”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in employee → Platform.db.get\_value(“Employee”, employee, “status”) equals “Inactive”.
  - Call the validation error handler Platform.throw(translated “Transactions cannot be created for an Inactive Employee {0}.”.format(get\_link\_to\_form(“Employee”, employee)), InactiveEmployeeStatusError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L5424) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L170) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L519)

<a id="op-aaec63734db3a7"></a>
### Validate loan repay from salary

`operation_workforce_human_resources_utils_business_behavior_validate_loan_repay_from_salary`

**Inputs** doc, method = no value.

**Explicit failure paths** validation helper — translated “Please select an Applicant” · validation helper — translated “Please select a Company” · validation helper — translated “Loan cannot be repayed from salary for Employee {0} because salary is processed in currency {1}”.format(doc.applicant, employee\_currency) · validation helper — translated “Repay From Salary can be selected only for term loans”.

**Local steps**

- If (doc.applicant\_type equals “Employee” and doc.repay\_from\_salary).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.applicant\_type equals “Employee” → doc.repay\_from\_salary.
  - Bind dependencies get\_employee\_currency.
  - If not doc.applicant.
    - Call the validation error handler Platform.throw(translated “Please select an Applicant”).
  - If not doc.company.
    - Call the validation error handler Platform.throw(translated “Please select a Company”).
  - Set employee\_currency from get\_employee\_currency(doc.applicant).
  - Set company\_currency from Enterprise.get\_company\_currency(doc.company).
  - If employee\_currency differs from company\_currency.
    - Call the validation error handler Platform.throw(translated “Loan cannot be repayed from salary for Employee {0} because salary is processed in currency {1}”.format(doc.applicant, employee\_currency)).
- If (not doc.is\_term\_loan and doc.repay\_from\_salary).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.is\_term\_loan → doc.repay\_from\_salary.
  - Call the validation error handler Platform.throw(translated “Repay From Salary can be selected only for term loans”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L5686) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L174) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L523)

<a id="op-01a5335799d4e5"></a>
### Get matching queries

`operation_workforce_human_resources_utils_business_behavior_get_matching_queries`

**Inputs** bank\_account, company, transaction, document\_types, exact\_match, account\_from\_to = no value, from\_date = no value, to\_date = no value, filter\_by\_reference\_date = no value, from\_reference\_date = no value, to\_reference\_date = no value, common\_filters = no value.

**Explicit results** queries.

**Local steps**

- Set queries from list().
- If transaction.withdrawal &gt; 0.
  - If “expense\_claim” belongs to document\_types.
    - Set ec\_amount\_matching from get\_ec\_matching\_query(bank\_account, company, exact\_match, from\_date, …).
    - Evaluate queries.extend(list(ec\_amount\_matching)).
- Return queries.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L6111) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L148) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L497)

<a id="op-f3c3b5835d4f85"></a>
### Get ec matching query

`operation_workforce_human_resources_utils_business_behavior_get_ec_matching_query`

**Inputs** bank\_account, company, exact\_match, from\_date = no value, to\_date = no value, common\_filters = no value.

**Record and data access** read “Mode of Payment Account” via get\_all.

**Explicit results** ec\_query.

**Local steps**

- Set filters from list().
- Set ec from qb.DocType(“Expense Claim”).
- Set mode\_of\_payments from list of x at “parent” for x drawn from Platform.db.get\_all(“Mode of Payment Account”, filters = mapping(“default\_account” → bank\_account), fields = list(“parent”)).
  - Draw x from Platform.db.get\_all(“Mode of Payment Account”, filters = mapping(“default\_account” → bank\_account), fields = list(“parent”)).
- Set company\_currency from get\_company\_currency(company).
- Evaluate filters.append(ec.docstatus equals 1).
- Evaluate filters.append(ec.is\_paid equals 1).
- Evaluate filters.append(ec.clearance\_date.isnull()).
- If mode\_of\_payments.
  - Evaluate filters.append(ec.mode\_of\_payment.isin(mode\_of\_payments)).
- If common\_filters.
  - Set ref\_rank from (nested operand in the contract.Case().when(ec.employee equals common\_filters.party, 1).else\_(0) + 1).
  - If exact\_match.
    - Evaluate filters.append(ec.total\_amount\_reimbursed equals common\_filters.amount).
  - Otherwise.
    - Evaluate filters.append(ec.total\_amount\_reimbursed.gt(common\_filters.amount)).
- Otherwise.
  - Set ref\_rank from ConstantColumn(1).
- If (from\_date and to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → to\_date.
  - Evaluate filters.append(ec.posting\_date at slice from\_date to to\_date).
- Set ec\_query from qb.from\_(ec).select(ref\_rank.as\_(“rank”), ConstantColumn(“Expense Claim”).as\_(“doctype”), ec.name, ec.total\_sanctioned\_amount.as\_(“paid\_amount”), …).where(Criterion.all(filters)).
- If (from\_date and to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → to\_date.
  - Set ec\_query from ec\_query.orderby(ec.posting\_date).
- Return ec\_query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0097.json#L6384) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L138) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L487)

<a id="op-858efa08f2faf5"></a>
### Validate bulk tool fields

`operation_workforce_human_resources_utils_business_behavior_validate_bulk_tool_fields`

**Inputs** self, fields, employees, from\_date = no value, to\_date = no value.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “{0} is required”.format(translated self.meta.get\_label(d)) · validation helper — translated “Please select at least one employee to perform this action.”.

**Local steps**

- For each d in fields.
  - If not self.get(d).
    - Call the validation error handler Platform.throw(translated “{0} is required”.format(translated self.meta.get\_label(d)), title = translated “Missing Field”).
- If (self.get(from\_date) and self.get(to\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(from\_date) → self.get(to\_date).
  - Evaluate self.validate\_from\_to\_dates(from\_date, to\_date).
- If not employees.
  - Call the validation error handler Platform.throw(translated “Please select at least one employee to perform this action.”, title = translated “No Employees Selected”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L171) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L520)

<a id="op-32d6b6c38a637b"></a>
### Notify bulk action status

`operation_workforce_human_resources_utils_business_behavior_notify_bulk_action_status`

**Inputs** doctype, failure, success.

**Declared result** no value.

**State and service calls** msgprint with msg.

**Local steps**

- Evaluate Platform.clear\_messages().
- Set msg from empty text.
- Set title from empty text.
- If failure.
  - Update msg using + translated “Failed to create/submit {0} for employees:”.format(doctype).
  - Update msg using + ((one space + comma\_and(failure, false)) + text in the contract).
  - Update msg using + translated “Check {0} for more details”.format(text in the contract).format(doctype, translated “Error Log”).
  - If success.
    - Set title from translated “Partial Success”.
    - Update msg using + text in the contract.
  - Otherwise.
    - Set title from translated “Creation Failed”.
- Otherwise.
  - Set title from translated “Success”.
- If success.
  - Update msg using + translated “Successfully created {0} for employees:”.format(doctype).
  - Update msg using + (one space + comma\_and(success, false)).
- If failure.
  - Set indicator from “orange” when success, otherwise “red”.
    - Value choice on success — true gives “orange”, false gives “red”.
- Otherwise.
  - Set indicator from “green”.
- Evaluate Platform.msgprint(msg, indicator = indicator, title = title, is\_minimizable = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L417) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L160) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L509)
