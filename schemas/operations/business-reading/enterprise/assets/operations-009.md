# Asset management · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset capitalization

[Record definition](../../../../data/record-types/asset_capitalization.json)

<a id="op-713a96788c327a"></a>
### Asset Capitalization.restore consumed asset items

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_restore_consumed_asset_items`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_doc.

**State and service calls** call db\_set on asset.

**Local steps**

- For each item in self.asset\_items.
  - Set asset from Platform.get\_doc(“Asset”, item.asset).
  - Evaluate self.set\_consumed\_asset\_status(asset).
  - If asset.calculate\_depreciation.
    - Evaluate reverse\_depreciation\_entry\_made\_on\_disposal(asset).
    - Set notes from translated “This schedule was created when Asset {0} was restored on Asset Capitalization {1}'s cancellation.”.format(get\_link\_to\_form(asset.doctype, asset.name), get\_link\_to\_form(self.doctype, self.name)).
    - Evaluate reset\_depreciation\_schedule(asset, notes).
  - Evaluate asset.db\_set(“disposal\_date”, no value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set consumed asset status](operations-009.md#op-f95c46893f7585).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0318.json#L4607) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L335)

<a id="op-f95c46893f7585"></a>
### Asset Capitalization.set consumed asset status

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_set_consumed_asset_status`

**Inputs** self, asset.

**Local steps**

- If self.docstatus equals 1.
  - Evaluate asset.set\_status(“Capitalized”).
  - Evaluate add\_asset\_activity(asset.name, translated “Asset capitalized after Asset Capitalization {0} was submitted”.format(get\_link\_to\_form(“Asset Capitalization”, self.name))).
- Otherwise.
  - Evaluate asset.set\_status().
  - Evaluate add\_asset\_activity(asset.name, translated “Asset restored after Asset Capitalization {0} was cancelled”.format(get\_link\_to\_form(“Asset Capitalization”, self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0318.json#L4918) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1438) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L337)

<a id="op-a30dcff43bdbe4"></a>
### Check capitalization access

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_check_capitalization_access`

**Inputs** company = no value.

**Local steps**

- Evaluate Platform.has\_permission(“Asset Capitalization”, throw = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset Capitalization”, throw = true).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L700) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1338)

<a id="op-f2c83fe68a8879"></a>
### Get target item details

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_get_target_item_details`

**Inputs** item\_code = no value, company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Platform.\_dict.

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit results** out.

**Local steps**

- Evaluate check\_capitalization\_access(company).
- Set out from Platform.\_dict().
- Set item from Platform.\_dict().
- If item\_code.
  - Set item from Platform.get\_cached\_doc(“Item”, item\_code).
- Set out.target\_item\_name from item.item\_name.
- Set item\_defaults from get\_item\_defaults(item.name, company).
- Set item\_group\_defaults from get\_item\_group\_defaults(item.name, company).
- Set brand\_defaults from get\_brand\_defaults(item.name, company).
- Set out.cost\_center from get\_default\_cost\_center(ItemDetailsCtx(mapping(“item\_code” → item.name, “company” → company)), item\_defaults, item\_group\_defaults, brand\_defaults).
- Return out.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, item\_code).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L357)

<a id="op-b8f5fda61efac7"></a>
### Get target asset details

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_get_target_asset_details`

**Inputs** asset = no value, company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Platform.\_dict.

**Record and data access** read “Asset” via get\_value.

**Explicit results** out.

**Local steps**

- Evaluate check\_capitalization\_access(company).
- Set out from Platform.\_dict().
- Set asset\_details from Platform.\_dict().
- If asset.
  - Evaluate Enterprise.require\_permission(“Asset”, asset, “select”).
  - Set asset\_details from Platform.db.get\_value(“Asset”, asset, list(“asset\_name”, “item\_code”, “company”), as\_dict = 1).
  - Evaluate check\_capitalization\_access(asset\_details.company).
  - Set out.target\_item\_code from asset\_details.item\_code.
- Set out.asset\_name from asset\_details.asset\_name.
- If asset\_details.item\_code.
  - Set out.target\_fixed\_asset\_account from get\_asset\_category\_account(“fixed\_asset\_account”, item = asset\_details.item\_code, company = company).
- Otherwise.
  - Set out.target\_fixed\_asset\_account from no value.
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1457) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L356)

<a id="op-6d247967656f14"></a>
### Get consumed stock item details

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_get_consumed_stock_item_details`

**Inputs** ctx.

**Wrappers, in declaration order** Platform.whitelist(), Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit results** out.

**Local steps**

- Evaluate Platform.has\_permission(“Stock Ledger Entry”, throw = true).
- If ctx.item\_code.
  - Evaluate Platform.get\_cached\_doc(“Item”, ctx.item\_code).check\_permission().
- Set out from \_get\_consumed\_stock\_item\_details(ctx).
- If out.warehouse.
  - Evaluate Platform.has\_permission(“Warehouse”, doc = out.warehouse, throw = true).
- Return out.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Stock Ledger Entry”, throw = true), Platform.has\_permission(“Warehouse”, doc = out.warehouse, throw = true) · configured or stored value from Platform.get\_cached\_doc(“Item”, ctx.item\_code).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L353)

