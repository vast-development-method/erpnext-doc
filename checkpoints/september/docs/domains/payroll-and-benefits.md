# Payroll and benefits

## Calculation contract

Payroll converts effective remuneration agreements, working-time evidence, benefit entitlements, tax configuration and approved adjustments into an employee salary slip and accounting obligations. Its reproducible output includes component rows, taxable projections, deductions, net amount, currency conversions, benefit movements, journal references and payment status. It is not sufficient to reproduce only the displayed net wage.

A salary structure groups ordered earnings, deductions and employer contributions. An effective assignment attaches it to an employee with base values, tax slab, currency, benefits and cost allocation. A payroll period supplies the company-specific annual or other assessment interval. A salary slip supplies a narrower pay interval, actual employment interval, payment-day basis and the evaluated component rows. A payroll batch selects employees, creates and submits slips, records failures and produces accrual and bank journals. A submitted slip is distinct from a bank payment and may be withheld.

All mathematical examples below are deliberately invented conformance cases using the inspected algorithms. They are not jurisdictional rates. Monetary values carry their currencies and field precision. Intermediate rounding and final rounding are separate operations; mathematical rules use full names in the companion [workforce calculations catalog](../../schemas/mathematics/workforce-calculations.json).

## Salary-slip submission and cancellation

Submission rejects a negative net wage, associates eligible time records with the salary slip and records benefit movements. Status is cancelled for a cancelled document; otherwise an attached withholding takes precedence over draft or submitted status. Linked gratuity and leave-encashment records included through additional salary are marked paid when the salary slip is submitted, and unpaid on cancellation. This paid label records inclusion in payroll and must not be mistaken for proof that the bank disbursement was submitted. Cancellation unlinks the time-record salary reference, cancels optional loan repayments and deletes benefit-ledger rows associated with the salary slip. The benefit entitlement ledger therefore uses removal on this cancellation path, separately from financial-ledger reversal rules.

## Date selection and working days

The ordinary duplicate check rejects another non-cancelled slip for the same employee with identical start and end dates, narrowed to the same payroll batch when the new slip has a batch reference. This is an exact-period check, not proof of a general overlap prohibition. Time-based slips separately reject already-payrolled time records. Eligible time records are submitted, billed or partially billed and have their start date inside the slip interval. Hourly wages equal the configured hour rate multiplied by their total working hours.

Working days initially equal the inclusive calendar-day count of the whole slip interval. When holidays are excluded, subtract the applicable holiday dates. Reject a result made negative by holiday configuration. The actual payment interval is clipped to joining and relieving dates; holidays are again excluded from that clipped interval when configured. A person joining after the slip ends has zero payment days. A relieving date before the slip begins also triggers the inspected employment-status check.

Payment days begin with that clipped interval and then subtract unpaid-leave equivalents and, in attendance mode, absence. Unmarked days are treated as present unless the setting makes them absent. The unmarked-day calculation excludes dates outside employment, counted attendance records and applicable holidays. Half-day attendance whose other half is absent adds a fractional absence deduction. A positive, verified payroll correction can add corrected days. The default half-day wage fraction is one half; a configured zero also falls back to one half in the inspected implementation. A replacement must not interpret zero as a valid instruction to pay nothing for a half day without explicitly changing this behaviour.

For a thirty-day month with four excluded holidays, total working days are twenty-six. An employee present for the whole month with two unpaid-leave equivalents and one absent day has twenty-three payment days. A day-dependent 2,600 earning becomes 2,300. A fixed 100 allowance not dependent on payment days remains 100. The gross wage is 2,400 before deductions. A joining date during the month changes the numerator through the clipped interval but not the whole-month denominator.

## Partially paid leave discrepancy

In approved-leave mode, a full partially paid leave contributes one minus its configured daily-salary fraction to unpaid-leave equivalents. A half day first contributes one minus the configured half-day wage fraction and then receives the partially paid factor. In attendance mode, the inspected implementation instead multiplies by the configured daily-salary fraction itself, falling back to one when that fraction is zero. Thus a single full partially paid leave with a retained-pay fraction of 0.75 reduces payment days by 0.25 in approved-leave mode and by 0.75 in attendance mode. A fraction of 0.5 conceals the discrepancy.

