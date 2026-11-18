# Subcontracting · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Subcontracting order

[Record definition](../../../../data/record-types/subcontracting_order.json)

<a id="op-54e3ec1464b022"></a>
### Subcontracting Order.calculate supplied items qty and amount

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_calculate_supplied_items_quantity_and_amount`

**Inputs** self.

**Record and data access** resolve a document from “BOM” via get\_doc.

**Local steps**

- For each item in self.get(“items”).
  - Set bom from Platform.get\_doc(“BOM”, item.bom).
  - Set rm\_cost from sum(generator of flt(rm\_item.amount) for rm\_item drawn from bom.items).
    - Draw rm\_item from bom.items.
  - Set item.rm\_cost\_per\_qty from flt((rm\_cost ÷ flt(bom.quantity)), item.precision(“rm\_cost\_per\_qty”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0953.json#L1488) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L984)

<a id="op-8a96182a967d4c"></a>
### Subcontracting Order.calculate items qty and amount

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_calculate_items_quantity_and_amount`

**Inputs** self.

**Local steps**

- Set total\_qty, total from 0.
- For each item in self.items.
  - Set item.rate from ((item.rm\_cost\_per\_qty + item.service\_cost\_per\_qty) + flt(item.additional\_cost\_per\_qty)).
  - Set item.amount from (item.qty × item.rate).
  - Update total\_qty using + flt(item.qty).
  - Update total using + flt(item.amount).
- After normal loop exhaustion.
  - Set self.total\_qty from total\_qty.
  - Set self.total from total.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L982)

<a id="op-defbcdf7c49f14"></a>
### Subcontracting Order.update ordered qty for subcontracting

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_update_ordered_quantity_for_subcontracting`

**Inputs** self, sco\_item\_rows = no value.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- Set item\_wh\_list from list().
- For each item in self.get(“items”).
  - If ((not sco\_item\_rows or item.name belongs to sco\_item\_rows) and list(item.item\_code, item.warehouse) does not belong to item\_wh\_list and Platform.get\_cached\_value(“Item”, item.item\_code, “is\_stock\_item”) an ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not sco\_item\_rows or item.name belongs to sco\_item\_rows) → list(item.item\_code, item.warehouse) does not belong to item\_wh\_list → Platform.get\_cached\_value(“Item”, item.item\_code, “is\_stock\_item”) → item.warehouse.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not sco\_item\_rows → item.name belongs to sco\_item\_rows.
    - Evaluate item\_wh\_list.append(list(item.item\_code, item.warehouse)).
- For each tuple(item\_code, warehouse) in item\_wh\_list.
  - Evaluate update\_bin\_qty(item\_code, warehouse, mapping(“ordered\_qty” → get\_ordered\_qty(item\_code, warehouse))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0953.json#L1997) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L993)

<a id="op-2bae33f96ec99f"></a>
### Subcontracting Order.update reserved qty for subcontracting

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_update_reserved_quantity_for_subcontracting`

**Inputs** self, sco\_item\_rows = no value.

**Local steps**

