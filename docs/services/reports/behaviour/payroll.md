# Payroll reports

The [structured report details](payroll.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Accrued Earnings Report

Script Report. The reference record is Employee Benefit Ledger. Declared inputs include `company`, `employee`, `department`, `branch`, `payroll_period`, `salary_component`, `flexible_benefit`.

The direct return positions are columns / data. Named output fields constructed in this report include `employee`, `employee_name`, `salary_component`, `yearly_benefit`, `total_accrued`, `total_payout`, `unpaid_accrual`, `flexible_benefit`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/accrued_earnings_report/accrued_earnings_report.py#L10) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/accrued_earnings_report/accrued_earnings_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/payroll/operations-001.md#op-8798c2a643b8b3)

## Bank Remittance

Script Report. The reference record is Payroll Entry. Declared inputs include `company`, `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `payroll_no`, `debit_account`, `payment_date`, `employee_name`, `bank_name`, `employee_account_no`, `bank_code`, `currency`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/bank_remittance/bank_remittance.py#L9) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/bank_remittance/bank_remittance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/payroll/operations-002.md#op-1429d32d158244)

## Employee Cost To Company Break Up

Script Report. The reference record is Salary Slip. Declared inputs include `company`, `employee`, `salary_structure_assignment`.

The direct return positions are columns / data / message / absent / absent. Named output fields constructed in this report include `salary_component`, `type`, `formula`, `per_cycle`, `annual`, `percent_of_ctc`, `currency`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/employee_ctc_break_up/employee_ctc_break_up.py#L324) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/employee_ctc_break_up/employee_ctc_break_up.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/payroll/operations-004.md#op-e60e1dec22f83e)

## Income Tax Computation

Script Report. The reference record is Salary Slip. Declared inputs include `company`, `payroll_period`, `employee`, `department`, `employee_status`, `consider_tax_exemption_declaration`.

The report returns the result of `IncomeTaxComputationReport.run`. Named output fields constructed in this report include `employee`, `employee_name`, `department`, `designation`, `date_of_joining`, `income_tax_slab`, `gross_earnings`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/income_tax_computation/income_tax_computation.py#L13) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/income_tax_computation/income_tax_computation.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/payroll/operations-006.md#op-06551755e9b5f7)

## Income Tax Deductions

Script Report. The reference record is Salary Slip. Declared inputs include `company`, `month`, `year`, `department`, `branch`.

The direct return positions are columns / data. Named output fields constructed in this report include `employee`, `employee_name`, `pan_number`, `it_comp`, `it_amount`, `gross_pay`, `posting_date`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/income_tax_deductions/income_tax_deductions.py#L14) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/income_tax_deductions/income_tax_deductions.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/payroll/operations-007.md#op-1ca520cdbdf65d)

## Salary Payments Based On Payment Mode

Script Report. The reference record is Salary Slip. Declared inputs include `company`, `month`, `year`, `department`, `branch`.

Named output fields constructed in this report include `branch`, `total`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/salary_payments_based_on_payment_mode/salary_payments_based_on_payment_mode.py#L14) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/salary_payments_based_on_payment_mode/salary_payments_based_on_payment_mode.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/payroll/operations-012.md#op-ceee1bf00fe978)

## Salary Payments Through A Bank Settlement Channel

Script Report. The reference record is Salary Slip. Declared inputs include `company`, `month`, `year`, `department`, `branch`, `type`.

The direct return positions are columns / data. Named output fields constructed in this report include `branch`, `employee_name`, `employee`, `gross_pay`, `net_pay`, `bank`, `account_no`, `ifsc`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/salary_payments_via_ecs/salary_payments_via_ecs.py#L13) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/salary_payments_via_ecs/salary_payments_via_ecs.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/payroll/operations-012.md#op-1ae79536e3b5ed)

## Salary Register

Script Report. The reference record is Salary Slip. Declared inputs include `from_date`, `to_date`, `currency`, `employee`, `company`, `docstatus`, `department`, `designation`, `branch`, `show_employer_contributions`.

Named output fields constructed in this report include `salary_slip_id`, `employee`, `employee_name`, `data_of_joining`, `branch`, `department`, `designation`, `company`. The structured entry gives their enclosing conditions and builders. [Worked result and boundaries](dynamic-output.md#salary-register) [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/salary_register/salary_register.py#L17) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/report/salary_register/salary_register.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/payroll/operations-012.md#op-99d6cea1cd3fbd)
