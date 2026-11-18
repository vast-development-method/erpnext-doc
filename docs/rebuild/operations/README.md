# Warehouse, supply and production contracts

This supplement follows operational decisions through ERPNext v16.60.0, pinned to [886ab6a](https://github.com/frappe/erpnext/tree/886ab6ae187244e7f1b852393384ab6019d56264). The [existing inventory](../../domains/inventory-and-valuation.md), [manufacturing](../../domains/manufacturing-and-subcontracting.md), [procurement](../../domains/procurement-and-fulfilment.md), [quality](../../domains/quality-and-maintenance.md) and [asset](../../domains/assets-and-depreciation.md) chapters describe the original development-snapshot baseline. Each chapter below identifies the v16 decisions and record boundaries a replacement can verify independently.

| Operation | Record boundary | Rebuild contract |
|---|---|---|
| Net dated sales demand and component demand | Forecast → master schedule → MRP report | [Forecast shares, critical-path lead times and time-phased netting](planning.md) |
| Turn shortages into demand for purchase, transfer or production | Reorder rule/bin or production-plan row → material request | [Thresholds, minimum order sizes, unit grids and draft-aware remaining quantities](replenishment.md) |
| Collect bids and approve future sourcing | Request + supplier invitation → draft quotation; supplier period → purchasing flags | [Portal authority, zero-price quotation, weighted score and cutoffs](sourcing.md) |
| Reconcile and close stock | Count/valuation comparison → stock and financial ledgers → company closing snapshot | [Explicit zero, tracked quantities, valuation layers and concurrent closing](inventory-control.md) |
| Cost and return supplier-manufactured goods | Subcontract order → finished and secondary output → return and service receipt | [Cost pools, charge reversal, cumulative quantities and order-merge conditions](subcontract-cost.md) |
| Establish evidence for stock and production release | Inspection → specific transaction row; quality review → goal | [Identity, readings, approval policy, review scheduling and corrective action](quality.md) |
| Capitalize manufactured equipment | Stock/service/source assets → composite fixed asset → work in progress and GL | [Layered issues, balanced disposal, repost delta and cancellation](capitalization.md) |

## Machine-readable acceptance

The [43 vectors](acceptance.json) conform to a [JSON Schema 2020-12 tagged union](acceptance.schema.json) with 14 operation-specific input and expected-output shapes. Each case supplies a stable identifier, a neutral operation, prior state or inputs, and an expected outcome. An implementation adapter supplies the operation, compares only the declared outputs and verifies the documented side effects. Arithmetic in monetary examples assumes two-decimal amounts and exact decimal account totals. All related resources use company currency unless another currency is stated.

| Family | Fixture assumptions |
|---|---|
| Forecast and scheduling | The split fixture uses an integer forecast and indivisible stock unit. Slice outcomes retain zero positions to show attribution; the actual scheduler omits satisfied rows. Critical-path fixtures use an explicit daily manufacturing capacity and already-computed child durations. |
| Supplier scoring and portal | Recency fixtures select the configurable expression score / (1 + period number). Period weights sum to 100. The portal fixture has one valid item row and a nonzero, applicable price-list default; a rejected command adds zero drafts. |
| Replenishment | Valid active item and company, eligible warehouse, automatic requests enabled; plan fixtures compare only the quantity of a newly proposed request. No request means zero. |
| Count and closing | Single untracked ordinary count, permissible non-stock difference account, prior stock exists, two decimal amounts and no future conflicts. Closure result describes worker publication, including a skipped worker when the document is already cancelled. |
| Subcontracting | Single finished row, residual percentage shared between one percentage output and the finished item. Accepted-return examples use one original row so original charge allocation is unambiguous. |
| Goal review | Inputs are the current objective statuses; outcome is the review header, independently of its corrective actions. |
| Fixed asset | FIFO, perpetual inventory, target work-in-progress account, ordinary depreciating source asset and no salvage, sale or gain/loss leg. The second case reprices the same consumption under revised history and shows the new total position. |

The fixtures are source-derived examples, not recorded live-site transactions. Schema validation checks shape and allowed outcomes. Checking values requires executing the operation or an independent numerical oracle. Upstream regression cases linked in each chapter provide setup for a live reference run, including partial failures, authorisation and concurrency.

## Qualification boundaries

The closing worker needs concurrent-session tests with a posting, cancellation and in-flight valuation repost. Quotation duplication and plan request generation need simultaneous writers, effective permissions and persistent rollback evidence. ERPNext's default permission records may be refined by a site's role and company rules. Mixed-currency subcontract receipts, batch-specific revaluation, reservation handoff, composite-component account mapping, multilevel capacity calendars and version-specific valuation replay need representative site fixtures. The discovered non-submittable master schedule and inherited-template reorder branch are documented at their decision sites for verification before treating them as active business workflows.
