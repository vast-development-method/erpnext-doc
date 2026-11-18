# Inventory and warehouses · operations 69

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Stock ageing

<a id="op-a32aed9474c22a"></a>
### FIFOSlots.compute outgoing stock

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_compute_outgoing_stock`

**Inputs** self, row, fifo\_queue, transfer\_key, serial\_nos, batch\_nos, from\_end = false.

**Local steps**

- If serial\_nos.
  - Evaluate self.\_consume\_serial\_fifo\_slots(fifo\_queue, serial\_nos).
- Otherwise.
  - If batch\_nos.
    - Evaluate self.\_consume\_batch\_fifo\_slots(row, fifo\_queue, transfer\_key, batch\_nos).
  - Otherwise.
    - Evaluate self.\_consume\_fifo\_slots(row, fifo\_queue, transfer\_key, from\_end).

If control reaches the end, it returns no value.

**Methods declared on this owner** [consume serial fifo slots](operations-069.md#op-36792ec3b5918f), [consume batch fifo slots](operations-069.md#op-6d186f7b58c39d), [consume fifo slots](operations-069.md#op-ca319eb1265dd5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L4331) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L710) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L322)

<a id="op-36792ec3b5918f"></a>
### FIFOSlots.consume serial fifo slots

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_consume_serial_first_in_first_out_slots`

**Inputs** self, fifo\_queue, serial\_nos.

**Declared result** no value.

**Local steps**

- Set fifo\_queue at slice no value to no value from list of slot for slot drawn from fifo\_queue where slot at FIFO\_QTY\_INDEX does not belong to serial\_nos.
  - Draw slot from fifo\_queue, keep a combination only if (slot at FIFO\_QTY\_INDEX does not belong to serial\_nos).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L4563) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L325)

<a id="op-6d186f7b58c39d"></a>
### FIFOSlots.consume batch fifo slots

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_consume_batch_first_in_first_out_slots`

**Inputs** self, row, fifo\_queue, transfer\_key, batch\_nos.

**Declared result** no value.

**Local steps**

- For each tuple(batch\_no, use\_batchwise\_valuation, qty, stock\_value\_difference) in batch\_nos.
  - Set items\_to\_remove from list().
  - For each slot in fifo\_queue.
    - If not self.\_can\_consume\_batch\_slot(slot, batch\_no, use\_batchwise\_valuation).
      - Continue with the next iteration or loop test.
    - Set slot\_qty from flt(slot at BATCH\_SLOT\_QTY\_INDEX).
    - Set slot\_stock\_value from flt(slot at BATCH\_SLOT\_VALUE\_INDEX).
    - If slot\_qty ≤ qty.
      - Update qty using − slot\_qty.
      - Update stock\_value\_difference using − slot\_stock\_value.
      - Evaluate self.transferred\_item\_details at transfer\_key.append(list(slot\_qty, slot at BATCH\_SLOT\_DATE\_INDEX, slot\_stock\_value)).
      - Evaluate items\_to\_remove.append(slot).
    - Otherwise.
      - Set slot at BATCH\_SLOT\_QTY\_INDEX from (slot\_qty − qty).
      - Set slot at BATCH\_SLOT\_VALUE\_INDEX from (slot\_stock\_value − stock\_value\_difference).
      - Evaluate self.transferred\_item\_details at transfer\_key.append(list(qty, slot at BATCH\_SLOT\_DATE\_INDEX, stock\_value\_difference)).
      - Set qty from 0.
      - Set stock\_value\_difference from 0.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - For each item in items\_to\_remove.
    - Evaluate fifo\_queue.remove(item).
  - If qty.
    - Evaluate self.\_append\_negative\_batch\_slot(row, fifo\_queue, transfer\_key, batch\_no, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [can consume batch slot](operations-069.md#op-fc4f32997c4846), [append negative batch slot](operations-069.md#op-284fa7cabbff1c).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L4687) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L711) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L323)

<a id="op-fc4f32997c4846"></a>
### FIFOSlots.can consume batch slot

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_can_consume_batch_slot`

