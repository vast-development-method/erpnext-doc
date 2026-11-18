# Payroll and benefits · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Gratuity

[Record definition](../../../../data/record-types/gratuity.json)

<a id="op-403185ae1cb265"></a>
### Gratuity.on discard

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_gratuity_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0112.json#L1849) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L430) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L779)

<a id="op-9b27319c410f61"></a>
### Get last salary slip

`operation_workforce_payroll_record_definitions_gratuity_business_behavior_get_last_salary_slip`

**Inputs** employee.

**Declared result** (dict bitwise or no value).

**Record and data access** read “Salary Slip” via get\_value · resolve a document from “Salary Slip” via get\_doc.

**Explicit results** Platform.get\_doc(“Salary Slip”, salary\_slip).

**Local steps**

- Set salary\_slip from Platform.db.get\_value(“Salary Slip”, mapping(“employee” → employee, “docstatus” → 1), order\_by = “start\_date desc”).
- If salary\_slip.
  - Return Platform.get\_doc(“Salary Slip”, salary\_slip).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0112.json#L1912) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L414) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L763)

<a id="op-12c8ecb5dca36b"></a>
### Get data

`operation_workforce_payroll_record_definitions_gratuity_gratuity_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “reference\_name”, “non\_standard\_fieldnames” → mapping(“Additional Salary” → “ref\_docname”), “transactions” → list(mapping(“label” → translated “Payment”, “items” → list(“Payment Entry ….

**Local steps**

- Return mapping(“fieldname” → “reference\_name”, “non\_standard\_fieldnames” → mapping(“Additional Salary” → “ref\_docname”), “transactions” → list(mapping(“label” → translated “Payment”, “items” → list(“Payment Entry ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0112.json#L2085) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L435) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L784)

## Record · Gratuity rule

[Record definition](../../../../data/record-types/gratuity_rule.json)

<a id="op-bf4727f193d52b"></a>
### Gratuity Rule.validate

`operation_workforce_payroll_record_definitions_gratuity_rule_business_behavior_gratuity_rule_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: From (Year) can not be greater than To (Year)”.format(current\_slab.idx) · validation helper — translated “You can not define multiple slabs if you have a slab with no lower and upper limits.”.

**Local steps**

- For each current\_slab in self.gratuity\_rule\_slabs.
  - If (current\_slab.from\_year &gt; current\_slab.to\_year and current\_slab.to\_year differs from 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_slab.from\_year &gt; current\_slab.to\_year → current\_slab.to\_year differs from 0.
    - Call the validation error handler Platform.throw(translated “Row {0}: From (Year) can not be greater than To (Year)”.format(current\_slab.idx)).
  - If (current\_slab.to\_year equals 0 and current\_slab.from\_year equals 0 and len(self.gratuity\_rule\_slabs) &gt; 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_slab.to\_year equals 0 → current\_slab.from\_year equals 0 → len(self.gratuity\_rule\_slabs) &gt; 1.
    - Call the validation error handler Platform.throw(translated “You can not define multiple slabs if you have a slab with no lower and upper limits.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L437) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L786)

<a id="op-0bf366695815e4"></a>
### Get gratuity rule

`operation_workforce_payroll_record_definitions_gratuity_rule_business_behavior_get_gratuity_rule`

**Inputs** name, slabs, remaining named values args.

**State and service calls** request new\_doc for “Gratuity Rule”.

**Explicit results** rule.

**Local steps**

- Set args from Platform.\_dict(args).
- Set rule from Platform.new\_doc(“Gratuity Rule”).
- Set rule.name from name.
- Set rule.calculate\_gratuity\_amount\_based\_on from (args.calculate\_gratuity\_amount\_based\_on or “Current Slab”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.calculate\_gratuity\_amount\_based\_on → “Current Slab”.
- Set rule.work\_experience\_calculation\_method from (args.work\_experience\_calculation\_method or “Take Exact Completed Years”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.work\_experience\_calculation\_method → “Take Exact Completed Years”.
- Set rule.minimum\_year\_for\_gratuity from 1.
- For each slab in slabs.
  - Set slab from Platform.\_dict(slab).
  - Evaluate rule.append(“gratuity\_rule\_slabs”, slab).
- Return rule.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L295) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L436) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L785)

