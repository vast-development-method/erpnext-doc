# Inventory and warehouses · operations 98

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock reconciliation

[Record definition](../../../../data/record-types/stock_reconciliation.json)

<a id="op-dab8263c3915af"></a>
### Stock Reconciliation.set new bundle from current

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_set_new_bundle_from_current`

**Inputs** self, item.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** request copy\_doc for current\_doc · call save on bundle\_doc.

**Explicit failure paths** validation helper — translated “Row #{0}: select the serial and batch numbers for the new quantity of Item {1}”.format(item.idx, Platform.bold(item.item\_code)).

**Local steps**

- Set current\_doc from Platform.get\_doc(“Serial and Batch Bundle”, item.current\_serial\_and\_batch\_bundle).
- If item.qty belongs to tuple(empty text, no value).
  - Set item.qty from abs(current\_doc.total\_qty).
- Otherwise.
  - If flt(item.qty) differs from abs(current\_doc.total\_qty).
    - Call the validation error handler Platform.throw(translated “Row #{0}: select the serial and batch numbers for the new quantity of Item {1}”.format(item.idx, Platform.bold(item.item\_code))).
- Set rate\_entered from item.valuation\_rate does not belong to tuple(empty text, no value).
- If not rate\_entered.
  - Set item.valuation\_rate from abs(current\_doc.avg\_rate).
- Set bundle\_doc from Platform.copy\_doc(current\_doc).
- Set bundle\_doc.warehouse from item.warehouse.
- Set bundle\_doc.type\_of\_transaction from “Inward”.
- For each row in bundle\_doc.entries.
  - Set row.qty from abs(row.qty).
  - Set row.incoming\_rate from flt(item.valuation\_rate) when rate\_entered, otherwise abs(flt(row.incoming\_rate)).
    - Value choice on rate\_entered — true gives flt(item.valuation\_rate), false gives abs(flt(row.incoming\_rate)).
  - Set row.is\_outward from 0.
- Evaluate bundle\_doc.calculate\_qty\_and\_amount().
- Set bundle\_doc.flags.ignore\_permissions from true.
- Evaluate bundle\_doc.save().
- Set item.serial\_and\_batch\_bundle from bundle\_doc.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L803)

<a id="op-e60a0d06f5bc22"></a>
### Stock Reconciliation.set new serial and batch bundle

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_set_new_serial_and_batch_bundle`

**Inputs** self.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**Local steps**

