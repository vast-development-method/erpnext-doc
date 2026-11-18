# Inventory and warehouses · operations 101

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock reservation entry

[Record definition](../../../../data/record-types/stock_reservation_entry.json)

<a id="op-da43635c420173"></a>
### Stock Reservation Entry.update unreserved qty in sre

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_update_unreserved_quantity_in_stock_reservation_entry`

**Inputs** self.

**Local steps**

- If self.voucher\_type differs from “Delivery Note”.
  - Evaluate self.give\_back\_to\_from\_voucher(self.get\_serial\_batch\_entries()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [give back to from voucher](operations-101.md#op-ffa447355936dc), [get serial batch entries](operations-101.md#op-96ca8519ec8471).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L263) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1177)

<a id="op-ffa447355936dc"></a>
### Stock Reservation Entry.give back to from voucher

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_give_back_to_from_voucher`

**Inputs** self, released.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not (self.from\_voucher\_type and self.from\_voucher\_detail\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_voucher\_type → self.from\_voucher\_detail\_no.
  - Return no value.
- If (self.has\_batch\_no or self.has\_serial\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_batch\_no → self.has\_serial\_no.
  - Evaluate self.give\_back\_serial\_batch(released).
- Evaluate self.update\_delivered\_qty\_in\_from\_voucher\_reservations().

If control reaches the end, it returns no value.

**Methods declared on this owner** [give back serial batch](operations-101.md#op-761a9af78effbe), [update delivered qty in from voucher reservations](operations-101.md#op-b32fa49037ed30).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L831)

<a id="op-b32fa49037ed30"></a>
### Stock Reservation Entry.update delivered qty in from voucher reservations

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_update_delivered_qty_in_from_voucher_reservations`

**Inputs** self.

**Record and data access** resolve a document from “Bin” via get\_cached\_doc.

**Local steps**

- Set sres from self.get\_from\_voucher\_reservation\_entries().
- Set open\_qty from get\_serial\_batch\_open\_qty(list of row.name for row drawn from sres).
  - Draw row from sres.
- Set counted\_qty from 0.0.
- For each row in sres.
  - If row.name belongs to open\_qty.
    - Set delivered\_qty from (row.reserved\_qty − open\_qty at row.name).
    - Evaluate set\_delivered\_qty(row, delivered\_qty).
    - Update counted\_qty using + delivered\_qty.
- Evaluate self.spread\_used\_qty(list of row for row drawn from sres where row.name does not belong to open\_qty, counted\_qty).
  - Draw row from sres, keep a combination only if (row.name does not belong to open\_qty).
- For each warehouse in set of row.warehouse for row drawn from sres.
  - Draw row from sres.
  - Evaluate Platform.get\_cached\_doc(“Bin”, get\_or\_make\_bin(self.item\_code, warehouse)).update\_reserved\_stock().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get from voucher reservation entries](operations-101.md#op-92368ba63a361a), [spread used qty](operations-101.md#op-a4d5b8a261ef0c).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Bin”, get\_or\_make\_bin(self.item\_code, warehouse)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L836)

<a id="op-a4d5b8a261ef0c"></a>
### Stock Reservation Entry.spread used qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_spread_used_qty`

**Inputs** self, sres, counted\_qty = 0.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not sres.
  - Return no value.
- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set used\_qty from ((sre.delivered\_qty + sre.transferred\_qty) + sre.consumed\_qty).
- Set delivered\_qty from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run(as\_list = true) at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … → 0.
- Set delivered\_qty from max((delivered\_qty − counted\_qty), 0).
- For each row in sres.
  - Set qty from min(row.reserved\_qty, delivered\_qty).
  - Evaluate set\_delivered\_qty(row, qty).
  - Update delivered\_qty using − qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L835)

<a id="op-9c080773178c7e"></a>
### Stock Reservation Entry.release reversed usage

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_release_reversed_usage`

**Inputs** self, field, row\_wise\_serial\_batch.

**Declared result** no value.

**State and service calls** call db\_set on self.

**Local steps**

- If ((self.has\_batch\_no or self.has\_serial\_no) and self.reservation\_based\_on equals “Serial and Batch”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.has\_batch\_no or self.has\_serial\_no) → self.reservation\_based\_on equals “Serial and Batch”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_batch\_no → self.has\_serial\_no.
  - Set before from self.get\_delivered\_serial\_batch\_entries().
  - Evaluate self.consume\_serial\_batch\_for\_material\_transfer(row\_wise\_serial\_batch).
  - Evaluate self.db\_set(field, self.matched\_serial\_batch\_qty, update\_modified = false).
  - Set after from self.get\_delivered\_serial\_batch\_entries().
  - Set released from Platform.\_dict(serial\_nos = list of serial\_no for serial\_no drawn from before.serial\_nos where serial\_no does not belong to after.serial\_nos, batches = mapping of batch\_no → (qty − after.batches at batch\_n ….
    - Draw serial\_no from before.serial\_nos, keep a combination only if (serial\_no does not belong to after.serial\_nos).
    - Draw tuple(batch\_no, qty) from before.batches.items().
  - Evaluate self.give\_back\_serial\_batch(released).
- Evaluate self.update\_delivered\_qty\_in\_from\_voucher\_reservations().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get delivered serial batch entries](operations-101.md#op-7c4632c345df92), [consume serial batch for material transfer](operations-102.md#op-1bdc347167bc81), [give back serial batch](operations-101.md#op-761a9af78effbe), [update delivered qty in from voucher reservations](operations-101.md#op-b32fa49037ed30).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L834)

<a id="op-761a9af78effbe"></a>
### Stock Reservation Entry.give back serial batch

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_give_back_serial_batch`

**Inputs** self, released.

**Declared result** no value.

**Local steps**

- Set sources from self.get\_from\_voucher\_reservation\_entries().
- Evaluate move\_serial\_batch\_delivered\_qty(mapping of row.name → row.delivered\_qty for row drawn from sources, released, release = true).
  - Draw row from sources.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get from voucher reservation entries](operations-101.md#op-92368ba63a361a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L830)

<a id="op-7c4632c345df92"></a>
### Stock Reservation Entry.get delivered serial batch entries

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_get_delivered_serial_batch_entries`

**Inputs** self.

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(mapping(“serial\_nos” → serial\_nos, “batches” → batches)).

**Local steps**

- Set serial\_nos from list().
- Set batches from defaultdict(float).
- For each entry in self.sb\_entries.
  - If (entry.serial\_no and flt(entry.delivered\_qty)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.serial\_no → flt(entry.delivered\_qty).
    - Evaluate serial\_nos.append(entry.serial\_no).
  - Otherwise.
    - If entry.batch\_no.
      - Update batches at entry.batch\_no using + flt(entry.delivered\_qty).
- Return Platform.\_dict(mapping(“serial\_nos” → serial\_nos, “batches” → batches)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L827)

<a id="op-96ca8519ec8471"></a>
### Stock Reservation Entry.get serial batch entries

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_get_serial_batch_entries`

**Inputs** self.

**Explicit results** Platform.\_dict(mapping(“serial\_nos” → serial\_nos, “batches” → batches)).

**Local steps**

- Set serial\_nos from list().
- Set batches from defaultdict(float).
- For each entry in self.sb\_entries.
  - If entry.serial\_no.
    - If (flt(entry.qty) and not flt(entry.delivered\_qty)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(entry.qty) → not flt(entry.delivered\_qty).
      - Evaluate serial\_nos.append(entry.serial\_no).
  - Otherwise.
    - If entry.batch\_no.
      - Update batches at entry.batch\_no using + (flt(entry.qty) − flt(entry.delivered\_qty)).
- Return Platform.\_dict(mapping(“serial\_nos” → serial\_nos, “batches” → batches)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L253) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1168)

<a id="op-92368ba63a361a"></a>
### Stock Reservation Entry.get from voucher reservation entries

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_get_from_voucher_reservation_entries`

**Inputs** self.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(sre.creation).for\_update().run(as\_dict = true).

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Return nested operand in the contract(nested operand in the contract).orderby(sre.creation).for\_update().run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L252) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1167)

<a id="op-cce17b2b04cc68"></a>
### Stock Reservation Entry.validate amended doc

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_validate_amended_record`

**Inputs** self.

**Declared result** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If self.amended\_from.
  - Set msg from translated “Cannot amend {0} {1}, please create a new one instead.”.format(self.doctype, Platform.bold(self.amended\_from)).
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0868.json#L1662) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L265) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1179)

<a id="op-7f404ac15e3167"></a>
### Stock Reservation Entry.validate mandatory

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_validate_mandatory`

**Inputs** self.

**Declared result** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set mandatory from list(“item\_code”, “warehouse”, “voucher\_type”, “voucher\_no”, …).
- For each d in mandatory.
  - If not self.get(d).
    - Set msg from translated “{0} is required”.format(translated self.meta.get\_label(d)).
    - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L267) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1181)

<a id="op-be75e5975a4ff1"></a>
### Stock Reservation Entry.validate group warehouse

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_validate_group_warehouse`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Warehouse” via get\_cached\_value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If Platform.get\_cached\_value(“Warehouse”, self.warehouse, “is\_group”).
  - Set msg from translated “Stock cannot be reserved in group warehouse {0}.”.format(Platform.bold(self.warehouse)).
  - Call the validation error handler Platform.throw(msg, title = translated “Invalid Warehouse”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, self.warehouse, “is\_group”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0868.json#L2075) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L266) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1180)

<a id="op-9cb77aa8d87765"></a>
### Stock Reservation Entry.validate uom is integer

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_validate_unit_of_measure_is_integer`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “UOM” via get\_value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If cint(Platform.db.get\_value(“UOM”, self.stock\_uom, “must\_be\_whole\_number”, cache = true)).
  - If cint(self.reserved\_qty) differs from flt(self.reserved\_qty, self.precision(“reserved\_qty”)).
    - Set msg from translated “Reserved Qty ({0}) cannot be a fraction. To allow this, disable '{1}' in UOM {2}.”.format(flt(self.reserved\_qty, self.precision(“reserved\_qty”)), Platform.bold(translated “Must be Whole Number” ….
    - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0868.json#L2269) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L271) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1185)

<a id="op-18eb9b009fa026"></a>
### Stock Reservation Entry.set reservation based on

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_set_reservation_based_on`

**Inputs** self.

**Declared result** no value.

**State and service calls** call db\_set on self.

**Local steps**

- If (self.reservation\_based\_on equals “Serial and Batch” and (not self.has\_serial\_no and not self.has\_batch\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reservation\_based\_on equals “Serial and Batch” → (not self.has\_serial\_no and not self.has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_serial\_no → not self.has\_batch\_no.
  - Evaluate self.db\_set(“reservation\_based\_on”, “Qty”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0868.json#L2624) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L258) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1172)

<a id="op-e16f6b8905319e"></a>
### Stock Reservation Entry.validate reservation based on qty

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_validate_reservation_based_on_quantity`

**Inputs** self.

**Declared result** no value.

**Local steps**

- If (self.reservation\_based\_on equals “Qty” and self.voucher\_type differs from “Subcontracting Inward Order”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reservation\_based\_on equals “Qty” → self.voucher\_type differs from “Subcontracting Inward Order”.
  - Evaluate self.validate\_with\_allowed\_qty(self.reserved\_qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate with allowed qty](operations-101.md#op-36a3b15be829e2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0868.json#L2749) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L268) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1182)

<a id="op-cfb4586cbbe416"></a>
### Stock Reservation Entry.auto reserve serial and batch

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_auto_reserve_serial_and_batch`

**Inputs** self, based\_on = no value.

**Declared result** no value.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- If (not self.from\_voucher\_type and self.get(“\_action”) equals “submit” and (self.has\_serial\_no or self.has\_batch\_no) and Platform.get\_single\_value(“Stock Settings”, “auto\_reserve\_serial\_and\_batch”) and not se ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.from\_voucher\_type → self.get(“\_action”) equals “submit” → (self.has\_serial\_no or self.has\_batch\_no) → Platform.get\_single\_value(“Stock Settings”, “auto\_reserve\_serial\_and\_batch”) → not self.sb\_entries.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_serial\_no → self.has\_batch\_no.
  - Bind dependencies get\_available\_batches.
  - Bind dependencies get\_serial\_nos\_for\_outward.
  - Bind dependencies get\_serial\_nos\_batch.
  - Set self.reservation\_based\_on from “Serial and Batch”.
  - Evaluate self.sb\_entries.clear().
  - Set kwargs from Platform.\_dict(mapping(“item\_code” → self.item\_code, “warehouse” → self.warehouse, “qty” → (abs(self.reserved\_qty) or 0), “based\_on” → (based\_on or Platform.get\_single\_value(“Stock Settings”, “pick\_serial\_ ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in abs(self.reserved\_qty) → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in based\_on → Platform.get\_single\_value(“Stock Settings”, “pick\_serial\_and\_batch\_based\_on”).
  - Set tuple(serial\_nos, batch\_nos) from tuple(list(), list()).
  - If self.has\_serial\_no.
    - Set serial\_nos from get\_serial\_nos\_for\_outward(kwargs).
  - If self.has\_batch\_no.
    - Set batch\_nos from get\_available\_batches(kwargs).
  - If serial\_nos.
    - Set serial\_no\_wise\_batch from Platform.\_dict(mapping()).
    - If self.has\_batch\_no.
      - Set serial\_no\_wise\_batch from get\_serial\_nos\_batch(serial\_nos).
    - For each serial\_no in serial\_nos.
      - Evaluate self.append(“sb\_entries”, mapping(“serial\_no” → serial\_no, “qty” → 1, “batch\_no” → serial\_no\_wise\_batch.get(serial\_no), “warehouse” → self.warehouse)).
  - Otherwise.
    - If batch\_nos.
      - For each tuple(batch\_no, batch\_qty) in batch\_nos.items().
        - Evaluate self.append(“sb\_entries”, mapping(“batch\_no” → batch\_no, “qty” → batch\_qty, “warehouse” → self.warehouse)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “auto\_reserve\_serial\_and\_batch”), Platform.get\_single\_value(“Stock Settings”, “pick\_serial\_and\_batch\_based\_on”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1162)

<a id="op-dafb12e7514c83"></a>
### Stock Reservation Entry.validate reservation based on serial and batch

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_validate_reservation_based_on_serial_and_batch`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Batch” via get\_value.

**State and service calls** call db\_update on entry · call db\_set on self.

**Explicit results** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set is\_production\_voucher from self.voucher\_type belongs to list(“Work Order”, “Subcontracting Order”).
- If is\_production\_voucher.
  - If self.from\_voucher\_type.
    - Return no value.
  - Evaluate self.validate\_with\_allowed\_qty(self.reserved\_qty).
  - If not self.sb\_entries.
    - Return no value.
- If self.reservation\_based\_on equals “Serial and Batch”.
  - Set allow\_partial\_reservation from Platform.get\_single\_value(“Stock Settings”, “allow\_partial\_reservation”).
  - Set available\_serial\_nos from list().
  - If self.has\_serial\_no.
    - Set available\_serial\_nos from get\_available\_serial\_nos\_to\_reserve(self.item\_code, self.warehouse, self.has\_batch\_no, ignore\_sre = self.name).
    - If not available\_serial\_nos.
      - Set msg from translated “Stock not available for Item {0} in Warehouse {1}.”.format(Platform.bold(self.item\_code), Platform.bold(self.warehouse)).
      - Call the validation error handler Platform.throw(msg).
  - Set qty\_to\_be\_reserved from 0.
  - Set tuple(selected\_batch\_nos, selected\_serial\_nos) from tuple(list(), list()).
  - For each entry in self.sb\_entries.
    - Set entry.warehouse from self.warehouse.
    - If self.has\_serial\_no.
      - Set entry.qty from 1.
      - Set key from tuple(entry.serial\_no, self.warehouse, entry.batch\_no) when self.has\_batch\_no, otherwise tuple(entry.serial\_no, self.warehouse).
        - Value choice on self.has\_batch\_no — true gives tuple(entry.serial\_no, self.warehouse, entry.batch\_no), false gives tuple(entry.serial\_no, self.warehouse).
      - If key does not belong to available\_serial\_nos.
        - Set msg from translated “Row #{0}: Serial No {1} for Item {2} is not available in {3} {4} or might be reserved in another {5}.”.format(entry.idx, Platform.bold(entry.serial\_no), Platform.bold(self.item\_code), translate ….
          - Value choice on self.has\_batch\_no — true gives translated “Batch {0} and Warehouse”.format(Platform.bold(entry.batch\_no)), false gives translated “Warehouse”.
        - Call the validation error handler Platform.throw(msg).
      - If entry.serial\_no belongs to selected\_serial\_nos.
        - Set msg from translated “Row #{0}: Serial No {1} is already selected.”.format(entry.idx, Platform.bold(entry.serial\_no)).
        - Call the validation error handler Platform.throw(msg).
      - Otherwise.
        - Evaluate selected\_serial\_nos.append(entry.serial\_no).
    - Otherwise.
      - If self.has\_batch\_no.
        - If cint(Platform.db.get\_value(“Batch”, entry.batch\_no, “disabled”)).
          - Set msg from translated “Row #{0}: Stock cannot be reserved for Item {1} against a disabled Batch {2}.”.format(entry.idx, Platform.bold(self.item\_code), Platform.bold(entry.batch\_no)).
          - Call the validation error handler Platform.throw(msg).
        - Set available\_qty\_to\_reserve from get\_available\_qty\_to\_reserve(self.item\_code, self.warehouse, entry.batch\_no, ignore\_sre = self.name).
        - If available\_qty\_to\_reserve ≤ 0.
          - Set msg from translated “Row #{0}: Stock not available to reserve for Item {1} against Batch {2} in Warehouse {3}.”.format(entry.idx, Platform.bold(self.item\_code), Platform.bold(entry.batch\_no), Platform.bold(self.warehouse)).
          - Call the validation error handler Platform.throw(msg).
        - If entry.qty &gt; available\_qty\_to\_reserve.
          - If allow\_partial\_reservation.
            - Set entry.qty from available\_qty\_to\_reserve.
            - If self.get(“\_action”) equals “update\_after\_submit”.
              - Evaluate entry.db\_update().
          - Otherwise.
            - Set msg from translated “Row #{0}: Qty should be less than or equal to Available Qty to Reserve (Actual Qty - Reserved Qty) {1} for I …”.format(entry.idx, Platform.bold(available\_qty\_to\_reserve), Platform.bold(self.ite ….
            - Call the validation error handler Platform.throw(msg).
        - If entry.batch\_no belongs to selected\_batch\_nos.
          - Set msg from translated “Row #{0}: Batch No {1} is already selected.”.format(entry.idx, Platform.bold(entry.batch\_no)).
          - Call the validation error handler Platform.throw(msg).
        - Otherwise.
          - Evaluate selected\_batch\_nos.append(entry.batch\_no).
    - Update qty\_to\_be\_reserved using + entry.qty.
  - If not qty\_to\_be\_reserved.
    - Set msg from translated “Please select Serial/Batch Nos to reserve or change Reservation Based On to Qty.”.
    - Call the validation error handler Platform.throw(msg).
  - If is\_production\_voucher.
    - Return no value.
  - If self.voucher\_type differs from “Subcontracting Inward Order”.
    - Evaluate self.validate\_with\_allowed\_qty(qty\_to\_be\_reserved).
  - Evaluate self.db\_set(“reserved\_qty”, qty\_to\_be\_reserved).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate with allowed qty](operations-101.md#op-36a3b15be829e2).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_partial\_reservation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L269) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1183)

<a id="op-afeacd6d58a62e"></a>
### Stock Reservation Entry.update reserved qty in voucher

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_update_reserved_quantity_in_voucher`

**Inputs** self, reserved\_qty\_field = “stock\_reserved\_qty”, update\_modified = true.

**Declared result** no value.

**Record and data access** read “Material Request Plan Item” via exists.

**State and service calls** request set\_value on item\_doctype.

**Local steps**

- Set item\_doctype from mapping(“Sales Order” → “Sales Order Item”, “Work Order” → “Work Order Item”, “Production Plan” → “Production Plan Sub Assembly Item”, “Subcontracting Order” → “Subcontracting Order Supplied Item”).get(sel ….
- If item\_doctype.
  - Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
  - Set reserved\_qty from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run(as\_list = true) at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … → 0.
  - If (self.voucher\_type equals “Production Plan” and Platform.db.exists(“Material Request Plan Item”, self.voucher\_detail\_no)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Production Plan” → Platform.db.exists(“Material Request Plan Item”, self.voucher\_detail\_no).
    - Set item\_doctype from “Material Request Plan Item”.
  - Evaluate Platform.db.set\_value(item\_doctype, self.voucher\_detail\_no, reserved\_qty\_field, reserved\_qty, update\_modified = update\_modified).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0869.json#L2059) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L260) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1174)

<a id="op-51a2afd185d538"></a>
### Stock Reservation Entry.update reserved qty in pick list

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_update_reserved_quantity_in_pick_list`

**Inputs** self, reserved\_qty\_field = “stock\_reserved\_qty”, update\_modified = true.

**Declared result** no value.

**State and service calls** request set\_value on “Pick List Item”.

**Local steps**

- If (self.from\_voucher\_type equals “Pick List” and self.from\_voucher\_no and self.from\_voucher\_detail\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_voucher\_type equals “Pick List” → self.from\_voucher\_no → self.from\_voucher\_detail\_no.
  - Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
  - Set reserved\_qty from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run(as\_list = true) at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … → 0.
  - Evaluate Platform.db.set\_value(“Pick List Item”, self.from\_voucher\_detail\_no, reserved\_qty\_field, reserved\_qty, update\_modified = update\_modified).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0869.json#L2703) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L259) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1173)

<a id="op-e936824e5f0652"></a>
### Stock Reservation Entry.update reserved stock in bin

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_update_reserved_stock_in_bin`

**Inputs** self.

**Declared result** no value.

**Record and data access** resolve a document from “Bin” via get\_cached\_doc.

**Local steps**

- Set bin\_name from get\_or\_make\_bin(self.item\_code, self.warehouse).
- Set bin\_doc from Platform.get\_cached\_doc(“Bin”, bin\_name).
- Evaluate bin\_doc.update\_reserved\_stock().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Bin”, bin\_name).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0869.json#L3147) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L261) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1175)

<a id="op-ed9ab6c42d5f4a"></a>
### Stock Reservation Entry.update status

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_update_status`

**Inputs** self, status = no value, update\_modified = true.

**Declared result** no value.

**State and service calls** request set\_value on self.doctype.

**Local steps**

- Evaluate Platform.db.set\_value(self.doctype, self.name, “status”, (status or get\_status(self)), update\_modified = update\_modified).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in status → get\_status(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L262) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1176)

<a id="op-dfaebf87433070"></a>
### Stock Reservation Entry.can be updated

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_can_be_updated`

**Inputs** self.

**Declared result** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If self.status belongs to tuple(“Partially Delivered”, “Delivered”).
  - Set msg from translated “{0} {1} cannot be updated. If you need to make changes, we recommend canceling the existing entry and creati …”.format(self.status, self.doctype).
  - Call the validation error handler Platform.throw(msg).
- If self.from\_voucher\_type equals “Pick List”.
  - Set msg from translated “Stock Reservation Entry created against a Pick List cannot be updated. If you need to make changes, we recom …”.
  - Call the validation error handler Platform.throw(msg).
- If self.delivered\_qty &gt; 0.
  - Set msg from translated “Stock Reservation Entry cannot be updated as it has been delivered.”.
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0869.json#L3746) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1165)

<a id="op-36a3b15be829e2"></a>
### Stock Reservation Entry.validate with allowed qty

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_validate_with_allowed_quantity`

**Inputs** self, qty\_to\_be\_reserved.

**Declared result** no value.

**Record and data access** read “Sales Order Item” via exists · read “Packed Item” via get\_value · read “Sales Order Item” via get\_value.

**State and service calls** call db\_set on self · call cancel on self · msgprint with msg.

**Explicit results** Platform.msgprint(msg).

**Explicit failure paths** validation helper — msg.

**Local steps**

- Evaluate self.db\_set(“available\_qty”, get\_available\_qty\_to\_reserve(self.item\_code, self.warehouse, ignore\_sre = self.name)).
- Set total\_reserved\_qty from self.get\_total\_reserved\_qty().
- Set voucher\_delivered\_qty from 0.
- If self.voucher\_type equals “Sales Order”.
  - Set voucher\_detail\_no from self.voucher\_detail\_no.
  - Set is\_packed\_item from not Platform.db.exists(“Sales Order Item”, self.voucher\_detail\_no).
  - If is\_packed\_item.
    - Set voucher\_detail\_no from Platform.get\_value(“Packed Item”, self.voucher\_detail\_no, “parent\_detail\_docname”).
  - Set tuple(delivered\_qty, conversion\_factor, stock\_qty) from Platform.db.get\_value(“Sales Order Item”, voucher\_detail\_no, list(“delivered\_qty”, “conversion\_factor”, “stock\_qty”)).
  - Set voucher\_delivered\_qty from (flt(delivered\_qty) × flt(conversion\_factor)).
  - If is\_packed\_item.
    - Update voucher\_delivered\_qty using × (flt(self.voucher\_qty) ÷ (flt(stock\_qty) or 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(stock\_qty) → 1.
- Set allowed\_qty from min(self.available\_qty, ((self.voucher\_qty − voucher\_delivered\_qty) − total\_reserved\_qty)).
- Set allowed\_qty from flt(allowed\_qty, self.precision(“reserved\_qty”)).
- Set qty\_to\_be\_reserved from flt(qty\_to\_be\_reserved, self.precision(“reserved\_qty”)).
- If (self.get(“\_action”) differs from “submit” and self.voucher\_type equals “Sales Order” and allowed\_qty ≤ 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“\_action”) differs from “submit” → self.voucher\_type equals “Sales Order” → allowed\_qty ≤ 0.
  - Set msg from translated “Item {0} is already reserved/delivered against Sales Order {1}.”.format(Platform.bold(self.item\_code), Platform.bold(self.voucher\_no)).
  - If self.docstatus equals 1.
    - Evaluate self.cancel().
    - Return Platform.msgprint(msg).
  - Otherwise.
    - Call the validation error handler Platform.throw(msg).
- If qty\_to\_be\_reserved &gt; allowed\_qty.
  - Set actual\_qty from \_get\_stock\_balance(self.item\_code, self.warehouse).
  - Set msg from multiline text in the contract.format(Platform.bold(allowed\_qty), self.stock\_uom, Platform.bold(self.item\_code), self.voucher\_type, …).
  - Call the validation error handler Platform.throw(msg).
- If qty\_to\_be\_reserved ≤ self.delivered\_qty.
  - Set msg from translated “Reserved Qty should be greater than Delivered Qty.”.
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get total reserved qty](operations-101.md#op-12ecd8d2c59734).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L272) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1186)

<a id="op-12ecd8d2c59734"></a>
### Stock Reservation Entry.get total reserved qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_get_total_reserved_qty`

**Inputs** self.

**Declared result** float.

**Explicit results** self.get\_row\_reserved\_qty() · get\_sre\_reserved\_qty\_for\_voucher\_detail\_no(self.item\_code, self.voucher\_type, self.voucher\_no, self.voucher\_detail\_no, ignore\_sre = self.name, warehouse = no value when self.voucher\_type equals “Sales Orde ….

**Local steps**

- If (self.voucher\_type belongs to list(“Work Order”, “Subcontracting Order”) and not self.from\_voucher\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type belongs to list(“Work Order”, “Subcontracting Order”) → not self.from\_voucher\_type.
  - Return self.get\_row\_reserved\_qty().
- Set from\_voucher\_detail\_no from no value.
- If self.from\_voucher\_type belongs to list(“Stock Entry”, “Production Plan”).
  - Set from\_voucher\_detail\_no from self.from\_voucher\_detail\_no.
- Return get\_sre\_reserved\_qty\_for\_voucher\_detail\_no(self.item\_code, self.voucher\_type, self.voucher\_no, self.voucher\_detail\_no, ignore\_sre = self.name, warehouse = no value when self.voucher\_type equals “Sales Orde ….
  - Value choice on self.voucher\_type equals “Sales Order” — true gives no value, false gives self.warehouse.

**Methods declared on this owner** [get row reserved qty](operations-102.md#op-d6613b28622897).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L829)
