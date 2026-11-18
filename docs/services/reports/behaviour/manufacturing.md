# Manufacturing reports

The [structured report details](manufacturing.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Bill Of Materials Explorer

Script Report. The reference record is BOM. Declared inputs include `bom`.

The direct return positions are columns / data. Named output fields constructed in this report include `item_code`, `item_name`, `bom`, `is_phantom_item`, `qty`, `uom`, `bom_level`, `description`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/bom_explorer/bom_explorer.py#L9) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/bom_explorer/bom_explorer.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-013.md#op-77d69bcf34d9a9)

## Bill Of Materials Operations Time

Script Report. The reference record is BOM. Declared inputs include `item_code`, `bom_id`, `workstation`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `item`, `item_name`, `uom`, `operation`, `workstation`, `time_in_mins`, `used_as_subassembly_items`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/bom_operations_time/bom_operations_time.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/bom_operations_time/bom_operations_time.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-014.md#op-29363a8f479842)

## Bill Of Materials Stock Analysis

Script Report. The reference record is BOM. Declared inputs include `bom`, `warehouse`, `qty_to_make`, `show_exploded_view`.

The direct return positions are columns / data. Named output fields constructed in this report include `item`, `description`, `from_bom_no`, `manufacturer`, `manufacturer_part_number`, `qty_per_unit`, `available_qty`, `required_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/bom_stock_analysis/bom_stock_analysis.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/bom_stock_analysis/bom_stock_analysis.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-014.md#op-432adea209155a)

## Bill Of Materials Variance Report

Script Report. The reference record is Stock Entry. Declared inputs include `bom_no`, `work_order`.

The direct return positions are columns / data. Named output fields constructed in this report include `work_order`, `bom_no`, `production_item`, `qty`, `produced_qty`, `raw_material_code`, `required_qty`, `consumed_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/bom_variance_report/bom_variance_report.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/bom_variance_report/bom_variance_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-016.md#op-306601daedfa1d)

## Completed Work Orders

Query Report. The reference record is Work Order.

See the [row-selection rule and worked example](query-rules.md#completed-work-orders). [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/completed_work_orders/completed_work_orders.json)

## Cost Of Poor Quality Report

Script Report. The reference record is Job Card. Declared inputs include `company`, `from_date`, `to_date`, `name`, `work_order`, `operation`, `workstation`, `production_item`, `serial_no`, `batch_no`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `name`, `work_order`, `item_code`, `item_name`, `operation`, `serial_no`, `batch_no`, `workstation`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/cost_of_poor_quality_report/cost_of_poor_quality_report.py#L16) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/cost_of_poor_quality_report/cost_of_poor_quality_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-016.md#op-8e8a0f0c28ad68)

## Downtime Analysis

Script Report. The reference record is Downtime Entry. Declared inputs include `from_date`, `to_date`, `workstation`.

The direct return positions are columns / data / absent / chart data. Named output fields constructed in this report include `name`, `workstation`, `operator`, `from_time`, `to_time`, `downtime`, `stop_reason`, `remarks`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/downtime_analysis/downtime_analysis.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/downtime_analysis/downtime_analysis.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-017.md#op-6c1a3dc81541c6)

## Exponential Smoothing Forecasting

Script Report. The reference record is Sales Order. Declared inputs include `company`, `from_date`, `to_date`, `based_on_document`, `based_on_field`, `no_of_years`, `periodicity`, `smoothing_constant`, `item_code`, `warehouse`.

The report returns the result of `ForecastingReport.execute_report`. Named output fields constructed in this report include `item_code`, `warehouse`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/exponential_smoothing_forecasting/exponential_smoothing_forecasting.py#L15) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/exponential_smoothing_forecasting/exponential_smoothing_forecasting.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-017.md#op-9daf15c31ad82e)

## Issued Items Against Work Order

Query Report. The reference record is Work Order.

See the [row-selection rule and worked example](query-rules.md#issued-items-against-work-order). [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/issued_items_against_work_order/issued_items_against_work_order.json)

## Job Card Summary

Script Report. The reference record is Job Card. Declared inputs include `company`, `fiscal_year`, `from_date`, `to_date`, `status`, `work_order`, `production_item`, `workstation`, `operation`.

The direct return positions are columns / data / absent / chart data. Named output fields constructed in this report include `name`, `posting_date`, `status`, `work_order`, `production_item`, `item_name`, `workstation`, `operation`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/job_card_summary/job_card_summary.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/job_card_summary/job_card_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-024.md#op-09a45da70107d0)

## Material Requirements Planning Report

Script Report. The reference record is Master Production Schedule. Declared inputs include `company`, `from_date`, `to_date`, `item_code`, `warehouse`, `mps`, `type_of_material`, `add_safety_stock`, `show_in_bucket_view`, `bucket_view`, `bucket_size`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `item_code`, `item_name`, `capacity`, `type_of_material`, `warehouse`, `demand_qty`, `adhoc_qty`, `planned_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/material_requirements_planning_report/material_requirements_planning_report.py#L28) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/material_requirements_planning_report/material_requirements_planning_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-026.md#op-53ab7fb104101c)

## Open Work Orders

Query Report. The reference record is Work Order.

See the [row-selection rule and worked example](query-rules.md#open-work-orders). [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/open_work_orders/open_work_orders.json)

## Process Loss Report

Script Report. The reference record is Work Order. Declared inputs include `company`, `item`, `work_order`, `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `production_item`, `status`, `qty_to_manufacture`, `produced_qty`, `process_loss_qty`, `total_pl_value`, `total_fg_value`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/process_loss_report/process_loss_report.py#L19) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/process_loss_report/process_loss_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-029.md#op-e0cd6f0d90460e)

## Production Analytics

Script Report. The reference record is Work Order. Declared inputs include `company`, `from_date`, `to_date`, `range`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `status`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/production_analytics/production_analytics.py#L19) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/production_analytics/production_analytics.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-029.md#op-6ce11f3b741c44)

## Production Plan Summary

Script Report. The reference record is Production Plan. Declared inputs include `production_plan`.

The direct return positions are columns / data. Named output fields constructed in this report include `item_code`, `item_name`, `sales_order`, `document_type`, `document_name`, `bom_level`, `qty`, `produced_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/production_plan_summary/production_plan_summary.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/production_plan_summary/production_plan_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-035.md#op-40bebee66eccac)

## Production Planning Report

Script Report. The reference record is Work Order. Declared inputs include `company`, `based_on`, `docnames`, `raw_material_warehouse`, `order_by`, `include_subassembly_raw_materials`.

The report returns the result of `ProductionPlanReport.execute_report`. Named output fields constructed in this report include `name`, `production_item`, `production_item_name`, `for_warehouse`, `qty_to_manufacture`, `available_qty`, `item_code`, `raw_material_name`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/production_planning_report/production_planning_report.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/production_planning_report/production_planning_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-036.md#op-494b7631b887f7)

## Quality Inspection Summary

Script Report. The reference record is Quality Inspection. Declared inputs include `from_date`, `to_date`, `status`, `item_code`, `inspected_by`.

The direct return positions are columns / data / absent / chart data. Named output fields constructed in this report include `name`, `report_date`, `status`, `item_code`, `item_name`, `sample_size`, `inspection_type`, `reference_type`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/quality_inspection_summary/quality_inspection_summary.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/quality_inspection_summary/quality_inspection_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-036.md#op-163a5d07a47a8e)

## Work Order Consumed Materials

Script Report. The reference record is Work Order. Declared inputs include `company`, `from_date`, `to_date`, `name`, `production_item`, `status`, `show_extra_consumed_materials`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `status`, `production_item`, `qty`, `produced_qty`, `raw_material_item_code`, `raw_material_name`, `required_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/work_order_consumed_materials/work_order_consumed_materials.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/work_order_consumed_materials/work_order_consumed_materials.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-046.md#op-b496bcd27c0b82)

## Work Order Stock Report

Script Report. The reference record is Work Order. Declared inputs include `warehouse`.

The direct return positions are columns / data. Named output fields constructed in this report include `work_order`, `bom_no`, `description`, `item_code`, `source_warehouse`, `qty`, `status`, `req_items`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/work_order_stock_report/work_order_stock_report.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/work_order_stock_report/work_order_stock_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-046.md#op-34f980f4015e57)

## Work Order Summary

Script Report. The reference record is Work Order. Declared inputs include `company`, `based_on`, `from_date`, `to_date`, `status`, `sales_order`, `production_item`, `age`, `charts_based_on`.

The direct return positions are columns / data / absent / chart data. Named output fields constructed in this report include `name`, `status`, `production_item`, `qty`, `produced_qty`, `sales_order`, `creation`, `planned_start_date`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/work_order_summary/work_order_summary.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/work_order_summary/work_order_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/manufacturing/operations-047.md#op-f79dafc1779eb4)

## Work Orders In Progress

Query Report. The reference record is Work Order.

See the [row-selection rule and worked example](query-rules.md#work-orders-in-progress). [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/work_orders_in_progress/work_orders_in_progress.json)
