# Regional and specialised capabilities

Read this chapter with [taxation and pricing](taxation-and-pricing.md), [financial accounting](financial-accounting.md), [company governance](company-and-master-governance.md), [supplier payables](accounts-payable.md) and [external integrations](../interfaces/external-integrations.md). The structured [customer and service calculations](../../schemas/mathematics/customer-and-service-calculations.json) and [acceptance cases](../../schemas/mathematics/customer-and-service-acceptance-cases.json) define exact examples for the calculations below.

## Scope and evidence boundary

Regional behaviour is selected by the company's country and configured tax accounts, identifiers, payment classifications, and document fields. It enriches the same customer, supplier, company, invoice, and tax records used elsewhere. It does not justify a separate accounting engine or unrestricted replacement of company-currency totals. The rules below describe the supplied snapshot's software behaviour; they do not assert that the forms or tax policies satisfy present-day law in every jurisdiction.

The active module manifest includes accounting, buying, selling, inventory, manufacturing, projects, support, maintenance, assets, quality, communications, telephony, regional functions, subcontracting, bulk transactions, and electronic business document interchange. It does not declare agricultural management or nonprofit operations as active modules. A residual template directory is not evidence of a functioning specialised domain. Do not invent agricultural production, grant accounting, or membership functionality and call it observed equivalence. Such additions need separately approved requirements and behavioral justification.

## Reduced withholding certificates

A reduced withholding certificate belongs to a company, supplier, withholding category, fiscal year, and date range. It carries certificate identifier, supplier tax identifier, reduced rate, and certificate limit. End date cannot precede beginning. Both validity endpoints must lie inside the selected fiscal year. Date overlap is inclusive: sharing an endpoint counts as overlap. Reject an overlapping certificate found for the same company, supplier, and withholding category.

The defined validation fetches one matching existing certificate and compares intervals. It does not prove that every possible overlapping certificate is checked if multiple nonoverlapping records already exist. A comprehensive acceptance fixture must include three existing intervals, not only one duplicate. Application of the rate, exhaustion of the certificate limit, and interactions with withholding thresholds belong to the accounting calculation specification and require separate evidence.

## Electronic invoice tax summaries

The defined electronic invoice exporter aggregates tax amount and taxable amount by tax rate. Fixed actual charges are excluded from that aggregation. A tax calculated on a prior tax row's amount or total can be represented as an extra charge item. That item's quantity is one, its rate and taxable amount are the referenced charge amount, and its tax amount equals referenced charge amount multiplied by the current tax percentage divided by 100. Zero-rate summaries carry exemption reason and exemption law. A fallback zero-rate summary is produced when no itemised zero-rate details populated the summary.

The invoice preflight requires company and customer addresses, company fiscal regime, both company tax and fiscal identifiers, and at least one tax row. Individual customers require fiscal code. Public administrations require fiscal code; other organisational customers require tax identifier. A zero tax row with zero amount requires exemption reason. Payment method codes are filled from the associated payment-method record when absent. These conditions must be evaluated before generating a document that cannot be accepted by its external consumer.

The external structured-invoice document layout, controlled document-type values, transmission identity, file naming, signature rules, acceptance receipts, and every validation of each national format are not fully expressed in this chapter. They remain exact-contract work items; do not treat the tax summary and preflight described here as a complete electronic-invoicing specification.

## Supplier electronic invoice intake

A supplier-invoice intake record supplies the company, buying price list, invoice identity policy, default product, supplier group, tax account, and attached archive. Import processes member documents, extracts supplier invoice number and date, supplier and address details, item lines, tax rows, and payment terms, then creates purchase invoices. The supplier invoice number is required. Defaults and row derivation are part of the intake contract, not a licence to post an imported total without recalculating the purchase document.

Each purchase-invoice creation has a local rollback point. A failure inside that creation step is logged and later invoice definitions continue. Supplier, contact and address creation, invoice-header parsing and item/tax preparation occur before the local rollback point. Failures in those earlier steps are not covered by the same catch-and-continue behavior and can stop the batch. Overall completion can therefore be partial, and a failed invoice can leave a newly created supplier or address. The imported document is attached to a successfully created invoice, and counters distinguish processed invoice headers from created invoices. One member containing multiple invoice headers can increment the processed count more than once.

When unit rate and line amount are both negative, line preparation reverses quantity and sets a return-detected marker. Invoice creation reads a different return-state input; consequently the detected marker does not itself guarantee a return invoice. Quantity, unit and tax rate carry between item iterations as specified below. Imported attachments are created as nonprivate; private retention is an additional hardening requirement, not the importer's existing guarantee.