<a id="op-d8c0fd00381d39"></a>
### Get consumed stock item details

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_get_consumed_stock_item_details`

**Inputs** ctx.

**Wrappers, in declaration order** Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Declared result** Platform.\_dict.

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit results** out.

**Local steps**

- Set out from Platform.\_dict().
- Set item from Platform.\_dict().
- If ctx.item\_code.
  - Set item from Platform.get\_cached\_doc(“Item”, ctx.item\_code).
- Set out.item\_name from item.item\_name.
- Set out.batch\_no from no value.
- Set out.serial\_no from empty text.
- Set out.stock\_qty from (flt(ctx.stock\_qty) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(ctx.stock\_qty) → 1.
- Set out.stock\_uom from item.stock\_uom.
- Set out.warehouse from get\_item\_warehouse\_(ctx, item, overwrite\_warehouse = true) when item, otherwise no value.
  - Value choice on item — true gives get\_item\_warehouse\_(ctx, item, overwrite\_warehouse = true), false gives no value.
- Set item\_defaults from get\_item\_defaults(item.name, ctx.company).
- Set item\_group\_defaults from get\_item\_group\_defaults(item.name, ctx.company).
- Set brand\_defaults from get\_brand\_defaults(item.name, ctx.company).
- Set out.cost\_center from get\_default\_cost\_center(ctx, item\_defaults, item\_group\_defaults, brand\_defaults).
- If (ctx.item\_code and out.warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.item\_code → out.warehouse.
  - Set incoming\_rate\_args from Platform.\_dict(mapping(“item\_code” → ctx.item\_code, “warehouse” → out.warehouse, “posting\_date” → ctx.posting\_date, “posting\_time” → ctx.posting\_time, …)).
  - Evaluate out.update(\_get\_warehouse\_details(incoming\_rate\_args)).
- Otherwise.
  - Set out.valuation\_rate from 0.
  - Set out.actual\_qty from 0.
- Return out.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, ctx.item\_code).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L701) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1339)

<a id="op-368b534a922456"></a>
### Get warehouse details

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_get_warehouse_details`

**Inputs** args.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_warehouse\_details(args).

**Local steps**

- If isinstance(args, str).
  - Set args from json.loads(args).
- Set args from Platform.\_dict(args).
- If (args.warehouse and args.item\_code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.warehouse → args.item\_code.
  - Evaluate Platform.has\_permission(“Item”, doc = args.item\_code, throw = true).
  - Evaluate Platform.has\_permission(“Warehouse”, doc = args.warehouse, throw = true).
  - Evaluate Platform.has\_permission(“Stock Ledger Entry”, throw = true).
- Return \_get\_warehouse\_details(args).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, doc = args.item\_code, throw = true), Platform.has\_permission(“Warehouse”, doc = args.warehouse, throw = true) and 1 further calls.

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L358)

