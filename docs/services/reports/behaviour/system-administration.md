# System Administration reports

The [structured report details](system-administration.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Database Storage Usage By Tables

Script Report. The reference record is Error Log.

The direct return positions are COLUMNS / data. [Row procedure](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/report/database_storage_usage_by_tables/database_storage_usage_by_tables.py#L14) [Declaration](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/report/database_storage_usage_by_tables/database_storage_usage_by_tables.json) [Local ordered decisions](../../../../schemas/operations/business-reading/foundation/record-runtime/operations-028.md#op-940ef57f08f80e)

## Document Share Report

Report Builder. The reference record is DocShare.

The saved view selects `DocShare.name`, `DocShare.user`, `DocShare.share_doctype`, `DocShare.share_name`, `DocShare.read`, `DocShare.write`, `DocShare.share`. Saved ordering uses `DocShare.creation` (desc). [Declaration](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/report/document_share_report/document_share_report.json)

## Permitted Documents For User

Script Report. The reference record is User. Declared inputs include `user`, `doctype`, `show_permissions`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/report/permitted_documents_for_user/permitted_documents_for_user.py#L12) [Declaration](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/report/permitted_documents_for_user/permitted_documents_for_user.json) [Local ordered decisions](../../../../schemas/operations/business-reading/foundation/record-runtime/operations-071.md#op-ac0d2c8d74f311)

## Prepared Report Analytics

Script Report. The reference record is Prepared Report. Declared inputs include `report`, `top_10`, `in_minutes`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `report_name`, `creation`, `report_end_time`, `runtime`, `peak_memory_usage`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/report/prepared_report_analytics/prepared_report_analytics.py#L12) [Declaration](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/report/prepared_report_analytics/prepared_report_analytics.json) [Local ordered decisions](../../../../schemas/operations/business-reading/foundation/record-runtime/operations-077.md#op-fd3411376f0947)

## User Activity Report

Report Builder. The reference record is User.

This saved layout is a test fixture. A site would have to register its own report to offer it to users. The saved view selects `User.name`, `User.user_type`, `User.first_name`, `User.last_name`, `User.last_active`, `Has Role.role`. Saved ordering uses `User.creation` (desc). [Declaration](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/doctype/report/user_activity_report.json)

## User Activity Report Without Sort

Report Builder. The reference record is User.

This saved layout is a test fixture. A site would have to register its own report to offer it to users. The saved view selects `User.name`, `User.user_type`, `User.first_name`, `User.last_name`, `User.last_active`, `Has Role.role`. [Declaration](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/doctype/report/user_activity_report_without_sort.json)

## User Record Type Permissions

Script Report. The reference record is User. Declared inputs include `user`, `doctype`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `user`, `doc_type`, `if_owner`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/report/user_doctype_permissions/user_doctype_permissions.py#L30) [Declaration](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/report/user_doctype_permissions/user_doctype_permissions.json) [Local ordered decisions](../../../../schemas/operations/business-reading/foundation/record-runtime/operations-101.md#op-178a5b33c23313)
