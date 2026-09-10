# Quality and maintenance

## Persistent contracts

| Record family | Internal specification |
|---|---|
| Inspection decisions | [Inspection](../../schemas/data/record-types/quality_inspection.json), [reading](../../schemas/data/record-types/quality_inspection_reading.json) and [template](../../schemas/data/record-types/quality_inspection_template.json) retain transaction association, observations and decision policy |
| Management system | [Procedure](../../schemas/data/record-types/quality_procedure.json), [goal](../../schemas/data/record-types/quality_goal.json), [review](../../schemas/data/record-types/quality_review.json), [action](../../schemas/data/record-types/quality_action.json) and [feedback](../../schemas/data/record-types/quality_feedback.json) separate organisation-level improvement from goods acceptance |
| Customer service | [Schedule](../../schemas/data/record-types/maintenance_schedule.json), [schedule detail](../../schemas/data/record-types/maintenance_schedule_detail.json) and [visit](../../schemas/data/record-types/maintenance_visit.json) bind covered products and actual completion |
| Asset care | [Maintenance task](../../schemas/data/record-types/asset_maintenance_task.json) and [maintenance log](../../schemas/data/record-types/asset_maintenance_log.json) preserve assignee, due date, completion, certificate fields and recurring obligation |

[Inventory mathematics](../../schemas/mathematics/inventory-calculations.json) defines the inspection mean and [acceptance cases](../../schemas/mathematics/inventory-acceptance-cases.json) compare range, formula, manual and lifecycle decisions.

## Quality records and decision model

A quality inspection is a document linked to a transaction and product, optionally to a particular row and serial or batch identities. Its inspection template supplies parameters, acceptance values or formulas, and numeric or descriptive reading definitions. A parameter row can contain up to ten numerical observations, bounds, manual-decision flag and resulting acceptance state. The inspection itself also has a manual-decision flag and overall state. Preserve raw entered readings and the number format used to interpret them alongside any numerical result required for reliable future review.

Automatic inspection processes each non-manual reading. A descriptive reading passes when actual text exactly equals expected text, using empty text for a missing value. A numerical range reading passes only when at least one nonempty observation exists and every supplied observation is inclusively between minimum and maximum. Empty observations are ignored for that range check. An inspection without any rejected rows is automatically Accepted unless the document is manual; one rejected row makes the automatic document Rejected. Do not substitute an average-only test for an all-observations-within-range rule.

## Numerical formulas and measurement precision

Formula-based criteria require a nonempty expression. The expression evaluates against the supported reading values and, for numeric rows, an arithmetic mean. The mean is the sum of nonempty observations divided by their count; with no observations it is zero. Missing individual reading variables are supplied as zero in the inspected formula context. That differs from the mean's exclusion of empty observations and must be preserved. Invalid variable references and invalid expressions fail validation with an explanation; they must not default to acceptance.

For readings ten, twelve and fourteen, the mean is twelve. If bounds are eleven through thirteen, the range-based decision is Rejected even though the mean passes those bounds. A formula explicitly checking mean between eleven and thirteen may accept the same measurements. An empty numeric row fails a range check but a poorly chosen expression such as mean equals zero could evaluate true. A replacement must preserve the distinction and expose the configured criterion to the operator.

Newly entered numeric readings are validated against the user's number format. Group separators and decimal separators are interpreted explicitly, and non-finite numerical values are rejected. Previously stored unchanged readings are not rejected merely because another user has a different number format. The reviewed decision procedure still interprets values during evaluation through its current parsing routines, so cross-locale save and decision stability needs a dedicated fixture. An implementation that stores normalised values and source-format provenance would make that intent explicit, but it is a proposed strengthening until equivalence is demonstrated.

## Which transactions require inspection

Inspection gating is conditional by document, product and stock effect. Purchase receipts, stock-updating purchase invoices and subcontract receipts use purchase inspection requirements. Delivery documents and stock-updating sales invoices use delivery inspection requirements. An invoice without stock update is outside this stock inspection gate. A stock movement uses its own inspection-required flag and an explicit purpose-to-row rule.

| Stock movement purpose | Rows inspected when the document requires inspection |
|---|---|
| Manufacture | Primary finished rows |
| Material receipt, repack, receipt from customer, subcontract return | Incoming warehouse rows |
| Material issue, transfer, production transfer, send to subcontractor, subcontract delivery, disassemble | Outgoing rows whose source and target warehouses differ |
| Material consumption for manufacture | Not included by this inspected output-inspection rule |
| Secondary outputs from manufacture, repack or disassemble | Exempt from this inspected primary quality gate |

For ordinary purchase receipts, purchase invoices, delivery documents and sales invoices, a setting can allow inspection after the movement. The reviewed after-movement bypass does not include subcontract receipts. Missing required inspection produces a warning on saving a draft and blocks submission. A linked but unsubmitted inspection and a rejected inspection each have their own configured action: Stop blocks submission; the alternative path warns. The specification therefore must not state that every rejected inspection universally prevents receipt or delivery. The configured policy is part of the business contract and must be exported with the data.

## Rejection, custody and accounting

