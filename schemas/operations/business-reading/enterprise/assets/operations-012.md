# Asset management · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset depreciation schedule

[Record definition](../../../../data/record-types/asset_depreciation_schedule.json)

<a id="op-21bb0685c6349e"></a>
### Depreciation Schedule Controller.get booked depr for months count

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_booked_depr_for_months_count`

**Inputs** self, last\_depr\_date.

**Explicit results** ((month\_diff(last\_depr\_date, first\_period\_end) − 1) + self.fb\_row.frequency\_of\_depreciation) · depr\_booked\_for\_months.

**Local steps**

- If (last\_depr\_date and self.has\_complete\_opening\_periods()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_depr\_date → self.has\_complete\_opening\_periods().
  - Set first\_period\_end from self.get\_next\_schedule\_date(negative cint(self.asset\_doc.opening\_number\_of\_booked\_depreciations)).
  - Return ((month\_diff(last\_depr\_date, first\_period\_end) − 1) + self.fb\_row.frequency\_of\_depreciation).
- Set depr\_booked\_for\_months from 0.
- If last\_depr\_date.
  - Set asset\_used\_for\_months from (self.fb\_row.frequency\_of\_depreciation × (1 + self.asset\_doc.opening\_number\_of\_booked\_depreciations)).
  - Set computed\_available\_for\_use\_date from add\_days(add\_months(self.fb\_row.depreciation\_start\_date, (negative 1 × asset\_used\_for\_months)), 1).
  - If getdate(computed\_available\_for\_use\_date) &lt; getdate(self.asset\_doc.available\_for\_use\_date).
    - Set computed\_available\_for\_use\_date from self.asset\_doc.available\_for\_use\_date.
  - Set depr\_booked\_for\_months from get\_elapsed\_months(computed\_available\_for\_use\_date, last\_depr\_date, cint(self.fb\_row.frequency\_of\_depreciation)).
- Return depr\_booked\_for\_months.

**Methods declared on this owner** [has complete opening periods](operations-012.md#op-d134803a013955), [get next schedule date](operations-012.md#op-5ae60102d954bd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1573) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L453)

<a id="op-d134803a013955"></a>
### Depreciation Schedule Controller.has complete opening periods

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_deppreciation_schedule_controller_depreciationschedulecontroller_has_complete_opening_periods`

**Inputs** self.

**Explicit results** false · first\_period\_start equals getdate(self.asset\_doc.available\_for\_use\_date).

**Local steps**

- If (self.fb\_row.depreciation\_method does not belong to tuple(“Straight Line”, “Manual”) or self.fb\_row.daily\_prorata\_based or self.fb\_row.shift\_based or not self.asset\_doc.opening\_number\_of\_booked\_depreciations).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.fb\_row.depreciation\_method does not belong to tuple(“Straight Line”, “Manual”) → self.fb\_row.daily\_prorata\_based → self.fb\_row.shift\_based → not self.asset\_doc.opening\_number\_of\_booked\_depreciations.
  - Return false.
- Set first\_period\_start from add\_days(self.get\_next\_schedule\_date((negative cint(nested operand in the contract.asset\_doc.opening\_number\_of\_booked\_depreciations) − 1)), 1).
- Return first\_period\_start equals getdate(self.asset\_doc.available\_for\_use\_date).

