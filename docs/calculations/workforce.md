# Workforce, pay and benefits

[Complete definitions, units, exceptions and examples](../../schemas/mathematics/workforce-calculations.json) · [Transaction and boundary cases](../../schemas/mathematics/workforce-acceptance-cases.json)

## Whole-period working days

`inclusive_calendar_day_count − excluded_full_holiday_count − 0.5 × excluded_half_holiday_count`

Count the whole pay interval inclusively. Deduct one day per excluded full holiday and half a day per excluded half holiday. Joining and leaving constrain eligible paid days separately.

- Holiday subtraction is zero when holidays are included.
- The denominator covers the whole pay interval, even when joining or leaving occurs within it.

## Payment days after unpaid equivalents

`preliminary_days = employment_interval_days - excluded_employment_holidays; result = preliminary_days - unpaid_leave_equivalents - attendance_absence_equivalents - applicable_unmarked_days when preliminary_days > unpaid_leave_equivalents, otherwise zero; payment_days = result + verified_corrected_days`

Determine the clipped employment interval after holidays. Enter the deduction branch only when that value exceeds unpaid-leave equivalents; otherwise start at zero. In the deduction branch subtract unpaid leave, absence and applicable unmarked days. Add only a positive verified correction last.

- Absence and unmarked-day deductions depend on attendance mode.
- The calculation enters subtraction only when preliminary payment days exceed unpaid leave equivalents; otherwise it starts from zero.
- No universal additional zero floor is applied after absence deductions in the subtraction branch; corrected days are added only after positive verification.

## Approved-leave partial-pay equivalent

`leave_day_fraction * (1 - retained_daily_salary_fraction)`

Use approved leave requests. A full day starts from one unpaid equivalent; a half day starts from one minus the effective half-day wage fraction. Multiply by one minus the retained salary fraction, with a zero retained fraction producing factor one.

- Full-day fraction is one; half-day fraction is one minus configured half-day wage fraction.

## Attendance-mode partial-pay equivalent

`attendance_leave_day_fraction × (1 − retained_daily_salary_fraction)`

Deduct the unpaid complement. A half-day attendance classification already represents the remaining half on a half-working holiday.

- On ordinary full-day leave use 1. For half-day leave use one minus the configured half-day wage share. Full-day absence on a half-working holiday can have a 0.5 day basis.

## Ordinary component payment-day proration

`round_to_field_precision(default_amount * payment_days / integer_part(total_working_days)) + round_to_additional_field_precision(additional_amount * payment_days / integer_part(total_working_days))`

Prorate the structure default and ordinary supplement separately and round them at their respective precisions before adding. Overwriting supplements, already-corrected arrears, accruals and hourly rows have separate branches.

- For an ordinary day-dependent component use the integer part of the whole-period working days as denominator. This formula requires that integer to be positive.
- Overwritten additional salary, accrued payouts, corrections and ordinary time-based wages have separate branches.

## Hourly wage earning

`hour_rate * sum(eligible_time_record_hours)`

Sum working hours from eligible time records whose start date is inside the pay interval. Multiply by the configured rate. A time record already linked to a salary slip must not be paid again.

- Eligible time records have a start date within the slip interval and a permitted submitted or billed state.

## Net pay

`gross_pay - employee_deductions - loan_repayment`

Subtract included employee deductions and optional loan repayment from included gross earnings. Employer contributions do not enter this expression. Negative net pay is rejected on slip submission.

- Employer contributions do not change this net amount.
- Loan repayment requires the optional lending boundary.

## Company-currency conversion

`round_to_destination_precision(transaction_amount * exchange_rate)`

The exchange rate is company-currency units per one transaction-currency unit. Multiply, then round using the destination field precision. Independently converted parent and child amounts can differ at rounding boundaries.

- Final salary rounding is performed independently in salary and company currency.

## Inclusive monthly assessment count

