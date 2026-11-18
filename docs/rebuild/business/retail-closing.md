# Retail session, tender reconciliation and consolidated posting

The [Retail session, tender reconciliation and consolidated posting](../../transactions/retail-closing.md) chapter defines the business rules, calculations and worked outcomes.

## Opening and membership

- [Opening rules](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/pos_opening_entry/pos_opening_entry.py)
- [Closing selector and validation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/pos_closing_entry/pos_closing_entry.py)

## Count cash and explain differences

- [Tender selection](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/pos_closing_entry/pos_closing_entry.py#L316-L473)
- [Interactive count](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/pos_closing_entry/pos_closing_entry.js#L62-L159)

## Close, reverse and retry

- [Consolidation, cancellation and batch threshold](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/pos_invoice_merge_log/pos_invoice_merge_log.py#L531-L760)
- [Sales and returns](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/pos_invoice_merge_log/pos_invoice_merge_log.py#L142-L235)
- [Operator guide](https://docs.frappe.io/erpnext/pos-workflows)
