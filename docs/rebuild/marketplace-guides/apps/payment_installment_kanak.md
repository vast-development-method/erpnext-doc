# Payment Installments

[Business workflow and acceptance cases](../../../capabilities/guides/accounting.md#sales-order-advance-and-instalment-invoicing).

Kanak Infosystems lists version 15. A sales operator attaches a Payment Term Template to a Sales Order, chooses the first installment date and optionally adds a charge such as freight. On submission, the app generates the schedule and immediately creates a down-payment invoice containing the charges. A scheduler creates a separate invoice for each installment two days before its due date. The publisher describes extra charges as separate from the sales base. Its marketplace wording says an installment is marked paid on invoice creation. The storefront confirms invoice creation but supplies no evidence of a corresponding receipt or Payment Entry. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/payment_installment_kanak) · [Publisher's versioned guide](https://www.kanakinfosystems.com/frappe/apps/15.0/payment_installment_kanak)

## Proposed rebuild contract

Core ERP defines a Payment Schedule child record. The add-on's additional schedule rows, month-end convention, charge tax treatment, cancellation route and interpretation of its paid flag require the publisher's build or a transaction trace. [Core schedule](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/payment_schedule/payment_schedule.json) · [Named app repository](https://github.com/kanakinfo/payment_installment_kanak)

[Read the consolidated workflow](../../../capabilities/guides/accounting.md#sales-order-advance-and-instalment-invoicing-1).
