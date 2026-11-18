# Inventory and warehouses · operations 35

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Packed item

[Record definition](../../../../data/record-types/packed_item.json)

<a id="op-7adef094c9de83"></a>
### Packed Item.set actual and projected qty

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_packeditem_set_actual_and_projected_qty`

**Inputs** self.

**Record and data access** read “Bin” via get\_value.

**Local steps**

- Set \_bin from Platform.db.get\_value(“Bin”, mapping(“item\_code” → self.item\_code, “warehouse” → self.warehouse), list(“actual\_qty”, “projected\_qty”), as\_dict = true).
- Set self.actual\_qty from \_bin.actual\_qty when \_bin, otherwise 0.
  - Value choice on \_bin — true gives \_bin.actual\_qty, false gives 0.
- Set self.projected\_qty from \_bin.projected\_qty when \_bin, otherwise 0.
  - Value choice on \_bin — true gives \_bin.projected\_qty, false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L904) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L401)

<a id="op-8c7abcdea927ce"></a>
### Make packing list

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_make_packing_list`

**Inputs** doc, order\_packed\_items = no value.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If doc.get(“is\_subcontracted”).
  - Return no value.
- If (doc.get(“\_action”) and doc.\_action equals “update\_after\_submit”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“\_action”) → doc.\_action equals “update\_after\_submit”.
  - Return no value.
- Set tuple(parent\_items\_price, reset) from tuple(mapping(), false).
- Set set\_price\_from\_children from Platform.get\_single\_value(“Selling Settings”, “editable\_bundle\_item\_rates”).
- Set stale\_packed\_items\_table from get\_indexed\_packed\_items\_table(doc).
- If order\_packed\_items is identical to no value.
  - Set order\_packed\_items from get\_order\_packed\_items(doc).
- Set returned\_packed\_qty from get\_returned\_packed\_qty(order\_packed\_items) when doc.get(“is\_return”), otherwise mapping().
  - Value choice on doc.get(“is\_return”) — true gives get\_returned\_packed\_qty(order\_packed\_items), false gives mapping().
- Set reset from reset\_packing\_list(doc).
- For each item\_row in doc.get(“items”).
  - If is\_product\_bundle(item\_row.item\_code).
    - Set order\_row from item\_row.name when doc.doctype equals “Sales Order”, otherwise get\_order\_row(doc, item\_row).
      - Value choice on doc.doctype equals “Sales Order” — true gives item\_row.name, false gives get\_order\_row(doc, item\_row).
    - Set so\_packed\_items from list(order\_packed\_items.get(order\_row, list())).
    - Set component\_rows from get\_component\_order\_rows(doc, item\_row.item\_code, get\_product\_bundle\_items(item\_row.item\_code), so\_packed\_items).
    - Set return\_qty from get\_return\_qty(doc, item\_row, component\_rows, returned\_packed\_qty).
    - For each tuple(bundle\_item, so\_packed\_item) in component\_rows.
      - Set item\_data from get\_packed\_item\_details(bundle\_item.item\_code, doc.company).
      - Set locations from get\_pick\_list\_locations(doc, item\_row, bundle\_item, item\_data, …).
      - For each location in (locations or list(no value)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in locations → list(no value).
        - Set pi\_row from add\_packed\_item\_row(doc = doc, packing\_item = bundle\_item, main\_item\_row = item\_row, packed\_items\_table = stale\_packed\_items\_table, …).
        - Evaluate update\_packed\_item\_basic\_data(item\_row, pi\_row, bundle\_item, item\_data, …).
        - If (so\_packed\_item and so\_packed\_item.name belongs to return\_qty).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in so\_packed\_item → so\_packed\_item.name belongs to return\_qty.
          - Set pi\_row.qty from return\_qty at so\_packed\_item.name.
        - Evaluate update\_packed\_item\_stock\_data(item\_row, pi\_row, bundle\_item, item\_data, …).
        - Evaluate update\_packed\_item\_price\_data(pi\_row, item\_data, doc).
        - If location.
          - Evaluate update\_packed\_item\_with\_pick\_list\_info(item\_row, pi\_row, location).
        - If set\_price\_from\_children.
          - Evaluate update\_product\_bundle\_rate(parent\_items\_price, pi\_row, item\_row).
- If not reset.
  - Evaluate remove\_unused\_pick\_list\_rows(doc, stale\_packed\_items\_table).
- If parent\_items\_price.
  - Evaluate set\_product\_bundle\_rate\_amount(doc, parent\_items\_price).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “editable\_bundle\_item\_rates”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L15)

