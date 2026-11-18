# PDC Cheque Management

A post-dated cheque can settle an invoice before money reaches the bank. The application models the interval for both customer receipts and instruments issued to suppliers. Virendra Maurya lists versions 15 and 16. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/pdc_cheque_management) · [NexGen release announcement](https://www.linkedin.com/posts/nexgen-enterprises-erp_erpnext-frappeframework-pdcmanagement-activity-7474689635479207937-F_lh)

## Published workflow

Party type selects a configurable interim account for incoming or outgoing instruments. Receiving or issuing a cheque creates a Payment Entry with accounts and invoice allocations selected for that direction. The publisher describes party-account currency detection, historical rates and exchange gain/loss handling. Staff can filter a clearance batch by date, bank or status, then deposit or clear selected cheques. The published statuses also include draft, cancelled and bounced. A bounce carries a date and reason. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/pdc_cheque_management)

## Attributed public copy

A separately maintained copy identifies NexGen as author and gives the exact marketplace repository in its manifest. In that copy, receipt and issue require invoice rows, submit a Payment Entry and retain its ID. Deposit creates a Bank Entry journal debiting the bank and crediting the holding account. Clearance then stamps that journal with the clearing date, which cannot precede the cheque date. Bounce handling first attempts to cancel the deposit journal and the Payment Entry. A positive bank charge can produce a further expense debit and bank credit. The deposit method uses the same two legs regardless of direction, so a supplier-issued instrument must be qualified separately. The Payment Entry code requests a rate without an explicit historical date. These are inspectable differences worth testing against the publisher's description. [Copy provenance](https://github.com/thinknxg/PDC-Cheque-Management/blob/4aaf803398c3009addec21be809136e47ae02a35/pyproject.toml) · [Cheque controller](https://github.com/thinknxg/PDC-Cheque-Management/blob/4aaf803398c3009addec21be809136e47ae02a35/pdc_cheque_management/pdc_banking_automation/doctype/pdc_cheque/pdc_cheque.py)

## Proposed rebuild contract

Store company, instrument ID, printed number, bank, direction, party, cheque date, amount and currency, invoice allocations, interim account, source voucher and transition history. Preserve the printed cheque number as text. Keep the instrument date, accounting date and clearing date distinct. Authorize entry and clearance against the owning company. Each clearance batch returns the result per instrument so an operator can resolve a failure without re-clearing successful rows.

| Operation | Required decision and effect |
|---|---|
| Record receipt or issue | Resolve the company holding account and party account. Persist the instrument and allocation voucher together under one request key. |
| Deposit and clear | For a customer receipt held in an asset account, deposit transfers the amount from the holding account to the bank. Clearance marks that bank movement as confirmed. For a supplier issue, resolve the payable-side holding configuration. Record the bank evidence and voucher identity. |
| Record a bounce | Require a date, reason and original voucher. Reverse the applicable movement and reopen affected allocations using the core settlement service. Link corrective vouchers to the original. |

## Multilingual acceptance

1. An Afrikaans-speaking clerk records cheque `00072` for a customer with an open 400.00 invoice in the same currency. Under the proposed receipt configuration the voucher debits the holding account 400.00 and credits the customer 400.00. A German-speaking reviewer deposits and then clears it. The bank increases by 400.00, the holding account returns to zero and the original voucher and instrument IDs agree in both views.
2. Submit clearance twice with the same bank reference and request key. Both responses identify the same posting. A subsequent conflicting amount routes to review. Translate these two outcomes separately.
3. Preserve a bank's original bounce reason, such as `Signature diffère`, and show a translated classification alongside it. A language change leaves exchange rates, transaction currency, cheque date and ledger mappings intact.

**Qualification.** The exact posting date and rate choices, partial allocations, bounce reversal sequence and atomicity of the publisher's batch tool require an inspectable release or an observed voucher trace. The journal entries above specify the replacement example. [Named repository](https://github.com/nexgenerptechnologies/PDC-Cheque-Management)