## Country-selected reporting

| Capability | Observed selection and calculation |
| --- | --- |
| South African value added tax audit | Reject another company region; require configured tax accounts; include submitted nonopening customer and supplier invoices in the selected date range; aggregate itemised taxable and tax amounts by invoice and rate |
| United Arab Emirates value added tax return | Reject another company region; split standard-rated sales by emirate; show tourist refunds with negative sign; separately report reverse-charge, zero-rated, exempt, and recoverable amounts |
| United States supplier payment statement | Return no columns and no rows outside the selected country; group qualifying suppliers' general-ledger debit amounts in account currency by supplier and fiscal year, optionally supplier group |

For the South African audit, zero-rate tax details without the item's explicit zero-rated marker are excluded. Gross amount for an included tax-rate bucket equals taxable amount plus tax amount. The configured account set decides which itemised taxes participate. For the United States report, the defined query sums supplier-side debit entries; it is not independently demonstrated to be equivalent to every statutory notion of a cash payment or to exclude every cancellation mechanism. Those distinctions require fixtures with journal adjustments, returns, and cancellations.

## Contract fulfilment

A business contract can reference a customer, supplier, or employee, with optional linkage to a quotation, project, order, or invoice. Keep signed flag, signatory, signing time, company signing user, dates, contractual terms, and fulfilment checklist. Contract status is unsigned until signed. With an end date it is active only within the inclusive date range; without an end date the defined helper reports active without separately testing whether the beginning date is in the future.

When fulfilment is required, zero completed checklist rows means unfulfilled, some means partially fulfilled, and all means fulfilled. An unmet fulfilment with a passed deadline becomes lapsed. With no fulfilment requirement, use “not applicable” in the neutral model. The signed contract's activation and checklist fulfilment do not themselves generate a receivable or payable; any related document has its own submission and posting rules.

## Acceptance and extension requirements

Test regional activation by company, required identifiers before invoice export, zero-rated versus exempt items, separate tax buckets, charge-on-charge calculations, refund signs, import partial success, overlap at certificate endpoints, contracts with future beginnings and no ends, and expired incomplete fulfilment. Country-specific external format validation and current regulatory certification are outside what these reviewed routines establish. Implementation work must not mark this chapter as full jurisdictional parity until those exact-format and calculation fixtures are completed.

## Regional record contracts

| Record | Durable fields | Governing rule |
| --- | --- | --- |
| Reduced withholding certificate | Company, supplier, fiscal year, withholding category, identifier, supplier tax identifier, beginning/end, reduced rate and limit | Date validation and overlapping-interval search described above |
| Country tax-account configuration | Company and selected tax-ledger account rows | Determines report inclusion; tax-account membership must not be inferred from an account name |
| Electronic invoice projection | Invoice identity, company/customer tax data, addresses, transmission sequence, document category, product rows, tax-rate summaries and payment installments | Derived from accepted invoice and regional configuration |
| Supplier import batch | Company, attached archive, default product/unit context, buying price list, supplier group, tax account, naming policy, progress and outcome counts | Protected background import with per-invoice failure boundaries |
| Contract | Party kind and identity, terms, signed state, signatory and time, company signer, effective dates, linked transaction and optional fulfilment checklist/deadline | Contract activation is separate from checklist fulfilment and financial posting |

The full field inventories are [reduced withholding certificate](../../schemas/data/record-types/lower_deduction_certificate.json), [supplier invoice import](../../schemas/data/record-types/import_supplier_invoice.json) and [contract](../../schemas/data/record-types/contract.json).

## Structured customer-invoice export contract

An export selection includes submitted customer invoices with nonempty company tax identifiers. Optional company, customer, beginning posting date and ending posting date narrow the selection; both dates form an inclusive range. Read permission is required. Opening invoices are excluded from the regional validation/submission generation path, although the bulk selection's base filter itself does not include an opening exclusion.

Preparation derives an unamended invoice number by removing the final amendment suffix when the invoice has an amendment origin. A return linked to a prior invoice defaults to the external credit-note document category; otherwise the default is ordinary invoice. A public-administration customer selects the public-administration transmission profile; other customers select the private-sector profile.