<a id="op-0813c0005d1503"></a>
### Get warehouse details

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_get_warehouse_details`

**Inputs** args.

**Declared result** dict.

**Explicit results** mapping() · mapping(“actual\_qty” → (get\_previous\_sle(args).get(“qty\_after\_transaction”) or 0), “valuation\_rate” → \_get\_incoming\_rate(args, raise\_error\_if\_no\_rate = false)).

**Local steps**

- Set args from Platform.\_dict(args).
- If not (args.warehouse and args.item\_code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.warehouse → args.item\_code.
  - Return mapping().
- Return mapping(“actual\_qty” → (get\_previous\_sle(args).get(“qty\_after\_transaction”) or 0), “valuation\_rate” → \_get\_incoming\_rate(args, raise\_error\_if\_no\_rate = false)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_previous\_sle(args).get(“qty\_after\_transaction”) → 0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L702) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1340)

<a id="op-7135eeb37febc8"></a>
### Get consumed asset details

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_get_consumed_asset_details`

**Inputs** ctx.

**Wrappers, in declaration order** Platform.whitelist(), Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Record and data access** read “Asset” via get\_value · resolve a document from “Item” via get\_cached\_doc.

**Explicit results** out.

**Local steps**

- Evaluate check\_capitalization\_access(ctx.get(“company”)).
- If ctx.get(“asset”).
  - Set ptype from “select” when Platform.only\_has\_select\_perm(“Asset”), otherwise “read”.
    - Value choice on Platform.only\_has\_select\_perm(“Asset”) — true gives “select”, false gives “read”.
  - Evaluate Platform.has\_permission(“Asset”, ptype, doc = ctx.get(“asset”), throw = true).
- Set out from Platform.\_dict().
- Set asset\_details from Platform.\_dict().
- If ctx.asset.
  - Evaluate Enterprise.require\_permission(“Asset”, ctx.asset, “select”).
  - Set asset\_details from Platform.db.get\_value(“Asset”, ctx.asset, list(“asset\_name”, “item\_code”, “item\_name”, “company”), as\_dict = 1).
  - Evaluate check\_capitalization\_access(asset\_details.company).
- Set out.item\_code from asset\_details.item\_code.
- Set out.asset\_name from asset\_details.asset\_name.
- Set out.item\_name from asset\_details.item\_name.
- If ctx.asset.
  - Set out.current\_asset\_value from flt(\_get\_asset\_value\_after\_depreciation(ctx.asset, finance\_book = ctx.finance\_book)).
  - Set out.asset\_value from calculate\_value\_after\_depreciation\_on\_disposal\_date(ctx.asset, ctx.posting\_date, finance\_book = ctx.finance\_book).
- Otherwise.
  - Set out.current\_asset\_value from 0.
  - Set out.asset\_value from 0.
- If asset\_details.item\_code.
  - Set out.fixed\_asset\_account from get\_asset\_category\_account(“fixed\_asset\_account”, item = asset\_details.item\_code, company = ctx.company).
- Otherwise.
  - Set out.fixed\_asset\_account from no value.
- If asset\_details.item\_code.
  - Set item from Platform.get\_cached\_doc(“Item”, asset\_details.item\_code).
  - Set item\_defaults from get\_item\_defaults(item.name, ctx.company).
  - Set item\_group\_defaults from get\_item\_group\_defaults(item.name, ctx.company).
  - Set brand\_defaults from get\_brand\_defaults(item.name, ctx.company).
  - Set out.cost\_center from get\_default\_cost\_center(ctx, item\_defaults, item\_group\_defaults, brand\_defaults).
- Return out.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset”, ptype, doc = ctx.get(“asset”), throw = true) · configured or stored value from Platform.get\_cached\_doc(“Item”, asset\_details.item\_code).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L352)

<a id="op-922d44cc29d64f"></a>
### Get service item details

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_get_service_item_details`

**Inputs** ctx.

**Wrappers, in declaration order** Platform.whitelist(), Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit results** out.

**Local steps**

- Evaluate check\_capitalization\_access(ctx.get(“company”)).
- Set out from Platform.\_dict().
- Set item from Platform.\_dict().
- If ctx.item\_code.
  - Set item from Platform.get\_cached\_doc(“Item”, ctx.item\_code).
- Set out.item\_name from item.item\_name.
- Set out.qty from (flt(ctx.qty) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(ctx.qty) → 1.
- Set out.uom from (item.purchase\_uom or item.stock\_uom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.purchase\_uom → item.stock\_uom.
- Set item\_defaults from get\_item\_defaults(item.name, ctx.company).
- Set item\_group\_defaults from get\_item\_group\_defaults(item.name, ctx.company).
- Set brand\_defaults from get\_brand\_defaults(item.name, ctx.company).
- Set out.expense\_account from get\_default\_expense\_account(ctx, item\_defaults, item\_group\_defaults, brand\_defaults).
- Set out.cost\_center from get\_default\_cost\_center(ctx, item\_defaults, item\_group\_defaults, brand\_defaults).
- Return out.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, ctx.item\_code).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L355)

<a id="op-316f238a7f1bed"></a>
### Get items tagged to wip composite asset

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_get_items_tagged_to_work_in_progress_composite_asset`

