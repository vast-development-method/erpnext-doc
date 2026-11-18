# Acceptance strategy

Acceptance establishes whether a replacement makes the specified business decisions and preserves the resulting records, quantities and financial consequences. A screen, record catalog, decision tree or passing arithmetic example is useful evidence within its own scope. None alone establishes operational conformance.

Use the [conformance profiles](conformance-profiles.md) to fix the selected behavior and the [conformance gates](../../schemas/traceability/conformance-gates.json) to record which qualification obligations have actually passed. Follow the [implementation sequence](sequence.md) so a domain is tested against the same shared identity, lifecycle and accounting services as the rest of the application.

## Evidence classes and permitted conclusions

| Evidence class | What it establishes | What it does not establish |
|---|---|---|
| Catalog integrity | Referenced records, fields, local links and declared choices are structurally present | Their business interpretation or execution is complete |
| Ordered decision structure | Branches, actions and dependencies have an explicit order and representation | Every condition has a complete business meaning or every reachable outcome is supported |
| Explained business contract | Inputs, rules, exceptions, outputs and consequences are stated without unavailable dependencies | The implementing system actually follows those rules |
| Independent arithmetic | A published numerical expectation follows its declared arithmetic and rounding | Authorization, persistent changes, concurrency or application execution |
| Isolated execution | One implemented operation produces the recorded result under a fixed profile | Its combined behavior with other domains or competing operations |
| Integrated execution | A complete implemented sequence preserves all specified records and consequences | Recovery, external delivery, performance or every other policy combination |
| Operational recovery | Restart, retry, restore and background completion preserve the tested sequence's meaning | Untested failure points, workloads or integrations |

An ordered translation is not automatically a complete explained contract. Unexpanded helper behavior, unresolved predicates, missing account selection, unspecified error outcomes or undocumented policy selection leave a semantic obligation open. Count these explicitly. Do not convert a large number of translated decisions into a percentage of business correctness.

Current mathematical catalogs include independently checked examples and explicitly stated expected outcomes. Their presence is not an execution certificate for a replacement. Gate outcomes require a result record from the actual implementing system and must identify the profile, test case, starting state, operation sequence, observed records and applicable completion boundary.

## Fixture envelope

Each executable scenario fixes the following information before the first operation:

| Required value | Meaning |
|---|---|
| Scenario identity and specification revision | Stable local case and exact version of the contract being assessed |
| Conformance profile | Currency, rounding, valuation, cancellation, financial-book, authority and compatibility choices |
| Business identities | Companies, users, parties, employees, products, accounts, warehouses and original document-line identities used |
| Calendar context | Effective dates, transaction dates, posting dates, timezone, holidays, shifts and financial periods |
| Starting records | Complete relevant values, lifecycle states, existing allocations, quantities, balances and record revisions |
| Acting identity | Roles, company membership, shared-record grants, ownership and field access, including explicit absence of bypass authority |
| Ordered operations | Business commands, amounts, units, reference identities and expected synchronization or background boundaries |
| Expected outcomes | Accepted or rejected condition; new or changed records; quantities; currency amounts; statuses; warnings; retained history |
| Failure schedule | Point at which validation fails, a competing operation commits, an acknowledgement is lost or a worker restarts |
| Reconciliation outputs | Named account balances, party claims, inventory quantities and values, interval recognition, and other applicable domain controls |

Amounts and measured quantities use decimal strings. State the precision and tie method for every rounding boundary, including rates, unit factors, tax rows and final settlements. State whether expected balances are complete company balances or only movements for the scenario's named accounts. An omitted account is not permission to hide a difference in an uninspected suspense account.

A generated operation identifier is distinct from a business document identity and from an external provider reference. Record each where applicable. Repeating a completed operation must return the existing result or reject the repeated lifecycle action without adding a second financial effect.

## Shared scenario families

