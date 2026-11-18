# Quality and maintenance

## Persistent contracts

| Record family | Internal specification |
|---|---|
| Inspection decisions | Inspection, reading and template retain transaction association, observations and decision policy |
| Management system | Procedure, goal, review, action and feedback separate organisation-level improvement from goods acceptance |
| Customer service | Schedule, schedule detail and visit bind covered products and actual completion |
| Asset care | Maintenance task and maintenance log preserve assignee, due date, completion, certificate fields and recurring obligation |

[Inventory mathematics](../calculations/README.md) defines the inspection mean and [acceptance cases](../calculations/README.md) compare range, formula, manual and lifecycle decisions.

## Quality records and decision model

A quality inspection is a document linked to a transaction and product, optionally to a particular row and serial or batch identities. Its inspection template supplies parameters, acceptance values or formulas, and numeric or descriptive reading definitions. A parameter row can contain up to ten numerical observations, bounds, manual-decision flag and resulting acceptance state. The inspection itself also has a manual-decision flag and overall state. Preserve raw entered readings and the number format used to interpret them alongside any numerical result required for reliable future review.

Automatic inspection processes each non-manual reading. A descriptive reading passes when actual text exactly equals expected text, using empty text for a missing value. A numerical range reading passes only when at least one nonempty observation exists and every supplied observation is inclusively between minimum and maximum. Empty observations are ignored for that range check. When at least one reading exists and none is rejected, an automatic inspection is Accepted. If loading the default template still yields no rows, automatic reading evaluation does not set the header decision. One rejected row makes the automatic document Rejected. Do not substitute an average-only test for an all-observations-within-range rule.

## Numerical formulas and measurement precision

Formula-based criteria require a nonempty expression. The expression evaluates against the supported reading values and, for numeric rows, an arithmetic mean. The mean is the sum of nonempty observations divided by their count. With no observations it is zero. Missing individual reading variables are supplied as zero in the formula context. That differs from the mean's exclusion of empty observations and must be preserved. Invalid variable references and invalid expressions fail validation with an explanation. They must not default to acceptance.

For readings ten, twelve and fourteen, the mean is twelve. If bounds are eleven through thirteen, the range-based decision is Rejected even though the mean passes those bounds. A formula explicitly checking mean between eleven and thirteen may accept the same measurements. An empty numeric row fails a range check but a poorly chosen expression such as mean equals zero could evaluate true. Keep the distinction and expose the configured criterion to the operator.

Newly entered numeric readings are validated against the user's number format. Group separators and decimal separators are interpreted explicitly, and non-finite numerical values are rejected. Previously stored unchanged readings are not rejected merely because another user has a different number format. The decision procedure still interprets values during evaluation through its current parsing routines, so cross-locale save and decision stability needs a dedicated fixture. Preserve the original readings, the number format used on entry and the inspection verdict when exchanging inspection evidence.

## Which transactions require inspection

Inspection gating is conditional by document, product and stock effect. Purchase receipts, stock-updating purchase invoices and subcontract receipts use purchase inspection requirements. Delivery documents and stock-updating sales invoices use delivery inspection requirements. An invoice without stock update is outside this stock inspection gate. A stock movement uses its own inspection-required flag and an explicit purpose-to-row rule.

| Stock movement purpose | Rows inspected when the document requires inspection |
|---|---|
| Manufacture | Primary finished rows |
| Material receipt, repack, receipt from customer, subcontract return | Incoming warehouse rows |
| Material issue, transfer, production transfer, send to subcontractor, subcontract delivery, disassemble | Outgoing rows whose source and target warehouses differ |
| Material consumption for manufacture | Not included by this output-inspection rule |
| Secondary outputs from manufacture, repack or disassemble | Exempt from this primary quality gate |

For ordinary purchase receipts, purchase invoices, delivery documents and sales invoices, a setting can allow inspection after the movement. The after-movement bypass does not include subcontract receipts. Missing required inspection produces a warning on saving a draft and blocks submission. A linked but unsubmitted inspection and a rejected inspection each have their own configured action: Stop blocks submission. The alternative path warns. The specification therefore must not state that every rejected inspection universally prevents receipt or delivery. The configured policy is part of the business contract and must be exported with the data.

## Rejection, custody and accounting

Quality rejection is a decision about observed goods. It is not itself a stock issue, supplier debit or customer credit. Accepted and rejected receipt quantities can be stored in separate warehouses. Their valuation follows purchasing and inventory settings. The inspection status alone must not erase inventory value. Material returned to a supplier requires the supplier-return workflow with source quantity checks. Destruction or process loss requires its own stock or manufacturing transaction. This separation preserves the financial consequence of goods owned but unavailable for use.

A later inspection can change the operational eligibility of goods without recreating their receipt. Quarantine release requires its own authorised stock movement. Inspection alone leaves the warehouse balance unchanged.

## Customer maintenance scheduling

A customer maintenance schedule records customer, covered product, serial identities where relevant, sales order reference, responsible service person, date interval and number of visits. Generation works on drafts. It creates visit schedule rows with planned date, product, source item reference, responsible person and Pending completion state. Submission requires generated schedule rows, validates serial coverage, updates service coverage dates on relevant serial identities and creates calendar events for the responsible person or fallback owner.

