# Payroll and benefits · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Employee ctc break up

<a id="op-f6b157c27767fb"></a>
### Salary Breakup Report.set employer contribution details

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_set_employer_contribution_details`

**Inputs** self.

**Record and data access** resolve a document from “Salary Structure Assignment” via get\_cached\_doc.

**Local steps**

- Set evaluated\_components from getattr(self.salary\_slip, “\_evaluated\_components”, no value).
- If evaluated\_components is identical to no value.
  - Set evaluated\_components from Platform.get\_cached\_doc(“Salary Structure Assignment”, self.salary\_structure\_assignment).get\_evaluated\_components().
- Update self.salary\_components using + list of mapping(“salary\_component” → component.salary\_component, “per\_cycle” → flt(component.default\_amount), “abbr” → component.abbr, “amount\_based\_on\_formula” → component.amount\_based\_on\_formula, …) for  ….
  - Draw component from evaluated\_components at “employer\_contributions”, keep a combination only if ((not component.statistical\_component and component.condition\_met)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not component.statistical\_component → component.condition\_met.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self.salary\_slip, “\_evaluated\_components”, no value) · configured or stored value from Platform.get\_cached\_doc(“Salary Structure Assignment”, self.salary\_structure\_assignment).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L8) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L957) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1304)

<a id="op-c5b5f9896a6008"></a>
### Salary Breakup Report.calculate yearly amounts and percent of ctc

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_calculate_yearly_amounts_and_percent_of_cost_to_company`

**Inputs** self.

**Local steps**

- For each component in self.salary\_components.
  - Set annual\_amount from (component.get(“per\_cycle”, 0) × self.cycle\_multiplier).
  - Evaluate component.update(mapping(“annual” → flt(annual\_amount, 2), “percent\_of\_ctc” → self.calculate\_percent\_of\_ctc(annual\_amount))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate percent of ctc](operations-004.md#op-863040465a2fba).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L947) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1294)

<a id="op-c2decef97121d8"></a>
### Salary Breakup Report.separate salary components by type

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_separate_salary_components_by_type`

**Inputs** self.

**Local steps**

- Set self.earning\_components from list of component for component drawn from self.salary\_components where component.get(“component\_type”) equals “earnings”.
  - Draw component from self.salary\_components, keep a combination only if (component.get(“component\_type”) equals “earnings”).
- Set self.deduction\_components from list of component for component drawn from self.salary\_components where (component.get(“component\_type”) equals “deductions” and not component.get(“is\_tax\_component”)).
  - Draw component from self.salary\_components, keep a combination only if ((component.get(“component\_type”) equals “deductions” and not component.get(“is\_tax\_component”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in component.get(“component\_type”) equals “deductions” → not component.get(“is\_tax\_component”).
- Set self.tax\_components from list of component for component drawn from self.salary\_components where component.get(“is\_tax\_component”).
  - Draw component from self.salary\_components, keep a combination only if (component.get(“is\_tax\_component”)).
- Set self.employer\_contribution\_components from list of component for component drawn from self.salary\_components where component.get(“component\_type”) equals “employer\_contributions”.
  - Draw component from self.salary\_components, keep a combination only if (component.get(“component\_type”) equals “employer\_contributions”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L182) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L955) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1302)

<a id="op-d027496ece863c"></a>
### Salary Breakup Report.set abbr type and formula

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_set_abbreviation_type_and_formula`

**Inputs** self.

**Local steps**

- For each component in ((self.earning\_components + self.deduction\_components) + self.employer\_contribution\_components).
  - Set component at “salary\_component” from formatted text {component.get(“salary\_component”)} ({component.get(“abbr”)}).
  - Set component at “type” from “Formula” when component.get(“amount\_based\_on\_formula”), otherwise “Fixed”.
    - Value choice on component.get(“amount\_based\_on\_formula”) — true gives “Formula”, false gives “Fixed”.
  - Set component at “formula” from (component.get(“formula”) or “-”) when component.get(“amount\_based\_on\_formula”), otherwise (component.get(“per\_cycle”) or “-”).
    - Value choice on component.get(“amount\_based\_on\_formula”) — true gives (component.get(“formula”) or “-”), false gives (component.get(“per\_cycle”) or “-”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in component.get(“formula”) → “-”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in component.get(“per\_cycle”) → “-”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L530) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L956) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1303)