**Methods declared on this owner** [get next schedule date](operations-012.md#op-5ae60102d954bd).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1362)

<a id="op-1bf58c96fecefa"></a>
### Depreciation Schedule Controller.get total pending days or years

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_total_pending_days_or_years`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Local steps**

- If cint(Platform.get\_single\_value(“Accounts Settings”, “calculate\_depr\_using\_total\_days”)).
  - Set last\_depr\_date from self.get\_last\_booked\_depreciation\_date().
  - If last\_depr\_date.
    - Set self.total\_pending\_days from (date\_diff(self.final\_schedule\_date, last\_depr\_date) − 1).
  - Otherwise.
    - Set self.total\_pending\_days from date\_diff(self.final\_schedule\_date, self.asset\_doc.available\_for\_use\_date).
- Otherwise.
  - Set self.total\_pending\_years from (self.pending\_months ÷ 12).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get last booked depreciation date](operations-011.md#op-27f3ed242dd680).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “calculate\_depr\_using\_total\_days”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L2368) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1586) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L466)

<a id="op-b97bd347dbe099"></a>
### Depreciation Schedule Controller.has fiscal year changed

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_has_fiscal_year_changed`

**Inputs** self, row\_idx.

**Local steps**

- Set self.fiscal\_year\_changed from false.
- Set schedule\_date from get\_last\_day(add\_months(self.fb\_row.depreciation\_start\_date, (row\_idx × cint(self.fb\_row.frequency\_of\_depreciation)))).
- If not self.current\_fiscal\_year\_end\_date.
  - Set self.current\_fiscal\_year\_end\_date from self.get\_fiscal\_year(self.fb\_row.depreciation\_start\_date) at 1.
  - Set self.fiscal\_year\_changed from true.
- Otherwise.
  - If getdate(schedule\_date) &gt; getdate(self.current\_fiscal\_year\_end\_date).
    - Set self.current\_fiscal\_year\_end\_date from add\_years(self.current\_fiscal\_year\_end\_date, 1).
    - Set self.fiscal\_year\_changed from true.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get fiscal year](operations-012.md#op-cb8ae1b3e1fd2b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1587) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L467)

<a id="op-affe93fe00aa3d"></a>
### Depreciation Schedule Controller.get prev depreciation amount

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_previous_depreciation_amount`

**Inputs** self, row\_idx.

**Local steps**

- If row\_idx &gt; 1.
  - Set self.prev\_depreciation\_amount from 0.
  - If len(self.get(“depreciation\_schedule”)) &gt; (row\_idx − 1).
    - Set self.prev\_depreciation\_amount from self.get(“depreciation\_schedule”) at (row\_idx − 1).depreciation\_amount.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L2943) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L461)

<a id="op-5ae60102d954bd"></a>
### Depreciation Schedule Controller.get next schedule date

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_next_schedule_date`

**Inputs** self, row\_idx.

**Explicit results** schedule\_date.

**Local steps**

- Set schedule\_date from add\_months(self.fb\_row.depreciation\_start\_date, (row\_idx × cint(self.fb\_row.frequency\_of\_depreciation))).
- If self.should\_get\_last\_day.
  - Set schedule\_date from get\_last\_day(schedule\_date).
- Return schedule\_date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L3139) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1579) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L459)

<a id="op-4348be19ef7be9"></a>
### Depreciation Schedule Controller.set depreciation amount for disposal

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_set_depreciation_amount_for_disposal`

**Inputs** self, row\_idx.

**Local steps**

- If self.depreciation\_schedule.
  - Set from\_date from add\_days(self.depreciation\_schedule at negative 1.schedule\_date, 1).
- Otherwise.
  - Set from\_date from self.\_get\_modified\_available\_for\_use\_date\_for\_existing\_assets().
  - If is\_last\_day\_of\_the\_month(getdate(self.asset\_doc.available\_for\_use\_date)).
    - Set from\_date from get\_last\_day(from\_date).
- Set tuple(self.depreciation\_amount, days, months) from self.\_get\_pro\_rata\_amt(from\_date, self.disposal\_date, original\_schedule\_date = self.schedule\_date).
- Set self.depreciation\_amount from flt(self.depreciation\_amount, self.asset\_doc.precision(“net\_purchase\_amount”)).
- If self.depreciation\_amount &gt; 0.
  - Set self.schedule\_date from self.disposal\_date.
  - Evaluate self.add\_depr\_schedule\_row(row\_idx).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get modified available for use date for existing assets](operations-011.md#op-751e815a455a79), [get pro rata amt](operations-011.md#op-d2727f2af6768a), [add depr schedule row](operations-012.md#op-bf3ba36ececf47).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L3294) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L472)

<a id="op-9c4151dbe7380c"></a>
### Depreciation Schedule Controller.set depreciation amount for first row

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_set_depreciation_amount_for_first_row`

**Inputs** self, row\_idx.

**Local steps**