<a id="op-528216cb0912d5"></a>
### Is product bundle

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_is_product_bundle`

**Inputs** item\_code.

**Declared result** bool.

**Record and data access** read “Product Bundle” via exists.

**Explicit results** bool(Platform.db.exists(“Product Bundle”, mapping(“new\_item\_code” → item\_code, “disabled” → 0))).

**Local steps**

- Return bool(Platform.db.exists(“Product Bundle”, mapping(“new\_item\_code” → item\_code, “disabled” → 0))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L14)

<a id="op-f1918b13c4a7cd"></a>
### Get indexed packed items table

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_get_indexed_packed_items_table`

**Inputs** doc.

**Explicit results** indexed\_table.

**Local steps**

- Set link\_field from get\_packed\_item\_link\_field(doc).
- Set indexed\_table from mapping().
- For each packed\_item in doc.get(“packed\_items”).
  - Set parent\_row from no value when doc.is\_new(), otherwise packed\_item.parent\_detail\_docname.
    - Value choice on doc.is\_new() — true gives no value, false gives packed\_item.parent\_detail\_docname.
  - If (doc.is\_new() and packed\_item.get(link\_field)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.is\_new() → packed\_item.get(link\_field).
    - Set parent\_row from packed\_item.get(link\_field).
  - Set key from tuple(packed\_item.parent\_item, packed\_item.item\_code, parent\_row).
  - Evaluate indexed\_table.setdefault(key, list()).append(packed\_item).
- If doc.is\_new().
  - Set needed\_counts from Counter(generator of tuple(item\_row.item\_code, bundle\_item.item\_code, no value) for item\_row drawn from doc.get(“items”), then bundle\_item drawn from get\_product\_bundle\_items(item\_row.item\_code)).
    - Draw item\_row from doc.get(“items”).
    - Draw bundle\_item from get\_product\_bundle\_items(item\_row.item\_code).
  - Set indexed\_table from mapping of key → rows for tuple(key, rows) drawn from indexed\_table.items() where (key at 2 or len(rows) equals needed\_counts at key).
    - Draw tuple(key, rows) from indexed\_table.items(), keep a combination only if ((key at 2 or len(rows) equals needed\_counts at key)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in key at 2 → len(rows) equals needed\_counts at key.
- Return indexed\_table.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L10)

<a id="op-6064bf0cc45d52"></a>
### Reset packing list

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_reset_packing_list`

**Inputs** doc.

**Explicit results** reset\_table.

**Local steps**

- Set reset\_table from false.
- Set doc\_before\_save from doc.get\_doc\_before\_save().
- If doc\_before\_save.
  - Set items\_before\_save from list of tuple(item.name, item.item\_code) for item drawn from doc\_before\_save.get(“items”).
    - Draw item from doc\_before\_save.get(“items”).
  - Set items\_after\_save from list of tuple(item.name, item.item\_code) for item drawn from doc.get(“items”).
    - Draw item from doc.get(“items”).
  - Set reset\_table from items\_before\_save differs from items\_after\_save.
- Otherwise.
  - Set reset\_table from true.
- If reset\_table.
  - Evaluate doc.set(“packed\_items”, list()).
- Return reset\_table.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L17)

<a id="op-088ac5b8d149bd"></a>
### Get product bundle items

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_product_bundle_items`

**Inputs** item\_code.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set product\_bundle from Platform.qb.DocType(“Product Bundle”).
- Set product\_bundle\_item from Platform.qb.DocType(“Product Bundle Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(product\_bundle\_item.item\_code, product\_bundle\_item.qty, product\_bundle\_item.uom, product\_bundle\_item.description).where((product\_bundle ….
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L899) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L396)

<a id="op-7efa858d3431c6"></a>
### Add packed item row

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_add_packed_item_row`

**Inputs** doc, packing\_item, main\_item\_row, packed\_items\_table, reset, linked\_packed\_item = no value, location = no value.

**Explicit results** pi\_row.

**Local steps**

- Set tuple(exists, pi\_row) from tuple(false, mapping()).
- Set key from get\_packed\_item\_key(doc, main\_item\_row, packing\_item.item\_code, packed\_items\_table, …).
- If stale\_rows bound to packed\_items\_table.get(key).
  - Set tuple(pi\_row, exists) from tuple(stale\_rows.pop(get\_stale\_row\_idx(stale\_rows, location)), true).
- If not exists.
  - Set pi\_row from doc.append(“packed\_items”, mapping()).
- Otherwise.
  - If reset.
    - Set pi\_row.idx from no value.
    - If doc.is\_new().
      - Set pi\_row.name from no value.
    - Set pi\_row from doc.append(“packed\_items”, pi\_row).
- Evaluate pi\_row.set(get\_packed\_item\_link\_field(doc), linked\_packed\_item).
- If (doc.get(“reserve\_stock”) and (doc.is\_new() or not exists)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“reserve\_stock”) → (doc.is\_new() or not exists).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.is\_new() → not exists.
  - Set pi\_row.reserve\_stock from 1.
- Return pi\_row.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L9)

<a id="op-59967d48d0a095"></a>
### Get packed item key

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_packed_item_key`

**Inputs** doc, main\_item\_row, item\_code, packed\_items\_table, linked\_packed\_item = no value.

**Explicit results** order\_key · tuple(main\_item\_row.item\_code, item\_code, no value when doc.is\_new(), otherwise main\_item\_row.name).

**Local steps**

- Set order\_key from tuple(main\_item\_row.item\_code, item\_code, linked\_packed\_item).
- If (doc.is\_new() and linked\_packed\_item and packed\_items\_table.get(order\_key)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.is\_new() → linked\_packed\_item → packed\_items\_table.get(order\_key).
  - Return order\_key.
- Return tuple(main\_item\_row.item\_code, item\_code, no value when doc.is\_new(), otherwise main\_item\_row.name).
  - Value choice on doc.is\_new() — true gives no value, false gives main\_item\_row.name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L893) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L390)

<a id="op-a42af3bd898931"></a>
### Get stale row idx

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_stale_row_idx`

**Inputs** stale\_rows, location = no value.

**Explicit results** 0 · next(generator of idx for tuple(idx, row) drawn from enumerate(stale\_rows) where is\_packed\_from(row, location), 0).

**Local steps**

- If not location.
  - Return 0.
- Return next(generator of idx for tuple(idx, row) drawn from enumerate(stale\_rows) where is\_packed\_from(row, location), 0).
  - Draw tuple(idx, row) from enumerate(stale\_rows), keep a combination only if (is\_packed\_from(row, location)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L902) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L399)

<a id="op-ce9a2f788f18a7"></a>
### Get location filters

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_location_filters`

**Inputs** row.

**Declared result** dict.

**Explicit results** mapping(“serial\_and\_batch\_bundle” → row.serial\_and\_batch\_bundle) · mapping(“warehouse” → row.warehouse).

**Local steps**

- If row.serial\_and\_batch\_bundle.
  - Return mapping(“serial\_and\_batch\_bundle” → row.serial\_and\_batch\_bundle).
- Return mapping(“warehouse” → row.warehouse).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L888) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L385)

