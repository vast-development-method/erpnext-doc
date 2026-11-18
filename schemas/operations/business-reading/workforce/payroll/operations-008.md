# Payroll and benefits · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payroll correction

[Record definition](../../../../data/record-types/payroll_correction.json)

<a id="op-6e39fee754a4f5"></a>
### Payroll Correction.fetch salary slip details

`operation_workforce_payroll_record_definitions_payroll_correction_business_behavior_payroll_correction_fetch_salary_slip_details`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (dict at tuple(str, list) bitwise or no value).

**Record and data access** read “Salary Slip” via get\_all.

**State and service calls** msgprint with translated “No Salary Slips with {0} found for employee {1} for payroll period {2}.”.format(Platform.bold(“Leave Without Pay”), self.employee, self.payroll\_period).

**Explicit results** mapping(“months” → list(), “slip\_details” → list()) · no value · mapping(“months” → sorted\_months, “slip\_details” → slip\_details).

**Local steps**

- If not (self.employee and self.payroll\_period and self.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.employee → self.payroll\_period → self.company.
  - Return mapping(“months” → list(), “slip\_details” → list()).
- Set slips from Platform.get\_all(“Salary Slip”, filters = mapping(“employee” → self.employee, “docstatus” → 1, “current\_payroll\_period” → self.payroll\_period, “company” → self.company, …), fields = list(“name”, “payment\_d ….
- If not slips.
  - Evaluate Platform.msgprint(translated “No Salary Slips with {0} found for employee {1} for payroll period {2}.”.format(Platform.bold(“Leave Without Pay”), self.employee, self.payroll\_period)).
  - Return no value.
- Set slip\_details from list().
- Set month\_set from set().
- For each slip in slips.
  - Set start\_date from slip.get(“start\_date”).
  - Set month\_name from calendar.month\_name at start\_date.month.
  - Evaluate month\_set.add(month\_name).
  - Evaluate slip\_details.append(mapping(“salary\_slip\_reference” → slip.get(“name”), “absent\_days” → slip.get(“absent\_days”), “leave\_without\_pay” → slip.get(“leave\_without\_pay”), “month\_name” → month\_name, …)).
- Set sorted\_months from sorted(list(month\_set)).
- Return mapping(“months” → sorted\_months, “slip\_details” → slip\_details).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L6147) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L467) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L816)

<a id="op-c472e95b2bcbd3"></a>
### Payroll Correction.populate breakup table

`operation_workforce_payroll_record_definitions_payroll_correction_business_behavior_payroll_correction_populate_breakup_table`

**Inputs** self.

**Record and data access** resolve a document from “Salary Slip” via get\_doc · read “System Settings” via get\_single\_value · read “Salary Component” via get\_list.