The generated dates divide the day difference between end and start by the number of visits, repeatedly add that interval, then adjust each visit around holidays. The holiday rule moves a holiday date backward until a non-holiday date is found. A result beyond the interval end is capped to the end. The first visit follows the first calculated interval rather than automatically occurring on the start date.

Periodicity defaults use seven days for weekly, thirty for monthly, ninety-one for quarterly, one hundred eighty-two for half yearly and three hundred sixty-five for yearly when deriving visit counts and end dates. A separate minimum-duration validator uses ninety and one hundred eighty for quarterly and half yearly. An interval of 90 days meets the quarterly minimum while its derived visit count still uses 91 days.

## Asset maintenance and due-date records

Asset maintenance is a separate recurring obligation from customer service visits. It assigns maintenance or calibration tasks to team members, associates completion and due dates, and creates or updates planned or overdue log records. Due-date calculation uses daily and weekly day increments, monthly/quarterly/half-yearly month increments, and yearly/two-yearly/three-yearly year increments. It chooses the last completion date as the base when that is later than the start date.

Both initial scheduling and completion use the task’s end date. Keep a candidate due on or before that date while its base remains earlier. Clear it when the candidate is beyond the end or the base or latest completion has already reached the end. A weekly calibration begun 3 June with end date 10 June is due on 10 June. Completing it on that date schedules no 17 June occurrence. [Recurrence and reversal](traceable-stock-and-service.md#recompute-service-and-calibration-due-dates)

## Quality procedures, objectives and review decisions

Quality procedures form a single-parent hierarchy. A procedure contains ordered process rows, some of which reference child procedures. Adding a child that already belongs to a different parent is rejected. Adding a child marks the parent as a group and sets the child's parent when absent. Removing a child process clears its parent relationship. Moving a procedure updates both the old parent's child list and the new parent's child list. Deleting a procedure clears child-process references to it. Tree traversal for a populated parent follows the process-row order rather than alphabetically sorting its children.

A quality goal records objectives, target text and measurement unit, with optional procedure and review frequency. When a new review has no objective rows, copy the current goal objectives, targets and units into the review. Later changes to the goal do not justify overwriting an already populated review. Objective status is explicitly Open, Passed or Failed. The objective record does not calculate pass/fail by comparing a numerical measurement against target text. When the goal changes, validate every review objective against the new goal. Otherwise validate only new rows and rows whose objective changed.

Review state is Open when there are no objectives or any row lacks a final Passed or Failed result. Otherwise Failed when any row is Failed. Otherwise Passed. Therefore a review with one Failed objective and one Open objective remains Open until the open objective is resolved. An automatic rule of 'any failure immediately fails the review' would change this behavior. A corrective or preventive action has resolution rows and optional links to review, goal, procedure and feedback. Its state is Completed only when at least one resolution exists and all are Completed. With zero resolution rows the action stays Open.

Generate one review per due goal and date. A monthly or quarterly day beyond month end falls on the last day of that month. For detailed cadence and duplicate handling see [Inspection and corrective action](quality.md).

Feedback references a user or customer. If its referenced identity is empty, the identity becomes the current user and the reference type becomes User. When a feedback template is selected and no parameter rows exist, copy its parameters and give each an initial rating of one. Existing parameter rows are retained. A default rating is recorded input, not independently verified evidence that a customer supplied that score.

## Customer visit completion and cancellation

A maintenance visit requires at least one purpose row. A supplied serial must exist and meet the customer or delivery-history checks. When schedule details are linked, require a submitted schedule for the visit’s customer and company and validate the item on each referenced detail. The header detail takes precedence, otherwise inspect the details on the purpose rows. For any linked detail with a schedule-item reference, the visit date must be inside that item’s start and end dates inclusively.

On submit or cancellation, recompute each affected schedule detail from its remaining submitted visits under lock. Prefer the newest Fully Completed visit, then the newest other visit, using maintenance date and creation order. Write its completion status and date. When there is no remaining visit, set Pending and clear actual date. The visit itself receives its own Submitted or Cancelled lifecycle status.

An unscheduled visit linked to a service-coverage claim updates its resolution date, responsible service person and work performed. Fully Completed closes that claim, Partially Completed makes it Work In Progress, and otherwise it remains Open. Before cancelling a visit, later submitted visits against the predecessor identity must be cancelled first, comparing maintenance date then maintenance time. The loop retains the last nonempty predecessor identity from the visit's purpose rows for this guard. Multiple different predecessors in one visit therefore require a dedicated fixture. The routine does not establish that every predecessor receives the same later-visit guard.

For an unscheduled warranty visit, if a different submitted fully completed visit already covers the claim, a nonfinal visit leaves its resolution untouched. When cancellation does restore a claim, select another submitted visit against that claim by descending document identifier, map its completion state and restore its resolution details. If none exists, set Open and clear those details. The chronological cancellation guard and this resolution selection have distinct orderings. Parts or billable work require their own stock and billing documents.

## Asset maintenance completion and certificates

A maintenance log whose due date is earlier than the current date becomes Overdue unless its state is already Completed or Cancelled. A Completed log must have a completion date. A noncompleted log must not carry a completion date. Submission permits only Completed or Cancelled maintenance state.

Completing a log advances the task from its completion date under the same end-date rule, sets the task to Planned, and saves the enclosing plan to refresh future logs. Submitting a log with business outcome Cancelled marks the task Cancelled. Cancelling a submitted completed log is a different action. Rewind only when that log drives the current task schedule. Restore the latest surviving completion and the cancelled log’s due date. [Schedule-driving log and same-day tie](traceable-stock-and-service.md#recompute-service-and-calibration-due-dates)

A task's certificate-required flag is copied into the log, and the log has a certificate-attachment field. Completion validation does not require a nonempty attachment solely because that flag is set. A mandatory calibration-certificate gate would be a strengthened business rule and must be identified as such. No automatic accounting entry follows merely from recording a maintenance certificate or completing a log.

## Deterministic inspection acceptance examples

| Input and configuration | Expected result | Reason |
|---|---|---|
| Numeric bounds ten through twenty. Readings ten, blank, twenty | Accepted | All supplied readings are within inclusive bounds and at least one exists |
| Same bounds. All readings blank | Rejected | No observation was supplied |
| Bounds eleven through thirteen. Readings ten, twelve, fourteen | Rejected | Range mode evaluates each observation |
| Expression requires mean at least eleven and at most thirteen. Same readings | Accepted | Mean is twelve and expression explicitly uses the mean |
| No readings. Expression requires mean equal zero | Accepted under that expression | Mean fallback is zero. An observation-presence condition must be separately specified |
| Expected descriptive value `Clean`. Observed `clean` | Rejected | Descriptive comparison is exact and case-sensitive |
| Manual reading marked Rejected in automatic inspection | Overall Rejected | Manual row state is retained and participates in overall rejection |
| Manual inspection with an automatically rejected row | Manual overall state retained | Document-level manual policy suppresses overall automatic overwrite |
| Review rows Failed and Open | Review Open | Outstanding objectives take precedence over final failure |
| Corrective action with no resolution rows | Action Open | Completion requires one or more completed resolutions |

These cases must preserve configured policy and the raw observations separately from derived status. Recomputing a decision after a user changes number format is a compatibility test, not a reason to discard the original entered reading.

## Acceptance scenarios

1. With numeric bounds ten through twenty, accept observations ten and twenty. Reject nine, twenty-one or an entirely empty row.
2. Supply observations ten, twelve and fourteen. Verify mean twelve. Distinguish rejection under bounds eleven through thirteen from acceptance under an explicitly mean-based expression.
3. Reject a missing formula or an unsupported reading variable instead of marking the inspection Accepted.
4. Save a draft receipt lacking a required inspection and observe a warning. Submission must block unless the applicable after-movement policy allows the workflow.
5. Test unsubmitted and rejected inspections under both Stop and warning policies. An invoice without stock update must not accidentally invoke the warehouse inspection gate.
6. Inspect primary manufactured output and exempt applicable secondary rows. Material-consumption-only rows must not acquire an unintended output-inspection requirement.
7. Generate customer visits across a holiday and verify backward adjustment and interval-end handling.
8. Exercise quarter and half-year boundaries independently in date derivation and minimum-duration validation.
9. Verify the calibration due date when a candidate falls before, exactly on, and beyond the plan end. Cancel the driving log and separately cancel an older log when a later completion exists.

## Cost responsibility

Repair parts, purchase services and depreciation changes require their own authorised inventory or financial transactions. Completing a visit or recording a certificate has no ledger effect by itself.

## Visit and inspection checks

Exercise translated inspection decisions, multiple predecessors on a single service visit, visits recorded at the same timestamp and each recurrence period at a calendar boundary. Inspect the separate stock and asset-repair postings when a visit uses parts.

## Linked specifications

- **Record definitions** · [Inspection](../../schemas/data/record-types/quality_inspection.json) · [reading](../../schemas/data/record-types/quality_inspection_reading.json) · [template](../../schemas/data/record-types/quality_inspection_template.json) · [Procedure](../../schemas/data/record-types/quality_procedure.json) · [goal](../../schemas/data/record-types/quality_goal.json) · [review](../../schemas/data/record-types/quality_review.json) · [action](../../schemas/data/record-types/quality_action.json) · [feedback](../../schemas/data/record-types/quality_feedback.json) · [Schedule](../../schemas/data/record-types/maintenance_schedule.json) · [schedule detail](../../schemas/data/record-types/maintenance_schedule_detail.json) · [visit](../../schemas/data/record-types/maintenance_visit.json) · [Maintenance task](../../schemas/data/record-types/asset_maintenance_task.json) · [maintenance log](../../schemas/data/record-types/asset_maintenance_log.json)
- **Calculation and acceptance cases** · [Inventory mathematics](../../schemas/mathematics/inventory-calculations.json) · [acceptance cases](../../schemas/mathematics/inventory-acceptance-cases.json)
