# Payroll and benefits · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Salary component

[Record definition](../../../../data/record-types/salary_component.json)

<a id="op-a49889718f1b2c"></a>
### Salary Component.before validate

`operation_workforce_payroll_record_definitions_salary_component_business_behavior_salary_component_before_validate`

**Inputs** self.

**Local steps**

- Set tuple(self.\_condition, self.condition) from tuple(self.condition, sanitize\_expression(self.condition)).
- Set tuple(self.\_formula, self.formula) from tuple(self.formula, sanitize\_expression(self.formula)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L5792) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L604) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L951)

<a id="op-1b0e392986c416"></a>
### Salary Component.validate

`operation_workforce_payroll_record_definitions_salary_component_business_behavior_salary_component_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_abbr().
- Evaluate self.validate\_accounts().
- Evaluate self.validate\_accrual\_component().
- Evaluate self.valide\_arrear\_component().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate abbr](operations-012.md#op-e88722baab9218), [validate accounts](operations-012.md#op-3cb3837e9ac64b), [validate accrual component](operations-012.md#op-5446e3ddf19c84), [valide arrear component](operations-012.md#op-ea85043e96f2d6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L5944) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L609) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L956)

<a id="op-912313c5ae915b"></a>
### Salary Component.on update

`operation_workforce_payroll_record_definitions_salary_component_business_behavior_salary_component_on_update`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- If self.\_condition differs from self.condition.
  - Evaluate self.db\_set(“condition”, self.\_condition).
- If self.\_formula differs from self.formula.
  - Evaluate self.db\_set(“formula”, self.\_formula).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L6055) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L607) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L954)

<a id="op-dcaf292176c57a"></a>
### Salary Component.clear cache

`operation_workforce_payroll_record_definitions_salary_component_business_behavior_salary_component_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Bind dependencies SALARY\_COMPONENT\_VALUES, TAX\_COMPONENTS\_BY\_COMPANY.
- Evaluate Platform.cache().delete\_value(SALARY\_COMPONENT\_VALUES).
- Evaluate Platform.cache().delete\_value(TAX\_COMPONENTS\_BY\_COMPANY).
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L6217) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L605) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L952)

<a id="op-e88722baab9218"></a>
### Salary Component.validate abbr

`operation_workforce_payroll_record_definitions_salary_component_business_behavior_salary_component_validate_abbreviation`

**Inputs** self.

**Local steps**

- If not self.salary\_component\_abbr.
  - Set self.salary\_component\_abbr from empty text.join(list of c at 0 for c drawn from nested operand in the contract.salary\_component.split()).upper().
    - Draw c from self.salary\_component.split().
- Set self.salary\_component\_abbr from self.salary\_component\_abbr.strip().
- Set self.salary\_component\_abbr from append\_number\_if\_name\_exists(“Salary Component”, self.salary\_component\_abbr, “salary\_component\_abbr”, separator = “\_”, filters = mapping(“name” → list(“!=”, self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L6353) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L610) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L957)

<a id="op-3cb3837e9ac64b"></a>
### Salary Component.validate accounts

`operation_workforce_payroll_record_definitions_salary_component_business_behavior_salary_component_validate_accounts`

**Inputs** self.

**State and service calls** msgprint.

**Local steps**

- If not (self.statistical\_component or (self.accounts and all(generator of d.account for d drawn from self.accounts))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.statistical\_component → (self.accounts and all(generator of d.account for d drawn from self.accounts)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.accounts → all(generator of d.account for d drawn from self.accounts).
  - Draw d from self.accounts.
  - Evaluate Platform.msgprint(title = translated “Warning”, msg = translated “Accounts not set for Salary Component {0}”.format(self.name), indicator = “orange”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L6637) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L611) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L958)

<a id="op-5446e3ddf19c84"></a>
### Salary Component.validate accrual component

`operation_workforce_payroll_record_definitions_salary_component_business_behavior_salary_component_validate_accrual_component`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Accrual Component can only be set for Earning Salary Components.” · validation helper — translated “Accrual Component must be set for Flexible Benefit Salary Components with accrual payout methods.” · validation helper — translated “Accrual Component can only be set for Flexible Benefit Salary Components with accrual payout methods.”.

