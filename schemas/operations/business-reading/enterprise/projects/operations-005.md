# Projects and time · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Project

[Record definition](../../../../data/record-types/project.json)

<a id="op-3703d7e8cef4a5"></a>
### Costing Summary.margins

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_costingsummary_margins`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“margin” → margin, “margin\_percent” → self.percent\_of(margin, self.billed), “planned\_margin” → (self.contract − self.estimate) when (self.contract and self.estimate), otherwise no value).

**Local steps**

- Set margin from (self.billed − self.cost).
- Return mapping(“margin” → margin, “margin\_percent” → self.percent\_of(margin, self.billed), “planned\_margin” → (self.contract − self.estimate) when (self.contract and self.estimate), otherwise no value).
  - Value choice on (self.contract and self.estimate) — true gives (self.contract − self.estimate), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.contract → self.estimate.

**Methods declared on this owner** [percent of](operations-005.md#op-c26c62c0180e15).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1232)

<a id="op-3a1e2dd03f01b7"></a>
### Costing Summary.is internal

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_costingsummary_is_internal`

**Inputs** self.

**Declared result** bool.

**Explicit results** (not self.project.customer and not self.contract and not self.billed).

**Local steps**

- Return (not self.project.customer and not self.contract and not self.billed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.project.customer → not self.contract → not self.billed.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L221) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1231)

<a id="op-c26c62c0180e15"></a>
### Costing Summary.percent of

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_costingsummary_percent_of`

**Inputs** amount, whole.

**Wrappers, in declaration order** staticmethod.

**Declared result** (float bitwise or no value).

**Explicit results** flt(((amount × 100) ÷ whole), 1) when whole, otherwise no value.

**Local steps**

- Return flt(((amount × 100) ÷ whole), 1) when whole, otherwise no value.
  - Value choice on whole — true gives flt(((amount × 100) ÷ whole), 1), false gives no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L223) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1233)

<a id="op-9bb86a9e8bda68"></a>
### Monthly rows

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_monthly_rows`

**Inputs** amounts.

**Declared result** list at dict.

**Explicit results** list() · list of mapping(“month” → month, expand mapping of source → flt(by\_month.get(month)) for tuple(source, by\_month) drawn from amounts.items()) for month drawn from month\_range(months at 0, months at negative 1).

**Local steps**

- Set months from sorted(set of month for months drawn from amounts.values(), then month drawn from months).
  - Draw months from amounts.values().
  - Draw month from months.
- If not months.
  - Return list().
- Return list of mapping(“month” → month, expand mapping of source → flt(by\_month.get(month)) for tuple(source, by\_month) drawn from amounts.items()) for month drawn from month\_range(months at 0, months at negative 1).
  - Draw month from month\_range(months at 0, months at negative 1).
  - Draw tuple(source, by\_month) from amounts.items().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1239)

<a id="op-031b8a2e55a772"></a>
### Month range

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_month_range`

**Inputs** first, last.

**Declared result** list at str.

**Explicit results** months.

**Local steps**

- Set tuple(month, end) from tuple(getdate((first + “-01”)), getdate((last + “-01”))).
- Set months from list().
- While month ≤ end.
  - Evaluate months.append(month.strftime(“%Y-%m”)).
  - Set month from getdate(add\_months(month, 1)).
- Return months.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1238)

<a id="op-86144d6eb95f4e"></a>
### Project Cost Queries.initialize

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_init`

**Inputs** self, project, readable\_only = false.

**Local steps**

- Set self.project from project.
- Set self.readable\_only from readable\_only.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1260)

<a id="op-f9399baeaa2f51"></a>
### Project Cost Queries.labour cost

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_labour_cost`

**Inputs** self, by\_month = false.

**Declared result** (float bitwise or MonthlyAmounts).

**Explicit results** sum\_amount(self.time\_logs(), detail.base\_costing\_amount, work\_date(detail), by\_month).

**Local steps**

- Set detail from qb.DocType(“Timesheet Detail”).
- Return sum\_amount(self.time\_logs(), detail.base\_costing\_amount, work\_date(detail), by\_month).

**Methods declared on this owner** [time logs](operations-005.md#op-c5ee9c55b11104).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L252) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1262)

<a id="op-51817dbbf0721c"></a>
### Project Cost Queries.labour hours

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_labour_hours`

