# Procurement and fulfilment

## Domain responsibility

Commercial commitments, physical receipt or dispatch, supplier or customer invoices, stock reservations and settlement are distinct records with linked row identities. An order expresses a commitment and updates planning quantities. A receipt or delivery changes stock. An invoice records the financial claim and can additionally perform the stock movement when its stock-update option is enabled. A payment settles a claim. The implementation must support partial performance and preserve the exact upstream row for each downstream quantity and amount.

Use the companion [inventory and valuation](inventory-and-valuation.md), [products, units and packaging](products-units-and-packaging.md), and [transaction progress and row closure](transaction-progress-and-row-closure.md) specifications for the arithmetic they own. Pricing, taxes, approval exposure and credit control are accounting contracts invoked during this workflow, not alternative calculations to be reinvented here.

## Quotation and conversion to an order

A quotation can address an existing customer or another supported commercial party that is resolved to a customer during conversion. It records company, transaction date, validity end date, quoted products and units, price and tax context, optional alternatives and source opportunity references. The validity end cannot precede the quotation date. A setting controls whether expired quotations can still generate orders. When the setting disallows it, a validity end before the current date prevents conversion.

Quotations support alternatives: an alternative product is not simply another mandatory line in the total requirement. Without selections, mapping takes ordinary non-alternative rows. With selected alternatives, alternative groups map only the selected eligible rows; ordinary independent rows remain eligible. Quantity already ordered is tracked in stock units. Quantity already mapped into the in-progress target is also subtracted, preventing duplicate allocation when combining documents into one draft.

Remaining ordered stock quantity is quoted stock quantity minus already ordered stock quantity minus stock quantity already mapped into the current target, clamped to zero. Target transaction quantity is this remainder divided by the original conversion factor. Zero-quantity unit-price rows have a separate setting-controlled path because they quote an uncertain future quantity. They must not be silently removed by a generic positive-quantity filter. Quotation state becomes Open, Partially Ordered or Ordered by comparing applicable rows with submitted order rows; unselected alternatives do not keep a fulfilled quotation artificially incomplete.

Evidence: source-artifact-cccc40bf3c9d3167fd05 lines 139–235; source-artifact-3e85e2f3fd51c063d2fe lines 15–146.

## Sales order contract and fulfilment demand

A sales order references the original quotation row where applicable. Referenced company, product, selected unit and conversion factor must agree. A setting can require the sales rate to remain equal to the referenced rate. Submitting the order checks credit exposure and approving authority, updates stock planning reservations, linked quotation and opportunity status, project information, blanket order usage and configured coupon usage, and creates explicit stock reservations when enabled. These are separate effects; merely writing a header state is insufficient.

Supplier-direct delivery requires a supplier on the row. It must not generate a normal company warehouse dispatch for the same quantity. A non-stock service may skip delivery when configured. Stock items, fixed assets and product bundles containing stocked components require delivery. An order that has no deliverable rows is reported as delivery Not Applicable with one hundred percent delivery progress, rather than waiting indefinitely for a warehouse event.

Deliverable orders require delivery dates. The header date follows the latest item date; a missing row date is filled from the header. A delivery date before the order date fails. A row may have several delivery schedule records containing date, transaction quantity, stock quantity, selected unit, stock unit, conversion and warehouse. Schedule stock quantity equals schedule transaction quantity multiplied by the row factor. Replacing a schedule preserves retained records and removes omitted records for that row. The inspected helper takes the first supplied schedule's date for the order row; a replacement must not assume it automatically sorts arbitrary input before choosing that date.

Evidence: source-artifact-91be43ae56a85a5b24a7 lines 371–448; source-artifact-91be43ae56a85a5b24a7 lines 478–568; source-artifact-63483c398054469c023c lines 14–95.

## Picking and explicit reservation routes

The inspected order-to-pick-list route rejects an order that already has explicit reserved stock. This avoids having two competing allocation mechanisms claim the same goods. Use the reserved-stock delivery route for reserved orders, or deliberately release the reservation before creating the pick list. A pick list can itself become the source of a reservation through a different workflow; this does not negate the order-mapper restriction.