<a id="op-cea6ca160644b1"></a>
### Is packed from

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_is_packed_from`

**Inputs** pi\_row, location.

**Explicit results** true · tuple(pi\_row.warehouse, (pi\_row.batch\_no or empty text)) equals tuple(location.warehouse, (location.batch\_no or empty text)).

**Local steps**

- Bind dependencies get\_serial\_nos.
- Set serial\_nos from set of number.lower() for number drawn from get\_serial\_nos(pi\_row.serial\_no).
  - Draw number from get\_serial\_nos(pi\_row.serial\_no).
- If (serial\_nos bitwise and set of number.lower() for number drawn from get\_serial\_nos(location.serial\_no)).
  - Draw number from get\_serial\_nos(location.serial\_no).
  - Return true.
- Return tuple(pi\_row.warehouse, (pi\_row.batch\_no or empty text)) equals tuple(location.warehouse, (location.batch\_no or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pi\_row.batch\_no → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in location.batch\_no → empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L903) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L400)

<a id="op-86cf06f841de5d"></a>
### Remove unused pick list rows

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_remove_unused_pick_list_rows`

**Inputs** doc, packed\_items\_table.

**Local steps**

- Set pick\_list\_rows from set of item.name for item drawn from doc.get(“items”) where item.get(“against\_pick\_list”).
  - Draw item from doc.get(“items”), keep a combination only if (item.get(“against\_pick\_list”)).