**Inputs** self, slot, batch\_no, use\_batchwise\_valuation.

**Declared result** bool.

**Explicit results** false · slot at BATCH\_SLOT\_BATCH\_INDEX equals batch\_no · not slot at BATCH\_SLOT\_VALUATION\_INDEX.

**Local steps**

- If not is\_batch\_slot(slot).
  - Return false.
- If flt(slot at BATCH\_SLOT\_QTY\_INDEX) ≤ 0.
  - Return false.
- If use\_batchwise\_valuation.
  - Return slot at BATCH\_SLOT\_BATCH\_INDEX equals batch\_no.
- Return not slot at BATCH\_SLOT\_VALUATION\_INDEX.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L5292) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L320)

<a id="op-284fa7cabbff1c"></a>
### FIFOSlots.append negative batch slot

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_append_negative_batch_slot`

**Inputs** self, row, fifo\_queue, transfer\_key, batch\_no, use\_batchwise\_valuation, qty, stock\_value\_difference.

**Declared result** no value.

**Local steps**

- Evaluate fifo\_queue.append(list(batch\_no, use\_batchwise\_valuation, negative qty, row.posting\_date, …)).
- Evaluate self.batches\_with\_negative\_slots.add(tuple(batch\_no, row.warehouse)).
- Evaluate self.transferred\_item\_details at transfer\_key.append(list(qty, row.posting\_date, stock\_value\_difference)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L706) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L318)

<a id="op-ca319eb1265dd5"></a>
### FIFOSlots.consume fifo slots

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_consume_first_in_first_out_slots`

**Inputs** self, row, fifo\_queue, transfer\_key, from\_end = false.

**Declared result** no value.

**Local steps**

- Set index from negative 1 when from\_end, otherwise 0.
  - Value choice on from\_end — true gives negative 1, false gives 0.
- Set qty\_to\_pop from abs(row.actual\_qty).
- Set stock\_value from abs(row.stock\_value\_difference).
- If (qty\_to\_pop and self.\_is\_return\_entry(row)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty\_to\_pop → self.\_is\_return\_entry(row).
  - Set tuple(qty\_to\_pop, stock\_value) from self.\_consume\_slots\_at\_return\_rate(fifo\_queue, transfer\_key, qty\_to\_pop, stock\_value, …).
- While qty\_to\_pop.
  - Set slot from fifo\_queue at index when fifo\_queue, otherwise list(0, no value, 0).
    - Value choice on fifo\_queue — true gives fifo\_queue at index, false gives list(0, no value, 0).
  - Set slot\_qty from flt(slot at FIFO\_QTY\_INDEX).
  - Set slot\_value from flt(slot at FIFO\_VALUE\_INDEX).
  - If 0 &lt; slot\_qty ≤ qty\_to\_pop.
    - Compare adjacent operands in order, stopping at the first false comparison in 0 &lt; slot\_qty ≤ qty\_to\_pop.
    - Update qty\_to\_pop using − slot\_qty.
    - Update stock\_value using − slot\_value.
    - Evaluate self.transferred\_item\_details at transfer\_key.append(fifo\_queue.pop(index)).
  - Otherwise.
    - If not fifo\_queue.
      - Evaluate fifo\_queue.append(list(negative qty\_to\_pop, row.posting\_date, negative stock\_value)).
      - Evaluate self.transferred\_item\_details at transfer\_key.append(list(qty\_to\_pop, row.posting\_date, stock\_value)).
      - Set qty\_to\_pop from 0.
      - Set stock\_value from 0.
    - Otherwise.
      - Set slot at FIFO\_QTY\_INDEX from (slot\_qty − qty\_to\_pop).
      - Set slot at FIFO\_VALUE\_INDEX from (slot\_value − stock\_value).
      - Evaluate self.transferred\_item\_details at transfer\_key.append(list(qty\_to\_pop, slot at FIFO\_DATE\_INDEX, stock\_value)).
      - Set qty\_to\_pop from 0.
      - Set stock\_value from 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [is return entry](operations-069.md#op-8337a7f36300da), [consume slots at return rate](operations-069.md#op-a121d6a26740e4).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L324)

<a id="op-59afe99f4fbaf1"></a>
### FIFOSlots.get subcontracting returns

`operation_enterprise_binding_enterprise_stock_report_stock_ageing_stock_ageing_fifoslots_get_subcontracting_returns`

**Inputs** self.

**Declared result** set.

**Record and data access** read “Subcontracting Receipt” via get\_all.

**Explicit results** set(Platform.get\_all(“Subcontracting Receipt”, filters = mapping(“is\_return” → 1, “docstatus” → 1, “company” → self.filters.get(“company”)), pluck = “name”)).

**Local steps**

- Return set(Platform.get\_all(“Subcontracting Receipt”, filters = mapping(“is\_return” → 1, “docstatus” → 1, “company” → self.filters.get(“company”)), pluck = “name”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1499) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L996)

<a id="op-8337a7f36300da"></a>
### FIFOSlots.is return entry

`operation_enterprise_binding_enterprise_stock_report_stock_ageing_stock_ageing_fifoslots_is_return_entry`

**Inputs** self, row.

**Declared result** bool.

**Explicit results** true · (row.voucher\_type equals “Subcontracting Receipt” and row.voucher\_no belongs to self.subcontracting\_returns).

**Local steps**

- If row.voucher\_type belongs to PURCHASE\_VOUCHER\_TYPES.
  - Return true.
- Return (row.voucher\_type equals “Subcontracting Receipt” and row.voucher\_no belongs to self.subcontracting\_returns).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.voucher\_type equals “Subcontracting Receipt” → row.voucher\_no belongs to self.subcontracting\_returns.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1500) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L997)

