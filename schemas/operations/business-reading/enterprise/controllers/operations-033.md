# Shared transaction rules · operations 33

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Subcontracting inward controller

<a id="op-e42fee6a905ecc"></a>
### Subcontracting Inward Controller.update inward order received items for manufacture

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_update_inward_order_received_items_for_manufacture`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order” via get\_cached\_value · read “Item” via get\_cached\_value · read “Work Order” via get\_cached\_value · read “Subcontracting Inward Order Received Item” via count.

**State and service calls** request delete\_doc for “Subcontracting Inward Order Received Item” · request bulk\_update on “Subcontracting Inward Order Received Item” · request new\_doc for “Subcontracting Inward Order Received Item” · call insert on doc · call submit on doc.

**Local steps**

- Set customer\_warehouse from Platform.get\_cached\_value(“Subcontracting Inward Order”, self.subcontracting\_inward\_order, “customer\_warehouse”).
- Set items from list of item for item drawn from self.items where (not item.is\_finished\_item and not item.secondary\_item\_type and not item.valuation\_type).
  - Draw item from self.items, keep a combination only if ((not item.is\_finished\_item and not item.secondary\_item\_type and not item.valuation\_type)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.is\_finished\_item → not item.secondary\_item\_type → not item.valuation\_type.
- Set item\_code\_wh from Platform.\_dict(mapping of tuple(item.item\_code, customer\_warehouse when Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”), otherwise item.s\_warehouse) → item.transfer\_qty when  ….
  - Draw item from items.
  - Value choice on Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”) — true gives customer\_warehouse, false gives item.s\_warehouse.
  - Value choice on self.\_action equals “submit” — true gives item.transfer\_qty, false gives negative item.transfer\_qty.
- Set tuple(item\_codes, warehouses) from zip(expanded list(item\_code\_wh.keys()), strict = true).
- Set table from Platform.qb.DocType(“Subcontracting Inward Order Received Item”).
- Set data from nested operand in the contract.qb.from\_(table).select(table.name, table.rm\_item\_code, table.is\_customer\_provided\_item, table.consumed\_qty, …).where(((((nested operand in the contract.docstatus equals 1 bit ….
- If data bound to data.run(as\_dict = true).
  - Set used\_item\_wh from list().
  - Set doc\_updates from mapping().
  - For each d in data.
    - If not d.warehouse.
      - Set d.warehouse from next(generator of key at 1 for key drawn from item\_code\_wh.keys() where (key at 0 equals d.rm\_item\_code and key does not belong to used\_item\_wh)).
        - Draw key from item\_code\_wh.keys(), keep a combination only if ((key at 0 equals d.rm\_item\_code and key does not belong to used\_item\_wh)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in key at 0 equals d.rm\_item\_code → key does not belong to used\_item\_wh.
      - Evaluate used\_item\_wh.append(tuple(d.rm\_item\_code, d.warehouse)).
    - Set qty from (d.consumed\_qty + item\_code\_wh at tuple(d.rm\_item\_code, d.warehouse)).
    - If (qty or d.is\_customer\_provided\_item or not d.is\_additional\_item).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in qty → d.is\_customer\_provided\_item → not d.is\_additional\_item.
      - Set doc\_updates at d.name from mapping(“consumed\_qty” → qty).
    - Otherwise.
      - Evaluate Platform.delete\_doc(“Subcontracting Inward Order Received Item”, d.name, ignore\_permissions = true).
  - If doc\_updates.
    - Evaluate Platform.db.bulk\_update(“Subcontracting Inward Order Received Item”, doc\_updates, chunk\_size = len(doc\_updates), update\_modified = false).
  - Set main\_item\_code from next(generator of fg for fg drawn from self.items where fg.is\_finished\_item).item\_code.
    - Draw fg from self.items, keep a combination only if (fg.is\_finished\_item).
  - For each extra\_item in list of item for item drawn from items where (not Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”) and tuple(item.item\_code, item.s\_warehouse) does not belong to list of tuple ….
    - Draw item from items, keep a combination only if ((not Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”) and tuple(item.item\_code, item.s\_warehouse) does not belong to list of tuple(d.rm\_item\_code, d.warehouse) for d drawn fro …).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”) → tuple(item.item\_code, item.s\_warehouse) does not belong to list of tuple(d.rm\_item\_code, d.warehouse) for d drawn from data where not d.is\_customer\_provided\_item.
    - Draw d from data, keep a combination only if (not d.is\_customer\_provided\_item).
    - Set doc from Platform.new\_doc(“Subcontracting Inward Order Received Item”, parent = self.subcontracting\_inward\_order, parenttype = “Subcontracting Inward Order”, parentfield = “received\_items”, idx = (Platform.db.count ….
    - Evaluate doc.insert(ignore\_permissions = true).
    - Evaluate doc.submit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Subcontracting Inward Order”, self.subcontracting\_inward\_order, “customer\_warehouse”), Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1070) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L747)

<a id="op-ed6e81bc4cbbf4"></a>
### Subcontracting Inward Controller.update inward order secondary items

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_update_inward_order_secondary_items`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order Secondary Item” via get\_all · read “Work Order” via get\_cached\_value · read “Subcontracting Inward Order Secondary Item” via count · read “Work Order” via get\_value.