**Inputs** params.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Asset” via get\_value · read “Purchase Receipt Item” via get\_all.

**Explicit results** tuple(stock\_items, asset\_items).

**Local steps**

- If isinstance(params, str).
  - Set params from json.loads(params).
- Set target\_asset from cstr(params.get(“target\_asset”)).
- Evaluate Enterprise.require\_permission(“Asset”, target\_asset, “select”).
- Evaluate check\_capitalization\_access(Platform.db.get\_value(“Asset”, target\_asset, “company”)).
- Set fields from list(“item\_code”, “item\_name”, “batch\_no”, “serial\_no”, …).
- Set pr\_items from Platform.get\_all(“Purchase Receipt Item”, filters = mapping(“wip\_composite\_asset” → target\_asset, “docstatus” → 1), fields = fields).
- For each purchase\_receipt in set of d.purchase\_receipt for d drawn from pr\_items.
  - Draw d from pr\_items.
  - Evaluate Enterprise.require\_permission(“Purchase Receipt”, purchase\_receipt).
- Set stock\_items from list().
- Set asset\_items from list().
- For each d in pr\_items.
  - If not d.is\_fixed\_asset.
    - Set stock\_item from process\_stock\_item(d).
    - If stock\_item.
      - Evaluate stock\_items.append(stock\_item).
  - Otherwise.
    - Set asset\_item from process\_fixed\_asset(d).
    - If asset\_item.
      - Evaluate asset\_items.append(asset\_item).
- Return tuple(stock\_items, asset\_items).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L354)

<a id="op-1e28f2d98e14f1"></a>
### Process stock item

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_process_stock_item`

**Inputs** d.

**Record and data access** read “Asset Capitalization Stock Item” via exists.

**Explicit results** no value · stock\_item\_data.

**Local steps**

- Set stock\_capitalized from Platform.db.exists(“Asset Capitalization Stock Item”, mapping(“purchase\_receipt\_item” → d.purchase\_receipt\_item, “parentfield” → “stock\_items”, “parenttype” → “Asset Capitalization”, “docstatus” → 1)).
- If stock\_capitalized.
  - Return no value.
- Set stock\_item\_data from Platform.\_dict(d).
- Set stock\_item\_data.purchase\_receipt\_item from d.purchase\_receipt\_item.
- Return stock\_item\_data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0319.json#L2320) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1461) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L360)

<a id="op-a904d861ea3659"></a>
### Process fixed asset

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_process_fixed_asset`

**Inputs** d.

**Record and data access** read “Asset” via get\_value.

**Explicit results** Platform.\_dict(d) · no value.

**Local steps**