| External contract concept | Fixed value in the supplied compatibility profile |
| --- | --- |
| Ordinary invoice category | `TD01` |
| Credit-note category | `TD04` |
| Public-administration transmission profile | `FPA12` |
| Private-sector transmission profile | `FPR12` |
| Regional schema namespace version | `1.2` |

These literals are external controlled values rather than abbreviations for this repository's business concepts. Their surrounding field meaning is defined in full. A newer national format must be a separate versioned contract; it must not silently change a historical invoice's selected profile.

The generated document contains the following ordered semantic groups:

1. Transmission: sender country and fiscal identity, monotonically allocated sequence, transmission profile, recipient routing identity and optional sender telephone/electronic mail.
2. Supplier identity: country and tax identity, optional fiscal identity, company name, fiscal regime, address and optional business-register information, share capital, member classification and liquidation state.
3. Customer identity: for a person, fiscal identity and first/last names; for an organisation, country/tax identity, optional fiscal identity and name; then customer address.
4. Invoice header: document category, currency, posting date, unamended number, optional stamp duty, document discount or surcharge, total and selling purpose.
5. Related business records: unique customer order references with dates, linked original invoice for a credit, delivery identities/dates with line references, and optional shipping address.
6. Goods/services: sequence, product identity, plain-text description, quantity, unit, unit price, discount/margin components, net row total, tax rate and optional exemption category.
7. Tax summaries: one rate bucket with taxable amount, tax amount, optional exemption category and exemption law; optional collectability is emitted only under the renderer's qualifying condition.
8. Payment: installment/full-payment classification and installment rows containing payment method, due date, amount and optional bank identity, international account number and bank-routing components.

Addresses require postal code, city and country code during preflight. Country codes are normalised to uppercase; recognised regional province names can map to province codes. Both company tax and fiscal identifiers are required. The issuer's fiscal regime and customer's appropriate individual, public-administration or organisational tax identity must be present. Each payment schedule row needs a payment method whose configured external code exists before regional submission.

### Export numerical and selection rules

The numeric formatter outputs absolute magnitudes. It uses exactly three decimal places when the requested field precision is three, four when it is four, and two for all other requested precisions. Therefore a return's negative quantity and amounts are rendered as positive magnitudes under its credit document category. This rendering does not alter signed internal ledger amounts.

For a line with tax rate $r$, the tax divisor is $1+r/100$ when any invoice tax row is included in the displayed price and the product tax rate is nonzero; otherwise the divisor is one. Unit-price selection prefers a nonzero price-list rate divided by this divisor, then a nonzero net rate, then rate divided by divisor. A zero value does not win either fallback. Percentage discount components are emitted only when positive. Positive margin components are emitted as a percentage, or as a fixed amount divided by the divisor.

Example: with a price-list rate of 115 and included tax rate 15 percent, the exported pre-tax unit price is 100. A positive amount margin 11.5 is rendered as a pre-tax margin ten. The row net amount remains the accepted invoice net amount; it is not recalculated by multiplying a formatted unit price and quantity in the exporter.

The document total selects nonzero rounded total, otherwise grand total. A positive overall discount is a discount component; a negative amount is a surcharge, with its exported magnitude positive. A fixed actual charge whose tax amount is exactly two is selected as stamp duty by this compatibility routine; the search is by amount and charge kind, not a separate dedicated stamp-duty flag.

Tax summaries are keyed by the textual tax-rate value. Zero-rate exemption reason and law come from the qualifying tax rows; several zero-rate categories at the same rate are not automatically separated into distinct summary keys. A charge on a prior tax row uses that prior row's tax amount as an additional charge item even for the prior-row-total calculation category. Preserve this exact rule in the export projection while the authoritative invoice's own tax engine remains governed by [taxation and pricing](taxation-and-pricing.md).

### File lifecycle and limits

Generated export files are private attachments to the invoice. Names combine the company's country-prefixed tax identifier, an underscore and an allocated five-digit sequence. Regeneration requests replacement: when a matching earlier attachment is found, remove it and reuse its name/sequence. Otherwise allocate a new sequence. Cancellation removes matching regional export attachments. Bulk download collects matching attachments and packages them as one compressed download.

The renderer includes fields for a national structured format, but generation alone does not sign or transmit the document, validate it against the receiver's entire schema, or process acceptance/rejection acknowledgements. The payment classification branch refers to a schedule collection distinct from the main invoice schedule lookup; multiple-installment output must be checked with a rendered fixture. The collectability condition similarly reads summary-level presence before emitting an invoice-level value. These conditions cannot be replaced by assumed ideal output.

