# Accounting and settlement · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Billed items to be received

<a id="op-017d39295e9cc2"></a>
### Get receipt returns as on

`operation_enterprise_binding_enterprise_accounts_report_billed_items_to_be_received_billed_items_to_be_received_get_receipt_returns_as_on`

**Inputs** as\_on\_date, linked\_by, alias.

**Explicit results** nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isnotnull()).groupby(link\_field).as\_(alias).

**Local steps**

- Set return\_receipt from Platform.qb.DocType(“Purchase Receipt”).
- Set return\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Set original\_item from Platform.qb.DocType(“Purchase Receipt Item”).as\_(“original\_item”).
- Set link\_field from getattr(original\_item, linked\_by).
- Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isnotnull()).groupby(link\_field).as\_(alias).

**Values supplied outside this operation** selected callable from getattr(original\_item, linked\_by).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1134)

<a id="op-93ad17542c6a16"></a>
### Get columns

`operation_enterprise_accounts_report_billed_items_to_be_received_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Purchase Invoice”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Purchase Invoice”, …), mapping(“label” → translated “Supplier”, “fieldname” → “supplier”, “fie ….

**Local steps**

- Return list(mapping(“label” → translated “Purchase Invoice”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Purchase Invoice”, …), mapping(“label” → translated “Supplier”, “fieldname” → “supplier”, “fie ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L692)

## Record · Bisect accounting statements

[Record definition](../../../../data/record-types/bisect_accounting_statements.json)

<a id="op-672f432dd7a576"></a>
### Bisect Accounting Statements.validate

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_dates().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dates](operations-021.md#op-891133c6084eef).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L1329) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L561)

<a id="op-891133c6084eef"></a>
### Bisect Accounting Statements.validate dates

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “From Date: {0} cannot be greater than To date: {1}”.format(Platform.bold(self.from\_date), Platform.bold(self.to\_date)).

**Local steps**

- If getdate(self.from\_date) &gt; getdate(self.to\_date).
  - Call the validation error handler Platform.throw(translated “From Date: {0} cannot be greater than To date: {1}”.format(Platform.bold(self.from\_date), Platform.bold(self.to\_date))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L1380) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L582) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L562)

<a id="op-99335ea4384f3e"></a>
### Bisect Accounting Statements.bfs

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_breadth_first_search`

**Inputs** self, from\_date, to\_date.

**State and service calls** request new\_doc for “Bisect Nodes” · call insert on node · call insert on left\_node · call insert on right\_node · call save on cur\_node.

**Local steps**

- Set node from Platform.new\_doc(“Bisect Nodes”).
- Set node.root from no value.
- Set node.period\_from\_date from from\_date.
- Set node.period\_to\_date from to\_date.
- Evaluate node.insert().
- Set period\_queue from deque(list(node)).
- While period\_queue.
  - Set cur\_node from period\_queue.popleft().
  - Set delta from (cur\_node.period\_to\_date − cur\_node.period\_from\_date).
  - If delta.days equals 0.
    - Continue with the next iteration or loop test.
  - Otherwise.
    - Set cur\_floor from floor((delta.days ÷ 2)).
    - Set next\_to\_date from (cur\_node.period\_from\_date + relativedelta(days = positive cur\_floor)).
    - Set left\_node from Platform.new\_doc(“Bisect Nodes”).
    - Set left\_node.period\_from\_date from cur\_node.period\_from\_date.
    - Set left\_node.period\_to\_date from next\_to\_date.
    - Set left\_node.root from cur\_node.name.
    - Set left\_node.generated from false.
    - Evaluate left\_node.insert().
    - Set cur\_node.left\_child from left\_node.name.
    - Evaluate period\_queue.append(left\_node).
    - Set next\_from\_date from (cur\_node.period\_from\_date + relativedelta(days = positive (cur\_floor + 1))).
    - Set right\_node from Platform.new\_doc(“Bisect Nodes”).
    - Set right\_node.period\_from\_date from next\_from\_date.
    - Set right\_node.period\_to\_date from cur\_node.period\_to\_date.
    - Set right\_node.root from cur\_node.name.
    - Set right\_node.generated from false.
    - Evaluate right\_node.insert().
    - Set cur\_node.right\_child from right\_node.name.
    - Evaluate period\_queue.append(right\_node).
    - Evaluate cur\_node.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L1571) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L572) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L552)

