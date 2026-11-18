# Inventory reports

The [structured report details](inventory.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Available Batch Report

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `to_date`, `item_code`, `warehouse`, `warehouse_type`, `batch_no`, `include_expired_batches`, `show_item_name`.

The direct return positions are columns / data. Named output fields constructed in this report include `item_code`, `item_name`, `warehouse`, `batch_no`, `expiry_date`, `balance_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/available_batch_report/available_batch_report.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/available_batch_report/available_batch_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-001.md#op-095586dd11f463)

## Available Serial Number

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `from_date`, `to_date`, `warehouse`, `item_code`, `voucher_no`, `valuation_field_type`.

Named output fields constructed in this report include `date`, `item_code`, `item_name`, `stock_uom`, `in_qty`, `out_qty`, `qty_after_transaction`, `warehouse`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/available_serial_no/available_serial_no.py#L21) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/available_serial_no/available_serial_no.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-001.md#op-dedd130cd77951)

## Batch Item Expiry Status

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `from_date`, `to_date`, `item`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/batch_item_expiry_status/batch_item_expiry_status.py#L18) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/batch_item_expiry_status/batch_item_expiry_status.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-002.md#op-ebfd5580bc98e6)

## Batch Wise Balance History

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `from_date`, `to_date`, `item_code`, `warehouse_type`, `warehouse`, `batch_no`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/batch_wise_balance_history/batch_wise_balance_history.py#L21) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/batch_wise_balance_history/batch_wise_balance_history.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-003.md#op-6519061250c7a6)

## Bill Of Materials Search

Script Report. The reference record is BOM. Declared inputs include `item1`, `item2`, `item3`, `item4`, `item5`, `search_sub_assemblies`.

Named output fields constructed in this report include `parent`, `doctype`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/bom_search/bom_search.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/bom_search/bom_search.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-004.md#op-7017b9fa7e8944)

## By Item Recommended Reorder Level

Script Report. The reference record is Item. Declared inputs include `from_date`, `to_date`, `item_group`, `brand`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/itemwise_recommended_reorder_level/itemwise_recommended_reorder_level.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/itemwise_recommended_reorder_level/itemwise_recommended_reorder_level.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-029.md#op-7148a3d17af418)

## Cost Of Goods Sold By Item Group

Script Report. The reference record is GL Entry. Declared inputs include `company`, `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `item_group`, `cogs_debit`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/cogs_by_item_group/cogs_by_item_group.py#L34) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/cogs_by_item_group/cogs_by_item_group.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-004.md#op-d8e5acd5fe9092)

## Delayed Item Report

Script Report. The reference record is Delivery Note. Declared inputs include `company`, `from_date`, `to_date`, `sales_order`, `customer`, `customer_group`, `item_group`, `based_on`.

The direct return positions are data / columns. Named output fields constructed in this report include `name`, `customer`, `shipping_address_name`, `delivery_date`, `posting_date`, `item_code`, `item_name`, `qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/delayed_item_report/delayed_item_report.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/delayed_item_report/delayed_item_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-005.md#op-bc8dcef8aa7cca)

## Delayed Order Report

Script Report. The reference record is Delivery Note. Declared inputs include `company`, `from_date`, `to_date`, `sales_order`, `customer`, `customer_group`, `item_group`, `based_on`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `customer`, `shipping_address_name`, `delivery_date`, `posting_date`, `grand_total`, `delayed_days`, `sales_order`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/delayed_order_report/delayed_order_report.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/delayed_order_report/delayed_order_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-006.md#op-bf5075d3e1b672)

## Delivery Note Trends

Script Report. The reference record is Delivery Note. Declared inputs include `company`, `period`, `based_on`, `group_by`, `fiscal_year`, `item_code`.

The linked row procedure owns the output; inspect its conditional returns and result builders for the selected filters. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/delivery_note_trends/delivery_note_trends.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/delivery_note_trends/delivery_note_trends.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-009.md#op-9c53836bc48be5)

## First In First Out Queue Compared With Quantity After Transaction Comparison

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `item_code`, `item_group`, `warehouse`, `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `item_code`, `warehouse`, `posting_date`, `posting_time`, `creation`, `voucher_type`, `voucher_no`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/fifo_queue_vs_qty_after_transaction_comparison/fifo_queue_vs_qty_after_transaction_comparison.py#L38) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/fifo_queue_vs_qty_after_transaction_comparison/fifo_queue_vs_qty_after_transaction_comparison.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-013.md#op-63bb2942907ada)

## Incorrect Balance Quantity After Transaction

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `item_code`, `warehouse`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `posting_date`, `voucher_type`, `voucher_no`, `item_code`, `warehouse`, `expected_balance_qty`, `qty_after_transaction`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/incorrect_balance_qty_after_transaction/incorrect_balance_qty_after_transaction.py#L9) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/incorrect_balance_qty_after_transaction/incorrect_balance_qty_after_transaction.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-017.md#op-347b80a7c199ae)

## Incorrect Serial And Batch Bundle

Script Report. The reference record is Serial and Batch Bundle. Declared inputs include `item_code`, `warehouse`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `voucher_type`, `voucher_no`, `voucher_detail_no`, `is_cancelled`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/incorrect_serial_and_batch_bundle/incorrect_serial_and_batch_bundle.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/incorrect_serial_and_batch_bundle/incorrect_serial_and_batch_bundle.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-018.md#op-b472347ae4405e)

## Incorrect Serial Number Valuation

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `item_code`, `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `company`, `name`, `posting_date`, `posting_time`, `voucher_type`, `voucher_no`, `item_code`, `warehouse`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/incorrect_serial_no_valuation/incorrect_serial_no_valuation.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/incorrect_serial_no_valuation/incorrect_serial_no_valuation.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-018.md#op-ef1734b28fef55)

## Incorrect Stock Value Report

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `account`, `from_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `posting_date`, `posting_time`, `voucher_type`, `voucher_no`, `item_code`, `warehouse`, `expected_stock_value`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/incorrect_stock_value_report/incorrect_stock_value_report.py#L16) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/incorrect_stock_value_report/incorrect_stock_value_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-018.md#op-52a3dbae0d88ae)

## Item Balance Simple

Script Report. The reference record is Bin.

The direct return positions are get columns / get data. Named output fields constructed in this report include `item_code`, `item_name`, `item_group`, `brand`, `description`, `warehouse`, `actual_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_balance_%28simple%29/item_balance_%28simple%29.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_balance_%28simple%29/item_balance_%28simple%29.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-025.md#op-71e9b866963f7d)

## Item Price Stock

Script Report. The reference record is Item. Declared inputs include `item_code`.

The direct return positions are columns / data. Named output fields constructed in this report include `item_code`, `item_name`, `brand`, `warehouse`, `stock_available`, `stock_uom`, `buying_price_list`, `buying_rate`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_price_stock/item_price_stock.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_price_stock/item_price_stock.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-026.md#op-2ece2e0e6e0132)

## Item Prices

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `items`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_prices/item_prices.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_prices/item_prices.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-027.md#op-1109cf04bb599f)

## Item Shortage Report

Script Report. The reference record is Bin. Declared inputs include `company`, `warehouse`.

Named output fields constructed in this report include `warehouse`, `item_code`, `actual_qty`, `ordered_qty`, `indented_qty`, `planned_qty`, `reserved_qty`, `reserved_qty_for_production`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_shortage_report/item_shortage_report.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_shortage_report/item_shortage_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-027.md#op-2645eeb854ff21)

## Item Variant Details

Script Report. The reference record is Item. Declared inputs include `item`, `item_group`, `warehouse`.

The direct return positions are columns / data. Named output fields constructed in this report include `variant_name`, `item_group`, `avg_buying_price_list_rate`, `avg_selling_price_list_rate`, `stock_uom`, `current_stock`, `in_production`, `open_orders`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_variant_details/item_variant_details.py#L17) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_variant_details/item_variant_details.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-027.md#op-953249802e431a)

## Item Where Used

Script Report. The reference record is Item. Declared inputs include `item`, `company`, `section`.

The direct return positions are get columns / data. Named output fields constructed in this report include `section`, `reference_type`, `document_type`, `document_name`, `related_item`, `row_index`, `quantity`, `uom`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_where_used/item_where_used.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_where_used/item_where_used.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-028.md#op-e111a30c1cdb00)

## Item Wise Consumption

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `supplier`, `from_date`, `to_date`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_wise_consumption/item_wise_consumption.py#L16) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_wise_consumption/item_wise_consumption.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-029.md#op-ee7b5b064b6473)

## Item Wise Price List Rate

Report Builder. The reference record is Item Price.

The saved view selects `Item Price.name`, `Item Price.price_list`, `Item Price.currency`, `Item Price.item_code`, `Item Price.brand`, `Item Price.price_list_rate`, `Item Price.docstatus`. Saved ordering uses ``tabItem Price`.`modified` asc`. [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/item_wise_price_list_rate/item_wise_price_list_rate.json)

## Items To Be Requested

Script Report. The reference record is Material Request.

The direct return positions are get columns / get data. Named output fields constructed in this report include `item_code`, `warehouse`, `actual_qty`, `indented_qty`, `reserved_qty`, `ordered_qty`, `projected_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/items_to_be_requested/items_to_be_requested.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/items_to_be_requested/items_to_be_requested.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-029.md#op-59171f1bac369c)

## Landed Cost Report

Script Report. The reference record is Landed Cost Voucher. Declared inputs include `company`, `from_date`, `to_date`, `raw_material_voucher_type`, `raw_material_voucher_no`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `landed_cost`, `currency`, `voucher_type`, `voucher_no`, `vendor_invoice`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/landed_cost_report/landed_cost_report.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/landed_cost_report/landed_cost_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-029.md#op-bdf8dd70603504)

## Material Requests For Which Supplier Quotations Are Not Created

Query Report. The reference record is Material Request.

See the [row-selection rule and worked example](query-rules.md#material-requests-for-which-supplier-quotations-are-not-created). [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/material_requests_for_which_supplier_quotations_are_not_created/material_requests_for_which_supplier_quotations_are_not_created.json)

## Negative Batch Report

Script Report. The reference record is Serial and Batch Bundle. Declared inputs include `company`, `item_code`, `warehouse`.

The direct return positions are columns / data. Named output fields constructed in this report include `posting_date`, `batch_no`, `item_code`, `warehouse`, `previous_qty`, `actual_qty`, `qty_after_transaction`, `voucher_type`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/negative_batch_report/negative_batch_report.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/negative_batch_report/negative_batch_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-034.md#op-eb7377ae54dba6)

## Product Bundle Balance

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `date`, `item_code`, `item_group`, `brand`, `warehouse`.

The direct return positions are columns / data. Named output fields constructed in this report include `item_code`, `warehouse`, `uom`, `bundle_qty`, `actual_qty`, `minimum_qty`, `item_group`, `brand`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/product_bundle_balance/product_bundle_balance.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/product_bundle_balance/product_bundle_balance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-043.md#op-d8d5de44464d38)

## Purchase Receipt Trends

Script Report. The reference record is Purchase Receipt. Declared inputs include `company`, `period`, `fiscal_year`, `based_on`, `group_by`, `item_code`.

The linked row procedure owns the output; inspect its conditional returns and result builders for the selected filters. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/purchase_receipt_trends/purchase_receipt_trends.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/purchase_receipt_trends/purchase_receipt_trends.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-047.md#op-1eaafb5e5819ba)

## Requested Items To Be Transferred

Query Report. The reference record is Stock Entry.

See the [row-selection rule and worked example](query-rules.md#requested-items-to-be-transferred). [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/requested_items_to_be_transferred/requested_items_to_be_transferred.json)

## Reserved Stock

Script Report. The reference record is Stock Reservation Entry. Declared inputs include `company`, `from_date`, `to_date`, `item_code`, `warehouse`, `stock_reservation_entry`, `voucher_type`, `voucher_no`, `from_voucher_type`, `from_voucher_no`, `reservation_based_on`, `status`, `project`.

The direct return positions are columns / data. Named output fields constructed in this report include `date`, `warehouse`, `item_code`, `stock_uom`, `voucher_qty`, `reserved_qty`, `delivered_qty`, `transferred_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/reserved_stock/reserved_stock.py#L15) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/reserved_stock/reserved_stock.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-053.md#op-14b2087d884427)

## Serial And Batch Summary

Script Report. The reference record is Serial and Batch Bundle. Declared inputs include `company`, `from_date`, `to_date`, `item_code`, `warehouse`, `voucher_type`, `voucher_no`, `serial_no`, `batch_no`.

The direct return positions are columns / data. Named output fields constructed in this report include `company`, `name`, `posting_date`, `voucher_type`, `voucher_no`, `item_code`, `item_name`, `warehouse`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/serial_and_batch_summary/serial_and_batch_summary.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/serial_and_batch_summary/serial_and_batch_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-060.md#op-f4b958ac1c776a)

## Serial Number And Batch Traceability

Script Report. The reference record is Serial and Batch Bundle. Declared inputs include `item_code`, `batches`, `serial_nos`, `traceability_direction`.

The direct return positions are columns / data. Named output fields constructed in this report include `item_code`, `item_name`, `serial_no`, `batch_no`, `batch_expiry_date`, `qty`, `reference_doctype`, `reference_name`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/serial_no_and_batch_traceability/serial_no_and_batch_traceability.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/serial_no_and_batch_traceability/serial_no_and_batch_traceability.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-064.md#op-d98eef53abd372)

## Serial Number Ledger

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `item_code`, `warehouse`, `serial_no`, `posting_date`, `posting_time`.

The direct return positions are columns / data. Named output fields constructed in this report include `posting_date`, `posting_time`, `voucher_type`, `voucher_no`, `company`, `warehouse`, `status`, `serial_no`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/serial_no_ledger/serial_no_ledger.py#L17) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/serial_no_ledger/serial_no_ledger.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-065.md#op-6cf2e836d5b9b1)

## Serial Number Service Contract Expiry

Report Builder. The reference record is Serial No.

The saved view selects `Serial No.name`, `Serial No.serial_no`, `Serial No.item_code`, `Serial No.amc_expiry_date`, `Serial No.maintenance_status`, `Serial No.item_name`, `Serial No.description`, `Serial No.item_group`, `Serial No.brand`. Saved ordering uses ``tabSerial No`.`amc_expiry_date` asc`. [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/serial_no_service_contract_expiry/serial_no_service_contract_expiry.json)

## Serial Number Status

Report Builder. The reference record is Serial No.

The saved view selects `Serial No.name`, `Serial No.serial_no`, `Serial No.item_code`, `Serial No.status`, `Serial No.warehouse`, `Serial No.item_name`, `Serial No.description`, `Serial No.item_group`, `Serial No.brand`, `Serial No.reference_name`, `Serial No.reference_doctype`, `Serial No.customer`. Saved ordering uses ``tabSerial No`.`serial_no` desc`. [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/serial_no_status/serial_no_status.json)

## Serial Number Warranty Expiry

Report Builder. The reference record is Serial No.

The saved view selects `Serial No.name`, `Serial No.serial_no`, `Serial No.item_code`, `Serial No.item_name`, `Serial No.customer`, `Serial No.warranty_expiry_date`, `Serial No.maintenance_status`, `Serial No.item_group`, `Serial No.brand`. Saved ordering uses ``tabSerial No`.`warranty_expiry_date` asc`. [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/serial_no_warranty_expiry/serial_no_warranty_expiry.json)

## Stock Ageing

Script Report. The reference record is Item. Declared inputs include `company`, `to_date`, `warehouse_type`, `warehouse`, `item_code`, `brand`, `range`, `show_warehouse_wise_stock`.

The direct return positions are columns / data / absent / chart data. Named output fields constructed in this report include `item_code`, `item_name`, `description`, `item_group`, `brand`, `warehouse`, `qty`, `average_age`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_ageing/stock_ageing.py#L39) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_ageing/stock_ageing.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-067.md#op-7738d32a481653)

## Stock Analytics

Script Report. The reference record is Stock Entry. Declared inputs include `item_group`, `item_code`, `value_quantity`, `brand`, `company`, `warehouse`, `from_date`, `to_date`, `range`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `name`, `item_name`, `item_group`, `brand`, `uom`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_analytics/stock_analytics.py#L23) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_analytics/stock_analytics.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-070.md#op-4ef48794d8efa1)

## Stock And Account Value Comparison

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `account`, `from_date`, `as_on_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `ledger_type`, `posting_date`, `posting_time`, `voucher_type`, `voucher_no`, `stock_value`, `account_value`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_and_account_value_comparison/stock_and_account_value_comparison.py#L18) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_and_account_value_comparison/stock_and_account_value_comparison.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-070.md#op-21471b885d7440)

## Stock Balance

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `from_date`, `to_date`, `item_group`, `item_code`, `warehouse`, `warehouse_type`, `valuation_field_type`, `include_uom`, `show_alt_uom_balance`, `show_variant_attributes`, `show_stock_ageing_data`, `ignore_closing_balance`, `include_zero_stock_items`, `show_dimension_wise_stock`.

The report returns the result of `StockBalanceReport.run`. Named output fields constructed in this report include `item_code`, `item_name`, `item_group`, `warehouse`, `stock_uom`, `bal_qty`, `bal_val`, `opening_qty`. The structured entry gives their enclosing conditions and builders. A separate snapshot procedure is also declared. [Worked result and boundaries](dynamic-output.md#stock-balances-and-optional-columns) [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_balance/stock_balance.py#L49) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_balance/stock_balance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-071.md#op-95270c52872739)

## Stock Ledger

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `from_date`, `to_date`, `warehouse`, `item_code`, `item_group`, `batch_no`, `brand`, `voucher_no`, `project`, `include_uom`, `valuation_field_type`, `segregate_serial_batch_bundle`.

Named output fields constructed in this report include `date`, `item_code`, `item_name`, `stock_uom`, `in_qty`, `out_qty`, `qty_after_transaction`, `warehouse`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_ledger/stock_ledger.py#L26) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_ledger/stock_ledger.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-087.md#op-fe45452b5d1971)

## Stock Ledger Entries Of Cancelled Vouchers

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `from_date`, `to_date`, `voucher_type`, `item_code`, `warehouse`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `name`, `voucher_type`, `voucher_no`, `posting_date`, `item_code`, `warehouse`, `actual_qty`, `stock_value_difference`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_ledger_entries_of_cancelled_vouchers/stock_ledger_entries_of_cancelled_vouchers.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_ledger_entries_of_cancelled_vouchers/stock_ledger_entries_of_cancelled_vouchers.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-094.md#op-2499126399d21d)

## Stock Ledger Invariant Check

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `item_code`, `warehouse`, `show_incorrect_entries`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `posting_date`, `posting_time`, `creation`, `voucher_type`, `voucher_no`, `batch_no`, `serial_and_batch_bundle`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_ledger_invariant_check/stock_ledger_invariant_check.py#L35) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_ledger_invariant_check/stock_ledger_invariant_check.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-095.md#op-472f1cf6ddcdca)

## Stock Ledger Variance

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `item_code`, `warehouse`, `difference_in`, `include_disabled`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `posting_date`, `posting_time`, `creation`, `item_code`, `warehouse`, `valuation_method`, `voucher_type`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_ledger_variance/stock_ledger_variance.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_ledger_variance/stock_ledger_variance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-096.md#op-482cb737201a38)

## Stock Projected Quantity

Script Report. The reference record is Item. Declared inputs include `company`, `warehouse`, `item_code`, `item_group`, `brand`, `include_uom`.

The direct return positions are columns / data. Named output fields constructed in this report include `item_code`, `item_name`, `description`, `item_group`, `brand`, `warehouse`, `stock_uom`, `actual_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_projected_qty/stock_projected_qty.py#L18) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_projected_qty/stock_projected_qty.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-096.md#op-1b12508b9b6c47)

## Stock Quantity Compared With Batch Quantity

Script Report. The reference record is Item. Declared inputs include `item`, `batch`.

The direct return positions are columns / data. Named output fields constructed in this report include `item_code`, `item_name`, `batch`, `batch_qty`, `stock_qty`, `difference`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_qty_vs_batch_qty/stock_qty_vs_batch_qty.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_qty_vs_batch_qty/stock_qty_vs_batch_qty.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-096.md#op-ab051097adf549)

## Stock Quantity Compared With Serial Number Count

Script Report. The reference record is Item. Declared inputs include `company`, `warehouse`, `show_disabled_items`.

The direct return positions are columns / data. Named output fields constructed in this report include `item_code`, `item_name`, `total`, `stock_qty`, `difference`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_qty_vs_serial_no_count/stock_qty_vs_serial_no_count.py#L16) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_qty_vs_serial_no_count/stock_qty_vs_serial_no_count.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-096.md#op-ab36bf017253b3)

## Stock Valuation Comparison

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `from_date`, `to_date`, `item_code`, `item_group`, `warehouse`, `show`, `tolerance`, `show_adjusted_differences`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `posting_date`, `posting_time`, `item_code`, `warehouse`, `voucher_type`, `voucher_no`, `serial_and_batch_bundle`, `actual_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_valuation_comparison/stock_valuation_comparison.py#L47) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_valuation_comparison/stock_valuation_comparison.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-104.md#op-1a6bbdd895e91a)

## Total Stock Summary

Script Report. The reference record is Stock Entry. Declared inputs include `group_by`, `company`.

The direct return positions are columns / stock. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/total_stock_summary/total_stock_summary.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/total_stock_summary/total_stock_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-105.md#op-8c3128553d5998)

## Warehouse Wise Item Balance Age And Value

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `from_date`, `to_date`, `item_group`, `item_code`, `warehouse`, `filter_total_zero_qty`.

The linked row procedure owns the output; inspect its conditional returns and result builders for the selected filters. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/warehouse_wise_item_balance_age_and_value/warehouse_wise_item_balance_age_and_value.py#L27) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/warehouse_wise_item_balance_age_and_value/warehouse_wise_item_balance_age_and_value.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-110.md#op-8deaa25c081ea8)

## Warehouse Wise Stock Balance

Script Report. The reference record is Stock Ledger Entry. Declared inputs include `company`, `show_disabled_warehouses`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `stock_balance`, `disabled`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/warehouse_wise_stock_balance/warehouse_wise_stock_balance.py#L22) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/warehouse_wise_stock_balance/warehouse_wise_stock_balance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/stock/operations-111.md#op-c0288f8f0df8a1)
