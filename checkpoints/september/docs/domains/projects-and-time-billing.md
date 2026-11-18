# Projects and time billing

The internal definitions are [project](../../schemas/data/record-types/project.json), [task](../../schemas/data/record-types/task.json), [timesheet](../../schemas/data/record-types/timesheet.json) and [time row](../../schemas/data/record-types/timesheet_detail.json). Numerical definitions are in [customer and service calculations](../../schemas/mathematics/customer-and-service-calculations.json); executable acceptance inputs and expected results are in [customer and service acceptance cases](../../schemas/mathematics/customer-and-service-acceptance-cases.json). Posting consequences belong to [customer receivables](accounts-receivable.md), [supplier payables](accounts-payable.md) and [inventory](inventory-and-valuation.md).

## Business model

A project groups a customer's or organisation's work, schedule, responsibilities, tasks, time, commercial orders, invoices, purchased services, and consumed material. A task describes work within a project and may belong to a group task. Task hierarchy and task dependencies are separate relationships: a parent organises work; a dependency restricts completion and can drive schedule changes. A timesheet is a submitted operational record with one or more time rows; its monetary totals are management measures until invoicing or another explicit posting operation recognises a financial consequence.

Keep project estimated value, order value, billable time value, invoiced value, labour costing, purchase cost, and consumed-material cost separately. They measure different facts and must not be collapsed into a generic revenue or cost field. Project monetary aggregates use company-currency values. Task records hold expected and actual dates, progress percentage, weight, expected and actual time, cost, and billable amount. Time rows retain activity, employee through their parent, project, task, beginning and ending timestamps, actual hours, billable marker, billing hours, costing rate, billing rate, calculated amounts, invoice association, and completion marker.

## Task integrity and completion

Expected and actual date ranges must be ordered. A child task's expected end cannot exceed its parent's expected end. The defined interactive validation also checks task expected and actual dates against the project's expected date window. A parent must be a group task. Template tasks are identified separately; their parent and dependencies must also be templates. A completed-on date cannot be in the future.

A task cannot move to completed while any dependency is neither completed nor cancelled. Completing a task closes its assignments and sets progress to 100. The defined progress check rejects values above 100; it does not establish a corresponding lower-bound rejection. Do not present a nonnegative lower bound as an observed rule without an additional metadata or runtime check. Where a start and expected duration are supplied without an end, derive the expected end by adding that duration.

The dependency graph must not contain a path returning to the task itself. The defined check traverses dependency reachability in both directions without an arbitrary depth cap. On task update, it checks the graph, reschedules dependent work, updates the project, adjusts assignments, and adds a parent dependency when applicable. Deleting a task with child tasks is rejected.

When a task has an expected end, otherwise an actual end, find its dependent open tasks in the same project. If such a dependent task has both expected dates and begins before that end, move its beginning to one day after the end and preserve its original difference between expected end and beginning. A dependent task beginning exactly on that end does not satisfy the strict earlier-than comparison. This is date-based rescheduling, not a working-calendar duration calculation.

Project membership changes grant shares to newly added users and revoke shares from removed users. A public task form can create or change a project association when the user has project write permission or is listed as a project user. An unchanged project on an existing task bypasses that association-change test, while other document permissions still apply.

## Project completion mathematics

The project chooses one calculation method:

| Method | Calculation and boundary |
| --- | --- |
| Manual | User-maintained percentage between zero and 100; setting completed forces 100 |
| Task completion | 100 multiplied by count of completed or cancelled tasks divided by total task count |
| Task progress | Sum of task progress percentages divided by total task count |
| Task weight | Sum, over tasks, of task progress multiplied by the weight share rounded to two decimal places |

Calculated results are rounded to two decimal places. With no tasks, calculated progress is zero. A project with no tasks can nevertheless be explicitly completed, which switches the method to manual and sets 100. Calculated completion updates status to completed exactly at 100 and otherwise open, except that a manually selected cancelled or on-hold state is preserved. Task cancellation counting as complete is an observed rule, not an assumption that cancelled work was performed. The weight share is calculated by safe division, which returns zero for a zero denominator and rounds each division to two decimal places before multiplication by task progress. Final project progress is also rounded to two decimal places. Consequently, three equally weighted tasks at 100 percent each produce 99 percent, because each share is 0.33. Do not defer all rounding to the final sum or normalise the rounded weights to one.

For example, four tasks with two completed, one cancelled, and one open produce 75 percent under task completion. Progresses of 100, 50, 0, and 0 produce 37.5 percent under task progress. Two tasks with progresses 50 and 100 and weights 1 and 3 produce 87.5 percent under task weight. Changing the selected method can change the displayed project completion without changing any task's factual status.

## Time recording and validation

When both timestamps exist, actual hours equal elapsed seconds divided by 3,600. Ending before beginning is rejected. The row can also derive an ending timestamp from beginning plus actual hours; an existing end is replaced when the discrepancy is at least one second. Timekeeping does not automatically subtract lunch, holidays, or other nonworking intervals. Breaks require separate intervals or a deliberate additional business rule.

