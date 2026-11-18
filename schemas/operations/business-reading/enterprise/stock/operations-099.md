# Inventory and warehouses · operations 99

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock reconciliation

[Record definition](../../../../data/record-types/stock_reconciliation.json)

<a id="op-f11986ed21b2e7"></a>
### Stock Reconciliation.get existing ledger entries

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_get_existing_ledger_entries`

**Inputs** self, dimensions.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).distinct().where(((((nested operand in the contract bitwise and nested operand ….

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).distinct().where(((((nested operand in the contract bitwise and nested operand ….
  - Draw field from dimensions.
  - Draw d from self.items.
  - Draw d from self.items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1299) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L796)

<a id="op-cec0f585e97eab"></a>
### Stock Reconciliation.set zero value for customer provided items

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_set_zero_value_for_customer_provided_items`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- Set changed\_any\_values from false.
- For each d in self.get(“items”).
  - Set is\_customer\_item from Platform.get\_cached\_value(“Item”, d.item\_code, “is\_customer\_provided\_item”).
  - If (is\_customer\_item and d.valuation\_rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_customer\_item → d.valuation\_rate.
    - Set d.valuation\_rate from 0.0.
    - Set d.allow\_zero\_valuation\_rate from 1.
    - Set changed\_any\_values from true.
- If changed\_any\_values.
  - Evaluate msgprint(translated “Valuation rate for customer provided items has been set to zero.”, title = translated “Note”, indicator = “blue”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, d.item\_code, “is\_customer\_provided\_item”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0860.json#L4493) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1062)

<a id="op-6e0fb676af2140"></a>
### Stock Reconciliation.set total qty and amount

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_set_total_quantity_and_amount`

**Inputs** self.

**Local steps**

- For each d in self.get(“items”).
  - Set d.amount from flt((flt(d.qty) × flt(d.valuation\_rate)), d.precision(“amount”)).
  - Set d.current\_amount from flt((flt(d.current\_qty) × flt(d.current\_valuation\_rate)), d.precision(“current\_amount”)).
  - Set d.quantity\_difference from (flt(d.qty) − flt(d.current\_qty)).
  - Set d.amount\_difference from (flt(d.amount) − flt(d.current\_amount)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0860.json#L4780) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1061)

<a id="op-7083d69d3bead1"></a>
### Stock Reconciliation.recalculate difference amount from ledger

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_recalculate_difference_amount_from_ledger`

**Inputs** self, voucher\_detail\_no = no value.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If self.purpose equals ADJUSTMENT\_ENTRY.
  - Evaluate AdjustmentEntry(self).set\_difference\_amount\_from\_ledger().
  - Return no value.
- For each row in self.items.
  - If voucher\_detail\_no belongs to tuple(no value, row.name).
    - Evaluate self.set\_row\_values\_from\_ledger(row).
- Set difference\_amount from sum(generator of flt(row.amount\_difference) for row drawn from self.items).
  - Draw row from self.items.
- Evaluate self.db\_set(“difference\_amount”, flt(difference\_amount, self.precision(“difference\_amount”)), update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set row values from ledger](operations-099.md#op-4b5a76512db500).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1056)

<a id="op-4b5a76512db500"></a>
### Stock Reconciliation.set row values from ledger

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_set_row_values_from_ledger`

**Inputs** self, row.

**State and service calls** call db\_set on row.

**Explicit results** no value.

**Local steps**

- Set stock\_value\_difference from flt(get\_row\_stock\_value\_difference(self.doctype, self.name, row.name)).
- Set amount\_difference from flt(stock\_value\_difference, row.precision(“amount\_difference”)).
- If self.is\_adjustment\_row(row).
  - Evaluate self.set\_adjustment\_row\_values(row, amount\_difference).
  - Return no value.
- Set amount from flt((flt(row.qty) × flt(row.valuation\_rate)), row.precision(“amount”)).
- Set current\_amount from flt((amount − amount\_difference), row.precision(“current\_amount”)).
- Set current\_qty from self.get\_current\_qty\_from\_ledger(row).
- Set current\_valuation\_rate from flt((current\_amount ÷ current\_qty), row.precision(“current\_valuation\_rate”)) when current\_qty, otherwise 0.0.
  - Value choice on current\_qty — true gives flt((current\_amount ÷ current\_qty), row.precision(“current\_valuation\_rate”)), false gives 0.0.
- Evaluate row.db\_set(mapping(“amount” → amount, “current\_qty” → current\_qty, “current\_valuation\_rate” → current\_valuation\_rate, “current\_amount” → current\_amount, …), update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is adjustment row](operations-099.md#op-1485cf1375f49b), [set adjustment row values](operations-099.md#op-c21c525011552e), [get current qty from ledger](operations-099.md#op-b409c33be1be12).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L804)

<a id="op-1485cf1375f49b"></a>
### Stock Reconciliation.is adjustment row

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_is_adjustment_row`

**Inputs** self, row.

**Declared result** bool.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** row.name belongs to self.flags.adjustment\_rows.

**Local steps**

- If self.flags.adjustment\_rows is identical to no value.
  - Set self.flags.adjustment\_rows from set(Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → self.doctype, “voucher\_no” → self.name, “is\_adjustment\_entry” → 1, “is\_cancelled” → 0), pluck = “voucher\_detail\_no”)).
- Return row.name belongs to self.flags.adjustment\_rows.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1304) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L801)

