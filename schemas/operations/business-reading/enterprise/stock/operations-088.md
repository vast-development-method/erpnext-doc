# Inventory and warehouses · operations 88

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Stock ledger

<a id="op-82380f8ba6f8b2"></a>
### Get sle conditions

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_stock_ledger_entry_conditions`

**Inputs** filters.

**Explicit results** “and {}”.format(“ and ”.join(conditions)) when conditions, otherwise empty text.

**Local steps**

- Set conditions from list().
- If filters.get(“warehouse”).
  - Set warehouse\_condition from get\_warehouse\_condition(filters.get(“warehouse”)).
  - If warehouse\_condition.
    - Evaluate conditions.append(warehouse\_condition).
- If filters.get(“voucher\_no”).
  - Evaluate conditions.append(“voucher\_no=%(voucher\_no)s”).
- If filters.get(“batch\_no”).
  - Evaluate conditions.append(“batch\_no=%(batch\_no)s”).
- If filters.get(“project”).
  - Evaluate conditions.append(“project=%(project)s”).
- For each dimension in get\_inventory\_dimensions().
  - If filters.get(dimension.fieldname).
    - Evaluate conditions.append(formatted text {dimension.fieldname} in %({dimension.fieldname})s).
- Return “and {}”.format(“ and ”.join(conditions)) when conditions, otherwise empty text.
  - Value choice on conditions — true gives “and {}”.format(“ and ”.join(conditions)), false gives empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0917.json#L5486) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L914) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L519)

<a id="op-21c8ea879eda53"></a>
### Get opening balance from batch

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_opening_balance_from_batch`

**Inputs** filters, columns, sl\_entries.

**Record and data access** read “Batch” via get\_value · read “Stock Ledger Entry” via get\_all.

**Explicit results** mapping(“item\_code” → translated “'Opening'”, “qty\_after\_transaction” → 0.0, “valuation\_rate” → 0.0, “stock\_value” → 0.0) · mapping(“item\_code” → translated “'Opening'”, “qty\_after\_transaction” → opening\_data.qty\_after\_transaction, “valuation\_rate” → opening\_data.valuation\_rate, “stock\_value” → opening\_data.stock\_value).

**Local steps**

- Set batch\_item from Platform.db.get\_value(“Batch”, filters.batch\_no, “item”).
- If (batch\_item and not Platform.has\_permission(“Item”, “read”, batch\_item)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_item → not Platform.has\_permission(“Item”, “read”, batch\_item).
  - Return mapping(“item\_code” → translated “'Opening'”, “qty\_after\_transaction” → 0.0, “valuation\_rate” → 0.0, “stock\_value” → 0.0).
- Set query\_filters from mapping(“batch\_no” → filters.batch\_no, “docstatus” → 1, “is\_cancelled” → 0, “posting\_date” → tuple(“&lt;”, filters.from\_date), …).
- If value bound to filters.get(“item\_code”).
  - Set query\_filters at “item\_code” from tuple(“in”, value).
- Set warehouses from get\_matching\_warehouses(filters.get(“warehouse”)).
- If warehouses.
  - Set query\_filters at “warehouse” from tuple(“in”, warehouses).
- Set opening\_data from Platform.get\_all(“Stock Ledger Entry”, fields = list(mapping(“SUM” → “actual\_qty”, “as” → “qty\_after\_transaction”), mapping(“SUM” → “stock\_value\_difference”, “as” → “stock\_value”)), filters = query\_filters) at 0.
- For each field in list(“qty\_after\_transaction”, “stock\_value”, “valuation\_rate”).
  - If opening\_data.get(field) is identical to no value.
    - Set opening\_data at field from 0.0.
- Set table from Platform.qb.DocType(“Stock Ledger Entry”).
- Set sabb\_table from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.serial\_and\_batch\_bundle equals nested operand in the contract.parent).select(Sum(nested operand in the contr ….
- If warehouses.
  - Set query from query.where(table.warehouse.isin(warehouses)).
- For each field in list(“item\_code”, “company”).
  - Set value from filters.get(field).
  - If not value.
    - Continue with the next iteration or loop test.
  - If isinstance(value, (list bitwise or tuple)).
    - Set query from query.where(table at field.isin(value)).
  - Otherwise.
    - Set query from query.where(table at field equals value).
- Set bundle\_data from query.run(as\_dict = true).
- If bundle\_data.
  - Update opening\_data.qty\_after\_transaction using + flt(bundle\_data at 0.qty).
  - Update opening\_data.stock\_value using + flt(bundle\_data at 0.stock\_value).
  - If opening\_data.qty\_after\_transaction.
    - Set opening\_data.valuation\_rate from (flt(opening\_data.stock\_value) ÷ flt(opening\_data.qty\_after\_transaction)).
- Return mapping(“item\_code” → translated “'Opening'”, “qty\_after\_transaction” → opening\_data.qty\_after\_transaction, “valuation\_rate” → opening\_data.valuation\_rate, “stock\_value” → opening\_data.stock\_value).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “read”, batch\_item).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L909) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L514)

