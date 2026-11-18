# Asset management · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset depreciation schedule

[Record definition](../../../../data/record-types/asset_depreciation_schedule.json)

<a id="op-1bb1070eed5a83"></a>
### Straight Line Method.get asset shift factors map

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_depreciation_methods_business_behavior_straight_line_method_get_asset_shift_factors_map`

**Inputs** self.

**Record and data access** read “Asset Shift Factor” via get\_all.

**Explicit results** dict(Platform.db.get\_all(“Asset Shift Factor”, list(“shift\_name”, “shift\_factor”), as\_list = true)).

**Local steps**

- Return dict(Platform.db.get\_all(“Asset Shift Factor”, list(“shift\_name”, “shift\_factor”), as\_list = true)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0324.json#L394) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1597) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L477)

<a id="op-bbdf5f530bb29b"></a>
### WDVMethod.get wdv or dd depr amount

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_depreciation_methods_business_behavior_written_down_value_method_get_written_down_value_or_two_digit_day_depr_amount`

**Inputs** self, row\_idx.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Explicit results** WDVMethod.calculate\_wdv\_or\_dd\_based\_depreciation\_amount(self, row\_idx).

**Local steps**

- Return WDVMethod.calculate\_wdv\_or\_dd\_based\_depreciation\_amount(self, row\_idx).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0324.json#L502) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L487)

<a id="op-b0512105833969"></a>
### WDVMethod.calculate wdv or dd based depreciation amount

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_depreciation_methods_business_behavior_written_down_value_method_calculate_written_down_value_or_two_digit_day_based_depreciation_amount`

**Inputs** self, row\_idx.

**Wrappers, in declaration order** staticmethod.

**Explicit results** self.get\_daily\_prorata\_based\_wdv\_depr\_amount(row\_idx) · self.get\_wdv\_depr\_amount().

**Local steps**

- If self.fb\_row.daily\_prorata\_based.
  - Return self.get\_daily\_prorata\_based\_wdv\_depr\_amount(row\_idx).
- Otherwise.
  - Return self.get\_wdv\_depr\_amount().

**Methods declared on this owner** [get daily prorata based wdv depr amount](operations-013.md#op-d4197690b62dc4), [get wdv depr amount](operations-013.md#op-f9ec54c8663082).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0324.json#L578) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L483)

<a id="op-f9ec54c8663082"></a>
### WDVMethod.get wdv depr amount

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_depreciation_methods_business_behavior_written_down_value_method_get_written_down_value_depr_amount`

**Inputs** self.

**Explicit results** depreciation\_amount · self.prev\_depreciation\_amount.

**Local steps**

- If self.is\_fiscal\_year\_changed().
  - Set yearly\_amount from ((flt(self.pending\_depreciation\_amount) × flt(self.fb\_row.rate\_of\_depreciation)) ÷ 100).
  - Set depreciation\_amount from ((yearly\_amount × self.fb\_row.frequency\_of\_depreciation) ÷ 12).
  - Set self.prev\_depreciation\_amount from depreciation\_amount.
  - Return depreciation\_amount.
- Otherwise.
  - Return self.prev\_depreciation\_amount.