<a id="op-c21c525011552e"></a>
### Stock Reconciliation.set adjustment row values

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_set_adjustment_row_values`

**Inputs** self, row, amount\_difference.

**State and service calls** call db\_set on row.

**Local steps**

- Set previous\_sle from (self.get\_previous\_ledger\_entry(row) or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_previous\_ledger\_entry(row) → Platform.\_dict().
- Set current\_qty from flt(previous\_sle.get(“qty\_after\_transaction”), row.precision(“current\_qty”)).
- Set current\_valuation\_rate from flt(previous\_sle.get(“valuation\_rate”), row.precision(“current\_valuation\_rate”)).
- Set current\_amount from flt(previous\_sle.get(“stock\_value”), row.precision(“current\_amount”)).
- Evaluate row.db\_set(mapping(“amount” → current\_amount, “current\_qty” → current\_qty, “current\_valuation\_rate” → current\_valuation\_rate, “current\_amount” → current\_amount, …), update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get previous ledger entry](operations-099.md#op-05cea48d9db595).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L802)

<a id="op-b409c33be1be12"></a>
### Stock Reconciliation.get current qty from ledger

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_get_current_quantity_from_ledger`

**Inputs** self, row.

**Record and data access** read “Serial and Batch Bundle” via get\_value.

**Explicit results** abs(flt(total\_qty, row.precision(“current\_qty”))) · flt(row.current\_qty, row.precision(“current\_qty”)) · flt(previous\_sle.get(“qty\_after\_transaction”), row.precision(“current\_qty”)).

**Local steps**

- If row.current\_serial\_and\_batch\_bundle.
  - Set total\_qty from Platform.db.get\_value(“Serial and Batch Bundle”, row.current\_serial\_and\_batch\_bundle, “total\_qty”).
  - Return abs(flt(total\_qty, row.precision(“current\_qty”))).
- Set previous\_sle from self.get\_previous\_ledger\_entry(row).
- If previous\_sle is identical to no value.
  - Return flt(row.current\_qty, row.precision(“current\_qty”)).
- Return flt(previous\_sle.get(“qty\_after\_transaction”), row.precision(“current\_qty”)).

