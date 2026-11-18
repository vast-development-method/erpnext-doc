# Inventory and warehouses · operations 78

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock entry

[Record definition](../../../../data/record-types/stock_entry.json)

<a id="op-b9682769e17d70"></a>
### Stock Entry.validate warehouse

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_warehouse`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Source warehouse is mandatory for row {0}”.format(d.idx) · validation helper — translated “Target warehouse is mandatory for row {0}”.format(d.idx) · validation helper — translated “Source and target warehouse cannot be same for row {0}”.format(d.idx) · validation helper — translated “At least one warehouse is mandatory”.

**Local steps**

- Set source\_mandatory from list(“Material Issue”, “Material Transfer”, “Send to Subcontractor”, “Material Transfer for Manufacture”, …).
- Set target\_mandatory from list(“Material Receipt”, “Material Transfer”, “Send to Subcontractor”, “Material Transfer for Manufacture”, …).
- Set has\_bom from any(list of d.bom\_no for d drawn from self.get(“items”)).
  - Draw d from self.get(“items”).
- If (self.purpose belongs to source\_mandatory and self.purpose does not belong to target\_mandatory).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose belongs to source\_mandatory → self.purpose does not belong to target\_mandatory.
  - Set self.to\_warehouse from no value.
  - For each d in self.get(“items”).
    - Set d.t\_warehouse from no value.
- Otherwise.
  - If (self.purpose belongs to target\_mandatory and self.purpose does not belong to source\_mandatory).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose belongs to target\_mandatory → self.purpose does not belong to source\_mandatory.
    - Set self.from\_warehouse from no value.
    - For each d in self.get(“items”).
      - Set d.s\_warehouse from no value.
- For each d in self.get(“items”).
  - If (not d.s\_warehouse and not d.t\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.s\_warehouse → not d.t\_warehouse.
    - Set d.s\_warehouse from self.from\_warehouse.
    - Set d.t\_warehouse from self.to\_warehouse.
  - If (self.purpose belongs to source\_mandatory and not d.s\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose belongs to source\_mandatory → not d.s\_warehouse.
    - If self.from\_warehouse.
      - Set d.s\_warehouse from self.from\_warehouse.
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Source warehouse is mandatory for row {0}”.format(d.idx)).
  - If (self.purpose belongs to target\_mandatory and not d.t\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose belongs to target\_mandatory → not d.t\_warehouse.
    - If self.to\_warehouse.
      - Set d.t\_warehouse from self.to\_warehouse.
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Target warehouse is mandatory for row {0}”.format(d.idx)).
  - If self.purpose belongs to list(“Manufacture”, “Repack”).
    - If (d.is\_finished\_item or d.secondary\_item\_type or d.valuation\_type).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.is\_finished\_item → d.secondary\_item\_type → d.valuation\_type.
      - Set d.s\_warehouse from no value.
      - If not d.t\_warehouse.
        - Call the validation error handler Platform.throw(translated “Target warehouse is mandatory for row {0}”.format(d.idx)).
    - Otherwise.
      - Set d.t\_warehouse from no value.
      - If not d.s\_warehouse.
        - Call the validation error handler Platform.throw(translated “Source warehouse is mandatory for row {0}”.format(d.idx)).
  - If self.purpose equals “Disassemble”.
    - If has\_bom.
      - If (d.is\_finished\_item or d.secondary\_item\_type or d.valuation\_type).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.is\_finished\_item → d.secondary\_item\_type → d.valuation\_type.
        - Set d.t\_warehouse from no value.
        - If not d.s\_warehouse.
          - Call the validation error handler Platform.throw(translated “Source warehouse is mandatory for row {0}”.format(d.idx)).
      - Otherwise.
        - Set d.s\_warehouse from no value.
        - If not d.t\_warehouse.
          - Call the validation error handler Platform.throw(translated “Target warehouse is mandatory for row {0}”.format(d.idx)).
  - If (cstr(d.s\_warehouse) equals cstr(d.t\_warehouse) and self.purpose does not belong to list(“Material Transfer for Manufacture”, “Material Transfer”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cstr(d.s\_warehouse) equals cstr(d.t\_warehouse) → self.purpose does not belong to list(“Material Transfer for Manufacture”, “Material Transfer”).
    - Call the validation error handler Platform.throw(translated “Source and target warehouse cannot be same for row {0}”.format(d.idx)).
  - If not (d.s\_warehouse or d.t\_warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.s\_warehouse → d.t\_warehouse.
    - Call the validation error handler Platform.throw(translated “At least one warehouse is mandatory”).
- Evaluate self.validate\_transit\_warehouses().
- Evaluate self.validate\_stock\_in\_rows().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate transit warehouses](operations-078.md#op-5ab3c6d3f1fec8), [validate stock in rows](operations-078.md#op-03d762dbb06418).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1280) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L777)

<a id="op-03d762dbb06418"></a>
### Stock Entry.validate stock in rows

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_stock_in_rows`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} does not match item {2} sent by {3}.”.format(item.idx, Platform.bold(item.item\_code), Platform.bold(outward\_row.item\_code), item.against\_stock\_entry) · validation helper — translated “Row #{0}: Item {1} must be taken from {2}, where {3} sent it.”.format(item.idx, Platform.bold(item.item\_code), Platform.bold(outward\_row.t\_warehouse), item.against\_stock\_entry).

