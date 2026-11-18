# Inventory and warehouses · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Get item details

<a id="op-4f0fec7c41420c"></a>
### Get bin details

`operation_enterprise_binding_enterprise_stock_get_item_details_get_bin_details`

**Inputs** item\_code, warehouse, company = no value, include\_child\_warehouses = false.

**Explicit results** bin\_details.

**Local steps**

- Set bin\_details from mapping(“projected\_qty” → 0, “actual\_qty” → 0, “reserved\_qty” → 0).
- If warehouse.
  - Bind dependencies Coalesce, Sum.
  - Bind dependencies get\_child\_warehouses.
  - Set warehouses from get\_child\_warehouses(warehouse) when include\_child\_warehouses, otherwise list(warehouse).
    - Value choice on include\_child\_warehouses — true gives get\_child\_warehouses(warehouse), false gives list(warehouse).
  - Set bin from Platform.qb.DocType(“Bin”).
  - Set bin\_details from nested operand in the contract.select(nested operand in the contract(nested operand in the contract), nested operand in the contract(nested operand in the contract), nested operand in the contract(nested o … at 0.
- If company.
  - Set bin\_details at “company\_total\_stock” from get\_company\_total\_stock(item\_code, company).
- Return bin\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1423) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L920)

<a id="op-f8541dbaba12a3"></a>
### Get company total stock

`operation_enterprise_stock_get_item_details_business_behavior_get_company_total_stock`

**Inputs** item\_code, company.

**Explicit results** nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand i … at 0.

**Local steps**

- Set bin from Platform.qb.DocType(“Bin”).
- Set wh from Platform.qb.DocType(“Warehouse”).
- Return nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand i … at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0883.json#L2885) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1179) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L719)

<a id="op-5c9d298980261f"></a>
### Get batch qty

`operation_enterprise_stock_get_item_details_business_behavior_get_batch_quantity`

**Inputs** batch\_no, warehouse, item\_code.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“actual\_batch\_qty” → batch.get\_batch\_qty(batch\_no, warehouse)).

**Local steps**

- Bind dependencies batch.
- Evaluate Enterprise.require\_user\_permission(“Warehouse”, warehouse).
- If batch\_no.
  - Return mapping(“actual\_batch\_qty” → batch.get\_batch\_qty(batch\_no, warehouse)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1176) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L716)

<a id="op-c637d7bc8d6024"></a>
### Apply price list

`operation_enterprise_stock_get_item_details_business_behavior_apply_price_list`

**Inputs** ctx, as\_doc = false, doc = no value.

**Wrappers, in declaration order** Platform.whitelist(), Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Explicit results** \_apply\_price\_list(ctx, as\_doc, doc).

**Local steps**

- Evaluate validate\_pricing\_context(ctx).
- Return \_apply\_price\_list(ctx, as\_doc, doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1166) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L706)

<a id="op-df80b08c2a2928"></a>
### Apply price list

`operation_enterprise_binding_enterprise_stock_get_item_details_apply_price_list`

**Inputs** ctx, as\_doc = false, doc = no value.

**Wrappers, in declaration order** Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Explicit results** ctx · mapping(“parent” → parent, “children” → children).

**Local steps**

- Evaluate \_preprocess\_ctx(ctx).
- Set parent from get\_price\_list\_currency\_and\_exchange\_rate(ctx).
- Evaluate ctx.update(parent).
- Set children from list().
- If “items” belongs to ctx.
  - Set item\_list from ctx.get(“items”).
  - Evaluate ctx.update(parent).
  - For each item in item\_list.
    - Set ctx\_copy from ItemDetailsCtx(ctx.copy()).
    - Evaluate ctx\_copy.update(item).
    - Set ctx\_copy.transaction\_type from ctx.transaction\_type.
    - Set item\_details from apply\_price\_list\_on\_item(ctx\_copy, doc = doc).
    - Evaluate children.append(item\_details).
