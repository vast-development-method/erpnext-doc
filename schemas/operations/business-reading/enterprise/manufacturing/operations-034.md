# Production · operations 34

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Production plan

[Record definition](../../../../data/record-types/production_plan.json)

<a id="op-1fe1947812f323"></a>
### Stock quantity

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_stock_quantity`

**Inputs** row.

**Explicit results** (flt(row.get(“quantity”)) × (flt(row.get(“conversion\_factor”)) or 1)).

**Local steps**

- Return (flt(row.get(“quantity”)) × (flt(row.get(“conversion\_factor”)) or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.get(“conversion\_factor”)) → 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L969)

<a id="op-ee76faabf77d47"></a>
### Set stock quantity

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_set_stock_quantity`

**Inputs** row, stock\_qty.

**Record and data access** read “UOM” via get\_cached\_value.

**Local steps**

- Set conversion\_factor from (flt(row.get(“conversion\_factor”)) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.get(“conversion\_factor”)) → 1.
- Set quantity from \_quantity\_in\_purchase\_uom(stock\_qty, conversion\_factor, stock\_qty).
- If Platform.get\_cached\_value(“UOM”, row.get(“uom”), “must\_be\_whole\_number”).
  - Set quantity from ceil(quantity).
- Set row at “quantity” from quantity.
- Evaluate \_keep\_stock\_qty\_whole(row, stock\_qty).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, row.get(“uom”), “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L966)

<a id="op-2dc2a6be7ca634"></a>
### Keep stock qty whole

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_keep_stock_qty_whole`

**Inputs** row, stock\_qty.

**Record and data access** read “UOM” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- Set stock\_uom from row.get(“stock\_uom”).
- If not Platform.get\_cached\_value(“UOM”, stock\_uom, “must\_be\_whole\_number”).
  - Return no value.
- Set row\_stock\_qty from flt(\_stock\_quantity(row), Platform.get\_precision(“Material Request Item”, “stock\_qty”)).
- If row\_stock\_qty.is\_integer().
  - Return no value.
- Evaluate row.update(mapping(“uom” → stock\_uom, “conversion\_factor” → 1.0, “quantity” → round\_up\_whole\_uom(stock\_qty, stock\_uom))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, stock\_uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1702) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L942)

<a id="op-e7ab7ae4a5119e"></a>
### Get sales orders

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_sales_orders`

**Inputs** self.

**Record and data access** read “Item” via exists.

**Explicit results** open\_so.

**Local steps**

