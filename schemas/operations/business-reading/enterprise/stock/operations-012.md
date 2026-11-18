# Inventory and warehouses · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Expected valuation

<a id="op-4448d054f4fb39"></a>
### Item Warehouse Stock.get rate to fall back on

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_get_rate_to_fall_back_on`

**Inputs** self.

**Declared result** float.

**Explicit results** (self.value ÷ self.qty) · (self.last\_valuation\_rate or self.pool.last\_rate or self.ledger\_rate\_of\_entry).

**Local steps**

- If (self.qty &gt; 0 and self.value &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.qty &gt; 0 → self.value &gt; 0.
  - Return (self.value ÷ self.qty).
- Return (self.last\_valuation\_rate or self.pool.last\_rate or self.ledger\_rate\_of\_entry).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.last\_valuation\_rate → self.pool.last\_rate → self.ledger\_rate\_of\_entry.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L868)

<a id="op-89a01f3133fcfb"></a>
### Item Warehouse Stock.receive into pool

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_receive_into_pool`

**Inputs** self, qty, rate.

**Declared result** no value.

**Local steps**

- Evaluate self.pool.receive(qty, rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1379) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L876)

<a id="op-bb8695a4edc079"></a>
### Item Warehouse Stock.issue from pool

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_issue_from_pool`

**Inputs** self, qty, preferred\_rate = no value.

**Declared result** no value.

**Local steps**

- If (not self.pool.qty &gt; 0 and not self.pool.last\_rate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.pool.qty &gt; 0 → not self.pool.last\_rate.
  - Evaluate self.pool.receive(0.0, (preferred\_rate or self.get\_rate\_to\_fall\_back\_on())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in preferred\_rate → self.get\_rate\_to\_fall\_back\_on().
- Evaluate self.pool.issue(qty, preferred\_rate).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get rate to fall back on](operations-012.md#op-4448d054f4fb39).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L870)

<a id="op-7d20c166cb0f39"></a>
### Item Warehouse Stock.receive into batch

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_receive_into_batch`

**Inputs** self, batch\_no, qty, rate.

**Declared result** no value.

**Local steps**

- Set lot from self.batch\_lots.setdefault(batch\_no, BatchLot()).
- Update lot.qty using + qty.
- Update lot.value using + (qty × rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1378) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L875)

<a id="op-c07ed120fe8d1b"></a>
### Item Warehouse Stock.issue from batch

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_issue_from_batch`

**Inputs** self, batch\_no, qty.

**Declared result** bool.

**Explicit results** has\_stock.

**Local steps**

- Set lot from self.batch\_lots.setdefault(batch\_no, BatchLot()).
- Set has\_stock from lot.qty &gt; 0.
- Set rate from lot.average\_rate when has\_stock, otherwise self.get\_rate\_to\_fall\_back\_on().
  - Value choice on has\_stock — true gives lot.average\_rate, false gives self.get\_rate\_to\_fall\_back\_on().
- Update lot.qty using − qty.
- Update lot.value using − (qty × rate).
- If abs(lot.qty) &lt; 1e-09.
  - Remove self.batch\_lots at batch\_no.
- Return has\_stock.

**Methods declared on this owner** [get rate to fall back on](operations-012.md#op-4448d054f4fb39).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L869)

<a id="op-d7c98671d2d6bc"></a>
### Item Warehouse Stock.receive serial

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_receive_serial`

**Inputs** self, serial\_no, rate.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If serial\_no belongs to self.serials\_issued\_before\_receipt.
  - Evaluate self.serials\_issued\_before\_receipt.pop(serial\_no).
  - Return no value.
- Set self.serial\_rates at serial\_no from rate.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L877)

