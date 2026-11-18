# Inventory and warehouses · operations 41

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pick list

[Record definition](../../../../data/record-types/pick_list.json)

<a id="op-fea97b0e5a2aef"></a>
### Has order specific amounts

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_has_order_specific_amounts`

**Inputs** sales\_order.

**Explicit results** true · any(generator of tax.charge\_type equals “Actual” for tax drawn from sales\_order.taxes).

**Local steps**

- If (flt(sales\_order.discount\_amount) and not flt(sales\_order.additional\_discount\_percentage)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(sales\_order.discount\_amount) → not flt(sales\_order.additional\_discount\_percentage).
  - Return true.
- Return any(generator of tax.charge\_type equals “Actual” for tax drawn from sales\_order.taxes).
  - Draw tax from sales\_order.taxes.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L194) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L942) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L439)

<a id="op-64e1e52e5f6177"></a>
### Get sales order headers

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_sales_order_headers`

**Inputs** sales\_orders.

**Record and data access** read “Sales Order” via get\_all.

**Explicit results** list() · headers.

**Local steps**

- Set sales\_orders from list of so for so drawn from sales\_orders where so.
  - Draw so from sales\_orders, keep a combination only if (so).
- If not sales\_orders.
  - Return list().
- Set headers from Platform.get\_all(“Sales Order”, filters = mapping(“name” → tuple(“in”, sales\_orders)), fields = list(“name as sales\_order”, expanded SALES\_ORDER\_HEADER\_FIELDS)).
- Set taxes from get\_sales\_order\_taxes(sales\_orders).
- For each header in headers.
  - Set header.taxes from taxes.get(header.sales\_order, list()).
- Return headers.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L938) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L435)

<a id="op-e5d0b1db7f0d76"></a>
### Get sales order taxes

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_sales_order_taxes`

**Inputs** sales\_orders.

**Explicit results** taxes.

**Local steps**

- Set tax from Platform.qb.DocType(“Sales Taxes and Charges”).
- Set rows from nested operand in the contract(nested operand in the contract).orderby(tax.parent).orderby(tax.idx).run(as\_dict = true).
  - Draw field from SALES\_ORDER\_TAX\_KEY\_FIELDS.
- Set taxes from mapping().
- For each row in rows.
  - Evaluate taxes.setdefault(row.parent, list()).append(row).
- Return taxes.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L191) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L939) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L436)

<a id="op-1ad6c841d96c23"></a>
### Create dn wo so

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_create_dn_wo_so`

**Inputs** pick\_list, delivery\_note = no value.

**Explicit results** create\_delivery\_wo\_so(pick\_list, “Delivery Note”, delivery\_note).

**Local steps**

- Return create\_delivery\_wo\_so(pick\_list, “Delivery Note”, delivery\_note).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L924) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L421)

<a id="op-18fe03f66089f9"></a>
### Create delivery wo so

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_create_delivery_wo_so`

**Inputs** pick\_list, target, target\_doc = no value, selected\_locations = no value.

**State and service calls** request new\_doc for target · call save on target\_doc.

**Explicit results** target\_doc.

**Local steps**

- If not target\_doc.
  - Set target\_doc from Platform.new\_doc(target).
- Set target\_doc.company from pick\_list.company.
- If not target\_doc.customer.
  - Set target\_doc.customer from pick\_list.customer.
- Set item\_table\_mapper\_without\_so from mapping(“doctype” → formatted text {target} Item, “field\_map” → mapping(“rate” → “rate”, “name” → “name”, “parent” → empty text)).
- Evaluate map\_pl\_locations(pick\_list, item\_table\_mapper\_without\_so, target\_doc, selected\_locations = selected\_locations).
- Set target\_doc.flags.ignore\_mandatory from true.
- If target equals “Sales Invoice”.
  - Set target\_doc.update\_stock from 1.
- Evaluate target\_doc.save().
- Return target\_doc.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L920) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L417)

<a id="op-901c958921afe5"></a>
### Create dn for pick lists

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_create_dn_for_pick_lists`

**Inputs** source\_name, target\_doc = no value, kwargs = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Pick List” via get\_doc · read “Sales Order” via get\_all · resolve a document from Platform.parse\_json(delivery\_note) via get\_doc.

