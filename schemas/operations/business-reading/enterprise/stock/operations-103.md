# Inventory and warehouses · operations 103

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock reservation entry

[Record definition](../../../../data/record-types/stock_reservation_entry.json)

<a id="op-3ec41c7818bf49"></a>
### Stock Reservation.initialize fields

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_initialize_fields`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.table\_name from “items”.
- Set self.qty\_field from “stock\_qty”.
- Set self.warehouse\_field from “warehouse”.
- Set self.warehouse from no value.
- If self.doc.doctype equals “Work Order”.
  - Set self.table\_name from “required\_items”.
  - Set self.qty\_field from “required\_qty”.
  - Set self.warehouse\_field from “source\_warehouse”.
  - If (self.doc.skip\_transfer and self.doc.from\_wip\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.skip\_transfer → self.doc.from\_wip\_warehouse.
    - Set self.warehouse from self.doc.wip\_warehouse.
- Otherwise.
  - If self.doc.doctype equals “Subcontracting Order”.
    - Set self.table\_name from “supplied\_items”.
    - Set self.qty\_field from “required\_qty”.
  - Otherwise.
    - If (self.doc.doctype equals “Production Plan” and self.kwargs).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.doctype equals “Production Plan” → self.kwargs.
      - For each tuple(key, value) in self.kwargs.items().
        - Evaluate setattr(self, key, value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L277) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1191)

<a id="op-bc7e8730806144"></a>
### Stock Reservation.cancel stock reservation entries

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_cancel_stock_reservation_entries`

**Inputs** self, names = no value.

**Declared result** no value.

**Record and data access** resolve a document from “Stock Reservation Entry” via get\_doc.

**State and service calls** call cancel on sre\_doc · msgprint with translated “Stock has been unreserved for work order {0}.”.format(Platform.bold(self.doc.name)).

**Local steps**

- If isinstance(names, str).
  - Set names from parse\_json(names).
- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set query from nested operand in the contract.qb.from\_(sre).select(sre.name).where(((sre.docstatus equals 1 bitwise and sre.voucher\_type equals self.doc.doctype) bitwise and sre.voucher\_no equals self.doc.name)).
- If names.
  - Set query from query.where(sre.name.isin(names)).
- Otherwise.
  - If self.warehouse.
    - Set query from query.where(sre.warehouse equals self.warehouse).
- Set sre\_names from query.run(as\_dict = true).
- If sre\_names.
  - For each sre\_name in sre\_names.
    - Set sre\_doc from Platform.get\_doc(“Stock Reservation Entry”, sre\_name.name).
    - Set sre\_doc.flags.ignore\_permissions from true.
    - Evaluate sre\_doc.cancel().
- If (sre\_names and names).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sre\_names → names.
  - Evaluate Platform.msgprint(translated “Stock has been unreserved for work order {0}.”.format(Platform.bold(self.doc.name)), alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1161)

<a id="op-0f287ee27bbe0c"></a>
### Stock Reservation.make stock reservation entries

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_make_stock_reservation_entries`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Item” via get\_cached\_value.

**State and service calls** request new\_doc for “Stock Reservation Entry” · msgprint with translated “Enable Allow Partial Reservation in the Stock Settings to reserve partial stock.” · call save on sre · call submit on sre.

**Explicit results** is\_sre\_created.

**Explicit failure paths** validation helper — translated “Source Warehouse is mandatory for the Item {0}.”.format(Platform.bold(item.item\_code)).

**Local steps**

- Set items from self.items.
- If not items.
  - Set items from self.doc.get(self.table\_name).
- Set child\_doctype from Platform.scrub((self.doc.doctype + “ Item”)).
- Set allow\_partial\_reservation from Platform.get\_single\_value(“Stock Settings”, “allow\_partial\_reservation”).
- Set is\_sre\_created from false.
- For each item in items.
  - Set sre from Platform.new\_doc(“Stock Reservation Entry”).
  - Set sre.flags.ignore\_permissions from true.
  - If isinstance(item, dict).
    - Set item from Platform.\_dict(item).
  - Set item\_code from (item.get(“item\_code”) or item.get(“production\_item”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“item\_code”) → item.get(“production\_item”).
  - Set item\_details from Platform.get\_cached\_value(“Item”, item\_code, list(“has\_serial\_no”, “has\_batch\_no”, “stock\_uom”), as\_dict = true).
  - Set warehouse from (self.warehouse or item.get(self.warehouse\_field) or item.get(“warehouse”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.warehouse → item.get(self.warehouse\_field) → item.get(“warehouse”).
  - If (self.doc.doctype equals “Production Plan” and item.get(“from\_warehouse”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.doctype equals “Production Plan” → item.get(“from\_warehouse”).
    - Set warehouse from item.get(“from\_warehouse”).
  - If (not warehouse and self.doc.doctype equals “Work Order” and (not self.doc.skip\_transfer or not self.doc.from\_wip\_warehouse)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not warehouse → self.doc.doctype equals “Work Order” → (not self.doc.skip\_transfer or not self.doc.from\_wip\_warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.doc.skip\_transfer → not self.doc.from\_wip\_warehouse.
    - Call the validation error handler Platform.throw(translated “Source Warehouse is mandatory for the Item {0}.”.format(Platform.bold(item.item\_code))).
  - Set qty from (item.get(self.qty\_field) or item.get(“stock\_qty”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(self.qty\_field) → item.get(“stock\_qty”).
  - If not qty.
    - Continue with the next iteration or loop test.
  - Set self.available\_qty\_to\_reserve from self.get\_available\_qty\_to\_reserve(item\_code, warehouse).
  - If not self.available\_qty\_to\_reserve.
    - Evaluate self.throw\_stock\_not\_exists\_error(item.get(“idx”), item\_code, warehouse).
  - Set self.qty\_to\_be\_reserved from qty when self.available\_qty\_to\_reserve ≥ qty, otherwise self.available\_qty\_to\_reserve.
    - Value choice on self.available\_qty\_to\_reserve ≥ qty — true gives qty, false gives self.available\_qty\_to\_reserve.
  - If not self.qty\_to\_be\_reserved.
    - Continue with the next iteration or loop test.
  - If (self.qty\_to\_be\_reserved &lt; qty and not allow\_partial\_reservation).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.qty\_to\_be\_reserved &lt; qty → not allow\_partial\_reservation.
    - Evaluate Platform.msgprint(translated “Enable Allow Partial Reservation in the Stock Settings to reserve partial stock.”, title = translated “Partial Stock Reservation”, indicator = “yellow”).
    - Continue with the next iteration or loop test.
  - Set sre.item\_code from item\_code.
  - Set sre.warehouse from warehouse.
  - Set sre.has\_serial\_no from item\_details.has\_serial\_no.
  - Set sre.has\_batch\_no from item\_details.has\_batch\_no.
  - Set sre.voucher\_type from (item.get(“voucher\_type”) or self.doc.doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“voucher\_type”) → self.doc.doctype.
  - Set sre.voucher\_no from (item.get(“voucher\_no”) or self.doc.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“voucher\_no”) → self.doc.name.
  - Set sre.voucher\_detail\_no from (item.get(child\_doctype) or item.name or item.get(“voucher\_detail\_no”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(child\_doctype) → item.name → item.get(“voucher\_detail\_no”).
  - Set sre.available\_qty from self.available\_qty\_to\_reserve.
  - Set sre.voucher\_qty from (self.get\_voucher\_qty(item, sre.voucher\_detail\_no) or qty).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_voucher\_qty(item, sre.voucher\_detail\_no) → qty.
  - Set sre.reserved\_qty from self.qty\_to\_be\_reserved.
  - Set sre.company from self.doc.company.
  - Set sre.stock\_uom from item\_details.stock\_uom.
  - Set sre.project from self.doc.project.
  - Set sre.from\_voucher\_no from item.get(“from\_voucher\_no”).
  - Set sre.from\_voucher\_detail\_no from item.get(“from\_voucher\_detail\_no”).
  - Set sre.from\_voucher\_type from item.get(“from\_voucher\_type”).
  - Set sre.reservation\_based\_on from (sre.reservation\_based\_on or “Qty”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sre.reservation\_based\_on → “Qty”.
  - If (item\_details.has\_batch\_no or item\_details.has\_serial\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_details.has\_batch\_no → item\_details.has\_serial\_no.
    - Set sre.reservation\_based\_on from “Serial and Batch”.
  - Evaluate sre.save().
  - If item.get(“serial\_and\_batch\_bundles”).
    - Set sre.reservation\_based\_on from “Serial and Batch”.
    - Evaluate self.set\_serial\_batch(sre, item.serial\_and\_batch\_bundles).
  - Evaluate sre.submit().
  - Set is\_sre\_created from true.
- Return is\_sre\_created.

**Methods declared on this owner** [get available qty to reserve](operations-103.md#op-3befdc740e0ccd), [throw stock not exists error](operations-103.md#op-3f862d33f77ba6), [get voucher qty](operations-103.md#op-a966ac2a17e063), [set serial batch](operations-103.md#op-05b15a6451561d).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_partial\_reservation”), Platform.get\_cached\_value(“Item”, item\_code, list(“has\_serial\_no”, “has\_batch\_no”, “stock\_uom”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L278) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1192)

<a id="op-a966ac2a17e063"></a>
### Stock Reservation.get voucher qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservation_get_voucher_qty`

