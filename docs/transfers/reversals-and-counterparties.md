# Reversals and counterparties conversions

[Structured field mappings](reversals-and-counterparties.json) · [All conversions](README.md)

## Create an order or invoice in the trading company from sales order

`sales.sales_order` → `procurement.purchase_order`

Resolve the receiving company and its internal customer or supplier. Change party and tax context, re-resolve exchange rates and carry only eligible remaining units. Preserve the counterpart document and appropriate source line identifiers. Receiving an internal sales order creates a purchase order, while receiving an internal supplier-side order creates a sales order. The equivalent invoice directions use receivables and payables respectively.

On sales order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `sales.sales_order_item.rate` | `procurement.purchase_order_item.rate` |
| `sales.sales_order_item.record_identifier` | `procurement.purchase_order_item.sales_order_item` |

## Create an order or invoice in the trading company from purchase order

`procurement.purchase_order` → `sales.sales_order`

Resolve the receiving company and its internal customer or supplier. Change party and tax context, re-resolve exchange rates and carry only eligible remaining units. Preserve the counterpart document and appropriate source line identifiers. Receiving an internal sales order creates a purchase order, while receiving an internal supplier-side order creates a sales order. The equivalent invoice directions use receivables and payables respectively.

On purchase order, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `procurement.purchase_order_item.rate` | `sales.sales_order_item.rate` |
| `procurement.purchase_order_item.owning_record_identifier` | `sales.sales_order_item.purchase_order_identifier` |
| `procurement.purchase_order_item.record_identifier` | `sales.sales_order_item.purchase_order_item` |

## Create an order or invoice in the trading company from sales invoice

`accounting.sales_invoice` → `accounting.purchase_invoice`

Resolve the receiving company and its internal customer or supplier. Change party and tax context, re-resolve exchange rates and carry only eligible remaining units. Preserve the counterpart document and appropriate source line identifiers. Receiving an internal sales order creates a purchase order, while receiving an internal supplier-side order creates a sales order. The equivalent invoice directions use receivables and payables respectively.

On sales invoice, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `accounting.sales_invoice_item.rate` | `accounting.purchase_invoice_item.rate` |
| `accounting.sales_invoice_item.record_identifier` | `accounting.purchase_invoice_item.sales_invoice_item` |

## Create an order or invoice in the trading company from purchase invoice

`accounting.purchase_invoice` → `accounting.sales_invoice`

Resolve the receiving company and its internal customer or supplier. Change party and tax context, re-resolve exchange rates and carry only eligible remaining units. Preserve the counterpart document and appropriate source line identifiers. Receiving an internal sales order creates a purchase order, while receiving an internal supplier-side order creates a sales order. The equivalent invoice directions use receivables and payables respectively.

On purchase invoice, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `accounting.purchase_invoice_item.rate` | `accounting.sales_invoice_item.rate` |

## Create the counterpart receipt or delivery from delivery note

`inventory.delivery_note` → `inventory.purchase_receipt`

A submitted delivery can supply an intercompany goods receipt and a submitted goods receipt can supply the corresponding delivery. Resolve counterpart company and internal party. Deduct quantities already received or effectively returned under the applicable direction. Each company's stock and accounting events retain separate source documents.

On delivery note, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `inventory.delivery_note_item.target_warehouse_identifier` | `inventory.purchase_receipt_item.from_warehouse_identifier` |
| `inventory.delivery_note_item.record_identifier` | `inventory.purchase_receipt_item.delivery_note_item` |

## Create the counterpart receipt or delivery from purchase receipt

`inventory.purchase_receipt` → `inventory.delivery_note`

A submitted delivery can supply an intercompany goods receipt and a submitted goods receipt can supply the corresponding delivery. Resolve counterpart company and internal party. Deduct quantities already received or effectively returned under the applicable direction. Each company's stock and accounting events retain separate source documents.

On purchase receipt, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `inventory.purchase_receipt_item.from_warehouse_identifier` | `inventory.delivery_note_item.target_warehouse_identifier` |

## Return against an issued transaction for sales invoice

`accounting.sales_invoice` → `accounting.sales_invoice`

Create a customer credit against the original sales invoice. Use negative remaining quantity and stock quantity after effective returns, retain the original sales-order, delivery and invoice line, and remove original advances. For a point-of-sale transaction deduct each tender’s share of change before reversing its net amount. Reject a consolidated point-of-sale invoice as the source of this operation.

On sales invoice, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `accounting.sales_invoice.record_identifier` | `accounting.sales_invoice.return_against_identifier` |
| `accounting.sales_invoice_item.serial_number` | `accounting.sales_invoice_item.serial_number` |
| `accounting.sales_invoice_item.batch_number_identifier` | `accounting.sales_invoice_item.batch_number_identifier` |
| `accounting.sales_invoice_item.record_identifier` | `accounting.sales_invoice_item.sales_invoice_item` |
| `inventory.packed_item.parent_detail_record_identifier` | `inventory.packed_item.parent_detail_record_identifier` |
| `inventory.packed_item.record_identifier` | `inventory.packed_item.return_against_packed_item` |