<a id="op-bbf84eab581526"></a>
### Item Warehouse Stock.issue serial

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_issue_serial`

**Inputs** self, serial\_no.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If serial\_no belongs to self.serial\_rates.
  - Evaluate self.serial\_rates.pop(serial\_no).
  - Return true.
- Set self.serials\_issued\_before\_receipt at serial\_no from self.get\_rate\_to\_fall\_back\_on().
- Return false.

**Methods declared on this owner** [get rate to fall back on](operations-012.md#op-4448d054f4fb39).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L871)

<a id="op-1de6c047147efd"></a>
### Item Warehouse Stock.set reconciled balance

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_set_reconciled_balance`

**Inputs** self, qty, rate.

**Declared result** no value.

**Local steps**

- Evaluate self.pool.set\_balance(qty, rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1381) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L878)

<a id="op-3aa639f10e9b8a"></a>
### Item Warehouse Stock.clear

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_clear`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.pool from no value.
- Evaluate self.\_\_post\_init\_\_().
- Set self.batch\_lots from mapping().
- Set self.serial\_rates from mapping().
- Set self.serials\_issued\_before\_receipt from mapping().

If control reaches the end, it returns no value.

**Methods declared on this owner** [post init](operations-011.md#op-8176847d07976f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L867)

<a id="op-3b3c49495552a5"></a>
### Item Warehouse Stock.write off leftover value

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_write_off_leftover_value`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.pool.clear().
- Set self.batch\_lots from mapping of batch\_no → lot for tuple(batch\_no, lot) drawn from self.batch\_lots.items() where abs(lot.qty) ≥ 1e-09.
  - Draw tuple(batch\_no, lot) from self.batch\_lots.items(), keep a combination only if (abs(lot.qty) ≥ 1e-09).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L880)

