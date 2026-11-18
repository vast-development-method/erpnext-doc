# Inventory and warehouses · operations 36

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Packed item

[Record definition](../../../../data/record-types/packed_item.json)

<a id="op-8b36172b78bd44"></a>
### Pop order packed item

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_pop_order_packed_item`

**Inputs** so\_packed\_items, parent\_item, item\_code.

**Explicit results** so\_packed\_items.pop(idx).

**Local steps**

- For each tuple(idx, row) in enumerate(so\_packed\_items).
  - If (row.parent\_item equals parent\_item and row.item\_code equals item\_code).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.parent\_item equals parent\_item → row.item\_code equals item\_code.
    - Return so\_packed\_items.pop(idx).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L905) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L402)

<a id="op-26c89e616c2866"></a>
### Get component order rows

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_component_order_rows`

**Inputs** doc, parent\_item, components, so\_packed\_items.

**Declared result** list at tuple.

**Explicit results** list of tuple(component, pop\_order\_packed\_item(so\_packed\_items, parent\_item, component.item\_code)) for component drawn from components · component\_rows.

**Local steps**

- If not doc.get(“is\_return”).
  - Return list of tuple(component, pop\_order\_packed\_item(so\_packed\_items, parent\_item, component.item\_code)) for component drawn from components.
    - Draw component from components.
- Set delivered\_rows from mapping().
- For each row in so\_packed\_items.
  - Evaluate delivered\_rows.setdefault((row.sales\_order\_packed\_item or row.name), list()).append(row).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.sales\_order\_packed\_item → row.name.
- Set first\_rows from list of rows at 0 for rows drawn from delivered\_rows.values().
  - Draw rows from delivered\_rows.values().
- Set component\_rows from list().
- For each component in components.
  - Set first\_row from pop\_order\_packed\_item(first\_rows, parent\_item, component.item\_code).
  - Set rows from delivered\_rows at (first\_row.sales\_order\_packed\_item or first\_row.name) when first\_row, otherwise list(no value).
    - Value choice on first\_row — true gives delivered\_rows at (first\_row.sales\_order\_packed\_item or first\_row.name), false gives list(no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in first\_row.sales\_order\_packed\_item → first\_row.name.
  - Evaluate component\_rows.extend(generator of tuple(component, row) for row drawn from rows).
    - Draw row from rows.
- Return component\_rows.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L884) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L381)

<a id="op-a836fc6bc32ab0"></a>
### Get order packed item pairs

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_order_packed_item_pairs`

**Inputs** doc.

**Declared result** list at tuple.

**Explicit results** pairs.

**Local steps**

- Set order\_packed\_items from get\_order\_packed\_items(doc).
- Set link\_field from get\_packed\_item\_link\_field(doc).
- Set pairs from list().
- For each item in doc.get(“items”).
  - Set so\_packed\_items from list(order\_packed\_items.get(get\_order\_row(doc, item), list())).
  - Set so\_packed\_items\_by\_name from mapping of row.name → row for row drawn from so\_packed\_items.
    - Draw row from so\_packed\_items.
  - For each packed\_item in doc.get(“packed\_items”).
    - If packed\_item.parent\_detail\_docname differs from (item.name or item.idx).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.name → item.idx.
      - Continue with the next iteration or loop test.
    - If so\_packed\_item bound to (so\_packed\_items\_by\_name.get(packed\_item.get(link\_field)) or pop\_order\_packed\_item(so\_packed\_items, packed\_item.parent\_item, packed\_item.item\_code)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in so\_packed\_items\_by\_name.get(packed\_item.get(link\_field)) → pop\_order\_packed\_item(so\_packed\_items, packed\_item.parent\_item, packed\_item.item\_code).
      - Evaluate pairs.append(tuple(packed\_item, so\_packed\_item)).
- Return pairs.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L889) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L386)

<a id="op-2f528b8403be99"></a>
### Get pick list locations

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_pick_list_locations`

**Inputs** doc, main\_item\_row, packing\_item, item\_data, so\_packed\_item, packed\_items\_table.

**Record and data access** read “Pick List Item” via get\_all.

**Explicit results** list() · allocate\_picked\_qty(pl\_rows, qty).

**Local steps**

- If not main\_item\_row.get(“against\_pick\_list”).
  - Return list().