<a id="op-dbd13fa17d2f6d"></a>
### Bisect Accounting Statements.dfs

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_depth_first_search`

**Inputs** self, from\_date, to\_date.

**State and service calls** request new\_doc for “Bisect Nodes” · call insert on node · call insert on left\_node · call insert on right\_node · call save on cur\_node.

**Local steps**

- Set node from Platform.new\_doc(“Bisect Nodes”).
- Set node.root from no value.
- Set node.period\_from\_date from from\_date.
- Set node.period\_to\_date from to\_date.
- Evaluate node.insert().
- Set period\_stack from list(node).
- While period\_stack.
  - Set cur\_node from period\_stack.pop().
  - Set delta from (cur\_node.period\_to\_date − cur\_node.period\_from\_date).
  - If delta.days equals 0.
    - Continue with the next iteration or loop test.
  - Otherwise.
    - Set cur\_floor from floor((delta.days ÷ 2)).
    - Set next\_to\_date from (cur\_node.period\_from\_date + relativedelta(days = positive cur\_floor)).
    - Set left\_node from Platform.new\_doc(“Bisect Nodes”).
    - Set left\_node.period\_from\_date from cur\_node.period\_from\_date.
    - Set left\_node.period\_to\_date from next\_to\_date.
    - Set left\_node.root from cur\_node.name.
    - Set left\_node.generated from false.
    - Evaluate left\_node.insert().
    - Set cur\_node.left\_child from left\_node.name.
    - Evaluate period\_stack.append(left\_node).
    - Set next\_from\_date from (cur\_node.period\_from\_date + relativedelta(days = positive (cur\_floor + 1))).
    - Set right\_node from Platform.new\_doc(“Bisect Nodes”).
    - Set right\_node.period\_from\_date from next\_from\_date.
    - Set right\_node.period\_to\_date from cur\_node.period\_to\_date.
    - Set right\_node.root from cur\_node.name.
    - Set right\_node.generated from false.
    - Evaluate right\_node.insert().
    - Set cur\_node.right\_child from right\_node.name.
    - Evaluate period\_stack.append(right\_node).
    - Evaluate cur\_node.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L2354) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L575) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L555)

<a id="op-2dc42e7303e92a"></a>
### Bisect Accounting Statements.build tree

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_build_tree`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Bisect Nodes” via get\_all.

**State and service calls** request delete on “Bisect Nodes” · call save on self.

**Local steps**

- Evaluate Platform.db.delete(“Bisect Nodes”).
- Set dt\_format from guess\_date\_format(self.from\_date).
- Set from\_date from datetime.datetime.strptime(self.from\_date, dt\_format).
- Set to\_date from datetime.datetime.strptime(self.to\_date, dt\_format).
- If self.algorithm equals “BFS”.
  - Evaluate self.bfs(from\_date, to\_date).
- If self.algorithm equals “DFS”.
  - Evaluate self.dfs(from\_date, to\_date).
