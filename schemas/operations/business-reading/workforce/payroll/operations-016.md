# Payroll and benefits · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Salary slip

[Record definition](../../../../data/record-types/salary_slip.json)

<a id="op-d0d01ef72e84fa"></a>
### Salary Slip.add structure component

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_add_structure_component`

**Inputs** self, struct\_row, component\_type.

**Record and data access** read “Salary Component” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If (self.salary\_slip\_based\_on\_timesheet and struct\_row.salary\_component equals getattr(self, “\_timesheet\_component”, no value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.salary\_slip\_based\_on\_timesheet → struct\_row.salary\_component equals getattr(self, “\_timesheet\_component”, no value).
  - Return no value.
- Set amount from self.eval\_condition\_and\_formula(struct\_row, self.data).
- Set condition\_met from amount is distinct from no value.
- If (struct\_row.statistical\_component or struct\_row.accrual\_component).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in struct\_row.statistical\_component → struct\_row.accrual\_component.
  - Set self.default\_data at struct\_row.abbr from flt(amount).
  - If struct\_row.depends\_on\_payment\_days.
    - Set amount from ((flt(amount) × flt(self.payment\_days)) ÷ cint(self.total\_working\_days)) when self.total\_working\_days, otherwise 0.
      - Value choice on self.total\_working\_days — true gives ((flt(amount) × flt(self.payment\_days)) ÷ cint(self.total\_working\_days)), false gives 0.
    - Set self.data at struct\_row.abbr from flt(amount, struct\_row.precision).
  - Set is\_accrual\_component from (condition\_met and component\_type equals “earnings” and struct\_row.accrual\_component and hasattr(self, “benefit\_ledger\_components”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in condition\_met → component\_type equals “earnings” → struct\_row.accrual\_component → hasattr(self, “benefit\_ledger\_components”).
  - If is\_accrual\_component.
    - Evaluate self.append(“accrued\_benefits”, mapping(“salary\_component” → struct\_row.salary\_component, “amount” → amount)).
    - Evaluate self.benefit\_ledger\_components.append(mapping(“salary\_component” → struct\_row.salary\_component, “amount” → amount, “is\_accrual” → 1, “transaction\_type” → “Accrual”, …)).
- Otherwise.
  - Set remove\_if\_zero\_valued from Platform.get\_cached\_value(“Salary Component”, struct\_row.salary\_component, “remove\_if\_zero\_valued”).
  - Set default\_amount from 0.
  - If (amount or (struct\_row.amount\_based\_on\_formula and amount is distinct from no value) or (not remove\_if\_zero\_valued and amount is distinct from no value and not self.data at struct\_row.abbr)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in amount → (struct\_row.amount\_based\_on\_formula and amount is distinct from no value) → (not remove\_if\_zero\_valued and amount is distinct from no value and not self.data at struct\_row.abbr).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in struct\_row.amount\_based\_on\_formula → amount is distinct from no value.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not remove\_if\_zero\_valued → amount is distinct from no value → not self.data at struct\_row.abbr.
    - Set default\_amount from flt(struct\_row.default\_amount).
    - If not struct\_row.condition\_met.
      - Set default\_amount from flt(self.eval\_condition\_and\_formula(struct\_row, self.default\_data)).
    - Set self.default\_data at struct\_row.abbr from default\_amount.
    - Evaluate self.update\_component\_row(struct\_row, amount, component\_type, data = self.data, default\_amount = default\_amount, remove\_if\_zero\_valued = remove\_if\_zero\_valued).

If control reaches the end, it returns no value.

**Methods declared on this owner** [eval condition and formula](operations-016.md#op-373cd93d8ccd5a), [update component row](operations-016.md#op-36d2d47c0e70e2).

**Values supplied outside this operation** selected callable from getattr(self, “\_timesheet\_component”, no value) · configured or stored value from Platform.get\_cached\_value(“Salary Component”, struct\_row.salary\_component, “remove\_if\_zero\_valued”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L103) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L633) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L980)

<a id="op-2a477af237b7b2"></a>
### Salary Slip.get data for eval

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_data_for_evaluate`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Explicit result forms** a structured result.

**Local structure** 1 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L903) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L671) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1018)

<a id="op-373cd93d8ccd5a"></a>
### Salary Slip.eval condition and formula

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_evaluate_condition_and_formula`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, struct\_row, data.

**Explicit result forms** a value selected from the current context, no value.

**Locally raised failures** active or constructed exception.

**Local structure** 3 condition or selection sites, 0 statement loops and 3 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L1268) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L662) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1009)

<a id="op-35fbb37f32851e"></a>
### Salary Slip.add employee benefits

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_add_employee_benefits`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.payroll\_period.
  - Return no value.
- Set tuple(self.benefit\_details\_parent, self.benefit\_details\_doctype) from get\_benefits\_details\_parent(self.employee, self.payroll\_period.name, self.\_salary\_structure\_assignment.name).
- If not self.benefit\_details\_parent.
  - Return no value.
