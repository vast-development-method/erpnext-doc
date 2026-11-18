# Accounting and settlement · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Budget

[Record definition](../../../../data/record-types/budget.json)

<a id="op-6d17b282e632ae"></a>
### Budget.validate existing expenses

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_validate_existing_expenses`

**Inputs** self.

**Record and data access** read “DocType” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Spending for Account {0} ({1}) between {2} and {3} has already exceeded the new allocated budget. Spent: {4} …”.format(Platform.bold(self.account), Platform.bold(self.company), Platform.bold(se ….

**Local steps**

- If (self.is\_new() and self.revision\_of).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → self.revision\_of.
  - Return no value.
- Set params from Platform.\_dict(mapping(“company” → self.company, “account” → self.account, “budget\_start\_date” → self.budget\_start\_date, “budget\_end\_date” → self.budget\_end\_date, …)).
- Set params at params.budget\_against\_field from self.get(params.budget\_against\_field).
- If Platform.get\_cached\_value(“DocType”, params.budget\_against\_doctype, “is\_tree”).
  - Set params.is\_tree from true.
- Otherwise.
  - Set params.is\_tree from false.
- Set actual\_spent from get\_actual\_expense(params).
- If actual\_spent &gt; self.budget\_amount.
  - Call the validation error handler Platform.throw(translated “Spending for Account {0} ({1}) between {2} and {3} has already exceeded the new allocated budget. Spent: {4} …”.format(Platform.bold(self.account), Platform.bold(self.company), P ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“DocType”, params.budget\_against\_doctype, “is\_tree”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L1784) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L584)

<a id="op-bf11954ba22dfb"></a>
### Budget.before save

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.allocate\_budget().
- Set self.budget\_distribution\_total from sum(generator of flt(row.amount) for row drawn from self.budget\_distribution).
  - Draw row from self.budget\_distribution.

If control reaches the end, it returns no value.

**Methods declared on this owner** [allocate budget](operations-022.md#op-5ea137ed4cbc3b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L2478) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L565)

<a id="op-423dfd4432743c"></a>
### Budget.on update

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_distribution\_totals().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate distribution totals](operations-022.md#op-fdbd953ebb9024).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L2597) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L570)

<a id="op-5ea137ed4cbc3b"></a>
### Budget.allocate budget

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_allocate_budget`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.\_should\_skip\_allocation().
  - Return no value.
- If self.\_should\_recalculate\_manual\_distribution().
  - Evaluate self.\_recalculate\_manual\_distribution().
  - Return no value.
- If not self.should\_regenerate\_budget\_distribution().
  - Return no value.
- Evaluate self.\_regenerate\_distribution().

If control reaches the end, it returns no value.

