# Service and projects conversions

[Structured field mappings](service-and-projects.json) · [All conversions](README.md)

## Schedule maintenance from a customer invoice

`accounting.sales_invoice` → `maintenance.maintenance_schedule`

Invoice product rows provide the maintenance lines. The destination owns the service intervals, visit generation and service personnel. Preparing the schedule does not create completed visits.

On sales invoice, require lifecycle state equals posted.

## Perform a scheduled maintenance visit

`maintenance.maintenance_schedule` → `maintenance.maintenance_visit`

Set the service type to scheduled. A selected schedule-detail identifier selects that occurrence, otherwise eligible incompletely visited rows can be proposed. Where one serial is selected use it for the visit purpose. Retain the responsible service person and schedule-detail identity.

On maintenance schedule, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `maintenance.maintenance_schedule.record_identifier` | `maintenance.maintenance_visit.maintenance_schedule_identifier` |
| `maintenance.maintenance_schedule_detail.sales_person_identifier` | `maintenance.maintenance_visit_purpose.service_person_identifier` |
| `maintenance.maintenance_schedule_detail.record_identifier` | `maintenance.maintenance_visit_purpose.maintenance_schedule_detail` |

## Start a timesheet from a project task

`projects.task` → `projects.timesheet`

Set the parent project from the task and create its time-detail reference. Enter actual working intervals before using any resulting time for costing or billing.

| Source record and field | Destination record and field |
|---|---|
| `projects.task.project_identifier` | `projects.timesheet.parent_project_identifier` |
| `projects.task.record_identifier` | `projects.timesheet_detail.task_identifier` |
| `projects.task.project_identifier` | `projects.timesheet_detail.project_identifier` |
| `projects.task.actual_time` | `projects.timesheet_detail.hours` |

## Open an external project from a sales order

`sales.sales_order` → `projects.project`

Use the order identity as project name and order reference. Set external project kind. The order's company-currency grand total supplies the initial costing estimate while net sales supplies the initial sales measure. They are different accounting bases.

On sales order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `sales.sales_order.record_identifier` | `projects.project.sales_order_identifier` |
| `sales.sales_order.company_currency_grand_total` | `projects.project.estimated_costing` |
| `sales.sales_order.net_total` | `projects.project.total_sales_amount` |
| `sales.sales_order.record_identifier` | `projects.project.project_name` |

## Schedule service against a sales order

`sales.sales_order` → `maintenance.maintenance_schedule`

Create maintenance coverage lines for the order rows. The schedule and its generated visits establish the service dates independently of delivery and billing. A submitted schedule already referring to this order suppresses a second proposal.

On sales order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `sales.sales_order_item.owning_record_identifier` | `maintenance.maintenance_schedule_item.sales_order_identifier` |

## Record a service visit from a sales order

`sales.sales_order` → `maintenance.maintenance_visit`

Select order lines for the visit purposes, retaining their originating order. Set the responsible service person, serials, date and completion state before submitting the visit. A prior submitted, fully completed visit against the order suppresses the new proposal.

On sales order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `sales.sales_order_item.owning_record_identifier` | `maintenance.maintenance_visit_purpose.prevdoc_record_identifier` |
| `sales.sales_order_item.owning_entity_type` | `maintenance.maintenance_visit_purpose.prevdoc_entity_type_identifier` |

## Record installation after delivery

`inventory.delivery_note` → `sales.installation_note`

Propose delivered less returned less installed units, omitting exhausted lines. From an explicit serial list remove returned identities. Submission must recheck the row belongs to the named delivery, is still submitted and agrees on product, customer and company.

| Calculated destination field | Rule after initial copying |
|---|---|
| `sales.installation_note_item.quantity` | Delivered quantity less returned quantity less installed quantity, measured on the original delivery row. |

On delivery note, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `inventory.delivery_note_item.record_identifier` | `sales.installation_note_item.prevdoc_detail_record_identifier` |
| `inventory.delivery_note_item.owning_record_identifier` | `sales.installation_note_item.prevdoc_record_identifier` |
| `inventory.delivery_note_item.owning_entity_type` | `sales.installation_note_item.prevdoc_entity_type` |

## Prepare an inspection from a manufacturing recipe

`manufacturing.bill_of_materials` → `inventory.quality_inspection`

Take the inspected product and recipe reference from the submitted recipe. Assign the active inspector. The inspection records independent measurements and requires its own sample and release decision.

On bill of materials, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.bill_of_materials.record_identifier` | `inventory.quality_inspection.bill_of_materials_number_identifier` |
| `manufacturing.bill_of_materials.item_identifier` | `inventory.quality_inspection.item_identifier` |

## Plan work for a support issue

`customer_support.issue` → `projects.task`

Start a project task from the support issue. Its subject can carry forward. Assign scheduling, ownership and time on the task. A task’s progress does not close the issue.

| Source record and field | Destination record and field |
|---|---|
| `customer_support.issue.subject` | `projects.task.subject` |

## Perform service against a warranty claim

`customer_support.warranty_claim` → `maintenance.maintenance_visit`

Suppress a new visit when a submitted, fully completed visit already identifies this claim. Where the claim records a product, add a visit purpose and set its predecessor kind and record identity to the claim. Completing a visit can update resolution and work-performed facts.

| Source record and field | Destination record and field |
|---|---|
| `customer_support.warranty_claim.record_identifier` | `maintenance.maintenance_visit_purpose.prevdoc_record_identifier` |
| `customer_support.warranty_claim.entity_type` | `maintenance.maintenance_visit_purpose.prevdoc_entity_type_identifier` |
