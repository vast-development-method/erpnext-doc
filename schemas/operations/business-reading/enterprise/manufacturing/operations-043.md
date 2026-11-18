# Production · operations 43

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Work order

[Record definition](../../../../data/record-types/work_order.json)

<a id="op-c1cfbba118b404"></a>
### Work Order.set reserved qty for wip and fg

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_set_reserved_qty_for_wip_and_fg`

**Inputs** self, stock\_entry.

**Explicit results** no value.

**Local steps**

- If stock\_entry.is\_return.
  - Return no value.
- Set items from Platform.\_dict().
- Evaluate stock\_entry.reload().
- If (stock\_entry.purpose equals “Manufacture” and (self.sales\_order or self.production\_plan\_sub\_assembly\_item or self.subcontracting\_inward\_order or stock\_entry.job\_card)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in stock\_entry.purpose equals “Manufacture” → (self.sales\_order or self.production\_plan\_sub\_assembly\_item or self.subcontracting\_inward\_order or stock\_entry.job\_card).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.sales\_order → self.production\_plan\_sub\_assembly\_item → self.subcontracting\_inward\_order → stock\_entry.job\_card.
  - Set items from self.get\_finished\_goods\_for\_reservation(stock\_entry).
- Otherwise.
  - If stock\_entry.purpose equals “Material Transfer for Manufacture”.
    - Set items from self.get\_list\_of\_materials\_for\_reservation(stock\_entry).
- If not items.
  - Return no value.
- Set item\_list from list(items.values()).
- Evaluate reserve\_stock\_for\_work\_order(self, item\_list, is\_transfer = false, notify = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get finished goods for reservation](operations-043.md#op-b1adfd33b6fa0d), [get list of materials for reservation](operations-043.md#op-cb4a3ee189626c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L85) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1095)

<a id="op-cb4a3ee189626c"></a>
### Work Order.get list of materials for reservation

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_list_of_materials_for_reservation`

**Inputs** self, stock\_entry.

**Explicit results** items.

**Local steps**

- Set items from Platform.\_dict().
- Set voucher\_detail\_no from mapping of d.item\_code → d.name for d drawn from self.required\_items.
  - Draw d from self.required\_items.
- For each row in stock\_entry.items.
  - If row.item\_code does not belong to items.
    - Set items at row.item\_code from Platform.\_dict(mapping(“voucher\_no” → self.name, “voucher\_type” → self.doctype, “voucher\_detail\_no” → voucher\_detail\_no.get(row.item\_code), “item\_code” → row.item\_code, …)).
  - Otherwise.
    - Update items at row.item\_code at “stock\_qty” using + row.transfer\_qty.
    - If row.serial\_and\_batch\_bundle.
      - Evaluate items at row.item\_code at “serial\_and\_batch\_bundles”.append(row.serial\_and\_batch\_bundle).
- Return items.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L54) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1064)

