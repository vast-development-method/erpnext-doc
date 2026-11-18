# Payroll and benefits · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Salary structure

[Record definition](../../../../data/record-types/salary_structure.json)

<a id="op-22c3f5e9c7a467"></a>
### Salary Structure.validate

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_missing\_values().
- Evaluate self.validate\_amount().
- Evaluate self.validate\_component\_based\_on\_tax\_slab().
- Evaluate self.validate\_payment\_days\_based\_dependent\_component().
- Evaluate self.validate\_timesheet\_component().
- Evaluate self.validate\_formula\_setup().
- Evaluate validate\_max\_benefit\_for\_flexible\_benefit(self.employee\_benefits, self.max\_benefits).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set missing values](operations-019.md#op-910a0cbc5f6aed), [validate amount](operations-019.md#op-c1cadebc0ceb10), [validate component based on tax slab](operations-019.md#op-9c1db6e59d21c2), [validate payment days based dependent component](operations-019.md#op-df3f056958f1a2), [validate timesheet component](operations-019.md#op-b8957e06dfe88a), [validate formula setup](operations-019.md#op-2baa3bcb4dcbd5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L1633) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L894) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1241)

<a id="op-0226f2e0dcb092"></a>
### Salary Structure.on update

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.reset\_condition\_and\_formula\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset condition and formula fields](operations-019.md#op-b4a37b71fbf242).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L1817) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L889) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1236)

<a id="op-bcfbd2e6b05f8b"></a>
### Salary Structure.on update after submit

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_on_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.reset\_condition\_and\_formula\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset condition and formula fields](operations-019.md#op-b4a37b71fbf242).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L1868) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L890) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1237)

<a id="op-2baa3bcb4dcbd5"></a>
### Salary Structure.validate formula setup

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_validate_formula_setup`

**Inputs** self.

**State and service calls** msgprint with translated “{0} Row #{1}: Formula is set but {2} is disabled for the Salary Component {3}.”.format(table.capitalize(), row.idx, Platform.bold(translated “Amount Based on Formula”), Platform.bold(row.salary ….

**Local steps**

- For each table in COMPONENT\_PARENTFIELDS.
  - For each row in self.get(table).
    - If (not row.amount\_based\_on\_formula and row.formula).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.amount\_based\_on\_formula → row.formula.
      - Evaluate Platform.msgprint(translated “{0} Row #{1}: Formula is set but {2} is disabled for the Salary Component {3}.”.format(table.capitalize(), row.idx, Platform.bold(translated “Amount Based on Formula”), Platfo ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L1919) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L897) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1244)

<a id="op-910a0cbc5f6aed"></a>
### Salary Structure.set missing values

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_set_missing_values`

**Inputs** self.

**Record and data access** read “Salary Component” via get\_value.

**Local steps**

- Set overwritten\_fields from list(“depends\_on\_payment\_days”, “variable\_based\_on\_taxable\_salary”, “is\_tax\_applicable”, “is\_flexible\_benefit”).
- Set overwritten\_fields\_if\_missing from list(“amount\_based\_on\_formula”, “formula”, “amount”).
- For each table in COMPONENT\_PARENTFIELDS.
  - For each d in self.get(table).
    - Set component\_default\_value from Platform.db.get\_value(“Salary Component”, cstr(d.salary\_component), (overwritten\_fields + overwritten\_fields\_if\_missing), as\_dict = 1).
    - If component\_default\_value.
      - For each fieldname in overwritten\_fields.
        - Set value from component\_default\_value.get(fieldname).
        - If d.get(fieldname) differs from value.
          - Evaluate d.set(fieldname, value).
      - If not (d.get(“amount”) or d.get(“formula”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.get(“amount”) → d.get(“formula”).
        - For each fieldname in overwritten\_fields\_if\_missing.
          - Evaluate d.set(fieldname, component\_default\_value.get(fieldname)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L2199) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L893) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1240)

<a id="op-9c1db6e59d21c2"></a>
### Salary Structure.validate component based on tax slab

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_validate_component_based_on_tax_slab`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Cannot set amount or formula for Salary Component {1} with Variable Based On Taxable Salary”.format(row.idx, row.salary\_component).

**Local steps**

- For each row in self.deductions.
  - If (row.variable\_based\_on\_taxable\_salary and (row.amount or row.formula)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.variable\_based\_on\_taxable\_salary → (row.amount or row.formula).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.amount → row.formula.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot set amount or formula for Salary Component {1} with Variable Based On Taxable Salary”.format(row.idx, row.salary\_component)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L2689) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L896) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1243)

<a id="op-c1cadebc0ceb10"></a>
### Salary Structure.validate amount

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_validate_amount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Net pay cannot be negative”.

**Local steps**

- If (flt(self.net\_pay) &lt; 0 and self.salary\_slip\_based\_on\_timesheet).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.net\_pay) &lt; 0 → self.salary\_slip\_based\_on\_timesheet.
  - Call the validation error handler Platform.throw(translated “Net pay cannot be negative”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L2851) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L895) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1242)

<a id="op-df3f056958f1a2"></a>
### Salary Structure.validate payment days based dependent component

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_validate_payment_days_based_dependent_component`

**Inputs** self.

**Explicit failure paths** validation helper — message.

**Local steps**

- Set abbreviations from self.get\_component\_abbreviations().
- For each component\_type in COMPONENT\_PARENTFIELDS.
  - For each row in self.get(component\_type).
    - If (row.formula and row.depends\_on\_payment\_days and any(generator of re.search(((“\\b” + abbr) + “\\b”), row.formula) for abbr drawn from abbreviations)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.formula → row.depends\_on\_payment\_days → any(generator of re.search(((“\\b” + abbr) + “\\b”), row.formula) for abbr drawn from abbreviations).
      - Draw abbr from abbreviations.
      - Set message from translated “Row #{0}: The {1} Component has the options {2} and {3} enabled.”.format(row.idx, Platform.bold(row.salary\_component), Platform.bold(translated “Amount based on formula”), Platform.bold(transla ….
      - Update message using + (text in the contract + translated “Disable {0} for the {1} component, to prevent the amount from being deducted twice, as its formula already u …”.format(Platform.bold(translated “Depends On Payment Days” ….
      - Call the validation error handler Platform.throw(message, title = translated “Payment Days Dependency”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get component abbreviations](operations-019.md#op-2a562e40cff28a).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L2974) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L898) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1245)

<a id="op-2a562e40cff28a"></a>
### Salary Structure.get component abbreviations

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_get_component_abbreviations`

**Inputs** self.

**Explicit results** abbr.

**Local steps**

- Set abbr from list().
- For each table in COMPONENT\_PARENTFIELDS.
  - Update abbr using + list of d.abbr for d drawn from self.get(table) where d.depends\_on\_payment\_days.
    - Draw d from self.get(table), keep a combination only if (d.depends\_on\_payment\_days).
- Return abbr.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L3475) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L887) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1234)

<a id="op-b8957e06dfe88a"></a>
### Salary Structure.validate timesheet component

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_validate_timesheet_component`

**Inputs** self.

**State and service calls** msgprint with translated “Row #{0}: Timesheet amount will overwrite the Earning component amount for the Salary Component {1}”.format(self.idx, Platform.bold(self.salary\_component)).

**Explicit results** no value.

**Local steps**

- If not self.salary\_slip\_based\_on\_timesheet.
  - Return no value.
- For each component in self.earnings.
  - If component.salary\_component equals self.salary\_component.
    - Evaluate Platform.msgprint(translated “Row #{0}: Timesheet amount will overwrite the Earning component amount for the Salary Component {1}”.format(self.idx, Platform.bold(self.salary\_component)), title = translated ….
    - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L3602) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L899) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1246)

<a id="op-8108baa607c6bc"></a>
### Salary Structure.sanitize condition and formula fields

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_sanitize_condition_and_formula_fields`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** self.

**Local structure** 2 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L3831) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L892) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1239)

<a id="op-b4a37b71fbf242"></a>
### Salary Structure.reset condition and formula fields

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_reset_condition_and_formula_fields`

**Inputs** self.

**Local steps**

- For each table in COMPONENT\_PARENTFIELDS.
  - For each row in self.get(table).
    - Set row.condition from row.\_condition.
    - Set row.formula from row.\_formula.
- Evaluate self.db\_update\_all().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L4124) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L891) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1238)

<a id="op-d570edf5dbf5c6"></a>
### Salary Structure.get employees

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_get_employees`

**Inputs** self, remaining named values kwargs.

**Record and data access** read “Employee” via get\_list.

**Explicit results** Platform.get\_list(“Employee”, filters = mapping(“status” → “Active”, expand filters), pluck = “name”).

**Local steps**

- Set filters from mapping of field → value for tuple(field, value) drawn from kwargs.items() where value.
  - Draw tuple(field, value) from kwargs.items(), keep a combination only if (value).
- Return Platform.get\_list(“Employee”, filters = mapping(“status” → “Active”, expand filters), pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L7) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L888) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1235)

<a id="op-9555d3b912bbc1"></a>
### Salary Structure.assign salary structure

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_salary_structure_assign_salary_structure`

**Inputs** self, branch = no value, grade = no value, department = no value, designation = no value, employee = no value, payroll\_payable\_account = no value, from\_date = no value, base = no value, variable = no value, income\_tax\_slab = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**State and service calls** enqueue with assign\_salary\_structure\_for\_employees · msgprint with translated “No Employee Found”.

**Local steps**

- Set employees from self.get\_employees(company = self.company, grade = grade, department = department, designation = designation, …).
- If employees.
  - If len(employees) &gt; 20.
    - Evaluate Platform.enqueue(assign\_salary\_structure\_for\_employees, timeout = 3000, employees = employees, salary\_structure = self, payroll\_payable\_account = payroll\_payable\_account, …).
  - Otherwise.
    - Evaluate assign\_salary\_structure\_for\_employees(employees, self, payroll\_payable\_account = payroll\_payable\_account, from\_date = from\_date, base = base, variable = variable, …).
- Otherwise.
  - Evaluate Platform.msgprint(translated “No Employee Found”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get employees](operations-019.md#op-d570edf5dbf5c6).

**Values supplied outside this operation** service or queued work from Platform.enqueue(assign\_salary\_structure\_for\_employees, timeout = 3000, employees = employees, salary\_structure = self, payroll\_payable\_account = payroll\_payable\_account, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L4561) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L884) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1231)

