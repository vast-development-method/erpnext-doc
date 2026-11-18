# Production · operations 32

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Production plan

[Record definition](../../../../data/record-types/production_plan.json)

<a id="op-8c7038bd1db380"></a>
### Production Plan.update ordered status

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_update_ordered_status`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- For each child\_table in list(“po\_items”, “sub\_assembly\_items”).
  - For each item in self.get(child\_table).
    - If item.ordered\_qty.
      - Set self.status from “In Process”.
      - Return no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0487.json#L3565) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L980) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L609)

<a id="op-0bdffa0df7362d"></a>
### Production Plan.update requested status

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_update_requested_status`

**Inputs** self.

**Local steps**

- If (self.mr\_items and all(generator of flt(d.requested\_qty) ≥ flt(d.quantity) for d drawn from self.mr\_items)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.mr\_items → all(generator of flt(d.requested\_qty) ≥ flt(d.quantity) for d drawn from self.mr\_items).
  - Draw d from self.mr\_items.
  - Set self.status from “Material Requested”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L982) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L611)

<a id="op-f536ece0e479eb"></a>
### Production Plan.get production items

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_get_production_items`

**Inputs** self.

**Record and data access** read “BOM” via get\_value · read “Sales Order” via get\_cached\_value.

**Explicit results** item\_dict.

**Local steps**

- Set item\_dict from mapping().
- Set pending from ProductionPlanWorkOrderQuantities(self.name).get\_pending\_quantities(self).
- For each d in self.po\_items.
  - Set item\_details from mapping(“production\_item” → d.item\_code, “use\_multi\_level\_bom” → d.include\_exploded\_items, “sales\_order” → d.sales\_order, “sales\_order\_item” → d.sales\_order\_item, …).
  - If (not item\_details at “project” and d.sales\_order).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item\_details at “project” → d.sales\_order.
    - Set item\_details at “project” from Platform.get\_cached\_value(“Sales Order”, d.sales\_order, “project”).
  - Set item\_details at “qty” from pending at “production\_plan\_item” at d.name.
  - Set item\_dict at d.name from item\_details.
- Return item\_dict.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Sales Order”, d.sales\_order, “project”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L958) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L587)

<a id="op-68804ca129d175"></a>
### Production Plan.make work order

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_make_work_order`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “No Work Orders were created” · msgprint with translated “No Purchase Orders were created”.

**Local steps**

- Bind dependencies get\_default\_warehouse.
- Evaluate self.validate\_plan\_is\_open().
- Evaluate self.reload().
- Set tuple(wo\_list, po\_list) from tuple(list(), list()).
- Set subcontracted\_po from mapping().
- Set default\_warehouses from get\_default\_warehouse(self.company).
- Evaluate self.make\_work\_order\_for\_finished\_goods(wo\_list, default\_warehouses).
- Evaluate self.make\_work\_order\_for\_subassembly\_items(wo\_list, subcontracted\_po, default\_warehouses).
- Evaluate self.make\_subcontracted\_purchase\_order(subcontracted\_po, po\_list).
- Evaluate self.show\_list\_created\_message(“Work Order”, wo\_list).
- Evaluate self.show\_list\_created\_message(“Purchase Order”, po\_list).
- If not wo\_list.
  - Evaluate Platform.msgprint(translated “No Work Orders were created”).