This is an unresolved source-behaviour discrepancy, not a universal payroll principle. Behavioural equivalence requires an explicit compatibility decision and a conformance case for fractions other than one half. Do not silently merge the branches into a preferred industry rule. The reviewed tests verify approved-leave calculations at one half and attendance half-day calculations, but do not establish equivalent outcomes for this three-quarter fraction.

## Component evaluation and proration

Components may carry a fixed amount, a condition and an expression, plus switches for taxable income, income-tax exemption, payment-day dependency, accrual treatment, exclusion from displayed totals, exclusion from accounting and integer rounding. Expressions may depend on earlier evaluated components and employee or assignment values. A rebuilding system needs a safe, deterministic expression contract with named inputs, arithmetic, comparisons, dates and controlled helper functions; it need not execute the source implementation language.

For an ordinary day-dependent row with default amount and separately tracked additional amount, prorate each portion by payment days divided by total working days, round each to its field precision and add them. An additional salary that overwrites the structure amount has different handling: its additional portion represents the difference from the prior default rather than an independently prorated ordinary supplement. Hourly wage components normally bypass day proration, except the inspected joining or relieving boundary branch. Arrears, payroll corrections, benefit claims and accrual components bypass another payment-day adjustment because their amounts already reflect the relevant entitlement or historical period.

Round a component to the nearest integer under the configured system rounding policy when that component requests it, then retain the configured monetary precision on saved rows. The three selectable policies and precision precedence are specified in [Persistence identity and values](../data/persistence-identity-and-values.md). Do not assume that every monetary half tie uses nearest-even rounding: leave-increment and interval-hour calculations use their separately documented nearest-even operation, while salary and currency helpers follow the selected policy. Gross pay excludes earnings explicitly omitted from totals. Deductions similarly exclude rows omitted from totals. Net pay equals gross pay minus total deductions and loan repayment when the optional lending integration supplies one. Company-currency totals multiply the corresponding transaction-currency amount by the exchange rate and round to the destination precision. Final rounded pay and rounded company-currency pay are calculated independently from their own net amounts. Employer contributions are calculated after employee deductions and are displayed separately; they do not enter gross, employee deduction or net-pay totals.

## Annualisation and tax assessment

A payroll period must enclose the entire salary-slip interval and belong to the company. Periods for one company cannot overlap. For monthly payroll without the payment-day factor, period counts use the inspected exact-month-difference rule; a July sixteenth to the following July fifteenth assessment contains twelve monthly periods. Other frequencies divide inclusive days in the assessment period by inclusive days in the current pay interval. Remaining periods use the end clipped to employment relief.

Annual taxable earnings combine prior submitted taxable earnings, eligible opening taxable earnings, actual current structured taxable earnings, projected future structured taxable earnings, current additional taxable earnings and other declared income, minus permitted exemptions. Current structured earnings reflect payment days; future structured earnings use a full-period value multiplied by the rounded remaining-period count minus one. Future non-taxable earnings are recalculated with full payment days and use the ceiling of remaining periods minus one. This means future tax estimates must not simply repeat a partially paid current month.

The current tax calculation first computes annual tax excluding additional components designated for immediate full taxation. It subtracts prior tax paid and divides the remainder by remaining periods when that count is positive; when it is zero, structured current-period tax is zero. It then adds the incremental annual tax caused by full-tax additional earnings. Finally, the current deduction is floored at zero. Excess previous withholding does not automatically generate a negative current deduction. An approved additional tax component may override the structured amount under its overwrite semantics.

A simple case with projected ordinary annual tax of 12,000, previously withheld tax of 7,200 and four remaining periods produces 1,200 current structured tax. If an immediate-tax bonus increases annual tax by 900, the current deduction is 2,100. If prior withholding instead exceeds ordinary annual tax and there is no bonus, the current deduction is zero. The remaining-period denominator and final floor both matter.

## Slab boundaries, sequential charges and relief

