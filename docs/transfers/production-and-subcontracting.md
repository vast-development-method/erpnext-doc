# Production and subcontracting conversions

[Structured field mappings](production-and-subcontracting.json) · [All conversions](README.md)

## Commission outsourced manufacture on a purchase order

`procurement.purchase_order` → `subcontracting.subcontracting_order`

Admit service rows whose ordered quantity exceeds their subcontracted quantity. Recompute outstanding service quantity, finished-good quantity and amount. Carry the production-plan reference when the relevant service rows identify one plan. Determine material reservation from the automatic or plan policy. A job-card link can supply the supplier work-in-progress warehouse.

On purchase order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `procurement.purchase_order_item.record_identifier` | `subcontracting.subcontracting_order_service_item.purchase_order_item` |
| `procurement.purchase_order_item.material_request_identifier` | `subcontracting.subcontracting_order_service_item.material_request_identifier` |
| `procurement.purchase_order_item.material_request_item` | `subcontracting.subcontracting_order_service_item.material_request_item` |

## Create a variant manufacturing recipe

`manufacturing.bill_of_materials` → `manufacturing.bill_of_materials`

Use the selected variant as the new output. Exclude template component rows that require a variant choice. For rows supplied by the variant-resolution step, derive component and stock quantities using the output scale and the component's conversion factor and field precision.

On bill of materials, require lifecycle state equals posted.

## Purchase an externally performed operation

`manufacturing.job_card` → `procurement.purchase_order`

Mark the purchase as subcontracted and use the card's work-in-progress warehouse as the supplier warehouse. Generate the ordered service product for the operation and preserve its link back to the operation card.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.job_card.work_in_progress_warehouse_identifier` | `procurement.purchase_order.supplier_warehouse_identifier` |
| `manufacturing.job_card.finished_good_identifier` | `procurement.purchase_order_item.finished_goods_item_identifier` |
| `manufacturing.job_card.record_identifier` | `procurement.purchase_order_item.job_card_identifier` |

## Request materials for an operation card

`manufacturing.job_card` → `inventory.material_request`

Generate a material transfer request to the card's work-in-progress warehouse. In shortage mode use the calculated shortage per card-material row. Where excess transfer is disallowed, cap requested quantities at pending requirement. Drop ineligible rows instead of requesting the whole operation quantity again.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.job_card.record_identifier` | `inventory.material_request.job_card_identifier` |
| `manufacturing.job_card_item.required_quantity` | `inventory.material_request_item.quantity` |
| `manufacturing.job_card_item.unit_of_measure_identifier` | `inventory.material_request_item.stock_unit_of_measure_identifier` |
| `manufacturing.job_card_item.record_identifier` | `inventory.material_request_item.job_card_item` |
| `manufacturing.job_card.work_in_progress_warehouse_identifier` | `inventory.material_request_item.warehouse_identifier` |

## Transfer components for an operation card

`manufacturing.job_card` → `inventory.stock_entry`

Select positive required quantities, respecting the excess-transfer policy and already transferred quantity. Point the target warehouse to work in progress. Set material transfer for manufacture as the purpose. Resolve finished units still due, recipe and substitution authority independently of the component quantity.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.job_card.record_identifier` | `inventory.stock_entry.job_card_identifier` |
| `manufacturing.job_card.for_quantity` | `inventory.stock_entry.finished_goods_completed_quantity` |
| `manufacturing.job_card_item.source_warehouse_identifier` | `inventory.stock_entry_detail.source_warehouse_identifier` |
| `manufacturing.job_card_item.required_quantity` | `inventory.stock_entry_detail.quantity` |
| `manufacturing.job_card_item.record_identifier` | `inventory.stock_entry_detail.job_card_item` |
| `manufacturing.job_card.work_in_progress_warehouse_identifier` | `inventory.stock_entry_detail.target_warehouse_identifier` |

## Open a corrective operation card

`manufacturing.job_card` → `manufacturing.job_card`

Mark the card as corrective and retain the original card identity. Select the corrective operation and the operation being corrected. Reset completed, lost and pending quantity fields before the new work is recorded.

| Calculated destination field | Rule after initial copying |
|---|---|
| `manufacturing.job_card.total_completed_quantity` | Zero before recording the corrective work. |
| `manufacturing.job_card.process_loss_quantity` | Zero before recording losses on the corrective work. |
| `manufacturing.job_card.pending_quantity` | Zero at initialisation. |

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.job_card.record_identifier` | `manufacturing.job_card.for_job_card_identifier` |

