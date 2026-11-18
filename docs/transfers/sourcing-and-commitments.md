# Sourcing and commitments conversions

[Structured field mappings](sourcing-and-commitments.json) · [All conversions](README.md)

## Prepare a supplier response to a request for quotation

`procurement.request_for_quotation` → `procurement.supplier_quotation`

Resolve the responding supplier, use its company-specific account currency unless supplied and apply its buying price list or the buying default. Each offered line retains the request and request-line identity. Portal submission also checks invitee and contact rights before saving a draft.

On request for quotation, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `procurement.request_for_quotation.opportunity_identifier` | `procurement.supplier_quotation.opportunity_identifier` |
| `procurement.request_for_quotation_item.record_identifier` | `procurement.supplier_quotation_item.request_for_quotation_item` |
| `procurement.request_for_quotation_item.owning_record_identifier` | `procurement.supplier_quotation_item.request_for_quotation_identifier` |
| `procurement.request_for_quotation_item.project_name_identifier` | `procurement.supplier_quotation_item.project_identifier` |
| `procurement.request_for_quotation_item.cost_center_identifier` | `procurement.supplier_quotation_item.cost_center_identifier` |

## Invite quotations for a supplier's requested products

`inventory.material_request` → `procurement.request_for_quotation`

Select purchasing requisitions and only product rows included in the supplier item set. Preserve transaction units and the cost centre alongside the original request and row identities.

On material request, require lifecycle state equals posted, material request type equals Purchase.

| Source record and field | Destination record and field |
|---|---|
| `inventory.material_request_item.record_identifier` | `procurement.request_for_quotation_item.material_request_item` |
| `inventory.material_request_item.owning_record_identifier` | `procurement.request_for_quotation_item.material_request_identifier` |
| `inventory.material_request_item.unit_of_measure_identifier` | `procurement.request_for_quotation_item.unit_of_measure_identifier` |
| `inventory.material_request_item.cost_center_identifier` | `procurement.request_for_quotation_item.cost_center_identifier` |

## Order a supplier quotation

`procurement.supplier_quotation` → `procurement.purchase_order`

A selected ordinary row contributes the open quantity remaining to order. A unit-price row with zero quoted quantity can also qualify. Exclude a row already mapped into the target. Cap proposed order quantity below at zero and extend it by the source conversion factor for stock quantity. The purchase order has its own transaction date.

| Calculated destination field | Rule after initial copying |
|---|---|
| `procurement.purchase_order_item.quantity` | Maximum of outstanding quoted quantity and zero. |
| `procurement.purchase_order_item.stock_quantity` | New order quantity × original quotation unit factor. |

On supplier quotation, require lifecycle state equals posted. Purchase taxes and charges rows. Reset destination collection before copying selected source rows.

| Source record and field | Destination record and field |
|---|---|
| `procurement.supplier_quotation_item.record_identifier` | `procurement.purchase_order_item.supplier_quotation_item_identifier` |
| `procurement.supplier_quotation_item.owning_record_identifier` | `procurement.purchase_order_item.supplier_quotation_identifier` |
| `procurement.supplier_quotation_item.material_request_identifier` | `procurement.purchase_order_item.material_request_identifier` |
| `procurement.supplier_quotation_item.material_request_item` | `procurement.purchase_order_item.material_request_item` |
| `procurement.supplier_quotation_item.sales_order_identifier` | `procurement.purchase_order_item.sales_order_identifier` |

## Prepare a customer quotation from supplier prices

`procurement.supplier_quotation` → `sales.quotation`

Keep the supplier quotation as the commercial precursor. When populating an empty destination collection include only products enabled for sale. Remove inapplicable terms as the transaction changes from buying to selling.

Quotation item rows. Only add rows when the destination collection is empty.

| Source record and field | Destination record and field |
|---|---|
| `procurement.supplier_quotation.record_identifier` | `sales.quotation.supplier_quotation_identifier` |

## Open a supplier evaluation period

`procurement.supplier_scorecard` → `procurement.supplier_scorecard_period`

Capture the supplier scorecard's scoring criteria and their effective measurements on the new period. The period must pass its date overlap, total-weight and score checks before a submitted assessment contributes to supplier standing.

## Source an opportunity through supplier enquiries

`sales_relationships.opportunity` → `procurement.request_for_quotation`

Calculate the requested product’s unit factor for the enquiry. Keep source context when allocating enquiry lines. Treat additional source-row fields as durable only where present on the saved destination.

| Source record and field | Destination record and field |
|---|---|
| `sales_relationships.opportunity_item.unit_of_measure_identifier` | `procurement.request_for_quotation_item.unit_of_measure_identifier` |