Each tax slab has lower amount, optional upper amount, percentage and optional eligibility condition. Conditions are evaluated using the annual taxable amount and the permitted context. A failed condition omits the slab. For a participating slab, the taxable width includes an added one currency unit: a bounded fully consumed slab uses upper minus lower plus one; a partly consumed or unbounded slab uses income minus lower plus one. A slab with no upper amount remains open-ended.

For a configured slab from 1,001 through 2,000 at ten percent, income 1,500 yields a width of 500 and tax of 50. Income 2,000 consumes width 1,000 and yields 100. A following slab starting at 2,000 would share that boundary under the current algorithm. Do not replace the added-one convention with a continuous-width formula or normalise overlapping boundaries without declaring the changed result. Fractional monetary incomes especially require tests because the source combines a discrete added-one boundary with currency-valued amounts.

Taxable income at or below the relief limit returns zero before other charges. The inspected regional marginal-relief rule applies only when income is strictly above the relief limit and strictly below the marginal-relief limit; within that interval, tax is capped at the excess income over the relief threshold when that excess is smaller. Surcharge extension runs next. Other charges run in row order on the running tax, with optional inclusive minimum and maximum income bounds. A ten-percent charge followed by a four-percent charge on base tax of 1,000 gives 100 and then 44, for total tax 1,144. It does not give 1,140. Tests explicitly exercise the sequential calculation.

The slab must not be disabled and must be effective on or before the payroll-period start. Exemption claims use declarations ordinarily but submitted proof when proof enforcement is selected; the final period forces proof enforcement. A standard exemption is added according to the configured slab rules. Declared other income is company-, employee- and payroll-period-specific and must be submitted. Region-specific additions remain effective-dated business configuration and need independent coverage; these calculations are descriptions of the inspected snapshot, not present-day legal advice.

## Benefits, accrual and claims

The benefit ledger records employee, company, payroll period, component, posting date, salary slip, entitlement reference, yearly amount and an accrual or payout movement. Only earning components are accepted. Accrued and paid totals are maintained separately. A monthly benefit of annual 12,000 over twelve periods starts at 1,000 for the current cycle, optionally prorated by payment days. The ledger must preserve the difference between entitlement accumulation and cash-bearing earnings.

For end-of-period payout, earlier cycles accrue. The final cycle pays the non-negative balance of prior accrual plus the current entitlement minus prior and current claims. Current entitlement is limited to the remaining yearly amount in the inspected positive-remainder branch. Claim-only benefits accrue but may optionally pay out the remaining balance in the final cycle. The claim-only branch also reduces current accrual when recorded payouts exceed prior accrual. This behaviour must be tested rather than inferred from its explanatory comments.

Claim eligibility in accrue-per-cycle mode is accrued amount plus current-cycle benefit minus paid amount, and an already overpaid balance is rejected. In full-benefit claim mode eligibility is the yearly amount minus paid amount. A claim creates an additional salary source and payout movements are recorded through the salary-slip flow. If annual entitlement is 12,000, prior accrual 5,000, prior payouts 3,000 and this cycle adds 1,000, claim eligibility is 3,000. Accrual of that entitlement is not an additional 3,000 earning by itself.

## Overtime and gratuity

Overtime slips reject overlapping non-cancelled intervals for one employee and repeated detail dates. Submitted present attendance with an overtime type supplies elapsed overtime. Attendance-derived durations are capped to a configured maximum when positive; manually entered durations above a configured maximum are rejected. Overtime amounts are grouped by earning component and produce submitted additional salary dated at the overtime interval's end.

Fixed-rate overtime equals duration times hourly rate times applicable multiplier. Component-derived hourly rate equals selected ordinary earning components divided by the greater of payment days and one, then divided by that detail's standard working hours. Additional salary rows are excluded from this component basis. Standard, weekly-rest-day and public-holiday multipliers are alternatives selected by the holiday classification and enabled settings. For monthly eligible earnings of 2,600, twenty-six payment days and eight standard hours, hourly rate is 12.50. Three overtime hours at one and a half times produce 56.25. A zero standard-hours divisor needs explicit validation; the inspected calculation does not establish a safe fallback.

