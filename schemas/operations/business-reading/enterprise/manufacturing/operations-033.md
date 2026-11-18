# Production · operations 33

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Production plan

[Record definition](../../../../data/record-types/production_plan.json)

<a id="op-410a3cbfd6fdd8"></a>
### Get planned qty by order row

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_planned_qty_by_order_row`

**Inputs** plans.

**Explicit results** mapping of tuple(row.parent, row.sales\_order\_item) → flt(row.qty) for row drawn from rows.

**Local steps**

- Set plan\_item from Platform.qb.DocType(“Production Plan Item”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.isin(plans)).groupby(plan\_item.parent, pl ….
- Return mapping of tuple(row.parent, row.sales\_order\_item) → flt(row.qty) for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L182) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L919)

<a id="op-34142d435bcb97"></a>
### Get qty to request

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_qty_to_request`

**Inputs** item, draft\_qty.

**Record and data access** read “UOM” via get\_cached\_value.

**Explicit results** qty\_to\_request.

**Local steps**

- Set qty\_to\_request from flt(((flt(item.quantity) − flt(item.requested\_qty)) − (flt(draft\_qty.get(item.name)) ÷ (flt(item.conversion\_factor) or 1))), item.precision(“quantity”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.conversion\_factor) → 1.
- If (qty\_to\_request &gt; 0 and Platform.get\_cached\_value(“UOM”, item.uom, “must\_be\_whole\_number”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty\_to\_request &gt; 0 → Platform.get\_cached\_value(“UOM”, item.uom, “must\_be\_whole\_number”).
  - Set qty\_to\_request from ceil(qty\_to\_request).
- Return qty\_to\_request.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, item.uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L187) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L924)

<a id="op-8b7e007dc59d38"></a>
### Download raw materials

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_download_raw_materials`

**Inputs** doc, warehouses = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- If isinstance(doc, str).
  - Set doc from Platform.\_dict(json.loads(doc)).
- Set item\_list from list(list(“Item Code”, “Item Name”, “Description”, “Stock UOM”, …)).
- Set doc.warehouse from no value.
- Set Platform.flags.show\_qty\_in\_stock\_uom from 1.
- Set items from get\_items\_for\_material\_requests(doc, warehouses = warehouses, get\_parent\_warehouse\_data = true).
- Set precision from Platform.get\_precision(“Material Request Plan Item”, “quantity”).
- Set duplicate\_item\_wh\_list from Platform.\_dict().
- For each d in items.
  - Set key from tuple(d.get(“item\_code”), d.get(“warehouse”)).
  - If key belongs to duplicate\_item\_wh\_list.
    - Set merged from duplicate\_item\_wh\_list at key.
    - Update merged.quantity using + (\_stock\_quantity(d) ÷ merged.conversion\_factor).
    - Set merged.row at 12 from flt(merged.quantity, precision).
    - Set merged.row at 5 from flt((flt(merged.row at 5) + flt(d.get(“required\_bom\_qty”))), precision).
    - Continue with the next iteration or loop test.
  - Set rm\_data from list(d.get(“item\_code”), d.get(“item\_name”), d.get(“description”), d.get(“stock\_uom”), …).
  - Set duplicate\_item\_wh\_list at key from Platform.\_dict(row = rm\_data, conversion\_factor = (flt(d.get(“conversion\_factor”)) or 1), quantity = flt(d.get(“quantity”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.get(“conversion\_factor”)) → 1.
  - Evaluate item\_list.append(rm\_data).
  - If not doc.get(“for\_warehouse”).
    - Set row from mapping(“item\_code” → d.get(“item\_code”)).
    - For each bin\_dict in \_get\_bin\_details(row, doc.company, all\_warehouse = true).
      - If d.get(“warehouse”) equals bin\_dict.get(“warehouse”).
        - Continue with the next iteration or loop test.
      - Evaluate item\_list.append(list(empty text, empty text, empty text, empty text, …)).
- Evaluate build\_csv\_response(item\_list, doc.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1663) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L903)

<a id="op-ffa53003d0275b"></a>
### Get exploded items

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_exploded_items`

**Inputs** item\_details, company, bom\_no, include\_non\_stock\_items, planned\_qty = 1, doc = no value.

**Explicit results** item\_details.

**Local steps**

- Set bei from Platform.qb.DocType(“BOM Explosion Item”).
- Set bom from Platform.qb.DocType(“BOM”).
- Set item from Platform.qb.DocType(“Item”).
- Set item\_default from Platform.qb.DocType(“Item Default”).
- Set item\_uom from Platform.qb.DocType(“UOM Conversion Detail”).
- Set data from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
  - Value choice on include\_non\_stock\_items — true gives item.is\_stock\_item.isin(list(0, 1)), false gives item.is\_stock\_item equals 1.
- For each d in data.
  - If (not d.conversion\_factor and d.purchase\_uom).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.conversion\_factor → d.purchase\_uom.
    - Set d.conversion\_factor from get\_uom\_conversion\_factor(d.item\_code, d.purchase\_uom).
  - Evaluate item\_details.setdefault(d.get(“item\_code”), d).
- Return item\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L906)

