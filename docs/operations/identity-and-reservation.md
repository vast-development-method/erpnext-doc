# Identify, value and release specific stock

## Choose eligible serials and batches

A bundle binds direction, company, item, warehouse, posting timestamp, voucher and row. It contains serial and/or batch entries with signed stock quantities, rates and extended values. A serial-tracked row needs a serial, a batch-tracked row needs a batch, and the serial/batch pair must agree when both are tracked on the outward path. Batch-only zero quantity normally fails except the inward stock-reconciliation case. Installation, job-card, maintenance and pick-list contexts may carry identities without invoking the ordinary stock valuation routine.

Auto-allocation starts with eligible batch/location rows and their relevant balances. Add legacy stock-ledger batch effects for the same pair. Reduce quantities by applicable POS holds, stock reservations and picking allocations. Missing or expired candidate rows must not be introduced by a reservation deduction. A sales-order reservation may narrow the candidate batches/locations. Expiry-based selection orders dated rows by earliest expiry and undated rows last. A historical query may filter lots depleted in a later view. Remove nonpositive balances at stock precision unless the explicit negative-batch policy applies. With a positive requested amount draw sequentially up to the remainder. The calculation may return less than requested. Posting must apply its own sufficiency checks.

For A with 7 units but 5 reserved for another demand, B with 3 and C with no expiry and 5, earliest-expiry demand of 6 can use A2, B3, C1 when the ordered candidates are A, B, C. The three physically allocated identities need not determine three independent valuation pools.

## Determine the stock value of those identities

| Mode | Effective valuation |
|---|---|
| Serial-specific valuation enabled | On issue resolve each serial's latest qualifying inward positive entry for the same item and warehouse through posting time, excluding the current voucher where specified. Order by posting time then creation. Retain a legitimate zero rate. Older storage has a separate fallback. |
| Serial-specific valuation disabled | Identity still tracks custody. In the outward rate routine skip per-serial pricing and apply the item/location valuation path. A prior stale serial outgoing rate can be replaced by the running rate on repost. |
| Batch with independent valuation | Use batch value / quantity in this warehouse when a balance exists. A single receipt at 10 followed by an equal-quantity receipt at 20 sets the batch rate to 15. Returning one originally received at 20 from this batch consumes 15. This prevents leaving value behind when the quantity is exhausted. |
| Batch participating in pooled FIFO/LIFO | Keep the selected lot for traceability and value the outgoing stock using the item's applicable layer queue. Partial withdrawal may span several unit costs. Persist the queue after each qualifying bundle row. |
| Reference return | Validate selected identities against the original receipt/delivery during normal validation. For an eligible batchwise outward return with available balance use the current batch average, including zero. An unavailable average leaves the original-reference rate fallback. Exclude serialized and inward operations from this override. Moving average with batchwise pricing globally disabled also skips it. |

Calculate each bundle row's value as signed quantity × effective row rate. Sum values and signed quantities, then divide totals for the weighted bundle rate (zero when total quantity is zero). Issuing two units at 10 and three at 14 produces quantity −5, value −62 and rate 12.4. An arithmetic average of the two rates would understate the cost.

## Persist only the physical entitlement used

Each reservation header belongs to one voucher row and location. Each tracked reservation child carries serial/batch, reserved, and already delivered quantities. For unbatched availability start with actual ledger stock and subtract effective other reservations' reserved − delivered − transferred − consumed quantities using the source's locked aggregate. A batch-specific lookup consults the batch calculation. For a batch-only reservation reject a disabled or unavailable batch. When the requested amount exceeds positive availability, partial reservation clamps it to available quantity. Disabling that setting rejects it. A bundle component also has to fit its own remaining order-row demand. The [shop-floor handoff](shop-floor.md) describes reservations transferred from production demand to another voucher.

When fulfilling tracked stock, read eligible children with a lock, oldest reservation creation first and child row order next. For release, use latest creation first and **delivered** quantities as the amount open for reversal. A selection has a signed direction, an exact list of serial identities or batch quantities, and a remaining maximum per reservation parent.

1. A serial match transfers the whole available row only if the serial was requested and the parent cap covers it. Remove that serial from the selection once used. Do not divide a serial or substitute a different serial that happens to share the same batch.
2. For a batch-only row take the least of open child quantity, residual selection for that batch and parent cap. Reduce the selection and cap before visiting the next row. Update each child's delivered quantity by its own delta, applying the reverse sign on release.
3. For old and new reservations of batch A holding 3 and 4 units, fulfilling 5 consumes 3 old and 2 new. Returning 3 from these eligible allocations gives back 2 new and 1 old. Remaining delivered amounts are 2 old and 0 new. Unrelated batch B remains untouched.
4. For fractionally converted quantities correct only the last allocation for round-off to the ledger quantity. Preserve previous allocations. A release caps the requested decrement by what was delivered and rounds the *remaining* balance at child precision. For an indivisible sales unit of measure with factor six, 17 stock units represent at most two whole units in the ordinary floor branch.

A stock-updating invoice or delivery that names another demand's reserved batch, or a serial not allocated to its sales order, may lack available stock even when the warehouse total is positive. Handling a return and cancelling a delivery must release the correct child identities before they become available for later reservations. Verify held-stock concurrency with simultaneous writers and reconcile total header, child and voucher balances after each retry.
