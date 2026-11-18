# Employment and attendance · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Employee advance

[Record definition](../../../../data/record-types/employee_advance.json)

<a id="op-8f2f49f5756329"></a>
### Employee Advance.set pending amount

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_set_pending_amount`

**Inputs** self, update = false.

**State and service calls** call db\_set on self.

**Local steps**

- Set Advance from Platform.qb.DocType(“Employee Advance”).
- Set pending\_amount from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0 or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract(nested operand i … at 0 → 0.0.
- If update.
  - Evaluate self.db\_set(“pending\_amount”, pending\_amount).
- Otherwise.
  - Set self.pending\_amount from pending\_amount.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0016.json#L2089) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L484) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L465)

<a id="op-132d8f64a30394"></a>
### Employee Advance.check linked payment entry

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_employee_advance_check_linked_payment_entry`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value.

**Local steps**

- Bind dependencies remove\_ref\_doc\_link\_from\_pe, update\_accounting\_ledgers\_after\_reference\_removal.
- If Platform.db.get\_single\_value(“HR Settings”, “unlink\_payment\_on\_cancellation\_of\_employee\_advance”).
  - Evaluate remove\_ref\_doc\_link\_from\_pe(self.doctype, self.name).
  - Evaluate update\_accounting\_ledgers\_after\_reference\_removal(self.doctype, self.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “unlink\_payment\_on\_cancellation\_of\_employee\_advance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0016.json#L2466) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L479) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L460)

<a id="op-e44262f577cc71"></a>
### Create return through additional salary

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_create_return_through_additional_salary`

**Inputs** doc.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**State and service calls** request new\_doc for “Additional Salary”.

**Explicit results** additional\_salary.

**Local steps**

- Bind dependencies json.
- If isinstance(doc, str).
  - Set doc from Platform.\_dict(json.loads(doc)).
- Set additional\_salary from Platform.new\_doc(“Additional Salary”).
- Set additional\_salary.employee from doc.employee.
- Set additional\_salary.currency from doc.currency.
- Set additional\_salary.overwrite\_salary\_structure\_amount from 0.
- Set additional\_salary.amount from (doc.paid\_amount − doc.claimed\_amount).
- Set additional\_salary.company from doc.company.
- Set additional\_salary.ref\_doctype from doc.doctype.
- Set additional\_salary.ref\_docname from doc.name.
- Return additional\_salary.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0016.json#L2621) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L476) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L457)

<a id="op-278348a10ba17d"></a>
### Make return entry

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_make_return_entry`

**Inputs** employee, company, employee\_advance\_name, return\_amount, advance\_account, currency, mode\_of\_payment = no value, bank\_account = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Account” via get\_value.

**State and service calls** msgprint with translated “Couldn't automatically pick a Bank/Cash Account for this return. Please set one in the Accounting Entries be …”.format(get\_link\_to\_form(“Company”, (company + “#accounts\_tab”), translated “Company”)) · request new\_doc for “Journal Entry”.

**Explicit results** je.as\_dict().

**Local steps**

- Set bank\_cash\_account from get\_same\_currency\_bank\_cash\_account(company, currency, mode\_of\_payment, bank\_account).
- If not (bank\_cash\_account.get(“account”) or bank\_cash\_account.get(“name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bank\_cash\_account.get(“account”) → bank\_cash\_account.get(“name”).
  - Evaluate Platform.msgprint(translated “Couldn't automatically pick a Bank/Cash Account for this return. Please set one in the Accounting Entries be …”.format(get\_link\_to\_form(“Company”, (company + “#accounts\_tab”), ….
- Set advance\_account\_currency from Platform.db.get\_value(“Account”, advance\_account, “account\_currency”).
- Set je from Platform.new\_doc(“Journal Entry”).
- Set je.posting\_date from nowdate().
- Set je.voucher\_type from get\_voucher\_type(mode\_of\_payment).
- Set je.company from company.
- Set je.remark from (“Return against Employee Advance: ” + employee\_advance\_name).
- Set je.multi\_currency from 1 when advance\_account\_currency differs from Enterprise.get\_company\_currency(company), otherwise 0.
  - Value choice on advance\_account\_currency differs from Enterprise.get\_company\_currency(company) — true gives 1, false gives 0.
- Set advance\_account\_amount from flt(return\_amount).
- Evaluate je.append(“accounts”, mapping(“account” → advance\_account, “credit\_in\_account\_currency” → advance\_account\_amount, “account\_currency” → advance\_account\_currency, “reference\_type” → “Employee Advance”, …)).
- Set bank\_amount from flt(return\_amount).
- Evaluate je.append(“accounts”, mapping(“account” → (bank\_cash\_account.account or bank\_cash\_account.name), “debit\_in\_account\_currency” → bank\_amount, “account\_currency” → bank\_cash\_account.account\_currency, “account ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bank\_cash\_account.account → bank\_cash\_account.name.
- Return je.as\_dict().

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L18) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L494) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L475)

<a id="op-780e3dd78d6ea7"></a>
### Get same currency bank cash account

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_get_same_currency_bank_cash_account`

**Inputs** company, currency, mode\_of\_payment = no value, account = no value.

**Record and data access** read “Account” via get\_all · read “Account” via get\_cached\_value.

**Explicit results** get\_default\_bank\_cash\_account(company, account\_type = “Cash”, mode\_of\_payment = no value when account, otherwise mode\_of\_payment, account = account) · Platform.get\_cached\_value(“Account”, account, list(“name”, “account\_currency”, “account\_type”), as\_dict = true).

**Explicit failure paths** validation helper — translated “No Bank/Cash Account found for currency {0}. Please create one under company {1}.”.format(Platform.bold(currency), company).

**Local steps**

- Set company\_currency from Enterprise.get\_company\_currency(company).
- If currency equals company\_currency.
  - Return get\_default\_bank\_cash\_account(company, account\_type = “Cash”, mode\_of\_payment = no value when account, otherwise mode\_of\_payment, account = account).
    - Value choice on account — true gives no value, false gives mode\_of\_payment.
- If (not account and mode\_of\_payment).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not account → mode\_of\_payment.
  - Bind dependencies get\_bank\_cash\_account.
  - Set account from get\_bank\_cash\_account(mode\_of\_payment, company).get(“account”).
- If not account.
  - Set accounts from Platform.get\_all(“Account”, filters = mapping(“company” → company, “account\_currency” → currency, “account\_type” → list(“in”, list(“Cash”, “Bank”)), “is\_group” → 0), limit = 1).
  - If not accounts.
    - Call the validation error handler Platform.throw(translated “No Bank/Cash Account found for currency {0}. Please create one under company {1}.”.format(Platform.bold(currency), company), title = translated “Account Not Found”).
  - Set account from accounts at 0.name.
- Return Platform.get\_cached\_value(“Account”, account, list(“name”, “account\_currency”, “account\_type”), as\_dict = true).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account, list(“name”, “account\_currency”, “account\_type”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L17) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L492) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L473)

<a id="op-595390fcd7795a"></a>
### Get voucher type

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_get_voucher_type`

**Inputs** mode\_of\_payment = no value.

**Record and data access** read “Mode of Payment” via get\_cached\_value.

**Explicit results** voucher\_type.

**Local steps**

- Set voucher\_type from “Cash Entry”.
- If mode\_of\_payment.
  - Set mode\_of\_payment\_type from Platform.get\_cached\_value(“Mode of Payment”, mode\_of\_payment, “type”).
  - If mode\_of\_payment\_type equals “Bank”.
    - Set voucher\_type from “Bank Entry”.
- Return voucher\_type.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Mode of Payment”, mode\_of\_payment, “type”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0016.json#L4431) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L493) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L474)

<a id="op-35fa87104e4ca2"></a>
### Get employee advance return

`operation_workforce_human_resources_record_definitions_employee_advance_business_behavior_get_employee_advance_return`

**Inputs** employee\_advance.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Employee Advance” via get\_value.

**Explicit results** mapping(“total\_return\_scheduled” → pending\_scheduled, “has\_return\_scheduled” → bool(pending\_scheduled)).

**Local steps**

- Evaluate Platform.has\_permission(“Employee Advance”, ptype = “read”, doc = employee\_advance, throw = true).
- Set AdditionalSalary from Platform.qb.DocType(“Additional Salary”).
- Set return\_entries from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“total\_return\_scheduled”)).where(((nested operand in the contract.ref\_doctype equals “Employee Advan ….
- Set total\_return\_scheduled from flt(return\_entries at 0.total\_return\_scheduled).
- Set already\_returned from flt(Platform.db.get\_value(“Employee Advance”, employee\_advance, “return\_amount”)).
- Set pending\_scheduled from max(0, (total\_return\_scheduled − already\_returned)).
- Return mapping(“total\_return\_scheduled” → pending\_scheduled, “has\_return\_scheduled” → bool(pending\_scheduled)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee Advance”, ptype = “read”, doc = employee\_advance, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0016.json#L4582) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L491) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L472)

<a id="op-31b0deeb716c98"></a>
### Get data

`operation_workforce_human_resources_record_definitions_employee_advance_employee_advance_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “employee\_advance”, “non\_standard\_fieldnames” → mapping(“Payment Entry” → “reference\_name”, “Journal Entry” → “reference\_name”), “transactions” → list(mapping(“items” → list(“Expense  ….

**Local steps**

- Return mapping(“fieldname” → “employee\_advance”, “non\_standard\_fieldnames” → mapping(“Payment Entry” → “reference\_name”, “Journal Entry” → “reference\_name”), “transactions” → list(mapping(“items” → list(“Expense  ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0016.json#L5105) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L495) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L476)

## Report · Employee advance summary

<a id="op-040d04910aebf0"></a>
### Execute

`operation_workforce_human_resources_report_employee_advance_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, advances\_list) · tuple(columns, result, no value, no value, …).

**Local steps**

- If not filters.
  - Set filters from Platform.\_dict().
- Set filters from Platform.\_dict(filters).
- Set advances\_list from get\_advances(filters).
- Set columns from get\_columns().
- If not advances\_list.
  - Evaluate msgprint(translated “No record found”).
  - Return tuple(columns, advances\_list).
- Set grouped from OrderedDict().
- Set group\_totals from OrderedDict().
- Set group\_labels from OrderedDict().
- For each advance in advances\_list.
  - Set advance.outstanding\_amount from (advance.paid\_amount − (advance.claimed\_amount + advance.return\_amount)).
  - Set advance.department from (advance.department or advance.employee\_department).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in advance.department → advance.employee\_department.
  - If filters.get(“group\_by”).
    - Set group\_key from advance.get(scrub(filters.get(“group\_by”))).
    - Evaluate grouped.setdefault(group\_key, list()).append(advance).
    - If group\_key does not belong to group\_totals.
      - Set group\_labels at group\_key from (formatted text {advance.employee}: {advance.employee\_name} when (filters.get(“group\_by”) equals “Employee” and advance.employee\_name), otherwise group\_key or group\_key).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in formatted text {advance.employee}: {advance.employee\_name} when (filters.get(“group\_by”) equals “Employee” and advance.employee\_name), otherwise group\_key → group\_key.
        - Value choice on (filters.get(“group\_by”) equals “Employee” and advance.employee\_name) — true gives formatted text {advance.employee}: {advance.employee\_name}, false gives group\_key.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“group\_by”) equals “Employee” → advance.employee\_name.
      - Set group\_totals at group\_key from Platform.\_dict(advance\_amount = 0, paid\_amount = 0, claimed\_amount = 0, return\_amount = 0, …).
    - Update group\_totals at group\_key.advance\_amount using + (advance.advance\_amount or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in advance.advance\_amount → 0.
    - Update group\_totals at group\_key.paid\_amount using + (advance.paid\_amount or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in advance.paid\_amount → 0.
    - Update group\_totals at group\_key.claimed\_amount using + (advance.claimed\_amount or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in advance.claimed\_amount → 0.
    - Update group\_totals at group\_key.return\_amount using + (advance.return\_amount or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in advance.return\_amount → 0.
    - Update group\_totals at group\_key.outstanding\_amount using + advance.outstanding\_amount.
- If not filters.get(“group\_by”).
  - For each row in advances\_list.
    - Set row.title from row.name.
    - Set row.outstanding\_amount from (row.paid\_amount − (row.claimed\_amount + row.return\_amount)).
    - Set row.department from (row.department or row.employee\_department).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.department → row.employee\_department.
    - If row.employee\_name.
      - Set row.employee from formatted text {row.employee}: {row.employee\_name}.
  - Return tuple(columns, advances\_list).
- Set result from list().
- Set grand\_total from Platform.\_dict(advance\_amount = 0, paid\_amount = 0, claimed\_amount = 0, return\_amount = 0, …).
- Set first\_currency from no value.
- For each tuple(key, rows) in grouped.items().
  - Set totals from group\_totals at key.
  - If not first\_currency.
    - Set first\_currency from totals.currency.
  - Update grand\_total.advance\_amount using + totals.advance\_amount.
  - Update grand\_total.paid\_amount using + totals.paid\_amount.
  - Update grand\_total.claimed\_amount using + totals.claimed\_amount.
  - Update grand\_total.return\_amount using + totals.return\_amount.
  - Update grand\_total.outstanding\_amount using + totals.outstanding\_amount.
  - Evaluate result.append(Platform.\_dict(title = (group\_labels.get(key) or translated “Not Set”), advance\_amount = totals.advance\_amount, paid\_amount = totals.paid\_amount, claimed\_amount = totals.claimed\_amount, …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in group\_labels.get(key) → translated “Not Set”.
  - For each row in rows.
    - Evaluate result.append(Platform.\_dict(title = row.name, employee = formatted text {row.employee}: {row.employee\_name} when row.employee\_name, otherwise row.employee, advance\_account = row.advance\_account, departmen ….
      - Value choice on row.employee\_name — true gives formatted text {row.employee}: {row.employee\_name}, false gives row.employee.
- Evaluate result.append(Platform.\_dict(title = translated “Total”, advance\_amount = grand\_total.advance\_amount, paid\_amount = grand\_total.paid\_amount, claimed\_amount = grand\_total.claimed\_amount, …)).
- Return tuple(columns, result, no value, no value, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0080.json#L2182) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1660) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L266)

<a id="op-80b850d91c38be"></a>
### Get columns

`operation_workforce_human_resources_report_employee_advance_summary_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Title”, “fieldname” → “title”, “fieldtype” → “Link”, “options” → “Employee Advance”, …), mapping(“label” → translated “Employee”, “fieldname” → “employee”, “fieldtype” →  ….

**Local steps**

- Return list(mapping(“label” → translated “Title”, “fieldname” → “title”, “fieldtype” → “Link”, “options” → “Employee Advance”, …), mapping(“label” → translated “Employee”, “fieldname” → “employee”, “fieldtype” →  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0080.json#L4239) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1662) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L268)

<a id="op-67b274974f22c5"></a>
### Get advances

`operation_workforce_human_resources_report_employee_advance_summary_business_behavior_get_advances`

**Inputs** filters.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set EmployeeAdvance from Platform.qb.DocType(“Employee Advance”).
- Set Employee from Platform.qb.DocType(“Employee”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.employee equals nested operand in the contract.name).select(EmployeeAdvance.name, EmployeeAdvance.employee,  ….
- If filters.get(“employee”).
  - Set query from query.where(EmployeeAdvance.employee equals filters.get(“employee”)).
- If filters.get(“company”).
  - Set query from query.where(EmployeeAdvance.company equals filters.get(“company”)).
- If filters.get(“status”).
  - Set query from query.where(EmployeeAdvance.status equals filters.get(“status”)).
- If filters.get(“from\_date”).
  - Set query from query.where(EmployeeAdvance.posting\_date ≥ filters.get(“from\_date”)).
- If filters.get(“to\_date”).
  - Set query from query.where(EmployeeAdvance.posting\_date ≤ filters.get(“to\_date”)).
- If filters.get(“department”).
  - Set query from query.where((EmployeeAdvance.department.isin(filters.get(“department”)) bitwise or (EmployeeAdvance.department.isnull() bitwise and Employee.department.isin(filters.get(“department”))))).
- If filters.get(“branch”).
  - Set query from query.where(Employee.branch.isin(filters.get(“branch”))).
- If filters.get(“advance\_account”).
  - Set query from query.where(EmployeeAdvance.advance\_account.isin(filters.get(“advance\_account”))).
- If filters.get(“group\_by”) equals “Department”.
  - Set query from query.orderby(EmployeeAdvance.department).
- Otherwise.
  - If filters.get(“group\_by”) equals “Branch”.
    - Set query from query.orderby(Employee.branch).
  - Otherwise.
    - Set query from query.orderby(EmployeeAdvance.employee).
- Set query from query.orderby(EmployeeAdvance.posting\_date, order = Order.desc).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0080.json#L5786) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1661) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L267)

## Report · Employee analytics

<a id="op-72e3b043d19690"></a>
### Execute

`operation_workforce_human_resources_report_employee_analytics_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, employees, no value, chart).

**Explicit failure paths** validation helper — translated “{0} is mandatory”.format(translated “Company”).

**Local steps**

- If not filters.
  - Set filters from mapping().
- If not filters at “company”.
  - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(translated “Company”)).
- Set columns from get\_columns().
- Set employees from get\_employees(filters).
- Set parameters from get\_parameters(filters).
- Set chart from get\_chart\_data(parameters, filters).
- Return tuple(columns, employees, no value, chart).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0081.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1663) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L269)

<a id="op-fec2acb32dc011"></a>
### Get columns

`operation_workforce_human_resources_report_employee_analytics_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list((translated “Employee” + “:Link/Employee:120”), (translated “Name” + “:Data:200”), (translated “Date of Birth” + “:Date:100”), (translated “Branch” + “:Link/Branch:120”), …).

**Local steps**

- Return list((translated “Employee” + “:Link/Employee:120”), (translated “Name” + “:Data:200”), (translated “Date of Birth” + “:Date:100”), (translated “Branch” + “:Link/Branch:120”), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0081.json#L297) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1665) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L271)

<a id="op-91c4258e213d95"></a>
### Get employees

`operation_workforce_human_resources_report_employee_analytics_business_behavior_get_employees`

**Inputs** filters.

**Record and data access** read “Employee” via get\_list.

**Explicit results** Platform.get\_list(“Employee”, filters = filters\_for\_employees, fields = list(“name”, “employee\_name”, “date\_of\_birth”, “branch”, …), as\_list = true).

**Local steps**

- Set filters\_for\_employees from Platform.\_dict((deepcopy(filters) or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in deepcopy(filters) → mapping().
- Set filters\_for\_employees at “status” from “Active”.
- Set filters\_for\_employees at nested operand in the contract.get(“parameter”).lower().replace(one space, “\_”) from list(“is”, “set”).
- Evaluate filters\_for\_employees.pop(“parameter”).
- Return Platform.get\_list(“Employee”, filters = filters\_for\_employees, fields = list(“name”, “employee\_name”, “date\_of\_birth”, “branch”, …), as\_list = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0081.json#L559) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1666) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L272)

<a id="op-fb4aa744a2f9f1"></a>
### Get parameters

`operation_workforce_human_resources_report_employee_analytics_business_behavior_get_parameters`

**Inputs** filters.

**Record and data access** read parameter via get\_all.

**Explicit results** Platform.get\_all(parameter, pluck = “name”).

**Local steps**

- If filters.get(“parameter”) equals “Grade”.
  - Set parameter from “Employee Grade”.
- Otherwise.
  - Set parameter from filters.get(“parameter”).
- Return Platform.get\_all(parameter, pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0081.json#L907) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1667) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L273)

<a id="op-83687eba8d58b2"></a>
### Get chart data

`operation_workforce_human_resources_report_employee_analytics_business_behavior_get_chart_data`

**Inputs** parameters, filters.

**Record and data access** read “Employee” via count.

**Explicit results** chart.

**Local steps**

- If not parameters.
  - Set parameters from list().
- Set datasets from list().
- Set parameter\_field\_name from filters.get(“parameter”).lower().replace(one space, “\_”).
- Set label from list().
- Set employee from Platform.qb.DocType(“Employee”).
- For each parameter in parameters.
  - If parameter.
    - Set total\_employee from nested operand in the contract(nested operand in the contract).where(nested operand in the contract at nested operand in the contract equals parameter).where(Criterion.all(build\_qb\_match\_conditions(“Employ ….
    - If total\_employee at 0 at 0.
      - Evaluate label.append(parameter).
    - Evaluate datasets.append(total\_employee at 0 at 0).
- Set values from list of value for value drawn from datasets where value differs from 0.
  - Draw value from datasets, keep a combination only if (value differs from 0).
- Set total\_employee from Platform.db.count(“Employee”, mapping(“status” → “Active”, “company” → filters.get(“company”))).
- Set others from (total\_employee − sum(values)).
- Evaluate label.append(“Not Set”).
- Evaluate values.append(others).
- Set chart from mapping(“data” → mapping(“labels” → label, “datasets” → list(mapping(“name” → “Employees”, “values” → values)))).
- Set chart at “type” from “donut”.
- Return chart.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0081.json#L1074) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1664) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L270)

## Record · Employee attendance tool

[Record definition](../../../../data/record-types/employee_attendance_tool.json)

<a id="op-57fb007cedf9e2"></a>
### Employee Attendance Tool.save

`operation_workforce_human_resources_record_definitions_employee_attendance_tool_business_behavior_employee_attendance_tool_save`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Return no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0018.json#L1557) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L527) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L508)

<a id="op-e15b8cbdbdaff2"></a>
### Employee Attendance Tool.get list

`operation_workforce_human_resources_record_definitions_employee_attendance_tool_business_behavior_employee_attendance_tool_get_list`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0018.json#L1593) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L525) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L506)

<a id="op-773c37e36d2188"></a>
### Employee Attendance Tool.get count

`operation_workforce_human_resources_record_definitions_employee_attendance_tool_business_behavior_employee_attendance_tool_get_count`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0018.json#L1623) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L524) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L505)

<a id="op-eedc9379dcdada"></a>
### Employee Attendance Tool.get stats

`operation_workforce_human_resources_record_definitions_employee_attendance_tool_business_behavior_employee_attendance_tool_get_stats`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0018.json#L1653) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L526) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L507)

<a id="op-83231b2e1b8eb8"></a>
### Employee Attendance Tool.db insert

`operation_workforce_human_resources_record_definitions_employee_attendance_tool_business_behavior_employee_attendance_tool_database_insert`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0018.json#L1683) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L521) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L502)

<a id="op-c875402054bed5"></a>
### Employee Attendance Tool.db update

`operation_workforce_human_resources_record_definitions_employee_attendance_tool_business_behavior_employee_attendance_tool_database_update`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0018.json#L1716) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L522) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L503)

<a id="op-358d43b0b2d6dc"></a>
### Employee Attendance Tool.delete

`operation_workforce_human_resources_record_definitions_employee_attendance_tool_business_behavior_employee_attendance_tool_delete`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0018.json#L1749) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L523) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L504)

<a id="op-4f36616a1750b1"></a>
### Get employees

`operation_workforce_human_resources_record_definitions_employee_attendance_tool_business_behavior_get_employees`

**Inputs** date, department = no value, branch = no value, company = no value, employment\_type = no value, designation = no value, employee\_grade = no value, shift = no value, filter\_by\_shift = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, list).

**Record and data access** read “Employee” via get\_list · read “Attendance” via get\_list.

**Explicit results** mapping(“marked” → attendance\_list, “half\_day\_marked” → half\_day\_attendance\_list, “unmarked” → unmarked\_attendance).

**Local steps**

- Set filters from mapping(“status” → “Active”, “date\_of\_joining” → list(“&lt;=”, date)).
- For each tuple(field, value) in mapping(“department” → department, “branch” → branch, “company” → company, “employment\_type” → employment\_type, …).items().
  - If value.
    - Set filters at field from value.
- Set employee\_list from Platform.get\_list(“Employee”, fields = list(“employee”, “employee\_name”), filters = filters, order\_by = “employee\_name”).
- Set attendance\_list from Platform.get\_list(“Attendance”, fields = list(“employee”, “employee\_name”, “status”, “shift”, …), filters = mapping(“attendance\_date” → date, “docstatus” → 1, “modify\_half\_day\_status” → 0), order\_by = “emp ….
- Set half\_day\_attendance\_list from Platform.get\_list(“Attendance”, fields = list(“employee”, “employee\_name”), filters = mapping(“attendance\_date” → date, “docstatus” → 1, “modify\_half\_day\_status” → 1, “leave\_type” → tuple(“is”, “set”)), or ….
- Set unmarked\_attendance from \_get\_unmarked\_attendance(employee\_list, list(expanded attendance\_list, expanded half\_day\_attendance\_list)).
- If filter\_by\_shift.
  - Set unmarked\_attendance from \_get\_unmarked\_attendance\_with\_shift(unmarked\_attendance, shift, date).
- Return mapping(“marked” → attendance\_list, “half\_day\_marked” → half\_day\_attendance\_list, “unmarked” → unmarked\_attendance).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0018.json#L1782) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L528) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L509)
