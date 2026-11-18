# Commerce and regional exchanges

## Customer carts and order conversion

Find the most recently modified draft shopping quotation for the party and current contact email. Resolve each online listing to a stock item or service and its online warehouse. Setting a nonzero item quantity inserts the line or replaces the first matching line’s quantity. Setting zero removes the item. Removing the final line closes the empty draft. Reapply current pricing, tax and shipping terms when changing the cart.

Order placement requires a shipping or billing address, an authorized party, a selling company and a valid quotation. Clear the copied payment schedule when mapping to the customer order. If out-of-stock sales are disallowed, require positive availability in the online warehouse and sufficient quantity for every stock line. Services bypass the stock availability test. Commit the quotation submission and resulting order together or restore the earlier state after rejection. Quote-only checkout follows its own save or submit policy.

A quotation is a price offer. A store that promises hard reservation must enforce it when accepting orders. If five units are available and two buyers concurrently order four, compare the accepted reservations and their fulfilment commitments against the five units.

## External channel orders

Match the external account and order reference, resolve customer and addresses, map every external product and preserve the commercial prices from the channel order. A missing product puts the order into exception review. A repeated notification returns the existing order reference. Paid and fulfilled notifications may respectively trigger an invoice or a dispatch. Each needs its own identity and reconciliation.

For a positive line quantity q, supplied unit price p, total line discount D and total line tax T, the imported rate is p − D/q for tax-exclusive pricing and p − (D + T)/q for tax-inclusive pricing. At p = 60, q = 2, D = 10 and T = 12, those rates are 55 and 49. For the inclusive line, 2 × 49 + 12 = 110, equal to 120 less the 10 discount. A rate at or below zero marks a free item and applies the full discount to prevent automatic repricing. Map emitted taxes to the company’s tax accounts.

On external cancellation, cancel a submitted order that has no posted invoice or delivery. Where downstream documents already exist, record the external financial status against all linked documents and reconcile each downstream reversal or refund separately.

## Carrier offers and booking

Request offers using available providers, pickup and drop-off addresses, parcel measurements and collection day. Offers with a known price sort first in ascending total price. Zero is a valid quoted price. A missing price is ineligible for booking. Preserve provider and service identities on each offer, since the cheapest offers can otherwise be indistinguishable.

On confirmed booking store carrier, service, consignment identity, price, waybill and booked state, then associate that response with the specified dispatch notes. Label attachment, tracking messages, warehouse dispatch and billing remain individually traceable. When a provider may already have accepted a timed-out request, reconcile its booking reference before retrying.

## Collection and donation settlement

Validate currency and minimum amount under the selected payment channel. With a configured minimum of 0.50, 0.49 is rejected and 0.50 accepted. For a two-decimal currency, 24.50 corresponds to 2,450 minor units. Use the agreed exponent for the currency and provider rather than assuming every currency has two decimal places.

Record external capture independently of local settlement. A paid or authorized request can still have an unposted allocation if local processing failed. Reconcile request and provider identities, then post the authorized payment once. For an invoice accounted for in company currency at 18 company units per collection unit, a party balance of 360 settles for 20 collection units at that rate.

A directly captured donation must authenticate the event and exclude invoice-linked or subscription captures already handled by other flows. Resolve the donor by the declared matching policy and payment method, store the capture identity and convert minor units. At two decimal places, 125,050 minor units equals 1,250.50. Automatic donation accounting requires an eligible payment account and one linked payment voucher under the donation's account mapping. When disabled, keep the donation receipt without that automated posting.

## Regional control examples

| Decision | Configuration and expected result |
|---|---|
| Indian electronic invoice registration | Check selling company registration, buyer billing registration, place of supply, applicable date and taxable lines. A duplicate registration response requires recovery of the registered buyer and total. Attach the recovered registration only if both match. Where the selected profile permits cancellation through 24 hours after acknowledgement, equality passes and later requests fail. A separately cancelled transport document remains succeeded if subsequent invoice-registration cancellation fails. |
| German financial inspection bundle | Verify access to the selected tables and submit permission before queuing assembly after commit. Include scoped parent and child records, the ordered structural index and allowed attachments. Mark completed only after attaching the private archive. Failures retain the request and cause. |
| German accounting exchange | Select company, adviser, client, chart and ordered columns. Order vouchers by effective date with a stable tie order. Emit metadata, headings and data. Under the regional interchange profile use day/month for voucher date, full day/month/year for full dates, decimal comma, a semicolon field separator and the receiving party’s approved character encoding. |
| French euro payment batch | Match a bank event to the batch line by end-to-end identity. A missing line blocks matching. A line already accepted returns its earlier result. Require a ledger account on the batch bank and reconcile the posted allocation to the matching bank movement. |
| United States sales tax account routing | Check company jurisdiction and that configured sales tax and shipping ledger accounts belong to the same company and accept postings. Accounts with the same display label in a second company are distinct. Resolve statutory rates and the related quote separately. |
| Integration of shared product and access grants | Resolve the explicitly linked product counterpart. When mirroring a grant, bind the target user and record, apply access scope, and mark the propagation so it cannot echo indefinitely. Changing or removing the origin removes only its owned mirror. |

## Instalment payment orders

A submitted supplier invoice with a balance can supply a bank payment order. An omitted schedule selection means all eligible rows, while an explicitly empty selection means none. A selected instalment must have positive outstanding after two-decimal eligibility rounding. Retain invoice and schedule line identifiers. Pay the supplier by default. Pay an employee only when both the business-trip employee and the employee-payment instruction are present. Select an enabled company bank account, preferring its designated default. Creating the order does not send instructions to the bank.

Sum non-cancelled payments on **other schedule rows** for the same invoice, including draft payments. Cap the selected instalment at max(0, invoice outstanding − other-row payments). A deleted schedule row has calculated payment zero. If execution is on or before the discount deadline, apply the percentage discount to the capped amount and round at the schedule’s outstanding precision.

An invoice has 100 outstanding, a different row accounts for 30, and the selected instalment has 90 outstanding. The cap is 70. A 2% discount on its last eligible day yields 68.60. The next day it yields 70. An existing payment of 68.60 on the same schedule row does not reduce its own recomputation. If other rows already cover 110, the calculated payment is zero.

## Cost centre on a property service

For the price-list service model, require a company and an active requested property. Preserve an existing line cost centre. Skip submitted lines, metered lines and rows without an item. Select the row’s expressly requested property, otherwise the sole requested property, otherwise the unique requested property whose service item matches. More than one matching property leaves allocation unresolved.

Resolve the selected property’s cost centre and then the item’s selling default for the request company. Accept only cost centres in that company. Synchronizing a property's own service item can fill a missing company default without replacing an existing selling cost centre. Two requested properties sharing a service item but carrying different cost centres require the service line to name its property before selecting either centre.

## Warehouse group restrictions

With warehouse restrictions enabled, validate inventory movement, receipt, dispatch, stock-updating sales or purchase invoice and count adjustments at save and at submission. For a transfer test both source and target for each item whose group is known. Otherwise test the line warehouse. Match the active rule by company and warehouse. An absent rule permits the item. Aggregate violations by line and warehouse. Transferring a tool between a tool-permitted origin and a food-only destination fails once for its destination. If neither permits tools, the same line has two violations.
