# Stock movement acceptance examples

Each row starts from the balances it states. Rates are per stock unit in company currency.

| Input and operation | Required result |
|---|---|
| Receive 10 at 100 and 20 at 200 under first-in, first-out with no independent batch rate. Receive another 5 at 300 and return those 5 against their receipt. | The third receipt adds a layer of 5 at 300. The return restores the initial two cost layers. |
| Receive two lots of 10 units in one batch, priced at 100 and 200 under last-in, first-out with no independent batch rate. Return 5 against the first receipt. | The remaining layers are 5 at 100 and 10 at 200, worth 2,500. |
| Receive 10 into batch A at 100 and 10 into B at 200 under last-in, first-out and no independent batch rate. Issue 5 specifically from batch A. | Physical custody decreases in A. Financial layers become 10 at 100 and 5 at 200. Inventory value decreases by 1,000. |
| Two serials are available in each of two batches. One expires in 60 days and the other in 5 days. Request two serials by earliest expiry. | Both serials come from the batch expiring in 5 days. |
| Receive 2 in one batch. Orders A and B reserve one each and explicitly assign that batch to their delivery lines. | Both deliveries can submit. Each uses its order’s claim. |
| Two batches have 2 units apiece. Order A reserves 2 in one batch. Order B attempts to take the reserved identities. | Reject B’s delivery even though there is free stock elsewhere. |
| Reserve two serials, deliver one, return it and reserve one on a new order. | The returned serial appears once on the new submitted reservation. |
| Offer three whole boxes of 12 for partial reservation, with 25 pieces actually available. | Reserve 24 pieces. |
| Create two correction requests for the same product and location. The later one is created 60 seconds after the earlier one began. | The earlier run leaves the later request queued. |
| Request restart first on a completed correction, then on a failed submitted correction. | Reject the first request. Reset the failed job to queued. |
| Receive 10 at 100, issue five later and cancel the original receipt. Allow negative stock and explicitly permit a zero rate on the pending recalculation. | The correction may complete. |
| Receive 10 at 100, transfer 5 and issue 2 at the destination. Then insert 10 at 200 before the transfer. Queue overlapping corrections for the source and destination. | The source request completes and the overlapping destination request is skipped. The two destination movements are revalued once each, giving running values 750 and 450. |
| Move 45 units between stores and finished goods, then cancel the transfer. | The original physical legs are −45 and +45. If the warehouses use different accounts, credit source inventory and debit target inventory by the same cost. A common account requires no net value transfer. Cancellation reverses the movement. |
| Post consumption of 10 units at 100. On an order for 10 finished units allocate 25% of that cost to five units of scrap. Save the manufacture draft. | Consumption is 1,000. The draft values the primary output at 750 and scrap at 250. The draft alone has no new stock posting. |
| Receive five components into each of two batches. Transfer ten into production, manufacture five twice and disassemble five twice. | The two recovered material-batch identities match the two original receipts, including multiplicity. |
| Manufacture from two units of raw material with a designated primary output and an additional target row having no output classification. | Reject the manufacture. |
| Receive 10 in a batch at 100, complete a stock closing and calculate the next closing opening. | The product and warehouse carry forward 10 units worth 1,000. |
| Cancel an inventory closing after its provisional balances have been generated and before publication. | Keep the closing cancelled and remove its provisional balance rows. |
| Submit a valuation correction before period end and leave it pending. Attempt an inventory closing through that period in the same company. | Reject the closing while that correction is pending. |
| Receive 10 at 100 and complete a closing. Insert another receipt of five at 100 before the closing cutoff. Run the balance report for the following period. | Mark the closing outdated. In the absence of further movements, both opening quantity and closing quantity are 15. |
