# Count adjustments and stock closing

The [Count adjustments and stock closing](../../operations/inventory-control.md) chapter defines the business rules, calculations and worked outcomes.

## Count stock as of the posting instant

- [Reconciliation decisions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_reconciliation/stock_reconciliation.py)
- [Upstream cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_reconciliation/test_stock_reconciliation.py)
- [Operator guide](https://docs.frappe.io/erpnext/stock-reconciliation)

## Correct valuation layers from a comparison

- [Valuation adjustment](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/valuation_adjustment.py)

## Publish a closing balance

- [Closing lifecycle and calculation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_closing_entry/stock_closing_entry.py)
- [Concurrency and batch cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_closing_entry/test_stock_closing_entry.py)
- [Operator guide](https://docs.frappe.io/erpnext/stock-closing-entry)
