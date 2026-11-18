# Payroll and benefits · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Employee benefit application

[Record definition](../../../../data/record-types/employee_benefit_application.json)

<a id="op-89350c2198ed5e"></a>
### Employee Benefit Application.validate max benefit

`operation_workforce_payroll_record_definitions_employee_benefit_application_business_behavior_employee_benefit_application_validate_maximum_benefit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Benefit amount of component {0} should be greater than 0”.format(benefit.salary\_component) · validation helper — translated “Benefit amount of component {0} exceeds {1}”.format(benefit.salary\_component, benefit.max\_benefit\_amount) · validation helper — translated “Sum of benefit amounts {0} exceeds maximum limit of {1}”.format(total\_benefit\_amount, self.max\_benefits).

**Local steps**

- Set total\_benefit\_amount from 0.
- For each benefit in self.employee\_benefits.
  - If (not benefit.amount or benefit.amount ≤ 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not benefit.amount → benefit.amount ≤ 0.
    - Call the validation error handler Platform.throw(translated “Benefit amount of component {0} should be greater than 0”.format(benefit.salary\_component)).
  - Otherwise.
    - If benefit.amount &gt; benefit.max\_benefit\_amount.
      - Call the validation error handler Platform.throw(translated “Benefit amount of component {0} exceeds {1}”.format(benefit.salary\_component, benefit.max\_benefit\_amount)).
  - Update total\_benefit\_amount using + flt(benefit.amount).
- If rounded(total\_benefit\_amount, 2) &gt; self.max\_benefits.
  - Call the validation error handler Platform.throw(translated “Sum of benefit amounts {0} exceeds maximum limit of {1}”.format(total\_benefit\_amount, self.max\_benefits)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0108.json#L6520) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L366) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L715)

<a id="op-056182be398b93"></a>
### Employee Benefit Application.validate duplicate on payroll period

`operation_workforce_payroll_record_definitions_employee_benefit_application_business_behavior_employee_benefit_application_validate_duplicate_on_payroll_period`

**Inputs** self.

**Record and data access** read “Employee Benefit Application” via exists.

**Explicit failure paths** validation helper — translated “Employee {0} already submitted an application {1} for the payroll period {2}”.format(self.employee, application, self.payroll\_period).

**Local steps**

- Set application from Platform.db.exists(“Employee Benefit Application”, mapping(“employee” → self.employee, “payroll\_period” → self.payroll\_period, “docstatus” → 1)).
- If application.
  - Call the validation error handler Platform.throw(translated “Employee {0} already submitted an application {1} for the payroll period {2}”.format(self.employee, application, self.payroll\_period)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0108.json#L6914) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L365) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L714)

<a id="op-5e3b26834f35aa"></a>
### Employee Benefit Application.set benefit components and currency

`operation_workforce_payroll_record_definitions_employee_benefit_application_business_behavior_employee_benefit_application_set_benefit_components_and_currency`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Record and data access** read “Salary Structure Assignment” via get\_value.

**Explicit failure paths** validation helper — translated “No Salary Structure Assignment found for employee {0} on date {1}”.format(self.employee, cstr(self.date)).

**Local steps**

- Set self.employee\_benefits from list().
- Set salary\_structure\_assignment from get\_salary\_structure\_assignment(self.employee, self.date).
- If not salary\_structure\_assignment.
  - Call the validation error handler Platform.throw(translated “No Salary Structure Assignment found for employee {0} on date {1}”.format(self.employee, cstr(self.date))).
- Set EmployeeBenefitDetail from Platform.qb.DocType(“Employee Benefit Detail”).
- Set employee\_benefits from nested operand in the contract(nested operand in the contract).select(EmployeeBenefitDetail.salary\_component, EmployeeBenefitDetail.amount).where(EmployeeBenefitDetail.parent equals salary\_structure\_assign ….
- If employee\_benefits.
  - Set tuple(max\_benefits, currency) from Platform.db.get\_value(“Salary Structure Assignment”, salary\_structure\_assignment, list(“max\_benefits”, “currency”)).
  - Set self.max\_benefits from max\_benefits.
  - Set self.currency from currency.
  - For each benefit in employee\_benefits.
    - Evaluate self.append(“employee\_benefits”, mapping(“salary\_component” → benefit.salary\_component, “max\_benefit\_amount” → benefit.amount)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L363) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L712)

## Record · Employee benefit claim

[Record definition](../../../../data/record-types/employee_benefit_claim.json)

<a id="op-e08f25c1ca1b0d"></a>
### Employee Benefit Claim.validate

`operation_workforce_payroll_record_definitions_employee_benefit_claim_business_behavior_employee_benefit_claim_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_date\_and\_benefit\_claim\_amount().
- Evaluate self.validate\_duplicate\_claim().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate date and benefit claim amount](operations-003.md#op-dc17ac6ed5b24d), [validate duplicate claim](operations-003.md#op-e0891db71aaf01).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L567) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L374) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L723)

<a id="op-dc17ac6ed5b24d"></a>
### Employee Benefit Claim.validate date and benefit claim amount

`operation_workforce_payroll_record_definitions_employee_benefit_claim_business_behavior_employee_benefit_claim_validate_date_and_benefit_claim_amount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Payroll date cannot be in the past. This is to ensure that claims are made for the current or future payroll …” · validation helper — translated “Claimed amount of employee {0} should be greater than 0”.format(self.employee) · validation helper — translated “Claimed amount of employee {0} exceeds maximum amount eligible for claim {1}”.format(self.employee, self.max\_amount\_eligible).

**Local steps**

- If getdate(self.payroll\_date) &lt; getdate().
  - Call the validation error handler Platform.throw(translated “Payroll date cannot be in the past. This is to ensure that claims are made for the current or future payroll …”).
- <a id="op-dc17ac6ed5b24d-guard-9"></a>If self.claimed\_amount ≤ 0.
  - Call the validation error handler Platform.throw(translated “Claimed amount of employee {0} should be greater than 0”.format(self.employee)).
- If self.claimed\_amount &gt; self.max\_amount\_eligible.
  - Call the validation error handler Platform.throw(translated “Claimed amount of employee {0} exceeds maximum amount eligible for claim {1}”.format(self.employee, self.max\_amount\_eligible)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.claimed\_amount ≤ 0, self.claimed\_amount = 0 selects the branch that calls the validation-error handler with translated “Claimed amount of employee {0} should be greater than 0”.format(self.employee). With self.claimed\_amount = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-dc17ac6ed5b24d-guard-9)

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L638) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L375) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L724)

<a id="op-e0891db71aaf01"></a>
### Employee Benefit Claim.validate duplicate claim

`operation_workforce_payroll_record_definitions_employee_benefit_claim_business_behavior_employee_benefit_claim_validate_duplicate_claim`

**Inputs** self.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set existing\_claim from self.get\_existing\_claim\_for\_month().
- If existing\_claim.
  - Set msg from translated “Employee {0} has already claimed the benefit '{1}' for {2} ({3}).&lt;br&gt;To prevent overpayments, only one claim …”.format(Platform.bold(self.employee), Platform.bold(self.earning\_component), Platf ….
  - Call the validation error handler Platform.throw(msg, title = translated “Duplicate Claim Detected”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get existing claim for month](operations-003.md#op-8ead36cac6a6ed).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L934) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L376) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L725)

<a id="op-cfffdad42fcee3"></a>
### Employee Benefit Claim.on submit

`operation_workforce_payroll_record_definitions_employee_benefit_claim_business_behavior_employee_benefit_claim_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.create\_additional\_salary().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create additional salary](operations-003.md#op-df5e73e6397e6e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L1234) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L372) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L721)

<a id="op-8ead36cac6a6ed"></a>
### Employee Benefit Claim.get existing claim for month

`operation_workforce_payroll_record_definitions_employee_benefit_claim_business_behavior_employee_benefit_claim_get_existing_claim_for_month`

**Inputs** self.

**Record and data access** read “Employee Benefit Claim” via get\_value.

**Explicit results** Platform.db.get\_value(“Employee Benefit Claim”, mapping(“employee” → self.employee, “earning\_component” → self.earning\_component, “payroll\_date” → list(“between”, list(month\_start\_date, month\_end\_date)), “ ….

**Local steps**

- Set month\_start\_date from Platform.utils.get\_first\_day(self.payroll\_date).
- Set month\_end\_date from Platform.utils.get\_last\_day(self.payroll\_date).
- Return Platform.db.get\_value(“Employee Benefit Claim”, mapping(“employee” → self.employee, “earning\_component” → self.earning\_component, “payroll\_date” → list(“between”, list(month\_start\_date, month\_end\_date)), “ ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L1285) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L371) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L720)

<a id="op-df5e73e6397e6e"></a>
### Employee Benefit Claim.create additional salary

`operation_workforce_payroll_record_definitions_employee_benefit_claim_business_behavior_employee_benefit_claim_create_additional_salary`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Additional Salary”, “company” → self.company, “employee” → self.employee, “currency” → self.currency, …) via get\_doc.

**State and service calls** call submit on Platform.get\_doc(mapping(“doctype” → “Additional Salary”, “company” → self.company, “employee” → self.employee, “currency” → self.currency, …)).

**Local steps**

- Evaluate Platform.get\_doc(mapping(“doctype” → “Additional Salary”, “company” → self.company, “employee” → self.employee, “currency” → self.currency, …)).submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L1560) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L367) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L716)

