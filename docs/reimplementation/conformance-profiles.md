# Conformance profiles

A conformance profile fixes the business choices under which a replacement is being assessed. Different active policies can legitimately produce different results from the same visible commercial amount. The profile therefore accompanies every fixture, command result and qualification statement. It is a declaration of scope and expected behavior, not an approval certificate.

Use [acceptance strategy](acceptance-strategy.md) for execution rules and [conformance gates](../../schemas/traceability/conformance-gates.json) for dependencies, required cases and result records. The [implementation sequence](sequence.md) explains when each shared capability becomes available.

## Profile contents

| Profile section | Required decisions |
|---|---|
| Identity | Profile identity, specification revision, immutable profile revision and effective assessment date |
| Company and authority | Companies, currency ownership, role and field permissions, membership boundaries, delegated authority and permitted exceptions |
| Numeric values | Monetary precisions, unit-rate and valuation precisions, unit-factor precision, selected decimal tie policy, tax row rounding, cash fraction and cash tie handling |
| Dates | Business timezone, posting and transaction dates, financial calendar, business calendars, shift crossing, inclusive or exclusive interval rules |
| Financial posting | General-ledger cancellation policy, reporting-rate date, financial-book selection, separate advance accounts, rounding accounts, dimensions and closing controls |
| Inventory | Enabled valuation methods, negative-stock policy and tolerance, quantity units and whole-unit constraints, standard-cost policy, reservations, serial and batch allocation, valuation completion boundary |
| Commercial behavior | Credit and overdue policy, order/delivery exposure, allowable over-fulfilment, row closure, taxes, discounts, withholding and payment terms |
| Workforce | Attendance basis, leave policy, compensation frequency, salary proration, benefit and tax rules, expense settlement, employment transfer and final settlement |
| Customer and service | Shared identity choices, lead/deal conversion, forecast, project progress, time billing, service calendar, pause and cancellation policies |
| Extensions and operations | Supported configurable predicates, custom fields, reports, integrations, durable background work, retries, backup, restore, workload and recovery limits |
| Compatibility decisions | Explicit selection for every documented anomaly or ambiguous behavior reached by the profile |
| Qualification evidence | Required gate identities, actual result records, unresolved findings and any declared capability exclusions |

A profile must not silently treat a missing policy as an industry convention. If the specification defines a default, record its resolved value. If it defines several choices, select one. If behavior remains unresolved for a reached condition, mark the corresponding gate blocked until an explicit policy and expected outcome exist.

## Supported assessment scopes

### Complete integrated compatibility

This scope includes the shared foundation, distribution, financial accounting, inventory, manufacturing and subcontracting, workforce and payroll, customer relationships, projects, service, configuration, reporting and operations. It selects the observed behavior specified by the local contracts, including unusual but explicit boundary decisions. All applicable gates in the register are required. No domain may be excluded while still describing the result as a complete reconstruction.

Compatibility does not excuse an unresolved accounting discrepancy or insecure authorization. If an observed behavior conflicts with the operational guarantees required for deployment, expose that conflict as a policy decision and qualification blocker. A replacement may adopt a corrected policy, but its declared scope must then distinguish that correction.

### Complete integrated application with declared corrections

This scope retains all business domains but deliberately changes one or more identified behaviors. Each correction names the old decision, the new decision, the affected data and operations, expected numerical or state differences, and the gates rerun. It requires the same integrated and operational evidence as complete compatibility.

A corrected profile does not claim strict equivalence on its declared deviations. For example, restoring an asset's original residual value on adjustment cancellation is a reasonable corrected policy, but the observed double-sign arithmetic has a different output. The profile must choose the appropriate expected result before testing.

### Limited capability assessment

This scope can be used while implementing a subset or preparing a deliberately smaller product. List every included and excluded capability, and enforce dependency closure. A payroll-only demonstration still needs identity, company ownership, calendars, financial accounts, salary liabilities and payment contracts for whatever payroll behavior it claims. It cannot bypass those dependencies by declaring accounting out of scope while still claiming posted payroll.

Limited assessment results are useful progress evidence. They do not become complete-application certification because the included cases pass. Their summary must name the assessed scope.

## Numeric and accounting choices that cannot be collapsed

| Choice | Required distinction |
|---|---|
| Generic decimal rounding | Half to even, half away from zero and scale-sensitive ties are distinct active behaviors |
| Cash fraction rounding | Exact half of the fraction chooses the lower multiple under its stated contract; this is separate from generic monetary rounding |
| Tax contribution rounding | Rounding each item before accumulation can differ from rounding the final accumulated tax |
| Pre-posting imbalance | Ordinary journals/payments and other vouchers have different repair allowances; final posted company debits and credits must balance after permitted repair |
| Currency measurement | Company, account, transaction and reporting measurements preserve their own values and rate dates |
| Advance accounting | Party credit/debit balances and separate advance accounts produce different application entries while preserving the original money movement |
| Inventory valuation | Moving average, ordered valuation layers and standard cost produce different unit cost, return and variance behavior |
| Depreciation | Fixed-period, daily-prorated, declining and shift-weighted methods have different denominators and residual corrections |
| Deferred recognition | Daily and monthly calculations differ in date counting, rounding, partial intervals and final residual handling |

