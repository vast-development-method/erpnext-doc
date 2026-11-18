# Asset management · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset

[Record definition](../../../../data/record-types/asset.json)

<a id="op-4b0c1c68628cfe"></a>
### Get gross asset value

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_get_gross_asset_value`

**Inputs** asset, finance\_book = no value.

**Declared result** float.

**Explicit results** flt(((flt(asset.net\_purchase\_amount) + flt(asset.additional\_asset\_cost)) + get\_value\_adjustment\_amount(asset, finance\_book)), asset.precision(“net\_purchase\_amount”)).

**Local steps**

- Return flt(((flt(asset.net\_purchase\_amount) + flt(asset.additional\_asset\_cost)) + get\_value\_adjustment\_amount(asset, finance\_book)), asset.precision(“net\_purchase\_amount”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L711) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1349)

<a id="op-65c276d0f72f84"></a>
### Get value adjustment amount

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_get_value_adjustment_amount`

**Inputs** asset, finance\_book = no value.

**Declared result** float.

**Explicit results** flt(asset.value\_adjustment\_amount) · flt(row.value\_adjustment\_amount) when row, otherwise 0.0.

**Local steps**

- If not asset.calculate\_depreciation.
  - Return flt(asset.value\_adjustment\_amount).
- Set row from next(generator of row for row drawn from asset.get(“finance\_books”) where (not finance\_book or row.finance\_book equals finance\_book), no value).
  - Draw row from asset.get(“finance\_books”), keep a combination only if ((not finance\_book or row.finance\_book equals finance\_book)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not finance\_book → row.finance\_book equals finance\_book.
- Return flt(row.value\_adjustment\_amount) when row, otherwise 0.0.
  - Value choice on row — true gives flt(row.value\_adjustment\_amount), false gives 0.0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1350)

<a id="op-b5b60566a2b476"></a>
### Get depreciation accounts

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_depreciation_accounts`

**Inputs** asset\_category, company.

**Record and data access** read “Asset Category” via get\_value · read “Asset Category Account” via get\_value · read “Company” via get\_cached\_value.

**Explicit results** tuple(fixed\_asset\_account, accumulated\_depreciation\_account, depreciation\_expense\_account).

**Explicit failure paths** validation helper — translated “Please set Fixed Asset Account in Asset Category {0}”.format(asset\_category) · validation helper — translated “Please set Depreciation related Accounts in Asset Category {0} or Company {1}”.format(asset\_category, company).

**Local steps**

- Set fixed\_asset\_account, accumulated\_depreciation\_account, depreciation\_expense\_account from no value.
- Set non\_depreciable\_category from Platform.db.get\_value(“Asset Category”, asset\_category, “non\_depreciable\_category”).
- Set accounts from Platform.db.get\_value(“Asset Category Account”, filters = mapping(“parent” → asset\_category, “company\_name” → company), fieldname = list(“fixed\_asset\_account”, “accumulated\_depreciation\_account”, “deprecia ….
- If accounts.
  - Set fixed\_asset\_account from accounts.fixed\_asset\_account.
  - Set accumulated\_depreciation\_account from accounts.accumulated\_depreciation\_account.
  - Set depreciation\_expense\_account from accounts.depreciation\_expense\_account.
- If not fixed\_asset\_account.
  - Call the validation error handler Platform.throw(translated “Please set Fixed Asset Account in Asset Category {0}”.format(asset\_category)).
- If not non\_depreciable\_category.
  - Set accounts from Platform.get\_cached\_value(“Company”, company, list(“accumulated\_depreciation\_account”, “depreciation\_expense\_account”)).
  - If not accumulated\_depreciation\_account.
    - Set accumulated\_depreciation\_account from accounts at 0.
  - If not depreciation\_expense\_account.
    - Set depreciation\_expense\_account from accounts at 1.
  - If (not accumulated\_depreciation\_account or not depreciation\_expense\_account).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not accumulated\_depreciation\_account → not depreciation\_expense\_account.
    - Call the validation error handler Platform.throw(translated “Please set Depreciation related Accounts in Asset Category {0} or Company {1}”.format(asset\_category, company)).
- Return tuple(fixed\_asset\_account, accumulated\_depreciation\_account, depreciation\_expense\_account).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, list(“accumulated\_depreciation\_account”, “depreciation\_expense\_account”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L4411) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1517) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L397)

<a id="op-ecc15ccf922f88"></a>
### Get profit gl entries

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_profit_general_ledger_entries`