For a normal row, convert picked stock quantity into order units, then compute remaining quantity to pick as ordered quantity minus the larger of picked quantity and delivered quantity. Do not subtract both picked and delivered quantities because delivered goods can already be included in picked goods. If ten cases were ordered, six picked and four delivered, the remaining pick requirement is four cases, not zero. Packed component quantities scale by the parent's remaining fraction. Closed rows and supplier-delivered rows are excluded.

Explicit reservations limit future delivery to the correct product, warehouse and optionally serial or batch identities. Availability and allowed reservation arithmetic are in the inventory specification. Reservation consumption, cancellation and transfer are stateful operations; a printed picking list alone is not proof that physical stock was dispatched.

Evidence: source-artifact-141c781627874ac461f9 lines 1033–1081; source-artifact-b1dc48719460ed10d39e lines 563–690; source-artifact-b1dc48719460ed10d39e lines 726–781.

## Delivery generation and shipment

Mapping an order to a delivery requires a submitted order. It excludes closed rows, rows fulfilled by a supplier and rows whose delivery is not required. Date filters can select exact delivery dates or a cutoff date. The ordinary mapped quantity is ordered quantity minus delivered quantity minus quantity already included in the target draft. Quantity-zero unit-price rows use their separate eligibility rule. Price and company-price amounts are recalculated for the mapped quantity using the source row's rates before the target's normal missing-value and total calculation routines run.

When delivering reserved stock, reservation rows determine warehouse and identity allocations rather than letting ordinary row mapping also allocate them. Preserve order-row references when splitting one commercial row across multiple warehouse or allocation rows. Packing slips prepare draft deliveries, dispatch posts inventory, and shipment records coordinate transport. Carrier tracking state does not replace the submitted stock document's accounting state.

Evidence: source-artifact-141c781627874ac461f9 lines 236–359. Packing and transport measurements are defined in [products, units and packaging](products-units-and-packaging.md).

## Billing quantity after returns and replacement delivery

The order-to-invoice quantity contract is intentionally more nuanced than ordered quantity minus billed quantity. First determine the quantity billable after returns and replacement deliveries: take the smaller of ordered quantity and the larger of ordered quantity minus returned quantity and delivered quantity. Then subtract submitted invoice quantities and quantities already mapped into the target draft, round to the row quantity precision, and clamp the pending quantity to zero.

For an order of ten, two returned and eight currently delivered, the billable quantity is eight. If replacement delivery raises delivered quantity back to ten, billable quantity becomes ten. If six have already been billed, pending quantities are respectively two and four. A replacement must preserve this distinction between a final reduction in the sale and a returned item that is subsequently replaced. Amount eligibility also considers configured overbilling allowance. Unit-price rows and amount remaining on previously billed rows require their own special treatment; their amount cannot be inferred solely from a nonzero quantity test.

Evidence: source-artifact-141c781627874ac461f9 lines 436–558.

## Purchasing and receipt generation

Procurement can originate in a material request, production demand, a sales order needing purchased goods, supplier quotations or a direct purchase order. A purchase order commits quantity, rate, supplier, company, expected date, warehouse and source demand references. Its submitted state contributes expected inbound quantity; it does not itself prove receipt. Receiving and billing can be partial and can proceed through separate linked documents.

The purchase-order-to-receipt mapper requires a submitted source, excludes supplier-direct and closed rows, and subtracts both already received quantity and quantity already present in the target draft. While ordinary ordered quantity remains, that remainder is proposed. Once ordinary quantity is fully received, any remaining permitted over-receipt allowance can still be proposed. Maximum receivable quantity equals ordered quantity multiplied by one plus allowance percent divided by one hundred. For an order of one hundred pieces with five percent allowance, receiving one hundred allows another five, but the initial receipt proposal remains the ordinary outstanding quantity rather than automatically adding the allowance.

Mapped stock quantity is target transaction quantity multiplied by the original factor. Document amount is target quantity multiplied by source rate; company amount additionally multiplies by the document exchange factor. The mapper preserves purchase order row, originating material request, sales order and other applicable source links. Zero-quantity unit-price rows remain a separate path.

