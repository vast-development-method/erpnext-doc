# Payroll and benefits · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payroll entry

[Record definition](../../../../data/record-types/payroll_entry.json)

<a id="op-57b437acf0db73"></a>
### Payroll Entry.submit salary slips

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_submit_salary_slips`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**State and service calls** call db\_set on self · enqueue with submit\_salary\_slips\_for\_employees · msgprint with translated “Salary Slip submission is queued. It may take a few minutes”.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set salary\_slips from self.get\_sal\_slip\_list(ss\_status = 0).
- If (len(salary\_slips) &gt; 30 or Platform.flags.enqueue\_payroll\_entry).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(salary\_slips) &gt; 30 → Platform.flags.enqueue\_payroll\_entry.
  - Evaluate self.db\_set(“status”, “Queued”).
  - Evaluate Platform.enqueue(submit\_salary\_slips\_for\_employees, timeout = 3000, payroll\_entry = self, salary\_slips = salary\_slips, publish\_progress = false).
  - Evaluate Platform.msgprint(translated “Salary Slip submission is queued. It may take a few minutes”, alert = true, indicator = “blue”).
- Otherwise.
  - Evaluate submit\_salary\_slips\_for\_employees(self, salary\_slips, publish\_progress = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sal slip list](operations-008.md#op-f5575160dcd091).

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · service or queued work from Platform.enqueue(submit\_salary\_slips\_for\_employees, timeout = 3000, payroll\_entry = self, salary\_slips = salary\_slips, publish\_progress = false).

**Boundaries to resolve** stored data, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L3093) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L536) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L883)

<a id="op-d0502526abe9f9"></a>
### Payroll Entry.email salary slip

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_email_salary_slip`

**Inputs** self, submitted\_ss.

**Record and data access** read “Payroll Settings” via get\_single\_value.

**Local steps**

- If Platform.db.get\_single\_value(“Payroll Settings”, “email\_salary\_slip\_to\_employee”).
  - For each ss in submitted\_ss.
    - Evaluate ss.email\_salary\_slip().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Payroll Settings”, “email\_salary\_slip\_to\_employee”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L3465) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L498) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L847)

<a id="op-21727c2972e204"></a>
### Payroll Entry.get salary component account

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_salary_component_account`

**Inputs** self, salary\_component.

**Record and data access** read “Salary Component Account” via get\_value.

**Explicit results** account.

**Explicit failure paths** validation helper — translated “Please set account in Salary Component {0}”.format(get\_link\_to\_form(“Salary Component”, salary\_component)).

**Local steps**

- Set account from Platform.db.get\_value(“Salary Component Account”, mapping(“parent” → salary\_component, “company” → self.company), “account”, cache = true).
- If not account.
  - Call the validation error handler Platform.throw(translated “Please set account in Salary Component {0}”.format(get\_link\_to\_form(“Salary Component”, salary\_component))).
- Return account.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L3580) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L512) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L859)

<a id="op-bd21865a3cce0b"></a>
### Payroll Entry.get salary components

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_salary_components`

**Inputs** self, component\_type.

**Explicit results** salary\_components.

**Local steps**

