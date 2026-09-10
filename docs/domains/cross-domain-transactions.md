# Cross-domain transactions

## Local record and calculation contracts

[General ledger entry](../../schemas/data/record-types/general_ledger_entry.json); [Party settlement entry](../../schemas/data/record-types/payment_ledger_entry.json); [Stock movement](../../schemas/data/record-types/stock_ledger_entry.json); [Payment](../../schemas/data/record-types/payment_entry.json); [Journal](../../schemas/data/record-types/journal_entry.json). These local definitions provide the persistent fields, relationships, defaults and permissions. The rules below explain their business meaning and lifecycle consequences.

[Financial calculations](../../schemas/mathematics/financial-calculations.json) define evaluation order and numerical boundaries. [Accounting acceptance cases](../../schemas/mathematics/accounting-acceptance-cases.json) provide complete journal events, expected closing balances, settlement outcomes and rejection conditions. These are independently checked arithmetic expectations; they do not claim execution of an entire application.

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

Workforce behaviour extends employee, time record, payment and project controllers. Payment submission, cancellation and submitted updates recalculate expense-claim payment state. Unreconciliation also refreshes that state. Journal submission updates claims, final employment settlement and salary withholding; cancellation additionally removes salary references where applicable. These are shared financial operations with workforce consequences, not isolated payroll screens.

Employee creation links hiring and onboarding records. Project and task updates feed employment onboarding or separation progress. A change in a holiday list invalidates calendar state used elsewhere.

Relationship integration adds contact validation, activity linkage, communication updates, deal-to-customer conversion and sales-order customer creation. When the relevant integration is enabled, product changes maintain relationship-side product projections. Deal-to-customer conversion and customer creation on an order are likewise configuration-gated. User permission and record-share changes synchronise related visibility. A combined application must preserve these effects without recursively creating the same record or confusing a display projection with the authoritative product.

## Global validation

Enterprise document validation applies service targets, running-deletion guards and company-master eligibility. Selected records additionally validate accounting periods and pre-submission requirements. These global hooks can reject an otherwise locally valid transaction.

## Cancellation dependencies

The automatic cancellation graph has exemptions. Payments may be unlinked instead of cancelled. Financial, stock, settlement and advance ledger records use their own reversal policies rather than ordinary document cascade. Closing-balance records also have specialised cancellation logic. These distinctions are necessary to preserve audit history and avoid reversing the same business consequence twice.

A replacement must explicitly model dependency edges as cancel, unlink, reverse, recalculate or block. A blanket cascade-delete relationship is not equivalent.

## Integration acceptance scenarios

1. Receive a partial purchase order, invoice a different permitted portion, pay part of the invoice, and cancel a permitted descendant. Compare remaining ordered, received and billed quantities with the supplier balance and inventory value.
2. Reserve a sales order, deliver part, invoice the delivery, collect a partial payment and close the unused row. Compare available stock, order progress, receivable and cash without inventing completion for the closed row.
3. Create an employee advance, record an expense in another currency and settle it through a payment. Reconcile the employee advance, expense payable and exchange differences.
4. Submit payroll, create its accrual journal, then cancel a permitted journal. Confirm salary references and withholding status follow the specified cancellation path.
5. Convert a deal to a customer, create an order and change a linked product or permission. Confirm shared identity, projections and record visibility remain consistent.
6. Make a late inventory value adjustment affecting sold or consumed goods. Track the inventory and financial reposting completion state before declaring reports final.

These are implementation acceptance obligations assembled from source coupling. Their exact numeric fixtures should use the corresponding mathematical catalog and a fixed configuration profile.

## Shared event boundaries and conservation checks

A successful commercial event can update progress, inventory, general ledger, settlement, tax history and reporting queues. Its persistent event identity belongs to the commercial document; each generated consequence retains its own identity and link to that event. Synchronous consequences must be committed together or rolled back together. When a defined operation deliberately processes intervals or documents in separate commits, return each completed unit and the next recoverable unit rather than reporting the entire batch as one success. Deferred recognition and valuation reposting have such independently visible progress states.

The following reconciliation equations are business checks, with exact account choices supplied by the selected policy:

| Flow | Conservation check | Why the separate records matter |
|---|---|---|
| Purchase receipt followed by invoice | Receipt clearing credit less eligible invoice clearing debits and return effects equals unbilled receipt obligation | Receipt cost, invoice cost and quantity can differ |
| Customer invoice followed by receipts and credits | Original claim plus debit adjustments less credits and applications equals remaining claim | A later allocation can change settlement without changing cash |
| Supplier invoice with withholding | Supplier amount due plus withheld liability equals gross liability before withholding | Tax remittance and supplier payment settle different creditors |
| Stock issue and asset repair capitalization | Inventory reduction equals expensed consumption plus capitalized consumption | Capitalization reclassifies the issue expense instead of issuing the stock twice |
| Deferred service | Posted recognized amount plus remaining deferred amount equals original deferred amount after adjustments | Due dates and cash receipts do not measure service delivery |
| Foreign claim settlement | Historical company claim plus exchange adjustments less company settlement equals residual company claim | Foreign outstanding can reach zero while a company-currency residual still needs its exchange entry |

Check each equation for one company and currency context, then aggregate. Combining currencies without conversion or companies without intercompany treatment does not yield a meaningful conservation test.

## Cancellation dependency decision contract

Each dependency edge declares one behavior: block cancellation; cancel the dependent commercial record first; reverse generated history; unlink an allocation; refresh a derived balance or status; or retain history without another posting. The cancellation coordinator must detect a consequence already reversed by another edge. A ledger reversal is not a request to cascade-delete the commercial records that explain it.

For a customer invoice paid in part, a permitted cancellation path must address its allocation before making the claim ineffective. For a bank statement matched to a payment, statement cancellation unlinks clearance while retaining the payment's bank movement. For an asset repair, cancelling capitalization and cancelling the material issue are separate consequences. For a payroll accrual, reversing the journal can refresh salary and withholding references while the preparation record's lifecycle remains independent. For an order-row closure, remove commitment eligibility and update reservations under its policy while retaining any invoice liability already posted.

The replacement's cancellation result lists original record, dependent identity, edge behavior, before and after lifecycle, financial reversal identities, settlement changes and remaining blockers. This explicit result shape is a proposed service contract that makes the observed distinct cancellation mechanisms reviewable; the source model alone does not provide a universal cancellation-response object.

## Complete integrated acceptance sequence

The machine-readable accounting cases use event sequences rather than isolated balance labels. `receipt_bill_partial_payment_and_return` checks received stock, clearing, payable and bank together. `customer_partial_payment_credit_and_reversal` checks the customer claim, tax, revenue and cash after every stage. `capitalized_repair_reclassifies_existing_expense` checks invoice liability, inventory issue, expense clearing and fixed-asset cost. `customer_advance_later_applied` checks that later application does not duplicate cash. Each event must independently balance in company currency; each sequence states its expected ending account balances.

These examples do not make all cross-domain combinations equivalent. Their explicit profiles state stock policy, tax rate, currency and financial-book assumptions. Extend them by varying one policy at a time, then introduce combinations with known shared dependencies. In particular, test a returned stock line already consumed in manufacturing, a backdated cost adjustment after financial closing, and payment of an invoice whose withheld tax was already remitted as separate operational acceptance cases rather than assuming the uncomplicated examples cover them.
