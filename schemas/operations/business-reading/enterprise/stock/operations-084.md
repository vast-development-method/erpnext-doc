# Inventory and warehouses · operations 84

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock entry

[Record definition](../../../../data/record-types/stock_entry.json)

<a id="op-2c0345c4548920"></a>
### Stock Entry.update transferred qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_update_transferred_qty`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Explicit results** no value.

**Local steps**

- If (self.purpose equals “Material Transfer” and self.outgoing\_stock\_entry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Material Transfer” → self.outgoing\_stock\_entry.
  - Set tuple(stock\_entries, stock\_entries\_child\_list) from self.get\_stock\_in\_transferred\_qty().
  - If not stock\_entries.
    - Return no value.
  - Set cond from empty text.
  - For each tuple(data, transferred\_qty) in stock\_entries.items().
    - Update cond using + “ WHEN (parent = {} and name = {}) THEN {}\\n\\t\\t\\t\\t\\t”.format(Platform.db.escape(data at 0), Platform.db.escape(data at 1), transferred\_qty).
  - If stock\_entries\_child\_list.
    - Evaluate Platform.db.sql(multiline text in the contract.format(cond = cond, ste\_details = “,”.join((list(“%s”) × len(stock\_entries\_child\_list)))), tuple(stock\_entries\_child\_list)).
  - Set args from mapping(“source\_dt” → “Stock Entry Detail”, “target\_field” → “transferred\_qty”, “target\_ref\_field” → “transfer\_qty”, “target\_dt” → “Stock Entry Detail”, …).
  - Evaluate self.\_update\_percent\_field\_in\_targets(args, update\_modified = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get stock in transferred qty](operations-083.md#op-f2cf1b56d58d64).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1251) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L748)

<a id="op-307ed8cd22fe4a"></a>
### Stock Entry.update quality inspection

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_update_quality_inspection`

**Inputs** self.

**State and service calls** request set\_value on “Quality Inspection”.

**Local steps**

- If self.inspection\_required.
  - Set reference\_type, reference\_name from empty text.
  - If self.docstatus equals 1.
    - Set reference\_name from self.name.
    - Set reference\_type from “Stock Entry”.
  - For each d in self.items.
    - If d.quality\_inspection.
      - Evaluate Platform.db.set\_value(“Quality Inspection”, d.quality\_inspection, mapping(“reference\_type” → reference\_type, “reference\_name” → reference\_name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0838.json#L5680) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L821)

<a id="op-1ed6300fa18aba"></a>
### Stock Entry.set material request transfer status

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_material_request_transfer_status`

**Inputs** self, status.

**Record and data access** read “Stock Entry” via get\_value · read “Stock Entry Detail” via get\_value.

**State and service calls** request set\_value on “Material Request”.

**Local steps**

- Set material\_requests from list().
- If self.outgoing\_stock\_entry.
  - Set parent\_se from Platform.get\_value(“Stock Entry”, self.outgoing\_stock\_entry, “add\_to\_transit”).
- For each item in self.items.
  - Set material\_request from item.get(“material\_request”).
  - If (self.purpose equals “Material Transfer” and material\_request does not belong to material\_requests).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Material Transfer” → material\_request does not belong to material\_requests.
    - If (self.outgoing\_stock\_entry and parent\_se).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.outgoing\_stock\_entry → parent\_se.
      - Set material\_request from Platform.get\_value(“Stock Entry Detail”, item.ste\_detail, “material\_request”).
  - If (material\_request and material\_request does not belong to material\_requests).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in material\_request → material\_request does not belong to material\_requests.
    - Evaluate material\_requests.append(material\_request).
    - Set request\_status from status.
    - If request\_status equals “Completed”.
      - Set qty from get\_transferred\_qty(material\_request).
      - If qty.get(“transfer\_qty”) &gt; qty.get(“transferred\_qty”).
        - Set request\_status from “In Transit”.
    - Evaluate Platform.db.set\_value(“Material Request”, material\_request, “transfer\_status”, request\_status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L733)

<a id="op-9d8ee47d8a638c"></a>
### Stock Entry.set serial no batch for finished good

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_serial_no_batch_for_finished_good`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not ((self.pro\_doc.has\_serial\_no or self.pro\_doc.has\_batch\_no) and Platform.db.get\_single\_value(“Manufacturing Settings”, “make\_serial\_no\_batch\_from\_work\_order”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.pro\_doc.has\_serial\_no or self.pro\_doc.has\_batch\_no) → Platform.db.get\_single\_value(“Manufacturing Settings”, “make\_serial\_no\_batch\_from\_work\_order”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.pro\_doc.has\_serial\_no → self.pro\_doc.has\_batch\_no.
  - Return no value.
- For each d in self.items.
  - If (d.is\_finished\_item and d.item\_code equals self.pro\_doc.production\_item and not d.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_finished\_item → d.item\_code equals self.pro\_doc.production\_item → not d.serial\_and\_batch\_bundle.
    - Set serial\_nos from self.get\_available\_serial\_nos().
    - If serial\_nos.
      - Set row from Platform.\_dict(mapping(“serial\_nos” → serial\_nos at slice 0 to cint(d.qty))).
      - Set id from create\_serial\_and\_batch\_bundle(self, row, Platform.\_dict(mapping(“item\_code” → d.item\_code, “warehouse” → d.t\_warehouse))).
      - Set d.serial\_and\_batch\_bundle from id.
      - Set d.use\_serial\_batch\_fields from 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get available serial nos](operations-084.md#op-6742ef60c3400e).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “make\_serial\_no\_batch\_from\_work\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L741)

<a id="op-6742ef60c3400e"></a>
### Stock Entry.get available serial nos

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_available_serial_nos`

**Inputs** self.

**Declared result** list at str.

**Record and data access** read “Serial No” via get\_all.

**Explicit results** serial\_nos.

**Local steps**

- Set serial\_nos from list().
- Set data from Platform.get\_all(“Serial No”, filters = mapping(“item\_code” → self.pro\_doc.production\_item, “warehouse” → tuple(“is”, “not set”), “status” → “Inactive”, “work\_order” → self.pro\_doc.name), fields = list(“na ….
- For each row in data.
  - Evaluate serial\_nos.append(row.name).
- Return serial\_nos.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1190) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L687)

<a id="op-7fefbed445543d"></a>
### Stock Entry.update subcontracting order status

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_update_subcontracting_order_status`

**Inputs** self.

**Local steps**

- If (self.subcontracting\_order and self.purpose belongs to list(“Send to Subcontractor”, “Material Transfer”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.subcontracting\_order → self.purpose belongs to list(“Send to Subcontractor”, “Material Transfer”).
  - Bind dependencies set\_subcontracting\_order\_status.
  - Evaluate set\_subcontracting\_order\_status(self.subcontracting\_order).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0838.json#L5915) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L823)

<a id="op-b625b7c95f64f5"></a>
### Stock Entry.update pick list status

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_update_pick_list_status`

**Inputs** self.

**Local steps**

- Bind dependencies update\_pick\_list\_status.
- If self.pick\_list.
  - Evaluate self.update\_qty().
- Evaluate update\_pick\_list\_status(self.pick\_list).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0838.json#L6028) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L820)

<a id="op-90fe9a8c33f664"></a>
### Stock Entry.set missing values

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_missing_values`

**Inputs** self.

**Local steps**

- Evaluate self.set\_transfer\_qty().
- Evaluate self.set\_actual\_qty().
- Evaluate self.calculate\_rate\_and\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set transfer qty](operations-077.md#op-90c3ce21ce82a9), [set actual qty](operations-079.md#op-eef6d1415cea78), [calculate rate and amount](operations-079.md#op-e089b5c80e72bd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0838.json#L6124) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1219) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L809)

<a id="op-7819b5c49d344a"></a>
### Move sample to retention warehouse

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_move_sample_to_retention_warehouse`

**Inputs** company, items.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Serial No” via exists.

**State and service calls** request new\_doc for “Stock Entry” · call save on sabb.

**Explicit results** stock\_entry.as\_dict().

**Local steps**

- Bind dependencies SerialBatchCreation, get\_batch\_nos.
- If isinstance(items, str).
  - Set items from json.loads(items).
- Set retention\_warehouse from get\_sample\_retention\_warehouse(company).
- Set stock\_entry from Platform.new\_doc(“Stock Entry”).
- Set stock\_entry.company from company.
- Set stock\_entry.purpose from “Material Transfer”.
- Evaluate stock\_entry.set\_stock\_entry\_type().
- For each item in items.
  - If (item.get(“sample\_quantity”) and item.get(“serial\_and\_batch\_bundle”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“sample\_quantity”) → item.get(“serial\_and\_batch\_bundle”).
    - Set warehouse from (item.get(“t\_warehouse”) or item.get(“warehouse”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“t\_warehouse”) → item.get(“warehouse”).
    - Set total\_qty from 0.
    - Set cls\_obj from SerialBatchCreation(mapping(“type\_of\_transaction” → “Outward”, “serial\_and\_batch\_bundle” → item.get(“serial\_and\_batch\_bundle”), “item\_code” → item.get(“item\_code”), “warehouse” → warehouse, …)).
    - Set sabb from cls\_obj.duplicate\_package().
    - Set batches from get\_batch\_nos(item.get(“serial\_and\_batch\_bundle”)).
    - Set sabe\_list from list().
    - For each batch\_no in batches.keys().
      - Set sample\_quantity from validate\_sample\_quantity(item.get(“item\_code”), item.get(“sample\_quantity”), (item.get(“transfer\_qty”) or item.get(“qty”)), company, …).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“transfer\_qty”) → item.get(“qty”).
      - Set sabe from next(generator of item for item drawn from sabb.entries where item.batch\_no equals batch\_no).
        - Draw item from sabb.entries, keep a combination only if (item.batch\_no equals batch\_no).
      - If sample\_quantity.
        - If sabb.has\_serial\_no.
          - Set new\_sabe from list of entry for entry drawn from sabb.entries where (entry.batch\_no equals batch\_no and Platform.db.exists(“Serial No”, mapping(“name” → entry.serial\_no, “warehouse” → warehouse))) at slice no value to i ….
            - Draw entry from sabb.entries, keep a combination only if ((entry.batch\_no equals batch\_no and Platform.db.exists(“Serial No”, mapping(“name” → entry.serial\_no, “warehouse” → warehouse)))).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.batch\_no equals batch\_no → Platform.db.exists(“Serial No”, mapping(“name” → entry.serial\_no, “warehouse” → warehouse)).
          - Evaluate sabe\_list.extend(new\_sabe).
          - Update total\_qty using + len(new\_sabe).
        - Otherwise.
          - Update total\_qty using + sample\_quantity.
          - Set sabe.qty from sample\_quantity.
      - Otherwise.
        - Evaluate sabb.entries.remove(sabe).
    - If total\_qty.
      - If sabe\_list.
        - Set sabb.entries from sabe\_list.
      - Evaluate sabb.save().
      - Evaluate stock\_entry.append(“items”, mapping(“item\_code” → item.get(“item\_code”), “s\_warehouse” → warehouse, “t\_warehouse” → retention\_warehouse, “qty” → total\_qty, …)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“conversion\_factor”) → 1.0.
- If stock\_entry.get(“items”).
  - Return stock\_entry.as\_dict().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1164) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L661)

<a id="op-623700e8bf4f87"></a>
### Make stock in entry

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_make_stock_in_entry`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Set qty\_precision from Platform.get\_precision(“Stock Entry Detail”, “transfer\_qty”).
- Bind local operation get\_remaining\_transfer\_qty for subsequent calls.
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Bind local operation map\_target\_dimensions\_to\_source for subsequent calls.
- Bind local operation get\_remaining\_qty\_in\_row\_uom for subsequent calls.
- Set doclist from get\_mapped\_doc(“Stock Entry”, source\_name, mapping(“Stock Entry” → mapping(“doctype” → “Stock Entry”, “field\_map” → mapping(“name” → “outgoing\_stock\_entry”), “validation” → mapping(“docstatus” → list(“=”,  ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1159) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L763)

<a id="op-362ce3dbbfc116"></a>
### Make stock in entry.get remaining transfer qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_make_stock_in_entry_get_remaining_transfer_qty`

**Inputs** source\_doc.

**Explicit results** flt(remaining\_qty, qty\_precision).

**Local steps**

- Set remaining\_qty from (flt(source\_doc.transfer\_qty) − flt(source\_doc.transferred\_qty)).
- Return flt(remaining\_qty, qty\_precision).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1162) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L659)

