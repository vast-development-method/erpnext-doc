# Assets and depreciation

## Asset identity and financial histories

A fixed asset is an individually identified capital resource associated with a company, product, asset category, acquisition or capitalization, available-for-use date, location or custodian and financial-book policies. An asset's financial history includes cost, additional capitalization, accumulated depreciation, expected residual value, schedule revisions, depreciation journals, value adjustments, sale, scrap and restoration. Asset identity is not interchangeable with product identity: several individually controlled assets can share one product master.

The depreciation schedule is a separate persistent record with asset identity, financial-book identity, method, frequency in months, total cycles, starting date, current carrying value, residual value, applicable rate, prorating and shift choices, lifecycle state, and ordered schedule rows. Each row retains schedule date, depreciation amount, accumulated depreciation, optional shift and posted journal reference. A second active schedule for the same asset and financial book is rejected in a source test. A completed posting link distinguishes immutable recognized history from future forecast. Evidence: source-artifact-c2093495635cba0caf62 lines 24–35; source-artifact-754baff265e1928e4846 lines 29–53.

This blueprint excludes migrations from older software versions. Initial recognition of an already owned asset is nevertheless a current business operation, not necessarily a software migration. Its opening accumulated depreciation and previously completed periods matter when computing future charges. Similarly, extending useful life or increasing asset value after repair changes future expectations without authorizing edits to already posted depreciation.

## Schedule regeneration

Regeneration begins by loading the asset and selected financial-book policy, retaining existing schedule rows with journal references and discarding only the future unposted portion. It then initializes current carrying value, remaining months and cycles, prorating indicators, next dates, and financial-year context. Each new row calculates a candidate charge, adjusts for disposal or partial periods, rounds it to asset monetary precision, updates remaining value, checks residual value and appends a positive charge. Accumulated depreciation is reconstructed by respecting previously posted cumulative amounts and adding newly calculated future charges. Evidence: source-artifact-754baff265e1928e4846 lines 29–143; source-artifact-754baff265e1928e4846 lines 393–421.

The schedule's anticipated future charges are not ledger balances. A forecast row without a posted journal must not be counted as recognized depreciation. The posting process links each actual journal to its schedule row. Acceptance must check both the asset carrying amount and the accumulated-depreciation account after posting and reversal.

## Straight-line method

Depreciable value is current value after depreciation less expected value after useful life. Under the fixed-period method, remaining periods equal remaining months divided by frequency in months. Each candidate charge is depreciable value divided by remaining periods. Prorating may add a final partial period. Final residual correction ensures that the last charge brings carrying value to the expected residual rather than leaving accumulated rounding error. Evidence: source-artifact-e17569ef363ca1f54de5 lines 15–31; source-artifact-754baff265e1928e4846 lines 113–143; source-artifact-754baff265e1928e4846 lines 342–378.

Derived fixed-period fixture: acquisition cost 12000.00, residual value 2000.00, five annual periods, no opening depreciation and no partial first period produce annual depreciation 2000.00 and closing carrying values 10000.00, 8000.00, 6000.00, 4000.00 and 2000.00. Debits to depreciation expense total 10000.00, credits to accumulated depreciation total 10000.00, and cost remains 12000.00 until disposal or a separately authorized value adjustment.

Under daily prorating, one policy divides remaining depreciable value by total remaining useful days. Another derives yearly depreciation by dividing depreciable value by remaining years, then divides that yearly amount by the number of days in the current depreciation financial year. The latter can produce different daily charges in leap and nonleap years while maintaining equal annual depreciation before rounding. Multiply daily amount by the inclusive number of depreciable days for each schedule interval. The first and final intervals depend on available-for-use date and schedule anchoring. Evidence: source-artifact-e17569ef363ca1f54de5 lines 33–45; source-artifact-754baff265e1928e4846 lines 429–439.

Source test expectation: cost subject to depreciation 100000.00 over 24 monthly periods, available on 2020-01-01, first schedule 2020-01-31, daily prorating enabled, and annual-day denominator selected. January 2020 depreciation is 4234.97, February 2020 is 3961.75 and cumulative February amount is 8196.72. December 2020 cumulative amount is 49999.98. January 2021 charge is 4246.58. Final December 2021 charge is 4246.56 and cumulative depreciation reaches exactly 100000.00. These values show the leap-year divisor and final rounding correction; a fixed monthly 4166.67 does not reproduce this schedule. Evidence: source-artifact-c2093495635cba0caf62 lines 37–87.

## Shift-weighted depreciation

When shift weighting is selected and prior unposted schedule rows exist, each row has a shift name resolved to a configured numeric factor. Sum factors for unposted rows. Charge for a row is remaining depreciable value divided by total unposted factors, multiplied by that row's factor. Posted rows do not participate in the new denominator. Without an existing schedule to supply shift assignments, the initial amount uses ordinary remaining-period division. Evidence: source-artifact-e17569ef363ca1f54de5 lines 47–73.

Derived fixture: remaining depreciable value 600.00 and three unposted rows with factors one, two and three produce charges 100.00, 200.00 and 300.00. If the first row has already posted, it remains unchanged; any later change to the shift factors redistributes only the remaining depreciable value. A zero total factor is an explicit invalid-input acceptance case that needs runtime verification because the reviewed arithmetic itself divides by that sum.

## Declining-balance methods

The double-declining annual percentage is 200 divided by useful life in years. Useful life in years is total number of depreciation cycles multiplied by frequency in months, divided by twelve. Round the resulting rate to configured general numeric precision. A five-year life therefore gives 40 percent. Evidence: source-artifact-b27f188a7ac1322f5204 lines 1004–1026.

