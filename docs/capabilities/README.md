# Optional business capabilities

The [capability directory](directory.md) organizes 366 distinct business purposes. A bank feed, for example, supplies statement observations. It has a different responsibility from a payment instruction, its authorization and its allocation to an invoice. The directory links applicable purposes to record events and worked decisions.

[Language selection, item text and issued documents](language-and-issuance.md) specifies language precedence, translated product rows, mixed-language documents, immutable issued renditions and retry behaviour.

[Activities that affect posting](optional-posting.md) follows livestock feed into valuation, crew production into weekly payroll, purchasing into price controls, and warehouse transfers into gate documents and store availability.

[Optional record contracts](records/README.md) lists the entity, field, relationship and permission definitions. [Optional services and reports](functions/README.md) lists callable operations, inputs, access boundaries and report definitions.

[Commerce and regional exchanges](trade-exchanges.md) traces carts through order acceptance, carrier quotes through booking, direct donations through settlement, and regional invoice and reporting decisions.

## Worked decisions

Each English chapter defines the workflow and a testable acceptance case. The other language columns present the operator objective, workflow and worked case in that language.

| Workflow | English | Afrikaans | Deutsch | 简体中文 |
|---|---|---|---|---|
| Accounting and tax | [Workflow and case](guides/accounting.md) | [Praktykgevalle](guides/af/accounting.md) | [Beispielfälle](guides/de/accounting.md) | [业务示例](guides/zh-Hans/accounting.md) |
| Banking and treasury | [Workflow and case](guides/banking.md) | [Praktykgevalle](guides/af/banking.md) | [Beispielfälle](guides/de/banking.md) | [业务示例](guides/zh-Hans/banking.md) |
| Customer communications | [Workflow and case](guides/communications.md) | [Praktykgevalle](guides/af/communications.md) | [Beispielfälle](guides/de/communications.md) | [业务示例](guides/zh-Hans/communications.md) |
| Document preparation and signing | [Workflow and case](guides/documents.md) | [Praktykgevalle](guides/af/documents.md) | [Beispielfälle](guides/de/documents.md) | [业务示例](guides/zh-Hans/documents.md) |
| Data transfer and entry | [Workflow and case](guides/data.md) | [Praktykgevalle](guides/af/data.md) | [Beispielfälle](guides/de/data.md) | [业务示例](guides/zh-Hans/data.md) |
| Service and project operations | [Workflow and case](guides/operations.md) | [Praktykgevalle](guides/af/operations.md) | [Beispielfälle](guides/de/operations.md) | [业务示例](guides/zh-Hans/operations.md) |
| People and payroll | [Workflow and case](guides/people.md) | [Praktykgevalle](guides/af/people.md) | [Beispielfälle](guides/de/people.md) | [业务示例](guides/zh-Hans/people.md) |
| Selling and customer management | [Workflow and case](guides/sales.md) | [Praktykgevalle](guides/af/sales.md) | [Beispielfälle](guides/de/sales.md) | [业务示例](guides/zh-Hans/sales.md) |
| Purchasing and inventory | [Workflow and case](guides/supply.md) | [Praktykgevalle](guides/af/supply.md) | [Beispielfälle](guides/de/supply.md) | [业务示例](guides/zh-Hans/supply.md) |
| Workspace and permissions | [Workflow and case](guides/workspace.md) | [Praktykgevalle](guides/af/workspace.md) | [Beispielfälle](guides/de/workspace.md) | [业务示例](guides/zh-Hans/workspace.md) |

## Implementation detail

The [extension transaction chapters](../rebuild/extensions/README.md) connect salary deductions to loan repayment, fee schedules to invoicing, customer carts to stock and settlement, and statutory submissions to their external acknowledgements. The [support, analytics, document and learning contracts](../rebuild/companion/README.md) identify the owner of each record when these services run alongside the core.

Each English worked decision links to the profile that documents its implementation evidence, source-specific variations and unresolved questions. The [declaration catalog](../rebuild/marketplace-model/README.md) locates record fields, permissions, services and reports. The [event and language catalog](../rebuild/marketplace-workflows/README.md) locates handlers for each record event and the available message resources.

## Scope of the contracts

The 69 worked cases specify outcomes for a selected configuration. Record-event entries identify possible interaction points. A shared event does not establish which optional functions are enabled, their execution order or whether an external organization accepted a transaction. Distinguish document submission, financial posting, remote acknowledgement and final settlement using their own identities and states. Regional capabilities require jurisdiction-specific rule profiles, reporting periods and the applicable authority’s acceptance conditions.
