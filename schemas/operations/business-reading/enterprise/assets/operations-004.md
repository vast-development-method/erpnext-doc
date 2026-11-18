# Asset management · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset

[Record definition](../../../../data/record-types/asset.json)

<a id="op-6f0b0df1b5051a"></a>
### Make sales invoice

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_make_sales_invoice`

**Inputs** asset, item\_code, company, sell\_qty, serial\_no = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Asset” via get\_doc · read “Company” via get\_cached\_value.

**State and service calls** request new\_doc for “Sales Invoice”.

**Explicit results** si.

**Local steps**

- Set asset\_doc from Platform.get\_doc(“Asset”, asset).
- Set si from Platform.new\_doc(“Sales Invoice”).
- Set si.company from company.
- Set si.currency from Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- Set tuple(disposal\_account, depreciation\_cost\_center) from \_get\_disposal\_account\_and\_cost\_center(company).
- Evaluate si.append(“items”, mapping(“item\_code” → item\_code, “is\_fixed\_asset” → 1, “asset” → asset, “income\_account” → disposal\_account, …)).
- Set accounting\_dimensions from get\_dimensions(with\_cost\_center\_and\_project = true).
- For each dimension in accounting\_dimensions at 0.
  - Evaluate si.update(mapping(dimension at “fieldname” → (asset\_doc.get(dimension at “fieldname”) or dimension.get(“default\_dimension”)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in asset\_doc.get(dimension at “fieldname”) → dimension.get(“default\_dimension”).
- Evaluate si.set\_missing\_values().
- Return si.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1316)

<a id="op-486ec2cba2429a"></a>
### Create asset maintenance

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_create_asset_maintenance`

**Inputs** asset, item\_code, item\_name, asset\_category, company.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Asset Maintenance”.

**Explicit results** asset\_maintenance.

**Local steps**

- Set asset\_maintenance from Platform.new\_doc(“Asset Maintenance”).
- Evaluate asset\_maintenance.update(mapping(“asset\_name” → asset, “company” → company, “item\_code” → item\_code, “item\_name” → item\_name, …)).
- Return asset\_maintenance.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L668) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1306)

<a id="op-496164d5977a47"></a>
### Create asset repair

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_create_asset_repair`

**Inputs** company, asset, asset\_name.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Asset Repair”.

**Explicit results** asset\_repair.

**Local steps**

- Set asset\_repair from Platform.new\_doc(“Asset Repair”).
- Evaluate asset\_repair.update(mapping(“company” → company, “asset” → asset, “asset\_name” → asset\_name)).
- Return asset\_repair.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L669) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1307)

<a id="op-87dd9eab250c9a"></a>
### Create asset capitalization

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_create_asset_capitalization`

**Inputs** company, asset, asset\_name, item\_code.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Asset Capitalization”.

**Explicit results** asset\_capitalization.

**Local steps**

- Set asset\_capitalization from Platform.new\_doc(“Asset Capitalization”).
- Evaluate asset\_capitalization.update(mapping(“target\_asset” → asset, “company” → company, “target\_asset\_name” → asset\_name, “target\_item\_code” → item\_code)).
- Return asset\_capitalization.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1305)

<a id="op-406e973108c3d3"></a>
### Create asset value adjustment

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_create_asset_value_adjustment`

**Inputs** asset, asset\_category, company.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Asset Value Adjustment”.

**Explicit results** asset\_value\_adjustment.

**Local steps**

- Set asset\_value\_adjustment from Platform.new\_doc(“Asset Value Adjustment”).
- Evaluate asset\_value\_adjustment.update(mapping(“asset” → asset, “company” → company, “asset\_category” → asset\_category)).
- Return asset\_value\_adjustment.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L670) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1308)

<a id="op-b5755aa8ca2d47"></a>
### Transfer asset

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_transfer_asset`

**Inputs** args.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** request new\_doc for “Asset Movement” · call insert on movement\_entry · call submit on movement\_entry · commit · msgprint with translated “Asset Movement record {0} created”.format(text in the contract).format(movement\_entry.name).

**Local steps**

- Set args from json.loads(args).
- If args.get(“serial\_no”).
  - Set args at “quantity” from len(args.get(“serial\_no”).split(whitespace '\\n')).