**Inputs** asset, profit\_amount, gl\_entries, disposal\_account, depreciation\_cost\_center, date = no value.

**Local steps**

- If not date.
  - Set date from getdate().
- Set debit\_or\_credit from “debit” when profit\_amount &lt; 0, otherwise “credit”.
  - Value choice on profit\_amount &lt; 0 — true gives “debit”, false gives “credit”.
- Evaluate gl\_entries.append(asset.get\_gl\_dict(mapping(“account” → disposal\_account, “cost\_center” → depreciation\_cost\_center, debit\_or\_credit → abs(profit\_amount), (debit\_or\_credit + “\_in\_account\_currency”) → abs(pr ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L5024) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1527) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L407)

<a id="op-d521331d9d76f8"></a>
### Get disposal account and cost center

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_disposal_account_and_cost_center`

**Inputs** company.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_disposal\_account\_and\_cost\_center(company).

**Local steps**

- Evaluate Platform.has\_permission(“Company”, “read”, company, throw = true).
- Return \_get\_disposal\_account\_and\_cost\_center(company).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, “read”, company, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1520) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L400)

<a id="op-b19c3ae86961ea"></a>
### Get disposal account and cost center

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_get_disposal_account_and_cost_center`

**Inputs** company.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(disposal\_account, depreciation\_cost\_center).

**Explicit failure paths** validation helper — translated “Please set 'Gain/Loss Account on Asset Disposal' in Company {0}”.format(company) · validation helper — translated “Please set 'Asset Depreciation Cost Center' in Company {0}”.format(company).

**Local steps**

- Set tuple(disposal\_account, depreciation\_cost\_center) from Platform.get\_cached\_value(“Company”, company, list(“disposal\_account”, “depreciation\_cost\_center”)).
- If not disposal\_account.
  - Call the validation error handler Platform.throw(translated “Please set 'Gain/Loss Account on Asset Disposal' in Company {0}”.format(company)).
- If not depreciation\_cost\_center.
  - Call the validation error handler Platform.throw(translated “Please set 'Asset Depreciation Cost Center' in Company {0}”.format(company)).
- Return tuple(disposal\_account, depreciation\_cost\_center).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, list(“disposal\_account”, “depreciation\_cost\_center”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L710) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1348)

<a id="op-fd7c10ac908e54"></a>
### Get value after depreciation on disposal date

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_value_after_depreciation_on_disposal_date`

**Inputs** asset, disposal\_date, finance\_book = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** float.

**Explicit results** calculate\_value\_after\_depreciation\_on\_disposal\_date(asset, disposal\_date, finance\_book).

**Local steps**

- Evaluate Platform.has\_permission(“Asset”, “read”, asset, throw = true).
- Return calculate\_value\_after\_depreciation\_on\_disposal\_date(asset, disposal\_date, finance\_book).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset”, “read”, asset, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1528) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L408)

<a id="op-9ab6114dc5369f"></a>
### Calculate value after depreciation on disposal date

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_calculate_value_after_depreciation_on_disposal_date`

**Inputs** asset, disposal\_date, finance\_book = no value.

**Declared result** float.

**Record and data access** resolve a document from “Asset” via get\_doc.

**Explicit results** flt(asset\_doc.value\_after\_depreciation) · flt((asset\_doc.net\_purchase\_amount − asset\_doc.opening\_accumulated\_depreciation)) · flt((flt(asset\_doc.net\_purchase\_amount) − accumulated\_depr\_amount), asset\_doc.precision(“net\_purchase\_amount”)).

**Local steps**

- Set asset\_doc from Platform.get\_doc(“Asset”, asset).
- If asset\_doc.asset\_type equals “Composite Component”.
  - Evaluate validate\_disposal\_date(asset\_doc.purchase\_date, getdate(disposal\_date), “purchase”).
  - Return flt(asset\_doc.value\_after\_depreciation).
- Evaluate validate\_disposal\_date(asset\_doc.available\_for\_use\_date, getdate(disposal\_date), “available for use”).
- If asset\_doc.available\_for\_use\_date equals getdate(disposal\_date).
  - Return flt((asset\_doc.net\_purchase\_amount − asset\_doc.opening\_accumulated\_depreciation)).
