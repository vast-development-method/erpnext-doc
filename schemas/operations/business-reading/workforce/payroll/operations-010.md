# Payroll and benefits · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payroll entry

[Record definition](../../../../data/record-types/payroll_entry.json)

<a id="op-c6f0dccd81f7f0"></a>
### Payroll Entry.set accounting entries for bank entry

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_set_accounting_entries_for_bank_entry`

**Inputs** self, je\_payment\_amount, user\_remark, employee\_wise\_accounting\_enabled.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** self.make\_journal\_entry(accounts, currencies, voucher\_type = “Cash Entry” when Platform.get\_cached\_value(“Account”, self.payment\_account, “account\_type”) equals “Cash”, otherwise “Bank Entry”, user\_remark  ….

**Local steps**

- Set payroll\_payable\_account from self.payroll\_payable\_account.
- Set precision from Platform.get\_precision(“Journal Entry Account”, “debit\_in\_account\_currency”).
- Set accounts from list().
- Set currencies from list().
- Set company\_currency from Enterprise.get\_company\_currency(self.company).
- Set accounting\_dimensions from (get\_accounting\_dimensions() or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_accounting\_dimensions() → list().
- Set tuple(exchange\_rate, amount) from self.get\_amount\_and\_exchange\_rate\_for\_journal\_entry(self.payment\_account, je\_payment\_amount, company\_currency, currencies).
- Evaluate accounts.append(self.update\_accounting\_dimensions(mapping(“account” → self.payment\_account, “bank\_account” → self.bank\_account, “credit\_in\_account\_currency” → flt(amount, precision), “exchange\_rate” → flt( ….
- If self.employee\_based\_payroll\_payable\_entries.
  - For each tuple(employee, employee\_details) in self.employee\_based\_payroll\_payable\_entries.items().
    - Set je\_payment\_amount from (((employee\_details.get(“earnings”, 0) or 0) − (employee\_details.get(“deductions”, 0) or 0)) − (employee\_details.get(“total\_loan\_repayment”, 0) or 0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee\_details.get(“earnings”, 0) → 0.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee\_details.get(“deductions”, 0) → 0.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee\_details.get(“total\_loan\_repayment”, 0) → 0.
    - If not je\_payment\_amount.
      - Continue with the next iteration or loop test.
    - Set tuple(exchange\_rate, amount) from self.get\_amount\_and\_exchange\_rate\_for\_journal\_entry(self.payment\_account, je\_payment\_amount, company\_currency, currencies).
    - Set cost\_centers from self.get\_payroll\_cost\_centers\_for\_employee(employee, employee\_details.get(“salary\_structure”)).
    - For each tuple(cost\_center, percentage) in cost\_centers.items().
      - Set amount\_against\_cost\_center from ((flt(amount) × percentage) ÷ 100).
      - Evaluate accounts.append(self.update\_accounting\_dimensions(mapping(“account” → payroll\_payable\_account, “debit\_in\_account\_currency” → flt(amount\_against\_cost\_center, precision), “exchange\_rate” → flt(exchange\_rate) ….
- Otherwise.
  - Set tuple(exchange\_rate, amount) from self.get\_amount\_and\_exchange\_rate\_for\_journal\_entry(payroll\_payable\_account, je\_payment\_amount, company\_currency, currencies).
  - Evaluate accounts.append(self.update\_accounting\_dimensions(mapping(“account” → payroll\_payable\_account, “debit\_in\_account\_currency” → flt(amount, precision), “exchange\_rate” → flt(exchange\_rate), “reference\_type” → ….
- Return self.make\_journal\_entry(accounts, currencies, voucher\_type = “Cash Entry” when Platform.get\_cached\_value(“Account”, self.payment\_account, “account\_type”) equals “Cash”, otherwise “Bank Entry”, user\_remark  ….
  - Value choice on Platform.get\_cached\_value(“Account”, self.payment\_account, “account\_type”) equals “Cash” — true gives “Cash Entry”, false gives “Bank Entry”.

**Methods declared on this owner** [get amount and exchange rate for journal entry](operations-009.md#op-ea19f1b65907fc), [update accounting dimensions](operations-009.md#op-3f9fbc06041232), [get payroll cost centers for employee](operations-009.md#op-25d4d56bcb6d03), [make journal entry](operations-009.md#op-6ba51720ef32b4).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.payment\_account, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0116.json#L5688) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L529) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L876)

<a id="op-e2284772e13630"></a>
### Payroll Entry.set journal entry in salary slips

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_set_journal_entry_in_salary_slips`