**State and service calls** msgprint with translated “No arrear components found in the salary slip. Ensure Arrear Component is checked in the Salary Component master.”.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Salary Slip not found.” · validation helper — translated “Cannot calculate payroll correction for salary component {0} because salary slip {1} has zero {2}.”.format(Platform.bold(component), Platform.bold(salary\_slip.name), translated “payment days” w ….

**Local steps**

- Set salary\_slip from Platform.get\_doc(“Salary Slip”, self.salary\_slip\_reference).
- Set precision from (salary\_slip.precision(“gross\_pay”) or Platform.db.get\_single\_value(“System Settings”, “currency\_precision”) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in salary\_slip.precision(“gross\_pay”) → Platform.db.get\_single\_value(“System Settings”, “currency\_precision”) → 2.
- If not salary\_slip.
  - Call the validation error handler Platform.throw(translated “Salary Slip not found.”).
- Evaluate self.set(“earning\_arrears”, list()).
- Evaluate self.set(“deduction\_arrears”, list()).
- Evaluate self.set(“accrual\_arrears”, list()).
- Set salary\_slip\_components from mapping().
- Set arrear\_components from list().
- For each section in list(“earnings”, “deductions”).
  - For each item in getattr(salary\_slip, section, list()).
    - If not item.additional\_salary.
      - Set salary\_slip\_components at item.salary\_component from mapping(“default\_amount” → (item.default\_amount or 0), “section” → “earning\_arrears” when section equals “earnings”, otherwise “deduction\_arrears”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.default\_amount → 0.
        - Value choice on section equals “earnings” — true gives “earning\_arrears”, false gives “deduction\_arrears”.
- For each item in getattr(salary\_slip, “accrued\_benefits”, list()).
  - Set salary\_slip\_components at item.salary\_component from mapping(“default\_amount” → (item.amount or 0), “section” → “accrual\_arrears”, “accrual\_component” → true).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.amount → 0.
- If salary\_slip\_components.
  - Set arrear\_components from Platform.db.get\_list(“Salary Component”, filters = mapping(“arrear\_component” → 1, “name” → list(“in”, salary\_slip\_components.keys()), “variable\_based\_on\_taxable\_salary” → 0, “disabled” → 0), fields = list ….
- If not arrear\_components.
  - Evaluate Platform.msgprint(translated “No arrear components found in the salary slip. Ensure Arrear Component is checked in the Salary Component master.”).
  - Return no value.
- For each component in arrear\_components.
  - Set component\_data from salary\_slip\_components at component.
  - If component\_data.get(“accrual\_component”).
    - Set total\_working\_days from salary\_slip.get(“payment\_days”, 1).
  - Otherwise.
    - Set total\_working\_days from salary\_slip.get(“total\_working\_days”, 1).
  - If not total\_working\_days.
    - Call the validation error handler Platform.throw(translated “Cannot calculate payroll correction for salary component {0} because salary slip {1} has zero {2}.”.format(Platform.bold(component), Platform.bold(salary\_slip.name), translated “ ….
      - Value choice on component\_data.get(“accrual\_component”) — true gives translated “payment days”, false gives translated “working days”.
  - Set per\_day\_amount from flt((component\_data at “default\_amount” ÷ total\_working\_days)).
  - Set arrear\_amount from flt((per\_day\_amount × self.days\_to\_reverse)).
  - Evaluate self.append(component\_data at “section”, mapping(“salary\_component” → component, “amount” → flt(arrear\_amount, precision))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “currency\_precision”) · selected callable from getattr(salary\_slip, section, list()), getattr(salary\_slip, “accrued\_benefits”, list()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L470) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L819)

<a id="op-c6e967025a655d"></a>
### Payroll Correction.validate arrear details

`operation_workforce_payroll_record_definitions_payroll_correction_business_behavior_payroll_correction_validate_arrear_details`

**Inputs** self.

**Explicit failure paths** validation helper — translated “No arrear details found”.

**Local steps**

- If not (self.earning\_arrears or self.deduction\_arrears or self.accrual\_arrears).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.earning\_arrears → self.deduction\_arrears → self.accrual\_arrears.
  - Call the validation error handler Platform.throw(translated “No arrear details found”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L1364) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L472) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L821)

<a id="op-ac32a88048b07c"></a>
### Payroll Correction.create additional salary

`operation_workforce_payroll_record_definitions_payroll_correction_business_behavior_payroll_correction_create_additional_salary`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Additional Salary”, “employee” → self.employee, “company” → self.company, “payroll\_date” → self.payroll\_date, …) via get\_doc.

**State and service calls** call insert on additional\_salary · call submit on additional\_salary.

**Local steps**

- For each component in ((self.earning\_arrears or list()) + (self.deduction\_arrears or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.earning\_arrears → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.deduction\_arrears → list().
  - Set additional\_salary from Platform.get\_doc(mapping(“doctype” → “Additional Salary”, “employee” → self.employee, “company” → self.company, “payroll\_date” → self.payroll\_date, …)).
  - Evaluate additional\_salary.insert().
  - Evaluate additional\_salary.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L1474) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L465) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L814)

<a id="op-947f0339b89212"></a>
### Payroll Correction.create benefit ledger entry

`operation_workforce_payroll_record_definitions_payroll_correction_business_behavior_payroll_correction_create_benefit_ledger_entry`

**Inputs** self.

**Record and data access** read “Salary Component” via get\_value · resolve a document from mapping(“doctype” → “Employee Benefit Ledger”, “employee” → self.employee, “employee\_name” → self.employee\_name, “company” → self.company, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Employee Benefit Ledger”, “employee” → self.employee, “employee\_name” → self.employee\_name, “company” → self.company, …)).