- For each rows in packed\_items\_table.values().
  - For each row in rows.
    - If row.parent\_detail\_docname belongs to pick\_list\_rows.
      - Evaluate doc.remove(row).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L906) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L403)

<a id="op-e61598602a9455"></a>
### Get packed item details

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_get_packed_item_details`

**Inputs** item\_code, company.

**Explicit results** query.run(as\_dict = true) at 0.

**Local steps**

- Set item from Platform.qb.DocType(“Item”).
- Set item\_default from Platform.qb.DocType(“Item Default”).
- Set query from nested operand in the contract(nested operand in the contract).on((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand in t ….
- Return query.run(as\_dict = true) at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0758.json#L2527) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L13)

<a id="op-62d8bf4e41f4e8"></a>
### Update packed item basic data

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_update_packed_item_basic_data`

**Inputs** main\_item\_row, pi\_row, packing\_item, item\_data, so\_packed\_item = no value.

**Local steps**

- Set pi\_row.parent\_item from main\_item\_row.item\_code.
- Set pi\_row.parent\_detail\_docname from (main\_item\_row.name or main\_item\_row.idx).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in main\_item\_row.name → main\_item\_row.idx.
- Set pi\_row.item\_code from packing\_item.item\_code.
- Set pi\_row.item\_name from item\_data.item\_name.
- Set pi\_row.uom from item\_data.stock\_uom.
- Set pi\_row.qty from get\_packed\_qty(main\_item\_row, packing\_item, item\_data, so\_packed\_item).
- Set pi\_row.conversion\_factor from main\_item\_row.conversion\_factor.
- Set pi\_row.delivered\_by\_supplier from main\_item\_row.get(“delivered\_by\_supplier”).
- If not pi\_row.description.
  - Set pi\_row.description from packing\_item.get(“description”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L251) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L19)

<a id="op-aca30ce0fafbda"></a>
### Get packed qty

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_packed_qty`

**Inputs** main\_item\_row, packing\_item, item\_data, so\_packed\_item = no value.

**Explicit results** flt((get\_component\_stock\_qty\_per\_unit(packing\_item, item\_data.stock\_uom, so\_packed\_item) × flt(main\_item\_row.stock\_qty)), Platform.get\_precision(“Packed Item”, “qty”)).

**Local steps**

- Return flt((get\_component\_stock\_qty\_per\_unit(packing\_item, item\_data.stock\_uom, so\_packed\_item) × flt(main\_item\_row.stock\_qty)), Platform.get\_precision(“Packed Item”, “qty”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L896) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L393)

<a id="op-1e9626f0a19049"></a>
### Get component stock qty per unit

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_component_stock_qty_per_unit`

