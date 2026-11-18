# Payroll and benefits · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Salary slip

[Record definition](../../../../data/record-types/salary_slip.json)

<a id="op-45ba46149eae56"></a>
### Salary Slip.get leave type map

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_leave_type_map`

**Inputs** self.

**Declared result** dict.

**Explicit results** Platform.cache().get\_value(LEAVE\_TYPE\_MAP, \_get\_leave\_type\_map).

**Local steps**

- Bind local operation \_get\_leave\_type\_map for subsequent calls.
- Return Platform.cache().get\_value(LEAVE\_TYPE\_MAP, \_get\_leave\_type\_map).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0124.json#L7013) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L686) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1033)

<a id="op-853b52feebbc85"></a>
### Salary Slip.get leave type map.get leave type map

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_leave_type_map_get_leave_type_map`

**Inputs** no declared parameters.

**Record and data access** read “Leave Type” via get\_all.

**Explicit results** mapping of leave\_type.name → leave\_type for leave\_type drawn from leave\_types.

**Local steps**

- Set leave\_types from Platform.get\_all(“Leave Type”, or\_filters = mapping(“is\_ppl” → 1, “is\_lwp” → 1), fields = list(“name”, “is\_lwp”, “is\_ppl”, “fraction\_of\_daily\_salary\_per\_leave”, …)).
- Return mapping of leave\_type.name → leave\_type for leave\_type drawn from leave\_types.
  - Draw leave\_type from leave\_types.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0124.json#L7263) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L687) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1034)

<a id="op-8ff1e32845903b"></a>
### Salary Slip.get employee attendance

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_employee_attendance`

**Inputs** self, start\_date, end\_date.

**Explicit results** attendance\_details.

**Local steps**

- Set attendance from Platform.qb.DocType(“Attendance”).
- Set attendance\_details from nested operand in the contract(nested operand in the contract).select(attendance.attendance\_date, attendance.status, attendance.leave\_type, attendance.half\_day\_status).where((((nested operand in the contra ….
- Return attendance\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L676) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1023)

<a id="op-3adeb8bf85f790"></a>
### Salary Slip.calculate lwp ppl and absent days based on attendance

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_calculate_leave_without_pay_partially_paid_leave_and_absent_days_based_on_attendance`

**Inputs** self, holidays, half\_day\_holidays, daily\_wages\_fraction\_for\_half\_day, consider\_marked\_attendance\_on\_holidays.

**Explicit results** tuple(lwp, absent).

**Local steps**

