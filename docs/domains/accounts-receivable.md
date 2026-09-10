# Accounts receivable

## Local record and calculation contracts

[Customer](../../schemas/data/record-types/customer.json); [Customer credit limit](../../schemas/data/record-types/customer_credit_limit.json); [Sales invoice](../../schemas/data/record-types/sales_invoice.json); [Sales invoice line](../../schemas/data/record-types/sales_invoice_item.json); [Payment](../../schemas/data/record-types/payment_entry.json); [Payment allocation](../../schemas/data/record-types/payment_entry_reference.json); [Payment schedule](../../schemas/data/record-types/payment_schedule.json); [Collection notice](../../schemas/data/record-types/dunning.json). These local definitions provide the persistent fields, relationships, defaults and permissions. The rules below explain their business meaning and lifecycle consequences.

[Financial calculations](../../schemas/mathematics/financial-calculations.json) define evaluation order and numerical boundaries. [Accounting acceptance cases](../../schemas/mathematics/accounting-acceptance-cases.json) provide complete journal events, expected closing balances, settlement outcomes and rejection conditions. These are independently checked arithmetic expectations; they do not claim execution of an entire application.

## Business boundary

Accounts receivable turns accepted sales into customer claims, adjusts those claims through credits and payments, and enforces exposure and overdue limits. It shares products, prices, currencies, parties, projects, fulfillment records, taxes, and accounting dimensions with the rest of the application. Quotation and order quantities express commercial intent; delivery records express stock fulfillment; the sales invoice creates the financial claim. A sales invoice can also perform stock delivery when its stock-update option is enabled. Never infer a delivery solely because a sales invoice exists.

The required records are customer and customer group; company-specific customer credit policy; sales invoice with ordered item and tax lines; sales invoice advance allocation; payment schedule; payment and its invoice references; credit invoice linked to an original claim or maintained as its own claim; collection notice and overdue-payment lines; general ledger entries; and party settlement entries. Item lines retain source quotation, order and delivery associations when those associations apply. An invoice identity survives payment, later reconciliation, return, and cancellation.

## Invoice calculation and posting

Calculate commercial line amounts, taxes, discounts, document totals and cash rounding through the shared calculation contract in [Taxation and pricing](taxation-and-pricing.md). Persist the resulting transaction and company amounts; the posting stage must use the approved values. The customer receivable is debited for the payable document total. The reviewed selection uses rounded total when both a nonzero rounding adjustment and a nonzero rounded total exist; otherwise it uses grand total. The company selection is evaluated against the company rounding fields separately. A return linked to an original invoice settles against that original invoice unless the return is configured to maintain its own outstanding amount.

Ordinary nonasset lines credit their income accounts. A deferred-revenue line on an ordinary invoice credits its deferred-revenue account instead. Tax lines credit the selected tax accounts using the tax calculation service's amount choice. An internal transfer within the same company skips ordinary customer receivable and income creation and follows the internal-transfer treatment. Fixed-asset disposal lines use asset disposal logic rather than merchandise revenue logic. This is why one generic debit-customer and credit-sales template is insufficient.

| Event | Debit | Credit | Claim effect |
|---|---|---|---|
| Ordinary untaxed sale 1000.00 | Customer receivable 1000.00 | Income 1000.00 | Customer owes 1000.00 |
| Sale 1000.00 plus tax 150.00 | Customer receivable 1150.00 | Income 1000.00 and tax 150.00 | Customer owes 1150.00 |
| Receipt applied to that claim 600.00 | Bank or cash 600.00 | Customer receivable 600.00 | Remaining claim 550.00 |
| Credit for net 200.00 and tax 30.00 | Income 200.00 and tax 30.00 | Customer receivable 230.00 | Remaining claim reduced by 230.00 |
| Deferred service sale 1200.00 | Customer receivable 1200.00 | Deferred income 1200.00 | Full claim exists before income recognition |

These table amounts are derived examples under one currency, no additional discounts, no stock update, no rounding difference and no asset disposal. They describe the composition rules; they are not evidence that every configuration was executed.

If invoice posting updates stock under perpetual accounting, the inventory posting service contributes the inventory reduction and cost-of-goods-sold effects. When delivered-but-unbilled accounting is enabled and the invoice bills a prior delivery, the matching delivery accrual is cleared instead of recognizing the same cost twice. Preserve exact delivery-line references for partial billing and returns. The inventory chapter owns valuation mathematics; receivables owns the link that prevents duplicate expense.

Separate discount accounting records discount expense while restoring the appropriate gross income contribution. For an item discount, the amount is per-unit discount multiplied by commercial quantity, converted at the invoice rate. Additional document discount uses the configured additional-discount account. Deferred revenue and returns alter the account selected for the paired income contribution. Receipt at point of sale, loyalty redemption, change, write-off, and cash rounding are additional composition stages; their existence must not be mistaken for a universal write-off permission on any invoice. The inspected invoice write-off builder is specifically gated by the point-of-sale flag.

## Schedules and collection dates

