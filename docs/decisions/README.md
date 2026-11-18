# When a business operation must refuse a request

Use this directory when deciding whether a command may proceed. Each row names the operation and the business condition that refuses it. The linked logical record defines its fields, ownership and declared grants. Evaluate the business condition as part of the operation even when the actor has the required grant. An account’s permission to submit a purchase document, for example, does not authorize a subcontract receipt on a future posting date.

The directory covers selected explicit rejection conditions for the records listed below. Each row is specific to its operation. Meeting one condition for acceptance does not bypass the remaining rules for that operation. A date equality permitted by one comparison can still fail a different test. The underlying transaction chapters cover posting consequences, recalculation, state changes and recovery. The tables here do not prescribe universal rollback or external delivery guarantees.

| Subject | Logical records in section | Refusal conditions |
|---|---:|---:|
| [Customers, purchasing and commercial commitments](customer-and-commercial.md) | 9 | 30 |
| [Production, subcontracting and supply commitments](production-and-supply.md) | 6 | 32 |
| [Service, maintenance and quality assurance](service-and-assurance.md) | 13 | 28 |
| [Inventory, warehouse controls and dispatch](inventory-and-carriage.md) | 10 | 23 |
| [Asset custody, maintenance and project time](assets-and-projects.md) | 7 | 25 |
| [Accounting controls, tax and treasury](accounting-and-treasury.md) | 11 | 28 |
| [Organization, approval and localized transactions](organization-and-authority.md) | 7 | 22 |

The tables contain 188 conditions across 62 distinct logical records. A record can appear in more than one section when different business operations use it.

[Financial and commercial events](../transactions/README.md) · [Physical operations](../operations/README.md) · [People and service workflows](../people-and-services/README.md) · [Logical entity index](../../schema/index.tsv)