- Set movement\_entry from Platform.new\_doc(“Asset Movement”).
- Evaluate movement\_entry.update(args).
- Evaluate movement\_entry.insert().
- Evaluate movement\_entry.submit().
- Evaluate Platform.db.commit().
- Evaluate Platform.msgprint(translated “Asset Movement record {0} created”.format(text in the contract).format(movement\_entry.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1322)

<a id="op-0eae70bae31ed9"></a>
### Get item details

`operation_enterprise_assets_record_definitions_asset_business_behavior_get_item_details`

**Inputs** item\_code, asset\_category, net\_purchase\_amount.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Asset Category” via get\_cached\_doc.

**Explicit results** books.

**Local steps**

- Evaluate Platform.has\_permission(“Asset Category”, “read”, asset\_category, throw = true).
- Set asset\_category\_doc from Platform.get\_cached\_doc(“Asset Category”, asset\_category).
- Set books from list().
- For each d in asset\_category\_doc.finance\_books.
  - Evaluate books.append(mapping(“finance\_book” → d.finance\_book, “depreciation\_method” → d.depreciation\_method, “total\_number\_of\_depreciations” → d.total\_number\_of\_depreciations, “frequency\_of\_depreciation” → d.frequ ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.depreciation\_start\_date → nowdate().
- Return books.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset Category”, “read”, asset\_category, throw = true) · configured or stored value from Platform.get\_cached\_doc(“Asset Category”, asset\_category) · clock or generated value from nowdate().

**Boundaries to resolve** stored data, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1418) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L318)

<a id="op-792573f6439f1a"></a>
### Get asset account

`operation_enterprise_assets_record_definitions_asset_business_behavior_get_asset_account`

**Inputs** account\_name, asset = no value, asset\_category = no value, company = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** account.

**Explicit failure paths** validation helper — translated “Set {0} in company {1}”.format(account\_name.replace(“\_”, one space).title(), company) · validation helper — translated “Set {0} in asset category {1} or company {2}”.format(account\_name.replace(“\_”, one space).title(), asset\_category, company).

**Local steps**

- Set account from no value.
- If asset.
  - Set account from get\_asset\_category\_account(account\_name, asset = asset, asset\_category = asset\_category, company = company).
- If (not asset and not account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not asset → not account.
  - Set account from get\_asset\_category\_account(account\_name, asset\_category = asset\_category, company = company).
- If not account.
  - Set account from Platform.get\_cached\_value(“Company”, company, account\_name).
- If not account.
  - If not asset\_category.
    - Call the validation error handler Platform.throw(translated “Set {0} in company {1}”.format(account\_name.replace(“\_”, one space).title(), company)).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Set {0} in asset category {1} or company {2}”.format(account\_name.replace(“\_”, one space).title(), asset\_category, company)).
- Return account.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, account\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L4892) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1415) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L315)

<a id="op-571c84b8f24718"></a>
### Make journal entry

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_make_journal_entry`

**Inputs** asset\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Asset” via get\_doc · read “Company” via get\_cached\_value.

**State and service calls** request new\_doc for “Journal Entry”.

**Explicit results** je.

**Local steps**

- Evaluate Platform.has\_permission(“Asset”, “read”, asset\_name, throw = true).
- Set asset from Platform.get\_doc(“Asset”, asset\_name).
- Set tuple(fixed\_asset\_account, accumulated\_depreciation\_account, depreciation\_expense\_account) from get\_depreciation\_accounts(asset.asset\_category, asset.company).
- Set tuple(depreciation\_cost\_center, depreciation\_series) from Platform.get\_cached\_value(“Company”, asset.company, list(“depreciation\_cost\_center”, “series\_for\_depreciation\_entry”)).
- Set depreciation\_cost\_center from (asset.cost\_center or depreciation\_cost\_center).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in asset.cost\_center → depreciation\_cost\_center.
- Set je from Platform.new\_doc(“Journal Entry”).
- Set je.voucher\_type from “Depreciation Entry”.
- Set je.naming\_series from depreciation\_series.
- Set je.company from asset.company.
- Set je.remark from translated “Depreciation Entry against asset {0}”.format(asset\_name).
- Evaluate je.append(“accounts”, mapping(“account” → depreciation\_expense\_account, “reference\_type” → “Asset”, “reference\_name” → asset.name, “cost\_center” → depreciation\_cost\_center)).
- Evaluate je.append(“accounts”, mapping(“account” → accumulated\_depreciation\_account, “reference\_type” → “Asset”, “reference\_name” → asset.name)).
- Return je.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset”, “read”, asset\_name, throw = true) · configured or stored value from Platform.get\_cached\_value(“Company”, asset.company, list(“depreciation\_cost\_center”, “series\_for\_depreciation\_entry”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1315)

<a id="op-d61de67809fa17"></a>
### Make asset movement

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_make_asset_movement`