Gratuity uses a configured work-experience method and selected ordinary default earnings from the latest submitted salary slip. Experience ordinarily equals elapsed days from joining to relieving, excluding the relieving endpoint through date subtraction, less counted non-working attendance, divided by configured working days per year or one when absent. Leave-based mode subtracts full unpaid-leave attendance records; attendance mode subtracts absent records. This is not the same inclusive-day rule used by payroll. Rounded experience and manually supplied experience are alternative modes.

A current-slab gratuity applies the selected fraction to all experience years and eligible monthly earnings. A cumulative-slab gratuity accumulates each completed interval width and then remaining years at the relevant fraction. Both require an applicable slab; calculated experience must meet the minimum threshold. For earnings of 2,000, seven years, a first five-year band at one half and a following band at one, cumulative gratuity is 9,000, while applying a current slab at one to all seven years gives 14,000. Submission either creates additional salary or directly debits gratuity expense and credits employee payable, according to the selected payment route.

## Adjustments, withholding and accounting

Current operations include payroll corrections and retrospective salary differences; they are not historical database migration. A payroll correction references a prior slip and limits total corrected days to its working days minus payment days, floored at zero. Ordinary eligible component correction equals default amount divided by total working days times corrected days. Accrual correction instead divides the recorded accrual amount by original payment days. A zero denominator is rejected. Only enabled components marked for arrears and not variable-tax components participate. Retrospective salary differences compare recalculated eligible components with existing amounts and retain positive differences only; decreases do not become negative arrears through that path.

Salary withholding identifies dated cycles and excludes ordinary disbursement until released. The cycle frequencies are monthly, every two months, every fourteen days, weekly or daily. A submitted withholding is released only when all its cycle flags are released. Submitting the release bank journal updates linked slips and cycles; cancelling it restores withheld status and clears the journal reference. A frequency of every two months must not be interpreted as twice per month.

Accrual debits earning expense accounts, credits deduction accounts and credits the remaining payroll payable. Each component uses its company-specific account mapping; missing mappings reject posting. Cost-centre distribution comes from the latest applicable assignment, otherwise employee default, then department default, then batch default. Multiply each amount by its distribution percentage divided by one hundred. Advance deductions receive employee and advance-document references so recovery clears the correct receivable. Employee-specific payable accounting is optional; aggregate posting still retains the payroll batch source.

For earnings 10,000, employee tax 1,500 and advance recovery 500, the basic journal debits wage expense 10,000 and credits tax payable 1,500, employee advance receivable 500 and payroll payable 8,000. Payment then debits payroll payable and credits the chosen bank account. Preserve company currency, account currency, exchange rates, cost centres and other accounting dimensions on each row. A displayed employer contribution must not be assumed posted: the inspected standard accrual builder requests earnings and deductions only. Employer-contribution liability posting is an identified verification gap in this snapshot.

## Projection discrepancy requiring execution

The future exempt-deduction expression routine advances weekly dates by six days per subperiod and fortnightly dates by thirteen; its daily branch refers to a local date before it has been assigned in that branch. These are current-source findings, not proposed frequency rules. Execute all non-monthly projection variants and explicitly record a compatibility or correction decision before describing these projections as complete.

## Acceptance and verification gates

Reproduce full-month and mid-month employment; holidays included and excluded; unpaid, partially paid and half-day leave; attendance marked or unmarked on holidays; exact-period duplicates; time-sheet already payrolled; zero payment days; component dependencies; supplement overwrite; full-tax bonus; final proof reconciliation; zero remaining tax periods; benefits accrued versus paid; overtime caps; gratuity slab boundaries; corrected days exhausted; withheld payment and cancellation; employee-specific and aggregate accrual; cost-centre splits; and missing account mappings. Compare component rows, intermediate tax projections, benefit movements and journals, not merely final wages. The reviewed source tests support selected working-day, projection, tax and overtime paths; no full runtime payroll execution was performed for this specification.

## Self-contained contracts and conformance

