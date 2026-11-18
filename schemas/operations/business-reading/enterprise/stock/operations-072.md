# Inventory and warehouses · operations 72

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Stock balance

<a id="op-deb3e33dba2c18"></a>
### Stock Balance Report.get latest valuation rates

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_get_latest_valuation_rates`

**Inputs** self, rows.

**Declared result** dict.

**Explicit results** mapping() · mapping of tuple(entry.item\_code, entry.warehouse) → flt(entry.valuation\_rate) for entry drawn from entries.

**Local steps**

- If not rows.
  - Return mapping().
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set ranked from nested operand in the contract(nested operand in the contract).select(sle.item\_code, sle.warehouse, sle.valuation\_rate, nested operand in the contract.as\_(“row\_no”)).where(((nested operand in the contract. ….
  - Draw row from rows.
- Set entries from nested operand in the contract(nested operand in the contract).select(ranked.item\_code, ranked.warehouse, ranked.valuation\_rate).where(ranked.row\_no equals 1).run(as\_dict = true).
- Return mapping of tuple(entry.item\_code, entry.warehouse) → flt(entry.valuation\_rate) for entry drawn from entries.
  - Draw entry from entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1530) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1027)

<a id="op-f7740d61b3aa97"></a>
### Stock Balance Report.prepare stock reco voucher wise count

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_prepare_stock_reco_voucher_wise_count`

**Inputs** self.

**Record and data access** read “Stock Reconciliation Item” via get\_value.

**Explicit results** no value.

**Local steps**