**Inputs** self, submitted\_salary\_slips, jv\_name = no value.

**Local steps**

- Set SalarySlip from Platform.qb.DocType(“Salary Slip”).
- Evaluate nested operand in the contract(nested operand in the contract).set(SalarySlip.journal\_entry, jv\_name).where(SalarySlip.name.isin(list of salary\_slip.name for salary\_slip drawn from submitted\_salary\_slips)).run().
  - Draw salary\_slip from submitted\_salary\_slips.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0116.json#L7124) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L531) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L878)

<a id="op-dac1aa1a44a655"></a>
### Payroll Entry.set start end dates

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_set_start_end_dates`

**Inputs** self.

**Local steps**

- Evaluate self.update(get\_start\_end\_dates(self.payroll\_frequency, (self.start\_date or self.posting\_date), self.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.start\_date → self.posting\_date.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0116.json#L7334) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L533) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L880)

<a id="op-1a615240e5b47f"></a>
### Payroll Entry.get employees with unmarked attendance

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_employees_with_unmarked_attendance`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (list at dict bitwise or no value).

**Explicit results** no value · unmarked\_attendance.

**Local steps**

- If not self.validate\_attendance.
  - Return no value.
- Set unmarked\_attendance from list().
- Set employee\_details from mapping of record.name → record for record drawn from self.get\_employee\_and\_attendance\_details().
  - Draw record from self.get\_employee\_and\_attendance\_details().
- Set holiday\_list\_ranges from get\_holiday\_list\_ranges\_for\_employees(mapping of name → details.company for tuple(name, details) drawn from employee\_details.items(), self.start\_date, self.end\_date).
  - Draw tuple(name, details) from employee\_details.items().
- Set payroll\_dates from mapping().
- For each tuple(employee, details) in employee\_details.items().
  - Set payroll\_dates at employee from self.get\_payroll\_dates\_for\_employee(details).
  - Set holiday\_list\_ranges at employee from clip\_holiday\_list\_ranges(holiday\_list\_ranges.get(employee, list()), expanded payroll\_dates at employee).
- Set holidays from get\_holidays\_in\_ranges\_map(holiday\_list\_ranges).
- For each emp in self.employees.
  - Set details from employee\_details.get(emp.employee).
  - If not details.
    - Continue with the next iteration or loop test.
  - Set tuple(start\_date, end\_date) from payroll\_dates at emp.employee.
  - Set payroll\_days from (date\_diff(end\_date, start\_date) + 1).
  - Set unmarked\_days from (payroll\_days − (len(holidays.get(emp.employee, list())) + details.attendance\_count)).
  - If unmarked\_days &gt; 0.
    - Evaluate unmarked\_attendance.append(mapping(“employee” → emp.employee, “employee\_name” → emp.employee\_name, “unmarked\_days” → unmarked\_days)).
- Return unmarked\_attendance.

