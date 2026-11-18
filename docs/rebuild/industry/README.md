# Workforce and sales application handoffs

These contracts follow operations that cross the workforce application, CRM product, ERP selling and enterprise accounting. The [people and services chapters](../../people-and-services/README.md) define the employee, leave, payroll, customer and sales records that participate in those transactions.

| Trace | Source of truth before handoff | Result and reversal |
|---|---|---|
| [Clock event to pay days](attendance-leave-payroll.md) | Shift, clock event, approval, attendance, leave type and payroll policy | Leave ledger, presence and slip inputs; cancellation selection and holiday boundaries |
| [Pay slip to cash](../../people-and-services/payroll-posting.md) · [evidence](payroll-posting.md) | Effective salary assignment and submitted payroll cohort | Wage and employer accruals, employee payable, draft bank journal, cancellation |
| [Candidate and employee funds](../../people-and-services/employee-recovery.md) · [evidence](recruiting-expenses-and-advances.md) | Applicant, job offer, referral, additional salary, approved advance/claim | Recruitment commitment, bonus identity, funding, sanctioned costs, advance clearing and return |
| [CRM deal to commercial order](crm-to-order.md) | CRM Deal/Organization/Product or native opportunity, mapped item/customer | Draft quote and ERP order, linked party provenance, different same-site/remote boundaries |

[Decision cases](cases.json) supply fixed input/output examples. [Case schema](cases.schema.json) defines a typed payload and expected result for each operation. [Source checks](verify-source.py) execute selected upstream function bodies in isolation using supplied records and stubbed persistence. They do not submit documents to a running ERP or perform statutory calculations. From this directory, pass the local HRMS and CRM clones to the checker, in that order.

```sh
python verify-source.py /path/to/hrms /path/to/crm
```

The [workforce–lending extension](../extensions/workforce-lending.md) describes the separate loan repayment transactions, and [product access synchronization](../extensions/regions-donation-operations.md) covers the catalog permission and sharing mirrors.

The inspected source packages are [Workforce](https://github.com/frappe/hrms/tree/1b2d7e034e0de8e30a9e513541d7741710587ad5), [Customer relationships](https://github.com/frappe/crm/tree/9ace234fceb3c5e7bd630b74f44ba1779e831abe) and [Business application](https://github.com/frappe/erpnext/tree/886ab6ae187244e7f1b852393384ab6019d56264). The golden cases cover source-level math, decision and mapping outcomes. Full-site checks still required include shift reprocessing after a partial commit, conflicting leave application cancellations, claim/advance settlement under concurrency, remote CRM recovery from partial contact sync, and reversing a posted payroll with a bank voucher and employer liabilities.