<a id="op-55c57942653681"></a>
### Get planned process loss percentage

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_planned_process_loss_percentage`

**Inputs** bom\_no.

**Record and data access** read “BOM” via get\_cached\_value.

**Explicit results** get\_planned\_loss\_percentage(Platform.get\_cached\_value(“BOM”, bom\_no, “process\_loss\_percentage”)).

**Local steps**

- Return get\_planned\_loss\_percentage(Platform.get\_cached\_value(“BOM”, bom\_no, “process\_loss\_percentage”)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“BOM”, bom\_no, “process\_loss\_percentage”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L918)

<a id="op-0f69cd2ca5d023"></a>
### Get plan process loss percentage

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_plan_process_loss_percentage`

**Inputs** plan, bom\_no.

**Explicit results** 0 · get\_planned\_process\_loss\_percentage(bom\_no).

**Local steps**

- If not plan.get(“consider\_process\_loss”).
  - Return 0.
- Return get\_planned\_process\_loss\_percentage(bom\_no).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L915)

<a id="op-87bd23c190200a"></a>
### Get planned loss percentage

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_planned_loss_percentage`

**Inputs** loss\_percentage.

**Explicit results** loss\_percentage when loss\_percentage &lt; 100, otherwise 0.

**Local steps**

- Set loss\_percentage from flt(loss\_percentage).
- Return loss\_percentage when loss\_percentage &lt; 100, otherwise 0.
  - Value choice on loss\_percentage &lt; 100 — true gives loss\_percentage, false gives 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L917)

<a id="op-d4563dabff9c14"></a>
### Get qty before process loss

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_qty_before_process_loss`

**Inputs** qty, loss\_percentage, uom.

**Explicit results** flt(qty) · round\_up\_to\_whole\_unit((flt(qty) ÷ (1 − (loss\_percentage ÷ 100))), uom).

**Local steps**

- Set loss\_percentage from get\_planned\_loss\_percentage(loss\_percentage).
- If not loss\_percentage.
  - Return flt(qty).
- Return round\_up\_to\_whole\_unit((flt(qty) ÷ (1 − (loss\_percentage ÷ 100))), uom).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L923)

<a id="op-f7cc77a4eccb62"></a>
### Round up to whole unit

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_round_up_to_whole_unit`

**Inputs** qty, uom.

**Record and data access** read “UOM” via get\_cached\_value.

**Explicit results** ceil(flt(qty, Platform.get\_precision(“Work Order”, “qty”))) · qty.

**Local steps**

- If (uom and Platform.get\_cached\_value(“UOM”, uom, “must\_be\_whole\_number”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in uom → Platform.get\_cached\_value(“UOM”, uom, “must\_be\_whole\_number”).
  - Return ceil(flt(qty, Platform.get\_precision(“Work Order”, “qty”))).
- Return qty.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L961)

<a id="op-473a68f0b0918b"></a>
### Get uom conversion factor

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_uom_conversion_factor`

**Inputs** item\_code, uom.

**Record and data access** read “Item” via get\_cached\_value · read “UOM Conversion Detail” via get\_value.

**Explicit results** (conversion\_factor or get\_uom\_conv\_factor(uom, item.stock\_uom)).

