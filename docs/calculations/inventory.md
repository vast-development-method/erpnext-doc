# Inventory, production and fulfilment

[Complete definitions, units, exceptions and examples](../../schemas/mathematics/inventory-calculations.json) · [Transaction and boundary cases](../../schemas/mathematics/inventory-acceptance-cases.json)

## Transaction quantity to stock quantity

`transaction_quantity × stock_units_per_transaction_unit`

Read the factor stored on the transaction row; multiply its commercial quantity by that factor; apply the destination quantity precision and the stock unit whole-number restriction. Never infer the factor from price or parcel size.

Preserve transaction factor; apply target stock quantity field precision and whole-number constraint.

- Stock unit conversion must equal one.
- Product unit conversion rows must not repeat a unit.

## Price per stock unit

`transaction_unit_price ÷ stock_units_per_transaction_unit`

Divide the price per selected transaction unit by stock units per that unit. Preserve document currency. Quantity times transaction price must equal converted stock quantity times unrounded stock-unit price.

Do not infer factor from a price or package dimension; the inspected rate helper treats a missing factor as one.

- A selected factor of zero cannot be used as an actual divisor.

## Bundle component stock requirement

`component_quantity_per_parent_stock_unit × parent_stock_quantity`

Resolve the selected eligible composition version; multiply each component quantity by the parent stock quantity. Retain the commercial parent row and component reference, including duplicate components belonging to different parents.

Preserve parent row identity; do not aggregate unrelated parents before applying return references.

- Do not post another stock movement for a non-stock commercial parent.

## Net weight of a packing slip

`round(sum(row.quantity × row.net_weight_per_unit), 2)`

Require a common row weight unit. Fill absent row weights from product defaults, multiply packed row quantities by unit weights, sum and round the total to two decimal places. Inclusive case count does not multiply row quantity.

Round the total to two decimal places after summing products.

- All row weight units must match.
- Gross weight defaults to net weight only when its entered value is empty or zero.

## Total shipment parcel weight

`sum(parcel.weight × parcel.count for parcels whose count is positive)`

Require every parcel weight to be positive. Sum weight times count only for positive-count parcel rows. Do not derive volumetric weight or alter commercial stock quantity.

Parcel weight field has one decimal place in inspected metadata; no separate total rounding appears in the helper.

- Every parcel weight must be positive.
- This expression is physical weight, not a carrier dimensional-weight tariff.

## Projected inventory quantity

`actual_quantity + ordered_quantity + requested_quantity + planned_quantity − sales_reserved_quantity − production_reserved_quantity − subcontract_reserved_quantity − production_plan_reserved_quantity`

Add physical quantity and eligible inbound planning counters, then subtract the four outbound planning counters. Explicit reservations are a separate physical-claim measure and must not be subtracted a second time here.

Sum planning counters; explicit physical reservation is not an additional term here.

- All operands must refer to the same product and warehouse planning scope.

## Unclaimed physical stock

`actual_quantity − sum(reserved_quantity − delivered_quantity − transferred_quantity − consumed_quantity)`

Within a protected product-and-warehouse state, subtract each active claim remainder from actual stock. The remainder deducts delivered, transferred and consumed quantities from reserved quantity.

Read and write under exclusion of competing claims for the same stock scope, including the first claim.

- Exclude current reservation when recomputing its permitted update.
- Batch-specific path uses batch availability.

## Maximum claim against a source row

`minimum(available_quantity, source_quantity − delivered_quantity − other_source_reservations)`

Convert source delivered quantity to stock units where needed. Compare source remaining demand with warehouse availability, choose the smaller and compare proposed reservation at reservation quantity precision.

Round allowed quantity and candidate reservation to reservation field precision before comparison.

- Candidate quantity cannot exceed this maximum.
- Candidate reserved quantity must be greater than delivered quantity on the reservation.

## Moving average receipt while previous inventory is positive

`(previous_quantity × previous_rate + incoming_quantity × incoming_rate) ÷ (previous_quantity + incoming_quantity)`

