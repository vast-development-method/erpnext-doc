# Consume substitutes, cost the output and recover material

The [Consume substitutes, cost the output and recover material](../../operations/material-cost-and-recovery.md) chapter defines the business rules, calculations and worked outcomes.

## Release material to a work order

- [Alternative master](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/item_alternative/item_alternative.py)
- [Authority and WIP provenance](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_entry/stock_entry.py#L1317-L1469)
- [Quantity splitter](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_entry/stock_entry.py#L5597-L5627)

## Determine the basis for output cost

- [Cost selection](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_entry/stock_entry.py#L2159-L2394)
- [Loss rollup](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/work_order/work_order.py#L1096-L1133)
- [Source fixtures](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_entry/test_stock_entry.py)

## A movement and accounting trace

- [Disassembly validation and cumulative quantities](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_entry/stock_entry.py#L1469-L1679)
- [Source availability and read access](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/work_order/work_order.py#L3540-L3560)

## Corrective jobs and equipment repairs

- [Repair lifecycle and GL](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/doctype/asset_repair/asset_repair.py)
- [Repair acceptance](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/doctype/asset_repair/test_asset_repair.py)
