# Enterprise scope and behavioural baseline

## Specification boundary

The [business map](business-compatibility-map.md) assigns each workflow to its accountable domain. Use the [logical records](../../schema/README.md), [ordered decisions](../../schemas/operations/README.md), [calculations](../calculations/README.md) and [posting examples](../transactions/README.md) to follow an operation from input to durable effect. The [coverage register](../references/coverage-and-evidence.md) identifies what has been inventoried, reviewed or executed.

| Capability group | Responsibility |
|---|---|
| Shared application capabilities | Metadata, persistence, identity, permissions, transactions, workflow, communication, jobs, reports and customization |
| Enterprise business capabilities | Accounting, parties, products, purchasing, selling, inventory, manufacturing, assets, projects, support and regional behavior |
| Workforce capabilities | Employment, attendance, leave, recruitment, payroll, benefits, expenses and employee-specific integration |
| Customer relationship capabilities | Leads, deals, contacts, activities, enrichment and commercial integration |

These are navigation groups within one logical application. They do not require separate installations, duplicated parties or independently inconsistent accounting systems. Similar records remain distinct when they have different ownership, states, permission boundaries or financial consequences.

Where company policy, enabled capabilities or jurisdiction select different outcomes, the relevant chapter identifies the selector, default and affected records. A proposed improvement has its own acceptance result.

## Current behaviour

Include reachable contemporary business record behaviors, service operations, metadata, user interfaces, reports, tests, scheduled operations, and current extension hooks. Preserve current defaults and selectable policies even when another policy is newer. A document amendment after cancellation is current business behaviour; it is not a historical database migration.

Exclude historical upgrade patches, removed-feature shims, obsolete transport generations where superseded and unused, development scaffolding, build tooling, and hosting recipes from the replacement requirements. Retain their inventory entries with an explicit classification so exclusion can be audited. Static classification alone cannot prove that a supposedly obsolete function is unreachable; domain review must check callers where the distinction affects behaviour.

## Included functional scope

Financial accounting is central: chart structure, company and party currencies, reporting currency where supported, journals, receivables, payables, payments, bank reconciliation, advances, budgets, deferred recognition, closing, consolidation, taxes, credit, assets and depreciation. Operational scope includes products, variants, units, packaging, purchasing, sales, delivery, replenishment, stock reservations, serial and batch identities, valuation, manufacturing, subcontracting and quality. Workforce and relationship capabilities share parties, people, activities, communication, projects and financial consequences.

The application also contains a general application foundation: custom record definitions, form behaviour, permission policies, approval workflows, assignments, notifications, printing, data import and export, public pages, files and background operations. These capabilities matter even when a future implementation supplies them through a different foundation.

## Explicit boundaries

Historical migration from the reference database is not required. A new implementation still needs fresh-install data initialisation, opening balances, ordinary business data import, backup and restoration semantics, and safe evolution of its own records; the implementation may choose its own mechanism.

Specific servers, operating systems, container arrangements, language packages, task runners, database brands and deployment commands are not requirements. Transaction isolation, durable records, monetary precision, permission enforcement and restart-safe business processing remain requirements because they affect outcomes.

The boundary of each optional service depends on which operations the specification describes. For example, [employee lending](../people-and-services/lending.md) specifies the payroll link, due-date selection, booked repayment and cancellation. A provider's private underwriting decisions require their own contract. Regional reporting also depends on the applicable authority's requirements.

The possible future implementation platform is deliberately absent from the blueprint. Its existing architecture neither narrows this scope nor changes the reference behaviour.
