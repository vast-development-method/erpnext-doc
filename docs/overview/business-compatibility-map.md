# Business compatibility map

The map groups capabilities by observable business responsibility. A chapter is a reviewed specification entry point, not a claim that every source branch or external integration has been executed. Use its evidence and verification boundary together with the structural catalogs.

| Capability | Specification scope | Detail |
|---|---|---|
| Record metadata and persistence | Identity, value semantics, parent ownership, singleton settings and virtual records | [Specification](../services/persistence-identity-and-values.md) |
| Document lifecycle and approvals | Draft, submission, cancellation, amendment, workflow, validation order and rollback | [Specification](../services/document-lifecycle-and-transactions.md) |
| Identity and permissions | Authentication, role, user restrictions, sharing, field access and tenant boundaries | [Specification](../services/identity-permissions-and-tenancy.md) |
| Organisation and master governance | Company eligibility, master visibility and protected membership changes | [Specification](../governance/company-and-master-governance.md) |
| General financial accounting | Balanced records, four monetary contexts, dimensions, tolerance and reversal policies | [Specification](../transactions/financial-accounting.md) |
| Accounts payable | Supplier invoices, receipts, advances, payable recognition and return adjustments | [Specification](../transactions/accounts-payable.md) |
| Accounts receivable | Customer invoices, credit exposure, settlement, returns and outstanding balances | [Specification](../transactions/accounts-receivable.md) |
| Taxation and pricing | Tax order, inclusive prices, compounding, discounts, withholding and rounding | [Specification](../transactions/taxation-and-pricing.md) |
| Treasury and reconciliation | Cash, banks, transfers, allocations, fees, exchange differences and matching | [Specification](../transactions/treasury-and-reconciliation.md) |
| Assets and depreciation | Acquisition, finance books, schedules, repair, movement and disposal | [Specification](../transactions/assets-and-depreciation.md) |
| Deferred recognition and financial control | Recognition schedules, budgeting, closing, revaluation and consolidation | [Specification](../transactions/deferred-recognition-and-financial-control.md) |
| Product identity and variants | Stock products, services, attributes, unit factors and variant identity | [Specification](../operations/products-units-and-packaging.md) |
| Packaging and physical parcels | Packs, cases, bundles, packing ranges, weight and dimensional boundaries | [Specification](../operations/products-units-and-packaging.md) |
| Inventory and valuation | Movement, reservations, serial and batch identity, moving-average and layer valuation, inventory revaluation and reposting | [Specification](../operations/inventory-and-valuation.md) |
| Procurement and fulfilment | Requests, quotations, orders, receipts, delivery, picking, returns and supplier evaluation | [Specification](../transactions/procurement-and-fulfilment.md) |
| Transaction progress and closure | Remaining commitments, clamped progress, allowances and close/reopen rules | [Specification](../operations/transaction-progress-and-row-closure.md) |
| Manufacturing and subcontracting | Recipes, materials, capacity, operations, consumption, yields and cost allocation | [Specification](../operations/manufacturing-and-subcontracting.md) |
| Quality and maintenance | Inspections, quality controls, customer maintenance and asset service scheduling | [Specification](../operations/quality-and-maintenance.md) |
| Workforce and employment | Employee identity, onboarding, assignment, separation and final settlement | [Specification](../people-and-services/workforce-and-employment.md) |
| Payroll and benefits | Salary calculation, annualisation, tax slabs, deductions, accrual and payment | [Specification](../people-and-services/payroll-and-benefits.md) |
| Attendance and leave | Shift boundaries, calendars, attendance, accrual, partial pay and entitlement records | [Specification](../people-and-services/attendance-and-leave.md) |
| Recruitment and performance | Hiring, interviews, offers, goals, appraisals, training and ratings | [Specification](../people-and-services/recruitment-and-performance.md) |
| Employee expenses and advances | Sanctioned expenses, advances, reimbursement, settlement and currency effects | [Specification](../people-and-services/employee-expenses-and-advances.md) |
| Customer relationships and sales | Leads, deals, contacts, conversion, ownership, forecasts and communication | [Specification](../people-and-services/customer-relationships-and-sales.md) |
| Projects and time billing | Task dependencies, progress, time, cost, billable hours and revenue | [Specification](../people-and-services/projects-and-time-billing.md) |
| Service and support | Issue routing, calendars, response and resolution targets, pause and escalation | [Specification](../people-and-services/service-and-support.md) |
| Regional capabilities | Supplied country rules, electronic documents and explicit external boundaries | [Specification](../governance/regional-and-specialised-capabilities.md) |
| Operator and customer experiences | Workspace, forms, actions, portal access, calendar and workflow visibility | [Specification](../services/desktop-workflows.md) |
| Remote service contracts | Operation input, authorisation, lifecycle effects, result and error boundaries | [Specification](../services/service-contracts.md) |
| Remote transport | Current routing semantics, supported verbs, pagination, files and notifications | [Specification](../services/remote-transport-contracts.md) |
| External integrations | External synchronisation, communication, acquisition, callbacks and provider boundaries | [Specification](../services/external-integrations.md) |
| Reporting and exports | Report filters, permissions, columns, totals, background reports and exports | [Specification](../services/reporting-and-exports.md) |
| Background work and consistency | Scheduling, durable work, retries, completion state and reconciliation | [Specification](../services/background-work-and-consistency.md) |
| Extensibility and configuration | Record definitions, custom fields, hooks, rules, templates and effective configuration | [Specification](../services/extensibility-and-configuration.md) |
| Fresh initialisation and data exchange | Initial organisation state, opening records, business import and export | [Specification](../services/fresh-initialisation-and-data-exchange.md) |
| Cross-domain transactions | Coordinated operational, financial and employee consequences | [Specification](../transactions/cross-domain-transactions.md) |

## Compatibility dimensions

A capability must agree in decisions, records, state, money, quantity, permissions, timing and failures. Record-schema similarity alone is not enough. Cross-domain operations must additionally agree in the consequences they trigger in other areas.

## Required policy profile

Before executing comparisons, fix the company and currencies, fiscal calendar, precision and rounding policies, valuation method, negative-stock setting, tax and pricing templates, allowance percentages, cancellation history policy, leave calculation basis, payroll calendar, and effective permissions. Record the active configuration choices alongside each acceptance case so the result can be reproduced.

## Deliberate differences

Neutral names replace source-specific identifiers. Deployment and historical migration procedures are excluded. Optional external application internals are outside the supplied source boundary. Proposed improvements are identified individually; adopting one changes strict equivalence for that behaviour.