**Local steps**

- Set item from Platform.get\_cached\_value(“Item”, item\_code, list(“variant\_of”, “stock\_uom”), as\_dict = true).
- Set conversion\_factor from Platform.db.get\_value(“UOM Conversion Detail”, mapping(“parent” → item\_code, “uom” → uom), “conversion\_factor”).
- If (not conversion\_factor and item.variant\_of).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not conversion\_factor → item.variant\_of.
  - Set conversion\_factor from Platform.db.get\_value(“UOM Conversion Detail”, mapping(“parent” → item.variant\_of, “uom” → uom), “conversion\_factor”).
- Return (conversion\_factor or get\_uom\_conv\_factor(uom, item.stock\_uom)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conversion\_factor → get\_uom\_conv\_factor(uom, item.stock\_uom).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, list(“variant\_of”, “stock\_uom”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1696) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L936)

<a id="op-a24f6f221e517f"></a>
### Get subitems

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_subitems`

**Inputs** doc, data, item\_details, bom\_no, company, include\_non\_stock\_items, include\_subcontracted\_items, parent\_qty, planned\_qty = 1.

**Explicit results** mapping of key → value for tuple(key, value) drawn from item\_details.items() where not value.get(“is\_phantom\_item”).

**Local steps**

- Set bom\_item from Platform.qb.DocType(“BOM Item”).
- Set bom from Platform.qb.DocType(“BOM”).
- Set item from Platform.qb.DocType(“Item”).
- Set item\_default from Platform.qb.DocType(“Item Default”).
- Set item\_uom from Platform.qb.DocType(“UOM Conversion Detail”).
- Set items from nested operand in the contract(nested operand in the contract).groupby(bom\_item.item\_code).orderby(bom\_item.idx).run(as\_dict = true).
  - Value choice on include\_non\_stock\_items — true gives item.is\_stock\_item.isin(list(0, 1)), false gives item.is\_stock\_item equals 1.
- For each d in items.
  - Set child\_bom from (d.line\_bom\_no or d.default\_bom).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.line\_bom\_no → d.default\_bom.
  - If tuple(d.item\_code, child\_bom) belongs to (data.get(“requested\_sub\_assemblies”) or tuple()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.get(“requested\_sub\_assemblies”) → tuple().
    - Continue with the next iteration or loop test.
  - Set explodable from (d.is\_phantom\_item or (data.get(“include\_exploded\_items”) and child\_bom)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.is\_phantom\_item → (data.get(“include\_exploded\_items”) and child\_bom).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.get(“include\_exploded\_items”) → child\_bom.
  - Set explode from (explodable and \_should\_explode\_subitem(d, include\_subcontracted\_items) and d.qty &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in explodable → \_should\_explode\_subitem(d, include\_subcontracted\_items) → d.qty &gt; 0.
  - If (not data.get(“include\_exploded\_items”) or not child\_bom or not explode).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not data.get(“include\_exploded\_items”) → not child\_bom → not explode.
    - Evaluate \_merge\_subitem(item\_details, d).
  - If explode.
    - Set qty from d.qty when d.is\_phantom\_item, otherwise get\_qty\_before\_process\_loss(d.qty, get\_plan\_process\_loss\_percentage(doc, child\_bom), d.stock\_uom).
      - Value choice on d.is\_phantom\_item — true gives d.qty, false gives get\_qty\_before\_process\_loss(d.qty, get\_plan\_process\_loss\_percentage(doc, child\_bom), d.stock\_uom).
    - Evaluate get\_subitems(doc, data, item\_details, child\_bom, …).
- Return mapping of key → value for tuple(key, value) drawn from item\_details.items() where not value.get(“is\_phantom\_item”).
  - Draw tuple(key, value) from item\_details.items(), keep a combination only if (not value.get(“is\_phantom\_item”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1694) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L934)

<a id="op-2fa5aa8c845860"></a>
### Merge subitem

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_merge_subitem`

**Inputs** item\_details, d.

**Explicit results** no value.

**Local steps**

- If d.item\_code belongs to item\_details.
  - Set item\_details at d.item\_code.qty from (item\_details at d.item\_code.qty + d.qty).
  - Return no value.
