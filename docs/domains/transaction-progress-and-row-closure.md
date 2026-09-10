# Transaction progress and row closure

## Responsibility

This policy connects source commitments to submitted downstream execution. Quantities and amounts are updated at source-row level, then summarised to parent percentages and business statuses. It is shared across buying, selling, delivery, receipt, billing and related operations. A replacement needs source-row identity and document lifecycle state to reproduce the result.

The governing source is source-artifact-0d529ad6588b0d95c1d7 lines 204–260 and source-artifact-0d529ad6588b0d95c1d7 lines 596–780.

## Recalculation order

On updating prior-document progress, validate closed source rows first, recompute affected quantities or amounts, then validate the resulting quantities. On submission, include the current transaction in the contributing set even where it has not yet reached its final stored submitted state. On cancellation, exclude it. Include any explicitly configured second source, such as an alternate transaction capable of fulfilling the same source row.

Recompute totals from qualifying descendants rather than adding a blind increment. This preserves the relationship under amendments, cancellation and repeated recalculation. It does not, by itself, prove that every calling service serialises concurrent submissions correctly; test the complete service transaction.

## Parent percentage formula

For a given progress measure, let each row have an expected magnitude and a completed magnitude. Use absolute values so return rows do not incorrectly cancel ordinary progress. Clamp each completed magnitude to that row's expected magnitude. A surplus on one row cannot satisfy a shortage on another.

When closure applies to the measure, remove closed rows from the calculation basis. If this removes every row, fall back to the full row set and report actual progress. If an explicit exclusion filter removes every row, the helper returns one hundred percent. Otherwise a zero total expected magnitude returns zero percent.

`completion percentage = round to six decimal places (100 × sum of clamped completed magnitudes ÷ sum of expected magnitudes)`.

The common status helper calls a measure not completed below 0.001 percent, fully completed at or above 99.999999 percent, and partly completed otherwise. One separate zero-value billing path uses a strict greater-than comparison for its full-billing label. Preserve this boundary distinction if reproducing that path exactly. Evidence: source-artifact-0d529ad6588b0d95c1d7 lines 674–744, source-artifact-0d529ad6588b0d95c1d7 lines 787–835.

| Expected rows | Completed rows | Closed rows | Result |
|---|---|---|---|
| 10 and 10 | 10 and 0 | Neither | 50 percent |
| 10 and 10 | 10 and 0 | Second | 100 percent against the remaining open commitment |
| 10 and 10 | 10 and 0 | Both | 50 percent actual progress, with the parent closed |
| 10 and 10 | 15 and 0 | Neither | 50 percent because the first row is clamped to 10 |
| −10 and −10 | −5 and 0 | Neither | 25 percent by magnitude |
| 0 and 0 | 0 and 0 | Neither | 0 percent without the explicit all-excluded special case |

These are derived arithmetic examples of the reviewed formula. The first two also correspond to source acceptance tests. Evidence: source-artifact-6fb9332d68977fc04e99 lines 58–73.

## Closing and reopening rows

Supported parents are sales orders, purchase orders, delivery records and purchase receipts. The actor needs submission permission, the parent must already be submitted, and at least one row identifier must be selected. The close value is normalised to a boolean representation. Unchanged or nonmatching selections produce no change after the initial checks.

Before closing, each changed row must have something still pending under its parent's policy. A fully settled row cannot be closed. Parent-specific close validation runs before row flags change. After changed rows are persisted, the parent recomputes its consequences. Closing every row closes the parent. Reopening a row reopens a closed parent through its normal reopening operation; reopening a sales order therefore also reaches its normal credit-check path.

Reopening the parent while every row is still closed is rejected. Amendments start with all row-closure flags cleared. Packed components follow the closure of the parent commercial row. Evidence: source-artifact-a01f1e6932aab5fcb6dd lines 18–145.

Closing a row changes remaining commitments and available follow-up actions. A purchase order row can release its outstanding ordered quantity; a sales order row can release reserved quantity. Neither is evidence of a physical stock movement or settlement of a monetary debt.

For received but unbilled rows, closing can set the parent closed while received progress remains one hundred percent and billed progress remains zero. Closing a return row does not alter the original transaction's returned quantity. Evidence: source-artifact-6fb9332d68977fc04e99 lines 49–56, source-artifact-6fb9332d68977fc04e99 lines 134–149, source-artifact-35e82564b916f38157e1 lines 220–248.

## Closed rows in editing and mapping

A mapping operation must omit a closed source row. A previously constructed draft referencing a row that is subsequently closed must be rejected when submitted. The guard checks current source state, not only what was true when the draft was created.

When an item-edit request omits a closed row because the form hides it, omission must not delete that row. A request attempting to change a closed row must fail. A complete request that includes it unchanged is accepted. Evidence: source-artifact-6fb9332d68977fc04e99 lines 182–197, source-artifact-d76d733e00832bbc7b04 lines 59–95.

## Over-fulfilment and overbilling

The helper checks only configured target measures. Quantity-overflow lookups additionally restrict to stock products; this is not a universal quantity rule for every service product. Ordinary rows reject negative quantities, and return rows reject positive quantities under the reviewed validation path. Zero is not rejected merely by those sign checks. Negative prices depend on separate buying and selling settings.

For a nonzero expected amount or quantity, compute:

`overflow percentage = 100 × (completed value − expected value) ÷ expected value`.

An allowance is exceeded when overflow percentage minus configured allowance is greater than 0.01 percentage points. The maximum permitted value shown to the operator is expected value multiplied by one plus allowance divided by one hundred. A configured privileged role can turn the excess into a warning. Internal-party amount checks have explicit exceptions. Pick-list progress uses zero allowance. A separate no-allowance path compares the absolute excess with 0.01 rather than applying the percentage threshold.

A zero per-product allowance is treated as absent and falls back to the global allowance. Therefore zero does not necessarily mean forbid all excess when the global default permits it. Allowance caches reset for each configuration block to avoid using a previous block's settings. Evidence: source-artifact-0d529ad6588b0d95c1d7 lines 327–488, source-artifact-0d529ad6588b0d95c1d7 lines 490–547, source-artifact-0d529ad6588b0d95c1d7 lines 850–905.

## Status precedence

Status rules are evaluated in reverse declaration order, and the first matching rule wins. This matters when on-hold, closed, cancelled and completion conditions overlap. Do not derive status from percentages alone or impose a universal precedence across document types. For example, the sales and purchase order declarations place their manual overrides in different relative positions. Evidence: source-artifact-0d529ad6588b0d95c1d7 lines 22–191, source-artifact-0d529ad6588b0d95c1d7 lines 283–325.

## Acceptance obligations

Verify every numeric row above; close and reopen one row; close all rows; block reopening an all-closed parent; block processing a newly closed source through an older draft; preserve closed rows omitted from an edit request; clear closure on amendment; preserve original return progress; test allowance boundaries and role override; and run two competing submissions against the same remaining quantity.
