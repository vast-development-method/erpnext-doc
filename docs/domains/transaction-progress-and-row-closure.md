# Transaction progress and row closure

## Responsibility

This policy connects source commitments to submitted downstream execution. Quantities and amounts are updated at source-row level, then summarised to parent percentages and business statuses. It is shared across buying, selling, delivery, receipt, billing and related operations. A replacement needs source-row identity and document lifecycle state to reproduce the result.

The [transaction-progress calculations](../../schemas/mathematics/transaction-progress-calculations.json) define the corresponding numeric contracts. Persistence is specified by [sales order rows](../../schemas/data/record-types/sales_order_item.json), [purchase order rows](../../schemas/data/record-types/purchase_order_item.json), [delivery rows](../../schemas/data/record-types/delivery_note_item.json) and [purchase receipt rows](../../schemas/data/record-types/purchase_receipt_item.json). The row link, closure flag, expected quantity or amount, completed counters and parent lifecycle must all remain available when recalculating progress.

## Recalculation order

On updating prior-document progress, validate closed source rows first, recompute affected quantities or amounts, then validate the resulting quantities. On submission, include the current transaction in the contributing set even where it has not yet reached its final stored submitted state. On cancellation, exclude it. Include any explicitly configured second source, such as an alternate transaction capable of fulfilling the same source row.

Recompute totals from qualifying descendants rather than adding a blind increment. This preserves the relationship under amendments, cancellation and repeated recalculation. It does not, by itself, prove that every calling service serialises concurrent submissions correctly; test the complete service transaction.

## Parent percentage formula

For a given progress measure, let each row have an expected magnitude and a completed magnitude. Use absolute values so return rows do not incorrectly cancel ordinary progress. Clamp each completed magnitude to that row's expected magnitude. A surplus on one row cannot satisfy a shortage on another.

When closure applies to the measure, remove closed rows from the calculation basis. If this removes every row, fall back to the full row set and report actual progress. If an explicit exclusion filter removes every row, the helper returns one hundred percent. Otherwise a zero total expected magnitude returns zero percent.

`completion percentage = round to six decimal places (100 × sum of clamped completed magnitudes ÷ sum of expected magnitudes)`.

The common status helper calls a measure not completed below 0.001 percent, fully completed at or above 99.999999 percent, and partly completed otherwise. One separate zero-value billing path uses a strict greater-than comparison for its full-billing label. Preserve this boundary distinction if reproducing that path exactly. 

| Expected rows | Completed rows | Closed rows | Result |
|---|---|---|---|
| 10 and 10 | 10 and 0 | Neither | 50 percent |
| 10 and 10 | 10 and 0 | Second | 100 percent against the remaining open commitment |
| 10 and 10 | 10 and 0 | Both | 50 percent actual progress, with the parent closed |
| 10 and 10 | 15 and 0 | Neither | 50 percent because the first row is clamped to 10 |
| −10 and −10 | −5 and 0 | Neither | 25 percent by magnitude |
| 0 and 0 | 0 and 0 | Neither | 0 percent without the explicit all-excluded special case |

These examples are complete calculation fixtures: compare the rounded percentage and the independent closure state, rather than substituting one for the other. 

## Closing and reopening rows

Supported parents are sales orders, purchase orders, delivery records and purchase receipts. The actor needs submission permission, the parent must already be submitted, and at least one row identifier must be selected. The close value is normalised to a boolean representation. Unchanged or nonmatching selections produce no change after the initial checks.

Before closing, each changed row must have something still pending under its parent's policy. A fully settled row cannot be closed. Parent-specific close validation runs before row flags change. After changed rows are persisted, the parent recomputes its consequences. Closing every row closes the parent. Reopening a row reopens a closed parent through its normal reopening operation; reopening a sales order therefore also reaches its normal credit-check path.

Reopening the parent while every row is still closed is rejected. Amendments start with all row-closure flags cleared. Packed components follow the closure of the parent commercial row. 