- If not po\_list.
  - Evaluate Platform.msgprint(translated “No Purchase Orders were created”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate plan is open](operations-032.md#op-52437660645a62), [make work order for finished goods](operations-032.md#op-42aff39803506a), [make work order for subassembly items](operations-032.md#op-db7651087514b1), [make subcontracted purchase order](operations-032.md#op-3d8bf77fdbb02c), [show list created message](operations-032.md#op-a061c6ec00e317).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L965) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L594)

<a id="op-52437660645a62"></a>
### Production Plan.validate plan is open

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_productionplan_validate_plan_is_open`

**Inputs** self.

**Record and data access** read “Production Plan” via get\_value.

**Explicit failure paths** validation helper with Platform.InvalidStatusError — translated “Production Plan {0} is {1}”.format(Platform.bold(self.name), translated status).

**Local steps**

- Set status from Platform.db.get\_value(“Production Plan”, self.name, “status”) when not self.is\_new(), otherwise self.status.
  - Value choice on not self.is\_new() — true gives Platform.db.get\_value(“Production Plan”, self.name, “status”), false gives self.status.
- If status belongs to tuple(“Closed”, “Completed”).
  - Call the validation error handler Platform.throw(translated “Production Plan {0} is {1}”.format(Platform.bold(self.name), translated status), Platform.InvalidStatusError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1714) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L954)

<a id="op-42aff39803506a"></a>
### Production Plan.make work order for finished goods

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_make_work_order_for_finished_goods`

**Inputs** self, wo\_list, default\_warehouses.

**Local steps**

- Set items\_data from self.get\_production\_items().
- For each tuple(\_key, item) in items\_data.items().
  - If self.sub\_assembly\_items.
    - Set item at “use\_multi\_level\_bom” from 0.
  - Evaluate set\_default\_warehouses(item, default\_warehouses).
  - Set work\_order from self.create\_work\_order(item).
  - If work\_order.
    - Evaluate wo\_list.append(work\_order).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get production items](operations-032.md#op-f536ece0e479eb), [create work order](operations-032.md#op-5b6724aa3ca14d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L966) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L595)

<a id="op-db7651087514b1"></a>
### Production Plan.make work order for subassembly items

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_make_work_order_for_subassembly_items`

**Inputs** self, wo\_list, subcontracted\_po, default\_warehouses.

**Record and data access** read “BOM” via get\_value.

**Local steps**

- Set pending from ProductionPlanWorkOrderQuantities(self.name).get\_pending\_quantities(self).
- For each row in self.sub\_assembly\_items.
  - If row.type\_of\_manufacturing equals “Subcontract”.
    - Set order\_qty from ProductionPlanWorkOrderQuantities.get\_order\_qty(row, “production\_plan\_sub\_assembly\_item”).
    - Evaluate subcontracted\_po.setdefault(row.supplier, list()).append(Platform.\_dict(row.as\_dict(), qty = order\_qty)).
    - Continue with the next iteration or loop test.
  - If row.type\_of\_manufacturing equals “Material Request”.
    - Continue with the next iteration or loop test.
  - Set work\_order\_data from mapping(“source\_warehouse” → Platform.get\_value(“BOM”, row.bom\_no, “default\_source\_warehouse”), “wip\_warehouse” → default\_warehouses.get(“wip\_warehouse”), “fg\_warehouse” → default\_warehouses.get(“fg\_wareho ….
  - Evaluate self.prepare\_data\_for\_sub\_assembly\_items(row, work\_order\_data, pending at “production\_plan\_sub\_assembly\_item” at row.name).
  - <a id="op-db7651087514b1-guard-28"></a>If work\_order\_data.get(“qty”) ≤ 0.
    - Continue with the next iteration or loop test.
  - Set work\_order from self.create\_work\_order(work\_order\_data).
  - If work\_order.
    - Evaluate wo\_list.append(work\_order).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison work\_order\_data.get(“qty”) ≤ 0, work\_order\_data.qty = 0 selects the branch that continues with the next loop iteration. With work\_order\_data.qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-db7651087514b1-guard-28)

**Methods declared on this owner** [prepare data for sub assembly items](operations-032.md#op-3e3bbf88cf5da7), [create work order](operations-032.md#op-5b6724aa3ca14d).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L967) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L596)

<a id="op-3e3bbf88cf5da7"></a>
### Production Plan.prepare data for sub assembly items

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_prepare_data_for_subordinate_assembly_items`

**Inputs** self, row, wo\_data, pending\_qty = no value.

**Local steps**

- For each field in list(“production\_item”, “item\_name”, “fg\_warehouse”, “description”, …).
  - If row.get(field).
    - Set wo\_data at field from row.get(field).
- If pending\_qty is identical to no value.
  - Set pending\_qty from ProductionPlanWorkOrderQuantities(self.name).get\_pending\_quantities(self) at “production\_plan\_sub\_assembly\_item” at row.name.
- Set wo\_data at “qty” from pending\_qty.
- Evaluate wo\_data.update(mapping(“use\_multi\_level\_bom” → 0, “production\_plan” → self.name, “production\_plan\_sub\_assembly\_item” → row.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L972) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L601)

<a id="op-f8518b623ab368"></a>
### Production Plan.get subcontracted qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_productionplan_get_subcontracted_qty`

**Inputs** self.

**Explicit results** Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(po\_item.production\_plan\_sub\_assembly\_item).run()).