The [financial calculations](../../schemas/mathematics/financial-calculations.json), [inventory calculations](../../schemas/mathematics/inventory-calculations.json), [workforce calculations](../../schemas/mathematics/workforce-calculations.json) and [customer/service calculations](../../schemas/mathematics/customer-and-service-calculations.json) define these choices with the linked domain explanations. Selecting one default does not authorize dropping other supported policy choices from the complete scope.

## Explicit compatibility decisions

| Decision | Observed behavior that must remain visible | Corrected alternative, if selected | Local case |
|---|---|---|---|
| Asset residual on value-adjustment cancellation | The documented double sign can increase residual again while carrying value restores | Restore the pre-adjustment residual and revalidate future depreciation | `asset_adjustment_residual_cancellation_boundary` in [accounting cases](../../schemas/mathematics/accounting-acceptance-cases.json) |
| Recognition cutoff in final service month | A final marker can survive a cutoff and recognize all remaining value early | Recognize only the declared elapsed interval until actual service end | `deferred_final_month_cutoff_boundary` in [accounting cases](../../schemas/mathematics/accounting-acceptance-cases.json) |
| Supplier and invoice holds | Supplier expiry, payment discovery, invoice generation and final invoice-reference checks have different predicates | Define one explicit expiry transition and apply it consistently before each operation | `supplier_hold_through_release_date` and `invoice_hold_date_and_flag_differ` in [accounting cases](../../schemas/mathematics/accounting-acceptance-cases.json) |
| Supplier bill-number uniqueness | Matching supplier and financial interval can reject a duplicate in another company | Scope duplicate detection by company as an explicitly changed policy | `supplier_number_uniqueness_cross_company_boundary` in [accounting cases](../../schemas/mathematics/accounting-acceptance-cases.json) |
| Employee advance exchange aggregation | Cumulative processing can make row order affect the final exchange amount | Aggregate each advance's independent exchange difference once | `workforce-advance-row-reorder` and `workforce-advance-offsetting-exchange-difference-example-1` in [workforce cases](../../schemas/mathematics/workforce-acceptance-cases.json) |
| Zero-value task and billing measurements | Specific zero-value and completed-percentage boundaries differ from ordinary nonzero paths | Adopt a separately defined uniform policy and record changed outcomes | `time-zero-price-billing-progress` in [customer and service cases](../../schemas/mathematics/customer-and-service-acceptance-cases.json) and progress boundary cases |
| Reporting-currency reversal | Reversal can remeasure reporting amounts using the applicable reversal-date policy | Preserve original reporting amounts or create a separately defined reporting adjustment | [Financial cancellation contract](../domains/financial-accounting.md#cancellation-and-correction) |

This table identifies concrete decisions; it does not grant blanket permission to change every unexpected result. Review each deviation's effect on persisted history, reports, integration payloads and dependent calculations. A changed default without a new profile revision invalidates previously recorded qualification results for affected gates.

## Result states and promotion

The gate register uses an explicit assessment status. `not_assessed` means no conclusion; `blocked` means an unresolved prerequisite or finding prevents assessment; `failed` means execution contradicts the selected contract; `passed` means the required evidence for that gate is present; `excluded` is allowed only in a declared limited scope with valid dependency treatment.

Evidence classes are recorded separately from gate status. An arithmetic gate can pass from independent arithmetic, while an integrated-posting gate requires implemented command execution and persistent record reconciliation. Do not convert an arithmetic pass into an integrated pass by reusing the same evidence record.

Each result identifies scenario, profile revision, implementation revision, test dates, executing actor, relevant starting-state identity, observed operation outcomes, retained records, reconciliation values, failure injection and evidence class. Its scope may be one company, currency, valuation policy or calendar. A broader claim requires the corresponding additional policy results.

## Current repository assessment

This repository supplies local contracts, record catalogs, decision structures and acceptance inputs. Selected numerical examples have independent arithmetic verification. The new gate register begins with all application qualification gates unassessed; it does not invent execution evidence for a replacement that has not been run. Historical validation files retain the scope of the checks they actually recorded and must not be treated as current enterprise certification.

A receiving implementation team can build directly against these local definitions and cases. Where the catalog records structural behavior without complete business meaning, the missing meaning is a specification obligation, not an instruction to obtain inaccessible implementation files. Resolve the obligation here, version the contract and rerun dependent gates.
