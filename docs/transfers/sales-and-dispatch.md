# Sales and dispatch conversions

[Structured field mappings](sales-and-dispatch.json) · [All conversions](README.md)

## Dispatch stock from a customer invoice

`accounting.sales_invoice` → `inventory.delivery_note`

Select rows with invoiced quantity above delivered quantity. Exclude supplier-delivered rows, inward-subcontract rows and rows already referring to a delivery line. Calculate remaining stock units as remaining invoice units times conversion factor. Calculate transaction and company amounts with their respective rates.

| Calculated destination field | Rule after initial copying |
|---|---|
| `inventory.delivery_note_item.quantity` | Invoiced quantity less delivered quantity. |
| `inventory.delivery_note_item.stock_quantity` | Remaining invoice quantity × invoice row conversion factor. |
| `inventory.delivery_note_item.company_currency_amount` | Remaining invoice quantity × company-currency invoice unit rate. |

On sales invoice, require lifecycle state equals posted. Sales taxes and charges rows. Reset destination collection before copying selected source rows. Sales team rows. Only add rows when the destination collection is empty.

| Source record and field | Destination record and field |
|---|---|
| `accounting.sales_invoice_item.record_identifier` | `inventory.delivery_note_item.sales_invoice_line` |
| `accounting.sales_invoice_item.owning_record_identifier` | `inventory.delivery_note_item.against_sales_invoice_identifier` |
| `accounting.sales_invoice_item.serial_number` | `inventory.delivery_note_item.serial_number` |
| `accounting.sales_invoice_item.sales_order_identifier` | `inventory.delivery_note_item.against_sales_order_identifier` |
| `accounting.sales_invoice_item.sales_order_line` | `inventory.delivery_note_item.sales_order_line` |
| `accounting.sales_invoice_item.cost_center_identifier` | `inventory.delivery_note_item.cost_center_identifier` |
| `sales.sales_team.incentives` | `sales.sales_team.incentives` |

## Commit a customer quotation to an order

`sales.quotation` → `sales.sales_order`

Resolve the customer for the quotation party. Exclude unselected alternatives by default and honour explicit row selection. The permitted open quantity and any unit-price-only lines determine order rows. Recalculate stock units and retain applicable blanket price terms, sales partner and commission context.

On quotation, require lifecycle state equals posted. Sales taxes and charges rows. Reset destination collection before copying selected source rows. Sales team rows. Only add rows when the destination collection is empty.

| Source record and field | Destination record and field |
|---|---|
| `sales.quotation_item.owning_record_identifier` | `sales.sales_order_item.prevdoc_record_identifier` |
| `sales.quotation_item.record_identifier` | `sales.sales_order_item.quotation_item` |

## Bill a customer quotation directly

`sales.quotation` → `accounting.sales_invoice`

Resolve the customer and map selected ordinary product rows. Alternative quotation rows are excluded. Calculate stock-unit quantity as quoted quantity times its conversion factor. Currency, tax and billing rules belong to the invoice.

On quotation, require lifecycle state equals posted. Sales taxes and charges rows. Reset destination collection before copying selected source rows. Sales team rows. Only add rows when the destination collection is empty.

## Dispatch a customer order

`sales.sales_order` → `inventory.delivery_note`

Exclude supplier-delivered and otherwise ineligible rows. Subtract delivered quantity and quantities already mapped into the current draft. Unit-price-only rows use a row-identity guard. Where physical reservations govern fulfilment, split the source row by its reserved warehouse and convert reserved stock units back to delivery units.

| Calculated destination field | Rule after initial copying |
|---|---|
| `inventory.delivery_note_item.quantity` | For an ordinary line, ordered quantity less delivered quantity less units already mapped from the same source row into the destination. |
| `inventory.delivery_note_item.company_currency_amount` | Remaining units × order row company-currency rate. For a reservation-specific split, re-evaluate the split quantity in its transaction unit. |

On sales order, require lifecycle state equals posted. Sales taxes and charges rows. Reset destination collection before copying selected source rows. Sales team rows. Only add rows when the destination collection is empty.