**Methods declared on this owner** [get employee and attendance details](operations-010.md#op-a8fbb3aac591d7), [get payroll dates for employee](operations-010.md#op-42bafa1f591990).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L97) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L505) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L853)

<a id="op-a8fbb3aac591d7"></a>
### Payroll Entry.get employee and attendance details

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_employee_and_attendance_details`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.isin(e ….

**Local steps**

- Set employees from list of emp.employee for emp drawn from self.employees.
  - Draw emp from self.employees.
- Set Employee from Platform.qb.DocType(“Employee”).
- Set Attendance from Platform.qb.DocType(“Attendance”).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.isin(e ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L96) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L504) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L852)

<a id="op-42bafa1f591990"></a>
### Payroll Entry.get payroll dates for employee

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_payroll_dates_for_employee`

**Inputs** self, employee\_details.

**Declared result** tuple at tuple(str, str).

**Explicit results** tuple(start\_date, end\_date).

**Local steps**

- Set start\_date from self.start\_date.
- If employee\_details.date\_of\_joining &gt; getdate(self.start\_date).
  - Set start\_date from employee\_details.date\_of\_joining.
- Set end\_date from self.end\_date.
- If (employee\_details.relieving\_date and employee\_details.relieving\_date &lt; getdate(self.end\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in employee\_details.relieving\_date → employee\_details.relieving\_date &lt; getdate(self.end\_date).
  - Set end\_date from employee\_details.relieving\_date.
- Return tuple(start\_date, end\_date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L1054) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L511) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L858)

<a id="op-4752abef3c66de"></a>
### Payroll Entry.create overtime slips

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_create_overtime_slips`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**State and service calls** call db\_set on self · enqueue with create\_overtime\_slips\_for\_employees · msgprint with translated “Overtime Slip creation is queued. It may take a few minutes”.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Bind dependencies create\_overtime\_slips\_for\_employees, filter\_employees\_for\_overtime\_slip\_creation.
- Set employee\_list from list of emp.employee for emp drawn from self.employees.
  - Draw emp from self.employees.
- Set employees from filter\_employees\_for\_overtime\_slip\_creation(self.start\_date, self.end\_date, employee\_list).
- If employees.
  - Set args from Platform.\_dict(mapping(“posting\_date” → self.posting\_date, “start\_date” → self.start\_date, “end\_date” → self.end\_date, “company” → self.company, …)).
  - If (len(employees) &gt; 30 or Platform.flags.enqueue\_payroll\_entry).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(employees) &gt; 30 → Platform.flags.enqueue\_payroll\_entry.
    - Evaluate self.db\_set(“status”, “Queued”).
    - Evaluate Platform.enqueue(create\_overtime\_slips\_for\_employees, timeout = 3000, employees = employees, args = args).
    - Evaluate Platform.msgprint(translated “Overtime Slip creation is queued. It may take a few minutes”, alert = true, indicator = “blue”).
  - Otherwise.
    - Evaluate create\_overtime\_slips\_for\_employees(employees, args).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · service or queued work from Platform.enqueue(create\_overtime\_slips\_for\_employees, timeout = 3000, employees = employees, args = args).

**Boundaries to resolve** stored data, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L1732) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L495) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L844)

<a id="op-bdfeb5c1b04912"></a>
### Payroll Entry.submit overtime slips

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_submit_overtime_slips`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**State and service calls** call db\_set on self · enqueue with submit\_overtime\_slips\_for\_employees · msgprint with translated “Overtime Slip submission is queued. It may take a few minutes”.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Bind dependencies submit\_overtime\_slips\_for\_employees.
- Set overtime\_slips from self.get\_unsubmitted\_overtime\_slips().
- If overtime\_slips.
  - If (len(overtime\_slips) &gt; 30 or Platform.flags.enqueue\_payroll\_entry).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(overtime\_slips) &gt; 30 → Platform.flags.enqueue\_payroll\_entry.
    - Evaluate self.db\_set(“status”, “Queued”).
    - Evaluate Platform.enqueue(submit\_overtime\_slips\_for\_employees, timeout = 3000, overtime\_slips = overtime\_slips, payroll\_entry = self.name).
    - Evaluate Platform.msgprint(translated “Overtime Slip submission is queued. It may take a few minutes”, alert = true, indicator = “blue”).
  - Otherwise.
    - Evaluate submit\_overtime\_slips\_for\_employees(overtime\_slips, self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get unsubmitted overtime slips](operations-010.md#op-98fb324f79fad1).

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · service or queued work from Platform.enqueue(submit\_overtime\_slips\_for\_employees, timeout = 3000, overtime\_slips = overtime\_slips, payroll\_entry = self.name).

**Boundaries to resolve** stored data, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L2301) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L535) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L882)