<a id="op-7704e8e07d2357"></a>
### Make stock in entry.set missing values

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_make_stock_in_entry_set_missing_values`

**Inputs** source, target.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- Set target.stock\_entry\_type from “Material Transfer”.
- Set target.add\_to\_transit from 0.
- Evaluate target.set\_missing\_values().
- If not Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).
  - Evaluate target.make\_serial\_and\_batch\_bundle\_for\_transfer().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1160) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L764)

<a id="op-55ae4cfdf94c7f"></a>
### Make stock in entry.update item

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_make_stock_in_entry_update_item`

**Inputs** source\_doc, target\_doc, source\_parent.

**Record and data access** read “Stock Entry” via get\_value · read “Material Request Item” via get\_value.

**Local steps**

- Set target\_doc.t\_warehouse from empty text.
- If (source\_doc.material\_request\_item and source\_doc.material\_request).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in source\_doc.material\_request\_item → source\_doc.material\_request.
  - Set add\_to\_transit from Platform.db.get\_value(“Stock Entry”, source\_name, “add\_to\_transit”).
  - If add\_to\_transit.
    - Set warehouse from Platform.get\_value(“Material Request Item”, source\_doc.material\_request\_item, “warehouse”).
    - Set target\_doc.t\_warehouse from warehouse.