`12 * (end_year - start_year) + end_month - start_month + (1 when end_day >= start_day else 0)`

Count month boundaries by year and month difference and add one when the ending day number is at least the starting day number. This is the monthly period-count convention, not rounded elapsed days divided by thirty.

- Used for monthly payroll when not explicitly payment-day based.

## Other-frequency remaining interval count

`inclusive_days(assessment_end_clipped_to_relief, slip_start) / inclusive_days(slip_end, slip_start)`

For a remaining period count, divide inclusive days from the current slip start to the assessment end clipped by relieving date by inclusive days in the current slip. For the total assessment count use the whole assessment interval instead.

- Remaining factors may be fractional.

## Annual taxable projection

`previous_taxable_earnings + current_structured_taxable_earnings + future_structured_taxable_earnings + current_additional_taxable_earnings + other_income + taxable_unclaimed_benefits - allowed_exemptions`

Combine earlier submitted taxable earnings including eligible opening balances, actual current ordinary taxable earnings, full-period future ordinary earnings, additional earnings and declared other income. Subtract eligible exemptions. Keep immediate-tax bonuses separately identifiable.

- Future structured values use full-payment-day amounts, not the reduced actual current amount.
- Final assessment period uses submitted exemption proof under the specified enforcement rule.

## Inclusive income-tax slab contribution

`zero when annual_income < lower_amount or eligibility_condition fails; otherwise (min(annual_income, upper_amount when supplied otherwise annual_income) - lower_amount + 1) * percentage / 100`

Reject participation when the condition fails or income is below the lower bound. Otherwise use income up to the upper bound, subtract the lower bound, add one currency unit and multiply by the percentage. An absent upper bound means unbounded.

- This expression applies only when annual income is at least the lower bound and the slab condition passes.
- For an unbounded slab substitute annual income for the upper amount.

## Sequential other tax charges

`for each eligible charge: charge_amount = running_tax * percentage / 100; running_tax = running_tax + charge_amount`

Process configured tax charges in row order. Each eligible percentage applies to tax including earlier charges; income limits are inclusive. Return both the total tax and the sum of added charges.

- Minimum and maximum taxable-income limits are inclusive when nonzero.

## Configured income marginal relief

`min(base_tax, annual_income - relief_limit)`

Within the strict marginal-relief interval cap base tax at income exceeding the relief threshold. This is configured regional behavior and does not establish current statutory rates.

- Applies only when annual income is strictly above relief limit and strictly below marginal relief limit.

## Current structured and immediate additional tax

`structured_tax = (annual_ordinary_tax - tax_previously_paid) / remaining_intervals when remaining_intervals > 0, otherwise zero; current_tax = max(0, structured_tax + immediate_bonus_tax)`

Without an explicit additional-tax override, divide unpaid annual ordinary tax by positive remaining periods, or use zero structured tax when no periods remain. Add immediate bonus tax and floor the combined amount at zero.

- When remaining intervals are zero, ordinary current tax is zero rather than divided by zero.
- Additional salary tax override follows its separate overwrite route.
- An explicit additional-tax override replaces the whole current amount and does not also add the immediate bonus-tax difference.

## Current benefit entitlement

`zero when total_assessment_intervals is zero; otherwise annual_benefit / total_assessment_intervals * payment_day_factor`

Divide annual entitlement by total assessment cycles; use zero when that count is zero. When payment-day dependent, multiply by payment days divided by total working days. Apply later payout/cap branches before monetary rounding.

- Payment-day factor is one unless the component is day-dependent.

## Accrued benefit claim eligibility

`prior_accrual + current_cycle_benefit - prior_payout`

For claim-only cycle-accrual benefits, add current-cycle entitlement to prior accrual and subtract prior payouts. For full-benefit claim mode, use yearly entitlement less payouts instead. Already overpaid eligibility is rejected.

- Accrued amount below already-paid amount is rejected in the inspected accrued-claim branch.

