# Inventory and warehouses · operations 59

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Serial and batch bundle

[Record definition](../../../../data/record-types/serial_and_batch_bundle.json)

<a id="op-aa40e66d5f3def"></a>
### Get reserved batches for pos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_reserved_batches_for_point_of_sale`

**Inputs** kwargs.

**Declared result** dict.

**Explicit results** pos\_batches.

**Local steps**

- Set pos\_batches from Platform.\_dict().
- Set POS\_Invoice from Platform.qb.DocType(“POS Invoice”).
- Set POS\_Invoice\_Item from Platform.qb.DocType(“POS Invoice Item”).
- Set pos\_invoices from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(POS\_Invoice\_Item.batch\_no, POS\_Invoice\_Item.qty, P ….
- If kwargs.get(“company”).
  - Set pos\_invoices from pos\_invoices.where(POS\_Invoice.company equals kwargs.get(“company”)).
- If kwargs.get(“ignore\_voucher\_nos”).
  - Set pos\_invoices from pos\_invoices.where(POS\_Invoice.name.notin(kwargs.get(“ignore\_voucher\_nos”))).
- If kwargs.get(“warehouse”).
  - Set warehouses from kwargs.warehouse when isinstance(kwargs.warehouse, list), otherwise list(kwargs.warehouse).
    - Value choice on isinstance(kwargs.warehouse, list) — true gives kwargs.warehouse, false gives list(kwargs.warehouse).
  - Set pos\_invoices from pos\_invoices.where(POS\_Invoice\_Item.warehouse.isin(warehouses)).
- Set pos\_invoices from pos\_invoices.run(as\_dict = true).
- Set batch\_nos from (kwargs.get(“batch\_no”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.get(“batch\_no”) → list().
- If isinstance(batch\_nos, str).
  - Set batch\_nos from list(batch\_nos).
- Set ids from list of pos\_invoice.serial\_and\_batch\_bundle for pos\_invoice drawn from pos\_invoices where (pos\_invoice.serial\_and\_batch\_bundle and not pos\_invoice.use\_serial\_batch\_fields).
  - Draw pos\_invoice from pos\_invoices, keep a combination only if ((pos\_invoice.serial\_and\_batch\_bundle and not pos\_invoice.use\_serial\_batch\_fields)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pos\_invoice.serial\_and\_batch\_bundle → not pos\_invoice.use\_serial\_batch\_fields.
- If ids.
  - For each d in \_get\_serial\_batch\_ledgers(kwargs.item\_code, docstatus = 1, name = ids).
    - If (batch\_nos and d.batch\_no does not belong to batch\_nos).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_nos → d.batch\_no does not belong to batch\_nos.
      - Continue with the next iteration or loop test.
    - Set key from tuple(d.batch\_no, d.warehouse).
    - If key does not belong to pos\_batches.
      - Set pos\_batches at key from Platform.\_dict(mapping(“qty” → d.qty, “warehouse” → d.warehouse)).
    - Otherwise.
      - Update pos\_batches at key.qty using + d.qty.
- For each row in pos\_invoices.
  - If (not row.batch\_no or row.serial\_and\_batch\_bundle belongs to ids).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.batch\_no → row.serial\_and\_batch\_bundle belongs to ids.
    - Continue with the next iteration or loop test.
  - If (batch\_nos and row.batch\_no does not belong to batch\_nos).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_nos → row.batch\_no does not belong to batch\_nos.
    - Continue with the next iteration or loop test.
  - Set key from tuple(row.batch\_no, row.warehouse).
  - If key belongs to pos\_batches.
    - Update pos\_batches at key at “qty” using + (row.qty × negative 1).
  - Otherwise.
    - Set pos\_batches at key from Platform.\_dict(mapping(“qty” → (row.qty × negative 1), “warehouse” → row.warehouse)).
- Return pos\_batches.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L877) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L523)

<a id="op-59230c4b5798f0"></a>
### Get reserved batches for sre

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_reserved_batches_for_stock_reservation_entry`

**Inputs** kwargs.

**Declared result** dict.

**Explicit results** reserved\_batches\_details.

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set sb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sb\_entry.batch\_no, sre.warehouse, nested operand in the contract.as\_(“qty”)).where((((nested operand in the contract equals nested oper ….
- If kwargs.get(“company”).
  - Set query from query.where(sre.company equals kwargs.get(“company”)).
- If kwargs.batch\_no.
  - If isinstance(kwargs.batch\_no, list).
    - Set query from query.where(sb\_entry.batch\_no.isin(kwargs.batch\_no)).
  - Otherwise.
    - Set query from query.where(sb\_entry.batch\_no equals kwargs.batch\_no).
- If kwargs.warehouse.
  - If isinstance(kwargs.warehouse, list).
    - Set query from query.where(sre.warehouse.isin(kwargs.warehouse)).
  - Otherwise.
    - Set query from query.where(sre.warehouse equals kwargs.warehouse).
- If kwargs.ignore\_voucher\_nos.
  - Set query from query.where(sre.name.notin(kwargs.ignore\_voucher\_nos)).
- Set data from query.run(as\_dict = true).
- Set reserved\_batches\_details from Platform.\_dict().
- If data.
  - Set reserved\_batches\_details from Platform.\_dict(mapping of tuple(d.batch\_no, d.warehouse) → Platform.\_dict(mapping(“warehouse” → d.warehouse, “qty” → d.qty)) for d drawn from data).
    - Draw d from data.
- Return reserved\_batches\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0811.json#L4391) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L878) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L524)

<a id="op-c31c6b3b3a4758"></a>
### Get batch qty for stock

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_get_batch_qty_for_stock`

**Inputs** batch\_no = no value, warehouse = no value, posting\_date = no value, posting\_time = no value, remaining named values kwargs.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** sum(generator of row.qty for row drawn from batches where row.batch\_no equals batch\_no) · batches.

**Local steps**

- Set kwargs from Platform.\_dict(kwargs).
- Evaluate kwargs.update(batch\_no = batch\_no, warehouse = warehouse, based\_on = Platform.get\_single\_value(“Stock Settings”, “pick\_serial\_and\_batch\_based\_on”)).
- If (not kwargs.posting\_datetime and posting\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not kwargs.posting\_datetime → posting\_date.
  - Set kwargs.posting\_datetime from combine\_datetime(posting\_date, posting\_time).
- Set batches from get\_auto\_batch\_nos(kwargs).
- If (batch\_no and warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_no → warehouse.
  - Return sum(generator of row.qty for row drawn from batches where row.batch\_no equals batch\_no).
    - Draw row from batches, keep a combination only if (row.batch\_no equals batch\_no).
- Return batches.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “pick\_serial\_and\_batch\_based\_on”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1077) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L574)

<a id="op-8a6907725eb89e"></a>
### Get auto batch nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_auto_batch_numbers`

**Inputs** kwargs.

**Explicit results** available\_batches · get\_qty\_based\_available\_batches(available\_batches, qty).

**Local steps**

- If (kwargs.against\_sales\_order and only\_consider\_batches bound to get\_batches\_to\_be\_considered(kwargs.against\_sales\_order)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs.against\_sales\_order → only\_consider\_batches bound to get\_batches\_to\_be\_considered(kwargs.against\_sales\_order).
  - Set tuple(batches, warehouses) from tuple(list(), list()).
  - For each item in only\_consider\_batches.
    - Evaluate batches.append(item.batch\_no).
    - Evaluate warehouses.append(item.warehouse).
  - If batches.
    - Set kwargs.batch\_no from batches.
    - Set kwargs.warehouse from warehouses.
- If (not kwargs.get(“posting\_datetime”) and kwargs.get(“posting\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not kwargs.get(“posting\_datetime”) → kwargs.get(“posting\_date”).
  - Set kwargs at “posting\_datetime” from combine\_datetime(kwargs.get(“posting\_date”), kwargs.get(“posting\_time”)).
- Set available\_batches from get\_available\_batches(kwargs).
- Set stock\_ledgers\_batches from get\_stock\_ledgers\_batches(kwargs).
- Set pos\_invoice\_batches from Platform.\_dict().
- If not kwargs.for\_stock\_levels.
  - Set pos\_invoice\_batches from get\_reserved\_batches\_for\_pos(kwargs).
- Set sre\_reserved\_batches from Platform.\_dict().
- If not kwargs.ignore\_reserved\_stock.
  - Set sre\_reserved\_batches from get\_reserved\_batches\_for\_sre(kwargs).
- If (kwargs.against\_sales\_order and only\_consider\_batches).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs.against\_sales\_order → only\_consider\_batches.
  - Set kwargs.batch\_no, kwargs.warehouse from no value.
- Set picked\_batches from Platform.\_dict().
- If kwargs.get(“is\_pick\_list”).
  - Set picked\_batches from get\_picked\_batches(kwargs).
- Evaluate update\_available\_batches(available\_batches, stock\_ledgers\_batches).
- Evaluate update\_available\_batches(available\_batches, pos\_invoice\_batches, sre\_reserved\_batches, picked\_batches, add\_missing = false, …).
- If kwargs.based\_on equals “Expiry”.
  - Set available\_batches from sorted(available\_batches, key = deferred anonymous expression).
- If (not kwargs.get(“do\_not\_check\_future\_batches”) and available\_batches and kwargs.get(“posting\_datetime”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not kwargs.get(“do\_not\_check\_future\_batches”) → available\_batches → kwargs.get(“posting\_datetime”).
  - Evaluate filter\_zero\_near\_batches(available\_batches, kwargs).
- If not kwargs.consider\_negative\_batches.
  - Set precision from Platform.get\_precision(“Stock Ledger Entry”, “actual\_qty”).
  - Set available\_batches from list of d for d drawn from available\_batches where flt(d.qty, precision) &gt; 0.
    - Draw d from available\_batches, keep a combination only if (flt(d.qty, precision) &gt; 0).
- Set qty from flt(kwargs.qty).
- If not qty.
  - Return available\_batches.
- Return get\_qty\_based\_available\_batches(available\_batches, qty).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L857) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L505)

<a id="op-581d6a11f1bae5"></a>
### Get batch nos from sre

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_batch_numbers_from_stock_reservation_entry`

**Inputs** kwargs.

**Explicit results** get\_qty\_based\_available\_batches(result, flt(kwargs.qty)) when flt(kwargs.qty), otherwise result.

**Local steps**

- Bind dependencies Sum.
- Set table from Platform.qb.DocType(“Stock Reservation Entry”).
- Set child\_table from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
- Set result from query.run(as\_dict = true).
- Return get\_qty\_based\_available\_batches(result, flt(kwargs.qty)) when flt(kwargs.qty), otherwise result.
  - Value choice on flt(kwargs.qty) — true gives get\_qty\_based\_available\_batches(result, flt(kwargs.qty)), false gives result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0812.json#L689) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L864) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L512)

<a id="op-229ed2c1c4d64b"></a>
### Get batches to be considered

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_batches_to_be_considered`

**Inputs** sales\_order\_name.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set parent from Platform.qb.DocType(“Stock Reservation Entry”).
- Set child from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(child.batch\_no, child.warehouse).distinct().where(((parent.docstatus equals 1 bitwise and parent.voucher\_no equals sales\_order\_name) bi ….
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0812.json#L1261) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L865) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L513)

<a id="op-0febd6cbaa017a"></a>
### Filter zero near batches

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_filter_zero_near_batches`

**Inputs** available\_batches, kwargs.

**Local steps**

- Set kwargs.batch\_no from list of d.batch\_no for d drawn from available\_batches.
  - Draw d from available\_batches.
- Remove kwargs at “posting\_datetime”.
- Set kwargs.do\_not\_check\_future\_batches from 1.
- Set available\_batches\_in\_future from get\_auto\_batch\_nos(kwargs).
- For each batch in available\_batches.
  - <a id="op-0febd6cbaa017a-guard-9"></a>If batch.qty ≤ 0.
    - Continue with the next iteration or loop test.
  - For each future\_batch in available\_batches\_in\_future.
    - If (batch.batch\_no equals future\_batch.batch\_no and batch.warehouse equals future\_batch.warehouse and future\_batch.qty ≤ 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch.batch\_no equals future\_batch.batch\_no → batch.warehouse equals future\_batch.warehouse → future\_batch.qty ≤ 0.
      - Set batch.qty from 0.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison batch.qty ≤ 0, batch.qty = 0 selects the branch that continues with the next loop iteration. With batch.qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-0febd6cbaa017a-guard-9)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0812.json#L1613) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L856) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L504)

<a id="op-7e47cf0b6a05e8"></a>
### Get qty based available batches

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_quantity_based_available_batches`

**Inputs** available\_batches, qty.

**Explicit results** batches.

**Local steps**

- Set precision from Platform.get\_precision(“Stock Ledger Entry”, “actual\_qty”).
- Set batches from list().
- For each batch in available\_batches.
  - If flt(qty, precision) ≤ 0.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set batch\_qty from flt(batch.qty).
  - If qty &gt; batch\_qty.
    - Evaluate batches.append(Platform.\_dict(mapping(“batch\_no” → batch.batch\_no, “qty” → batch\_qty, “warehouse” → batch.warehouse))).
    - Update qty using − batch\_qty.
  - Otherwise.
    - Evaluate batches.append(Platform.\_dict(mapping(“batch\_no” → batch.batch\_no, “qty” → qty, “warehouse” → batch.warehouse))).
    - Set qty from 0.
- Return batches.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L875) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L521)

<a id="op-de0a86f565ee29"></a>
### Update available batches

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_update_available_batches`

**Inputs** available\_batches, remaining positional values reserved\_batches, add\_missing (named only, default true).

**Declared result** no value.

**Local steps**

- Set precision from Platform.get\_precision(“Stock Ledger Entry”, “actual\_qty”).
- For each batches in reserved\_batches.
  - If batches.
    - For each tuple(key, data) in batches.items().
      - Set tuple(batch\_no, warehouse) from key.
      - Set batch\_not\_exists from true.
      - For each batch in available\_batches.
        - If (batch.batch\_no equals batch\_no and batch.warehouse equals warehouse).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch.batch\_no equals batch\_no → batch.warehouse equals warehouse.
          - Set batch.qty from flt((batch.qty + data.qty), precision).
          - Set batch\_not\_exists from false.
      - If (batch\_not\_exists and add\_missing).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_not\_exists → add\_missing.
        - Evaluate available\_batches.append(data).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L977) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L621)

<a id="op-56d3c0b8296150"></a>
### Get available batches

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_available_batches`

**Inputs** kwargs.

**Explicit results** data.

**Local steps**

- Set stock\_ledger\_entry from Platform.qb.DocType(“Stock Ledger Entry”).
- Set batch\_ledger from Platform.qb.DocType(“Serial and Batch Entry”).
- Set batch\_table from Platform.qb.DocType(“Batch”).
- Set query from nested operand in the contract(nested operand in the contract).select(batch\_ledger.batch\_no, batch\_ledger.warehouse, nested operand in the contract.as\_(“qty”), batch\_table.expiry\_date).where(stock\_ledger\_e ….
- If kwargs.get(“company”).
  - Set query from query.where(stock\_ledger\_entry.company equals kwargs.get(“company”)).
- If not kwargs.get(“for\_stock\_levels”).
  - Set query from query.where(batch\_table.disabled equals 0).
  - Set query from query.where((batch\_table.expiry\_date ≥ today() bitwise or batch\_table.expiry\_date.isnull())).
- If kwargs.get(“posting\_datetime”).
  - Set timestamp\_condition from stock\_ledger\_entry.posting\_datetime ≤ kwargs.posting\_datetime.
  - If kwargs.get(“creation”).
    - Set timestamp\_condition from stock\_ledger\_entry.posting\_datetime &lt; kwargs.posting\_datetime.
    - Update timestamp\_condition using bitwise or (stock\_ledger\_entry.posting\_datetime equals kwargs.posting\_datetime bitwise and stock\_ledger\_entry.creation &lt; kwargs.creation).
  - Set query from query.where(timestamp\_condition).
- For each field in list(“warehouse”, “item\_code”).
  - If not kwargs.get(field).
    - Continue with the next iteration or loop test.
  - If isinstance(kwargs.get(field), list).
    - Set query from query.where(stock\_ledger\_entry at field.isin(kwargs.get(field))).
  - Otherwise.
    - Set query from query.where(stock\_ledger\_entry at field equals kwargs.get(field)).
- If kwargs.get(“batch\_no”).
  - If isinstance(kwargs.batch\_no, list).
    - Set query from query.where(batch\_ledger.batch\_no.isin(kwargs.batch\_no)).
  - Otherwise.
    - Set query from query.where(batch\_ledger.batch\_no equals kwargs.batch\_no).
- If kwargs.based\_on equals “LIFO”.
  - Set query from query.orderby(batch\_table.creation, order = Platform.qb.desc).
- Otherwise.
  - If kwargs.based\_on equals “Expiry”.
    - Set query from query.orderby(batch\_table.expiry\_date).
  - Otherwise.
    - Set query from query.orderby(batch\_table.creation).
- If kwargs.get(“ignore\_voucher\_nos”).
  - Set query from query.where(stock\_ledger\_entry.voucher\_no.notin(kwargs.get(“ignore\_voucher\_nos”))).
- Set data from query.run(as\_dict = true).
- Return data.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L859) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L507)

<a id="op-490843f10a0bf4"></a>
### Get voucher wise serial batch from bundle

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_voucher_wise_serial_batch_from_bundle`

**Inputs** remaining named values kwargs.

**Declared result** dict at tuple(str, dict).

**Record and data access** read doctype via get\_cached\_value.

**Explicit results** mapping() · group\_by\_voucher.

**Local steps**

- Set data from get\_ledgers\_from\_serial\_batch\_bundle(expanded names kwargs).
- If not data.
  - Return mapping().
- Set group\_by\_voucher from mapping().
- For each row in data.
  - Set key from tuple(row.item\_code, row.warehouse, row.voucher\_no).
  - If kwargs.get(“get\_subcontracted\_item”).
    - Set tuple(doctype, field\_name) from kwargs.get(“get\_subcontracted\_item”).
    - Set subcontracted\_item\_code from Platform.get\_cached\_value(doctype, row.voucher\_detail\_no, field\_name).
    - Set key from tuple(row.item\_code, subcontracted\_item\_code, row.warehouse, row.voucher\_no).
  - If key does not belong to group\_by\_voucher.
    - Evaluate group\_by\_voucher.setdefault(key, Platform.\_dict(mapping(“serial\_nos” → list(), “batch\_nos” → defaultdict(float), “item\_row” → row))).
  - Set child\_row from group\_by\_voucher at key.
  - If row.serial\_no.
    - Evaluate child\_row at “serial\_nos”.append(row.serial\_no).
    - Set child\_row at “item\_row”.qty from (len(child\_row at “serial\_nos”) × negative 1 when row.type\_of\_transaction equals “Outward”, otherwise 1).
      - Value choice on row.type\_of\_transaction equals “Outward” — true gives negative 1, false gives 1.
  - If row.batch\_no.
    - Update child\_row at “batch\_nos” at row.batch\_no using + row.qty.
- Return group\_by\_voucher.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(doctype, row.voucher\_detail\_no, field\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0812.json#L4215) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L895) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L541)

<a id="op-ec3b86db659d5f"></a>
### Get picked batches

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_picked_batches`

**Inputs** kwargs.

**Declared result** dict at tuple(str, dict).

**Explicit results** picked\_batches.

**Local steps**

- Set picked\_batches from Platform.\_dict().
- Set child\_table from Platform.qb.DocType(“Serial and Batch Entry”).
- Set pick\_list\_table from Platform.qb.DocType(“Pick List”).
- Set query from nested operand in the contract(nested operand in the contract).select(child\_table.batch\_no, child\_table.warehouse, nested operand in the contract.as\_(“qty”)).where(((((nested operand in the contract bitwis ….
- If kwargs.get(“company”).
  - Set query from query.where(pick\_list\_table.company equals kwargs.get(“company”)).
- If kwargs.get(“item\_code”).
  - Set query from query.where(child\_table.item\_code equals kwargs.get(“item\_code”)).
- If kwargs.get(“warehouse”).
  - If isinstance(kwargs.warehouse, list).
    - Set query from query.where(child\_table.warehouse.isin(kwargs.warehouse)).
  - Otherwise.
    - Set query from query.where(child\_table.warehouse equals kwargs.get(“warehouse”)).
- Set data from query.run(as\_dict = true).
- For each row in data.
  - If not row.qty.
    - Continue with the next iteration or loop test.
  - Set key from tuple(row.batch\_no, row.warehouse).
  - If key does not belong to picked\_batches.
    - Set picked\_batches at key from Platform.\_dict(mapping(“qty” → row.qty, “warehouse” → row.warehouse)).
  - Otherwise.
    - Update picked\_batches at key.qty using + row.qty.
- Return picked\_batches.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L873) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L519)

<a id="op-b8c7f2ae618501"></a>
### Get picked serial nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_picked_serial_numbers`

**Inputs** item\_code, warehouse = no value.

**Declared result** list at str.

**Explicit results** list() · list of row.serial\_no for row drawn from data where row.serial\_no.

**Local steps**

- Set child\_table from Platform.qb.DocType(“Serial and Batch Entry”).
- Set pick\_list\_table from Platform.qb.DocType(“Pick List”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.voucher\_no equals nested operand in the contract.name).select(child\_table.serial\_no).where((((((nested opera ….
- If item\_code.
  - Set query from query.where(child\_table.item\_code equals item\_code).
- If warehouse.
  - If isinstance(warehouse, list).
    - Set query from query.where(child\_table.warehouse.isin(warehouse)).
  - Otherwise.
    - Set query from query.where(child\_table.warehouse equals warehouse).
- Set data from query.run(as\_dict = true).
- If not data.
  - Return list().
- Return list of row.serial\_no for row drawn from data where row.serial\_no.
  - Draw row from data, keep a combination only if (row.serial\_no).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L874) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L520)

<a id="op-e7eda62e3a1f2e"></a>
### Get ledgers from serial batch bundle

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_ledgers_from_serial_batch_bundle`

**Inputs** remaining named values kwargs.

**Declared result** list at Platform.\_dict.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- Set bundle\_table from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set serial\_batch\_table from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(serial\_batch\_table.serial\_no, bundle\_table.warehouse, bundle\_table.item\_code, serial\_batch\_table.batch\_no, …).where(((nested operand in ….
- For each tuple(key, val) in kwargs.items().
  - If val is identical to no value.
    - Continue with the next iteration or loop test.
  - If (not val and isinstance(val, list)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not val → isinstance(val, list).
    - Return list().
  - If key equals “get\_subcontracted\_item”.
    - Continue with the next iteration or loop test.
  - If key belongs to list(“name”, “item\_code”, “warehouse”, “voucher\_no”, …).
    - If isinstance(val, list).
      - Set query from query.where(bundle\_table at key.isin(val)).
    - Otherwise.
      - Set query from query.where(bundle\_table at key equals val).
  - Otherwise.
    - If key belongs to list(“posting\_datetime”).
      - Set query from query.where(bundle\_table at key ≥ val).
    - Otherwise.
      - If isinstance(val, list).
        - Set query from query.where(serial\_batch\_table at key.isin(val)).
      - Otherwise.
        - Set query from query.where(serial\_batch\_table at key equals val).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0813.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L870) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L516)

<a id="op-a65fcc4bd6ea0e"></a>
### Get stock ledgers for serial nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_stock_ledgers_for_serial_numbers`

**Inputs** kwargs.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set stock\_ledger\_entry from Platform.qb.DocType(“Stock Ledger Entry”).
- Set serial\_batch\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.is\_cancel ….
- If kwargs.get(“posting\_datetime”).
  - Set timestamp\_condition from stock\_ledger\_entry.posting\_datetime ≤ kwargs.posting\_datetime.
  - If kwargs.get(“creation”).
    - Set timestamp\_condition from stock\_ledger\_entry.posting\_datetime &lt; kwargs.posting\_datetime.
    - Update timestamp\_condition using bitwise or (stock\_ledger\_entry.posting\_datetime equals kwargs.posting\_datetime bitwise and stock\_ledger\_entry.creation &lt; kwargs.creation).
  - Set query from query.where(timestamp\_condition).
- For each field in list(“warehouse”, “item\_code”).
  - If not kwargs.get(field).
    - Continue with the next iteration or loop test.
  - If isinstance(kwargs.get(field), list).
    - Set query from query.where(stock\_ledger\_entry at field.isin(kwargs.get(field))).
  - Otherwise.
    - Set query from query.where(stock\_ledger\_entry at field equals kwargs.get(field)).
- Set serial\_nos from (kwargs.get(“serial\_nos”) or kwargs.get(“serial\_no”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.get(“serial\_nos”) → kwargs.get(“serial\_no”).
- If (serial\_nos and not isinstance(serial\_nos, list)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in serial\_nos → not isinstance(serial\_nos, list).
  - Set serial\_nos from list(serial\_nos).
- If serial\_nos.
  - Bind dependencies re.
  - Set escaped\_serial\_nos from list of re.escape(sn) for sn drawn from serial\_nos where sn.
    - Draw sn from serial\_nos, keep a combination only if (sn).
  - Set regex\_pattern from ((“\\n(” + “\|”.join(escaped\_serial\_nos)) + “)\\n”).
  - Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.serial\_and\_batch\_bundle equals nested operand in the contract.parent).where((nested operand in the contract. …().
- If kwargs.ignore\_voucher\_detail\_no.
  - Set query from query.where(stock\_ledger\_entry.voucher\_detail\_no differs from kwargs.ignore\_voucher\_detail\_no).
- Otherwise.
  - If kwargs.voucher\_no.
    - Set query from query.where(stock\_ledger\_entry.voucher\_no differs from kwargs.voucher\_no).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L892) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L538)

<a id="op-a52de997bb96f7"></a>
### Get stock ledgers batches

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_stock_ledgers_batches`

**Inputs** kwargs.

**Explicit results** batches.

**Local steps**

- Set stock\_ledger\_entry from Platform.qb.DocType(“Stock Ledger Entry”).
- Set batch\_table from Platform.qb.DocType(“Batch”).
- Set query from nested operand in the contract(nested operand in the contract).select(stock\_ledger\_entry.warehouse, stock\_ledger\_entry.item\_code, nested operand in the contract.as\_(“qty”), stock\_ledger\_entry.batch\_no, …). ….
- If kwargs.get(“company”).
  - Set query from query.where(stock\_ledger\_entry.company equals kwargs.get(“company”)).
- For each field in list(“warehouse”, “item\_code”, “batch\_no”).
  - If not kwargs.get(field).
    - Continue with the next iteration or loop test.
  - If isinstance(kwargs.get(field), list).
    - Set query from query.where(stock\_ledger\_entry at field.isin(kwargs.get(field))).
  - Otherwise.
    - Set query from query.where(stock\_ledger\_entry at field equals kwargs.get(field)).
- If not kwargs.get(“for\_stock\_levels”).
  - Set query from query.where((batch\_table.expiry\_date ≥ today() bitwise or batch\_table.expiry\_date.isnull())).
- If kwargs.get(“posting\_datetime”).
  - Set timestamp\_condition from stock\_ledger\_entry.posting\_datetime ≤ kwargs.posting\_datetime.
  - If kwargs.get(“creation”).
    - Set timestamp\_condition from stock\_ledger\_entry.posting\_datetime &lt; kwargs.posting\_datetime.
    - Update timestamp\_condition using bitwise or (stock\_ledger\_entry.posting\_datetime equals kwargs.posting\_datetime bitwise and stock\_ledger\_entry.creation &lt; kwargs.creation).
  - Set query from query.where(timestamp\_condition).
- If kwargs.get(“ignore\_voucher\_nos”).
  - Set query from query.where(stock\_ledger\_entry.voucher\_no.notin(kwargs.get(“ignore\_voucher\_nos”))).
- If kwargs.based\_on equals “LIFO”.
  - Set query from query.orderby(batch\_table.creation, order = Platform.qb.desc).
- Otherwise.
  - If kwargs.based\_on equals “Expiry”.
    - Set query from query.orderby(batch\_table.expiry\_date).
  - Otherwise.
    - Set query from query.orderby(batch\_table.creation).
- Set data from query.run(as\_dict = true).
- Set batches from mapping().
- For each d in data.
  - Set key from tuple(d.batch\_no, d.warehouse).
  - If key does not belong to batches.
    - Set batches at key from d.
  - Otherwise.
    - Update batches at key.qty using + d.qty.
- Return batches.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L891) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L537)

<a id="op-be03be6959ea75"></a>
### Get batch no from serial no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_batch_number_from_serial_number`

**Inputs** serial\_no.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Serial No” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Serial No”, serial\_no, “batch\_no”).

**Local steps**

- Return Platform.get\_cached\_value(“Serial No”, serial\_no, “batch\_no”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Serial No”, serial\_no, “batch\_no”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L863) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L511)

<a id="op-194ba44170fc9d"></a>
### Is serial batch no exists

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_is_serial_batch_number_exists`

**Inputs** item\_code, type\_of\_transaction, serial\_no = no value, batch\_no = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Serial No” via exists · read “Batch” via exists.

**Explicit failure paths** validation helper — translated “Serial No {0} does not exists”.format(serial\_no) · validation helper — translated “Batch No {0} does not exists”.format(batch\_no).

**Local steps**

- Evaluate Platform.has\_permission(“Item”, ptype = “select”, throw = true).
- If (serial\_no and not Platform.db.exists(“Serial No”, serial\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in serial\_no → not Platform.db.exists(“Serial No”, serial\_no).
  - If type\_of\_transaction differs from “Inward”.
    - Call the validation error handler Platform.throw(translated “Serial No {0} does not exists”.format(serial\_no)).
  - Evaluate Platform.has\_permission(“Serial and Batch Bundle”, “create”, throw = true).
  - Evaluate make\_serial\_no(serial\_no, item\_code).
- If (batch\_no and not Platform.db.exists(“Batch”, batch\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_no → not Platform.db.exists(“Batch”, batch\_no).
  - If type\_of\_transaction differs from “Inward”.
    - Call the validation error handler Platform.throw(translated “Batch No {0} does not exists”.format(batch\_no)).
  - Evaluate Platform.has\_permission(“Serial and Batch Bundle”, “create”, throw = true).
  - Evaluate make\_batch\_no(batch\_no, item\_code).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, ptype = “select”, throw = true), Platform.has\_permission(“Serial and Batch Bundle”, “create”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L897) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L543)

<a id="op-0b68678de41643"></a>
### Make serial no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_make_serial_number`

**Inputs** serial\_no, item\_code.

**State and service calls** request new\_doc for “Serial No” · call save on serial\_no\_doc.

**Local steps**

- Set serial\_no\_doc from Platform.new\_doc(“Serial No”).
- Set serial\_no\_doc.serial\_no from serial\_no.
- Set serial\_no\_doc.item\_code from item\_code.
- Evaluate serial\_no\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0813.json#L4329) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L901) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L547)

<a id="op-365cbd495dd860"></a>
### Make batch no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_make_batch_number`

**Inputs** batch\_no, item\_code.

**State and service calls** request new\_doc for “Batch” · call save on batch\_doc.

**Local steps**

- Set batch\_doc from Platform.new\_doc(“Batch”).
- Set batch\_doc.batch\_id from batch\_no.
- Set batch\_doc.item from item\_code.
- Evaluate batch\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0813.json#L4463) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L899) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L545)

<a id="op-7f0101b185e067"></a>
### Is duplicate serial no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_is_duplicate_serial_number`

**Inputs** bundle\_id, serial\_no.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Serial and Batch Entry” via exists.

**Explicit results** Platform.db.exists(“Serial and Batch Entry”, mapping(“parent” → bundle\_id, “serial\_no” → serial\_no)).

**Local steps**

- Return Platform.db.exists(“Serial and Batch Entry”, mapping(“parent” → bundle\_id, “serial\_no” → serial\_no)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L896) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L542)

<a id="op-be873877e44534"></a>
### Parse serial nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_parse_serial_numbers`

**Inputs** serial\_no.

**Explicit results** serial\_no · list of s.strip() for s drawn from nested operand in the contract.strip().replace(“,”, whitespace '\\n').split(whitespace '\\n') where s.strip().

**Local steps**

- If isinstance(serial\_no, list).
  - Return serial\_no.
- Return list of s.strip() for s drawn from nested operand in the contract.strip().replace(“,”, whitespace '\\n').split(whitespace '\\n') where s.strip().
  - Draw s from nested operand in the contract(nested operand in the contract).strip().replace(“,”, whitespace '\\n').split(whitespace '\\n'), keep a combination only if (s.strip()).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0813.json#L4730) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L905) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L551)

<a id="op-bfcde44d5e0438"></a>
### Get stock reco details

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_stock_reco_details`

**Inputs** voucher\_detail\_no.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “Stock Reconciliation Item” via get\_value.

**Explicit results** Platform.db.get\_value(“Stock Reconciliation Item”, voucher\_detail\_no, list(“current\_serial\_no”, “serial\_no”, “serial\_and\_batch\_bundle”, “current\_serial\_and\_batch\_bundle”, …), as\_dict = true).

**Local steps**

- Return Platform.db.get\_value(“Stock Reconciliation Item”, voucher\_detail\_no, list(“current\_serial\_no”, “serial\_no”, “serial\_and\_batch\_bundle”, “current\_serial\_and\_batch\_bundle”, …), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0813.json#L4907) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L893) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L539)

<a id="op-7125d43e6629fa"></a>
### On doctype update

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Serial and Batch Bundle”.

**Local steps**

- Evaluate Platform.db.add\_index(“Serial and Batch Bundle”, list(“voucher\_no”, “voucher\_type”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L903) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L549)
