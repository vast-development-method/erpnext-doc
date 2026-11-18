# Advance Authorisation Licence

Finbyz Tech Pvt Ltd links import and export invoice lines to the authorisation under which a manufacturer imports inputs for an export product. The publisher lists versions 14 and 15. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/advance_authorisation_licence) · [Publisher’s worked procedure](https://erp.finbyz.tech/erpnext/apps/advanced-authorisation-licence-erpnext)

## Documented workflow

A licence records the reference, application file number and date, validity dates, currency, export item, approved export quantity and value, and licence amount. The input table identifies each declared import item and its ratio to the export item. The publisher gives a ratio range of 0.01 through 1. On import, the operator selects a licence on the Purchase Invoice line and records CIF and FOB values. Submission consumes the item allowance. An insufficient amount or quantity prevents submission. On export, the operator selects the licence on the Sales Invoice line and provides freight and insurance in invoice currency to determine the FOB value. Export utilisation and its remaining commitment are tracked separately. An upper variation setting accommodates agreed excess export performance. [Import and export procedure](https://cloud.frappe.io/marketplace/apps/advance_authorisation_licence)

## Proposed rebuild contract

Maintain a movement per company, licence, direction, item and originating invoice line. Store the quantity with its unit and the assessed value with its currency. If invoice and authorisation currencies differ, persist the approved conversion basis before testing a value ceiling. Make the remaining quantity and value reproducible from approved limits and posted movements. Retain the licence and corresponding movements when an invoice is cancelled, recording a reversing movement only once. The calculated balance must survive two buyers posting for the same licence concurrently.

| Operation | Input and observable result |
|---|---|
| Assess utilisation | Return quantity available, value available, requested amounts and the first exceeded limit for each line. No posting. |
| Apply invoice | Reassess all lines against the same locked/versioned balance. Commit the invoice references and movements together. |
| Show utilisation | Present the separate import allowances and export commitment with drill-down to the invoice line and any reversal. |

## Language and acceptance

Localise “amount remaining”, “export commitment” and the maximum-available error with separate message keys. Preserve licence numbers, file numbers and externally assigned item codes exactly. An English-language invoice and a Hindi-language licence report must select the same licence ID, currency and ratio.

- **Within both limits.** An import allowance has 80 kg and 700 units of licence currency available. Posting 30 kg assessed at 250 leaves 50 kg and 450. A replay of the same committed line retains both balances.
- **Independent limits.** From 50 kg and 450 remaining, an invoice for 40 kg assessed at 451 fails the value check. Neither balance moves. An export transaction against the same licence must leave the import movements intact.

The evidence describes application behaviour. The exact valuation basis, tolerance formula, conversion-date policy and treatment of amendments require a publisher example or a running installation. [Publisher-named repository](https://github.com/finbyz/advance_authorisation_licence)