**Local steps**

- Set po\_item from Platform.qb.DocType(“Purchase Order Item”).
- Return Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(po\_item.production\_plan\_sub\_assembly\_item).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1709) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L949)

<a id="op-3d8bf77fdbb02c"></a>
### Production Plan.make subcontracted purchase order

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_make_subcontracted_purchase_order`

**Inputs** self, subcontracted\_po, purchase\_orders.

**State and service calls** request new\_doc for “Purchase Order” · call insert on po.

**Explicit results** no value.

**Local steps**

- If not subcontracted\_po.
  - Return no value.
- Set subcontracted\_po from consolidate\_subcontracted\_po(subcontracted\_po, self.get\_subcontracted\_qty()).
- For each tuple(supplier, po\_list) in subcontracted\_po.items().
  - Set po from Platform.new\_doc(“Purchase Order”).
  - Set po.company from self.company.
  - Set po.supplier from supplier.
  - Set po.schedule\_date from getdate(po\_list at 0.schedule\_date) when po\_list at 0.schedule\_date, otherwise nowdate().
    - Value choice on po\_list at 0.schedule\_date — true gives getdate(po\_list at 0.schedule\_date), false gives nowdate().
  - Set po.is\_subcontracted from 1.
  - For each row in po\_list.
    - Set po\_data from mapping(“fg\_item” → row.production\_item, “warehouse” → row.fg\_warehouse, “production\_plan\_sub\_assembly\_item” → row.name, “bom” → row.bom\_no, …).
    - For each field in list(“schedule\_date”, “qty”, “description”, “production\_plan\_item”, …).
      - Set po\_data at field from row.get(field).
    - Evaluate po.append(“items”, po\_data).
  - Evaluate po.set\_service\_items\_for\_finished\_goods().
  - Evaluate po.set\_missing\_values().
  - Set po.flags.ignore\_mandatory from true.
  - Set po.flags.ignore\_validate from true.
  - Evaluate po.insert().
  - Evaluate purchase\_orders.append(po.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get subcontracted qty](operations-032.md#op-f8518b623ab368).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L964) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L593)

<a id="op-a061c6ec00e317"></a>
### Production Plan.show list created message

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_show_list_created_message`

**Inputs** self, doctype, doc\_list = no value.

**Explicit results** no value.

**Local steps**

- If not doc\_list.
  - Return no value.
- Set Platform.flags.mute\_messages from false.
- Evaluate msgprint(translated “{0} created”.format(get\_filtered\_list\_link(doctype, doc\_list))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L978) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L607)

<a id="op-5b6724aa3ca14d"></a>
### Production Plan.create work order

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_create_work_order`

**Inputs** self, item.

**State and service calls** request new\_doc for “Work Order” · call insert on wo.

**Explicit results** no value · wo.name.

**Local steps**

- Bind dependencies OverProductionError.
- If flt(item.get(“qty”)) ≤ 0.
  - Return no value.
- Set wo from Platform.new\_doc(“Work Order”).
- Evaluate wo.update(item).
- Set wo.reserve\_stock from self.reserve\_stock.
- Set wo.planned\_start\_date from (item.get(“planned\_start\_date”) or item.get(“schedule\_date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“planned\_start\_date”) → item.get(“schedule\_date”).
- If item.get(“warehouse”).
  - Set wo.fg\_warehouse from item.get(“warehouse”).
- Evaluate wo.set\_work\_order\_operations().
- Evaluate wo.set\_required\_items().
- Attempt the following.
  - Set wo.flags.ignore\_mandatory from true.
  - Set wo.flags.ignore\_validate from true.
  - Set wo.company from self.company.
  - Evaluate wo.insert().
  - Return wo.name.
- On failure (OverProductionError).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L948) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L579)

<a id="op-b7310538f66a8e"></a>
### Production Plan.validate mr subcontracted

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_validate_material_request_subcontracted`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Item {0} is not a subcontracted item”.format(row.item\_code).

**Local steps**

