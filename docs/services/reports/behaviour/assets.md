# Assets reports

The [structured report details](assets.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Asset Activity

Report Builder. The reference record is Asset Activity.

The saved view supplies no explicit column selection. The report builder resolves its visible fields from the reference record and effective view. [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/report/asset_activity/asset_activity.json)

## Asset Maintenance

Report Builder. The reference record is Asset Maintenance.

The saved view selects `Asset Maintenance.name`, `Asset Maintenance.asset_name`, `Asset Maintenance.item_code`, `Asset Maintenance Task.maintenance_type`, `Asset Maintenance Task.maintenance_task`, `Asset Maintenance Task.description`, `Asset Maintenance Task.assign_to_name`, `Asset Maintenance Task.maintenance_status`, `Asset Maintenance Task.next_due_date`, `Asset Maintenance Task.last_completion_date`. Saved ordering uses `Asset Maintenance.modified` (desc). [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/report/asset_maintenance/asset_maintenance.json)

## Fixed Asset Register

Script Report. The reference record is Asset. Declared inputs include `company`, `status`, `asset_category`, `cost_center`, `group_by`, `only_existing_assets`, `finance_book`, `include_default_book_assets`, `filter_based_on`, `from_date`, `to_date`, `from_fiscal_year`, `to_fiscal_year`, `date_based_on`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `net_purchase_amount`, `opening_accumulated_depreciation`, `depreciated_amount`, `asset_value`, `company`, `asset_id`, `asset_name`, `asset_category`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/report/fixed_asset_register/fixed_asset_register.py#L22) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/report/fixed_asset_register/fixed_asset_register.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/assets/operations-019.md#op-a280c9080d9c6f)