<a id="op-937ad185d5c8be"></a>
### Get expected valuation

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_expected_valuation`

**Inputs** item\_code, warehouse, to\_date = no value.

**Declared result** list at tuple at tuple(Platform.\_dict, ExpectedValues).

**Explicit results** list(expected\_valuation) · list().

**Local steps**

- For each tuple(\_item\_code, \_warehouse, expected\_valuation) in iterate\_expected\_valuations(list(tuple(item\_code, warehouse)), to\_date).
  - Return list(expected\_valuation).
- Return list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L859)

<a id="op-61f696b17660cb"></a>
### Iterate expected valuations

`operation_enterprise_binding_enterprise_stock_expected_valuation_iterate_expected_valuations`

**Inputs** item\_warehouses, to\_date = no value.

**Declared result** Iterator at tuple at tuple(str, str, Iterator at tuple at tuple(nested operand in the contract.\_dict, ExpectedValues)).

**Local steps**

- Set settings from ValuationSettings().
- For each item\_warehouses\_to\_read in create\_batch(list(item\_warehouses), ITEM\_WAREHOUSES\_PER\_READ).
  - Set entries\_by\_item\_warehouse from get\_ledger\_entries(item\_warehouses\_to\_read, to\_date, settings).
  - Set data from LedgerData(entries\_by\_item\_warehouse, settings).
  - For each tuple(item\_code, warehouse) in item\_warehouses\_to\_read.
    - Set ledger\_entries from entries\_by\_item\_warehouse.get(tuple(item\_code, warehouse)).
    - If ledger\_entries.
      - Set details from ValuationDetails(item\_code, ledger\_entries at 0.company, data).
      - yield tuple(item\_code, warehouse, replay\_ledger(ledger\_entries, details)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L882)

<a id="op-73b4db60e4747d"></a>
### Iterate expected stock at

`operation_enterprise_binding_enterprise_stock_expected_valuation_iterate_expected_stock_at`

**Inputs** item\_warehouses, posting\_datetime, exclude\_voucher\_no = no value.

**Declared result** Iterator at tuple at tuple(str, str, ItemWarehouseStock, Platform.\_dict, …).

**Local steps**

- Set settings from ValuationSettings().
- Set cutoff from get\_datetime(posting\_datetime).
- For each item\_warehouses\_to\_read in create\_batch(list(item\_warehouses), ITEM\_WAREHOUSES\_PER\_READ).
  - Set entries\_by\_item\_warehouse from get\_ledger\_entries(item\_warehouses\_to\_read, getdate(cutoff), settings).
  - Set data from LedgerData(entries\_by\_item\_warehouse, settings).
  - For each tuple(item\_code, warehouse) in item\_warehouses\_to\_read.
    - Set ledger\_entries from list of entry for entry drawn from entries\_by\_item\_warehouse.get(tuple(item\_code, warehouse), list()) where (get\_datetime(entry.posting\_datetime) ≤ cutoff and entry.voucher\_no differs from exclude\_voucher\_no).
      - Draw entry from entries\_by\_item\_warehouse.get(tuple(item\_code, warehouse), list()), keep a combination only if ((get\_datetime(entry.posting\_datetime) ≤ cutoff and entry.voucher\_no differs from exclude\_voucher\_no)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in get\_datetime(entry.posting\_datetime) ≤ cutoff → entry.voucher\_no differs from exclude\_voucher\_no.
    - If not ledger\_entries.
      - Continue with the next iteration or loop test.
    - Set details from ValuationDetails(item\_code, ledger\_entries at 0.company, data).
    - Set stock from ItemWarehouseStock(details.valuation\_method).
    - For each \_entry\_and\_values in replay\_ledger(ledger\_entries, details, stock).
      - Take no action here.
    - yield tuple(item\_code, warehouse, stock, ledger\_entries at negative 1, …).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L881)

<a id="op-b7d747b2699308"></a>
### Replay ledger

`operation_enterprise_binding_enterprise_stock_expected_valuation_replay_ledger`

**Inputs** ledger\_entries, details, stock = no value.

**Declared result** Iterator at tuple at tuple(Platform.\_dict, ExpectedValues).

**Local steps**

- If stock is identical to no value.
  - Set stock from ItemWarehouseStock(details.valuation\_method).
- For each entry in ledger\_entries.
  - yield tuple(entry, value\_ledger\_entry(stock, entry, details)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L903)

<a id="op-78386afd1302cd"></a>
### Value ledger entry

`operation_enterprise_binding_enterprise_stock_expected_valuation_value_ledger_entry`

**Inputs** stock, entry, details.

**Declared result** ExpectedValues.

**Explicit results** value\_adjustment\_entry(stock, entry, details) · make\_expected\_values(stock, carried\_value\_before, basis).

**Local steps**

- If details.is\_adjustment\_voucher(entry).
  - Return value\_adjustment\_entry(stock, entry, details).
- Set carried\_value\_before from stock.carried\_value.
- Set value\_before from stock.value.
- Set stock.ledger\_rate\_of\_entry from get\_ledger\_rate(entry).
- If details.is\_reconciled\_balance(entry).
  - Set tuple(reconciled\_qty, reconciled\_rate) from details.get\_reconciled\_balance(entry).
  - Evaluate stock.set\_reconciled\_balance(reconciled\_qty, reconciled\_rate).
  - Set basis from BASIS\_RECONCILED.
- Otherwise.
  - If (entry.is\_adjustment\_entry and not flt(entry.actual\_qty)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.is\_adjustment\_entry → not flt(entry.actual\_qty).
    - Set basis from BASIS\_WRITE\_OFF.
  - Otherwise.
    - If flt(entry.actual\_qty) &gt; 0.
      - Set basis from receive\_stock(stock, entry, details).
    - Otherwise.
      - If flt(entry.actual\_qty) &lt; 0.
        - Set basis from issue\_stock(stock, entry, details).
      - Otherwise.
        - Set basis from BASIS\_INCOMING\_RATE.
- If abs(stock.qty) &lt; details.qty\_tolerance.
  - If abs(((stock.carried\_value + stock.value) − value\_before)) ≥ details.value\_tolerance.
    - Set basis from formatted text {basis}, {BASIS\_WRITE\_OFF} when basis differs from BASIS\_WRITE\_OFF, otherwise basis.
      - Value choice on basis differs from BASIS\_WRITE\_OFF — true gives formatted text {basis}, {BASIS\_WRITE\_OFF}, false gives basis.
  - Evaluate stock.write\_off\_leftover\_value().
  - Set stock.carried\_value from 0.0.
- Otherwise.
  - If (basis equals BASIS\_RECONCILED or details.is\_valued\_as\_a\_whole(entry)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in basis equals BASIS\_RECONCILED → details.is\_valued\_as\_a\_whole(entry).
    - Set stock.carried\_value from flt(stock.value, details.currency\_precision).
    - Evaluate carry\_moving\_average\_rate\_from\_rounded\_value(stock).
  - Otherwise.
    - Set stock.carried\_value from flt(((stock.carried\_value + stock.value) − value\_before), details.currency\_precision).
- Return make\_expected\_values(stock, carried\_value\_before, basis).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1417) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L914)

<a id="op-be679ace7513e2"></a>
### Value adjustment entry

`operation_enterprise_binding_enterprise_stock_expected_valuation_value_adjustment_entry`

**Inputs** stock, entry, details.

**Declared result** ExpectedValues.

**Explicit results** ExpectedValues(qty\_after\_transaction = flt(entry.qty\_after\_transaction), stock\_value\_difference = flt(entry.stock\_value\_difference), stock\_value = flt(entry.stock\_value), valuation\_rate = flt(entry.valuati … · make\_expected\_values(stock, carried\_value\_before, BASIS\_ADJUSTED).

**Local steps**

- If entry.name does not belong to details.data.adjustment\_last\_entries.
  - Set stock.carried\_value from flt(entry.stock\_value).
  - Return ExpectedValues(qty\_after\_transaction = flt(entry.qty\_after\_transaction), stock\_value\_difference = flt(entry.stock\_value\_difference), stock\_value = flt(entry.stock\_value), valuation\_rate = flt(entry.valuati ….
- Set carried\_value\_before from (flt(entry.stock\_value) − flt(entry.stock\_value\_difference)).
- Evaluate stock.clear().
- For each row in details.data.adjustment\_rows.get(tuple(entry.voucher\_no, entry.item\_code, entry.warehouse), list()).
  - Set rate from flt(row.valuation\_rate).
  - If row.serial\_no.
    - For each serial\_no in get\_serial\_nos(row.serial\_no).
      - If details.values\_everything\_in\_pool.
        - Evaluate stock.receive\_into\_pool(1, rate).
      - Otherwise.
        - Evaluate stock.receive\_serial(serial\_no, rate).
  - Otherwise.
    - If (row.batch\_no and details.is\_valued\_batch\_wise(row.batch\_no)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.batch\_no → details.is\_valued\_batch\_wise(row.batch\_no).
      - Evaluate stock.receive\_into\_batch(row.batch\_no, flt(row.qty), rate).
    - Otherwise.
      - If flt(row.qty).
        - Evaluate stock.receive\_into\_pool(flt(row.qty), rate).
- Set stock.carried\_value from flt(stock.value, details.currency\_precision).
- Evaluate carry\_moving\_average\_rate\_from\_rounded\_value(stock).
- Return make\_expected\_values(stock, carried\_value\_before, BASIS\_ADJUSTED).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1416) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L913)

<a id="op-ac208a659ed3a1"></a>
### Carry moving average rate from rounded value

`operation_enterprise_binding_enterprise_stock_expected_valuation_carry_moving_average_rate_from_rounded_value`

**Inputs** stock.

**Declared result** no value.

**Local steps**

- If (isinstance(stock.pool, MovingAveragePool) and stock.pool.qty and stock.qty equals stock.pool.qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(stock.pool, MovingAveragePool) → stock.pool.qty → stock.qty equals stock.pool.qty.
  - Set stock.pool.rate from (stock.carried\_value ÷ stock.pool.qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L852)

<a id="op-06a9de34486542"></a>
### Get ledger rate

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_ledger_rate`