<a id="op-98fb324f79fad1"></a>
### Payroll Entry.get unsubmitted overtime slips

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_unsubmitted_overtime_slips`

**Inputs** self, limit = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** query.run(pluck = “name”).

**Local steps**

- Set OvertimeSlip from Platform.qb.DocType(“Overtime Slip”).
- Set query from nested operand in the contract.qb.from\_(OvertimeSlip).select(OvertimeSlip.name).where((OvertimeSlip.docstatus equals 0 bitwise and OvertimeSlip.payroll\_entry equals self.name)).
- If limit.
  - Set query from query.limit(limit).
- Return query.run(pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L2672) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L517) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L864)

<a id="op-1fb21bbfa3a585"></a>
### Payroll Entry.get overtime slip details

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_overtime_slip_details`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at bool.

**Record and data access** read “Payroll Settings” via get\_single\_value.

**Explicit results** list(len(employee\_eligible\_for\_overtime) &gt; 0, len(unsubmitted\_overtime\_slips) &gt; 0).

**Local steps**

- Bind dependencies filter\_employees\_for\_overtime\_slip\_creation.
- Set employee\_eligible\_for\_overtime, unsubmitted\_overtime\_slips from list().
- If Platform.db.get\_single\_value(“Payroll Settings”, “create\_overtime\_slip”).
  - Set employees from list of emp.employee for emp drawn from self.employees.
    - Draw emp from self.employees.
  - Set employee\_eligible\_for\_overtime from filter\_employees\_for\_overtime\_slip\_creation(self.start\_date, self.end\_date, employees).
  - Set unsubmitted\_overtime\_slips from self.get\_unsubmitted\_overtime\_slips(limit = 1).
- Return list(len(employee\_eligible\_for\_overtime) &gt; 0, len(unsubmitted\_overtime\_slips) &gt; 0).

