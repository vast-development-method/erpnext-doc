# Sanpra Easypay

[Business workflow and acceptance cases](../../../capabilities/guides/banking.md#supplier-payment-batch-authorization).

Sanpra Software Solutions lists a version 15 connector for collections and disbursements through ICICI Bank. Its release announcement describes bulk supplier payouts from Payment Entries, OTP authorization, bank transaction logs, live status tracking and RTGS and NEFT support. The screenshot shows a Supplier Bank Payment document with a source account, a date filter, a Payment Entry retrieval action, detail rows and API Logs. The public material gives more detail for outbound payments than for collections. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/sanpra_easypay) · [Publisher announcement](https://www.linkedin.com/posts/sanpra-software-solution_frappe-icicibank-erpnext-activity-7321781697237114880-9_Sk) · [Supplier payment screen](https://cloud.frappe.io/files/image758cac.webp)

## Proposed bank connector contract

[Read the consolidated workflow](../../../capabilities/guides/banking.md#supplier-payment-batch-authorization-1).

## Multilingual acceptance

**Qualification.** Exact ICICI message formats, ownership of ledger posting, OTP delivery and validity rules, supported currencies, inbound matching fields and the current operational status of the integration require bank or vendor fixtures. No live payment was sent to test these proposed cases. [Named repository](https://github.com/Sanprasoftware/Sanpra-Easypay)

[Read the consolidated acceptance cases](../../../capabilities/guides/banking.md#supplier-payment-batch-authorization-2).
