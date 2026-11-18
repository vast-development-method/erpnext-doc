# Payroll and benefits · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Salary slip

[Record definition](../../../../data/record-types/salary_slip.json)

<a id="op-89eddf3d9f1c8a"></a>
### Salary Slip.get tax paid in period

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_tax_paid_in_period`

**Inputs** self, start\_date, end\_date, tax\_component.

**Explicit results** (total\_tax\_paid + tax\_deducted\_till\_date).

**Local steps**

- Set total\_tax\_paid from self.get\_salary\_slip\_details(start\_date, end\_date, parentfield = “deductions”, salary\_component = tax\_component, variable\_based\_on\_taxable\_salary = 1).
- Set tax\_deducted\_till\_date from self.get\_opening\_for(“tax\_deducted\_till\_date”, start\_date, end\_date).
- Return (total\_tax\_paid + tax\_deducted\_till\_date).

**Methods declared on this owner** [get salary slip details](operations-016.md#op-3d9b68950fbac3), [get opening for](operations-016.md#op-0c89b467a31afe).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L3940) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L697) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1044)

<a id="op-c7b06c93ae9232"></a>
### Salary Slip.get taxable earnings

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_taxable_earnings`

**Inputs** self, allow\_tax\_exemption = false, based\_on\_payment\_days = 0.