**Methods declared on this owner** [get unsubmitted overtime slips](operations-010.md#op-98fb324f79fad1).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Payroll Settings”, “create\_overtime\_slip”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L2984) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L508) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L855)

<a id="op-a41b244086f842"></a>
### Get salary structure

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_get_salary_structure`

**Inputs** company, currency, salary\_slip\_based\_on\_timesheet, payroll\_frequency.

**Declared result** list at str.

**Explicit results** query.run(pluck = true).

**Local steps**

- Set SalaryStructure from Platform.qb.DocType(“Salary Structure”).
- Set query from nested operand in the contract.qb.from\_(SalaryStructure).select(SalaryStructure.name).where(((((nested operand in the contract.docstatus equals 1 bitwise and nested operand in the contract.is\_active equals ….
- If not salary\_slip\_based\_on\_timesheet.
  - Set query from query.where(SalaryStructure.payroll\_frequency equals payroll\_frequency).
- Return query.run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L3297) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L486) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L835)

<a id="op-3e0d055d992c89"></a>
### Get filtered employees

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_get_filtered_employees`

**Inputs** sal\_struct, filters, searchfield = no value, search\_string = no value, fields = no value, as\_dict = false, limit = no value, offset = no value, ignore\_match\_conditions = false.

**Declared result** list.

**Explicit results** query.run(as\_dict = as\_dict).

**Local steps**

- Set SalaryStructureAssignment from Platform.qb.DocType(“Salary Structure Assignment”).
- Set Employee from Platform.qb.DocType(“Employee”).
- Set query from nested operand in the contract(nested operand in the contract).join(SalaryStructureAssignment).on(Employee.name equals SalaryStructureAssignment.employee).where(((((((nested operand in the contract bitwise ….
- Set query from set\_fields\_to\_select(query, fields).
- Set query from set\_searchfield(query, searchfield, search\_string, qb\_object = Employee).
- Set query from set\_filter\_conditions(query, filters, qb\_object = Employee).
- If not ignore\_match\_conditions.
  - Set query from set\_match\_conditions(query = query, qb\_object = Employee).
- If limit.
  - Set query from query.limit(limit).
- If offset.
  - Set query from query.offset(offset).
- Return query.run(as\_dict = as\_dict).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L3689) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L482) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L831)

<a id="op-117919cbac6e34"></a>
### Set fields to select

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_set_fields_to_select`

**Inputs** query, fields = no value.

**Explicit results** query.

**Local steps**

- Set default\_fields from list(“employee”, “employee\_name”, “department”, “designation”).
- If fields.
  - Set query from query.select(expanded fields).distinct().
- Otherwise.
  - Set query from query.select(expanded default\_fields).distinct().
- Return query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L4516) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L543) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L890)

<a id="op-8050f1c8a7e018"></a>
### Set searchfield

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_set_searchfield`

**Inputs** query, searchfield, search\_string, qb\_object.

**Explicit results** query.

**Local steps**

- If searchfield.
  - Set query from query.where((qb\_object at searchfield.like(((“%” + search\_string) + “%”)) bitwise or qb\_object.employee\_name.like(((“%” + search\_string) + “%”)))).
- Return query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L4732) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L546) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L893)

<a id="op-c269864b011be5"></a>
### Set filter conditions

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_set_filter_conditions`

**Inputs** query, filters, qb\_object.

**Explicit results** query.

**Local steps**

- If filters.get(“employees”).
  - Set query from query.where(qb\_object.name.notin(filters.get(“employees”))).
- For each fltr\_key in list(“branch”, “department”, “designation”, “grade”).
  - If filters.get(fltr\_key).
    - Set query from query.where(qb\_object at fltr\_key equals filters at fltr\_key).
- Return query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L4913) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L544) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L891)

<a id="op-dbe832aea71f40"></a>
### Set match conditions

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_set_match_conditions`

**Inputs** query, qb\_object.

**Explicit results** query.

**Local steps**

- Set match\_conditions from get\_match\_cond(“Employee”, as\_condition = false).
- Set employee\_permission\_fields from get\_employee\_permission\_fields().
- For each cond in match\_conditions.
  - If isinstance(cond, dict).
    - For each tuple(key, value) in cond.items().
      - Set fieldname from employee\_permission\_fields.get(key).
      - If not fieldname.
        - Continue with the next iteration or loop test.
      - If isinstance(value, list).
        - Set query from query.where(qb\_object at fieldname.isin(value)).
      - Otherwise.
        - Set query from query.where(qb\_object at fieldname equals value).
- Return query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L5198) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L545) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L892)

<a id="op-042eb634f143f2"></a>
### Get employee permission fields

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_get_employee_permission_fields`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L5556) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L479) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L828)

<a id="op-9c1951234d43e3"></a>
### Remove payrolled employees

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_remove_payrolled_employees`

**Inputs** emp\_list, start\_date, end\_date.

**Explicit results** list of emp\_list at emp for emp drawn from emp\_list where emp does not belong to employees\_with\_payroll.

**Local steps**

- Set SalarySlip from Platform.qb.DocType(“Salary Slip”).
- Set employees\_with\_payroll from nested operand in the contract(nested operand in the contract).select(SalarySlip.employee).where(((nested operand in the contract.docstatus equals 1 bitwise and nested operand in the contract.start\_date eq ….
- Return list of emp\_list at emp for emp drawn from emp\_list where emp does not belong to employees\_with\_payroll.
  - Draw emp from emp\_list, keep a combination only if (emp does not belong to employees\_with\_payroll).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L5731) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L542) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L889)