**Local steps**

- Set rows from list of item for item drawn from self.items where (item.against\_stock\_entry and item.ste\_detail).
  - Draw item from self.items, keep a combination only if ((item.against\_stock\_entry and item.ste\_detail)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.against\_stock\_entry → item.ste\_detail.
- If not rows.
  - Return no value.
- Set outward\_rows from get\_outward\_rows(list of item.ste\_detail for item drawn from rows).
  - Draw item from rows.
- For each item in rows.
  - Set outward\_row from outward\_rows.get(item.ste\_detail).
  - If not outward\_row.
    - Continue with the next iteration or loop test.
  - If item.item\_code differs from outward\_row.item\_code.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} does not match item {2} sent by {3}.”.format(item.idx, Platform.bold(item.item\_code), Platform.bold(outward\_row.item\_code), item.against\_stock\_entry)).
  - If item.s\_warehouse differs from outward\_row.t\_warehouse.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} must be taken from {2}, where {3} sent it.”.format(item.idx, Platform.bold(item.item\_code), Platform.bold(outward\_row.t\_warehouse), item.against\_stock\_entry)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1277) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L774)

<a id="op-5ab3c6d3f1fec8"></a>
### Stock Entry.validate transit warehouses

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_transit_warehouses`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Default Target Warehouse {0} must be a Transit warehouse when Add to Transit is enabled.”.format(Platform.bold(self.to\_warehouse)) · validation helper — translated “Row #{0}: Target Warehouse {1} must be a Transit warehouse when Add to Transit is enabled.”.format(row.idx, Platform.bold(row.t\_warehouse)).

**Local steps**

- If not self.add\_to\_transit.
  - Return no value.
- Set target\_warehouses from set of row.t\_warehouse for row drawn from self.items where row.t\_warehouse.
  - Draw row from self.items, keep a combination only if (row.t\_warehouse).
- If self.to\_warehouse.
  - Evaluate target\_warehouses.add(self.to\_warehouse).
- If not target\_warehouses.
  - Return no value.
- Set transit\_warehouses from set(Platform.get\_all(“Warehouse”, filters = mapping(“name” → tuple(“in”, list(target\_warehouses)), “warehouse\_type” → “Transit”, “company” → self.company), pluck = “name”)).
- If (self.to\_warehouse and self.to\_warehouse does not belong to transit\_warehouses).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.to\_warehouse → self.to\_warehouse does not belong to transit\_warehouses.
  - Call the validation error handler Platform.throw(translated “Default Target Warehouse {0} must be a Transit warehouse when Add to Transit is enabled.”.format(Platform.bold(self.to\_warehouse))).
- For each row in self.items.
  - If (row.t\_warehouse and row.t\_warehouse does not belong to transit\_warehouses).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.t\_warehouse → row.t\_warehouse does not belong to transit\_warehouses.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Target Warehouse {1} must be a Transit warehouse when Add to Transit is enabled.”.format(row.idx, Platform.bold(row.t\_warehouse))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1279) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L776)

<a id="op-5feb3ad798888d"></a>
### Stock Entry.validate work order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_work_order`

**Inputs** self.

**Record and data access** read “Work Order” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “For Quantity (Manufactured Qty) is mandatory”.

**Local steps**

