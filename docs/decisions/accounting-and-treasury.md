# Accounting controls, tax and treasury

Posting controls use the company, accounting period, account and currency of the selected operation. Bank charges and allocations are tested in their respective monetary units.

## Account

Logical record `accounting.account`. [Field definitions and declared grants](../../schema/entities/accounting-01.json)

| Operation | Refuse when |
|---|---|
| Change account currency | The proposed currency differs from the currency already established by postings to the account. |

## Accounting dimension

Logical record `accounting.accounting_dimension`. [Field definitions and declared grants](../../schema/entities/accounting-01.json)

| Operation | Refuse when |
|---|---|
| Define an accounting dimension | The selected record type is a child row or a singleton setting. Dimension values require independently identifiable records. |
| Create an accounting dimension | A dimension already uses the selected record type. |
| Set company defaults for a dimension | Two rows specify the same company. |

## Accounting period

Logical record `accounting.accounting_period`. [Field definitions and declared grants](../../schema/entities/accounting-01.json)

| Operation | Refuse when |
|---|---|
| Define a closed accounting period | Its start is later than its end. |
| Define a closed accounting period | Its end is later than the current business date. |

## Cost center

Logical record `accounting.cost_center`. [Field definitions and declared grants](../../schema/entities/accounting-01.json)

| Operation | Refuse when |
|---|---|
| Assign a cost centre’s parent | The selected parent is missing or is not a grouping node. |
| Assign a cost centre’s parent | The parent belongs to a different company. |
| Convert a cost centre group to a posting node | Child nodes exist. |
| Convert a posting cost centre to a group | The node already has general ledger entries. |

## Bank transaction

Logical record `accounting.bank_transaction`. [Field definitions and declared grants](../../schema/entities/accounting-01.json)

| Operation | Refuse when |
|---|---|
| Allocate a bank statement row | The same voucher kind and identity appears more than once among its allocations. |
| Add bank reconciliation allocations | The bank movement’s remaining unallocated amount is zero or negative. |
| Normalize a fee included in a withdrawal | The nonzero included fee exceeds the withdrawal. |
| Normalize a fee excluded from a deposit | Deducting the fee from the positive deposit produces a negative amount. |

## Payment reconciliation

Logical record `accounting.payment_reconciliation`. [Field definitions and declared grants](../../schema/entities/accounting-02.json)

| Operation | Refuse when |
|---|---|
| Reconcile within an accounting dimension | A specified value falls outside the operator’s restricted set of permitted values. |
| Apply a positive payment allocation | A nonzero proposed allocation to an identified invoice exceeds the amount on its payment row. |

## Payment terms template

Logical record `accounting.payment_terms_template`. [Field definitions and declared grants](../../schema/entities/accounting-02.json)

| Operation | Refuse when |
|---|---|
| Define installment-based payment allocation | A template requests allocation by payment term but a row has no term. |

## Period closing voucher

Logical record `accounting.period_closing_voucher`. [Field definitions and declared grants](../../schema/entities/accounting-02.json)

| Operation | Refuse when |
|---|---|
| Select a period-closing account | The account’s root classification is neither liability nor equity. |
| Select a period-closing account | The account’s company differs from that of the closing document. |
| Select a period-closing account | The account is a group node. |
| Select a period-closing account | The account is disabled. |
| Select a period-closing account | Account currency differs from company currency. |
| Define a period close | The selected endpoint lies after fiscal-year end. |

## Sales taxes and charges template

Logical record `accounting.sales_taxes_and_charges_template`. [Field definitions and declared grants](../../schema/entities/accounting-04.json)

| Operation | Refuse when |
|---|---|
| Select a default sales tax template | A disabled template is marked as the default. |

## Tax withholding category

Logical record `accounting.tax_withholding_category`. [Field definitions and declared grants](../../schema/entities/accounting-04.json)

| Operation | Refuse when |
|---|---|
| Set a withholding-rate window | Its start is on or after its end. A one-day interval with equal dates fails this comparison. |
| Set a withholding company account | The company has already been included in the category. |
| Set withholding thresholds | Both single-event and cumulative thresholds are nonzero and the cumulative threshold is smaller. |

## Lower deduction certificate

Logical record `regional_accounting.lower_deduction_certificate`. [Field definitions and declared grants](../../schema/entities/regional-accounting.json)

| Operation | Refuse when |
|---|---|
| Delete a reduced-withholding certificate | The certificate has been used. Existing tax history retains its authorizing certificate. |