**Inputs** packing\_item, stock\_uom, so\_packed\_item = no value.

**Explicit results** get\_ordered\_qty\_per\_unit(qty\_per\_unit, so\_packed\_item).

**Local steps**

- Set qty\_per\_unit from (flt(packing\_item.qty) × get\_component\_conversion\_factor(packing\_item, stock\_uom)).
- Return get\_ordered\_qty\_per\_unit(qty\_per\_unit, so\_packed\_item).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L885) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L382)

<a id="op-3e95dd0025a58a"></a>
### Get ordered qty per unit

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_ordered_qty_per_unit`

**Inputs** qty\_per\_unit, so\_packed\_item = no value.

**Explicit results** so\_packed\_item.qty\_per\_unit · qty\_per\_unit.

**Local steps**

- If (so\_packed\_item and so\_packed\_item.qty\_per\_unit).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in so\_packed\_item → so\_packed\_item.qty\_per\_unit.
  - Set ordered\_qty from flt((qty\_per\_unit × flt(so\_packed\_item.order\_stock\_qty)), Platform.get\_precision(“Packed Item”, “qty”)).
  - If ordered\_qty differs from flt(so\_packed\_item.qty).
    - Return so\_packed\_item.qty\_per\_unit.
- Return qty\_per\_unit.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L892) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L389)

<a id="op-e31c392c7eda3d"></a>
### Get component conversion factor

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_component_conversion_factor`

**Inputs** packing\_item, stock\_uom.

**Explicit results** 1.0 · (flt(get\_conversion\_factor(packing\_item.item\_code, uom).get(“conversion\_factor”)) or 1.0).

**Local steps**

- Set uom from packing\_item.get(“uom”).
- If (not uom or uom equals stock\_uom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not uom → uom equals stock\_uom.
  - Return 1.0.
- Return (flt(get\_conversion\_factor(packing\_item.item\_code, uom).get(“conversion\_factor”)) or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(get\_conversion\_factor(packing\_item.item\_code, uom).get(“conversion\_factor”)) → 1.0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L883) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L380)

<a id="op-5dec8837cbd39f"></a>
### Update packed item stock data

`operation_enterprise_stock_record_definitions_packed_item_business_behavior_update_packed_item_stock_data`

**Inputs** main\_item\_row, pi\_row, packing\_item, item\_data, doc, so\_packed\_item = no value.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- If (so\_packed\_item and not doc.get(“is\_return”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in so\_packed\_item → not doc.get(“is\_return”).
  - If (so\_packed\_item.reserve\_stock or not pi\_row.warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in so\_packed\_item.reserve\_stock → not pi\_row.warehouse.
    - Set pi\_row.warehouse from so\_packed\_item.warehouse.
- If not pi\_row.warehouse.
  - Set fetch\_warehouse from (doc.get(“is\_pos”) or item\_data.is\_stock\_item or not item\_data.default\_warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“is\_pos”) → item\_data.is\_stock\_item → not item\_data.default\_warehouse.
  - Set pi\_row.warehouse from main\_item\_row.warehouse when (fetch\_warehouse and main\_item\_row.warehouse), otherwise item\_data.default\_warehouse.
    - Value choice on (fetch\_warehouse and main\_item\_row.warehouse) — true gives main\_item\_row.warehouse, false gives item\_data.default\_warehouse.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fetch\_warehouse → main\_item\_row.warehouse.
- If not pi\_row.target\_warehouse.
  - Set pi\_row.target\_warehouse from main\_item\_row.get(“target\_warehouse”).
- If not item\_data.is\_stock\_item.
  - Set pi\_row.reserve\_stock from 0.
- Set bin from get\_packed\_item\_bin\_qty(packing\_item.item\_code, pi\_row.warehouse).
- Set pi\_row.actual\_qty from flt(bin.get(“actual\_qty”)).
- Set pi\_row.projected\_qty from flt(bin.get(“projected\_qty”)).
- Set pi\_row.use\_serial\_batch\_fields from Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L254) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L21)

<a id="op-1817a30121c64f"></a>
### Get order packed items

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_order_packed_items`

**Inputs** doc.

**Declared result** dict.

**Explicit results** get\_packed\_items\_of\_order\_rows(set of row for item drawn from doc.get(“items”) where row bound to get\_order\_row(doc, item), doc.doctype when doc.get(“is\_return”), otherwise “Sales Order”).

**Local steps**

- Return get\_packed\_items\_of\_order\_rows(set of row for item drawn from doc.get(“items”) where row bound to get\_order\_row(doc, item), doc.doctype when doc.get(“is\_return”), otherwise “Sales Order”).
  - Draw item from doc.get(“items”), keep a combination only if (row bound to get\_order\_row(doc, item)).
  - Value choice on doc.get(“is\_return”) — true gives doc.doctype, false gives “Sales Order”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L890) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L387)

<a id="op-7b73a88c8389ed"></a>
### Get linked packed item

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_linked_packed_item`

**Inputs** doc, so\_packed\_item.

**Explicit results** so\_packed\_item.name.

**Local steps**

- If (so\_packed\_item and doc.doctype differs from “Sales Order”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in so\_packed\_item → doc.doctype differs from “Sales Order”.
  - Return so\_packed\_item.name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L887) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L384)

