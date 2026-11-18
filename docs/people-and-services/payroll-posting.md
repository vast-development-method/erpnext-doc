# Salary accrual, employer contributions and disbursement

The payroll run fixes company, period, payment currency/account, payable account, employee cohort and dimensions. The assignment relates an employee to an effective, submitted salary structure, its base and allocation. The salary slip carries the actual covered period, pay days, earning/deduction detail and associated run. The accounting journal references the run; a cash payment is a subsequent posting.

## Build and post

1. Select the effective submitted assignment for employee/structure no later than the actual period start. Reject a missing assignment. Check existing slips before generating duplicates. Batch creation and submission are separate operations; validate the resulting identities and submission state when resuming a run.
2. Use the salary component's company accounts and employee cost-centre allocation. Salary expense is debited, deductions credited and the net credited to payroll payable. Employee-wise accounting additionally retains party identities on payable entries. Referenced employee advance deductions have their own advance-account and employee links. Statistical components do not constitute a bank transfer.
3. Fetch employer-only contributions **before** linking slips to the accrual journal. The selection of unlinked slips would otherwise omit them. The service creates a separate submitted contribution journal. Debit each configured contribution expense account by cost centre; credit its configured liability, partitioned by employee when that mode is enabled. Round the contribution first, round each allocation except the last, then assign the remainder to the last cost centre. This expense never reduces employee take-home.
4. Generate the bank voucher separately with write permission. Ordinary and withheld salary selection are distinct. Calculate the eligible earnings less deductions and loan repayments; generate a payment voucher only if the resulting total is positive. Debit payroll payable, credit cash/bank. The called journal builder saves the bank voucher by default; posting still requires submission. The accrual builder explicitly submits its journal.

Assume one currency, a 20-day period, eligible payment days of 19.75, wage component 2,000 prorated by days, fixed retention 100 and employer contribution 10.01. The employee earns 1,975.00 and is owed 1,875.00. Two expense centres share the contribution 60/40. At two monetary decimals the first receives 6.01 and the second the residual 4.00.

| Posting event | Debits | Credits |
|---|---|---|
| Submitted salary accrual | Wages 1,975.00 | Deduction payable 100.00; payroll payable 1,875.00 |
| Submitted employer contribution accrual | Employer expense, centre A 6.01; employer expense, centre B 4.00 | Employer contribution payable 10.01 |
| Submitted bank payment | Payroll payable 1,875.00 | Bank 1,875.00 |

The fixed retention and employer contribution are inputs to this example. Statutory rates, brackets, contribution ceilings, exemptions, tax year and employer jurisdiction require effective-dated configuration. Use the rates effective for the employee’s jurisdiction when calculating an actual payroll.

## Failure and reversal

Submission may skip slips that the worker cannot submit and separately tracks the submitted list. Accrual runs when that list is nonempty. Review individual results together with the run status. In the outer failure path the worker rolls back in production and records a payroll failure. On cancellation the run cancels submitted linked slips, deletes linked slips (including drafts), cancels linked submitted payment-ledger records/journals and resets its created/submitted flags. A run with more than 50 linked slips schedules cancellation as background work. Restoring an earlier state in another system must also reverse posted balances and preserve its audit evidence. Banking-network refunds or already executed external transfers are separate settlement events.