- If (not d.conversion\_factor and d.purchase\_uom).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.conversion\_factor → d.purchase\_uom.
  - Set d.conversion\_factor from get\_uom\_conversion\_factor(d.item\_code, d.purchase\_uom).
- Set item\_details at d.item\_code from d.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1704) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L944)

<a id="op-7970793111d737"></a>
### Should explode subitem

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_should_explode_subitem`

**Inputs** d, include\_subcontracted\_items.

**Explicit results** bool(((d.default\_material\_request\_type belongs to list(“Manufacture”, “Purchase”) and not d.is\_sub\_contracted) or (d.is\_sub\_contracted and include\_subcontracted\_items) or d.is\_phantom\_item)).

**Local steps**

- Return bool(((d.default\_material\_request\_type belongs to list(“Manufacture”, “Purchase”) and not d.is\_sub\_contracted) or (d.is\_sub\_contracted and include\_subcontracted\_items) or d.is\_phantom\_item)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (d.default\_material\_request\_type belongs to list(“Manufacture”, “Purchase”) and not d.is\_sub\_contracted) → (d.is\_sub\_contracted and include\_subcontracted\_items) → d.is\_phantom\_item.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.default\_material\_request\_type belongs to list(“Manufacture”, “Purchase”) → not d.is\_sub\_contracted.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_sub\_contracted → include\_subcontracted\_items.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L967)

<a id="op-c361e7171f3eb8"></a>
### Get material request items

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_material_request_items`

**Inputs** doc, row, sales\_order, company, ignore\_existing\_ordered\_qty, include\_safety\_stock, warehouse, target\_warehouse, bin\_dict, consumed\_qty, shortage\_bin, is\_transfer = false.

**Explicit results** item.

**Local steps**