- Set pro\_rata\_amount\_applicable from false.
- If (self.has\_pro\_rata and not self.opening\_accumulated\_depreciation and not self.flags.wdv\_it\_act\_applied).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_pro\_rata → not self.opening\_accumulated\_depreciation → not self.flags.wdv\_it\_act\_applied.
  - Set from\_date from self.asset\_doc.available\_for\_use\_date.
  - Set pro\_rata\_amount\_applicable from true.
- Otherwise.
  - If (self.has\_pro\_rata and self.opening\_accumulated\_depreciation).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_pro\_rata → self.opening\_accumulated\_depreciation.
    - Set from\_date from self.\_get\_modified\_available\_for\_use\_date\_for\_existing\_assets().
    - Set pro\_rata\_amount\_applicable from true.
- If pro\_rata\_amount\_applicable.
  - Set tuple(self.depreciation\_amount, days, months) from self.\_get\_pro\_rata\_amt(from\_date, self.fb\_row.depreciation\_start\_date).
  - Evaluate self.validate\_depreciation\_amount\_for\_low\_value\_assets().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get modified available for use date for existing assets](operations-011.md#op-751e815a455a79), [get pro rata amt](operations-011.md#op-d2727f2af6768a), [validate depreciation amount for low value assets](operations-012.md#op-b51a109148aa16).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L3702) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L473)

<a id="op-8bb0db2dddf9ab"></a>
### Depreciation Schedule Controller.set depreciation amount for last row

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_set_depreciation_amount_for_last_row`

**Inputs** self, row\_idx.

**Local steps**

- If not self.fb\_row.increase\_in\_asset\_life.
  - Set self.final\_schedule\_date from add\_months(self.asset\_doc.available\_for\_use\_date, ((row\_idx + self.opening\_number\_of\_booked\_depreciations) × cint(self.fb\_row.frequency\_of\_depreciation))).
  - If is\_last\_day\_of\_the\_month(getdate(self.asset\_doc.available\_for\_use\_date)).
    - Set self.final\_schedule\_date from get\_last\_day(self.final\_schedule\_date).
- If self.opening\_accumulated\_depreciation.
  - Set tuple(self.depreciation\_amount, days, months) from self.\_get\_pro\_rata\_amt(self.schedule\_date, self.final\_schedule\_date).
- Otherwise.
  - If not self.fb\_row.increase\_in\_asset\_life.
    - Update self.depreciation\_amount using − self.get(“depreciation\_schedule”) at 0.depreciation\_amount.
  - Set days from (date\_diff(self.final\_schedule\_date, self.schedule\_date) + 1).
- Set self.schedule\_date from add\_days(self.schedule\_date, (days − 1)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get pro rata amt](operations-011.md#op-d2727f2af6768a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L3993) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1594) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L474)

<a id="op-48a61b0389d95d"></a>
### Depreciation Schedule Controller.adjust depr amount for salvage value

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_adjust_depr_amount_for_salvage_value`

**Inputs** self, row\_idx.

**Local steps**

- If ((row\_idx equals (cint(self.final\_number\_of\_depreciations) − 1) and flt(self.pending\_depreciation\_amount) differs from flt(self.fb\_row.expected\_value\_after\_useful\_life)) or flt(self.pending\_depreciation\_am ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (row\_idx equals (cint(self.final\_number\_of\_depreciations) − 1) and flt(self.pending\_depreciation\_amount) differs from flt(self.fb\_row.expected\_value\_after\_useful\_life)) → flt(self.pending\_depreciation\_amount) &lt; flt(self.fb\_row.expected\_value\_after\_useful\_life).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row\_idx equals (cint(self.final\_number\_of\_depreciations) − 1) → flt(self.pending\_depreciation\_amount) differs from flt(self.fb\_row.expected\_value\_after\_useful\_life).
  - Update self.depreciation\_amount using + (flt(self.pending\_depreciation\_amount) − flt(self.fb\_row.expected\_value\_after\_useful\_life)).
  - Set self.depreciation\_amount from flt(self.depreciation\_amount, self.precision(“value\_after\_depreciation”)).
  - Set self.skip\_row from true.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L4459) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1568) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L448)

