# Accounting and settlement · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Asset depreciations and balances

<a id="op-1a3385d48c1688"></a>
### Get asset value adjustment map by category

`operation_enterprise_accounts_report_asset_depreciations_and_balances_business_behavior_get_asset_value_adjustment_map_by_category`

**Inputs** filters.

**Explicit results** mapping of row.pop(“asset\_category”) → row for row drawn from asset\_value\_adjustments.

**Local steps**

- Set asset from Platform.qb.DocType(“Asset”).
- Set gl\_entry from Platform.qb.DocType(“GL Entry”).
- Set asset\_category\_account from Platform.qb.DocType(“Asset Category Account”).
- Set asset\_value\_adjustments from nested operand in the contract(nested operand in the contract).where(get\_finance\_book\_condition(gl\_entry, filters)).groupby(asset.asset\_category).run(as\_dict = true).
- Return mapping of row.pop(“asset\_category”) → row for row drawn from asset\_value\_adjustments.
  - Draw row from asset\_value\_adjustments.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L294) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L653)

<a id="op-a790b7849445ad"></a>
### Get group by asset data

`operation_enterprise_accounts_report_asset_depreciations_and_balances_business_behavior_get_group_by_asset_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set asset\_details from get\_asset\_details\_for\_grouped\_by\_category(filters).
- Set assets from get\_assets\_for\_grouped\_by\_asset(filters).
- Set asset\_value\_adjustment\_map from get\_asset\_value\_adjustment\_map(filters).
- For each asset\_detail in asset\_details.
  - Set row from Platform.\_dict().
  - Evaluate row.update(asset\_detail).
  - Evaluate row.update(next(generator of asset for asset drawn from assets where asset at “asset” equals asset\_detail.get(“name”, empty text))).
    - Draw asset from assets, keep a combination only if (asset at “asset” equals asset\_detail.get(“name”, empty text)).
  - Evaluate apply\_value\_adjustments(row, asset\_value\_adjustment\_map.get(asset\_detail.get(“name”, empty text), mapping())).
  - Set row.value\_as\_on\_to\_date from (((((flt(nested operand in the contract.value\_as\_on\_from\_date) + flt(nested operand in the contract.value\_of\_new\_purchase)) − flt(row.value\_of\_sold\_asset)) − flt(row.value\_of\_scrapped\_asset)) − flt(row.val ….
  - Set row.accumulated\_depreciation\_as\_on\_to\_date from (((flt(row.accumulated\_depreciation\_as\_on\_from\_date) + flt(row.depreciation\_amount\_during\_the\_period)) − flt(row.depreciation\_eliminated\_during\_the\_period)) − flt(row.depreciation\_eliminated\_via\_reversal)).
  - Set row.net\_asset\_value\_as\_on\_from\_date from (flt(row.value\_as\_on\_from\_date) − flt(row.accumulated\_depreciation\_as\_on\_from\_date)).
  - Set row.net\_asset\_value\_as\_on\_to\_date from (flt(row.value\_as\_on\_to\_date) − flt(row.accumulated\_depreciation\_as\_on\_to\_date)).
  - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L300) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L659)

<a id="op-afaa8b19d9725f"></a>
### Get asset details for grouped by category

`operation_enterprise_accounts_report_asset_depreciations_and_balances_business_behavior_get_asset_details_for_grouped_by_category`

**Inputs** filters.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set asset from Platform.qb.DocType(“Asset”).
- Set asset\_depreciation\_schedule from Platform.qb.DocType(“Asset Depreciation Schedule”).
- Set asset\_capitalization\_asset\_item from Platform.qb.DocType(“Asset Capitalization Asset Item”).
- Set asset\_capitalization from Platform.qb.DocType(“Asset Capitalization”).
- Set disposal\_in\_period from ((IfNull(asset.disposal\_date, 0) differs from 0 bitwise and asset.disposal\_date ≥ filters.from\_date) bitwise and asset.disposal\_date ≤ filters.to\_date).
- Set capitalized\_before\_from\_date from nested operand in the contract(nested operand in the contract).select(asset\_capitalization\_asset\_item.asset).where(asset\_capitalization.posting\_date &lt; filters.from\_date).where(asset\_capitalization.docstatu ….
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.notin(capitalized\_before\_from\_date)).where(asset.name.isin(nested operand in the contract.qb.get\_query(“A ….
- If filters.get(“asset”).
  - Set query from query.where(asset.name equals filters.get(“asset”)).
- If filters.get(“finance\_book”).
  - Set assets\_with\_finance\_book from nested operand in the contract.qb.from\_(asset\_depreciation\_schedule).select(asset\_depreciation\_schedule.asset).where(asset\_depreciation\_schedule.finance\_book equals filters.get(“finance\_book”)).
  - Set query from query.where(asset.name.isin(assets\_with\_finance\_book)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L292) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L651)

<a id="op-f99e2acef98bf3"></a>
### Get assets for grouped by asset

`operation_enterprise_accounts_report_asset_depreciations_and_balances_business_behavior_get_assets_for_grouped_by_asset`

**Inputs** filters.

**Explicit results** list(combined.values()).

**Local steps**

- Set asset from Platform.qb.DocType(“Asset”).
- Set gl\_entry from Platform.qb.DocType(“GL Entry”).
- Set asset\_category\_account from Platform.qb.DocType(“Asset Category Account”).
- Set company from Platform.qb.DocType(“Company”).
- Set asset\_depreciation\_schedule from Platform.qb.DocType(“Asset Depreciation Schedule”).
- Set assets\_with\_finance\_book from no value.
- If filters.get(“finance\_book”).
  - Set assets\_with\_finance\_book from nested operand in the contract.qb.from\_(asset\_depreciation\_schedule).select(asset\_depreciation\_schedule.asset).where(asset\_depreciation\_schedule.finance\_book equals filters.get(“finance\_book”)).
- Set from\_gl\_entries\_query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.is\_cancelled equals 0).where(gl\_entry.account equals IfNull(asset\_category\_account.depreciation\_expense\_a ….
- Set from\_opening\_depreciation\_query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.company equals nested operand in the contract.company).where(asset.purchase\_date ≤ filters.to\_date).group ….
- If filters.get(“asset”).
  - Set from\_gl\_entries\_query from from\_gl\_entries\_query.where(asset.name equals filters.get(“asset”)).
  - Set from\_opening\_depreciation\_query from from\_opening\_depreciation\_query.where(asset.name equals filters.get(“asset”)).
- Set from\_gl\_entries\_query from from\_gl\_entries\_query.where(get\_finance\_book\_condition(gl\_entry, filters)).
- If assets\_with\_finance\_book is distinct from no value.
  - Set from\_gl\_entries\_query from from\_gl\_entries\_query.where(asset.name.isin(assets\_with\_finance\_book)).
  - Set from\_opening\_depreciation\_query from from\_opening\_depreciation\_query.where(asset.name.isin(assets\_with\_finance\_book)).
- Set combined from mapping().
- For each row in from\_gl\_entries\_query.run(as\_dict = true).
  - Set combined at row.asset from mapping(“asset” → row.asset, “accumulated\_depreciation\_as\_on\_from\_date” → flt(row.accumulated\_depreciation\_as\_on\_from\_date), “depreciation\_eliminated\_via\_reversal” → flt(row.depreciation\_eliminated\_via\_rev ….
- For each row in from\_opening\_depreciation\_query.run(as\_dict = true).
  - If row.asset does not belong to combined.
    - Set combined at row.asset from mapping(“asset” → row.asset, “accumulated\_depreciation\_as\_on\_from\_date” → 0.0, “depreciation\_eliminated\_via\_reversal” → 0.0, “depreciation\_eliminated\_during\_the\_period” → 0.0, …).
  - Update combined at row.asset at “accumulated\_depreciation\_as\_on\_from\_date” using + flt(row.accumulated\_depreciation\_as\_on\_from\_date).
  - Update combined at row.asset at “depreciation\_eliminated\_during\_the\_period” using + flt(row.depreciation\_eliminated\_during\_the\_period).
- Return list(combined.values()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L654)

<a id="op-34fd5124831a9c"></a>
### Get asset value adjustment map

`operation_enterprise_accounts_report_asset_depreciations_and_balances_business_behavior_get_asset_value_adjustment_map`

**Inputs** filters.

**Explicit results** mapping of row.pop(“asset”) → row for row drawn from asset\_with\_value\_adjustments.

**Local steps**

- Set asset from Platform.qb.DocType(“Asset”).
- Set gl\_entry from Platform.qb.DocType(“GL Entry”).
- Set asset\_category\_account from Platform.qb.DocType(“Asset Category Account”).
- Set asset\_with\_value\_adjustments from nested operand in the contract(nested operand in the contract).where(get\_finance\_book\_condition(gl\_entry, filters)).groupby(asset.name).run(as\_dict = true).
- Return mapping of row.pop(“asset”) → row for row drawn from asset\_with\_value\_adjustments.
  - Draw row from asset\_with\_value\_adjustments.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L293) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L652)

<a id="op-62e6521947e20f"></a>
### Get value adjustment columns

`operation_enterprise_binding_enterprise_accounts_report_asset_depreciations_and_balances_asset_depreciations_and_balances_get_value_adjustment_columns`

**Inputs** asset, gl\_entry, filters.

**Declared result** list.

**Explicit results** list(get\_adjustment\_sum(gl\_entry, (held\_in\_period bitwise and gl\_entry.posting\_date &lt; filters.from\_date), “adjustment\_before\_from\_date”), get\_adjustment\_sum(gl\_entry, till\_to\_date, “adjustment\_till\_to\_date ….

**Local steps**

- Set is\_adjustment from (gl\_entry.voucher\_type.notin(list(“Sales Invoice”, “Asset Capitalization”)) bitwise and gl\_entry.voucher\_no differs from IfNull(asset.journal\_entry\_for\_scrap, empty text)).
- Set held\_in\_period from (asset.disposal\_date.isnull() bitwise or asset.disposal\_date ≥ filters.from\_date).
- Set till\_to\_date from ((is\_adjustment bitwise and held\_in\_period) bitwise and gl\_entry.posting\_date ≤ filters.to\_date).
- Set disposed\_in\_period from (asset.disposal\_date.isnotnull() bitwise and asset.disposal\_date ≤ filters.to\_date).
- Return list(get\_adjustment\_sum(gl\_entry, (held\_in\_period bitwise and gl\_entry.posting\_date &lt; filters.from\_date), “adjustment\_before\_from\_date”), get\_adjustment\_sum(gl\_entry, till\_to\_date, “adjustment\_till\_to\_date ….
  - Draw tuple(status, fieldname) from DISPOSAL\_VALUE\_FIELDS.items().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1125)

<a id="op-da722e21cee534"></a>
### Get adjustment sum

`operation_enterprise_binding_enterprise_accounts_report_asset_depreciations_and_balances_asset_depreciations_and_balances_get_adjustment_sum`

**Inputs** gl\_entry, condition, alias.

**Explicit results** IfNull(Sum(amount), 0).as\_(alias).

**Local steps**

- Set amount from nested operand in the contract.terms.Case().when(condition, (gl\_entry.debit − gl\_entry.credit)).else\_(0).
- Return IfNull(Sum(amount), 0).as\_(alias).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L485) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1123)

<a id="op-3829e5cff34092"></a>
### Apply value adjustments

`operation_enterprise_binding_enterprise_accounts_report_asset_depreciations_and_balances_asset_depreciations_and_balances_apply_value_adjustments`

**Inputs** row, adjustments.

**Declared result** no value.

**Local steps**

- Set row.adjustment\_during\_period from (flt(adjustments.get(“adjustment\_till\_to\_date”)) − flt(adjustments.get(“adjustment\_before\_from\_date”))).
- Update row.value\_as\_on\_from\_date using + flt(adjustments.get(“adjustment\_before\_from\_date”)).
- For each fieldname in DISPOSAL\_VALUE\_FIELDS.values().
  - Set row at fieldname from (flt(row at fieldname) + flt(adjustments.get(formatted text adjustment\_of\_{fieldname}))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L484) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1122)

<a id="op-ad03611504504e"></a>
### Get columns

`operation_enterprise_accounts_report_asset_depreciations_and_balances_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list().
- If filters.get(“group\_by”) equals “Asset Category”.
  - Evaluate columns.append(mapping(“label” → translated “Asset Category”, “fieldname” → “asset\_category”, “fieldtype” → “Link”, “options” → “Asset Category”, …)).
