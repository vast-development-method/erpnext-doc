# Payroll and benefits · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Arrear

[Record definition](../../../../data/record-types/arrear.json)

<a id="op-c11656eb5ae881"></a>
### Arrear.validate salary structure assignment

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_validate_salary_structure_assignment`

**Inputs** self.

**Record and data access** read “Salary Structure Assignment” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “No active Salary Structure Assignment found for employee {0} with salary structure {1} on or after arrear st …”.format(Platform.bold(self.employee), Platform.bold(self.salary\_structure), (Platf ….

**Local steps**

- If not (self.employee and self.salary\_structure and self.payroll\_period).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.employee → self.salary\_structure → self.payroll\_period.
  - Return no value.
- Set assignment from Platform.db.get\_value(“Salary Structure Assignment”, mapping(“employee” → self.employee, “salary\_structure” → self.salary\_structure, “docstatus” → 1, “from\_date” → tuple(“&gt;=”, self.arrear\_start\_date)), lis ….
- If not assignment.
  - Call the validation error handler Platform.throw(translated “No active Salary Structure Assignment found for employee {0} with salary structure {1} on or after arrear st …”.format(Platform.bold(self.employee), Platform.bold(self.salary\_str ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.bold(self.arrear\_start\_date) → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0106.json#L6942) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L355) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L704)

<a id="op-a8bf7517c9ab74"></a>
### Arrear.validate duplicate doc

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_validate_duplicate_record`

**Inputs** self.

**Record and data access** read “Arrear” via exists.

**Explicit failure paths** validation helper — translated “An Arrear document already exists for employee {0} with salary structure {1} in payroll period {2}”.format(Platform.bold(self.employee), Platform.bold(self.salary\_structure), Platform.bold(self ….

**Local steps**

- If Platform.db.exists(“Arrear”, mapping(“employee” → self.employee, “salary\_structure” → self.salary\_structure, “payroll\_period” → self.payroll\_period, “docstatus” → 1, …)).
  - Call the validation error handler Platform.throw(translated “An Arrear document already exists for employee {0} with salary structure {1} in payroll period {2}”.format(Platform.bold(self.employee), Platform.bold(self.salary\_structure), Pla ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L354) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L703)

<a id="op-be96cd159e3a82"></a>
### Arrear.calculate salary structure arrears

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_calculate_salary_structure_arrears`

**Inputs** self.

**Local steps**

- Set existing\_salary\_slips from self.get\_existing\_salary\_slips().
- Set salary\_slip\_names from list of slip.get(“name”) for slip drawn from existing\_salary\_slips.
  - Draw slip from existing\_salary\_slips.
- Set existing\_components from self.fetch\_existing\_salary\_components(salary\_slip\_names).
- Set new\_structure\_components from self.generate\_preview\_components(existing\_salary\_slips).
- Set component\_differences from self.compute\_component\_differences(existing\_components, new\_structure\_components).
- If component\_differences.
  - Evaluate self.populate\_arrear\_tables(component\_differences).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get existing salary slips](operations-002.md#op-c853a69e12b87a), [fetch existing salary components](operations-002.md#op-3cfa350673da49), [generate preview components](operations-002.md#op-c36a2c8903b771), [compute component differences](operations-002.md#op-c0daceb54aba9e), [populate arrear tables](operations-002.md#op-e54eec58c01f7d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L312) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L337) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L686)

<a id="op-c853a69e12b87a"></a>
### Arrear.get existing salary slips

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_get_existing_salary_slips`

**Inputs** self.

**Record and data access** read “Salary Slip” via get\_all.

**Explicit results** salary\_slips.

**Explicit failure paths** validation helper — translated “No salary slips found for the selected employee from {0}”.format(self.arrear\_start\_date).

**Local steps**

- Set salary\_slips from list().
- If (self.employee and self.arrear\_start\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.employee → self.arrear\_start\_date.
  - Set filters from mapping(“employee” → self.employee, “docstatus” → 1, “start\_date” → tuple(“&gt;=”, self.arrear\_start\_date)).
  - Set salary\_slips from Platform.get\_all(“Salary Slip”, filters = filters, fields = list(“name”, “posting\_date”, “start\_date”, “end\_date”), order\_by = “start\_date”).
- If not salary\_slips.
  - Call the validation error handler Platform.throw(translated “No salary slips found for the selected employee from {0}”.format(self.arrear\_start\_date)).
- Return salary\_slips.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L554) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L346) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L695)

