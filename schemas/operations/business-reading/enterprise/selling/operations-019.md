# Sales · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales order

[Record definition](../../../../data/record-types/sales_order.json)

<a id="op-5c311bc5189601"></a>
### Make purchase order.filter items

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_purchase_order_filter_items`

**Inputs** item, supplier.

**Explicit results** true · false.

**Local steps**

- If (qty\_to\_order at item.name &gt; 0 and not is\_product\_bundle(item.item\_code) and item.name belongs to items\_to\_map and items\_to\_map at item.name equals supplier).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty\_to\_order at item.name &gt; 0 → not is\_product\_bundle(item.item\_code) → item.name belongs to items\_to\_map → items\_to\_map at item.name equals supplier.
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L557) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L54)

<a id="op-bd00737a54eda5"></a>
### Set delivery date

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_set_delivery_date`

**Inputs** items, sales\_order.

**Record and data access** read “Sales Order Item” via get\_all.

**Local steps**

- Set delivery\_dates from Platform.get\_all(“Sales Order Item”, filters = mapping(“parent” → sales\_order), fields = list(“delivery\_date”, “item\_code”)).
- Set delivery\_by\_item from Platform.\_dict().
- For each date in delivery\_dates.
  - Set delivery\_by\_item at date.item\_code from date.delivery\_date.
- For each item in items.
  - If item.product\_bundle.
    - Set item.schedule\_date from delivery\_by\_item at item.product\_bundle.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L88)

<a id="op-2fafa3d5209769"></a>
### Is product bundle

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_is_product_bundle`

**Inputs** item\_code.

**Record and data access** read “Product Bundle” via exists.

**Explicit results** Platform.db.exists(“Product Bundle”, mapping(“name” → item\_code, “disabled” → 0)).

**Local steps**

- Return Platform.db.exists(“Product Bundle”, mapping(“name” → item\_code, “disabled” → 0)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L32)

<a id="op-2ed39c8e4a8f88"></a>
### Make work orders

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_work_orders`

**Inputs** items, sales\_order, company, project = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Work Order” via get\_doc.

**State and service calls** call insert on Platform.get\_doc(doctype = “Work Order”, production\_item = i at “item\_code”, bom\_no = i.get(“bom”), qty = i at “pending\_qty”, …) · call save on work\_order.

**Explicit results** list of p.name for p drawn from out.

**Explicit failure paths** validation helper — translated “Please select BOM against item {0}”.format(i.get(“item\_code”)) · validation helper — translated “Please select Qty against item {0}”.format(i.get(“item\_code”)).

**Local steps**

- Evaluate Platform.has\_permission(“Sales Order”, “read”, sales\_order, throw = true).
- Set items from json.loads(items).get(“items”).
- Set out from list().
- For each i in items.
  - If not i.get(“bom”).
    - Call the validation error handler Platform.throw(translated “Please select BOM against item {0}”.format(i.get(“item\_code”))).
  - If not i.get(“pending\_qty”).
    - Call the validation error handler Platform.throw(translated “Please select Qty against item {0}”.format(i.get(“item\_code”))).
  - Set work\_order from Platform.get\_doc(doctype = “Work Order”, production\_item = i at “item\_code”, bom\_no = i.get(“bom”), qty = i at “pending\_qty”, …).insert().
  - Evaluate work\_order.set\_work\_order\_operations().
  - Set work\_order.flags.ignore\_mandatory from true.
  - Evaluate work\_order.save().
  - Evaluate out.append(work\_order).
- Return list of p.name for p drawn from out.
  - Draw p from out.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Sales Order”, “read”, sales\_order, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L574) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L71)

