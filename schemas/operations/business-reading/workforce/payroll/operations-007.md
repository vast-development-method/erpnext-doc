# Payroll and benefits · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Income tax computation

<a id="op-c7963d73b25818"></a>
### Income Tax Computation Report.get eligible hra

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_eligible_hra`

**Inputs** self, source.

**Record and data access** read source via get\_all.

**Local steps**

- If source equals “Employee Tax Exemption Proof Submission”.
  - Set hra\_amount\_field from “total\_eligible\_hra\_exemption”.
- Otherwise.
  - Set hra\_amount\_field from “annual\_hra\_exemption”.
- Set records from Platform.get\_all(source, filters = mapping(“docstatus” → 1, “employee” → list(“in”, list(nested operand in the contract.employees.keys())), “payroll\_period” → self.filters.payroll\_period), fields = list(“e ….
- For each d in records.
  - If not self.employees at d at 0 at “allow\_tax\_exemption”.
    - Continue with the next iteration or loop test.
  - If d at 0 does not belong to self.employees\_with\_proofs.
    - Evaluate self.employees at d at 0.setdefault(“hra”, d at 1).
    - Update self.employees at d at 0 at “total\_exemption” using + d at 1.
    - Evaluate self.employees\_with\_proofs.append(d at 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L4949) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L977) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1324)

<a id="op-cb1082bff95801"></a>
### Income Tax Computation Report.get standard tax exemption

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_standard_tax_exemption`

**Inputs** self.

**Record and data access** read “Income Tax Slab” via get\_all.

**Local steps**

- Evaluate self.add\_column(“Standard Tax Exemption”).
- Set standard\_exemptions\_per\_slab from dict(Platform.get\_all(“Income Tax Slab”, filters = mapping(“company” → self.filters.company, “docstatus” → 1, “disabled” → 0), fields = list(“name”, “standard\_tax\_exemption\_amount”), as\_list = 1)).
- For each emp\_details in self.employees.values().
  - Set income\_tax\_slab from emp\_details.get(“income\_tax\_slab”).
  - Set standard\_exemption from standard\_exemptions\_per\_slab.get(income\_tax\_slab, 0).
  - Set emp\_details at “standard\_tax\_exemption” from standard\_exemption.
  - Evaluate emp\_details.setdefault(“total\_exemption”, 0).
  - Update emp\_details at “total\_exemption” using + standard\_exemption.