- Set self.stock\_reco\_voucher\_wise\_count from Platform.\_dict().
- Set doctype from Platform.qb.DocType(“Stock Ledger Entry”).
- Set item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(doctype.voucher\_detail\_no, nested operand in the contract.as\_(“count”)).where((((nested operand in the contract equals nested operand i ….
- If items bound to self.filters.item\_code.
  - If isinstance(items, str).
    - Set items from list(items).
  - Set query from query.where(item.name.isin(items)).
- If self.filters.item\_group.
  - Set childrens from list().
  - Evaluate childrens.append(self.filters.item\_group).
  - If item\_group\_childrens bound to get\_descendants\_of(“Item Group”, self.filters.item\_group, ignore\_permissions = true).
    - Evaluate childrens.extend(item\_group\_childrens).
  - If childrens.
    - Set query from query.where(item.item\_group.isin(childrens)).
- If warehouses bound to self.filters.get(“warehouse”).
  - If isinstance(warehouses, str).
    - Set warehouses from list(warehouses).
  - Set childrens from list().
  - For each warehouse in warehouses.
    - Evaluate childrens.append(warehouse).
    - If warehouse\_childrens bound to get\_descendants\_of(“Warehouse”, warehouse, ignore\_permissions = true).
      - Evaluate childrens.extend(warehouse\_childrens).
  - If childrens.
    - Set query from query.where(doctype.warehouse.isin(childrens)).
- Set data from query.run(as\_dict = true).
- If not data.
  - Return no value.
- For each row in data.
  - <a id="op-f7740d61b3aa97-guard-56"></a>If row.count differs from 1.
    - Continue with the next iteration or loop test.
  - Set sr\_item from Platform.db.get\_value(“Stock Reconciliation Item”, row.voucher\_detail\_no, list(“current\_qty”, “qty”), as\_dict = true).
  - If (sr\_item.qty and sr\_item.current\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sr\_item.qty → sr\_item.current\_qty.
    - Set self.stock\_reco\_voucher\_wise\_count at row.voucher\_detail\_no from sr\_item.current\_qty.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison row.count differs from 1, row.count = 2 selects the branch that continues with the next loop iteration. With row.count = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-f7740d61b3aa97-guard-56)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0913.json#L2669) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L877) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L485)

<a id="op-7dd6aefda042c1"></a>
### Stock Balance Report.prepare new data

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_prepare_new_data`

**Inputs** self.

**Local steps**

- If self.filters.get(“show\_stock\_ageing\_data”).
  - Set self.filters at “show\_warehouse\_wise\_stock” from true.
  - Set item\_wise\_fifo\_queue from FIFOSlots(self.filters).generate().
- Remove self.sle\_entries.
- Set sre\_details from self.get\_sre\_reserved\_qty\_details().
- Set variant\_values from mapping().
- If self.filters.get(“show\_variant\_attributes”).
  - Set variant\_values from self.get\_variant\_values\_for().
- For each tuple(\_key, report\_data) in self.item\_warehouse\_map.items().
  - If variant\_data bound to variant\_values.get(report\_data.item\_code).
    - Evaluate report\_data.update(variant\_data).
  - If self.filters.get(“show\_stock\_ageing\_data”).
    - Evaluate report\_data.update(self.get\_row\_stock\_ageing\_data(report\_data, item\_wise\_fifo\_queue)).
  - Evaluate report\_data.update(mapping(“reserved\_stock” → sre\_details.get(tuple(report\_data.item\_code, report\_data.warehouse), 0.0))).
  - If (not self.filters.get(“include\_zero\_stock\_items”) and report\_data and report\_data.bal\_qty equals 0 and report\_data.bal\_val equals 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.filters.get(“include\_zero\_stock\_items”) → report\_data → report\_data.bal\_qty equals 0 → report\_data.bal\_val equals 0.
    - Continue with the next iteration or loop test.
  - Evaluate self.data.append(report\_data).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sre reserved qty details](operations-072.md#op-ed4fa33395151a), [get variant values for](operations-072.md#op-4901dd037bcc0f), [get row stock ageing data](operations-072.md#op-7722fb49d3228d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L874) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L482)

<a id="op-ed4fa33395151a"></a>
### Stock Balance Report.get sre reserved qty details

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_get_stock_reservation_entry_reserved_quantity_details`

**Inputs** self.

**Declared result** dict.

**Explicit results** get\_reserved\_qty\_details(item\_code\_list, warehouse\_list).

**Local steps**

- Bind dependencies get\_reserved\_qty\_details.
- Set tuple(item\_code\_list, warehouse\_list) from tuple(list(), list()).
- For each d in self.item\_warehouse\_map.
  - Evaluate item\_code\_list.append(d at 0).
  - Evaluate warehouse\_list.append(d at 1).
- Return get\_reserved\_qty\_details(item\_code\_list, warehouse\_list).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0913.json#L4758) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L868) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L476)

<a id="op-915e04733245ac"></a>
### Stock Balance Report.prepare item warehouse map

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_prepare_item_warehouse_map`

**Inputs** self, entry, group\_by\_key.

**Local steps**

- Set qty\_dict from self.item\_warehouse\_map at group\_by\_key.
- Set balance from self.get\_item\_warehouse\_balance(entry, qty\_dict).
- For each field in self.inventory\_dimensions.
  - Set qty\_dict at field from entry.get(field).
- If (entry.voucher\_type equals “Stock Reconciliation” and self.is\_reconciled\_balance(entry) and (not entry.batch\_no or entry.serial\_no or entry.serial\_and\_batch\_bundle) and len(group\_by\_key) equals 2).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.voucher\_type equals “Stock Reconciliation” → self.is\_reconciled\_balance(entry) → (not entry.batch\_no or entry.serial\_no or entry.serial\_and\_batch\_bundle) → len(group\_by\_key) equals 2.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not entry.batch\_no → entry.serial\_no → entry.serial\_and\_batch\_bundle.
  - If (entry.serial\_no and entry.voucher\_detail\_no belongs to self.stock\_reco\_voucher\_wise\_count).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.serial\_no → entry.voucher\_detail\_no belongs to self.stock\_reco\_voucher\_wise\_count.
    - Update qty\_dict.opening\_qty using − self.stock\_reco\_voucher\_wise\_count.get(entry.voucher\_detail\_no, 0).
    - Set qty\_dict.bal\_qty from 0.0.
    - Set balance.bal\_qty from 0.0.
    - Set qty\_diff from flt(entry.actual\_qty).
    - Set value\_diff from flt(entry.stock\_value\_difference).
  - Otherwise.
    - Set qty\_diff from (flt(entry.qty\_after\_transaction) − flt(balance.bal\_qty)).
    - Set value\_diff from (flt(entry.stock\_value) − flt(balance.bal\_val)).
- Otherwise.
  - Set qty\_diff from flt(entry.actual\_qty).
  - Set value\_diff from flt(entry.stock\_value\_difference).
- If (entry.posting\_date &lt; self.from\_date or entry.voucher\_no belongs to self.opening\_vouchers.get(entry.voucher\_type, list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.posting\_date &lt; self.from\_date → entry.voucher\_no belongs to self.opening\_vouchers.get(entry.voucher\_type, list()).
  - Update qty\_dict.opening\_qty using + qty\_diff.
  - Update qty\_dict.opening\_val using + value\_diff.
- Otherwise.
  - If (entry.posting\_date ≥ self.from\_date and entry.posting\_date ≤ self.to\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.posting\_date ≥ self.from\_date → entry.posting\_date ≤ self.to\_date.
    - If flt(qty\_diff, self.float\_precision) ≥ 0.
      - Update qty\_dict.in\_qty using + qty\_diff.
    - Otherwise.
      - Update qty\_dict.out\_qty using + abs(qty\_diff).
    - If flt(value\_diff, self.float\_precision) ≥ 0.
      - Update qty\_dict.in\_val using + value\_diff.
    - Otherwise.
      - Update qty\_dict.out\_val using + abs(value\_diff).
- Set qty\_dict.val\_rate from entry.valuation\_rate.
- Update qty\_dict.bal\_qty using + qty\_diff.
- Update qty\_dict.bal\_val using + value\_diff.
- Evaluate self.add\_to\_item\_warehouse\_balance(balance, qty\_dict, qty\_diff, value\_diff).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item warehouse balance](operations-072.md#op-8c85589422ab22), [is reconciled balance](operations-072.md#op-d5b28e7d824e0d), [add to item warehouse balance](operations-072.md#op-6708c4f11d94e7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L872) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L480)

<a id="op-d5b28e7d824e0d"></a>
### Stock Balance Report.is reconciled balance

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_is_reconciled_balance`

**Inputs** self, entry.

**Declared result** bool.

**Explicit results** self.adjustment\_netting.is\_adjustment(entry) · true.

**Local steps**

- If entry.is\_adjustment\_entry.
  - Return self.adjustment\_netting.is\_adjustment(entry).
- Return true.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1032)

<a id="op-8c85589422ab22"></a>
### Stock Balance Report.get item warehouse balance

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_get_item_warehouse_balance`

**Inputs** self, entry, qty\_dict.

**Declared result** Platform.\_dict.

**Explicit results** qty\_dict · self.item\_warehouse\_balances at key.

**Local steps**

- If not self.filters.get(“show\_dimension\_wise\_stock”).
  - Return qty\_dict.
- Set key from tuple(entry.item\_code, entry.warehouse).
- If key does not belong to self.item\_warehouse\_balances.
  - Set opening from (self.item\_warehouse\_map.get(key) or Platform.\_dict(bal\_qty = 0.0, bal\_val = 0.0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.item\_warehouse\_map.get(key) → Platform.\_dict(bal\_qty = 0.0, bal\_val = 0.0).
  - Set self.item\_warehouse\_balances at key from Platform.\_dict(bal\_qty = opening.bal\_qty, bal\_val = opening.bal\_val).
- Return self.item\_warehouse\_balances at key.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1529) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1026)

<a id="op-6708c4f11d94e7"></a>
### Stock Balance Report.add to item warehouse balance

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_add_to_item_warehouse_balance`

**Inputs** self, balance, qty\_dict, qty\_diff, value\_diff.

**Local steps**

- If balance is distinct from qty\_dict.
  - Update balance.bal\_qty using + qty\_diff.
  - Update balance.bal\_val using + value\_diff.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1526) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1023)

<a id="op-c2addb7b8447ec"></a>
### Stock Balance Report.initialize data

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_initialize_data`

**Inputs** self, group\_by\_key, entry.

**Local steps**

- Set self.item\_warehouse\_map at group\_by\_key from Platform.\_dict(mapping(“item\_code” → entry.item\_code, “warehouse” → entry.warehouse, “item\_group” → entry.item\_group, “company” → entry.company, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L871) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L479)

<a id="op-45124a0e9c8ff2"></a>
### Stock Balance Report.get group by key

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_get_group_by_key`

**Inputs** self, row.

**Declared result** tuple.

**Explicit results** tuple(group\_by\_key).

**Local steps**

- Set group\_by\_key from list(row.item\_code, row.warehouse).
- For each fieldname in self.inventory\_dimensions.
  - If not row.get(fieldname).
    - Continue with the next iteration or loop test.
  - If (self.filters.get(fieldname) or self.filters.get(“show\_dimension\_wise\_stock”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.get(fieldname) → self.filters.get(“show\_dimension\_wise\_stock”).
    - Evaluate group\_by\_key.append(row.get(fieldname)).
- Return tuple(group\_by\_key).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0913.json#L6192) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L862) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L471)

<a id="op-690082251c8e15"></a>
### Stock Balance Report.apply inventory dimensions filters

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_apply_inventory_dimensions_filters`

**Inputs** self, query, sle.

**Declared result** str.

**Explicit results** query.

**Local steps**

- Set inventory\_dimension\_fields from self.get\_inventory\_dimension\_fields().
- If inventory\_dimension\_fields.
  - For each fieldname in inventory\_dimension\_fields.
    - Set query from query.select(fieldname).
    - If self.filters.get(fieldname).
      - Set query from query.where(sle at fieldname.isin(self.filters.get(fieldname))).
- Return query.

**Methods declared on this owner** [get inventory dimension fields](operations-072.md#op-8cd87fb2f71b69).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0913.json#L6430) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L856) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L466)

<a id="op-29963056035fe1"></a>
### Stock Balance Report.apply warehouse filters

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_apply_warehouse_filters`

**Inputs** self, query, sle.

**Declared result** str.

**Explicit results** query.

**Local steps**

- Set warehouse\_table from Platform.qb.DocType(“Warehouse”).
- If self.filters.get(“warehouse”).
  - Set query from apply\_warehouse\_filter(query, sle, self.filters).
- If warehouse\_type bound to self.filters.get(“warehouse\_type”).
  - Set query from query.where(sle.warehouse.isin(nested operand in the contract(nested operand in the contract).select(warehouse\_table.name).where(warehouse\_table.warehouse\_type equals warehouse\_type))).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L858) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L468)

<a id="op-7a796ca7cb414a"></a>
### Stock Balance Report.apply items filters

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_apply_items_filters`

**Inputs** self, query, item\_table.

**Declared result** str.

**Explicit results** query.

**Local steps**

- If item\_group bound to self.filters.get(“item\_group”).
  - Set children from get\_descendants\_of(“Item Group”, item\_group, ignore\_permissions = true).
  - Set query from query.where(item\_table.item\_group.isin(list(expanded children, item\_group))).
- If item\_codes bound to self.filters.get(“item\_code”).
  - Set query from query.where(item\_table.name.isin(item\_codes)).
- If brand bound to self.filters.get(“brand”).
  - Set query from query.where(item\_table.brand equals brand).
- Return query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0913.json#L6974) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L857) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L467)

<a id="op-9001027475e616"></a>
### Stock Balance Report.apply date filters

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_apply_date_filters`

**Inputs** self, query, sle.

**Declared result** str.

**Explicit results** query.

**Local steps**

- If (not self.filters.ignore\_closing\_balance and self.start\_from).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.filters.ignore\_closing\_balance → self.start\_from.
  - Set query from query.where(sle.posting\_date ≥ self.start\_from).
- If self.to\_date.
  - Set query from query.where(sle.posting\_date ≤ self.to\_date).
- Return query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0913.json#L7355) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L855) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L465)

<a id="op-aa6f7cb9af9ca1"></a>
### Stock Balance Report.get columns

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_get_columns`

**Inputs** self.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Item”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “width” → 150), mappi ….
- If self.filters.get(“show\_dimension\_wise\_stock”).
  - For each dimension in get\_inventory\_dimensions().
    - Evaluate columns.append(mapping(“label” → translated dimension.doctype, “fieldname” → dimension.fieldname, “fieldtype” → “Link”, “options” → dimension.doctype, …)).
- Evaluate columns.extend(list(mapping(“label” → translated “Stock UOM”, “fieldname” → “stock\_uom”, “fieldtype” → “Link”, “options” → “UOM”, …), mapping(“label” → translated “Balance Qty”, “fieldname” → “bal\_qty”, “f ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.valuation\_field\_type → “Currency”.
  - Value choice on self.filters.valuation\_field\_type equals “Currency” — true gives “Company:company:default\_currency”, false gives no value.
- If self.filters.get(“show\_stock\_ageing\_data”).
  - Update columns using + list(mapping(“label” → translated “Average Age”, “fieldname” → “average\_age”, “width” → 100), mapping(“label” → translated “Earliest Age”, “fieldname” → “earliest\_age”, “width” → 100), mapping(“label” → tr ….
- If self.filters.get(“show\_variant\_attributes”).
  - Update columns using + list of mapping(“label” → att\_name, “fieldname” → att\_name, “width” → 100) for att\_name drawn from get\_variants\_attributes().
    - Draw att\_name from get\_variants\_attributes().
- Return columns.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L860) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L469)

<a id="op-f1fe7562d746dc"></a>
### Stock Balance Report.add additional uom columns

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_add_additional_unit_of_measure_columns`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.filters.get(“include\_uom”).
  - Return no value.
- Set conversion\_factors from self.get\_itemwise\_conversion\_factor().
- Evaluate add\_additional\_uom\_columns(self.columns, self.data, self.filters.include\_uom, conversion\_factors).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get itemwise conversion factor](operations-072.md#op-0ecbc5531c1440).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0914.json#L2356) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L853) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L463)

<a id="op-26dd3d5e162295"></a>
### Stock Balance Report.add alt uom columns

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_add_alt_unit_of_measure_columns`

**Inputs** self.

**Declared result** no value.

**State and service calls** call insert on self.columns.

**Explicit results** no value.

**Local steps**

- If not self.filters.get(“show\_alt\_uom\_balance”).
  - Return no value.
- Set item\_alt\_uom\_map from self.get\_item\_alt\_uom\_map().
- If not item\_alt\_uom\_map.
  - Return no value.
- Set bal\_qty\_idx from next(generator of i for tuple(i, col) drawn from enumerate(self.columns) where (isinstance(col, dict) and col.get(“fieldname”) equals “bal\_qty”), no value).
  - Draw tuple(i, col) from enumerate(self.columns), keep a combination only if ((isinstance(col, dict) and col.get(“fieldname”) equals “bal\_qty”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(col, dict) → col.get(“fieldname”) equals “bal\_qty”.
- If bal\_qty\_idx is identical to no value.
  - Return no value.
- Evaluate self.columns.insert((bal\_qty\_idx + 1), mapping(“label” → translated “Balance Qty (Alt UOM)”, “fieldname” → “alt\_uom\_bal\_qty”, “fieldtype” → “Float”, “width” → 140)).
- Evaluate self.columns.insert((bal\_qty\_idx + 1), mapping(“label” → translated “Alt UOM”, “fieldname” → “alt\_uom”, “fieldtype” → “Data”, “width” → 90)).
- For each row in self.data.
  - Set alt\_uoms from item\_alt\_uom\_map.get(row.item\_code, list()).
  - If alt\_uoms.
    - Set tuple(uom, factor) from tuple(alt\_uoms at 0 at “uom”, flt(alt\_uoms at 0 at “conversion\_factor”)).
    - Set row at “alt\_uom” from uom.
    - Set row at “alt\_uom\_bal\_qty” from (flt(row.get(“bal\_qty”, 0)) ÷ factor) when factor, otherwise 0.0.
      - Value choice on factor — true gives (flt(row.get(“bal\_qty”, 0)) ÷ factor), false gives 0.0.
  - Otherwise.
    - Set row at “alt\_uom” from empty text.
    - Set row at “alt\_uom\_bal\_qty” from 0.0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item alt uom map](operations-072.md#op-b49bc525502d97).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0914.json#L2503) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L854) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L464)

<a id="op-b49bc525502d97"></a>
### Stock Balance Report.get item alt uom map

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_get_item_alt_unit_of_measure_map`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping() · result.

**Local steps**

- Set item\_codes from list(set of d at “item\_code” for d drawn from self.data).
  - Draw d from self.data.
- If not item\_codes.
  - Return mapping().
- Set uom\_detail from Platform.qb.DocType(“UOM Conversion Detail”).
- Set item\_table from Platform.qb.DocType(“Item”).
- Set rows from nested operand in the contract(nested operand in the contract).orderby(uom\_detail.parent).orderby(uom\_detail.idx).run(as\_dict = true).
- Set result from mapping().
- For each row in rows.
  - Evaluate result.setdefault(row.parent, list()).
  - If not result at row.parent.
    - Evaluate result at row.parent.append(mapping(“uom” → row.uom, “conversion\_factor” → row.conversion\_factor)).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0914.json#L3295) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L864) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L473)

<a id="op-0ecbc5531c1440"></a>
### Stock Balance Report.get itemwise conversion factor

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_get_itemwise_conversion_factor`

**Inputs** self.

**Explicit results** mapping() · mapping of d.parent → d.conversion\_factor for d drawn from result.

**Local steps**

- Set items from list().
- If (self.filters.item\_code or self.filters.item\_group).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.item\_code → self.filters.item\_group.
  - Set items from list of d.item\_code for d drawn from self.data.
    - Draw d from self.data.
- Set table from Platform.qb.DocType(“UOM Conversion Detail”).
- Set query from nested operand in the contract.qb.from\_(table).select(table.conversion\_factor, table.parent).where((table.parenttype equals “Item” bitwise and table.uom equals self.filters.include\_uom)).
- If items.
  - Set query from query.where(table.parent.isin(items)).
- Set result from query.run(as\_dict = 1).
- If not result.
  - Return mapping().
- Return mapping of d.parent → d.conversion\_factor for d drawn from result.
  - Draw d from result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0914.json#L3943) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L865) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L474)

<a id="op-4901dd037bcc0f"></a>
### Stock Balance Report.get variant values for

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_get_variant_values_for`

**Inputs** self.

**Record and data access** read “Item Variant Attribute” via get\_all.

**Explicit results** attribute\_map.

**Local steps**

- Set attribute\_map from mapping().
- Set items from list().
- If (self.filters.item\_code or self.filters.item\_group).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.item\_code → self.filters.item\_group.
  - Set items from list of d.item\_code for d drawn from self.data.
    - Draw d from self.data.
- Set filters from mapping().
- If items.
  - Set filters from mapping(“parent” → tuple(“in”, items)).
- Set attribute\_info from Platform.get\_all(“Item Variant Attribute”, fields = list(“parent”, “attribute”, “attribute\_value”), filters = filters).
- For each attr in attribute\_info.
  - Evaluate attribute\_map.setdefault(attr at “parent”, mapping()).
  - Evaluate attribute\_map at attr at “parent”.update(mapping(attr at “attribute” → attr at “attribute\_value”)).
- Return attribute\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0914.json#L4389) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L869) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L477)

<a id="op-c533753f9090d0"></a>
### Stock Balance Report.get opening vouchers

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_get_opening_vouchers`

**Inputs** self.

**Explicit results** opening\_vouchers.

**Local steps**

- Set opening\_vouchers from mapping(“Stock Entry” → list(), “Stock Reconciliation” → list()).
- Set se from Platform.qb.DocType(“Stock Entry”).
- Set sr from Platform.qb.DocType(“Stock Reconciliation”).
- Set vouchers\_data from nested operand in the contract.qb.from\_((nested operand in the contract(nested operand in the contract) + nested operand in the contract(nested operand in the contract))).select(“voucher\_type”, “name”).run ….
- If vouchers\_data.
  - For each d in vouchers\_data.
    - Evaluate opening\_vouchers at d.voucher\_type.append(d.name).
- Return opening\_vouchers.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0914.json#L4806) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L867) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L475)

<a id="op-8cd87fb2f71b69"></a>
### Stock Balance Report.get inventory dimension fields

`operation_enterprise_stock_report_stock_balance_business_behavior_stock_balance_report_get_inventory_dimension_fields`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** list of dimension.fieldname for dimension drawn from get\_inventory\_dimensions().

**Local steps**

- Return list of dimension.fieldname for dimension drawn from get\_inventory\_dimensions().
  - Draw dimension from get\_inventory\_dimensions().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0914.json#L5451) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L863) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L472)

<a id="op-7722fb49d3228d"></a>
### Stock Balance Report.get row stock ageing data

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_stockbalancereport_get_row_stock_ageing_data`

**Inputs** self, report\_data, item\_wise\_fifo\_queue.

**Explicit results** stock\_ageing\_data.

**Local steps**

- Set fifo\_queue from (item\_wise\_fifo\_queue.get(tuple(report\_data.item\_code, report\_data.warehouse)) or mapping()).get(“fifo\_queue”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_wise\_fifo\_queue.get(tuple(report\_data.item\_code, report\_data.warehouse)) → mapping().
- Set stock\_ageing\_data from mapping(“average\_age” → 0, “earliest\_age” → 0, “latest\_age” → 0).
- If fifo\_queue.
  - Evaluate stock\_ageing\_data.update(get\_stock\_ageing\_data(fifo\_queue, self.to\_date)).
- Return stock\_ageing\_data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1533) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1030)

<a id="op-4dfc61f064efe3"></a>
### Get stock ageing data

`operation_enterprise_stock_report_stock_balance_business_behavior_get_stock_ageing_data`

**Inputs** fifo\_queue, to\_date.

**Declared result** dict.

**Explicit results** stock\_ageing\_data.

**Local steps**

- Set stock\_ageing\_data from mapping(“average\_age” → 0, “earliest\_age” → 0, “latest\_age” → 0).
- Set fifo\_queue from sorted(filter(itemgetter(1), normalize\_fifo\_queue(fifo\_queue)), key = itemgetter(1)).
- If not fifo\_queue.
  - Return stock\_ageing\_data.
- Set stock\_ageing\_data at “average\_age” from get\_average\_age(fifo\_queue, to\_date).
- Set stock\_ageing\_data at “earliest\_age” from date\_diff(to\_date, fifo\_queue at 0 at 1).
- Set stock\_ageing\_data at “latest\_age” from date\_diff(to\_date, fifo\_queue at negative 1 at 1).
- Set stock\_ageing\_data at “fifo\_queue” from fifo\_queue.
- Return stock\_ageing\_data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0914.json#L5656) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L851) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L461)