- Set bom from Platform.qb.DocType(“BOM”).
- Set pi from Platform.qb.DocType(“Packed Item”).
- Set so from Platform.qb.DocType(“Sales Order”).
- Set so\_item from Platform.qb.DocType(“Sales Order Item”).
- Set open\_so\_subquery1 from nested operand in the contract.qb.from\_(bom).select(bom.name).where(bom.is\_active equals 1).
- Set open\_so\_subquery2 from nested operand in the contract.qb.from\_(pi).select(pi.name).where(((pi.parent equals so.name bitwise and pi.parent\_item equals so\_item.item\_code) bitwise and ExistsCriterion(nested operand in the contract. ….
- Set open\_so\_query from nested operand in the contract(nested operand in the contract).select(so.name, so.transaction\_date, so.customer, so.base\_grand\_total).distinct().where(((((nested operand in the contract.parent equals neste ….
- Set date\_field\_mapper from mapping(“from\_date” → so.transaction\_date ≥ self.from\_date, “to\_date” → so.transaction\_date ≤ self.to\_date, “from\_delivery\_date” → so\_item.delivery\_date ≥ self.from\_delivery\_date, “to\_delivery\_date” → so\_i ….
- For each tuple(field, value) in date\_field\_mapper.items().
  - If self.get(field).
    - Set open\_so\_query from open\_so\_query.where(value).
- For each field in tuple(“customer”, “project”, “sales\_order\_status”).
  - If self.get(field).
    - Set so\_field from “status” when field equals “sales\_order\_status”, otherwise field.
      - Value choice on field equals “sales\_order\_status” — true gives “status”, false gives field.
    - Set open\_so\_query from open\_so\_query.where(so at so\_field equals self.get(field)).
- If (self.item\_code and Platform.db.exists(“Item”, self.item\_code)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.item\_code → Platform.db.exists(“Item”, self.item\_code).
  - Set open\_so\_query from open\_so\_query.where(so\_item.item\_code equals self.item\_code).
  - Set open\_so\_subquery1 from open\_so\_subquery1.where((self.get\_bom\_item\_condition() or bom.item equals so\_item.item\_code)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_bom\_item\_condition() → bom.item equals so\_item.item\_code.
- Set open\_so\_query from open\_so\_query.where((ExistsCriterion(open\_so\_subquery1) bitwise or ExistsCriterion(open\_so\_subquery2))).
- Set open\_so from open\_so\_query.run(as\_dict = true).
- Return open\_so.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L193) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L930)

<a id="op-7ea9e198a59915"></a>
### Required qty for mr

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_required_qty_for_mr`

**Inputs** row, ignore\_existing\_ordered\_qty, warehouse, bin\_dict, consumed\_qty, include\_safety\_stock.

**Explicit results** \_adjust\_required\_qty\_for\_uom(row, required\_qty).

**Local steps**

- Set safety\_stock from flt(row at “safety\_stock”) when include\_safety\_stock, otherwise 0.
  - Value choice on include\_safety\_stock — true gives flt(row at “safety\_stock”), false gives 0.
- Set qty from flt(row.get(“qty”)).
- Set projected\_qty from max(0, flt(bin\_dict.get(“projected\_qty”))) when ignore\_existing\_ordered\_qty, otherwise 0.
  - Value choice on ignore\_existing\_ordered\_qty — true gives max(0, flt(bin\_dict.get(“projected\_qty”))), false gives 0.
- Set key from tuple(row.get(“item\_code”), warehouse).
- Set available\_qty from (projected\_qty − consumed\_qty at key).
- Set required\_qty from max(0, (qty − (available\_qty − safety\_stock))).
- Update consumed\_qty at key using + (qty − required\_qty).
- Return \_adjust\_required\_qty\_for\_uom(row, required\_qty).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L959)

<a id="op-4de9510239ead6"></a>
### Adjust required qty for uom

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_adjust_required_qty_for_uom`

**Inputs** row, required\_qty.

**Explicit results** required\_qty.

**Explicit failure paths** validation helper — translated “UOM Conversion factor ({0} -&gt; {1}) not found for item: {2}”.format(row at “purchase\_uom”, row at “stock\_uom”, row.item\_code).

**Local steps**

- If not row at “purchase\_uom”.
  - Set row at “purchase\_uom” from row at “stock\_uom”.
- If row at “purchase\_uom” differs from row at “stock\_uom”.
  - If not (row at “conversion\_factor” or Platform.flags.show\_qty\_in\_stock\_uom).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row at “conversion\_factor” → Platform.flags.show\_qty\_in\_stock\_uom.
    - Call the validation error handler Platform.throw(translated “UOM Conversion factor ({0} -&gt; {1}) not found for item: {2}”.format(row at “purchase\_uom”, row at “stock\_uom”, row.item\_code)).
- Return required\_qty.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1655) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L895)

<a id="op-db4148b7d2e591"></a>
### Get bin details

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_bin_details`

**Inputs** row, company, for\_warehouse = no value, all\_warehouse = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_bin\_details(row, company, for\_warehouse, all\_warehouse, ignore\_permissions = false).

**Local steps**

- Evaluate Platform.has\_permission(“Production Plan”, “read”, throw = true).
- Return \_get\_bin\_details(row, company, for\_warehouse, all\_warehouse, ignore\_permissions = false).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Production Plan”, “read”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L904)

<a id="op-aae943a079b4b4"></a>
### Get bin details

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_bin_details_b10cfc9a458e`

**Inputs** row, company, for\_warehouse = no value, all\_warehouse = false, ignore\_permissions = true.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- If isinstance(row, str).
  - Set row from Platform.\_dict(json.loads(row)).
- Set bin from Platform.qb.DocType(“Bin”).
- Set wh from Platform.qb.DocType(“Warehouse”).
- Set subquery from Platform.qb.get\_query(“Warehouse”, fields = list(“name”), ignore\_permissions = ignore\_permissions).where(wh.company equals company).
- Set warehouse from empty text.
- If not all\_warehouse.
  - Set warehouse from (for\_warehouse or row.get(“source\_warehouse”) or row.get(“default\_warehouse”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in for\_warehouse → row.get(“source\_warehouse”) → row.get(“default\_warehouse”).
- If warehouse.
  - Set tuple(lft, rgt) from Platform.db.get\_value(“Warehouse”, warehouse, list(“lft”, “rgt”)).
  - Set subquery from subquery.where(((wh.lft ≥ lft bitwise and wh.rgt ≤ rgt) bitwise and wh.name equals bin.warehouse)).
- Set query from nested operand in the contract(nested operand in the contract).select(bin.warehouse, nested operand in the contract.as\_(“projected\_qty”), nested operand in the contract.as\_(“actual\_qty”), nested operand in ….
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L905)

<a id="op-77e8e29b577291"></a>
### Get pooled bin details

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_pooled_bin_details`

**Inputs** row, company, for\_warehouse.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_aggregate\_bin\_details(\_get\_bin\_details(row, company, for\_warehouse, ignore\_permissions = false)).

**Local steps**

- Evaluate Platform.has\_permission(“Production Plan”, “read”, throw = true).
- Return \_aggregate\_bin\_details(\_get\_bin\_details(row, company, for\_warehouse, ignore\_permissions = false)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Production Plan”, “read”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L185) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L922)

<a id="op-4607922bcf7d80"></a>
### Get so details

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_so_details`

**Inputs** sales\_order.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Sales Order” via get\_value.

**Explicit results** Platform.db.get\_value(“Sales Order”, mapping(“name” → sales\_order, “docstatus” → 1), list(“transaction\_date”, “customer”, “grand\_total”), as\_dict = 1).

**Local steps**

- Evaluate Platform.has\_permission(“Production Plan”, throw = true).
- Evaluate Enterprise.require\_user\_permission(“Sales Order”, sales\_order).
- Return Platform.db.get\_value(“Sales Order”, mapping(“name” → sales\_order, “docstatus” → 1), list(“transaction\_date”, “customer”, “grand\_total”), as\_dict = 1).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Production Plan”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L194) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L931)

<a id="op-dab91b5ad3ba5d"></a>
### Get warehouse list

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_warehouse_list`

**Inputs** warehouses.

**Explicit results** warehouse\_list.

**Local steps**

- Set warehouse\_list from list().
- If isinstance(warehouses, str).
  - Set warehouses from json.loads(warehouses).
- For each row in warehouses.
  - Set child\_warehouses from Platform.db.get\_descendants(“Warehouse”, row.get(“warehouse”)).
  - If child\_warehouses.
    - Evaluate warehouse\_list.extend(child\_warehouses).
  - Otherwise.
    - Evaluate warehouse\_list.append(row.get(“warehouse”)).
- Return warehouse\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1697) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L937)

<a id="op-acdaf68ce69ae9"></a>
### Authorize mr request

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_authorize_mr_request`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, warehouses.

**Observed service boundaries** effective access lookup, record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1659) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L899)

<a id="op-7ab46b59bfa218"></a>
### Iter mr rows

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_iter_mr_rows`

**Inputs** doc.

**Local steps**

- For each key in tuple(“po\_items”, “items”, “sub\_assembly\_items”).
  - For each row in (doc.get(key) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(key) → list().
    - If isinstance(row, dict).
      - yield row.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1701) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L941)

<a id="op-ebd67410535679"></a>
### Get items for material requests

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_items_for_material_requests`

**Inputs** doc, warehouses = no value, get\_parent\_warehouse\_data = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Item” via get\_doc.

**State and service calls** msgprint with message.

**Explicit results** mr\_items.

**Explicit failure paths** validation helper — translated “Items to Manufacture are required to pull the Raw Materials associated with it.” · validation helper — translated “For row {0}: Enter Planned Qty”.format(data.get(“idx”)).

**Local steps**

- Evaluate Platform.has\_permission(“Production Plan”, “read”, throw = true).
- Set doc from Platform.\_dict(json.loads(doc) when isinstance(doc, str), otherwise doc).
  - Value choice on isinstance(doc, str) — true gives json.loads(doc), false gives doc.
- Evaluate \_authorize\_mr\_request(doc, warehouses).
- Evaluate \_validate\_group\_warehouse\_target(doc).
- If warehouses.
  - Set warehouses from list(set(get\_warehouse\_list(warehouses))).
  - If doc.get(“for\_warehouse”) belongs to warehouses.
    - Evaluate warehouses.remove(doc.get(“for\_warehouse”)).
- Set doc at “mr\_items” from list().
- Set po\_items from doc.get(“po\_items”) when doc.get(“po\_items”), otherwise doc.get(“items”).
  - Value choice on doc.get(“po\_items”) — true gives doc.get(“po\_items”), false gives doc.get(“items”).
- If doc.get(“sub\_assembly\_items”).
  - For each sa\_row in doc.sub\_assembly\_items.
    - Set sa\_row from Platform.\_dict(sa\_row).
    - If sa\_row.type\_of\_manufacturing equals “Material Request”.
      - Evaluate po\_items.append(Platform.\_dict(mapping(“item\_code” → sa\_row.production\_item, “required\_qty” → sa\_row.qty, “include\_exploded\_items” → 0))).
- If (not po\_items or not list of row.get(“item\_code”) for row drawn from po\_items where row.get(“item\_code”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not po\_items → not list of row.get(“item\_code”) for row drawn from po\_items where row.get(“item\_code”).
  - Draw row from po\_items, keep a combination only if (row.get(“item\_code”)).
  - Call the validation error handler Platform.throw(translated “Items to Manufacture are required to pull the Raw Materials associated with it.”, title = translated “Items Required”).
- Set company from doc.get(“company”).
- Set ignore\_existing\_ordered\_qty from doc.get(“ignore\_existing\_ordered\_qty”).
- Set include\_safety\_stock from doc.get(“include\_safety\_stock”).
- Set so\_item\_details from Platform.\_dict().
- Set existing\_sub\_assembly\_items from set().
- Set sub\_assembly\_items from defaultdict(int).
- If (doc.get(“skip\_available\_sub\_assembly\_item”) and doc.get(“sub\_assembly\_items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“skip\_available\_sub\_assembly\_item”) → doc.get(“sub\_assembly\_items”).
  - For each d in doc.get(“sub\_assembly\_items”).
    - If d.get(“type\_of\_manufacturing”) equals “Material Request”.
      - Continue with the next iteration or loop test.
    - Update sub\_assembly\_items at tuple(d.get(“production\_item”), d.get(“bom\_no”), d.get(“type\_of\_manufacturing”)) using + get\_qty\_before\_process\_loss(d.get(“qty”), d.get(“process\_loss\_percentage”), d.get(“stock\_uom”)).
  - Set sub\_assembly\_items from mapping of k at slice no value to 2 → v for tuple(k, v) drawn from sub\_assembly\_items.items().
    - Draw tuple(k, v) from sub\_assembly\_items.items().
- Set requested\_sub\_assemblies from get\_requested\_sub\_assemblies(doc).
- Set all\_requested from set().union(expanded requested\_sub\_assemblies.values()).
- For each data in po\_items.
  - If (not data.get(“include\_exploded\_items”) and doc.get(“sub\_assembly\_items”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not data.get(“include\_exploded\_items”) → doc.get(“sub\_assembly\_items”).
    - Set data at “include\_exploded\_items” from 1.
  - Set data at “requested\_sub\_assemblies” from all\_requested when doc.get(“combine\_sub\_items”), otherwise requested\_sub\_assemblies.get(data.get(“name”), set()).
    - Value choice on doc.get(“combine\_sub\_items”) — true gives all\_requested, false gives requested\_sub\_assemblies.get(data.get(“name”), set()).
  - Set planned\_qty from (data.get(“required\_qty”) or data.get(“planned\_qty”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.get(“required\_qty”) → data.get(“planned\_qty”).
  - If (data.get(“bom\_no”) and not data.get(“required\_qty”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.get(“bom\_no”) → not data.get(“required\_qty”).
    - Set loss\_percentage from get\_plan\_process\_loss\_percentage(doc, data.get(“bom\_no”)).
    - Set planned\_qty from get\_qty\_before\_process\_loss(planned\_qty, loss\_percentage, data.get(“stock\_uom”)).
  - Set ignore\_existing\_ordered\_qty from (data.get(“ignore\_existing\_ordered\_qty”) or ignore\_existing\_ordered\_qty).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.get(“ignore\_existing\_ordered\_qty”) → ignore\_existing\_ordered\_qty.
  - Set item\_details from mapping().
  - If (data.get(“bom”) or data.get(“bom\_no”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.get(“bom”) → data.get(“bom\_no”).
    - If data.get(“required\_qty”).
      - Set bom\_no from data.get(“bom”).
      - Set include\_non\_stock\_items from 1.
      - Set include\_subcontracted\_items from 1 when data.get(“include\_exploded\_items”), otherwise 0.
        - Value choice on data.get(“include\_exploded\_items”) — true gives 1, false gives 0.
    - Otherwise.
      - Set bom\_no from data.get(“bom\_no”).
      - Set include\_subcontracted\_items from doc.get(“include\_subcontracted\_items”).
      - Set include\_non\_stock\_items from doc.get(“include\_non\_stock\_items”).
    - If not planned\_qty.
      - Call the validation error handler Platform.throw(translated “For row {0}: Enter Planned Qty”.format(data.get(“idx”))).
    - If bom\_no.
      - If (data.get(“include\_exploded\_items”) and doc.get(“skip\_available\_sub\_assembly\_item”) and doc.get(“sub\_assembly\_items”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.get(“include\_exploded\_items”) → doc.get(“skip\_available\_sub\_assembly\_item”) → doc.get(“sub\_assembly\_items”).
        - Set item\_details from get\_raw\_materials\_of\_sub\_assembly\_items(existing\_sub\_assembly\_items, item\_details, company, bom\_no, planned\_qty = planned\_qty, …).
      - Otherwise.
        - If (data.get(“include\_exploded\_items”) and include\_subcontracted\_items and not data.get(“requested\_sub\_assemblies”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.get(“include\_exploded\_items”) → include\_subcontracted\_items → not data.get(“requested\_sub\_assemblies”).
          - Set item\_details from get\_exploded\_items(item\_details, company, bom\_no, include\_non\_stock\_items, planned\_qty = planned\_qty, doc = doc).
        - Otherwise.
          - Set item\_details from get\_subitems(doc, data, item\_details, bom\_no, planned\_qty = planned\_qty, …).
  - Otherwise.
    - If data.get(“item\_code”).
      - Set item\_master from Platform.get\_doc(“Item”, data at “item\_code”).as\_dict().
      - Set purchase\_uom from (item\_master.purchase\_uom or item\_master.stock\_uom).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_master.purchase\_uom → item\_master.stock\_uom.
      - Set conversion\_factor from get\_uom\_conversion\_factor(item\_master.name, purchase\_uom) when item\_master.purchase\_uom, otherwise 1.0.
        - Value choice on item\_master.purchase\_uom — true gives get\_uom\_conversion\_factor(item\_master.name, purchase\_uom), false gives 1.0.
      - Set item\_details at item\_master.item\_code from Platform.\_dict(mapping(“item\_name” → item\_master.item\_name, “default\_bom” → doc.bom, “purchase\_uom” → purchase\_uom, “default\_warehouse” → item\_master.default\_warehouse, …)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in planned\_qty → 1.
  - Set sales\_order from data.get(“sales\_order”).
  - Set qty\_precision from Platform.get\_precision(“Material Request Plan Item”, “quantity”).
  - For each tuple(key, details) in item\_details.items().
    - Set details.qty from flt(details.qty, qty\_precision).
    - Evaluate so\_item\_details.setdefault(sales\_order, Platform.\_dict()).
    - If key belongs to so\_item\_details.get(sales\_order, mapping()).
      - Set so\_item\_details at sales\_order at key at “qty” from (so\_item\_details at sales\_order at key.get(“qty”, 0) + flt(details.qty)).
    - Otherwise.
      - Set so\_item\_details at sales\_order at key from details.
- Set mr\_items from list().
- Set consumed\_qty from defaultdict(float).
- Set target\_warehouse from doc.get(“for\_warehouse”).
- Set scope\_warehouse from (doc.get(“raw\_material\_group\_warehouse”) or target\_warehouse).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“raw\_material\_group\_warehouse”) → target\_warehouse.
- Set is\_transfer from bool(((ignore\_existing\_ordered\_qty or get\_parent\_warehouse\_data) and warehouses)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (ignore\_existing\_ordered\_qty or get\_parent\_warehouse\_data) → warehouses.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ignore\_existing\_ordered\_qty → get\_parent\_warehouse\_data.
- For each sales\_order in so\_item\_details.
  - Set item\_dict from so\_item\_details at sales\_order.
  - For each details in item\_dict.values().
    - Set fallback from (details.get(“source\_warehouse”) or details.get(“default\_warehouse”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in details.get(“source\_warehouse”) → details.get(“default\_warehouse”).
    - Set row\_scope\_warehouse from (scope\_warehouse or fallback).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in scope\_warehouse → fallback.
    - Set row\_target\_warehouse from (target\_warehouse or fallback).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in target\_warehouse → fallback.
    - Set bins from \_get\_bin\_details(details, doc.company, row\_scope\_warehouse).
    - Set bin\_dict from \_aggregate\_bin\_details(bins).
    - Set tuple(shortage\_warehouse, shortage\_bin) from tuple(row\_scope\_warehouse, bin\_dict).
    - If (is\_transfer and row\_scope\_warehouse differs from row\_target\_warehouse).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_transfer → row\_scope\_warehouse differs from row\_target\_warehouse.
      - Set shortage\_warehouse from row\_target\_warehouse.
      - Set shortage\_bin from \_aggregate\_bin\_details(generator of row for row drawn from bins where row.warehouse equals row\_target\_warehouse).
        - Draw row from bins, keep a combination only if (row.warehouse equals row\_target\_warehouse).
    - If details.qty &gt; 0.
      - Set items from get\_material\_request\_items(doc, details, sales\_order, company, …).
      - If items.
        - Evaluate mr\_items.append(items).
- If is\_transfer.
  - Set new\_mr\_items from list().
  - Set locations\_by\_item from \_get\_transfer\_locations(mr\_items, warehouses, company).
  - For each item in mr\_items.
    - Evaluate get\_materials\_from\_other\_locations(item, warehouses, new\_mr\_items, company, consider\_minimum\_order\_qty = doc.get(“consider\_minimum\_order\_qty”), locations = locations\_by\_item at item.get(“item\_code”)).
  - Set mr\_items from new\_mr\_items.
- If doc.get(“consider\_minimum\_order\_qty”).
  - Evaluate \_apply\_minimum\_order\_qty(mr\_items).
- If not mr\_items.
  - Set to\_enable from Platform.bold(Platform.get\_meta(“Production Plan”).get\_field(“ignore\_existing\_ordered\_qty”).label).
  - Set warehouse from Platform.bold(doc.get(“for\_warehouse”)).
  - Set message from (translated “As there are sufficient raw materials, Material Request is not required for Warehouse {0}.”.format(warehouse) + text in the contract).
  - Update message using + translated “If you still want to proceed, please enable {0}.”.format(to\_enable).
  - Evaluate Platform.msgprint(message, title = translated “Note”).
- Return mr\_items.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Production Plan”, “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1668) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L908)

<a id="op-e93e58867746cc"></a>
### Validate group warehouse target

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_validate_group_warehouse_target`

**Inputs** doc.

**Explicit failure paths** validation helper — translated “{0} is required to get raw materials when {1} is set.”.format(Platform.bold(translated “For Warehouse”), Platform.bold(translated “Raw Material Group Warehouse”)).

**Local steps**

- If (doc.get(“raw\_material\_group\_warehouse”) and not doc.get(“for\_warehouse”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“raw\_material\_group\_warehouse”) → not doc.get(“for\_warehouse”).
  - Call the validation error handler Platform.throw(translated “{0} is required to get raw materials when {1} is set.”.format(Platform.bold(translated “For Warehouse”), Platform.bold(translated “Raw Material Group Warehouse”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L971)

<a id="op-7c68740d8637e4"></a>
### Aggregate bin details

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_aggregate_bin_details`

**Inputs** bin\_list.

**Explicit results** aggregated.

**Local steps**

- Set qty\_fields from tuple(“projected\_qty”, “actual\_qty”, “ordered\_qty”, “reserved\_qty\_for\_production”, …).
- Set aggregated from mapping of field → 0 for field drawn from qty\_fields.
  - Draw field from qty\_fields.
- For each row in (bin\_list or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bin\_list → list().
  - For each field in qty\_fields.
    - Update aggregated at field using + flt(row.get(field)).
- Return aggregated.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1656) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L896)

<a id="op-149a2e77cf76d6"></a>
### Get materials from other locations

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_materials_from_other_locations`

**Inputs** item, warehouses, new\_mr\_items, company, consider\_minimum\_order\_qty = false, locations = no value.

**Local steps**

- If locations is identical to no value.
  - Set locations from \_get\_transfer\_locations(list(item), warehouses, company) at item.get(“item\_code”).
- Set required\_qty from item.get(“quantity”).
- If (item.get(“conversion\_factor”) and item.get(“purchase\_uom”) differs from item.get(“stock\_uom”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“conversion\_factor”) → item.get(“purchase\_uom”) differs from item.get(“stock\_uom”).
  - Set required\_qty from (required\_qty × item.get(“conversion\_factor”)).
- Set first\_row from len(new\_mr\_items).
- Set required\_qty from \_transfer\_from\_locations(item, locations, new\_mr\_items, required\_qty).
- Set precision from Platform.get\_precision(“Material Request Plan Item”, “quantity”).
- If flt(required\_qty, precision) &gt; 0.
  - Set min\_order\_qty from flt(item.get(“min\_order\_qty”)) when consider\_minimum\_order\_qty, otherwise 0.
    - Value choice on consider\_minimum\_order\_qty — true gives flt(item.get(“min\_order\_qty”)), false gives 0.
  - Set quantity from \_quantity\_in\_purchase\_uom(required\_qty, item.get(“conversion\_factor”), min\_order\_qty).
  - Set item at “quantity” from round\_up\_whole\_uom(quantity, item.get(“uom”)).
  - Evaluate \_keep\_stock\_qty\_whole(item, required\_qty).
  - Evaluate new\_mr\_items.append(item).
- Evaluate \_split\_required\_bom\_qty(item, new\_mr\_items at slice first\_row to no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1671) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L911)

<a id="op-203a4fe371fe7d"></a>
### Split required bom qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_split_required_bom_qty`

**Inputs** item, rows.

**Explicit results** no value.

**Local steps**

- If not rows.
  - Return no value.
- Set precision from Platform.get\_precision(“Material Request Plan Item”, “required\_bom\_qty”).
- Set remaining\_qty from flt(item.get(“required\_bom\_qty”)).
- For each row in rows at slice no value to negative 1.
  - Set row at “required\_bom\_qty” from flt(min(flt(row.get(“quantity”)), remaining\_qty), precision).
  - Update remaining\_qty using − row at “required\_bom\_qty”.
- Set rows at negative 1 at “required\_bom\_qty” from flt(remaining\_qty, precision).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L968)

<a id="op-6971a973392996"></a>
### Get transfer locations

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_transfer_locations`

**Inputs** mr\_items, warehouses, company.

**Explicit results** mapping of item\_code → get\_available\_item\_locations(item\_code, warehouses, required\_qty, company, ignore\_validation = true) when required\_qty &gt; 0, otherwise list() for tuple(item\_code, required\_qty) drawn  ….

**Local steps**

- Bind dependencies get\_available\_item\_locations.
- Set required\_qty\_by\_item from defaultdict(float).
- For each item in mr\_items.
  - Update required\_qty\_by\_item at item.get(“item\_code”) using + max(0, (flt(item.get(“quantity”)) × flt(item.get(“conversion\_factor”)))).
- Return mapping of item\_code → get\_available\_item\_locations(item\_code, warehouses, required\_qty, company, ignore\_validation = true) when required\_qty &gt; 0, otherwise list() for tuple(item\_code, required\_qty) drawn  ….
  - Draw tuple(item\_code, required\_qty) from required\_qty\_by\_item.items().
  - Value choice on required\_qty &gt; 0 — true gives get\_available\_item\_locations(item\_code, warehouses, required\_qty, company, ignore\_validation = true), false gives list().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1695) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L935)

<a id="op-f635fbf5b3e997"></a>
### Transfer from locations

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_transfer_from_locations`

**Inputs** item, locations, new\_mr\_items, required\_qty.

**Explicit results** required\_qty.

**Local steps**

- Set precision from Platform.get\_precision(“Material Request Plan Item”, “quantity”).
- Set transfers\_by\_warehouse from mapping().
- For each d in locations.
  - If flt(required\_qty, precision) ≤ 0.
    - Return required\_qty.
  - Set quantity from flt(min(required\_qty, d.get(“qty”)), precision).
  - <a id="op-f635fbf5b3e997-guard-9"></a>If quantity ≤ 0.
    - Continue with the next iteration or loop test.
  - Update d at “qty” using − quantity.
  - Update required\_qty using − quantity.
  - Set warehouse from d.get(“warehouse”).
  - If warehouse belongs to transfers\_by\_warehouse.
    - Set transfer from transfers\_by\_warehouse at warehouse.
    - Set transfer at “quantity” from flt((transfer at “quantity” + quantity), precision).
    - Continue with the next iteration or loop test.
  - Set new\_dict from copy.deepcopy(item).
  - Evaluate new\_dict.update(mapping(“quantity” → quantity, “material\_request\_type” → “Material Transfer”, “uom” → new\_dict.get(“stock\_uom”), “from\_warehouse” → warehouse, …)).
  - Set transfers\_by\_warehouse at warehouse from new\_dict.
  - Evaluate new\_mr\_items.append(new\_dict).
- Return required\_qty.

**Derived branch illustrations**

- At the comparison quantity ≤ 0, quantity = 0 selects the branch that continues with the next loop iteration. With quantity = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-f635fbf5b3e997-guard-9)

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1730) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L970)

<a id="op-4e7aba921a6261"></a>
### Get item data

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_item_data`

**Inputs** item\_code.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“bom\_no” → item\_details.get(“bom\_no”), “stock\_uom” → item\_details.get(“stock\_uom”), “description” → item\_details.get(“description”)).

**Local steps**

- Set item\_details from get\_item\_details(item\_code).
- Return mapping(“bom\_no” → item\_details.get(“bom\_no”), “stock\_uom” → item\_details.get(“stock\_uom”), “description” → item\_details.get(“description”)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L907)

<a id="op-b55b293af9de35"></a>
### Get sub assembly items

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_sub_assembly_items`

**Inputs** bin\_details, bom\_no, bom\_data, to\_produce\_qty, company, warehouse = no value, indent = 0, skip\_available\_sub\_assembly\_item = false, consider\_process\_loss = false.

**Record and data access** read “BOM” via get\_cached\_value.

**Local steps**

- Set data from get\_bom\_children(parent = bom\_no).
- Set precision from Platform.get\_precision(“Production Plan Sub Assembly Item”, “qty”).
- For each d in data.
  - If d.expandable.
    - Set parent\_item\_code from Platform.get\_cached\_value(“BOM”, bom\_no, “item”).
    - Set stock\_qty from ((d.stock\_qty ÷ d.parent\_bom\_qty) × flt(to\_produce\_qty)).
    - Set required\_qty from stock\_qty.
    - If (warehouse and d.item\_code does not belong to bin\_details).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in warehouse → d.item\_code does not belong to bin\_details.
      - Set bins from \_get\_bin\_details(d, company, for\_warehouse = warehouse).
      - Set bin\_details at d.item\_code from Platform.\_dict(\_aggregate\_bin\_details(bins)).
    - If skip\_available\_sub\_assembly\_item.
      - Set bin\_dict from bin\_details at d.item\_code.
      - Set available\_qty from bin\_dict.get(“available\_qty”, bin\_dict.projected\_qty).
      - If available\_qty ≥ stock\_qty.
        - Set bin\_dict.available\_qty from (available\_qty − stock\_qty).
        - Set stock\_qty from 0.
      - Otherwise.
        - If available\_qty &gt; 0.
          - Set bin\_dict.available\_qty from 0.
          - Update stock\_qty using − available\_qty.
    - If not d.is\_phantom\_item.
      - Set d.process\_loss\_percentage from get\_planned\_process\_loss\_percentage(d.value) when consider\_process\_loss, otherwise 0.
        - Value choice on consider\_process\_loss — true gives get\_planned\_process\_loss\_percentage(d.value), false gives 0.
      - Set stock\_qty from round\_up\_to\_whole\_unit(stock\_qty, d.stock\_uom).
      - Evaluate bom\_data.append(Platform.\_dict(mapping(“actual\_qty” → nested operand in the contract.get(nested operand in the contract.item\_code, mapping()).get(“actual\_qty”, 0), “parent\_item\_code” → parent\_item\_code, “d ….
      - Set stock\_qty from get\_qty\_before\_process\_loss(stock\_qty, d.process\_loss\_percentage, d.stock\_uom).
    - If d.value.
      - Evaluate get\_sub\_assembly\_items(bin\_details, d.value, bom\_data, stock\_qty, indent = (indent + 1), skip\_available\_sub\_assembly\_item = skip\_available\_sub\_assembly\_item, consider\_process\_loss = consider\_process\_loss, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“BOM”, bom\_no, “item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L195) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1692) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L932)

<a id="op-3c9f99c0ddea49"></a>
### Set default warehouses

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_set_default_warehouses`

**Inputs** row, default\_warehouses.

**Local steps**

- For each field in list(“wip\_warehouse”, “fg\_warehouse”, “scrap\_warehouse”).
  - If not row.get(field).
    - Set row at field from default\_warehouses.get(field).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L965)

<a id="op-c1a36b0d45bf91"></a>
### Get reserved qty for production plan

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_get_reserved_qty_for_production_plan`

**Inputs** item\_code, warehouse.

**Explicit results** no value · reserved\_qty.

**Local steps**

- Set plan\_reservations from \_get\_plan\_reservations(item\_code).
- If not plan\_reservations.
  - Return no value.
- Set work\_order\_reservations from \_get\_work\_order\_reservations(item\_code, list(plan\_reservations)).
- Set reserved\_qty from 0.0.
- For each tuple(plan, plan\_qty\_by\_warehouse) in plan\_reservations.items().
  - Update reserved\_qty using + \_get\_remaining\_reserved\_qty(plan\_qty\_by\_warehouse, work\_order\_reservations.get(plan, mapping()), warehouse).
- Return reserved\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L191) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1688) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L928)
