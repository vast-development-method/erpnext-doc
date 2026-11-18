# Asset management · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset depreciation schedule

[Record definition](../../../../data/record-types/asset_depreciation_schedule.json)

<a id="op-f8c5495f7de44c"></a>
### Asset Depreciation Schedule.validate

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_asset_depreciation_schedule_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_another\_asset\_depr\_schedule\_does\_not\_exist().
- If not self.finance\_book\_id.
  - Evaluate self.create\_depreciation\_schedule().
- Evaluate self.update\_shift\_depr\_schedule().
- Evaluate self.validate\_manual\_schedule().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate another asset depr schedule does not exist](operations-010.md#op-d4438f366e8dd4), [update shift depr schedule](operations-010.md#op-21d8677f250130), [validate manual schedule](operations-010.md#op-1472c11fbf17c6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1551) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L431)

<a id="op-d4438f366e8dd4"></a>
### Asset Depreciation Schedule.validate another asset depr schedule does not exist

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_asset_depreciation_schedule_validate_another_asset_depr_schedule_does_not_exist`

**Inputs** self.

**Record and data access** read “Asset Depreciation Schedule” via exists.

**Explicit failure paths** validation helper — translated “Asset Depreciation Schedule {0} for Asset {1} and Finance Book {2} already exists.”.format(asset\_depr\_schedule, self.asset, self.finance\_book) · validation helper — translated “Asset Depreciation Schedule {0} for Asset {1} already exists.”.format(asset\_depr\_schedule, self.asset).

**Local steps**

- Set finance\_book\_filter from list(“finance\_book”, “is”, “not set”).
- If self.finance\_book.
  - Set finance\_book\_filter from list(“finance\_book”, “=”, self.finance\_book).
- Set asset\_depr\_schedule from Platform.db.exists(“Asset Depreciation Schedule”, list(list(“asset”, “=”, self.asset), finance\_book\_filter, list(“docstatus”, “&lt;”, 2))).
- If (asset\_depr\_schedule and asset\_depr\_schedule differs from self.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in asset\_depr\_schedule → asset\_depr\_schedule differs from self.name.
  - If self.finance\_book.
    - Call the validation error handler Platform.throw(translated “Asset Depreciation Schedule {0} for Asset {1} and Finance Book {2} already exists.”.format(asset\_depr\_schedule, self.asset, self.finance\_book)).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Asset Depreciation Schedule {0} for Asset {1} already exists.”.format(asset\_depr\_schedule, self.asset)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L681) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1552) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L432)

<a id="op-1472c11fbf17c6"></a>
### Asset Depreciation Schedule.validate manual schedule

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_asset_depreciation_schedule_assetdepreciationschedule_validate_manual_schedule`

**Inputs** self.

**Record and data access** read “Asset” via get\_value.

**Explicit results** no value.

**Local steps**

- If (self.depreciation\_method differs from “Manual” or self.flags.is\_rescheduled).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.depreciation\_method differs from “Manual” → self.flags.is\_rescheduled.
  - Return no value.
- Set available\_for\_use\_date from Platform.db.get\_value(“Asset”, self.asset, “available\_for\_use\_date”).
- For each row in self.get(“depreciation\_schedule”).
  - Evaluate self.validate\_manual\_row(row, available\_for\_use\_date).
- Evaluate self.validate\_manual\_total().
- Evaluate self.set\_accumulated\_depreciation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate manual row](operations-010.md#op-330a6af3762ff6), [validate manual total](operations-010.md#op-e21699c0b17fee).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L715) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1353)

<a id="op-330a6af3762ff6"></a>
### Asset Depreciation Schedule.validate manual row

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_asset_depreciation_schedule_assetdepreciationschedule_validate_manual_row`

**Inputs** self, row, available\_for\_use\_date.

**Explicit failure paths** validation helper — translated “Row #{0}: Depreciation Amount must be greater than zero”.format(row.idx) · validation helper — translated “Row #{0}: Schedule Date cannot be before the Available-for-use Date {1}”.format(row.idx, Platform.format(available\_for\_use\_date, “Date”)).

**Local steps**

- If flt(row.depreciation\_amount) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Depreciation Amount must be greater than zero”.format(row.idx)).
- If getdate(row.schedule\_date) &lt; getdate(available\_for\_use\_date).
  - Call the validation error handler Platform.throw(translated “Row #{0}: Schedule Date cannot be before the Available-for-use Date {1}”.format(row.idx, Platform.format(available\_for\_use\_date, “Date”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L714) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1352)

<a id="op-e21699c0b17fee"></a>
### Asset Depreciation Schedule.validate manual total

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_asset_depreciation_schedule_assetdepreciationschedule_validate_manual_total`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Total Depreciation Amount {0} must be equal to the depreciable value {1}”.format(Platform.bold(Platform.format(pending\_amount, “Currency”)), Platform.bold(Platform.format(depreciable\_amount, “C ….

**Local steps**

- Set precision from self.precision(“value\_after\_depreciation”).
- Set pending\_amount from sum(generator of flt(row.depreciation\_amount) for row drawn from self.depreciation\_schedule where not row.journal\_entry).
  - Draw row from self.depreciation\_schedule, keep a combination only if (not row.journal\_entry).
- Set depreciable\_amount from (flt(self.value\_after\_depreciation) − flt(self.expected\_value\_after\_useful\_life)).
- If flt(pending\_amount, precision) differs from flt(depreciable\_amount, precision).
  - Call the validation error handler Platform.throw(translated “Total Depreciation Amount {0} must be equal to the depreciable value {1}”.format(Platform.bold(Platform.format(pending\_amount, “Currency”)), Platform.bold(Platform.format(depreci ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1354)

<a id="op-19f1485666fdba"></a>
### Asset Depreciation Schedule.on submit

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_asset_depreciation_schedule_on_submit`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.validate\_asset().
- Evaluate self.db\_set(“status”, “Active”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate asset](operations-010.md#op-087fc3d429b39a).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L1072) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1549) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L429)

<a id="op-087fc3d429b39a"></a>
### Asset Depreciation Schedule.validate asset

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_asset_depreciation_schedule_validate_asset`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_doc.

**Explicit failure paths** validation helper — translated “Asset {0} is not set to calculate depreciation.”.format(get\_link\_to\_form(“Asset”, self.asset)) · validation helper — translated “Asset {0} is not submitted. Please submit the asset before proceeding.”.format(get\_link\_to\_form(“Asset”, self.asset)).

**Local steps**

- Set asset from Platform.get\_doc(“Asset”, self.asset).
- If not asset.calculate\_depreciation.
  - Call the validation error handler Platform.throw(translated “Asset {0} is not set to calculate depreciation.”.format(get\_link\_to\_form(“Asset”, self.asset))).
- <a id="op-087fc3d429b39a-guard-9"></a>If asset.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Asset {0} is not submitted. Please submit the asset before proceeding.”.format(get\_link\_to\_form(“Asset”, self.asset))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison asset.docstatus differs from 1, asset.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Asset {0} is not submitted. Please submit the asset before proceeding.”.format(get\_link\_to\_form(“Asset”, self.asset)). With asset.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-087fc3d429b39a-guard-9)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L1156) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1553) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L433)

<a id="op-b540cf34de0fe2"></a>
### Asset Depreciation Schedule.before cancel

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_asset_depreciation_schedule_assetdepreciationschedule_before_cancel`

**Inputs** self.

**Record and data access** read “Asset” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot cancel the depreciation schedule of submitted Asset {0}. Cancel the Asset instead.”.format(get\_link\_to\_form(“Asset”, self.asset)).

**Local steps**

- If self.flags.should\_not\_cancel\_depreciation\_entries.
  - Return no value.
- If Platform.db.get\_value(“Asset”, self.asset, “docstatus”) equals 1.
  - Call the validation error handler Platform.throw(translated “Cannot cancel the depreciation schedule of submitted Asset {0}. Cancel the Asset instead.”.format(get\_link\_to\_form(“Asset”, self.asset))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1351)

<a id="op-f89d731431021c"></a>
### Asset Depreciation Schedule.on cancel

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_asset_depreciation_schedule_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).
- If not self.flags.should\_not\_cancel\_depreciation\_entries.
  - Evaluate self.cancel\_depreciation\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [cancel depreciation entries](operations-010.md#op-c4ed70e7020f1c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L1434) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1548) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L428)

<a id="op-c4ed70e7020f1c"></a>
### Asset Depreciation Schedule.cancel depreciation entries

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_asset_depreciation_schedule_cancel_depreciation_entries`

**Inputs** self.

**Record and data access** read “Journal Entry” via get\_value · resolve a document from “Journal Entry” via get\_doc.

**State and service calls** call cancel on Platform.get\_doc(“Journal Entry”, d.journal\_entry).

**Explicit failure paths** validation helper — translated “Cannot cancel Asset Depreciation Schedule {0} as it has a draft journal entry {1}.”.format(self.name, d.journal\_entry).

**Local steps**

- For each d in self.get(“depreciation\_schedule”).
  - If d.journal\_entry.
    - Set je\_status from Platform.db.get\_value(“Journal Entry”, d.journal\_entry, “docstatus”).
    - If je\_status equals 0.
      - Call the validation error handler Platform.throw(translated “Cannot cancel Asset Depreciation Schedule {0} as it has a draft journal entry {1}.”.format(self.name, d.journal\_entry)).
    - Evaluate Platform.get\_doc(“Journal Entry”, d.journal\_entry).cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L1540) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L425)

<a id="op-21d8677f250130"></a>
### Asset Depreciation Schedule.update shift depr schedule

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_asset_depreciation_schedule_update_shift_depr_schedule`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.shift\_based or self.docstatus differs from 0 or self.get(“\_\_islocal”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.shift\_based → self.docstatus differs from 0 → self.get(“\_\_islocal”).
  - Return no value.
- Evaluate self.create\_depreciation\_schedule().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L1815) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1550) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L430)

<a id="op-02a913307facca"></a>
### Asset Depreciation Schedule.get finance book row

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_asset_depreciation_schedule_get_finance_book_row`

**Inputs** self, fb\_row = no value.

**Record and data access** read “Asset Finance Book” via get\_value · resolve a document from “Asset Finance Book” via get\_doc.

**Explicit results** no value.

**Local steps**

- If fb\_row.
  - Set self.fb\_row from fb\_row.
  - Return no value.
- Set finance\_book\_filter from list(“finance\_book”, “is”, “not set”).
- If self.finance\_book.
  - Set finance\_book\_filter from list(“finance\_book”, “=”, self.finance\_book).
- Set asset\_finance\_book\_name from Platform.db.get\_value(doctype = “Asset Finance Book”, filters = list(list(“parent”, “=”, self.asset), finance\_book\_filter)).
- Set self.fb\_row from Platform.get\_doc(“Asset Finance Book”, asset\_finance\_book\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L1934) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L427)