**Local steps**

- For each component in (self.accrual\_arrears or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.accrual\_arrears → list().
  - If (not component.salary\_component or not component.amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not component.salary\_component → not component.amount.
    - Continue with the next iteration or loop test.
  - Set is\_flexible\_benefit from Platform.db.get\_value(“Salary Component”, component.salary\_component, “is\_flexible\_benefit”).
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Employee Benefit Ledger”, “employee” → self.employee, “employee\_name” → self.employee\_name, “company” → self.company, …)).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L1822) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L466) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L815)

## Record · Payroll entry

[Record definition](../../../../data/record-types/payroll_entry.json)

<a id="op-6da453d4aa0f37"></a>
### Payroll Entry.onload

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_onload`

**Inputs** self.

**Record and data access** read “Salary Slip” via count.

**Explicit results** no value.

**Local steps**

- If (self.docstatus equals 0 and not self.salary\_slips\_created and self.employees).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 0 → not self.salary\_slips\_created → self.employees.
  - Set list(employees\_eligible\_for\_overtime, unsubmitted\_overtime\_slips) from self.get\_overtime\_slip\_details().
  - Set overtime\_step from no value.
  - If unsubmitted\_overtime\_slips.
    - Set overtime\_step from “Submit”.
  - Otherwise.
    - If employees\_eligible\_for\_overtime.
      - Set overtime\_step from “Create”.
  - Set self.overtime\_step from overtime\_step.
- If (not self.docstatus equals 1 or self.salary\_slips\_submitted).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.docstatus equals 1 → self.salary\_slips\_submitted.
  - Return no value.
- Set entries from Platform.db.count(“Salary Slip”, mapping(“payroll\_entry” → self.name, “docstatus” → 1)).
- If cint(entries) equals len(self.employees).
  - Evaluate self.set\_onload(“submitted\_ss”, true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get overtime slip details](operations-010.md#op-1fb21bbfa3a585).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L4215) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L526) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L873)

<a id="op-0bf9ed894bd8a5"></a>
### Payroll Entry.validate

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_validate`

**Inputs** self.

**Local steps**

- Set self.number\_of\_employees from len(self.employees).
- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-008.md#op-d42ef38cfb8d31).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L4620) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L539) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L886)

<a id="op-d42ef38cfb8d31"></a>
### Payroll Entry.set status

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_set_status`

**Inputs** self, status = no value, update = false.

**State and service calls** call db\_set on self.

**Local steps**

- If not status.
  - Set status from mapping(0 → “Draft”, 1 → “Submitted”, 2 → “Cancelled”) at (self.docstatus or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus → 0.
- If update.
  - Evaluate self.db\_set(“status”, status).
- Otherwise.
  - Set self.status from status.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L4705) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L534) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L881)

<a id="op-5216b50502091e"></a>
### Payroll Entry.before submit

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_before_submit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot submit. Attendance is not marked for some employees.”.

**Local steps**

- Evaluate self.validate\_existing\_salary\_slips().
- Evaluate self.validate\_payroll\_payable\_account().
- If self.get\_employees\_with\_unmarked\_attendance().
  - Call the validation error handler Platform.throw(translated “Cannot submit. Attendance is not marked for some employees.”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate existing salary slips](operations-008.md#op-364ac088d9d389), [validate payroll payable account](operations-008.md#op-d29eaff3e9e0ad), [get employees with unmarked attendance](operations-010.md#op-1a615240e5b47f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L4899) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L491) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L840)

<a id="op-ef5a01b35a936c"></a>
### Payroll Entry.on submit

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status(update = true, status = “Submitted”).
- Evaluate self.create\_salary\_slips().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-008.md#op-d42ef38cfb8d31), [create salary slips](operations-008.md#op-0004c17e8afdcf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L5032) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L525) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L872)

<a id="op-364ac088d9d389"></a>
### Payroll Entry.validate existing salary slips

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_validate_existing_salary_slips`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If not self.employees.
  - Return no value.
