# Accounting and tax

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Egyptian electronic tax submission

Group invoices and debit and credit notes into a signed submission. Persist each member’s validation state. Process a cancellation against the accepted document identity. Initial acceptance of one member leaves its final validation pending.

**Worked case.** One signed submission contains invoice INV-001 and invoice INV-002. The test provider returns 202 with an external ID for INV-001 and a structure error for INV-002. Only INV-001 awaits final validation. INV-002 is flagged for correction. Neither is recorded as finally approved. Arabic and German views preserve both internal IDs, the official error code and the exact signed request.

### Additional decisions

Model issuer, source document revision, document type/version, customer, tax and product codes, original-invoice references, signed content digest, submission attempt, external document ID and validation events. Capture source values and outbound representations separately. The adapter can queue a batch, process accepted and rejected members independently and refresh each accepted document’s status. Keep cancellations and adjustment documents tied to the targeted authority IDs. Do not infer tax acceptance or reverse the ERP ledger from a transport acknowledgement alone.

#### Correlating a mixed submission

Store the signed-request digest and internal document ID before transmission. Record the submission identifier once at batch level and the authority’s document identifier or rejection details separately for each member. For a correction, link the new document revision to the rejected member. Preserve the originally signed bytes and its error code. Refresh the accepted member through its external identifier. A late validation response must match that same member before changing its state.

If the accepted invoice later fails validation, keep the original initial acceptance, the later rejection and their timestamps. Count zero finally validated documents in this two-invoice example until an accepted member completes validation. Resubmitting the corrected second invoice must leave both the first invoice’s validation history and the ERP’s issued invoice ledger intact. The authority response, the correction workflow and the accounting disposition each have their own identity.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/e_invoice.md).

## Forward exchange contract allocation

Allocate part or all of a forward contract across one or more payments. Track the unallocated balance in contract units. On a profitable cancellation of an export forward, debit the bank and credit exchange gain for the difference between contract proceeds and cancellation proceeds.

**Worked case.** An export contract sells USD 1,000 at 17.50 NAD/USD and USD 600 has been utilized. The operator cancels USD 100 at 17.20 NAD/USD, with no fees. USD 300 remains and a NAD 30 gain balances a NAD 30 bank debit. Currency pair, quote direction, allocations and journal amounts survive a language change.

### Additional decisions

Keep the currency pair, quote denominator, units, rate precision and approved booked rate on the contract. Treat utilizations and cancellations as individually identified movements. Remaining contract units equal booked units less effective utilizations and effective cancellations. Assign one payment allocation ID per contract leg. Apply the legs atomically and serialize competing draws on the same remaining balance. Link the cancellation to its journal and preserve both sides of a subsequently authorized reversal.

Translate hedge-type, gain/loss and status captions. Fix bank references, account IDs, currency codes and rational rate direction independently of language. Input may use locale-specific decimals; after explicit locale parsing, persist canonical decimals. Render monetary values with their currency codes. A French-speaking clerk and German-speaking reviewer can share a contract while maintaining the same signed rate and amount.

### Detailed workflow and cases

<a id="forward-exchange-contract-allocation-3"></a>

#### Operating rules

| Acceptance example | Expected result |
|---|---|
| Book an exporter sale of USD 1,000 at 17.50 NAD per USD. Allocate USD 600 to one receipt and cancel USD 100 at 17.20 NAD per USD. Ignore fees in this target example. | USD 300 remains. For the stated sell-USD direction, closing USD 100 at a 0.30 differential gives a NAD 30 gain, with equal bank debit and gain credit under the example's cash-settled convention. A translation change leaves both journal legs intact. |
| Two clerks attempt to use USD 200 each from the remaining USD 300. | Only one draw succeeds at that balance. The other receives the available USD 100 and a localized rejection. No partial posting occurs. |
| A payment uses two contracts with different rates or one leg has the wrong currency pair. | Preserve the amount and booked rate on each valid leg. A mismatched pair rejects the whole request before balances or journals change. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/forward_contract.md).

## Invoice image and document extraction

