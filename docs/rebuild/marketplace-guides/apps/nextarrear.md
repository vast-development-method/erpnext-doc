# NextArrear

[Business workflow and acceptance cases](../../../capabilities/guides/people.md#retroactive-payroll-adjustments).

Apoorv Soral's version 14 listing describes a **Salary Arrear** record. A payroll operator supplies the required information, the app retrieves salary slips with their earnings and deductions, and saving calculates the net arrear. The publisher describes review, adjustment and final approval, plus reports showing the component breakdown. The listing supplies neither the exact eligibility fields nor the proration, tax, negative-arrear or accounting policy. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/nextarrear)

## Proposed rebuild contract

Core HRMS publishes currency, dates, component tables, total deductions and net pay on its Salary Slip. This provides a reference integration model. Access to the app's own component-selection and payment rules is still needed for behavioural equivalence. [Core Salary Slip definition](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/doctype/salary_slip/salary_slip.json) · [Named app repository](https://github.com/asoral/nextarrear)

[Read the consolidated workflow](../../../capabilities/guides/people.md#retroactive-payroll-adjustments-1).
