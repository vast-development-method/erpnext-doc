# Inventory and warehouses · operations 40

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pick list

[Record definition](../../../../data/record-types/pick_list.json)

<a id="op-3034d9bf30e128"></a>
### Validate no reserved stock

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_validate_no_reserved_stock`

**Inputs** sales\_order.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Cannot create a pick list for Sales Order {0} because it has reserved stock. Please unreserve the stock in o …”.format(Platform.bold(sales\_order)).

**Local steps**

- Bind dependencies get\_sre\_reserved\_qty\_details\_for\_voucher.
- If get\_sre\_reserved\_qty\_details\_for\_voucher(“Sales Order”, sales\_order).
  - Call the validation error handler Platform.throw(translated “Cannot create a pick list for Sales Order {0} because it has reserved stock. Please unreserve the stock in o …”.format(Platform.bold(sales\_order))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L218) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L966) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L463)

<a id="op-9161c967c2f26c"></a>
### Update pick list status

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_update_pick_list_status`

**Inputs** pick\_list.

**Record and data access** resolve a document from “Pick List” via get\_doc.

**Local steps**

- If pick\_list.
  - Set doc from Platform.get\_doc(“Pick List”, pick\_list).
  - Evaluate doc.update\_bundle\_delivered\_qty().
  - Evaluate doc.run\_method(“update\_status”).
  - Evaluate doc.update\_picked\_qty\_in\_work\_order().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from doc.run\_method(“update\_status”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0764.json#L4747) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L124)

<a id="op-c84a5cc0882189"></a>
### Is live material request

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_is_live_material_request`

**Inputs** material\_request.

**Record and data access** read “Material Request” via get\_value.

**Explicit results** false · (docstatus equals 1 and status differs from “Stopped”).

**Local steps**

- If not material\_request.
  - Return false.
- Set tuple(docstatus, status) from Platform.db.get\_value(“Material Request”, material\_request, list(“docstatus”, “status”)).
- Return (docstatus equals 1 and status differs from “Stopped”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in docstatus equals 1 → status differs from “Stopped”.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0764.json#L4885) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L70)

<a id="op-ef3aecf7059815"></a>
### Get picked items qty

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_picked_items_quantity`

**Inputs** items, contains\_packed\_items = false.

**Declared result** list at dict.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set pi\_item from Platform.qb.DocType(“Pick List Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(pi\_item.sales\_order\_item, pi\_item.product\_bundle\_item, pi\_item.item\_code, pi\_item.sales\_order, …).where(pi\_item.docstatus equals 1).for\_update().
- If contains\_packed\_items.
  - Set query from query.groupby(pi\_item.product\_bundle\_item, pi\_item.sales\_order).where(pi\_item.product\_bundle\_item.isin(items)).
- Otherwise.
  - Set query from query.groupby(pi\_item.sales\_order\_item, pi\_item.sales\_order).where(pi\_item.sales\_order\_item.isin(items)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L314) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L68)

<a id="op-8c42a7bf04015d"></a>
### Validate item locations

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_validate_item_locations`

**Inputs** pick\_list.

**Explicit failure paths** validation helper — translated “Add items in the Item Locations table”.

**Local steps**

- If not pick\_list.locations.
  - Call the validation error handler Platform.throw(translated “Add items in the Item Locations table”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L217) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L965) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L462)

<a id="op-51466ce564c14a"></a>
### Get whole bundle count

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_whole_bundle_count`

**Inputs** qty, qty\_per\_bundle.

**Declared result** int.

**Explicit results** bundles.

**Local steps**

- Set precision from Platform.get\_precision(“Packed Item”, “qty”).
- Set qty from flt(qty, precision).
- Set bundles from int((qty ÷ sum(qty\_per\_bundle))).
- While get\_packed\_bundle\_qty((bundles + 1), qty\_per\_bundle, precision) ≤ qty.
  - Update bundles using + 1.
- While (bundles and get\_packed\_bundle\_qty(bundles, qty\_per\_bundle, precision) &gt; qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bundles → get\_packed\_bundle\_qty(bundles, qty\_per\_bundle, precision) &gt; qty.
  - Update bundles using − 1.
- Return bundles.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L193) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L941) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L438)

