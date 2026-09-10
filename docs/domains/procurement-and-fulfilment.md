# Procurement and fulfilment

## Domain responsibility

Commercial commitments, physical receipt or dispatch, supplier or customer invoices, stock reservations and settlement are distinct records with linked row identities. An order expresses a commitment and updates planning quantities. A receipt or delivery changes stock. An invoice records the financial claim and can additionally perform the stock movement when its stock-update option is enabled. A payment settles a claim. The implementation must support partial performance and preserve the exact upstream row for each downstream quantity and amount.

Use the companion [inventory and valuation](inventory-and-valuation.md), [products, units and packaging](products-units-and-packaging.md), and [transaction progress and row closure](transaction-progress-and-row-closure.md) specifications for the arithmetic they own. Pricing, taxes, approval exposure and credit control are accounting contracts invoked during this workflow, not alternative calculations to be reinvented here.

## Records and durable links

| Stage | Required persistent reference |
|---|---|
| Commercial offer and commitment | [Sales order](../../schemas/data/record-types/sales_order.json), [sales row](../../schemas/data/record-types/sales_order_item.json), [purchase order](../../schemas/data/record-types/purchase_order.json) and [purchase row](../../schemas/data/record-types/purchase_order_item.json) retain party, company, unit, factor, rate and predecessor row |
| Receiving | [Receipt](../../schemas/data/record-types/purchase_receipt.json) and [receipt row](../../schemas/data/record-types/purchase_receipt_item.json) retain accepted, rejected, stock and returned quantities with warehouse placement |
| Dispatch | [Delivery](../../schemas/data/record-types/delivery_note.json) and [delivery row](../../schemas/data/record-types/delivery_note_item.json) retain order-row fulfilment and stock valuation independently of invoicing |
| Reserved allocation | [Stock reservation](../../schemas/data/record-types/stock_reservation_entry.json) identifies the physical claim against the same upstream child row |
| Shared quantities | [Inventory mathematics](../../schemas/mathematics/inventory-calculations.json) and [acceptance examples](../../schemas/mathematics/inventory-acceptance-cases.json) specify picking, ordering, billing, over-receipt and putaway |

A header identifier alone is insufficient to match obligations: two rows for the same product can carry different prices, delivery dates, warehouses, projects or unit factors. Mapping and returns preserve the relevant child-row identity.

## Quotation and conversion to an order

A quotation can address an existing customer or another supported commercial party that is resolved to a customer during conversion. It records company, transaction date, validity end date, quoted products and units, price and tax context, optional alternatives and source opportunity references. The validity end cannot precede the quotation date. A setting controls whether expired quotations can still generate orders. When the setting disallows it, a validity end before the current date prevents conversion.

Quotations support alternatives: an alternative product is not simply another mandatory line in the total requirement. Without selections, mapping takes ordinary non-alternative rows. With selected alternatives, alternative groups map only the selected eligible rows; ordinary independent rows remain eligible. Quantity already ordered is tracked in stock units. Quantity already mapped into the in-progress target is also subtracted, preventing duplicate allocation when combining documents into one draft.

Remaining ordered stock quantity is quoted stock quantity minus already ordered stock quantity minus stock quantity already mapped into the current target, clamped to zero. Target transaction quantity is this remainder divided by the original conversion factor. Zero-quantity unit-price rows have a separate setting-controlled path because they quote an uncertain future quantity. They must not be silently removed by a generic positive-quantity filter. Quotation state becomes Open, Partially Ordered or Ordered by comparing applicable rows with submitted order rows; unselected alternatives do not keep a fulfilled quotation artificially incomplete.

## Sales order contract and fulfilment demand

A sales order references the original quotation row where applicable. Referenced company, product, selected unit and conversion factor must agree. A setting can require the sales rate to remain equal to the referenced rate. Submitting the order checks credit exposure and approving authority, updates stock planning reservations, linked quotation and opportunity status, project information, blanket order usage and configured coupon usage, and creates explicit stock reservations when enabled. These are separate effects; merely writing a header state is insufficient.

