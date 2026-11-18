# Production · operations 42

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Work order

[Record definition](../../../../data/record-types/work_order.json)

<a id="op-4f878759c4272e"></a>
### Work Order.update transferred qty for required items

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_transferred_quantity_for_required_items`

**Inputs** self.

**State and service calls** call db\_set on row.

**Explicit results** no value.

**Local steps**

- If self.skip\_transfer.
  - Return no value.
- Set transferred\_by\_key from self.\_material\_transfer\_qty\_by\_item\_warehouse\_and\_operation().
- Set transferred\_items from Platform.\_dict().
- For each tuple(tuple(item\_code, \_warehouse, \_operation\_row\_id, \_operation), qty) in transferred\_by\_key.items().
  - Set transferred\_items at item\_code from (flt(transferred\_items.get(item\_code)) + qty).
- Set row\_wise\_serial\_batch from Platform.\_dict(mapping()).
- If self.reserve\_stock.
  - Set row\_wise\_serial\_batch from get\_row\_wise\_serial\_batch(self.name).
- Set transferred\_by\_row from distribute\_transfers\_over\_rows(self.required\_items, transferred\_by\_key).
- For each row in self.required\_items.
  - Set transferred\_qty from transferred\_by\_row at row.name.
  - Evaluate row.db\_set(“transferred\_qty”, transferred\_qty, update\_modified = false).
  - If self.reserve\_stock.
    - Evaluate self.update\_qty\_in\_stock\_reservation(row, transferred\_qty, row\_wise\_serial\_batch).
- Evaluate self.recompute\_material\_transferred\_for\_manufacturing(transferred\_items).

If control reaches the end, it returns no value.

**Methods declared on this owner** [material transfer qty by item warehouse and operation](operations-042.md#op-1d4c9f74f510e2), [update qty in stock reservation](operations-042.md#op-db58bfc12bdc1d), [recompute material transferred for manufacturing](operations-042.md#op-21dd2425dea2e4).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L834)

<a id="op-9e2e8ec34d746a"></a>
### Work Order.refresh material transferred for manufacturing

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_refresh_material_transferred_for_manufacturing`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.skip\_transfer.
  - Return no value.
- Set transferred\_items from self.\_material\_transfer\_qty\_by\_item(is\_return = 0).
- Evaluate self.recompute\_material\_transferred\_for\_manufacturing(transferred\_items).

If control reaches the end, it returns no value.