- Set target\_doc.s\_warehouse from source\_doc.t\_warehouse.
- Set target\_doc.qty from get\_remaining\_qty\_in\_row\_uom(source\_doc).
- Evaluate map\_target\_dimensions\_to\_source(source\_doc, target\_doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1161) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L765)

<a id="op-4dd7ec54a7628c"></a>
### Make stock in entry.map target dimensions to source

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_make_stock_in_entry_map_target_dimensions_to_source`

**Inputs** source\_doc, target\_doc.

**Local steps**

- Bind dependencies get\_inventory\_dimensions.
- For each dimension in get\_inventory\_dimensions().
  - Set fieldname from dimension.source\_fieldname.
  - If (fieldname.startswith(“to\_”) or not target\_doc.meta.has\_field(formatted text to\_{fieldname})).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldname.startswith(“to\_”) → not target\_doc.meta.has\_field(formatted text to\_{fieldname}).
    - Continue with the next iteration or loop test.
  - Evaluate target\_doc.set(fieldname, source\_doc.get(formatted text to\_{fieldname})).
  - Evaluate target\_doc.set(formatted text to\_{fieldname}, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1163) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L660)

<a id="op-526a8a06f0f307"></a>
### Make stock in entry.get remaining qty in row uom

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_make_stock_in_entry_get_remaining_qty_in_row_uom`