- If as\_doc.
  - Set ctx.price\_list\_currency from tuple(parent.price\_list\_currency).
  - Set ctx.plc\_conversion\_rate from parent.plc\_conversion\_rate.
  - If ctx.get(“items”).
    - For each tuple(i, item) in enumerate(ctx.get(“items”)).
      - For each fieldname in children at i.
        - If (fieldname belongs to item and fieldname does not belong to tuple(“name”, “doctype”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname belongs to item → fieldname does not belong to tuple(“name”, “doctype”).
          - Set item at fieldname from children at i at fieldname.
  - Return ctx.
- Otherwise.
  - Return mapping(“parent” → parent, “children” → children).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1418) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L915)

<a id="op-c20d7f191f41ed"></a>
### Apply price list on item

`operation_enterprise_stock_get_item_details_business_behavior_apply_price_list_on_item`

**Inputs** ctx, doc = no value.

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit results** item\_details.

**Local steps**

- Set item\_doc from Platform.get\_cached\_doc(“Item”, ctx.item\_code).
- Set source\_row from get\_rate\_locked\_source\_row(ctx, doc).
- If source\_row.
  - Set item\_details from Platform.\_dict().
  - Evaluate lock\_source\_rate(item\_details, source\_row).
- Otherwise.
  - Set item\_details from get\_price\_list\_rate(ctx, item\_doc).
