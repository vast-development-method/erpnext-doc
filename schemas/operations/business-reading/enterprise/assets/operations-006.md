# Asset management · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset

[Record definition](../../../../data/record-types/asset.json)

<a id="op-868b68388b9a21"></a>
### Get comma separated links

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_comma_separated_links`

**Inputs** names, doctype.

**Explicit results** links.

**Local steps**

- Set links from list().
- For each name in names.
  - Evaluate links.append(get\_link\_to\_form(doctype, name)).
- Set links from “, ”.join(links).
- Return links.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L5304) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1510) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L390)

<a id="op-f9794d22d4bfab"></a>
### Get message for depr entry posting error

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_message_for_depr_entry_posting_error`

**Inputs** asset\_links, error\_log\_links.

**Explicit results** (((((((nested operand in the contract + nested operand in the contract) + “.”) + text in the contract) + nested operand in the contract(nested operand in the contract).format(error\_log\_links)) + “.”) + tex ….

**Local steps**

- Return (((((((nested operand in the contract + nested operand in the contract) + “.”) + text in the contract) + nested operand in the contract(nested operand in the contract).format(error\_log\_links)) + “.”) + tex ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L5448) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1524) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L404)

<a id="op-c6af439afc457d"></a>
### Scrap asset

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_scrap_asset`

**Inputs** asset\_name, scrap\_date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Asset” via get\_doc.

**State and service calls** call db\_set on asset.

**Local steps**

- Evaluate Platform.has\_permission(“Asset”, “write”, asset\_name, throw = true).
- Evaluate Platform.has\_permission(“Journal Entry”, “submit”, throw = true).
- Set asset from Platform.get\_doc(“Asset”, asset\_name).
- Set scrap\_date from (getdate(scrap\_date) or getdate(today())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate(scrap\_date) → getdate(today()).
- Evaluate asset.db\_set(“disposal\_date”, scrap\_date).
- Evaluate validate\_asset\_for\_scrap(asset, scrap\_date).
- Evaluate depreciate\_asset(asset, scrap\_date, get\_note\_for\_scrap(asset)).
- Evaluate asset.reload().
- Evaluate create\_journal\_entry\_for\_scrap(asset, scrap\_date).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset”, “write”, asset\_name, throw = true), Platform.has\_permission(“Journal Entry”, “submit”, throw = true) · clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, effective access, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L418)

<a id="op-308e5f03d522db"></a>
### Validate asset for scrap

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_validate_asset_for_scrap`

**Inputs** asset, scrap\_date.

**Explicit failure paths** validation helper — translated “Asset {0} must be submitted”.format(asset.name) · validation helper — translated “Asset {0} cannot be scrapped, as it is already {1}”.format(asset.name, asset.status).

**Local steps**

- If asset.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Asset {0} must be submitted”.format(asset.name)).
- Otherwise.
  - If asset.status belongs to tuple(“Cancelled”, “Sold”, “Scrapped”, “Capitalized”).
    - Call the validation error handler Platform.throw(translated “Asset {0} cannot be scrapped, as it is already {1}”.format(asset.name, asset.status)).
- Evaluate validate\_scrap\_date(asset, scrap\_date).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L6014) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1542) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L422)

<a id="op-017ebcd9ba3869"></a>
### Validate scrap date

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_validate_scrap_date`

**Inputs** asset, scrap\_date.

**Explicit failure paths** validation helper — translated “Future date is not allowed” · validation helper — translated “Scrap date cannot be before purchase date” · validation helper — translated “Asset cannot be scrapped before the last depreciation entry.”.

**Local steps**

- If scrap\_date &gt; getdate().
  - Call the validation error handler Platform.throw(translated “Future date is not allowed”).
- Otherwise.
  - If scrap\_date &lt; getdate(asset.purchase\_date).
    - Call the validation error handler Platform.throw(translated “Scrap date cannot be before purchase date”).
- If asset.calculate\_depreciation.
  - Set last\_booked\_depreciation\_date from get\_last\_depreciation\_date(asset.name).
  - If (last\_booked\_depreciation\_date and scrap\_date &lt; last\_booked\_depreciation\_date and scrap\_date &gt; getdate(asset.purchase\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_booked\_depreciation\_date → scrap\_date &lt; last\_booked\_depreciation\_date → scrap\_date &gt; getdate(asset.purchase\_date).
    - Call the validation error handler Platform.throw(translated “Asset cannot be scrapped before the last depreciation entry.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0310.json#L6275) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1544) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L424)

<a id="op-03889014ffc5d5"></a>
### Get last depreciation date

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_last_depreciation_date`