**Inputs** self, item, voucher\_detail\_no.

**Explicit results** no value · rows at 0.get(self.qty\_field) when rows, otherwise no value.

**Local steps**

- If item.get(“from\_voucher\_type”) belongs to list(“Stock Entry”, “Production Plan”).
  - Return no value.
- Set rows from self.doc.get(self.table\_name, mapping(“name” → voucher\_detail\_no)).
- Return rows at 0.get(self.qty\_field) when rows, otherwise no value.
  - Value choice on rows — true gives rows at 0.get(self.qty\_field), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L825)

<a id="op-05b15a6451561d"></a>
### Stock Reservation.set serial batch

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_set_serial_batch`

**Inputs** self, sre, serial\_batch\_bundles.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Local steps**

- Set bundle\_details from Platform.get\_all(“Serial and Batch Entry”, fields = list(“serial\_no”, “batch\_no”, “qty”), filters = mapping(“parent” → tuple(“in”, serial\_batch\_bundles)), order\_by = “creation”).
- Set qty\_to\_reserve from sre.reserved\_qty.
- For each detail in bundle\_details.
  - Set qty from flt(min(abs(detail.qty), qty\_to\_reserve), sre.precision(“reserved\_qty”)).
  - <a id="op-05b15a6451561d-guard-12"></a>If qty ≤ 0.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Update qty\_to\_reserve using − qty.
  - Evaluate sre.append(“sb\_entries”, mapping(“serial\_no” → detail.serial\_no, “batch\_no” → detail.batch\_no, “qty” → qty, “warehouse” → sre.warehouse)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison qty ≤ 0, qty = 0 selects the branch that exits the enclosing loop. With qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-05b15a6451561d-guard-12)

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L280) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1194)

<a id="op-3f862d33f77ba6"></a>
### Stock Reservation.throw stock not exists error

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_throw_stock_not_exists_error`

**Inputs** self, idx, item\_code, warehouse.

**State and service calls** msgprint with msg.

**Local steps**

- If idx.
  - Set msg from translated “Row #{0}: Stock not available to reserve for the Item {1} in Warehouse {2}.”.format(idx, Platform.bold(item\_code), Platform.bold(warehouse)).
- Otherwise.
  - Set msg from translated “Stock not available to reserve for the Item {0} in Warehouse {1}.”.format(Platform.bold(item\_code), Platform.bold(warehouse)).
