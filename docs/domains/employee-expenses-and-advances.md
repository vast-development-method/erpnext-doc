# Employee expenses and advances

## Business boundary and records

This domain records money spent on behalf of a company, approval of reimbursement, cash advanced before spending, allocation of that advance, returns and payroll recovery. The employee is a financial party. Requested, approved, paid, claimed and returned amounts are different measures and must not be collapsed into one balance. An expense claim can also contribute to project and task cost and can originate from travel or vehicle use.

An expense claim owns expense rows, tax rows and advance-allocation rows. It retains employee, company, department, claim currency, exchange rate, posting context, approver, approval status, payable account, cost centre, project, payment method, reimbursement totals and document state. Each expense row retains claimed and sanctioned amount, transaction date, type, account, cost centre and optional project. Each advance allocation retains the original advance, employee party, account, currency, payment information, allocated amount, return amount and original exchange rate. An employee advance separately retains requested amount, paid amount, claimed amount, returned amount, reason, posting date and receivable account. Evidence: source-artifact-eceb277b10e28c2ada70 lines 100–268. Evidence: source-artifact-eceb277b10e28c2ada70 lines 268–407. Evidence: source-artifact-ac7c1c8028a6331e06a5 lines 115–287.

## Claim validation and decision state

Claims require an active employee. A selected department must belong to the claim's company when that department is company-specific. A sanctioned line cannot exceed its claimed amount. Rejecting a claim resets sanctioned line amounts to zero. If multiple-currency claims are disabled, the claim currency becomes the company currency and the exchange rate becomes one, including advance conversion setup. Expense account and cost-centre requirements are enforced before accounting. Evidence: source-artifact-eceb277b10e28c2ada70 lines 100–268. Evidence: source-artifact-eceb277b10e28c2ada70 lines 426–605.

The approval status and document status are independent. A draft approval decision cannot be submitted; approved and rejected decisions are permitted. An approved submitted claim with positive sanctioned amount is unpaid until reimbursed, partially paid when some but not all has been reimbursed, and paid when its precision-rounded reimbursement equals its grand total. A zero residual claim fully covered by advances is also paid, provided there is a positive sanctioned amount. An immediate-payment flag can mark the appropriate claim paid through the same submission posting. A rejected claim retains the rejected state. Evidence: source-artifact-eceb277b10e28c2ada70 lines 100–268.

When self-expense approval prevention is enabled and no separate approval workflow governs the record, the linked employee user cannot submit their own claim through the approval path. The approver receives a share of the record; employee creation/editing permission does not by itself confer approval-field permission or submission authority. A selected custom workflow must implement its own equivalent restrictions rather than relying on the bypassed default branch. Evidence: source-artifact-eceb277b10e28c2ada70 lines 100–268.

## Amount and tax order

Round each expense row at its configured precision before summing. Total claimed amount is the sum of requested row amounts. Total sanctioned amount is the sum of approved row amounts. Company-currency amounts multiply each relevant transaction amount by the claim exchange rate and round to the corresponding company-currency precision. Parent totals are also converted and rounded; they need not equal an unrounded sum reconstructed in another representation. Evidence: source-artifact-eceb277b10e28c2ada70 lines 426–605.

Each expense tax with a nonzero rate equals total sanctioned amount times rate divided by one hundred, rounded to that tax amount's precision. A zero-rate row preserves a manually supplied tax amount. Every percentage tax row uses sanctioned amount as its basis, so these expense taxes do not compound on earlier taxes. Total taxes sum the tax rows. Grand total equals sanctioned amount plus taxes minus allocated advances and is rounded at the claim total precision. Evidence: source-artifact-eceb277b10e28c2ada70 lines 426–605.

For claimed spending of 300 with sanctioned spending of 200 and a nine-percent tax, tax is 18 and the total obligation is 218. If no advance applies, the reimbursement payable is 218. The reviewed accounting test confirms expense debit 200, tax debit 18 and employee payable credit 218. Another precision test uses 130.84 sanctioned with seven-percent tax: tax rounds to 9.16 and grand total is 140.00. Cancelling the matching payment changes the claim from paid back to unpaid. Evidence: source-artifact-40c2a5f5fc8e5a203047 lines 526–564. Evidence: source-artifact-40c2a5f5fc8e5a203047 lines 750–775.

