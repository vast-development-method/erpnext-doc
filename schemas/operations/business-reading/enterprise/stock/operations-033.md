# Inventory and warehouses · operations 33

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Material request

[Record definition](../../../../data/record-types/material_request.json)

<a id="op-3a3fa0c679cd75"></a>
### Material Request.validate work order qty

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_materialrequest_validate_work_order_qty`

**Inputs** self, row, ordered\_qty, mr\_qty\_allowance.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.InvalidStatusError — translated “Material Request {0} is stopped”.format(self.name) · validation helper — translated “The total Work Order quantity {0} in Material Request {1} cannot be greater than allowed requested quantity  …”.format(ordered\_qty, self.name, allowed\_qty, row.item\_code).

**Local steps**

- Set precision from row.precision(“ordered\_qty”).
- If flt(ordered\_qty, precision) ≤ flt(row.ordered\_qty, precision).
  - Return no value.
- <a id="op-3a3fa0c679cd75-guard-6"></a>If self.status equals “Stopped”.
  - Call the validation error handler Platform.throw(translated “Material Request {0} is stopped”.format(self.name), Platform.InvalidStatusError).
- Set allowed\_qty from flt((row.stock\_qty + ((row.stock\_qty × flt(mr\_qty\_allowance)) ÷ 100)), precision).
- If flt(ordered\_qty, precision) &gt; allowed\_qty.
  - Call the validation error handler Platform.throw(translated “The total Work Order quantity {0} in Material Request {1} cannot be greater than allowed requested quantity  …”.format(ordered\_qty, self.name, allowed\_qty, row.item\_code)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Stopped”, self.status = “Stopped” selects the branch that calls the validation-error handler with translated “Material Request {0} is stopped”.format(self.name). With self.status = “Draft”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-3a3fa0c679cd75-guard-6)

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L874) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L371)

<a id="op-d82943adc4fbf1"></a>
### Material Request.update requested qty

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_update_requested_quantity`

**Inputs** self, mr\_item\_rows = no value.

**Record and data access** read “Item” via get\_all.

**Explicit results** no value.

**Local steps**

- Set item\_warehouses from dict.fromkeys(generator of tuple(d.item\_code, d.warehouse) for d drawn from self.get(“items”) where (d.warehouse and (not mr\_item\_rows or d.name belongs to mr\_item\_rows))).
  - Draw d from self.get(“items”), keep a combination only if ((d.warehouse and (not mr\_item\_rows or d.name belongs to mr\_item\_rows))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.warehouse → (not mr\_item\_rows or d.name belongs to mr\_item\_rows).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not mr\_item\_rows → d.name belongs to mr\_item\_rows.
- If not item\_warehouses.
  - Return no value.
- Set stock\_items from set(Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, set of item\_code for tuple(item\_code, warehouse) drawn from item\_warehouses), “is\_stock\_item” → 1), pluck = “name”)).
  - Draw tuple(item\_code, warehouse) from item\_warehouses.
- For each tuple(item\_code, warehouse) in item\_warehouses.
  - If item\_code does not belong to stock\_items.
    - Continue with the next iteration or loop test.
  - Evaluate update\_bin\_qty(item\_code, warehouse, mapping(“indented\_qty” → get\_indented\_qty(item\_code, warehouse))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1320)

<a id="op-eb9942e90d2b4f"></a>
### Material Request.update requested qty in production plan

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_update_requested_quantity_in_production_plan`

**Inputs** self, cancel = false.

**Explicit results** no value.

**Local steps**

- Set items\_from\_pp from list of d for d drawn from self.items where (d.production\_plan and d.material\_request\_plan\_item).
  - Draw d from self.items, keep a combination only if ((d.production\_plan and d.material\_request\_plan\_item)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.production\_plan → d.material\_request\_plan\_item.
- If not items\_from\_pp.
  - Return no value.
- Evaluate update\_plan\_item\_requested\_qty(set of d.material\_request\_plan\_item for d drawn from items\_from\_pp).
  - Draw d from items\_from\_pp.
- Evaluate update\_production\_plan\_status(set of d.production\_plan for d drawn from items\_from\_pp).
  - Draw d from items\_from\_pp.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1321)

<a id="op-aded92330aa5c3"></a>
### Update production plan status

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_update_production_plan_status`