**Inputs** source\_doc.

**Explicit results** qty · (remaining\_qty ÷ conversion\_factor).

**Local steps**

- Set remaining\_qty from get\_remaining\_transfer\_qty(source\_doc).
- Set conversion\_factor from flt(source\_doc.conversion\_factor).
- Set qty from flt((flt(source\_doc.qty) − (flt(source\_doc.transferred\_qty) ÷ conversion\_factor)), source\_doc.precision(“qty”)).
- If flt((qty × conversion\_factor), qty\_precision) equals remaining\_qty.
  - Return qty.
- Return (remaining\_qty ÷ conversion\_factor).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1161) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L658)

<a id="op-12f4baee4fbe7b"></a>
### Get pending work orders

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_get_pending_work_orders`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Declared result** list.

**Explicit results** query.where(work\_order.qty &gt; work\_order.produced\_qty).run().

**Local steps**

- Set work\_order from Platform.qb.DocType(“Work Order”).
- Set query from Platform.qb.get\_query(“Work Order”, fields = list(“name”, “production\_item”), filters = mapping(“docstatus” → 1, “company” → filters.get(“company”), “name” → tuple(“like”, formatted text %{txt}%)), order\_b ….
- Return query.where(work\_order.qty &gt; work\_order.produced\_qty).run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1152) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L756)

<a id="op-308bbb65ed43b0"></a>
### Get work order details

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_get_work_order_details`

