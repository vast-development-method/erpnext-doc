# ERP coverage by release and business area

Use this register to decide what evidence applies to a rebuild. It covers every module named by the November ERPNext release, with shared controllers and infrastructure in a separate row. The release has **534 canonical ERPNext record types and 10,617 fields**. The November field dictionary also covers **332 Frappe record types**. The [framework directory](../model/INDEX.md), [navigation catalog](../source-coverage/README.md) and [platform contracts](../platform/README.md) cover the shared application foundation.

## Read by business area

| Area | Implementation chapter | Review a business outcome |
|---|---|---|
| Accounts | [Trading ledgers, tax, exchange, ageing, collection, statements and bank reconciliation](../finance/README.md) | Post and reverse the twelve vouchers; reconcile the six financial reports. |
| CRM | [Lead, opportunity and party conversion](../industry/crm-to-order.md) | Preserve CRM source identity through the ERP sales handoff. |
| Buying | [Supplier quotes, scorecards, order quantities and receipts](../operations/sourcing.md) | Keep an invitation, supplier response, ordered row and received quantity linked. |
| Projects | [Timesheets, project progress, stock consumption, billing and margin](project-costing.md) | Reconcile time, materials and billing for work produced and delivered under one project. |
| Selling | [Quotation, pricing, approval, orders, fulfilment and billing](../business/order-promises.md) | Follow row-level promises, delivery and invoice progress under partial fulfilment. |
| Setup | [Master defaults, item policy, shared parties, units and site configuration](../configuration/README.md) | Compare two installations with different effective grants, fields and defaults. |
| Manufacturing | [BOM, planning, shop orders, job cards and secondary output](../production/README.md) | Compare consumed components, finished goods and recoveries with the stock ledger. |
| Stock | [Receipt, putaway, reservation, pick, pack, trip and valuation](../warehouse-fulfilment/README.md) | Follow one batch through split allocation and a partial delivery. |
| Support | [Issue, appointment, SLA selection and service clock](../business/appointments-and-service.md) | Re-evaluate a service agreement on a new versus existing ticket. |
| Utilities | [Rename, merge, video identity and statistics refresh](record-rename-and-video.md) | Keep committed rows on partial failure and preserve provider identity across display languages. |
| Assets | [Capitalization, depreciation, repair, composite assets and disposal](../operations/capitalization.md) | Reconcile components and services to the capitalized value and subsequent schedules. |
| Portal | [Website users, contact-to-party identity and scoped transactions](../business/batch-portal-and-codes.md) | Repeat portal account creation for a user already linked to a party. |
| Maintenance | [Visit scheduling, delivered serial, warranty and contract expiry](../business/appointments-and-service.md) | Check boundary dates and recompute serial coverage when a contract is cancelled. |
| Regional | [Country setup, tax selection and optional regional applications](../extensions/regions-donation-operations.md) | Resolve the country rule, dependency, version and effective company settings separately. |
| ERPNext Integrations | [Institution connections, bank account binding, statement import and recovery](bank-feed.md) | Reconcile a movement imported twice, a rejected currency and an advanced import date. |
| Quality Management | [Inspection limits, quality reviews and corrective actions](../operations/quality.md) | Compare measurement outcomes and blocking policy at purchase or production. |
| Communication | [Communication media, employee groups and availability windows](service-routing.md) | Choose eligible recipients at a shift boundary and on a disabled medium. |
| Telephony | [Call transfer, caller identity, service history and agent summaries](service-routing.md) | Transfer an active call and preserve the agent and party links on the same log. |
| Bulk Transaction | [Batch document conversion, limits, job outcomes and retries](../business/batch-portal-and-codes.md) | Record per-source success or failure and retry only eligible work. |
| Subcontracting | [Supply raw material, receive output, recognize service and material cost](../operations/subcontract-cost.md) | Reconcile supplied, unused and consumed quantities to receipt value. |
| EDI | [Publisher code lists, common-code versions and column import](../business/batch-portal-and-codes.md) | Use the publisher code and version independent of its translated description. |
| Shared and repository | [Controllers, cross-module services and repository-level declarations](../surfaces/README.md) | Trace document effects through shared finance and inventory controllers. |

## Measure the change between editions

The November tree has **11,007 in-scope ERPNext server function definitions** under the counting rules below. Of these, 4,199 match their September bodies structurally, 3,289 changed and 3,519 are new at their qualified paths. Another 2,070 September definitions are absent at those paths in November. A newly introduced or renamed operation needs a release-specific reading before its earlier decision contract can be reused. Even unchanged bodies may call changed services.

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

## Depth of evidence

- **September baseline.** Browse the [business chapters](../../../checkpoints/september/docs/domains/README.md) and [catalog access guide](../../../checkpoints/september/catalog-access.md). The [operation lookup corrections](../checkpoint-corrections/README.md) identify the missing historical stock contracts and the duplicate entries.
- **November release.** The [purchase-to-cash run](../live/README.md), [stock tests](../stock-live/README.md), [warehouse fulfilment tests](../warehouse-fulfilment/README.md), [reference workflow results](reference-tests.md), [platform observations](../platform-live/README.md) and [restoration experiment](../recovery-live/README.md) identify which decisions were exercised on a configured system. Other chapters mark source interpretations and derived acceptance cases.
- **Installed applications.** The [marketplace register](../marketplace-model/README.md) covers the dated set of 398 listings. The [source and workflow profiles](../marketplace-workflows/README.md) and [69 multilingual guides](../marketplace-guides/README.md) describe the evidence available for individual apps. Exact installed releases, private changes and combinations need the applicable installation profile.
- **Independent implementation.** The [20 qualification gates](../qualification.json) specify how to compare a replacement. The pinned reference runs establish expected outcomes for the recorded cases. The comparison of a future replacement remains open.