Advance validation runs in the inspected order before the tax recalculation routine. Because its cap includes the claim's currently stored tax total, changing taxes and advance allocations together needs a targeted interaction test; the specification does not claim every edit ordering produces the same intermediate validation result. A replacement can resolve this through an explicit recalculation contract after confirming intended compatibility.

## Advance eligibility and allocation

The advance account must be receivable and its account currency must match the advance currency. Claim allocations must belong to the same employee and pass account and currency validation. An allocated amount cannot exceed the row's available unclaimed amount less return amount. The total allocation cannot exceed sanctioned expenses plus tax. Linking another employee's advance is rejected even when both employees belong to the same company. Evidence: source-artifact-ac7c1c8028a6331e06a5 lines 115–287. Evidence: source-artifact-eceb277b10e28c2ada70 lines 426–605.

Advance paid and returned values come from active advance-payment-ledger movements, separated by sign and event semantics. Paid amount cannot exceed the request. Return amount cannot exceed paid amount minus claimed amount. Claimed amount is recomputed from positive allocations in submitted, approved expense claims. These amounts must be ledger-derived rather than accepted from arbitrary client totals. The pending amount is a broader measure: it sums unpaid portions of the employee's submitted unpaid or partially paid advances posted up to the current advance's posting date. Evidence: source-artifact-ac7c1c8028a6331e06a5 lines 115–287.

The advance state is derived in priority order. Draft and cancelled follow document state. For a submitted advance, fully claimed paid funds are claimed; funds fully returned are returned; an exactly exhausted mixture is partly claimed and returned. Otherwise a fully disbursed request is paid, a partially disbursed request is partially paid, and one without payment is unpaid. An advance can therefore remain paid while some paid funds have been claimed but a residual remains; the numeric residual is more precise than the label alone. Evidence: source-artifact-ac7c1c8028a6331e06a5 lines 115–287.

## Accounting postings

When disbursing an advance, debit the employee advance receivable and credit bank or cash through the payment process. The request document is the allocation target. On an approved claim, debit each approved expense account and each tax account, credit the allocated employee advance receivable with its source reference, and credit the remaining employee payable with the claim reference. Every entry retains company, employee party where applicable, transaction amount, company amount, account currency, exchange rate, cost centre and project dimensions. Evidence: source-artifact-eceb277b10e28c2ada70 lines 268–407. Evidence: source-artifact-ac7c1c8028a6331e06a5 lines 115–287.

For an advance of 100 followed by the 218 obligation above, claim posting debits expense 200 and tax 18, credits advance receivable 100 and employee payable 118. Paying the residual debits employee payable 118 and credits bank 118. The prior advance payment remains a separate bank outflow of 100. Total bank outflow across both transactions is 218 and total recognised expenditure plus tax is 218. These are separate documents connected by allocations, not two payments against the same payable.

An immediately paid claim first records its payable and expense sides and additionally credits the payment account and debits the same employee payable within the generated entries. A payment method is required for that route. A positive remaining payable combined with allocated advances disables the direct paid flag in the inspected validation path. When an advance covers the entire approved amount, grand total is zero and no residual payable line is needed. Evidence: source-artifact-eceb277b10e28c2ada70 lines 100–268. Evidence: source-artifact-eceb277b10e28c2ada70 lines 268–407.

Cancelling a claim reverses its accounting and refreshes linked advance consumption and reimbursement state through the domain hooks. Submitted claims can support controlled account or accounting-dimension changes through reposting; an implementation must not allow such edits to leave the ledger referencing stale accounts. Project and task cost updates occur on claim submission and cancellation, so financial reversal and project cost reversal form one observable workflow. Evidence: source-artifact-eceb277b10e28c2ada70 lines 100–268.

## Currency differences and source discrepancy