<a id="op-a99350fc5a20cd"></a>
### Make production plan

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_production_plan`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Sales Order” via get\_doc.

**State and service calls** request new\_doc for “Production Plan”.

**Explicit results** production\_plan.

**Explicit failure paths** validation helper — translated “Sales Order {0} is not available for production”.format(sales\_order.name).

**Local steps**

- Set sales\_order from Platform.get\_doc(“Sales Order”, source\_name).
- Set production\_plan from Platform.new\_doc(“Production Plan”, company = sales\_order.company, get\_items\_from = “Sales Order”, posting\_date = nowdate()).
- Set open\_so from list of data.name for data drawn from get\_sales\_orders(production\_plan).
  - Draw data from get\_sales\_orders(production\_plan).
- If sales\_order.name does not belong to open\_so.
  - Call the validation error handler Platform.throw(translated “Sales Order {0} is not available for production”.format(sales\_order.name)).
- Evaluate production\_plan.append(“sales\_orders”, mapping(“sales\_order” → sales\_order.name, “sales\_order\_date” → sales\_order.transaction\_date, “customer” → sales\_order.customer, “grand\_total” → sales\_order.base\_grand\_total)).
- Evaluate production\_plan.get\_items().
- If not production\_plan.get(“po\_items”).
  - Call the validation error handler Platform.throw(translated “Sales Order {0} is not available for production”.format(sales\_order.name)).
- Return production\_plan.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L553) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L50)

<a id="op-48b49e2f858518"></a>
### Update status

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_update_status`

**Inputs** status, name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Sales Order” via get\_doc.

**Explicit failure paths** validation helper — translated “Sales Order status cannot be set to {0}”.format(status) · validation helper — translated “Only a submitted Sales Order can be put On Hold, Closed or re-opened”.

**Local steps**

- If status does not belong to tuple(“Draft”, “On Hold”, “Closed”).
  - Call the validation error handler Platform.throw(translated “Sales Order status cannot be set to {0}”.format(status)).
- Set so from Platform.get\_doc(“Sales Order”, name, check\_permission = “submit”).
- <a id="op-48b49e2f858518-guard-6"></a>If so.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Only a submitted Sales Order can be put On Hold, Closed or re-opened”).
- Evaluate so.update\_status(status).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison so.docstatus differs from 1, so.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Only a submitted Sales Order can be put On Hold, Closed or re-opened”. With so.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-48b49e2f858518-guard-6)

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1378)

<a id="op-8bc9e0cda82cfa"></a>
### Make raw material request

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_raw_material_request`

**Inputs** items, company, sales\_order, project = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**State and service calls** msgprint with translated “Material Request not created, as quantity for Raw Materials already available.” · request new\_doc for “Material Request” · call insert on material\_request · call submit on material\_request.

**Explicit results** no value · material\_request.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If not Platform.has\_permission(“Sales Order”, “write”).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- If isinstance(items, str).
  - Set items from Platform.\_dict(json.loads(items)).
- For each item in items.get(“items”).
  - Set item at “include\_exploded\_items” from items.get(“include\_exploded\_items”).
  - Set item at “ignore\_existing\_ordered\_qty” from items.get(“ignore\_existing\_ordered\_qty”).
  - Set item at “include\_raw\_materials\_from\_sales\_order” from items.get(“include\_raw\_materials\_from\_sales\_order”).
- Evaluate items.update(mapping(“company” → company, “sales\_order” → sales\_order)).
- Set item\_wh from mapping().
- For each item in items.get(“items”).
  - If item.get(“warehouse”).
    - Set item\_wh at item.get(“item\_code”) from item.get(“warehouse”).
- Set raw\_materials from get\_items\_for\_material\_requests(items).
- If not raw\_materials.
  - Evaluate Platform.msgprint(translated “Material Request not created, as quantity for Raw Materials already available.”).
  - Return no value.
- Set material\_request from Platform.new\_doc(“Material Request”).
- Evaluate material\_request.update(dict(doctype = “Material Request”, transaction\_date = nowdate(), company = company, material\_request\_type = “Purchase”)).
- For each item in raw\_materials.
  - Set item\_doc from Platform.get\_cached\_doc(“Item”, item.get(“item\_code”)).
  - Set schedule\_date from add\_days(nowdate(), cint(item\_doc.lead\_time\_days)).
  - Set row from material\_request.append(“items”, mapping(“item\_code” → item.get(“item\_code”), “qty” → item.get(“quantity”), “uom” → item.get(“uom”), “schedule\_date” → schedule\_date, …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_wh.get(item.get(“main\_bom\_item”)) → item.get(“warehouse”).
  - If not (strip\_html(item.get(“description”)) and strip\_html(item\_doc.description)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in strip\_html(item.get(“description”)) → strip\_html(item\_doc.description).
    - Set row.description from (item\_doc.item\_name or item.get(“item\_code”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_doc.item\_name → item.get(“item\_code”).
- Evaluate material\_request.insert().
- Set material\_request.flags.ignore\_permissions from 1.
- Evaluate material\_request.run\_method(“set\_missing\_values”).
- Evaluate material\_request.submit().
- Return material\_request.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Sales Order”, “write”) · clock or generated value from nowdate() · configured or stored value from Platform.get\_cached\_doc(“Item”, item.get(“item\_code”)) · selected callable from material\_request.run\_method(“set\_missing\_values”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L561) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L58)

<a id="op-2a54235b2ea87d"></a>
### Make inter company purchase order

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_inter_company_purchase_order`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_inter\_company\_transaction(“Sales Order”, source\_name, target\_doc).

