# Asset management · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset capitalization

[Record definition](../../../../data/record-types/asset_capitalization.json)

<a id="op-1d6afaa0714efc"></a>
### Asset Capitalization.validate consumed stock item

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_validate_consumed_stock_item`

**Inputs** self.

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} is not a stock item”.format(d.idx, d.item\_code) · validation helper — translated “Row #{0}: Qty must be a positive number”.format(d.idx).

**Local steps**

- For each d in self.stock\_items.
  - If d.item\_code.
    - Set item from Platform.get\_cached\_doc(“Item”, d.item\_code).
    - If not item.is\_stock\_item.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} is not a stock item”.format(d.idx, d.item\_code)).
    - If flt(d.stock\_qty) ≤ 0.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Qty must be a positive number”.format(d.idx)).
    - Evaluate self.validate\_item(item).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate item](operations-008.md#op-e72ecd626894b6).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, d.item\_code).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0317.json#L6238) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1447) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L346)

<a id="op-27695a2fa6920d"></a>
### Asset Capitalization.validate consumed asset item

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_validate_consumed_asset_item`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Consumed Asset {1} cannot be the same as the Target Asset”.format(d.idx, d.asset) · validation helper — translated “Row #{0}: Consumed Asset {1} cannot be {2}”.format(d.idx, asset.name, asset.status) · validation helper — translated “Row #{0}: Consumed Asset {1} cannot be Draft”.format(d.idx, asset.name) · validation helper — translated “Row #{0}: Consumed Asset {1} cannot be cancelled”.format(d.idx, asset.name) · validation helper — translated “Row #{0}: Consumed Asset {1} does not belong to company {2}”.format(d.idx, asset.name, self.company).

**Local steps**

- For each d in self.asset\_items.
  - If d.asset.
    - If d.asset equals self.target\_asset.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Consumed Asset {1} cannot be the same as the Target Asset”.format(d.idx, d.asset)).
    - Set asset from self.get\_asset\_for\_validation(d.asset).
    - If asset.status belongs to tuple(“Draft”, “Scrapped”, “Sold”, “Capitalized”).
      - Call the validation error handler Platform.throw(translated “Row #{0}: Consumed Asset {1} cannot be {2}”.format(d.idx, asset.name, asset.status)).
    - If asset.docstatus equals 0.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Consumed Asset {1} cannot be Draft”.format(d.idx, asset.name)).
    - Otherwise.
      - <a id="op-27695a2fa6920d-guard-22"></a>If asset.docstatus equals 2.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Consumed Asset {1} cannot be cancelled”.format(d.idx, asset.name)).
    - If asset.company differs from self.company.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Consumed Asset {1} does not belong to company {2}”.format(d.idx, asset.name, self.company)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison asset.docstatus equals 2, asset.docstatus = 2 (cancelled) selects the branch that calls the validation-error handler with translated “Row #{0}: Consumed Asset {1} cannot be cancelled”.format(d.idx, asset.name). With asset.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-27695a2fa6920d-guard-22)