Evidence: source-artifact-0a7930220e6f93cf26a5 lines 26–107.

## Receipt execution and warehouse placement

A receipt checks business posting time, order date compatibility, required purchase order policy, referenced documents, inspection requirements, whole-number units, provisional accounting accounts and source order hold or closure. The inspected path rejects a posting date in the future. Accepted and rejected goods retain separate quantity and warehouse information; rejected stock valuation is controlled by purchasing settings and must not be assumed always zero.

Submission first updates source-document progress, then updates stock and financial ledgers and schedules affected future valuation recalculation. That order is significant because warehouse planned quantities depend on the newly updated purchase-order received quantity. Cancellation reverses the source progress and stock or financial effects in the corresponding dependency order. A transaction failure must roll back the entire business operation, not leave an order marked received without its inventory.

Putaway rules express quantity capacity per product and warehouse. Stock capacity is configured commercial capacity multiplied by conversion factor. Free capacity is stock capacity minus current stock. Allocation chooses the smaller of pending stock quantity and available capacity, converts back to the transaction unit, and floors the result when that unit requires whole numbers. Thus capacity for seventeen pieces with a six-piece indivisible pack permits two packs, or twelve pieces; it does not permit a third pack. Rules consume capacity while splitting incoming rows among warehouses. Unaccommodated quantity is reported for operator resolution. This is quantity capacity, not geometric box fitting.

Evidence: source-artifact-d5380569afb1caff0e06 lines 239–449; source-artifact-598fd7f1fda59f4050a8 lines 88–200; source-artifact-d895b5cf742b4120514c lines 23–153.

## Returns, cancellation and incomplete commitments

A reference return uses the same party and company as its source and cannot predate that source. Its exchange factor must agree with the referenced transaction. A sales invoice return cannot enable stock update when the referenced invoice did not deliver stock. Reference returns must not exceed the original returnable quantity less already returned quantity. Stock-updating documents compare stock quantities, while invoices without stock update compare transaction quantities. Accepted and rejected warehouse return paths have distinct remaining-quantity checks.

Return quantities are negative in the commercial return document. Physical ledger direction follows the business flow: a customer return increases available company inventory; a supplier return decreases it. The financial credit or debit and inventory effect remain independently controlled by the document's role. Cancelling an order with downstream submitted documents is constrained, and a closed sales order must be reopened before cancellation. Closing an unfulfilled row writes off its remaining expectation; it does not claim that the missing goods were delivered. Progress and closure arithmetic is owned by [transaction progress and row closure](transaction-progress-and-row-closure.md).

Evidence: source-artifact-1ee006cdbf659be60221 lines 22–87; source-artifact-1ee006cdbf659be60221 lines 192–257; source-artifact-91be43ae56a85a5b24a7 lines 478–568.

## Acceptance scenarios

1. Quote two Cases of Twelve, order one, then map the remainder. Verify the second order receives twelve stock units and one transaction case.
2. Quote an ordinary row plus an alternative group. Select only one alternative and ensure the other option never becomes mandatory fulfilment demand.
3. With one hundred pieces ordered and five percent receipt allowance, receive one hundred then five; reject a further quantity outside the allowance unless an authorised override applies.
4. With ten cases ordered, six picked and four delivered, propose four for picking. A second draft mapping must subtract the first target's mapped quantity.
5. Prevent the ordinary order-to-pick-list route while the order already carries explicit reservations.
6. Receive stocked goods, then invoice without stock update. Verify only one inventory receipt and one purchase price variance when standard cost applies.
7. Return two of ten, bill eight, and then replace the two. Verify the later billing limit follows the replacement-delivery rule.
8. Close a partially fulfilled row and verify that closure changes the remaining obligation without fabricating delivery or a ledger movement.

## Review boundary

These contracts are supported by the inspected source ranges. Every supplier quotation selection policy, direct-delivery accounting variation, delivery-schedule validation entry point, credit override and inter-company pairing still needs its dedicated acceptance fixture before whole-domain dynamic equivalence can be claimed. Missing fixture coverage is a verification boundary, not permission to use a generic order-processing approximation.
