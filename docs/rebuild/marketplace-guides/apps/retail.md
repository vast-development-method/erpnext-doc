# Retail Suite

Ahmed's point-of-sale extension lists versions 15 and 16, with Nightly also shown on the detail page. The publisher explicitly describes Arabic and English interfaces, barcode scanning including on mobile, product search by serial or batch, offline operation, and cart modes for drafts, sales and returns. Checkout handles discounts and tax. A separate reconciliation screen matches payments to invoices. The cashier's shift dashboard brings together cash flow, sales and payments by method. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/retail) · [Publisher's v16 release description](https://www.linkedin.com/posts/ahmed-a-641a76251_retail-operations-arent-just-about-selling-activity-7473466240972394496-yYOy)

## Working through one shift

The publisher's closing screen shows opening, sales and expected amounts for payment methods, allows counted balances, and flags shortages. The screenshot uses a specific local currency. The rebuild must retain the shift's recorded currency and distinguish a shift count from allocation to an individual invoice. [Shift close screen](https://cloud.frappe.io/files/closing_shift.webp)

| Proposed operation | Contract and state |
|---|---|
| Open shift | Bind cashier, terminal, POS profile, company, warehouse, operating currency, opening time and opening amount per tender. Return a stable shift ID. |
| Build cart | A scan identifies a product and where relevant its serial or batch. Store item ID, quantity, unit, price and tax configuration on the line. A draft can be resumed across language changes. |
| Complete sale or return | Validate tracked inventory, prices and tender totals on the authoritative service. Use a durable sale key for offline submissions. Link returns to sold lines and enforce the remaining returnable quantity. Return the committed invoice and payment IDs. |
| Close shift | Require outstanding offline submissions to be resolved or explicitly carried forward. Compare expected with counted per tender and record differences separately. Handle overages and shortages with an authorized explanation. |

## Multilingual acceptance

A cashier scans a serial-labelled item under an Arabic interface and saves a draft. An authorized English-speaking operator resumes it and sees the identical serial, warehouse, tax and quantity. A receipt can use the customer's language. Keep serials and barcodes in their original character order when embedded in right-to-left text.

For a synthetic shift, open cash with 100.00, receive 200.00 cash and 50.00 card, and refund 30.00 cash. Expected cash is 270.00 and expected card movement is 50.00. Counts of 268.00 and 50.00 yield a 2.00 cash shortage. Both UI languages show the same discrepancy and original transactions. Replaying an already acknowledged offline sale produces one invoice. A request for a serial already sold on another terminal requires review.

**Qualification.** Published material leaves offline conflict arbitration, exact voucher classes, return authorization, locale coverage across receipts and analytics, and variance posting rules open. [Named repository](https://github.com/AhmedAbokhatwa/retail-suite)
