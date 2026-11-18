# Runtime

These chapters specify shared execution semantics: document lifecycle, transaction boundaries, identity, permissions, background work and controlled extensions. Domain-specific calculations inherit these rules unless a chapter states a precise exception.

[Parent index](../README.md)

## Definitions

| Entry | Contents |
|---|---|
| [Background work and consistency](background-work-and-consistency.md) | Business work can finish within a request or continue through a tracked background operation. The observable contract includes when work becomes eligible, which… |
| [Decision contract interpretation](decision-contract-interpretation.md) | This chapter defines how to read the ordered decision catalogs as language-neutral behavioral structures. It explains every retained value kind, action, operator,… |
| [Document lifecycle and transactions](document-lifecycle-and-transactions.md) | The transaction document is the common unit of business control. Its stored state is separate from descriptive statuses such as partly delivered, overdue, paid,… |
| [Extensibility and configuration](extensibility-and-configuration.md) | Extensibility is part of the application model. The reviewed system combines declarative record definitions with executable business behavior, event handlers,… |
| [Identity, permissions, and tenancy](identity-permissions-and-tenancy.md) | Identity establishes the acting user and tenant. Permission decides whether that actor may perform a particular action on a particular record and field. Workflow,… |
