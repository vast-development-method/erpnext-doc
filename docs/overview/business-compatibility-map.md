# Business compatibility map

The map groups capabilities by observable business responsibility. A chapter is a reviewed specification entry point, not a claim that every source branch or external integration has been executed. Use its evidence and verification boundary together with the structural catalogs.

| Capability | Specification scope | Detail |
|---|---|---|
| Record metadata and persistence | Identity, value semantics, parent ownership, singleton settings and virtual records | [Specification](../data/persistence-identity-and-values.md) |
| Document lifecycle and approvals | Draft, submission, cancellation, amendment, workflow, validation order and rollback | [Specification](../runtime/document-lifecycle-and-transactions.md) |
| Identity and permissions | Authentication, role, user restrictions, sharing, field access and tenant boundaries | [Specification](../runtime/identity-permissions-and-tenancy.md) |
| Organisation and master governance | Company eligibility, master visibility and protected membership changes | [Specification](../domains/company-and-master-governance.md) |
| General financial accounting | Balanced records, four monetary contexts, dimensions, tolerance and reversal policies | [Specification](../domains/financial-accounting.md) |
| Accounts payable | Supplier invoices, receipts, advances, payable recognition and return adjustments | [Specification](../domains/accounts-payable.md) |
| Accounts receivable | Customer invoices, credit exposure, settlement, returns and outstanding balances | [Specification](../domains/accounts-receivable.md) |
| Taxation and pricing | Tax order, inclusive prices, compounding, discounts, withholding and rounding | [Specification](../domains/taxation-and-pricing.md) |
| Treasury and reconciliation | Cash, banks, transfers, allocations, fees, exchange differences and matching | [Specification](../domains/treasury-and-reconciliation.md) |
| Assets and depreciation | Acquisition, finance books, schedules, repair, movement and disposal | [Specification](../domains/assets-and-depreciation.md) |
| Deferred recognition and financial control | Recognition schedules, budgeting, closing, revaluation and consolidation | [Specification](../domains/deferred-recognition-and-financial-control.md) |
| Product identity and variants | Stock products, services, attributes, unit factors and variant identity | [Specification](../domains/products-units-and-packaging.md) |
| Packaging and physical parcels | Packs, cases, bundles, packing ranges, weight and dimensional boundaries | [Specification](../domains/products-units-and-packaging.md) |
| Inventory and valuation | Movement, reservations, serial and batch identity, valuation, standard cost and reposting | [Specification](../domains/inventory-and-valuation.md) |
| Procurement and fulfilment | Requests, quotations, orders, receipts, delivery, picking, returns and supplier evaluation | [Specification](../domains/procurement-and-fulfilment.md) |
| Transaction progress and closure | Remaining commitments, clamped progress, allowances and close/reopen rules | [Specification](../domains/transaction-progress-and-row-closure.md) |
| Manufacturing and subcontracting | Recipes, materials, capacity, operations, consumption, yields and cost allocation | [Specification](../domains/manufacturing-and-subcontracting.md) |
| Quality and maintenance | Inspections, quality controls, customer maintenance and asset service scheduling | [Specification](../domains/quality-and-maintenance.md) |
| Workforce and employment | Employee identity, onboarding, assignment, separation and final settlement | [Specification](../domains/workforce-and-employment.md) |
| Payroll and benefits | Salary calculation, annualisation, tax slabs, deductions, accrual and payment | [Specification](../domains/payroll-and-benefits.md) |
| Attendance and leave | Shift boundaries, calendars, attendance, accrual, partial pay and entitlement records | [Specification](../domains/attendance-and-leave.md) |
| Recruitment and performance | Hiring, interviews, offers, goals, appraisals, training and ratings | [Specification](../domains/recruitment-and-performance.md) |
| Employee expenses and advances | Sanctioned expenses, advances, reimbursement, settlement and currency effects | [Specification](../domains/employee-expenses-and-advances.md) |
| Customer relationships and sales | Leads, deals, contacts, conversion, ownership, forecasts and communication | [Specification](../domains/customer-relationships-and-sales.md) |
| Projects and time billing | Task dependencies, progress, time, cost, billable hours and revenue | [Specification](../domains/projects-and-time-billing.md) |
| Service and support | Issue routing, calendars, response and resolution targets, pause and escalation | [Specification](../domains/service-and-support.md) |
| Regional capabilities | Supplied country rules, electronic documents and explicit external boundaries | [Specification](../domains/regional-and-specialised-capabilities.md) |
| Operator and customer experiences | Workspace, forms, actions, portal access, calendar and workflow visibility | [Specification](../interfaces/desktop-workflows.md) |
| Remote service contracts | Operation input, authorisation, lifecycle effects, result and error boundaries | [Specification](../interfaces/service-contracts.md) |
| Remote transport | Current routing semantics, supported verbs, pagination, files and notifications | [Specification](../interfaces/remote-transport-contracts.md) |
| External integrations | External synchronisation, communication, acquisition, callbacks and provider boundaries | [Specification](../interfaces/external-integrations.md) |
| Reporting and exports | Report filters, permissions, columns, totals, background reports and exports | [Specification](../interfaces/reporting-and-exports.md) |
| Background work and consistency | Scheduling, durable work, retries, completion state and reconciliation | [Specification](../runtime/background-work-and-consistency.md) |
| Extensibility and configuration | Record definitions, custom fields, hooks, rules, templates and effective configuration | [Specification](../runtime/extensibility-and-configuration.md) |
| Fresh initialisation and data exchange | Initial organisation state, opening records, business import and export | [Specification](../data/fresh-initialisation-and-data-exchange.md) |
| Cross-domain transactions | Coordinated operational, financial and employee consequences | [Specification](../domains/cross-domain-transactions.md) |

## Compatibility dimensions

A capability must agree in decisions, records, state, money, quantity, permissions, timing and failures. Record-schema similarity alone is not enough. Cross-domain operations must additionally agree in the consequences they trigger in other areas.

## Required policy profile

Before executing comparisons, fix the company and currencies, fiscal calendar, precision and rounding policies, valuation method, negative-stock setting, tax and pricing templates, allowance percentages, cancellation history policy, leave calculation basis, payroll calendar, and effective permissions. Active configuration alternatives remain part of the snapshot even when a future implementation initially selects only one.

## Deliberate differences

Neutral names replace source-specific identifiers. Deployment and historical migration procedures are excluded. Optional external application internals are outside the supplied source boundary. Proposed improvements are identified individually; adopting one changes strict equivalence for that behaviour.