- Set salary\_slips from self.get\_sal\_slip\_list(ss\_status = 1, as\_dict = true).
- If salary\_slips.
  - Set ss from Platform.qb.DocType(“Salary Slip”).
  - Set ssd from Platform.qb.DocType(“Salary Detail”).
  - Set salary\_components from nested operand in the contract(nested operand in the contract).select(ssd.salary\_component, ssd.amount, ssd.parentfield, ssd.additional\_salary, …).where(((nested operand in the contract.parentfield equals  ….
    - Draw d from salary\_slips.
  - Return salary\_components.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sal slip list](operations-008.md#op-f5575160dcd091).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L3816) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L514) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L861)

<a id="op-b0cb9cdd9d66dd"></a>
### Payroll Entry.get salary component total

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_salary_component_total`

**Inputs** self, component\_type = no value, employee\_wise\_accounting\_enabled = false.

**Explicit results** account\_details.

**Local steps**

- Set salary\_components from self.get\_salary\_components(component\_type).
- If salary\_components.
  - Set component\_dict from mapping().
  - Set advance\_deductions from self.get\_advance\_deductions(component\_type, salary\_components).
  - For each item in salary\_components.
    - Set employee\_cost\_centers from self.get\_payroll\_cost\_centers\_for\_employee(item.employee, item.salary\_structure).
    - Set employee\_advance from advance\_deductions.get(item.additional\_salary).
    - For each tuple(cost\_center, percentage) in employee\_cost\_centers.items().
      - Set amount\_against\_cost\_center from ((flt(item.amount) × percentage) ÷ 100).
      - If employee\_advance.
        - Evaluate self.add\_advance\_deduction\_entry(item, amount\_against\_cost\_center, cost\_center, employee\_advance).
      - Otherwise.
        - Set key from tuple(item.salary\_component, cost\_center).
        - Set component\_dict at key from (component\_dict.get(key, 0) + amount\_against\_cost\_center).
      - If employee\_wise\_accounting\_enabled.
        - Evaluate self.set\_employee\_based\_payroll\_payable\_entries(component\_type, item.employee, amount\_against\_cost\_center).
  - Set account\_details from self.get\_account(component\_dict = component\_dict).
  - Return account\_details.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get salary components](operations-009.md#op-bd21865a3cce0b), [get advance deductions](operations-009.md#op-03a60913e60edf), [get payroll cost centers for employee](operations-009.md#op-25d4d56bcb6d03), [add advance deduction entry](operations-009.md#op-de1cffdaf8864a), [set employee based payroll payable entries](operations-009.md#op-a24f505bc66216), [get account](operations-009.md#op-b476b4815df073).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L98) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L513) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L860)

<a id="op-03a60913e60edf"></a>
### Payroll Entry.get advance deductions

`operation_workforce_binding_workforce_payroll_doctype_payroll_entry_payroll_entry_payrollentry_get_advance_deductions`

**Inputs** self, component\_type, salary\_components.

**Declared result** dict at tuple(str, dict).

**Explicit results** mapping() · mapping of d.additional\_salary → d for d drawn from advances.

**Local steps**

- Set additional\_salaries from list(set of d.additional\_salary for d drawn from salary\_components where d.additional\_salary).
  - Draw d from salary\_components, keep a combination only if (d.additional\_salary).
- If (component\_type differs from “deductions” or not additional\_salaries).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in component\_type differs from “deductions” → not additional\_salaries.
  - Return mapping().
- Set AdditionalSalary from Platform.qb.DocType(“Additional Salary”).
- Set EmployeeAdvance from Platform.qb.DocType(“Employee Advance”).
- Set advances from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.isin(additional\_salaries)).where(Addition ….
- Return mapping of d.additional\_salary → d for d drawn from advances.
  - Draw d from advances.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L174) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L225) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L225)

<a id="op-de1cffdaf8864a"></a>
### Payroll Entry.add advance deduction entry

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_add_advance_deduction_entry`

**Inputs** self, item, amount, cost\_center, employee\_advance.

**Declared result** no value.

**Local steps**

- Evaluate self.\_advance\_deduction\_entries.append(mapping(“employee” → item.employee, “account” → employee\_advance.advance\_account, “amount” → amount, “cost\_center” → cost\_center, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L95) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L490) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L839)

<a id="op-2666a9da36fc55"></a>
### Payroll Entry.set accounting entries for advance deductions

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_set_accounting_entries_for_advance_deductions`

**Inputs** self, accounts, currencies, company\_currency, accounting\_dimensions, precision, payable\_amount.

**Explicit results** payable\_amount.

**Local steps**

- For each entry in self.\_advance\_deduction\_entries.
  - Set payable\_amount from self.get\_accounting\_entries\_and\_payable\_amount(entry.get(“account”), entry.get(“cost\_center”), entry.get(“amount”), currencies, entry\_type = “credit”, accounts = accounts, party = entry.get(“employee”), re ….
- Return payable\_amount.

**Methods declared on this owner** [get accounting entries and payable amount](operations-009.md#op-8c5f688824e697).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L5278) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L528) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L875)

<a id="op-a24f505bc66216"></a>
### Payroll Entry.set employee based payroll payable entries

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_set_employee_based_payroll_payable_entries`

**Inputs** self, component\_type, employee, amount, salary\_structure = no value.

**Local steps**

- Set employee\_details from self.employee\_based\_payroll\_payable\_entries.setdefault(employee, mapping()).
- Evaluate employee\_details.setdefault(component\_type, 0).
- Update employee\_details at component\_type using + amount.
- If (salary\_structure and “salary\_structure” does not belong to employee\_details).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in salary\_structure → “salary\_structure” does not belong to employee\_details.
  - Set employee\_details at “salary\_structure” from salary\_structure.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L5639) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L530) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L877)

