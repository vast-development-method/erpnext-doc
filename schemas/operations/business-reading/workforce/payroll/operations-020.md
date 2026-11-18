# Payroll and benefits · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Salary structure assignment

[Record definition](../../../../data/record-types/salary_structure_assignment.json)

<a id="op-91085326172b51"></a>
### Salary Structure Assignment.validate

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_dates().
- Evaluate self.validate\_company().
- Evaluate self.validate\_income\_tax\_slab().
- Evaluate self.set\_payroll\_payable\_account().
- Evaluate validate\_max\_benefit\_for\_flexible\_benefit(self.employee\_benefits, self.max\_benefits).
- If not self.get(“payroll\_cost\_centers”).
  - Evaluate self.set\_payroll\_cost\_centers().
- Evaluate self.validate\_cost\_centers().
- Evaluate self.warn\_about\_missing\_opening\_entries().
- Evaluate self.calculate\_ctc\_and\_gross().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dates](operations-020.md#op-8b39f80705c65b), [validate company](operations-020.md#op-10da38639bd0c0), [validate income tax slab](operations-020.md#op-4ec1ec7c4fb9f5), [set payroll payable account](operations-020.md#op-cc492484eff980), [set payroll cost centers](operations-020.md#op-25a8397c2de4af), [validate cost centers](operations-020.md#op-3c0e7dfb885318), [warn about missing opening entries](operations-020.md#op-895b3d078dba6e), [calculate ctc and gross](operations-020.md#op-dc1dbcf2f51bc3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L1168) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L857) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1204)

<a id="op-5ec32ca368fcd4"></a>
### Salary Structure Assignment.on update after submit

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_on_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_cost\_centers().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate cost centers](operations-020.md#op-3c0e7dfb885318).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L1428) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L853) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1200)

<a id="op-8b39f80705c65b"></a>
### Salary Structure Assignment.validate dates

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_validate_dates`

**Inputs** self.

**Record and data access** read “Employee” via get\_value · read “Salary Structure Assignment” via exists.

**Explicit failure paths** validation helper with DuplicateAssignment — translated “Salary Structure Assignment for Employee already exists” · validation helper — translated “From Date {0} cannot be before employee's joining Date {1}”.format(self.from\_date, joining\_date) · validation helper — translated “From Date {0} cannot be after employee's relieving Date {1}”.format(self.from\_date, relieving\_date).

**Local steps**

- Set tuple(joining\_date, relieving\_date) from Platform.db.get\_value(“Employee”, self.employee, list(“date\_of\_joining”, “relieving\_date”)).
- If self.from\_date.
  - If Platform.db.exists(“Salary Structure Assignment”, mapping(“employee” → self.employee, “from\_date” → self.from\_date, “docstatus” → 1)).
    - Call the validation error handler Platform.throw(translated “Salary Structure Assignment for Employee already exists”, DuplicateAssignment).
  - If (joining\_date and getdate(self.from\_date) &lt; joining\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in joining\_date → getdate(self.from\_date) &lt; joining\_date.
    - Call the validation error handler Platform.throw(translated “From Date {0} cannot be before employee's joining Date {1}”.format(self.from\_date, joining\_date)).
  - If (relieving\_date and getdate(self.from\_date) &gt; relieving\_date and not self.flags.old\_employee).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in relieving\_date → getdate(self.from\_date) &gt; relieving\_date → not self.flags.old\_employee.
    - Call the validation error handler Platform.throw(translated “From Date {0} cannot be after employee's relieving Date {1}”.format(self.from\_date, relieving\_date)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L1479) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L860) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1207)

<a id="op-10da38639bd0c0"></a>
### Salary Structure Assignment.validate company

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_validate_company`

**Inputs** self.

**Record and data access** read “Salary Structure” via get\_value.

**Explicit failure paths** validation helper — translated “Salary Structure {0} does not belong to company {1}”.format(Platform.bold(self.salary\_structure), Platform.bold(self.company)).

**Local steps**

- Set salary\_structure\_company from Platform.db.get\_value(“Salary Structure”, self.salary\_structure, “company”, cache = true).
- If self.company differs from salary\_structure\_company.
  - Call the validation error handler Platform.throw(translated “Salary Structure {0} does not belong to company {1}”.format(Platform.bold(self.salary\_structure), Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L1978) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L858) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1205)

