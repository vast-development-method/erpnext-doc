# Derive effective rates and value changes

The v16.60.0 master-data options for item, company and stock settings are FIFO, Moving Average and LIFO. The existing development-snapshot inventory chapter also specifies Standard Cost. Bind the engine to its selected baseline: applying that fourth policy to this revision would create a configuration absent from its selectors. An item override wins. With a company supplied, the pinned resolver reads its default; without a company it uses stock settings with a FIFO fallback. [Item metadata](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/item/item.json) · [Company metadata](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/setup/doctype/company/company.json) · [Resolution](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/utils.py#L516-L534)

## Calculate one moving-average ledger row

Carry item, warehouse, previous on-hand quantity Q, running rate r, effective signed transaction quantity d, and the incoming or outgoing transaction rate. Let N = Q + d. Historical valuation is ordered by effective posting time and creation within that time. A ledger value change is the difference between two consecutive running values. It can differ from d × the displayed document rate.

| Condition | Running rate before final currency normalisation |
|---|---|
| Receipt, N ≥ 0 and Q > 0 | (Q × r + d × incoming rate) / N |
| Receipt, N ≥ 0 and Q ≤ 0 | Incoming rate, including zero. The receipt crossing through zero establishes the next cost. |
| Issue, N ≥ 0 with a nonzero outgoing rate | (Q × r + d × outgoing rate) / N when N is positive. At N = 0 retain the outgoing rate. |
| Issue, N ≥ 0 without a nonzero outgoing rate | Retain r. An explicit outgoing value of zero is false in this particular condition. |
| N < 0 | If crossing from Q ≥ 0 with a nonzero outgoing rate, adopt it. Otherwise retain r. If the rate is still zero on a positive receipt use its incoming rate. If it remains zero and a voucher detail exists, check its explicit zero-valuation permission before fetching a fallback. |

After applying the rule, extend N × rate. Where N rounded at stock precision is nonzero, divide currency-rounded extended value by stock-precision quantity to recompute the stored rate. Round stock value to currency precision and force it to zero when rounded quantity is zero. Preserve last known rate where the rule retains one. For 10 units at 8 and 2 units returned at 5, N = 8 and remaining value = 70, hence rate 8.75. Using a simple moving-average issue of 2 at 8 would leave only 64. For −3 units at 9, a receipt of 2 at 14 leaves −1 at 9; a receipt of 5 at 14 against the same opening leaves +2 at 14. The two cases don't establish authority to transact in negative stock.

When a nonnegative balance is required, check quantity after the move less reservations to retain, at stock precision. A negative difference is rejected on this guard only when its magnitude exceeds 0.0001 at precision ≤4 or one unit of the configured grid at finer precision. Separate serial/batch, warehouse, and future-balance gates apply. [Row dispatch and value rounding](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/stock_ledger.py#L1190-L1299) · [Moving-average and negative-stock rules](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/stock_ledger.py#L2053-L2144) · [Reservation-aware balance check](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/stock_ledger.py#L1559-L1578)

## Use a rate hint on an outward layer movement

Persist layers oldest first. Quantities with the same rate merge on the trailing layer when receiving. An ordinary issue consumes from the FIFO head or LIFO tail. The source contains additional branches for an explicitly valued outward leg.

| Outward instruction | FIFO chooses | LIFO chooses |
|---|---|---|
| Ordinary, no positive hint | Oldest layer | Newest layer |
| Ordinary, positive hint | Oldest layer whose rate exactly equals the hint; if absent, oldest overall | Newest layer, ignoring the hint for layer selection |
| Purchase return, including zero hint | Oldest matching-rate layer; if absent, oldest overall | Newest matching-rate layer; if absent, newest overall |

Continue selection after each exhausted layer. Matching uses rate equality; equal-price receipts separated in time retain different positions. For layers 2 × 10, 3 × 20, 4 × 10, issue 3 units with rate 10. FIFO at that hint removes 2 units from the first layer and 1 from the last, leaving [3 × 20, 3 × 10]. LIFO purchase return removes 3 from the last, leaving [2 × 10, 3 × 20, 1 × 10]. Both balances are worth 90. The next unhinted one-unit issue costs 20 under FIFO and 10 under LIFO. If the requested return rate is 99 and no layer matches, return one unit from the FIFO head at 10 or LIFO tail at its rate. At the untracked ledger dispatcher the explicit purchase-return flag is only set for eligible returning purchase/subcontract receipt/invoice types and is suppressed in the skip-serial/batch-valuation branch. A higher-level posting may also supply a hint on other movement types.

If withdrawal exhausts all layers and negative stock is permitted, create a negative layer for the shortage at nonzero outgoing hint or last selected rate. When the queue starts empty, obtain a fallback rate if zero is disallowed. For an incoming different rate against a negative tail, a receipt leaving quantity negative or exactly zero preserves the previous rate. Crossing above zero replaces the tail with the excess at the incoming rate. Quantities of magnitude strictly below 10⁻⁷ are set to zero by the layer helper. If removal empties the stored queue, the ledger wrapper can retain a zero-quantity layer with an available rate for subsequent reads. The helper's empty list and the persisted ledger representation have different purposes. [Layer algorithms](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/valuation.py) · [Layer regression cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/tests/test_valuation.py) · [Integrated positive FIFO case](../integrated/README.md)