**Inputs** asset\_name, finance\_book = no value.

**Explicit results** last\_depreciation\_date at 0 at 0 when last\_depreciation\_date, otherwise no value.

**Local steps**

- Set depreciation from Platform.qb.DocType(“Asset Depreciation Schedule”).
- Set depreciation\_schedule from Platform.qb.DocType(“Depreciation Schedule”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.journal\_entry differs from empty text).orderby(depreciation\_schedule.schedule\_date, order = Order.desc).limit(1).
- If finance\_book.
  - Set query from query.where(depreciation.finance\_book equals finance\_book).
- Set last\_depreciation\_date from query.run().
- Return last\_depreciation\_date at 0 at 0 when last\_depreciation\_date, otherwise no value.
  - Value choice on last\_depreciation\_date — true gives last\_depreciation\_date at 0 at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1523) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L403)

<a id="op-6f16ebb757b0aa"></a>
### Get note for scrap

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_note_for_scrap`

**Inputs** asset.

**Explicit results** translated “This schedule was created when Asset {0} was scrapped.”.format(get\_link\_to\_form(asset.doctype, asset.name)).

**Local steps**

- Return translated “This schedule was created when Asset {0} was scrapped.”.format(get\_link\_to\_form(asset.doctype, asset.name)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1526) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L406)

<a id="op-96a29fb792d79e"></a>
### Create journal entry for scrap

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_create_journal_entry_for_scrap`

**Inputs** asset, scrap\_date.

**Record and data access** read “Company” via get\_cached\_value.

**State and service calls** request new\_doc for “Journal Entry” · call save on je · call submit on je · msgprint with translated “Asset scrapped via Journal Entry {0}”.format(get\_link\_to\_form(“Journal Entry”, je.name)).

**Local steps**

- Set depreciation\_series from Platform.get\_cached\_value(“Company”, asset.company, “series\_for\_depreciation\_entry”).
- Set je from Platform.new\_doc(“Journal Entry”).
- Set je.voucher\_type from “Asset Disposal”.
- Set je.naming\_series from depreciation\_series.
- Set je.posting\_date from scrap\_date.
- Set je.company from asset.company.
- Set je.remark from formatted text Scrap Entry for asset {asset.name}.
- For each entry in get\_gl\_entries\_on\_asset\_disposal(asset, scrap\_date).
  - Evaluate entry.update(mapping(“reference\_type” → “Asset”, “reference\_name” → asset.name)).
  - Evaluate je.append(“accounts”, entry).
- Set je.flags.ignore\_permissions from true.
- Evaluate je.save().
- If not je.meta.get\_workflow().
  - Evaluate je.submit().
- Evaluate add\_asset\_activity(asset.name, translated “Asset scrapped”).
- Evaluate Platform.msgprint(translated “Asset scrapped via Journal Entry {0}”.format(get\_link\_to\_form(“Journal Entry”, je.name))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, asset.company, “series\_for\_depreciation\_entry”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1504) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L384)

<a id="op-d9e78ddfc65478"></a>
### Restore asset

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_restore_asset`

**Inputs** asset\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Asset” via get\_doc.

**Explicit failure paths** validation helper — translated “Asset {0} cannot be restored, as it is not scrapped”.format(asset\_name).

**Local steps**

- Evaluate Platform.has\_permission(“Asset”, “write”, asset\_name, throw = true).
- Set asset from Platform.get\_doc(“Asset”, asset\_name).
- If not asset.journal\_entry\_for\_scrap.
  - Call the validation error handler Platform.throw(translated “Asset {0} cannot be restored, as it is not scrapped”.format(asset\_name)).
- Evaluate reverse\_depreciation\_entry\_made\_on\_disposal(asset).
- Evaluate reset\_depreciation\_schedule(asset, get\_note\_for\_restore(asset)).
- Evaluate cancel\_journal\_entry\_for\_scrap(asset).
- Evaluate asset.set\_status().
- Evaluate add\_asset\_activity(asset\_name, translated “Asset restored”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset”, “write”, asset\_name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L416)

<a id="op-1fd14cd8dda313"></a>
### Get note for restore

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_note_for_restore`

