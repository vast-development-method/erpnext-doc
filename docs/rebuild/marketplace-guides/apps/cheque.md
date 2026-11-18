# cheque

Ahmed’s listing covers received and issued cheques in versions 15 and 16, with deposit batches, journals, bank reconciliation, reminders and bilingual Arabic/English receipts. A submitted receipt creates its cheque. Deposit-slip selection filters by company, date and status, and excludes cheques already assigned to a slip. The listing also describes endorsement, agent collection, discounting and bank charges. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/cheque)

## Business events and journal effects

| Event | Debit | Credit |
|---|---|---|
| Receive a customer cheque | Bills receivable | Customer receivable |
| Deposit it with the bank | Cheques under collection | Bills receivable |
| Bank confirms collection | Bank | Cheques under collection |
| Bank returns it unpaid | Bills receivable | Cheques under collection |
| Hand it back to the customer | Customer receivable | Bills receivable |
| Issue a cheque to a supplier | Supplier payable | Notes payable |
| Bank clears the issued cheque | Notes payable | Bank |
| Record bank charges | Bank charges expense | Bank |

These nominal account roles come from the publisher’s transition descriptions. Account selections depend on company setup. A returned cheque may be deposited again or returned to the party. An issued cheque follows its own state machine. [Listing and posting map](https://cloud.frappe.io/marketplace/apps/cheque) · [Recovered transition table](https://github.com/MohamedAbdulsalam96/cheque/blob/f7c198056dfc829c6326e559cd8943ea385a41dc/cheque/cheque/doctype/cheque/cheque.py#L8)

## What the recovered source implements

The public copy’s package names Ahmed Abukhatwa as author and describes the same cheque lifecycle. The source threshold comparison is inclusive when the configured threshold is positive. The submit handler writes a pending approval status and then raises an exception. A static reading does not establish whether a pending record persists after rollback. A deduction requires an account and must be smaller than the face amount. The manager check and permitted transition map appear on the cheque controller. [Package identity](https://github.com/MohamedAbdulsalam96/cheque/blob/f7c198056dfc829c6326e559cd8943ea385a41dc/pyproject.toml) · [Validation and approval](https://github.com/MohamedAbdulsalam96/cheque/blob/f7c198056dfc829c6326e559cd8943ea385a41dc/cheque/cheque/doctype/cheque/cheque.py#L53)

Bank reconciliation looks for a submitted deposited cheque matching the trimmed reference. It then requires a linked journal before recording the result. A withdrawal, or selected Arabic or English keywords in the description or transaction type, selects the returned path. A positive deposit otherwise selects collection. The lookup shown does not include company or bank account. A replacement needs an unambiguous scoped match. [Bank matching and return classification](https://github.com/MohamedAbdulsalam96/cheque/blob/f7c198056dfc829c6326e559cd8943ea385a41dc/cheque/utils/cheque_reconciliation.py#L13)

## Proposed rebuild and acceptance

Give each authorised transition an event ID and references to its journal, deposit slip and originating bank transaction. Commit workflow status and its accounting effect together. An approval request should stay visible to the manager after commit, while no journal posts until approval. Require manual review when a reference, account, amount or direction is ambiguous.

- With a threshold of 1,000, submit a cheque for exactly 1,000 and query it in a fresh session. Expect pending approval and no journal. A manager approves it once. Retrying the command returns the posted journal ID.
- A cheque for 1,000 is received, deposited and collected. The bank increases by 1,000, customer receivables decrease by 1,000, and the two intervening clearing balances net to zero. Reimporting the bank line leaves the balances unchanged.
- Two companies deposit cheques numbered 0123. A statement lacking the account context must leave both untouched. A bank’s local-language return code takes precedence over translating free text.

Render the same cheque ID, number, amount and date in both language copies. Support right-to-left labels while preserving the reading order and leading zeros of instrument numbers. Move the publisher’s pounds/piastres wording into a currency-specific print template. Capture approval evidence, statement mapping and journal references independently of the operator’s language. Runtime equivalence to the commercial build remains unverified.
