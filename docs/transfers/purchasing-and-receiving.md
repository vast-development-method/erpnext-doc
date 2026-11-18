# Purchasing and receiving conversions

[Structured field mappings](purchasing-and-receiving.json) · [All conversions](README.md)

## Prepare stock movement from a supplier invoice

`accounting.purchase_invoice` → `inventory.stock_entry`

Use the invoiced row's stock-unit quantity as movement quantity and carry the batch when present. The movement is a separate stock authority. The operator must complete its purpose and warehouse legs before posting.

On purchase invoice, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `accounting.purchase_invoice_item.stock_quantity` | `inventory.stock_entry_detail.transferred_quantity` |
| `accounting.purchase_invoice_item.batch_number_identifier` | `inventory.stock_entry_detail.batch_number_identifier` |

## Receive goods from a supplier invoice

`accounting.purchase_invoice` → `inventory.purchase_receipt`

Exclude fully received rows, quantities already mapped into the target and rows outside the selection. Start with invoiced less already received and mapped. The received field initially takes that remainder. Deduct applicable returned quantity for accepted quantity and multiply the result by the unit factor for stock quantity. Initial line amount uses the pending quantity and invoice rate. Remove zero target rows and recalculate document totals.

| Calculated destination field | Rule after initial copying |
|---|---|
| `inventory.purchase_receipt_item.quantity` | Unreceived and unmapped quantity less applicable returned quantity. |
| `inventory.purchase_receipt_item.received_quantity` | Unreceived and unmapped quantity before deducting the return. |
| `inventory.purchase_receipt_item.stock_quantity` | Accepted quantity × invoice row conversion factor. |
| `inventory.purchase_receipt_item.company_currency_amount` | Unreceived and unmapped quantity × invoice unit rate × invoice exchange rate. |

On purchase invoice, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `accounting.purchase_invoice_item.record_identifier` | `inventory.purchase_receipt_item.purchase_invoice_item` |
| `accounting.purchase_invoice_item.owning_record_identifier` | `inventory.purchase_receipt_item.purchase_invoice_identifier` |
| `accounting.purchase_invoice_item.bill_of_materials_identifier` | `inventory.purchase_receipt_item.bill_of_materials_identifier` |
| `accounting.purchase_invoice_item.purchase_order_identifier` | `inventory.purchase_receipt_item.purchase_order_identifier` |
| `accounting.purchase_invoice_item.purchase_order_line` | `inventory.purchase_receipt_item.purchase_order_item` |
| `accounting.purchase_invoice_item.material_request_identifier` | `inventory.purchase_receipt_item.material_request_identifier` |
| `accounting.purchase_invoice_item.material_request_item` | `inventory.purchase_receipt_item.material_request_item` |
| `accounting.purchase_invoice_item.work_in_progress_composite_asset_identifier` | `inventory.purchase_receipt_item.work_in_progress_composite_asset_identifier` |

## Receive a purchase order

`procurement.purchase_order` → `inventory.purchase_receipt`

Exclude supplier-delivered rows. For ordinary rows compare absolute received and already mapped quantities with absolute ordered quantity. For zero-quantity unit-price rows use prior mapping of that exact row to prevent adding it twice. Calculate pending quantity, extend by the unit conversion factor for stock, and value with the order rate and conversion rate. Retain the material request, sales order and composite-asset links where applicable.

| Calculated destination field | Rule after initial copying |
|---|---|
| `inventory.purchase_receipt_item.stock_quantity` | Remaining receivable purchase quantity × original order row conversion factor. |
| `inventory.purchase_receipt_item.amount` | Remaining receivable purchase quantity × order rate. |
| `inventory.purchase_receipt_item.company_currency_amount` | Remaining receivable purchase quantity × order rate × order exchange rate. |

On purchase order, require lifecycle state equals posted. Purchase taxes and charges rows. Reset destination collection before copying selected source rows.