- Evaluate Platform.msgprint(msg, title = translated “Stock Reservation”, indicator = “orange”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0871.json#L3069) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L281) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1195)

<a id="op-3befdc740e0ccd"></a>
### Stock Reservation.get available qty to reserve

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_get_available_quantity_to_reserve`

**Inputs** self, item\_code, warehouse, ignore\_sre = no value.

**Explicit results** (available\_qty − reserved\_qty) · available\_qty.

**Local steps**

- Set available\_qty from \_get\_stock\_balance(item\_code, warehouse).
- If available\_qty.
  - Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
  - Set query from nested operand in the contract.qb.from\_(sre).select(Sum((((nested operand in the contract − nested operand in the contract) − nested operand in the contract.transferred\_qty) − sre.consumed\_qty))).where(((( ….
  - If ignore\_sre.
    - Set query from query.where(sre.name differs from ignore\_sre).
  - Set reserved\_qty from (query.run() at 0 at 0 or 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run() at 0 at 0 → 0.0.
  - If reserved\_qty.
    - Return (available\_qty − reserved\_qty).
- Return available\_qty.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L273) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1187)

<a id="op-e7fdeca5b87101"></a>
### Stock Reservation.transfer reservation entries to

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_transfer_reservation_entries_to`

**Inputs** self, docnames, from\_doctype, to\_doctype, against\_fg\_item = no value, qty\_change = no value.

**Record and data access** read “Item” via get\_value.

**State and service calls** msgprint with translated “No available quantity to reserve for item {0} in warehouse {1}”.format(Platform.bold(entry.item\_code), Platform.bold(entry.warehouse)) · request new\_doc for “Stock Reservation Entry” · call insert on sre · call submit on sre.

**Explicit results** no value.

**Local steps**

- If isinstance(docnames, str).
  - Set docnames from list(docnames).
- Set items\_to\_reserve from self.get\_items\_to\_reserve(docnames, from\_doctype, to\_doctype).
- If qty\_change.
  - For each tuple(key, value) in qty\_change.items().
    - Set row from next(generator of item for item drawn from items\_to\_reserve where item.voucher\_detail\_no equals key, no value).
      - Draw item from items\_to\_reserve, keep a combination only if (item.voucher\_detail\_no equals key).
    - If row.
      - Update row.qty using + value.
      - Update row.required\_qty using + value.
- If not items\_to\_reserve.
  - Return no value.
- Set reservation\_entries from self.get\_reserved\_entries(from\_doctype, docnames, against\_fg\_item).
- If not reservation\_entries.
  - Return no value.
- Set entries\_to\_reserve from Platform.\_dict().
- For each row in reservation\_entries.
  - Set reserved\_qty\_field from “reserved\_qty” when row.reservation\_based\_on equals “Qty”, otherwise “sabb\_qty”.
    - Value choice on row.reservation\_based\_on equals “Qty” — true gives “reserved\_qty”, false gives “sabb\_qty”.
  - Set delivered\_qty\_field from “delivered\_qty” when row.reservation\_based\_on equals “Qty”, otherwise “sabb\_delivered\_qty”.
    - Value choice on row.reservation\_based\_on equals “Qty” — true gives “delivered\_qty”, false gives “sabb\_delivered\_qty”.
  - Set available\_qty from (row.get(reserved\_qty\_field) − row.get(delivered\_qty\_field)).
  - For each entry in items\_to\_reserve.
    - If not (row.item\_code equals entry.item\_code and row.warehouse equals entry.warehouse and entry.qty &gt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_code equals entry.item\_code → row.warehouse equals entry.warehouse → entry.qty &gt; 0.
      - Continue with the next iteration or loop test.
    - <a id="op-e7fdeca5b87101-guard-37"></a>If available\_qty ≤ 0.
      - Continue with the next iteration or loop test.
    - Set key from tuple(row.item\_code, row.warehouse, entry.voucher\_detail\_no).
    - If key does not belong to entries\_to\_reserve.
      - Evaluate entries\_to\_reserve.setdefault(key, Platform.\_dict(mapping(“qty\_to\_reserve” → 0.0, “item\_code” → row.item\_code, “warehouse” → row.warehouse, “voucher\_type” → (entry.voucher\_type or to\_doctype), …))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.voucher\_type → to\_doctype.
    - If available\_qty &gt; entry.qty.
      - Set qty\_to\_reserve from entry.qty.
    - Otherwise.
      - Set qty\_to\_reserve from available\_qty.
    - Update available\_qty using − qty\_to\_reserve.
    - Update entry.qty using − qty\_to\_reserve.
    - Update entries\_to\_reserve at key at “qty\_to\_reserve” using + qty\_to\_reserve.
    - If row.has\_batch\_no.
      - Update entries\_to\_reserve at key at “batches” at row.batch\_no using + qty\_to\_reserve.
    - If row.has\_serial\_no.
      - Evaluate entries\_to\_reserve at key at “serial\_nos”.append(row.serial\_no).
    - If row.name.
      - Update entries\_to\_reserve at key at “sre\_names” at row.name using + qty\_to\_reserve.
- For each key in entries\_to\_reserve.
  - Set data from entries\_to\_reserve at key.
  - Evaluate self.update\_delivered\_qty(data).
  - Evaluate self.make\_stock\_reservation\_entry(data).
- Set extra\_items from (set(generator of tuple(entry.item\_code, entry.warehouse) for entry drawn from items\_to\_reserve) − set(generator of tuple(row.item\_code, row.warehouse) for row drawn from reservation\_entries)).
  - Draw entry from items\_to\_reserve.
  - Draw row from reservation\_entries.
- For each entry in list of entry for entry drawn from items\_to\_reserve where tuple(entry.item\_code, entry.warehouse) belongs to extra\_items.
  - Draw entry from items\_to\_reserve, keep a combination only if (tuple(entry.item\_code, entry.warehouse) belongs to extra\_items).
  - Set available\_qty from get\_available\_qty\_to\_reserve(entry.item\_code, entry.warehouse).
  - If not available\_qty.
    - Evaluate Platform.msgprint(translated “No available quantity to reserve for item {0} in warehouse {1}”.format(Platform.bold(entry.item\_code), Platform.bold(entry.warehouse)), alert = true).
    - Continue with the next iteration or loop test.
  - Set sre from Platform.new\_doc(“Stock Reservation Entry”).
  - Set sre.flags.ignore\_permissions from true.
  - Set sre.company from self.doc.company.
  - Set sre.voucher\_type from entry.voucher\_type.
  - Set sre.voucher\_no from entry.voucher\_no.
  - Set sre.voucher\_detail\_no from entry.voucher\_detail\_no.
  - Set sre.available\_qty from available\_qty.
  - Set sre.voucher\_qty from entry.required\_qty.
  - Set sre.item\_code from entry.item\_code.
  - Set sre.warehouse from entry.warehouse.
  - Set sre.stock\_uom from entry.stock\_uom.
  - Set sre.reserved\_qty from min(sre.available\_qty, entry.qty).
  - Set sre.has\_serial\_no from Platform.get\_value(“Item”, sre.item\_code, “has\_serial\_no”).
  - Set sre.has\_batch\_no from Platform.get\_value(“Item”, sre.item\_code, “has\_batch\_no”).
  - Evaluate sre.insert().
  - Evaluate sre.submit().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison available\_qty ≤ 0, available\_qty = 0 selects the branch that continues with the next loop iteration. With available\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e7fdeca5b87101-guard-37)

**Methods declared on this owner** [get items to reserve](operations-103.md#op-689a021fd4576a), [get reserved entries](operations-103.md#op-a10b8a64c90802), [update delivered qty](operations-103.md#op-c02cff33b63ab9), [make stock reservation entry](operations-103.md#op-c3a70770c5f1c9).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L282) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1196)

<a id="op-c02cff33b63ab9"></a>
### Stock Reservation.update delivered qty

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_update_delivered_quantity`

**Inputs** self, data.

**Record and data access** resolve a document from “Stock Reservation Entry” via get\_doc.

**State and service calls** call db\_set on sre.

**Local steps**

- For each tuple(name, qty) in data.get(“sre\_names”).items().
  - Set sre from Platform.get\_doc(“Stock Reservation Entry”, name, for\_update = true).
  - Set delivered\_qty from flt((sre.delivered\_qty + qty), sre.precision(“delivered\_qty”)).
  - Evaluate sre.db\_set(mapping(“delivered\_qty” → delivered\_qty, “status” → “Closed” when delivered\_qty ≥ sre.reserved\_qty, otherwise “Reserved”)).
    - Value choice on delivered\_qty ≥ sre.reserved\_qty — true gives “Closed”, false gives “Reserved”.
  - Evaluate sre.update\_reserved\_qty\_in\_voucher().
- If (data.serial\_nos or data.batches).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.serial\_nos → data.batches.
  - Evaluate move\_serial\_batch\_delivered\_qty(data.get(“sre\_names”), data).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L283) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1197)

<a id="op-c3a70770c5f1c9"></a>
### Stock Reservation.make stock reservation entry

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_make_stock_reservation_entry`

**Inputs** self, row.

**Record and data access** read “Serial No” via get\_value.

**State and service calls** request new\_doc for “Stock Reservation Entry” · call save on sre · call submit on sre.

**Local steps**

- Set fields from list(“item\_code”, “warehouse”, “voucher\_type”, “voucher\_no”, …).
- Set sre from Platform.new\_doc(“Stock Reservation Entry”).
- Set sre.flags.ignore\_permissions from true.
- For each row\_field in fields.
  - Evaluate sre.set(row\_field, row.get(row\_field)).
- Set sre.available\_qty from row.get(“qty\_to\_reserve”).
- Set sre.reserved\_qty from row.get(“qty\_to\_reserve”).
- Set sre.voucher\_qty from row.get(“qty\_to\_reserve”).
- Set against\_row from row.get(“against\_row”).
- Set sre.from\_voucher\_no from against\_row.voucher\_no.
- Set sre.from\_voucher\_detail\_no from against\_row.voucher\_detail\_no.
- Set sre.from\_voucher\_type from against\_row.voucher\_type.
- Set sre.reservation\_based\_on from against\_row.reservation\_based\_on.
- Set sre.has\_serial\_no from against\_row.has\_serial\_no.
- Set sre.has\_batch\_no from against\_row.has\_batch\_no.
- If row.serial\_nos.
  - For each serial\_no in row.serial\_nos.
    - Set batch\_no from no value.
    - If row.batches.
      - Set batch\_no from Platform.db.get\_value(“Serial No”, serial\_no, “batch\_no”).
    - Evaluate sre.append(“sb\_entries”, mapping(“serial\_no” → serial\_no, “warehouse” → row.warehouse, “batch\_no” → batch\_no, “qty” → 1)).
- Otherwise.
  - If row.batches.
    - For each tuple(batch\_no, qty) in row.batches.items().
      - Evaluate sre.append(“sb\_entries”, mapping(“batch\_no” → batch\_no, “warehouse” → row.warehouse, “qty” → qty)).
- Evaluate sre.save().
- Evaluate sre.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L279) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1193)

<a id="op-a10b8a64c90802"></a>
### Stock Reservation.get reserved entries

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_get_reserved_entries`

**Inputs** self, doctype, docnames, against\_fg\_item = no value.

**Record and data access** read “Subcontracting Inward Order Received Item” via get\_all.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- If isinstance(docnames, str).
  - Set docnames from list(docnames).
- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set sabb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- If (self.items and data bound to list of item.from\_voucher\_detail\_no for item drawn from self.items).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.items → data bound to list of item.from\_voucher\_detail\_no for item drawn from self.items.
  - Draw item from self.items.
  - Set query from query.where(sre.voucher\_detail\_no.isin(data)).
- If against\_fg\_item.
  - Set query from query.where(sre.voucher\_detail\_no.isin(Platform.get\_all(“Subcontracting Inward Order Received Item”, mapping(“reference\_name” → against\_fg\_item, “docstatus” → 1), pluck = “name”))).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0872.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L275) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1189)

<a id="op-689a021fd4576a"></a>
### Stock Reservation.get items to reserve

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_get_items_to_reserve`

**Inputs** self, docnames, from\_doctype, to\_doctype.

**Explicit results** items.

**Local steps**

- Set field from Platform.scrub(from\_doctype).
- Set tuple(item\_code\_fieldname, child\_table\_suffix) from tuple(“rm\_item\_code”, “ Supplied Item”) when to\_doctype equals “Subcontracting Order”, otherwise tuple(“item\_code”, “ Item”).
  - Value choice on to\_doctype equals “Subcontracting Order” — true gives tuple(“rm\_item\_code”, “ Supplied Item”), false gives tuple(“item\_code”, “ Item”).
- Set doctype from Platform.qb.DocType(to\_doctype).
- Set child\_doctype from Platform.qb.DocType((to\_doctype + child\_table\_suffix)).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“voucher\_no”), nested operand in the contract.as\_(“voucher\_detail\_no”), nested operand in the contra ….
- If to\_doctype equals “Work Order”.
  - Set query from query.select(child\_doctype.source\_warehouse, doctype.wip\_warehouse, doctype.skip\_transfer, doctype.from\_wip\_warehouse, …).
  - Set query from query.where((doctype.qty &gt; doctype.material\_transferred\_for\_manufacturing bitwise and doctype.status differs from “Completed”)).