- For each row in self.mr\_items.
  - If row.material\_request\_type equals “Subcontracting”.
    - If not Platform.db.get\_value(“Item”, row.item\_code, “is\_sub\_contracted\_item”).
      - Call the validation error handler Platform.throw(translated “Item {0} is not a subcontracted item”.format(row.item\_code), title = translated “Invalid Item”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L987) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L616)

<a id="op-fa3b140e6773c9"></a>
### Production Plan.make material request

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_make_material_request`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Item” via get\_cached\_doc · read “Warehouse” via get\_cached\_value · read “Sales Order” via get\_value.

**State and service calls** request new\_doc for “Material Request” · call save on material\_request · call submit on material\_request.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot create Material Request for item {0} in group warehouse {1}.”.format(Platform.bold(item.item\_code), Platform.bold(item.warehouse)).

**Local steps**

- Evaluate self.load\_saved\_plan\_for\_material\_request().
- Evaluate self.validate\_mr\_subcontracted().
- Set material\_request\_list from list().
- Set material\_request\_map from mapping().
- Set draft\_qty from self.get\_draft\_requested\_qty().
- For each item in self.mr\_items.
  - Set qty\_to\_request from get\_qty\_to\_request(item, draft\_qty).
  - <a id="op-fa3b140e6773c9-guard-12"></a>If qty\_to\_request ≤ 0.
    - Continue with the next iteration or loop test.
  - Set item\_doc from Platform.get\_cached\_doc(“Item”, item.item\_code).
  - If (item.warehouse and Platform.get\_cached\_value(“Warehouse”, item.warehouse, “is\_group”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.warehouse → Platform.get\_cached\_value(“Warehouse”, item.warehouse, “is\_group”).
    - Call the validation error handler Platform.throw(translated “Cannot create Material Request for item {0} in group warehouse {1}.”.format(Platform.bold(item.item\_code), Platform.bold(item.warehouse))).
  - Set material\_request\_type from (item.material\_request\_type or item\_doc.default\_material\_request\_type).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.material\_request\_type → item\_doc.default\_material\_request\_type.
  - Set key from “{}:{}:{}”.format(item.sales\_order, material\_request\_type, empty text).
  - Set schedule\_date from (item.schedule\_date or add\_days(nowdate(), cint(item\_doc.lead\_time\_days))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.schedule\_date → add\_days(nowdate(), cint(item\_doc.lead\_time\_days)).
  - If key does not belong to material\_request\_map.
    - Set material\_request\_map at key from Platform.new\_doc(“Material Request”).
    - Set material\_request from material\_request\_map at key.
    - Evaluate material\_request.update(mapping(“transaction\_date” → nowdate(), “status” → “Draft”, “company” → self.company, “material\_request\_type” → material\_request\_type)).
    - Evaluate material\_request\_list.append(material\_request).
  - Otherwise.
    - Set material\_request from material\_request\_map at key.
  - Evaluate material\_request.append(“items”, mapping(“item\_code” → item.item\_code, “from\_warehouse” → item.from\_warehouse when material\_request\_type equals “Material Transfer”, otherwise no value, “qty” → qty\_to\_reque ….
    - Value choice on material\_request\_type equals “Material Transfer” — true gives item.from\_warehouse, false gives no value.
    - Value choice on item.sales\_order — true gives Platform.db.get\_value(“Sales Order”, item.sales\_order, “project”), false gives no value.
- If not material\_request\_list.
  - Evaluate msgprint(translated “All items are already requested”).
  - Return no value.
- For each material\_request in material\_request\_list.
  - Set material\_request.flags.ignore\_permissions from 1.
  - Evaluate material\_request.run\_method(“set\_missing\_values”).
  - Evaluate material\_request.save().
  - If self.get(“submit\_material\_request”).
    - Evaluate material\_request.submit().
- Set Platform.flags.mute\_messages from false.
- If material\_request\_list.
  - Set material\_request\_list from list of get\_link\_to\_form(“Material Request”, m.name) for m drawn from material\_request\_list.
    - Draw m from material\_request\_list.
  - Evaluate msgprint(translated “{0} created”.format(comma\_and(material\_request\_list))).
- Otherwise.
  - Evaluate msgprint(translated “No material request created”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison qty\_to\_request ≤ 0, qty\_to\_request = 0 selects the branch that continues with the next loop iteration. With qty\_to\_request = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-fa3b140e6773c9-guard-12)

**Methods declared on this owner** [load saved plan for material request](operations-032.md#op-ec2c61f826484f), [validate mr subcontracted](operations-032.md#op-b7310538f66a8e), [get draft requested qty](operations-032.md#op-852792e249727f).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, item.item\_code), Platform.get\_cached\_value(“Warehouse”, item.warehouse, “is\_group”) · clock or generated value from nowdate() · selected callable from material\_request.run\_method(“set\_missing\_values”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L963) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L592)

<a id="op-ec2c61f826484f"></a>
### Production Plan.load saved plan for material request

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_productionplan_load_saved_plan_for_material_request`