<a id="op-4ec1ec7c4fb9f5"></a>
### Salary Structure Assignment.validate income tax slab

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_validate_income_tax_slab`

**Inputs** self.

**Record and data access** read “Income Tax Slab” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Income Tax Slab is mandatory since the Salary Structure {0} has a tax component {1}”.format(get\_link\_to\_form(“Salary Structure”, self.salary\_structure), Platform.bold(tax\_component)) · validation helper — translated “Currency of selected Income Tax Slab should be {0} instead of {1}”.format(self.currency, income\_tax\_slab\_currency).

**Local steps**

- Set tax\_component from get\_tax\_component(self.salary\_structure).
- If (tax\_component and not self.income\_tax\_slab).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax\_component → not self.income\_tax\_slab.
  - Call the validation error handler Platform.throw(translated “Income Tax Slab is mandatory since the Salary Structure {0} has a tax component {1}”.format(get\_link\_to\_form(“Salary Structure”, self.salary\_structure), Platform.bold(tax\_compone ….
- If not self.income\_tax\_slab.
  - Return no value.
- Set income\_tax\_slab\_currency from Platform.db.get\_value(“Income Tax Slab”, self.income\_tax\_slab, “currency”).
- If self.currency differs from income\_tax\_slab\_currency.
  - Call the validation error handler Platform.throw(translated “Currency of selected Income Tax Slab should be {0} instead of {1}”.format(self.currency, income\_tax\_slab\_currency)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L2203) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L861) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1208)

<a id="op-cc492484eff980"></a>
### Salary Structure Assignment.set payroll payable account

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_set_payroll_payable_account`

**Inputs** self.

**Record and data access** read “Company” via get\_value · read “Account” via get\_value.

**Local steps**

- If not self.payroll\_payable\_account.
  - Set payroll\_payable\_account from Platform.db.get\_value(“Company”, self.company, “default\_payroll\_payable\_account”).
  - If not payroll\_payable\_account.
    - Set payroll\_payable\_account from Platform.db.get\_value(“Account”, mapping(“account\_name” → translated “Payroll Payable”, “company” → self.company, “account\_currency” → Platform.db.get\_value(“Company”, self.company, “default\_currency”), “i ….
  - Set self.payroll\_payable\_account from payroll\_payable\_account.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L2601) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L855) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1202)

<a id="op-25a8397c2de4af"></a>
### Salary Structure Assignment.set payroll cost centers

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_set_payroll_cost_centers`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Local steps**

- Set self.payroll\_cost\_centers from list().
- Set default\_payroll\_cost\_center from self.get\_payroll\_cost\_center().
- If default\_payroll\_cost\_center.
  - Evaluate self.append(“payroll\_cost\_centers”, mapping(“cost\_center” → default\_payroll\_cost\_center, “percentage” → 100)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get payroll cost center](operations-020.md#op-80ca2ec489ec6c).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L2897) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L854) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1201)

<a id="op-80ca2ec489ec6c"></a>
### Salary Structure Assignment.get payroll cost center

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_get_payroll_cost_center`

**Inputs** self.

**Record and data access** read “Employee” via get\_value · read “Department” via get\_value.

**Explicit results** payroll\_cost\_center.

**Local steps**

- Set payroll\_cost\_center from Platform.db.get\_value(“Employee”, self.employee, “payroll\_cost\_center”).
- If (not payroll\_cost\_center and self.department).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not payroll\_cost\_center → self.department.
  - Set payroll\_cost\_center from Platform.db.get\_value(“Department”, self.department, “payroll\_cost\_center”).
- Return payroll\_cost\_center.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L3065) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L851) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1198)

<a id="op-3c0e7dfb885318"></a>
### Salary Structure Assignment.validate cost centers

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_validate_cost_centers`

**Inputs** self.

**Record and data access** read “Cost Center” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Cost Center {1} does not belong to Company {2}”.format(entry.idx, Platform.bold(entry.cost\_center), Platform.bold(self.company)) · validation helper — translated “Total percentage against cost centers should be 100”.

**Local steps**

- If not self.get(“payroll\_cost\_centers”).
  - Return no value.
- Set total\_percentage from 0.
- For each entry in self.payroll\_cost\_centers.
  - Set company from Platform.db.get\_value(“Cost Center”, entry.cost\_center, “company”).
  - If company differs from self.company.
    - Call the validation error handler Platform.throw(translated “Row {0}: Cost Center {1} does not belong to Company {2}”.format(entry.idx, Platform.bold(entry.cost\_center), Platform.bold(self.company)), title = translated “Invalid Cost Center”).
  - Update total\_percentage using + flt(entry.percentage).
- <a id="op-3c0e7dfb885318-guard-18"></a>If total\_percentage differs from 100.
  - Call the validation error handler Platform.throw(translated “Total percentage against cost centers should be 100”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison total\_percentage differs from 100, total\_percentage = 101 selects the branch that calls the validation-error handler with translated “Total percentage against cost centers should be 100”. With total\_percentage = 100, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-3c0e7dfb885318-guard-18)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L3230) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L859) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1206)

<a id="op-895b3d078dba6e"></a>
### Salary Structure Assignment.warn about missing opening entries

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_warn_about_missing_opening_entries`