For positive preceding stock and a positive receipt, add receipt value to carried value and divide by resulting quantity. Preserve rate precision and round the carried company-currency amount at its own precision.

Next stock value is rounded to currency precision; nonzero quantity is rounded to quantity precision before recalculated carried rate.

- If previous quantity is zero or negative and receipt makes next quantity nonnegative, use incoming rate directly.

## Moving average issue with specified outgoing rate

`(previous_quantity × previous_rate + signed_issue_quantity × outgoing_rate) ÷ (previous_quantity + signed_issue_quantity)`

For a nonzero remainder, subtract issue quantity valued at its explicit outgoing rate from prior value, then divide by remaining quantity. This may change the remaining average, especially for a purchase return.

Apply only when resulting quantity is nonzero; currency and quantity precision follow ledger processing.

- When resulting quantity is zero, keep outgoing rate as rate state and set stock value zero.
- An ordinary issue without specified outgoing rate normally retains average rate.

## Monetary change caused by a stock ledger row

`rounded_next_stock_value − previous_carried_value`

First determine and round next inventory value under the selected method; force zero value at zero physical balance; subtract previously carried rounded value. Financial inventory movement follows this difference, not selling price.

Round next value to currency precision first; force zero value when quantity is exactly zero.

- A reconciliation may replace target quantity and rate rather than adding a receipt.

## Inventory carried at effective standard

`next_quantity × effective_standard_rate`

Select the approved standard effective on the posting date. Multiply the resulting quantity by that standard, independently of purchase or actual manufacturing cost. Recognise price or manufacturing variance separately.

Use standard effective on posting date, then currency precision for stock value.

- Missing effective standard fails.
- A posting before the latest approved effective date fails.
- Serial and batch cost paths do not override standard carrying value.

## Manufacturing variance under standard cost

