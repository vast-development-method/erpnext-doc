# Payroll and benefits · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Salary register

<a id="op-a7a85183f38efe"></a>
### Get component fieldnames

`operation_workforce_binding_workforce_payroll_report_salary_register_salary_register_get_component_fieldnames`

**Inputs** components, parentfields.

**Explicit results** fieldnames.

**Local steps**

- Set fieldnames from mapping().
- Set used from set().
- For each parentfield in parentfields.
  - For each component in components at parentfield.
    - Set fieldname from Platform.scrub(component).
    - If parentfield equals “employer\_contributions”.
      - Set fieldname from formatted text employer\_contribution\_{fieldname}.
    - If fieldname belongs to used.
      - Set fieldname from formatted text {fieldname}\_{len(used)}.
    - Evaluate used.add(fieldname).
    - Set fieldnames at tuple(parentfield, component) from fieldname.
- Return fieldnames.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L181) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L232) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L232)

<a id="op-92a1683c7074d4"></a>
### Get components by parentfield

`operation_workforce_binding_workforce_payroll_report_salary_register_salary_register_get_components_by_parentfield`

**Inputs** salary\_slips, parentfields.

**Explicit results** mapping of parentfield → sorted(names) for tuple(parentfield, names) drawn from components.items().

**Local steps**

- Set rows from get\_salary\_components(salary\_slips).
- Set components from mapping of parentfield → set() for parentfield drawn from COMPONENT\_PARENTFIELDS.
  - Draw parentfield from COMPONENT\_PARENTFIELDS.
- Set pay\_components from set().
- For each parentfield in parentfields.
  - For each row in rows.
    - If row.parentfield differs from parentfield.
      - Continue with the next iteration or loop test.
    - If parentfield equals “employer\_contributions”.
      - Evaluate components at parentfield.add(row.salary\_component).
    - Otherwise.
      - If row.salary\_component does not belong to pay\_components.
        - Evaluate components at parentfield.add(row.salary\_component).
        - Evaluate pay\_components.add(row.salary\_component).
- Return mapping of parentfield → sorted(names) for tuple(parentfield, names) drawn from components.items().
  - Draw tuple(parentfield, names) from components.items().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L182) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L233) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L233)

<a id="op-4624d09da65cb0"></a>
### Update column width

`operation_workforce_payroll_report_salary_register_business_behavior_update_column_width`

**Inputs** ss, columns.

**Local steps**

- If ss.branch is distinct from no value.
  - Evaluate columns at 3.update(mapping(“width” → 120)).
- If ss.department is distinct from no value.
  - Evaluate columns at 4.update(mapping(“width” → 120)).
- If ss.designation is distinct from no value.
  - Evaluate columns at 5.update(mapping(“width” → 120)).
