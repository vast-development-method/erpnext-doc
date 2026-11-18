# Asset management · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset maintenance log

[Record definition](../../../../data/record-types/asset_maintenance_log.json)

<a id="op-617a4830e58a43"></a>
### Asset Maintenance Log.on submit

`operation_enterprise_assets_record_definitions_asset_maintenance_log_business_behavior_asset_maintenance_log_on_submit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Maintenance Status has to be Cancelled or Completed to Submit”.

**Local steps**

- <a id="op-617a4830e58a43-guard-2"></a>If self.maintenance\_status does not belong to list(“Completed”, “Cancelled”).
  - Call the validation error handler Platform.throw(translated “Maintenance Status has to be Cancelled or Completed to Submit”).
- Evaluate self.update\_maintenance\_task().
- Evaluate self.update\_asset\_status().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.maintenance\_status does not belong to list(“Completed”, “Cancelled”), self.maintenance\_status = “Planned” selects the branch that calls the validation-error handler with translated “Maintenance Status has to be Cancelled or Completed to Submit”. With self.maintenance\_status = “Completed”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-617a4830e58a43-guard-2)

**Methods declared on this owner** [update maintenance task](operations-014.md#op-86f7d09e605a21), [update asset status](operations-014.md#op-cd5c7880b1aaca).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1639) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L519)

<a id="op-fab398bffbbe3f"></a>
### Asset Maintenance Log.on cancel

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_log_asset_maintenance_log_assetmaintenancelog_on_cancel`

**Inputs** self.

**Local steps**

- If self.maintenance\_status equals “Completed”.
  - Evaluate self.revert\_maintenance\_task().

If control reaches the end, it returns no value.