- Set root from Platform.db.get\_all(“Bisect Nodes”, filters = mapping(“root” → list(“is”, “not set”))) at 0.
- Set self.current\_node from root.name.
- Set self.current\_from\_date from self.from\_date.
- Set self.current\_to\_date from self.to\_date.
- Evaluate self.get\_report\_summary().
- Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [bfs](operations-021.md#op-99335ea4384f3e), [dfs](operations-021.md#op-dbd13fa17d2f6d), [get report summary](operations-021.md#op-f3f683f145fa3c).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L3125) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L573) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L553)

<a id="op-f3f683f145fa3c"></a>
### Bisect Accounting Statements.get report summary

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_get_report_summary`

**Inputs** self.

**Record and data access** resolve a document from “Report” via get\_doc.

**Local steps**

- Set filters from mapping(“company” → self.company, “filter\_based\_on” → “Date Range”, “period\_start\_date” → self.current\_from\_date, “period\_end\_date” → self.current\_to\_date, …).
- Set pl\_summary from Platform.get\_doc(“Report”, “Profit and Loss Statement”).
- Set self.p\_l\_summary from pl\_summary.execute\_script\_report(filters = filters) at 5.
- Set bs\_summary from Platform.get\_doc(“Report”, “Balance Sheet”).
- Set self.b\_s\_summary from bs\_summary.execute\_script\_report(filters = filters) at 5.
- Set self.difference from abs((self.p\_l\_summary − self.b\_s\_summary)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L3631) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L578) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L558)

<a id="op-c14dc50357821a"></a>
### Bisect Accounting Statements.update node

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_update_runtime_process`

**Inputs** self.

**Record and data access** resolve a document from “Bisect Nodes” via get\_doc.

**State and service calls** call save on current\_node.

**Local steps**

- Set current\_node from Platform.get\_doc(“Bisect Nodes”, self.current\_node).
- Set current\_node.balance\_sheet\_summary from self.b\_s\_summary.
- Set current\_node.profit\_loss\_summary from self.p\_l\_summary.
- Set current\_node.difference from self.difference.
- Set current\_node.generated from true.
- Evaluate current\_node.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L3973) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L580) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L560)

<a id="op-4c03d9a3002488"></a>
### Bisect Accounting Statements.current node has summary info

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_current_runtime_process_has_summary_info`

**Inputs** self.

**Record and data access** read “Bisect Nodes” via get\_value.

**Explicit results** Platform.db.get\_value(“Bisect Nodes”, self.current\_node, “generated”).

**Local steps**

- Return Platform.db.get\_value(“Bisect Nodes”, self.current\_node, “generated”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L4146) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L574) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L554)

<a id="op-f811d5b8c1561b"></a>
### Bisect Accounting Statements.fetch summary info from current node

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_fetch_summary_info_from_current_runtime_process`

**Inputs** self.

**Record and data access** resolve a document from “Bisect Nodes” via get\_doc.

**Local steps**

- Set current\_node from Platform.get\_doc(“Bisect Nodes”, self.current\_node).
- Set self.p\_l\_summary from current\_node.profit\_loss\_summary.
- Set self.b\_s\_summary from current\_node.balance\_sheet\_summary.
- Set self.difference from abs((self.p\_l\_summary − self.b\_s\_summary)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L577) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L557)

<a id="op-343d3252a1b90b"></a>
### Bisect Accounting Statements.fetch or calculate

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_fetch_or_calculate`

**Inputs** self.

**Local steps**

- If self.current\_node\_has\_summary\_info().
  - Evaluate self.fetch\_summary\_info\_from\_current\_node().
- Otherwise.
  - Evaluate self.get\_report\_summary().
  - Evaluate self.update\_node().

If control reaches the end, it returns no value.

**Methods declared on this owner** [current node has summary info](operations-021.md#op-4c03d9a3002488), [fetch summary info from current node](operations-021.md#op-f811d5b8c1561b), [get report summary](operations-021.md#op-f3f683f145fa3c), [update node](operations-021.md#op-c14dc50357821a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L4390) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L576) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L556)

<a id="op-ef6c332b064d09"></a>
### Bisect Accounting Statements.bisect left

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_bisect_left`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bisect Nodes” via get\_doc.

**State and service calls** call save on self · msgprint with translated “No more children on Left”.

**Local steps**