**Methods declared on this owner** [should skip allocation](operations-022.md#op-294d113eb71e0f), [should recalculate manual distribution](operations-022.md#op-0ea062ab3024c6), [recalculate manual distribution](operations-022.md#op-c492093e6cbec5), [should regenerate budget distribution](operations-022.md#op-2310120bfd7cc4), [regenerate distribution](operations-022.md#op-4597adc3485ebd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L2648) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L564)

<a id="op-294d113eb71e0f"></a>
### Budget.should skip allocation

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_should_skip_allocation`

**Inputs** self.

**Explicit results** (self.revision\_of and not self.distribute\_equally).

**Local steps**

- Return (self.revision\_of and not self.distribute\_equally).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.revision\_of → not self.distribute\_equally.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L2810) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L577)

<a id="op-0ea062ab3024c6"></a>
### Budget.should recalculate manual distribution

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_should_recalculate_manual_distribution`

**Inputs** self.

**Explicit results** (not self.distribute\_equally and bool(self.budget\_distribution) and self.\_is\_only\_budget\_amount\_changed()).

**Local steps**

- Return (not self.distribute\_equally and bool(self.budget\_distribution) and self.\_is\_only\_budget\_amount\_changed()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.distribute\_equally → bool(self.budget\_distribution) → self.\_is\_only\_budget\_amount\_changed().

**Methods declared on this owner** [is only budget amount changed](operations-022.md#op-ce30e4b9881ce3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L2869) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L575)

<a id="op-ce30e4b9881ce3"></a>
### Budget.is only budget amount changed

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_is_only_budget_amount_changed`

**Inputs** self.

**Explicit results** false · (old.budget\_amount differs from self.budget\_amount and old.distribution\_frequency equals self.distribution\_frequency and old.budget\_start\_date equals self.budget\_start\_date and old.budget\_end\_date equals s ….

**Local steps**

- Set old from self.get\_doc\_before\_save().
- If not old.
  - Return false.
- Return (old.budget\_amount differs from self.budget\_amount and old.distribution\_frequency equals self.distribution\_frequency and old.budget\_start\_date equals self.budget\_start\_date and old.budget\_end\_date equals s ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old.budget\_amount differs from self.budget\_amount → old.distribution\_frequency equals self.distribution\_frequency → old.budget\_start\_date equals self.budget\_start\_date → old.budget\_end\_date equals self.budget\_end\_date.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L2959) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L594) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L569)

<a id="op-c492093e6cbec5"></a>
### Budget.recalculate manual distribution

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_recalculate_manual_distribution`

**Inputs** self.

**Local steps**

- For each row in self.budget\_distribution.
  - Set row.amount from flt(((row.percent ÷ 100) × self.budget\_amount), 3).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L3140) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L571)

<a id="op-2310120bfd7cc4"></a>
### Budget.should regenerate budget distribution

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_should_regenerate_budget_distribution`

**Inputs** self.

**Explicit results** true · bool(self.distribute\_equally).

**Local steps**

- Set old\_doc from self.get\_doc\_before\_save() when not self.is\_new(), otherwise no value.
  - Value choice on not self.is\_new() — true gives self.get\_doc\_before\_save(), false gives no value.
- If (not old\_doc or not self.budget\_distribution).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not old\_doc → not self.budget\_distribution.
  - Return true.
- If old\_doc.
  - Set changed\_fields from list(“from\_fiscal\_year”, “to\_fiscal\_year”, “budget\_amount”, “distribution\_frequency”).
  - For each field in changed\_fields.
    - If old\_doc.get(field) differs from self.get(field).
      - Return true.
- Return bool(self.distribute\_equally).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L3247) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L576)

<a id="op-4597adc3485ebd"></a>
### Budget.regenerate distribution

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_regenerate_distribution`

**Inputs** self.

**Local steps**

- Evaluate self.set(“budget\_distribution”, list()).
- Set periods from self.get\_budget\_periods().
- Set total\_periods from len(periods).
- Set row\_percent from (100 ÷ total\_periods) when total\_periods, otherwise 0.
  - Value choice on total\_periods — true gives (100 ÷ total\_periods), false gives 0.
- For each tuple(start\_date, end\_date) in periods.
  - Set row from self.append(“budget\_distribution”, mapping()).
  - Set row.start\_date from start\_date.
  - Set row.end\_date from end\_date.
  - Evaluate self.add\_allocated\_amount(row, row\_percent).
- Set self.budget\_distribution\_total from self.budget\_amount.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get budget periods](operations-022.md#op-f8d706029b533f), [add allocated amount](operations-022.md#op-f83643924557b3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L3525) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L597) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L572)

<a id="op-f8d706029b533f"></a>
### Budget.get budget periods

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_get_budget_periods`

**Inputs** self.

**Explicit results** periods.

**Local steps**

- Set frequency from self.distribution\_frequency.
- Set periods from list().
- Set start\_date from getdate(self.budget\_start\_date).
- Set end\_date from getdate(self.budget\_end\_date).
- While start\_date ≤ end\_date.
  - Set period\_start from get\_first\_day(start\_date).
  - Set period\_end from self.get\_period\_end(period\_start, frequency).
  - Set period\_end from min(period\_end, end\_date).
  - Evaluate periods.append(tuple(period\_start, period\_end)).
  - Set start\_date from add\_months(period\_start, self.get\_month\_increment(frequency)).
- Return periods.

**Methods declared on this owner** [get period end](operations-022.md#op-1dc6cbacebf32f), [get month increment](operations-022.md#op-a17d82d8e2f3da).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L3818) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L566)

<a id="op-1dc6cbacebf32f"></a>
### Budget.get period end

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_get_period_end`

**Inputs** self, start\_date, frequency.

**Explicit results** get\_last\_day(start\_date) · get\_last\_day(add\_months(start\_date, 2)) · get\_last\_day(add\_months(start\_date, 5)) · get\_last\_day(add\_months(start\_date, 11)).

**Local steps**

- If frequency equals “Monthly”.
  - Return get\_last\_day(start\_date).
- Otherwise.
  - If frequency equals “Quarterly”.
    - Return get\_last\_day(add\_months(start\_date, 2)).
  - Otherwise.
    - If frequency equals “Half-Yearly”.
      - Return get\_last\_day(add\_months(start\_date, 5)).
    - Otherwise.
      - Return get\_last\_day(add\_months(start\_date, 11)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L4140) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L568)