**Methods declared on this owner** [revert maintenance task](operations-014.md#op-129f4b5e0f0583).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L735) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1373)

<a id="op-129f4b5e0f0583"></a>
### Asset Maintenance Log.revert maintenance task

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_log_asset_maintenance_log_assetmaintenancelog_revert_maintenance_task`

**Inputs** self.

**Record and data access** resolve a document from “Asset Maintenance Task” via get\_doc · read “Asset Maintenance Log” via get\_value · resolve a document from “Asset Maintenance” via get\_doc.

**State and service calls** call save on task · call save on Platform.get\_doc(“Asset Maintenance”, self.asset\_maintenance).

**Explicit results** no value.

**Local steps**

- Set task from Platform.get\_doc(“Asset Maintenance Task”, self.task).
- If not self.drives\_task\_schedule(task).
  - Return no value.
- Set task.last\_completion\_date from Platform.db.get\_value(“Asset Maintenance Log”, mapping(“task” → self.task, “docstatus” → 1, “maintenance\_status” → “Completed”, “name” → tuple(“!=”, self.name)), “completion\_date”, order\_by = “completion\_date desc”).
- Set task.next\_due\_date from self.due\_date.
- Evaluate task.save().
- Evaluate Platform.get\_doc(“Asset Maintenance”, self.asset\_maintenance).save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [drives task schedule](operations-014.md#op-03dc3e117424fc).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L736) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1374)

<a id="op-03dc3e117424fc"></a>
### Asset Maintenance Log.drives task schedule

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_log_asset_maintenance_log_assetmaintenancelog_drives_task_schedule`

**Inputs** self, task.

**Declared result** bool.

**Record and data access** read “Asset Maintenance Log” via exists.

**Explicit results** false · not Platform.db.exists(“Asset Maintenance Log”, mapping(“task” → self.task, “docstatus” → 1, “maintenance\_status” → “Completed”, “completion\_date” → self.completion\_date, …)).

**Local steps**

- If (not task.last\_completion\_date or getdate(task.last\_completion\_date) differs from getdate(self.completion\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not task.last\_completion\_date → getdate(task.last\_completion\_date) differs from getdate(self.completion\_date).
  - Return false.
- Return not Platform.db.exists(“Asset Maintenance Log”, mapping(“task” → self.task, “docstatus” → 1, “maintenance\_status” → “Completed”, “completion\_date” → self.completion\_date, …)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L734) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1372)

<a id="op-86f7d09e605a21"></a>
### Asset Maintenance Log.update maintenance task

`operation_enterprise_assets_record_definitions_asset_maintenance_log_business_behavior_asset_maintenance_log_update_maintenance_task`

**Inputs** self.

**Record and data access** resolve a document from “Asset Maintenance Task” via get\_doc · resolve a document from “Asset Maintenance” via get\_doc.

**State and service calls** call save on asset\_maintenance\_doc.

**Local steps**

- Set asset\_maintenance\_doc from Platform.get\_doc(“Asset Maintenance Task”, self.task).
- If self.maintenance\_status equals “Completed”.
  - If asset\_maintenance\_doc.last\_completion\_date differs from self.completion\_date.
    - Set next\_due\_date from calculate\_next\_due\_date(periodicity = self.periodicity, end\_date = asset\_maintenance\_doc.end\_date, last\_completion\_date = self.completion\_date).
    - Set asset\_maintenance\_doc.last\_completion\_date from self.completion\_date.
    - Set asset\_maintenance\_doc.next\_due\_date from next\_due\_date.
    - Set asset\_maintenance\_doc.maintenance\_status from “Planned”.
    - Evaluate asset\_maintenance\_doc.save().
- If self.maintenance\_status equals “Cancelled”.
  - Set asset\_maintenance\_doc.maintenance\_status from “Cancelled”.
  - Evaluate asset\_maintenance\_doc.save().
- Set asset\_maintenance\_doc from Platform.get\_doc(“Asset Maintenance”, self.asset\_maintenance).
- Evaluate asset\_maintenance\_doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L520)

<a id="op-cd5c7880b1aaca"></a>
### Asset Maintenance Log.update asset status

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_log_asset_maintenance_log_assetmaintenancelog_update_asset_status`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_doc.

**Local steps**

- Set asset from Platform.get\_doc(“Asset”, self.asset\_name).
- If (asset.status equals “In Maintenance” and not has\_due\_maintenance(asset.name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in asset.status equals “In Maintenance” → not has\_due\_maintenance(asset.name).
  - Evaluate asset.set\_status().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L737) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1375)

<a id="op-f925200f9a49b4"></a>
### Update asset maintenance log status

`operation_enterprise_assets_record_definitions_asset_maintenance_log_business_behavior_update_asset_maintenance_log_status`

**Inputs** no declared parameters.

**Local steps**

- Set AssetMaintenanceLog from DocType(“Asset Maintenance Log”).
- Evaluate nested operand in the contract(nested operand in the contract).set(AssetMaintenanceLog.maintenance\_status, “Overdue”).where((AssetMaintenanceLog.maintenance\_status equals “Planned” bitwise and AssetMainten ….run().
- Set AssetMaintenanceTask from DocType(“Asset Maintenance Task”).
- Evaluate nested operand in the contract(nested operand in the contract).set(AssetMaintenanceTask.maintenance\_status, “Overdue”).where((AssetMaintenanceTask.maintenance\_status equals “Planned” bitwise and AssetMaint ….run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1643) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L523)

<a id="op-2bced42a6057c2"></a>
### Get maintenance tasks

`operation_enterprise_assets_record_definitions_asset_maintenance_log_business_behavior_get_maintenance_tasks`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Asset Maintenance Task” via get\_all.

**Explicit results** Platform.get\_all(“Asset Maintenance Task”, filters = mapping(“parent” → asset\_maintenance, “parenttype” → “Asset Maintenance”), or\_filters = mapping(“name” → tuple(“like”, formatted text %{txt}%), “mainten ….

**Local steps**

- Set asset\_maintenance from filters.get(“asset\_maintenance”).
- Evaluate Platform.has\_permission(“Asset Maintenance”, “read”, asset\_maintenance, throw = true).
- Return Platform.get\_all(“Asset Maintenance Task”, filters = mapping(“parent” → asset\_maintenance, “parenttype” → “Asset Maintenance”), or\_filters = mapping(“name” → tuple(“like”, formatted text %{txt}%), “mainten ….

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset Maintenance”, “read”, asset\_maintenance, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1642) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L522)

## Record · Asset maintenance team

[Record definition](../../../../data/record-types/asset_maintenance_team.json)

<a id="op-b7a9bd5981cdbf"></a>
### Asset Maintenance Team.validate

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_team_asset_maintenance_team_assetmaintenanceteam_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_unique\_members().
- Evaluate self.validate\_manager\_is\_member().
- Evaluate self.validate\_removed\_members\_have\_no\_tasks().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate unique members](operations-014.md#op-aba17325fa2154), [validate manager is member](operations-014.md#op-2656d350b912ae), [validate removed members have no tasks](operations-014.md#op-d1999900f23b01).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1380)

<a id="op-aba17325fa2154"></a>
### Asset Maintenance Team.validate unique members

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_team_asset_maintenance_team_assetmaintenanceteam_validate_unique_members`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: {1} is already a member of this team.”.format(row.idx, Platform.bold(row.team\_member)).

**Local steps**

- Set members from set().
- For each row in self.maintenance\_team\_members.
  - If row.team\_member belongs to members.
    - Call the validation error handler Platform.throw(translated “Row #{0}: {1} is already a member of this team.”.format(row.idx, Platform.bold(row.team\_member))).
  - Evaluate members.add(row.team\_member).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L745) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1383)

