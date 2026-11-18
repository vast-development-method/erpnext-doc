# NextArrear

Apoorv Soral's version 14 listing describes a **Salary Arrear** record. A payroll operator supplies the required information, the app retrieves salary slips with their earnings and deductions, and saving calculates the net arrear. The publisher describes review, adjustment and final approval, plus reports showing the component breakdown. The listing supplies neither the exact eligibility fields nor the proration, tax, negative-arrear or accounting policy. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/nextarrear)

## Proposed rebuild contract

Open a calculation for an employee, company, covered periods and effective pay revision. Retrieve authorized finalized slips and component amounts for those periods. Retain each slip and line reference, original amount, recomputed entitlement, payroll currency and rounding policy. For components that affect net pay, calculate the change in earnings minus the change in deductions. Group by employee, period and currency before summation. A review adjustment must identify its author, rationale and component. Bind approval to the exact basis revision. A later correction to a source slip invalidates an unapproved calculation and requires a new review.

Paying the arrear or creating a journal entry requires a separate, authorized settlement operation with its own reference. Use stable component IDs across salary structures and reporting periods. Distinguish the employee's statement language from the payroll officer's language. Translate component descriptions, period names and review reasons for display. Preserve the authorized code, decimals and sign on exports. An unknown translated label falls back to the recorded component description alongside its code.

| Proposed acceptance case | Expected result |
|---|---|
| A finalized monthly slip recorded earnings of 2,000 and deductions of 250. Corrected amounts are 2,150 and 280 in the same currency. | Earnings difference is +150, deduction difference is +30 and net arrear is +120. Changing the statement language reproduces the same slip references, component codes and totals. |
| A second slip has earnings unchanged and deductions reduced from 100 to 90. | The adjustment for that slip is +10. Combined with the first example in the same currency, the total is +130, with both calculations visible. |
| One requested slip is cancelled after calculation but before approval. | The stale result cannot be approved. The reviewer sees the affected period and a localized explanation, and no settlement is created. |
| Two reviewers open the same calculation. One changes a component after the other's preview. | The earlier preview cannot approve a different revision. The retained audit trail identifies the adjustment. |

Core HRMS publishes currency, dates, component tables, total deductions and net pay on its Salary Slip. This provides a reference integration model. Access to the app's own component-selection and payment rules is still needed for behavioural equivalence. [Core Salary Slip definition](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/payroll/doctype/salary_slip/salary_slip.json) · [Named app repository](https://github.com/asoral/nextarrear)
