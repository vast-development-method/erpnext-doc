# Subcontracting · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Subcontracting inward order

[Record definition](../../../../data/record-types/subcontracting_inward_order.json)

<a id="op-43462398a7cf44"></a>
### Subcontracting Inward Order.on cancel

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_status().
- Evaluate self.update\_subcontracted\_quantity\_in\_so().
- Evaluate cancel\_stock\_reservation\_entries(voucher\_type = self.doctype, voucher\_no = self.name, notify = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status](operations-002.md#op-05b7f44912f36b), [update subcontracted quantity in so](operations-002.md#op-025fa8a844a662).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1445) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L941)

<a id="op-05b7f44912f36b"></a>
### Subcontracting Inward Order.update status

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_update_status`

**Inputs** self, status = no value, update\_modified = true.

**State and service calls** call db\_set on self.

**Local steps**

- If (self.status equals “Closed” and self.status differs from status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Closed” → self.status differs from status.
  - Evaluate check\_on\_hold\_or\_closed\_status(“Sales Order”, self.sales\_order).
- Set total\_to\_be\_received, total\_received, total\_rm\_returned from 0.
- For each rm in self.get(“received\_items”).
  - If rm.get(“is\_customer\_provided\_item”).
    - Update total\_to\_be\_received using + flt(rm.required\_qty).
    - Update total\_received using + flt(rm.received\_qty).
    - Update total\_rm\_returned using + flt(rm.returned\_qty).
- Set total\_to\_be\_produced, total\_produced, total\_process\_loss, total\_delivered, total\_fg\_returned from 0.
- For each item in self.get(“items”).
  - Update total\_to\_be\_produced using + flt(item.qty).
  - Update total\_produced using + flt(item.produced\_qty).
  - Update total\_process\_loss using + flt(item.process\_loss\_qty).
  - Update total\_delivered using + flt(item.delivered\_qty).
  - Update total\_fg\_returned using + flt(item.returned\_qty).
- Set per\_raw\_material\_received from flt(((total\_received ÷ total\_to\_be\_received) × 100), 2).
- Set per\_raw\_material\_returned from flt(((total\_rm\_returned ÷ total\_received) × 100), 2) when total\_received, otherwise 0.
  - Value choice on total\_received — true gives flt(((total\_rm\_returned ÷ total\_received) × 100), 2), false gives 0.
- Set per\_produced from flt(((total\_produced ÷ total\_to\_be\_produced) × 100), 2).
- Set per\_process\_loss from flt(((total\_process\_loss ÷ total\_produced) × 100), 2) when total\_produced, otherwise 0.
  - Value choice on total\_produced — true gives flt(((total\_process\_loss ÷ total\_produced) × 100), 2), false gives 0.
- Set per\_delivered from flt(((total\_delivered ÷ total\_to\_be\_produced) × 100), 2).
- Set per\_returned from flt(((total\_fg\_returned ÷ total\_delivered) × 100), 2) when total\_delivered, otherwise 0.
  - Value choice on total\_delivered — true gives flt(((total\_fg\_returned ÷ total\_delivered) × 100), 2), false gives 0.
- Evaluate self.db\_set(“per\_raw\_material\_received”, per\_raw\_material\_received, update\_modified = update\_modified).
- Evaluate self.db\_set(“per\_raw\_material\_returned”, per\_raw\_material\_returned, update\_modified = update\_modified).
- Evaluate self.db\_set(“per\_produced”, per\_produced, update\_modified = update\_modified).
- Evaluate self.db\_set(“per\_process\_loss”, per\_process\_loss, update\_modified = update\_modified).
- Evaluate self.db\_set(“per\_delivered”, per\_delivered, update\_modified = update\_modified).
- Evaluate self.db\_set(“per\_returned”, per\_returned, update\_modified = update\_modified).
- If (self.docstatus ≥ 1 and not status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus ≥ 1 → not status.
  - If self.docstatus equals 1.
    - If self.status equals “Draft”.
      - Set status from “Open”.
    - Otherwise.
      - If self.per\_returned equals 100.
        - Set status from “Returned”.
      - Otherwise.
        - If self.per\_delivered equals 100.
          - Set status from “Delivered”.
        - Otherwise.
          - If self.per\_produced equals 100.
            - Set status from “Produced”.
          - Otherwise.
            - If self.per\_raw\_material\_received &gt; 0.
              - Set status from “Ongoing”.
            - Otherwise.
              - Set status from “Open”.
  - Otherwise.
    - If self.docstatus equals 2.
      - Set status from “Cancelled”.
- If (status and self.status differs from status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status → self.status differs from status.
  - Evaluate self.db\_set(“status”, status, update\_modified = update\_modified).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0949.json#L3690) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1450) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L946)

<a id="op-025fa8a844a662"></a>
### Subcontracting Inward Order.update subcontracted quantity in so

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_update_subcontracted_quantity_in_sales_order`

**Inputs** self.

**Record and data access** resolve a document from “Sales Order Item” via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- For each service\_item in self.service\_items.
  - Set doc from Platform.get\_doc(“Sales Order Item”, service\_item.sales\_order\_item).
  - Set doc.subcontracted\_qty from (doc.subcontracted\_qty + service\_item.qty) when self.\_action equals “submit”, otherwise (doc.subcontracted\_qty − service\_item.qty).
    - Value choice on self.\_action equals “submit” — true gives (doc.subcontracted\_qty + service\_item.qty), false gives (doc.subcontracted\_qty − service\_item.qty).
  - Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0949.json#L5152) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1451) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L947)

<a id="op-15bbf2facdbdc9"></a>
### Subcontracting Inward Order.validate customer warehouse

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_validate_customer_warehouse`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Customer Warehouse {0} does not belong to Customer {1}.”.format(Platform.bold(self.customer\_warehouse), Platform.bold(self.customer)).

**Local steps**

- If Platform.get\_cached\_value(“Warehouse”, self.customer\_warehouse, “customer”) differs from self.customer.
  - Call the validation error handler Platform.throw(translated “Customer Warehouse {0} does not belong to Customer {1}.”.format(Platform.bold(self.customer\_warehouse), Platform.bold(self.customer))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, self.customer\_warehouse, “customer”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0949.json#L5355) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L950)

<a id="op-1d6163c91d4b4d"></a>
### Subcontracting Inward Order.validate service items

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_validate_service_items`

**Inputs** self.

**Local steps**

- Set sales\_order\_items from list of item.sales\_order\_item for item drawn from self.items.
  - Draw item from self.items.
- Set self.service\_items from list of service\_item for service\_item drawn from self.service\_items where service\_item.sales\_order\_item belongs to sales\_order\_items.
  - Draw service\_item from self.service\_items, keep a combination only if (service\_item.sales\_order\_item belongs to sales\_order\_items).
- For each service\_item in self.service\_items.
  - Set item from next(generator of item for item drawn from self.items where item.sales\_order\_item equals service\_item.sales\_order\_item).
    - Draw item from self.items, keep a combination only if (item.sales\_order\_item equals service\_item.sales\_order\_item).
  - Set service\_item.qty from (item.qty × item.subcontracting\_conversion\_factor).
  - Set service\_item.fg\_item\_qty from item.qty.
  - Set service\_item.amount from (service\_item.qty × service\_item.rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0949.json#L5553) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L951)

<a id="op-1b361aaea90d6d"></a>
### Subcontracting Inward Order.populate items table

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_populate_items_table`

**Inputs** self.

**Record and data access** resolve a document from “Item” via get\_doc · resolve a document from “Sales Order Item” via get\_doc · read “Sales Order Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Please select Finished Good Item for Service Item {0}”.format((si.item\_name or si.item\_code)).

**Local steps**

- Set items from list().
- For each si in self.service\_items.
  - If si.fg\_item.
    - Set item from Platform.get\_doc(“Item”, si.fg\_item).
    - Set so\_item from Platform.get\_doc(“Sales Order Item”, si.sales\_order\_item).
    - Set available\_qty from (so\_item.stock\_qty − so\_item.subcontracted\_qty).
    - <a id="op-1b361aaea90d6d-guard-11"></a>If available\_qty equals 0.
      - Continue with the next iteration or loop test.
    - Set si.required\_qty from available\_qty.
    - Set conversion\_factor from (so\_item.stock\_qty ÷ so\_item.fg\_item\_qty).
    - Set si.fg\_item\_qty from flt((available\_qty ÷ conversion\_factor), Platform.get\_precision(“Sales Order Item”, “qty”)).
    - Set si.amount from (available\_qty × si.rate).
    - Evaluate items.append(mapping(“item\_code” → item.name, “item\_name” → item.item\_name, “expected\_delivery\_date” → Platform.get\_cached\_value(“Sales Order Item”, si.sales\_order\_item, “delivery\_date”), “description” → i ….
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Please select Finished Good Item for Service Item {0}”.format((si.item\_name or si.item\_code))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in si.item\_name → si.item\_code.
- If items.
  - For each item in items.
    - Evaluate self.append(“items”, item).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison available\_qty equals 0, available\_qty = 0 selects the branch that continues with the next loop iteration. With available\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-1b361aaea90d6d-guard-11)

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Sales Order Item”, si.sales\_order\_item, “delivery\_date”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1447) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L943)

<a id="op-3076c4bd05e6ab"></a>
### Subcontracting Inward Order.validate customer provided items

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_validate_customer_provided_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Atleast one raw material for Finished Good Item {0} should be customer provided.”.format(Platform.bold(item.item\_code)).

**Local steps**

- For each item in self.get(“items”).
  - Set raw\_materials from list of rm for rm drawn from self.get(“received\_items”) where rm.main\_item\_code equals item.item\_code.
    - Draw rm from self.get(“received\_items”), keep a combination only if (rm.main\_item\_code equals item.item\_code).
  - If not any(list of rm.is\_customer\_provided\_item for rm drawn from raw\_materials).
    - Draw rm from raw\_materials.
    - Call the validation error handler Platform.throw(translated “Atleast one raw material for Finished Good Item {0} should be customer provided.”.format(Platform.bold(item.item\_code))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L949)

<a id="op-b2c6c1f744356c"></a>
### Subcontracting Inward Order.set is customer provided item

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_set_is_customer_provided_item`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- For each item in self.get(“received\_items”).
  - Set item.is\_customer\_provided\_item from Platform.get\_cached\_value(“Item”, item.rm\_item\_code, “is\_customer\_provided\_item”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.rm\_item\_code, “is\_customer\_provided\_item”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0949.json#L6996) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1448) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L944)

<a id="op-28ec27fb3ac016"></a>
### Subcontracting Inward Order.make work order

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_make_work_order`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “No Work Orders were created”.

**Explicit results** wo\_list.

**Local steps**

- Set wo\_list from list().
- For each item in self.get\_production\_items().
  - Set work\_order from self.create\_work\_order(item).
  - If work\_order.
    - Evaluate wo\_list.append(work\_order).
- Evaluate self.show\_list\_created\_message(“Work Order”, wo\_list).
- If not wo\_list.
  - Evaluate Platform.msgprint(translated “No Work Orders were created”).
- Return wo\_list.

**Methods declared on this owner** [get production items](operations-002.md#op-689de06ec00ae8), [create work order](operations-002.md#op-0ba9bb72c9f69c), [show list created message](operations-002.md#op-1ce65e12f1b592).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0950.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1444) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L940)

<a id="op-689de06ec00ae8"></a>
### Subcontracting Inward Order.get production items

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_get_production_items`

**Inputs** self.

**Record and data access** read “Sales Order” via get\_cached\_value · read “UOM” via get\_cached\_value.

**Explicit results** item\_list.

**Local steps**

- Set item\_list from list().
- Set pending\_qty from self.get\_pending\_work\_order\_qty().
- For each d in self.items.
  - If d.produced\_qty ≥ d.qty.
    - Continue with the next iteration or loop test.
  - Set item\_details from mapping(“production\_item” → d.item\_code, “use\_multi\_level\_bom” → d.include\_exploded\_items, “subcontracting\_inward\_order” → self.name, “bom\_no” → d.bom, …).
  - Set qty from min(list of flt((((nested operand in the contract.received\_qty − nested operand in the contract.returned\_qty) − item.work\_order\_qty) ÷ flt((nested operand in the contract.required\_qty ÷ nested operand in the c …).
    - Draw item from self.get(“received\_items”), keep a combination only if ((item.reference\_name equals d.name and item.is\_customer\_provided\_item and item.required\_qty)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.reference\_name equals d.name → item.is\_customer\_provided\_item → item.required\_qty.
  - Set qty from min(int(qty) when Platform.get\_cached\_value(“UOM”, d.stock\_uom, “must\_be\_whole\_number”), otherwise qty, ((d.qty − d.produced\_qty) − flt(pending\_qty.get(d.name)))).
    - Value choice on Platform.get\_cached\_value(“UOM”, d.stock\_uom, “must\_be\_whole\_number”) — true gives int(qty), false gives qty.
  - Evaluate item\_details.update(mapping(“qty” → qty, “max\_producible\_qty” → qty)).
  - Evaluate item\_list.append(item\_details).
- Return item\_list.

**Methods declared on this owner** [get pending work order qty](operations-002.md#op-afea69488fae58).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Sales Order”, self.sales\_order, “project”), Platform.get\_cached\_value(“UOM”, d.stock\_uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L930)

<a id="op-afea69488fae58"></a>
### Subcontracting Inward Order.get pending work order qty

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_inward_order_subcontracting_inward_order_subcontractinginwardorder_get_pending_work_order_qty`

**Inputs** self.

**Explicit results** Platform.\_dict(query.run()).

**Local steps**

- Set wo from Platform.qb.DocType(“Work Order”).
- Set query from nested operand in the contract(nested operand in the contract).select(wo.subcontracting\_inward\_order\_item, Sum((nested operand in the contract − nested operand in the contract))).where(((nested operand in  ….
- Return Platform.\_dict(query.run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L194) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1184)

<a id="op-0ba9bb72c9f69c"></a>
### Subcontracting Inward Order.create work order

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_create_work_order`

**Inputs** self, item.

**State and service calls** request new\_doc for “Work Order” · call insert on wo.

**Explicit results** no value · wo.name.

**Local steps**

- Bind dependencies OverProductionError.
- If flt(item.get(“qty”)) ≤ 0.
  - Return no value.
- Set wo from Platform.new\_doc(“Work Order”).
- Evaluate wo.update(item).
- Evaluate wo.set\_work\_order\_operations().
- Evaluate wo.set\_required\_items().
- Attempt the following.
  - Set wo.flags.ignore\_mandatory from true.
  - Set wo.flags.ignore\_validate from true.
  - Evaluate wo.insert().
  - Return wo.name.
- On failure (OverProductionError).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0950.json#L1064) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1433) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L929)

<a id="op-1ce65e12f1b592"></a>
### Subcontracting Inward Order.show list created message

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_show_list_created_message`

**Inputs** self, doctype, doc\_list = no value.

**State and service calls** msgprint with translated “{0} created”.format(comma\_and(doc\_list)).

**Explicit results** no value.

**Local steps**

- If not doc\_list.
  - Return no value.
- Set Platform.flags.mute\_messages from false.
- If doc\_list.
  - Set doc\_list from list of get\_link\_to\_form(doctype, p) for p drawn from doc\_list.
    - Draw p from doc\_list.
  - Evaluate Platform.msgprint(translated “{0} created”.format(comma\_and(doc\_list))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0950.json#L1362) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1449) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L945)

<a id="op-6033833aa232fc"></a>
### Subcontracting Inward Order.make rm stock entry inward

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_make_raw_material_stock_entry_inward`

**Inputs** self, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** stock\_entry · stock\_entry.as\_dict().

**Local steps**

- Bind local operation calculate\_qty\_as\_per\_bom for subsequent calls.
- If (target\_doc and target\_doc.get(“items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in target\_doc → target\_doc.get(“items”).
  - Set target\_doc.items from list().
- Bind local operation postprocess for subsequent calls.
- Set stock\_entry from get\_mapped\_doc(“Subcontracting Inward Order”, self.name, mapping(“Subcontracting Inward Order” → mapping(“doctype” → “Stock Entry”, “validation” → mapping(“docstatus” → list(“=”, 1)))), target\_doc, postpro ….
- If target\_doc.
  - Return stock\_entry.
- Otherwise.
  - Return stock\_entry.as\_dict().

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1437) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L933)

<a id="op-19d056ed368e42"></a>
### Subcontracting Inward Order.make rm stock entry inward.calculate qty as per bom

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_make_raw_material_stock_entry_inward_calculate_quantity_as_per_bill_of_materials`

**Inputs** rm\_item.

**Record and data access** read “Subcontracting Inward Order Item” via get\_value · read “BOM Explosion Item” when data.include\_exploded\_items, otherwise “BOM Item” via get\_value.

**Explicit results** (((rm\_item.required\_qty − rm\_item.received\_qty) + rm\_item.returned\_qty) + qty).

**Local steps**

- Set data from Platform.get\_value(“Subcontracting Inward Order Item”, mapping(“name” → rm\_item.reference\_name), list(“process\_loss\_qty”, “include\_exploded\_items”), as\_dict = true).
- Set qty\_consumed\_per\_unit from Platform.get\_value(“BOM Explosion Item” when data.include\_exploded\_items, otherwise “BOM Item”, mapping(“name” → rm\_item.bom\_detail\_no), “qty\_consumed\_per\_unit”).
  - Value choice on data.include\_exploded\_items — true gives “BOM Explosion Item”, false gives “BOM Item”.
- Set qty from flt((qty\_consumed\_per\_unit × data.process\_loss\_qty), Platform.get\_precision(“Subcontracting Inward Order Received Item”, “required\_qty”)).
- Return (((rm\_item.required\_qty − rm\_item.received\_qty) + rm\_item.returned\_qty) + qty).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1438) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L934)

<a id="op-86fe70659cb118"></a>
### Subcontracting Inward Order.make rm stock entry inward.postprocess

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_make_raw_material_stock_entry_inward_postprocess`

**Inputs** source, target.

**Local steps**

- Set target.purpose from “Receive from Customer”.
- Set target.subcontracting\_inward\_order from source.name.
- Evaluate target.set\_stock\_entry\_type().
- For each rm\_item in source.received\_items.
  - If (not rm\_item.required\_qty or not rm\_item.is\_customer\_provided\_item).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not rm\_item.required\_qty → not rm\_item.is\_customer\_provided\_item.
    - Continue with the next iteration or loop test.
  - Evaluate target.append(“items”, mapping(“scio\_detail” → rm\_item.get(“name”), “item\_code” → rm\_item.get(“rm\_item\_code”), “qty” → calculate\_qty\_as\_per\_bom(rm\_item), “t\_warehouse” → rm\_item.get(“warehouse”), …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0950.json#L2899) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1439) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L935)

<a id="op-02eb36af6e86fe"></a>
### Subcontracting Inward Order.make rm return

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_make_raw_material_return`

**Inputs** self, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** stock\_entry · stock\_entry.as\_dict().

**Local steps**

- If (target\_doc and target\_doc.get(“items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in target\_doc → target\_doc.get(“items”).
  - Set target\_doc.items from list().
- Bind local operation postprocess for subsequent calls.
- Set stock\_entry from get\_mapped\_doc(“Subcontracting Inward Order”, self.name, mapping(“Subcontracting Inward Order” → mapping(“doctype” → “Stock Entry”, “validation” → mapping(“docstatus” → list(“=”, 1)))), target\_doc, postpro ….
- If target\_doc.
  - Return stock\_entry.
- Otherwise.
  - Return stock\_entry.as\_dict().

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1435) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L931)

<a id="op-df099604eb79f6"></a>
### Subcontracting Inward Order.make rm return.postprocess

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_make_raw_material_return_postprocess`

**Inputs** source, target.

**Local steps**

- Set target.purpose from “Return Raw Material to Customer”.
- Set target.subcontracting\_inward\_order from source.name.
- Evaluate target.set\_stock\_entry\_type().
- For each rm\_item in source.received\_items.
  - Set qty from ((rm\_item.received\_qty − rm\_item.work\_order\_qty) − rm\_item.returned\_qty).
  - If (not rm\_item.is\_customer\_provided\_item or qty ≤ 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not rm\_item.is\_customer\_provided\_item → qty ≤ 0.
    - Continue with the next iteration or loop test.
  - Evaluate target.append(“items”, mapping(“scio\_detail” → rm\_item.get(“name”), “item\_code” → rm\_item.get(“rm\_item\_code”), “qty” → qty, “s\_warehouse” → rm\_item.get(“warehouse”), …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L932)

<a id="op-27ce296aa73c28"></a>
### Subcontracting Inward Order.make subcontracting delivery

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_make_subcontracting_delivery`

**Inputs** self, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** stock\_entry · stock\_entry.as\_dict().

**Local steps**

- If (target\_doc and target\_doc.get(“items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in target\_doc → target\_doc.get(“items”).
  - Set target\_doc.items from list().
- Bind local operation postprocess for subsequent calls.
- Set stock\_entry from get\_mapped\_doc(“Subcontracting Inward Order”, self.name, mapping(“Subcontracting Inward Order” → mapping(“doctype” → “Stock Entry”, “validation” → mapping(“docstatus” → list(“=”, 1)))), target\_doc, postpro ….
- If target\_doc.
  - Return stock\_entry.
- Otherwise.
  - Return stock\_entry.as\_dict().

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1440) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L936)

<a id="op-ed5c0ab3549a2b"></a>
### Subcontracting Inward Order.make subcontracting delivery.postprocess

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_make_subcontracting_delivery_postprocess`

**Inputs** source, target.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Local steps**

- Set target.purpose from “Subcontracting Delivery”.
- Set target.subcontracting\_inward\_order from source.name.
- Evaluate target.set\_stock\_entry\_type().
- Set scio\_details from list().
- Set allow\_over from Platform.get\_single\_value(“Selling Settings”, “allow\_delivery\_of\_overproduced\_qty”).
- For each fg\_item in source.items.
  - Set qty from (fg\_item.produced\_qty when allow\_over, otherwise min(fg\_item.qty, fg\_item.produced\_qty) − fg\_item.delivered\_qty).
    - Value choice on allow\_over — true gives fg\_item.produced\_qty, false gives min(fg\_item.qty, fg\_item.produced\_qty).
  - <a id="op-ed5c0ab3549a2b-guard-12"></a>If qty &lt; 0.
    - Continue with the next iteration or loop test.
  - Evaluate scio\_details.append(fg\_item.name).
  - If qty &gt; 0.
    - Evaluate target.append(“items”, mapping(“qty” → qty, “item\_code” → fg\_item.item\_code, “s\_warehouse” → fg\_item.delivery\_warehouse, “stock\_uom” → fg\_item.stock\_uom, …)).
- If (Platform.get\_single\_value(“Selling Settings”, “deliver\_secondary\_items”) and source.secondary\_items and scio\_details).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_single\_value(“Selling Settings”, “deliver\_secondary\_items”) → source.secondary\_items → scio\_details.
  - For each secondary\_item in source.secondary\_items.
    - If secondary\_item.reference\_name does not belong to scio\_details.
      - Continue with the next iteration or loop test.
    - Set qty from (secondary\_item.produced\_qty − secondary\_item.delivered\_qty).
    - If qty &gt; 0.
      - Evaluate target.append(“items”, mapping(“qty” → qty, “item\_code” → secondary\_item.item\_code, “s\_warehouse” → secondary\_item.warehouse, “stock\_uom” → secondary\_item.stock\_uom, …)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison qty &lt; 0, qty = -1 selects the branch that continues with the next loop iteration. With qty = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-ed5c0ab3549a2b-guard-12)

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “allow\_delivery\_of\_overproduced\_qty”), Platform.get\_single\_value(“Selling Settings”, “deliver\_secondary\_items”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1441) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L937)

<a id="op-61d5984da00c02"></a>
### Subcontracting Inward Order.make subcontracting return

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_make_subcontracting_return`

**Inputs** self, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** stock\_entry · stock\_entry.as\_dict().

**Local steps**

- If (target\_doc and target\_doc.get(“items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in target\_doc → target\_doc.get(“items”).
  - Set target\_doc.items from list().
- Bind local operation postprocess for subsequent calls.
- Set stock\_entry from get\_mapped\_doc(“Subcontracting Inward Order”, self.name, mapping(“Subcontracting Inward Order” → mapping(“doctype” → “Stock Entry”, “validation” → mapping(“docstatus” → list(“=”, 1)), “field\_map” → mapping ….
- If target\_doc.
  - Return stock\_entry.
- Otherwise.
  - Return stock\_entry.as\_dict().

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1442) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L938)

<a id="op-197c843a518336"></a>
### Subcontracting Inward Order.make subcontracting return.postprocess

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_make_subcontracting_return_postprocess`

**Inputs** source, target.

**Local steps**

- Set target.purpose from “Subcontracting Return”.
- Evaluate target.set\_stock\_entry\_type().
- For each fg\_item in source.items.
  - Set qty from (fg\_item.delivered\_qty − fg\_item.returned\_qty).
  - <a id="op-197c843a518336-guard-7"></a>If qty ≤ 0.
    - Continue with the next iteration or loop test.
  - Evaluate target.append(“items”, mapping(“qty” → qty, “item\_code” → fg\_item.item\_code, “stock\_uom” → fg\_item.stock\_uom, “scio\_detail” → fg\_item.name, …)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison qty ≤ 0, qty = 0 selects the branch that continues with the next loop iteration. With qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-197c843a518336-guard-7)

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1443) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L939)

<a id="op-5a8effb383fd05"></a>
### Set subcontracting inward order status

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_set_subcontracting_inward_order_status`

**Inputs** scio, status = no value.

**Record and data access** resolve a document from “Subcontracting Inward Order” via get\_doc.

**Local steps**

- If isinstance(scio, str).
  - Set scio from Platform.get\_doc(“Subcontracting Inward Order”, scio).
- Evaluate scio.update\_status(status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0951.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L928)

<a id="op-8df058cc02fd84"></a>
### Update subcontracting inward order status

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_update_subcontracting_inward_order_status`

**Inputs** scio, status = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Subcontracting Inward Order” via get\_doc.

**Explicit failure paths** validation helper — translated “Only a submitted Subcontracting Inward Order can be closed or re-opened.” · validation helper — translated “Status {0} cannot be set manually.”.format(Platform.bold(status)).

**Local steps**

- If isinstance(scio, str).
  - Set scio from Platform.get\_doc(“Subcontracting Inward Order”, scio).
- Evaluate scio.check\_permission(“write”).
- <a id="op-8df058cc02fd84-guard-7"></a>If scio.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Only a submitted Subcontracting Inward Order can be closed or re-opened.”).
- If (status and status differs from “Closed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status → status differs from “Closed”.
  - Call the validation error handler Platform.throw(translated “Status {0} cannot be set manually.”.format(Platform.bold(status))).
- Evaluate set\_subcontracting\_inward\_order\_status(scio, status).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison scio.docstatus differs from 1, scio.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Only a submitted Subcontracting Inward Order can be closed or re-opened.”. With scio.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-8df058cc02fd84-guard-7)

**Values supplied outside this operation** effective access from scio.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L952)