Choose receivable or payable, attach the original invoice, extract header and line values, and compare the declared total with the independently calculated line total. An authorized reviewer confirms a linked draft in the selected ledger. Keep extraction distinct from posting.

**Worked case.** The German PDF shows 14.07.2023 and a single EUR 1.234,50 line; the clerk works in English. Extract, review and confirm the same import twice. One linked draft has the date 2023-07-14 and amount EUR 1234.50, with its source available for review. Changing the review language preserves source strings, party identity, canonical date and decimal value.

### Additional decisions

An authorized clerk selects direction and company, attaches a file and requests an extraction using its attachment ID. Preserve the file hash, original text, document-language hints, extracted strings and reviewer corrections. Limit candidate parties to the authorized business scope. Match on stable party identity and show competing matches for review. Currency precision comes from the currency metadata. A model suggestion must never determine a posting by itself.

Show translated field captions beside the supplier’s original words. Preserve names, identifiers and line descriptions, including mixed scripts. Parse decimal and date conventions from document evidence separately from the reviewer’s UI locale. Present questionable values with their source text. Require a reviewer to confirm direction, party, date, amounts and currency before producing one linked draft per approved import revision.

### Detailed workflow and cases

<a id="invoice-image-and-document-extraction-2"></a>

#### Operating rules

| Acceptance example | Expected result |
|---|---|
| German PDF has a line “Beratung”, amount “1.234,50 EUR”, and date “18.11.2026”; clerk works in English | Review displays EUR 1234.50 and 2026-11-18 alongside their source strings. Approval produces one linked draft carrying currency EUR. Repeating the same approval returns that draft. |
| Input states “03/04/26” with no further date context or contains an image without extractable text | Flag the date for review or route the file for explicit OCR/manual entry. The import remains unposted, with its source available to an authorized clerk. |
| Header total differs from reviewed lines, taxes and rounding | Show the signed discrepancy and prevent final approval until it is explained. Switching UI language preserves the same decimal value and review decision. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/ipconnex_ai_invoice.md).

## Employee advance and return in Yemen

A normal employee advance debits the designated advance account and credits the funding account. A return exchanges the two legs. Preserve transaction currency, company currency, employee identity and exchange rate on both vouchers.

**Worked case.** An advance is 100 transaction units at 2 company units per unit, with matching account setup. Finance submits the advance and records a full return at the same rate. The advance debits and credits 200 company units; the return exchanges the legs and offsets both balances. Arabic and English report views retain the same account codes, vouchers, currency and values.

### Additional decisions

Maintain a stable voucher identity, employee or party reference, company, project/dimension, accounts, transaction and base amounts and posting status. Submission, return and cancellation each need an auditable link to the original and a balanced journal. Keep HR attendance and finance permissions independent. Render report column names, status text and amount-in-words output in the requested language. Preserve employee names, account codes, voucher references and currency identities. A Yemen company can issue an Arabic voucher and show the same transaction to an English-speaking auditor.

### Detailed workflow and cases

<a id="employee-advance-and-return-in-yemen-1"></a>

#### Operating rules

| Proposed acceptance case | Expected result |
|---|---|
| An authorized officer submits an advance for 100 transaction units at 2 company units per transaction unit. | Debit and credit are each 200 company units. A return of the same 100 at the same rate exchanges the legs. Arabic and English reports select the same vouchers. |
| Cancel the original advance on a separate fixture with no dependent return, then repeat the request. | The ledger is reversed exactly once, the persisted voucher shows cancelled, and report drill-down exposes the reversal reference in either language. |
| Run an attendance report for an employee scheduled 08:00–17:00 with scans at 08:10 and 16:50. | It shows 10 minutes late entry, 10 minutes early exit and an 8 h 40 min first-to-last span. The span is labeled distinctly from paid hours. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/pav.md).

## Sales order advance and instalment invoicing

Submitting an order with a first instalment date creates its schedule and an advance invoice. Additional charges belong on the advance invoice. Issue each later instalment two days before its due date and deduplicate by order and schedule line. Allocate any rounding residual to a specified line.