- If ss.leave\_without\_pay is distinct from no value.
  - Evaluate columns at 9.update(mapping(“width” → 120)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0149.json#L3076) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1042) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1378)

<a id="op-1d047dcc806e4e"></a>
### Get columns

`operation_workforce_payroll_report_salary_register_business_behavior_get_columns`

**Inputs** components, fieldnames.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Salary Slip ID”, “fieldname” → “salary\_slip\_id”, “fieldtype” → “Link”, “options” → “Salary Slip”, …), mapping(“label” → translated “Employee”, “fieldname” → “employee”, “ ….
- For each earning in components at “earnings”.
  - Evaluate columns.append(mapping(“label” → earning, “fieldname” → fieldnames at tuple(“earnings”, earning), “fieldtype” → “Currency”, “options” → “currency”, …)).
- Evaluate columns.append(mapping(“label” → translated “Gross Pay”, “fieldname” → “gross\_pay”, “fieldtype” → “Currency”, “options” → “currency”, …)).
- For each deduction in components at “deductions”.
  - Evaluate columns.append(mapping(“label” → deduction, “fieldname” → fieldnames at tuple(“deductions”, deduction), “fieldtype” → “Currency”, “options” → “currency”, …)).
- If “lending” belongs to Platform.get\_installed\_apps().
  - Evaluate columns.append(mapping(“label” → translated “Loan Repayment”, “fieldname” → “total\_loan\_repayment”, “fieldtype” → “Currency”, “options” → “currency”, …)).
- Evaluate columns.extend(list(mapping(“label” → translated “Total Deduction”, “fieldname” → “total\_deduction”, “fieldtype” → “Currency”, “options” → “currency”, …), mapping(“label” → translated “Net Pay”, “fieldname ….
- For each contribution in components at “employer\_contributions”.
  - Evaluate columns.append(mapping(“label” → contribution, “fieldname” → fieldnames at tuple(“employer\_contributions”, contribution), “fieldtype” → “Currency”, “options” → “currency”, …)).
- If components at “employer\_contributions”.
  - Evaluate columns.append(mapping(“label” → translated “Total Employer Contribution”, “fieldname” → “total\_employer\_contribution”, “fieldtype” → “Currency”, “options” → “currency”, …)).
- Evaluate columns.append(mapping(“label” → translated “Currency”, “fieldtype” → “Data”, “fieldname” → “currency”, “options” → “Currency”, …)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L11) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1035) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1373)

<a id="op-5fece955077584"></a>
### Get salary components

`operation_workforce_payroll_report_salary_register_business_behavior_get_salary_components`

**Inputs** salary\_slips.

**Explicit results** nested operand in the contract(nested operand in the contract).select(salary\_detail.parentfield, salary\_detail.salary\_component).distinct().run(as\_dict = true).

**Local steps**

- Return nested operand in the contract(nested operand in the contract).select(salary\_detail.parentfield, salary\_detail.salary\_component).distinct().run(as\_dict = true).
  - Draw d from salary\_slips.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L12) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1039) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1375)

<a id="op-56c45725e79769"></a>
### Get salary slips

`operation_workforce_payroll_report_salary_register_business_behavior_get_salary_slips`

**Inputs** filters, company\_currency.

**Explicit results** (salary\_slips or list()).

**Local steps**

- Set doc\_status from mapping(“Draft” → 0, “Submitted” → 1, “Cancelled” → 2).
- Set query from Platform.qb.from\_(salary\_slip).select(salary\_slip.star).
- If filters.get(“docstatus”).
  - Set query from query.where(salary\_slip.docstatus equals doc\_status at filters.get(“docstatus”)).
- If filters.get(“from\_date”).
  - Set query from query.where(salary\_slip.start\_date ≥ filters.get(“from\_date”)).
- If filters.get(“to\_date”).
  - Set query from query.where(salary\_slip.end\_date ≤ filters.get(“to\_date”)).
- If filters.get(“company”).
  - Set query from query.where(salary\_slip.company equals filters.get(“company”)).
- If filters.get(“employee”).
  - Set query from query.where(salary\_slip.employee equals filters.get(“employee”)).
- If (filters.get(“currency”) and filters.get(“currency”) differs from company\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“currency”) → filters.get(“currency”) differs from company\_currency.
  - Set query from query.where(salary\_slip.currency equals filters.get(“currency”)).
- If filters.get(“department”).
  - Set query from query.where(salary\_slip.department equals filters at “department”).
- If filters.get(“designation”).
  - Set query from query.where(salary\_slip.designation equals filters at “designation”).
- If filters.get(“branch”).
  - Set query from query.where(salary\_slip.branch equals filters at “branch”).
- Set salary\_slips from query.run(as\_dict = 1).
- Return (salary\_slips or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in salary\_slips → list().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0149.json#L5967) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1041) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1377)

<a id="op-b7bead09a51ff9"></a>
### Get employee doj map

`operation_workforce_payroll_report_salary_register_business_behavior_get_employee_doj_map`

**Inputs** no declared parameters.

**Explicit results** Platform.\_dict(result).

**Local steps**

- Set employee from Platform.qb.DocType(“Employee”).
- Set result from nested operand in the contract.qb.from\_(employee).select(employee.name, employee.date\_of\_joining).run().
- Return Platform.\_dict(result).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0149.json#L7029) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1037) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1374)

<a id="op-4eeac4577123d5"></a>
### Get salary slip details

`operation_workforce_payroll_report_salary_register_business_behavior_get_salary_slip_details`

**Inputs** salary\_slips, currency, company\_currency, parentfield.

**Explicit results** ss\_map.

**Local steps**

- Set salary\_slips from list of ss.name for ss drawn from salary\_slips.
  - Draw ss from salary\_slips.
- Set result from nested operand in the contract(nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contract equals nested operand in the  ….
- Set ss\_map from mapping().
- For each d in result.
  - Evaluate ss\_map.setdefault(d.parent, Platform.\_dict()).setdefault(d.salary\_component, 0.0).
  - If currency equals company\_currency.
    - Update ss\_map at d.parent at d.salary\_component using + (flt(d.amount) × flt(d.exchange\_rate when d.exchange\_rate, otherwise 1)).
      - Value choice on d.exchange\_rate — true gives d.exchange\_rate, false gives 1.
  - Otherwise.
    - Update ss\_map at d.parent at d.salary\_component using + flt(d.amount).
- Return ss\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L13) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1040) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1376)