- Set lwp from 0.
- Set absent from 0.
- Set leave\_type\_map from self.get\_leave\_type\_map().
- Set attendance\_details from self.get\_employee\_attendance(start\_date = self.start\_date, end\_date = self.actual\_end\_date).
- For each d in attendance\_details.
  - If (d.status belongs to tuple(“Half Day”, “On Leave”) and d.leave\_type and d.leave\_type does not belong to leave\_type\_map.keys()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.status belongs to tuple(“Half Day”, “On Leave”) → d.leave\_type → d.leave\_type does not belong to leave\_type\_map.keys().
    - Continue with the next iteration or loop test.
  - If (not consider\_marked\_attendance\_on\_holidays and getdate(d.attendance\_date) belongs to holidays).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not consider\_marked\_attendance\_on\_holidays → getdate(d.attendance\_date) belongs to holidays.
    - If (d.status belongs to list(“Absent”, “Half Day”) or (d.leave\_type and d.leave\_type belongs to leave\_type\_map.keys() and not leave\_type\_map at d.leave\_type at “include\_holiday”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.status belongs to list(“Absent”, “Half Day”) → (d.leave\_type and d.leave\_type belongs to leave\_type\_map.keys() and not leave\_type\_map at d.leave\_type at “include\_holiday”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.leave\_type → d.leave\_type belongs to leave\_type\_map.keys() → not leave\_type\_map at d.leave\_type at “include\_holiday”.
      - Continue with the next iteration or loop test.
  - If d.leave\_type.
    - Set fraction\_of\_daily\_salary\_per\_leave from leave\_type\_map at d.leave\_type at “fraction\_of\_daily\_salary\_per\_leave”.
  - Set day\_fraction from HALF\_DAY\_HOLIDAY\_FRACTION when getdate(d.attendance\_date) belongs to half\_day\_holidays, otherwise 1.
    - Value choice on getdate(d.attendance\_date) belongs to half\_day\_holidays — true gives HALF\_DAY\_HOLIDAY\_FRACTION, false gives 1.
  - If (d.status equals “Half Day” and d.leave\_type and d.leave\_type belongs to leave\_type\_map.keys()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.status equals “Half Day” → d.leave\_type → d.leave\_type belongs to leave\_type\_map.keys().
    - Set equivalent\_lwp from (1 − daily\_wages\_fraction\_for\_half\_day).
    - If leave\_type\_map at d.leave\_type at “is\_ppl”.
      - Update equivalent\_lwp using × (1 − flt(fraction\_of\_daily\_salary\_per\_leave)).
    - Update lwp using + equivalent\_lwp.
  - Otherwise.
    - If (d.status equals “On Leave” and d.leave\_type and d.leave\_type belongs to leave\_type\_map.keys()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.status equals “On Leave” → d.leave\_type → d.leave\_type belongs to leave\_type\_map.keys().
      - Set equivalent\_lwp from 1.
      - If leave\_type\_map at d.leave\_type at “is\_ppl”.
        - Update equivalent\_lwp using × (1 − flt(fraction\_of\_daily\_salary\_per\_leave)).
      - Update lwp using + (equivalent\_lwp × day\_fraction).
    - Otherwise.
      - If d.status equals “Absent”.
        - Update absent using + day\_fraction.
- Return tuple(lwp, absent).

**Methods declared on this owner** [get leave type map](operations-015.md#op-45ba46149eae56), [get employee attendance](operations-015.md#op-8ff1e32845903b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L105) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L641) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L988)

<a id="op-3760386e14eff2"></a>
### Salary Slip.set salary structure assignment

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_set_salary_structure_assignment`

**Inputs** self.

**Record and data access** read “Salary Structure Assignment” via get\_value.

**Explicit failure paths** validation helper — translated “Please assign a Salary Structure for Employee {0} applicable from or before {1} first”.format(Platform.bold(self.employee\_name), Platform.bold(formatdate(self.actual\_start\_date))).

**Local steps**

- Set self.\_salary\_structure\_assignment from Platform.db.get\_value(“Salary Structure Assignment”, mapping(“employee” → self.employee, “salary\_structure” → self.salary\_structure, “from\_date” → tuple(“&lt;=”, self.actual\_start\_date), “docstatus” → 1), “\*” ….
- If not self.\_salary\_structure\_assignment.
  - Call the validation error handler Platform.throw(translated “Please assign a Salary Structure for Employee {0} applicable from or before {1} first”.format(Platform.bold(self.employee\_name), Platform.bold(formatdate(self.actual\_start\_date)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L1174) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L725) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1072)

<a id="op-856a3df225339e"></a>
### Salary Slip.calculate net pay

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_calculate_net_pay`

**Inputs** self, skip\_tax\_breakup\_computation = false.

**Local steps**

- Bind local operation set\_gross\_pay\_and\_base\_gross\_pay for subsequent calls.
- If self.payroll\_period.
  - Set self.remaining\_sub\_periods from get\_period\_factor(self.employee, self.start\_date, self.end\_date, self.payroll\_frequency, joining\_date = self.joining\_date, relieving\_date = self.relieving\_date, …) at 1.
- If self.salary\_structure.
  - Evaluate self.calculate\_component\_amounts(“earnings”).
- Evaluate set\_gross\_pay\_and\_base\_gross\_pay().
- If self.salary\_structure.
  - Evaluate self.calculate\_component\_amounts(“deductions”).
- Evaluate set\_loan\_repayment(self).
- Evaluate self.apply\_regional\_deductions().
- If self.salary\_structure.
  - Evaluate self.calculate\_component\_amounts(“employer\_contributions”).
- Evaluate self.apply\_regional\_employer\_contributions().
- Evaluate self.set\_precision\_for\_component\_amounts().
- Evaluate self.set\_net\_pay().
- If not skip\_tax\_breakup\_computation.
  - Evaluate self.compute\_income\_tax\_breakup().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate component amounts](operations-015.md#op-8eb18ed38e854b), [apply regional deductions](operations-015.md#op-9ab13663bdb618), [apply regional employer contributions](operations-015.md#op-b0a3e381d0b873), [set precision for component amounts](operations-016.md#op-08fb727f8c9329), [set net pay](operations-015.md#op-4e7abd95c13398), [compute income tax breakup](operations-015.md#op-be41d11265811d).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L106) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L642) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L989)

<a id="op-bdcb20ef9bbe40"></a>
### Salary Slip.calculate net pay.set gross pay and base gross pay

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_calculate_net_pay_set_gross_pay_and_base_gross_pay`

**Inputs** no declared parameters.

**Local steps**

- Set self.gross\_pay from self.get\_component\_totals(“earnings”, depends\_on\_payment\_days = 1).
- Set self.base\_gross\_pay from flt((flt(self.gross\_pay) × flt(self.exchange\_rate)), self.precision(“base\_gross\_pay”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L2071) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L643) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L990)

<a id="op-9ab13663bdb618"></a>
### Salary Slip.apply regional deductions

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_apply_regional_deductions`

**Inputs** self.

**Wrappers, in declaration order** Workforce.allow\_regional.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L2238) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L637) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L984)

<a id="op-b0a3e381d0b873"></a>
### Salary Slip.apply regional employer contributions

`operation_workforce_binding_workforce_payroll_doctype_salary_slip_salary_slip_salaryslip_apply_regional_employer_contributions`

**Inputs** self.

**Wrappers, in declaration order** Workforce.allow\_regional.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L177) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L228) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L228)

<a id="op-4e7abd95c13398"></a>
### Salary Slip.set net pay

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_set_net_pay`

**Inputs** self.

**Local steps**

- Set self.total\_deduction from self.get\_component\_totals(“deductions”).
- Set self.base\_total\_deduction from flt((flt(self.total\_deduction) × flt(self.exchange\_rate)), self.precision(“base\_total\_deduction”)).
- Set self.net\_pay from (flt(self.gross\_pay) − (flt(self.total\_deduction) + flt(self.get(“total\_loan\_repayment”)))).
- Set self.rounded\_total from rounded(self.net\_pay).
- Set self.base\_net\_pay from flt((flt(self.net\_pay) × flt(self.exchange\_rate)), self.precision(“base\_net\_pay”)).
- Set self.base\_rounded\_total from flt(rounded(self.base\_net\_pay), self.precision(“base\_net\_pay”)).
- If self.hour\_rate.
  - Set self.base\_hour\_rate from flt((flt(self.hour\_rate) × flt(self.exchange\_rate)), self.precision(“base\_hour\_rate”)).
- Evaluate self.set\_net\_total\_in\_words().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get component totals](operations-017.md#op-d6ac3135008503), [set net total in words](operations-013.md#op-4b67332a93dc41).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L2280) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L722) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1069)

<a id="op-3604f62a437076"></a>
### Salary Slip.compute taxable earnings for year

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_compute_taxable_earnings_for_year`

**Inputs** self.

**Local steps**

- Set tuple(self.previous\_taxable\_earnings, exempted\_amount) from self.get\_taxable\_earnings\_for\_prev\_period(self.payroll\_period.start\_date, self.start\_date, self.tax\_slab.allow\_tax\_exemption).
- Set self.previous\_taxable\_earnings\_before\_exemption from (self.previous\_taxable\_earnings + exempted\_amount).
- Evaluate self.compute\_current\_and\_future\_taxable\_earnings().
- If self.payroll\_period.end\_date ≤ getdate(self.end\_date).
  - Set self.deduct\_tax\_for\_unsubmitted\_tax\_exemption\_proof from 1.
- Set self.unclaimed\_taxable\_benefits from 0.
- Set self.total\_exemption\_amount from self.get\_total\_exemption\_amount().
- Set self.other\_incomes from (self.get\_income\_form\_other\_sources() or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_income\_form\_other\_sources() → 0.0.
- Set self.total\_taxable\_earnings from ((((((nested operand in the contract.previous\_taxable\_earnings + nested operand in the contract.current\_structured\_taxable\_earnings) + self.future\_structured\_taxable\_earnings) + self.current\_additional\_ear ….
- Set self.total\_taxable\_earnings\_without\_full\_tax\_addl\_components from (self.total\_taxable\_earnings − self.current\_additional\_earnings\_with\_full\_tax).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get taxable earnings for prev period](operations-016.md#op-b5cb8c30ecb706), [compute current and future taxable earnings](operations-015.md#op-44e5b04f4aab21), [get total exemption amount](operations-017.md#op-84d5996f112623), [get income form other sources](operations-017.md#op-ec782c8e4c4a47).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L2852) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L657) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1004)

<a id="op-44e5b04f4aab21"></a>
### Salary Slip.compute current and future taxable earnings

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_compute_current_and_future_taxable_earnings`

**Inputs** self.

**Local steps**

- Set self.current\_taxable\_earnings from self.get\_taxable\_earnings(self.tax\_slab.allow\_tax\_exemption).
- Set self.future\_structured\_taxable\_earnings from (self.current\_taxable\_earnings.taxable\_earnings × (round(self.remaining\_sub\_periods) − 1)).
- Set current\_taxable\_earnings\_before\_exemption from (self.current\_taxable\_earnings.taxable\_earnings + self.current\_taxable\_earnings.amount\_exempted\_from\_income\_tax).
- Set self.future\_structured\_taxable\_earnings\_before\_exemption from (current\_taxable\_earnings\_before\_exemption × (round(self.remaining\_sub\_periods) − 1)).
- Set self.current\_taxable\_earnings\_for\_payment\_days from self.get\_taxable\_earnings(self.tax\_slab.allow\_tax\_exemption, based\_on\_payment\_days = 1).
- Set self.current\_structured\_taxable\_earnings from self.current\_taxable\_earnings\_for\_payment\_days.taxable\_earnings.
- Set self.current\_structured\_taxable\_earnings\_before\_exemption from (self.current\_structured\_taxable\_earnings + self.current\_taxable\_earnings\_for\_payment\_days.amount\_exempted\_from\_income\_tax).
- Set self.current\_additional\_earnings from self.current\_taxable\_earnings\_for\_payment\_days.additional\_income.
- Set self.current\_additional\_earnings\_with\_full\_tax from self.current\_taxable\_earnings\_for\_payment\_days.additional\_income\_with\_full\_tax.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get taxable earnings](operations-017.md#op-c7b06c93ae9232).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L3282) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L653) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1000)

<a id="op-be41d11265811d"></a>
### Salary Slip.compute income tax breakup

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_compute_income_tax_breakup`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.payroll\_period.
  - Return no value.
- Set self.standard\_tax\_exemption\_amount from 0.
- Set self.tax\_exemption\_declaration from 0.
- Set self.deductions\_before\_tax\_calculation from 0.
- Set self.non\_taxable\_earnings from self.compute\_non\_taxable\_earnings().
- Set self.ctc from self.compute\_ctc().
- Set self.income\_from\_other\_sources from self.get\_income\_form\_other\_sources().
- Set self.total\_earnings from (self.ctc + self.income\_from\_other\_sources).
- If hasattr(self, “tax\_slab”).
  - If self.tax\_slab.allow\_tax\_exemption.
    - Set self.standard\_tax\_exemption\_amount from self.tax\_slab.standard\_tax\_exemption\_amount.
    - Set self.deductions\_before\_tax\_calculation from self.compute\_annual\_deductions\_before\_tax\_calculation().
  - Set self.tax\_exemption\_declaration from (self.get\_total\_exemption\_amount() − self.standard\_tax\_exemption\_amount).
- Set self.annual\_taxable\_amount from (self.total\_earnings − (((self.non\_taxable\_earnings + self.deductions\_before\_tax\_calculation) + self.tax\_exemption\_declaration) + self.standard\_tax\_exemption\_amount)).
- Set self.income\_tax\_deducted\_till\_date from self.get\_income\_tax\_deducted\_till\_date().
- If (hasattr(self, “total\_structured\_tax\_amount”) and hasattr(self, “current\_structured\_tax\_amount”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(self, “total\_structured\_tax\_amount”) → hasattr(self, “current\_structured\_tax\_amount”).
  - Set self.future\_income\_tax\_deductions from ((self.total\_structured\_tax\_amount + self.get(“full\_tax\_on\_additional\_earnings”, 0)) − self.income\_tax\_deducted\_till\_date).
  - Set self.current\_month\_income\_tax from self.get(“current\_tax\_amount\_for\_payment\_days”, 0).
  - Set self.total\_income\_tax from (self.income\_tax\_deducted\_till\_date + self.future\_income\_tax\_deductions).

If control reaches the end, it returns no value.

**Methods declared on this owner** [compute non taxable earnings](operations-015.md#op-15a9f7424efa56), [compute ctc](operations-015.md#op-8a321fc1f7d2a0), [get income form other sources](operations-017.md#op-ec782c8e4c4a47), [compute annual deductions before tax calculation](operations-015.md#op-f162f6eda5d780), [get total exemption amount](operations-017.md#op-84d5996f112623), [get income tax deducted till date](operations-015.md#op-39686e03de1791).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L108) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L654) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1001)

<a id="op-8a321fc1f7d2a0"></a>
### Salary Slip.compute ctc

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_compute_cost_to_company`

**Inputs** self.

**Explicit results** (((((self.previous\_taxable\_earnings\_before\_exemption + self.current\_structured\_taxable\_earnings\_before\_exemption) + self.future\_structured\_taxable\_earnings\_before\_exemption) + self.current\_additional\_earni … · 0.0.

**Local steps**

- If hasattr(self, “previous\_taxable\_earnings”).
  - Return (((((self.previous\_taxable\_earnings\_before\_exemption + self.current\_structured\_taxable\_earnings\_before\_exemption) + self.future\_structured\_taxable\_earnings\_before\_exemption) + self.current\_additional\_earni ….
- Return 0.0.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L4318) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L652) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L999)

<a id="op-15a9f7424efa56"></a>
### Salary Slip.compute non taxable earnings

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_compute_non_taxable_earnings`

**Inputs** self.

**Explicit results** non\_taxable\_earnings.

**Local steps**

- Set prev\_period\_non\_taxable\_earnings from self.get\_salary\_slip\_details(self.payroll\_period.start\_date, self.start\_date, parentfield = “earnings”, is\_tax\_applicable = 0).
- Set tuple(current\_period\_non\_taxable\_earnings, non\_taxable\_additional\_salary) from self.get\_non\_taxable\_earnings\_for\_current\_period().
- Set future\_period\_non\_taxable\_earnings from self.get\_future\_period\_non\_taxable\_earnings().
- Set non\_taxable\_earnings from (((prev\_period\_non\_taxable\_earnings + current\_period\_non\_taxable\_earnings) + future\_period\_non\_taxable\_earnings) + non\_taxable\_additional\_salary).
- Return non\_taxable\_earnings.

**Methods declared on this owner** [get salary slip details](operations-016.md#op-3d9b68950fbac3), [get non taxable earnings for current period](operations-015.md#op-07a1a437091361), [get future period non taxable earnings](operations-015.md#op-942fcaf2ac22ed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L4453) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L656) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1003)

<a id="op-942fcaf2ac22ed"></a>
### Salary Slip.get future period non taxable earnings

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_future_period_non_taxable_earnings`

**Inputs** self.

**State and service calls** request copy\_doc for self.

**Explicit results** (future\_period\_non\_taxable\_earnings × (ceil(self.remaining\_sub\_periods) − 1)).

**Local steps**

- Set salary\_slip from Platform.copy\_doc(self).
- Set salary\_slip.payment\_days from salary\_slip.total\_working\_days.
- Evaluate salary\_slip.calculate\_net\_pay(skip\_tax\_breakup\_computation = true).
- Set future\_period\_non\_taxable\_earnings from 0.
- For each earning in salary\_slip.earnings.
  - If (not earning.is\_tax\_applicable and not earning.additional\_salary).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not earning.is\_tax\_applicable → not earning.additional\_salary.
    - Update future\_period\_non\_taxable\_earnings using + earning.amount.
- Return (future\_period\_non\_taxable\_earnings × (ceil(self.remaining\_sub\_periods) − 1)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L4662) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L678) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1025)

<a id="op-07a1a437091361"></a>
### Salary Slip.get non taxable earnings for current period

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_non_taxable_earnings_for_current_period`

**Inputs** self.

**Explicit results** tuple(current\_period\_non\_taxable\_earnings, non\_taxable\_additional\_salary).

**Local steps**

- Set current\_period\_non\_taxable\_earnings from 0.0.
- Set non\_taxable\_additional\_salary from self.get\_salary\_slip\_details(self.payroll\_period.start\_date, self.start\_date, parentfield = “earnings”, is\_tax\_applicable = 0, field\_to\_select = “additional\_amount”).
- For each earning in self.earnings.
  - If earning.is\_tax\_applicable.
    - Continue with the next iteration or loop test.
  - If earning.additional\_amount.
    - Update non\_taxable\_additional\_salary using + earning.additional\_amount.
    - If (earning.additional\_salary and earning.is\_recurring\_additional\_salary).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in earning.additional\_salary → earning.is\_recurring\_additional\_salary.
      - Update non\_taxable\_additional\_salary using + self.get\_future\_recurring\_additional\_amount(earning.additional\_salary, earning.additional\_amount).
  - Otherwise.
    - Update current\_period\_non\_taxable\_earnings using + earning.amount.
- Return tuple(current\_period\_non\_taxable\_earnings, non\_taxable\_additional\_salary).

**Methods declared on this owner** [get salary slip details](operations-016.md#op-3d9b68950fbac3), [get future recurring additional amount](operations-017.md#op-fd3cf4e32e8d90).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L4897) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L689) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1036)

<a id="op-f162f6eda5d780"></a>
### Salary Slip.compute annual deductions before tax calculation

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_compute_annual_deductions_before_tax_calculation`

**Inputs** self.

**Explicit results** (((prev\_period\_exempted\_amount + current\_period\_exempted\_amount) + future\_period\_exempted\_amount) or 0).

**Local steps**

- Set prev\_period\_exempted\_amount from 0.
- Set current\_period\_exempted\_amount from 0.
- Set future\_period\_exempted\_amount from 0.
- Set prev\_period\_exempted\_amount from self.get\_salary\_slip\_details(self.payroll\_period.start\_date, self.start\_date, parentfield = “deductions”, exempted\_from\_income\_tax = 1).
- For each d in self.get(“deductions”).
  - If d.exempted\_from\_income\_tax.
    - Update current\_period\_exempted\_amount using + d.amount.
- For each deduction in self.\_evaluated\_components at “deductions”.
  - If deduction.exempted\_from\_income\_tax.
    - If deduction.amount\_based\_on\_formula.
      - For each sub\_period in range(1, ceil(self.remaining\_sub\_periods)).
        - Update future\_period\_exempted\_amount using + self.get\_amount\_from\_formula(deduction, sub\_period).
    - Otherwise.
      - Update future\_period\_exempted\_amount using + (deduction.amount × (ceil(self.remaining\_sub\_periods) − 1)).
- Return (((prev\_period\_exempted\_amount + current\_period\_exempted\_amount) + future\_period\_exempted\_amount) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ((prev\_period\_exempted\_amount + current\_period\_exempted\_amount) + future\_period\_exempted\_amount) → 0.

**Methods declared on this owner** [get salary slip details](operations-016.md#op-3d9b68950fbac3), [get amount from formula](operations-015.md#op-4f0d5f0dfaa74a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L5198) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L650) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L997)

<a id="op-4f0d5f0dfaa74a"></a>
### Salary Slip.get amount from formula

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_amount_from_formula`

**Inputs** self, struct\_row, sub\_period = 1.

**Explicit results** flt(self.eval\_condition\_and\_formula(struct\_row, local\_data)).

**Local steps**

- If self.payroll\_frequency equals “Monthly”.
  - Set start\_date from Platform.utils.add\_months(self.start\_date, sub\_period).
  - Set end\_date from Platform.utils.add\_months(self.end\_date, sub\_period).
  - Set posting\_date from Platform.utils.add\_months(self.posting\_date, sub\_period).
- Otherwise.
  - Set days\_to\_add from 0.
  - If self.payroll\_frequency equals “Weekly”.
    - Set days\_to\_add from (sub\_period × 6).
  - If self.payroll\_frequency equals “Fortnightly”.
    - Set days\_to\_add from (sub\_period × 13).
  - If self.payroll\_frequency equals “Daily”.
    - Set days\_to\_add from start\_date.
  - Set start\_date from Platform.utils.add\_days(self.start\_date, days\_to\_add).
  - Set end\_date from Platform.utils.add\_days(self.end\_date, days\_to\_add).
  - Set posting\_date from start\_date.
- Set local\_data from self.data.copy().
- Evaluate local\_data.update(mapping(“start\_date” → start\_date, “end\_date” → end\_date, “posting\_date” → posting\_date)).
- Return flt(self.eval\_condition\_and\_formula(struct\_row, local\_data)).

**Methods declared on this owner** [eval condition and formula](operations-016.md#op-373cd93d8ccd5a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L5633) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L665) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1012)

<a id="op-39686e03de1791"></a>
### Salary Slip.get income tax deducted till date

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_income_tax_deducted_till_date`

**Inputs** self.

**Explicit results** tax\_deducted.

**Local steps**

- Set tax\_deducted from 0.0.
- For each tax\_component in (self.get(“\_component\_based\_variable\_tax”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“\_component\_based\_variable\_tax”) → mapping().
  - Update tax\_deducted using + (self.\_component\_based\_variable\_tax at tax\_component at “previous\_total\_paid\_taxes” + self.\_component\_based\_variable\_tax at tax\_component at “current\_tax\_amount\_for\_payment\_days”).
- Return tax\_deducted.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L113) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L684) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1031)

<a id="op-8eb18ed38e854b"></a>
### Salary Slip.calculate component amounts

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_calculate_component_amounts`

**Inputs** self, component\_type.

**Explicit results** no value.

**Local steps**

- If component\_type equals “earnings”.
  - Set self.accrued\_benefits from list().
  - Set self.benefit\_ledger\_components from list().
- If not getattr(self, “\_evaluated\_components”, no value).
  - Evaluate self.\_set\_evaluated\_components().
- Evaluate self.add\_structure\_components(component\_type).
- If component\_type equals “employer\_contributions”.
  - Return no value.
- Evaluate self.add\_additional\_salary\_components(component\_type).
- If component\_type equals “earnings”.
  - Evaluate self.add\_employee\_benefits().
- Otherwise.
  - Evaluate self.add\_tax\_components().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set evaluated components](operations-015.md#op-87fa1860e327c1), [add structure components](operations-015.md#op-d58e6f690c148b), [add additional salary components](operations-016.md#op-52c567971fe769), [add employee benefits](operations-016.md#op-35fbb37f32851e), [add tax components](operations-016.md#op-a9c60b47c100ac).

**Values supplied outside this operation** selected callable from getattr(self, “\_evaluated\_components”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L6370) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L639) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L986)

<a id="op-87fa1860e327c1"></a>
### Salary Slip.set evaluated components

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_set_evaluated_components`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.\_evaluated\_components from self.\_get\_ssa\_doc().get\_evaluated\_components().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get ssa doc](operations-015.md#op-20bb18cb8a0757).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L6674) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L721) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1068)

<a id="op-20bb18cb8a0757"></a>
### Salary Slip.get ssa doc

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_ssa_record`

**Inputs** self.

**Record and data access** resolve a document from “Salary Structure Assignment” via get\_cached\_doc.

**Explicit results** self.\_ssa\_doc.

**Local steps**

- If not getattr(self, “\_ssa\_doc”, no value).
  - If not hasattr(self, “\_salary\_structure\_assignment”).
    - Evaluate self.set\_salary\_structure\_assignment().
  - Set self.\_ssa\_doc from Platform.get\_cached\_doc(“Salary Structure Assignment”, self.\_salary\_structure\_assignment.name).
- Return self.\_ssa\_doc.

**Methods declared on this owner** [set salary structure assignment](operations-015.md#op-3760386e14eff2).

**Values supplied outside this operation** selected callable from getattr(self, “\_ssa\_doc”, no value) · configured or stored value from Platform.get\_cached\_doc(“Salary Structure Assignment”, self.\_salary\_structure\_assignment.name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L6747) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L694) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1041)

<a id="op-d58e6f690c148b"></a>
### Salary Slip.add structure components

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_add_structure_components`

**Inputs** self, component\_type.

**Local steps**

- Set tuple(self.data, self.default\_data) from self.get\_data\_for\_eval().
- For each struct\_row in self.\_evaluated\_components at component\_type.
  - Evaluate self.add\_structure\_component(struct\_row, component\_type).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get data for eval](operations-016.md#op-2a477af237b7b2), [add structure component](operations-016.md#op-d0d01ef72e84fa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0125.json#L6925) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L634) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L981)