Closing a row changes remaining commitments and available follow-up actions. A purchase order row can release its outstanding ordered quantity; a sales order row can release reserved quantity. Neither is evidence of a physical stock movement or settlement of a monetary debt.

For received but unbilled rows, closing can set the parent closed while received progress remains one hundred percent and billed progress remains zero. Closing a return row does not alter the original transaction's returned quantity. 

## Closed rows in editing and mapping

A mapping operation must omit a closed source row. A previously constructed draft referencing a row that is subsequently closed must be rejected when submitted. The guard checks current source state, not only what was true when the draft was created.

When an item-edit request omits a closed row because the form hides it, omission must not delete that row. A request attempting to change a closed row must fail. A complete request that includes it unchanged is accepted. 

## Over-fulfilment and overbilling

The helper checks only configured target measures. Quantity-overflow lookups additionally restrict to stock products; this is not a universal quantity rule for every service product. Ordinary rows reject negative quantities, and return rows reject positive quantities under the reviewed validation path. Zero is not rejected merely by those sign checks. Negative prices depend on separate buying and selling settings.

For a nonzero expected amount or quantity, compute:

`overflow percentage = 100 × (completed value − expected value) ÷ expected value`.

An allowance is exceeded when overflow percentage minus configured allowance is greater than 0.01 percentage points. The maximum permitted value shown to the operator is expected value multiplied by one plus allowance divided by one hundred. A configured privileged role can turn the excess into a warning. Internal-party amount checks have explicit exceptions. Pick-list progress uses zero allowance. A separate no-allowance path compares the completed value minus expected value directly with 0.01, rather than applying the percentage threshold. Its candidate lookup already selects only completed values greater than expected values; it is not an absolute-value comparison of arbitrary signed inputs.

A zero per-product allowance is treated as absent and falls back to the global allowance. Therefore zero does not necessarily mean forbid all excess when the global default permits it. Allowance caches reset for each configuration block to avoid using a previous block's settings. 

## Status precedence

Status rules are evaluated in reverse declaration order, and the first matching rule wins. This matters when on-hold, closed, cancelled and completion conditions overlap. Do not derive status from percentages alone or impose a universal precedence across document types. For example, the sales and purchase order declarations place their manual overrides in different relative positions. 

## Concrete status decision tables

Evaluate each table from highest to lowest precedence and stop at the first match. Lifecycle state and manually held or closed status are separate inputs; the rules below reproduce even combinations that an ordinary screen may prevent.

| Sales order priority | Match | Result |
|---|---|---|
| 1 | Existing business status is On Hold | On Hold |
| 2 | Existing status is Closed and lifecycle is not cancelled | Closed |
| 3 | Lifecycle is cancelled | Cancelled |
| 4 | Submitted, billed percentage at least 100, and delivery percentage at least 100 or delivery skipped | Completed |
| 5 | Submitted and advance-payment state is Requested | To Pay |
| 6 | Submitted, delivery below 100, billing at least 100, and delivery not skipped | To Deliver |
| 7 | Submitted, billing below 100, and delivery at least 100 or delivery skipped | To Bill |
| 8 | Submitted, both delivery and billing below 100 | To Deliver and Bill |
| 9 | No earlier match | Draft |

| Purchase order priority | Match | Result |
|---|---|---|
| 1 | Existing status is Closed and lifecycle is not cancelled | Closed |
| 2 | Existing business status is On Hold | On Hold |
| 3 | Lifecycle is cancelled | Cancelled |
| 4 | Existing status is Delivered | Delivered |
| 5 | Submitted, receipt percentage at least 100 and billing exactly 100 | Completed |
| 6 | Submitted and advance-payment state is Initiated | To Pay |
| 7 | Submitted, receipt and billing both below 100 | To Receive and Bill |
| 8 | Submitted, receipt below 100 and billing exactly 100 | To Receive |
| 9 | Submitted, receipt at least 100 and billing below 100 | To Bill |
| 10 | No earlier match | Draft |