**Inputs** self.

**Record and data access** read “Production Plan” via exists.

**Explicit failure paths** validation helper — translated “Save the Production Plan before creating Material Requests”.

**Local steps**

- Set submit\_material\_request from cint(self.get(“submit\_material\_request”)).
- If not (self.name and Platform.db.exists(“Production Plan”, self.name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.name → Platform.db.exists(“Production Plan”, self.name).
  - Call the validation error handler Platform.throw(translated “Save the Production Plan before creating Material Requests”).
- Evaluate self.load\_from\_db().
- Evaluate self.check\_permission(“write”).
- Set self.submit\_material\_request from submit\_material\_request.
- Evaluate self.validate\_plan\_is\_open().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate plan is open](operations-032.md#op-52437660645a62).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1710) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L950)

<a id="op-852792e249727f"></a>
### Production Plan.get draft requested qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_productionplan_get_draft_requested_qty`

**Inputs** self.

**Explicit results** Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(mr\_item.material\_request\_plan\_item).run()).

**Local steps**

- Set mr\_item from Platform.qb.DocType(“Material Request Item”).
- Return Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(mr\_item.material\_request\_plan\_item).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1707) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L947)

<a id="op-2142c351c57218"></a>
### Production Plan.get sub assembly items

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_get_subordinate_assembly_items`

**Inputs** self, manufacturing\_type = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “BOM” via get\_value.

**State and service calls** msgprint with translated “Row #{0}: Since 'Produce Item per Operation' is enabled, the BOM {1} cannot be used for Sub Assembly Items”.format(row.idx, row.bom\_no) · msgprint with message.

**Explicit failure paths** validation helper — translated “Row #{0}: Please select the Sub Assembly Warehouse”.format(row.idx) · validation helper — translated “Row #{0}: Please select Item Code in Assembly Items”.format(row.idx) · validation helper — translated “Row #{0}: Please select the BOM No in Assembly Items”.format(row.idx).

**Local steps**

- Set self.sub\_assembly\_items from list().
- Set sub\_assembly\_items\_store from list().
- Set bin\_details from Platform.\_dict().
- Set track\_semi\_finished\_goods from true.
- For each row in self.po\_items.
  - If (self.skip\_available\_sub\_assembly\_item and not self.sub\_assembly\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.skip\_available\_sub\_assembly\_item → not self.sub\_assembly\_warehouse.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Please select the Sub Assembly Warehouse”.format(row.idx)).
  - If not row.item\_code.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Please select Item Code in Assembly Items”.format(row.idx)).
  - If not row.bom\_no.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Please select the BOM No in Assembly Items”.format(row.idx)).
  - If Platform.db.get\_value(“BOM”, row.bom\_no, “track\_semi\_finished\_goods”).
    - Evaluate Platform.msgprint(translated “Row #{0}: Since 'Produce Item per Operation' is enabled, the BOM {1} cannot be used for Sub Assembly Items”.format(row.idx, row.bom\_no)).
    - Continue with the next iteration or loop test.
  - Set bom\_data from list().
  - Set track\_semi\_finished\_goods from false.
  - Evaluate get\_sub\_assembly\_items(bin\_details, row.bom\_no, bom\_data, get\_qty\_before\_process\_loss(row.planned\_qty, get\_plan\_process\_loss\_percentage(self, row.bom\_no), row.stock\_uom), warehouse = self.sub\_assembly\_ware ….
  - Evaluate self.set\_sub\_assembly\_items\_based\_on\_level(row, bom\_data, manufacturing\_type).
  - Evaluate sub\_assembly\_items\_store.extend(bom\_data).
- If (not track\_semi\_finished\_goods and not sub\_assembly\_items\_store and self.skip\_available\_sub\_assembly\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not track\_semi\_finished\_goods → not sub\_assembly\_items\_store → self.skip\_available\_sub\_assembly\_item.
  - Set message from (translated “As there are sufficient Sub Assembly Items, Work Order is not required for Warehouse {0}.”.format(self.sub\_assembly\_warehouse) + text in the contract).
  - Update message using + translated “If you still want to proceed, please disable '{0}' checkbox.”.format(self.meta.get\_field(“skip\_available\_sub\_assembly\_item”).label).
  - Evaluate Platform.msgprint(message, title = translated “Note”).
- If self.combine\_sub\_items.
  - Set sub\_assembly\_items\_store from self.combine\_subassembly\_items(sub\_assembly\_items\_store).
- For each tuple(idx, row) in enumerate(sub\_assembly\_items\_store).
  - Set row.idx from (idx + 1).
  - Evaluate self.append(“sub\_assembly\_items”, row).
- Evaluate self.set\_default\_supplier\_for\_subcontracting\_order().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set sub assembly items based on level](operations-032.md#op-2c3fedaa8a0349), [combine subassembly items](operations-032.md#op-ce3c295c447c1a), [set default supplier for subcontracting order](operations-032.md#op-5703f813f6d5f1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L962) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L591)

<a id="op-2c3fedaa8a0349"></a>
### Production Plan.set sub assembly items based on level

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_set_subordinate_assembly_items_based_on_level`