**Inputs** work\_order, company.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Explicit results** mapping(“from\_bom” → 1, “bom\_no” → work\_order.bom\_no, “use\_multi\_level\_bom” → work\_order.use\_multi\_level\_bom, “wip\_warehouse” → work\_order.wip\_warehouse, …).

**Local steps**

- Set work\_order from Platform.get\_doc(“Work Order”, work\_order).
- Evaluate work\_order.check\_permission(“read”).
- Set pending\_qty\_to\_produce from (flt(work\_order.qty) − flt(work\_order.produced\_qty)).
- Return mapping(“from\_bom” → 1, “bom\_no” → work\_order.bom\_no, “use\_multi\_level\_bom” → work\_order.use\_multi\_level\_bom, “wip\_warehouse” → work\_order.wip\_warehouse, …).

**Values supplied outside this operation** effective access from work\_order.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1157) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L761)

<a id="op-b34a40bf0c5e84"></a>
### Get consumed operating cost

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_get_consumed_operating_cost`

**Inputs** wo\_name, bom\_no, operation\_id.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set table from Platform.qb.DocType(“Stock Entry”).
- Set child\_table from Platform.qb.DocType(“Landed Cost Taxes and Charges”).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“consumed\_cost”), nested operand in the contract.as\_(“consumed\_qty”), child\_table.operating\_componen ….
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0839.json#L1047) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1151) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L755)

<a id="op-1a2f74db7a49b5"></a>
### Uses sub assembly operating cost

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_uses_sub_assembly_operating_cost`

**Inputs** work\_order, bom\_no.

**Record and data access** read “Manufacturing Settings” via get\_single\_value · read “Work Order” via get\_cached\_value.

**Explicit results** bool((bom\_no and Platform.db.get\_single\_value(“Manufacturing Settings”, “set\_op\_cost\_and\_secondary\_items\_from\_sub\_assemblies”) and Platform.get\_cached\_value(“Work Order”, work\_order.name, “use\_multi\_level\_bom”))).

**Local steps**