| Family | Required boundary cases | Local executable targets |
|---|---|---|
| Identity and authority | Same display name with different identity; wrong company; permitted read but rejected use; denied conversion; same command through ordinary form and remote call | [Customer and service cases](../../schemas/mathematics/customer-and-service-acceptance-cases.json), including `restricted-master-visible-but-ineligible` and `conversion-permission-denial` |
| Lifecycle and progress | Save, submit, prohibited submitted edit, cancellation, amendment, stale revision, newly closed predecessor, all rows closed, repeated recalculation | [Transaction progress](../../schemas/mathematics/transaction-progress-calculations.json), including `closed_order_preserves_posted_effects` |
| Commercial units | Each, packs of three, six and twelve, fractional packs, whole-stock-unit rule, historical returns, indivisible warehouse placement | [Inventory cases](../../schemas/mathematics/inventory-acceptance-cases.json), including `mixed_commercial_pack_sequence`, `whole_stock_unit_rejection` and `putaway_indivisible_six_pack` |
| Pricing and taxes | Margin before discount; compound included tax; fixed-charge residual; row versus total rounding; withholding history and certificate allocation | [Financial calculations](../../schemas/mathematics/financial-calculations.json) and [accounting cases](../../schemas/mathematics/accounting-acceptance-cases.json) |
| Posting and settlement | Imbalance rejection; explicit rounding; partial payment; excess advance; signed credit; historical exchange rate; statement match without new cash | [Accounting cases](../../schemas/mathematics/accounting-acceptance-cases.json), including `journal_rounding_repair`, `foreign_customer_receipt_and_realized_gain` and `bank_statement_partial_clearance_and_unlink` |
| Inventory and costing | Ordered valuation layers; backdating; late landed cost; standard variance; reservation contention; negative-stock precision | [Inventory cases](../../schemas/mathematics/inventory-acceptance-cases.json), including `backdated_receipt_reposting`, `landed_cost_after_partial_delivery` and `reservation_concurrent_last_units` |
| Manufacturing | Nested component denominator; process loss; secondary output allocation; actual zero material cost; standard output variance | [Inventory cases](../../schemas/mathematics/inventory-acceptance-cases.json), including `recursive_recipe_explosion`, `genuine_zero_cost_manufacture` and `manufacturing_standard_variance` |
| Workforce | Partial pay; overnight shift cutoff; leave ownership; payroll accrual; withholding reversal; shared advance allocation; expense cancellation | [Workforce cases](../../schemas/mathematics/workforce-acceptance-cases.json), including `workforce-balanced-payroll-accrual`, `workforce-night-shift-watermark` and `workforce-concurrent-advance` |
| Customer and service | Contact reuse; deal conversion; time overlap; zero-value billing; deadline equality; paused business calendars; cancellation dependencies | [Customer and service cases](../../schemas/mathematics/customer-and-service-acceptance-cases.json), including `time-adjacent-intervals`, `service-deadline-equality-fulfilled` and `service-hold-wall-clock-extension` |
| Financial periods | Final recognition residual; frozen-date shift; draft recognition reservation; depreciation; asset cancellation anomaly; budget and closing gates | [Accounting cases](../../schemas/mathematics/accounting-acceptance-cases.json), including `daily_deferred_income_with_final_residual` and `complete_daily_depreciation_leap_year_schedule` |

Case identifiers select records within the linked catalog. Their existing expected data is the starting contract; the implementing system must add observed execution results without overwriting expectations to match its output.

## Financial reconciliation is exact after authorized adjustments

