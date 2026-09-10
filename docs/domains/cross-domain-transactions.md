# Cross-domain transactions

## Shared business consequences

The application combines commitments, execution, accounting and settlement. Each is an independently meaningful record family with explicit links. The following matrix states the integration obligations; the linked domain specifications supply the precise policy-dependent posting rules and formulas.

| Operation | Operational consequence | Financial consequence | Required linked evidence |
|---|---|---|---|
| Submit sales order | Commitment, schedules, reservation and credit exposure | Usually no revenue recognition at order submission | Party, company, source rows, prices, tax and credit policy |
| Submit purchase order | Supply commitment, expected quantities and schedules | Commitment and budget effects under policy; not automatically supplier debt | Supplier, company, items, dimensions and downstream row identity |
| Receive purchased goods | Accepted and rejected quantities, stock location and valuation | Inventory and received-not-invoiced treatment where perpetual accounting applies | Order row, valuation components, warehouse and posting context |
| Record supplier invoice | Billed progress and supplier obligation | Payable, expense or receipt clearing, tax and valuation differences | Receipt or order references, currencies, tax rows and posting dimensions |
| Deliver goods | Physical issue and delivered progress | Inventory reduction and cost recognition under policy | Sales row, warehouse, serial or batch allocation and valuation basis |
| Record customer invoice | Billing progress, credit exposure and customer obligation | Receivable, revenue, tax and optional stock effects | Delivery or order reference; stock-update policy prevents duplicate movement |
| Receive or make payment | Settlement allocation and payment-request progress | Bank or cash, party control, deductions, exchange difference and advance treatment | Invoice or advance allocation, account currency and bank references |
| Cancel or reverse a transaction | Remove or reverse its qualifying progress contributions | Policy-specific reversal and preserved history | Original voucher, dependent documents and reconciliation status |
| Close an unfinished row | Remove remaining commitment and follow-up eligibility | No implied receipt, invoice, cash movement or financial write-off | Row identity and parent close policy |
| Complete manufacturing | Consume materials, record output and operational completion | Transfer and allocate inventory cost, operation cost and variance | Work order, bill of materials, consumption, secondary output and costing policy |
| Submit payroll preparation | Payroll submitted state and generated draft salary statements | No automatic accrual merely from preparation submission | Employee selection, payroll period and preparation settings |
| Submit salary statements through payroll processing | Submitted accepted statements and employee liability state | Expense, payable and relevant deduction accrual through the separate posting operation | Employee, period, dimensions and component account mapping |
| Pay employee expense | Claim settlement progress and advance adjustment | Bank, employee payable and exchange differences where applicable | Claim, sanctioned amount, advance and payment allocation |
| Bill project time | Billed hours and project revenue progress | Customer invoice and associated revenue or cost effects | Original time rows, rates, currency and project dimensions |

These effects must be taken from the current service paths, not inferred from a form title. See [financial accounting](financial-accounting.md), [inventory and valuation](inventory-and-valuation.md), [payroll and benefits](payroll-and-benefits.md), and [transaction progress](transaction-progress-and-row-closure.md).

## Composition of shared records

Workforce behaviour extends employee, time record, payment and project controllers. Payment submission, cancellation and submitted updates recalculate expense-claim payment state. Unreconciliation also refreshes that state. Journal submission updates claims, final employment settlement and salary withholding; cancellation additionally removes salary references where applicable. These are shared financial operations with workforce consequences, not isolated payroll screens. Evidence: source-artifact-1e30c9d20ea8e211402e lines 162–222.

Employee creation links hiring and onboarding records. Project and task updates feed employment onboarding or separation progress. A change in a holiday list invalidates calendar state used elsewhere. Evidence: source-artifact-1e30c9d20ea8e211402e lines 184–249.

Relationship integration adds contact validation, activity linkage, communication updates, deal-to-customer conversion and sales-order customer creation. When the relevant integration is enabled, product changes maintain relationship-side product projections. Deal-to-customer conversion and customer creation on an order are likewise configuration-gated. User permission and record-share changes synchronise related visibility. A combined application must preserve these effects without recursively creating the same record or confusing a display projection with the authoritative product. Evidence: source-artifact-85bf1e834e4e4d148fa6 lines 154–220.

## Global validation

Enterprise document validation applies service targets, running-deletion guards and company-master eligibility. Selected records additionally validate accounting periods and pre-submission requirements. These global hooks can reject an otherwise locally valid transaction. Evidence: source-artifact-84576302b4033b578065 lines 387–414.

## Cancellation dependencies

The automatic cancellation graph has exemptions. Payments may be unlinked instead of cancelled. Financial, stock, settlement and advance ledger records use their own reversal policies rather than ordinary document cascade. Closing-balance records also have specialised cancellation logic. These distinctions are necessary to preserve audit history and avoid reversing the same business consequence twice. Evidence: source-artifact-84576302b4033b578065 lines 471–485.

A replacement must explicitly model dependency edges as cancel, unlink, reverse, recalculate or block. A blanket cascade-delete relationship is not equivalent.

## Integration acceptance scenarios

1. Receive a partial purchase order, invoice a different permitted portion, pay part of the invoice, and cancel a permitted descendant. Compare remaining ordered, received and billed quantities with the supplier balance and inventory value.
2. Reserve a sales order, deliver part, invoice the delivery, collect a partial payment and close the unused row. Compare available stock, order progress, receivable and cash without inventing completion for the closed row.
3. Create an employee advance, record an expense in another currency and settle it through a payment. Reconcile the employee advance, expense payable and exchange differences.
4. Submit payroll, create its accrual journal, then cancel a permitted journal. Confirm salary references and withholding status follow the specified cancellation path.
5. Convert a deal to a customer, create an order and change a linked product or permission. Confirm shared identity, projections and record visibility remain consistent.
6. Make a late inventory value adjustment affecting sold or consumed goods. Track the inventory and financial reposting completion state before declaring reports final.

These are implementation acceptance obligations assembled from source coupling. Their exact numeric fixtures should use the corresponding mathematical catalog and a fixed configuration profile.