- Evaluate self.add\_column(“Total Exemption”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add column](operations-007.md#op-ec2101c0cba054).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L5433) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L990) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1337)

<a id="op-89234bced46857"></a>
### Income Tax Computation Report.get income from other sources

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_income_from_other_sources`

**Inputs** self.

**Record and data access** read “Employee Other Income” via get\_all.

**Local steps**

- Evaluate self.add\_column(“Other Income”).
- For each employee in list(self.employees.keys()).
  - Set other\_income from (Platform.get\_all(“Employee Other Income”, filters = mapping(“employee” → employee, “payroll\_period” → nested operand in the contract.filters.payroll\_period, “company” → nested operand in the contract.filt ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“Employee Other Income”, filters = mapping(“employee” → employee, “payroll\_period” → self.filters.payroll\_period, “company” → self.filters.company, “docstatus” → 1), fields = list(mapping( … → 0.0.
  - Evaluate self.employees at employee.setdefault(“other\_income”, other\_income).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add column](operations-007.md#op-ec2101c0cba054).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L5829) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L986) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1333)

<a id="op-87125c5896f901"></a>
### Income Tax Computation Report.get total taxable amount

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_total_taxable_amount`

**Inputs** self.

**Record and data access** read “Salary Slip” via get\_value.

**Local steps**

- Evaluate self.add\_column(“Total Taxable Amount”).
- For each tuple(employee, emp\_details) in self.employees.items().
  - Set total\_taxable\_amount from 0.0.
  - Set annual\_taxable\_amount, tax\_exemption\_declaration, standard\_tax\_exemption\_amount, deductions\_before\_tax\_calculation from 0.0.
  - Set last\_ss from self.get\_last\_salary\_slip(employee).
  - If (last\_ss and last\_ss.end\_date equals self.payroll\_period\_end\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_ss → last\_ss.end\_date equals self.payroll\_period\_end\_date.
    - Set tuple(annual\_taxable\_amount, tax\_exemption\_declaration, deductions\_before\_tax\_calculation, standard\_tax\_exemption\_amount) from Platform.db.get\_value(“Salary Slip”, last\_ss.name, list(“annual\_taxable\_amount”, “tax\_exemption\_declaration”, “deductions\_before\_tax\_calculation”, “standard\_tax\_exemption\_amount”)).
  - Otherwise.
    - Set future\_salary\_slips from self.future\_salary\_slips.get(employee, list()).
    - If future\_salary\_slips.
      - Set last\_ss from future\_salary\_slips at 0.
      - Set annual\_taxable\_amount from last\_ss.get(“annual\_taxable\_amount”, 0.0).
      - Set tax\_exemption\_declaration from last\_ss.get(“tax\_exemption\_declaration”, 0.0).
      - Set standard\_tax\_exemption\_amount from last\_ss.get(“standard\_tax\_exemption\_amount”, 0.0).
      - Set deductions\_before\_tax\_calculation from last\_ss.get(“deductions\_before\_tax\_calculation”, 0.0).
  - If annual\_taxable\_amount.
    - Set total\_taxable\_amount from ((((flt(annual\_taxable\_amount) + flt(tax\_exemption\_declaration)) + flt(standard\_tax\_exemption\_amount)) + flt(deductions\_before\_tax\_calculation)) − emp\_details at “total\_exemption”).
  - Set emp\_details at “total\_taxable\_amount” from total\_taxable\_amount.

If control reaches the end, it returns no value.

**Methods declared on this owner** [add column](operations-007.md#op-ec2101c0cba054), [get last salary slip](operations-006.md#op-a9bd876dffde7a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L6161) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L995) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1342)

<a id="op-60269cf8cde852"></a>
### Income Tax Computation Report.get applicable tax

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_applicable_tax`

**Inputs** self.

**Record and data access** read “Salary Component” via get\_value · resolve a document from “Income Tax Slab” via get\_cached\_doc.

**Local steps**

- Evaluate self.add\_column(“Income Tax (Slab Based)”, “income\_tax\_slab\_based”).
- Evaluate self.add\_column(“Other Taxes and Charges”).
- Evaluate self.add\_column(“Total Applicable Tax”, “applicable\_tax”).
- Set is\_tax\_rounded from Platform.db.get\_value(“Salary Component”, mapping(“variable\_based\_on\_taxable\_salary” → 1, “disabled” → 0), “round\_to\_the\_nearest\_integer”).
- For each tuple(emp, emp\_details) in self.employees.items().
  - Set tax\_slab from emp\_details.get(“income\_tax\_slab”).
  - If tax\_slab.
    - Set tax\_slab from Platform.get\_cached\_doc(“Income Tax Slab”, tax\_slab).
    - Set tuple(eval\_globals, eval\_locals) from self.get\_data\_for\_eval(emp, emp\_details).
    - Set tuple(tax\_amount, other\_taxes\_and\_charges) from calculate\_tax\_by\_tax\_slab(emp\_details at “total\_taxable\_amount”, tax\_slab, eval\_globals = eval\_globals, eval\_locals = eval\_locals).
  - Otherwise.
    - Set tax\_amount from 0.0.
    - Set other\_taxes\_and\_charges from 0.0.
  - If is\_tax\_rounded.
    - Set tax\_amount from rounded(tax\_amount).
    - Set other\_taxes\_and\_charges from rounded(other\_taxes\_and\_charges).
  - Set emp\_details at “income\_tax\_slab\_based” from (tax\_amount − other\_taxes\_and\_charges).
  - Set emp\_details at “other\_taxes\_and\_charges” from other\_taxes\_and\_charges.
  - Set emp\_details at “applicable\_tax” from tax\_amount.

If control reaches the end, it returns no value.

**Methods declared on this owner** [add column](operations-007.md#op-ec2101c0cba054), [get data for eval](operations-007.md#op-23d81a3e36b833).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Income Tax Slab”, tax\_slab).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0146.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L974) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1321)

<a id="op-23d81a3e36b833"></a>
### Income Tax Computation Report.get data for eval

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_data_for_evaluate`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, emp, emp\_details.

**Explicit result forms** a structured result.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0146.json#L599) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L976) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1323)

<a id="op-497d03e3607ff3"></a>
### Income Tax Computation Report.get total deducted tax

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_total_deducted_tax`

**Inputs** self.

**Explicit results** list().

**Local steps**

- Set SalaryComponent from Platform.qb.DocType(“Salary Component”).
- Set tax\_components from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.type equals “Deduction”).where(SalaryComponent.disabled equals 0).run(pluck = “name”).
- If not tax\_components.
  - Return list().
- Evaluate self.add\_column(“Total Tax Deducted”).
- Set ss from Platform.qb.DocType(“Salary Slip”).
- Set ss\_ded from Platform.qb.DocType(“Salary Detail”).
- Set records from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.end\_date ≤ nested operand in the contract.payroll\_period\_end\_date).groupby(ss.employee).run(as\_dict = true).
- For each d in records.
  - Set total\_tax\_deducted from (flt(self.employees at d.employee.get(“tax\_deducted\_till\_date”, 0)) + d.amount).
  - Evaluate self.employees at d.employee.setdefault(“total\_tax\_deducted”, total\_tax\_deducted).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add column](operations-007.md#op-ec2101c0cba054).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0146.json#L1033) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L994) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1341)

<a id="op-30d095b5722afb"></a>
### Income Tax Computation Report.get payable tax

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_payable_tax`

**Inputs** self.

**Local steps**

- Evaluate self.add\_column(“Payable Tax”).
- For each tuple(\_\_, emp\_details) in self.employees.items().
  - Set payable\_tax from (flt(emp\_details.get(“applicable\_tax”)) − flt(emp\_details.get(“total\_tax\_deducted”))).
  - If payable\_tax &lt; 0.
    - Set payable\_tax from 0.0.
  - Set emp\_details at “payable\_tax” from payable\_tax.

If control reaches the end, it returns no value.

**Methods declared on this owner** [add column](operations-007.md#op-ec2101c0cba054).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0146.json#L1980) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L989) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1336)

<a id="op-ec2101c0cba054"></a>
### Income Tax Computation Report.add column

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_add_column`

**Inputs** self, label, fieldname = no value, fieldtype = no value, options = no value, width = no value.

**Local steps**

- Set col from mapping(“label” → translated label, “fieldname” → (fieldname or scrub(label)), “fieldtype” → (fieldtype or “Currency”), “options” → options, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldname → scrub(label).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldtype → “Currency”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in width → “140px”.
- Evaluate self.columns.append(col).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0146.json#L2206) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L972) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1319)

<a id="op-5e8b1b3a308cbd"></a>
### Income Tax Computation Report.get fixed columns

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_fixed_columns`

**Inputs** self.

**Local steps**

- Set self.columns from list(mapping(“label” → translated “Employee”, “fieldname” → “employee”, “fieldtype” → “Link”, “options” → “Employee”, …), mapping(“label” → translated “Employee Name”, “fieldname” → “employee\_name”, “field ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0146.json#L2469) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L981) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1328)

## Report · Income tax deductions

<a id="op-1ca520cdbdf65d"></a>
### Execute

`operation_workforce_payroll_report_income_tax_deductions_business_behavior_execute`

**Inputs** filters = no value.

**Declared result** tuple.

**Explicit results** tuple(columns, data).

**Local steps**

- Set is\_indian\_company from Enterprise.get\_region(filters.get(“company”)) equals “India”.
- Set columns from get\_columns(is\_indian\_company).
- Set data from get\_data(filters, is\_indian\_company).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0146.json#L6442) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1006) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1353)

<a id="op-5d1c9a1d96e0f9"></a>
### Get columns

`operation_workforce_payroll_report_income_tax_deductions_business_behavior_get_columns`

**Inputs** is\_indian\_company.

**Declared result** list at dict.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Employee”, “options” → “Employee”, “fieldname” → “employee”, “fieldtype” → “Link”, …), mapping(“label” → translated “Employee Name”, “fieldname” → “employee\_name”, “field ….
- If is\_indian\_company.
  - Evaluate columns.append(mapping(“label” → translated “PAN Number”, “fieldname” → “pan\_number”, “fieldtype” → “Data”, “width” → 140)).
- Update columns using + list(mapping(“label” → translated “Income Tax Component”, “fieldname” → “it\_comp”, “fieldtype” → “Data”, “width” → 170), mapping(“label” → translated “Income Tax Amount”, “fieldname” → “it\_amount”, “fieldt ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0147.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1007) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1354)

<a id="op-5bfc5ae24452d6"></a>
### Get data

`operation_workforce_payroll_report_income_tax_deductions_business_behavior_get_data`

**Inputs** filters, is\_indian\_company.

**Declared result** list at dict.

**Record and data access** read “Employee” via get\_all.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set employee\_pan\_dict from mapping().
- If is\_indian\_company.
  - Set employee\_pan\_dict from Platform.\_dict(Platform.get\_all(“Employee”, fields = list(“name”, “pan\_number”), as\_list = true)).
- Set deductions from get\_income\_tax\_deductions(filters).
- For each d in deductions.
  - Set employee from mapping(“employee” → d.employee, “employee\_name” → d.employee\_name, “it\_comp” → d.salary\_component, “posting\_date” → d.posting\_date, …).
  - If is\_indian\_company.
    - Set employee at “pan\_number” from employee\_pan\_dict.get(d.employee).
  - Evaluate data.append(employee).
- Return data.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0147.json#L791) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1008) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1355)

<a id="op-df69d7c651c947"></a>
### Get income tax deductions

`operation_workforce_payroll_report_income_tax_deductions_business_behavior_get_income_tax_deductions`

**Inputs** filters.

**Declared result** list at dict.

**Record and data access** read “Salary Component” via get\_all.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- Set component\_types from Platform.get\_all(“Salary Component”, filters = mapping(“is\_income\_tax\_component” → 1), pluck = “name”).
- If not component\_types.
  - Return list().
- Set SalarySlip from Platform.qb.DocType(“Salary Slip”).
- Set SalaryDetail from Platform.qb.DocType(“Salary Detail”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(SalarySlip.employee, SalarySlip.employee\_name, Sal ….
- For each field in list(“department”, “branch”, “company”).
  - If filters.get(field).
    - Set query from query.where(getattr(SalarySlip, field) equals filters.get(field)).
- If filters.get(“month”).
  - Set query from query.where(Extract(“month”, SalarySlip.start\_date) equals filters.month).
- If filters.get(“year”).
  - Set query from query.where(Extract(“year”, SalarySlip.start\_date) equals filters.year).
- Return query.run(as\_dict = true).

**Values supplied outside this operation** selected callable from getattr(SalarySlip, field).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0147.json#L1219) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1009) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1356)

## Record · Income tax slab

[Record definition](../../../../data/record-types/income_tax_slab.json)

<a id="op-af276cd3b710fb"></a>
### Income Tax Slab.validate

`operation_workforce_payroll_record_definitions_income_tax_slab_business_behavior_income_tax_slab_validate`

**Inputs** self.

**Local steps**

- If self.company.
  - Set self.currency from Enterprise.get\_company\_currency(self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L711) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L455) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L804)

<a id="op-d6e4f4623a972b"></a>
### Calculate tax by tax slab

`operation_workforce_payroll_record_definitions_income_tax_slab_business_behavior_calculate_tax_by_tax_slab`

**Inputs** annual\_taxable\_earning, tax\_slab, eval\_globals = no value, eval\_locals = no value.

**Explicit results** tuple(0, 0) · tuple(tax\_amount, (surcharge + other\_taxes)).

**Local steps**

- Set eval\_globals from (eval\_globals or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in eval\_globals → mapping().
- Set eval\_locals from (eval\_locals or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in eval\_locals → mapping().
- If annual\_taxable\_earning ≤ tax\_slab.tax\_relief\_limit.
  - Return tuple(0, 0).
- Set tax\_amount from calculate\_base\_tax\_from\_tax\_slabs(annual\_taxable\_earning, tax\_slab, eval\_globals, eval\_locals).
- If tax\_with\_marginal\_relief bound to calculate\_tax\_with\_marginal\_relief(tax\_slab, tax\_amount, annual\_taxable\_earning).
  - Set tax\_amount from tax\_with\_marginal\_relief.
- Set tuple(tax\_amount, surcharge) from apply\_surcharge\_with\_marginal\_relief(tax\_amount, annual\_taxable\_earning, tax\_slab, eval\_globals, …).
- Set tuple(tax\_amount, other\_taxes) from calculate\_other\_charges(tax\_amount, annual\_taxable\_earning, tax\_slab).
- Return tuple(tax\_amount, (surcharge + other\_taxes)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L795) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L453) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L802)

<a id="op-4fdf038662f6b7"></a>
### Calculate base tax from tax slabs

`operation_workforce_payroll_record_definitions_income_tax_slab_business_behavior_calculate_base_tax_from_tax_slabs`

**Inputs** annual\_taxable\_earning, tax\_slab, eval\_globals, eval\_locals.

**Explicit results** tax\_amount.

**Local steps**

- Set tax\_amount from 0.
- Evaluate eval\_locals.update(mapping(“annual\_taxable\_earning” → annual\_taxable\_earning)).
- For each slab in tax\_slab.slabs.
  - Set cond from cstr(slab.condition).strip().
  - If (cond and not eval\_tax\_slab\_condition(cond, eval\_globals, eval\_locals)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cond → not eval\_tax\_slab\_condition(cond, eval\_globals, eval\_locals).
    - Continue with the next iteration or loop test.
  - If (not slab.to\_amount and annual\_taxable\_earning ≥ slab.from\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not slab.to\_amount → annual\_taxable\_earning ≥ slab.from\_amount.
    - Update tax\_amount using + ((((annual\_taxable\_earning − slab.from\_amount) + 1) × slab.percent\_deduction) × 0.01).
    - Continue with the next iteration or loop test.
  - If (annual\_taxable\_earning ≥ slab.from\_amount and annual\_taxable\_earning &lt; slab.to\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in annual\_taxable\_earning ≥ slab.from\_amount → annual\_taxable\_earning &lt; slab.to\_amount.
    - Update tax\_amount using + ((((annual\_taxable\_earning − slab.from\_amount) + 1) × slab.percent\_deduction) × 0.01).
  - Otherwise.
    - If (annual\_taxable\_earning ≥ slab.from\_amount and annual\_taxable\_earning ≥ slab.to\_amount).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in annual\_taxable\_earning ≥ slab.from\_amount → annual\_taxable\_earning ≥ slab.to\_amount.
      - Update tax\_amount using + ((((slab.to\_amount − slab.from\_amount) + 1) × slab.percent\_deduction) × 0.01).
- Return tax\_amount.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L1152) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L451) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L800)

<a id="op-50cb38115d1d4a"></a>
### Calculate other charges

`operation_workforce_payroll_record_definitions_income_tax_slab_business_behavior_calculate_other_charges`

**Inputs** tax\_amount, annual\_taxable\_earning, tax\_slab.

**Explicit results** tuple(tax\_amount, total\_other\_taxes\_and\_charges).

**Local steps**

- Set total\_other\_taxes\_and\_charges from 0.
- For each d in tax\_slab.other\_taxes\_and\_charges.
  - If (flt(d.min\_taxable\_income) and flt(d.min\_taxable\_income) &gt; annual\_taxable\_earning).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(d.min\_taxable\_income) → flt(d.min\_taxable\_income) &gt; annual\_taxable\_earning.
    - Continue with the next iteration or loop test.
  - If (flt(d.max\_taxable\_income) and flt(d.max\_taxable\_income) &lt; annual\_taxable\_earning).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(d.max\_taxable\_income) → flt(d.max\_taxable\_income) &lt; annual\_taxable\_earning.
    - Continue with the next iteration or loop test.
  - Set other\_taxes\_and\_charges from ((tax\_amount × flt(d.percent)) ÷ 100).
  - Update tax\_amount using + other\_taxes\_and\_charges.
  - Update total\_other\_taxes\_and\_charges using + other\_taxes\_and\_charges.
- Return tuple(tax\_amount, total\_other\_taxes\_and\_charges).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L1682) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L452) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L801)

<a id="op-12e5b7b22b044f"></a>
### Eval tax slab condition

`operation_workforce_payroll_record_definitions_income_tax_slab_business_behavior_evaluate_tax_slab_condition`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** condition, eval\_globals, eval\_locals.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** active or constructed exception.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 3 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L1974) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L454) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L803)