<a id="op-25d4d56bcb6d03"></a>
### Payroll Entry.get payroll cost centers for employee

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_payroll_cost_centers_for_employee`

**Inputs** self, employee, salary\_structure.

**Record and data access** read “Employee” via get\_cached\_value · read “Department” via get\_cached\_value.

**Explicit results** self.employee\_cost\_centers.get(employee, mapping()).

**Local steps**

- If not hasattr(self, “employee\_cost\_centers”).
  - Set self.employee\_cost\_centers from mapping().
- If not self.employee\_cost\_centers.get(employee).
  - Set SalaryStructureAssignment from Platform.qb.DocType(“Salary Structure Assignment”).
  - Set EmployeeCostCenter from Platform.qb.DocType(“Employee Cost Center”).
  - Set assignment\_subquery from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract ≤ nested operand ….
  - Set cost\_centers from dict(nested operand in the contract.select(nested operand in the contract.cost\_center, nested operand in the contract.percentage).where(EmployeeCostCenter.parent equals assignment\_subquery).run(as\_list = true)).
  - If not cost\_centers.
    - Set tuple(default\_cost\_center, department) from Platform.get\_cached\_value(“Employee”, employee, list(“payroll\_cost\_center”, “department”)).
    - If (not default\_cost\_center and department).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not default\_cost\_center → department.
      - Set default\_cost\_center from Platform.get\_cached\_value(“Department”, department, “payroll\_cost\_center”).
    - If not default\_cost\_center.
      - Set default\_cost\_center from self.cost\_center.
    - Set cost\_centers from mapping(default\_cost\_center → 100).
  - Evaluate self.employee\_cost\_centers.setdefault(employee, cost\_centers).
- Return self.employee\_cost\_centers.get(employee, mapping()).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Employee”, employee, list(“payroll\_cost\_center”, “department”)), Platform.get\_cached\_value(“Department”, department, “payroll\_cost\_center”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L5846) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L510) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L857)

<a id="op-b476b4815df073"></a>
### Payroll Entry.get account

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_account`

**Inputs** self, component\_dict = no value.

**Explicit results** account\_dict.

**Local steps**

- Set account\_dict from mapping().
- For each tuple(key, amount) in component\_dict.items().
  - Set tuple(component, cost\_center) from key.
  - Set account from self.get\_salary\_component\_account(component).
  - Set accounting\_key from tuple(account, cost\_center).
  - Set account\_dict at accounting\_key from (account\_dict.get(accounting\_key, 0) + amount).
- Return account\_dict.