<a id="op-b51a109148aa16"></a>
### Depreciation Schedule Controller.validate depreciation amount for low value assets

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_validate_depreciation_amount_for_low_value_assets`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Net Purchase Amount {0} cannot be depreciated over {1} cycles.”.format(Platform.bold(self.asset\_doc.net\_purchase\_amount), Platform.bold(self.fb\_row.total\_number\_of\_depreciations)).

**Local steps**

- If flt(self.depreciation\_amount, self.asset\_doc.precision(“net\_purchase\_amount”)) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Net Purchase Amount {0} cannot be depreciated over {1} cycles.”.format(Platform.bold(self.asset\_doc.net\_purchase\_amount), Platform.bold(self.fb\_row.total\_number\_of\_depreciations))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L4791) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L476)

<a id="op-bf3ba36ececf47"></a>
### Depreciation Schedule Controller.add depr schedule row

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_add_depr_schedule_row`

**Inputs** self, row\_idx.

**Local steps**

- Set shift from no value.
- If self.shift\_based.
  - Set shift from self.schedules\_before\_clearing at row\_idx.shift when (self.schedules\_before\_clearing and len(self.schedules\_before\_clearing) &gt; row\_idx), otherwise get\_default\_shift\_name().
    - Value choice on (self.schedules\_before\_clearing and len(self.schedules\_before\_clearing) &gt; row\_idx) — true gives self.schedules\_before\_clearing at row\_idx.shift, false gives get\_default\_shift\_name().
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.schedules\_before\_clearing → len(self.schedules\_before\_clearing) &gt; row\_idx.
- Evaluate self.append(“depreciation\_schedule”, mapping(“schedule\_date” → self.schedule\_date, “depreciation\_amount” → self.depreciation\_amount, “shift” → shift)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1567) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L447)

<a id="op-01e243101ddff5"></a>
### Depreciation Schedule Controller.set accumulated depreciation

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_set_accumulated_depreciation`

**Inputs** self.

**Local steps**

- Set accumulated\_depreciation from flt(self.opening\_accumulated\_depreciation).
- For each d in self.get(“depreciation\_schedule”).
  - Update accumulated\_depreciation using + d.depreciation\_amount.
  - Set d.accumulated\_depreciation\_amount from flt(accumulated\_depreciation, d.precision(“accumulated\_depreciation\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L471)

<a id="op-0d1d503c1d6ba3"></a>
### Depreciation Schedule Controller.get depreciation amount

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_depreciation_amount`

**Inputs** self, row\_idx.

**Explicit results** self.get\_straight\_line\_depr\_amount(row\_idx) · self.get\_wdv\_or\_dd\_depr\_amount(row\_idx).

**Local steps**

- If self.fb\_row.depreciation\_method belongs to tuple(“Straight Line”, “Manual”).
  - Return self.get\_straight\_line\_depr\_amount(row\_idx).
- Otherwise.
  - Return self.get\_wdv\_or\_dd\_depr\_amount(row\_idx).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L5484) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1574) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L454)

<a id="op-51d2400dec3fac"></a>
### Depreciation Schedule Controller.get total days

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_total_days_2`

**Inputs** self, depreciation\_start\_date, row\_idx.

**Explicit results** tuple(from\_date, (date\_diff(to\_date, from\_date) + 1)).

**Local steps**

- Set from\_date from add\_months(depreciation\_start\_date, ((row\_idx − 1) × self.frequency\_of\_depreciation)).
- Set to\_date from add\_months(from\_date, self.frequency\_of\_depreciation).
- If is\_last\_day\_of\_the\_month(depreciation\_start\_date).
  - Set to\_date from get\_last\_day(to\_date).
  - Set from\_date from add\_days(get\_last\_day(from\_date), 1).
- Return tuple(from\_date, (date\_diff(to\_date, from\_date) + 1)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L5608) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1584) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L464)

<a id="op-9ee67e007e70fc"></a>
### Depreciation Schedule Controller.get total days in current depr year

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_total_days_in_current_depr_year`

**Inputs** self.

**Explicit results** (date\_diff(fy\_end\_date, fy\_start\_date) + 1).

**Local steps**

- Set tuple(fy\_start\_date, fy\_end\_date) from self.get\_fiscal\_year(self.schedule\_date).
- Return (date\_diff(fy\_end\_date, fy\_start\_date) + 1).