| Source record and field | Destination record and field |
|---|---|
| `sales.sales_order_item.rate` | `inventory.delivery_note_item.rate` |
| `sales.sales_order_item.record_identifier` | `inventory.delivery_note_item.sales_order_line` |
| `sales.sales_order_item.owning_record_identifier` | `inventory.delivery_note_item.against_sales_order_identifier` |

## Bill a customer order

`sales.sales_order` → `accounting.sales_invoice`

Use the order line's effective returns, delivered units, invoiced quantity, currently mapped quantity and amount tolerance. A quantity-complete but monetarily underbilled row may qualify. Resolve the customer's receivable account, deferred revenue applicability and cost centre. Preserve the difference between a unit-price-only row and a fully billed ordinary row.

| Calculated destination field | Rule after initial copying |
|---|---|
| `accounting.sales_invoice_item.company_currency_amount` | Proposed billable transaction amount × source order exchange rate. |
| `accounting.sales_invoice_item.amount` | When billing by outstanding value, original row amount less effective billed amount. |

On sales order, require lifecycle state equals posted. Sales taxes and charges rows. Reset destination collection before copying selected source rows. Sales team rows. Only add rows when the destination collection is empty.

| Source record and field | Destination record and field |
|---|---|
| `sales.sales_order.party_account_currency_identifier` | `accounting.sales_invoice.party_account_currency_identifier` |
| `sales.sales_order_item.record_identifier` | `accounting.sales_invoice_item.sales_order_line` |
| `sales.sales_order_item.owning_record_identifier` | `accounting.sales_invoice_item.sales_order_identifier` |

## Pick against a customer order

`sales.sales_order` → `inventory.pick_list`

Prepare a delivery pick from still-open items and component rows. Use transaction-to-stock conversion. Preserve the original order line and each packed component occurrence to calculate complete bundle quantities even when component identities repeat.

On sales order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `sales.sales_order.default_warehouse_identifier` | `inventory.pick_list.parent_warehouse_identifier` |
| `sales.sales_order_item.owning_record_identifier` | `inventory.pick_list_item.sales_order_identifier` |
| `sales.sales_order_item.record_identifier` | `inventory.pick_list_item.sales_order_item` |
| `inventory.packed_item.owning_record_identifier` | `inventory.pick_list_item.sales_order_identifier` |
| `inventory.packed_item.parent_detail_record_identifier` | `inventory.pick_list_item.sales_order_item` |
| `inventory.packed_item.record_identifier` | `inventory.pick_list_item.product_bundle_item` |

## Bill a customer delivery

`inventory.delivery_note` → `accounting.sales_invoice`

Select still-billable rows with their delivery and sales-order identities. Allow a zero-price or value-completion branch where applicable. Deduct effective returns and already billed or mapped quantities. The invoice extends the billable quantity at the document and company currency rates.

On delivery note, require lifecycle state equals posted. Sales team rows. Only add rows when the destination collection is empty.

| Source record and field | Destination record and field |
|---|---|
| `inventory.delivery_note.is_return` | `accounting.sales_invoice.is_return` |
| `inventory.delivery_note_item.record_identifier` | `accounting.sales_invoice_item.delivery_note_line` |
| `inventory.delivery_note_item.owning_record_identifier` | `accounting.sales_invoice_item.delivery_note_identifier` |
| `inventory.delivery_note_item.sales_order_line` | `accounting.sales_invoice_item.sales_order_line` |
| `inventory.delivery_note_item.against_sales_order_identifier` | `accounting.sales_invoice_item.sales_order_identifier` |
| `inventory.delivery_note_item.cost_center_identifier` | `accounting.sales_invoice_item.cost_center_identifier` |
| `sales.sales_team.incentives` | `sales.sales_team.incentives` |

## Attach a delivery to a trip stop

`inventory.delivery_note` → `inventory.delivery_trip`