**Methods declared on this owner** [get salary component account](operations-009.md#op-21727c2972e204).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0115.json#L6650) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L500) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L849)

<a id="op-13a10313c16032"></a>
### Payroll Entry.make accrual jv entry

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_make_accrual_journal_voucher_entry`

**Inputs** self, submitted\_salary\_slips.

**Record and data access** read “Payroll Settings” via get\_single\_value.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set employee\_wise\_accounting\_enabled from Platform.db.get\_single\_value(“Payroll Settings”, “process\_payroll\_accounting\_entry\_based\_on\_employee”).
- Set self.employee\_based\_payroll\_payable\_entries from mapping().
- Set self.\_advance\_deduction\_entries from list().
- Set earnings from (self.get\_salary\_component\_total(component\_type = “earnings”, employee\_wise\_accounting\_enabled = employee\_wise\_accounting\_enabled) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_salary\_component\_total(component\_type = “earnings”, employee\_wise\_accounting\_enabled = employee\_wise\_accounting\_enabled) → mapping().
- Set deductions from (self.get\_salary\_component\_total(component\_type = “deductions”, employee\_wise\_accounting\_enabled = employee\_wise\_accounting\_enabled) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_salary\_component\_total(component\_type = “deductions”, employee\_wise\_accounting\_enabled = employee\_wise\_accounting\_enabled) → mapping().
- Set employer\_contributions from (self.get\_salary\_components(“employer\_contributions”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_salary\_components(“employer\_contributions”) → list().
- Set precision from Platform.get\_precision(“Journal Entry Account”, “debit\_in\_account\_currency”).
- If (earnings or deductions).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in earnings → deductions.
  - Set accounts from list().
  - Set currencies from list().
  - Set payable\_amount from 0.
  - Set accounting\_dimensions from (get\_accounting\_dimensions() or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_accounting\_dimensions() → list().
  - Set company\_currency from Enterprise.get\_company\_currency(self.company).
  - Set payable\_amount from self.get\_payable\_amount\_for\_earnings\_and\_deductions(accounts, earnings, deductions, currencies, …).
  - Set payable\_amount from self.set\_accounting\_entries\_for\_advance\_deductions(accounts, currencies, company\_currency, accounting\_dimensions, …).
  - Evaluate self.set\_payable\_amount\_against\_payroll\_payable\_account(accounts, currencies, company\_currency, accounting\_dimensions, …).
  - Evaluate self.make\_journal\_entry(accounts, currencies, self.payroll\_payable\_account, voucher\_type = “Journal Entry”, user\_remark = translated “Accrual Journal Entry for salaries from {0} to {1}”.format(self.start\_d ….
- Evaluate self.make\_employer\_contribution\_jv\_entry(employer\_contributions, employee\_wise\_accounting\_enabled).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get salary component total](operations-009.md#op-b0cb9cdd9d66dd), [get salary components](operations-009.md#op-bd21865a3cce0b), [get payable amount for earnings and deductions](operations-009.md#op-c039498f1b63fc), [set accounting entries for advance deductions](operations-009.md#op-2666a9da36fc55), [set payable amount against payroll payable account](operations-009.md#op-db2aa6a1140aba), [make journal entry](operations-009.md#op-6ba51720ef32b4), [make employer contribution jv entry](operations-009.md#op-ad165b0d234b55).

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · configured or stored value from Platform.db.get\_single\_value(“Payroll Settings”, “process\_payroll\_accounting\_entry\_based\_on\_employee”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L99) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L519) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L866)

<a id="op-ad165b0d234b55"></a>
### Payroll Entry.make employer contribution jv entry

`operation_workforce_binding_workforce_payroll_doctype_payroll_entry_payroll_entry_payrollentry_make_employer_contribution_jv_entry`

**Inputs** self, employer\_contributions, employee\_wise\_accounting\_enabled = false.

**Explicit results** no value.

**Local steps**

- If not employer\_contributions.
  - Return no value.
- Set component\_accounts from self.get\_employer\_contribution\_accounts(set of item.salary\_component for item drawn from employer\_contributions).
  - Draw item from employer\_contributions.
- Set precision from Platform.get\_precision(“Journal Entry Account”, “debit\_in\_account\_currency”).
- Set expense\_entries from mapping().
- Set liability\_entries from mapping().
- For each item in employer\_contributions.
  - Set tuple(expense\_account, liability\_account) from component\_accounts at item.salary\_component.
  - Set item\_amount from flt(item.amount, precision).
  - Set employee\_cost\_centers from list(self.get\_payroll\_cost\_centers\_for\_employee(item.employee, item.salary\_structure).items()).
  - Set allocated from 0.
  - For each tuple(cost\_center, percentage) in employee\_cost\_centers at slice no value to negative 1.
    - Set split from flt(((item\_amount × percentage) ÷ 100), precision).
    - Update allocated using + split.
    - Set expense\_key from tuple(expense\_account, cost\_center).
    - Set expense\_entries at expense\_key from (expense\_entries.get(expense\_key, 0) + split).
  - Set last\_cost\_center from employee\_cost\_centers at negative 1 at 0.
  - Set expense\_key from tuple(expense\_account, last\_cost\_center).
  - Set expense\_entries at expense\_key from (expense\_entries.get(expense\_key, 0) + flt((item\_amount − allocated), precision)).
  - Set liability\_key from tuple(liability\_account, item.employee when employee\_wise\_accounting\_enabled, otherwise no value).
    - Value choice on employee\_wise\_accounting\_enabled — true gives item.employee, false gives no value.
  - Set liability\_entries at liability\_key from (liability\_entries.get(liability\_key, 0) + item\_amount).
- If not any(expense\_entries.values()).
  - Return no value.
- Set accounting\_dimensions from (get\_accounting\_dimensions() or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_accounting\_dimensions() → list().
- Set company\_currency from Enterprise.get\_company\_currency(self.company).
- Set accounts from list().
- Set currencies from list().
- For each tuple(tuple(account, cost\_center), amount) in expense\_entries.items().
  - Evaluate self.get\_accounting\_entries\_and\_payable\_amount(account, (cost\_center or self.cost\_center), amount, currencies, entry\_type = “debit”, accounts = accounts, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cost\_center → self.cost\_center.
- For each tuple(tuple(account, employee), amount) in liability\_entries.items().
  - Evaluate self.get\_accounting\_entries\_and\_payable\_amount(account, self.cost\_center, amount, currencies, entry\_type = “credit”, accounts = accounts, party = employee, reference\_type = self.doctype, …).
- Evaluate self.make\_journal\_entry(accounts, currencies, voucher\_type = “Journal Entry”, user\_remark = translated “Employer contribution accrual for salaries from {0} to {1}”.format(self.start\_date, self.end\_date), s ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get employer contribution accounts](operations-009.md#op-ae5d0a8944a66d), [get payroll cost centers for employee](operations-009.md#op-25d4d56bcb6d03), [get accounting entries and payable amount](operations-009.md#op-8c5f688824e697), [make journal entry](operations-009.md#op-6ba51720ef32b4).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L176) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L227) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L227)

<a id="op-ae5d0a8944a66d"></a>
### Payroll Entry.get employer contribution accounts

`operation_workforce_binding_workforce_payroll_doctype_payroll_entry_payroll_entry_payrollentry_get_employer_contribution_accounts`

**Inputs** self, salary\_components.

**Record and data access** read “Salary Component Account” via get\_all.

**Explicit results** component\_accounts.

**Explicit failure paths** validation helper — translated “Please set expense and liability accounts in Salary Component {0}”.format(get\_link\_to\_form(“Salary Component”, salary\_component)).

**Local steps**

- Set salary\_components from list(salary\_components).
- Set account\_details from Platform.get\_all(“Salary Component Account”, filters = mapping(“parenttype” → “Salary Component”, “parent” → list(“in”, salary\_components), “company” → self.company), fields = list(“parent”, “account”, “li ….
- Set component\_accounts from mapping of d.parent → tuple(d.account, d.liability\_account) for d drawn from account\_details.
  - Draw d from account\_details.
- For each salary\_component in salary\_components.
  - Set accounts from component\_accounts.get(salary\_component).
  - If (not accounts or not all(accounts)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not accounts → not all(accounts).
    - Call the validation error handler Platform.throw(translated “Please set expense and liability accounts in Salary Component {0}”.format(get\_link\_to\_form(“Salary Component”, salary\_component))).
- Return component\_accounts.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L175) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L226) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L226)

<a id="op-6ba51720ef32b4"></a>
### Payroll Entry.make journal entry

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_make_journal_entry`

**Inputs** self, accounts, currencies, payroll\_payable\_account = no value, voucher\_type = “Journal Entry”, user\_remark = empty text, submitted\_salary\_slips = no value, submit\_journal\_entry = false, employee\_wise\_accounting\_enabled = false, title = no value.

**Declared result** str.

**State and service calls** request new\_doc for “Journal Entry” · call save on journal\_entry · call submit on journal\_entry · msgprint with e.

**Explicit results** journal\_entry.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set multi\_currency from 0.
- If len(currencies) &gt; 1.
  - Set multi\_currency from 1.
- Set journal\_entry from Platform.new\_doc(“Journal Entry”).
- Set journal\_entry.voucher\_type from voucher\_type.
- Set journal\_entry.user\_remark from user\_remark.
- Set journal\_entry.company from self.company.
- Set journal\_entry.posting\_date from self.posting\_date.
- Set journal\_entry.party\_not\_required from true when not employee\_wise\_accounting\_enabled, otherwise false.
  - Value choice on not employee\_wise\_accounting\_enabled — true gives true, false gives false.
- Evaluate journal\_entry.set(“accounts”, accounts).
- Set journal\_entry.multi\_currency from multi\_currency.
- If voucher\_type equals “Journal Entry”.
  - Set journal\_entry.title from (title or payroll\_payable\_account).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → payroll\_payable\_account.
- Evaluate journal\_entry.save(ignore\_permissions = true).
- Attempt the following.
  - If submit\_journal\_entry.
    - Evaluate journal\_entry.submit().
  - If submitted\_salary\_slips.
    - Evaluate self.set\_journal\_entry\_in\_salary\_slips(submitted\_salary\_slips, jv\_name = journal\_entry.name).
- On failure (Exception) bound to e.
  - If type(e) belongs to tuple(str, list, tuple).
    - Evaluate Platform.msgprint(e).
  - Evaluate self.log\_error(“Journal Entry creation against Salary Slip failed”).
  - Propagate the active failure.
- Return journal\_entry.

**Methods declared on this owner** [set journal entry in salary slips](operations-010.md#op-e2284772e13630).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L100) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L522) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L869)

<a id="op-c039498f1b63fc"></a>
### Payroll Entry.get payable amount for earnings and deductions

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_payable_amount_for_earnings_and_deductions`

**Inputs** self, accounts, earnings, deductions, currencies, company\_currency, accounting\_dimensions, precision, payable\_amount, employee\_wise\_accounting\_enabled.

**Explicit results** payable\_amount.

**Local steps**

- For each tuple(acc\_cc, amount) in earnings.items().
  - Set payable\_amount from self.get\_accounting\_entries\_and\_payable\_amount(acc\_cc at 0, (acc\_cc at 1 or self.cost\_center), amount, currencies, entry\_type = “debit”, accounts = accounts, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in acc\_cc at 1 → self.cost\_center.
- For each tuple(acc\_cc, amount) in deductions.items().
  - Set payable\_amount from self.get\_accounting\_entries\_and\_payable\_amount(acc\_cc at 0, (acc\_cc at 1 or self.cost\_center), amount, currencies, entry\_type = “credit”, accounts = accounts, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in acc\_cc at 1 → self.cost\_center.
- Return payable\_amount.

**Methods declared on this owner** [get accounting entries and payable amount](operations-009.md#op-8c5f688824e697).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0116.json#L1420) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L509) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L856)

<a id="op-db2aa6a1140aba"></a>
### Payroll Entry.set payable amount against payroll payable account

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_set_payable_amount_against_payroll_payable_account`

**Inputs** self, accounts, currencies, company\_currency, accounting\_dimensions, precision, payable\_amount, payroll\_payable\_account, employee\_wise\_accounting\_enabled.

**Local steps**

- If employee\_wise\_accounting\_enabled.
  - For each tuple(employee, employee\_details) in self.employee\_based\_payroll\_payable\_entries.items().
    - Set payable\_amount from ((employee\_details.get(“earnings”, 0) or 0) − (employee\_details.get(“deductions”, 0) or 0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee\_details.get(“earnings”, 0) → 0.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee\_details.get(“deductions”, 0) → 0.
    - Set payable\_amount from self.get\_accounting\_entries\_and\_payable\_amount(payroll\_payable\_account, self.cost\_center, payable\_amount, currencies, entry\_type = “payable”, party = employee, accounts = accounts, …).
- Otherwise.
  - Set payable\_amount from self.get\_accounting\_entries\_and\_payable\_amount(payroll\_payable\_account, self.cost\_center, payable\_amount, currencies, entry\_type = “payable”, accounts = accounts, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get accounting entries and payable amount](operations-009.md#op-8c5f688824e697).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0116.json#L1817) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L532) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L879)

<a id="op-8c5f688824e697"></a>
### Payroll Entry.get accounting entries and payable amount

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_accounting_entries_and_payable_amount`

**Inputs** self, account, cost\_center, amount, currencies, company\_currency, payable\_amount, accounting\_dimensions, precision, entry\_type = “credit”, party = no value, accounts = no value, reference\_type = no value, reference\_name = no value, is\_advance = no value.

**Explicit results** payable\_amount.

**Local steps**

- Set tuple(exchange\_rate, amt) from self.get\_amount\_and\_exchange\_rate\_for\_journal\_entry(account, amount, company\_currency, currencies).
- Set row from mapping(“account” → account, “exchange\_rate” → flt(exchange\_rate), “cost\_center” → cost\_center, “project” → self.project).
- If entry\_type equals “debit”.
  - Update payable\_amount using + flt(amount, precision).
  - Evaluate row.update(mapping(“debit\_in\_account\_currency” → flt(amt, precision))).
- Otherwise.
  - If entry\_type equals “credit”.
    - Update payable\_amount using − flt(amount, precision).
    - Evaluate row.update(mapping(“credit\_in\_account\_currency” → flt(amt, precision))).
  - Otherwise.
    - Evaluate row.update(mapping(“credit\_in\_account\_currency” → flt(amt, precision), “reference\_type” → self.doctype, “reference\_name” → self.name)).
- If party.
  - Evaluate row.update(mapping(“party\_type” → “Employee”, “party” → party)).
- If reference\_type.
  - Evaluate row.update(mapping(“reference\_type” → reference\_type, “reference\_name” → reference\_name, “is\_advance” → is\_advance)).
- Evaluate self.update\_accounting\_dimensions(row, accounting\_dimensions).
- If amt.
  - Evaluate accounts.append(row).
- Return payable\_amount.

**Methods declared on this owner** [get amount and exchange rate for journal entry](operations-009.md#op-ea19f1b65907fc), [update accounting dimensions](operations-009.md#op-3f9fbc06041232).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0116.json#L2222) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L501) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L850)

<a id="op-3f9fbc06041232"></a>
### Payroll Entry.update accounting dimensions

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_update_accounting_dimensions`

**Inputs** self, row, accounting\_dimensions.

**Explicit results** row.

**Local steps**

- For each dimension in accounting\_dimensions.
  - Evaluate row.update(mapping(dimension → self.get(dimension))).
- Return row.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0116.json#L3057) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L537) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L884)

<a id="op-ea19f1b65907fc"></a>
### Payroll Entry.get amount and exchange rate for journal entry

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_amount_and_exchange_rate_for_journal_entry`

**Inputs** self, account, amount, company\_currency, currencies.

**Record and data access** read “Account” via get\_value.

**Explicit results** tuple(exchange\_rate, amount).

**Local steps**

- Set conversion\_rate from 1.
- Set exchange\_rate from self.exchange\_rate.
- Set account\_currency from Platform.db.get\_value(“Account”, account, “account\_currency”).
- If account\_currency does not belong to currencies.
  - Evaluate currencies.append(account\_currency).
- If company\_currency does not belong to currencies.
  - Evaluate currencies.append(company\_currency).
- If account\_currency equals company\_currency.
  - Set conversion\_rate from self.exchange\_rate.
  - Set exchange\_rate from 1.
- Set amount from (flt(amount) × flt(conversion\_rate)).
- Return tuple(exchange\_rate, amount).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0116.json#L3175) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L503) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L851)

<a id="op-e2f2399c464f0c"></a>
### Payroll Entry.has bank entries

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_has_bank_entries`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, bool).

**Explicit results** mapping(“has\_bank\_entries” → bool(bank\_entries), “has\_bank\_entries\_for\_withheld\_salaries” → not any(generator of employee.is\_salary\_withheld for employee drawn from self.employees)).

**Local steps**

- Set je from Platform.qb.DocType(“Journal Entry”).
- Set jea from Platform.qb.DocType(“Journal Entry Account”).
- Set bank\_entries from nested operand in the contract(nested operand in the contract).select(je.name).where((((nested operand in the contract equals nested operand in the contract bitwise or nested operand in the contract equals ….
- Return mapping(“has\_bank\_entries” → bool(bank\_entries), “has\_bank\_entries\_for\_withheld\_salaries” → not any(generator of employee.is\_salary\_withheld for employee drawn from self.employees)).
  - Draw employee from self.employees.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0116.json#L3516) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L518) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L865)

<a id="op-d61345de093ac4"></a>
### Payroll Entry.make bank entry

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_make_bank_entry`

**Inputs** self, for\_withheld\_salaries = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** (Document bitwise or no value).

**Record and data access** read “Payroll Settings” via get\_single\_value · read “Salary Component” via get\_value.

**Explicit results** bank\_entry.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set self.employee\_based\_payroll\_payable\_entries from mapping().
- Set employee\_wise\_accounting\_enabled from Platform.db.get\_single\_value(“Payroll Settings”, “process\_payroll\_accounting\_entry\_based\_on\_employee”).
- Set salary\_slip\_total from 0.
- Set salary\_details from self.get\_salary\_slip\_details(for\_withheld\_salaries).
- For each salary\_detail in salary\_details.
  - Set statistical\_component from Platform.db.get\_value(“Salary Component”, salary\_detail.salary\_component, “statistical\_component”, cache = true).
  - If not statistical\_component.
    - Set parent\_field from salary\_detail.parentfield.
    - If parent\_field belongs to tuple(“earnings”, “deductions”).
      - If employee\_wise\_accounting\_enabled.
        - Evaluate self.set\_employee\_based\_payroll\_payable\_entries(salary\_detail.parentfield, salary\_detail.employee, salary\_detail.amount, salary\_detail.salary\_structure).
      - If parent\_field equals “earnings”.
        - Update salary\_slip\_total using + salary\_detail.amount.
      - Otherwise.
        - If parent\_field equals “deductions”.
          - Update salary\_slip\_total using − salary\_detail.amount.
- Set total\_loan\_repayment from (self.process\_loan\_repayments\_for\_bank\_entry(salary\_details) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.process\_loan\_repayments\_for\_bank\_entry(salary\_details) → 0.
- Update salary\_slip\_total using − total\_loan\_repayment.
- Set bank\_entry from no value.
- If salary\_slip\_total &gt; 0.
  - Set remark from “withheld salaries” when for\_withheld\_salaries, otherwise “salaries”.
    - Value choice on for\_withheld\_salaries — true gives “withheld salaries”, false gives “salaries”.
  - Set bank\_entry from self.set\_accounting\_entries\_for\_bank\_entry(salary\_slip\_total, remark, employee\_wise\_accounting\_enabled).
  - If for\_withheld\_salaries.
    - Evaluate link\_bank\_entry\_in\_salary\_withholdings(salary\_details, bank\_entry.name).
- Return bank\_entry.

**Methods declared on this owner** [get salary slip details](operations-009.md#op-30d0a550a4a716), [set employee based payroll payable entries](operations-009.md#op-a24f505bc66216), [process loan repayments for bank entry](operations-009.md#op-cf6705e0674981), [set accounting entries for bank entry](operations-010.md#op-c6f0dccd81f7f0).

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · configured or stored value from Platform.db.get\_single\_value(“Payroll Settings”, “process\_payroll\_accounting\_entry\_based\_on\_employee”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0116.json#L3989) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L520) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L867)

<a id="op-30d0a550a4a716"></a>
### Payroll Entry.get salary slip details

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_get_salary_slip_details`

**Inputs** self, for\_withheld\_salaries = false.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set SalarySlip from Platform.qb.DocType(“Salary Slip”).
- Set SalaryDetail from Platform.qb.DocType(“Salary Detail”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(SalarySlip.name, SalarySlip.employee, SalarySlip.s ….
- If “lending” belongs to Platform.get\_installed\_apps().
  - Set query from query.select(SalarySlip.total\_loan\_repayment).
- If for\_withheld\_salaries.
  - Set query from query.where(SalarySlip.status equals “Withheld”).
- Otherwise.
  - Set query from query.where(SalarySlip.status differs from “Withheld”).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0116.json#L4721) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L515) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L862)

<a id="op-cf6705e0674981"></a>
### Payroll Entry.process loan repayments for bank entry

`operation_workforce_payroll_record_definitions_payroll_entry_business_behavior_payroll_entry_process_loan_repayments_for_bank_entry`

**Inputs** self, salary\_details.

**Wrappers, in declaration order** if\_lending\_app\_installed.

**Declared result** float.

**Explicit results** total\_loan\_repayment.

**Local steps**

- Set unique\_salary\_slips from mapping of row at “employee” → row for row drawn from salary\_details.values().
  - Draw row from salary\_details.
- Set total\_loan\_repayment from sum(generator of flt(slip.get(“total\_loan\_repayment”, 0)) for slip drawn from unique\_salary\_slips).
  - Draw slip from unique\_salary\_slips.
- If self.employee\_based\_payroll\_payable\_entries.
  - For each salary\_slip in unique\_salary\_slips.
    - If salary\_slip.get(“total\_loan\_repayment”).
      - Evaluate self.set\_employee\_based\_payroll\_payable\_entries(“total\_loan\_repayment”, salary\_slip.employee, salary\_slip.total\_loan\_repayment, salary\_slip.salary\_structure).
- Return total\_loan\_repayment.

**Methods declared on this owner** [set employee based payroll payable entries](operations-009.md#op-a24f505bc66216).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0116.json#L5383) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L527) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L874)