## Prepare a supplier offer from an opportunity

`sales_relationships.opportunity` → `procurement.supplier_quotation`

Connect the supplier offer to the opportunity. The explicitly selected opportunity item unit enters the supplier quotation's stock-unit field. The buyer must still select the supplier and validate the resulting offer.

| Source record and field | Destination record and field |
|---|---|
| `sales_relationships.opportunity.record_identifier` | `procurement.supplier_quotation.opportunity_identifier` |
| `sales_relationships.opportunity_item.unit_of_measure_identifier` | `procurement.supplier_quotation_item.stock_unit_of_measure_identifier` |

## Request supply against sales order lines

`sales.sales_order` → `inventory.material_request`

For ordinary rows subtract requested stock quantity converted to order units and positive delivered quantity. For bundle components subtract requests against the packed row and the positive delivered parent quantity scaled by components per unit. Keep the component identity. Refresh physical stock and price for the destination and remove commercial terms inappropriate to a requisition.

On sales order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `inventory.packed_item.owning_record_identifier` | `inventory.material_request_item.sales_order_identifier` |
| `inventory.packed_item.unit_of_measure_identifier` | `inventory.material_request_item.stock_unit_of_measure_identifier` |
| `inventory.packed_item.record_identifier` | `inventory.material_request_item.packed_item` |
| `sales.sales_order_item.record_identifier` | `inventory.material_request_item.sales_order_item` |
| `sales.sales_order_item.owning_record_identifier` | `inventory.material_request_item.sales_order_identifier` |
| `sales.sales_order_item.delivery_date` | `inventory.material_request_item.schedule_date` |
| `sales.sales_order_item.bill_of_materials_number_identifier` | `inventory.material_request_item.bill_of_materials_number_identifier` |
| `sales.sales_order.project_identifier` | `inventory.material_request_item.project_identifier` |

## Procure outstanding sales-order demand

`sales.sales_order` → `procurement.purchase_order`

Use the selected supplier's buying currency and an appropriate buying exchange rate. For ordinary rows use their remaining ordering quantities, and for bundle rows use the component still to order. Clear sales discounts, shipping terms and inherited payment schedules. Supplier drop-ship contact and location data apply only to the eligible branch.

On sales order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `sales.sales_order_item.record_identifier` | `procurement.purchase_order_item.sales_order_item` |
| `sales.sales_order_item.owning_record_identifier` | `procurement.purchase_order_item.sales_order_identifier` |
| `sales.sales_order_item.stock_unit_of_measure_identifier` | `procurement.purchase_order_item.stock_unit_of_measure_identifier` |
| `sales.sales_order_item.unit_of_measure_identifier` | `procurement.purchase_order_item.unit_of_measure_identifier` |
| `sales.sales_order_item.unit_conversion_factor` | `procurement.purchase_order_item.unit_conversion_factor` |
| `sales.sales_order_item.delivery_date` | `procurement.purchase_order_item.schedule_date` |
| `inventory.packed_item.record_identifier` | `procurement.purchase_order_item.sales_order_packed_item` |
| `inventory.packed_item.owning_record_identifier` | `procurement.purchase_order_item.sales_order_identifier` |
| `inventory.packed_item.unit_of_measure_identifier` | `procurement.purchase_order_item.unit_of_measure_identifier` |
| `inventory.packed_item.unit_conversion_factor` | `procurement.purchase_order_item.unit_conversion_factor` |
| `inventory.packed_item.parent_item_identifier` | `procurement.purchase_order_item.product_bundle_identifier` |
| `inventory.packed_item.rate` | `procurement.purchase_order_item.rate` |

## Purchase materials requested by a business unit

`inventory.material_request` → `procurement.purchase_order`

Require a purchasing or subcontracting request. Select rows whose ordered stock remains below required stock. Supplier and selection filters narrow the eligible set. For subcontracting map the requested item and quantity as finished goods, while ordinary purchasing takes the transaction and stock units. Re-resolve buying prices on the destination.

On material request, require lifecycle state equals posted, material request type one of Purchase, Subcontracting.

| Source record and field | Destination record and field |
|---|---|
| `inventory.material_request_item.record_identifier` | `procurement.purchase_order_item.material_request_item` |
| `inventory.material_request_item.owning_record_identifier` | `procurement.purchase_order_item.material_request_identifier` |
| `inventory.material_request_item.sales_order_identifier` | `procurement.purchase_order_item.sales_order_identifier` |
| `inventory.material_request_item.sales_order_item` | `procurement.purchase_order_item.sales_order_item` |
| `inventory.material_request_item.work_in_progress_composite_asset_identifier` | `procurement.purchase_order_item.work_in_progress_composite_asset_identifier` |

