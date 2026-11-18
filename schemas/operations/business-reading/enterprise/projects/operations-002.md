# Projects and time · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Project

[Record definition](../../../../data/record-types/project.json)

<a id="op-d7d1bcbc8ad8c4"></a>
### Project Accounts.monthly

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_monthly`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** rows.

**Local steps**

- Set last from min(getdate(), getdate(self.fiscal\_year.year\_end\_date)).
- Set months from month\_range(str(self.fiscal\_year.year\_start\_date) at slice no value to 7, str(last) at slice no value to 7).
- Set expense from set of account.name for account drawn from self.accounts where account.root\_type equals “Expense”.
  - Draw account from self.accounts, keep a combination only if (account.root\_type equals “Expense”).
- If self.budgets.
  - Update expense using bitwise and set(self.budgets).
- Set tuple(actual, budget, rows) from tuple(0.0, 0.0, list()).
- For each month in months.
  - Update actual using + sum(generator of self.ledger\_by\_month.get(tuple(account, month), 0) for account drawn from expense).
    - Draw account from expense.
  - Update budget using + sum(generator of nested operand in the contract.budgets at account at “by\_month”.get(month, 0) for account drawn from (expense bitwise and set(self.budgets))).
    - Draw account from (expense bitwise and set(self.budgets)).
  - Evaluate rows.append(mapping(“month” → month, “actual” → actual, “budget” → budget when self.budgets, otherwise no value)).
    - Value choice on self.budgets — true gives budget, false gives no value.
- Return rows.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L171) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1181)

<a id="op-f2cb7a00a6ec9e"></a>
### Project Accounts.accounts

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_accounts`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** list at Platform.\_dict.

**Record and data access** read “Account” via get\_list.

**Explicit results** Platform.get\_list(“Account”, filters = mapping(“name” → list(“in”, list(names)), “report\_type” → “Profit and Loss”), fields = list(“name”, “account\_name”, “root\_type”), order\_by = “root\_type desc, account\_name”).

**Local steps**

- Set names from (((set(self.ledger\_totals) bitwise or set(self.budgets)) bitwise or set(self.ordered)) bitwise or set(self.requested)).
- Evaluate names.discard(no value).
- Return Platform.get\_list(“Account”, filters = mapping(“name” → list(“in”, list(names)), “report\_type” → “Profit and Loss”), fields = list(“name”, “account\_name”, “root\_type”), order\_by = “root\_type desc, account\_name”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L160) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1170)

<a id="op-9e73af41a61578"></a>
### Project Accounts.ledger totals

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_ledger_totals`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** dict at tuple(str, dict).

**Explicit results** totals.

**Local steps**

- Set totals from mapping().
- For each row in self.ledger\_rows.
  - Set total from totals.setdefault(row.account, mapping(“balance” → 0.0, “entries” → 0)).
  - Update total at “balance” using + flt(row.amount).
  - Update total at “entries” using + row.entries.
- Return totals.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L170) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1180)

<a id="op-2f821e2cf8603a"></a>
### Project Accounts.ledger by month

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_ledger_by_month`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** dict at tuple(tuple at tuple(str, str), float).

**Explicit results** mapping of tuple(row.account, formatted text {int(row.year)}-{int(row.month)}) → flt(row.amount) for row drawn from self.ledger\_rows.

**Local steps**

- Return mapping of tuple(row.account, formatted text {int(row.year)}-{int(row.month)}) → flt(row.amount) for row drawn from self.ledger\_rows.
  - Draw row from self.ledger\_rows.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L167) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1177)