- Set filters from mapping(“item\_code” → packing\_item.item\_code, “sales\_order\_item” → main\_item\_row.get(“so\_detail”), “parent” → main\_item\_row.against\_pick\_list).
- If so\_packed\_item.
  - Set filters at “product\_bundle\_item” from so\_packed\_item.name.
- Set pl\_rows from Platform.get\_all(“Pick List Item”, filters, list(“name”, “item\_code”, “warehouse”, “batch\_no”, …), order\_by = “qty desc”).
- If not pl\_rows.
  - Return list().
- Set key from get\_packed\_item\_key(doc, main\_item\_row, packing\_item.item\_code, packed\_items\_table, …).
- Set stale\_rows from packed\_items\_table.get(key, list()).
- Evaluate pl\_rows.sort(key = deferred anonymous expression).
- Set qty from get\_packed\_qty(main\_item\_row, packing\_item, item\_data, so\_packed\_item).
- Return allocate\_picked\_qty(pl\_rows, qty).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L898) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L395)

<a id="op-f323aaf678c176"></a>
### Allocate picked qty

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_allocate_picked_qty`

**Inputs** pl\_rows, qty.

**Explicit results** allocate\_qty(pl\_rows, qty, deferred anonymous expression).

**Local steps**

- Set precision from Platform.get\_precision(“Pick List Item”, “delivered\_qty”).
- Return allocate\_qty(pl\_rows, qty, deferred anonymous expression).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L881) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L378)

<a id="op-ac12cb9d51e0b9"></a>
### Allocate qty

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_allocate_qty`

**Inputs** rows, qty, get\_available\_qty.

**Explicit results** locations.

**Local steps**

- Set qty\_precision from Platform.get\_precision(“Packed Item”, “qty”).
- Set locations from list().
- For each row in rows.
  - Set row.pack\_qty from min(get\_available\_qty(row), qty).
  - If row.pack\_qty &gt; 0.
    - Evaluate locations.append(row).
    - Set qty from flt((qty − row.pack\_qty), qty\_precision).
- If not locations.
  - Set rows at 0.pack\_qty from 0.
  - Set locations from rows at slice no value to 1.
- Update locations at negative 1.pack\_qty using + qty.
- Return locations.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L882) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L379)

<a id="op-cd5b751ecd088b"></a>
### Get returned packed qty

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_returned_packed_qty`

**Inputs** order\_packed\_items.

**Declared result** dict.

**Explicit results** mapping() · dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(packed\_item.return\_against\_packed\_item).run()).

**Local steps**

- Set names from list of row.name for rows drawn from order\_packed\_items.values(), then row drawn from rows.
  - Draw rows from order\_packed\_items.values().
  - Draw row from rows.
- If not names.
  - Return mapping().
- Set packed\_item from Platform.qb.DocType(“Packed Item”).
- Return dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(packed\_item.return\_against\_packed\_item).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L901) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L398)

<a id="op-bf2bedbfa627f8"></a>
### Get return qty

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_return_qty`

**Inputs** doc, item\_row, component\_rows, returned\_packed\_qty.

**Declared result** dict.

**Explicit results** mapping() · return\_qty.

**Local steps**

- If not doc.get(“is\_return”).
  - Return mapping().
- Set delivered\_rows from mapping().
- For each tuple(component, so\_packed\_item) in component\_rows.
  - If so\_packed\_item.
    - Evaluate delivered\_rows.setdefault(id(component), list()).append(so\_packed\_item).
- Set precision from Platform.get\_precision(“Packed Item”, “qty”).
- Set return\_qty from mapping().
- For each rows in delivered\_rows.values().
  - <a id="op-bf2bedbfa627f8-guard-16"></a>If len(rows) &lt; 2.
    - Continue with the next iteration or loop test.
  - Set qty from flt((negative sum(generator of row.qty\_per\_unit for row drawn from rows) × flt(item\_row.stock\_qty)), precision).
    - Draw row from rows.
  - Set locations from allocate\_qty(rows, qty, deferred anonymous expression).
  - Evaluate return\_qty.update(mapping of row.name → 0 for row drawn from rows).
    - Draw row from rows.
  - For each row in locations.
    - Set return\_qty at row.name from negative flt(row.pack\_qty, precision).
    - Set returned\_packed\_qty at row.name from (flt(returned\_packed\_qty.get(row.name)) + row.pack\_qty).