Payment terms produce dated portions of the amount remaining after recognized write-off and allocated advances. The currency of an advance is the party account currency, which determines whether it is subtracted from the company total or transaction total before recalculating the other measurement. A scheduled percentage is applied to each total independently and rounded to the corresponding schedule amount precision. The invoice due date is the latest schedule date, not the earliest. Duplicate due dates are rejected by the shared schedule validation. A schedule discount date cannot follow its due date. Returns and immediately paid invoice variants can clear their schedules.

Due dates support days after invoice date, days after invoice-month end, and months after invoice-month end. The supplier-bill date takes precedence when present in the shared calculation. A computed payment-term due date earlier than posting date is brought forward to posting date. The observed schedule total validation tolerates an absolute difference up to 0.10 in either transaction or company total; an amount above that tolerance is rejected. Do not silently replace this tolerance with the ledger balancing tolerance.

Reviewed test expectation: an invoice with net 200.00 and tax 18 percent produces scheduled payment amounts of 200.00 and 36.00 when its terms explicitly separate basic amount and tax. Full payment updates the corresponding schedule rows to those paid amounts. This fixture shows that schedule identity matters, beyond the invoice-wide outstanding number.

## Settlement, advances, credits, and outstanding values

A payment allocation names the reference document, optional payment term, allocated amount, reference exchange rate and resulting exchange difference. The payment service refreshes outstanding references and checks current amounts before accepting allocation. A fully paid reference is rejected; a stale partially paid reference can require refreshing the outstanding selection; term-based allocation requires the term. Positive allocations cannot exceed current positive outstanding, and negative allocations cannot pass the negative outstanding boundary.

Unallocated receipts are retained as customer credit or a separate customer-advance liability, depending on policy. Reconciling an advance later transfers its settlement relationship without duplicating the receipt. A credit invoice can reduce the original invoice's outstanding or remain a separate negative claim for subsequent allocation. A payment direction inconsistent with the sign of the claim is validated separately from the arithmetic. Acceptance must cover ordinary receipt, refund, partial return, and credit applied to another invoice.

The separate-advance-account option intentionally avoids directly linking the original advance-account posting to the invoice in the first payment composition. Later advance movements use dedicated references and can be reversed independently. Records must retain both the origin of funds and the later settled invoice.

Reviewed test expectation: a receipt against a foreign invoice created at company conversion 50 and settled using 55 records an exchange difference of 500.00 for a 100-unit foreign claim. The receipt's main journal debits bank 5500.00 and credits customer receivable 5500.00; a linked exchange journal is created, and invoice outstanding becomes zero. Recording just the bank movement and leaving a 500.00 residual would be incorrect.

## Credit exposure is not overdue balance

Credit limit is resolved from the customer-company setting, then customer-group setting where not bypassed, then company default. A false or zero value falls through rather than unconditionally imposing a zero-credit policy. Where the effective limit is positive, reject only when exposure is strictly greater than the limit; equality is accepted. A configured credit-controller role can bypass the rejection. A proposed implementation that treats zero as no credit would change observed behaviour.

Exposure is the sum of effective customer general-ledger debit less credit, the unbilled share of submitted nonclosed sales orders when that component is enabled, and eligible standalone delivery exposure. Order exposure is company grand total multiplied by one minus billed percentage divided by 100. Standalone delivery exposure includes only positive unbilled line remainders without sales-order or direct-sales-invoice links and with a positive company net total. The reviewed expression is line amount less billed line amount, divided by company delivery net total, multiplied by company delivery grand total. Its mixed measurement contexts require a foreign-delivery fixture; this document does not normalize the expression into a different presumed formula.

Derived single-currency exposure fixture: customer ledger net 3000.00, unbilled sales-order share 2000.00, eligible delivery share 500.00, and a proposed additional exposure of 100.00 produce 5600.00. A limit of 5500.00 rejects for a user without bypass authority; a limit of 5600.00 accepts. Delivery linked to the already-counted sales order must not add another 500.00.

Overdue billing uses a different policy and a different basis. It must be enabled globally; its threshold resolves from customer then customer group. The amount comes from non-delinked settlement-ledger amounts grouped by sales invoice and expressed in company currency. For payment schedules, compute the sum of installments whose due dates are strictly before today. Paid amount for this calculation is company grand total less invoice outstanding. Overdue portion equals the minimum of outstanding and the maximum of past-due scheduled amount less paid amount and zero. Without a past-due scheduled amount, use the whole outstanding only when the invoice due date itself is before today. A separate bypass role applies.

Reviewed test expectations: a 1200.00 invoice with one 600.00 installment past due and another 600.00 installment in the future contributes 600.00 overdue, although its invoice due date is in the future. Paying 600.00 clears the overdue amount. An 800.00 receipt allocated after an overdue invoice was submitted clears that invoice's overdue contribution through settlement-ledger changes. A foreign 100.00 overdue invoice at conversion 50 contributes 5000.00 company-currency overdue. An invoice due today contributes zero until the following date.

## Collection notices and interfaces