<a id="op-5238c46d6ae1e9"></a>
### Project Accounts.ledger rows

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_ledger_rows`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** list at Platform.\_dict.

**Explicit results** nested operand in the contract().select(gle.account, nested operand in the contract.as\_(“year”), nested operand in the contract.as\_(“month”), nested operand in the contract.as\_(“amount”), …).groupby(gle.ac ….

**Local steps**

- Set gle from qb.DocType(“GL Entry”).
- Set tuple(year, month) from tuple(Extract(DatePart.year, gle.posting\_date), Extract(DatePart.month, gle.posting\_date)).
- Return nested operand in the contract().select(gle.account, nested operand in the contract.as\_(“year”), nested operand in the contract.as\_(“month”), nested operand in the contract.as\_(“amount”), …).groupby(gle.ac ….

**Methods declared on this owner** [ledger query](operations-002.md#op-65a043d2ce5f81).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L169) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1179)

<a id="op-6b54ba41eaf716"></a>
### Project Accounts.budget spend

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_budget_spend`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** dict at tuple(str, dict at tuple(str, float)).

**Explicit results** mapping() · mapping of row.account → mapping(“spent” → flt(row.spent), “spent\_to\_date” → flt(row.spent\_to\_date)) for row drawn from rows.

**Local steps**

- If not self.budgets.
  - Return mapping().
- Set gle from qb.DocType(“GL Entry”).
- Set amount from (gle.debit − gle.credit).
- Set periods from Criterion.any(list of (gle.account equals account bitwise and gle.posting\_date at slice budget at “budget\_start\_date” to budget at “budget\_end\_date”) for tuple(account, budget) drawn from self.budgets.items()).
  - Draw tuple(account, budget) from self.budgets.items().
- Set to\_date from Case().when(gle.posting\_date ≤ get\_last\_day(getdate()), amount).else\_(0).
- Set rows from nested operand in the contract(nested operand in the contract).select(gle.account, nested operand in the contract.as\_(“spent”), nested operand in the contract.as\_(“spent\_to\_date”)).groupby(gle.account).run ….
- Return mapping of row.account → mapping(“spent” → flt(row.spent), “spent\_to\_date” → flt(row.spent\_to\_date)) for row drawn from rows.
  - Draw row from rows.

**Methods declared on this owner** [readable ledger](operations-002.md#op-61f86dfb07548f).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L161) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1171)

<a id="op-65a043d2ce5f81"></a>
### Project Accounts.ledger query

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_ledger_query`

**Inputs** self.

**Explicit results** self.readable\_ledger().where(gle.posting\_date at slice self.fiscal\_year.year\_start\_date to self.fiscal\_year.year\_end\_date).

**Local steps**

- Set gle from qb.DocType(“GL Entry”).
- Return self.readable\_ledger().where(gle.posting\_date at slice self.fiscal\_year.year\_start\_date to self.fiscal\_year.year\_end\_date).

**Methods declared on this owner** [readable ledger](operations-002.md#op-61f86dfb07548f).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L168) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1178)

<a id="op-61f86dfb07548f"></a>
### Project Accounts.readable ledger

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_readable_ledger`

**Inputs** self.

**Explicit results** nested operand in the contract(nested operand in the contract).where(nested operand in the contract.project equals nested operand in the contract.name).where(gle.company equals self.project.company).where( ….

**Local steps**

- Set gle from qb.DocType(“GL Entry”).
- Set readable from Platform.qb.get\_query(“GL Entry”, fields = list(“name”), filters = mapping(“project” → self.project.name), ignore\_permissions = false).
- Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.project equals nested operand in the contract.name).where(gle.company equals self.project.company).where( ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L174) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1184)

<a id="op-8e04b45dcfa7e6"></a>
### Project Accounts.budgets

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_budgets`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** dict at tuple(str, dict).

**Record and data access** read “Budget” via get\_list.

**Explicit results** mapping() · mapping of budget.account → mapping(expand budget, “by\_month” → by\_month.get(budget.name, mapping())) for budget drawn from budgets.

**Local steps**

- If not self.can\_read\_budgets.
  - Return mapping().
- Set today from getdate().
- Set budgets from Platform.get\_list(“Budget”, filters = mapping(“budget\_against” → “Project”, “project” → self.project.name, “company” → self.project.company, “docstatus” → 1, …), fields = BUDGET\_FIELDS).
- Set by\_month from self.distribution\_by\_month(list of budget.name for budget drawn from budgets).
  - Draw budget from budgets.
- Return mapping of budget.account → mapping(expand budget, “by\_month” → by\_month.get(budget.name, mapping())) for budget drawn from budgets.
  - Draw budget from budgets.

**Methods declared on this owner** [distribution by month](operations-002.md#op-d6a0083211e17c).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L162) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1172)

<a id="op-d6a0083211e17c"></a>
### Project Accounts.distribution by month

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_distribution_by_month`

