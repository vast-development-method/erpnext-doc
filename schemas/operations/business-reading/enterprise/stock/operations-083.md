# Inventory and warehouses · operations 83

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock entry

[Record definition](../../../../data/record-types/stock_entry.json)

<a id="op-71a15391fcc3c0"></a>
### Stock Entry.get secondary items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_secondary_items`

**Inputs** self, qty.

**Record and data access** read “Manufacturing Settings” via get\_single\_value · read “Work Order” via get\_cached\_value.

**Explicit results** item\_dict.

**Local steps**

- Bind dependencies get\_bom\_items\_as\_dict.
- If (Platform.db.get\_single\_value(“Manufacturing Settings”, “set\_op\_cost\_and\_secondary\_items\_from\_sub\_assemblies”) and self.work\_order and Platform.get\_cached\_value(“Work Order”, self.work\_order, “use\_multi\_level\_bom”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_single\_value(“Manufacturing Settings”, “set\_op\_cost\_and\_secondary\_items\_from\_sub\_assemblies”) → self.work\_order → Platform.get\_cached\_value(“Work Order”, self.work\_order, “use\_multi\_level\_bom”).
  - Set item\_dict from get\_secondary\_items\_from\_sub\_assemblies(self.bom\_no, self.company, qty).
- Otherwise.
  - Set item\_dict from (get\_bom\_items\_as\_dict(self.bom\_no, self.company, qty = qty, fetch\_exploded = 0, fetch\_secondary\_items = 1) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_bom\_items\_as\_dict(self.bom\_no, self.company, qty = qty, fetch\_exploded = 0, fetch\_secondary\_items = 1) → mapping().
- For each item in item\_dict.values().
  - Set item.from\_warehouse from empty text.
- Return item\_dict.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “set\_op\_cost\_and\_secondary\_items\_from\_sub\_assemblies”), Platform.get\_cached\_value(“Work Order”, self.work\_order, “use\_multi\_level\_bom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L711)

<a id="op-c77d7087645fae"></a>
### Stock Entry.set secondary items from job card

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_secondary_items_from_job_card`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- <a id="op-c77d7087645fae-guard-2"></a>If self.purpose does not belong to list(“Manufacture”, “Repack”).
  - Return no value.
- Set item\_dict from mapping().
- Set rows from list of row for row drawn from self.get\_secondary\_items\_from\_job\_card() where row.stock\_qty &gt; 0.
  - Draw row from self.get\_secondary\_items\_from\_job\_card(), keep a combination only if (row.stock\_qty &gt; 0).
- Set bom\_rows from self.get\_bom\_secondary\_item\_details(rows).
- For each row in rows.
  - Set bom\_row from bom\_rows.get(row.bom\_secondary\_item, Platform.\_dict()).
  - Set entry from Platform.\_dict(mapping(“item\_code” → row.item\_code, “uom” → row.stock\_uom, “from\_warehouse” → empty text, “qty” → row.stock\_qty, …)).
  - If entry.valuation\_type equals “Manual”.
    - Set entry.manual\_rate from (flt(bom\_row.base\_cost) ÷ flt(bom\_row.stock\_qty)) when flt(bom\_row.get(“stock\_qty”)), otherwise 0.
      - Value choice on flt(bom\_row.get(“stock\_qty”)) — true gives (flt(bom\_row.base\_cost) ÷ flt(bom\_row.stock\_qty)), false gives 0.
  - Set item\_dict at get\_secondary\_item\_key(row) from entry.
- For each item in item\_dict.values().
  - Set item.from\_warehouse from empty text.
- Evaluate self.add\_to\_stock\_entry\_detail(item\_dict).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.purpose does not belong to list(“Manufacture”, “Repack”), self.purpose = “Material Issue” selects the branch that returns no value. With self.purpose = “Manufacture”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c77d7087645fae-guard-2)

**Methods declared on this owner** [get secondary items from job card](operations-083.md#op-a70ac58cbceb38), [get bom secondary item details](operations-083.md#op-0b6e8b32a0e4f7), [add to stock entry detail](operations-083.md#op-e7c2657477c713).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L735)

<a id="op-0b6e8b32a0e4f7"></a>
### Stock Entry.get bom secondary item details

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_bom_secondary_item_details`

**Inputs** self, secondary\_items.

**Declared result** dict.

**Record and data access** read “BOM Secondary Item” via get\_all.

**Explicit results** mapping() · mapping of row.name → row for row drawn from Platform.get\_all(“BOM Secondary Item”, filters = mapping(“name” → tuple(“in”, names)), fields = list(“name”, “valuation\_type”, “base\_cost”, “stock\_qty”)).

**Local steps**

- Set names from list of row.bom\_secondary\_item for row drawn from secondary\_items where row.bom\_secondary\_item.
  - Draw row from secondary\_items, keep a combination only if (row.bom\_secondary\_item).
- If not names.
  - Return mapping().
- Return mapping of row.name → row for row drawn from Platform.get\_all(“BOM Secondary Item”, filters = mapping(“name” → tuple(“in”, names)), fields = list(“name”, “valuation\_type”, “base\_cost”, “stock\_qty”)).
  - Draw row from Platform.get\_all(“BOM Secondary Item”, filters = mapping(“name” → tuple(“in”, names)), fields = list(“name”, “valuation\_type”, “base\_cost”, “stock\_qty”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L692)

<a id="op-a70ac58cbceb38"></a>
### Stock Entry.get secondary items from job card

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_secondary_items_from_job_card`

**Inputs** self.

**Record and data access** read “UOM” via get\_cached\_value.

**Explicit results** list() · other.

**Local steps**

- If not hasattr(self, “pro\_doc”).
  - Set self.pro\_doc from no value.
- If not self.pro\_doc.
  - Evaluate self.set\_work\_order\_details().
- If not self.pro\_doc.operations.
  - Return list().
- Set job\_card from Platform.qb.DocType(“Job Card”).
- Set job\_card\_secondary\_item from Platform.qb.DocType(“Job Card Secondary Item”).
- Set other from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op ….
- If self.job\_card.
  - Set other from other.where(job\_card.name equals self.job\_card).
- Set other from other.run(as\_dict = 1).
- If self.job\_card.
  - Set pending\_qty from flt(self.fg\_completed\_qty).
- Otherwise.
  - Set pending\_qty from (flt(self.get\_completed\_job\_card\_qty()) − flt(self.pro\_doc.produced\_qty)).
- Set used\_secondary\_items from self.get\_used\_secondary\_items().
- For each row in other.
  - Set key from get\_secondary\_item\_key(row).
  - Update row.stock\_qty using − flt(used\_secondary\_items.get(key)).
  - Set row.stock\_qty from ((row.stock\_qty × flt(self.fg\_completed\_qty)) ÷ flt(pending\_qty)).
  - If cint(Platform.get\_cached\_value(“UOM”, row.stock\_uom, “must\_be\_whole\_number”)).
    - Set row.stock\_qty from Platform.utils.ceil(row.stock\_qty).
- Return other.

**Methods declared on this owner** [set work order details](operations-082.md#op-759b32c5cade62), [get completed job card qty](operations-083.md#op-7a2b5e152c8e50), [get used secondary items](operations-083.md#op-58e43d46b46027).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, row.stock\_uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L712)

<a id="op-7a2b5e152c8e50"></a>
### Stock Entry.get completed job card qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_completed_job_card_qty`

**Inputs** self.

**Explicit results** flt(min(list of d.completed\_qty for d drawn from self.pro\_doc.operations)).

**Local steps**

- Return flt(min(list of d.completed\_qty for d drawn from self.pro\_doc.operations)).
  - Draw d from self.pro\_doc.operations.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L693)

<a id="op-58e43d46b46027"></a>
### Stock Entry.get used secondary items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_used_secondary_items`

**Inputs** self.

**Explicit results** used\_secondary\_items.

**Local steps**

- Set used\_secondary\_items from defaultdict(float).
- Set StockEntry from Platform.qb.DocType(“Stock Entry”).
- Set StockEntryDetail from Platform.qb.DocType(“Stock Entry Detail”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(StockEntryDetail.item\_code, StockEntryDetail.secon ….
- If self.job\_card.
  - Set query from query.where(StockEntry.job\_card equals self.job\_card).
- For each row in query.run(as\_dict = 1).
  - Update used\_secondary\_items at get\_secondary\_item\_key(row) using + row.qty.
- Return used\_secondary\_items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1223) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L720)

<a id="op-987595ea7d3553"></a>
### Stock Entry.get unconsumed raw materials

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_unconsumed_raw_materials`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc · read “Work Order Item” via get\_all.

**Local steps**

- Set wo from Platform.get\_doc(“Work Order”, self.work\_order).
- Set wo\_items from Platform.get\_all(“Work Order Item”, filters = mapping(“parent” → self.work\_order), fields = list(“item\_code”, “source\_warehouse”, “required\_qty”, “consumed\_qty”, …)).
- Set work\_order\_qty from (wo.material\_transferred\_for\_manufacturing or wo.qty).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in wo.material\_transferred\_for\_manufacturing → wo.qty.
- Set alternative\_items from get\_alternative\_items\_for\_work\_order(self.work\_order, list of item.item\_code for item drawn from wo\_items, exclude\_stock\_entry = no value when self.is\_new(), otherwise self.name).
  - Draw item from wo\_items.
  - Value choice on self.is\_new() — true gives no value, false gives self.name.
- For each item in wo\_items.
  - Set item\_account\_details from get\_item\_defaults(item.item\_code, self.company).
  - Set wo\_item\_qty from (item.transferred\_qty or item.required\_qty).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.transferred\_qty → item.required\_qty.
  - Set wo\_qty\_unconsumed from (flt(wo\_item\_qty) − flt(item.consumed\_qty)).
  - Set wo\_qty\_to\_produce from (flt(work\_order\_qty) − flt(wo.produced\_qty)).
  - Set bom\_qty\_per\_unit from (item.required\_qty ÷ wo.qty).
  - Set req\_qty\_each from (wo\_qty\_unconsumed ÷ (wo\_qty\_to\_produce or 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in wo\_qty\_to\_produce → 1.
  - Set req\_qty\_each from min(req\_qty\_each, bom\_qty\_per\_unit).
  - Set qty from (req\_qty\_each × flt(self.fg\_completed\_qty)).
  - If qty &gt; 0.
    - Set item\_row from mapping(“from\_warehouse” → (wo.wip\_warehouse or item.source\_warehouse), “to\_warehouse” → empty text, “qty” → qty, “item\_name” → item.item\_name, …).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in wo.wip\_warehouse → item.source\_warehouse.
    - Set materials from alternative\_items.get(item.item\_code).
    - Set split from split\_qty\_by\_alternative\_items(qty, materials) when materials, otherwise list().
      - Value choice on materials — true gives split\_qty\_by\_alternative\_items(qty, materials), false gives list().
    - If not split.
      - Evaluate self.add\_to\_stock\_entry\_detail(mapping(item.item\_code → item\_row)).
      - Continue with the next iteration or loop test.
    - For each tuple(material, material\_qty) in split.
      - If not material.original\_item.
        - Evaluate self.add\_to\_stock\_entry\_detail(mapping(item.item\_code → mapping(expand item\_row, “qty” → material\_qty))).
        - Continue with the next iteration or loop test.
      - Evaluate self.add\_to\_stock\_entry\_detail(mapping(tuple(material.item\_code, item.item\_code) → mapping(expand item\_row, “item\_code” → material.item\_code, “item\_name” → material.item\_name, “description” → material.desc ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [add to stock entry detail](operations-083.md#op-e7c2657477c713).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1221) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L718)

<a id="op-29a61e18a684e5"></a>
### Stock Entry.add transfered raw materials in items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_add_transfered_raw_materials_in_items`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Work Order” via get\_value · read “UOM” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- Set available\_materials from get\_available\_materials(self.work\_order).
- Set wo\_data from Platform.db.get\_value(“Work Order”, self.work\_order, list(“qty”, “produced\_qty”, “process\_loss\_qty”, “material\_transferred\_for\_manufacturing as trans\_qty”), as\_dict = 1).
- Set transferred\_qty from flt(wo\_data.trans\_qty).
- Set pending\_qty\_to\_mfg from ((transferred\_qty − flt(wo\_data.produced\_qty)) − flt(wo\_data.process\_loss\_qty)).
- Set fg\_completed\_qty from flt(self.fg\_completed\_qty).
- Set fg\_precision from self.precision(“fg\_completed\_qty”).
- If (not self.is\_return and (flt(pending\_qty\_to\_mfg, fg\_precision) ≤ 0 or not fg\_completed\_qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_return → (flt(pending\_qty\_to\_mfg, fg\_precision) ≤ 0 or not fg\_completed\_qty).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(pending\_qty\_to\_mfg, fg\_precision) ≤ 0 → not fg\_completed\_qty.
  - Return no value.
- Set precision from Platform.get\_precision(“Stock Entry Detail”, “qty”).
- For each tuple(\_key, row) in available\_materials.items().
  - Set pending\_qty from (transferred\_qty − sum(row.consumed\_for.values())).
  - If flt((min(pending\_qty\_to\_mfg, pending\_qty) − fg\_completed\_qty), fg\_precision) ≤ 0.
    - Set pending\_qty from fg\_completed\_qty.
  - Set qty from flt(row.qty).
  - If not self.is\_return.
    - Set qty from ((flt(row.qty) × fg\_completed\_qty) ÷ pending\_qty).
  - Set item from row.item\_details.
  - If cint(Platform.get\_cached\_value(“UOM”, item.stock\_uom, “must\_be\_whole\_number”)).
    - Set qty from Platform.utils.ceil(qty).
  - If row.batch\_details.
    - Set row.batches\_to\_be\_consume from defaultdict(float).
    - Set batches from self.get\_batches\_to\_consume(row, qty).
    - Evaluate self.update\_batches\_to\_be\_consume(batches, row, qty).
  - Otherwise.
    - If row.serial\_nos.
      - Set serial\_nos from row.serial\_nos at slice 0 to cint(qty).
      - Set row.serial\_nos from serial\_nos.
  - If flt(qty, precision) differs from 0.0.
    - Evaluate self.update\_item\_in\_stock\_entry\_detail(row, item, qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get batches to consume](operations-083.md#op-7d99163b3ae201), [update batches to be consume](operations-083.md#op-a8b854d36e8071), [update item in stock entry detail](operations-083.md#op-fdf4dbe5877bba).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, item.stock\_uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1177) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L674)

<a id="op-7d99163b3ae201"></a>
### Stock Entry.get batches to consume

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_batches_to_consume`

**Inputs** self, row, qty.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** row.batch\_details · batches.

**Local steps**

- If not Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).
  - Return row.batch\_details.
- Set unreserved\_qty from self.get\_unreserved\_batch\_qty(row).
- Set batches from mapping of batch\_no → min(batch\_qty, unreserved\_qty at batch\_no) for tuple(batch\_no, batch\_qty) drawn from row.batch\_details.items() where (batch\_qty &gt; 0 and batch\_no belongs to unreserved\_qty).
  - Draw tuple(batch\_no, batch\_qty) from row.batch\_details.items(), keep a combination only if ((batch\_qty &gt; 0 and batch\_no belongs to unreserved\_qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_qty &gt; 0 → batch\_no belongs to unreserved\_qty.
- Set precision from Platform.get\_precision(“Stock Entry Detail”, “qty”).
- If flt(sum(batches.values()), precision) ≥ flt(qty, precision).
  - Return batches.
- Return row.batch\_details.

**Methods declared on this owner** [get unreserved batch qty](operations-083.md#op-a1aa10f43712db).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1192) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L689)

<a id="op-a1aa10f43712db"></a>
### Stock Entry.get unreserved batch qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_unreserved_batch_qty`

**Inputs** self, row.

**Explicit results** mapping of batch.batch\_no → batch.qty for batch drawn from batches.

**Local steps**

- Bind dependencies get\_auto\_batch\_nos.
- Set batches from get\_auto\_batch\_nos(Platform.\_dict(item\_code = row.item\_details.item\_code, warehouse = row.item\_details.warehouse, batch\_no = list(row.batch\_details), posting\_date = self.posting\_date, …)).
- Return mapping of batch.batch\_no → batch.qty for batch drawn from batches.
  - Draw batch from batches.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L719)

<a id="op-99a9240dde1336"></a>
### Stock Entry.work order reservations

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_work_order_reservations`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Record and data access** read “Stock Reservation Entry” via get\_all.

**Explicit results** Platform.get\_all(“Stock Reservation Entry”, filters = mapping(“voucher\_type” → “Work Order”, “voucher\_no” → self.work\_order, “docstatus” → 1), pluck = “name”).

**Local steps**

- Return Platform.get\_all(“Stock Reservation Entry”, filters = mapping(“voucher\_type” → “Work Order”, “voucher\_no” → self.work\_order, “docstatus” → 1), pluck = “name”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1285) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L782)

<a id="op-a8b854d36e8071"></a>
### Stock Entry.update batches to be consume

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_update_batches_to_be_consume`

**Inputs** self, batches, row, qty.

**Local steps**

- Set qty\_to\_be\_consumed from qty.
- Set batches from sorted(batches.items(), key = deferred anonymous expression).
- For each tuple(batch\_no, batch\_qty) in batches.
  - If (qty\_to\_be\_consumed ≤ 0 or batch\_qty ≤ 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in qty\_to\_be\_consumed ≤ 0 → batch\_qty ≤ 0.
    - Continue with the next iteration or loop test.
  - If batch\_qty &gt; qty\_to\_be\_consumed.
    - Set batch\_qty from qty\_to\_be\_consumed.
  - Update row.batches\_to\_be\_consume at batch\_no using + batch\_qty.
  - If (batch\_no and row.serial\_nos).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_no → row.serial\_nos.
    - Set serial\_nos from self.get\_serial\_nos\_based\_on\_transferred\_batch(batch\_no, row.serial\_nos).
    - Set serial\_nos from serial\_nos at slice 0 to cint(batch\_qty).
    - For each sn in serial\_nos.
      - Evaluate row.serial\_nos.remove(sn).
  - If “batch\_details” belongs to row.
    - Update row.batch\_details at batch\_no using − batch\_qty.
  - Update qty\_to\_be\_consumed using − batch\_qty.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get serial nos based on transferred batch](operations-083.md#op-309d9211c53f5c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L744)

<a id="op-fdf4dbe5877bba"></a>
### Stock Entry.update item in stock entry detail

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_update_item_in_stock_entry_detail`

**Inputs** self, row, item, qty.

**Declared result** no value.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not qty.
  - Return no value.
- Set use\_serial\_batch\_fields from Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).
- Set ste\_item\_details from mapping(“from\_warehouse” → item.warehouse, “to\_warehouse” → empty text, “qty” → qty, “item\_name” → item.item\_name, …).
  - Value choice on not use\_serial\_batch\_fields — true gives create\_serial\_and\_batch\_bundle(self, row, item, “Outward”), false gives empty text.
  - Value choice on (row.serial\_nos and not row.batches\_to\_be\_consume) — true gives whitespace '\\n'.join(row.serial\_nos), false gives empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.serial\_nos → not row.batches\_to\_be\_consume.
- If self.is\_return.
  - Set ste\_item\_details at “to\_warehouse” from item.s\_warehouse.
- If (use\_serial\_batch\_fields and not row.serial\_no and row.batches\_to\_be\_consume).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in use\_serial\_batch\_fields → not row.serial\_no → row.batches\_to\_be\_consume.
  - For each tuple(batch\_no, batch\_qty) in row.batches\_to\_be\_consume.items().
    - Evaluate ste\_item\_details.update(mapping(“batch\_no” → batch\_no, “qty” → batch\_qty)).
    - If row.serial\_nos.
      - Set serial\_nos from row.serial\_nos at slice 0 to cint(batch\_qty).
      - Set ste\_item\_details at “serial\_no” from whitespace '\\n'.join(serial\_nos).
      - Set row.serial\_nos from list of sn for sn drawn from row.serial\_nos where sn does not belong to serial\_nos.
        - Draw sn from row.serial\_nos, keep a combination only if (sn does not belong to serial\_nos).
    - Evaluate self.add\_to\_stock\_entry\_detail(mapping(item.item\_code → ste\_item\_details)).
- Otherwise.
  - Evaluate self.add\_to\_stock\_entry\_detail(mapping(item.item\_code → ste\_item\_details)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add to stock entry detail](operations-083.md#op-e7c2657477c713).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L746)

<a id="op-309d9211c53f5c"></a>
### Stock Entry.get serial nos based on transferred batch

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_serial_nos_based_on_transferred_batch`

**Inputs** batch\_no, serial\_nos.

**Wrappers, in declaration order** staticmethod.

**Declared result** list.

**Record and data access** read “Serial No” via get\_all.

**Explicit results** list of d.name for d drawn from serial\_nos.

**Local steps**

- Set serial\_nos from Platform.get\_all(“Serial No”, filters = mapping(“batch\_no” → batch\_no, “name” → tuple(“in”, serial\_nos), “warehouse” → tuple(“is”, “not set”)), order\_by = “creation”).
- Return list of d.name for d drawn from serial\_nos.
  - Draw d from serial\_nos.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1217) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L714)

<a id="op-6f64d56fedd7d5"></a>
### Stock Entry.get pending raw materials

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_pending_raw_materials`

**Inputs** self, backflush\_based\_on = no value.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**State and service calls** msgprint with translated “All items have already been transferred for this Work Order.”.

**Explicit results** item\_dict.

**Local steps**

- Set item\_dict from self.get\_pro\_order\_required\_items(backflush\_based\_on).
- Set max\_qty from flt(self.pro\_doc.qty).
- Set allow\_overproduction from false.
- Set overproduction\_percentage from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”)).
- Set transfer\_extra\_materials\_percentage from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “transfer\_extra\_materials\_percentage”)).
- Set to\_transfer\_qty from (flt(self.pro\_doc.material\_transferred\_for\_manufacturing) + flt(self.fg\_completed\_qty)).
- Set transfer\_limit\_qty from (max\_qty + ((max\_qty × overproduction\_percentage) ÷ 100)).
- If transfer\_extra\_materials\_percentage.
  - Set transfer\_limit\_qty from (max\_qty + ((max\_qty × transfer\_extra\_materials\_percentage) ÷ 100)).
- If transfer\_limit\_qty ≥ to\_transfer\_qty.
  - Set allow\_overproduction from true.
- For each tuple(item, item\_details) in item\_dict.items().
  - Set pending\_to\_issue from (flt(item\_details.required\_qty) − flt(item\_details.transferred\_qty)).
  - Set desire\_to\_transfer from ((flt(self.fg\_completed\_qty) × flt(item\_details.required\_qty)) ÷ max\_qty).
  - If (desire\_to\_transfer ≤ pending\_to\_issue or (desire\_to\_transfer &gt; 0 and backflush\_based\_on equals “Material Transferred for Manufacture”) or allow\_overproduction).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in desire\_to\_transfer ≤ pending\_to\_issue → (desire\_to\_transfer &gt; 0 and backflush\_based\_on equals “Material Transferred for Manufacture”) → allow\_overproduction.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in desire\_to\_transfer &gt; 0 → backflush\_based\_on equals “Material Transferred for Manufacture”.
    - Set item\_dict at item at “qty” from desire\_to\_transfer when desire\_to\_transfer &gt; 0, otherwise pending\_to\_issue.
      - Value choice on desire\_to\_transfer &gt; 0 — true gives desire\_to\_transfer, false gives pending\_to\_issue.
  - Otherwise.
    - If pending\_to\_issue &gt; 0.
      - Set item\_dict at item at “qty” from pending\_to\_issue.
    - Otherwise.
      - Set item\_dict at item at “qty” from 0.
- Set list\_of\_items from list(item\_dict.keys()).
- For each item in list\_of\_items.
  - If not item\_dict at item at “qty”.
    - Remove item\_dict at item.
- If not len(item\_dict).
  - Evaluate Platform.msgprint(translated “All items have already been transferred for this Work Order.”).
- Return item\_dict.

**Methods declared on this owner** [get pro order required items](operations-083.md#op-227143c2f8aea2).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”), Platform.db.get\_single\_value(“Manufacturing Settings”, “transfer\_extra\_materials\_percentage”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1207) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L704)

<a id="op-227143c2f8aea2"></a>
### Stock Entry.get pro order required items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_pro_order_required_items`

**Inputs** self, backflush\_based\_on = no value.

**Record and data access** resolve a document from “Work Order” via get\_doc · read “Warehouse” via get\_value · read “Job Card” via get\_value.

**Explicit results** item\_dict.

**Local steps**

- Bind dependencies get\_allowed\_transfer\_qty.
- Set tuple(item\_dict, job\_card\_items) from tuple(Platform.\_dict(), list()).
- Set work\_order from Platform.get\_doc(“Work Order”, self.work\_order).
- Set consider\_job\_card from (work\_order.transfer\_material\_against equals “Job Card” and self.get(“job\_card”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in work\_order.transfer\_material\_against equals “Job Card” → self.get(“job\_card”).
- If consider\_job\_card.
  - Set job\_card\_items from self.get\_job\_card\_item\_codes(self.get(“job\_card”)).
- If not Platform.db.get\_value(“Warehouse”, work\_order.wip\_warehouse, “is\_group”).
  - Set wip\_warehouse from work\_order.wip\_warehouse.
- Otherwise.
  - Set wip\_warehouse from no value.
- Set job\_card\_operation from Platform.db.get\_value(“Job Card”, self.get(“job\_card”), list(“operation\_row\_id”, “operation”), as\_dict = true) when consider\_job\_card, otherwise no value.
  - Value choice on consider\_job\_card — true gives Platform.db.get\_value(“Job Card”, self.get(“job\_card”), list(“operation\_row\_id”, “operation”), as\_dict = true), false gives no value.
- For each d in work\_order.get(“required\_items”).
  - If (consider\_job\_card and d.item\_code does not belong to job\_card\_items).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in consider\_job\_card → d.item\_code does not belong to job\_card\_items.
    - Continue with the next iteration or loop test.
  - If (consider\_job\_card and not is\_row\_of\_job\_card\_operation(d, job\_card\_operation)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in consider\_job\_card → not is\_row\_of\_job\_card\_operation(d, job\_card\_operation).
    - Continue with the next iteration or loop test.
  - Set transfer\_pending from get\_allowed\_transfer\_qty(d.required\_qty) &gt; flt(d.transferred\_qty).
  - Set can\_transfer from (transfer\_pending or backflush\_based\_on equals “Material Transferred for Manufacture”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in transfer\_pending → backflush\_based\_on equals “Material Transferred for Manufacture”.
  - If (can\_transfer and d.include\_item\_in\_manufacturing).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in can\_transfer → d.include\_item\_in\_manufacturing.
    - Evaluate self.add\_required\_item\_row(item\_dict, d, work\_order, consider\_job\_card, …).
- Return item\_dict.

**Methods declared on this owner** [get job card item codes](operations-083.md#op-ca2864998364a8), [add required item row](operations-083.md#op-99fa73da1cac06).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L705)

<a id="op-99fa73da1cac06"></a>
### Stock Entry.add required item row

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_add_required_item_row`

**Inputs** self, item\_dict, d, work\_order, consider\_job\_card, wip\_warehouse.

**Record and data access** read “Job Card Item” via get\_value · read “Warehouse” via get\_value · read “Item” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- Set key from tuple(d.item\_code, d.source\_warehouse).
- If existing\_row bound to item\_dict.get(key).
  - Set existing\_row at “required\_qty” from (flt(existing\_row at “required\_qty”) + flt(d.required\_qty)).
  - Set existing\_row at “transferred\_qty” from (flt(existing\_row at “transferred\_qty”) + flt(d.transferred\_qty)).
  - Return no value.
- Set item\_row from d.as\_dict().
- Set item\_row at “idx” from (len(item\_dict) + 1).
- If consider\_job\_card.
  - Set job\_card\_item from Platform.db.get\_value(“Job Card Item”, mapping(“item\_code” → d.item\_code, “parent” → self.get(“job\_card”))).
  - Set item\_row at “job\_card\_item” from (job\_card\_item or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in job\_card\_item → no value.
- If (d.source\_warehouse and not Platform.db.get\_value(“Warehouse”, d.source\_warehouse, “is\_group”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.source\_warehouse → not Platform.db.get\_value(“Warehouse”, d.source\_warehouse, “is\_group”).
  - Set item\_row at “from\_warehouse” from d.source\_warehouse.
- Set item\_row at “to\_warehouse” from wip\_warehouse.
- Set item\_row at “allow\_alternative\_item” from cint((work\_order.allow\_alternative\_item and Platform.get\_cached\_value(“Item”, d.item\_code, “allow\_alternative\_item”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in work\_order.allow\_alternative\_item → Platform.get\_cached\_value(“Item”, d.item\_code, “allow\_alternative\_item”).
- Set item\_dict at key from item\_row.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, d.item\_code, “allow\_alternative\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1175) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L672)

<a id="op-ca2864998364a8"></a>
### Stock Entry.get job card item codes

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_job_card_item_codes`

**Inputs** self, job\_card = no value.

**Record and data access** read “Job Card Item” via get\_all.

**Explicit results** list() · list of d.item\_code for d drawn from job\_card\_items.

**Local steps**

- If not job\_card.
  - Return list().
- Set job\_card\_items from Platform.get\_all(“Job Card Item”, filters = mapping(“parent” → job\_card), fields = list(“item\_code”), distinct = true).
- Return list of d.item\_code for d drawn from job\_card\_items.
  - Draw d from job\_card\_items.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1204) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L701)

<a id="op-e7c2657477c713"></a>
### Stock Entry.add to stock entry detail

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_add_to_stock_entry_detail`

**Inputs** self, item\_dict, bom\_no = no value.

**Record and data access** read “Item” via get\_value.

**Local steps**

- Set precision from Platform.get\_precision(“Stock Entry Detail”, “qty”).
- For each d in item\_dict.
  - Set item\_row from item\_dict at d.
  - Set child\_qty from flt(item\_row at “qty”, precision).
  - If (not self.is\_return and child\_qty ≤ 0 and not item\_row.get(“secondary\_item\_type”) and not item\_row.get(“valuation\_type”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_return → child\_qty ≤ 0 → not item\_row.get(“secondary\_item\_type”) → not item\_row.get(“valuation\_type”).
    - <a id="op-e7c2657477c713-guard-13"></a>If self.purpose does not belong to list(“Receive from Customer”, “Send to Subcontractor”).
      - Continue with the next iteration or loop test.
  - Set se\_child from self.append(“items”).
  - Set stock\_uom from (item\_row.get(“stock\_uom”) or Platform.db.get\_value(“Item”, d, “stock\_uom”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“stock\_uom”) → Platform.db.get\_value(“Item”, d, “stock\_uom”).
  - Set se\_child.s\_warehouse from item\_row.get(“from\_warehouse”).
  - Set se\_child.t\_warehouse from item\_row.get(“to\_warehouse”).
  - Set se\_child.item\_code from (item\_row.get(“item\_code”) or cstr(d)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“item\_code”) → cstr(d).
  - Set se\_child.uom from item\_row at “uom” when item\_row.get(“uom”), otherwise stock\_uom.
    - Value choice on item\_row.get(“uom”) — true gives item\_row at “uom”, false gives stock\_uom.
  - Set se\_child.stock\_uom from stock\_uom.
  - Set se\_child.qty from child\_qty when child\_qty &gt; 0, otherwise 0.
    - Value choice on child\_qty &gt; 0 — true gives child\_qty, false gives 0.
  - Set se\_child.allow\_alternative\_item from item\_row.get(“allow\_alternative\_item”, 0).
  - Set se\_child.subcontracted\_item from item\_row.get(“main\_item\_code”).
  - Set se\_child.cost\_center from (item\_row.get(“cost\_center”) or get\_default\_cost\_center(item\_row, company = self.company)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“cost\_center”) → get\_default\_cost\_center(item\_row, company = self.company).
  - Set se\_child.is\_finished\_item from item\_row.get(“is\_finished\_item”, 0).
  - Set se\_child.po\_detail from item\_row.get(“po\_detail”).
  - Set se\_child.sco\_rm\_detail from item\_row.get(“sco\_rm\_detail”).
  - Set se\_child.scio\_detail from item\_row.get(“scio\_detail”).
  - Set se\_child.sample\_quantity from item\_row.get(“sample\_quantity”, 0).
  - Set se\_child.secondary\_item\_type from item\_row.get(“secondary\_item\_type”).
  - Set se\_child.valuation\_type from item\_row.get(“valuation\_type”).
  - If item\_row.get(“valuation\_type”) equals “Manual”.
    - Set se\_child.set\_basic\_rate\_manually from 1.
    - Set se\_child.basic\_rate from flt(item\_row.get(“manual\_rate”)).
  - Set se\_child.bom\_secondary\_item from (item\_row.get(“name”) or item\_row.get(“bom\_secondary\_item”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“name”) → item\_row.get(“bom\_secondary\_item”).
  - For each field in list(self.subcontract\_data.rm\_detail\_field, “original\_item”, “expense\_account”, “description”, …).
    - If item\_row.get(field).
      - Evaluate se\_child.set(field, item\_row.get(field)).
  - If se\_child.s\_warehouse is identical to no value.
    - Set se\_child.s\_warehouse from self.from\_warehouse.
  - If se\_child.t\_warehouse is identical to no value.
    - Set se\_child.t\_warehouse from self.to\_warehouse.
  - Set se\_child.conversion\_factor from (flt(item\_row.get(“conversion\_factor”)) or 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item\_row.get(“conversion\_factor”)) → 1.
  - Set se\_child.transfer\_qty from flt((item\_row at “qty” × se\_child.conversion\_factor), se\_child.precision(“qty”)).
  - Set se\_child.bom\_no from bom\_no.
  - Set se\_child.job\_card\_item from item\_row.get(“job\_card\_item”) when self.get(“job\_card”), otherwise no value.
    - Value choice on self.get(“job\_card”) — true gives item\_row.get(“job\_card\_item”), false gives no value.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.purpose does not belong to list(“Receive from Customer”, “Send to Subcontractor”), self.purpose = “Material Issue” selects the branch that continues with the next loop iteration. With self.purpose = “Send to Subcontractor”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e7c2657477c713-guard-13)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1176) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L673)

<a id="op-86be136156d55e"></a>
### Stock Entry.validate with material request

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_with_material_request`

**Inputs** self.

**Record and data access** read “Stock Entry Detail” via get\_value · read “Material Request Item” via get\_value.

**Explicit failure paths** validation helper with Platform.MappingMismatchError — translated “Item for row {0} does not match Material Request”.format(item.idx).

**Local steps**

- For each item in self.get(“items”).
  - Set material\_request from (item.material\_request or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.material\_request → no value.
  - Set material\_request\_item from (item.material\_request\_item or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.material\_request\_item → no value.
  - If (self.purpose equals “Material Transfer” and self.outgoing\_stock\_entry).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Material Transfer” → self.outgoing\_stock\_entry.
    - Set parent\_se from Platform.get\_value(“Stock Entry Detail”, item.ste\_detail, list(“material\_request”, “material\_request\_item”), as\_dict = true).
    - If parent\_se.
      - Set material\_request from parent\_se.material\_request.
      - Set material\_request\_item from parent\_se.material\_request\_item.
  - If material\_request.
    - Set mreq\_item from Platform.db.get\_value(“Material Request Item”, mapping(“name” → material\_request\_item, “parent” → material\_request), list(“item\_code”, “warehouse”, “idx”), as\_dict = true).
    - If mreq\_item.item\_code differs from item.item\_code.
      - Call the validation error handler Platform.throw(translated “Item for row {0} does not match Material Request”.format(item.idx), Platform.MappingMismatchError).
    - Otherwise.
      - If (self.purpose equals “Material Transfer” and self.add\_to\_transit).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Material Transfer” → self.add\_to\_transit.
        - Continue with the next iteration or loop test.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1282) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L779)

<a id="op-7defab565a8265"></a>
### Stock Entry.validate against pick list

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_against_pick_list`

**Inputs** self.

**Record and data access** read “Pick List Item” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} was picked from {2}, not {3}.”.format(d.idx, Platform.bold(d.item\_code), Platform.bold(picked\_row.warehouse), Platform.bold(d.s\_warehouse)) · validation helper — translated “Row #{0}: Item {1} is transferred more than the {2} picked in {3}.”.format(d.idx, Platform.bold(d.item\_code), flt(picked\_row.picked\_qty), self.pick\_list).

**Local steps**

- Set pick\_list\_items from set of d.pick\_list\_item for d drawn from self.items where d.pick\_list\_item.
  - Draw d from self.items, keep a combination only if (d.pick\_list\_item).
- If (not pick\_list\_items or self.is\_return).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not pick\_list\_items → self.is\_return.
  - Return no value.
- Set picked\_rows from mapping of row.name → row for row drawn from Platform.get\_all(“Pick List Item”, filters = mapping(“name” → tuple(“in”, list(pick\_list\_items))), fields = list(“name”, “warehouse”, “picked\_qty”, “transferred\_qty”)).
  - Draw row from Platform.get\_all(“Pick List Item”, filters = mapping(“name” → tuple(“in”, list(pick\_list\_items))), fields = list(“name”, “warehouse”, “picked\_qty”, “transferred\_qty”)).
- Set transfer\_qty from defaultdict(float).
- For each d in self.items.
  - Set picked\_row from picked\_rows.get(d.pick\_list\_item).
  - If not picked\_row.
    - Continue with the next iteration or loop test.
  - If (d.s\_warehouse and d.s\_warehouse differs from picked\_row.warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.s\_warehouse → d.s\_warehouse differs from picked\_row.warehouse.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} was picked from {2}, not {3}.”.format(d.idx, Platform.bold(d.item\_code), Platform.bold(picked\_row.warehouse), Platform.bold(d.s\_warehouse))).
  - Update transfer\_qty at d.pick\_list\_item using + (flt(d.qty) × flt((d.conversion\_factor or 1))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.conversion\_factor → 1.
  - If (flt(picked\_row.transferred\_qty) + transfer\_qty at d.pick\_list\_item) &gt; flt(picked\_row.picked\_qty).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} is transferred more than the {2} picked in {3}.”.format(d.idx, Platform.bold(d.item\_code), flt(picked\_row.picked\_qty), self.pick\_list)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1254) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L751)

<a id="op-31a7b67af0ba2a"></a>
### Stock Entry.validate batch

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_batch`

**Inputs** self.

**Record and data access** read “Batch” via get\_value.

**Explicit failure paths** validation helper — translated “Batch {0} of Item {1} has expired.”.format(item.batch\_no, item.item\_code) · validation helper — translated “Batch {0} of Item {1} is disabled.”.format(item.batch\_no, item.item\_code).

**Local steps**

- If self.purpose belongs to list(“Material Transfer for Manufacture”, “Manufacture”, “Repack”, “Send to Subcontractor”).
  - For each item in self.get(“items”).
    - If item.batch\_no.
      - Set disabled from Platform.db.get\_value(“Batch”, item.batch\_no, “disabled”).
      - If disabled equals 0.
        - Set expiry\_date from Platform.db.get\_value(“Batch”, item.batch\_no, “expiry\_date”).
        - If expiry\_date.
          - If getdate(self.posting\_date) &gt; getdate(expiry\_date).
            - Call the validation error handler Platform.throw(translated “Batch {0} of Item {1} has expired.”.format(item.batch\_no, item.item\_code)).
      - Otherwise.
        - Call the validation error handler Platform.throw(translated “Batch {0} of Item {1} is disabled.”.format(item.batch\_no, item.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1240) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L827)

<a id="op-8054193fc34b37"></a>
### Stock Entry.update subcontract order supplied items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_update_subcontract_order_supplied_items`

**Inputs** self.

**Record and data access** read self.subcontract\_data.order\_supplied\_items\_field via get\_all.

**State and service calls** request set\_value on self.subcontract\_data.order\_supplied\_items\_field.

**Local steps**

- If (self.get(self.subcontract\_data.order\_field) and (self.purpose belongs to list(“Send to Subcontractor”, “Material Transfer”) or self.is\_return)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(self.subcontract\_data.order\_field) → (self.purpose belongs to list(“Send to Subcontractor”, “Material Transfer”) or self.is\_return).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purpose belongs to list(“Send to Subcontractor”, “Material Transfer”) → self.is\_return.
  - Set order\_supplied\_items from Platform.db.get\_all(self.subcontract\_data.order\_supplied\_items\_field, filters = mapping(“parent” → self.get(self.subcontract\_data.order\_field)), fields = list(“name”, “rm\_item\_code”, “reserve\_warehouse”)).
  - Set supplied\_items from get\_supplied\_items(self.get(self.subcontract\_data.order\_field), self.subcontract\_data.rm\_detail\_field, self.subcontract\_data.order\_field).
  - For each row in order\_supplied\_items.
    - Set tuple(key, item) from tuple(row.name, mapping()).
    - If not supplied\_items.get(key).
      - Set item from mapping(“supplied\_qty” → 0, “returned\_qty” → 0, “total\_supplied\_qty” → 0).
    - Otherwise.
      - Set item from supplied\_items.get(key).
    - Evaluate Platform.db.set\_value(self.subcontract\_data.order\_supplied\_items\_field, row.name, item).
  - Set item\_wh from mapping of x.get(“rm\_item\_code”) → x.get(“reserve\_warehouse”) for x drawn from order\_supplied\_items.
    - Draw x from order\_supplied\_items.
  - For each d in self.get(“items”).
    - Set item\_code from (d.get(“original\_item”) or d.get(“item\_code”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.get(“original\_item”) → d.get(“item\_code”).
    - Set reserve\_warehouse from item\_wh.get(item\_code).
    - If not (reserve\_warehouse and item\_code).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in reserve\_warehouse → item\_code.
      - Continue with the next iteration or loop test.
    - Set stock\_bin from get\_bin(item\_code, reserve\_warehouse).
    - Evaluate stock\_bin.update\_reserved\_qty\_for\_sub\_contracting().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L747)

<a id="op-f2cf1b56d58d64"></a>
### Stock Entry.get stock in transferred qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_stock_in_transferred_qty`

**Inputs** self.

**Explicit results** tuple(mapping(), list()) · tuple(stock\_entries, ste\_details).

**Explicit failure paths** validation helper — translated “Row {0}: Transferred quantity cannot be greater than the requested quantity.”.format(d.idx).

**Local steps**

- Set rows from list of d for d drawn from self.items where (d.against\_stock\_entry and d.ste\_detail).
  - Draw d from self.items, keep a combination only if ((d.against\_stock\_entry and d.ste\_detail)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.against\_stock\_entry → d.ste\_detail.
- If not rows.
  - Return tuple(mapping(), list()).
- Set ste\_details from list of d.ste\_detail for d drawn from rows.
  - Draw d from rows.
- Set outward\_rows from get\_outward\_rows(ste\_details).
- Set transferred\_qty\_map from get\_transferred\_qty\_map(ste\_details).
- Set stock\_entries from mapping().
- For each d in rows.
  - Set transferred\_qty from flt(transferred\_qty\_map.get(d.ste\_detail)).
  - Set outward\_row from outward\_rows.get(d.ste\_detail, Platform.\_dict()).
  - If (d.docstatus equals 1 and transferred\_qty &gt; flt(outward\_row.transfer\_qty)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.docstatus equals 1 → transferred\_qty &gt; flt(outward\_row.transfer\_qty).
    - Call the validation error handler Platform.throw(translated “Row {0}: Transferred quantity cannot be greater than the requested quantity.”.format(d.idx)).
  - Set stock\_entries at tuple(d.against\_stock\_entry, d.ste\_detail) from transferred\_qty.
- Return tuple(stock\_entries, ste\_details).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1219) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L716)
