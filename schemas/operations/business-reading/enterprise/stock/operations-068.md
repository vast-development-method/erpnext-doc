# Inventory and warehouses · operations 68

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Stock ageing

<a id="op-90d344ed4a05c0"></a>
### FIFOSlots.generate

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_generate`

**Inputs** self.

**Declared result** dict.

**Explicit results** self.item\_details.

**Local steps**

- Set stock\_ledger\_entries from self.sle.
- Set tuple(bundle\_wise\_serial\_nos, bundle\_wise\_batch\_nos) from self.\_get\_bundle\_wise\_details(stock\_ledger\_entries).
- Set adjustment\_netting from AdjustmentNetting(by\_lot = true).
- Evaluate self.prepare\_stock\_reco\_voucher\_wise\_count().
- Set self.subcontracting\_returns from self.\_get\_subcontracting\_returns().
- Set self.float\_precision from get\_float\_precision().
- If stock\_ledger\_entries is identical to no value.
  - Evaluate self.\_prefetch\_batchwise\_valuations().
  - Evaluate self.\_prefetch\_valuation\_methods().
- Within Platform.db.unbuffered\_cursor().
  - If stock\_ledger\_entries is identical to no value.
    - Set stock\_ledger\_entries from self.\_get\_stock\_ledger\_entries().
  - For each row in adjustment\_netting.net\_by\_lot(stock\_ledger\_entries, item\_field = “name”).
    - Evaluate self.\_process\_stock\_ledger\_entry(row, bundle\_wise\_serial\_nos, bundle\_wise\_batch\_nos).
  - Remove stock\_ledger\_entries.
- Evaluate self.\_recompute\_moving\_average\_slots().
- Evaluate self.\_rebalance\_batch\_slots().
- If not self.filters.get(“show\_warehouse\_wise\_stock”).
  - Set self.item\_details from self.\_aggregate\_details\_by\_item(self.item\_details).
- Return self.item\_details.

**Methods declared on this owner** [get bundle wise details](operations-068.md#op-fc0dec6b484189), [prepare stock reco voucher wise count](operations-070.md#op-842c2eb7c2622d), [get subcontracting returns](operations-069.md#op-59afe99f4fbaf1), [prefetch batchwise valuations](operations-068.md#op-ae665a6f8e8d19), [prefetch valuation methods](operations-068.md#op-7c8ffba3b5c664), [get stock ledger entries](operations-069.md#op-d390a2cc7c451a), [process stock ledger entry](operations-068.md#op-2c0c40fda23b4f), [recompute moving average slots](operations-068.md#op-b8a6c02e05727d), [rebalance batch slots](operations-068.md#op-c57026c7effdea), [aggregate details by item](operations-069.md#op-85433f27ff501c).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L714) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L326)

<a id="op-b8a6c02e05727d"></a>
### FIFOSlots.recompute moving average slots

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_recompute_moving_average_slots`

**Inputs** self.

**Declared result** no value.

**Local steps**

