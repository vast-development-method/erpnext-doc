# Inspection evidence, release gates and corrective action

The [Inspection evidence, release gates and corrective action](../../operations/quality.md) chapter defines the business rules, calculations and worked outcomes.

For a monthly goal scheduled on the 31st, 28 February 2025 is the effective due date. A single daily pass tests for an existing review by goal and date. Concurrent scheduler invocations require an atomic uniqueness guarantee on that pair.

## Bind evidence to the inspected row

- [Row binding and lifecycle](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/quality_inspection/quality_inspection.py)
- [Upstream inspection cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/quality_inspection/test_quality_inspection.py)

## Decide the reading and release the operation

- [Release gates](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/stock_controller.py#L1823-L1926)
- [Operator guide](https://docs.frappe.io/erpnext/quality-inspection)

## Review goals and resolve actions

- [Goal review](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/quality_management/doctype/quality_review/quality_review.py)
- [Action](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/quality_management/doctype/quality_action/quality_action.py)
- [Nonconformance record](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/quality_management/doctype/non_conformance/non_conformance.json)