- Set ctx.conversion\_factor from (flt(ctx.conversion\_factor) or get\_conversion\_factor(ctx.item\_code, ctx.uom).get(“conversion\_factor”, 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(ctx.conversion\_factor) → get\_conversion\_factor(ctx.item\_code, ctx.uom).get(“conversion\_factor”, 1).
- Set ctx.stock\_qty from (flt(ctx.qty) × flt(ctx.conversion\_factor)).
- If not source\_row.
  - Evaluate item\_details.update(get\_pricing\_rule\_for\_item(ctx, doc = doc)).
- Return item\_details.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, ctx.item\_code).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0883.json#L4082) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1167) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L707)

<a id="op-c63badd5baddc9"></a>
### Get price list currency and exchange rate

`operation_enterprise_stock_get_item_details_business_behavior_get_price_list_currency_and_exchange_rate`

**Inputs** ctx.

**Explicit results** mapping() · Platform.\_dict(mapping(“price\_list\_currency” → price\_list\_currency, “price\_list\_uom\_dependant” → price\_list\_uom\_dependant, “plc\_conversion\_rate” → (plc\_conversion\_rate or 1))).

**Local steps**

- If not ctx.price\_list.
  - Return mapping().
- If ctx.doctype belongs to sales\_doctypes.
  - Evaluate ctx.update(mapping(“exchange\_rate” → “for\_selling”)).
- Otherwise.
  - If ctx.doctype belongs to purchase\_doctypes.
    - Evaluate ctx.update(mapping(“exchange\_rate” → “for\_buying”)).
- Set price\_list\_details from get\_price\_list\_details(ctx.price\_list).
- Set price\_list\_currency from price\_list\_details.get(“currency”).
- Set price\_list\_uom\_dependant from price\_list\_details.get(“price\_not\_uom\_dependent”).
- Set plc\_conversion\_rate from ctx.plc\_conversion\_rate.
- Set company\_currency from get\_company\_currency(ctx.company).
- If (not plc\_conversion\_rate or (price\_list\_currency and ctx.price\_list\_currency and price\_list\_currency differs from ctx.price\_list\_currency)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not plc\_conversion\_rate → (price\_list\_currency and ctx.price\_list\_currency and price\_list\_currency differs from ctx.price\_list\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in price\_list\_currency → ctx.price\_list\_currency → price\_list\_currency differs from ctx.price\_list\_currency.
  - Set plc\_conversion\_rate from (get\_exchange\_rate(price\_list\_currency, company\_currency, ctx.transaction\_date, ctx.exchange\_rate) or plc\_conversion\_rate).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_exchange\_rate(price\_list\_currency, company\_currency, ctx.transaction\_date, ctx.exchange\_rate) → plc\_conversion\_rate.
- Return Platform.\_dict(mapping(“price\_list\_currency” → price\_list\_currency, “price\_list\_uom\_dependant” → price\_list\_uom\_dependant, “plc\_conversion\_rate” → (plc\_conversion\_rate or 1))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in plc\_conversion\_rate → 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1204) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L744)

<a id="op-f26774fe009943"></a>
### Get default bom

`operation_enterprise_stock_get_item_details_business_behavior_get_default_bill_of_materials`

**Inputs** item\_code = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_value.

**Explicit results** no value · bom\_name.

**Local steps**

- Bind local operation \_get\_bom for subsequent calls.
- If not item\_code.
  - Return no value.
- Set bom\_name from \_get\_bom(item\_code).
- Set template\_item from Platform.db.get\_value(“Item”, item\_code, “variant\_of”).
- If (not bom\_name and template\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not bom\_name → template\_item.
  - Set bom\_name from \_get\_bom(template\_item).
- Return bom\_name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L721)

<a id="op-2742617140f698"></a>
### Get default bom.get bom

`operation_enterprise_stock_get_item_details_business_behavior_get_default_bill_of_materials_get_bill_of_materials`

**Inputs** item.

**Record and data access** read “BOM” via get\_all.

**Explicit results** bom at 0.name when bom, otherwise no value.

**Local steps**

- Set bom from Platform.get\_all(“BOM”, dict(item = item, is\_active = true, is\_default = true, docstatus = 1), limit = 1).
- Return bom at 0.name when bom, otherwise no value.
  - Value choice on bom — true gives bom at 0.name, false gives no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0883.json#L5476) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L722)

<a id="op-6cc288e64fea9c"></a>
### Get valuation rate

`operation_enterprise_stock_get_item_details_business_behavior_get_valuation_rate`

**Inputs** item\_code, company, warehouse = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** \_get\_valuation\_rate(item\_code, company, warehouse).

**Local steps**

- Evaluate Platform.has\_permission(“Item”, doc = item\_code, throw = true).
- Evaluate Platform.has\_permission(“Company”, doc = company, ptype = “select”, throw = true).
- If Platform.get\_cached\_value(“Item”, item\_code, “is\_stock\_item”).
  - Set warehouse from (warehouse or get\_default\_warehouse(item\_code, company)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in warehouse → get\_default\_warehouse(item\_code, company).
  - If warehouse.
    - Evaluate Enterprise.require\_user\_permission(“Warehouse”, warehouse).
- Return \_get\_valuation\_rate(item\_code, company, warehouse).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, doc = item\_code, throw = true), Platform.has\_permission(“Company”, doc = company, ptype = “select”, throw = true) · configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L753)

<a id="op-748cb2e3ae3f2d"></a>
### Get default warehouse

`operation_enterprise_binding_enterprise_stock_get_item_details_get_default_warehouse`

**Inputs** item\_code, company.

**Declared result** (str bitwise or no value).

**Explicit results** (get\_item\_defaults(item\_code, company).get(“default\_warehouse”) or get\_item\_group\_defaults(item\_code, company).get(“default\_warehouse”) or get\_brand\_defaults(item\_code, company).get(“default\_warehouse”)).

**Local steps**

- Return (get\_item\_defaults(item\_code, company).get(“default\_warehouse”) or get\_item\_group\_defaults(item\_code, company).get(“default\_warehouse”) or get\_brand\_defaults(item\_code, company).get(“default\_warehouse”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_item\_defaults(item\_code, company).get(“default\_warehouse”) → get\_item\_group\_defaults(item\_code, company).get(“default\_warehouse”) → get\_brand\_defaults(item\_code, company).get(“default\_warehouse”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1425) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L922)

<a id="op-abd4381bff4b53"></a>
### Get valuation rate

`operation_enterprise_binding_enterprise_stock_get_item_details_get_valuation_rate`

**Inputs** item\_code, company, warehouse = no value.

**Record and data access** read “Warehouse” via get\_cached\_value · read “Bin” via get\_value.

**Explicit results** mapping(“valuation\_rate” → 0.0) · (Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse), list(“valuation\_rate”), as\_dict = true) or mapping(“valuation\_rate” → (item.get(“valuation\_rate”) or 0))) · mapping(“valuation\_rate” → (valuation\_rate at 0 at 0 or 0.0)).