- For each item\_dict in self.item\_details.values().
  - If (item\_dict.get(“has\_serial\_no”) or item\_dict.get(“has\_batch\_no”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_dict.get(“has\_serial\_no”) → item\_dict.get(“has\_batch\_no”).
    - Continue with the next iteration or loop test.
  - Set details from item\_dict at “details”.
  - If self.\_get\_item\_valuation\_method(details.name) differs from “Moving Average”.
    - Continue with the next iteration or loop test.
  - Set rate from flt(details.valuation\_rate).
  - For each slot in item\_dict at “fifo\_queue”.
    - If is\_qty\_slot(slot).
      - Set slot at FIFO\_VALUE\_INDEX from flt((slot at FIFO\_QTY\_INDEX × rate)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item valuation method](operations-068.md#op-9ca65151d0c0e3).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L4313) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L739) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L351)

<a id="op-c57026c7effdea"></a>
### FIFOSlots.rebalance batch slots

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_rebalance_batch_slots`

**Inputs** self.

**Declared result** no value.

**Local steps**

- For each item\_dict in self.item\_details.values().
  - If item\_dict.get(“has\_batch\_no”).
    - Evaluate self.\_rebalance\_batch\_slot\_values(item\_dict at “fifo\_queue”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [rebalance batch slot values](operations-068.md#op-162e881676f7dd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L4639) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L738) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L350)

<a id="op-162e881676f7dd"></a>
### FIFOSlots.rebalance batch slot values

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_rebalance_batch_slot_values`

**Inputs** self, fifo\_queue.

**Declared result** no value.

**Local steps**

- Set groups from mapping().
- For each slot in fifo\_queue.
  - If is\_batch\_slot(slot).
    - Set key from slot at BATCH\_SLOT\_BATCH\_INDEX when slot at BATCH\_SLOT\_VALUATION\_INDEX, otherwise no value.
      - Value choice on slot at BATCH\_SLOT\_VALUATION\_INDEX — true gives slot at BATCH\_SLOT\_BATCH\_INDEX, false gives no value.
    - Evaluate groups.setdefault(key, list()).append(slot).
- For each slots in groups.values().
  - Set total\_qty from sum(generator of flt(slot at BATCH\_SLOT\_QTY\_INDEX) for slot drawn from slots).
    - Draw slot from slots.
  - <a id="op-162e881676f7dd-guard-12"></a>If total\_qty ≤ 0.
    - Continue with the next iteration or loop test.
  - Set rate from (sum(generator of flt(slot at BATCH\_SLOT\_VALUE\_INDEX) for slot drawn from slots) ÷ total\_qty).
    - Draw slot from slots.
  - For each slot in slots.
    - Set slot at BATCH\_SLOT\_VALUE\_INDEX from flt((slot at BATCH\_SLOT\_QTY\_INDEX × rate)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison total\_qty ≤ 0, total\_qty = 0 selects the branch that continues with the next loop iteration. With total\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-162e881676f7dd-guard-12)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L4769) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L737) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L349)

<a id="op-fc0dec6b484189"></a>
### FIFOSlots.get bundle wise details

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_bundle_wise_details`

**Inputs** self, stock\_ledger\_entries.

**Declared result** tuple at tuple(dict, dict).

**Explicit results** tuple(Platform.\_dict(mapping()), Platform.\_dict(mapping())) · tuple(self.\_get\_bundle\_wise\_serial\_nos(), self.\_get\_bundle\_wise\_batch\_nos()).

**Local steps**

- If stock\_ledger\_entries is distinct from no value.
  - Return tuple(Platform.\_dict(mapping()), Platform.\_dict(mapping())).
- Return tuple(self.\_get\_bundle\_wise\_serial\_nos(), self.\_get\_bundle\_wise\_batch\_nos()).

**Methods declared on this owner** [get bundle wise serial nos](operations-069.md#op-3219a38cc74028), [get bundle wise batch nos](operations-069.md#op-fd55c8f9ac4df0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L5187) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L329)

<a id="op-2c0c40fda23b4f"></a>
### FIFOSlots.process stock ledger entry

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_process_stock_ledger_entry`

**Inputs** self, row, bundle\_wise\_serial\_nos, bundle\_wise\_batch\_nos.

**Declared result** no value.

**Local steps**

- Set tuple(key, fifo\_queue, transferred\_item\_key) from self.\_init\_key\_stores(row).
- Set prev\_balance\_qty from self.item\_details at key.get(“qty\_after\_transaction”, 0).
- Evaluate self.\_set\_stock\_reconciliation\_actual\_qty(row, key, fifo\_queue, prev\_balance\_qty).
- Set tuple(serial\_nos, batch\_nos) from self.\_get\_serial\_and\_batch\_nos(row, bundle\_wise\_serial\_nos, bundle\_wise\_batch\_nos).
- If row.actual\_qty &gt; 0.
  - Evaluate self.\_compute\_incoming\_stock(row, fifo\_queue, transferred\_item\_key, serial\_nos, …).
- Otherwise.
  - Set from\_end from self.\_get\_item\_valuation\_method(row.name) equals “LIFO”.
  - Evaluate self.\_compute\_outgoing\_stock(row, fifo\_queue, transferred\_item\_key, serial\_nos, …).
- Evaluate self.\_revalue\_stock\_reconciliation\_slots(row, fifo\_queue, batch\_nos).
- Evaluate self.\_update\_balances(row, key).
- Evaluate self.\_trim\_serial\_fifo\_queue(row, key, fifo\_queue).

If control reaches the end, it returns no value.

