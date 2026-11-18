# Turning a shortage into an authorised material request

The [Turning a shortage into an authorised material request](../../operations/replenishment.md) chapter defines the business rules, calculations and worked outcomes.

The scheduler copies a template's reorder rows to eligible variants without explicit rows. It later skips records bearing the multi-variant template flag. Explicit variant-level rules follow normal replenishment. Validate that the copied rule survives selection before counting an inherited template rule as expected supply.

## Scheduled replenishment

- [Scheduler](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/reorder_item.py)
- [Material-request tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/material_request/test_material_request.py)

## Material requests from a production plan

- [Production plan](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/production_plan/production_plan.py)
- [Minimums, conversions and reservation cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/production_plan/test_production_plan.py)