**Inputs** self, row, bom\_data, manufacturing\_type = no value.

**Record and data access** read “Warehouse” via get\_value.

**Local steps**

- Set is\_group\_warehouse from Platform.db.get\_value(“Warehouse”, self.sub\_assembly\_warehouse, “is\_group”).
- For each data in bom\_data.
  - Set data.qty from data.stock\_qty.
  - Set data.production\_plan\_item from row.name.
  - Set data.schedule\_date from row.planned\_start\_date.
  - Set data.type\_of\_manufacturing from (manufacturing\_type or “Subcontract” when data.is\_sub\_contracted\_item, otherwise “In House”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in manufacturing\_type → “Subcontract” when data.is\_sub\_contracted\_item, otherwise “In House”.
    - Value choice on data.is\_sub\_contracted\_item — true gives “Subcontract”, false gives “In House”.
  - If not is\_group\_warehouse.
    - Set data.fg\_warehouse from self.sub\_assembly\_warehouse.
  - If not self.combine\_sub\_items.
    - Set data.sales\_order from row.sales\_order.
    - Set data.sales\_order\_item from row.sales\_order\_item.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L977) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L606)

<a id="op-5703f813f6d5f1"></a>
### Production Plan.set default supplier for subcontracting order

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_set_default_supplier_for_subcontracting_order`

**Inputs** self.

**Record and data access** read “Item Default” via get\_all.

**Explicit results** no value.

**Local steps**

- Set items from list of d.production\_item for d drawn from self.sub\_assembly\_items where d.type\_of\_manufacturing equals “Subcontract”.
  - Draw d from self.sub\_assembly\_items, keep a combination only if (d.type\_of\_manufacturing equals “Subcontract”).
- If not items.
  - Return no value.
- Set default\_supplier from Platform.\_dict(Platform.get\_all(“Item Default”, fields = list(“parent”, “default\_supplier”), filters = mapping(“parent” → tuple(“in”, items), “default\_supplier” → tuple(“is”, “set”)), as\_list = 1)).
- If not default\_supplier.
  - Return no value.
- For each row in self.sub\_assembly\_items.
  - If row.type\_of\_manufacturing differs from “Subcontract”.
    - Continue with the next iteration or loop test.
  - Set row.supplier from default\_supplier.get(row.production\_item).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L974) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L603)

<a id="op-ce3c295c447c1a"></a>
### Production Plan.combine subassembly items

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_combine_subassembly_items`

**Inputs** self, sub\_assembly\_items\_store.

**Explicit results** sub\_assembly\_items\_store.

**Local steps**