**Methods declared on this owner** [get asset for validation](operations-008.md#op-5c32ee8cf35ef1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0318.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1446) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L345)

<a id="op-4ec4f60c519055"></a>
### Asset Capitalization.validate duplicate consumed assets

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_assetcapitalization_validate_duplicate_consumed_assets`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Consumed Asset {1} is added more than once”.format(d.idx, d.asset).

**Local steps**

- Set consumed\_assets from set().
- For each d in self.asset\_items.
  - If d.asset belongs to consumed\_assets.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Consumed Asset {1} is added more than once”.format(d.idx, d.asset)).
  - Evaluate consumed\_assets.add(d.asset).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L699) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1337)

<a id="op-544f7628b07566"></a>
### Asset Capitalization.validate consumed asset disposal date

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_assetcapitalization_validate_consumed_asset_disposal_date`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Consumed Asset {1} cannot be capitalized before its last depreciation entry dated {2}”.format(d.idx, d.asset, Platform.format(last\_depreciation\_date, “Date”)).

**Local steps**

- For each d in self.asset\_items.
  - Set last\_depreciation\_date from get\_last\_depreciation\_date(d.asset).
  - If (last\_depreciation\_date and getdate(self.posting\_date) &lt; last\_depreciation\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_depreciation\_date → getdate(self.posting\_date) &lt; last\_depreciation\_date.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Consumed Asset {1} cannot be capitalized before its last depreciation entry dated {2}”.format(d.idx, d.asset, Platform.format(last\_depreciation\_date, “Date”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L698) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1336)

<a id="op-e9dcda3d1ed90f"></a>
### Asset Capitalization.validate service item

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_validate_service_item`

**Inputs** self.

**Record and data access** resolve a document from “Item” via get\_cached\_doc · read “Company” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} is not a service item”.format(d.idx, d.item\_code) · validation helper — translated “Row #{0}: Qty must be a positive number”.format(d.idx) · validation helper — translated “Row #{0}: Amount must be a positive number”.format(d.idx).

**Local steps**

- For each d in self.service\_items.
  - If d.item\_code.
    - Set item from Platform.get\_cached\_doc(“Item”, d.item\_code).
    - If (item.is\_stock\_item or item.is\_fixed\_asset).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.is\_stock\_item → item.is\_fixed\_asset.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} is not a service item”.format(d.idx, d.item\_code)).
    - If flt(d.qty) ≤ 0.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Qty must be a positive number”.format(d.idx)).
    - If flt(d.rate) ≤ 0.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Amount must be a positive number”.format(d.idx)).
    - Evaluate self.validate\_item(item).
  - If not d.cost\_center.
    - Set d.cost\_center from Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate item](operations-008.md#op-e72ecd626894b6).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, d.item\_code), Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0318.json#L619) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1449) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L348)

<a id="op-f953e9ac8427db"></a>
### Asset Capitalization.validate source mandatory

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_validate_source_mandatory`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Consumed Stock Items, Consumed Asset Items or Consumed Service Items is mandatory for Capitalization”.

**Local steps**

- If not (self.get(“stock\_items”) or self.get(“asset\_items”) or self.get(“service\_items”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“stock\_items”) → self.get(“asset\_items”) → self.get(“service\_items”).
  - Call the validation error handler Platform.throw(translated “Consumed Stock Items, Consumed Asset Items or Consumed Service Items is mandatory for Capitalization”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0318.json#L1118) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1450) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L349)

<a id="op-e72ecd626894b6"></a>
### Asset Capitalization.validate item

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_validate_item`

**Inputs** self, item.

**Local steps**

- Bind dependencies validate\_end\_of\_life.
- Evaluate validate\_end\_of\_life(item.name, item.end\_of\_life, item.disabled).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0318.json#L1278) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1448) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L347)

<a id="op-5c32ee8cf35ef1"></a>
### Asset Capitalization.get asset for validation

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_get_asset_for_validation`

**Inputs** self, asset.

**Record and data access** read “Asset” via get\_value.

**Explicit results** Platform.db.get\_value(“Asset”, asset, list(“name”, “item\_code”, “company”, “status”, …), as\_dict = 1).

**Local steps**

- Return Platform.db.get\_value(“Asset”, asset, list(“name”, “item\_code”, “company”, “status”, …), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0318.json#L1367) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L328)

<a id="op-c2f7e1a447dd42"></a>
### Asset Capitalization.set warehouse details

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_set_warehouse_details`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.check\_permission(“write”).
- For each d in self.get(“stock\_items”).
  - If (d.item\_code and d.warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.item\_code → d.warehouse.
    - Set args from self.get\_args\_for\_incoming\_rate(d).
    - Set warehouse\_details from \_get\_warehouse\_details(args).
    - Evaluate d.update(warehouse\_details).
- Evaluate self.split\_valuation\_rate\_for\_grouped\_stock\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get args for incoming rate](operations-008.md#op-cde3d3edc2933a), [split valuation rate for grouped stock items](operations-007.md#op-c5693b39e911da).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1441) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L340)

<a id="op-509ddd0a829f85"></a>
### Asset Capitalization.set asset values

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_set_asset_values`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.check\_permission(“write”).
- For each d in self.get(“asset\_items”).
  - If d.asset.
    - Set finance\_book from (d.get(“finance\_book”) or self.get(“finance\_book”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.get(“finance\_book”) → self.get(“finance\_book”).
    - Set d.current\_asset\_value from flt(\_get\_asset\_value\_after\_depreciation(d.asset, finance\_book = finance\_book)).
    - Set d.asset\_value from calculate\_value\_after\_depreciation\_on\_disposal\_date(d.asset, self.posting\_date, finance\_book = finance\_book).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1437) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L336)

<a id="op-cde3d3edc2933a"></a>
### Asset Capitalization.get args for incoming rate

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_get_arguments_for_incoming_rate`

**Inputs** self, item.

**Explicit results** Platform.\_dict(mapping(“item\_code” → item.item\_code, “warehouse” → item.warehouse, “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time, …)).

**Local steps**

- Return Platform.\_dict(mapping(“item\_code” → item.item\_code, “warehouse” → item.warehouse, “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time, …)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0318.json#L2001) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1427) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L327)

<a id="op-e3e93d655d3523"></a>
### Asset Capitalization.calculate totals

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_calculate_totals`

**Inputs** self.

**Local steps**

- Set self.stock\_items\_total from 0.
- Set self.asset\_items\_total from 0.
- Set self.service\_items\_total from 0.
- For each d in self.stock\_items.
  - Set d.amount from flt((flt(d.stock\_qty) × flt(d.valuation\_rate)), d.precision(“amount”)).
  - Update self.stock\_items\_total using + d.amount.
- For each d in self.asset\_items.
  - Set d.asset\_value from flt(flt(d.asset\_value), d.precision(“asset\_value”)).
  - Update self.asset\_items\_total using + d.asset\_value.
- For each d in self.service\_items.
  - Set d.amount from flt((flt(d.qty) × flt(d.rate)), d.precision(“amount”)).
  - Update self.service\_items\_total using + d.amount.
- Set self.stock\_items\_total from flt(self.stock\_items\_total, self.precision(“stock\_items\_total”)).
- Set self.asset\_items\_total from flt(self.asset\_items\_total, self.precision(“asset\_items\_total”)).
- Set self.service\_items\_total from flt(self.service\_items\_total, self.precision(“service\_items\_total”)).
- Set self.total\_value from ((self.stock\_items\_total + self.asset\_items\_total) + self.service\_items\_total).
- Set self.total\_value from flt(self.total\_value, self.precision(“total\_value”)).
- Set self.target\_incoming\_rate from self.total\_value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0318.json#L2356) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1426) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L326)

<a id="op-a4fd86ad09a89a"></a>
### Asset Capitalization.update stock ledger

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_update_stock_ledger`

**Inputs** self.

**Local steps**

- Set sl\_entries from list().
- For each d in self.stock\_items.
  - Set sle from self.get\_sl\_entries(d, mapping(“actual\_qty” → negative flt(d.stock\_qty), “serial\_and\_batch\_bundle” → d.serial\_and\_batch\_bundle)).
  - Evaluate sl\_entries.append(sle).
- If self.docstatus equals 2.
  - Evaluate sl\_entries.reverse().
- If sl\_entries.
  - Evaluate self.make\_sl\_entries(sl\_entries).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0318.json#L3101) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1443) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L342)

<a id="op-e0fccbbbe1ce13"></a>
### Asset Capitalization.make gl entries

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_make_general_ledger_entries`

**Inputs** self, gl\_entries = no value, from\_repost = false.

**Local steps**

- Bind dependencies make\_gl\_entries, make\_reverse\_gl\_entries.
- If self.docstatus equals 1.
  - If not gl\_entries.
    - Set gl\_entries from self.get\_gl\_entries().
  - If gl\_entries.
    - Evaluate make\_gl\_entries(gl\_entries, merge\_entries = false, from\_repost = from\_repost).
- Otherwise.
  - If self.docstatus equals 2.
    - Evaluate make\_reverse\_gl\_entries(voucher\_type = self.doctype, voucher\_no = self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get gl entries](operations-008.md#op-24a0c490aa4762).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0318.json#L3354) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L331)

<a id="op-24a0c490aa4762"></a>
### Asset Capitalization.get gl entries

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_get_general_ledger_entries`

**Inputs** self, inventory\_account\_map = no value, default\_expense\_account = no value, default\_cost\_center = no value.

**Explicit results** gl\_entries.

**Local steps**

- Set gl\_entries from list().
- Set self.inventory\_account\_map from inventory\_account\_map.
- If not self.inventory\_account\_map.
  - Set self.inventory\_account\_map from self.get\_inventory\_account\_map().
- Set precision from self.get\_debit\_field\_precision().
- Set self.sle\_map from self.get\_stock\_ledger\_details().
- Set target\_account from self.get\_target\_account().
- Set target\_against from set().
- Evaluate self.get\_gl\_entries\_for\_consumed\_stock\_items(gl\_entries, target\_account, target\_against, precision).
- Evaluate self.get\_gl\_entries\_for\_consumed\_asset\_items(gl\_entries, target\_account, target\_against, precision).
- Evaluate self.get\_gl\_entries\_for\_consumed\_service\_items(gl\_entries, target\_account, target\_against, precision).
- Evaluate self.get\_gl\_entries\_for\_target\_item(gl\_entries, target\_account, target\_against, precision).
- Return gl\_entries.

**Methods declared on this owner** [get target account](operations-008.md#op-57b5a7eca04048), [get gl entries for consumed stock items](operations-008.md#op-0c8540fac3b806), [get gl entries for consumed asset items](operations-008.md#op-def4727f59c3a4), [get gl entries for consumed service items](operations-008.md#op-1f1161b2d8d73d), [get gl entries for target item](operations-008.md#op-a7dda5e803f598).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L329)

<a id="op-57b5a7eca04048"></a>
### Asset Capitalization.get target account

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_get_target_account`

**Inputs** self.

**Record and data access** read “Asset” via get\_cached\_value.

**Explicit results** target\_account when target\_account, otherwise self.target\_fixed\_asset\_account · self.target\_fixed\_asset\_account.

**Local steps**

- Bind dependencies is\_cwip\_accounting\_enabled.
- Set asset\_category from Platform.get\_cached\_value(“Asset”, self.target\_asset, “asset\_category”).
- If is\_cwip\_accounting\_enabled(asset\_category).
  - Set target\_account from get\_asset\_category\_account(“capital\_work\_in\_progress\_account”, asset\_category = asset\_category, company = self.company).
  - Return target\_account when target\_account, otherwise self.target\_fixed\_asset\_account.
    - Value choice on target\_account — true gives target\_account, false gives self.target\_fixed\_asset\_account.
- Otherwise.
  - Return self.target\_fixed\_asset\_account.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Asset”, self.target\_asset, “asset\_category”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0318.json#L3711) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L330)

<a id="op-0c8540fac3b806"></a>
### Asset Capitalization.get gl entries for consumed stock items

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_assetcapitalization_get_gl_entries_for_consumed_stock_items`

**Inputs** self, gl\_entries, target\_account, target\_against, precision.

**Local steps**

- For each item\_row in self.stock\_items.
  - Set sle\_list from self.sle\_map.get(item\_row.name).
  - If sle\_list.
    - Set \_inv\_dict from self.get\_inventory\_account\_dict(item\_row, self.inventory\_account\_map).
    - For each sle in sle\_list.
      - Set stock\_value\_difference from flt(sle.stock\_value\_difference, precision).
      - If Enterprise.is\_perpetual\_inventory\_enabled(self.company).
        - Set account from \_inv\_dict at “account”.
      - Otherwise.
        - Set account from self.get\_company\_default(“default\_expense\_account”).
      - Evaluate target\_against.add(account).
      - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → account, “against” → target\_account, “cost\_center” → item\_row.cost\_center, “project” → (item\_row.get(“project”) or self.get(“project”)), …), \_inv\_dict ….
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“project”) → self.get(“project”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → “Accounting Entry for Stock”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L695) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1333)

<a id="op-def4727f59c3a4"></a>
### Asset Capitalization.get gl entries for consumed asset items

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_assetcapitalization_get_gl_entries_for_consumed_asset_items`

**Inputs** self, gl\_entries, target\_account, target\_against, precision.

**Record and data access** resolve a document from “Asset” via get\_doc.

**Local steps**

- For each item in self.asset\_items.
  - Set asset from Platform.get\_doc(“Asset”, item.asset).
  - If asset.asset\_type equals “Composite Component”.
    - Continue with the next iteration or loop test.
  - Set fixed\_asset\_gl\_entries from get\_gl\_entries\_on\_asset\_disposal(asset, item.asset\_value, (item.get(“finance\_book”) or self.get(“finance\_book”)), self.get(“doctype”), …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“finance\_book”) → self.get(“finance\_book”).
  - For each gle in fixed\_asset\_gl\_entries.
    - Set gle at “against” from target\_account.
    - Evaluate gl\_entries.append(self.get\_gl\_dict(gle, item = item)).
    - Evaluate target\_against.add(gle at “account”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L693) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1331)

<a id="op-1f1161b2d8d73d"></a>
### Asset Capitalization.get gl entries for consumed service items

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_assetcapitalization_get_gl_entries_for_consumed_service_items`

**Inputs** self, gl\_entries, target\_account, target\_against, precision.

**Local steps**

- For each item\_row in self.service\_items.
  - Set expense\_amount from flt(item\_row.amount, precision).
  - Evaluate target\_against.add(item\_row.expense\_account).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → item\_row.expense\_account, “against” → target\_account, “cost\_center” → item\_row.cost\_center, “project” → (item\_row.get(“project”) or self.get(“project” ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“project”) → self.get(“project”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → “Accounting Entry for Stock”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L694) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1332)

<a id="op-a7dda5e803f598"></a>
### Asset Capitalization.get gl entries for target item

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_assetcapitalization_get_gl_entries_for_target_item`

**Inputs** self, gl\_entries, target\_account, target\_against, precision.

**Local steps**

- Set total\_value from flt(sum(generator of (flt(gle.credit) − flt(gle.debit)) for gle drawn from gl\_entries), precision).
  - Draw gle from gl\_entries.
- If total\_value.
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → target\_account, “against” → “, ”.join(target\_against), “remarks” → (self.get(“remarks”) or translated “Accounting Entry for Asset”), “debit” → total\_v ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Asset”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L696) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1334)

<a id="op-0da7de103d3cd1"></a>
### Asset Capitalization.update target asset

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_update_target_asset`

**Inputs** self.

**State and service calls** msgprint with translated “Asset {0} has been updated. Please set the depreciation details if any and submit it.”.format(get\_link\_to\_form(“Asset”, self.target\_asset)).

**Local steps**

- Set total\_target\_asset\_value from flt(self.total\_value, self.precision(“total\_value”)).
- If self.docstatus equals 2.
  - Update total\_target\_asset\_value using × negative 1.
- Evaluate self.add\_to\_target\_asset\_cost(total\_target\_asset\_value).
- Evaluate Platform.msgprint(translated “Asset {0} has been updated. Please set the depreciation details if any and submit it.”.format(get\_link\_to\_form(“Asset”, self.target\_asset))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add to target asset cost](operations-008.md#op-464954ea47b67a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1444) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L343)

<a id="op-464954ea47b67a"></a>
### Asset Capitalization.add to target asset cost

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_assetcapitalization_add_to_target_asset_cost`

**Inputs** self, amount.

**Declared result** no value.

**Record and data access** resolve a document from “Asset” via get\_doc.

**State and service calls** call db\_set on asset\_doc.

**Local steps**

- Set asset\_doc from Platform.get\_doc(“Asset”, self.target\_asset).
- Evaluate asset\_doc.db\_set(mapping(“net\_purchase\_amount” → (asset\_doc.net\_purchase\_amount + amount), “purchase\_amount” → (asset\_doc.purchase\_amount + amount), “total\_asset\_cost” → (asset\_doc.total\_asset\_cost + amount))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1327)

<a id="op-687e6cfd0ba748"></a>
### Asset Capitalization.update stock item rate

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_assetcapitalization_update_stock_item_rate`

**Inputs** self, row\_name, valuation\_rate.

**Declared result** no value.

**Record and data access** read “Asset” via get\_value.

**State and service calls** call db\_update on row · call db\_update on self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The cost of items consumed in Asset Capitalization {0} has changed, but its Target Asset {1} is already subm …”.format(get\_link\_to\_form(self.doctype, self.name), get\_link\_to\_form(“Asset”, self. ….

**Local steps**

- Set row from self.get(“stock\_items”, mapping(“name” → row\_name)) at 0.
- Set previous\_total from self.total\_value.
- Set row.valuation\_rate from valuation\_rate.
- Evaluate self.calculate\_totals().
- Set difference from flt((self.total\_value − previous\_total), self.precision(“total\_value”)).
- If not difference.
  - Return no value.
- Set target\_asset\_status from Platform.db.get\_value(“Asset”, self.target\_asset, “docstatus”).
- If target\_asset\_status equals 1.
  - Call the validation error handler Platform.throw(translated “The cost of items consumed in Asset Capitalization {0} has changed, but its Target Asset {1} is already subm …”.format(get\_link\_to\_form(self.doctype, self.name), get\_link\_to\_form ….
- Evaluate row.db\_update().
- Evaluate self.db\_update().
- If target\_asset\_status equals 0.
  - Evaluate self.add\_to\_target\_asset\_cost(difference).

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate totals](operations-008.md#op-e3e93d655d3523), [add to target asset cost](operations-008.md#op-464954ea47b67a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L697) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1335)

<a id="op-6549f0bfab188b"></a>
### Asset Capitalization.dispose consumed assets

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_assetcapitalization_dispose_consumed_assets`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_doc.

**State and service calls** call db\_set on asset.

**Local steps**

- For each item in self.asset\_items.
  - Set asset from Platform.get\_doc(“Asset”, item.asset).
  - If asset.asset\_type differs from “Composite Component”.
    - Set notes from translated “This schedule was created when Asset {0} was consumed through Asset Capitalization {1}.”.format(get\_link\_to\_form(asset.doctype, asset.name), get\_link\_to\_form(self.doctype, self.name)).
    - Evaluate depreciate\_asset(asset, self.posting\_date, notes).
    - Evaluate asset.reload().
  - Evaluate asset.db\_set(“disposal\_date”, self.posting\_date).
  - Evaluate self.set\_consumed\_asset\_status(asset).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set consumed asset status](operations-009.md#op-f95c46893f7585).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L692) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1330)
