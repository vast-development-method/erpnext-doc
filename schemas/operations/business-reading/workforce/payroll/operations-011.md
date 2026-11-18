# Payroll and benefits · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payroll entry

[Record definition](../../../../data/record-types/payroll_entry.json)

<a id="op-eddc4d974a43cf"></a>
### Show payroll submission status

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_show_payroll_submission_status`

**Inputs** submitted, unsubmitted, payroll\_entry.

**State and service calls** msgprint with translated “No salary slip found to submit for the above selected criteria OR salary slip already submitted” · msgprint with translated “Salary Slips submitted for period from {0} to {1}”.format(payroll\_entry.start\_date, payroll\_entry.end\_date) · msgprint with translated “Could not submit some Salary Slips: {}”.format(“, ”.join(generator of get\_link\_to\_form(“Salary Slip”, entry) for entry drawn from unsubmitted)).

**Local steps**

- If (not submitted and not unsubmitted).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not submitted → not unsubmitted.
  - Evaluate Platform.msgprint(translated “No salary slip found to submit for the above selected criteria OR salary slip already submitted”).
- Otherwise.
  - If (submitted and not unsubmitted).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in submitted → not unsubmitted.
    - Evaluate Platform.msgprint(translated “Salary Slips submitted for period from {0} to {1}”.format(payroll\_entry.start\_date, payroll\_entry.end\_date), title = translated “Success”, indicator = “green”).
  - Otherwise.
    - If unsubmitted.
      - Evaluate Platform.msgprint(translated “Could not submit some Salary Slips: {}”.format(“, ”.join(generator of get\_link\_to\_form(“Salary Slip”, entry) for entry drawn from unsubmitted)), title = translated “Failure”,  ….
        - Draw entry from unsubmitted.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0118.json#L2294) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L547) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L894)

<a id="op-02c56c484eb10b"></a>
### Get existing salary slips

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_get_existing_salary_slips`

**Inputs** employees, args.

**Explicit results** nested operand in the contract(nested operand in the contract).distinct().where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract ≥ n ….

**Local steps**

- Set SalarySlip from Platform.qb.DocType(“Salary Slip”).
- Return nested operand in the contract(nested operand in the contract).distinct().where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract ≥ n ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0118.json#L2685) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L481) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L830)

<a id="op-634bb23e421374"></a>
### Submit salary slips for employees

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_submit_salary_slips_for_employees`

**Inputs** payroll\_entry, salary\_slips, publish\_progress = true.

**Record and data access** resolve a document from “Salary Slip” via get\_doc.

**State and service calls** savepoint savepoint · call submit on salary\_slip · rollback · call db\_set on payroll\_entry · commit · 1 additional forms in the steps below.

**Local steps**

- Attempt the following.
  - Set submitted from list().
  - Set unsubmitted from list().
  - Set Platform.flags.via\_payroll\_entry from true.
  - Set count from 0.
  - Set savepoint from “before\_salary\_slip\_submission”.
  - For each entry in salary\_slips.
    - Set salary\_slip from Platform.get\_doc(“Salary Slip”, entry at 0).
    - If salary\_slip.net\_pay &lt; 0.
      - Evaluate unsubmitted.append(entry at 0).
    - Otherwise.
      - Attempt the following.
        - Evaluate Platform.db.savepoint(savepoint).
        - Evaluate salary\_slip.submit().
        - Evaluate submitted.append(salary\_slip).
      - On failure (Platform.ValidationError).
        - Evaluate Platform.db.rollback(save\_point = savepoint).
        - Evaluate unsubmitted.append(entry at 0).
    - Update count using + 1.
    - If publish\_progress.
      - Evaluate Platform.publish\_progress(((count × 100) ÷ len(salary\_slips)), title = translated “Submitting Salary Slips...”).
  - If submitted.
    - Evaluate payroll\_entry.make\_accrual\_jv\_entry(submitted).
    - Evaluate payroll\_entry.email\_salary\_slip(submitted).
    - Evaluate payroll\_entry.db\_set(mapping(“salary\_slips\_submitted” → 1, “status” → “Submitted”, “error\_message” → empty text)).
  - Evaluate show\_payroll\_submission\_status(submitted, unsubmitted, payroll\_entry).
- On failure (Exception) bound to e.
  - If not Platform.in\_test.
    - Evaluate Platform.db.rollback().
  - Evaluate log\_payroll\_failure(“submission”, payroll\_entry, e).
- On exit, including pending return or failure.
  - If not Platform.in\_test.
    - Evaluate Platform.db.commit().
  - Evaluate Platform.publish\_realtime(“completed\_salary\_slip\_submission”, user = Platform.session.user).
- Set Platform.flags.via\_payroll\_entry from false.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“completed\_salary\_slip\_submission”, user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L101) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L548) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L895)

<a id="op-e1ef9d484c9a19"></a>
### Get payroll entries for jv

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_get_payroll_entries_for_journal_voucher`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Declared result** list.

