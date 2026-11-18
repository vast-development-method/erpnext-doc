# Inventory and warehouses · operations 107

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-6f3abbb28f4040"></a>
### Scan barcode

`operation_enterprise_stock_utils_business_behavior_scan_barcode`

**Inputs** search\_value, ctx = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** BarcodeScanResult.

**Record and data access** read “Item Barcode” via get\_value · read “Serial No” via get\_value · read “Batch” via get\_value · read “Item” via get\_cached\_value · read “Warehouse” via get\_cached\_value.

**Explicit results** authorised(scan\_data) · authorised(barcode\_data) · authorised(serial\_no\_data) · authorised(batch\_no\_data) · warehouse\_data · 1 additional forms in the steps below.

**Explicit failure paths** validation helper — translated “Batch No {0} is linked with Item {1} which has serial no. Please scan serial no instead.”.format(search\_value, batch\_no\_data.item\_code).

**Local steps**

- Evaluate Platform.has\_permission(“Item”, ptype = “select”, throw = true).
- Bind local operation authorised for subsequent calls.
- Bind local operation set\_cache for subsequent calls.
- Bind local operation get\_cache for subsequent calls.
- If ctx is identical to no value.
  - Set ctx from Platform.\_dict().
- If scan\_data bound to get\_cache().
  - Return authorised(scan\_data).
- Set barcode\_data from Platform.db.get\_value(“Item Barcode”, mapping(“barcode” → search\_value), list(“barcode”, “parent as item\_code”, “uom”), as\_dict = true).
- If barcode\_data.
  - Evaluate set\_cache(barcode\_data).
  - Return authorised(barcode\_data).
- Set serial\_no\_data from Platform.db.get\_value(“Serial No”, search\_value, list(“name as serial\_no”, “item\_code”, “batch\_no”), as\_dict = true).
- If serial\_no\_data.
  - Evaluate set\_cache(serial\_no\_data).
  - Return authorised(serial\_no\_data).
- Set batch\_no\_data from Platform.db.get\_value(“Batch”, search\_value, list(“name as batch\_no”, “item as item\_code”), as\_dict = true).
- If batch\_no\_data.
  - If Platform.get\_cached\_value(“Item”, batch\_no\_data.item\_code, “has\_serial\_no”).
    - Call the validation error handler Platform.throw(translated “Batch No {0} is linked with Item {1} which has serial no. Please scan serial no instead.”.format(search\_value, batch\_no\_data.item\_code)).
  - Evaluate set\_cache(batch\_no\_data).
  - Return authorised(batch\_no\_data).
- Set warehouse from Platform.get\_cached\_value(“Warehouse”, search\_value, tuple(“name”, “disabled”), as\_dict = true).
- If (warehouse and not warehouse.disabled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in warehouse → not warehouse.disabled.
  - Set warehouse\_data from mapping(“warehouse” → warehouse.name).
  - Evaluate set\_cache(warehouse\_data).
  - Return warehouse\_data.
- Return mapping().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, ptype = “select”, throw = true) · configured or stored value from Platform.get\_cached\_value(“Item”, batch\_no\_data.item\_code, “has\_serial\_no”), Platform.get\_cached\_value(“Warehouse”, search\_value, tuple(“name”, “disabled”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1400) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L896)

<a id="op-fac08a85980296"></a>
### Scan barcode.authorised

`operation_enterprise_binding_enterprise_stock_utils_scan_barcode_authorised`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** data.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1641) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1138)

<a id="op-5e6a139e085027"></a>
### Scan barcode.set cache

`operation_enterprise_stock_utils_business_behavior_scan_barcode_set_cache`

**Inputs** data.

**Local steps**

- Evaluate Platform.cache().set\_value(formatted text Enterprise:barcode\_scan:{search\_value}, data, expires\_in\_sec = 120).
- Evaluate \_update\_item\_info(data, ctx).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L4080) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L898)

<a id="op-b0335e9b9cb630"></a>
### Scan barcode.get cache

`operation_enterprise_stock_utils_business_behavior_scan_barcode_get_cache`

**Inputs** no declared parameters.

**Declared result** (BarcodeScanResult bitwise or no value).

**Explicit results** no value · data.

**Local steps**

- Set data from Platform.cache().get\_value(formatted text Enterprise:barcode\_scan:{search\_value}).
- If not data.
  - Return no value.
- Evaluate \_update\_item\_info(data, ctx).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L4206) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L897)

<a id="op-99df8b94a34c08"></a>
### Update item info

`operation_enterprise_stock_utils_business_behavior_update_item_info`

**Inputs** scan\_result, ctx = no value.

**Declared result** dict at tuple(str, (str bitwise or no value)).

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** scan\_result.

**Local steps**