<a id="op-775988f40052bc"></a>
### Get data

`operation_workforce_payroll_record_definitions_gratuity_rule_gratuity_rule_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “gratuity\_rule”, “transactions” → list(mapping(“label” → translated “Gratuity”, “items” → list(“Gratuity”)))).

**Local steps**

- Return mapping(“fieldname” → “gratuity\_rule”, “transactions” → list(mapping(“label” → translated “Gratuity”, “items” → list(“Gratuity”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0113.json#L581) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L438) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L787)

## Report · Income tax computation

<a id="op-06551755e9b5f7"></a>
### Execute

`operation_workforce_payroll_report_income_tax_computation_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** IncomeTaxComputationReport(filters).run().

**Local steps**

- Return IncomeTaxComputationReport(filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0144.json#L5460) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L971) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1318)

<a id="op-eb45b38b226a3f"></a>
### Income Tax Computation Report.initialize

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_initialize`

**Inputs** self, filters = no value.

**Record and data access** read “Payroll Period” via get\_value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set self.columns from list().
- Set self.data from list().
- Set self.employees from Platform.\_dict().
- Set self.payroll\_period\_start\_date from no value.
- Set self.payroll\_period\_end\_date from no value.
- If self.filters.payroll\_period.
  - Set tuple(self.payroll\_period\_start\_date, self.payroll\_period\_end\_date) from Platform.db.get\_value(“Payroll Period”, self.filters.payroll\_period, list(“start\_date”, “end\_date”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0144.json#L5524) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L997) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1344)

<a id="op-9f16714e62e195"></a>
### Income Tax Computation Report.run

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_run`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data).

**Local steps**

- Evaluate self.get\_fixed\_columns().
- Evaluate self.get\_data().
- Return tuple(self.columns, self.data).

