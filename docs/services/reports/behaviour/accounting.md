# Accounting reports

The [structured report details](accounting.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Account Balance

Script Report. The reference record is Bank Account. Declared inputs include `company`, `report_date`, `root_type`, `account_type`.

The direct return positions are columns / data. Named output fields constructed in this report include `account`, `currency`, `balance`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/account_balance/account_balance.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/account_balance/account_balance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-003.md#op-43c91e496a5776)

## Accounts Payable

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `report_date`, `finance_book`, `cost_center`, `project`, `party_account`, `ageing_based_on`, `age_as_on`, `range`, `payment_terms_template`, `party_type`, `party`, `supplier_group`, `group_by_party`, `based_on_payment_terms`, `show_remarks`, `show_future_payments`, `in_party_currency`, `for_revaluation_journals`, `ignore_accounts`, `handle_employee_advances`.

The report returns the result of `ReceivablePayableReport.run`. [Worked result and boundaries](dynamic-output.md#invoice-ageing) [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/accounts_payable/accounts_payable.py#L8) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/accounts_payable/accounts_payable.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-006.md#op-d1d0079a6e47b6)

## Accounts Payable Summary

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `report_date`, `ageing_based_on`, `age_as_on`, `range`, `finance_book`, `cost_center`, `project`, `party_type`, `party`, `payment_terms_template`, `supplier_group`, `based_on_payment_terms`, `for_revaluation_journals`, `show_gl_balance`.

The report returns the result of `AccountsReceivableSummary.run`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/accounts_payable_summary/accounts_payable_summary.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/accounts_payable_summary/accounts_payable_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-006.md#op-ecff1d24b01f1f)

## Accounts Receivable

Script Report. The reference record is Sales Invoice. Declared inputs include `company`, `report_date`, `finance_book`, `cost_center`, `project`, `party_type`, `party`, `party_account`, `ageing_based_on`, `age_as_on`, `range`, `customer_group`, `payment_terms_template`, `sales_partner`, `sales_person`, `territory`, `group_by_party`, `based_on_payment_terms`, `show_future_payments`, `show_delivery_notes`, `show_sales_person`, `show_remarks`, `in_party_currency`, `for_revaluation_journals`, `ignore_accounts`.

The report returns the result of `ReceivablePayableReport.run`. [Worked result and boundaries](dynamic-output.md#invoice-ageing) [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/accounts_receivable/accounts_receivable.py#L43) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/accounts_receivable/accounts_receivable.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-006.md#op-c1c27f0dd6fe55)

## Accounts Receivable Summary

Script Report. The reference record is Sales Invoice. Declared inputs include `company`, `report_date`, `ageing_based_on`, `age_as_on`, `range`, `finance_book`, `cost_center`, `project`, `party_type`, `party`, `customer_group`, `payment_terms_template`, `territory`, `sales_partner`, `sales_person`, `based_on_payment_terms`, `show_future_payments`, `show_gl_balance`, `for_revaluation_journals`.

The report returns the result of `AccountsReceivableSummary.run`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/accounts_receivable_summary/accounts_receivable_summary.py#L15) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/accounts_receivable_summary/accounts_receivable_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-008.md#op-fa391d2917c012)

## Asset Depreciation Ledger

Script Report. The reference record is Asset. Declared inputs include `company`, `from_date`, `to_date`, `asset`, `asset_category`, `cost_center`, `finance_book`, `include_default_book_assets`.

The direct return positions are columns / data. Named output fields constructed in this report include `asset`, `asset_name`, `depreciation_date`, `net_purchase_amount`, `opening_accumulated_depreciation`, `depreciation_amount`, `accumulated_depreciation_amount`, `value_after_depreciation`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/asset_depreciation_ledger/asset_depreciation_ledger.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/asset_depreciation_ledger/asset_depreciation_ledger.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-010.md#op-317ee778295fbb)

## Asset Depreciations And Balances

Script Report. The reference record is Asset. Declared inputs include `company`, `from_date`, `to_date`, `group_by`, `asset_category`, `asset`, `finance_book`.

The direct return positions are columns / data. Named output fields constructed in this report include `asset_category`, `asset`, `asset_name`, `value_as_on_from_date`, `value_of_new_purchase`, `value_of_sold_asset`, `value_of_scrapped_asset`, `value_of_capitalized_asset`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/asset_depreciations_and_balances/asset_depreciations_and_balances.py#L19) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/asset_depreciations_and_balances/asset_depreciations_and_balances.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-010.md#op-ecdb5f2de794e0)

## Balance Sheet

Script Report. The reference record is GL Entry. Declared inputs include `company`, `finance_book`, `filter_based_on`, `period_start_date`, `period_end_date`, `from_fiscal_year`, `to_fiscal_year`, `periodicity`, `presentation_currency`, `cost_center`, `project`, `group_by_dimension`, `report_template`, `show_account_details`, `selected_view`, `accumulated_values`, `include_default_book_entries`, `show_zero_values`.

The report returns the result of `FinancialReportEngine.execute`. The direct return positions are columns / data / message / chart / report summary / primitive summary. A separate snapshot procedure is also declared. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/balance_sheet/balance_sheet.py#L33) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/balance_sheet/balance_sheet.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-011.md#op-3b9edf6faddd65)

## Bank Clearance Summary

Script Report. The reference record is Journal Entry. Declared inputs include `from_date`, `to_date`, `account`.

The direct return positions are columns / data. Named output fields constructed in this report include `payment_document_type`, `payment_entry`, `posting_date`, `cheque_no`, `clearance_date`, `against`, `amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/bank_clearance_summary/bank_clearance_summary.py#L15) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/bank_clearance_summary/bank_clearance_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-012.md#op-3564e4b4ed1be5)

## Bank Reconciliation Statement

Script Report. The reference record is Journal Entry. Declared inputs include `company`, `account`, `report_date`, `include_pos_transactions`.

Named output fields constructed in this report include `posting_date`, `payment_document`, `payment_entry`, `debit`, `credit`, `against_account`, `reference_no`, `ref_date`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/bank_reconciliation_statement/bank_reconciliation_statement.py#L16) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/bank_reconciliation_statement/bank_reconciliation_statement.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-013.md#op-26c7b308f99cc3)

## Billed Items To Be Received

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `posting_date`, `purchase_invoice`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `supplier`, `posting_date`, `item_code`, `item_name`, `uom`, `qty`, `received_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/billed_items_to_be_received/billed_items_to_be_received.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/billed_items_to_be_received/billed_items_to_be_received.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-020.md#op-a796a7f03aee9d)

## Budget Variance Report

Script Report. The reference record is Cost Center. Declared inputs include `company`, `from_fiscal_year`, `to_fiscal_year`, `period`, `budget_against`, `budget_against_filter`, `show_cumulative`.

Named output fields constructed in this report include `budget_against`, `account`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/budget_variance_report/budget_variance_report.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/budget_variance_report/budget_variance_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-023.md#op-fd27148720be21)

## Calculated Discount Mismatch

Script Report. The reference record is Sales Invoice.

The direct return positions are columns / data. Named output fields constructed in this report include `doctype`, `docname`, `actual_discount_percentage`, `actual_discount_amount`, `suspected_discount_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/calculated_discount_mismatch/calculated_discount_mismatch.py#L29) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/calculated_discount_mismatch/calculated_discount_mismatch.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-023.md#op-e5f2976882aab7)

## Cash Flow

Script Report. The reference record is GL Entry. Declared inputs include `company`, `finance_book`, `filter_based_on`, `period_start_date`, `period_end_date`, `from_fiscal_year`, `to_fiscal_year`, `periodicity`, `presentation_currency`, `cost_center`, `project`, `group_by_dimension`, `report_template`, `show_account_details`, `include_default_book_entries`, `accumulated_values`, `show_opening_and_closing_balance`.

The report returns the result of `FinancialReportEngine.execute`. The direct return positions are columns / data / absent / chart / report summary. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/cash_flow/cash_flow.py#L36) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/cash_flow/cash_flow.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-024.md#op-3ffd75a7621fe3)

## Cheques And Deposits Incorrectly Cleared

Script Report. The reference record is Payment Entry. Declared inputs include `company`, `account`, `report_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `payment_document`, `payment_entry`, `debit`, `credit`, `posting_date`, `clearance_date`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/cheques_and_deposits_incorrectly_cleared/cheques_and_deposits_incorrectly_cleared.py#L15) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/cheques_and_deposits_incorrectly_cleared/cheques_and_deposits_incorrectly_cleared.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-026.md#op-55dc4c476ed41c)

## Consolidated Accounts Payable

Script Report. The reference record is Purchase Invoice. Declared inputs include `companies`, `report_date`, `party_type`, `party`, `ageing_based_on`, `age_as_on`, `range`, `supplier_group`, `group_by_party`, `group_by_company`, `ignore_accounts`, `based_on_payment_terms`, `show_future_payments`, `show_remarks`, `for_revaluation_journals`, `in_party_currency`.

The report returns the result of `ConsolidatedReceivablePayable.run`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_accounts_payable/consolidated_accounts_payable.py#L9) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_accounts_payable/consolidated_accounts_payable.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-026.md#op-abdcafef5d4567)

## Consolidated Accounts Payable Summary

Script Report. The reference record is Purchase Invoice. Declared inputs include `companies`, `report_date`, `ageing_based_on`, `age_as_on`, `range`, `party_type`, `party`, `supplier_group`, `show_future_payments`, `show_gl_balance`, `based_on_payment_terms`, `for_revaluation_journals`.

The report returns the result of `ConsolidatedReceivablePayableSummary.run`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_accounts_payable_summary/consolidated_accounts_payable_summary.py#L9) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_accounts_payable_summary/consolidated_accounts_payable_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-026.md#op-6fbf434a333cdd)

## Consolidated Accounts Receivable

Script Report. The reference record is Sales Invoice. Declared inputs include `companies`, `report_date`, `party_type`, `party`, `ageing_based_on`, `age_as_on`, `range`, `customer_group`, `territory`, `sales_partner`, `sales_person`, `group_by_party`, `group_by_company`, `ignore_accounts`, `based_on_payment_terms`, `show_future_payments`, `show_remarks`, `show_sales_person`, `show_delivery_notes`, `for_revaluation_journals`, `in_party_currency`.

The report returns the result of `ConsolidatedReceivablePayable.run`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_accounts_receivable/consolidated_accounts_receivable.py#L19) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_accounts_receivable/consolidated_accounts_receivable.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-026.md#op-f32746b81fc47f)

## Consolidated Accounts Receivable Summary

Script Report. The reference record is Sales Invoice. Declared inputs include `companies`, `report_date`, `ageing_based_on`, `age_as_on`, `range`, `party_type`, `party`, `customer_group`, `territory`, `show_future_payments`, `sales_partner`, `sales_person`, `show_gl_balance`, `show_sales_person`, `based_on_payment_terms`, `for_revaluation_journals`.

The report returns the result of `ConsolidatedReceivablePayableSummary.run`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_accounts_receivable_summary/consolidated_accounts_receivable_summary.py#L23) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_accounts_receivable_summary/consolidated_accounts_receivable_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-027.md#op-7ae43ae1f758dd)

## Consolidated Financial Statement

Script Report. The reference record is Account. Declared inputs include `company`, `filter_based_on`, `period_start_date`, `period_end_date`, `from_fiscal_year`, `to_fiscal_year`, `finance_book`, `report`, `presentation_currency`, `accumulated_in_group_company`, `include_default_book_entries`, `show_zero_values`.

The direct return positions are columns / data / message / chart, columns / data / message / chart / report summary. Named output fields constructed in this report include `account`, `currency`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_financial_statement/consolidated_financial_statement.py#L46) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_financial_statement/consolidated_financial_statement.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-027.md#op-c5478cc6716a03)

## Consolidated Trial Balance

Script Report. The reference record is GL Entry. Declared inputs include `company`, `fiscal_year`, `from_date`, `to_date`, `finance_book`, `presentation_currency`, `with_period_closing_entry_for_opening`, `with_period_closing_entry_for_current_period`, `show_zero_values`, `show_unclosed_fy_pl_balances`, `include_default_book_entries`, `show_net_values`, `show_group_accounts`.

The direct return positions are columns / data. Named output fields constructed in this report include `account_name`, `acc_name`, `acc_number`, `currency`, `opening_debit`, `opening_credit`, `debit`, `credit`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_trial_balance/consolidated_trial_balance.py#L35) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_trial_balance/consolidated_trial_balance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-029.md#op-2c7c4b962cb14b)

## Custom Financial Statement

Script Report. The reference record is GL Entry. Declared inputs include `company`, `finance_book`, `filter_based_on`, `period_start_date`, `period_end_date`, `from_fiscal_year`, `to_fiscal_year`, `periodicity`, `presentation_currency`, `cost_center`, `project`, `report_template`, `show_account_details`, `include_default_book_entries`.

The report returns the result of `FinancialReportEngine.execute`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/custom_financial_statement/custom_financial_statement.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/custom_financial_statement/custom_financial_statement.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-031.md#op-b3c30cbf16b389)

## Customer Ledger Summary

Script Report. The reference record is Sales Invoice. Declared inputs include `company`, `from_date`, `to_date`, `finance_book`, `party`, `customer_group`, `payment_terms_template`, `territory`, `sales_partner`, `sales_person`, `tax_id`, `customer_name`, `cost_center`, `project`, `ignore_cr_dr_notes`.

The report returns the result of `PartyLedgerSummaryReport.run`. Named output fields constructed in this report include `party`, `party_name`, `customer_group`, `territory`, `supplier_group`, `opening_balance`, `invoiced_amount`, `paid_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/customer_ledger_summary/customer_ledger_summary.py#L521) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/customer_ledger_summary/customer_ledger_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-032.md#op-5344d0eefcaedb)

## Day Book

Script Report. The reference record is GL Entry. Declared inputs include `company`, `from_date`, `to_date`, `voucher_type`, `detailed`, `show_remarks`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `posting_date`, `particulars`, `voucher_type`, `voucher_no`, `debit`, `credit`, `remarks`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/day_book/day_book.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/day_book/day_book.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-032.md#op-6eabba658b7323)

## Deferred Revenue And Expense

Script Report. The reference record is GL Entry. Declared inputs include `company`, `filter_based_on`, `period_start_date`, `period_end_date`, `from_fiscal_year`, `to_fiscal_year`, `periodicity`, `type`, `with_upcoming_postings`.

The direct return positions are columns / data / message / chart. Named output fields constructed in this report include `name`, `service_start_date`, `service_end_date`, `amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/deferred_revenue_and_expense/deferred_revenue_and_expense.py#L499) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/deferred_revenue_and_expense/deferred_revenue_and_expense.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-034.md#op-c0950d9574eb27)

## Delivered Items To Be Billed

Script Report. The reference record is Sales Invoice. Declared inputs include `company`, `posting_date`, `delivery_note`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `date`, `customer`, `customer_name`, `item_code`, `amount`, `billed_amount`, `returned_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/delivered_items_to_be_billed/delivered_items_to_be_billed.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/delivered_items_to_be_billed/delivered_items_to_be_billed.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-034.md#op-c50f00bc3484ac)

## Dimension Wise Accounts Balance Report

Script Report. The reference record is GL Entry. Declared inputs include `company`, `fiscal_year`, `from_date`, `to_date`, `finance_book`, `dimension`.

Named output fields constructed in this report include `account`, `currency`, `total`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/dimension_wise_accounts_balance_report/dimension_wise_accounts_balance_report.py#L18) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/dimension_wise_accounts_balance_report/dimension_wise_accounts_balance_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-034.md#op-6ea8373cbe3c26)

## Financial Ratios

Script Report. The reference record is Account. Declared inputs include `company`, `from_fiscal_year`, `to_fiscal_year`, `periodicity`, `period_start_date`, `period_end_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `ratio`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/financial_ratios/financial_ratios.py#L91) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/financial_ratios/financial_ratios.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-037.md#op-feed6a5f2f2136)

## General And Payment Ledger Comparison

Script Report. The reference record is GL Entry. Declared inputs include `company`, `period_start_date`, `period_end_date`, `account`, `party_type`, `party`, `voucher_no`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/general_and_payment_ledger_comparison/general_and_payment_ledger_comparison.py#L419) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/general_and_payment_ledger_comparison/general_and_payment_ledger_comparison.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-047.md#op-ab9df1d204f9d6)

## General Ledger

Script Report. The reference record is GL Entry. Declared inputs include `company`, `finance_book`, `from_date`, `to_date`, `account`, `voucher_no`, `against_voucher_no`, `party_type`, `party`, `party_name`, `categorize_by`, `tax_id`, `presentation_currency`, `cost_center`, `project`, `include_dimensions`, `disable_opening_balance_calculation`, `show_opening_entries`, `include_default_book_entries`, `show_cancelled_entries`, `show_net_values_in_party_account`, `show_amount_in_company_currency`, `convert_at_reporting_date_rate`, `add_values_in_transaction_currency`, `show_remarks`, `ignore_err`, `ignore_cr_dr_notes`.

Named output fields constructed in this report include `gl_entry`, `posting_date`, `account`, `debit`, `credit`, `balance`, `debit_in_transaction_currency`, `credit_in_transaction_currency`. The structured entry gives their enclosing conditions and builders. A separate snapshot procedure is also declared. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/general_ledger/general_ledger.py#L34) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/general_ledger/general_ledger.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-047.md#op-d8c401fad4e326)

## Gross And Net Profit Report

Script Report. The reference record is GL Entry. Declared inputs include `company`, `finance_book`, `filter_based_on`, `period_start_date`, `period_end_date`, `from_fiscal_year`, `to_fiscal_year`, `periodicity`, `presentation_currency`, `cost_center`, `project`, `accumulated_values`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/gross_and_net_profit_report/gross_and_net_profit_report.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/gross_and_net_profit_report/gross_and_net_profit_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-050.md#op-73b6730dea2407)

## Gross Profit

Script Report. The reference record is Sales Invoice. Declared inputs include `company`, `from_date`, `to_date`, `sales_invoice`, `group_by`, `item_group`, `sales_person`, `warehouse`, `cost_center`, `project`, `include_returned_invoices`.

The direct return positions are columns / data. Named output fields constructed in this report include `parent_invoice`, `posting_date`, `posting_time`, `item_code`, `item_name`, `item_group`, `description`, `warehouse`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/gross_profit/gross_profit.py#L24) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/gross_profit/gross_profit.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-051.md#op-9a5dfd4ab61707)

## Inactive Sales Items

Script Report. The reference record is Sales Invoice. Declared inputs include `territory`, `item`, `item_group`, `based_on`, `days`.

The direct return positions are columns / data. Named output fields constructed in this report include `territory`, `item_group`, `item`, `item_name`, `customer`, `last_order_date`, `qty`, `days_since_last_order`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/inactive_sales_items/inactive_sales_items.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/inactive_sales_items/inactive_sales_items.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-052.md#op-82967992f061a4)

## Invalid Ledger Entries

Script Report. The reference record is GL Entry. Declared inputs include `company`, `from_date`, `to_date`, `account`, `voucher_no`.

The direct return positions are columns / data. Named output fields constructed in this report include `voucher_type`, `voucher_no`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/invalid_ledger_entries/invalid_ledger_entries.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/invalid_ledger_entries/invalid_ledger_entries.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-053.md#op-d68b5e5d23305a)

## Item Wise Purchase Register

Script Report. The reference record is Purchase Invoice. Declared inputs include `from_date`, `to_date`, `item_code`, `item_group`, `supplier`, `company`, `mode_of_payment`, `group_by`.

The report returns the result of `_execute`. Named output fields constructed in this report include `item_code`, `item_name`, `item_group`, `description`, `invoice`, `posting_date`, `supplier`, `supplier_name`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/item_wise_purchase_register/item_wise_purchase_register.py#L20) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/item_wise_purchase_register/item_wise_purchase_register.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-054.md#op-f32881998682a2)

## Item Wise Sales Register

Script Report. The reference record is Sales Invoice. Declared inputs include `from_date`, `to_date`, `customer`, `company`, `mode_of_payment`, `warehouse`, `brand`, `item_code`, `item_group`, `group_by`, `income_account`.

The report returns the result of `_execute`. Named output fields constructed in this report include `item_code`, `item_name`, `item_group`, `description`, `invoice`, `posting_date`, `customer_group`, `customer`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/item_wise_sales_register/item_wise_sales_register.py#L23) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/item_wise_sales_register/item_wise_sales_register.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-054.md#op-cb8c82bf396727)

## Payment Ledger

Script Report. The reference record is Payment Ledger Entry. Declared inputs include `company`, `period_start_date`, `period_end_date`, `account`, `party_type`, `party`, `voucher_no`, `against_voucher_no`, `include_account_currency`, `group_party`.

The report returns the result of `PaymentLedger.run`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/payment_ledger/payment_ledger.py#L276) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/payment_ledger/payment_ledger.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-069.md#op-8a7e1fb62f49f8)

## Payment Period Based On Invoice Date

Script Report. The reference record is Journal Entry. Declared inputs include `company`, `from_date`, `to_date`, `payment_type`, `party_type`, `party`.

The direct return positions are columns / data. Named output fields constructed in this report include `payment_document`, `payment_entry`, `party_type`, `party`, `posting_date`, `invoice`, `invoice_posting_date`, `due_date`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/payment_period_based_on_invoice_date/payment_period_based_on_invoice_date.py#L18) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/payment_period_based_on_invoice_date/payment_period_based_on_invoice_date.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-070.md#op-8ddbac327faa39)

## Point Of Sale Register

Script Report. The reference record is POS Invoice. Declared inputs include `company`, `from_date`, `to_date`, `pos_profile`, `owner`, `customer`, `mode_of_payment`, `group_by`, `is_return`.

Named output fields constructed in this report include `posting_date`, `invoice_type`, `pos_invoice`, `customer`, `pos_profile`, `owner`, `grand_total`, `paid_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/pos_register/pos_register.py#L16) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/pos_register/pos_register.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-083.md#op-68b31077d76af2)

## Profit And Loss Statement

Script Report. The reference record is GL Entry. Declared inputs include `company`, `finance_book`, `filter_based_on`, `period_start_date`, `period_end_date`, `from_fiscal_year`, `to_fiscal_year`, `periodicity`, `presentation_currency`, `cost_center`, `project`, `group_by_dimension`, `report_template`, `show_account_details`, `selected_view`, `accumulated_values`, `include_default_book_entries`, `show_zero_values`.

The report returns the result of `FinancialReportEngine.execute`. The direct return positions are columns / data / absent / chart / report summary / primitive summary. A separate snapshot procedure is also declared. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/profit_and_loss_statement/profit_and_loss_statement.py#L33) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/profit_and_loss_statement/profit_and_loss_statement.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-090.md#op-d51d7073c29f61)

## Profitability Analysis

Script Report. The reference record is GL Entry. Declared inputs include `company`, `based_on`, `accounting_dimension`, `fiscal_year`, `from_date`, `to_date`, `finance_book`, `include_default_book_entries`, `show_zero_values`.

The direct return positions are columns / data. Named output fields constructed in this report include `account`, `currency`, `income`, `expense`, `gross_profit_loss`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/profitability_analysis/profitability_analysis.py#L23) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/profitability_analysis/profitability_analysis.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-091.md#op-e92bfa3c412830)

## Purchase Invoice Trends

Script Report. The reference record is Purchase Invoice. Declared inputs include `period_based_on`.

The linked row procedure owns the output; inspect its conditional returns and result builders for the selected filters. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/purchase_invoice_trends/purchase_invoice_trends.py#L8) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/purchase_invoice_trends/purchase_invoice_trends.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-095.md#op-696587f75f448f)

## Purchase Register

Script Report. The reference record is Purchase Invoice. Declared inputs include `from_date`, `to_date`, `supplier`, `supplier_group`, `company`, `mode_of_payment`, `cost_center`, `warehouse`, `item_group`, `include_payments`.

The report returns the result of `_execute`. Named output fields constructed in this report include `voucher_type`, `voucher_no`, `posting_date`, `supplier_id`, `supplier_name`, `supplier_group`, `tax_id`, `payable_account`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/purchase_register/purchase_register.py#L28) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/purchase_register/purchase_register.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-095.md#op-714d45bae1901c)

## Received Items To Be Billed

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `posting_date`, `purchase_receipt`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `date`, `supplier`, `supplier_name`, `item_code`, `amount`, `billed_amount`, `returned_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/received_items_to_be_billed/received_items_to_be_billed.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/received_items_to_be_billed/received_items_to_be_billed.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-096.md#op-2a66d0260fd751)

## Sales Invoice Trends

Script Report. The reference record is Sales Invoice. Declared inputs include `company`, `period`, `based_on`, `group_by`, `fiscal_year`, `item_code`.

The linked row procedure owns the output; inspect its conditional returns and result builders for the selected filters. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/sales_invoice_trends/sales_invoice_trends.py#L8) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/sales_invoice_trends/sales_invoice_trends.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-105.md#op-042a66c554c806)

## Sales Partners Commission

Script Report. The reference record is Sales Invoice. Declared inputs include `company`, `from_date`, `to_date`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `sales_partner`, `invoiced_amount`, `amount_eligible_for_commission`, `total_commission`, `average_commission_rate`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/sales_partners_commission/sales_partners_commission.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/sales_partners_commission/sales_partners_commission.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-105.md#op-a6c5e563edaea0)

## Sales Payment Summary

Script Report. The reference record is Sales Invoice. Declared inputs include `from_date`, `to_date`, `company`, `owner`, `is_pos`, `payment_detail`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/sales_payment_summary/sales_payment_summary.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/sales_payment_summary/sales_payment_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-105.md#op-8ca1072140fbf6)

## Sales Register

Script Report. The reference record is Sales Invoice. Declared inputs include `from_date`, `to_date`, `customer`, `customer_group`, `company`, `mode_of_payment`, `owner`, `cost_center`, `warehouse`, `brand`, `item_group`, `include_payments`.

The report returns the result of `_execute`. Named output fields constructed in this report include `voucher_type`, `voucher_no`, `posting_date`, `customer`, `customer_name`, `customer_group`, `territory`, `tax_id`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/sales_register/sales_register.py#L28) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/sales_register/sales_register.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-106.md#op-ec5aca5a83ba62)

## Share Balance

Script Report. The reference record is Share Transfer. Declared inputs include `date`, `shareholder`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/share_balance/share_balance.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/share_balance/share_balance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-107.md#op-80e6aeb96622ce)

## Share Ledger

Script Report. The reference record is Share Transfer. Declared inputs include `date`, `shareholder`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/share_ledger/share_ledger.py#L9) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/share_ledger/share_ledger.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-107.md#op-6174b67a1b7560)

## Supplier Ledger Summary

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `from_date`, `to_date`, `finance_book`, `party`, `supplier_group`, `payment_terms_template`, `tax_id`, `supplier_name`, `cost_center`, `project`.

The report returns the result of `PartyLedgerSummaryReport.run`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/supplier_ledger_summary/supplier_ledger_summary.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/supplier_ledger_summary/supplier_ledger_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-111.md#op-f43ff1e65040c4)

## Tax Deducted At Source Computation Summary

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `party_type`, `party`, `from_date`, `to_date`.

The module binds its entry to the class method `TDSComputationSummaryReport.execute`. It invokes the report class with the selected filters so its own validations, columns and row selection apply. Named output fields constructed in this report include `tax_id`, `party`, `party_name`, `tax_withholding_category`, `party_entity_type`, `rate`, `total_amount`, `tax_amount`. The structured entry gives their enclosing conditions and builders. [Worked result and boundaries](dynamic-output.md#tax-withholding) [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/tds_computation_summary/tds_computation_summary.py#L95) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/tds_computation_summary/tds_computation_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-112.md#op-333d66570971d1)

## Tax Withholding Details

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `party_type`, `party`, `from_date`, `to_date`.

The module binds its entry to the class method `TaxWithholdingDetailsReport.execute`. It invokes the report class with the selected filters so its own validations, columns and row selection apply. Named output fields constructed in this report include `tax_withholding_category`, `tax_id`, `party_name`, `party`, `party_entity_type`, `supplier_invoice_no`, `supplier_invoice_date`, `rate`. The structured entry gives their enclosing conditions and builders. [Worked result and boundaries](dynamic-output.md#tax-withholding) [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/tax_withholding_details/tax_withholding_details.py#L307) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/tax_withholding_details/tax_withholding_details.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-112.md#op-333d66570971d1)

## Trial Balance

Script Report. The reference record is GL Entry. Declared inputs include `company`, `fiscal_year`, `from_date`, `to_date`, `cost_center`, `project`, `finance_book`, `presentation_currency`, `with_period_closing_entry_for_opening`, `with_period_closing_entry_for_current_period`, `show_zero_values`, `show_unclosed_fy_pl_balances`, `include_default_book_entries`, `show_net_values`, `show_group_accounts`.

The direct return positions are columns / data. Named output fields constructed in this report include `account`, `acc_name`, `acc_number`, `currency`, `opening_debit`, `opening_credit`, `debit`, `credit`. The structured entry gives their enclosing conditions and builders. A separate snapshot procedure is also declared. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/trial_balance/trial_balance.py#L43) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/trial_balance/trial_balance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-116.md#op-24a86282a9f90b)

## Trial Balance For Party

Script Report. The reference record is GL Entry. Declared inputs include `company`, `fiscal_year`, `from_date`, `to_date`, `party_type`, `party`, `account`, `finance_book`, `include_default_book_entries`, `show_zero_values`, `exclude_zero_balance_parties`.

The direct return positions are columns / data. Named output fields constructed in this report include `party`, `opening_debit`, `opening_credit`, `debit`, `credit`, `closing_debit`, `closing_credit`, `currency`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/trial_balance_for_party/trial_balance_for_party.py#L16) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/trial_balance_for_party/trial_balance_for_party.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-117.md#op-f2303b86270402)

## Trial Balance Simple

Query Report. The reference record is GL Entry. Declared inputs include `company`.

See the [row-selection rule and worked example](query-rules.md#trial-balance-simple). [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/trial_balance_simple/trial_balance_simple.json)

## Voucher Wise Balance

Script Report. The reference record is GL Entry. Declared inputs include `company`, `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `voucher_type`, `voucher_no`, `debit`, `credit`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/voucher_wise_balance/voucher_wise_balance.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/voucher_wise_balance/voucher_wise_balance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-123.md#op-e1c7a9925cd3c1)