<a id="op-b1adfd33b6fa0d"></a>
### Work Order.get finished goods for reservation

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_finished_goods_for_reservation`

**Inputs** self, stock\_entry.

**Record and data access** read “Job Card” via get\_value.

**Explicit results** no value · items.

**Local steps**

- Set items from Platform.\_dict().
- If self.production\_plan\_sub\_assembly\_item.
  - Set item\_details from self.get\_wo\_details().
- Otherwise.
  - If self.subcontracting\_inward\_order.
    - Set item\_details from self.get\_scio\_details().
  - Otherwise.
    - If stock\_entry.job\_card.
      - Set finished\_good from Platform.db.get\_value(“Job Card”, stock\_entry.job\_card, “finished\_good”).
      - If finished\_good equals self.production\_item.
        - Return no value.
      - Set item\_details from self.get\_items\_to\_reserve\_for\_job\_card(stock\_entry, finished\_good).
    - Otherwise.
      - Set item\_details from self.get\_so\_details().
- For each item in item\_details.
  - Set qty\_to\_reserve from (flt(item.stock\_qty) − flt((item.stock\_reserved\_qty + item.delivered\_qty))).
  - <a id="op-b1adfd33b6fa0d-guard-22"></a>If qty\_to\_reserve ≤ 0.
    - Continue with the next iteration or loop test.
  - Set warehouse from item.warehouse.
  - If (item.get(“parenttype”) equals “Work Order” and item.get(“skip\_transfer”) and item.get(“from\_wip\_warehouse”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“parenttype”) equals “Work Order” → item.get(“skip\_transfer”) → item.get(“from\_wip\_warehouse”).
    - Set warehouse from item.wip\_warehouse.
  - For each row in stock\_entry.items.
    - If (not row.t\_warehouse or not row.is\_finished\_item or row.t\_warehouse differs from warehouse or row.item\_code differs from item.item\_code).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.t\_warehouse → not row.is\_finished\_item → row.t\_warehouse differs from warehouse → row.item\_code differs from item.item\_code.
      - Continue with the next iteration or loop test.
    - Set reserved\_qty from qty\_to\_reserve.
    - If qty\_to\_reserve &gt; row.transfer\_qty.
      - Set reserved\_qty from row.transfer\_qty.
      - Update qty\_to\_reserve using − row.transfer\_qty.
    - Otherwise.
      - Set qty\_to\_reserve from 0.
    - If row.item\_code does not belong to items.
      - Set items at row.item\_code from Platform.\_dict(mapping(“voucher\_no” → item.voucher\_no, “voucher\_type” → item.voucher\_type, “voucher\_detail\_no” → item.name, “item\_code” → row.item\_code, …)).
    - Otherwise.
      - Update items at row.item\_code at “stock\_qty” using + reserved\_qty.
- Return items.

**Derived branch illustrations**

- At the comparison qty\_to\_reserve ≤ 0, qty\_to\_reserve = 0 selects the branch that continues with the next loop iteration. With qty\_to\_reserve = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-b1adfd33b6fa0d-guard-22)

**Methods declared on this owner** [get wo details](operations-043.md#op-7f8da210e7bc1d), [get scio details](operations-043.md#op-23f01374c89a69), [get items to reserve for job card](operations-043.md#op-315b069f680316), [get so details](operations-043.md#op-a145a80350c91a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L49) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1059)

<a id="op-315b069f680316"></a>
### Work Order.get items to reserve for job card

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_items_to_reserve_for_job_card`

**Inputs** self, stock\_entry, finished\_good.

**Record and data access** read “Work Order Item” via get\_value · read “Stock Reservation Entry” via get\_all.

**Explicit results** item\_details.

**Local steps**

- Set item\_details from list().
- For each row in stock\_entry.items.
  - If row.item\_code equals finished\_good.
    - Set name from Platform.db.get\_value(“Work Order Item”, mapping(“item\_code” → finished\_good, “parent” → self.name), “name”).
    - Set sres from Platform.get\_all(“Stock Reservation Entry”, fields = list(“reserved\_qty”), filters = mapping(“voucher\_no” → self.name, “item\_code” → finished\_good, “voucher\_detail\_no” → name, “warehouse” → row.t\_warehouse, …)).
    - Set pending\_qty from row.qty.
    - For each d in sres.
      - Update pending\_qty using − d.reserved\_qty.
    - If pending\_qty &gt; 0.
      - Set item\_details from list(Platform.\_dict(mapping(“item\_code” → row.item\_code, “stock\_qty” → pending\_qty, “stock\_reserved\_qty” → 0, “warehouse” → row.t\_warehouse, …))).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return item\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L52) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1062)

<a id="op-7f8da210e7bc1d"></a>
### Work Order.get wo details

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_wo_details`

**Inputs** self.

**Explicit results** query.run(as\_dict = 1).

**Local steps**

- Set doctype from Platform.qb.DocType(“Work Order”).
- Set child\_doctype from Platform.qb.DocType(“Work Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(child\_doctype.name, child\_doctype.required\_qty.as\_ ….
- Return query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L61) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1071)

<a id="op-23f01374c89a69"></a>
### Work Order.get scio details

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_scio_details`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order Item” via get\_all.