**Explicit results** nested operand in the contract(nested operand in the contract).limit(page\_len).offset(start).run().

**Local steps**

- Set PayrollEntry from Platform.qb.DocType(“Payroll Entry”).
- Set JournalEntryAccount from Platform.qb.DocType(“Journal Entry Account”).
- Set linked\_entries from nested operand in the contract.qb.from\_(JournalEntryAccount).select(JournalEntryAccount.reference\_name).where(JournalEntryAccount.reference\_type equals “Payroll Entry”).
- Return nested operand in the contract(nested operand in the contract).limit(page\_len).offset(start).run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0118.json#L3779) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L485) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L834)

<a id="op-9b3d09ca61de84"></a>
### Get employee list

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_get_employee_list`

**Inputs** filters, searchfield = no value, search\_string = no value, fields = no value, as\_dict = true, limit = no value, offset = no value, ignore\_match\_conditions = false.

**Declared result** list.

**Explicit results** list() · remove\_payrolled\_employees(employees\_to\_check, filters.start\_date, filters.end\_date).

**Local steps**

- Set sal\_struct from get\_salary\_structure(filters.company, filters.currency, filters.salary\_slip\_based\_on\_timesheet, filters.payroll\_frequency).
- If not sal\_struct.
  - Return list().
- Set emp\_list from get\_filtered\_employees(sal\_struct, filters, searchfield, search\_string, as\_dict = as\_dict, limit = limit, offset = offset, ignore\_match\_conditions = ignore\_match\_conditions, …).
- If as\_dict.
  - Set employees\_to\_check from mapping of emp.employee → emp for emp drawn from emp\_list.
    - Draw emp from emp\_list.
- Otherwise.
  - Set employees\_to\_check from mapping of emp at 0 → emp for emp drawn from emp\_list.
    - Draw emp from emp\_list.
- Return remove\_payrolled\_employees(employees\_to\_check, filters.start\_date, filters.end\_date).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0118.json#L4295) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L478) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L827)

<a id="op-62439e0a4f1312"></a>
### Employee query

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_employee_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Declared result** list.

**Explicit results** employee\_list.

**Explicit failure paths** validation helper — translated “Select Payroll Frequency.”.

**Local steps**

- Set filters from Platform.\_dict(filters).
- If not filters.payroll\_frequency.
  - Call the validation error handler Platform.throw(translated “Select Payroll Frequency.”).
- Set employee\_list from get\_employee\_list(filters, searchfield = searchfield, search\_string = txt, fields = list(“name”, “employee\_name”), as\_dict = false, …).
- Return employee\_list.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0118.json#L4717) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L477) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L826)

<a id="op-5dcd7c7e0ab060"></a>
### Get salary withholdings

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_get_salary_withholdings`

**Inputs** start\_date, end\_date, employee = no value, pluck = no value.

**Declared result** (list at str bitwise or list at dict).

**Explicit results** withheld\_salaries.run(pluck = pluck) · withheld\_salaries.run(as\_dict = true).

**Local steps**