Quality rejection is a decision about observed goods. It is not itself a stock issue, supplier debit or customer credit. Accepted and rejected receipt quantities can be stored in separate warehouses. Their valuation follows purchasing and inventory settings; the inspection status alone must not erase inventory value. Material returned to a supplier requires the supplier-return workflow with source quantity checks. Destruction or process loss requires its own stock or manufacturing transaction. This separation preserves the financial consequence of goods owned but unavailable for use.

A later inspection can change the operational eligibility of goods without recreating their receipt. If an implementation adds quarantine release or automatic warehouse transfer based on quality status, that must be a specified additional workflow with explicit stock entries, permissions and repeat protection. Automatic quarantine release has not been established by the behavioral paths described here.

## Customer maintenance scheduling

A customer maintenance schedule records customer, covered product, serial identities where relevant, sales order reference, responsible service person, date interval and number of visits. Generation works on drafts. It creates visit schedule rows with planned date, product, source item reference, responsible person and Pending completion state. Submission requires generated schedule rows, validates serial coverage, updates service coverage dates on relevant serial identities and creates calendar events for the responsible person or fallback owner.

The generated dates divide the day difference between end and start by the number of visits, repeatedly add that interval, then adjust each visit around holidays. The inspected holiday rule moves a holiday date backward until a non-holiday date is found; a result beyond the interval end is capped to the end. The first visit follows the first calculated interval rather than automatically occurring on the start date.

Periodicity defaults use seven days for weekly, thirty for monthly, ninety-one for quarterly, one hundred eighty-two for half yearly and three hundred sixty-five for yearly when deriving visit counts and end dates. A separate minimum-duration validator uses ninety and one hundred eighty for quarterly and half yearly. These are distinct observed rules, not a typographical simplification to calendar months. A replacement seeking equivalence needs fixtures around these boundary differences. A proposed calendar-month policy should be documented as an intentional change.

## Asset maintenance and due-date records

Asset maintenance is a separate recurring obligation from customer service visits. It assigns maintenance or calibration tasks to team members, associates completion and due dates, and creates or updates planned or overdue log records. The inspected due-date helper uses daily and weekly day increments, monthly/quarterly/half-yearly month increments, and yearly/two-yearly/three-yearly year increments. It chooses the last completion date as the base when that is later than the start date.

There is an observed source anomaly in the final end-date condition: a supplied end date combined with a nonempty calculated next due date clears that due date, even if it is earlier than the end date. This specification does not silently recast that expression as the usual 'next due date after end date' rule. Reproduction of the observed result and adoption of the likely intended bounded recurrence are different acceptance decisions. Record this as an unresolved compatibility question until an executable reference fixture establishes the required product decision.

## Quality procedures, objectives and review decisions

Quality procedures form a single-parent hierarchy. A procedure contains ordered process rows, some of which reference child procedures. Adding a child that already belongs to a different parent is rejected. Adding a child marks the parent as a group and sets the child's parent when absent. Removing a child process clears its parent relationship. Moving a procedure updates both the old parent's child list and the new parent's child list. Deleting a procedure clears child-process references to it. Tree traversal for a populated parent follows the process-row order rather than alphabetically sorting its children.

A quality goal records objectives, target text and measurement unit, with optional procedure and review frequency. When a new review has no objective rows, copy the current goal objectives, targets and units into the review. Later changes to the goal do not justify overwriting an already populated review. Objective status is explicitly Open, Passed or Failed; the reviewed objective record does not calculate pass/fail by comparing a numerical measurement against target text.

Review state precedence is Open when there are no objective rows or any row is Open; otherwise Failed when any row is Failed; otherwise Passed. Therefore a review with one Failed objective and one Open objective remains Open until the open objective is resolved. An automatic rule of 'any failure immediately fails the review' would change this behavior. A corrective or preventive action has resolution rows and optional links to review, goal, procedure and feedback. Its state is Open while any resolution is Open, otherwise Completed. The empty-resolution case is Completed in this decision routine.

Review generation runs for every daily goal, weekly goals matching the configured weekday, monthly goals matching the current day number, and quarterly goals on the first day of January, April, July and October. The metadata's weekly choices run Monday through Saturday, and the monthly day choices run one through thirty. The reviewed creation routine always inserts a review and does not check for an existing same-goal, same-date review. Repeating the scheduled invocation can therefore duplicate reviews. Duplicate suppression is an intentional improvement requiring a named uniqueness policy, not behavior already guaranteed here.

Feedback references a user or customer. If its referenced identity is empty, the identity becomes the current user and the reference type becomes User. When a feedback template is selected and no parameter rows exist, copy its parameters and give each an initial rating of one. Existing parameter rows are retained. A default rating is recorded input, not independently verified evidence that a customer supplied that score.

## Customer visit completion and cancellation

A maintenance visit requires at least one purpose row. Any serial identity entered in a purpose row must exist. A Scheduled visit with a linked schedule detail must fall inclusively within the start and end dates of the corresponding schedule item. When no header detail is selected, perform the equivalent date check for each linked purpose-row schedule detail. Unscheduled and Breakdown visits do not use this particular scheduled-date restriction.