**Explicit results** Platform.get\_all(“Subcontracting Inward Order Item”, filters = mapping(“name” → self.subcontracting\_inward\_order\_item, “docstatus” → 1), fields = list(“item\_code”, “name”, “qty as stock\_qty”, “produced\_qty ….

**Local steps**

- Return Platform.get\_all(“Subcontracting Inward Order Item”, filters = mapping(“name” → self.subcontracting\_inward\_order\_item, “docstatus” → 1), fields = list(“item\_code”, “name”, “qty as stock\_qty”, “produced\_qty ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L56) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1066)

<a id="op-a145a80350c91a"></a>
### Work Order.get so details

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_so_details`

**Inputs** self.

**Record and data access** read “Sales Order Item” via get\_all.

**Explicit results** Platform.get\_all(“Sales Order Item”, filters = mapping(“parent” → self.sales\_order, “item\_code” → self.production\_item, “docstatus” → 1), fields = list(“item\_code”, “name”, “stock\_qty”, “stock\_reserved\_qty”, …)).

**Local steps**

- Return Platform.get\_all(“Sales Order Item”, filters = mapping(“parent” → self.sales\_order, “item\_code” → self.production\_item, “docstatus” → 1), fields = list(“item\_code”, “name”, “stock\_qty”, “stock\_reserved\_qty”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L57) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1067)

<a id="op-cc6e748f8882c3"></a>
### Work Order.get voucher details

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_voucher_details`

**Inputs** self, stock\_entry.

**Record and data access** read “Sales Order Item” via get\_value.

**Explicit results** Platform.\_dict(vocher\_detail\_no).

**Local steps**

- Set vocher\_detail\_no from mapping().
- If (stock\_entry.purpose equals “Manufacture” and self.sales\_order).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in stock\_entry.purpose equals “Manufacture” → self.sales\_order.
  - Set so\_details from Platform.db.get\_value(“Sales Order Item”, mapping(“parent” → self.sales\_order, “item\_code” → self.production\_item, “docstatus” → 1, “stock\_reserved\_qty” → 0), list(“name”, “stock\_qty”, “stock\_reserved\_qty” ….
  - Set vocher\_detail\_no from mapping(self.production\_item → so\_details).
- Otherwise.
  - Set vocher\_detail\_no from mapping of d.item\_code → d.name for d drawn from self.required\_items.
    - Draw d from self.required\_items.
- Return Platform.\_dict(vocher\_detail\_no).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L60) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1070)

<a id="op-77e7dc52f02b27"></a>
### Work Order.cancel reserved qty for wip and fg

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_cancel_reserved_qty_for_wip_and_fg`

**Inputs** self, ste\_doc.

**Record and data access** read “Stock Reservation Entry” via get\_all · resolve a document from “Stock Reservation Entry” via get\_doc.

**State and service calls** call cancel on sre\_doc · call db\_set on self.

**Local steps**

- Set sre\_list from Platform.get\_all(“Stock Reservation Entry”, filters = mapping(“from\_voucher\_no” → ste\_doc.name, “from\_voucher\_detail\_no” → tuple(“in”, list of row.name for row drawn from ste\_doc.items), “docstatus” → 1),  ….
  - Draw row from ste\_doc.items.
- For each name in sre\_list.
  - Set sre\_doc from Platform.get\_doc(“Stock Reservation Entry”, name).
  - Set sre\_doc.flags.ignore\_permissions from true.
  - Evaluate sre\_doc.cancel().
- If sre\_list.
  - Evaluate self.reload().
  - Evaluate self.db\_set(“status”, self.get\_status()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get status](operations-039.md#op-7a6d94ec35a98e).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L35) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1045)

<a id="op-5f5b7678eb0b1c"></a>
### Work Order.release reserved qty for subcontract transfer

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_release_reserved_qty_for_subcontract_transfer`

**Inputs** self.

**Record and data access** read “Stock Reservation Entry” via get\_all · resolve a document from “Stock Reservation Entry” via get\_doc.

**State and service calls** call db\_set on sre.

**Local steps**

- Set sent from self.\_subcontract\_transferred\_qty\_by\_item().
- Set entries from Platform.get\_all(“Stock Reservation Entry”, filters = mapping(“voucher\_no” → self.name, “voucher\_type” → “Work Order”, “docstatus” → 1), fields = list(“name”, “item\_code”, “warehouse”, “reservation\_based\_o ….
- For each entry in entries.
  - If entry.reservation\_based\_on equals “Serial and Batch”.
    - Continue with the next iteration or loop test.
  - Set key from tuple(entry.item\_code, entry.warehouse).
  - Set sre from Platform.get\_doc(“Stock Reservation Entry”, entry.name).
  - Set available from ((flt(sre.reserved\_qty) − flt(sre.consumed\_qty)) − flt(sre.delivered\_qty)).
  - Set qty\_to\_set from max(min(flt(sent.get(key, 0.0)), available), 0.0).
  - If key belongs to sent.
    - Set sent at key from (flt(sent at key) − qty\_to\_set).
  - If flt(sre.transferred\_qty) equals qty\_to\_set.
    - Continue with the next iteration or loop test.
  - Evaluate sre.db\_set(“transferred\_qty”, qty\_to\_set, update\_modified = false).
  - Evaluate sre.update\_status().
  - Evaluate sre.update\_reserved\_stock\_in\_bin().

If control reaches the end, it returns no value.

**Methods declared on this owner** [subcontract transferred qty by item](operations-043.md#op-e967705f780a98).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L74) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1084)

<a id="op-e967705f780a98"></a>
### Work Order.subcontract transferred qty by item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_subcontract_transferred_qty_by_item`

**Inputs** self.

**Record and data access** read “Job Card” via get\_all · read “Subcontracting Order Item” via get\_all · read “Purchase Order Item” via get\_all.

**Explicit results** mapping() · mapping of tuple(d.item\_code, d.s\_warehouse) → flt(d.qty) for d drawn from rows.

**Local steps**

- Set job\_cards from Platform.get\_all(“Job Card”, filters = mapping(“work\_order” → self.name, “is\_subcontracted” → 1), pluck = “name”).
- If not job\_cards.
  - Return mapping().
- Set sco\_names from Platform.get\_all(“Subcontracting Order Item”, filters = mapping(“job\_card” → list(“in”, job\_cards)), pluck = “parent”).
- Set po\_names from Platform.get\_all(“Purchase Order Item”, filters = mapping(“job\_card” → list(“in”, job\_cards)), pluck = “parent”).
- If (not sco\_names and not po\_names).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not sco\_names → not po\_names.
  - Return mapping().
- Set ste from Platform.qb.DocType(“Stock Entry”).
- Set ste\_child from Platform.qb.DocType(“Stock Entry Detail”).
- Set link from no value.
- If sco\_names.
  - Set link from ste.subcontracting\_order.isin(list(set(sco\_names))).
- If po\_names.
  - Set po\_link from ste.purchase\_order.isin(list(set(po\_names))).
  - Set link from po\_link when link is identical to no value, otherwise (link bitwise or po\_link).
    - Value choice on link is identical to no value — true gives po\_link, false gives (link bitwise or po\_link).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
- Return mapping of tuple(d.item\_code, d.s\_warehouse) → flt(d.qty) for d drawn from rows.
  - Draw d from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L88) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1098)

<a id="op-e71a819d5e8b88"></a>
### Work Order.remove additional items

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_remove_additional_items`

**Inputs** self, stock\_entry.

**Local steps**

- For each row in stock\_entry.items.
  - For each item in self.required\_items.
    - If ((row.original\_item or row.item\_code) equals item.item\_code and row.name equals item.voucher\_detail\_reference).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in (row.original\_item or row.item\_code) equals item.item\_code → row.name equals item.voucher\_detail\_reference.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.original\_item → row.item\_code.
      - Evaluate item.delete().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L807)

<a id="op-e9320492e3f0e1"></a>
### Work Order.add additional items

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_add_additional_items`

**Inputs** self, stock\_entry.

**Record and data access** read “Manufacturing Settings” via get\_single\_value · read “Job Card” via get\_cached\_value.

**State and service calls** call insert on child\_row.

**Explicit results** no value.

**Local steps**

- If Platform.db.get\_single\_value(“Manufacturing Settings”, “validate\_components\_quantities\_per\_bom”).
  - Return no value.
- If stock\_entry.purpose differs from “Material Transfer for Manufacture”.
  - Return no value.
- If (stock\_entry.job\_card and Platform.get\_cached\_value(“Job Card”, stock\_entry.job\_card, “is\_corrective\_job\_card”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in stock\_entry.job\_card → Platform.get\_cached\_value(“Job Card”, stock\_entry.job\_card, “is\_corrective\_job\_card”).
  - Return no value.
- Set required\_items from list of d.item\_code for d drawn from self.required\_items.
  - Draw d from self.required\_items.
- Set additional\_items from Platform.\_dict().
- For each row in stock\_entry.items.
  - Set item\_code from (row.original\_item or row.item\_code).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.original\_item → row.item\_code.
  - If item\_code does not belong to required\_items.
    - Evaluate additional\_items.setdefault(item\_code, list()).append(row).
- For each tuple(item\_code, rows) in additional\_items.items().
  - For each row in rows.
    - Set child\_row from self.append(“required\_items”, mapping(“item\_code” → item\_code, “source\_warehouse” → row.s\_warehouse, “item\_name” → row.item\_name, “required\_qty” → row.transfer\_qty, …)).
    - Evaluate child\_row.insert().
  - Evaluate stock\_entry.reload().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “validate\_components\_quantities\_per\_bom”), Platform.get\_cached\_value(“Job Card”, stock\_entry.job\_card, “is\_corrective\_job\_card”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L787)

<a id="op-f6a51379898415"></a>
### Make stock reservation entries

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_make_stock_reservation_entries`

**Inputs** doc, items = no value, is\_transfer = true, notify = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Local steps**

- If isinstance(doc, str).
  - Set doc from parse\_json(doc).
  - Set doc from Platform.get\_doc(“Work Order”, doc.get(“name”)).
- Evaluate Platform.has\_permission(“Work Order”, “write”, doc = doc, throw = true).
- Evaluate reserve\_stock\_for\_work\_order(doc, items, is\_transfer, notify).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Work Order”, “write”, doc = doc, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L14) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1024)

<a id="op-c35baecb5ebd52"></a>
### Reserve stock for work order

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_reserve_stock_for_work_order`

**Inputs** doc, items = no value, is\_transfer = true, notify = false.

**State and service calls** msgprint with translated “Stock Reservation Entries Created” · call db\_set on doc.

**Local steps**

- Set is\_transfer from cint(is\_transfer).
- If (items and isinstance(items, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in items → isinstance(items, str).
  - Set items from parse\_json(items).
- Set sre from StockReservation(doc, items = items).
- If (doc.docstatus equals 2 or doc.status equals “Closed”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.docstatus equals 2 → doc.status equals “Closed”.
  - Evaluate sre.cancel\_stock\_reservation\_entries().
- Otherwise.
  - If doc.docstatus equals 1.
    - If (doc.production\_plan and is\_transfer).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.production\_plan → is\_transfer.
      - Evaluate sre.transfer\_reservation\_entries\_to(doc.production\_plan, from\_doctype = “Production Plan”, to\_doctype = “Work Order”).
    - Otherwise.
      - If (doc.subcontracting\_inward\_order and is\_transfer).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.subcontracting\_inward\_order → is\_transfer.
        - Evaluate doc.set\_qty\_change().
        - Evaluate sre.transfer\_reservation\_entries\_to(doc.subcontracting\_inward\_order, from\_doctype = “Subcontracting Inward Order”, to\_doctype = “Work Order”, against\_fg\_item = doc.subcontracting\_inward\_order\_item, qty\_cha ….
      - Otherwise.
        - Set sre\_created from sre.make\_stock\_reservation\_entries().
        - If sre\_created.
          - Evaluate Platform.msgprint(translated “Stock Reservation Entries Created”, alert = true).
- Evaluate doc.reload().
- Evaluate doc.db\_set(“status”, doc.get\_status()).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L21) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1031)

<a id="op-c0d24a671f4437"></a>
### Cancel stock reservation entries

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_cancel_stock_reservation_entries`

**Inputs** doc, sre\_list.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Local steps**

- If isinstance(doc, str).
  - Set doc from parse\_json(doc).
  - Set doc from Platform.get\_doc(“Work Order”, doc.get(“name”)).
- Evaluate Platform.has\_permission(“Work Order”, “write”, doc = doc, throw = true).
- If isinstance(sre\_list, str).
  - Set sre\_list from parse\_json(sre\_list).
- Evaluate unreserve\_stock\_for\_work\_order(doc, sre\_list).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Work Order”, “write”, doc = doc, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L992)

<a id="op-8f3529550922af"></a>
### Unreserve stock for work order

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_unreserve_stock_for_work_order`

**Inputs** doc, sre\_list.

**State and service calls** call db\_set on doc.

**Local steps**

- Set sre from StockReservation(doc).
- Evaluate sre.cancel\_stock\_reservation\_entries(sre\_list).
- Evaluate doc.reload().
- Evaluate doc.db\_set(“status”, doc.get\_status()).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L27) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1037)

<a id="op-33602619ce3c1a"></a>
### Get sre details

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_sre_details`

**Inputs** work\_order.

**Record and data access** read “Stock Reservation Entry” via get\_all.

**Explicit results** sre\_details.

**Local steps**

- Set sre\_details from Platform.\_dict().
- Set data from Platform.get\_all(“Stock Reservation Entry”, filters = mapping(“voucher\_no” → work\_order, “docstatus” → 1), fields = list(“item\_code”, “warehouse”, “reserved\_qty”, “transferred\_qty”, …)).
- For each row in data.
  - If row.voucher\_detail\_no does not belong to sre\_details.
    - Evaluate sre\_details.setdefault(row.voucher\_detail\_no, row).
  - Otherwise.
    - Update sre\_details at row.voucher\_detail\_no.reserved\_qty using + row.reserved\_qty.
    - Update sre\_details at row.voucher\_detail\_no.transferred\_qty using + row.transferred\_qty.
    - Update sre\_details at row.voucher\_detail\_no.consumed\_qty using + row.consumed\_qty.
- Return sre\_details.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L4) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1014)

<a id="op-0aae979d2e665f"></a>
### Get consumed qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_consumed_qty`

**Inputs** work\_order, item\_code.

**Explicit results** flt(result at 0 at 0) when result, otherwise 0.

**Local steps**

- Set stock\_entry from Platform.qb.DocType(“Stock Entry”).
- Set stock\_entry\_detail from Platform.qb.DocType(“Stock Entry Detail”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(nested operand in the contract.Sum(nested operand  ….
- Set result from query.run().
- Return flt(result at 0 at 0) when result, otherwise 0.
  - Value choice on result — true gives flt(result at 0 at 0), false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1762) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1002)

<a id="op-0052f9c7f2c1bd"></a>
### Get work order allocated qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_work_order_allocated_qty`

**Inputs** scio\_item\_name, rm\_item\_codes.

**Declared result** dict at tuple(str, float).

**Explicit results** dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(work\_order\_item.item\_code).run()).

**Local steps**

- Set work\_order from Platform.qb.DocType(“Work Order”).
- Set work\_order\_item from Platform.qb.DocType(“Work Order Item”).
- Return dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(work\_order\_item.item\_code).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L7) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1017)

<a id="op-5ee8f4875e560a"></a>
### Get bom operations

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_get_bill_of_materials_operations`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read parenttype via exists · read “BOM Operation” via get\_all.

**Explicit results** list() · Platform.get\_all(“BOM Operation”, filters = filters, fields = list(“operation”), as\_list = 1).

**Local steps**

- Set parent from filters.get(“parent”).
- Set parenttype from (filters.get(“parenttype”) or “BOM”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“parenttype”) → “BOM”.
- If (not parent or not Platform.db.exists(parenttype, parent)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent → not Platform.db.exists(parenttype, parent).
  - Return list().
- Set ptype from “select” when Platform.only\_has\_select\_perm(parenttype), otherwise “read”.
  - Value choice on Platform.only\_has\_select\_perm(parenttype) — true gives “select”, false gives “read”.
- Evaluate Platform.has\_permission(parenttype, ptype, doc = parent, throw = true).
- If txt.
  - Set filters at “operation” from tuple(“like”, (“%%%s%%” modulo or format txt)).
- Return Platform.get\_all(“BOM Operation”, filters = filters, fields = list(“operation”), as\_list = 1).

**Values supplied outside this operation** effective access from Platform.has\_permission(parenttype, ptype, doc = parent, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L781)

<a id="op-7a8bf4eb03d107"></a>
### Get item details

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_item_details`

**Inputs** item, project = no value, skip\_bom\_info = false, throw = true.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** execute query text (SELECT, Item) · read “BOM” via get\_value · read “Item” via get\_value.

**State and service calls** msgprint with translated “Default BOM not found for Item {0} and Project {1}”.format(item, project) · msgprint with msg.

**Explicit results** mapping() · res.

**Local steps**

- Evaluate Platform.has\_permission(“Item”, “read”, doc = item, throw = true).
- Set res from Platform.db.sql(query text (SELECT, Item), tuple(nowdate(), item), as\_dict = 1).
- If not res.
  - Return mapping().
- Set res from res at 0.
- If skip\_bom\_info.
  - Return res.
- Set filters from mapping(“item” → item, “is\_default” → 1, “docstatus” → 1).
- If project.
  - Set filters from mapping(“item” → item, “project” → project).
- Set res at “bom\_no” from Platform.db.get\_value(“BOM”, filters = filters).
- If not res at “bom\_no”.
  - Set variant\_of from Platform.db.get\_value(“Item”, item, “variant\_of”).
  - If variant\_of.
    - Set res at “bom\_no” from Platform.db.get\_value(“BOM”, filters = mapping(“item” → variant\_of, “is\_default” → 1)).
- If not res at “bom\_no”.
  - If project.
    - Set res from get\_item\_details(item, throw = throw).
    - Evaluate Platform.msgprint(translated “Default BOM not found for Item {0} and Project {1}”.format(item, project), alert = 1).
  - Otherwise.
    - Set msg from translated “Default BOM for {0} not found”.format(item).
    - Evaluate Platform.msgprint(msg, raise\_exception = throw, indicator = “yellow”, alert = not throw).
    - Return res.
- Set bom\_data from Platform.db.get\_value(“BOM”, res at “bom\_no”, list(“project”, “allow\_alternative\_item”, “transfer\_material\_against”, “item\_name”), as\_dict = 1).
- Set res at “project” from (project or bom\_data.pop(“project”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in project → bom\_data.pop(“project”).
- Evaluate res.update(bom\_data).
- Evaluate res.update(check\_if\_scrap\_warehouse\_mandatory(res at “bom\_no”)).
- Return res.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “read”, doc = item, throw = true) · clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1764) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1004)

<a id="op-c88884afb7cd7f"></a>
### Make work order

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_make_work_order`

**Inputs** bom\_no, item, qty = 0, company = no value, project = no value, variant\_items = no value, use\_multi\_level\_bom = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_value · read “BOM” via get\_value.

**State and service calls** request new\_doc for “Work Order”.

**Explicit results** wo\_doc.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- Bind dependencies get\_default\_company.
- If not Platform.has\_permission(“Work Order”, “write”).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set item\_details from get\_item\_details(item, project).
- If (Platform.db.get\_value(“Item”, item, “variant\_of”) and Platform.db.get\_value(“BOM”, bom\_no, “item”) differs from item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_value(“Item”, item, “variant\_of”) → Platform.db.get\_value(“BOM”, bom\_no, “item”) differs from item.
  - If variant\_bom bound to Platform.db.get\_value(“BOM”, mapping(“item” → item, “is\_default” → 1, “docstatus” → 1)).
    - Set bom\_no from variant\_bom.
- Set wo\_doc from Platform.new\_doc(“Work Order”).
- Set wo\_doc.track\_semi\_finished\_goods from Platform.db.get\_value(“BOM”, bom\_no, “track\_semi\_finished\_goods”).
- Set wo\_doc.production\_item from item.
- Set wo\_doc.company from (company or get\_default\_company()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in company → get\_default\_company().
- Evaluate wo\_doc.update(item\_details).
- Set wo\_doc.bom\_no from bom\_no.
- Set wo\_doc.use\_multi\_level\_bom from cint(use\_multi\_level\_bom).
- If flt(qty) &gt; 0.
  - Set wo\_doc.qty from flt(qty).
  - Evaluate wo\_doc.get\_items\_and\_operations\_from\_bom().
- If (variant\_items and not wo\_doc.use\_multi\_level\_bom).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in variant\_items → not wo\_doc.use\_multi\_level\_bom.
  - Evaluate add\_variant\_item(variant\_items, wo\_doc, bom\_no, “required\_items”).
- Return wo\_doc.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Work Order”, “write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L16) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1026)

<a id="op-159deb1c7f74e6"></a>
### Add variant item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_add_variant_item`

**Inputs** variant\_items, wo\_doc, bom\_no, table\_name = “items”.

**Record and data access** resolve a document from “BOM” via get\_cached\_doc.

**Local steps**

- If isinstance(variant\_items, str).
  - Set variant\_items from json.loads(variant\_items).
- For each item in variant\_items.
  - Set args from Platform.\_dict(mapping(“item\_code” → item.get(“variant\_item\_code”), “source\_warehouse” → item.get(“source\_warehouse”), “operation” → item.get(“operation”))).
  - Set bom\_doc from Platform.get\_cached\_doc(“BOM”, bom\_no).
  - Set item\_data from get\_item\_details(args.item\_code, skip\_bom\_info = true).
  - Evaluate args.update(item\_data).
  - Evaluate args.update(\_variant\_row\_qty(args.item\_code, item, item\_data.stock\_uom)).
  - Set args at “rate” from get\_raw\_material\_rate(args, wo\_doc, bom\_doc).
  - If not args.source\_warehouse.
    - Set args at “source\_warehouse” from get\_item\_defaults(item.get(“variant\_item\_code”), wo\_doc.company).default\_warehouse.
  - Set args at “amount” from (flt(args.get(“required\_qty”)) × flt(args.get(“rate”))).
  - If table\_name differs from “required\_items”.
    - Set args at “rate” from flt((args.rate × args.conversion\_factor), Platform.get\_precision(“BOM Item”, “rate”)).
    - Evaluate wo\_doc.append(table\_name, args).
    - Continue with the next iteration or loop test.
  - Set existing\_row from get\_template\_rm\_item(wo\_doc, item.get(“item\_code”)).
  - If existing\_row.
    - Evaluate existing\_row.update(args).
  - Otherwise.
    - Evaluate wo\_doc.append(table\_name, args).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“BOM”, bom\_no).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L989)