Exact receiver element names, national controlled-value sets, signature envelopes and acknowledgement schemas belong to a versioned [external integration contract](../interfaces/external-integrations.md). They remain an external compatibility boundary where this repository has not supplied a complete validated receiver contract. This chapter fully states the exporter calculations above; it does not certify present-day regulatory acceptance.

## Supplier import row derivation and partial failure

Import invocation requires write permission on the batch, sets processing state and schedules a background job. A default stock unit must exist. Archive members are decoded using the supported Unicode text encodings and parsed into invoice headers, supplier identity, details, tax summaries and payments. Each header requires supplier invoice number and supplies bill date; posting date is the import's current date, and currency is the company's default currency. The created purchase invoice remains draft.

Supplier lookup first matches tax identity, then supplier name. If absent, create the supplier and its contact. Address reuse compares street and postal value on linked addresses. The extraction stores postal information under a different internal field name from the subsequent assignment helper, and the existing-supplier contact search similarly references a different name key. Therefore import cannot claim reliable postal preservation or duplicate-contact avoidance without acceptance for those key mismatches.

The product preparation starts once per invoice with quantity one, rate zero, tax rate zero and the configured default unit. Only detail rows containing both unit price and line total are converted. For each such row:

1. Read rate and line total, defaulting absent numeric values to zero.
2. Replace quantity only when rate is nonzero, line total divided by rate differs from one, and the row supplies a quantity. Within that same branch, replace unit when supplied; otherwise keep the previous quantity/unit.
3. When both rate and total are negative, multiply the current quantity by negative one and set the return-detected marker. The invoice-return marker mismatch described above remains significant.
4. Replace tax rate only when the row supplies one; otherwise retain the preceding tax rate.
5. Create a row using the batch's default product, a sanitised description, current quantity/unit, absolute unit rate, stock conversion factor one and current tax rate. Description punctuation is replaced by separators and the product display name is limited to 140 characters.
6. Add each percentage-discount component as its percentage of signed rate multiplied by current quantity to the batch's document discount total.

Example: the first line has rate ten, total thirty, quantity three and unit box. A second line has rate five and total five but no quantity/unit. It inherits quantity three and unit box, so its prepared amount is fifteen rather than five. This is a compatibility defect captured by the acceptance catalog. A replacement may adopt per-row defaults only as a declared correction, not while claiming the old import produced independent rows.

Tax summaries become actual-amount tax rows using the configured tax account. Supplier invoices recalculate their own totals after insertion. A positive accumulated discount is applied to grand total. Imported payment amounts are then adjusted to the recalculated invoice total: sum imported installments, subtract invoice grand total, and remove that entire difference from the first installment only. Later installments keep their amounts. Store the original imported sum separately.

For imported installments 60 and 60 and recalculated grand total 110, the difference is ten and the new installments are 50 and 60. If the difference exceeds the first installment, the first can become negative under this routine; rejection or redistribution requires another validated rule. Missing installment due dates default to the import date.

An error during purchase-invoice creation rolls back that invoice creation and logs failure, after supplier/address preparation has already occurred. An attachment-write failure occurs outside that same catch boundary. Full completion is reported only when created-invoice count equals processed-header count. Neither full nor partial completion proves that the draft invoices have been approved or posted. Retry deduplication by supplier invoice identity must be validated separately through the purchase-invoice uniqueness policy.

## Report arithmetic and presentation boundaries

For the South African audit, iterate supplier invoices and customer invoices independently. Select submitted, nonopening documents and item-tax detail rows belonging to configured tax accounts. Accumulate taxable amount and tax amount for each invoice/rate pair. A zero-rate detail is included only when its product row explicitly has the zero-rated marker. Gross equals taxable plus tax. Sections group by tax rate and contain subtotals; invoice rows are ordered by posting date descending in the initial selection.

Example: one invoice has taxable 1,000 and tax 150 at 15 percent, plus taxable 200 and tax zero with the explicit zero-rated marker. It contributes two buckets: gross 1,150 and gross 200. Another zero-tax row lacking that marker contributes nothing to the zero-rate bucket. Display headings convert rate to an integer, so a fractional rate must retain its true numeric grouping value even if the inherited heading truncates its label.

The United Arab Emirates standard-rated sales selection groups submitted invoice rows that are neither exempt nor zero rated by emirate, summing company-currency net amounts and row tax amounts. The fixed displayed order is Abu Dhabi, Dubai, Sharjah, Ajman, Umm Al Quwain, Ras Al Khaimah and Fujairah, with zero rows when a category has no amounts. Tourist refund totals and tax amounts are negated for display. Reverse-charge, zero-rated, exempt, recoverable and standard expense amounts are separate report components with their own invoice/ledger selection.

