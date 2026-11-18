# Asset management · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset depreciation schedule

[Record definition](../../../../data/record-types/asset_depreciation_schedule.json)

<a id="op-1d097be6375c93"></a>
### Get asset depreciation schedule

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_asset_depreciation_schedule_get_asset_depreciation_schedule`

**Inputs** asset\_name, status = no value, finance\_book = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_asset\_depr\_schedule\_doc(asset\_name, status, finance\_book).

**Local steps**

- Evaluate Platform.has\_permission(“Asset”, “read”, asset\_name, throw = true).
- Return get\_asset\_depr\_schedule\_doc(asset\_name, status, finance\_book).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset”, “read”, asset\_name, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1355)

<a id="op-88a9c77cd8de60"></a>
### Get depr schedule

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_get_depr_schedule`

**Inputs** asset\_name, status, finance\_book = no value.

**Explicit results** no value · asset\_depr\_schedule\_doc.get(“depreciation\_schedule”).

**Local steps**

- Set asset\_depr\_schedule\_doc from get\_asset\_depr\_schedule\_doc(asset\_name, status, finance\_book).
- If not asset\_depr\_schedule\_doc.
  - Return no value.
- Return asset\_depr\_schedule\_doc.get(“depreciation\_schedule”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1560) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L440)

<a id="op-0ee646bf380ffb"></a>
### Get asset depr schedule doc

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_get_asset_depr_schedule_record`

**Inputs** asset\_name, status = no value, finance\_book = no value.

**Record and data access** resolve a document from “Asset Depreciation Schedule” via get\_doc.

**Explicit results** no value · asset\_depr\_schedule\_doc.

**Local steps**

- Set asset\_depr\_schedule from get\_asset\_depr\_schedule\_name(asset\_name, status, finance\_book).
- If not asset\_depr\_schedule.
  - Return no value.
- Set asset\_depr\_schedule\_doc from Platform.get\_doc(“Asset Depreciation Schedule”, asset\_depr\_schedule at 0.name).
- Return asset\_depr\_schedule\_doc.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1557) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L437)

<a id="op-fd8bbbf06414e6"></a>
### Get asset depr schedule name

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_get_asset_depr_schedule_name`

**Inputs** asset\_name, status = no value, finance\_book = no value.

**Record and data access** read “Asset Depreciation Schedule” via get\_all.

**Explicit results** Platform.get\_all(doctype = “Asset Depreciation Schedule”, filters = filters, limit = 1).

**Local steps**

- Set filters from list(list(“asset”, “=”, asset\_name), list(“docstatus”, “&lt;”, 2)).
- If status.
  - If isinstance(status, str).
    - Set status from list(status).
  - Evaluate filters.append(list(“status”, “in”, status)).
- If finance\_book.
  - Evaluate filters.append(list(“finance\_book”, “=”, finance\_book)).
- Otherwise.
  - Evaluate filters.append(list(“finance\_book”, “is”, “not set”)).
- Return Platform.get\_all(doctype = “Asset Depreciation Schedule”, filters = filters, limit = 1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1556) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L436)

<a id="op-d63cd9ce0d4e06"></a>
### Is first day of the month

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_business_behavior_is_first_day_of_the_month`

**Inputs** date.

**Explicit results** getdate(first\_day\_of\_the\_month) equals getdate(date).

**Local steps**

- Set first\_day\_of\_the\_month from get\_first\_day(date).
- Return getdate(first\_day\_of\_the\_month) equals getdate(date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L5320) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1562) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L442)

<a id="op-b2352243dda8eb"></a>
### Depreciation Schedule Controller.initialize

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L5423) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L468)

<a id="op-81cfb1645d8846"></a>
### Depreciation Schedule Controller.create depreciation schedule

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_create_depreciation_schedule`

**Inputs** self, fb\_row = no value, disposal\_date = no value.

**Record and data access** resolve a document from “Asset” via get\_doc.

**Local steps**