<a id="op-3cfa350673da49"></a>
### Arrear.fetch existing salary components

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_fetch_existing_salary_components`

**Inputs** self, salary\_slips.

**Explicit results** mapping(“earnings” → earnings\_totals, “deductions” → deductions\_totals, “accruals” → accrual\_totals).

**Explicit failure paths** validation helper — translated “No arrear components found in the existing salary slips.”.

**Local steps**

- Set SalarySlipDetail from Platform.qb.DocType(“Salary Detail”).
- Set SalaryComponent from Platform.qb.DocType(“Salary Component”).
- Set slip\_details from nested operand in the contract(nested operand in the contract).select(SalarySlipDetail.parentfield, SalarySlipDetail.salary\_component, SalarySlipDetail.amount).where((((nested operand in the contract(neste ….
- Set earnings\_totals from mapping().
- Set deductions\_totals from mapping().
- For each detail in slip\_details.
  - Set comp from detail.salary\_component.
  - Set amt from detail.amount.
  - Set parentfield from detail.parentfield.
  - If parentfield equals “earnings”.
    - Set earnings\_totals at comp from (earnings\_totals.get(comp, 0.0) + amt).
  - Otherwise.
    - If parentfield equals “deductions”.
      - Set deductions\_totals at comp from (deductions\_totals.get(comp, 0.0) + amt).
- Set accrual\_totals from self.fetch\_existing\_accrual\_components(salary\_slips).
- Set payroll\_correction\_totals from self.fetch\_existing\_payroll\_corrections(salary\_slips).
- For each tuple(component, amount) in payroll\_correction\_totals.get(“earnings”, mapping()).items().
  - Set earnings\_totals at component from (earnings\_totals.get(component, 0.0) + amount).
- For each tuple(component, amount) in payroll\_correction\_totals.get(“deductions”, mapping()).items().
  - Set deductions\_totals at component from (deductions\_totals.get(component, 0.0) + amount).
- For each tuple(component, amount) in payroll\_correction\_totals.get(“accruals”, mapping()).items().
  - Set accrual\_totals at component from (accrual\_totals.get(component, 0.0) + amount).
- If not (earnings\_totals or deductions\_totals or accrual\_totals).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in earnings\_totals → deductions\_totals → accrual\_totals.
  - Call the validation error handler Platform.throw(translated “No arrear components found in the existing salary slips.”).
- Return mapping(“earnings” → earnings\_totals, “deductions” → deductions\_totals, “accruals” → accrual\_totals).

**Methods declared on this owner** [fetch existing accrual components](operations-002.md#op-f8b5b570b89358), [fetch existing payroll corrections](operations-002.md#op-bcf862adcf0592).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L892) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L343) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L692)

<a id="op-f8b5b570b89358"></a>
### Arrear.fetch existing accrual components

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_fetch_existing_accrual_components`

**Inputs** self, salary\_slips.

**Explicit results** mapping() · accrual\_totals.

**Local steps**

- If not salary\_slips.
  - Return mapping().
