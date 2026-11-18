# Asset management · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset shift allocation

[Record definition](../../../../data/record-types/asset_shift_allocation.json)

<a id="op-63b69788939756"></a>
### Replace active depr schedule

`operation_enterprise_binding_enterprise_assets_doctype_asset_shift_allocation_asset_shift_allocation_replace_active_depr_schedule`

**Inputs** active\_schedule\_doc, new\_schedule\_doc.

**Declared result** no value.

**State and service calls** call cancel on active\_schedule\_doc · call submit on new\_schedule\_doc.

**Local steps**

- Set active\_schedule\_doc.flags.should\_not\_cancel\_depreciation\_entries from true.
- Set active\_schedule\_doc.ignore\_linked\_doctypes from tuple(“Asset Shift Allocation”).
- Evaluate active\_schedule\_doc.cancel().
- Evaluate new\_schedule\_doc.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L767) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L7)

<a id="op-1980ee56163fa5"></a>
### Get schedule rows

`operation_enterprise_binding_enterprise_assets_doctype_asset_shift_allocation_asset_shift_allocation_get_schedule_rows`

**Inputs** schedule.

**Declared result** list at tuple.

**Explicit results** list of tuple(getdate(row.schedule\_date), flt(row.depreciation\_amount, 2), row.shift, (row.journal\_entry or no value)) for row drawn from schedule.

**Local steps**

- Return list of tuple(getdate(row.schedule\_date), flt(row.depreciation\_amount, 2), row.shift, (row.journal\_entry or no value)) for row drawn from schedule.
  - Draw row from schedule.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.journal\_entry → no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L766) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L6)

## Record · Asset shift factor

[Record definition](../../../../data/record-types/asset_shift_factor.json)

<a id="op-7dd9317572e52b"></a>
### Asset Shift Factor.validate