## Final-period benefit payout

`max(prior_accrual + current_cycle_benefit - prior_payout - current_claim_payout, 0)`

For end-of-period payout use prior accrual plus current entitlement less prior and current claim payouts, floored at zero. Claim-only mode can first reduce current entitlement for overpayment, so this final expression alone is insufficient for that branch.

- The final-cycle option and benefit payout method control applicability.

## Salary-component-derived overtime rate

`sum(selected_ordinary_earnings) / max(payment_days, 1) / standard_working_hours`

Take selected ordinary earnings excluding additional salary, divide by payment days with minimum one, then divide by the row standard working hours. A zero standard-hours value has no established fallback.

- Exclude additional-salary earnings from the basis.

## Overtime pay

`eligible_overtime_hours * applicable_hourly_rate * selected_multiplier`

Use allowed overtime duration after the applicable cap and multiply by the fixed or component-derived hourly rate and the selected ordinary, rest-day or public-holiday multiplier.

- Weekly rest day and public holiday multiplier replace the standard multiplier when enabled and applicable.
- Attendance-derived hours are capped; manually supplied over-cap hours are rejected.

## Calculated gratuity experience

`(elapsed_joining_to_relief_days - counted_nonworking_attendance_days) / (configured_working_days_per_year when nonzero, otherwise 1)`

Subtract counted non-working attendance from elapsed joining-to-relieving date difference. Divide by configured working days per year, falling back to one for an absent or zero divisor. The relieving endpoint is not included by date subtraction.

- Date subtraction excludes one endpoint, unlike inclusive salary working days.
- A missing or zero annual divisor has a fallback value of one.

## Current-slab gratuity

`eligible_default_earnings * experience_years * selected_slab_fraction`

Use the applicable slab fraction for every eligible experience year and the selected default earning basis from the latest submitted salary slip. Experience must meet the minimum policy threshold.

- Default earnings come from the most recent submitted slip and configured earning components.

## Cumulative-slab gratuity

`eligible_default_earnings * sum(years_consumed_in_band * band_fraction)`

Multiply the width of experience consumed in each band by that band fraction, sum the weighted years and multiply by the eligible ordinary earning basis. This differs from applying the final band to all years.

- The final participating band consumes the remaining years.

## Ordinary payroll-correction amount

`eligible_original_default_amount / original_total_working_days * approved_corrected_days`

For eligible ordinary components prorate original default amount by approved corrected days over original working days. For accrual components instead use original accrual divided by original payment days. A zero denominator is rejected.

- Cumulative corrected days cannot exceed original working days minus payment days.
- Accrual correction uses accrued amount divided by original payment days instead.
- A zero divisor is rejected.

## Retrospective positive salary difference

`new_eligible_amount - existing_eligible_amount, retained only when positive`

Recalculate eligible historical components under the revised structure and keep only positive differences. A reduction does not create negative arrears through this route.

- Negative differences do not become recoveries through this path.

## Each paired attendance interval

`round_half_to_even(total_elapsed_seconds(exit_timestamp, entry_timestamp) / 3600, 2)`

Measure full elapsed seconds between the two timestamps, including date boundaries, divide by three thousand six hundred and round to two decimal places using nearest-even. Pair mode sums these individually rounded intervals.

- Summation happens after each valid pair has been rounded.
- Elapsed seconds include whole days; do not use only the seconds remaining within one day. Malformed reversed endpoints are not clamped by this arithmetic helper.

## Leave application day count

`inclusive_calendar_days - valid_nonholiday_half_day_reduction - excluded_holidays`

Start from the inclusive date count. Subtract a half day only for a valid half-day date that is not a holiday; subtract excluded holiday quantities according to the leave-type setting. Reject nonpositive consumption.

- Half-day reduction is zero when its specified date is a holiday.

## Cycle earned-leave entitlement

`annual_leave / annual_frequency_count * inclusive_days_from_joining / inclusive_cycle_days`