**Local steps**

- If Platform.get\_cached\_value(“Warehouse”, warehouse, “is\_group”).
  - Return mapping(“valuation\_rate” → 0.0).
- Set item from get\_item\_defaults(item\_code, company).
- If item.get(“is\_stock\_item”).
  - Set warehouse from (warehouse or get\_accessible\_warehouse(get\_default\_warehouse(item\_code, company))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in warehouse → get\_accessible\_warehouse(get\_default\_warehouse(item\_code, company)).
  - Return (Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse), list(“valuation\_rate”), as\_dict = true) or mapping(“valuation\_rate” → (item.get(“valuation\_rate”) or 0))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse), list(“valuation\_rate”), as\_dict = true) → mapping(“valuation\_rate” → (item.get(“valuation\_rate”) or 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“valuation\_rate”) → 0.
- Otherwise.
  - If not item.get(“is\_stock\_item”).
    - Set pi\_item from Platform.qb.DocType(“Purchase Invoice Item”).
    - Set valuation\_rate from nested operand in the contract(nested operand in the contract).select((nested operand in the contract(nested operand in the contract) ÷ nested operand in the contract(nested operand in the contract))).wher ….run().
    - If valuation\_rate.
      - Return mapping(“valuation\_rate” → (valuation\_rate at 0 at 0 or 0.0)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in valuation\_rate at 0 at 0 → 0.0.
  - Otherwise.
    - Return mapping(“valuation\_rate” → 0.0).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, warehouse, “is\_group”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1438) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L935)

<a id="op-fc8791c9ef7df4"></a>
### Get gross profit

`operation_enterprise_stock_get_item_details_business_behavior_get_gross_profit`

**Inputs** out.

**Explicit results** out.

**Local steps**

- If out.valuation\_rate.
  - Evaluate out.update(mapping(“gross\_profit” → ((out.base\_rate − out.valuation\_rate) × out.stock\_qty))).
- Return out.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1191) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L731)

<a id="op-d0881f3aefa698"></a>
### Get serial no

`operation_enterprise_stock_get_item_details_business_behavior_get_serial_number`

**Inputs** \_args, serial\_nos = no value, sales\_order = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** serial\_nos.

**Local steps**

- Set serial\_nos from (serial\_nos or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in serial\_nos → list().
- Return serial\_nos.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L750)

<a id="op-0d139d9ef45f06"></a>
### Update party blanket order

`operation_enterprise_stock_get_item_details_business_behavior_update_party_blanket_order`

**Inputs** ctx, out.

**Local steps**

- If out at “against\_blanket\_order”.
  - Set blanket\_order\_details from \_get\_blanket\_order\_details(ctx).
  - If blanket\_order\_details.
    - Evaluate out.update(blanket\_order\_details).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1223) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L763)

<a id="op-070542448ee82c"></a>
### Get blanket order details

`operation_enterprise_stock_get_item_details_business_behavior_get_blanket_order_details`

**Inputs** ctx.

**Wrappers, in declaration order** Platform.whitelist(), Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Explicit results** \_get\_blanket\_order\_details(ctx).

**Local steps**

- Evaluate validate\_pricing\_context(ctx).
- Return \_get\_blanket\_order\_details(ctx).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1178) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L718)

<a id="op-7e4b4f35bd5be3"></a>
### Get blanket order details

`operation_enterprise_binding_enterprise_stock_get_item_details_get_blanket_order_details`

**Inputs** ctx.

**Wrappers, in declaration order** Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Record and data access** read “Selling Settings” when ctx.doctype belongs to tuple(“Sales Order”, “Quotation”), otherwise “Buying Settings” via get\_single\_value.