**Methods declared on this owner** [get fixed columns](operations-007.md#op-5e8b1b3a308cbd), [get data](operations-006.md#op-915f75d69ce5f1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0144.json#L5809) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L998) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1345)

<a id="op-915f75d69ce5f1"></a>
### Income Tax Computation Report.get data

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_data`

**Inputs** self.

**Local steps**

- Evaluate self.get\_employee\_details().
- Evaluate self.get\_future\_salary\_slips().
- Evaluate self.get\_gross\_earnings().
- Evaluate self.get\_income\_from\_other\_sources().
- Evaluate self.get\_tax\_exempted\_earnings\_and\_deductions().
- Evaluate self.get\_employee\_tax\_exemptions().
- Evaluate self.get\_hra().
- Evaluate self.get\_standard\_tax\_exemption().
- Evaluate self.get\_total\_taxable\_amount().
- Evaluate self.get\_applicable\_tax().
- Evaluate self.get\_total\_deducted\_tax().
- Evaluate self.get\_payable\_tax().
- Set self.data from list(self.employees.values()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get employee details](operations-006.md#op-7f0ede4e612871), [get future salary slips](operations-006.md#op-6d294d82c01572), [get gross earnings](operations-006.md#op-62764cd6e587cf), [get income from other sources](operations-007.md#op-89234bced46857), [get tax exempted earnings and deductions](operations-006.md#op-381e75a4cc5b26), [get employee tax exemptions](operations-006.md#op-e34481ae993848), [get hra](operations-006.md#op-d74318428cff5c), [get standard tax exemption](operations-007.md#op-cb1082bff95801), [get total taxable amount](operations-007.md#op-87125c5896f901), [get applicable tax](operations-007.md#op-60269cf8cde852), [get total deducted tax](operations-007.md#op-497d03e3607ff3), [get payable tax](operations-007.md#op-30d095b5722afb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0144.json#L5904) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L975) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1322)

<a id="op-7f0ede4e612871"></a>
### Income Tax Computation Report.get employee details

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_employee_details`

**Inputs** self.

**Record and data access** read “Employee” via get\_all.

**Explicit failure paths** validation helper — translated “No employees found with selected filters and active salary structure”.

**Local steps**

- Set filters from self.get\_employee\_filters().
- Set fields from list(“name as employee”, “employee\_name”, “department”, “designation”, …).
- Set employees from Platform.get\_all(“Employee”, filters = filters, fields = fields).
- Set ss\_assignments from self.get\_ss\_assignments(list of d.employee for d drawn from employees).
  - Draw d from employees.
- For each d in employees.
  - If d.employee belongs to list(ss\_assignments.keys()).
    - If getdate(d.date\_of\_joining) &gt; getdate(self.payroll\_period\_end\_date).
      - Continue with the next iteration or loop test.
    - If (d.relieving\_date and getdate(d.relieving\_date) &lt; getdate(self.payroll\_period\_start\_date)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.relieving\_date → getdate(d.relieving\_date) &lt; getdate(self.payroll\_period\_start\_date).
      - Continue with the next iteration or loop test.
    - Evaluate d.update(ss\_assignments at d.employee).
    - Evaluate self.employees.setdefault(d.employee, d).
- If not self.employees.
  - Call the validation error handler Platform.throw(translated “No employees found with selected filters and active salary structure”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get employee filters](operations-006.md#op-564f8255351f28), [get ss assignments](operations-006.md#op-2b1904ab1c1937).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0144.json#L6220) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L978) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1325)

<a id="op-564f8255351f28"></a>
### Income Tax Computation Report.get employee filters

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_employee_filters`

**Inputs** self.

**Explicit results** filters.

**Local steps**

- Set filters from mapping(“company” → self.filters.company).
- If self.filters.employee.
  - Set filters from mapping(“name” → self.filters.employee).
- Otherwise.
  - If self.filters.department.
    - Evaluate filters.update(mapping(“department” → self.filters.department)).
  - Otherwise.
    - If self.filters.employee\_status.
      - Set filters at “status” from self.filters.employee\_status.
- Return filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0144.json#L6772) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L979) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1326)

<a id="op-2b1904ab1c1937"></a>
### Income Tax Computation Report.get ss assignments

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_two_digit_second_assignments`

**Inputs** self, employees.

**Record and data access** read “Salary Structure Assignment” via get\_all · read “Income Tax Slab” via get\_cached\_value.

**Explicit results** employee\_ss\_assignments.

**Local steps**

- Set ss\_assignments from Platform.get\_all(“Salary Structure Assignment”, filters = mapping(“employee” → list(“in”, employees), “docstatus” → 1, “salary\_structure” → list(“is”, “set”), “income\_tax\_slab” → list(“is”, “set”)), fields ….
- Set employee\_ss\_assignments from Platform.\_dict().
- For each d in ss\_assignments.
  - If d.employee does not belong to list(employee\_ss\_assignments.keys()).
    - Set tax\_slab from Platform.get\_cached\_value(“Income Tax Slab”, d.income\_tax\_slab, list(“allow\_tax\_exemption”, “disabled”), as\_dict = 1).
    - If (tax\_slab and not tax\_slab.disabled).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax\_slab → not tax\_slab.disabled.
      - Set opening\_entries\_applicable from getdate(d.from\_date) ≥ getdate(self.payroll\_period\_start\_date).
      - Evaluate employee\_ss\_assignments.setdefault(d.employee, mapping(“salary\_structure” → d.salary\_structure, “income\_tax\_slab” → d.income\_tax\_slab, “allow\_tax\_exemption” → tax\_slab.allow\_tax\_exemption, “total\_exemption ….
        - Value choice on opening\_entries\_applicable — true gives flt(d.taxable\_earnings\_till\_date), false gives 0.0.
        - Value choice on opening\_entries\_applicable — true gives flt(d.tax\_deducted\_till\_date), false gives 0.0.
- Return employee\_ss\_assignments.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Income Tax Slab”, d.income\_tax\_slab, list(“allow\_tax\_exemption”, “disabled”), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L9) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L996) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1343)

<a id="op-6d294d82c01572"></a>
### Income Tax Computation Report.get future salary slips

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_future_salary_slips`

**Inputs** self.

**State and service calls** request new\_doc for “Salary Slip”.

**Local steps**

- Set self.future\_salary\_slips from Platform.\_dict().
- For each employee in list(self.employees.keys()).
  - Set last\_ss from self.get\_last\_salary\_slip(employee).
  - If (last\_ss and last\_ss.end\_date equals self.payroll\_period\_end\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_ss → last\_ss.end\_date equals self.payroll\_period\_end\_date.
    - Continue with the next iteration or loop test.
  - Set relieving\_date from self.employees at employee.get(“relieving\_date”, empty text).
  - If last\_ss.
    - Set ss\_start\_date from add\_days(last\_ss.end\_date, 1).
  - Otherwise.
    - Set ss\_start\_date from self.payroll\_period\_start\_date.
    - Set last\_ss from Platform.\_dict(mapping(“payroll\_frequency” → “Monthly”, “salary\_structure” → self.employees at employee.get(“salary\_structure”))).
  - While (getdate(ss\_start\_date) &lt; getdate(self.payroll\_period\_end\_date) and (not relieving\_date or getdate(ss\_start\_date) &lt; relieving\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(ss\_start\_date) &lt; getdate(self.payroll\_period\_end\_date) → (not relieving\_date or getdate(ss\_start\_date) &lt; relieving\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not relieving\_date → getdate(ss\_start\_date) &lt; relieving\_date.
    - Set ss\_end\_date from get\_start\_end\_dates(last\_ss.payroll\_frequency, ss\_start\_date).end\_date.
    - Set ss from Platform.new\_doc(“Salary Slip”).
    - Set ss.employee from employee.
    - Set ss.start\_date from ss\_start\_date.
    - Set ss.end\_date from ss\_end\_date.
    - Set ss.salary\_structure from last\_ss.salary\_structure.
    - Set ss.payroll\_frequency from last\_ss.payroll\_frequency.
    - Set ss.company from self.filters.company.
    - Attempt the following.
      - Evaluate ss.process\_salary\_structure(for\_preview = 1).
      - Evaluate self.future\_salary\_slips.setdefault(employee, list()).append(ss.as\_dict()).
    - On failure (Exception).
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Set ss\_start\_date from add\_days(ss\_end\_date, 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get last salary slip](operations-006.md#op-a9bd876dffde7a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L983) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1330)

<a id="op-a9bd876dffde7a"></a>
### Income Tax Computation Report.get last salary slip

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_last_salary_slip`

**Inputs** self, employee.

**Record and data access** read “Salary Slip” via get\_value.

**Explicit results** last\_salary\_slip.

**Local steps**

- Set last\_salary\_slip from Platform.db.get\_value(“Salary Slip”, mapping(“employee” → employee, “docstatus” → 1, “start\_date” → list(“between”, list(self.payroll\_period\_start\_date, self.payroll\_period\_end\_date))), list(“name”, “start ….
- Return last\_salary\_slip.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L818) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L987) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1334)

<a id="op-62764cd6e587cf"></a>
### Income Tax Computation Report.get gross earnings

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_gross_earnings`

**Inputs** self.

**Local steps**

- Set ss from Platform.qb.DocType(“Salary Slip”).
- Set existing\_ss from Platform.\_dict(nested operand in the contract.where(nested operand in the contract ≤ nested operand in the contract).groupby(ss.employee).run()).
- For each tuple(employee, employee\_details) in self.employees.items().
  - Set opening\_taxable\_earnings from employee\_details at “taxable\_earnings\_till\_date”.
  - Set future\_ss\_earnings from self.get\_future\_earnings(employee).
  - Set gross\_earnings from ((flt(opening\_taxable\_earnings) + flt(existing\_ss.get(employee))) + future\_ss\_earnings).
  - Evaluate self.employees at employee.setdefault(“gross\_earnings”, gross\_earnings).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get future earnings](operations-006.md#op-1947cc7bc07525).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L1049) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L984) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1331)

<a id="op-1947cc7bc07525"></a>
### Income Tax Computation Report.get future earnings

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_future_earnings`

**Inputs** self, employee.

**Explicit results** future\_earnings.

**Local steps**

- Set future\_earnings from 0.0.
- For each ss in self.future\_salary\_slips.get(employee, list()).
  - Update future\_earnings using + flt(ss.base\_gross\_pay).
- Return future\_earnings.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L1625) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L982) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1329)