A nonbillable row has zero billing hours. A billable row with zero billing hours defaults its billing hours to actual hours. Billing hours greater than actual hours trigger a warning, not a rejection. This supports commercial billing that differs from time worked, but the decision must remain visible to the user. The task can supply a missing project reference; an explicitly provided row project must agree with the parent timesheet project, and the task must belong to the row's project.

Overlap validation is independently configurable for user and employee. When enabled for a supplied identity, compare against existing noncancelled timesheets and rows within the same timesheet. Reject intervals that begin inside an existing interval, end inside one, or contain it. Adjacent intervals whose only common point is an endpoint are permitted. The existing-row search excludes the current row and parent while a separate check covers internal overlap. A replacement must preserve this distinction when an entire timesheet is edited.

Submission requires time-row information and nonzero hours; when an employee is set, the activity type is required. The defined timestamp condition rejects a row when both timestamps are missing. Do not broaden this operation-specific check into a claim that every individual missing endpoint is rejected at that same stage; timestamp derivation and metadata requirements also participate. Submission, cancellation, and permitted changes after submission recalculate affected task and project aggregates. For each referenced task, the current timesheet's completion markers determine completed versus working status in the defined update operation.

## Rates, currency, and invoice mathematics

An activity-cost lookup first seeks an employee-and-activity-specific rate, then falls back to the activity type. Only the fallback activity-type branch performs optional conversion from the global default currency into a requested currency in the defined helper. Existing nonzero row rates are preserved. Costing uses actual hours; billing uses billable hours. A missing parent exchange rate falls back to one. Converted rates and amounts are rounded at their respective field precisions, meaning the rounded converted rate multiplied by hours need not exactly equal a converted amount rounded independently.

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

Project actual beginning and ending derive from the earliest and latest timestamps in submitted time rows; actual time is the sum of their hours. Labour costing and billable value sum company-currency amounts from those rows. Order value comes from submitted order net totals. Billed value sums submitted invoice-row net amounts assigned to the project. Parent-project attribution applies only to invoice rows without their own project, avoiding double counting when both parent and child carry a project.

The project purchase-cost aggregate sums company-currency net amounts from submitted purchase invoice rows explicitly assigned to the project. It does not establish the same parent-project fallback used in customer invoice aggregation. The explicit refresh command requires project write permission.

Project expense measure equals labour costing plus purchase cost plus consumed-material cost. Gross margin equals billed amount minus that expense measure. Gross margin percentage equals 100 multiplied by gross margin divided by billed amount; with zero billed amount it is zero. This is the project's particular management calculation. Do not infer that it reconciles to every general-ledger expense or accrual merely because it uses the term margin.

## Acceptance and remaining checks

Acceptance requires: rejection of completion with an unfinished dependency; permitted completion with a cancelled dependency; exact project percentages for all four methods; adjacent time intervals accepted and overlapping intervals rejected; overlap settings applied independently; a warning for excess billable hours; deterministic per-field currency rounding; partial invoicing followed by invoicing of only the remaining rows; invoice cancellation restoring the correct billable state; and project parent/child attribution counting each invoice row once.

These behavioral contracts have been checked against the supplied implementation material. No running-system project acceptance suite was executed for this review. The dependency graph, rescheduling, project sharing, and purchase attribution rules are documented above; their simultaneous-update and rollback behaviour still require executed acceptance fixtures before claiming executable parity.

## State dimensions and durable records

| Record | Stored facts | Derived business state |
| --- | --- | --- |
| Project | Company, customer, expected dates, selected completion method, optional project template, user membership, cost and revenue associations | Open, completed, cancelled or on hold; calculated completion and commercial aggregates |
| Task | Project, optional group parent, dependency rows, subject, expected and actual dates, progress, weight, assignment and template marker | Open, working, pending review, overdue, completed or cancelled according to its workflow; completion requires dependency checks |
| Timesheet | Document lifecycle, company, optional employee, recording user, currency, exchange rate and stable time-row identities | Draft, submitted, cancelled, partially billed, billed or completed as specified above |
| Time row | Activity, project, task, beginning and ending, actual and billing hours, costing and billing rates, invoice link, task-completed marker | Monetary amounts and contribution to project/task aggregates |

The submitted/cancelled lifecycle must remain separate from the displayed billing label. A billed label does not authorise editing a submitted time interval, and a completed project does not imply every customer invoice has been paid. The customer on the project must agree with a customer order that is assigned to it; company ownership and [master eligibility](company-and-master-governance.md) apply independently.

## Interval and amount invariants

Treat each time interval as beginning-inclusive and ending-exclusive for overlap. Two intervals overlap when the later beginning is strictly earlier than the earlier ending. Thus 09:00–10:00 and 10:00–11:00 are adjacent and allowed, while 09:00–10:00 and 09:59–11:00 overlap by one minute. Compare both saved rows and other rows in the current unsaved document. When user overlap checking is disabled but employee overlap checking is enabled, the same employee must still be protected across different recording users.