- Bind dependencies get\_item\_warehouse\_.
- Set item\_code from scan\_result.get(“item\_code”).
- If not item\_code.
  - Return scan\_result.
- If item\_info bound to Platform.get\_cached\_value(“Item”, item\_code, tuple(“has\_batch\_no”, “has\_serial\_no”), as\_dict = true).
  - Evaluate scan\_result.update(item\_info).
- If (ctx and warehouse bound to get\_item\_warehouse\_(ctx, Platform.\_dict(name = item\_code), overwrite\_warehouse = true)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx → warehouse bound to get\_item\_warehouse\_(ctx, Platform.\_dict(name = item\_code), overwrite\_warehouse = true).
  - Set scan\_result at “default\_warehouse” from warehouse.
- Return scan\_result.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, tuple(“has\_batch\_no”, “has\_serial\_no”), as\_dict = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L4348) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L900)

<a id="op-baaf88057630de"></a>
### Get combine datetime

`operation_enterprise_stock_utils_business_behavior_get_combine_datetime`

**Inputs** posting\_date, posting\_time.

**Explicit results** datetime.datetime.combine(posting\_date, posting\_time).

**Local steps**

- Bind dependencies datetime.
- If isinstance(posting\_date, str).
  - Set posting\_date from getdate(posting\_date).
- If isinstance(posting\_time, str).
  - Set posting\_time from get\_time(posting\_time).
- If isinstance(posting\_time, datetime.timedelta).
  - Set posting\_time from (datetime.datetime.min + posting\_time).time().
- Return datetime.datetime.combine(posting\_date, posting\_time).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L4724) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L878)

<a id="op-4c9d4012ef92b9"></a>
### Get default stock uom

`operation_enterprise_stock_utils_business_behavior_get_default_stock_unit_of_measure`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.request\_cache.

**Declared result** (str bitwise or no value).

**Record and data access** read “Stock Settings” via get\_cached\_value · read “UOM” via get\_values.

**Explicit results** default\_uom · next(generator of uom for uom drawn from acceptable\_default\_uoms where uom belongs to available\_default\_uoms, no value).

**Local steps**

- If default\_uom bound to Platform.get\_cached\_value(“Stock Settings”, no value, “stock\_uom”).
  - Return default\_uom.
- Set acceptable\_default\_uoms from dict.fromkeys(tuple(“Nos”, \_(“Nos”, Platform.get\_system\_settings(“language”)), translated “Nos”)).
- Set available\_default\_uoms from Platform.db.get\_values(“UOM”, mapping(“name” → tuple(“in”, tuple(acceptable\_default\_uoms))), pluck = “name”).
- Return next(generator of uom for uom drawn from acceptable\_default\_uoms where uom belongs to available\_default\_uoms, no value).
  - Draw uom from acceptable\_default\_uoms, keep a combination only if (uom belongs to available\_default\_uoms).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Settings”, no value, “stock\_uom”), Platform.get\_system\_settings(“language”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L4978) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L879)

## Service · Valuation

<a id="op-79b51b156b0e1e"></a>
### Bin Wise Valuation.add stock

`operation_enterprise_stock_valuation_business_behavior_bin_wise_valuation_add_stock`

**Inputs** self, qty, rate.

**Wrappers, in declaration order** abstractmethod.

**Declared result** no value.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L5324) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L903)

<a id="op-996e5033d0712d"></a>
### Bin Wise Valuation.remove stock

`operation_enterprise_stock_valuation_business_behavior_bin_wise_valuation_remove_stock`

**Inputs** self, qty, outgoing\_rate = 0.0, rate\_generator = no value, is\_return\_purchase\_entry = false.

**Wrappers, in declaration order** abstractmethod.

**Declared result** list at StockBin.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L5386) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1411) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L907)

<a id="op-5ba8db14cd47a0"></a>
### Bin Wise Valuation.state

`operation_enterprise_stock_valuation_business_behavior_bin_wise_valuation_state`

**Inputs** self.

**Wrappers, in declaration order** abstractproperty.

**Declared result** list at StockBin.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L5521) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1413) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L909)

<a id="op-7d2480ff8ec62a"></a>
### Bin Wise Valuation.get total stock and value

`operation_enterprise_stock_valuation_business_behavior_bin_wise_valuation_get_total_stock_and_value`

**Inputs** self.

**Declared result** tuple at tuple(float, float).

**Explicit results** tuple(round\_off\_if\_near\_zero(total\_qty), round\_off\_if\_near\_zero(total\_value)).

**Local steps**

- Set total\_qty from 0.0.
- Set total\_value from 0.0.
- For each tuple(qty, rate) in self.state.
  - Update total\_qty using + flt(qty).
  - Update total\_value using + (flt(qty) × flt(rate)).
- Return tuple(round\_off\_if\_near\_zero(total\_qty), round\_off\_if\_near\_zero(total\_value)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L5571) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1409) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L905)

