# Transaction progress and row closure

## Responsibility

This policy connects source commitments to submitted downstream execution. Quantities and amounts are updated at source-row level, then summarised to parent percentages and business statuses. It is shared across buying, selling, delivery, receipt, billing and related operations. A replacement needs source-row identity and document lifecycle state to reproduce the result.

The [transaction-progress calculations](../calculations/README.md) define the corresponding numeric contracts. Persistence is specified by sales order rows, purchase order rows, delivery rows and purchase receipt rows. Persist the source-row link, expected quantity or amount, completed counters and parent lifecycle. Independent row closure additionally requires an explicit row flag and operations to close or reopen that row.

## Recalculation order

The core progress service recomputes affected quantities or amounts and then validates them. A deployment offering independent row closure also checks the row flag when admitting a downstream operation. On submission, include the current transaction in the contributing set even where it has not yet reached its final stored submitted state. On cancellation, exclude it. Include any explicitly configured second source, such as an alternate transaction capable of fulfilling the same source row.

Recompute totals from qualifying descendants rather than adding a blind increment. This preserves the relationship under amendments, cancellation and repeated recalculation. It does not, by itself, prove that every calling service serialises concurrent submissions correctly. Test the complete service transaction.

## Parent percentage formula

For a given progress measure, let each row have an expected magnitude and a completed magnitude. Use absolute values so return rows do not incorrectly cancel ordinary progress. Clamp each completed magnitude to that row's expected magnitude. A surplus on one row cannot satisfy a shortage on another.

Read every item row for the selected parent type and identity. An empty set or a zero sum of expected magnitudes yields zero. Round the computed value to six decimal places. For the stored parent percentage, snap values of 99.999999% or higher to 100%.

`completion percentage = round(100 × sum(min(abs(completed), abs(expected))) / sum(abs(expected)), 6)`

| Expected rows | Completed rows | Measured percentage |
|---|---|---:|
| 10 and 10 | 10 and 0 | 50% |
| 10 and 10 | 15 and 0 | 50% |
| −10 and −10 | −5 and 0 | 25% |
| 0 and 0 | 0 and 0 | 0% |

The common status labels treat less than 0.001% as uncompleted, at least 99.999999% as complete, and the interval between them as partial. The zero-value billing path uses the same inclusive full boundary.

## Close and reopen a document

The business status belongs to the parent. Closing an order stops its remaining commitment and preserves all posted quantities, stock values, invoices and settlements. The core sales close checks the stored modification time and refuses an order with an active explicit stock reservation. Unreserve first. A successful status change refreshes bin commitments, linked subcontracting status, blanket-order consumption and notifications. Reopening checks any applicable blanket-order limit. Resetting a submitted sales order through its reopening path also checks the customer's credit limit. The purchase order refreshes ordered quantities and linked requests under its own status operation. Delivery notes and purchase receipts expose their own parent status update.

A purchase order for ten units with six received remains 60% received after closure. An independent per-row close capability requires its own field, mapping rule and authorization. The standard order and delivery/receipt item declarations supply no row close flag.

## Closing and reopening rows

**Optional row-closure capability.** A deployment implementing this extension exposes row-level actions on the following submitted parents. The core parent-close action above remains available independently.

Supported parents are sales orders, purchase orders, delivery records and purchase receipts. The actor needs submission permission, the parent must already be submitted, and at least one row identifier must be selected. The close value is normalised to a boolean representation. Unchanged or nonmatching selections produce no change after the initial checks.

Before closing, each changed row must have something still pending under its parent's policy. A fully settled row cannot be closed. Parent-specific close validation runs before row flags change. After changed rows are persisted, the parent recomputes its consequences. Closing every row closes the parent. Reopening a row reopens a closed parent through its normal reopening operation. Reopening a sales order therefore also reaches its normal credit-check path.

Reopening the parent while every row is still closed is rejected. Amendments start with all row-closure flags cleared. Packed components follow the closure of the parent commercial row.

Closing a row changes remaining commitments and available follow-up actions. A purchase order row can release its outstanding ordered quantity. A sales order row can release reserved quantity. Neither is evidence of a physical stock movement or settlement of a monetary debt.

For received but unbilled rows, closing can set the parent closed while received progress remains one hundred percent and billed progress remains zero. Closing a return row does not alter the original transaction's returned quantity.

