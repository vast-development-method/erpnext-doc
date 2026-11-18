# Business transactions and financial control

The [receipt-to-cash example](receipt-to-cash.md) follows twelve linked vouchers from two supplier receipts through conversion, delivery, invoicing, return and settlement. It shows when stock changes, which account each event affects, how a partial payment survives a credit, and how the closing amounts appear in six reports.

| Business question | Specification |
|---|---|
| When does an event post, who may authorize it, and which prior records must survive a reversal? | [Financial accounting](financial-accounting.md), [cross-domain transactions](cross-domain-transactions.md), [line closure and progress](../operations/transaction-progress-and-row-closure.md) |
| How does a lead become an approved order with a price, delivery promise and collectible invoice? | [Customer relationships](../people-and-services/customer-relationships-and-sales.md), [sales pipeline and approval](sales-pipeline-and-approval.md), [delivery promises and pro forma billing](order-promises.md), [pricing and rewards](pricing-and-loyalty.md) |
| How are a supplier's delivery, invoice and liability matched? | [Procurement and fulfilment](procurement-and-fulfilment.md), [supplier payables](accounts-payable.md), [purchase tax and asset cost](purchase-tax-and-stock.md) |
| How does the system select a tax treatment and calculate the amount? | [Tax and pricing calculations](taxation-and-pricing.md), [tax rule selection](tax-rule-selection.md), [inclusive charges, discounts and rounding](invoice-tax-and-discount.md) |
| How are customers billed, financed and collected? | [Receivables](accounts-receivable.md), [overdue collection](overdue-collection.md), [receivables financing](receivables-financing.md), [recurring billing](recurring-billing.md) |
| How do treasury instructions, cash, exchange differences and bank clearance relate? | [Payment instructions and bank guarantees](payment-instructions.md), [treasury and reconciliation](treasury-and-reconciliation.md), [realized exchange](realized-exchange.md), [statement imports](bank-feed.md), [statement rules](bank-rule-selection.md) |
| Which costs enter asset or project measures? | [Asset capitalization and depreciation](assets-and-depreciation.md), [composite assets](composite-asset-cost.md), [project costs and margin](project-costing.md) |
| How are budgets, accruals, period closing and reporting linked? | [Deferred recognition and financial control](deferred-recognition-and-financial-control.md), [journal to four financial statements](journal-to-statements.md), [group currency translation](group-currency-translation.md) |
| How do changes in share ownership relate to actual accounting? | [Numbered shares and company folios](equity-register.md) |
| How are appointments, tender sessions, sales targets and customer-facing batch operations handled? | [Appointments and service billing](../people-and-services/customer-appointments.md), [retail session close](retail-closing.md), [commercial performance](commercial-performance.md), [bulk conversions, portal parties and exchange codes](batch-portal-and-codes.md) |

## Numerical inputs and expected results

Amounts in the posting sets use the units declared by each example. In the receipt-to-cash case, a decimal string represents a major-unit amount. In the two-month journal, an integer is a minor-unit amount. Preserve the example’s precision, dates, currency pair, operation order and account roles when reproducing a result.

| Examples | Interpret alongside |
|---|---|
| [Financing, dunning, tax selection, bank rules and capitalization](examples/financial-decisions.json) | Read the input, decision, account movements and resulting state together. |
| [Invoice posting and exchange cases](examples/invoice-posting.json) | Reconcile tax, inventory, party control, bank charges and realized gains or losses. |
| [Journal to financial statements](examples/journal-to-statements.json) and [group currency translation](examples/group-translation.json) | Compare gross turnover as well as net balances, period movement, reporting currency and consolidated scope. |
| [Receipt-to-cash event sequence](examples/receipt-to-cash.json) | Compare the party balance and stock ledger after each step before comparing closing accounts. |
| [Commercial decisions](examples/commercial-decisions.json) and their [input assumptions](examples/commercial-scenarios.json) | Apply the declared units and conditions for each operation. |
| [Commissions, targets, installments and country templates](examples/commercial-reporting.json) | Distinguish sales credit, invoice coverage and receipt of cash. |
| [Calculation definitions and event cases](../calculations/README.md) | Reference the full calculation, precision, conditions and related transaction cases. |