- Set Withholding from Platform.qb.DocType(“Salary Withholding”).
- Set WithholdingCycle from Platform.qb.DocType(“Salary Withholding Cycle”).
- Set withheld\_salaries from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(Withholding.employee, Withholding.name.as\_(“salary ….
- If employee.
  - Set withheld\_salaries from withheld\_salaries.where(Withholding.employee equals employee).
- If pluck.
  - Return withheld\_salaries.run(pluck = pluck).
- Return withheld\_salaries.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0118.json#L5042) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L487) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L836)

<a id="op-7078b5f8cfdd46"></a>
### Get data

`operation_workforce_payroll_record_definitions_payroll_entry_payroll_entry_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “payroll\_entry”, “non\_standard\_fieldnames” → mapping(“Journal Entry” → “reference\_name”, “Payment Entry” → “reference\_name”), “transactions” → list(mapping(“items” → list(“Salary Slip ….

**Local steps**

- Return mapping(“fieldname” → “payroll\_entry”, “non\_standard\_fieldnames” → mapping(“Journal Entry” → “reference\_name”, “Payment Entry” → “reference\_name”), “transactions” → list(mapping(“items” → list(“Salary Slip ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0118.json#L5638) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L549) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L896)

## Record · Payroll period

[Record definition](../../../../data/record-types/payroll_period.json)

<a id="op-8386d690076b2d"></a>
### Payroll Period.validate

`operation_workforce_payroll_record_definitions_payroll_period_business_behavior_payroll_period_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_from\_to\_dates(“start\_date”, “end\_date”).
- Evaluate self.validate\_overlap().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overlap](operations-011.md#op-c71e8e87c4d2a7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L1554) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L593) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L940)

<a id="op-3f47d3a3138e55"></a>
### Payroll Period.clear cache

`operation_workforce_payroll_record_definitions_payroll_period_business_behavior_payroll_period_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Evaluate get\_payroll\_period.clear\_cache().
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L1643) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L592) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L939)

<a id="op-c71e8e87c4d2a7"></a>
### Payroll Period.validate overlap

`operation_workforce_payroll_record_definitions_payroll_period_business_behavior_payroll_period_validate_overlap`

**Inputs** self.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If not self.name.
  - Set self.name from (“New ” + self.doctype).
- Set DocType from Platform.qb.DocType(self.doctype).
- Set overlap\_doc from nested operand in the contract(nested operand in the contract).select(DocType.name).where(((nested operand in the contract.name differs from nested operand in the contract.name bitwise and nested operand i ….
- If overlap\_doc.
  - Set msg from ((translated “A {0} exists between {1} and {2} (”.format(self.doctype, formatdate(self.start\_date), formatdate(self.end\_date)) + formatted text  &lt;b&gt;&lt;a href="/app/Form/{self.doctype}/{overlap\_doc at 0.name} ….
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L1717) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L594) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L941)

<a id="op-24aa0e1d2b6ba3"></a>
### Get payroll period days

`operation_workforce_payroll_record_definitions_payroll_period_business_behavior_get_payroll_period_days`

**Inputs** start\_date, end\_date, employee, company = no value.

**Record and data access** read “Employee” via get\_value · read “Payroll Settings” via get\_single\_value.

**Explicit results** tuple(payroll\_period at 0 at 0, working\_days, actual\_no\_of\_days) · tuple(false, false, false).

**Local steps**

- If not company.
  - Set company from Platform.db.get\_value(“Employee”, employee, “company”).
- Set PayrollPeriod from Platform.qb.DocType(“Payroll Period”).
- Set payroll\_period from nested operand in the contract(nested operand in the contract).select(PayrollPeriod.name, PayrollPeriod.start\_date, PayrollPeriod.end\_date).where(((((nested operand in the contract bitwise and nested opera ….run().
- If len(payroll\_period) &gt; 0.
  - Set actual\_no\_of\_days from (date\_diff(getdate(payroll\_period at 0 at 2), getdate(payroll\_period at 0 at 1)) + 1).
  - Set working\_days from actual\_no\_of\_days.
  - If not cint(Platform.db.get\_single\_value(“Payroll Settings”, “include\_holidays\_in\_total\_working\_days”)).
    - Set holidays from get\_holiday\_dates\_for\_employee(employee, getdate(payroll\_period at 0 at 1), getdate(payroll\_period at 0 at 2)).
    - Update working\_days using − len(holidays).
  - Return tuple(payroll\_period at 0 at 0, working\_days, actual\_no\_of\_days).
- Return tuple(false, false, false).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Payroll Settings”, “include\_holidays\_in\_total\_working\_days”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L2366) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L590) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L937)

<a id="op-fed51fef10d781"></a>
### Get payroll period

`operation_workforce_payroll_record_definitions_payroll_period_business_behavior_get_payroll_period`

**Inputs** from\_date, to\_date, company.

**Wrappers, in declaration order** redis\_cache().

**Explicit results** payroll\_period at 0 when payroll\_period, otherwise no value.

**Local steps**

- Set PayrollPeriod from Platform.qb.DocType(“Payroll Period”).
- Set payroll\_period from nested operand in the contract(nested operand in the contract).select(PayrollPeriod.name, PayrollPeriod.start\_date, PayrollPeriod.end\_date).where(((nested operand in the contract.start\_date ≤ from\_date bit ….
- Return payroll\_period at 0 when payroll\_period, otherwise no value.
  - Value choice on payroll\_period — true gives payroll\_period at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L3104) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L589) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L936)

<a id="op-adcc09a703d471"></a>
### Get period factor

`operation_workforce_payroll_record_definitions_payroll_period_business_behavior_get_period_factor`

**Inputs** employee, start\_date, end\_date, payroll\_frequency, payroll\_period, depends\_on\_payment\_days = 0, joining\_date = no value, relieving\_date = no value.

**Record and data access** read “Employee” via get\_cached\_value.

**Explicit results** tuple(total\_sub\_periods, remaining\_sub\_periods).

**Local steps**

- Set tuple(period\_start, period\_end) from tuple(payroll\_period.start\_date, payroll\_period.end\_date).
- If (not joining\_date and not relieving\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not joining\_date → not relieving\_date.
  - Set tuple(joining\_date, relieving\_date) from Platform.get\_cached\_value(“Employee”, employee, list(“date\_of\_joining”, “relieving\_date”)).
- If getdate(joining\_date) &gt; getdate(period\_start).
  - Set period\_start from joining\_date.
- If (relieving\_date and getdate(relieving\_date) &lt; getdate(period\_end)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in relieving\_date → getdate(relieving\_date) &lt; getdate(period\_end).
  - Set period\_end from relieving\_date.
- Set tuple(total\_sub\_periods, remaining\_sub\_periods) from tuple(0.0, 0.0).
- If (payroll\_frequency equals “Monthly” and not depends\_on\_payment\_days).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in payroll\_frequency equals “Monthly” → not depends\_on\_payment\_days.
  - Set total\_sub\_periods from get\_exact\_month\_diff(payroll\_period.end\_date, payroll\_period.start\_date).
  - Set remaining\_sub\_periods from get\_exact\_month\_diff(period\_end, start\_date).
- Otherwise.
  - Set salary\_days from (date\_diff(end\_date, start\_date) + 1).
  - Set days\_in\_payroll\_period from (date\_diff(payroll\_period.end\_date, payroll\_period.start\_date) + 1).
  - Set total\_sub\_periods from (flt(days\_in\_payroll\_period) ÷ flt(salary\_days)).
  - Set remaining\_days\_in\_payroll\_period from (date\_diff(period\_end, start\_date) + 1).
  - Set remaining\_sub\_periods from (flt(remaining\_days\_in\_payroll\_period) ÷ flt(salary\_days)).
- Return tuple(total\_sub\_periods, remaining\_sub\_periods).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Employee”, employee, list(“date\_of\_joining”, “relieving\_date”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L3398) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L591) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L938)

<a id="op-d57fc02850cfc4"></a>
### Get data

`operation_workforce_payroll_record_definitions_payroll_period_payroll_period_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “payroll\_period”, “transactions” → list(mapping(“items” → list(“Employee Tax Exemption Proof Submission”, “Employee Tax Exemption Declaration”)))).

**Local steps**

- Return mapping(“fieldname” → “payroll\_period”, “transactions” → list(mapping(“items” → list(“Employee Tax Exemption Proof Submission”, “Employee Tax Exemption Declaration”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L4122) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L595) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L942)

## Record · Payroll settings

[Record definition](../../../../data/record-types/payroll_settings.json)

<a id="op-926d3e51f37d11"></a>
### Payroll Settings.validate

`operation_workforce_payroll_record_definitions_payroll_settings_business_behavior_payroll_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_password\_policy().
- If not self.daily\_wages\_fraction\_for\_half\_day.
  - Set self.daily\_wages\_fraction\_for\_half\_day from 0.5.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate password policy](operations-011.md#op-d9f3c271600cf0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L4225) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L598) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L945)

<a id="op-d9f3c271600cf0"></a>
### Payroll Settings.validate password policy

`operation_workforce_payroll_record_definitions_payroll_settings_business_behavior_payroll_settings_validate_password_policy`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L4311) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L599) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L946)

<a id="op-e6dfd94ff772c1"></a>
### Payroll Settings.on update

`operation_workforce_payroll_record_definitions_payroll_settings_business_behavior_payroll_settings_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.toggle\_rounded\_total().
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [toggle rounded total](operations-011.md#op-39cf634730411f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L4427) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L596) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L943)

<a id="op-39cf634730411f"></a>
### Payroll Settings.toggle rounded total

`operation_workforce_payroll_record_definitions_payroll_settings_business_behavior_payroll_settings_toggle_rounded_total`

**Inputs** self.

**Local steps**

- Set self.disable\_rounded\_total from cint(self.disable\_rounded\_total).
- Evaluate make\_property\_setter(“Salary Slip”, “rounded\_total”, “hidden”, self.disable\_rounded\_total, validate\_fields\_for\_doctype = false, …).
- Evaluate make\_property\_setter(“Salary Slip”, “rounded\_total”, “print\_hide”, self.disable\_rounded\_total, validate\_fields\_for\_doctype = false, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L4497) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L597) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L944)

## Record · Retention bonus

[Record definition](../../../../data/record-types/retention_bonus.json)

<a id="op-e4e8934d7fd619"></a>
### Retention Bonus.validate

`operation_workforce_payroll_record_definitions_retention_bonus_business_behavior_retention_bonus_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Bonus Payment Date cannot be a past date”.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- If getdate(self.bonus\_payment\_date) &lt; getdate().
  - Call the validation error handler Platform.throw(translated “Bonus Payment Date cannot be a past date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L4696) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L603) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L950)

<a id="op-cae254ee6a0851"></a>
### Retention Bonus.on submit

`operation_workforce_payroll_record_definitions_retention_bonus_business_behavior_retention_bonus_on_submit`

**Inputs** self.

**Record and data access** read “Employee” via get\_value · read “Additional Salary” via get\_value.

**State and service calls** request new\_doc for “Additional Salary” · call submit on additional\_salary · request set\_value on “Additional Salary” · call db\_set on self.

**Local steps**

- Set company from Platform.db.get\_value(“Employee”, self.employee, “company”).
- Set additional\_salary from self.get\_additional\_salary().
- If not additional\_salary.
  - Set additional\_salary from Platform.new\_doc(“Additional Salary”).
  - Set additional\_salary.employee from self.employee.
  - Set additional\_salary.salary\_component from self.salary\_component.
  - Set additional\_salary.amount from self.bonus\_amount.
  - Set additional\_salary.payroll\_date from self.bonus\_payment\_date.
  - Set additional\_salary.company from company.
  - Set additional\_salary.overwrite\_salary\_structure\_amount from 0.
  - Set additional\_salary.ref\_doctype from self.doctype.
  - Set additional\_salary.ref\_docname from self.name.
  - Evaluate additional\_salary.submit().
- Otherwise.
  - Set bonus\_added from (Platform.db.get\_value(“Additional Salary”, additional\_salary, “amount”) + self.bonus\_amount).
  - Evaluate Platform.db.set\_value(“Additional Salary”, additional\_salary, “amount”, bonus\_added).
  - Evaluate self.db\_set(“additional\_salary”, additional\_salary).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get additional salary](operations-011.md#op-ab84779effe94f).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L4839) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L602) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L949)

<a id="op-54c7f312e2bf76"></a>
### Retention Bonus.on cancel

`operation_workforce_payroll_record_definitions_retention_bonus_business_behavior_retention_bonus_on_cancel`

**Inputs** self.

**Record and data access** read “Additional Salary” via get\_value · resolve a document from “Additional Salary” via get\_doc.

**State and service calls** call cancel on Platform.get\_doc(“Additional Salary”, additional\_salary) · request set\_value on “Additional Salary”.

**Local steps**

- Set additional\_salary from self.get\_additional\_salary().
- If additional\_salary.
  - Set bonus\_removed from (Platform.db.get\_value(“Additional Salary”, additional\_salary, “amount”) − self.bonus\_amount).
  - If bonus\_removed equals 0.
    - Evaluate Platform.get\_doc(“Additional Salary”, additional\_salary).cancel().
  - Otherwise.
    - Evaluate Platform.db.set\_value(“Additional Salary”, additional\_salary, “amount”, bonus\_removed).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get additional salary](operations-011.md#op-ab84779effe94f).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L5324) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L601) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L948)

<a id="op-ab84779effe94f"></a>
### Retention Bonus.get additional salary

`operation_workforce_payroll_record_definitions_retention_bonus_business_behavior_retention_bonus_get_additional_salary`

**Inputs** self.

**Record and data access** read “Additional Salary” via exists.

**Explicit results** Platform.db.exists(“Additional Salary”, mapping(“employee” → self.employee, “salary\_component” → self.salary\_component, “payroll\_date” → self.bonus\_payment\_date, “company” → self.company, …)).

**Local steps**

- Return Platform.db.exists(“Additional Salary”, mapping(“employee” → self.employee, “salary\_component” → self.salary\_component, “payroll\_date” → self.bonus\_payment\_date, “company” → self.company, …)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L5570) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L600) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L947)

## Service · Retention bonus

<a id="op-a5a30579b402cb"></a>
### Get context

`operation_workforce_payroll_notification_retention_bonus_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L6860) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L312) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L661)