- Otherwise.
  - If to\_doctype equals “Subcontracting Order”.
    - Set query from query.select(child\_doctype.stock\_reserved\_qty, child\_doctype.required\_qty.as\_(“qty”), child\_doctype.reserve\_warehouse.as\_(“source\_warehouse”)).
- If (self.items and data bound to list of item.voucher\_detail\_no for item drawn from self.items).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.items → data bound to list of item.voucher\_detail\_no for item drawn from self.items.
  - Draw item from self.items.
  - Set query from query.where(child\_doctype.name.isin(data)).
- Set data from query.run(as\_dict = true).
- Set items from list().
- For each row in data.
  - If row.qty &gt; row.stock\_reserved\_qty.
    - Update row.qty using − flt(row.stock\_reserved\_qty).
    - Set row.warehouse from row.source\_warehouse.
    - If (row.skip\_transfer and row.from\_wip\_warehouse).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.skip\_transfer → row.from\_wip\_warehouse.
      - Set row.warehouse from row.wip\_warehouse.
    - If to\_doctype equals “Work Order”.
      - Set row.voucher\_type from “Work Order”.
    - Evaluate items.append(row).
- Return items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L274) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1188)

<a id="op-59f9d5bf9253a4"></a>
### Create stock reservation entries for so items

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_create_stock_reservation_entries_for_sales_order_items`

**Inputs** sales\_order, items\_details = no value, from\_voucher\_type = no value, notify = true.

**Record and data access** read “Warehouse” via get\_cached\_value · read “Stock Settings” via get\_single\_value · resolve a document from “Sales Order Item” via get\_doc · read “Item” via get\_cached\_value.

**State and service calls** msgprint with translated “Stock cannot be reserved in the group warehouse {0}.”.format(Platform.bold(sales\_order.set\_warehouse)) · msgprint with translated “Row #{0}: Stock cannot be reserved for a non-stock Item {1}”.format(item.idx, Platform.bold(item.item\_code)) · call db\_set on item · msgprint with translated “Row #{0}: Stock cannot be reserved in group warehouse {1}.”.format(item.idx, Platform.bold(item.warehouse)) · msgprint with translated “Row #{0}: Stock is already reserved for the Item {1}.”.format(item.idx, Platform.bold(item.item\_code)) · 7 additional forms in the steps below.

**Explicit results** Platform.msgprint(translated “Stock cannot be reserved in the group warehouse {0}.”.format(Platform.bold(sales\_order.set\_warehouse))) · sre\_count.

**Explicit failure paths** validation helper — translated “Sales Order Item {0} does not belong to {1}”.format(so\_item.name, sales\_order.name) · validation helper — translated “Row #{0}: Item {1} has been picked, please reserve stock from the Pick List.”.format(item.idx, Platform.bold(item.item\_code)).

**Local steps**

- Bind dependencies get\_unreserved\_qty.
- If (not from\_voucher\_type and (sales\_order.get(“\_action”) equals “submit” and sales\_order.set\_warehouse and cint(Platform.get\_cached\_value(“Warehouse”, sales\_order.set\_warehouse, “is\_group”)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not from\_voucher\_type → (sales\_order.get(“\_action”) equals “submit” and sales\_order.set\_warehouse and cint(Platform.get\_cached\_value(“Warehouse”, sales\_order.set\_warehouse, “is\_group”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sales\_order.get(“\_action”) equals “submit” → sales\_order.set\_warehouse → cint(Platform.get\_cached\_value(“Warehouse”, sales\_order.set\_warehouse, “is\_group”)).
  - Return Platform.msgprint(translated “Stock cannot be reserved in the group warehouse {0}.”.format(Platform.bold(sales\_order.set\_warehouse))).
- Evaluate validate\_stock\_reservation\_settings(sales\_order).
- Set allow\_partial\_reservation from Platform.get\_single\_value(“Stock Settings”, “allow\_partial\_reservation”).
- Set items from list().
- If items\_details.
  - For each item in items\_details.
    - Set so\_item from Platform.get\_doc(“Sales Order Item”, item.get(“sales\_order\_item”)).
    - If so\_item.parent differs from sales\_order.name.
      - Call the validation error handler Platform.throw(translated “Sales Order Item {0} does not belong to {1}”.format(so\_item.name, sales\_order.name)).
    - Set so\_item.warehouse from item.get(“warehouse”).
    - Set so\_item.qty\_to\_reserve from flt(item.get(“qty\_to\_reserve”)) when from\_voucher\_type belongs to list(“Pick List”, “Purchase Receipt”), otherwise (flt(item.get(“qty\_to\_reserve”)) × (flt(item.get(“conversion\_factor”)) or flt(so\_item.conv ….
      - Value choice on from\_voucher\_type belongs to list(“Pick List”, “Purchase Receipt”) — true gives flt(item.get(“qty\_to\_reserve”)), false gives (flt(item.get(“qty\_to\_reserve”)) × (flt(item.get(“conversion\_factor”)) or flt(so\_item.conversion\_factor) or 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.get(“conversion\_factor”)) → flt(so\_item.conversion\_factor) → 1.
    - Set so\_item.from\_voucher\_no from item.get(“from\_voucher\_no”).
    - Set so\_item.from\_voucher\_detail\_no from item.get(“from\_voucher\_detail\_no”).
    - Set so\_item.serial\_and\_batch\_bundle from item.get(“serial\_and\_batch\_bundle”).
    - Evaluate items.append(so\_item).
- Set sre\_count from 0.
- Set reserved\_qty\_details from get\_sre\_reserved\_qty\_details\_for\_voucher(“Sales Order”, sales\_order.name).
- For each item in items when items\_details, otherwise sales\_order.get(“items”).
  - Value choice on items\_details — true gives items, false gives sales\_order.get(“items”).
  - If not item.get(“reserve\_stock”).
    - Continue with the next iteration or loop test.
  - If (from\_voucher\_type differs from “Pick List” and flt(item.picked\_qty) &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_voucher\_type differs from “Pick List” → flt(item.picked\_qty) &gt; 0.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} has been picked, please reserve stock from the Pick List.”.format(item.idx, Platform.bold(item.item\_code))).
  - Set tuple(is\_stock\_item, has\_serial\_no, has\_batch\_no) from Platform.get\_cached\_value(“Item”, item.item\_code, list(“is\_stock\_item”, “has\_serial\_no”, “has\_batch\_no”)).
  - If not is\_stock\_item.
    - If not from\_voucher\_type.
      - Evaluate Platform.msgprint(translated “Row #{0}: Stock cannot be reserved for a non-stock Item {1}”.format(item.idx, Platform.bold(item.item\_code)), title = translated “Stock Reservation”, indicator = “yellow”).
    - Evaluate item.db\_set(“reserve\_stock”, 0).
    - Continue with the next iteration or loop test.
  - If Platform.get\_cached\_value(“Warehouse”, item.warehouse, “is\_group”).
    - Evaluate Platform.msgprint(translated “Row #{0}: Stock cannot be reserved in group warehouse {1}.”.format(item.idx, Platform.bold(item.warehouse)), title = translated “Stock Reservation”, indicator = “yellow”).
    - Continue with the next iteration or loop test.
  - Set unreserved\_qty from get\_unreserved\_qty(item, reserved\_qty\_details).
  - If unreserved\_qty ≤ 0.
    - If not from\_voucher\_type.
      - Evaluate Platform.msgprint(translated “Row #{0}: Stock is already reserved for the Item {1}.”.format(item.idx, Platform.bold(item.item\_code)), title = translated “Stock Reservation”, indicator = “yellow”).
    - Continue with the next iteration or loop test.
  - Set available\_qty\_to\_reserve from get\_available\_qty\_to\_reserve(item.item\_code, item.warehouse).
  - <a id="op-59f9d5bf9253a4-guard-113"></a>If available\_qty\_to\_reserve ≤ 0.
    - Evaluate Platform.msgprint(translated “Row #{0}: Stock not available to reserve for the Item {1} in Warehouse {2}.”.format(item.idx, Platform.bold(item.item\_code), Platform.bold(item.warehouse)), title = translated ….
    - Continue with the next iteration or loop test.
  - Set qty\_to\_be\_reserved from min(unreserved\_qty, available\_qty\_to\_reserve).
  - If hasattr(item, “qty\_to\_reserve”).
    - If item.qty\_to\_reserve ≤ 0.
      - Evaluate Platform.msgprint(translated “Row #{0}: Quantity to reserve for the Item {1} should be greater than 0.”.format(item.idx, Platform.bold(item.item\_code)), title = translated “Stock Reservation”, indicator = “orange”).
      - Continue with the next iteration or loop test.
    - Otherwise.
      - Set qty\_to\_be\_reserved from min(qty\_to\_be\_reserved, item.qty\_to\_reserve).
  - Set qty\_to\_be\_reserved from get\_whole\_sales\_unit\_qty(item, qty\_to\_be\_reserved, min(unreserved\_qty, available\_qty\_to\_reserve) when from\_voucher\_type equals “Purchase Receipt”, otherwise no value).
    - Value choice on from\_voucher\_type equals “Purchase Receipt” — true gives min(unreserved\_qty, available\_qty\_to\_reserve), false gives no value.
  - If not qty\_to\_be\_reserved.
    - Continue with the next iteration or loop test.
  - If qty\_to\_be\_reserved &lt; unreserved\_qty.
    - If (not from\_voucher\_type and (not item.get(“qty\_to\_reserve”) or qty\_to\_be\_reserved &lt; flt(item.get(“qty\_to\_reserve”)))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not from\_voucher\_type → (not item.get(“qty\_to\_reserve”) or qty\_to\_be\_reserved &lt; flt(item.get(“qty\_to\_reserve”))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.get(“qty\_to\_reserve”) → qty\_to\_be\_reserved &lt; flt(item.get(“qty\_to\_reserve”)).
      - Set msg from translated “Row #{0}: Only {1} available to reserve for the Item {2}”.format(item.idx, Platform.bold(((str((qty\_to\_be\_reserved ÷ nested operand in the contract.conversion\_factor)) + one space) + item.uom)) ….
      - Evaluate Platform.msgprint(msg, title = translated “Stock Reservation”, indicator = “orange”).
    - If not allow\_partial\_reservation.
      - If qty\_to\_be\_reserved equals flt(item.get(“qty\_to\_reserve”)).
        - Set msg from translated “Enable Allow Partial Reservation in the Stock Settings to reserve partial stock.”.
        - Evaluate Platform.msgprint(msg, title = translated “Partial Stock Reservation”, indicator = “yellow”).
      - Continue with the next iteration or loop test.
  - Set sre from Platform.new\_doc(“Stock Reservation Entry”).
  - Set sre.item\_code from item.item\_code.
  - Set sre.warehouse from item.warehouse.
  - Set sre.has\_serial\_no from has\_serial\_no.
  - Set sre.has\_batch\_no from has\_batch\_no.
  - Set sre.voucher\_type from sales\_order.doctype.
  - Set sre.voucher\_no from sales\_order.name.
  - Set sre.voucher\_detail\_no from item.name.
  - Set sre.available\_qty from available\_qty\_to\_reserve.
  - Set sre.voucher\_qty from item.stock\_qty.
  - Set sre.reserved\_qty from qty\_to\_be\_reserved.
  - Set sre.company from sales\_order.company.
  - Set sre.stock\_uom from item.stock\_uom.
  - Set sre.project from sales\_order.project.
  - If from\_voucher\_type.
    - Set sre.from\_voucher\_type from from\_voucher\_type.
    - Set sre.from\_voucher\_no from item.from\_voucher\_no.
    - Set sre.from\_voucher\_detail\_no from item.from\_voucher\_detail\_no.
  - If item.get(“serial\_and\_batch\_bundle”).
    - Set sre.reservation\_based\_on from “Serial and Batch”.
    - Evaluate set\_reserved\_serial\_batch\_entries(sre, item.serial\_and\_batch\_bundle, qty\_to\_be\_reserved, has\_serial\_no, …).
  - Evaluate sre.save().
  - Evaluate sre.submit().
  - Update sre\_count using + 1.
- If (sre\_count and notify).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sre\_count → notify.
  - Evaluate Platform.msgprint(translated “Stock Reservation Entries Created”, alert = true, indicator = “green”).
- Return sre\_count.

**Derived branch illustrations**

- At the comparison available\_qty\_to\_reserve ≤ 0, available\_qty\_to\_reserve = 0 selects the branch that requests a message with translated “Row #{0}: Stock not available to reserve for the Item {1} in Warehouse {2}.”.format(item.idx, Platform.bold(item.item\_cod …. With available\_qty\_to\_reserve = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-59f9d5bf9253a4-guard-113)

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, sales\_order.set\_warehouse, “is\_group”), Platform.get\_single\_value(“Stock Settings”, “allow\_partial\_reservation”) and 2 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1145)

<a id="op-6571b90016992e"></a>
### Set reserved serial batch entries

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_set_reserved_serial_batch_entries`