**Inputs** asset.

**Explicit results** translated “This schedule was created when Asset {0} was restored.”.format(get\_link\_to\_form(asset.doctype, asset.name)).

**Local steps**

- Return translated “This schedule was created when Asset {0} was restored.”.format(get\_link\_to\_form(asset.doctype, asset.name)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L969) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1525) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L405)

<a id="op-4a121f8bbd6ae0"></a>
### Cancel journal entry for scrap

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_cancel_journal_entry_for_scrap`

**Inputs** asset.

**Record and data access** resolve a document from “Journal Entry” via get\_doc.

**State and service calls** call db\_set on asset · call cancel on Platform.get\_doc(“Journal Entry”, je).

**Local steps**

- If asset.journal\_entry\_for\_scrap.
  - Set je from asset.journal\_entry\_for\_scrap.
  - Evaluate asset.db\_set(“disposal\_date”, no value).
  - Evaluate asset.db\_set(“journal\_entry\_for\_scrap”, no value).
  - Evaluate Platform.get\_doc(“Journal Entry”, je).cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L1066) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1503) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L383)

<a id="op-ddc4870964e260"></a>
### Depreciate asset

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_depreciate_asset`

**Inputs** asset\_doc, date, notes.

**Explicit results** no value.

**Local steps**

- If not asset\_doc.calculate\_depreciation.
  - Return no value.
- Evaluate reschedule\_depreciation(asset\_doc, notes, disposal\_date = date).
- Evaluate make\_depreciation\_entry\_on\_disposal(asset\_doc, date).
- Evaluate asset\_doc.reload().
- Evaluate cancel\_depreciation\_entries(asset\_doc, date).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L1232) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1506) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L386)

<a id="op-ce8272dc9e9b6c"></a>
### Cancel depreciation entries

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_cancel_depreciation_entries`

**Inputs** asset\_doc, date.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L1406) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1502) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L382)

<a id="op-da033bc15dece1"></a>
### Reset depreciation schedule

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_reset_depreciation_schedule`

**Inputs** asset\_doc, notes.

**Local steps**

- If asset\_doc.calculate\_depreciation.
  - Evaluate reschedule\_depreciation(asset\_doc, notes).
  - Evaluate asset\_doc.set\_total\_booked\_depreciations().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L1455) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L415)

<a id="op-57488f37b05acf"></a>
### Reverse depreciation entry made on disposal

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_reverse_depreciation_entry_made_on_disposal`

**Inputs** asset.

**Local steps**

- For each row in asset.get(“finance\_books”).
  - Set schedule\_doc from get\_asset\_depr\_schedule\_doc(asset.name, “Active”, row.finance\_book).
  - If (not schedule\_doc or not schedule\_doc.get(“depreciation\_schedule”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not schedule\_doc → not schedule\_doc.get(“depreciation\_schedule”).
    - Continue with the next iteration or loop test.
  - For each tuple(schedule\_idx, schedule) in enumerate(schedule\_doc.get(“depreciation\_schedule”)).
    - If (schedule.schedule\_date equals asset.disposal\_date and schedule.journal\_entry).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in schedule.schedule\_date equals asset.disposal\_date → schedule.journal\_entry.
      - If (not disposal\_was\_made\_on\_original\_schedule\_date(schedule\_idx, row, asset.disposal\_date) or disposal\_happens\_in\_the\_future(asset.disposal\_date)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not disposal\_was\_made\_on\_original\_schedule\_date(schedule\_idx, row, asset.disposal\_date) → disposal\_happens\_in\_the\_future(asset.disposal\_date).
        - Set je from create\_reverse\_depreciation\_entry(asset.name, schedule.journal\_entry).
        - Evaluate update\_value\_after\_depreciation\_on\_asset\_restore(schedule, row, je).
- Evaluate asset.sync\_value\_after\_depreciation().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L417)

<a id="op-8b82bc9b8a1391"></a>
### Disposal was made on original schedule date

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_disposal_was_made_on_original_schedule_date`

**Inputs** schedule\_idx, row, disposal\_date.

**Explicit results** true · false.

**Local steps**

