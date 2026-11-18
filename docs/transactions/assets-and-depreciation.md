# Assets and depreciation

## Asset identity and financial histories

A fixed asset is an individually identified capital resource associated with a company, product, asset category, acquisition or capitalization, available-for-use date, location or custodian and financial-book policies. An asset's financial history includes cost, additional capitalization, accumulated depreciation, expected residual value, schedule revisions, depreciation journals, value adjustments, sale, scrap and restoration. Asset identity is not interchangeable with product identity: several individually controlled assets can share one product master.

The depreciation schedule is a separate persistent record with asset identity, financial-book identity, method, frequency in months, total cycles, starting date, current carrying value, residual value, applicable rate, prorating and shift choices, lifecycle state, and ordered schedule rows. Each row retains schedule date, depreciation amount, accumulated depreciation, optional shift and posted journal reference. A second active schedule for the same asset and financial book is rejected in a test. A completed posting link distinguishes immutable recognized history from future forecast.

Initial recognition of an already owned asset records its opening financial position. Its opening accumulated depreciation and previously completed periods matter when computing future charges. Similarly, extending useful life or increasing asset value after repair changes future expectations without authorizing edits to already posted depreciation.

## Schedule regeneration

Regeneration begins by loading the asset and selected financial-book policy, retaining existing schedule rows with journal references and discarding only the future unposted portion. It then initializes current carrying value, remaining months and cycles, prorating indicators, next dates, and financial-year context. Each new row calculates a candidate charge, adjusts for disposal or partial periods, rounds it to asset monetary precision, updates remaining value, checks residual value and appends a positive charge. Accumulated depreciation is reconstructed by respecting previously posted cumulative amounts and adding newly calculated future charges.

The schedule's anticipated future charges are not ledger balances. A forecast row without a posted journal must not be counted as recognized depreciation. The posting process links each actual journal to its schedule row. Acceptance must check both the asset carrying amount and the accumulated-depreciation account after posting and reversal.

## Straight-line method

Depreciable value is current value after depreciation less expected value after useful life. Under the fixed-period method, remaining periods equal remaining months divided by frequency in months. Each candidate charge is depreciable value divided by remaining periods. Prorating may add a final partial period. Final residual correction ensures that the last charge brings carrying value to the expected residual rather than leaving accumulated rounding error.

Derived fixed-period fixture: acquisition cost 12000.00, residual value 2000.00, five annual periods, no opening depreciation and no partial first period produce annual depreciation 2000.00 and closing carrying values 10000.00, 8000.00, 6000.00, 4000.00 and 2000.00. Debits to depreciation expense total 10000.00, credits to accumulated depreciation total 10000.00, and cost remains 12000.00 until disposal or a separately authorized value adjustment.

Under daily prorating, one policy divides remaining depreciable value by total remaining useful days. Another derives yearly depreciation by dividing depreciable value by remaining years, then divides that yearly amount by the number of days in the current depreciation financial year. The latter can produce different daily charges in leap and nonleap years while maintaining equal annual depreciation before rounding. Multiply daily amount by the inclusive number of depreciable days for each schedule interval. The first and final intervals depend on available-for-use date and schedule anchoring.

Settlement example. cost subject to depreciation 100000.00 over 24 monthly periods, available on 2020-01-01, first schedule 2020-01-31, daily prorating enabled, and annual-day denominator selected. January 2020 depreciation is 4234.97, February 2020 is 3961.75 and cumulative February amount is 8196.72. December 2020 cumulative amount is 49999.98. January 2021 charge is 4246.58. Final December 2021 charge is 4246.56 and cumulative depreciation reaches exactly 100000.00. These values show the leap-year divisor and final rounding correction; a fixed monthly 4166.67 does not reproduce this schedule.

## Shift-weighted depreciation

When shift weighting is selected and prior unposted schedule rows exist, each row has a shift name resolved to a configured numeric factor. Sum factors for unposted rows. Charge for a row is remaining depreciable value divided by total unposted factors, multiplied by that row's factor. Posted rows do not participate in the new denominator. Without an existing schedule to supply shift assignments, the initial amount uses ordinary remaining-period division.

