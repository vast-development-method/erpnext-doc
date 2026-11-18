# Inventory and warehouses · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Deprecated serial batch

<a id="op-8e11aa51f3e710"></a>
### Deprecated Serial No Valuation.get last inward sle for serial no

`operation_enterprise_binding_enterprise_stock_deprecated_serial_batch_deprecatedserialnovaluation_get_last_inward_sle_for_serial_no`

**Inputs** self, serial\_no, posting\_datetime.

**Explicit results** query.run(as\_dict = 1).

**Local steps**

- Set table from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).orderby(table.posting\_datetime, order = Order.desc).orderby(table.creation, order = Order.desc).limit(1).
- If Platform.db.db\_type equals “mariadb”.
  - Set query from query.force\_index(“item\_code\_warehouse\_posting\_datetime\_creation\_index”).
- Return query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L698) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L195)

<a id="op-d3acde64f3f3a7"></a>
### Deprecated Batch No Valuation.get non batchwise avg rate

`operation_enterprise_binding_enterprise_stock_deprecated_serial_batch_deprecatedbatchnovaluation_get_non_batchwise_avg_rate`

**Inputs** self, batch\_no, fallback\_rate.

**Explicit results** (balance\_value ÷ balance\_qty) · fallback\_rate.

**Local steps**

- Set balance\_qty from flt(self.non\_batchwise\_balance\_qty.get(batch\_no)).
- Set balance\_value from flt(self.non\_batchwise\_balance\_value.get(batch\_no)).
- If (balance\_qty &gt; 0 and balance\_value &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in balance\_qty &gt; 0 → balance\_value &gt; 0.
  - Return (balance\_value ÷ balance\_qty).
- Return fallback\_rate.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L695) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L192)

<a id="op-9e13da32638210"></a>
### Deprecated Batch No Valuation.get pooled fallback rate

`operation_enterprise_binding_enterprise_stock_deprecated_serial_batch_deprecatedbatchnovaluation_get_pooled_fallback_rate`

**Inputs** self.

**Explicit results** (value ÷ qty) · (total\_value ÷ total\_qty) · 0.0.

**Local steps**

- Set last\_sle from (self.last\_sle or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.last\_sle → Platform.\_dict().
- Set total\_qty from flt(last\_sle.qty\_after\_transaction).
- Set total\_value from flt(last\_sle.stock\_value).
- Set tuple(qty, value) from tuple(total\_qty, total\_value).
- For each batch\_no in self.batchwise\_valuation\_batches.
  - Update qty using − flt(self.available\_qty.get(batch\_no)).
  - Update value using − flt(self.stock\_value\_differece.get(batch\_no)).
- If (qty &gt; 0 and value &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty &gt; 0 → value &gt; 0.
  - Return (value ÷ qty).
- If (total\_qty &gt; 0 and total\_value &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in total\_qty &gt; 0 → total\_value &gt; 0.
  - Return (total\_value ÷ total\_qty).
- Return 0.0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L696) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L193)

<a id="op-11a2fd2bde3a28"></a>
### Deprecated Batch No Valuation.use batch pool for moving average

`operation_enterprise_binding_enterprise_stock_deprecated_serial_batch_deprecatedbatchnovaluation_use_batch_pool_for_moving_average`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** self.\_use\_batch\_pool\_for\_moving\_average.

**Local steps**

- If not hasattr(self, “\_use\_batch\_pool\_for\_moving\_average”).
  - Set self.\_use\_batch\_pool\_for\_moving\_average from (self.get\_valuation\_method(self.sle.item\_code) equals “Moving Average” and not Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get\_valuation\_method(self.sle.item\_code) equals “Moving Average” → not Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”).
- Return self.\_use\_batch\_pool\_for\_moving\_average.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L697) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L194)

## Service · Expected valuation

<a id="op-ec16cf9d213977"></a>
### Moving Average Pool.initialize

`operation_enterprise_binding_enterprise_stock_expected_valuation_movingaveragepool_init`

**Inputs** self.

**Local steps**

- Set self.qty from 0.0.
- Set self.rate from 0.0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1391) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L888)

<a id="op-75a3d9470acf36"></a>
### Moving Average Pool.value

`operation_enterprise_binding_enterprise_stock_expected_valuation_movingaveragepool_value`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** float.

**Explicit results** (self.qty × self.rate).

**Local steps**

- Return (self.qty × self.rate).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L893)

<a id="op-0ff5e0c1980919"></a>
### Moving Average Pool.receive

`operation_enterprise_binding_enterprise_stock_expected_valuation_movingaveragepool_receive`

**Inputs** self, qty, rate.

**Declared result** no value.

**Local steps**

