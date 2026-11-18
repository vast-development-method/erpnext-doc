# Financial recognition, pricing and settlement

[Complete definitions, units, exceptions and examples](financial-calculations.json) · [Transaction and boundary cases](accounting-acceptance-cases.json)

## Convert a commercial amount to company currency

`round(round(commercial_amount, commercial_precision) × conversion_rate, company_precision)`

- Round the commercial field before multiplication
- Multiply by the document conversion rate
- Round to the company field precision

## Convert ledger amounts to reporting currency

`reporting_amount = company_amount × reporting_rate`

- Resolve company and reporting currencies
- Use transaction date when present, otherwise posting date
- Require a valid rate
- Calculate reporting debit and credit separately

- The body does not explicitly round these multiplications to a field precision.

## Price after percentage or amount margin

`percentage mode: list_rate × (1 + margin_percentage ÷ 100); amount mode: list_rate + margin_amount`

- Resolve the applicable price rule
- Apply percentage or amount margin before discount

## Apply per-unit discount after margin

`discount_amount = round(margin_inclusive_rate × discount_percentage ÷ 100, discount_precision); accepted_rate = round(margin_inclusive_rate − discount_amount, rate_precision)`

- Calculate percentage discount when percentage is positive
- Use resulting or explicitly supplied amount discount
- Subtract and round accepted unit rate

- A manually supplied rate can override reconstructed margin and discount where no applicable pricing rule forces them.

## Commercial quantity and price extension

`line_amount = round(accepted_rate × commercial_quantity, amount_precision)`

- Validate permitted quantity semantics
- Multiply commercial quantity by accepted rate
- Round line amount

- A permitted value-only return with zero quantity uses negative accepted rate as amount.
- A permitted value-only debit adjustment uses positive accepted rate as amount.

## Compound a percentage discount on the remaining price

`combined_discount_percentage = previous_discount_percentage + (100 − previous_discount_percentage) × next_discount_percentage ÷ 100`

- Apply eligible multiple rules in ascending priority sequence
- Apply this formula only when the rule discounts the remaining rate

## Recursive free-product quantity

`continuous award = (eligible_quantity − offset_quantity) × free_quantity_per_interval ÷ repeat_interval_quantity; whole award = floor((eligible_quantity − offset_quantity) ÷ repeat_interval_quantity) × free_quantity_per_interval`

- Apply normal rule quantity eligibility
- Remove configured offset
- Apply recursion only for positive remaining quantity
- Floor intervals only when whole awards are enabled

## Tax on the current item net amount

`tax_amount = tax_percentage ÷ 100 × selected_net_amount`

- Use item account-rate override where supplied
- For included tax before document-discount recomputation use unrounded inclusive net when available
- Otherwise use rounded item net
- Apply row rounding only when enabled

## Allocate a document fixed charge across items

`share = item_net_amount × document_charge ÷ document_net_total; final_share = calculated_final_share + document_charge − sum(all_calculated_shares)`

- Return initial zero share when document net total is zero
- Apply row rounding policy
- Track remaining actual charge
- Add final residual to last participating item

## Tax on an earlier tax row amount

`tax_amount = tax_percentage ÷ 100 × previous_tax_amount`

- Require an ordered earlier-row reference
- Use its current-item amount rather than document tax total

## Tax on an earlier cumulative item amount

`tax_amount = tax_percentage ÷ 100 × previous_cumulative_total`

- Resolve referenced cumulative row
- Multiply its current-item total by current rate

## Tax charged per commercial unit

`tax_amount = tax_rate_per_unit × commercial_quantity`

- Apply tax applicability
- Multiply by commercial quantity, not implicitly by stock quantity

## Tax on an extension-resolved fixed base

`tax_amount = resolved_base × tax_percentage ÷ 100`

- Resolve registered taxable-base behaviour
- Apply rate
- For inclusive extraction treat the amount as an intercept independent of unknown net

