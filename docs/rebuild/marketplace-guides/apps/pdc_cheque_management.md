# PDC Cheque Management

[Business workflow and acceptance cases](../../../capabilities/guides/banking.md#post-dated-cheque-settlement).

A post-dated cheque can settle an invoice before money reaches the bank. The application models the interval for both customer receipts and instruments issued to suppliers. Virendra Maurya lists versions 15 and 16. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/pdc_cheque_management) · [NexGen release announcement](https://www.linkedin.com/posts/nexgen-enterprises-erp_erpnext-frappeframework-pdcmanagement-activity-7474689635479207937-F_lh)

## Published workflow

Party type selects a configurable interim account for incoming or outgoing instruments. Receiving or issuing a cheque creates a Payment Entry with accounts and invoice allocations selected for that direction. The publisher describes party-account currency detection, historical rates and exchange gain/loss handling. Staff can filter a clearance batch by date, bank or status, then deposit or clear selected cheques. The published statuses also include draft, cancelled and bounced. A bounce carries a date and reason. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/pdc_cheque_management)

## Attributed public copy

A separately maintained copy identifies NexGen as author and gives the exact marketplace repository in its manifest. In that copy, receipt and issue require invoice rows, submit a Payment Entry and retain its ID. Deposit creates a Bank Entry journal debiting the bank and crediting the holding account. Clearance then stamps that journal with the clearing date, which cannot precede the cheque date. Bounce handling first attempts to cancel the deposit journal and the Payment Entry. A positive bank charge can produce a further expense debit and bank credit. The deposit method uses the same two legs regardless of direction, so a supplier-issued instrument must be qualified separately. The Payment Entry code requests a rate without an explicit historical date. These are inspectable differences worth testing against the publisher's description. [Copy provenance](https://github.com/thinknxg/PDC-Cheque-Management/blob/4aaf803398c3009addec21be809136e47ae02a35/pyproject.toml) · [Cheque controller](https://github.com/thinknxg/PDC-Cheque-Management/blob/4aaf803398c3009addec21be809136e47ae02a35/pdc_cheque_management/pdc_banking_automation/doctype/pdc_cheque/pdc_cheque.py)

## Proposed rebuild contract

[Read the consolidated workflow](../../../capabilities/guides/banking.md#post-dated-cheque-settlement-3).

## Multilingual acceptance

**Qualification.** The exact posting date and rate choices, partial allocations, bounce reversal sequence and atomicity of the publisher's batch tool require an inspectable release or an observed voucher trace. The journal entries above specify the replacement example. [Named repository](https://github.com/nexgenerptechnologies/PDC-Cheque-Management)

[Read the consolidated acceptance cases](../../../capabilities/guides/banking.md#post-dated-cheque-settlement-4).
