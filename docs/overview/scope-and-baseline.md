# Scope and source baseline

## Reference boundary

Four source archives define the reference snapshot. Archive content digests and embedded revision identifiers appear in the [source snapshot catalog](../../schemas/traceability/source-snapshot.json). These revisions are fixed evidence; a later moving development branch is not interchangeable with them.

The foundation, enterprise, and workforce snapshots identify themselves as development version 17.0.0. The relationship snapshot identifies itself as development version 2.0.0 and declares a foundation compatibility interval ending at development version 17.0.0. These are development snapshots, not a certified combination of stable releases. Their declared intervals can overlap without proving that every combined operation has been exercised successfully.

| Source pack | Responsibility in this specification |
|---|---|
| Foundation | Record metadata, persistence, identity, permission evaluation, transactions, workflows, communication, jobs, reports, customisation |
| Enterprise | Accounting, parties, products, purchasing, selling, inventory, manufacturing, assets, projects, support and regional behaviours |
| Workforce | Employment, attendance, leave, recruitment, payroll, benefits, expenses and employee-specific integration |
| Relationships | Lead and deal workspaces, contacts, activities, enrichment, external lead synchronisation and commercial integration |

Pack names are evidence partitions, not required deployment units or product modules. The intended application presents a coherent domain model across them.

## Current behaviour

Include reachable contemporary business controllers, service functions, metadata, user interfaces, reports, tests, scheduled operations, and current extension hooks. Preserve current defaults and selectable policies even when another policy is newer. A document amendment after cancellation is current business behaviour; it is not a historical database migration.

Exclude historical upgrade patches, removed-feature shims, obsolete transport generations where superseded and unused, development scaffolding, build tooling, and hosting recipes from the replacement requirements. Retain their inventory entries with an explicit classification so exclusion can be audited. Static classification alone cannot prove that a supposedly obsolete function is unreachable; domain review must check callers where the distinction affects behaviour.

## Included functional scope

Financial accounting is central: chart structure, company and party currencies, reporting currency where supported, journals, receivables, payables, payments, bank reconciliation, advances, budgets, deferred recognition, closing, consolidation, taxes, credit, assets and depreciation. Operational scope includes products, variants, units, packaging, purchasing, sales, delivery, replenishment, stock reservations, serial and batch identities, valuation, manufacturing, subcontracting and quality. Workforce and relationship capabilities share parties, people, activities, communication, projects and financial consequences.

The source also contains a general application foundation: custom record definitions, form behaviour, permission policies, approval workflows, assignments, notifications, printing, data import and export, public pages, files and background operations. These capabilities matter even when a future implementation supplies them through a different foundation.

## Explicit boundaries

Historical migration from the reference database is not required. A new implementation still needs fresh-install data initialisation, opening balances, ordinary business data import, backup and restoration semantics, and safe evolution of its own records; the implementation may choose its own mechanism.

Specific servers, operating systems, container arrangements, language packages, task runners, database brands and deployment commands are not requirements. Transaction isolation, durable records, monetary precision, permission enforcement and restart-safe business processing remain requirements because they affect outcomes.

Optional applications referenced by a hook but absent from the supplied source are integration boundaries. Their internals cannot be inferred as implemented merely because a linking field exists. Lending is one such boundary. Detailed jurisdictional compliance outside the supplied regional logic likewise requires an additional authoritative source and its own acceptance set.

The possible future implementation platform is deliberately absent from the blueprint. Its existing architecture neither narrows this scope nor changes the reference behaviour.
