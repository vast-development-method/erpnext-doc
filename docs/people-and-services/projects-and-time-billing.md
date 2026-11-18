# Projects and time billing

Consult [project costing](../transactions/project-costing.md) for purchase, material, time and invoice attribution.

## Business model

A project groups a customer's or organisation's work, schedule, responsibilities, tasks, time, commercial orders, invoices, purchased services, and consumed material. A task describes work within a project and may belong to a group task. Task hierarchy and task dependencies are separate relationships: a parent organises work; a dependency restricts completion and can drive schedule changes. A timesheet is a submitted operational record with one or more time rows; its monetary totals are management measures until invoicing or another explicit posting operation recognises a financial consequence.

Keep project estimated value, order value, billable time value, invoiced value, labour costing, purchase cost, and consumed-material cost separately. They measure different facts and must not be collapsed into a generic revenue or cost field. The normal costing basis uses company currency. The employee-expense costing variant takes time amounts in sheet currency, which requires separate reconciliation on a multicurrency job. Task records hold expected and actual dates, progress percentage, weight, expected and actual time, cost, and billable amount. Time rows retain activity, employee through their parent, project, task, beginning and ending timestamps, actual hours, billable marker, billing hours, costing rate, billing rate, calculated amounts, invoice association, and completion marker.

## Task integrity and completion

Expected and actual date ranges must be ordered. A child task's expected end cannot exceed its parent's expected end. The defined interactive validation also checks task expected and actual dates against the project's expected date window. A parent must be a group task. Template tasks are identified separately; their parent and dependencies must also be templates. A completed-on date cannot be in the future.

A task cannot move to completed while any dependency is neither completed nor cancelled. Completing a task closes its assignments and sets progress to 100. The defined progress check rejects values above 100; it does not establish a corresponding lower-bound rejection. Where a start and expected duration are supplied without an end, derive the expected end by adding that duration.

The dependency graph must not contain a path returning to the task itself. The bounded reachability scan is described below. On task update, it checks the graph, reschedules dependent work, updates the project, adjusts assignments, and adds a parent dependency when applicable. Deleting a task with child tasks is rejected.

When a task has an expected end, otherwise an actual end, find its dependent open tasks in the same project. If such a dependent task has both expected dates and begins before that end, move its beginning to one day after the end and preserve its original difference between expected end and beginning. A dependent task beginning exactly on that end does not satisfy the strict earlier-than comparison. This is date-based rescheduling, not a working-calendar duration calculation.

Project membership changes grant shares to newly added users and revoke shares from removed users. A public task form can create or change a project association when the user has project write permission or is listed as a project user. An unchanged project on an existing task bypasses that association-change test, while other document permissions still apply.

## Project completion mathematics

| Method | Calculation | Three tasks of weights 2, 3 and 5, respectively completed, cancelled and working at 20% |
|---|---|---|
| Completion count or blank method | Completed and cancelled task count divided by all project tasks, times 100. | 66.67% |
| Task progress | Arithmetic mean. Completed and cancelled tasks each contribute 100 regardless of their stored progress. | 73.33% |
| Task weight | Sum of effective progress × weight divided by total weight. A zero total weight substitutes one for every task. Round the final percentage to two decimals. | 60.00%. With all weights zero, 73.33%. |
| Manual | Validate the user-entered percentage between zero and 100. Setting Completed makes it 100. | Retain the entered value unless completed. |

Calculated progress is zero with no tasks. Explicit completion of a taskless project switches it to manual 100. Cancelled and on-hold statuses survive recalculation. A manual attempt to mark an existing calculated project Completed with unfinished progress is rejected. On an ordinary task update, entering Completed requires all listed dependencies to be completed or cancelled. It sets completion date if absent, closes assignments and sets task progress to 100. A time log marked completed can finish a task. Recomputing from surviving time logs keeps a task already completed or cancelled in that state.

Saving a task checks its dependency graph in each direction. The bounded dependency check expands at most 15 list entries in each direction. Do not claim full cycle detection on arbitrary graphs from this bounded search. In ordinary rescheduling, an open, working or overdue dependent in the same project with both dates and a start strictly before its prerequisite's end moves to the following day. Preserve the difference between its original dates. The owning parent task is excluded from that rescheduling query. A prerequisite ending 12 June moves a 10–15 June dependent to 13–18 June, while a dependent beginning on the 12th stays put. The explicit project completion/cancellation service checks project write access, applies the target status to tasks in dependency order with rescheduling suppressed, and then saves the project. Switching the project's language cannot change the dependency edges or their status identities.