**Methods declared on this owner** [init key stores](operations-068.md#op-8308b780d3030a), [set stock reconciliation actual qty](operations-068.md#op-9e99ed69977714), [get serial and batch nos](operations-068.md#op-487504b54bc2dd), [compute incoming stock](operations-068.md#op-162c219885a17e), [get item valuation method](operations-068.md#op-9ca65151d0c0e3), [compute outgoing stock](operations-069.md#op-a32aed9474c22a), [revalue stock reconciliation slots](operations-068.md#op-49a75ad69ec2c6), [update balances](operations-069.md#op-c509973ef1cb20), [trim serial fifo queue](operations-068.md#op-4259eeb5d49530).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L5366) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L736) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L348)

<a id="op-9e99ed69977714"></a>
### FIFOSlots.set stock reconciliation actual qty

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_set_stock_reconciliation_actual_quantity`

**Inputs** self, row, key, fifo\_queue, prev\_balance\_qty.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If (row.voucher\_type differs from “Stock Reconciliation” or row.get(“is\_adjustment\_entry”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.voucher\_type differs from “Stock Reconciliation” → row.get(“is\_adjustment\_entry”).
  - Return no value.
- If (row.has\_serial\_no and (not row.batch\_no or row.serial\_no or row.serial\_and\_batch\_bundle)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.has\_serial\_no → (not row.batch\_no or row.serial\_no or row.serial\_and\_batch\_bundle).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.batch\_no → row.serial\_no → row.serial\_and\_batch\_bundle.
  - If row.voucher\_detail\_no belongs to self.stock\_reco\_voucher\_wise\_count.
    - Set row.stock\_value\_difference from flt((row.qty\_after\_transaction × row.valuation\_rate)).
    - Set row.actual\_qty from row.qty\_after\_transaction.
    - Set self.item\_details at key at “qty\_after\_transaction” from 0.
    - Set self.item\_details at key at “total\_qty” from 0.
    - Evaluate fifo\_queue.clear().
    - Return no value.
- Set row.actual\_qty from (flt(row.qty\_after\_transaction) − flt(prev\_balance\_qty)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L354)

<a id="op-49a75ad69ec2c6"></a>
### FIFOSlots.revalue stock reconciliation slots

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_revalue_stock_reconciliation_slots`

**Inputs** self, row, fifo\_queue, batch\_nos.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If (row.voucher\_type differs from “Stock Reconciliation” or row.has\_serial\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.voucher\_type differs from “Stock Reconciliation” → row.has\_serial\_no.
  - Return no value.
- If row.has\_batch\_no.
  - If row.get(“is\_adjustment\_entry”).
    - Return no value.
  - If flt(row.actual\_qty) &gt; 0.
    - Evaluate self.\_revalue\_reconciled\_batch\_slots(fifo\_queue, batch\_nos).
  - Return no value.
- For each slot in fifo\_queue.
  - If is\_qty\_slot(slot).
    - Set slot at FIFO\_VALUE\_INDEX from flt((slot at FIFO\_QTY\_INDEX × flt(row.valuation\_rate))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [revalue reconciled batch slots](operations-068.md#op-15e0036bb62233).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L353)

<a id="op-15e0036bb62233"></a>
### FIFOSlots.revalue reconciled batch slots

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_revalue_reconciled_batch_slots`

**Inputs** self, fifo\_queue, batch\_nos.

**Declared result** no value.

**Local steps**

- For each tuple(batch\_no, \_use\_batchwise\_valuation, qty, stock\_value\_difference) in batch\_nos.
  - If not flt(qty).
    - Continue with the next iteration or loop test.
  - Set slots from list of slot for slot drawn from fifo\_queue where (is\_batch\_slot(slot) and slot at BATCH\_SLOT\_BATCH\_INDEX equals batch\_no).
    - Draw slot from fifo\_queue, keep a combination only if ((is\_batch\_slot(slot) and slot at BATCH\_SLOT\_BATCH\_INDEX equals batch\_no)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_batch\_slot(slot) → slot at BATCH\_SLOT\_BATCH\_INDEX equals batch\_no.
  - If flt((sum(generator of flt(slot at BATCH\_SLOT\_QTY\_INDEX) for slot drawn from slots) − flt(qty)), self.float\_precision).
    - Draw slot from slots.
    - Continue with the next iteration or loop test.
  - Set rate from (flt(stock\_value\_difference) ÷ flt(qty)).
  - For each slot in slots.
    - Set slot at BATCH\_SLOT\_VALUE\_INDEX from flt((slot at BATCH\_SLOT\_QTY\_INDEX × rate)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L6588) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L740) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L352)

<a id="op-487504b54bc2dd"></a>
### FIFOSlots.get serial and batch nos

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_serial_and_batch_numbers`

**Inputs** self, row, bundle\_wise\_serial\_nos, bundle\_wise\_batch\_nos.

**Declared result** tuple at tuple(list, list).

**Explicit results** tuple(self.uppercase\_serial\_nos(serial\_nos), batch\_nos).

**Local steps**

- Bind dependencies get\_serial\_nos\_from\_bundle.
- Set serial\_nos from get\_serial\_nos(row.serial\_no) when row.serial\_no, otherwise list().
  - Value choice on row.serial\_no — true gives get\_serial\_nos(row.serial\_no), false gives list().
- Set batch\_nos from self.\_get\_row\_batch\_nos(row).
- If row.serial\_and\_batch\_bundle.
  - If row.has\_serial\_no.
    - If bundle\_wise\_serial\_nos.
      - Set serial\_nos from (bundle\_wise\_serial\_nos.get(row.serial\_and\_batch\_bundle) or list()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in bundle\_wise\_serial\_nos.get(row.serial\_and\_batch\_bundle) → list().
    - Otherwise.
      - Set serial\_nos from (sorted(get\_serial\_nos\_from\_bundle(row.serial\_and\_batch\_bundle)) or list()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in sorted(get\_serial\_nos\_from\_bundle(row.serial\_and\_batch\_bundle)) → list().
  - Otherwise.
    - If row.has\_batch\_no.
      - If bundle\_wise\_batch\_nos.
        - Set batch\_nos from (bundle\_wise\_batch\_nos.get(row.serial\_and\_batch\_bundle) or list()).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in bundle\_wise\_batch\_nos.get(row.serial\_and\_batch\_bundle) → list().
      - Otherwise.
        - Set batch\_nos from (self.\_get\_bundle\_wise\_batch\_nos(row.serial\_and\_batch\_bundle).get(row.serial\_and\_batch\_bundle) or list()).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_get\_bundle\_wise\_batch\_nos(row.serial\_and\_batch\_bundle).get(row.serial\_and\_batch\_bundle) → list().
- Return tuple(self.uppercase\_serial\_nos(serial\_nos), batch\_nos).

**Methods declared on this owner** [get row batch nos](operations-068.md#op-64c1fb7bd93a20), [get bundle wise batch nos](operations-069.md#op-fd55c8f9ac4df0), [uppercase serial nos](operations-068.md#op-e5e510e6ef6130).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L6989) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L336)

<a id="op-64c1fb7bd93a20"></a>
### FIFOSlots.get row batch nos

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_row_batch_numbers`

**Inputs** self, row.

**Declared result** list.

**Explicit results** list() · list(list(row.batch\_no.upper(), self.\_get\_batchwise\_valuation(row.batch\_no), abs(row.actual\_qty), abs(row.stock\_value\_difference))).

**Local steps**

- If not row.batch\_no.
  - Return list().
- Return list(list(row.batch\_no.upper(), self.\_get\_batchwise\_valuation(row.batch\_no), abs(row.actual\_qty), abs(row.stock\_value\_difference))).

**Methods declared on this owner** [get batchwise valuation](operations-068.md#op-f9bcfeac8dc05f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L335)

<a id="op-4259eeb5d49530"></a>
### FIFOSlots.trim serial fifo queue

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_trim_serial_first_in_first_out_queue`

**Inputs** self, row, key, fifo\_queue.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not row.has\_serial\_no.
  - Return no value.
- Set qty\_after from cint(self.item\_details at key at “qty\_after\_transaction”).
- If qty\_after ≤ 0.
  - Evaluate fifo\_queue.clear().
- Otherwise.
  - If len(fifo\_queue) &gt; qty\_after.
    - Set fifo\_queue at slice no value to no value from fifo\_queue at slice no value to qty\_after.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L743) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L355)

<a id="op-e5e510e6ef6130"></a>
### FIFOSlots.uppercase serial nos

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_uppercase_serial_numbers`

**Inputs** self, serial\_nos.

**Explicit results** list of sn.upper() for sn drawn from serial\_nos.

**Local steps**

- Return list of sn.upper() for sn drawn from serial\_nos.
  - Draw sn from serial\_nos.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L435) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L745) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L357)

<a id="op-f9bcfeac8dc05f"></a>
### FIFOSlots.get batchwise valuation

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_batchwise_valuation`

**Inputs** self, batch\_no.

**Record and data access** read “Batch” via get\_value.

**Explicit results** self.batchwise\_valuation\_by\_batch at batch\_no.

**Local steps**

- If batch\_no does not belong to self.batchwise\_valuation\_by\_batch.
  - Set self.batchwise\_valuation\_by\_batch at batch\_no from Platform.db.get\_value(“Batch”, batch\_no, “use\_batchwise\_valuation”).
- Return self.batchwise\_valuation\_by\_batch at batch\_no.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L509) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L715) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L327)

<a id="op-ae665a6f8e8d19"></a>
### FIFOSlots.prefetch batchwise valuations

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_prefetch_batchwise_valuations`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set batch from Platform.qb.DocType(“Batch”).
- Set to\_date from get\_datetime((self.filters.get(“to\_date”) + “ 23:59:59.999999”)).
- Set query from nested operand in the contract(nested operand in the contract).select(sle.batch\_no, batch.use\_batchwise\_valuation).distinct().where((((nested operand in the contract.batch\_no.isnotnull() bitwise and sle.co ….
- Set query from self.\_apply\_filter(query, sle, “item\_code”).
- For each tuple(batch\_no, use\_batchwise\_valuation) in query.run().
  - Set self.batchwise\_valuation\_by\_batch at batch\_no from use\_batchwise\_valuation.

If control reaches the end, it returns no value.

**Methods declared on this owner** [apply filter](operations-069.md#op-56ded164a52d4e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L733) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L345)

<a id="op-9ca65151d0c0e3"></a>
### FIFOSlots.get item valuation method

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_get_item_valuation_method`

**Inputs** self, item\_code.

**Declared result** str.

**Explicit results** self.valuation\_method\_by\_item at item\_code.

**Local steps**

- Bind dependencies get\_valuation\_method.
- If item\_code does not belong to self.valuation\_method\_by\_item.
  - Set self.valuation\_method\_by\_item at item\_code from get\_valuation\_method(item\_code, self.filters.get(“company”)).
- Return self.valuation\_method\_by\_item at item\_code.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L1181) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L333)

