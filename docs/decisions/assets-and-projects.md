# Asset custody, maintenance and project time

Custody checks depend on the asset’s current recorded location and custodian. Project planning and billing depend on the selected task, project, time record and activity rate.

## Asset category

Logical record `fixed_assets.asset_category`. [Field definitions and declared grants](../../schema/entities/fixed-assets.json)

| Operation | Refuse when |
|---|---|
| Set residual-value policy | The salvage percentage lies outside the inclusive interval from 0 through 100. |
| Set depreciation rate | The rate is negative. |

## Asset maintenance team

Logical record `fixed_assets.asset_maintenance_team`. [Field definitions and declared grants](../../schema/entities/fixed-assets.json)

| Operation | Refuse when |
|---|---|
| Define asset maintenance membership | One person appears more than once on the same team. |
| Assign the maintenance manager | The nominated manager is missing from the team’s members. |
| Remove a maintenance team member | The person still has maintenance tasks requiring reassignment. |

## Asset movement

Logical record `fixed_assets.asset_movement`. [Field definitions and declared grants](../../schema/entities/fixed-assets.json)

| Operation | Refuse when |
|---|---|
| Record an asset movement | The same asset occurs more than once in the proposed movement. |
| Move an asset | The asset has not been submitted, or its status is sold, scrapped or capitalized into another asset. |
| Move an asset | The asset belongs to a company other than the movement company. |
| Backdate a custody movement | The most recent submitted movement for the asset has a later transaction instant than the proposed movement. |
| Confirm a transfer’s source | A supplied source location differs from the asset’s current location. |
| Transfer an asset | The source and target locations are identical. |
| Validate a change of custodian | The supplied releasing employee differs from the asset’s current custodian. |

## Asset repair

Logical record `fixed_assets.asset_repair`. [Field definitions and declared grants](../../schema/entities/fixed-assets.json)

| Operation | Refuse when |
|---|---|
| Accept an asset for repair | Its status is sold, scrapped or capitalized. |
| Mark a repair complete | No completion date was supplied. |
| Date a repair completion | The supplied completion predates the failure. |

## Activity cost

Logical record `projects.activity_cost`. [Field definitions and declared grants](../../schema/entities/projects.json)

| Operation | Refuse when |
|---|---|
| Set an employee activity rate | Another rate for that same employee and activity already exists. |
| Define a default activity rate | An existing employee-independent rate already covers the same activity. |

## Project template

Logical record `projects.project_template`. [Field definitions and declared grants](../../schema/entities/projects.json)

| Operation | Refuse when |
|---|---|
| Assemble a project template | A selected task is not marked as a template task. |
| Schedule a child template task | Child start offset plus duration exceeds the corresponding sum for its parent. |
| Save template dependencies | A dependency of a selected task is absent from the template. |

## Timesheet detail

Logical record `projects.timesheet_detail`. [Field definitions and declared grants](../../schema/entities/projects.json)

| Operation | Refuse when |
|---|---|
| Validate elapsed time | The time row contains negative hours. Zero is handled separately at submission. |
| Validate elapsed interval | Both timestamps are present and the end precedes the beginning. |
| Attribute a time row to a project | A project fixed on the timesheet header differs from the row project. |
| Attribute a task-linked time row | The selected task has a project that differs from the project on the row. |
| Classify a time row | The selected activity type has been disabled. |