<a id="op-381e75a4cc5b26"></a>
### Income Tax Computation Report.get tax exempted earnings and deductions

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_tax_exempted_earnings_and_deductions`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set tax\_exempted\_components from self.get\_tax\_exempted\_components().
- If not tax\_exempted\_components.
  - Return no value.
- Set ss from Platform.qb.DocType(“Salary Slip”).
- Set ss\_comps from Platform.qb.DocType(“Salary Detail”).
- Set records from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.end\_date ≤ nested operand in the contract.payroll\_period\_end\_date).groupby(ss.employee, ss\_comps.salary\_c ….
- Set existing\_ss\_exemptions from Platform.\_dict().
- For each d in records.
  - Evaluate existing\_ss\_exemptions.setdefault(d.employee, mapping()).setdefault(scrub(d.salary\_component), d.amount).
- For each employee in list(self.employees.keys()).
  - If not self.employees at employee at “allow\_tax\_exemption”.
    - Continue with the next iteration or loop test.
  - Set exemptions from existing\_ss\_exemptions.get(employee, mapping()).
  - Evaluate self.add\_exemptions\_from\_future\_salary\_slips(employee, exemptions).
  - Evaluate self.employees at employee.update(exemptions).
  - Set total\_exemptions from sum(list(exemptions.values())).
  - Set self.employees at employee at “total\_exemption” from 0.
  - Update self.employees at employee at “total\_exemption” using + total\_exemptions.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get tax exempted components](operations-006.md#op-d5d2029f26c70d), [add exemptions from future salary slips](operations-006.md#op-531956bb2e325a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L1750) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L992) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1339)

<a id="op-531956bb2e325a"></a>
### Income Tax Computation Report.add exemptions from future salary slips

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_add_exemptions_from_future_salary_slips`

