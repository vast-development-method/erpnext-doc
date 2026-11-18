# Worked document transitions

## A sales invoice posts with or without a physical movement

Read the [sales invoice stages](accounting.json) alongside the [field and relationship index](../../schema/index.tsv). A billing clerk posts an invoice against an approved delivery. The invoice has an optional inventory-update selection, originating order and delivery lines, a customer, company, currency, taxes and, where applicable, tracked stock, fixed assets, time records and loyalty information.

1. Validate the paid amount for a point-of-sale invoice, the actor's amount-based approval authority and the states of linked commercial records. When a return disables the sales-order billed-amount update, suppress that update. Apply sales withholding, then update originating document progress and delivery-note billing. Drop unallocated payment methods.
2. When the invoice updates stock, construct the applicable tracking allocations for normal and packed rows, validate tracked identifiers, update reservations, post movements and verify produced identifiers against their reservations. Originating progress must already reflect delivered quantities when warehouse balances are calculated. With a separate delivery and no inventory update, invoicing performs its accounting work without issuing those units a second time.
3. Split a sold asset where quantity requires it. An ordinary sale processes depreciation before setting disposal values and posting the accounts. A return processes the depreciation reversal after the accounting entries so that reinstatement can use the prior asset value.
4. An inventory-affecting invoice can require recalculation of later inventory and financial entries, pick status and project material cost. An ordinary nonopening invoice also checks credit and overdue billing thresholds. If a later blocking rule fails within this transaction, earlier provisional ledger writes are rolled back.
5. Apply the remaining applicable settlement, time-billing, intercompany, coupon, loyalty and subcontract-billing rules. A return can recalculate loyalty awarded on its original invoice. The presence of a coupon field or a customer does not by itself establish a loyalty entry.

For a single unit shipped on a separate delivery, inspect invoice progress, customer receivable and sales tax after commitment. The invoice has no additional physical issue. For an otherwise comparable invoice that both bills and ships the unit, inspect its stock movement, reserved quantity, cost entry and financial voucher together.

## A manufacturing stock movement changes reservations before valuation

The [inventory stage register](inventory.json) covers ordinary transfers, independent issues, manufacturing movements and subcontracting movements. On posting a stock movement, resolve serial or batch tracking for disassembly, associate tracking allocations, update work-order and disassembly progress, adjust return reservations and update stock reservations. Release the work order's applicable material reservation for subcontracting **before** the stock availability and valuation routine processes the issue.

Post inventory movements before recording the finished goods' relationships to consumed materials. Then handle work-in-progress and finished-goods reservations, subcontract stock, supplied quantities, subcontract order and pick status. Apply the accounting effects and any recalculation of later transactions, project material costs, transferred quantities and inspection updates. A transit leg marks the request in transit. A corresponding arrival leg marks the request completed under its own conditions.

For a work order with two units both reserved and both being issued to its subcontractor, the issue must consume its own authorized reservation. It must not treat another order's two reserved units as free. Cancelling the issue applies the cancellation rules for work orders, subcontract supply, reservations, inventory, accounting and project costs. A validation relating to a linked asset repair or closed subcontract order can prevent cancellation.

## A payment cancellation restores settlement balances

For [payment entries](accounting.json), a nonzero difference amount blocks posting before payment withholding or ledger work. A balanced payment applies applicable withholding, updates linked payment requests and schedules, records its financial entries, refreshes outstanding balances and collection notices, sets status and requests any linked subscription update.

On cancellation, invoke the inherited financial cancellation policy, reverse payment withholding where applicable, update payment requests in cancellation mode, restore scheduled allocations, reverse or cancel the accounting entries, and recalculate the reference balances. Then refresh linked collection notices, remove advance references, set status and request the subscription invoice update. An invoice with 100.00 outstanding and no other allocations returns to 100.00 outstanding after cancelling its only 100.00 receipt. An independent 20.00 credit changes that expected result to 80.00. Reconciliation must consider every surviving allocation.

## Changing a posted sales order

The [sales order](sales.json) has separate before-change and after-change obligations for submitted orders. A permitted field edit still invokes the inherited before-change policy and checks the customer's purchase order, drop-shipment details, affected suppliers and delivery dates. On a row with positive purchased quantity, a proposed supplier must agree with the previously saved supplier when the row supplies a supplier. Following a successful edit the order rechecks its credit limit.

Two rows can have the same item and different procurement progress. If the first has ordered quantity greater than zero and the second has none, evaluate their supplier changes against their own stored rows. A rejection on the first must leave the aggregate in its preceding committed state.

## Renaming or merging an inventory item

The [inventory item](inventory.json) keeps a display name and a key used by other records. Before the key change, update the display name only if it equalled the old key. For a merge, check compatible properties, duplicated bundle membership and duplicated lead-time definitions. Remove a source warehouse balance row where that warehouse already has a destination balance.

After a merge, check whether the resulting references would produce a repeated item within a submitted reconciliation at one warehouse. Set the surviving item code to the destination key. Recompute the last purchase rate and warehouse balances for a merge. The attached rename action updates the searchable item. Valuation projections can take additional time to catch up. A successful rename is distinct from completion of all subsequent projections. The [bulk rename rules](../services/identity-and-media.md) specify per-row rollback, partial success and notification for an uploaded set of changes.
