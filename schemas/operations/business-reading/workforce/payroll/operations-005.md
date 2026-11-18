# Payroll and benefits · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Employee tax exemption proof submission

[Record definition](../../../../data/record-types/employee_tax_exemption_proof_submission.json)

<a id="op-c83910c2a2ee0c"></a>
### Employee Tax Exemption Proof Submission.validate

`operation_workforce_payroll_record_definitions_employee_tax_exemption_proof_submission_business_behavior_employee_tax_exemption_proof_submission_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate validate\_tax\_declaration(self.tax\_exemption\_proofs).
- Evaluate self.set\_total\_actual\_amount().
- Evaluate self.set\_total\_exemption\_amount().
- Evaluate self.calculate\_hra\_exemption().
- Evaluate validate\_duplicate\_exemption\_for\_payroll\_period(self.doctype, self.name, self.payroll\_period, self.employee).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set total actual amount](operations-005.md#op-a53add01507df3), [set total exemption amount](operations-005.md#op-96c39ea6368bcb), [calculate hra exemption](operations-005.md#op-6e7eee04516d19).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L435) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L408) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L757)

<a id="op-a53add01507df3"></a>
### Employee Tax Exemption Proof Submission.set total actual amount

`operation_workforce_payroll_record_definitions_employee_tax_exemption_proof_submission_business_behavior_employee_tax_exemption_proof_submission_set_total_actual_amount`

**Inputs** self.

**Local steps**

- Set self.total\_actual\_amount from flt(self.get(“house\_rent\_payment\_amount”)).
- For each d in self.tax\_exemption\_proofs.
  - Update self.total\_actual\_amount using + flt(d.amount).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L627) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L406) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L755)

<a id="op-96c39ea6368bcb"></a>
### Employee Tax Exemption Proof Submission.set total exemption amount

`operation_workforce_payroll_record_definitions_employee_tax_exemption_proof_submission_business_behavior_employee_tax_exemption_proof_submission_set_total_exemption_amount`

**Inputs** self.

**Local steps**

- Set self.exemption\_amount from flt(get\_total\_exemption\_amount(self.tax\_exemption\_proofs), self.precision(“exemption\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L753) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L407) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L756)

<a id="op-6e7eee04516d19"></a>
### Employee Tax Exemption Proof Submission.calculate hra exemption

`operation_workforce_payroll_record_definitions_employee_tax_exemption_proof_submission_business_behavior_employee_tax_exemption_proof_submission_calculate_hra_exemption`

**Inputs** self.

**Local steps**

- Set tuple(self.monthly\_hra\_exemption, self.monthly\_house\_rent, self.total\_eligible\_hra\_exemption) from tuple(0, 0, 0).
- If self.get(“house\_rent\_payment\_amount”).
  - Set hra\_exemption from calculate\_hra\_exemption\_for\_period(self).
  - If hra\_exemption.
    - Update self.exemption\_amount using + hra\_exemption at “total\_eligible\_hra\_exemption”.
    - Set self.exemption\_amount from flt(self.exemption\_amount, self.precision(“exemption\_amount”)).
    - Set self.monthly\_hra\_exemption from flt(hra\_exemption at “monthly\_exemption”, self.precision(“monthly\_hra\_exemption”)).
    - Set self.monthly\_house\_rent from flt(hra\_exemption at “monthly\_house\_rent”, self.precision(“monthly\_house\_rent”)).
    - Set self.total\_eligible\_hra\_exemption from flt(hra\_exemption at “total\_eligible\_hra\_exemption”, self.precision(“total\_eligible\_hra\_exemption”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L857) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L405) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L754)

## Record · Employee tax exemption sub category

<a id="op-c7d37e3df64bef"></a>
### Employee Tax Exemption Sub Category.validate

`operation_workforce_payroll_record_definitions_employee_tax_exemption_sub_category_business_behavior_employee_tax_exemption_subordinate_category_validate`

**Inputs** self.

**Record and data access** read “Employee Tax Exemption Category” via get\_value.

**Explicit failure paths** validation helper — translated “Max Exemption Amount cannot be greater than maximum exemption amount {0} of Tax Exemption Category {1}”.format(category\_max\_amount, self.exemption\_category).

**Local steps**

- Set category\_max\_amount from Platform.db.get\_value(“Employee Tax Exemption Category”, self.exemption\_category, “max\_amount”).
- If flt(self.max\_amount) &gt; flt(category\_max\_amount).
  - Call the validation error handler Platform.throw(translated “Max Exemption Amount cannot be greater than maximum exemption amount {0} of Tax Exemption Category {1}”.format(category\_max\_amount, self.exemption\_category)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L2886) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L413) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L762)

## Record · Gratuity

[Record definition](../../../../data/record-types/gratuity.json)

<a id="op-0af956467ecc0c"></a>
### Gratuity.validate

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_validate`