<a id="op-a121d6a26740e4"></a>
### FIFOSlots.consume slots at return rate

`operation_enterprise_binding_enterprise_stock_report_stock_ageing_stock_ageing_fifoslots_consume_slots_at_return_rate`

**Inputs** self, fifo\_queue, transfer\_key, qty\_to\_pop, stock\_value, from\_end.

**Declared result** tuple at tuple(float, float).

**Explicit results** tuple(qty\_to\_pop, stock\_value).

**Local steps**

- Set return\_rate from (stock\_value ÷ qty\_to\_pop).
- For each slot in list(reversed(fifo\_queue)) when from\_end, otherwise list(fifo\_queue).
  - Value choice on from\_end — true gives list(reversed(fifo\_queue)), false gives list(fifo\_queue).
  - Set slot\_qty from flt(slot at FIFO\_QTY\_INDEX).
  - If (slot\_qty ≤ 0 or abs(((flt(nested operand in the contract at nested operand in the contract) ÷ slot\_qty) − return\_rate)) &gt; 0.01).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in slot\_qty ≤ 0 → abs(((flt(slot at FIFO\_VALUE\_INDEX) ÷ slot\_qty) − return\_rate)) &gt; 0.01.
    - Continue with the next iteration or loop test.
  - Set qty from min(slot\_qty, qty\_to\_pop).
  - Set value from ((flt(slot at FIFO\_VALUE\_INDEX) × qty) ÷ slot\_qty).
  - Set slot at FIFO\_QTY\_INDEX from (slot\_qty − qty).
  - Set slot at FIFO\_VALUE\_INDEX from (flt(slot at FIFO\_VALUE\_INDEX) − value).
  - If not slot at FIFO\_QTY\_INDEX.
    - Evaluate fifo\_queue.remove(slot).
  - Evaluate self.transferred\_item\_details at transfer\_key.append(list(qty, slot at FIFO\_DATE\_INDEX, value)).
  - Update qty\_to\_pop using − qty.
  - Update stock\_value using − value.
  - If not qty\_to\_pop.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return tuple(qty\_to\_pop, stock\_value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L995)

