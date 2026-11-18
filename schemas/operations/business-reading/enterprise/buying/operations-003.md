# Purchasing · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Purchase order

[Record definition](../../../../data/record-types/purchase_order.json)

<a id="op-8810017227a24f"></a>
### Purchase Order.update status updater

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_update_status_updater`

**Inputs** self.

**Local steps**

- Evaluate self.status\_updater.extend(self.get\_sales\_order\_status\_updater()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sales order status updater](operations-003.md#op-57834f40ac7009).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L184) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1387)

<a id="op-57834f40ac7009"></a>
### Purchase Order.get sales order status updater

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_purchaseorder_get_sales_order_status_updater`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** list(mapping(“source\_dt” → “Purchase Order Item”, “target\_dt” → “Sales Order Item”, “target\_field” → “ordered\_qty”, “target\_parent\_dt” → “Sales Order”, …), mapping(“source\_dt” → “Purchase Order Item”, “tar ….

**Local steps**

- Return list(mapping(“source\_dt” → “Purchase Order Item”, “target\_dt” → “Sales Order Item”, “target\_field” → “ordered\_qty”, “target\_parent\_dt” → “Sales Order”, …), mapping(“source\_dt” → “Purchase Order Item”, “tar ….

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_sales”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L813) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L53)

<a id="op-238282a0c86233"></a>
### Purchase Order.update status updater if from pp

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_update_status_updater_if_from_production_plan`

**Inputs** self.

**Local steps**

- Evaluate self.status\_updater.append(mapping(“source\_dt” → “Purchase Order Item”, “target\_dt” → “Production Plan Sub Assembly Item”, “join\_field” → “production\_plan\_sub\_assembly\_item”, “target\_field” → “ordered\_qty”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L185) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1388)

<a id="op-29340c99cd1a51"></a>
### Purchase Order.update delivered qty in sales order

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_purchaseorder_update_delivered_qty_in_sales_order`

**Inputs** self.

**Local steps**

- Set sales\_orders\_to\_update from list().
- For each item in self.items.
  - If (item.sales\_order and item.delivered\_by\_supplier equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.sales\_order → item.delivered\_by\_supplier equals 1.
    - If item.sales\_order does not belong to sales\_orders\_to\_update.
      - Evaluate sales\_orders\_to\_update.append(item.sales\_order).
- For each so\_name in sales\_orders\_to\_update.
  - Set so from Platform.get\_lazy\_doc(“Sales Order”, so\_name).
  - Evaluate so.update\_delivery\_status().
  - Evaluate so.set\_status(update = true).
  - Evaluate so.notify\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L817) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L57)

<a id="op-078842097cb386"></a>
### Purchase Order.set received qty to zero for drop ship items

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_purchaseorder_set_received_qty_to_zero_for_drop_ship_items`

**Inputs** self.

**State and service calls** call db\_set on item.

**Local steps**

- For each item in self.items.
  - If item.delivered\_by\_supplier.
    - Evaluate item.db\_set(“received\_qty”, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L816) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L56)

<a id="op-1bdeec63022cc2"></a>
### Purchase Order.has drop ship item

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_purchaseorder_has_drop_ship_item`

**Inputs** self.

**Explicit results** any(generator of d.delivered\_by\_supplier for d drawn from self.items).

**Local steps**

- Return any(generator of d.delivered\_by\_supplier for d drawn from self.items).
  - Draw d from self.items.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L814) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L54)