- Set key\_wise\_data from mapping().
- For each row in sub\_assembly\_items\_store.
  - Set key from tuple(row.get(“production\_item”), row.get(“fg\_warehouse”), row.get(“bom\_no”), row.get(“type\_of\_manufacturing”)).
  - If key does not belong to key\_wise\_data.
    - Set key\_wise\_data at key from row.
    - Continue with the next iteration or loop test.
  - Set existing\_row from key\_wise\_data at key.
  - If existing\_row.
    - Update existing\_row.qty using + flt(row.qty).
    - Update existing\_row.required\_qty using + flt(row.required\_qty).
    - Update existing\_row.stock\_qty using + flt(row.stock\_qty).
    - Set existing\_row.bom\_level from max(existing\_row.bom\_level, row.bom\_level).
    - Continue with the next iteration or loop test.
  - Otherwise.
    - Set key\_wise\_data at key from row.
- Set sub\_assembly\_items\_store from list of key\_wise\_data at key for key drawn from key\_wise\_data.
  - Draw key from key\_wise\_data.
- Return sub\_assembly\_items\_store.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L947) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L578)

<a id="op-17ae94613df0b1"></a>
### Production Plan.all items completed

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_all_items_completed`

**Inputs** self.

**Record and data access** read “Work Order” via get\_all.

**Explicit results** false · all\_work\_orders\_completed.

**Local steps**

- Set all\_items\_produced from all(generator of (flt(d.planned\_qty) − flt(d.produced\_qty)) &lt; 1e-06 for d drawn from self.po\_items).
  - Draw d from self.po\_items.
- If not all\_items\_produced.
  - Return false.
- Set wo\_status from Platform.get\_all(“Work Order”, filters = mapping(“production\_plan” → self.name, “status” → tuple(“not in”, list(“Closed”, “Stopped”)), “docstatus” → 1), fields = “status”, pluck = “status”).
- Set all\_work\_orders\_completed from all(generator of s equals “Completed” for s drawn from wo\_status).
  - Draw s from wo\_status.
- Return all\_work\_orders\_completed.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L943) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L574)

<a id="op-8eadd39cc825cd"></a>
### Get mr item planned qty query

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_mr_item_planned_qty_query`

**Inputs** mr\_item.

**Explicit results** nested operand in the contract.qb.from\_(plan\_item).select(Sum(plan\_item.planned\_qty)).where((plan\_item.material\_request\_item equals mr\_item.name bitwise and plan\_item.docstatus equals 1)).

**Local steps**

- Set plan\_item from Platform.qb.DocType(“Production Plan Item”).
- Return nested operand in the contract.qb.from\_(plan\_item).select(Sum(plan\_item.planned\_qty)).where((plan\_item.material\_request\_item equals mr\_item.name bitwise and plan\_item.docstatus equals 1)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L912)

<a id="op-76c1af92150da1"></a>
### Get planned qty of references

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_planned_qty_of_references`

**Inputs** sales\_orders.

**Explicit results** list() · allocated.

**Local steps**

- Set plans from get\_plans\_with\_references(sales\_orders).
- If not plans.
  - Return list().
- Set reference from Platform.qb.DocType(“Production Plan Item Reference”).
- Set references from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.isin(p ….
- Set planned\_qty from get\_planned\_qty\_by\_order\_row(plans).
- Set allocated from list().
- For each row in references.
  - Set key from tuple(row.parent, row.item\_reference).
  - Set qty from min(flt(row.qty), max(planned\_qty.get(key, 0), 0)).
  - Set planned\_qty at key from (planned\_qty.get(key, 0) − qty).
  - Evaluate allocated.append(Platform.\_dict(sales\_order = row.sales\_order, sales\_order\_item = row.sales\_order\_item, qty = qty)).
- Return allocated.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L183) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L920)

<a id="op-daf1e1c3b17228"></a>
### Get plans with references

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_plans_with_references`

**Inputs** sales\_orders.

**Explicit results** nested operand in the contract(nested operand in the contract).distinct().where((nested operand in the contract.sales\_order.isin(sales\_orders) bitwise and plan.docstatus equals 1)).run(pluck = true).

**Local steps**

- Set reference from Platform.qb.DocType(“Production Plan Item Reference”).
- Set plan from Platform.qb.DocType(“Production Plan”).
- Return nested operand in the contract(nested operand in the contract).distinct().where((nested operand in the contract.sales\_order.isin(sales\_orders) bitwise and plan.docstatus equals 1)).run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L184) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L921)