For each posted event, compare company-currency debits and credits after all authorized rounding and exchange rows have been included. A permitted pre-posting imbalance is a rule for creating an explicit balancing row or rejecting the event. It is not an allowance to publish unbalanced books. The ordinary journal and payment allowance differs from the other-voucher allowance; see [financial accounting](../domains/financial-accounting.md#posting-pipeline-and-balancing).

Check each named account and dimension as well as the overall sum. A balanced entry can still duplicate variance, post to the wrong customer, issue stock twice or conceal an incorrect cost in another expense account. Compare company, account, transaction and reporting currency separately. Reporting-currency reversal can use a different rate date under its documented policy; do not promise a zero reporting residual solely because company and account amounts reverse.

Reconcile party claims after payments, credits, advance applications and realized exchange entries. Preserve unapplied advances separately from settled claims. Reconcile inventory quantity and value with effective stock history, and stock financial accounts under the selected perpetual-accounting policy. A backdated or late-cost operation is unfinished while required valuation and financial recalculation remain pending. Any permitted temporary difference must name its operation, amount, pending work and completion condition.

Reconcile payroll expenses, employee liabilities, deductions, withholding, advances and bank payments against the salary or expense records they concern. Salary preparation, salary submission, accrual journal creation and payment are separate observable operations. Reconcile asset carrying value and financial-book depreciation independently of forecast rows.

## Failure, atomicity and external consequences

For a single-document operation, introduce failure at the final required synchronous validation. Compare the entire before-and-after state: parent lifecycle, previous-document progress, stock movement, general ledger, party allocation, withholding, schedule links and queued external work. The failed event must leave no partial effective business consequence. A generated identifier or provisional row is not success.

Some batch operations deliberately retain successful units before another unit fails. The scenario must identify that declared unit of work. Require a complete partial-result record naming completed units, failed unit, error and safe resumption point. Do not demand a whole-batch rollback from a contract that explicitly publishes interval-level completion, and do not silently apply partial completion to a single-document posting.

For after-commit work, verify no external request becomes eligible until its owning business event is durable. Lose the external acknowledgement after the provider accepts a request, then retry: the adapter must identify the previous operation and avoid sending the payment, message or business effect twice under its declared provider contract. If the provider cannot guarantee deduplication, the profile needs an explicit reconciliation and operator-recovery policy; it cannot claim automatic exactly-once external execution.

## Deterministic concurrency scenarios

Use two workers with controlled barriers. Both read the same initial remainder; pause immediately before the protected mutation; allow one to commit; then release the other. Record actual outcomes, including a revalidation rejection, conflict or permitted partial allocation. Timing two requests approximately together is insufficient to prove the contested interleaving occurred.

Required contested resources include the final available stock, the final outstanding invoice amount, one paid employee advance, a budget remainder, the same draft revision, one generated salary interval, a recognition interval and one external operation identifier. Under the replacement's consistency requirement, effective allocations cannot exceed the available amount and a completed business event cannot be duplicated. Any observed compatibility behavior that lacks this guarantee must be called out as a policy decision instead of being described as a passed concurrency gate.

## Cancellation and recovery

A cancellation fixture declares every dependency edge as block, cancel, reverse, unlink, recalculate or retain. Test both a permitted case and a blocked dependent case. Verify history, not only current status. Bank-statement cancellation removes clearance without reversing the payment; advance-application cancellation restores the allocation without reversing the original money movement; order closure releases commitment without paying an invoice.

Restart background processing after each durable boundary, including after result creation but before acknowledgement. Resume pending valuation, salary, recognition, import and integration work and prove that completed units remain single. Restore a backup into an isolated environment, recompute the same company and domain reconciliations, and compare outstanding work before accepting the restore. Recovery objectives and workload limits belong to the declared deployment profile and require measured execution.

## Conformance decision

The [gate register](../../schemas/traceability/conformance-gates.json) defines required dependencies and evidence. A capability may be marked excluded from a limited profile only when that exclusion is explicit and its dependent capabilities are excluded or separately supported. It cannot be excluded from the complete integrated profile while still claiming the full application has been rebuilt.

An unresolved financial, permission, data-loss, duplicate-effect or reconciliation failure blocks qualification for the affected profile. A documented compatibility anomaly requires a selected policy and the corresponding expected result; documentation alone does not make a contradictory implementation conformant. Structural completeness, mathematical consistency and operational readiness remain separate reported conclusions.