<a id="op-2656d350b912ae"></a>
### Asset Maintenance Team.validate manager is member

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_team_asset_maintenance_team_assetmaintenanceteam_validate_manager_is_member`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Maintenance Manager {0} must be a member of the team.”.format(Platform.bold(self.maintenance\_manager)).

**Local steps**

- If not (self.is\_new() or self.has\_value\_changed(“maintenance\_manager”) or self.manager\_left\_members()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.has\_value\_changed(“maintenance\_manager”) → self.manager\_left\_members().
  - Return no value.
- If (self.maintenance\_manager and self.maintenance\_manager does not belong to self.get\_members()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.maintenance\_manager → self.maintenance\_manager does not belong to self.get\_members().
  - Call the validation error handler Platform.throw(translated “Maintenance Manager {0} must be a member of the team.”.format(Platform.bold(self.maintenance\_manager))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [manager left members](operations-014.md#op-1747b03506a30c), [get members](operations-014.md#op-0e82f3843a2106).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L743) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1381)

<a id="op-d1999900f23b01"></a>
### Asset Maintenance Team.validate removed members have no tasks

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_team_asset_maintenance_team_assetmaintenanceteam_validate_removed_members_have_no_tasks`

**Inputs** self.

**Record and data access** read “Asset Maintenance Task” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Reassign the maintenance tasks of {0} before removing them from the team.”.format(“, ”.join(generator of Platform.bold(assignee) for assignee drawn from assignees)).

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- Set removed\_members from (previous.get\_members() − self.get\_members()) when previous, otherwise set().
  - Value choice on previous — true gives (previous.get\_members() − self.get\_members()), false gives set().
- If not removed\_members.
  - Return no value.
- Set assignees from Platform.get\_all(“Asset Maintenance Task”, filters = mapping(“parenttype” → “Asset Maintenance”, “parent” → tuple(“in”, self.get\_asset\_maintenances()), “assign\_to” → tuple(“in”, removed\_members), “maintena ….
- If assignees.
  - Call the validation error handler Platform.throw(translated “Reassign the maintenance tasks of {0} before removing them from the team.”.format(“, ”.join(generator of Platform.bold(assignee) for assignee drawn from assignees))).
    - Draw assignee from assignees.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get members](operations-014.md#op-0e82f3843a2106), [get asset maintenances](operations-014.md#op-2144481bab5085).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L744) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1382)

<a id="op-1747b03506a30c"></a>
### Asset Maintenance Team.manager left members

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_team_asset_maintenance_team_assetmaintenanceteam_manager_left_members`

**Inputs** self.

**Declared result** bool.

**Explicit results** bool((previous and self.maintenance\_manager belongs to previous.get\_members() and self.maintenance\_manager does not belong to self.get\_members())).

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- Return bool((previous and self.maintenance\_manager belongs to previous.get\_members() and self.maintenance\_manager does not belong to self.get\_members())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous → self.maintenance\_manager belongs to previous.get\_members() → self.maintenance\_manager does not belong to self.get\_members().

**Methods declared on this owner** [get members](operations-014.md#op-0e82f3843a2106).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1379)

<a id="op-0e82f3843a2106"></a>
### Asset Maintenance Team.get members

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_team_asset_maintenance_team_assetmaintenanceteam_get_members`

**Inputs** self.

**Declared result** set at str.

**Explicit results** set of row.team\_member for row drawn from self.maintenance\_team\_members.

**Local steps**

- Return set of row.team\_member for row drawn from self.maintenance\_team\_members.
  - Draw row from self.maintenance\_team\_members.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L740) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1378)

