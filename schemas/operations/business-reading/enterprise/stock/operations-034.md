# Inventory and warehouses · operations 34

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Material request

[Record definition](../../../../data/record-types/material_request.json)

<a id="op-bfa72b91062166"></a>
### Make purchase orders by supplier

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_purchase_orders_by_supplier`

**Inputs** source\_name, item\_suppliers.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** list at str.

**State and service calls** call insert on purchase\_order · toast with translated “{0} was set to today for items whose requested date has passed”.format(translated Platform.get\_meta(“Purchase Order Item”).get\_label(“schedule\_date”)) · msgprint with translated “{0} created”.format(comma\_and(list of get\_link\_to\_form(“Purchase Order”, name) for name drawn from purchase\_orders)).

**Explicit results** purchase\_orders.

**Explicit failure paths** validation helper — translated “Select at least one Item” · validation helper — translated “Item {0} cannot be ordered more than once”.format(item\_link) · validation helper — translated “Select a Supplier for Item {0}”.format(item\_link) · validation helper — translated “Quantity for Item {0} must be greater than zero and cannot exceed {1}”.format(item\_link, Platform.bold(formatted text {pending\_qty} {(nested operand in the contract.uom or empty text)}.strip())).

**Local steps**

- Set item\_suppliers from Platform.parse\_json(item\_suppliers).
- If not item\_suppliers.
  - Call the validation error handler Platform.throw(translated “Select at least one Item”).
- Set pending\_items from mapping of d at “material\_request\_item” → Platform.\_dict(d) for d drawn from get\_item\_default\_suppliers(source\_name).
  - Draw d from get\_item\_default\_suppliers(source\_name).
- Set items\_by\_supplier from mapping().
- Set requested\_items from set().
- For each row in item\_suppliers.
  - Set row from Platform.\_dict(row).
  - Set pending from (pending\_items.get(row.material\_request\_item) or Platform.\_dict()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in pending\_items.get(row.material\_request\_item) → Platform.\_dict().
  - Set item\_link from get\_link\_to\_form(“Item”, row.item\_code).
  - If row.material\_request\_item belongs to requested\_items.
    - Call the validation error handler Platform.throw(translated “Item {0} cannot be ordered more than once”.format(item\_link)).
  - Evaluate requested\_items.add(row.material\_request\_item).
  - If not row.supplier.
    - Call the validation error handler Platform.throw(translated “Select a Supplier for Item {0}”.format(item\_link)).
  - If (flt(row.qty) ≤ 0 or flt(row.qty) &gt; flt(pending.pending\_qty)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.qty) ≤ 0 → flt(row.qty) &gt; flt(pending.pending\_qty).
    - Set pending\_qty from Platform.format\_value(flt(pending.pending\_qty), “Float”).
    - Call the validation error handler Platform.throw(translated “Quantity for Item {0} must be greater than zero and cannot exceed {1}”.format(item\_link, Platform.bold(formatted text {pending\_qty} {(nested operand in the contract or nested ope ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in pending.uom → empty text.
  - Set items\_by\_supplier.setdefault(row.supplier, mapping()) at row.material\_request\_item from flt(row.qty).
- Set purchase\_orders from list().
- Set is\_rescheduled from false.
- For each tuple(supplier, requested\_qty) in items\_by\_supplier.items().
  - Set purchase\_order from make\_purchase\_order(source\_name, args = mapping(“supplier” → supplier, “filtered\_children” → list(requested\_qty), “requested\_qty” → requested\_qty)).
  - For each item in purchase\_order.items.
    - If not item.schedule\_date.
      - Set item.schedule\_date from nowdate().
      - Set is\_rescheduled from true.
  - Evaluate purchase\_order.insert().
  - Evaluate purchase\_orders.append(purchase\_order.name).
- If is\_rescheduled.
  - Evaluate Platform.toast(translated “{0} was set to today for items whose requested date has passed”.format(translated nested operand in the contract.get\_meta(“Purchase Order Item”).get\_label(“schedule\_date”)), indi ….
- <a id="op-bfa72b91062166-guard-63"></a>If len(purchase\_orders) &gt; 1.
  - Evaluate Platform.msgprint(translated “{0} created”.format(comma\_and(list of get\_link\_to\_form(“Purchase Order”, name) for name drawn from purchase\_orders))).
    - Draw name from purchase\_orders.
- Return purchase\_orders.

**Derived branch illustrations**

- At the comparison len(purchase\_orders) &gt; 1, length of purchase\_orders = 2 selects the branch that requests a message with translated “{0} created”.format(comma\_and(list of get\_link\_to\_form(“Purchase Order”, name) for name drawn from purchase\_orders)). With length of purchase\_orders = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-bfa72b91062166-guard-63)

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L858) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L355)

<a id="op-da5123100dc105"></a>
### Make request for quotation

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_request_for_quotation`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Evaluate validate\_request\_not\_stopped(source\_name).
- Bind local operation update\_item for subsequent calls.
- Bind local operation select\_item for subsequent calls.
- Set doclist from get\_mapped\_doc(“Material Request”, source\_name, mapping(“Material Request” → mapping(“doctype” → “Request for Quotation”, “validation” → mapping(“docstatus” → list(“=”, 1), “material\_request\_type” → list(“ ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L859) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L356)

<a id="op-d2b5638cf1e8db"></a>
### Make request for quotation.update item

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_request_for_quotation_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Set qty from (obj.ordered\_qty or obj.received\_qty).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in obj.ordered\_qty → obj.received\_qty.
- Set target.qty from (flt((flt(obj.stock\_qty) − flt(qty))) ÷ target.conversion\_factor).
- Set target.stock\_qty from (target.qty × target.conversion\_factor).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L861) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L358)

<a id="op-04c789d3fcf577"></a>
### Make request for quotation.select item

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_request_for_quotation_select_item`

**Inputs** d.

**Explicit results** qty &lt; d.stock\_qty.

**Local steps**

- Set qty from (d.ordered\_qty or d.received\_qty).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.ordered\_qty → d.received\_qty.
- Return qty &lt; d.stock\_qty.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L860) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L357)

<a id="op-b6d086c2b192c7"></a>
### Make purchase order based on supplier

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_purchase_order_based_on_supplier`

**Inputs** source\_name, target\_doc = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** target\_doc.

**Local steps**

- Set mr from source\_name.
- Set supplier\_items from get\_items\_based\_on\_default\_supplier(args.get(“supplier”)).
- Bind local operation postprocess for subsequent calls.
- Set target\_doc from get\_mapped\_doc(“Material Request”, mr, mapping(“Material Request” → mapping(“doctype” → “Purchase Order”), “Material Request Item” → mapping(“doctype” → “Purchase Order Item”, “field\_map” → list(list(“name ….
- Return target\_doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L852) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L349)

<a id="op-fb44d28e1221ef"></a>
### Make purchase order based on supplier.postprocess

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_purchase_order_based_on_supplier_postprocess`

**Inputs** source, target\_doc.

**Local steps**

- Set target\_doc.supplier from args.get(“supplier”).
- If getdate(target\_doc.schedule\_date) &lt; getdate(nowdate()).
  - Set target\_doc.schedule\_date from no value.
- Evaluate target\_doc.set(“items”, list of d for d drawn from target\_doc.get(“items”) where (d.get(“item\_code”) belongs to supplier\_items and d.get(“qty”) &gt; 0)).
  - Draw d from target\_doc.get(“items”), keep a combination only if ((d.get(“item\_code”) belongs to supplier\_items and d.get(“qty”) &gt; 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“item\_code”) belongs to supplier\_items → d.get(“qty”) &gt; 0.
- Evaluate set\_missing\_values(source, target\_doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L853) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L350)

<a id="op-9b96e9cc17bd42"></a>
### Get items based on default supplier

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_get_items_based_on_default_supplier`

**Inputs** supplier.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item Default” via get\_all · read “Item” via get\_list.

**Explicit results** list() · list of item for item drawn from supplier\_items where item belongs to permitted\_items.

**Local steps**

- Evaluate Platform.has\_permission(“Item”, “select”, throw = true).
- Set supplier\_items from Platform.get\_all(“Item Default”, mapping(“default\_supplier” → supplier, “parenttype” → “Item”), pluck = “parent”).
- If not supplier\_items.
  - Return list().
- Set permitted\_items from set(Platform.get\_list(“Item”, filters = mapping(“name” → list(“in”, supplier\_items)), pluck = “name”, limit = 0)).
- Return list of item for item drawn from supplier\_items where item belongs to permitted\_items.
  - Draw item from supplier\_items, keep a combination only if (item belongs to permitted\_items).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “select”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L846) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L343)

<a id="op-ddfd9782a2b07d"></a>
### Get material requests based on supplier

`operation_enterprise_stock_record_definitions_material_request_business_behavior_get_material_remote_requests_based_on_supplier`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Material Request Item” via get\_all · read “Material Request” via get\_list.

**Explicit results** list() · nested operand in the contract(nested operand in the contract, order = nested operand in the contract).limit(cint(page\_len)).offset(cint(start)).run().

**Explicit failure paths** validation helper — translated “{0} is not the default supplier for any items.”.format(supplier).

**Local steps**

- Set supplier from filters.get(“supplier”).
- Set supplier\_items from get\_items\_based\_on\_default\_supplier(supplier).
- If not supplier\_items.
  - Call the validation error handler Platform.throw(translated “{0} is not the default supplier for any items.”.format(supplier)).
- Set mr\_filters from list(list(“material\_request\_type”, “=”, “Purchase”), list(“per\_ordered”, “&lt;”, 99.99), list(“docstatus”, “=”, 1), list(“status”, “!=”, “Stopped”), …).
- If Platform.has\_permission(“Material Request”, “read”).
  - Evaluate mr\_filters.append(list(“Material Request Item”, “item\_code”, “in”, supplier\_items)).
- Otherwise.
  - Set parents from Platform.get\_all(“Material Request Item”, filters = mapping(“item\_code” → tuple(“in”, supplier\_items), “parenttype” → “Material Request”), pluck = “parent”, distinct = true).
  - Evaluate mr\_filters.append(list(“name”, “in”, (parents or list(empty text)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parents → list(empty text).
- If txt.
  - Evaluate mr\_filters.append(list(“name”, “like”, formatted text %{txt}%)).
- If filters.get(“transaction\_date”).
  - Set date from filters.get(“transaction\_date”) at 1.
  - Evaluate mr\_filters.append(list(“transaction\_date”, “between”, list(date at 0, date at 1))).
- Set permitted from Platform.get\_list(“Material Request”, filters = mr\_filters, pluck = “name”, order\_by = empty text, limit\_page\_length = 0).
- If not permitted.
  - Return list().
- Set mr from Platform.qb.DocType(“Material Request”).
- Set mr\_item from Platform.qb.DocType(“Material Request Item”).
- Return nested operand in the contract(nested operand in the contract, order = nested operand in the contract).limit(cint(page\_len)).offset(cint(start)).run().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Material Request”, “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1302)

<a id="op-e3e0ca0a416c76"></a>
### Make supplier quotation

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_supplier_quotation`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Evaluate validate\_request\_not\_stopped(source\_name).
- Bind local operation postprocess for subsequent calls.
- Set doclist from get\_mapped\_doc(“Material Request”, source\_name, mapping(“Material Request” → mapping(“doctype” → “Supplier Quotation”, “validation” → mapping(“docstatus” → list(“=”, 1), “material\_request\_type” → list(“=”, ….
- Evaluate doclist.set\_onload(“load\_after\_mapping”, false).
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L865) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L362)

<a id="op-3b538086f45a3a"></a>
### Make supplier quotation.postprocess

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_supplier_quotation_postprocess`

**Inputs** source, target\_doc.

**Local steps**

- Evaluate set\_missing\_values(source, target\_doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L866) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L363)

<a id="op-bbcbe96ba644a2"></a>
### Make stock entry

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_stock_entry`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Evaluate validate\_request\_not\_stopped(source\_name).
- Bind local operation update\_item for subsequent calls.
- Bind local operation set\_missing\_values for subsequent calls.
- Set doclist from get\_mapped\_doc(“Material Request”, source\_name, mapping(“Material Request” → mapping(“doctype” → “Stock Entry”, “validation” → mapping(“docstatus” → list(“=”, 1), “material\_request\_type” → list(“in”, list( ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L862) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L359)

<a id="op-1dcd7a1f4d5044"></a>
### Make stock entry.update item

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_stock_entry_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Set qty from (flt((flt(obj.stock\_qty) − flt(obj.ordered\_qty))) ÷ target.conversion\_factor) when flt(obj.stock\_qty) &gt; flt(obj.ordered\_qty), otherwise 0.
  - Value choice on flt(obj.stock\_qty) &gt; flt(obj.ordered\_qty) — true gives (flt((flt(obj.stock\_qty) − flt(obj.ordered\_qty))) ÷ target.conversion\_factor), false gives 0.
- Set target.qty from qty.
- Set target.transfer\_qty from (qty × obj.conversion\_factor).
- Set target.conversion\_factor from obj.conversion\_factor.
- If (source\_parent.material\_request\_type equals “Material Transfer” or source\_parent.material\_request\_type equals “Customer Provided”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_parent.material\_request\_type equals “Material Transfer” → source\_parent.material\_request\_type equals “Customer Provided”.
  - Set target.t\_warehouse from obj.warehouse.
- Otherwise.
  - Set target.s\_warehouse from obj.warehouse.
- If source\_parent.material\_request\_type equals “Customer Provided”.
  - Set target.allow\_zero\_valuation\_rate from 1.
- If source\_parent.material\_request\_type equals “Material Transfer”.
  - Set target.s\_warehouse from obj.from\_warehouse.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L864) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L361)

<a id="op-9d8c329f818ced"></a>
### Make stock entry.set missing values

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_stock_entry_set_missing_values`

**Inputs** source, target.

**Record and data access** read “Job Card” via get\_all · read “Work Order” via get\_value.

**Local steps**

- Set target.purpose from source.material\_request\_type.
- Set target.from\_warehouse from source.set\_from\_warehouse.
- Set target.to\_warehouse from source.set\_warehouse.
- If source.material\_request\_type equals “Material Issue”.
  - Set target.from\_warehouse from source.set\_warehouse.
  - Set target.to\_warehouse from no value.
- If source.job\_card.
  - Set target.purpose from “Material Transfer for Manufacture”.
- If source.work\_order.
  - Set target.purpose from “Material Transfer for Manufacture”.
- If source.material\_request\_type equals “Customer Provided”.
  - Set target.purpose from “Material Receipt”.
- Evaluate target.set\_transfer\_qty().
- Evaluate target.set\_actual\_qty().
- Evaluate target.calculate\_rate\_and\_amount(raise\_error\_if\_no\_rate = false).
- Set target.stock\_entry\_type from target.purpose.
- Evaluate target.set\_job\_card\_data().
- If source.job\_card.
  - Set job\_card\_details from Platform.get\_all(“Job Card”, filters = mapping(“name” → source.job\_card), fields = list(“bom\_no”, “for\_quantity”)).
  - If (job\_card\_details and job\_card\_details at 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in job\_card\_details → job\_card\_details at 0.
    - Set target.bom\_no from job\_card\_details at 0.bom\_no.
    - Set target.fg\_completed\_qty from job\_card\_details at 0.for\_quantity.
    - Set target.from\_bom from 1.
- If source.work\_order.
  - Set work\_order\_details from Platform.db.get\_value(“Work Order”, source.work\_order, list(“bom\_no”, “use\_multi\_level\_bom”), as\_dict = true).
  - If work\_order\_details.
    - Set target.bom\_no from work\_order\_details.bom\_no.
    - Set target.use\_multi\_level\_bom from work\_order\_details.use\_multi\_level\_bom.
    - Set target.from\_bom from 1.
    - If not source.job\_card.
      - Set target.fg\_completed\_qty from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L863) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L360)

<a id="op-c9c6699e4120d7"></a>
### Raise work orders

`operation_enterprise_stock_record_definitions_material_request_business_behavior_raise_work_orders`

**Inputs** material\_request, company.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Material Request” via get\_doc · read “Company” via get\_cached\_value · read “BOM” via exists · read “Item” via get\_value.

**State and service calls** request new\_doc for “Work Order” · call save on wo\_order.

**Explicit results** work\_orders.

**Explicit failure paths** validation helper — translated “Material Request must be submitted to create Work Orders” · validation helper — translated “Cannot create Work Orders from a stopped Material Request” · validation helper — translated “Work Order cannot be created for following reason: &lt;br&gt; {0}”.format(new\_line\_sep(errors)).

**Local steps**

- Set mr from Platform.get\_doc(“Material Request”, material\_request).
- Evaluate mr.check\_permission(“read”).
- <a id="op-c9c6699e4120d7-guard-4"></a>If mr.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Material Request must be submitted to create Work Orders”).
- Evaluate mr.validate\_value(“material\_request\_type”, “=”, “Manufacture”).
- If mr.status equals “Stopped”.
  - Call the validation error handler Platform.throw(translated “Cannot create Work Orders from a stopped Material Request”).
- Set errors from list().
- Set work\_orders from list().
- Set default\_wip\_warehouse from Platform.get\_cached\_value(“Company”, company, “default\_wip\_warehouse”).
- Set draft\_qty from get\_draft\_work\_order\_qty(mr.name).
- For each d in mr.items.
  - Set pending\_qty from flt(((d.stock\_qty − d.ordered\_qty) − flt(draft\_qty.get(d.name))), d.precision(“stock\_qty”)).
  - If pending\_qty &gt; 0.
    - If (Platform.db.exists(“BOM”, mapping(“item” → d.item\_code, “is\_default” → 1, “is\_active” → 1)) or (variant\_of bound to Platform.get\_value(“Item”, d.item\_code, “variant\_of”) and Platform.db.exists(“BOM”, mapp ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.exists(“BOM”, mapping(“item” → d.item\_code, “is\_default” → 1, “is\_active” → 1)) → (variant\_of bound to Platform.get\_value(“Item”, d.item\_code, “variant\_of”) and Platform.db.exists(“BOM”, mapping(“item” → variant\_of, “is\_default” → 1, “is\_active” → 1))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in variant\_of bound to Platform.get\_value(“Item”, d.item\_code, “variant\_of”) → Platform.db.exists(“BOM”, mapping(“item” → variant\_of, “is\_default” → 1, “is\_active” → 1)).
      - Set wo\_order from Platform.new\_doc(“Work Order”).
      - Evaluate wo\_order.update(mapping(“production\_item” → d.item\_code, “qty” → pending\_qty, “fg\_warehouse” → d.warehouse, “wip\_warehouse” → default\_wip\_warehouse, …)).
      - Evaluate wo\_order.get\_items\_and\_operations\_from\_bom().
      - Set wo\_order.flags.ignore\_validate from true.
      - Set wo\_order.flags.ignore\_mandatory from true.
      - Evaluate wo\_order.save().
      - Evaluate work\_orders.append(wo\_order.name).
    - Otherwise.
      - Evaluate errors.append(translated “Row {0}: Bill of Materials not found for the Item {1}”.format(d.idx, get\_link\_to\_form(“Item”, d.item\_code))).
- If work\_orders.
  - Set work\_orders\_list from list of get\_link\_to\_form(“Work Order”, d) for d drawn from work\_orders.
    - Draw d from work\_orders.
  - If len(work\_orders) &gt; 1.
    - Evaluate msgprint(translated “The following {0} were created: {1}”.format(Platform.bold(translated “Work Orders”), (text in the contract + “, ”.join(work\_orders\_list)))).
  - Otherwise.
    - Evaluate msgprint(translated “The {0} {1} created successfully”.format(Platform.bold(translated “Work Order”), work\_orders\_list at 0)).
- If errors.
  - Call the validation error handler Platform.throw(translated “Work Order cannot be created for following reason: &lt;br&gt; {0}”.format(new\_line\_sep(errors))).
- Return work\_orders.

**Derived branch illustrations**

- At the comparison mr.docstatus differs from 1, mr.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Material Request must be submitted to create Work Orders”. With mr.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c9c6699e4120d7-guard-4)

**Values supplied outside this operation** effective access from mr.check\_permission(“read”) · configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_wip\_warehouse”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L149) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1330)

<a id="op-422e38975993e2"></a>
### Create pick list

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_create_pick_list`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doc.

**Local steps**

- Evaluate validate\_request\_not\_stopped(source\_name).
- Bind local operation update\_item for subsequent calls.
- Set doc from get\_mapped\_doc(“Material Request”, source\_name, mapping(“Material Request” → mapping(“doctype” → “Pick List”, “field\_map” → mapping(“material\_request\_type” → “purpose”), “validation” → mapping(“docstatus”  ….
- If not doc.pick\_manually.
  - Evaluate doc.set\_item\_locations().
- Return doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L841) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L338)

<a id="op-e30ee0de9148fe"></a>
### Create pick list.update item

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_create_pick_list_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Set qty from flt((get\_pending\_pick\_qty(obj) ÷ target.conversion\_factor), obj.precision(“qty”)).
- Set target.qty from qty.
- Set target.stock\_qty from (qty × obj.conversion\_factor).
- Set target.conversion\_factor from obj.conversion\_factor.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L842) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L339)

<a id="op-56ea91492ef70f"></a>
### Make in transit stock entry

`operation_enterprise_binding_enterprise_stock_doctype_material_request_material_request_make_in_transit_stock_entry`

**Inputs** source\_name, in\_transit\_warehouse.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** ste\_doc.

**Local steps**

- Set ste\_doc from make\_stock\_entry(source\_name).
- Set ste\_doc.add\_to\_transit from 1.
- Set ste\_doc.to\_warehouse from in\_transit\_warehouse.
- For each row in ste\_doc.items.
  - Set row.t\_warehouse from in\_transit\_warehouse.
- Return ste\_doc.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L850) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L347)

<a id="op-ede185d44f813d"></a>
### Get data

`operation_enterprise_stock_record_definitions_material_request_material_request_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “material\_request”, “internal\_links” → mapping(“Sales Order” → list(“items”, “sales\_order”), “Project” → list(“items”, “project”), “Cost Center” → list(“items”, “cost\_center”)), “tran ….

**Local steps**

- Return mapping(“fieldname” → “material\_request”, “internal\_links” → mapping(“Sales Order” → list(“items”, “sales\_order”), “Project” → list(“items”, “project”), “Cost Center” → list(“items”, “cost\_center”)), “tran ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0754.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L176) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1334)

## Record · Material request item

[Record definition](../../../../data/record-types/material_request_item.json)

<a id="op-a715e43db28235"></a>
### On doctype update

`operation_enterprise_stock_record_definitions_material_request_item_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Material Request Item”.

**Local steps**

- Evaluate Platform.db.add\_index(“Material Request Item”, list(“item\_code”, “warehouse”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0757.json#L7443) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L152) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1333)

## Report · Negative batch report

<a id="op-eb7377ae54dba6"></a>
### Execute

`operation_enterprise_stock_report_negative_batch_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0898.json#L1796) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L238)

<a id="op-8336711d087842"></a>
### Get columns

`operation_enterprise_stock_report_negative_batch_report_business_behavior_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(mapping(“label” → translated “Posting Datetime”, “fieldname” → “posting\_date”, “fieldtype” → “Datetime”, “width” → 160), mapping(“label” → translated “Batch No”, “fieldname” → “batch\_no”, “fieldtype”  ….

**Local steps**

- Return list(mapping(“label” → translated “Posting Datetime”, “fieldname” → “posting\_date”, “fieldtype” → “Datetime”, “width” → 160), mapping(“label” → translated “Batch No”, “fieldname” → “batch\_no”, “fieldtype”  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L617) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L240)

<a id="op-f141888a6dd23a"></a>
### Get data

`operation_enterprise_stock_report_negative_batch_report_business_behavior_get_data`

**Inputs** filters.

**Declared result** list at dict.

**Explicit results** batch\_negative\_data.

**Local steps**

- Set batches from get\_batches(filters).
- Set batch\_negative\_data from list().
- Set flt\_precision from (Platform.db.get\_default(“float\_precision”) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_default(“float\_precision”) → 2.
- Set distinct\_batches from set().
- Set warehouses from get\_warehouses(filters).
- For each \_warehouse in warehouses.
  - For each batch in batches.
    - Set tuple(\_c, data) from stock\_ledger\_execute(Platform.\_dict(mapping(“batch\_no” → batch, “from\_date” → add\_to\_date(today(), years = negative 12), “to\_date” → today(), “warehouse” → \_warehouse.name, …))).
    - Set previous\_qty from 0.
    - For each row in data.
      - Set key from tuple(row.get(“warehouse”), batch).
      - If key belongs to distinct\_batches.
        - Continue with the next iteration or loop test.
      - If flt(row.get(“qty\_after\_transaction”), flt\_precision) &lt; 0.
        - Evaluate batch\_negative\_data.append(mapping(“posting\_date” → row.get(“date”), “batch\_no” → row.get(“batch\_no”), “item\_code” → row.get(“item\_code”), “item\_name” → row.get(“item\_name”), …)).
        - Evaluate distinct\_batches.add(key).
      - Set previous\_qty from row.get(“qty\_after\_transaction”).
- Return batch\_negative\_data.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0898.json#L2824) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L618) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L241)

<a id="op-e5aca9c0b973ea"></a>
### Get warehouses

`operation_enterprise_stock_report_negative_batch_report_business_behavior_get_warehouses`

**Inputs** filters.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** Platform.get\_all(“Warehouse”, fields = list(“name”, “company”), filters = warehouse\_filters).

**Local steps**

- Set warehouse\_filters from mapping(“disabled” → 0, “is\_group” → 0).
- If filters.get(“company”).
  - Set warehouse\_filters at “company” from filters at “company”.
- If filters.get(“warehouse”).
  - Set warehouse\_filters at “name” from filters at “warehouse”.
- Return Platform.get\_all(“Warehouse”, fields = list(“name”, “company”), filters = warehouse\_filters).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0898.json#L3822) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L619) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L242)

<a id="op-80e84e8c8b4c9e"></a>
### Get batches

`operation_enterprise_stock_report_negative_batch_report_business_behavior_get_batches`

**Inputs** filters.

**Record and data access** read “Batch” via get\_all.

**Explicit results** Platform.get\_all(“Batch”, pluck = “name”, filters = batch\_filters).

**Local steps**

- Set batch\_filters from mapping().
- If filters.get(“item\_code”).
  - Set batch\_filters at “item” from filters at “item\_code”.
- Return Platform.get\_all(“Batch”, pluck = “name”, filters = batch\_filters).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0898.json#L4103) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L239)