- Set AccruedBenefit from Platform.qb.DocType(“Employee Benefit Detail”).
- Set SalaryComponent from Platform.qb.DocType(“Salary Component”).
- Set accrual\_details from nested operand in the contract(nested operand in the contract).select(AccruedBenefit.salary\_component, AccruedBenefit.amount).where((nested operand in the contract.parent.isin(salary\_slips) bitwise and Sal ….
- Set accrual\_totals from mapping().
- For each detail in accrual\_details.
  - Set comp from detail.get(“salary\_component”).
  - Set amt from detail.get(“amount”, 0.0).
  - Set accrual\_totals at comp from (accrual\_totals.get(comp, 0.0) + amt).
- Return accrual\_totals.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L2004) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L341) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L690)

<a id="op-bcf862adcf0592"></a>
### Arrear.fetch existing payroll corrections

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_fetch_existing_payroll_corrections`

**Inputs** self, salary\_slips.

**Explicit results** mapping(“earnings” → mapping(), “deductions” → mapping(), “accruals” → mapping()) · mapping(“earnings” → earnings\_totals, “deductions” → deductions\_totals, “accruals” → accrual\_totals).

**Local steps**

- If not salary\_slips.
  - Return mapping(“earnings” → mapping(), “deductions” → mapping(), “accruals” → mapping()).
- Set PayrollCorrection from Platform.qb.DocType(“Payroll Correction”).
- Set PCChild from Platform.qb.DocType(“Payroll Correction Child”).
- Set SalaryComponent from Platform.qb.DocType(“Salary Component”).
- Set corrections from nested operand in the contract(nested operand in the contract).select(PCChild.parentfield, PCChild.salary\_component, PCChild.amount).where(((nested operand in the contract.isin(salary\_slips) bitwise and ne ….
- Set earnings\_totals from mapping().
- Set deductions\_totals from mapping().
- Set accrual\_totals from mapping().
- For each detail in corrections.
  - Set comp from detail.salary\_component.
  - Set amt from (detail.amount or 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in detail.amount → 0.0.
  - Set parentfield from detail.parentfield.
  - If parentfield equals “earning\_arrears”.
    - Set earnings\_totals at comp from (earnings\_totals.get(comp, 0.0) + amt).
  - Otherwise.
    - If parentfield equals “deduction\_arrears”.
      - Set deductions\_totals at comp from (deductions\_totals.get(comp, 0.0) + amt).
    - Otherwise.
      - If parentfield equals “accrual\_arrears”.
        - Set accrual\_totals at comp from (accrual\_totals.get(comp, 0.0) + amt).
- Return mapping(“earnings” → earnings\_totals, “deductions” → deductions\_totals, “accruals” → accrual\_totals).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L2495) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L342) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L691)

<a id="op-c36a2c8903b771"></a>
### Arrear.generate preview components

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_generate_preview_components`

**Inputs** self, salary\_slips.

**Record and data access** resolve a document from mapping(“doctype” → “Salary Slip”, “employee” → self.employee, “salary\_structure” → self.salary\_structure, “posting\_date” → slip.get(“posting\_date”), …) via get\_doc.

**Explicit results** mapping() · mapping(“earnings” → preview\_earnings, “deductions” → preview\_deductions, “accruals” → preview\_accruals).

**Local steps**

- If not salary\_slips.
  - Return mapping().