`operation_enterprise_assets_record_definitions_asset_shift_factor_business_behavior_asset_shift_factor_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_shift\_factor().
- Evaluate self.validate\_default().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate shift factor](operations-018.md#op-318c87f0e365a4), [validate default](operations-018.md#op-061348cfbc8841).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1766) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L619)

<a id="op-318c87f0e365a4"></a>
### Asset Shift Factor.validate shift factor

`operation_enterprise_binding_enterprise_assets_doctype_asset_shift_factor_asset_shift_factor_assetshiftfactor_validate_shift_factor`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Shift Factor must be greater than zero.”.

**Local steps**

- If flt(self.shift\_factor) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Shift Factor must be greater than zero.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L768) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L8)

<a id="op-061348cfbc8841"></a>
### Asset Shift Factor.validate default

`operation_enterprise_assets_record_definitions_asset_shift_factor_business_behavior_asset_shift_factor_validate_default`

**Inputs** self.

**Record and data access** read “Asset Shift Factor” via get\_value.

**Explicit failure paths** validation helper — translated “Asset Shift Factor {0} is set as default currently. Please change it first.”.format(Platform.bold(existing\_default\_shift\_factor)).

**Local steps**

- If self.default.
  - Set existing\_default\_shift\_factor from Platform.db.get\_value(“Asset Shift Factor”, mapping(“default” → 1, “name” → tuple(“!=”, self.name)), “name”).
  - If existing\_default\_shift\_factor.
    - Call the validation error handler Platform.throw(translated “Asset Shift Factor {0} is set as default currently. Please change it first.”.format(Platform.bold(existing\_default\_shift\_factor))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1767) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L620)

## Record · Asset value adjustment

[Record definition](../../../../data/record-types/asset_value_adjustment.json)

<a id="op-31aeb7bdc1bc7b"></a>
### Asset Value Adjustment.validate

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_asset\_not\_disposed().
- Evaluate self.validate\_date().
- Evaluate self.validate\_new\_asset\_value().
- Evaluate self.validate\_finance\_book().
- Evaluate self.set\_current\_asset\_value().
- Evaluate self.set\_difference\_amount().
- Evaluate self.validate\_difference\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate asset not disposed](operations-018.md#op-22a658b3b6720a), [validate date](operations-018.md#op-b804f5e9b551b5), [validate new asset value](operations-018.md#op-dedafb87a9d239), [validate finance book](operations-018.md#op-a43ca7cfc5fc0f), [set current asset value](operations-018.md#op-a64cd61b0342d3), [set difference amount](operations-018.md#op-129c9c6aadcd65), [validate difference amount](operations-018.md#op-df85546392f1aa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L50) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L703)

<a id="op-9e87a00f1c11c0"></a>
### Asset Value Adjustment.before cancel

`operation_enterprise_binding_enterprise_assets_doctype_asset_value_adjustment_asset_value_adjustment_assetvalueadjustment_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_asset\_not\_disposed().
- Evaluate self.validate\_asset\_not\_split().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate asset not disposed](operations-018.md#op-22a658b3b6720a), [validate asset not split](operations-018.md#op-cc3018edbc87e5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L769) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L9)

<a id="op-cc3018edbc87e5"></a>
### Asset Value Adjustment.validate asset not split

`operation_enterprise_binding_enterprise_assets_doctype_asset_value_adjustment_asset_value_adjustment_assetvalueadjustment_validate_asset_not_split`

**Inputs** self.

**Record and data access** read self.doctype via get\_value · read “Asset” via get\_value.

**Explicit failure paths** validation helper — translated “Asset {0} was split into Asset {1} after this adjustment, so it cannot be cancelled. Adjust the value of eac …”.format(get\_link\_to\_form(“Asset”, self.asset), get\_link\_to\_form(“Asset”, split\_asset)).

**Local steps**

- Set submitted\_on from Platform.db.get\_value(self.doctype, self.name, “modified”).
- Set split\_asset from Platform.db.get\_value(“Asset”, mapping(“split\_from” → self.asset, “creation” → tuple(“&gt;”, submitted\_on)), “name”).
- If split\_asset.
  - Call the validation error handler Platform.throw(translated “Asset {0} was split into Asset {1} after this adjustment, so it cannot be cancelled. Adjust the value of eac …”.format(get\_link\_to\_form(“Asset”, self.asset), get\_link\_to\_form(“As ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L772) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L12)

<a id="op-22a658b3b6720a"></a>
### Asset Value Adjustment.validate asset not disposed

`operation_enterprise_binding_enterprise_assets_doctype_asset_value_adjustment_asset_value_adjustment_assetvalueadjustment_validate_asset_not_disposed`

**Inputs** self.

**Record and data access** read “Asset” via get\_value.

**Explicit failure paths** validation helper — translated “Asset {0} is disposed, its value cannot be adjusted”.format(get\_link\_to\_form(“Asset”, self.asset)).

**Local steps**

- Set tuple(status, disposal\_date) from Platform.db.get\_value(“Asset”, self.asset, list(“status”, “disposal\_date”)).
- If (disposal\_date or status belongs to tuple(“Sold”, “Scrapped”, “Capitalized”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in disposal\_date → status belongs to tuple(“Sold”, “Scrapped”, “Capitalized”).
  - Call the validation error handler Platform.throw(translated “Asset {0} is disposed, its value cannot be adjusted”.format(get\_link\_to\_form(“Asset”, self.asset))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L771) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L11)

<a id="op-b804f5e9b551b5"></a>
### Asset Value Adjustment.validate date

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_validate_date`

**Inputs** self.

**Record and data access** read “Asset” via get\_value.

**Explicit failure paths** validation helper — translated “Asset Value Adjustment cannot be posted before Asset's purchase date &lt;b&gt;{0}&lt;/b&gt;.”.format(formatdate(asset\_purchase\_date)) · validation helper — translated “Asset Value Adjustment cannot be posted before the last depreciation entry dated {0}”.format(formatdate(last\_depreciation\_date)).

**Local steps**

- Set asset\_purchase\_date from Platform.db.get\_value(“Asset”, self.asset, “purchase\_date”).
- If getdate(self.date) &lt; getdate(asset\_purchase\_date).
  - Call the validation error handler Platform.throw(translated “Asset Value Adjustment cannot be posted before Asset's purchase date &lt;b&gt;{0}&lt;/b&gt;.”.format(formatdate(asset\_purchase\_date)), title = translated “Incorrect Date”).
- Set last\_depreciation\_date from get\_last\_depreciation\_date(self.asset, self.finance\_book).
- If (last\_depreciation\_date and getdate(self.date) &lt; last\_depreciation\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_depreciation\_date → getdate(self.date) &lt; last\_depreciation\_date.
  - Call the validation error handler Platform.throw(translated “Asset Value Adjustment cannot be posted before the last depreciation entry dated {0}”.format(formatdate(last\_depreciation\_date)), title = translated “Incorrect Date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L51) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L704)

<a id="op-dedafb87a9d239"></a>
### Asset Value Adjustment.validate new asset value

`operation_enterprise_binding_enterprise_assets_doctype_asset_value_adjustment_asset_value_adjustment_assetvalueadjustment_validate_new_asset_value`

**Inputs** self.

**Explicit failure paths** validation helper — translated “New Asset Value cannot be negative”.

**Local steps**

- If flt(self.new\_asset\_value) &lt; 0.
  - Call the validation error handler Platform.throw(translated “New Asset Value cannot be negative”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L776) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L16)

<a id="op-a43ca7cfc5fc0f"></a>
### Asset Value Adjustment.validate finance book

`operation_enterprise_binding_enterprise_assets_doctype_asset_value_adjustment_asset_value_adjustment_assetvalueadjustment_validate_finance_book`

**Inputs** self.

**Record and data access** read “Asset” via get\_value.

**Explicit results** no value.

**Local steps**

- If not Platform.db.get\_value(“Asset”, self.asset, “calculate\_depreciation”).
  - Return no value.
- If self.finance\_book.
  - Evaluate self.validate\_finance\_book\_is\_set\_on\_asset().
- Otherwise.
  - Evaluate self.validate\_asset\_has\_no\_named\_finance\_book().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate finance book is set on asset](operations-018.md#op-c42ab5fba26579), [validate asset has no named finance book](operations-018.md#op-e317bca15068f8).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L774) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L14)

<a id="op-c42ab5fba26579"></a>
### Asset Value Adjustment.validate finance book is set on asset

`operation_enterprise_binding_enterprise_assets_doctype_asset_value_adjustment_asset_value_adjustment_assetvalueadjustment_validate_finance_book_is_set_on_asset`

**Inputs** self.

**Record and data access** read “Asset Finance Book” via exists.

**Explicit failure paths** validation helper — translated “Finance Book {0} is not set on Asset {1}”.format(Platform.bold(self.finance\_book), get\_link\_to\_form(“Asset”, self.asset)).

**Local steps**

- If not Platform.db.exists(“Asset Finance Book”, mapping(“parent” → self.asset, “parenttype” → “Asset”, “finance\_book” → self.finance\_book)).
  - Call the validation error handler Platform.throw(translated “Finance Book {0} is not set on Asset {1}”.format(Platform.bold(self.finance\_book), get\_link\_to\_form(“Asset”, self.asset))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L775) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L15)

<a id="op-e317bca15068f8"></a>
### Asset Value Adjustment.validate asset has no named finance book

`operation_enterprise_binding_enterprise_assets_doctype_asset_value_adjustment_asset_value_adjustment_assetvalueadjustment_validate_asset_has_no_named_finance_book`

**Inputs** self.

**Record and data access** read “Asset Finance Book” via exists.

**Explicit failure paths** validation helper — translated “Select a Finance Book, as Asset {0} has named finance books”.format(get\_link\_to\_form(“Asset”, self.asset)).

**Local steps**

- If Platform.db.exists(“Asset Finance Book”, mapping(“parent” → self.asset, “parenttype” → “Asset”, “finance\_book” → list(“is”, “set”))).
  - Call the validation error handler Platform.throw(translated “Select a Finance Book, as Asset {0} has named finance books”.format(get\_link\_to\_form(“Asset”, self.asset)), title = translated “Missing Finance Book”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L770) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L10)

<a id="op-df85546392f1aa"></a>
### Asset Value Adjustment.validate difference amount

`operation_enterprise_binding_enterprise_assets_doctype_asset_value_adjustment_asset_value_adjustment_assetvalueadjustment_validate_difference_amount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “New Asset Value is the same as the current asset value”.

**Local steps**

- If not self.difference\_amount.
  - Call the validation error handler Platform.throw(translated “New Asset Value is the same as the current asset value”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L773) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L13)

<a id="op-129c9c6aadcd65"></a>
### Asset Value Adjustment.set difference amount

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_set_difference_amount`

**Inputs** self.

**Local steps**

- Set self.difference\_amount from flt((self.new\_asset\_value − self.current\_asset\_value)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L5220) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L46) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L699)

<a id="op-a64cd61b0342d3"></a>
### Asset Value Adjustment.set current asset value

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_set_current_asset_value`

**Inputs** self.

**Local steps**

- If self.asset.
  - Set self.current\_asset\_value from \_get\_asset\_value\_after\_depreciation(self.asset, self.finance\_book).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L45) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L698)