- For each item in self.supplied\_items.
  - If (sco\_item\_rows and item.reference\_name does not belong to sco\_item\_rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sco\_item\_rows → item.reference\_name does not belong to sco\_item\_rows.
    - Continue with the next iteration or loop test.
  - If item.rm\_item\_code.
    - Set stock\_bin from get\_bin(item.rm\_item\_code, item.reserve\_warehouse).
    - Evaluate stock\_bin.update\_reserved\_qty\_for\_sub\_contracting().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0953.json#L2347) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1499) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L994)

<a id="op-22dfa70a9381f3"></a>
### Subcontracting Order.update subcontracted qty in work orders

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_order_subcontracting_order_subcontractingorder_update_subcontracted_qty_in_work_orders`

**Inputs** self.

**Record and data access** read “Job Card” via get\_all.

**Explicit results** no value.

**Local steps**

- Set job\_cards from list of d.job\_card for d drawn from self.items where d.job\_card.
  - Draw d from self.items, keep a combination only if (d.job\_card).
- If not job\_cards.
  - Return no value.
- For each work\_order in Platform.get\_all(“Job Card”, filters = mapping(“name” → tuple(“in”, job\_cards)), pluck = “work\_order”, distinct = true).
  - Evaluate update\_subcontracted\_qty(work\_order).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1694) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1191)

<a id="op-fb66991ceb2f49"></a>
### Subcontracting Order.populate items table

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_populate_items_table`

**Inputs** self.

**Record and data access** resolve a document from “Item” via get\_doc · read “Purchase Order Item” via get\_value.

**Explicit failure paths** validation helper — translated “Please select Finished Good Item for Service Item {0}”.format((si.item\_name or si.item\_code)).

**Local steps**

- Set items from list().
- For each si in self.service\_items.
  - If si.fg\_item.
    - Set item from Platform.get\_doc(“Item”, si.fg\_item).
    - Set tuple(qty, subcontracted\_qty, fg\_item\_qty, production\_plan\_sub\_assembly\_item, …) from Platform.db.get\_value(“Purchase Order Item”, si.purchase\_order\_item, list(“qty”, “subcontracted\_qty”, “fg\_item\_qty”, “production\_plan\_sub\_assembly\_item”, …)).
    - Set available\_qty from (flt(qty) − flt(subcontracted\_qty)).
    - <a id="op-fb66991ceb2f49-guard-27"></a>If available\_qty equals 0.
      - Continue with the next iteration or loop test.
    - Set si.qty from available\_qty.
    - Set conversion\_factor from (flt(qty) ÷ flt(fg\_item\_qty)).
    - Set si.fg\_item\_qty from flt((available\_qty ÷ conversion\_factor), Platform.get\_precision(“Purchase Order Item”, “qty”)).
    - Set si.amount from (available\_qty × si.rate).
    - Evaluate items.append(mapping(“item\_code” → item.name, “item\_name” → item.item\_name, “schedule\_date” → self.schedule\_date, “description” → item.description, …)).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Please select Finished Good Item for Service Item {0}”.format((si.item\_name or si.item\_code))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in si.item\_name → si.item\_code.
- If items.
  - For each item in items.
    - Evaluate self.append(“items”, item).
- Evaluate self.set\_missing\_values().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison available\_qty equals 0, available\_qty = 0 selects the branch that continues with the next loop iteration. With available\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-fb66991ceb2f49-guard-27)

