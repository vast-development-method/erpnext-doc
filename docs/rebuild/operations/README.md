# Warehouse, supply and production contracts

[Physical operations](../../operations/README.md) covers demand, ordering, movement, production and quality control. Use the following transactions to trace the record boundaries, quantity decisions and financial effects.

| Operation | Record boundary | Rebuild contract |
|---|---|---|
| Net dated sales demand and component demand | Forecast → master schedule → MRP report | [Forecast shares, critical-path lead times and time-phased netting](../../operations/planning.md) · [evidence](planning.md) |
| Turn shortages into demand for purchase, transfer or production | Reorder rule/bin or production-plan row → material request | [Thresholds, minimum order sizes, unit grids and draft-aware remaining quantities](../../operations/replenishment.md) · [evidence](replenishment.md) |
| Collect bids and approve future sourcing | Request + supplier invitation → draft quotation; supplier period → purchasing flags | [Portal authority, zero-price quotation, weighted score and cutoffs](../../operations/sourcing.md) · [evidence](sourcing.md) |
| Reconcile and close stock | Count/valuation comparison → stock and financial ledgers → company closing snapshot | [Explicit zero, tracked quantities, valuation layers and concurrent closing](../../operations/inventory-control.md) · [evidence](inventory-control.md) |
| Cost and return supplier-manufactured goods | Subcontract order → finished and secondary output → return and service receipt | [Cost pools, charge reversal, cumulative quantities and order-merge conditions](../../operations/subcontract-cost.md) · [evidence](subcontract-cost.md) |
| Establish evidence for stock and production release | Inspection → specific transaction row; quality review → goal | [Identity, readings, approval policy, review scheduling and corrective action](../../operations/quality.md) · [evidence](quality.md) |
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

The closing worker needs concurrent-session tests with a posting, cancellation and in-flight valuation repost. Quotation duplication and plan request generation need simultaneous writers, effective permissions and persistent rollback evidence. Default permission records may be refined by a site's role and company rules. Mixed-currency subcontract receipts, batch-specific revaluation, reservation handoff, composite-component account mapping, multilevel capacity calendars and valuation replay under the configured costing policy need representative site fixtures. The discovered non-submittable master schedule and inherited-template reorder branch are documented at their decision sites for verification before treating them as active business workflows.

## Posting and status decision evidence

The [transaction progress rules](../../operations/transaction-progress-and-row-closure.md) define whole-document closure, row-capped progress and the optional independent row-closure capability. The common percentage covers every item of the parent. Ordinary delivery billing uses the amount allocated to the delivery row, with an adjustment for partial returns. The zero-net order/delivery path uses quantities and rounds the quotient to two places before multiplying by 100. Evidence paths for those decisions follow.

| Behavior | Decision evidence |
|---|---|
| Parent close with reserved stock, credit and blanket order on reopening | [Sales order](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/doctype/sales_order/sales_order.py#L672-L704) · [Purchase order](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/doctype/purchase_order/purchase_order.py#L538-L555) |
| Capped row magnitudes, rounded percentages and billing-state boundary | [Progress and labels](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/status_updater.py#L686-L725) · [Zero-value reference document](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/status_updater.py#L788-L838) · [Division precision](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/utils/data.py#L1353-L1364) |
| Monetary billing for deliveries and allocation from the order | [Return adjustment and percentage](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/stock_controller.py#L1800-L1823) · [Direct invoice sums](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/sales_invoice/sales_invoice.py#L2435-L2468) · [Order allocation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/delivery_note/delivery_note.py#L867-L941) |