<a id="op-31ef2dbc47a86c"></a>
### FIFOSlots.adjust incoming transfer qty

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_adjust_incoming_transfer_quantity`

**Inputs** self, transfer\_data, fifo\_queue, row, batch\_nos = no value, serial\_nos = no value.

**Local steps**

- Set transfer\_qty\_to\_pop from flt(row.actual\_qty).
- Set stock\_value from flt(row.stock\_value\_difference).
- Set batch\_nos from list of list(batch\_no) for batch\_no drawn from (batch\_nos or list()).
  - Draw batch\_no from (batch\_nos or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in batch\_nos → list().
- Set serial\_nos from list((serial\_nos or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in serial\_nos → list().
- While transfer\_qty\_to\_pop.
  - If (transfer\_data and 0 &lt; flt(transfer\_data at 0 at FIFO\_QTY\_INDEX) ≤ transfer\_qty\_to\_pop).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in transfer\_data → 0 &lt; flt(transfer\_data at 0 at FIFO\_QTY\_INDEX) ≤ transfer\_qty\_to\_pop.
    - Compare adjacent operands in order, stopping at the first false comparison in 0 &lt; flt(transfer\_data at 0 at FIFO\_QTY\_INDEX) ≤ transfer\_qty\_to\_pop.
    - Set transfer\_qty from flt(transfer\_data at 0 at FIFO\_QTY\_INDEX).
    - Set transfer\_date from transfer\_data at 0 at FIFO\_DATE\_INDEX.
    - Set transfer\_value from flt(transfer\_data at 0 at FIFO\_VALUE\_INDEX).
    - Update transfer\_qty\_to\_pop using − transfer\_qty.
    - Update stock\_value using − transfer\_value.
    - Evaluate self.\_add\_incoming\_transfer\_slots(fifo\_queue, row.warehouse, batch\_nos, transfer\_qty, …).
    - Evaluate transfer\_data.pop(0).
  - Otherwise.
    - If not transfer\_data.
      - Evaluate self.\_add\_incoming\_transfer\_slots(fifo\_queue, row.warehouse, batch\_nos, transfer\_qty\_to\_pop, …).
      - Set transfer\_qty\_to\_pop from 0.
      - Set stock\_value from 0.
    - Otherwise.
      - Update transfer\_data at 0 at FIFO\_QTY\_INDEX using − transfer\_qty\_to\_pop.
      - Update transfer\_data at 0 at FIFO\_VALUE\_INDEX using − stock\_value.
      - Evaluate self.\_add\_incoming\_transfer\_slots(fifo\_queue, row.warehouse, batch\_nos, transfer\_qty\_to\_pop, …).
      - Set transfer\_qty\_to\_pop from 0.
      - Set stock\_value from 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [add incoming transfer slots](operations-069.md#op-eaa4cd2fd3073c).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L704) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L316)

<a id="op-eaa4cd2fd3073c"></a>
### FIFOSlots.add incoming transfer slots

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_add_incoming_transfer_slots`

**Inputs** self, fifo\_queue, warehouse, batch\_nos, qty, posting\_date, value, serial\_nos = no value.

**Declared result** no value.

**Local steps**