Supplier-direct delivery requires a supplier on the row. It must not generate a normal company warehouse dispatch for the same quantity. A non-stock service may skip delivery when configured. Stock items, fixed assets and product bundles containing stocked components require delivery. An order that has no deliverable rows is reported as delivery Not Applicable with one hundred percent delivery progress, rather than waiting indefinitely for a warehouse event.

Deliverable orders require delivery dates. The header date follows the latest item date; a missing row date is filled from the header. A delivery date before the order date fails. A row may have several delivery schedule records containing date, transaction quantity, stock quantity, selected unit, stock unit, conversion and warehouse. Schedule stock quantity equals schedule transaction quantity multiplied by the row factor. Replacing a schedule preserves retained records and removes omitted records for that row. The inspected helper takes the first supplied schedule's date for the order row; a replacement must not assume it automatically sorts arbitrary input before choosing that date.

## Picking and explicit reservation routes

The inspected order-to-pick-list route rejects an order that already has explicit reserved stock. This avoids having two competing allocation mechanisms claim the same goods. Use the reserved-stock delivery route for reserved orders, or deliberately release the reservation before creating the pick list. A pick list can itself become the source of a reservation through a different workflow; this does not negate the order-mapper restriction.

For a normal row, convert picked stock quantity into order units, then compute remaining quantity to pick as ordered quantity minus the larger of picked quantity and delivered quantity. Do not subtract both picked and delivered quantities because delivered goods can already be included in picked goods. If ten cases were ordered, six picked and four delivered, the remaining pick requirement is four cases, not zero. Packed component quantities scale by the parent's remaining fraction. Closed rows and supplier-delivered rows are excluded.

Explicit reservations limit future delivery to the correct product, warehouse and optionally serial or batch identities. Availability and allowed reservation arithmetic are in the inventory specification. Reservation consumption, cancellation and transfer are stateful operations; a printed picking list alone is not proof that physical stock was dispatched.

## Delivery generation and shipment

Mapping an order to a delivery requires a submitted order. It excludes closed rows, rows fulfilled by a supplier and rows whose delivery is not required. Date filters can select exact delivery dates or a cutoff date. The ordinary mapped quantity is ordered quantity minus delivered quantity minus quantity already included in the target draft. Quantity-zero unit-price rows use their separate eligibility rule. Price and company-price amounts are recalculated for the mapped quantity using the source row's rates before the target's normal missing-value and total calculation routines run.

When delivering reserved stock, reservation rows determine warehouse and identity allocations rather than letting ordinary row mapping also allocate them. Preserve order-row references when splitting one commercial row across multiple warehouse or allocation rows. Packing slips prepare draft deliveries, dispatch posts inventory, and shipment records coordinate transport. Carrier tracking state does not replace the submitted stock document's accounting state.

Packing and transport measurements are defined in [products, units and packaging](products-units-and-packaging.md).

## Billing quantity after returns and replacement delivery

The order-to-invoice quantity contract is intentionally more nuanced than ordered quantity minus billed quantity. First determine the quantity billable after returns and replacement deliveries: take the smaller of ordered quantity and the larger of ordered quantity minus returned quantity and delivered quantity. Then subtract submitted invoice quantities and quantities already mapped into the target draft, round to the row quantity precision, and clamp the pending quantity to zero.

For an order of ten, two returned and eight currently delivered, the billable quantity is eight. If replacement delivery raises delivered quantity back to ten, billable quantity becomes ten. If six have already been billed, pending quantities are respectively two and four. A replacement must preserve this distinction between a final reduction in the sale and a returned item that is subsequently replaced. Amount eligibility also considers configured overbilling allowance. Unit-price rows and amount remaining on previously billed rows require their own special treatment; their amount cannot be inferred solely from a nonzero quantity test.

## Purchasing and receipt generation

Procurement can originate in a material request, production demand, a sales order needing purchased goods, supplier quotations or a direct purchase order. A purchase order commits quantity, rate, supplier, company, expected date, warehouse and source demand references. Its submitted state contributes expected inbound quantity; it does not itself prove receipt. Receiving and billing can be partial and can proceed through separate linked documents.

