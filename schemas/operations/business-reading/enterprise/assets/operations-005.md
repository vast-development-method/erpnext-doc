# Asset management · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset

[Record definition](../../../../data/record-types/asset.json)

<a id="op-de18fdaf685e16"></a>
### Create new depr schedule

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_create_new_depr_schedule`

**Inputs** current\_depr\_schedule\_doc, existing\_asset, new\_asset, is\_new\_asset, fb\_row.

**State and service calls** request copy\_doc for current\_depr\_schedule\_doc.

**Explicit results** new\_depr\_schedule\_doc.

**Local steps**

- Set new\_depr\_schedule\_doc from Platform.copy\_doc(current\_depr\_schedule\_doc).
- Set new\_depr\_schedule\_doc.asset\_doc from new\_asset when is\_new\_asset, otherwise existing\_asset.
  - Value choice on is\_new\_asset — true gives new\_asset, false gives existing\_asset.
- Set new\_depr\_schedule\_doc.fb\_row from fb\_row.
- Evaluate new\_depr\_schedule\_doc.fetch\_asset\_details().
- Return new\_depr\_schedule\_doc.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1310)

<a id="op-286a16bef2951b"></a>
### Update depreciation terms

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_update_depreciation_terms`

**Inputs** new\_depr\_schedule\_doc, scaling\_factor.

**Local steps**

- Set accumulated\_depreciation from flt(new\_depr\_schedule\_doc.opening\_accumulated\_depreciation).
- For each term in new\_depr\_schedule\_doc.get(“depreciation\_schedule”).
  - Set depreciation\_amount from flt((term.depreciation\_amount × scaling\_factor), term.precision(“depreciation\_amount”)).
  - Set term.depreciation\_amount from depreciation\_amount.
  - Set accumulated\_depreciation from flt((accumulated\_depreciation + depreciation\_amount), term.precision(“depreciation\_amount”)).
  - Set term.accumulated\_depreciation\_amount from accumulated\_depreciation.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1323)

<a id="op-5454e9bb244df8"></a>
### Add depr schedule notes

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_add_depr_schedule_notes`

**Inputs** new\_depr\_schedule\_doc, existing\_asset, new\_asset, is\_new\_asset.

**Local steps**

- Set notes from translated “This schedule was created when Asset {0} was {1} into new Asset {2}.”.format(get\_link\_to\_form(existing\_asset.doctype, existing\_asset.name), “split” when is\_new\_asset, otherwise “updated after b ….
  - Value choice on is\_new\_asset — true gives “split”, false gives “updated after being split”.
- Set new\_depr\_schedule\_doc.notes from notes.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L223) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L650) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1288)

<a id="op-903331afedd23b"></a>
### Add reference in jv on split

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_add_reference_in_jv_on_split`

**Inputs** entry\_name, new\_asset\_name, old\_asset\_name, depreciation\_amount.

**Record and data access** resolve a document from “Journal Entry” via get\_doc.

**State and service calls** call save on journal\_entry.

**Local steps**

- Set journal\_entry from Platform.get\_doc(“Journal Entry”, entry\_name).
- Set entries\_to\_add from list().
- Evaluate adjust\_existing\_accounts(journal\_entry, old\_asset\_name, depreciation\_amount, entries\_to\_add).
- Evaluate add\_new\_entries(journal\_entry, entries\_to\_add, new\_asset\_name, depreciation\_amount).
- Set journal\_entry.flags.ignore\_validate\_update\_after\_submit from true.
- Evaluate journal\_entry.save().
- Set journal\_entry.docstatus from 2.
- Evaluate journal\_entry.make\_gl\_entries(1).
- Set journal\_entry.docstatus from 1.
- Evaluate journal\_entry.make\_gl\_entries().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L225) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L652) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1290)