- For each slot in self.\_get\_incoming\_transfer\_slots(warehouse, batch\_nos, qty, posting\_date, …).
  - Evaluate self.\_add\_transfer\_slot\_to\_fifo\_queue(fifo\_queue, slot).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get incoming transfer slots](operations-069.md#op-4bfdc9c919bd63), [add transfer slot to fifo queue](operations-069.md#op-fca8b796a74cd8).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L700) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L312)

<a id="op-4bfdc9c919bd63"></a>
### FIFOSlots.get incoming transfer slots

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_incoming_transfer_slots`

**Inputs** self, warehouse, batch\_nos, qty, posting\_date, value, serial\_nos = no value.

**Declared result** list.

**Explicit results** self.\_get\_serial\_incoming\_transfer\_slots(serial\_nos, warehouse, qty, posting\_date, …) · list(list(qty, posting\_date, value)) · incoming\_slots.

**Local steps**

- If serial\_nos.
  - Return self.\_get\_serial\_incoming\_transfer\_slots(serial\_nos, warehouse, qty, posting\_date, …).
- If not batch\_nos.
  - Return list(list(qty, posting\_date, value)).
- Set incoming\_slots from list().
- Set remaining\_qty from flt(qty).
- Set remaining\_value from flt(value).
- While (remaining\_qty and batch\_nos).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in remaining\_qty → batch\_nos.
  - Set tuple(batch\_no, use\_batchwise\_valuation, batch\_qty, \_) from batch\_nos at 0.
  - Set batch\_qty from flt(batch\_qty).
  - Set slot\_qty from min(batch\_qty, remaining\_qty).
  - Set slot\_value from remaining\_value when slot\_qty equals remaining\_qty, otherwise flt((remaining\_value × (slot\_qty ÷ remaining\_qty))).
    - Value choice on slot\_qty equals remaining\_qty — true gives remaining\_value, false gives flt((remaining\_value × (slot\_qty ÷ remaining\_qty))).
  - Evaluate incoming\_slots.append(list(batch\_no, use\_batchwise\_valuation, slot\_qty, posting\_date, …)).
  - Set batch\_nos at 0 at 2 from flt((batch\_qty − slot\_qty)).
  - If not batch\_nos at 0 at 2.
    - Evaluate batch\_nos.pop(0).
  - Set remaining\_qty from flt((remaining\_qty − slot\_qty)).
  - Set remaining\_value from flt((remaining\_value − slot\_value)).
- If remaining\_qty.
  - Evaluate incoming\_slots.append(list(remaining\_qty, posting\_date, remaining\_value)).
- Return incoming\_slots.

**Methods declared on this owner** [get serial incoming transfer slots](operations-069.md#op-5ff3bb07a6eefd).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L331)

<a id="op-5ff3bb07a6eefd"></a>
### FIFOSlots.get serial incoming transfer slots

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_serial_incoming_transfer_slots`

**Inputs** self, serial\_nos, warehouse, qty, posting\_date, value.

**Declared result** list.

**Explicit results** incoming\_slots.

**Local steps**

- Set incoming\_slots from list().
- Set remaining\_value from flt(value).
- Set serial\_count from min(cint(qty), len(serial\_nos)).
- For each index in range(serial\_count).
  - Set serial\_no from serial\_nos.pop(0).
  - Set serial\_value from remaining\_value when index equals (serial\_count − 1), otherwise flt((value ÷ serial\_count)).
    - Value choice on index equals (serial\_count − 1) — true gives remaining\_value, false gives flt((value ÷ serial\_count)).
  - Set serial\_posting\_date from self.serial\_no\_details.setdefault(tuple(serial\_no, warehouse), posting\_date).
  - Evaluate incoming\_slots.append(list(serial\_no, serial\_posting\_date, serial\_value)).
  - Set remaining\_value from flt((remaining\_value − serial\_value)).
- Return incoming\_slots.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L337)

