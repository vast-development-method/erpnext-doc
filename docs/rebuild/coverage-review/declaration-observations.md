# Source declaration comparison

This evidence explains how source declarations were counted and compared. The [business-area register](README.md) and [entity dictionary](../../../schema/README.md) give the behavior and record contracts to implement. A path or syntax change alone establishes neither a new feature nor a selectable configuration. The [entity cross-reference](entity-cross-reference.tsv) joins each scoped definition to its reviewed declaration.

The November tree has **11,007 in-scope ERPNext server function definitions** under the counting rules below. Of these, 4,199 match their September bodies structurally, 3,289 changed and 3,519 are new at their qualified paths. Another 2,070 September definitions are absent at those paths in November. A moved, renamed or changed definition requires matching its inputs, effects and callers before reusing a decision contract. Even unchanged bodies may call changed services.

| Module and field dictionary | Record types / fields | Reports / exposed operations | Nov functions | Changed / added / removed definitions |
|---|---:|---:|---:|---|
| [Accounts](../model/modules/erpnext-accounts.md) | 191 / 3,419 | 57 / 230 | 2,924 | [805 / 545 / 434](release-changes/accounts.tsv) |
| [CRM](../model/modules/erpnext-crm.md) | 28 / 359 | 9 / 26 | 344 | [112 / 112 / 26](release-changes/crm.tsv) |
| [Buying](../model/modules/erpnext-buying.md) | 20 / 786 | 10 / 31 | 331 | [121 / 108 / 55](release-changes/buying.tsv) |
| [Projects](../model/modules/erpnext-projects.md) | 15 / 239 | 5 / 32 | 382 | [77 / 215 / 6](release-changes/projects.tsv) |
| [Selling](../model/modules/erpnext-selling.md) | 20 / 782 | 23 / 64 | 551 | [164 / 224 / 133](release-changes/selling.tsv) |
| [Setup](../model/modules/erpnext-setup.md) | 40 / 583 | 0 / 36 | 408 | [129 / 53 / 21](release-changes/setup.tsv) |
| [Manufacturing](../model/modules/erpnext-manufacturing.md) | 50 / 1,028 | 21 / 95 | 1,159 | [344 / 555 / 688](release-changes/manufacturing.tsv) |
| [Stock](../model/modules/erpnext-stock.md) | 76 / 2,045 | 52 / 164 | 2,666 | [837 / 987 / 606](release-changes/stock.tsv) |
| [Support](../model/modules/erpnext-support.md) | 11 / 168 | 4 / 10 | 161 | [51 / 39 / 4](release-changes/support.tsv) |
| [Utilities](../model/modules/erpnext-utilities.md) | 4 / 24 | 1 / 7 | 105 | [39 / 40 / 4](release-changes/utilities.tsv) |
| [Assets](../model/modules/erpnext-assets.md) | 26 / 421 | 3 / 41 | 471 | [138 / 139 / 40](release-changes/assets.tsv) |
| [Portal](../model/modules/erpnext-portal.md) | 2 / 2 | 0 / 0 | 5 | 0 / 0 / 0 |
| [Maintenance](../model/modules/erpnext-maintenance.md) | 5 / 96 | 1 / 5 | 50 | [22 / 16 / 1](release-changes/maintenance.tsv) |
| [Regional](../model/modules/erpnext-regional.md) | 5 / 34 | 4 / 3 | 154 | [52 / 36 / 1](release-changes/regional.tsv) |
| [ERPNext Integrations](../model/modules/erpnext-erpnext-integrations.md) | 1 / 9 | 0 / 7 | 21 | [8 / 1 / 3](release-changes/erpnext-integrations.tsv) |
| [Quality Management](../model/modules/erpnext-quality-management.md) | 16 / 93 | 1 / 3 | 30 | [12 / 11 / 1](release-changes/quality-management.tsv) |
| [Communication](../model/modules/erpnext-communication.md) | 2 / 12 | 0 / 0 | 2 | [0 / 2 / 0](release-changes/communication.tsv) |
| [Telephony](../model/modules/erpnext-telephony.md) | 5 / 40 | 0 / 1 | 34 | [9 / 15 / 0](release-changes/telephony.tsv) |
| [Bulk Transaction](../model/modules/erpnext-bulk-transaction.md) | 2 / 15 | 0 / 0 | 13 | [3 / 4 / 0](release-changes/bulk-transaction.tsv) |
| [Subcontracting](../model/modules/erpnext-subcontracting.md) | 13 / 443 | 3 / 19 | 176 | [50 / 73 / 9](release-changes/subcontracting.tsv) |
| [EDI](../model/modules/erpnext-edi.md) | 2 / 19 | 0 / 2 | 33 | [9 / 7 / 0](release-changes/edi.tsv) |
| Shared and repository | 0 / 0 | 0 / 63 | 987 | [307 / 337 / 38](release-changes/shared-and-repository.tsv) |

The change links open tab-separated tables. Each row retains the source file, qualified operation, change type and declaration line in each applicable revision. A dash means the definition is absent at that path in that edition. Select the source revision before looking up the line. [September source](https://github.com/frappe/erpnext/tree/4671d1a6658107df592f88f8eb7485847e3d7ae2) · [November source](https://github.com/frappe/erpnext/tree/886ab6ae187244e7f1b852393384ab6019d56264) · [Machine-readable counts](module-counts.json)

**Counting rules.** The file census includes every tracked blob in each upstream revision, assigned by its release module directory or to the shared/repository group. The function comparison reads application server modules under the ERPNext package, excluding test, fixture and patch directories, test modules and test configuration. It includes methods and nested functions. Matching keys use file path and qualified name, with occurrence order for repeated definitions. It compares syntax trees without source positions. Whitespace-only changes disappear, while changed docstrings count and file moves may appear as removal and addition. Record counts use canonical record JSON and were joined by source blob, record name and complete field order against the release dictionary. Report and exposed-operation counts use the independent release surface shards. These measures cannot be added to derive a percentage of implemented business behaviour.

## Entity and field interpretation

The [entity cross-reference](entity-cross-reference.tsv) joins **866** business and shared platform declarations and **695** extension declarations to the field dictionary. Identities are qualified by their source path as well as their name, so identically named records in different scopes have distinct bindings. Fourteen more rows point to the comparisons that preserve their earlier layout. The [compatibility field register](compatibility-fields.tsv) resolves each of the 155 retained fields on live records to the specific removed declaration. The original grants, constraints and values of those fields remain available for interpreting prior data.

For workforce and customer relationships, the field dictionary retains 319 applicable conditional form rules and incorporates 29 additional rules from the declared fields. An earlier company requirement on the leave control panel is preserved in the [field-level comparison](../model/delta/hrms-hr-01.json), under **Leave Control Panel → company → mandatory_depends_on**. The current form has no such conditional requirement. These rules govern form behavior. Server-side permissions and posting validation belong to the relevant operations.