**Inputs** production\_plans.

**Record and data access** resolve a document from “Production Plan” via get\_doc.

**State and service calls** call db\_set on doc.

**Local steps**

- For each production\_plan in production\_plans.
  - Set doc from Platform.get\_doc(“Production Plan”, production\_plan).
  - Set doc.flags.ignore\_permissions from true.
  - Evaluate doc.set\_status().
  - Evaluate doc.db\_set(“status”, doc.status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L879) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L376)

<a id="op-96cb5c58c199ac"></a>
### Update plan item requested qty

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_update_plan_item_requested_qty`

**Inputs** plan\_item\_names.

**State and service calls** request set\_value on “Material Request Plan Item”.

**Local steps**

- Set mr\_item from Platform.qb.DocType(“Material Request Item”).
- Set plan\_item from Platform.qb.DocType(“Material Request Plan Item”).
- Set requested from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.isin(nested operand in the contract(neste ….
- For each row in requested.
  - Set requested\_qty from (flt(row.stock\_qty) ÷ (flt(row.conversion\_factor) or 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.conversion\_factor) → 1.
  - Evaluate Platform.db.set\_value(“Material Request Plan Item”, row.name, “requested\_qty”, requested\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L878) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L375)

<a id="op-08ca49863157cb"></a>
### Get qty in plan uom

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_get_qty_in_plan_uom`

**Inputs** item, plan\_item.

**Explicit results** (flt(item.stock\_qty) ÷ (flt(plan\_item.conversion\_factor) or 1)).

**Local steps**

- Return (flt(item.stock\_qty) ÷ (flt(plan\_item.conversion\_factor) or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(plan\_item.conversion\_factor) → 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L848) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L345)

<a id="op-86f866554baea9"></a>
### Validate request not stopped

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_validate_request_not_stopped`

**Inputs** source\_name.

**Record and data access** read “Material Request” via get\_value.

**Explicit failure paths** validation helper with Platform.InvalidStatusError — translated “Material Request {0} is stopped”.format(source\_name).

**Local steps**

- If Platform.db.get\_value(“Material Request”, source\_name, “status”) equals “Stopped”.
  - Call the validation error handler Platform.throw(translated “Material Request {0} is stopped”.format(source\_name), Platform.InvalidStatusError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L880) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L377)

<a id="op-100703c06d8178"></a>
### Get pending pick qty

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_get_pending_pick_qty`

**Inputs** row.

**Explicit results** (flt(row.stock\_qty) − max(flt(row.ordered\_qty), flt(row.picked\_qty))).

**Local steps**

- Return (flt(row.stock\_qty) − max(flt(row.ordered\_qty), flt(row.picked\_qty))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L847) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L344)