<a id="op-9d6f397bf9106a"></a>
### Get start end dates

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_get_start_end_dates`

**Inputs** payroll\_frequency, start\_date = no value, company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(mapping(“start\_date” → start\_date, “end\_date” → end\_date)).

**Local steps**

- If (payroll\_frequency equals “Monthly” or payroll\_frequency equals “Bimonthly” or payroll\_frequency equals empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in payroll\_frequency equals “Monthly” → payroll\_frequency equals “Bimonthly” → payroll\_frequency equals empty text.
  - Set fiscal\_year from get\_fiscal\_year(start\_date, company = company) at 0.
  - Set month from (“%02d” modulo or format getdate(start\_date).month).
  - Set m from get\_month\_details(fiscal\_year, month).
  - If payroll\_frequency equals “Bimonthly”.
    - If getdate(start\_date).day ≤ 15.
      - Set start\_date from m at “month\_start\_date”.
      - Set end\_date from m at “month\_mid\_end\_date”.
    - Otherwise.
      - Set start\_date from m at “month\_mid\_start\_date”.
      - Set end\_date from m at “month\_end\_date”.
  - Otherwise.
    - Set start\_date from m at “month\_start\_date”.
    - Set end\_date from m at “month\_end\_date”.
- If payroll\_frequency equals “Weekly”.
  - Set end\_date from add\_days(start\_date, 6).
- If payroll\_frequency equals “Fortnightly”.
  - Set end\_date from add\_days(start\_date, 13).
- If payroll\_frequency equals “Daily”.
  - Set end\_date from start\_date.
- Return Platform.\_dict(mapping(“start\_date” → start\_date, “end\_date” → end\_date)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L6017) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L488) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L837)

<a id="op-c4269c241e58ee"></a>
### Get frequency kwargs

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_get_frequency_named_arguments`

**Inputs** frequency\_name.

**Explicit results** frequency\_dict.get(frequency\_name).

**Local steps**

- Set frequency\_dict from mapping(“monthly” → mapping(“months” → 1), “fortnightly” → mapping(“days” → 14), “weekly” → mapping(“days” → 7), “daily” → mapping(“days” → 1)).
- Return frequency\_dict.get(frequency\_name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L6684) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L483) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L832)

<a id="op-8386536a558544"></a>
### Get end date

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_get_end_date`

**Inputs** start\_date, frequency.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** dict(end\_date = end\_date.strftime(DATE\_FORMAT)) · dict(end\_date = empty text).

**Local steps**

- Set start\_date from getdate(start\_date).
- Set frequency from frequency.lower() when frequency, otherwise “monthly”.
  - Value choice on frequency — true gives frequency.lower(), false gives “monthly”.
- Set kwargs from get\_frequency\_kwargs(frequency) when frequency differs from “bimonthly”, otherwise get\_frequency\_kwargs(“monthly”).
  - Value choice on frequency differs from “bimonthly” — true gives get\_frequency\_kwargs(frequency), false gives get\_frequency\_kwargs(“monthly”).
- Set end\_date from (add\_to\_date(start\_date, expanded names kwargs) − relativedelta(days = 1)).
- If frequency differs from “bimonthly”.
  - Return dict(end\_date = end\_date.strftime(DATE\_FORMAT)).
- Otherwise.
  - Return dict(end\_date = empty text).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0117.json#L6859) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L480) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L829)

<a id="op-d47141bc1f7247"></a>
### Get month details

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_get_month_details`

**Inputs** year, month.

**Record and data access** read “Fiscal Year” via get\_value.

**Explicit results** Platform.\_dict(mapping(“year” → msd.year, “month\_start\_date” → msd, “month\_end\_date” → med, “month\_mid\_start\_date” → mid\_start, …)).

**Explicit failure paths** validation helper — translated “Fiscal Year {0} not found”.format(year).

**Local steps**

- Set ysd from Platform.db.get\_value(“Fiscal Year”, year, “year\_start\_date”).
- If ysd.
  - Bind dependencies calendar.
  - Bind dependencies datetime.
  - Set diff\_mnt from (cint(month) − cint(ysd.month)).
  - If diff\_mnt &lt; 0.
    - Set diff\_mnt from ((12 − int(ysd.month)) + cint(month)).
  - Set msd from (ysd + relativedelta(months = diff\_mnt)).
  - Set month\_days from cint(calendar.monthrange(cint(msd.year), cint(month)) at 1).
  - Set mid\_start from datetime.date(msd.year, cint(month), 16).
  - Set mid\_end from datetime.date(msd.year, cint(month), 15).
  - Set med from datetime.date(msd.year, cint(month), month\_days).
  - Return Platform.\_dict(mapping(“year” → msd.year, “month\_start\_date” → msd, “month\_end\_date” → med, “month\_mid\_start\_date” → mid\_start, …)).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Fiscal Year {0} not found”.format(year)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0118.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L484) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L833)

