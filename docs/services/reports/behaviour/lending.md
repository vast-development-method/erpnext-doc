# Lending reports

The [structured report details](lending.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## ALM Audit Report

Script Report. The reference record is Loan. Declared inputs include `company`, `as_on_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `loan`, `loan_product`, `ageing`, `accrued_principal`, `accrued_interest`, `penalty_amount`, `total`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/alm_audit_report/alm_audit_report.py#L10) [Declaration](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/alm_audit_report/alm_audit_report.json) [Module bindings](procedures/lending--alm-audit-report-bindings.json) · [Ordered report procedures](procedures/lending--alm-audit-report-1.json)

## Applicant-Wise Loan Security Exposure

Script Report. The reference record is Loan Security. Declared inputs include `company`.

The direct return positions are columns / data. Named output fields constructed in this report include `applicant_type`, `applicant_name`, `loan_security`, `loan_security_code`, `loan_security_name`, `haircut`, `loan_security_type`, `disabled`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/applicant_wise_loan_security_exposure/applicant_wise_loan_security_exposure.py#L13) [Declaration](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/applicant_wise_loan_security_exposure/applicant_wise_loan_security_exposure.json) [Module bindings](procedures/lending--applicant-wise-loan-security-exposure-bindings.json) · [Ordered report procedures](procedures/lending--applicant-wise-loan-security-exposure-1.json)

## Disbursement Analysis Report

Script Report. The reference record is Loan Disbursement. Declared inputs include `company`, `applicant_type`, `applicant`, `loan_product`, `loan`, `loan_disbursement`.

The direct return positions are columns / data. Named output fields constructed in this report include `loan_account`, `loan_disbursement_id`, `applicant`, `applicant_type`, `tranche_number`, `interest_rate`, `maturity_date`, `disbursement_date`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/disbursement_analysis_report/disbursement_analysis_report.py#L10) [Declaration](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/disbursement_analysis_report/disbursement_analysis_report.json) [Module bindings](procedures/lending--disbursement-analysis-report-bindings.json) · [Ordered report procedures](procedures/lending--disbursement-analysis-report-1.json)

## Future Cashflow Report

Script Report. The reference record is Loan. Declared inputs include `company`, `as_on_date`, `loan_product`, `loan`, `loan_disbursement`.

The direct return positions are columns / data. Named output fields constructed in this report include `loan`, `loan_disbursement`, `loan_product`, `payment_date`, `principal_amount`, `interest_amount`, `total_payment`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/future_cashflow_report/future_cashflow_report.py#L8) [Declaration](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/future_cashflow_report/future_cashflow_report.json) [Module bindings](procedures/lending--future-cashflow-report-bindings.json) · [Ordered report procedures](procedures/lending--future-cashflow-report-1.json)

## Loan Outstanding Report

Script Report. The reference record is Loan. Declared inputs include `company`, `as_on_date`, `applicant_type`, `applicant`, `loan_product`, `loan`, `loan_disbursement`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `loan`, `applicant`, `posting_date`, `loan_amount`, `loan_disbursement`, `disbursement_date`, `disbursed_amount`, `loan_product`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/loan_outstanding_report/loan_outstanding_report.py#L12) [Declaration](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/loan_outstanding_report/loan_outstanding_report.json) [Module bindings](procedures/lending--loan-outstanding-report-bindings.json) · [Ordered report procedures](procedures/lending--loan-outstanding-report-1.json)

## Loan Repayment and Closure

Script Report. The reference record is Loan Repayment. Declared inputs include `company`, `loan_product`, `from_date`, `to_date`, `loan`, `applicant_type`, `applicant`.

The direct return positions are columns / data. Named output fields constructed in this report include `posting_date`, `value_date`, `loan_repayment`, `against_loan`, `applicant`, `repayment_type`, `overdue_amount`, `principal_amount_paid`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/loan_repayment_and_closure/loan_repayment_and_closure.py#L9) [Declaration](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/loan_repayment_and_closure/loan_repayment_and_closure.json) [Module bindings](procedures/lending--loan-repayment-and-closure-bindings.json) · [Ordered report procedures](procedures/lending--loan-repayment-and-closure-1.json)

## Loan Security Exposure

Script Report. The reference record is Loan Security. Declared inputs include `company`.

The direct return positions are columns / data. Named output fields constructed in this report include `loan_security`, `loan_security_code`, `loan_security_name`, `haircut`, `loan_security_type`, `disabled`, `total_qty`, `latest_price`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/loan_security_exposure/loan_security_exposure.py#L16) [Declaration](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/loan_security_exposure/loan_security_exposure.json) [Module bindings](procedures/lending--loan-security-exposure-bindings.json) · [Ordered report procedures](procedures/lending--loan-security-exposure-1.json)

## Loan Security Ledger

Script Report. The reference record is Loan Security. Declared inputs include `loan`, `applicant`, `loan_security`.

The direct return positions are columns / data. Named output fields constructed in this report include `date`, `doctype`, `loan_security`, `loan_security_type`, `loan`, `qty`, `balance_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/loan_security_ledger/loan_security_ledger.py#L10) [Declaration](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/loan_security_ledger/loan_security_ledger.json) [Module bindings](procedures/lending--loan-security-ledger-bindings.json) · [Ordered report procedures](procedures/lending--loan-security-ledger-1.json)

## Loan Security Status

Script Report. The reference record is Loan Security. Declared inputs include `company`, `applicant_type`, `applicant`, `pledge_status`.

The direct return positions are columns / data. Named output fields constructed in this report include `loan_security_assignment`, `loan`, `applicant`, `status`, `pledge_time`, `loan_security`, `qty`, `loan_security_price`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/loan_security_status/loan_security_status.py#L9) [Declaration](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/loan_security_status/loan_security_status.json) [Module bindings](procedures/lending--loan-security-status-bindings.json) · [Ordered report procedures](procedures/lending--loan-security-status-1.json)

## Loan Statement of Account

Script Report. The reference record is Loan. Declared inputs include `company`, `applicant_type`, `applicant`, `loan`, `loan_product`, `from_date`, `to_date`, `group_by`.

The direct return positions are columns / data. Named output fields constructed in this report include `posting_date`, `transaction_type`, `transaction_name`, `loan`, `debit`, `credit`, `balance`, `remarks`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/loan_statement_of_account/loan_statement_of_account.py#L9) [Declaration](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/loan_statement_of_account/loan_statement_of_account.json) [Module bindings](procedures/lending--loan-statement-of-account-bindings.json) · [Ordered report procedures](procedures/lending--loan-statement-of-account-1.json)

## Past Cashflow Report

Script Report. The reference record is Loan. Declared inputs include `company`, `as_on_date`, `applicant_type`, `applicant`, `loan_product`, `loan`.

The direct return positions are columns / data. Named output fields constructed in this report include `loan`, `applicant`, `loan_product`, `principal_amount`, `interest_amount`, `additional_interest`, `total_charges_paid`, `total_penalty_paid`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/past_cashflow_report/past_cashflow_report.py#L6) [Declaration](https://github.com/frappe/lending/blob/06fd61f48fa745e4bf75ee8909d0f9f617059099/lending/loan_management/report/past_cashflow_report/past_cashflow_report.json) [Module bindings](procedures/lending--past-cashflow-report-bindings.json) · [Ordered report procedures](procedures/lending--past-cashflow-report-1.json)
