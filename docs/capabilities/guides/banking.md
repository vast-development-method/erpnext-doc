# Banking and treasury

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Cheque approval and collection

Submission creates the customer instrument. A deposit groups eligible instruments by bank. Match deposited instruments by reference and linked journal before recording clearance or return. Apply the approval threshold before creation of the posting journal.

**Worked case.** The company has an active approval threshold of 1,000 and receives a cheque for exactly 1,000. Submit it, reload it in a new session and then approve it as Accounts Manager. It remains pending with no journal before approval, and approval posts exactly one journal. Arabic and English receipts use the same instrument number, approval event and monetary amount.

### Additional decisions

Give each authorised transition an event ID and references to its journal, deposit slip and originating bank transaction. Commit workflow status and its accounting effect together. An approval request should stay visible to the manager after commit, while no journal posts until approval. Require manual review when a reference, account, amount or direction is ambiguous.

### Detailed workflow and cases

<a id="cheque-approval-and-collection-3"></a>

#### Operating rules

- With a threshold of 1,000, submit a cheque for exactly 1,000 and query it in a fresh session. Expect pending approval and no journal. A manager approves it once. Retrying the command returns the posted journal ID.
- A cheque for 1,000 is received, deposited and collected. The bank increases by 1,000, customer receivables decrease by 1,000, and the two intervening clearing balances net to zero. Reimporting the bank line leaves the balances unchanged.
- Two companies deposit cheques numbered 0123. A statement lacking the account context must leave both untouched. A bank’s local-language return code takes precedence over translating free text.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/cheque.md).

## Saved payment method collections

Use the customer’s saved payment method, identified merchant and invoice currency. Record the external collection request separately from confirmed capture. On confirmation, allocate a single customer receipt to the open invoice.

**Worked case.** A French-speaking payer starts one collection against an English invoice with EUR 40 outstanding. Send the same collection request twice and replay the provider's successful event. One provider charge is allocated once for EUR 40; the invoice balance is zero. Receipt language does not change payer, merchant, provider reference, currency or amount.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/ipconnex_stripe_payment.md).

## Post-dated cheque settlement

Receiving a customer cheque or issuing a supplier cheque opens a payment against the configured holding account. Deposit creates the bank journal. Clearance records the clearing date against that journal. Link a dishonour to the original instrument and postings.

**Worked case.** One customer owes 400.00 in the company currency and pays by cheque 00072. The configured holding account starts at zero. Record the receipt, deposit it, confirm clearance, then replay the same clearing request. The invoice is allocated once, the bank increases by 400.00, the holding account returns to zero and replay creates no extra journal. The German reviewer sees the same instrument 00072, dates, amount and linked voucher IDs as the Afrikaans-speaking clerk.

### Additional decisions

Store company, instrument ID, printed number, bank, direction, party, cheque date, amount and currency, invoice allocations, interim account, source voucher and transition history. Preserve the printed cheque number as text. Keep the instrument date, accounting date and clearing date distinct. Authorize entry and clearance against the owning company. Each clearance batch returns the result per instrument so an operator can resolve a failure without re-clearing successful rows.

### Detailed workflow and cases

<a id="post-dated-cheque-settlement-3"></a>

#### Operating rules

| Operation | Required decision and effect |
|---|---|
| Record receipt or issue | Resolve the company holding account and party account. Persist the instrument and allocation voucher together under one request key. |
| Deposit and clear | For a customer receipt held in an asset account, deposit transfers the amount from the holding account to the bank. Clearance marks that bank movement as confirmed. For a supplier issue, resolve the payable-side holding configuration. Record the bank evidence and voucher identity. |
| Record a bounce | Require a date, reason and original voucher. Reverse the applicable movement and reopen affected allocations using the core settlement service. Link corrective vouchers to the original. |

<a id="post-dated-cheque-settlement-4"></a>

#### Acceptance cases

1. An Afrikaans-speaking clerk records cheque `00072` for a customer with an open 400.00 invoice in the same currency. Under the proposed receipt configuration the voucher debits the holding account 400.00 and credits the customer 400.00. A German-speaking reviewer deposits and then clears it. The bank increases by 400.00, the holding account returns to zero and the original voucher and instrument IDs agree in both views.
2. Submit clearance twice with the same bank reference and request key. Both responses identify the same posting. A subsequent conflicting amount routes to review. Translate these two outcomes separately.
3. Preserve a bank's original bounce reason, such as `Signature diffère`, and show a translated classification alongside it. A language change leaves exchange rates, transaction currency, cheque date and ledger mappings intact.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/pdc_cheque_management.md).

## Bank statement import and duplicate review

Select a bank account and its statement layout, preview date, deposit, withdrawal, reference and description, then review repeat references. Import accepted rows as unreconciled bank movements. Identify conflicting amounts separately from matching repeats.