**Inputs** self, employee, exemptions.

**Explicit results** exemptions.

**Local steps**

- For each ss in self.future\_salary\_slips.get(employee, list()).
  - For each e in ss.earnings.
    - If not e.is\_tax\_applicable.
      - Evaluate exemptions.setdefault(scrub(e.salary\_component), 0).
      - Update exemptions at scrub(e.salary\_component) using + flt(e.amount).
  - For each d in ss.deductions.
    - If d.exempted\_from\_income\_tax.
      - Evaluate exemptions.setdefault(scrub(d.salary\_component), 0).
      - Update exemptions at scrub(d.salary\_component) using + flt(d.amount).
- Return exemptions.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L2745) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L973) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1320)

<a id="op-d5d2029f26c70d"></a>
### Income Tax Computation Report.get tax exempted components

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_tax_exempted_components`

**Inputs** self.

**Record and data access** read “Salary Component” via get\_all.

**Explicit results** tax\_exempted\_components.

**Local steps**

- Set nontaxable\_earning\_components from list of d.name for d drawn from Platform.get\_all(“Salary Component”, mapping(“type” → “Earning”, “is\_tax\_applicable” → 0, “disabled” → 0)).
  - Draw d from Platform.get\_all(“Salary Component”, mapping(“type” → “Earning”, “is\_tax\_applicable” → 0, “disabled” → 0)).
- Set tax\_exempted\_deduction\_components from list of d.name for d drawn from Platform.get\_all(“Salary Component”, mapping(“type” → “Deduction”, “exempted\_from\_income\_tax” → 1, “disabled” → 0)).
  - Draw d from Platform.get\_all(“Salary Component”, mapping(“type” → “Deduction”, “exempted\_from\_income\_tax” → 1, “disabled” → 0)).
- Set tax\_exempted\_components from (nontaxable\_earning\_components + tax\_exempted\_deduction\_components).
- For each d in tax\_exempted\_components.
  - Evaluate self.add\_column(d).
- Return tax\_exempted\_components.

**Methods declared on this owner** [add column](operations-007.md#op-ec2101c0cba054).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L3098) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L991) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1338)

<a id="op-e34481ae993848"></a>
### Income Tax Computation Report.get employee tax exemptions

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_employee_tax_exemptions`

**Inputs** self.

**Record and data access** read “Employee Tax Exemption Category” via get\_all.

**Local steps**