<a id="op-c8a11469b72326"></a>
### Get packed bundle qty

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_packed_bundle_qty`

**Inputs** bundles, qty\_per\_bundle, precision.

**Declared result** float.

**Explicit results** sum(generator of flt((bundles × qty\_per\_unit), precision) for qty\_per\_unit drawn from qty\_per\_bundle).

**Local steps**

- Return sum(generator of flt((bundles × qty\_per\_unit), precision) for qty\_per\_unit drawn from qty\_per\_bundle).
  - Draw qty\_per\_unit from qty\_per\_bundle.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L187) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L935) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L432)

<a id="op-21b069232005ca"></a>
### Get items with location and quantity

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_items_with_location_and_quantity`

**Inputs** item\_doc, item\_location\_map, docstatus.

**Record and data access** read “UOM” via get\_cached\_value.

**Explicit results** locations.

**Local steps**

- Set available\_locations from item\_location\_map.get(item\_doc.item\_code).
- Set locations from list().
- Set remaining\_stock\_qty from item\_doc.qty when (docstatus equals 1 and item\_doc.stock\_qty equals 0), otherwise item\_doc.stock\_qty.
  - Value choice on (docstatus equals 1 and item\_doc.stock\_qty equals 0) — true gives item\_doc.qty, false gives item\_doc.stock\_qty.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in docstatus equals 1 → item\_doc.stock\_qty equals 0.