## Create a master schedule for a sales forecast

`manufacturing.sales_forecast` → `manufacturing.master_production_schedule`

Require the forecast to be submitted and in Planned state. Link the forecast and copy its start date. The schedule resolves actual open demand by item and location. Saving the schedule updates the linked forecast status.

On sales forecast, require lifecycle state equals posted, status equals Planned.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.sales_forecast.record_identifier` | `manufacturing.master_production_schedule.sales_forecast_identifier` |
| `manufacturing.sales_forecast.from_date` | `manufacturing.master_production_schedule.from_date` |

## Pick materials for a manufacturing order

`manufacturing.work_order` → `inventory.pick_list`

Allocate the required fraction of production, capped by still-unclaimed component quantities. Preserve the product/source warehouse allocation when several material rows use the same product. Use material transfer for manufacture as the pick purpose and the requested finished quantity as its basis.

On work order, require lifecycle state equals posted.

## Request manufacturing order components

`manufacturing.work_order` → `inventory.material_request`

Use the material stock unit as the requesting unit, carry the source warehouse and set the destination to the work-in-progress warehouse. Add only positive allocated demand. Consume each allocation once across repeated source rows and date the new request line at the effective request date.

| Calculated destination field | Rule after initial copying |
|---|---|
| `inventory.material_request_item.quantity` | Allocated quantity remaining for this product, warehouse and operation group, consumed only once. |

On work order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.work_order.record_identifier` | `inventory.material_request.work_order_identifier` |
| `manufacturing.work_order_item.stock_unit_of_measure_identifier` | `inventory.material_request_item.unit_of_measure_identifier` |
| `manufacturing.work_order_item.source_warehouse_identifier` | `inventory.material_request_item.from_warehouse_identifier` |
| `manufacturing.work_order.work_in_progress_warehouse_identifier` | `inventory.material_request_item.warehouse_identifier` |

## Commission production for a customer

`sales.sales_order` → `subcontracting.subcontracting_inward_order`

Select unprocessed service rows from the submitted order and preserve the original service line. Generate the outstanding production requirements in the inward subcontract order. Customer-owned material receipts and service billing progress are independent.

On sales order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `sales.sales_order_item.record_identifier` | `subcontracting.subcontracting_inward_order_service_item.sales_order_item` |

## Receive the customer's components

`subcontracting.subcontracting_inward_order` → `inventory.stock_entry`

Prepare an inward material movement under the customer manufacturing order. Proposed material demand uses required less already received plus returned and the recipe-based quantity due to eligible process loss. Warehouse custody is distinct from company ownership.

On subcontracting inward order, require lifecycle state equals posted.

## Return unused material to a customer

`subcontracting.subcontracting_inward_order` → `inventory.stock_entry`

For customer-provided materials compute received less allocated work-order quantity less already returned. Issue only positive quantities from their recorded warehouse.

On subcontracting inward order, require lifecycle state equals posted.

## Deliver goods produced for a customer

`subcontracting.subcontracting_inward_order` → `inventory.stock_entry`

If overproduction delivery is enabled use produced quantity, otherwise use the lesser of ordered and produced. Subtract prior delivery progress and propose only positive remaining rows.

On subcontracting inward order, require lifecycle state equals posted.

## Accept a customer's return of manufactured goods

`subcontracting.subcontracting_inward_order` → `inventory.stock_entry`

Propose delivered units less units already returned. Retain the customer manufacturing order and output row so returns update the correct product balance.

On subcontracting inward order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `subcontracting.subcontracting_inward_order.record_identifier` | `inventory.stock_entry.subcontracting_inward_order_identifier` |