**Inputs** sre, bundle, qty\_to\_reserve, has\_serial\_no, has\_batch\_no.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**Local steps**

- Set picked\_qty from 0.
- For each entry in Platform.get\_doc(“Serial and Batch Bundle”, bundle).entries.
  - If picked\_qty ≥ qty\_to\_reserve.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set qty from 1 when has\_serial\_no, otherwise min(abs(entry.qty), (qty\_to\_reserve − picked\_qty)).
    - Value choice on has\_serial\_no — true gives 1, false gives min(abs(entry.qty), (qty\_to\_reserve − picked\_qty)).
  - Evaluate sre.append(“sb\_entries”, mapping(“serial\_no” → entry.serial\_no, “batch\_no” → entry.batch\_no, “qty” → qty, “warehouse” → entry.warehouse)).
  - Update picked\_qty using + qty.
- If picked\_qty &lt; qty\_to\_reserve.
  - Evaluate add\_available\_serial\_batch\_entries(sre, (qty\_to\_reserve − picked\_qty), has\_serial\_no, has\_batch\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L824)

<a id="op-4a0dac7b56916d"></a>
### Add available serial batch entries

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_add_available_serial_batch_entries`

**Inputs** sre, qty\_needed, has\_serial\_no, has\_batch\_no.

**Local steps**

- If has\_serial\_no.
  - Evaluate add\_available\_serial\_entries(sre, qty\_needed, has\_batch\_no).
- Otherwise.
  - Evaluate add\_available\_batch\_entries(sre, qty\_needed).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1312) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L809)

<a id="op-a02d71d18a87f8"></a>
### Add available serial entries

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_add_available_serial_entries`