**Local steps**

- If (self.type differs from “Earning” and self.accrual\_component).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.type differs from “Earning” → self.accrual\_component.
  - Call the validation error handler Platform.throw(translated “Accrual Component can only be set for Earning Salary Components.”, title = translated “Invalid Accrual Component”).
- If self.is\_flexible\_benefit.
  - Set requires\_accrual from self.payout\_method belongs to list(“Accrue and payout at end of payroll period”, “Accrue per cycle, pay only on claim”).
  - If (requires\_accrual and not self.accrual\_component).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in requires\_accrual → not self.accrual\_component.
    - Call the validation error handler Platform.throw(translated “Accrual Component must be set for Flexible Benefit Salary Components with accrual payout methods.”, title = translated “Invalid Accrual Component”).
  - If (not requires\_accrual and self.accrual\_component).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not requires\_accrual → self.accrual\_component.
    - Call the validation error handler Platform.throw(translated “Accrual Component can only be set for Flexible Benefit Salary Components with accrual payout methods.”, title = translated “Invalid Accrual Component”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0122.json#L6849) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L612) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L959)

<a id="op-ea85043e96f2d6"></a>
### Salary Component.valide arrear component

`operation_workforce_payroll_record_definitions_salary_component_business_behavior_salary_component_valide_arrear_component`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Arrear Component cannot be set for Salary Components based on taxable salary.”.

**Local steps**

- If (self.variable\_based\_on\_taxable\_salary and self.arrear\_component).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.variable\_based\_on\_taxable\_salary → self.arrear\_component.
  - Call the validation error handler Platform.throw(translated “Arrear Component cannot be set for Salary Components based on taxable salary.”, title = translated “Invalid Arrear Component”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L613) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L960)

<a id="op-69d55976ee0463"></a>
### Salary Component.get structures to be updated

`operation_workforce_payroll_record_definitions_salary_component_business_behavior_salary_component_get_structures_to_be_updated`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** nested operand in the contract(nested operand in the contract).select(SalaryStructure.name).where((SalaryDetail.salary\_component equals self.name bitwise and SalaryStructure.docstatus differs from 2)).run( ….

**Local steps**

- Set SalaryStructure from Platform.qb.DocType(“Salary Structure”).
- Set SalaryDetail from Platform.qb.DocType(“Salary Detail”).
- Return nested operand in the contract(nested operand in the contract).select(SalaryStructure.name).where((SalaryDetail.salary\_component equals self.name bitwise and SalaryStructure.docstatus differs from 2)).run( ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L128) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L606) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L953)

<a id="op-81491417e86f81"></a>
### Salary Component.update salary structures

`operation_workforce_payroll_record_definitions_salary_component_business_behavior_salary_component_update_salary_structures`

**Inputs** self, field, value, structures = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from “Salary Structure” via get\_doc.

**Local steps**

- Set is\_formula\_related from field equals “formula”.
- If not structures.
  - Set structures from self.get\_structures\_to\_be\_updated().