<a id="op-7c8ffba3b5c664"></a>
### FIFOSlots.prefetch valuation methods

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_prefetch_valuation_methods`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Bind dependencies get\_valuation\_method.
- Set company from self.filters.get(“company”).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set item from Platform.qb.DocType(“Item”).
- Set to\_date from get\_datetime((self.filters.get(“to\_date”) + “ 23:59:59.999999”)).
- Set query from nested operand in the contract(nested operand in the contract).select(item.name, item.valuation\_method).distinct().where(((sle.company equals company bitwise and sle.posting\_datetime ≤ to\_date) bitwise and ….
- Set query from self.\_apply\_filter(query, sle, “item\_code”).
- Set default\_method from no value.
- For each tuple(item\_code, valuation\_method) in query.run().
  - If not valuation\_method.
    - If default\_method is identical to no value.
      - Set default\_method from get\_valuation\_method(item\_code, company).
    - Set valuation\_method from default\_method.
  - Set self.valuation\_method\_by\_item at item\_code from valuation\_method.

If control reaches the end, it returns no value.

**Methods declared on this owner** [apply filter](operations-069.md#op-56ded164a52d4e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L734) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L346)

<a id="op-8308b780d3030a"></a>
### FIFOSlots.init key stores

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_initialize_key_stores`

