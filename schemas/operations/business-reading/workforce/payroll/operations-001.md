# Payroll and benefits · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Accrued earnings report

<a id="op-8798c2a643b8b3"></a>
### Execute

`operation_workforce_payroll_report_accrued_earnings_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L6893) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L936) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1283)

<a id="op-b8c80c3e11d97d"></a>
### Get columns

`operation_workforce_payroll_report_accrued_earnings_report_business_behavior_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(mapping(“label” → translated “Employee”, “fieldname” → “employee”, “fieldtype” → “Link”, “options” → “Employee”, …), mapping(“label” → translated “Employee Name”, “fieldname” → “employee\_name”, “field ….

**Local steps**

- Return list(mapping(“label” → translated “Employee”, “fieldname” → “employee”, “fieldtype” → “Link”, “options” → “Employee”, …), mapping(“label” → translated “Employee Name”, “fieldname” → “employee\_name”, “field ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0142.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L937) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1284)

<a id="op-e1a9971da97bd1"></a>
### Get data

`operation_workforce_payroll_report_accrued_earnings_report_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set EBL from DocType(“Employee Benefit Ledger”).
- Set EMP from DocType(“Employee”).
- Set SC from DocType(“Salary Component”).
- Set query from nested operand in the contract(nested operand in the contract).inner\_join(SC).on(EBL.salary\_component equals SC.name).select(EBL.employee, EBL.employee\_name, EBL.payroll\_period, EBL.salary\_component, …).
- If filters.get(“company”).
  - Set query from query.where(EBL.company equals filters at “company”).
- If filters.get(“employee”).
  - Set query from query.where(EBL.employee equals filters at “employee”).
- If filters.get(“department”).
  - Set query from query.where(EMP.department equals filters at “department”).
- If filters.get(“branch”).
  - Set query from query.where(EMP.branch equals filters at “branch”).
- If filters.get(“payroll\_period”).
  - Set query from query.where(EBL.payroll\_period equals filters at “payroll\_period”).
- If filters.get(“salary\_component”).
  - Set query from query.where(EBL.salary\_component equals filters at “salary\_component”).
- Set query from query.where(SC.accrual\_component equals 1).
- Set flexible\_benefit from filters.get(“flexible\_benefit”).
- If flexible\_benefit equals “Yes”.
  - Set query from query.where(EBL.flexible\_benefit equals 1).
- Otherwise.
  - If flexible\_benefit equals “No”.
    - Set query from query.where((EBL.flexible\_benefit equals 0 bitwise or EBL.flexible\_benefit.isnull())).
- Set query from query.orderby(EBL.employee, EBL.salary\_component, EBL.flexible\_benefit).
- Set ledger\_entries from query.run(as\_dict = true).
- Set grouped\_data from mapping().
- For each entry in ledger\_entries.
  - Set key from tuple(entry.employee, entry.employee\_name, entry.payroll\_period, entry.salary\_component, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.flexible\_benefit → 0.
  - If key does not belong to grouped\_data.
    - Set grouped\_data at key from mapping(“employee” → entry.employee, “employee\_name” → entry.employee\_name, “payroll\_period” → entry.payroll\_period, “salary\_component” → entry.salary\_component, …).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.flexible\_benefit → 0.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.yearly\_benefit → 0.
  - If entry.transaction\_type equals “Accrual”.
    - Update grouped\_data at key at “total\_accrued” using + (entry.amount or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.amount → 0.
  - Otherwise.
    - If entry.transaction\_type equals “Payout”.
      - Update grouped\_data at key at “total\_payout” using + (entry.amount or 0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.amount → 0.
- Set data from list().
- For each row\_data in grouped\_data.values().
  - Set row\_data at “unpaid\_accrual” from (row\_data at “total\_accrued” − row\_data at “total\_payout”).
  - If (not row\_data at “flexible\_benefit” and row\_data at “unpaid\_accrual” &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row\_data at “flexible\_benefit” → row\_data at “unpaid\_accrual” &gt; 0.
    - Set row\_data at “create\_additional\_salary” from formatted text   &lt;a  onclick="create\_additional\_salary('{row\_data at “employee”}',     '{row\_data at “salary\_component”}',     {row\_d.
  - Otherwise.
    - Set row\_data at “create\_additional\_salary” from empty text.
  - Evaluate data.append(row\_data).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0142.json#L885) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L938) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1285)

## Record · Additional salary

[Record definition](../../../../data/record-types/additional_salary.json)

<a id="op-9481270514f329"></a>
### Additional Salary.before validate

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_before_validate`

**Inputs** self.

**Local steps**

- If self.is\_recurring.
  - Set self.payroll\_date from no value.
- Otherwise.
  - Set self.from\_date from no value.
  - Set self.to\_date from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0105.json#L1977) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L314) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L663)

<a id="op-48ddb8daed3c24"></a>
### Additional Salary.on submit

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_employee\_referral().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update employee referral](operations-001.md#op-8aca1cd4d1b3e0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0105.json#L2070) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L317) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L666)

<a id="op-906516a5b14166"></a>
### Additional Salary.on cancel

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_employee\_referral(cancel = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update employee referral](operations-001.md#op-8aca1cd4d1b3e0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0105.json#L2121) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L316) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L665)

<a id="op-6fa5da15a6190d"></a>
### Additional Salary.validate

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Amount should not be less than zero”.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate self.validate\_dates().
- Evaluate self.validate\_salary\_structure().
- Evaluate self.validate\_recurring\_additional\_salary\_overlap().
- Evaluate self.validate\_employee\_referral().
- Evaluate self.validate\_duplicate\_additional\_salary().
- Evaluate self.validate\_tax\_component\_overwrite().
- Evaluate self.validate\_accrual\_component().
- <a id="op-6fa5da15a6190d-guard-11"></a>If self.amount &lt; 0.
  - Call the validation error handler Platform.throw(translated “Amount should not be less than zero”).
- If self.ref\_doctype equals “Employee Advance”.
  - Evaluate self.validate\_employee\_advance\_return().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.amount &lt; 0, self.amount = -1 selects the branch that calls the validation-error handler with translated “Amount should not be less than zero”. With self.amount = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6fa5da15a6190d-guard-11)

**Methods declared on this owner** [validate dates](operations-001.md#op-c84b870d588f8d), [validate salary structure](operations-001.md#op-a9e8c53462c1b3), [validate recurring additional salary overlap](operations-001.md#op-fbc9b2a9d0a705), [validate employee referral](operations-001.md#op-4ab10e341efa2d), [validate duplicate additional salary](operations-001.md#op-92abf543bff40c), [validate tax component overwrite](operations-001.md#op-1d5b6608de0e25), [validate accrual component](operations-001.md#op-4167c95d06da67), [validate employee advance return](operations-001.md#op-be6bc038a56733).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0105.json#L2183) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L319) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L668)

<a id="op-a9e8c53462c1b3"></a>
### Additional Salary.validate salary structure

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_validate_salary_structure`

**Inputs** self.

**Record and data access** read “Salary Structure Assignment” via get\_value · read “Salary Detail” via get\_value.

**State and service calls** msgprint with translated “Overwrite Salary Structure Amount is disabled as the Salary Component: {0} not part of the Salary Structure: {1}”.format(self.salary\_component, salary\_structure).

**Explicit failure paths** validation helper — translated “There is no Salary Structure assigned to {0}. First assign a Salary Structure.”.format(self.employee).

**Local steps**

- Set salary\_structure from Platform.db.get\_value(“Salary Structure Assignment”, mapping(“employee” → self.employee, “docstatus” → 1, “from\_date” → list(“&lt;=”, (self.payroll\_date or self.from\_date))), “salary\_structure”, order\_by = “f ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.payroll\_date → self.from\_date.
- If not salary\_structure.
  - Call the validation error handler Platform.throw(translated “There is no Salary Structure assigned to {0}. First assign a Salary Structure.”.format(self.employee)).
- If self.overwrite\_salary\_structure\_amount.
  - Set is\_structure\_component from Platform.db.get\_value(“Salary Detail”, mapping(“parenttype” → “Salary Structure”, “parent” → salary\_structure, “salary\_component” → self.salary\_component)).
  - If not is\_structure\_component.
    - Set self.overwrite\_salary\_structure\_amount from 0.
    - Evaluate Platform.msgprint(translated “Overwrite Salary Structure Amount is disabled as the Salary Component: {0} not part of the Salary Structure: {1}”.format(self.salary\_component, salary\_structure)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0105.json#L2495) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L326) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L675)

<a id="op-fbc9b2a9d0a705"></a>
### Additional Salary.validate recurring additional salary overlap

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_validate_recurring_additional_salary_overlap`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Additional Salary: {0} already exist for Salary Component: {1} for period {2} and {3}”.format(bold(comma\_and(additional\_salaries)), bold(self.salary\_component), bold(formatdate(self.from\_date)) ….

**Local steps**

- If self.is\_recurring.
  - Set AdditionalSalary from Platform.qb.DocType(“Additional Salary”).
  - Set additional\_salaries from nested operand in the contract(nested operand in the contract).select(AdditionalSalary.name).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
  - If (additional\_salaries and len(additional\_salaries)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in additional\_salaries → len(additional\_salaries).
    - Call the validation error handler Platform.throw(translated “Additional Salary: {0} already exist for Salary Component: {1} for period {2} and {3}”.format(bold(comma\_and(additional\_salaries)), bold(self.salary\_component), bold(formatdate(s ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0105.json#L2946) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L325) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L674)

<a id="op-c84b870d588f8d"></a>
### Additional Salary.validate dates

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_validate_dates`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “From and to dates are mandatory for recurring type additional salaries.” · validation helper — translated “Payroll date is mandatory for non-recurring type additional salaries.” · validation helper — translated “Payroll date can not be less than employee's joining date.” · validation helper — translated “From date can not be less than employee's joining date.” · validation helper — translated “To date can not be greater than employee's relieving date.” · 1 additional forms in the steps below.

**Local steps**

- Set tuple(date\_of\_joining, relieving\_date) from Platform.db.get\_value(“Employee”, self.employee, list(“date\_of\_joining”, “relieving\_date”)).
- Evaluate self.validate\_from\_to\_dates(“from\_date”, “to\_date”).
- If (self.is\_recurring and not (self.from\_date and self.to\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_recurring → not (self.from\_date and self.to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_date → self.to\_date.
  - Call the validation error handler Platform.throw(translated “From and to dates are mandatory for recurring type additional salaries.”).
- Otherwise.
  - If (not self.is\_recurring and not self.payroll\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_recurring → not self.payroll\_date.
    - Call the validation error handler Platform.throw(translated “Payroll date is mandatory for non-recurring type additional salaries.”).
- If date\_of\_joining.
  - If (self.payroll\_date and getdate(self.payroll\_date) &lt; getdate(date\_of\_joining)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.payroll\_date → getdate(self.payroll\_date) &lt; getdate(date\_of\_joining).
    - Call the validation error handler Platform.throw(translated “Payroll date can not be less than employee's joining date.”).
  - Otherwise.
    - If (self.from\_date and getdate(self.from\_date) &lt; getdate(date\_of\_joining)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_date → getdate(self.from\_date) &lt; getdate(date\_of\_joining).
      - Call the validation error handler Platform.throw(translated “From date can not be less than employee's joining date.”).
- If relieving\_date.
  - If (self.to\_date and getdate(self.to\_date) &gt; getdate(relieving\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.to\_date → getdate(self.to\_date) &gt; getdate(relieving\_date).
    - Call the validation error handler Platform.throw(translated “To date can not be greater than employee's relieving date.”).
  - If (self.payroll\_date and getdate(self.payroll\_date) &gt; getdate(relieving\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.payroll\_date → getdate(self.payroll\_date) &gt; getdate(relieving\_date).
    - Call the validation error handler Platform.throw(translated “Payroll date can not be greater than employee's relieving date.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L93) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L321) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L670)

<a id="op-4ab10e341efa2d"></a>
### Additional Salary.validate employee referral

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_validate_employee_referral`

**Inputs** self.

**Record and data access** read “Employee Referral” via get\_value.

**Explicit failure paths** validation helper — translated “Employee Referral {0} is not applicable for referral bonus.”.format(self.ref\_docname) · validation helper — translated “Earning Salary Component is required for Employee Referral Bonus.” · validation helper — translated “Additional Salary for referral bonus can only be created against Employee Referral with status {0}”.format(Platform.bold(translated “Accepted”)).

**Local steps**

- If self.ref\_doctype equals “Employee Referral”.
  - Set referral\_details from Platform.db.get\_value(“Employee Referral”, self.ref\_docname, list(“is\_applicable\_for\_referral\_bonus”, “status”), as\_dict = 1).
  - If not referral\_details.is\_applicable\_for\_referral\_bonus.
    - Call the validation error handler Platform.throw(translated “Employee Referral {0} is not applicable for referral bonus.”.format(self.ref\_docname)).
  - If self.type equals “Deduction”.
    - Call the validation error handler Platform.throw(translated “Earning Salary Component is required for Employee Referral Bonus.”).
  - If referral\_details.status differs from “Accepted”.
    - Call the validation error handler Platform.throw(translated “Additional Salary for referral bonus can only be created against Employee Referral with status {0}”.format(Platform.bold(translated “Accepted”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0105.json#L4271) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L324) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L673)

<a id="op-92abf543bff40c"></a>
### Additional Salary.validate duplicate additional salary

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_validate_duplicate_additional_salary`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If not self.overwrite\_salary\_structure\_amount.
  - Return no value.
- Set AdditionalSalary from Platform.qb.DocType(“Additional Salary”).
- Set existing\_additional\_salary from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and (nested operand in the contract bitwise or nest ….
- If existing\_additional\_salary.
  - Set msg from translated “Additional Salary for this salary component with {0} enabled already exists for this date”.format(Platform.bold(translated “Overwrite Salary Structure Amount”)).
  - Update msg using + text in the contract.
  - Update msg using + translated “Reference: {0}”.format(get\_link\_to\_form(“Additional Salary”, existing\_additional\_salary)).
  - Call the validation error handler Platform.throw(msg, title = translated “Duplicate Overwritten Salary”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0105.json#L4662) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L322) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L671)

<a id="op-1d5b6608de0e25"></a>
### Additional Salary.validate tax component overwrite

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_validate_tax_component_overwrite`

**Inputs** self.

**Record and data access** read “Salary Component” via get\_value.

**State and service calls** msgprint with translated “This will overwrite the tax component {0} in the salary slip and tax won't be calculated based on the Income …”.format(Platform.bold(self.salary\_component)).

**Explicit results** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If not Platform.db.get\_value(“Salary Component”, self.salary\_component, “variable\_based\_on\_taxable\_salary”).
  - Return no value.
- If self.overwrite\_salary\_structure\_amount.
  - Evaluate Platform.msgprint(translated “This will overwrite the tax component {0} in the salary slip and tax won't be calculated based on the Income …”.format(Platform.bold(self.salary\_component)), title = translate ….
- Otherwise.
  - Set msg from translated “{0} has {1} enabled”.format(get\_link\_to\_form(“Salary Component”, self.salary\_component), Platform.bold(translated “Variable Based On Taxable Salary”)).
  - Update msg using + (text in the contract + translated “To overwrite the salary component amount for a tax component, please enable {0}”.format(Platform.bold(translated “Overwrite Salary Structure Amount”))).
  - Call the validation error handler Platform.throw(msg, title = translated “Invalid Additional Salary”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0105.json#L5308) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L327) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L676)

<a id="op-4167c95d06da67"></a>
### Additional Salary.validate accrual component

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_validate_accrual_component`

**Inputs** self.

**Record and data access** read “Salary Component” via get\_value.

**State and service calls** msgprint with translated “{0} is an Accrual Component and this will be recorded as a payout in Employee Benefits Ledger”.format(Platform.bold(self.salary\_component)).

**Local steps**

- If Platform.db.get\_value(“Salary Component”, self.salary\_component, “accrual\_component”).
  - Evaluate Platform.msgprint(translated “{0} is an Accrual Component and this will be recorded as a payout in Employee Benefits Ledger”.format(Platform.bold(self.salary\_component)), title = translated “Warning”, indi ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0105.json#L5757) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L320) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L669)

<a id="op-be6bc038a56733"></a>
### Additional Salary.validate employee advance return

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_validate_employee_advance_return`

**Inputs** self.

**Record and data access** resolve a document from “Employee Advance” via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If (self.ref\_doctype differs from “Employee Advance” or not self.ref\_docname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.ref\_doctype differs from “Employee Advance” → not self.ref\_docname.
  - Return no value.
- Set precision from self.precision(“amount”).
- Set advance from Platform.get\_doc(“Employee Advance”, self.ref\_docname).
- Set AdditionalSalary from Platform.qb.DocType(“Additional Salary”).
- Set scheduled\_deductions from (nested operand in the contract.select(nested operand in the contract.name, nested operand in the contract.amount).where((((nested operand in the contract bitwise and nested operand in the contract) bitwis ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).select(AdditionalSalary.name, AdditionalSalary.amount).where((((nested operand in the contract equals nested operand in the contract bitwise a … → list().
- Set available\_return\_amount from flt((advance.paid\_amount − advance.claimed\_amount), precision).
- Set scheduled\_return\_amount from flt(sum(generator of flt(d.amount, precision) for d drawn from scheduled\_deductions), precision).
  - Draw d from scheduled\_deductions.
- Set remaining\_return\_amount from flt((available\_return\_amount − scheduled\_return\_amount), precision).
- If flt(self.amount, precision) ≤ remaining\_return\_amount.
  - Return no value.
- Set pending\_scheduled from max(0, flt((scheduled\_return\_amount − advance.return\_amount), precision)).
- If pending\_scheduled &gt; 0.
  - Set msg from translated “Employee Advance {0} has {1} available for return. {2} has already been scheduled for deduction in {3}.”.format(get\_link\_to\_form(“Employee Advance”, self.ref\_docname), fmt\_money(remaining\_retur ….
    - Draw d from scheduled\_deductions.
- Otherwise.
  - Set msg from translated “The amount exceeds the available balance for Employee Advance {0}. Available amount for return: {1}.”.format(get\_link\_to\_form(“Employee Advance”, self.ref\_docname), fmt\_money(remaining\_return\_a ….
- Call the validation error handler Platform.throw(msg, title = translated “Amount Exceeds Available Balance”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0106.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L323) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L672)

<a id="op-8aca1cd4d1b3e0"></a>
### Additional Salary.update employee referral

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_update_employee_referral`

**Inputs** self, cancel = false.

**State and service calls** request set\_value on “Employee Referral”.

**Local steps**

- If self.ref\_doctype equals “Employee Referral”.
  - Set status from “Unpaid” when cancel, otherwise “Paid”.
    - Value choice on cancel — true gives “Unpaid”, false gives “Paid”.
  - Evaluate Platform.db.set\_value(“Employee Referral”, self.ref\_docname, “referral\_payment\_status”, status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0106.json#L1053) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L318) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L667)

<a id="op-babf76aa1d6cbe"></a>
### Additional Salary.get amount

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_get_amount`

**Inputs** self, sal\_start\_date, sal\_end\_date.

**Explicit results** (amount\_per\_day × no\_of\_days).

**Local steps**

- Set start\_date from getdate(sal\_start\_date).
- Set end\_date from getdate(sal\_end\_date).
- Set total\_days from (date\_diff(getdate(self.to\_date), getdate(self.from\_date)) + 1).
- Set amount\_per\_day from (self.amount ÷ total\_days).
- If getdate(sal\_start\_date) ≤ getdate(self.from\_date).
  - Set start\_date from getdate(self.from\_date).
- If getdate(sal\_end\_date) &gt; getdate(self.to\_date).
  - Set end\_date from getdate(self.to\_date).
- Set no\_of\_days from (date\_diff(getdate(end\_date), getdate(start\_date)) + 1).
- Return (amount\_per\_day × no\_of\_days).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0106.json#L1203) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L315) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L664)

<a id="op-fcbd751a699a84"></a>
### Additional Salary.before update after submit

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_additional_salary_before_update_after_submit`

**Inputs** self.

**Local steps**

- If not self.disabled.
  - Evaluate self.validate\_recurring\_additional\_salary\_overlap().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate recurring additional salary overlap](operations-001.md#op-fbc9b2a9d0a705).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0106.json#L1642) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L313) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L662)

<a id="op-1aa1c88080655a"></a>
### Get additional salaries

`operation_workforce_payroll_record_definitions_additional_salary_business_behavior_get_additional_salaries`

**Inputs** employee, start\_date, end\_date, component\_type.

**Explicit results** additional\_salaries.

**Explicit failure paths** validation helper — translated “Multiple Additional Salaries with overwrite property exist for Salary Component {0} between {1} and {2}.”.format(Platform.bold(d.component), start\_date, end\_date).

**Local steps**

- Bind dependencies Criterion.
- Set comp\_type from “Earning” when component\_type equals “earnings”, otherwise “Deduction”.
  - Value choice on component\_type equals “earnings” — true gives “Earning”, false gives “Deduction”.
- Set additional\_sal from Platform.qb.DocType(“Additional Salary”).
- Set component\_field from additional\_sal.salary\_component.as\_(“component”).
- Set overwrite\_field from additional\_sal.overwrite\_salary\_structure\_amount.as\_(“overwrite”).
- Set additional\_salary\_list from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- Set additional\_salaries from list().
- Set components\_to\_overwrite from list().
- For each d in additional\_salary\_list.
  - If d.overwrite.
    - If d.component belongs to components\_to\_overwrite.
      - Call the validation error handler Platform.throw(translated “Multiple Additional Salaries with overwrite property exist for Salary Component {0} between {1} and {2}.”.format(Platform.bold(d.component), start\_date, end\_date), title = transl ….
    - Evaluate components\_to\_overwrite.append(d.component).
  - Evaluate additional\_salaries.append(d).
- Return additional\_salaries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0106.json#L1711) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L328) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L677)

## Record · Arrear

[Record definition](../../../../data/record-types/arrear.json)

<a id="op-1d9ed45417fdd9"></a>
### Arrear.payroll period details

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_payroll_period_details`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** resolve a document from “Payroll Period” via get\_doc.

**Explicit results** self.\_\_payroll\_period\_details.

**Local steps**

- If not hasattr(self, “\_\_payroll\_period\_details”).
  - Set self.\_\_payroll\_period\_details from Platform.get\_doc(“Payroll Period”, self.payroll\_period).
- Return self.\_\_payroll\_period\_details.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0106.json#L6255) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L349) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L698)

<a id="op-a3b74224c0f02d"></a>
### Arrear.validate

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_dates().
- Evaluate self.validate\_salary\_structure\_assignment().
- Evaluate self.validate\_duplicate\_doc().
- Evaluate self.calculate\_salary\_structure\_arrears().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dates](operations-001.md#op-6e01a16f7fc1f5), [validate salary structure assignment](operations-002.md#op-c11656eb5ae881), [validate duplicate doc](operations-002.md#op-a8bf7517c9ab74), [calculate salary structure arrears](operations-002.md#op-be96cd159e3a82).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0106.json#L6378) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L351) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L700)

<a id="op-311baa3380eb0c"></a>
### Arrear.on submit

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_arrear\_details().
- Evaluate self.create\_additional\_salary().
- Evaluate self.create\_benefit\_ledger\_entry().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate arrear details](operations-002.md#op-6017145d6edff7), [create additional salary](operations-002.md#op-8420d940894715), [create benefit ledger entry](operations-002.md#op-e2d60445c080ce).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0106.json#L6489) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L348) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L697)

<a id="op-7157b98c01446a"></a>
### Arrear.on cancel

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate delete\_employee\_benefit\_ledger\_entry(“reference\_document”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0106.json#L6580) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L347) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L696)

<a id="op-6e01a16f7fc1f5"></a>
### Arrear.validate dates

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “From Date {0} cannot be before Payroll Period start date {1}”.format(self.arrear\_start\_date, self.payroll\_period\_details.start\_date) · validation helper — translated “From Date {0} cannot be after Payroll Period end date {1}”.format(self.arrear\_start\_date, self.payroll\_period\_details.end\_date).

**Local steps**

- If (self.arrear\_start\_date and self.payroll\_period).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.arrear\_start\_date → self.payroll\_period.
  - If getdate(self.arrear\_start\_date) &lt; self.payroll\_period\_details.start\_date.
    - Call the validation error handler Platform.throw(translated “From Date {0} cannot be before Payroll Period start date {1}”.format(self.arrear\_start\_date, self.payroll\_period\_details.start\_date)).
  - Otherwise.
    - If getdate(self.arrear\_start\_date) &gt; self.payroll\_period\_details.end\_date.
      - Call the validation error handler Platform.throw(translated “From Date {0} cannot be after Payroll Period end date {1}”.format(self.arrear\_start\_date, self.payroll\_period\_details.end\_date)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0106.json#L6647) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L353) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L702)