The allocated advance is translated at the claim exchange rate for the claim posting, while the original paid advance retains its own exchange rate. The difference must remain attributable to that advance and to a separate exchange gain or loss journal. For allocation of 100 foreign units, an original rate of 1.50 and claim rate of 1.60 imply a company-currency difference of 10. The selected gain or loss account, employee payable and references preserve the adjustment's audit trail. Evidence: source-artifact-eceb277b10e28c2ada70 lines 426–605.

The inspected multiple-advance adjustment loop accumulates a running per-advance difference and then adds that cumulative value into the total for each row. Consequently, differences of 10 and 20 can produce a total of 40 instead of the independently summed 30: first running difference 10, then running difference 30, total 10 plus 30. This is a static discrepancy requiring a multiple-advance runtime case. The documentation does not silently declare 30 the observed source result. A rebuilding effort must choose between compatibility and a reviewed correction and record that decision. Evidence: source-artifact-eceb277b10e28c2ada70 lines 426–605.

## Travel and vehicle costs

A travel request captures employee, travel purpose, domestic or international classification, funding arrangement, sponsor and organiser details, itinerary, proposed cost rows, company and cost centre. Its inspected custom validation requires an active employee. A travel request is planning and approval evidence; the inspected controller does not itself book an expense, calculate mileage rates or issue a cash advance. Those follow through the appropriate expense and payment transactions. Evidence: source-artifact-2c00a90a22c49dc1db3e lines 1–49.

A vehicle log requires its odometer not to fall below the previous value. Submission updates the vehicle's last odometer. Preparing an expense claim rejects an existing claim linked to that log and computes service-detail cost plus fuel unit price times fuel quantity. A zero resulting expense is rejected. Cancellation handles linked draft expense claims: it deletes those containing only the vehicle expense or removes the vehicle expense and link from mixed claims. The vehicle odometer is adjusted by subtracting the cancelled log's positive travelled distance. Later-log cancellation ordering therefore deserves a conformance case. Evidence: source-artifact-9d075d03270607666fa8 lines 38–136.

For service rows 40 and 60, forty litres of fuel at 1.80 produce fuel expense 72 and a prepared total claim of 172. This preparation is not approval: sanctioned values and tax still belong to the claim's review. Distance travelled does not multiply an automatic reimbursement rate in this controller.

## Payroll recovery and final settlement

Unused employee advances can be recovered through a linked additional salary deduction. The payroll accrual uses the employee, advance account and advance-document reference to credit the original receivable rather than treating the deduction as ordinary employer income. The amount withheld from wages reduces the payroll payable. Final settlement lists unsettled advances separately from salary and reimbursement payables and combines them only for display or a specifically authorised settlement transaction. Refer to [Payroll and benefits](payroll-and-benefits.md) and [Workforce and employment](workforce-and-employment.md). Evidence: source-artifact-d5acb8e83e12487cc684 lines 393–912. Evidence: source-artifact-6d41c13978f619ac7243 lines 50–215.

## Acceptance criteria

1. Reject a sanctioned amount above the request, a department from another company, a non-receivable advance account and another employee's advance.
2. Round expense lines and taxes as specified; the 130.84 and seven-percent case produces 140.00.
3. Approve and submit a taxed claim partly covered by an advance. Verify expense and tax debits, advance credit and only the residual payable.
4. Allocate advances covering the complete obligation. Verify zero residual payable and paid claim status without a second bank outflow.
5. Make two partial reimbursements, cancel one, and verify the claim's remaining payable and status are rebuilt from surviving movements.
6. Reject a disbursement above the requested advance and a return exceeding the unclaimed paid balance.
7. Exercise self-approval with default settings and separately with a configured approval workflow.
8. Post two foreign-currency advance allocations with different rates; compare each difference and total to the identified source discrepancy.
9. Cancel a mixed draft vehicle claim's originating log and preserve unrelated expense rows.
10. Recover an advance through payroll and verify that both employee receivable and payroll payable reduce with source references intact.

Selected expense posting and rounding cases were reviewed in source tests. They were not executed against a running system. Multi-currency allocation ordering, multiple-advance gain/loss, concurrent reimbursement and reposting require runtime verification before claiming complete financial equivalence.