**Worked case.** A configured source format uses comma decimals. An account receives reference 00038 with amount 1.234,50. Import it twice, then import a third observation of the same reference for 1.234,55. One transaction is committed, the identical observation is linked as a duplicate, and the conflicting amount goes to review. Operator language cannot alter the bank number format, original description or leading zeros in a reference.

### Additional decisions

An operator chooses a company, bank account, file and a versioned import profile. Stage the original file as a restricted attachment. For each line retain its ordinal, original text or restricted source pointer, bank reference, value date, amount, currency and description. Decode the file with the source profile, identify ignorable headers or footers, then parse and validate monetary values before committing a Bank Transaction. Reconciliation to invoices and ledger vouchers is a subsequent decision.

### Detailed workflow and cases

<a id="bank-statement-import-and-duplicate-review-1"></a>

#### Operating rules

| Input for the same bank account | Proposed handling |
|---|---|
| New non-empty bank reference with well-formed values | Create a statement transaction once, recording the source line and profile revision. |
| Existing reference and identical material values | Classify as duplicate and link to the existing transaction. |
| Existing reference with changed amount, date or currency | Hold both observations for a reviewer. Never discard a correction as an ordinary repeat. |
| Missing reference, unknown column layout or ambiguous date | Return a localized diagnostic identifying the row or file. Require explicit resolution before posting the affected row. |

<a id="bank-statement-import-and-duplicate-review-2"></a>

#### Acceptance cases

Use a synthetic profile with Bosnian headings, comma decimals and an explicit day/month/year date pattern. Import a row with debtor text `Željko Hadžić`, reference `00038`, amount `1.234,50` and date `05.06.2026`. Under an English or German interface the result is the same original name, reference, exact decimal 1234.50 and date 2026-06-05. The operator can translate the classification and column captions while viewing the bank's original wording.

Re-import the example, then import a second file carrying the same account and reference with 1234.55. Expect one committed transaction, one duplicate response and one review item. Switching display language cannot resolve a discrepancy. Source currency comes from the agreed account or file profile.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/procreditbank.md).

## Treasury transaction register

Each treasury has payable and receivable accounts per payment mode. A clerk may enter direct account lines or select a party and allocate amounts to its outstanding invoices. A party-only register includes only movements with a recorded party.

**Worked case.** One treasury records a party-linked cash receipt of 250.00 and a non-party cash payment of 75.00 in the same currency. Open the register in a different language, inspect the totals and apply the party-only filter. The net movement is +175.00. The party filter returns only the receipt for 250.00. Direction codes, party IDs and source amounts are independent of their translated captions.

### Detailed workflow and cases

<a id="treasury-transaction-register-2"></a>

#### Operating rules

| Step | Data and effect |
|---|---|
| Configure treasury | Authorize the manager for the company, resolve the main treasury account and the payable and receivable mappings for the selected payment mode and retain the setup revision used by each entry. |
| Record transaction | Accept treasury ID, posting date, amount, explicit currency, canonical direction, mode, party flag, optional party and instrument reference. The proposed contract requires a party for a party-based row and a cheque number for cheque mode. |
| Review and post | Resolve a balanced posting or a link to the core payment voucher according to company accounting policy. Store the posting identity and prevent a repeated submission from creating another voucher. An unposted register entry remains visibly distinguishable. |
| Inspect list | Filter by company, treasury, direction, date and party flag. Present receipt and payment totals separately before deriving net movement. Corrections reference the original entry. |

<a id="treasury-transaction-register-3"></a>

#### Acceptance cases

A clerk using Afrikaans records a cash receipt of 250.00 against party C-44 and a non-party cash payment of 75.00 at the same treasury, date and currency. A German-speaking reviewer sees receipts of 250.00, payments of 75.00 and net movement of +175.00. Returning to the party-only filter leaves the receipt. Persist direction, mode and party IDs independently of words such as *ontvang* or *uitbetaling*.

In the proposed contract a party-based receipt without a party returns a localized field error and no posting. If a clerk changes the form language while entering cheque `000381`, the mode remains cheque and every digit survives. The printed payee or drawer text is kept as entered, with a separate recipient-language receipt caption.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/safe_entry.md).

## Supplier payment batch authorization

Select outstanding supplier payment instructions, authorize a batch with a one-time challenge and track each bank response separately. The selected transfer method and bank reference survive retries and partial batch rejection.

**Worked case.** An approved two-line supplier payout batch has one bank-confirmed instruction and one rejected instruction. Process the bank response twice and issue advice for the successfully paid supplier. One confirmed payment receives one advice. The rejected item remains unpaid with its original bank reason. The Hindi operator, English approver and German-speaking recipient see localized messages for identical payment and bank identifiers.