<a id="op-a17d82d8e2f3da"></a>
### Budget.get month increment

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_get_month_increment`

**Inputs** self, frequency.

**Explicit results** mapping(“Monthly” → 1, “Quarterly” → 3, “Half-Yearly” → 6, “Yearly” → 12).get(frequency, 1).

**Local steps**

- Return mapping(“Monthly” → 1, “Quarterly” → 3, “Half-Yearly” → 6, “Yearly” → 12).get(frequency, 1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L4387) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L567)

<a id="op-f83643924557b3"></a>
### Budget.add allocated amount

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_add_allocated_amount`

**Inputs** self, row, row\_percent.

**Local steps**

- Set row.amount from flt(((self.budget\_amount × row\_percent) ÷ 100), 3).
- Set row.percent from flt(row\_percent, 3).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L4497) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L563)

<a id="op-fdbd953ebb9024"></a>
### Budget.validate distribution totals

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_validate_distribution_totals`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Total distributed amount {0} must be equal to Budget Amount {1}”.format(flt(total\_amount, 2), self.budget\_amount) · validation helper — translated “Total distribution percent must equal 100 (currently {0})”.format(round(total\_percent, 2)).

**Local steps**

- If self.should\_regenerate\_budget\_distribution().
  - Return no value.
- Set total\_amount from sum(generator of flt(d.amount) for d drawn from self.budget\_distribution).
  - Draw d from self.budget\_distribution.
- Set total\_percent from sum(generator of flt(d.percent) for d drawn from self.budget\_distribution).
  - Draw d from self.budget\_distribution.
- If flt(abs((total\_amount − self.budget\_amount)), 2) &gt; 0.1.
  - Call the validation error handler Platform.throw(translated “Total distributed amount {0} must be equal to Budget Amount {1}”.format(flt(total\_amount, 2), self.budget\_amount)).
- If flt(abs((total\_percent − 100)), 2) &gt; 0.1.
  - Call the validation error handler Platform.throw(translated “Total distribution percent must equal 100 (currently {0})”.format(round(total\_percent, 2))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [should regenerate budget distribution](operations-022.md#op-2310120bfd7cc4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L4627) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L582)

<a id="op-e7fea44e1d9740"></a>
### Validate expense against budget

`operation_enterprise_accounts_record_definitions_budget_business_behavior_validate_expense_against_budget`

**Inputs** params, expense\_amount = 0.

**Record and data access** read “Budget” via count · execute query text (SELECT, Budget, Fiscal Year) · read “Company” via get\_cached\_value · read “Account” via get\_cached\_value · read “DocType” via get\_cached\_value · 1 additional forms in the steps below.

**State and service calls** execute a supplied database query.

**Explicit results** no value.

**Local steps**

- Set params from Platform.\_dict(params).
- If not Platform.db.count(“Budget”, cache = true).
  - Return no value.
- If not params.fiscal\_year.
  - Set params.fiscal\_year from get\_fiscal\_year(params.get(“posting\_date”), company = params.get(“company”)) at 0.
- Set posting\_date from getdate(params.get(“posting\_date”)).
- Set posting\_fiscal\_year from get\_fiscal\_year(posting\_date, company = params.get(“company”)) at 0.
- Set tuple(year\_start\_date, year\_end\_date) from get\_fiscal\_year\_date\_range(posting\_fiscal\_year, posting\_fiscal\_year).
- Set budget\_exists from Platform.db.sql(query text (SELECT, Budget, Fiscal Year), tuple(params.company, year\_end\_date, year\_start\_date)).
- If not budget\_exists.
  - Return no value.
- If params.get(“company”).
  - Set Platform.flags.exception\_approver\_role from Platform.get\_cached\_value(“Company”, params.get(“company”), “exception\_budget\_approver\_role”).
- If not params.account.
  - Set params.account from params.get(“expense\_account”).
- If (not params.get(“expense\_account”) and params.get(“account”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not params.get(“expense\_account”) → params.get(“account”).
  - Set params.expense\_account from params.account.
- If (not (params.get(“account”) and params.get(“cost\_center”)) and params.item\_code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not (params.get(“account”) and params.get(“cost\_center”)) → params.item\_code.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in params.get(“account”) → params.get(“cost\_center”).
  - Set tuple(params.cost\_center, params.account) from get\_item\_details(params).
- If not params.account.
  - Return no value.
- Set default\_dimensions from list(mapping(“fieldname” → “project”, “document\_type” → “Project”), mapping(“fieldname” → “cost\_center”, “document\_type” → “Cost Center”)).
- For each dimension in (default\_dimensions + get\_accounting\_dimensions(as\_list = false)).
  - Set budget\_against from dimension.get(“fieldname”).
  - If (params.get(budget\_against) and params.account and Platform.get\_cached\_value(“Account”, params.account, “root\_type”) equals “Expense”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in params.get(budget\_against) → params.account → Platform.get\_cached\_value(“Account”, params.account, “root\_type”) equals “Expense”.
    - Set doctype from dimension.get(“document\_type”).
    - If Platform.get\_cached\_value(“DocType”, doctype, “is\_tree”).
      - Set tuple(lft, rgt) from Platform.get\_cached\_value(doctype, params.get(budget\_against), list(“lft”, “rgt”)).
      - Set condition from formatted text and exists(select name from ′tab{doctype}′  where lft&lt;={lft} and rgt&gt;={rgt} and name=b.{budget\_against}).
      - Set params.is\_tree from true.
    - Otherwise.
      - Set condition from formatted text and b.{budget\_against}={Platform.db.escape(params.get(budget\_against))}.
      - Set params.is\_tree from false.
    - Set params.budget\_against\_field from budget\_against.
    - Set params.budget\_against\_doctype from doctype.
    - Set budget\_records from Platform.db.sql(formatted text   SELECT  b.name,  b.{budget\_against} AS budget\_against,  b.budget\_amount,  b.from\_fiscal\_year,  b.to\_fiscal\_year,  b.budge, tuple(params.company,  ….
    - If budget\_records.
      - Evaluate validate\_budget\_records(params, budget\_records, expense\_amount).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, params.get(“company”), “exception\_budget\_approver\_role”), Platform.get\_cached\_value(“Account”, params.account, “root\_type”) and 2 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L600)

<a id="op-961c4e967baef3"></a>
### Validate budget records

`operation_enterprise_accounts_record_definitions_budget_business_behavior_validate_budget_records`

**Inputs** params, budget\_records, expense\_amount.

**Local steps**

- For each budget in budget\_records.
  - If flt(budget.budget\_amount).
    - Set tuple(yearly\_action, monthly\_action) from get\_actions(params, budget).
    - Set params at “for\_material\_request” from budget.for\_material\_request.
    - Set params at “for\_purchase\_order” from budget.for\_purchase\_order.
    - Set tuple(params at “from\_fiscal\_year”, params at “to\_fiscal\_year”) from tuple(budget.from\_fiscal\_year, budget.to\_fiscal\_year).
    - Set tuple(params at “budget\_start\_date”, params at “budget\_end\_date”) from tuple(budget.budget\_start\_date, budget.budget\_end\_date).
    - If yearly\_action belongs to tuple(“Stop”, “Warn”).
      - Evaluate compare\_expense\_with\_budget(params, flt(budget.budget\_amount), translated “Annual”, yearly\_action, …).
    - If monthly\_action belongs to list(“Stop”, “Warn”).
      - Set budget\_amount from get\_accumulated\_monthly\_budget(budget.name, params.posting\_date).
      - Set params at “month\_end\_date” from get\_last\_day(params.posting\_date).
      - Evaluate compare\_expense\_with\_budget(params, budget\_amount, translated “Accumulated Monthly”, monthly\_action, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0033.json#L2602) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L599)

<a id="op-a409694bb69ef9"></a>
### Compare expense with budget

`operation_enterprise_accounts_record_definitions_budget_business_behavior_compare_expense_with_budget`

**Inputs** params, budget\_amount, action\_for, action, budget\_against, amount = 0.

**Record and data access** read “Company” via get\_cached\_value.

**State and service calls** msgprint with msg.

**Explicit failure paths** validation helper with BudgetError — msg.

**Local steps**

- Set tuple(params.actual\_expense, params.requested\_amount, params.ordered\_amount) from tuple(get\_actual\_expense(params), 0, 0).
- If not amount.
  - Set tuple(params.requested\_amount, params.ordered\_amount) from tuple(get\_requested\_amount(params), get\_ordered\_amount(params)).
  - If (params.get(“doctype”) equals “Material Request” and params.for\_material\_request).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in params.get(“doctype”) equals “Material Request” → params.for\_material\_request.
    - Set amount from (params.requested\_amount + params.ordered\_amount).
  - Otherwise.
    - If (params.get(“doctype”) equals “Purchase Order” and params.for\_purchase\_order).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in params.get(“doctype”) equals “Purchase Order” → params.for\_purchase\_order.
      - Set amount from params.ordered\_amount.
- Set total\_expense from (params.actual\_expense + amount).
- If flt((total\_expense − budget\_amount), Platform.get\_precision(“Budget”, “budget\_amount”)) &gt; 0.
  - If params.actual\_expense &gt; budget\_amount.
    - Set diff from (params.actual\_expense − budget\_amount).
    - Set \_msg from translated “{0} Budget for Account {1} against {2} {3} is {4}. It is already exceeded by {5}.”.
  - Otherwise.
    - Set diff from (total\_expense − budget\_amount).
    - Set \_msg from translated “{0} Budget for Account {1} against {2} {3} is {4}. It will be exceeded by {5}.”.
  - Set currency from Platform.get\_cached\_value(“Company”, params.company, “default\_currency”).
  - Set msg from \_msg.format(translated action\_for, Platform.bold(params.account), Platform.unscrub(params.budget\_against\_field), Platform.bold(budget\_against), …).
  - Update msg using + get\_expense\_breakup(params, currency, budget\_against).
  - If (Platform.flags.exception\_approver\_role and Platform.flags.exception\_approver\_role belongs to Platform.get\_roles(Platform.session.user)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.exception\_approver\_role → Platform.flags.exception\_approver\_role belongs to Platform.get\_roles(Platform.session.user).
    - Set action from “Warn”.
  - If action equals “Stop”.
    - Call the validation error handler Platform.throw(msg, BudgetError, title = translated “Budget Exceeded”).
  - Otherwise.
    - Evaluate Platform.msgprint(msg, indicator = “orange”, title = translated “Budget Exceeded”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, params.company, “default\_currency”) · effective access from Platform.get\_roles(Platform.session.user).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L587)

<a id="op-d909e03780783b"></a>
### Get expense breakup

`operation_enterprise_accounts_record_definitions_budget_business_behavior_get_expense_breakup`

**Inputs** params, currency, budget\_against.

**Record and data access** read “Fiscal Year” via get\_cached\_value.

**Explicit results** msg.

**Local steps**

- Set msg from text in the contract.format(translated “Total Expenses booked through”).
- Set common\_filters from Platform.\_dict(mapping(params.budget\_against\_field → budget\_against, “account” → params.account, “company” → params.company)).
- Set from\_date from Platform.get\_cached\_value(“Fiscal Year”, params.from\_fiscal\_year, “year\_start\_date”).
- Set to\_date from Platform.get\_cached\_value(“Fiscal Year”, params.to\_fiscal\_year, “year\_end\_date”).
- Set gl\_filters from common\_filters.copy().
- Evaluate gl\_filters.update(mapping(“from\_date” → from\_date, “to\_date” → to\_date, “is\_cancelled” → 0)).
- Update msg using + ((((text in the contract + nested operand in the contract.utils.get\_link\_to\_report(“General Ledger”, label = translated “Actual Expenses”, filters = gl\_filters)) + “ - ”) + Platform.bold(fmt\_money(params.a ….
- Set mr\_filters from common\_filters.copy().
- Evaluate mr\_filters.update(mapping(“status” → list(list(“!=”, “Stopped”)), “docstatus” → 1, “material\_request\_type” → “Purchase”, “schedule\_date” → list(list(“between”, list(from\_date, to\_date))), …)).
- Update msg using + ((((text in the contract + nested operand in the contract.utils.get\_link\_to\_report(“Material Request”, label = translated “Material Requests”, report\_type = “Report Builder”, doctype = “Material Request”,  ….
- Set po\_filters from common\_filters.copy().
- Evaluate po\_filters.update(mapping(“status” → list(list(“!=”, “Closed”)), “docstatus” → 1, “transaction\_date” → list(list(“between”, list(from\_date, to\_date))), “per\_billed” → list(list(“&lt;”, 100)))).
- Update msg using + ((((text in the contract + nested operand in the contract.utils.get\_link\_to\_report(“Purchase Order”, label = translated “Unbilled Orders”, report\_type = “Report Builder”, doctype = “Purchase Order”, filter ….
- Return msg.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Fiscal Year”, params.from\_fiscal\_year, “year\_start\_date”), Platform.get\_cached\_value(“Fiscal Year”, params.to\_fiscal\_year, “year\_end\_date”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L591)

<a id="op-a9c238fe25c5d9"></a>
### Get actions

`operation_enterprise_accounts_record_definitions_budget_business_behavior_get_actions`

**Inputs** params, budget.

**Explicit results** tuple(yearly\_action, monthly\_action).

**Local steps**

- Set yearly\_action from budget.action\_if\_annual\_budget\_exceeded.
- Set monthly\_action from budget.action\_if\_accumulated\_monthly\_budget\_exceeded.
- If (params.get(“doctype”) equals “Material Request” and budget.for\_material\_request).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in params.get(“doctype”) equals “Material Request” → budget.for\_material\_request.
  - Set yearly\_action from budget.action\_if\_annual\_budget\_exceeded\_on\_mr.
  - Set monthly\_action from budget.action\_if\_accumulated\_monthly\_budget\_exceeded\_on\_mr.
- Otherwise.
  - If (params.get(“doctype”) equals “Purchase Order” and budget.for\_purchase\_order).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in params.get(“doctype”) equals “Purchase Order” → budget.for\_purchase\_order.
    - Set yearly\_action from budget.action\_if\_annual\_budget\_exceeded\_on\_po.
    - Set monthly\_action from budget.action\_if\_accumulated\_monthly\_budget\_exceeded\_on\_po.
- Return tuple(yearly\_action, monthly\_action).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0033.json#L5501) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L614) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L589)

<a id="op-561dde06c59d51"></a>
### Get requested amount

`operation_enterprise_accounts_record_definitions_budget_business_behavior_get_requested_amount`

**Inputs** params.

**Explicit results** data at 0 at 0 when data, otherwise 0.

**Local steps**

- Set child from Platform.qb.DocType(“Material Request Item”).
- Set parent from Platform.qb.DocType(“Material Request”).
- Set data from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“amount”)).where(((((nested operand in the contract bitwise and nested operand in the contract) bitw ….
- Return data at 0 at 0 when data, otherwise 0.
  - Value choice on data — true gives data at 0 at 0, false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L622) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L597)

<a id="op-a2ed724a5edfc0"></a>
### Get ordered amount

`operation_enterprise_accounts_record_definitions_budget_business_behavior_get_ordered_amount`

**Inputs** params.

**Record and data access** read “Fiscal Year” via get\_cached\_value.

**Explicit results** data at 0 at 0 when data, otherwise 0.

**Local steps**

- Set child from Platform.qb.DocType(“Purchase Order Item”).
- Set parent from Platform.qb.DocType(“Purchase Order”).
- Set conditions from list(parent.docstatus equals 1, child.amount &gt; child.billed\_amt, parent.status differs from “Closed”, child.expense\_account equals params.expense\_account).
- Set budget\_against\_field from params.get(“budget\_against\_field”).
- If (budget\_against\_field and params.get(budget\_against\_field)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in budget\_against\_field → params.get(budget\_against\_field).
  - Evaluate conditions.append(child at budget\_against\_field equals params.get(budget\_against\_field)).
- Set start\_date from Platform.get\_cached\_value(“Fiscal Year”, params.from\_fiscal\_year, “year\_start\_date”).
- Set end\_date from Platform.get\_cached\_value(“Fiscal Year”, params.to\_fiscal\_year, “year\_end\_date”).
- Evaluate conditions.append(parent.transaction\_date at slice str(start\_date) to str(end\_date)).
- Set data from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“amount”)).where(Criterion.all(conditions)).run(as\_list = 1).
- Return data at 0 at 0 when data, otherwise 0.
  - Value choice on data — true gives data at 0 at 0, false gives 0.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Fiscal Year”, params.from\_fiscal\_year, “year\_start\_date”), Platform.get\_cached\_value(“Fiscal Year”, params.to\_fiscal\_year, “year\_end\_date”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L620) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L595)

<a id="op-1062a9594ce0be"></a>
### Get other condition

`operation_enterprise_accounts_record_definitions_budget_business_behavior_get_other_condition`

**Inputs** params, child, parent, for\_doc.

**Record and data access** read “Fiscal Year” via get\_cached\_value.

**Explicit results** conditions.

**Local steps**

- Set conditions from list(child.expense\_account equals params.expense\_account).
- Set budget\_against\_field from params.get(“budget\_against\_field”).
- If (budget\_against\_field and params.get(budget\_against\_field)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in budget\_against\_field → params.get(budget\_against\_field).
  - Evaluate conditions.append(child at budget\_against\_field equals params.get(budget\_against\_field)).
- Set date\_field from “schedule\_date” when for\_doc equals “Material Request”, otherwise “transaction\_date”.
  - Value choice on for\_doc equals “Material Request” — true gives “schedule\_date”, false gives “transaction\_date”.
- Set start\_date from Platform.get\_cached\_value(“Fiscal Year”, params.from\_fiscal\_year, “year\_start\_date”).
- Set end\_date from Platform.get\_cached\_value(“Fiscal Year”, params.to\_fiscal\_year, “year\_end\_date”).
- Evaluate conditions.append(parent at date\_field at slice str(start\_date) to str(end\_date)).
- Return conditions.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Fiscal Year”, params.from\_fiscal\_year, “year\_start\_date”), Platform.get\_cached\_value(“Fiscal Year”, params.to\_fiscal\_year, “year\_end\_date”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0034.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L621) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L596)

<a id="op-68a3055b53517b"></a>
### Get actual expense

`operation_enterprise_accounts_record_definitions_budget_business_behavior_get_actual_expense`

**Inputs** params.

**Record and data access** read params.budget\_against\_doctype via get\_value.

**State and service calls** execute a supplied database query.

**Explicit results** amount.

**Local steps**

- If not params.budget\_against\_doctype.
  - Set params.budget\_against\_doctype from Platform.unscrub(params.budget\_against\_field).
- Set budget\_against\_field from params.get(“budget\_against\_field”).
- Set condition1 from “ and gle.posting\_date &lt;= %(month\_end\_date)s” when params.get(“month\_end\_date”), otherwise empty text.
  - Value choice on params.get(“month\_end\_date”) — true gives “ and gle.posting\_date &lt;= %(month\_end\_date)s”, false gives empty text.
- Set date\_condition from formatted text and gle.posting\_date between '{params.budget\_start\_date}' and '{params.budget\_end\_date}'.
- If params.is\_tree.
  - Set lft\_rgt from Platform.db.get\_value(params.budget\_against\_doctype, params.get(budget\_against\_field), list(“lft”, “rgt”), as\_dict = 1).
  - Evaluate params.update(lft\_rgt).
  - Set condition2 from formatted text   and exists(  select name from ′tab{params.budget\_against\_doctype}′  where lft &gt;= %(lft)s and rgt &lt;= %(rgt)s  and name = gle.{budget\_again.
- Otherwise.
  - Set condition2 from formatted text   and gle.{budget\_against\_field} = %({budget\_against\_field})s.
- Set amount from flt(Platform.db.sql(formatted text   select sum(gle.debit) - sum(gle.credit)  from ′tabGL Entry′ gle  where  is\_cancelled = 0  and gle.account = %(account)s  {condi, params) at 0 at 0).
- Return amount.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L590)