**Inputs** self.

**State and service calls** msgprint with msg.

**Local steps**

- If (self.are\_opening\_entries\_required() and not self.taxable\_earnings\_till\_date and not self.tax\_deducted\_till\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.are\_opening\_entries\_required() → not self.taxable\_earnings\_till\_date → not self.tax\_deducted\_till\_date.
  - Set msg from translated “Please specify {0} and {1} (if any), for the correct tax calculation in future salary slips.”.format(Platform.bold(translated “Taxable Earnings Till Date”), Platform.bold(translated “Tax Deduct ….
  - Evaluate Platform.msgprint(msg, indicator = “orange”, title = translated “Missing Opening Entries”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [are opening entries required](operations-020.md#op-730b15b5c19b73).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L3639) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L862) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1209)

<a id="op-b2db2291991c18"></a>
### Salary Structure Assignment.get evaluated components

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_get_evaluated_components`

**Inputs** self.

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(earnings = rows\_by\_type at “earnings”, deductions = rows\_by\_type at “deductions”, employer\_contributions = rows\_by\_type at “employer\_contributions”).

**Local steps**

- Set tuple(\_data, rows\_by\_type) from self.\_evaluate\_all\_components().
- Return Platform.\_dict(earnings = rows\_by\_type at “earnings”, deductions = rows\_by\_type at “deductions”, employer\_contributions = rows\_by\_type at “employer\_contributions”).

**Methods declared on this owner** [evaluate all components](operations-020.md#op-6bc46756130c38).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L3891) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L850) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1197)

<a id="op-198f7fa07d33be"></a>
### Salary Structure Assignment.get timesheet config

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_get_timesheet_configuration`

**Inputs** self.

**Declared result** Platform.\_dict.

**Record and data access** read “Salary Structure” via get\_cached\_value.

**Explicit results** Platform.\_dict(based\_on\_timesheet = cint(ss.salary\_slip\_based\_on\_timesheet), hour\_rate = flt(ss.hour\_rate), timesheet\_component = ss.salary\_component).

**Local steps**

- Set ss from (Platform.get\_cached\_value(“Salary Structure”, self.salary\_structure, list(“salary\_slip\_based\_on\_timesheet”, “hour\_rate”, “salary\_component”), as\_dict = true) or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Salary Structure”, self.salary\_structure, list(“salary\_slip\_based\_on\_timesheet”, “hour\_rate”, “salary\_component”), as\_dict = true) → Platform.\_dict().
- Return Platform.\_dict(based\_on\_timesheet = cint(ss.salary\_slip\_based\_on\_timesheet), hour\_rate = flt(ss.hour\_rate), timesheet\_component = ss.salary\_component).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Salary Structure”, self.salary\_structure, list(“salary\_slip\_based\_on\_timesheet”, “hour\_rate”, “salary\_component”), as\_dict = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L4042) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L852) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1199)

<a id="op-dc1dbcf2f51bc3"></a>
### Salary Structure Assignment.calculate ctc and gross

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_calculate_cost_to_company_and_gross`

**Inputs** self.

**Declared result** no value.

**Record and data access** resolve a document from “Salary Structure” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- If (not self.base or not self.salary\_structure).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.base → not self.salary\_structure.
  - Set self.annual\_gross\_earning from 0.
  - Set self.ctc from 0.
  - Return no value.
- Set salary\_structure from Platform.get\_cached\_doc(“Salary Structure”, self.salary\_structure).
- Set periods from PERIODS\_PER\_YEAR.get(salary\_structure.payroll\_frequency, 12).
- Set tuple(data, rows\_by\_type) from self.\_evaluate\_all\_components().
- Set gross\_per\_period from flt(data.get(“gross\_pay”)).
- Set non\_payable\_earnings\_per\_period from sum(generator of flt(r.default\_amount) for r drawn from rows\_by\_type at “earnings” where (not r.statistical\_component and r.do\_not\_include\_in\_total)).
  - Draw r from rows\_by\_type at “earnings”, keep a combination only if ((not r.statistical\_component and r.do\_not\_include\_in\_total)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not r.statistical\_component → r.do\_not\_include\_in\_total.
- Set employer\_per\_period from sum(generator of flt(r.default\_amount) for r drawn from rows\_by\_type at “employer\_contributions” where not r.statistical\_component).
  - Draw r from rows\_by\_type at “employer\_contributions”, keep a combination only if (not r.statistical\_component).
- Set self.annual\_gross\_earning from flt((gross\_per\_period × periods), self.precision(“annual\_gross\_earning”)).
- Set self.ctc from flt((((gross\_per\_period + non\_payable\_earnings\_per\_period) + employer\_per\_period) × periods), self.precision(“ctc”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [evaluate all components](operations-020.md#op-6bc46756130c38).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Salary Structure”, self.salary\_structure).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L4264) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L846) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1193)

<a id="op-6bc46756130c38"></a>
### Salary Structure Assignment.evaluate all components

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_evaluate_all_components`

**Inputs** self.

**Declared result** tuple at tuple(Platform.\_dict, dict).

**Record and data access** resolve a document from “Salary Structure” via get\_cached\_doc.

**Explicit results** tuple(data, rows\_by\_type).

**Local steps**

- Set salary\_structure from Platform.get\_cached\_doc(“Salary Structure”, self.salary\_structure).
- Set data from self.\_get\_component\_eval\_context().
- Set rows\_by\_type from mapping().
- Set rows\_by\_type at “earnings” from self.\_evaluate\_component\_table((salary\_structure.get(“earnings”) or list()), data).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in salary\_structure.get(“earnings”) → list().
- Set data at “gross\_pay” from sum(generator of flt(r.default\_amount) for r drawn from rows\_by\_type at “earnings” where (not r.statistical\_component and not r.do\_not\_include\_in\_total)).
  - Draw r from rows\_by\_type at “earnings”, keep a combination only if ((not r.statistical\_component and not r.do\_not\_include\_in\_total)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not r.statistical\_component → not r.do\_not\_include\_in\_total.
- Set rows\_by\_type at “deductions” from self.\_evaluate\_component\_table((salary\_structure.get(“deductions”) or list()), data).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in salary\_structure.get(“deductions”) → list().
- Set rows\_by\_type at “employer\_contributions” from self.\_evaluate\_component\_table((salary\_structure.get(“employer\_contributions”) or list()), data).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in salary\_structure.get(“employer\_contributions”) → list().
- Evaluate self.apply\_regional\_ctc\_components(rows\_by\_type, data).
- Return tuple(data, rows\_by\_type).

**Methods declared on this owner** [get component eval context](operations-020.md#op-a85480ae3266df), [evaluate component table](operations-020.md#op-4a20edc8067973), [apply regional ctc components](operations-020.md#op-c53d1e3d648d9b).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Salary Structure”, self.salary\_structure).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L4852) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L847) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1194)

<a id="op-c53d1e3d648d9b"></a>
### Salary Structure Assignment.apply regional ctc components

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_apply_regional_cost_to_company_components`

**Inputs** self, rows\_by\_type, data.

**Wrappers, in declaration order** Workforce.allow\_regional.

**Declared result** no value.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0139.json#L5371) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L844) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1191)

<a id="op-c1c636e170e58c"></a>
### Salary Structure Assignment.upsert employer contribution

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_upsert_employer_contribution`

**Inputs** self, rows\_by\_type, data, salary\_component, amount.

**Declared result** (Platform.\_dict bitwise or no value).

**Record and data access** read “Salary Component” via get\_value.

**Explicit results** no value · row.

**Local steps**

- Set fields from (list of f for f drawn from SALARY\_COMPONENT\_FLAGS where f differs from “abbr” + list(“salary\_component\_abbr”)).
  - Draw f from SALARY\_COMPONENT\_FLAGS, keep a combination only if (f differs from “abbr”).
- Set component from Platform.db.get\_value(“Salary Component”, salary\_component, fields, as\_dict = true).
- If not component.
  - Return no value.
- Set rows from rows\_by\_type at “employer\_contributions”.
- Set row from next(generator of r for r drawn from rows where r.salary\_component equals salary\_component, no value).
  - Draw r from rows, keep a combination only if (r.salary\_component equals salary\_component).
- If row is identical to no value.
  - If not flt(amount).
    - Return no value.
  - Set row from Platform.\_dict(condition = no value, condition\_met = true, formula = no value, precision = Platform.get\_precision(“Salary Detail”, “amount”)).
  - For each field in SALARY\_COMPONENT\_FLAGS.
    - Set row at field from component.get(field).
  - Set row.salary\_component from salary\_component.
  - Set row.abbr from component.salary\_component\_abbr.
  - Evaluate rows.append(row).
- Otherwise.
  - Set row.condition from no value.
  - Set row.formula from no value.
  - Set row.amount\_based\_on\_formula from 0.
- Set value from flt(amount, row.precision).
- Set row.default\_amount from value.
- Set row.amount from value.
- If row.abbr.
  - Set data at row.abbr from value.
- Return row.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L3) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L856) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1203)

<a id="op-a85480ae3266df"></a>
### Salary Structure Assignment.get component eval context

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_get_component_evaluate_context`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L2) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L849) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1196)

<a id="op-b64432abfc6554"></a>
### Salary Structure Assignment.get full cycle dates

`operation_workforce_binding_workforce_payroll_doctype_salary_structure_assignment_salary_structure_assignment_salarystructureassignment_get_full_cycle_dates`

**Inputs** self, frequency.

**Declared result** Platform.\_dict.

**Explicit results** get\_start\_end\_dates(frequency, self.from\_date) · Platform.\_dict(start\_date = start\_date, end\_date = end\_date).

**Local steps**

- Bind dependencies get\_start\_end\_dates.
- If frequency does not belong to tuple(“Monthly”, “Bimonthly”, empty text).
  - Return get\_start\_end\_dates(frequency, self.from\_date).
- Set from\_date from getdate(self.from\_date).
- Set tuple(start\_date, end\_date) from tuple(get\_first\_day(from\_date), get\_last\_day(from\_date)).
- If frequency equals “Bimonthly”.
  - If from\_date.day ≤ 15.
    - Set end\_date from start\_date.replace(day = 15).
  - Otherwise.
    - Set start\_date from start\_date.replace(day = 16).
- Return Platform.\_dict(start\_date = start\_date, end\_date = end\_date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L179) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L230) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L230)

<a id="op-4a20edc8067973"></a>
### Salary Structure Assignment.evaluate component table

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_evaluate_component_table`

**Inputs** self, rows, data.

**Declared result** list.

**Explicit results** evaluated\_components.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set evaluated\_components from list().
- For each struct\_row in rows.
  - Set condition from sanitize\_expression(struct\_row.condition).
  - Set formula from sanitize\_expression(struct\_row.formula).
  - Set amount from flt(struct\_row.amount).
  - Set condition\_met from true.
  - Attempt the following.
    - If (condition and not \_safe\_eval(condition, COMPONENT\_EVAL\_GLOBALS.copy(), data)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in condition → not \_safe\_eval(condition, COMPONENT\_EVAL\_GLOBALS.copy(), data).
      - Set condition\_met from false.
      - Set default\_amount from 0.
    - Otherwise.
      - If (struct\_row.amount\_based\_on\_formula and formula).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in struct\_row.amount\_based\_on\_formula → formula.
        - Set default\_amount from flt(\_safe\_eval(formula, COMPONENT\_EVAL\_GLOBALS.copy(), data), struct\_row.precision(“amount”)).
      - Otherwise.
        - Set default\_amount from amount.
  - On failure (NameError) bound to ne.
    - Evaluate throw\_error\_message(struct\_row, ne, title = translated “Name error”, description = translated “This error can be due to missing or deleted field.”).
  - On failure (SyntaxError) bound to se.
    - Evaluate throw\_error\_message(struct\_row, se, title = translated “Syntax error”, description = translated “This error can be due to invalid syntax.”).
  - On failure (Exception) bound to exc.
    - Evaluate throw\_error\_message(struct\_row, exc, title = translated “Error in formula or condition”, description = translated “This error can be due to invalid formula or condition.”).
    - Propagate the active failure.
  - If condition\_met.
    - Set data at struct\_row.abbr from default\_amount.
  - Set evaluated\_component\_row from Platform.\_dict(default\_amount = default\_amount, amount = amount, condition\_met = condition\_met, condition = condition, …).
  - For each field in SALARY\_COMPONENT\_FLAGS.
    - Set evaluated\_component\_row at field from struct\_row.get(field).
  - Evaluate evaluated\_components.append(evaluated\_component\_row).
- Return evaluated\_components.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L119) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L848) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1195)