**Methods declared on this owner** [is fiscal year changed](operations-013.md#op-a2882801aec7f2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0324.json#L685) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1606) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L486)

<a id="op-a2882801aec7f2"></a>
### WDVMethod.is fiscal year changed

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_depreciation_methods_business_behavior_written_down_value_method_is_fiscal_year_changed`

**Inputs** self.

**Explicit results** true.

**Local steps**

- Set tuple(fy\_start\_date, fy\_end\_date) from self.get\_fiscal\_year(self.schedule\_date).
- If fy\_start\_date differs from self.get(“prev\_fy\_start\_date”).
  - Set self.prev\_fy\_start\_date from fy\_start\_date.
  - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0324.json#L877) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L488)

<a id="op-d4197690b62dc4"></a>
### WDVMethod.get daily prorata based wdv depr amount

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_depreciation_methods_business_behavior_written_down_value_method_get_daily_prorata_based_written_down_value_depr_amount`

**Inputs** self, row\_idx.

**Explicit results** (daily\_depr\_amount × total\_depreciable\_days).

**Local steps**

- Set daily\_depr\_amount from self.get\_daily\_wdv\_depr\_amount().
- Set tuple(from\_date, total\_depreciable\_days) from self.\_get\_total\_days(self.fb\_row.depreciation\_start\_date, row\_idx).
- Return (daily\_depr\_amount × total\_depreciable\_days).

**Methods declared on this owner** [get daily wdv depr amount](operations-013.md#op-38fe268fa142d2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0324.json#L1012) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1604) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L484)

<a id="op-38fe268fa142d2"></a>
### WDVMethod.get daily wdv depr amount

`operation_enterprise_assets_record_definitions_asset_depreciation_schedule_depreciation_methods_business_behavior_written_down_value_method_get_daily_written_down_value_depr_amount`

**Inputs** self.

**Explicit results** (self.yearly\_wdv\_depr\_amount ÷ total\_days\_in\_current\_depr\_year).

**Local steps**

- If self.is\_fiscal\_year\_changed().
  - Set self.yearly\_wdv\_depr\_amount from ((self.pending\_depreciation\_amount × self.fb\_row.rate\_of\_depreciation) ÷ 100).
- Set total\_days\_in\_current\_depr\_year from self.get\_total\_days\_in\_current\_depr\_year().
- Return (self.yearly\_wdv\_depr\_amount ÷ total\_days\_in\_current\_depr\_year).

**Methods declared on this owner** [is fiscal year changed](operations-013.md#op-a2882801aec7f2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0324.json#L1142) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1605) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L485)

## Record · Asset maintenance

[Record definition](../../../../data/record-types/asset_maintenance.json)

<a id="op-84e00b7d6e5c51"></a>
### Asset Maintenance.validate

`operation_enterprise_assets_record_definitions_asset_maintenance_business_behavior_asset_maintenance_validate`

**Inputs** self.

**Record and data access** read “Maintenance Team Member” via get\_all.

**Local steps**

- Evaluate self.validate\_asset().
- Set team\_members from Platform.get\_all(“Maintenance Team Member”, filters = mapping(“parent” → self.maintenance\_team), pluck = “team\_member”).
- For each task in self.get(“asset\_maintenance\_tasks”).
  - If (task.end\_date and getdate(task.start\_date) ≥ getdate(task.end\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in task.end\_date → getdate(task.start\_date) ≥ getdate(task.end\_date).
    - Evaluate throw(translated “Start date should be less than end date for task {0}”.format(task.maintenance\_task)).
  - If (not task.next\_due\_date and task.periodicity).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not task.next\_due\_date → task.periodicity.
    - Set task.next\_due\_date from (calculate\_next\_due\_date(task.periodicity, task.start\_date, task.end\_date, task.last\_completion\_date) or no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in calculate\_next\_due\_date(task.periodicity, task.start\_date, task.end\_date, task.last\_completion\_date) → no value.
  - If (task.next\_due\_date and getdate(task.next\_due\_date) &lt; getdate(task.start\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in task.next\_due\_date → getdate(task.next\_due\_date) &lt; getdate(task.start\_date).
    - Evaluate throw(translated “Row #{0}: Next Due Date cannot be before the Start Date”.format(task.idx)).
  - Evaluate self.set\_task\_status(task).
  - Evaluate self.validate\_assignee(task, team\_members).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate asset](operations-013.md#op-7aa9c7157ccf98), [set task status](operations-013.md#op-3f6833b3799d67), [validate assignee](operations-013.md#op-8666bd302d084e).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1633) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L513)

<a id="op-8666bd302d084e"></a>
### Asset Maintenance.validate assignee

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_asset_maintenance_assetmaintenance_validate_assignee`

**Inputs** self, task, team\_members.

**Explicit results** no value.

**Local steps**

- If task.maintenance\_status equals “Cancelled”.
  - Return no value.
- If (not task.assign\_to and self.docstatus equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not task.assign\_to → self.docstatus equals 0.
  - Evaluate throw(translated “Row #{}: Please assign task to a member.”.format(task.idx)).
- If (task.assign\_to and task.assign\_to does not belong to team\_members).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in task.assign\_to → task.assign\_to does not belong to team\_members.
  - Evaluate throw(translated “Row #{0}: {1} is not a member of the maintenance team {2}”.format(task.idx, task.assign\_to, self.maintenance\_team)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L733) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1371)

<a id="op-7aa9c7157ccf98"></a>
### Asset Maintenance.validate asset

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_asset_maintenance_assetmaintenance_validate_asset`

**Inputs** self.

**Record and data access** read “Asset” via get\_value.

**Local steps**

- If Platform.db.get\_value(“Asset”, self.asset\_name, “docstatus”) differs from 1.
  - Evaluate throw(translated “Asset {0} must be submitted”.format(self.asset\_name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L732) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1370)

<a id="op-3f6833b3799d67"></a>
### Asset Maintenance.set task status

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_asset_maintenance_assetmaintenance_set_task_status`

**Inputs** self, task.

**Explicit results** no value.

**Local steps**

- If task.maintenance\_status equals “Cancelled”.
  - Return no value.
- If getdate(task.next\_due\_date) &lt; getdate(nowdate()).
  - Set task.maintenance\_status from “Overdue”.
- Otherwise.
  - If task.maintenance\_status equals “Overdue”.
    - Set task.maintenance\_status from “Planned”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1369)

<a id="op-9ed94bd58cc2f0"></a>
### Asset Maintenance.on update

`operation_enterprise_assets_record_definitions_asset_maintenance_business_behavior_asset_maintenance_on_update`

**Inputs** self.

**Local steps**

- For each task in self.get\_active\_tasks().
  - Evaluate assign\_tasks(self.name, task.assign\_to, task.maintenance\_task, task.next\_due\_date).
- Evaluate self.close\_unassigned\_todos().
- Evaluate self.sync\_maintenance\_tasks().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get active tasks](operations-013.md#op-0b1edaddd62e3c), [close unassigned todos](operations-013.md#op-42c771ac6f54eb), [sync maintenance tasks](operations-013.md#op-b0f4b09ba1df71).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1631) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L511)

<a id="op-4910067df8e11a"></a>
### Asset Maintenance.on trash

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_asset_maintenance_assetmaintenance_on_trash`

**Inputs** self.

**Record and data access** read “Asset Maintenance Log” via get\_all.

**State and service calls** request delete\_doc for “Asset Maintenance Log”.

**Local steps**

- Set draft\_logs from Platform.get\_all(“Asset Maintenance Log”, filters = mapping(“asset\_maintenance” → self.name, “docstatus” → 0), pluck = “name”).
- For each log in draft\_logs.
  - Evaluate Platform.delete\_doc(“Asset Maintenance Log”, log, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L730) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1368)

<a id="op-50b45007c491e3"></a>
### Asset Maintenance.after delete

`operation_enterprise_assets_record_definitions_asset_maintenance_business_behavior_asset_maintenance_after_delete`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_doc.

**Local steps**

- Set asset from Platform.get\_doc(“Asset”, self.asset\_name).
- If asset.status equals “In Maintenance”.
  - Evaluate asset.set\_status().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0326.json#L2970) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L510)

<a id="op-42c771ac6f54eb"></a>
### Asset Maintenance.close unassigned todos

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_asset_maintenance_assetmaintenance_close_unassigned_todos`

**Inputs** self.

**Record and data access** read “ToDo” via get\_all.

**Local steps**

- Set assignees from list of task.assign\_to for task drawn from self.get\_active\_tasks().
  - Draw task from self.get\_active\_tasks().
- Set unassigned\_users from Platform.get\_all(“ToDo”, filters = mapping(“reference\_type” → self.doctype, “reference\_name” → self.name, “status” → “Open”, “allocated\_to” → tuple(“not in”, (assignees or list(empty text)))), pluck = “all ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in assignees → list(empty text).
- For each user in unassigned\_users.
  - Evaluate assign\_to.remove(self.doctype, self.name, user).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get active tasks](operations-013.md#op-0b1edaddd62e3c).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1366)

<a id="op-0b1edaddd62e3c"></a>
### Asset Maintenance.get active tasks

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_asset_maintenance_assetmaintenance_get_active_tasks`

**Inputs** self.

**Declared result** list.

**Explicit results** list of task for task drawn from self.asset\_maintenance\_tasks where task.maintenance\_status differs from “Cancelled”.

**Local steps**

- Return list of task for task drawn from self.asset\_maintenance\_tasks where task.maintenance\_status differs from “Cancelled”.
  - Draw task from self.asset\_maintenance\_tasks, keep a combination only if (task.maintenance\_status differs from “Cancelled”).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1367)

<a id="op-b0f4b09ba1df71"></a>
### Asset Maintenance.sync maintenance tasks

`operation_enterprise_assets_record_definitions_asset_maintenance_business_behavior_asset_maintenance_sync_maintenance_tasks`

**Inputs** self.

**Record and data access** read “Asset Maintenance Log” via get\_all · resolve a document from “Asset Maintenance Log” via get\_doc.

**State and service calls** call db\_set on maintenance\_log.

**Local steps**

- Set tasks\_names from list().
- For each task in self.get(“asset\_maintenance\_tasks”).
  - If task.maintenance\_status equals “Cancelled”.
    - Continue with the next iteration or loop test.
  - Evaluate tasks\_names.append(task.name).
  - Evaluate update\_maintenance\_log(asset\_maintenance = self.name, item\_code = self.item\_code, item\_name = self.item\_name, task = task).
- Set asset\_maintenance\_logs from Platform.get\_all(“Asset Maintenance Log”, fields = list(“name”), filters = mapping(“asset\_maintenance” → self.name, “task” → tuple(“not in”, tasks\_names), “docstatus” → 0, “maintenance\_status” → tuple(“in” ….
- If asset\_maintenance\_logs.
  - For each asset\_maintenance\_log in asset\_maintenance\_logs.
    - Set maintenance\_log from Platform.get\_doc(“Asset Maintenance Log”, asset\_maintenance\_log.name).
    - Evaluate maintenance\_log.db\_set(“maintenance\_status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1632) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L512)

<a id="op-dcb48f464320de"></a>
### Assign tasks

`operation_enterprise_assets_record_definitions_asset_maintenance_business_behavior_assign_tasks`

**Inputs** asset\_maintenance\_name, assign\_to\_member, maintenance\_task, next\_due\_date.

**Record and data access** read “ToDo” via exists.

**Local steps**

- Set args from mapping(“doctype” → “Asset Maintenance”, “assign\_to” → assign\_to\_member, “name” → asset\_maintenance\_name, “description” → maintenance\_task, …).
- If not Platform.db.exists(“ToDo”, mapping(“reference\_type” → args at “doctype”, “reference\_name” → args at “name”, “status” → “Open”, “allocated\_to” → args at “assign\_to”)).
  - Set args at “assign\_to” from list(args at “assign\_to”).
  - Evaluate assign\_to.add(args).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1634) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L514)

<a id="op-e6d0fcc9def73a"></a>
### Calculate next due date

`operation_enterprise_assets_record_definitions_asset_maintenance_business_behavior_calculate_next_due_date`

**Inputs** periodicity, start\_date = no value, end\_date = no value, last\_completion\_date = no value, next\_due\_date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** next\_due\_date.

**Local steps**

- If (not start\_date and not last\_completion\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not start\_date → not last\_completion\_date.
  - Set start\_date from Platform.utils.now().
- If (last\_completion\_date and ((start\_date and last\_completion\_date &gt; start\_date) or not start\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_completion\_date → ((start\_date and last\_completion\_date &gt; start\_date) or not start\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (start\_date and last\_completion\_date &gt; start\_date) → not start\_date.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in start\_date → last\_completion\_date &gt; start\_date.
  - Set start\_date from last\_completion\_date.
- If periodicity equals “Daily”.
  - Set next\_due\_date from add\_days(start\_date, 1).
- If periodicity equals “Weekly”.
  - Set next\_due\_date from add\_days(start\_date, 7).
- If periodicity equals “Monthly”.
  - Set next\_due\_date from add\_months(start\_date, 1).
- If periodicity equals “Quarterly”.
  - Set next\_due\_date from add\_months(start\_date, 3).
- If periodicity equals “Half-yearly”.
  - Set next\_due\_date from add\_months(start\_date, 6).
- If periodicity equals “Yearly”.
  - Set next\_due\_date from add\_years(start\_date, 1).
- If periodicity equals “2 Yearly”.
  - Set next\_due\_date from add\_years(start\_date, 2).
- If periodicity equals “3 Yearly”.
  - Set next\_due\_date from add\_years(start\_date, 3).
- If (end\_date and ((start\_date and getdate(start\_date) ≥ getdate(end\_date)) or (last\_completion\_date and getdate(last\_completion\_date) ≥ getdate(end\_date)) or (next\_due\_date and getdate(next\_due\_date) &gt; getdat ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in end\_date → ((start\_date and getdate(start\_date) ≥ getdate(end\_date)) or (last\_completion\_date and getdate(last\_completion\_date) ≥ getdate(end\_date)) or (next\_due\_date and getdate(next\_due\_date) &gt; getdate(end\_date))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (start\_date and getdate(start\_date) ≥ getdate(end\_date)) → (last\_completion\_date and getdate(last\_completion\_date) ≥ getdate(end\_date)) → (next\_due\_date and getdate(next\_due\_date) &gt; getdate(end\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in start\_date → getdate(start\_date) ≥ getdate(end\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_completion\_date → getdate(last\_completion\_date) ≥ getdate(end\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in next\_due\_date → getdate(next\_due\_date) &gt; getdate(end\_date).
  - Set next\_due\_date from empty text.
- Return next\_due\_date.

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L515)

<a id="op-f6e41ead88a23e"></a>
### Update maintenance log

`operation_enterprise_assets_record_definitions_asset_maintenance_business_behavior_update_maintenance_log`

**Inputs** asset\_maintenance, item\_code, item\_name, task.

**Record and data access** read “Asset Maintenance Log” via get\_value · resolve a document from mapping(“doctype” → “Asset Maintenance Log”, “asset\_maintenance” → asset\_maintenance, “asset\_name” → asset\_maintenance, “item\_code” → item\_code, …) via get\_doc · resolve a document from “Asset Maintenance Log” via get\_doc.

**State and service calls** call insert on asset\_maintenance\_log · call save on maintenance\_log.

**Explicit results** no value.

**Local steps**

- Set asset\_maintenance\_log from Platform.get\_value(“Asset Maintenance Log”, mapping(“asset\_maintenance” → asset\_maintenance, “task” → task.name, “maintenance\_status” → tuple(“in”, list(“Planned”, “Overdue”)))).
- If not asset\_maintenance\_log.
  - If not task.next\_due\_date.
    - Return no value.
  - Set asset\_maintenance\_log from Platform.get\_doc(mapping(“doctype” → “Asset Maintenance Log”, “asset\_maintenance” → asset\_maintenance, “asset\_name” → asset\_maintenance, “item\_code” → item\_code, …)).
  - Evaluate asset\_maintenance\_log.insert(ignore\_permissions = true).
- Otherwise.
  - Set maintenance\_log from Platform.get\_doc(“Asset Maintenance Log”, asset\_maintenance\_log).
  - Set maintenance\_log.assign\_to\_name from task.assign\_to\_name.
  - Set maintenance\_log.has\_certificate from task.certificate\_required.
  - Set maintenance\_log.description from task.description.
  - Set maintenance\_log.periodicity from str(task.periodicity).
  - Set maintenance\_log.maintenance\_type from task.maintenance\_type.
  - Set maintenance\_log.due\_date from task.next\_due\_date.
  - Evaluate maintenance\_log.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1638) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L518)

<a id="op-d4c424868a3785"></a>
### Get team members

`operation_enterprise_assets_record_definitions_asset_maintenance_business_behavior_get_team_members`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Maintenance Team Member” via get\_all.

**Explicit results** Platform.get\_all(“Maintenance Team Member”, filters = mapping(“parent” → team, “parenttype” → “Asset Maintenance Team”, “team\_member” → tuple(“like”, formatted text %{txt}%)), fields = list(“team\_member”), ….

**Local steps**

- Set team from filters.get(“maintenance\_team”).
- Evaluate Platform.has\_permission(“Asset Maintenance Team”, “select”, team, throw = true).
- Return Platform.get\_all(“Maintenance Team Member”, filters = mapping(“parent” → team, “parenttype” → “Asset Maintenance Team”, “team\_member” → tuple(“like”, formatted text %{txt}%)), fields = list(“team\_member”), ….

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset Maintenance Team”, “select”, team, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1637) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L517)

<a id="op-97a23e6c4b8157"></a>
### Get maintenance log

`operation_enterprise_assets_record_definitions_asset_maintenance_business_behavior_get_maintenance_log`

**Inputs** asset\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Asset Maintenance Log” via get\_list.

**Explicit results** Platform.get\_list(“Asset Maintenance Log”, filters = mapping(“asset\_name” → asset\_name), fields = list(“maintenance\_status”, mapping(“COUNT” → “asset\_name”, “as” → “count”), “asset\_name”), group\_by = “main ….

**Local steps**

- Return Platform.get\_list(“Asset Maintenance Log”, filters = mapping(“asset\_name” → asset\_name), fields = list(“maintenance\_status”, mapping(“COUNT” → “asset\_name”, “as” → “count”), “asset\_name”), group\_by = “main ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L516)

## Record · Asset maintenance log

[Record definition](../../../../data/record-types/asset_maintenance_log.json)

<a id="op-5441993776042b"></a>
### Asset Maintenance Log.validate

`operation_enterprise_assets_record_definitions_asset_maintenance_log_business_behavior_asset_maintenance_log_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please select Completion Date for Completed Asset Maintenance Log” · validation helper — translated “Completion Date cannot be in the future” · validation helper — translated “Please select Maintenance Status as Completed or remove Completion Date”.

**Local steps**

- Evaluate self.validate\_task().
- If self.maintenance\_status belongs to tuple(“Planned”, “Overdue”).
  - Set self.maintenance\_status from “Overdue” when getdate(self.due\_date) &lt; getdate(nowdate()), otherwise “Planned”.
    - Value choice on getdate(self.due\_date) &lt; getdate(nowdate()) — true gives “Overdue”, false gives “Planned”.
- If (self.maintenance\_status equals “Completed” and not self.completion\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.maintenance\_status equals “Completed” → not self.completion\_date.
  - Call the validation error handler Platform.throw(translated “Please select Completion Date for Completed Asset Maintenance Log”).
- If (self.completion\_date and getdate(self.completion\_date) &gt; getdate(nowdate())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.completion\_date → getdate(self.completion\_date) &gt; getdate(nowdate()).
  - Call the validation error handler Platform.throw(translated “Completion Date cannot be in the future”).
- If (self.maintenance\_status differs from “Completed” and self.completion\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.maintenance\_status differs from “Completed” → self.completion\_date.
  - Call the validation error handler Platform.throw(translated “Please select Maintenance Status as Completed or remove Completion Date”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate task](operations-013.md#op-92f66682a37003).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1641) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L521)

<a id="op-92f66682a37003"></a>
### Asset Maintenance Log.validate task

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_log_asset_maintenance_log_assetmaintenancelog_validate_task`

**Inputs** self.

**Record and data access** read “Asset Maintenance Task” via get\_value.

**Explicit failure paths** validation helper — translated “Please select a Task” · validation helper — translated “Task {0} does not belong to Asset Maintenance {1}”.format(self.task, self.asset\_maintenance).

**Local steps**

- If not self.task.
  - Call the validation error handler Platform.throw(translated “Please select a Task”).
- If Platform.db.get\_value(“Asset Maintenance Task”, self.task, “parent”) differs from self.asset\_maintenance.
  - Call the validation error handler Platform.throw(translated “Task {0} does not belong to Asset Maintenance {1}”.format(self.task, self.asset\_maintenance)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L738) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1376)