The [workforce calculations](../../schemas/mathematics/workforce-calculations.json) define named inputs, calculation order, boundary conditions and numerical examples. The [workforce acceptance cases](../../schemas/mathematics/workforce-acceptance-cases.json) define arrangements, actions, expected records, accounting consequences and rejection conditions. These files and the linked record definitions are part of this specification; no external implementation or unavailable evidence identifier is required to interpret a rule. A verification label distinguishes inspected transaction behavior from calculations exercised in isolation.

## Persistent payroll contracts

| Record definition | Retained facts and relationship constraints |
| --- | --- |
| [Salary component](../../schemas/data/record-types/salary_component.json) | Earning, deduction or employer-contribution classification; full component name; condition and amount expression; taxable and tax-exempt choices; payment-day dependence; accrual and payout rules; display-total and accounting exclusions; company-specific accounts |
| [Salary structure](../../schemas/data/record-types/salary_structure.json) | Company, currency, frequency, active state, ordered component rows, hour-rate basis and benefit limits; order is meaningful when later expressions use earlier values |
| [Salary structure assignment](../../schemas/data/record-types/salary_structure_assignment.json) | Employee, structure, effective start, base and variable values, tax slab, opening balances, leave encashment value and distribution rows; a submitted assignment effective no later than actual pay-interval start must exist |
| [Salary slip](../../schemas/data/record-types/salary_slip.json) | Employee and company, whole and actual pay intervals, calendar basis, working and payment days, earnings/deductions/contributions, accrual rows, tax inputs and outputs, time records, withholding, document state and journal links |
| [Payroll entry](../../schemas/data/record-types/payroll_entry.json) | Company, posting and pay dates, currency, exchange rate, frequency, selected employees, account context, submission progress, failures and payroll accounting references |
| [Employee benefit claim](../../schemas/data/record-types/employee_benefit_claim.json) | Employee, component, payroll date, company and currency, yearly entitlement, displayed eligibility, claimed amount and submitted state |
| [Employee benefit ledger](../../schemas/data/record-types/employee_benefit_ledger.json) | Employee, component, assessment period, posting date, amount, movement kind, salary-slip link and benefit entitlement context; accrual and payout totals remain separately calculable |
| [Additional salary](../../schemas/data/record-types/additional_salary.json) | Employee, component, company, amount and currency, effective payroll date or recurrence interval, overwrite choice and originating business record |

A payroll rebuild must save enough evaluated information to reproduce the submitted result after a later structure or tax setting changes. Re-evaluation of an old draft may use current effective configuration; a posted monetary obligation must remain traceable to the values actually accepted for that obligation. This preservation requirement complements the [record lifecycle](../runtime/README.md) and [financial accounting](financial-accounting.md) rules.

## Ordered calculation protocol

1. Resolve employee, company, whole pay interval, actual employment interval, effective structure and effective submitted assignment. Obtain the payroll basis and holiday configuration. Reject an absent payroll basis.
2. Identify existing non-cancelled exact-period slips using the batch-sensitive duplicate rule. Validate any selected time records against existing payroll links.
3. Determine the whole-period denominator and clipped employment-day numerator. Count unpaid-leave equivalents using the selected basis. Apply absence, unmarked-day and corrected-day branches in their stated order.
4. Evaluate ordinary earnings and eligible additional salary, preserving default and additional portions. Evaluate benefits and retain separate accrual versus payout rows. Calculate gross pay from included earning rows.
5. Evaluate deductions and variable tax with the annual projection. Add optional loan recovery and configured regional deductions. Evaluate employer contributions separately.
6. Store component monetary precision, deduction totals, net pay, exchange-converted totals and independent rounded totals. Reject negative net pay on submission.
7. Submit the slip, link eligible time records, record benefit movements and update linked payroll-originated benefit payment labels. Create accrual only through the accounting action; create payment only through the bank or cash action.

The payment-day branch has a subtle guard: it subtracts unpaid leave and then attendance deductions only when clipped employment days are strictly greater than unpaid-leave equivalents. Otherwise it sets payment days to zero before any verified correction. The inspected routine does not apply an additional universal zero floor after all absence deductions. Inconsistent attendance counts can therefore expose a negative result before later validation. Adding such a floor is a behavior change and requires an explicit decision. A nonzero manually supplied unpaid-leave total can be retained with a discrepancy message; a supplied zero follows the automatic calculation branch.