## Record · Salary slip

[Record definition](../../../../data/record-types/salary_slip.json)

<a id="op-1f3680a3316c37"></a>
### Salary Slip.initialize

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.whitelisted\_globals from COMPONENT\_EVAL\_GLOBALS.copy().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L2567) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L706) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1053)

<a id="op-76e6cd38280884"></a>
### Salary Slip.default series

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_default_series`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** formatted text Sal Slip/{self.employee}/.#####.

**Local steps**

- Return formatted text Sal Slip/{self.employee}/.#####.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L2678) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L660) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1007)

<a id="op-3f2da1b98b940a"></a>
### Salary Slip.autoname

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_autoname`

**Inputs** self.

**Local steps**

- If not self.has\_custom\_naming\_series.
  - Set self.name from make\_autoname(self.default\_series).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L2744) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L638) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L985)

<a id="op-00a4d940305cc8"></a>
### Salary Slip.has custom naming series

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_has_custom_naming_series`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Property Setter” via exists.

**Explicit results** Platform.db.exists(“Property Setter”, mapping(“doc\_type” → “Salary Slip”, “property” → “autoname”)).

**Local steps**

- Return Platform.db.exists(“Property Setter”, mapping(“doc\_type” → “Salary Slip”, “property” → “autoname”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L2830) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L705) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1052)

<a id="op-13618bb8ececfe"></a>
### Salary Slip.joining date

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_joining_date`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Employee” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Employee”, self.employee, “date\_of\_joining”).

**Local steps**

- Return Platform.get\_cached\_value(“Employee”, self.employee, “date\_of\_joining”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Employee”, self.employee, “date\_of\_joining”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L2945) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L708) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1055)

<a id="op-c910727a466cd5"></a>
### Salary Slip.relieving date

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_relieving_date`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Employee” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Employee”, self.employee, “relieving\_date”).

**Local steps**

- Return Platform.get\_cached\_value(“Employee”, self.employee, “relieving\_date”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Employee”, self.employee, “relieving\_date”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L3026) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L719) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1066)

<a id="op-2435db10cb5f83"></a>
### Salary Slip.payroll period

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_payroll_period`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** get\_payroll\_period(self.start\_date, self.end\_date, self.company).

**Local steps**

- Return get\_payroll\_period(self.start\_date, self.end\_date, self.company).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L3107) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L714) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1061)

<a id="op-1fb6b912dcbaaa"></a>
### Salary Slip.actual start date

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_actual_start_date`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.joining\_date · self.start\_date.

**Local steps**

- If (self.joining\_date and getdate(self.start\_date) &lt; self.joining\_date ≤ getdate(self.end\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.joining\_date → getdate(self.start\_date) &lt; self.joining\_date ≤ getdate(self.end\_date).
  - Compare adjacent operands in order, stopping at the first false comparison in getdate(self.start\_date) &lt; self.joining\_date ≤ getdate(self.end\_date).
  - Return self.joining\_date.
- Return self.start\_date.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L3184) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L627) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L974)

<a id="op-d97c34b584c437"></a>
### Salary Slip.actual end date

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_actual_end_date`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.relieving\_date · self.end\_date.

**Local steps**

- If (self.relieving\_date and getdate(self.start\_date) ≤ self.relieving\_date &lt; getdate(self.end\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.relieving\_date → getdate(self.start\_date) ≤ self.relieving\_date &lt; getdate(self.end\_date).
  - Compare adjacent operands in order, stopping at the first false comparison in getdate(self.start\_date) ≤ self.relieving\_date &lt; getdate(self.end\_date).
  - Return self.relieving\_date.
- Return self.end\_date.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L3324) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L626) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L973)

