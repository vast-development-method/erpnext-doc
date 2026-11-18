# Labor Management System

## Publisher evidence

Micro Solution lists version 14. The product handles temporary workers from registration and placement through attendance, deductions, payslips and payment. Staff enter or import worker identity and mobile details and define project, profit/cost assignment, work breakdown, subcontractor, attendance machine, shift and worker organization. Placement assigns the worker to a project, shift and cost center. Imported attendance logs produce attendance and overtime. Staff enter payment adjustments, generate a payslip and pay it. The linked vendor guide did not yield readable documentation during this review. [Marketplace workflow](https://cloud.frappe.io/marketplace/apps/laborers_management) · [Linked guide](https://www.micro-sl.com/labor-management-system) · [Listed repository](https://github.com/micro-sl/laborers_management)

## What the publisher's screens show

The workspace gives separate entries to machine logs, attendance allowances, timesheet assignments and bulk adjustments. It presents the payslip, payslip payment and payroll batch as separate operations. The role screen distinguishes master-data, operations and viewer roles. This identifies role labels, without establishing their individual permission grants. [Workspace](https://cloud.frappe.io/files/l1.webp) · [Role assignments](https://cloud.frappe.io/files/l4.webp)

In the workflow drawing, a placement leads to an attendance log, then attendance. Attendance feeds overtime; attendance, overtime and payment adjustments feed the payslip, which in turn leads to its payment. The report screenshot breaks payslips down by project, profit center and payment type. The sample shows project P101 with 120 in timesheet earnings and 80 for overtime; a separate adjustment row shows 100 with no project displayed. The example supplies neither a currency nor a pay-rate formula. [Workflow diagram](https://cloud.frappe.io/files/Screenshot%20from%202023-09-21%2009-20-01.webp) · [Payslip-by-type report](https://cloud.frappe.io/files/Screenshot%20from%202023-09-21%2009-20-57.webp)

## Proposed rebuild contract

| Stage | Inputs and accounting boundary |
|---|---|
| Identity and placement | Give each person a worker ID distinct from their name and each machine its own identity. Bind the device's worker key to that worker for a validity period. Record effective dates on placement and preserve the project, shift and cost center used for each work interval. |
| Attendance review | Deduplicate imports by machine and event ID. Pair punches within a placement and shift. Keep missing punches, ambiguous local times and conflicting placements in a review queue. The supervisor approves the interval and any overtime under the effective pay policy. |
| Payroll | Calculate approved regular units × regular rate, plus approved overtime units × applicable rate and signed adjustments. Preserve each line's currency, rate, units, basis, project and cost center. Freeze the inputs and pay policy on an approved statement. |
| Settlement | Record the payee, payment reference and amount allocated to the statement. A duplicate confirmation must not create a second disbursement. Corrections after approval create auditable adjustments and a revised or supplementary statement under the site's policy. |

## Multilingual operation and acceptance

Take a single placement with eight approved regular hours at 30 per hour, two approved overtime hours at 45, and a deduction of 20 in the same configured currency. The worker’s statement shows regular pay 240, overtime 90, deduction 20 and amount due 310. These are illustrative contract rates. Reprint the statement in the worker’s chosen language and retain the same payroll and cost-center references and decimal amounts.

Import the same machine event again after an administrator changes the worker’s display name or UI language. It still maps to the original worker, and the 310 total is unchanged. An unmatched checkout produces a localizable review reason and zero auto-approved overtime. Keep original personal names in their script; localize earning/deduction captions, hours and period presentation. A supervisor who views a different project cannot retrieve the worker’s complete payslip through a translated dashboard.

## Remaining evidence

The shipped shift-pairing logic, overtime rules, overnight and split placements, deductions, statement approvals, posting accounts, currency rounding, available translations and settlement mechanism need versioned source or authorized example records. Payroll rates in the example describe a fixture, not statutory rates.