<a id="op-10e1cf126a2690"></a>
### Employee Benefit Claim.get benefit details

`operation_workforce_payroll_record_definitions_employee_benefit_claim_business_behavior_employee_benefit_claim_get_benefit_details`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Local steps**

- Bind dependencies get\_max\_claim\_eligible.
- Set payroll\_period from get\_payroll\_period(self.payroll\_date, self.payroll\_date, self.company).get(“name”).
- Set salary\_structure\_assignment from get\_salary\_structure\_assignment(self.employee, self.payroll\_date).
- Set component\_details from self.get\_component\_details(payroll\_period, salary\_structure\_assignment).
- Set yearly\_benefit from 0.
- Set claimable\_benefit from 0.
- If component\_details.
  - Set current\_month\_amount from self.\_get\_current\_month\_benefit\_amount(component\_details).
  - Set yearly\_benefit from component\_details.get(“amount”, 0).
  - Set claimable\_benefit from get\_max\_claim\_eligible(self.employee, payroll\_period, component\_details, current\_month\_amount).
- Set self.yearly\_benefit from yearly\_benefit.
- Set self.max\_amount\_eligible from claimable\_benefit.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get component details](operations-003.md#op-e9098f87e53b35), [get current month benefit amount](operations-003.md#op-b704df6c6bf404).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L1825) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L368) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L717)

<a id="op-e9098f87e53b35"></a>
### Employee Benefit Claim.get component details

`operation_workforce_payroll_record_definitions_employee_benefit_claim_business_behavior_employee_benefit_claim_get_component_details`

**Inputs** self, payroll\_period, salary\_structure\_assignment.

**Explicit results** no value · component\_details at 0 when component\_details, otherwise no value.

**Local steps**

- Set tuple(benefit\_details\_parent, benefit\_details\_doctype) from get\_benefits\_details\_parent(self.employee, payroll\_period, salary\_structure\_assignment).
- If not benefit\_details\_parent.
  - Return no value.
- Set EmployeeBenefitDetail from Platform.qb.DocType(benefit\_details\_doctype).
- Set SalaryComponent from Platform.qb.DocType(“Salary Component”).
- Set component\_details from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.name equa ….
- Return component\_details at 0 when component\_details, otherwise no value.
  - Value choice on component\_details — true gives component\_details at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L2207) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L369) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L718)

