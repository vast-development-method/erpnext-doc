# Reimplementation sequence

The sequence follows dependency closure and financial consequences. Each stage produces usable operations plus measurable evidence. A stage is not complete merely because its screens or tables exist.

| Stage | Build and integrate | Exit evidence |
|---|---|---|
| 1. Value and identity foundation | Currency-aware amounts, quantities, dates, precision, record identity, parent ownership and schema registry | Exact numeric fixture results; stable references; rejected invalid ownership |
| 2. Authorised record lifecycle | User identity, permissions, tenant boundary, document save, submission, cancellation, revisions and workflows | Same operation decisions across form and remote entry; rollback and stale-write cases |
| 3. Organisation and shared masters | Companies, fiscal periods, accounts, dimensions, parties, products, warehouses and units | Referential and company restrictions; full unit conversion matrix |
| 4. Journal and settlement foundation | Balanced postings, party balances, advances, payment allocation, currencies, reconciliation and reversals | Trial balance, party reconciliation and cancellation histories agree |
| 5. Inventory foundation | Stock records, availability projections, reservations, serial and batch identity, valuation and reposting | Quantity conservation and value reconciliation under backdating and returns |
| 6. Purchase and sales cycle | Quotations, orders, receipt and delivery, invoices, taxes, discounts, credit and progress | Complete purchase-to-payment and order-to-collection scenarios |
| 7. Treasury and period accounting | Bank reconciliation, deferred recognition, budgets, closing, revaluation, consolidation and assets | Period reports agree with postings and fixtures; reopening and cancellation policies pass |
| 8. Manufacturing and subcontracting | Material structures, operations, capacity, work orders, consumption, outputs, subcontract materials and variances | Component conservation and cost allocation reconcile to inventory and accounts |
| 9. Workforce and payroll | Employment, calendars, attendance, leave, expenses, recruitment, compensation, deductions and payroll posting | Day and tax calculations match; employee liability and payment reconcile |
| 10. Customer and service operations | Lead and deal management, communications, project time, support targets, maintenance and portals | Conversion and permission cases; forecasts and billing reproduce defined outcomes |
| 11. Configurable enterprise experience | Metadata editing, custom fields, rules, dashboards, reports, print, imports, exports and integrations | Effective-schema fixtures; ordinary-user access and failure behaviour |
| 12. Full scenario qualification | Mixed domains, concurrent updates, background retries, cancellation chains and reconciliation | All claimed capability rows have executed acceptance evidence and resolved findings |

## Parallel work

Domain work can proceed in parallel once value types, identity, company boundaries, lifecycle and accounting contracts are agreed. Financial and inventory teams must share posting cut-offs, precision, reversal policies and transaction identities. Workforce and customer work must share person, contact and communication contracts without assuming they are the same record.

A domain implementation must not invent its own currency or unit handling. All formulas should use the declared operands, rounding points and policy profile from the mathematical catalogs.

## Recommended reading paths

For financial work, read persistence values, financial accounting, taxes and pricing, receivables, payables, settlement and asset specifications before building reports. For distribution, read products and packaging, transaction progress, inventory valuation and procurement before manufacturing. For workforce, read identity, calendars, leave, payroll and expense accounting together. For the shared foundation, read lifecycle, permissions, service contracts, background work and extensibility as one dependency set.

## Deliverable boundary

The blueprint does not fix a language, process count, database brand, user-interface framework or deployment platform. Equivalent business behaviour is the acceptance target. A proposed improvement is a deliberate deviation and should be enabled only under a named replacement policy, with its own tests and an explicit statement that strict source equivalence is changed.