<a id="op-1d17d5569b8d41"></a>
### Purchase Order.update dropship received qty

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_update_dropship_received_quantity`

**Inputs** self, data.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on item.

**Explicit failure paths** validation helper — translated “Please select at least one item to update delivered quantity.” · validation helper — translated “Item with name {0} not found in the Purchase Order”.format(Platform.bold(d.get(“name”))) · validation helper — translated “Item {0} is not a drop ship item. Only drop ship items can have Delivered Qty updated.”.format(Platform.bold(item.item\_code)) · validation helper — translated “You don't have permission to update Received Qty DocField for item {0}”.format(Platform.bold(item.item\_code)) · validation helper — translated “Item {0} has no changes in delivered quantity. Please unselect the row if you do not wish to update its quantity.”.format(Platform.bold(item.item\_code)) · 2 additional forms in the steps below.

**Local steps**

- Evaluate self.check\_permission(“write”).
- If not data.
  - Call the validation error handler Platform.throw(translated “Please select at least one item to update delivered quantity.”).
- For each d in data.
  - Set item from next(generator of item for item drawn from self.items where item.name equals d.get(“name”), no value).
    - Draw item from self.items, keep a combination only if (item.name equals d.get(“name”)).
  - If not item.
    - Call the validation error handler Platform.throw(translated “Item with name {0} not found in the Purchase Order”.format(Platform.bold(d.get(“name”)))).
  - If not item.delivered\_by\_supplier.
    - Call the validation error handler Platform.throw(translated “Item {0} is not a drop ship item. Only drop ship items can have Delivered Qty updated.”.format(Platform.bold(item.item\_code))).
  - If not item.has\_permlevel\_access\_to(“received\_qty”, permission\_type = “write”).
    - Call the validation error handler Platform.throw(translated “You don't have permission to update Received Qty DocField for item {0}”.format(Platform.bold(item.item\_code))).
  - If not d.get(“qty\_change”).
    - Call the validation error handler Platform.throw(translated “Item {0} has no changes in delivered quantity. Please unselect the row if you do not wish to update its quantity.”.format(Platform.bold(item.item\_code))).
  - If (d.get(“qty\_change”) &lt; 0 and abs(d.get(“qty\_change”)) &gt; item.received\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“qty\_change”) &lt; 0 → abs(d.get(“qty\_change”)) &gt; item.received\_qty.
    - Call the validation error handler Platform.throw(translated “Delivered Qty cannot be reduced by more than {0} for item {1}”.format(item.received\_qty, Platform.bold(item.item\_code))).
  - If (d.get(“qty\_change”) &gt; 0 and (item.received\_qty + d.get(“qty\_change”)) &gt; item.qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“qty\_change”) &gt; 0 → (item.received\_qty + d.get(“qty\_change”)) &gt; item.qty.
    - Call the validation error handler Platform.throw(translated “Delivered Qty cannot be increased by more than {0} for item {1}”.format((item.qty − item.received\_qty), Platform.bold(item.item\_code))).
  - Set qty\_change from (item.received\_qty + d.get(“qty\_change”)).
  - Evaluate item.db\_set(“received\_qty”, qty\_change, update\_modified = true).
  - Evaluate self.add\_comment(“Label”, translated “updated delivered quantity for item {0} to {1}”.format(Platform.bold(item.item\_code), Platform.bold(qty\_change))).
- Evaluate self.update\_receiving\_percentage().
- Evaluate self.set\_status(update = true).
- Evaluate self.update\_delivered\_qty\_in\_sales\_order().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update receiving percentage](operations-003.md#op-045bbf8188f24a), [update delivered qty in sales order](operations-003.md#op-29340c99cd1a51).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1381)

<a id="op-c70a01a06197c3"></a>
### Purchase Order.is against so

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_is_against_sales_order`

**Inputs** self.

**Explicit results** any(generator of d.sales\_order for d drawn from self.items where d.sales\_order).

**Local steps**

- Return any(generator of d.sales\_order for d drawn from self.items where d.sales\_order).
  - Draw d from self.items, keep a combination only if (d.sales\_order).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0338.json#L5583) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L98) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1375)

<a id="op-97f7defb881378"></a>
### Purchase Order.is against pp

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_is_against_production_plan`

**Inputs** self.

**Explicit results** any(generator of d.production\_plan for d drawn from self.items where d.production\_plan).

**Local steps**

- Return any(generator of d.production\_plan for d drawn from self.items where d.production\_plan).
  - Draw d from self.items, keep a combination only if (d.production\_plan).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0338.json#L5668) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L97) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1374)

<a id="op-10887b4d05fea4"></a>
### Purchase Order.update reserved qty for subcontract

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_purchaseorder_update_reserved_qty_for_subcontract`

**Inputs** self.

**Local steps**

- If self.is\_old\_subcontracting\_flow.
  - For each d in self.supplied\_items.
    - If d.rm\_item\_code.
      - Set stock\_bin from get\_bin(d.rm\_item\_code, d.reserve\_warehouse).
      - Evaluate stock\_bin.update\_reserved\_qty\_for\_sub\_contracting(subcontract\_doctype = “Purchase Order”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L818) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L58)

<a id="op-045bbf8188f24a"></a>
### Purchase Order.update receiving percentage

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_update_receiving_percentage`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set tuple(total\_qty, received\_qty) from tuple(0.0, 0.0).
- For each item in self.items.
  - Update received\_qty using + min(item.received\_qty, item.qty).
  - Update total\_qty using + item.qty.
- If (total\_qty and received\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in total\_qty → received\_qty.
  - Evaluate self.db\_set(“per\_received”, (flt((received\_qty ÷ total\_qty)) × 100), update\_modified = false).
- Otherwise.
  - Evaluate self.db\_set(“per\_received”, 0, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L182) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1385)

<a id="op-f15f0a1c7bc1a1"></a>
### Purchase Order.set service items for finished goods

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_set_service_items_for_finished_goods`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.is\_subcontracted or self.is\_old\_subcontracting\_flow).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_subcontracted → self.is\_old\_subcontracting\_flow.
  - Return no value.