- Set existing\_salary\_slips from list().
- Set SalarySlip from Platform.qb.DocType(“Salary Slip”).
- Set existing\_salary\_slips from nested operand in the contract(nested operand in the contract).select(SalarySlip.employee, SalarySlip.name).where((((nested operand in the contract(nested operand in the contract) bitwise and nested operan ….
  - Draw emp from self.employees.
- If len(existing\_salary\_slips).
  - Set msg from translated “Salary Slip already exists for {0} for the given dates”.format(comma\_and(list of Platform.bold(d.employee) for d drawn from existing\_salary\_slips)).
    - Draw d from existing\_salary\_slips.
  - Update msg using + text in the contract.
  - Update msg using + translated “Reference: {0}”.format(comma\_and(list of get\_link\_to\_form(“Salary Slip”, d.name) for d drawn from existing\_salary\_slips)).
    - Draw d from existing\_salary\_slips.
  - Call the validation error handler Platform.throw(msg, title = translated “Duplicate Entry”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L5124) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L540) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L887)

<a id="op-d29eaff3e9e0ad"></a>
### Payroll Entry.validate payroll payable account

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_validate_payroll_payable_account`

**Inputs** self.

**Record and data access** read “Account” via get\_value.

**Explicit failure paths** validation helper — translated “Account type should be set {0} for payroll payable account {1}, please set and try again”.format(Platform.bold(“Payable”), Platform.bold(get\_link\_to\_form(“Account”, self.payroll\_payable\_account))).

**Local steps**

- Set payroll\_payable\_account\_type from Platform.db.get\_value(“Account”, self.payroll\_payable\_account, “account\_type”).
- If payroll\_payable\_account\_type differs from “Payable”.
  - Call the validation error handler Platform.throw(translated “Account type should be set {0} for payroll payable account {1}, please set and try again”.format(Platform.bold(“Payable”), Platform.bold(get\_link\_to\_form(“Account”, self.payroll\_ ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L5737) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L541) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L888)

<a id="op-a452902044d8a3"></a>
### Payroll Entry.on cancel

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Salary Slip”, “Journal Entry”).
- Evaluate self.delete\_linked\_salary\_slips().
- Evaluate self.cancel\_linked\_journal\_entries().
- Evaluate self.cancel\_linked\_payment\_ledger\_entries().
- Evaluate self.db\_set(“salary\_slips\_created”, 0).
- Evaluate self.db\_set(“salary\_slips\_submitted”, 0).
- Evaluate self.set\_status(update = true, status = “Cancelled”).
- Evaluate self.db\_set(“error\_message”, empty text).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete linked salary slips](operations-008.md#op-b9be5624b95ef6), [cancel linked journal entries](operations-008.md#op-79e461ddd187f6), [cancel linked payment ledger entries](operations-008.md#op-aa5bb486d6ec75), [set status](operations-008.md#op-d42ef38cfb8d31).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L5967) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L523) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L870)

<a id="op-bfecec0728984a"></a>
### Payroll Entry.on discard

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L6239) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L524) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L871)

<a id="op-9faac21e01a480"></a>
### Payroll Entry.cancel

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_cancel`

**Inputs** self.

**State and service calls** msgprint with msg.

**Local steps**

- If len(self.get\_linked\_salary\_slips()) &gt; 50.
  - Set msg from translated “Payroll Entry cancellation is queued. It may take a few minutes”.
  - Update msg using + text in the contract.
  - Update msg using + translated “In case of any error during this background process, the system will add a comment about the error on this P …”.
  - Evaluate Platform.msgprint(msg, indicator = “blue”, title = translated “Cancellation Queued”).
  - Evaluate self.queue\_action(“cancel”, timeout = 3000).
- Otherwise.
  - Evaluate self.\_cancel().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get linked salary slips](operations-008.md#op-6b87c84b35d50a).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L6302) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L492) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L841)

<a id="op-b9be5624b95ef6"></a>
### Payroll Entry.delete linked salary slips

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_delete_linked_salary_slips`

**Inputs** self.

**Record and data access** resolve a document from “Salary Slip” via get\_doc.

**State and service calls** call cancel on Platform.get\_doc(“Salary Slip”, salary\_slip.name) · request delete\_doc for “Salary Slip”.

**Local steps**

- Set salary\_slips from self.get\_linked\_salary\_slips().
- For each salary\_slip in salary\_slips.
  - If salary\_slip.docstatus equals 1.
    - Evaluate Platform.get\_doc(“Salary Slip”, salary\_slip.name).cancel().
  - Evaluate Platform.delete\_doc(“Salary Slip”, salary\_slip.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get linked salary slips](operations-008.md#op-6b87c84b35d50a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0114.json#L6561) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L497) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L846)

<a id="op-79e461ddd187f6"></a>
### Payroll Entry.cancel linked journal entries

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_cancel_linked_journal_entries`

**Inputs** self.

**Record and data access** read “Journal Entry Account” via get\_all · read “Payment Ledger Entry” via get\_all · resolve a document from “Payment Ledger Entry” via get\_doc · resolve a document from “Journal Entry” via get\_doc.

**State and service calls** call cancel on payment\_ledger\_entry · call cancel on journal\_entry.

**Local steps**

- Set journal\_entries from Platform.get\_all(“Journal Entry Account”, mapping(“reference\_type” → self.doctype, “reference\_name” → self.name, “docstatus” → 1), pluck = “parent”, distinct = true).
- For each je in journal\_entries.
  - Set journal\_entry\_payment\_ledgers from Platform.get\_all(“Payment Ledger Entry”, mapping(“voucher\_type” → “Journal Entry”, “voucher\_no” → je, “docstatus” → 1), distinct = true).
  - For each pl in journal\_entry\_payment\_ledgers.
    - Set payment\_ledger\_entry from Platform.get\_doc(“Payment Ledger Entry”, pl).
    - Set payment\_ledger\_entry.flags.ignore\_permissions from true.
    - Evaluate payment\_ledger\_entry.cancel().
  - Set journal\_entry from Platform.get\_doc(“Journal Entry”, je).
  - Set journal\_entry.flags.ignore\_permissions from true.
  - Evaluate journal\_entry.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L493) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L842)

