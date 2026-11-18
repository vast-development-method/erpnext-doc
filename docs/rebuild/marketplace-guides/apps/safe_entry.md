# Treasury Entry

Brandimic describes a treasury register for receipts and payments made by cash or cheque. A System Manager or Accounts Manager configures a Treasury with a name, company, main treasury account and payment-mode account. On a Treasury Entry the operator selects that treasury, payment direction and mode, and indicates whether the transaction is party-based. Treasury List provides the transaction overview. The version selector lists 13 and 14. The publisher's narrative also mentions 12. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/safe_entry)

## What the publisher's forms show

On the setup form, each payment mode has **separate payable and receivable account fields**. The entry form also has a posting date and a numbering series. With the party checkbox clear, the clerk enters Treasury Item rows with an account and amount and sees a total. With the box selected, the form shows a party type, an action to retrieve outstanding invoices and a payment-reference table with document type, name, grand total, outstanding and allocated amounts. The screenshot labels those columns EGP for the illustrated setup. It shows the allocation inputs on an unsaved document, with no posted result or voucher. [Treasury setup](https://i.postimg.cc/L6P2nqNw/Screenshot-from-2023-07-04-16-53-04.png) · [Entry without a party](https://i.postimg.cc/wvDn9J6Q/Screenshot-from-2023-07-04-16-56-27.png) · [Party entry and invoice references](https://i.postimg.cc/QCyQP4R4/Screenshot-from-2023-07-04-16-58-37.png)

## Proposed recording contract

| Step | Data and effect |
|---|---|
| Configure treasury | Authorize the manager for the company, resolve the main treasury account and the payable and receivable mappings for the selected payment mode and retain the setup revision used by each entry. |
| Record transaction | Accept treasury ID, posting date, amount, explicit currency, canonical direction, mode, party flag, optional party and instrument reference. The proposed contract requires a party for a party-based row and a cheque number for cheque mode. |
| Review and post | Resolve a balanced posting or a link to the core payment voucher according to company accounting policy. Store the posting identity and prevent a repeated submission from creating another voucher. An unposted register entry remains visibly distinguishable. |
| Inspect list | Filter by company, treasury, direction, date and party flag. Present receipt and payment totals separately before deriving net movement. Corrections reference the original entry. |

## Multilingual acceptance

A clerk using Afrikaans records a cash receipt of 250.00 against party C-44 and a non-party cash payment of 75.00 at the same treasury, date and currency. A German-speaking reviewer sees receipts of 250.00, payments of 75.00 and net movement of +175.00. Returning to the party-only filter leaves the receipt. Persist direction, mode and party IDs independently of words such as *ontvang* or *uitbetaling*.

In the proposed contract a party-based receipt without a party returns a localized field error and no posting. If a clerk changes the form language while entering cheque `000381`, the mode remains cheque and every digit survives. The printed payee or drawer text is kept as entered, with a separate recipient-language receipt caption.

**Qualification.** The screenshots and listing establish the setup instructions and user-facing classifications. The exact voucher generated, balancing rule, account mappings, reversal workflow and existing translation resources remain unverified. [Named repository](https://github.com/Brandimic0/erpnext_safe_entry)
