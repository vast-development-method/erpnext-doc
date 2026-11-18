# Accounting and tax

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Egyptian electronic tax submission

Group invoices and debit and credit notes into a signed submission. Persist each member’s validation state. Process a cancellation against the accepted document identity. Initial acceptance of one member leaves its final validation pending.

**Worked case.** One signed submission contains invoice INV-001 and invoice INV-002. The test provider returns 202 with an external ID for INV-001 and a structure error for INV-002. Only INV-001 awaits final validation. INV-002 is flagged for correction. Neither is recorded as finally approved. Arabic and German views preserve both internal IDs, the official error code and the exact signed request.

### Additional decisions

Model issuer, source document revision, document type/version, customer, tax and product codes, original-invoice references, signed content digest, submission attempt, external document ID and validation events. Capture source values and outbound representations separately. The adapter can queue a batch, process accepted and rejected members independently and refresh each accepted document’s status. Keep cancellations and adjustment documents tied to the targeted authority IDs. Do not infer tax acceptance or reverse the ERP ledger from a transport acknowledgement alone.

## Forward exchange contract allocation

Allocate part or all of a forward contract across one or more payments. Track the unallocated balance in contract units. On a profitable cancellation of an export forward, debit the bank and credit exchange gain for the difference between contract proceeds and cancellation proceeds.

**Worked case.** An export contract sells USD 1,000 at 17.50 NAD/USD and USD 600 has been utilized. The operator cancels USD 100 at 17.20 NAD/USD, with no fees. USD 300 remains and a NAD 30 gain balances a NAD 30 bank debit. Currency pair, quote direction, allocations and journal amounts survive a language change.

### Additional decisions

Keep the currency pair, quote denominator, units, rate precision and approved booked rate on the contract. Treat utilizations and cancellations as individually identified movements. Remaining contract units equal booked units less effective utilizations and effective cancellations. Assign one payment allocation ID per contract leg. Apply the legs atomically and serialize competing draws on the same remaining balance. Link the cancellation to its journal and preserve both sides of a subsequently authorized reversal.

Translate hedge-type, gain/loss and status captions. Fix bank references, account IDs, currency codes and rational rate direction independently of language. Input may use locale-specific decimals; after explicit locale parsing, persist canonical decimals. Render monetary values with their currency codes. A French-speaking clerk and German-speaking reviewer can share a contract while maintaining the same signed rate and amount.

## Invoice image and document extraction

Choose receivable or payable, attach the original invoice, extract header and line values, and compare the declared total with the independently calculated line total. An authorized reviewer confirms a linked draft in the selected ledger. Keep extraction distinct from posting.

**Worked case.** The German PDF shows 14.07.2023 and a single EUR 1.234,50 line; the clerk works in English. Extract, review and confirm the same import twice. One linked draft has the date 2023-07-14 and amount EUR 1234.50, with its source available for review. Changing the review language preserves source strings, party identity, canonical date and decimal value.

### Additional decisions

An authorized clerk selects direction and company, attaches a file and requests an extraction using its attachment ID. Preserve the file hash, original text, document-language hints, extracted strings and reviewer corrections. Limit candidate parties to the authorized business scope. Match on stable party identity and show competing matches for review. Currency precision comes from the currency metadata. A model suggestion must never determine a posting by itself.

Show translated field captions beside the supplier’s original words. Preserve names, identifiers and line descriptions, including mixed scripts. Parse decimal and date conventions from document evidence separately from the reviewer’s UI locale. Present questionable values with their source text. Require a reviewer to confirm direction, party, date, amounts and currency before producing one linked draft per approved import revision.

## Employee advance and return in Yemen

A normal employee advance debits the designated advance account and credits the funding account. A return exchanges the two legs. Preserve transaction currency, company currency, employee identity and exchange rate on both vouchers.

**Worked case.** An advance is 100 transaction units at 2 company units per unit, with matching account setup. Finance submits the advance and records a full return at the same rate. The advance debits and credits 200 company units; the return exchanges the legs and offsets both balances. Arabic and English report views retain the same account codes, vouchers, currency and values.

### Additional decisions

Maintain a stable voucher identity, employee or party reference, company, project/dimension, accounts, transaction and base amounts and posting status. Submission, return and cancellation each need an auditable link to the original and a balanced journal. Keep HR attendance and finance permissions independent. Render report column names, status text and amount-in-words output in the requested language. Preserve employee names, account codes, voucher references and currency identities. A Yemen company can issue an Arabic voucher and show the same transaction to an English-speaking auditor.

## Sales order advance and instalment invoicing

Submitting an order with a first instalment date creates its schedule and an advance invoice. Additional charges belong on the advance invoice. Issue each later instalment two days before its due date and deduplicate by order and schedule line. Allocate any rounding residual to a specified line.

**Worked case.** An order has principal 1,000, a 20% advance, freight 50 and three installments from 15 January. The first scheduled invoicing run executes twice on 13 January with no payment. The down-payment invoice is 250 and exactly one first-installment invoice for 266.67 exists, all of it outstanding. Changing the customer’s language retains the principal, due date, allocated amount and unique invoice origin.

### Additional decisions

Track invoice generation and payment settlement separately. The advance covers only its agreed share of the principal plus the separately charged amount. Cash receipts, credits and reversals alter open balances through allocation. Staff can see an invoice has been issued while its full value remains outstanding. Translate the template name, charge description, reminder and customer-facing due-date label. Keep percentages, scheduled civil dates, currency and invoice origins stable when changing language.

## British return aggregation

Map item tax lines or invoice-level tax, apply journal adjustments and close the reporting period against its tax accounts. Store period, registration, report box and submission receipt. Distinguish reviewed, transmitted and authority-acknowledged returns.

**Worked case.** A working paper includes two tax lines of 12 and 8, their invoice-level summary of 20, and a separate mapped adjustment of minus 2. A Welsh-speaking preparer and an English-speaking filer open the same reviewed reporting period. Both views show 18 in the configured bucket, with the invoice summary excluded from double counting. Changing the reporting language preserves the registration, period key, box identities, evidence links and amounts.