<a id="op-b704df6c6bf404"></a>
### Employee Benefit Claim.get current month benefit amount

`operation_workforce_payroll_record_definitions_employee_benefit_claim_business_behavior_employee_benefit_claim_get_current_month_benefit_amount`

**Inputs** self, component\_details.

**Declared result** float.

**Explicit results** self.preview\_salary\_slip\_and\_fetch\_current\_month\_benefit\_amount() · 0.0.

**Local steps**

- Set payout\_method from component\_details.get(“payout\_method”).
- If payout\_method equals “Accrue per cycle, pay only on claim”.
  - Return self.preview\_salary\_slip\_and\_fetch\_current\_month\_benefit\_amount().
- Return 0.0.

**Methods declared on this owner** [preview salary slip and fetch current month benefit amount](operations-003.md#op-1914c7a634331a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L2640) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L370) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L719)

<a id="op-1914c7a634331a"></a>
### Employee Benefit Claim.preview salary slip and fetch current month benefit amount

`operation_workforce_payroll_record_definitions_employee_benefit_claim_business_behavior_employee_benefit_claim_preview_salary_slip_and_fetch_current_month_benefit_amount`

**Inputs** self.

**Explicit results** benefit.get(“amount”, 0) · 0.

**Local steps**

- Bind dependencies make\_salary\_slip.
- Set salary\_structure from get\_assigned\_salary\_structure(self.employee, self.payroll\_date).
- Set salary\_slip from make\_salary\_slip(salary\_structure, employee = self.employee, posting\_date = self.payroll\_date, for\_preview = 1).
- Set accrued\_benefits from salary\_slip.get(“accrued\_benefits”, list()).
- For each benefit in accrued\_benefits.
  - If benefit.get(“salary\_component”) equals self.earning\_component.
    - Return benefit.get(“amount”, 0).
- Return 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L2769) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L373) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L722)