**Inputs** self, row.

**Declared result** tuple.

**Explicit results** tuple(key, fifo\_queue, transferred\_item\_key).

**Local steps**

- Set key from tuple(row.name, row.warehouse).
- Evaluate self.item\_details.setdefault(key, mapping(“details” → row, “fifo\_queue” → list())).
- Set fifo\_queue from self.item\_details at key at “fifo\_queue”.
- Set transferred\_item\_key from tuple(row.voucher\_no, row.name, row.warehouse).
- Evaluate self.transferred\_item\_details.setdefault(transferred\_item\_key, list()).
- Return tuple(key, fifo\_queue, transferred\_item\_key).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L1959) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L341)

<a id="op-162c219885a17e"></a>
### FIFOSlots.compute incoming stock

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_compute_incoming_stock`

**Inputs** self, row, fifo\_queue, transfer\_key, serial\_nos, batch\_nos.

**Local steps**

- Set transfer\_data from self.transferred\_item\_details.get(transfer\_key).
- If transfer\_data.
  - Evaluate self.\_adjust\_incoming\_transfer\_qty(transfer\_data, fifo\_queue, row, batch\_nos, serial\_nos = serial\_nos when row.get(“has\_serial\_no”), otherwise no value).
    - Value choice on row.get(“has\_serial\_no”) — true gives serial\_nos, false gives no value.
- Otherwise.
  - If (serial\_nos and row.get(“has\_serial\_no”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in serial\_nos → row.get(“has\_serial\_no”).
    - Evaluate self.\_add\_serial\_fifo\_slots(row, fifo\_queue, serial\_nos).
  - Otherwise.
    - If (batch\_nos and row.get(“has\_batch\_no”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_nos → row.get(“has\_batch\_no”).
      - Evaluate self.\_add\_batch\_fifo\_slots(row, fifo\_queue, batch\_nos).
    - Otherwise.
      - If (fifo\_queue and is\_qty\_slot(fifo\_queue at 0) and flt(fifo\_queue at 0 at FIFO\_QTY\_INDEX) ≤ 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in fifo\_queue → is\_qty\_slot(fifo\_queue at 0) → flt(fifo\_queue at 0 at FIFO\_QTY\_INDEX) ≤ 0.
        - Evaluate self.\_add\_to\_negative\_fifo\_head(row, fifo\_queue).
      - Otherwise.
        - Evaluate fifo\_queue.append(list(flt(row.actual\_qty), row.posting\_date, flt(row.stock\_value\_difference))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [adjust incoming transfer qty](operations-069.md#op-31ef2dbc47a86c), [add serial fifo slots](operations-068.md#op-5ab12e6cd42269), [add batch fifo slots](operations-068.md#op-cfd76e40aad8b6), [add to negative fifo head](operations-068.md#op-845d6f42a4f22e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L2227) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L709) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L321)

<a id="op-5ab12e6cd42269"></a>
### FIFOSlots.add serial fifo slots

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_add_serial_first_in_first_out_slots`

