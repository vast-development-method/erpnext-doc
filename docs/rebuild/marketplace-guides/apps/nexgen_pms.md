# EstateFlow

[Business workflow and acceptance cases](../../../capabilities/guides/operations.md#rent-collection-and-reminders).

NexGen Enterprises describes property, unit and lease management for versions 15 and 16. Properties can have towers, sectors, floors, amenities, images and documents. Units carry availability, booking or sale status. Maintenance requests link the property, unit and tenant and move from open through in progress to closed. Lease records support agreement printing, identification documents and an expiry notice 15 days before the end date. Company, Customer, Address, Sales Person and Employee are named integration points. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/nexgen_pms)

The rent dashboard draws from active leases and linked Sales Invoices. An operator can generate invoices or reminders in bulk, start a Payment Entry against a rent invoice and see invoiced, paid and outstanding totals. Reminder templates take tenant name, amount and due date. The described WhatsApp flow validates the phone number and opens a prefilled click-to-chat link on the operator's device. Opening the link establishes no delivery receipt. [Publisher's collection and communication description](https://cloud.frappe.io/marketplace/apps/nexgen_pms)

## Proposed rebuild contract

Public evidence does not establish renewal/amendment rules, due-date ageing bands, automatic posting, supported message languages or delivery tracking. The source named by the publisher remains unpinned. [Named app repository](https://github.com/nexgenerptechnologies/nexgen_pms) · [Core Payment Entry](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/payment_entry/payment_entry.json)

[Read the consolidated workflow](../../../capabilities/guides/operations.md#rent-collection-and-reminders-1).