<a id="op-f0de796e72a30a"></a>
### Get opening balance

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_opening_balance`

**Inputs** filters, columns, sl\_entries, inv\_dimension\_wise\_value = no value.

**Explicit results** no value · mapping(“item\_code” → translated “'Opening'”, “qty\_after\_transaction” → total\_qty, “valuation\_rate” → valuation\_rate, “stock\_value” → total\_stock\_value).

**Local steps**

- If not (filters.item\_code and filters.warehouse and filters.from\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.item\_code → filters.warehouse → filters.from\_date.
  - Return no value.
- Set item\_codes from filters.item\_code.
- If isinstance(item\_codes, str).
  - Set item\_codes from list(item\_codes).
- Set warehouses from get\_matching\_warehouses(filters.warehouse).
- If not warehouses.
  - Return no value.
- Set sle\_doctype from Platform.qb.DocType(“Stock Ledger Entry”).
- Set sr\_doctype from Platform.qb.DocType(“Stock Reconciliation”).
- Set opening\_reco\_query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.voucher\_type equals “Stock Reconciliation”).where(sle\_doctype.posting\_date equals filters.from\_date).wher ….
- Set opening\_reco\_vouchers from set(opening\_reco\_query.run(pluck = true)).
- If opening\_reco\_vouchers.
  - Set sl\_entries at slice no value to no value from list of sle for sle drawn from sl\_entries where sle.get(“voucher\_no”) does not belong to opening\_reco\_vouchers.
    - Draw sle from sl\_entries, keep a combination only if (sle.get(“voucher\_no”) does not belong to opening\_reco\_vouchers).
- Set sle\_cond from sle\_doctype.posting\_date &lt; filters.from\_date.
- If opening\_reco\_vouchers.
  - Set sle\_cond from (sle\_cond bitwise or (sle\_doctype.posting\_date equals filters.from\_date bitwise and sle\_doctype.voucher\_no.isin(list(opening\_reco\_vouchers)))).
- Set subq from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isin(item\_codes)).where(sle\_doctype.warehouse.isin(warehouses)).where(sle\_cond).
- For each field in list(“voucher\_no”, “project”, “company”).
  - If filters.get(field).
    - Set subq from subq.where(sle\_doctype at field equals filters.get(field)).
- Set inventory\_dimension\_fields from get\_inventory\_dimension\_fields().
- If inventory\_dimension\_fields.
  - For each fieldname in inventory\_dimension\_fields.
    - If filters.get(fieldname).
      - Set subq from subq.where(sle\_doctype at fieldname.isin(filters.get(fieldname))).
- Set query from nested operand in the contract.qb.from\_(subq).select(IfNull(nested operand in the contract(nested operand in the contract), 0.0).as\_(“total\_qty”), IfNull(nested operand in the contract(nested operand in th ….
- Set res from query.run(as\_dict = true).
- Set total\_qty from flt(res at 0.total\_qty) when res, otherwise 0.0.
  - Value choice on res — true gives flt(res at 0.total\_qty), false gives 0.0.
- Set total\_stock\_value from flt(res at 0.total\_stock\_value) when res, otherwise 0.0.
  - Value choice on res — true gives flt(res at 0.total\_stock\_value), false gives 0.0.
- Set valuation\_rate from flt((total\_stock\_value ÷ total\_qty)) when total\_qty, otherwise 0.0.
  - Value choice on total\_qty — true gives flt((total\_stock\_value ÷ total\_qty)), false gives 0.0.
- Return mapping(“item\_code” → translated “'Opening'”, “qty\_after\_transaction” → total\_qty, “valuation\_rate” → valuation\_rate, “stock\_value” → total\_stock\_value).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L907) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L512)

<a id="op-04ef5296fcca17"></a>
### Apply permitted warehouses

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_stock_ledger_apply_permitted_warehouses`

