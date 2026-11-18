# Salary accrual, employer contributions and disbursement

The [Salary accrual, employer contributions and disbursement](../../people-and-services/payroll-posting.md) chapter defines the business rules, calculations and worked outcomes.

The employer contribution builder produces a separate submitted journal. The example qualifies the journal sides and arithmetic under its supplied rates. Payroll rules in the employee's jurisdiction determine the applicable rates.

## Build and post

- [Assignment lookup](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/doctype/salary_slip/salary_slip.py#L879-L900)
- [Accrual build](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/doctype/payroll_entry/payroll_entry.py#L442-L662)
- [Employer contribution entries](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/doctype/payroll_entry/payroll_entry.py#L664-L777)
- [Accrual versus bank submission](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/doctype/payroll_entry/payroll_entry.py#L778-L823)
- [Disbursement selection and entries](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/doctype/payroll_entry/payroll_entry.py#L1054-L1250)

## Failure and reversal

- [Submission worker](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/doctype/payroll_entry/payroll_entry.py#L1798-L1845)
- [Cancellation](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/doctype/payroll_entry/payroll_entry.py#L129-L208)
