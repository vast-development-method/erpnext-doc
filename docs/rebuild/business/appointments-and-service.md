# Customer appointments, service commitments and service billing

The [Customer appointments, service commitments and service billing](../../people-and-services/customer-appointments.md) chapter defines the business rules, calculations and worked outcomes.

## Reserve an appointment

- [Public booking command](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/www/book_appointment/index.py#L100-L175)
- [Validation and lifecycle](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/appointment/appointment.py#L49-L206)
- [Overlap predicate](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/appointment/appointment.py#L423-L475)
- [Verification](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/www/book_appointment/verify/index.py)
- [Materialization and assignment](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/appointment/appointment.py#L234-L419)

## Choose a service-level agreement

- [service clock and hold accounting](../../domains/service-and-support.md)
- [Rule selection](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/support/doctype/service_level_agreement/service_level_agreement.py#L344-L450)

## Bind maintenance coverage to the delivered serial

- [Serial and schedule checks](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/maintenance/doctype/maintenance_schedule/maintenance_schedule.py#L295-L379)
- [Cancellation and projection](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/maintenance/doctype/maintenance_schedule/maintenance_schedule.py#L417-L456)

## Costed time, task access and invoicing

- [Task and project access](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L221-L269)
- [Totals inputs and task status](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L368-L405)
- [Invoice preparation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L550-L604)
- [Project costing](../../domains/projects-and-time-billing.md)
