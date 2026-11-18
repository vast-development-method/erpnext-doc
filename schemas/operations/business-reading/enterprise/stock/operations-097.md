# Inventory and warehouses · operations 97

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Stock qty vs serial no count

<a id="op-24f99f57df6ae6"></a>
### Get data

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_get_data`

**Inputs** warehouse, show\_disabled\_items.

**Record and data access** read “Item” via get\_all · read “Serial No” via count.

**Explicit results** data.

**Local steps**

- Set warehouses from get\_warehouses(warehouse).
- Set filters from mapping(“has\_serial\_no” → true).
- If not show\_disabled\_items.
  - Set filters at “disabled” from false.
- Set item\_filters from list(filters).
- If condition bound to get\_allowed\_masters\_condition(Platform.qb.DocType(“Item”).name, “Item”).
  - Evaluate item\_filters.append(condition).
- Set serial\_item\_list from Platform.get\_all(“Item”, filters = item\_filters, fields = list(“item\_code”, “item\_name”)).
- Set status\_list from list(“Active”, “Expired”).
- Set data from list().
- For each item in serial\_item\_list.
  - Set total\_serial\_no from Platform.db.count(“Serial No”, filters = mapping(“item\_code” → item.item\_code, “status” → tuple(“in”, status\_list), “warehouse” → tuple(“in”, warehouses))).
  - Set bin\_table from Platform.qb.DocType(“Bin”).
  - Set bin\_qty from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.item\_code equals nested operand in the contract.item\_code).where(bin\_table.warehouse.isin(warehouses)).run().
  - Set actual\_qty from flt(bin\_qty at 0 at 0) when bin\_qty, otherwise 0.
    - Value choice on bin\_qty — true gives flt(bin\_qty at 0 at 0), false gives 0.
  - Set difference from (total\_serial\_no − actual\_qty).
  - Set row from mapping(“item\_code” → item.item\_code, “item\_name” → item.item\_name, “total” → total\_serial\_no, “stock\_qty” → actual\_qty, …).
  - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L993) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L573)

<a id="op-5bb43660eec18f"></a>
### Sync serial no status

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_sync_serial_number_status`

**Inputs** warehouse, item\_code = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Warehouse” via exists · read “Item” via exists.

**State and service calls** enqueue with sync\_serial\_no\_status\_for\_warehouse · msgprint with translated “Serial No status sync has been queued. Reload the report after a few minutes.”.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted to update Serial No” · validation helper — translated “Warehouse {0} does not exist”.format(warehouse) · validation helper — translated “Item {0} does not exist”.format(item\_code).

**Local steps**

- If not Platform.has\_permission(“Serial No”, “write”).
  - Call the validation error handler Platform.throw(translated “Not permitted to update Serial No”, Platform.PermissionError).
- Set warehouse from cstr(warehouse).
- Set item\_code from cstr(item\_code) when item\_code, otherwise no value.
  - Value choice on item\_code — true gives cstr(item\_code), false gives no value.
- If not Platform.db.exists(“Warehouse”, warehouse).
  - Call the validation error handler Platform.throw(translated “Warehouse {0} does not exist”.format(warehouse)).