<a id="op-8e4e10b47bb28c"></a>
### Assign salary structure for employees

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_assign_salary_structure_for_employees`

**Inputs** employees, salary\_structure, payroll\_payable\_account = no value, from\_date = no value, base = no value, variable = no value, income\_tax\_slab = no value.

**State and service calls** savepoint savepoint · rollback · msgprint with translated “Structures have been assigned successfully”.

**Local steps**

- Set assignments from list().
- Set existing\_assignments\_for from get\_existing\_assignments(employees, salary\_structure, from\_date).
- Set count from 0.
- Set savepoint from “before\_assignment\_submission”.
- For each employee in employees.
  - Attempt the following.
    - Evaluate Platform.db.savepoint(savepoint).
    - If employee belongs to existing\_assignments\_for.
      - Continue with the next iteration or loop test.
    - Update count using + 1.
    - Set assignment from create\_salary\_structure\_assignment(employee, salary\_structure.name, salary\_structure.company, salary\_structure.currency, …).
    - Evaluate assignments.append(assignment).
    - Evaluate Platform.publish\_progress(((count × 100) ÷ len((set(employees) − set(existing\_assignments\_for)))), title = translated “Assigning Structures...”).
  - On failure (Exception).
    - Evaluate Platform.db.rollback(save\_point = savepoint).
    - Evaluate Platform.log\_error(formatted text Salary Structure Assignment failed for employee {employee}, reference\_doctype = “Salary Structure Assignment”).
- If assignments.
  - Evaluate Platform.msgprint(translated “Structures have been assigned successfully”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L5199) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L876) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1223)

<a id="op-9a10504dcc6300"></a>
### Create salary structure assignment

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_create_salary_structure_assignment`