**Inputs** assets, purpose = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Asset” via get\_doc.

**State and service calls** request new\_doc for “Asset Movement”.

**Explicit results** asset\_movement.as\_dict().

**Explicit failure paths** validation helper — translated “At least one asset has to be selected.”.

**Local steps**

- Bind dependencies json.
- If isinstance(assets, str).
  - Set assets from json.loads(assets).
- <a id="op-d61de67809fa17-guard-7"></a>If len(assets) equals 0.
  - Call the validation error handler Platform.throw(translated “At least one asset has to be selected.”).
- Set asset\_movement from Platform.new\_doc(“Asset Movement”).
- Set asset\_movement.quantity from len(assets).
- For each asset in assets.
  - Set asset at “name” from cstr(asset.get(“name”)).
  - If (not asset at “name” or not Platform.has\_permission(“Asset”, “select”, doc = asset at “name”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not asset at “name” → not Platform.has\_permission(“Asset”, “select”, doc = asset at “name”).
    - Evaluate \_refuse().
  - Set asset from Platform.get\_doc(“Asset”, asset.get(“name”)).
  - Set asset\_movement.company from asset.get(“company”).
  - Evaluate asset\_movement.append(“assets”, mapping(“asset” → asset.get(“name”), “source\_location” → asset.get(“location”), “from\_employee” → asset.get(“custodian”))).
- If asset\_movement.get(“assets”).
  - Return asset\_movement.as\_dict().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(assets) equals 0, length of assets = 0 selects the branch that calls the validation-error handler with translated “At least one asset has to be selected.”. With length of assets = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-d61de67809fa17-guard-7)

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset”, “select”, doc = asset at “name”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1314)

<a id="op-bbdafe165e3bfb"></a>
### Is cwip accounting enabled

`operation_enterprise_assets_record_definitions_asset_business_behavior_is_cwip_accounting_enabled`

**Inputs** asset\_category.

**Record and data access** read “Asset Category” via get\_value.

**Explicit results** cint(Platform.db.get\_value(“Asset Category”, asset\_category, “enable\_cwip\_accounting”)).

**Local steps**

- Return cint(Platform.db.get\_value(“Asset Category”, asset\_category, “enable\_cwip\_accounting”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L5380) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1422) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L322)

<a id="op-52a83785356dd6"></a>
### Get asset value after depreciation

`operation_enterprise_assets_record_definitions_asset_business_behavior_get_asset_value_after_depreciation`

**Inputs** asset\_name, finance\_book = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_asset\_value\_after\_depreciation(asset\_name, finance\_book).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If not any(generator of Platform.has\_permission(dt, “write”) for dt drawn from tuple(“Asset Value Adjustment”, “Asset Capitalization”, “Asset Repair”)).
  - Draw dt from tuple(“Asset Value Adjustment”, “Asset Capitalization”, “Asset Repair”).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set ptype from “select” when Platform.only\_has\_select\_perm(“Asset”), otherwise “read”.
  - Value choice on Platform.only\_has\_select\_perm(“Asset”) — true gives “select”, false gives “read”.
- Evaluate Platform.has\_permission(“Asset”, ptype, doc = asset\_name, throw = true).
- Return \_get\_asset\_value\_after\_depreciation(asset\_name, finance\_book).

**Values supplied outside this operation** effective access from Platform.has\_permission(dt, “write”), Platform.has\_permission(“Asset”, ptype, doc = asset\_name, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1417) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L317)

