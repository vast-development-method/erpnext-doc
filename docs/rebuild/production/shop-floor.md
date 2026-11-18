# Shop-floor execution and material reservation handoff

The [Shop-floor execution and material reservation handoff](../../operations/shop-floor.md) chapter defines the business rules, calculations and worked outcomes.

## Allocate finite capacity and record actual machine time

- [Scheduling, interval costing and employee checks](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/job_card/job_card.py)
- [Workstation entry points](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/workstation/workstation.py#L189-L241)

## Quantity through sequential operations

- [Sequence and loss rules](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/job_card/job_card.py#L1717-L1920)
- [Reference test setup](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/job_card/test_job_card.py)

## Cost regular and corrective operations

- [manufacturing blueprint](../../domains/manufacturing-and-subcontracting.md)
- [Operating cost calculations](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/work_order/work_order.py#L726-L776)

## Reserve, hand off and release material identities

- [Reservation boundaries and handoff](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_reservation_entry/stock_reservation_entry.py)

## Downtime unit and reporting boundary

- [Downtime validation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/downtime_entry/downtime_entry.py)
- [Report](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/report/downtime_analysis/downtime_analysis.py)