**Worked case.** An order has principal 1,000, a 20% advance, freight 50 and three installments from 15 January. The first scheduled invoicing run executes twice on 13 January with no payment. The down-payment invoice is 250 and exactly one first-installment invoice for 266.67 exists, all of it outstanding. Changing the customer’s language retains the principal, due date, allocated amount and unique invoice origin.

### Additional decisions

Track invoice generation and payment settlement separately. The advance covers only its agreed share of the principal plus the separately charged amount. Cash receipts, credits and reversals alter open balances through allocation. Staff can see an invoice has been issued while its full value remains outstanding. Translate the template name, charge description, reminder and customer-facing due-date label. Keep percentages, scheduled civil dates, currency and invoice origins stable when changing language.

### Detailed workflow and cases

<a id="sales-order-advance-and-instalment-invoicing-1"></a>

#### Operating rules

Freeze the commercial basis on submission: order, currency, eligible sales base, advance share, installment count, first due date, frequency and distinct extra-charge lines. Represent schedule rows with a stable key, principal share, due date, invoice reference, paid allocations and balance. Allocate any rounding residual to a specified row. Link the advance and each scheduled invoice to that order and row. A unique invoice origin prevents duplicate creation if the scheduler retries or two workers pick up the same date. Define the site's calendar-day cut-off and a catch-up policy for missed runs.

| Proposed acceptance case | Expected result |
|---|---|
| An order has a principal of 1,000.00, an advance of 20%, separate freight of 50.00 and three equal monthly installments from 15 January. Use a two-decimal currency and put the residual in the final row. | The immediate invoice is 250.00. The installments are 266.67, 266.67 and 266.66. Total invoiced after all runs is 1,050.00 and the sales principal remains 1,000.00. |
| Run the scheduler twice on 13 January for the first installment, with no cash receipt. | One 266.67 invoice is linked to the 15 January row. Its paid allocation is zero and 266.67 remains outstanding. |
| An Arabic-speaking customer receives the schedule made in a German interface and pays 100.00 against the first installment. | The same invoice and due date are shown, 166.67 remains open and the other scheduled rows retain their amounts. Reversing that allocation restores 266.67. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/payment_installment_kanak.md).

## British return aggregation

Map item tax lines or invoice-level tax, apply journal adjustments and close the reporting period against its tax accounts. Store period, registration, report box and submission receipt. Distinguish reviewed, transmitted and authority-acknowledged returns.

**Worked case.** A working paper includes two tax lines of 12 and 8, their invoice-level summary of 20, and a separate mapped adjustment of minus 2. A Welsh-speaking preparer and an English-speaking filer open the same reviewed reporting period. Both views show 18 in the configured bucket, with the invoice summary excluded from double counting. Changing the reporting language preserves the registration, period key, box identities, evidence links and amounts.

### Detailed workflow and cases

<a id="british-return-aggregation-2"></a>

#### Operating rules

Store box identifiers, obligation keys and HMRC evidence as received. A user can display the same working paper in English or Welsh using reviewed labels. Use the definitive declaration required by the applicable HMRC process and retain the presented wording, version and language. Translation of an explanation cannot change the return or replace an official declaration. Reporting period, jurisdiction, authority payload schema and reporting units belong to the filing configuration and are independent of the preparer's language. Where an official rendering is unavailable, display its available language and distinguish any explanatory translation.

<a id="british-return-aggregation-3"></a>

#### Acceptance cases

- An isolated test dataset contains two mapped output-tax lines of 12.00 and 8.00, an invoice summary of 20.00 representing those same lines, and a separate eligible adjustment of −2.00. For this configured output-tax bucket the result is 18.00 in both language views. The trace identifies the two lines and adjustment exactly once.
- A Welsh-speaking preparer and an English-speaking authorized filer open the same reviewed period. They see the same box identifiers, values and evidence references. The filed result links to one receipt. Reopening it in Welsh cannot submit a second return or book another closing journal.
- If acknowledgement times out after submission, mark submission uncertain, query the period and reconcile before retrying. A payment in the liabilities view cannot by itself mark an unsubmitted draft as filed. A user authorized for a different registration cannot inspect or file it.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/uk.md).