- Return return\_qty.

**Derived branch illustrations**

- At the comparison len(rows) &lt; 2, length of rows = 1 selects the branch that continues with the next loop iteration. With length of rows = 2, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-bf2bedbfa627f8-guard-16)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L900) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L397)

<a id="op-46e1c34ff18ee5"></a>
### Update packed item with pick list info

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_update_packed_item_with_pick_list_info`

**Inputs** main\_item\_row, pi\_row, location.

**Local steps**

- If not is\_packed\_from(pi\_row, location).
  - Set pi\_row.serial\_no from no value.
- Set pi\_row.qty from flt(location.pack\_qty, pi\_row.precision(“qty”)).
- Set pi\_row.warehouse from location.warehouse.
- Set pi\_row.batch\_no from location.batch\_no.
- Set pi\_row.serial\_no from get\_packed\_serial\_nos(main\_item\_row, pi\_row, location).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L255) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L22)

<a id="op-488d1fda2717d0"></a>
### Get packed serial nos

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_packed_serial_nos`

**Inputs** main\_item\_row, pi\_row, pl\_row.

**Explicit results** whitespace '\\n'.join(serial\_nos at slice no value to qty).

**Local steps**

- Bind dependencies get\_pending\_serial\_nos.
- Bind dependencies get\_serial\_nos.
- Set serial\_nos from get\_serial\_nos(pi\_row.serial\_no).
- Set qty from cint(pi\_row.qty).
- If (len(serial\_nos) &lt; qty and pl\_row.serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(serial\_nos) &lt; qty → pl\_row.serial\_no.
  - Set delivered from get\_delivered\_component\_serial\_nos(main\_item\_row, pl\_row) when pl\_row.delivered\_qty, otherwise set().
    - Value choice on pl\_row.delivered\_qty — true gives get\_delivered\_component\_serial\_nos(main\_item\_row, pl\_row), false gives set().
  - Set kept from set of number.lower() for number drawn from serial\_nos.
    - Draw number from serial\_nos.
  - Set pending from get\_serial\_nos(get\_pending\_serial\_nos(pl\_row, mapping(pl\_row.name → delivered))).
  - Update serial\_nos using + list of number for number drawn from pending where number.lower() does not belong to kept.
    - Draw number from pending, keep a combination only if (number.lower() does not belong to kept).
- Return whitespace '\\n'.join(serial\_nos at slice no value to qty).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L897) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L394)

<a id="op-95e80885e66069"></a>
### Get delivered component serial nos

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_delivered_component_serial_nos`

**Inputs** main\_item\_row, pl\_row.

**Explicit results** delivered\_serial\_nos at tuple(so\_detail, pl\_row.item\_code, pl\_row.warehouse, (pl\_row.batch\_no or empty text)).

**Local steps**

- Bind dependencies get\_delivered\_bundle\_component\_qty.
- Set so\_detail from main\_item\_row.get(“so\_detail”).
- Set delivered\_serial\_nos from get\_delivered\_bundle\_component\_qty(main\_item\_row.against\_pick\_list, set(so\_detail)) at 1.
- Return delivered\_serial\_nos at tuple(so\_detail, pl\_row.item\_code, pl\_row.warehouse, (pl\_row.batch\_no or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pl\_row.batch\_no → empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L886) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L383)

<a id="op-564983804fc321"></a>
### Update packed item price data

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_update_packed_item_price_data`

**Inputs** pi\_row, item\_data, doc.

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- If pi\_row.rate.
  - Return no value.
- Set item\_doc from Platform.get\_cached\_doc(“Item”, pi\_row.item\_code).
- Set ctx from ItemDetailsCtx(pi\_row.as\_dict().copy()).
- Evaluate ctx.update(mapping(“company” → doc.get(“company”), “price\_list” → doc.get(“selling\_price\_list”), “currency” → doc.get(“currency”), “conversion\_rate” → doc.get(“conversion\_rate”))).
- If not ctx.transaction\_date.
  - Evaluate ctx.update(mapping(“transaction\_date” → doc.get(“transaction\_date”))).
- Set rate from get\_price\_list\_rate(ctx, item\_doc).get(“price\_list\_rate”).
- Set pi\_row.rate from (rate or item\_data.get(“valuation\_rate”) or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rate → item\_data.get(“valuation\_rate”) → 0.0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, pi\_row.item\_code).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L253) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L20)