**Inputs** self, budgets.

**Declared result** dict at tuple(str, dict at tuple(str, float)).

**Record and data access** read “Budget Distribution” via get\_all.

**Explicit results** by\_month.

**Local steps**

- Set rows from Platform.get\_all(“Budget Distribution”, filters = mapping(“parenttype” → “Budget”, “parent” → list(“in”, budgets)), fields = list(“parent”, “start\_date”, “amount”)).
- Set by\_month from mapping().
- For each row in rows.
  - Set months from by\_month.setdefault(row.parent, mapping()).
  - Set month from str(row.start\_date) at slice no value to 7.
  - Set months at month from (months.get(month, 0) + flt(row.amount)).
- Return by\_month.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L165) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1175)

<a id="op-d4d825b3271301"></a>
### Project Billing.initialize

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_billing_projectbilling_init`

**Inputs** self, project, access.

**Local steps**

- Set self.project from project.
- Set self.queries from ProjectCostQueries(project).
- Set self.access from access.
- Set self.item\_billed\_invoices from set().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L179) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1189)

<a id="op-98a147d3261e0d"></a>
### Project Billing.build

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_billing_projectbilling_build`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“sales\_orders” → (orders and orders at slice no value to LIST\_LIMIT), “sales\_order\_count” → len(orders) when orders is distinct from no value, otherwise no value, “invoices” → (invoices and invoice ….

**Local steps**

- Set orders from self.sales\_orders().
- Set invoices from self.invoices().
- Return mapping(“sales\_orders” → (orders and orders at slice no value to LIST\_LIMIT), “sales\_order\_count” → len(orders) when orders is distinct from no value, otherwise no value, “invoices” → (invoices and invoice ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in orders → orders at slice no value to LIST\_LIMIT.
  - Value choice on orders is distinct from no value — true gives len(orders), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in invoices → invoices at slice no value to LIST\_LIMIT.
  - Value choice on invoices is distinct from no value — true gives len(invoices), false gives no value.
  - Value choice on invoices — true gives self.invoice\_filter(invoices), false gives no value.

**Methods declared on this owner** [sales orders](operations-002.md#op-1c21ad4270eef4), [invoices](operations-002.md#op-4620065c4f61ee), [invoice filter](operations-002.md#op-efdfd1d167aa39).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L178) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1188)

<a id="op-1c21ad4270eef4"></a>
### Project Billing.sales orders

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_billing_projectbilling_sales_orders`

**Inputs** self.

**Declared result** (list at dict bitwise or no value).

**Record and data access** read “Sales Order” via get\_list.

**Explicit results** no value · Platform.get\_list(“Sales Order”, filters = mapping(“project” → self.project, “docstatus” → 1), fields = list(“name”, “transaction\_date”, “status”, “base\_net\_total”, …), order\_by = “transaction\_date desc”).

**Local steps**

- If not self.access at “sales\_orders”.
  - Return no value.
- Return Platform.get\_list(“Sales Order”, filters = mapping(“project” → self.project, “docstatus” → 1), fields = list(“name”, “transaction\_date”, “status”, “base\_net\_total”, …), order\_by = “transaction\_date desc”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1192)

<a id="op-4620065c4f61ee"></a>
### Project Billing.invoices

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_billing_projectbilling_invoices`

**Inputs** self, start = 0, page\_length = no value.

**Declared result** (list at dict bitwise or no value).

**Record and data access** read “Sales Invoice” via get\_list.

**Explicit results** no value · list() · list of mapping(expand invoice, “amount” → amounts at invoice.name) for invoice drawn from invoices.

**Local steps**

- If not self.access at “invoices”.
  - Return no value.
- Set amounts from self.billed\_by\_invoice().
- If not amounts.
  - Return list().
- Set invoices from Platform.get\_list(“Sales Invoice”, filters = mapping(“name” → list(“in”, list(amounts))), fields = list(“name”, “posting\_date”, “status”, “project”), order\_by = “posting\_date desc, name desc”, offset = start, …).
- Return list of mapping(expand invoice, “amount” → amounts at invoice.name) for invoice drawn from invoices.
  - Draw invoice from invoices.

**Methods declared on this owner** [billed by invoice](operations-002.md#op-7e4ab74dad42f6).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1191)

<a id="op-efdfd1d167aa39"></a>
### Project Billing.invoice filter

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_billing_projectbilling_invoice_filter`

**Inputs** self, invoices.

**Declared result** (dict bitwise or no value).

**Explicit results** mapping(“project” → self.project) · mapping(“Sales Invoice Item.project” → self.project) · no value.

**Local steps**

- If all(generator of invoice at “project” equals self.project for invoice drawn from invoices).
  - Draw invoice from invoices.
  - Return mapping(“project” → self.project).
- If set of invoice at “name” for invoice drawn from invoices ≤ self.item\_billed\_invoices.
  - Draw invoice from invoices.
  - Return mapping(“Sales Invoice Item.project” → self.project).
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L180) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1190)

<a id="op-7e4ab74dad42f6"></a>
### Project Billing.billed by invoice

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_billing_projectbilling_billed_by_invoice`

**Inputs** self.

**Declared result** dict at tuple(str, float).

**Explicit results** combine(sum\_by(from\_invoice, invoice.name, item.base\_net\_amount), from\_items).

**Local steps**

- Set invoice from qb.DocType(“Sales Invoice”).
- Set item from qb.DocType(“Sales Invoice Item”).
- Set tuple(from\_invoice, from\_item) from self.queries.billed\_items().
- Set from\_items from sum\_by(from\_item, invoice.name, item.base\_net\_amount).
- Set self.item\_billed\_invoices from set(from\_items).
- Return combine(sum\_by(from\_invoice, invoice.name, item.base\_net\_amount), from\_items).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L177) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1187)

<a id="op-cab43c897e9a2a"></a>
### Budget summary

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_budgets_budget_summary`

**Inputs** budget, spend.

**Declared result** dict.

**Explicit results** mapping(“amount” → amount, “control” → control, “rule” → rule\_label(control), “spent” → spend at “spent”, …).

**Local steps**

- Set control from budget\_control(budget).
- Set amount from flt(budget at “budget\_amount”).
- Return mapping(“amount” → amount, “control” → control, “rule” → rule\_label(control), “spent” → spend at “spent”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L185) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1195)

<a id="op-087cf8489df2ff"></a>
### Rule label

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_budgets_rule_label`

**Inputs** control.

**Declared result** str.

**Explicit results** translated “Tracks only” · labels at tuple(control at “action”, control at “stage”).

**Local steps**

- If not control.
  - Return translated “Tracks only”.
- Set labels from mapping(tuple(“Stop”, “Purchase Order”) → translated “Stops on orders”, tuple(“Stop”, “Material Request”) → translated “Stops on requests”, tuple(“Stop”, “Expense”) → translated “Stops on expenses”, tuple( ….
- Return labels at tuple(control at “action”, control at “stage”).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L188) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1198)

<a id="op-54e03411a6bf62"></a>
### Budget control

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_budgets_budget_control`

**Inputs** budget.

**Declared result** (dict bitwise or no value).

**Explicit results** mapping(“stage” → stage, “action” → action) · no value.

**Local steps**

- Set actions from stage\_actions(budget).
- For each wanted in tuple(“Stop”, “Warn”).
  - For each tuple(stage, \_period, action) in actions.
    - If action equals wanted.
      - Return mapping(“stage” → stage, “action” → action).
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L184) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1194)

<a id="op-f895c3328ecfd2"></a>
### Stage actions

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_budgets_stage_actions`

**Inputs** budget.

**Declared result** list at tuple at tuple(str, str, str).

**Explicit results** list of tuple(stage, period, budget at field) for tuple(stage, applies, annual, monthly) drawn from CONTROL\_STAGES where budget at applies, then tuple(period, field) drawn from tuple(tuple(“annual”, annual ….

**Local steps**

- Return list of tuple(stage, period, budget at field) for tuple(stage, applies, annual, monthly) drawn from CONTROL\_STAGES where budget at applies, then tuple(period, field) drawn from tuple(tuple(“annual”, annual ….
  - Draw tuple(stage, applies, annual, monthly) from CONTROL\_STAGES, keep a combination only if (budget at applies).
  - Draw tuple(period, field) from tuple(tuple(“annual”, annual), tuple(“monthly”, monthly)).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L189) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1199)

<a id="op-1dcc81cb9da44d"></a>
### Account status

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_budgets_account_status`

**Inputs** budget, spend.

**Declared result** str.

**Explicit results** “none” · “blocked” · “over” · “over\_to\_date” when exceeded, otherwise “ok”.

**Local steps**

- If not budget.
  - Return “none”.
- Set exceeded from exceeded\_checks(budget, spend).
- If any(generator of action equals “Stop” for tuple(\_period, action) drawn from exceeded).
  - Draw tuple(\_period, action) from exceeded.
  - Return “blocked”.
- If any(generator of period equals “annual” for tuple(period, \_action) drawn from exceeded).
  - Draw tuple(period, \_action) from exceeded.
  - Return “over”.
- Return “over\_to\_date” when exceeded, otherwise “ok”.
  - Value choice on exceeded — true gives “over\_to\_date”, false gives “ok”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L183) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1193)

<a id="op-0431560fa70621"></a>
### Exceeded checks

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_budgets_exceeded_checks`

**Inputs** budget, spend.

**Declared result** list at tuple at tuple(str, str).

**Explicit results** list of tuple(period, action) for tuple(stage, period, action) drawn from stage\_actions(budget) where flt((expense at period when stage equals “Expense”, otherwise amounts at stage − limits at period), pre ….

**Local steps**

- Set amounts from mapping(“Purchase Order” → spend at “ordered”, “Material Request” → spend at “requested”, “Cumulative” → ((spend at “ordered” + spend at “requested”) + spend at “actual”)).
- Set expense from mapping(“annual” → spend at “spent”, “monthly” → spend at “spent\_to\_date”).
- Set limits from mapping(“annual” → flt(budget at “budget\_amount”), “monthly” → monthly\_budget\_to\_date(budget)).
- Set precision from Platform.get\_precision(“Budget”, “budget\_amount”).
- Return list of tuple(period, action) for tuple(stage, period, action) drawn from stage\_actions(budget) where flt((expense at period when stage equals “Expense”, otherwise amounts at stage − limits at period), pre ….
  - Draw tuple(stage, period, action) from stage\_actions(budget), keep a combination only if (flt((expense at period when stage equals “Expense”, otherwise amounts at stage − limits at period), precision) &gt; 0).
  - Value choice on stage equals “Expense” — true gives expense at period, false gives amounts at stage.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L186) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1196)

<a id="op-146b7e6b8e1da1"></a>
### Monthly budget to date

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_budgets_monthly_budget_to_date`

**Inputs** budget.

**Declared result** float.

**Explicit results** sum(generator of amount for tuple(month, amount) drawn from budget at “by\_month”.items() where month ≤ this\_month).

**Local steps**

- Set this\_month from str(getdate()) at slice no value to 7.
- Return sum(generator of amount for tuple(month, amount) drawn from budget at “by\_month”.items() where month ≤ this\_month).
  - Draw tuple(month, amount) from budget at “by\_month”.items(), keep a combination only if (month ≤ this\_month).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L187) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1197)

<a id="op-ac1dd3c16e3d69"></a>
### Cost Drivers.initialize

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_drivers_costdrivers_init`

**Inputs** self, project, access.

**Local steps**

- Set self.queries from ProjectCostQueries(project, readable\_only = true).
- Set self.access from access.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L192) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1202)
