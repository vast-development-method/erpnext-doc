# Sanpra Easypay

Sanpra Software Solutions lists a version 15 connector for collections and disbursements through ICICI Bank. Its release announcement describes bulk supplier payouts from Payment Entries, OTP authorization, bank transaction logs, live status tracking and RTGS and NEFT support. The screenshot shows a Supplier Bank Payment document with a source account, a date filter, a Payment Entry retrieval action, detail rows and API Logs. The public material gives more detail for outbound payments than for collections. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/sanpra_easypay) · [Publisher announcement](https://www.linkedin.com/posts/sanpra-software-solution_frappe-icicibank-erpnext-activity-7321781697237114880-9_Sk) · [Supplier payment screen](https://cloud.frappe.io/files/image758cac.webp)

## Proposed bank connector contract

| Operation | Request and durable result |
|---|---|
| Prepare batch | The accounts operator selects organization, eligible source bank account, mode and open Payment Entries. Bind each instruction to its payee bank identifiers, reference, exact amount and currency. Freeze a digest of the batch submitted for approval. |
| Authorize and submit | A bank-authorized user completes the configured challenge. Send each instruction under a stable request identity. Audit the authorization outcome and timestamp without storing the OTP in logs. Editing beneficiary or amount invalidates the earlier approval. |
| Reconcile outcome | Keep bank acknowledgement, per-line status, bank reference and settlement evidence. A timeout leaves a line pending inquiry. Resolve that reference before any resend. One rejected instruction leaves other line outcomes intact. |
| Apply a collection | Correlate a bank-confirmed inward item to a receipt or an unmatched item awaiting review. Do not infer the payer's invoice purely from a similar localized name. |

## Multilingual acceptance

A clerk works in Hindi, an approver in English and the supplier wants German remittance advice. Approve a two-instruction batch. Feed one confirmed bank reference and one rejection. The first supplier gets one advice in its requested language, the second remains unpaid. A repeated bank status message creates no second advice or voucher. Numbers, references, bank codes, submitted beneficiary name and provider status remain traceable in their original form.

If approval expires after the user changes UI language, refuse submission and offer the localized reauthorization flow. If the bank status is unknown, distinguish “waiting for confirmation” from “failed” in every translation. Determine currency and rail eligibility from the bank agreement and account setup, independently of display language.

**Qualification.** Exact ICICI message formats, ownership of ledger posting, OTP delivery and validity rules, supported currencies, inbound matching fields and the current operational status of the integration require bank or vendor fixtures. No live payment was sent to test these proposed cases. [Named repository](https://github.com/Sanprasoftware/Sanpra-Easypay)
