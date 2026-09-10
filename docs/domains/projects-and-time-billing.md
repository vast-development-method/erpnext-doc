# Projects and time billing

## Business model

A project groups a customer's or organisation's work, schedule, responsibilities, tasks, time, commercial orders, invoices, purchased services, and consumed material. A task describes work within a project and may belong to a group task. Task hierarchy and task dependencies are separate relationships: a parent organises work; a dependency restricts completion and can drive schedule changes. A timesheet is a submitted operational record with one or more time rows; its monetary totals are management measures until invoicing or another explicit posting operation recognises a financial consequence.

Keep project estimated value, order value, billable time value, invoiced value, labour costing, purchase cost, and consumed-material cost separately. They measure different facts and must not be collapsed into a generic revenue or cost field. Project monetary aggregates use company-currency values. Task records hold expected and actual dates, progress percentage, weight, expected and actual time, cost, and billable amount. Time rows retain activity, employee through their parent, project, task, beginning and ending timestamps, actual hours, billable marker, billing hours, costing rate, billing rate, calculated amounts, invoice association, and completion marker. Evidence: `source-artifact-fbb290b930b6e27bd40d lines 262–415`. Evidence: `source-artifact-c22a3364aa56314f9e13 lines 46–137`.

## Task integrity and completion

Expected and actual date ranges must be ordered. A child task's expected end cannot exceed its parent's expected end. The inspected interactive validation also checks task expected and actual dates against the project's expected date window. A parent must be a group task. Template tasks are identified separately; their parent and dependencies must also be templates. A completed-on date cannot be in the future.

A task cannot move to completed while any dependency is neither completed nor cancelled. Completing a task closes its assignments and sets progress to 100. The explicitly inspected progress check rejects values above 100; it does not establish a corresponding lower-bound rejection. Do not present a nonnegative lower bound as an observed rule without an additional metadata or runtime check. Where a start and expected duration are supplied without an end, derive the expected end by adding that duration. Evidence: `source-artifact-99dd9269f4b4ba1e67df lines 79–221`.

The dependency graph must not contain a path returning to the task itself. The inspected check traverses dependency reachability in both directions without an arbitrary depth cap. On task update, it checks the graph, reschedules dependent work, updates the project, adjusts assignments, and adds a parent dependency when applicable. Deleting a task with child tasks is rejected.

When a task has an expected end, otherwise an actual end, find its dependent open tasks in the same project. If such a dependent task has both expected dates and begins before that end, move its beginning to one day after the end and preserve its original difference between expected end and beginning. A dependent task beginning exactly on that end does not satisfy the strict earlier-than comparison. This is date-based rescheduling, not a working-calendar duration calculation. Evidence: `source-artifact-99dd9269f4b4ba1e67df lines 216–365`.

Project membership changes grant shares to newly added users and revoke shares from removed users. A public task form can create or change a project association when the user has project write permission or is listed as a project user. An unchanged project on an existing task bypasses that association-change test, while other document permissions still apply. Evidence: `source-artifact-fbb290b930b6e27bd40d lines 441–468`. Evidence: `source-artifact-99dd9269f4b4ba1e67df lines 216–365`.

## Project completion mathematics

The project chooses one calculation method:

| Method | Calculation and boundary |
| --- | --- |
| Manual | User-maintained percentage between zero and 100; setting completed forces 100 |
| Task completion | 100 multiplied by count of completed or cancelled tasks divided by total task count |
| Task progress | Sum of task progress percentages divided by total task count |
| Task weight | Sum, over tasks, of task progress multiplied by the weight share rounded to two decimal places |

Calculated results are rounded to two decimal places. With no tasks, calculated progress is zero. A project with no tasks can nevertheless be explicitly completed, which switches the method to manual and sets 100. Calculated completion updates status to completed exactly at 100 and otherwise open, except that a manually selected cancelled or on-hold state is preserved. Task cancellation counting as complete is an observed rule, not an assumption that cancelled work was performed. The weight share is calculated by safe division, which returns zero for a zero denominator and rounds each division to two decimal places before multiplication by task progress. Final project progress is also rounded to two decimal places. Consequently, three equally weighted tasks at 100 percent each produce 99 percent, because each share is 0.33. Do not defer all rounding to the final sum or normalise the rounded weights to one. Evidence: `source-artifact-fbb290b930b6e27bd40d lines 262–415`. Evidence: `source-artifact-91eb5c3685f0ea77eecb lines 1364–1377`.

For example, four tasks with two completed, one cancelled, and one open produce 75 percent under task completion. Progresses of 100, 50, 0, and 0 produce 37.5 percent under task progress. Two tasks with progresses 50 and 100 and weights 1 and 3 produce 87.5 percent under task weight. Changing the selected method can change the displayed project completion without changing any task's factual status.

## Time recording and validation

When both timestamps exist, actual hours equal elapsed seconds divided by 3,600. Ending before beginning is rejected. The row can also derive an ending timestamp from beginning plus actual hours; an existing end is replaced when the discrepancy is at least one second. Timekeeping does not automatically subtract lunch, holidays, or other nonworking intervals. Breaks require separate intervals or a deliberate additional business rule.

A nonbillable row has zero billing hours. A billable row with zero billing hours defaults its billing hours to actual hours. Billing hours greater than actual hours trigger a warning, not a rejection. This supports commercial billing that differs from time worked, but the decision must remain visible to the user. The task can supply a missing project reference; an explicitly provided row project must agree with the parent timesheet project, and the task must belong to the row's project. Evidence: `source-artifact-c22a3364aa56314f9e13 lines 46–137`.