<a id="op-fca8b796a74cd8"></a>
### FIFOSlots.add transfer slot to fifo queue

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_add_transfer_slot_to_first_in_first_out_queue`

**Inputs** self, fifo\_queue, slot.

**Declared result** no value.

**Local steps**

- Set matching\_negative\_batch\_slot from self.\_get\_matching\_negative\_batch\_slot(fifo\_queue, slot).
- If (fifo\_queue and is\_qty\_slot(fifo\_queue at 0) and is\_qty\_slot(slot) and flt(fifo\_queue at 0 at FIFO\_QTY\_INDEX) ≤ 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fifo\_queue → is\_qty\_slot(fifo\_queue at 0) → is\_qty\_slot(slot) → flt(fifo\_queue at 0 at FIFO\_QTY\_INDEX) ≤ 0.
  - Update fifo\_queue at 0 at FIFO\_QTY\_INDEX using + flt(slot at FIFO\_QTY\_INDEX).
  - Set fifo\_queue at 0 at FIFO\_DATE\_INDEX from slot at FIFO\_DATE\_INDEX.
  - Update fifo\_queue at 0 at FIFO\_VALUE\_INDEX using + flt(slot at FIFO\_VALUE\_INDEX).
- Otherwise.
  - If matching\_negative\_batch\_slot.
    - Update matching\_negative\_batch\_slot at BATCH\_SLOT\_QTY\_INDEX using + flt(slot at BATCH\_SLOT\_QTY\_INDEX).
    - Set matching\_negative\_batch\_slot at BATCH\_SLOT\_DATE\_INDEX from slot at BATCH\_SLOT\_DATE\_INDEX.
    - Update matching\_negative\_batch\_slot at BATCH\_SLOT\_VALUE\_INDEX using + flt(slot at BATCH\_SLOT\_VALUE\_INDEX).
    - If self.\_is\_empty\_batch\_slot(matching\_negative\_batch\_slot).
      - Evaluate fifo\_queue.remove(matching\_negative\_batch\_slot).
  - Otherwise.
    - Evaluate fifo\_queue.append(slot).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get matching negative batch slot](operations-069.md#op-e584c6f0991af3), [is empty batch slot](operations-069.md#op-4d44507a1959ad).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0906.json#L412) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L703) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L315)

<a id="op-4d44507a1959ad"></a>
### FIFOSlots.is empty batch slot

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_is_empty_batch_slot`

**Inputs** self, slot.

**Declared result** bool.

**Explicit results** (not flt(slot at BATCH\_SLOT\_QTY\_INDEX) and round\_off\_if\_near\_zero(slot at BATCH\_SLOT\_VALUE\_INDEX, 2) equals 0).

**Local steps**

