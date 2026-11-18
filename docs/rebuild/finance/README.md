# Financial decisions across document boundaries

These five contracts extend the [accounting](../../domains/financial-accounting.md), [tax](../../domains/taxation-and-pricing.md), [treasury](../../domains/treasury-and-reconciliation.md), [receivables](../../domains/accounts-receivable.md), and [asset](../../domains/assets-and-depreciation.md) chapters. They describe observed behavior of ERPNext release 16.60.0, revision `886ab6ae187244e7f1b852393384ab6019d56264`. Use this revision when resolving a difference with the repository's earlier four-archive baseline. Published manuals explain operator intent. Each chapter links the exact implementation and test evidence that determines the versioned result.

| Business decision | Persistent consequences and evidence |
|---|---|
| [Borrow against receivables](receivables-financing.md) | Select pledged invoices, reclassify the claim, fund and repay the loan, route collections, reverse the journals. |
| [Collect overdue installments](overdue-collection.md) | Reconstruct live principal, distinguish notice charges from invoice principal, recognize collection and evaluate successor notices. |
| [Build a composite asset](composite-asset-cost.md) | Move stock, services and carrying value into the new asset, revalue a draft target after a stock repost and reverse a submitted capitalization. |
| [Select a tax template](tax-rule-selection.md) | Resolve date, category, customer hierarchy, location, priority, conflict and disabled-template decisions before calculating taxes. |
| [Classify bank statement lines](bank-rule-selection.md) | Validate and rank bank rules, evaluate statement text and amount, retain the match for reconciliation. |

[Acceptance vectors](financial-examples.json) carry input records, expected decisions, financial movements, and observable postconditions. Their [JSON Schema](financial-examples.schema.json) defines the interchange form. Financial rows contain positive **integer minor units** of the declared currency. `debit` and `credit` denote journal sides. Figures in the chapters use major units. `entries` describe the change caused by one operation, so use the supplied opening state if testing a sequence. A draft or read operation has an empty posting set. Case identifiers prefixed `FIN` are stable test references for this supplement. These are derived acceptance examples checked against source branches and independent calculations. They have not been executed on a running reference site.

The [financial statement reconciliation](reporting/README.md) follows one opening journal and fourteen operating, investing and financing vouchers through two monthly trial balances, income statements, balance sheets and indirect cash-flow statements. Its fixture provides the expected balances of every leaf account and the report control totals.

[Posted invoice, valuation and settlement examples](posting/README.md) exercise 26 tax and currency scenarios against source-test expectations and derived accounting cases. They distinguish each voucher's postings, including the separate exchange journal and the stock valuation share of a purchase charge.

Run the [offline verifier](verify.py) from the blueprint checkout with Python 3.10 or later. It reconstructs the 25 decision outcomes and their account movements, the 26 posting cases and their 30 named journals, 182 monthly financial-report amounts and 24 parent/subsidiary translation outputs. Monetary inputs are integer minor units. Ratios and exchange rates retain precision through the stated rounding point. The verifier covers the supplied profiles, including exact minor-unit dunning interest and nonzero stock allocation bases. [Committed document and report evidence](../live/README.md) covers a separately executed receipt-to-cash scenario.

```sh
python3 docs/rebuild/finance/verify.py
```