- Set asset\_details from Platform.db.get\_value(“Asset”, mapping(“item\_code” → d.item\_code, “purchase\_receipt” → d.purchase\_receipt, “status” → tuple(“not in”, list(“Draft”, “Scrapped”, “Sold”, “Capitalized”))), list(“name as asset ….
- If asset\_details.
  - Evaluate asset\_details.update(d).
  - Evaluate asset\_details.update(get\_consumed\_asset\_details(asset\_details)).
  - Evaluate d.update(asset\_details).
  - Return Platform.\_dict(d).
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0319.json#L2545) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L359)

## Record · Asset category

[Record definition](../../../../data/record-types/asset_category.json)

<a id="op-62575934b99485"></a>
### Asset Category.validate

`operation_enterprise_assets_record_definitions_asset_category_business_behavior_asset_category_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_non\_depreciable\_category().
- Evaluate self.validate\_finance\_books().
- Evaluate self.validate\_account\_types().
- Evaluate self.validate\_account\_currency().
- Evaluate self.valide\_cwip\_account().
- Evaluate self.validate\_account\_change\_for\_existing\_assets().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate non depreciable category](operations-009.md#op-cd60d07fb49e7c), [validate finance books](operations-009.md#op-25347c32d5301d), [validate account types](operations-009.md#op-e403f4a08cf04b), [validate account currency](operations-009.md#op-480bc8a1647f07), [valide cwip account](operations-009.md#op-20f561354ac5db), [validate account change for existing assets](operations-009.md#op-03c3a136f127e9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L374)

<a id="op-cd60d07fb49e7c"></a>
### Asset Category.validate non depreciable category

`operation_enterprise_binding_enterprise_assets_doctype_asset_category_asset_category_assetcategory_validate_non_depreciable_category`

**Inputs** self.

**Record and data access** read “Asset” via exists.

**Explicit failure paths** validation helper — translated “Cannot mark the category as Non Depreciable since it has assets being depreciated”.

**Local steps**

- If (self.non\_depreciable\_category and Platform.db.exists(“Asset”, mapping(“asset\_category” → self.name, “calculate\_depreciation” → 1, “docstatus” → 1, “status” → list(“in”, DEPRECIATING\_ASSET\_STATUSES)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.non\_depreciable\_category → Platform.db.exists(“Asset”, mapping(“asset\_category” → self.name, “calculate\_depreciation” → 1, “docstatus” → 1, “status” → list(“in”, DEPRECIATING\_ASSET\_STATUSES))).
  - Call the validation error handler Platform.throw(translated “Cannot mark the category as Non Depreciable since it has assets being depreciated”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L706) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1344)

<a id="op-25347c32d5301d"></a>
### Asset Category.validate finance books

`operation_enterprise_assets_record_definitions_asset_category_business_behavior_asset_category_validate_finance_books`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Row {0}: {1} must be greater than 0”.format(d.idx, field) · validation helper — translated “Row {0}: Salvage Value Percentage must be between 0 and 100”.format(d.idx) · validation helper — translated “Row {0}: Rate of Depreciation cannot be negative”.format(d.idx).

**Local steps**

- For each d in self.finance\_books.
  - For each field in tuple(“Total Number of Depreciations”, “Frequency of Depreciation”).
    - If cint(d.get(Platform.scrub(field))) &lt; 1.
      - Call the validation error handler Platform.throw(translated “Row {0}: {1} must be greater than 0”.format(d.idx, field), Platform.MandatoryError).
  - If not 0 ≤ flt(d.salvage\_value\_percentage) ≤ 100.
    - Compare adjacent operands in order, stopping at the first false comparison in 0 ≤ flt(d.salvage\_value\_percentage) ≤ 100.
    - Call the validation error handler Platform.throw(translated “Row {0}: Salvage Value Percentage must be between 0 and 100”.format(d.idx)).
  - If flt(d.rate\_of\_depreciation) &lt; 0.
    - Call the validation error handler Platform.throw(translated “Row {0}: Rate of Depreciation cannot be negative”.format(d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L377)

<a id="op-480bc8a1647f07"></a>
### Asset Category.validate account currency

`operation_enterprise_assets_record_definitions_asset_category_business_behavior_asset_category_validate_account_currency`

**Inputs** self.

**Record and data access** read “Company” via get\_value · read “Account” via get\_value.

**Explicit failure paths** validation helper — translated “Row #{}: Currency of {} - {} doesn't matches company currency.”.format(d.idx, Platform.bold(Platform.unscrub(d.type)), Platform.bold(d.account)).

**Local steps**

- Set invalid\_accounts from list().
- For each d in self.accounts.
  - Set company\_currency from Platform.get\_value(“Company”, d.get(“company\_name”), “default\_currency”).
  - For each type\_of\_account in ACCOUNT\_FIELDS.
    - If d.get(type\_of\_account).
      - Set account\_currency from Platform.get\_value(“Account”, d.get(type\_of\_account), “account\_currency”).
      - If account\_currency differs from company\_currency.
        - Evaluate invalid\_accounts.append(Platform.\_dict(mapping(“type” → type\_of\_account, “idx” → d.idx, “account” → d.get(type\_of\_account)))).
- For each d in invalid\_accounts.
  - Call the validation error handler Platform.throw(translated “Row #{}: Currency of {} - {} doesn't matches company currency.”.format(d.idx, Platform.bold(Platform.unscrub(d.type)), Platform.bold(d.account)), title = translated “Invalid Account”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L375)

<a id="op-e403f4a08cf04b"></a>
### Asset Category.validate account types

`operation_enterprise_assets_record_definitions_asset_category_business_behavior_asset_category_validate_account_types`

**Inputs** self.

**Record and data access** read “Account” via get\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: {1} of {2} should be {3}. Please update the {1} or select a different account.”.format(d.idx, Platform.unscrub(key\_to\_match), Platform.bold(selected\_account), Platform.bold(“ or ”.joi ….

**Local steps**

- Set account\_type\_map from mapping(“fixed\_asset\_account” → mapping(“account\_type” → list(“Fixed Asset”)), “accumulated\_depreciation\_account” → mapping(“account\_type” → list(“Accumulated Depreciation”)), “depreciation\_expense\_account ….
- For each d in self.accounts.
  - For each fieldname in account\_type\_map.keys().
    - If d.get(fieldname).
      - Set selected\_account from d.get(fieldname).
      - Set key\_to\_match from next(iter(account\_type\_map.get(fieldname))).
      - Set selected\_key\_type from Platform.db.get\_value(“Account”, selected\_account, key\_to\_match).
      - Set expected\_key\_types from account\_type\_map at fieldname at key\_to\_match.
      - If selected\_key\_type does not belong to expected\_key\_types.
        - Call the validation error handler Platform.throw(translated “Row #{0}: {1} of {2} should be {3}. Please update the {1} or select a different account.”.format(d.idx, Platform.unscrub(key\_to\_match), Platform.bold(selected\_account), Platform. ….
      - Evaluate self.validate\_account\_details(d, selected\_account).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate account details](operations-009.md#op-b1b804c80cba52).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L376)

<a id="op-b1b804c80cba52"></a>
### Asset Category.validate account details

`operation_enterprise_binding_enterprise_assets_doctype_asset_category_asset_category_assetcategory_validate_account_details`

**Inputs** self, row, account.

**Record and data access** read “Account” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — error.format(row.idx, Platform.bold(account), Platform.bold(row.company\_name)).

**Local steps**

- Set tuple(company, is\_group, disabled) from Platform.db.get\_value(“Account”, account, list(“company”, “is\_group”, “disabled”)).
- If company differs from row.company\_name.
  - Set error from translated “Row #{0}: Account {1} does not belong to company {2}.”.
- Otherwise.
  - If is\_group.
    - Set error from translated “Row #{0}: Account {1} is a group account.”.
  - Otherwise.
    - If disabled.
      - Set error from translated “Row #{0}: Account {1} is disabled.”.
    - Otherwise.
      - Return no value.
- Call the validation error handler Platform.throw(error.format(row.idx, Platform.bold(account), Platform.bold(row.company\_name)), title = translated “Invalid Account”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L705) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1343)

<a id="op-20f561354ac5db"></a>
### Asset Category.valide cwip account

`operation_enterprise_binding_enterprise_assets_doctype_asset_category_asset_category_assetcategory_valide_cwip_account`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If self.enable\_cwip\_accounting.
  - Set missing\_cwip\_accounts\_for\_company from list().
  - For each d in self.accounts.
    - If (not d.capital\_work\_in\_progress\_account and not Platform.db.get\_value(“Company”, d.company\_name, “capital\_work\_in\_progress\_account”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.capital\_work\_in\_progress\_account → not Platform.db.get\_value(“Company”, d.company\_name, “capital\_work\_in\_progress\_account”).
      - Evaluate missing\_cwip\_accounts\_for\_company.append(get\_link\_to\_form(“Company”, d.company\_name)).
  - If missing\_cwip\_accounts\_for\_company.
    - Set msg from (translated “To enable Capital Work in Progress Accounting,” + one space).
    - Update msg using + translated “you must select Capital Work in Progress Account in accounts table”.
    - Update msg using + text in the contract.
    - Update msg using + translated “You can also set default CWIP account in Company {}”.format(“, ”.join(missing\_cwip\_accounts\_for\_company)).
    - Call the validation error handler Platform.throw(msg, title = translated “Missing Account”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L707) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1345)

<a id="op-03c3a136f127e9"></a>
### Asset Category.validate account change for existing assets

`operation_enterprise_binding_enterprise_assets_doctype_asset_category_asset_category_assetcategory_validate_account_change_for_existing_assets`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot change {0} for company {1} since it has active assets in this category”.format(“, ”.join(generator of Platform.bold(translated nested operand in the contract.unscrub(fieldname)) for fiel ….

**Local steps**

- Set previous\_doc from self.get\_doc\_before\_save().
- If not previous\_doc.
  - Return no value.
- Set current\_rows from mapping of row.company\_name → row for row drawn from self.accounts.
  - Draw row from self.accounts.
- For each previous\_row in previous\_doc.accounts.
  - Set current\_row from (current\_rows.get(previous\_row.company\_name) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in current\_rows.get(previous\_row.company\_name) → mapping().
  - Set changed\_fields from list of fieldname for fieldname drawn from ACCOUNT\_FIELDS where (previous\_row.get(fieldname) and current\_row.get(fieldname) differs from previous\_row.get(fieldname)).
    - Draw fieldname from ACCOUNT\_FIELDS, keep a combination only if ((previous\_row.get(fieldname) and current\_row.get(fieldname) differs from previous\_row.get(fieldname))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_row.get(fieldname) → current\_row.get(fieldname) differs from previous\_row.get(fieldname).
  - If (changed\_fields and self.has\_active\_assets(previous\_row.company\_name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in changed\_fields → self.has\_active\_assets(previous\_row.company\_name).
    - Call the validation error handler Platform.throw(translated “Cannot change {0} for company {1} since it has active assets in this category”.format(“, ”.join(generator of Platform.bold(translated nested operand in the contract(nested operan ….
      - Draw fieldname from changed\_fields.

If control reaches the end, it returns no value.

**Methods declared on this owner** [has active assets](operations-009.md#op-4314eca05b8779).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L704) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1342)

<a id="op-4314eca05b8779"></a>
### Asset Category.has active assets

`operation_enterprise_binding_enterprise_assets_doctype_asset_category_asset_category_assetcategory_has_active_assets`

**Inputs** self, company.

**Declared result** bool.

**Record and data access** read “Asset” via get\_all.

**Explicit results** bool(Platform.get\_all(“Asset”, filters = mapping(“asset\_category” → self.name, “company” → company, “docstatus” → list(“&lt;”, 2), “status” → list(“not in”, DISPOSED\_ASSET\_STATUSES)), or\_filters = mapping(“docstat …).

**Local steps**

- Return bool(Platform.get\_all(“Asset”, filters = mapping(“asset\_category” → self.name, “company” → company, “docstatus” → list(“&lt;”, 2), “status” → list(“not in”, DISPOSED\_ASSET\_STATUSES)), or\_filters = mapping(“docstat …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L703) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1341)

<a id="op-4f4c6d1be16ed3"></a>
### Get asset category account

`operation_enterprise_assets_record_definitions_asset_category_business_behavior_get_asset_category_account`

**Inputs** fieldname, item = no value, asset = no value, account = no value, asset\_category = no value, company = no value.

**Record and data access** read “Item” via get\_value · read “Account” via get\_value · read “Asset” via get\_value · read “Asset Category Account” via get\_value.

**Explicit results** account.

**Local steps**

- If (item and Platform.db.get\_value(“Item”, item, “is\_fixed\_asset”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → Platform.db.get\_value(“Item”, item, “is\_fixed\_asset”).
  - Set asset\_category from Platform.db.get\_value(“Item”, item, list(“asset\_category”)).
- Otherwise.
  - If (not asset\_category or not company).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not asset\_category → not company.
    - If account.
      - If Platform.db.get\_value(“Account”, account, “account\_type”) differs from “Fixed Asset”.
        - Set account from no value.
    - If not account.
      - Set asset\_details from Platform.db.get\_value(“Asset”, asset, list(“asset\_category”, “company”)).
      - Set tuple(asset\_category, company) from (asset\_details or list(no value, no value)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in asset\_details → list(no value, no value).
- Set account from Platform.db.get\_value(“Asset Category Account”, filters = mapping(“parent” → asset\_category, “company\_name” → company), fieldname = fieldname).
- Return account.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0321.json#L5137) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L378)
