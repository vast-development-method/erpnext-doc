# Declaration comparison evidence

These counts reconcile the source extracts used to build the [record specification](INDEX.md). Group a record by its declaring module, or by its last known module if absent. Each comparison supplies the source paths and changed facts. Added and removed record fields follow import order. The ordering comparison covers only fields present in both inputs.

| Area | Comparison input records / fields | Dictionary input records / fields | Added | Absent | Changed | Unchanged |
|---|---:|---:|---:|---:|---:|---:|
| Shared foundation | 296 / 3448 | 332 / 3795 | 42 | 6 | 141 | 149 |
| Business application | 534 / 10648 | 534 / 10617 | 3 | 3 | 340 | 191 |
| Workforce | 160 / 2118 | 161 / 2219 | 6 | 5 | 104 | 51 |
| Customer relationships | 52 / 595 | 54 / 610 | 2 | 0 | 13 | 39 |

## Shared foundation

| Module | Comparison | Records differing |
|---|---|---:|
| Automation | [Compared declarations](delta/frappe-automation-01.json) | 12 |
| Contacts | [Compared declarations](delta/frappe-contacts-01.json) | 5 |
| Core | [Compared declarations](delta/frappe-core-01.json) | 51 |
| Custom | [Compared declarations](delta/frappe-custom-01.json) | 7 |
| Desk | [Compared declarations](delta/frappe-desk-01.json) | 31 |
| Email | [Compared declarations](delta/frappe-email-01.json) | 9 |
| Flow | [Compared declarations](delta/frappe-flow-01.json) | 20 |
| Geo | [Compared declarations](delta/frappe-geo-01.json) | 2 |
| Integrations | [Compared declarations](delta/frappe-integrations-01.json) | 17 |
| Printing | [Compared declarations](delta/frappe-printing-01.json) | 7 |
| Studio | [Compared declarations](delta/frappe-studio-01.json) | 10 |
| Website | [Compared declarations](delta/frappe-website-01.json) | 14 |
| Workflow | [Compared declarations](delta/frappe-workflow-01.json) | 4 |

## Business application

| Module | Comparison | Records differing |
|---|---|---:|
| Accounts | [Compared declarations](delta/erpnext-accounts-01.json) | 106 |
| Assets | [Compared declarations](delta/erpnext-assets-01.json) | 20 |
| Buying | [Compared declarations](delta/erpnext-buying-01.json) | 15 |
| CRM | [Compared declarations](delta/erpnext-crm-01.json) | 16 |
| Communication | [Compared declarations](delta/erpnext-communication-01.json) | 1 |
| EDI | [Compared declarations](delta/erpnext-edi-01.json) | 2 |
| Business Integrations | [Compared declarations](delta/erpnext-erpnext-integrations-01.json) | 1 |
| Maintenance | [Compared declarations](delta/erpnext-maintenance-01.json) | 2 |
| Manufacturing | [Compared declarations](delta/erpnext-manufacturing-01.json) | 35 |
| Projects | [Compared declarations](delta/erpnext-projects-01.json) | 11 |
| Quality Management | [Compared declarations](delta/erpnext-quality-management-01.json) | 10 |
| Regional | [Compared declarations](delta/erpnext-regional-01.json) | 4 |
| Selling | [Compared declarations](delta/erpnext-selling-01.json) | 15 |
| Setup | [Compared declarations](delta/erpnext-setup-01.json) | 29 |
| Stock | [Compared declarations](delta/erpnext-stock-01.json) | 57 |
| Subcontracting | [Compared declarations](delta/erpnext-subcontracting-01.json) | 9 |
| Support | [Compared declarations](delta/erpnext-support-01.json) | 6 |
| Telephony | [Compared declarations](delta/erpnext-telephony-01.json) | 4 |
| Utilities | [Compared declarations](delta/erpnext-utilities-01.json) | 3 |

## Workforce

| Module | Comparison | Records differing |
|---|---|---:|
| HR | [Compared declarations](delta/hrms-hr-01.json) | 89 |
| Payroll | [Compared declarations](delta/hrms-payroll-01.json) | 26 |

## Customer relationships

| Module | Comparison | Records differing |
|---|---|---:|
| Domain Enrichment | [Compared declarations](delta/crm-domain-enrichment-01.json) | 3 |
| FCRM | [Compared declarations](delta/crm-fcrm-01.json) | 12 |