<a id="op-e348d6928534b3"></a>
### Get packed item bin qty

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_get_packed_item_bin_quantity`

**Inputs** item, warehouse.

**Record and data access** read “Bin” via get\_values.

**Explicit results** bin\_data at 0 when bin\_data, otherwise mapping().

**Local steps**

- Set bin\_data from Platform.db.get\_values(“Bin”, fieldname = list(“actual\_qty”, “projected\_qty”), filters = mapping(“item\_code” → item, “warehouse” → warehouse), as\_dict = true).
- Return bin\_data at 0 when bin\_data, otherwise mapping().
  - Value choice on bin\_data — true gives bin\_data at 0, false gives mapping().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0758.json#L5024) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L243) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L12)

<a id="op-3f08e7e68462c1"></a>
### Update product bundle rate

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_update_product_bundle_rate`

**Inputs** parent\_items\_price, pi\_row, item\_row.

**Local steps**

- Set key from tuple(pi\_row.parent\_item, pi\_row.parent\_detail\_docname).
- Set rate from parent\_items\_price.get(key).
- If not rate.
  - Set parent\_items\_price at key from 0.0.
- Update parent\_items\_price at key using + flt(((pi\_row.rate × pi\_row.qty) ÷ item\_row.stock\_qty)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0758.json#L5342) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L256) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L23)

<a id="op-8e600d12fca67a"></a>
### Set product bundle rate amount

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_set_product_bundle_rate_amount`

**Inputs** doc, parent\_items\_price.

**Local steps**

- Set rate\_updated from false.
- For each item in doc.get(“items”).
  - Set bundle\_rate from parent\_items\_price.get(tuple(item.item\_code, item.name)).
  - If (bundle\_rate and bundle\_rate differs from item.rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in bundle\_rate → bundle\_rate differs from item.rate.
    - Set item.rate from bundle\_rate.
    - Set item.amount from flt((bundle\_rate × item.qty)).
    - Set item.margin\_rate\_or\_amount from 0.
    - Set item.discount\_percentage from 0.
    - Set item.discount\_amount from 0.
    - Set rate\_updated from true.
- If rate\_updated.
  - Evaluate doc.calculate\_taxes\_and\_totals().
  - Evaluate doc.set\_total\_in\_words().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0758.json#L5545) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L18)

<a id="op-9f79df56002b29"></a>
### On doctype update

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Packed Item”.

**Local steps**

- Evaluate Platform.db.add\_index(“Packed Item”, list(“item\_code”, “warehouse”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0758.json#L5890) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L16)

<a id="op-1841bfc1f1bc36"></a>
### Get items from product bundle

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_get_items_from_product_bundle`

**Inputs** row.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** items.

**Local steps**

- Set tuple(row, items) from tuple(ItemDetailsCtx(json.loads(row)), list()).
- Set bundled\_items from get\_product\_bundle\_items(row at “item\_code”).
- For each item in bundled\_items.
  - Evaluate row.update(mapping(“item\_code” → item.item\_code, “qty” → ((flt(row at “quantity”) × flt(item.qty)) × get\_component\_conversion\_factor(item, no value)), “conversion\_rate” → 1, “currency” → Platform.defaults. ….
  - Evaluate items.append(get\_item\_details(row)).
- Return items.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L11)

## Record · Packing slip

[Record definition](../../../../data/record-types/packing_slip.json)

<a id="op-fe6fd263511c28"></a>
### Packing Slip.initialize

`operation_enterprise_stock_record_definitions_packing_slip_business_behavior_packing_slip_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Declared result** no value.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.status\_updater from list(mapping(“target\_dt” → “Delivery Note Item”, “join\_field” → “dn\_detail”, “target\_field” → “packed\_qty”, “target\_parent\_dt” → “Delivery Note”, …), mapping(“target\_dt” → “Packed Item”, “join\_field” → “pi ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0760.json#L968) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L280) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L40)

<a id="op-9ed6c726fe528c"></a>
### Packing Slip.validate

`operation_enterprise_stock_record_definitions_packing_slip_business_behavior_packing_slip_validate`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Bind dependencies validate\_uom\_is\_integer.
- Evaluate self.validate\_delivery\_note().
- Evaluate self.validate\_case\_nos().
- Evaluate self.validate\_items().
- Evaluate validate\_uom\_is\_integer(self, “stock\_uom”, “qty”).
- Evaluate validate\_uom\_is\_integer(self, “weight\_uom”, “net\_weight”).
- Evaluate self.set\_missing\_values().
- Evaluate self.calculate\_net\_total\_pkg().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate delivery note](operations-036.md#op-5c8bbf72804fee), [validate case nos](operations-036.md#op-c0094daafa3f56), [validate items](operations-037.md#op-c5f95a1604cfe4), [set missing values](operations-037.md#op-8d180f984191c2), [calculate net total pkg](operations-037.md#op-bdefd236935ba4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0760.json#L1303) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L284) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L44)

<a id="op-e46a486f9b9d78"></a>
### Packing Slip.on submit

`operation_enterprise_stock_record_definitions_packing_slip_business_behavior_packing_slip_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_prevdoc\_status().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0760.json#L1518) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L282) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L42)

<a id="op-b94c5d8de542a7"></a>
### Packing Slip.before cancel

`operation_enterprise_binding_enterprise_stock_doctype_packing_slip_packing_slip_packingslip_before_cancel`

**Inputs** self.

**Record and data access** read “Delivery Note” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Packing Slip cannot be cancelled as Delivery Note {0} is already submitted.”.format(Platform.bold(self.delivery\_note)).

**Local steps**

- If self.flags.cancelled\_by\_delivery\_note.
  - Return no value.
- If cint(Platform.db.get\_value(“Delivery Note”, self.delivery\_note, “docstatus”)) equals 1.
  - Call the validation error handler Platform.throw(translated “Packing Slip cannot be cancelled as Delivery Note {0} is already submitted.”.format(Platform.bold(self.delivery\_note))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L907) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L404)

<a id="op-046dc7ea36b07e"></a>
### Packing Slip.on cancel

`operation_enterprise_stock_record_definitions_packing_slip_business_behavior_packing_slip_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_prevdoc\_status().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0760.json#L1567) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L281) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L41)

<a id="op-5c8bbf72804fee"></a>
### Packing Slip.validate delivery note

`operation_enterprise_stock_record_definitions_packing_slip_business_behavior_packing_slip_validate_delivery_note`

**Inputs** self.

**Record and data access** read “Delivery Note” via get\_value.

**Explicit failure paths** validation helper — translated “A Packing Slip can only be created for Draft Delivery Note.”.format(self.delivery\_note).

**Local steps**

- If cint(Platform.db.get\_value(“Delivery Note”, self.delivery\_note, “docstatus”)) differs from 0.
  - Call the validation error handler Platform.throw(translated “A Packing Slip can only be created for Draft Delivery Note.”.format(self.delivery\_note)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L286) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L46)

<a id="op-c0094daafa3f56"></a>
### Packing Slip.validate case nos

`operation_enterprise_stock_record_definitions_packing_slip_business_behavior_packing_slip_validate_case_numbers`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The 'From Package No.' field must neither be empty nor it's value less than 1.” · validation helper — translated “'To Package No.' cannot be less than 'From Package No.'” · validation helper — translated “Package No(s) already in use. Try from Package No {0}”.format(self.get\_recommended\_case\_no()).

**Local steps**

- If cint(self.from\_case\_no) ≤ 0.
  - Call the validation error handler Platform.throw(translated “The 'From Package No.' field must neither be empty nor it's value less than 1.”).
- Otherwise.
  - If not self.to\_case\_no.
    - Set self.to\_case\_no from self.from\_case\_no.
  - Otherwise.
    - If cint(self.to\_case\_no) &lt; cint(self.from\_case\_no).
      - Call the validation error handler Platform.throw(translated “'To Package No.' cannot be less than 'From Package No.'”).
    - Otherwise.
      - Set ps from Platform.qb.DocType(“Packing Slip”).
      - Set res from nested operand in the contract(nested operand in the contract).select(ps.name).where(((nested operand in the contract.delivery\_note equals nested operand in the contract.delivery\_note bitwise and nested op ….run().
      - If res.
        - Call the validation error handler Platform.throw(translated “Package No(s) already in use. Try from Package No {0}”.format(self.get\_recommended\_case\_no())).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get recommended case no](operations-037.md#op-5833794f9a6a1b).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L285) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L45)