- Set precision from Platform.get\_precision(“Pick List Item”, “qty”).
- While (flt(remaining\_stock\_qty, precision) &gt; 0 and available\_locations).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(remaining\_stock\_qty, precision) &gt; 0 → available\_locations.
  - Set item\_location from available\_locations.pop(0).
  - Set item\_location from Platform.\_dict(item\_location).
  - Set stock\_qty from remaining\_stock\_qty when item\_location.qty ≥ remaining\_stock\_qty, otherwise item\_location.qty.
    - Value choice on item\_location.qty ≥ remaining\_stock\_qty — true gives remaining\_stock\_qty, false gives item\_location.qty.
  - Set qty from (stock\_qty ÷ (item\_doc.conversion\_factor or 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_doc.conversion\_factor → 1.
  - Set uom\_must\_be\_whole\_number from Platform.get\_cached\_value(“UOM”, item\_doc.uom, “must\_be\_whole\_number”).
  - If uom\_must\_be\_whole\_number.
    - Set qty from floor(qty).
    - Set stock\_qty from (qty × item\_doc.conversion\_factor).
    - If not stock\_qty.
      - Continue with the next iteration or loop test.
  - Set serial\_nos from no value.
  - If item\_location.serial\_nos.
    - Set serial\_nos from whitespace '\\n'.join(item\_location.serial\_nos at slice 0 to cint(stock\_qty)).
  - Evaluate locations.append(Platform.\_dict(mapping(“qty” → qty, “stock\_qty” → stock\_qty, “warehouse” → item\_location.warehouse, “serial\_no” → serial\_nos, …))).
  - Update remaining\_stock\_qty using − stock\_qty.
  - Set qty\_diff from (item\_location.qty − stock\_qty).
  - If qty\_diff &gt; 0.
    - Set item\_location.qty from qty\_diff.
    - If item\_location.serial\_nos.
      - Set item\_location.serial\_nos from item\_location.serial\_nos at slice cint(stock\_qty) to no value.
    - Set available\_locations from list(item\_location, expanded available\_locations).
- Set item\_location\_map at item\_doc.item\_code from available\_locations.
- Return locations.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, item\_doc.uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L64)

<a id="op-75e65e79ed50d6"></a>
### Get delivered sales order item query

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_delivered_sales_order_item_query`

**Inputs** pi\_item.

**Explicit results** nested operand in the contract.qb.from\_(so\_item).select(so\_item.name).where((so\_item.name equals pi\_item.sales\_order\_item bitwise and so\_item.delivered\_qty ≥ so\_item.qty)).

**Local steps**

- Set so\_item from Platform.qb.DocType(“Sales Order Item”).
- Return nested operand in the contract.qb.from\_(so\_item).select(so\_item.name).where((so\_item.name equals pi\_item.sales\_order\_item bitwise and so\_item.delivered\_qty ≥ so\_item.qty)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L929) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L426)

<a id="op-6ae3e5f88b85d2"></a>
### Get uom conversion factors

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_uom_conversion_factors`

**Inputs** item\_codes.

**Declared result** dict.

**Record and data access** read “UOM Conversion Detail” via get\_all.

**Explicit results** mapping() · mapping of tuple(row.parent, row.uom) → flt(row.conversion\_factor) for row drawn from Platform.get\_all(“UOM Conversion Detail”, filters = mapping(“parent” → tuple(“in”, list(item\_codes)), “parenttype” → “I ….

**Local steps**

- If not item\_codes.
  - Return mapping().
- Return mapping of tuple(row.parent, row.uom) → flt(row.conversion\_factor) for row drawn from Platform.get\_all(“UOM Conversion Detail”, filters = mapping(“parent” → tuple(“in”, list(item\_codes)), “parenttype” → “I ….
  - Draw row from Platform.get\_all(“UOM Conversion Detail”, filters = mapping(“parent” → tuple(“in”, list(item\_codes)), “parenttype” → “Item”), fields = list(“parent”, “uom”, “conversion\_factor”)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L192) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L940) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L437)

<a id="op-3a803f737cea4c"></a>
### Get available item locations

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_available_item_locations`

**Inputs** item\_code, from\_warehouses, required\_qty, company, ignore\_validation = false, picked\_item\_details = no value, consider\_rejected\_warehouses = false, priority\_warehouses = no value, keep\_all\_locations = false, exclude\_warehouses = no value, own\_vouchers = no value.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** locations.

**Local steps**

- Set locations from list().
- Set has\_serial\_no from Platform.get\_cached\_value(“Item”, item\_code, “has\_serial\_no”).
- Set has\_batch\_no from Platform.get\_cached\_value(“Item”, item\_code, “has\_batch\_no”).
- If (has\_batch\_no and has\_serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_batch\_no → has\_serial\_no.
  - Set locations from get\_available\_item\_locations\_for\_serial\_and\_batched\_item(item\_code, from\_warehouses, required\_qty, company, consider\_rejected\_warehouses = consider\_rejected\_warehouses).
- Otherwise.
  - If has\_serial\_no.
    - Set locations from get\_available\_item\_locations\_for\_serialized\_item(item\_code, from\_warehouses, company, consider\_rejected\_warehouses = consider\_rejected\_warehouses).
  - Otherwise.
    - If has\_batch\_no.
      - Set locations from get\_available\_item\_locations\_for\_batched\_item(item\_code, from\_warehouses, company, consider\_rejected\_warehouses = consider\_rejected\_warehouses).
    - Otherwise.
      - Set locations from get\_available\_item\_locations\_for\_other\_item(item\_code, from\_warehouses, company, consider\_rejected\_warehouses = consider\_rejected\_warehouses).
- If exclude\_warehouses.
  - Set locations from list of location for location drawn from locations where location.warehouse does not belong to exclude\_warehouses.
    - Draw location from locations, keep a combination only if (location.warehouse does not belong to exclude\_warehouses).
- If picked\_item\_details.
  - Set locations from filter\_locations\_by\_picked\_materials(locations, picked\_item\_details).
- If has\_serial\_no.
  - Set locations from remove\_serial\_nos\_reserved\_for\_others(item\_code, locations, own\_vouchers).
- If (locations and keep\_all\_locations).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in locations → keep\_all\_locations.
  - Set locations from prioritize\_locations(locations, priority\_warehouses).
- Otherwise.
  - If locations.
    - Set locations from get\_locations\_based\_on\_required\_qty(locations, required\_qty, priority\_warehouses).
- If not ignore\_validation.
  - Evaluate validate\_picked\_materials(item\_code, required\_qty, locations, picked\_item\_details).
- Return locations.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “has\_serial\_no”), Platform.get\_cached\_value(“Item”, item\_code, “has\_batch\_no”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L299) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L58)

<a id="op-1e5a180431ebd1"></a>
### Prioritize locations

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_prioritize_locations`

**Inputs** locations, priority\_warehouses.

**Explicit results** locations · (priority\_locations + fallback\_locations).

**Local steps**

- If not priority\_warehouses.
  - Return locations.
- Set priority\_locations from list of loc for loc drawn from locations where loc.warehouse belongs to priority\_warehouses.
  - Draw loc from locations, keep a combination only if (loc.warehouse belongs to priority\_warehouses).
- Set fallback\_locations from list of loc for loc drawn from locations where loc.warehouse does not belong to priority\_warehouses.
  - Draw loc from locations, keep a combination only if (loc.warehouse does not belong to priority\_warehouses).
- Return (priority\_locations + fallback\_locations).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L205) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L953) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L450)