- Set required\_qty from \_required\_qty\_for\_mr(row, ignore\_existing\_ordered\_qty, warehouse, shortage\_bin, …).
- Set item\_group\_defaults from get\_item\_group\_defaults(row.item\_code, company).
- Set purchase\_uom from get\_mr\_purchase\_uom(row).
- Set conversion\_factor from 1.0.
- If purchase\_uom.
  - Set conversion\_factor from (get\_conversion\_factor(row.item\_code, purchase\_uom).get(“conversion\_factor”) or 1.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_conversion\_factor(row.item\_code, purchase\_uom).get(“conversion\_factor”) → 1.0.
- Set uom from (purchase\_uom or row.get(“stock\_uom”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in purchase\_uom → row.get(“stock\_uom”).
- Set min\_order\_qty from flt(row.get(“min\_order\_qty”)) when doc.get(“consider\_minimum\_order\_qty”), otherwise 0.
  - Value choice on doc.get(“consider\_minimum\_order\_qty”) — true gives flt(row.get(“min\_order\_qty”)), false gives 0.
- If is\_transfer.
  - Set quantity from (round\_up\_whole\_uom(required\_qty, row.get(“stock\_uom”)) ÷ conversion\_factor).
- Otherwise.
  - Set quantity from round\_up\_whole\_uom(\_quantity\_in\_purchase\_uom(required\_qty, conversion\_factor, min\_order\_qty), uom).
- Set item from mapping(“item\_code” → row.item\_code, “item\_name” → row.item\_name, “quantity” → quantity, “conversion\_factor” → conversion\_factor, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in target\_warehouse → row.get(“source\_warehouse”) → row.get(“default\_warehouse”) → item\_group\_defaults.get(“default\_warehouse”).
- If not is\_transfer.
  - Evaluate \_keep\_stock\_qty\_whole(item, required\_qty).
- Return item.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1669) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L909)

<a id="op-6f277e98b7158d"></a>
### Consolidate subcontracted po

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_consolidate_subcontracted_po`

**Inputs** subcontracted\_po, subcontracted\_qty.

**Explicit results** mapping of key → value for tuple(key, value) drawn from subcontracted\_po.items() where value.

**Local steps**

- Set items\_to\_remove from defaultdict(list).
- For each tuple(supplier, items) in subcontracted\_po.items().
  - For each item in items.
    - Set ordered\_qty from flt(subcontracted\_qty.get(item.name)).
    - If flt(item.qty) ≤ ordered\_qty.
      - Evaluate items\_to\_remove at supplier.append(item).
    - Otherwise.
      - If ordered\_qty.
        - Update item.qty using − ordered\_qty.
  - Set subcontracted\_po at supplier from list of item for item drawn from items where item does not belong to items\_to\_remove at supplier.
    - Draw item from items, keep a combination only if (item does not belong to items\_to\_remove at supplier).
- Return mapping of key → value for tuple(key, value) drawn from subcontracted\_po.items() where value.
  - Draw tuple(key, value) from subcontracted\_po.items(), keep a combination only if (value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1661) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L901)

<a id="op-258a0322032c63"></a>
### Get requested sub assemblies

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_requested_sub_assemblies`

**Inputs** doc.

**Explicit results** requested\_sub\_assemblies.

**Local steps**

- Set requested\_sub\_assemblies from mapping().
- For each row in (doc.get(“sub\_assembly\_items”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“sub\_assembly\_items”) → list().
  - Set row from Platform.\_dict(row).
  - If row.type\_of\_manufacturing equals “Material Request”.
    - Evaluate requested\_sub\_assemblies.setdefault(row.production\_plan\_item, set()).add(tuple(row.production\_item, row.bom\_no)).
- Return requested\_sub\_assemblies.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L927)

<a id="op-88fb409170c966"></a>
### Round up whole uom

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_round_up_whole_uom`

**Inputs** quantity, uom.

**Record and data access** read “UOM” via get\_cached\_value.

**Explicit results** ceil(flt(quantity, Platform.get\_precision(“Material Request Plan Item”, “quantity”))) · quantity.

**Local steps**

- If (uom and Platform.get\_cached\_value(“UOM”, uom, “must\_be\_whole\_number”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in uom → Platform.get\_cached\_value(“UOM”, uom, “must\_be\_whole\_number”).
  - Return ceil(flt(quantity, Platform.get\_precision(“Material Request Plan Item”, “quantity”))).
- Return quantity.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L962)

<a id="op-8cf7ce62e32a26"></a>
### Get mr purchase uom

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_mr_purchase_uom`

**Inputs** row.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** item\_details.purchase\_uom.

**Local steps**

- Set item\_details from Platform.get\_cached\_value(“Item”, row.item\_code, list(“purchase\_uom”, “stock\_uom”), as\_dict = 1).
- If (row.get(“default\_material\_request\_type”) equals “Purchase” and item\_details.purchase\_uom and item\_details.purchase\_uom differs from item\_details.stock\_uom).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“default\_material\_request\_type”) equals “Purchase” → item\_details.purchase\_uom → item\_details.purchase\_uom differs from item\_details.stock\_uom.
  - Return item\_details.purchase\_uom.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.item\_code, list(“purchase\_uom”, “stock\_uom”), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L913)

<a id="op-253ae756fb0737"></a>
### Quantity in purchase uom

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_quantity_in_purchase_uom`

**Inputs** required\_qty, conversion\_factor, min\_order\_qty = 0.

**Explicit results** quantity.

**Local steps**

- Set min\_order\_qty from min(min\_order\_qty, required\_qty).
- Set precision from Platform.get\_precision(“Material Request Plan Item”, “quantity”).
- Set quantity from flt((required\_qty ÷ conversion\_factor), precision).
- If (min\_order\_qty and (quantity × conversion\_factor) &lt; min\_order\_qty ≤ required\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in min\_order\_qty → (quantity × conversion\_factor) &lt; min\_order\_qty ≤ required\_qty.
  - Compare adjacent operands in order, stopping at the first false comparison in (quantity × conversion\_factor) &lt; min\_order\_qty ≤ required\_qty.
  - Set grid from (Decimal(10) to the power negative precision).
  - Set exact from (Decimal(str(min\_order\_qty)) ÷ Decimal(str(conversion\_factor))).
  - Set quantity from flt(exact.quantize(grid, rounding = ROUND\_CEILING)).
- Return quantity.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1718) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L958)

<a id="op-55fb0ec8230885"></a>
### Apply minimum order qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_apply_minimum_order_qty`

