# Scope and source baseline

## Specification boundary

The [specification baseline](../../schemas/traceability/specification-baseline.json) defines the fixed application boundary. Every business rule must be available as explanatory text, a record definition, an ordered decision, a calculation or an acceptance case within this repository. No external archive or previous conversation is required to interpret these contracts.

| Capability group | Responsibility |
|---|---|
| Shared application capabilities | Metadata, persistence, identity, permissions, transactions, workflow, communication, jobs, reports and customization |
| Enterprise business capabilities | Accounting, parties, products, purchasing, selling, inventory, manufacturing, assets, projects, support and regional behavior |
| Workforce capabilities | Employment, attendance, leave, recruitment, payroll, benefits, expenses and employee-specific integration |
| Customer relationship capabilities | Leads, deals, contacts, activities, enrichment and commercial integration |

These are navigation groups within one logical application. They do not require separate installations, duplicated parties or independently inconsistent accounting systems. Similar records remain distinct when they have different ownership, states, permission boundaries or financial consequences.

The baseline describes a development snapshot. Compatibility findings are documented as actual decision branches; integrated execution and replacement conformance are separate qualification gates. Future revisions enter the specification through explicit contract changes, not an assumption that a moving upstream version is equivalent.

## Current behaviour

Include reachable contemporary business record behaviors, service operations, metadata, user interfaces, reports, tests, scheduled operations, and current extension hooks. Preserve current defaults and selectable policies even when another policy is newer. A document amendment after cancellation is current business behaviour; it is not a historical database migration.

Exclude historical upgrade patches, removed-feature shims, obsolete transport generations where superseded and unused, development scaffolding, build tooling, and hosting recipes from the replacement requirements. Retain their inventory entries with an explicit classification so exclusion can be audited. Static classification alone cannot prove that a supposedly obsolete function is unreachable; domain review must check callers where the distinction affects behaviour.

## Included functional scope

Financial accounting is central: chart structure, company and party currencies, reporting currency where supported, journals, receivables, payables, payments, bank reconciliation, advances, budgets, deferred recognition, closing, consolidation, taxes, credit, assets and depreciation. Operational scope includes products, variants, units, packaging, purchasing, sales, delivery, replenishment, stock reservations, serial and batch identities, valuation, manufacturing, subcontracting and quality. Workforce and relationship capabilities share parties, people, activities, communication, projects and financial consequences.

The application also contains a general application foundation: custom record definitions, form behaviour, permission policies, approval workflows, assignments, notifications, printing, data import and export, public pages, files and background operations. These capabilities matter even when a future implementation supplies them through a different foundation.

## Explicit boundaries

Historical migration from the reference database is not required. A new implementation still needs fresh-install data initialisation, opening balances, ordinary business data import, backup and restoration semantics, and safe evolution of its own records; the implementation may choose its own mechanism.

Specific servers, operating systems, container arrangements, language packages, task runners, database brands and deployment commands are not requirements. Transaction isolation, durable records, monetary precision, permission enforcement and restart-safe business processing remain requirements because they affect outcomes.

Optional applications referenced by a hook but absent from the defined baseline are integration boundaries. Their internals cannot be inferred as implemented merely because a linking field exists. Lending is one such boundary. Detailed jurisdictional compliance outside the supplied regional logic likewise requires an additional authoritative source and its own acceptance set.

The possible future implementation platform is deliberately absent from the blueprint. Its existing architecture neither narrows this scope nor changes the reference behaviour.