## Return against an issued transaction for point-of-sale invoice

`accounting.point_of_sale_invoice` → `accounting.point_of_sale_invoice`

Retain the original point-of-sale invoice line and refund only previously retained tender after its share of change. Negate fixed tax charges. Restrict explicit serial selections to units still returnable.

On point of sale invoice, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `accounting.point_of_sale_invoice.record_identifier` | `accounting.point_of_sale_invoice.return_against_identifier` |
| `accounting.point_of_sale_invoice_item.serial_number` | `accounting.point_of_sale_invoice_item.serial_number` |
| `accounting.point_of_sale_invoice_item.batch_number_identifier` | `accounting.point_of_sale_invoice_item.batch_number_identifier` |
| `accounting.point_of_sale_invoice_item.record_identifier` | `accounting.point_of_sale_invoice_item.point_of_sale_invoice_item` |
| `inventory.packed_item.parent_detail_record_identifier` | `inventory.packed_item.parent_detail_record_identifier` |
| `inventory.packed_item.record_identifier` | `inventory.packed_item.return_against_packed_item` |

## Return against an issued transaction for purchase invoice

`accounting.purchase_invoice` → `accounting.purchase_invoice`

Create the supplier-side debit note against the original invoice. Derive negative remaining received, rejected, accepted and stock quantities separately. Preserve original purchase order and receipt links, withholding selection and the original supplier invoice row. Clear inherited advances.

On purchase invoice, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `accounting.purchase_invoice.record_identifier` | `accounting.purchase_invoice.return_against_identifier` |
| `accounting.purchase_invoice_item.serial_number` | `accounting.purchase_invoice_item.serial_number` |
| `accounting.purchase_invoice_item.batch_number_identifier` | `accounting.purchase_invoice_item.batch_number_identifier` |
| `accounting.purchase_invoice_item.record_identifier` | `accounting.purchase_invoice_item.purchase_invoice_item` |

## Return against an issued transaction for delivery note

`inventory.delivery_note` → `inventory.delivery_note`

Restore returned goods using the negative remainder of delivered transaction and stock units, after effective prior returns. Retain order and billing line context. Prefer the company’s designated sales-return warehouse when configured. Keep packed component identities tied to their original occurrence.

On delivery note, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `inventory.delivery_note.record_identifier` | `inventory.delivery_note.return_against_identifier` |
| `inventory.delivery_note_item.serial_number` | `inventory.delivery_note_item.serial_number` |
| `inventory.delivery_note_item.batch_number_identifier` | `inventory.delivery_note_item.batch_number_identifier` |
| `inventory.delivery_note_item.record_identifier` | `inventory.delivery_note_item.delivery_note_line` |
| `inventory.packed_item.parent_detail_record_identifier` | `inventory.packed_item.parent_detail_record_identifier` |
| `inventory.packed_item.record_identifier` | `inventory.packed_item.return_against_packed_item` |

## Return against an issued transaction for purchase receipt

`inventory.purchase_receipt` → `inventory.purchase_receipt`

Return the remaining accepted stock against its original receipt row, supplier and warehouse. For the rejected-warehouse action take only remaining rejected stock, use the rejection warehouse as the issue location, clear the separate rejected quantity and tie the return to that disposition.

On purchase receipt, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `inventory.purchase_receipt.record_identifier` | `inventory.purchase_receipt.return_against_identifier` |
| `inventory.purchase_receipt_item.serial_number` | `inventory.purchase_receipt_item.serial_number` |
| `inventory.purchase_receipt_item.batch_number_identifier` | `inventory.purchase_receipt_item.batch_number_identifier` |
| `inventory.purchase_receipt_item.record_identifier` | `inventory.purchase_receipt_item.purchase_receipt_item` |

## Return against an issued transaction for subcontracting receipt

`subcontracting.subcontracting_receipt` → `subcontracting.subcontracting_receipt`

Return output against the original subcontracting receipt line. Preserve the subcontract order row and set process loss to zero. An accepted-output return and a rejected-warehouse return use different eligible quantities. The rejected branch uses only remaining rejected stock at the rejection warehouse.

On subcontracting receipt, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `subcontracting.subcontracting_receipt.record_identifier` | `subcontracting.subcontracting_receipt.return_against_identifier` |
| `subcontracting.subcontracting_receipt_item.serial_number` | `subcontracting.subcontracting_receipt_item.serial_number` |
| `subcontracting.subcontracting_receipt_item.batch_number_identifier` | `subcontracting.subcontracting_receipt_item.batch_number_identifier` |
| `subcontracting.subcontracting_receipt_item.record_identifier` | `subcontracting.subcontracting_receipt_item.subcontracting_receipt_item` |
