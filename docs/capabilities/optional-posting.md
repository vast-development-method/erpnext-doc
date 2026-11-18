# Optional activities that affect posting

## Farm activity and livestock valuation

Capture company, active employee in that company, livestock item, inventory batch, house warehouse and effective time. The house and optional project belong to the company. The selected livestock is enabled, batch tracked and not individually serialized. Determine population **in this house at the activity time**. Reject future activity, activity before batch manufacture and an empty house.

| Activity | Document consequence | Additional checks |
|---|---|---|
| Feeding | Draft material issue of feed from its source warehouse | Positive quantities in stock units. The livestock cannot be its own feed. |
| Mortality | Draft material issue of livestock from the house | Readable mortality reason and positive whole count at most equal to the population. |
| Produce collection | Draft material receipt into the selected warehouse | Receive produce distinct from the livestock, with a positive stated rate. |
| Weighing | Weight observation | Whole sample size at most equal to population. Compare with the previous uncancelled kilogram observation in the same company, house, batch and item. |
| Husbandry | Husbandry event | A permitted practice and end at or after start. Pregnancy checks require the structured pregnancy record. |

Feed and produce allow one through 100 rows of enabled, non-serialized stock items with a matching active batch where needed. Saving creates a draft. Submitting an eligible feed or treatment issue against an active capitalization batch creates a linked revaluation. Consume and receive the same livestock and quantity in the same warehouse at the source posting time. Group actual additional costs by expense account. The consumed animals carry their inventory valuation. An empty capitalization location blocks revaluation. Mortality and produce collection are outside this capitalization decision.

Use one operation identity per intended save. Within the destination document class the same identity and equivalent request identify the existing record, subject to read permission. Reject reuse with changed input even when two activities both target stock movements. Lookup precedes repeating volatile stock checks. Concurrent submissions need one winning record, and a losing participant reads that outcome.

Twenty animals carry aggregate value 2,000. A feed issue of 120 with capitalization active reduces feed value by 120 and raises animal value to 2,120. Animal count remains 20 and animal unit value becomes 106. An attempt to record 21 deaths fails. When reversing a posted pair reconcile the original feed issue, linked revaluation and both stock and financial balances.

## Daily piece-rate work and weekly payroll basis

A daily document belongs to an attendance date, company and shift. A line identifies an activity and item for which a costing rate exists. Use recorded units multiplied by that rate. The employee roster comes from attendance matching company, shift and date. Rebuilding the roster replaces its employee rows. Check-in times shown are informational. Division of the pool is equal per roster row irrespective of hours. Where multiple punches exist, define the selection order explicitly. Without eligible workers, report the unallocated pool before committing the distribution.

An inherited entry behaviour substitutes one for a zero line quantity in amount calculation while quantity totals retain zero. An installation choosing that rule must show the effective billing quantity. A zero-earns-zero policy must enforce that choice on all entry paths. Distinguish these cases in the payroll agreement.

Aggregate submitted unprocessed daily rows over an inclusive interval by employee. A weekly posting creates a salary basis assignment per employee using its total, selected salary structure and period end as effective date. This creates no bank payment. A date-range-only selector may consume daily documents belonging to another company. Require an owning company and source allocation link for a company-scoped run, commit processing flags together with the allocations, and release only owned allocations on cancellation. Reconcile resulting salary basis assignments on a reversal.

Twelve units at 5 and four units at 10 produce 100. Two workers receive 50 each. A subsequent 30 for the first produces bases 80 and 50. With three workers and two currency decimals, a policy awarding residual by ascending employee identity gives 33.34, 33.33 and 33.33. Store the chosen rounding policy and original pool.

## Incoming material price

Apply an enabled guard before submission to positive purchase-order rows at order rate, purchase receipts and stock-updating purchase invoices at valuation rate, positive inbound stock movements with a target warehouse except internal transfer or transfer for manufacture, and positive stock reconciliation quantities at valuation rate. Skip a zero comparison rate. Internal suppliers can be excluded. Resolve warehouse from the row, then target warehouse, then document default. Resolve reference day from posting date, transaction date or current business date.

Select an exact-item rule before a direct item-group rule. Within either target select a dated warehouse match, dated all-warehouse rule, perpetual warehouse match, then perpetual all-warehouse rule. Inclusive start/end dates can each be open. Reject overlapping enabled dated rules or duplicate enabled perpetual rules for the same target and warehouse. Allow a dated override over a perpetual default. Compare on the policy currency and stock unit. A raw order-rate profile must record its currency and unit before an operator compares it with a warehouse-valuation profile.

Let expected rate be E, incoming rate A, allowance T and severe multiplier M. Percentage variance is 100 × |A − E| / E. The zero-expected fallback is zero variance and hard limits can still apply. Use a nonzero rule allowance or the configured default. A rate strictly below an active hard minimum or strictly above an active maximum is severe. Otherwise variance strictly greater than T × M is severe, strictly greater than T is a warning, and all other values pass. A blocking severe override needs an authorized role and nonblank reason. Store rule identity, voucher, warehouse, item, rate basis, severity, identity of the authorizer and reason. Check missing-rule bypass separately. Where a failed posting rolls back, distinguish a durable audit notification from a log written in that posting.

At expected 100, allowance 10% and multiplier 2, rates 90 and 110 pass; rates 80 and 120 warn; rates 79 and 121 are severe. A hard maximum of 115 makes rate 116 severe. If the item’s dated warehouse rate of 100 expires and an all-warehouse item rate of 110 applies, rate 121 has variance exactly 10% and passes. A group rate of 95 does not displace the item match.

## Gate pass and external store availability

A submitted external material transfer or dispatch to a subcontractor initiates a physical gate pass. The worker re-reads submitted status and transfer direction. A return first searches for a draft inbound pass linked to the original outbound movement. Otherwise it reuses an existing pass for the same movement or creates one with company, vehicle, item quantities and direction. A uniqueness rule on movement and handoff purpose prevents two workers from issuing duplicate passes.

After an inventory-affecting movement commits, refresh each linked active store/item mapping from current balances in its selected warehouses. Where configured, subtract reserved balances from actual balances. For sales-unit publication, divide by the stock-units-per-sales-unit conversion and round down to a whole sales unit. Publish against the store-specific product or variation under its parent. A disabled item may publish zero under the selected policy. Duplicate requests can coalesce or recompute the same current quantity.

Warehouse A holds 35 pieces, five reserved. Warehouse B holds one piece, none reserved. A sales box contains six. A store using only A and one using A plus B both initially expose five boxes. An external transfer of 12 pieces A to B creates one outbound pass. The first store now exposes floor((23 − 5) / 6) = 3 boxes. The second still exposes floor((23 − 5 + 13) / 6) = 5. Removing the external flag suppresses the gate pass without suppressing the balance change. A rollback produces no committed quantity change. Track a rejected remote update as a delivery failure, separate from the already posted movement.
