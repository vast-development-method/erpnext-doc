# Procurement reports

The [structured report details](procurement.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Item Wise Purchase History

Script Report. The reference record is Purchase Order. Declared inputs include `company`, `from_date`, `to_date`, `item_group`, `item_code`, `supplier`.

The direct return positions are columns / data / absent / chart data. Named output fields constructed in this report include `item_code`, `item_name`, `item_group`, `description`, `quantity`, `uom`, `rate`, `amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/item_wise_purchase_history/item_wise_purchase_history.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/item_wise_purchase_history/item_wise_purchase_history.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/buying/operations-001.md#op-09f38ba63046b7)

## Procurement Tracker

Script Report. The reference record is Purchase Order. Declared inputs include `company`, `cost_center`, `project`, `from_date`, `to_date`, `show_completed_orders`.

The direct return positions are columns / data. Named output fields constructed in this report include `material_request_date`, `material_request_no`, `cost_center`, `project`, `requesting_site`, `requestor`, `item_code`, `quantity`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/procurement_tracker/procurement_tracker.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/procurement_tracker/procurement_tracker.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/buying/operations-001.md#op-ea880d36e17ee4)

## Purchase Analytics

Script Report. The reference record is Purchase Order. Declared inputs include `tree_type`, `entity`, `doc_type`, `value_quantity`, `from_date`, `to_date`, `company`, `range`, `curves`, `show_aggregate_value_from_subsidiary_companies`.

The report returns the result of `Analytics.run`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/purchase_analytics/purchase_analytics.py#L9) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/purchase_analytics/purchase_analytics.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/buying/operations-002.md#op-4b80862c2b0019)

## Purchase Order Analysis

Script Report. The reference record is Purchase Order. Declared inputs include `company`, `from_date`, `to_date`, `project`, `name`, `status`, `group_by_po`, `group_by_item`.

Named output fields constructed in this report include `date`, `required_date`, `purchase_order`, `status`, `supplier`, `project`, `item_code`, `uom`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/purchase_order_analysis/purchase_order_analysis.py#L18) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/purchase_order_analysis/purchase_order_analysis.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/buying/operations-004.md#op-55847e05911c28)

## Purchase Order Trends

Script Report. The reference record is Purchase Order. Declared inputs include `include_closed_orders`.

The linked row procedure owns the output; inspect its conditional returns and result builders for the selected filters. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/purchase_order_trends/purchase_order_trends.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/purchase_order_trends/purchase_order_trends.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/buying/operations-005.md#op-c163244e67514f)

## Requested Items To Order And Receive

Script Report. The reference record is Material Request. Declared inputs include `company`, `from_date`, `to_date`, `material_request`, `item_code`, `group_by_mr`.

Named output fields constructed in this report include `material_request`, `date`, `required_date`, `item_code`, `item_name`, `description`, `uom`, `stock_uom`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/requested_items_to_order_and_receive/requested_items_to_order_and_receive.py#L15) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/requested_items_to_order_and_receive/requested_items_to_order_and_receive.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/buying/operations-007.md#op-becd3033fefcf9)

## Subcontract Order Summary

Script Report. The reference record is Subcontracting Order. Declared inputs include `company`, `from_date`, `to_date`, `order_type`, `name`.

The direct return positions are columns / data. Named output fields constructed in this report include `order_id`, `supplier`, `status`, `item_code`, `qty`, `received_qty`, `rm_item_code`, `required_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/subcontract_order_summary/subcontract_order_summary.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/subcontract_order_summary/subcontract_order_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/buying/operations-007.md#op-462627f019add9)

## Subcontracted Item To Be Received

Script Report. The reference record is Subcontracting Order. Declared inputs include `order_type`, `supplier`, `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `subcontract_order`, `date`, `supplier`, `fg_item_code`, `item_name`, `required_qty`, `received_qty`, `pending_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/subcontracted_item_to_be_received/subcontracted_item_to_be_received.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/subcontracted_item_to_be_received/subcontracted_item_to_be_received.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/buying/operations-007.md#op-e860273111ea65)

## Subcontracted Raw Materials To Be Transferred

Script Report. The reference record is Subcontracting Order. Declared inputs include `order_type`, `supplier`, `from_date`, `to_date`.

Named output fields constructed in this report include `subcontract_order`, `date`, `supplier`, `rm_item_code`, `reqd_qty`, `transferred_qty`, `returned_qty`, `p_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/subcontracted_raw_materials_to_be_transferred/subcontracted_raw_materials_to_be_transferred.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/subcontracted_raw_materials_to_be_transferred/subcontracted_raw_materials_to_be_transferred.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/buying/operations-008.md#op-afff51e3b24e5e)

## Supplier Quotation Comparison

Script Report. The reference record is Supplier Quotation. Declared inputs include `company`, `from_date`, `to_date`, `item_code`, `supplier`, `supplier_quotation`, `request_for_quotation`, `categorize_by`, `status`, `order_status`, `include_expired`.

Named output fields constructed in this report include `supplier_name`, `item_code`, `uom`, `qty`, `stock_uom`, `currency`, `price`, `price_per_unit`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/supplier_quotation_comparison/supplier_quotation_comparison.py#L15) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/report/supplier_quotation_comparison/supplier_quotation_comparison.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/buying/operations-011.md#op-6154c4c1e66b78)