<a id="op-dae037940d70ad"></a>
### Get asset value after depreciation

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_get_asset_value_after_depreciation`

**Inputs** asset\_name, finance\_book = no value.

**Record and data access** resolve a document from “Asset” via get\_doc.

**Explicit results** flt(asset.value\_after\_depreciation) · asset.get\_value\_after\_depreciation(finance\_book).

**Local steps**

- Set asset from Platform.get\_doc(“Asset”, asset\_name).
- If not asset.calculate\_depreciation.
  - Return flt(asset.value\_after\_depreciation).
- Return asset.get\_value\_after\_depreciation(finance\_book).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1311)

<a id="op-ff83c703a063d6"></a>
### Has active capitalization

`operation_enterprise_assets_record_definitions_asset_business_behavior_has_active_capitalization`

**Inputs** asset.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Asset Capitalization” via count.

**Explicit results** active\_capitalizations &gt; 0.

**Local steps**

- Evaluate Platform.has\_permission(“Asset”, doc = asset, throw = true).
- Set active\_capitalizations from Platform.db.count(“Asset Capitalization”, filters = mapping(“target\_asset” → asset, “docstatus” → 1)).
- Return active\_capitalizations &gt; 0.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset”, doc = asset, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L320)

<a id="op-927435f5c7937a"></a>
### Get values from purchase doc

`operation_enterprise_assets_record_definitions_asset_business_behavior_get_values_from_purchase_record`

**Inputs** purchase\_doc\_name, item\_code, doctype, asset = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from doctype via get\_doc · resolve a document from “Asset” via get\_doc.

**Explicit results** mapping(“company” → purchase\_doc.company, “purchase\_date” → purchase\_doc.get(“posting\_date”), “net\_purchase\_amount” → ((flt(item.valuation\_rate) × flt((item.conversion\_factor or 1))) × asset\_quantity), “as ….

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid document type” · validation helper — translated “Selected {0} does not contain the Item Code {1}”.format(doctype, item\_code) · validation helper — translated “All quantities of Item {0} in {1} are already linked to Assets.”.format(Platform.bold(item\_code), get\_link\_to\_form(doctype, purchase\_doc\_name)).

**Local steps**

- If doctype does not belong to tuple(“Purchase Receipt”, “Purchase Invoice”).
  - Call the validation error handler Platform.throw(translated “Invalid document type”, Platform.PermissionError).
- Evaluate Platform.has\_permission(“Asset”, “write”, throw = true).
- Set purchase\_doc from Platform.get\_doc(doctype, purchase\_doc\_name, check\_permission = “read”).
- Set matching\_items from purchase\_doc.get(“items”, mapping(“item\_code” → item\_code)).
- If not matching\_items.
  - Call the validation error handler Platform.throw(translated “Selected {0} does not contain the Item Code {1}”.format(doctype, item\_code)).
- If asset.
  - Set asset from Platform.get\_doc(“Asset”, asset, check\_permission = “write”).
- Set fieldname from Platform.scrub(doctype).
- Set linked\_asset\_qty from get\_linked\_asset\_qty((fieldname + “\_item”), list of item.name for item drawn from matching\_items, asset.name when asset, otherwise no value).
  - Draw item from matching\_items.
  - Value choice on asset — true gives asset.name, false gives no value.
- If (asset and asset.get(fieldname) equals purchase\_doc\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in asset → asset.get(fieldname) equals purchase\_doc\_name.
  - Evaluate matching\_items.sort(key = deferred anonymous expression).
- For each item in matching\_items.
  - Set asset\_quantity from (flt(item.qty) − flt(linked\_asset\_qty.get(item.name))).
  - <a id="op-927435f5c7937a-guard-34"></a>If asset\_quantity &gt; 0.
    - Leave the innermost loop without its normal-exhaustion alternative.
- After normal loop exhaustion.
  - Call the validation error handler Platform.throw(translated “All quantities of Item {0} in {1} are already linked to Assets.”.format(Platform.bold(item\_code), get\_link\_to\_form(doctype, purchase\_doc\_name)), title = translated “No Available  ….
- Return mapping(“company” → purchase\_doc.company, “purchase\_date” → purchase\_doc.get(“posting\_date”), “net\_purchase\_amount” → ((flt(item.valuation\_rate) × flt((item.conversion\_factor or 1))) × asset\_quantity), “as ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.conversion\_factor → 1.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.cost\_center → purchase\_doc.get(“cost\_center”).
  - Value choice on doctype equals “Purchase Receipt” — true gives item.name, false gives no value.
  - Value choice on doctype equals “Purchase Invoice” — true gives item.name, false gives no value.

**Derived branch illustrations**

- At the comparison asset\_quantity &gt; 0, asset\_quantity = 1 selects the branch that exits the enclosing loop. With asset\_quantity = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-927435f5c7937a-guard-34)

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset”, “write”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1419) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L319)

<a id="op-5403cffbe7b598"></a>
### Split asset

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_split_asset`

**Inputs** asset\_name, split\_qty.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Asset” via get\_doc.

**Explicit results** splitted\_asset.

**Local steps**

- Set existing\_asset from Platform.get\_doc(“Asset”, asset\_name).
- Set split\_qty from cint(split\_qty).
- Evaluate validate\_asset\_split(existing\_asset, split\_qty).
- Set remaining\_qty from (existing\_asset.asset\_quantity − split\_qty).
- Set splitted\_asset from create\_new\_asset\_from\_split(existing\_asset, split\_qty).
- Evaluate update\_existing\_asset\_after\_split(existing\_asset, remaining\_qty, splitted\_asset).
- Return splitted\_asset.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1321)

