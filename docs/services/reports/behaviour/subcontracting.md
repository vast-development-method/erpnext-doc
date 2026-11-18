# Subcontracting reports

The [structured report details](subcontracting.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Subcontracted Items To Be Delivered

Script Report. The reference record is Subcontracting Inward Order.

The direct return positions are get columns / get data. Named output fields constructed in this report include `item_code`, `item_name`, `stock_uom`, `qty`, `produced_qty`, `delivered_qty`, `pending_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/subcontracting/report/subcontracted_items_to_be_delivered/subcontracted_items_to_be_delivered.py#L9) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/subcontracting/report/subcontracted_items_to_be_delivered/subcontracted_items_to_be_delivered.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/subcontracting/operations-001.md#op-0e64a6a0989951)

## Subcontracted Raw Materials To Be Received

Script Report. The reference record is Subcontracting Inward Order.

The direct return positions are get columns / get data. Named output fields constructed in this report include `main_item_code`, `rm_item_code`, `stock_uom`, `required_qty`, `received_qty`, `returned_qty`, `process_loss_qty`, `pending_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/subcontracting/report/subcontracted_raw_materials_to_be_received/subcontracted_raw_materials_to_be_received.py#L9) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/subcontracting/report/subcontracted_raw_materials_to_be_received/subcontracted_raw_materials_to_be_received.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/subcontracting/operations-001.md#op-07d066dd741325)

## Subcontracting Inward Order Summary

Script Report. The reference record is Subcontracting Inward Order. Declared inputs include `subcontracting_inward_order`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `status`, `item_code`, `stock_uom`, `qty`, `produced_qty`, `delivered_qty`, `returned_qty`, `rm_item_code`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/subcontracting/report/subcontracting_inward_order_summary/subcontracting_inward_order_summary.py#L8) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/subcontracting/report/subcontracting_inward_order_summary/subcontracting_inward_order_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/subcontracting/operations-003.md#op-f6755d9c25b52e)