<a id="op-730b15b5c19b73"></a>
### Salary Structure Assignment.are opening entries required

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_salary_structure_assignment_are_opening_entries_required`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- If not get\_tax\_component(self.salary\_structure).
  - Return false.
- Set payroll\_period from get\_payroll\_period(self.from\_date, self.from\_date, self.company).
- If (payroll\_period and getdate(self.from\_date) ≤ getdate(payroll\_period.start\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in payroll\_period → getdate(self.from\_date) ≤ getdate(payroll\_period.start\_date).
  - Return false.
- Return true.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0140.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L845) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1192)

<a id="op-8d3138f2ca4ffb"></a>
### Get assigned salary structure

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_get_assigned_salary_structure`

**Inputs** employee, on\_date.

**Explicit results** no value · result at 0 at 0 when result, otherwise no value.

**Local steps**

- If (not employee or not on\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not employee → not on\_date.
  - Return no value.
- Set salary\_structure\_assignment from Platform.qb.DocType(“Salary Structure Assignment”).
- Set query from nested operand in the contract(nested operand in the contract).where(on\_date ≥ nested operand in the contract.from\_date).orderby(salary\_structure\_assignment.from\_date, order = Platform.qb.desc).limit(1).
- Set result from query.run().
- Return result at 0 at 0 when result, otherwise no value.
  - Value choice on result — true gives result at 0 at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0140.json#L224) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L841) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1188)

<a id="op-2c20abfe8db1ac"></a>
### Get employee currency

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_get_employee_currency`

**Inputs** employee.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Record and data access** read “Salary Structure Assignment” via get\_value.

**Explicit results** employee\_currency.

**Explicit failure paths** validation helper — translated “There is no Salary Structure assigned to {0}. First assign a Salary Structure.”.format(employee).

**Local steps**

- Evaluate Platform.has\_permission(“Employee”, “read”, employee, throw = true).
- Set employee\_currency from Platform.db.get\_value(“Salary Structure Assignment”, mapping(“employee” → employee, “docstatus” → 1), “currency”, order\_by = “from\_date desc”).
- If not employee\_currency.
  - Call the validation error handler Platform.throw(translated “There is no Salary Structure assigned to {0}. First assign a Salary Structure.”.format(employee)).
- Return employee\_currency.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L118) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L842) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1189)

<a id="op-40b7c8693ac080"></a>
### Get tax component

`operation_workforce_payroll_record_definitions_salary_structure_assignment_business_behavior_get_tax_component`

**Inputs** salary\_structure.

**Declared result** (str bitwise or no value).

**Record and data access** resolve a document from “Salary Structure” via get\_cached\_doc.

**Explicit results** d.salary\_component · no value.

**Local steps**

- Set salary\_structure from Platform.get\_cached\_doc(“Salary Structure”, salary\_structure).
- For each d in salary\_structure.deductions.
  - If (cint(d.variable\_based\_on\_taxable\_salary) and not d.formula and not flt(d.amount)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(d.variable\_based\_on\_taxable\_salary) → not d.formula → not flt(d.amount).
    - Return d.salary\_component.
- Return no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Salary Structure”, salary\_structure).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0140.json#L845) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L843) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1190)

## Record · Salary withholding

[Record definition](../../../../data/record-types/salary_withholding.json)

<a id="op-2d1450630a9fa1"></a>
### Salary Withholding.validate

`operation_workforce_payroll_record_definitions_salary_withholding_business_behavior_salary_withholding_validate`

**Inputs** self.

**Local steps**

- If not self.payroll\_frequency.
  - Set self.payroll\_frequency from get\_payroll\_frequency(self.employee, self.from\_date).
- Evaluate self.set\_withholding\_cycles\_and\_to\_date().
- Evaluate self.validate\_duplicate\_record().
- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set withholding cycles and to date](operations-021.md#op-97b71b56a6b411), [validate duplicate record](operations-021.md#op-1abad3b41680a9), [set status](operations-021.md#op-4517f0efc909b2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0140.json#L7037) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L920) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1267)