| Source record and field | Destination record and field |
|---|---|
| `procurement.purchase_order.supplier_warehouse_identifier` | `inventory.purchase_receipt.supplier_warehouse_identifier` |
| `procurement.purchase_order_item.record_identifier` | `inventory.purchase_receipt_item.purchase_order_item` |
| `procurement.purchase_order_item.owning_record_identifier` | `inventory.purchase_receipt_item.purchase_order_identifier` |
| `procurement.purchase_order_item.bill_of_materials_identifier` | `inventory.purchase_receipt_item.bill_of_materials_identifier` |
| `procurement.purchase_order_item.material_request_identifier` | `inventory.purchase_receipt_item.material_request_identifier` |
| `procurement.purchase_order_item.material_request_item` | `inventory.purchase_receipt_item.material_request_item` |
| `procurement.purchase_order_item.sales_order_identifier` | `inventory.purchase_receipt_item.sales_order_identifier` |
| `procurement.purchase_order_item.sales_order_item` | `inventory.purchase_receipt_item.sales_order_item` |
| `procurement.purchase_order_item.work_in_progress_composite_asset_identifier` | `inventory.purchase_receipt_item.work_in_progress_composite_asset_identifier` |

## Bill a purchase order

`procurement.purchase_order` → `accounting.purchase_invoice`

Take outstanding quantity after effective bills and rows already in this target. Allow a row whose quantity has been exhausted but whose billed value is below its order value when it is not already mapped. Unit-price rows can start with zero quantity. Resolve the payable account for the supplier/company and buying cost centre from the row, project, product or product group.

| Calculated destination field | Rule after initial copying |
|---|---|
| `accounting.purchase_invoice_item.quantity` | For an ordinary item, max(ordered − already billed − already mapped into the destination, 0). A price-only row starts at zero. |

On purchase order, require lifecycle state equals posted. Purchase taxes and charges rows. Reset destination collection before copying selected source rows.

| Source record and field | Destination record and field |
|---|---|
| `procurement.purchase_order.party_account_currency_identifier` | `accounting.purchase_invoice.party_account_currency_identifier` |
| `procurement.purchase_order.supplier_warehouse_identifier` | `accounting.purchase_invoice.supplier_warehouse_identifier` |
| `procurement.purchase_order_item.record_identifier` | `accounting.purchase_invoice_item.purchase_order_line` |
| `procurement.purchase_order_item.owning_record_identifier` | `accounting.purchase_invoice_item.purchase_order_identifier` |
| `procurement.purchase_order_item.material_request_identifier` | `accounting.purchase_invoice_item.material_request_identifier` |
| `procurement.purchase_order_item.material_request_item` | `accounting.purchase_invoice_item.material_request_item` |
| `procurement.purchase_order_item.work_in_progress_composite_asset_identifier` | `accounting.purchase_invoice_item.work_in_progress_composite_asset_identifier` |

## Bill a supplier quotation directly

`procurement.supplier_quotation` → `accounting.purchase_invoice`

Create the supplier bill from the submitted quotation and its product rows. Re-evaluate tax row values in the bill's context. This path bypasses receipt and purchase-order progress unless separate linked documents establish those events.

On supplier quotation, require lifecycle state equals posted. Purchase taxes and charges rows. Reset destination collection before copying selected source rows.

## Execute an authorised material request

`inventory.material_request` → `inventory.stock_entry`

Accept transfer, issue or customer-provided requests with open stock quantity. A transfer uses the source and destination, an issue uses the issuing warehouse and customer-provided stock creates a receipt with zero valuation permitted. A work-order or operation-card transfer carries the production purpose and its recipe context.

On material request, require lifecycle state equals posted, material request type one of Material Transfer, Material Issue, Customer Provided.

| Source record and field | Destination record and field |
|---|---|
| `inventory.material_request_item.record_identifier` | `inventory.stock_entry_detail.material_request_item_identifier` |
| `inventory.material_request_item.owning_record_identifier` | `inventory.stock_entry_detail.material_request_identifier` |
| `inventory.material_request_item.unit_of_measure_identifier` | `inventory.stock_entry_detail.stock_unit_of_measure_identifier` |
| `inventory.material_request_item.job_card_item` | `inventory.stock_entry_detail.job_card_item` |

## Pick a material transfer request

`inventory.material_request` → `inventory.pick_list`

Require a submitted transfer request. Map still-unpicked stock quantity at row precision. Use the request's source warehouse as the pick warehouse and retain the request row so another pick can only consume its remaining demand.

On material request, require lifecycle state equals posted, material request type equals Material Transfer.