Divide annual entitlement by accrual frequency, prorate only when joining falls after cycle start, then apply quantity precision and the selected leave increment. Carried entitlement is excluded from new-entitlement annual quota checks.

- Joining-day proration applies only when joining is later than cycle start.
- Frequency counts are one, two, four and twelve.
- Apply quantity precision, then optional quarter-, half- or whole-day rounding.

## Carried leave after limits

`min(unused_prior_leave, carry_forward_cap, total_allocation_cap - new_allocation)`

Take unused eligible prior balance subject to a configured carry cap and remaining total-allocation capacity. Unset limits are omitted. Expire the transferred prior balance and record the admitted new balance separately.

- An unset cap is omitted from the minimum.
- Separate validation rejects new allocations above their allowed maximum.

## Maximum encashment days

`min(max(available_balance - nonencashable_retention, 0), encashment_cap)`

Remove the non-encashable retention from the available leave balance with a zero floor; then apply an optional encashment cap. An unset cap is not a zero-day prohibition.

- An unset cap does not limit the remaining balance.

## Leave encashment amount

`selected_encashment_days * positive_per_day_amount`

Multiply selected eligible days by the positive rate from the latest applicable salary assignment, falling back to the structure rate when the assignment value is zero. Submit through exactly one chosen payout route.

- Latest eligible assignment supplies the rate, falling back to structure rate.

## Compensatory leave earned

`inclusive_worked_holiday_days - selected_half_day_reduction`

Count inclusive eligible worked holidays and subtract one half when a valid half-day claim is selected. Every day requires qualifying submitted attendance; entitlement begins the day after the worked interval.

- Every day must be a holiday with eligible submitted attendance.
- Entitlement begins the day after the work interval ends.

## Expense percentage tax

`round_to_tax_precision(total_sanctioned_amount * percentage / 100)`

For each nonzero-rate tax row, multiply total sanctioned spending by that rate and round at the tax-row precision. Zero-rate rows retain their manually supplied amount. Percentage expense taxes do not compound.

- Each percentage tax uses the same sanctioned base; expense taxes do not compound.

## Claim residual payable

`total_sanctioned_amount + total_taxes - allocated_advances`

Approved spending plus tax is the whole expense obligation; subtract eligible allocated advances to obtain the remaining employee payable. Parent monetary rounding is applied after arithmetic.

## Available paid advance

`paid_amount - claimed_amount - returned_amount`

From posted paid advance movements subtract submitted approved claim allocations and posted returns. The remaining available amount identifies a receivable balance, not a new reimbursement claim.

- Paid amount cannot exceed requested advance; returns cannot exceed paid less claimed.

## Single advance exchange difference

`allocated_foreign_amount * (claim_exchange_rate - original_advance_exchange_rate)`

For one eligible allocation compare its company amount at claim rate with the company amount at original advance rate. The multiple-row compatibility path separately accumulates running differences and is row-order sensitive.

## Vehicle-originated claim amount

`sum(service_expense_rows) + fuel_quantity * fuel_unit_price`

Add maintenance/service rows and fuel quantity times unit price. Vehicle distance itself does not multiply an automatic mileage reimbursement rate in this preparation action.

- Preparing the claim does not approve or post it.

## Incremental staffing budget

`sum(vacancies_by_designation * estimated_cost_per_position)`

Multiply each designation vacancy count by estimated cost per new position and sum rows. Existing employees affect planned headcount but do not multiply the incremental vacancy cost.

- Current employees contribute to planned position count but not vacancy cost.

## Offer acceptance rate

`100 * submitted_accepted_offers / all_submitted_offers`

Count accepted submitted offers over all submitted offers. Use zero for an empty population. Business response status and document submission state both affect the numerator.

- Return zero when the denominator is zero.

## Individual interview feedback average

`sum(skill_ratings) / count(skill_rows)`