**Inputs** mr\_items.

**Local steps**

- For each rows in \_purchase\_rows\_by\_item(mr\_items).values().
  - Set surplus\_qty from 0.0.
  - For each order\_rows in \_rows\_by\_sales\_order(rows).
    - Set surplus\_qty from \_apply\_minimum\_order\_qty\_to\_order(order\_rows, surplus\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1657) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L897)

<a id="op-5c0c96a0bc5f6e"></a>
### Purchase rows by item

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_purchase_rows_by_item`

**Inputs** mr\_items.

**Explicit results** rows\_by\_item.

**Local steps**

- Set rows\_by\_item from defaultdict(list).
- For each row in mr\_items.
  - If row.get(“material\_request\_type”) does not belong to tuple(“Purchase”, “Subcontracting”).
    - Continue with the next iteration or loop test.
  - If flt(row.get(“quantity”)) ≤ 0.
    - Continue with the next iteration or loop test.
  - Set key from tuple(row.get(“item\_code”), row.get(“warehouse”), row.get(“material\_request\_type”), row.get(“supplier”)).
  - Evaluate rows\_by\_item at key.append(row).
- Return rows\_by\_item.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L957)

<a id="op-02d78b4aca6c6a"></a>
### Rows by sales order

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_rows_by_sales_order`

**Inputs** rows.

**Explicit results** list of rows\_by\_order at sales\_order for sales\_order drawn from sorted(rows\_by\_order).

**Local steps**

- Set rows\_by\_order from defaultdict(list).
- For each row in rows.
  - Evaluate rows\_by\_order at (row.get(“sales\_order”) or empty text).append(row).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“sales\_order”) → empty text.
- Return list of rows\_by\_order at sales\_order for sales\_order drawn from sorted(rows\_by\_order).
  - Draw sales\_order from sorted(rows\_by\_order).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L963)

<a id="op-0ae5afc15210cc"></a>
### Apply minimum order qty to order

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_apply_minimum_order_qty_to_order`

**Inputs** rows, surplus\_qty.

**Explicit results** ((surplus\_qty + purchased\_qty) − demand\_qty).

**Local steps**

- Set demand\_qty from sum(generator of \_stock\_quantity(row) for row drawn from rows).
  - Draw row from rows.
- Evaluate \_cover\_from\_surplus(rows, surplus\_qty).
- Set min\_order\_qty from max(generator of flt(row.get(“min\_order\_qty”)) for row drawn from rows).
  - Draw row from rows.
- Set total\_qty from sum(generator of \_stock\_quantity(row) for row drawn from rows).
  - Draw row from rows.
- If 0 &lt; total\_qty &lt; min\_order\_qty.
  - Compare adjacent operands in order, stopping at the first false comparison in 0 &lt; total\_qty &lt; min\_order\_qty.
  - Set row from next(generator of row for row drawn from rows where \_stock\_quantity(row) &gt; 0).
    - Draw row from rows, keep a combination only if (\_stock\_quantity(row) &gt; 0).
  - Evaluate \_set\_stock\_quantity(row, ((\_stock\_quantity(row) + min\_order\_qty) − total\_qty)).
- Set purchased\_qty from sum(generator of \_stock\_quantity(row) for row drawn from rows).
  - Draw row from rows.
- Return ((surplus\_qty + purchased\_qty) − demand\_qty).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1658) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L898)

<a id="op-18a95c6f27884a"></a>
### Cover from surplus

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_cover_from_surplus`

**Inputs** rows, surplus\_qty.

**Local steps**

- For each row in rows.
  - Set covered\_qty from min(surplus\_qty, \_stock\_quantity(row)).
  - <a id="op-18a95c6f27884a-guard-4"></a>If covered\_qty ≤ 0.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate \_set\_stock\_quantity(row, (\_stock\_quantity(row) − covered\_qty)).
  - Update surplus\_qty using − covered\_qty.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison covered\_qty ≤ 0, covered\_qty = 0 selects the branch that exits the enclosing loop. With covered\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-18a95c6f27884a-guard-4)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1662) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L902)