**Methods declared on this owner** [get previous ledger entry](operations-099.md#op-05cea48d9db595).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1043)

<a id="op-05cea48d9db595"></a>
### Stock Reconciliation.get previous ledger entry

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_get_previous_ledger_entry`

**Inputs** self, row.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit results** no value · previous\_sle at 0 when previous\_sle, otherwise Platform.\_dict().

**Local steps**

- Set reco\_sle from Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_type” → self.doctype, “voucher\_no” → self.name, “voucher\_detail\_no” → row.name, “is\_cancelled” → 0), list(“posting\_datetime”, “creation”), as\_dict = true).
- If not reco\_sle.
  - Return no value.
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set previous\_sle from nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(sle.creation, order = nested operand in the contract.qb.desc).limit(1).run(as\_dict = true).
- Return previous\_sle at 0 when previous\_sle, otherwise Platform.\_dict().
  - Value choice on previous\_sle — true gives previous\_sle at 0, false gives Platform.\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1301) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L798)

<a id="op-5a782a270c622e"></a>
### Stock Reconciliation.submit

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_submit`

**Inputs** self.

**State and service calls** call save on self.

**Local steps**

- If len(self.items) &gt; 100.
  - Evaluate self.check\_permission(“submit”).
  - Set self.docstatus from DocStatus.draft().
  - Evaluate self.save().
  - Evaluate msgprint(translated “The task has been enqueued as a background job. In case there is any issue on processing in background, the  …”).
  - Evaluate self.queue\_action(“submit”, timeout = 4600).
- Otherwise.
  - Evaluate self.\_submit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“submit”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L142) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1063)

<a id="op-db8627b2d73b48"></a>
### Stock Reconciliation.cancel

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_cancel`

**Inputs** self.

**Local steps**

- If len(self.items) &gt; 100.
  - Evaluate msgprint(translated “The task has been enqueued as a background job. In case there is any issue on processing in background, the  …”).
  - Evaluate self.queue\_action(“cancel”, timeout = 2000).
- Otherwise.
  - Evaluate self.\_cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0860.json#L6805) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1040)

<a id="op-bfe5fe1ad7932f"></a>
### Get items

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_get_items`

**Inputs** warehouse, posting\_date, posting\_time, company, item\_code = no value, ignore\_empty\_stock = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** res.

**Local steps**

- Evaluate Platform.has\_permission(“Stock Reconciliation”, “write”, throw = true).
- Evaluate Platform.has\_permission(“Item”, “read”, throw = true).
- Evaluate Platform.has\_permission(“Warehouse”, “read”, doc = warehouse, throw = true).
- If Platform.db.get\_value(“Warehouse”, warehouse, “is\_group”).
  - For each child\_warehouse in Platform.db.get\_descendants(“Warehouse”, warehouse).
    - Evaluate Platform.has\_permission(“Warehouse”, “read”, doc = child\_warehouse, throw = true).
- Set ignore\_empty\_stock from cint(ignore\_empty\_stock).
- Set items from list().
- If (item\_code and warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_code → warehouse.
  - Set items from get\_item\_and\_warehouses(item\_code, warehouse).
- If not item\_code.
  - Set items from get\_items\_for\_stock\_reco(warehouse, company).
- Set res from list().
- Set itemwise\_batch\_data from get\_itemwise\_batch(warehouse, posting\_date, company, item\_code, …).
- For each d in items.
  - If tuple(d.item\_code, d.warehouse) belongs to itemwise\_batch\_data.
    - For each row in itemwise\_batch\_data.get(tuple(d.item\_code, d.warehouse)).
      - If (ignore\_empty\_stock and not row.qty).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in ignore\_empty\_stock → not row.qty.
        - Continue with the next iteration or loop test.
      - Set args from get\_item\_data(row, row.qty, row.valuation\_rate).
      - Evaluate res.append(args).
  - Otherwise.
    - Set stock\_bal from \_get\_stock\_balance(d.item\_code, d.warehouse, posting\_date, posting\_time, with\_valuation\_rate = true, with\_serial\_no = cint(d.has\_serial\_no)).
    - Set tuple(qty, valuation\_rate, serial\_no) from tuple(stock\_bal at 0, stock\_bal at 1, stock\_bal at 2 when cint(d.has\_serial\_no), otherwise empty text).
      - Value choice on cint(d.has\_serial\_no) — true gives stock\_bal at 2, false gives empty text.
    - If (ignore\_empty\_stock and not stock\_bal at 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in ignore\_empty\_stock → not stock\_bal at 0.
      - Continue with the next iteration or loop test.
    - Set args from get\_item\_data(d, qty, valuation\_rate, serial\_no).
    - Evaluate res.append(args).
- Return res.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Stock Reconciliation”, “write”, throw = true), Platform.has\_permission(“Item”, “read”, throw = true) and 2 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1034)

