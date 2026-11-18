# Inventory and warehouses · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Get item details

<a id="op-cb0221e8ab681a"></a>
### Get default deferred account

`operation_enterprise_stock_get_item_details_business_behavior_get_default_deferred_account`

**Inputs** ctx, item, fieldname = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** (get\_item\_defaults(ctx.item\_code, ctx.company).get(fieldname) or get\_item\_group\_defaults(ctx.item\_code, ctx.company).get(fieldname) or get\_brand\_defaults(ctx.item\_code, ctx.company).get(fieldname) or ctx.g … · no value.

**Local steps**

- If (item.get(“enable\_deferred\_revenue”) or item.get(“enable\_deferred\_expense”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“enable\_deferred\_revenue”) → item.get(“enable\_deferred\_expense”).
  - Return (get\_item\_defaults(ctx.item\_code, ctx.company).get(fieldname) or get\_item\_group\_defaults(ctx.item\_code, ctx.company).get(fieldname) or get\_brand\_defaults(ctx.item\_code, ctx.company).get(fieldname) or ctx.g ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_item\_defaults(ctx.item\_code, ctx.company).get(fieldname) → get\_item\_group\_defaults(ctx.item\_code, ctx.company).get(fieldname) → get\_brand\_defaults(ctx.item\_code, ctx.company).get(fieldname) → ctx.get(fieldname) → Platform.get\_cached\_value(“Company”, ctx.company, (“default\_” + fieldname)).
- Otherwise.
  - Return no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, ctx.company, (“default\_” + fieldname)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1184) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L724)

<a id="op-f1f6a31fc64ea9"></a>
### Get default cost center

`operation_enterprise_stock_get_item_details_business_behavior_get_default_cost_center`

**Inputs** ctx, item = no value, item\_group = no value, brand = no value, company = no value.

**Wrappers, in declaration order** Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Record and data access** read “Project” via get\_value · read “Cost Center” via get\_cached\_value · read “Company” via get\_cached\_value.

**Explicit results** data.selling\_cost\_center · data.buying\_cost\_center · (data.selling\_cost\_center or data.buying\_cost\_center) · no value · cost\_center.

**Local steps**

- Set cost\_center from no value.
- If (not company and ctx.get(“company”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not company → ctx.get(“company”).
  - Set company from ctx.get(“company”).
- If ctx.get(“project”).
  - Set cost\_center from Platform.db.get\_value(“Project”, ctx.get(“project”), “cost\_center”, cache = true).
- If (not cost\_center and (item and item\_group and brand)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cost\_center → (item and item\_group and brand).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → item\_group → brand.
  - If ctx.get(“customer”).
    - Set cost\_center from (item.get(“selling\_cost\_center”) or item\_group.get(“selling\_cost\_center”) or brand.get(“selling\_cost\_center”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“selling\_cost\_center”) → item\_group.get(“selling\_cost\_center”) → brand.get(“selling\_cost\_center”).
  - Otherwise.
    - Set cost\_center from (item.get(“buying\_cost\_center”) or item\_group.get(“buying\_cost\_center”) or brand.get(“buying\_cost\_center”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“buying\_cost\_center”) → item\_group.get(“buying\_cost\_center”) → brand.get(“buying\_cost\_center”).
- Otherwise.
  - If (not cost\_center and ctx.get(“item\_code”) and company).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cost\_center → ctx.get(“item\_code”) → company.
    - For each method in list(“get\_item\_defaults”, “get\_item\_group\_defaults”, “get\_brand\_defaults”).
      - Set path from formatted text Enterprise.stock.get\_item\_details.{method}.
      - Set data from Platform.get\_attr(path)(ctx.get(“item\_code”), company).
      - If (data and (data.selling\_cost\_center or data.buying\_cost\_center)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → (data.selling\_cost\_center or data.buying\_cost\_center).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.selling\_cost\_center → data.buying\_cost\_center.
        - If (ctx.get(“customer”) and data.selling\_cost\_center).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.get(“customer”) → data.selling\_cost\_center.
          - Return data.selling\_cost\_center.
        - Otherwise.
          - If (ctx.get(“supplier”) and data.buying\_cost\_center).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.get(“supplier”) → data.buying\_cost\_center.
            - Return data.buying\_cost\_center.
        - Return (data.selling\_cost\_center or data.buying\_cost\_center).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.selling\_cost\_center → data.buying\_cost\_center.
- If (not cost\_center and ctx.get(“cost\_center”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cost\_center → ctx.get(“cost\_center”).
  - Set cost\_center from ctx.get(“cost\_center”).
- If (company and cost\_center and Platform.get\_cached\_value(“Cost Center”, cost\_center, “company”) differs from company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → cost\_center → Platform.get\_cached\_value(“Cost Center”, cost\_center, “company”) differs from company.
  - Return no value.
- If (not cost\_center and company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cost\_center → company.
  - Set cost\_center from Platform.get\_cached\_value(“Company”, company, “cost\_center”).
- Return cost\_center.

**Values supplied outside this operation** selected callable from Platform.get\_attr(path) · configured or stored value from Platform.get\_cached\_value(“Cost Center”, cost\_center, “company”), Platform.get\_cached\_value(“Company”, company, “cost\_center”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0881.json#L3717) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1183) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L723)

<a id="op-89e6bdabda989f"></a>
### Get default supplier

`operation_enterprise_stock_get_item_details_business_behavior_get_default_supplier`

**Inputs** \_ctx, item, item\_group, brand.

**Explicit results** (item.get(“default\_supplier”) or item\_group.get(“default\_supplier”) or brand.get(“default\_supplier”)).

**Local steps**

- Return (item.get(“default\_supplier”) or item\_group.get(“default\_supplier”) or brand.get(“default\_supplier”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“default\_supplier”) → item\_group.get(“default\_supplier”) → brand.get(“default\_supplier”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1189) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L729)

<a id="op-c53eefeb3dcd0c"></a>
### Get price list rate

`operation_enterprise_stock_get_item_details_business_behavior_get_price_list_rate`

**Inputs** ctx, item\_doc, out = no value.

**Record and data access** read “Price List” via get\_cached\_value · read “Stock Settings” via get\_cached\_value · read “Buying Settings” via get\_single\_value.

**Explicit results** out.

**Local steps**

- If out is identical to no value.
  - Set out from ItemDetails().
- Set meta from Platform.get\_meta((ctx.parenttype or ctx.doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.parenttype → ctx.doctype.
- If (meta.get\_field(“currency”) or ctx.get(“currency”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.get\_field(“currency”) → ctx.get(“currency”).
  - If (not ctx.price\_list\_currency or not ctx.plc\_conversion\_rate).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not ctx.price\_list\_currency → not ctx.plc\_conversion\_rate.
    - Set pl\_details from get\_price\_list\_currency\_and\_exchange\_rate(ctx).
    - Evaluate ctx.update(pl\_details).
  - If meta.get\_field(“currency”).
    - Evaluate validate\_conversion\_rate(ctx, meta).
  - If (ctx.get(“price\_list\_uom\_dependant”) is identical to no value and ctx.price\_list).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.get(“price\_list\_uom\_dependant”) is identical to no value → ctx.price\_list.
    - Set ctx.price\_list\_uom\_dependant from Platform.get\_cached\_value(“Price List”, ctx.price\_list, “price\_not\_uom\_dependent”).
  - Set price\_list\_rate from get\_price\_list\_rate\_for(ctx, item\_doc.name).
  - If (price\_list\_rate is identical to no value and item\_doc.variant\_of).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in price\_list\_rate is identical to no value → item\_doc.variant\_of.
    - Set price\_list\_rate from get\_price\_list\_rate\_for(ctx, item\_doc.variant\_of).
  - If (price\_list\_rate is identical to no value or Platform.get\_cached\_value(“Stock Settings”, “Stock Settings”, “update\_existing\_price\_list\_rate”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in price\_list\_rate is identical to no value → Platform.get\_cached\_value(“Stock Settings”, “Stock Settings”, “update\_existing\_price\_list\_rate”).
    - Evaluate insert\_item\_price(ctx).
  - If price\_list\_rate is identical to no value.
    - Return out.
  - Set out.price\_list\_rate from ((flt(price\_list\_rate) × flt(ctx.plc\_conversion\_rate)) ÷ flt(ctx.conversion\_rate)).
  - If Platform.db.get\_single\_value(“Buying Settings”, “disable\_last\_purchase\_rate”).
    - Return out.
  - If (not ctx.is\_internal\_supplier and not out.price\_list\_rate and ctx.transaction\_type equals “buying”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not ctx.is\_internal\_supplier → not out.price\_list\_rate → ctx.transaction\_type equals “buying”.
    - Bind dependencies get\_last\_purchase\_details.
    - Evaluate out.update(get\_last\_purchase\_details(item\_doc.name, ctx.name, ctx.conversion\_rate)).
- Return out.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Price List”, ctx.price\_list, “price\_not\_uom\_dependent”), Platform.get\_cached\_value(“Stock Settings”, “Stock Settings”, “update\_existing\_price\_list\_rate”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1205) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L745)

<a id="op-ace5c23935c889"></a>
### Get item prices to auto update

`operation_enterprise_binding_enterprise_stock_get_item_details_get_item_prices_to_auto_update`

**Inputs** ctx.

**Explicit results** nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(ip.valid\_from, order = nested operand in the contract.qb.desc).orderby(ip.creation, order = Pl ….

**Local steps**

- Set ip from Platform.qb.DocType(“Item Price”).
- Set query from nested operand in the contract.qb.from\_(ip).select(ip.name, ip.price\_list\_rate, ip.valid\_from, ip.valid\_upto).where((((ip.item\_code equals ctx.item\_code bitwise and ip.price\_list equals ctx.price\_list) bit ….
- For each fieldname in tuple(“customer”, “supplier”, “batch\_no”).
  - Set query from query.where(IfNull(ip at fieldname, empty text).isin(list(empty text, cstr(ctx.get(fieldname))))).
  - Set query from query.orderby(IfNull(ip at fieldname, empty text), order = Platform.qb.desc).
- Return nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(ip.valid\_from, order = nested operand in the contract.qb.desc).orderby(ip.creation, order = Pl ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L926)

<a id="op-faf7fe2221ad04"></a>
### Insert item price

`operation_enterprise_stock_get_item_details_business_behavior_insert_item_price`

**Inputs** ctx.

**Record and data access** resolve a document from “Stock Settings” via get\_cached\_doc · read “Price List” via get\_value · resolve a document from mapping(“doctype” → “Item Price”, “price\_list” → ctx.price\_list, “item\_code” → ctx.item\_code, “currency” → ctx.currency, …) via get\_doc.

**State and service calls** request set\_value on “Item Price” · msgprint with translated “Item Price updated for {0} in Price List {1}”.format(ctx.item\_code, ctx.price\_list) · request new\_doc for “Item Price” · call insert on item\_price · msgprint with translated “Item Price added for {0} in Price List - {1}”.format(get\_link\_to\_form(“Item”, ctx.item\_code), ctx.price\_list).

**Explicit results** no value.

**Local steps**

- If (not ctx.price\_list or not ctx.rate or ctx.is\_internal\_supplier or ctx.is\_internal\_customer).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not ctx.price\_list → not ctx.rate → ctx.is\_internal\_supplier → ctx.is\_internal\_customer.
  - Return no value.
- Set stock\_settings from Platform.get\_cached\_doc(“Stock Settings”).
- If (not Platform.db.get\_value(“Price List”, ctx.price\_list, “currency”, cache = true) equals ctx.currency or not stock\_settings.auto\_insert\_price\_list\_rate\_if\_missing or not Platform.has\_permission(“Item Pric ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.db.get\_value(“Price List”, ctx.price\_list, “currency”, cache = true) equals ctx.currency → not stock\_settings.auto\_insert\_price\_list\_rate\_if\_missing → not Platform.has\_permission(“Item Price”, “write”).
  - Return no value.
- Set transaction\_date from (getdate((ctx.get(“posting\_date”) or ctx.get(“transaction\_date”) or ctx.get(“posting\_datetime”))) or getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate((ctx.get(“posting\_date”) or ctx.get(“transaction\_date”) or ctx.get(“posting\_datetime”))) → getdate().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.get(“posting\_date”) → ctx.get(“transaction\_date”) → ctx.get(“posting\_datetime”).
- Set item\_prices from get\_item\_prices\_to\_auto\_update(ctx).
- Set item\_price from next(generator of row for row drawn from item\_prices where ((not row.valid\_from or getdate(nested operand in the contract.valid\_from) ≤ transaction\_date) and (not row.valid\_upto or getdate(nested operand i ….
  - Draw row from item\_prices, keep a combination only if (((not row.valid\_from or getdate(row.valid\_from) ≤ transaction\_date) and (not row.valid\_upto or getdate(row.valid\_upto) ≥ transaction\_date))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not row.valid\_from or getdate(row.valid\_from) ≤ transaction\_date) → (not row.valid\_upto or getdate(row.valid\_upto) ≥ transaction\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.valid\_from → getdate(row.valid\_from) ≤ transaction\_date.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.valid\_upto → getdate(row.valid\_upto) ≥ transaction\_date.
  - Value choice on item\_prices — true gives item\_prices at 0, false gives no value.
- Set update\_based\_on\_price\_list\_rate from stock\_settings.update\_price\_list\_based\_on equals “Price List Rate”.
- If (item\_price and item\_price.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_price → item\_price.name.
  - If not stock\_settings.update\_existing\_price\_list\_rate.
    - Return no value.
  - Set rate\_to\_consider from flt(ctx.price\_list\_rate) when update\_based\_on\_price\_list\_rate, otherwise flt(ctx.rate).
    - Value choice on update\_based\_on\_price\_list\_rate — true gives flt(ctx.price\_list\_rate), false gives flt(ctx.rate).
  - Set price\_list\_rate from \_get\_stock\_uom\_rate(rate\_to\_consider, ctx).
  - If (not price\_list\_rate or item\_price.price\_list\_rate equals price\_list\_rate).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not price\_list\_rate → item\_price.price\_list\_rate equals price\_list\_rate.
    - Return no value.
  - Set is\_price\_valid\_for\_transaction from ((not item\_price.valid\_from or getdate(item\_price.valid\_from) ≤ transaction\_date) and (not item\_price.valid\_upto or getdate(item\_price.valid\_upto) ≥ transaction\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not item\_price.valid\_from or getdate(item\_price.valid\_from) ≤ transaction\_date) → (not item\_price.valid\_upto or getdate(item\_price.valid\_upto) ≥ transaction\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_price.valid\_from → getdate(item\_price.valid\_from) ≤ transaction\_date.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_price.valid\_upto → getdate(item\_price.valid\_upto) ≥ transaction\_date.
  - If is\_price\_valid\_for\_transaction.
    - Evaluate Platform.db.set\_value(“Item Price”, item\_price.name, “price\_list\_rate”, price\_list\_rate).
    - Evaluate Platform.msgprint(translated “Item Price updated for {0} in Price List {1}”.format(ctx.item\_code, ctx.price\_list), alert = true).
  - Otherwise.
    - Set item\_price from Platform.new\_doc(“Item Price”, item\_code = ctx.item\_code, price\_list\_rate = price\_list\_rate, currency = ctx.currency, uom = ctx.stock\_uom, …).
    - Evaluate item\_price.insert().
    - Evaluate Platform.msgprint(translated “Item Price added for {0} in Price List - {1}”.format(get\_link\_to\_form(“Item”, ctx.item\_code), ctx.price\_list), alert = true).
- Otherwise.
  - Set rate\_to\_consider from (flt(ctx.price\_list\_rate) or flt(ctx.rate)) when update\_based\_on\_price\_list\_rate, otherwise flt(ctx.rate).
    - Value choice on update\_based\_on\_price\_list\_rate — true gives (flt(ctx.price\_list\_rate) or flt(ctx.rate)), false gives flt(ctx.rate).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(ctx.price\_list\_rate) → flt(ctx.rate).
  - Set price\_list\_rate from \_get\_stock\_uom\_rate(rate\_to\_consider, ctx).
  - Set item\_price from Platform.get\_doc(mapping(“doctype” → “Item Price”, “price\_list” → ctx.price\_list, “item\_code” → ctx.item\_code, “currency” → ctx.currency, …)).
  - Evaluate item\_price.insert().
  - Evaluate Platform.msgprint(translated “Item Price added for {0} in Price List - {1}”.format(get\_link\_to\_form(“Item”, ctx.item\_code), ctx.price\_list), alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Stock Settings”) · effective access from Platform.has\_permission(“Item Price”, “write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L755)

<a id="op-f02b1a0eb43fb5"></a>
### Get stock uom rate

`operation_enterprise_stock_get_item_details_business_behavior_get_stock_unit_of_measure_rate`

**Inputs** rate, ctx.

**Explicit results** (rate ÷ ctx.conversion\_factor) when ctx.conversion\_factor, otherwise rate.

**Local steps**

- Return (rate ÷ ctx.conversion\_factor) when ctx.conversion\_factor, otherwise rate.
  - Value choice on ctx.conversion\_factor — true gives (rate ÷ ctx.conversion\_factor), false gives rate.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L751)

<a id="op-7180ddcff7fa50"></a>
### Get item price

`operation_enterprise_stock_get_item_details_business_behavior_get_item_price`

**Inputs** pctx, item\_code, ignore\_party = false, force\_batch\_no = false, limit = 1.

**Declared result** list at dict.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set pctx from Platform.\_dict(pctx).
- Set tuple(query, ip) from \_get\_item\_price\_query(pctx, list(item\_code), ignore\_party, force\_batch\_no).
- Set query from query.select(ip.name, ip.price\_list\_rate, ip.uom, ip.packing\_unit).
- Set query from \_order\_item\_prices(query, ip, pctx).
- If limit.
  - Set query from query.limit(limit).
- Return query.run(as\_dict = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L734)

<a id="op-f202bbba94c461"></a>
### Get item prices for stock uom

`operation_enterprise_binding_enterprise_stock_get_item_details_get_item_prices_for_stock_uom`

**Inputs** pctx, item\_codes.

**Declared result** dict at tuple(str, ItemDetails).

**Explicit results** mapping() · mapping of price.item\_code → price for price drawn from prices.

**Local steps**

- If not item\_codes.
  - Return mapping().
- Set pctx from Platform.\_dict(pctx).
- Set tuple(query, ip) from \_get\_item\_price\_query(pctx, item\_codes, match\_uom = false).
- Set item from Platform.qb.DocType(“Item”).
- Set priority from \_order\_item\_prices(RowNumber().over(ip.item\_code), ip, pctx).
- Set ranked\_prices from nested operand in the contract(nested operand in the contract).select(ip.item\_code, ip.name, ip.price\_list\_rate, ip.packing\_unit, …).where((IfNull(nested operand in the contract.uom, empty text) equals emp ….
- Set prices from nested operand in the contract(nested operand in the contract).select(ranked\_prices.item\_code, ranked\_prices.name, ranked\_prices.price\_list\_rate, ranked\_prices.packing\_unit).where(ranked\_prices.priority eq ….
- Return mapping of price.item\_code → price for price drawn from prices.
  - Draw price from prices.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L925)

<a id="op-d7865987e12037"></a>
### Get item price query

`operation_enterprise_binding_enterprise_stock_get_item_details_get_item_price_query`

**Inputs** pctx, item\_codes, ignore\_party = false, force\_batch\_no = false, match\_uom = true.

**Explicit results** tuple(query, ip).

**Local steps**

- Set ip from Platform.qb.DocType(“Item Price”).
- Set query from Platform.qb.from\_(ip).where((ip.item\_code.isin(item\_codes) bitwise and ip.price\_list equals pctx.price\_list)).
- If match\_uom.
  - Set query from query.where(IfNull(ip.uom, empty text).isin(list(empty text, pctx.uom))).
- If force\_batch\_no.
  - Set query from query.where(ip.batch\_no equals pctx.batch\_no).
- Otherwise.
  - Set query from query.where(IfNull(ip.batch\_no, empty text).isin(list(empty text, pctx.batch\_no))).
- If not ignore\_party.
  - If pctx.customer.
    - Set query from query.where((ip.customer equals pctx.customer bitwise or (IfNull(ip.customer, empty text) equals empty text bitwise and IfNull(ip.supplier, empty text) equals empty text))).
  - Otherwise.
    - If pctx.supplier.
      - Set query from query.where((ip.supplier equals pctx.supplier bitwise or (IfNull(ip.customer, empty text) equals empty text bitwise and IfNull(ip.supplier, empty text) equals empty text))).
    - Otherwise.
      - Set query from query.where((IfNull(ip.customer, empty text) equals empty text bitwise and IfNull(ip.supplier, empty text) equals empty text)).
- If pctx.transaction\_date.
  - Set query from query.where((IfNull(ip.valid\_from, “2000-01-01”) ≤ pctx.transaction\_date bitwise and IfNull(ip.valid\_upto, “2500-12-31”) ≥ pctx.transaction\_date)).
- Return tuple(query, ip).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1427) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L924)

<a id="op-df8667a84c1f9c"></a>
### Order item prices

`operation_enterprise_binding_enterprise_stock_get_item_details_order_item_prices`

**Inputs** query, ip, pctx.

**Explicit results** query.orderby(IfNull(nested operand in the contract.batch\_no, empty text), order = Order.desc).orderby(ip.valid\_from, order = Order.desc).orderby(ip.uom, order = Order.desc).

**Local steps**

- If pctx.customer.
  - Set query from query.orderby(IfNull(ip.customer, empty text), order = Order.desc).
- Otherwise.
  - If pctx.supplier.
    - Set query from query.orderby(IfNull(ip.supplier, empty text), order = Order.desc).
- Return query.orderby(IfNull(nested operand in the contract.batch\_no, empty text), order = Order.desc).orderby(ip.valid\_from, order = Order.desc).orderby(ip.uom, order = Order.desc).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1441) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L938)

<a id="op-743a9d9716dbce"></a>
### Get batch based item price

`operation_enterprise_stock_get_item_details_business_behavior_get_batch_based_item_price`

**Inputs** pctx, item\_code.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** float.

**Explicit results** \_get\_batch\_based\_item\_price(pctx, item\_code).

**Local steps**

- Set pctx from Platform.\_dict(parse\_json(pctx)).
- Evaluate validate\_pricing\_context(pctx).
- Return \_get\_batch\_based\_item\_price(pctx, item\_code).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1174) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L714)

<a id="op-4137ef2279d623"></a>
### Get batch based item price

`operation_enterprise_binding_enterprise_stock_get_item_details_get_batch_based_item_price`

**Inputs** pctx, item\_code.

**Declared result** float.

**Explicit results** item\_price at 0.price\_list\_rate · 0.0.

**Local steps**

- Set pctx from parse\_json(pctx).
- Set item\_price from get\_item\_price(pctx, item\_code, force\_batch\_no = true).
- If not item\_price.
  - Set item\_price from get\_item\_price(pctx, item\_code, ignore\_party = true, force\_batch\_no = true).
- Set is\_free\_item from pctx.get(“items”, list(mapping())) at 0.get(“is\_free\_item”).
- If (item\_price and item\_price at 0.uom equals pctx.uom and not is\_free\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_price → item\_price at 0.uom equals pctx.uom → not is\_free\_item.
  - Return item\_price at 0.price\_list\_rate.
- Return 0.0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1421) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L918)

<a id="op-2cd97bcdef4ed9"></a>
### Get price list rate for

`operation_enterprise_stock_get_item_details_business_behavior_get_price_list_rate_for`

**Inputs** ctx, item\_code.

**Wrappers, in declaration order** Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Explicit results** item\_price\_data at 0.price\_list\_rate · flt((item\_price\_data at 0.price\_list\_rate × flt(ctx.get(“conversion\_factor”, 1)))).

**Local steps**

- Set pctx from ItemPriceCtx(mapping(“item\_code” → item\_code, “price\_list” → ctx.get(“price\_list”), “customer” → ctx.get(“customer”), “supplier” → ctx.get(“supplier”), …)).
- Set item\_price\_data from 0.
- Set price\_list\_rate from get\_item\_price(pctx, item\_code, limit = no value).
- If price\_list\_rate.
  - If desired\_qty bound to ctx.get(“qty”).
    - Set item\_price\_data from get\_prices\_fitting\_packing\_unit(price\_list\_rate, desired\_qty).
- Otherwise.
  - Set general\_price\_list\_rate from (ctx.get(“ignore\_party”) and get\_item\_price(pctx, item\_code, ignore\_party = true)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.get(“ignore\_party”) → get\_item\_price(pctx, item\_code, ignore\_party = true).
  - If (not general\_price\_list\_rate and ctx.get(“uom”) differs from ctx.get(“stock\_uom”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not general\_price\_list\_rate → ctx.get(“uom”) differs from ctx.get(“stock\_uom”).
    - Set pctx.uom from ctx.get(“stock\_uom”).
    - Set general\_price\_list\_rate from get\_item\_price(pctx, item\_code, ignore\_party = ctx.get(“ignore\_party”)).
  - If general\_price\_list\_rate.
    - Set item\_price\_data from general\_price\_list\_rate.
- If item\_price\_data.
  - If item\_price\_data at 0.uom equals ctx.get(“uom”).
    - Return item\_price\_data at 0.price\_list\_rate.
  - Otherwise.
    - If not ctx.get(“price\_list\_uom\_dependant”).
      - Return flt((item\_price\_data at 0.price\_list\_rate × flt(ctx.get(“conversion\_factor”, 1)))).
    - Otherwise.
      - Return item\_price\_data at 0.price\_list\_rate.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1206) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L746)

<a id="op-fd14df42176a77"></a>
### Get prices fitting packing unit

`operation_enterprise_binding_enterprise_stock_get_item_details_get_prices_fitting_packing_unit`

**Inputs** item\_prices, desired\_qty.

**Explicit results** list(item\_price) · list().

**Local steps**

- For each item\_price in item\_prices.
  - If (not item\_price.packing\_unit or (flt(desired\_qty) modulo or format flt(item\_price.packing\_unit)) equals 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_price.packing\_unit → (flt(desired\_qty) modulo or format flt(item\_price.packing\_unit)) equals 0.
    - Return list(item\_price).
- Return list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L931)

<a id="op-978d0a70815883"></a>
### Check packing list

`operation_enterprise_stock_get_item_details_business_behavior_check_packing_list`

**Inputs** price\_list\_rate\_name, desired\_qty, item\_code.

**Record and data access** read “Item Price” via get\_value.

**Explicit results** flag.

**Local steps**

- Set flag from true.
- If packing\_unit bound to Platform.db.get\_value(“Item Price”, price\_list\_rate\_name, “packing\_unit”, cache = true).
  - Set packing\_increment from (desired\_qty modulo or format packing\_unit).
  - If packing\_increment differs from 0.
    - Set flag from false.
- Return flag.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0882.json#L4735) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1169) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L709)

<a id="op-e6c04984b624da"></a>
### Validate conversion rate

`operation_enterprise_stock_get_item_details_business_behavior_validate_conversion_rate`

**Inputs** ctx, meta.

**Record and data access** read “Company” via get\_cached\_value · read “Price List” via get\_value.

**Local steps**

- Bind dependencies validate\_conversion\_rate.
- Set company\_currency from Platform.get\_cached\_value(“Company”, ctx.company, “default\_currency”).
- If (not ctx.conversion\_rate and ctx.currency equals company\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not ctx.conversion\_rate → ctx.currency equals company\_currency.
  - Set ctx.conversion\_rate from 1.0.
- If (not ctx.ignore\_conversion\_rate and ctx.conversion\_rate equals 1 and ctx.currency differs from company\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not ctx.ignore\_conversion\_rate → ctx.conversion\_rate equals 1 → ctx.currency differs from company\_currency.
  - Set ctx.conversion\_rate from (get\_exchange\_rate(ctx.currency, company\_currency, ctx.transaction\_date, “for\_buying”) or 1.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_exchange\_rate(ctx.currency, company\_currency, ctx.transaction\_date, “for\_buying”) → 1.0.
- Evaluate validate\_conversion\_rate(ctx.currency, ctx.conversion\_rate, meta.get\_label(“conversion\_rate”), ctx.company).
- Set ctx.conversion\_rate from flt(ctx.conversion\_rate, get\_field\_precision(meta.get\_field(“conversion\_rate”), Platform.\_dict(mapping(“fields” → ctx)))).
- If ctx.price\_list.
  - If (not ctx.plc\_conversion\_rate and ctx.price\_list\_currency equals Platform.db.get\_value(“Price List”, ctx.price\_list, “currency”, cache = true)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not ctx.plc\_conversion\_rate → ctx.price\_list\_currency equals Platform.db.get\_value(“Price List”, ctx.price\_list, “currency”, cache = true).
    - Set ctx.plc\_conversion\_rate from 1.0.
  - If not ctx.price\_list\_currency.
    - Evaluate throw(translated “Price List Currency not selected”).
  - Otherwise.
    - Evaluate validate\_conversion\_rate(ctx.price\_list\_currency, ctx.plc\_conversion\_rate, meta.get\_label(“plc\_conversion\_rate”), ctx.company).
    - If meta.get\_field(“plc\_conversion\_rate”).
      - Set ctx.plc\_conversion\_rate from flt(ctx.plc\_conversion\_rate, get\_field\_precision(meta.get\_field(“plc\_conversion\_rate”), Platform.\_dict(mapping(“fields” → ctx)))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, ctx.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L765)

<a id="op-38fee107eebf6f"></a>
### Get party item code

`operation_enterprise_stock_get_item_details_business_behavior_get_party_item_code`

**Inputs** ctx, item\_doc, out.

**Record and data access** read “Customer” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If (ctx.transaction\_type equals “selling” and ctx.customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.transaction\_type equals “selling” → ctx.customer.
  - Set out.customer\_item\_code from no value.
  - If (ctx.quotation\_to and ctx.quotation\_to differs from “Customer”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.quotation\_to → ctx.quotation\_to differs from “Customer”.
    - Return no value.
  - Set customer\_item\_code from item\_doc.get(“customer\_items”, mapping(“customer\_name” → ctx.customer)).
  - If customer\_item\_code.
    - Set out.customer\_item\_code from customer\_item\_code at 0.ref\_code.
  - Otherwise.
    - Set customer\_group from Platform.get\_cached\_value(“Customer”, ctx.customer, “customer\_group”).
    - Set customer\_group\_item\_code from item\_doc.get(“customer\_items”, mapping(“customer\_group” → customer\_group)).
    - If (customer\_group\_item\_code and not customer\_group\_item\_code at 0.customer\_name).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in customer\_group\_item\_code → not customer\_group\_item\_code at 0.customer\_name.
      - Set out.customer\_item\_code from customer\_group\_item\_code at 0.ref\_code.
- If (ctx.transaction\_type equals “buying” and ctx.supplier).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.transaction\_type equals “buying” → ctx.supplier.
  - Set item\_supplier from item\_doc.get(“supplier\_items”, mapping(“supplier” → ctx.supplier)).
  - Set out.supplier\_part\_no from item\_supplier at 0.supplier\_part\_no when item\_supplier, otherwise no value.
    - Value choice on item\_supplier — true gives item\_supplier at 0.supplier\_part\_no, false gives no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Customer”, ctx.customer, “customer\_group”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1201) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L741)

<a id="op-b2c74b86bbc40f"></a>
### Get tax withholding category

`operation_enterprise_stock_get_item_details_business_behavior_get_tax_withholding_category`

**Inputs** ctx, item\_doc, out.

**Record and data access** read “Supplier” via get\_cached\_value · read “Customer” via get\_cached\_value.

**Local steps**

- Set tax\_withholding\_category from no value.
- Set field from “sales\_tax\_withholding\_category” when ctx.transaction\_type equals “selling”, otherwise “purchase\_tax\_withholding\_category”.
  - Value choice on ctx.transaction\_type equals “selling” — true gives “sales\_tax\_withholding\_category”, false gives “purchase\_tax\_withholding\_category”.
- If item\_doc.get(field).
  - Set tax\_withholding\_category from item\_doc.get(field).
- Otherwise.
  - If (ctx.transaction\_type equals “buying” and ctx.supplier).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.transaction\_type equals “buying” → ctx.supplier.
    - Set tax\_withholding\_category from Platform.get\_cached\_value(“Supplier”, ctx.supplier, “tax\_withholding\_category”).
  - Otherwise.
    - If (ctx.transaction\_type equals “selling” and ctx.customer).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.transaction\_type equals “selling” → ctx.customer.
      - Set tax\_withholding\_category from Platform.get\_cached\_value(“Customer”, ctx.customer, “tax\_withholding\_category”).
- Set out.tax\_withholding\_category from tax\_withholding\_category.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Supplier”, ctx.supplier, “tax\_withholding\_category”), Platform.get\_cached\_value(“Customer”, ctx.customer, “tax\_withholding\_category”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L752)

<a id="op-8e4eab7b512347"></a>
### Get pos profile item details

`operation_enterprise_stock_get_item_details_business_behavior_get_point_of_sale_profile_item_details`

**Inputs** ctx, company, pos\_profile = no value, update\_data = false.

**Wrappers, in declaration order** Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Explicit results** res.

**Local steps**

- Set res from Platform.\_dict().
- If (not Platform.flags.pos\_profile and not pos\_profile).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.flags.pos\_profile → not pos\_profile.
  - Set pos\_profile, Platform.flags.pos\_profile from get\_pos\_profile(company, ctx.pos\_profile).
- If pos\_profile.
  - For each fieldname in tuple(“income\_account”, “cost\_center”, “warehouse”, “expense\_account”).
    - If ((not ctx.get(fieldname) or update\_data) and pos\_profile.get(fieldname)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not ctx.get(fieldname) or update\_data) → pos\_profile.get(fieldname).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not ctx.get(fieldname) → update\_data.
      - Set res at fieldname from pos\_profile.get(fieldname).
  - If res.get(“warehouse”).
    - Set res.actual\_qty from \_get\_bin\_details(ctx.item\_code, res.warehouse, include\_child\_warehouses = true).get(“actual\_qty”).
- Return res.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1203) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L743)

<a id="op-9f9208deb1fe8d"></a>
### Get pos profile

`operation_enterprise_stock_get_item_details_business_behavior_get_point_of_sale_profile`

**Inputs** company, pos\_profile = no value, user = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “POS Profile” via get\_cached\_doc · read “POS Profile” via get\_list.

**Explicit results** Platform.get\_cached\_doc(“POS Profile”, pos\_profile) · no value · ((pos\_profile and pos\_profile at 0) or no value).

**Local steps**

- If pos\_profile.
  - Evaluate Platform.has\_permission(“POS Profile”, “read”, doc = pos\_profile, throw = true).
  - Return Platform.get\_cached\_doc(“POS Profile”, pos\_profile).
- If not user.
  - Set user from Platform.session at “user”.
- Set allowed\_pos\_profiles from Platform.get\_list(“POS Profile”, pluck = “name”).
- If not allowed\_pos\_profiles.
  - Return no value.
- Set pf from Platform.qb.DocType(“POS Profile”).
- Set pfu from Platform.qb.DocType(“POS Profile User”).
- Set query from nested operand in the contract(nested operand in the contract).select(pf.star).where((pfu.user equals user bitwise and pfu.default equals 1)).where(pf.name.isin(allowed\_pos\_profiles)).
- If company.
  - Set query from query.where(pf.company equals company).
- Set pos\_profile from query.run(as\_dict = true).
- If (not pos\_profile and company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not pos\_profile → company.
  - Set pos\_profile from nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand i ….
- Return ((pos\_profile and pos\_profile at 0) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (pos\_profile and pos\_profile at 0) → no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pos\_profile → pos\_profile at 0.

**Values supplied outside this operation** effective access from Platform.has\_permission(“POS Profile”, “read”, doc = pos\_profile, throw = true) · configured or stored value from Platform.get\_cached\_doc(“POS Profile”, pos\_profile).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1202) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L742)

<a id="op-75cfc69feb3784"></a>
### Get conversion factor

`operation_enterprise_stock_get_item_details_business_behavior_get_conversion_factor`

**Inputs** item\_code, uom, throw\_if\_missing = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** mapping(“conversion\_factor” → 1.0) · mapping(“conversion\_factor” → (conversion\_factor or 1.0)).

**Local steps**

- Set item from Platform.get\_cached\_value(“Item”, item\_code, list(“variant\_of”, “stock\_uom”, “is\_stock\_item”), as\_dict = true).
- If (not item\_code or not item or uom equals item.stock\_uom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_code → not item → uom equals item.stock\_uom.
  - Return mapping(“conversion\_factor” → 1.0).
- Set item\_codes from list(item\_code).
- If item.variant\_of.
  - Evaluate item\_codes.append(item.variant\_of).
- Set parent from Platform.qb.DocType(“Item”).
- Set child from Platform.qb.DocType(“UOM Conversion Detail”).
- Set query from nested operand in the contract(nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contract equals nested operand in the  ….
- Set conversion\_factor from query.run(pluck = “conversion\_factor”).
- If not conversion\_factor.
  - Set conversion\_factor from get\_uom\_conv\_factor(uom, item.stock\_uom).
- Otherwise.
  - Set conversion\_factor from conversion\_factor at 0.
- If (throw\_if\_missing and not conversion\_factor and item.is\_stock\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in throw\_if\_missing → not conversion\_factor → item.is\_stock\_item.
  - Evaluate throw(translated “UOM {0} has no conversion factor in Item {1}.”.format(uom, item\_code)).
- Return mapping(“conversion\_factor” → (conversion\_factor or 1.0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conversion\_factor → 1.0.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, list(“variant\_of”, “stock\_uom”, “is\_stock\_item”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1180) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L720)

<a id="op-d043b81f9bd5bf"></a>
### Get projected qty

`operation_enterprise_stock_get_item_details_business_behavior_get_projected_quantity`

**Inputs** item\_code, warehouse.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Bin” via get\_value.

**Explicit results** mapping(“projected\_qty” → Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse), “projected\_qty”)).

**Local steps**

- Evaluate Platform.has\_permission(“Item”, doc = item\_code, throw = true).
- Evaluate Enterprise.require\_user\_permission(“Warehouse”, warehouse).
- Return mapping(“projected\_qty” → Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse), “projected\_qty”)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, doc = item\_code, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1207) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L747)

<a id="op-ea6984f1cd0d23"></a>
### Get bin details

`operation_enterprise_stock_get_item_details_business_behavior_get_bin_details`

**Inputs** item\_code, warehouse, company = no value, include\_child\_warehouses = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_bin\_details(item\_code, warehouse, company, include\_child\_warehouses).

**Local steps**

- Evaluate Platform.has\_permission(“Item”, ptype = “select”, throw = true).
- If warehouse.
  - Evaluate Enterprise.require\_user\_permission(“Warehouse”, warehouse).
- Return \_get\_bin\_details(item\_code, warehouse, company, include\_child\_warehouses).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, ptype = “select”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1177) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L717)