**Explicit results** blanket\_order\_details.

**Local steps**

- Set blanket\_order\_details from no value.
- If ctx.item\_code.
  - Set bo from Platform.qb.DocType(“Blanket Order”).
  - Set bo\_item from Platform.qb.DocType(“Blanket Order Item”).
  - Set allowance from flt(Platform.db.get\_single\_value(“Selling Settings” when ctx.doctype belongs to tuple(“Sales Order”, “Quotation”), otherwise “Buying Settings”, “blanket\_order\_allowance”)).
    - Value choice on ctx.doctype belongs to tuple(“Sales Order”, “Quotation”) — true gives “Selling Settings”, false gives “Buying Settings”.
  - Set query from nested operand in the contract(nested operand in the contract).orderby(bo.to\_date).orderby(bo.name).limit(1).
  - If (ctx.customer and ctx.doctype equals “Sales Order”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.customer → ctx.doctype equals “Sales Order”.
    - Set query from query.where(bo.customer equals ctx.customer).
  - Otherwise.
    - If (ctx.supplier and ctx.doctype equals “Purchase Order”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.supplier → ctx.doctype equals “Purchase Order”.
      - Set query from query.where(bo.supplier equals ctx.supplier).
  - If ctx.blanket\_order.
    - Set query from query.where(bo.name equals ctx.blanket\_order).
  - If ctx.currency.
    - Set query from query.where(bo.currency equals ctx.currency).
  - If ctx.transaction\_date.
    - Set query from query.where((bo.from\_date ≤ ctx.transaction\_date bitwise and bo.to\_date ≥ ctx.transaction\_date)).
  - Set blanket\_order\_details from query.run(as\_dict = true).
  - Set blanket\_order\_details from blanket\_order\_details at 0 when blanket\_order\_details, otherwise empty text.
    - Value choice on blanket\_order\_details — true gives blanket\_order\_details at 0, false gives empty text.
- Return blanket\_order\_details.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Selling Settings” when ctx.doctype belongs to tuple(“Sales Order”, “Quotation”), otherwise “Buying Settings”, “blanket\_order\_allowance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1424) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L921)

## Report · Incorrect balance qty after transaction

<a id="op-347b80a7c199ae"></a>
### Execute