<a id="op-647434506b7463"></a>
### Adjust existing accounts

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_adjust_existing_accounts`

**Inputs** journal\_entry, old\_asset\_name, depreciation\_amount, entries\_to\_add.

**State and service calls** request copy\_doc for account.

**Local steps**

- For each account in journal\_entry.get(“accounts”).
  - If account.reference\_name equals old\_asset\_name.
    - Evaluate entries\_to\_add.append(Platform.copy\_doc(account).as\_dict()).
    - Evaluate adjust\_account\_balance(account, depreciation\_amount).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L227) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L654) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1292)

<a id="op-04b8c8e525c57c"></a>
### Adjust account balance

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_adjust_account_balance`

**Inputs** account, depreciation\_amount.

**Local steps**

- If account.credit.
  - Update account.credit using − depreciation\_amount.
  - Update account.credit\_in\_account\_currency using − (account.exchange\_rate × depreciation\_amount).
- Otherwise.
  - If account.debit.
    - Update account.debit using − depreciation\_amount.
    - Update account.debit\_in\_account\_currency using − (account.exchange\_rate × depreciation\_amount).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L226) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L653) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1291)

<a id="op-4a38a7cae0dc85"></a>
### Add new entries

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_add_new_entries`

**Inputs** journal\_entry, entries\_to\_add, new\_asset\_name, depreciation\_amount.

**Local steps**

- Set idx from (len(journal\_entry.get(“accounts”)) + 1).
- For each entry in entries\_to\_add.
  - Set entry.reference\_name from new\_asset\_name.
  - If entry.credit.
    - Set entry.credit from depreciation\_amount.
    - Set entry.credit\_in\_account\_currency from (entry.exchange\_rate × depreciation\_amount).
  - Otherwise.
    - If entry.debit.
      - Set entry.debit from depreciation\_amount.
      - Set entry.debit\_in\_account\_currency from (entry.exchange\_rate × depreciation\_amount).
  - Set entry.idx from idx.
  - Update idx using + 1.
  - Evaluate journal\_entry.append(“accounts”, entry).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L224) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L651) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1289)

<a id="op-b0d55565dcaed0"></a>
### Get data

`operation_enterprise_assets_record_definitions_asset_asset_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“non\_standard\_fieldnames” → mapping(“Asset Movement” → “asset”), “transactions” → list(mapping(“label” → translated “Movement”, “items” → list(“Asset Movement”)))).

**Local steps**