- Return bool((bom\_no and Platform.db.get\_single\_value(“Manufacturing Settings”, “set\_op\_cost\_and\_secondary\_items\_from\_sub\_assemblies”) and Platform.get\_cached\_value(“Work Order”, work\_order.name, “use\_multi\_level\_bom”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bom\_no → Platform.db.get\_single\_value(“Manufacturing Settings”, “set\_op\_cost\_and\_secondary\_items\_from\_sub\_assemblies”) → Platform.get\_cached\_value(“Work Order”, work\_order.name, “use\_multi\_level\_bom”).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “set\_op\_cost\_and\_secondary\_items\_from\_sub\_assemblies”), Platform.get\_cached\_value(“Work Order”, work\_order.name, “use\_multi\_level\_bom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1286) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L783)

<a id="op-74efdad0152916"></a>
### Get remaining operating cost

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_get_remaining_operating_cost`

**Inputs** work\_order = no value, bom\_no = no value.

**Record and data access** read “BOM” via get\_value.

**Explicit results** get\_op\_cost\_from\_sub\_assemblies(bom\_no) · remaining\_operating\_cost.

**Local steps**

- Set remaining\_operating\_cost from 0.
- If work\_order.
  - If uses\_sub\_assembly\_operating\_cost(work\_order, bom\_no).
    - Return get\_op\_cost\_from\_sub\_assemblies(bom\_no).
  - If not bom\_no.
    - Set bom\_no from work\_order.bom\_no.
  - For each d in work\_order.get(“operations”).
    - Set consumed\_op\_cost from (get\_consumed\_operating\_cost(work\_order.name, bom\_no, d.name) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_consumed\_operating\_cost(work\_order.name, bom\_no, d.name) → list().
    - Set cost from 0.
    - For each row in consumed\_op\_cost.
      - Update cost using + flt(row.consumed\_cost).
    - If flt(d.completed\_qty).
      - Update remaining\_operating\_cost using + flt((d.actual\_operating\_cost − cost)).
    - Otherwise.
      - If work\_order.qty.
        - Update remaining\_operating\_cost using + (flt(d.planned\_operating\_cost) ÷ flt(work\_order.qty)).
- If (not remaining\_operating\_cost and bom\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not remaining\_operating\_cost → bom\_no.
  - Set bom from Platform.db.get\_value(“BOM”, bom\_no, list(“base\_operating\_cost”, “quantity”), as\_dict = 1).
  - If bom.quantity.
    - Set remaining\_operating\_cost from (flt(bom.base\_operating\_cost) ÷ flt(bom.quantity)).
- Return remaining\_operating\_cost.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1153) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L757)

<a id="op-423acd8792ef92"></a>
### Get used alternative items

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_get_used_alternative_items`

**Inputs** subcontract\_order = no value, subcontract\_order\_field = “subcontracting\_order”, work\_order = no value.

**State and service calls** execute a supplied database query.

**Explicit results** mapping() · used\_alternative\_items.

**Local steps**

- Set cond from empty text.
- If subcontract\_order.
  - Set cond from formatted text and ste.purpose = 'Send to Subcontractor' and ste.{subcontract\_order\_field} = '{subcontract\_order}'.
- Otherwise.
  - If work\_order.
    - Set cond from formatted text and ste.purpose = 'Material Transfer for Manufacture' and ste.work\_order = '{work\_order}'.
- If not cond.
  - Return mapping().
- Set used\_alternative\_items from mapping().
- Set data from Platform.db.sql(formatted text  select sted.original\_item, sted.uom, sted.conversion\_factor,  sted.item\_code, sted.item\_name, sted.conversion\_factor,sted.stock\_uom, sted.descripti, as\_dict = 1).
- For each d in data.
  - Set used\_alternative\_items at d.original\_item from d.
- Return used\_alternative\_items.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1155) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L759)

<a id="op-727fb0aa88348e"></a>
### Get bom stock qty by item

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_bom_stock_qty_by_item`

**Inputs** raw\_materials.

**Explicit results** stock\_qty\_by\_item.

**Local steps**

- Set stock\_qty\_by\_item from mapping().
- For each tuple(key, details) in raw\_materials.items().
  - Set item\_code from key at 0 when isinstance(key, tuple), otherwise key.
    - Value choice on isinstance(key, tuple) — true gives key at 0, false gives key.
  - Set stock\_qty from (flt(details.get(“qty”)) × (flt(details.get(“conversion\_factor”)) or 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(details.get(“conversion\_factor”)) → 1.
  - Set stock\_qty\_by\_item at item\_code from (stock\_qty\_by\_item.get(item\_code, 0.0) + stock\_qty).
- Return stock\_qty\_by\_item.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L632)

<a id="op-fca7efec79e45b"></a>
### Get alternative items for work order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_alternative_items_for_work_order`