- Set preview\_earnings from mapping().
- Set preview\_deductions from mapping().
- Set preview\_accruals from mapping().
- Bind local operation is\_arrear\_component for subsequent calls.
- For each slip in salary\_slips.
  - Set salary\_slip\_doc from Platform.get\_doc(mapping(“doctype” → “Salary Slip”, “employee” → self.employee, “salary\_structure” → self.salary\_structure, “posting\_date” → slip.get(“posting\_date”), …)).
  - Set PayrollCorrection from Platform.qb.DocType(“Payroll Correction”).
  - Set total\_days\_to\_reverse from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“total\_days”)).where((PayrollCorrection.salary\_slip\_reference equals slip.name bitwise and PayrollCo ….
  - Set total\_days\_to\_reverse from (total\_days\_to\_reverse at 0 or 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in total\_days\_to\_reverse at 0 → 0.0.
  - Set preview\_slip from make\_salary\_slip(self.salary\_structure, salary\_slip\_doc, self.employee, lwp\_days\_corrected = total\_days\_to\_reverse).
  - For each row in (preview\_slip.get(“earnings”, list()) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in preview\_slip.get(“earnings”, list()) → list().
    - If (not getattr(row, “additional\_salary”, no value) and is\_arrear\_component(row.salary\_component)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not getattr(row, “additional\_salary”, no value) → is\_arrear\_component(row.salary\_component).
      - Set preview\_earnings at row.salary\_component from (preview\_earnings.get(row.salary\_component, 0.0) + getattr(row, “amount”, 0.0)).
  - For each row in (preview\_slip.get(“deductions”, list()) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in preview\_slip.get(“deductions”, list()) → list().
    - If (not getattr(row, “additional\_salary”, no value) and not getattr(row, “variable\_based\_on\_taxable\_salary”, false) and is\_arrear\_component(row.salary\_component)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not getattr(row, “additional\_salary”, no value) → not getattr(row, “variable\_based\_on\_taxable\_salary”, false) → is\_arrear\_component(row.salary\_component).
      - Set preview\_deductions at row.salary\_component from (preview\_deductions.get(row.salary\_component, 0.0) + getattr(row, “amount”, 0.0)).
  - For each row in (getattr(preview\_slip, “accrued\_benefits”, list()) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(preview\_slip, “accrued\_benefits”, list()) → list().
    - If is\_arrear\_component(row.salary\_component).
      - Set preview\_accruals at row.salary\_component from (preview\_accruals.get(row.salary\_component, 0.0) + getattr(row, “amount”, 0.0)).
- Return mapping(“earnings” → preview\_earnings, “deductions” → preview\_deductions, “accruals” → preview\_accruals).

**Values supplied outside this operation** selected callable from getattr(row, “additional\_salary”, no value), getattr(row, “amount”, 0.0) and 2 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L3394) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L344) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L693)

<a id="op-ba3bdf0c945ff8"></a>
### Arrear.generate preview components.is arrear component

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_generate_preview_components_is_arrear_component`

**Inputs** component.

**Record and data access** read “Salary Component” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Salary Component”, component, “arrear\_component”).

**Local steps**

- Return Platform.get\_cached\_value(“Salary Component”, component, “arrear\_component”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Salary Component”, component, “arrear\_component”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L4685) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L345) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L694)

<a id="op-c0daceb54aba9e"></a>
### Arrear.compute component differences

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_compute_component_differences`

**Inputs** self, existing\_components, new\_components.

**Explicit results** result.

**Explicit failure paths** validation helper — translated “There are no arrear differences between existing and new salary structure components.”.

**Local steps**

- If not existing\_components.
  - Set existing\_components from mapping(“earnings” → mapping(), “deductions” → mapping(), “accruals” → mapping()).
- If not new\_components.
  - Set new\_components from mapping(“earnings” → mapping(), “deductions” → mapping(), “accruals” → mapping()).
- Set earnings\_diff from mapping().
- Set deductions\_diff from mapping().
- Set accruals\_diff from mapping().
- For each tuple(comp, amount) in new\_components.get(“earnings”, mapping()).items().
  - Set existing\_amount from existing\_components.get(“earnings”, mapping()).get(comp, 0.0).
  - Set diff from (amount − existing\_amount).
  - If diff &gt; 0.
    - Set earnings\_diff at comp from diff.
- For each tuple(comp, amount) in new\_components.get(“deductions”, mapping()).items().
  - Set existing\_amount from existing\_components.get(“deductions”, mapping()).get(comp, 0.0).
  - Set diff from (amount − existing\_amount).
  - If diff &gt; 0.
    - Set deductions\_diff at comp from diff.
- For each tuple(comp, amount) in new\_components.get(“accruals”, mapping()).items().
  - Set existing\_amount from existing\_components.get(“accruals”, mapping()).get(comp, 0.0).
  - Set diff from (amount − existing\_amount).
  - If diff &gt; 0.
    - Set accruals\_diff at comp from diff.
- Set result from mapping().
- If (earnings\_diff or deductions\_diff or accruals\_diff).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in earnings\_diff → deductions\_diff → accruals\_diff.
  - Set result from mapping(“earnings” → earnings\_diff, “deductions” → deductions\_diff, “accruals” → accruals\_diff).
- If not result.
  - Call the validation error handler Platform.throw(translated “There are no arrear differences between existing and new salary structure components.”).
- Return result.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L4757) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L338) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L687)

<a id="op-e54eec58c01f7d"></a>
### Arrear.populate arrear tables

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_populate_arrear_tables`

**Inputs** self, component\_differences.

**Local steps**

- Evaluate self.set(“earning\_arrears”, list()).
- Evaluate self.set(“deduction\_arrears”, list()).
- Evaluate self.set(“accrual\_arrears”, list()).
- For each tuple(comp, total\_amount) in component\_differences.get(“earnings”, mapping()).items().
  - Evaluate self.append(“earning\_arrears”, mapping(“salary\_component” → comp, “amount” → total\_amount)).
- For each tuple(comp, total\_amount) in component\_differences.get(“deductions”, mapping()).items().
  - Evaluate self.append(“deduction\_arrears”, mapping(“salary\_component” → comp, “amount” → total\_amount)).
- For each tuple(comp, total\_amount) in component\_differences.get(“accruals”, mapping()).items().
  - Evaluate self.append(“accrual\_arrears”, mapping(“salary\_component” → comp, “amount” → total\_amount)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L5673) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L350) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L699)

<a id="op-6017145d6edff7"></a>
### Arrear.validate arrear details

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_validate_arrear_details`

**Inputs** self.

**Explicit failure paths** validation helper — translated “No arrear details found”.

**Local steps**

- If not (self.earning\_arrears or self.deduction\_arrears or self.accrual\_arrears).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.earning\_arrears → self.deduction\_arrears → self.accrual\_arrears.
  - Call the validation error handler Platform.throw(translated “No arrear details found”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L6174) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L352) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L701)