**Inputs** self, by\_month = false.

**Declared result** (float bitwise or MonthlyAmounts).

**Explicit results** sum\_amount(self.time\_logs(), detail.hours, work\_date(detail), by\_month).

**Local steps**

- Set detail from qb.DocType(“Timesheet Detail”).
- Return sum\_amount(self.time\_logs(), detail.hours, work\_date(detail), by\_month).

**Methods declared on this owner** [time logs](operations-005.md#op-c5ee9c55b11104).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L253) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1263)

<a id="op-4f04e305499bc8"></a>
### Project Cost Queries.purchase cost

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_purchase_cost`

**Inputs** self, by\_month = false.

**Declared result** (float bitwise or MonthlyAmounts).

**Explicit results** combine(self.non\_stock\_purchase\_cost(by\_month), self.capitalised\_landed\_cost(by\_month), sign = negative 1).

**Local steps**

- Return combine(self.non\_stock\_purchase\_cost(by\_month), self.capitalised\_landed\_cost(by\_month), sign = negative 1).

**Methods declared on this owner** [non stock purchase cost](operations-005.md#op-2b97b03a70537e), [capitalised landed cost](operations-005.md#op-6abed87bc1d14f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L257) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1267)

<a id="op-416c14f28d6d5e"></a>
### Project Cost Queries.material cost

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_material_cost`

**Inputs** self, by\_month = false.

**Declared result** (float bitwise or MonthlyAmounts).

**Explicit results** combine(self.stock\_value\_consumed(by\_month), self.stock\_entry\_capitalised\_cost(by\_month)).

**Local steps**

- Return combine(self.stock\_value\_consumed(by\_month), self.stock\_entry\_capitalised\_cost(by\_month)).

**Methods declared on this owner** [stock value consumed](operations-005.md#op-8e8f9df00f2ca2), [stock entry capitalised cost](operations-005.md#op-43bafa64046638).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L254) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1264)

<a id="op-65be7c5ca8c7a0"></a>
### Project Cost Queries.billed amount

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_billed_amount`

**Inputs** self, by\_month = false.

**Declared result** (float bitwise or MonthlyAmounts).

**Explicit results** combine(sum\_amount(from\_invoice, item.base\_net\_amount, invoice.posting\_date, by\_month), sum\_amount(from\_item, item.base\_net\_amount, invoice.posting\_date, by\_month)).

**Local steps**

- Set invoice from qb.DocType(“Sales Invoice”).
- Set item from qb.DocType(“Sales Invoice Item”).
- Set tuple(from\_invoice, from\_item) from self.billed\_items().
- Return combine(sum\_amount(from\_invoice, item.base\_net\_amount, invoice.posting\_date, by\_month), sum\_amount(from\_item, item.base\_net\_amount, invoice.posting\_date, by\_month)).

**Methods declared on this owner** [billed items](operations-005.md#op-f54adfccc2f34e).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L245) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1255)

<a id="op-49e69339564d46"></a>
### Project Cost Queries.expense claim cost

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_expense_claim_cost`

**Inputs** self, by\_month = false.

**Declared result** (float bitwise or MonthlyAmounts).

**Explicit results** sum\_amount(self.expense\_claim\_rows(), detail.sanctioned\_amount, claim.posting\_date, by\_month).

**Local steps**

- Set claim from qb.DocType(“Expense Claim”).
- Set detail from qb.DocType(“Expense Claim Detail”).
- Return sum\_amount(self.expense\_claim\_rows(), detail.sanctioned\_amount, claim.posting\_date, by\_month).

**Methods declared on this owner** [expense claim rows](operations-005.md#op-42ae649b86e702).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1258)

<a id="op-8342d0104de7e8"></a>
### Project Cost Queries.sales order amount

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_sales_order_amount`

**Inputs** self.

**Declared result** float.

**Explicit results** sum\_amount(query, order.base\_net\_total).

**Local steps**

- Set order from qb.DocType(“Sales Order”).
- Set query from qb.from\_(order).where((order.project equals self.project bitwise and order.docstatus equals 1)).
- Return sum\_amount(query, order.base\_net\_total).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L258) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1268)

<a id="op-c5ee9c55b11104"></a>
### Project Cost Queries.time logs

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_time_logs`

**Inputs** self.

**Declared result** QueryBuilder.

**Explicit results** self.keep\_readable(query, detail.parent, “Timesheet”).

**Local steps**

- Set detail from qb.DocType(“Timesheet Detail”).
- Set query from qb.from\_(detail).where((detail.project equals self.project bitwise and detail.docstatus equals 1)).
- Return self.keep\_readable(query, detail.parent, “Timesheet”).

**Methods declared on this owner** [keep readable](operations-005.md#op-9d06464ef2496d).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L262) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1272)

<a id="op-2b97b03a70537e"></a>
### Project Cost Queries.non stock purchase cost

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_non_stock_purchase_cost`

**Inputs** self, by\_month.

**Declared result** (float bitwise or MonthlyAmounts).

**Explicit results** sum\_amount(query, invoice\_item.base\_net\_amount, invoice.posting\_date, by\_month).

**Local steps**

- Set invoice from qb.DocType(“Purchase Invoice”).
- Set invoice\_item from qb.DocType(“Purchase Invoice Item”).
- Set query from self.non\_stock\_purchase\_items().
- Return sum\_amount(query, invoice\_item.base\_net\_amount, invoice.posting\_date, by\_month).

**Methods declared on this owner** [non stock purchase items](operations-005.md#op-a71c43640d0c5d).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L255) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1265)

<a id="op-a71c43640d0c5d"></a>
### Project Cost Queries.non stock purchase items

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_non_stock_purchase_items`

**Inputs** self.

**Declared result** QueryBuilder.

**Explicit results** self.keep\_readable(query, invoice.name, “Purchase Invoice”).

**Local steps**

- Set invoice from qb.DocType(“Purchase Invoice”).
- Set invoice\_item from qb.DocType(“Purchase Invoice Item”).
- Set item from qb.DocType(“Item”).
- Set purchase\_order from qb.DocType(“Purchase Order”).
- Set never\_stocked from ((item.is\_stock\_item.isnull() bitwise or item.is\_stock\_item equals 0) bitwise or invoice\_item.delivered\_by\_supplier equals 1).
- Set not\_subcontracted from (purchase\_order.is\_subcontracted.isnull() bitwise or purchase\_order.is\_subcontracted equals 0).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.purchase\_order).where((invoice\_item.project equals self.project b ….
- Return self.keep\_readable(query, invoice.name, “Purchase Invoice”).

**Methods declared on this owner** [keep readable](operations-005.md#op-9d06464ef2496d).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L256) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1266)

<a id="op-6abed87bc1d14f"></a>
### Project Cost Queries.capitalised landed cost

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_capitalised_landed_cost`

**Inputs** self, by\_month.

**Declared result** (float bitwise or MonthlyAmounts).

**Explicit results** total.

**Local steps**

- Set total from mapping() when by\_month, otherwise 0.0.
  - Value choice on by\_month — true gives mapping(), false gives 0.0.
- For each tuple(row\_doctype, parent\_doctype) in LANDED\_COST\_RECEIPTS.items().
  - Set row from qb.DocType(row\_doctype).
  - Set parent from qb.DocType(parent\_doctype).
  - Set query from nested operand in the contract(nested operand in the contract).join(parent).on(parent.name equals row.parent).where((row.project equals self.project bitwise and row.docstatus equals 1)).
  - Set total from combine(total, sum\_amount(query, row.landed\_cost\_voucher\_amount, parent.posting\_date, by\_month)).
- Return total.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1257)

<a id="op-8e8f9df00f2ca2"></a>
### Project Cost Queries.stock value consumed

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_stock_value_consumed`

**Inputs** self, by\_month.

**Declared result** (float bitwise or MonthlyAmounts).

**Explicit results** sum\_amount(query, (ledger.stock\_value\_difference × negative 1), ledger.posting\_date, by\_month).

**Local steps**

- Set ledger from qb.DocType(“Stock Ledger Entry”).
- Set query from self.stock\_consumption\_entries().
- Return sum\_amount(query, (ledger.stock\_value\_difference × negative 1), ledger.posting\_date, by\_month).

**Methods declared on this owner** [stock consumption entries](operations-005.md#op-9a1c509dd6333f).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L261) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1271)

<a id="op-9a1c509dd6333f"></a>
### Project Cost Queries.stock consumption entries

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_stock_consumption_entries`

**Inputs** self.

**Declared result** QueryBuilder.

**Explicit results** self.keep\_readable(query, ledger.name, “Stock Ledger Entry”).

**Local steps**

- Set ledger from qb.DocType(“Stock Ledger Entry”).
- Set stock\_entry from qb.DocType(“Stock Entry”).
- Set query from nested operand in the contract(nested operand in the contract).left\_join(stock\_entry).on((ledger.voucher\_type equals “Stock Entry” bitwise and stock\_entry.name equals ledger.voucher\_no)).where((((ledger.pr ….
- Return self.keep\_readable(query, ledger.name, “Stock Ledger Entry”).

**Methods declared on this owner** [keep readable](operations-005.md#op-9d06464ef2496d).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L259) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1269)

<a id="op-43bafa64046638"></a>
### Project Cost Queries.stock entry capitalised cost

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_stock_entry_capitalised_cost`

**Inputs** self, by\_month.

**Declared result** (float bitwise or MonthlyAmounts).

**Explicit results** sum\_amount(query, amount, stock\_entry.posting\_date, by\_month).

**Local steps**

- Set stock\_entry from qb.DocType(“Stock Entry”).
- Set row from qb.DocType(“Stock Entry Detail”).
- Set query from nested operand in the contract(nested operand in the contract).join(stock\_entry).on(stock\_entry.name equals row.parent).where(((row.project equals self.project bitwise and stock\_entry.docstatus equals 1) b ….
- Set amount from (row.additional\_cost + row.landed\_cost\_voucher\_amount).
- Return sum\_amount(query, amount, stock\_entry.posting\_date, by\_month).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L260) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1270)

<a id="op-f54adfccc2f34e"></a>
### Project Cost Queries.billed items

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_billed_items`

**Inputs** self.

**Declared result** tuple at tuple(QueryBuilder, QueryBuilder).

**Explicit results** tuple(from\_invoice, from\_item).

**Local steps**

- Set invoice from qb.DocType(“Sales Invoice”).
- Set item from qb.DocType(“Sales Invoice Item”).
- Set items from qb.from\_(item).join(invoice).on(invoice.name equals item.parent).
- Set from\_invoice from items.where(((item.project.isnull() bitwise and invoice.project equals self.project) bitwise and invoice.docstatus equals 1)).
- Set from\_item from items.where((item.project equals self.project bitwise and item.docstatus equals 1)).
- Return tuple(from\_invoice, from\_item).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1256)

<a id="op-42ae649b86e702"></a>
### Project Cost Queries.expense claim rows

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_expense_claim_rows`

**Inputs** self.

**Declared result** QueryBuilder.

**Explicit results** nested operand in the contract(nested operand in the contract).join(claim).on(claim.name equals detail.parent).where((claim.docstatus equals 1 bitwise and Coalesce(NullIf(detail.project, empty text), claim ….

**Local steps**

- Set claim from qb.DocType(“Expense Claim”).
- Set detail from qb.DocType(“Expense Claim Detail”).
- Return nested operand in the contract(nested operand in the contract).join(claim).on(claim.name equals detail.parent).where((claim.docstatus equals 1 bitwise and Coalesce(NullIf(detail.project, empty text), claim ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1259)

<a id="op-9d06464ef2496d"></a>
### Project Cost Queries.keep readable

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_projectcostqueries_keep_readable`

**Inputs** self, query, document, doctype.

**Declared result** QueryBuilder.

**Explicit results** query · query.where(document.isin(readable)).

**Local steps**

- If not self.readable\_only.
  - Return query.
- Set readable from Platform.qb.get\_query(doctype, fields = list(“name”), ignore\_permissions = false).
- Return query.where(document.isin(readable)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L251) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1261)

<a id="op-91529bed114d55"></a>
### Sum by

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_queries_sum_by`

**Inputs** query, group, amount.

**Declared result** dict at tuple(str, float).

**Explicit results** mapping of row.group\_value → flt(row.amount) for row drawn from rows.

**Local steps**

- Set rows from query.select(nested operand in the contract.as\_(“group\_value”), nested operand in the contract.as\_(“amount”)).groupby(group).run(as\_dict = true).
- Return mapping of row.group\_value → flt(row.amount) for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L264) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1274)