- Return (not flt(slot at BATCH\_SLOT\_QTY\_INDEX) and round\_off\_if\_near\_zero(slot at BATCH\_SLOT\_VALUE\_INDEX, 2) equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(slot at BATCH\_SLOT\_QTY\_INDEX) → round\_off\_if\_near\_zero(slot at BATCH\_SLOT\_VALUE\_INDEX, 2) equals 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0906.json#L912) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L730) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L342)

<a id="op-e584c6f0991af3"></a>
### FIFOSlots.get matching negative batch slot

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_matching_negative_batch_slot`

**Inputs** self, fifo\_queue, slot.

**Declared result** (list bitwise or no value).

**Explicit results** no value · next(generator of existing\_slot for existing\_slot drawn from fifo\_queue where self.\_is\_matching\_negative\_batch\_slot(existing\_slot, slot at BATCH\_SLOT\_BATCH\_INDEX, slot at BATCH\_SLOT\_VALUATION\_INDEX, includ ….

**Local steps**

- If not is\_batch\_slot(slot).
  - Return no value.
- Return next(generator of existing\_slot for existing\_slot drawn from fifo\_queue where self.\_is\_matching\_negative\_batch\_slot(existing\_slot, slot at BATCH\_SLOT\_BATCH\_INDEX, slot at BATCH\_SLOT\_VALUATION\_INDEX, includ ….
  - Draw existing\_slot from fifo\_queue, keep a combination only if (self.\_is\_matching\_negative\_batch\_slot(existing\_slot, slot at BATCH\_SLOT\_BATCH\_INDEX, slot at BATCH\_SLOT\_VALUATION\_INDEX, include\_zero\_qty = true)).

**Methods declared on this owner** [is matching negative batch slot](operations-068.md#op-856b8d9eca7843).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0906.json#L1035) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L334)

<a id="op-c509973ef1cb20"></a>
### FIFOSlots.update balances

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_update_balances`

**Inputs** self, row, key.

**Local steps**

- Set self.item\_details at key at “qty\_after\_transaction” from row.qty\_after\_transaction.
- If “total\_qty” does not belong to self.item\_details at key.
  - Set self.item\_details at key at “total\_qty” from row.actual\_qty.
- Otherwise.
  - Update self.item\_details at key at “total\_qty” using + row.actual\_qty.
- Set self.item\_details at key at “has\_serial\_no” from row.has\_serial\_no.
- Set self.item\_details at key at “has\_batch\_no” from row.has\_batch\_no.
- Set self.item\_details at key at “details”.valuation\_rate from row.valuation\_rate.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0906.json#L1231) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L744) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L356)

<a id="op-85433f27ff501c"></a>
### FIFOSlots.aggregate details by item

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_aggregate_details_by_item`

**Inputs** self, wh\_wise\_data.

**Declared result** dict.

**Explicit results** item\_aggregated\_data.

**Local steps**

- Set item\_aggregated\_data from mapping().
- For each tuple(key, row) in wh\_wise\_data.items().
  - Set item from key at 0.
  - If not item\_aggregated\_data.get(item).
    - Evaluate item\_aggregated\_data.setdefault(item, mapping(“details” → Platform.\_dict(), “fifo\_queue” → list(), “qty\_after\_transaction” → 0.0, “total\_qty” → 0.0)).
  - Set item\_row from item\_aggregated\_data.get(item).
  - Evaluate item\_row at “details”.update(row at “details”).
  - Evaluate item\_row at “fifo\_queue”.extend(row at “fifo\_queue”).
  - Update item\_row at “qty\_after\_transaction” using + flt(row at “qty\_after\_transaction”).
  - Update item\_row at “total\_qty” using + flt(row at “total\_qty”).
  - Set item\_row at “has\_serial\_no” from row at “has\_serial\_no”.
  - Set item\_row at “has\_batch\_no” from row at “has\_batch\_no”.
- Return item\_aggregated\_data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0906.json#L1577) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L705) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L317)

<a id="op-d390a2cc7c451a"></a>
### FIFOSlots.get stock ledger entries

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_stock_ledger_entries`

**Inputs** self.

**Declared result** Iterator at dict.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** sle\_query.run(as\_dict = true, as\_iterator = true).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set item from self.\_get\_item\_query().
- Set to\_date from get\_datetime((self.filters.get(“to\_date”) + “ 23:59:59.999999”)).
- Set sle\_query from nested operand in the contract(nested operand in the contract).from\_(item).select(item.name, item.item\_name, item.item\_group, item.brand, …).where((((sle.item\_code equals item.name bitwise and sle.company  ….
- If warehouses bound to get\_allowed\_docs\_for\_doctype(get\_user\_permissions().get(“Warehouse”, list()), “Item”).
  - Set sle\_query from sle\_query.where(sle.warehouse.isin(warehouses)).
- If companies bound to get\_allowed\_docs\_for\_doctype(get\_user\_permissions().get(“Company”, list()), “Stock Ledger Entry”).
  - Set sle\_query from sle\_query.where(sle.company.isin(companies)).
- If self.filters.get(“warehouse”).
  - Set sle\_query from self.\_get\_warehouse\_conditions(sle, sle\_query).
- Otherwise.
  - If self.filters.get(“warehouse\_type”).
    - Set warehouses from Platform.get\_all(“Warehouse”, filters = mapping(“warehouse\_type” → self.filters.get(“warehouse\_type”), “is\_group” → 0), pluck = “name”).
    - If warehouses.
      - Set sle\_query from sle\_query.where(sle.warehouse.isin(warehouses)).
- Set sle\_query from sle\_query.orderby(sle.posting\_datetime, sle.creation).
- Return sle\_query.run(as\_dict = true, as\_iterator = true).

**Methods declared on this owner** [get item query](operations-069.md#op-fa74dd5506c417), [get warehouse conditions](operations-069.md#op-17fe6e8cf58f9e).

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L338)

<a id="op-3219a38cc74028"></a>
### FIFOSlots.get bundle wise serial nos

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_bundle_wise_serial_numbers`

**Inputs** self.

**Declared result** dict.

**Explicit results** bundle\_wise\_serial\_nos.

**Local steps**

- Set bundle from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set to\_date from get\_datetime((self.filters.get(“to\_date”) + “ 23:59:59.999999”)).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(bundle.name, entry.serial\_no).where((((bundle.docs ….
- Set query from self.\_apply\_filter(query, bundle, “item\_code”).
- If self.filters.get(“warehouse”).
  - Set query from self.\_get\_warehouse\_conditions(bundle, query).
- Set bundle\_wise\_serial\_nos from Platform.\_dict(mapping()).
- For each tuple(bundle\_name, serial\_no) in query.run().
  - Evaluate bundle\_wise\_serial\_nos.setdefault(bundle\_name, list()).append(serial\_no).
- Return bundle\_wise\_serial\_nos.

**Methods declared on this owner** [apply filter](operations-069.md#op-56ded164a52d4e), [get warehouse conditions](operations-069.md#op-17fe6e8cf58f9e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L718) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L330)

<a id="op-fd55c8f9ac4df0"></a>
### FIFOSlots.get bundle wise batch nos

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_bundle_wise_batch_numbers`

**Inputs** self, sabb\_name = no value.

**Declared result** dict.

**Explicit results** bundle\_wise\_batch\_nos.

**Local steps**

- Set bundle from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set batch from Platform.qb.DocType(“Batch”).
- Set to\_date from get\_datetime((self.filters.get(“to\_date”) + “ 23:59:59.999999”)).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.batch\_no equals nested operand in the contract.name).select(bundle.name, entry.batch\_no, batch.use\_batchwise ….
- Set query from self.\_apply\_filter(query, bundle, “item\_code”).
- If self.filters.get(“warehouse”).
  - Set query from self.\_get\_warehouse\_conditions(bundle, query).
- If sabb\_name.
  - Set query from query.where(bundle.name equals sabb\_name).
- Set bundle\_wise\_batch\_nos from Platform.\_dict(mapping()).
- For each tuple(bundle\_name, batch\_no, use\_batchwise\_valuation, qty, …) in query.run().
  - Evaluate bundle\_wise\_batch\_nos.setdefault(bundle\_name, list()).append(list(batch\_no.upper(), use\_batchwise\_valuation, qty, stock\_value\_difference)).
- Return bundle\_wise\_batch\_nos.

**Methods declared on this owner** [apply filter](operations-069.md#op-56ded164a52d4e), [get warehouse conditions](operations-069.md#op-17fe6e8cf58f9e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L328)

<a id="op-fa74dd5506c417"></a>
### FIFOSlots.get item query

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_item_query`

**Inputs** self.

**Declared result** str.

**Explicit results** item.

**Local steps**

- Set item\_table from Platform.qb.DocType(“Item”).
- Set item from Platform.qb.from\_(“Item”).select(“name”, “item\_name”, “description”, “stock\_uom”, …).
- Set item from self.\_apply\_filter(item, item\_table, “item\_code”).
- If self.filters.get(“brand”).
  - Set item from item.where(item\_table.brand equals self.filters.get(“brand”)).
- Return item.

**Methods declared on this owner** [apply filter](operations-069.md#op-56ded164a52d4e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0906.json#L4600) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L332)

<a id="op-56ded164a52d4e"></a>
### FIFOSlots.apply filter

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_apply_filter`

**Inputs** self, query, table, fieldname.

**Explicit results** query · query.where(table at fieldname.isin(filter\_value)) · query.where(table at fieldname equals filter\_value).

**Local steps**

- Set filter\_value from self.filters.get(fieldname).
- If not filter\_value.
  - Return query.
- If isinstance(filter\_value, ((list bitwise or tuple) bitwise or set)).
  - Return query.where(table at fieldname.isin(filter\_value)).
- Return query.where(table at fieldname equals filter\_value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0906.json#L4949) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L707) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L319)

<a id="op-17fe6e8cf58f9e"></a>
### FIFOSlots.get warehouse conditions

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_warehouse_conditions`

**Inputs** self, sle, sle\_query.

**Declared result** str.

**Explicit results** apply\_warehouse\_filter(sle\_query, sle, self.filters).

**Local steps**

- Return apply\_warehouse\_filter(sle\_query, sle, self.filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0906.json#L5189) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L339)