**Methods declared on this owner** [set missing values](operations-003.md#op-5938df9ae3f4ae).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L990)

<a id="op-80d00c8ebd7843"></a>
### Subcontracting Order.update status

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_update_status`

**Inputs** self, status = no value, update\_modified = true, update\_bin = true.

**State and service calls** call db\_set on self.

**Local steps**

- If (self.status equals “Closed” and self.status differs from status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Closed” → self.status differs from status.
  - Evaluate check\_on\_hold\_or\_closed\_status(“Purchase Order”, self.purchase\_order).
- If (self.docstatus ≥ 1 and not status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus ≥ 1 → not status.
  - If self.docstatus equals 1.
    - If self.status equals “Draft”.
      - Set status from “Open”.
    - Otherwise.
      - If self.per\_received ≥ 100.
        - Set status from “Completed”.
      - Otherwise.
        - If (self.per\_received &gt; 0 and self.per\_received &lt; 100).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.per\_received &gt; 0 → self.per\_received &lt; 100.
          - Set status from “Partially Received”.
        - Otherwise.
          - Set total\_required\_qty, total\_supplied\_qty from 0.
          - For each item in self.supplied\_items.
            - Update total\_required\_qty using + item.required\_qty.
            - Update total\_supplied\_qty using + flt(item.total\_supplied\_qty).
          - If total\_supplied\_qty.
            - Set status from “Partial Material Transferred”.
            - If total\_supplied\_qty ≥ total\_required\_qty.
              - Set status from “Material Transferred”.
          - Otherwise.
            - Set status from “Open”.
  - Otherwise.
    - If self.docstatus equals 2.
      - Set status from “Cancelled”.
- If (status and self.status differs from status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status → self.status differs from status.
  - Evaluate self.db\_set(“status”, status, update\_modified = update\_modified).
- If status equals “Closed”.
  - Evaluate self.release\_stock\_reservations().
- Evaluate self.update\_requested\_qty().
- If update\_bin.
  - Evaluate self.update\_ordered\_qty\_for\_subcontracting().
  - Evaluate self.update\_reserved\_qty\_for\_subcontracting().
  - Evaluate self.update\_subcontracted\_qty\_in\_work\_orders().

If control reaches the end, it returns no value.

**Methods declared on this owner** [release stock reservations](operations-004.md#op-814f7c9a492403), [update ordered qty for subcontracting](operations-004.md#op-defbcdf7c49f14), [update reserved qty for subcontracting](operations-004.md#op-2bae33f96ec99f), [update subcontracted qty in work orders](operations-004.md#op-22dfa70a9381f3).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1500) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L995)

<a id="op-7d9fc48e248f3a"></a>
### Subcontracting Order.update subcontracted quantity in po

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_update_subcontracted_quantity_in_purchase_order`

**Inputs** self.

**Record and data access** read “Purchase Order Item” via get\_all.

**State and service calls** request set\_value on “Purchase Order Item”.

**Explicit results** no value.

**Local steps**

- Set po\_items from list of d.purchase\_order\_item for d drawn from self.service\_items where d.purchase\_order\_item.
  - Draw d from self.service\_items, keep a combination only if (d.purchase\_order\_item).
- If not po\_items.
  - Return no value.
- Set service\_item from Platform.qb.DocType(“Subcontracting Order Service Item”).
- Set order from Platform.qb.DocType(“Subcontracting Order”).
- Set subcontracted from mapping of row.purchase\_order\_item → row for row drawn from nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(service\_item.purchase\_o ….
  - Draw row from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bi ….
- Set po\_rows from mapping of row.name → row for row drawn from Platform.get\_all(“Purchase Order Item”, filters = mapping(“name” → list(“in”, po\_items)), fields = list(“name”, “qty”, “fg\_item\_qty”)).
  - Draw row from Platform.get\_all(“Purchase Order Item”, filters = mapping(“name” → list(“in”, po\_items)), fields = list(“name”, “qty”, “fg\_item\_qty”)).
- Set precision from Platform.get\_precision(“Purchase Order Item”, “fg\_item\_qty”).
- For each po\_item in po\_items.
  - Set row from (subcontracted.get(po\_item) or Platform.\_dict()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in subcontracted.get(po\_item) → Platform.\_dict().
  - Set qty from flt(row.qty).
  - If flt(row.fg\_item\_qty, precision) ≥ flt(po\_rows at po\_item.fg\_item\_qty, precision) &gt; 0.
    - Compare adjacent operands in order, stopping at the first false comparison in flt(row.fg\_item\_qty, precision) ≥ flt(po\_rows at po\_item.fg\_item\_qty, precision) &gt; 0.
    - Set qty from po\_rows at po\_item.qty.
  - Evaluate Platform.db.set\_value(“Purchase Order Item”, po\_item, “subcontracted\_qty”, qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L996)

<a id="op-a3769f2dc41fa7"></a>
### Subcontracting Order.reserve raw materials

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_reserve_raw_materials`

**Inputs** self, items = no value, stock\_entry = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.check\_permission(“write”).
- Evaluate self.make\_raw\_material\_reservations(items, stock\_entry).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make raw material reservations](operations-004.md#op-c93f24abf6101f).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L991)

<a id="op-c93f24abf6101f"></a>
### Subcontracting Order.make raw material reservations

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_order_subcontracting_order_subcontractingorder_make_raw_material_reservations`

**Inputs** self, items = no value, stock\_entry = no value.

**Record and data access** read “Material Request Plan Item” via get\_value.

**State and service calls** msgprint with translated “Stock Reservation Entries created”.

**Local steps**

- If self.reserve\_stock.
  - Set item\_dict from mapping().
  - If items.
    - Set item\_dict from mapping of d at “name” → d for d drawn from items.
      - Draw d from items.
    - Set items from list of item for item drawn from self.supplied\_items where item.name belongs to item\_dict.
      - Draw item from self.supplied\_items, keep a combination only if (item.name belongs to item\_dict).
  - Set reservation\_items from list().
  - Set is\_transfer from false.
  - For each item in (items or self.supplied\_items).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in items → self.supplied\_items.
    - Set data from Platform.\_dict(mapping(“voucher\_no” → self.name, “voucher\_type” → self.doctype, “voucher\_detail\_no” → item.name, “item\_code” → item.rm\_item\_code, …)).
    - If stock\_entry.
      - Evaluate data.update(mapping(“from\_voucher\_no” → stock\_entry, “from\_voucher\_type” → “Stock Entry”, “from\_voucher\_detail\_no” → item\_dict at item.name at “reference\_voucher\_detail\_no”, “serial\_and\_batch\_bundles” → it ….
    - Otherwise.
      - If self.production\_plan.
        - Set fg\_item from next(generator of i for i drawn from self.items where i.name equals item.reference\_name).
          - Draw i from self.items, keep a combination only if (i.name equals item.reference\_name).
        - If production\_plan\_sub\_assembly\_item bound to fg\_item.production\_plan\_sub\_assembly\_item.
          - Set tuple(from\_voucher\_detail\_no, reserved\_qty) from Platform.get\_value(“Material Request Plan Item”, mapping(“parent” → self.production\_plan, “item\_code” → item.rm\_item\_code, “warehouse” → item.reserve\_warehouse, “sub\_assembly\_item\_reference” → production\_p ….
          - If flt(item.stock\_reserved\_qty) &lt; reserved\_qty.
            - Set is\_transfer from true.
            - Evaluate data.update(mapping(“from\_voucher\_no” → self.production\_plan, “from\_voucher\_type” → “Production Plan”, “from\_voucher\_detail\_no” → from\_voucher\_detail\_no)).
    - Evaluate reservation\_items.append(data).
  - Set sre from StockReservation(self, items = reservation\_items).
  - If is\_transfer.
    - Evaluate sre.transfer\_reservation\_entries\_to(self.production\_plan, from\_doctype = “Production Plan”, to\_doctype = “Subcontracting Order”).
  - Otherwise.
    - If sre.make\_stock\_reservation\_entries().
      - Evaluate Platform.msgprint(translated “Stock Reservation Entries created”, alert = true, indicator = “blue”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1186)

<a id="op-fa00f4a1605fa4"></a>
### Subcontracting Order.has unreserved stock

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_has_unreserved_stock`

**Inputs** self.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- For each item in self.get(“supplied\_items”).
  - If ((item.required\_qty − flt(item.total\_supplied\_qty)) − flt(item.stock\_reserved\_qty)) &gt; 0.
    - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1491) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L986)

<a id="op-814f7c9a492403"></a>
### Subcontracting Order.release stock reservations

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_order_subcontracting_order_subcontractingorder_release_stock_reservations`

**Inputs** self.

**Local steps**

- Set sre\_list from list().
- For each sre in get\_stock\_reservation\_entries\_for\_voucher(self.doctype, self.name, fields = list(“name”, “transferred\_qty”, “consumed\_qty”), ignore\_status = true).
  - If (flt(sre.transferred\_qty) or flt(sre.consumed\_qty)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(sre.transferred\_qty) → flt(sre.consumed\_qty).
    - Evaluate self.release\_unused\_reserved\_qty(sre.name).
  - Otherwise.
    - Evaluate sre\_list.append(sre.name).
- If sre\_list.
  - Evaluate self.cancel\_stock\_reservation\_entries(sre\_list, notify = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [release unused reserved qty](operations-004.md#op-34b07af2c1f27b), [cancel stock reservation entries](operations-004.md#op-7573a3fd8e2d9f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1187)

<a id="op-34b07af2c1f27b"></a>
### Subcontracting Order.release unused reserved qty

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_order_subcontracting_order_subcontractingorder_release_unused_reserved_qty`

**Inputs** self, sre\_name.

**Declared result** no value.

**Record and data access** resolve a document from “Stock Reservation Entry” via get\_doc.

**State and service calls** call db\_set on sre.

**Local steps**

- Set sre from Platform.get\_doc(“Stock Reservation Entry”, sre\_name).
- Evaluate sre.db\_set(“reserved\_qty”, ((flt(sre.delivered\_qty) + flt(sre.transferred\_qty)) + flt(sre.consumed\_qty))).
- Set sb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Evaluate nested operand in the contract(nested operand in the contract).set(sb\_entry.qty, sb\_entry.delivered\_qty).where(((nested operand in the contract.parenttype equals “Stock Reservation Entry” bitwise and neste ….run().
- Evaluate sre.update\_status().
- Evaluate sre.update\_reserved\_qty\_in\_voucher().
- Evaluate sre.update\_unreserved\_qty\_in\_sre().
- Evaluate sre.update\_reserved\_stock\_in\_bin().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1188)

<a id="op-7573a3fd8e2d9f"></a>
### Subcontracting Order.cancel stock reservation entries

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_subcontracting_order_cancel_stock_reservation_entries`

**Inputs** self, sre\_list = no value, notify = true.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Bind dependencies cancel\_stock\_reservation\_entries.
- Evaluate cancel\_stock\_reservation\_entries(voucher\_type = self.doctype, voucher\_no = self.name, sre\_list = sre\_list, notify = notify).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1490) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L985)

<a id="op-baddfe4a54ab02"></a>
### Update subcontracted qty

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_order_subcontracting_order_update_subcontracted_qty`

**Inputs** work\_order.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**State and service calls** call db\_set on row.

**Local steps**

- Set job\_card from Platform.qb.DocType(“Job Card”).
- Set order from Platform.qb.DocType(“Subcontracting Order”).
- Set order\_item from Platform.qb.DocType(“Subcontracting Order Item”).
- Set supplied\_item from Platform.qb.DocType(“Subcontracting Order Supplied Item”).
- Set qty from Case().when(order.status equals “Closed”, supplied\_item.total\_supplied\_qty).else\_(supplied\_item.required\_qty).
- Set subcontracted from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bi ….run().
- Set subcontracted from mapping of tuple(row at 0, row at 1) → flt(row at 2) for row drawn from subcontracted.
  - Draw row from subcontracted.
- Set doc from Platform.get\_doc(“Work Order”, work\_order).
- Set required from defaultdict(float).
- For each row in doc.required\_items.
  - Update required at tuple(row.operation\_row\_id, row.item\_code) using + flt(row.required\_qty).
- For each row in doc.required\_items.
  - Set key from tuple(row.operation\_row\_id, row.item\_code).
  - Set qty from ((subcontracted.get(key, 0.0) × flt(row.required\_qty)) ÷ required at key) when required at key, otherwise 0.0.
    - Value choice on required at key — true gives ((subcontracted.get(key, 0.0) × flt(row.required\_qty)) ÷ required at key), false gives 0.0.
  - If flt(row.subcontracted\_qty) differs from qty.
    - Evaluate row.db\_set(“subcontracted\_qty”, qty).
- Evaluate doc.update\_reserved\_qty\_for\_production().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1698) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1195)

<a id="op-3cfe8df5a1de1d"></a>
### Make subcontracting receipt

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_make_subcontracting_receipt`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_mapped\_subcontracting\_receipt(source\_name, target\_doc, items = items).

**Local steps**

- Set items from Platform.flags.args.get(“items”) when Platform.flags.args, otherwise no value.
  - Value choice on Platform.flags.args — true gives Platform.flags.args.get(“items”), false gives no value.
- Return get\_mapped\_subcontracting\_receipt(source\_name, target\_doc, items = items).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1484) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L979)

<a id="op-656d577f64fd5a"></a>
### Get mapped subcontracting receipt

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_get_mapped_subcontracting_receipt`

**Inputs** source\_name, target\_doc = no value, items = no value.

**Explicit results** target\_doc.

**Local steps**

- Bind local operation update\_item for subsequent calls.
- Set items from mapping of item at “name” → item at “qty” for item drawn from items when items, otherwise mapping().
  - Value choice on items — true gives mapping of item at “name” → item at “qty” for item drawn from items, false gives mapping().
  - Draw item from items.
- Set target\_doc from get\_mapped\_doc(“Subcontracting Order”, source\_name, mapping(“Subcontracting Order” → mapping(“doctype” → “Subcontracting Receipt”, “field\_map” → mapping(“supplier\_warehouse” → “supplier\_warehouse”, “set\_wa ….
- Return target\_doc.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0954.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1482) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L977)

<a id="op-dc3e0bff4a61fb"></a>
### Get mapped subcontracting receipt.update item

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_get_mapped_subcontracting_receipt_update_item`

**Inputs** source, target, source\_parent.

**Record and data access** read “BOM” via get\_value.

**Local steps**

- Set target.purchase\_order from source\_parent.purchase\_order.
- Set target.purchase\_order\_item from source.purchase\_order\_item.
- Set target.qty from (items.get(source.name) or (flt(source.qty) − flt(source.received\_qty))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in items.get(source.name) → (flt(source.qty) − flt(source.received\_qty)).
- Set target.received\_qty from target.qty.
- If process\_loss\_per bound to Platform.get\_value(“BOM”, source.bom, “process\_loss\_percentage”).
  - Set target.process\_loss\_qty from flt((target.qty × (process\_loss\_per ÷ 100)), target.precision(“process\_loss\_qty”)).
  - Update target.qty using − target.process\_loss\_qty.
- Set target.amount from ((flt(source.qty) − flt(source.received\_qty)) × flt(source.rate)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0954.json#L989) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1483) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L978)

<a id="op-19507bbf388018"></a>
### Set subcontracting order status

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_set_subcontracting_order_status`

**Inputs** sco, status = no value.

**Record and data access** resolve a document from “Subcontracting Order” via get\_doc.

**Local steps**

- If isinstance(sco, str).
  - Set sco from Platform.get\_doc(“Subcontracting Order”, sco).
- Evaluate sco.update\_status(status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0954.json#L1450) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1485) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L980)

<a id="op-6660a3ad61e2a3"></a>
### Update subcontracting order status

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_business_behavior_update_subcontracting_order_status`

**Inputs** sco, status = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Subcontracting Order” via get\_doc.

**Explicit failure paths** validation helper — translated “Cannot set the status of a Subcontracting Order to {0}.”.format(status) · validation helper — translated “Only a submitted Subcontracting Order can be closed or re-opened.”.

**Local steps**

- If (status and status differs from “Closed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status → status differs from “Closed”.
  - Call the validation error handler Platform.throw(translated “Cannot set the status of a Subcontracting Order to {0}.”.format(status)).
- If isinstance(sco, str).
  - Set sco from Platform.get\_doc(“Subcontracting Order”, sco).
- Evaluate sco.check\_permission(“write”).
- <a id="op-6660a3ad61e2a3-guard-10"></a>If sco.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Only a submitted Subcontracting Order can be closed or re-opened.”).
- Evaluate set\_subcontracting\_order\_status(sco, status).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison sco.docstatus differs from 1, sco.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Only a submitted Subcontracting Order can be closed or re-opened.”. With sco.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6660a3ad61e2a3-guard-10)

**Values supplied outside this operation** effective access from sco.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1506) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1001)

<a id="op-92b28824db699d"></a>
### Get data

`operation_enterprise_subcontracting_record_definitions_subcontracting_order_subcontracting_order_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “subcontracting\_order”, “non\_standard\_fieldnames” → mapping(“Stock Reservation Entry” → “voucher\_no”), “transactions” → list(mapping(“label” → translated “Reference”, “items” → list(“ ….

**Local steps**

- Return mapping(“fieldname” → “subcontracting\_order”, “non\_standard\_fieldnames” → mapping(“Stock Reservation Entry” → “voucher\_no”), “transactions” → list(mapping(“label” → translated “Reference”, “items” → list(“ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0954.json#L1811) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1507) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1002)

## Record · Subcontracting receipt

[Record definition](../../../../data/record-types/subcontracting_receipt.json)

<a id="op-de114933a7fa21"></a>
### Subcontracting Receipt.initialize

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.status\_updater from list(mapping(“target\_dt” → “Subcontracting Order Item”, “join\_field” → “subcontracting\_order\_item”, “target\_field” → “received\_qty”, “target\_parent\_dt” → “Subcontracting Order”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0957.json#L4876) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1037)

<a id="op-03dd511183c1e3"></a>
### Subcontracting Receipt.onload

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_onload`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value · read “Stock Settings” via get\_single\_value.

**Local steps**

- Evaluate self.set\_onload(“backflush\_based\_on”, Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”)).
- If self.docstatus equals 1.
  - Evaluate self.set\_onload(“allow\_to\_make\_qc\_after\_submission”, Platform.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”), Platform.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1551) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1041)

<a id="op-bc8de75c15614a"></a>
### Subcontracting Receipt.before validate

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.save\_inventory\_dimensions().
- Evaluate super().before\_validate().
- Evaluate self.validate\_items\_qty().
- Evaluate self.set\_items\_bom().
- Evaluate self.set\_items\_received\_qty().
- Evaluate self.set\_items\_cost\_center().
- If self.company.
  - Set default\_expense\_account from self.get\_company\_default(“default\_expense\_account”, ignore\_validation = true).
  - Evaluate self.set\_service\_expense\_account(default\_expense\_account).
  - Evaluate self.set\_expense\_account\_for\_subcontracted\_items(default\_expense\_account).

If control reaches the end, it returns no value.

**Methods declared on this owner** [save inventory dimensions](operations-005.md#op-95e4982fb2000f), [validate items qty](operations-005.md#op-f392a37410b6a1), [set items bom](operations-005.md#op-dacae14289847f), [set items received qty](operations-005.md#op-0ca441c49b9e1d), [set items cost center](operations-005.md#op-5c8321c36d2162), [set service expense account](operations-005.md#op-f2773eba9e404d), [set expense account for subcontracted items](operations-005.md#op-a9438da97065b0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1026)
