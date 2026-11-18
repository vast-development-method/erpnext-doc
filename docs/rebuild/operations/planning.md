# From dated demand to a release recommendation

The [From dated demand to a release recommendation](../../operations/planning.md) chapter defines the business rules, calculations and worked outcomes.

The master schedule supports creation, saving and reporting. Its submission callback names a deferred materials-planning job, but the declared form cannot be submitted. A production workflow that relies on logs from this job must establish a reachable dispatch path.

## Forecast and schedule records

- [Forecast controller](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/sales_forecast/sales_forecast.py)
- [Schedule controller](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/master_production_schedule/master_production_schedule.py)
- [Schedule metadata](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/master_production_schedule/master_production_schedule.json)

## Calculate cumulative lead time

- [Schedule calculation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/master_production_schedule/master_production_schedule.py#L193-L227)
- [Report calculation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/material_requirements_planning_report/material_requirements_planning_report.py#L1350-L1365)

## Net demand in order

- [Requirements report](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/material_requirements_planning_report/material_requirements_planning_report.py)
- [Upstream acceptance cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/material_requirements_planning_report/test_material_requirements_planning_report.py)