- If self.current\_node is distinct from no value.
  - Set cur\_node from Platform.get\_doc(“Bisect Nodes”, self.current\_node).
  - If cur\_node.left\_child is distinct from no value.
    - Set lft\_node from Platform.get\_doc(“Bisect Nodes”, cur\_node.left\_child).
    - Set self.current\_node from cur\_node.left\_child.
    - Set self.current\_from\_date from lft\_node.period\_from\_date.
    - Set self.current\_to\_date from lft\_node.period\_to\_date.
    - Evaluate self.fetch\_or\_calculate().
    - Evaluate self.save().
  - Otherwise.
    - Evaluate Platform.msgprint(translated “No more children on Left”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [fetch or calculate](operations-021.md#op-343d3252a1b90b).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L4505) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L570) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L550)

<a id="op-1b2a15993a7bba"></a>
### Bisect Accounting Statements.bisect right

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_bisect_right`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bisect Nodes” via get\_doc.

**State and service calls** call save on self · msgprint with translated “No more children on Right”.

**Local steps**

- If self.current\_node is distinct from no value.
  - Set cur\_node from Platform.get\_doc(“Bisect Nodes”, self.current\_node).
  - If cur\_node.right\_child is distinct from no value.
    - Set rgt\_node from Platform.get\_doc(“Bisect Nodes”, cur\_node.right\_child).
    - Set self.current\_node from cur\_node.right\_child.
    - Set self.current\_from\_date from rgt\_node.period\_from\_date.
    - Set self.current\_to\_date from rgt\_node.period\_to\_date.
    - Evaluate self.fetch\_or\_calculate().
    - Evaluate self.save().
  - Otherwise.
    - Evaluate Platform.msgprint(translated “No more children on Right”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [fetch or calculate](operations-021.md#op-343d3252a1b90b).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L4851) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L571) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L551)

<a id="op-a1674f387b05d0"></a>
### Bisect Accounting Statements.move up

`operation_enterprise_accounts_record_definitions_bisect_accounting_statements_business_behavior_bisect_accounting_statements_move_up`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bisect Nodes” via get\_doc.

**State and service calls** call save on self · msgprint with translated “Reached Root”.

**Local steps**

- If self.current\_node is distinct from no value.
  - Set cur\_node from Platform.get\_doc(“Bisect Nodes”, self.current\_node).
  - If cur\_node.root is distinct from no value.
    - Set root from Platform.get\_doc(“Bisect Nodes”, cur\_node.root).
    - Set self.current\_node from cur\_node.root.
    - Set self.current\_from\_date from root.period\_from\_date.
    - Set self.current\_to\_date from root.period\_to\_date.
    - Evaluate self.fetch\_or\_calculate().
    - Evaluate self.save().
  - Otherwise.
    - Evaluate Platform.msgprint(translated “Reached Root”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [fetch or calculate](operations-021.md#op-343d3252a1b90b).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L5197) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L579) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L559)

## Record · Budget

[Record definition](../../../../data/record-types/budget.json)

<a id="op-096869a3bd228d"></a>
### Budget.validate

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is mandatory”.format(self.budget\_against).

**Local steps**

- If not self.get(Platform.scrub(self.budget\_against)).
  - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(self.budget\_against)).
- Evaluate self.validate\_budget\_amount().
- Evaluate self.validate\_fiscal\_year().
- Evaluate self.set\_fiscal\_year\_dates().
- Evaluate self.validate\_duplicate().
- Evaluate self.validate\_account().
- Evaluate self.set\_null\_value().
- Evaluate self.validate\_applicable\_for().
- Evaluate self.validate\_existing\_expenses().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate budget amount](operations-021.md#op-e293cbd3e2e200), [validate fiscal year](operations-021.md#op-f92af047185928), [set fiscal year dates](operations-021.md#op-dfd0a1281eb3d0), [validate duplicate](operations-021.md#op-c6e8efd47148bd), [validate account](operations-021.md#op-7888bfbb458f91), [set null value](operations-021.md#op-4fd4dc8e0926cb), [validate applicable for](operations-021.md#op-f1177699f0ccad), [validate existing expenses](operations-022.md#op-6d17b282e632ae).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L6517) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L578)

<a id="op-e293cbd3e2e200"></a>
### Budget.validate budget amount

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_validate_budget_amount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Budget Amount can not be {0}.”.format(self.budget\_amount).

**Local steps**

- <a id="op-e293cbd3e2e200-guard-2"></a>If self.budget\_amount ≤ 0.
  - Call the validation error handler Platform.throw(translated “Budget Amount can not be {0}.”.format(self.budget\_amount)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.budget\_amount ≤ 0, self.budget\_amount = 0 selects the branch that calls the validation-error handler with translated “Budget Amount can not be {0}.”.format(self.budget\_amount). With self.budget\_amount = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e293cbd3e2e200-guard-2)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L6820) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L606) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L581)

<a id="op-f92af047185928"></a>
### Budget.validate fiscal year

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_validate_fiscal_year`

**Inputs** self.

**Local steps**

- If self.from\_fiscal\_year.
  - Evaluate self.validate\_fiscal\_year\_company(self.from\_fiscal\_year, self.company).
- If self.to\_fiscal\_year.
  - Evaluate self.validate\_fiscal\_year\_company(self.to\_fiscal\_year, self.company).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate fiscal year company](operations-021.md#op-bce1b6d0299c91).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L6937) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L585)

<a id="op-bce1b6d0299c91"></a>
### Budget.validate fiscal year company

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_validate_fiscal_year_company`

**Inputs** self, fiscal\_year, company.

**Record and data access** read “Fiscal Year Company” via get\_all.

**Explicit failure paths** validation helper — translated “Fiscal Year {0} is not available for Company {1}.”.format(fiscal\_year, company).

**Local steps**

- Set linked\_companies from Platform.get\_all(“Fiscal Year Company”, filters = mapping(“parent” → fiscal\_year), pluck = “company”).
- If (linked\_companies and company does not belong to linked\_companies).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in linked\_companies → company does not belong to linked\_companies.
  - Call the validation error handler Platform.throw(translated “Fiscal Year {0} is not available for Company {1}.”.format(fiscal\_year, company)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0031.json#L7069) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L586)

<a id="op-dfd0a1281eb3d0"></a>
### Budget.set fiscal year dates

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_set_fiscal_year_dates`

**Inputs** self.

**Record and data access** read “Fiscal Year” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “From Fiscal Year cannot be greater than To Fiscal Year”.

**Local steps**

- If self.from\_fiscal\_year.
  - Set self.budget\_start\_date from Platform.get\_cached\_value(“Fiscal Year”, self.from\_fiscal\_year, “year\_start\_date”).
- If self.to\_fiscal\_year.
  - Set self.budget\_end\_date from Platform.get\_cached\_value(“Fiscal Year”, self.to\_fiscal\_year, “year\_end\_date”).
- If self.budget\_start\_date &gt; self.budget\_end\_date.
  - Call the validation error handler Platform.throw(translated “From Fiscal Year cannot be greater than To Fiscal Year”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Fiscal Year”, self.from\_fiscal\_year, “year\_start\_date”), Platform.get\_cached\_value(“Fiscal Year”, self.to\_fiscal\_year, “year\_end\_date”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L598) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L573)

<a id="op-c6e8efd47148bd"></a>
### Budget.validate duplicate

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_validate_duplicate`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Explicit results** no value.

**Explicit failure paths** validation helper with DuplicateBudgetError — translated “Another Budget record '{0}' already exists against {1} '{2}' and account '{3}' with overlapping fiscal years.”.format(d.name, self.budget\_against, budget\_against, d.account).

**Local steps**

- Set budget\_against\_field from Platform.scrub(self.budget\_against).
- Set budget\_against from self.get(budget\_against\_field).
- Set account from self.account.
- If not account.
  - Return no value.
- Set existing\_budget from Platform.db.sql(formatted text   SELECT name, account  FROM ′tabBudget′  WHERE  docstatus &lt; 2  AND company = %s  AND {budget\_against\_field} = %s  AND account = %s , tuple(self.company, bu ….
- If existing\_budget.
  - Set d from existing\_budget at 0.
  - Call the validation error handler Platform.throw(translated “Another Budget record '{0}' already exists against {1} '{2}' and account '{3}' with overlapping fiscal years.”.format(d.name, self.budget\_against, budget\_against, d.account), Dup ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L583)

<a id="op-7888bfbb458f91"></a>
### Budget.validate account

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_validate_account`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Account is mandatory” · validation helper — translated “Budget cannot be assigned against Group Account {0}”.format(self.account) · validation helper — translated “Account {0} does not belong to company {1}”.format(self.account, self.company) · validation helper — translated “Budget cannot be assigned against {0}, as its Root Type is not of Income or Expense”.format(self.account).

**Local steps**

- If not self.account.
  - Call the validation error handler Platform.throw(translated “Account is mandatory”).
- Set account\_details from Platform.get\_cached\_value(“Account”, self.account, list(“is\_group”, “company”, “report\_type”), as\_dict = 1).
- If account\_details.is\_group.
  - Call the validation error handler Platform.throw(translated “Budget cannot be assigned against Group Account {0}”.format(self.account)).
- Otherwise.
  - If account\_details.company differs from self.company.
    - Call the validation error handler Platform.throw(translated “Account {0} does not belong to company {1}”.format(self.account, self.company)).
  - Otherwise.
    - If account\_details.report\_type differs from “Profit and Loss”.
      - Call the validation error handler Platform.throw(translated “Budget cannot be assigned against {0}, as its Root Type is not of Income or Expense”.format(self.account)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, list(“is\_group”, “company”, “report\_type”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L1024) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L604) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L579)