The strict equality for purchase-order billing differs from sales-order billing's at-least comparison. The percentages' ordinary calculation caps rows, but an independently stored exceptional value above 100 cannot be assumed to choose the same status in both tables. The On Hold rules do not themselves check lifecycle, so a stale hold value can precede a cancelled match; cancellation services must update their input status consistently.

For delivery records, precedence is Closed when not cancelled, Cancelled, an unbilled return, fully returned, exactly fully billed, partly billed, unbilled, then Draft. For purchase receipts, precedence is Closed when not cancelled, Cancelled, Completed, fully returned, an unbilled return, partly billed, unbilled, then Draft. A submitted ordinary purchase receipt with zero total and not fully returned is Completed even while billing percentage is zero. Purchase receipt completion also accepts billing at least 100; delivery completion checks exactly 100.

## Failure outcomes and numeric boundary fixtures

| Operation or input | Required observable outcome |
|---|---|
| Expected quantity 100, completed 105, allowance 5 percent | Within allowance; permitted maximum displayed as 105 |
| Expected 100, completed 105.009, allowance 5 percent | Excess above allowance is 0.009 percentage points; percentage check does not reject |
| Expected 100, completed 105.02, allowance 5 percent | Excess above allowance is 0.02 percentage points; reject unless the applicable privileged role makes it a warning |
| No-allowance rule, completed minus expected 0.01 | Not rejected by the strict greater-than check |
| No-allowance rule, completed minus expected 0.011 | Rejected |
| Percentage 0.000999 | Not completed |
| Percentage 0.001 | Partly completed |
| Percentage 99.999999 | Fully completed through common helper; still partly billed through the separate zero-value billing label path |
| Close an already closed selected row | No additional quantity change after permission and lifecycle validation |
| Close one invalid fully settled row together with an eligible row | Reject before persisting closure flags; no partial closure |
| Recalculate after cancelling one of two receipts | Recompute using only the remaining qualifying receipt, not an extra negative receipt invented for progress |

For a purchase order of ten units, receive six and close its remaining commitment. Actual received quantity stays six and warehouse quantity remains the six received. When every row is closed, progress reports sixty percent actual receipt while the parent is Closed. Reopening makes four outstanding units available again and cannot recreate the earlier six-unit receipt. A customer invoice or supplier debt already posted remains collectible or payable after order closure.

Submission failure must leave progress, stock, financial entries and closure flags at their pre-operation state. Repeated recalculation must converge on the same counters. A concurrency acceptance case starts two submissions each requesting the final available remainder; whichever business transaction commits first determines the remaining allowed quantity for the second. This is a required replacement consistency property, not a claim that a read-only arithmetic helper alone provides locking.

## Acceptance obligations

Verify every numeric row above; close and reopen one row; close all rows; block reopening an all-closed parent; block processing a newly closed source through an older draft; preserve closed rows omitted from an edit request; clear closure on amendment; preserve original return progress; test allowance boundaries and role override; and run two competing submissions against the same remaining quantity.

## Financial and physical closure invariants

Row closure must preserve actual received, delivered, billed and returned contributions while changing the remaining commitment selected by the parent policy. For a ten-unit purchase order received six units at 12.00, closing the last four units leaves warehouse quantity six and received stock value 72.00. If the six units are already invoiced, supplier debt remains 72.00 until settled or credited. If they are not invoiced, the 72.00 received-but-unbilled clearing balance remains. A close operation that credits inventory or debits supplier payable merely to make the order look completed is incorrect.

The local calculation catalog now records the exact threshold, zero-value, all-excluded and all-closed cases as data. Its `closed_order_preserves_posted_effects` example separates ordered quantity ten, actual quantity six, closed parent, sixty percent actual progress, released commitment four and unchanged recognized stock or liability. This cross-check prevents a reader from equating a closed business status with one hundred percent physical performance or financial settlement.
