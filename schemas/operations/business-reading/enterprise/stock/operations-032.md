# Inventory and warehouses · operations 32

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Material request

[Record definition](../../../../data/record-types/material_request.json)

<a id="op-db46186a9c7a90"></a>
### Material Request.update item rates

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_update_item_rates`

**Inputs** self.

**Record and data access** read “Price List” via get\_value.

**State and service calls** call db\_set on item · msgprint with translated “Item rates have been updated based on the selected Buying Price List {0}”.format(self.buying\_price\_list).

**Local steps**

- Set price\_not\_uom\_dependent from Platform.get\_value(“Price List”, self.buying\_price\_list, “price\_not\_uom\_dependent”).
- For each item in self.items.
  - Set rate from get\_price\_list\_rate\_for(Platform.\_dict(mapping(“price\_list” → self.buying\_price\_list, “uom” → item.uom, “transaction\_date” → self.transaction\_date, “qty” → item.qty, …)), item.item\_code).
  - If rate is distinct from no value.
    - Evaluate item.db\_set(mapping(“rate” → rate, “amount” → flt((rate × item.qty), item.precision(“amount”)))).
- Evaluate Platform.msgprint(translated “Item rates have been updated based on the selected Buying Price List {0}”.format(self.buying\_price\_list), alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0752.json#L4190) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1319)

<a id="op-3c6d5c953a63b1"></a>
### Material Request.validate pp qty

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_validate_production_plan_quantity`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Quantity cannot be greater than {0} for Item {1}”.format(available\_qty, item.item\_code).

**Local steps**

- Set items\_from\_pp from list of item for item drawn from self.items where item.material\_request\_plan\_item.
  - Draw item from self.items, keep a combination only if (item.material\_request\_plan\_item).
- If not items\_from\_pp.
  - Return no value.
- Set plan\_items from self.get\_plan\_items(items\_from\_pp).
- Set requested\_qty from mapping().
- For each item in items\_from\_pp.
  - Set row from plan\_items at item.material\_request\_plan\_item.
  - Set precision from item.precision(“qty”).
  - Set available\_qty from flt((flt(row.quantity) − flt(row.requested\_qty)), precision).
  - Set qty from get\_qty\_in\_plan\_uom(item, row).
  - Set requested\_qty at row.name from (requested\_qty.get(row.name, 0) + qty).
  - If max(flt(qty, precision), flt(requested\_qty at row.name, precision)) &gt; available\_qty.
    - Call the validation error handler Platform.throw(translated “Quantity cannot be greater than {0} for Item {1}”.format(available\_qty, item.item\_code)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get plan items](operations-032.md#op-cd3bf13eed3f29).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L146) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1327)

<a id="op-cd3bf13eed3f29"></a>
### Material Request.get plan items

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_materialrequest_get_plan_items`

**Inputs** self, items.

**Record and data access** read “Material Request Plan Item” via get\_all.

**Explicit results** mapping of row.name → row for row drawn from Platform.get\_all(“Material Request Plan Item”, filters = mapping(“name” → tuple(“in”, set of item.material\_request\_plan\_item for item drawn from items)), fields ….

**Local steps**

- Return mapping of row.name → row for row drawn from Platform.get\_all(“Material Request Plan Item”, filters = mapping(“name” → tuple(“in”, set of item.material\_request\_plan\_item for item drawn from items)), fields ….
  - Draw row from Platform.get\_all(“Material Request Plan Item”, filters = mapping(“name” → tuple(“in”, set of item.material\_request\_plan\_item for item drawn from items)), fields = list(“name”, “quantity”, “requested\_qty”,  ….
  - Draw item from items.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L868) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L365)

<a id="op-1d4d44c73bf373"></a>
### Material Request.before update after submit

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_before_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_schedule\_date().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0752.json#L5193) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1307)

<a id="op-bdbcbf86bbc5f7"></a>
### Material Request.clear source warehouse

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_materialrequest_clear_source_warehouse`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- <a id="op-bdbcbf86bbc5f7-guard-3"></a>If self.material\_request\_type equals “Material Transfer”.
  - Return no value.
- For each item in self.items.
  - Set item.from\_warehouse from no value.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.material\_request\_type equals “Material Transfer”, self.material\_request\_type = “Material Transfer” selects the branch that returns no value. With self.material\_request\_type = “Purchase”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-bdbcbf86bbc5f7-guard-3)

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L867) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L364)