<a id="op-1388addb75ae72"></a>
### Log payroll failure

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_log_payroll_failure`

**Inputs** process, payroll\_entry, error.

**State and service calls** call db\_set on payroll\_entry.

**Local steps**

- Set error\_log from Platform.log\_error(title = translated “Salary Slip {0} failed for Payroll Entry {1}”.format(process, payroll\_entry.name)).
- Set message\_log from Platform.message\_log.pop() when Platform.message\_log, otherwise str(error).
  - Value choice on Platform.message\_log — true gives Platform.message\_log.pop(), false gives str(error).
- Attempt the following.
  - If isinstance(message\_log, str).
    - Set error\_message from json.loads(message\_log).get(“message”).
  - Otherwise.
    - Set error\_message from message\_log.get(“message”).
- On failure (Exception).
  - Set error\_message from message\_log.
- Update error\_message using + (whitespace '\\n' + translated “Check Error Log {0} for more details.”.format(get\_link\_to\_form(“Error Log”, error\_log.name))).
- Evaluate payroll\_entry.db\_set(mapping(“error\_message” → error\_message, “status” → “Failed”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0118.json#L694) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L489) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L838)

<a id="op-5813662ba9d1eb"></a>
### Create salary slips for employees

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_create_salary_slips_for_employees`

**Inputs** employees, args, publish\_progress = true.

**Record and data access** resolve a document from “Payroll Entry” via get\_cached\_doc · resolve a document from slip\_args via get\_doc.

**State and service calls** call insert on Platform.get\_doc(slip\_args) · call db\_set on payroll\_entry · msgprint with translated “Salary Slips already exist for employees {}, and will not be processed by this payroll.”.format(Platform.bold(“, ”.join(generator of emp for emp drawn from salary\_slips\_exist\_for))) · rollback · commit · 1 additional forms in the steps below.

**Local steps**

- Set payroll\_entry from Platform.get\_cached\_doc(“Payroll Entry”, args.payroll\_entry).
- Attempt the following.
  - Set salary\_slips\_exist\_for from get\_existing\_salary\_slips(employees, args).
  - Set count from 0.
  - Set employees from list((set(employees) − set(salary\_slips\_exist\_for))).
  - For each emp in employees.
    - Set slip\_args from mapping(“doctype” → “Salary Slip”, “employee” → emp, “salary\_slip\_based\_on\_timesheet” → args.get(“salary\_slip\_based\_on\_timesheet”), “payroll\_frequency” → args.get(“payroll\_frequency”), …).
    - Evaluate Platform.get\_doc(slip\_args).insert().
    - Update count using + 1.
    - If publish\_progress.
      - Evaluate Platform.publish\_progress(((count × 100) ÷ len(employees)), title = translated “Creating Salary Slips...”).
  - Evaluate payroll\_entry.db\_set(mapping(“status” → “Submitted”, “salary\_slips\_created” → 1, “error\_message” → empty text)).
  - If salary\_slips\_exist\_for.
    - Evaluate Platform.msgprint(translated “Salary Slips already exist for employees {}, and will not be processed by this payroll.”.format(Platform.bold(“, ”.join(generator of emp for emp drawn from salary\_slips\_exist\_ ….
      - Draw emp from salary\_slips\_exist\_for.
- On failure (Exception) bound to e.
  - If not Platform.in\_test.
    - Evaluate Platform.db.rollback().
  - Evaluate log\_payroll\_failure(“creation”, payroll\_entry, e).
- On exit, including pending return or failure.
  - If not Platform.in\_test.
    - Evaluate Platform.db.commit().
  - Evaluate Platform.publish\_realtime(“completed\_salary\_slip\_creation”, user = Platform.session.user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Payroll Entry”, args.payroll\_entry) · service or queued work from Platform.publish\_realtime(“completed\_salary\_slip\_creation”, user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0118.json#L1146) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L476) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L825)