## Extract net from inclusive ordered taxes

`unrounded_net = (printed_amount − quantity × total_tax_intercept_per_unit) ÷ (1 + total_tax_slope)`

- Derive each included tax slope and intercept in row order
- Negate included deductions
- Subtract total fixed contribution
- Divide by net coefficient
- Retain unrounded net for applicable included taxes
- Round stored net and then derive net unit rate

## Distribute trade discount and correct running rounding

`raw_share = discount_amount × item_net_amount ÷ discountable_total; adjusted_net = item_net_amount − raw_share; correction = round(running_expected_net − running_rounded_net, document_net_precision)`

- Compute raw proportional share
- Round adjusted line net
- Compare cumulative raw and rounded net
- Add correction to current net and subtract it from current discount share
- Recalculate net unit rate and company values
- Recompute affected taxes

## Exclude fixed charges from trade discount base

`discountable_total = pre_discount_grand_total − signed_fixed_charges − signed_dependent_fixed_tax`

- Find actual and per-unit taxes
- Follow dependent row references for fixed portions
- Exclude valuation-only charges from payable fixed total
- Subtract from grand total

## Apply cash or nontrade discount after tax

`grand_total = original_grand_total − discount_amount; company_grand_total = original_company_grand_total − company_discount_amount`

- Retain item net and tax values
- Subtract discount from totals
- Reset and recompute settlement rounding

## Round a total to the smallest settlement fraction

`if remainder > fraction ÷ 2 then rounded_total = amount + fraction − remainder, otherwise rounded_total = amount − remainder`

- Use configured fraction if nonzero
- At exact half choose the lower multiple
- Without fraction apply configured integer rounding
- Round returned amount to total precision

## Retain the settlement rounding difference

`rounding_adjustment = round(rounded_total − grand_total, adjustment_precision)`

- Clear rounded total and adjustment when disabled
- Otherwise calculate rounded total
- Store exact signed difference at field precision
- Convert both rounded total and adjustment to company values

## Detect and correct company-currency imbalance

`difference = round(sum(round(each_debit, precision) − round(each_credit, precision)), precision)`

- Round each row
- Sum signed differences
- Round aggregate
- Apply voucher-specific allowance
- Within allowance and at least one decimal unit, post the opposite amount to rounding account

- Journal and payment allowance equals 5 ÷ 10^precision.
- Other vouchers use allowance 0.50.
- Specialized exchange gain or loss journal has an explicit rejection exception.

## Allocate a ledger amount to child cost centers

`child_amount = round(original_amount × allocation_percentage ÷ 100, precision)`

- Select latest allocation effective on posting date
- Validate main-center budget
- Apply formula to each debit and credit context
- Assign rounding-account rows to first child without splitting

## Calculate source and destination company amounts

`company_paid = round(paid_amount × source_conversion_rate, paid_precision); company_received = round(received_amount × target_conversion_rate, received_precision)`

- Calculate both independently
- Do not substitute one rate for both account currencies

## Calculate realized exchange difference on a reference

`exchange_difference = round(allocated_amount × payment_party_rate, company_precision) − round(allocated_amount × reference_rate, company_precision)`

- Calculate payment-side allocation
- Calculate historical-reference allocation
- Store difference on reference
- Create linked exchange journal during posting where required

- Order advances use the payment-side rate without a reference exchange difference.

## Separate explicit fees from automatic exchange difference

`automatic_difference = round(company_paid − company_received − ordinary_deductions, deduction_precision)`

- For internal transfer subtract existing nonexchange deductions
- Retain only one automatic difference row
- Remove it if zero
- Select bank charges for same-currency discrepancy where configured, otherwise exchange account

## Require a balanced payment after allocations and deductions

`receipt: company_party_amount − company_received + included_taxes − deductions; payment: company_paid − company_party_amount − included_taxes − deductions; transfer: company_paid − company_received − included_taxes − deductions`

