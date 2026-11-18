# Maintenance declarations in business application

Each dictionary part contains an ordered field list, source location, record settings and grants. The source column opens the declaration at the reviewed revision.

| Record | Storage | Fields | Dictionary | Source |
|---|---|---:|---|---|
| Maintenance Schedule | ordinary | 24 | [Part 1](../catalog/erpnext-maintenance-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/maintenance/doctype/maintenance_schedule/maintenance_schedule.json) |
| Maintenance Schedule Detail | child | 12 | [Part 1](../catalog/erpnext-maintenance-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/maintenance/doctype/maintenance_schedule_detail/maintenance_schedule_detail.json) |
| Maintenance Schedule Item | child | 16 | [Part 1](../catalog/erpnext-maintenance-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/maintenance/doctype/maintenance_schedule_item/maintenance_schedule_item.json) |
| Maintenance Visit | ordinary | 32 | [Part 1](../catalog/erpnext-maintenance-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/maintenance/doctype/maintenance_visit/maintenance_visit.json) |
| Maintenance Visit Purpose | child | 12 | [Part 1](../catalog/erpnext-maintenance-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/maintenance/doctype/maintenance_visit_purpose/maintenance_visit_purpose.json) |
