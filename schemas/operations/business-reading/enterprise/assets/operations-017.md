# Asset management · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset repair

[Record definition](../../../../data/record-types/asset_repair.json)

<a id="op-088ca17f4824bb"></a>
### Get unallocated repair cost

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_get_unallocated_repair_cost`

**Inputs** purchase\_invoice, expense\_account, exclude\_asset\_repair = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** float.

**Explicit results** 0.0 · \_get\_unallocated\_repair\_cost(purchase\_invoice, expense\_account, exclude\_asset\_repair).

**Local steps**

- If (not purchase\_invoice or not expense\_account).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not purchase\_invoice → not expense\_account.
  - Return 0.0.
- Evaluate Platform.has\_permission(“Purchase Invoice”, “read”, purchase\_invoice, throw = true).
- Return \_get\_unallocated\_repair\_cost(purchase\_invoice, expense\_account, exclude\_asset\_repair).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Purchase Invoice”, “read”, purchase\_invoice, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L579)

<a id="op-19750b6534fee8"></a>
### Get unallocated repair cost

`operation_enterprise_binding_enterprise_assets_doctype_asset_repair_asset_repair_get_unallocated_repair_cost`

**Inputs** purchase\_invoice, expense\_account, exclude\_asset\_repair = no value.

**Declared result** float.

**Explicit results** flt((total\_amount − used\_amount), precision).

**Local steps**

- Set used\_amount from get\_allocated\_repair\_cost(purchase\_invoice, expense\_account, exclude\_asset\_repair).
- Set total\_amount from get\_total\_expense\_amount(purchase\_invoice, expense\_account).
- Set precision from Platform.get\_precision(“Asset Repair Purchase Invoice”, “repair\_cost”).
- Return flt((total\_amount − used\_amount), precision).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L758) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1396)

<a id="op-e3120eba45983f"></a>
### Get allocated repair cost

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_get_allocated_repair_cost`

**Inputs** purchase\_invoice, expense\_account, exclude\_asset\_repair = no value.

**Declared result** float.

**Explicit results** flt(result at 0.total) when result, otherwise 0.0.

**Local steps**