<a id="op-4f3781527d232a"></a>
### Get locations based on required qty

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_locations_based_on_required_quantity`

**Inputs** locations, required\_qty, priority\_warehouses.

**Explicit results** filtered\_locations.

**Local steps**

- Set filtered\_locations from list().
- For each location in prioritize\_locations(locations, priority\_warehouses).
  - If location.qty ≥ required\_qty.
    - Set location.qty from required\_qty.
    - Evaluate filtered\_locations.append(location).
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Update required\_qty using − location.qty.
  - Evaluate filtered\_locations.append(location).
- Return filtered\_locations.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L65)

<a id="op-0162a3667b11af"></a>
### Validate picked materials

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_validate_picked_materials`

**Inputs** item\_code, required\_qty, locations, picked\_item\_details = no value.

**State and service calls** msgprint with translated “{0} units of Item {1} is not available in any of the warehouses. Other Pick Lists exist for this item.”.format(remaining\_qty, get\_link\_to\_form(“Item”, item\_code)) · msgprint with translated “{0} units of Item {1} is not available in any of the warehouses.”.format(remaining\_qty, get\_link\_to\_form(“Item”, item\_code)).

**Local steps**

- For each location in list(locations).
  - If location at “qty” &lt; 0.
    - Evaluate locations.remove(location).
- Set total\_qty\_available from sum(generator of location.get(“qty”) for location drawn from locations).
  - Draw location from locations.
