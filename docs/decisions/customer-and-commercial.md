# Customers, purchasing and commercial commitments

Customer and supplier decisions span the offer, order, issued document, installed item and commercial agreement. Match the proposed action to its own record lifecycle.

## Quotation

Logical record `sales.quotation`. [Field definitions and declared grants](../../schema/entities/sales.json)

| Operation | Refuse when |
|---|---|
| Validate quotation dates | A supplied validity end precedes the quotation date. The same date is within the validity interval. |
| Declare an offer lost | The quotation has not been submitted. |
| Declare an offer lost | The quotation has already generated a partial or complete order. |
| Record a lost offer with no orders | No loss reason was supplied. |

## Proforma invoice

Logical record `sales.proforma_invoice`. [Field definitions and declared grants](../../schema/entities/sales.json)

| Operation | Refuse when |
|---|---|
| Issue a pro forma | The linked sales order is outside the submitted lifecycle. |
| Attach pro forma rows | The selected order line is already present on another row. Two distinct lines containing the same product remain distinguishable. |
| Attach a quoted amount or quantity | The selected line cannot be found among the lines of the nominated order. |
| Confirm a pro forma quantity | Requested quantity is zero or negative. |
| Confirm an amount-based pro forma | The line amount is zero or negative. |
| Email a pro forma | The document has not been issued. |

## Product bundle

Logical record `sales.product_bundle`. [Field definitions and declared grants](../../schema/entities/sales.json)

| Operation | Refuse when |
|---|---|
| Define the sellable bundle | Its parent is itself an inventory-tracked product. The component lines carry the physical quantities. |
| Define the sellable bundle | Its parent is a fixed asset. |
| Attach a bundle component | The component is the same product as the bundle parent. |
| Attach a bundle component | An enabled bundle already uses the component as its parent. |
| Save bundle composition | A component quantity is zero or negative. |

## Installation note

Logical record `sales.installation_note`. [Field definitions and declared grants](../../schema/entities/sales.json)

| Operation | Refuse when |
|---|---|
| Record an installation | The referenced delivery line is missing or its delivery has not been submitted. |
| Validate installation lineage | The line belongs to a delivery document different from the delivery named on the installation row. |
| Install a serial-tracked unit | Its serial identifier is absent from the serials on the selected delivery. |
| Date the installed unit | The installation date precedes its referenced delivery date. |

## Supplier quotation

Logical record `procurement.supplier_quotation`. [Field definitions and declared grants](../../schema/entities/procurement.json)

| Operation | Refuse when |
|---|---|
| Set supplier offer validity | A supplied end date precedes the transaction date. |
| Order against a supplier offer | The supplier quotation has expired. |

## Supplier

Logical record `procurement.supplier`. [Field definitions and declared grants](../../schema/entities/procurement.json)

| Operation | Refuse when |
|---|---|
| Classify a supplier | The selected supplier group is an internal hierarchy node. Select a leaf group. |
| Set a supplier’s primary contact or address | The proposed record lacks an association to that supplier. |

## Request for quotation

Logical record `procurement.request_for_quotation`. [Field definitions and declared grants](../../schema/entities/procurement.json)

| Operation | Refuse when |
|---|---|
| Prepare a supplier quotation from an invitation | A selected source line is not among the invitation’s rows. |

## Contract

Logical record `sales_relationships.contract`. [Field definitions and declared grants](../../schema/entities/sales-relationships.json)

| Operation | Refuse when |
|---|---|
| Set a contract interval | Both dates exist and the end precedes the start. |
| Mark a contract signed | Either the signatory or the signature date is missing. |
| Associate a contract with another document | For a linked document on a nonemployee contract, the party resolved for that role differs from the contract party. |

## Email campaign

Logical record `sales_relationships.email_campaign`. [Field definitions and declared grants](../../schema/entities/sales-relationships.json)

| Operation | Refuse when |
|---|---|
| Start a new campaign enrolment | The identified recipient has unsubscribed. |
| Change a campaign start | The changed date is earlier than the current business date. |
| Target a lead in an email campaign | The lead has no email address. |
