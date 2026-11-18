# Insightly

[Business workflow and acceptance cases](../../../capabilities/guides/sales.md#party-order-dashboard).

## Publisher evidence

Meet Sherasiya lists versions 15 and 16. The customer dashboard groups Sales Orders, Delivery Notes, Payment Requests and Payment Entries by selected date range, counts and amounts, with drill-down by document type and customer. Its supplier counterpart covers Purchase Orders, Purchase Receipts, Purchase Invoices and Payment Entries, with supplier and date filters. The publisher describes identifying pending deliveries and payments; it gives no aging formula. These are internal sales and procurement dashboards. [Marketplace feature inventory](https://cloud.frappe.io/marketplace/apps/insightly) · [Listed source](https://github.com/MeetSherasiya/insightly)

## Pinned public copy

The copy's README directs installers to MeetSherasiya/insightly. At revision `46c2de000108db004279f16eff03087823ee5954` both controllers count submitted documents. Orders use transaction date, invoices and receipts/deliveries use posting date, and Payment Requests use creation timestamp. The customer controller additionally includes Sales Invoices, and the supplier controller includes Payment Requests. Invoice metrics sum both outstanding and grand total less outstanding. The aggregate queries shown group by party without currency separation. The rebuild below deliberately specifies currency grouping. This is a third-party copy and does not establish the publisher’s current release. [Origin in copy README](https://github.com/Beveren-Software-Inc/insightly/blob/46c2de000108db004279f16eff03087823ee5954/README.md#L17) · [Customer metrics](https://github.com/Beveren-Software-Inc/insightly/blob/46c2de000108db004279f16eff03087823ee5954/insightly/insightly/page/customer_insights/customer_insights.py#L35) · [Supplier metrics](https://github.com/Beveren-Software-Inc/insightly/blob/46c2de000108db004279f16eff03087823ee5954/insightly/insightly/page/supplier_insights/supplier_insights.py#L35)

## Proposed rebuild contract

[Read the consolidated workflow](../../../capabilities/guides/sales.md#party-order-dashboard).

## Multilingual operation and acceptance

[Read the consolidated acceptance cases](../../../capabilities/guides/sales.md#party-order-dashboard-4).

## Remaining evidence

Agreement of the shipped dashboards with the public copy, treatment of cancellations and returns, pagination, permission enforcement, installed translations and consistency under concurrent updates remain unverified. For parity, compare each tile and its drill-down against the same seeded transactions on a versioned installation.