**State and service calls** request delete\_doc for “Subcontracting Inward Order Secondary Item” · request bulk\_update on “Subcontracting Inward Order Secondary Item” · request new\_doc for “Subcontracting Inward Order Secondary Item” · call insert on doc · call submit on doc.

**Local steps**

- If (scio bound to self.subcontracting\_inward\_order and self.purpose equals “Manufacture”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in scio bound to self.subcontracting\_inward\_order → self.purpose equals “Manufacture”.
  - Set secondary\_items\_list from list of item for item drawn from self.items where (item.secondary\_item\_type or item.valuation\_type).
    - Draw item from self.items, keep a combination only if ((item.secondary\_item\_type or item.valuation\_type)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.secondary\_item\_type → item.valuation\_type.
  - Set secondary\_items from defaultdict(float).
  - For each item in secondary\_items\_list.
    - Update secondary\_items at tuple(item.item\_code, item.t\_warehouse) using + item.transfer\_qty when self.\_action equals “submit”, otherwise negative item.transfer\_qty.
      - Value choice on self.\_action equals “submit” — true gives item.transfer\_qty, false gives negative item.transfer\_qty.
  - Set secondary\_items from Platform.\_dict(secondary\_items).
  - If secondary\_items.
    - Set tuple(item\_codes, warehouses) from zip(expanded list(secondary\_items.keys()), strict = true).
    - Set item\_codes from list(item\_codes).
    - Set warehouses from list(warehouses).
    - Set result from Platform.get\_all(“Subcontracting Inward Order Secondary Item”, filters = mapping(“item\_code” → list(“in”, item\_codes), “warehouse” → list(“in”, warehouses), “reference\_name” → Platform.get\_cached\_value(“Wo ….
    - If result.
      - Set secondary\_items\_dict from Platform.\_dict(mapping of tuple(d.item\_code, d.warehouse) → Platform.\_dict(mapping(“name” → d.name, “produced\_qty” → d.produced\_qty)) for d drawn from result).
        - Draw d from result.
      - Set doc\_updates from mapping().
      - For each tuple(key, value) in secondary\_items\_dict.items().
        - If (self.\_action equals “cancel” and (value.produced\_qty − abs(secondary\_items.get(key))) equals 0).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.\_action equals “cancel” → (value.produced\_qty − abs(secondary\_items.get(key))) equals 0.
          - Evaluate Platform.delete\_doc(“Subcontracting Inward Order Secondary Item”, value.name, ignore\_permissions = true).
        - Otherwise.
          - Set doc\_updates at value.name from mapping(“produced\_qty” → (value.produced\_qty + secondary\_items.get(key))).
      - If doc\_updates.
        - Evaluate Platform.db.bulk\_update(“Subcontracting Inward Order Secondary Item”, doc\_updates, chunk\_size = len(doc\_updates), update\_modified = false).
    - Set fg\_item\_code from next(generator of fg for fg drawn from self.items where fg.is\_finished\_item).item\_code.
      - Draw fg from self.items, keep a combination only if (fg.is\_finished\_item).
    - For each secondary\_item in list of item for item drawn from secondary\_items\_list where tuple(item.item\_code, item.t\_warehouse) does not belong to list of tuple(d.item\_code, d.warehouse) for d drawn from result.
      - Draw item from secondary\_items\_list, keep a combination only if (tuple(item.item\_code, item.t\_warehouse) does not belong to list of tuple(d.item\_code, d.warehouse) for d drawn from result).
      - Draw d from result.
      - Set doc from Platform.new\_doc(“Subcontracting Inward Order Secondary Item”, parent = scio, parenttype = “Subcontracting Inward Order”, parentfield = “secondary\_items”, idx = (Platform.db.count(“Subcontracting Inward Or ….
      - Evaluate doc.insert(ignore\_permissions = true).
      - Evaluate doc.submit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Work Order”, self.work\_order, “subcontracting\_inward\_order\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1072) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L749)

<a id="op-0eaed53a40548b"></a>
### Subcontracting Inward Controller.cancel stock reservation entries for inward

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_cancel_stock_reservation_entries_for_inward`

**Inputs** self.

**Local steps**

- If self.purpose equals “Receive from Customer”.
  - Evaluate self.adjust\_inward\_reservations(release = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [adjust inward reservations](operations-033.md#op-9f37edb8c5246a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1060) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L737)

<a id="op-6c78329a62936b"></a>
### Subcontracting Inward Controller.remove reference for additional items

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_remove_reference_for_additional_items`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order Received Item” via exists · read “Subcontracting Inward Order Item” via exists · read “Subcontracting Inward Order Secondary Item” via exists.

**State and service calls** call db\_set on item.

**Local steps**

- If self.subcontracting\_inward\_order.
  - Set items from list of item for item drawn from self.items where (item.scio\_detail and (not nested operand in the contract.db.exists(“Subcontracting Inward Order Received Item”, item.scio\_detail) and not nested operand i ….
    - Draw item from self.items, keep a combination only if ((item.scio\_detail and (not Platform.db.exists(“Subcontracting Inward Order Received Item”, item.scio\_detail) and not Platform.db.exists(“Subcontracting Inward Order Item”, item.scio\_detail) and not Platfor …).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.scio\_detail → (not Platform.db.exists(“Subcontracting Inward Order Received Item”, item.scio\_detail) and not Platform.db.exists(“Subcontracting Inward Order Item”, item.scio\_detail) and not Platform.db.exists(“Subcontra ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.db.exists(“Subcontracting Inward Order Received Item”, item.scio\_detail) → not Platform.db.exists(“Subcontracting Inward Order Item”, item.scio\_detail) → not Platform.db.exists(“Subcontracting Inward Order Secondary Item”, item.scio\_detail).
  - For each item in items.
    - Evaluate item.db\_set(“scio\_detail”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0400.json#L1930) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1065) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L742)

<a id="op-7ec9633ff145a8"></a>
### Subcontracting Inward Controller.create stock reservation entries for inward

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_create_stock_reservation_entries_for_inward`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value · resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** request new\_doc for “Stock Reservation Entry” · call submit on sre · msgprint with translated “Stock Reservation Entries Created”.

**Local steps**

- If self.purpose equals “Receive from Customer”.
  - For each item in self.items.
    - Evaluate item.reload().
    - Set sre from Platform.new\_doc(“Stock Reservation Entry”).
    - Set sre.company from self.company.
    - Set sre.voucher\_type from “Subcontracting Inward Order”.
    - Set sre.voucher\_qty, sre.reserved\_qty, sre.available\_qty from item.transfer\_qty.
    - Set sre.voucher\_no from self.subcontracting\_inward\_order.
    - Set sre.voucher\_detail\_no from item.scio\_detail.
    - Set sre.item\_code from item.item\_code.
    - Set sre.stock\_uom from item.stock\_uom.
    - Set sre.warehouse from (item.t\_warehouse or item.s\_warehouse).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.t\_warehouse → item.s\_warehouse.
    - Set sre.has\_serial\_no from Platform.get\_cached\_value(“Item”, item.item\_code, “has\_serial\_no”).
    - Set sre.has\_batch\_no from Platform.get\_cached\_value(“Item”, item.item\_code, “has\_batch\_no”).
    - Set sre.reservation\_based\_on from “Qty” when not item.serial\_and\_batch\_bundle, otherwise “Serial and Batch”.
      - Value choice on not item.serial\_and\_batch\_bundle — true gives “Qty”, false gives “Serial and Batch”.
    - If item.serial\_and\_batch\_bundle.
      - Set sabb from Platform.get\_doc(“Serial and Batch Bundle”, item.serial\_and\_batch\_bundle).
      - For each entry in sabb.entries.
        - Evaluate sre.append(“sb\_entries”, mapping(“serial\_no” → entry.serial\_no, “batch\_no” → entry.batch\_no, “qty” → entry.qty, “warehouse” → entry.warehouse)).
    - Evaluate sre.submit().
  - Evaluate Platform.msgprint(translated “Stock Reservation Entries Created”, alert = true, indicator = “green”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.item\_code, “has\_serial\_no”), Platform.get\_cached\_value(“Item”, item.item\_code, “has\_batch\_no”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0400.json#L2206) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1061) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L738)

<a id="op-d8965c137687ff"></a>
### Subcontracting Inward Controller.validate no later work order reservation

`operation_enterprise_binding_enterprise_controllers_subcontracting_inward_controller_subcontractinginwardcontroller_validate_no_later_work_order_reservation`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Work Order {1} reserved Item {2} after this return. Cancel the Work Order first.”.format(item.idx, get\_link\_to\_form(“Work Order”, reservation.voucher\_no), bold(item.item\_code)).

**Local steps**

- Set rows from defaultdict(list).
- For each item in self.items.
  - If (not item.scio\_detail or Platform.get\_cached\_value(“Item”, item.item\_code, “has\_serial\_no”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.scio\_detail → Platform.get\_cached\_value(“Item”, item.item\_code, “has\_serial\_no”).
    - Continue with the next iteration or loop test.
  - If batches bound to get\_serial\_batch\_list\_from\_item(item) at 1.
    - Evaluate rows at item.scio\_detail.append(tuple(item, batches)).
- If not rows.
  - Return no value.
- For each reservation in self.get\_later\_work\_order\_reservations(list(rows)).
  - For each tuple(item, batches) in rows at reservation.from\_voucher\_detail\_no.
    - If (reservation.batch\_no and reservation.batch\_no does not belong to batches).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in reservation.batch\_no → reservation.batch\_no does not belong to batches.
      - Continue with the next iteration or loop test.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Work Order {1} reserved Item {2} after this return. Cancel the Work Order first.”.format(item.idx, get\_link\_to\_form(“Work Order”, reservation.voucher\_no), bold(item.item\_code))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get later work order reservations](operations-033.md#op-1e12b03e9535bb).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.item\_code, “has\_serial\_no”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L451)

<a id="op-1e12b03e9535bb"></a>
### Subcontracting Inward Controller.get later work order reservations

`operation_enterprise_binding_enterprise_controllers_subcontracting_inward_controller_subcontractinginwardcontroller_get_later_work_order_reservations`

**Inputs** self, scio\_details.

**Declared result** list.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** nested operand in the contract(nested operand in the contract).select(reservation.voucher\_no, reservation.from\_voucher\_detail\_no, entry.batch\_no).where(((((nested operand in the contract bitwise and nested ….

**Local steps**

- Set submitted\_on from Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → self.doctype, “voucher\_no” → self.name), pluck = “creation”, order\_by = “creation asc”, limit = 1).
- Set reservation from Platform.qb.DocType(“Stock Reservation Entry”).
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Return nested operand in the contract(nested operand in the contract).select(reservation.voucher\_no, reservation.from\_voucher\_detail\_no, entry.batch\_no).where(((((nested operand in the contract bitwise and nested ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L448)

<a id="op-a942a4bbad4b28"></a>
### Subcontracting Inward Controller.adjust stock reservation entries for return

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_adjust_stock_reservation_entries_for_return`

**Inputs** self.

**Local steps**

- If self.purpose equals “Return Raw Material to Customer”.
  - If self.\_action equals “cancel”.
    - Evaluate self.validate\_no\_later\_work\_order\_reservation().
  - Evaluate self.adjust\_inward\_reservations(release = self.\_action equals “submit”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate no later work order reservation](operations-033.md#op-d8965c137687ff), [adjust inward reservations](operations-033.md#op-9f37edb8c5246a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1059) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L736)

<a id="op-9f37edb8c5246a"></a>
### Subcontracting Inward Controller.adjust inward reservations

`operation_enterprise_binding_enterprise_controllers_subcontracting_inward_controller_subcontractinginwardcontroller_adjust_inward_reservations`

**Inputs** self, release.

**Record and data access** resolve a document from “Serial and Batch Entry” via get\_doc · read “Serial and Batch Entry” via get\_value.

**State and service calls** call db\_set on Platform.get\_doc(“Serial and Batch Entry”, row.sbe\_name) · call db\_set on sbe\_doc.

**Local steps**

- For each item in self.items.
  - Set tuple(serial\_list, batch\_list) from get\_serial\_batch\_list\_from\_item(item).
  - If (serial\_list or batch\_list).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in serial\_list → batch\_list.
    - Set table from Platform.qb.DocType(“Stock Reservation Entry”).
    - Set child\_table from Platform.qb.DocType(“Serial and Batch Entry”).
    - Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“sre\_name”), nested operand in the contract.as\_(“sbe\_name”), child\_table.batch\_no, child\_table.qty,  ….
      - Value choice on release — true gives Order.asc, false gives Order.desc.
    - If serial\_list.
      - Set query from query.where(child\_table.serial\_no.isin(serial\_list)).
    - If batch\_list.
      - Set query from query.where(child\_table.batch\_no.isin(batch\_list)).
    - Set result from query.run(as\_dict = true).
    - Set qty\_to\_deliver from mapping of row.sre\_name → 0 for row drawn from result.
      - Draw row from result.
    - Set consumed\_qty from mapping of batch → 0 for batch drawn from batch\_list.
      - Draw batch from batch\_list.
    - For each row in result.
      - If serial\_list.
        - Evaluate Platform.get\_doc(“Serial and Batch Entry”, row.sbe\_name).db\_set(“delivered\_qty”, 1 when release, otherwise 0).
          - Value choice on release — true gives 1, false gives 0.
        - Update qty\_to\_deliver at row.sre\_name using + row.qty.
      - Otherwise.
        - If (batch\_list and not serial\_list).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_list → not serial\_list.
          - Set sabe\_qty from abs(Platform.get\_value(“Serial and Batch Entry”, mapping(“parent” → item.serial\_and\_batch\_bundle, “batch\_no” → row.batch\_no), “qty”)).
          - Set open\_qty from (row.qty − row.delivered\_qty) when release, otherwise row.delivered\_qty.
            - Value choice on release — true gives (row.qty − row.delivered\_qty), false gives row.delivered\_qty.
          - Set qty from min(open\_qty, (sabe\_qty − consumed\_qty at row.batch\_no)).
          - Set sbe\_doc from Platform.get\_doc(“Serial and Batch Entry”, row.sbe\_name).
          - Evaluate sbe\_doc.db\_set(“delivered\_qty”, (sbe\_doc.delivered\_qty + qty when release, otherwise negative qty)).
            - Value choice on release — true gives qty, false gives negative qty.
          - Update qty\_to\_deliver at row.sre\_name using + qty.
          - Update consumed\_qty at row.batch\_no using + qty.
    - For each tuple(sre\_name, qty) in qty\_to\_deliver.items().
      - Evaluate self.update\_inward\_reserved\_qty(sre\_name, negative qty when release, otherwise qty).
        - Value choice on release — true gives negative qty, false gives qty.
  - Otherwise.
    - Set table from Platform.qb.DocType(“Stock Reservation Entry”).
    - Set open\_qty from (table.reserved\_qty − table.delivered\_qty) when release, otherwise (table.voucher\_qty − table.reserved\_qty).
      - Value choice on release — true gives (table.reserved\_qty − table.delivered\_qty), false gives (table.voucher\_qty − table.reserved\_qty).
    - Set sre\_list from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
    - Set voucher\_qty from item.transfer\_qty.
    - For each sre in sre\_list.
      - Set qty from min(sre.qty, voucher\_qty).
      - Evaluate self.update\_inward\_reserved\_qty(sre.name, negative qty when release, otherwise qty).
        - Value choice on release — true gives negative qty, false gives qty.
      - Update voucher\_qty using − qty.
      - <a id="op-9f37edb8c5246a-guard-80"></a>If voucher\_qty ≤ 0.
        - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison voucher\_qty ≤ 0, voucher\_qty = 0 selects the branch that exits the enclosing loop. With voucher\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-9f37edb8c5246a-guard-80)

**Methods declared on this owner** [update inward reserved qty](operations-033.md#op-bbfcb29c1901f7).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1207) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L447)

<a id="op-bbfcb29c1901f7"></a>
### Subcontracting Inward Controller.update inward reserved qty

`operation_enterprise_binding_enterprise_controllers_subcontracting_inward_controller_subcontractinginwardcontroller_update_inward_reserved_qty`

**Inputs** self, sre\_name, qty\_change.

**Record and data access** resolve a document from “Stock Reservation Entry” via get\_doc.

**State and service calls** call db\_set on sre\_doc.

**Local steps**

- Set sre\_doc from Platform.get\_doc(“Stock Reservation Entry”, sre\_name).
- Evaluate sre\_doc.db\_set(“reserved\_qty”, (sre\_doc.reserved\_qty + qty\_change)).
- Evaluate sre\_doc.update\_status().
- Evaluate sre\_doc.update\_reserved\_stock\_in\_bin().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L450)

<a id="op-45a9e97d5d9e45"></a>
### Subcontracting Inward Controller.update inward order status

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_update_inward_order_status`

**Inputs** self.

**Local steps**

- If self.subcontracting\_inward\_order.
  - Bind dependencies set\_subcontracting\_inward\_order\_status.
  - Evaluate set\_subcontracting\_inward\_order\_status(self.subcontracting\_inward\_order).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0400.json#L4834) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1073) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L750)

<a id="op-8bfa9a799b1596"></a>
### Get fg reference names

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_get_finished_goods_reference_names`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Subcontracting Inward Order Item” via get\_all.

**Explicit results** list() · Platform.get\_all(“Subcontracting Inward Order Item”, limit\_start = start, limit\_page\_length = page\_len, filters = mapping(“parent” → parent, “docstatus” → 1), or\_filters = list(list(“name”, “like”, (“%%%s% ….

**Local steps**

- Set parent from filters.get(“parent”).
- If (not parent or not isinstance(parent, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent → not isinstance(parent, str).
  - Return list().
- Evaluate Platform.has\_permission(“Subcontracting Inward Order”, “read”, parent, throw = true).
- Return Platform.get\_all(“Subcontracting Inward Order Item”, limit\_start = start, limit\_page\_length = page\_len, filters = mapping(“parent” → parent, “docstatus” → 1), or\_filters = list(list(“name”, “like”, (“%%%s% ….

**Values supplied outside this operation** effective access from Platform.has\_permission(“Subcontracting Inward Order”, “read”, parent, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1058) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L735)

## Service · Taxes and totals

<a id="op-da31e4245c0d6f"></a>
### Calculate taxes and totals.initialize

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_initialize`

**Inputs** self, doc.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Local steps**

- Set self.doc from doc.
- Set Platform.flags.round\_off\_applicable\_accounts from (get\_round\_off\_applicable\_accounts(self.doc.company, list(), self.doc) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_round\_off\_applicable\_accounts(self.doc.company, list(), self.doc) → list().
- Set Platform.flags.round\_row\_wise\_tax from Platform.get\_single\_value(“Accounts Settings”, “round\_row\_wise\_tax”).
- Set self.\_items from self.filter\_rows() when self.doc.doctype equals “Quotation”, otherwise self.doc.get(“items”).
  - Value choice on self.doc.doctype equals “Quotation” — true gives self.filter\_rows(), false gives self.doc.get(“items”).
- Evaluate self.calculate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [filter rows](operations-033.md#op-437daa69af07d6), [calculate](operations-033.md#op-997d2d8d2a55b3).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “round\_row\_wise\_tax”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0400.json#L5301) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L790)

<a id="op-437daa69af07d6"></a>
### Calculate taxes and totals.filter rows

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_filter_rows`

**Inputs** self.

**Explicit results** items.

**Local steps**

- Set items from list(filter(deferred anonymous expression, self.doc.get(“items”))).
- Return items.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0400.json#L5589) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L782)

<a id="op-997d2d8d2a55b3"></a>
### Calculate taxes and totals.calculate

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate`

**Inputs** self, ignore\_tax\_template\_validation = false.

**Explicit results** no value · self.calculate(ignore\_tax\_template\_validation = true).

**Local steps**

- If not len(self.doc.items).
  - Return no value.
- Set self.need\_recomputation from false.
- Set self.ignore\_tax\_template\_validation from ignore\_tax\_template\_validation.
- Evaluate self.calculate\_discounted\_totals().
- If (not ignore\_tax\_template\_validation and self.need\_recomputation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not ignore\_tax\_template\_validation → self.need\_recomputation.
  - Return self.calculate(ignore\_tax\_template\_validation = true).
- Evaluate self.calculate\_shipping\_charges().
- If self.doc.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”).
  - Evaluate self.calculate\_total\_advance().
- If self.doc.meta.get\_field(“other\_charges\_calculation”).
  - Evaluate self.set\_item\_wise\_tax\_breakup().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate discounted totals](operations-033.md#op-83ba640450407b), [calculate shipping charges](operations-034.md#op-87543aa01af067), [calculate total advance](operations-035.md#op-133b50a06e8294), [set item wise tax breakup](operations-035.md#op-790fdb2cbe72d1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1098) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L767)

<a id="op-83ba640450407b"></a>
### Calculate taxes and totals.calculate discounted totals

`operation_enterprise_binding_enterprise_controllers_taxes_and_totals_calculate_taxes_and_totals_calculate_discounted_totals`

**Inputs** self.

**Local steps**

- Set self.discount\_amount\_applied from false.
- Evaluate self.\_calculate().
- If (self.doc.meta.get\_field(“discount\_amount”) and not self.has\_mapped\_discount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.meta.get\_field(“discount\_amount”) → not self.has\_mapped\_discount.
  - Evaluate self.set\_discount\_amount().
  - Evaluate self.apply\_discount\_amount().
- If (self.doc.apply\_discount\_on equals “Grand Total” and self.doc.get(“is\_cash\_or\_non\_trade\_discount”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.apply\_discount\_on equals “Grand Total” → self.doc.get(“is\_cash\_or\_non\_trade\_discount”).
  - Update self.doc.grand\_total using − self.doc.discount\_amount.
  - Update self.doc.base\_grand\_total using − self.doc.base\_discount\_amount.
  - Set self.doc.rounding\_adjustment, self.doc.base\_rounding\_adjustment from 0.0.
  - Evaluate self.set\_rounded\_total().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate](operations-033.md#op-b66b9d64dc80e1), [set discount amount](operations-035.md#op-2fb271029092a4), [apply discount amount](operations-035.md#op-69499f68e14f6c), [set rounded total](operations-035.md#op-4c9ec36bddb291).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L454)

<a id="op-b66b9d64dc80e1"></a>
### Calculate taxes and totals.calculate

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_2`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_conversion\_rate().
- Evaluate self.calculate\_item\_values().
- Evaluate self.validate\_item\_tax\_template().
- Evaluate self.update\_item\_tax\_map().
- Evaluate self.initialize\_taxes().
- Evaluate self.determine\_exclusive\_rate().
- Evaluate self.apply\_mapped\_additional\_discount().
- Evaluate self.calculate\_net\_total().
- Evaluate self.calculate\_taxes().
- Evaluate self.adjust\_grand\_total\_for\_inclusive\_tax().
- Evaluate self.calculate\_totals().
- Evaluate self.calculate\_total\_net\_weight().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate conversion rate](operations-033.md#op-17fa598d2fd8bd), [calculate item values](operations-033.md#op-61381d9d23f17c), [validate item tax template](operations-033.md#op-4d1111543d926a), [update item tax map](operations-033.md#op-7b52aee8666bb5), [initialize taxes](operations-034.md#op-2f6a2c6aa66370), [determine exclusive rate](operations-034.md#op-25479e96ef1b0e), [apply mapped additional discount](operations-034.md#op-be2d44920d8944), [calculate net total](operations-034.md#op-b256ca60be3e62), [calculate taxes](operations-034.md#op-e678ec8c201c81), [adjust grand total for inclusive tax](operations-035.md#op-7e80713d1c0d92), [calculate totals](operations-035.md#op-bc79046895dbab), [calculate total net weight](operations-035.md#op-1e667b53343bbf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1099) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L768)

<a id="op-4d1111543d926a"></a>
### Calculate taxes and totals.validate item tax template

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_validate_item_tax_template`

**Inputs** self.

**Record and data access** resolve a document from “Item” via get\_cached\_doc · resolve a document from “Item Group” via get\_cached\_doc.

**State and service calls** msgprint with translated “Row {0}: Item Tax template updated as per validity and rate applied”.format(item.idx, Platform.bold(item.item\_code)).

**Explicit results** no value.

**Local steps**

- If self.ignore\_tax\_template\_validation.
  - Return no value.
- If (self.doc.get(“is\_return”) and self.doc.get(“return\_against”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.get(“is\_return”) → self.doc.get(“return\_against”).
  - Return no value.
- For each item in self.doc.items.
  - If (item.item\_code and item.get(“item\_tax\_template”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.item\_code → item.get(“item\_tax\_template”).
    - Set item\_doc from Platform.get\_cached\_doc(“Item”, item.item\_code).
    - Set ctx from ItemDetailsCtx(mapping(“net\_rate” → (item.net\_rate or item.rate), “base\_net\_rate” → (item.base\_net\_rate or item.base\_rate), “tax\_category” → self.doc.get(“tax\_category”), “posting\_date” → self.doc.get(“pos ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.net\_rate → item.rate.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.base\_net\_rate → item.base\_rate.
    - Set item\_group from item\_doc.item\_group.
    - Set item\_group\_taxes from list().
    - While item\_group.
      - Set item\_group\_doc from Platform.get\_cached\_doc(“Item Group”, item\_group).
      - Update item\_group\_taxes using + (item\_group\_doc.taxes or list()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_group\_doc.taxes → list().
      - Set item\_group from item\_group\_doc.parent\_item\_group.
    - Set item\_taxes from (item\_doc.taxes or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_doc.taxes → list().
    - If (not item\_group\_taxes and not item\_taxes).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item\_group\_taxes → not item\_taxes.
      - Continue with the next iteration or loop test.
    - Set taxes from \_get\_item\_tax\_template(ctx, (item\_taxes + item\_group\_taxes), for\_validate = true).
    - If taxes.
      - If item.item\_tax\_template does not belong to taxes.
        - Set item.item\_tax\_template from get\_item\_tax\_template(ctx, item\_doc).
        - Evaluate Platform.msgprint(translated “Row {0}: Item Tax template updated as per validity and rate applied”.format(item.idx, Platform.bold(item.item\_code))).
        - If (self.discount\_amount\_applied and self.doc.apply\_discount\_on equals “Grand Total”).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.discount\_amount\_applied → self.doc.apply\_discount\_on equals “Grand Total”.
          - Set self.need\_recomputation from true.
- Evaluate self.validate\_item\_tax\_templates\_are\_usable().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate item tax templates are usable](operations-033.md#op-9498e89a247240).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, item.item\_code), Platform.get\_cached\_doc(“Item Group”, item\_group).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L807)

<a id="op-9498e89a247240"></a>
### Calculate taxes and totals.validate item tax templates are usable

`operation_enterprise_binding_enterprise_controllers_taxes_and_totals_calculate_taxes_and_totals_validate_item_tax_templates_are_usable`

**Inputs** self.

**Record and data access** read “Item Tax Template” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Item Tax Template {0} is disabled”.format(get\_link\_to\_form(“Item Tax Template”, template)) · validation helper — translated “Item Tax Template {0} does not belong to Company {1}”.format(get\_link\_to\_form(“Item Tax Template”, template), Platform.bold(self.doc.company)).

**Local steps**

- If (self.doc.get(“\_action”) does not belong to tuple(“save”, “submit”) or self.doc.get(“is\_consolidated”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.get(“\_action”) does not belong to tuple(“save”, “submit”) → self.doc.get(“is\_consolidated”).
  - Return no value.
- For each template in self.get\_changed\_item\_tax\_templates().
  - Set tuple(disabled, company) from Platform.get\_cached\_value(“Item Tax Template”, template, list(“disabled”, “company”)).
  - If disabled.
    - Call the validation error handler Platform.throw(translated “Item Tax Template {0} is disabled”.format(get\_link\_to\_form(“Item Tax Template”, template)), title = translated “Disabled Item Tax Template”).
  - If company differs from self.doc.company.
    - Call the validation error handler Platform.throw(translated “Item Tax Template {0} does not belong to Company {1}”.format(get\_link\_to\_form(“Item Tax Template”, template), Platform.bold(self.doc.company))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get changed item tax templates](operations-033.md#op-90a3d6ce394ac8).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item Tax Template”, template, list(“disabled”, “company”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1219) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L459)

<a id="op-90a3d6ce394ac8"></a>
### Calculate taxes and totals.get changed item tax templates

`operation_enterprise_binding_enterprise_controllers_taxes_and_totals_calculate_taxes_and_totals_get_changed_item_tax_templates`

**Inputs** self.

**Declared result** set.

**Explicit results** set of item.item\_tax\_template for item drawn from self.doc.items where (item.get(“item\_tax\_template”) and item.item\_tax\_template differs from saved\_templates.get(item.name)).

**Local steps**

- Set doc\_before\_save from self.doc.get\_doc\_before\_save().
- Set saved\_templates from mapping of item.name → item.item\_tax\_template for item drawn from doc\_before\_save.items when doc\_before\_save, otherwise mapping().
  - Value choice on doc\_before\_save — true gives mapping of item.name → item.item\_tax\_template for item drawn from doc\_before\_save.items, false gives mapping().
  - Draw item from doc\_before\_save.items.
- Return set of item.item\_tax\_template for item drawn from self.doc.items where (item.get(“item\_tax\_template”) and item.item\_tax\_template differs from saved\_templates.get(item.name)).
  - Draw item from self.doc.items, keep a combination only if ((item.get(“item\_tax\_template”) and item.item\_tax\_template differs from saved\_templates.get(item.name))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“item\_tax\_template”) → item.item\_tax\_template differs from saved\_templates.get(item.name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L456)

<a id="op-7b52aee8666bb5"></a>
### Calculate taxes and totals.update item tax map

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_update_item_tax_map`

**Inputs** self.

**Local steps**

- For each item in self.doc.items.
  - Set item.item\_tax\_rate from \_get\_item\_tax\_map(doc = self.doc, tax\_template = item.item\_tax\_template, as\_json = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L805)

<a id="op-17fa598d2fd8bd"></a>
### Calculate taxes and totals.validate conversion rate

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_validate_conversion_rate`

**Inputs** self.

**Local steps**

- Set company\_currency from Enterprise.get\_company\_currency(self.doc.company).
- If (not self.doc.currency or self.doc.currency equals company\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.doc.currency → self.doc.currency equals company\_currency.
  - Set self.doc.currency from company\_currency.
  - Set self.doc.conversion\_rate from 1.0.
- Otherwise.
  - Evaluate validate\_conversion\_rate(self.doc.currency, self.doc.conversion\_rate, self.doc.meta.get\_label(“conversion\_rate”), self.doc.company).
- Set self.doc.conversion\_rate from flt(self.doc.conversion\_rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L806)

<a id="op-3ef0cbc229a6f5"></a>
### Calculate taxes and totals.calculate item rate

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_item_rate`

**Inputs** self, item.

**Record and data access** resolve a document from “Pricing Rule” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- If not item.price\_list\_rate.
  - Evaluate remove\_margin(item).
  - Evaluate remove\_discount(item).
  - Set item.rate\_with\_margin from 0.
  - Return no value.
- Set applied\_rules from get\_applied\_pricing\_rules(item.pricing\_rules).
- Set has\_pricing\_rules from (bool(applied\_rules) and not self.doc.ignore\_pricing\_rule).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(applied\_rules) → not self.doc.ignore\_pricing\_rule.
- If has\_pricing\_rules.
  - Evaluate remove\_margin(item).
  - For each d in applied\_rules.
    - Set pricing\_rule from Platform.get\_cached\_doc(“Pricing Rule”, d).
    - Evaluate apply\_pricing\_rule\_margin(pricing\_rule, item, self.doc).
- Set item.rate\_with\_margin from get\_rate\_with\_margin(item).
- If item.discount\_percentage &gt; 0.
  - Set item.discount\_amount from flt(((item.rate\_with\_margin × item.discount\_percentage) ÷ 100.0), item.precision(“discount\_amount”)).
- Set calculated\_rate from flt((item.rate\_with\_margin − item.discount\_amount), item.precision(“rate”)).
- If (has\_pricing\_rules or not item.rate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_pricing\_rules → not item.rate.
  - Set item.rate from calculated\_rate.
  - Return no value.
- If item.rate equals calculated\_rate.
  - Return no value.
- If item.rate &gt; item.price\_list\_rate.
  - Set item.margin\_type from “Amount”.
  - Set item.margin\_rate\_or\_amount from flt((item.rate − item.price\_list\_rate), item.precision(“margin\_rate\_or\_amount”)).
  - Set item.rate\_with\_margin from item.rate.
  - Evaluate remove\_discount(item).
  - Return no value.
- Set item.rate\_with\_margin from item.price\_list\_rate.
- Set item.discount\_amount from flt((item.rate\_with\_margin − item.rate), item.precision(“discount\_amount”)).
- Set item.discount\_percentage from 0.
- Evaluate remove\_margin(item).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Pricing Rule”, d).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1101) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L770)

<a id="op-61381d9d23f17c"></a>
### Calculate taxes and totals.calculate item values

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_item_values`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.doc.get(“is\_consolidated”) or self.discount\_amount\_applied).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.get(“is\_consolidated”) → self.discount\_amount\_applied.
  - Return no value.
- Set do\_not\_round\_fields from list(“valuation\_rate”, “incoming\_rate”, “sales\_incoming\_rate”, “conversion\_factor”).
- For each item in self.doc.items.
  - Evaluate self.doc.round\_floats\_in(item, do\_not\_round\_fields = do\_not\_round\_fields).
  - Set item.\_mapped\_discount\_inclusive\_amount from 0.
  - Evaluate self.calculate\_item\_rate(item).
  - Set item.net\_rate from item.rate.
  - If (not (flt(item.qty) or flt(item.get(“rejected\_qty”))) and self.doc.get(“is\_return”) and self.doc.get(“doctype”) differs from “Purchase Receipt”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not (flt(item.qty) or flt(item.get(“rejected\_qty”))) → self.doc.get(“is\_return”) → self.doc.get(“doctype”) differs from “Purchase Receipt”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.qty) → flt(item.get(“rejected\_qty”)).
    - Set item.amount from flt((negative 1 × item.rate), item.precision(“amount”)).
  - Otherwise.
    - If (not item.qty and self.doc.get(“is\_debit\_note”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.qty → self.doc.get(“is\_debit\_note”).
      - Set item.amount from flt(item.rate, item.precision(“amount”)).
    - Otherwise.
      - Set item.amount from flt((item.rate × self.get\_billed\_qty(item)), item.precision(“amount”)).
  - Set item.net\_amount from item.amount.
  - Evaluate self.\_set\_in\_company\_currency(item, list(“price\_list\_rate”, “rate\_with\_margin”, “rate”, “net\_rate”, …)).
  - Set item.item\_tax\_amount from 0.0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate item rate](operations-033.md#op-3ef0cbc229a6f5), [get billed qty](operations-034.md#op-0d91de14fc41c1), [set in company currency](operations-034.md#op-2605086ca20dec).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L771)