## Receive completed outsourced production

`subcontracting.subcontracting_order` → `subcontracting.subcontracting_receipt`

For unselected rows propose order quantity less received. For an explicit selection use the requested quantity or remaining quantity as applicable. Retain the underlying service order row. Calculate process loss as accepted proposal times the configured loss percentage at its field precision.

| Calculated destination field | Rule after initial copying |
|---|---|
| `subcontracting.subcontracting_receipt_item.quantity` | Use selected positive proposal if supplied, otherwise original order quantity less received quantity. |
| `subcontracting.subcontracting_receipt_item.received_quantity` | Proposed receipt quantity. |
| `subcontracting.subcontracting_receipt_item.process_loss_quantity` | Proposed quantity × process-loss percentage ÷ 100, rounded at the process-loss quantity precision. |

On subcontracting order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `subcontracting.subcontracting_order.supplier_warehouse_identifier` | `subcontracting.subcontracting_receipt.supplier_warehouse_identifier` |
| `subcontracting.subcontracting_order.default_warehouse_identifier` | `subcontracting.subcontracting_receipt.default_warehouse_identifier` |
| `subcontracting.subcontracting_order_item.record_identifier` | `subcontracting.subcontracting_receipt_item.subcontracting_order_item` |
| `subcontracting.subcontracting_order_item.owning_record_identifier` | `subcontracting.subcontracting_receipt_item.subcontracting_order_identifier` |
| `subcontracting.subcontracting_order_item.bill_of_materials_identifier` | `subcontracting.subcontracting_receipt_item.bill_of_materials_identifier` |

## Receive the supplier service linked to completed goods

`procurement.purchase_order` → `inventory.purchase_receipt`

Reconstruct service receipt rows from the associated purchase order and finished receipt. Include only order lines linked to the selected completed goods. Distinguish tax-withholding and merged tax rows so several purchases cannot duplicate fixed charges.

On purchase order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `procurement.purchase_order.supplier_warehouse_identifier` | `inventory.purchase_receipt.supplier_warehouse_identifier` |
| `procurement.purchase_order_item.record_identifier` | `inventory.purchase_receipt_item.purchase_order_item` |
| `procurement.purchase_order_item.owning_record_identifier` | `inventory.purchase_receipt_item.purchase_order_identifier` |
| `procurement.purchase_order_item.bill_of_materials_identifier` | `inventory.purchase_receipt_item.bill_of_materials_identifier` |

## Send company components to a supplier against purchase order

`procurement.purchase_order` → `inventory.stock_entry`

Set the movement purpose to sending to the subcontractor. Create material rows for the supplier warehouse from the order's eligible supplied materials. Preserve the governing order identity, whether it is a purchase order or a separate subcontract order.

On purchase order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `procurement.purchase_order.record_identifier` | `inventory.stock_entry.purchase_order_identifier` |

## Recover company components from a supplier against purchase order

`procurement.purchase_order` → `inventory.stock_entry`

Build a return transfer for the original order and company. Select the remaining transferable identities and reverse custody to the receiving warehouse. This is distinct from a return of completed goods.

| Source record and field | Destination record and field |
|---|---|
| `procurement.purchase_order.record_identifier` | `inventory.stock_entry.purchase_order_identifier` |

## Send company components to a supplier against subcontracting order

`subcontracting.subcontracting_order` → `inventory.stock_entry`

Set the movement purpose to sending to the subcontractor. Create material rows for the supplier warehouse from the order's eligible supplied materials. Preserve the governing order identity, whether it is a purchase order or a separate subcontract order.

On subcontracting order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `subcontracting.subcontracting_order.record_identifier` | `inventory.stock_entry.subcontracting_order_identifier` |

## Recover company components from a supplier against subcontracting order

`subcontracting.subcontracting_order` → `inventory.stock_entry`

Build a return transfer for the original order and company. Select the remaining transferable identities and reverse custody to the receiving warehouse. This is distinct from a return of completed goods.

| Source record and field | Destination record and field |
|---|---|
| `subcontracting.subcontracting_order.record_identifier` | `inventory.stock_entry.subcontracting_order_identifier` |