## Exact tax-boundary decision table

For each eligible slab, first compare annual income with its lower bound. Income below the lower bound contributes zero, even when it lies within one currency unit of that bound. Once the lower bound is reached, the added-one width convention applies. This gate cannot be replaced by taking only the maximum of zero and a width expression.

| Annual income | Lower bound | Upper bound | Rate | Tax from this slab |
| ---: | ---: | ---: | ---: | ---: |
| 1,000.50 | 1,001 | 2,000 | 10 percent | 0.00 |
| 1,001.00 | 1,001 | 2,000 | 10 percent | 0.10 |
| 1,500.00 | 1,001 | 2,000 | 10 percent | 50.00 |
| 2,000.00 | 1,001 | 2,000 | 10 percent | 100.00 |

These boundary values and the sequential-charge case were exercised by isolated calculation calls with controlled inputs. The verification establishes these arithmetic branches; it does not establish database posting, regional legal sufficiency or every configured expression. Annual taxable projections use nearest-even whole-count rounding for taxable future periods, whereas future non-taxable earnings and exempt-deduction iteration use a ceiling. For a remaining-period count of 2.5, taxable projection uses one future period and non-taxable projection uses two. This difference must remain explicit.

## Benefit claim and accrual edge contracts

A benefit claim payroll date cannot precede the current date. The claimed amount must be positive and cannot exceed its displayed maximum eligibility. The duplicate query rejects another **submitted** claim for the same employee and component in the same calendar month. It uses calendar-month boundaries even for weekly payroll; it is not one claim per weekly interval. A draft does not reserve that monthly slot under this check. Submitting creates a submitted additional salary with supplement semantics and a reference to the claim. Payout ledger entries arise when the salary slip is submitted.

The claim validation path checks the stored maximum eligibility; fetching benefit details is a separate action. Therefore server-side recomputation on every submit is an additional integrity requirement for a replacement, not a claim already proved by this validation routine. A concurrent double submission must be exercised against transaction isolation before declaring the duplicate check sufficient. Cancellation must account for the submitted additional salary and any submitted slip that consumed it; the claim controller does not establish an unconditional automatic cancellation cascade.

The following exact edge cases were evaluated in isolated calculation calls:

| Arrangement | Result |
| --- | --- |
| Annual 12,000; prior accrual 5,000; prior payouts 5,500; normal current entitlement 1,000; claim-only mode; ordinary cycle | Current accrual is reduced to 500 |
| Same values; final cycle and final payout enabled | Reduced current entitlement 500 is used again against prior payouts; payout is zero |
| Annual 12,000 already fully accrued; current entitlement 1,000; end-of-period-payout mode; ordinary cycle | Current accrual remains 1,000 because the remaining-entitlement cap tests a strictly positive remainder |

The last case does not justify an unlimited entitlement. It documents that the inspected cap alone does not enforce the annual ceiling when the remainder is zero or negative. An enterprise replacement must expose the chosen compatibility treatment and verify combined claim, payout and year-end reconciliation. It must never describe the strict-positive cap as a universal annual hard limit.

## Accrual, payment and reversal matrix

| Action | Business records | Financial consequence |
| --- | --- | --- |
| Save salary preview | Calculated draft values only | No booked wage expense or bank movement |
| Submit salary slip | Submitted slip; linked time records; benefit accrual or payout movements; inclusion-based paid labels | Salary submission alone does not establish bank settlement |
| Submit payroll accrual | Submitted journal linked to eligible slips and payroll batch | Debit included earnings expense; credit included deductions, referenced advance recovery and residual payroll payable |
| Submit ordinary bank journal | Payment references for eligible unwithheld slips | Debit payroll payable; credit bank with currency and accounting dimensions preserved |
| Submit withholding release payment | Release flags and associated slip states updated | Bank settlement of the released obligation |
| Cancel release payment | Restore withholding flags and clear payment reference | Reverse the cancelled financial movement |
| Cancel salary slip | Cancelled slip, time links removed, benefit-ledger rows removed, linked gratuity or encashment inclusion labels cleared | Related submitted accounting requires its cancellation/reversal lifecycle; deleting benefit entitlement rows is not a substitute |
| Cancel payroll batch | Coordinated cancellation of linked slips and journals; cancellation progress may be asynchronous | No surviving active accrual or payment should continue to represent a cancelled slip without an explicitly retained independent obligation |