## Seek prices for a purchase requisition

`inventory.material_request` → `procurement.request_for_quotation`

Accept a submitted purchase request. Derive requested transaction units as remaining unordered stock units divided by the target conversion factor. Carry the project, cost centre and source row so that supplier quotations can trace back to the demand.

| Calculated destination field | Rule after initial copying |
|---|---|
| `procurement.request_for_quotation_item.quantity` | Requested stock units less ordered stock units, divided by the destination conversion factor. |
| `procurement.request_for_quotation_item.stock_quantity` | Enquiry quantity × destination conversion factor. |

On material request, require lifecycle state equals posted, material request type equals Purchase.

| Source record and field | Destination record and field |
|---|---|
| `inventory.material_request_item.record_identifier` | `procurement.request_for_quotation_item.material_request_item` |
| `inventory.material_request_item.owning_record_identifier` | `procurement.request_for_quotation_item.material_request_identifier` |
| `inventory.material_request_item.project_identifier` | `procurement.request_for_quotation_item.project_name_identifier` |
| `inventory.material_request_item.cost_center_identifier` | `procurement.request_for_quotation_item.cost_center_identifier` |

## Build a purchase order for a chosen supplier

`inventory.material_request` → `procurement.purchase_order`

Select eligible requests/items for that supplier and open lines whose ordered quantity is below the request quantity. Set the chosen supplier on the target and resolve delivery dates from its lines.

| Source record and field | Destination record and field |
|---|---|
| `inventory.material_request_item.record_identifier` | `procurement.purchase_order_item.material_request_item` |
| `inventory.material_request_item.owning_record_identifier` | `procurement.purchase_order_item.material_request_identifier` |
| `inventory.material_request_item.unit_of_measure_identifier` | `procurement.purchase_order_item.stock_unit_of_measure_identifier` |
| `inventory.material_request_item.unit_of_measure_identifier` | `procurement.purchase_order_item.unit_of_measure_identifier` |

## Create a supplier offer for requested goods

`inventory.material_request` → `procurement.supplier_quotation`

Accept a submitted purchase request and rows whose ordered or received progress is below requested stock quantity. Keep the original demand and any originating sales order available for comparison.

On material request, require lifecycle state equals posted, material request type equals Purchase.

| Source record and field | Destination record and field |
|---|---|
| `inventory.material_request_item.record_identifier` | `procurement.supplier_quotation_item.material_request_item` |
| `inventory.material_request_item.owning_record_identifier` | `procurement.supplier_quotation_item.material_request_identifier` |
| `inventory.material_request_item.sales_order_identifier` | `procurement.supplier_quotation_item.sales_order_identifier` |

## Draw against a blanket agreement for sales order

`manufacturing.blanket_order` → `sales.sales_order`

A selling agreement can produce a customer quotation or sales order. A purchasing agreement can produce a purchase order. Accept a zero-quantity price agreement or a row with a positive remaining quantity. Propose max(agreed less ordered, zero), attach the agreed rate and resolve current product units and descriptions. A customer quotation identifies the agreement customer as its party.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.blanket_order_item.rate` | `sales.sales_order_item.blanket_order_rate` |
| `manufacturing.blanket_order_item.owning_record_identifier` | `sales.sales_order_item.blanket_order_identifier` |

## Draw against a blanket agreement for purchase order

`manufacturing.blanket_order` → `procurement.purchase_order`

A selling agreement can produce a customer quotation or sales order. A purchasing agreement can produce a purchase order. Accept a zero-quantity price agreement or a row with a positive remaining quantity. Propose max(agreed less ordered, zero), attach the agreed rate and resolve current product units and descriptions. A customer quotation identifies the agreement customer as its party.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.blanket_order_item.rate` | `procurement.purchase_order_item.blanket_order_rate` |
| `manufacturing.blanket_order_item.owning_record_identifier` | `procurement.purchase_order_item.blanket_order_identifier` |

## Draw against a blanket agreement for quotation

`manufacturing.blanket_order` → `sales.quotation`

A selling agreement can produce a customer quotation or sales order. A purchasing agreement can produce a purchase order. Accept a zero-quantity price agreement or a row with a positive remaining quantity. Propose max(agreed less ordered, zero), attach the agreed rate and resolve current product units and descriptions. A customer quotation identifies the agreement customer as its party.

| Source record and field | Destination record and field |
|---|---|
| `manufacturing.blanket_order_item.rate` | `sales.quotation_item.blanket_order_rate` |
| `manufacturing.blanket_order_item.owning_record_identifier` | `sales.quotation_item.blanket_order_identifier` |