- Set new\_qty from (self.qty + qty).
- If (self.qty ≤ 0 and new\_qty ≥ 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.qty ≤ 0 → new\_qty ≥ 0.
  - Set self.rate from rate.
- Otherwise.
  - If new\_qty &gt; 0.
    - Set self.rate from ((self.value + (qty × rate)) ÷ new\_qty).
  - Otherwise.
    - If not self.rate.
      - Set self.rate from rate.
- Set self.qty from new\_qty.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1394) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L891)

<a id="op-793906a9e426dc"></a>
### Moving Average Pool.issue

`operation_enterprise_binding_enterprise_stock_expected_valuation_movingaveragepool_issue`

**Inputs** self, qty, preferred\_rate = no value.

**Declared result** float.

**Explicit results** (qty × self.rate).

**Local steps**

- Update self.qty using − qty.
- Return (qty × self.rate).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1392) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L889)

<a id="op-1744b6e1857507"></a>
### Moving Average Pool.set balance

`operation_enterprise_binding_enterprise_stock_expected_valuation_movingaveragepool_set_balance`

**Inputs** self, qty, rate.

**Declared result** no value.

**Local steps**

- Set self.qty from qty.
- Set self.rate from rate.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L892)

<a id="op-4b3528773d5182"></a>
### Moving Average Pool.clear

`operation_enterprise_binding_enterprise_stock_expected_valuation_movingaveragepool_clear`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.qty from 0.0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1390) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L887)

<a id="op-b73244f25b60b7"></a>
### Moving Average Pool.last rate

`operation_enterprise_binding_enterprise_stock_expected_valuation_movingaveragepool_last_rate`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** float.

**Explicit results** self.rate.

**Local steps**

- Return self.rate.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L890)

<a id="op-384722a93443be"></a>
### Queue Pool.initialize

`operation_enterprise_binding_enterprise_stock_expected_valuation_queuepool_init`

**Inputs** self, last\_in\_first\_out = false.

**Local steps**

- Set self.last\_in\_first\_out from last\_in\_first\_out.
- Set self.layers from list().
- Set self.last\_rate from 0.0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L896)

<a id="op-71b9dbd2effc13"></a>
### Queue Pool.qty

`operation_enterprise_binding_enterprise_stock_expected_valuation_queuepool_qty`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** float.

**Explicit results** sum(generator of qty for tuple(qty, \_rate) drawn from self.layers).

**Local steps**

- Return sum(generator of qty for tuple(qty, \_rate) drawn from self.layers).
  - Draw tuple(qty, \_rate) from self.layers.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L898)

<a id="op-b6c629c1240977"></a>
### Queue Pool.value

`operation_enterprise_binding_enterprise_stock_expected_valuation_queuepool_value`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** float.

**Explicit results** sum(generator of (qty × rate) for tuple(qty, rate) drawn from self.layers).

**Local steps**

- Return sum(generator of (qty × rate) for tuple(qty, rate) drawn from self.layers).
  - Draw tuple(qty, rate) from self.layers.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L901)

<a id="op-81e910fd5c84d8"></a>
### Queue Pool.receive

`operation_enterprise_binding_enterprise_stock_expected_valuation_queuepool_receive`

**Inputs** self, qty, rate.

**Declared result** no value.

**Local steps**