<a id="op-7710839a0a0f99"></a>
### Get item and warehouses

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_get_item_and_warehouses`

**Inputs** item\_code, warehouse.

**Record and data access** read “Item” via get\_cached\_value · read “Warehouse” via get\_cached\_value.

**Explicit results** items.

**Local steps**

- Bind dependencies get\_descendants\_of.
- Set items from list().
- Set stock\_uom from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”).
- If Platform.get\_cached\_value(“Warehouse”, warehouse, “is\_group”).
  - Set childrens from get\_descendants\_of(“Warehouse”, warehouse, ignore\_permissions = true, order\_by = “lft”).
  - For each ch\_warehouse in childrens.
    - Evaluate items.append(Platform.\_dict(mapping(“item\_code” → item\_code, “warehouse” → ch\_warehouse, “stock\_uom” → stock\_uom))).
- Otherwise.
  - Set items from list(Platform.\_dict(mapping(“item\_code” → item\_code, “warehouse” → warehouse, “stock\_uom” → stock\_uom))).
- Return items.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”), Platform.get\_cached\_value(“Warehouse”, warehouse, “is\_group”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0861.json#L830) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1032)

<a id="op-6848a42dd05e4d"></a>
### Get items for stock reco

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_get_items_for_stock_reco`

**Inputs** warehouse, company.

**Record and data access** read “Warehouse” via get\_value · execute query text (SELECT, Item, Warehouse).

**State and service calls** execute a supplied database query.

**Explicit results** items.

**Local steps**

- Set tuple(lft, rgt) from Platform.db.get\_value(“Warehouse”, warehouse, list(“lft”, “rgt”)).
- Set items from Platform.db.sql(formatted text   select  i.name as item\_code, i.item\_name, bin.warehouse as warehouse, i.has\_serial\_no, i.has\_batch\_no,  i.stock\_uom  from  ′tabBin′ bin, ′ta, as\_dict = 1).
- Update items using + Platform.db.sql(query text (SELECT, Item, Warehouse), tuple(lft, rgt, company), as\_dict = 1).
- Set iw\_keys from set().
- Set items from list of item for item drawn from items where list(tuple(item.item\_code, item.warehouse) does not belong to iw\_keys, iw\_keys.add(tuple(item.item\_code, item.warehouse))) at 0.
  - Draw item from items, keep a combination only if (list(tuple(item.item\_code, item.warehouse) does not belong to iw\_keys, iw\_keys.add(tuple(item.item\_code, item.warehouse))) at 0).
- Return items.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1035)

<a id="op-11f611bc913367"></a>
### Get item data

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_get_item_data`

**Inputs** row, qty, valuation\_rate, serial\_no = no value.

**Explicit results** mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “qty” → qty, “item\_name” → row.item\_name, …).

**Local steps**

- Return mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “qty” → qty, “item\_name” → row.item\_name, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0861.json#L2473) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1033)

<a id="op-3b26e0fa3a08e3"></a>
### Get itemwise batch

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_get_itemwise_batch`

**Inputs** warehouse, posting\_date, company, item\_code = no value, posting\_time = no value.

**Explicit results** itemwise\_batch\_data.

**Local steps**

- Bind dependencies execute.
- Set itemwise\_batch\_data from mapping().
- Set filters from Platform.\_dict(mapping(“warehouse” → warehouse, “from\_date” → posting\_date, “to\_date” → posting\_date, “company” → company)).
- If posting\_time.
  - Set filters.to\_datetime from combine\_datetime(posting\_date, posting\_time).
- If item\_code.
  - Set filters.item\_code from item\_code.
- Set tuple(columns, data) from execute(filters).
- For each row in data.
  - Evaluate itemwise\_batch\_data.setdefault(tuple(row at 0, row at 3), list()).append(Platform.\_dict(mapping(“item\_code” → row at 0, “warehouse” → row at 3, “qty” → row at 8, “valuation\_rate” → row at 9, …))).
- Return itemwise\_batch\_data.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1036)

