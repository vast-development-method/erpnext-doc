# Document-specific lifecycle rules

A stock movement can update a work order and its reservations before posting inventory. A sales invoice can post without inventory effects. Use the [entity index](entity-index.tsv) to find the rules for a particular business record and its qualified [schema definition](../../schema/README.md). The [worked transitions](examples.md) follow sales invoices, stock movements, payments, posted sales order edits and master-data merges.

## How a stage runs

1. Resolve the tenant, record, effective actor, requested transition, stored edit token and applicable role and field grants. The [shared record lifecycle](../services/document-lifecycle-and-transactions.md) specifies the sequence for creating, saving, posting, correcting, cancelling, discarding or deleting a record.
2. For the requested stage, select the entity's own stage if present. Otherwise follow its **inherited stages** to the named [shared policy](shared-policies.json) or to the named parent entity. The **policy order** gives precedence, nearest first. When a stage explicitly continues with the next inherited policy, resume at that point. Overriding a stage does not automatically perform every ancestor's actions. An empty own stage deliberately carries no record-specific responsibilities for that stage.
3. Read the **responsibilities** in their listed order. They describe selected business operations, field writes, validation failures and early returns. A scope identifies a guard, repetition or recovery path. Where several conditions form a complex expression, “conditional branch” marks the point at which behaviour can diverge. A validation can stop subsequent steps. A named service can find no eligible rows or roll back even when its entry is reached. Separate alternatives listed in order do not denote cumulative effects.
4. Apply the [attached actions](attached-actions.json) for the event. These can add company restrictions, period closure, service-level tracking, commercial links, stock progress and regional tax handling to a record. The register includes shared business actions on platform-owned records; those records retain their own schema identity. Region-specific actions evaluate the applicable business profile. Global validation applies to record saves, subject to the authority and scope of the particular rule.
5. After-store and after-post stages run inside the enclosing transaction unless an operation specifies an independent commit or deferred job. A later guard can roll back earlier work. A notification or queued recalculation can have a different completion boundary from the posted document.

A record with no special stage uses its common lifecycle, ownership and relationship rules. An owned line typically persists through its parent. A hierarchy additionally maintains parent membership and nested ordering; a published-content record may also affect public visibility. A structured import acquires the per-payload commit and retry rules in [data exchange](../services/fresh-initialisation-and-data-exchange.md).

## Business areas

| Area | Entities |
|---|---:|
| [Accounting](accounting.json) | 191 |
| [Administration](administration.json) | 4 |
| [Batch Processing](batch-processing.json) | 2 |
| [Business Correspondence](business-correspondence.json) | 2 |
| [Business Integrations](business-integrations.json) | 1 |
| [Customer Support](customer-support.json) | 11 |
| [Electronic Document Exchange](electronic-document-exchange.json) | 2 |
| [Fixed Assets](fixed-assets.json) | 26 |
| [Inventory](inventory.json) | 76 |
| [Maintenance](maintenance.json) | 5 |
| [Manufacturing](manufacturing.json) | 50 |
| [Organization](organization.json) | 40 |
| [Procurement](procurement.json) | 20 |
| [Projects](projects.json) | 15 |
| [Quality Management](quality-management.json) | 16 |
| [Regional Accounting](regional-accounting.json) | 5 |
| [Sales](sales.json) | 20 |
| [Sales Relationships](sales-relationships.json) | 28 |
| [Self Service](self-service.json) | 2 |
| [Subcontracting](subcontracting.json) | 13 |
| [Telephony](telephony.json) | 5 |

The register contains 534 core business entities, including 77 that declare a posting lifecycle. 222 entities declare a total of 669 specialized stages. 38 entities select at least one specialized inherited stage. A single entity can appear in both groups. The area tables describe business responsibilities at stage boundaries. A listing establishes dispatch and ordering for the named operations; it does not establish every downstream calculation, exception, concurrency outcome or deployment-specific extension.