- Set self.disposal\_date from disposal\_date.
- Set self.asset\_doc from Platform.get\_doc(“Asset”, self.asset).
- Evaluate self.get\_finance\_book\_row(fb\_row).
- Evaluate self.fetch\_asset\_details().
- Evaluate self.clear().
- Evaluate self.create().
- Evaluate self.set\_accumulated\_depreciation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear](operations-011.md#op-624a780500bd5d), [create](operations-011.md#op-249d6604bbec21), [set accumulated depreciation](operations-012.md#op-01e243101ddff5).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L5506) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1572) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L452)

<a id="op-624a780500bd5d"></a>
### Depreciation Schedule Controller.clear

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_clear`

**Inputs** self.

**Local steps**

- Set rows from self.get(“depreciation\_schedule”).
- Set self.schedules\_before\_clearing from rows.
- Set gap\_idx from next(generator of idx for tuple(idx, row) drawn from enumerate(rows) where not row.journal\_entry, no value).
  - Draw tuple(idx, row) from enumerate(rows), keep a combination only if (not row.journal\_entry).
- Set self.first\_non\_depreciated\_row\_idx from len(rows) when gap\_idx is identical to no value, otherwise gap\_idx.
  - Value choice on gap\_idx is identical to no value — true gives len(rows), false gives gap\_idx.
- Set self.depreciation\_schedule from list(rows) when gap\_idx is identical to no value, otherwise rows at slice no value to gap\_idx.
  - Value choice on gap\_idx is identical to no value — true gives list(rows), false gives rows at slice no value to gap\_idx.
- Set self.booked\_rows\_after\_gap from list() when gap\_idx is identical to no value, otherwise list of row for row drawn from rows at slice gap\_idx to no value where row.journal\_entry.
  - Value choice on gap\_idx is identical to no value — true gives list(), false gives list of row for row drawn from rows at slice gap\_idx to no value where row.journal\_entry.
  - Draw row from rows at slice gap\_idx to no value, keep a combination only if (row.journal\_entry).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1570) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L450)

<a id="op-249d6604bbec21"></a>
### Depreciation Schedule Controller.create

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_create`

**Inputs** self.

**Local steps**

- Evaluate self.initialize\_variables().
- For each row\_idx in range(self.first\_non\_depreciated\_row\_idx, self.final\_number\_of\_depreciations).
  - If self.skip\_row.
    - Continue with the next iteration or loop test.
  - Evaluate self.has\_fiscal\_year\_changed(row\_idx).
  - If self.fiscal\_year\_changed.
    - Set self.yearly\_opening\_wdv from self.pending\_depreciation\_amount.
  - Evaluate self.get\_prev\_depreciation\_amount(row\_idx).
  - Set self.schedule\_date from self.get\_next\_schedule\_date(row\_idx).
  - If self.add\_booked\_row(self.schedule\_date).
    - Continue with the next iteration or loop test.
  - Set self.depreciation\_amount from self.get\_depreciation\_amount(row\_idx).
  - If (self.disposal\_date and getdate(self.schedule\_date) ≥ getdate(self.disposal\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.disposal\_date → getdate(self.schedule\_date) ≥ getdate(self.disposal\_date).
    - Evaluate self.set\_depreciation\_amount\_for\_disposal(row\_idx).
    - Leave the innermost loop without its normal-exhaustion alternative.
  - If row\_idx equals 0.
    - Evaluate self.set\_depreciation\_amount\_for\_first\_row(row\_idx).
  - Otherwise.
    - If (self.has\_pro\_rata and row\_idx equals (cint(self.final\_number\_of\_depreciations) − 1)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_pro\_rata → row\_idx equals (cint(self.final\_number\_of\_depreciations) − 1).
      - Evaluate self.set\_depreciation\_amount\_for\_last\_row(row\_idx).
  - Set self.depreciation\_amount from flt(self.depreciation\_amount, self.asset\_doc.precision(“net\_purchase\_amount”)).
  - If not self.depreciation\_amount.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set self.pending\_depreciation\_amount from flt((self.pending\_depreciation\_amount − self.depreciation\_amount), self.asset\_doc.precision(“net\_purchase\_amount”)).
  - Evaluate self.adjust\_depr\_amount\_for\_salvage\_value(row\_idx).
  - If flt(self.depreciation\_amount, self.asset\_doc.precision(“net\_purchase\_amount”)) &gt; 0.
    - Evaluate self.add\_depr\_schedule\_row(row\_idx).
- Evaluate self.add\_remaining\_booked\_rows().

If control reaches the end, it returns no value.

**Methods declared on this owner** [initialize variables](operations-011.md#op-a93578b1550e64), [has fiscal year changed](operations-012.md#op-b97bd347dbe099), [get prev depreciation amount](operations-012.md#op-affe93fe00aa3d), [get next schedule date](operations-012.md#op-5ae60102d954bd), [add booked row](operations-011.md#op-de3004585db8ec), [get depreciation amount](operations-012.md#op-0d1d503c1d6ba3), [set depreciation amount for disposal](operations-012.md#op-4348be19ef7be9), [set depreciation amount for first row](operations-012.md#op-9c4151dbe7380c), [set depreciation amount for last row](operations-012.md#op-8bb0db2dddf9ab), [adjust depr amount for salvage value](operations-012.md#op-48a61b0389d95d), [add depr schedule row](operations-012.md#op-bf3ba36ececf47), [add remaining booked rows](operations-011.md#op-07ff3f23b82688).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1571) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L451)

<a id="op-de3004585db8ec"></a>
### Depreciation Schedule Controller.add booked row

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_deppreciation_schedule_controller_depreciationschedulecontroller_add_booked_row`

**Inputs** self, schedule\_date.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Set booked\_row from next(generator of row for row drawn from self.booked\_rows\_after\_gap where getdate(row.schedule\_date) equals getdate(schedule\_date), no value).
  - Draw row from self.booked\_rows\_after\_gap, keep a combination only if (getdate(row.schedule\_date) equals getdate(schedule\_date)).
- If not booked\_row.
  - Return false.
- Evaluate self.booked\_rows\_after\_gap.remove(booked\_row).
- Evaluate self.append(“depreciation\_schedule”, booked\_row).
- Return true.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1358)

<a id="op-07ff3f23b82688"></a>
### Depreciation Schedule Controller.add remaining booked rows

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_deppreciation_schedule_controller_depreciationschedulecontroller_add_remaining_booked_rows`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.booked\_rows\_after\_gap.
  - Return no value.
- Set rows from (self.depreciation\_schedule + self.booked\_rows\_after\_gap).
- Set self.booked\_rows\_after\_gap from list().
- Set self.depreciation\_schedule from list().
- For each row in sorted(rows, key = deferred anonymous expression).
  - Evaluate self.append(“depreciation\_schedule”, row).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1359)

<a id="op-a93578b1550e64"></a>
### Depreciation Schedule Controller.initialize variables

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_initialize_variables`

**Inputs** self.

**Local steps**

- Set self.pending\_depreciation\_amount from self.fb\_row.value\_after\_depreciation.
- Set self.should\_get\_last\_day from is\_last\_day\_of\_the\_month(self.fb\_row.depreciation\_start\_date).
- Set self.skip\_row from false.
- Set self.depreciation\_amount from 0.
- Set self.prev\_per\_day\_depr from true.
- Set self.prev\_depreciation\_amount from 0.
- Set self.current\_fiscal\_year\_end\_date from no value.
- Set self.yearly\_opening\_wdv from self.pending\_depreciation\_amount.
- Evaluate self.get\_number\_of\_pending\_months().
- Evaluate self.get\_final\_number\_of\_depreciations().
- Evaluate self.is\_wdv\_or\_dd\_non\_yearly\_pro\_rata().
- Evaluate self.get\_total\_pending\_days\_or\_years().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get number of pending months](operations-011.md#op-25d9e510ca2157), [get final number of depreciations](operations-011.md#op-4d628ea3a255b3), [is wdv or dd non yearly pro rata](operations-011.md#op-2a66a5a8872ebc), [get total pending days or years](operations-012.md#op-1bf58c96fecefa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L6723) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L469)

<a id="op-4d628ea3a255b3"></a>
### Depreciation Schedule Controller.get final number of depreciations

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_final_number_of_depreciations`

**Inputs** self.

**Local steps**

- Set self.final\_number\_of\_depreciations from (cint(self.fb\_row.total\_number\_of\_depreciations) − cint(self.opening\_number\_of\_booked\_depreciations)).
- Evaluate self.\_check\_is\_pro\_rata().
- If self.has\_pro\_rata.
  - Update self.final\_number\_of\_depreciations using + 1.
- Evaluate self.set\_final\_number\_of\_depreciations\_considering\_increase\_in\_asset\_life().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check is pro rata](operations-011.md#op-d257882530080f), [set final number of depreciations considering increase in asset life](operations-011.md#op-7045bda495fe55).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0322.json#L7003) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1575) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L455)

<a id="op-7045bda495fe55"></a>
### Depreciation Schedule Controller.set final number of depreciations considering increase in asset life

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_set_final_number_of_depreciations_considering_increase_in_asset_life`

**Inputs** self.

**Local steps**

- Set self.final\_schedule\_date from add\_months(self.asset\_doc.available\_for\_use\_date, ((self.fb\_row.total\_number\_of\_depreciations × cint(self.fb\_row.frequency\_of\_depreciation)) + cint(self.fb\_row.increase\_in\_asset\_life))).
- Set number\_of\_pending\_depreciations from (cint(self.fb\_row.total\_number\_of\_depreciations) − cint(self.asset\_doc.opening\_number\_of\_booked\_depreciations)).
- Set schedule\_date from add\_months(self.fb\_row.depreciation\_start\_date, (number\_of\_pending\_depreciations × cint(self.fb\_row.frequency\_of\_depreciation))).
- If self.final\_schedule\_date &gt; getdate(schedule\_date).
  - Set months from month\_diff(self.final\_schedule\_date, schedule\_date).
  - Update self.final\_number\_of\_depreciations using + ((months floor divide cint(self.fb\_row.frequency\_of\_depreciation)) + 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L475)

<a id="op-2a66a5a8872ebc"></a>
### Depreciation Schedule Controller.is wdv or dd non yearly pro rata

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_is_written_down_value_or_two_digit_day_non_yearly_pro_rata`

**Inputs** self.

**Local steps**

- If (self.fb\_row.depreciation\_method belongs to tuple(“Written Down Value”, “Double Declining Balance”) and cint(self.fb\_row.frequency\_of\_depreciation) differs from 12).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.fb\_row.depreciation\_method belongs to tuple(“Written Down Value”, “Double Declining Balance”) → cint(self.fb\_row.frequency\_of\_depreciation) differs from 12.
  - Evaluate self.\_check\_is\_pro\_rata().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check is pro rata](operations-011.md#op-d257882530080f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L405) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L470)

<a id="op-d257882530080f"></a>
### Depreciation Schedule Controller.check is pro rata

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_check_is_pro_rata`

**Inputs** self.

**Explicit failure paths** validation helper — translated multiline text in the contract.format(self.asset\_doc.opening\_number\_of\_booked\_depreciations, self.asset\_doc.opening\_number\_of\_booked\_depreciations).

**Local steps**

- Set self.has\_pro\_rata from false.
- If self.fb\_row.depreciation\_method belongs to tuple(“Straight Line”, “Manual”).
  - Set prev\_depreciation\_start\_date from get\_last\_day(add\_months(self.fb\_row.depreciation\_start\_date, ((self.fb\_row.frequency\_of\_depreciation × negative 1) × self.asset\_doc.opening\_number\_of\_booked\_depreciations))).
  - Set from\_date from self.asset\_doc.available\_for\_use\_date.
  - Set days from (date\_diff(prev\_depreciation\_start\_date, from\_date) + 1).
  - Set total\_days from self.get\_total\_days(prev\_depreciation\_start\_date).
- Otherwise.
  - Set from\_date from self.\_get\_modified\_available\_for\_use\_date\_for\_existing\_assets().
  - Set days from (date\_diff(self.fb\_row.depreciation\_start\_date, from\_date) + 1).
  - Set total\_days from self.get\_total\_days(self.fb\_row.depreciation\_start\_date).
- <a id="op-d257882530080f-guard-23"></a>If days ≤ 0.
  - Call the validation error handler Platform.throw(translated multiline text in the contract.format(self.asset\_doc.opening\_number\_of\_booked\_depreciations, self.asset\_doc.opening\_number\_of\_booked\_depreciations)).
- If days &lt; total\_days.
  - Set self.has\_pro\_rata from true.
  - Set self.has\_wdv\_or\_dd\_non\_yearly\_pro\_rata from true.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison days ≤ 0, days = 0 selects the branch that calls the validation-error handler with translated multiline text in the contract.format(self.asset\_doc.opening\_number\_of\_booked\_depreciations, self.asset\_doc.opening\_number …. With days = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-d257882530080f-guard-23)

**Methods declared on this owner** [get total days](operations-011.md#op-bb7d68a268c97b), [get modified available for use date for existing assets](operations-011.md#op-751e815a455a79).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1569) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L449)

<a id="op-751e815a455a79"></a>
### Depreciation Schedule Controller.get modified available for use date for existing assets

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_modified_available_for_use_date_for_existing_assets`

**Inputs** self.

**Explicit results** from\_date · self.asset\_doc.available\_for\_use\_date.

**Local steps**

- If self.asset\_doc.opening\_number\_of\_booked\_depreciations &gt; 0.
  - Set from\_date from add\_days(add\_months(self.fb\_row.depreciation\_start\_date, (self.fb\_row.frequency\_of\_depreciation × negative 1)), 1).
  - Return from\_date.
- Otherwise.
  - Return self.asset\_doc.available\_for\_use\_date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L1071) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1578) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L458)

<a id="op-bb7d68a268c97b"></a>
### Depreciation Schedule Controller.get total days

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_total_days`

**Inputs** self, date.

**Explicit results** date\_diff(date, period\_start\_date).

**Local steps**

- Set period\_start\_date from add\_months(date, (cint(self.fb\_row.frequency\_of\_depreciation) × negative 1)).
- If is\_last\_day\_of\_the\_month(date).
  - Set period\_start\_date from get\_last\_day(period\_start\_date).
- Return date\_diff(date, period\_start\_date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L1232) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1583) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L463)

<a id="op-d2727f2af6768a"></a>
### Depreciation Schedule Controller.get pro rata amt

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_pro_rata_amount`

**Inputs** self, from\_date, to\_date, original\_schedule\_date = no value.

**Explicit results** tuple(((self.depreciation\_amount × flt(days)) ÷ flt(total\_days)), days, months).

**Local steps**

- Set days from (date\_diff(to\_date, from\_date) + 1).
- Set months from month\_diff(to\_date, from\_date).
- Set total\_days from self.get\_total\_days((original\_schedule\_date or to\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in original\_schedule\_date → to\_date.
- Return tuple(((self.depreciation\_amount × flt(days)) ÷ flt(total\_days)), days, months).

**Methods declared on this owner** [get total days](operations-011.md#op-bb7d68a268c97b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L1411) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1582) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L462)

<a id="op-25d9e510ca2157"></a>
### Depreciation Schedule Controller.get number of pending months

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_number_of_pending_months`

**Inputs** self.

**Local steps**

- Set total\_months from ((cint(self.fb\_row.total\_number\_of\_depreciations) × cint(self.fb\_row.frequency\_of\_depreciation)) + cint(self.fb\_row.increase\_in\_asset\_life)).
- Set last\_depr\_date from self.get\_last\_booked\_depreciation\_date().
- Set depr\_booked\_for\_months from (self.get\_booked\_depr\_for\_months\_count(last\_depr\_date) + self.get\_months\_booked\_after\_gap()).
- Set self.pending\_months from (total\_months − depr\_booked\_for\_months).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get last booked depreciation date](operations-011.md#op-27f3ed242dd680), [get booked depr for months count](operations-012.md#op-21bb0685c6349e), [get months booked after gap](operations-011.md#op-8b27745d08d900).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1580) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L460)

<a id="op-8b27745d08d900"></a>
### Depreciation Schedule Controller.get months booked after gap

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_deppreciation_schedule_controller_depreciationschedulecontroller_get_months_booked_after_gap`

**Inputs** self.

**Declared result** float.

**Explicit results** 0 · sum(generator of self.get\_months\_covered(rows at (idx − 1).schedule\_date, rows at idx.schedule\_date) for idx drawn from range((self.first\_non\_depreciated\_row\_idx + 1), len(rows)) where rows at idx.journal\_entry).

**Local steps**

- If not self.booked\_rows\_after\_gap.
  - Return 0.
- Set rows from self.schedules\_before\_clearing.
- Return sum(generator of self.get\_months\_covered(rows at (idx − 1).schedule\_date, rows at idx.schedule\_date) for idx drawn from range((self.first\_non\_depreciated\_row\_idx + 1), len(rows)) where rows at idx.journal\_entry).
  - Draw idx from range((self.first\_non\_depreciated\_row\_idx + 1), len(rows)), keep a combination only if (rows at idx.journal\_entry).

**Methods declared on this owner** [get months covered](operations-011.md#op-ee742fc6f1c521).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1360)

<a id="op-ee742fc6f1c521"></a>
### Depreciation Schedule Controller.get months covered

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_deppreciation_schedule_controller_depreciationschedulecontroller_get_months_covered`

**Inputs** self, previous\_date, schedule\_date.

**Declared result** float.

**Explicit results** frequency · get\_elapsed\_months(add\_days(previous\_date, 1), schedule\_date, frequency).

**Local steps**

- Set frequency from cint(self.fb\_row.frequency\_of\_depreciation).
- If self.is\_full\_period(previous\_date, schedule\_date).
  - Return frequency.
- Return get\_elapsed\_months(add\_days(previous\_date, 1), schedule\_date, frequency).

**Methods declared on this owner** [is full period](operations-011.md#op-b3751f322d24db).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1361)

<a id="op-b3751f322d24db"></a>
### Depreciation Schedule Controller.is full period

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_deppreciation_schedule_controller_depreciationschedulecontroller_is_full_period`

**Inputs** self, previous\_date, schedule\_date.

**Declared result** bool.

**Explicit results** false · (getdate(self.get\_next\_schedule\_date(row\_idx)) equals schedule\_date and getdate(self.get\_next\_schedule\_date((row\_idx − 1))) equals getdate(previous\_date)).

**Local steps**

- Set tuple(start\_date, schedule\_date) from tuple(getdate(self.fb\_row.depreciation\_start\_date), getdate(schedule\_date)).
- Set frequency from cint(self.fb\_row.frequency\_of\_depreciation).
- Set months from ((((schedule\_date.year − start\_date.year) × 12) + schedule\_date.month) − start\_date.month).
- If (months modulo or format frequency).
  - Return false.
- Set row\_idx from (months floor divide frequency).
- Return (getdate(self.get\_next\_schedule\_date(row\_idx)) equals schedule\_date and getdate(self.get\_next\_schedule\_date((row\_idx − 1))) equals getdate(previous\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(self.get\_next\_schedule\_date(row\_idx)) equals schedule\_date → getdate(self.get\_next\_schedule\_date((row\_idx − 1))) equals getdate(previous\_date).

**Methods declared on this owner** [get next schedule date](operations-012.md#op-5ae60102d954bd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1363)

<a id="op-27f3ed242dd680"></a>
### Depreciation Schedule Controller.get last booked depreciation date

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_last_booked_depreciation_date`

**Inputs** self.

**Explicit results** last\_depr\_date.

**Local steps**

- Set last\_depr\_date from no value.
- If self.first\_non\_depreciated\_row\_idx &gt; 0.
  - Set last\_depr\_date from self.depreciation\_schedule at (self.first\_non\_depreciated\_row\_idx − 1).schedule\_date.
- Otherwise.
  - If self.asset\_doc.opening\_number\_of\_booked\_depreciations &gt; 0.
    - Set last\_depr\_date from add\_months(self.fb\_row.depreciation\_start\_date, (negative 1 × self.fb\_row.frequency\_of\_depreciation)).
    - If (self.has\_complete\_opening\_periods() and self.should\_get\_last\_day).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_complete\_opening\_periods() → self.should\_get\_last\_day.
      - Set last\_depr\_date from get\_last\_day(last\_depr\_date).
- Return last\_depr\_date.

**Methods declared on this owner** [has complete opening periods](operations-012.md#op-d134803a013955).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1577) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L457)