<a id="op-2144481bab5085"></a>
### Asset Maintenance Team.get asset maintenances

`operation_enterprise_binding_enterprise_assets_doctype_asset_maintenance_team_asset_maintenance_team_assetmaintenanceteam_get_asset_maintenances`

**Inputs** self.

**Declared result** list at str.

**Record and data access** read “Asset Maintenance” via get\_all.

**Explicit results** Platform.get\_all(“Asset Maintenance”, filters = mapping(“maintenance\_team” → self.name), pluck = “name”).

**Local steps**

- Return Platform.get\_all(“Asset Maintenance”, filters = mapping(“maintenance\_team” → self.name), pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L739) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1377)

## Record · Asset movement

[Record definition](../../../../data/record-types/asset_movement.json)

<a id="op-c9749b34d97a5d"></a>
### Asset Movement.validate

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate\_assets().
- For each d in self.assets.
  - Evaluate self.validate\_asset(d).
  - Evaluate self.validate\_movement(d).
  - Evaluate self.validate\_transaction\_date(d).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate assets](operations-014.md#op-88e461e290c183), [validate asset](operations-014.md#op-5a4bf9a1b6aee8), [validate movement](operations-014.md#op-2fac0555733081), [validate transaction date](operations-014.md#op-e705686a0ba2e9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L534)

<a id="op-88e461e290c183"></a>
### Asset Movement.validate duplicate assets

`operation_enterprise_binding_enterprise_assets_doctype_asset_movement_asset_movement_assetmovement_validate_duplicate_assets`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Asset {1} is already added in another row”.format(d.idx, d.asset).

**Local steps**

- Set seen\_assets from set().
- For each d in self.assets.
  - If d.asset belongs to seen\_assets.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Asset {1} is already added in another row”.format(d.idx, d.asset)).
  - Evaluate seen\_assets.add(d.asset).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L747) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1385)

<a id="op-5a4bf9a1b6aee8"></a>
### Asset Movement.validate asset

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_validate_asset`

**Inputs** self, d.

**Record and data access** read “Asset” via get\_value.

**Explicit failure paths** validation helper — translated “Asset {0} is {1} and cannot be moved”.format(d.asset, translated status) · validation helper — translated “Asset {0} does not belong to company {1}”.format(d.asset, self.company).

**Local steps**

- Set tuple(status, company, docstatus) from Platform.db.get\_value(“Asset”, d.asset, list(“status”, “company”, “docstatus”)).
- If (docstatus differs from 1 or status belongs to tuple(“Scrapped”, “Sold”, “Capitalized”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in docstatus differs from 1 → status belongs to tuple(“Scrapped”, “Sold”, “Capitalized”).
  - Call the validation error handler Platform.throw(translated “Asset {0} is {1} and cannot be moved”.format(d.asset, translated status)).
- If company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Asset {0} does not belong to company {1}”.format(d.asset, self.company)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L535)

<a id="op-2fac0555733081"></a>
### Asset Movement.validate movement

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_validate_movement`

**Inputs** self, d.

**Local steps**

- If self.purpose equals “Transfer and Issue”.
  - Evaluate self.validate\_location\_and\_employee(d).
