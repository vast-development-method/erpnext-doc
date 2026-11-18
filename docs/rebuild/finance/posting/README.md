# Posted invoice, valuation and settlement examples

The [acceptance cases](posting-cases.json) and [case schema](posting-cases.schema.json) use integer currency minor units. Each case names a business operation, supplies its inputs, and gives the document, stock or settlement outputs plus journal deltas in company currency. Monetary rows are signed debit-positive. Within each named journal the sum must be zero. Compare the journals before aggregating them by account. Several workflows produce the same net balance by different documents, and reversing a payment must identify its own linked exchange journal. The evidence profile is ERPNext `v16.60.0`, revision `886ab6ae187244e7f1b852393384ab6019d56264`.

| Contract | Cases and main decision |
|---|---|
| [Invoice tax, discount and residual allocation](invoice-tax-and-discount.md) | Included percentage and unit charge, net versus gross discount, per-row versus document rounding, exempt child rows, different compound bases and historic returns. |
| [Purchased tax and stock acquisition cost](purchase-tax-and-stock.md) | Recoverable portion, inventory cost, quantity fallback, stock-only freight, mixed services, rejected goods and partial returns. |
| [Realized exchange difference on settlement](realized-exchange.md) | Source claim rate, settlement rate, payable sign inversion, partial allocation and separate exchange journals. |

Cases marked `upstream-test` reproduce numerical assertions in the linked test sources. Other explicitly marked derived examples exercise another branch or reconcile postings from those rules. Local validation covers fixture shape, arithmetic and balanced legs. Execution on an installed reference application is a separate qualification step.