<a id="op-4fd4dc8e0926cb"></a>
### Budget.set null value

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_set_null_value`

**Inputs** self.

**Local steps**

- <a id="op-4fd4dc8e0926cb-guard-2"></a>If self.budget\_against equals “Cost Center”.
  - Set self.project from no value.
- Otherwise.
  - Set self.cost\_center from no value.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.budget\_against equals “Cost Center”, self.budget\_against = “Cost Center” selects the branch that assigns no value to self.project. With self.budget\_against = “Project”, the alternative assigns no value to self.cost\_center. [Local guard](#op-4fd4dc8e0926cb-guard-2)

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L1446) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L599) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L574)

<a id="op-f1177699f0ccad"></a>
### Budget.validate applicable for

`operation_enterprise_accounts_record_definitions_budget_business_behavior_budget_validate_applicable_for`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please enable Applicable on Purchase Order and Applicable on Booking Actual Expenses” · validation helper — translated “Please enable Applicable on Booking Actual Expenses”.

**Local steps**

- If (self.applicable\_on\_material\_request and not (self.applicable\_on\_purchase\_order and self.applicable\_on\_booking\_actual\_expenses)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.applicable\_on\_material\_request → not (self.applicable\_on\_purchase\_order and self.applicable\_on\_booking\_actual\_expenses).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.applicable\_on\_purchase\_order → self.applicable\_on\_booking\_actual\_expenses.
  - Call the validation error handler Platform.throw(translated “Please enable Applicable on Purchase Order and Applicable on Booking Actual Expenses”).
- Otherwise.
  - If (self.applicable\_on\_purchase\_order and not self.applicable\_on\_booking\_actual\_expenses).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.applicable\_on\_purchase\_order → not self.applicable\_on\_booking\_actual\_expenses.
    - Call the validation error handler Platform.throw(translated “Please enable Applicable on Booking Actual Expenses”).
  - Otherwise.
    - If not (self.applicable\_on\_material\_request or self.applicable\_on\_purchase\_order or self.applicable\_on\_booking\_actual\_expenses).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.applicable\_on\_material\_request → self.applicable\_on\_purchase\_order → self.applicable\_on\_booking\_actual\_expenses.
      - Set self.applicable\_on\_booking\_actual\_expenses from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0032.json#L1540) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L605) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L580)