<a id="op-aa5bb486d6ec75"></a>
### Payroll Entry.cancel linked payment ledger entries

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_cancel_linked_payment_ledger_entries`

**Inputs** self.

**Record and data access** read “Payment Ledger Entry” via get\_all · resolve a document from “Payment Ledger Entry” via get\_doc.

**State and service calls** call cancel on payment\_ledger\_entry.

**Local steps**

- Set payment\_ledgers from Platform.get\_all(“Payment Ledger Entry”, mapping(“against\_voucher\_type” → self.doctype, “against\_voucher\_no” → self.name, “docstatus” → 1), distinct = true).
- For each pl in payment\_ledgers.
  - Set payment\_ledger\_entry from Platform.get\_doc(“Payment Ledger Entry”, pl).
  - Set payment\_ledger\_entry.flags.ignore\_permissions from true.
  - Evaluate payment\_ledger\_entry.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L447) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L494) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L843)

<a id="op-6b87c84b35d50a"></a>
### Payroll Entry.get linked salary slips

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_linked_salary_slips`

**Inputs** self.

**Record and data access** read “Salary Slip” via get\_all.

**Explicit results** Platform.get\_all(“Salary Slip”, mapping(“payroll\_entry” → self.name), list(“name”, “docstatus”)).

**Local steps**

- Return Platform.get\_all(“Salary Slip”, mapping(“payroll\_entry” → self.name), list(“name”, “docstatus”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L680) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L507) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L854)

<a id="op-9090cded75d981"></a>
### Payroll Entry.make filters

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_make_filters`

**Inputs** self.

**Explicit results** filters.

**Local steps**

- Set filters from Platform.\_dict(company = self.company, branch = self.branch, department = self.department, designation = self.designation, …).
- If not self.salary\_slip\_based\_on\_timesheet.
  - Evaluate filters.update(dict(payroll\_frequency = self.payroll\_frequency)).
- Return filters.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L791) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L521) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L868)

<a id="op-7982f72deb5c85"></a>
### Payroll Entry.fill employee details

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_fill_employee_details`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (list at dict bitwise or no value).

**Explicit results** self.get\_employees\_with\_unmarked\_attendance().

**Explicit failure paths** validation helper — error\_msg.

**Local steps**