- Determine payment direction
- Calculate direction-specific difference
- Round to difference precision
- Require zero on submission

## Calculate each scheduled invoice portion

`scheduled_amount = round(remaining_invoice_amount × portion_percentage ÷ 100, schedule_precision)`

- Subtract advances in party currency context
- Calculate transaction and company schedule independently
- Retain dates and term identity
- Validate total schedule within observed 0.10 tolerance

## Allocate available money by selected ordering

`allocation = min(available_payment, invoice_outstanding)`

- Iterate payments in supplied order
- Iterate invoices in supplied order
- Subtract allocation from both amounts
- Advance when either amount is exhausted
- Omit zero rows

## Calculate statement remainder after matching

`remaining = round(abs(withdrawal − deposit) − sum(allocations), remaining_precision)`

- Sum linked match allocations
- Subtract from absolute movement
- Positive means unreconciled on submitted statement
- Zero or negative yields reconciled status after allocation validations

## Normalize an excluded bank fee exactly once

`deposit mode: deposit = deposit − excluded_fee; withdrawal mode: withdrawal = withdrawal + excluded_fee; included_fee = included_fee + excluded_fee; excluded_fee = 0`

- Reject simultaneous deposit and withdrawal when applying fee
- Reject fee greater than positive deposit
- Use withdrawal mode when deposit is zero, including a fee-only transaction
- Reset excluded fee to prevent repeated normalization

## Revalue a nonzero foreign financial balance

`new_company_balance = account_balance × new_rate; adjustment = round(new_company_balance, precision) − round(company_balance, precision)`

- Group effective balance by account and party
- Apply configured small-balance allowance
- For nonzero pairs preserve foreign balance
- Post company adjustment against unrealized exchange account

## Unbilled sales-order contribution to credit exposure

`order_exposure = company_order_grand_total × (100 − billed_percentage) ÷ 100`

- Include only submitted orders with billed percentage below one hundred
- Exclude closed orders
- Omit entire order component when bypass policy requests it

## Combine customer exposure components

`exposure = ledger_exposure + order_exposure + standalone_delivery_exposure + max(additional_exposure, 0)`

- Resolve customer, group then company positive limit
- Calculate exposure components without double-counting linked delivery
- Reject strictly greater than positive limit unless permitted bypass

## Overdue portion with partial schedules

`paid = invoice_company_total − outstanding; overdue = min(max(past_due_scheduled_amount − paid, 0), outstanding)`

- Read non-delinked settlement ledger
- Use due-date comparison strictly before today
- If no past-due term total exists, use whole outstanding only when invoice due date is before today

## Simple annual interest on overdue principal

`interest = principal × annual_percentage ÷ 100 ÷ 365 × overdue_days`

- Require referenced invoices in notice currency
- Calculate date difference
- Calculate each line interest
- Add interest and fee to outstanding total

## Recognize a nonfinal service interval by inclusive days

`recognition = round(line_net × booking_days ÷ service_days, amount_precision)`

- Determine interval from prior recognition or service start
- Cap at month end, service end, stop date and cutoff
- Use company and account currency calculations separately
- Use residual instead for final interval

## Absorb remaining deferred amount in the final interval

`final_recognition = round(line_net − already_recognized, amount_precision)`

- Find prior recognized amounts
- Calculate company and account residuals separately
- Apply also when reviewed date routine marks a stopped-service interval final

## Compute effective months for monthly recognition

`effective_months = round(calendar_months × service_date_difference ÷ complete_month_date_difference, 1)`

- Count touched months
- Calculate noninclusive date ratio
- Round effective month count to one decimal
- Divide line net by effective months for ordinary month charge

- One-day and zero-denominator edge cases require an explicit execution fixture.

## Prorate a monthly recognition interval

`partial_amount = ordinary_month_amount × round(booking_date_difference ÷ full_month_date_difference, 1)`