## Release a finished product for internal manufacture

`manufacturing.production_plan` → `manufacturing.work_order`

Reload the open plan before issuing work. Closed and completed plans cannot release new orders. Generate an order only for positive remaining production demand. Inherit reservation policy and planned start or schedule date. Warehouse overrides on the plan line take precedence over defaults. Expand the recipe into required materials and operations when preparing the work order.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.production_plan.record_identifier` | `manufacturing.work_order.production_plan_identifier` |
| `manufacturing.production_plan.reserve_stock` | `manufacturing.work_order.reserve_stock` |
| `manufacturing.production_plan_item.record_identifier` | `manufacturing.work_order.production_plan_item` |
| `manufacturing.production_plan_item.item_identifier` | `manufacturing.work_order.production_item_identifier` |
| `manufacturing.production_plan_item.bill_of_materials_number_identifier` | `manufacturing.work_order.bill_of_materials_number_identifier` |
| `manufacturing.production_plan_item.warehouse_identifier` | `manufacturing.work_order.finished_goods_warehouse_identifier` |

## Release a manufactured subassembly

`manufacturing.production_plan` → `manufacturing.work_order`

Use subassembly rows classified for internal manufacture. Subtract work already allocated to the plan row and skip nonpositive amounts. Resolve source warehouse from the recipe, then apply the specific subassembly warehouse when set. The generated order retains the plan row and subassembly identity. A subcontracted subassembly or material-request row follows its own route.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.production_plan.record_identifier` | `manufacturing.work_order.production_plan_identifier` |
| `manufacturing.production_plan_sub_assembly_item.record_identifier` | `manufacturing.work_order.production_plan_sub_assembly_item` |
| `manufacturing.production_plan_sub_assembly_item.production_item_identifier` | `manufacturing.work_order.production_item_identifier` |
| `manufacturing.production_plan_sub_assembly_item.bill_of_materials_number_identifier` | `manufacturing.work_order.bill_of_materials_number_identifier` |
| `manufacturing.production_plan_sub_assembly_item.finished_goods_warehouse_identifier` | `manufacturing.work_order.finished_goods_warehouse_identifier` |

## Order outsourced plan subassemblies

`manufacturing.production_plan` → `procurement.purchase_order`

Select subcontract rows, consolidate outstanding requirements by supplier and take account of existing noncancelled purchase lines already linked to the plan. A supplier gets its own outsourced purchase order. Use finished-product quantity on the purchase line, the finished warehouse and the selected service item. Distinguish the scheduled procurement event from the later receipt of goods.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.production_plan.company_identifier` | `procurement.purchase_order.company_identifier` |
| `manufacturing.production_plan_sub_assembly_item.record_identifier` | `procurement.purchase_order_item.production_plan_sub_assembly_item` |
| `manufacturing.production_plan_sub_assembly_item.production_item_identifier` | `procurement.purchase_order_item.finished_goods_item_identifier` |
| `manufacturing.production_plan_sub_assembly_item.finished_goods_warehouse_identifier` | `procurement.purchase_order_item.warehouse_identifier` |

## Request planned materials

`manufacturing.production_plan` → `inventory.material_request`

Read the saved, writable, open plan. Group material requirements by sales order and request kind. Select positive remaining quantity after prior submitted requests and quantities in linked drafts converted back into the transaction unit. Reject a group warehouse. Use each required date or effective date plus item lead days. Preserve plan and requirement identities. Save drafts or submit according to the selected action.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.production_plan.company_identifier` | `inventory.material_request.company_identifier` |
| `manufacturing.material_request_plan_item.record_identifier` | `inventory.material_request_item.material_request_plan_item` |
| `manufacturing.material_request_plan_item.item_identifier` | `inventory.material_request_item.item_identifier` |
| `manufacturing.material_request_plan_item.warehouse_identifier` | `inventory.material_request_item.warehouse_identifier` |
| `manufacturing.material_request_plan_item.sales_order_identifier` | `inventory.material_request_item.sales_order_identifier` |