- Return mapping(“non\_standard\_fieldnames” → mapping(“Asset Movement” → “asset”), “transactions” → list(mapping(“label” → translated “Movement”, “items” → list(“Asset Movement”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L6404) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L260)

<a id="op-f1902f4cd14cde"></a>
### Post depreciation entries

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_post_depreciation_entries`

**Inputs** date = no value.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not cint(Platform.get\_single\_value(“Accounts Settings”, “book\_asset\_depreciation\_entry\_automatically”)).
  - Return no value.
- Set date from (date or today()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in date → today().
- Evaluate book\_depreciation\_entries(date).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “book\_asset\_depreciation\_entry\_automatically”) · clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L6541) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1534) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L414)

<a id="op-d3c896f9d158ca"></a>
### Book depreciation entries

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_book_depreciation_entries`

**Inputs** date.

**State and service calls** commit · rollback.

**Local steps**

- Set tuple(failed\_assets, error\_logs) from tuple(list(), list()).
- Set depreciable\_assets\_data from get\_depreciable\_assets\_data(date).
- Set accounting\_dimensions from get\_checks\_for\_pl\_and\_bs\_accounts().
- For each data in depreciable\_assets\_data.
  - Set tuple(depr\_schedule\_name, asset\_name, sch\_start\_idx, sch\_end\_idx) from data.
  - Attempt the following.
    - Evaluate \_make\_depreciation\_entry(depr\_schedule\_name, date, sch\_start\_idx, sch\_end\_idx, …).
    - If not Platform.in\_test.
      - Evaluate Platform.db.commit().
  - On failure (Exception) bound to e.
    - Evaluate Platform.db.rollback().
    - Evaluate failed\_assets.append(asset\_name).
    - Set error\_log from Platform.log\_error(e).
    - Evaluate error\_logs.append(error\_log.name).
- If failed\_assets.
  - Evaluate set\_depr\_entry\_posting\_status\_for\_failed\_assets(failed\_assets).
  - Evaluate notify\_depr\_entry\_posting\_error(failed\_assets, error\_logs).
- If not Platform.in\_test.
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L381)

<a id="op-e9f38fc65cb01c"></a>
### Get depreciable assets data

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_depreciable_assets_data`

**Inputs** date.

**Explicit results** res.run().

**Local steps**

- Set a from Platform.qb.DocType(“Asset”).
- Set ads from Platform.qb.DocType(“Asset Depreciation Schedule”).
- Set ds from Platform.qb.DocType(“Depreciation Schedule”).
- Set res from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.schedule\_date ≤ date).groupby(ads.name).orderby(a.creation, order = Order.desc).
- Set companies\_with\_frozen\_limits from get\_companies\_with\_frozen\_limits().
- For each tuple(company, frozen\_upto) in companies\_with\_frozen\_limits.items().
  - Set res from res.where((a.company differs from company bitwise or ds.schedule\_date &gt; frozen\_upto)).
- Return res.run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1516) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L396)

<a id="op-c0e51af53ac355"></a>
### Get companies with frozen limits

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_companies_with_frozen_limits`

**Inputs** no declared parameters.

**Record and data access** read “Company” via get\_all.

**Explicit results** companies\_with\_frozen\_limits.

**Local steps**

- Set companies\_with\_frozen\_limits from mapping().
- For each d in Platform.get\_all(“Company”, fields = list(“name”, “accounts\_frozen\_till\_date”, “role\_allowed\_for\_frozen\_entries”)).
  - If not d.accounts\_frozen\_till\_date.
    - Continue with the next iteration or loop test.
  - If (d.role\_allowed\_for\_frozen\_entries does not belong to Platform.get\_roles() and Platform.session.user differs from “Administrator”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.role\_allowed\_for\_frozen\_entries does not belong to Platform.get\_roles() → Platform.session.user differs from “Administrator”.
    - Set companies\_with\_frozen\_limits at d.name from getdate(d.accounts\_frozen\_till\_date).
- Return companies\_with\_frozen\_limits.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L1248) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1511) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L391)

<a id="op-b60038f296d875"></a>
### Make depreciation entry on disposal

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_make_depreciation_entry_on_disposal`

**Inputs** asset\_doc, disposal\_date = no value.

**Local steps**

- For each row in asset\_doc.get(“finance\_books”).
  - Set depr\_schedule\_name from get\_asset\_depr\_schedule\_name(asset\_doc.name, “Active”, row.finance\_book).
  - Evaluate \_make\_depreciation\_entry(depr\_schedule\_name, disposal\_date).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L1501) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1531) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L411)

<a id="op-95f16646c844ba"></a>
### Get credit debit accounts for asset

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_credit_debit_accounts_for_asset`

**Inputs** asset\_category, company.

**Explicit results** tuple(credit\_account, debit\_account).

**Local steps**

- Set tuple(\_, accumulated\_depr\_account, depr\_expense\_account) from get\_depreciation\_accounts(asset\_category, company).
- Set tuple(credit\_account, debit\_account) from get\_credit\_and\_debit\_accounts(accumulated\_depr\_account, depr\_expense\_account).
- Return tuple(credit\_account, debit\_account).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L1649) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1514) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L394)

