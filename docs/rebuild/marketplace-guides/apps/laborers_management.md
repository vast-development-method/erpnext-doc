# Labor Management System

[Business workflow and acceptance cases](../../../capabilities/guides/people.md#temporary-labour-placement-and-pay).

## Publisher evidence

Micro Solution lists version 14. The product handles temporary workers from registration and placement through attendance, deductions, payslips and payment. Staff enter or import worker identity and mobile details and define project, profit/cost assignment, work breakdown, subcontractor, attendance machine, shift and worker organization. Placement assigns the worker to a project, shift and cost center. Imported attendance logs produce attendance and overtime. Staff enter payment adjustments, generate a payslip and pay it. The linked vendor guide did not yield readable documentation during this review. [Marketplace workflow](https://cloud.frappe.io/marketplace/apps/laborers_management) · [Linked guide](https://www.micro-sl.com/labor-management-system) · [Listed repository](https://github.com/micro-sl/laborers_management)

## What the publisher's screens show

The workspace gives separate entries to machine logs, attendance allowances, timesheet assignments and bulk adjustments. It presents the payslip, payslip payment and payroll batch as separate operations. The role screen distinguishes master-data, operations and viewer roles. This identifies role labels, without establishing their individual permission grants. [Workspace](https://cloud.frappe.io/files/l1.webp) · [Role assignments](https://cloud.frappe.io/files/l4.webp)

In the workflow drawing, a placement leads to an attendance log, then attendance. Attendance feeds overtime; attendance, overtime and payment adjustments feed the payslip, which in turn leads to its payment. The report screenshot breaks payslips down by project, profit center and payment type. The sample shows project P101 with 120 in timesheet earnings and 80 for overtime; a separate adjustment row shows 100 with no project displayed. The example supplies neither a currency nor a pay-rate formula. [Workflow diagram](https://cloud.frappe.io/files/Screenshot%20from%202023-09-21%2009-20-01.webp) · [Payslip-by-type report](https://cloud.frappe.io/files/Screenshot%20from%202023-09-21%2009-20-57.webp)

## Proposed rebuild contract

[Read the consolidated workflow](../../../capabilities/guides/people.md#temporary-labour-placement-and-pay-3).

## Multilingual operation and acceptance

[Read the consolidated acceptance cases](../../../capabilities/guides/people.md#temporary-labour-placement-and-pay-4).

## Remaining evidence

The shipped shift-pairing logic, overtime rules, overnight and split placements, deductions, statement approvals, posting accounts, currency rounding, available translations and settlement mechanism need versioned source or authorized example records. Payroll rates in the example describe a fixture, not statutory rates.