- Set exemption\_categories from Platform.get\_all(“Employee Tax Exemption Category”, mapping(“is\_active” → 1)).
- For each d in exemption\_categories.
  - Evaluate self.add\_column(d.name).
- Set self.employees\_with\_proofs from list().
- Evaluate self.get\_tax\_exemptions(“Employee Tax Exemption Proof Submission”).
- If self.filters.consider\_tax\_exemption\_declaration.
  - Evaluate self.get\_tax\_exemptions(“Employee Tax Exemption Declaration”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add column](operations-007.md#op-ec2101c0cba054), [get tax exemptions](operations-006.md#op-96ea7ac4c6773f).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L3422) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L980) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1327)

<a id="op-96ea7ac4c6773f"></a>
### Income Tax Computation Report.get tax exemptions

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_tax_exemptions`

**Inputs** self, source.

**Local steps**

- If source equals “Employee Tax Exemption Proof Submission”.
  - Set child\_doctype from “Employee Tax Exemption Proof Submission Detail”.
- Otherwise.
  - Set child\_doctype from “Employee Tax Exemption Declaration Category”.
- Set max\_exemptions from self.get\_max\_exemptions\_based\_on\_category().
- Set par from Platform.qb.DocType(source).
- Set child from Platform.qb.DocType(child\_doctype).
- Set records from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.payroll\_period equals nested operand in the contract.payroll\_period).groupby(par.employee, child.exemptio ….
- For each d in records.
  - If not self.employees at d.employee at “allow\_tax\_exemption”.
    - Continue with the next iteration or loop test.
  - If (source equals “Employee Tax Exemption Declaration” and d.employee belongs to self.employees\_with\_proofs).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in source equals “Employee Tax Exemption Declaration” → d.employee belongs to self.employees\_with\_proofs.
    - Continue with the next iteration or loop test.
  - Set amount from flt(d.amount).
  - Set max\_eligible\_amount from flt(max\_exemptions.get(d.exemption\_category)).
  - If (max\_eligible\_amount and amount &gt; max\_eligible\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_eligible\_amount → amount &gt; max\_eligible\_amount.
    - Set amount from max\_eligible\_amount.
  - Evaluate self.employees at d.employee.setdefault(scrub(d.exemption\_category), amount).
  - Update self.employees at d.employee at “total\_exemption” using + amount.
  - If (source equals “Employee Tax Exemption Proof Submission” and d.employee does not belong to self.employees\_with\_proofs).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in source equals “Employee Tax Exemption Proof Submission” → d.employee does not belong to self.employees\_with\_proofs.
    - Evaluate self.employees\_with\_proofs.append(d.employee).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get max exemptions based on category](operations-006.md#op-df41b07ae08f68).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L3650) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L993) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1340)

<a id="op-df41b07ae08f68"></a>
### Income Tax Computation Report.get max exemptions based on category

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_maximum_exemptions_based_on_category`

**Inputs** self.

**Record and data access** read “Employee Tax Exemption Category” via get\_all.

**Explicit results** dict(Platform.get\_all(“Employee Tax Exemption Category”, filters = mapping(“is\_active” → 1), fields = list(“name”, “max\_amount”), as\_list = 1)).

**Local steps**

- Return dict(Platform.get\_all(“Employee Tax Exemption Category”, filters = mapping(“is\_active” → 1), fields = list(“name”, “max\_amount”), as\_list = 1)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L4603) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L988) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1335)

<a id="op-d74318428cff5c"></a>
### Income Tax Computation Report.get hra

`operation_workforce_payroll_report_income_tax_computation_business_behavior_income_tax_computation_report_get_hra`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not Platform.get\_meta(“Employee Tax Exemption Declaration”).has\_field(“monthly\_house\_rent”).
  - Return no value.
- Evaluate self.add\_column(“HRA”).
- Set self.employees\_with\_proofs from list().
- Evaluate self.get\_eligible\_hra(“Employee Tax Exemption Proof Submission”).
- If self.filters.consider\_tax\_exemption\_declaration.
  - Evaluate self.get\_eligible\_hra(“Employee Tax Exemption Declaration”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add column](operations-007.md#op-ec2101c0cba054), [get eligible hra](operations-007.md#op-c7963d73b25818).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0145.json#L4741) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L985) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1332)
