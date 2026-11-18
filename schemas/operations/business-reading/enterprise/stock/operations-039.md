# Inventory and warehouses · operations 39

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pick list

[Record definition](../../../../data/record-types/pick_list.json)

<a id="op-3c055ff2b15a01"></a>
### Pick List.update sales order picking status

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_update_sales_order_picking_status`

**Inputs** self.

**Declared result** no value.

**Record and data access** resolve a document from “Sales Order” via get\_doc.

**Local steps**

- Set sales\_orders from list().
- For each row in self.locations.
  - If (row.sales\_order and row.sales\_order does not belong to sales\_orders).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.sales\_order → row.sales\_order does not belong to sales\_orders.
    - Evaluate sales\_orders.append(row.sales\_order).
- For each sales\_order in sales\_orders.
  - Evaluate Platform.get\_doc(“Sales Order”, sales\_order, for\_update = true).update\_picking\_status().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L2293) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L110)

<a id="op-4e1ec741cb6386"></a>
### Pick List.update picked qty in work order

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_update_picked_quantity_in_work_order`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Explicit results** no value.

**Local steps**

- If not self.work\_order.
  - Return no value.
- Evaluate Platform.get\_doc(“Work Order”, self.work\_order).update\_picked\_qty\_for\_required\_items().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L107)

<a id="op-2ce3e6ca58139d"></a>
### Pick List.create stock reservation entries

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_create_stock_reservation_entries`

**Inputs** self, notify = true.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from “Sales Order” via get\_doc.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set so\_items\_details\_map from mapping().
- For each location in self.locations.
  - If (location.warehouse and location.sales\_order and location.sales\_order\_item).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in location.warehouse → location.sales\_order → location.sales\_order\_item.
    - Set item\_details from mapping(“sales\_order\_item” → (location.product\_bundle\_item or location.sales\_order\_item), “item\_code” → location.item\_code, “warehouse” → location.warehouse, “qty\_to\_reserve” → (flt(location.picked\_qty) −  ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in location.product\_bundle\_item → location.sales\_order\_item.
    - Evaluate so\_items\_details\_map.setdefault(location.sales\_order, list()).append(item\_details).
- If so\_items\_details\_map.
  - For each tuple(so, items\_details) in so\_items\_details\_map.items().
    - Set so\_doc from Platform.get\_doc(“Sales Order”, so).
    - Evaluate so\_doc.\_create\_stock\_reservation\_entries(items\_details = items\_details, from\_voucher\_type = “Pick List”, notify = notify).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L78)

<a id="op-8dbdd4ac335e5f"></a>
### Pick List.cancel stock reservation entries

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_cancel_stock_reservation_entries`

**Inputs** self, notify = true.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Bind dependencies cancel\_stock\_reservation\_entries.
- Evaluate cancel\_stock\_reservation\_entries(from\_voucher\_type = “Pick List”, from\_voucher\_no = self.name, notify = notify).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L323) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L75)