- If (item\_code and not Platform.db.exists(“Item”, item\_code)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_code → not Platform.db.exists(“Item”, item\_code).
  - Call the validation error handler Platform.throw(translated “Item {0} does not exist”.format(item\_code)).
- Evaluate Platform.enqueue(sync\_serial\_no\_status\_for\_warehouse, queue = “long”, warehouse = warehouse, item\_code = item\_code).
- Evaluate Platform.msgprint(translated “Serial No status sync has been queued. Reload the report after a few minutes.”, alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Serial No”, “write”) · service or queued work from Platform.enqueue(sync\_serial\_no\_status\_for\_warehouse, queue = “long”, warehouse = warehouse, item\_code = item\_code).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0923.json#L5574) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1000) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L580)

<a id="op-f0b4f599ab1d51"></a>
### Sync serial no status for warehouse

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_sync_serial_number_status_for_warehouse`

**Inputs** warehouse, item\_code = no value.

**Record and data access** read “Item” via get\_all.

**Local steps**

- Set filters from mapping(“has\_serial\_no” → 1).
- If item\_code.
  - Set filters at “name” from item\_code.
- Set warehouses from get\_warehouses(warehouse).
- For each item in Platform.get\_all(“Item”, filters = filters, pluck = “name”).
  - Evaluate sync\_serial\_no\_status\_for\_item(item, warehouses).
  - Evaluate restore\_serial\_nos\_in\_stock(item, warehouses).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1002) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L582)

<a id="op-538ea7d7ac6946"></a>
### Restore serial nos in stock

`operation_enterprise_binding_enterprise_stock_report_stock_qty_vs_serial_no_count_stock_qty_vs_serial_no_count_restore_serial_nos_in_stock`

**Inputs** item\_code, warehouses.

**State and service calls** request set\_value on “Serial No”.

**Explicit results** no value.

**Local steps**

- Set serial\_nos from get\_serial\_nos\_received\_in(item\_code, warehouses).
- If not serial\_nos.
  - Return no value.
- Set last\_moves from get\_last\_ledger\_moves(item\_code, serial\_nos).
- For each serial\_no in serial\_nos.
  - Set row from last\_moves.get(serial\_no).
  - If (row and flt(row.qty) &gt; 0 and row.warehouse belongs to warehouses).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row → flt(row.qty) &gt; 0 → row.warehouse belongs to warehouses.
    - Evaluate Platform.db.set\_value(“Serial No”, serial\_no, mapping(“warehouse” → row.warehouse, “status” → “Active”), update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1560) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1057)

<a id="op-5c7fd7ff2dbde5"></a>
### Get serial nos received in

`operation_enterprise_binding_enterprise_stock_report_stock_qty_vs_serial_no_count_stock_qty_vs_serial_no_count_get_serial_nos_received_in`

**Inputs** item\_code, warehouses.

**Explicit results** nested operand in the contract(nested operand in the contract).distinct().where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract &gt; n ….

**Local steps**

- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set serial\_no from Platform.qb.DocType(“Serial No”).
- Return nested operand in the contract(nested operand in the contract).distinct().where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract &gt; n ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1559) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1056)

<a id="op-80779e2c854883"></a>
### Sync serial no status for item

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_sync_serial_number_status_for_item`

**Inputs** item\_code, warehouses.

**Record and data access** read “Serial No” via get\_all.

**Explicit results** no value.

**Local steps**

- Set serial\_nos from Platform.get\_all(“Serial No”, filters = mapping(“item\_code” → item\_code, “warehouse” → tuple(“in”, warehouses), “status” → tuple(“in”, list(“Active”, “Expired”))), fields = list(“name”, “warehouse”)).
- If not serial\_nos.
  - Return no value.
- Set last\_moves from get\_last\_ledger\_moves(item\_code, list of d.name for d drawn from serial\_nos).
  - Draw d from serial\_nos.
- For each serial\_no in serial\_nos.
  - Set row from last\_moves.get(serial\_no.name).
  - If (row and flt(row.qty) &gt; 0 and row.warehouse equals serial\_no.warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row → flt(row.qty) &gt; 0 → row.warehouse equals serial\_no.warehouse.
    - Continue with the next iteration or loop test.
  - Evaluate set\_serial\_no\_state\_from\_ledger(serial\_no.name, row).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1001) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L581)

<a id="op-3fd83badce8452"></a>
### Set serial no state from ledger

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_set_serial_number_state_from_ledger`

**Inputs** serial\_no, row.

**State and service calls** request set\_value on “Serial No”.

**Explicit results** no value.

**Local steps**

- If not row.
  - Evaluate Platform.db.set\_value(“Serial No”, serial\_no, mapping(“warehouse” → no value, “status” → “Inactive”), update\_modified = false).
  - Return no value.
- Set status from get\_serial\_no\_status(Platform.\_dict(actual\_qty = flt(row.qty), warehouse = row.warehouse, voucher\_type = row.voucher\_type, voucher\_no = row.voucher\_no, …)).
- Set warehouse from row.warehouse when status equals “Active”, otherwise no value.
  - Value choice on status equals “Active” — true gives row.warehouse, false gives no value.
- Evaluate Platform.db.set\_value(“Serial No”, serial\_no, mapping(“warehouse” → warehouse, “status” → status), update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0923.json#L6680) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L999) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L579)

<a id="op-207b3193f7f168"></a>
### Get last ledger moves

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_get_last_ledger_moves`