<a id="op-28375fefe50a0a"></a>
### Get depreciation cost center and series

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_depreciation_cost_center_and_series`

**Inputs** asset.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(depreciation\_cost\_center, depreciation\_series).

**Local steps**

- Set tuple(depreciation\_cost\_center, depreciation\_series) from Platform.get\_cached\_value(“Company”, asset.company, list(“depreciation\_cost\_center”, “series\_for\_depreciation\_entry”)).
- Set depreciation\_cost\_center from (asset.cost\_center or depreciation\_cost\_center).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in asset.cost\_center → depreciation\_cost\_center.
- Return tuple(depreciation\_cost\_center, depreciation\_series).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, asset.company, list(“depreciation\_cost\_center”, “series\_for\_depreciation\_entry”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L1787) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1519) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L399)

<a id="op-fa9f0475bf4a3b"></a>
### Get depr cost center and series

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_depr_cost_center_and_series`

**Inputs** no declared parameters.

**Record and data access** read “Company” via get\_all · read “Company” via get\_cached\_value.

**Explicit results** res.

**Local steps**

- Set company\_names from Platform.db.get\_all(“Company”, pluck = “name”).
- Set res from mapping().
- For each company\_name in company\_names.
  - Set tuple(depreciation\_cost\_center, depreciation\_series) from Platform.get\_cached\_value(“Company”, company\_name, list(“depreciation\_cost\_center”, “series\_for\_depreciation\_entry”)).
  - Evaluate res.setdefault(company\_name, tuple(depreciation\_cost\_center, depreciation\_series)).
- Return res.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company\_name, list(“depreciation\_cost\_center”, “series\_for\_depreciation\_entry”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L1935) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1515) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L395)

<a id="op-92b223402b930e"></a>
### Make depreciation entry

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_make_depreciation_entry`

**Inputs** depr\_schedule\_name, date = no value, sch\_start\_idx = no value, sch\_end\_idx = no value, accounting\_dimensions = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Asset Depreciation Schedule” via get\_doc.

**Explicit results** \_make\_depreciation\_entry(depr\_schedule\_name, date, sch\_start\_idx, sch\_end\_idx, …).

**Local steps**

- Set depr\_schedule\_doc from Platform.get\_doc(“Asset Depreciation Schedule”, depr\_schedule\_name).
- Evaluate Platform.has\_permission(“Asset Depreciation Schedule”, “write”, depr\_schedule\_doc, throw = true).
- Evaluate Platform.has\_permission(“Asset”, “write”, depr\_schedule\_doc.asset, throw = true).
- Evaluate Platform.has\_permission(“Journal Entry”, throw = true).
- Return \_make\_depreciation\_entry(depr\_schedule\_name, date, sch\_start\_idx, sch\_end\_idx, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset Depreciation Schedule”, “write”, depr\_schedule\_doc, throw = true), Platform.has\_permission(“Asset”, “write”, depr\_schedule\_doc.asset, throw = true) and 1 further calls.

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1529) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L409)

<a id="op-6fff88ae89796e"></a>
### Make depreciation entry

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_make_depreciation_entry_2`

**Inputs** depr\_schedule\_name, date = no value, sch\_start\_idx = no value, sch\_end\_idx = no value, accounting\_dimensions = no value.

**Record and data access** resolve a document from “Asset Depreciation Schedule” via get\_doc · resolve a document from “Asset” via get\_doc.

**State and service calls** call db\_set on asset.

**Explicit results** depr\_schedule\_doc.

**Explicit failure paths** depr\_posting\_error.

**Local steps**