Actual hours measure elapsed seconds divided by 3,600. Billing hours are a commercial quantity, not a replacement for actual hours. A billable row whose billing hours are zero takes its actual hours, so a deliberately free billable service is represented by zero billing rate with positive billing hours, or by a nonbillable row, according to the intended tracking result. It is not represented by relying on zero billable hours to survive the defaulting rule.

For converted amounts, specify the precision of each rate and amount field independently. At company-currency rate precision two and amount precision two, actual hours three, costing rate 0.335 and exchange rate one can display a converted rate 0.34 while a directly converted amount based on 1.005 rounds according to the configured rounding policy. The calculation order must use the configured decimal rounding method; presentation rounding must not silently change stored billable totals. Boundary examples exactly halfway between representable decimals need their own rounding-policy fixture.

## Invoice linkage and remaining-value allocation

The time-to-invoice command takes a time-record identity and optional product, customer and currency. The invoice is initially a draft. When a product is supplied, its generated line represents remaining billable hours at the effective remaining rate, while its time associations identify the unbilled rows. Without a product, the command still supplies the time associations and the caller must complete the invoice. The generation operation checks billable-hour availability but does not itself establish a submitted-time or record-permission guard. Authoritative invoice submission must apply its own linked-time and permission rules; caller visibility is not proof of authorisation. Customer, project, company and currency must remain coherent with the invoice's own validation. Creating a draft invoice must not be treated as a cash receipt or as final ledger recognition.

Example: recorded billable hours ten and billable amount 1,000, with four hours and 360 already billed, leave six hours and 640. The remaining effective rate is the exact fraction 320 divided by three, approximately 106.6667. An implementation must not take the original average rate 100 and bill 600, since that would lose 40 of remaining value. Apply invoice precision after computing the remaining value, and retain any document rounding adjustment under the invoice contract.

Because billed-hour progress is derived from row links, cancellation must detach only rows associated with the cancelled invoice and recalculate totals. It must not clear a row associated with a different valid invoice. Two billing commands operating concurrently on the same unbilled row require a final submission conflict check or another declared allocation guarantee. The record structure alone does not establish that race protection.

For a free service with eight billable hours at zero rate, two invoiced hours yield 25 percent billed by the hours fallback. Monetary ratio alone would otherwise leave the timesheet permanently at zero percent. When a direct parent invoice reference exists, completed takes precedence over billed/partially-billed display state.

## Project aggregation matrix

| Measure | Included records | Attribution and exclusions |
| --- | --- | --- |
| Actual time | Submitted time rows | Match project, sum actual hours; cancelled and draft time do not count |
| Actual dates | Submitted time rows | Earliest beginning and latest ending |
| Labour costing | Submitted time rows | Sum company-currency costing amounts |
| Billable time value | Submitted time rows | Sum company-currency billing amounts |
| Order value | Submitted customer orders | Sum company-currency net totals attributed to project |
| Billed value | Submitted customer invoice rows | Match row project, or use parent project only when the row has no project |
| Purchase cost | Submitted supplier invoice rows | Explicit row project only; parent-only attribution is not included by this aggregate |
| Consumed material | Submitted stock-movement rows assigned to the project with no destination warehouse, plus company-currency additional costs on submitted manufacturing stock movements whose parent references the project | Sum row amounts and qualifying additional costs; destination-bearing transfers do not enter the first component |
| Gross margin | Billed value less labour costing, purchase cost and consumed material | A management measure; use financial statements for complete ledger profit |

For invoice rows of 100 assigned to Project East and 200 without a row project on a parent assigned to Project West, count 100 for East and 200 for West. Do not also assign the first 100 to West. For a supplier invoice with parent Project West but no project on its 200 row, the specific purchase-cost refresh described here counts zero for West. A proposal to add symmetric purchase fallback is a behavior change, not a harmless refactor.

## Scheduling, sharing and operation acceptance

A dependent task's rescheduling preserves the difference between its old expected dates, not an inclusive count of working days. If a prerequisite ends 12 September and an open dependent originally spans 10–15 September, move it to 13–18 September. If it originally starts exactly 12 September, the strictly-earlier trigger does not move it. Completed and cancelled dependent tasks are outside the open-task rescheduling selection.

Project membership determines direct project sharing. Removing a member revokes the share introduced by that membership, but permissions obtained through another role must still be evaluated normally. A website task association change requires project write permission or membership; maintaining the unchanged project does not repeat that particular association-change check.

Acceptance must compare stored results after the complete command, including related task status, project totals, assignments and invoice links. Submit a time record referencing several tasks with different completed markers; then cancel it and verify that aggregates use the surviving submitted time. Add a dependency that creates a cycle beyond several intermediate tasks and reject it before rescheduling anything. Race and rollback fixtures remain unexecuted obligations; the numerical fixtures in this repository demonstrate expected calculations, not a certification of a running replacement.