<a id="op-5ccc45f388008d"></a>
### Get draft work order qty

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_get_draft_work_order_qty`

**Inputs** material\_request.

**Explicit results** Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(work\_order.material\_request\_item).run()).

**Local steps**

- Set work\_order from Platform.qb.DocType(“Work Order”).
- Return Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(work\_order.material\_request\_item).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L844) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L341)

<a id="op-bf6b338c473271"></a>
### Is valid buying price list

`operation_enterprise_stock_record_definitions_material_request_business_behavior_is_valid_buying_price_list`

**Inputs** price\_list.

**Declared result** bool.

**Record and data access** read “Price List” via get\_value.

**Explicit results** (is\_price\_list\_enabled(price\_list) and bool(Platform.get\_value(“Price List”, price\_list, “buying”))).

**Local steps**

- Return (is\_price\_list\_enabled(price\_list) and bool(Platform.get\_value(“Price List”, price\_list, “buying”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_price\_list\_enabled(price\_list) → bool(Platform.get\_value(“Price List”, price\_list, “buying”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0753.json#L2919) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1303)

<a id="op-23baa65d3b12d6"></a>
### Update completed and requested qty

`operation_enterprise_stock_record_definitions_material_request_business_behavior_update_completed_and_requested_quantity`

**Inputs** stock\_entry, method.

**Record and data access** resolve a document from “Material Request” via get\_doc.

**Explicit failure paths** validation helper with Platform.InvalidStatusError — translated “{0} {1} is cancelled or stopped”.format(translated “Material Request”, mr).

**Local steps**

- If stock\_entry.doctype equals “Stock Entry”.
  - Set material\_request\_map from mapping().
  - For each d in stock\_entry.get(“items”).
    - If d.material\_request.
      - Evaluate material\_request\_map.setdefault(d.material\_request, list()).append(d.material\_request\_item).
  - For each tuple(mr, mr\_item\_rows) in material\_request\_map.items().
    - If (mr and mr\_item\_rows).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in mr → mr\_item\_rows.
      - Set mr\_obj from Platform.get\_doc(“Material Request”, mr).
      - If mr\_obj.status belongs to list(“Stopped”, “Cancelled”).
        - Call the validation error handler Platform.throw(translated “{0} {1} is cancelled or stopped”.format(translated “Material Request”, mr), Platform.InvalidStatusError).
      - Evaluate mr\_obj.update\_completed\_qty(mr\_item\_rows).
      - Evaluate mr\_obj.update\_requested\_qty(mr\_item\_rows).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0753.json#L3043) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L150) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1331)

<a id="op-eba610f5b51d6e"></a>
### Set missing values

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_set_missing_values`

**Inputs** source, target\_doc.

**Local steps**

- If (target\_doc.doctype equals “Purchase Order” and getdate(target\_doc.schedule\_date) &lt; getdate(nowdate())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in target\_doc.doctype equals “Purchase Order” → getdate(target\_doc.schedule\_date) &lt; getdate(nowdate()).
  - Set target\_doc.schedule\_date from no value.
- Evaluate target\_doc.run\_method(“set\_missing\_values”).
- Evaluate target\_doc.run\_method(“calculate\_taxes\_and\_totals”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate() · selected callable from target\_doc.run\_method(“set\_missing\_values”), target\_doc.run\_method(“calculate\_taxes\_and\_totals”).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L876) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L373)

<a id="op-16e4de1f5dcb32"></a>
### Get source item for qty

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_get_source_item_for_qty`

**Inputs** item, qty.

**Explicit results** source\_item.

**Local steps**

- Set source\_item from Platform.\_dict(item.as\_dict()).
- Set source\_item.ordered\_qty from 0.
- Set source\_item.received\_qty from 0.
- Set source\_item.stock\_qty from (flt(qty) × flt(item.conversion\_factor)).
- Return source\_item.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L849) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L346)

<a id="op-bf1a699a5654f5"></a>
### Update item

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_update_item`

**Inputs** obj, target, source\_parent.

**Record and data access** read “UOM Conversion Detail” via get\_value.

**Local steps**

- Set target.conversion\_factor from obj.conversion\_factor.
- Set qty from (obj.ordered\_qty or obj.received\_qty).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in obj.ordered\_qty → obj.received\_qty.
- Set target.qty from (flt((flt(obj.stock\_qty) − flt(qty))) ÷ target.conversion\_factor).
- Set target.stock\_qty from (target.qty × target.conversion\_factor).
- If getdate(target.schedule\_date) &lt; getdate(nowdate()).
  - Set target.schedule\_date from no value.
- If target.fg\_item.
  - Set target.fg\_item\_qty from target.stock\_qty.
  - If sc\_bom bound to get\_subcontracting\_boms\_for\_finished\_goods(target.fg\_item).
    - Set target.item\_code from sc\_bom.service\_item.
    - Set target.uom from sc\_bom.service\_item\_uom.
    - Set target.conversion\_factor from (Platform.db.get\_value(“UOM Conversion Detail”, mapping(“parent” → sc\_bom.service\_item, “uom” → sc\_bom.service\_item\_uom), “conversion\_factor”) or 1).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“UOM Conversion Detail”, mapping(“parent” → sc\_bom.service\_item, “uom” → sc\_bom.service\_item\_uom), “conversion\_factor”) → 1.
    - Set target.qty from (target.fg\_item\_qty × sc\_bom.conversion\_factor).
    - Set target.stock\_qty from (target.qty × target.conversion\_factor).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L877) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L374)