**Inputs** self, row, fifo\_queue, serial\_nos.

**Declared result** no value.

**Local steps**

- Set valuation from (row.stock\_value\_difference ÷ row.actual\_qty).
- For each serial\_no in serial\_nos.
  - Set posting\_date from self.serial\_no\_details.setdefault(tuple(serial\_no, row.warehouse), row.posting\_date).
  - Evaluate fifo\_queue.append(list(serial\_no, posting\_date, valuation)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L701) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L313)

<a id="op-cfd76e40aad8b6"></a>
### FIFOSlots.add batch fifo slots

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_add_batch_first_in_first_out_slots`

**Inputs** self, row, fifo\_queue, batch\_nos.

**Declared result** no value.

**Local steps**

- For each tuple(batch\_no, use\_batchwise\_valuation, qty, stock\_value\_difference) in batch\_nos.
  - Set tuple(qty, stock\_value\_difference) from self.\_neutralize\_negative\_batch\_stock(fifo\_queue, row, batch\_no, use\_batchwise\_valuation, …).
  - If not qty.
    - Continue with the next iteration or loop test.
  - Set posting\_date from self.batch\_no\_details.setdefault(tuple(batch\_no, row.warehouse), row.posting\_date).
  - Evaluate fifo\_queue.append(list(batch\_no, use\_batchwise\_valuation, qty, posting\_date, …)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [neutralize negative batch stock](operations-068.md#op-eb58d48fb29b3c).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L699) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L311)

<a id="op-eb58d48fb29b3c"></a>
### FIFOSlots.neutralize negative batch stock

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_neutralize_negative_batch_stock`

**Inputs** self, fifo\_queue, row, batch\_no, use\_batchwise\_valuation, qty, stock\_value\_difference.

**Declared result** tuple at tuple(float, float).

**Explicit results** tuple(qty, stock\_value\_difference).

**Local steps**

- Set qty from flt(qty).
- Set stock\_value\_difference from flt(stock\_value\_difference).
- If not qty.
  - Return tuple(qty, stock\_value\_difference).
- If tuple(batch\_no, row.warehouse) does not belong to self.batches\_with\_negative\_slots.
  - Return tuple(qty, stock\_value\_difference).