**Local steps**

- Bind dependencies make\_inter\_company\_transaction.
- Return make\_inter\_company\_transaction(“Sales Order”, source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L42)

<a id="op-d430aed7d83083"></a>
### Create pick list

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_create_pick_list`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Sales Order” via get\_doc.

**Explicit results** doc.

**Local steps**

- Bind dependencies is\_product\_bundle.
- Bind dependencies validate\_no\_reserved\_stock.
- Set source\_doc from Platform.get\_doc(“Sales Order”, source\_name).
- Set so\_items from mapping of row.name → row for row drawn from source\_doc.items.
  - Draw row from source\_doc.items.
- Bind local operation should\_pick\_packed\_item for subsequent calls.
- Bind local operation get\_packed\_qty\_to\_pick for subsequent calls.
- Bind local operation update\_item\_quantity for subsequent calls.
- Bind local operation update\_packed\_item\_qty for subsequent calls.
- Bind local operation should\_pick\_order\_item for subsequent calls.
- Evaluate validate\_no\_reserved\_stock(source\_name).
- Set doc from get\_mapped\_doc(“Sales Order”, source\_name, mapping(“Sales Order” → mapping(“doctype” → “Pick List”, “field\_map” → mapping(“set\_warehouse” → “parent\_warehouse”), “validation” → mapping(“docstatus” → list(“= ….
- Set doc.purpose from “Delivery”.
- If not doc.pick\_manually.
  - Evaluate doc.set\_item\_locations().
- Return doc.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L521) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L18)

<a id="op-ddd53338032bb9"></a>
### Create pick list.should pick packed item

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_create_pick_list_should_pick_packed_item`

**Inputs** packed\_item.

**Declared result** bool.

**Explicit results** bool((parent and parent.delivered\_by\_supplier differs from 1 and abs(parent.delivered\_qty) &lt; abs(parent.qty) and get\_packed\_qty\_to\_pick(packed\_item, parent) &gt; 0)).

**Local steps**

- Set parent from so\_items.get(packed\_item.parent\_detail\_docname).
- Return bool((parent and parent.delivered\_by\_supplier differs from 1 and abs(parent.delivered\_qty) &lt; abs(parent.qty) and get\_packed\_qty\_to\_pick(packed\_item, parent) &gt; 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent → parent.delivered\_by\_supplier differs from 1 → abs(parent.delivered\_qty) &lt; abs(parent.qty) → get\_packed\_qty\_to\_pick(packed\_item, parent) &gt; 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L524) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L21)