<a id="op-e47d29036be067"></a>
### Asset Depreciation Schedule.fetch asset details

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_asset_depreciation_schedule_fetch_asset_details`

**Inputs** self.

**Local steps**

- Set self.asset from self.asset\_doc.name.
- Set self.finance\_book from self.fb\_row.get(“finance\_book”).
- Set self.finance\_book\_id from self.fb\_row.idx.
- Set self.opening\_accumulated\_depreciation from (self.asset\_doc.opening\_accumulated\_depreciation or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.asset\_doc.opening\_accumulated\_depreciation → 0.
- Set self.opening\_number\_of\_booked\_depreciations from (self.asset\_doc.opening\_number\_of\_booked\_depreciations or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.asset\_doc.opening\_number\_of\_booked\_depreciations → 0.
- Set self.net\_purchase\_amount from self.asset\_doc.net\_purchase\_amount.
- Set self.depreciation\_method from self.fb\_row.depreciation\_method.
- Set self.total\_number\_of\_depreciations from self.fb\_row.total\_number\_of\_depreciations.
- Set self.frequency\_of\_depreciation from self.fb\_row.frequency\_of\_depreciation.
- Set self.rate\_of\_depreciation from self.fb\_row.get(“rate\_of\_depreciation”).
- Set self.value\_after\_depreciation from self.fb\_row.value\_after\_depreciation.
- Set self.expected\_value\_after\_useful\_life from self.fb\_row.get(“expected\_value\_after\_useful\_life”).
- Set self.daily\_prorata\_based from self.fb\_row.get(“daily\_prorata\_based”).
- Set self.shift\_based from self.fb\_row.get(“shift\_based”).
- Set self.status from “Draft”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L2213) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L426)

<a id="op-e61a28f9954c3e"></a>
### Make draft asset depr schedule

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_make_draft_asset_depr_schedule`