<a id="op-79aa90b1341712"></a>
### Get packed item link field

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_packed_item_link_field`

**Inputs** doc.

**Explicit results** “return\_against\_packed\_item” when doc.get(“is\_return”), otherwise “sales\_order\_packed\_item”.

**Local steps**

- Return “return\_against\_packed\_item” when doc.get(“is\_return”), otherwise “sales\_order\_packed\_item”.
  - Value choice on doc.get(“is\_return”) — true gives “return\_against\_packed\_item”, false gives “sales\_order\_packed\_item”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L894) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L391)

<a id="op-feb499d01ddf84"></a>
### Get order row

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_order_row`

**Inputs** doc, item\_row.

**Explicit results** item\_row.get(“so\_detail”) · item\_row.get(“dn\_detail” when doc.doctype equals “Delivery Note”, otherwise (Platform.scrub(doc.doctype) + “\_item”)).

**Local steps**

- If not doc.get(“is\_return”).
  - Return item\_row.get(“so\_detail”).
- Return item\_row.get(“dn\_detail” when doc.doctype equals “Delivery Note”, otherwise (Platform.scrub(doc.doctype) + “\_item”)).
  - Value choice on doc.doctype equals “Delivery Note” — true gives “dn\_detail”, false gives (Platform.scrub(doc.doctype) + “\_item”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L891) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L388)

<a id="op-7f25a846a96bae"></a>
### Get packed items of order rows

`operation_enterprise_binding_enterprise_stock_doctype_packed_item_packed_item_get_packed_items_of_order_rows`

**Inputs** order\_rows, doctype = “Sales Order”.

**Declared result** dict.

**Explicit results** mapping() · order\_packed\_items.

**Local steps**

- If not order\_rows.
  - Return mapping().
- Set packed\_item from Platform.qb.DocType(“Packed Item”).
- Set order\_item from Platform.qb.DocType(formatted text {doctype} Item).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where((nested operand in the contract equal ….
- Set order\_packed\_items from mapping().
- For each row in rows.
  - Set row.qty\_per\_unit from (flt(row.qty) ÷ flt(row.order\_stock\_qty)) when flt(row.order\_stock\_qty), otherwise 0.
    - Value choice on flt(row.order\_stock\_qty) — true gives (flt(row.qty) ÷ flt(row.order\_stock\_qty)), false gives 0.
  - Evaluate order\_packed\_items.setdefault(row.parent\_detail\_docname, list()).append(row).
- Return order\_packed\_items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L895) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L392)