- Set finished\_goods\_without\_service\_item from list(set of d.fg\_item for d drawn from self.items where (not d.item\_code and d.fg\_item)).
  - Draw d from self.items, keep a combination only if ((not d.item\_code and d.fg\_item)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.item\_code → d.fg\_item.
- If subcontracting\_boms bound to get\_subcontracting\_boms\_for\_finished\_goods(finished\_goods\_without\_service\_item).
  - For each item in self.items.
    - If (not item.item\_code and item.fg\_item belongs to subcontracting\_boms).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.item\_code → item.fg\_item belongs to subcontracting\_boms.
      - Set subcontracting\_bom from subcontracting\_boms at item.fg\_item.
      - Set item.item\_code from subcontracting\_bom.service\_item.
      - Set item.qty from (flt(item.fg\_item\_qty) × flt(subcontracting\_bom.conversion\_factor)).
      - Set item.uom from subcontracting\_bom.service\_item\_uom.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1380)

<a id="op-1c1dc92ffe9793"></a>
### Purchase Order.can update items

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_can_update_items`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Subcontracting Order” via exists.

**Explicit results** result.

**Local steps**

- Set result from true.
- If (self.is\_subcontracted and not self.is\_old\_subcontracting\_flow).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_subcontracted → not self.is\_old\_subcontracting\_flow.
  - If Platform.db.exists(“Subcontracting Order”, mapping(“purchase\_order” → self.name, “docstatus” → list(“!=”, 2))).
    - Set result from false.
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L92) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1370)

<a id="op-85b2ae627e692f"></a>
### Purchase Order.update ordered qty in so for removed items

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_update_ordered_quantity_in_sales_order_for_removed_items`

**Inputs** self, removed\_items.

**Explicit results** no value.

**Local steps**

- If not removed\_items.
  - Return no value.
- For each args in self.get\_sales\_order\_status\_updater().
  - Evaluate self.\_update\_children(mapping(expand args, “cond” → empty text), update\_modified = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sales order status updater](operations-003.md#op-57834f40ac7009).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1383)

<a id="op-aee7bdc8f4bd23"></a>
### Purchase Order.auto create subcontracting order

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_purchaseorder_auto_create_subcontracting_order`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Local steps**

- If (self.is\_subcontracted and not self.is\_old\_subcontracting\_flow).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_subcontracted → not self.is\_old\_subcontracting\_flow.
  - If Platform.db.get\_single\_value(“Buying Settings”, “auto\_create\_subcontracting\_order”).
    - Evaluate make\_subcontracting\_order(self.name, save = true, notify = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “auto\_create\_subcontracting\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L811) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L51)

<a id="op-f8ec8678e8f764"></a>
### Purchase Order.update subcontracting order status

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_purchaseorder_update_subcontracting_order_status`

**Inputs** self.

**Record and data access** read “Subcontracting Order” via get\_all.

**Local steps**

- Bind dependencies update\_sco\_status.
- If (self.is\_subcontracted and not self.is\_old\_subcontracting\_flow).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_subcontracted → not self.is\_old\_subcontracting\_flow.
  - For each sco in Platform.get\_all(“Subcontracting Order”, mapping(“purchase\_order” → self.name, “docstatus” → 1), pluck = “name”).
    - Evaluate update\_sco\_status(sco, “Closed” when self.status equals “Closed”, otherwise no value).
      - Value choice on self.status equals “Closed” — true gives “Closed”, false gives no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L819) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L59)

<a id="op-58fe4ca25ab219"></a>
### Item last purchase rate

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_item_last_purchase_rate`

**Inputs** name, conversion\_rate, item\_code, conversion\_factor = 1.0.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** last\_purchase\_rate · ((item\_last\_purchase\_rate × (flt(conversion\_factor) or 1.0)) ÷ conversion\_rate).

**Local steps**

- Set conversion\_rate from (flt(conversion\_rate) or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(conversion\_rate) → 1.0.
- Set last\_purchase\_details from get\_last\_purchase\_details(item\_code, name).
- If last\_purchase\_details.
  - Set last\_purchase\_rate from ((last\_purchase\_details at “base\_net\_rate” × (flt(conversion\_factor) or 1.0)) ÷ conversion\_rate).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(conversion\_factor) → 1.0.
  - Return last\_purchase\_rate.
- Otherwise.
  - Set item\_last\_purchase\_rate from Platform.get\_cached\_value(“Item”, item\_code, “last\_purchase\_rate”).
  - If item\_last\_purchase\_rate.
    - Return ((item\_last\_purchase\_rate × (flt(conversion\_factor) or 1.0)) ÷ conversion\_rate).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(conversion\_factor) → 1.0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “last\_purchase\_rate”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L90) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1368)

<a id="op-dfbdb4ee372b90"></a>
### Close or unclose purchase orders

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_close_or_unclose_purchase_orders`

**Inputs** names, status.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid name”.

**Local steps**