Derived fixture: remaining depreciable value 600.00 and three unposted rows with factors one, two and three produce charges 100.00, 200.00 and 300.00. If the first row has already posted, it remains unchanged; any later change to the shift factors redistributes only the remaining depreciable value. A zero total factor is an explicit invalid-input acceptance case that needs runtime verification because the arithmetic itself divides by that sum.

## Declining-balance methods

The double-declining annual percentage is 200 divided by useful life in years. Useful life in years is total number of depreciation cycles multiplied by frequency in months, divided by twelve. Round the resulting rate to configured general numeric precision. A five-year life therefore gives 40 percent.

Written-down-value rate can be explicitly supplied. When calculating it, divide residual value by current asset carrying value, raise that ratio to one divided by remaining years, subtract from one, and multiply by 100. Remaining years uses unbooked periods times frequency plus life-extension months, divided by twelve. An explicit rate is preserved during validation; a supplied rate can also remain when residual value is zero. For residual 1000.00, current value 10000.00 and five years remaining, the derived annual percentage before rate rounding is approximately 36.90426555. At two rate places it is 36.90 percent, so residual correction remains necessary.

For non-daily declining methods, each new financial year calculates yearly depreciation as remaining carrying amount multiplied by annual rate divided by 100. The periodic charge is that annual amount multiplied by frequency divided by twelve. Subsequent periods in the same financial year reuse that periodic amount. This is yearly declining balance allocated across periods, not monthly compounding against the immediately previous month. With daily prorating, the financial-year charge is divided by the actual days in that financial year and multiplied by inclusive interval days.

Derived full-year double-declining fixture: cost 10000.00, five-year life, annual 40 percent, annual periods and residual 1000.00. Candidate charges are 4000.00, 2400.00, 1440.00 and 864.00, leaving 1296.00 before year five. The last raw 518.40 would breach residual, so final depreciation is 296.00 and closing carrying value is 1000.00. Earlier termination at residual suppresses further depreciation rows.

## Partial periods, disposal, and low-value assets

When disposal occurs on or before a planned schedule date, the interval begins after the last scheduled depreciation date or the applicable initial available-for-use date. A prorated charge is calculated through disposal, rounded, and appended at disposal date if positive; generation stops after that. First-period and final-period adjustments depend on month-end anchoring and any useful-life extension. An asset whose rounded first-period charge is not positive can be rejected as too small to depreciate over the selected number of cycles.

Residual correction applies when a final row would leave carrying value different from expected residual, or when any row would push value below residual. Add the difference between candidate remaining value and residual to the candidate depreciation, round, and stop further rows. This preserves cost less accumulated depreciation equal to residual under the intended completed schedule. Do not let a generic rounding routine erase the final remaining cent.

A manual schedule starts from straight-line generation. When saving a manual edit, each row must have a strictly positive charge and a date on or after the asset’s available-for-use date. Sum only rows without a journal entry. At carrying-value precision, this sum must equal current carrying value less the expected residual. Recompute accumulated depreciation after validating the total. Internally regenerated schedules follow their rescheduling path and skip these manual-edit checks. Submission also requires a submitted asset with depreciation enabled.

## Depreciation and disposal posting

Recognized depreciation debits the configured depreciation-expense account and credits the accumulated-depreciation account for the chosen asset category and company, retaining asset, schedule, financial book, cost center, date and dimensions. A sale or scrap first determines depreciation through disposal date and then removes the asset's financial position. Posting failures must leave the schedule's posting reference and status consistent with whether a journal was actually submitted. The detailed batch-failure and retry behaviour should be verified independently; the existence of a daily scheduler does not establish exactly-once posting.

For disposal, credit the fixed-asset account for gross asset value. Round net purchase amount plus capitalized additions plus net value adjustments to purchase-amount precision. For a depreciating asset, take the adjustment from the selected finance-book row, or the first finance-book row when no book was specified. A missing matching row contributes zero adjustment. For a nondepreciating asset, use its asset-level adjustment. Debit accumulated depreciation for gross asset value less the selected carrying value, rounded to purchase-amount precision. Selling amount less carrying value determines the gain or loss in the disposal account. The sales invoice or scrap journal supplies the remaining counter-entry.