## Closed rows in editing and mapping

These mapping and amendment rules apply when independent row closure is enabled. For measures configured to exclude closed rows, use the remaining open rows. If all are closed, measure actual progress over all of them. If an explicit exclusion filter removes every row, that optional filtered measure reports 100%. With two ten-unit rows and ten units completed on the first, closing only the second makes open-commitment progress 100%. Closing both yields 50% actual progress.

A mapping operation must omit a closed source row. A previously constructed draft referencing a row that is subsequently closed must be rejected when submitted. The guard checks current source state, not only what was true when the draft was created.

When an item-edit request omits a closed row because the form hides it, omission must not delete that row. A request attempting to change a closed row must fail. A complete request that includes it unchanged is accepted.

## Over-fulfilment and overbilling

The calculation checks only configured target measures. Quantity-overflow lookups additionally restrict to stock products. This is not a universal quantity rule for every service product. Ordinary rows reject negative quantities, and return rows reject positive quantities under the validation path. Zero is not rejected merely by those sign checks. Negative prices depend on separate buying and selling settings.

For a nonzero expected amount or quantity, compute:

`overflow percentage = 100 × (completed value − expected value) ÷ expected value`.

An allowance is exceeded when overflow percentage minus configured allowance is greater than 0.01 percentage points. The maximum permitted value shown to the operator is expected value multiplied by one plus allowance divided by one hundred. A configured privileged role can turn the excess into a warning. Internal-party amount checks have explicit exceptions. Pick-list progress uses zero allowance. A separate no-allowance path compares the completed value minus expected value directly with 0.01, rather than applying the percentage threshold. Its candidate lookup already selects only completed values greater than expected values. It is not an absolute-value comparison of arbitrary signed inputs.

A zero per-product allowance is treated as absent and falls back to the global allowance. Therefore zero does not necessarily mean forbid all excess when the global default permits it. Allowance caches reset for each configuration block to avoid using a previous block's settings.

## Status precedence

Status rules are evaluated in reverse declaration order, and the first matching rule wins. This matters when on-hold, closed, cancelled and completion conditions overlap. Do not derive status from percentages alone or impose a universal precedence across document types. For example, the sales and purchase order declarations place their manual overrides in different relative positions.

## Concrete status decision tables

Evaluate each table from highest to lowest precedence and stop at the first match. Lifecycle state and manually held or closed status are separate inputs. The rules below reproduce even combinations that an ordinary screen may prevent.

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

The strict equality for purchase-order billing differs from sales-order billing's at-least comparison. The percentages' ordinary calculation caps rows, but an independently stored exceptional value above 100 cannot be assumed to choose the same status in both tables. The On Hold rules do not themselves check lifecycle, so a stale hold value can precede a cancelled match. Cancellation services must update their input status consistently.

For delivery records, precedence is Closed when not cancelled, Cancelled, an unbilled return, fully returned, exactly fully billed, partly billed, unbilled, then Draft. For purchase receipts, precedence is Closed when not cancelled, Cancelled, Completed, fully returned, an unbilled return, partly billed, unbilled, then Draft. A submitted ordinary purchase receipt with zero total and not fully returned is Completed even while billing percentage is zero. Purchase receipt completion also accepts billing at least 100. Delivery completion checks exactly 100.

## Failure outcomes and numeric boundary fixtures

| Operation or input | Required observable outcome |
|---|---|
| Expected quantity 100, completed 105, allowance 5 percent | Within allowance. Permitted maximum displayed as 105 |
| Expected 100, completed 105.009, allowance 5 percent | Excess above allowance is 0.009 percentage points. Percentage check does not reject |
| Expected 100, completed 105.02, allowance 5 percent | Excess above allowance is 0.02 percentage points. Reject unless the applicable privileged role makes it a warning |
| No-allowance rule, completed minus expected 0.01 | Not rejected by the strict greater-than check |
| No-allowance rule, completed minus expected 0.011 | Rejected |
| Percentage 0.000999 | Not completed |
| Percentage 0.001 | Partly completed |
| Percentage 99.999999 | Fully completed in the common status helper and the zero-value billing path |
| Optional row closure · close an already closed selected row | No additional quantity change after permission and lifecycle validation |
| Optional row closure · close one invalid fully settled row together with an eligible row | Reject before persisting closure flags. No partial closure |
| Recalculate after cancelling one of two receipts | Recompute using only the remaining qualifying receipt, not an extra negative receipt invented for progress |