- If not asset\_doc.calculate\_depreciation.
  - Return flt(asset\_doc.value\_after\_depreciation).
- Set idx from 1.
- If finance\_book.
  - For each d in asset\_doc.finance\_books.
    - If d.finance\_book equals finance\_book.
      - Set idx from d.idx.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Set row from asset\_doc.finance\_books at (idx − 1).
- Set temp\_asset\_depreciation\_schedule from get\_temp\_depr\_schedule\_doc(asset\_doc, row, getdate(disposal\_date)).
- Set accumulated\_depr\_amount from temp\_asset\_depreciation\_schedule.get(“depreciation\_schedule”) at negative 1.accumulated\_depreciation\_amount.
- Return flt((flt(asset\_doc.net\_purchase\_amount) − accumulated\_depr\_amount), asset\_doc.precision(“net\_purchase\_amount”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1346)

<a id="op-97852ce078b564"></a>
### Validate disposal date

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_validate_disposal_date`

**Inputs** reference\_date, disposal\_date, label.

**Explicit failure paths** validation helper — translated “Disposal date {0} cannot be before {1} date {2} of the asset.”.format(disposal\_date, label, reference\_date).

**Local steps**

- If reference\_date &gt; disposal\_date.
  - Call the validation error handler Platform.throw(translated “Disposal date {0} cannot be before {1} date {2} of the asset.”.format(disposal\_date, label, reference\_date)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L6270) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1543) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L423)

## Record · Asset activity

[Record definition](../../../../data/record-types/asset_activity.json)

<a id="op-ac42e32352b558"></a>
### Add asset activity

`operation_enterprise_assets_record_definitions_asset_activity_business_behavior_add_asset_activity`

**Inputs** asset, subject.

**Record and data access** resolve a document from mapping(“doctype” → “Asset Activity”, “asset” → asset, “subject” → subject, “user” → Platform.session.user, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Asset Activity”, “asset” → asset, “subject” → subject, “user” → Platform.session.user, …)).

**Local steps**

- Evaluate Platform.get\_doc(mapping(“doctype” → “Asset Activity”, “asset” → asset, “subject” → subject, “user” → Platform.session.user, …)).insert(ignore\_permissions = true, ignore\_links = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0317.json#L2445) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L259)

<a id="op-906451ae845240"></a>
### Get permission query conditions

`operation_enterprise_binding_enterprise_assets_doctype_asset_activity_asset_activity_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user, doctype.

**Explicit result forms** a value selected from the current context, no value.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L221) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L648) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1286)

<a id="op-b20db7bc8b2c68"></a>
### Has permission

`operation_enterprise_binding_enterprise_assets_doctype_asset_activity_asset_activity_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, user, ptype.

**Explicit result forms** Boolean false, the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L222) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L649) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1287)

## Record · Asset capitalization

[Record definition](../../../../data/record-types/asset_capitalization.json)

<a id="op-0fe36a9b50e8a6"></a>
### Asset Capitalization.validate

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_posting\_time().
- Evaluate self.set\_missing\_values(for\_validate = true).
- Evaluate self.validate\_target\_item().
- Evaluate self.validate\_target\_asset().
- Evaluate self.validate\_consumed\_stock\_item().
- Evaluate self.validate\_consumed\_asset\_item().
- Evaluate self.validate\_duplicate\_consumed\_assets().
- Evaluate self.validate\_consumed\_asset\_disposal\_date().
- Evaluate self.validate\_service\_item().
- Evaluate self.set\_warehouse\_details().
- Evaluate self.set\_asset\_values().
- Evaluate self.calculate\_totals().
- Evaluate self.set\_title().
- Evaluate self.validate\_inventory\_dimension\_mandatory().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set missing values](operations-007.md#op-5d08bcdfb44827), [validate target item](operations-007.md#op-774200462fe748), [validate target asset](operations-007.md#op-6b1d805e8bf056), [validate consumed stock item](operations-008.md#op-1d6afaa0714efc), [validate consumed asset item](operations-008.md#op-27695a2fa6920d), [validate duplicate consumed assets](operations-008.md#op-4ec4f60c519055), [validate consumed asset disposal date](operations-008.md#op-544f7628b07566), [validate service item](operations-008.md#op-e9dcda3d1ed90f), [set warehouse details](operations-008.md#op-c2f7e1a447dd42), [set asset values](operations-008.md#op-509ddd0a829f85), [calculate totals](operations-008.md#op-e3e93d655d3523), [set title](operations-007.md#op-6e73ab895eef70).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1445) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L344)

<a id="op-e04cd7614833ba"></a>
### Asset Capitalization.on update

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_on_update`