<a id="op-8420d940894715"></a>
### Arrear.create additional salary

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_create_additional_salary`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Additional Salary”, “employee” → self.employee, “company” → self.company, “payroll\_date” → self.payroll\_date, …) via get\_doc.

**State and service calls** call insert on additional\_salary · call submit on additional\_salary.

**Local steps**

- For each component in ((self.earning\_arrears or list()) + (self.deduction\_arrears or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.earning\_arrears → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.deduction\_arrears → list().
  - If (not component.salary\_component or not component.amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not component.salary\_component → not component.amount.
    - Continue with the next iteration or loop test.
  - Set additional\_salary from Platform.get\_doc(mapping(“doctype” → “Additional Salary”, “employee” → self.employee, “company” → self.company, “payroll\_date” → self.payroll\_date, …)).
  - Evaluate additional\_salary.insert().
  - Evaluate additional\_salary.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L6284) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L339) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L688)

<a id="op-e2d60445c080ce"></a>
### Arrear.create benefit ledger entry

`operation_workforce_payroll_record_definitions_arrear_business_behavior_arrear_create_benefit_ledger_entry`

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

[Applicable decision contract](../../../workforce-decision-contracts/part-0107.json#L6671) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L340) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L689)

## Report · Bank remittance

<a id="op-1429d32d158244"></a>
### Execute

`operation_workforce_payroll_report_bank_remittance_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from list(mapping(“label” → translated “Payroll Number”, “fieldtype” → “Link”, “fieldname” → “payroll\_no”, “options” → “Payroll Entry”, …), mapping(“label” → translated “Debit A/C Number”, “fieldtype” → “Int”,  ….
- If Platform.db.has\_column(“Employee”, “ifsc\_code”).
  - Evaluate columns.append(mapping(“label” → translated “IFSC Code”, “fieldtype” → “Data”, “fieldname” → “bank\_code”, “width” → 100)).
- Update columns using + list(mapping(“label” → translated “Currency”, “fieldtype” → “Data”, “fieldname” → “currency”, “width” → 50), mapping(“label” → translated “Net Salary Amount”, “fieldtype” → “Currency”, “options” → “currenc ….
- Set data from list().
- Set accounts from get\_bank\_accounts().
- Set payroll\_entries from get\_payroll\_entries(accounts, filters).
- Set salary\_slips from get\_salary\_slips(payroll\_entries).
- If Platform.db.has\_column(“Employee”, “ifsc\_code”).
  - Evaluate get\_emp\_bank\_ifsc\_code(salary\_slips).
- For each salary in salary\_slips.
  - If (salary.bank\_name and salary.bank\_account\_no and salary.debit\_acc\_no and salary.status belongs to list(“Submitted”, “Paid”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in salary.bank\_name → salary.bank\_account\_no → salary.debit\_acc\_no → salary.status belongs to list(“Submitted”, “Paid”).
    - Set row from mapping(“payroll\_no” → salary.payroll\_entry, “debit\_account” → salary.debit\_acc\_no, “payment\_date” → Platform.utils.formatdate(salary.modified.strftime(“%Y-%m-%d”)), “bank\_name” → salary.bank\_name, …).
    - Evaluate data.append(row).
- Return tuple(columns, data).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0142.json#L2802) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L939) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1286)

<a id="op-3da08b9cbc9417"></a>
### Get bank accounts

`operation_workforce_payroll_report_bank_remittance_business_behavior_get_bank_accounts`

**Inputs** no declared parameters.

**Explicit results** accounts.

**Local steps**

- Set accounts from list of d.name for d drawn from get\_all(“Account”, filters = mapping(“account\_type” → “Bank”)).
  - Draw d from get\_all(“Account”, filters = mapping(“account\_type” → “Bank”)).
- Return accounts.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0142.json#L4302) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L940) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1287)

<a id="op-ded75f9b4b291e"></a>
### Get payroll entries

`operation_workforce_payroll_report_bank_remittance_business_behavior_get_payroll_entries`

**Inputs** accounts, filters.

**Explicit results** entries.

**Local steps**

- Set payroll\_filter from list(tuple(“payment\_account”, “IN”, accounts), tuple(“number\_of\_employees”, “&gt;”, 0), tuple(“Company”, “=”, filters.company)).
- If filters.to\_date.
  - Evaluate payroll\_filter.append(tuple(“posting\_date”, “&lt;”, filters.to\_date)).
- If filters.from\_date.
  - Evaluate payroll\_filter.append(tuple(“posting\_date”, “&gt;”, filters.from\_date)).
- Set entries from get\_all(“Payroll Entry”, payroll\_filter, list(“name”, “payment\_account”)).
- Set payment\_accounts from list of d.payment\_account for d drawn from entries.
  - Draw d from entries.
- Set entries from set\_company\_account(payment\_accounts, entries).
- Return entries.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0142.json#L4420) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L942) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1289)

<a id="op-fdf9b5910a4515"></a>
### Get salary slips

`operation_workforce_payroll_report_bank_remittance_business_behavior_get_salary_slips`

**Inputs** payroll\_entries.

**Explicit results** salary\_slips.

**Local steps**

- Set payroll from list of d.name for d drawn from payroll\_entries.
  - Draw d from payroll\_entries.
- Set salary\_slips from get\_all(“Salary Slip”, filters = list(tuple(“payroll\_entry”, “IN”, payroll)), fields = list(“modified”, “net\_pay”, “bank\_name”, “bank\_account\_no”, …)).
- Set payroll\_entry\_map from mapping().
- For each entry in payroll\_entries.
  - Set payroll\_entry\_map at entry.name from entry.
- For each slip in salary\_slips.
  - If slip.payroll\_entry.
    - Set slip at “debit\_acc\_no” from payroll\_entry\_map at slip.payroll\_entry at “company\_account”.
  - Otherwise.
    - Set slip at “debit\_acc\_no” from no value.
- Return salary\_slips.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0142.json#L4792) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L943) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1290)

<a id="op-4c0878119d14e5"></a>
### Get emp bank ifsc code

`operation_workforce_payroll_report_bank_remittance_business_behavior_get_employee_bank_ifsc_code`

**Inputs** salary\_slips.

**Explicit results** salary\_slips.

**Local steps**

- Set emp\_names from list of d.employee for d drawn from salary\_slips.
  - Draw d from salary\_slips.
- Set ifsc\_codes from get\_all(“Employee”, list(tuple(“name”, “IN”, emp\_names)), list(“ifsc\_code”, “name”)).
- Set ifsc\_codes\_map from mapping of code.name → code.ifsc\_code for code drawn from ifsc\_codes.
  - Draw code from ifsc\_codes.
- For each slip in salary\_slips.
  - Set slip at “ifsc\_code” from ifsc\_codes\_map at slip.employee.
- Return salary\_slips.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0142.json#L5155) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L941) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1288)

<a id="op-c6eb6fa537d4d1"></a>
### Set company account

`operation_workforce_payroll_report_bank_remittance_business_behavior_set_company_account`

**Inputs** payment\_accounts, payroll\_entries.

**Explicit results** payroll\_entries.

**Local steps**

- Set company\_accounts from get\_all(“Bank Account”, list(tuple(“account”, “in”, payment\_accounts)), list(“account”, “bank\_account\_no”)).
- Set company\_accounts\_map from mapping().
- For each acc in company\_accounts.
  - Set company\_accounts\_map at acc.account from acc.
- For each entry in payroll\_entries.
  - Set company\_account from empty text.
  - If entry.payment\_account belongs to company\_accounts\_map.
    - Set company\_account from company\_accounts\_map at entry.payment\_account at “bank\_account\_no”.
  - Set entry at “company\_account” from company\_account.
- Return payroll\_entries.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0142.json#L5396) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L944) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1291)

## Record · Bulk salary structure assignment

[Record definition](../../../../data/record-types/bulk_salary_structure_assignment.json)

<a id="op-30367a0baeae40"></a>
### Bulk Salary Structure Assignment.get employees

`operation_workforce_payroll_record_definitions_bulk_salary_structure_assignment_business_behavior_bulk_salary_structure_assignment_get_employees`

**Inputs** self, advanced\_filters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set quick\_filter\_fields from list(“company”, “employment\_type”, “branch”, “department”, …).
- Set filters from list of list(d, “=”, self.get(d)) for d drawn from quick\_filter\_fields where self.get(d).
  - Draw d from quick\_filter\_fields, keep a combination only if (self.get(d)).
- Update filters using + advanced\_filters.
- Set Assignment from Platform.qb.DocType(“Salary Structure Assignment”).
- Set employees\_with\_assignments from SubQuery(nested operand in the contract.select(nested operand in the contract.employee).distinct().where((Assignment.from\_date equals self.from\_date bitwise and Assignment.docstatus equals 1))).
- Set Employee from Platform.qb.DocType(“Employee”).
- Set Grade from Platform.qb.DocType(“Employee Grade”).
- Set query from nested operand in the contract(nested operand in the contract).left\_join(Grade).on(Employee.grade equals Grade.name).select(Coalesce(Grade.default\_base\_pay, 0).as\_(“base”), ConstantColumn(0).as\_(“variable”)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L94) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L359) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L708)

<a id="op-e92184725bf49b"></a>
### Bulk Salary Structure Assignment.bulk assign structure

`operation_workforce_payroll_record_definitions_bulk_salary_structure_assignment_business_behavior_bulk_salary_structure_assignment_bulk_assign_structure`

**Inputs** self, employees.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**State and service calls** enqueue with self.\_bulk\_assign\_structure · msgprint with translated “Creation of Salary Structure Assignments has been queued. It may take a few minutes.”.

**Explicit results** self.\_bulk\_assign\_structure(employees).

**Local steps**

- Set mandatory\_fields from list(“salary\_structure”, “from\_date”, “company”).
- Evaluate validate\_bulk\_tool\_fields(self, mandatory\_fields, employees).
- If len(employees) ≤ 30.
  - Return self.\_bulk\_assign\_structure(employees).
- Evaluate Platform.enqueue(self.\_bulk\_assign\_structure, timeout = 3000, employees = employees).
- Evaluate Platform.msgprint(translated “Creation of Salary Structure Assignments has been queued. It may take a few minutes.”, alert = true, indicator = “blue”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [bulk assign structure](operations-002.md#op-eaf557eea23c4f).

**Values supplied outside this operation** service or queued work from Platform.enqueue(self.\_bulk\_assign\_structure, timeout = 3000, employees = employees).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0108.json#L3627) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L357) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L706)

<a id="op-eaf557eea23c4f"></a>
### Bulk Salary Structure Assignment.bulk assign structure

`operation_workforce_payroll_record_definitions_bulk_salary_structure_assignment_business_behavior_bulk_salary_structure_assignment_bulk_assign_structure_2`

**Inputs** self, employees.

**Declared result** no value.

**State and service calls** savepoint savepoint · rollback · publish realtime with “completed\_bulk\_salary\_structure\_assignment”.

**Local steps**

- Set tuple(success, failure) from tuple(list(), list()).
- Set count from 0.
- Set savepoint from “before\_salary\_assignment”.
- For each d in employees.
  - Attempt the following.
    - Evaluate Platform.db.savepoint(savepoint).
    - Set assignment from create\_salary\_structure\_assignment(employee = d at “employee”, salary\_structure = self.salary\_structure, company = self.company, currency = self.currency, …).
  - On failure (Exception).
    - Evaluate Platform.db.rollback(save\_point = savepoint).
    - Evaluate Platform.log\_error(formatted text Bulk Assignment - Salary Structure Assignment failed for employee {d at “employee”}., reference\_doctype = “Salary Structure Assignment”).
    - Evaluate failure.append(d at “employee”).
  - When the protected block completes normally.
    - Evaluate success.append(mapping(“doc” → get\_link\_to\_form(“Salary Structure Assignment”, assignment), “employee” → d at “employee”)).
  - Update count using + 1.
  - Evaluate Platform.publish\_progress(((count × 100) ÷ len(employees)), title = translated “Assigning Structure...”).
- Evaluate Platform.publish\_realtime(“completed\_bulk\_salary\_structure\_assignment”, message = mapping(“success” → success, “failure” → failure), doctype = “Bulk Salary Structure Assignment”, after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“completed\_bulk\_salary\_structure\_assignment”, message = mapping(“success” → success, “failure” → failure), doctype = “Bulk Salary Structure Assignment”, after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0108.json#L3940) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L358) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L707)

## Record · Employee benefit application

[Record definition](../../../../data/record-types/employee_benefit_application.json)

<a id="op-ae2f7507c40329"></a>
### Employee Benefit Application.validate

`operation_workforce_payroll_record_definitions_employee_benefit_application_business_behavior_employee_benefit_application_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “As per your assigned Salary Structure you cannot apply for benefits”.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate self.validate\_duplicate\_on\_payroll\_period().
- If self.employee\_benefits.
  - Evaluate self.validate\_max\_benefit().
- Otherwise.
  - Call the validation error handler Platform.throw(translated “As per your assigned Salary Structure you cannot apply for benefits”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate on payroll period](operations-003.md#op-056182be398b93), [validate max benefit](operations-003.md#op-89350c2198ed5e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0108.json#L6370) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L364) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L713)