`operation_enterprise_stock_report_incorrect_balance_quantity_after_transaction_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set tuple(columns, data) from tuple(list(), list()).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0891.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L141)

<a id="op-cf092fbda76308"></a>
### Get data

`operation_enterprise_stock_report_incorrect_balance_quantity_after_transaction_business_behavior_get_data`

**Inputs** filters.

**Explicit results** res.

**Local steps**

- Set data from get\_stock\_ledger\_entries(filters).
- Set itewise\_balance\_qty from mapping().
- For each row in data.
  - Set key from tuple(row.item\_code, row.warehouse).
  - Evaluate itewise\_balance\_qty.setdefault(key, list()).append(row).
- Set res from validate\_data(itewise\_balance\_qty).
- Return res.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0891.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L499) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L143)

<a id="op-c9357c09a2d3f2"></a>
### Validate data

`operation_enterprise_stock_report_incorrect_balance_quantity_after_transaction_business_behavior_validate_data`

**Inputs** itewise\_balance\_qty.

**Explicit results** res.

**Local steps**

- Set res from list().
- Set precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- Set reconciled\_qty from get\_reconciled\_qty(itewise\_balance\_qty).
- For each tuple(\_key, data) in itewise\_balance\_qty.items().
  - Set row from get\_incorrect\_data(data, precision, reconciled\_qty).
  - If row.
    - Evaluate res.append(row).
    - Evaluate res.append(mapping()).
- Return res.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L502) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L146)

<a id="op-ee628d15cee351"></a>
### Get reconciled qty

`operation_enterprise_binding_enterprise_stock_report_incorrect_balance_qty_after_transaction_incorrect_balance_qty_after_transaction_get_reconciled_qty`

**Inputs** itewise\_balance\_qty.

**Record and data access** read “Stock Reconciliation Item” via get\_all.

**Explicit results** mapping() · dict(Platform.get\_all(“Stock Reconciliation Item”, filters = mapping(“name” → tuple(“in”, names)), fields = list(“name”, “qty”), as\_list = true)).

**Local steps**

- Set names from list of row.voucher\_detail\_no for data drawn from itewise\_balance\_qty.values(), then row drawn from data where (row.voucher\_type equals “Stock Reconciliation” and row.voucher\_detail\_no).
  - Draw data from itewise\_balance\_qty.values().
  - Draw row from data, keep a combination only if ((row.voucher\_type equals “Stock Reconciliation” and row.voucher\_detail\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.voucher\_type equals “Stock Reconciliation” → row.voucher\_detail\_no.
- If not names.
  - Return mapping().
- Return dict(Platform.get\_all(“Stock Reconciliation Item”, filters = mapping(“name” → tuple(“in”, names)), fields = list(“name”, “qty”), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L182) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L957)

<a id="op-7179e59f6fc4ce"></a>
### Get incorrect data

`operation_enterprise_stock_report_incorrect_balance_quantity_after_transaction_business_behavior_get_incorrect_data`

**Inputs** data, precision, reconciled\_qty.

**Explicit results** row.

**Local steps**

- Set balance\_qty from 0.0.
- For each row in data.
  - Update balance\_qty using + row.actual\_qty.
  - If (row.voucher\_type equals “Stock Reconciliation” and not row.batch\_no and not row.is\_adjustment\_entry).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.voucher\_type equals “Stock Reconciliation” → not row.batch\_no → not row.is\_adjustment\_entry.
    - Set balance\_qty from flt(row.qty\_after\_transaction).
    - If (not row.actual\_qty and row.voucher\_detail\_no belongs to reconciled\_qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.actual\_qty → row.voucher\_detail\_no belongs to reconciled\_qty.
      - Set balance\_qty from flt(reconciled\_qty at row.voucher\_detail\_no).
  - Set row.expected\_balance\_qty from balance\_qty.
  - Set difference from abs(flt((flt(row.expected\_balance\_qty) − flt(row.qty\_after\_transaction)), precision)).
  - If difference.
    - Set row.differnce from difference.
    - Return row.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L500) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L144)

<a id="op-902f5c360e9017"></a>
### Get stock ledger entries

`operation_enterprise_stock_report_incorrect_balance_quantity_after_transaction_business_behavior_get_stock_ledger_entries`

**Inputs** report\_filters.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** Platform.get\_all(“Stock Ledger Entry”, fields = fields, filters = filters, order\_by = “posting\_date asc, posting\_time asc, creation asc”).

**Local steps**

- Set filters from mapping(“is\_cancelled” → 0).
- Set fields from list(“name”, “voucher\_type”, “voucher\_no”, “item\_code”, …).
- For each field in list(“warehouse”, “item\_code”, “company”).
  - If report\_filters.get(field).
    - Set filters at field from report\_filters.get(field).
- Return Platform.get\_all(“Stock Ledger Entry”, fields = fields, filters = filters, order\_by = “posting\_date asc, posting\_time asc, creation asc”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L145)

<a id="op-07a6bcbfef0038"></a>
### Get columns

`operation_enterprise_stock_report_incorrect_balance_quantity_after_transaction_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Id”, “fieldtype” → “Link”, “fieldname” → “name”, “options” → “Stock Ledger Entry”, …), mapping(“label” → translated “Posting Date”, “fieldtype” → “Date”, “fieldname” → “p ….

**Local steps**

- Return list(mapping(“label” → translated “Id”, “fieldtype” → “Link”, “fieldname” → “name”, “options” → “Stock Ledger Entry”, …), mapping(“label” → translated “Posting Date”, “fieldtype” → “Date”, “fieldname” → “p ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0891.json#L1151) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L142)