**Inputs** entry.

**Declared result** float.

**Explicit results** 0.0 · abs((flt(entry.stock\_value\_difference) ÷ flt(entry.actual\_qty))).

**Local steps**

- If not flt(entry.actual\_qty).
  - Return 0.0.
- Return abs((flt(entry.stock\_value\_difference) ÷ flt(entry.actual\_qty))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L863)

<a id="op-82b06466fbe78d"></a>
### Receive stock

`operation_enterprise_binding_enterprise_stock_expected_valuation_receive_stock`

**Inputs** stock, entry, details.

**Declared result** str.

**Explicit results** BASIS\_INCOMING\_RATE.

**Local steps**

- For each movement in details.get\_lot\_movements(entry).
  - If movement.serial\_no.
    - Evaluate stock.receive\_serial(movement.serial\_no, movement.rate).
  - Otherwise.
    - If (movement.batch\_no and details.is\_valued\_batch\_wise(movement.batch\_no)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in movement.batch\_no → details.is\_valued\_batch\_wise(movement.batch\_no).
      - Evaluate stock.receive\_into\_batch(movement.batch\_no, movement.qty, movement.rate).
    - Otherwise.
      - Evaluate stock.receive\_into\_pool(movement.qty, movement.rate).
- Return BASIS\_INCOMING\_RATE.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L902)

