# Insightly

## Publisher evidence

Meet Sherasiya lists versions 15 and 16. The customer dashboard groups Sales Orders, Delivery Notes, Payment Requests and Payment Entries by selected date range, counts and amounts, with drill-down by document type and customer. Its supplier counterpart covers Purchase Orders, Purchase Receipts, Purchase Invoices and Payment Entries, with supplier and date filters. The publisher describes identifying pending deliveries and payments; it gives no aging formula. These are internal sales and procurement dashboards. [Marketplace feature inventory](https://cloud.frappe.io/marketplace/apps/insightly) · [Listed source](https://github.com/MeetSherasiya/insightly)

## Pinned public copy

The copy's README directs installers to MeetSherasiya/insightly. At revision `46c2de000108db004279f16eff03087823ee5954` both controllers count submitted documents. Orders use transaction date, invoices and receipts/deliveries use posting date, and Payment Requests use creation timestamp. The customer controller additionally includes Sales Invoices, and the supplier controller includes Payment Requests. Invoice metrics sum both outstanding and grand total less outstanding. The aggregate queries shown group by party without currency separation. The rebuild below deliberately specifies currency grouping. This is a third-party copy and does not establish the publisher’s current release. [Origin in copy README](https://github.com/Beveren-Software-Inc/insightly/blob/46c2de000108db004279f16eff03087823ee5954/README.md#L17) · [Customer metrics](https://github.com/Beveren-Software-Inc/insightly/blob/46c2de000108db004279f16eff03087823ee5954/insightly/insightly/page/customer_insights/customer_insights.py#L35) · [Supplier metrics](https://github.com/Beveren-Software-Inc/insightly/blob/46c2de000108db004279f16eff03087823ee5954/insightly/insightly/page/supplier_insights/supplier_insights.py#L35)

## Proposed rebuild contract

A reader selects a company, party side, party and reporting period. Return one row per type, its count, amount buckets and a drill-down filter. Publish the type-specific date field, amount field, sign convention and eligible document states alongside the metric definition. For example, use submitted orders and their transaction dates for an ordered-value metric. An order, delivery and payment can describe the same sale. Present them as separate stages and do not sum their values into revenue.

Evaluate party, company and document permissions before aggregation and again for drill-down. Attribute a payment to its party and direction. If the implementation provides invoice allocation detail for payments, count each payment once at the payment level. Handle refunds and returns with the metric's published sign policy. Amounts use document currency buckets or an explicitly defined reporting-currency measure. A mixed-currency scalar without conversion evidence is invalid.

## Multilingual operation and acceptance

| Scenario | Observable outcome |
|---|---|
| A reader has access to two submitted orders for customer C17, worth EUR 100 and EUR 40, and one further order is a draft | The proposed submitted-order tile shows count 2 and EUR 140. Opening the tile returns those two order IDs under the very same filters. |
| An accountant switches from German to Afrikaans | Labels, date and decimal presentation change. The query still uses the original party and document-type IDs and yields the same order list. Customer-supplied names remain searchable in their original script. |
| A third permitted order is denominated in NAD and the reporting-currency option is unset | Count becomes 3. EUR and NAD appear as distinct amount buckets, each with its currency code. |
| A supplier user cannot read another supplier's receipt | Counts, charts and drill-downs exclude that receipt. A translated document-type label cannot broaden the filter. |

## Remaining evidence

Agreement of the shipped dashboards with the public copy, treatment of cancellations and returns, pagination, permission enforcement, installed translations and consistency under concurrent updates remain unverified. For parity, compare each tile and its drill-down against the same seeded transactions on a versioned installation.