This calculation belongs to the [optional standard-cost policy](../operations/inventory-and-valuation.md#standard-cost-and-effective-dating).

`consumed_material_value + additional_cost − finished_standard_value`

For a qualifying finished row, subtract actual posted standard inventory value from its intended actual incoming amount, including allocated material, additional and landed cost. Positive variance is an expense debit and negative variance an expense credit.

Use monetary ledger values rather than a rounded displayed per-unit rate.

- Post to configured manufacturing variance account.
- Finished inventory remains at standard.

## Automatic landed charge distribution

`total_charges × row_basis ÷ sum_of_bases`

Sum the selected quantity or amount basis. Reject a zero total. Calculate each proportional share, round it at its field precision, and allocate the full residual to the final item row in preserved order.

Round each row to applicable charge precision; assign total minus sum of rounded rows to final row.

- Zero total allocation basis fails.
- Row sequence determines which row receives the residual.

## Manual landed allocation reconciliation threshold

`abs(round(difference, currency_precision)) < 2 ÷ (10 raised to currency_precision)`

Validate nonzero manual total, subtract allocated charges from required charges, and round the difference at company-currency precision. Absorb the difference into the final row only when its absolute amount is strictly below two smallest currency units.

Round the difference before testing the strict less-than threshold.

- If true, assign difference to last row.
- If false, fail reconciliation.

## Putaway quantity constrained to whole commercial units

`floor(minimum(pending_stock_quantity, free_stock_capacity) ÷ conversion_factor)`

Subtract current stock from capacity converted to stock units. Take the smaller of free capacity and pending stock quantity, divide by the row factor, and floor to a whole transaction quantity when the selected unit requires integers.

Apply floor only when commercial unit requires whole numbers; multiply result by factor for actual stock allocation.

- This is quantity capacity and does not determine geometric parcel fit.

## Unordered quantity mapped from quotation

`maximum(quoted_stock_quantity − already_ordered_stock_quantity − already_mapped_stock_quantity, 0) ÷ conversion_factor`

Subtract stock already ordered and stock already mapped into the current draft from quoted stock, clamp negative remainder to zero, then divide by the original factor. Apply the selected-alternative and unit-price row eligibility rules separately.

Subtract in stock units before converting to source transaction units.

- Alternative eligibility and quantity-zero unit-price exceptions are tested separately.

## Billable order quantity after returns and replacement delivery

`minimum(ordered_quantity, maximum(ordered_quantity − returned_quantity, delivered_quantity))`

Use returned quantity to reduce the original billable requirement unless actual replacement delivery supports a larger billable quantity; cap it at original ordered quantity before subtracting existing billing and current draft mapping.

Then subtract submitted billed quantity and target draft mapped quantity; round and clamp pending result to zero.

- Replacement delivery can restore billing eligibility.
- Quantity-zero unit-price rows follow a separate contract.

## Pick requirement without double subtracting delivered stock

`ordered_quantity − maximum(picked_stock_quantity ÷ conversion_factor, delivered_quantity)`

Convert already-picked stock into the order unit. Subtract the greater of picked and delivered quantities from ordered quantity, because delivery may already be included in picking. Do not subtract both independently.

Convert picked quantity before comparing; target stock quantity multiplies the result by factor.

- Ordinary order-to-pick-list mapping fails when order has explicit reserved stock.

## Purchase order receiving allowance

`ordered_quantity × (100 + allowance_percentage) ÷ 100`

Increase original ordered quantity by the permitted percentage to obtain the upper posting limit. The ordinary mapper proposes ordered quantity less received quantity and the amount already in the draft. It omits a fully allocated ordinary row. For 10 ordered and 10 received, a 10% allowance gives a posting ceiling of 11 and an ordinary proposal of zero.

A deployment may offer a separate proposal for the unused allowance once ordinary demand is exhausted. That policy requires an explicit mapper and remains subject to the posting checks.

- Exclude closed orders and supplier-direct rows. A deployment with the independent row-closure capability also excludes closed lines.
- Subtract quantity already included in current draft.

## Recipe percentage converted to component entry unit

Core input recipes store a component quantity and its unit conversion. Compute input stock quantity as entered quantity times the unit factor, then scale material requirements to production output. A percentage allocation on a secondary output distributes cost and does not set an input ingredient quantity. The following formula applies to the optional percentage-input recipe model, where the material rows explicitly carry percentages and a balance-row designation.

`component_percentage ÷ 100 × recipe_quantity × batch_unit_to_component_unit_factor`

Resolve the sole optional balance percentage, require total percentage within tolerance of one hundred, resolve a valid dimensional conversion, multiply batch quantity by component percentage and unit factor, and round at the component quantity field.

Round result to component quantity field precision after multiplication.

- Total percentages within 0.0001 percentage points of one hundred.
- Only one balance component, with positive remainder.
- General unit conversion must exist.

## Nested material requirement

`child_component_stock_quantity ÷ child_recipe_output_quantity × parent_required_subassembly_stock_quantity`

Divide child component stock quantity by child output quantity and multiply by required subassembly stock quantity. Repeat down acyclic recipe links. Keep operation identity when grouping leaf demand; never round an intermediate per-unit quotient prematurely.

Use complete recipe quantities rather than prematurely rounded stored per-output quotient.

- Preserve operation identity when grouping.
- Do not count phantom grouping as an additional physical component.

## Cost of an operation duration

`hourly_cost × operation_minutes ÷ 60`

Convert recorded minutes to hours before multiplying by the hourly rate. Recipe per-batch and output-based rules are additional scaling steps, while actual work-order cost retains the amount already consumed by prior receipts.

Work-order operation amounts round to their amount precision; recipe operation conversion follows company factor.

- Planned and actual duration are distinct operands on distinct calculations.

## Primary output material-derived rate after secondary allocations

`(consumed_material_cost − own_cost_secondary_value) × primary_allocation_percentage ÷ 100 ÷ finished_stock_quantity`

Value own-cost secondary outputs first; deduct them once from actual consumed material cost. Apply the primary allocation percentage to that residual pool and divide by actual primary stock quantity. Actual zero cost does not trigger a historical-price fallback.

Value own-cost secondary output before percentage rows; do not round derived basic rate early.

- Known zero consumed cost remains zero and does not trigger unrelated fallback.
- Additional costs are allocated separately afterward.
- An installed standard-cost capability can set the final carrying amount and record its variance.

## Stock entry valuation rate including charges

`basic_rate + (additional_cost + landed_cost) ÷ stock_quantity`

After the basic material rate is known, add the row additional and landed costs divided by row stock quantity. Manufacture and repack allocate ordinary additional charges only to eligible primary finished rows.

Do not round valuation rate; round row amount separately after summing basic amount and charges.

- Only calculate division when stock quantity is nonzero.

## Expected process loss quantity

`recipe_quantity × loss_percentage ÷ 100`

Multiply recipe output by loss percentage; validate allowed percentage and whole-number quantity constraints. At manufacture the completed quantity equals actual finished quantity plus process loss, with no fabricated stock receipt for loss.

Secondary loss uses recipe quantity precision; reject fractional loss for whole-number units.

- Main recipe loss greater than one hundred percent fails.
- Loss quantity is not a positive inventory receipt.

## Arithmetic mean of entered observations

`sum(observations) ÷ count(observations), or zero when no observations`

Interpret supplied finite numeric observations using their applicable number format, exclude blank observations, divide their sum by count, and provide zero when none exists. Individual missing formula variables can still be zero.

The average uses the parsed input values without an additional rounding step.

- Missing observations excluded from mean.
- Individual missing formula variables are supplied as zero separately.

## Precision-dependent negative stock rejection

`difference = round(previous_quantity + signed_movement_quantity − reserved_quantity, quantity_precision); reject when difference < 0 and abs(difference) > threshold; threshold = 0.0001 when quantity_precision <= 4, otherwise 10 raised to negative quantity_precision`

Subtract protected stock reservations after applying signed movement quantity, round at stock quantity precision, and reject only a negative amount whose absolute size strictly exceeds the documented threshold. Tracked identity validation remains independent.

Round quantity difference before the strict magnitude comparison.

- Applies when negative-stock validation is active.
- Batch-specific allowance is separately configurable.

## Purchase price variance under standard cost

This calculation belongs to the [optional standard-cost policy](../operations/inventory-and-valuation.md#standard-cost-and-effective-dating).

`full_incoming_transaction_amount − posted_standard_inventory_value`

Round at financial posting precision. Positive variance debits the dedicated purchase price variance account; do not post it again when the later invoice only clears the receipt.

Round at financial posting precision. Positive variance debits the dedicated purchase price variance account; do not post it again when the later invoice only clears the receipt.

- Round at financial posting precision. Positive variance debits the dedicated purchase price variance account; do not post it again when the later invoice only clears the receipt.

## On-hand inventory revaluation after a standard change

`on_hand_quantity × (new_standard_rate − previous_standard_rate)`

Use the validated effective date and current on-hand quantity; zero quantity change. The corresponding revaluation posting balances the financial value movement.

Use the validated effective date and current on-hand quantity; zero quantity change. The corresponding revaluation posting balances the financial value movement.

- Use the validated effective date and current on-hand quantity; zero quantity change. The corresponding revaluation posting balances the financial value movement.

## Absolute inventory count adjustment

`counted_quantity − prior_effective_quantity; target_value = counted_quantity × selected_rate`

This ordinary nondimension, nonbatch case sets an absolute target rather than adding the counted quantity. Compare value against previously carried value.

This ordinary nondimension, nonbatch case sets an absolute target rather than adding the counted quantity. Compare value against previously carried value.

- This ordinary nondimension, nonbatch case sets an absolute target rather than adding the counted quantity. Compare value against previously carried value.

## Additional landed cost retained after partial consumption

`landed_cost_increment × remaining_received_quantity ÷ original_received_quantity`

Applicable to one isolated receipt with no other cost layers, returns or intervening valuation changes. Repost historical issues and dependent transfers; the example is not a universal shortcut for mixed layers.

Applicable to one isolated receipt with no other cost layers, returns or intervening valuation changes. Repost historical issues and dependent transfers; the example is not a universal shortcut for mixed layers.

- Applicable to one isolated receipt with no other cost layers, returns or intervening valuation changes. Repost historical issues and dependent transfers; the example is not a universal shortcut for mixed layers.

## Invoice quantity after prior billing and current draft allocation

`maximum(round(billable_after_returns − submitted_billed_quantity − quantity_already_in_target, quantity_precision), 0)`

Use the billable-after-returns calculation before subtracting existing invoices. Unit-price rows and permitted overbilling amounts have separate eligibility contracts.

Use the billable-after-returns calculation before subtracting existing invoices. Unit-price rows and permitted overbilling amounts have separate eligibility contracts.

- Use the billable-after-returns calculation before subtracting existing invoices. Unit-price rows and permitted overbilling amounts have separate eligibility contracts.

## Cumulative reference return quantity

`original_returnable_quantity − effective_previous_return_quantity`

Use stock quantity for stock-updating returns and transaction quantity for invoices without stock update. Preserve separate accepted and rejected return limits and all predecessor links.

Use stock quantity for stock-updating returns and transaction quantity for invoices without stock update. Preserve separate accepted and rejected return limits and all predecessor links.

- Use stock quantity for stock-updating returns and transaction quantity for invoices without stock update. Preserve separate accepted and rejected return limits and all predecessor links.

## Usable output after process loss

`completed_quantity − process_loss_quantity`

Compare at stock movement quantity precision. The loss is not a separately valued inventory output.

Compare at stock movement quantity precision. The loss is not a separately valued inventory output.

- Compare at stock movement quantity precision. The loss is not a separately valued inventory output.

## Material rate on usable output after loss

`(consumed_material_value − secondary_output_value) ÷ actual_finished_quantity`

Applicable to one fully allocated primary output with positive usable quantity. Under the optional standard-cost policy the approved standard controls carrying value and the difference posts as variance.

Applicable to one fully allocated primary output with positive usable quantity. Under the optional standard-cost policy the approved standard controls carrying value and the difference posts as variance.

- Applicable to one fully allocated primary output with positive usable quantity. Under the optional standard-cost policy the approved standard controls carrying value and the difference posts as variance.

## Actual operating cost available for later production

`eligible_actual_operation_cost − operation_cost_already_capitalised`

Allocate only the eligible remaining portion to subsequent output and cap allocation at available cost. Preserve the consumed-cost references across retries.

Allocate only the eligible remaining portion to subsequent output and cap allocation at available cost. Preserve the consumed-cost references across retries.

- Allocate only the eligible remaining portion to subsequent output and cap allocation at available cost. Preserve the consumed-cost references across retries.

## Service quantity for customer-owned manufacture

`finished_quantity × subcontracting_conversion_factor`

Service quantity differs from finished stock quantity. Multiply service quantity by service rate for invoicing amount and preserve the referenced sales-order row.

Service quantity differs from finished stock quantity. Multiply service quantity by service rate for invoicing amount and preserve the referenced sales-order row.

- Service quantity differs from finished stock quantity. Multiply service quantity by service rate for invoicing amount and preserve the referenced sales-order row.

## Inclusive numerical range acceptance

`supplied_reading_count > 0 and every supplied reading >= lower_bound and <= upper_bound`

Ignore blank observations for range evaluation. Every supplied value must pass; an accepted mean does not override an out-of-range observation.

Ignore blank observations for range evaluation. Every supplied value must pass; an accepted mean does not override an out-of-range observation.

- Ignore blank observations for range evaluation. Every supplied value must pass; an accepted mean does not override an out-of-range observation.

## Overall quality review state

`Open when no rows or any row Open; otherwise Failed when any row Failed; otherwise Passed`

Evaluate unresolved objectives before final failure. Objective target text does not independently calculate the row state.

Evaluate unresolved objectives before final failure. Objective target text does not independently calculate the row state.

- Evaluate unresolved objectives before final failure. Objective target text does not independently calculate the row state.