<a id="op-920ce9400b7f33"></a>
### Asset Value Adjustment.on submit

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.make\_asset\_revaluation\_entry().
- Evaluate self.update\_asset().
- Evaluate add\_asset\_activity(self.asset, translated “Asset's value adjusted after submission of Asset Value Adjustment {0}”.format(get\_link\_to\_form(“Asset Value Adjustment”, self.name))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make asset revaluation entry](operations-018.md#op-b3f3fba9f8642a), [update asset](operations-019.md#op-7ec019a68ef5bb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L5402) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L44) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L697)

<a id="op-0fcc53de87f333"></a>
### Asset Value Adjustment.on cancel

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.cancel\_asset\_revaluation\_entry().
- Evaluate self.update\_asset().
- Evaluate add\_asset\_activity(self.asset, translated “Asset's value adjusted after cancellation of Asset Value Adjustment {0}”.format(get\_link\_to\_form(“Asset Value Adjustment”, self.name))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [cancel asset revaluation entry](operations-018.md#op-597066fbcac691), [update asset](operations-019.md#op-7ec019a68ef5bb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L5562) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L43) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L696)

<a id="op-b3f3fba9f8642a"></a>
### Asset Value Adjustment.make asset revaluation entry

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_make_asset_revaluation_entry`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_doc · read “Company” via get\_cached\_value.

**State and service calls** request new\_doc for “Journal Entry” · call submit on je · call db\_set on self.

**Local steps**

- Set asset from Platform.get\_doc(“Asset”, self.asset).
- Set tuple(fixed\_asset\_account, accumulated\_depreciation\_account, depreciation\_expense\_account) from get\_depreciation\_accounts(asset.asset\_category, asset.company).
- Set tuple(depreciation\_cost\_center, depreciation\_series) from Platform.get\_cached\_value(“Company”, asset.company, list(“depreciation\_cost\_center”, “series\_for\_depreciation\_entry”)).
- Set je from Platform.new\_doc(“Journal Entry”).
- Set je.voucher\_type from “Journal Entry”.
- Set je.naming\_series from depreciation\_series.
- Set je.posting\_date from self.date.
- Set je.company from self.company.
- Set je.remark from formatted text Revaluation Entry against {self.asset} worth {self.difference\_amount}.
- Set je.finance\_book from self.finance\_book.
- Set entry\_template from mapping(“cost\_center” → (self.cost\_center or depreciation\_cost\_center), “reference\_type” → “Asset”, “reference\_name” → asset.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → depreciation\_cost\_center.
- If self.difference\_amount &lt; 0.
  - Set tuple(credit\_entry, debit\_entry) from self.get\_entry\_for\_asset\_value\_decrease(fixed\_asset\_account, entry\_template).
- Otherwise.
  - If self.difference\_amount &gt; 0.
    - Set tuple(credit\_entry, debit\_entry) from self.get\_entry\_for\_asset\_value\_increase(fixed\_asset\_account, entry\_template).
- Evaluate self.update\_accounting\_dimensions(credit\_entry, debit\_entry).
- Evaluate je.append(“accounts”, credit\_entry).
- Evaluate je.append(“accounts”, debit\_entry).
- Set je.flags.ignore\_permissions from true.
- Evaluate je.submit().
- Evaluate self.db\_set(“journal\_entry”, je.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get entry for asset value decrease](operations-018.md#op-404e472c92b7f8), [get entry for asset value increase](operations-018.md#op-9c36156223b6d3), [update accounting dimensions](operations-018.md#op-52acaeeebd6556).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, asset.company, list(“depreciation\_cost\_center”, “series\_for\_depreciation\_entry”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L5722) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L42) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L695)

<a id="op-404e472c92b7f8"></a>
### Asset Value Adjustment.get entry for asset value decrease

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_get_entry_for_asset_value_decrease`

**Inputs** self, fixed\_asset\_account, entry\_template.

**Explicit results** tuple(credit\_entry, debit\_entry).

**Local steps**

- Set credit\_entry from mapping(“account” → fixed\_asset\_account, “credit\_in\_account\_currency” → negative self.difference\_amount, expand entry\_template).
- Set debit\_entry from mapping(“account” → self.difference\_account, “debit\_in\_account\_currency” → negative self.difference\_amount, expand entry\_template).
- Return tuple(credit\_entry, debit\_entry).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L6511) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L40) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L693)