<a id="op-cdb1c4982312d3"></a>
### Get benefit components

`operation_workforce_payroll_record_definitions_employee_benefit_claim_business_behavior_get_benefit_components`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list.

**Explicit results** list() · nested operand in the contract(nested operand in the contract).where(nested operand in the contract.parent equals benefit\_details\_parent).where(SalaryComponent.payout\_method.isin(list(“Accrue per cycle, pa ….run().

**Local steps**

- Evaluate Platform.has\_permission(“Employee”, “read”, filters.get(“employee”), throw = true).
- Set employee from filters.get(“employee”).
- Set date from filters.get(“date”).
- Set company from filters.get(“company”).
- If (not employee or not date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not employee → not date.
  - Return list().
- Attempt the following.
  - Set salary\_structure\_assignment from get\_salary\_structure\_assignment(employee, date).
  - Set payroll\_period from get\_payroll\_period(date, date, company).get(“name”).
  - Set tuple(benefit\_details\_parent, benefit\_details\_doctype) from get\_benefits\_details\_parent(employee, payroll\_period, salary\_structure\_assignment).
  - If not benefit\_details\_parent.
    - Return list().
  - Set SalaryComponent from Platform.qb.DocType(“Salary Component”).
  - Set EmployeeBenefitDetail from Platform.qb.DocType(benefit\_details\_doctype).
  - Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.parent equals benefit\_details\_parent).where(SalaryComponent.payout\_method.isin(list(“Accrue per cycle, pa ….run().
- On failure (Exception) bound to e.
  - Evaluate Platform.log\_error(“Error fetching benefit components”, e).
  - Return list().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, filters.get(“employee”), throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L3049) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L377) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L726)

<a id="op-d1e132b0d10829"></a>
### Get salary structure assignment

`operation_workforce_payroll_record_definitions_employee_benefit_claim_business_behavior_get_salary_structure_assignment`

**Inputs** employee, date.

**Explicit results** result at 0.

**Explicit failure paths** validation helper — translated “Salary Structure Assignment not found for employee {0} on date {1}”.format(employee, date).

**Local steps**

- Set SalaryStructureAssignment from Platform.qb.DocType(“Salary Structure Assignment”).
- Set result from nested operand in the contract(nested operand in the contract).orderby(SalaryStructureAssignment.from\_date, order = nested operand in the contract.qb.desc).limit(1).run(pluck = “name”).
- If not result.
  - Call the validation error handler Platform.throw(translated “Salary Structure Assignment not found for employee {0} on date {1}”.format(employee, date)).
- Return result at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L3841) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L378) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L727)

