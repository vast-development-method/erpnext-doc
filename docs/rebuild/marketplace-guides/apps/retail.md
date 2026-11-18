# Retail Suite

[Business workflow and acceptance cases](../../../capabilities/guides/sales.md#retail-shift-settlement).

Ahmed's point-of-sale extension lists versions 15 and 16, with Nightly also shown on the detail page. The publisher explicitly describes Arabic and English interfaces, barcode scanning including on mobile, product search by serial or batch, offline operation, and cart modes for drafts, sales and returns. Checkout handles discounts and tax. A separate reconciliation screen matches payments to invoices. The cashier's shift dashboard brings together cash flow, sales and payments by method. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/retail) · [Publisher's v16 release description](https://www.linkedin.com/posts/ahmed-a-641a76251_retail-operations-arent-just-about-selling-activity-7473466240972394496-yYOy)

## Historical fork evidence

A public fork event on 17 May 2026 links the publisher repository to the Galaxlabs fork. Its inspected revision identifies the original publisher in the app metadata. Subsequent fork changes are possible. The observations below apply to this revision. [Fork metadata](https://github.com/galaxlabs/retail-suite/blob/3d5f92c3a4eabe74f15561e8f95ea5b2791973c4/retail/hooks.py)

* **Returns.** The return handler accepts an original Sales Invoice, item codes and positive quantities. It requires a submitted original, builds negative return lines at the original rate and recalculates tax and totals. If the original has payment rows, the handler uses its first payment method for the full refund. Split-tender refund allocation therefore needs explicit qualification. [Return handler](https://github.com/galaxlabs/retail-suite/blob/3d5f92c3a4eabe74f15561e8f95ea5b2791973c4/retail/retail/api/invoice.py#L210)
* **Shift close.** The closing record requires an open opening shift, checks for another submitted close for the same user and opening shift, and blocks closure with drafts unless the POS profile permits it. For each payment method it computes counted minus expected at the configured currency precision, falling back to three decimal places. [Closing controller](https://github.com/galaxlabs/retail-suite/blob/3d5f92c3a4eabe74f15561e8f95ea5b2791973c4/retail/retail/doctype/pos_closing_shift/pos_closing_shift.py#L14)
* **Translation.** The fork's POS page uses a language helper with English and Urdu dictionaries, including sale, tax, cart and shift actions. It reads the language from settings, defaults to English and resolves missing keys through English and then the key itself. Its toggle switches between English and Urdu. One shift-report date formatter specifies Egyptian Arabic independently. The advertised product's Arabic and English support comes from the publisher's description. The fork shows why that claim needs testing screen by screen against the intended release. [POS page](https://github.com/galaxlabs/retail-suite/blob/3d5f92c3a4eabe74f15561e8f95ea5b2791973c4/retail-suite/src/pages/POS.vue#L361) · [Language catalogs and selection](https://github.com/galaxlabs/retail-suite/blob/3d5f92c3a4eabe74f15561e8f95ea5b2791973c4/retail-suite/src/composables/i18n.js) · [Report date formatting](https://github.com/galaxlabs/retail-suite/blob/3d5f92c3a4eabe74f15561e8f95ea5b2791973c4/retail-suite/src/pages/Shifts/ShiftShow.vue#L628)

## Working through one shift

The publisher's closing screen shows opening, sales and expected amounts for payment methods, allows counted balances, and flags shortages. The screenshot uses a specific local currency. The rebuild must retain the shift's recorded currency and distinguish a shift count from allocation to an individual invoice. [Shift close screen](https://cloud.frappe.io/files/closing_shift.webp)

[Read the consolidated workflow](../../../capabilities/guides/sales.md#retail-shift-settlement-2).

## Multilingual acceptance

**Qualification.** The publisher release commit is unverified. Offline conflict arbitration, split-tender refunds, return authorization, locale coverage across receipts and analytics, and variance posting rules in that release remain open. [Named repository](https://github.com/AhmedAbokhatwa/retail-suite)

[Read the consolidated acceptance cases](../../../capabilities/guides/sales.md#retail-shift-settlement-3).