**Explicit results** Platform.\_dict(mapping(“taxable\_earnings” → taxable\_earnings, “additional\_income” → additional\_income, “amount\_exempted\_from\_income\_tax” → amount\_exempted\_from\_income\_tax, “additional\_income\_with\_full\_tax” ….

**Local steps**

- Set taxable\_earnings from 0.
- Set additional\_income from 0.
- Set additional\_income\_with\_full\_tax from 0.
- Set amount\_exempted\_from\_income\_tax from 0.
- For each earning in self.earnings.
  - If based\_on\_payment\_days.
    - Set tuple(amount, additional\_amount) from self.get\_amount\_based\_on\_payment\_days(earning).
  - Otherwise.
    - If earning.additional\_amount.
      - Set tuple(amount, additional\_amount) from tuple((earning.amount or 0), (earning.additional\_amount or 0)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in earning.amount → 0.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in earning.additional\_amount → 0.
    - Otherwise.
      - Set tuple(amount, additional\_amount) from tuple((earning.default\_amount or 0), (earning.additional\_amount or 0)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in earning.default\_amount → 0.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in earning.additional\_amount → 0.
  - If earning.is\_tax\_applicable.
    - Update taxable\_earnings using + (amount − additional\_amount).
    - Update additional\_income using + additional\_amount.
    - If (additional\_amount and earning.is\_recurring\_additional\_salary).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in additional\_amount → earning.is\_recurring\_additional\_salary.
      - Update additional\_income using + self.get\_future\_recurring\_additional\_amount(earning.additional\_salary, earning.additional\_amount).
    - If earning.deduct\_full\_tax\_on\_selected\_payroll\_date.
      - Update additional\_income\_with\_full\_tax using + additional\_amount.
- If allow\_tax\_exemption.
  - For each ded in self.deductions.
    - If ded.exempted\_from\_income\_tax.
      - Set tuple(amount, additional\_amount) from tuple(ded.amount, ded.additional\_amount).
      - If based\_on\_payment\_days.
        - Set tuple(amount, additional\_amount) from self.get\_amount\_based\_on\_payment\_days(ded).
      - Update taxable\_earnings using − flt((amount − additional\_amount)).
      - Update additional\_income using − additional\_amount.
      - Update amount\_exempted\_from\_income\_tax using + flt((amount − additional\_amount)).
      - If (additional\_amount and ded.is\_recurring\_additional\_salary).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in additional\_amount → ded.is\_recurring\_additional\_salary.
        - Update additional\_income using − self.get\_future\_recurring\_additional\_amount(ded.additional\_salary, ded.additional\_amount).
- Return Platform.\_dict(mapping(“taxable\_earnings” → taxable\_earnings, “additional\_income” → additional\_income, “amount\_exempted\_from\_income\_tax” → amount\_exempted\_from\_income\_tax, “additional\_income\_with\_full\_tax” ….

**Methods declared on this owner** [get amount based on payment days](operations-017.md#op-c455f878229abb), [get future recurring additional amount](operations-017.md#op-fd3cf4e32e8d90).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L4122) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L698) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1045)

<a id="op-291fe23009cf59"></a>
### Salary Slip.get future recurring period

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_future_recurring_period`

**Inputs** self, additional\_salary.

**Record and data access** read “Additional Salary” via get\_value.

**Explicit results** future\_recurring\_period.

**Local steps**

- Set to\_date from no value.
- If self.relieving\_date.
  - Set to\_date from self.relieving\_date.
- If not to\_date.
  - Set to\_date from Platform.db.get\_value(“Additional Salary”, additional\_salary, “to\_date”, cache = true).
- Set tuple(from\_date, to\_date) from tuple(getdate(self.start\_date), getdate(to\_date)).
- If getdate(to\_date) &gt; getdate(self.payroll\_period.end\_date).
  - Set to\_date from getdate(self.payroll\_period.end\_date).
- Set future\_recurring\_period from (((to\_date.year − from\_date.year) × 12) + (to\_date.month − from\_date.month)).
- If (future\_recurring\_period &gt; 0 and to\_date.month equals from\_date.month).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in future\_recurring\_period &gt; 0 → to\_date.month equals from\_date.month.
  - Update future\_recurring\_period using − 1.
- Return future\_recurring\_period.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L4908) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L680) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1027)

<a id="op-fd3cf4e32e8d90"></a>
### Salary Slip.get future recurring additional amount

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_future_recurring_additional_amount`

**Inputs** self, additional\_salary, monthly\_additional\_amount.

**Explicit results** future\_recurring\_additional\_amount.

**Local steps**

- Set future\_recurring\_additional\_amount from 0.
- Set future\_recurring\_period from self.get\_future\_recurring\_period(additional\_salary).
- If future\_recurring\_period &gt; 0.
  - Set future\_recurring\_additional\_amount from (monthly\_additional\_amount × future\_recurring\_period).
- Return future\_recurring\_additional\_amount.

**Methods declared on this owner** [get future recurring period](operations-017.md#op-291fe23009cf59).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L5349) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L679) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1026)

<a id="op-c455f878229abb"></a>
### Salary Slip.get amount based on payment days

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_amount_based_on_payment_days`

**Inputs** self, row.

**Record and data access** read “Salary Component” via get\_value.

**Explicit results** tuple(amount, additional\_amount).

**Local steps**

- Set tuple(amount, additional\_amount) from tuple(row.amount, row.additional\_amount).
- Set timesheet\_component from getattr(self, “\_timesheet\_component”, no value).
- If (not row.additional\_salary and not row.default\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.additional\_salary → not row.default\_amount.
  - Set tuple(amount, additional\_amount) from tuple(amount, additional\_amount).
- Otherwise.
  - If (self.salary\_structure and cint(row.depends\_on\_payment\_days) and cint(self.total\_working\_days) and not (row.additional\_salary and row.default\_amount) and (row.salary\_component differs from timesheet\_compon ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.salary\_structure → cint(row.depends\_on\_payment\_days) → cint(self.total\_working\_days) → not (row.additional\_salary and row.default\_amount) → (row.salary\_component differs from timesheet\_component or getdate(self.start\_date) &lt; self.joining\_date or (self.relieving\_date and getdate(self.end\_date) &gt; self.relieving\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.additional\_salary → row.default\_amount.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.salary\_component differs from timesheet\_component → getdate(self.start\_date) &lt; self.joining\_date → (self.relieving\_date and getdate(self.end\_date) &gt; self.relieving\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.relieving\_date → getdate(self.end\_date) &gt; self.relieving\_date.
    - Set additional\_amount from flt(((flt(row.additional\_amount) × flt(self.payment\_days)) ÷ cint(self.total\_working\_days)), row.precision(“additional\_amount”)).
    - Set amount from (flt(((flt(row.default\_amount) × flt(self.payment\_days)) ÷ cint(self.total\_working\_days)), row.precision(“amount”)) + additional\_amount).
  - Otherwise.
    - If (not self.payment\_days and row.salary\_component differs from timesheet\_component and cint(row.depends\_on\_payment\_days)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.payment\_days → row.salary\_component differs from timesheet\_component → cint(row.depends\_on\_payment\_days).
      - Set tuple(amount, additional\_amount) from tuple(0, 0).
    - Otherwise.
      - If (not row.amount and row.additional\_amount and not (row.additional\_salary and row.default\_amount)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.amount → row.additional\_amount → not (row.additional\_salary and row.default\_amount).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.additional\_salary → row.default\_amount.
        - Set amount from flt(row.additional\_amount).
- If Platform.db.get\_value(“Salary Component”, row.salary\_component, “round\_to\_the\_nearest\_integer”, cache = true).
  - Set tuple(amount, additional\_amount) from tuple(rounded((amount or 0)), rounded((additional\_amount or 0))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in amount → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in additional\_amount → 0.
- Return tuple(amount, additional\_amount).

**Values supplied outside this operation** selected callable from getattr(self, “\_timesheet\_component”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L109) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L664) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1011)

<a id="op-84d5996f112623"></a>
### Salary Slip.get total exemption amount

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_total_exemption_amount`

**Inputs** self.

**Record and data access** read “Employee Tax Exemption Proof Submission” via get\_value · read “Employee Tax Exemption Declaration” via get\_value.

**Explicit results** total\_exemption\_amount.

**Local steps**

- Set total\_exemption\_amount from 0.
- If self.tax\_slab.allow\_tax\_exemption.
  - If self.deduct\_tax\_for\_unsubmitted\_tax\_exemption\_proof.
    - Set exemption\_proof from Platform.db.get\_value(“Employee Tax Exemption Proof Submission”, mapping(“employee” → self.employee, “payroll\_period” → self.payroll\_period.name, “docstatus” → 1), “exemption\_amount”, cache = true).
    - If exemption\_proof.
      - Set total\_exemption\_amount from exemption\_proof.
  - Otherwise.
    - Set declaration from Platform.db.get\_value(“Employee Tax Exemption Declaration”, mapping(“employee” → self.employee, “payroll\_period” → self.payroll\_period.name, “docstatus” → 1), “total\_exemption\_amount”, cache = true).
    - If declaration.
      - Set total\_exemption\_amount from declaration.
- If self.tax\_slab.standard\_tax\_exemption\_amount.
  - Update total\_exemption\_amount using + flt(self.tax\_slab.standard\_tax\_exemption\_amount).
- Return total\_exemption\_amount.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L6416) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L700) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1047)

<a id="op-ec782c8e4c4a47"></a>
### Salary Slip.get income form other sources

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_income_form_other_sources`

**Inputs** self.

**Record and data access** read “Employee Other Income” via get\_all.

**Explicit results** (Platform.get\_all(“Employee Other Income”, filters = mapping(“employee” → self.employee, “payroll\_period” → nested operand in the contract.payroll\_period.name, “company” → self.company, “docstatus” → 1), f ….

**Local steps**

- Return (Platform.get\_all(“Employee Other Income”, filters = mapping(“employee” → self.employee, “payroll\_period” → nested operand in the contract.payroll\_period.name, “company” → self.company, “docstatus” → 1), f ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“Employee Other Income”, filters = mapping(“employee” → self.employee, “payroll\_period” → self.payroll\_period.name, “company” → self.company, “docstatus” → 1), fields = list(mapping(“SUM”  … → 0.0.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L6843) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L683) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1030)

<a id="op-d6ac3135008503"></a>
### Salary Slip.get component totals

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_component_totals`

**Inputs** self, component\_type, depends\_on\_payment\_days = 0.

**Explicit results** total.

**Local steps**

- Set total from 0.0.
- Set components from (self.get(component\_type) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(component\_type) → list().
- For each d in components.
  - If d.do\_not\_include\_in\_total.
    - Continue with the next iteration or loop test.
  - If depends\_on\_payment\_days.
    - Set amount from self.get\_amount\_based\_on\_payment\_days(d) at 0.
  - Otherwise.
    - Set amount from flt(d.amount, d.precision(“amount”)).
  - Update total using + amount.
- Return total.

**Methods declared on this owner** [get amount based on payment days](operations-017.md#op-c455f878229abb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L7065) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L669) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1016)

<a id="op-3dffbd2a7878ed"></a>
### Salary Slip.email salary slip

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_email_salary_slip`

**Inputs** self.

**Record and data access** read “Employee” via get\_value · read “Payroll Settings” via get\_single · resolve a document from “Email Template” via get\_doc.

**State and service calls** sendmail.

**Local steps**

- Set receiver from Platform.db.get\_value(“Employee”, self.employee, “prefered\_email”, cache = true).
- Set payroll\_settings from Platform.get\_single(“Payroll Settings”).
- Set subject from formatted text Salary Slip - from {self.start\_date} to {self.end\_date}.
- Set message from translated “Please see attachment”.
- If payroll\_settings.email\_template.
  - Set email\_template from Platform.get\_doc(“Email Template”, payroll\_settings.email\_template).
  - Set context from self.as\_dict().
  - Set subject from Platform.render\_template(email\_template.subject, context).
  - Set message from Platform.render\_template(email\_template.response, context).
- Set password from no value.
- If payroll\_settings.encrypt\_salary\_slips\_in\_emails.
  - Set password from generate\_password\_for\_pdf(payroll\_settings.password\_policy, self.employee).
  - If not payroll\_settings.email\_template.
    - Update message using + (text in the contract + translated “Note: Your salary slip is password protected, the password to unlock the PDF is of the format {0}.”.format(payroll\_settings.password\_policy)).
- If receiver.
  - Set posting\_date from getdate(self.posting\_date).
  - Set email\_args from mapping(“sender” → payroll\_settings.sender\_email, “recipients” → list(receiver), “message” → message, “subject” → subject, …).
    - Value choice on posting\_date &gt; getdate() — true gives posting\_date, false gives no value.
  - If not Platform.flags.in\_test.
    - Evaluate enqueue(method = Platform.sendmail, queue = “short”, timeout = 300, is\_async = true, …).
  - Otherwise.
    - Evaluate Platform.sendmail(expanded names email\_args).
- Otherwise.
  - Evaluate msgprint(translated “{0}: Employee email not found, hence email not sent”.format(self.employee\_name)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from enqueue(method = Platform.sendmail, queue = “short”, timeout = 300, is\_async = true, …), Platform.sendmail(expanded names email\_args).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L661) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1008)

<a id="op-36eafe6a75c344"></a>
### Salary Slip.update status

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_update_status`

**Inputs** self, salary\_slip = no value.

**Record and data access** resolve a document from “Timesheet” via get\_doc.

**State and service calls** call save on timesheet.

**Local steps**

- For each data in self.timesheets.
  - If data.time\_sheet.
    - Set timesheet from Platform.get\_doc(“Timesheet”, data.time\_sheet).
    - Set timesheet.salary\_slip from salary\_slip.
    - Set timesheet.flags.ignore\_validate\_update\_after\_submit from true.
    - Evaluate timesheet.set\_status().
    - Evaluate timesheet.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L974) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L732) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1079)

<a id="op-8f7c324ed09168"></a>
### Salary Slip.set status

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_set_status`

**Inputs** self, status = no value.

**State and service calls** call db\_set on self.

**Local steps**

- If not status.
  - Set status from self.get\_status().
- Evaluate self.db\_set(“status”, status).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get status](operations-014.md#op-c997b531df6d34).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L1164) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L726) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1073)

<a id="op-051ff5d285e426"></a>
### Salary Slip.process salary structure

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_process_salary_structure`

**Inputs** self, for\_preview = 0, lwp\_days\_corrected = no value.

**Local steps**

- If self.payroll\_frequency.
  - Evaluate self.get\_date\_details().
- Evaluate self.pull\_emp\_details().
- Evaluate self.get\_working\_days\_details(for\_preview = for\_preview, lwp\_days\_corrected = lwp\_days\_corrected).
- Evaluate self.calculate\_net\_pay().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get date details](operations-014.md#op-2218a2becf449f), [pull emp details](operations-017.md#op-dc86bc42f0a1c1), [get working days details](operations-014.md#op-263c6d91c048e3), [calculate net pay](operations-015.md#op-856a3df225339e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L1278) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L716) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1063)

<a id="op-dc86bc42f0a1c1"></a>
### Salary Slip.pull emp details

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_pull_employee_details`

**Inputs** self.

**Record and data access** read “Employee” via get\_cached\_value.

**Local steps**

- Set account\_details from Platform.get\_cached\_value(“Employee”, self.employee, list(“bank\_name”, “bank\_ac\_no”, “salary\_mode”), as\_dict = 1).
- If account\_details.
  - Set self.mode\_of\_payment from account\_details.salary\_mode.
  - Set self.bank\_name from account\_details.bank\_name.
  - Set self.bank\_account\_no from account\_details.bank\_ac\_no.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Employee”, self.employee, list(“bank\_name”, “bank\_ac\_no”, “salary\_mode”), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L1445) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L718) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1065)

<a id="op-c2374cf8b5a900"></a>
### Salary Slip.process salary based on working days

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_process_salary_based_on_working_days`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Local steps**

- Evaluate self.get\_working\_days\_details(lwp = self.leave\_without\_pay).
- Evaluate self.calculate\_net\_pay().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get working days details](operations-014.md#op-263c6d91c048e3), [calculate net pay](operations-015.md#op-856a3df225339e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L1635) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L715) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1062)

<a id="op-5c5f6d3df7b2e6"></a>
### Salary Slip.set totals

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_set_totals`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Local steps**

- Set self.gross\_pay from 0.0.
- If self.salary\_slip\_based\_on\_timesheet equals 1.
  - Evaluate self.calculate\_total\_for\_salary\_slip\_based\_on\_timesheet().
- Otherwise.
  - Set self.total\_deduction from 0.0.
  - If hasattr(self, “earnings”).
    - For each earning in self.earnings.
      - Update self.gross\_pay using + flt(earning.amount, earning.precision(“amount”)).
  - If hasattr(self, “deductions”).
    - For each deduction in self.deductions.
      - Update self.total\_deduction using + flt(deduction.amount, deduction.precision(“amount”)).
  - Set self.net\_pay from ((flt(self.gross\_pay) − flt(self.total\_deduction)) − flt(self.get(“total\_loan\_repayment”))).
- Evaluate self.set\_base\_totals().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate total for salary slip based on timesheet](operations-017.md#op-43b23747c5c953), [set base totals](operations-017.md#op-4cd1f335a29d2a).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L1739) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L728) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1075)

<a id="op-4cd1f335a29d2a"></a>
### Salary Slip.set base totals

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_set_base_totals`

**Inputs** self.

**Local steps**

- Set self.base\_gross\_pay from (flt(self.gross\_pay) × flt(self.exchange\_rate)).
- Set self.base\_total\_deduction from (flt(self.total\_deduction) × flt(self.exchange\_rate)).
- Set self.rounded\_total from rounded((self.net\_pay or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.net\_pay → 0.
- Set self.base\_net\_pay from (flt(self.net\_pay) × flt(self.exchange\_rate)).
- Set self.base\_rounded\_total from rounded((self.base\_net\_pay or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.base\_net\_pay → 0.
- Evaluate self.set\_net\_total\_in\_words().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set net total in words](operations-013.md#op-4b67332a93dc41).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L2192) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L720) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1067)

<a id="op-43b23747c5c953"></a>
### Salary Slip.calculate total for salary slip based on timesheet

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_calculate_total_for_salary_slip_based_on_timesheet`

**Inputs** self.

**Record and data access** read “Salary Structure” via get\_value.

**Local steps**

- If self.timesheets.
  - Set self.total\_working\_hours from 0.
  - For each timesheet in self.timesheets.
    - If timesheet.working\_hours.
      - Update self.total\_working\_hours using + timesheet.working\_hours.
- Set wages\_amount from (self.total\_working\_hours × self.hour\_rate).
- Set self.base\_hour\_rate from (flt(self.hour\_rate) × flt(self.exchange\_rate)).
- Set salary\_component from Platform.db.get\_value(“Salary Structure”, mapping(“name” → self.salary\_structure), “salary\_component”, cache = true).
- If self.earnings.
  - For each tuple(i, earning) in enumerate(self.earnings).
    - If earning.salary\_component equals salary\_component.
      - Set self.earnings at i.amount from wages\_amount.
    - Update self.gross\_pay using + flt(self.earnings at i.amount, earning.precision(“amount”)).
- Set self.net\_pay from (flt(self.gross\_pay) − flt(self.total\_deduction)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L2499) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L644) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L991)

<a id="op-ddd10b7b50ae46"></a>
### Salary Slip.compute year to date

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_compute_year_to_date`

**Inputs** self.

**Record and data access** read “Salary Slip” via get\_list.

**Local steps**

- Set year\_to\_date from 0.
- Set tuple(period\_start\_date, period\_end\_date) from self.get\_year\_to\_date\_period().
- Set salary\_slip\_sum from Platform.get\_list(“Salary Slip”, fields = list(mapping(“SUM” → “net\_pay”, “as” → “net\_sum”), mapping(“SUM” → “gross\_pay”, “as” → “gross\_sum”)), filters = mapping(“employee” → self.employee, “start\_date” →  ….
- Set year\_to\_date from flt(salary\_slip\_sum at 0.net\_sum) when salary\_slip\_sum, otherwise 0.0.
  - Value choice on salary\_slip\_sum — true gives flt(salary\_slip\_sum at 0.net\_sum), false gives 0.0.
- Set gross\_year\_to\_date from flt(salary\_slip\_sum at 0.gross\_sum) when salary\_slip\_sum, otherwise 0.0.
  - Value choice on salary\_slip\_sum — true gives flt(salary\_slip\_sum at 0.gross\_sum), false gives 0.0.
- Update year\_to\_date using + self.net\_pay.
- Update gross\_year\_to\_date using + self.gross\_pay.
- Set self.year\_to\_date from year\_to\_date.
- Set self.gross\_year\_to\_date from gross\_year\_to\_date.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get year to date period](operations-017.md#op-181ade6a5d8565).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L3011) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L658) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1005)

<a id="op-bac9d09c6105a6"></a>
### Salary Slip.compute month to date

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_compute_month_to_date`

**Inputs** self.

**Record and data access** read “Salary Slip” via get\_list.

**Local steps**

- Set month\_to\_date from 0.
- Set first\_day\_of\_the\_month from get\_first\_day(self.start\_date).
- Set salary\_slip\_sum from Platform.get\_list(“Salary Slip”, fields = list(mapping(“SUM” → “net\_pay”, “as” → “sum”)), filters = mapping(“employee” → self.employee, “start\_date” → list(“&gt;=”, first\_day\_of\_the\_month), “end\_date” → list( ….
- Set month\_to\_date from flt(salary\_slip\_sum at 0.sum) when salary\_slip\_sum, otherwise 0.0.
  - Value choice on salary\_slip\_sum — true gives flt(salary\_slip\_sum at 0.sum), false gives 0.0.
- Update month\_to\_date using + self.net\_pay.
- Set self.month\_to\_date from month\_to\_date.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L3488) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L655) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1002)

<a id="op-fb72874bb69605"></a>
### Salary Slip.compute component wise year to date

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_compute_component_wise_year_to_date`

**Inputs** self.

**Local steps**

- Set tuple(period\_start\_date, period\_end\_date) from self.get\_year\_to\_date\_period().
- Set ss from Platform.qb.DocType(“Salary Slip”).
- Set sd from Platform.qb.DocType(“Salary Detail”).
- For each key in COMPONENT\_PARENTFIELDS.
  - For each component in self.get(key).
    - Set year\_to\_date from 0.
    - Set component\_sum from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“sum”)).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise ….run().
    - Set year\_to\_date from flt(component\_sum at 0 at 0) when component\_sum, otherwise 0.0.
      - Value choice on component\_sum — true gives flt(component\_sum at 0 at 0), false gives 0.0.
    - Update year\_to\_date using + component.amount.
    - Set component.year\_to\_date from year\_to\_date.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get year to date period](operations-017.md#op-181ade6a5d8565).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L3852) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L651) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L998)

<a id="op-181ade6a5d8565"></a>
### Salary Slip.get year to date period

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_year_to_date_period`

**Inputs** self.

**Explicit results** tuple(period\_start\_date, period\_end\_date).

**Local steps**

- If self.payroll\_period.
  - Set period\_start\_date from self.payroll\_period.start\_date.
  - Set period\_end\_date from self.payroll\_period.end\_date.
- Otherwise.
  - Set fiscal\_year from get\_fiscal\_year(date = self.start\_date, company = self.company, as\_dict = 1).
  - Set period\_start\_date from fiscal\_year.year\_start\_date.
  - Set period\_end\_date from fiscal\_year.year\_end\_date.
- Return tuple(period\_start\_date, period\_end\_date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L4452) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L703) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1050)

<a id="op-0f8dd95c526a69"></a>
### Salary Slip.add leave balances

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_add_leave_balances`

**Inputs** self.

**Record and data access** read “Payroll Settings” via get\_single\_value.

**Local steps**

- Evaluate self.set(“leave\_details”, list()).
- If Platform.db.get\_single\_value(“Payroll Settings”, “show\_leave\_balances\_in\_salary\_slip”).
  - Bind dependencies get\_leave\_details.
  - Set leave\_details from get\_leave\_details(self.employee, self.end\_date, true).
  - For each tuple(leave\_type, leave\_values) in leave\_details at “leave\_allocation”.items().
    - Evaluate self.append(“leave\_details”, mapping(“leave\_type” → leave\_type, “total\_allocated\_leaves” → flt(leave\_values.get(“total\_leaves”)), “expired\_leaves” → flt(leave\_values.get(“expired\_leaves”)), “used\_leaves” → ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Payroll Settings”, “show\_leave\_balances\_in\_salary\_slip”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L4651) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L632) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L979)

<a id="op-c714bd340be9c4"></a>
### Salary Slip.on discard

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L5122) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L710) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1057)

<a id="op-af6f845ece6420"></a>
### Get benefits details parent

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_get_benefits_details_parent`

**Inputs** employee, payroll\_period, salary\_structure\_assignment.

**Record and data access** read “Payroll Settings” via get\_single\_value · read “Employee Benefit Application” via get\_value.

**Explicit results** tuple(benefit\_details\_parent, benefit\_details\_doctype).

**Local steps**

- Set mandatory\_benefit\_application from Platform.db.get\_single\_value(“Payroll Settings”, “mandatory\_benefit\_application”).
- Set benefit\_details\_parent from no value.
- Set benefit\_details\_doctype from no value.
- Set employee\_benefit\_application from Platform.db.get\_value(“Employee Benefit Application”, mapping(“employee” → employee, “payroll\_period” → payroll\_period, “docstatus” → 1), “name”).
- If mandatory\_benefit\_application.
  - If employee\_benefit\_application.
    - Set benefit\_details\_parent from employee\_benefit\_application.
    - Set benefit\_details\_doctype from “Employee Benefit Application Detail”.
- Otherwise.
  - If employee\_benefit\_application.
    - Set benefit\_details\_parent from employee\_benefit\_application.
    - Set benefit\_details\_doctype from “Employee Benefit Application Detail”.
  - Otherwise.
    - Set benefit\_details\_parent from salary\_structure\_assignment.
    - Set benefit\_details\_doctype from “Employee Benefit Detail”.
- Return tuple(benefit\_details\_parent, benefit\_details\_doctype).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Payroll Settings”, “mandatory\_benefit\_application”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0128.json#L5185) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L620) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L967)