**Inputs** self.

**Local steps**

- If self.stock\_items.
  - Evaluate self.set\_serial\_and\_batch\_bundle(table\_name = “stock\_items”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0317.json#L2901) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1435) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L334)

<a id="op-3f41add99055e1"></a>
### Asset Capitalization.before submit

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_source\_mandatory().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate source mandatory](operations-008.md#op-f953e9ac8427db).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0317.json#L2979) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1425) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L325)

<a id="op-4ff2c649f87384"></a>
### Asset Capitalization.on submit

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.make\_bundle\_using\_old\_serial\_batch\_fields().
- Evaluate self.update\_stock\_ledger().
- Evaluate self.dispose\_consumed\_assets().
- Evaluate self.make\_gl\_entries().
- Evaluate self.repost\_future\_sle\_and\_gle().
- Evaluate self.update\_target\_asset().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update stock ledger](operations-008.md#op-a4fd86ad09a89a), [dispose consumed assets](operations-008.md#op-6549f0bfab188b), [make gl entries](operations-008.md#op-e0fccbbbe1ce13), [update target asset](operations-008.md#op-0da7de103d3cd1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L333)

<a id="op-4a518146ae1d09"></a>
### Asset Capitalization.before cancel

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_assetcapitalization_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.cancel\_target\_asset().

If control reaches the end, it returns no value.

**Methods declared on this owner** [cancel target asset](operations-007.md#op-ea25e1ae859f76).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1328)

<a id="op-ea25e1ae859f76"></a>
### Asset Capitalization.cancel target asset

`operation_enterprise_binding_enterprise_assets_doctype_asset_capitalization_asset_capitalization_assetcapitalization_cancel_target_asset`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_doc.

**State and service calls** call cancel on target\_asset.

**Explicit results** no value.

**Local steps**

- Set target\_asset from Platform.get\_doc(“Asset”, self.target\_asset).
- <a id="op-ea25e1ae859f76-guard-4"></a>If target\_asset.docstatus differs from 1.
  - Return no value.
- Set target\_asset.flags.cancelled\_by\_asset\_capitalization from self.name.
- Evaluate target\_asset.cancel().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison target\_asset.docstatus differs from 1, target\_asset.docstatus = 0 (draft) selects the branch that returns no value. With target\_asset.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-ea25e1ae859f76-guard-4)

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1329)

<a id="op-b5d5de9ccf2dee"></a>
### Asset Capitalization.on cancel

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_on_cancel`

**Inputs** self.

**Local steps**

- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Repost Item Valuation”, “Serial and Batch Bundle”, …).
- Evaluate self.update\_stock\_ledger().
- Evaluate self.make\_gl\_entries().
- Evaluate self.repost\_future\_sle\_and\_gle().
- Evaluate self.restore\_consumed\_asset\_items().
- Evaluate self.update\_target\_asset().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update stock ledger](operations-008.md#op-a4fd86ad09a89a), [make gl entries](operations-008.md#op-e0fccbbbe1ce13), [restore consumed asset items](operations-009.md#op-713a96788c327a), [update target asset](operations-008.md#op-0da7de103d3cd1).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0317.json#L3158) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1433) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L332)

<a id="op-6e73ab895eef70"></a>
### Asset Capitalization.set title

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_set_title`

**Inputs** self.

**Local steps**

- Set self.title from (self.target\_asset\_name or self.target\_item\_code).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.target\_asset\_name → self.target\_item\_code.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0317.json#L3360) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1440) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L339)

