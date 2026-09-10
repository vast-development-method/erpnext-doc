# Quality and maintenance

## Quality records and decision model

A quality inspection is a document linked to a transaction and product, optionally to a particular row and serial or batch identities. Its inspection template supplies parameters, acceptance values or formulas, and numeric or descriptive reading definitions. A parameter row can contain up to ten numerical observations, bounds, manual-decision flag and resulting acceptance state. The inspection itself also has a manual-decision flag and overall state. Preserve raw entered readings and the number format used to interpret them alongside any numerical result required for reliable future review.

Automatic inspection processes each non-manual reading. A descriptive reading passes when actual text exactly equals expected text, using empty text for a missing value. A numerical range reading passes only when at least one nonempty observation exists and every supplied observation is inclusively between minimum and maximum. Empty observations are ignored for that range check. An inspection without any rejected rows is automatically Accepted unless the document is manual; one rejected row makes the automatic document Rejected. Do not substitute an average-only test for an all-observations-within-range rule.

Evidence: source-artifact-f6270a13e7c3b6eb791d lines 271–417.

## Numerical formulas and measurement precision

Formula-based criteria require a nonempty expression. The expression evaluates against the supported reading values and, for numeric rows, an arithmetic mean. The mean is the sum of nonempty observations divided by their count; with no observations it is zero. Missing individual reading variables are supplied as zero in the inspected formula context. That differs from the mean's exclusion of empty observations and must be preserved. Invalid variable references and invalid expressions fail validation with an explanation; they must not default to acceptance.

For readings ten, twelve and fourteen, the mean is twelve. If bounds are eleven through thirteen, the range-based decision is Rejected even though the mean passes those bounds. A formula explicitly checking mean between eleven and thirteen may accept the same measurements. An empty numeric row fails a range check but a poorly chosen expression such as mean equals zero could evaluate true. A replacement must preserve the distinction and expose the configured criterion to the operator.

Newly entered numeric readings are validated against the user's number format. Group separators and decimal separators are interpreted explicitly, and non-finite numerical values are rejected. Previously stored unchanged readings are not rejected merely because another user has a different number format. The source still interprets values during evaluation through its current parsing routines, so cross-locale save and decision stability needs a dedicated fixture. An implementation that stores normalised values and source-format provenance would make that intent explicit, but it is a proposed strengthening until equivalence is demonstrated. Parsing evidence: source-artifact-f6270a13e7c3b6eb791d lines 584–617.

Evidence: source-artifact-f6270a13e7c3b6eb791d lines 271–417.

## Which transactions require inspection

Inspection gating is conditional by document, product and stock effect. Purchase receipts, stock-updating purchase invoices and subcontract receipts use purchase inspection requirements. Delivery documents and stock-updating sales invoices use delivery inspection requirements. An invoice without stock update is outside this stock inspection gate. A stock movement uses its own inspection-required flag and an explicit purpose-to-row rule.

| Stock movement purpose | Rows inspected when the document requires inspection |
|---|---|
| Manufacture | Primary finished rows |
| Material receipt, repack, receipt from customer, subcontract return | Incoming warehouse rows |
| Material issue, transfer, production transfer, send to subcontractor, subcontract delivery, disassemble | Outgoing rows whose source and target warehouses differ |
| Material consumption for manufacture | Not included by this inspected output-inspection rule |
| Secondary outputs from manufacture, repack or disassemble | Exempt from this inspected primary quality gate |

For commercial purchase or delivery flows, a setting can allow inspection after the movement. Missing required inspection produces a warning on saving a draft and blocks submission. A linked but unsubmitted inspection and a rejected inspection each have their own configured action: Stop blocks submission; the alternative path warns. The specification therefore must not state that every rejected inspection universally prevents receipt or delivery. The configured policy is part of the business contract and must be exported with the data.

Evidence: source-artifact-0bc8595c210f65691869 lines 15–163.

## Rejection, custody and accounting

Quality rejection is a decision about observed goods. It is not itself a stock issue, supplier debit or customer credit. Accepted and rejected receipt quantities can be stored in separate warehouses. Their valuation follows purchasing and inventory settings; the inspection status alone must not erase inventory value. Material returned to a supplier requires the supplier-return workflow with source quantity checks. Destruction or process loss requires its own stock or manufacturing transaction. This separation preserves the financial consequence of goods owned but unavailable for use.

A later inspection can change the operational eligibility of goods without recreating their receipt. If an implementation adds quarantine release or automatic warehouse transfer based on quality status, that must be a specified additional workflow with explicit stock entries, permissions and repeat protection. Automatic quarantine release has not been established by the source ranges reviewed here.

## Customer maintenance scheduling

A customer maintenance schedule records customer, covered product, serial identities where relevant, sales order reference, responsible service person, date interval and number of visits. Generation works on drafts. It creates visit schedule rows with planned date, product, source item reference, responsible person and Pending completion state. Submission requires generated schedule rows, validates serial coverage, updates service coverage dates on relevant serial identities and creates calendar events for the responsible person or fallback owner.

The generated dates divide the day difference between end and start by the number of visits, repeatedly add that interval, then adjust each visit around holidays. The inspected holiday rule moves a holiday date backward until a non-holiday date is found; a result beyond the interval end is capped to the end. The first visit follows the first calculated interval rather than automatically occurring on the start date.

Periodicity defaults use seven days for weekly, thirty for monthly, ninety-one for quarterly, one hundred eighty-two for half yearly and three hundred sixty-five for yearly when deriving visit counts and end dates. A separate minimum-duration validator uses ninety and one hundred eighty for quarterly and half yearly. These are distinct observed rules, not a typographical simplification to calendar months. A replacement seeking equivalence needs fixtures around these boundary differences. A proposed calendar-month policy should be documented as an intentional change.

Evidence: source-artifact-42c1faca32e03699af0b lines 50–235.

## Asset maintenance and due-date records

Asset maintenance is a separate recurring obligation from customer service visits. It assigns maintenance or calibration tasks to team members, associates completion and due dates, and creates or updates planned or overdue log records. The inspected due-date helper uses daily and weekly day increments, monthly/quarterly/half-yearly month increments, and yearly/two-yearly/three-yearly year increments. It chooses the last completion date as the base when that is later than the start date.

There is an observed source anomaly in the final end-date condition: a supplied end date combined with a nonempty calculated next due date clears that due date, even if it is earlier than the end date. This specification does not silently recast that expression as the usual 'next due date after end date' rule. Reproduction of the observed result and adoption of the likely intended bounded recurrence are different acceptance decisions. Record this as an unresolved compatibility question until an executable reference fixture establishes the required product decision.

Evidence: source-artifact-c65f632ea7a7ac1fdac5 lines 97–175.

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

Quality procedure, goal, review, feedback, action and report records belong to the broader quality-management catalog. Calibration certificate enforcement, completed visit restrictions, customer issue resolution, repair-part accounting and every maintenance recurrence edge require additional behavioral review. This document supplies source-inspected inspection and scheduling contracts; it does not claim a fully executed quality-management certification or a complete live maintenance run.
