# Customers, projects and service

[Complete definitions, units, exceptions and examples](customer-and-service-calculations.json) · [Transaction and boundary cases](customer-and-service-acceptance-cases.json)

## Commercial product discount

`product_amount = quantity * rate; discount_amount = product_amount * discount_percentage / 100; net_amount = product_amount - discount_amount`

- Interactive calculation observed; authoritative noninteractive total validation needs separate evidence.
- A genuine zero net amount from a full discount must not fall back to gross.

## Commercial probability weighted forecast

`forecast_contribution = expected_value * probability_percentage / 100 * stored_exchange_rate`

- This expression applies to categories other than lost. Missing exchange rate is treated as one; missing probability is zero.

## Lost opportunity forecast contribution

`forecast_contribution = expected_value * stored_exchange_rate`

- Counterintuitive specified compatibility behavior; excluding lost value would be an explicit specification change.

## Project task count completion

`completion_percentage = round_to_configured_precision(100 * (completed_task_count + cancelled_task_count) / total_task_count, 2)`

- No tasks yields zero for calculated methods; explicit completion without tasks switches to manual at 100.

## Project weighted completion

`completion_percentage = round(sum(effective_task_progress × task_weight) / total_task_weight, 2)`

- Completed and cancelled tasks contribute 100 percent. When total weight is zero give each task unit weight. An empty task set gives zero for calculated methods.

## Time cost and billable amount

`costing_amount = actual_hours * costing_rate; billing_amount = billing_hours * billing_rate`

- Billing hours exceeding actual hours warns and does not reject.
- Zero billing hours on a billable row default to actual hours; nonbillable rows have zero billing hours.

## Remaining time invoice rate

`remaining_hours = billable_hours - billed_hours; remaining_amount = billable_amount - billed_amount; effective_rate = remaining_amount / remaining_hours`

- Reject when no billable hours or all hours billed. Apply invoice field precision after deriving rate; the exact effective rate is expressed as a reduced fraction to avoid inventing output precision.

## Project gross margin

`expense_amount = labour_cost + purchase_cost + consumed_material_cost; gross_margin = billed_amount - expense_amount; margin_percentage = 100 * gross_margin / billed_amount when billed_amount is nonzero, otherwise 0`

- Management aggregate, not a claim to reconcile to all general-ledger expense.

## Working time response deadline

`deadline = consume_service_seconds(start_timestamp, target_seconds, weekday_windows, holiday_dates)`

- Opening boundary included; closing boundary excluded.
- No timezone offset is assumed by this local calendar example.
- Empty positive-capacity calendar lacks a terminating termination guarantee.

## Issue resolution target hold extension

`resolution_deadline = calendar_deadline + round_to_configured_precision(total_hold_seconds) wall-clock seconds`

- Accumulated hold is not consumed through the business calendar again.

## Regional charge on charge

`taxable_charge = referenced_charge_amount; tax_amount = referenced_charge_amount * tax_percentage / 100`

- Additional exported charge row has quantity one; exact external serialization remains separate.

## Equal task weight rounding

`round((100 × 1 + 100 × 1 + 100 × 1) / (1 + 1 + 1), 2)`

- Round the final weighted mean.

## Zero weight project completion

`completion_percentage = round(sum(effective_task_progress) / task_count, 2) when total weight is zero and tasks exist`

## Time billed percentage zero price

`billed_percentage = 100 * billed_hours / billable_hours when billed monetary ratio is unavailable and both hours are positive`

## Maintenance visit spacing

`visit_interval_days = date_difference(end_date, start_date) / visit_count; each nominal_visit_date advances by visit_interval_days`

- Holiday adjustment moves backwards; example assumes no holidays.
- Fractional day handling needs a date utility fixture rather than a calendar-month substitution.
- Coverage end derivation and minimum inclusive coverage validation use different quarterly and half-yearly day counts. Nominal spacing uses elapsed day difference, not inclusive day count.

## Dependent task rescheduling

`rescheduled_start = prerequisite_end + 1 day; preserved_duration_days = original_end - original_start; rescheduled_end = rescheduled_start + preserved_duration_days`

- Applies only when dependent beginning is strictly before prerequisite end and both dependent expected dates exist.

## Campaign final date

`campaign_end_date = campaign_start_date + maximum(schedule_delay_days)`

- At least one scheduled entry is required.

## Project task progress average

`completion_percentage = round(sum(effective_task_progress_percentages) / total_task_count, 2) for a nonempty set, otherwise zero`

- Completed and cancelled tasks contribute 100. Other tasks contribute their recorded progress.

## Commercial full discount forecast fallback

`new_expected_value = nonzero(product_net_total) otherwise product_total, only when automatic refresh is enabled and previous_expected_value is nonzero`

- This changes the opportunity forecast field only; it does not change the zero net product amount or authorise an invoice for gross value.

## Company master visibility

`visible_by_company_helper = restriction_disabled or actor_restriction_absent or nonempty_intersection(master_companies, actor_companies)`

- Ordinary record permission remains a separate predicate.

## Company membership edit authority

`changed_companies = symmetric_difference(previous_companies, new_companies); permitted = actor_restriction_absent or changed_companies is a subset of actor_companies`

- Removing an unauthorised company is protected just as adding it is.

## Time interval overlap

`overlap = maximum(first_beginning, second_beginning) < minimum(first_ending, second_ending)`

- Applies independently to each enabled user or employee identity overlap check.

## Project invoice row attribution

`effective_project = invoice_parent_project only when row_project is null, otherwise row_project`

- An empty string differs from a null row project. Include only submitted invoice lines and keep credits signed.

## Working time response elapsed

`elapsed_service_seconds = sum(eligible one-second steps from beginning inclusive to ending exclusive)`

- Thirty service minutes on Friday and sixty on Tuesday.

## Issue first response outside window

`issue_metric = one second when equal day-of-month branch finds neither timestamp inside support hours`

- Issue helper includes closing and ignores holiday dates in its weekday-window branches.

## Supplier import first installment adjustment

`difference = sum(imported_installments) - calculated_invoice_total; adjusted_first_installment = first_imported_installment - difference; later installments unchanged`

- A difference greater than the first installment can make that installment negative under the compatibility routine.

## Supplier import carried quantity

`quantity remains previous quantity when current line_total / unit_rate equals one; prepared_amount = carried_quantity * absolute(unit_rate)`

- This is a documented compatibility defect, not a recommended independent-row import design.

## Regional tax inclusive export price

`tax_divisor = 1 + tax_percentage / 100; exported_unit_price = price_list_rate / tax_divisor; exported_amount_margin = amount_margin / tax_divisor`

## Regional tax bucket gross

`gross_amount = taxable_amount + tax_amount`

- Zero-rate tax buckets require an explicitly zero-rated item marker in the South African audit.

## Contract fulfilment result

`zero completed rows => unfulfilled; some but not all => partially fulfilled; all => fulfilled; incomplete and current_date > deadline => lapsed`

- An empty required checklist follows the zero-completed branch and is unfulfilled. Daily activation refresh does not recalculate this field.