<a id="op-12e9da48770399"></a>
### Apply surcharge with marginal relief

`operation_workforce_payroll_record_definitions_income_tax_slab_business_behavior_apply_surcharge_with_marginal_relief`

**Inputs** tax\_amount, annual\_taxable\_earning, tax\_slab, eval\_globals, eval\_locals.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Explicit results** tuple(tax\_amount, 0).

**Local steps**

- Return tuple(tax\_amount, 0).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L2480) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L450) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L799)

## Record · Payroll correction

[Record definition](../../../../data/record-types/payroll_correction.json)

<a id="op-fab12cc2bd172d"></a>
### Payroll Correction.validate

`operation_workforce_payroll_record_definitions_payroll_correction_business_behavior_payroll_correction_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Days to Reverse must be greater than zero.”.

**Local steps**

- <a id="op-fab12cc2bd172d-guard-2"></a>If self.days\_to\_reverse ≤ 0.
  - Call the validation error handler Platform.throw(translated “Days to Reverse must be greater than zero.”).
- Evaluate self.validate\_days().
- Evaluate self.populate\_breakup\_table().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.days\_to\_reverse ≤ 0, self.days\_to\_reverse = 0 selects the branch that calls the validation-error handler with translated “Days to Reverse must be greater than zero.”. With self.days\_to\_reverse = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-fab12cc2bd172d-guard-2)

**Methods declared on this owner** [validate days](operations-007.md#op-844559427e742c), [populate breakup table](operations-008.md#op-c472e95b2bcbd3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L5321) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L471) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L820)

<a id="op-19c37aaac1118d"></a>
### Payroll Correction.on submit

`operation_workforce_payroll_record_definitions_payroll_correction_business_behavior_payroll_correction_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_arrear\_details().
- Evaluate self.create\_additional\_salary().
- Evaluate self.create\_benefit\_ledger\_entry().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate arrear details](operations-008.md#op-c6e967025a655d), [create additional salary](operations-008.md#op-ac32a88048b07c), [create benefit ledger entry](operations-008.md#op-947f0339b89212).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L5457) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L469) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L818)

<a id="op-844559427e742c"></a>
### Payroll Correction.validate days

`operation_workforce_payroll_record_definitions_payroll_correction_business_behavior_payroll_correction_validate_days`

**Inputs** self.

**Record and data access** resolve a document from “Salary Slip” via get\_doc · read “Payroll Correction” via get\_all.

**Explicit failure paths** validation helper — translated “You cannot reverse more than the total LWP days {0}. You have already reversed {1} days for this employee.”.format(self.lwp\_days, total\_days\_reversed).

**Local steps**

- If (self.days\_to\_reverse and self.salary\_slip\_reference).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.days\_to\_reverse → self.salary\_slip\_reference.
  - Set salary\_slip from Platform.get\_doc(“Salary Slip”, self.salary\_slip\_reference).
  - Set self.working\_days from salary\_slip.total\_working\_days.
  - Set self.payment\_days from salary\_slip.payment\_days.
  - Set self.lwp\_days from max((salary\_slip.total\_working\_days − salary\_slip.payment\_days), 0).
  - Set payroll\_corrections from Platform.get\_all(“Payroll Correction”, filters = mapping(“docstatus” → 1, “payroll\_period” → self.payroll\_period, “salary\_slip\_reference” → self.salary\_slip\_reference, “employee” → self.employee, …), field ….
  - Set total\_days\_reversed from (sum(generator of entry at “days\_to\_reverse” for entry drawn from payroll\_corrections) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sum(generator of entry at “days\_to\_reverse” for entry drawn from payroll\_corrections) → 0.
    - Draw entry from payroll\_corrections.
  - If (total\_days\_reversed + self.days\_to\_reverse) &gt; self.lwp\_days.
    - Call the validation error handler Platform.throw(translated “You cannot reverse more than the total LWP days {0}. You have already reversed {1} days for this employee.”.format(self.lwp\_days, total\_days\_reversed)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L5548) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L473) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L822)

<a id="op-ba9e5124cd8daa"></a>
### Payroll Correction.on cancel

`operation_workforce_payroll_record_definitions_payroll_correction_business_behavior_payroll_correction_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate delete\_employee\_benefit\_ledger\_entry(“reference\_document”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L6080) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L468) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L817)