- For each item in self.items.
  - If not item.item\_code.
    - Continue with the next iteration or loop test.
  - If item.use\_serial\_batch\_fields.
    - Continue with the next iteration or loop test.
  - If (item.current\_serial\_and\_batch\_bundle and not item.serial\_and\_batch\_bundle and item.qty differs from 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.current\_serial\_and\_batch\_bundle → not item.serial\_and\_batch\_bundle → item.qty differs from 0.
    - Evaluate self.set\_new\_bundle\_from\_current(item).
    - Continue with the next iteration or loop test.
  - If not item.qty.
    - Continue with the next iteration or loop test.
  - If (item.serial\_and\_batch\_bundle and not item.qty and not item.valuation\_rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.serial\_and\_batch\_bundle → not item.qty → not item.valuation\_rate.
    - Set bundle\_doc from Platform.get\_doc(“Serial and Batch Bundle”, item.serial\_and\_batch\_bundle).
    - Set item.qty from bundle\_doc.total\_qty.
    - Set item.valuation\_rate from bundle\_doc.avg\_rate.
  - Otherwise.
    - If (item.serial\_and\_batch\_bundle and item.qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.serial\_and\_batch\_bundle → item.qty.
      - Evaluate self.update\_existing\_serial\_and\_batch\_bundle(item).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set new bundle from current](operations-098.md#op-dab8263c3915af), [update existing serial and batch bundle](operations-098.md#op-6ccd57aca2b5db).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1060)

<a id="op-6ccd57aca2b5db"></a>
### Stock Reconciliation.update existing serial and batch bundle

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_update_existing_serial_and_batch_bundle`

**Inputs** self, item.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**State and service calls** request set\_value on “Serial and Batch Entry”.

**Explicit results** no value.

**Local steps**

- Set batch\_details from Platform.get\_all(“Serial and Batch Entry”, fields = list(“batch\_no”, “qty”, “name”), filters = mapping(“parent” → item.serial\_and\_batch\_bundle, “batch\_no” → tuple(“is”, “set”))).
- If (batch\_details and len(batch\_details) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_details → len(batch\_details) equals 1.
  - Set batch from batch\_details at 0.
  - If abs(batch.qty) equals abs(item.qty).
    - Return no value.
  - Set update\_values from mapping(“qty” → item.qty, “stock\_value\_difference” → (flt(item.valuation\_rate) × flt(item.qty))).
  - Evaluate Platform.db.set\_value(“Serial and Batch Entry”, batch.name, update\_values).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0858.json#L5519) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L143) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1064)

<a id="op-6d7d6373f5dea1"></a>
### Stock Reconciliation.remove items with no change

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_remove_items_with_number_change`

**Inputs** self.

**State and service calls** msgprint with translated “Removed items with no change in quantity or value.”.

**Explicit failure paths** validation helper with EmptyStockReconciliationItemsError — translated “None of the items have any change in quantity or value.”.

**Local steps**

- Set self.difference\_amount from 0.0.
- Bind local operation \_changed for subsequent calls.
- Set items from list(filter(deferred anonymous expression, self.items)).
- If not items.
  - Call the validation error handler Platform.throw(translated “None of the items have any change in quantity or value.”, EmptyStockReconciliationItemsError).
- Otherwise.
  - If len(items) differs from len(self.items).
    - Set self.items from items.
    - Set self.change\_idx from true.
    - Evaluate Platform.msgprint(translated “Removed items with no change in quantity or value.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1057)

<a id="op-960a4929ef8b45"></a>
### Stock Reconciliation.remove items with no change.changed

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_remove_items_with_number_change_changed`

**Inputs** item.

**Record and data access** read “Serial and Batch Bundle” via get\_all.

**Explicit results** true · false.

**Local steps**

- If item.current\_serial\_and\_batch\_bundle.
  - Set bundle\_data from Platform.get\_all(“Serial and Batch Bundle”, filters = mapping(“name” → item.current\_serial\_and\_batch\_bundle), fields = list(“total\_qty as qty”, “avg\_rate as rate”)) at 0.
  - Set bundle\_data.qty from abs(bundle\_data.qty).
  - Evaluate self.calculate\_difference\_amount(item, bundle\_data).
  - Return true.
- Set inventory\_dimensions\_dict from mapping().
- If (not item.batch\_no and not item.serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.batch\_no → not item.serial\_no.
  - For each dimension in get\_inventory\_dimensions().
    - If item.get(dimension.get(“fieldname”)).
      - Set inventory\_dimensions\_dict at dimension.get(“fieldname”) from item.get(dimension.get(“fieldname”)).
- Set item\_dict from get\_stock\_balance\_for(item.item\_code, item.warehouse, self.posting\_date, self.posting\_time, batch\_no = item.batch\_no, inventory\_dimensions\_dict = inventory\_dimensions\_dict, row = item, company = self.company).
- If (not item\_dict.get(“qty”) and not item.qty and not item.valuation\_rate and not item.current\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item\_dict.get(“qty”) → not item.qty → not item.valuation\_rate → not item.current\_qty.
  - If abs(self.get\_stranded\_stock\_value(item)) &gt; 0.
    - Return true.
- Set rate\_precision from item.precision(“valuation\_rate”).
- Set rate from flt(item\_dict.get(“rate”), rate\_precision).
- Set valuation\_rate from flt(item.valuation\_rate, rate\_precision) when item.valuation\_rate does not belong to tuple(empty text, no value), otherwise no value.
  - Value choice on item.valuation\_rate does not belong to tuple(empty text, no value) — true gives flt(item.valuation\_rate, rate\_precision), false gives no value.
- If ((item.qty is identical to no value or item.qty equals item\_dict.get(“qty”)) and (valuation\_rate is identical to no value or valuation\_rate equals rate) and (not item.serial\_no or item.serial\_no equals ite ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (item.qty is identical to no value or item.qty equals item\_dict.get(“qty”)) → (valuation\_rate is identical to no value or valuation\_rate equals rate) → (not item.serial\_no or item.serial\_no equals item\_dict.get(“serial\_nos”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.qty is identical to no value → item.qty equals item\_dict.get(“qty”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in valuation\_rate is identical to no value → valuation\_rate equals rate.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.serial\_no → item.serial\_no equals item\_dict.get(“serial\_nos”).
  - Return false.
- Otherwise.
  - If item.qty is identical to no value.
    - Set item.qty from item\_dict.get(“qty”).
  - If (item.valuation\_rate is identical to no value and (item\_dict.get(“rate”) or item\_dict.get(“qty”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.valuation\_rate is identical to no value → (item\_dict.get(“rate”) or item\_dict.get(“qty”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_dict.get(“rate”) → item\_dict.get(“qty”).
    - Set item.valuation\_rate from item\_dict.get(“rate”).
  - If item\_dict.get(“serial\_nos”).
    - Set item.current\_serial\_no from item\_dict.get(“serial\_nos”).
    - If (self.purpose equals “Stock Reconciliation” and not item.serial\_no and item.qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Stock Reconciliation” → not item.serial\_no → item.qty.
      - Set item.serial\_no from item.current\_serial\_no.
  - Set item.current\_qty from item\_dict.get(“qty”).
  - Set item.current\_valuation\_rate from item\_dict.get(“rate”).
  - Evaluate self.calculate\_difference\_amount(item, item\_dict).
  - Return true.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1058)

<a id="op-7e1be19dcdb735"></a>
### Stock Reconciliation.calculate difference amount

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_calculate_difference_amount`

**Inputs** self, item, item\_dict.

**Local steps**

- Set qty\_precision from item.precision(“qty”).
- Set amount\_precision from item.precision(“amount”).
- Set new\_qty from flt(item.qty, qty\_precision).
- Set new\_valuation\_rate from flt(item.valuation\_rate when item.valuation\_rate does not belong to tuple(empty text, no value), otherwise item\_dict.get(“rate”)).
  - Value choice on item.valuation\_rate does not belong to tuple(empty text, no value) — true gives item.valuation\_rate, false gives item\_dict.get(“rate”).
- Set current\_qty from flt(item\_dict.get(“qty”), qty\_precision).
- Set current\_valuation\_rate from flt(item\_dict.get(“rate”)).
- Set new\_amount from flt((new\_qty × new\_valuation\_rate), amount\_precision).
- Set current\_amount from flt((current\_qty × current\_valuation\_rate), amount\_precision).
- Set item.flags.difference\_valuation\_rate from new\_valuation\_rate.
- Update self.difference\_amount using + (new\_amount − current\_amount).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1039)

<a id="op-a622adf04f95a9"></a>
### Stock Reconciliation.validate data

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_validate_data`

**Inputs** self.

**Record and data access** read “Item Price” via get\_value · read “Item” via get\_value.

**Explicit failure paths** Platform.ValidationError(self.validation\_messages).

**Local steps**

- Bind local operation \_get\_msg for subsequent calls.
- Set self.validation\_messages from list().
- Set item\_warehouse\_combinations from list().
- Set default\_currency from Platform.db.get\_default(“currency”).
- For each row in self.items.
  - Set key from list(row.item\_code, row.warehouse).
  - For each field in list(“serial\_no”, “batch\_no”).
    - If row.get(field).
      - Evaluate key.append(row.get(field)).
  - For each dimension in get\_inventory\_dimensions().
    - If row.get(dimension.get(“fieldname”)).
      - Evaluate key.append(row.get(dimension.get(“fieldname”))).
  - If key belongs to item\_warehouse\_combinations.
    - Evaluate self.validation\_messages.append(\_get\_msg(row.idx, translated “Same item and warehouse combination already entered.”)).
  - Otherwise.
    - Evaluate item\_warehouse\_combinations.append(key).
  - Evaluate self.validate\_item(row.item\_code, row).
  - If (row.serial\_no and not row.qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.serial\_no → not row.qty.
    - Evaluate self.validation\_messages.append(\_get\_msg(row.idx, formatted text Quantity should not be zero for the {bold(row.item\_code)} since serial nos are specified)).
  - If (row.qty belongs to list(empty text, no value) and row.valuation\_rate belongs to list(empty text, no value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.qty belongs to list(empty text, no value) → row.valuation\_rate belongs to list(empty text, no value).
    - Evaluate self.validation\_messages.append(\_get\_msg(row.idx, translated “Please specify either Quantity or Valuation Rate or both”)).
  - If flt(row.qty) &lt; 0.
    - Evaluate self.validation\_messages.append(\_get\_msg(row.idx, translated “Negative Quantity is not allowed”)).
  - If flt(row.valuation\_rate) &lt; 0.
    - Evaluate self.validation\_messages.append(\_get\_msg(row.idx, translated “Negative Valuation Rate is not allowed”)).
  - If (row.qty and row.valuation\_rate belongs to list(empty text, no value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.qty → row.valuation\_rate belongs to list(empty text, no value).
    - Set row.valuation\_rate from \_get\_stock\_balance(row.item\_code, row.warehouse, self.posting\_date, self.posting\_time, with\_valuation\_rate = true) at 1.
    - If not row.valuation\_rate.
      - Set buying\_rate from Platform.db.get\_value(“Item Price”, mapping(“item\_code” → row.item\_code, “buying” → 1, “currency” → default\_currency), “price\_list\_rate”).
      - If buying\_rate.
        - Set row.valuation\_rate from buying\_rate.
      - Otherwise.
        - Set row.valuation\_rate from Platform.get\_value(“Item”, row.item\_code, “valuation\_rate”).
    - Update self.difference\_amount using + flt((flt(row.qty) × (flt(row.valuation\_rate) − flt(row.flags.difference\_valuation\_rate))), row.precision(“amount”)).
- If self.validation\_messages.
  - For each msg in self.validation\_messages.
    - Evaluate msgprint(msg).
  - Raise Platform.ValidationError(self.validation\_messages).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate item](operations-098.md#op-72980082ef36fc).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L146) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1067)

<a id="op-d70e1d4d450835"></a>
### Stock Reconciliation.validate data.get msg

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_validate_data_get_message`

**Inputs** row\_num, msg.

**Explicit results** ((translated “Row #{0}:”.format(row\_num) + one space) + msg).

**Local steps**

- Return ((translated “Row #{0}:”.format(row\_num) + one space) + msg).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0859.json#L5139) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L147) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1068)

<a id="op-79038b69f827fd"></a>
### Stock Reconciliation.change row indexes

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_change_row_indexes`

**Inputs** self.

**Local steps**

- If getattr(self, “change\_idx”, false).
  - For each tuple(i, item) in enumerate(self.items).
    - Set item.idx from (i + 1).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self, “change\_idx”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0859.json#L5231) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1041)

<a id="op-72980082ef36fc"></a>
### Stock Reconciliation.validate item

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_validate_item`

**Inputs** self, item\_code, row.

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Local steps**

- Bind dependencies validate\_cancelled\_item, validate\_end\_of\_life, validate\_is\_stock\_item.
- Bind local operation validate\_serial\_batch\_items for subsequent calls.
- Attempt the following.
  - Set item from Platform.get\_cached\_doc(“Item”, item\_code).
  - Evaluate validate\_end\_of\_life(item\_code, item.end\_of\_life, item.disabled).
  - Evaluate validate\_is\_stock\_item(item\_code, item.is\_stock\_item).
  - Evaluate validate\_serial\_batch\_items().
  - Evaluate validate\_cancelled\_item(item\_code, item.docstatus).
- On failure (Exception) bound to e.
  - Evaluate self.validation\_messages.append(((translated “Row #” + (“%d: ” modulo or format row.idx)) + cstr(e))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, item\_code).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0859.json#L5359) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L150) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1071)

<a id="op-badf0e531a48ed"></a>
### Stock Reconciliation.validate item.validate serial batch items

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_validate_item_validate_serial_batch_items`

**Inputs** no declared parameters.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** Platform.ValidationError(translated “Please enter Batch No”) · Platform.ValidationError(translated “Please enter Serial No”).

**Local steps**

- Set tuple(has\_batch\_no, has\_serial\_no) from Platform.get\_value(“Item”, item\_code, list(“has\_batch\_no”, “has\_serial\_no”)).
- If (row.use\_serial\_batch\_fields and self.purpose equals “Stock Reconciliation”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.use\_serial\_batch\_fields → self.purpose equals “Stock Reconciliation”.
  - If (has\_batch\_no and not row.batch\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_batch\_no → not row.batch\_no.
    - Raise Platform.ValidationError(translated “Please enter Batch No”).
  - If (has\_serial\_no and not row.serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_serial\_no → not row.serial\_no.
    - Raise Platform.ValidationError(translated “Please enter Serial No”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0859.json#L5934) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L151) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1072)

<a id="op-6148a71f11d4e3"></a>
### Stock Reconciliation.validate reserved stock

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_validate_reserved_stock`

**Inputs** self.

**Declared result** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Bind dependencies get\_sre\_reserved\_qty\_details.
- Set tuple(item\_code\_list, warehouse\_list) from tuple(list(), list()).
- For each tuple(item\_code, warehouse) in self.get\_item\_warehouses\_changing\_qty().
  - Evaluate item\_code\_list.append(item\_code).
  - Evaluate warehouse\_list.append(warehouse).
- Set sre\_reserved\_qty\_details from get\_sre\_reserved\_qty\_details(item\_code\_list, warehouse\_list).
- If sre\_reserved\_qty\_details.
  - Set data from list().
  - For each tuple(tuple(item\_code, warehouse), reserved\_qty) in sre\_reserved\_qty\_details.items().
    - Evaluate data.append(list(item\_code, warehouse, reserved\_qty)).
  - Set msg from empty text.
  - If len(data) equals 1.
    - Set msg from translated “{0} units are reserved for Item {1} in Warehouse {2}, please un-reserve the same to {3} the Stock Reconciliation.”.format(bold(data at 0 at 2), bold(data at 0 at 0), bold(data at 0 at 1), self.\_action).
  - Otherwise.
    - Set items\_html from empty text.
    - For each d in data.
      - Update items\_html using + text in the contract.format(bold(d at 2), bold(d at 0), bold(d at 1)).
    - Set msg from translated “The stock has been reserved for the following Items and Warehouses, un-reserve the same to {0} the Stock Rec …”.format(self.\_action, items\_html).
  - Call the validation error handler Platform.throw(msg, title = translated “Stock Reservation”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item warehouses changing qty](operations-098.md#op-5e291b89a99524).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L152) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1073)

<a id="op-5e291b89a99524"></a>
### Stock Reconciliation.get item warehouses changing qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_get_item_warehouses_changing_qty`

**Inputs** self.

**Declared result** list at tuple at tuple(str, str).

**Explicit results** list of tuple(item.item\_code, item.warehouse) for item drawn from self.items where item.qty differs from item.current\_qty · list of key for tuple(key, change) drawn from qty\_change.items() where abs(change) &gt; 1e-09.

**Local steps**

- If self.purpose differs from ADJUSTMENT\_ENTRY.
  - Return list of tuple(item.item\_code, item.warehouse) for item drawn from self.items where item.qty differs from item.current\_qty.
    - Draw item from self.items, keep a combination only if (item.qty differs from item.current\_qty).
- Set qty\_change from defaultdict(float).
- For each item in self.items.
  - Update qty\_change at tuple(item.item\_code, item.warehouse) using + (flt(item.qty) − flt(item.current\_qty)).
- Return list of key for tuple(key, change) drawn from qty\_change.items() where abs(change) &gt; 1e-09.
  - Draw tuple(key, change) from qty\_change.items(), keep a combination only if (abs(change) &gt; 1e-09).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1300) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L797)

<a id="op-24873dfd5aa284"></a>
### Stock Reconciliation.update stock ledger

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_update_stock_ledger`

**Inputs** self, allow\_negative\_stock = false.

**Record and data access** read “Item” via get\_cached\_value · read “Stock Settings” via get\_single\_value.

**State and service calls** call cancel on AdjustmentEntry(self).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} is not a Serialized/Batched Item. It cannot have a Serial No/Batch No against it.”.format(row.idx, Platform.bold(row.item\_code)) · validation helper — translated “Valuation Rate required for Item {0} at row {1}”.format(row.item\_code, row.idx) · validation helper — translated “No stock ledger entries were created. Please set the quantity or valuation rate for the items properly and t …”.

**Local steps**

- Bind dependencies get\_previous\_sle.
- If self.purpose equals ADJUSTMENT\_ENTRY.
  - If self.docstatus equals 2.
    - Evaluate AdjustmentEntry(self).cancel().
  - Otherwise.
    - Evaluate AdjustmentEntry(self).post().
  - Return no value.
- If self.docstatus equals 2.
  - Evaluate self.make\_sle\_on\_cancel(allow\_negative\_stock).
  - Return no value.
- Set sl\_entries from list().
- For each row in self.items.
  - If (not row.qty and not row.valuation\_rate and not row.current\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.qty → not row.valuation\_rate → not row.current\_qty.
    - Evaluate self.make\_adjustment\_entry(row, sl\_entries).
    - Continue with the next iteration or loop test.
  - Set item from Platform.get\_cached\_value(“Item”, row.item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1).
  - If (item.has\_serial\_no or item.has\_batch\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.has\_serial\_no → item.has\_batch\_no.
    - Evaluate self.get\_sle\_for\_serialized\_items(row, sl\_entries).
  - Otherwise.
    - If row.serial\_and\_batch\_bundle.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} is not a Serialized/Batched Item. It cannot have a Serial No/Batch No against it.”.format(row.idx, Platform.bold(row.item\_code))).
    - Set previous\_sle from get\_previous\_sle(mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time)).
    - If previous\_sle.
      - If row.qty belongs to tuple(empty text, no value).
        - Set row.qty from previous\_sle.get(“qty\_after\_transaction”, 0).
      - If row.valuation\_rate belongs to tuple(empty text, no value).
        - Set row.valuation\_rate from previous\_sle.get(“valuation\_rate”, 0).
    - If (row.qty and not row.valuation\_rate and not row.allow\_zero\_valuation\_rate).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.qty → not row.valuation\_rate → not row.allow\_zero\_valuation\_rate.
      - Call the validation error handler Platform.throw(translated “Valuation Rate required for Item {0} at row {1}”.format(row.item\_code, row.idx)).
    - If ((previous\_sle and row.qty equals previous\_sle.get(“qty\_after\_transaction”) and (row.valuation\_rate equals previous\_sle.get(“valuation\_rate”) or row.qty equals 0)) or (not previous\_sle and not row.qty)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (previous\_sle and row.qty equals previous\_sle.get(“qty\_after\_transaction”) and (row.valuation\_rate equals previous\_sle.get(“valuation\_rate”) or row.qty equals 0)) → (not previous\_sle and not row.qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_sle → row.qty equals previous\_sle.get(“qty\_after\_transaction”) → (row.valuation\_rate equals previous\_sle.get(“valuation\_rate”) or row.qty equals 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.valuation\_rate equals previous\_sle.get(“valuation\_rate”) → row.qty equals 0.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not previous\_sle → not row.qty.
      - Continue with the next iteration or loop test.
    - Evaluate sl\_entries.append(self.get\_sle\_for\_items(row)).
- If sl\_entries.
  - If not allow\_negative\_stock.
    - Set allow\_negative\_stock from cint(Platform.db.get\_single\_value(“Stock Settings”, “allow\_negative\_stock”)).
  - Evaluate self.make\_sl\_entries(sl\_entries, allow\_negative\_stock = allow\_negative\_stock).
- Otherwise.
  - <a id="op-24873dfd5aa284-guard-74"></a>If self.docstatus equals 1.
    - Call the validation error handler Platform.throw(translated “No stock ledger entries were created. Please set the quantity or valuation rate for the items properly and t …”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 1, self.docstatus = 1 (submitted) selects the branch that calls the validation-error handler with translated “No stock ledger entries were created. Please set the quantity or valuation rate for the items properly and t …”. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-24873dfd5aa284-guard-74)

**Methods declared on this owner** [make sle on cancel](operations-098.md#op-eb26d64badc13c), [make adjustment entry](operations-098.md#op-e202207667abca), [get sle for serialized items](operations-098.md#op-e2a6f09da506fc), [get sle for items](operations-098.md#op-9647b88abf5514).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1), Platform.db.get\_single\_value(“Stock Settings”, “allow\_negative\_stock”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L144) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1065)

<a id="op-67242f748b278f"></a>
### Stock Reconciliation.get balance before reconciliation

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_get_balance_before_reconciliation`

**Inputs** self, row.

**Declared result** dict.

**Explicit results** get\_previous\_sle(mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time)).

**Local steps**

- Bind dependencies get\_previous\_sle.
- Return get\_previous\_sle(mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L795)

<a id="op-77eac3d3d2c723"></a>
### Stock Reconciliation.get stranded stock value

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_get_stranded_stock_value`

**Inputs** self, row, previous\_sle = no value.

**Declared result** float.

**Explicit results** 0.0 · get\_stock\_value\_difference(row.item\_code, row.warehouse, self.posting\_date, self.posting\_time, …).

**Local steps**

- Bind dependencies get\_stock\_value\_difference.
- If previous\_sle is identical to no value.
  - Set previous\_sle from self.get\_balance\_before\_reconciliation(row).
- If flt(previous\_sle.get(“qty\_after\_transaction”)).
  - Return 0.0.
- Return get\_stock\_value\_difference(row.item\_code, row.warehouse, self.posting\_date, self.posting\_time, …).

**Methods declared on this owner** [get balance before reconciliation](operations-098.md#op-67242f748b278f).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1303) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L800)

<a id="op-e202207667abca"></a>
### Stock Reconciliation.make adjustment entry

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_make_adjustment_entry`

**Inputs** self, row, sl\_entries.

**Explicit results** no value.

**Local steps**

- Set previous\_sle from self.get\_balance\_before\_reconciliation(row).
- Set difference\_amount from self.get\_stranded\_stock\_value(row, previous\_sle = previous\_sle).
- If not flt(difference\_amount, self.precision(“difference\_amount”)).
  - Return no value.
- Set args from self.get\_sle\_for\_items(row).
- Evaluate args.update(mapping(“stock\_value\_difference” → (negative 1 × difference\_amount), “valuation\_rate” → flt(previous\_sle.get(“valuation\_rate”)), “is\_adjustment\_entry” → 1)).
- Evaluate sl\_entries.append(args).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get balance before reconciliation](operations-098.md#op-67242f748b278f), [get stranded stock value](operations-098.md#op-77eac3d3d2c723), [get sle for items](operations-098.md#op-9647b88abf5514).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1049)

<a id="op-e2a6f09da506fc"></a>
### Stock Reconciliation.get sle for serialized items

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_get_stock_ledger_entry_for_serialized_items`

**Inputs** self, row, sl\_entries.

**Local steps**

- If row.current\_serial\_and\_batch\_bundle.
  - Set args from self.get\_sle\_for\_items(row).
  - Evaluate args.update(mapping(“actual\_qty” → (negative 1 × row.current\_qty), “serial\_and\_batch\_bundle” → row.current\_serial\_and\_batch\_bundle, “valuation\_rate” → row.current\_valuation\_rate)).
  - Evaluate sl\_entries.append(args).
- If row.qty differs from 0.
  - Set args from self.get\_sle\_for\_items(row).
  - Evaluate args.update(mapping(“actual\_qty” → row.qty, “incoming\_rate” → row.valuation\_rate, “serial\_and\_batch\_bundle” → row.serial\_and\_batch\_bundle)).
  - Evaluate sl\_entries.append(args).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sle for items](operations-098.md#op-9647b88abf5514).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0860.json#L1505) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1046)

<a id="op-9647b88abf5514"></a>
### Stock Reconciliation.get sle for items

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_get_stock_ledger_entry_for_items`

**Inputs** self, row, serial\_nos = no value, current\_bundle = true.

**Record and data access** read “Item” via get\_value.

**Explicit results** data.

**Local steps**

- If (not serial\_nos and row.serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not serial\_nos → row.serial\_no.
  - Set serial\_nos from get\_serial\_nos(row.serial\_no).
- Set data from Platform.\_dict(mapping(“doctype” → “Stock Ledger Entry”, “item\_code” → row.item\_code, “warehouse” → row.warehouse, “posting\_date” → self.posting\_date, …)).
  - Value choice on self.docstatus equals 2 — true gives 1, false gives 0.
- If not row.batch\_no.
  - Set data.qty\_after\_transaction from flt(row.qty, row.precision(“qty”)).
- Set dimensions from get\_inventory\_dimensions().
- Set has\_dimensions from false.
- For each dimension in dimensions.
  - If row.get(dimension.get(“fieldname”)).
    - Set has\_dimensions from true.
- If self.docstatus equals 2.
  - If self.is\_adjustment\_row(row).
    - Set data.actual\_qty from 0.0.
    - Set data.qty\_after\_transaction from flt(row.current\_qty).
    - Set data.previous\_qty\_after\_transaction from flt(row.current\_qty).
    - Set data.valuation\_rate from flt(row.current\_valuation\_rate).
    - Set data.stock\_value from flt(row.current\_amount).
    - Set data.stock\_value\_difference from (negative 1 × flt(row.amount\_difference)).
  - Otherwise.
    - If (row.current\_qty and current\_bundle).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.current\_qty → current\_bundle.
      - Set data.actual\_qty from (negative 1 × row.current\_qty).
      - Set data.qty\_after\_transaction from flt(row.current\_qty).
      - Set data.previous\_qty\_after\_transaction from flt(row.qty).
      - Set data.valuation\_rate from flt(row.current\_valuation\_rate).
      - Set data.serial\_and\_batch\_bundle from row.current\_serial\_and\_batch\_bundle.
      - Set data.stock\_value from (data.qty\_after\_transaction × data.valuation\_rate).
      - Set data.stock\_value\_difference from (negative 1 × flt(row.amount\_difference)).
    - Otherwise.
      - Set data.actual\_qty from row.qty.
      - Set data.qty\_after\_transaction from 0.0.
      - Set data.serial\_and\_batch\_bundle from row.serial\_and\_batch\_bundle.
      - Set data.valuation\_rate from flt(row.valuation\_rate).
      - Set data.stock\_value\_difference from (negative 1 × flt(row.amount\_difference)).
- Otherwise.
  - If (self.docstatus equals 1 and has\_dimensions and (not row.batch\_no or not row.serial\_and\_batch\_bundle)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → has\_dimensions → (not row.batch\_no or not row.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.batch\_no → not row.serial\_and\_batch\_bundle.
    - Set data.actual\_qty from row.qty.
    - Set data.qty\_after\_transaction from 0.0.
    - Set data.incoming\_rate from flt(row.valuation\_rate).
- Evaluate self.update\_inventory\_dimensions(row, data).
- Return data.

**Methods declared on this owner** [is adjustment row](operations-099.md#op-1485cf1375f49b).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1045)

<a id="op-eb26d64badc13c"></a>
### Stock Reconciliation.make sle on cancel

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_make_stock_ledger_entry_on_cancel`

**Inputs** self, allow\_negative\_stock = false.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- Set sl\_entries from list().
- Set has\_serial\_no from false.
- For each row in self.items.
  - Evaluate sl\_entries.append(self.get\_sle\_for\_items(row)).
  - If (row.serial\_and\_batch\_bundle and row.current\_serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.serial\_and\_batch\_bundle → row.current\_serial\_and\_batch\_bundle.
    - Evaluate sl\_entries.append(self.get\_sle\_for\_items(row, current\_bundle = false)).
- If sl\_entries.
  - If has\_serial\_no.
    - Set sl\_entries from self.merge\_similar\_item\_serial\_nos(sl\_entries).
  - Evaluate sl\_entries.reverse().
  - Set allow\_negative\_stock from (allow\_negative\_stock or cint(Platform.db.get\_single\_value(“Stock Settings”, “allow\_negative\_stock”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in allow\_negative\_stock → cint(Platform.db.get\_single\_value(“Stock Settings”, “allow\_negative\_stock”)).
  - Evaluate self.make\_sl\_entries(sl\_entries, allow\_negative\_stock = allow\_negative\_stock).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sle for items](operations-098.md#op-9647b88abf5514), [merge similar item serial nos](operations-098.md#op-4f9e960a6d1baa).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “allow\_negative\_stock”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1051)

<a id="op-4f9e960a6d1baa"></a>
### Stock Reconciliation.merge similar item serial nos

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_merge_similar_item_serial_numbers`

**Inputs** self, sl\_entries.

**Explicit results** new\_sl\_entries.

**Local steps**

- Set new\_sl\_entries from list().
- Set merge\_similar\_entries from mapping().
- For each d in sl\_entries.
  - If (not d.serial\_no or flt(d.get(“actual\_qty”)) &lt; 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.serial\_no → flt(d.get(“actual\_qty”)) &lt; 0.
    - Evaluate new\_sl\_entries.append(d).
    - Continue with the next iteration or loop test.
  - Set key from tuple(d.item\_code, d.warehouse).
  - If key does not belong to merge\_similar\_entries.
    - Set d.total\_amount from (flt(d.actual\_qty) × d.valuation\_rate).
    - Set merge\_similar\_entries at key from d.
  - Otherwise.
    - If d.serial\_no.
      - Set data from merge\_similar\_entries at key.
      - Update data.actual\_qty using + d.actual\_qty.
      - Update data.qty\_after\_transaction using + d.qty\_after\_transaction.
      - Update data.total\_amount using + (d.actual\_qty × d.valuation\_rate).
      - Set data.valuation\_rate from (data.total\_amount ÷ data.actual\_qty).
      - Update data.serial\_no using + (whitespace '\\n' + d.serial\_no).
      - Set data.incoming\_rate from (data.total\_amount ÷ data.actual\_qty).
- Evaluate new\_sl\_entries.extend(merge\_similar\_entries.values()).
- Return new\_sl\_entries.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0860.json#L3545) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1052)

<a id="op-fcda470ad9b951"></a>
### Stock Reconciliation.get gl entries

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_get_general_ledger_entries`

**Inputs** self, inventory\_account\_map = no value.

**Explicit results** super().get\_gl\_entries(inventory\_account\_map, self.expense\_account, self.cost\_center).

**Local steps**

- If not self.cost\_center.
  - Evaluate msgprint(translated “Please enter Cost Center”, raise\_exception = 1).
- Return super().get\_gl\_entries(inventory\_account\_map, self.expense\_account, self.cost\_center).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1044)

<a id="op-174767fa3ddc9e"></a>
### Stock Reconciliation.validate expense account

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_validate_expense_account`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value · read “Stock Ledger Entry” via get\_all · read “Account” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Please enter Expense Account” · validation helper — translated “Difference Account {0} cannot be a Stock account”.format(Platform.bold(self.expense\_account)) · validation helper with OpeningEntryAccountError — translated “Difference Account must be a Asset/Liability type account, since this Stock Reconciliation is an Opening Entry”.

**Local steps**

- If not cint(Enterprise.is\_perpetual\_inventory\_enabled(self.company)).
  - Return no value.
- If not self.expense\_account.
  - Call the validation error handler Platform.throw(translated “Please enter Expense Account”).
- Otherwise.
  - If Platform.get\_cached\_value(“Account”, self.expense\_account, “account\_type”) equals “Stock”.
    - Call the validation error handler Platform.throw(translated “Difference Account {0} cannot be a Stock account”.format(Platform.bold(self.expense\_account))).
  - Otherwise.
    - If (self.purpose equals “Opening Stock” or not Platform.db.get\_all(“Stock Ledger Entry”, filters = mapping(“company” → self.company, “is\_cancelled” → 0), limit = 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purpose equals “Opening Stock” → not Platform.db.get\_all(“Stock Ledger Entry”, filters = mapping(“company” → self.company, “is\_cancelled” → 0), limit = 1).
      - If Platform.db.get\_value(“Account”, self.expense\_account, “report\_type”) equals “Profit and Loss”.
        - Call the validation error handler Platform.throw(translated “Difference Account must be a Asset/Liability type account, since this Stock Reconciliation is an Opening Entry”, OpeningEntryAccountError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.expense\_account, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L148) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1069)

<a id="op-539e105c27a2df"></a>
### Stock Reconciliation.validate opening stock

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_validate_opening_stock`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Rows {0}: the items already have stock transactions in these warehouses, use the purpose Stock Reconciliatio …”.format(“, ”.join(rows)).

**Local steps**

- If (self.purpose differs from “Opening Stock” or not self.items).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purpose differs from “Opening Stock” → not self.items.
  - Return no value.
- Set dimensions from list of dimension.get(“fieldname”) for dimension drawn from get\_inventory\_dimensions().
  - Draw dimension from get\_inventory\_dimensions().
- Set entries from mapping().
- For each entry in self.get\_existing\_ledger\_entries(dimensions).
  - Evaluate entries.setdefault(tuple(entry.item\_code, entry.warehouse), list()).append(entry).
- Set rows from list of str(row.idx) for row drawn from self.items where any(generator of all(generator of nested operand in the contract(nested operand in the contract) equals nested operand in the contract(nested operan ….
  - Draw row from self.items, keep a combination only if (any(generator of all(generator of nested operand in the contract.get(field) equals nested operand in the contract.get(field) for field drawn from dimensions where row.get(field)) for entry drawn from entries.g …)).
  - Draw entry from entries.get(tuple(row.item\_code, row.warehouse), list()).
  - Draw field from dimensions, keep a combination only if (row.get(field)).
- If rows.
  - Call the validation error handler Platform.throw(translated “Rows {0}: the items already have stock transactions in these warehouses, use the purpose Stock Reconciliatio …”.format(“, ”.join(rows))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get existing ledger entries](operations-099.md#op-f11986ed21b2e7).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1310) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L807)