- Set remaining\_qty from (required\_qty − total\_qty\_available).
- If remaining\_qty &gt; 0.
  - If picked\_item\_details.
    - Evaluate Platform.msgprint(translated “{0} units of Item {1} is not available in any of the warehouses. Other Pick Lists exist for this item.”.format(remaining\_qty, get\_link\_to\_form(“Item”, item\_code)), title = tra ….
  - Otherwise.
    - Evaluate Platform.msgprint(translated “{0} units of Item {1} is not available in any of the warehouses.”.format(remaining\_qty, get\_link\_to\_form(“Item”, item\_code)), title = translated “Insufficient Stock”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L125)

<a id="op-dd831cf1feb8c1"></a>
### Filter locations by picked materials

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_filter_locations_by_picked_materials`

**Inputs** locations, picked\_item\_details.

**Declared result** list at dict.

**Explicit results** filterd\_locations.

**Local steps**

- Set filterd\_locations from list().
- Set precision from Platform.get\_precision(“Pick List Item”, “qty”).
- For each row in locations.
  - Set key from row.warehouse.
  - If row.batch\_no.
    - Set key from tuple(row.warehouse, row.batch\_no).
  - Set picked\_qty from picked\_item\_details.get(key, mapping()).get(“picked\_qty”, 0).
  - If not picked\_qty.
    - Evaluate filterd\_locations.append(row).
    - Continue with the next iteration or loop test.
  - If picked\_qty &gt; row.qty.
    - Update picked\_item\_details at key at “picked\_qty” using − row.qty.
    - Set row.qty from 0.
  - Otherwise.
    - Update row.qty using − picked\_qty.
    - Set picked\_item\_details at key at “picked\_qty” from 0.0.
    - If row.serial\_nos.
      - Set picked\_serial\_nos from set((picked\_item\_details at key.get(“serial\_no”) or list())).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in picked\_item\_details at key.get(“serial\_no”) → list().
      - Set row.serial\_nos from list of serial\_no for serial\_no drawn from row.serial\_nos where serial\_no does not belong to picked\_serial\_nos.
        - Draw serial\_no from row.serial\_nos, keep a combination only if (serial\_no does not belong to picked\_serial\_nos).
  - If flt(row.qty, precision) &gt; 0.
    - Evaluate filterd\_locations.append(row).
- Return filterd\_locations.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0765.json#L4232) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L56)

<a id="op-b170f870de20e9"></a>
### Remove serial nos reserved for others

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_remove_serial_nos_reserved_for_others`

**Inputs** item\_code, locations, own\_vouchers = no value.

**Explicit results** locations · list of location for location drawn from locations where location.qty &gt; 0.

**Local steps**

- Set reserved\_serial\_nos from set of row.serial\_no for row drawn from get\_reserved\_serial\_nos\_for\_sre(Platform.\_dict(item\_code = item\_code)) where row.voucher\_no does not belong to (own\_vouchers or tuple()).
  - Draw row from get\_reserved\_serial\_nos\_for\_sre(Platform.\_dict(item\_code = item\_code)), keep a combination only if (row.voucher\_no does not belong to (own\_vouchers or tuple())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in own\_vouchers → tuple().
- If not reserved\_serial\_nos.
  - Return locations.
- For each location in locations.
  - Set serial\_nos from list of sn for sn drawn from location.serial\_nos where sn does not belong to reserved\_serial\_nos.
    - Draw sn from location.serial\_nos, keep a combination only if (sn does not belong to reserved\_serial\_nos).
  - Update location.qty using − (len(location.serial\_nos) − len(serial\_nos)).
  - Set location.serial\_nos from serial\_nos.
- Return list of location for location drawn from locations where location.qty &gt; 0.
  - Draw location from locations, keep a combination only if (location.qty &gt; 0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L206) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L954) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L451)

<a id="op-52c6d84ae92456"></a>
### Get available item locations for serial and batched item

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_available_item_locations_for_serial_and_batched_item`

**Inputs** item\_code, from\_warehouses, required\_qty, company, consider\_rejected\_warehouses = false.

**Explicit results** locations.

**Local steps**

- Set locations from get\_available\_item\_locations\_for\_batched\_item(item\_code, from\_warehouses, company, consider\_rejected\_warehouses = consider\_rejected\_warehouses).
- If locations.
  - Set sn from Platform.qb.DocType(“Serial No”).
  - Set conditions from (sn.item\_code equals item\_code bitwise and sn.company equals company).
  - For each location in locations.
    - Set location.qty from required\_qty when location.qty &gt; required\_qty, otherwise location.qty.
      - Value choice on location.qty &gt; required\_qty — true gives required\_qty, false gives location.qty.
    - Set serial\_nos from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op ….
    - Set serial\_nos from list of sn.name for sn drawn from serial\_nos.
      - Draw sn from serial\_nos.
    - Set location.serial\_nos from serial\_nos.
    - Set location.qty from len(serial\_nos).
- Return locations.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0765.json#L4875) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L302) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L61)

<a id="op-b6881e288cafa4"></a>
### Get available item locations for serialized item

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_available_item_locations_for_serialized_item`

**Inputs** item\_code, from\_warehouses, company, consider\_rejected\_warehouses = false.

**Explicit results** locations.

**Local steps**

- Set sn from Platform.qb.DocType(“Serial No”).
- Set query from nested operand in the contract(nested operand in the contract).select(sn.name, sn.warehouse).where(sn.item\_code equals item\_code).orderby(sn.creation).
- If from\_warehouses.
  - Set query from query.where(sn.warehouse.isin(from\_warehouses)).
- Otherwise.
  - Set query from query.where(Coalesce(sn.warehouse, empty text) differs from empty text).
  - Set query from query.where(sn.company equals company).
- If not consider\_rejected\_warehouses.
  - If rejected\_warehouses bound to get\_rejected\_warehouses().
    - Set query from query.where(sn.warehouse.notin(rejected\_warehouses)).
