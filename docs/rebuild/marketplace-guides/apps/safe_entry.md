# Treasury Entry

Brandimic describes a treasury register for receipts and payments made by cash or cheque. A System Manager or Accounts Manager configures a Treasury with a name, company, main treasury account and payment-mode account. On a Treasury Entry the operator selects that treasury, payment direction and mode, and indicates whether the transaction is party-based. Treasury List provides the transaction overview. The version selector lists 13 and 14. The publisher's narrative also mentions 12. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/safe_entry)

## Proposed recording contract

| Step | Data and effect |
|---|---|
| Configure treasury | Authorize the manager for the company, resolve both configured accounts and retain the setup revision used by each entry. |
| Record transaction | Accept treasury ID, posting date, amount, explicit currency, canonical direction, mode, party flag, optional party and instrument reference. The proposed contract requires a party for a party-based row and a cheque number for cheque mode. |
| Review and post | Resolve a balanced posting or a link to the core payment voucher according to company accounting policy. Store the posting identity and prevent a repeated submission from creating another voucher. An unposted register entry remains visibly distinguishable. |
| Inspect list | Filter by company, treasury, direction, date and party flag. Present receipt and payment totals separately before deriving net movement. Corrections reference the original entry. |

## Multilingual acceptance

A clerk using Afrikaans records a cash receipt of 250.00 against party C-44 and a non-party cash payment of 75.00 at the same treasury, date and currency. A German-speaking reviewer sees receipts of 250.00, payments of 75.00 and net movement of +175.00. Returning to the party-only filter leaves the receipt. Persist direction, mode and party IDs independently of words such as *ontvang* or *uitbetaling*.

In the proposed contract a party-based receipt without a party returns a localized field error and no posting. If a clerk changes the form language while entering cheque `000381`, the mode remains cheque and every digit survives. The printed payee or drawer text is kept as entered, with a separate recipient-language receipt caption.

**Qualification.** The screenshots and listing establish the setup instructions and user-facing classifications. The exact voucher generated, balancing rule, account mappings, reversal workflow and existing translation resources remain unverified. [Named repository](https://github.com/Brandimic0/erpnext_safe_entry)