### Detailed workflow and cases

<a id="supplier-payment-batch-authorization-1"></a>

#### Operating rules

| Operation | Request and durable result |
|---|---|
| Prepare batch | The accounts operator selects organization, eligible source bank account, mode and open Payment Entries. Bind each instruction to its payee bank identifiers, reference, exact amount and currency. Freeze a digest of the batch submitted for approval. |
| Authorize and submit | A bank-authorized user completes the configured challenge. Send each instruction under a stable request identity. Audit the authorization outcome and timestamp without storing the OTP in logs. Editing beneficiary or amount invalidates the earlier approval. |
| Reconcile outcome | Keep bank acknowledgement, per-line status, bank reference and settlement evidence. A timeout leaves a line pending inquiry. Resolve that reference before any resend. One rejected instruction leaves other line outcomes intact. |
| Apply a collection | Correlate a bank-confirmed inward item to a receipt or an unmatched item awaiting review. Do not infer the payer's invoice purely from a similar localized name. |

<a id="supplier-payment-batch-authorization-2"></a>

#### Acceptance cases

A clerk works in Hindi, an approver in English and the supplier wants German remittance advice. Approve a two-instruction batch. Feed one confirmed bank reference and one rejection. The first supplier gets one advice in its requested language, the second remains unpaid. A repeated bank status message creates no second advice or voucher. Numbers, references, bank codes, submitted beneficiary name and provider status remain traceable in their original form.

If approval expires after the user changes UI language, refuse submission and offer the localized reauthorization flow. If the bank status is unknown, distinguish “waiting for confirmation” from “failed” in every translation. Determine currency and rail eligibility from the bank agreement and account setup, independently of display language.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/sanpra_easypay.md).

## Online and terminal payment collection

Verify the company contact and authorize the merchant account. Associate each online or terminal payment method with a settlement path. A payment request supports hosted checkout or a saved recurring method. A cashier associates a terminal capture with the same payable document.

**Worked case.** A submitted EUR 35.70 invoice has a French-speaking payer and a German-speaking cashier. The payer completes checkout and the provider delivers the same verified success event twice. Allocate EUR 35.70 once and show the same settled invoice on both language views. The checkout and receipt may use the payer’s language while the invoice identity and currency remain unchanged.

### Detailed workflow and cases

<a id="online-and-terminal-payment-collection-2"></a>

#### Operating rules

| Operation | Inputs and authority | Result and exception |
|---|---|---|
| Prepare collection | Company-authorized cashier, submitted request ID, mode, amount and currency from the request | Return hosted checkout, recurring attempt or paired terminal reference. Reject a test/live or company/reader mismatch before collecting. |
| Apply collection | Verified event for the connected account, provider transaction reference, amount, currency and request | Store its disposition; post and allocate exactly once on confirmed success. An incomplete or delayed method remains pending. A mismatch goes to reconciliation. |
| Notify payer | Settled request, recorded recipient and preferred document language | Render the receipt and optional document copy in that language. Retain version, reference and delivery disposition. A failed notification leaves settlement intact. |

<a id="online-and-terminal-payment-collection-3"></a>

#### Acceptance cases

- A German-speaking cashier opens online collection for a French-speaking payer's EUR 35.70 invoice. Checkout shows the selected supported French locale. Two copies of the same success event yield one EUR 35.70 allocation. Retrieve the document in German and the same invoice reference and balance remain visible.
- A saved recurring method requires customer action. Preserve the open request, provide the payer with a localized action prompt, and issue the paid receipt only after confirmation.
- A terminal registered for a second company or a webhook carrying a different currency cannot settle the request. The operator sees a translated reason and the reconciliation record retains the original currency and event reference.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/stripe2.md).

## Clearing accounts for cheque movements

| Event | Debit | Credit |
|---|---|---|
| Receive a customer cheque | Bills receivable | Customer receivable |
| Deposit with the bank | Cheques under collection | Bills receivable |
| Confirm collection | Bank | Cheques under collection |
| Bank returns the cheque unpaid | Bills receivable | Cheques under collection |
| Hand the instrument back to the customer | Customer receivable | Bills receivable |
| Issue a cheque to a supplier | Supplier payable | Notes payable |
| Clear the issued cheque | Notes payable | Bank |
| Record bank charges | Bank charges expense | Bank |

Select eligible deposit-slip lines by company, date and instrument state and exclude cheques already assigned to a slip. A returned instrument may be presented again or handed back to its party. A deduction requires an expense account and must be less than the instrument's face value. Match an imported clearance to a submitted, deposited instrument and its journal using bank account, company, reference, direction and amount. If two companies deposit cheque 0123 and the statement lacks the account context, leave both instruments unchanged. A structured bank return code takes precedence over translated description text.