**Inputs** sre, qty\_needed, has\_batch\_no.

**Explicit results** no value.

**Local steps**

- Set taken from set of row.serial\_no for row drawn from sre.sb\_entries.
  - Draw row from sre.sb\_entries.
- For each serial in get\_available\_serial\_nos\_to\_reserve(sre.item\_code, sre.warehouse, has\_batch\_no).
  - <a id="op-a02d71d18a87f8-guard-4"></a>If qty\_needed ≤ 0.
    - Return no value.
  - If serial at 0 belongs to taken.
    - Continue with the next iteration or loop test.
  - Set batch\_no from serial at 2 when (has\_batch\_no and len(serial) &gt; 2), otherwise no value.
    - Value choice on (has\_batch\_no and len(serial) &gt; 2) — true gives serial at 2, false gives no value.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_batch\_no → len(serial) &gt; 2.
  - Evaluate sre.append(“sb\_entries”, mapping(“serial\_no” → serial at 0, “batch\_no” → batch\_no, “qty” → 1, “warehouse” → sre.warehouse)).
  - Update qty\_needed using − 1.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison qty\_needed ≤ 0, qty\_needed = 0 selects the branch that returns no value. With qty\_needed = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-a02d71d18a87f8-guard-4)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1313) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L810)

<a id="op-dbbeec3409ded4"></a>
### Add available batch entries

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_add_available_batch_entries`

**Inputs** sre, qty\_needed.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_auto\_batch\_nos.
- Set taken from mapping().
- For each row in sre.sb\_entries.
  - Set taken at row.batch\_no from (taken.get(row.batch\_no, 0) + flt(row.qty)).
- For each batch in get\_auto\_batch\_nos(Platform.\_dict(item\_code = sre.item\_code, warehouse = sre.warehouse)).
  - Set qty from min((flt(batch.qty) − taken.get(batch.batch\_no, 0)), qty\_needed).
  - <a id="op-dbbeec3409ded4-guard-10"></a>If qty ≤ 0.
    - Continue with the next iteration or loop test.
  - If existing bound to next(generator of row for row drawn from sre.sb\_entries where row.batch\_no equals batch.batch\_no, no value).
    - Draw row from sre.sb\_entries, keep a combination only if (row.batch\_no equals batch.batch\_no).
    - Set existing.qty from (flt(existing.qty) + qty).
  - Otherwise.
    - Evaluate sre.append(“sb\_entries”, mapping(“batch\_no” → batch.batch\_no, “qty” → qty, “warehouse” → sre.warehouse)).
  - Update qty\_needed using − qty.
  - <a id="op-dbbeec3409ded4-guard-18"></a>If qty\_needed ≤ 0.
    - Return no value.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison qty ≤ 0, qty = 0 selects the branch that continues with the next loop iteration. With qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-dbbeec3409ded4-guard-10)
- At the comparison qty\_needed ≤ 0, qty\_needed = 0 selects the branch that returns no value. With qty\_needed = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-dbbeec3409ded4-guard-18)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1311) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L808)

<a id="op-d0d90f51e66f67"></a>
### Cancel stock reservation entries

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_cancel_stock_reservation_entries`