- Set orginal\_schedule\_date from add\_months(row.depreciation\_start\_date, (schedule\_idx × cint(row.frequency\_of\_depreciation))).
- If is\_last\_day\_of\_the\_month(row.depreciation\_start\_date).
  - Set orginal\_schedule\_date from get\_last\_day(orginal\_schedule\_date).
- If orginal\_schedule\_date equals disposal\_date.
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L1954) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1508) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L388)

<a id="op-037b9b381c4899"></a>
### Disposal happens in the future

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_disposal_happens_in_the_future`

**Inputs** disposal\_date.

**Explicit results** true · false.

**Local steps**

- If disposal\_date &gt; getdate().
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L2151) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1507) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L387)

<a id="op-f35dcd80a2492b"></a>
### Create reverse depreciation entry

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_create_reverse_depreciation_entry`

**Inputs** asset\_name, journal\_entry.

**State and service calls** call submit on reverse\_journal\_entry.

**Explicit results** reverse\_journal\_entry.

**Explicit failure paths** validation helper — translated “Please disable workflow temporarily for Journal Entry {0}”.format(reverse\_journal\_entry.name).

**Local steps**

- Set reverse\_journal\_entry from map\_reverse\_journal\_entry(journal\_entry, ignore\_permissions = true).
- Set reverse\_journal\_entry.posting\_date from nowdate().
- For each account in reverse\_journal\_entry.accounts.
  - Evaluate account.update(mapping(“reference\_type” → “Asset”, “reference\_name” → asset\_name)).
- Set Platform.flags.is\_reverse\_depr\_entry from true.
- If not reverse\_journal\_entry.meta.get\_workflow().
  - Set reverse\_journal\_entry.flags.ignore\_permissions from true.
  - Evaluate reverse\_journal\_entry.submit().
  - Return reverse\_journal\_entry.
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Please disable workflow temporarily for Journal Entry {0}”.format(reverse\_journal\_entry.name)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1505) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L385)

<a id="op-30fa17ef662a74"></a>
### Update value after depreciation on asset restore

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_update_value_after_depreciation_on_asset_restore`

**Inputs** schedule, row, journal\_entry.

**State and service calls** request set\_value on “Depreciation Schedule” · call db\_set on row.

**Local steps**

- Evaluate Platform.db.set\_value(“Depreciation Schedule”, schedule.name, “journal\_entry”, no value, update\_modified = false).
- Set depreciation\_amount from get\_depreciation\_amount\_in\_je(journal\_entry).
- Set value\_after\_depreciation from flt((row.value\_after\_depreciation + depreciation\_amount), row.precision(“value\_after\_depreciation”)).
- Evaluate row.db\_set(“value\_after\_depreciation”, value\_after\_depreciation).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L2536) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1541) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L421)

<a id="op-b24ccb52f88c06"></a>
### Get depreciation amount in je

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_depreciation_amount_in_je`

**Inputs** journal\_entry.

**Explicit results** journal\_entry.accounts at 0.debit\_in\_account\_currency · journal\_entry.accounts at 0.credit\_in\_account\_currency.

**Local steps**

- If journal\_entry.accounts at 0.debit\_in\_account\_currency.
  - Return journal\_entry.accounts at 0.debit\_in\_account\_currency.
- Otherwise.
  - Return journal\_entry.accounts at 0.credit\_in\_account\_currency.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0311.json#L2767) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1518) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L398)

<a id="op-9d5a8f049a6863"></a>
### Get gl entries on asset regain

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_general_ledger_entries_on_asset_regain`

**Inputs** asset, selling\_amount = 0, finance\_book = no value, voucher\_type = no value, voucher\_no = no value, date = no value, disposal\_values = no value.

**Explicit results** gl\_entries.

**Local steps**

- If not date.
  - Set date from getdate().
- Set tuple(fixed\_asset\_account, asset, depreciation\_cost\_center, accumulated\_depr\_account, …) from get\_asset\_details(asset, finance\_book, disposal\_values).
- Set gl\_entries from list(asset.get\_gl\_dict(mapping(“account” → fixed\_asset\_account, “debit\_in\_account\_currency” → gross\_asset\_value, “debit” → gross\_asset\_value, “cost\_center” → depreciation\_cost\_center, …), item = asset), as ….
- Set profit\_amount from (abs(flt(value\_after\_depreciation)) − abs(flt(selling\_amount))).
- If profit\_amount.
  - Evaluate get\_profit\_gl\_entries(asset, profit\_amount, gl\_entries, disposal\_account, …).
- If (voucher\_type and voucher\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_type → voucher\_no.
  - For each entry in gl\_entries.
    - Set entry at “voucher\_type” from voucher\_type.
    - Set entry at “voucher\_no” from voucher\_no.
- Return gl\_entries.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1522) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L402)

<a id="op-24033c800ff26c"></a>
### Get gl entries on asset disposal

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_general_ledger_entries_on_asset_disposal`