- Set asset\_repair\_pi from DocType(“Asset Repair Purchase Invoice”).
- Set query from nested operand in the contract.qb.from\_(asset\_repair\_pi).select(Sum(nested operand in the contract.repair\_cost).as\_(“total”)).where(((asset\_repair\_pi.purchase\_invoice equals purchase\_invoice bitwise and as ….
- If exclude\_asset\_repair.
  - Set query from query.where(asset\_repair\_pi.parent differs from exclude\_asset\_repair).
- Set result from query.run(as\_dict = true).
- Return flt(result at 0.total) when result, otherwise 0.0.
  - Value choice on result — true gives flt(result at 0.total), false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0329.json#L2406) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L573)

<a id="op-7283908fedc2dc"></a>
### Get total expense amount

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_get_total_expense_amount`

**Inputs** purchase\_invoice, expense\_account.

**Declared result** float.

**Explicit results** flt(result at 0.total) when result, otherwise 0.0.

**Local steps**

- Set gl\_entry from DocType(“GL Entry”).
- Set result from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“total”)).where((((nested operand in the contract equals nested operand in the contract bitwise and  ….
- Return flt(result at 0.total) when result, otherwise 0.0.
  - Value choice on result — true gives flt(result at 0.total), false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0329.json#L2810) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L578)

## Record · Asset shift allocation

[Record definition](../../../../data/record-types/asset_shift_allocation.json)

<a id="op-27cdaa2767527d"></a>
### Asset Shift Allocation.validate

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_validate`

**Inputs** self.

**Local steps**

- Set self.asset\_depr\_schedule\_doc from get\_asset\_depr\_schedule\_doc(self.asset, “Active”, self.finance\_book).
- If self.get(“depreciation\_schedule”).
  - Evaluate self.set\_booked\_journal\_entries().
  - Evaluate self.validate\_invalid\_shift\_change().
  - Evaluate self.update\_depr\_schedule().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set booked journal entries](operations-017.md#op-4e5773398199ab), [validate invalid shift change](operations-017.md#op-a6eebcb4f846a8), [update depr schedule](operations-017.md#op-eec6b6f65679a6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1761) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L614)

<a id="op-027672f0384c29"></a>
### Asset Shift Allocation.after insert

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.fetch\_and\_set\_depr\_schedule().

If control reaches the end, it returns no value.

**Methods declared on this owner** [fetch and set depr schedule](operations-017.md#op-dbb78fc54e81d9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0330.json#L7032) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L605)

<a id="op-be36db4bb9d1e3"></a>
### Asset Shift Allocation.before submit

`operation_enterprise_binding_enterprise_assets_doctype_asset_shift_allocation_asset_shift_allocation_assetshiftallocation_before_submit`

**Inputs** self.

**Local steps**

- Set self.previous\_depreciation\_schedule from self.asset\_depr\_schedule\_doc.name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L760) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1398)

<a id="op-aa41ba4a5c6aab"></a>
### Asset Shift Allocation.on submit

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.create\_new\_asset\_depr\_schedule().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create new asset depr schedule](operations-017.md#op-0998b4dfeb8421).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0330.json#L7083) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1758) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L611)

<a id="op-89bd02aa03c0ce"></a>
### Asset Shift Allocation.on cancel

`operation_enterprise_binding_enterprise_assets_doctype_asset_shift_allocation_asset_shift_allocation_assetshiftallocation_on_cancel`

**Inputs** self.

**Local steps**

- If self.previous\_depreciation\_schedule.
  - Evaluate self.restore\_previous\_depr\_schedule().

If control reaches the end, it returns no value.

**Methods declared on this owner** [restore previous depr schedule](operations-017.md#op-2006ab75069db1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L762) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L2)

<a id="op-4e5773398199ab"></a>
### Asset Shift Allocation.set booked journal entries

`operation_enterprise_binding_enterprise_assets_doctype_asset_shift_allocation_asset_shift_allocation_assetshiftallocation_set_booked_journal_entries`

**Inputs** self.

**Local steps**

- Set journal\_entries from mapping of getdate(row.schedule\_date) → row.journal\_entry for row drawn from self.asset\_depr\_schedule\_doc.depreciation\_schedule.
  - Draw row from self.asset\_depr\_schedule\_doc.depreciation\_schedule.
- For each row in self.depreciation\_schedule.
  - Set row.journal\_entry from journal\_entries.get(getdate(row.schedule\_date)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L764) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L4)

<a id="op-a6eebcb4f846a8"></a>
### Asset Shift Allocation.validate invalid shift change

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_validate_invalid_shift_change`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Shift cannot be changed since the depreciation has already been processed”.format(i).

**Local steps**

- For each tuple(i, sch) in enumerate(self.depreciation\_schedule).
  - If (sch.journal\_entry and self.asset\_depr\_schedule\_doc.depreciation\_schedule at i.shift differs from sch.shift).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sch.journal\_entry → self.asset\_depr\_schedule\_doc.depreciation\_schedule at i.shift differs from sch.shift.
    - Call the validation error handler Platform.throw(translated “Row {0}: Shift cannot be changed since the depreciation has already been processed”.format(i)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1762) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L615)

<a id="op-eec6b6f65679a6"></a>
### Asset Shift Allocation.update depr schedule

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_update_depr_schedule`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_doc.

**Local steps**

- Evaluate self.adjust\_depr\_shifts().
- Set asset\_doc from Platform.get\_doc(“Asset”, self.asset).
- Set fb\_row from self.get\_finance\_book\_row(asset\_doc).
- Set temp\_depr\_schedule\_doc from get\_temp\_depr\_schedule\_doc(asset\_doc, fb\_row, updated\_depr\_schedule = self.depreciation\_schedule).
- Set self.depreciation\_schedule from list().
- Evaluate self.modify\_depr\_schedule(temp\_depr\_schedule\_doc.get(“depreciation\_schedule”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [adjust depr shifts](operations-017.md#op-fd70f0781a6d41), [get finance book row](operations-017.md#op-66d71694b18159), [modify depr schedule](operations-017.md#op-553ae431a9915f).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L192) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1760) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L613)

<a id="op-fd70f0781a6d41"></a>
### Asset Shift Allocation.adjust depr shifts

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_adjust_depr_shifts`

**Inputs** self.

**Local steps**

- Set shift\_factors\_map from get\_asset\_shift\_factors\_map().
- Set reverse\_shift\_factors\_map from mapping of v → k for tuple(k, v) drawn from shift\_factors\_map.items().
  - Draw tuple(k, v) from shift\_factors\_map.items().
- Set factor\_diff from self.calculate\_shift\_factor\_diff(shift\_factors\_map).
- If factor\_diff &gt; 0.
  - Evaluate self.reduce\_depr\_shifts(factor\_diff, shift\_factors\_map, reverse\_shift\_factors\_map).
- Otherwise.
  - If factor\_diff &lt; 0.
    - Evaluate self.add\_depr\_shifts(factor\_diff, shift\_factors\_map, reverse\_shift\_factors\_map).

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate shift factor diff](operations-017.md#op-c7faf5211b7fe8), [reduce depr shifts](operations-017.md#op-5e3ed8bd5d4b85), [add depr shifts](operations-017.md#op-a6ce14a799c5b7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L426) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L604)

<a id="op-c7faf5211b7fe8"></a>
### Asset Shift Allocation.calculate shift factor diff

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_calculate_shift_factor_diff`

**Inputs** self, shift\_factors\_map.

**Explicit results** (new\_shift\_sum − original\_shift\_sum).

**Local steps**

- Set original\_shift\_sum from sum(generator of shift\_factors\_map.get(schedule.shift, 0) for schedule drawn from self.asset\_depr\_schedule\_doc.depreciation\_schedule).
  - Draw schedule from self.asset\_depr\_schedule\_doc.depreciation\_schedule.
- Set new\_shift\_sum from sum(generator of shift\_factors\_map.get(schedule.shift, 0) for schedule drawn from self.depreciation\_schedule).
  - Draw schedule from self.depreciation\_schedule.
- Return (new\_shift\_sum − original\_shift\_sum).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L677) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L606)

<a id="op-5e3ed8bd5d4b85"></a>
### Asset Shift Allocation.reduce depr shifts

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_reduce_depr_shifts`

**Inputs** self, factor\_diff, shift\_factors\_map, reverse\_shift\_factors\_map.

**Explicit failure paths** validation helper — translated “The increase in shifts cannot be balanced by reducing the shifts of the rows after the changed rows”.

**Local steps**

- Set last\_changed\_index from self.get\_last\_changed\_row\_index().
- For each tuple(i, schedule) in reversed(list(enumerate(self.depreciation\_schedule))).
  - If (factor\_diff ≤ 0 or i ≤ last\_changed\_index).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in factor\_diff ≤ 0 → i ≤ last\_changed\_index.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set current\_factor from shift\_factors\_map.get(schedule.shift, 0).
  - If current\_factor ≤ factor\_diff.
    - Evaluate self.depreciation\_schedule.pop(i).
    - Update factor\_diff using − current\_factor.
  - Otherwise.
    - If new\_shift bound to reverse\_shift\_factors\_map.get((current\_factor − factor\_diff)).
      - Set self.depreciation\_schedule at i.shift from new\_shift.
      - Set factor\_diff from 0.
    - Otherwise.
      - Leave the innermost loop without its normal-exhaustion alternative.
- If factor\_diff &gt; 0.
  - Call the validation error handler Platform.throw(translated “The increase in shifts cannot be balanced by reducing the shifts of the rows after the changed rows”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get last changed row index](operations-017.md#op-04631b8e52d5b4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1759) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L612)

<a id="op-04631b8e52d5b4"></a>
### Asset Shift Allocation.get last changed row index

`operation_enterprise_binding_enterprise_assets_doctype_asset_shift_allocation_asset_shift_allocation_assetshiftallocation_get_last_changed_row_index`

**Inputs** self.

**Declared result** int.

**Explicit results** max(changed\_indexes, default = negative 1).

**Local steps**

- Set original\_schedule from (self.get\_doc\_before\_save() or self.asset\_depr\_schedule\_doc).depreciation\_schedule.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_doc\_before\_save() → self.asset\_depr\_schedule\_doc.
- Set changed\_indexes from list of i for tuple(i, schedule) drawn from enumerate(self.depreciation\_schedule) where (i ≥ len(original\_schedule) or schedule.shift differs from original\_schedule at i.shift).
  - Draw tuple(i, schedule) from enumerate(self.depreciation\_schedule), keep a combination only if ((i ≥ len(original\_schedule) or schedule.shift differs from original\_schedule at i.shift)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in i ≥ len(original\_schedule) → schedule.shift differs from original\_schedule at i.shift.
- Return max(changed\_indexes, default = negative 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L761) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1399)

<a id="op-a6ce14a799c5b7"></a>
### Asset Shift Allocation.add depr shifts

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_add_depr_shifts`

**Inputs** self, factor\_diff, shift\_factors\_map, reverse\_shift\_factors\_map.

**Explicit failure paths** validation helper — translated “Could not find a suitable shift to match the difference: {0}”.format(factor\_diff).

**Local steps**

- Set factor\_diff from abs(factor\_diff).
- Set shift\_factors from sorted(shift\_factors\_map.values(), reverse = true).
- While factor\_diff &gt; 0.
  - For each factor in shift\_factors.
    - If factor ≤ factor\_diff.
      - Evaluate self.add\_schedule\_row(factor, reverse\_shift\_factors\_map).
      - Update factor\_diff using − factor.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - After normal loop exhaustion.
    - Call the validation error handler Platform.throw(translated “Could not find a suitable shift to match the difference: {0}”.format(factor\_diff)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add schedule row](operations-017.md#op-d93fc756bd4cbd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L1192) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L602)

<a id="op-d93fc756bd4cbd"></a>
### Asset Shift Allocation.add schedule row

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_add_schedule_row`

**Inputs** self, factor, reverse\_shift\_factors\_map.

**Local steps**

- Set schedule\_date from add\_months(self.depreciation\_schedule at negative 1.schedule\_date, cint(self.asset\_depr\_schedule\_doc.frequency\_of\_depreciation)).
- If is\_last\_day\_of\_the\_month(self.depreciation\_schedule at negative 1.schedule\_date).
  - Set schedule\_date from get\_last\_day(schedule\_date).
- Evaluate self.append(“depreciation\_schedule”, mapping(“schedule\_date” → schedule\_date, “shift” → reverse\_shift\_factors\_map.get(factor))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L1475) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L603)

<a id="op-66d71694b18159"></a>
### Asset Shift Allocation.get finance book row

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_get_finance_book_row`

**Inputs** self, asset\_doc.

**Explicit results** asset\_doc.get(“finance\_books”) at (idx − 1).

**Local steps**

- Set idx from 0.
- For each d in asset\_doc.get(“finance\_books”).
  - If d.finance\_book equals self.finance\_book.
    - Set idx from d.idx.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return asset\_doc.get(“finance\_books”) at (idx − 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L1744) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1756) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L609)

<a id="op-553ae431a9915f"></a>
### Asset Shift Allocation.modify depr schedule

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_modify_depr_schedule`

**Inputs** self, temp\_depr\_schedule.

**Local steps**

- For each schedule in temp\_depr\_schedule.
  - Evaluate self.append(“depreciation\_schedule”, mapping(“schedule\_date” → schedule.schedule\_date, “depreciation\_amount” → schedule.depreciation\_amount, “accumulated\_depreciation\_amount” → schedule.accumulated\_depreci ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L1925) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1757) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L610)

<a id="op-dbb78fc54e81d9"></a>
### Asset Shift Allocation.fetch and set depr schedule

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_fetch_and_set_depr_schedule`

**Inputs** self.

**State and service calls** call save on self.

**Explicit failure paths** validation helper — translated “Asset Depreciation Schedule for Asset {0} and Finance Book {1} is not using shift based depreciation”.format(self.asset, self.finance\_book) · validation helper — translated “Asset Depreciation Schedule not found for Asset {0} and Finance Book {1}”.format(self.asset, self.finance\_book).

**Local steps**

- If self.asset\_depr\_schedule\_doc.
  - If self.asset\_depr\_schedule\_doc.shift\_based.
    - Evaluate self.modify\_depr\_schedule(self.asset\_depr\_schedule\_doc.depreciation\_schedule).
    - Set self.flags.ignore\_validate from true.
    - Evaluate self.save().
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Asset Depreciation Schedule for Asset {0} and Finance Book {1} is not using shift based depreciation”.format(self.asset, self.finance\_book)).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Asset Depreciation Schedule not found for Asset {0} and Finance Book {1}”.format(self.asset, self.finance\_book)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [modify depr schedule](operations-017.md#op-553ae431a9915f).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0331.json#L2111) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1755) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L608)

<a id="op-0998b4dfeb8421"></a>
### Asset Shift Allocation.create new asset depr schedule

`operation_enterprise_assets_record_definitions_asset_shift_allocation_business_behavior_asset_shift_allocation_create_new_asset_depr_schedule`

**Inputs** self.

**State and service calls** request copy\_doc for self.asset\_depr\_schedule\_doc.

**Local steps**

- Set new\_asset\_depr\_schedule\_doc from Platform.copy\_doc(self.asset\_depr\_schedule\_doc).
- Set new\_asset\_depr\_schedule\_doc.depreciation\_schedule from list().
- For each schedule in self.depreciation\_schedule.
  - Evaluate new\_asset\_depr\_schedule\_doc.append(“depreciation\_schedule”, mapping(“schedule\_date” → schedule.schedule\_date, “depreciation\_amount” → schedule.depreciation\_amount, “accumulated\_depreciation\_amount” → sched ….
- Set notes from translated “This schedule was created when Asset {0}'s shifts were adjusted through Asset Shift Allocation {1}.”.format(get\_link\_to\_form(“Asset”, self.asset), get\_link\_to\_form(self.doctype, self.name)).
- Set new\_asset\_depr\_schedule\_doc.notes from notes.
- Evaluate replace\_active\_depr\_schedule(self.asset\_depr\_schedule\_doc, new\_asset\_depr\_schedule\_doc).
- Evaluate add\_asset\_activity(self.asset, translated “Asset's depreciation schedule updated after Asset Shift Allocation {0}”.format(get\_link\_to\_form(self.doctype, self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1754) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L607)

<a id="op-2006ab75069db1"></a>
### Asset Shift Allocation.restore previous depr schedule

`operation_enterprise_binding_enterprise_assets_doctype_asset_shift_allocation_asset_shift_allocation_assetshiftallocation_restore_previous_depr_schedule`

**Inputs** self.

**Record and data access** resolve a document from “Asset Depreciation Schedule” via get\_doc.

**State and service calls** request copy\_doc for Platform.get\_doc(“Asset Depreciation Schedule”, self.previous\_depreciation\_schedule).

**Local steps**

- Set active\_schedule\_doc from get\_asset\_depr\_schedule\_doc(self.asset, “Active”, self.finance\_book).
- Evaluate self.validate\_previous\_depr\_schedule\_restorable(active\_schedule\_doc).
- Set restored\_schedule\_doc from Platform.copy\_doc(Platform.get\_doc(“Asset Depreciation Schedule”, self.previous\_depreciation\_schedule)).
- Set restored\_schedule\_doc.notes from translated “This schedule was restored when Asset Shift Allocation {0} was cancelled.”.format(get\_link\_to\_form(self.doctype, self.name)).
- Evaluate replace\_active\_depr\_schedule(active\_schedule\_doc, restored\_schedule\_doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate previous depr schedule restorable](operations-017.md#op-f7ecd08a359138).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L763) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L3)

<a id="op-f7ecd08a359138"></a>
### Asset Shift Allocation.validate previous depr schedule restorable

`operation_enterprise_binding_enterprise_assets_doctype_asset_shift_allocation_asset_shift_allocation_assetshiftallocation_validate_previous_depr_schedule_restorable`

**Inputs** self, active\_schedule\_doc.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Cannot cancel since the asset's depreciation schedule has changed or depreciation has been posted after this …”.

**Local steps**

- If get\_schedule\_rows(active\_schedule\_doc.depreciation\_schedule) differs from get\_schedule\_rows(self.depreciation\_schedule).
  - Call the validation error handler Platform.throw(translated “Cannot cancel since the asset's depreciation schedule has changed or depreciation has been posted after this …”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L765) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L5)