- If self.purpose belongs to tuple(“Manufacture”, “Material Transfer for Manufacture”, “Material Consumption for Manufacture”, “Disassemble”).
  - If ((self.purpose equals “Manufacture” or self.purpose equals “Material Consumption for Manufacture”) and self.work\_order and Platform.get\_cached\_value(“Work Order”, self.work\_order, “track\_semi\_finished\_good ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.purpose equals “Manufacture” or self.purpose equals “Material Consumption for Manufacture”) → self.work\_order → Platform.get\_cached\_value(“Work Order”, self.work\_order, “track\_semi\_finished\_goods”) differs from 1.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purpose equals “Manufacture” → self.purpose equals “Material Consumption for Manufacture”.
    - If not self.fg\_completed\_qty.
      - Call the validation error handler Platform.throw(translated “For Quantity (Manufactured Qty) is mandatory”).
    - Evaluate self.check\_if\_operations\_completed().
    - Evaluate self.check\_duplicate\_entry\_for\_work\_order().
- Otherwise.
  - <a id="op-5feb3ad798888d-guard-19"></a>If self.purpose differs from “Material Transfer”.
    - Set self.work\_order from no value.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.purpose differs from “Material Transfer”, self.purpose = “Material Issue” selects the branch that assigns no value to self.work\_order. With self.purpose = “Material Transfer”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-5feb3ad798888d-guard-19)

