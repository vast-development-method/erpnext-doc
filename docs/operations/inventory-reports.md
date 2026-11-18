# Inventory reports and reconciliation

A warehouse balance shows how much stock is present. The projected-stock report also includes future receipts and existing commitments. Stock ageing prices and groups the remaining receipt quantities by age. The stock-to-accounts report identifies vouchers whose physical and financial valuation disagree. Use the same company, stock units and date scope when comparing these reports.

## Projected quantity and shortage

The balance for a product at a warehouse carries eight planning counters in stock units. Calculate projected quantity by adding on-hand, ordered, requested and planned production quantities, then subtracting sales-order reservations, production requirements, subcontract requirements and production-plan requirements. Changing a counter recalculates the projection with the other current counters. An explicit reservation tied to identified physical stock answers a different question and must not be subtracted twice.

For the displayed projection the report also deducts applicable point-of-sale reserved quantities. Select eligible, enabled stock items with warehouse balance rows and no end-of-life date on or before today. A product-group filter includes descendant groups. Show the reorder threshold and lot for this product and warehouse. Report a shortage only when a threshold or lot exists and threshold exceeds displayed projection. The shortage is threshold less displayed projection. The [replenishment decision](replenishment.md) can still trigger a request at exact equality.

For example, 20 on hand, 8 ordered, 3 requested and 5 planned give 36 before commitments. Deduct 10 sales, 4 production, 3 subcontract and 2 production-plan units. The warehouse projection is 17. Deduct a point-of-sale claim of 2 to display 15. A threshold of 18 yields a reported shortage of 3. That amount is neither a warehouse movement nor necessarily the purchase lot size.

## Ageing at the report cutoff

Retain dated quantities and values for remaining receipt portions. A partial issue consumes the relevant slots. A transfer can carry the receipt age to a destination. A tracked serial contributes one unit for its dated identity. Distinguish batch-specific valuation from a pooled item valuation in selecting remaining quantities. A valuation-only adjustment can change the value on a slot while preserving its receipt date. A report that replaces every receipt date with the last movement date understates the age of transferred stock.

Let $q_i$ be remaining quantity in slot $i$ and $a_i$ the whole calendar days from its receipt date to the cutoff. Weighted average age is $\sum q_i a_i / \sum q_i$, rounded to two decimals, or zero for a zero denominator. Display the oldest and youngest ages separately. Omit products whose net quantity rounds to zero at the configured stock precision, and omit entries without dated slots.

Age bands accept numeric day thresholds in ascending order. The usual thresholds are 30, 60 and 90 days. Place each slot in the first band whose upper bound is at least its age, otherwise use the last open-ended band. Sum quantities and values in each band at configured precision. For 2 pieces worth 16 received 30 days ago and 3 pieces worth 36 received 40 days ago, average age is 36 days, oldest is 40 and youngest is 30. The first band holds 2 and 16. The second holds 3 and 36. With no further activity the next day moves the first two units beyond the 30-day boundary.

## Stock value versus financial postings

Require a company with perpetual inventory. Use an inclusive cutoff that defaults to the current business date and an optional inclusive start no later than the cutoff. Use effective, noncancelled movements in both ledgers. Group by the combination of voucher type and voucher identifier. If one stock account is selected, restrict stock movements to its applicable warehouses and financial entries to that account. Otherwise use the company's stock accounts.

| Quantity compared | Calculation |
|---|---|
| Stock value movement | Sum of stock-value differences on the voucher's inventory ledger rows |
| Account value movement | Debits less credits on included financial rows in account currency |
| Difference | Stock movement less account movement. For a financial-only voucher the stock movement is zero. |

For a voucher present on the stock side, include it only when the absolute difference is **greater than 0.10**. A difference of exactly 0.10 is below this report's inclusion test. This rule filters the report. Posting still requires balanced monetary effects under the accounting policy. Independently include financial vouchers with no corresponding stock voucher. Correct an identified discrepancy through its owning business event or valuation correction. Editing the report cannot settle it.

For a receipt with stock value increase 50 and an account debit of 48, report a positive difference of 2. For a standalone ledger credit of 7 on an inventory account, the account movement is −7, the stock movement is zero and the reported difference is +7. A transfer between warehouses sharing an account may correctly net to zero while both warehouse legs remain visible on the movement ledger.