## Time recording and validation

When both timestamps exist, actual hours equal elapsed seconds divided by 3,600. Ending before beginning is rejected. The row can also derive an ending timestamp from beginning plus actual hours; an existing end is replaced when the discrepancy is at least one second. Timekeeping does not automatically subtract lunch, holidays, or other nonworking intervals. Breaks require separate intervals or a deliberate additional business rule.

A nonbillable row has zero billing hours. A billable row with zero billing hours defaults its billing hours to actual hours. Billing hours greater than actual hours trigger a warning, not a rejection. This supports commercial billing that differs from time worked, but the decision must remain visible to the user. The task can supply a missing project reference; an explicitly provided row project must agree with the parent timesheet project, and the task must belong to the row's project.

Overlap validation is independently configurable for user and employee. When enabled for a supplied identity, compare against existing noncancelled timesheets and rows within the same timesheet. Reject intervals that begin inside an existing interval, end inside one, or contain it. Adjacent intervals whose only common point is an endpoint are permitted. The existing-row search excludes the current row and parent while a separate check covers internal overlap. Preserve this distinction when an entire timesheet is edited.

Submission requires time-row information and nonzero hours; when an employee is set, the activity type is required. The defined timestamp condition rejects a row when both timestamps are missing. Do not broaden this operation-specific check into a claim that every individual missing endpoint is rejected at that same stage; timestamp derivation and metadata requirements also participate. Submission, cancellation, and permitted changes after submission recalculate affected task and project aggregates. For each affected task, retain Completed or Cancelled. Otherwise use surviving submitted time rows: no rows gives Open, any row marking completion gives Completed, and other rows give Working.

## Rates, currency, and invoice mathematics

Choose the first matching rate pair in this order: employee and activity, activity with no employee, then activity type. A zero rate on a matched pair does not trigger another search. Convert from global default currency into requested currency when different. Existing nonzero row rates are preserved. Costing uses actual hours; billing uses billable hours. A missing parent exchange rate falls back to one. Converted rates and amounts are rounded at their respective field precisions, meaning the rounded converted rate multiplied by hours need not exactly equal a converted amount rounded independently.

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

The timesheet's state begins with draft, submitted, or cancelled from its document lifecycle. A billed percentage of at least 100 yields billed; a positive percentage below 100 yields partially billed. A direct parent invoice reference takes precedence and yields completed. Record these derived business labels separately from irreversible submission state.

Invoice creation rejects a timesheet with no billable hours or one whose billable hours all have already been billed. Remaining hours equal total billable hours minus billed hours; remaining amount equals total billable amount minus billed amount. The invoice's effective hourly rate is remaining amount divided by remaining hours. Preserve the individual unbilled time-row links in addition to the aggregated invoice line so that invoicing can be audited and cancellation can detach the correct work.

With actual hours 2.5, billing hours 3, costing rate 40, billing rate 80, and exchange rate 1.2, labour costing is 100, billable amount is 240, company-currency costing is 120, and company-currency billable amount is 288 before field-specific rounding. The difference between actual and billable hours must be disclosed as a warning while retaining the amounts.

## Project costing and financial boundaries

Submitted orders establish contract value and submitted customer invoice items establish billed revenue. Time rows establish labour cost and billable value. Direct supplier services, supplier-delivered goods, capitalised freight and signed inventory value changes each have a separate attribution rule. The [project costing chapter](../transactions/project-costing.md) applies those rules to a worked multicurrency job. A project refresh requires project write permission.

## Acceptance and remaining checks

Acceptance requires: rejection of completion with an unfinished dependency; permitted completion with a cancelled dependency; exact project percentages for all four methods; adjacent time intervals accepted and overlapping intervals rejected; overlap settings applied independently; a warning for excess billable hours; deterministic per-field currency rounding; partial invoicing followed by invoicing of only the remaining rows; invoice cancellation restoring the correct billable state; and project parent/child attribution counting each invoice row once.

For simultaneous operations, check dependency, assignment and cost totals after both authorized saves have completed.

## State dimensions and durable records

