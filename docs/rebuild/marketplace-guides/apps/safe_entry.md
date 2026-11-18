# Treasury Entry

[Business workflow and acceptance cases](../../../capabilities/guides/banking.md#treasury-transaction-register).

Brandimic describes a treasury register for receipts and payments made by cash or cheque. A System Manager or Accounts Manager configures a Treasury with a name, company, main treasury account and payment-mode account. On a Treasury Entry the operator selects that treasury, payment direction and mode, and indicates whether the transaction is party-based. Treasury List provides the transaction overview. The version selector lists 13 and 14. The publisher's narrative also mentions 12. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/safe_entry)

## What the publisher's forms show

On the setup form, each payment mode has **separate payable and receivable account fields**. The entry form also has a posting date and a numbering series. With the party checkbox clear, the clerk enters Treasury Item rows with an account and amount and sees a total. With the box selected, the form shows a party type, an action to retrieve outstanding invoices and a payment-reference table with document type, name, grand total, outstanding and allocated amounts. The screenshot labels those columns EGP for the illustrated setup. It shows the allocation inputs on an unsaved document, with no posted result or voucher. [Treasury setup](https://i.postimg.cc/L6P2nqNw/Screenshot-from-2023-07-04-16-53-04.png) · [Entry without a party](https://i.postimg.cc/wvDn9J6Q/Screenshot-from-2023-07-04-16-56-27.png) · [Party entry and invoice references](https://i.postimg.cc/QCyQP4R4/Screenshot-from-2023-07-04-16-58-37.png)

## Proposed recording contract

[Read the consolidated workflow](../../../capabilities/guides/banking.md#treasury-transaction-register-2).

## Multilingual acceptance

**Qualification.** The screenshots and listing establish the setup instructions and user-facing classifications. The exact voucher generated, balancing rule, account mappings, reversal workflow and existing translation resources remain unverified. [Named repository](https://github.com/Brandimic0/erpnext_safe_entry)

[Read the consolidated acceptance cases](../../../capabilities/guides/banking.md#treasury-transaction-register-3).