<a id="op-dbfeddf21b53a1"></a>
### Create pick list.get packed qty to pick

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_create_pick_list_get_packed_qty_to_pick`

**Inputs** packed\_item, parent.

**Declared result** float.

**Explicit results** flt((flt(packed\_item.qty) − max(flt(packed\_item.picked\_qty), delivered\_qty)), packed\_item.precision(“qty”)).

**Local steps**

- Set delivered\_qty from ((flt(packed\_item.qty) × flt(parent.delivered\_qty)) ÷ flt(parent.qty)).
- Return flt((flt(packed\_item.qty) − max(flt(packed\_item.picked\_qty), delivered\_qty)), packed\_item.precision(“qty”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L522) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L19)

<a id="op-93021d3bc34c08"></a>
### Create pick list.update item quantity

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_create_pick_list_update_item_quantity`

**Inputs** source, target, source\_parent.

**Declared result** no value.

**Local steps**

- Set picked\_qty from (flt(source.picked\_qty) ÷ (flt(source.conversion\_factor) or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(source.conversion\_factor) → 1.
- Set qty\_to\_be\_picked from (flt(source.qty) − max(picked\_qty, flt(source.delivered\_qty))).
- Set target.qty from qty\_to\_be\_picked.
- Set target.stock\_qty from (qty\_to\_be\_picked × flt(source.conversion\_factor)).
- Set bin\_details from \_get\_bin\_details(source.item\_code, source.warehouse, source\_parent.company).
- Set target.actual\_qty from bin\_details.get(“actual\_qty”).
- Set target.company\_total\_stock from bin\_details.get(“company\_total\_stock”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L525) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L22)

<a id="op-5472b09f4b3cb5"></a>
### Create pick list.update packed item qty

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_create_pick_list_update_packed_item_qty`

**Inputs** source, target, source\_parent.

**Declared result** no value.

**Local steps**

- Set target.qty, target.stock\_qty from get\_packed\_qty\_to\_pick(source, so\_items at source.parent\_detail\_docname).
- Set target.conversion\_factor from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L526) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L23)

<a id="op-436d1368fdd97d"></a>
### Create pick list.should pick order item

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_create_pick_list_should_pick_order_item`

**Inputs** item.

**Declared result** bool.

**Explicit results** (abs(item.delivered\_qty) &lt; abs(item.qty) and item.delivered\_by\_supplier differs from 1 and not is\_product\_bundle(item.item\_code)).

**Local steps**

- Return (abs(item.delivered\_qty) &lt; abs(item.qty) and item.delivered\_by\_supplier differs from 1 and not is\_product\_bundle(item.item\_code)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in abs(item.delivered\_qty) &lt; abs(item.qty) → item.delivered\_by\_supplier differs from 1 → not is\_product\_bundle(item.item\_code).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L523) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L20)

<a id="op-e8706ca6ca1c44"></a>
### Update produced qty in so item

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_update_produced_quantity_in_sales_order_item`

**Inputs** sales\_order, sales\_order\_item.

**Record and data access** read “Work Order” via get\_all.

**State and service calls** request set\_value on “Sales Order Item”.

**Explicit results** no value.

**Local steps**

- Set linked\_wo\_with\_so\_item from Platform.db.get\_all(“Work Order”, list(“produced\_qty”), mapping(“sales\_order\_item” → sales\_order\_item, “sales\_order” → sales\_order, “docstatus” → 1)).
- Set total\_produced\_qty from 0.
- For each wo in linked\_wo\_with\_so\_item.
  - Update total\_produced\_qty using + flt(wo.get(“produced\_qty”)).
- If (not total\_produced\_qty and Platform.flags.in\_patch).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not total\_produced\_qty → Platform.flags.in\_patch.
  - Return no value.
- Evaluate Platform.db.set\_value(“Sales Order Item”, sales\_order\_item, “produced\_qty”, total\_produced\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0643.json#L5414) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1377)

<a id="op-4a6240f0ebe028"></a>
### Get work order items

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_get_work_order_items`

**Inputs** sales\_order, for\_raw\_material\_request = 0.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Sales Order” via get\_doc · read “Product Bundle” via get\_all · read “Manufacturing Settings” via get\_single\_value.

**Explicit results** items.

**Local steps**