- Set date from (date or today()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in date → today().
- Set depr\_schedule\_doc from Platform.get\_doc(“Asset Depreciation Schedule”, depr\_schedule\_name).
- Set asset from Platform.get\_doc(“Asset”, depr\_schedule\_doc.asset).
- Set tuple(credit\_account, debit\_account) from get\_credit\_debit\_accounts\_for\_asset(asset.asset\_category, asset.company).
- Set tuple(depr\_cost\_center, depr\_series) from get\_depreciation\_cost\_center\_and\_series(asset).
- Set accounting\_dimensions from (accounting\_dimensions or get\_checks\_for\_pl\_and\_bs\_accounts()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in accounting\_dimensions → get\_checks\_for\_pl\_and\_bs\_accounts().
- Set depr\_posting\_error from no value.
- For each d in depr\_schedule\_doc.get(“depreciation\_schedule”) at slice (sch\_start\_idx or 0) to (sch\_end\_idx or len(depr\_schedule\_doc.get(“depreciation\_schedule”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sch\_start\_idx → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sch\_end\_idx → len(depr\_schedule\_doc.get(“depreciation\_schedule”)).
  - Attempt the following.
    - Evaluate \_make\_journal\_entry\_for\_depreciation(depr\_schedule\_doc, asset, date, d, …).
  - On failure (Exception) bound to e.
    - Set depr\_posting\_error from e.
- Evaluate asset.reload().
- Evaluate asset.set\_status().
- If not depr\_posting\_error.
  - Evaluate asset.db\_set(“depr\_entry\_posting\_status”, “Successful”).
  - Evaluate depr\_schedule\_doc.reload().
  - Return depr\_schedule\_doc.
- Raise depr\_posting\_error.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1530) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L410)

<a id="op-bfdd471f84b36f"></a>
### Make journal entry for depreciation

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_make_journal_entry_for_depreciation`

**Inputs** depr\_schedule\_doc, asset, date, depr\_schedule, depr\_cost\_center, depr\_series, credit\_account, debit\_account, accounting\_dimensions.

**State and service calls** request new\_doc for “Journal Entry” · call save on je · call submit on je.

**Explicit results** no value.

**Local steps**

- If (depr\_schedule.journal\_entry or getdate(depr\_schedule.schedule\_date) &gt; getdate(date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in depr\_schedule.journal\_entry → getdate(depr\_schedule.schedule\_date) &gt; getdate(date).
  - Return no value.
- Set je from Platform.new\_doc(“Journal Entry”).
- Evaluate setup\_journal\_entry\_metadata(je, depr\_schedule\_doc, depr\_series, depr\_schedule, …).
- Set tuple(credit\_entry, debit\_entry) from get\_credit\_and\_debit\_entry(credit\_account, depr\_schedule, asset, depr\_cost\_center, …).
- Evaluate je.append(“accounts”, credit\_entry).
- Evaluate je.append(“accounts”, debit\_entry).
- Set je.flags.ignore\_permissions from true.
- Evaluate je.save().
- If not je.meta.get\_workflow().
  - Evaluate je.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1532) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L412)

<a id="op-541f0304676cbb"></a>
### Setup journal entry metadata

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_setup_journal_entry_metadata`

**Inputs** je, depr\_schedule\_doc, depr\_series, depr\_schedule, asset.

**Local steps**

- Set je.voucher\_type from “Depreciation Entry”.
- If depr\_series.
  - Set je.naming\_series from depr\_series.
- Set je.posting\_date from depr\_schedule.schedule\_date.
- Set je.company from asset.company.
- Set je.finance\_book from depr\_schedule\_doc.finance\_book.
- Set je.remark from translated “Depreciation Entry against {0} worth {1}”.format(asset.name, depr\_schedule.depreciation\_amount).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L3774) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L420)

<a id="op-e58b70028cc8ef"></a>
### Get credit and debit entry

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_credit_and_debit_entry`

**Inputs** credit\_account, depr\_schedule, asset, depr\_cost\_center, debit\_account, dimensions.

**Explicit results** tuple(credit\_entry, debit\_entry).

**Local steps**

- Set credit\_entry from mapping(“account” → credit\_account, “credit\_in\_account\_currency” → depr\_schedule.depreciation\_amount, “reference\_type” → “Asset”, “reference\_name” → asset.name, …).
- Set debit\_entry from mapping(“account” → debit\_account, “debit\_in\_account\_currency” → depr\_schedule.depreciation\_amount, “reference\_type” → “Asset”, “reference\_name” → asset.name, …).
- For each dimension in dimensions.
  - Set value from asset.get(dimension at “fieldname”).
  - Set is\_asset\_company from dimension.get(“company”) equals asset.company.
  - If (value or (is\_asset\_company and dimension.get(“mandatory\_for\_bs”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → (is\_asset\_company and dimension.get(“mandatory\_for\_bs”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_asset\_company → dimension.get(“mandatory\_for\_bs”).
    - Set credit\_entry at dimension at “fieldname” from (value or dimension.get(“default\_dimension”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → dimension.get(“default\_dimension”).
  - If (value or (is\_asset\_company and dimension.get(“mandatory\_for\_pl”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → (is\_asset\_company and dimension.get(“mandatory\_for\_pl”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_asset\_company → dimension.get(“mandatory\_for\_pl”).
    - Set debit\_entry at dimension at “fieldname” from (value or dimension.get(“default\_dimension”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → dimension.get(“default\_dimension”).
- Return tuple(credit\_entry, debit\_entry).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1513) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L393)

<a id="op-c7ebd70dcbc31b"></a>
### Get credit and debit accounts

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_credit_and_debit_accounts`

**Inputs** accumulated\_depreciation\_account, depreciation\_expense\_account.

**Record and data access** read “Account” via get\_value.

**Explicit results** tuple(credit\_account, debit\_account).

**Explicit failure paths** validation helper — translated “Depreciation Expense Account should be an Income or Expense Account.”.

**Local steps**

- Set root\_type from Platform.get\_value(“Account”, depreciation\_expense\_account, “root\_type”).
- If root\_type equals “Expense”.
  - Set credit\_account from accumulated\_depreciation\_account.
  - Set debit\_account from depreciation\_expense\_account.
- Otherwise.
  - If root\_type equals “Income”.
    - Set credit\_account from depreciation\_expense\_account.
    - Set debit\_account from accumulated\_depreciation\_account.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Depreciation Expense Account should be an Income or Expense Account.”).