<a id="op-cebaaa943b7bb5"></a>
### Notify missing service items

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_notify_missing_service_items`

**Inputs** purchase\_order.

**State and service calls** msgprint with translated “No active Subcontracting BOM found for Finished Good {0}. Please select the Service Item manually for these rows.”.format(comma\_and(list of get\_link\_to\_form(“Item”, fg\_item) for fg\_item drawn f ….

**Explicit results** no value.

**Local steps**

- Set finished\_goods from list(dict.fromkeys(generator of d.fg\_item for d drawn from purchase\_order.items where (d.fg\_item and not d.item\_code))).
  - Draw d from purchase\_order.items, keep a combination only if ((d.fg\_item and not d.item\_code)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.fg\_item → not d.item\_code.
- If not finished\_goods.
  - Return no value.
- Evaluate Platform.msgprint(translated “No active Subcontracting BOM found for Finished Good {0}. Please select the Service Item manually for these rows.”.format(comma\_and(list of get\_link\_to\_form(“Item”, fg\_item) f ….
  - Draw fg\_item from finished\_goods.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L875) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L372)

<a id="op-888ef4140e3b72"></a>
### Get list context

`operation_enterprise_stock_record_definitions_material_request_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** list\_context.

**Local steps**

- Bind dependencies get\_list\_context.
- Set list\_context from get\_list\_context(context).
- Evaluate list\_context.update(mapping(“show\_sidebar” → true, “show\_search” → true, “no\_breadcrumbs” → true, “title” → translated “Material Request”, …)).
- Return list\_context.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0753.json#L3484) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1301)

<a id="op-d9342712108c80"></a>
### Update status

`operation_enterprise_stock_record_definitions_material_request_business_behavior_update_status`

**Inputs** name, status.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Material Request” via get\_doc.

**Local steps**

- Set material\_request from Platform.get\_doc(“Material Request”, name).
- Evaluate material\_request.check\_permission(“write”).
- Evaluate material\_request.update\_status(status).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from material\_request.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L151) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1332)

<a id="op-47cd147365b021"></a>
### Make purchase order

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_purchase_order`

**Inputs** source\_name, target\_doc = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Material Request” via get\_value.

**Explicit results** doclist.

**Local steps**

- Evaluate validate\_request\_not\_stopped(source\_name).
- If args is identical to no value.
  - Set args from (Platform.flags.args or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.args → mapping().
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set mapped\_qty\_by\_item from get\_qty\_already\_mapped(target\_doc, “material\_request\_item”, “stock\_qty”).
- Set is\_subcontracted from Platform.db.get\_value(“Material Request”, source\_name, “material\_request\_type”) equals “Subcontracting”.
- Set requested\_qty from (args.get(“requested\_qty”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“requested\_qty”) → mapping().
- Bind local operation postprocess for subsequent calls.
- Bind local operation update\_requested\_item for subsequent calls.
- Bind local operation select\_item for subsequent calls.
- Bind local operation generate\_field\_map for subsequent calls.
- Set doclist from get\_mapped\_doc(“Material Request”, source\_name, mapping(“Material Request” → mapping(“doctype” → “Purchase Order”, “validation” → mapping(“docstatus” → list(“=”, 1), “material\_request\_type” → list(“in”, li ….
  - Value choice on is\_subcontracted — true gives list(“item\_code”, “item\_name”, “qty”), false gives list().
- If is\_subcontracted.
  - Evaluate notify\_missing\_service\_items(doclist).
- Evaluate doclist.set\_onload(“load\_after\_mapping”, false).
- Return doclist.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L851) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L348)

<a id="op-bbe15412e0d62f"></a>
### Make purchase order.postprocess

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_purchase_order_postprocess`

**Inputs** source, target\_doc.

**Local steps**

- Set target\_doc.is\_subcontracted from is\_subcontracted.
- If args.get(“supplier”).
  - Set target\_doc.supplier from args.get(“supplier”).
- Evaluate set\_missing\_values(source, target\_doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L855) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L352)