<a id="op-8633805aa1a959"></a>
### Salary Breakup Report.set totals row for component types

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_set_totals_row_for_component_types`

**Inputs** self.

**Local steps**

- Bind local operation calculate\_total for subsequent calls.
- Bind local operation set\_totals\_row for subsequent calls.
- For each component\_type in tuple(“Earnings”, “Deductions”, “Tax Deductions”, “Employer Contributions”).
  - Evaluate set\_totals\_row(component\_type).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L868) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L960) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1307)

<a id="op-5e8a90a7226e82"></a>
### Salary Breakup Report.set totals row for component types.calculate total

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_set_totals_row_for_component_types_calculate_total`

**Inputs** period, components.

**Explicit results** total.

**Local steps**

- Set total from 0.
- For each component in components.
  - Update total using + component.get(period).
- Return total.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L1355) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L961) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1308)

<a id="op-02eb0780a910d0"></a>
### Salary Breakup Report.set totals row for component types.set totals row

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_set_totals_row_for_component_types_set_totals_row`

**Inputs** component\_type.

**State and service calls** call insert on components.

**Local steps**

- Set components from mapping(“Earnings” → self.earning\_components, “Deductions” → self.deduction\_components, “Tax Deductions” → self.tax\_components, “Employer Contributions” → self.employer\_contribution\_components).get(component\_type).
- Set totals\_row from mapping(“salary\_component” → component\_type, “type” → empty text, “formula” → empty text, “bold” → true, …).
- Evaluate components.insert(0, totals\_row).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L1456) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L962) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1309)

<a id="op-42055dd6e4bf87"></a>
### Salary Breakup Report.set net and gross earning rows

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_set_net_and_gross_earning_rows`

**Inputs** self.

**Local steps**

- Set self.total\_net\_earnings from list(mapping(“salary\_component” → “Total Net Earnings”, “type” → empty text, “formula” → empty text, “per\_cycle” → self.net\_pay, …)).
- Set self.total\_gross\_earnings from list(mapping(“salary\_component” → “Total Gross Earnings”, “type” → empty text, “formula” → empty text, “per\_cycle” → self.gross\_pay, …)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate percent of ctc](operations-004.md#op-863040465a2fba).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L1786) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L958) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1305)

<a id="op-863040465a2fba"></a>
### Salary Breakup Report.calculate percent of ctc

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_calculate_percent_of_cost_to_company`

**Inputs** self, amount.

**Explicit results** flt(((amount × 100) ÷ self.ctc), 2).

**Local steps**

- Return flt(((amount × 100) ÷ self.ctc), 2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L2164) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L946) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1293)

<a id="op-91023b44a00f68"></a>
### Salary Breakup Report.get per cycle ctc

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_get_per_cycle_cost_to_company`

**Inputs** self.

**Explicit results** flt((self.ctc ÷ self.cycle\_multiplier), 2).

**Local steps**

- Return flt((self.ctc ÷ self.cycle\_multiplier), 2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L2247) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L952) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1299)

<a id="op-963e53fe4783d6"></a>
### Salary Breakup Report.indent salary components

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_indent_salary_components`

**Inputs** self.

**Local steps**

- For each component in self.salary\_components.
  - Set component at “indent” from 1.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L2319) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L953) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1300)

<a id="op-b731ff9a5eebd6"></a>
### Salary Breakup Report.format currency

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_format_currency`

**Inputs** self, amount.

**Explicit results** fmt\_money(amount, precision = 2, currency = self.currency).

**Local steps**

- Return fmt\_money(amount, precision = 2, currency = self.currency).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L2393) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L948) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1295)

<a id="op-a56e9b9054b8dd"></a>
### Salary Breakup Report.get columns

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_get_columns`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** list(mapping(“label” → translated “Component”, “fieldname” → “salary\_component”, “fieldtype” → “Data”, “width” → 300, …), mapping(“label” → translated “Type”, “fieldname” → “type”, “fieldtype” → “Data”, “w ….

**Local steps**

- Return list(mapping(“label” → translated “Component”, “fieldname” → “salary\_component”, “fieldtype” → “Data”, “width” → 300, …), mapping(“label” → translated “Type”, “fieldname” → “type”, “fieldtype” → “Data”, “w ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L2477) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L949) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1296)

<a id="op-84bc031aeb8b05"></a>
### Salary Breakup Report.get message

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_salary_breakup_report_get_message`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Explicit results** employee\_profile\_card.

**Local steps**

