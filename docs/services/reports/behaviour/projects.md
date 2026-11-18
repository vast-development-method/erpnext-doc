# Projects reports

The [structured report details](projects.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Daily Timesheet Summary

Script Report. The reference record is Timesheet. Declared inputs include `from_date`, `to_date`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/report/daily_timesheet_summary/daily_timesheet_summary.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/report/daily_timesheet_summary/daily_timesheet_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/projects/operations-001.md#op-0789c7633b3fe2)

## Delayed Tasks Summary

Script Report. The reference record is Task. Declared inputs include `project`, `from_date`, `to_date`, `priority`, `status`.

The direct return positions are columns / data / absent / charts. Named output fields constructed in this report include `name`, `subject`, `project`, `status`, `priority`, `progress`, `exp_start_date`, `exp_end_date`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/report/delayed_tasks_summary/delayed_tasks_summary.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/report/delayed_tasks_summary/delayed_tasks_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/projects/operations-001.md#op-acd865efa5cf1b)

## Project Summary

Script Report. The reference record is Project. Declared inputs include `company`, `is_active`, `status`, `project_type`, `priority`.

The direct return positions are columns / data / absent / chart / report summary. Named output fields constructed in this report include `name`, `project_name`, `project_type`, `status`, `total_tasks`, `completed_tasks`, `overdue_tasks`, `percent_complete`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/report/project_summary/project_summary.py#L9) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/report/project_summary/project_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/projects/operations-011.md#op-22829e6670df39)

## Project Wise Stock Tracking

Script Report. The reference record is Project.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/report/project_wise_stock_tracking/project_wise_stock_tracking.py#L9) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/report/project_wise_stock_tracking/project_wise_stock_tracking.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/projects/operations-012.md#op-7e210926d940ba)

## Timesheet Billing Summary

Script Report. The reference record is Timesheet. Declared inputs include `employee`, `project`, `from_date`, `to_date`, `group_by`, `include_draft_timesheets`.

Named output fields constructed in this report include `date`, `project`, `employee`, `employee_name`, `timesheet`, `hours`, `billing_hours`, `billing_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/report/timesheet_billing_summary/timesheet_billing_summary.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/report/timesheet_billing_summary/timesheet_billing_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/projects/operations-016.md#op-e9668d7f0c8cda)