For a 60 percent and 40 percent assignment split of 10,000 earnings, expense allocation is 6,000 and 4,000 at the applicable row precision. Tax 1,500 and advance recovery 500 leave payroll payable 8,000. Total debit and credit are both 10,000. A displayed employer contribution of 700 leaves this ordinary builder unchanged; recognizing a separate employer expense and contribution liability requires a supported posting extension and its own acceptance case.

## Projection compatibility cases

A weekly exempt-deduction projection shifts the current interval by six days for the first future period, twelve days for the second, and so on. A fourteen-day projection shifts it by thirteen and twenty-six days. The daily branch raises an unassigned-date error before expression evaluation; that failure was reproduced in an isolated invocation. Other non-monthly frequencies without a dedicated branch leave their offset at zero. The full payroll runtime was not executed; these results establish the isolated branch behavior and the requirement to resolve projection compatibility before production use.

## Optional loan service boundary

This boundary defines only the loan information and operations consumed by payroll and separation. The [salary loan row](../../schemas/data/record-types/salary_slip_loan.json) holds loan identity, loan-product identity, principal account, interest-income account, principal amount, interest amount, editable total payment and returned repayment identity. Its amounts use company currency. The machine-readable boundary is included under `external_record_contracts` in the [workforce acceptance catalog](../../schemas/mathematics/workforce-acceptance-cases.json).

| External record or operation | Minimum required contract |
| --- | --- |
| Loan record | Stable identity; company; applicant employee identity; submitted document state; repay-from-salary choice; open/closed business state; product identity; term-loan choice; principal and interest-income accounts |
| Loan product record | Stable identity passed to accrual and repayment services; payroll does not infer amortization, rates or eligibility from this identity |
| Calculate amounts | Input loan identity and valuation date equal to salary end date; output total payable amount, interest amount and payable principal amount |
| Prepare term-loan obligations | For eligible term loans, accrue interest up to salary end and generate due demands when that capability exists; the older capability branch prepares term-loan interest only |
| Create repayment | Input loan, employee, company, posting date, product, normal-repayment kind, interest, principal, total payment, payroll payable account, employee-accounting choice and value date equal to salary end; output a saveable repayment record |
| Save and submit repayment | Persist the returned repayment, submit it and store its identity on the salary loan row |
| Cancel repayment | Resolve the salary loan row's repayment identity and cancel that repayment through the loan service's reversal rules |

Loan selection requires submitted state, matching employee and company, salary repayment enabled and business status other than closed. When salary loan rows are empty, fetch eligible loans and add only those with nonzero payable amount. For every row, recalculate the pending amount at salary end and reject a total payment above that amount. Sum stored principal, interest and total payment independently into the slip totals. The inspected payroll validation does not demonstrate that editing total payment proportionately recomputes principal and interest; that consistency is an explicit service acceptance case.

Salary-slip submission creates and submits nonzero loan repayments. It selects the payroll payable account from the linked batch, falling back to the company's default when there is no batch. The bank-payment builder subtracts total loan recovery from cash salary; a loan recovery must therefore not also be included as cash paid to the employee. Cancelling the slip cancels repayment records linked by its loan rows. Repeating submission after a partial failure must preserve one effective repayment per row; the available hook alone does not establish complete retry isolation.

Final settlement additionally consumes a submitted repayment schedule with schedule-row identity, principal amount, interest amount and accrued marker. It queries pending principal, interest, payable amount and penalty information and prepares unaccrued schedule obligations as of the settlement date. Repayment and interest-accrual cancellation are selected by loan and posting date. Multiple same-date repayments therefore require transaction-level selection testing. These integration calls do not specify interest calculation, payment allocation order, amortization, impairment or loan-product policy; those remain responsibilities of a separately specified loan service.
