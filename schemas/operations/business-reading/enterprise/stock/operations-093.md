# Inventory and warehouses · operations 93

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock ledger

<a id="op-a13fffe7d3ef3f"></a>
### Get prior ledger condition

`operation_enterprise_binding_enterprise_stock_stock_ledger_get_prior_ledger_condition`

**Inputs** table, posting\_datetime, creation.

**Explicit results** (table.posting\_datetime &lt; posting\_datetime bitwise or (table.posting\_datetime equals posting\_datetime bitwise and table.creation &lt; creation)) · table.posting\_datetime ≤ posting\_datetime.

**Local steps**

- If creation.
  - Return (table.posting\_datetime &lt; posting\_datetime bitwise or (table.posting\_datetime equals posting\_datetime bitwise and table.creation &lt; creation)).
- Return table.posting\_datetime ≤ posting\_datetime.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1090)

<a id="op-d362bc63fd379a"></a>
### Get valuation rate

`operation_enterprise_stock_stock_ledger_business_behavior_get_valuation_rate`

**Inputs** item\_code, warehouse, voucher\_type, voucher\_no, allow\_zero\_rate = false, currency = no value, company = no value, fallbacks = true, raise\_error\_if\_no\_rate = true, batch\_no = no value, serial\_and\_batch\_bundle = no value, posting\_datetime = no value, creation = no value.

**Record and data access** read “Warehouse” via get\_cached\_value · read “Batch” via get\_value · read “Serial and Batch Bundle” via get\_value · read “Item” via get\_value · read “Item Price” via get\_value.

**Explicit results** flt(last\_valuation\_rate at 0 at 0) · batch\_obj.get\_incoming\_rate() · flt(rate).

**Explicit failure paths** validation helper.

**Local steps**

- Bind dependencies BatchNoValuation.
- If not company.
  - Set company from Platform.get\_cached\_value(“Warehouse”, warehouse, “company”).