**Inputs** asset, selling\_amount = 0, finance\_book = no value, voucher\_type = no value, voucher\_no = no value, date = no value, disposal\_values = no value.

**Explicit results** gl\_entries.

**Local steps**

- If not date.
  - Set date from getdate().
- Set tuple(fixed\_asset\_account, asset, depreciation\_cost\_center, accumulated\_depr\_account, …) from get\_asset\_details(asset, finance\_book, disposal\_values).
- Set gl\_entries from list(asset.get\_gl\_dict(mapping(“account” → fixed\_asset\_account, “credit\_in\_account\_currency” → gross\_asset\_value, “credit” → gross\_asset\_value, “cost\_center” → depreciation\_cost\_center, …), item = asset)).
- If accumulated\_depr\_amount.
  - Evaluate gl\_entries.append(asset.get\_gl\_dict(mapping(“account” → accumulated\_depr\_account, “debit\_in\_account\_currency” → accumulated\_depr\_amount, “debit” → accumulated\_depr\_amount, “cost\_center” → depreciation\_cost ….
- Set profit\_amount from (flt(selling\_amount) − flt(value\_after\_depreciation)).
- If profit\_amount.
  - Evaluate get\_profit\_gl\_entries(asset, profit\_amount, gl\_entries, disposal\_account, …).
- If (voucher\_type and voucher\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_type → voucher\_no.
  - For each entry in gl\_entries.
    - Set entry at “voucher\_type” from voucher\_type.
    - Set entry at “voucher\_no” from voucher\_no.
- Return gl\_entries.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1521) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L401)

<a id="op-1ad7b51e6e39c9"></a>
### Get asset details

`operation_enterprise_assets_record_definitions_asset_depreciation_business_behavior_get_asset_details`

**Inputs** asset, finance\_book = no value, disposal\_values = no value.

**Explicit results** tuple(fixed\_asset\_account, asset, depreciation\_cost\_center, accumulated\_depr\_account, …).

**Local steps**

- Set disposal\_values from (disposal\_values or get\_asset\_disposal\_values(asset, finance\_book)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in disposal\_values → get\_asset\_disposal\_values(asset, finance\_book).
- Set value\_after\_depreciation from flt(disposal\_values at “value\_after\_depreciation”).
- Set gross\_asset\_value from flt(disposal\_values at “gross\_asset\_value”).
- Set accumulated\_depr\_amount from flt((gross\_asset\_value − flt(value\_after\_depreciation)), asset.precision(“net\_purchase\_amount”)).
- Set tuple(fixed\_asset\_account, accumulated\_depr\_account, \_) from get\_depreciation\_accounts(asset.asset\_category, asset.company).
- Set tuple(disposal\_account, depreciation\_cost\_center) from \_get\_disposal\_account\_and\_cost\_center(asset.company).
- Set depreciation\_cost\_center from (asset.cost\_center or depreciation\_cost\_center).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in asset.cost\_center → depreciation\_cost\_center.
- Return tuple(fixed\_asset\_account, asset, depreciation\_cost\_center, accumulated\_depr\_account, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1509) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L389)

<a id="op-6b619b1aece444"></a>
### Get asset disposal values

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_get_asset_disposal_values`

**Inputs** asset, finance\_book = no value.

**Declared result** dict.

**Explicit results** mapping(“value\_after\_depreciation” → asset.get\_value\_after\_depreciation(finance\_book), “gross\_asset\_value” → get\_gross\_asset\_value(asset, finance\_book)).

**Local steps**

- Return mapping(“value\_after\_depreciation” → asset.get\_value\_after\_depreciation(finance\_book), “gross\_asset\_value” → get\_gross\_asset\_value(asset, finance\_book)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L709) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1347)