<a id="op-63b249bf999ed7"></a>
### Validate asset split

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_validate_asset_split`

**Inputs** existing\_asset, split\_qty.

**Explicit failure paths** validation helper — translated “Asset {0} cannot be split, as it is {1}”.format(existing\_asset.name, existing\_asset.status) · validation helper — translated “Split Quantity must be greater than zero” · validation helper — translated “Split Quantity must be less than Asset Quantity”.

**Local steps**

- If (existing\_asset.docstatus differs from 1 or existing\_asset.status belongs to tuple(“Sold”, “Scrapped”, “Capitalized”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in existing\_asset.docstatus differs from 1 → existing\_asset.status belongs to tuple(“Sold”, “Scrapped”, “Capitalized”).
  - Call the validation error handler Platform.throw(translated “Asset {0} cannot be split, as it is {1}”.format(existing\_asset.name, existing\_asset.status)).
- <a id="op-63b249bf999ed7-guard-7"></a>If split\_qty ≤ 0.
  - Call the validation error handler Platform.throw(translated “Split Quantity must be greater than zero”).
- If split\_qty ≥ existing\_asset.asset\_quantity.
  - Call the validation error handler Platform.throw(translated “Split Quantity must be less than Asset Quantity”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison split\_qty ≤ 0, split\_qty = 0 selects the branch that calls the validation-error handler with translated “Split Quantity must be greater than zero”. With split\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-63b249bf999ed7-guard-7)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L688) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1326)

<a id="op-f8ba38e69f36fc"></a>
### Create new asset from split

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_create_new_asset_from_split`

**Inputs** existing\_asset, split\_qty.

**Explicit results** process\_asset\_split(existing\_asset, split\_qty, is\_new\_asset = true).

**Local steps**

- Return process\_asset\_split(existing\_asset, split\_qty, is\_new\_asset = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L671) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1309)

<a id="op-dfe7a64ffb2615"></a>
### Update existing asset after split

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_update_existing_asset_after_split`

**Inputs** existing\_asset, remaining\_qty, splitted\_asset.

**Local steps**

- Evaluate process\_asset\_split(existing\_asset, remaining\_qty, splitted\_asset = splitted\_asset).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1324)

<a id="op-c7fc091a395016"></a>
### Process asset split

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_process_asset_split`

**Inputs** existing\_asset, split\_qty, splitted\_asset = no value, is\_new\_asset = false.

**State and service calls** request copy\_doc for existing\_asset.

**Explicit results** new\_asset.

**Local steps**

- Set scaling\_factor from (flt(split\_qty) ÷ flt(existing\_asset.asset\_quantity)).
- Set new\_asset from Platform.copy\_doc(existing\_asset) when is\_new\_asset, otherwise splitted\_asset.
  - Value choice on is\_new\_asset — true gives Platform.copy\_doc(existing\_asset), false gives splitted\_asset.
- Set asset\_doc from new\_asset when is\_new\_asset, otherwise existing\_asset.
  - Value choice on is\_new\_asset — true gives new\_asset, false gives existing\_asset.
- Set asset\_doc.flags.is\_split\_asset from true.
- Evaluate set\_split\_asset\_values(asset\_doc, scaling\_factor, split\_qty, existing\_asset, …).
- Evaluate log\_asset\_activity(existing\_asset, asset\_doc, splitted\_asset, is\_new\_asset).
- Evaluate update\_finance\_books(asset\_doc, existing\_asset, new\_asset, scaling\_factor, …).
- Return new\_asset.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1318)