- Set self.last\_rate from (rate or self.last\_rate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rate → self.last\_rate.
- If (self.layers and self.layers at negative 1 at 0 ≤ 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.layers → self.layers at negative 1 at 0 ≤ 0.
  - Set balance from (self.layers at negative 1 at 0 + qty).
  - Set self.layers at negative 1 from list(balance, rate) when balance &gt; 0, otherwise list(balance, self.layers at negative 1 at 1).
    - Value choice on balance &gt; 0 — true gives list(balance, rate), false gives list(balance, self.layers at negative 1 at 1).
- Otherwise.
  - If (self.layers and self.layers at negative 1 at 1 equals rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.layers → self.layers at negative 1 at 1 equals rate.
    - Update self.layers at negative 1 at 0 using + qty.
  - Otherwise.
    - Evaluate self.layers.append(list(qty, rate)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L899)

<a id="op-0c0604b9fd8403"></a>
### Queue Pool.issue

`operation_enterprise_binding_enterprise_stock_expected_valuation_queuepool_issue`

**Inputs** self, qty, preferred\_rate = no value.

**Declared result** float.

**Explicit results** (value\_before − self.value).

**Local steps**

- Set value\_before from self.value.
- While qty &gt; 0.
  - If not self.layers.
    - Evaluate self.layers.append(list(0.0, preferred\_rate when preferred\_rate is distinct from no value, otherwise self.last\_rate)).
      - Value choice on preferred\_rate is distinct from no value — true gives preferred\_rate, false gives self.last\_rate.
  - Set index from self.get\_layer\_to\_consume(preferred\_rate).
  - Set tuple(layer\_qty, layer\_rate) from self.layers at index.
  - Set self.last\_rate from (layer\_rate or self.last\_rate).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in layer\_rate → self.last\_rate.
  - If layer\_qty &gt; qty.
    - Set self.layers at index at 0 from (layer\_qty − qty).
    - Set qty from 0.
    - Continue with the next iteration or loop test.
  - Evaluate self.layers.pop(index).
  - Set qty from (qty − layer\_qty).
  - If (not self.layers and qty &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.layers → qty &gt; 0.
    - Evaluate self.layers.append(list(negative qty, (preferred\_rate or layer\_rate))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in preferred\_rate → layer\_rate.
    - Set qty from 0.
- Return (value\_before − self.value).

**Methods declared on this owner** [get layer to consume](operations-011.md#op-8665f67f5be667).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1400) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L897)

<a id="op-8665f67f5be667"></a>
### Queue Pool.get layer to consume

`operation_enterprise_binding_enterprise_stock_expected_valuation_queuepool_get_layer_to_consume`

**Inputs** self, preferred\_rate.

**Declared result** int.

**Explicit results** negative 1 · index · 0.

**Local steps**

- If self.last\_in\_first\_out.
  - Return negative 1.
- If preferred\_rate is distinct from no value.
  - For each tuple(index, tuple(\_qty, rate)) in enumerate(self.layers).
    - If rate equals preferred\_rate.
      - Return index.
- Return 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L895)

<a id="op-d4ab9967dc5ea9"></a>
### Queue Pool.set balance

`operation_enterprise_binding_enterprise_stock_expected_valuation_queuepool_set_balance`

**Inputs** self, qty, rate.

**Declared result** no value.

**Local steps**

- Set self.layers from list(list(qty, rate)).
- Set self.last\_rate from (rate or self.last\_rate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rate → self.last\_rate.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1403) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L900)

<a id="op-afe563dc166116"></a>
### Queue Pool.clear

`operation_enterprise_binding_enterprise_stock_expected_valuation_queuepool_clear`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.layers from list().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L894)

<a id="op-cd1e6ca3131a5f"></a>
### Batch Lot.average rate

`operation_enterprise_binding_enterprise_stock_expected_valuation_batchlot_average_rate`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** float.

**Explicit results** (self.value ÷ self.qty) when self.qty, otherwise 0.0.

**Local steps**

- Return (self.value ÷ self.qty) when self.qty, otherwise 0.0.
  - Value choice on self.qty — true gives (self.value ÷ self.qty), false gives 0.0.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L851)

<a id="op-8176847d07976f"></a>
### Item Warehouse Stock.post init

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_post_init`

**Inputs** self.

**Local steps**

- If self.pool is identical to no value.
  - If self.valuation\_method belongs to tuple(“FIFO”, “LIFO”).
    - Set self.pool from QueuePool(last\_in\_first\_out = self.valuation\_method equals “LIFO”).
  - Otherwise.
    - Set self.pool from MovingAveragePool().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L873)

<a id="op-b8629634abc7d0"></a>
### Item Warehouse Stock.qty

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_qty`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** float.

**Explicit results** (((self.pool.qty + sum(generator of lot.qty for lot drawn from nested operand in the contract.values())) + len(self.serial\_rates)) − len(self.serials\_issued\_before\_receipt)).

**Local steps**

- Return (((self.pool.qty + sum(generator of lot.qty for lot drawn from nested operand in the contract.values())) + len(self.serial\_rates)) − len(self.serials\_issued\_before\_receipt)).
  - Draw lot from self.batch\_lots.values().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L874)

<a id="op-1b2dd2bd25965d"></a>
### Item Warehouse Stock.value

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_value`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** float.

**Explicit results** (((self.pool.value + sum(generator of lot.value for lot drawn from nested operand in the contract.values())) + sum(self.serial\_rates.values())) − sum(self.serials\_issued\_before\_receipt.values())).

**Local steps**

- Return (((self.pool.value + sum(generator of lot.value for lot drawn from nested operand in the contract.values())) + sum(self.serial\_rates.values())) − sum(self.serials\_issued\_before\_receipt.values())).
  - Draw lot from self.batch\_lots.values().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L879)

<a id="op-f38ed9116a9394"></a>
### Item Warehouse Stock.pool basis

`operation_enterprise_binding_enterprise_stock_expected_valuation_itemwarehousestock_pool_basis`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** mapping(“FIFO” → BASIS\_FIFO, “LIFO” → BASIS\_LIFO).get(self.valuation\_method, BASIS\_MOVING\_AVERAGE).

**Local steps**

- Return mapping(“FIFO” → BASIS\_FIFO, “LIFO” → BASIS\_LIFO).get(self.valuation\_method, BASIS\_MOVING\_AVERAGE).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L872)