**Methods declared on this owner** [check if operations completed](operations-078.md#op-73e4788c7a2d05), [check duplicate entry for work order](operations-079.md#op-d7ae0226a4c4aa).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Work Order”, self.work\_order, “track\_semi\_finished\_goods”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1283) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L780)

<a id="op-d13281b1716f58"></a>
### Stock Entry.validate work order status for return

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_work_order_status_for_return`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Components can be returned only after Work Order {0} is Completed or Closed”.format(get\_link\_to\_form(“Work Order”, self.work\_order)).

**Local steps**

- If (not (self.is\_return and self.pro\_doc) or self.pro\_doc.status belongs to tuple(“Completed”, “Closed”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not (self.is\_return and self.pro\_doc) → self.pro\_doc.status belongs to tuple(“Completed”, “Closed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.pro\_doc.
  - Return no value.
- Call the validation error handler Platform.throw(translated “Components can be returned only after Work Order {0} is Completed or Closed”.format(get\_link\_to\_form(“Work Order”, self.work\_order)), title = translated “Work Order Not Finished”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1284) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L781)

<a id="op-b120ff66262fb1"></a>
### Stock Entry.validate job card for semi finished goods

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_job_card_for_semi_finished_goods`

**Inputs** self.

**Record and data access** read “Job Card” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Transfer materials for Work Order {0} from its Job Cards.”.format(get\_link\_to\_form(“Work Order”, self.work\_order)) · validation helper — translated “Send materials for Job Card {0} to the supplier from its Subcontracting Order.”.format(get\_link\_to\_form(“Job Card”, self.job\_card)).

**Local steps**

- If (self.purpose differs from “Material Transfer for Manufacture” or self.is\_return or not self.pro\_doc.get(“track\_semi\_finished\_goods”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purpose differs from “Material Transfer for Manufacture” → self.is\_return → not self.pro\_doc.get(“track\_semi\_finished\_goods”).
  - Return no value.
- If not self.job\_card.
  - Call the validation error handler Platform.throw(translated “Transfer materials for Work Order {0} from its Job Cards.”.format(get\_link\_to\_form(“Work Order”, self.work\_order)), title = translated “Job Card Required”).
- If Platform.db.get\_value(“Job Card”, self.job\_card, “is\_subcontracted”).
  - Call the validation error handler Platform.throw(translated “Send materials for Job Card {0} to the supplier from its Subcontracting Order.”.format(get\_link\_to\_form(“Job Card”, self.job\_card)), title = translated “Subcontracted Job Card”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1263) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L760)

<a id="op-bd92821f5c6bf8"></a>
### Stock Entry.validate returned qty within work order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_returned_qty_within_work_order`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Item {0}: cannot return {1} to the store, Work Order {2} has only {3} of it left unconsumed.”.format(Platform.bold(item\_code), flt(returned\_qty), get\_link\_to\_form(“Work Order”, self.work\_order) ….

**Local steps**

- If not (self.is\_return and self.pro\_doc and self.purpose equals “Material Transfer for Manufacture”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.pro\_doc → self.purpose equals “Material Transfer for Manufacture”.
  - Return no value.
- Set returnable\_qty from self.get\_returnable\_qty().
- For each tuple(item\_code, returned\_qty) in self.get\_returned\_qty\_by\_item().items().
  - If flt(returned\_qty, 6) &gt; flt(returnable\_qty at item\_code, 6).
    - Call the validation error handler Platform.throw(translated “Item {0}: cannot return {1} to the store, Work Order {2} has only {3} of it left unconsumed.”.format(Platform.bold(item\_code), flt(returned\_qty), get\_link\_to\_form(“Work Order”, s ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get returnable qty](operations-078.md#op-0beb2a92b161b0), [get returned qty by item](operations-078.md#op-3e05cb71663a22).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1274) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L771)

<a id="op-0beb2a92b161b0"></a>
### Stock Entry.get returnable qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_returnable_qty`

**Inputs** self.

**Declared result** dict.

**Explicit results** defaultdict(float, mapping of item\_code → flt(qty) for tuple(item\_code, qty) drawn from rows).

**Local steps**

- Bind dependencies Case.
- Set stock\_entry from Platform.qb.DocType(“Stock Entry”).
- Set detail from Platform.qb.DocType(“Stock Entry Detail”).
- Set transferred from (stock\_entry.purpose equals “Material Transfer for Manufacture” bitwise and stock\_entry.is\_return equals 0).
- Set consumed from (detail.s\_warehouse.isnotnull() bitwise and (stock\_entry.purpose.isin(list(“Manufacture”, “Material Consumption for Manufacture”)) bitwise or (stock\_entry.purpose equals “Material Transfer for Manufacture” ….
- Set rows from nested operand in the contract(nested operand in the contract).where((transferred bitwise or consumed)).groupby(detail.item\_code).run().
- Return defaultdict(float, mapping of item\_code → flt(qty) for tuple(item\_code, qty) drawn from rows).
  - Draw tuple(item\_code, qty) from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L709)

<a id="op-3e05cb71663a22"></a>
### Stock Entry.get returned qty by item

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_returned_qty_by_item`

**Inputs** self.

**Declared result** dict.

**Explicit results** qty\_by\_item.

**Local steps**

- Set qty\_by\_item from defaultdict(float).
- For each row in self.items.
  - If row.s\_warehouse.
    - Update qty\_by\_item at row.item\_code using + (flt(row.qty) × flt((row.conversion\_factor or 1))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.conversion\_factor → 1.
- Return qty\_by\_item.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L710)

<a id="op-a3ca4e418d3a86"></a>
### Stock Entry.validate alternative items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_alternative_items`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Work Order {1} does not allow alternative items”.format(rows at 0.idx, Platform.bold(self.work\_order)).

**Local steps**

- If (not self.pro\_doc or self.purpose does not belong to tuple(“Manufacture”, “Material Transfer for Manufacture”, “Material Consumption for Manufacture”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.pro\_doc → self.purpose does not belong to tuple(“Manufacture”, “Material Transfer for Manufacture”, “Material Consumption for Manufacture”).
  - Return no value.
- Set rows from list of row for row drawn from self.items where (row.original\_item and row.original\_item differs from row.item\_code).
  - Draw row from self.items, keep a combination only if ((row.original\_item and row.original\_item differs from row.item\_code)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.original\_item → row.original\_item differs from row.item\_code.
- If not rows.
  - Return no value.
- Set transferred\_pairs from self.get\_transferred\_alternative\_pairs().
- Set rows from list of row for row drawn from rows where tuple(row.original\_item, row.item\_code) does not belong to transferred\_pairs.
  - Draw row from rows, keep a combination only if (tuple(row.original\_item, row.item\_code) does not belong to transferred\_pairs).
- If not rows.
  - Return no value.
- If not self.pro\_doc.allow\_alternative\_item.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Work Order {1} does not allow alternative items”.format(rows at 0.idx, Platform.bold(self.work\_order))).
- Evaluate self.validate\_alternative\_item\_rows(rows).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get transferred alternative pairs](operations-078.md#op-9d0c961e452f72), [validate alternative item rows](operations-078.md#op-c9e92657e61a14).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1256) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L753)

<a id="op-c9e92657e61a14"></a>
### Stock Entry.validate alternative item rows

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_alternative_item_rows`

**Inputs** self, rows.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} is not an alternative of Item {2}”.format(row.idx, Platform.bold(row.item\_code), Platform.bold(row.original\_item)).

**Local steps**

- Bind dependencies get\_alternative\_item\_pairs.
- Set alternative\_pairs from get\_alternative\_item\_pairs(list(set of row.original\_item for row drawn from rows)).
  - Draw row from rows.
- For each row in rows.
  - If tuple(row.original\_item, row.item\_code) does not belong to alternative\_pairs.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} is not an alternative of Item {2}”.format(row.idx, Platform.bold(row.item\_code), Platform.bold(row.original\_item))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1255) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L752)

<a id="op-9d0c961e452f72"></a>
### Stock Entry.get transferred alternative pairs

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_transferred_alternative_pairs`

**Inputs** self.

**Explicit results** set() · set of tuple(pair) for pair drawn from pairs.

**Local steps**

- If (self.purpose equals “Material Transfer for Manufacture” and not self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Material Transfer for Manufacture” → not self.is\_return.
  - Return set().
- Set stock\_entry from Platform.qb.DocType(“Stock Entry”).
- Set stock\_entry\_detail from Platform.qb.DocType(“Stock Entry Detail”).
- Set pairs from nested operand in the contract(nested operand in the contract, nested operand in the contract).distinct().where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and ne ….run().
- Return set of tuple(pair) for pair drawn from pairs.
  - Draw pair from pairs.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1220) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L717)

<a id="op-e33c3e985dff60"></a>
### Stock Entry.validate source stock entry

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_source_stock_entry`

**Inputs** self.

**Record and data access** read “Stock Entry” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Source Stock Entry {0} belongs to Work Order {1}, not {2}. Please use a manufacture entry from the same Work Order.”.format(self.source\_stock\_entry, source\_wo, self.work\_order) · validation helper — translated “Cannot disassemble {0} qty against Stock Entry {1}. Only {2} qty available to disassemble.”.format(self.fg\_completed\_qty, self.source\_stock\_entry, available\_qty).

**Local steps**

- If not self.get(“source\_stock\_entry”).
  - Return no value.
- If self.work\_order.
  - Set source\_wo from Platform.db.get\_value(“Stock Entry”, self.source\_stock\_entry, “work\_order”).
  - If (source\_wo and source\_wo differs from self.work\_order).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in source\_wo → source\_wo differs from self.work\_order.
    - Call the validation error handler Platform.throw(translated “Source Stock Entry {0} belongs to Work Order {1}, not {2}. Please use a manufacture entry from the same Work Order.”.format(self.source\_stock\_entry, source\_wo, self.work\_order),  ….
- Bind dependencies get\_disassembly\_available\_qty.
- Set available\_qty from get\_disassembly\_available\_qty(self.source\_stock\_entry, self.name).
- If flt(self.fg\_completed\_qty) &gt; available\_qty.
  - Call the validation error handler Platform.throw(translated “Cannot disassemble {0} qty against Stock Entry {1}. Only {2} qty available to disassemble.”.format(self.fg\_completed\_qty, self.source\_stock\_entry, available\_qty), title = transla ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1254) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L838)

<a id="op-1e8e13da564b31"></a>
### Stock Entry.validate disassembly quantities

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_disassembly_quantities`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_finished\_good\_consumption().
- Evaluate self.validate\_materials\_against\_source().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate finished good consumption](operations-078.md#op-26097b00fe584f), [validate materials against source](operations-078.md#op-7e3012d36f4684).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1259) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L756)

<a id="op-26097b00fe584f"></a>
### Stock Entry.validate finished good consumption

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_finished_good_consumption`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Finished good quantity being consumed ({0} in stock UOM) must equal the quantity to disassemble ({1}). Do no …”.format(flt(fg\_stock\_qty, precision), flt(fg\_completed\_qty, precision)).

**Local steps**

- Set precision from Platform.get\_precision(“Stock Entry Detail”, “transfer\_qty”).
- Set tolerance from \_qty\_tolerance(precision).
- Set fg\_stock\_qty from sum(generator of flt(row.transfer\_qty) for row drawn from self.items where row.is\_finished\_item).
  - Draw row from self.items, keep a combination only if (row.is\_finished\_item).
- Set fg\_completed\_qty from flt(self.fg\_completed\_qty).
- If abs((flt(fg\_stock\_qty, precision) − flt(fg\_completed\_qty, precision))) &gt; tolerance.
  - Call the validation error handler Platform.throw(translated “Finished good quantity being consumed ({0} in stock UOM) must equal the quantity to disassemble ({1}). Do no …”.format(flt(fg\_stock\_qty, precision), flt(fg\_completed\_qty, precisi ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1260) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L757)

<a id="op-7e3012d36f4684"></a>
### Stock Entry.validate materials against source

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_materials_against_source`

**Inputs** self.

**Explicit results** self.validate\_materials\_against\_bom().

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} is not part of the source manufacture entry and cannot be added to this disassembly.”.format(row.idx, Platform.bold(row.item\_code)) · validation helper — translated “Row #{0}: Item {1} quantity ({2} in stock UOM) does not match the quantity derived from the source ({3}). Do …”.format(row.idx, Platform.bold(row.item\_code), flt(row.transfer\_qty, precision), f ….

**Local steps**

- Set source\_fg\_qty from self.get\_source\_fg\_qty().
- If not source\_fg\_qty.
  - Return self.validate\_materials\_against\_bom().
- Set progress from self.get\_disassembly\_progress(source\_fg\_qty).
- Set expected\_rows from list of tuple(source\_row, self.get\_component\_stock\_qty(source\_row, progress)) for source\_row drawn from self.get\_items\_from\_manufacture\_stock\_entry().
  - Draw source\_row from self.get\_items\_from\_manufacture\_stock\_entry().
- Set tuple(expected\_by\_name, expected\_by\_item) from tuple(mapping(), defaultdict(float)).
- For each tuple(source\_row, qty) in expected\_rows.
  - If source\_row.get(“name”).
    - Set expected\_by\_name at source\_row.name from tuple(qty, flt(source\_row.conversion\_factor)).
  - Update expected\_by\_item at source\_row.item\_code using + qty.
- Set precision from Platform.get\_precision(“Stock Entry Detail”, “transfer\_qty”).
- Set tolerance from \_qty\_tolerance(precision).
- Set qty\_precision from Platform.get\_precision(“Stock Entry Detail”, “qty”).
- Evaluate self.validate\_no\_missing\_components(expected\_rows, precision, tolerance).
- For each row in self.items.
  - If row.is\_finished\_item.
    - Continue with the next iteration or loop test.
  - If (row.ste\_detail and row.ste\_detail belongs to expected\_by\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.ste\_detail → row.ste\_detail belongs to expected\_by\_name.
    - Set tuple(expected, conversion\_factor) from expected\_by\_name at row.ste\_detail.
  - Otherwise.
    - If row.item\_code belongs to expected\_by\_item.
      - Set tuple(expected, conversion\_factor) from tuple(expected\_by\_item at row.item\_code, 1).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} is not part of the source manufacture entry and cannot be added to this disassembly.”.format(row.idx, Platform.bold(row.item\_code)), title = translated “Invali ….
  - Set expected from (flt((expected ÷ conversion\_factor), qty\_precision) × conversion\_factor).
  - If abs((flt(row.transfer\_qty, precision) − flt(expected, precision))) &gt; tolerance.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} quantity ({2} in stock UOM) does not match the quantity derived from the source ({3}). Do …”.format(row.idx, Platform.bold(row.item\_code), flt(row.transfer\_qty ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get source fg qty](operations-078.md#op-d969a5020c4c38), [validate materials against bom](operations-078.md#op-a0d627af507534), [get disassembly progress](operations-078.md#op-883a013a5f800b), [get component stock qty](operations-078.md#op-9eca59f956ffcd), [get items from manufacture stock entry](operations-082.md#op-28a561352164af), [validate no missing components](operations-078.md#op-cf1f3c9601ba15).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1265) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L762)

<a id="op-a0d627af507534"></a>
### Stock Entry.validate materials against bom

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_materials_against_bom`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Item {0} is not part of the BOM {1} and cannot be added to this disassembly.”.format(Platform.bold(item\_code), Platform.bold(self.bom\_no)) · validation helper — translated “Item {0} quantity ({1} in stock UOM) does not match the BOM quantity {2}.”.format(Platform.bold(item\_code), flt(qty, precision), flt(expected\_qty at item\_code, precision)).

**Local steps**

- If not self.bom\_no.
  - Return no value.
- Set expected\_qty from self.get\_bom\_component\_qty().
- Set precision from Platform.get\_precision(“Stock Entry Detail”, “transfer\_qty”).
- For each tuple(item\_code, qty) in self.get\_received\_component\_qty().items().
  - If item\_code does not belong to expected\_qty.
    - Call the validation error handler Platform.throw(translated “Item {0} is not part of the BOM {1} and cannot be added to this disassembly.”.format(Platform.bold(item\_code), Platform.bold(self.bom\_no)), title = translated “Invalid Disassembly Item”).
  - If abs((flt(qty, precision) − flt(expected\_qty at item\_code, precision))) &gt; \_qty\_tolerance(precision).
    - Call the validation error handler Platform.throw(translated “Item {0} quantity ({1} in stock UOM) does not match the BOM quantity {2}.”.format(Platform.bold(item\_code), flt(qty, precision), flt(expected\_qty at item\_code, precision)), title ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get bom component qty](operations-078.md#op-d0ebb97f3f7c70), [get received component qty](operations-078.md#op-4d5caea4964644).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1264) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L761)

<a id="op-d0ebb97f3f7c70"></a>
### Stock Entry.get bom component qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_bom_component_qty`

**Inputs** self.

**Declared result** dict.

**Explicit results** component\_qty.

**Local steps**

- Bind dependencies get\_bom\_items\_as\_dict.
- Set component\_qty from defaultdict(float).
- For each row in get\_bom\_items\_as\_dict(self.bom\_no, self.company, qty = self.fg\_completed\_qty, fetch\_exploded = self.use\_multi\_level\_bom).values().
  - Update component\_qty at row.item\_code using + flt(row.qty).
- Return component\_qty.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1193) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L690)

<a id="op-cf1f3c9601ba15"></a>
### Stock Entry.validate no missing components

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_no_missing_components`

**Inputs** self, expected\_rows, precision, tolerance.

**Explicit failure paths** validation helper — translated “Item {0} is missing from this disassembly. Get the items again.”.format(Platform.bold(source\_row.item\_code)).

**Local steps**

- Set present from set of (row.ste\_detail or row.item\_code) for row drawn from self.items.
  - Draw row from self.items.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.ste\_detail → row.item\_code.
- For each tuple(source\_row, qty) in expected\_rows.
  - Set key from (source\_row.get(“name”) or source\_row.item\_code).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_row.get(“name”) → source\_row.item\_code.
  - If (not source\_row.is\_finished\_item and flt(qty, precision) &gt; tolerance and key does not belong to present).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not source\_row.is\_finished\_item → flt(qty, precision) &gt; tolerance → key does not belong to present.
    - Call the validation error handler Platform.throw(translated “Item {0} is missing from this disassembly. Get the items again.”.format(Platform.bold(source\_row.item\_code)), title = translated “Missing Disassembly Item”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1267) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L764)

<a id="op-4d5caea4964644"></a>
### Stock Entry.get received component qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_received_component_qty`

**Inputs** self.

**Declared result** dict.

**Explicit results** received\_qty.

**Local steps**

- Set received\_qty from defaultdict(float).
- For each row in self.items.
  - If (row.t\_warehouse and not row.is\_finished\_item).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.t\_warehouse → not row.is\_finished\_item.
    - Update received\_qty at row.item\_code using + flt(row.transfer\_qty).
- Return received\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1209) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L706)

<a id="op-d969a5020c4c38"></a>
### Stock Entry.get source fg qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_source_fg_qty`

**Inputs** self.

**Declared result** float.

**Record and data access** read “Stock Entry” via get\_value · read “Work Order” via get\_value.

**Explicit results** flt(Platform.db.get\_value(“Stock Entry”, self.source\_stock\_entry, “fg\_completed\_qty”)) · flt(Platform.db.get\_value(“Work Order”, self.work\_order, “produced\_qty”)) · 0.0.

**Local steps**

- If self.source\_stock\_entry.
  - Return flt(Platform.db.get\_value(“Stock Entry”, self.source\_stock\_entry, “fg\_completed\_qty”)).
- If self.work\_order.
  - Return flt(Platform.db.get\_value(“Work Order”, self.work\_order, “produced\_qty”)).
- Return 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1218) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L715)

<a id="op-883a013a5f800b"></a>
### Stock Entry.get disassembly progress

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_disassembly_progress`

**Inputs** self, source\_fg\_qty.

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(share\_to\_date = ((flt(earlier\_fg\_qty) + flt(self.fg\_completed\_qty)) ÷ source\_fg\_qty), moved\_qty = mapping of row.key → flt(row.qty) for row drawn from moved).

**Local steps**

- Set SE from Platform.qb.DocType(“Stock Entry”).
- Set SED from Platform.qb.DocType(“Stock Entry Detail”).
- If self.source\_stock\_entry.
  - Set tuple(source\_filter, key) from tuple(SE.source\_stock\_entry equals self.source\_stock\_entry, SED.ste\_detail).
- Otherwise.
  - Set tuple(source\_filter, key) from tuple(SE.work\_order equals self.work\_order, SED.item\_code).
- Set earlier from ((source\_filter bitwise and SE.purpose equals “Disassemble”) bitwise and SE.docstatus equals 1).
- Set earlier\_fg\_qty from nested operand in the contract(nested operand in the contract).where(earlier).run() at 0 at 0.
- Set moved from nested operand in the contract(nested operand in the contract, nested operand in the contract).where((earlier bitwise and nested operand in the contract equals nested operand in the contract)).groupby(key) ….
- Return Platform.\_dict(share\_to\_date = ((flt(earlier\_fg\_qty) + flt(self.fg\_completed\_qty)) ÷ source\_fg\_qty), moved\_qty = mapping of row.key → flt(row.qty) for row drawn from moved).
  - Draw row from moved.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1199) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L696)

<a id="op-9eca59f956ffcd"></a>
### Stock Entry.get component stock qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_component_stock_qty`

**Inputs** self, source\_row, progress.

**Declared result** float.

**Explicit results** flt(max(((flt(source\_row.transfer\_qty) × progress.share\_to\_date) − moved\_qty), 0), precision) · (max((units\_to\_date − round((moved\_qty ÷ step))), 0) × step).

**Local steps**

- Set precision from Platform.get\_precision(“Stock Entry Detail”, “transfer\_qty”).
- Set moved\_qty from progress.moved\_qty.get((source\_row.get(“name”) or source\_row.item\_code), 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_row.get(“name”) → source\_row.item\_code.
- Set whole\_number\_units from get\_whole\_number\_units(source\_row).
- If not whole\_number\_units.
  - Return flt(max(((flt(source\_row.transfer\_qty) × progress.share\_to\_date) − moved\_qty), 0), precision).
- Set tuple(units, step) from whole\_number\_units.
- Set units\_to\_date from math.floor(flt((units × progress.share\_to\_date), precision)).
- Return (max((units\_to\_date − round((moved\_qty ÷ step))), 0) × step).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L694)

<a id="op-73e4788c7a2d05"></a>
### Stock Entry.check if operations completed

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_check_if_operations_completed`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc · read “Manufacturing Settings” via get\_single\_value · read “Job Card” via get\_value.

**Explicit failure paths** validation helper — translated “Work Order {0}: Job Card not found for the operation {1}”.format(self.work\_order, d.operation) · validation helper with OperationsNotCompleteError — translated “Row #{0}: Operation {1} is not completed for {2} qty of finished goods in Work Order {3}. Please update oper …”.format(d.idx, Platform.bold(d.operation), Platform.bold(total\_completed\_qty), wor ….

**Local steps**

- Bind dependencies get\_upstream\_process\_loss.
- Set prod\_order from Platform.get\_doc(“Work Order”, self.work\_order).
- Set allowance\_percentage from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”)).
- For each d in prod\_order.get(“operations”).
  - Set total\_completed\_qty from ((flt(self.fg\_completed\_qty) + flt(prod\_order.produced\_qty)) + flt(prod\_order.process\_loss\_qty)).
  - Set completed\_qty from (((d.completed\_qty + d.process\_loss\_qty) + get\_upstream\_process\_loss(prod\_order, d)) + ((allowance\_percentage ÷ 100) × d.completed\_qty)).
  - If flt(total\_completed\_qty, self.precision(“fg\_completed\_qty”)) &gt; flt(completed\_qty, self.precision(“fg\_completed\_qty”)).
    - Set job\_card from Platform.db.get\_value(“Job Card”, mapping(“operation\_id” → d.name), “name”).
    - If not job\_card.
      - Call the validation error handler Platform.throw(translated “Work Order {0}: Job Card not found for the operation {1}”.format(self.work\_order, d.operation)).
    - Set work\_order\_link from get\_link\_to\_form(“Work Order”, self.work\_order).
    - Set job\_card\_link from get\_link\_to\_form(“Job Card”, job\_card).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Operation {1} is not completed for {2} qty of finished goods in Work Order {3}. Please update oper …”.format(d.idx, Platform.bold(d.operation), Platform.bold(total\_comp ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1184) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L681)