<a id="op-85f6567f8f721c"></a>
### Material Request.validate material request type

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_validate_material_request_type`

**Inputs** self.

**Local steps**

- If self.material\_request\_type equals “Customer Provided”.
  - Evaluate self.validate\_customer\_provided\_items().
- Otherwise.
  - Set self.customer from no value.
- If self.material\_request\_type equals “Subcontracting”.
  - Evaluate self.validate\_subcontracted\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate customer provided items](operations-032.md#op-f742ce8b0ac071), [validate subcontracted items](operations-032.md#op-6cc2c9234097d4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L144) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1325)

<a id="op-f742ce8b0ac071"></a>
### Material Request.validate customer provided items

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_materialrequest_validate_customer_provided_items`

**Inputs** self.

**Record and data access** read “Item” via get\_all.

**Explicit failure paths** validation helper — translated “Items {0} are not Customer Provided Items”.format(“, ”.join(generator of Platform.bold(d) for d drawn from sorted(other\_items))).

**Local steps**

- Set items from set of d.item\_code for d drawn from self.items where d.item\_code.
  - Draw d from self.items, keep a combination only if (d.item\_code).
- Set provided\_items from Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, items), “is\_customer\_provided\_item” → 1), pluck = “name”).
- If other\_items bound to (items − set(provided\_items)).
  - Call the validation error handler Platform.throw(translated “Items {0} are not Customer Provided Items”.format(“, ”.join(generator of Platform.bold(d) for d drawn from sorted(other\_items)))).
    - Draw d from sorted(other\_items).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L871) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L368)

<a id="op-6cc2c9234097d4"></a>
### Material Request.validate subcontracted items

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_materialrequest_validate_subcontracted_items`

**Inputs** self.

**Record and data access** read “Item” via get\_all.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} must be a stock item with Supply Raw Materials for Purchase enabled for a Subcontracting  …”.format(row.idx, get\_link\_to\_form(“Item”, row.item\_code)).

**Local steps**

- Set items from Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, list(set of d.item\_code for d drawn from self.items where d.item\_code))), fields = list(“name”, “is\_stock\_item”, “is\_sub\_contracted\_item”)).
  - Draw d from self.items, keep a combination only if (d.item\_code).
- Set items from mapping of d.name → d for d drawn from items.
  - Draw d from items.
- For each row in self.items.
  - Set item from items.get(row.item\_code).
  - If (item and not (item.is\_stock\_item and item.is\_sub\_contracted\_item)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → not (item.is\_stock\_item and item.is\_sub\_contracted\_item).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.is\_stock\_item → item.is\_sub\_contracted\_item.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} must be a stock item with Supply Raw Materials for Purchase enabled for a Subcontracting  …”.format(row.idx, get\_link\_to\_form(“Item”, row.item\_code)), title =  ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L873) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L370)

<a id="op-aea116e0bfb713"></a>
### Material Request.set title

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_set_title`

**Inputs** self.

**Local steps**

- If not self.title.
  - Set items from “, ”.join(list of d.item\_name for d drawn from self.items at slice no value to 3).
    - Draw d from self.items.
  - Set self.title from translated “{0} Request for {1}”.format(translated self.material\_request\_type, items) at slice no value to 100.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0752.json#L5314) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1316)