**Inputs** asset\_doc, row.

**State and service calls** request new\_doc for “Asset Depreciation Schedule” · call insert on asset\_depr\_schedule\_doc.

**Explicit results** asset\_depr\_schedule\_doc.name.

**Local steps**

- Set asset\_depr\_schedule\_doc from Platform.new\_doc(“Asset Depreciation Schedule”).
- Evaluate asset\_depr\_schedule\_doc.create\_depreciation\_schedule(asset\_doc, row).
- Evaluate asset\_depr\_schedule\_doc.insert().
- Return asset\_depr\_schedule\_doc.name.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L2716) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1563) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L443)

<a id="op-8a8ed91e30fd4a"></a>
### Convert draft asset depr schedules into active

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_convert_draft_asset_depr_schedules_into_active`

**Inputs** asset\_doc.

**State and service calls** call submit on asset\_depr\_schedule\_doc.

**Local steps**

- For each row in asset\_doc.get(“finance\_books”).
  - Set asset\_depr\_schedule\_doc from get\_asset\_depr\_schedule\_doc(asset\_doc.name, “Draft”, row.finance\_book).
  - If not asset\_depr\_schedule\_doc.
    - Continue with the next iteration or loop test.
  - Evaluate asset\_depr\_schedule\_doc.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L2846) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L435)

<a id="op-ffa1c83beb3785"></a>
### Cancel asset depr schedules

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_cancel_asset_depr_schedules`