<a id="op-af7aae96b70f4e"></a>
### Get row stock value difference

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_get_row_stock_value_difference`

**Inputs** voucher\_type, voucher\_no, voucher\_detail\_no.

**Explicit results** flt(result at 0 at 0) when (result and result at 0 at 0), otherwise 0.0.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set result from nested operand in the contract(nested operand in the contract).select(Sum(nested operand in the contract.stock\_value\_difference)).where((((nested operand in the contract equals nested operand in the contra ….run().
- Return flt(result at 0 at 0) when (result and result at 0 at 0), otherwise 0.0.
  - Value choice on (result and result at 0 at 0) — true gives flt(result at 0 at 0), false gives 0.0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in result → result at 0 at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0861.json#L3263) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1037)

<a id="op-4e9ef555bd073c"></a>
### Get stock balance for

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_get_stock_balance_for`

**Inputs** item\_code, warehouse, posting\_date, posting\_time, batch\_no = no value, with\_valuation\_rate = true, inventory\_dimensions\_dict = no value, row = no value, company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_cached\_value · read “Stock Settings” via get\_single\_value.

**Explicit results** mapping(“qty” → 0, “rate” → 0, “serial\_nos” → no value, “use\_serial\_batch\_fields” → row.use\_serial\_batch\_fields when row, otherwise use\_serial\_batch\_fields) · mapping(“qty” → qty, “rate” → rate when cint(with\_valuation\_rate), otherwise 0, “serial\_nos” → serial\_nos, “use\_serial\_batch\_fields” → row.use\_serial\_batch\_fields when row, otherwise use\_serial\_batch\_fields).

**Explicit failure paths** validation helper — msg.

**Local steps**

- Evaluate Platform.has\_permission(“Stock Reconciliation”, “write”, throw = true).
- Set item\_dict from Platform.get\_cached\_value(“Item”, item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1).
- If isinstance(row, str).
  - Set row from json.loads(row).
- If isinstance(row, dict).
  - Set row from Platform.\_dict(row).
- If not item\_dict.
  - Set msg from translated “Item {} does not exist.”.format(item\_code).
  - Call the validation error handler Platform.throw(msg, title = translated “Missing”).
- Set serial\_nos from no value.
- Set has\_serial\_no from bool(item\_dict.get(“has\_serial\_no”)).
- Set has\_batch\_no from bool(item\_dict.get(“has\_batch\_no”)).
- Set use\_serial\_batch\_fields from Platform.db.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).
- If (not batch\_no and has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not batch\_no → has\_batch\_no.
  - Return mapping(“qty” → 0, “rate” → 0, “serial\_nos” → no value, “use\_serial\_batch\_fields” → row.use\_serial\_batch\_fields when row, otherwise use\_serial\_batch\_fields).
    - Value choice on row — true gives row.use\_serial\_batch\_fields, false gives use\_serial\_batch\_fields.
- Set data from \_get\_stock\_balance(item\_code, warehouse, posting\_date, posting\_time, with\_valuation\_rate = true, with\_serial\_no = (has\_serial\_no and not has\_batch\_no), inventory\_dimensions\_dict = inventory\_dimensions\_dict).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_serial\_no → not has\_batch\_no.
- If (has\_serial\_no and not has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_serial\_no → not has\_batch\_no.
  - Set tuple(qty, rate, serial\_nos) from data.
- Otherwise.
  - Set tuple(qty, rate) from data.
- If item\_dict.get(“has\_batch\_no”).
  - Set qty from (get\_batch\_qty\_for\_stock(batch\_no, warehouse, posting\_date = posting\_date, posting\_time = posting\_time, for\_stock\_levels = true, consider\_negative\_batches = true, …) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_batch\_qty\_for\_stock(batch\_no, warehouse, posting\_date = posting\_date, posting\_time = posting\_time, for\_stock\_levels = true, consider\_negative\_batches = true, …) → 0.
  - If has\_serial\_no.
    - Set serial\_no\_details from get\_available\_serial\_nos(Platform.\_dict(mapping(“item\_code” → item\_code, “warehouse” → warehouse, “posting\_datetime” → combine\_datetime(posting\_date, posting\_time), “ignore\_warehouse” → 1, …))).
    - Set serial\_nos from whitespace '\\n'.join(generator of d.serial\_no for d drawn from serial\_no\_details where d.batch\_no equals batch\_no).
      - Draw d from serial\_no\_details, keep a combination only if (d.batch\_no equals batch\_no).
  - If (row and row.use\_serial\_batch\_fields and row.batch\_no and (qty or row.current\_qty)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row → row.use\_serial\_batch\_fields → row.batch\_no → (qty or row.current\_qty).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in qty → row.current\_qty.
    - Set rate from \_get\_incoming\_rate(Platform.\_dict(mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “qty” → (flt((qty or nested operand in the contract.current\_qty)) × negative 1), “batch\_no” → row.batch\_no, …))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in qty → row.current\_qty.
      - Value choice on (row and row.get(“creation”)) — true gives row.get(“creation”), false gives now().
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row → row.get(“creation”).
- Return mapping(“qty” → qty, “rate” → rate when cint(with\_valuation\_rate), otherwise 0, “serial\_nos” → serial\_nos, “use\_serial\_batch\_fields” → row.use\_serial\_batch\_fields when row, otherwise use\_serial\_batch\_fields).
  - Value choice on cint(with\_valuation\_rate) — true gives rate, false gives 0.
  - Value choice on row — true gives row.use\_serial\_batch\_fields, false gives use\_serial\_batch\_fields.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Stock Reconciliation”, “write”, throw = true) · configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1), Platform.db.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”) · clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1038)

