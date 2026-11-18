# Shared services and administration

A purchasing manager can approve an order while a warehouse operator can see only its receiving fields. The approval can schedule work, change an assignment and notify a supplier in another language. The services below define who can perform each step, which effects commit together and how to distinguish a delayed effect from a rejected one.

| Business question | Specification |
|---|---|
| Who may see a header, an owned row, a masked value, a report or an attachment? | [Identity, permissions and tenant isolation](identity-permissions-and-tenancy.md) and [requests and records](record-services.md) |
| What distinguishes an omitted value, a clear, a restricted edit and a cancellation? | [Persistence and value semantics](persistence-identity-and-values.md) and [record lifecycle, transaction boundaries and concurrency](document-lifecycle-and-transactions.md) |
| Which commands exist, how are inputs interpreted and what survives a partial failure? | [Business operation directory](operations/README.md), [service contracts](service-contracts.md) and [request and response contracts](remote-transport-contracts.md) |
| How do assignment, workflow approval, deferred execution and retries interact? | [Approval, assignment and dispatch](work-dispatch.md), [background work and consistency](background-work-and-consistency.md) and [event automation, waits and recovery](automation.md) |
| How do we configure the enterprise, load opening balances or restore a tenant? | [Effective configuration](extensibility-and-configuration.md), [initialisation and data exchange](fresh-initialisation-and-data-exchange.md) and [tenant configuration and recovery](site-operations.md) |
| How do users discover and act on the same transactions? | [Navigation and destinations](navigation/README.md), [operator workspaces](desktop-workflows.md), [interactive product and sales forms](embedded-client-behaviors.md), [field change examples](form-examples.json) and [ordered setup tasks](setup-tasks.json) |
| Who selects the screen, recipient and issued-document languages? | [Language, currency and document issuance](languages-and-issuance.md) and [notice delivery examples](notice-examples.json) |
| How are reports filtered, prepared, exported and reconciled? | [Report directory](reports/README.md), [execution and exports](reporting-and-exports.md), [attachments and prepared results](files-and-reports.md) and [six reports after settlement](settlement-reports.md) |
| How do connected providers, master identifiers and published media interact with internal records? | [External integrations](external-integrations.md) and [bulk identity changes and video statistics](identity-and-media.md) |

## Structured rules

[Decision tables](decision-tables.json) describe ordered alternatives for record access, edit conflicts, admission, work scheduling, approval, retries, duplicate event claims, report stalls and attachment reuse. Evaluate each table against its input contract, in sequence. The first rule whose conditions all match supplies the outcome. An empty condition list is the fallback. [Boundary examples](decision-examples.json) give exact inputs and expected results.

The [configuration map](configuration-map.json) associates business document types with the settings that affect them. A missing default means the row supplies no declared initial value. Read defaults together with the active tenant settings. The [indicator definitions](indicator-definitions.json) specify chart or measure, aggregation, time basis, fixed filters and operator-specific defaults. A record's visibility in either directory does not confer the right to read its underlying transactions.