**Inputs** self.

**Local steps**

- Set data from self.calculate\_work\_experience\_and\_amount().
- Set self.current\_work\_experience from data at “current\_work\_experience”.
- Set self.amount from data at “amount”.
- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate work experience and amount](operations-005.md#op-4d65b7c8a6a64d), [set status](operations-005.md#op-3388eb2f60b4ce).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L3085) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L434) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L783)

<a id="op-01eb5f8dbc6613"></a>
### Gratuity.gratuity settings

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_gratuity_settings`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Gratuity Rule” via get\_value.

**Explicit results** self.\_gratuity\_settings.

**Local steps**

- If not hasattr(self, “\_gratuity\_settings”).
  - Set self.\_gratuity\_settings from Platform.db.get\_value(“Gratuity Rule”, self.gratuity\_rule, list(“work\_experience\_calculation\_function as method”, “total\_working\_days\_per\_year”, “minimum\_year\_for\_gratuity”, “calculate\_gratuity\_amount\_base ….
- Return self.\_gratuity\_settings.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L3220) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L426) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L775)

<a id="op-3388eb2f60b4ce"></a>
### Gratuity.set status

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_set_status`

**Inputs** self, update = false.

**State and service calls** call db\_set on self.

**Local steps**

- Set status from mapping(“0” → “Draft”, “1” → “Submitted”, “2” → “Cancelled”) at cstr((self.docstatus or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus → 0.
- If self.docstatus equals 1.
  - Set precision from self.precision(“paid\_amount”).
  - If (flt(self.paid\_amount) &gt; 0 and flt(self.amount, precision) equals flt(self.paid\_amount, precision)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.paid\_amount) &gt; 0 → flt(self.amount, precision) equals flt(self.paid\_amount, precision).
    - Set status from “Paid”.
  - Otherwise.
    - Set status from “Unpaid”.
- If (update and self.status differs from status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in update → self.status differs from status.
  - Evaluate self.db\_set(“status”, status).
- Otherwise.
  - Set self.status from status.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L3393) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L432) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L781)

<a id="op-6fb84ee04dd71c"></a>
### Gratuity.on submit

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_on_submit`

**Inputs** self.

**Local steps**

- If self.pay\_via\_salary\_slip.
  - Evaluate self.create\_additional\_salary().
- Otherwise.
  - Evaluate self.create\_gl\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create additional salary](operations-005.md#op-c30aa9aa296b8f), [create gl entries](operations-005.md#op-2ee419117b9865).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L3789) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L431) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L780)

<a id="op-b529ceaeef1988"></a>
### Gratuity.on cancel

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_on_cancel`

**Inputs** self.

**Local steps**

- Set self.ignore\_linked\_doctypes from list(“GL Entry”, “Payment Ledger Entry”, “Advance Payment Ledger Entry”).
- Evaluate self.create\_gl\_entries(cancel = true).
- Evaluate self.set\_status(update = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create gl entries](operations-005.md#op-2ee419117b9865), [set status](operations-005.md#op-3388eb2f60b4ce).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L3875) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L429) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L778)

<a id="op-2ee419117b9865"></a>
### Gratuity.create gl entries

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_create_general_ledger_entries`

**Inputs** self, cancel = false.

**Local steps**

- Set gl\_entries from self.get\_gl\_entries().
- Evaluate make\_gl\_entries(gl\_entries, cancel).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get gl entries](operations-005.md#op-ff442cfab3fa44).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L4013) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L417) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L766)

<a id="op-ff442cfab3fa44"></a>
### Gratuity.get gl entries

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_get_general_ledger_entries`

**Inputs** self.

**Explicit results** gl\_entry.

**Explicit failure paths** validation helper — translated “Total Amount cannot be zero”.

**Local steps**

- Set gl\_entry from list().
- If self.amount.
  - Evaluate gl\_entry.append(self.get\_gl\_dict(mapping(“account” → self.payable\_account, “credit” → self.amount, “credit\_in\_account\_currency” → self.amount, “against” → self.expense\_account, …), item = self)).
  - Evaluate gl\_entry.append(self.get\_gl\_dict(mapping(“account” → self.expense\_account, “debit” → self.amount, “debit\_in\_account\_currency” → self.amount, “against” → self.payable\_account, …), item = self)).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Total Amount cannot be zero”).
- Return gl\_entry.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L4106) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L419) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L768)