<a id="op-9aaabede7026fc"></a>
### Bin Wise Valuation.repr

`operation_enterprise_stock_valuation_business_behavior_bin_wise_valuation_representation`

**Inputs** self.

**Explicit results** str(self.state).

**Local steps**

- Return str(self.state).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L5783) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1412) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L908)

<a id="op-87a1bcf5d3df82"></a>
### Bin Wise Valuation.iterate

`operation_enterprise_stock_valuation_business_behavior_bin_wise_valuation_iter`

**Inputs** self.

**Explicit results** iter(self.state).

**Local steps**

- Return iter(self.state).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L5837) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1410) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L906)

<a id="op-ad8ae157cd9363"></a>
### Bin Wise Valuation.eq

`operation_enterprise_stock_valuation_business_behavior_bin_wise_valuation_eq`

**Inputs** self, other.

**Explicit results** self.state equals other · (type(self) equals type(other) and self.state equals other.state).

**Local steps**

- If isinstance(other, list).
  - Return self.state equals other.
- Return (type(self) equals type(other) and self.state equals other.state).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in type(self) equals type(other) → self.state equals other.state.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L5891) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1408) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L904)

<a id="op-6e0714626fce3a"></a>
### FIFOValuation.initialize

`operation_enterprise_stock_valuation_business_behavior_first_in_first_out_valuation_initialize`

**Inputs** self, state.

**Local steps**

- Set self.queue from state when state is distinct from no value, otherwise list().
  - Value choice on state is distinct from no value — true gives state, false gives list().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L6050) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1415) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L911)

<a id="op-1091467da12cb8"></a>
### FIFOValuation.state

`operation_enterprise_stock_valuation_business_behavior_first_in_first_out_valuation_state`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** list at StockBin.

**Explicit results** self.queue.

**Local steps**

- Return self.queue.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L6149) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1417) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L913)

<a id="op-912237be0354e9"></a>
### FIFOValuation.add stock

`operation_enterprise_stock_valuation_business_behavior_first_in_first_out_valuation_add_stock`

**Inputs** self, qty, rate.

**Declared result** no value.

**Local steps**

- If not len(self.queue).
  - Evaluate self.queue.append(list(0, 0)).
- If self.queue at negative 1 at RATE equals rate.
  - Update self.queue at negative 1 at QTY using + qty.
- Otherwise.
  - If self.queue at negative 1 at QTY &gt; 0.
    - Evaluate self.queue.append(list(qty, rate)).
  - Otherwise.
    - Set qty from (self.queue at negative 1 at QTY + qty).
    - If qty &gt; 0.
      - Set self.queue at negative 1 from list(qty, rate).
    - Otherwise.
      - Set self.queue at negative 1 at QTY from qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L6207) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1414) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L910)

<a id="op-00dfaadc69c3a5"></a>
### FIFOValuation.remove stock

`operation_enterprise_stock_valuation_business_behavior_first_in_first_out_valuation_remove_stock`

**Inputs** self, qty, outgoing\_rate = 0.0, rate\_generator = no value, is\_return\_purchase\_entry = false.

**Declared result** list at StockBin.

**Explicit results** consumed\_bins.

**Local steps**

- If not rate\_generator.
  - Set rate\_generator from deferred anonymous expression.
- Set consumed\_bins from list().
- While qty.
  - If not len(self.queue).
    - Evaluate self.queue.append(list(0, rate\_generator())).
  - Set index from no value.
  - If (outgoing\_rate &gt; 0 or is\_return\_purchase\_entry).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in outgoing\_rate &gt; 0 → is\_return\_purchase\_entry.
    - For each tuple(idx, fifo\_bin) in enumerate(self.queue).
      - If fifo\_bin at RATE equals outgoing\_rate.
        - Set index from idx.
        - Leave the innermost loop without its normal-exhaustion alternative.
    - If index is identical to no value.
      - Set index from 0.
  - Otherwise.
    - Set index from 0.
  - Set fifo\_bin from self.queue at index.
  - If qty ≥ fifo\_bin at QTY.
    - Set qty from round\_off\_if\_near\_zero((qty − fifo\_bin at QTY)).
    - Set to\_consume from self.queue.pop(index).
    - Evaluate consumed\_bins.append(list(to\_consume)).
    - If (not self.queue and qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.queue → qty.
      - Evaluate self.queue.append(list(negative qty, (outgoing\_rate or fifo\_bin at RATE))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in outgoing\_rate → fifo\_bin at RATE.
      - Evaluate consumed\_bins.append(list(qty, (outgoing\_rate or fifo\_bin at RATE))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in outgoing\_rate → fifo\_bin at RATE.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - Otherwise.
    - Set fifo\_bin at QTY from round\_off\_if\_near\_zero((fifo\_bin at QTY − qty)).
    - Evaluate consumed\_bins.append(list(qty, fifo\_bin at RATE)).
    - Set qty from 0.
- Return consumed\_bins.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L6625) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1416) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L912)

