# French Accounting reports

The [structured report details](french-accounting.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Bank Transaction Categories

Script Report. The reference record is Bank Transaction. Declared inputs include `company`, `period`, `transaction_type`.

The direct return positions are columns / data / absent / chart data. Named output fields constructed in this report include `category`, `amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/scopen-coop/erpnext_france/blob/10744bfd69e47e19a86672713c0574fe0a35dfd0/erpnext_france/erpnext_france/report/bank_transaction_categories/bank_transaction_categories.py#L8) [Declaration](https://github.com/scopen-coop/erpnext_france/blob/10744bfd69e47e19a86672713c0574fe0a35dfd0/erpnext_france/erpnext_france/report/bank_transaction_categories/bank_transaction_categories.json) [Module bindings](procedures/french-accounting--bank-transaction-categories-bindings.json) · [Ordered report procedures](procedures/french-accounting--bank-transaction-categories-1.json)

## Fichier des Ecritures Comptables [FEC]

Script Report. The reference record is GL Entry. Declared inputs include `company`, `fiscal_year`, `from_date`, `to_date`, `hide_already_exported`.

The direct return positions are COLUMNS / get result. [Row procedure](https://github.com/scopen-coop/erpnext_france/blob/10744bfd69e47e19a86672713c0574fe0a35dfd0/erpnext_france/erpnext_france/report/fichier_des_ecritures_comptables_%5Bfec%5D/fichier_des_ecritures_comptables_%5Bfec%5D.py#L151) [Declaration](https://github.com/scopen-coop/erpnext_france/blob/10744bfd69e47e19a86672713c0574fe0a35dfd0/erpnext_france/erpnext_france/report/fichier_des_ecritures_comptables_%5Bfec%5D/fichier_des_ecritures_comptables_%5Bfec%5D.json) [Module bindings](procedures/french-accounting--fichier-des-ecritures-comptables-fec-bindings.json) · [Ordered report procedures](procedures/french-accounting--fichier-des-ecritures-comptables-fec-1.json)

## General Ledger

Script Report. The reference record is GL Entry. Declared inputs include `company`, `finance_book`, `from_date`, `to_date`, `account`, `voucher_no`, `against_voucher_no`, `party_type`, `party`, `party_name`, `categorize_by`, `tax_id`, `presentation_currency`, `cost_center`, `project`, `include_dimensions`, `disable_opening_balance_calculation`, `show_opening_entries`, `include_default_book_entries`, `show_cancelled_entries`, `show_net_values_in_party_account`, `show_amount_in_company_currency`, `convert_at_reporting_date_rate`, `add_values_in_transaction_currency`, `show_remarks`, `ignore_err`, `ignore_cr_dr_notes`.

Shares the general-ledger report name. The effective registered module determines the procedure. This regional declaration extends the standard browser controls. Named output fields constructed in this report include `accounting_entry_number`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/scopen-coop/erpnext_france/blob/10744bfd69e47e19a86672713c0574fe0a35dfd0/erpnext_france/erpnext_france/report/general_ledger/general_ledger.py#L14) [Declaration](https://github.com/scopen-coop/erpnext_france/blob/10744bfd69e47e19a86672713c0574fe0a35dfd0/erpnext_france/erpnext_france/report/general_ledger/general_ledger.json) [Module bindings](procedures/french-accounting--general-ledger-bindings.json) · [Ordered report procedures](procedures/french-accounting--general-ledger-1.json)

## Monthly Recurring Revenue

Script Report. The reference record is Subscription. Declared inputs include `company`, `filter_based_on`, `period_start_date`, `period_end_date`, `from_fiscal_year`, `to_fiscal_year`, `periodicity`.

Named output fields constructed in this report include `customer`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/scopen-coop/erpnext_france/blob/10744bfd69e47e19a86672713c0574fe0a35dfd0/erpnext_france/erpnext_france/report/monthly_recurring_revenue/monthly_recurring_revenue.py#L13) [Declaration](https://github.com/scopen-coop/erpnext_france/blob/10744bfd69e47e19a86672713c0574fe0a35dfd0/erpnext_france/erpnext_france/report/monthly_recurring_revenue/monthly_recurring_revenue.json) [Module bindings](procedures/french-accounting--monthly-recurring-revenue-bindings.json) · [Ordered report procedures](procedures/french-accounting--monthly-recurring-revenue-1.json)

## Transaction Log Report

Script Report. The reference record is Transaction Log.

The direct return positions are columns / data. Named output fields constructed in this report include `chain_integrity`, `reference_doctype`, `reference_name`, `owner`, `modified_by`, `timestamp`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/scopen-coop/erpnext_france/blob/10744bfd69e47e19a86672713c0574fe0a35dfd0/erpnext_france/erpnext_france/report/transaction_log_report/transaction_log_report.py#L11) [Declaration](https://github.com/scopen-coop/erpnext_france/blob/10744bfd69e47e19a86672713c0574fe0a35dfd0/erpnext_france/erpnext_france/report/transaction_log_report/transaction_log_report.json) [Module bindings](procedures/french-accounting--transaction-log-report-bindings.json) · [Ordered report procedures](procedures/french-accounting--transaction-log-report-1.json)

## Transactions Tax Summary

Script Report. The reference record is GL Entry. Declared inputs include `company`, `period_start_date`, `period_end_date`, `transaction_type`.

The report returns the result of `get_data`. Named output fields constructed in this report include `date`, `reference_doctype`, `reference_document`, `item_code`, `base_grand_total`, `base_net_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/scopen-coop/erpnext_france/blob/10744bfd69e47e19a86672713c0574fe0a35dfd0/erpnext_france/erpnext_france/report/transactions_tax_summary/transactions_tax_summary.py#L12) [Declaration](https://github.com/scopen-coop/erpnext_france/blob/10744bfd69e47e19a86672713c0574fe0a35dfd0/erpnext_france/erpnext_france/report/transactions_tax_summary/transactions_tax_summary.json) [Module bindings](procedures/french-accounting--transactions-tax-summary-bindings.json) · [Ordered report procedures](procedures/french-accounting--transactions-tax-summary-1.json)
