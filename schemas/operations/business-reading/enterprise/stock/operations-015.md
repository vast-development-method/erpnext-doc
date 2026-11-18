# Inventory and warehouses · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Get item details

<a id="op-d3d4ecee6df523"></a>
### Get item code

`operation_enterprise_stock_get_item_details_business_behavior_get_item_code`

**Inputs** barcode = no value, serial\_no = no value.

**Record and data access** read “Item Barcode” via get\_value · read “Serial No” via get\_value.

**Explicit results** item\_code.

**Explicit failure paths** validation helper — translated “No Item with Barcode {0}”.format(barcode) · validation helper — translated “No Item with Serial No {0}”.format(serial\_no).

**Local steps**

- If barcode.
  - Set item\_code from Platform.db.get\_value(“Item Barcode”, mapping(“barcode” → barcode), fieldname = list(“parent”)).
  - If not item\_code.
    - Call the validation error handler Platform.throw(translated “No Item with Barcode {0}”.format(barcode)).
- Otherwise.
  - If serial\_no.
    - Set item\_code from Platform.db.get\_value(“Serial No”, serial\_no, “item\_code”).
    - If not item\_code.
      - Call the validation error handler Platform.throw(translated “No Item with Serial No {0}”.format(serial\_no)).
- Return item\_code.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0879.json#L6933) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1192) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L732)

<a id="op-636da4d1f61f2a"></a>
### Validate item details

`operation_enterprise_stock_get_item_details_business_behavior_validate_item_details`

**Inputs** ctx, item.

**Local steps**

- If not ctx.company.
  - Evaluate throw(translated “Please specify Company”).
- Bind dependencies validate\_end\_of\_life.
- Evaluate validate\_end\_of\_life(item.name, item.end\_of\_life, item.disabled).
- If cint(item.has\_variants).
  - Set msg from formatted text Item {item.name} is a template, please select one of its variants.
  - Evaluate throw(translated msg, title = translated “Template Item Selected”).
- Otherwise.
  - If ctx.doctype differs from “Material Request”.
    - If ctx.is\_subcontracted.
      - If ctx.is\_old\_subcontracting\_flow.
        - If item.is\_sub\_contracted\_item differs from 1.
          - Evaluate throw(translated “Item {0} must be a Sub-contracted Item”.format(item.name)).
      - Otherwise.
        - If item.is\_stock\_item.
          - Evaluate throw(translated “Item {0} must be a Non-Stock Item”.format(item.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1226) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L766)

<a id="op-d585cf4b6fc587"></a>
### Get basic details

`operation_enterprise_stock_get_item_details_business_behavior_get_basic_details`

**Inputs** ctx, item, overwrite\_warehouse = true.

**Declared result** ItemDetails.

**Record and data access** resolve a document from “Item” via get\_cached\_doc · read “Item Tax” via exists · read “Material Request” via get\_value · read “Batch” via get\_cached\_value · read “Company” via get\_cached\_value · 2 additional forms in the steps below.

**Explicit results** out.

**Local steps**

- If not item.
  - Set item from Platform.get\_cached\_doc(“Item”, ctx.item\_code).
