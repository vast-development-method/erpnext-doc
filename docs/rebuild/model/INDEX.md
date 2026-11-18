# Modules and release comparison

## Core data dictionary

| App | Module | Records | Fields |
|---|---|---:|---:|
| erpnext | [Accounts](modules/erpnext-accounts.md) | 191 | 3419 |
| erpnext | [Assets](modules/erpnext-assets.md) | 26 | 421 |
| erpnext | [Bulk Transaction](modules/erpnext-bulk-transaction.md) | 2 | 15 |
| erpnext | [Buying](modules/erpnext-buying.md) | 20 | 786 |
| erpnext | [CRM](modules/erpnext-crm.md) | 28 | 359 |
| erpnext | [Communication](modules/erpnext-communication.md) | 2 | 12 |
| erpnext | [EDI](modules/erpnext-edi.md) | 2 | 19 |
| erpnext | [ERPNext Integrations](modules/erpnext-erpnext-integrations.md) | 1 | 9 |
| erpnext | [Maintenance](modules/erpnext-maintenance.md) | 5 | 96 |
| erpnext | [Manufacturing](modules/erpnext-manufacturing.md) | 50 | 1028 |
| erpnext | [Portal](modules/erpnext-portal.md) | 2 | 2 |
| erpnext | [Projects](modules/erpnext-projects.md) | 15 | 239 |
| erpnext | [Quality Management](modules/erpnext-quality-management.md) | 16 | 93 |
| erpnext | [Regional](modules/erpnext-regional.md) | 5 | 34 |
| erpnext | [Selling](modules/erpnext-selling.md) | 20 | 782 |
| erpnext | [Setup](modules/erpnext-setup.md) | 40 | 583 |
| erpnext | [Stock](modules/erpnext-stock.md) | 76 | 2045 |
| erpnext | [Subcontracting](modules/erpnext-subcontracting.md) | 13 | 443 |
| erpnext | [Support](modules/erpnext-support.md) | 11 | 168 |
| erpnext | [Telephony](modules/erpnext-telephony.md) | 5 | 40 |
| erpnext | [Utilities](modules/erpnext-utilities.md) | 4 | 24 |
| frappe | [Automation](modules/frappe-automation.md) | 16 | 182 |
| frappe | [Contacts](modules/frappe-contacts.md) | 7 | 61 |
| frappe | [Core](modules/frappe-core.md) | 106 | 1242 |
| frappe | [Custom](modules/frappe-custom.md) | 7 | 220 |
| frappe | [Desk](modules/frappe-desk.md) | 67 | 684 |
| frappe | [Email](modules/frappe-email.md) | 17 | 256 |
| frappe | [Flow](modules/frappe-flow.md) | 20 | 190 |
| frappe | [Geo](modules/frappe-geo.md) | 2 | 13 |
| frappe | [Integrations](modules/frappe-integrations.md) | 24 | 274 |
| frappe | [Printing](modules/frappe-printing.md) | 8 | 122 |
| frappe | [Studio](modules/frappe-studio.md) | 10 | 92 |
| frappe | [Website](modules/frappe-website.md) | 39 | 402 |
| frappe | [Workflow](modules/frappe-workflow.md) | 9 | 57 |

## Differences from the September source profile

Parts are grouped by current module, or by former module for a missing record. Each changed record has source paths for both revisions and its changed facts. For additions and removals the field names are in imported order. The preserved-field ordering comparison ignores insertion or removal alone.

| App | September records / fields | November records / fields | Added | Absent | Changed | Unchanged |
|---|---:|---:|---:|---:|---:|---:|
| frappe | 296 / 3448 | 332 / 3795 | 42 | 6 | 141 | 149 |
| erpnext | 534 / 10648 | 534 / 10617 | 3 | 3 | 340 | 191 |
| hrms | 160 / 2118 | 161 / 2219 | 6 | 5 | 104 | 51 |
| crm | 52 / 595 | 54 / 610 | 2 | 0 | 13 | 39 |

### frappe

| Module | Comparison | Records differing |
|---|---|---:|
| Automation | [Differences](delta/frappe-automation-01.json) | 12 |
| Contacts | [Differences](delta/frappe-contacts-01.json) | 5 |
| Core | [Differences](delta/frappe-core-01.json) | 51 |
| Custom | [Differences](delta/frappe-custom-01.json) | 7 |
| Desk | [Differences](delta/frappe-desk-01.json) | 31 |
| Email | [Differences](delta/frappe-email-01.json) | 9 |
| Flow | [Differences](delta/frappe-flow-01.json) | 20 |
| Geo | [Differences](delta/frappe-geo-01.json) | 2 |
| Integrations | [Differences](delta/frappe-integrations-01.json) | 17 |
| Printing | [Differences](delta/frappe-printing-01.json) | 7 |
| Studio | [Differences](delta/frappe-studio-01.json) | 10 |
| Website | [Differences](delta/frappe-website-01.json) | 14 |
| Workflow | [Differences](delta/frappe-workflow-01.json) | 4 |

### erpnext

| Module | Comparison | Records differing |
|---|---|---:|
| Accounts | [Differences](delta/erpnext-accounts-01.json) | 106 |
| Assets | [Differences](delta/erpnext-assets-01.json) | 20 |
| Buying | [Differences](delta/erpnext-buying-01.json) | 15 |
| CRM | [Differences](delta/erpnext-crm-01.json) | 16 |
| Communication | [Differences](delta/erpnext-communication-01.json) | 1 |
| EDI | [Differences](delta/erpnext-edi-01.json) | 2 |
| ERPNext Integrations | [Differences](delta/erpnext-erpnext-integrations-01.json) | 1 |
| Maintenance | [Differences](delta/erpnext-maintenance-01.json) | 2 |
| Manufacturing | [Differences](delta/erpnext-manufacturing-01.json) | 35 |
| Projects | [Differences](delta/erpnext-projects-01.json) | 11 |
| Quality Management | [Differences](delta/erpnext-quality-management-01.json) | 10 |
| Regional | [Differences](delta/erpnext-regional-01.json) | 4 |
| Selling | [Differences](delta/erpnext-selling-01.json) | 15 |
| Setup | [Differences](delta/erpnext-setup-01.json) | 29 |
| Stock | [Differences](delta/erpnext-stock-01.json) | 57 |
| Subcontracting | [Differences](delta/erpnext-subcontracting-01.json) | 9 |
| Support | [Differences](delta/erpnext-support-01.json) | 6 |
| Telephony | [Differences](delta/erpnext-telephony-01.json) | 4 |
| Utilities | [Differences](delta/erpnext-utilities-01.json) | 3 |

### hrms

| Module | Comparison | Records differing |
|---|---|---:|
| HR | [Differences](delta/hrms-hr-01.json) | 89 |
| Payroll | [Differences](delta/hrms-payroll-01.json) | 26 |

### crm

| Module | Comparison | Records differing |
|---|---|---:|
| Domain Enrichment | [Differences](delta/crm-domain-enrichment-01.json) | 3 |
| FCRM | [Differences](delta/crm-fcrm-01.json) | 12 |