- Otherwise.
  - If filters.get(“group\_by”) equals “Asset”.
    - Evaluate columns.append(mapping(“label” → translated “Asset”, “fieldname” → “asset”, “fieldtype” → “Link”, “options” → “Asset”, …)).
    - Evaluate columns.append(mapping(“label” → translated “Asset Name”, “fieldname” → “asset\_name”, “fieldtype” → “Data”, “width” → 140)).
- Update columns using + list(mapping(“label” → ((translated “Value as on” + one space) + formatdate(filters.day\_before\_from\_date)), “fieldname” → “value\_as\_on\_from\_date”, “fieldtype” → “Currency”, “width” → 140), mapping(“label”  ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L656)

## Report · Balance sheet

<a id="op-3b9edf6faddd65"></a>
### Execute

`operation_enterprise_accounts_report_balance_sheet_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** FinancialReportEngine().execute(filters) · no value · tuple(columns, data, message, chart, …).

**Local steps**

- If (filters and filters.report\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.report\_template.
  - Return FinancialReportEngine().execute(filters).
- Set period\_list from build\_period\_list(filters).
- If not period\_list.
  - Return no value.
- Set filters.period\_start\_date from period\_list at 0 at “year\_start\_date”.
- Set currency from (filters.presentation\_currency or Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.presentation\_currency → Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).
- Set asset from get\_data(filters.company, “Asset”, “Debit”, period\_list, only\_current\_fiscal\_year = false, filters = filters, accumulated\_values = filters.accumulated\_values).
- Set liability from get\_data(filters.company, “Liability”, “Credit”, period\_list, only\_current\_fiscal\_year = false, filters = filters, accumulated\_values = filters.accumulated\_values).
- Set equity from get\_data(filters.company, “Equity”, “Credit”, period\_list, only\_current\_fiscal\_year = false, filters = filters, accumulated\_values = filters.accumulated\_values).
- Set tuple(provisional\_profit\_loss, total\_credit) from get\_provisional\_profit\_loss(asset, liability, equity, period\_list, accumulated\_values = filters.accumulated\_values, …).
- Set tuple(message, opening\_balance) from check\_opening\_balance(asset, liability, equity).
- Set data from list().
- Evaluate data.extend((asset or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in asset → list().
- Evaluate data.extend((liability or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in liability → list().
- Evaluate data.extend((equity or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in equity → list().
- If (opening\_balance and filters.accumulated\_values).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in opening\_balance → filters.accumulated\_values.
  - Evaluate data.append(get\_unclosed\_profit\_loss(opening\_balance, provisional\_profit\_loss, period\_list, currency)).
- If provisional\_profit\_loss.
  - Evaluate data.append(provisional\_profit\_loss).
- If total\_credit.
  - Evaluate data.append(total\_credit).
- Set columns from get\_columns(filters.periodicity, period\_list, filters.accumulated\_values, company = filters.company, selected\_view = filters.get(“selected\_view”)).
- Set chart from get\_chart\_data(filters, period\_list, asset, liability, …).
- Set tuple(report\_summary, primitive\_summary) from get\_report\_summary(period\_list, asset, liability, equity, …).
- If filters.get(“selected\_view”) equals “Growth”.
  - Evaluate compute\_growth\_view\_data(data, period\_list).
- Return tuple(columns, data, message, chart, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L303) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L661)

<a id="op-0066c2ccfda557"></a>
### Get provisional profit loss

`operation_enterprise_accounts_report_balance_sheet_business_behavior_get_provisional_profit_loss`

**Inputs** asset, liability, equity, period\_list, company, currency = no value, consolidated = false, accumulated\_values = false.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(provisional\_profit\_loss, total\_row).

**Local steps**

- Set provisional\_profit\_loss from mapping().
- Set total\_row from mapping().
- If asset.
  - Set currency from (currency or Platform.get\_cached\_value(“Company”, company, “default\_currency”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in currency → Platform.get\_cached\_value(“Company”, company, “default\_currency”).
  - Set total\_row from mapping(“account\_name” → ((“'” + translated “Total (Credit)”) + “'”), “account” → ((“'” + translated “Total (Credit)”) + “'”), “warn\_if\_negative” → true, “currency” → currency).
  - Set has\_value from false.
  - For each period in period\_list.
    - Set key from period when consolidated, otherwise period.key.
      - Value choice on consolidated — true gives period, false gives period.key.
    - Set total\_assets from flt(asset at negative 2.get(key)).
    - Set effective\_liability from 0.0.
    - If (liability and liability at negative 1 equals mapping()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in liability → liability at negative 1 equals mapping().
      - Update effective\_liability using + flt(liability at negative 2.get(key)).
    - If (equity and equity at negative 1 equals mapping()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in equity → equity at negative 1 equals mapping().
      - Update effective\_liability using + flt(equity at negative 2.get(key)).
    - Set provisional\_profit\_loss at key from (total\_assets − effective\_liability).
    - Set total\_row at key from (provisional\_profit\_loss at key + effective\_liability).
    - If provisional\_profit\_loss at key.
      - Set has\_value from true.
  - Set total\_keys from get\_period\_keys\_for\_total(period\_list, accumulated\_values, consolidated).
  - Set provisional\_profit\_loss at “total” from flt(sum(generator of provisional\_profit\_loss.get(k, 0.0) for k drawn from total\_keys)).
    - Draw k from total\_keys.
  - Set total\_row at “total” from flt(sum(generator of total\_row.get(k, 0.0) for k drawn from total\_keys)).
    - Draw k from total\_keys.
  - If has\_value.
    - Evaluate set\_provisional\_profit\_loss\_labels(provisional\_profit\_loss, currency).
- Return tuple(provisional\_profit\_loss, total\_row).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L665)

<a id="op-a683989f8226e6"></a>
### Set provisional profit loss labels

`operation_enterprise_binding_enterprise_accounts_report_balance_sheet_balance_sheet_set_provisional_profit_loss_labels`

**Inputs** provisional\_profit\_loss, currency.

**Declared result** no value.

**Local steps**

- Evaluate provisional\_profit\_loss.update(mapping(“account\_name” → ((“'” + translated “Provisional Profit / Loss (Credit)”) + “'”), “account” → ((“'” + translated “Provisional Profit / Loss (Credit)”) + “'”), “warn\_i ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L490) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1128)

<a id="op-cceb588573d426"></a>
### Get unclosed profit loss

`operation_enterprise_binding_enterprise_accounts_report_balance_sheet_balance_sheet_get_unclosed_profit_loss`

**Inputs** opening\_balance, provisional\_profit\_loss, period\_list, currency.

**Explicit results** unclosed.

**Local steps**

- Set unclosed from mapping(“account\_name” → ((“'” + translated “Unclosed Fiscal Years Profit / Loss (Credit)”) + “'”), “account” → ((“'” + translated “Unclosed Fiscal Years Profit / Loss (Credit)”) + “'”), “warn\_if\_negative” ….
- For each period in period\_list.
  - Set unclosed at period.key from opening\_balance.
  - If provisional\_profit\_loss.
    - Update provisional\_profit\_loss at period.key using − opening\_balance.
- If provisional\_profit\_loss.
  - Update provisional\_profit\_loss at “total” using − opening\_balance.
  - Evaluate set\_provisional\_profit\_loss\_labels(provisional\_profit\_loss, currency).
- Return unclosed.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1127)

<a id="op-cf299f53a6ace6"></a>
### Check opening balance

`operation_enterprise_accounts_report_balance_sheet_business_behavior_check_opening_balance`

**Inputs** asset, liability, equity.

**Explicit results** tuple(translated “Previous Financial Year is not closed”, opening\_balance) · tuple(no value, no value).

**Local steps**

- Set opening\_balance from 0.
- Set float\_precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- If asset.
  - Set opening\_balance from flt(get\_total\_row(asset).get(“opening\_balance”, 0), float\_precision).
- If liability.
  - Update opening\_balance using − flt(get\_total\_row(liability).get(“opening\_balance”, 0), float\_precision).
- If equity.
  - Update opening\_balance using − flt(get\_total\_row(equity).get(“opening\_balance”, 0), float\_precision).
- Set opening\_balance from flt(opening\_balance, float\_precision).
- If opening\_balance.
  - Return tuple(translated “Previous Financial Year is not closed”, opening\_balance).
- Return tuple(no value, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L302) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L660)

<a id="op-d187b58e87a541"></a>
### Get total row

`operation_enterprise_binding_enterprise_accounts_report_balance_sheet_balance_sheet_get_total_row`

**Inputs** rows.

**Declared result** dict.

**Explicit results** rows at negative 2 when (rows at negative 1 equals mapping() and len(rows) &gt; 1), otherwise rows at negative 1.

**Local steps**

- Return rows at negative 2 when (rows at negative 1 equals mapping() and len(rows) &gt; 1), otherwise rows at negative 1.
  - Value choice on (rows at negative 1 equals mapping() and len(rows) &gt; 1) — true gives rows at negative 2, false gives rows at negative 1.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rows at negative 1 equals mapping() → len(rows) &gt; 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1126)

<a id="op-eb690f1b86e6ee"></a>
### Get report summary

`operation_enterprise_accounts_report_balance_sheet_business_behavior_get_report_summary`

**Inputs** period\_list, asset, liability, equity, provisional\_profit\_loss, currency, filters, consolidated = false.

**Explicit results** tuple(list(mapping(“value” → net\_asset, “label” → translated “Total Asset”, “datatype” → “Currency”, “currency” → currency), mapping(“value” → net\_liability, “label” → translated “Total Liability”, “dataty ….

**Local steps**

- Set tuple(net\_asset, net\_liability, net\_equity, net\_provisional\_profit\_loss) from tuple(0.0, 0.0, 0.0, 0.0).
- If filters.get(“accumulated\_in\_group\_company”).
  - Set period\_list from get\_filtered\_list\_for\_consolidated\_report(filters, period\_list).
  - Set keys from list of period when consolidated, otherwise period.key for period drawn from period\_list.
    - Draw period from period\_list.
    - Value choice on consolidated — true gives period, false gives period.key.
- Otherwise.
  - Set keys from get\_period\_keys\_for\_total(period\_list, filters.accumulated\_values, consolidated).
- For each key in keys.
  - If asset.
    - Update net\_asset using + flt(asset at negative 2.get(key)).
  - If (liability and liability at negative 1 equals mapping()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in liability → liability at negative 1 equals mapping().
    - Update net\_liability using + flt(liability at negative 2.get(key)).
  - If (equity and equity at negative 1 equals mapping()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in equity → equity at negative 1 equals mapping().
    - Update net\_equity using + flt(equity at negative 2.get(key)).
  - If provisional\_profit\_loss.
    - Update net\_provisional\_profit\_loss using + flt(provisional\_profit\_loss.get(key)).
- Return tuple(list(mapping(“value” → net\_asset, “label” → translated “Total Asset”, “datatype” → “Currency”, “currency” → currency), mapping(“value” → net\_liability, “label” → translated “Total Liability”, “dataty ….
  - Value choice on net\_provisional\_profit\_loss &gt; 0 — true gives “Green”, false gives “Red”.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0229.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L666)

<a id="op-3b560141411cb2"></a>
### Get chart data

`operation_enterprise_accounts_report_balance_sheet_business_behavior_get_chart_data`

**Inputs** filters, chart\_columns, asset, liability, equity, currency.

**Explicit results** chart.

**Local steps**

- Set labels from list of col.get(“label”) for col drawn from chart\_columns.
  - Draw col from chart\_columns.
- Set tuple(asset\_data, liability\_data, equity\_data) from tuple(list(), list(), list()).
- For each col in chart\_columns.
  - Set key from (col.get(“key”) or col.get(“fieldname”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“key”) → col.get(“fieldname”).
  - If asset.
    - Evaluate asset\_data.append(asset at negative 2.get(key)).
  - If liability.
    - Evaluate liability\_data.append(liability at negative 2.get(key)).
  - If equity.
    - Evaluate equity\_data.append(equity at negative 2.get(key)).
- Set datasets from list().
- If asset\_data.
  - Evaluate datasets.append(mapping(“name” → translated “Assets”, “values” → asset\_data)).
- If liability\_data.
  - Evaluate datasets.append(mapping(“name” → translated “Liabilities”, “values” → liability\_data)).
- If equity\_data.
  - Evaluate datasets.append(mapping(“name” → translated “Equity”, “values” → equity\_data)).
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → datasets)).
- If not filters.accumulated\_values.
  - Set chart at “type” from “bar”.
- Otherwise.
  - Set chart at “type” from “line”.
- Set chart at “fieldtype” from “Currency”.
- Set chart at “options” from “currency”.
- Set chart at “currency” from currency.
- Return chart.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0229.json#L991) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L663)

<a id="op-5fa95be5ef80b8"></a>
### Execute snapshot report

`operation_enterprise_accounts_report_balance_sheet_business_behavior_execute_snapshot_report`

**Inputs** filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** execute(filters) · tuple(columns, data, message, chart, …).

**Explicit failure paths** validation helper — translated “Balance Sheet requires {0} to be synced to DuckDB”.format(Platform.bold(“GL Entry”)).

**Local steps**

- If (filters.report\_template or has\_gl\_entry\_restrictions()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.report\_template → has\_gl\_entry\_restrictions().
  - Return execute(filters).
- Bind dependencies get\_latest\_sync.
- If not conn bound to get\_latest\_sync(“GL Entry”).
  - Call the validation error handler Platform.throw(translated “Balance Sheet requires {0} to be synced to DuckDB”.format(Platform.bold(“GL Entry”))).
- Set period\_list from build\_period\_list(filters).
- Set filters.period\_start\_date from period\_list at 0 at “year\_start\_date”.
- Set currency from (filters.presentation\_currency or Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.presentation\_currency → Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).
- Set asset from \_get\_data\_duckdb(conn, filters, “Asset”, “Debit”, …).
- Set liability from \_get\_data\_duckdb(conn, filters, “Liability”, “Credit”, …).
- Set equity from \_get\_data\_duckdb(conn, filters, “Equity”, “Credit”, …).
- Set tuple(provisional\_profit\_loss, total\_credit) from get\_provisional\_profit\_loss(asset, liability, equity, period\_list, accumulated\_values = filters.accumulated\_values, …).
- Set tuple(message, opening\_balance) from check\_opening\_balance(asset, liability, equity).
- Set data from list().
- Evaluate data.extend((asset or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in asset → list().
- Evaluate data.extend((liability or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in liability → list().
- Evaluate data.extend((equity or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in equity → list().
- If (opening\_balance and filters.accumulated\_values).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in opening\_balance → filters.accumulated\_values.
  - Evaluate data.append(get\_unclosed\_profit\_loss(opening\_balance, provisional\_profit\_loss, period\_list, currency)).
- If provisional\_profit\_loss.
  - Evaluate data.append(provisional\_profit\_loss).
- If total\_credit.
  - Evaluate data.append(total\_credit).
- Set columns from get\_columns(filters.periodicity, period\_list, filters.accumulated\_values, company = filters.company, selected\_view = filters.get(“selected\_view”)).
- Set chart from get\_chart\_data(filters, period\_list, asset, liability, …).
- Set tuple(report\_summary, primitive\_summary) from get\_report\_summary(period\_list, asset, liability, equity, …).
- If filters.get(“selected\_view”) equals “Growth”.
  - Evaluate compute\_growth\_view\_data(data, period\_list).
- Return tuple(columns, data, message, chart, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L304) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L662)

<a id="op-6fef97509d121d"></a>
### Get data duckdb

`operation_enterprise_accounts_report_balance_sheet_business_behavior_get_data_duckdb`

**Inputs** conn, filters, root\_type, balance\_must\_be, period\_list.

**Explicit results** no value · out.

**Local steps**

- Set accounts from get\_accounts(filters.company, root\_type).
- If not accounts.
  - Return no value.
- Set tuple(accounts, accounts\_by\_name, parent\_children\_map) from filter\_accounts(accounts).
- Set company\_currency from get\_appropriate\_currency(filters.company, filters).
- Set gl\_entries\_by\_account from mapping().
- Evaluate \_load\_gl\_entries\_duckdb(conn, filters, period\_list, accounts, …).
- Evaluate calculate\_values(accounts\_by\_name, gl\_entries\_by\_account, period\_list, filters.accumulated\_values, …).
- Evaluate accumulate\_values\_into\_parents(accounts, accounts\_by\_name, period\_list).
- Set out from prepare\_data(accounts, balance\_must\_be, period\_list, company\_currency, accumulated\_values = filters.accumulated\_values).
- Set out from filter\_out\_zero\_value\_rows(out, parent\_children\_map, filters.show\_zero\_values).
- If out.
  - Evaluate add\_total\_row(out, root\_type, balance\_must\_be, period\_list, …).
- Return out.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0229.json#L3128) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L664)

<a id="op-85899ef5a3542e"></a>
### Load gl entries duckdb

`operation_enterprise_accounts_report_balance_sheet_business_behavior_load_general_ledger_entries_duckdb`

**Inputs** conn, filters, period\_list, accounts, gl\_entries\_by\_account, root\_type.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Period Closing Voucher” via get\_all.

**Explicit results** no value.

**Local steps**

- Bind dependencies \_extra\_gl\_conditions, \_fetch\_gl\_rows\_duckdb.
- Bind dependencies convert\_to\_presentation\_currency, get\_currency.
- Set company from filters.company.
- Set year\_start\_date from period\_list at 0 at “year\_start\_date”.
- Set last\_to\_date from period\_list at negative 1 at “to\_date”.
- Set ignore\_is\_opening from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).
- Set leaf\_accounts from list of acc.name for acc drawn from accounts where not acc.is\_group.
  - Draw acc from accounts, keep a combination only if (not acc.is\_group).
- If not leaf\_accounts.
  - Return no value.
- Set opening\_from\_date from no value.
- Set ignore\_opening\_entries from false.
- Set ignore\_closing\_balances from Platform.get\_single\_value(“Accounts Settings”, “ignore\_account\_closing\_balance”).
- If not ignore\_closing\_balances.
  - Set last\_pcv\_list from Platform.db.get\_all(“Period Closing Voucher”, filters = mapping(“docstatus” → 1, “company” → company, “period\_end\_date” → tuple(“&lt;”, (filters.get(“period\_start\_date”) or year\_start\_date))), fields = list(“ ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“period\_start\_date”) → year\_start\_date.
  - If last\_pcv\_list.
    - Set last\_pcv from last\_pcv\_list at 0.
    - Set pcv\_entries from get\_accounting\_entries(“Account Closing Balance”, no value, last\_to\_date, filters, root\_type = root\_type, ignore\_closing\_entries = false, period\_closing\_voucher = last\_pcv.name).
    - If filters.get(“presentation\_currency”).
      - Evaluate convert\_to\_presentation\_currency(pcv\_entries, get\_currency(filters)).
    - For each entry in pcv\_entries.
      - Evaluate gl\_entries\_by\_account.setdefault(entry.account, list()).append(entry).
    - Set opening\_from\_date from add\_days(last\_pcv.period\_end\_date, 1).
    - Set ignore\_opening\_entries from true.
- Set tuple(extra\_cond, extra\_params) from \_extra\_gl\_conditions(filters).
- Set account\_placeholders from “, ”.join((list(“?”) × len(leaf\_accounts))).
- Set base\_conds from list(“company = ?”, “is\_cancelled = 0”, formatted text account IN ({account\_placeholders})).
- Set base\_params from list(company, expanded leaf\_accounts).
- If (ignore\_opening\_entries and not ignore\_is\_opening).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ignore\_opening\_entries → not ignore\_is\_opening.
  - Evaluate base\_conds.append(“is\_opening = 'No'”).
- Evaluate base\_conds.extend(extra\_cond).
- Evaluate base\_params.extend(extra\_params).
- Set open\_conds from list(expanded base\_conds, “posting\_date &lt; ?”).
- Set open\_params from list(expanded base\_params, year\_start\_date).
- If opening\_from\_date.
  - Set open\_conds from list(expanded open\_conds, “posting\_date &gt;= ?”).
  - Set open\_params from list(expanded open\_params, opening\_from\_date).
- Set opening\_entries from \_fetch\_gl\_rows\_duckdb(conn, open\_conds, open\_params).
- If filters.get(“presentation\_currency”).
  - Evaluate convert\_to\_presentation\_currency(opening\_entries, get\_currency(filters)).
- Set synthetic\_open\_date from add\_days(year\_start\_date, negative 1).
- For each entry in opening\_entries.
  - Set entry.posting\_date from synthetic\_open\_date.
  - Evaluate gl\_entries\_by\_account.setdefault(entry.account, list()).append(entry).
- For each period in period\_list.
  - Set period\_conds from list(expanded base\_conds, “posting\_date &gt;= ?”, “posting\_date &lt;= ?”).
  - Set period\_params from list(expanded base\_params, period.from\_date, period.to\_date).
  - Set period\_entries from \_fetch\_gl\_rows\_duckdb(conn, period\_conds, period\_params).
  - If filters.get(“presentation\_currency”).
    - Evaluate convert\_to\_presentation\_currency(period\_entries, get\_currency(filters)).
  - For each entry in period\_entries.
    - Set entry.posting\_date from period.to\_date.
    - Evaluate gl\_entries\_by\_account.setdefault(entry.account, list()).append(entry).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”), Platform.get\_single\_value(“Accounts Settings”, “ignore\_account\_closing\_balance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0229.json#L3588) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L667)

## Record · Bank

[Record definition](../../../../data/record-types/bank.json)

<a id="op-fa3c786727d8a8"></a>
### Bank.onload

`operation_enterprise_accounts_record_definitions_bank_business_behavior_bank_onload`

**Inputs** self.

**Local steps**

- Evaluate load\_address\_and\_contact(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0014.json#L3226) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L262) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L252)

<a id="op-91d4004e0869b1"></a>
### Bank.on trash

`operation_enterprise_accounts_record_definitions_bank_business_behavior_bank_on_trash`

**Inputs** self.

**Local steps**

- Evaluate delete\_contact\_and\_address(“Bank”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0014.json#L3278) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L261) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L251)

<a id="op-14fda86495ad92"></a>
### Get data

`operation_enterprise_accounts_record_definitions_bank_bank_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “bank”, “transactions” → list(mapping(“label” → translated “Bank Details”, “items” → list(“Bank Account”, “Bank Guarantee”)))).

**Local steps**

- Return mapping(“fieldname” → “bank”, “transactions” → list(mapping(“label” → translated “Bank Details”, “items” → list(“Bank Account”, “Bank Guarantee”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0014.json#L3345) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L260) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L250)

## Record · Bank account

[Record definition](../../../../data/record-types/bank_account.json)

<a id="op-e29463f42a9922"></a>
### Bank Account.onload

`operation_enterprise_accounts_record_definitions_bank_account_business_behavior_bank_account_onload`

**Inputs** self.

**Local steps**

- Evaluate load\_address\_and\_contact(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0014.json#L3479) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L239)
