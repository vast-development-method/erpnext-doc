# Customer order promises, delivery splits and pro forma invoices

The [Customer order promises, delivery splits and pro forma invoices](../../transactions/order-promises.md) chapter defines the business rules, calculations and worked outcomes.

- [row progress contract](../../domains/transaction-progress-and-row-closure.md)
- [customer relationships](../../domains/customer-relationships-and-sales.md)

## Set and resize delivery promises

- [Delivery schedule lifecycle](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/doctype/sales_order/sales_order.py#L1040-L1168)

## Map delivery and invoice independently

- [Delivery mapping](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/doctype/sales_order/sales_order.py#L1419-L1591)
- [Invoice mapper](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/doctype/sales_order/sales_order.py#L1594-L1826)
- [Return criteria](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/doctype/sales_order/sales_order.py#L2523-L2543)

## Issue a pro forma

- [Issue, validation and calculation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/doctype/proforma_invoice/proforma_invoice.py)
- [Upstream cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/doctype/proforma_invoice/test_proforma_invoice.py)
- [Operator guide](https://docs.frappe.io/erpnext/proforma-invoice)