| Record | Stored facts | Derived business state |
| --- | --- | --- |
| Project | Company, customer, expected dates, selected completion method, optional project template, user membership, cost and revenue associations | Open, completed, cancelled or on hold; calculated completion and commercial aggregates |
| Task | Project, optional group parent, dependency rows, subject, expected and actual dates, progress, weight, assignment and template marker | Open, working, pending review, overdue, completed or cancelled according to its workflow; completion requires dependency checks |
| Timesheet | Document lifecycle, company, optional employee, recording user, currency, exchange rate and stable time-row identities | Draft, submitted, cancelled, partially billed, billed or completed as specified above |
| Time row | Activity, project, task, beginning and ending, actual and billing hours, costing and billing rates, invoice link, task-completed marker | Monetary amounts and contribution to project/task aggregates |

The submitted/cancelled lifecycle must remain separate from the displayed billing label. A billed label does not authorise editing a submitted time interval, and a completed project does not imply every customer invoice has been paid. The customer on the project must agree with a customer order that is assigned to it; company ownership and [master eligibility](../model/README.md) apply independently.

## Interval and amount invariants

Treat each time interval as beginning-inclusive and ending-exclusive for overlap. Two intervals overlap when the later beginning is strictly earlier than the earlier ending. Thus 09:00–10:00 and 10:00–11:00 are adjacent and allowed, while 09:00–10:00 and 09:59–11:00 overlap by one minute. Compare both saved rows and other rows in the current unsaved document. When user overlap checking is disabled but employee overlap checking is enabled, the same employee must still be protected across different recording users.

Actual hours measure elapsed seconds divided by 3,600. Billing hours are a commercial quantity, not a replacement for actual hours. A billable row whose billing hours are zero takes its actual hours, so a deliberately free billable service is represented by zero billing rate with positive billing hours, or by a nonbillable row, according to the intended tracking result. It is not represented by relying on zero billable hours to survive the defaulting rule.

For converted amounts, specify the precision of each rate and amount field independently. At company-currency rate precision two and amount precision two, actual hours three, costing rate 0.335 and exchange rate one can display a converted rate 0.34 while a directly converted amount based on 1.005 rounds according to the configured rounding policy. The calculation order must use the configured decimal rounding method; presentation rounding must not silently change stored billable totals. Boundary examples exactly halfway between representable decimals need their own rounding-policy fixture.

## Invoice linkage and remaining-value allocation

The time-to-invoice command takes a time-record identity and optional product, customer and currency. The invoice is initially a draft. When a product is supplied, its generated line represents remaining billable hours at the effective remaining rate, while its time associations identify the unbilled rows. Without a product, the command still supplies the time associations and the caller must complete the invoice. The generation operation checks billable-hour availability but does not itself establish a submitted-time or record-permission guard. Authoritative invoice submission must apply its own linked-time and permission rules; caller visibility is not proof of authorisation. Customer, project, company and currency must remain coherent with the invoice's own validation. Creating a draft invoice must not be treated as a cash receipt or as final ledger recognition.

For example, recorded billable hours ten and billable amount 1,000, with four hours and 360 already billed, leave six hours and 640. The remaining effective rate is the exact fraction 320 divided by three, approximately 106.6667. An implementation must not take the original average rate 100 and bill 600, since that would lose 40 of remaining value. Apply invoice precision after computing the remaining value, and retain any document rounding adjustment under the invoice contract.

Because billed-hour progress is derived from row links, cancellation must detach only rows associated with the cancelled invoice and recalculate totals. It must not clear a row associated with a different valid invoice. Two billing commands operating concurrently on the same unbilled row require a final submission conflict check or another declared allocation guarantee. The record structure alone does not establish that race protection.

For a free service with eight billable hours at zero rate, two invoiced hours yield 25 percent billed by the hours fallback. Monetary ratio alone would otherwise leave the timesheet permanently at zero percent. When a direct parent invoice reference exists, completed takes precedence over billed/partially-billed display state.

## Scheduling, sharing and operation acceptance

A dependent task's rescheduling preserves the difference between its old expected dates, not an inclusive count of working days. If a prerequisite ends 12 June and an open dependent originally spans 10–15 June, move it to 13–18 June. If it originally starts exactly 12 June, the strictly-earlier trigger does not move it. Completed and cancelled dependent tasks are outside the open-task rescheduling selection.

Project membership determines direct project sharing. Removing a member revokes the share introduced by that membership, but permissions obtained through another role must still be evaluated normally. A website task association change requires project write permission or membership; maintaining the unchanged project does not repeat that particular association-change check.

Acceptance must compare stored results after the complete command, including related task status, project totals, assignments and invoice links. Submit a time record referencing several tasks with different completed markers; then cancel it and verify that aggregates use the surviving submitted time. A detected cycle rejects the save before rescheduling. Exercise a cycle beyond the ordinary bounded traversal separately.