- Return tuple(credit\_account, debit\_account).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L4631) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1512) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L392)

<a id="op-cc6e9628aa7dd7"></a>
### Set depr entry posting status for failed assets

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_set_depr_entry_posting_status_for_failed_assets`

**Inputs** failed\_asset\_names.

**State and service calls** request set\_value on “Asset”.

**Local steps**

- For each asset\_name in failed\_asset\_names.
  - Evaluate Platform.db.set\_value(“Asset”, asset\_name, “depr\_entry\_posting\_status”, “Failed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L4871) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L419)

<a id="op-f28107d63de456"></a>
### Notify depr entry posting error

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_notify_depr_entry_posting_error`

**Inputs** failed\_asset\_names, error\_log\_names.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**State and service calls** sendmail.

**Local steps**

- Set user\_role from Platform.db.get\_single\_value(“Accounts Settings”, “role\_to\_notify\_on\_depreciation\_failure”).
- Set recipients from get\_users\_with\_role((user\_role or “Accounts Manager”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_role → “Accounts Manager”.
- If not recipients.
  - Set recipients from get\_users\_with\_role(“System Manager”).
- Set subject from translated “Error while posting depreciation entries”.
- Set asset\_links from get\_comma\_separated\_links(failed\_asset\_names, “Asset”).
- Set error\_log\_links from get\_comma\_separated\_links(error\_log\_names, “Error Log”).
- Set message from get\_message\_for\_depr\_entry\_posting\_error(asset\_links, error\_log\_links).
- Evaluate Platform.sendmail(recipients = recipients, subject = subject, message = message).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Accounts Settings”, “role\_to\_notify\_on\_depreciation\_failure”) · service or queued work from Platform.sendmail(recipients = recipients, subject = subject, message = message).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L4966) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1533) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L413)