<a id="op-230f33d6b6e5c4"></a>
### Set split asset values

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_set_split_asset_values`

**Inputs** asset\_doc, scaling\_factor, split\_qty, existing\_asset, is\_new\_asset.

**State and service calls** call save on asset\_doc.

**Local steps**

- Set asset\_doc.net\_purchase\_amount from (existing\_asset.net\_purchase\_amount × scaling\_factor).
- Set asset\_doc.purchase\_amount from asset\_doc.net\_purchase\_amount.
- Set asset\_doc.additional\_asset\_cost from (existing\_asset.additional\_asset\_cost × scaling\_factor).
- Set asset\_doc.total\_asset\_cost from (asset\_doc.net\_purchase\_amount + asset\_doc.additional\_asset\_cost).
- Set asset\_doc.opening\_accumulated\_depreciation from (existing\_asset.opening\_accumulated\_depreciation × scaling\_factor).
- Set asset\_doc.value\_after\_depreciation from (existing\_asset.value\_after\_depreciation × scaling\_factor).
- Set asset\_doc.value\_adjustment\_amount from (flt(existing\_asset.value\_adjustment\_amount) × scaling\_factor).
- Set asset\_doc.asset\_quantity from split\_qty.
- Set asset\_doc.split\_from from existing\_asset.name when is\_new\_asset, otherwise no value.
  - Value choice on is\_new\_asset — true gives existing\_asset.name, false gives no value.
- For each row in asset\_doc.get(“finance\_books”).
  - Set row.value\_after\_depreciation from (row.value\_after\_depreciation × scaling\_factor).
  - Set row.expected\_value\_after\_useful\_life from (row.expected\_value\_after\_useful\_life × scaling\_factor).
  - Set row.value\_adjustment\_amount from (flt(row.value\_adjustment\_amount) × scaling\_factor).
- If not is\_new\_asset.
  - Set asset\_doc.flags.ignore\_validate\_update\_after\_submit from true.
  - Evaluate asset\_doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1320)

<a id="op-c2ee4c8c360bd7"></a>
### Log asset activity

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_log_asset_activity`

**Inputs** existing\_asset, asset\_doc, splitted\_asset, is\_new\_asset.

**State and service calls** call insert on asset\_doc · call submit on asset\_doc.

**Local steps**

- If is\_new\_asset.
  - Evaluate asset\_doc.insert().
  - Evaluate add\_asset\_activity(asset\_doc.name, translated “Asset created after being split from Asset {0}”.format(get\_link\_to\_form(“Asset”, existing\_asset.name))).
  - Evaluate asset\_doc.submit().
  - Evaluate asset\_doc.set\_status().
- Otherwise.
  - Evaluate add\_asset\_activity(existing\_asset.name, translated “Asset updated after being split into Asset {0}”.format(get\_link\_to\_form(“Asset”, splitted\_asset.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1313)

<a id="op-e0e41a600f6dc5"></a>
### Update finance books

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_update_finance_books`

**Inputs** asset\_doc, existing\_asset, new\_asset, scaling\_factor, is\_new\_asset.

**Local steps**

- For each fb\_row in asset\_doc.get(“finance\_books”).
  - Evaluate reschedule\_depr\_for\_updated\_asset(existing\_asset, new\_asset, fb\_row, scaling\_factor, …).
- If is\_new\_asset.
  - For each row in new\_asset.get(“finance\_books”).
    - Set depr\_schedule\_doc from get\_depr\_schedule(new\_asset.name, “Active”, row.finance\_book).
    - For each schedule in depr\_schedule\_doc.
      - If schedule.journal\_entry.
        - Evaluate add\_reference\_in\_jv\_on\_split(schedule.journal\_entry, new\_asset.name, existing\_asset.name, schedule.depreciation\_amount).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1325)

<a id="op-cf040091b1ac2a"></a>
### Reschedule depr for updated asset

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_reschedule_depr_for_updated_asset`

**Inputs** existing\_asset, new\_asset, fb\_row, scaling\_factor, is\_new\_asset.

**State and service calls** call cancel on current\_depr\_schedule\_doc · call submit on new\_depr\_schedule\_doc.

**Explicit results** no value.

**Local steps**

- Set current\_depr\_schedule\_doc from get\_asset\_depr\_schedule\_doc(existing\_asset.name, “Active”, fb\_row.finance\_book).
- If not current\_depr\_schedule\_doc.
  - Return no value.
- Set new\_depr\_schedule\_doc from create\_new\_depr\_schedule(current\_depr\_schedule\_doc, existing\_asset, new\_asset, is\_new\_asset, …).
- Evaluate update\_depreciation\_terms(new\_depr\_schedule\_doc, scaling\_factor).
- Evaluate add\_depr\_schedule\_notes(new\_depr\_schedule\_doc, existing\_asset, new\_asset, is\_new\_asset).
- Set new\_depr\_schedule\_doc.flags.is\_rescheduled from true.
- If not is\_new\_asset.
  - Set current\_depr\_schedule\_doc.flags.should\_not\_cancel\_depreciation\_entries from true.
  - Evaluate current\_depr\_schedule\_doc.cancel().
- Evaluate new\_depr\_schedule\_doc.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1319)