**Inputs** employee, salary\_structure, company, currency, from\_date, payroll\_payable\_account = no value, base = no value, variable = no value, income\_tax\_slab = no value.

**Record and data access** read “Company” via get\_value · read “Account” via get\_value.

**State and service calls** request new\_doc for “Salary Structure Assignment” · call save on assignment · call submit on assignment.

**Explicit results** assignment.name.

**Explicit failure paths** validation helper — translated “Please set "Default Payroll Payable Account" in Company Defaults” · validation helper — translated “Invalid Payroll Payable Account. The account currency must be {0} or {1}”.format(currency, company\_curency).

**Local steps**

- Set assignment from Platform.new\_doc(“Salary Structure Assignment”).
- If not payroll\_payable\_account.
  - Set payroll\_payable\_account from Platform.db.get\_value(“Company”, company, “default\_payroll\_payable\_account”).
  - If not payroll\_payable\_account.
    - Call the validation error handler Platform.throw(translated “Please set "Default Payroll Payable Account" in Company Defaults”).
- Set payroll\_payable\_account\_currency from Platform.db.get\_value(“Account”, payroll\_payable\_account, “account\_currency”).
- Set company\_curency from Enterprise.get\_company\_currency(company).
- If (payroll\_payable\_account\_currency differs from currency and payroll\_payable\_account\_currency differs from company\_curency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in payroll\_payable\_account\_currency differs from currency → payroll\_payable\_account\_currency differs from company\_curency.
  - Call the validation error handler Platform.throw(translated “Invalid Payroll Payable Account. The account currency must be {0} or {1}”.format(currency, company\_curency)).
- Set assignment.employee from employee.
- Set assignment.salary\_structure from salary\_structure.
- Set assignment.company from company.
- Set assignment.currency from currency.
- Set assignment.payroll\_payable\_account from payroll\_payable\_account.
- Set assignment.from\_date from from\_date.
- Set assignment.base from base.
- Set assignment.variable from variable.
- Set assignment.income\_tax\_slab from income\_tax\_slab.
- Evaluate assignment.save().
- Evaluate assignment.submit().
- Return assignment.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L4) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L877) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1224)