<a id="op-02a2464cf8933b"></a>
### Reconciliation allowed docs

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_reconciliation_allowed_docs`

**Inputs** doctype.

**Explicit results** get\_allowed\_docs\_for\_doctype(get\_user\_permissions(Platform.session.user).get(doctype, list()), “Stock Reconciliation”).

**Local steps**

- Return get\_allowed\_docs\_for\_doctype(get\_user\_permissions(Platform.session.user).get(doctype, list()), “Stock Reconciliation”).

**Values supplied outside this operation** effective access from get\_user\_permissions(Platform.session.user).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L793)

<a id="op-c1ad22d8bb1b3b"></a>
### Require reconciliation permission

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_require_reconciliation_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, name.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L794)

<a id="op-fc263d03e67beb"></a>
### Get difference account

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_get_difference_account`

**Inputs** purpose, company.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Account” via get\_value.

**Explicit results** account.

**Local steps**

- Evaluate Platform.has\_permission(“Stock Reconciliation”, “read”, throw = true).
- Evaluate Platform.has\_permission(“Company”, “select”, doc = company, throw = true).
- Evaluate \_require\_reconciliation\_permission(“Company”, company).
- If purpose belongs to tuple(“Stock Reconciliation”, ADJUSTMENT\_ENTRY).
  - Set account from get\_company\_default(company, “stock\_adjustment\_account”).
- Otherwise.
  - Set account from Platform.db.get\_value(“Account”, mapping(“is\_group” → 0, “company” → company, “account\_type” → “Temporary”), “name”).
- Return account.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Stock Reconciliation”, “read”, throw = true), Platform.has\_permission(“Company”, “select”, doc = company, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1031)

<a id="op-ef2eb2a451acd9"></a>
### On doctype update

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_on_doctype_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Stock Reconciliation”.

**Local steps**

- Evaluate Platform.db.add\_index(“Stock Reconciliation”, list(“purpose”, “posting\_date”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L792)

## Record · Stock reposting settings

[Record definition](../../../../data/record-types/stock_reposting_settings.json)

<a id="op-88a6ff1574c92b"></a>
### Stock Reposting Settings.validate

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_stock_reposting_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_minimum\_reposting\_time\_slot().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set minimum reposting time slot](operations-100.md#op-2ff6653983f29f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0866.json#L5669) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L221) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1137)

<a id="op-ed054396b8e161"></a>
### Stock Reposting Settings.before save

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_stock_reposting_settings_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.reset\_parallel\_reposting\_settings().

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset parallel reposting settings](operations-100.md#op-ad2871a72557bf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0866.json#L5720) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L217) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1133)