For a purchase of 12,000.00 with capitalized additions of 2,000.00, an upward adjustment of 500.00 and a carrying value of 9,500.00, a sale for 10,000.00 credits fixed assets 14,500.00 and disposal gain 500.00. It debits accumulated depreciation 5,000.00 and receivables 10,000.00.

Derived sale fixture: cost 12000.00, accumulated depreciation 8000.00, carrying value 4000.00 and sale amount 4500.00 before sales tax. Disposal credits cost 12000.00, debits accumulated depreciation 8000.00 and credits disposal gain 500.00; the invoice debits customer receivable 4500.00. At sale amount 3500.00 the disposal account receives a 500.00 debit loss instead. A scrap with no proceeds debits disposal loss 4000.00, debits accumulated depreciation 8000.00 and credits cost 12000.00.

Restoration and sales returns need the prior disposal context, relevant depreciation journals and financial-book carrying amount. They cannot merely set an asset status back to active. The workflow includes regain, disposal reversal, depreciation cancellation and schedule reset paths. Their complete combination matrix with partial disposals, repairs, capitalization and multiple financial books is recorded as a remaining execution requirement rather than claimed as fully validated.

## Acceptance requirements

1. Reject duplicate active asset and financial-book schedules.
2. Reproduce the leap-year schedule values above and the final cumulative 100000.00.
3. Reproduce fixed straight-line, weighted-shift and annual declining examples at declared precision.
4. Rebuilding a schedule after a posted row retains its date, amount, accumulated amount and journal link.
5. Changing future shift factors or extending remaining life affects only unposted charges.
6. A disposal mid-period records required prorated depreciation before cost removal and gain or loss.
7. Completed depreciation never leaves carrying value below the configured residual.
8. Cancelling or reversing depreciation restores expense, accumulated depreciation, asset carrying value and schedule linkage consistently.
9. A second financial book can have a different method and schedule without silently duplicating another book's postings in a report that includes only one book.
10. Failed journal submission cannot leave a schedule row falsely marked as posted.

The exact arithmetic fixtures do not execute every schedule anchor, manual edit, composite capitalization or restoration combination. The additional value-adjustment and capitalized-repair contracts below establish their observed financial mechanics and identify specific compatibility anomalies.

## Value adjustment is a separate accounting event

A value-adjustment record identifies the asset, financial book, effective date, current carrying value, proposed new value, signed difference, difference account, dimensions and journal. Reject a disposed asset, a negative new value, a date before acquisition, or a date before the last depreciation entry for that asset and book. A depreciating asset with named finance books requires a book assigned to it. During validation, read the current carrying value for the selected book from the asset, even if the caller supplied a previous value. Reject a zero difference before journal construction.

A positive adjustment debits fixed assets and credits the difference account. A negative adjustment exchanges the two sides. On journal submission, apply the signed difference to carrying value and the cumulative value-adjustment amount. Use the selected book’s adjustment balance for a depreciating asset and the asset-level balance otherwise. Regenerate the depreciation schedule and status. The classification of the difference account depends on the company’s accounting policy.

For a depreciating asset, change the selected book’s expected residual by the signed difference multiplied by its salvage percentage divided by 100. Cancellation of the adjustment cancels its submitted journal and applies the opposite signed difference to carrying value, adjustment balance and expected residual before rescheduling. For a 1,000.00 increase, a 10% salvage percentage and an opening residual of 1,000.00, the residual becomes 1,100.00 on submission and returns to 1,000.00 on cancellation. The [accounting fixture](../../schemas/mathematics/accounting-acceptance-cases.json) retains the identifier `asset_adjustment_residual_cancellation_boundary`.

Reject cancellation after disposal or if a new asset was split from this asset after the adjustment was submitted. The original adjustment was distributed between the split assets. Further adjustments must be made to the individual assets. For a target assembled from stock, services and components, the [composite asset contract](composite-asset-cost.md) gives the target ledger debit, purchase and total cost updates, and the recosting decision for each target status.