**Inputs** filters.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** true · bool(filters.warehouse).

**Local steps**

- Set permitted from get\_allowed\_docs\_for\_doctype(get\_user\_permissions().get(“Warehouse”, list()), “Stock Ledger Entry”).
- If not permitted.
  - Return true.
- If filters.get(“warehouse”).
  - Set selected from set(get\_matching\_warehouses(filters.warehouse)).
  - Set permitted from list of warehouse for warehouse drawn from permitted where warehouse belongs to selected.
    - Draw warehouse from permitted, keep a combination only if (warehouse belongs to selected).
- Set filters.warehouse from Platform.get\_all(“Warehouse”, filters = mapping(“name” → tuple(“in”, (permitted or list(empty text))), “is\_group” → 0), pluck = “name”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in permitted → list(empty text).
- Return bool(filters.warehouse).

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1553) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1050)

<a id="op-855fbf5d958381"></a>
### Get matching warehouses

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_matching_warehouses`

**Inputs** warehouses.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** list() · warehouses · matching when matching, otherwise warehouses.

**Local steps**

- If not warehouses.
  - Return list().
- If isinstance(warehouses, str).
  - Set warehouses from list(warehouses).
- Set warehouse\_details from Platform.get\_all(“Warehouse”, filters = mapping(“name” → tuple(“in”, warehouses)), fields = list(“lft”, “rgt”)).
- If not warehouse\_details.
  - Return warehouses.
- Set wh from Platform.qb.DocType(“Warehouse”).
- Set cond from no value.
- For each d in warehouse\_details.
  - Set c from (wh.lft ≥ d.lft bitwise and wh.rgt ≤ d.rgt).
  - Set cond from c when cond is identical to no value, otherwise (cond bitwise or c).
    - Value choice on cond is identical to no value — true gives c, false gives (cond bitwise or c).
- Set matching from nested operand in the contract(nested operand in the contract).select(wh.name).where(cond).run(pluck = true).
- Return matching when matching, otherwise warehouses.
  - Value choice on matching — true gives matching, false gives warehouses.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0918.json#L3353) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L906) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L511)

<a id="op-dc193c71c8e43c"></a>
### Get warehouse condition

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_warehouse_condition`

**Inputs** warehouses.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** empty text · formatted text  exists (select name from ′tabWarehouse′ {alias}  where ({conditions}) and warehouse = {alias}.name).

**Local steps**

- If not warehouses.
  - Return empty text.
- If isinstance(warehouses, str).
  - Set warehouses from list(warehouses).
- Set warehouse\_range from Platform.get\_all(“Warehouse”, filters = mapping(“name” → tuple(“in”, warehouses)), fields = list(“lft”, “rgt”), as\_list = true).
- If not warehouse\_range.
  - Return empty text.
- Set alias from “wh”.
- Set conditions from list().
- For each tuple(lft, rgt) in warehouse\_range.
  - Evaluate conditions.append(formatted text ({alias}.lft &gt;= {lft} and {alias}.rgt &lt;= {rgt})).