Written-down-value rate can be explicitly supplied. When calculating it, divide residual value by current asset carrying value, raise that ratio to one divided by remaining years, subtract from one, and multiply by 100. Remaining years uses unbooked periods times frequency plus life-extension months, divided by twelve. An explicit rate is preserved during validation; a supplied rate can also remain when residual value is zero. For residual 1000.00, current value 10000.00 and five years remaining, the derived annual percentage before rate rounding is approximately 36.90426555. At two rate places it is 36.90 percent, so residual correction remains necessary. Evidence: source-artifact-b27f188a7ac1322f5204 lines 1028–1051.

For non-daily declining methods, each new financial year calculates yearly depreciation as remaining carrying amount multiplied by annual rate divided by 100. The periodic charge is that annual amount multiplied by frequency divided by twelve. Subsequent periods in the same financial year reuse that periodic amount. This is yearly declining balance allocated across periods, not monthly compounding against the immediately previous month. With daily prorating, the financial-year charge is divided by the actual days in that financial year and multiplied by inclusive interval days. Evidence: source-artifact-e17569ef363ca1f54de5 lines 76–119.

Derived full-year double-declining fixture: cost 10000.00, five-year life, annual 40 percent, annual periods and residual 1000.00. Candidate charges are 4000.00, 2400.00, 1440.00 and 864.00, leaving 1296.00 before year five. The last raw 518.40 would breach residual, so final depreciation is 296.00 and closing carrying value is 1000.00. Earlier termination at residual suppresses further depreciation rows.

## Partial periods, disposal, and low-value assets

When disposal occurs on or before a planned schedule date, the interval begins after the last scheduled depreciation date or the applicable initial available-for-use date. A prorated charge is calculated through disposal, rounded, and appended at disposal date if positive; generation stops after that. First-period and final-period adjustments depend on month-end anchoring and any useful-life extension. An asset whose rounded first-period charge is not positive can be rejected as too small to depreciate over the selected number of cycles. Evidence: source-artifact-754baff265e1928e4846 lines 297–391.

Residual correction applies when a final row would leave carrying value different from expected residual, or when any row would push value below residual. Add the difference between candidate remaining value and residual to the candidate depreciation, round, and stop further rows. This preserves cost less accumulated depreciation equal to residual under the intended completed schedule. Do not let a generic rounding routine erase the final remaining cent.

The manual schedule selection shares initial straight-line generation in the inspected schedule method dispatcher. That does not prove that all later manual-edit validation is equivalent to straight-line calculation. Manual schedule editing requires its own command validation and acceptance tests for date ordering, total charge, journal-linked rows and residual preservation. Evidence: source-artifact-754baff265e1928e4846 lines 423–427.

## Depreciation and disposal posting

Recognized depreciation debits the configured depreciation-expense account and credits the accumulated-depreciation account for the chosen asset category and company, retaining asset, schedule, financial book, cost center, date and dimensions. A sale or scrap first determines depreciation through disposal date and then removes the asset's financial position. Posting failures must leave the schedule's posting reference and status consistent with whether a journal was actually submitted. The detailed batch-failure and retry behaviour should be verified independently; the existence of a daily scheduler does not establish exactly-once posting.

For disposal, credit the fixed-asset account for net purchase cost and debit accumulated depreciation for its accumulated amount. Profit equals selling amount less carrying value after depreciation; its sign determines gain or loss movement in the disposal account. The sales invoice or scrap journal supplies the remaining counter-entry. Evidence: source-artifact-80fc5683d2f98099fac7 lines 655–709.

Derived sale fixture: cost 12000.00, accumulated depreciation 8000.00, carrying value 4000.00 and sale amount 4500.00 before sales tax. Disposal credits cost 12000.00, debits accumulated depreciation 8000.00 and credits disposal gain 500.00; the invoice debits customer receivable 4500.00. At sale amount 3500.00 the disposal account receives a 500.00 debit loss instead. A scrap with no proceeds debits disposal loss 4000.00, debits accumulated depreciation 8000.00 and credits cost 12000.00.

Restoration and sales returns need the prior disposal context, relevant depreciation journals and financial-book carrying amount. They cannot merely set an asset status back to active. The inspected code contains explicit regain, disposal reversal, depreciation cancellation and schedule reset paths. Their complete combination matrix with partial disposals, repairs, capitalization and multiple financial books is recorded as a remaining execution requirement rather than claimed as fully validated.

## Acceptance requirements

1. Reject duplicate active asset and financial-book schedules.
2. Reproduce the leap-year source test values above and the final cumulative 100000.00.
3. Reproduce fixed straight-line, weighted-shift and annual declining examples at declared precision.
4. Rebuilding a schedule after a posted row retains its date, amount, accumulated amount and journal link.
5. Changing future shift factors or extending remaining life affects only unposted charges.
6. A disposal mid-period records required prorated depreciation before cost removal and gain or loss.
7. Completed depreciation never leaves carrying value below the configured residual.
8. Cancelling or reversing depreciation restores expense, accumulated depreciation, asset carrying value and schedule linkage consistently.
9. A second financial book can have a different method and schedule without silently duplicating another book's postings in a report that includes only one book.
10. Failed journal submission cannot leave a schedule row falsely marked as posted.

The formulas and selected schedule expectations are source-reviewed. Full depreciation date arithmetic for every anchor, manual edits, capitalization, repair, impairment and restoration is not established by these examples alone and remains enumerated in the review catalog.