- Set path from “Workforce/payroll/report/employee\_ctc\_break\_up/employee\_profile\_card.html”.
- Set tuple(employee\_name, designation, image) from Platform.get\_value(“Employee”, self.employee, list(“employee\_name”, “designation”, “image”)).
- Set context from dict(mapping(“employee\_name” → employee\_name, “designation” → designation, “image” → image, “salary\_structure” → self.salary\_structure, …)).
- Set employee\_profile\_card from render\_template(path, context = context, is\_path = true).
- Return employee\_profile\_card.

**Methods declared on this owner** [format currency](operations-004.md#op-b731ff9a5eebd6), [get per cycle ctc](operations-004.md#op-91023b44a00f68).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L3291) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L951) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1298)

<a id="op-e60e1dec22f83e"></a>
### Execute

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, message, no value, …).

**Explicit failure paths** validation helper — translated “Please set {0} to get CTC report”.format(Platform.bold(missing\_filter)).

**Local steps**

- Set employee from filters.get(“employee”).
- Set salary\_structure\_assignment from filters.get(“salary\_structure\_assignment”).
- Set missing\_filter from “Employee” when not employee, otherwise “Salary Structure Assignment” when not salary\_structure\_assignment, otherwise no value.
  - Value choice on not employee — true gives “Employee”, false gives “Salary Structure Assignment” when not salary\_structure\_assignment, otherwise no value.
  - Value choice on not salary\_structure\_assignment — true gives “Salary Structure Assignment”, false gives no value.
- If missing\_filter.
  - Call the validation error handler Platform.throw(translated “Please set {0} to get CTC report”.format(Platform.bold(missing\_filter)), title = translated “Missing value for filters”).
- Evaluate validate\_employee\_access(employee).
- Set salary\_breakup\_report from SalaryBreakupReport(employee, salary\_structure\_assignment).
- Set data from salary\_breakup\_report.get\_data().
- Set columns from salary\_breakup\_report.get\_columns().
- Set message from salary\_breakup\_report.get\_message().
- Return tuple(columns, data, message, no value, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L3790) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L945) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1292)

<a id="op-137c74fa0c305b"></a>
### Validate employee access

`operation_workforce_payroll_report_employee_ctc_break_up_business_behavior_validate_employee_access`

**Inputs** employee.

**Record and data access** read “Employee” via get\_value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not permitted to access the CTC report of another employee.”.

**Local steps**

- Set can\_view\_any\_employee from has\_common(ROLES\_ALLOWED\_TO\_VIEW\_ANY\_EMPLOYEE, Platform.get\_roles()).
- Set is\_own\_record from Platform.db.get\_value(“Employee”, employee, “user\_id”) equals Platform.session.user.
- If (not can\_view\_any\_employee and not is\_own\_record).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not can\_view\_any\_employee → not is\_own\_record.
  - Call the validation error handler Platform.throw(translated “You are not permitted to access the CTC report of another employee.”, Platform.PermissionError, title = translated “Not Permitted”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../workforce-decision-contracts/part-0143.json#L4207) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L964) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1311)

## Record · Employee incentive

[Record definition](../../../../data/record-types/employee_incentive.json)

<a id="op-29a6de7e6a9c76"></a>
### Employee Incentive.validate

`operation_workforce_payroll_record_definitions_employee_incentive_business_behavior_employee_incentive_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate self.validate\_salary\_structure().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate salary structure](operations-004.md#op-8df90d979310b8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L6376) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L385) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L734)

<a id="op-8df90d979310b8"></a>
### Employee Incentive.validate salary structure

`operation_workforce_payroll_record_definitions_employee_incentive_business_behavior_employee_incentive_validate_salary_structure`

**Inputs** self.

**Record and data access** read “Salary Structure Assignment” via exists.

**Explicit failure paths** validation helper — translated “There is no Salary Structure assigned to {0}. First assign a Salary Structure.”.format(self.employee).

**Local steps**

- If not Platform.db.exists(“Salary Structure Assignment”, mapping(“employee” → self.employee)).
  - Call the validation error handler Platform.throw(translated “There is no Salary Structure assigned to {0}. First assign a Salary Structure.”.format(self.employee)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L6452) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L386) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L735)

<a id="op-1f2cdc4a10a68b"></a>
### Employee Incentive.on submit

`operation_workforce_payroll_record_definitions_employee_incentive_business_behavior_employee_incentive_on_submit`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**State and service calls** request new\_doc for “Additional Salary” · call submit on additional\_salary.

**Local steps**

- Set company from Platform.db.get\_value(“Employee”, self.employee, “company”).
- Set additional\_salary from Platform.new\_doc(“Additional Salary”).
- Set additional\_salary.employee from self.employee.
- Set additional\_salary.currency from self.currency.
- Set additional\_salary.salary\_component from self.salary\_component.
- Set additional\_salary.overwrite\_salary\_structure\_amount from 0.
- Set additional\_salary.amount from self.incentive\_amount.
- Set additional\_salary.payroll\_date from self.payroll\_date.
- Set additional\_salary.company from company.
- Set additional\_salary.ref\_doctype from self.doctype.
- Set additional\_salary.ref\_docname from self.name.
- Evaluate additional\_salary.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L6607) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L384) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L733)

## Record · Employee tax exemption declaration

[Record definition](../../../../data/record-types/employee_tax_exemption_declaration.json)

<a id="op-c167616cbf2dd3"></a>
### Employee Tax Exemption Declaration.validate

`operation_workforce_payroll_record_definitions_employee_tax_exemption_declaration_business_behavior_employee_tax_exemption_declaration_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate validate\_tax\_declaration(self.declarations).
- Evaluate validate\_duplicate\_exemption\_for\_payroll\_period(self.doctype, self.name, self.payroll\_period, self.employee).
- Evaluate self.set\_total\_declared\_amount().
- Evaluate self.set\_total\_exemption\_amount().
- Evaluate self.calculate\_hra\_exemption().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set total declared amount](operations-004.md#op-7192ea873ece5f), [set total exemption amount](operations-004.md#op-770aa7ce301e51), [calculate hra exemption](operations-004.md#op-b6b6cdbf3679e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0109.json#L6928) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L390) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L739)

<a id="op-7192ea873ece5f"></a>
### Employee Tax Exemption Declaration.set total declared amount

`operation_workforce_payroll_record_definitions_employee_tax_exemption_declaration_business_behavior_employee_tax_exemption_declaration_set_total_declared_amount`

**Inputs** self.

**Local steps**

- Set self.total\_declared\_amount from 0.0.
- For each d in self.declarations.
  - Update self.total\_declared\_amount using + flt(d.amount).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0110.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L388) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L737)

