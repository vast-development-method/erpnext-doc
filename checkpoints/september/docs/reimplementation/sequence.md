# Reimplementation sequence

Build one integrated application around shared identity, company ownership, record lifecycle, monetary arithmetic, inventory units and financial posting. Human resources, customer relationships, manufacturing and distribution are consumers and contributors to those shared services. Separate teams may implement them, but they must not invent disconnected employees, parties, products, payments or account histories.

The sequence below is ordered by the records and decisions a stage requires. A stage produces operational behavior and measurable acceptance evidence. Record creation or screen availability alone does not satisfy an exit gate. Use the [acceptance strategy](acceptance-strategy.md), [conformance profiles](conformance-profiles.md) and [machine-readable gates](../../schemas/traceability/conformance-gates.json) together.

## Stage plan and exit gates

| Stage | Required predecessors | Build and integrate | Concrete exit evidence |
|---|---|---|---|
| 1. Value and identity | None | Stable record identities, parent-row identity, exact amount and quantity meanings, date/time context, precision and rounding choices, schema loading and relationships | Currency and quantity fixtures agree at every stated rounding boundary; duplicate identity, invalid parent and unresolved required relationship are rejected |
| 2. Authority and lifecycle | Stage 1 | User identity, roles, company and field restrictions, permitted read versus permitted use, draft revisions, submission, cancellation, amendment and workflow gates | Same business command through ordinary form and remote transport has the same authority checks; stale updates and rejected submission preserve the before-state |
| 3. Shared organizational masters | Stages 1–2 | Company and financial calendar, accounts, dimensions, financial books, customers, suppliers, contacts, employees, products, variants, units, warehouses and policies | Account and warehouse company restrictions pass; shared contact does not imply shared employee or customer identity; commercial pack conversion preserves stock-unit quantities |
| 4. Financial event foundation | Stages 1–3 | Ordered posting validation, explicit rounding, company/account/transaction/reporting measurements, general ledger, party settlement history, reversal and query projection | `journal_rounding_repair`, over-allowance rejection, negative-side normalization, named-account comparison and reversal-date reporting rules pass |
| 5. Pricing and commercial commitments | Stages 1–4 | Price lists, discounts, taxes, withholding prerequisites, quotations, orders, row references, allowances, closure and progress recalculation | Compound included tax, fixed-charge residual, packs and zero-value rows pass; closed rows cannot be silently deleted or used by stale drafts; closure does not post cash or stock |
| 6. Inventory and valuation | Stages 1–5 | Receipts, issues, transfers, reservation, ordered cost layers, standard costs, serial and batch identity, backdated recalculation and late cost allocation | Mixed-pack receipt/issue/return, final-stock contention, receipt variance only once, backdated cost and remaining-versus-sold landed-cost allocation pass |
| 7. Commercial claims and settlement | Stages 4–6 | Customer and supplier invoices, receipt/delivery billing, stock-updating invoices, credit and debit adjustments, payment schedules, partial payment, advances and realized exchange | Complete purchase-to-payment and sale-to-collection sequences reconcile stock, clearing, income/expense, tax, party outstanding and bank after every event |
| 8. Treasury and financial periods | Stages 4, 6–7 | Statement import/matching, fees, exchange revaluation, deferred recognition, budgets, period close, reporting books, asset acquisition, depreciation, disposal and repair capitalization | Bank match creates no second cash event; recognition and depreciation residuals reconcile; chosen anomaly policies pass; close rejects stale inventory history |
| 9. Manufacturing and subcontracting | Stages 3–8 | Component structures, nested recipes, operation costs, capacity, work orders, material supply, consumption, output, secondary output, process loss and variance | Exact material demand, consumed value, capitalized operation costs, actual zero-cost material and standard variance reconcile with inventory and accounting |
| 10. Workforce and payroll | Stages 2–4, 7–8 | Employment, recruitment, onboarding, calendars, attendance, leave, salary rules, tax slabs, benefits, advances, expenses, payroll accrual, payment and final settlement | Attendance and leave boundaries pass; salary preparation does not imply accrual; payroll and claim sequences reconcile employee liabilities, deductions, advances, tax and bank |
| 11. Customer, project and service operations | Stages 2–5, 7–8 | Lead and deal conversion, communications, campaigns, contracts, project/task progress, time billing, service calendars, maintenance and customer-facing access | Shared identity and denied-conversion cases pass; billable time, forecast, service deadlines, paused intervals and dependency cancellation produce declared records |
| 12. Configuration and operational interfaces | Stages 1–11 | Schema extensions, configurable predicates, rule validation, reports, printing, imports, exports, external adapters, queues and administration | Extensions use shared lifecycle and permissions; imports and retries preserve identity; reports trace to named ledger and domain records; unsupported rules fail explicitly |
| 13. Integrated qualification | All preceding stages | Cross-domain workloads, controlled concurrency, cancellation chains, pending-work recovery, restore, access review and measured operational limits | Every required gate has an executed result for the exact profile; financial and domain reconciliation pass; unresolved critical findings block qualification |