- Set serial\_nos from query.run(as\_list = true).
- Set warehouse\_serial\_nos\_map from Platform.\_dict().
- For each tuple(serial\_no, warehouse) in serial\_nos.
  - Evaluate warehouse\_serial\_nos\_map.setdefault(warehouse, list()).append(serial\_no).
- Set locations from list().
- For each tuple(warehouse, serial\_nos) in warehouse\_serial\_nos\_map.items().
  - Set qty from len(serial\_nos).
  - Evaluate locations.append(Platform.\_dict(mapping(“qty” → qty, “warehouse” → warehouse, “item\_code” → item\_code, “serial\_nos” → serial\_nos))).
- Return locations.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0765.json#L5433) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L303) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L62)

<a id="op-471657dd326175"></a>
### Get available item locations for batched item

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_available_item_locations_for_batched_item`

**Inputs** item\_code, from\_warehouses, company, consider\_rejected\_warehouses = false.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** locations.

**Local steps**

- Set locations from list().
- Set data from get\_auto\_batch\_nos(Platform.\_dict(mapping(“item\_code” → item\_code, “warehouse” → from\_warehouses, “company” → company, “based\_on” → Platform.get\_single\_value(“Stock Settings”, “pick\_serial\_and\_batch\_based\_on”)))).
- Set warehouse\_wise\_batches from Platform.\_dict().
- Set rejected\_warehouses from get\_rejected\_warehouses().
- For each d in data.
  - If (not consider\_rejected\_warehouses and rejected\_warehouses and d.warehouse belongs to rejected\_warehouses).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not consider\_rejected\_warehouses → rejected\_warehouses → d.warehouse belongs to rejected\_warehouses.
    - Continue with the next iteration or loop test.
  - If d.warehouse does not belong to warehouse\_wise\_batches.
    - Evaluate warehouse\_wise\_batches.setdefault(d.warehouse, defaultdict(float)).
  - Update warehouse\_wise\_batches at d.warehouse at d.batch\_no using + d.qty.
- For each tuple(warehouse, batches) in warehouse\_wise\_batches.items().
  - For each tuple(batch\_no, qty) in batches.items().
    - Evaluate locations.append(Platform.\_dict(mapping(“qty” → qty, “warehouse” → warehouse, “item\_code” → item\_code, “batch\_no” → batch\_no))).
- Return locations.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “pick\_serial\_and\_batch\_based\_on”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0765.json#L6200) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L300) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L59)

<a id="op-ee0b9f20250f38"></a>
### Get available item locations for other item

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_available_item_locations_for_other_item`

**Inputs** item\_code, from\_warehouses, company, consider\_rejected\_warehouses = false.

**Explicit results** item\_locations.

**Local steps**

- Set bin from Platform.qb.DocType(“Bin”).
- Set query from nested operand in the contract(nested operand in the contract).select(bin.warehouse, nested operand in the contract.as\_(“qty”)).where((bin.item\_code equals item\_code bitwise and bin.actual\_qty &gt; 0)).orderb ….
- If from\_warehouses.
  - Set query from query.where(bin.warehouse.isin(from\_warehouses)).
- Otherwise.
  - Set wh from Platform.qb.DocType(“Warehouse”).
  - Set query from query.from\_(wh).where((bin.warehouse equals wh.name bitwise and wh.company equals company)).
- If not consider\_rejected\_warehouses.
  - If rejected\_warehouses bound to get\_rejected\_warehouses().
    - Set query from query.where(bin.warehouse.notin(rejected\_warehouses)).
- Set item\_locations from query.run(as\_dict = true).
- Return item\_locations.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0765.json#L6808) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L301) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L60)

<a id="op-5466cca39a352a"></a>
### Create delivery note

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_create_delivery_note`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** create\_delivery(source\_name, target\_doc, “Delivery Note”).

**Local steps**

- Return create\_delivery(source\_name, target\_doc, “Delivery Note”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L918) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L415)

<a id="op-bc01ca21793c1f"></a>
### Get existing drafts

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_existing_drafts`

**Inputs** source\_name, target\_doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Record and data access** resolve a document from “Pick List” via get\_doc · read target\_doctype via get\_list.