- If (warehouse and batch\_no and Platform.db.get\_value(“Batch”, batch\_no, “use\_batchwise\_valuation”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in warehouse → batch\_no → Platform.db.get\_value(“Batch”, batch\_no, “use\_batchwise\_valuation”).
  - Set table from Platform.qb.DocType(“Stock Ledger Entry”).
  - Set query from nested operand in the contract.qb.from\_(table).select((Sum(table.stock\_value\_difference) ÷ Sum(table.actual\_qty))).where((((table.item\_code equals item\_code bitwise and table.warehouse equals warehouse) bi ….
  - If voucher\_no.
    - Set query from query.where((table.voucher\_no differs from voucher\_no bitwise or table.voucher\_type differs from voucher\_type)).
  - If posting\_datetime.
    - Set query from query.where(get\_prior\_ledger\_condition(table, posting\_datetime, creation)).
  - Set last\_valuation\_rate from query.run().
  - If (last\_valuation\_rate and last\_valuation\_rate at 0 at 0 is distinct from no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_valuation\_rate → last\_valuation\_rate at 0 at 0 is distinct from no value.
    - Return flt(last\_valuation\_rate at 0 at 0).
- If (warehouse and serial\_and\_batch\_bundle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in warehouse → serial\_and\_batch\_bundle.
  - Set bundle from Platform.get\_value(“Serial and Batch Bundle”, serial\_and\_batch\_bundle, list(“total\_qty”, “posting\_datetime”), as\_dict = true).
  - Set batch\_obj from BatchNoValuation(sle = Platform.\_dict(mapping(“item\_code” → item\_code, “warehouse” → warehouse, “actual\_qty” → negative abs(flt(nested operand in the contract.total\_qty)), “serial\_and\_batch\_bundle” → seria ….
  - Return batch\_obj.get\_incoming\_rate().
- Set sle\_entry from Platform.qb.DocType(“Stock Ledger Entry”).
- Set last\_sle\_query from nested operand in the contract(nested operand in the contract).orderby(sle\_entry.posting\_datetime, order = nested operand in the contract.qb.desc).orderby(sle\_entry.creation, order = Platform.qb.desc).limit(1).
- If voucher\_no.
  - Set last\_sle\_query from last\_sle\_query.where(complement (sle\_entry.voucher\_no equals voucher\_no bitwise and sle\_entry.voucher\_type equals voucher\_type)).
- If posting\_datetime.
  - Set last\_sle\_query from last\_sle\_query.where(get\_prior\_ledger\_condition(sle\_entry, posting\_datetime, creation)).
- If last\_valuation\_rate bound to last\_sle\_query.run().
  - Return flt(last\_valuation\_rate at 0 at 0).
- If fallbacks.
  - If rate bound to (Platform.db.get\_value(“Item”, item\_code, “valuation\_rate”) or Platform.db.get\_value(“Item”, item\_code, “standard\_rate”) or Platform.db.get\_value(“Item Price”, dict(item\_code = item\_code, buying = 1, curre ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Item”, item\_code, “valuation\_rate”) → Platform.db.get\_value(“Item”, item\_code, “standard\_rate”) → Platform.db.get\_value(“Item Price”, dict(item\_code = item\_code, buying = 1, currency = currency), “price\_list\_rate”).
    - Return flt(rate).
- If (not allow\_zero\_rate and raise\_error\_if\_no\_rate and cint(Enterprise.is\_perpetual\_inventory\_enabled(company))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not allow\_zero\_rate → raise\_error\_if\_no\_rate → cint(Enterprise.is\_perpetual\_inventory\_enabled(company)).
  - Set form\_link from get\_link\_to\_form(“Item”, item\_code).
  - Set message from translated “Valuation Rate for the Item {0}, is required to do accounting entries for {1} {2}.”.format(form\_link, voucher\_type, voucher\_no).
  - Update message using + (text in the contract + translated “Here are the options to proceed:”).
  - Set solutions from ((text in the contract + translated “If the item is transacting as a Zero Valuation Rate item in this entry, please enable 'Allow Zero Valuation  …”.format(voucher\_type)) + “&lt;/li&gt;”).
  - Update solutions using + ((((text in the contract + translated “If not, you can Cancel / Submit this entry”) + “ {} ”.format(Platform.bold(translated “after”))) + translated “performing either one below:”) + “&lt;/li&gt;”).
  - Set sub\_solutions from ((text in the contract + translated “Create an incoming stock transaction for the Item.”) + “&lt;/li&gt;”).
  - If fallbacks.
    - Update sub\_solutions using + ((text in the contract + translated “Mention Valuation Rate in the Item master.”) + “&lt;/li&gt;&lt;/ul&gt;”).
  - Otherwise.
    - Update sub\_solutions using + ((text in the contract + translated “Enter the Incoming Rate (Costing) in the {0} Item table.”.format(voucher\_type)) + “&lt;/li&gt;&lt;/ul&gt;”).
  - Set msg from (((message + solutions) + sub\_solutions) + “&lt;/li&gt;”).
  - Call the validation error handler Platform.throw(msg = msg, title = translated “Valuation Rate Missing”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, warehouse, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1217) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L732)

<a id="op-a5a57c45c23a25"></a>
### Update qty in future sle

`operation_enterprise_stock_stock_ledger_business_behavior_update_quantity_in_future_stock_ledger_entry`

**Inputs** args, allow\_negative\_stock = false.

**Local steps**

- Set qty\_shift from args.actual\_qty.
- Set posting\_datetime from get\_combine\_datetime(args at “posting\_date”, args at “posting\_time”).
- Set args at “posting\_datetime” from posting\_datetime.
- If args.voucher\_type equals “Stock Reconciliation”.
  - Set qty\_shift from get\_stock\_reco\_qty\_shift(args).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set future\_condition from sle.posting\_datetime &gt; posting\_datetime.
- If (args.get(“creation”) and not args.get(“is\_cancelled”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“creation”) → not args.get(“is\_cancelled”).
  - Set future\_condition from (future\_condition bitwise or (sle.posting\_datetime equals posting\_datetime bitwise and sle.creation &gt; args.get(“creation”))).
- Set query from Platform.qb.update(sle).where((((sle.item\_code equals nested operand in the contract.get(“item\_code”) bitwise and sle.warehouse equals nested operand in the contract.get(“warehouse”)) bitwise and sle.is\_ca ….
- Set next\_stock\_reco\_detail from get\_next\_stock\_reco(args).
- If next\_stock\_reco\_detail.
  - Set query from query.where(get\_datetime\_limit\_condition(sle, next\_stock\_reco\_detail at 0)).
- Set new\_qty from (sle.qty\_after\_transaction + qty\_shift).
- Set valuation\_method from get\_valuation\_method(args.get(“item\_code”), args.get(“company”)).
- Set query from set\_value\_shift\_in\_future\_sle(query, sle, args, new\_qty, …).
- Set query from query.set(sle.qty\_after\_transaction, new\_qty).
- Evaluate query.run().
- Evaluate validate\_negative\_qty\_in\_future\_sle(args, allow\_negative\_stock).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1287) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L796)

<a id="op-60d1d71a0f5cc0"></a>
### Set value shift in future sle

`operation_enterprise_binding_enterprise_stock_stock_ledger_set_value_shift_in_future_sle`

**Inputs** query, sle, args, new\_qty, valuation\_method.

**Explicit results** query · query.set(sle.valuation\_rate, new\_rate).set(sle.stock\_value, new\_value).

**Local steps**

- Set value\_shift from get\_value\_shift\_for\_future\_sle(args).
- If not value\_shift.
  - Return query.
- Set new\_value from (sle.stock\_value + value\_shift).
- Set new\_rate from Case().when(new\_qty differs from 0, (new\_value ÷ new\_qty)).else\_(sle.valuation\_rate).
- If (valuation\_method belongs to tuple(“FIFO”, “LIFO”) and not (args.has\_serial\_no or args.has\_batch\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in valuation\_method belongs to tuple(“FIFO”, “LIFO”) → not (args.has\_serial\_no or args.has\_batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.has\_serial\_no → args.has\_batch\_no.
  - Set query from query.set(sle.stock\_queue, Concat(“&#91;&#91;”, new\_qty, “, ”, new\_rate, …)).
- Return query.set(sle.valuation\_rate, new\_rate).set(sle.stock\_value, new\_value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1108)

<a id="op-99361db8d4c62b"></a>
### Get value shift for future sle

`operation_enterprise_binding_enterprise_stock_stock_ledger_get_value_shift_for_future_sle`

**Inputs** args.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit results** 0.0 · flt(Platform.db.get\_value(“Stock Ledger Entry”, args.name, “stock\_value\_difference”)) · negative get\_stock\_value\_difference\_of\_cancelled\_entry(args).

**Local steps**

- Bind dependencies future\_sle\_exists.
- If not future\_sle\_exists(args).
  - Return 0.0.
- If not args.get(“is\_cancelled”).
  - Return flt(Platform.db.get\_value(“Stock Ledger Entry”, args.name, “stock\_value\_difference”)).
- Return negative get\_stock\_value\_difference\_of\_cancelled\_entry(args).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1093)

<a id="op-2cccc39bd20aa9"></a>
### Get stock value difference of cancelled entry

`operation_enterprise_binding_enterprise_stock_stock_ledger_get_stock_value_difference_of_cancelled_entry`

**Inputs** args.

**Explicit results** flt(entry at 0 at 0) when entry, otherwise 0.0.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set entry from nested operand in the contract(nested operand in the contract).orderby(sle.creation, order = Order.desc).limit(1).run().
- Return flt(entry at 0 at 0) when entry, otherwise 0.0.
  - Value choice on entry — true gives flt(entry at 0 at 0), false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1092)

<a id="op-ce145162658d4e"></a>
### Get stock reco qty shift

`operation_enterprise_stock_stock_ledger_business_behavior_get_stock_reco_quantity_shift`

**Inputs** kwargs.

**Explicit results** flt(kwargs.actual\_qty) · kwargs.get(“previous\_qty\_after\_transaction”) · stock\_reco\_qty\_shift.

**Local steps**

- Set stock\_reco\_qty\_shift from 0.
- If (kwargs.get(“is\_adjustment\_entry”) and not kwargs.get(“is\_cancelled”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs.get(“is\_adjustment\_entry”) → not kwargs.get(“is\_cancelled”).
  - Return flt(kwargs.actual\_qty).
- If kwargs.get(“is\_cancelled”).
  - If kwargs.get(“previous\_qty\_after\_transaction”).
    - If kwargs.get(“serial\_and\_batch\_bundle”).
      - Return kwargs.get(“previous\_qty\_after\_transaction”).
    - Set last\_balance from kwargs.get(“previous\_qty\_after\_transaction”).
    - Set stock\_reco\_qty\_shift from (flt(kwargs.qty\_after\_transaction) − flt(last\_balance)).
  - Otherwise.
    - Set stock\_reco\_qty\_shift from flt(kwargs.actual\_qty).
- Otherwise.
  - If kwargs.get(“serial\_and\_batch\_bundle”).
    - Set stock\_reco\_qty\_shift from flt(kwargs.actual\_qty).
  - Otherwise.
    - Set last\_balance from get\_previous\_sle\_of\_current\_voucher(kwargs, “&lt;=”, exclude\_current\_voucher = true).get(“qty\_after\_transaction”).
    - If last\_balance is distinct from no value.
      - Set stock\_reco\_qty\_shift from (flt(kwargs.qty\_after\_transaction) − flt(last\_balance)).
    - Otherwise.
      - Set stock\_reco\_qty\_shift from kwargs.qty\_after\_transaction.
- Return stock\_reco\_qty\_shift.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L730)

<a id="op-3a23ec77bfbdd4"></a>
### Get next reco datetime condition

`operation_enterprise_stock_stock_ledger_business_behavior_get_next_reco_datetime_condition`

**Inputs** sle, kwargs.

**Explicit results** sle.posting\_datetime ≥ current\_datetime · (sle.posting\_datetime &gt; current\_datetime bitwise or (sle.posting\_datetime equals current\_datetime bitwise and sle.creation &gt; creation)).

**Local steps**

- Set current\_datetime from get\_combine\_datetime(kwargs.get(“posting\_date”), kwargs.get(“posting\_time”)).
- Set creation from kwargs.get(“creation”).
- If not creation.
  - Return sle.posting\_datetime ≥ current\_datetime.
- Return (sle.posting\_datetime &gt; current\_datetime bitwise or (sle.posting\_datetime equals current\_datetime bitwise and sle.creation &gt; creation)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1205) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L720)

<a id="op-d9ef10f78bd458"></a>
### Get next stock reco

`operation_enterprise_stock_stock_ledger_business_behavior_get_next_stock_reco`

**Inputs** kwargs.

**Explicit results** next\_reco.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).orderby(sle.posting\_datetime).orderby(sle.creation).limit(1).
- If Platform.db.db\_type equals “mariadb”.
  - Set query from query.for\_update().
- Set next\_reco from query.run(as\_dict = true).
- If (next\_reco and is\_batch\_reco(next\_reco at 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in next\_reco → is\_batch\_reco(next\_reco at 0).
  - Set next\_reco from query.where(get\_balance\_setting\_reco\_condition(sle, kwargs)).run(as\_dict = true).
- Return next\_reco.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1206) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L721)

<a id="op-b5e790e4eb71c3"></a>
### Is batch reco

`operation_enterprise_binding_enterprise_stock_stock_ledger_is_batch_reco`

**Inputs** reco.

**Explicit results** bool((reco.has\_batch\_no or reco.batch\_no)).

**Local steps**

- Return bool((reco.has\_batch\_no or reco.batch\_no)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in reco.has\_batch\_no → reco.batch\_no.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1597) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1094)

<a id="op-d82ba3006ff5fa"></a>
### Get balance setting reco condition

`operation_enterprise_binding_enterprise_stock_stock_ledger_get_balance_setting_reco_condition`

**Inputs** sle, kwargs.

**Explicit results** condition · ((condition bitwise or sle.batch\_no.isin(batches)) bitwise or sle.serial\_and\_batch\_bundle.isin(bundles\_counting\_batches)).

**Local steps**

- Set condition from (sle.has\_batch\_no equals 0 bitwise and Coalesce(sle.batch\_no, empty text) equals empty text).
- Set batches from get\_batches\_of\_entry(kwargs).
- If not batches.
  - Return condition.
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set bundles\_counting\_batches from nested operand in the contract.qb.from\_(entry).select(entry.parent).where(((entry.warehouse equals kwargs.get(“warehouse”) bitwise and entry.batch\_no.isin(batches)) bitwise and entry.voucher\_type equals “S ….
- Return ((condition bitwise or sle.batch\_no.isin(batches)) bitwise or sle.serial\_and\_batch\_bundle.isin(bundles\_counting\_batches)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1086)

<a id="op-41699899a1a8af"></a>
### Get batches of entry

`operation_enterprise_binding_enterprise_stock_stock_ledger_get_batches_of_entry`

**Inputs** kwargs.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** list(batches).

**Local steps**

- Set batches from (set(kwargs.get(“batch\_no”)) − set(no value, empty text)).
- If kwargs.get(“serial\_and\_batch\_bundle”).
  - Evaluate batches.update(Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → kwargs.get(“serial\_and\_batch\_bundle”), “batch\_no” → tuple(“is”, “set”)), pluck = “batch\_no”)).
- Return list(batches).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1087)

<a id="op-9c2372ffe43199"></a>
### Get datetime limit condition

`operation_enterprise_stock_stock_ledger_business_behavior_get_datetime_limit_condition`

**Inputs** sle, detail.

**Explicit results** (sle.posting\_datetime &lt; posting\_datetime bitwise or (sle.posting\_datetime equals posting\_datetime bitwise and sle.creation &lt; detail.creation)).

**Local steps**

- Set posting\_datetime from get\_combine\_datetime(detail.posting\_date, detail.posting\_time).
- Return (sle.posting\_datetime &lt; posting\_datetime bitwise or (sle.posting\_datetime equals posting\_datetime bitwise and sle.creation &lt; detail.creation)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0941.json#L5620) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L713)

<a id="op-96628e0237498b"></a>
### Validate negative qty in future sle

`operation_enterprise_stock_stock_ledger_business_behavior_validate_negative_quantity_in_future_stock_ledger_entry`

**Inputs** args, allow\_negative\_stock = false.

**Record and data access** read “Stock Reconciliation Item” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with NegativeStockError — message.

**Local steps**

- If (args.voucher\_type equals “Stock Reconciliation” and args.actual\_qty &lt; 0 and args.get(“serial\_and\_batch\_bundle”) and flt(Platform.db.get\_value(“Stock Reconciliation Item”, args.voucher\_detail\_no, “qty”)) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.voucher\_type equals “Stock Reconciliation” → args.actual\_qty &lt; 0 → args.get(“serial\_and\_batch\_bundle”) → flt(Platform.db.get\_value(“Stock Reconciliation Item”, args.voucher\_detail\_no, “qty”)) &gt; 0.
  - Return no value.
- If (allow\_negative\_stock or is\_negative\_stock\_allowed(item\_code = args.item\_code)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in allow\_negative\_stock → is\_negative\_stock\_allowed(item\_code = args.item\_code).
  - If (not allow\_negative\_stock and is\_reserved\_stock\_drawn(args)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not allow\_negative\_stock → is\_reserved\_stock\_drawn(args).
    - Evaluate validate\_reserved\_stock(args).
  - Return no value.
- If (args.actual\_qty ≥ 0 and args.voucher\_type differs from “Stock Reconciliation”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.actual\_qty ≥ 0 → args.voucher\_type differs from “Stock Reconciliation”.
  - Return no value.
- Set neg\_sle from get\_future\_sle\_with\_negative\_qty(args).
- If is\_negative\_with\_precision(neg\_sle).
  - Set message from translated “{0} units of {1} needed in {2} on {3} {4} for {5} to complete this transaction.”.format(abs(neg\_sle at 0 at “qty\_after\_transaction”), Platform.get\_desk\_link(“Item”, args.item\_code, show\_title\_w ….
  - Call the validation error handler Platform.throw(message, NegativeStockError, title = translated “Insufficient Stock”).
- If args.batch\_no.
  - Set neg\_batch\_sle from get\_future\_sle\_with\_negative\_batch\_qty(args).
  - If is\_negative\_with\_precision(neg\_batch\_sle, is\_batch = true).
    - Set message from translated “{0} units of {1} needed in {2} on {3} {4} for {5} to complete this transaction.”.format(abs(neg\_batch\_sle at 0 at “cumulative\_total”), Platform.get\_desk\_link(“Batch”, args.batch\_no), Platform.g ….
    - Call the validation error handler Platform.throw(message, NegativeStockError, title = translated “Insufficient Stock for Batch”).
- If args.reserved\_stock.
  - Evaluate validate\_reserved\_stock(args).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1290) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L799)

<a id="op-db61081e5f8175"></a>
### Is reserved stock drawn

`operation_enterprise_binding_enterprise_stock_stock_ledger_is_reserved_stock_drawn`

**Inputs** sle.

**Record and data access** resolve a document from “Stock Settings” via get\_cached\_doc.

**Explicit results** bool((flt(sle.reserved\_stock) and flt(sle.actual\_qty) &lt; 0 and not sle.get(“is\_cancelled”) and not Platform.get\_cached\_doc(“Stock Settings”).allow\_negative\_stock)).

**Local steps**

- Return bool((flt(sle.reserved\_stock) and flt(sle.actual\_qty) &lt; 0 and not sle.get(“is\_cancelled”) and not Platform.get\_cached\_doc(“Stock Settings”).allow\_negative\_stock)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(sle.reserved\_stock) → flt(sle.actual\_qty) &lt; 0 → not sle.get(“is\_cancelled”) → not Platform.get\_cached\_doc(“Stock Settings”).allow\_negative\_stock.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Stock Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1098)

<a id="op-3df82e1c62a88f"></a>
### Is negative with precision

`operation_enterprise_stock_stock_ledger_business_behavior_is_negative_with_precision`

**Inputs** neg\_sle, is\_batch = false.

**Explicit results** false · (qty\_deficit &lt; 0 and abs(qty\_deficit) &gt; 0.0001).

**Local steps**

- If not neg\_sle.
  - Return false.
- Set field from “cumulative\_total” when is\_batch, otherwise “qty\_after\_transaction”.
  - Value choice on is\_batch — true gives “cumulative\_total”, false gives “qty\_after\_transaction”.
- Set precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- Set qty\_deficit from flt(neg\_sle at 0 at field, precision).
- Return (qty\_deficit &lt; 0 and abs(qty\_deficit) &gt; 0.0001).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty\_deficit &lt; 0 → abs(qty\_deficit) &gt; 0.0001.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0941.json#L6850) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1221) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L736)

<a id="op-71edbf1b95688a"></a>
### Get future sle with negative qty

`operation_enterprise_stock_stock_ledger_business_behavior_get_future_stock_ledger_entry_with_negative_quantity`

**Inputs** sle\_args.

**Record and data access** execute query text (SELECT, Stock Ledger Entry).

**Explicit results** Platform.db.sql(query text (SELECT, Stock Ledger Entry), sle\_args, as\_dict = 1).

**Local steps**

- Return Platform.db.sql(query text (SELECT, Stock Ledger Entry), sle\_args, as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1199) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L715)

<a id="op-5ea99cd3305d95"></a>
### Get future sle with negative batch qty

`operation_enterprise_stock_stock_ledger_business_behavior_get_future_stock_ledger_entry_with_negative_batch_quantity`

**Inputs** sle\_args.

**State and service calls** execute query text (WITH, Stock Ledger Entry).

**Explicit results** Platform.db.sql(query text (WITH, Stock Ledger Entry), sle\_args, as\_dict = 1).

**Local steps**

- Return Platform.db.sql(query text (WITH, Stock Ledger Entry), sle\_args, as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0942.json#L432) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L714)

<a id="op-4c4bcbb59cf884"></a>
### Validate reserved stock

`operation_enterprise_stock_stock_ledger_business_behavior_validate_reserved_stock`

**Inputs** kwargs.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- Set balance\_qty from \_get\_stock\_balance(kwargs.item\_code, kwargs.warehouse).
- Set diff from flt((balance\_qty − kwargs.get(“reserved\_stock”, 0)), precision).
- If (diff &lt; 0 and abs(diff) &gt; 0.0001).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in diff &lt; 0 → abs(diff) &gt; 0.0001.
  - Set msg from translated “{0} units of {1} needed in {2} on {3} {4} to complete this transaction.”.format(abs(diff), Platform.get\_desk\_link(“Item”, kwargs.item\_code, show\_title\_with\_name = true), Platform.get\_desk\_link( ….
  - Call the validation error handler Platform.throw(msg, title = translated “Reserved Stock”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1293) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L802)

<a id="op-9e7013c2c14c2a"></a>
### Validate reserved serial nos

`operation_enterprise_stock_stock_ledger_business_behavior_validate_reserved_serial_numbers`

**Inputs** item\_code, warehouse, serial\_nos.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If reserved\_serial\_nos\_details bound to get\_sre\_reserved\_serial\_nos\_details(item\_code, warehouse, serial\_nos).
  - If common\_serial\_nos bound to list(set(serial\_nos).intersection(set(reserved\_serial\_nos\_details.keys()))).
    - Set msg from translated “Serial Nos are reserved in Stock Reservation Entries, you need to unreserve them before proceeding.”.
    - Update msg using + text in the contract.
    - Update msg using + translated “Example: Serial No {0} reserved in {1}.”.format(Platform.bold(common\_serial\_nos at 0), Platform.get\_desk\_link(“Stock Reservation Entry”, reserved\_serial\_nos\_details at common\_serial\_nos at 0)).
    - Call the validation error handler Platform.throw(msg, title = translated “Reserved Serial No.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0942.json#L969) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1292) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L801)

<a id="op-ed9925866376ae"></a>
### Validate reserved batch nos

`operation_enterprise_stock_stock_ledger_business_behavior_validate_reserved_batch_numbers`

**Inputs** item\_code, warehouse, batch\_nos.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If reserved\_batches\_map bound to get\_sre\_reserved\_batch\_nos\_details(item\_code, warehouse, batch\_nos).
  - Set available\_batches from get\_auto\_batch\_nos(Platform.\_dict(mapping(“item\_code” → item\_code, “warehouse” → warehouse, “posting\_datetime” → get\_combine\_datetime(nowdate(), nowtime())))).
  - Set available\_batches\_map from mapping of row.batch\_no → row.qty for row drawn from available\_batches.
    - Draw row from available\_batches.
  - Set precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
  - For each batch\_no in batch\_nos.
    - Set diff from flt((available\_batches\_map.get(batch\_no, 0) − reserved\_batches\_map.get(batch\_no, 0)), precision).
    - If (diff &lt; 0 and abs(diff) &gt; 0.0001).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in diff &lt; 0 → abs(diff) &gt; 0.0001.
      - Set msg from translated “{0} units of {1} needed in {2} on {3} {4} to complete this transaction.”.format(abs(diff), Platform.get\_desk\_link(“Batch”, batch\_no), Platform.get\_desk\_link(“Warehouse”, warehouse), nowdate(), …).
      - Call the validation error handler Platform.throw(msg, title = translated “Reserved Stock for Batch”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0942.json#L1332) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1291) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L800)

<a id="op-9c711527b3fdd6"></a>
### Is negative stock allowed

`operation_enterprise_stock_stock_ledger_business_behavior_is_negative_stock_allowed`

**Inputs** item\_code (named only, default no value).

**Declared result** bool.

**Record and data access** resolve a document from “Stock Settings” via get\_cached\_doc · read “Item” via get\_cached\_value.

**Explicit results** true · false.

**Local steps**

- If Platform.get\_cached\_doc(“Stock Settings”).allow\_negative\_stock.
  - Return true.
- If (item\_code and cint(Platform.get\_cached\_value(“Item”, item\_code, “allow\_negative\_stock”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_code → cint(Platform.get\_cached\_value(“Item”, item\_code, “allow\_negative\_stock”)).
  - Return true.
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Stock Settings”), Platform.get\_cached\_value(“Item”, item\_code, “allow\_negative\_stock”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0942.json#L1992) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1220) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L735)

<a id="op-302c8022939a5e"></a>
### Get incoming rate for inter company transfer

`operation_enterprise_stock_stock_ledger_business_behavior_get_incoming_rate_for_inter_company_transfer`

**Inputs** sle.

**Declared result** float.

**Record and data access** read (sle.voucher\_type + “ Item”) via get\_cached\_value · read “Purchase Receipt Item” via get\_cached\_value · read doctype via get\_cached\_value · read formatted text {sle.voucher\_type} Item via get\_value.

**Explicit results** (rate + lcv\_rate).

**Local steps**

- Set rate from 0.0.
- Set lcv\_rate from 0.0.
- Set field from “delivery\_note\_item” when sle.voucher\_type equals “Purchase Receipt”, otherwise “sales\_invoice\_item”.
  - Value choice on sle.voucher\_type equals “Purchase Receipt” — true gives “delivery\_note\_item”, false gives “sales\_invoice\_item”.
- Set doctype from “Delivery Note Item” when sle.voucher\_type equals “Purchase Receipt”, otherwise “Sales Invoice Item”.
  - Value choice on sle.voucher\_type equals “Purchase Receipt” — true gives “Delivery Note Item”, false gives “Sales Invoice Item”.
- Set reference\_name from Platform.get\_cached\_value((sle.voucher\_type + “ Item”), sle.voucher\_detail\_no, field).
- If (sle.voucher\_type equals “Purchase Receipt” and not reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Purchase Receipt” → not reference\_name.
  - Set doctype from “Packed Item”.
  - Set reference\_name from Platform.get\_cached\_value(“Purchase Receipt Item”, sle.voucher\_detail\_no, “delivery\_note\_packed\_item”).
- If reference\_name.
  - Set rate from Platform.get\_cached\_value(doctype, reference\_name, “incoming\_rate”).
- Set lcv\_amount from Platform.db.get\_value(formatted text {sle.voucher\_type} Item, sle.voucher\_detail\_no, “landed\_cost\_voucher\_amount”).
- If lcv\_amount.
  - Set lcv\_rate from flt((lcv\_amount ÷ abs(sle.actual\_qty))).
- Return (rate + lcv\_rate).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value((sle.voucher\_type + “ Item”), sle.voucher\_detail\_no, field), Platform.get\_cached\_value(“Purchase Receipt Item”, sle.voucher\_detail\_no, “delivery\_note\_packed\_item”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1200) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L716)

<a id="op-b3face84c22ba1"></a>
### Is internal transfer

`operation_enterprise_stock_stock_ledger_business_behavior_is_internal_transfer`

**Inputs** sle.

**Record and data access** read sle.voucher\_type via get\_cached\_value.

**Explicit results** true.

**Local steps**

- Set data from Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, list(“is\_internal\_supplier”, “represents\_company”, “company”), as\_dict = true).
- If (data.is\_internal\_supplier and data.represents\_company equals data.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.is\_internal\_supplier → data.represents\_company equals data.company.
  - Return true.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, list(“is\_internal\_supplier”, “represents\_company”, “company”), as\_dict = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0942.json#L2570) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1219) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L734)