| Return component | Amount selection | Tax selection |
| --- | --- | --- |
| Tourist refunds | Negative sum of company-currency totals of submitted customer invoices with a positive tourist-refund amount | Negative sum of those tourist-refund amounts |
| Reverse-charge supplies | Sum company-currency totals of submitted supplier invoices marked reverse charge | Sum ledger debits on configured regional tax accounts joined to those invoices, with submitted ledger lifecycle |
| Zero-rated supplies | Sum company-currency net values of submitted customer invoice rows explicitly zero rated | Display a nonnumeric empty tax placeholder |
| Exempt supplies | Sum company-currency net values of submitted customer invoice rows explicitly exempt | Display a nonnumeric empty tax placeholder |
| Standard-rated recoverable expenses | Sum company-currency totals of submitted supplier invoices with positive recoverable standard expense amounts | Sum the stored recoverable standard expense amounts |
| Recoverable reverse-charge expenses | Sum company-currency totals of submitted reverse-charge supplier invoices with positive recoverability percentage | Sum configured tax-account ledger debits multiplied by that invoice's recoverability percentage divided by 100 |

The reverse-charge ledger joins use invoice identity without an explicit voucher-kind comparison in that join. They check submitted lifecycle but do not independently filter the ledger cancellation marker. These details require conflicting-name and cancelled-ledger fixtures rather than an assumption that every debit is a current qualifying tax. A tax debit of 150 and recoverability percentage 40 contributes recoverable tax 60 while the recoverable amount column contains the full qualifying invoice total.

One shared date-filter helper adds the upper boundary only when a beginning date is supplied. An ending-only request therefore does not reliably constrain every component, and a beginning-only request can pass an absent upper value. Paired beginning/end dates are the supported acceptance fixture for report consistency; repair of independent optional bounds is a separately declared correction.

The United States supplier payment statement selects general-ledger debit amounts in account currency for qualifying supplier parties in the chosen company and fiscal year, optionally restricted by supplier group. It does not perform currency conversion merely because several suppliers share a report. Returns, journal adjustments, ledger cancellation and account-currency mixtures require explicit fixtures before interpreting its displayed total as a statutory cash-payment total.

The printable supplier statement renders each qualifying supplier separately, using the fiscal-year beginning's calendar year, company and supplier tax identities, selected addresses, and a payment value formatted in United States dollars with zero decimal places. The payer-address lookup prioritises postal, then billing, then deterministic name order among records marked as company addresses; it does not constrain that address selection to the requested company. The recipient lookup matches the party identity through address links without additionally restricting the linked party kind. These are explicit cross-company and duplicate-name acceptance cases, not assurances of correctly scoped printed addresses.

## Contract transitions and acceptance

Validate end not before beginning. Fill an absent party display name from the selected party; keep the party kind so a customer and employee with identical display names remain different counterparties. Submission records the acting company user as company signatory. Unsigned remains unsigned regardless of date. A signed contract with both bounds is active from beginning through end inclusive; a signed contract without an end is active even when its beginning is in the future under the stated compatibility rule.

When fulfilment is required, count fulfilled checklist rows. Zero gives unfulfilled, a positive count below row count gives partially fulfilled, and all rows fulfilled gives fulfilled. A required but empty checklist yields unfulfilled because the zero branch takes precedence. A passed deadline changes any incomplete result to lapsed, but equality with the deadline does not lapse it. With no fulfilment requirement the result is not applicable.

The daily contract update selects signed submitted contracts and refreshes activation status. It does not call the fulfilment calculation in that daily path, so elapsed deadlines alone do not establish automatic lapse until a path recomputes fulfilment. Permitted submitted-record updates recalculate both states. Cancellation/discard records cancelled activation. Neither signing nor fulfilment posts accounting; explicit purchase, customer, payroll or project documents carry financial consequences.

Acceptance cases cover inclusive validity and overlap endpoints, zero versus absent values, full and partial imports, inherited row values, missing postal/contact keys, payment adjustment, credit-document magnitudes, currency/rate grouping, future unbounded contracts and checklist lapse recalculation. Calculations are independently checkable; complete jurisdictional behavior remains gated by the external receiver contracts and executed report/invoice fixtures.