- Bind dependencies qty\_against\_sales\_order.
- If sales\_order.
  - Set so from Platform.get\_doc(“Sales Order”, sales\_order).
  - Evaluate so.check\_permission(“read”).
  - Set wo from qb.DocType(“Work Order”).
  - Set plan\_item from qb.DocType(“Production Plan Item”).
  - Set precision from Platform.get\_precision(“Work Order”, “qty”).
  - Set items from list().
  - Set item\_codes from list of i.item\_code for i drawn from so.items.
    - Draw i from so.items.
  - Set product\_bundle\_parents from list of pb.new\_item\_code for pb drawn from Platform.get\_all(“Product Bundle”, mapping(“new\_item\_code” → list(“in”, item\_codes), “disabled” → 0), list(“new\_item\_code”)).
    - Draw pb from Platform.get\_all(“Product Bundle”, mapping(“new\_item\_code” → list(“in”, item\_codes), “disabled” → 0), list(“new\_item\_code”)).
  - Set overproduction\_percentage\_for\_sales\_order from (Platform.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_sales\_order”) ÷ 100).
  - For each table in list(so.items, so.packed\_items).
    - For each i in table.
      - Set bom from get\_default\_bom(i.item\_code).
      - Set stock\_qty from i.qty when i.doctype equals “Packed Item”, otherwise i.stock\_qty.
        - Value choice on i.doctype equals “Packed Item” — true gives i.qty, false gives i.stock\_qty.
      - If not for\_raw\_material\_request.
        - Set total\_work\_order\_qty from flt(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0).
        - Set pending\_qty from flt((stock\_qty − total\_work\_order\_qty), precision).
      - Otherwise.
        - Set pending\_qty from stock\_qty.
      - If not pending\_qty.
        - Set pending\_qty from (stock\_qty × overproduction\_percentage\_for\_sales\_order).
      - If (pending\_qty &gt; 0 and i.item\_code does not belong to product\_bundle\_parents and bom).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in pending\_qty &gt; 0 → i.item\_code does not belong to product\_bundle\_parents → bom.
        - Evaluate items.append(dict(name = i.name, item\_code = i.item\_code, item\_name = i.item\_name, description = i.description, …)).
          - Value choice on for\_raw\_material\_request — true gives pending\_qty, false gives 0.
  - Return items.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from so.check\_permission(“read”) · configured or stored value from Platform.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_sales\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L64) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1335)

<a id="op-3c440d47148aea"></a>
### Get stock reservation status

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_get_stock_reservation_status`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Local steps**

- Return Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0644.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L63) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1334)

<a id="op-1d01e3ae68d254"></a>
### Make subcontracting inward order

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_subcontracting_inward_order`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_mapped\_subcontracting\_inward\_order(source\_name, target\_doc).

**Explicit failure paths** validation helper — translated “This Sales Order has been fully subcontracted.”.

**Local steps**

- Evaluate check\_on\_hold\_or\_closed\_status(“Sales Order”, source\_name).
- If not is\_so\_fully\_subcontracted(source\_name).
  - Return get\_mapped\_subcontracting\_inward\_order(source\_name, target\_doc).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “This Sales Order has been fully subcontracted.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L573) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L70)

<a id="op-83b2fdd79c56a5"></a>
### Is so fully subcontracted

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_is_so_fully_subcontracted`

**Inputs** so\_name.

**Explicit results** not query.run(as\_dict = true).

**Local steps**

- Set table from Platform.qb.DocType(“Sales Order Item”).
- Set query from nested operand in the contract.qb.from\_(table).select(table.name).where((table.parent equals so\_name bitwise and table.stock\_qty &gt; table.subcontracted\_qty)).
- Return not query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L33)

<a id="op-0935b7ac4a4590"></a>
### Get mapped subcontracting inward order

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_get_mapped_subcontracting_inward_order`

**Inputs** source\_name, target\_doc = no value.

**Explicit results** target\_doc.

**Local steps**