<a id="op-1bf27f2a24f398"></a>
### Issue stock

`operation_enterprise_binding_enterprise_stock_expected_valuation_issue_stock`

**Inputs** stock, entry, details.

**Declared result** str.

**Explicit results** “, ”.join(dict.fromkeys(bases)).

**Local steps**

- Set bases from list().
- For each movement in details.get\_lot\_movements(entry).
  - If movement.serial\_no.
    - Set was\_on\_hand from stock.issue\_serial(movement.serial\_no).
    - Evaluate bases.append(BASIS\_SERIAL\_RATE when was\_on\_hand, otherwise BASIS\_NO\_STOCK).
      - Value choice on was\_on\_hand — true gives BASIS\_SERIAL\_RATE, false gives BASIS\_NO\_STOCK.
  - Otherwise.
    - If (movement.batch\_no and details.is\_valued\_batch\_wise(movement.batch\_no)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in movement.batch\_no → details.is\_valued\_batch\_wise(movement.batch\_no).
      - Set had\_stock from stock.issue\_from\_batch(movement.batch\_no, movement.qty).
      - Evaluate bases.append(BASIS\_BATCH\_AVERAGE when had\_stock, otherwise BASIS\_NO\_STOCK).
        - Value choice on had\_stock — true gives BASIS\_BATCH\_AVERAGE, false gives BASIS\_NO\_STOCK.
    - Otherwise.
      - Set return\_rate from details.get\_purchase\_return\_rate(entry).
      - Set had\_stock from stock.pool.qty &gt; 0.
      - Evaluate stock.issue\_from\_pool(movement.qty, preferred\_rate = return\_rate).
      - If return\_rate is distinct from no value.
        - Evaluate bases.append(BASIS\_PURCHASE\_RETURN).
      - Otherwise.
        - Evaluate bases.append(stock.pool\_basis when had\_stock, otherwise BASIS\_NO\_STOCK).
          - Value choice on had\_stock — true gives stock.pool\_basis, false gives BASIS\_NO\_STOCK.
- Return “, ”.join(dict.fromkeys(bases)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L866)

<a id="op-6bc604deb70086"></a>
### Make expected values

`operation_enterprise_binding_enterprise_stock_expected_valuation_make_expected_values`

**Inputs** stock, carried\_value\_before, basis.

**Declared result** ExpectedValues.

**Explicit results** ExpectedValues(qty\_after\_transaction = qty, stock\_value\_difference = (stock.carried\_value − carried\_value\_before), stock\_value = stock.carried\_value, valuation\_rate = stock.last\_valuation\_rate, …).

**Local steps**

- Set qty from stock.qty.
- If qty.
  - Set stock.last\_valuation\_rate from (stock.carried\_value ÷ qty).
- Return ExpectedValues(qty\_after\_transaction = qty, stock\_value\_difference = (stock.carried\_value − carried\_value\_before), stock\_value = stock.carried\_value, valuation\_rate = stock.last\_valuation\_rate, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1389) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L886)