**Explicit results** delivery\_note.

**Local steps**

- If kwargs is identical to no value.
  - Set kwargs from mapping().
- If isinstance(kwargs, str).
  - Set kwargs from json.loads(kwargs).
- Set pick\_list from Platform.get\_doc(“Pick List”, source\_name).
- Evaluate pick\_list.check\_permission(“read”).
- Evaluate validate\_item\_locations(pick\_list).
- Set sales\_order\_arg from kwargs.get(“sales\_order”).
- Set customer\_arg from kwargs.get(“customer”).
- If sales\_order\_arg.
  - Set sales\_orders from set(sales\_order\_arg).
- Otherwise.
  - Set sales\_orders from set of row.sales\_order for row drawn from pick\_list.locations where row.sales\_order.
    - Draw row from pick\_list.locations, keep a combination only if (row.sales\_order).
  - If customer\_arg.
    - Set sales\_orders from Platform.get\_all(“Sales Order”, filters = mapping(“customer” → customer\_arg, “name” → list(“in”, list(sales\_orders))), pluck = “name”).
- Set delivery\_note from create\_delivery\_from\_so(pick\_list, sales\_orders, “Delivery Note”, target\_doc = target\_doc, kwargs = kwargs).
- If (not sales\_order\_arg and not all(generator of item.sales\_order for item drawn from pick\_list.locations)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not sales\_order\_arg → not all(generator of item.sales\_order for item drawn from pick\_list.locations).
  - Draw item from pick\_list.locations.
  - If isinstance(delivery\_note, str).
    - Set delivery\_note from Platform.get\_doc(Platform.parse\_json(delivery\_note)).
  - Set delivery\_note from create\_delivery\_wo\_so(pick\_list, “Delivery Note”, delivery\_note, set((kwargs.get(“filtered\_children”) or list()))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.get(“filtered\_children”) → list().
- Return delivery\_note.

**Values supplied outside this operation** effective access from pick\_list.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L921) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L418)

<a id="op-38962d54bff68e"></a>
### Create dn with so

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_create_dn_with_so`

**Inputs** sales\_dict, pick\_list.

**Explicit results** create\_delivery\_with\_so(sales\_dict, pick\_list, “Delivery Note”).

**Local steps**

- Return create\_delivery\_with\_so(sales\_dict, pick\_list, “Delivery Note”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L923) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L420)

<a id="op-2df73507e00765"></a>
### Create delivery with so

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_create_delivery_with_so`

**Inputs** sales\_dict, pick\_list, target.

**State and service calls** call save on document.

**Explicit results** documents.

**Local steps**

- Set documents from list().
- For each key in sales\_dict.
  - Set document from create\_delivery\_from\_so(pick\_list, sales\_dict at key, target).
  - If (document and document.get(“items”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in document → document.get(“items”).
    - Set document.flags.ignore\_mandatory from true.
    - If target equals “Sales Invoice”.
      - Set document.update\_stock from 1.
    - Evaluate document.save().
    - Evaluate documents.append(document).
- Return documents.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L919) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L416)

<a id="op-3bee59acd90ce0"></a>
### Create dn from so

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_create_dn_from_so`

**Inputs** pick\_list, sales\_order\_list, delivery\_note = no value, kwargs = no value.

**Explicit results** create\_delivery\_from\_so(pick\_list, sales\_order\_list, “Delivery Note”, target\_doc = delivery\_note, kwargs = kwargs).

**Local steps**

- Return create\_delivery\_from\_so(pick\_list, sales\_order\_list, “Delivery Note”, target\_doc = delivery\_note, kwargs = kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L922) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L419)

<a id="op-93514c54b93b2e"></a>
### Create delivery from so

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_create_delivery_from_so`

**Inputs** pick\_list, sales\_order\_list, target, target\_doc = no value, kwargs = no value.

**Explicit results** target\_doc · no value.

**Local steps**

- If not sales\_order\_list.
  - Return target\_doc.
- If kwargs is identical to no value.
  - Set kwargs from mapping().