**Methods declared on this owner** [get fiscal year](operations-012.md#op-cb8ae1b3e1fd2b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L5875) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1585) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L465)

<a id="op-cb8ae1b3e1fd2b"></a>
### Depreciation Schedule Controller.get fiscal year

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_deppreciation_schedule_controller_business_behavior_depreciation_schedule_controller_get_fiscal_year`

**Inputs** self, date.

**Explicit results** tuple(fy\_start\_date, fy\_end\_date).

**Local steps**

- Set fy from get\_fiscal\_year(date, company = self.asset\_doc.company, as\_dict = true, raise\_on\_missing = false).
- If fy.
  - Set fy\_start\_date from fy.year\_start\_date.
  - Set fy\_end\_date from fy.year\_end\_date.
- Otherwise.
  - Set current\_fy from get\_fiscal\_year(nowdate(), company = self.asset\_doc.company, as\_dict = true).
  - Set months from month\_diff(date, current\_fy.year\_start\_date).
  - If (months modulo or format 12).
    - Set years from (months floor divide 12).
  - Otherwise.
    - Set years from ((months floor divide 12) − 1).
  - Set fy\_start\_date from add\_years(current\_fy.year\_start\_date, years).
  - Set fy\_end\_date from add\_days(add\_years(fy\_start\_date, 1), negative 1).
- Return tuple(fy\_start\_date, fy\_end\_date).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1576) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L456)

<a id="op-002be52568e0ba"></a>
### Get elapsed months

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_deppreciation_schedule_controller_get_elapsed_months`

**Inputs** from\_date, to\_date, frequency.

**Declared result** float.

**Explicit results** ((periods + (date\_diff(partial\_period\_end, from\_date) ÷ partial\_period\_days)) × frequency).

**Local steps**

- Set tuple(from\_date, period\_end) from tuple(getdate(from\_date), getdate(add\_days(to\_date, 1))).
- Set periods from 0.
- While getdate(add\_months(period\_end, (negative frequency × (periods + 1)))) ≥ from\_date.
  - Update periods using + 1.
- Set partial\_period\_end from add\_months(period\_end, (negative frequency × periods)).
- Set partial\_period\_days from date\_diff(partial\_period\_end, add\_months(partial\_period\_end, negative frequency)).
- Return ((periods + (date\_diff(partial\_period\_end, from\_date) ÷ partial\_period\_days)) × frequency).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1365)

<a id="op-cacd8097f12343"></a>
### Get default shift name

`operation_enterprise_binding_enterprise_assets_doctype_asset_depreciation_schedule_deppreciation_schedule_controller_get_default_shift_name`

**Inputs** no declared parameters.

**Declared result** str.

**Record and data access** read “Asset Shift Factor” via get\_cached\_value.

**Explicit results** shift\_name.

**Explicit failure paths** validation helper — translated “Please set a default Asset Shift Factor to use shift based depreciation.”.

**Local steps**

- Set shift\_name from Platform.get\_cached\_value(“Asset Shift Factor”, mapping(“default” → 1), “shift\_name”).
- If not shift\_name.
  - Call the validation error handler Platform.throw(translated “Please set a default Asset Shift Factor to use shift based depreciation.”).
- Return shift\_name.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Asset Shift Factor”, mapping(“default” → 1), “shift\_name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1364)

<a id="op-e7098f8be2741f"></a>
### Straight Line Method.get straight line depr amount

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_depreciation_methods_business_behavior_straight_line_method_get_straight_line_depr_amount`

**Inputs** self, row\_idx.

**Explicit results** self.get\_shift\_depr\_amount(row\_idx) · self.get\_daily\_prorata\_based\_depr\_amount(row\_idx) · self.get\_fixed\_depr\_amount().

**Local steps**

- Set self.depreciable\_value from (flt(self.fb\_row.value\_after\_depreciation) − flt(self.fb\_row.expected\_value\_after\_useful\_life)).
- If self.fb\_row.shift\_based.
  - Return self.get\_shift\_depr\_amount(row\_idx).
- If self.fb\_row.daily\_prorata\_based.
  - Return self.get\_daily\_prorata\_based\_depr\_amount(row\_idx).
- Otherwise.
  - Return self.get\_fixed\_depr\_amount().

**Methods declared on this owner** [get shift depr amount](operations-012.md#op-5bfa9caaff46d1), [get daily prorata based depr amount](operations-012.md#op-998578bc126500), [get fixed depr amount](operations-012.md#op-eac43fa15188a2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L6367) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L482)

<a id="op-eac43fa15188a2"></a>
### Straight Line Method.get fixed depr amount

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_depreciation_methods_business_behavior_straight_line_method_get_fixed_depr_amount`