The purchase-order-to-receipt mapper requires a submitted source, excludes supplier-direct and closed rows, and subtracts both already received quantity and quantity already present in the target draft. While ordinary ordered quantity remains, that remainder is proposed. Once ordinary quantity is fully received, any remaining permitted over-receipt allowance can still be proposed. Maximum receivable quantity equals ordered quantity multiplied by one plus allowance percent divided by one hundred. For an order of one hundred pieces with five percent allowance, receiving one hundred allows another five, but the initial receipt proposal remains the ordinary outstanding quantity rather than automatically adding the allowance.

Mapped stock quantity is target transaction quantity multiplied by the original factor. Document amount is target quantity multiplied by source rate; company amount additionally multiplies by the document exchange factor. The mapper preserves purchase order row, originating material request, sales order and other applicable source links. Zero-quantity unit-price rows remain a separate path.

## Receipt execution and warehouse placement

A receipt checks business posting time, order date compatibility, required purchase order policy, referenced documents, inspection requirements, whole-number units, provisional accounting accounts and source order hold or closure. The inspected path rejects a posting date in the future. Accepted and rejected goods retain separate quantity and warehouse information; rejected stock valuation is controlled by purchasing settings and must not be assumed always zero.

Submission first updates source-document progress, then updates stock and financial ledgers and schedules affected future valuation recalculation. That order is significant because warehouse planned quantities depend on the newly updated purchase-order received quantity. Cancellation reverses the source progress and stock or financial effects in the corresponding dependency order. A transaction failure must roll back the entire business operation, not leave an order marked received without its inventory.

Putaway rules express quantity capacity per product and warehouse. Stock capacity is configured commercial capacity multiplied by conversion factor. Free capacity is stock capacity minus current stock. Allocation chooses the smaller of pending stock quantity and available capacity, converts back to the transaction unit, and floors the result when that unit requires whole numbers. Thus capacity for seventeen pieces with a six-piece indivisible pack permits two packs, or twelve pieces; it does not permit a third pack. Rules consume capacity while splitting incoming rows among warehouses. Unaccommodated quantity is reported for operator resolution. This is quantity capacity, not geometric box fitting.

## Returns, cancellation and incomplete commitments

A reference return uses the same party and company as its source and cannot predate that source. Its exchange factor must agree with the referenced transaction. A sales invoice return cannot enable stock update when the referenced invoice did not deliver stock. Reference returns must not exceed the original returnable quantity less already returned quantity. Stock-updating documents compare stock quantities, while invoices without stock update compare transaction quantities. Accepted and rejected warehouse return paths have distinct remaining-quantity checks.

Return quantities are negative in the commercial return document. Physical ledger direction follows the business flow: a customer return increases available company inventory; a supplier return decreases it. The financial credit or debit and inventory effect remain independently controlled by the document's role. Cancelling an order with downstream submitted documents is constrained, and a closed sales order must be reopened before cancellation. Closing an unfulfilled row writes off its remaining expectation; it does not claim that the missing goods were delivered. Progress and closure arithmetic is owned by [transaction progress and row closure](transaction-progress-and-row-closure.md).

## Operational decision table

| Event | Commitment and progress | Warehouse consequence | Financial consequence |
|---|---|---|---|
| Submit sales order | Establish demand and approval exposure; reserve planning quantity | No dispatch; optional explicit physical reservation | No customer invoice solely from order submission |
| Submit purchase order | Establish expected inbound commitment | No receipt | No supplier payable solely from order submission |
| Create pick list | Select physical locations and track picking quantity | No dispatch solely from creating a pick list | No sales revenue solely from picking |
| Submit purchase receipt | Increase received progress against purchase row | Receive accepted and applicable rejected stock | Perpetual inventory posts received stock and goods-received clearing, with taxes or variances where applicable |
| Submit delivery | Increase delivered progress against sales row | Issue stocked items or bundle components | Perpetual inventory recognises stock cost; sales revenue is governed by the invoicing contract |
| Submit invoice without stock update | Increase billing progress | No additional receipt or dispatch | Create payable or receivable and its tax, revenue, expense or receipt-clearing effects |
| Submit invoice with stock update | Update billing and stock-relevant progress in one business operation | Perform the stock effect that was not already posted by a separate receipt or delivery | Post both financial claim and applicable inventory consequences |
| Close remaining row | Remove unfulfilled expectation according to closure policy | No fabricated receipt or delivery | No fabricated invoice or payment |
| Cancel submitted performance | Reverse qualifying submitted progress | Reverse its own stock effect and recalculate subsequent value | Reverse its own financial entries under period and dependency controls |