Sum skill ratings and divide by all assessment rows, including unrated rows counted as zero. An empty assessment table produces zero. Store field precision before interview-wide aggregation.

- Unrated rows remain in the denominator; an empty table produces zero.
- The example is the arithmetic stage before rating-field storage rounding; saved ratings can have scale two.

## Overall interview average

`arithmetic_mean(submitted_feedback_averages)`

Average the saved averages of submitted individual feedback documents. Every feedback document has equal weight regardless of its number of skill rows. Cancellation removes that feedback from the aggregate.

- Do not pool skill rows across interviewers; each submitted feedback has equal weight.
- Actual aggregation uses saved feedback averages. The example isolates mathematical aggregation; apply storage scale before composing it with saved feedback.

## Goal-derived five-point appraisal score

`sum(result_area_completion_percent * result_area_weight_percent / 100) / 20`

Average top-level non-archived goal completion within each result area, weight by that result-area percentage, sum and divide by twenty to convert percentage completion to a five-point score.

- Each completion value averages top-level non-archived goals.

## Default final appraisal score

`(goal_score + average_feedback_score + self_assessment_score) / 3`

Average goal score, submitted reviewer average and self-assessment score with fixed denominator three. Missing categories contribute zero. A configured final-score expression explicitly replaces this default.

- Missing categories are not omitted from the denominator.
- A configured final-score expression replaces this default.

## Separate final settlement totals

`payable_total = sum(payable_rows); receivable_total = sum(receivable_rows) + asset_recovery_cost`

Keep payable and receivable totals separate. Add asset-recovery cost only to receivables and retain every obligation reference and settled status. A display net amount cannot replace those records.

- Keep separate obligation records and their settlement states.

## Future ordinary taxable projection

`full_period_taxable_earnings * (round_half_to_even(remaining_period_count) - 1)`

No ceiling is substituted for nearest-even rounding of the remaining-period count.

- No ceiling is substituted for nearest-even rounding of the remaining-period count.

## Future ordinary non-taxable projection

`recalculated_full_period_nontaxable_earnings * (ceiling(remaining_period_count) - 1)`

Recalculate a copy of the salary slip with payment days equal to working days; exclude additional-salary rows from ordinary future earnings.

- Recalculate a copy of the salary slip with payment days equal to working days; exclude additional-salary rows from ordinary future earnings.

## Claim-only benefit after excess payout

`current_entitlement - max(prior_payout + current_claim_payout - prior_accrual, 0)`

Then apply the strictly positive remaining-yearly-entitlement cap and optional final payout branch. Nonpositive resulting rows are omitted.

- Then apply the strictly positive remaining-yearly-entitlement cap and optional final payout branch. Nonpositive resulting rows are omitted.

## Cumulative multiple-advance exchange difference

`running_difference begins at zero; for each eligible row add rounded local difference; when running_difference is nonzero store it on the row and add it to document_difference`

Observed compatibility behavior is row-order sensitive; an independent sum of 30 is a separate financial correction candidate.

- Observed compatibility behavior is row-order sensitive; an independent sum of 30 is a separate financial correction candidate.

## Weighted self-assessment score

`sum(normalised_rating * configured_star_count * criterion_weight / 100)`

Apply score-field precision after summing; weights must meet the applicable validation rule.

- Apply score-field precision after summing; weights must meet the applicable validation rule.

## Parent goal completion

`sum(direct_nonarchived_child_completion) / count(direct_nonarchived_children)`

Closed children remain eligible; archived children do not. Moving a child refreshes old and new parents.

- Closed children remain eligible; archived children do not. Moving a child refreshes old and new parents.

## Offsetting advance differences under cumulative behavior

`apply ordered cumulative multiple-advance difference rule`

The second row does not trigger a nonzero update; this does not equal independent net exchange exposure.

- The second row does not trigger a nonzero update; this does not equal independent net exchange exposure.
