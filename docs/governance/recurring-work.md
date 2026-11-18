# Recurring business operations

The scheduler selects due work. A selected operation then evaluates its business settings and record state. The date the scheduler ran, the posting date on a document and the date on which a payment becomes due can all differ. Store enough information to tell a late run from a completed economic event.

| When eligible | Work selected | Observable business result |
|---|---|---|
| Each quarter hour | Resume incomplete bill-of-material cost updates and eligible inventory revaluation batches | A cost roll-up or repost can continue after interruption. Its request and completion are distinct. Verify the affected item, warehouse and valuation order before using revised margins. |
| Hourly | Project reminders and overdue service agreements | Reminders follow the project's communication schedule. An overdue agreement can fail even when no operator opens the ticket. |
| Hourly maintenance | Unverified appointments, valuation work, retryable bulk transactions, project status collection and reminders, bank feeds and bank matching rules | Expired appointments cease to reserve availability according to appointment policy. An imported bank line remains a statement observation until matched. Retrying a transaction must distinguish previous success from remaining work. |
| Hourly maintenance | External video engagement | A refresh may change engagement counts. It leaves the video identity, description, permissions and related business document intact. |
| Daily | Ticket and opportunity closure, lead/event follow-up, invoice status, contract and service agreement status, quotation expiry, project and task status | Re-evaluate configured dates and conditions on eligible records. Quotation expiry changes its commercial availability. It does not reverse a posted invoice. |
| Daily | Fiscal-year creation, exchange revaluation where daily frequency is selected, ledger checks, depreciation postings, asset and serial maintenance status | Use the fiscal calendar and posting rules for the company. A maintenance status update and a depreciation charge have different ledger consequences. |
| Daily | Stock reordering, supplier scorecards, bill-of-material prices and quality reviews | Recalculate reorder need against projected stock and existing supply. Refreshing a bill of materials affects estimates. Actual posted stock value follows the valuation rules for the relevant movements. |
| Daily | Subscription processing, account statements, campaigns, digests, project billing totals and project communications | Generate eligible documents or recipient outputs for the configured period. A statement email records communication. Its delivery is independent of the outstanding amount. |
| Weekly | Exchange revaluation if selected, incorrect inventory valuations | Use the last eligible balances and identify prior work before generating a correction. The configured revaluation frequency selects which cycle applies. |
| Monthly | Deferred accounting and exchange revaluation if selected | Recognise the eligible fraction of service already earned or incurred. Revaluation measures an open monetary balance at the selected rate. The two operations have separate source records. |
| Frequent attendance processing opportunity | Interview reminders | Only interviews due under the reminder configuration produce a notice. |
| Hourly workforce processing | Check-in synchronisation, automatic attendance, shift schedule assignment | Resolve shifts and the completeness watermark before deriving attendance. A late-arriving check-in and an actually absent employee require distinct handling. |
| Daily workforce processing | Eligible birthdays, anniversaries, interview feedback, expired shifts and expired job openings | Notify the configured recipients. Expiring an assignment or vacancy changes its availability without deleting employee or applicant history. |
| Daily workforce entitlement processing | Expired allocations, leave encashment and earned-leave accrual | Retain the employee, leave category, eligible interval and previous posting. Reconcile entitlement movements before creating a payout. |
| Weekly or monthly workforce reminders | Advance notices for upcoming employee events | Select the configured frequency and recipient. A reminder has no payroll posting effect. |

**Backdated example.** Issue four units on Tuesday, then accept a Monday receipt that changes the issue valuation. The receipt can enqueue a future recalculation. Tuesday's issue keeps its original voucher and quantity. After the run completes, compare its recalculated carrying value with the balancing accounts and any affected job cost. A queued or failed request alone cannot establish the revised margin.

**Attendance boundary.** An overnight shift ends at 06:00. With a synchronisation watermark of 06:00, that shift is pending. Once the watermark passes 06:00, evaluate the events that belong to the shift's starting date. Retrying after attendance has been saved must recognise the check-ins already linked to it.

[Valuation and operational controls](../operations/README.md) · [Workforce attendance](../people-and-services/attendance-and-leave.md) · [Work dispatch](../services/work-dispatch.md)