<a id="op-c17a48686813ed"></a>
### Valuation Settings.initialize

`operation_enterprise_binding_enterprise_stock_expected_valuation_valuationsettings_init`

**Inputs** self.

**Record and data access** read “System Settings” via get\_single\_value · read “Stock Settings” via get\_single\_value.

**Local steps**

- Set float\_precision from (cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)) or 3).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)) → 3.
- Set self.currency\_precision from (cint(Platform.db.get\_single\_value(“System Settings”, “currency\_precision”)) or float\_precision).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“System Settings”, “currency\_precision”)) → float\_precision.
- Set self.qty\_tolerance from (1.0 ÷ (10 to the power float\_precision)).
- Set self.value\_tolerance from (1.0 ÷ (10 to the power self.currency\_precision)).
- Set self.dimension\_fields from get\_inventory\_dimension\_fields().
- Set self.do\_not\_use\_batchwise\_valuation from cint(Platform.db.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”), Platform.db.get\_single\_value(“System Settings”, “currency\_precision”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1415) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L912)

<a id="op-a480dcab6882b8"></a>
### Ledger Data.initialize

`operation_enterprise_binding_enterprise_stock_expected_valuation_ledgerdata_init`

**Inputs** self, entries\_by\_item\_warehouse, settings.

**Local steps**

- Set ledger\_entries from list of entry for entries drawn from entries\_by\_item\_warehouse.values(), then entry drawn from entries.
  - Draw entries from entries\_by\_item\_warehouse.values().
  - Draw entry from entries.
- Set self.settings from settings.
- Set self.bundle\_rows from get\_bundle\_rows(set of entry.serial\_and\_batch\_bundle for entry drawn from ledger\_entries where entry.serial\_and\_batch\_bundle).
  - Draw entry from ledger\_entries, keep a combination only if (entry.serial\_and\_batch\_bundle).
- Set self.batch\_wise\_valued\_batches from get\_batch\_wise\_valued\_batches(self.get\_batches(ledger\_entries)).
- Set self.reconciled\_balances from get\_reconciled\_balances(ledger\_entries).
- Set self.adjustment\_vouchers from get\_adjustment\_vouchers(ledger\_entries).
- Set self.adjustment\_rows from get\_adjustment\_rows(self.adjustment\_vouchers).
- Set self.adjustment\_last\_entries from get\_adjustment\_last\_entries(entries\_by\_item\_warehouse, self.adjustment\_vouchers).
- Set self.items from get\_item\_settings(set of entry.item\_code for entry drawn from ledger\_entries).
  - Draw entry from ledger\_entries.
- Set self.company\_valuation\_methods from get\_company\_valuation\_methods().
- Set self.purchase\_return\_rates from get\_purchase\_return\_rates(ledger\_entries).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get batches](operations-012.md#op-1686d67a413926).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1388) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L885)

<a id="op-1686d67a413926"></a>
### Ledger Data.get batches

`operation_enterprise_binding_enterprise_stock_expected_valuation_ledgerdata_get_batches`

**Inputs** self, ledger\_entries.

**Declared result** set at str.

**Explicit results** batches.

**Local steps**

- Set batches from set of entry.batch\_no for entry drawn from ledger\_entries where entry.batch\_no.
  - Draw entry from ledger\_entries, keep a combination only if (entry.batch\_no).
- For each rows in self.bundle\_rows.values().
  - Evaluate batches.update(generator of row.batch\_no for row drawn from rows where row.batch\_no).
    - Draw row from rows, keep a combination only if (row.batch\_no).
- Return batches.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L883)