<a id="op-c56ec8e9e83da5"></a>
### Make purchase order.update requested item

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_purchase_order_update_requested_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- If obj.name belongs to requested\_qty.
  - Set obj from get\_source\_item\_for\_qty(obj, requested\_qty at obj.name).
- Evaluate update\_item(obj, target, source\_parent).
- If (not target.rate and not target.price\_list\_rate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not target.rate → not target.price\_list\_rate.
  - Set target.rate, target.price\_list\_rate from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L857) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L354)

<a id="op-c28964016b4a5b"></a>
### Make purchase order.select item

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_purchase_order_select_item`

**Inputs** d.

**Explicit results** (qty &lt; d.stock\_qty and child\_filter).

**Local steps**

- Set filtered\_items from args.get(“filtered\_children”, list()).
- Set child\_filter from d.name belongs to filtered\_items when filtered\_items, otherwise true.
  - Value choice on filtered\_items — true gives d.name belongs to filtered\_items, false gives true.
- Set qty from ((d.ordered\_qty or d.received\_qty) + flt(mapped\_qty\_by\_item.get(d.name, 0))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.ordered\_qty → d.received\_qty.
- Return (qty &lt; d.stock\_qty and child\_filter).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty &lt; d.stock\_qty → child\_filter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L856) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L353)

<a id="op-748890d490e833"></a>
### Make purchase order.generate field map

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_purchase_order_generate_field_map`

**Inputs** no declared parameters.

**Explicit results** field\_map.

**Local steps**

- Set field\_map from list(list(“name”, “material\_request\_item”), list(“parent”, “material\_request”), list(“sales\_order”, “sales\_order”), list(“sales\_order\_item”, “sales\_order\_item”), …).
- If is\_subcontracted.
  - Evaluate field\_map.extend(list(list(“item\_code”, “fg\_item”), list(“qty”, “fg\_item\_qty”))).
- Otherwise.
  - Evaluate field\_map.extend(list(list(“uom”, “stock\_uom”), list(“uom”, “uom”))).
- Return field\_map.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L854) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L351)

<a id="op-7f3331c6255fb9"></a>
### Get default supplier for item

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_get_default_supplier_for_item`

**Inputs** item\_code, company.

**Declared result** (str bitwise or no value).

**Explicit results** get\_default\_supplier(Platform.\_dict(), get\_item\_defaults(item\_code, company), get\_item\_group\_defaults(item\_code, company), get\_brand\_defaults(item\_code, company)).

**Local steps**

- Return get\_default\_supplier(Platform.\_dict(), get\_item\_defaults(item\_code, company), get\_item\_group\_defaults(item\_code, company), get\_brand\_defaults(item\_code, company)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L843) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L340)

<a id="op-0a38445f595f90"></a>
### Get item default suppliers

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_get_item_default_suppliers`

**Inputs** source\_name, filtered\_children = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** resolve a document from “Material Request” via get\_doc.

**Explicit results** items.

**Local steps**

- Set filtered\_children from Platform.parse\_json(filtered\_children) when filtered\_children, otherwise list().
  - Value choice on filtered\_children — true gives Platform.parse\_json(filtered\_children), false gives list().
- Set material\_request from Platform.get\_doc(“Material Request”, source\_name).
- Evaluate material\_request.check\_permission(“read”).
- Set items from list().
- For each item in material\_request.items.
  - If (filtered\_children and item.name does not belong to filtered\_children).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filtered\_children → item.name does not belong to filtered\_children.
    - Continue with the next iteration or loop test.
  - Set ordered\_qty from (flt(item.ordered\_qty) or flt(item.received\_qty)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.ordered\_qty) → flt(item.received\_qty).
  - If ordered\_qty ≥ flt(item.stock\_qty).
    - Continue with the next iteration or loop test.
  - Evaluate items.append(mapping(“material\_request\_item” → item.name, “item\_code” → item.item\_code, “item\_name” → item.item\_name, “pending\_qty” → ((flt(item.stock\_qty) − ordered\_qty) ÷ (flt(item.conversion\_factor) or 1)), …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.conversion\_factor) → 1.
- Return items.

**Values supplied outside this operation** effective access from material\_request.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L845) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L342)