<a id="op-16685d4073a20a"></a>
### Get existing assignments

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_get_existing_assignments`

**Inputs** employees, salary\_structure, from\_date.

**State and service calls** msgprint with translated “Skipping Salary Structure Assignment for the following employees, as Salary Structure Assignment records alr …”.format(whitespace '\\n'.join(salary\_structures\_assignments)).

**Explicit results** salary\_structures\_assignments.

**Local steps**

- Set ssa from Platform.qb.DocType(“Salary Structure Assignment”).
- Set salary\_structures\_assignments from nested operand in the contract(nested operand in the contract).distinct().where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equ ….
- If salary\_structures\_assignments.
  - Evaluate Platform.msgprint(translated “Skipping Salary Structure Assignment for the following employees, as Salary Structure Assignment records alr …”.format(whitespace '\\n'.join(salary\_structures\_assignments))).
- Return salary\_structures\_assignments.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0137.json#L6438) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L879) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1226)

<a id="op-669ac71cea1238"></a>
### Make salary slip

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_make_salary_slip`

**Inputs** source\_name, target\_doc = no value, employee = no value, posting\_date = no value, as\_print = false, print\_format = no value, for\_preview = 0, lwp\_days\_corrected = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (str bitwise or Document).

**Explicit results** \_make\_salary\_slip(source\_name, target\_doc = target\_doc, employee = employee, posting\_date = posting\_date, as\_print = as\_print, …).

**Local steps**

- Return \_make\_salary\_slip(source\_name, target\_doc = target\_doc, employee = employee, posting\_date = posting\_date, as\_print = as\_print, …).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L5) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L881) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1228)

<a id="op-6bafce9f09910e"></a>
### Make salary slip

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_make_salary_slip_2`

**Inputs** source\_name, target\_doc = no value, employee = no value, posting\_date = no value, as\_print = false, print\_format = no value, for\_preview = 0, lwp\_days\_corrected = no value, ignore\_permissions = false.

**Declared result** (str bitwise or Document).

**Explicit results** Platform.get\_print(doc.doctype, doc.name, doc = doc, print\_format = print\_format) · doc.

**Local steps**

- If employee.
  - Evaluate Platform.has\_permission(“Employee”, “read”, employee, throw = true).
- Bind local operation postprocess for subsequent calls.
- Set doc from get\_mapped\_doc(“Salary Structure”, source\_name, mapping(“Salary Structure” → mapping(“doctype” → “Salary Slip”, “field\_map” → mapping(“total\_earning” → “gross\_pay”, “name” → “salary\_structure”, “currency”  ….
- If cint(as\_print).
  - Set doc.name from formatted text Preview for {employee}.
  - Return Platform.get\_print(doc.doctype, doc.name, doc = doc, print\_format = print\_format).
- Otherwise.
  - Return doc.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee, throw = true).

**Boundaries to resolve** callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L882) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1229)

<a id="op-6db49543e0e0ff"></a>
### Make salary slip.postprocess

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_make_salary_slip_postprocess`

**Inputs** source, target.

**Local steps**

- If employee.
  - Set target.employee from employee.
  - If posting\_date.
    - Set target.posting\_date from posting\_date.
- Evaluate target.run\_method(“process\_salary\_structure”, for\_preview = for\_preview, lwp\_days\_corrected = lwp\_days\_corrected).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“process\_salary\_structure”, for\_preview = for\_preview, lwp\_days\_corrected = lwp\_days\_corrected).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0138.json#L1063) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L883) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1230)