- For each structure in structures.
  - Evaluate Platform.has\_permission(“Salary Structure”, “write”, structure, throw = true).
  - Set salary\_structure from Platform.get\_doc(“Salary Structure”, structure).
  - Set salary\_structure.\_doc\_before\_save from copy.deepcopy(salary\_structure).
  - Set salary\_detail\_row from next(generator of d for d drawn from salary\_structure.get(COMPONENT\_TYPE\_TO\_PARENTFIELD at self.type) where d.salary\_component equals self.name, no value).
    - Draw d from salary\_structure.get(COMPONENT\_TYPE\_TO\_PARENTFIELD at self.type), keep a combination only if (d.salary\_component equals self.name).
  - If not salary\_detail\_row.
    - Continue with the next iteration or loop test.
  - If is\_formula\_related.
    - Set value from value when self.amount\_based\_on\_formula, otherwise no value.
      - Value choice on self.amount\_based\_on\_formula — true gives value, false gives no value.
    - Evaluate salary\_detail\_row.set(“amount\_based\_on\_formula”, self.amount\_based\_on\_formula).
  - Evaluate salary\_detail\_row.set(field, value).
  - Evaluate salary\_structure.db\_update\_all().
  - Set salary\_structure.flags.updater\_reference from mapping(“doctype” → self.doctype, “docname” → self.name, “label” → translated “via Salary Component sync”).
  - Evaluate salary\_structure.save\_version().
  - Evaluate salary\_structure.clear\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get structures to be updated](operations-012.md#op-69d55976ee0463).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Salary Structure”, “write”, structure, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L453) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L608) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L955)

## Report · Salary payments based on payment mode

<a id="op-ceee1bf00fe978"></a>
### Execute

`operation_workforce_payroll_report_salary_payments_based_on_payment_mode_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(list(), list()) · tuple(columns, data, no value, chart, …).

**Local steps**

- Set mode\_of\_payments from get\_payment\_modes().
- If not len(mode\_of\_payments).
  - Return tuple(list(), list()).
- Set columns from get\_columns(filters, mode\_of\_payments).
- Set tuple(data, total\_rows, report\_summary) from get\_data(filters, mode\_of\_payments).
- Set chart from get\_chart(mode\_of\_payments, total\_rows).
- Return tuple(columns, data, no value, chart, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0148.json#L1943) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1022) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1360)

<a id="op-05a5f3ee027ac0"></a>
### Get columns

`operation_workforce_payroll_report_salary_payments_based_on_payment_mode_business_behavior_get_columns`

**Inputs** filters, mode\_of\_payments.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Branch”, “options” → “Branch”, “fieldname” → “branch”, “fieldtype” → “Link”, …)).
- For each mode in mode\_of\_payments.
  - Evaluate columns.append(mapping(“label” → translated mode, “fieldname” → mode, “fieldtype” → “Currency”, “width” → 160)).
- Evaluate columns.append(mapping(“label” → translated “Total”, “fieldname” → “total”, “fieldtype” → “Currency”, “width” → 140)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0148.json#L2175) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1024) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1362)

<a id="op-1cf2c3ca55f405"></a>
### Get payment modes

`operation_workforce_payroll_report_salary_payments_based_on_payment_mode_business_behavior_get_payment_modes`

**Inputs** no declared parameters.

**Explicit results** mode\_of\_payments.

**Local steps**

- Set SalarySlip from DocType(“Salary Slip”).
- Set mode\_of\_payments from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.docstatus equals 1).distinct().run(pluck = true).
- Return mode\_of\_payments.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0148.json#L2580) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1026) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1364)

<a id="op-27b1184091e37d"></a>
### Prepare data

`operation_workforce_payroll_report_salary_payments_based_on_payment_mode_business_behavior_prepare_data`

**Inputs** entry.

**Explicit results** tuple(branch\_wise\_entries, gross\_pay).

**Local steps**

- Set branch\_wise\_entries from mapping().
- Set gross\_pay from 0.
- For each d in entry.
  - Update gross\_pay using + d.gross\_pay.
  - If branch\_wise\_entries.get(d.branch).
    - Set branch\_wise\_entries at d.branch at d.mode\_of\_payment from d.net\_pay.
  - Otherwise.
    - Evaluate branch\_wise\_entries.setdefault(d.branch, mapping()).setdefault(d.mode\_of\_payment, d.net\_pay).
- Return tuple(branch\_wise\_entries, gross\_pay).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0148.json#L2760) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1029) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1367)

<a id="op-57027f9df79ced"></a>
### Get data

`operation_workforce_payroll_report_salary_payments_based_on_payment_mode_business_behavior_get_data`

**Inputs** filters, mode\_of\_payments.

**Explicit results** tuple(data, total\_row, report\_summary).

**Local steps**

- Set data from list().
- Set SalarySlip from DocType(“Salary Slip”).
- Set filter\_clauses from get\_conditions(filters).
- Set base\_where from SalarySlip.docstatus equals 1.
- For each clause in filter\_clauses.
  - Set base\_where from (base\_where bitwise and clause).
- Set entry from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(base\_where).groupby(SalarySlip.branch, S ….
- Set tuple(branch\_wise\_entries, gross\_pay) from prepare\_data(entry).
- Set branches from nested operand in the contract(nested operand in the contract).where(base\_where).distinct().run(pluck = true).
- Set total\_row from mapping(“total” → 0, “branch” → “Total”).
- For each branch in branches.
  - Set total from 0.
  - Set row from mapping(“branch” → branch).
  - For each mode in mode\_of\_payments.
    - If branch\_wise\_entries.get(branch).get(mode).
      - Set row at mode from branch\_wise\_entries.get(branch).get(mode).
      - Update total using + branch\_wise\_entries.get(branch).get(mode).
  - Set row at “total” from total.
  - Evaluate data.append(row).
- Set total\_row from get\_total\_based\_on\_mode\_of\_payment(data, mode\_of\_payments).
- Set total\_deductions from (gross\_pay − total\_row.get(“total”)).
- Set report\_summary from list().
- If data.
  - Evaluate data.append(total\_row).
  - Evaluate data.append(mapping()).
  - Evaluate data.append(mapping(“branch” → “Total Gross Pay”, mode\_of\_payments at 0 → gross\_pay)).
  - Evaluate data.append(mapping(“branch” → “Total Deductions”, mode\_of\_payments at 0 → total\_deductions)).
  - Evaluate data.append(mapping(“branch” → “Total Net Pay”, mode\_of\_payments at 0 → total\_row.get(“total”))).
  - Set currency from Enterprise.get\_company\_currency(filters.company).
  - Set report\_summary from get\_report\_summary(gross\_pay, total\_deductions, total\_row.get(“total”), currency).
- Return tuple(data, total\_row, report\_summary).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0148.json#L2993) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1025) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1363)

<a id="op-cefac91352e5e4"></a>
### Get total based on mode of payment

`operation_workforce_payroll_report_salary_payments_based_on_payment_mode_business_behavior_get_total_based_on_mode_of_payment`

**Inputs** data, mode\_of\_payments.

**Explicit results** total\_row.

**Local steps**

- Set total from 0.
- Set total\_row from mapping(“branch” → “Total”).
- For each mode in mode\_of\_payments.
  - Set sum\_of\_payment from sum(list of detail at mode for detail drawn from data where mode belongs to detail.keys()).
    - Draw detail from data, keep a combination only if (mode belongs to detail.keys()).
  - Set total\_row at mode from sum\_of\_payment.
  - Update total using + sum\_of\_payment.
- Set total\_row at “total” from total.
- Return total\_row.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0148.json#L4278) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1028) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1366)

<a id="op-55e1dde07f4ec8"></a>
### Get report summary

`operation_workforce_payroll_report_salary_payments_based_on_payment_mode_business_behavior_get_report_summary`

**Inputs** gross\_pay, total\_deductions, net\_pay, currency.

**Explicit results** list(mapping(“value” → gross\_pay, “label” → translated “Total Gross Pay”, “indicator” → “Green”, “datatype” → “Currency”, …), mapping(“value” → total\_deductions, “label” → translated “Total Deduction”, “da ….

**Local steps**

- Return list(mapping(“value” → gross\_pay, “label” → translated “Total Gross Pay”, “indicator” → “Green”, “datatype” → “Currency”, …), mapping(“value” → total\_deductions, “label” → translated “Total Deduction”, “da ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0148.json#L4516) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1027) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1365)

<a id="op-924fbc0d795cce"></a>
### Get chart

`operation_workforce_payroll_report_salary_payments_based_on_payment_mode_business_behavior_get_chart`

**Inputs** mode\_of\_payments, data.

**Explicit results** chart.

**Local steps**

- If data.
  - Set values from list().
  - Set labels from list().
  - For each mode in mode\_of\_payments.
    - Evaluate values.append(data at mode).
    - Evaluate labels.append(list(mode)).
  - Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → “Mode Of Payments”, “values” → values)))).
  - Set chart at “type” from “bar”.
  - Return chart.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0148.json#L4871) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1023) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1361)

## Report · Salary payments via ecs

<a id="op-1ae79536e3b5ed"></a>
### Execute

`operation_workforce_payroll_report_salary_payments_via_electronic_clearing_service_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0148.json#L5136) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1030) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1368)

<a id="op-7ba123026b23ee"></a>
### Get columns

`operation_workforce_payroll_report_salary_payments_via_electronic_clearing_service_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Branch”, “options” → “Branch”, “fieldname” → “branch”, “fieldtype” → “Link”, …), mapping(“label” → translated “Employee Name”, “options” → “Employee”, “fieldname” → “empl ….
- If Enterprise.get\_region() equals “India”.
  - Update columns using + list(mapping(“label” → translated “IFSC”, “fieldname” → “ifsc”, “fieldtype” → “Data”, “width” → 140), mapping(“label” → translated “MICR”, “fieldname” → “micr”, “fieldtype” → “Data”, “width” → 140)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0148.json#L5240) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1031) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1369)

<a id="op-a8b85ba9753c3c"></a>
### Get conditions

`operation_workforce_payroll_report_salary_payments_via_electronic_clearing_service_business_behavior_get_conditions`

**Inputs** filters.

**Explicit results** filter\_clauses.

**Local steps**

- Set SalarySlip from DocType(“Salary Slip”).
- Set filter\_clauses from list().
- If filters.get(“department”).
  - Evaluate filter\_clauses.append(SalarySlip.department equals filters at “department”).
- If filters.get(“branch”).
  - Evaluate filter\_clauses.append(SalarySlip.branch equals filters at “branch”).
- If filters.get(“company”).
  - Evaluate filter\_clauses.append(SalarySlip.company equals filters at “company”).
- If filters.get(“month”).
  - Evaluate filter\_clauses.append(Extract(“month”, SalarySlip.start\_date) equals int(filters at “month”)).
- If filters.get(“year”).
  - Evaluate filter\_clauses.append(Extract(“year”, SalarySlip.start\_date) equals int(filters at “year”)).
- Return filter\_clauses.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0148.json#L6239) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1032) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1370)

<a id="op-029827a5c4b93c"></a>
### Get data

`operation_workforce_payroll_report_salary_payments_via_electronic_clearing_service_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Employee” via get\_list.

**Explicit results** data.

**Local steps**

- Set SalarySlip from DocType(“Salary Slip”).
- Set filter\_clauses from get\_conditions(filters).
- Set fields from list(“employee”, “branch”, “bank\_name”, “bank\_ac\_no”, …).
- If Enterprise.get\_region() equals “India”.
  - Update fields using + list(“ifsc\_code”, “micr\_code”).
- Set employee\_details from Platform.get\_list(“Employee”, fields = fields).
- Set employee\_data\_dict from mapping().
- For each d in employee\_details.
  - Evaluate employee\_data\_dict.setdefault(d.employee, mapping(“bank\_ac\_no” → d.bank\_ac\_no, “ifsc\_code” → (d.ifsc\_code or no value), “micr\_code” → (d.micr\_code or no value), “branch” → d.branch, …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.ifsc\_code → no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.micr\_code → no value.
- Set base\_where from SalarySlip.docstatus equals 1.
- For each clause in filter\_clauses.
  - Set base\_where from (base\_where bitwise and clause).
- Set entry from nested operand in the contract(nested operand in the contract).select(SalarySlip.employee, SalarySlip.employee\_name, SalarySlip.gross\_pay, SalarySlip.net\_pay).where(base\_where).run(as\_dict = true).
- Set data from list().
- For each d in entry.
  - Set employee from mapping(“branch” → employee\_data\_dict.get(d.employee).get(“branch”), “employee\_name” → d.employee\_name, “employee” → d.employee, “gross\_pay” → d.gross\_pay, …).
  - If employee\_data\_dict.get(d.employee).get(“salary\_mode”) equals “Bank”.
    - Set employee at “bank” from employee\_data\_dict.get(d.employee).get(“bank\_name”).
    - Set employee at “account\_no” from employee\_data\_dict.get(d.employee).get(“bank\_ac\_no”).
    - If Enterprise.get\_region() equals “India”.
      - Set employee at “ifsc” from employee\_data\_dict.get(d.employee).get(“ifsc\_code”).
      - Set employee at “micr” from employee\_data\_dict.get(d.employee).get(“micr\_code”).
  - Otherwise.
    - Set employee at “account\_no” from employee\_data\_dict.get(d.employee).get(“salary\_mode”).
  - If (filters.get(“type”) and employee\_data\_dict.get(d.employee).get(“salary\_mode”) equals filters.get(“type”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“type”) → employee\_data\_dict.get(d.employee).get(“salary\_mode”) equals filters.get(“type”).
    - Evaluate data.append(employee).
  - Otherwise.
    - If not filters.get(“type”).
      - Evaluate data.append(employee).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0149.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1033) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1371)

## Report · Salary register

<a id="op-99d6cea1cd3fbd"></a>
### Execute

`operation_workforce_payroll_report_salary_register_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(list(), list()) · tuple(columns, data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set currency from no value.
- If filters.get(“currency”).
  - Set currency from filters.get(“currency”).
- Set company\_currency from Enterprise.get\_company\_currency(filters.get(“company”)).
- Set salary\_slips from get\_salary\_slips(filters, company\_currency).
- If not salary\_slips.
  - Return tuple(list(), list()).
- Set parentfields from get\_active\_parentfields(filters).
- Set components from get\_components\_by\_parentfield(salary\_slips, parentfields).
- Set fieldnames from get\_component\_fieldnames(components, parentfields).
- Set columns from get\_columns(components, fieldnames).
- Set component\_maps from mapping of parentfield → get\_salary\_slip\_details(salary\_slips, currency, company\_currency, parentfield) for parentfield drawn from parentfields.
  - Draw parentfield from parentfields.
- Set doj\_map from get\_employee\_doj\_map().
- Set data from list().
- For each ss in salary\_slips.
  - Set row from mapping(“salary\_slip\_id” → ss.name, “employee” → ss.employee, “employee\_name” → ss.employee\_name, “data\_of\_joining” → doj\_map.get(ss.employee), …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in currency → company\_currency.
  - Evaluate update\_column\_width(ss, columns).
  - For each parentfield in parentfields.
    - Set amounts from component\_maps at parentfield.get(ss.name, mapping()).
    - For each tuple(component, amount) in amounts.items().
      - Set fieldname from fieldnames.get(tuple(parentfield, component)).
      - If fieldname.
        - Set row at fieldname from amount.
  - If components at “employer\_contributions”.
    - Evaluate row.update(mapping(“total\_employer\_contribution” → sum(nested operand in the contract.get(nested operand in the contract.name, mapping()).values()))).
  - If currency equals company\_currency.
    - Evaluate row.update(mapping(“gross\_pay” → (flt(ss.gross\_pay) × flt(ss.exchange\_rate)), “total\_deduction” → ((flt(ss.total\_deduction) + flt(ss.total\_loan\_repayment)) × flt(ss.exchange\_rate)), “net\_pay” → (flt(ss.net ….
  - Otherwise.
    - Evaluate row.update(mapping(“gross\_pay” → ss.gross\_pay, “total\_deduction” → (flt(ss.total\_deduction) + flt(ss.total\_loan\_repayment)), “net\_pay” → ss.net\_pay)).
  - Evaluate data.append(row).
- Return tuple(columns, data).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L10) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1034) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1372)

<a id="op-86a23a69b3f57f"></a>
### Get active parentfields

`operation_workforce_binding_workforce_payroll_report_salary_register_salary_register_get_active_parentfields`

**Inputs** filters.

**Explicit results** COMPONENT\_PARENTFIELDS · tuple(“earnings”, “deductions”).

**Local steps**

- If filters.get(“show\_employer\_contributions”).
  - Return COMPONENT\_PARENTFIELDS.
- Return tuple(“earnings”, “deductions”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L180) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L231) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L231)
