# Inventory and warehouses · operations 91

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock ledger

<a id="op-036cb973ba0fad"></a>
### Update entries after.update serial batch no valuation

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_serial_batch_number_valuation`

**Inputs** self, sle, doc, prev\_sle = no value.

**State and service calls** request set\_value on “Serial and Batch Entry” · request set\_value on “Serial and Batch Bundle”.

**Explicit results** no value.

**Local steps**

- Bind dependencies BatchNoValuation, SerialNoValuation.
- Set sabb\_data from get\_serial\_from\_sabb(sle.serial\_and\_batch\_bundle).
- If not sabb\_data.
  - Evaluate doc.update(mapping(“total\_amount” → 0.0, “total\_qty” → 0.0, “avg\_rate” → 0.0)).
  - Return no value.
- Set serial\_nos from list of d.serial\_no for d drawn from sabb\_data where d.serial\_no.
  - Draw d from sabb\_data, keep a combination only if (d.serial\_no).
- If serial\_nos.
  - Set sle at “serial\_nos” from get\_serial\_nos\_data(“,”.join(serial\_nos)).
  - Set sn\_obj from SerialNoValuation(sle = sle, item\_code = sle.item\_code, warehouse = sle.warehouse).
- Otherwise.
  - Set sle at “batch\_nos” from mapping of row.batch\_no → row for row drawn from sabb\_data where row.batch\_no.
    - Draw row from sabb\_data, keep a combination only if (row.batch\_no).
  - Set sn\_obj from BatchNoValuation(sle = sle, item\_code = sle.item\_code, warehouse = sle.warehouse, prev\_sle = prev\_sle).
- Set tot\_amt from 0.0.
- Set total\_qty from 0.0.
- Set avg\_rate from 0.0.
- For each d in sabb\_data.
  - Set incoming\_rate from get\_incoming\_rate\_for\_serial\_and\_batch(sle.item\_code, d, sn\_obj, self.company).
  - Set amount from (incoming\_rate × flt(d.qty)).
  - Update tot\_amt using + flt(amount).
  - Update total\_qty using + flt(d.qty).
  - If (flt(incoming\_rate, self.currency\_precision) equals flt(d.incoming\_rate, self.currency\_precision) and not getattr(d, “stock\_queue”, no value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(incoming\_rate, self.currency\_precision) equals flt(d.incoming\_rate, self.currency\_precision) → not getattr(d, “stock\_queue”, no value).
    - Continue with the next iteration or loop test.
  - Set values\_to\_update from mapping(“incoming\_rate” → incoming\_rate, “stock\_value\_difference” → amount).
  - If d.stock\_queue.
    - Set values\_to\_update at “stock\_queue” from d.stock\_queue.
  - Evaluate Platform.db.set\_value(“Serial and Batch Entry”, d.name, values\_to\_update, update\_modified = false).
- If total\_qty.
  - Set avg\_rate from (tot\_amt ÷ total\_qty).
- Evaluate doc.update(mapping(“total\_amount” → tot\_amt, “total\_qty” → total\_qty, “avg\_rate” → avg\_rate)).
- Evaluate Platform.db.set\_value(“Serial and Batch Bundle”, sle.serial\_and\_batch\_bundle, mapping(“total\_qty” → total\_qty, “avg\_rate” → avg\_rate, “total\_amount” → tot\_amt), update\_modified = false).
- For each key in tuple(“serial\_nos”, “batch\_nos”).
  - If key belongs to sle.
    - Remove sle at key.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(d, “stock\_queue”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1284) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L793)

<a id="op-a6405c735dc43f"></a>
### Update entries after.get reserved stock to keep

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_get_reserved_stock_to_keep`

**Inputs** self, sle.

**Record and data access** read “Stock Reconciliation Item” via get\_value.

**Explicit results** reserved\_stock · max((reserved\_stock − flt(counted\_qty)), 0).

**Local steps**

