# Business questions covered by the domain review

The six domain registers identified 52 topics for investigation. The tables locate the documented decisions for 51 business topics. The final topic, combined-system execution, describes running a configured installation. The business chapters supply the expected decisions for that later comparison.

For example, a payment rule specifies when to recheck the outstanding balance and reject an excess allocation. Database isolation and timing determine which of two simultaneous requests reaches the write first. The [provider evidence register](../rebuild/marketplace-guides/provider-evidence.md) records which provider decisions remain unavailable from public material.

## Finance and statutory interfaces

| Review topic | Applicable chapter |
|---|---|
| Concurrent payment allocation | [Allocation against a changing balance](../transactions/treasury-and-reconciliation.md#allocation-against-a-changing-balance) |
| Foreign standalone delivery exposure | [Unbilled standalone deliveries in company currency](../transactions/accounts-receivable.md#unbilled-standalone-deliveries-in-company-currency) |
| Automatic dimension offsets in foreign accounts | [Automatic dimension offsets in a foreign account](../transactions/financial-accounting.md#automatic-dimension-offsets-in-a-foreign-account) |
| Reporting currency on cancellation | [Reporting exchange on an immutable reversal](../transactions/financial-accounting.md#reporting-exchange-on-an-immutable-reversal) |
| Multiple matching budgets | [Overlapping budgets on one account](../transactions/deferred-recognition-and-financial-control.md#overlapping-budgets-on-one-account) |
| Budget entries across financial years | [Fiscal date of a proposed ledger batch](../transactions/deferred-recognition-and-financial-control.md#fiscal-date-of-a-proposed-ledger-batch) |
| Point of sale and loyalty | [Returns and loyalty at consolidation](../transactions/retail-closing.md#returns-and-loyalty-at-consolidation) |
| Purchase holds | [Supplier and invoice release controls](../transactions/accounts-payable.md#supplier-and-invoice-release-controls) |
| Regional taxation | [Regional base and settlement identity](../transactions/taxation-and-pricing.md#regional-base-and-settlement-identity) |
| Withholding recovery and certificates | [Certificate capacity on recalculation](../transactions/taxation-and-pricing.md#certificate-capacity-on-recalculation) |
| Depreciation date combinations | [Book specific adjustment and reversal](../transactions/assets-and-depreciation.md#book-specific-adjustment-and-reversal) |
| Deferred recognition edge intervals | [Final service date and reserved intervals](../transactions/deferred-recognition-and-financial-control.md#final-service-date-and-reserved-intervals) |
| Intercompany elimination | [Group aggregation and eliminations](../transactions/financial-accounting.md#group-aggregation-and-eliminations) |
| Complete financial report contracts | [Ageing cutoff and payment allocation](../transactions/accounts-receivable.md#ageing-cutoff-and-payment-allocation) |

[Detailed finance and statutory interfaces review register](../../schemas/traceability/financial-review.json)

## Employment and payroll

| Review topic | Applicable chapter |
|---|---|
| Leave and attendance on a partially paid day | [Leave and attendance on a partially paid day](../people-and-services/payroll-and-benefits.md#leave-and-attendance-on-a-partially-paid-day) |
| Employer contributions post independently of net wages | [Employer contributions post independently of net wages](../people-and-services/payroll-posting.md#employer-contributions-post-independently-of-net-wages) |
| Exchange differences on successive advance rows | [Exchange differences on successive advance rows](../people-and-services/employee-expenses-and-advances.md#exchange-differences-on-successive-advance-rows) |
| Future dates in a formula deduction | [Future dates in a formula deduction](../people-and-services/payroll-and-benefits.md#future-dates-in-a-formula-deduction) |
| Overtime with zero standard hours | [Overtime with zero standard hours](../people-and-services/payroll-and-benefits.md#overtime-with-zero-standard-hours) |
| Unpaid leave around submitted payroll | [Unpaid leave around submitted payroll](../people-and-services/attendance-and-leave.md#unpaid-leave-around-submitted-payroll) |
| Training result and participant completion | [Training result and participant completion](../people-and-services/recruitment-and-performance.md#training-result-and-participant-completion) |
| Referral state after a later edit | [Referral state after a later edit](../people-and-services/recruitment-and-performance.md#referral-state-after-a-later-edit) |
| Goal progress at and below zero | [Goal progress at and below zero](../people-and-services/recruitment-and-performance.md#goal-progress-at-and-below-zero) |
| Collection cases and promises to pay | [Collection cases and promises to pay](../people-and-services/lending.md#collection-cases-and-promises-to-pay) |
| Competing workforce transactions | [Competing workforce transactions](../people-and-services/employee-expenses-and-advances.md#competing-workforce-transactions) |

[Detailed employment and payroll review register](../../schemas/traceability/workforce-review.json)

## Inventory, fulfilment and production

| Review topic | Applicable chapter |
|---|---|
| Batch expiry and automatic selection precedence | [Select batches at the effective business time](../operations/traceable-stock-and-service.md#select-batches-at-the-effective-business-time) |
| Serial-specific return cost across every reference combination | [Return the original serial or batch](../operations/traceable-stock-and-service.md#return-the-original-serial-or-batch) |
| Inventory dimension valuation and every inter-company transfer combination | [Check dimension specific stock before and after a movement](../operations/traceable-stock-and-service.md#check-dimension-specific-stock-before-and-after-a-movement) |
| Carrier booking and provider-specific charges | [Quote book and cancel a consignment](../operations/traceable-stock-and-service.md#quote-book-and-cancel-a-consignment) |
| Workstation capacity across every shift, holiday and simultaneous scheduling combination | [Allocate a production window](../operations/traceable-stock-and-service.md#allocate-a-production-window) |
| All calibration and customer maintenance completion policies | [Recompute service and calibration due dates](../operations/traceable-stock-and-service.md#recompute-service-and-calibration-due-dates) |
| Cross-locale inspection evaluation stability | [Evaluate inspection readings across number formats](../operations/traceable-stock-and-service.md#evaluate-inspection-readings-across-number-formats) |
| Asset maintenance end-date and completion-reversal boundaries | [Recompute service and calibration due dates](../operations/traceable-stock-and-service.md#recompute-service-and-calibration-due-dates) |

[Detailed inventory, fulfilment and production review register](../../schemas/traceability/inventory-review.json)

## Transactions crossing business areas

| Review topic | Applicable chapter |
|---|---|
| Concurrent cross-domain commands | [Reserve fulfil and release the last units](../transfers/competing-commitments.md#reserve-fulfil-and-release-the-last-units) |
| Closed-row lifecycle compatibility | [Close and reopen an order after partial execution](../transfers/competing-commitments.md#close-and-reopen-an-order-after-partial-execution) |

[Detailed transactions crossing business areas review register](../../schemas/traceability/cross-domain-review.json)

## Customers and service delivery

| Review topic | Applicable chapter |
|---|---|
| Full commercial record conversion | [Conversion contract](../people-and-services/customer-relationships-and-sales.md#conversion-contract) |
| Forecast selection | [Monetary calculations and forecasts](../people-and-services/customer-relationships-and-sales.md#monetary-calculations-and-forecasts) |
| Project dependencies | [Task progress and dependency scheduling](../transactions/project-costing.md#task-progress-and-dependency-scheduling) |
| Service policy selection | [Preserve two kinds of response promise](../people-and-services/service-and-support.md#preserve-two-kinds-of-response-promise) |
| Service clocks | [Issue response holds resolution and reopening](../people-and-services/service-and-support.md#issue-response-holds-resolution-and-reopening) |
| External lead acquisition | [Lead form acquisition and replay](../people-and-services/customer-relationships-and-sales.md#lead-form-acquisition-and-replay) |
| Regional electronic documents | [Receiver element mapping](../governance/regional-and-specialised-capabilities.md#receiver-element-mapping) |
| Reports and interfaces | [Reports directory](../services/reports/README.md) |
| External connector catalog | [Financial connector completion conditions](../services/external-integrations.md#financial-connector-completion-conditions) |
| Supplier import compatibility defects | [Supplier import row derivation and partial failure](../governance/regional-and-specialised-capabilities.md#supplier-import-row-derivation-and-partial-failure) |

[Detailed customers and service delivery review register](../../schemas/traceability/customer-and-service-review.json)

## Shared services

| Review topic | Applicable chapter |
|---|---|
| Background retry identity | [Execution and retry](../services/background-work-and-consistency.md#execution-and-retry) |
| Task progress visibility | [Task progress and record visibility](../services/identity-permissions-and-tenancy.md#task-progress-and-record-visibility) |
| Savepoint external effects | [Batch outcomes and queued effects](../services/background-work-and-consistency.md#batch-outcomes-and-queued-effects) |
| Workflow path consistency | [Approval action and saved state](../services/document-lifecycle-and-transactions.md#approval-action-and-saved-state) |
| Creation response filtering | [Document creation copy update and deletion](../services/service-contracts.md#document-creation-copy-update-and-deletion) |
| Chunked upload concurrency | [Completion of a multi part attachment](../services/remote-transport-contracts.md#completion-of-a-multi-part-attachment) |

[Detailed shared services review register](../../schemas/traceability/foundation-review.json)

## Additional decisions located during review

The [report execution and prepared-result rules](../services/reporting-and-exports.md#report-admission-current-rows-and-stored-results), [maintenance schedule outcomes](../people-and-services/service-and-support.md#maintenance-schedule-generation-details) and [payment and lending handoffs](../services/optional-settlement.md) document decisions that cross the original topics. The [calculation cross-reference](../../schemas/mathematics/definition-coverage.json) locates the worked case for each named formula or ordered inventory-cost procedure.