**Inputs** self.

**Explicit results** (self.depreciable\_value ÷ pending\_periods).

**Local steps**

- Set pending\_periods from (flt(self.pending\_months) ÷ flt(self.fb\_row.frequency\_of\_depreciation)).
- Return (self.depreciable\_value ÷ pending\_periods).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L6577) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L480)

<a id="op-998578bc126500"></a>
### Straight Line Method.get daily prorata based depr amount

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_depreciation_methods_business_behavior_straight_line_method_get_daily_prorata_based_depr_amount`

**Inputs** self, row\_idx.

**Explicit results** (daily\_depr\_amount × total\_depreciable\_days).

**Local steps**

- Set daily\_depr\_amount from self.get\_daily\_depr\_amount().
- Set tuple(from\_date, total\_depreciable\_days) from self.\_get\_total\_days(self.fb\_row.depreciation\_start\_date, row\_idx).
- Return (daily\_depr\_amount × total\_depreciable\_days).

**Methods declared on this owner** [get daily depr amount](operations-012.md#op-fad08f3ae00f89).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L6683) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1599) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L479)

<a id="op-fad08f3ae00f89"></a>
### Straight Line Method.get daily depr amount

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_depreciation_methods_business_behavior_straight_line_method_get_daily_depr_amount`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** (self.depreciable\_value ÷ self.total\_pending\_days) · (yearly\_depr\_amount ÷ total\_days\_in\_current\_depr\_year).

**Local steps**

- If cint(Platform.get\_single\_value(“Accounts Settings”, “calculate\_depr\_using\_total\_days”)).
  - Return (self.depreciable\_value ÷ self.total\_pending\_days).
- Otherwise.
  - Set yearly\_depr\_amount from (self.depreciable\_value ÷ self.total\_pending\_years).
  - Set total\_days\_in\_current\_depr\_year from self.get\_total\_days\_in\_current\_depr\_year().
  - Return (yearly\_depr\_amount ÷ total\_days\_in\_current\_depr\_year).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “calculate\_depr\_using\_total\_days”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0323.json#L6813) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1598) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L478)

<a id="op-5bfa9caaff46d1"></a>
### Straight Line Method.get shift depr amount

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_depreciation_methods_business_behavior_straight_line_method_get_shift_depr_amount`

**Inputs** self, row\_idx.

**Explicit results** (self.depreciable\_value ÷ pending\_periods) · ((self.depreciable\_value ÷ shift\_factors\_sum) × shift\_factor).

**Local steps**

- If not self.schedules\_before\_clearing.
  - Set pending\_periods from (flt(self.pending\_months) ÷ flt(self.fb\_row.frequency\_of\_depreciation)).
  - Return (self.depreciable\_value ÷ pending\_periods).
- Set asset\_shift\_factors\_map from self.get\_asset\_shift\_factors\_map().
- If self.schedules\_before\_clearing.
  - Set shift from self.schedules\_before\_clearing at row\_idx.shift when len(self.schedules\_before\_clearing) &gt; row\_idx, otherwise no value.
    - Value choice on len(self.schedules\_before\_clearing) &gt; row\_idx — true gives self.schedules\_before\_clearing at row\_idx.shift, false gives no value.
- Set shift\_factor from asset\_shift\_factors\_map.get(shift, 0).
- Set shift\_factors\_sum from sum(list of flt(asset\_shift\_factors\_map.get(d.shift)) for d drawn from self.schedules\_before\_clearing where not d.journal\_entry).
  - Draw d from self.schedules\_before\_clearing, keep a combination only if (not d.journal\_entry).
- Return ((self.depreciable\_value ÷ shift\_factors\_sum) × shift\_factor).

**Methods declared on this owner** [get asset shift factors map](operations-013.md#op-1bb1070eed5a83).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0324.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L481)