## Capitalized repairs and stock consumption

Repair cost has two sources: allocated amounts from submitted supplier bills and materials consumed from inventory. A selected supplier-bill expense account must actually occur on the bill for nonstock items. Allocated repair cost cannot exceed the remaining eligible amount for that invoice-and-expense-account pair after prior allocations; the same supplier bill cannot be treated as a new payable merely because its expense is later capitalized. Repair cost equals the sum of invoice allocations; consumed-material cost equals quantity multiplied by valuation rate for each consumption row; total repair cost is their sum.

Submission creates the material issue when consumption rows exist. When capitalization is enabled, increase total asset cost, additional capitalized cost and applicable financial-book carrying values by total repair cost, apply the life extension, regenerate future depreciation and create capitalization entries. For each supplier-bill allocation, debit fixed asset and credit the original eligible expense account. For consumed material, use the material issue's valued amount and expense account for the matching debit to fixed asset and credit to expense. The inventory issue remains the event that credits inventory; the capitalization must not credit inventory again.

Derived fixture: a submitted repair bill has expense debit 300.00 and supplier payable credit 300.00. Materials issued for the repair debit repair expense 200.00 and credit inventory 200.00. Capitalization debits fixed asset 500.00 and credits the two repair-expense contributions totaling 500.00. The resulting increase in asset value is 500.00, net repair expense is zero, inventory has decreased by 200.00, and supplier payable remains 300.00. With capitalization disabled, the expense remains and the fixed asset does not increase.

Cancelling capitalized repair reverses its asset-value increment, capitalization entries and useful-life increment and rebuilds the future schedule. Its linked material issue and serial-or-batch selections have their own cancellation relationships. Require the integrated cancellation to identify which linked issue is cancelled or blocked; the repair's capitalization journal alone does not restore warehouse quantity.

## Financial-book reconciliation output

For every asset and selected financial book, report acquisition cost, additional capitalization, value adjustments, posted depreciation, disposal removals and carrying value, plus unposted forecast depreciation separately. Every contributing amount links to its local journal or business record. A schedule row's forecast accumulated amount is not a substitute for summing effective posted depreciation. Reconciliation must identify missing journal links, duplicated schedule posting, wrong-book entries and cancelled journals still marked as recognized. Check the value-adjustment anomaly above separately from general journal reversal.

The complete twenty-four-row leap-year schedule is included in the `daily_depreciation_leap_year` example in [financial calculations](../calculations/README.md), including every date, day denominator, charge, accumulated depreciation and remaining carrying value. The corresponding accounting acceptance case turns those rows into individual proposed posting events and verifies the final accumulated amount independently.

## Book-specific adjustment and reversal

Before applying a change, select the asset, company, financial book, effective date and the active depreciation schedule. Separate already posted rows from pending depreciation. Apply the signed valuation difference to the chosen book and regenerate applicable future rows. A change from carrying value 600 to 540 is a 60 reduction. Cancelling the adjustment restores the signed difference of 60 and rebuilds the applicable schedule. A manual row in a second financial book is not evidence of a duplicate posting. Reconcile each book’s purchase cost, residual, accumulated depreciation, posted journals and remaining schedule independently. The [capitalization composition](composite-asset-cost.md) identifies which source values enter a capitalized target.

## Linked specifications

- **Record definitions** · [Asset](../../schemas/data/record-types/asset.json) · [Asset category](../../schemas/data/record-types/asset_category.json) · [Asset financial book](../../schemas/data/record-types/asset_finance_book.json) · [Asset depreciation schedule](../../schemas/data/record-types/asset_depreciation_schedule.json) · [Depreciation row](../../schemas/data/record-types/depreciation_schedule.json) · [Asset capitalization](../../schemas/data/record-types/asset_capitalization.json) · [Asset repair](../../schemas/data/record-types/asset_repair.json) · [Asset value adjustment](../../schemas/data/record-types/asset_value_adjustment.json)
- **Calculation and acceptance cases** · [Financial calculations](../../schemas/mathematics/financial-calculations.json) · [Accounting acceptance cases](../../schemas/mathematics/accounting-acceptance-cases.json)