| Source record and field | Destination record and field |
|---|---|
| `inventory.material_request.material_request_type` | `inventory.pick_list.purpose` |
| `inventory.material_request_item.record_identifier` | `inventory.pick_list_item.material_request_item` |
| `inventory.material_request_item.stock_quantity` | `inventory.pick_list_item.stock_quantity` |
| `inventory.material_request_item.from_warehouse_identifier` | `inventory.pick_list_item.warehouse_identifier` |

## Bill accepted supplier receipts

`inventory.purchase_receipt` → `accounting.purchase_invoice`

Calculate pending billable quantity per received row, accounting for posted bills, returns and any already mapped into the target. Keep original receipt and originating order line, asset and project context. Derive bill stock quantity from bill quantity and conversion factor. Rejected quantity on the bill is cleared.

On purchase receipt, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `inventory.purchase_receipt.supplier_warehouse_identifier` | `accounting.purchase_invoice.supplier_warehouse_identifier` |
| `inventory.purchase_receipt.is_return` | `accounting.purchase_invoice.is_return` |
| `inventory.purchase_receipt_item.record_identifier` | `accounting.purchase_invoice_item.purchase_receipt_line` |
| `inventory.purchase_receipt_item.owning_record_identifier` | `accounting.purchase_invoice_item.purchase_receipt_identifier` |
| `inventory.purchase_receipt_item.quantity` | `accounting.purchase_invoice_item.received_quantity` |
| `inventory.purchase_receipt_item.purchase_order_item` | `accounting.purchase_invoice_item.purchase_order_line` |
| `inventory.purchase_receipt_item.purchase_order_identifier` | `accounting.purchase_invoice_item.purchase_order_identifier` |
| `inventory.purchase_receipt_item.is_fixed_asset` | `accounting.purchase_invoice_item.is_fixed_asset` |
| `inventory.purchase_receipt_item.asset_location_identifier` | `accounting.purchase_invoice_item.asset_location_identifier` |
| `inventory.purchase_receipt_item.asset_category_identifier` | `accounting.purchase_invoice_item.asset_category_identifier` |
| `inventory.purchase_receipt_item.work_in_progress_composite_asset_identifier` | `accounting.purchase_invoice_item.work_in_progress_composite_asset_identifier` |

## Move received goods to another warehouse

`inventory.purchase_receipt` → `inventory.stock_entry`

Create an internal material transfer using the receipt's warehouse as the source and its available tracking selection. Preserve the selected serials or batch. Build an appropriate outward allocation when multiple tracked identities are involved.

| Source record and field | Destination record and field |
|---|---|
| `inventory.purchase_receipt_item.warehouse_identifier` | `inventory.stock_entry_detail.source_warehouse_identifier` |
| `inventory.purchase_receipt_item.owning_record_identifier` | `inventory.stock_entry_detail.reference_purchase_receipt_identifier` |
| `inventory.purchase_receipt_item.batch_number_identifier` | `inventory.stock_entry_detail.batch_number_identifier` |

## Complete the receiving leg of transit stock

`inventory.stock_entry` → `inventory.stock_entry`

Require a submitted transfer to transit. Compute remaining transferred stock quantity at row precision. Divide by the original conversion factor to get receiving units. Set the transit location as the source, the chosen destination as the target, and clear the instruction to place this leg into transit again.

| Calculated destination field | Rule after initial copying |
|---|---|
| `inventory.stock_entry_detail.quantity` | Remaining transferable stock units divided by the original transaction-to-stock unit factor. Skip fully received transit movements. |

On stock entry, require lifecycle state equals posted, purpose equals Material Transfer, add to transit equals 1.

| Source record and field | Destination record and field |
|---|---|
| `inventory.stock_entry.record_identifier` | `inventory.stock_entry.outgoing_stock_entry_identifier` |
| `inventory.stock_entry_detail.record_identifier` | `inventory.stock_entry_detail.ste_detail` |
| `inventory.stock_entry_detail.owning_record_identifier` | `inventory.stock_entry_detail.related_stock_movement_identifier` |
| `inventory.stock_entry_detail.serial_number` | `inventory.stock_entry_detail.serial_number` |
| `inventory.stock_entry_detail.batch_number_identifier` | `inventory.stock_entry_detail.batch_number_identifier` |
| `inventory.stock_entry_detail.target_warehouse_identifier` | `inventory.stock_entry_detail.source_warehouse_identifier` |