- If (item.variant\_of and not item.taxes and Platform.db.exists(“Item Tax”, mapping(“parent” → item.variant\_of))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.variant\_of → not item.taxes → Platform.db.exists(“Item Tax”, mapping(“parent” → item.variant\_of)).
  - Evaluate item.update\_template\_tables().
- Set item\_defaults from get\_item\_defaults(item.name, ctx.company).
- Set item\_group\_defaults from get\_item\_group\_defaults(item.name, ctx.company).
- Set brand\_defaults from get\_brand\_defaults(item.name, ctx.company).
- Set defaults from Platform.\_dict(mapping(“item\_defaults” → item\_defaults, “item\_group\_defaults” → item\_group\_defaults, “brand\_defaults” → brand\_defaults)).
- Set warehouse from get\_item\_warehouse\_(ctx, item, overwrite\_warehouse, defaults).
- If (ctx.doctype equals “Material Request” and not ctx.material\_request\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.doctype equals “Material Request” → not ctx.material\_request\_type.
  - Set ctx at “material\_request\_type” from Platform.db.get\_value(“Material Request”, ctx.name, “material\_request\_type”, cache = true).
- Set expense\_account from no value.
- If item.is\_fixed\_asset.
  - Bind dependencies get\_asset\_account, is\_cwip\_accounting\_enabled.
  - If is\_cwip\_accounting\_enabled(item.asset\_category).
    - Set expense\_account from get\_asset\_account(“capital\_work\_in\_progress\_account”, asset\_category = item.asset\_category, company = ctx.company).
  - Otherwise.
    - If ctx.doctype belongs to tuple(“Purchase Invoice”, “Purchase Receipt”, “Purchase Order”, “Material Request”).
      - Bind dependencies get\_asset\_category\_account.
      - Set expense\_account from get\_asset\_category\_account(fieldname = “fixed\_asset\_account”, item = ctx.item\_code, company = ctx.company).
- If not ctx.uom.
  - If ctx.doctype belongs to sales\_doctypes.
    - Set ctx.uom from item.sales\_uom when item.sales\_uom, otherwise item.stock\_uom.
      - Value choice on item.sales\_uom — true gives item.sales\_uom, false gives item.stock\_uom.
  - Otherwise.
    - If (ctx.doctype belongs to list(“Purchase Order”, “Purchase Receipt”, “Purchase Invoice”) or (ctx.doctype equals “Material Request” and ctx.material\_request\_type equals “Purchase”) or ctx.doctype equals “Supp ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.doctype belongs to list(“Purchase Order”, “Purchase Receipt”, “Purchase Invoice”) → (ctx.doctype equals “Material Request” and ctx.material\_request\_type equals “Purchase”) → ctx.doctype equals “Supplier Quotation”.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.doctype equals “Material Request” → ctx.material\_request\_type equals “Purchase”.
      - Set ctx.uom from item.purchase\_uom when item.purchase\_uom, otherwise item.stock\_uom.
        - Value choice on item.purchase\_uom — true gives item.purchase\_uom, false gives item.stock\_uom.
    - Otherwise.
      - Set ctx.uom from item.stock\_uom.
- Set ctx.stock\_uom from item.stock\_uom.
- If (ctx.batch\_no and item.name differs from Platform.get\_cached\_value(“Batch”, ctx.batch\_no, “item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.batch\_no → item.name differs from Platform.get\_cached\_value(“Batch”, ctx.batch\_no, “item”).
  - Set ctx.batch\_no from empty text.
- Set out from ItemDetails(mapping(“item\_code” → item.name, “item\_name” → item.item\_name, “description” → cstr(item.description).strip(), “image” → cstr(item.image).strip(), …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in expense\_account → get\_default\_expense\_account(ctx, item\_defaults, item\_group\_defaults, brand\_defaults).
  - Value choice on ctx.doctype equals “Material Request” — true gives flt(item.min\_order\_qty), false gives empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(ctx.qty) → 1.0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(ctx.qty) → 1.0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(ctx.discount\_amount) → 0.0.
  - Value choice on ctx.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”) — true gives ctx.update\_stock, false gives 0.
  - Value choice on ctx.doctype belongs to list(“Sales Order”, “Sales Invoice”) — true gives item.delivered\_by\_supplier, false gives 0.
  - Value choice on ctx.doctype belongs to list(“Purchase Order”) — true gives item.last\_purchase\_rate, false gives 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.weight\_per\_unit → item.get(“weight\_per\_unit”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.weight\_uom → item.get(“weight\_uom”).
- If (not item.is\_stock\_item and not out.expense\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.is\_stock\_item → not out.expense\_account.
  - Set out.expense\_account from Platform.get\_cached\_value(“Company”, ctx.company, “service\_expense\_account”).
- Set default\_supplier from get\_default\_supplier(ctx, item\_defaults, item\_group\_defaults, brand\_defaults).
- If default\_supplier.
  - Set out.supplier from default\_supplier.
- If (item.get(“enable\_deferred\_revenue”) or item.get(“enable\_deferred\_expense”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“enable\_deferred\_revenue”) → item.get(“enable\_deferred\_expense”).
  - Evaluate out.update(calculate\_service\_end\_date(ctx, item)).
- If item.stock\_uom equals ctx.uom.
  - Set out.conversion\_factor from 1.0.
- Otherwise.
  - Set out.conversion\_factor from (ctx.conversion\_factor or get\_conversion\_factor(item.name, ctx.uom, throw\_if\_missing = true).get(“conversion\_factor”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.conversion\_factor → get\_conversion\_factor(item.name, ctx.uom, throw\_if\_missing = true).get(“conversion\_factor”).
- Set ctx.conversion\_factor from out.conversion\_factor.
- Set out.stock\_qty from (out.qty × out.conversion\_factor).
- Set ctx.stock\_qty from out.stock\_qty.
- If (ctx.doctype belongs to purchase\_doctypes and not Platform.db.get\_single\_value(“Buying Settings”, “disable\_last\_purchase\_rate”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.doctype belongs to purchase\_doctypes → not Platform.db.get\_single\_value(“Buying Settings”, “disable\_last\_purchase\_rate”).
  - Bind dependencies item\_last\_purchase\_rate.
  - Set out.last\_purchase\_rate from item\_last\_purchase\_rate(ctx.name, ctx.conversion\_rate, item.name, out.conversion\_factor).
- Set expense\_account\_field from “default\_expense\_account”.
- If (item.is\_stock\_item and Enterprise.is\_perpetual\_inventory\_enabled(ctx.company) and (ctx.doctype equals “Purchase Receipt” or (ctx.doctype equals “Purchase Invoice” and ctx.get(“update\_stock”)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.is\_stock\_item → Enterprise.is\_perpetual\_inventory\_enabled(ctx.company) → (ctx.doctype equals “Purchase Receipt” or (ctx.doctype equals “Purchase Invoice” and ctx.get(“update\_stock”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.doctype equals “Purchase Receipt” → (ctx.doctype equals “Purchase Invoice” and ctx.get(“update\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.doctype equals “Purchase Invoice” → ctx.get(“update\_stock”).
  - Set expense\_account\_field from “stock\_received\_but\_not\_billed”.
- For each d in list(list(“Account”, “income\_account”, “default\_income\_account”), list(“Account”, “expense\_account”, expense\_account\_field), list(“Cost Center”, “cost\_center”, “cost\_center”), list(“Warehouse”, “warehouse” ….
  - If not out at d at 1.
    - Set out at d at 1 from Platform.get\_cached\_value(“Company”, ctx.company, d at 2) when d at 2, otherwise no value.
      - Value choice on d at 2 — true gives Platform.get\_cached\_value(“Company”, ctx.company, d at 2), false gives no value.
- For each fieldname in tuple(“item\_name”, “item\_group”, “brand”, “stock\_uom”).
  - Set out at fieldname from item.get(fieldname).
- If ctx.manufacturer.
  - Set part\_no from \_get\_item\_manufacturer\_part\_no(ctx.item\_code, ctx.manufacturer).
  - If part\_no.
    - Set out.manufacturer\_part\_no from part\_no.
  - Otherwise.
    - Set out.manufacturer\_part\_no from no value.
    - Set out.manufacturer from no value.
- Otherwise.
  - Set data from Platform.get\_cached\_value(“Item”, item.name, list(“default\_item\_manufacturer”, “default\_manufacturer\_part\_no”), as\_dict = true).
  - If data.
    - Evaluate out.update(mapping(“manufacturer” → data.default\_item\_manufacturer, “manufacturer\_part\_no” → data.default\_manufacturer\_part\_no)).
- Set child\_doctype from (ctx.doctype + “ Item”).
- Set meta from Platform.get\_meta(child\_doctype).
- If meta.get\_field(“barcode”).
  - Evaluate update\_barcode\_value(out).
- If out.weight\_per\_unit.
  - Set out.total\_weight from (out.weight\_per\_unit × out.stock\_qty).
- Return out.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, ctx.item\_code), Platform.get\_cached\_value(“Batch”, ctx.batch\_no, “item”) and 4 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1173) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L713)

<a id="op-727c43efdaccb0"></a>
### Get item warehouse

`operation_enterprise_stock_get_item_details_business_behavior_get_item_warehouse`

**Inputs** ctx, item, overwrite\_warehouse, defaults = no value.

**Wrappers, in declaration order** Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** get\_accessible\_warehouse(Platform.get\_cached\_value(“Company”, ctx.company, “default\_warehouse”)) · warehouse.

**Local steps**

- If not defaults.
  - Set defaults from Platform.\_dict(mapping(“item\_defaults” → get\_item\_defaults(item.name, ctx.company), “item\_group\_defaults” → get\_item\_group\_defaults(item.name, ctx.company), “brand\_defaults” → get\_brand\_defaults(item.name, ….
- If (overwrite\_warehouse or not ctx.warehouse).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in overwrite\_warehouse → not ctx.warehouse.
  - Set warehouse from (ctx.set\_warehouse or get\_accessible\_warehouse(defaults.item\_defaults.get(“default\_warehouse”), defaults.item\_group\_defaults.get(“default\_warehouse”), defaults.brand\_defaults.get(“default\_warehouse”)) or c ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.set\_warehouse → get\_accessible\_warehouse(defaults.item\_defaults.get(“default\_warehouse”), defaults.item\_group\_defaults.get(“default\_warehouse”), defaults.brand\_defaults.get(“default\_warehouse”)) → ctx.warehouse.
- Otherwise.
  - Set warehouse from ctx.warehouse.
- If (not warehouse and ctx.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not warehouse → ctx.company.
  - Return get\_accessible\_warehouse(Platform.get\_cached\_value(“Company”, ctx.company, “default\_warehouse”)).
- Return warehouse.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, ctx.company, “default\_warehouse”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1200) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L740)

<a id="op-1897600be146d4"></a>
### Get accessible warehouse

`operation_enterprise_binding_enterprise_stock_get_item_details_get_accessible_warehouse`

**Inputs** remaining positional values warehouses.

**Declared result** (str bitwise or no value).

**Explicit results** next(iter(warehouses), no value) · next(generator of warehouse for warehouse drawn from warehouses where Enterprise.\_is\_within\_user\_permissions(“Warehouse”, warehouse), no value).

**Local steps**

- Set warehouses from list of warehouse for warehouse drawn from warehouses where warehouse.
  - Draw warehouse from warehouses, keep a combination only if (warehouse).
- If not get\_user\_permissions().get(“Warehouse”).
  - Return next(iter(warehouses), no value).
- Return next(generator of warehouse for warehouse drawn from warehouses where Enterprise.\_is\_within\_user\_permissions(“Warehouse”, warehouse), no value).
  - Draw warehouse from warehouses, keep a combination only if (Enterprise.\_is\_within\_user\_permissions(“Warehouse”, warehouse)).

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1419) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L916)

<a id="op-38ee27a7289232"></a>
### Update barcode value

`operation_enterprise_stock_get_item_details_business_behavior_update_barcode_value`

**Inputs** out.

**Local steps**

- Set barcode\_data from get\_barcode\_data(list(out)).
- If (barcode\_data and len(barcode\_data.get(out.item\_code)) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in barcode\_data → len(barcode\_data.get(out.item\_code)) equals 1.
  - Set out at “barcode” from barcode\_data.get(out.item\_code) at 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0880.json#L5141) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1221) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L761)

<a id="op-635aff5c8db16c"></a>
### Get barcode data

`operation_enterprise_stock_get_item_details_business_behavior_get_barcode_data`

**Inputs** items\_list = no value, item\_code = no value.

**Record and data access** read “Item Barcode” via get\_all.

**Explicit results** itemwise\_barcode.

**Local steps**

- Set itemwise\_barcode from mapping().
- If (not items\_list and item\_code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not items\_list → item\_code.
  - Set \_dict\_item\_code from Platform.\_dict(mapping(“item\_code” → item\_code)).
  - Set items\_list from list(Platform.\_dict(\_dict\_item\_code)).
- For each item in items\_list.
  - Set barcodes from Platform.db.get\_all(“Item Barcode”, filters = mapping(“parent” → item.item\_code), fields = “barcode”).
  - For each barcode in barcodes.
    - If item.item\_code does not belong to itemwise\_barcode.
      - Evaluate itemwise\_barcode.setdefault(item.item\_code, list()).
    - Evaluate itemwise\_barcode at item.item\_code.append(barcode.get(“barcode”)).
- Return itemwise\_barcode.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0880.json#L5320) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1172) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L712)

<a id="op-fc43aa62cd3ad7"></a>
### Get item tax info

`operation_enterprise_stock_get_item_details_business_behavior_get_item_tax_info`

**Inputs** doc, tax\_category, item\_codes, item\_rates = no value, item\_tax\_templates = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit results** out.

**Explicit failure paths** validation helper — translated “Invalid Item Code”.

**Local steps**

- Set out from mapping().
- If item\_tax\_templates is identical to no value.
  - Set item\_tax\_templates from mapping().
- If item\_rates is identical to no value.
  - Set item\_rates from mapping().
- Set doc from parse\_json(doc).
- Set item\_codes from parse\_json(item\_codes).
- Set item\_rates from parse\_json(item\_rates).
- Set item\_tax\_templates from parse\_json(item\_tax\_templates).
- For each item\_code in item\_codes.
  - If (not item\_code or item\_code at 1 belongs to out or not item\_tax\_templates.get(item\_code at 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_code → item\_code at 1 belongs to out → not item\_tax\_templates.get(item\_code at 1).
    - Continue with the next iteration or loop test.
  - If not isinstance(item\_code at 0, str).
    - Call the validation error handler Platform.throw(translated “Invalid Item Code”).
  - Set out at item\_code at 1 from ItemDetails().
  - Set item from Platform.get\_cached\_doc(“Item”, item\_code at 0).
  - Set ctx from mapping(“company” → doc.company, “tax\_category” → tax\_category, “base\_net\_rate” → item\_rates.get(item\_code at 1)).
  - If item\_tax\_templates.
    - Evaluate ctx.update(mapping(“item\_tax\_template” → item\_tax\_templates.get(item\_code at 1))).
  - Evaluate get\_item\_tax\_template(ctx, item, out at item\_code at 1).
  - Set out at item\_code at 1 at “item\_tax\_rate” from \_get\_item\_tax\_map(doc = doc, tax\_template = out at item\_code at 1.get(“item\_tax\_template”), as\_json = true).
- For each item\_tax\_template in set of row.item\_tax\_template for row drawn from out.values() where row.item\_tax\_template.
  - Draw row from out.values(), keep a combination only if (row.item\_tax\_template).
  - Evaluate Enterprise.require\_permission(“Item Tax Template”, item\_tax\_template, “select”).
- Return out.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, item\_code at 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L735)

<a id="op-8305fb8c47fe23"></a>
### Get item tax template

`operation_enterprise_stock_get_item_details_business_behavior_get_item_tax_template`

**Inputs** ctx, item = no value, out = no value.

**Wrappers, in declaration order** Platform.whitelist(), Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit results** item\_tax\_template.

**Explicit failure paths** validation helper — translated “Item/Item Code required to get Item Tax Template.”.

**Local steps**

- If not item.
  - If (not ctx.get(“item\_code”) or not isinstance(ctx.item\_code, str)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not ctx.get(“item\_code”) → not isinstance(ctx.item\_code, str).
    - Call the validation error handler Platform.throw(translated “Item/Item Code required to get Item Tax Template.”).
  - Otherwise.
    - Set item from Platform.get\_cached\_doc(“Item”, ctx.item\_code).
- Set item\_tax\_template from no value.
- If item.taxes.
  - Set item\_tax\_template from \_get\_item\_tax\_template(ctx, item.taxes, out).
- If not item\_tax\_template.
  - Set item\_tax\_template from \_get\_item\_tax\_template\_from\_item\_group(ctx, item.item\_group, out).
- If (out and ctx.get(“child\_doctype”) and item\_tax\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in out → ctx.get(“child\_doctype”) → item\_tax\_template.
  - Evaluate out.update(get\_fetch\_values(ctx.get(“child\_doctype”), “item\_tax\_template”, item\_tax\_template)).
- Return item\_tax\_template.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, ctx.item\_code).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L737)

<a id="op-9d7744a9603d38"></a>
### Get item tax template from item group

`operation_enterprise_stock_get_item_details_business_behavior_get_item_tax_template_from_item_group`

**Inputs** ctx, item\_group, out = no value.

**Record and data access** resolve a document from “Item Group” via get\_cached\_doc.

**Explicit results** item\_tax\_template · no value.

**Local steps**

- While item\_group.
  - Set group\_doc from Platform.get\_cached\_doc(“Item Group”, item\_group).
  - Set item\_tax\_template from \_get\_item\_tax\_template(ctx, group\_doc.taxes, out).
  - If item\_tax\_template.
    - Return item\_tax\_template.
  - Set item\_group from group\_doc.parent\_item\_group.
- Return no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item Group”, item\_group).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1199) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L739)

<a id="op-1f5785e72c1086"></a>
### Get item tax template

`operation_enterprise_stock_get_item_details_business_behavior_get_item_tax_template_2`

**Inputs** ctx, taxes, out = no value, for\_validate = false.

**Wrappers, in declaration order** Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Declared result** ((no value bitwise or str) bitwise or list at str).

**Explicit results** category\_templates · ctx.get(“item\_tax\_template”) · category\_templates at 0 · no value.

**Local steps**

- If out is identical to no value.
  - Set out from ItemDetails().
- Set taxes from get\_latest\_item\_taxes(get\_applicable\_item\_taxes(ctx, taxes)).
- Set category\_templates from list of tax.item\_tax\_template for tax drawn from taxes where cstr(tax.tax\_category) equals cstr(ctx.get(“tax\_category”)).
  - Draw tax from taxes, keep a combination only if (cstr(tax.tax\_category) equals cstr(ctx.get(“tax\_category”))).
- If for\_validate.
  - Return category\_templates.
- If ctx.get(“item\_tax\_template”) belongs to (category\_templates or set of t.item\_tax\_template for t drawn from taxes).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in category\_templates → set of t.item\_tax\_template for t drawn from taxes.
  - Draw t from taxes.
  - Set out.item\_tax\_template from ctx.get(“item\_tax\_template”).
  - Return ctx.get(“item\_tax\_template”).
- If category\_templates.
  - Set out.item\_tax\_template from category\_templates at 0.
  - Return category\_templates at 0.
- Return no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L738)

<a id="op-4895bc4804b71e"></a>
### Get applicable item taxes

`operation_enterprise_binding_enterprise_stock_get_item_details_get_applicable_item_taxes`

**Inputs** ctx, taxes.

**Declared result** list.

**Record and data access** read “Item Tax Template” via get\_cached\_value.

**Explicit results** applicable\_taxes.

**Local steps**

- Set validation\_date from getdate((ctx.get(“bill\_date”) or ctx.get(“posting\_date”) or ctx.get(“transaction\_date”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.get(“bill\_date”) → ctx.get(“posting\_date”) → ctx.get(“transaction\_date”).
- Set applicable\_taxes from list().
- For each tax in taxes.
  - Set tuple(disabled, tax\_company) from Platform.get\_cached\_value(“Item Tax Template”, tax.item\_tax\_template, list(“disabled”, “company”)).
  - If (not disabled and tax\_company equals ctx at “company” and get\_item\_tax\_valid\_from(tax) ≤ validation\_date and is\_within\_valid\_range(ctx, tax)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not disabled → tax\_company equals ctx at “company” → get\_item\_tax\_valid\_from(tax) ≤ validation\_date → is\_within\_valid\_range(ctx, tax).
    - Evaluate applicable\_taxes.append(tax).
- Return applicable\_taxes.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item Tax Template”, tax.item\_tax\_template, list(“disabled”, “company”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L917)

<a id="op-ecdcba97cf2627"></a>
### Get latest item taxes

`operation_enterprise_binding_enterprise_stock_get_item_details_get_latest_item_taxes`

**Inputs** taxes.

**Declared result** list.

**Explicit results** latest\_taxes.

**Local steps**

- Set latest\_priority from mapping().
- Set latest\_taxes from list().
- For each tax in sorted(taxes, key = get\_item\_tax\_priority, reverse = true).
  - Set priority from get\_item\_tax\_priority(tax).
  - Set key from tuple(tax.get(“parenttype”), tax.get(“parent”), cstr(tax.tax\_category)).
  - If latest\_priority.setdefault(key, priority) equals priority.
    - Evaluate latest\_taxes.append(tax).
- Return latest\_taxes.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1433) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L930)

<a id="op-233c58e9aefd84"></a>
### Get item tax priority

`operation_enterprise_binding_enterprise_stock_get_item_details_get_item_tax_priority`

**Inputs** tax.

**Declared result** tuple.

**Explicit results** tuple(get\_item\_tax\_valid\_from(tax), flt(tax.maximum\_net\_rate) &gt; 0).

**Local steps**

- Return tuple(get\_item\_tax\_valid\_from(tax), flt(tax.maximum\_net\_rate) &gt; 0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L928)

<a id="op-d38a2330d3609e"></a>
### Get item tax valid from

`operation_enterprise_binding_enterprise_stock_get_item_details_get_item_tax_valid_from`

**Inputs** tax.

**Declared result** datetime.date.

**Explicit results** getdate(tax.valid\_from) when tax.valid\_from, otherwise datetime.date.min.

**Local steps**

- Return getdate(tax.valid\_from) when tax.valid\_from, otherwise datetime.date.min.
  - Value choice on tax.valid\_from — true gives getdate(tax.valid\_from), false gives datetime.date.min.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L929)

<a id="op-9e7d9c4e8a9deb"></a>
### Is within valid range

`operation_enterprise_stock_get_item_details_business_behavior_is_within_valid_range`

**Inputs** ctx, tax.

**Wrappers, in declaration order** Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If not flt(tax.maximum\_net\_rate).
  - Return true.
- Otherwise.
  - If flt(tax.minimum\_net\_rate) ≤ flt(ctx.get(“base\_net\_rate”)) ≤ flt(tax.maximum\_net\_rate).
    - Compare adjacent operands in order, stopping at the first false comparison in flt(tax.minimum\_net\_rate) ≤ flt(ctx.get(“base\_net\_rate”)) ≤ flt(tax.maximum\_net\_rate).
    - Return true.
- Return false.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0881.json#L1107) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L756)

<a id="op-a7b975f2e0fa51"></a>
### Get item tax map

`operation_enterprise_stock_get_item_details_business_behavior_get_item_tax_map`

**Inputs** doc (named only), tax\_template (named only, default no value), as\_json (named only, default true).

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_item\_tax\_map(doc = doc, tax\_template = tax\_template, as\_json = as\_json).

**Local steps**

- If tax\_template.
  - Evaluate Enterprise.require\_permission(“Item Tax Template”, tax\_template, “select”).
- Return \_get\_item\_tax\_map(doc = doc, tax\_template = tax\_template, as\_json = as\_json).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L736)

<a id="op-a4e54593a2aeeb"></a>
### Get item tax map

`operation_enterprise_binding_enterprise_stock_get_item_details_get_item_tax_map`

**Inputs** doc (named only), tax\_template (named only, default no value), as\_json (named only, default true).

**Record and data access** resolve a document from “Item Tax Template” via get\_cached\_doc · read “Account” via get\_cached\_value.

**Explicit results** json.dumps(item\_tax\_map) when as\_json, otherwise item\_tax\_map.

**Local steps**

- Set doc from parse\_json(doc).
- Set item\_tax\_map from mapping().
- For each t in generator of t for t drawn from (doc.get(“taxes”) or list()) where not t.get(“set\_by\_item\_tax\_template”).
  - Draw t from (doc.get(“taxes”) or list()), keep a combination only if (not t.get(“set\_by\_item\_tax\_template”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“taxes”) → list().
  - Set item\_tax\_map at t.get(“account\_head”) from t.get(“rate”).
- If tax\_template.
  - Set template from Platform.get\_cached\_doc(“Item Tax Template”, tax\_template).
  - For each d in template.taxes.
    - If Platform.get\_cached\_value(“Account”, d.tax\_type, “company”) equals doc.get(“company”).
      - If d.get(“not\_applicable”).
        - Set item\_tax\_map at d.tax\_type from NOT\_APPLICABLE\_TAX.
      - Otherwise.
        - Set item\_tax\_map at d.tax\_type from d.tax\_rate.
- Return json.dumps(item\_tax\_map) when as\_json, otherwise item\_tax\_map.
  - Value choice on as\_json — true gives json.dumps(item\_tax\_map), false gives item\_tax\_map.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item Tax Template”, tax\_template), Platform.get\_cached\_value(“Account”, d.tax\_type, “company”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L927)

<a id="op-f6e34aa225120c"></a>
### Calculate service end date

`operation_enterprise_stock_get_item_details_business_behavior_calculate_service_end_date`

**Inputs** ctx, item = no value.

**Wrappers, in declaration order** Platform.whitelist(), Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit results** deferred\_detail.

**Explicit failure paths** validation helper — translated “Invalid Item Code”.

**Local steps**

- Evaluate \_preprocess\_ctx(ctx).
- If not isinstance(ctx.item\_code, str).
  - Call the validation error handler Platform.throw(translated “Invalid Item Code”).
- If not item.
  - Set item from Platform.get\_cached\_doc(“Item”, ctx.item\_code).
- Set doctype from (ctx.parenttype or ctx.doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.parenttype → ctx.doctype.
- If doctype equals “Sales Invoice”.
  - Set enable\_deferred from “enable\_deferred\_revenue”.
  - Set no\_of\_months from “no\_of\_months”.
  - Set account from “deferred\_revenue\_account”.
- Otherwise.
  - Set enable\_deferred from “enable\_deferred\_expense”.
  - Set no\_of\_months from “no\_of\_months\_exp”.
  - Set account from “deferred\_expense\_account”.
- Set service\_start\_date from ctx.service\_start\_date when ctx.service\_start\_date, otherwise ctx.transaction\_date.
  - Value choice on ctx.service\_start\_date — true gives ctx.service\_start\_date, false gives ctx.transaction\_date.
- Set service\_end\_date from add\_months(service\_start\_date, item.get(no\_of\_months)).
- Set deferred\_detail from mapping(“service\_start\_date” → service\_start\_date, “service\_end\_date” → service\_end\_date).
- Set deferred\_detail at enable\_deferred from item.get(enable\_deferred).
- Set deferred\_detail at account from get\_default\_deferred\_account(ctx, item, fieldname = account).
- Return deferred\_detail.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, ctx.item\_code).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1168) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L708)

<a id="op-23a5be99225e44"></a>
### Get default income account

`operation_enterprise_stock_get_item_details_business_behavior_get_default_income_account`

**Inputs** ctx, item, item\_group, brand.

**Explicit results** (item.get(“income\_account”) or item\_group.get(“income\_account”) or brand.get(“income\_account”) or ctx.income\_account).

**Local steps**

- Return (item.get(“income\_account”) or item\_group.get(“income\_account”) or brand.get(“income\_account”) or ctx.income\_account).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“income\_account”) → item\_group.get(“income\_account”) → brand.get(“income\_account”) → ctx.income\_account.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1187) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L727)

<a id="op-56d36e878e8a9d"></a>
### Get default inventory account

`operation_enterprise_stock_get_item_details_business_behavior_get_default_inventory_account`

**Inputs** ctx, item, item\_group, brand.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value · (ctx.inventory\_account or item.get(“default\_inventory\_account”) or item\_group.get(“default\_inventory\_account”) or brand.get(“default\_inventory\_account”)).

**Local steps**

- If not Platform.get\_cached\_value(“Company”, ctx.company, “enable\_item\_wise\_inventory\_account”).
  - Return no value.
- Return (ctx.inventory\_account or item.get(“default\_inventory\_account”) or item\_group.get(“default\_inventory\_account”) or brand.get(“default\_inventory\_account”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.inventory\_account → item.get(“default\_inventory\_account”) → item\_group.get(“default\_inventory\_account”) → brand.get(“default\_inventory\_account”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, ctx.company, “enable\_item\_wise\_inventory\_account”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1188) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L728)

<a id="op-13bab46a5119e7"></a>
### Get default expense account

`operation_enterprise_stock_get_item_details_business_behavior_get_default_expense_account`

**Inputs** ctx, item, item\_group, brand.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** expense\_account · (item.get(“expense\_account”) or item\_group.get(“expense\_account”) or brand.get(“expense\_account”) or ctx.expense\_account).

**Local steps**

- If ctx.get(“doctype”) belongs to list(“Sales Invoice”, “Delivery Note”).
  - Set expense\_account from (item.get(“default\_cogs\_account”) or item\_group.get(“default\_cogs\_account”) or brand.get(“default\_cogs\_account”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“default\_cogs\_account”) → item\_group.get(“default\_cogs\_account”) → brand.get(“default\_cogs\_account”).
  - If not expense\_account.
    - Set expense\_account from Platform.get\_cached\_value(“Company”, ctx.company, “default\_expense\_account”).
  - If expense\_account.
    - Return expense\_account.
- Return (item.get(“expense\_account”) or item\_group.get(“expense\_account”) or brand.get(“expense\_account”) or ctx.expense\_account).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“expense\_account”) → item\_group.get(“expense\_account”) → brand.get(“expense\_account”) → ctx.expense\_account.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, ctx.company, “default\_expense\_account”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1186) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L726)

<a id="op-030a82e15d3dbb"></a>
### Get provisional account

`operation_enterprise_stock_get_item_details_business_behavior_get_provisional_account`

**Inputs** ctx, item, item\_group, brand.

**Explicit results** (item.get(“default\_provisional\_account”) or item\_group.get(“default\_provisional\_account”) or brand.get(“default\_provisional\_account”) or ctx.default\_provisional\_account).

**Local steps**

- Return (item.get(“default\_provisional\_account”) or item\_group.get(“default\_provisional\_account”) or brand.get(“default\_provisional\_account”) or ctx.default\_provisional\_account).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“default\_provisional\_account”) → item\_group.get(“default\_provisional\_account”) → brand.get(“default\_provisional\_account”) → ctx.default\_provisional\_account.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L748)

<a id="op-e466730d28b0c6"></a>
### Get default discount account

`operation_enterprise_stock_get_item_details_business_behavior_get_default_discount_account`

**Inputs** ctx, item, item\_group, brand.

**Explicit results** (item.get(“default\_discount\_account”) or item\_group.get(“default\_discount\_account”) or brand.get(“default\_discount\_account”) or ctx.discount\_account).

**Local steps**

- Return (item.get(“default\_discount\_account”) or item\_group.get(“default\_discount\_account”) or brand.get(“default\_discount\_account”) or ctx.discount\_account).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“default\_discount\_account”) → item\_group.get(“default\_discount\_account”) → brand.get(“default\_discount\_account”) → ctx.discount\_account.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1185) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L725)