Stage numbers indicate dependencies, not a requirement to complete every screen before parallel work begins. A payroll team can begin calendar and compensation logic after the shared values and identities stabilize; its accrual and payment qualification still depends on the financial service. Customer conversion can be developed before manufacturing; customer billing still uses the common pricing, invoice and settlement contracts.

## First working vertical sequence

The first integrated demonstration uses one company, one currency, two users with different authority, a customer, a supplier and an ordinary stock product. Fix two decimal monetary places, no tax, moving-average valuation, 1000.00 opening bank and 1000.00 opening equity, with zero stock. A case contains twelve pieces, a six pack contains six and a three pack contains three. Receipt cost is 5.00 per piece; selling price is 7.00 per piece.

| Operation | Debit | Credit | Physical quantity change |
|---|---|---|---|
| Receive five cases of twelve at 60.00 per case | Inventory 300.00 | Received but unbilled 300.00 | Plus 60 |
| Bill the received goods | Received but unbilled 300.00 | Supplier payable 300.00 | None |
| Deliver two six packs | Cost of goods sold 60.00 | Inventory 60.00 | Minus 12 |
| Invoice the customer at 42.00 per six pack | Customer receivable 84.00 | Sales income 84.00 | None |
| Receive part of customer claim | Bank 40.00 | Customer receivable 40.00 | None |
| Pay part of supplier claim | Supplier payable 150.00 | Bank 150.00 | None |
| Receive one three pack returned at original cost | Inventory 15.00 | Cost of goods sold 15.00 | Plus 3 |
| Credit the returned three pieces at original selling price | Sales income 21.00 | Customer receivable 21.00 | None |

Expected ending stock is 51 pieces valued at 255.00. Bank is 890.00, supplier debt is 150.00, customer debt is 23.00 and received-but-unbilled clearing is zero. Net sales are 63.00, cost of goods sold is 45.00 and gross profit is 18.00. Preserve the original receipt, delivery, invoice, return and allocation line identities throughout.

The complete `integrated_mixed_pack_trading` fixture, including every posting and closing balance, is embedded in the [conformance gate register](../../schemas/traceability/conformance-gates.json). It extends `mixed_commercial_pack_sequence` from [inventory acceptance](../../schemas/mathematics/inventory-acceptance-cases.json) with fully defined invoice, credit and payment amounts. Physical returns and customer credits remain distinct events, even if the implementing interface submits them together.

The second user then attempts a prohibited company or posting operation, and a stale draft attempts to use a newly closed order row. Both must fail without changing the demonstrated balances. Repeat a completed submission and allocation to verify it cannot duplicate the event. This sequence exercises shared services early, before expanding into many disconnected feature demonstrations.

## Parallel implementation boundaries

Freeze and version these contracts before domain teams integrate:

1. Identity and ownership: companies, parties, employees, contacts, products, original document lines and generated consequence links.
2. Values: quantity units, amount currencies, rates, timezone, date intervals, field precision and rounding stages.
3. Commands: authorized actor, expected record revision, lifecycle action, stable operation identity, result and error envelope.
4. Posting: prepared amounts, account selection, dimensions, financial books, settlement references, effective dates and cancellation policy.
5. Background work: durable owner event, declared unit of completion, retry identity, pending state, failure result and recovery command.
6. Reconciliation: query measurement, included history, as-of cutoff, pending recalculation treatment and named-account comparison.

One domain must not change another domain's balances by direct record editing. It invokes the owning business operation or records a deliberately defined shared transaction. Shared query projections can be rebuilt from authoritative records, but rebuilding a projection must not replay a bank payment or create new accounting.

## Reading paths tied to implementation

| Workstream | Read before coding | Read before declaring integration complete |
|---|---|---|
| Shared records and authority | [Persistence and values](../data/persistence-identity-and-values.md), [lifecycle](../runtime/document-lifecycle-and-transactions.md), [identity and permissions](../runtime/identity-permissions-and-tenancy.md) | [Service contracts](../interfaces/service-contracts.md), [configuration](../runtime/extensibility-and-configuration.md), [background consistency](../runtime/background-work-and-consistency.md) |
| Distribution | [Products and packaging](../domains/products-units-and-packaging.md), [progress and closure](../domains/transaction-progress-and-row-closure.md), [inventory](../domains/inventory-and-valuation.md), [procurement](../domains/procurement-and-fulfilment.md) | [Financial accounting](../domains/financial-accounting.md), [pricing and taxes](../domains/taxation-and-pricing.md), [receivables](../domains/accounts-receivable.md), [payables](../domains/accounts-payable.md) |
| Period accounting | [Treasury](../domains/treasury-and-reconciliation.md), [deferred recognition and controls](../domains/deferred-recognition-and-financial-control.md), [assets](../domains/assets-and-depreciation.md) | [Cross-domain transactions](../domains/cross-domain-transactions.md), [reporting](../interfaces/reporting-and-exports.md) |
| Manufacturing | [Manufacturing and subcontracting](../domains/manufacturing-and-subcontracting.md), [quality and maintenance](../domains/quality-and-maintenance.md) | Inventory costing, asset capitalization, supplier claims and applicable accounting gates |
| Workforce | [Employment](../domains/workforce-and-employment.md), [attendance and leave](../domains/attendance-and-leave.md), [payroll](../domains/payroll-and-benefits.md) | [Expenses and advances](../domains/employee-expenses-and-advances.md), [recruitment](../domains/recruitment-and-performance.md), shared payment and ledger gates |
| Customer and service | [Relationships and sales](../domains/customer-relationships-and-sales.md), [projects and time](../domains/projects-and-time-billing.md), [service](../domains/service-and-support.md) | Shared identity, commercial claims, ordinary-user report access and external communication recovery |

## Policy decisions before promotion

The [profiles](conformance-profiles.md) separate observed compatibility from deliberately corrected policies. Select each exceptional behavior before evaluating its case. Examples include asset-adjustment residual cancellation, final-month recognition cutoff, hold-release predicates, cumulative advance exchange behavior and configurable rounding. Do not change an expectation after a failed test without recording a specification or profile change and rerunning affected gates.

A structurally represented component with an unexplained business condition remains unfinished for reconstruction. A domain whose arithmetic passes but whose submission, failure or permission paths are unexecuted remains unqualified. The complete integrated profile includes distribution, accounting, manufacturing, workforce and customer/service operations with shared operational capabilities; removing a domain creates a narrower profile and cannot support a claim of complete behavioral equivalence.

## Delivery boundary

The specification does not choose an implementation language, database brand, user-interface technology, process topology or hosting provider. Every stage must produce a reviewable record of business behavior, supported configuration and measured evidence. Hand off the exact specification revision, profile, gate results, unresolved findings, reconciliation outputs and recovery run results. These records allow the next team to continue implementation without rediscovering the business rules or guessing which claims were actually tested.