A collection notice stores original overdue principal, due dates, annual interest percentage, collection fee, document currency and conversion. All referenced invoices must have the same currency as the notice. Interest for a line is outstanding principal multiplied by annual percentage divided by 100 and 365, multiplied by days between notice date and due date. Total notice charge is the sum of interest plus fee; grand total adds outstanding principal. This is simple interest with a 365-day divisor, not compounding. Derived example: principal 3650.00, annual rate 10 percent and 30 overdue days yield 30.00 interest; a 20.00 fee yields charges 50.00 and demand 3700.00.

The receivable service boundary exposes invoice preparation, validation, submission, credit creation, cancellation, outstanding inquiry, payment-term inquiry, credit exposure inquiry, overdue inquiry and reconciliation. Read operations must respect company, party and dimensional access. Mutations return the authoritative document identity, lifecycle state, financial totals, outstanding amount and references to generated accounting effects. A rejected mutation returns the business condition and leaves no partial claim change.

## Acceptance requirements and remaining evidence

Acceptance must compare document totals, customer balances, income and tax postings, stock expense when enabled, outstanding by invoice and term, and history after reversal. Include exact-limit and just-over-limit tests; due-today and overdue tests; a customer with a zero local limit and nonzero inherited limit; a customer-controller bypass; stale and concurrent allocation; a linked and standalone credit; partial order billing; standalone delivery billing; and deferred service billing.

Reviewed source and selected tests establish the contracts above. Exhaustive combinations of loyalty, point-of-sale consolidation, asset sales, regional tax extensions, foreign standalone delivery exposure and advanced returns remain separate operational verification obligations. They must not be represented as executed acceptance coverage merely because corresponding symbols or fields exist.

## Claim control and collection reconciliation

A claim balance is a signed quantity in a specified currency. An ordinary customer invoice contributes a positive claim; an applied receipt or credit contributes a reduction. A standalone credit keeps its own negative outstanding until refunded or reconciled. Present positive invoice debt and unapplied customer credits separately before presenting a net customer balance. Net customer exposure can be zero even though one invoice and one unallocated receipt still require reconciliation.

For a fixed invoice and account-currency measurement, the conservation identity is original claim plus debit adjustments less applied credit adjustments less applied settlements equals remaining claim. The settlement history must retain the allocation that changes each term. In company currency, historical-rate and realized-exchange entries explain why the control-account movement need not equal a foreign allocation multiplied by the invoice's original rate at every intermediate stage. The [treasury contract](treasury-and-reconciliation.md#reference-validation-and-foreign-settlement) owns that conversion sequence.

Derived foreign settlement: invoice 100.00 foreign units at company rate 50 posts receivable debit 5000.00 and income credit 5000.00. Receipt at rate 55 posts bank debit 5500.00 and receivable credit 5500.00. The linked realized-exchange event debits receivable 500.00 and credits exchange gain 500.00 in company currency, with zero foreign receivable movement. The receivable company balance and foreign outstanding both become zero; income remains 5000.00 and realized gain is separately visible at 500.00. Cancellation must reverse both the receipt and the linked exchange consequence selected by the cancellation service; reversing only cash leaves a false receivable residual.

## Partial credits and receipt reversal example

A customer buys goods with net amount 1000.00 and tax 150.00. A receipt of 600.00 leaves 550.00 outstanding. A permitted credit of net 200.00 and tax 30.00 reduces that outstanding to 320.00. The receipt has not changed merely because a later credit was added. If the receipt is subsequently cancelled under an eligible cancellation path, restore 600.00 to outstanding: the invoice now has 920.00 still due, net sales 800.00, tax liability 120.00 and no retained bank increase from that receipt. The invoice and credit remain separate history. If the credit itself updates inventory, its stock valuation reversal is additionally required and cannot be inferred from the 230.00 customer credit alone.

For a receipt greater than the remaining claim, allocate at most the current claim amount and keep the excess as unapplied credit or the separate customer advance liability. For a credit larger than the outstanding claim, preserve the resulting refundable credit according to the selected standalone-versus-linked credit policy; do not manufacture a negative cash receipt to force a zero balance.

## Ageing and exposure output contract

Each enquiry must declare company, party, as-of date, selected currency, financial-book treatment, permitted dimensions and whether future-dated postings are excluded. Return both document and term identities, original amount, credit adjustments, allocations, outstanding, due date and age. An ageing bucket is a presentation over this dated result, not a new ledger. The threshold enquiry uses the exact overdue selection already specified above, while the credit-limit enquiry additionally includes eligible order and delivery exposure.

The current-date overdue check must not be presented as a historical as-of ageing engine. A replacement can expose both operations, but a date input on a report cannot silently change the business-date checks used when authorizing a new sale. Cancellation, late allocation and backdated posting must be reflected according to each operation's documented effective-date policy.

The cases `customer_partial_payment_credit_and_reversal`, `foreign_customer_receipt_and_realized_gain`, and `customer_advance_later_applied` specify complete debit-and-credit sequences. They complement the separate exposure and overdue formulas; none substitutes an invoice status label for measured debt.