<a id="op-1cb75c1fc5ee25"></a>
### Material Request.on submit

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_on_submit`

**Inputs** self.

**Record and data access** read “Budget” via exists.

**Local steps**

- Evaluate self.update\_requested\_qty\_in\_production\_plan().
- Evaluate self.update\_requested\_qty().
- Evaluate self.update\_requested\_qty\_in\_job\_card().
- Evaluate self.update\_requested\_qty\_in\_work\_order().
- Evaluate self.update\_prevdoc\_status().
- If (self.material\_request\_type equals “Purchase” and Platform.db.exists(“Budget”, mapping(“applicable\_on\_material\_request” → 1, “docstatus” → 1))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.material\_request\_type equals “Purchase” → Platform.db.exists(“Budget”, mapping(“applicable\_on\_material\_request” → 1, “docstatus” → 1)).
  - Evaluate self.validate\_budget().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update requested qty in production plan](operations-033.md#op-eb9942e90d2b4f), [update requested qty](operations-033.md#op-d82943adc4fbf1), [update requested qty in job card](operations-032.md#op-1b18cc92fd6133), [update requested qty in work order](operations-032.md#op-e90928f073f530).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1313)

<a id="op-9f62d406319e6d"></a>
### Material Request.before save

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status(update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0752.json#L5745) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1305)

<a id="op-77fdcddc08bede"></a>
### Material Request.before submit

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status(update = true).
- Evaluate self.validate\_pending\_qty\_in\_job\_card().
- Evaluate self.validate\_pending\_qty\_in\_work\_order().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate pending qty in job card](operations-032.md#op-c576dbd65c0be1), [validate pending qty in work order](operations-032.md#op-e35c3dfc8faa53).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1306)

<a id="op-c576dbd65c0be1"></a>
### Material Request.validate pending qty in job card

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_materialrequest_validate_pending_qty_in_job_card`

**Inputs** self.

**Record and data access** resolve a document from “Job Card” via get\_doc.

**Local steps**

- If self.job\_card.
  - Set job\_card from Platform.get\_doc(“Job Card”, self.job\_card, for\_update = true).
  - Evaluate job\_card.validate\_incoming\_material\_demand(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L872) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L369)

<a id="op-e35c3dfc8faa53"></a>
### Material Request.validate pending qty in work order

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_validate_pending_quantity_in_work_order`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Explicit results** no value.

**Local steps**

- If (not self.work\_order or self.job\_card or self.material\_request\_type differs from “Material Transfer”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.work\_order → self.job\_card → self.material\_request\_type differs from “Material Transfer”.
  - Return no value.
- Set work\_order from Platform.get\_doc(“Work Order”, self.work\_order, for\_update = true).
- Set incoming from mapping().
- For each row in self.items.
  - Set incoming at row.item\_code from (incoming.get(row.item\_code, 0.0) + flt(row.stock\_qty)).
- Evaluate work\_order.validate\_incoming\_material\_demand(incoming).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L145) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1326)

<a id="op-c2762c1926902b"></a>
### Material Request.before cancel

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate check\_on\_hold\_or\_closed\_status(self.doctype, self.name).
- Evaluate self.set\_status(update = true, status = “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0752.json#L6166) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1304)

<a id="op-ea96f21c7fa1f8"></a>
### Material Request.check modified date

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_check_modified_date`

**Inputs** self.

**Record and data access** execute query text (SELECT, Material Request).

**State and service calls** execute a supplied database query.

**Explicit failure paths** validation helper — translated “{0} {1} has been modified. Please refresh.”.format(translated self.doctype, self.name).

**Local steps**