- Set negative\_slot\_may\_remain from false.
- For each slot in list(fifo\_queue).
  - If not self.\_is\_matching\_negative\_batch\_slot(slot, batch\_no, use\_batchwise\_valuation).
    - Continue with the next iteration or loop test.
  - Set qty\_to\_adjust from min(qty, abs(flt(slot at BATCH\_SLOT\_QTY\_INDEX))).
  - Set value\_to\_adjust from stock\_value\_difference when qty\_to\_adjust equals qty, otherwise flt((stock\_value\_difference × (qty\_to\_adjust ÷ qty))).
    - Value choice on qty\_to\_adjust equals qty — true gives stock\_value\_difference, false gives flt((stock\_value\_difference × (qty\_to\_adjust ÷ qty))).
  - Set slot at BATCH\_SLOT\_QTY\_INDEX from (flt(slot at BATCH\_SLOT\_QTY\_INDEX) + qty\_to\_adjust).
  - Set slot at BATCH\_SLOT\_DATE\_INDEX from row.posting\_date.
  - Set slot at BATCH\_SLOT\_VALUE\_INDEX from (flt(slot at BATCH\_SLOT\_VALUE\_INDEX) + value\_to\_adjust).
  - Set qty from flt((qty − qty\_to\_adjust)).
  - Set stock\_value\_difference from flt((stock\_value\_difference − value\_to\_adjust)).
  - If (not flt(slot at BATCH\_SLOT\_QTY\_INDEX) and not flt(slot at BATCH\_SLOT\_VALUE\_INDEX)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(slot at BATCH\_SLOT\_QTY\_INDEX) → not flt(slot at BATCH\_SLOT\_VALUE\_INDEX).
    - Evaluate fifo\_queue.remove(slot).
  - Otherwise.
    - If flt(slot at BATCH\_SLOT\_QTY\_INDEX) &lt; 0.
      - Set negative\_slot\_may\_remain from true.
  - If not qty.
    - Set negative\_slot\_may\_remain from true.
    - Leave the innermost loop without its normal-exhaustion alternative.
- If not negative\_slot\_may\_remain.
  - Evaluate self.batches\_with\_negative\_slots.discard(tuple(batch\_no, row.warehouse)).
- Return tuple(qty, stock\_value\_difference).

**Methods declared on this owner** [is matching negative batch slot](operations-068.md#op-856b8d9eca7843).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L732) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L344)

<a id="op-856b8d9eca7843"></a>
### FIFOSlots.is matching negative batch slot

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_is_matching_negative_batch_slot`

**Inputs** self, slot, batch\_no, use\_batchwise\_valuation, include\_zero\_qty = false.

**Declared result** bool.

**Explicit results** false · (slot at BATCH\_SLOT\_BATCH\_INDEX equals batch\_no and slot at BATCH\_SLOT\_VALUATION\_INDEX equals use\_batchwise\_valuation and qty ≤ 0 when include\_zero\_qty, otherwise qty &lt; 0).

**Local steps**

- If not is\_batch\_slot(slot).
  - Return false.
- Set qty from flt(slot at BATCH\_SLOT\_QTY\_INDEX).
- Return (slot at BATCH\_SLOT\_BATCH\_INDEX equals batch\_no and slot at BATCH\_SLOT\_VALUATION\_INDEX equals use\_batchwise\_valuation and qty ≤ 0 when include\_zero\_qty, otherwise qty &lt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in slot at BATCH\_SLOT\_BATCH\_INDEX equals batch\_no → slot at BATCH\_SLOT\_VALUATION\_INDEX equals use\_batchwise\_valuation → qty ≤ 0 when include\_zero\_qty, otherwise qty &lt; 0.
  - Value choice on include\_zero\_qty — true gives qty ≤ 0, false gives qty &lt; 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L3915) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L343)

<a id="op-845d6f42a4f22e"></a>
### FIFOSlots.add to negative fifo head

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_add_to_negative_first_in_first_out_head`

**Inputs** self, row, fifo\_queue.

**Declared result** no value.

**Local steps**

- Update fifo\_queue at 0 at FIFO\_QTY\_INDEX using + flt(row.actual\_qty).
- Set fifo\_queue at 0 at FIFO\_DATE\_INDEX from row.posting\_date.
- Update fifo\_queue at 0 at FIFO\_VALUE\_INDEX using + flt(row.stock\_value\_difference).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0905.json#L4162) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L702) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L314)