- Set SalaryComponent from Platform.qb.DocType(“Salary Component”).
- Set EmployeeBenefitDetail from Platform.qb.DocType(self.benefit\_details\_doctype).
- Set employee\_benefits from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.is\_flexible\_benefit equals 1).where(SalaryComponent.accrual\_component equals 1).run(as\_dict = true).
- If employee\_benefits.
  - Set employee\_benefits from self.get\_current\_period\_employee\_benefit\_amounts(employee\_benefits).
  - Evaluate self.add\_current\_period\_employee\_benefits(employee\_benefits).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get current period employee benefit amounts](operations-016.md#op-0532524757b6b3), [add current period employee benefits](operations-016.md#op-919d2c84ee8424).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L1812) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L631) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L978)

<a id="op-919d2c84ee8424"></a>
### Salary Slip.add current period employee benefits

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_add_current_period_employee_benefits`

**Inputs** self, employee\_benefits.

**Local steps**

- For each benefit in employee\_benefits.
  - <a id="op-919d2c84ee8424-guard-4"></a>If benefit.amount ≤ 0.
    - Continue with the next iteration or loop test.
  - Set earning\_component from get\_salary\_component\_data(benefit.salary\_component).
  - If not earning\_component.is\_flexible\_benefit.
    - Continue with the next iteration or loop test.
  - If benefit.is\_accrual.
    - Evaluate self.append(“accrued\_benefits”, mapping(“salary\_component” → benefit.salary\_component, “amount” → benefit.amount)).
  - Otherwise.
    - Evaluate self.update\_component\_row(earning\_component, benefit.amount, “earnings”).
  - Set transaction\_type from “Accrual” when benefit.is\_accrual, otherwise “Payout”.
    - Value choice on benefit.is\_accrual — true gives “Accrual”, false gives “Payout”.
  - Set remarks from “Pro rata flexible benefit accrual” when benefit.is\_accrual, otherwise “Flexible benefit payout”.
    - Value choice on benefit.is\_accrual — true gives “Pro rata flexible benefit accrual”, false gives “Flexible benefit payout”.
  - Evaluate self.benefit\_ledger\_components.append(mapping(“salary\_component” → benefit.salary\_component, “is\_accrual” → benefit.is\_accrual, “amount” → flt(benefit.amount), “transaction\_type” → transaction\_type, …)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison benefit.amount ≤ 0, benefit.amount = 0 selects the branch that continues with the next loop iteration. With benefit.amount = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-919d2c84ee8424-guard-4)

**Methods declared on this owner** [update component row](operations-016.md#op-36d2d47c0e70e2).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L2392) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L629) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L976)

<a id="op-0532524757b6b3"></a>
### Salary Slip.get current period employee benefit amounts

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_current_period_employee_benefit_amounts`

**Inputs** self, employee\_benefits.

**Declared result** dict.

**Explicit results** employee\_benefits.

**Local steps**

- Bind dependencies defaultdict.
- Set is\_last\_payroll\_cycle from false.
- If (self.payroll\_period and getdate(self.payroll\_period.end\_date) ≤ getdate(self.end\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.payroll\_period → getdate(self.payroll\_period.end\_date) ≤ getdate(self.end\_date).
  - Set is\_last\_payroll\_cycle from true.
- Set total\_sub\_periods from get\_period\_factor(self.employee, self.start\_date, self.end\_date, self.payroll\_frequency, …) at 0.
- Set ledger\_map from self.\_get\_benefit\_ledger\_entries(employee\_benefits).
- Set precision from Platform.get\_precision(“Employee Benefit Detail”, “amount”).
- For each benefit in employee\_benefits.
  - Set current\_period\_benefit from (benefit.yearly\_amount ÷ total\_sub\_periods) when total\_sub\_periods, otherwise 0.
    - Value choice on total\_sub\_periods — true gives (benefit.yearly\_amount ÷ total\_sub\_periods), false gives 0.
  - If benefit.depends\_on\_payment\_days.
    - Set current\_period\_benefit from ((flt(current\_period\_benefit) × flt(self.payment\_days)) ÷ cint(self.total\_working\_days)).
  - Set total\_accrued from ledger\_map at benefit.salary\_component.get(“Accrual”, 0).
  - Set total\_paid from ledger\_map at benefit.salary\_component.get(“Payout”, 0).
  - Set tuple(current\_period\_benefit, is\_accrual) from self.\_get\_benefit\_amount\_and\_transaction\_type(benefit, current\_period\_benefit, total\_accrued, total\_paid, …).
  - Set current\_period\_benefit from flt(current\_period\_benefit, precision).
  - If benefit.round\_to\_the\_nearest\_integer.
    - Set current\_period\_benefit from rounded((current\_period\_benefit or 0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in current\_period\_benefit → 0.
  - Set benefit.is\_accrual from is\_accrual.
  - Set benefit.amount from current\_period\_benefit.
- Return employee\_benefits.

**Methods declared on this owner** [get benefit ledger entries](operations-016.md#op-2295c7d6ce28c6), [get benefit amount and transaction type](operations-016.md#op-a31d7759202e9f).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L2897) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L670) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1017)

<a id="op-2295c7d6ce28c6"></a>
### Salary Slip.get benefit ledger entries

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_benefit_ledger_entries`

**Inputs** self, employee\_benefits.

**Record and data access** read “Employee Benefit Ledger” via get\_all.

**Explicit results** benefit\_ledger\_map.

**Local steps**

- Bind dependencies defaultdict.
- Set ledger\_entries from Platform.get\_all(“Employee Benefit Ledger”, filters = mapping(“employee” → self.employee, “salary\_component” → list(“in”, list of benefit.salary\_component for benefit drawn from employee\_benefits), “payrol ….
  - Draw benefit from employee\_benefits.
- Set benefit\_ledger\_map from defaultdict(deferred anonymous expression).
- For each entry in ledger\_entries.
  - Update benefit\_ledger\_map at entry at “salary\_component” at entry at “transaction\_type” using + entry at “amount”.
- Return benefit\_ledger\_map.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L3602) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L667) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1014)

<a id="op-a31d7759202e9f"></a>
### Salary Slip.get benefit amount and transaction type

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_benefit_amount_and_transaction_type`

**Inputs** self, benefit, current\_period\_benefit, total\_accrued, total\_paid, is\_last\_payroll\_cycle.

**Explicit results** tuple(current\_period\_benefit, is\_accrual).

**Local steps**

- Set is\_accrual from 1.
- If benefit.payout\_method equals “Accrue and payout at end of payroll period”.
  - Set tuple(current\_period\_benefit, is\_accrual) from self.\_get\_final\_period\_benefit\_payout(benefit, current\_period\_benefit, total\_accrued, total\_paid, …).
- Otherwise.
  - If benefit.payout\_method equals “Accrue per cycle, pay only on claim”.
    - Set tuple(current\_period\_benefit, is\_accrual) from self.\_get\_claim\_based\_benefit\_payout(benefit, current\_period\_benefit, total\_accrued, total\_paid, …).
- Return tuple(current\_period\_benefit, is\_accrual).

**Methods declared on this owner** [get final period benefit payout](operations-016.md#op-05a544fe62ef71), [get claim based benefit payout](operations-016.md#op-c2c5ea695f9f7f).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L3952) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L666) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1013)

<a id="op-05a544fe62ef71"></a>
### Salary Slip.get final period benefit payout

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_final_period_benefit_payout`

**Inputs** self, benefit, current\_period\_benefit, total\_accrued, total\_paid, is\_last\_payroll\_cycle.

**Explicit results** tuple(current\_period\_benefit, is\_accrual).

**Local steps**

- Set is\_accrual from 1.
- Set benefit\_claims from list of row for row drawn from self.earnings where (row.salary\_component equals benefit.salary\_component and getattr(row, “additional\_salary”, no value)).
  - Draw row from self.earnings, keep a combination only if ((row.salary\_component equals benefit.salary\_component and getattr(row, “additional\_salary”, no value))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.salary\_component equals benefit.salary\_component → getattr(row, “additional\_salary”, no value).
- Set claimed\_amount from sum(generator of row.amount for row drawn from benefit\_claims) when benefit\_claims, otherwise 0.
  - Value choice on benefit\_claims — true gives sum(generator of row.amount for row drawn from benefit\_claims), false gives 0.
  - Draw row from benefit\_claims.
- Update total\_paid using + claimed\_amount.
- If 0 &lt; (benefit.yearly\_amount − total\_accrued) &lt; current\_period\_benefit.
  - Compare adjacent operands in order, stopping at the first false comparison in 0 &lt; (benefit.yearly\_amount − total\_accrued) &lt; current\_period\_benefit.
  - Set current\_period\_benefit from (benefit.yearly\_amount − total\_accrued).
- If is\_last\_payroll\_cycle.
  - Set current\_period\_benefit from max(((total\_accrued + current\_period\_benefit) − total\_paid), 0).
  - Set is\_accrual from 0.
- Return tuple(current\_period\_benefit, is\_accrual).

**Values supplied outside this operation** selected callable from getattr(row, “additional\_salary”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L4212) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L677) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1024)

<a id="op-c2c5ea695f9f7f"></a>
### Salary Slip.get claim based benefit payout

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_claim_based_benefit_payout`

**Inputs** self, benefit, current\_period\_benefit, total\_accrued, total\_paid, is\_last\_payroll\_cycle.

**Explicit results** tuple(current\_period\_benefit, is\_accrual).

**Local steps**

- Set is\_accrual from 1.
- Set benefit\_claims from list of row for row drawn from self.earnings where (row.salary\_component equals benefit.salary\_component and getattr(row, “additional\_salary”, no value)).
  - Draw row from self.earnings, keep a combination only if ((row.salary\_component equals benefit.salary\_component and getattr(row, “additional\_salary”, no value))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.salary\_component equals benefit.salary\_component → getattr(row, “additional\_salary”, no value).
- Set claimed\_amount from sum(generator of row.amount for row drawn from benefit\_claims) when benefit\_claims, otherwise 0.
  - Value choice on benefit\_claims — true gives sum(generator of row.amount for row drawn from benefit\_claims), false gives 0.
  - Draw row from benefit\_claims.
- Update total\_paid using + claimed\_amount.
- If total\_paid &gt; total\_accrued.
  - Update current\_period\_benefit using − (total\_paid − total\_accrued).
- If 0 &lt; (benefit.yearly\_amount − total\_accrued) &lt; current\_period\_benefit.
  - Compare adjacent operands in order, stopping at the first false comparison in 0 &lt; (benefit.yearly\_amount − total\_accrued) &lt; current\_period\_benefit.
  - Set current\_period\_benefit from (benefit.yearly\_amount − total\_accrued).
- If (is\_last\_payroll\_cycle and benefit.final\_cycle\_accrual\_payout).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_last\_payroll\_cycle → benefit.final\_cycle\_accrual\_payout.
  - Set current\_period\_benefit from max(((total\_accrued + current\_period\_benefit) − total\_paid), 0).
  - Set is\_accrual from 0.
- Return tuple(current\_period\_benefit, is\_accrual).

**Values supplied outside this operation** selected callable from getattr(row, “additional\_salary”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L4605) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L668) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1015)

<a id="op-52c567971fe769"></a>
### Salary Slip.add additional salary components

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_add_additional_salary_components`

**Inputs** self, component\_type.

**Record and data access** read “Salary Component” via get\_cached\_value.

**Local steps**

- Set additional\_salaries from get\_additional\_salaries(self.employee, self.start\_date, self.end\_date, component\_type).
- For each additional\_salary in additional\_salaries.
  - Set component\_data from get\_salary\_component\_data(additional\_salary.component).
  - Set remove\_if\_zero\_valued from (Platform.get\_cached\_value(“Salary Component”, additional\_salary.component, “remove\_if\_zero\_valued”) and not component\_data.variable\_based\_on\_taxable\_salary).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_cached\_value(“Salary Component”, additional\_salary.component, “remove\_if\_zero\_valued”) → not component\_data.variable\_based\_on\_taxable\_salary.
  - If (flt(additional\_salary.amount) equals 0 and remove\_if\_zero\_valued and not additional\_salary.overwrite).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(additional\_salary.amount) equals 0 → remove\_if\_zero\_valued → not additional\_salary.overwrite.
    - Continue with the next iteration or loop test.
  - Evaluate self.update\_component\_row(component\_data, additional\_salary.amount, component\_type, additional\_salary, is\_recurring = additional\_salary.is\_recurring, remove\_if\_zero\_valued = remove\_if\_zero\_valued).
  - If (component\_type equals “earnings” and hasattr(self, “benefit\_ledger\_components”) and flt(additional\_salary.amount)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in component\_type equals “earnings” → hasattr(self, “benefit\_ledger\_components”) → flt(additional\_salary.amount).
    - If ((additional\_salary.ref\_doctype equals “Employee Benefit Claim” and component\_data.is\_flexible\_benefit) or component\_data.accrual\_component).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (additional\_salary.ref\_doctype equals “Employee Benefit Claim” and component\_data.is\_flexible\_benefit) → component\_data.accrual\_component.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in additional\_salary.ref\_doctype equals “Employee Benefit Claim” → component\_data.is\_flexible\_benefit.
      - If additional\_salary.ref\_doctype equals “Employee Benefit Claim”.
        - Set remarks from formatted text Payout against Employee Benefit Claim {additional\_salary.ref\_docname}.
        - Set flexible\_benefit from 1.
      - Otherwise.
        - Set remarks from “Accrual Component payout via Additional Salary”.
        - Set flexible\_benefit from 0.
      - Evaluate self.benefit\_ledger\_components.append(mapping(“salary\_component” → additional\_salary.component, “amount” → additional\_salary.amount, “is\_accrual” → 0, “transaction\_type” → “Payout”, …)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update component row](operations-016.md#op-36d2d47c0e70e2).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Salary Component”, additional\_salary.component, “remove\_if\_zero\_valued”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L102) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L628) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L975)

<a id="op-a9c60b47c100ac"></a>
### Salary Slip.add tax components

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_add_tax_components`

**Inputs** self.

**State and service calls** msgprint with translated “Added tax components from the Salary Component master as the salary structure didn't have any tax component.”.

**Explicit results** no value.

**Local steps**

- Set tuple(tax\_components, self.other\_deduction\_components) from tuple(list(), list()).
- For each d in self.\_evaluated\_components at “deductions”.
  - If (d.variable\_based\_on\_taxable\_salary equals 1 and not d.formula and not flt(d.amount)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.variable\_based\_on\_taxable\_salary equals 1 → not d.formula → not flt(d.amount).
    - Evaluate tax\_components.append(d.salary\_component).
  - Otherwise.
    - Evaluate self.other\_deduction\_components.append(d.salary\_component).
- If not tax\_components.
  - Set tax\_components from list of d.salary\_component for d drawn from self.get(“deductions”) where d.variable\_based\_on\_taxable\_salary.
    - Draw d from self.get(“deductions”), keep a combination only if (d.variable\_based\_on\_taxable\_salary).
- If (self.is\_new() and not tax\_components).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → not tax\_components.
  - Set tax\_components from self.get\_tax\_components().
  - Evaluate Platform.msgprint(translated “Added tax components from the Salary Component master as the salary structure didn't have any tax component.”, indicator = “blue”, alert = true).
- Set self.\_component\_based\_variable\_tax from mapping().
- If (tax\_components and self.payroll\_period and self.salary\_structure).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax\_components → self.payroll\_period → self.salary\_structure.
  - Set self.tax\_slab from self.get\_income\_tax\_slabs().
  - Evaluate self.compute\_taxable\_earnings\_for\_year().
- If self.handle\_additional\_salary\_tax\_component().
  - Evaluate self.\_component\_based\_variable\_tax.setdefault(self.additional\_salary\_component, mapping()).
  - Evaluate self.calculate\_variable\_tax(self.additional\_salary\_component, true).
  - Return no value.
- For each tax\_component in tax\_components.
  - Evaluate self.\_component\_based\_variable\_tax.setdefault(tax\_component, mapping()).
  - Evaluate self.calculate\_variable\_based\_on\_taxable\_salary(tax\_component).
  - If self.\_component\_based\_variable\_tax at tax\_component.
    - Set tax\_amount from self.\_component\_based\_variable\_tax at tax\_component at “current\_tax\_amount”.
    - Set tax\_row from get\_salary\_component\_data(tax\_component).
    - Evaluate self.update\_component\_row(tax\_row, tax\_amount, “deductions”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get tax components](operations-016.md#op-d78c954596eb40), [get income tax slabs](operations-016.md#op-36da12e83616cd), [compute taxable earnings for year](operations-015.md#op-3604f62a437076), [handle additional salary tax component](operations-016.md#op-387507b6fb5f4c), [calculate variable tax](operations-016.md#op-6f313e0df7b241), [calculate variable based on taxable salary](operations-016.md#op-b39d606f61f94c), [update component row](operations-016.md#op-36d2d47c0e70e2).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L5691) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L635) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L982)

<a id="op-d78c954596eb40"></a>
### Salary Slip.get tax components

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_tax_components`

**Inputs** self.

**Declared result** list.

**Explicit results** tax\_components.get(self.company, default\_tax\_components).

**Local steps**

- Set tax\_components from Platform.cache().get\_value(TAX\_COMPONENTS\_BY\_COMPANY, self.\_fetch\_tax\_components\_by\_company).
- Set default\_tax\_components from tax\_components.get(“default”, list()).
- Return tax\_components.get(self.company, default\_tax\_components).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L6499) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L696) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1043)

<a id="op-bcef6cd549ec9c"></a>
### Salary Slip.fetch tax components by company

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_fetch_tax_components_by_company`

**Inputs** self.

**Declared result** dict.

**Explicit results** tax\_components.

**Local steps**

- Set tax\_components from mapping().
- Set sc from Platform.qb.DocType(“Salary Component”).
- Set sca from Platform.qb.DocType(“Salary Component Account”).
- Set components from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract.variable\_based\_on\_taxable\_salary equals 1).where(sc.disabled equals 0).ru ….
- For each component in components.
  - Set key from (component.company or “default”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in component.company → “default”.
  - Evaluate tax\_components.setdefault(key, list()).
  - Evaluate tax\_components at key.append(component.name).
- Return tax\_components.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L6648) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L663) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1010)

<a id="op-387507b6fb5f4c"></a>
### Salary Slip.handle additional salary tax component

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_handle_additional_salary_tax_component`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Additional Salary” via get\_value.

**Explicit results** false · true.

**Local steps**

- Set component from next(generator of d for d drawn from self.get(“deductions”) where (d.variable\_based\_on\_taxable\_salary and d.additional\_salary), no value).
  - Draw d from self.get(“deductions”), keep a combination only if ((d.variable\_based\_on\_taxable\_salary and d.additional\_salary)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.variable\_based\_on\_taxable\_salary → d.additional\_salary.
- If not component.
  - Return false.
- Set additional\_salary from Platform.db.get\_value(“Additional Salary”, component.additional\_salary, list(“amount”, “overwrite\_salary\_structure\_amount”), as\_dict = 1).
- Set self.additional\_salary\_amount from additional\_salary.amount.
- Set self.additional\_salary\_component from component.salary\_component.
- If additional\_salary.overwrite\_salary\_structure\_amount.
  - Return true.
- Otherwise.
  - Evaluate self.get(“deductions”, list()).remove(component).
  - Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0126.json#L7089) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L704) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1051)

<a id="op-36d2d47c0e70e2"></a>
### Salary Slip.update component row

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_update_component_row`

**Inputs** self, component\_data, amount, component\_type, additional\_salary = no value, is\_recurring = 0, data = no value, default\_amount = no value, remove\_if\_zero\_valued = no value.

**Explicit results** no value.

**Local steps**

- Set component\_row from no value.
- For each d in self.get(component\_type).
  - If d.salary\_component differs from component\_data.salary\_component.
    - Continue with the next iteration or loop test.
  - If ((not d.additional\_salary and (not additional\_salary or additional\_salary.overwrite)) or (additional\_salary and additional\_salary.name equals d.additional\_salary)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not d.additional\_salary and (not additional\_salary or additional\_salary.overwrite)) → (additional\_salary and additional\_salary.name equals d.additional\_salary).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.additional\_salary → (not additional\_salary or additional\_salary.overwrite).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not additional\_salary → additional\_salary.overwrite.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in additional\_salary → additional\_salary.name equals d.additional\_salary.
    - Set component\_row from d.
    - Leave the innermost loop without its normal-exhaustion alternative.
- If (additional\_salary and additional\_salary.overwrite).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in additional\_salary → additional\_salary.overwrite.
  - Evaluate self.set(component\_type, list of d for d drawn from self.get(component\_type) where (d.salary\_component differs from component\_data.salary\_component or (d.additional\_salary and additional\_salary.name differ ….
    - Draw d from self.get(component\_type), keep a combination only if ((d.salary\_component differs from component\_data.salary\_component or (d.additional\_salary and additional\_salary.name differs from d.additional\_salary) or d equals component\_row)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.salary\_component differs from component\_data.salary\_component → (d.additional\_salary and additional\_salary.name differs from d.additional\_salary) → d equals component\_row.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.additional\_salary → additional\_salary.name differs from d.additional\_salary.
- If not component\_row.
  - If (not (amount or default\_amount) and remove\_if\_zero\_valued).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not (amount or default\_amount) → remove\_if\_zero\_valued.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in amount → default\_amount.
    - Return no value.
  - Set component\_row from self.append(component\_type).
  - For each attr in tuple(“depends\_on\_payment\_days”, “salary\_component”, “abbr”, “do\_not\_include\_in\_total”, …).
    - Evaluate component\_row.set(attr, component\_data.get(attr)).
- If additional\_salary.
  - If additional\_salary.overwrite.
    - Set component\_row.additional\_amount from flt((flt(amount) − flt(component\_row.get(“default\_amount”, 0))), component\_row.precision(“additional\_amount”)).
  - Otherwise.
    - Set component\_row.default\_amount from 0.
    - Set component\_row.additional\_amount from amount.
  - Set component\_row.is\_recurring\_additional\_salary from is\_recurring.
  - Set component\_row.additional\_salary from additional\_salary.name.
  - Set component\_row.deduct\_full\_tax\_on\_selected\_payroll\_date from additional\_salary.deduct\_full\_tax\_on\_selected\_payroll\_date.
- Otherwise.
  - Set component\_row.default\_amount from (default\_amount or amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in default\_amount → amount.
  - Set component\_row.additional\_amount from 0.
  - Set component\_row.deduct\_full\_tax\_on\_selected\_payroll\_date from component\_data.deduct\_full\_tax\_on\_selected\_payroll\_date.
- Set component\_row.amount from amount.
- Set skip\_payment\_days\_adjustment from ((additional\_salary and additional\_salary.get(“ref\_doctype”) belongs to list(“Arrear”, “Payroll Correction”, “Employee Benefit Claim”)) or component\_row.accrual\_component).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (additional\_salary and additional\_salary.get(“ref\_doctype”) belongs to list(“Arrear”, “Payroll Correction”, “Employee Benefit Claim”)) → component\_row.accrual\_component.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in additional\_salary → additional\_salary.get(“ref\_doctype”) belongs to list(“Arrear”, “Payroll Correction”, “Employee Benefit Claim”).
- If not skip\_payment\_days\_adjustment.
  - Evaluate self.update\_component\_amount\_based\_on\_payment\_days(component\_row, remove\_if\_zero\_valued).
- If data.
  - Set data at component\_row.abbr from component\_row.amount.

If control reaches the end, it returns no value.

**Methods declared on this owner** [update component amount based on payment days](operations-016.md#op-3f8e4566e04634).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L730) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1077)

<a id="op-3f8e4566e04634"></a>
### Salary Slip.update component amount based on payment days

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_update_component_amount_based_on_payment_days`

**Inputs** self, component\_row, remove\_if\_zero\_valued = no value.

**Local steps**

- Set component\_row.amount from self.get\_amount\_based\_on\_payment\_days(component\_row) at 0.
- If (component\_row.amount equals 0 and remove\_if\_zero\_valued).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in component\_row.amount equals 0 → remove\_if\_zero\_valued.
  - Evaluate self.remove(component\_row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get amount based on payment days](operations-017.md#op-c455f878229abb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L1186) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L729) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1076)

<a id="op-08fb727f8c9329"></a>
### Salary Slip.set precision for component amounts

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_set_precision_for_component_amounts`

**Inputs** self.

**Local steps**

- For each component\_type in COMPONENT\_PARENTFIELDS.
  - For each component\_row in self.get(component\_type).
    - Set component\_row.amount from flt(component\_row.amount, component\_row.precision(“amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L1336) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L724) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1071)

<a id="op-b39d606f61f94c"></a>
### Salary Slip.calculate variable based on taxable salary

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_calculate_variable_based_on_taxable_salary`

**Inputs** self, tax\_component.

**State and service calls** msgprint with translated “Start and end dates not in a valid Payroll Period, cannot calculate {0}.”.format(tax\_component).

**Explicit results** no value · self.calculate\_variable\_tax(tax\_component).

**Local steps**

- If not self.payroll\_period.
  - Evaluate Platform.msgprint(translated “Start and end dates not in a valid Payroll Period, cannot calculate {0}.”.format(tax\_component)).
  - Return no value.
- Return self.calculate\_variable\_tax(tax\_component).

**Methods declared on this owner** [calculate variable tax](operations-016.md#op-6f313e0df7b241).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L1471) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L645) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L992)

<a id="op-6f313e0df7b241"></a>
### Salary Slip.calculate variable tax

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_calculate_variable_tax`

**Inputs** self, tax\_component, has\_additional\_salary\_tax\_component = false.

**Local steps**

- Set self.previous\_total\_paid\_taxes from self.get\_tax\_paid\_in\_period(self.payroll\_period.start\_date, self.start\_date, tax\_component).
- Set tuple(eval\_locals, default\_data) from self.get\_data\_for\_eval().
- Set tuple(self.total\_structured\_tax\_amount, \_\_) from calculate\_tax\_by\_tax\_slab(self.total\_taxable\_earnings\_without\_full\_tax\_addl\_components, self.tax\_slab, self.whitelisted\_globals, eval\_locals).
- Set payment\_days\_share from 1.
- If not has\_additional\_salary\_tax\_component.
  - Set tax\_row from (next(generator of d for d drawn from self.get(“deductions”) where (d.salary\_component equals tax\_component and not d.additional\_salary), no value) or get\_salary\_component\_data(tax\_component)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in next(generator of d for d drawn from self.get(“deductions”) where (d.salary\_component equals tax\_component and not d.additional\_salary), no value) → get\_salary\_component\_data(tax\_component).
    - Draw d from self.get(“deductions”), keep a combination only if ((d.salary\_component equals tax\_component and not d.additional\_salary)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.salary\_component equals tax\_component → not d.additional\_salary.
  - If (cint(tax\_row.depends\_on\_payment\_days) and cint(self.total\_working\_days)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(tax\_row.depends\_on\_payment\_days) → cint(self.total\_working\_days).
    - Set payment\_days\_share from (flt(self.payment\_days) ÷ cint(self.total\_working\_days)).
- Set remaining\_sub\_periods from ((self.remaining\_sub\_periods − 1) + payment\_days\_share).
- If has\_additional\_salary\_tax\_component.
  - Set self.current\_structured\_tax\_amount from self.additional\_salary\_amount.
- Otherwise.
  - If remaining\_sub\_periods &gt; 0.
    - Set self.current\_structured\_tax\_amount from ((self.total\_structured\_tax\_amount − self.previous\_total\_paid\_taxes) ÷ remaining\_sub\_periods).
  - Otherwise.
    - Set self.current\_structured\_tax\_amount from 0.0.
- Set self.full\_tax\_on\_additional\_earnings from 0.0.
- If self.current\_additional\_earnings\_with\_full\_tax.
  - Set tuple(self.total\_tax\_amount, \_\_) from calculate\_tax\_by\_tax\_slab(self.total\_taxable\_earnings, self.tax\_slab, self.whitelisted\_globals, eval\_locals).
  - Set self.full\_tax\_on\_additional\_earnings from (self.total\_tax\_amount − self.total\_structured\_tax\_amount).
- Set self.current\_tax\_amount from max(0, flt(self.current\_structured\_tax\_amount when has\_additional\_salary\_tax\_component, otherwise (self.current\_structured\_tax\_amount + self.full\_tax\_on\_additional\_earnings))).
  - Value choice on has\_additional\_salary\_tax\_component — true gives self.current\_structured\_tax\_amount, false gives (self.current\_structured\_tax\_amount + self.full\_tax\_on\_additional\_earnings).
- Set self.current\_tax\_amount\_for\_payment\_days from flt((self.current\_tax\_amount × payment\_days\_share)).
- Evaluate self.\_component\_based\_variable\_tax at tax\_component.update(mapping(“previous\_total\_paid\_taxes” → self.previous\_total\_paid\_taxes, “total\_structured\_tax\_amount” → self.total\_structured\_tax\_amount, “current\_s ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get tax paid in period](operations-017.md#op-89eddf3d9f1c8a), [get data for eval](operations-016.md#op-2a477af237b7b2).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L107) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L646) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L993)

<a id="op-36da12e83616cd"></a>
### Salary Slip.get income tax slabs

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_income_tax_slabs`

**Inputs** self.

**Record and data access** resolve a document from “Income Tax Slab” via get\_cached\_doc.

**Explicit results** income\_tax\_slab\_doc.

**Explicit failure paths** validation helper — translated “Income Tax Slab not set in Salary Structure Assignment: {0}”.format(get\_link\_to\_form(“Salary Structure Assignment”, self.\_salary\_structure\_assignment.name)) · validation helper — translated “Income Tax Slab: {0} is disabled”.format(income\_tax\_slab) · validation helper — translated “Income Tax Slab must be effective on or before Payroll Period Start Date: {0}”.format(self.payroll\_period.start\_date).

**Local steps**

- Set income\_tax\_slab from self.\_salary\_structure\_assignment.income\_tax\_slab.
- If not income\_tax\_slab.
  - Call the validation error handler Platform.throw(translated “Income Tax Slab not set in Salary Structure Assignment: {0}”.format(get\_link\_to\_form(“Salary Structure Assignment”, self.\_salary\_structure\_assignment.name)), title = translated “ ….
- Set income\_tax\_slab\_doc from Platform.get\_cached\_doc(“Income Tax Slab”, income\_tax\_slab).
- If income\_tax\_slab\_doc.disabled.
  - Call the validation error handler Platform.throw(translated “Income Tax Slab: {0} is disabled”.format(income\_tax\_slab)).
- If getdate(income\_tax\_slab\_doc.effective\_from) &gt; getdate(self.payroll\_period.start\_date).
  - Call the validation error handler Platform.throw(translated “Income Tax Slab must be effective on or before Payroll Period Start Date: {0}”.format(self.payroll\_period.start\_date)).
- Return income\_tax\_slab\_doc.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Income Tax Slab”, income\_tax\_slab).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L2252) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L685) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1032)

<a id="op-b5cb8c30ecb706"></a>
### Salary Slip.get taxable earnings for prev period

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_taxable_earnings_for_previous_period`

**Inputs** self, start\_date, end\_date, allow\_tax\_exemption = false.

**Explicit results** tuple(((taxable\_earnings + opening\_taxable\_earning) − exempted\_amount), exempted\_amount).

**Local steps**

- Set exempted\_amount from 0.
- Set taxable\_earnings from self.get\_salary\_slip\_details(start\_date, end\_date, parentfield = “earnings”, is\_tax\_applicable = 1).
- If allow\_tax\_exemption.
  - Set exempted\_amount from self.get\_salary\_slip\_details(start\_date, end\_date, parentfield = “deductions”, exempted\_from\_income\_tax = 1).
- Set opening\_taxable\_earning from self.get\_opening\_for(“taxable\_earnings\_till\_date”, start\_date, end\_date).
- Return tuple(((taxable\_earnings + opening\_taxable\_earning) − exempted\_amount), exempted\_amount).

**Methods declared on this owner** [get salary slip details](operations-016.md#op-3d9b68950fbac3), [get opening for](operations-016.md#op-0c89b467a31afe).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L2663) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L699) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1046)

<a id="op-0c89b467a31afe"></a>
### Salary Slip.get opening for

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_opening_for`

**Inputs** self, field\_to\_select, start\_date, end\_date.

**Explicit results** 0 · (self.\_salary\_structure\_assignment.get(field\_to\_select) or 0).

**Local steps**

- If self.\_salary\_structure\_assignment.from\_date &lt; self.payroll\_period.start\_date.
  - Return 0.
- Return (self.\_salary\_structure\_assignment.get(field\_to\_select) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_salary\_structure\_assignment.get(field\_to\_select) → 0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L2939) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L691) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1038)

<a id="op-3d9b68950fbac3"></a>
### Salary Slip.get salary slip details

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_get_salary_slip_details`

**Inputs** self, start\_date, end\_date, parentfield, salary\_component = no value, is\_tax\_applicable = no value, is\_flexible\_benefit = 0, exempted\_from\_income\_tax = 0, variable\_based\_on\_taxable\_salary = 0, field\_to\_select = “amount”.

**Explicit results** flt(result at 0 at 0) when result, otherwise 0.0.

**Local steps**

- Set ss from Platform.qb.DocType(“Salary Slip”).
- Set sd from Platform.qb.DocType(“Salary Detail”).
- Set field from sd.amount when field\_to\_select equals “amount”, otherwise sd.additional\_amount.
  - Value choice on field\_to\_select equals “amount” — true gives sd.amount, false gives sd.additional\_amount.
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.employee equals nested operand in the contract.employee).where(ss.start\_date.between(start\_date, end\_date ….
- If is\_tax\_applicable is distinct from no value.
  - Set query from query.where(sd.is\_tax\_applicable equals is\_tax\_applicable).
- If exempted\_from\_income\_tax.
  - Set query from query.where(sd.exempted\_from\_income\_tax equals exempted\_from\_income\_tax).
- If variable\_based\_on\_taxable\_salary.
  - Set query from query.where(sd.variable\_based\_on\_taxable\_salary equals variable\_based\_on\_taxable\_salary).
- If salary\_component.
  - Set query from query.where(sd.salary\_component equals salary\_component).
- Set result from query.run().
- Return flt(result at 0 at 0) when result, otherwise 0.0.
  - Value choice on result — true gives flt(result at 0 at 0), false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0127.json#L3073) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L693) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1040)
