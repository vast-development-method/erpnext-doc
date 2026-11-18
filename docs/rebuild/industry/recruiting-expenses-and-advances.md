# Recruiting commitments and employee money

The [Recruiting commitments and employee money](../../people-and-services/employee-recovery.md) chapter defines the business rules, calculations and worked outcomes.

## From referral to a pay event

- [Referral and applicant mapping](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/doctype/employee_referral/employee_referral.py)
- [Vacancies and employee mapping](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/doctype/job_offer/job_offer.py#L128-L220)
- [Cost and offer preview](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/doctype/job_offer/job_offer.py#L219-L393)
- [Bonus mapping](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/doctype/employee_referral/employee_referral.py#L82-L94)
- [Bonus gates and status](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/doctype/additional_salary/additional_salary.py#L134-L157)

## Request, fund, claim, settle, reverse

- [Advance validation, sign and status](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/doctype/employee_advance/employee_advance.py#L78-L252)
- [Claim lifecycle and journal](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/doctype/expense_claim/expense_claim.py#L55-L391)
- [Allocation and tax gates](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/doctype/expense_claim/expense_claim.py#L493-L615)
- [Exchange adjustment](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/doctype/expense_claim/expense_claim.py#L412-L467)
- [Existing expense and settlement contract](../../domains/employee-expenses-and-advances.md)
