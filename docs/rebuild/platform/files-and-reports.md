# Files and reporting

The [Files and reporting](../../services/files-and-reports.md) chapter defines the business rules, calculations and worked outcomes.

## Attachment identity and access

- [Attachment validation](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/doctype/file/file.py#L104-L282)
- [Move and compensation](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/doctype/file/file.py#L295-L437)
- [Controller and listing policy](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/doctype/file/file.py#L1088-L1180)

## Prepared results

- [Resolve and authorize](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/desk/query_report.py#L30-L66)
- [Explicit result gate](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/desk/query_report.py#L283-L350)
- [Reference filter gate](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/desk/query_report.py#L1225-L1255)
- [Preparation worker](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/doctype/prepared_report/prepared_report.py#L66-L206)
- [Lookup, expiry and download](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/doctype/prepared_report/prepared_report.py#L208-L391)