<a id="op-770aa7ce301e51"></a>
### Employee Tax Exemption Declaration.set total exemption amount

`operation_workforce_payroll_record_definitions_employee_tax_exemption_declaration_business_behavior_employee_tax_exemption_declaration_set_total_exemption_amount`

**Inputs** self.

**Local steps**

- Set self.total\_exemption\_amount from flt(get\_total\_exemption\_amount(self.declarations), self.precision(“total\_exemption\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0110.json#L105) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L389) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L738)

<a id="op-b6b6cdbf3679e7"></a>
### Employee Tax Exemption Declaration.calculate hra exemption

`operation_workforce_payroll_record_definitions_employee_tax_exemption_declaration_business_behavior_employee_tax_exemption_declaration_calculate_hra_exemption`

**Inputs** self.

**Local steps**

- Set tuple(self.salary\_structure\_hra, self.annual\_hra\_exemption, self.monthly\_hra\_exemption) from tuple(0, 0, 0).
- If self.get(“monthly\_house\_rent”).
  - Set hra\_exemption from calculate\_annual\_eligible\_hra\_exemption(self).
  - If hra\_exemption.
    - Update self.total\_exemption\_amount using + hra\_exemption at “annual\_exemption”.
    - Set self.total\_exemption\_amount from flt(self.total\_exemption\_amount, self.precision(“total\_exemption\_amount”)).
    - Set self.salary\_structure\_hra from flt(hra\_exemption at “hra\_amount”, self.precision(“salary\_structure\_hra”)).
    - Set self.annual\_hra\_exemption from flt(hra\_exemption at “annual\_exemption”, self.precision(“annual\_hra\_exemption”)).
    - Set self.monthly\_hra\_exemption from flt(hra\_exemption at “monthly\_exemption”, self.precision(“monthly\_hra\_exemption”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0110.json#L209) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L387) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L736)

<a id="op-b0e5583b3eb428"></a>
### Make proof submission

`operation_workforce_payroll_record_definitions_employee_tax_exemption_declaration_business_behavior_make_proof_submission`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Explicit results** doclist.

**Local steps**

- Set doclist from get\_mapped\_doc(“Employee Tax Exemption Declaration”, source\_name, mapping(“Employee Tax Exemption Declaration” → mapping(“doctype” → “Employee Tax Exemption Proof Submission”, “field\_no\_map” → list(“monthl ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0110.json#L598) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L391) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L740)