Create or extend a delivery trip by adding a stop. A draft delivery is eligible for planning and a cancelled delivery is refused. The stop uses the shipping address in preference to the customer address. Submitting the trip requires its linked deliveries to be submitted.

| Source record and field | Destination record and field |
|---|---|
| `inventory.delivery_note.record_identifier` | `inventory.delivery_stop.delivery_note_identifier` |
| `inventory.delivery_note.contact_person_identifier` | `inventory.delivery_stop.contact_identifier` |
| `inventory.delivery_note.contact_display` | `inventory.delivery_stop.customer_contact` |
| `inventory.delivery_note.company_identifier` | `inventory.delivery_trip.company_identifier` |

## Pack a draft delivery

`inventory.delivery_note` → `inventory.packing_slip`

Require a draft delivery. For ordinary items use delivery quantity less already packed. Where a bundle is active use packed component rows as the source. An active bundle parent is excluded from ordinary packing. Track each delivery or packed row separately for cumulative packing and cancellation.

| Calculated destination field | Rule after initial copying |
|---|---|
| `inventory.packing_slip_item.quantity` | Ordinary row quantity less packed quantity, or the packable component remainder for a product bundle. |

On delivery note, require lifecycle state equals draft.

| Source record and field | Destination record and field |
|---|---|
| `inventory.delivery_note.record_identifier` | `inventory.packing_slip.delivery_note_identifier` |
| `inventory.delivery_note.letter_head_identifier` | `inventory.packing_slip.letter_head_identifier` |
| `inventory.delivery_note_item.item_identifier` | `inventory.packing_slip_item.item_identifier` |
| `inventory.delivery_note_item.item_name` | `inventory.packing_slip_item.item_name` |
| `inventory.delivery_note_item.batch_number_identifier` | `inventory.packing_slip_item.batch_number_identifier` |
| `inventory.delivery_note_item.description` | `inventory.packing_slip_item.description` |
| `inventory.delivery_note_item.quantity` | `inventory.packing_slip_item.quantity` |
| `inventory.delivery_note_item.unit_of_measure_identifier` | `inventory.packing_slip_item.stock_unit_of_measure_identifier` |
| `inventory.delivery_note_item.record_identifier` | `inventory.packing_slip_item.delivery_note_line` |
| `inventory.packed_item.item_identifier` | `inventory.packing_slip_item.item_identifier` |
| `inventory.packed_item.item_name` | `inventory.packing_slip_item.item_name` |
| `inventory.packed_item.batch_number_identifier` | `inventory.packing_slip_item.batch_number_identifier` |
| `inventory.packed_item.description` | `inventory.packing_slip_item.description` |
| `inventory.packed_item.quantity` | `inventory.packing_slip_item.quantity` |
| `inventory.packed_item.record_identifier` | `inventory.packing_slip_item.delivery_note_packed_item_identifier` |

## Prepare a carrier shipment from a delivery

`inventory.delivery_note` → `inventory.shipment`

Append the delivery to the shipment. Use the dispatching company and selected sender contact at pickup. Prefer the delivery's shipping address for destination, falling back to the customer address. Carrier booking, label issuance and physical delivery are separate events.

On delivery note, require lifecycle state equals posted, is return equals 0.

| Source record and field | Destination record and field |
|---|---|
| `inventory.delivery_note.grand_total` | `inventory.shipment.value_of_goods` |
| `inventory.delivery_note.company_identifier` | `inventory.shipment.pickup_company_identifier` |
| `inventory.delivery_note.company_address_identifier` | `inventory.shipment.pickup_address_name_identifier` |
| `inventory.delivery_note.company_address_display` | `inventory.shipment.pickup_address` |
| `inventory.delivery_note.customer_identifier` | `inventory.shipment.delivery_customer_identifier` |
| `inventory.delivery_note.contact_person_identifier` | `inventory.shipment.delivery_contact_name_identifier` |
| `inventory.delivery_note.contact_email` | `inventory.shipment.delivery_contact_email` |
| `inventory.delivery_note.record_identifier` | `inventory.shipment_delivery_note.delivery_note_identifier` |