On submission, set the visit document state to Submitted and update linked schedule details with the visit's Partially Completed or Fully Completed state and actual visit date. On cancellation, restore those schedule details to Pending and clear the actual date. This procedure writes the selected status directly; it is not an aggregation over every visit ever associated with the schedule detail.

An unscheduled visit linked to a service-coverage claim updates its resolution date, responsible service person and work performed. Fully Completed closes that claim, Partially Completed makes it Work In Progress, and otherwise it remains Open. Before cancelling a visit, later submitted visits against the inspected predecessor identity must be cancelled first, comparing maintenance date then maintenance time. The reviewed loop retains the last nonempty predecessor identity from the visit's purpose rows for this guard. Multiple different predecessors in one visit therefore require a dedicated fixture; the routine does not establish that every predecessor receives the same later-visit guard.

When cancellation restores a claim, it selects another submitted Partially Completed visit by descending document identifier, not by latest maintenance timestamp, and restores that visit's resolution details. If none exists, the claim becomes Open and those details are cleared. Keep this selection behavior distinct from the chronological cancellation guard. Visit completion itself does not consume repair parts or create an invoice: those require the applicable stock and billing records.

## Asset maintenance completion and certificates

A maintenance log whose due date is earlier than the current date becomes Overdue unless its state is already Completed or Cancelled. A Completed log must have a completion date. A noncompleted log must not carry a completion date. Submission permits only Completed or Cancelled maintenance state.

Completing a log updates the underlying maintenance task's last completion date, calculates its next due date from that completion date when changed, and resets the task to Planned. Cancelling through the log's maintenance state marks the task Cancelled. The completion recurrence call does not pass the task's end date into the due-date helper; it therefore differs from the end-date anomaly described above. After updating the task, the enclosing asset-maintenance record is saved and its future log maintenance runs.

A task's certificate-required flag is copied into the log, and the log has a certificate-attachment field. The inspected completion validation does not require a nonempty attachment solely because that flag is set. A mandatory calibration-certificate gate would be a strengthened business rule and must be identified as such. No automatic accounting entry follows merely from recording a maintenance certificate or completing a log.

## Deterministic inspection acceptance examples

| Input and configuration | Expected result | Reason |
|---|---|---|
| Numeric bounds ten through twenty; readings ten, blank, twenty | Accepted | All supplied readings are within inclusive bounds and at least one exists |
| Same bounds; all readings blank | Rejected | No observation was supplied |
| Bounds eleven through thirteen; readings ten, twelve, fourteen | Rejected | Range mode evaluates each observation |
| Expression requires mean at least eleven and at most thirteen; same readings | Accepted | Mean is twelve and expression explicitly uses the mean |
| No readings; expression requires mean equal zero | Accepted under that expression | Mean fallback is zero; an observation-presence condition must be separately specified |
| Expected descriptive value `Clean`; observed `clean` | Rejected | Descriptive comparison is exact and case-sensitive |
| Manual reading marked Rejected in automatic inspection | Overall Rejected | Manual row state is retained and participates in overall rejection |
| Manual inspection with an automatically rejected row | Manual overall state retained | Document-level manual policy suppresses overall automatic overwrite |
| Review rows Failed and Open | Review Open | Outstanding objectives take precedence over final failure |
| Corrective action with no resolution rows | Action Completed | No Open resolution exists in the reviewed decision routine |

These cases must preserve configured policy and the raw observations separately from derived status. Recomputing a decision after a user changes number format is a compatibility test, not a reason to discard the original entered reading.

## Acceptance scenarios

1. With numeric bounds ten through twenty, accept observations ten and twenty; reject nine, twenty-one or an entirely empty row.
2. Supply observations ten, twelve and fourteen. Verify mean twelve; distinguish rejection under bounds eleven through thirteen from acceptance under an explicitly mean-based expression.
3. Reject a missing formula or an unsupported reading variable instead of marking the inspection Accepted.
4. Save a draft receipt lacking a required inspection and observe a warning; submission must block unless the applicable after-movement policy allows the workflow.
5. Test unsubmitted and rejected inspections under both Stop and warning policies. An invoice without stock update must not accidentally invoke the warehouse inspection gate.
6. Inspect primary manufactured output and exempt applicable secondary rows; material-consumption-only rows must not acquire an unintended output-inspection requirement.
7. Generate customer visits across a holiday and verify backward adjustment and interval-end handling.
8. Exercise quarter and half-year boundaries independently in date derivation and minimum-duration validation.
9. For asset maintenance with an end date, preserve the observed due-date anomaly in a reference fixture and record any chosen corrected behavior as a deliberate deviation.

## Review boundary

The management-system, visit and maintenance-log decision procedures above supplement the inspection contracts. Cross-locale decision stability, multiple predecessors on one visit, exact timestamp ties and every calendar recurrence boundary remain required dynamic acceptance cases. Repair-part accounting belongs to inventory and asset-repair transactions rather than being an implicit effect of visit completion. This specification does not claim a completed live maintenance run or quality-management certification.