- Use only for a nonfinal partial month
- Compute date ratio without inclusive extra day
- Round ratio to one decimal before multiplication
- Final interval instead uses residual

## Remaining straight-line depreciation per fixed period

`depreciation = (current_carrying_value − residual_value) ÷ (remaining_months ÷ frequency_months)`

- Determine unposted remaining periods
- Calculate candidate charge
- Apply partial-period and residual correction
- Round at asset monetary precision

## Daily straight-line depreciation under selected denominator

`total-days mode: depreciable_value ÷ remaining_days × interval_days; yearly mode: depreciable_value ÷ remaining_years ÷ current_financial_year_days × interval_days`

- Choose configured denominator policy
- Calculate unrounded daily amount
- Multiply by interval days
- Round scheduled charge
- Correct final residual

## Allocate remaining depreciation by shift factors

`charge = depreciable_value × row_factor ÷ unposted_factor_sum`

- Preserve posted rows
- Use ordinary fixed-period calculation for an initial schedule without shift assignments
- Resolve each shift factor
- Weight future rows only

## Determine annual double-declining percentage

`annual_percentage = round(200 ÷ (total_cycles × frequency_months ÷ 12), rate_precision)`

- Convert cycle life to years
- Divide two hundred by life years
- Round rate before schedule calculation

## Calculate written-down-value annual percentage

`annual_percentage = round(100 × (1 − (residual_value ÷ current_carrying_value)^(1 ÷ remaining_years)), rate_precision)`

- Preserve explicit rate during validation where allowed
- Determine carrying amount and unbooked useful life
- Calculate root ratio
- Round percentage

## Declining annual amount allocated across periods

`period_charge = financial_year_opening_value × annual_percentage ÷ 100 × frequency_months ÷ 12`

- Recompute at financial-year change
- Reuse the resulting period charge within the same financial year
- Apply prorating and residual cap where relevant

## Stop depreciation at expected residual

`corrected_charge = round(candidate_charge + candidate_remaining_value − residual_value, value_precision)`

- Apply on final planned row with a remaining difference or whenever residual would be breached
- Stop generating further rows
- Retain only positive charge

## Asset disposal gain or loss

`disposal_result = selling_amount − carrying_value`

- Recognize required depreciation through disposal
- Credit cost account for asset net purchase cost
- Debit accumulated depreciation
- Credit positive gain or debit negative loss
- Use sales claim or scrap journal as remaining counter-entry

## Value direct stock receipt by invoice

`candidate_stock_value = round(round(valuation_rate, valuation_precision) × commercial_quantity × conversion_factor, amount_precision)`

- Calculate candidate value
- In the ordinary stock-update branch compare only when the corresponding stock-ledger value is nonzero
- For the qualifying return branch use its separately selected actual stock-ledger value, including zero
- Use applicable actual stock-ledger movement and post difference to selected variance account

- The ordinary replacement branch requires stock update enabled and a nonzero corresponding stock-ledger value.
- The return-specific branch requires a stock-updating return and either an internal supplier or no original-return reference; that branch can replace the candidate with an actual zero value.

## Clear a receipt billed at a new exchange rate

`clearing_adjustment = commercial_quantity × net_unit_rate × (receipt_rate − invoice_rate)`

- Require linked stock receipt, perpetual accounting and unchanged unit net rate
- Apply when invoice-price incoming-rate adjustment is disabled
- Post signed debit to clearing and opposite credit to exchange account

## Combine commitments and expense for budget control

`exposure = outstanding_requests + unbilled_orders + actual_expense + current_changes; excess = exposure − selected_budget`

- Resolve dimension and account budget key
- Calculate request and order commitments
- Add current proposed ledger amount without double-counting submitted orders
- Apply annual and accumulated-period thresholds independently
- Positive excess triggers configured action

## Decide whether withholding threshold is reached

`ordinary remaining_threshold = cumulative_threshold − historical_under_withheld; when transaction threshold enabled, remaining_threshold = min(remaining_threshold, single_threshold); crossed = current_taxable >= remaining_threshold`