Overlap validation is independently configurable for user and employee. When enabled for a supplied identity, compare against existing noncancelled timesheets and rows within the same timesheet. Reject intervals that begin inside an existing interval, end inside one, or contain it. Adjacent intervals whose only common point is an endpoint are permitted. The existing-row search excludes the current row and parent while a separate check covers internal overlap. A replacement must preserve this distinction when an entire timesheet is edited.

Submission requires time-row information and nonzero hours; when an employee is set, the activity type is required. The inspected timestamp condition rejects a row when both timestamps are missing. Do not broaden this source-specific check into a claim that every individual missing endpoint is rejected at that same stage; timestamp derivation and metadata requirements also participate. Submission, cancellation, and permitted changes after submission recalculate affected task and project aggregates. For each referenced task, the current timesheet's completion markers determine completed versus working status in the inspected update operation. Evidence: `source-artifact-8595348130b8e717250e lines 68–285`.

## Rates, currency, and invoice mathematics

An activity-cost lookup first seeks an employee-and-activity-specific rate, then falls back to the activity type. Only the fallback activity-type branch performs optional conversion from the global default currency into a requested currency in the inspected helper. Existing nonzero row rates are preserved. Evidence: `source-artifact-8595348130b8e717250e lines 507–531`. Costing uses actual hours; billing uses billable hours. A missing parent exchange rate falls back to one. Converted rates and amounts are rounded at their respective field precisions, meaning the rounded converted rate multiplied by hours need not exactly equal a converted amount rounded independently.

| Output | Calculation |
| --- | --- |
| Costing amount | Costing rate multiplied by actual hours |
| Billing amount | Billing rate multiplied by billing hours |
| Company-currency costing amount | Round costing amount multiplied by exchange rate at amount precision |
| Company-currency billing amount | Round billing amount multiplied by exchange rate at amount precision |
| Total hours | Sum of all row actual hours |
| Total billable hours | Sum of billable row billing hours |
| Total billed hours | Sum of billable row billing hours with an invoice association |
| Billed percentage | 100 multiplied by billed amount divided by billable amount when both are positive; otherwise use billed hours divided by billable hours when both are positive; otherwise zero |

The timesheet's state begins with draft, submitted, or cancelled from its document lifecycle. A billed percentage of at least 100 yields billed; a positive percentage below 100 yields partially billed. A direct parent invoice reference takes precedence and yields completed. Record these derived business labels separately from irreversible submission state. Evidence: `source-artifact-c22a3364aa56314f9e13 lines 46–137`. Evidence: `source-artifact-8595348130b8e717250e lines 68–285`.

Invoice creation rejects a timesheet with no billable hours or one whose billable hours all have already been billed. Remaining hours equal total billable hours minus billed hours; remaining amount equals total billable amount minus billed amount. The invoice's effective hourly rate is remaining amount divided by remaining hours. Preserve the individual unbilled time-row links in addition to the aggregated invoice line so that invoicing can be audited and cancellation can detach the correct work. Evidence: `source-artifact-8595348130b8e717250e lines 453–500`.

With actual hours 2.5, billing hours 3, costing rate 40, billing rate 80, and exchange rate 1.2, labour costing is 100, billable amount is 240, company-currency costing is 120, and company-currency billable amount is 288 before field-specific rounding. The difference between actual and billable hours must be disclosed as a warning while retaining the amounts.

## Project costing and financial boundaries

Project actual beginning and ending derive from the earliest and latest timestamps in submitted time rows; actual time is the sum of their hours. Labour costing and billable value sum company-currency amounts from those rows. Order value comes from submitted order net totals. Billed value sums submitted invoice-row net amounts assigned to the project. Parent-project attribution applies only to invoice rows without their own project, avoiding double counting when both parent and child carry a project.

The project purchase-cost aggregate sums company-currency net amounts from submitted purchase invoice rows explicitly assigned to the project. It does not establish the same parent-project fallback used in customer invoice aggregation. The explicit refresh command requires project write permission. Evidence: `source-artifact-fbb290b930b6e27bd40d lines 852–870`.

Project expense measure equals labour costing plus purchase cost plus consumed-material cost. Gross margin equals billed amount minus that expense measure. Gross margin percentage equals 100 multiplied by gross margin divided by billed amount; with zero billed amount it is zero. This is the project's particular management calculation. Do not infer that it reconciles to every general-ledger expense or accrual merely because it uses the term margin. Evidence: `source-artifact-fbb290b930b6e27bd40d lines 262–415`.

## Acceptance and remaining checks

Acceptance requires: rejection of completion with an unfinished dependency; permitted completion with a cancelled dependency; exact project percentages for all four methods; adjacent time intervals accepted and overlapping intervals rejected; overlap settings applied independently; a warning for excess billable hours; deterministic per-field currency rounding; partial invoicing followed by invoicing of only the remaining rows; invoice cancellation restoring the correct billable state; and project parent/child attribution counting each invoice row once.

These rules come from inspected controllers. The reference application was not started and its project test suite was not executed for this review. The dependency graph, rescheduling, project sharing, and purchase attribution rules are documented above; their simultaneous-update and rollback behaviour still require executed acceptance fixtures before claiming executable parity.
