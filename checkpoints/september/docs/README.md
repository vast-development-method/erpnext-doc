# Documentation index

The human-readable specification explains business decisions, records, state transitions, calculations, authorization and operational consequences. Follow a chapter through its internal record and acceptance links to obtain both the rule and its verification cases.

[Repository overview](../README.md) · [Implementation sequence](../docs/reimplementation/sequence.md) · [Coverage and evidence](../docs/references/coverage-and-evidence.md)

## Folders

| Folder | Purpose |
|---|---|
| [Data](data/README.md) | These chapters define persistent identity, values, record relationships, effective schema construction, fresh initialization and data exchange. Read the domain model before applying the per-record field catalog. |
| [Domains](domains/README.md) | The chapters below form one integrated application. A workflow can update commercial progress, inventory valuation, financial settlement and employee entitlements in the same business transaction. The cross-domain chapter establishes those shared consequences. |
| [Interfaces](interfaces/README.md) | These contracts define user journeys, authorized service operations, transport profiles, reports, exports and external counterpart boundaries. Literal transport conventions belong to compatibility adapters; business decisions belong to the shared domain contracts. |
| [Overview](overview/README.md) | Start with scope, architecture and the business compatibility map. These documents explain what the replacement must preserve and how the detailed contracts fit together. |
| [References](references/README.md) | These documents define specification quality, measured coverage, verification meaning and honest limits. An internal reference is navigation to a supplied definition; it does not replace an explanation of the business rule. |
| [Reimplementation](reimplementation/README.md) | Use the implementation sequence and conformance profiles to build and qualify the system in dependency order. Each stage names the records, effects and acceptance obligations needed before advancing. |
| [Runtime](runtime/README.md) | These chapters specify shared execution semantics: document lifecycle, transaction boundaries, identity, permissions, background work and controlled extensions. Domain-specific calculations inherit these rules unless a chapter states a precise exception. |