<a id="op-bb470df4ddcf3d"></a>
### Pick List.validate picked qty

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_validate_picked_quantity`

**Inputs** self, data, ordered\_doctype = “Sales Order Item”.

**Record and data access** read “Stock Settings” via get\_single\_value · read ordered\_doctype via get\_all.

**Explicit failure paths** validation helper — translated “You are picking more than required quantity for the item {0}. Check if there is any other pick list created  …”.format(row.item\_code, row.sales\_order).

**Local steps**

- Set allowance from (1 + (flt(Platform.get\_single\_value(“Stock Settings”, “over\_picking\_allowance”)) ÷ 100)).
- Set qty\_field from “qty” when ordered\_doctype equals “Packed Item”, otherwise “stock\_qty”.
  - Value choice on ordered\_doctype equals “Packed Item” — true gives “qty”, false gives “stock\_qty”.
- Set reference\_field from “product\_bundle\_item” when ordered\_doctype equals “Packed Item”, otherwise “sales\_order\_item”.
  - Value choice on ordered\_doctype equals “Packed Item” — true gives “product\_bundle\_item”, false gives “sales\_order\_item”.
- Set ordered\_qty from dict(Platform.get\_all(ordered\_doctype, filters = mapping(“name” → tuple(“in”, list of nested operand in the contract.get(reference\_field) for row drawn from data)), fields = list(“name”, qty\_field), as\_list = true)).
  - Draw row from data.
- For each row in data.
  - Set ordered from flt(ordered\_qty.get(row.get(reference\_field))).
  - If (ordered and flt(row.picked\_qty, 6) &gt; flt((ordered × allowance), 6)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ordered → flt(row.picked\_qty, 6) &gt; flt((ordered × allowance), 6).
    - Call the validation error handler Platform.throw(translated “You are picking more than required quantity for the item {0}. Check if there is any other pick list created  …”.format(row.item\_code, row.sales\_order)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “over\_picking\_allowance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L117)

<a id="op-3b00d61c3d44ac"></a>
### Pick List.set item locations

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_set_item_locations`

**Inputs** self, save = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Pick List” via exists · read “Warehouse” via get\_value · read “Work Order Item” via get\_all · read “UOM” via get\_cached\_value.

**State and service calls** msgprint with translated “Please Restock Items and Update the Pick List to continue. To discontinue, cancel the Pick List.” · call save on self.

**Local steps**