<a id="op-c30aa9aa296b8f"></a>
### Gratuity.create additional salary

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_create_additional_salary`

**Inputs** self.

**State and service calls** request new\_doc for “Additional Salary” · call submit on additional\_salary.

**Local steps**

- If self.pay\_via\_salary\_slip.
  - Set additional\_salary from Platform.new\_doc(“Additional Salary”).
  - Set additional\_salary.employee from self.employee.
  - Set additional\_salary.salary\_component from self.salary\_component.
  - Set additional\_salary.overwrite\_salary\_structure\_amount from 0.
  - Set additional\_salary.amount from self.amount.
  - Set additional\_salary.payroll\_date from self.payroll\_date.
  - Set additional\_salary.company from self.company.
  - Set additional\_salary.ref\_doctype from self.doctype.
  - Set additional\_salary.ref\_docname from self.name.
  - Evaluate additional\_salary.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L4593) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L416) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L765)

<a id="op-2e73b29cc4a125"></a>
### Gratuity.set total advance paid

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_set_total_advance_paid`

**Inputs** self.

**State and service calls** call db\_set on self.

**Explicit failure paths** validation helper — translated “Row {0}# Paid Amount cannot be greater than Total amount”.

**Local steps**

- Set aple from Platform.qb.DocType(“Advance Payment Ledger Entry”).
- Set paid\_amount from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run(as\_dict = true) at 0.paid\_amount or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … → 0.
- If flt(paid\_amount) &gt; self.amount.
  - Call the validation error handler Platform.throw(translated “Row {0}# Paid Amount cannot be greater than Total amount”).
- Evaluate self.db\_set(“paid\_amount”, paid\_amount).
- Evaluate self.set\_status(update = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-005.md#op-3388eb2f60b4ce).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L4856) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L433) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L782)

<a id="op-4d65b7c8a6a64d"></a>
### Gratuity.calculate work experience and amount

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_calculate_work_experience_and_amount`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“current\_work\_experience” → current\_work\_experience, “amount” → gratuity\_amount).

**Local steps**

- If self.gratuity\_settings.method equals “Manual”.
  - Set current\_work\_experience from flt(self.current\_work\_experience).
- Otherwise.
  - Set current\_work\_experience from self.get\_work\_experience().
- Set gratuity\_amount from self.get\_gratuity\_amount(current\_work\_experience).
- Return mapping(“current\_work\_experience” → current\_work\_experience, “amount” → gratuity\_amount).

**Methods declared on this owner** [get work experience](operations-005.md#op-49a651f33f97ac), [get gratuity amount](operations-005.md#op-44e3a252532c20).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L5324) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L415) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L764)

<a id="op-49a651f33f97ac"></a>
### Gratuity.get work experience

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_get_work_experience`

**Inputs** self.

**Declared result** float.

**Explicit results** (work\_experience or 0).

**Explicit failure paths** validation helper — translated “Employee: {0} have to complete minimum {1} years for gratuity”.format(bold(self.employee), rule.minimum\_year\_for\_gratuity).

**Local steps**

- Set total\_working\_days from self.get\_total\_working\_days().
- Set rule from self.gratuity\_settings.
- Set work\_experience from (total\_working\_days ÷ (rule.total\_working\_days\_per\_year or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rule.total\_working\_days\_per\_year → 1.
- If rule.method equals “Round off Work Experience”.
  - Set work\_experience from round(work\_experience).
- Otherwise.
  - Set work\_experience from flt(work\_experience, self.precision(“current\_work\_experience”)).
- If work\_experience &lt; rule.minimum\_year\_for\_gratuity.
  - Call the validation error handler Platform.throw(translated “Employee: {0} have to complete minimum {1} years for gratuity”.format(bold(self.employee), rule.minimum\_year\_for\_gratuity)).
- Return (work\_experience or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in work\_experience → 0.

**Methods declared on this owner** [get total working days](operations-005.md#op-4cf1d0fae062e9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L5533) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L425) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L774)

<a id="op-4cf1d0fae062e9"></a>
### Gratuity.get total working days

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_get_total_working_days`

**Inputs** self.

**Declared result** float.

**Record and data access** read “Employee” via get\_value · read “Payroll Settings” via get\_single\_value.

**Explicit results** total\_working\_days.

**Explicit failure paths** validation helper — translated “Please set Relieving Date for employee: {0}”.format(bold(get\_link\_to\_form(“Employee”, self.employee))).

**Local steps**

- Set tuple(date\_of\_joining, relieving\_date) from Platform.db.get\_value(“Employee”, self.employee, list(“date\_of\_joining”, “relieving\_date”)).
- If not relieving\_date.
  - Call the validation error handler Platform.throw(translated “Please set Relieving Date for employee: {0}”.format(bold(get\_link\_to\_form(“Employee”, self.employee)))).
- Set total\_working\_days from (get\_datetime(relieving\_date) − get\_datetime(date\_of\_joining)).days.
- Set payroll\_based\_on from (Platform.db.get\_single\_value(“Payroll Settings”, “payroll\_based\_on”) or “Leave”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“Payroll Settings”, “payroll\_based\_on”) → “Leave”.
- If payroll\_based\_on equals “Leave”.
  - Set total\_lwp from self.get\_non\_working\_days(relieving\_date, “On Leave”).
  - Update total\_working\_days using − total\_lwp.
- Otherwise.
  - If payroll\_based\_on equals “Attendance”.
    - Set total\_absent from self.get\_non\_working\_days(relieving\_date, “Absent”).
    - Update total\_working\_days using − total\_absent.
- Return total\_working\_days.

**Methods declared on this owner** [get non working days](operations-005.md#op-3cf2fef3b6f7fe).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Payroll Settings”, “payroll\_based\_on”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L5871) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L424) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L773)

<a id="op-3cf2fef3b6f7fe"></a>
### Gratuity.get non working days

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_get_non_working_days`

**Inputs** self, relieving\_date, status.

**Declared result** float.

**Record and data access** read “Leave Type” via get\_all · read “Attendance” via get\_all.

**Explicit results** record at 0.total\_lwp when len(record), otherwise 0.

**Local steps**

- Set filters from mapping(“docstatus” → 1, “status” → status, “employee” → self.employee, “attendance\_date” → tuple(“&lt;=”, get\_datetime(relieving\_date))).
- If status equals “On Leave”.
  - Set lwp\_leave\_types from Platform.get\_all(“Leave Type”, filters = mapping(“is\_lwp” → 1), pluck = “name”).
  - Set filters at “leave\_type” from tuple(“IN”, lwp\_leave\_types).
- Set record from Platform.get\_all(“Attendance”, filters = filters, fields = list(mapping(“COUNT” → “\*”, “as” → “total\_lwp”))).
- Return record at 0.total\_lwp when len(record), otherwise 0.
  - Value choice on len(record) — true gives record at 0.total\_lwp, false gives 0.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0111.json#L6352) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L422) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L771)

<a id="op-44e3a252532c20"></a>
### Gratuity.get gratuity amount

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_get_gratuity_amount`

**Inputs** self, experience.

**Declared result** float.

**Explicit results** flt(gratuity\_amount, self.precision(“amount”)).

**Explicit failure paths** validation helper — translated “No applicable slab found for the calculation of gratuity amount as per the Gratuity Rule: {0}”.format(bold(self.gratuity\_rule)).

**Local steps**

- Set total\_component\_amount from self.get\_total\_component\_amount().
- Set calculate\_amount\_based\_on from self.gratuity\_settings.calculate\_gratuity\_amount\_based\_on.
- Set gratuity\_amount from 0.
- Set slabs from self.get\_gratuity\_rule\_slabs().
- Set slab\_found from false.
- Set years\_left from experience.
- For each slab in slabs.
  - If calculate\_amount\_based\_on equals “Current Slab”.
    - If self.\_is\_experience\_within\_slab(slab, experience).
      - Set gratuity\_amount from ((total\_component\_amount × experience) × slab.fraction\_of\_applicable\_earnings).
      - If slab.fraction\_of\_applicable\_earnings.
        - Set slab\_found from true.
    - If slab\_found.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - Otherwise.
    - If calculate\_amount\_based\_on equals “Sum of all previous slabs”.
      - If (slab.to\_year equals 0 and slab.from\_year equals 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in slab.to\_year equals 0 → slab.from\_year equals 0.
        - Update gratuity\_amount using + ((years\_left × total\_component\_amount) × slab.fraction\_of\_applicable\_earnings).
        - Set slab\_found from true.
        - Leave the innermost loop without its normal-exhaustion alternative.
      - If self.\_is\_experience\_beyond\_slab(slab, experience).
        - Update gratuity\_amount using + (((slab.to\_year − slab.from\_year) × total\_component\_amount) × slab.fraction\_of\_applicable\_earnings).
        - Update years\_left using − (slab.to\_year − slab.from\_year).
        - Set slab\_found from true.
      - Otherwise.
        - If self.\_is\_experience\_within\_slab(slab, experience).
          - Update gratuity\_amount using + ((years\_left × total\_component\_amount) × slab.fraction\_of\_applicable\_earnings).
          - Set slab\_found from true.
          - Leave the innermost loop without its normal-exhaustion alternative.
- If not slab\_found.
  - Call the validation error handler Platform.throw(translated “No applicable slab found for the calculation of gratuity amount as per the Gratuity Rule: {0}”.format(bold(self.gratuity\_rule))).
- Return flt(gratuity\_amount, self.precision(“amount”)).

**Methods declared on this owner** [get total component amount](operations-005.md#op-89985209ead5b9), [get gratuity rule slabs](operations-005.md#op-a70872bcc28e9c), [is experience within slab](operations-005.md#op-154b31a63ffb52), [is experience beyond slab](operations-005.md#op-fc9f70b46c11f9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0112.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L420) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L769)

<a id="op-89985209ead5b9"></a>
### Gratuity.get total component amount

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_get_total_component_amount`

**Inputs** self.

**Declared result** float.

**Explicit results** total\_amount.

**Explicit failure paths** validation helper — translated “No Salary Slip found for Employee: {0}”.format(bold(self.employee)) · validation helper — translated “No applicable Earning component found in last salary slip for Gratuity Rule: {0}”.format(bold(get\_link\_to\_form(“Gratuity Rule”, self.gratuity\_rule))).

**Local steps**

- Set applicable\_earning\_components from self.get\_applicable\_components().
- Set salary\_slip from get\_last\_salary\_slip(self.employee).
- If not salary\_slip.
  - Call the validation error handler Platform.throw(translated “No Salary Slip found for Employee: {0}”.format(bold(self.employee))).
- Set total\_amount from 0.
- Set component\_found from false.
- For each row in salary\_slip.earnings.
  - If row.salary\_component belongs to applicable\_earning\_components.
    - Update total\_amount using + flt(row.default\_amount).
    - Set component\_found from true.
- If not component\_found.
  - Call the validation error handler Platform.throw(translated “No applicable Earning component found in last salary slip for Gratuity Rule: {0}”.format(bold(get\_link\_to\_form(“Gratuity Rule”, self.gratuity\_rule)))).
- Return total\_amount.

**Methods declared on this owner** [get applicable components](operations-005.md#op-399bb74dbd8026).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0112.json#L761) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L423) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L772)

<a id="op-399bb74dbd8026"></a>
### Gratuity.get applicable components

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_get_applicable_components`

**Inputs** self.

**Declared result** list at str.

**Record and data access** read “Gratuity Applicable Component” via get\_all.

**Explicit results** applicable\_earning\_components.

**Explicit failure paths** validation helper — translated “No applicable Earning components found for Gratuity Rule: {0}”.format(bold(get\_link\_to\_form(“Gratuity Rule”, self.gratuity\_rule))).

**Local steps**

- Set applicable\_earning\_components from Platform.get\_all(“Gratuity Applicable Component”, filters = mapping(“parent” → self.gratuity\_rule), pluck = “salary\_component”).
- If not applicable\_earning\_components.
  - Call the validation error handler Platform.throw(translated “No applicable Earning components found for Gratuity Rule: {0}”.format(bold(get\_link\_to\_form(“Gratuity Rule”, self.gratuity\_rule)))).
- Return applicable\_earning\_components.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0112.json#L1164) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L418) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L767)

<a id="op-a70872bcc28e9c"></a>
### Gratuity.get gratuity rule slabs

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_get_gratuity_rule_slabs`

**Inputs** self.

**Declared result** list at dict.

**Record and data access** read “Gratuity Rule Slab” via get\_all.

**Explicit results** Platform.get\_all(“Gratuity Rule Slab”, filters = mapping(“parent” → self.gratuity\_rule), fields = list(“from\_year”, “to\_year”, “fraction\_of\_applicable\_earnings”), order\_by = “idx”).

**Local steps**

- Return Platform.get\_all(“Gratuity Rule Slab”, filters = mapping(“parent” → self.gratuity\_rule), fields = list(“from\_year”, “to\_year”, “fraction\_of\_applicable\_earnings”), order\_by = “idx”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0112.json#L1406) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L421) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L770)

<a id="op-154b31a63ffb52"></a>
### Gratuity.is experience within slab

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_is_experience_within_slab`

**Inputs** self, slab, experience.

**Declared result** bool.

**Explicit results** bool((slab.from\_year ≤ experience and (experience ≤ slab.to\_year or slab.to\_year equals 0))).

**Local steps**

- Return bool((slab.from\_year ≤ experience and (experience ≤ slab.to\_year or slab.to\_year equals 0))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in slab.from\_year ≤ experience → (experience ≤ slab.to\_year or slab.to\_year equals 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in experience ≤ slab.to\_year → slab.to\_year equals 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0112.json#L1561) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L428) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L777)

<a id="op-fc9f70b46c11f9"></a>
### Gratuity.is experience beyond slab

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_is_experience_beyond_slab`

**Inputs** self, slab, experience.

**Declared result** bool.

**Explicit results** bool((slab.from\_year &lt; experience and (slab.to\_year &lt; experience and slab.to\_year differs from 0))).

**Local steps**

- Return bool((slab.from\_year &lt; experience and (slab.to\_year &lt; experience and slab.to\_year differs from 0))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in slab.from\_year &lt; experience → (slab.to\_year &lt; experience and slab.to\_year differs from 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in slab.to\_year &lt; experience → slab.to\_year differs from 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0112.json#L1705) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L427) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L776)
