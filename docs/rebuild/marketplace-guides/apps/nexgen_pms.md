# EstateFlow

NexGen Enterprises describes property, unit and lease management for versions 15 and 16. Properties can have towers, sectors, floors, amenities, images and documents. Units carry availability, booking or sale status. Maintenance requests link the property, unit and tenant and move from open through in progress to closed. Lease records support agreement printing, identification documents and an expiry notice 15 days before the end date. Company, Customer, Address, Sales Person and Employee are named integration points. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/nexgen_pms)

The rent dashboard draws from active leases and linked Sales Invoices. An operator can generate invoices or reminders in bulk, start a Payment Entry against a rent invoice and see invoiced, paid and outstanding totals. Reminder templates take tenant name, amount and due date. The described WhatsApp flow validates the phone number and opens a prefilled click-to-chat link on the operator's device. Opening the link establishes no delivery receipt. [Publisher's collection and communication description](https://cloud.frappe.io/marketplace/apps/nexgen_pms)

## Proposed rebuild contract

Use separate immutable keys for property, unit, tenant, lease, charge period, invoice and allocation. Generate rent for an active lease by charge period and retain the invoice reference on rerun. Compute unpaid amounts from invoice allocations, credit adjustments and reversals. Prevent a cash-entry shortcut from marking a rent invoice settled until the payment is posted and allocated. Separate arrears ageing from lease expiry and maintenance status. Record the operator, time, target and individual result of each bulk action.

Resolve dashboard text in the operator's language and reminders in the tenant's preferred language. Validate every required placeholder against the message template revision. Preserve tenant names, unit identifiers, dates, amounts and currency codes across renderings. A sent agreement should retain its signed language and revision. A translation of legal terms is a separately approved document version. Provide a text label for every coloured payment status.

| Proposed acceptance case | Expected result |
|---|---|
| A lease has one 900 invoice and a posted payment allocated for 350 in the invoice currency. A German-speaking manager prepares an Afrikaans reminder. | The outstanding amount is 550, in both views. The reminder uses the tenant's language. Opening WhatsApp records a handoff to the operator and creates no second payment or invoice. |
| Generate rent twice for the same unit, lease and period while one tenant in the bulk list has an invalid phone. | One invoice exists per eligible charge. The invalid contact receives an individual failure and no chat link. Other eligible tenants remain processable. |
| On the site-local expiry notification date, an open maintenance ticket exists for the same unit. | One expiry notice is associated with that lease and date. The ticket retains its own state and assignment. |

Public evidence does not establish renewal/amendment rules, due-date ageing bands, automatic posting, supported message languages or delivery tracking. The source named by the publisher remains unpinned. [Named app repository](https://github.com/nexgenerptechnologies/nexgen_pms) · [Core Payment Entry](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/payment_entry/payment_entry.json)