<a id="op-5d08bcdfb44827"></a>
### Asset Capitalization.set missing values

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_set_missing_values`

**Inputs** self, for\_validate = false.

**Local steps**

- Set target\_item\_details from get\_target\_item\_details(self.target\_item\_code, self.company).
- For each tuple(k, v) in target\_item\_details.items().
  - If (self.meta.has\_field(k) and (not self.get(k) or k belongs to force\_fields)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.has\_field(k) → (not self.get(k) or k belongs to force\_fields).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.get(k) → k belongs to force\_fields.
    - Evaluate self.set(k, v).
- Set target\_asset\_details from get\_target\_asset\_details(self.target\_asset, self.company).
- For each tuple(k, v) in target\_asset\_details.items().
  - If (self.meta.has\_field(k) and (not self.get(k) or k belongs to force\_fields)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.has\_field(k) → (not self.get(k) or k belongs to force\_fields).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.get(k) → k belongs to force\_fields.
    - Evaluate self.set(k, v).
- For each d in self.stock\_items.
  - Set args from self.as\_dict().
  - Evaluate args.update(d.as\_dict()).
  - Set args.doctype from self.doctype.
  - Set args.name from self.name.
  - Set consumed\_stock\_item\_details from \_get\_consumed\_stock\_item\_details(args).
  - For each tuple(k, v) in consumed\_stock\_item\_details.items().
    - If (d.meta.has\_field(k) and (not d.get(k) or k belongs to force\_fields)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.meta.has\_field(k) → (not d.get(k) or k belongs to force\_fields).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.get(k) → k belongs to force\_fields.
      - Evaluate d.set(k, v).
- Evaluate self.split\_valuation\_rate\_for\_grouped\_stock\_items().
- For each d in self.asset\_items.
  - Set args from self.as\_dict().
  - Evaluate args.update(d.as\_dict()).
  - Set args.doctype from self.doctype.
  - Set args.name from self.name.
  - Set args.finance\_book from (d.get(“finance\_book”) or self.get(“finance\_book”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.get(“finance\_book”) → self.get(“finance\_book”).
  - Set consumed\_asset\_details from get\_consumed\_asset\_details(args).
  - For each tuple(k, v) in consumed\_asset\_details.items().
    - If (d.meta.has\_field(k) and (not d.get(k) or k belongs to force\_fields)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.meta.has\_field(k) → (not d.get(k) or k belongs to force\_fields).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.get(k) → k belongs to force\_fields.
      - Evaluate d.set(k, v).
- For each d in self.service\_items.
  - Set args from self.as\_dict().
  - Evaluate args.update(d.as\_dict()).
  - Set args.doctype from self.doctype.
  - Set args.name from self.name.
  - Set service\_item\_details from get\_service\_item\_details(args).
  - For each tuple(k, v) in service\_item\_details.items().
    - If (d.meta.has\_field(k) and (not d.get(k) or k belongs to force\_fields)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.meta.has\_field(k) → (not d.get(k) or k belongs to force\_fields).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.get(k) → k belongs to force\_fields.
      - Evaluate d.set(k, v).

If control reaches the end, it returns no value.

**Methods declared on this owner** [split valuation rate for grouped stock items](operations-007.md#op-c5693b39e911da).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1439) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L338)

<a id="op-c5693b39e911da"></a>
### Asset Capitalization.split valuation rate for grouped stock items

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_split_valuation_rate_for_grouped_stock_items`

**Inputs** self.

**Local steps**