- Set reserved\_stock from flt(self.get\_reserved\_stock(sle.item\_code, sle.warehouse)).
- If (not reserved\_stock or sle.voucher\_type differs from “Stock Reconciliation” or flt(sle.actual\_qty) ≥ 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not reserved\_stock → sle.voucher\_type differs from “Stock Reconciliation” → flt(sle.actual\_qty) ≥ 0.
  - Return reserved\_stock.
- Set counted\_qty from Platform.db.get\_value(“Stock Reconciliation Item”, sle.voucher\_detail\_no, “qty”).
- Return max((reserved\_stock − flt(counted\_qty)), 0).

**Methods declared on this owner** [get reserved stock](operations-089.md#op-c1d0e0e037b732).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1617) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1114)

<a id="op-fadd8b554db67d"></a>
### Update entries after.get outgoing rate for batched item

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_outgoing_rate_for_batched_item`

**Inputs** self, sle.

**Explicit results** 0 · (flt(self.wh\_data.stock\_value) ÷ flt(self.wh\_data.qty\_after\_transaction)).

**Local steps**

- If self.wh\_data.qty\_after\_transaction equals 0.
  - Return 0.
- Return (flt(self.wh\_data.stock\_value) ÷ flt(self.wh\_data.qty\_after\_transaction)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0939.json#L1196) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1245) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L757)

<a id="op-ee296855de420e"></a>
### Update entries after.validate negative stock

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_validate_negative_stock`

**Inputs** self, sle.

**Explicit results** false · true.

**Local steps**

- Set diff from ((self.wh\_data.qty\_after\_transaction + flt(sle.actual\_qty)) − self.get\_reserved\_stock\_to\_keep(sle)).
- Set diff from flt(diff, self.flt\_precision).
- Set diff\_threshold from 0.0001.
- If self.flt\_precision &gt; 4.
  - Set diff\_threshold from (10 to the power (negative 1 × self.flt\_precision)).
- If (diff &lt; 0 and abs(diff) &gt; diff\_threshold).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in diff &lt; 0 → abs(diff) &gt; diff\_threshold.
  - Set exc from sle.copy().update(mapping(“diff” → diff)).
  - Evaluate self.exceptions.setdefault(sle.warehouse, list()).append(exc).
  - Return false.
- Otherwise.
  - Return true.

**Methods declared on this owner** [get reserved stock to keep](operations-091.md#op-a6405c735dc43f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1285) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L794)

<a id="op-08efb4406b4dd4"></a>
### Update entries after.get dynamic incoming outgoing rate

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_dynamic_incoming_outgoing_rate`

**Inputs** self, sle.

**Local steps**

- If (sle.recalculate\_rate or self.has\_landed\_cost\_based\_on\_pi(sle) or (sle.voucher\_type equals “Stock Entry” and sle.actual\_qty &gt; 0 and is\_repack\_entry(sle.voucher\_no)) or is\_manufactured\_finished\_good(sle) or ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.recalculate\_rate → self.has\_landed\_cost\_based\_on\_pi(sle) → (sle.voucher\_type equals “Stock Entry” and sle.actual\_qty &gt; 0 and is\_repack\_entry(sle.voucher\_no)) → is\_manufactured\_finished\_good(sle) → self.recalculates\_voucher(sle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Stock Entry” → sle.actual\_qty &gt; 0 → is\_repack\_entry(sle.voucher\_no).
  - Set rate from self.get\_incoming\_outgoing\_rate\_from\_transaction(sle).
  - If flt(sle.actual\_qty) ≥ 0.
    - Set sle.incoming\_rate from rate.
  - Otherwise.
    - Set sle.outgoing\_rate from rate.
- Otherwise.
  - If self.has\_stale\_serial\_no\_wise\_outgoing\_rate(sle).
    - Set sle.outgoing\_rate from flt(self.wh\_data.valuation\_rate).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has landed cost based on pi](operations-091.md#op-c69d5137a8fb84), [recalculates voucher](operations-091.md#op-fd6d3617b98aca), [get incoming outgoing rate from transaction](operations-091.md#op-fe790f1ec4b411), [has stale serial no wise outgoing rate](operations-091.md#op-0e4f6630b66549).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L747)

<a id="op-66c12673ec7e33"></a>
### Update entries after.has bundle valuation

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_has_bundle_valuation`

**Inputs** self, sle.

**Explicit results** bool((sle.serial\_and\_batch\_bundle and not self.skip\_serial\_batch\_valuation)).

**Local steps**

- Return bool((sle.serial\_and\_batch\_bundle and not self.skip\_serial\_batch\_valuation)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.serial\_and\_batch\_bundle → not self.skip\_serial\_batch\_valuation.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1620) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1117)

<a id="op-99e99108f16a17"></a>
### Update entries after.is inward transfer leg

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_is_inward_transfer_leg`

**Inputs** self, sle.

**Record and data access** read formatted text {sle.voucher\_type} Item via get\_value.

**Explicit results** false · true · bool((row and row.item\_code equals sle.item\_code and row.target\_warehouse equals sle.warehouse)).

**Local steps**

- If not (sle.recalculate\_rate and flt(sle.actual\_qty) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.recalculate\_rate → flt(sle.actual\_qty) &gt; 0.
  - Return false.
- If sle.voucher\_type equals “Stock Entry”.
  - Return true.
- If sle.voucher\_type does not belong to tuple(“Delivery Note”, “Sales Invoice”).
  - Return false.
- Set row from Platform.db.get\_value(formatted text {sle.voucher\_type} Item, sle.voucher\_detail\_no, list(“item\_code”, “target\_warehouse”), as\_dict = true).
- Return bool((row and row.item\_code equals sle.item\_code and row.target\_warehouse equals sle.warehouse)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row → row.item\_code equals sle.item\_code → row.target\_warehouse equals sle.warehouse.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1622) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1119)

<a id="op-39744cade41828"></a>
### Update entries after.is outward internal transfer leg

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_is_outward_internal_transfer_leg`

**Inputs** self, sle.

**Explicit results** bool((sle.voucher\_type belongs to tuple(“Delivery Note”, “Sales Invoice”) and sle.dependant\_sle\_voucher\_detail\_no and flt(sle.actual\_qty) &lt; 0)).

**Local steps**

- Return bool((sle.voucher\_type belongs to tuple(“Delivery Note”, “Sales Invoice”) and sle.dependant\_sle\_voucher\_detail\_no and flt(sle.actual\_qty) &lt; 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type belongs to tuple(“Delivery Note”, “Sales Invoice”) → sle.dependant\_sle\_voucher\_detail\_no → flt(sle.actual\_qty) &lt; 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1120)

<a id="op-ee95f96a3d18d9"></a>
### Update entries after.get incoming rate from outward leg

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_get_incoming_rate_from_outward_leg`

**Inputs** self, sle.

**Explicit results** sle.incoming\_rate · (outward\_value ÷ flt(sle.actual\_qty)).

**Local steps**

- Set outward\_value from self.get\_outward\_leg\_value(sle).
- If outward\_value is identical to no value.
  - Return sle.incoming\_rate.
- Return (outward\_value ÷ flt(sle.actual\_qty)).

**Methods declared on this owner** [get outward leg value](operations-091.md#op-71dc4eb93aee5d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1613) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1110)

<a id="op-ff4cbc12d2cdef"></a>
### Update entries after.is produced row

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_is_produced_row`

**Inputs** self, sle.

**Explicit results** bool((sle.voucher\_type equals “Stock Entry” and flt(sle.actual\_qty) &gt; 0 and is\_manufacture\_or\_repack\_entry(sle.voucher\_no))).

**Local steps**

- Return bool((sle.voucher\_type equals “Stock Entry” and flt(sle.actual\_qty) &gt; 0 and is\_manufacture\_or\_repack\_entry(sle.voucher\_no))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Stock Entry” → flt(sle.actual\_qty) &gt; 0 → is\_manufacture\_or\_repack\_entry(sle.voucher\_no).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1121)

<a id="op-f8f7b80aa14e1d"></a>
### Update entries after.update bundle rate

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_update_bundle_rate`

**Inputs** self, bundle, rate.

**State and service calls** call db\_set on entry.

**Local steps**

- For each entry in bundle.entries.
  - If entry.incoming\_rate differs from rate.
    - Evaluate entry.db\_set(mapping(“incoming\_rate” → rate, “stock\_value\_difference” → (flt(entry.qty) × rate))).
- Evaluate bundle.calculate\_qty\_and\_amount(save = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1631) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1128)

<a id="op-af41d2f32f7a6b"></a>
### Update entries after.get produced row rate

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_get_produced_row_rate`

**Inputs** self, sle.

**Record and data access** read “Stock Entry Detail” via get\_all · read “Stock Ledger Entry” via get\_all · read “Stock Entry” via get\_value.

**Explicit results** sle.incoming\_rate · (flt(row.amount) ÷ flt(sle.actual\_qty)) · (max(value, 0) ÷ flt(sle.actual\_qty)).

**Local steps**

- Set rows from Platform.get\_all(“Stock Entry Detail”, filters = mapping(“parent” → sle.voucher\_no), fields = list(“name”, “s\_warehouse”, “t\_warehouse”, “amount”, …), order\_by = “amount desc, idx asc”).
- Set outputs from list of d for d drawn from rows where (d.t\_warehouse and not d.s\_warehouse).
  - Draw d from rows, keep a combination only if ((d.t\_warehouse and not d.s\_warehouse)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.t\_warehouse → not d.s\_warehouse.
- Set row from next(generator of d for d drawn from outputs where d.name equals sle.voucher\_detail\_no, no value).
  - Draw d from outputs, keep a combination only if (d.name equals sle.voucher\_detail\_no).
- Set absorber from next(generator of d for d drawn from outputs where (d.is\_finished\_item and not d.allow\_zero\_valuation\_rate), no value).
  - Draw d from outputs, keep a combination only if ((d.is\_finished\_item and not d.allow\_zero\_valuation\_rate)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_finished\_item → not d.allow\_zero\_valuation\_rate.
- If (not row or not absorber or any(generator of d.set\_basic\_rate\_manually for d drawn from outputs)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row → not absorber → any(generator of d.set\_basic\_rate\_manually for d drawn from outputs).
  - Draw d from outputs.
  - Return sle.incoming\_rate.
- If row.name differs from absorber.name.
  - Return (flt(row.amount) ÷ flt(sle.actual\_qty)).
- Set consumed from Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → “Stock Entry”, “voucher\_no” → sle.voucher\_no, “actual\_qty” → tuple(“&lt;”, 0), “is\_cancelled” → 0), pluck = “stock\_value\_difference”).
- If not consumed.
  - Return sle.incoming\_rate.
- Set additional\_cost from Platform.db.get\_value(“Stock Entry”, sle.voucher\_no, “total\_additional\_costs”).
- Set landed\_cost from sum(generator of flt(d.landed\_cost\_voucher\_amount) for d drawn from outputs).
  - Draw d from outputs.
- Set other\_outputs from sum(generator of flt(d.amount) for d drawn from outputs where d.name differs from row.name).
  - Draw d from outputs, keep a combination only if (d.name differs from row.name).
- Set value from (((negative sum(generator of nested operand in the contract(nested operand in the contract) for v drawn from consumed) + flt(additional\_cost)) + landed\_cost) − other\_outputs).
  - Draw v from consumed.
- Return (max(value, 0) ÷ flt(sle.actual\_qty)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1113)

<a id="op-71dc4eb93aee5d"></a>
### Update entries after.get outward leg value

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_get_outward_leg_value`

**Inputs** self, sle.

**Record and data access** read “Stock Ledger Entry” via get\_value · read “Stock Entry Detail” via get\_value.

**Explicit results** no value · abs(flt(outward\_value)) · (abs(flt(outward\_value)) + flt(additional\_cost)).

**Local steps**

- Set outward\_value from Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_type” → sle.voucher\_type, “voucher\_no” → sle.voucher\_no, “voucher\_detail\_no” → sle.voucher\_detail\_no, “item\_code” → sle.item\_code, …), “stock\_va ….
- If outward\_value is identical to no value.
  - Return no value.
- If sle.voucher\_type differs from “Stock Entry”.
  - Return abs(flt(outward\_value)).
- Set additional\_cost from Platform.db.get\_value(“Stock Entry Detail”, sle.voucher\_detail\_no, “additional\_cost”).
- Return (abs(flt(outward\_value)) + flt(additional\_cost)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1112)

<a id="op-0e4f6630b66549"></a>
### Update entries after.has stale serial no wise outgoing rate

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_has_stale_serial_no_wise_outgoing_rate`

**Inputs** self, sle.

**Explicit results** bool((self.skip\_serial\_batch\_valuation and self.valuation\_method equals “Moving Average” and flt(sle.actual\_qty) &lt; 0 and flt(sle.outgoing\_rate))).

**Local steps**

- Return bool((self.skip\_serial\_batch\_valuation and self.valuation\_method equals “Moving Average” and flt(sle.actual\_qty) &lt; 0 and flt(sle.outgoing\_rate))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.skip\_serial\_batch\_valuation → self.valuation\_method equals “Moving Average” → flt(sle.actual\_qty) &lt; 0 → flt(sle.outgoing\_rate).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1621) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1118)

<a id="op-fd6d3617b98aca"></a>
### Update entries after.recalculates voucher

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_recalculates_voucher`

**Inputs** self, sle.

**Explicit results** bool((self.repost\_doc and self.repost\_doc.get(“recalculate\_valuation\_rate”) and sle.voucher\_type equals self.repost\_doc.voucher\_type and sle.voucher\_no equals self.repost\_doc.voucher\_no)).

**Local steps**

- Return bool((self.repost\_doc and self.repost\_doc.get(“recalculate\_valuation\_rate”) and sle.voucher\_type equals self.repost\_doc.voucher\_type and sle.voucher\_no equals self.repost\_doc.voucher\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.repost\_doc → self.repost\_doc.get(“recalculate\_valuation\_rate”) → sle.voucher\_type equals self.repost\_doc.voucher\_type → sle.voucher\_no equals self.repost\_doc.voucher\_no.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1627) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1124)

<a id="op-c69d5137a8fb84"></a>
### Update entries after.has landed cost based on pi

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_has_landed_cost_based_on_purchase_invoice`

**Inputs** self, sle.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** true · false.

**Local steps**

- If (sle.voucher\_type equals “Purchase Receipt” and Platform.db.get\_single\_value(“Buying Settings”, “set\_landed\_cost\_based\_on\_purchase\_invoice\_rate”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Purchase Receipt” → Platform.db.get\_single\_value(“Buying Settings”, “set\_landed\_cost\_based\_on\_purchase\_invoice\_rate”).
  - Return true.
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “set\_landed\_cost\_based\_on\_purchase\_invoice\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0939.json#L2014) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1251) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L762)

<a id="op-fe790f1ec4b411"></a>
### Update entries after.get incoming outgoing rate from transaction

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_incoming_outgoing_rate_from_transaction`

**Inputs** self, sle.

**Record and data access** read “Stock Entry Detail” via get\_value · read sle.voucher\_type via get\_cached\_value · read (sle.voucher\_type + “ Item”) via get\_value · read ref\_doctype via get\_value.

**State and service calls** request set\_value on (sle.voucher\_type + “ Item”).

**Explicit results** rate.

**Local steps**

- Set rate from 0.
- If sle.voucher\_type equals “Stock Entry”.
  - Evaluate self.recalculate\_amounts\_in\_stock\_entry(sle.voucher\_no, sle.voucher\_detail\_no).
  - Set rate from Platform.db.get\_value(“Stock Entry Detail”, sle.voucher\_detail\_no, “valuation\_rate”).
- Otherwise.
  - If self.is\_returned\_supplied\_item(sle).
    - Set rate from self.get\_returned\_supplied\_item\_rate(sle).
  - Otherwise.
    - If sle.voucher\_type belongs to tuple(“Purchase Receipt”, “Purchase Invoice”, “Delivery Note”, “Sales Invoice”, …).
      - If Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, “is\_return”).
        - Bind dependencies get\_rate\_for\_return.
        - If (self.valuation\_method equals “Moving Average” and (self.skip\_serial\_batch\_valuation or not (sle.get(“serial\_no”) or sle.get(“batch\_no”) or sle.get(“serial\_and\_batch\_bundle”)))).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.valuation\_method equals “Moving Average” → (self.skip\_serial\_batch\_valuation or not (sle.get(“serial\_no”) or sle.get(“batch\_no”) or sle.get(“serial\_and\_batch\_bundle”))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.skip\_serial\_batch\_valuation → not (sle.get(“serial\_no”) or sle.get(“batch\_no”) or sle.get(“serial\_and\_batch\_bundle”)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.get(“serial\_no”) → sle.get(“batch\_no”) → sle.get(“serial\_and\_batch\_bundle”).
          - Set rate from self.get\_moving\_average\_rate\_for\_return(sle).
          - If (not rate and sle.voucher\_type belongs to list(“Delivery Note”, “Sales Invoice”)).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in not rate → sle.voucher\_type belongs to list(“Delivery Note”, “Sales Invoice”).
            - Set rate from get\_rate\_for\_return(sle.voucher\_type, sle.voucher\_no, sle.item\_code, voucher\_detail\_no = sle.voucher\_detail\_no, sle = sle).
        - Otherwise.
          - If (self.skip\_serial\_batch\_valuation and flt(sle.actual\_qty) &lt; 0).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.skip\_serial\_batch\_valuation → flt(sle.actual\_qty) &lt; 0.
            - Set rate from 0.0.
          - Otherwise.
            - Set rate from get\_rate\_for\_return(sle.voucher\_type, sle.voucher\_no, sle.item\_code, voucher\_detail\_no = sle.voucher\_detail\_no, sle = sle).
        - If (sle.get(“serial\_and\_batch\_bundle”) and rate &gt; 0 and sle.voucher\_type belongs to list(“Delivery Note”, “Sales Invoice”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.get(“serial\_and\_batch\_bundle”) → rate &gt; 0 → sle.voucher\_type belongs to list(“Delivery Note”, “Sales Invoice”).
          - Evaluate Platform.db.set\_value((sle.voucher\_type + “ Item”), sle.voucher\_detail\_no, “incoming\_rate”, rate).
      - Otherwise.
        - If (sle.voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”) and sle.voucher\_detail\_no and is\_internal\_transfer(sle)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”) → sle.voucher\_detail\_no → is\_internal\_transfer(sle).
          - Set rate from get\_incoming\_rate\_for\_inter\_company\_transfer(sle).
        - Otherwise.
          - If sle.voucher\_type belongs to tuple(“Purchase Receipt”, “Purchase Invoice”).
            - Set rate\_field from “valuation\_rate”.
          - Otherwise.
            - If sle.voucher\_type equals “Subcontracting Receipt”.
              - Set rate\_field from “rate”.
            - Otherwise.
              - Set rate\_field from “incoming\_rate”.
          - Set tuple(item\_code, incoming\_rate) from Platform.db.get\_value((sle.voucher\_type + “ Item”), sle.voucher\_detail\_no, list(“item\_code”, rate\_field)).
          - If item\_code equals sle.item\_code.
            - Set rate from 0.0 when self.is\_unvalued\_rejected\_material(sle), otherwise incoming\_rate.
              - Value choice on self.is\_unvalued\_rejected\_material(sle) — true gives 0.0, false gives incoming\_rate.
          - Otherwise.
            - If sle.voucher\_type belongs to tuple(“Delivery Note”, “Sales Invoice”).
              - Set ref\_doctype from “Packed Item”.
            - Otherwise.
              - If sle.voucher\_type equals “Subcontracting Receipt”.
                - Set ref\_doctype from “Subcontracting Receipt Supplied Item”.
              - Otherwise.
                - Set ref\_doctype from “Purchase Receipt Item Supplied”.
            - Set rate from Platform.db.get\_value(ref\_doctype, mapping(“parent\_detail\_docname” → sle.voucher\_detail\_no, “item\_code” → sle.item\_code), rate\_field).
- Return rate.

**Methods declared on this owner** [recalculate amounts in stock entry](operations-091.md#op-2bb64bdd878e9e), [is returned supplied item](operations-091.md#op-44e95ee27994f2), [get returned supplied item rate](operations-091.md#op-226ab0f6d8bc81), [get moving average rate for return](operations-091.md#op-186faad667b168), [is unvalued rejected material](operations-091.md#op-21523aba77729c).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, “is\_return”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1240) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L752)

<a id="op-44e95ee27994f2"></a>
### Update entries after.is returned supplied item

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_is_returned_supplied_item`

**Inputs** sle.

**Wrappers, in declaration order** staticmethod.

**Explicit results** (sle.voucher\_type equals “Subcontracting Receipt” and flt(sle.actual\_qty) &gt; 0 and bool(sle.dependant\_sle\_voucher\_detail\_no)).

**Local steps**

- Return (sle.voucher\_type equals “Subcontracting Receipt” and flt(sle.actual\_qty) &gt; 0 and bool(sle.dependant\_sle\_voucher\_detail\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Subcontracting Receipt” → flt(sle.actual\_qty) &gt; 0 → bool(sle.dependant\_sle\_voucher\_detail\_no).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1122)

<a id="op-226ab0f6d8bc81"></a>
### Update entries after.get returned supplied item rate

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_get_returned_supplied_item_rate`

**Inputs** sle.

**Wrappers, in declaration order** staticmethod.

**Record and data access** resolve a document from “Subcontracting Receipt” via get\_doc.

**Explicit results** scr.get\_supplied\_item\_rates(list(row)) at 0.

**Local steps**

- Set scr from Platform.get\_doc(“Subcontracting Receipt”, sle.voucher\_no).
- Set row from scr.getone(“supplied\_items”, mapping(“name” → sle.voucher\_detail\_no)).
- Return scr.get\_supplied\_item\_rates(list(row)) at 0.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1618) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1115)

<a id="op-21523aba77729c"></a>
### Update entries after.is unvalued rejected material

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_is_unvalued_rejected_material`

**Inputs** self, sle.

**Record and data access** read formatted text {sle.voucher\_type} Item via get\_value · read “Buying Settings” via get\_single\_value.

**Explicit results** false · (sle.warehouse equals rejected\_warehouse and (sle.voucher\_type equals “Subcontracting Receipt” or not Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”))).

**Local steps**

- If sle.voucher\_type does not belong to tuple(“Purchase Receipt”, “Purchase Invoice”, “Subcontracting Receipt”).
  - Return false.
- Set rejected\_warehouse from Platform.db.get\_value(formatted text {sle.voucher\_type} Item, sle.voucher\_detail\_no, “rejected\_warehouse”).
- Return (sle.warehouse equals rejected\_warehouse and (sle.voucher\_type equals “Subcontracting Receipt” or not Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.warehouse equals rejected\_warehouse → (sle.voucher\_type equals “Subcontracting Receipt” or not Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.voucher\_type equals “Subcontracting Receipt” → not Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1123)

<a id="op-186faad667b168"></a>
### Update entries after.get moving average rate for return

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_moving_average_rate_for_return`

**Inputs** self, sle.

**Explicit results** rate · flt(rate).

**Local steps**

- Set rate from flt(self.wh\_data.valuation\_rate).
- If rate.
  - Return rate.
- Set previous\_sle from get\_previous\_sle\_of\_current\_voucher(Platform.\_dict(item\_code = sle.item\_code, warehouse = sle.warehouse, posting\_date = sle.posting\_date, posting\_time = sle.posting\_time, …), exclude\_current\_voucher = true).
- Set rate from previous\_sle.get(“valuation\_rate”).
- If rate is identical to no value.
  - Set rate from self.get\_fallback\_rate(sle).
- Return flt(rate).

**Methods declared on this owner** [get fallback rate](operations-092.md#op-c1ee762e31f9b4).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1243) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L755)

<a id="op-6c550a94b91e06"></a>
### Update entries after.update outgoing rate on transaction

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_outgoing_rate_on_transaction`

**Inputs** self, sle.

**Record and data access** resolve a document from sle.voucher\_type via get\_doc.

**Explicit results** no value.

**Local steps**

- If sle.voucher\_type equals “Stock Reconciliation”.
  - If not self.args.get(“sle\_id”).
    - Evaluate self.update\_rate\_on\_stock\_reconciliation(sle).
  - Return no value.
- If (sle.actual\_qty and sle.voucher\_detail\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.actual\_qty → sle.voucher\_detail\_no.
  - Set outgoing\_rate from (abs(flt(sle.stock\_value\_difference)) ÷ abs(sle.actual\_qty)).
  - If (flt(sle.actual\_qty) &lt; 0 and sle.voucher\_type equals “Stock Entry”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(sle.actual\_qty) &lt; 0 → sle.voucher\_type equals “Stock Entry”.
    - Evaluate self.update\_rate\_on\_stock\_entry(sle, outgoing\_rate).
  - Otherwise.
    - If sle.voucher\_type belongs to tuple(“Delivery Note”, “Sales Invoice”).
      - Evaluate self.update\_rate\_on\_delivery\_and\_sales\_return(sle, outgoing\_rate).
    - Otherwise.
      - If (flt(sle.actual\_qty) &lt; 0 and sle.voucher\_type belongs to tuple(“Purchase Receipt”, “Purchase Invoice”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(sle.actual\_qty) &lt; 0 → sle.voucher\_type belongs to tuple(“Purchase Receipt”, “Purchase Invoice”).
        - Evaluate self.update\_rate\_on\_purchase\_receipt(sle, outgoing\_rate).
      - Otherwise.
        - If (sle.voucher\_type equals “Subcontracting Receipt” and (flt(sle.actual\_qty) &lt; 0 or self.is\_returned\_supplied\_item(sle))).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Subcontracting Receipt” → (flt(sle.actual\_qty) &lt; 0 or self.is\_returned\_supplied\_item(sle)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(sle.actual\_qty) &lt; 0 → self.is\_returned\_supplied\_item(sle).
          - Evaluate self.update\_rate\_on\_subcontracting\_receipt(sle, outgoing\_rate).
        - Otherwise.
          - If (flt(sle.actual\_qty) &lt; 0 and sle.voucher\_type equals “Asset Capitalization”).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(sle.actual\_qty) &lt; 0 → sle.voucher\_type equals “Asset Capitalization”.
            - Evaluate Platform.get\_doc(sle.voucher\_type, sle.voucher\_no).update\_stock\_item\_rate(sle.voucher\_detail\_no, outgoing\_rate).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update rate on stock reconciliation](operations-092.md#op-4fa7a84d022feb), [update rate on stock entry](operations-091.md#op-d519896a51407f), [update rate on delivery and sales return](operations-092.md#op-48749af69859a4), [update rate on purchase receipt](operations-092.md#op-39049f20682a52), [is returned supplied item](operations-091.md#op-44e95ee27994f2), [update rate on subcontracting receipt](operations-092.md#op-b815f6e7ceacb4).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1276) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L785)

<a id="op-d519896a51407f"></a>
### Update entries after.update rate on stock entry

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_rate_on_stock_entry`

**Inputs** self, sle, outgoing\_rate.

**State and service calls** request set\_value on “Stock Entry Detail”.

**Local steps**

- Evaluate Platform.db.set\_value(“Stock Entry Detail”, sle.voucher\_detail\_no, “basic\_rate”, outgoing\_rate).
- Evaluate self.recalculated\_stock\_entries.discard(sle.voucher\_no).
- If (not self.args.get(“sle\_id”) and not sle.dependant\_sle\_voucher\_detail\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.args.get(“sle\_id”) → not sle.dependant\_sle\_voucher\_detail\_no.
  - Evaluate self.recalculate\_amounts\_in\_stock\_entry(sle.voucher\_no, sle.voucher\_detail\_no).

If control reaches the end, it returns no value.

**Methods declared on this owner** [recalculate amounts in stock entry](operations-091.md#op-2bb64bdd878e9e).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1281) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L790)

<a id="op-2bb64bdd878e9e"></a>
### Update entries after.recalculate amounts in stock entry

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_recalculate_amounts_in_stock_entry`

**Inputs** self, voucher\_no, voucher\_detail\_no.

**State and service calls** call db\_update on stock\_entry · call db\_update on d.

**Explicit results** no value.

**Local steps**

- If voucher\_no belongs to self.recalculated\_stock\_entries.
  - Return no value.
- Set stock\_entry from Platform.get\_lazy\_doc(“Stock Entry”, voucher\_no, for\_update = true).
- Set stock\_entry.flags.via\_repost from true.
- Evaluate stock\_entry.calculate\_rate\_and\_amount(reset\_outgoing\_rate = false, raise\_error\_if\_no\_rate = false).
- Evaluate stock\_entry.db\_update().
- Set update\_additional\_cost\_rows from bool(stock\_entry.get(“additional\_costs”)).
- For each d in stock\_entry.items.
  - If (d.name equals voucher\_detail\_no or (not d.s\_warehouse and d.t\_warehouse) or stock\_entry.purpose belongs to list(“Manufacture”, “Repack”) or (update\_additional\_cost\_rows and d.t\_warehouse)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.name equals voucher\_detail\_no → (not d.s\_warehouse and d.t\_warehouse) → stock\_entry.purpose belongs to list(“Manufacture”, “Repack”) → (update\_additional\_cost\_rows and d.t\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.s\_warehouse → d.t\_warehouse.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in update\_additional\_cost\_rows → d.t\_warehouse.
    - Evaluate d.db\_update().
- If (update\_additional\_cost\_rows and all(generator of d.s\_warehouse for d drawn from stock\_entry.items where d.t\_warehouse)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in update\_additional\_cost\_rows → all(generator of d.s\_warehouse for d drawn from stock\_entry.items where d.t\_warehouse).
  - Draw d from stock\_entry.items, keep a combination only if (d.t\_warehouse).
  - Evaluate self.recalculated\_stock\_entries.add(voucher\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1264) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L773)