**Inputs** asset\_doc.

**State and service calls** call cancel on asset\_depr\_schedule\_doc.

**Local steps**

- For each row in asset\_doc.get(“finance\_books”).
  - Set asset\_depr\_schedule\_doc from get\_asset\_depr\_schedule\_doc(asset\_doc.name, “Active”, row.finance\_book).
  - If not asset\_depr\_schedule\_doc.
    - Continue with the next iteration or loop test.
  - Evaluate asset\_depr\_schedule\_doc.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L2994) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1554) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L434)

<a id="op-481208901defdb"></a>
### Reschedule depreciation

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_reschedule_depreciation`

**Inputs** asset\_doc, notes, disposal\_date = no value.

**State and service calls** request copy\_doc for current\_schedule · request new\_doc for “Asset Depreciation Schedule” · call cancel on current\_schedule · call submit on new\_schedule.

**Local steps**

- For each row in asset\_doc.get(“finance\_books”).
  - Set current\_schedule from get\_asset\_depr\_schedule\_doc(asset\_doc.name, no value, row.finance\_book).
  - If (disposal\_date and flt(row.value\_after\_depreciation) ≤ flt(row.expected\_value\_after\_useful\_life)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in disposal\_date → flt(row.value\_after\_depreciation) ≤ flt(row.expected\_value\_after\_useful\_life).
    - Continue with the next iteration or loop test.
  - If current\_schedule.
    - If current\_schedule.docstatus equals 1.
      - Set new\_schedule from Platform.copy\_doc(current\_schedule).
    - Otherwise.
      - If current\_schedule.docstatus equals 0.
        - Set new\_schedule from current\_schedule.
  - Otherwise.
    - Set new\_schedule from Platform.new\_doc(“Asset Depreciation Schedule”).
    - Set new\_schedule.asset from asset\_doc.name.
  - Evaluate set\_modified\_depreciation\_rate(asset\_doc, row, new\_schedule).
  - Evaluate new\_schedule.create\_depreciation\_schedule(row, disposal\_date).
  - Set new\_schedule.notes from notes.
  - Set new\_schedule.flags.is\_rescheduled from true.
  - If (current\_schedule and current\_schedule.docstatus equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_schedule → current\_schedule.docstatus equals 1.
    - Set current\_schedule.flags.should\_not\_cancel\_depreciation\_entries from true.
    - Set current\_schedule.flags.ignore\_permissions from true.
    - Evaluate current\_schedule.cancel().
  - Set new\_schedule.flags.ignore\_permissions from true.
  - Evaluate new\_schedule.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1565) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L445)

<a id="op-052d9d8eeca43d"></a>
### Set modified depreciation rate

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_set_modified_depreciation_rate`

**Inputs** asset\_doc, row, new\_schedule.

**State and service calls** call db\_set on row.

**Local steps**

- If (row.depreciation\_method belongs to tuple(“Written Down Value”, “Double Declining Balance”) and not is\_depreciation\_rate\_entered(asset\_doc, row)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.depreciation\_method belongs to tuple(“Written Down Value”, “Double Declining Balance”) → not is\_depreciation\_rate\_entered(asset\_doc, row).
  - Set new\_rate\_of\_depreciation from flt(asset\_doc.get\_depreciation\_rate(row), row.precision(“rate\_of\_depreciation”)).
  - Evaluate row.db\_set(“rate\_of\_depreciation”, new\_rate\_of\_depreciation).
  - Set new\_schedule.rate\_of\_depreciation from new\_rate\_of\_depreciation.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1566) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L446)