- If (self.name and Platform.db.exists(“Pick List”, self.name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.name → Platform.db.exists(“Pick List”, self.name).
  - Evaluate self.check\_permission(“write”).
- Evaluate self.validate\_for\_qty().
- Set items from self.aggregate\_item\_qty().
- Set picked\_items\_details from self.get\_picked\_items\_details(items).
- Set self.item\_location\_map from Platform.\_dict().
- Set from\_warehouses from list().
- If self.parent\_warehouse.
  - Set from\_warehouses from list(self.parent\_warehouse).
- Otherwise.
  - If self.work\_order.
    - Set root\_warehouse from Platform.db.get\_value(“Warehouse”, mapping(“company” → self.company, “parent\_warehouse” → list(“IS”, “NOT SET”), “is\_group” → 1)).
    - Set from\_warehouses from list(root\_warehouse).
- If from\_warehouses.
  - Evaluate from\_warehouses.extend(get\_descendants\_of(“Warehouse”, from\_warehouses at 0)).
- Set item\_warehouse\_dict from Platform.\_dict().
- If self.work\_order.
  - Set item\_warehouse\_list from Platform.get\_all(“Work Order Item”, filters = mapping(“parent” → self.work\_order), fields = list(“item\_code”, “source\_warehouse”)).
  - If item\_warehouse\_list.
    - Set item\_warehouse\_dict from mapping of item.item\_code → item.source\_warehouse for item drawn from item\_warehouse\_list.
      - Draw item from item\_warehouse\_list.
- Set locations\_replica from self.get(“locations”).
- Set own\_vouchers from self.get\_own\_vouchers().
- Set reset\_rows from list().
- For each row in self.get(“locations”).
  - If not row.picked\_qty.
    - Evaluate reset\_rows.append(row).
- For each row in reset\_rows.
  - Evaluate self.remove(row).
- Set updated\_locations from Platform.\_dict().
- Set len\_idx from (len(self.get(“locations”)) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(self.get(“locations”)) → 0.
- Set excluded\_warehouses from self.get\_excluded\_warehouses().
- For each item\_doc in items.
  - Set item\_code from item\_doc.item\_code.
  - Set priority\_warehouses from list(item\_doc.warehouse) when (item\_doc.warehouse and not self.work\_order), otherwise list().
    - Value choice on (item\_doc.warehouse and not self.work\_order) — true gives list(item\_doc.warehouse), false gives list().
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_doc.warehouse → not self.work\_order.
  - If (self.work\_order and item\_warehouse\_dict.get(item\_code)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → item\_warehouse\_dict.get(item\_code).
    - Set source\_warehouse from item\_warehouse\_dict.get(item\_code).
    - Set priority\_warehouses from list(source\_warehouse).
    - Evaluate priority\_warehouses.extend(get\_descendants\_of(“Warehouse”, source\_warehouse)).
    - Set from\_warehouses from list(dict.fromkeys((priority\_warehouses + from\_warehouses))).
  - If item\_code does not belong to self.item\_location\_map.
    - Set self.item\_location\_map at item\_code from get\_available\_item\_locations(item\_code, from\_warehouses, self.item\_count\_map.get(item\_code), self.company, picked\_item\_details = picked\_items\_details.get(item\_code), consider\_rejected\_warehouses = self.con ….
  - Set locations from get\_items\_with\_location\_and\_quantity(item\_doc, self.item\_location\_map, self.docstatus).
  - Set item\_doc.idx from no value.
  - Set item\_doc.name from no value.
  - For each row in locations.
    - Set location from item\_doc.as\_dict().
    - Evaluate location.update(row).
    - Set key from tuple(location.item\_code, location.warehouse, location.uom, location.batch\_no, …).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in location.sales\_order\_item → location.material\_request\_item.
    - If key does not belong to updated\_locations.
      - Evaluate updated\_locations.setdefault(key, location).
    - Otherwise.
      - Update updated\_locations at key.qty using + location.qty.
      - Update updated\_locations at key.stock\_qty using + location.stock\_qty.
- For each location in updated\_locations.values().
  - If location.picked\_qty &gt; location.stock\_qty.
    - Set location.picked\_qty from location.stock\_qty.
  - Update len\_idx using + 1.
  - Set location.idx from len\_idx.
  - Evaluate self.append(“locations”, location).
- If (not self.get(“locations”) and self.docstatus equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(“locations”) → self.docstatus equals 1.
  - For each location in locations\_replica.
    - Set location.stock\_qty from 0.
    - Set location.picked\_qty from 0.
    - Update len\_idx using + 1.
    - Set location.idx from len\_idx.
    - Evaluate self.append(“locations”, location).
  - Evaluate Platform.msgprint(translated “Please Restock Items and Update the Pick List to continue. To discontinue, cancel the Pick List.”, title = translated “Out of Stock”, indicator = “red”).
- If save.
  - Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate for qty](operations-039.md#op-89d49a05d53215), [aggregate item qty](operations-039.md#op-ba755641e8c536), [get picked items details](operations-039.md#op-514f17140be301), [get own vouchers](operations-039.md#op-df32fca8c73b0b), [get excluded warehouses](operations-039.md#op-3e03aa2071acb7).

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · configured or stored value from Platform.get\_cached\_value(“UOM”, item\_doc.uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L101)

<a id="op-3e03aa2071acb7"></a>
### Pick List.get excluded warehouses

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_picklist_get_excluded_warehouses`

**Inputs** self.

**Declared result** set.

**Record and data access** read “Warehouse” via get\_all · read “Work Order” via get\_value.

**Explicit results** excluded.

**Local steps**

- Set excluded from set(Platform.get\_all(“Warehouse”, filters = mapping(“company” → self.company, “warehouse\_type” → “Transit”), pluck = “name”)).
- If (self.work\_order and wip\_warehouse bound to Platform.db.get\_value(“Work Order”, self.work\_order, “wip\_warehouse”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → wip\_warehouse bound to Platform.db.get\_value(“Work Order”, self.work\_order, “wip\_warehouse”).
  - Evaluate excluded.add(wip\_warehouse).
- Return excluded.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L199) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L947) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L444)

<a id="op-ba755641e8c536"></a>
### Pick List.aggregate item qty

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_aggregate_item_quantity`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value · read “Product Bundle” via exists.

**Explicit results** item\_map.values().

**Explicit failure paths** validation helper — formatted text Row #{item.idx}: Item Code is Mandatory.

**Local steps**

- Set locations from self.get(“locations”).
- Set self.item\_count\_map from mapping().
- Set item\_map from OrderedDict().
- For each item in locations.
  - If item.picked\_qty.
    - Continue with the next iteration or loop test.
  - If not item.item\_code.
    - Call the validation error handler Platform.throw(formatted text Row #{item.idx}: Item Code is Mandatory).
  - If (not cint(Platform.get\_cached\_value(“Item”, item.item\_code, “is\_stock\_item”)) and not Platform.db.exists(“Product Bundle”, mapping(“new\_item\_code” → item.item\_code, “disabled” → 0))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(Platform.get\_cached\_value(“Item”, item.item\_code, “is\_stock\_item”)) → not Platform.db.exists(“Product Bundle”, mapping(“new\_item\_code” → item.item\_code, “disabled” → 0)).
    - Continue with the next iteration or loop test.
  - Set item\_code from item.item\_code.
  - Set reference from (item.sales\_order\_item or item.material\_request\_item).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.sales\_order\_item → item.material\_request\_item.
  - Set key from tuple(item\_code, item.uom, item.warehouse, item.batch\_no, …).
  - Set item.idx from no value.
  - Set item.name from no value.
  - If item\_map.get(key).
    - Update item\_map at key.qty using + item.qty.
    - Update item\_map at key.stock\_qty using + flt(item.stock\_qty, item.precision(“stock\_qty”)).
  - Otherwise.
    - Set item\_map at key from item.
  - Evaluate self.item\_count\_map.setdefault(item\_code, 0).
  - Update self.item\_count\_map at item\_code using + flt(item.stock\_qty, item.precision(“stock\_qty”)).
- Return item\_map.values().

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L319) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L71)

<a id="op-89d49a05d53215"></a>
### Pick List.validate for qty

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_validate_for_quantity`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Qty of Finished Goods Item should be greater than 0.”.

**Local steps**

- If (self.purpose equals “Material Transfer for Manufacture” and (self.for\_qty is identical to no value or self.for\_qty equals 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Material Transfer for Manufacture” → (self.for\_qty is identical to no value or self.for\_qty equals 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.for\_qty is identical to no value → self.for\_qty equals 0.
  - Call the validation error handler Platform.throw(translated “Qty of Finished Goods Item should be greater than 0.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L6303) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L364) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L114)

<a id="op-1659c92e03e385"></a>
### Pick List.before print

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_before_print`

**Inputs** self, settings = no value.

**Local steps**

- If self.group\_same\_items.
  - Evaluate self.group\_similar\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [group similar items](operations-039.md#op-2d258a8dfa9d6a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L6450) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L320) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L72)

<a id="op-2d258a8dfa9d6a"></a>
### Pick List.group similar items

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_group_similar_items`

**Inputs** self.

**Local steps**

- Set grouped\_rows from mapping().
- For each item in self.locations.
  - Set key from tuple(item.item\_code, item.warehouse, item.uom, (item.batch\_no or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.batch\_no → empty text.
  - If key does not belong to grouped\_rows.
    - Set grouped\_rows at key from item.
    - Continue with the next iteration or loop test.
  - Set grouped\_row from grouped\_rows at key.
  - Set grouped\_row.qty from (flt(grouped\_row.qty) + flt(item.qty)).
  - Set grouped\_row.stock\_qty from (flt(grouped\_row.stock\_qty) + flt(item.stock\_qty)).
  - Set grouped\_row.picked\_qty from (flt(grouped\_row.picked\_qty) + flt(item.picked\_qty)).
- Evaluate self.set(“locations”, list(grouped\_rows.values())).
- For each tuple(idx, item) in enumerate(self.locations, start = 1).
  - Set item.idx from idx.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L85)

<a id="op-15d2b99efab325"></a>
### Pick List.update bundle picked qty

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_update_bundle_picked_quantity`

**Inputs** self.

**State and service calls** request set\_value on “Sales Order Item”.

**Local steps**

- Set product\_bundles from self.\_get\_product\_bundles().
- Set product\_bundle\_qty\_map from self.\_get\_product\_bundle\_qty\_map(product\_bundles).
- For each tuple(so\_row, packed\_items) in get\_packed\_items\_of\_order\_rows(product\_bundles).items().
  - Set picked\_qty from defaultdict(float).
  - For each row in packed\_items.
    - Update picked\_qty at row.item\_code using + flt(row.picked\_qty).
  - Set bundle\_qty from min(generator of get\_whole\_bundle\_count(picked\_qty at item\_code, qty\_per\_bundle) for tuple(item\_code, qty\_per\_bundle) drawn from product\_bundle\_qty\_map at so\_row.items(), default = 0).
    - Draw tuple(item\_code, qty\_per\_bundle) from product\_bundle\_qty\_map at so\_row.items().
  - Evaluate Platform.db.set\_value(“Sales Order Item”, so\_row, “picked\_qty”, bundle\_qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get product bundles](operations-039.md#op-98501972b8699e), [get product bundle qty map](operations-039.md#op-b20e904b84182a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L104)

<a id="op-df32fca8c73b0b"></a>
### Pick List.get own vouchers

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_picklist_get_own_vouchers`

**Inputs** self.

**Explicit results** vouchers.

**Local steps**

- Set vouchers from set of row.sales\_order for row drawn from self.locations where row.sales\_order.
  - Draw row from self.locations, keep a combination only if (row.sales\_order).
- If self.work\_order.
  - Evaluate vouchers.add(self.work\_order).
- Return vouchers.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L201) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L949) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L446)

<a id="op-514f17140be301"></a>
### Pick List.get picked items details

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_get_picked_items_details`

**Inputs** self, items.

**Explicit results** picked\_items.

**Local steps**

- Set picked\_items from Platform.\_dict().
- If not items.
  - Return picked\_items.
- Set items\_data from self.\_get\_pick\_list\_items(items).
- For each item\_data in items\_data.
  - Set key from tuple(item\_data.warehouse, item\_data.batch\_no) when item\_data.batch\_no, otherwise item\_data.warehouse.
    - Value choice on item\_data.batch\_no — true gives tuple(item\_data.warehouse, item\_data.batch\_no), false gives item\_data.warehouse.
  - Set serial\_no from list of x for x drawn from item\_data.serial\_no.split(whitespace '\\n') where x when item\_data.serial\_no, otherwise no value.
    - Value choice on item\_data.serial\_no — true gives list of x for x drawn from item\_data.serial\_no.split(whitespace '\\n') where x, false gives no value.
    - Draw x from item\_data.serial\_no.split(whitespace '\\n'), keep a combination only if (x).
  - If item\_data.item\_code does not belong to picked\_items.
    - Set picked\_items at item\_data.item\_code from mapping().
  - If item\_data.serial\_and\_batch\_bundle.
    - If not serial\_no.
      - Set serial\_no from get\_serial\_nos\_from\_bundle(item\_data.serial\_and\_batch\_bundle).
    - If (not item\_data.batch\_no and not serial\_no).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item\_data.batch\_no → not serial\_no.
      - Set bundle\_batches from get\_batches\_from\_bundle(item\_data.serial\_and\_batch\_bundle).
      - For each tuple(batch\_no, batch\_qty) in bundle\_batches.items().
        - Set batch\_qty from abs(batch\_qty).
        - Set key from tuple(item\_data.warehouse, batch\_no).
        - If key does not belong to picked\_items at item\_data.item\_code.
          - Set picked\_items at item\_data.item\_code at key from mapping(“picked\_qty” → 0).
        - Update picked\_items at item\_data.item\_code at key at “picked\_qty” using + batch\_qty.
      - Continue with the next iteration or loop test.
  - If key does not belong to picked\_items at item\_data.item\_code.
    - Set picked\_items at item\_data.item\_code at key from Platform.\_dict(mapping(“picked\_qty” → 0, “serial\_no” → list(), “batch\_no” → (item\_data.batch\_no or empty text), “warehouse” → item\_data.warehouse)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_data.batch\_no → empty text.
  - Update picked\_items at item\_data.item\_code at key at “picked\_qty” using + item\_data.picked\_qty.
  - If serial\_no.
    - Evaluate picked\_items at item\_data.item\_code at key at “serial\_no”.extend(serial\_no).
- Evaluate self.update\_picked\_item\_from\_current\_pick\_list(picked\_items).
- Return picked\_items.

**Methods declared on this owner** [get pick list items](operations-039.md#op-58c696e5c56257), [update picked item from current pick list](operations-039.md#op-0a3f32ea6cd694).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L81)

<a id="op-0a3f32ea6cd694"></a>
### Pick List.update picked item from current pick list

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_update_picked_item_from_current_pick_list`

**Inputs** self, picked\_items.

**Local steps**

- For each row in self.locations.
  - If flt(row.picked\_qty) &gt; 0.
    - Set key from tuple(row.warehouse, row.batch\_no) when row.batch\_no, otherwise row.warehouse.
      - Value choice on row.batch\_no — true gives tuple(row.warehouse, row.batch\_no), false gives row.warehouse.
    - Set serial\_no from list of x for x drawn from row.serial\_no.split(whitespace '\\n') where x when row.serial\_no, otherwise no value.
      - Value choice on row.serial\_no — true gives list of x for x drawn from row.serial\_no.split(whitespace '\\n') where x, false gives no value.
      - Draw x from row.serial\_no.split(whitespace '\\n'), keep a combination only if (x).
    - If row.item\_code does not belong to picked\_items.
      - Set picked\_items at row.item\_code from mapping().
    - If key does not belong to picked\_items at row.item\_code.
      - Set picked\_items at row.item\_code at key from Platform.\_dict(mapping(“picked\_qty” → 0, “serial\_no” → list(), “batch\_no” → (row.batch\_no or empty text), “warehouse” → row.warehouse)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.batch\_no → empty text.
    - Update picked\_items at row.item\_code at key at “picked\_qty” using + (flt(row.stock\_qty) or flt(row.picked\_qty)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.stock\_qty) → flt(row.picked\_qty).
    - If serial\_no.
      - Evaluate picked\_items at row.item\_code at key at “serial\_no”.extend(serial\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0764.json#L941) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L106)

<a id="op-58c696e5c56257"></a>
### Pick List.get pick list items

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_get_pick_list_items`

**Inputs** self, items.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set pi from Platform.qb.DocType(“Pick List”).
- Set pi\_item from Platform.qb.DocType(“Pick List Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(pi\_item.item\_code, pi\_item.warehouse, pi\_item.batc ….
  - Draw x from items.
- If self.name.
  - Set query from query.where(pi\_item.parent differs from self.name).
- Set query from query.for\_update().
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L80)

<a id="op-98501972b8699e"></a>
### Pick List.get product bundles

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_get_product_bundles`

**Inputs** self.

**Declared result** list at str.

**Record and data access** read “Sales Order Item” via get\_all.

**Explicit results** list() · list of name for name drawn from so\_item\_names where name belongs to existing.

**Local steps**

- Set so\_item\_names from list(dict.fromkeys(generator of item.sales\_order\_item for item drawn from self.locations where item.product\_bundle\_item)).
  - Draw item from self.locations, keep a combination only if (item.product\_bundle\_item).
- If not so\_item\_names.
  - Return list().
- Set existing from set(Platform.get\_all(“Sales Order Item”, filters = mapping(“name” → tuple(“in”, so\_item\_names)), pluck = “name”)).
- Return list of name for name drawn from so\_item\_names where name belongs to existing.
  - Draw name from so\_item\_names, keep a combination only if (name belongs to existing).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L83)

<a id="op-b20e904b84182a"></a>
### Pick List.get product bundle qty map

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_get_product_bundle_quantity_map`

**Inputs** self, so\_rows.

**Declared result** dict at tuple(str, dict at tuple(str, list at float)).

**Record and data access** read “Item” via get\_all.

**Explicit results** mapping() · qty\_map.

**Local steps**

- Set bundles from get\_packed\_items\_of\_order\_rows(so\_rows).
- If not bundles.
  - Return mapping().
- Set item\_codes from set of row.item\_code for packed\_items drawn from bundles.values(), then row drawn from packed\_items.
  - Draw packed\_items from bundles.values().
  - Draw row from packed\_items.
- Set stock\_items from set(Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, list(item\_codes)), “is\_stock\_item” → 1), pluck = “name”)).
- Set components from mapping().
- Set qty\_map from defaultdict(deferred anonymous expression).
- For each tuple(so\_row, packed\_items) in bundles.items().
  - Set parent\_item from packed\_items at 0.parent\_item.
  - If parent\_item does not belong to components.
    - Set components at parent\_item from list of tuple(component, get\_component\_stock\_qty\_per\_unit(component, no value)) for component drawn from get\_product\_bundle\_items(parent\_item).
      - Draw component from get\_product\_bundle\_items(parent\_item).
  - For each tuple(component, qty\_per\_unit) in components at parent\_item.
    - Set packed\_item from pop\_order\_packed\_item(packed\_items, parent\_item, component.item\_code).
    - If (packed\_item and component.item\_code belongs to stock\_items).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in packed\_item → component.item\_code belongs to stock\_items.
      - Evaluate qty\_map at so\_row at component.item\_code.append(get\_ordered\_qty\_per\_unit(qty\_per\_unit, packed\_item)).
- Return qty\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L82)

<a id="op-b685092db0c80a"></a>
### Pick List.compute picked qty for bundle

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_compute_picked_quantity_for_bundle`

**Inputs** self, bundle\_row, bundle\_items, pending\_only = false.

**Declared result** int.

**Explicit results** min(generator of get\_whole\_bundle\_count(picked\_qty at item\_code, qty) for tuple(item\_code, qty) drawn from bundle\_items.items(), default = 0).

**Local steps**

- Set picked\_qty from defaultdict(float).
- For each item in self.locations.
  - If item.sales\_order\_item equals bundle\_row.
    - Update picked\_qty at item.item\_code using + (flt(item.picked\_qty) − flt(item.delivered\_qty) when pending\_only, otherwise 0).
      - Value choice on pending\_only — true gives flt(item.delivered\_qty), false gives 0.
- Return min(generator of get\_whole\_bundle\_count(picked\_qty at item\_code, qty) for tuple(item\_code, qty) drawn from bundle\_items.items(), default = 0).
  - Draw tuple(item\_code, qty) from bundle\_items.items().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L325) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L77)

<a id="op-ae3a47012ef3c6"></a>
### Pick List.update bundle delivered qty

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_update_bundle_delivered_quantity`

**Inputs** self.

**State and service calls** request bulk\_update on “Pick List Item”.

**Explicit results** no value.

**Local steps**

- Set bundle\_locations from defaultdict(list).
- For each location in self.locations.
  - If location.product\_bundle\_item.
    - Evaluate bundle\_locations at tuple(location.sales\_order\_item, location.item\_code, location.warehouse, (location.batch\_no or empty text)).append(location).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in location.batch\_no → empty text.
- If not bundle\_locations.
  - Return no value.
- Set tuple(delivered\_qty\_by\_key, delivered\_serial\_nos) from get\_delivered\_bundle\_component\_qty(self.name, set of bundle\_key at 0 for bundle\_key drawn from bundle\_locations).
  - Draw bundle\_key from bundle\_locations.
- Set updates from mapping().
- For each tuple(bundle\_key, locations) in bundle\_locations.items().
  - Set qty\_by\_location from self.\_get\_bundle\_location\_delivered\_qty(locations, delivered\_qty\_by\_key.get(bundle\_key, 0), delivered\_serial\_nos at bundle\_key).
  - For each location in locations.
    - Set precision from location.precision(“delivered\_qty”).
    - Set delivered\_qty from flt(qty\_by\_location at location.name, precision).
    - If flt(location.delivered\_qty, precision) equals delivered\_qty.
      - Continue with the next iteration or loop test.
    - Set location.delivered\_qty from delivered\_qty.
    - Set updates at location.name from mapping(“delivered\_qty” → delivered\_qty).
- If updates.
  - Evaluate Platform.db.bulk\_update(“Pick List Item”, updates, update\_modified = false).
- Evaluate self.\_set\_delivery\_status\_from\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get bundle location delivered qty](operations-039.md#op-2950fa3c013be7), [set delivery status from items](operations-039.md#op-c29c9f52c78c60).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L103)

<a id="op-2950fa3c013be7"></a>
### Pick List.get bundle location delivered qty

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_picklist_get_bundle_location_delivered_qty`

**Inputs** locations, delivered\_qty, delivered\_serial\_nos.

**Wrappers, in declaration order** staticmethod.

**Explicit results** qty\_by\_location.

**Local steps**

- Set qty\_by\_location from mapping of location.name → len((set of number.lower() for number drawn from get\_serial\_nos(location.serial\_no) bitwise and delivered\_serial\_nos)) for location drawn from locations.
  - Draw location from locations.
  - Draw number from get\_serial\_nos(location.serial\_no).
- Set remaining\_qty from max((delivered\_qty − sum(qty\_by\_location.values())), 0).
- For each location in locations.
  - Set qty from min((flt(location.picked\_qty) − qty\_by\_location at location.name), remaining\_qty).
  - Update qty\_by\_location at location.name using + qty.
  - Update remaining\_qty using − qty.
- Return qty\_by\_location.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L197) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L945) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L442)

<a id="op-c29c9f52c78c60"></a>
### Pick List.set delivery status from items

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_set_delivery_status_from_items`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set per\_delivered from self.\_calculate\_target\_parent\_percentage(self.name, “Pick List”, “Pick List Item”, “picked\_qty”, …).
- Set delivery\_status from self.\_determine\_status(per\_delivered, “Delivered”).
- Set self.per\_delivered from per\_delivered.
- Set self.delivery\_status from delivery\_status.
- Evaluate self.db\_set(mapping(“per\_delivered” → per\_delivered, “delivery\_status” → delivery\_status), update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0764.json#L4187) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L100)

<a id="op-52cdb43f348185"></a>
### Pick List.has unreserved stock

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_has_unreserved_stock`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- If self.purpose equals “Delivery”.
  - For each location in self.locations.
    - If (location.sales\_order and location.sales\_order\_item and (flt(location.picked\_qty) − flt(location.stock\_reserved\_qty)) &gt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in location.sales\_order → location.sales\_order\_item → (flt(location.picked\_qty) − flt(location.stock\_reserved\_qty)) &gt; 0.
      - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0764.json#L4424) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L87)

<a id="op-3729827498d09e"></a>
### Pick List.has reserved stock

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_has_reserved_stock`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- If self.purpose equals “Delivery”.
  - For each location in self.locations.
    - If (location.sales\_order and location.sales\_order\_item and flt(location.stock\_reserved\_qty) &gt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in location.sales\_order → location.sales\_order\_item → flt(location.stock\_reserved\_qty) &gt; 0.
      - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0764.json#L4597) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L86)