**Inputs** item\_code, serial\_nos.

**Explicit results** last\_moves.

**Local steps**

- Set last\_moves from get\_last\_bundle\_moves(item\_code, serial\_nos).
- If missing bound to list of serial\_no for serial\_no drawn from serial\_nos where serial\_no does not belong to last\_moves.
  - Draw serial\_no from serial\_nos, keep a combination only if (serial\_no does not belong to last\_moves).
  - Evaluate set\_legacy\_last\_moves(item\_code, missing, last\_moves).
- Return last\_moves.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0923.json#L7060) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L996) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L576)

<a id="op-d64d0cf4fb854c"></a>
### Get last bundle moves

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_get_last_bundle_moves`

**Inputs** item\_code, serial\_nos.

**Explicit results** last\_moves.

**Local steps**

- Set last\_moves from mapping().
- For each start in range(0, len(serial\_nos), SYNC\_CHUNK\_SIZE).
  - For each row in get\_last\_bundle\_moves\_chunk(item\_code, serial\_nos at slice start to (start + SYNC\_CHUNK\_SIZE)).
    - Set last\_moves at row.serial\_no from row.
- Return last\_moves.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0923.json#L7217) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L994) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L574)

<a id="op-ace7101d438545"></a>
### Get last bundle moves chunk

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_get_last_bundle_moves_chunk`

**Inputs** item\_code, serial\_nos.

**Explicit results** nested operand in the contract(nested operand in the contract).select(ranked.serial\_no, ranked.qty, ranked.warehouse, ranked.voucher\_type, …).where(ranked.row\_no equals 1).run(as\_dict = true).

**Local steps**

- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set bundle from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set row\_number from nested operand in the contract().over(entry.serial\_no).orderby(Coalesce(entry.posting\_datetime, bundle.posting\_datetime), order = Order.desc).orderby(sle.creation, order = Order.desc).
- Set ranked from nested operand in the contract(nested operand in the contract).select(entry.serial\_no, entry.qty, nested operand in the contract.as\_(“warehouse”), bundle.voucher\_type, …).where(((((nested operand in the co ….
- Return nested operand in the contract(nested operand in the contract).select(ranked.serial\_no, ranked.qty, ranked.warehouse, ranked.voucher\_type, …).where(ranked.row\_no equals 1).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0924.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L995) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L575)

<a id="op-1932390052ad08"></a>
### Set legacy last moves

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_set_legacy_last_moves`

**Inputs** item\_code, serial\_nos, last\_moves.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Local steps**

- Bind dependencies get\_serial\_nos.
- Set pending from set(serial\_nos).
- Set rows from Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“item\_code” → item\_code, “is\_cancelled” → 0, “serial\_no” → tuple(“is”, “set”)), fields = list(“serial\_no”, “actual\_qty”, “warehouse”, “voucher\_type” ….
- For each row in rows.
  - Set qty from 1 when flt(row.actual\_qty) &gt; 0, otherwise negative 1.
    - Value choice on flt(row.actual\_qty) &gt; 0 — true gives 1, false gives negative 1.
  - For each serial\_no in get\_serial\_nos(row.serial\_no).
    - If serial\_no belongs to pending.
      - Set last\_moves at serial\_no from Platform.\_dict(qty = qty, warehouse = row.warehouse, voucher\_type = row.voucher\_type, voucher\_no = row.voucher\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0924.json#L845) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L998) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L578)

## Record · Stock reconciliation

[Record definition](../../../../data/record-types/stock_reconciliation.json)

<a id="op-ade4e3e6fa844e"></a>
### Stock Reconciliation.initialize

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.head\_row from list(“Item Code”, “Warehouse”, “Quantity”, “Valuation Rate”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0857.json#L4714) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1048)

<a id="op-fbc3fb7ccd6de1"></a>
### Stock Reconciliation.validate

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_validate`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If self.purpose equals ADJUSTMENT\_ENTRY.
  - Evaluate self.validate\_adjustment\_entry().
  - Return no value.
- Evaluate self.validate\_items\_exist().
- If not self.expense\_account.
  - Set self.expense\_account from Platform.get\_cached\_value(“Company”, self.company, “stock\_adjustment\_account”).
- If not self.cost\_center.
  - Set self.cost\_center from Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).
- Evaluate self.validate\_posting\_time().
- Evaluate self.set\_current\_serial\_and\_batch\_bundle().
- Evaluate self.set\_new\_serial\_and\_batch\_bundle().
- Evaluate self.validate\_duplicate\_serial\_and\_batch\_bundle(“items”).
- Evaluate self.remove\_items\_with\_no\_change().
- Evaluate self.validate\_data().
- Evaluate self.change\_row\_indexes().
- Evaluate self.validate\_expense\_account().
- Evaluate self.validate\_opening\_stock().
- Evaluate self.validate\_customer\_provided\_item().
- Evaluate self.set\_zero\_value\_for\_customer\_provided\_items().
- Evaluate self.clean\_serial\_nos().
- Evaluate self.set\_total\_qty\_and\_amount().
- Evaluate self.validate\_putaway\_capacity().
- Evaluate self.validate\_inventory\_dimension().
- Evaluate self.validate\_inventory\_dimension\_mandatory().
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “qty”).
- If self.\_action equals “submit”.
  - Evaluate self.validate\_reserved\_stock().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate adjustment entry](operations-097.md#op-6163de27d9c55b), [set current serial and batch bundle](operations-097.md#op-eff422cd884076), [set new serial and batch bundle](operations-098.md#op-e60a0d06f5bc22), [remove items with no change](operations-098.md#op-6d7d6373f5dea1), [validate data](operations-098.md#op-a622adf04f95a9), [change row indexes](operations-098.md#op-79038b69f827fd), [validate expense account](operations-098.md#op-174767fa3ddc9e), [validate opening stock](operations-098.md#op-539e105c27a2df), [set zero value for customer provided items](operations-099.md#op-cec0f585e97eab), [set total qty and amount](operations-099.md#op-6e0fb676af2140), [validate inventory dimension](operations-097.md#op-bb3728b1243c90), [validate reserved stock](operations-098.md#op-6148a71f11d4e3).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “stock\_adjustment\_account”), Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L145) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1066)

<a id="op-6163de27d9c55b"></a>
### Stock Reconciliation.validate adjustment entry

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_validate_adjustment_entry`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- Evaluate AdjustmentEntry(self).validate\_made\_from\_report().
- If not self.expense\_account.
  - Set self.expense\_account from Platform.get\_cached\_value(“Company”, self.company, “stock\_adjustment\_account”).
- If not self.cost\_center.
  - Set self.cost\_center from Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).
- Evaluate self.validate\_posting\_time().
- Evaluate self.validate\_expense\_account().
- Evaluate AdjustmentEntry(self).validate().
- If self.\_action equals “submit”.
  - Evaluate self.validate\_reserved\_stock().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate expense account](operations-098.md#op-174767fa3ddc9e), [validate reserved stock](operations-098.md#op-6148a71f11d4e3).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “stock\_adjustment\_account”), Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L805)

<a id="op-1e3c3b169dd616"></a>
### Stock Reconciliation.on update

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_on_update`

**Inputs** self.

**Local steps**

- Evaluate super().on\_update().
- Evaluate self.set\_serial\_and\_batch\_bundle(ignore\_validate = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0857.json#L5465) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1055)

<a id="op-bb3728b1243c90"></a>
### Stock Reconciliation.validate inventory dimension

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_validate_inventory_dimension`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: You cannot use the inventory dimension '{1}' in Stock Reconciliation to modify the quantity or val …”.format(row.idx, bold(dimension.get(“doctype”))).

**Local steps**

- Set dimensions from get\_inventory\_dimensions().
- For each dimension in dimensions.
  - For each row in self.items.
    - If (not row.batch\_no and row.current\_qty and row.get(dimension.get(“source\_fieldname”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.batch\_no → row.current\_qty → row.get(dimension.get(“source\_fieldname”)).
      - Call the validation error handler Platform.throw(translated “Row #{0}: You cannot use the inventory dimension '{1}' in Stock Reconciliation to modify the quantity or val …”.format(row.idx, bold(dimension.get(“doctype”)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0857.json#L5549) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L149) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1070)

<a id="op-5f2d01de37a631"></a>
### Stock Reconciliation.on submit

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_on_submit`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.purpose equals ADJUSTMENT\_ENTRY.
  - Evaluate AdjustmentEntry(self).post().
  - Evaluate self.make\_gl\_entries().
  - Evaluate self.repost\_future\_sle\_and\_gle().
  - Return no value.
- Evaluate self.make\_bundle\_for\_current\_qty().
- Evaluate self.make\_bundle\_using\_old\_serial\_batch\_fields().
- Evaluate self.update\_stock\_ledger().
- Evaluate self.validate\_future\_batch\_quantity().
- Evaluate self.make\_gl\_entries().
- Evaluate self.repost\_future\_sle\_and\_gle().

If control reaches the end, it returns no value.

**Methods declared on this owner** [make bundle for current qty](operations-097.md#op-4f521717f816e0), [update stock ledger](operations-098.md#op-24873dfd5aa284), [validate future batch quantity](operations-097.md#op-034d1317b1c4d5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1054)

<a id="op-034d1317b1c4d5"></a>
### Stock Reconciliation.validate future batch quantity

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_validate_future_batch_quantity`

**Inputs** self.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**Local steps**

- For each row in self.items.
  - If row.current\_serial\_and\_batch\_bundle.
    - Evaluate Platform.get\_doc(“Serial and Batch Bundle”, row.current\_serial\_and\_batch\_bundle).validate\_future\_batch\_quantity().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L806)

<a id="op-e3769e75914a62"></a>
### Stock Reconciliation.on cancel

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_on_cancel`

**Inputs** self.

**State and service calls** call cancel on AdjustmentEntry(self).

**Explicit results** no value.

**Local steps**

- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Repost Item Valuation”, “Serial and Batch Bundle”).
- If self.purpose equals ADJUSTMENT\_ENTRY.
  - Evaluate self.validate\_reserved\_stock().
  - Evaluate AdjustmentEntry(self).cancel().
  - Evaluate self.make\_gl\_entries\_on\_cancel().
  - Evaluate self.repost\_future\_sle\_and\_gle().
  - Return no value.
- Evaluate self.validate\_reserved\_stock().
- Evaluate self.make\_sle\_on\_cancel().
- Evaluate self.make\_gl\_entries\_on\_cancel().
- Evaluate self.repost\_future\_sle\_and\_gle().
- Evaluate self.delete\_auto\_created\_batches().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate reserved stock](operations-098.md#op-6148a71f11d4e3), [make sle on cancel](operations-098.md#op-eb26d64badc13c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1053)

<a id="op-4f521717f816e0"></a>
### Stock Reconciliation.make bundle for current qty

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_make_bundle_for_current_quantity`

**Inputs** self.

**State and service calls** call db\_set on row.

**Local steps**

- Bind dependencies SerialBatchCreation.
- For each row in self.items.
  - If not row.use\_serial\_batch\_fields.
    - Continue with the next iteration or loop test.
  - If row.current\_serial\_and\_batch\_bundle.
    - Continue with the next iteration or loop test.
  - If (row.current\_qty and (row.current\_serial\_no or row.batch\_no)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.current\_qty → (row.current\_serial\_no or row.batch\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.current\_serial\_no → row.batch\_no.
    - Set sn\_doc from SerialBatchCreation(mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “posting\_datetime” → combine\_datetime(self.posting\_date, self.posting\_time), “voucher\_type” → self.doctype, …)).make\_se …().
      - Value choice on row.current\_qty &gt; 0 — true gives “Outward”, false gives “Inward”.
      - Value choice on row.current\_serial\_no — true gives get\_serial\_nos(row.current\_serial\_no), false gives no value.
      - Value choice on row.batch\_no — true gives Platform.\_dict(mapping(row.batch\_no → row.current\_qty)), false gives no value.
    - Set row.current\_serial\_and\_batch\_bundle from sn\_doc.name.
    - Evaluate row.db\_set(mapping(“current\_serial\_and\_batch\_bundle” → sn\_doc.name, “current\_serial\_no” → empty text)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0858.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1050)

<a id="op-eff422cd884076"></a>
### Stock Reconciliation.set current serial and batch bundle

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_set_current_serial_and_batch_bundle`

**Inputs** self, voucher\_detail\_no = no value, save = false.

**Declared result** no value.

**Record and data access** read “Item” via get\_cached\_value · read “Serial and Batch Bundle” via get\_value · resolve a document from “Serial and Batch Bundle” via get\_doc · resolve a document from mapping(“doctype” → “Serial and Batch Bundle”, “company” → self.company, “item\_code” → item.item\_code, “warehouse” → item.warehouse, …) via get\_doc.

**State and service calls** call submit on sabb\_doc · call db\_set on item · call save on serial\_and\_batch\_bundle · call db\_set on serial\_and\_batch\_bundle.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row # {0}: Please add Serial and Batch Bundle for Item {1}”.format(item.idx, Platform.bold(item.item\_code)) · validation helper — translated “Row # {0}: Please enter quantity for Item {1} as it is not zero.”.format(item.idx, item.item\_code).

**Local steps**

- For each item in self.items.
  - If (voucher\_detail\_no and voucher\_detail\_no differs from item.name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_detail\_no → voucher\_detail\_no differs from item.name.
    - Continue with the next iteration or loop test.
  - If not item.item\_code.
    - Continue with the next iteration or loop test.
  - Set item\_details from Platform.get\_cached\_value(“Item”, item.item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1).
  - If not (item\_details.has\_serial\_no or item\_details.has\_batch\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_details.has\_serial\_no → item\_details.has\_batch\_no.
    - Continue with the next iteration or loop test.
  - If (not item.use\_serial\_batch\_fields and not item.reconcile\_all\_serial\_batch and not item.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.use\_serial\_batch\_fields → not item.reconcile\_all\_serial\_batch → not item.serial\_and\_batch\_bundle.
    - Call the validation error handler Platform.throw(translated “Row # {0}: Please add Serial and Batch Bundle for Item {1}”.format(item.idx, Platform.bold(item.item\_code))).
  - If (not item.reconcile\_all\_serial\_batch and item.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.reconcile\_all\_serial\_batch → item.serial\_and\_batch\_bundle.
    - Set bundle from self.get\_bundle\_for\_specific\_serial\_batch(item).
    - If not bundle.
      - Continue with the next iteration or loop test.
    - Set item.current\_serial\_and\_batch\_bundle from bundle.name.
    - Set item.current\_valuation\_rate from abs(bundle.avg\_rate).
    - If bundle.total\_qty.
      - Set item.current\_qty from abs(bundle.total\_qty).
    - If save.
      - If not item.current\_qty.
        - Call the validation error handler Platform.throw(translated “Row # {0}: Please enter quantity for Item {1} as it is not zero.”.format(item.idx, item.item\_code)).
      - If (self.docstatus equals 1 and item.current\_serial\_and\_batch\_bundle and Platform.db.get\_value(“Serial and Batch Bundle”, item.current\_serial\_and\_batch\_bundle, “docstatus”) equals 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → item.current\_serial\_and\_batch\_bundle → Platform.db.get\_value(“Serial and Batch Bundle”, item.current\_serial\_and\_batch\_bundle, “docstatus”) equals 0.
        - Set sabb\_doc from Platform.get\_doc(“Serial and Batch Bundle”, item.current\_serial\_and\_batch\_bundle).
        - Set sabb\_doc.voucher\_no from self.name.
        - Evaluate sabb\_doc.submit().
      - Evaluate item.db\_set(mapping(“current\_serial\_and\_batch\_bundle” → item.current\_serial\_and\_batch\_bundle, “current\_qty” → item.current\_qty, “current\_valuation\_rate” → item.current\_valuation\_rate)).
    - If not item.valuation\_rate.
      - Set item.valuation\_rate from item.current\_valuation\_rate.
    - Continue with the next iteration or loop test.
  - If (not save and item.use\_serial\_batch\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not save → item.use\_serial\_batch\_fields.
    - Continue with the next iteration or loop test.
  - If not item.current\_serial\_and\_batch\_bundle.
    - Set serial\_and\_batch\_bundle from Platform.get\_doc(mapping(“doctype” → “Serial and Batch Bundle”, “company” → self.company, “item\_code” → item.item\_code, “warehouse” → item.warehouse, …)).
  - Otherwise.
    - Set serial\_and\_batch\_bundle from Platform.get\_doc(“Serial and Batch Bundle”, item.current\_serial\_and\_batch\_bundle).
    - Evaluate serial\_and\_batch\_bundle.set(“entries”, list()).
  - If item\_details.has\_serial\_no.
    - Set serial\_nos\_details from get\_available\_serial\_nos(Platform.\_dict(mapping(“item\_code” → item.item\_code, “warehouse” → item.warehouse, “posting\_datetime” → combine\_datetime(self.posting\_date, self.posting\_time), “ignore\_warehouse” → 1, …))).
    - For each serial\_no\_row in serial\_nos\_details.
      - Evaluate serial\_and\_batch\_bundle.append(“entries”, mapping(“serial\_no” → serial\_no\_row.serial\_no, “qty” → negative 1, “warehouse” → serial\_no\_row.warehouse, “batch\_no” → serial\_no\_row.batch\_no)).
  - Otherwise.
    - If item\_details.has\_batch\_no.
      - Set batch\_nos\_details from get\_available\_batches(Platform.\_dict(mapping(“item\_code” → item.item\_code, “warehouse” → item.warehouse, “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time, …))).
      - For each tuple(batch\_no, qty) in batch\_nos\_details.items().
        - Evaluate serial\_and\_batch\_bundle.append(“entries”, mapping(“batch\_no” → batch\_no, “qty” → (qty × negative 1), “warehouse” → item.warehouse)).
  - If not serial\_and\_batch\_bundle.entries.
    - If voucher\_detail\_no.
      - Return no value.
    - Continue with the next iteration or loop test.
  - Evaluate serial\_and\_batch\_bundle.save().
  - Set item.current\_serial\_and\_batch\_bundle from serial\_and\_batch\_bundle.name.
  - Set item.current\_qty from abs(serial\_and\_batch\_bundle.total\_qty).
  - Set item.current\_valuation\_rate from abs(serial\_and\_batch\_bundle.avg\_rate).
  - If save.
    - Set sle\_creation from Platform.db.get\_value(“Serial and Batch Bundle”, item.serial\_and\_batch\_bundle, “creation”).
    - Set creation from add\_to\_date(sle\_creation, seconds = negative 1).
    - Evaluate item.db\_set(mapping(“current\_serial\_and\_batch\_bundle” → item.current\_serial\_and\_batch\_bundle, “current\_qty” → item.current\_qty, “current\_valuation\_rate” → item.current\_valuation\_rate, “creation” → creation)).
    - Evaluate serial\_and\_batch\_bundle.db\_set(mapping(“creation” → creation, “voucher\_no” → self.name, “voucher\_detail\_no” → voucher\_detail\_no)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get bundle for specific serial batch](operations-097.md#op-b2f044b0f2ec43).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1059)

<a id="op-b2f044b0f2ec43"></a>
### Stock Reconciliation.get bundle for specific serial batch

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_get_bundle_for_specific_serial_batch`

**Inputs** self, row.

**Declared result** str.

**State and service calls** call save on reco\_obj.

**Explicit results** Platform.\_dict(mapping(“name” → row.current\_serial\_and\_batch\_bundle, “avg\_rate” → row.current\_valuation\_rate)) · reco\_obj.

**Local steps**

- Bind dependencies SerialBatchCreation.
- If (row.current\_serial\_and\_batch\_bundle and not self.has\_change\_in\_serial\_batch(row)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.current\_serial\_and\_batch\_bundle → not self.has\_change\_in\_serial\_batch(row).
  - Return Platform.\_dict(mapping(“name” → row.current\_serial\_and\_batch\_bundle, “avg\_rate” → row.current\_valuation\_rate)).
- Set cls\_obj from SerialBatchCreation(mapping(“type\_of\_transaction” → “Outward”, “serial\_and\_batch\_bundle” → row.serial\_and\_batch\_bundle, “item\_code” → row.get(“item\_code”), “warehouse” → row.get(“warehouse”), …)).
- Set reco\_obj from cls\_obj.duplicate\_package().
- Set total\_current\_qty from 0.0.
- Set entries\_in\_stock from list().
- Set serial\_nos\_in\_stock from self.get\_serial\_nos\_in\_stock(row, reco\_obj.entries).
- For each entry in reco\_obj.entries.
  - If (not entry.batch\_no or entry.serial\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not entry.batch\_no → entry.serial\_no.
    - If entry.serial\_no does not belong to serial\_nos\_in\_stock.
      - Continue with the next iteration or loop test.
    - Set current\_qty from entry.qty.
  - Otherwise.
    - Set current\_qty from get\_batch\_qty\_for\_stock(entry.batch\_no, row.warehouse, item\_code = row.item\_code, ignore\_voucher\_nos = list(self.name), posting\_date = self.posting\_date, posting\_time = self.posting\_time, …).
    - If not current\_qty.
      - Continue with the next iteration or loop test.
  - Update total\_current\_qty using + current\_qty.
  - Set entry.qty from (current\_qty × negative 1).
  - Evaluate entries\_in\_stock.append(entry).
- If total\_current\_qty.
  - Evaluate reco\_obj.set(“entries”, entries\_in\_stock).
  - Evaluate reco\_obj.save().
  - Set row.current\_qty from total\_current\_qty.
  - Return reco\_obj.

If control reaches the end, it returns no value.

**Methods declared on this owner** [has change in serial batch](operations-097.md#op-d9a7aedd483a2e), [get serial nos in stock](operations-097.md#op-09c5f2759b0ad5).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1042)

<a id="op-09c5f2759b0ad5"></a>
### Stock Reconciliation.get serial nos in stock

`operation_enterprise_binding_enterprise_stock_doctype_stock_reconciliation_stock_reconciliation_stockreconciliation_get_serial_nos_in_stock`

**Inputs** self, row, entries.

**Declared result** set.

**Explicit results** set() · set(in\_stock).

**Local steps**

- Set serial\_nos from list of entry.serial\_no for entry drawn from entries where entry.serial\_no.
  - Draw entry from entries, keep a combination only if (entry.serial\_no).
- If not serial\_nos.
  - Return set().
- Set in\_stock from get\_serial\_nos\_based\_on\_posting\_date(Platform.\_dict(mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “posting\_datetime” → combine\_datetime(self.posting\_date, self.posting\_time), “serial\_no ….
- Return set(in\_stock).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1302) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L799)

<a id="op-d9a7aedd483a2e"></a>
### Stock Reconciliation.has change in serial batch

`operation_enterprise_stock_record_definitions_stock_reconciliation_business_behavior_stock_reconciliation_has_change_in_serial_batch`

**Inputs** self, row.

**Declared result** bool.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**State and service calls** request delete\_doc for “Serial and Batch Bundle”.

**Explicit results** true · false.

**Local steps**

- Set bundles from mapping(row.serial\_and\_batch\_bundle → list(), row.current\_serial\_and\_batch\_bundle → list()).
- Set data from Platform.get\_all(“Serial and Batch Entry”, fields = list(“serial\_no”, “batch\_no”, “parent”), filters = mapping(“parent” → tuple(“in”, list(row.serial\_and\_batch\_bundle, row.current\_serial\_and\_batch\_bundle)) ….
- For each d in data.
  - Evaluate bundles at d.parent.append((d.serial\_no or d.batch\_no)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.serial\_no → d.batch\_no.
- Set diff from (set(bundles at row.serial\_and\_batch\_bundle) − set(bundles at row.current\_serial\_and\_batch\_bundle)).
- If diff.
  - Set bundle from row.current\_serial\_and\_batch\_bundle.
  - Set row.current\_serial\_and\_batch\_bundle from no value.
  - Evaluate Platform.delete\_doc(“Serial and Batch Bundle”, bundle).
  - Return true.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0858.json#L4247) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1047)