**Methods declared on this owner** [material transfer qty by item](operations-042.md#op-86fffd1aee2ebd), [recompute material transferred for manufacturing](operations-042.md#op-21dd2425dea2e4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L806)

<a id="op-86fffd1aee2ebd"></a>
### Work Order.material transfer qty by item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_material_transfer_qty_by_item`

**Inputs** self, is\_return.

**Explicit results** self.\_cap\_returned\_qty\_to\_transferred(transferred\_items) · transferred\_items.

**Local steps**

- Set ste from Platform.qb.DocType(“Stock Entry”).
- Set ste\_child from Platform.qb.DocType(“Stock Entry Detail”).
- Set job\_card from Platform.qb.DocType(“Job Card”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
- Set data from (query.run(as\_dict = 1) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run(as\_dict = 1) → list().
- Set transferred\_items from Platform.\_dict().
- For each d in data.
  - Set key from (d.original\_item or d.item\_code).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.original\_item → d.item\_code.
  - Set transferred\_items at key from (flt(transferred\_items.get(key)) + flt(d.qty)).
- If is\_return.
  - Return self.\_cap\_returned\_qty\_to\_transferred(transferred\_items).
- Return transferred\_items.

**Methods declared on this owner** [cap returned qty to transferred](operations-042.md#op-141a82ee6a0928).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L65) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1075)

<a id="op-141a82ee6a0928"></a>
### Work Order.cap returned qty to transferred

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_cap_returned_qty_to_transferred`

**Inputs** self, returned\_qty\_by\_item.

**Explicit results** Platform.\_dict(mapping of item\_code → min(flt(returned\_qty), flt(transferred\_qty\_by\_item.get(item\_code))) for tuple(item\_code, returned\_qty) drawn from returned\_qty\_by\_item.items()).

**Local steps**

- Set transferred\_qty\_by\_item from self.\_material\_transfer\_qty\_by\_item(is\_return = 0).
- Return Platform.\_dict(mapping of item\_code → min(flt(returned\_qty), flt(transferred\_qty\_by\_item.get(item\_code))) for tuple(item\_code, returned\_qty) drawn from returned\_qty\_by\_item.items()).
  - Draw tuple(item\_code, returned\_qty) from returned\_qty\_by\_item.items().

**Methods declared on this owner** [material transfer qty by item](operations-042.md#op-86fffd1aee2ebd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L36) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1046)

<a id="op-1d4c9f74f510e2"></a>
### Work Order.material transfer qty by item warehouse and operation

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_material_transfer_qty_by_item_warehouse_and_operation`

**Inputs** self.

**Explicit results** qty\_by\_key.

**Local steps**

- Set ste from Platform.qb.DocType(“Stock Entry”).
- Set ste\_child from Platform.qb.DocType(“Stock Entry Detail”).
- Set job\_card from Platform.qb.DocType(“Job Card”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- Set qty\_by\_key from mapping().
- For each d in (query.run(as\_dict = 1) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run(as\_dict = 1) → list().
  - Set key from tuple((d.original\_item or d.item\_code), d.s\_warehouse, d.operation\_row\_id, d.operation).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.original\_item → d.item\_code.
  - Set qty\_by\_key at key from (qty\_by\_key.get(key, 0.0) + flt(d.qty)).
- Return qty\_by\_key.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L66) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1076)

<a id="op-21dd2425dea2e4"></a>
### Work Order.recompute material transferred for manufacturing

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_recompute_material_transferred_for_manufacturing`

**Inputs** self, transferred\_items.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If (self.operations and self.transfer\_material\_against equals “Job Card”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.operations → self.transfer\_material\_against equals “Job Card”.
  - Return no value.
- Set sum\_fg\_completed\_qty from self.get\_transferred\_or\_manufactured\_qty(“Material Transfer for Manufacture”, “material\_transferred\_for\_manufacturing”).
- If sum\_fg\_completed\_qty.
  - Evaluate self.db\_set(“material\_transferred\_for\_manufacturing”, sum\_fg\_completed\_qty).
  - Return no value.
- Set required\_by\_item from mapping().
- For each row in self.required\_items.
  - If (not row.include\_item\_in\_manufacturing or flt(row.required\_qty) ≤ 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.include\_item\_in\_manufacturing → flt(row.required\_qty) ≤ 0.
    - Continue with the next iteration or loop test.
  - Set required\_by\_item at row.item\_code from (required\_by\_item.get(row.item\_code, 0.0) + flt(row.required\_qty)).
- If not required\_by\_item.
  - Return no value.
- Set min\_fraction from min(generator of (flt((nested operand in the contract.get(item\_code) or 0)) ÷ required\_qty) for tuple(item\_code, required\_qty) drawn from required\_by\_item.items()).
  - Draw tuple(item\_code, required\_qty) from required\_by\_item.items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in transferred\_items.get(item\_code) → 0.
- Set min\_fraction from min(min\_fraction, 1.0).
- Set material\_transferred from (min\_fraction × flt(self.qty)).
- Evaluate self.db\_set(“material\_transferred\_for\_manufacturing”, material\_transferred).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get transferred or manufactured qty](operations-039.md#op-67c1568be00a5d).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L73) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1083)

<a id="op-db58bfc12bdc1d"></a>
### Work Order.update qty in stock reservation

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_update_qty_in_stock_reservation`

**Inputs** self, row, transferred\_qty, row\_wise\_serial\_batch.

**Record and data access** read “Stock Reservation Entry” via get\_all · resolve a document from “Stock Reservation Entry” via get\_doc.

**State and service calls** call db\_set on doc.

**Local steps**

- Set filters from mapping(“voucher\_no” → self.name, “item\_code” → row.item\_code, “voucher\_detail\_no” → row.name, “warehouse” → row.source\_warehouse).
- Set names from Platform.get\_all(“Stock Reservation Entry”, filters = mapping(expand filters, “status” → tuple(“not in”, list(“Closed”, “Cancelled”, “Completed”))), pluck = “name”).
- If self.status equals “Closed”.
  - Update names using + Platform.get\_all(“Stock Reservation Entry”, filters = mapping(expand filters, “docstatus” → 2, “transferred\_qty” → tuple(“&gt;”, 0)), pluck = “name”, order\_by = “creation”).
- If names.
  - For each name in names.
    - Set doc from Platform.get\_doc(“Stock Reservation Entry”, name).
    - Set qty\_to\_update from 0.0.
    - <a id="op-db58bfc12bdc1d-guard-25"></a>If transferred\_qty &lt; 0.
      - Continue with the next iteration or loop test.
    - Set qty\_to\_update from min(flt(transferred\_qty), flt((doc.reserved\_qty − doc.consumed\_qty))).
    - Set transferred\_qty from (flt(transferred\_qty) − qty\_to\_update).
    - <a id="op-db58bfc12bdc1d-guard-31"></a>If qty\_to\_update &lt; 0.
      - Continue with the next iteration or loop test.
    - If doc.docstatus equals 2.
      - Evaluate doc.db\_set(“transferred\_qty”, flt(qty\_to\_update), update\_modified = false).
      - Evaluate doc.release\_reversed\_usage(“transferred\_qty”, row\_wise\_serial\_batch).
      - Continue with the next iteration or loop test.
    - If ((doc.has\_batch\_no or doc.has\_serial\_no) and doc.reservation\_based\_on equals “Serial and Batch”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in (doc.has\_batch\_no or doc.has\_serial\_no) → doc.reservation\_based\_on equals “Serial and Batch”.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.has\_batch\_no → doc.has\_serial\_no.
      - Evaluate doc.consume\_serial\_batch\_for\_material\_transfer(row\_wise\_serial\_batch).
      - Set qty\_to\_update from doc.matched\_serial\_batch\_qty.
    - Evaluate doc.db\_set(“transferred\_qty”, flt(qty\_to\_update), update\_modified = false).
    - If doc.transferred\_qty ≥ doc.reserved\_qty.
      - Evaluate doc.db\_set(“status”, “Closed”, update\_modified = false).
    - Evaluate doc.update\_status().
    - Evaluate doc.update\_reserved\_stock\_in\_bin().
    - Evaluate doc.update\_reserved\_qty\_in\_voucher().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison transferred\_qty &lt; 0, transferred\_qty = -1 selects the branch that continues with the next loop iteration. With transferred\_qty = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-db58bfc12bdc1d-guard-25)
- At the comparison qty\_to\_update &lt; 0, qty\_to\_update = -1 selects the branch that continues with the next loop iteration. With qty\_to\_update = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-db58bfc12bdc1d-guard-31)

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L93) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1103)

<a id="op-f27d84ab7dbb1d"></a>
### Work Order.update returned qty

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_returned_quantity`

**Inputs** self.

**State and service calls** call db\_set on row.

**Local steps**

- Set returned\_by\_row from distribute\_over\_rows(self.required\_items, self.\_material\_transfer\_qty\_by\_item(is\_return = 1)).
- For each row in self.required\_items.
  - Evaluate row.db\_set(“returned\_qty”, returned\_by\_row at row.name, update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [material transfer qty by item](operations-042.md#op-86fffd1aee2ebd).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1392) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L831)

<a id="op-729bce707ba907"></a>
### Work Order.validate incoming material demand

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_validate_incoming_material_demand`

**Inputs** self, incoming\_qty\_by\_item.

**Explicit failure paths** validation helper — translated “Only {0} {1} of {2} is pending in Work Order {3}.”.format(max(pending, 0.0), uom\_by\_item at item\_code, item\_code, self.name).

**Local steps**

- Set required\_by\_item from mapping().
- Set uom\_by\_item from mapping().
- For each row in self.required\_items.
  - Set required\_by\_item at row.item\_code from (required\_by\_item.get(row.item\_code, 0.0) + flt(row.required\_qty)).
  - Evaluate uom\_by\_item.setdefault(row.item\_code, row.stock\_uom).
- Set transferred from self.\_material\_transfer\_qty\_by\_item(is\_return = 0).
- Set requested from self.\_material\_request\_pending\_qty\_by\_item().
- Set picked from self.\_pick\_list\_pending\_qty\_by\_item().
- Set precision from Platform.get\_precision(“Work Order Item”, “required\_qty”).
- For each tuple(item\_code, incoming\_qty) in incoming\_qty\_by\_item.items().
  - If item\_code does not belong to required\_by\_item.
    - Continue with the next iteration or loop test.
  - Set pending from flt((((get\_allowed\_transfer\_qty(required\_by\_item at item\_code) − flt(nested operand in the contract.get(item\_code))) − flt(requested.get(item\_code))) − flt(picked.get(item\_code))), precision).
  - If flt(incoming\_qty, precision) &gt; pending.
    - Call the validation error handler Platform.throw(translated “Only {0} {1} of {2} is pending in Work Order {3}.”.format(max(pending, 0.0), uom\_by\_item at item\_code, item\_code, self.name), title = translated “Exceeds Pending Qty”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [material transfer qty by item](operations-042.md#op-86fffd1aee2ebd), [material request pending qty by item](operations-042.md#op-b860616dacf201), [pick list pending qty by item](operations-042.md#op-460a8ff0146f3c).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L98) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1108)

<a id="op-d21e494a4a67f8"></a>
### Work Order.update requested qty for required items

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_update_requested_qty_for_required_items`

**Inputs** self.

**State and service calls** call db\_set on row.

**Local steps**

- Set requested\_items from self.\_material\_request\_pending\_qty\_by\_item().
- For each row in self.required\_items.
  - Evaluate row.db\_set(“requested\_qty”, (requested\_items.get(row.item\_code) or 0.0), update\_modified = false).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in requested\_items.get(row.item\_code) → 0.0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [material request pending qty by item](operations-042.md#op-b860616dacf201).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L94) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1104)

<a id="op-b860616dacf201"></a>
### Work Order.material request pending qty by item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_material_request_pending_qty_by_item`

**Inputs** self.

**Explicit results** Platform.\_dict(mapping of d.item\_code → flt(d.qty) for d drawn from query.run(as\_dict = 1)).

**Local steps**

- Set mr from Platform.qb.DocType(“Material Request”).
- Set mr\_item from Platform.qb.DocType(“Material Request Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(mr\_item.item\_code, nested operand in the contract.as\_(“qty”)).where(((((nested operand in the contract bitwise and nested operand in th ….
- Return Platform.\_dict(mapping of d.item\_code → flt(d.qty) for d drawn from query.run(as\_dict = 1)).
  - Draw d from query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L64) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1074)

<a id="op-7e5512bd9c7459"></a>
### Work Order.update picked qty for required items

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_update_picked_qty_for_required_items`

**Inputs** self.

**State and service calls** call db\_set on row.

**Local steps**

- Set picked\_items from self.\_pick\_list\_pending\_qty\_by\_item().
- For each row in self.required\_items.
  - Evaluate row.db\_set(“picked\_qty”, (picked\_items.get(row.item\_code) or 0.0), update\_modified = false).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in picked\_items.get(row.item\_code) → 0.0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [pick list pending qty by item](operations-042.md#op-460a8ff0146f3c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L92) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1102)

<a id="op-460a8ff0146f3c"></a>
### Work Order.pick list pending qty by item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_pick_list_pending_qty_by_item`

**Inputs** self.

**Explicit results** Platform.\_dict(mapping of d.item\_code → flt(d.qty) for d drawn from query.run(as\_dict = 1)).

**Local steps**

- Set pick\_list from Platform.qb.DocType(“Pick List”).
- Set pick\_list\_item from Platform.qb.DocType(“Pick List Item”).
- Set mr from Platform.qb.DocType(“Material Request”).
- Set query from nested operand in the contract(nested operand in the contract).select(pick\_list\_item.item\_code, nested operand in the contract.as\_(“qty”)).where((((nested operand in the contract equals nested operand in t ….
- Return Platform.\_dict(mapping of d.item\_code → flt(d.qty) for d drawn from query.run(as\_dict = 1)).
  - Draw d from query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L68) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1078)

<a id="op-1011763a46381c"></a>
### Work Order.update consumed qty for required items

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_consumed_quantity_for_required_items`

**Inputs** self.

**State and service calls** call db\_set on item.

**Local steps**

- Set wip\_warehouse from self.wip\_warehouse.
- If (self.skip\_transfer and not self.from\_wip\_warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.skip\_transfer → not self.from\_wip\_warehouse.
  - Set wip\_warehouse from no value.
- Set consumed\_by\_item from self.get\_consumed\_qty\_by\_item().
- Set consumed\_by\_row from distribute\_over\_rows(self.required\_items, consumed\_by\_item).
- Set reserved\_consumption from self.split\_consumption\_over\_reservations(consumed\_by\_item, wip\_warehouse) when self.reserve\_stock, otherwise mapping().
  - Value choice on self.reserve\_stock — true gives self.split\_consumption\_over\_reservations(consumed\_by\_item, wip\_warehouse), false gives mapping().
- For each item in self.required\_items.
  - Set consumed\_qty from (consumed\_by\_row at item.name + flt(item.returned\_qty)).
  - Evaluate item.db\_set(“consumed\_qty”, flt(consumed\_qty), update\_modified = false).
  - If not self.reserve\_stock.
    - Continue with the next iteration or loop test.
  - Set warehouse from (wip\_warehouse or item.source\_warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in wip\_warehouse → item.source\_warehouse.
  - Evaluate self.update\_consumed\_qty\_in\_stock\_reservation(item, (flt(reserved\_consumption.get(item.name)) + flt(item.returned\_qty)), warehouse).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get consumed qty by item](operations-042.md#op-884acd0b31aa25), [split consumption over reservations](operations-042.md#op-d19173cb4bba53), [update consumed qty in stock reservation](operations-042.md#op-dd2f81bfb6dd01).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L823)

<a id="op-d19173cb4bba53"></a>
### Work Order.split consumption over reservations

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_split_consumption_over_reservations`

**Inputs** self, consumed\_by\_item, wip\_warehouse.

**Explicit results** consumption\_by\_row.

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sre.voucher\_detail\_no, sre.warehouse, nested operand in the contract.as\_(“qty”)).where((sre.voucher\_type equals “Work Order” bitwise an ….
- If self.status equals “Closed”.
  - Set query from query.where((sre.docstatus.isin(list(1, 2)) bitwise and (sre.docstatus equals 1 bitwise or sre.consumed\_qty &gt; 0))).
- Otherwise.
  - Set query from query.where(sre.docstatus equals 1).
- If not self.skip\_transfer.
  - Set query from query.where(fn.Coalesce(sre.from\_voucher\_no, empty text) differs from empty text).
- Set reserved from mapping of tuple(row.voucher\_detail\_no, row.warehouse) → flt(row.qty) for row drawn from query.run(as\_dict = true).
  - Draw row from query.run(as\_dict = true).
- Set remaining from mapping of item\_code → flt(qty) for tuple(item\_code, qty) drawn from consumed\_by\_item.items().
  - Draw tuple(item\_code, qty) from consumed\_by\_item.items().
- Set consumption\_by\_row from mapping().
- For each row in self.required\_items.
  - Set reserved\_qty from reserved.get(tuple(row.name, (wip\_warehouse or row.source\_warehouse)), 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in wip\_warehouse → row.source\_warehouse.
  - Set qty from min(reserved\_qty, remaining.get(row.item\_code, 0.0)).
  - Set consumption\_by\_row at row.name from qty.
  - Set remaining at row.item\_code from (remaining.get(row.item\_code, 0.0) − qty).
- Return consumption\_by\_row.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L87) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1097)

<a id="op-884acd0b31aa25"></a>
### Work Order.get consumed qty by item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_consumed_qty_by_item`

**Inputs** self.

**Explicit results** Platform.\_dict(mapping of d.item\_code → flt(d.qty) for d drawn from query.run(as\_dict = 1)).

**Local steps**

- Set ste from Platform.qb.DocType(“Stock Entry”).
- Set ste\_child from Platform.qb.DocType(“Stock Entry Detail”).
- Set item\_code from fn.Coalesce(fn.NullIf(ste\_child.original\_item, empty text), ste\_child.item\_code).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“item\_code”), nested operand in the contract.as\_(“qty”)).where((((nested operand in the contract equ ….
- Return Platform.\_dict(mapping of d.item\_code → flt(d.qty) for d drawn from query.run(as\_dict = 1)).
  - Draw d from query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L47) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1057)

<a id="op-dd2f81bfb6dd01"></a>
### Work Order.update consumed qty in stock reservation

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_update_consumed_qty_in_stock_reservation`

**Inputs** self, item, consumed\_qty, wip\_warehouse.

**Record and data access** read “Stock Reservation Entry” via get\_all · resolve a document from “Stock Reservation Entry” via get\_doc.

**State and service calls** call db\_set on doc.

**Local steps**

- Set filters from mapping(“voucher\_no” → self.name, “item\_code” → item.item\_code, “voucher\_detail\_no” → item.name, “warehouse” → wip\_warehouse, …).
- Set or\_filters from no value.
- If self.status equals “Closed”.
  - Set filters at “docstatus” from tuple(“in”, list(1, 2)).
  - Set or\_filters from mapping(“docstatus” → 1, “consumed\_qty” → tuple(“&gt;”, 0)).
- If not self.skip\_transfer.
  - Set filters at “from\_voucher\_no” from tuple(“is”, “set”).
- Set row\_wise\_serial\_batch from get\_row\_wise\_serial\_batch(self.name, CONSUMPTION\_PURPOSES).
- If names bound to Platform.get\_all(“Stock Reservation Entry”, filters = filters, or\_filters = or\_filters, pluck = “name”, order\_by = “creation”).
  - For each name in names.
    - If consumed\_qty &lt; 0.
      - Set consumed\_qty from 0.
    - Set doc from Platform.get\_doc(“Stock Reservation Entry”, name).
    - Set reserved\_qty from doc.reserved\_qty.
    - Set qty\_to\_update from consumed\_qty when consumed\_qty &lt; reserved\_qty, otherwise reserved\_qty.
      - Value choice on consumed\_qty &lt; reserved\_qty — true gives consumed\_qty, false gives reserved\_qty.
    - If qty\_to\_update ≥ 0.
      - Evaluate doc.db\_set(“consumed\_qty”, flt(qty\_to\_update), update\_modified = false).
      - Update consumed\_qty using − qty\_to\_update.
    - If doc.docstatus equals 2.
      - Evaluate doc.release\_reversed\_usage(“consumed\_qty”, row\_wise\_serial\_batch).
      - Continue with the next iteration or loop test.
    - If ((doc.has\_batch\_no or doc.has\_serial\_no) and doc.reservation\_based\_on equals “Serial and Batch”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in (doc.has\_batch\_no or doc.has\_serial\_no) → doc.reservation\_based\_on equals “Serial and Batch”.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.has\_batch\_no → doc.has\_serial\_no.
      - Evaluate doc.consume\_serial\_batch\_for\_material\_transfer(row\_wise\_serial\_batch).
      - Evaluate doc.db\_set(“consumed\_qty”, doc.matched\_serial\_batch\_qty, update\_modified = false).
    - Evaluate doc.update\_status().
    - Evaluate doc.update\_reserved\_stock\_in\_bin().
    - Evaluate doc.update\_reserved\_qty\_in\_voucher().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L91) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1101)

<a id="op-88341bc70ac7f2"></a>
### Work Order.validate reserved qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_validate_reserved_qty`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Consumed Qty cannot be greater than Reserved Qty for item {0}”.format(details.consumed\_qty, details.reserved\_qty, item.item\_code).

**Local steps**

- Set sre\_details from get\_sre\_details(self.name).
- For each item in self.required\_items.
  - If details bound to sre\_details.get(item.name).
    - If details.reserved\_qty &lt; details.consumed\_qty.
      - Call the validation error handler Platform.throw(translated “Consumed Qty cannot be greater than Reserved Qty for item {0}”.format(details.consumed\_qty, details.reserved\_qty, item.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1110)

<a id="op-52d849bf69fe8c"></a>
### Work Order.make bom

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_make_bill_of_materials`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “BOM”.

**Explicit results** bom.

**Local steps**

- Set bom from Platform.new\_doc(“BOM”).
- Set bom.item from self.production\_item.
- Set bom.company from self.company.
- Set bom.currency from get\_company\_currency(self.company).
- Set bom.conversion\_rate from 1.
- Set bom.quantity from (flt(self.produced\_qty) or flt(self.qty)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.produced\_qty) → flt(self.qty).
- For each d in self.get\_consumed\_items\_for\_bom().
  - Evaluate bom.append(“items”, mapping(“item\_code” → d.item\_code, “qty” → d.qty, “source\_warehouse” → d.s\_warehouse)).
- If self.operations.
  - Set bom.with\_operations from 1.
  - For each row in self.get\_bom\_operation\_rows(bom.quantity).
    - Evaluate bom.append(“operations”, row).
- Evaluate bom.set\_bom\_material\_details().
- Return bom.

**Methods declared on this owner** [get consumed items for bom](operations-042.md#op-0d3d554d407ee7), [get bom operation rows](operations-042.md#op-d29ff9c673d320).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L798)

<a id="op-0d3d554d407ee7"></a>
### Work Order.get consumed items for bom

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_consumed_items_for_bom`

**Inputs** self.

**Explicit results** nested operand in the contract(nested operand in the contract).groupby(sed.item\_code, sed.s\_warehouse).orderby(Min(sed.idx)).run(as\_dict = 1).

**Local steps**

- Set sed from Platform.qb.DocType(“Stock Entry Detail”).
- Set se from Platform.qb.DocType(“Stock Entry”).
- Return nested operand in the contract(nested operand in the contract).groupby(sed.item\_code, sed.s\_warehouse).orderby(Min(sed.idx)).run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L46) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1056)

<a id="op-d29ff9c673d320"></a>
### Work Order.get bom operation rows

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_bom_operation_rows`

**Inputs** self, bom\_qty.

**Explicit results** rows.

**Local steps**

- Set source\_operations from self.get\_source\_bom\_operations().
- Set sources\_by\_name from mapping of d.name → d for sources drawn from source\_operations.values(), then d drawn from sources.
  - Draw sources from source\_operations.values().
  - Draw d from sources.
- Set occurrence from mapping().
- Set rows from list().
- For each operation in self.operations.
  - Set source from self.get\_source\_bom\_operation(operation, source\_operations, sources\_by\_name, occurrence).
  - Evaluate rows.append(self.get\_bom\_operation\_row(operation, bom\_qty, source)).
- Return rows.

**Methods declared on this owner** [get source bom operations](operations-042.md#op-05776d999c578d), [get source bom operation](operations-042.md#op-2bf1f087337aa6), [get bom operation row](operations-042.md#op-d0912c3353bbcf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L44) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1054)

<a id="op-2bf1f087337aa6"></a>
### Work Order.get source bom operation

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_source_bom_operation`

**Inputs** self, operation, source\_operations, sources\_by\_name, occurrence.

**Explicit results** source when (source and source.keeps\_own\_time), otherwise no value.

**Local steps**

- If operation.get(“bom\_operation”).
  - Set source from sources\_by\_name.get(operation.bom\_operation).
  - If (source and tuple(source.parent, source.operation) differs from tuple((operation.bom or self.bom\_no), operation.operation)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in source → tuple(source.parent, source.operation) differs from tuple((operation.bom or self.bom\_no), operation.operation).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in operation.bom → self.bom\_no.
    - Set source from no value.
- Otherwise.
  - Set key from tuple((operation.bom or self.bom\_no), operation.operation).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in operation.bom → self.bom\_no.
  - Set idx, occurrence at key from (occurrence.get(key, negative 1) + 1).
  - Set sources from source\_operations.get(key, list()).
  - Set source from sources at idx when idx &lt; len(sources), otherwise no value.
    - Value choice on idx &lt; len(sources) — true gives sources at idx, false gives no value.
- Return source when (source and source.keeps\_own\_time), otherwise no value.
  - Value choice on (source and source.keeps\_own\_time) — true gives source, false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in source → source.keeps\_own\_time.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L58) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1068)

<a id="op-05776d999c578d"></a>
### Work Order.get source bom operations

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_source_bom_operations`

**Inputs** self.

**Record and data access** read “BOM Operation” via get\_all · read “Operation” via get\_all.

**Explicit results** source\_operations.

**Local steps**

- Set operations from Platform.get\_all(“BOM Operation”, filters = mapping(“parent” → self.bom\_no, “parenttype” → “BOM”), fields = list(“name”, “parent”, “operation”, “time\_in\_mins”, …), order\_by = “idx”).
- Set batch\_based from set(Platform.get\_all(“Operation”, filters = mapping(“name” → tuple(“in”, (list(set of nested operand in the contract for nested operand in the contract drawn from nested operand in the contract) or list(empty  …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list(set of d.operation for d drawn from operations) → list(empty text).
  - Draw d from operations.
- Set source\_operations from mapping().
- For each d in operations.
  - Set d.keeps\_own\_time from (cint(d.fixed\_time) or (d.operation belongs to batch\_based and flt(d.batch\_size))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(d.fixed\_time) → (d.operation belongs to batch\_based and flt(d.batch\_size)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.operation belongs to batch\_based → flt(d.batch\_size).
  - Evaluate source\_operations.setdefault(tuple(d.parent, d.operation), list()).append(d).
- Return source\_operations.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L59) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1069)

<a id="op-d0912c3353bbcf"></a>
### Work Order.get bom operation row

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_bom_operation_row`

**Inputs** self, operation, bom\_qty, source = no value.

**Explicit results** row.

**Local steps**

- Set row from mapping().
- For each fieldname in \_BOM\_OPERATION\_FIELDS\_FROM\_WORK\_ORDER.
  - Set row at fieldname from operation.get(fieldname).
- If source.
  - Evaluate row.update(mapping(“time\_in\_mins” → source.time\_in\_mins, “fixed\_time” → source.fixed\_time, “batch\_size” → source.batch\_size)).
  - Return row.
- If (flt(operation.completed\_qty) and flt(operation.actual\_operation\_time)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(operation.completed\_qty) → flt(operation.actual\_operation\_time).
  - Set completed\_qty from ((flt(operation.completed\_qty) × flt(self.qty)) ÷ get\_operation\_qty(self, operation)).
  - Set time\_per\_unit from (flt(operation.actual\_operation\_time) ÷ completed\_qty).
- Otherwise.
  - Set time\_per\_unit from (flt(operation.time\_in\_mins) ÷ flt(self.qty)).
- Set row at “time\_in\_mins” from (time\_per\_unit × flt(bom\_qty)).
- If (operation.bom and operation.bom differs from self.bom\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in operation.bom → operation.bom differs from self.bom\_no.
  - Set row at “batch\_size” from (flt(bom\_qty) or 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(bom\_qty) → 1.
- Return row.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L43) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1053)