- Set conditions from “ or ”.join(conditions).
- Return formatted text  exists (select name from ′tabWarehouse′ {alias}  where ({conditions}) and warehouse = {alias}.name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0918.json#L3858) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L915) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L520)

<a id="op-310ff822d3a9e0"></a>
### Get item group condition

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_item_group_condition`

**Inputs** item\_group, item\_table = no value.

**Record and data access** read “Item Group” via get\_value.

**Explicit results** item\_table.item\_group.isin(nested operand in the contract.from\_(ig).select(ig.name).where(((ig.lft ≥ item\_group\_details.lft bitwise and ig.rgt ≤ item\_group\_details.rgt) bitwise and item\_table.item\_group eq … · formatted text item.item\_group in (select ig.name from ′tabItem Group′ ig  where ig.lft &gt;= {item\_group\_details.lft} and ig.rgt &lt;= {item\_group\_details.rgt} and ite.

**Local steps**

- Set item\_group\_details from Platform.db.get\_value(“Item Group”, item\_group, list(“lft”, “rgt”), as\_dict = 1).
- If item\_group\_details.
  - If item\_table.
    - Set ig from Platform.qb.DocType(“Item Group”).
    - Return item\_table.item\_group.isin(nested operand in the contract.from\_(ig).select(ig.name).where(((ig.lft ≥ item\_group\_details.lft bitwise and ig.rgt ≤ item\_group\_details.rgt) bitwise and item\_table.item\_group eq ….
  - Otherwise.
    - Return formatted text item.item\_group in (select ig.name from ′tabItem Group′ ig  where ig.lft &gt;= {item\_group\_details.lft} and ig.rgt &lt;= {item\_group\_details.rgt} and ite.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0918.json#L4340) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L904) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L509)

<a id="op-ca90a55566d1a9"></a>
### Get opening balance for inv dimension

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_opening_balance_for_invoice_dimension`

**Inputs** filters, inv\_dimension\_wise\_value, items = no value.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- If not filters.from\_date.
  - Return list().
- Set sl\_doctype from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sl\_doctype.item\_code, sl\_doctype.warehouse, nested operand in the contract.as\_(“qty\_after\_transaction”), nested operand in the contract ….
- If items.
  - Set query from query.where(sl\_doctype.item\_code.isin(items)).
- Otherwise.
  - Set permitted\_items from Platform.qb.get\_query(“Item”, fields = list(“name”), ignore\_permissions = false).
  - Set query from query.where(sl\_doctype.item\_code.isin(permitted\_items)).
- If warehouses bound to get\_matching\_warehouses(filters.get(“warehouse”)).
  - Set query from query.where(sl\_doctype.warehouse.isin(warehouses)).
- If filters.get(“company”).
  - Set query from query.where(sl\_doctype.company equals filters.company).
- For each tuple(key, value) in inv\_dimension\_wise\_value.items().
  - If isinstance(value, (list bitwise or tuple)).
    - Set query from query.where(sl\_doctype at key.isin(value)).
  - Otherwise.
    - Set query from query.where(sl\_doctype at key equals value).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L908) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L513)

<a id="op-91be8a3e258b65"></a>
### Get inv dimension opening row

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_stock_ledger_get_inv_dimension_opening_row`

**Inputs** inv\_dimension\_opening.

**Explicit results** Platform.\_dict(mapping()) · Platform.\_dict(mapping(“item\_code” → translated “'Opening'”, “qty\_after\_transaction” → qty, “stock\_value” → stock\_value, “valuation\_rate” → (stock\_value ÷ qty) when qty, otherwise 0)).

**Local steps**

- If not inv\_dimension\_opening.
  - Return Platform.\_dict(mapping()).
- Set qty from sum(generator of flt(row.qty\_after\_transaction) for row drawn from inv\_dimension\_opening).
  - Draw row from inv\_dimension\_opening.
- Set stock\_value from sum(generator of flt(row.stock\_value) for row drawn from inv\_dimension\_opening).
  - Draw row from inv\_dimension\_opening.
- Return Platform.\_dict(mapping(“item\_code” → translated “'Opening'”, “qty\_after\_transaction” → qty, “stock\_value” → stock\_value, “valuation\_rate” → (stock\_value ÷ qty) when qty, otherwise 0)).
  - Value choice on qty — true gives (stock\_value ÷ qty), false gives 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1554) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1051)

<a id="op-0c4eba7ba96b99"></a>
### Get inv dimension wise value

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_invoice_dimension_wise_value`

**Inputs** filters.

**Declared result** list.

**Record and data access** read “Inventory Dimension” via get\_all.

**Explicit results** inv\_dimension\_key.

**Local steps**