- Set filters from self.make\_filters().
- Set employees from get\_employee\_list(filters = filters, as\_dict = true, ignore\_match\_conditions = true).
- Evaluate self.set(“employees”, list()).
- If not employees.
  - Set error\_msg from translated “No employees found for the mentioned criteria:&lt;br&gt;Company: {0}&lt;br&gt; Currency: {1}&lt;br&gt;Payroll Payable Account: {2}”.format(Platform.bold(self.company), Platform.bold(self.currency), Platform.bold ….
  - If self.branch.
    - Update error\_msg using + (text in the contract + translated “Branch: {0}”.format(Platform.bold(self.branch))).
  - If self.department.
    - Update error\_msg using + (text in the contract + translated “Department: {0}”.format(Platform.bold(self.department))).
  - If self.designation.
    - Update error\_msg using + (text in the contract + translated “Designation: {0}”.format(Platform.bold(self.designation))).
  - If self.start\_date.
    - Update error\_msg using + (text in the contract + translated “Start date: {0}”.format(Platform.bold(self.start\_date))).
  - If self.end\_date.
    - Update error\_msg using + (text in the contract + translated “End date: {0}”.format(Platform.bold(self.end\_date))).
  - Call the validation error handler Platform.throw(error\_msg, title = translated “No employees found”).
- Evaluate self.set(“employees”, employees).
- Set self.number\_of\_employees from len(self.employees).
- Evaluate self.update\_employees\_with\_withheld\_salaries().
- Return self.get\_employees\_with\_unmarked\_attendance().

**Methods declared on this owner** [make filters](operations-008.md#op-9090cded75d981), [update employees with withheld salaries](operations-008.md#op-56f190728eb749), [get employees with unmarked attendance](operations-010.md#op-1a615240e5b47f).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L1046) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L499) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L848)

<a id="op-56f190728eb749"></a>
### Payroll Entry.update employees with withheld salaries

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_update_employees_with_withheld_salaries`

**Inputs** self.

**Local steps**

- Set withheld\_salaries from get\_salary\_withholdings(self.start\_date, self.end\_date, pluck = “employee”).
- For each employee in self.employees.
  - If employee.employee belongs to withheld\_salaries.
    - Set employee.is\_salary\_withheld from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L1924) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L538) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L885)

<a id="op-0004c17e8afdcf"></a>
### Payroll Entry.create salary slips

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_create_salary_slips`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**State and service calls** call db\_set on self · enqueue with create\_salary\_slips\_for\_employees · msgprint with translated “Salary Slip creation is queued. It may take a few minutes”.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set employees from list of emp.employee for emp drawn from self.employees.
  - Draw emp from self.employees.
- If employees.
  - Set args from Platform.\_dict(mapping(“salary\_slip\_based\_on\_timesheet” → self.salary\_slip\_based\_on\_timesheet, “payroll\_frequency” → self.payroll\_frequency, “start\_date” → self.start\_date, “end\_date” → self.end\_date, …)).
  - If (len(employees) &gt; 30 or Platform.flags.enqueue\_payroll\_entry).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(employees) &gt; 30 → Platform.flags.enqueue\_payroll\_entry.
    - Evaluate self.db\_set(“status”, “Queued”).
    - Evaluate Platform.enqueue(create\_salary\_slips\_for\_employees, timeout = 3000, employees = employees, args = args, publish\_progress = false).
    - Evaluate Platform.msgprint(translated “Salary Slip creation is queued. It may take a few minutes”, alert = true, indicator = “blue”).
  - Otherwise.
    - Evaluate create\_salary\_slips\_for\_employees(employees, args, publish\_progress = false).
    - Evaluate self.reload().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · service or queued work from Platform.enqueue(create\_salary\_slips\_for\_employees, timeout = 3000, employees = employees, args = args, publish\_progress = false).

**Boundaries to resolve** stored data, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L2072) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L496) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L845)

<a id="op-f5575160dcd091"></a>
### Payroll Entry.get sal slip list

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_selling_slip_list`

**Inputs** self, ss\_status, as\_dict = false.

**Explicit results** ss\_list.

**Local steps**

- Set ss from Platform.qb.DocType(“Salary Slip”).
- Set ss\_list from nested operand in the contract(nested operand in the contract).select(ss.name, ss.salary\_structure).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested o ….
- Return ss\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L2706) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L516) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L863)