For a purchase order of ten units, receive six and close its remaining commitment. Actual received quantity stays six and warehouse quantity remains the six received. The generic measure reports sixty percent actual receipt while the parent is Closed. Reopening makes four outstanding units available again and cannot recreate the earlier six-unit receipt. A customer invoice or supplier debt already posted remains collectible or payable after order closure.

Submission failure must leave progress, stock, financial entries and closure flags at their pre-operation state. Repeated recalculation must converge on the same counters. A concurrency acceptance case starts two submissions each requesting the final available remainder. Whichever business transaction commits first determines the remaining allowed quantity for the second. Apply the authority check and the quantity mutation to the same protected predecessor.

## Acceptance obligations

For the core workflow, test the numeric boundaries, close and reopen the parent, and check both reservation refusal and the later authorized close. For the optional row-closure capability, close and reopen one row. Close all rows. Block reopening an all-closed parent. Block processing a newly closed source through an older draft. Preserve closed rows omitted from an edit request. Clear closure on amendment. Preserve original return progress. Test allowance boundaries and role override. And run two competing submissions against the same remaining quantity.

## Financial and physical closure invariants

Closing a document or an independently closable row must preserve actual received, delivered, billed and returned contributions while changing the remaining commitment selected by the parent policy. For a ten-unit purchase order received six units at 12.00, closing the last four units leaves warehouse quantity six and received stock value 72.00. If the six units are already invoiced, supplier debt remains 72.00 until settled or credited. If they are not invoiced, the 72.00 received-but-unbilled clearing balance remains. A close operation that credits inventory or debits supplier payable merely to make the order look completed is incorrect.

The [calculation contracts](../calculations/README.md) include zero-value, all-excluded and all-closed order cases. Closing the remaining four units of a ten-unit order after receiving six preserves sixty percent actual fulfilment and the posted inventory and liability amounts.

## Billing a delivery after a price change

On a delivery, sum line amounts and returned quantity times the line rate. When the total returned value is below the original total, subtract each line's returned value from its reference amount. Otherwise use each line's original amount. Apply the parent percentage formula to the billed amount and reference amount of every delivery row. A direct invoice for ten units at 8 against ten delivered at 10 contributes 80 against 100 and reports **80% billed**. Six invoiced at 10 report 60%. A delivery created against an existing invoice without an order link takes its own row amount as billed. For invoice amounts linked only to an order line, allocate the submitted non-stock-updating invoice amounts across eligible delivery rows in posting date, time and document-name order.

For a submitted reference order or delivery with zero company-currency net total, non-return sales invoice submission and cancellation trigger a separate quantity calculation. Sum the referenced quantities and the qualifying submitted invoice quantities. Divide the lesser of the two by the reference quantity, with zero on a zero divisor. Round that ratio to two decimals under the configured rounding rule before multiplying by 100. Apply the same inclusive full-percentage threshold. Eight of ten zero-value units gives 80%, one of three gives 33%, and 996 of 1,000 gives 100%. The zero-value fallback therefore has coarser resolution than ordinary monetary progress.

A deployment can implement an additional quantity-inclusive progress measure. Under that option, compare each line's capped billed amount with its reference amount multiplied by the capped invoiced share of its net quantity and take the larger. Zero net quantity contributes zero from quantity. Combine those amounts over the selected reference values, round to six places and use zero when their total is zero. Ten units billed at 8 against ten at 10 then give **100% quantity-inclusive progress** while the ordinary monetary billing measure remains **80%**. An implementation must identify which measure it is displaying. Neither measure sets the receivable balance.

## Linked specifications

- **Calculation and acceptance cases** · [transaction-progress calculations](../../schemas/mathematics/transaction-progress-calculations.json)
- **Record definitions** · [sales order rows](../../schemas/data/record-types/sales_order_item.json) · [purchase order rows](../../schemas/data/record-types/purchase_order_item.json) · [delivery rows](../../schemas/data/record-types/delivery_note_item.json) · [purchase receipt rows](../../schemas/data/record-types/purchase_receipt_item.json)