- Bind local operation post\_process for subsequent calls.
- If (target\_doc and isinstance(target\_doc, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in target\_doc → isinstance(target\_doc, str).
  - Set target\_doc from json.loads(target\_doc).
  - For each key in list(“service\_items”, “items”, “received\_items”).
    - If key belongs to target\_doc.
      - Remove target\_doc at key.
  - Set target\_doc from json.dumps(target\_doc).
- Set target\_doc from get\_mapped\_doc(“Sales Order”, source\_name, mapping(“Sales Order” → mapping(“doctype” → “Subcontracting Inward Order”, “field\_map” → mapping(), “field\_no\_map” → list(“total\_qty”, “total”, “net\_total”), “val ….
- Return target\_doc.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L529) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L26)

<a id="op-21dc943c1a32b1"></a>
### Get mapped subcontracting inward order.post process

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_get_mapped_subcontracting_inward_order_post_process`

**Inputs** source\_doc, target\_doc.

**Record and data access** read “Warehouse” via count · read “Warehouse” via get\_cached\_value.

**Local steps**

- If Platform.db.count(“Warehouse”, mapping(“customer” → source\_doc.customer, “disabled” → 0, “is\_rejected\_warehouse” → 0)) equals 1.
  - Set target\_doc.customer\_warehouse from Platform.get\_cached\_value(“Warehouse”, mapping(“customer” → source\_doc.customer, “disabled” → 0, “is\_rejected\_warehouse” → 0), “name”).
- Evaluate target\_doc.populate\_items\_table().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, mapping(“customer” → source\_doc.customer, “disabled” → 0, “is\_rejected\_warehouse” → 0), “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L530) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L27)

<a id="op-20a844eb7b7702"></a>
### Get credit note return criterion

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_get_credit_note_return_criterion`

**Inputs** invoice.

**Explicit results** ((invoice.is\_return equals 1 bitwise and invoice.update\_stock equals 1) bitwise and invoice.update\_billed\_amount\_in\_sales\_order equals 1).

**Local steps**

- Return ((invoice.is\_return equals 1 bitwise and invoice.update\_stock equals 1) bitwise and invoice.update\_billed\_amount\_in\_sales\_order equals 1).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L528) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L25)

<a id="op-775011f1fd24fd"></a>
### Get billed qty query

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_get_billed_qty_query`

**Inputs** sales\_order\_item.

**Explicit results** qb.from\_(invoice\_item).select((IfNull(Sum((nested operand in the contract × nested operand in the contract)), 0) ÷ sales\_order\_item.conversion\_factor)).where((invoice\_item.docstatus equals 1 bitwise and in ….

**Local steps**

- Set invoice\_item from qb.DocType(“Sales Invoice Item”).
- Return qb.from\_(invoice\_item).select((IfNull(Sum((nested operand in the contract × nested operand in the contract)), 0) ÷ sales\_order\_item.conversion\_factor)).where((invoice\_item.docstatus equals 1 bitwise and in ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L527) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L24)

<a id="op-5fc909f1ecf1a8"></a>
### Get pending qty criterion

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_get_pending_quantity_criterion`

**Inputs** sales\_order\_item, billed\_qty.

**Explicit results** (has\_unbilled\_ordered\_qty bitwise and has\_unbilled\_delivered\_qty).

**Local steps**

- Set invoice from qb.DocType(“Sales Invoice”).
- Set invoice\_item from qb.DocType(“Sales Invoice Item”).
- Set credit\_note\_returned\_qty from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select((IfNull(Sum((nested operand in the contract × nest ….
- Set returned\_qty from (sales\_order\_item.returned\_qty − credit\_note\_returned\_qty).
- Set qty\_precision from Platform.get\_precision(“Sales Order Item”, “qty”).
- Set has\_unbilled\_ordered\_qty from Round((sales\_order\_item.qty − billed\_qty), qty\_precision) &gt; 0.
- Set has\_unbilled\_delivered\_qty from (Round(((sales\_order\_item.qty − returned\_qty) − billed\_qty), qty\_precision) &gt; 0 bitwise or Round((sales\_order\_item.delivered\_qty − billed\_qty), qty\_precision) &gt; 0).
- Return (has\_unbilled\_ordered\_qty bitwise and has\_unbilled\_delivered\_qty).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L60) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1331)