## Record · Employee benefit ledger

[Record definition](../../../../data/record-types/employee_benefit_ledger.json)

<a id="op-c9a1bfd03d77db"></a>
### Employee Benefit Ledger.validate

`operation_workforce_payroll_record_definitions_employee_benefit_ledger_business_behavior_employee_benefit_ledger_validate`

**Inputs** self.

**Record and data access** read “Salary Component” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Salary Component {0} must be of type 'Earning' to be used in Employee Benefit Ledger”.format(self.salary\_component).

**Local steps**

- Set type from Platform.get\_cached\_value(“Salary Component”, self.salary\_component, “type”).
- If type differs from “Earning”.
  - Call the validation error handler Platform.throw(translated “Salary Component {0} must be of type 'Earning' to be used in Employee Benefit Ledger”.format(self.salary\_component)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Salary Component”, self.salary\_component, “type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L4234) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L381) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L730)

<a id="op-cd2cafcf2e0fc8"></a>
### Create employee benefit ledger entry

`operation_workforce_payroll_record_definitions_employee_benefit_ledger_business_behavior_create_employee_benefit_ledger_entry`

**Inputs** ref\_doc, args = no value, delete = false.

**Record and data access** read args.get(“benefit\_details\_doctype”) via get\_value · resolve a document from entry via get\_doc.

**State and service calls** call insert on Platform.get\_doc(entry).

**Explicit results** no value.

**Local steps**

- Set components from ((args or mapping()).get(“benefit\_ledger\_components”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (args or mapping()).get(“benefit\_ledger\_components”) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args → mapping().
- If not components.
  - Return no value.
- Set base\_entry from mapping(“doctype” → “Employee Benefit Ledger”, “employee” → ref\_doc.employee, “employee\_name” → ref\_doc.employee\_name, “company” → ref\_doc.company, …).
- Set reference\_doctype from “Salary Structure Assignment” when args.get(“benefit\_details\_doctype”) equals “Employee Benefit Detail”, otherwise “Employee Benefit Application”.
  - Value choice on args.get(“benefit\_details\_doctype”) equals “Employee Benefit Detail” — true gives “Salary Structure Assignment”, false gives “Employee Benefit Application”.
- Set reference\_document from args.get(“benefit\_details\_parent”).
- For each component in components.
  - Set entry from base\_entry.copy().
  - Evaluate entry.update(mapping(“salary\_component” → component.get(“salary\_component”), “amount” → component.get(“amount”), “transaction\_type” → component.get(“transaction\_type”), “yearly\_benefit” → component.get(“ye ….
  - If entry at “flexible\_benefit” equals 1.
    - Set entry at “reference\_doctype” from reference\_doctype.
    - Set entry at “reference\_document” from reference\_document.
    - If not entry at “yearly\_benefit”.
      - Set entry at “yearly\_benefit” from (Platform.db.get\_value(args.get(“benefit\_details\_doctype”), mapping(“parent” → args.get(“benefit\_details\_parent”), “salary\_component” → entry at “salary\_component”), “amount”) or 0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(args.get(“benefit\_details\_doctype”), mapping(“parent” → args.get(“benefit\_details\_parent”), “salary\_component” → entry at “salary\_component”), “amount”) → 0.
  - Evaluate Platform.get\_doc(entry).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L4398) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L379) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L728)

<a id="op-04ac38dc11b65c"></a>
### Delete employee benefit ledger entry

`operation_workforce_payroll_record_definitions_employee_benefit_ledger_business_behavior_delete_employee_benefit_ledger_entry`

**Inputs** ref\_field, ref\_value.

**Explicit results** no value.

**Local steps**

- Set EmployeeBenefitLedger from Platform.qb.DocType(“Employee Benefit Ledger”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where(EmployeeBenefitLedger at ref\_field equals ref\_value).run().
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L5362) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L380) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L729)

<a id="op-8d77ab707d9bc0"></a>
### Get max claim eligible

`operation_workforce_payroll_record_definitions_employee_benefit_ledger_business_behavior_get_maximum_claim_eligible`

**Inputs** employee, payroll\_period, benefit\_component, current\_month\_benefit\_amount = 0.

**Explicit results** claim\_eligible.

**Explicit failure paths** validation helper — translated “Accrued amount {0} is less than paid amount {1} for Benefit {2} in payroll period {3}”.format(accrued, paid, benefit\_component.name, payroll\_period).

**Local steps**

- Set payout\_method from benefit\_component.payout\_method.
- Set precision from Platform.get\_precision(“Employee Benefit Detail”, “amount”).
- Set claim\_eligible from 0.
- Set amounts from get\_benefit\_amount(employee, payroll\_period, benefit\_component.name).
- Set accrued from flt(amounts.get(“Accrual”, 0), precision).
- Set paid from flt(amounts.get(“Payout”, 0), precision).
- If payout\_method equals “Accrue per cycle, pay only on claim”.
  - Update accrued using + current\_month\_benefit\_amount.
  - If accrued ≥ paid.
    - Set claim\_eligible from flt((accrued − paid), precision).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Accrued amount {0} is less than paid amount {1} for Benefit {2} in payroll period {3}”.format(accrued, paid, benefit\_component.name, payroll\_period)).