**Inputs** voucher\_type = no value, voucher\_no = no value, voucher\_detail\_no = no value, from\_voucher\_type = no value, from\_voucher\_no = no value, from\_voucher\_detail\_no = no value, sre\_list = no value, notify = true.

**Declared result** no value.

**Record and data access** resolve a document from “Stock Reservation Entry” via get\_doc.

**State and service calls** call cancel on Platform.get\_doc(“Stock Reservation Entry”, sre) · msgprint with msg.

**Local steps**

- If not sre\_list.
  - Set sre\_list from mapping().
  - If (voucher\_type and voucher\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_type → voucher\_no.
    - Set sre\_list from \_get\_stock\_reservation\_entries\_for\_voucher(voucher\_type, voucher\_no, voucher\_detail\_no, fields = list(“name”)).
  - Otherwise.
    - If (from\_voucher\_type and from\_voucher\_no).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_voucher\_type → from\_voucher\_no.
      - Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
      - Set query from nested operand in the contract(nested operand in the contract).select(sre.name).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equa ….
      - If from\_voucher\_detail\_no.
        - Set query from query.where(sre.from\_voucher\_detail\_no equals from\_voucher\_detail\_no).
      - Set sre\_list from query.run(as\_dict = true).
  - Set sre\_list from list of d.name for d drawn from sre\_list.
    - Draw d from sre\_list.
- If sre\_list.
  - For each sre in sre\_list.
    - Evaluate Platform.get\_doc(“Stock Reservation Entry”, sre).cancel().
  - If notify.
    - Set msg from translated “Stock Reservation Entries Cancelled”.
    - Evaluate Platform.msgprint(msg, alert = true, indicator = “red”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0872.json#L5822) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1144)

<a id="op-e174e205dbbc8d"></a>
### Get stock reservation entries for voucher

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_stock_reservation_entries_for_voucher`

**Inputs** voucher\_type, voucher\_no, voucher\_detail\_no = no value, fields = no value, ignore\_status = false.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** \_get\_stock\_reservation\_entries\_for\_voucher(voucher\_type, voucher\_no, voucher\_detail\_no, fields, ignore\_permissions = false, …).

**Local steps**

- Return \_get\_stock\_reservation\_entries\_for\_voucher(voucher\_type, voucher\_no, voucher\_detail\_no, fields, ignore\_permissions = false, …).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0872.json#L6655) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1150)

<a id="op-6dfcba69fbdaa4"></a>
### Get stock reservation entries for voucher

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_stock_reservation_entries_for_voucher_2`

**Inputs** voucher\_type, voucher\_no, voucher\_detail\_no = no value, fields = no value, ignore\_status = false, ignore\_permissions = true.

**Declared result** list at dict.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- If (not fields or not isinstance(fields, list)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not fields → not isinstance(fields, list).
  - Set fields from list(“name”, “item\_code”, “warehouse”, “voucher\_detail\_no”, …).
- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set query from Platform.get\_query(sre, fields = fields, ignore\_permissions = ignore\_permissions).where(((nested operand in the contract.docstatus equals 1 bitwise and nested operand in the contract.voucher\_type equals vo ….
- If voucher\_detail\_no.
  - Set query from query.where(sre.voucher\_detail\_no equals voucher\_detail\_no).
- If ignore\_status.
  - Set query from query.where(sre.delivered\_qty &lt; sre.reserved\_qty).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1151)

<a id="op-ba34094eeb33ba"></a>
### Get serial batch open qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_get_serial_batch_open_qty`

**Inputs** sre\_names.

**Declared result** dict at tuple(str, float).

**Explicit results** mapping() · open\_qty.

**Local steps**

- If not sre\_names.
  - Return mapping().
- Set sb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set open\_qty from defaultdict(float).
- For each tuple(parent, qty) in nested operand in the contract(nested operand in the contract, nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the  …().run().
  - Update open\_qty at parent using + flt(qty).
- Return open\_qty.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1320) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L817)

<a id="op-65284b5abacd69"></a>
### Set delivered qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_set_delivered_qty`

**Inputs** sre, delivered\_qty.

**Declared result** no value.

**State and service calls** request set\_value on “Stock Reservation Entry”.

**Local steps**

- Set sre.delivered\_qty from delivered\_qty.
- Evaluate Platform.db.set\_value(“Stock Reservation Entry”, sre.name, mapping(“delivered\_qty” → delivered\_qty, “status” → get\_status(sre))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L823)

<a id="op-5b564e18c385c1"></a>
### Get status

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_get_status`

**Inputs** sre.

**Declared result** str.

**Explicit results** “Cancelled” · “Draft” · “Partially Used” when sre.transferred\_qty &lt; sre.reserved\_qty, otherwise “Closed” · “Delivered” · “Partially Delivered” · 3 additional forms in the steps below.

**Local steps**

- <a id="op-5b564e18c385c1-guard-3"></a>If sre.docstatus equals 2.
  - Return “Cancelled”.
- <a id="op-5b564e18c385c1-guard-5"></a>If sre.docstatus differs from 1.
  - Return “Draft”.
- If sre.transferred\_qty.
  - Return “Partially Used” when sre.transferred\_qty &lt; sre.reserved\_qty, otherwise “Closed”.
    - Value choice on sre.transferred\_qty &lt; sre.reserved\_qty — true gives “Partially Used”, false gives “Closed”.
- If (flt(sre.delivered\_qty) + flt(sre.consumed\_qty)) ≥ flt(sre.reserved\_qty).
  - Return “Delivered”.
- If sre.delivered\_qty.
  - Return “Partially Delivered”.
- If sre.consumed\_qty.
  - Return “Partially Used”.
- Set precision from Platform.get\_precision(“Stock Reservation Entry”, “reserved\_qty”).
- If flt(sre.reserved\_qty, precision) ≥ flt(sre.voucher\_qty, precision).
  - Return “Reserved”.
- Return “Partially Reserved”.

**Derived branch illustrations**

- At the comparison sre.docstatus equals 2, sre.docstatus = 2 (cancelled) selects the branch that returns “Cancelled”. With sre.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-5b564e18c385c1-guard-3)
- At the comparison sre.docstatus differs from 1, sre.docstatus = 0 (draft) selects the branch that returns “Draft”. With sre.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-5b564e18c385c1-guard-5)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1322) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L819)

<a id="op-2cf94ff83e571c"></a>
### Move serial batch delivered qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_move_serial_batch_delivered_qty`

**Inputs** limits, serial\_batch, release = false.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not limits.
  - Return no value.
- Set entries from get\_open\_serial\_batch\_entries(list(limits), release).
- Set moved\_qty from allocate\_serial\_batch\_qty(entries, limits, serial\_batch).
- Evaluate add\_serial\_batch\_delivered\_qty(mapping of name → negative qty when release, otherwise qty for tuple(name, qty) drawn from moved\_qty.items()).
  - Draw tuple(name, qty) from moved\_qty.items().
  - Value choice on release — true gives negative qty, false gives qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1324) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L821)
