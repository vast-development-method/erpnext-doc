# Advance Authorisation Licence

[Business workflow and acceptance cases](../../../capabilities/guides/supply.md#import-and-export-licence-balances).

Finbyz Tech Pvt Ltd links import and export invoice lines to the authorisation under which a manufacturer imports inputs for an export product. The publisher lists versions 14 and 15. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/advance_authorisation_licence) · [Publisher’s worked procedure](https://erp.finbyz.tech/erpnext/apps/advanced-authorisation-licence-erpnext)

## Documented workflow

A licence records the reference, application file number and date, validity dates, currency, export item, approved export quantity and value, and licence amount. The input table identifies each declared import item and its ratio to the export item. The publisher gives a ratio range of 0.01 through 1. On import, the operator selects a licence on the Purchase Invoice line and records CIF and FOB values. Submission consumes the item allowance. An insufficient amount or quantity prevents submission. On export, the operator selects the licence on the Sales Invoice line and provides freight and insurance in invoice currency to determine the FOB value. Export utilisation and its remaining commitment are tracked separately. An upper variation setting accommodates agreed excess export performance. [Import and export procedure](https://cloud.frappe.io/marketplace/apps/advance_authorisation_licence)

## Proposed rebuild contract

[Read the consolidated workflow](../../../capabilities/guides/supply.md#import-and-export-licence-balances-2).

## Language and acceptance

The evidence describes application behaviour. The exact valuation basis, tolerance formula, conversion-date policy and treatment of amendments require a publisher example or a running installation. [Publisher-named repository](https://github.com/finbyz/advance_authorisation_licence)

[Read the consolidated acceptance cases](../../../capabilities/guides/supply.md#import-and-export-licence-balances-3).