- Otherwise.
  - If payout\_method equals “Allow claim for full benefit amount”.
    - Set claim\_eligible from (benefit\_component.amount − paid).
- Return claim\_eligible.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L5528) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L383) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L732)

<a id="op-457f9703969826"></a>
### Get benefit amount

`operation_workforce_payroll_record_definitions_employee_benefit_ledger_business_behavior_get_benefit_amount`

**Inputs** employee, payroll\_period, salary\_component.

**Explicit results** amounts.

**Local steps**

- Bind dependencies defaultdict.
- Set EmployeeBenefitLedger from Platform.qb.DocType(“Employee Benefit Ledger”).
- Set query from nested operand in the contract.qb.from\_(EmployeeBenefitLedger).select(EmployeeBenefitLedger.transaction\_type, EmployeeBenefitLedger.amount).where(((EmployeeBenefitLedger.employee equals employee bitwise an ….
- Set result from query.run(as\_dict = true).
- Set amounts from defaultdict(float).
- For each row in result.
  - Update amounts at row at “transaction\_type” using + row at “amount”.
- Return amounts.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L6018) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L382) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L731)

## Report · Employee ctc break up

<a id="op-f179aedce8981f"></a>
### Salary Breakup Report.initialize

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_initialize`

**Inputs** self, employee, salary\_structure\_assignment.

**Record and data access** read “Salary Structure Assignment” via get\_value.

**Local steps**

- Set self.employee from employee.
- Set self.salary\_structure\_assignment from salary\_structure\_assignment.
- Set tuple(self.salary\_structure, self.currency, self.assignment\_date, self.income\_tax\_slab, …) from Platform.get\_value(“Salary Structure Assignment”, mapping(“name” → salary\_structure\_assignment, “employee” → employee), list(“salary\_structure”, “currency”, “from\_date”, “income\_tax\_slab”, …)).
- Evaluate self.validate\_ctc().
- Set self.salary\_slip from \_make\_salary\_slip(self.salary\_structure, employee = self.employee, for\_preview = 1, as\_print = false, posting\_date = Platform.flags.posting\_date when Platform.flags.in\_test, otherwise no value, …).
  - Value choice on Platform.flags.in\_test — true gives Platform.flags.posting\_date, false gives no value.
- Set self.net\_pay from self.salary\_slip.net\_pay.
- Set self.gross\_pay from self.salary\_slip.gross\_pay.
- Set self.payroll\_frequency from self.salary\_slip.payroll\_frequency.
- Set self.cycle\_multiplier from mapping(“Monthly” → 12, “Fortnightly” → 24, “Bimonthly” → 6, “Weekly” → 52, …).get(self.payroll\_frequency).
- Set self.salary\_components from list().
- Set self.earning\_components from list().
- Set self.deduction\_components from list().
- Set self.tax\_components from list().
- Set self.employer\_contribution\_components from list().
- Set self.total\_net\_earnings from list().
- Set self.total\_gross\_earnings from list().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate ctc](operations-003.md#op-43c4cab9eaa140).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0142.json#L5685) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L954) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1301)

<a id="op-43c4cab9eaa140"></a>
### Salary Breakup Report.validate ctc

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_validate_cost_to_company`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please set cost to company(CTC) for employee {0} in the {1}”.format(Platform.bold(self.employee), get\_link\_to\_form(“Salary Structure Assignment”, self.salary\_structure\_assignment, “Salary Struc ….

**Local steps**

- If not self.ctc.
  - Call the validation error handler Platform.throw(translated “Please set cost to company(CTC) for employee {0} in the {1}”.format(Platform.bold(self.employee), get\_link\_to\_form(“Salary Structure Assignment”, self.salary\_structure\_assignment ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0142.json#L6354) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L963) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1310)

<a id="op-3768ad7ab4bfef"></a>
### Salary Breakup Report.get data

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_get_data`

**Inputs** self.

**Explicit results** (((((self.earning\_components + self.deduction\_components) + self.tax\_components) + self.employer\_contribution\_components) + self.total\_net\_earnings) + self.total\_gross\_earnings).

**Local steps**

- Evaluate self.set\_salary\_component\_details().
- Evaluate self.set\_employer\_contribution\_details().
- Evaluate self.calculate\_yearly\_amounts\_and\_percent\_of\_ctc().
- Evaluate self.indent\_salary\_components().
- Evaluate self.separate\_salary\_components\_by\_type().
- Evaluate self.set\_abbr\_type\_and\_formula().
- Evaluate self.set\_totals\_row\_for\_component\_types().
- Evaluate self.set\_net\_and\_gross\_earning\_rows().
- Return (((((self.earning\_components + self.deduction\_components) + self.tax\_components) + self.employer\_contribution\_components) + self.total\_net\_earnings) + self.total\_gross\_earnings).

**Methods declared on this owner** [set salary component details](operations-003.md#op-f1ff3d40d4ab88), [set employer contribution details](operations-004.md#op-f6b157c27767fb), [calculate yearly amounts and percent of ctc](operations-004.md#op-c5b5f9896a6008), [indent salary components](operations-004.md#op-963e53fe4783d6), [separate salary components by type](operations-004.md#op-c2decef97121d8), [set abbr type and formula](operations-004.md#op-d027496ece863c), [set totals row for component types](operations-004.md#op-8633805aa1a959), [set net and gross earning rows](operations-004.md#op-42055dd6e4bf87).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0142.json#L6547) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L950) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1297)

<a id="op-f1ff3d40d4ab88"></a>
### Salary Breakup Report.set salary component details

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_set_salary_component_details`

**Inputs** self.

**Record and data access** read “Salary Detail” via get\_all.

**Local steps**

- Set salary\_component\_details from Platform.db.get\_all(“Salary Detail”, filters = mapping(“parent” → self.salary\_structure), fields = list(“salary\_component”, “amount\_based\_on\_formula”, “formula”)).
- Set self.salary\_components from list of mapping(“salary\_component” → component.salary\_component, “per\_cycle” → component.amount, “abbr” → component.abbr, “is\_tax\_component” → component.variable\_based\_on\_taxable\_salary, …) for component d ….
  - Draw component from (self.salary\_slip.earnings + self.salary\_slip.deductions).
- For each component in self.salary\_components.
  - Set component\_details from next(generator of detail for detail drawn from salary\_component\_details where component.get(“salary\_component”) equals detail.salary\_component, mapping()).
    - Draw detail from salary\_component\_details, keep a combination only if (component.get(“salary\_component”) equals detail.salary\_component).
  - Evaluate component.update(component\_details).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0142.json#L6809) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L959) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1306)