- Set groups from mapping().
- For each d in self.stock\_items.
  - If (d.item\_code and d.warehouse and not (d.serial\_no or d.batch\_no or d.serial\_and\_batch\_bundle)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.item\_code → d.warehouse → not (d.serial\_no or d.batch\_no or d.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.serial\_no → d.batch\_no → d.serial\_and\_batch\_bundle.
    - Evaluate groups.setdefault(tuple(d.item\_code, d.warehouse), list()).append(d).
- For each rows in groups.values().
  - <a id="op-c5693b39e911da-guard-8"></a>If len(rows) &lt; 2.
    - Continue with the next iteration or loop test.
  - Set cumulative\_qty from 0.0.
  - Set prev\_cumulative\_value from 0.0.
  - For each d in rows.
    - Update cumulative\_qty using + flt(d.stock\_qty).
    - Set args from self.get\_args\_for\_incoming\_rate(d).
    - Set args at “qty” from (negative 1 × cumulative\_qty).
    - Set cumulative\_rate from flt(\_get\_incoming\_rate(args, raise\_error\_if\_no\_rate = false)).
    - Set cumulative\_value from (cumulative\_rate × cumulative\_qty).
    - Set row\_value from (cumulative\_value − prev\_cumulative\_value).
    - Set d.valuation\_rate from flt((row\_value ÷ d.stock\_qty)) when flt(d.stock\_qty), otherwise 0.0.
      - Value choice on flt(d.stock\_qty) — true gives flt((row\_value ÷ d.stock\_qty)), false gives 0.0.
    - Set d.amount from flt((flt(d.stock\_qty) × d.valuation\_rate), d.precision(“amount”)).
    - Set prev\_cumulative\_value from cumulative\_value.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(rows) &lt; 2, length of rows = 1 selects the branch that continues with the next loop iteration. With length of rows = 2, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c5693b39e911da-guard-8)

**Methods declared on this owner** [get args for incoming rate](operations-008.md#op-cde3d3edc2933a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1442) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L341)

<a id="op-774200462fe748"></a>
### Asset Capitalization.validate target item

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_validate_target_item`

**Inputs** self.

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit failure paths** validation helper — translated “Target Item {0} must be a Fixed Asset item”.format(target\_item.name).

**Local steps**

- Set target\_item from Platform.get\_cached\_doc(“Item”, self.target\_item\_code).
- If not target\_item.is\_fixed\_asset.
  - Call the validation error handler Platform.throw(translated “Target Item {0} must be a Fixed Asset item”.format(target\_item.name)).
- Evaluate self.validate\_item(target\_item).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate item](operations-008.md#op-e72ecd626894b6).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, self.target\_item\_code).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0317.json#L5424) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1452) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L351)

<a id="op-6b1d805e8bf056"></a>
### Asset Capitalization.validate target asset

`operation_enterprise_assets_record_definitions_asset_capitalization_business_behavior_asset_capitalization_validate_target_asset`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Target Asset is mandatory” · validation helper — translated “Target Asset {0} needs to be composite asset”.format(target\_asset.name) · validation helper — translated “Asset {0} does not belong to Item {1}”.format(self.target\_asset, self.target\_item\_code) · validation helper — translated “Target Asset {0} cannot be {1}”.format(target\_asset.name, target\_asset.status) · validation helper — translated “Target Asset {0} cannot be submitted”.format(target\_asset.name) · 2 additional forms in the steps below.

**Local steps**

- If not self.target\_asset.
  - Call the validation error handler Platform.throw(translated “Target Asset is mandatory”, Platform.MandatoryError).
- Set target\_asset from self.get\_asset\_for\_validation(self.target\_asset).
- If not target\_asset.asset\_type equals “Composite Asset”.
  - Call the validation error handler Platform.throw(translated “Target Asset {0} needs to be composite asset”.format(target\_asset.name)).
- If target\_asset.item\_code differs from self.target\_item\_code.
  - Call the validation error handler Platform.throw(translated “Asset {0} does not belong to Item {1}”.format(self.target\_asset, self.target\_item\_code)).
- If target\_asset.status belongs to tuple(“Scrapped”, “Sold”, “Capitalized”).
  - Call the validation error handler Platform.throw(translated “Target Asset {0} cannot be {1}”.format(target\_asset.name, target\_asset.status)).
- If target\_asset.docstatus equals 1.
  - Call the validation error handler Platform.throw(translated “Target Asset {0} cannot be submitted”.format(target\_asset.name)).
- Otherwise.
  - <a id="op-6b1d805e8bf056-guard-20"></a>If target\_asset.docstatus equals 2.
    - Call the validation error handler Platform.throw(translated “Target Asset {0} cannot be cancelled”.format(target\_asset.name)).
- If target\_asset.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Target Asset {0} does not belong to company {1}”.format(target\_asset.name, self.company)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison target\_asset.docstatus equals 2, target\_asset.docstatus = 2 (cancelled) selects the branch that calls the validation-error handler with translated “Target Asset {0} cannot be cancelled”.format(target\_asset.name). With target\_asset.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6b1d805e8bf056-guard-20)

**Methods declared on this owner** [get asset for validation](operations-008.md#op-5c32ee8cf35ef1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1451) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L350)