<a id="op-f437a3e46ab913"></a>
### Salary Slip.validate

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_validate`

**Inputs** self.

**Record and data access** read “Payroll Settings” via get\_single\_value.

**State and service calls** msgprint with translated “Total working hours should not be greater than max working hours {0}”.format(max\_working\_hours).

**Local steps**

- Evaluate self.check\_salary\_withholding().
- Set self.status from self.get\_status().
- Evaluate validate\_active\_employee(self.employee).
- Evaluate self.validate\_dates().
- Evaluate self.check\_existing().
- If self.payroll\_frequency.
  - Evaluate self.get\_date\_details().
- If not (len(self.get(“earnings”)) or len(self.get(“deductions”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(self.get(“earnings”)) → len(self.get(“deductions”)).
  - Evaluate self.get\_emp\_and\_working\_day\_details().
- Otherwise.
  - Evaluate self.get\_working\_days\_details(lwp = self.leave\_without\_pay).
- Evaluate self.set\_salary\_structure\_assignment().
- Evaluate self.calculate\_net\_pay().
- Evaluate self.compute\_year\_to\_date().
- Evaluate self.compute\_month\_to\_date().
- Evaluate self.compute\_component\_wise\_year\_to\_date().
- Evaluate self.add\_leave\_balances().
- Set max\_working\_hours from Platform.db.get\_single\_value(“Payroll Settings”, “max\_working\_hours\_against\_timesheet”).
- If max\_working\_hours.
  - If (self.salary\_slip\_based\_on\_timesheet and self.total\_working\_hours &gt; int(max\_working\_hours)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.salary\_slip\_based\_on\_timesheet → self.total\_working\_hours &gt; int(max\_working\_hours).
    - Evaluate Platform.msgprint(translated “Total working hours should not be greater than max working hours {0}”.format(max\_working\_hours), alert = true).
- If (self.payroll\_period and not self.current\_payroll\_period).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.payroll\_period → not self.current\_payroll\_period.
  - Set self.current\_payroll\_period from self.payroll\_period.name.

If control reaches the end, it returns no value.

**Methods declared on this owner** [check salary withholding](operations-013.md#op-0ee443de4d74d4), [get status](operations-014.md#op-c997b531df6d34), [validate dates](operations-014.md#op-f903fb01864c34), [check existing](operations-014.md#op-b1fbcb4b6d5294), [get date details](operations-014.md#op-2218a2becf449f), [get emp and working day details](operations-014.md#op-0e4be42cf0a378), [get working days details](operations-014.md#op-263c6d91c048e3), [set salary structure assignment](operations-015.md#op-3760386e14eff2), [calculate net pay](operations-015.md#op-856a3df225339e), [compute year to date](operations-017.md#op-ddd10b7b50ae46), [compute month to date](operations-017.md#op-bac9d09c6105a6), [compute component wise year to date](operations-017.md#op-fb72874bb69605), [add leave balances](operations-017.md#op-0f8dd95c526a69).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Payroll Settings”, “max\_working\_hours\_against\_timesheet”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L3464) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L733) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1080)

<a id="op-0ee443de4d74d4"></a>
### Salary Slip.check salary withholding

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_check_salary_withholding`

**Inputs** self.

**Local steps**

- Set withholding from get\_salary\_withholdings(self.start\_date, self.end\_date, self.employee).
- If withholding.
  - Set self.salary\_withholding from withholding at 0.salary\_withholding.
  - Set self.salary\_withholding\_cycle from withholding at 0.salary\_withholding\_cycle.
- Otherwise.
  - Set self.salary\_withholding from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L4143) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L648) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L995)