- Set item\_table\_mapper from mapping(“doctype” → formatted text {target} Item, “field\_map” → mapping(“rate” → “rate”, “name” → “so\_detail”, “parent” → “against\_sales\_order” when target equals “Delivery Note”, otherwise “sales\_order”), ….
  - Value choice on target equals “Delivery Note” — true gives “against\_sales\_order”, false gives “sales\_order”.
- Set selected\_locations from set((kwargs.get(“filtered\_children”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.get(“filtered\_children”) → list().
- Set mapper\_kwargs from mapping(“skip\_item\_mapping” → true, “ignore\_pricing\_rule” → pick\_list.ignore\_pricing\_rule).
- Set target\_doc from create\_delivery\_note\_from\_sales\_order(next(iter(sales\_order\_list)), target\_doc, kwargs = mapper\_kwargs) when target equals “Delivery Note”, otherwise create\_sales\_invoice\_from\_sales\_order(next(iter(sales\_o ….
  - Value choice on target equals “Delivery Note” — true gives create\_delivery\_note\_from\_sales\_order(next(iter(sales\_order\_list)), target\_doc, kwargs = mapper\_kwargs), false gives create\_sales\_invoice\_from\_sales\_order(next(iter(sales\_order\_list)), target\_doc, args = mapper\_kwargs).
- If not target\_doc.
  - Return no value.
- For each so in sales\_order\_list.
  - Evaluate map\_pl\_locations(pick\_list, item\_table\_mapper, target\_doc, so, …).
- Return target\_doc.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L917) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L414)

<a id="op-1e909f28d261ec"></a>
### Map pl locations

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_map_pl_locations`

**Inputs** pick\_list, item\_mapper, target\_doc, sales\_order = no value, selected\_locations = no value.

**Record and data access** resolve a document from “Sales Order” via get\_doc · read “Sales Order” via get\_value.

**Local steps**

- Set sales\_order\_items from mapping of d.name → d for d drawn from Platform.get\_doc(“Sales Order”, sales\_order).items when sales\_order, otherwise mapping().
  - Value choice on sales\_order — true gives mapping of d.name → d for d drawn from Platform.get\_doc(“Sales Order”, sales\_order).items, false gives mapping().
  - Draw d from Platform.get\_doc(“Sales Order”, sales\_order).items.
- Set condition from item\_mapper.get(“condition”).
- Set moved\_serial\_nos from get\_moved\_serial\_nos(list of location for location drawn from pick\_list.locations where location.sales\_order equals sales\_order).
  - Draw location from pick\_list.locations, keep a combination only if (location.sales\_order equals sales\_order).
- For each location in pick\_list.locations.
  - If (location.sales\_order differs from sales\_order or location.product\_bundle\_item).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in location.sales\_order differs from sales\_order → location.product\_bundle\_item.
    - Continue with the next iteration or loop test.
  - If (flt(location.picked\_qty) − flt(location.delivered\_qty)) ≤ 0.
    - Continue with the next iteration or loop test.
  - If (selected\_locations and location.name does not belong to selected\_locations).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in selected\_locations → location.name does not belong to selected\_locations.
    - Continue with the next iteration or loop test.
  - Set sales\_order\_item from sales\_order\_items.get(location.sales\_order\_item).
  - If (sales\_order\_item and condition and not condition(sales\_order\_item)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sales\_order\_item → condition → not condition(sales\_order\_item).
    - Continue with the next iteration or loop test.
  - Set source\_doc from (sales\_order\_item or location).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sales\_order\_item → location.
  - Set child\_item from map\_child\_doc(source\_doc, target\_doc, item\_mapper).
  - If child\_item.
    - Set child\_item.against\_pick\_list from pick\_list.name.
    - Set child\_item.pick\_list\_item from location.name.
    - Set child\_item.warehouse from location.warehouse.
    - Set child\_item.qty from (flt((location.picked\_qty − location.delivered\_qty)) ÷ (flt(child\_item.conversion\_factor) or 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(child\_item.conversion\_factor) → 1.
    - Set child\_item.batch\_no from location.batch\_no.
    - Set child\_item.serial\_no from get\_pending\_serial\_nos(location, moved\_serial\_nos).
    - Set child\_item.use\_serial\_batch\_fields from location.use\_serial\_batch\_fields.
    - If not child\_item.qty.
      - Evaluate target\_doc.items.remove(child\_item).
      - Continue with the next iteration or loop test.
    - Evaluate update\_child\_item(source\_doc, child\_item, target\_doc).
- If sales\_order.
  - Evaluate add\_product\_bundles\_to\_target(pick\_list, target\_doc, item\_mapper, sales\_order, …).
- Evaluate set\_target\_missing\_values(target\_doc).
- Set target\_doc.company from pick\_list.company.
- If sales\_order.
  - Set target\_doc.customer from Platform.get\_value(“Sales Order”, sales\_order, “customer”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L195) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L943) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L440)

<a id="op-1fe606c70dca19"></a>
### Get moved serial nos

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_moved_serial_nos`

**Inputs** locations, moved\_qty\_field = “delivered\_qty”.

**Explicit results** mapping of row → set of entry.serial\_no.lower() for entry drawn from entries where entry.serial\_no for tuple(row, entries) drawn from moved.items().

**Local steps**

- Set moved from get\_moved\_entries(list of row.name for row drawn from locations where (row.serial\_no and row.get(moved\_qty\_field))).
  - Draw row from locations, keep a combination only if ((row.serial\_no and row.get(moved\_qty\_field))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.serial\_no → row.get(moved\_qty\_field).
- Return mapping of row → set of entry.serial\_no.lower() for entry drawn from entries where entry.serial\_no for tuple(row, entries) drawn from moved.items().
  - Draw tuple(row, entries) from moved.items().
  - Draw entry from entries, keep a combination only if (entry.serial\_no).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L934) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L431)

<a id="op-4643aea785dcf0"></a>
### Get pending serial nos

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_pending_serial_nos`

**Inputs** location, moved\_serial\_nos, moved\_qty\_field = “delivered\_qty”.

**Explicit results** location.serial\_no · whitespace '\\n'.join(pending\_serial\_nos at slice no value to pending\_qty).

**Local steps**

- If not location.get(moved\_qty\_field).
  - Return location.serial\_no.
- Set moved from moved\_serial\_nos.get(location.name, set()).
- Set pending\_serial\_nos from list of number for number drawn from get\_serial\_nos(location.serial\_no) where number.lower() does not belong to moved.
  - Draw number from get\_serial\_nos(location.serial\_no), keep a combination only if (number.lower() does not belong to moved).
- Set pending\_qty from max(cint((flt(location.picked\_qty) − flt(location.get(moved\_qty\_field)))), 0).
- Return whitespace '\\n'.join(pending\_serial\_nos at slice no value to pending\_qty).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L936) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L433)

<a id="op-c0c4de580fca41"></a>
### Get moved entries

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_moved_entries`

**Inputs** pick\_list\_items.

**Record and data access** read doctype via get\_all.

**Explicit results** mapping() · moved.

**Local steps**

- If not pick\_list\_items.
  - Return mapping().
- Set pick\_list\_item\_by\_voucher\_detail from mapping().
- For each doctype in tuple(“Delivery Note Item”, “Sales Invoice Item”, “Stock Entry Detail”).
  - Evaluate pick\_list\_item\_by\_voucher\_detail.update(Platform.get\_all(doctype, filters = mapping(“pick\_list\_item” → tuple(“in”, pick\_list\_items), “docstatus” → 1), fields = list(“name”, “pick\_list\_item”), as\_list = true)).
- If not pick\_list\_item\_by\_voucher\_detail.
  - Return mapping().
- Set bundle from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set entries from nested operand in the contract(nested operand in the contract).select(bundle.voucher\_detail\_no, entry.serial\_no, entry.batch\_no, entry.qty).where((((nested operand in the contract(nested operand in the con ….
- Set moved from defaultdict(list).
- For each row in entries.
  - Evaluate moved at pick\_list\_item\_by\_voucher\_detail at row.voucher\_detail\_no.append(row).
- Return moved.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L185) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L933) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L430)

<a id="op-c057ede36c4d2c"></a>
### Add product bundles to delivery note

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_add_product_bundles_to_delivery_note`

**Inputs** pick\_list, delivery\_note, item\_mapper, sales\_order = no value.

**Declared result** no value.

**Explicit results** add\_product\_bundles\_to\_target(pick\_list, delivery\_note, item\_mapper, sales\_order).

**Local steps**

- Return add\_product\_bundles\_to\_target(pick\_list, delivery\_note, item\_mapper, sales\_order).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L913) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L410)

<a id="op-b3ba4ec41f8c8c"></a>
### Add product bundles to target

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_add_product_bundles_to_target`

**Inputs** pick\_list, target\_doc, item\_mapper, sales\_order = no value, selected\_locations = no value.

**Declared result** no value.

**Record and data access** resolve a document from “Sales Order Item” via get\_doc.

**Local steps**

- Set product\_bundles from pick\_list.\_get\_product\_bundles().
- If selected\_locations.
  - Set selected\_bundles from set of row.sales\_order\_item for row drawn from pick\_list.locations where (row.product\_bundle\_item and row.name belongs to selected\_locations).
    - Draw row from pick\_list.locations, keep a combination only if ((row.product\_bundle\_item and row.name belongs to selected\_locations)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.product\_bundle\_item → row.name belongs to selected\_locations.
  - Set product\_bundles from list of so\_row for so\_row drawn from product\_bundles where so\_row belongs to selected\_bundles.
    - Draw so\_row from product\_bundles, keep a combination only if (so\_row belongs to selected\_bundles).
- Set product\_bundle\_qty\_map from pick\_list.\_get\_product\_bundle\_qty\_map(product\_bundles).
- For each so\_row in product\_bundles.
  - Set sales\_order\_item from Platform.get\_doc(“Sales Order Item”, so\_row).
  - If (sales\_order and sales\_order\_item.parent differs from sales\_order).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sales\_order → sales\_order\_item.parent differs from sales\_order.
    - Continue with the next iteration or loop test.
  - Set pending\_qty from pick\_list.\_compute\_picked\_qty\_for\_bundle(so\_row, product\_bundle\_qty\_map.get(so\_row, mapping()), pending\_only = true).
  - If not pending\_qty.
    - Continue with the next iteration or loop test.
  - Set target\_bundle\_item from map\_child\_doc(sales\_order\_item, target\_doc, item\_mapper).
  - Set target\_bundle\_item.qty from flt((pending\_qty ÷ (flt(target\_bundle\_item.conversion\_factor) or 1)), target\_bundle\_item.precision(“qty”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(target\_bundle\_item.conversion\_factor) → 1.
  - Set target\_bundle\_item.against\_pick\_list from pick\_list.name.
  - Evaluate update\_child\_item(sales\_order\_item, target\_bundle\_item, target\_doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L914) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L411)

<a id="op-c1a3f6649c63b0"></a>
### Create stock entry

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_create_stock_entry`

**Inputs** pick\_list.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from Platform.parse\_json(pick\_list) via get\_doc · read “Material Request” via get\_value.

**State and service calls** request new\_doc for “Stock Entry” · msgprint with translated “All picked items have already been transferred against this Pick List”.

**Explicit results** Platform.msgprint(translated “All picked items have already been transferred against this Pick List”) · stock\_entry.as\_dict().

**Local steps**

- Set pick\_list from Platform.get\_doc(Platform.parse\_json(pick\_list)).
- Evaluate pick\_list.check\_permission(“read”).
- Evaluate validate\_item\_locations(pick\_list).
- Set stock\_entry from Platform.new\_doc(“Stock Entry”).
- Set stock\_entry.pick\_list from pick\_list.get(“name”).
- Set stock\_entry.purpose from pick\_list.get(“purpose”).
- Set stock\_entry.company from pick\_list.get(“company”).
- Set job\_card from (pick\_list.get(“material\_request”) and Platform.db.get\_value(“Material Request”, pick\_list.get(“material\_request”), “job\_card”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pick\_list.get(“material\_request”) → Platform.db.get\_value(“Material Request”, pick\_list.get(“material\_request”), “job\_card”).
- If job\_card.
  - Set stock\_entry from update\_stock\_entry\_based\_on\_job\_card(pick\_list, stock\_entry, job\_card).
- Otherwise.
  - If pick\_list.get(“work\_order”).
    - Set stock\_entry from update\_stock\_entry\_based\_on\_work\_order(pick\_list, stock\_entry).
  - Otherwise.
    - If pick\_list.get(“material\_request”).
      - Set stock\_entry from update\_stock\_entry\_based\_on\_material\_request(pick\_list, stock\_entry).
    - Otherwise.
      - Set stock\_entry from update\_stock\_entry\_items\_with\_no\_reference(pick\_list, stock\_entry).
- Evaluate stock\_entry.set\_stock\_entry\_type().
- If not stock\_entry.get(“items”).
  - Return Platform.msgprint(translated “All picked items have already been transferred against this Pick List”).
- Evaluate stock\_entry.set\_missing\_values().
- Return stock\_entry.as\_dict().

**Values supplied outside this operation** effective access from pick\_list.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L925) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L422)

<a id="op-b23fc6a7fb80d0"></a>
### Get pending work orders

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_pending_work_orders`

**Inputs** doctype, txt, searchfield, start, page\_length, filters, as\_dict.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** nested operand in the contract(nested operand in the contract).limit(cint(page\_length)).offset(start).run(as\_dict = as\_dict).

**Local steps**

- Evaluate Platform.has\_permission(“Pick List”, throw = true).
- Set wo from Platform.qb.DocType(“Work Order”).
- Return nested operand in the contract(nested operand in the contract).limit(cint(page\_length)).offset(start).run(as\_dict = as\_dict).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Pick List”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L311) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L66)

<a id="op-3682d07637ecda"></a>
### Get item details

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_item_details`

**Inputs** item\_code, uom = no value, warehouse = no value, company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_value.

**Explicit results** details.

**Local steps**

- Evaluate Platform.has\_permission(“Pick List”, throw = true).
- Set details from Platform.db.get\_value(“Item”, item\_code, “stock\_uom”, as\_dict = 1).
- Set details.uom from (uom or details.stock\_uom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in uom → details.stock\_uom.
- If uom.
  - Evaluate details.update(get\_conversion\_factor(item\_code, uom)).
- If warehouse.
  - Set details.actual\_qty from flt(get\_actual\_qty(item\_code, warehouse)).
- If company.
  - Set details.company\_total\_stock from get\_company\_total\_stock(item\_code, company).
- Return details.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Pick List”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L63)

<a id="op-7e2713c9f55760"></a>
### Get actual qty

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_actual_quantity`

**Inputs** item\_code, warehouse.

**Record and data access** read “Bin” via get\_value.

**Explicit results** Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse), “actual\_qty”).

**Local steps**

- Return Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse), “actual\_qty”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0766.json#L1061) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L57)

<a id="op-3da34a2b3ea555"></a>
### Update delivery note item

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_update_delivery_note_item`

**Inputs** source, target, delivery\_note.

**Explicit results** update\_child\_item(source, target, delivery\_note).

**Local steps**

- Return update\_child\_item(source, target, delivery\_note).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L212) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L960) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L457)

<a id="op-3dd1b93c41426f"></a>
### Update child item

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_update_child_item`

**Inputs** source, target, target\_doc.

**Record and data access** read “Project” via get\_value.

**Local steps**

- Set cost\_center from Platform.db.get\_value(“Project”, target\_doc.project, “cost\_center”).
- If not cost\_center.
  - Set cost\_center from get\_cost\_center(source.item\_code, “Item”, target\_doc.company).
- If not cost\_center.
  - Set cost\_center from get\_cost\_center(source.item\_group, “Item Group”, target\_doc.company).
- Set target.cost\_center from cost\_center.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L210) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L958) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L455)

<a id="op-863e85e94fde3c"></a>
### Get cost center

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_cost_center`

**Inputs** for\_item, from\_doctype, company.

**Record and data access** read “Item Default” via get\_value.

**Explicit results** Platform.db.get\_value(“Item Default”, fieldname = list(“buying\_cost\_center”), filters = mapping(“parent” → for\_item, “parenttype” → from\_doctype, “company” → company)).

**Local steps**

- Return Platform.db.get\_value(“Item Default”, fieldname = list(“buying\_cost\_center”), filters = mapping(“parent” → for\_item, “parenttype” → from\_doctype, “company” → company)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L926) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L423)

<a id="op-b30d50bf0fc45e"></a>
### Set delivery note missing values

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_set_delivery_note_missing_values`

**Inputs** target.

**Explicit results** set\_target\_missing\_values(target).

**Local steps**

- Return set\_target\_missing\_values(target).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L207) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L955) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L452)