**Explicit results** Platform.get\_list(target\_doctype, filters = mapping(“docstatus” → 0, “against\_pick\_list” → source\_name), pluck = “name”, order\_by = “name”).

**Explicit failure paths** validation helper — translated “Unsupported target document type”.

**Local steps**

- If target\_doctype does not belong to set(“Delivery Note”, “Sales Invoice”).
  - Call the validation error handler Platform.throw(translated “Unsupported target document type”).
- Set pick\_list from Platform.get\_doc(“Pick List”, source\_name).
- Evaluate pick\_list.check\_permission(“read”).
- Return Platform.get\_list(target\_doctype, filters = mapping(“docstatus” → 0, “against\_pick\_list” → source\_name), pluck = “name”, order\_by = “name”).

**Values supplied outside this operation** effective access from pick\_list.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L182) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L930) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L427)

<a id="op-518bcda1bea028"></a>
### Create delivery

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_create_delivery`

**Inputs** source\_name, target\_doc = no value, target = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Pick List” via get\_doc.

**State and service calls** msgprint with translated “{0} created”.format(comma\_and(doc\_list)).

**Explicit results** documents at 0.

**Explicit failure paths** validation helper — translated “Nothing picked in this Pick List is left to deliver.”.

**Local steps**

- Set pick\_list from Platform.get\_doc(“Pick List”, source\_name).
- Evaluate pick\_list.check\_permission(“read”).
- Set target from (target or (Platform.flags.args or mapping()).get(“target”) or “Delivery Note”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in target → (Platform.flags.args or mapping()).get(“target”) → “Delivery Note”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.args → mapping().
- Evaluate validate\_item\_locations(pick\_list).
- Set sales\_dict from dict().
- Set documents from list().
- Set sales\_orders from get\_sales\_order\_headers(set of location.sales\_order for location drawn from pick\_list.locations).
  - Draw location from pick\_list.locations.
- For each tuple(key, rows) in groupby(sorted(sales\_orders, key = get\_header\_key), key = get\_header\_key).
  - Set sales\_dict at key from set of row.sales\_order for row drawn from rows.
    - Draw row from rows.
- If sales\_dict.
  - Evaluate documents.extend(create\_delivery\_with\_so(sales\_dict, pick\_list, target)).
- If any(generator of (not row.sales\_order and flt(row.picked\_qty) &gt; flt(row.delivered\_qty)) for row drawn from pick\_list.locations).
  - Draw row from pick\_list.locations.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.sales\_order → flt(row.picked\_qty) &gt; flt(row.delivered\_qty).
  - Evaluate documents.append(create\_delivery\_wo\_so(pick\_list, target, target\_doc)).
- If not documents.
  - Call the validation error handler Platform.throw(translated “Nothing picked in this Pick List is left to deliver.”).
- If len(documents) equals 1.
  - Return documents at 0.
- Otherwise.
  - Bind dependencies comma\_and.
  - Set doc\_list from list of get\_link\_to\_form(target, p.name) for p drawn from documents.
    - Draw p from documents.
  - Evaluate Platform.msgprint(translated “{0} created”.format(comma\_and(doc\_list))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from pick\_list.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L916) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L413)

<a id="op-f387115e70ebe9"></a>
### Get header key

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_header_key`

**Inputs** sales\_order.

**Explicit results** key.

**Local steps**

- Set key from tuple(generator of cstr(sales\_order.get(field)) for field drawn from SALES\_ORDER\_HEADER\_FIELDS).
  - Draw field from SALES\_ORDER\_HEADER\_FIELDS.
- Update key using + tuple(tuple(generator of tuple(generator of cstr(nested operand in the contract(nested operand in the contract)) for field drawn from SALES\_ORDER\_TAX\_KEY\_FIELDS) for tax drawn from sales\_order.taxes)).
  - Draw tax from sales\_order.taxes.
  - Draw field from SALES\_ORDER\_TAX\_KEY\_FIELDS.
- If has\_order\_specific\_amounts(sales\_order).
  - Update key using + tuple(sales\_order.sales\_order).
- Return key.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L183) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L931) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L428)
