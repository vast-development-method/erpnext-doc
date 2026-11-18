# Picking for delivery, transfer and production

The [Picking for delivery, transfer and production](../../operations/picking.md) chapter defines the business rules, calculations and worked outcomes.

## Location and quantity decisions

- [Unit selection and availability](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/pick_list/pick_list.py#L127-L238)
- [Pending requirements and submission](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/pick_list/pick_list.py#L310-L413)
- [Cancellation and reservation release](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/pick_list/pick_list.py#L471-L502)
- [Location selection examples](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/pick_list/test_pick_list.py#L1048-L1089)

## Delivery generation and partial fulfilment

- [Grouping and eligibility](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/pick_list/pick_list.py#L1689-L1789)
- [Persisting group drafts](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/pick_list/pick_list.py#L1903-L1924)
- [Serial readback](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/pick_list/pick_list.py#L1977-L2060)
- [Transfer targets](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/pick_list/pick_list.py#L2128-L2160)
- [Remaining transfer quantity](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/pick_list/pick_list.py#L2371-L2392)
- [Order-level bundle calculation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/pick_list/pick_list.py#L913-L929)
- [Pending bundle calculation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/pick_list/pick_list.py#L1092-L1106)
- [Reference run](reference-run.json)