- Set inv\_dimension\_key from Platform.\_dict(mapping()).
- For each dimension in get\_inventory\_dimensions().
  - If (dimension.fieldname belongs to filters and filters.get(dimension.fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in dimension.fieldname belongs to filters → filters.get(dimension.fieldname).
    - Set inv\_dimension\_key at dimension.fieldname from filters.get(dimension.fieldname).
- If (filters.get(“project”) and not Platform.get\_all(“Inventory Dimension”, filters = mapping(“reference\_document” → “Project”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“project”) → not Platform.get\_all(“Inventory Dimension”, filters = mapping(“reference\_document” → “Project”)).
  - Set inv\_dimension\_key at “project” from filters.get(“project”).
- Return inv\_dimension\_key.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0918.json#L5965) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L902) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L507)

## Service · Stock ledger

<a id="op-d80bf06423faed"></a>
### Repost Queue.initialize

`operation_enterprise_binding_enterprise_stock_stock_ledger_repostqueue_init`

**Inputs** self, sles = no value.

**Local steps**

- Set self.\_heap from list().
- Set self.\_counter from count().
- Evaluate self.extend((sles or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sles → list().

If control reaches the end, it returns no value.

**Methods declared on this owner** [extend](operations-088.md#op-c0f10d277a5998).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1606) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1103)

<a id="op-c0f10d277a5998"></a>
### Repost Queue.extend

`operation_enterprise_binding_enterprise_stock_stock_ledger_repostqueue_extend`

**Inputs** self, sles.

**Local steps**

- For each sle in sles.
  - Set key from tuple(get\_datetime(sle.posting\_datetime), get\_datetime(sle.creation), next(self.\_counter)).
  - Evaluate heappush(self.\_heap, tuple(expanded key, sle)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1604) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1101)

<a id="op-380c21c648db06"></a>
### Repost Queue.popleft

`operation_enterprise_binding_enterprise_stock_stock_ledger_repostqueue_popleft`

**Inputs** self.

**Explicit results** heappop(self.\_heap) at negative 1.

**Local steps**

- Return heappop(self.\_heap) at negative 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1106)

<a id="op-c036144b9baf13"></a>
### Repost Queue.first

`operation_enterprise_binding_enterprise_stock_stock_ledger_repostqueue_first`

**Inputs** self.

**Explicit results** self.\_heap at 0 at negative 1.

**Local steps**

- Return self.\_heap at 0 at negative 1.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1605) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1102)

<a id="op-04d652d5c17b59"></a>
### Repost Queue.peek

`operation_enterprise_binding_enterprise_stock_stock_ledger_repostqueue_peek`

**Inputs** self, n.

**Explicit results** list of entry at negative 1 for entry drawn from nsmallest(n, self.\_heap).

**Local steps**

- Return list of entry at negative 1 for entry drawn from nsmallest(n, self.\_heap).
  - Draw entry from nsmallest(n, self.\_heap).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1105)

<a id="op-6df7d256ce7616"></a>
### Repost Queue.len

`operation_enterprise_binding_enterprise_stock_stock_ledger_repostqueue_len`

**Inputs** self.

**Explicit results** len(self.\_heap).

**Local steps**

- Return len(self.\_heap).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1104)

<a id="op-2e683d64e8d633"></a>
### Validate stock frozen by closing entry

`operation_enterprise_stock_stock_ledger_business_behavior_validate_stock_frozen_by_closing_entry`

**Inputs** sl\_entries.

**Record and data access** read “Warehouse” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Stock transactions dated on or before {0} are frozen because the period is closed and the Stock Closing Entr …”.format(Platform.bold(format\_date(closing\_entry.to\_date)), get\_link\_to\_form(“Stock ….

**Local steps**

- Bind dependencies get\_closing\_entry\_for\_closed\_period.
- Set company from sl\_entries at 0.get(“company”).
- If not company.
  - Set company from Platform.get\_cached\_value(“Warehouse”, sl\_entries at 0.get(“warehouse”), “company”).
- Set closing\_entry from get\_closing\_entry\_for\_closed\_period(company).
- If not closing\_entry.
  - Return no value.
- For each sle in sl\_entries.
  - If (sle.get(“posting\_date”) and getdate(sle.get(“posting\_date”)) ≤ getdate(closing\_entry.to\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.get(“posting\_date”) → getdate(sle.get(“posting\_date”)) ≤ getdate(closing\_entry.to\_date).
    - Call the validation error handler Platform.throw(translated “Stock transactions dated on or before {0} are frozen because the period is closed and the Stock Closing Entr …”.format(Platform.bold(format\_date(closing\_entry.to\_date)), get\_link ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, sl\_entries at 0.get(“warehouse”), “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0935.json#L4885) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L803)

<a id="op-a8b1ff1436b6f4"></a>
### Mark stock closing outdated

`operation_enterprise_binding_enterprise_stock_stock_ledger_mark_stock_closing_outdated`

**Inputs** sl\_entries.

**Record and data access** read “Warehouse” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- Bind dependencies has\_closing\_entry\_to\_coordinate, lock\_company\_for\_closing, mark\_closing\_entries\_outdated.
- Set company from sl\_entries at 0.get(“company”).
- If not company.
  - Set company from Platform.get\_cached\_value(“Warehouse”, sl\_entries at 0.get(“warehouse”), “company”).
- Set posting\_dates from list of getdate(sle.get(“posting\_date”)) for sle drawn from sl\_entries where sle.get(“posting\_date”).
  - Draw sle from sl\_entries, keep a combination only if (sle.get(“posting\_date”)).
- If not posting\_dates.
  - Return no value.
- If has\_closing\_entry\_to\_coordinate(company, min(posting\_dates)).
  - Evaluate lock\_company\_for\_closing(company).
- Evaluate mark\_closing\_entries\_outdated(company, min(posting\_dates)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, sl\_entries at 0.get(“warehouse”), “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1099)

<a id="op-91f9dbe04e261b"></a>
### Make sl entries

`operation_enterprise_stock_stock_ledger_business_behavior_make_stock_ledger_entries`

**Inputs** sl\_entries, allow\_negative\_stock = false, via\_landed\_cost\_voucher = false, defer\_dimension\_checks = false.

**Record and data access** read “Item” via get\_cached\_value · read “Bin” via get\_value.

**State and service calls** msgprint with translated “Item {0} ignored since it is not a stock item”.format(args.get(“item\_code”)).

**Local steps**

- Bind dependencies future\_sle\_exists, invalidate\_future\_sle\_cache.
- If sl\_entries.
  - Evaluate validate\_stock\_frozen\_by\_closing\_entry(sl\_entries).
  - Evaluate mark\_stock\_closing\_outdated(sl\_entries).
  - Set cancelled from sl\_entries at 0.get(“is\_cancelled”).
  - If cancelled.
    - Evaluate validate\_cancellation(sl\_entries).
    - Evaluate set\_as\_cancel(sl\_entries at 0.get(“voucher\_type”), sl\_entries at 0.get(“voucher\_no”)).
  - Set args from get\_args\_for\_future\_sle(sl\_entries at 0).
  - Evaluate invalidate\_future\_sle\_cache(args.voucher\_type, args.voucher\_no).
  - Evaluate future\_sle\_exists(args, sl\_entries).
  - Set sle\_docs from list().
  - For each sle in sl\_entries.
    - If cancelled.
      - Set sle at “actual\_qty” from negative flt(sle.get(“actual\_qty”)).
      - If (sle at “actual\_qty” &lt; 0 and not sle.get(“outgoing\_rate”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle at “actual\_qty” &lt; 0 → not sle.get(“outgoing\_rate”).
        - Set sle at “outgoing\_rate” from get\_incoming\_outgoing\_rate\_for\_cancel(sle.item\_code, sle.voucher\_type, sle.voucher\_no, sle.voucher\_detail\_no).
        - Set sle at “incoming\_rate” from 0.0.
      - If (sle at “actual\_qty” &gt; 0 and not sle.get(“incoming\_rate”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle at “actual\_qty” &gt; 0 → not sle.get(“incoming\_rate”).
        - Set sle at “incoming\_rate” from get\_incoming\_outgoing\_rate\_for\_cancel(sle.item\_code, sle.voucher\_type, sle.voucher\_no, sle.voucher\_detail\_no).
        - Set sle at “outgoing\_rate” from 0.0.
    - If not (sle.get(“actual\_qty”) or sle.get(“voucher\_type”) equals “Stock Reconciliation”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.get(“actual\_qty”) → sle.get(“voucher\_type”) equals “Stock Reconciliation”.
      - Continue with the next iteration or loop test.
    - Set sle\_doc from make\_entry(sle, allow\_negative\_stock, via\_landed\_cost\_voucher, defer\_future\_dimension\_check = true).
    - Evaluate sle\_docs.append(sle\_doc).
    - Set args from sle\_doc.as\_dict().
    - Set args at “posting\_datetime” from get\_combine\_datetime(args.posting\_date, args.posting\_time).
    - If sle.get(“voucher\_type”) equals “Stock Reconciliation”.
      - Set args.previous\_qty\_after\_transaction from sle.get(“previous\_qty\_after\_transaction”).
    - Set is\_stock\_item from Platform.get\_cached\_value(“Item”, args.get(“item\_code”), “is\_stock\_item”).
    - If is\_stock\_item.
      - Set bin\_name from get\_or\_make\_bin(args.get(“item\_code”), args.get(“warehouse”)).
      - Set args.reserved\_stock from flt(Platform.db.get\_value(“Bin”, bin\_name, “reserved\_stock”)).
      - Evaluate repost\_current\_voucher(args, allow\_negative\_stock, via\_landed\_cost\_voucher, cancelled = cancelled).
      - Evaluate update\_bin\_qty(bin\_name, args).
    - Otherwise.
      - Evaluate Platform.msgprint(translated “Item {0} ignored since it is not a stock item”.format(args.get(“item\_code”))).
  - Evaluate validate\_future\_dimension\_balances(sle\_docs, defer = defer\_dimension\_checks).
  - Evaluate invalidate\_future\_sle\_cache(sl\_entries at 0.get(“voucher\_type”), sl\_entries at 0.get(“voucher\_no”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, args.get(“item\_code”), “is\_stock\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L739)

<a id="op-2165631fc1bf05"></a>
### Validate future dimension balances

`operation_enterprise_binding_enterprise_stock_stock_ledger_validate_future_dimension_balances`

**Inputs** sle\_docs, defer = false.

**Explicit results** no value.

**Local steps**

- If not sle\_docs.
  - Return no value.
- Set tuple(voucher\_type, voucher\_no) from tuple(sle\_docs at 0.voucher\_type, sle\_docs at 0.voucher\_no).
- Evaluate get\_pending\_dimension\_checks().setdefault(tuple(voucher\_type, voucher\_no), list()).extend(sle\_docs).
- If not defer.
  - Evaluate run\_pending\_dimension\_checks(voucher\_type, voucher\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1633) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1130)

<a id="op-a728711763fa19"></a>
### Run pending dimension checks

`operation_enterprise_binding_enterprise_stock_stock_ledger_run_pending_dimension_checks`

**Inputs** voucher\_type, voucher\_no.

**Local steps**

- For each sle\_doc in get\_pending\_dimension\_checks().pop(tuple(voucher\_type, voucher\_no), list()).
  - Evaluate sle\_doc.validate\_future\_dimension\_balance\_after\_voucher().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1107)

<a id="op-7c8aecae54b502"></a>
### Get pending dimension checks

`operation_enterprise_binding_enterprise_stock_stock_ledger_get_pending_dimension_checks`

**Inputs** no declared parameters.

**Explicit results** Platform.local.pending\_dimension\_checks.

**Local steps**

- If not getattr(Platform.local, “pending\_dimension\_checks”, no value).
  - Set Platform.local.pending\_dimension\_checks from mapping().
- Return Platform.local.pending\_dimension\_checks.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “pending\_dimension\_checks”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1088)

<a id="op-12e4a551ac3ad7"></a>
### Repost current voucher

`operation_enterprise_stock_stock_ledger_business_behavior_repost_current_voucher`

**Inputs** args, allow\_negative\_stock = false, via\_landed\_cost\_voucher = false, cancelled = false.

**Local steps**

- If (args.get(“actual\_qty”) or args.get(“voucher\_type”) equals “Stock Reconciliation”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“actual\_qty”) → args.get(“voucher\_type”) equals “Stock Reconciliation”.
  - If not args.get(“posting\_date”).
    - Set args at “posting\_date” from nowdate().
  - If not (args.get(“is\_cancelled”) and via\_landed\_cost\_voucher).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“is\_cancelled”) → via\_landed\_cost\_voucher.
    - Evaluate update\_entries\_after(mapping(“item\_code” → args.get(“item\_code”), “warehouse” → args.get(“warehouse”), “posting\_date” → args.get(“posting\_date”), “posting\_time” → args.get(“posting\_time”), …), allow\_negati ….
  - Evaluate update\_qty\_in\_future\_sle(args, allow\_negative\_stock).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0936.json#L1566) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1226) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L740)

<a id="op-3520afeefb4b4a"></a>
### Get args for future sle

`operation_enterprise_stock_stock_ledger_business_behavior_get_arguments_for_future_stock_ledger_entry`

**Inputs** row.

**Explicit results** Platform.\_dict(mapping(“voucher\_type” → row.get(“voucher\_type”), “voucher\_no” → row.get(“voucher\_no”), “posting\_date” → row.get(“posting\_date”), “posting\_time” → row.get(“posting\_time”))).

**Local steps**

- Return Platform.\_dict(mapping(“voucher\_type” → row.get(“voucher\_type”), “voucher\_no” → row.get(“voucher\_no”), “posting\_date” → row.get(“posting\_date”), “posting\_time” → row.get(“posting\_time”))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0936.json#L2215) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L711)