<a id="op-f0d25b4c4015dd"></a>
### LIFOValuation.initialize

`operation_enterprise_stock_valuation_business_behavior_last_in_first_out_valuation_initialize`

**Inputs** self, state.

**Local steps**

- Set self.stack from state when state is distinct from no value, otherwise list().
  - Value choice on state is distinct from no value — true gives state, false gives list().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L7463) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1419) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L915)

<a id="op-a915bd89bbef92"></a>
### LIFOValuation.state

`operation_enterprise_stock_valuation_business_behavior_last_in_first_out_valuation_state`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** list at StockBin.

**Explicit results** self.stack.

**Local steps**

- Return self.stack.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L7562) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1421) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L917)

<a id="op-d61de182e426f3"></a>
### LIFOValuation.add stock

`operation_enterprise_stock_valuation_business_behavior_last_in_first_out_valuation_add_stock`

**Inputs** self, qty, rate.

**Declared result** no value.

**Local steps**

- If not len(self.stack).
  - Evaluate self.stack.append(list(0, 0)).
- If self.stack at negative 1 at RATE equals rate.
  - Update self.stack at negative 1 at QTY using + qty.
- Otherwise.
  - If self.stack at negative 1 at QTY &gt; 0.
    - Evaluate self.stack.append(list(qty, rate)).
  - Otherwise.
    - Set qty from (self.stack at negative 1 at QTY + qty).
    - If qty &gt; 0.
      - Set self.stack at negative 1 from list(qty, rate).
    - Otherwise.
      - Set self.stack at negative 1 at QTY from qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0949.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1418) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L914)

<a id="op-af746379ca079d"></a>
### LIFOValuation.remove stock

`operation_enterprise_stock_valuation_business_behavior_last_in_first_out_valuation_remove_stock`

**Inputs** self, qty, outgoing\_rate = 0.0, rate\_generator = no value, is\_return\_purchase\_entry = false.

**Declared result** list at StockBin.

**Explicit results** consumed\_bins.

**Local steps**

- If not rate\_generator.
  - Set rate\_generator from deferred anonymous expression.
- Set consumed\_bins from list().
- While qty.
  - If not len(self.stack).
    - Evaluate self.stack.append(list(0, rate\_generator())).
  - Set index from negative 1.
  - If is\_return\_purchase\_entry.
    - Set index from next(generator of idx for idx drawn from reversed(range(len(self.stack))) where self.stack at idx at RATE equals outgoing\_rate, negative 1).
      - Draw idx from reversed(range(len(self.stack))), keep a combination only if (self.stack at idx at RATE equals outgoing\_rate).
  - Set stock\_bin from self.stack at index.
  - If qty ≥ stock\_bin at QTY.
    - Set qty from round\_off\_if\_near\_zero((qty − stock\_bin at QTY)).
    - Set to\_consume from self.stack.pop(index).
    - Evaluate consumed\_bins.append(list(to\_consume)).
    - If (not self.stack and qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.stack → qty.
      - Evaluate self.stack.append(list(negative qty, (outgoing\_rate or stock\_bin at RATE))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in outgoing\_rate → stock\_bin at RATE.
      - Evaluate consumed\_bins.append(list(qty, (outgoing\_rate or stock\_bin at RATE))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in outgoing\_rate → stock\_bin at RATE.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - Otherwise.
    - Set stock\_bin at QTY from round\_off\_if\_near\_zero((stock\_bin at QTY − qty)).
    - Evaluate consumed\_bins.append(list(qty, stock\_bin at RATE)).
    - Set qty from 0.
- Return consumed\_bins.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L916)

<a id="op-96456b30b64593"></a>
### Round off if near zero

`operation_enterprise_stock_valuation_business_behavior_round_off_if_near_zero`

**Inputs** number, precision = 7.

**Declared result** float.

**Explicit results** 0.0 · flt(number).

**Local steps**

- If abs((0.0 − flt(number))) &lt; (1.0 ÷ (10 to the power precision)).
  - Return 0.0.
- Return flt(number).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0949.json#L1102) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1422) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L918)

## Service · Valuation adjustment

<a id="op-915eff38656c9d"></a>
### Adjustment Row.key

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmentrow_key`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** tuple.

**Explicit results** tuple((self.batch\_no or no value), tuple(sorted(self.serial\_nos)), flt(self.qty, 6)).

**Local steps**

- Return tuple((self.batch\_no or no value), tuple(sorted(self.serial\_nos)), flt(self.qty, 6)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.batch\_no → no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1663) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1160)