<a id="op-9c36156223b6d3"></a>
### Asset Value Adjustment.get entry for asset value increase

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_get_entry_for_asset_value_increase`

**Inputs** self, fixed\_asset\_account, entry\_template.

**Explicit results** tuple(credit\_entry, debit\_entry).

**Local steps**

- Set credit\_entry from mapping(“account” → self.difference\_account, “credit\_in\_account\_currency” → self.difference\_amount, expand entry\_template).
- Set debit\_entry from mapping(“account” → fixed\_asset\_account, “debit\_in\_account\_currency” → self.difference\_amount, expand entry\_template).
- Return tuple(credit\_entry, debit\_entry).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L6703) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L41) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L694)

<a id="op-52acaeeebd6556"></a>
### Asset Value Adjustment.update accounting dimensions

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_update_accounting_dimensions`

**Inputs** self, credit\_entry, debit\_entry.

**Local steps**

- Set accounting\_dimensions from get\_checks\_for\_pl\_and\_bs\_accounts().
- For each dimension in accounting\_dimensions.
  - Set value from self.get(dimension at “fieldname”).
  - Set is\_own\_company from dimension.get(“company”) equals self.company.
  - If (value or (is\_own\_company and dimension.get(“mandatory\_for\_bs”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → (is\_own\_company and dimension.get(“mandatory\_for\_bs”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_own\_company → dimension.get(“mandatory\_for\_bs”).
    - Set credit\_entry at dimension at “fieldname” from (value or dimension.get(“default\_dimension”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → dimension.get(“default\_dimension”).
  - If (value or (is\_own\_company and dimension.get(“mandatory\_for\_pl”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → (is\_own\_company and dimension.get(“mandatory\_for\_pl”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_own\_company → dimension.get(“mandatory\_for\_pl”).
    - Set debit\_entry at dimension at “fieldname” from (value or dimension.get(“default\_dimension”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → dimension.get(“default\_dimension”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L47) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L700)

<a id="op-597066fbcac691"></a>
### Asset Value Adjustment.cancel asset revaluation entry

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_cancel_asset_revaluation_entry`

**Inputs** self.

**Record and data access** resolve a document from “Journal Entry” via get\_doc.

**State and service calls** call cancel on revaluation\_entry.

**Explicit results** no value.

**Local steps**

- If not self.journal\_entry.
  - Return no value.
- Set revaluation\_entry from Platform.get\_doc(“Journal Entry”, self.journal\_entry).
- If revaluation\_entry.docstatus equals 1.
  - Set revaluation\_entry.flags.ignore\_permissions from true.
  - Set revaluation\_entry.flags.via\_asset\_value\_adjustment from true.
  - Evaluate revaluation\_entry.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L7196) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L37) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L690)
