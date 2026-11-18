# Purchase tax and stock acquisition cost

The [Purchase tax and stock acquisition cost](../../../transactions/purchase-tax-and-stock.md) chapter defines the business rules, calculations and worked outcomes.

- [Purchase invoice tax posting](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/purchase_invoice/purchase_invoice.py#L1749-L1846)
- [Total-stage signing](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/taxes_and_totals.py#L716-L738)
- [Stock valuation formula](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/buying_controller.py#L711-L798)

## Which rows carry the charge?

- [Valuation row allocation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/buying_controller.py#L816-L992)
- [Mixed-item receipt assertions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py#L2052-L2189)
- [Independent charge rounding](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py#L2275-L2347)
- [Rejected warehouse](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py#L9242-L9288)
- [Return attribution](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py#L3849-L3896)
