# Banking and treasury

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Cheque approval and collection

Submission creates the customer instrument. A deposit groups eligible instruments by bank. Match deposited instruments by reference and linked journal before recording clearance or return. Apply the approval threshold before creation of the posting journal.

**Worked case.** The company has an active approval threshold of 1,000 and receives a cheque for exactly 1,000. Submit it, reload it in a new session and then approve it as Accounts Manager. It remains pending with no journal before approval, and approval posts exactly one journal. Arabic and English receipts use the same instrument number, approval event and monetary amount.

### Additional decisions

Give each authorised transition an event ID and references to its journal, deposit slip and originating bank transaction. Commit workflow status and its accounting effect together. An approval request should stay visible to the manager after commit, while no journal posts until approval. Require manual review when a reference, account, amount or direction is ambiguous.

## Saved payment method collections

Use the customer’s saved payment method, identified merchant and invoice currency. Record the external collection request separately from confirmed capture. On confirmation, allocate a single customer receipt to the open invoice.

**Worked case.** A French-speaking payer starts one collection against an English invoice with EUR 40 outstanding. Send the same collection request twice and replay the provider's successful event. One provider charge is allocated once for EUR 40; the invoice balance is zero. Receipt language does not change payer, merchant, provider reference, currency or amount.

## Post-dated cheque settlement

Receiving a customer cheque or issuing a supplier cheque opens a payment against the configured holding account. Deposit creates the bank journal. Clearance records the clearing date against that journal. Link a dishonour to the original instrument and postings.

**Worked case.** One customer owes 400.00 in the company currency and pays by cheque 00072. The configured holding account starts at zero. Record the receipt, deposit it, confirm clearance, then replay the same clearing request. The invoice is allocated once, the bank increases by 400.00, the holding account returns to zero and replay creates no extra journal. The German reviewer sees the same instrument 00072, dates, amount and linked voucher IDs as the Afrikaans-speaking clerk.

### Additional decisions

Store company, instrument ID, printed number, bank, direction, party, cheque date, amount and currency, invoice allocations, interim account, source voucher and transition history. Preserve the printed cheque number as text. Keep the instrument date, accounting date and clearing date distinct. Authorize entry and clearance against the owning company. Each clearance batch returns the result per instrument so an operator can resolve a failure without re-clearing successful rows.

## Bank statement import and duplicate review

Select a bank account and its statement layout, preview date, deposit, withdrawal, reference and description, then review repeat references. Import accepted rows as unreconciled bank movements. Identify conflicting amounts separately from matching repeats.

**Worked case.** A configured source format uses comma decimals. An account receives reference 00038 with amount 1.234,50. Import it twice, then import a third observation of the same reference for 1.234,55. One transaction is committed, the identical observation is linked as a duplicate, and the conflicting amount goes to review. Operator language cannot alter the bank number format, original description or leading zeros in a reference.

### Additional decisions

An operator chooses a company, bank account, file and a versioned import profile. Stage the original file as a restricted attachment. For each line retain its ordinal, original text or restricted source pointer, bank reference, value date, amount, currency and description. Decode the file with the source profile, identify ignorable headers or footers, then parse and validate monetary values before committing a Bank Transaction. Reconciliation to invoices and ledger vouchers is a subsequent decision.

## Treasury transaction register

Each treasury has payable and receivable accounts per payment mode. A clerk may enter direct account lines or select a party and allocate amounts to its outstanding invoices. A party-only register includes only movements with a recorded party.

**Worked case.** One treasury records a party-linked cash receipt of 250.00 and a non-party cash payment of 75.00 in the same currency. Open the register in a different language, inspect the totals and apply the party-only filter. The net movement is +175.00. The party filter returns only the receipt for 250.00. Direction codes, party IDs and source amounts are independent of their translated captions.

## Supplier payment batch authorization

Select outstanding supplier payment instructions, authorize a batch with a one-time challenge and track each bank response separately. The selected transfer method and bank reference survive retries and partial batch rejection.

**Worked case.** An approved two-line supplier payout batch has one bank-confirmed instruction and one rejected instruction. Process the bank response twice and issue advice for the successfully paid supplier. One confirmed payment receives one advice. The rejected item remains unpaid with its original bank reason. The Hindi operator, English approver and German-speaking recipient see localized messages for identical payment and bank identifiers.

## Online and terminal payment collection

Verify the company contact and authorize the merchant account. Associate each online or terminal payment method with a settlement path. A payment request supports hosted checkout or a saved recurring method. A cashier associates a terminal capture with the same payable document.

**Worked case.** A submitted EUR 35.70 invoice has a French-speaking payer and a German-speaking cashier. The payer completes checkout and the provider delivers the same verified success event twice. Allocate EUR 35.70 once and show the same settled invoice on both language views. The checkout and receipt may use the payer’s language while the invoice identity and currency remain unchanged.

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