<a id="op-634cdb35835b8c"></a>
### Is depreciation rate entered

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_asset_depreciation_schedule_is_depreciation_rate_entered`

**Inputs** asset\_doc, row.

**Declared result** bool.

**Explicit results** true · (bool(first\_schedule) and asset\_doc.is\_entered\_depreciation\_rate(first\_schedule)).

**Local steps**

- If row.is\_rate\_of\_depreciation\_entered.
  - Return true.
- Set first\_schedule from get\_first\_depreciation\_schedule(asset\_doc.name, row.finance\_book).
- Return (bool(first\_schedule) and asset\_doc.is\_entered\_depreciation\_rate(first\_schedule)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(first\_schedule) → asset\_doc.is\_entered\_depreciation\_rate(first\_schedule).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1357)

<a id="op-0bad81ab00a08d"></a>
### Get first depreciation schedule

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_asset_depreciation_schedule_get_first_depreciation_schedule`

**Inputs** asset, finance\_book.

**Declared result** (dict bitwise or no value).

**Record and data access** read “Asset Depreciation Schedule” via get\_all.

**Explicit results** schedules at 0 when schedules, otherwise no value.

**Local steps**

- Set schedules from Platform.get\_all(“Asset Depreciation Schedule”, filters = mapping(“asset” → asset, “finance\_book” → (finance\_book or list(“is”, “not set”))), fields = list(“depreciation\_method”, “rate\_of\_depreciation”, “e ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in finance\_book → list(“is”, “not set”).
- Return schedules at 0 when schedules, otherwise no value.
  - Value choice on schedules — true gives schedules at 0, false gives no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L718) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1356)

<a id="op-a209910ac7878b"></a>
### Get temp depr schedule doc

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_get_temporary_depr_schedule_record`

**Inputs** asset\_doc, fb\_row, disposal\_date = no value, updated\_depr\_schedule = no value.

**State and service calls** request copy\_doc for current\_schedule.

**Explicit results** temp\_schedule\_doc.

**Local steps**

- Set current\_schedule from get\_current\_asset\_depr(asset\_doc, fb\_row).
- Set temp\_schedule\_doc from Platform.copy\_doc(current\_schedule).
- If updated\_depr\_schedule.
  - Evaluate modify\_depreciation\_dchedule(temp\_schedule\_doc, updated\_depr\_schedule).
- Evaluate temp\_schedule\_doc.create\_depreciation\_schedule(fb\_row, disposal\_date).
- Return temp\_schedule\_doc.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L3861) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1561) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L441)

<a id="op-1080f8f4a40011"></a>
### Get current asset depr

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_get_current_asset_depr`

**Inputs** asset\_doc, row.

**Explicit results** current\_schedule.

**Explicit failure paths** validation helper — translated “Asset Depreciation Schedule not found for Asset {0} and Finance Book {1}”.format(get\_link\_to\_form(“Asset”, asset\_doc.name), row.finance\_book).

**Local steps**

- Set current\_schedule from get\_asset\_depr\_schedule\_doc(asset\_doc.name, “Active”, row.finance\_book).
- If not current\_schedule.
  - Call the validation error handler Platform.throw(translated “Asset Depreciation Schedule not found for Asset {0} and Finance Book {1}”.format(get\_link\_to\_form(“Asset”, asset\_doc.name), row.finance\_book)).
- Return current\_schedule.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L4049) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1559) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L439)

<a id="op-ada793cdc75340"></a>
### Modify depreciation dchedule

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_modify_depreciation_dchedule`

**Inputs** temp\_schedule\_doc, updated\_depr\_schedule.

**Local steps**

- Set temp\_schedule\_doc.depreciation\_schedule from list().
- For each schedule in updated\_depr\_schedule.
  - Evaluate temp\_schedule\_doc.append(“depreciation\_schedule”, mapping(“schedule\_date” → schedule.schedule\_date, “depreciation\_amount” → schedule.depreciation\_amount, “accumulated\_depreciation\_amount” → schedule.accumu ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L4246) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1564) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L444)

<a id="op-2833f07dd1a41b"></a>
### Get asset shift factors map

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_get_asset_shift_factors_map`

**Inputs** no declared parameters.

**Record and data access** read “Asset Shift Factor” via get\_all.

**Explicit results** dict(Platform.db.get\_all(“Asset Shift Factor”, list(“shift\_name”, “shift\_factor”), as\_list = true)).

**Local steps**

- Return dict(Platform.db.get\_all(“Asset Shift Factor”, list(“shift\_name”, “shift\_factor”), as\_list = true)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L4449) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1558) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L438)