<a id="op-3492e548003ec2"></a>
### Get employees

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_get_employees`

**Inputs** salary\_structure.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Record and data access** read “Salary Structure Assignment” via get\_list.

**Explicit results** list(set(employees)).

**Explicit failure paths** validation helper — translated “There's no Employee with Salary Structure: {0}. Assign {1} to an Employee to preview Salary Slip”.format(salary\_structure, salary\_structure).

**Local steps**

- Set employees from Platform.get\_list(“Salary Structure Assignment”, filters = mapping(“salary\_structure” → salary\_structure, “docstatus” → 1), pluck = “employee”).
- If not employees.
  - Call the validation error handler Platform.throw(translated “There's no Employee with Salary Structure: {0}. Assign {1} to an Employee to preview Salary Slip”.format(salary\_structure, salary\_structure)).
- Return list(set(employees)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0138.json#L1197) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L878) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1225)

<a id="op-daccd1514bf02e"></a>
### Get salary component

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_get_salary_component`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Declared result** list.

**Explicit results** accounts.

**Local steps**

- Set sc from Platform.qb.DocType(“Salary Component”).
- Set sca from Platform.qb.DocType(“Salary Component Account”).
- Set salary\_components from nested operand in the contract(nested operand in the contract).limit(page\_len).offset(start).run(as\_dict = true).
- Set accounts from list().
- For each component in salary\_components.
  - If not component.company.
    - Evaluate accounts.append(tuple(component.name, component.account, component.company)).
  - Otherwise.
    - If component.company equals filters at “company”.
      - Evaluate accounts.append(tuple(component.name, component.account, component.company)).
- Return accounts.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0138.json#L1461) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L880) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1227)

<a id="op-c82a276360b103"></a>
### Validate max benefit for flexible benefit

`operation_workforce_payroll_record_definitions_salary_structure_business_behavior_validate_maximum_benefit_for_flexible_benefit`

**Inputs** employee\_benefits, max\_benefits = no value.

**Record and data access** read “Salary Component” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Salary Component {0} cannot be selected more than once in Employee Benefits”.format(benefit.salary\_component) · validation helper — translated “Benefit amount {0} for Salary Component {1} should not be greater than maximum benefit amount {2} set in {3}”.format(benefit.amount, benefit.salary\_component, max\_of\_component, get\_link\_to\_form … · validation helper — translated “Total of all employee benefits cannot be greater that Max Benefits Amount {0}”.format(max\_benefits).

**Local steps**

- If not employee\_benefits.
  - Return no value.
- Set benefit\_total from 0.
- Set benefit\_components from list().
- For each benefit in employee\_benefits.
  - If benefit.salary\_component belongs to benefit\_components.
    - Call the validation error handler Platform.throw(translated “Salary Component {0} cannot be selected more than once in Employee Benefits”.format(benefit.salary\_component)).
  - Update benefit\_total using + benefit.amount.
  - Set max\_of\_component from Platform.db.get\_value(“Salary Component”, benefit.salary\_component, “max\_benefit\_amount”).
  - If (max\_of\_component and max\_of\_component &gt; 0 and benefit.amount &gt; max\_of\_component).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_of\_component → max\_of\_component &gt; 0 → benefit.amount &gt; max\_of\_component.
    - Call the validation error handler Platform.throw(translated “Benefit amount {0} for Salary Component {1} should not be greater than maximum benefit amount {2} set in {3}”.format(benefit.amount, benefit.salary\_component, max\_of\_component, g ….
  - Evaluate benefit\_components.append(benefit.salary\_component).
- If (max\_benefits and benefit\_total &gt; max\_benefits).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_benefits → benefit\_total &gt; max\_benefits.
  - Call the validation error handler Platform.throw(translated “Total of all employee benefits cannot be greater that Max Benefits Amount {0}”.format(max\_benefits), title = translated “Invalid Benefit Amounts”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0138.json#L2205) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L900) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1247)

<a id="op-1168e29628acf5"></a>
### Get data

`operation_workforce_payroll_record_definitions_salary_structure_salary_structure_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “salary\_structure”, “non\_standard\_fieldnames” → mapping(“Employee Grade” → “default\_salary\_structure”), “transactions” → list(mapping(“items” → list(“Salary Structure Assignment”, “Sa ….

**Local steps**

- Return mapping(“fieldname” → “salary\_structure”, “non\_standard\_fieldnames” → mapping(“Employee Grade” → “default\_salary\_structure”), “transactions” → list(mapping(“items” → list(“Salary Structure Assignment”, “Sa ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0138.json#L2750) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L901) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1248)