**Inputs** work\_order, item\_codes, exclude\_stock\_entry = no value.

**Explicit results** mapping() · alternative\_items.

**Local steps**

- Set item\_codes from set((item\_codes or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_codes → list().
- If (not work\_order or not item\_codes).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not work\_order → not item\_codes.
  - Return mapping().
- Set ste from Platform.qb.DocType(“Stock Entry”).
- Set sted from Platform.qb.DocType(“Stock Entry Detail”).
- Set transfers from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- Set alternative\_items from mapping().
- For each row in transfers.
  - Set original\_item from (row.original\_item or row.item\_code).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.original\_item → row.item\_code.
  - If original\_item does not belong to item\_codes.
    - Continue with the next iteration or loop test.
  - Evaluate alternative\_items.setdefault(original\_item, list()).append(Platform.\_dict(item\_code = row.item\_code, item\_name = row.item\_name, description = row.description, stock\_uom = row.stock\_uom, …)).
    - Value choice on original\_item differs from row.item\_code — true gives original\_item, false gives no value.
- Set alternative\_items from mapping of original\_item → materials for tuple(original\_item, materials) drawn from alternative\_items.items() where any(generator of d.original\_item for d drawn from materials).
  - Draw tuple(original\_item, materials) from alternative\_items.items(), keep a combination only if (any(generator of d.original\_item for d drawn from materials)).
  - Draw d from materials.
- If not alternative\_items.
  - Return mapping().
- Set materials from mapping of tuple(d.item\_code, original\_item) → d for tuple(original\_item, rows) drawn from alternative\_items.items(), then d drawn from rows.
  - Draw tuple(original\_item, rows) from alternative\_items.items().
  - Draw d from rows.
- Set query from nested operand in the contract(nested operand in the contract).select(sted.item\_code, sted.original\_item, nested operand in the contract.as\_(“qty”)).where(((((nested operand in the contract bitwise and nes ….
  - Draw key from materials.
- If exclude\_stock\_entry.
  - Set query from query.where(ste.name differs from exclude\_stock\_entry).
- For each row in query.run(as\_dict = 1).
  - If material bound to materials.get(tuple(row.item\_code, (row.original\_item or row.item\_code))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.original\_item → row.item\_code.
    - Update material.available\_qty using − flt(row.qty).
- Return alternative\_items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L628)

<a id="op-29f90e83bb6f42"></a>
### Split qty by alternative items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_split_qty_by_alternative_items`

**Inputs** qty, materials.

**Explicit results** list() · split.

**Local steps**

- Set available from list of max(flt(d.available\_qty), 0.0) for d drawn from materials.
  - Draw d from materials.
- If not sum(available).
  - Set available from list of max(flt(d.transferred\_qty), 0.0) for d drawn from materials.
    - Draw d from materials.
- Set total from sum(available).
- If not total.
  - Return list().
- Set precision from Platform.get\_precision(“Stock Entry Detail”, “qty”).
- Set pending\_qty from flt(qty).
- Set last\_idx from max(generator of idx for tuple(idx, material\_qty) drawn from enumerate(available) where material\_qty).
  - Draw tuple(idx, material\_qty) from enumerate(available), keep a combination only if (material\_qty).
- Set split from list().
- For each tuple(idx, material) in enumerate(materials).
  - If not available at idx.
    - Continue with the next iteration or loop test.
  - Set material\_qty from pending\_qty when idx equals last\_idx, otherwise min(flt(((flt(qty) × available at idx) ÷ total), precision), pending\_qty).
    - Value choice on idx equals last\_idx — true gives pending\_qty, false gives min(flt(((flt(qty) × available at idx) ÷ total), precision), pending\_qty).
  - Update pending\_qty using − material\_qty.
  - If flt(material\_qty, precision) &gt; 0.
    - Evaluate split.append(tuple(material, flt(material\_qty, precision))).
- Return split.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1169) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L666)