- Otherwise.
  - If self.purpose belongs to list(“Receipt”, “Transfer”).
    - Evaluate self.validate\_location(d).
  - Otherwise.
    - Evaluate self.validate\_employee(d).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate location and employee](operations-014.md#op-91860d1a34de52), [validate location](operations-014.md#op-61187e348086e9), [validate employee](operations-014.md#op-4e0c7968a0e205).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0327.json#L2100) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L539)

<a id="op-e705686a0ba2e9"></a>
### Asset Movement.validate transaction date

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_validate_transaction_date`

**Inputs** self, d.

**Record and data access** read “Asset Movement” via get\_value.

**Explicit failure paths** validation helper — translated “Transaction date can't be earlier than previous movement date”.

**Local steps**

- Set previous\_movement\_date from Platform.db.get\_value(“Asset Movement”, list(list(“Asset Movement Item”, “asset”, “=”, d.asset), list(“docstatus”, “=”, 1)), “transaction\_date”, order\_by = “transaction\_date desc”).
- If (previous\_movement\_date and get\_datetime(previous\_movement\_date) &gt; get\_datetime(self.transaction\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_movement\_date → get\_datetime(previous\_movement\_date) &gt; get\_datetime(self.transaction\_date).
  - Call the validation error handler Platform.throw(translated “Transaction date can't be earlier than previous movement date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0327.json#L2276) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L540)

<a id="op-91860d1a34de52"></a>
### Asset Movement.validate location and employee

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_validate_location_and_employee`

**Inputs** self, d.

**Local steps**

- Evaluate self.validate\_location(d).
- Evaluate self.validate\_employee(d).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate location](operations-014.md#op-61187e348086e9), [validate employee](operations-014.md#op-4e0c7968a0e205).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0327.json#L2536) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L538)

<a id="op-61187e348086e9"></a>
### Asset Movement.validate location

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_validate_location`

**Inputs** self, d.

**Record and data access** read “Asset” via get\_value · read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “Asset {0} does not belong to the location {1}”.format(d.asset, d.source\_location) · validation helper — translated “Target Location is required for transferring Asset {0}”.format(d.asset) · validation helper — translated “Source and Target Location cannot be same” · validation helper — translated “Target Location is required while receiving Asset {0}”.format(d.asset) · validation helper — translated “Employee {0} does not belong to the company {1}”.format(d.to\_employee, self.company).

**Local steps**

- If self.purpose belongs to list(“Transfer”, “Transfer and Issue”).
  - Set current\_location from Platform.db.get\_value(“Asset”, d.asset, “location”).
  - If d.source\_location.
    - If current\_location differs from d.source\_location.
      - Call the validation error handler Platform.throw(translated “Asset {0} does not belong to the location {1}”.format(d.asset, d.source\_location)).
  - Otherwise.
    - Set d.source\_location from current\_location.
  - If not d.target\_location.
    - Call the validation error handler Platform.throw(translated “Target Location is required for transferring Asset {0}”.format(d.asset)).
  - If d.source\_location equals d.target\_location.
    - Call the validation error handler Platform.throw(translated “Source and Target Location cannot be same”).
- If self.purpose equals “Receipt”.
  - If not d.target\_location.
    - Call the validation error handler Platform.throw(translated “Target Location is required while receiving Asset {0}”.format(d.asset)).
  - If (d.to\_employee and Platform.db.get\_value(“Employee”, d.to\_employee, “company”) differs from self.company).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.to\_employee → Platform.db.get\_value(“Employee”, d.to\_employee, “company”) differs from self.company.
    - Call the validation error handler Platform.throw(translated “Employee {0} does not belong to the company {1}”.format(d.to\_employee, self.company)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0327.json#L2624) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L537)

<a id="op-4e0c7968a0e205"></a>
### Asset Movement.validate employee

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_validate_employee`

**Inputs** self, d.

**Record and data access** read “Asset” via get\_value · read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “From Employee is required while issuing Asset {0}”.format(d.asset) · validation helper — translated “Asset {0} does not belong to the custodian {1}”.format(d.asset, d.from\_employee) · validation helper — translated “Employee is required while issuing Asset {0}”.format(d.asset) · validation helper — translated “Employee {0} does not belong to the company {1}”.format(d.to\_employee, self.company).

**Local steps**

- If self.purpose equals “Transfer and Issue”.
  - If not d.from\_employee.
    - Call the validation error handler Platform.throw(translated “From Employee is required while issuing Asset {0}”.format(d.asset)).
- If d.from\_employee.
  - Set current\_custodian from Platform.db.get\_value(“Asset”, d.asset, “custodian”).
  - If current\_custodian differs from d.from\_employee.
    - Call the validation error handler Platform.throw(translated “Asset {0} does not belong to the custodian {1}”.format(d.asset, d.from\_employee)).
- If not d.to\_employee.
  - Call the validation error handler Platform.throw(translated “Employee is required while issuing Asset {0}”.format(d.asset)).
- If (d.to\_employee and Platform.db.get\_value(“Employee”, d.to\_employee, “company”) differs from self.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.to\_employee → Platform.db.get\_value(“Employee”, d.to\_employee, “company”) differs from self.company.
  - Call the validation error handler Platform.throw(translated “Employee {0} does not belong to the company {1}”.format(d.to\_employee, self.company)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0327.json#L3264) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L536)

<a id="op-b84659661c0783"></a>
### Asset Movement.on submit

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.set\_latest\_location\_and\_custodian\_in\_asset().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set latest location and custodian in asset](operations-015.md#op-29b48f812c00b4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0327.json#L3784) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L531)