- Set mod\_db from Platform.db.sql(query text (SELECT, Material Request), self.name).
- Set date\_diff from Platform.db.sql(“select TIMEDIFF(%s, %s)”, tuple(mod\_db at 0 at 0, cstr(self.modified))).
- If (date\_diff and date\_diff at 0 at 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in date\_diff → date\_diff at 0 at 0.
  - Call the validation error handler Platform.throw(translated “{0} {1} has been modified. Please refresh.”.format(translated self.doctype, self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1309)

<a id="op-3cf3a7dad4051e"></a>
### Material Request.update status

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_update_status`

**Inputs** self, status.

**Local steps**

- Evaluate self.check\_modified\_date().
- Evaluate self.status\_can\_change(status).
- Evaluate self.set\_status(update = true, status = status).
- Evaluate self.update\_requested\_qty().
- Evaluate self.update\_requested\_qty\_in\_job\_card().
- Evaluate self.update\_requested\_qty\_in\_work\_order().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check modified date](operations-032.md#op-ea96f21c7fa1f8), [status can change](operations-032.md#op-3216f800f6a08d), [update requested qty](operations-033.md#op-d82943adc4fbf1), [update requested qty in job card](operations-032.md#op-1b18cc92fd6133), [update requested qty in work order](operations-032.md#op-e90928f073f530).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L142) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1323)

<a id="op-3216f800f6a08d"></a>
### Material Request.status can change

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_status_can_change`

**Inputs** self, status.

**Explicit failure paths** validation helper with Platform.InvalidStatusError — translated “{0} {1} is cancelled so the action cannot be completed”.format(translated self.doctype, self.name) · validation helper with Platform.InvalidStatusError — translated “{0} {1} has not been submitted so the action cannot be completed”.format(translated self.doctype, self.name).

**Local steps**

- If (self.status and self.status equals “Cancelled”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status → self.status equals “Cancelled”.
  - If status differs from self.status.
    - Call the validation error handler Platform.throw(translated “{0} {1} is cancelled so the action cannot be completed”.format(translated self.doctype, self.name), Platform.InvalidStatusError).
- Otherwise.
  - If (self.status and self.status equals “Draft”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status → self.status equals “Draft”.
    - If status differs from “Pending”.
      - Call the validation error handler Platform.throw(translated “{0} {1} has not been submitted so the action cannot be completed”.format(translated self.doctype, self.name), Platform.InvalidStatusError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0752.json#L6665) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1317)

<a id="op-45759f00022bea"></a>
### Material Request.on cancel

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_requested\_qty\_in\_production\_plan(cancel = true).
- Evaluate self.update\_requested\_qty().
- Evaluate self.update\_requested\_qty\_in\_job\_card().
- Evaluate self.update\_requested\_qty\_in\_work\_order().
- Evaluate self.update\_prevdoc\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update requested qty in production plan](operations-033.md#op-eb9942e90d2b4f), [update requested qty](operations-033.md#op-d82943adc4fbf1), [update requested qty in job card](operations-032.md#op-1b18cc92fd6133), [update requested qty in work order](operations-032.md#op-e90928f073f530).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1312)

<a id="op-10f9dfabecea60"></a>
### Material Request.get mr items ordered qty

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_get_material_request_items_ordered_quantity`

**Inputs** self, mr\_items.

**Explicit results** mr\_items\_ordered\_qty.

**Local steps**

- Set mr\_items\_ordered\_qty from mapping().
- Set mr\_items from list of d.name for d drawn from self.get(“items”) where d.name belongs to mr\_items.
  - Draw d from self.get(“items”), keep a combination only if (d.name belongs to mr\_items).
- Set doctype, qty\_field from no value.
- If self.material\_request\_type belongs to tuple(“Material Issue”, “Material Transfer”, “Customer Provided”).
  - Set doctype from Platform.qb.DocType(“Stock Entry Detail”).
  - Set qty\_field from doctype.transfer\_qty.
- Otherwise.
  - If self.material\_request\_type equals “Manufacture”.
    - Set doctype from Platform.qb.DocType(“Work Order”).
    - Set qty\_field from Case().when((doctype.status equals “Closed” bitwise and doctype.produced\_qty &lt; doctype.qty), doctype.produced\_qty).else\_(doctype.qty).
- If (doctype and qty\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → qty\_field.
  - Set query from nested operand in the contract(nested operand in the contract).select(doctype.material\_request\_item, Sum(qty\_field)).where(((nested operand in the contract.material\_request equals nested operand in the con ….
  - Set mr\_items\_ordered\_qty from Platform.\_dict(query.run()).
- Return mr\_items\_ordered\_qty.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1310)

<a id="op-af316193324991"></a>
### Material Request.update completed qty

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_update_completed_quantity`

**Inputs** self, mr\_items = no value, update\_modified = true.

**Record and data access** read “Stock Settings” via get\_single\_value.

**State and service calls** request set\_value on d.doctype.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The total Issue / Transfer quantity {0} in Material Request {1}  cannot be greater than allowed requested qu …”.format(d.ordered\_qty, d.parent, allowed\_qty, d.item\_code) · validation helper — translated “The total Issue / Transfer quantity {0} in Material Request {1} cannot be greater than requested quantity {2 …”.format(d.ordered\_qty, d.parent, d.qty, d.item\_code).

**Local steps**

- <a id="op-af316193324991-guard-2"></a>If self.material\_request\_type equals “Purchase”.
  - Return no value.
- If not mr\_items.
  - Set mr\_items from list of d.name for d drawn from self.get(“items”).
    - Draw d from self.get(“items”).
- Set mr\_items\_ordered\_qty from self.get\_mr\_items\_ordered\_qty(mr\_items).
- Set mr\_qty\_allowance from Platform.db.get\_single\_value(“Stock Settings”, “mr\_qty\_allowance”).
- For each d in self.get(“items”).
  - Set precision from d.precision(“ordered\_qty”).
  - If d.name belongs to mr\_items.
    - If self.material\_request\_type belongs to tuple(“Material Issue”, “Material Transfer”, “Customer Provided”).
      - Set d.ordered\_qty from flt(mr\_items\_ordered\_qty.get(d.name)).
      - If mr\_qty\_allowance.
        - Set allowed\_qty from flt((d.stock\_qty + (d.stock\_qty × (mr\_qty\_allowance ÷ 100))), d.precision(“ordered\_qty”)).
        - If (d.ordered\_qty and flt(d.ordered\_qty, precision) &gt; flt(allowed\_qty, precision)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.ordered\_qty → flt(d.ordered\_qty, precision) &gt; flt(allowed\_qty, precision).
          - Call the validation error handler Platform.throw(translated “The total Issue / Transfer quantity {0} in Material Request {1}  cannot be greater than allowed requested qu …”.format(d.ordered\_qty, d.parent, allowed\_qty, d.item\_code)).
      - Otherwise.
        - If (d.ordered\_qty and flt(d.ordered\_qty, precision) &gt; flt(d.stock\_qty, precision)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.ordered\_qty → flt(d.ordered\_qty, precision) &gt; flt(d.stock\_qty, precision).
          - Call the validation error handler Platform.throw(translated “The total Issue / Transfer quantity {0} in Material Request {1} cannot be greater than requested quantity {2 …”.format(d.ordered\_qty, d.parent, d.qty, d.item\_code)).
    - Otherwise.
      - If self.material\_request\_type equals “Manufacture”.
        - Set ordered\_qty from flt(mr\_items\_ordered\_qty.get(d.name)).
        - Evaluate self.validate\_work\_order\_qty(d, ordered\_qty, mr\_qty\_allowance).
        - Set d.ordered\_qty from ordered\_qty.
    - Evaluate Platform.db.set\_value(d.doctype, d.name, “ordered\_qty”, d.ordered\_qty).
- Evaluate self.update\_per\_ordered(update\_modified).
- Evaluate self.update\_requested\_qty\_in\_work\_order().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.material\_request\_type equals “Purchase”, self.material\_request\_type = “Purchase” selects the branch that returns no value. With self.material\_request\_type = “Material Transfer”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-af316193324991-guard-2)

**Methods declared on this owner** [get mr items ordered qty](operations-032.md#op-10f9dfabecea60), [validate work order qty](operations-033.md#op-3a3fa0c679cd75), [update per ordered](operations-032.md#op-a8568b9e5174c1), [update requested qty in work order](operations-032.md#op-e90928f073f530).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “mr\_qty\_allowance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1318)

<a id="op-a8568b9e5174c1"></a>
### Material Request.update per ordered

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_materialrequest_update_per_ordered`

**Inputs** self, update\_modified = true.

**Local steps**

- Evaluate self.\_update\_percent\_field(mapping(“target\_dt” → “Material Request Item”, “target\_parent\_dt” → self.doctype, “target\_parent\_field” → “per\_ordered”, “target\_ref\_field” → “stock\_qty”, …), update\_modified).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L869) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L366)

<a id="op-e90928f073f530"></a>
### Material Request.update requested qty in work order

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_update_requested_quantity_in_work_order`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Explicit results** no value.

**Local steps**

- If (not self.work\_order or self.material\_request\_type differs from “Material Transfer”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.work\_order → self.material\_request\_type differs from “Material Transfer”.
  - Return no value.
- Set work\_order from Platform.get\_doc(“Work Order”, self.work\_order).
- Evaluate work\_order.update\_requested\_qty\_for\_required\_items().
- Evaluate work\_order.update\_picked\_qty\_for\_required\_items().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1322)

<a id="op-1b18cc92fd6133"></a>
### Material Request.update requested qty in job card

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_materialrequest_update_requested_qty_in_job_card`

**Inputs** self.

**Record and data access** resolve a document from “Job Card” via get\_doc.

**Local steps**

- If self.job\_card.
  - Evaluate Platform.get\_doc(“Job Card”, self.job\_card).set\_requested\_qty().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L870) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L367)
