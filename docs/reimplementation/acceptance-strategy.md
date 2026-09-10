# Acceptance strategy

## Fixture envelope

Every acceptance scenario must define: active schema and policy profile; company and currencies; effective date and timezone; acting identity and permissions; starting records; ordered operations; expected acceptance or error; resulting persisted records; numeric results with units; background completion boundary; and reconciliation assertions.

Use decimal strings for exact monetary and measured-quantity fixture values. Include the rounding method and precision at each step where the source rounds. A result that happens to match at two decimal places does not validate a different sequence of intermediate rounding.

## Required scenario families

| Family | Required variations |
|---|---|
| Lifecycle | Draft save, submit, prohibited edit, permitted submitted edit, cancel, amend, discard, linked dependencies |
| Permissions | Allowed role, denied role, company restriction, record share, owner-only access, field-level restriction, portal boundary |
| Quantities | Units of one, packs of three, six and twelve, fractional quantity, integer-only unit, variant identity, negative return, over-allowance |
| Pricing | List price, discount, inclusive tax, compound tax, fixed charge, quantity charge, residual rounding, zero-value row |
| Finance | Balanced and unbalanced posting, multiple currencies, advance, partial settlement, exchange difference, cancellation and period close |
| Inventory | Receipt, issue, transfer, rejection, return, reservation, backdating, recalculation, serial or batch assignment, configured negative stock |
| Manufacturing | Nested components, phantom assembly, operation cost, partial completion, scrap, secondary output, subcontract consumption |
| Workforce | Join and leave mid-period, holidays, half day, partial pay, unpaid leave, overnight shift, overtime, tax slabs, expense settlement |
| Customer and service | Duplicate lead, lead conversion, lost and won deals, forecast, business calendar, paused target, time billing |
| Failure and concurrency | Two consumers of remaining quantity, stale edit, dependent validation failure, job retry, repeated integration callback |

## Financial reconciliation

For each relevant company and posting context, compare total debits and credits under the configured tolerance. Reconcile receivable and payable control accounts with party settlement records after allocation and exchange adjustments. Reconcile stock value with inventory accounts under the active perpetual-accounting policy, allowing only documented transitional differences. Reconcile payroll accrual and employee payments with the salary and expense records they settle.

A report total alone is insufficient evidence. Compare the voucher-level records and dimensions that explain it. When cancellation retains reversed or cancelled ledger rows, compare effective balances and preserved history under the configured policy.

## State and quantity reconciliation

Compare both lifecycle and business status. Recalculate progress from qualifying descendants using the source's clamping, closed-row and precision rules. Check physical quantity separately from reserved quantity and financial valuation. Closing an unfulfilled order line changes remaining commitment; it does not manufacture a receipt, delivery, return or financial write-off.

## Failure atomicity

Submit an operation whose final downstream validation fails. Confirm the parent transition and all intended synchronous consequences are rolled back. Confirm that no after-commit external action was sent for the failed transaction. Where a source operation intentionally commits partial work, record that boundary explicitly and test the resulting partial-completion report.

Simultaneously attempt two changes against the same remaining commitment or record revision. The acceptance target is the reviewed concurrency contract; a replacement must not claim protection for an untested path merely because another path uses a lock.

## Reference evidence

Source tests are evidence of intended examples and assertions. Static review can establish the arithmetic expressed by a function. Independently recalculating a worked example checks the example. Only execution against a configured reference instance establishes the actual end-to-end outcome of that instance. Record these evidence levels separately.

The supplied source was not installed as a running reference enterprise in this documentation task. The repository therefore does not claim that its acceptance scenarios have already passed against a running reference or a replacement. That qualification remains a distinct completion gate.