<a id="op-4b67332a93dc41"></a>
### Salary Slip.set net total in words

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_set_net_total_in_words`

**Inputs** self.

**Local steps**

- Set doc\_currency from self.currency.
- Set company\_currency from Enterprise.get\_company\_currency(self.company).
- Set total from self.net\_pay when self.is\_rounding\_total\_disabled(), otherwise self.rounded\_total.
  - Value choice on self.is\_rounding\_total\_disabled() — true gives self.net\_pay, false gives self.rounded\_total.
- Set base\_total from self.base\_net\_pay when self.is\_rounding\_total\_disabled(), otherwise self.base\_rounded\_total.
  - Value choice on self.is\_rounding\_total\_disabled() — true gives self.base\_net\_pay, false gives self.base\_rounded\_total.
- Set self.total\_in\_words from money\_in\_words(total, doc\_currency).
- Set self.base\_total\_in\_words from money\_in\_words(base\_total, company\_currency).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is rounding total disabled](operations-014.md#op-2346ceaeee2d22).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L4304) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L723) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1070)

<a id="op-751e773eb4a44a"></a>
### Salary Slip.on update

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-014.md#op-1e188e80fae523).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L4545) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L713) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1060)

<a id="op-51e8488e428d18"></a>
### Salary Slip.on submit

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_on_submit`

**Inputs** self.

**Record and data access** read “Payroll Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Net Pay cannot be less than 0”.

**Local steps**

- If self.net\_pay &lt; 0.
  - Call the validation error handler Platform.throw(translated “Net Pay cannot be less than 0”).
- Otherwise.
  - Evaluate self.set\_status().
  - Evaluate self.update\_status(self.name).
  - Evaluate make\_loan\_repayment\_entry(self).
  - If (not Platform.flags.via\_payroll\_entry and not Platform.flags.in\_patch).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.flags.via\_payroll\_entry → not Platform.flags.in\_patch.
    - Set email\_salary\_slip from cint(Platform.db.get\_single\_value(“Payroll Settings”, “email\_salary\_slip\_to\_employee”)).
    - If email\_salary\_slip.
      - Evaluate self.email\_salary\_slip().
- Evaluate self.update\_payment\_status\_for\_gratuity\_and\_leave\_encashment().
- Evaluate self.create\_benefits\_ledger\_entry().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-017.md#op-8f7c324ed09168), [update status](operations-017.md#op-36eafe6a75c344), [email salary slip](operations-017.md#op-3dffbd2a7878ed), [update payment status for gratuity and leave encashment](operations-013.md#op-d8536c9e4c68e9), [create benefits ledger entry](operations-013.md#op-f2159505291844).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Payroll Settings”, “email\_salary\_slip\_to\_employee”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L4596) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L711) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1058)

<a id="op-d8536c9e4c68e9"></a>
### Salary Slip.update payment status for gratuity and leave encashment

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_update_payment_status_for_gratuity_and_leave_encashment`

**Inputs** self.

**Record and data access** read “Additional Salary” via get\_all.

**State and service calls** request set\_value on additional\_salary.ref\_doctype.

**Explicit results** no value.

**Local steps**

- Set additional\_salary\_docs from Platform.db.get\_all(“Additional Salary”, filters = mapping(“payroll\_date” → tuple(“between”, list(self.start\_date, self.end\_date)), “employee” → self.employee, “ref\_doctype” → list(“in”, list(“Gratuity”, “ ….
- If not additional\_salary\_docs.
  - Return no value.
- Set status from “Paid” when self.docstatus equals 1, otherwise “Unpaid”.
  - Value choice on self.docstatus equals 1 — true gives “Paid”, false gives “Unpaid”.
- Set earnings from set of entry.additional\_salary for entry drawn from self.earnings.
  - Draw entry from self.earnings.
- For each additional\_salary in additional\_salary\_docs.
  - If additional\_salary.name belongs to earnings.
    - Evaluate Platform.db.set\_value(additional\_salary.ref\_doctype, additional\_salary.ref\_docname, “status”, status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L4941) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L731) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1078)

<a id="op-f2159505291844"></a>
### Salary Slip.create benefits ledger entry

`operation_workforce_payroll_record_definitions_salary_slip_business_behavior_salary_slip_create_benefits_ledger_entry`

**Inputs** self.

**Local steps**

- If self.benefit\_ledger\_components.
  - Set args from mapping(“payroll\_period” → self.payroll\_period.name, “benefit\_ledger\_components” → self.benefit\_ledger\_components, “benefit\_details\_parent” → self.benefit\_details\_parent, “benefit\_details\_doctype” → self.b ….
  - Evaluate create\_employee\_benefit\_ledger\_entry(self, args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0123.json#L5374) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L659) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1006)