- Explicit override succeeds
- Transaction-only mode compares directly to single threshold
- Zero cumulative threshold succeeds
- Excess-only mode proceeds to exemption calculation
- Existing positive settled history keeps threshold crossed
- Otherwise use remaining-threshold expression

## Exclude the unused cumulative threshold from excess-only withholding

`exempt_amount = min(unused_threshold, current_taxable); remaining_taxable = current_taxable − exempt_amount`

- Evaluate category excess-only policy
- Record exemption separately
- Process remaining taxable amount through historical adjustments and applicable rates

## Allocate certificate and ordinary withholding

`certificate_base = min(taxable_amount, certificate_remaining_taxable_allowance); ordinary_base = taxable_amount − certificate_base; withheld = round(certificate_base × certificate_rate ÷ 100, precision) + round(ordinary_base × ordinary_rate ÷ 100, precision)`

- Complete threshold and prior withholding matching first
- Apply certificate rate to constrained taxable value
- Apply ordinary rate to remaining taxable value
- Retain separate allocations before account aggregation

- Applicable certificate, dates and scope must be valid
- This simplified positive-value formula does not silently replace signed return handling

## Match a current taxable event with prior withholding

`matched_tax = round(min(round(remaining_taxable_amount × prior_tax_rate ÷ 100, precision), prior_withholding_available), precision); matched_taxable = round(100 × matched_tax ÷ prior_tax_rate, precision)`

- Select eligible prior event and rate
- Compute and cap tax
- Recover matched taxable base
- Retain both taxable and withholding identities
- Decrease queues and continue

- For zero rate, match the smaller taxable amount instead of dividing by rate
- Matched historical tax does not create a second current deduction

## Reverse the billed portion of an earlier service accrual

`reversed_accrual = min(invoice_quantity, receipt_quantity) × receipt_transaction_rate × receipt_conversion_rate`

- Require effective provisional posting for exact receipt line
- Use the smaller qualifying quantity
- Value at receipt rate and receipt conversion
- Reverse provisional expense and liability
- Recognize approved invoice expense and payable separately

- Enabled nonstock provisional-accounting policy required
- Preserve normal field rounding when producing final ledger amounts

## Change asset carrying value

`difference = new_carrying_value − previous_carrying_value`

- Validate date not before acquisition
- Calculate signed difference
- Positive: debit fixed asset and credit difference account
- Negative: debit difference account and credit fixed asset
- After posting update carrying value and future schedule

- Zero difference has no constructed posting branch and needs an explicit replacement validation policy
- Caller-supplied nonzero previous value is not forcibly refreshed by this calculation

## Calculate capitalized repair cost

`capitalized_value = sum(invoice_allocations) + sum(consumed_quantities × consumed_valuation_rates)`

- Validate invoice and account allocation availability
- Submit material issue for consumed quantity
- Use issue value in capitalization posting
- Debit fixed asset and credit corresponding expense
- Regenerate future depreciation

- Capitalization is a configured choice
- Stock issue owns inventory credit and capitalization must not issue stock again

## Reconcile one invoice claim in account currency

`remaining_claim = original_claim + sum(debit_adjustments) − sum(credit_adjustments) − sum(settlements)`

- Select one company, account, party and invoice identity
- Exclude delinked or reversed allocations under active policy
- Sum signed adjustments and applications
- Compare authoritative claim outstanding

- General-ledger company balance requires separate exchange adjustments
- A standalone credit remains its own claim until allocated

## Close profit and loss account balances

`net_profit = income_credit_balance − expense_debit_balance`

- Debit income for its credit balance
- Credit expense for its debit balance
- Credit closing equity or liability for positive profit
- For loss debit closing account by absolute loss
- Preserve financial-book and dimensional grouping

- Applicable interval, prior-close and stock-close gates must pass
- Completion follows successful posting, not job creation