The table does not permit posting both a receipt and a stock-updating invoice for the same quantity without the applicable linked-quantity validation. A replacement must distinguish stock already handled by a predecessor from stock deliberately handled by the invoice.

## Partial fulfilment with mixed units

Order ten Cases of Twelve, giving one hundred twenty stock pieces. Deliver three cases, leaving eighty-four stock pieces outstanding. A subsequent mapper operating in the original case unit proposes seven cases, less any quantity already present in its target draft. An operator's view of fourteen Packs of Six is the same eighty-four-piece demand, but a change of reference unit must pass the upstream unit-compatibility rule. Conversion arithmetic is not authorisation to alter the original contractual factor.

Assume a customer orders ten units at twenty currency units each, receives ten and returns two without replacement. The billable-after-returns formula permits eight units and a pre-tax amount of 160. If six units were invoiced previously, the newly billable quantity is two. After two replacement units are delivered and the delivered counter returns to ten, the maximum becomes ten and the remaining invoice quantity becomes four, less anything already mapped into the new draft. Cancelling the replacement delivery must restore the former limit and any linked billing must be checked before that cancellation succeeds.

For purchasing, order one hundred units with five-percent over-receipt allowance. Before any receipt, map one hundred. After receiving ninety-eight, map two, not seven. Once ordinary ordered quantity is fully received, a later mapping can propose the remaining allowance of five. After receiving another three, only two allowance units remain. Reject an additional three where the total would exceed one hundred five. Store the authorised allowance policy and the exact required quantity rather than writing one hundred five as if it were the original order quantity.

## Warehouse capacity and concurrent allocation

A putaway rule's capacity is expressed through product quantity and conversion. For capacity twenty Packs of Six, stock capacity is one hundred twenty pieces. If current stock is one hundred three pieces, free capacity is seventeen pieces. A receipt requiring whole packs can place two packs, twelve pieces, leaving five unusable capacity pieces under this unit rule. The unplaced receipt remainder must be offered to another eligible rule or reported as unaccommodated; it must not silently vanish from the receipt.

During allocation of several incoming rows, reduce the available capacity in the same planning context as each preceding allocation. Checking every row against the original seventeen-piece free capacity would overfill the location. This local allocation behavior is distinct from simultaneous receipt concurrency: two separate receipt submissions must additionally protect the effective balances or detect a stale capacity decision before committing. Physical dimensions and load-bearing limits are not inferred by this quantity-capacity rule.

## Return and cancellation acceptance controls

For a reference delivery of twenty-four pieces, a previous customer return of six leaves eighteen returnable pieces. An attempted return of nineteen fails before any warehouse or financial effect. Returning three Packs of Six is quantity-equivalent to eighteen pieces only when the documented reference unit and conversion rules allow that representation. A supplier return uses the same cumulative check but decreases company stock.

A commercial return must preserve party and company and cannot predate the reference. Retain the reference exchange factor where required instead of using today's market factor. A credit note does not automatically return stock when its reference invoice did not update stock. A physical return without immediate credit changes inventory and delivered progress according to its document contract but does not fabricate settlement. Cancellation removes the effectiveness of a transaction; it is not a backdated return entered under another name.

The submit operation must either record all its required source-row progress, stock movements, financial entries and identity consequences or leave a recoverable, explicitly recorded recalculation obligation after the committed posting. Failed validation leaves the draft with no submitted ledger effects. Reopening a closed commitment must restore its allowed business state before its cancellation or further fulfilment can proceed.

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

These contracts are supported by the record and calculation contracts in this repository. Every supplier quotation selection policy, direct-delivery accounting variation, delivery-schedule validation entry point, credit override and inter-company pairing still needs its dedicated acceptance fixture before whole-domain dynamic equivalence can be claimed. Missing fixture coverage is a verification boundary, not permission to use a generic order-processing approximation.