- Evaluate Platform.has\_permission(“Purchase Order”, “write”, throw = true).
- Set names from json.loads(names).
- For each name in names.
  - If not isinstance(name, str).
    - Call the validation error handler Platform.throw(translated “Invalid name”, Platform.PermissionError).
  - Set po from Platform.get\_lazy\_doc(“Purchase Order”, name, check\_permission = “submit”).
  - If po.docstatus equals 1.
    - If status equals “Closed”.
      - If (po.status does not belong to tuple(“Cancelled”, “Closed”) and (po.per\_received &lt; 100 or po.per\_billed &lt; 100)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in po.status does not belong to tuple(“Cancelled”, “Closed”) → (po.per\_received &lt; 100 or po.per\_billed &lt; 100).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in po.per\_received &lt; 100 → po.per\_billed &lt; 100.
        - Evaluate po.update\_status(status).
    - Otherwise.
      - If po.status equals “Closed”.
        - Evaluate po.update\_status(“Draft”).
    - Evaluate po.update\_blanket\_order().
- Set Platform.local.message\_log from list().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Purchase Order”, “write”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L88) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1366)

<a id="op-9b3fabcad8348d"></a>
### Set missing values

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_set_missing_values`

**Inputs** source, target.

**Local steps**

- Evaluate target.set\_transaction\_date\_exchange\_rate().
- Evaluate target.run\_method(“set\_missing\_values”).
- Evaluate target.run\_method(“calculate\_taxes\_and\_totals”).
- Evaluate target.run\_method(“set\_use\_serial\_batch\_fields”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”), target.run\_method(“calculate\_taxes\_and\_totals”) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L823) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L63)

<a id="op-9c0becea9ca24e"></a>
### Is unit price row

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_is_unit_price_row`

**Inputs** po\_item, has\_unit\_price\_items.

**Declared result** bool.

**Explicit results** (bool(has\_unit\_price\_items) and po\_item.qty equals 0).

**Local steps**

- Return (bool(has\_unit\_price\_items) and po\_item.qty equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(has\_unit\_price\_items) → po\_item.qty equals 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L803) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L43)

<a id="op-b9ff7789a3be23"></a>
### Make purchase receipt

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_make_purchase_receipt`

**Inputs** source\_name, target\_doc = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Purchase Order” via get\_value.

**Explicit results** doc.

**Local steps**

- If args is identical to no value.
  - Set args from mapping().
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set has\_unit\_price\_items from Platform.db.get\_value(“Purchase Order”, source\_name, “has\_unit\_price\_items”).
- Set mapped\_qty\_by\_item from get\_qty\_already\_mapped(target\_doc, “purchase\_order\_item”).
- Bind local operation update\_item for subsequent calls.
- Bind local operation select\_item for subsequent calls.
- Set doc from get\_mapped\_doc(“Purchase Order”, source\_name, mapping(“Purchase Order” → mapping(“doctype” → “Purchase Receipt”, “field\_map” → mapping(“supplier\_warehouse” → “supplier\_warehouse”), “validation” → mapping(“ ….
- Return doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L807) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L47)

<a id="op-5bcba28390ab81"></a>
### Make purchase receipt.update item

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_make_purchase_receipt_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Set received\_qty from (flt(obj.received\_qty) + flt(mapped\_qty\_by\_item.get(obj.name, 0))).
- Set pending\_qty from (flt(obj.qty) − received\_qty).
- Set target.qty from flt(obj.qty) when is\_unit\_price\_row(obj, has\_unit\_price\_items), otherwise pending\_qty.
  - Value choice on is\_unit\_price\_row(obj, has\_unit\_price\_items) — true gives flt(obj.qty), false gives pending\_qty.
- Set target.stock\_qty from (pending\_qty × flt(obj.conversion\_factor)).
- Set target.amount from (pending\_qty × flt(obj.rate)).
- Set target.base\_amount from ((pending\_qty × flt(obj.rate)) × flt(source\_parent.conversion\_rate)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L809) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L49)

<a id="op-dd15c104826663"></a>
### Make purchase receipt.select item

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_make_purchase_receipt_select_item`

**Inputs** d.

**Explicit results** child\_filter.

**Local steps**

- Set filtered\_items from args.get(“filtered\_children”, list()).
- Set child\_filter from d.name belongs to filtered\_items when filtered\_items, otherwise true.
  - Value choice on filtered\_items — true gives d.name belongs to filtered\_items, false gives true.
- Return child\_filter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L808) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L48)

<a id="op-b486f88ff3db94"></a>
### Make purchase invoice

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_make_purchase_invoice`

**Inputs** source\_name, target\_doc = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_mapped\_purchase\_invoice(source\_name, target\_doc, args = args).

**Local steps**

- Return get\_mapped\_purchase\_invoice(source\_name, target\_doc, args = args).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L805) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L45)
