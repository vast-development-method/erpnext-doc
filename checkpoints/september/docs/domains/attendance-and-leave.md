# Attendance and leave

## Record boundaries

Attendance is an employee's evaluated daily or shift presence. A clock event is a timestamped observation from which attendance may be derived. A shift definition supplies time boundaries and evaluation policy; a dated assignment applies it to an employee. A holiday calendar classifies dates, including weekly rest days and half holidays. Leave is an authorised absence with a type, interval, entitlement allocation and ledger effects. These records must remain distinct: a raw clock event is not an approved day of attendance, and a leave balance is not a salary amount.

The persistent model includes clock events; shift definitions, requests, assignments, recurring schedules and locations; attendance and attendance requests; holiday assignments; leave types, policies, policy assignments, allocations, earned-leave schedule rows, applications, ledger entries, adjustments, compensatory requests and encashments. Leave ledger entries retain employee, company, leave type, effective interval, quantity, transaction source, carry-forward classification and cancellation state. Generated attendance retains links back to the evidence that created it.

## Shift definitions and scheduling

Start and end times must differ. When start is later than end, the shift ends on the following day. Buffered duration equals the nominal duration, rounded to minutes, plus the allowed early check-in buffer and late checkout buffer. A buffered duration of at least one thousand four hundred and forty minutes is rejected because the shift would overlap its own next occurrence. A twenty-two-hundred to zero-six-hundred shift is an eight-hour night shift, not a negative duration.

An active shift assignment validates the employee and date ordering. Multiple assignments with overlapping dates are rejected unless the corresponding setting permits them; even then, overlapping shift times are rejected. Inactive assignments bypass the overlap check. Cancellation is blocked when matching clock events or attendance records exist in the assigned interval, and successful cancellation makes the assignment inactive. The behaviour of unbounded assignment intervals in these reference checks requires a targeted runtime case.

Recurring schedules choose weekdays and a frequency of every week, every two weeks, every three weeks or every four weeks. Consecutive selected dates are grouped into individual assignment intervals. The repeat cycle is anchored relative to the supplied start date, and skipped weeks advance by seven times the gap count. With no explicit end, generation extends ninety days from the starting date. The last generated end date is stored so the next scheduled expansion begins the following day. This cursor and the generated assignment references prevent a recurring schedule from being mistaken for a single indefinitely active shift.

## Clock-event identity, location and immutability

Before validation, event timestamps discard microseconds. A duplicate is the same employee, timestamp and log type, excluding the record being edited. The same employee and second with a different log type is therefore not rejected by this exact duplicate check. A linked attendance record prevents changing the event time until that attendance is cancelled. Resolving a shift stores nominal start and end plus buffered actual start and end; an event outside every shift is marked off shift. A strict entry/exit classification requires a log type unless automatic attendance is explicitly skipped.

When geographic tracking is enabled, coordinates are required according to the inspected check. If a matching active assignment supplies a location with positive radius, compute geographic distance and reject only when distance exceeds the allowed metres. Equality is permitted. The current source examines the first matching assignment location, so multiple eligible locations need a conformance case. The coordinate-presence check treats two zero values as absent even though they identify a real geographic coordinate; preserve this as a known edge case or explicitly decide to correct it.

## Working-hour calculation

The calculation supports two independent choices: infer alternating entry and exit observations or obey explicit event types; and use the first entry through last exit or sum every valid pair. In alternating first-to-last mode, the entire span is paid, including breaks. In alternating pair mode, events are consumed in successive pairs and an unmatched final event contributes no interval. In strict first-to-last mode, find the first entry and final exit; missing either yields zero hours. In strict pair mode, accumulate valid entry/exit pairs in chronological order, ignoring events that do not complete the expected pair. Each measured interval is converted from seconds to hours and rounded to two decimal places before addition.

A worker observed at 08:00, 12:00, 13:00 and 17:00 has nine hours under first-to-last mode and eight hours under pair mode. Two intervals of one minute each round separately to 0.02 hours and sum to 0.04; rounding the combined two minutes once would instead produce 0.03. This difference is observable and must be retained in mathematical tests.

Automatic attendance groups eligible events by employee and nominal shift-start timestamp, so a night shift belongs to its starting calendar date. Events must be unlinked, not skipped, not off shift, at or after the processing start, and have buffered shift end strictly earlier than the last completed clock synchronisation. A shift ending exactly at the synchronisation marker remains pending. Processing is not one giant all-or-nothing operation: observed groups are committed, then absence marking proceeds in employee batches. A replacement should preserve restartable progress and absence/evidence consistency without prescribing the original infrastructure.

## Presence thresholds and exception flags

For each group, calculate hours first. Mark late only when the first entry is strictly later than shift start plus late grace minutes. Mark early departure only when final exit is strictly earlier than shift end minus early grace minutes. Exact equality does not set either flag. If the absence threshold is nonzero and hours are below it, mark absent. Otherwise, if the half-day threshold is nonzero and hours are below it, mark half day. Otherwise mark present. On a half holiday, both thresholds are divided by two. Zero thresholds disable their respective comparison.

With absence threshold four hours and half-day threshold seven hours, 3.99 hours is absent, exactly four is half day, 6.99 is half day and exactly seven is present. Neither lateness nor early departure directly implies a wage deduction in this calculation. Payroll uses attendance status and its own settings. Overtime exists only when permitted for the shift and measured hours exceed nominal standard hours; the difference is passed to overtime payroll, which applies its separate caps and pay multipliers.

## Leave allocation and entitlement ledger

Leave allocations cannot overlap a submitted allocation for the same employee and leave type. The allocation end must be later than its start: unlike an application, a one-day allocation is rejected by the inspected date check. Unpaid leave cannot be allocated. An allocation validates the maximum new entitlement for its leave period, total entitlement against interval length unless over-allocation is allowed, and current balance consistency. Zero total allocations are allowed only for the supported earned, compensatory or negative-balance cases.

Total allocated leave equals newly allocated leave plus eligible unused carry-forward, limited by configured maximum total. Carry-forward also obeys its own cap. For fifteen unused days, a ten-day carry cap and fifteen new days, total entitlement is twenty-five. With twenty-five new days and a thirty-day total cap, only five unused days carry. Creating a carry-forward allocation expires unused entitlement in the earlier allocation and records how much moved forward. The allocation tests explicitly establish those examples.

Earned-leave entitlement divides annual allocation by one, two, four or twelve for yearly, half-yearly, quarterly or monthly cycles. If joining occurs after the cycle begins, prorate by inclusive days from joining through cycle end divided by inclusive days in the cycle. Earned leave first rounds to system quantity precision and then, when selected, to quarter-day, half-day or whole-day increments. Those increments use nearest-value rounding with half-to-even behaviour inherited by the inspected rounding operation, rather than always rounding upward. For annual twenty-four days, a thirty-day month and joining on day sixteen, entitlement is two times fifteen divided by thirty, or one day.

Scheduled accrual compares previously accumulated new entitlement with the annual policy allocation, excludes carried balances from that comparison and rejects excess for non-yearly frequencies. A maximum total allocation can reduce the current increment to the remaining quota. Schedule rows record whether processing was attempted, allocated or failed and retain a failure reason; retries must not disguise a prior successful increment as another new entitlement. Carry-forward expiry has its own effective date and must distinguish already-consumed carried leave from still-available carried leave. The reviewed expiry test confirms expired carried entitlement is not carried again.

## Application validation and approval

An application validates active employment, dates, entitlement balance, overlap, maximum duration, blocked days, salary processing, attendance compatibility, optional-leave eligibility, service waiting period and approver requirements. The leave-day count is inclusive. A valid half-day date within the interval subtracts one half only when that day is not a holiday. When the leave type excludes holidays, subtract those holiday quantities. Requests producing zero or fewer leave days are rejected.

For a Monday-through-Friday application containing one excluded full holiday and one valid half day, consumed leave is three and a half days. A half-day marker on the holiday does not subtract another half day. A partially paid leave may consume one day of leave entitlement while reducing pay by a smaller fraction; the entitlement quantity and unpaid-pay equivalent must not share one overloaded field. The payroll mode discrepancy for partially paid leave is documented in [Payroll and benefits](payroll-and-benefits.md).

Open and approved non-cancelled applications are checked for overlap, including draft applications. Two qualifying half-day requests may share a date until the existing half-day total reaches one. Rejected requests do not reserve the same interval through this overlap query. Insufficient balance blocks ordinary paid leave, while a leave type allowing negative balances emits the inspected warning path and permits the request. Approval over blocked dates is denied to actors outside the configured exception conditions.

Submission requires approved or rejected status; open and cancelled status cannot be submitted. Approval updates attendance and creates leave-ledger effects; cancellation reverses the leave ledger and cancels linked attendance. Backdated applications involving already-expired allocations add a compensating expiry adjustment where required. These are current business corrections and do not constitute migration from an old software version.

Unpaid-leave application endpoints falling within an already submitted salary slip are rejected by the inspected salary-processing guard. Because this guard tests endpoints, an application wholly enclosing a payroll interval needs a specific test before claiming complete overlap protection. A mandatory approver setting requires a selected approver. With self-approval prevention enabled and no separate configured workflow, an employee user cannot approve their own leave. A configured workflow governs that branch separately. Default employee permissions allow creating and editing requests, while submission and protected approval fields belong to designated approver and workforce roles. Record-specific access checks remain necessary.

## Compensatory leave, manual adjustment and encashment

Compensatory leave requires holiday dates and submitted attendance on every requested date, accepting present, working from home or half-day presence. A half-day attendance cannot justify a full-day compensatory claim. The new entitlement equals inclusive worked days minus one half if selected and becomes valid the day after work ends. An existing suitable allocation receives an additional ledger movement; otherwise a new allocation is created within a valid leave period. Cancellation reverses the entitlement movement and adjusts the allocation. Missing a leave period for the day after work prevents submission.

A manual adjustment adds or reduces entitlement through its own ledger source. Zero adjustments are rejected after precision rounding. A reduction cannot exceed the available balance; an addition cannot exceed the configured allocation maximum. Only one submitted adjustment per employee and allocation is permitted by the inspected duplicate rule; further changes require cancelling and amending that adjustment. Cancellation reverses the adjustment movement.

Encashable balance starts from allocation totals minus already-carried-forward quantity plus signed leave-consumption movements. Non-encashable retained days, where configured, reduce the balance but not below zero; an encashment cap then limits it. A requested encashment cannot exceed the result. The per-day amount comes from the latest applicable salary assignment, falling back to the salary structure when no nonzero assignment value exists. Amount equals selected days times the positive per-day amount, otherwise zero, and a valid nonzero amount is required for submission.

Submitting encashment either creates additional salary or directly debits encashment expense and credits employee payable. It updates the allocation's encashed quantity and creates the negative leave-ledger movement. Cancellation reverses the quantity and ledger, cancels the linked additional salary where available, and reverses direct accounting when that route was selected. A balance of fourteen, retention floor four, cap eight and per-day value 120 allows at most eight days and amount 960. Encashment must not post once directly and again through ordinary salary.

## Acceptance criteria and remaining checks

The conformance suite must cover second-level clock duplicates, timestamp edits after attendance linking, midnight shifts, the twenty-four-hour buffer boundary, missing entry or exit, odd event counts, per-pair rounding, strict synchronisation cutoff, equality at attendance thresholds, half holidays, absent unmarked dates, overlapping assignments, paired half-day requests, negative leave balance, carried-balance caps and expiry, proration after joining, allocation retries, paid-payroll guards, self-approval, compensatory eligibility and both encashment payment routes. Recompute leave ledger balances and payroll-day effects independently. Static inspection supports these rules; production-level behaviour under concurrent clock ingestion, schedule expansion and leave approval remains to be executed and compared.

## Self-contained contracts and conformance

The [workforce calculations](../../schemas/mathematics/workforce-calculations.json) define named inputs, calculation order, boundary conditions and numerical examples. The [workforce acceptance cases](../../schemas/mathematics/workforce-acceptance-cases.json) define arrangements, actions, expected records, accounting consequences and rejection conditions. These files and the linked record definitions are part of this specification; no external implementation or unavailable evidence identifier is required to interpret a rule. A verification label distinguishes inspected transaction behavior from calculations exercised in isolation.

## Record contracts and ownership

| Record definition | Business identity and retained state |
| --- | --- |
| [Shift type](../../schemas/data/record-types/shift_type.json) | Nominal daily start/end, entry/exit interpretation, working-hour basis, buffers, absence/half-day thresholds, grace periods, overtime policy and processing markers |
| [Shift assignment](../../schemas/data/record-types/shift_assignment.json) | Employee, company, shift, inclusive assignment interval, active state and optional attendance location |
| [Employee checkin](../../schemas/data/record-types/employee_checkin.json) | Employee, second-resolution observation time, event type, device and geographic evidence, nominal and buffered shift timestamps, attendance link and skip/off-shift state |
| [Attendance](../../schemas/data/record-types/attendance.json) | Employee, company, date, shift, presence status, half-day remainder status, leave link, measured hours, entry/exit times, exception flags and overtime quantities |
| [Leave type](../../schemas/data/record-types/leave_type.json) | Paid, unpaid or partially paid meaning; daily-pay fraction; holiday treatment; negative balance permission; allocation, carry, expiry, waiting-period and encashment policy |
| [Leave allocation](../../schemas/data/record-types/leave_allocation.json) | Employee, type, interval, new entitlement, carried quantity, encashed quantity, expiry, policy link and submitted state |
| [Leave application](../../schemas/data/record-types/leave_application.json) | Employee, type, inclusive interval, half-day date, requested quantity, reason, approver, approval state and submitted state |
| [Leave ledger entry](../../schemas/data/record-types/leave_ledger_entry.json) | Employee, leave type, posting interval, signed quantity, originating business record, allocation/expiry/carry classification and cancellation information |

The entitlement unit is a leave day, not hours or currency. A fractional leave day can affect payment days, but conversion into money belongs to the payroll or encashment contract. A public-holiday row may carry a half-day quantity; holiday-count conventions are specific to the consuming calculation and must not be globally converted to whole days.

## Attendance duplicate and override rules

The ordinary duplicate query checks non-cancelled attendance for the same employee and date, excluding the record being changed. It includes records with an empty half-day remainder or with half-day modification disabled. When the new attendance has a shift, it rejects an existing attendance without a shift or for the same shift. When the new attendance has no shift, it checks the entire employee/date scope. Existing attendance eligible for half-day remainder modification has a separate path.

Different shifts on the same date additionally undergo time-overlap validation. A universal unique employee/date constraint would incorrectly disallow legitimate non-overlapping multiple shifts. Conversely, uniqueness only by employee/date/shift would incorrectly admit an unshifted record alongside an ordinary shifted record. The observed duplicate query requests a locking read; concurrent creation still needs a transaction-level test for empty result sets and insertion races.

An approved submitted leave covering the attendance date can overwrite the entered attendance status to on leave or half day and attach the corresponding leave application. A half-day or on-leave attendance without matching approved leave sets half-day modification off and the other-half status to absent through the warning path. Cancelling attendance clears its link from clock events, making those observations eligible for reprocessing. Cancelling a leave application also cancels its linked attendance and reverses its leave movement; these must not be treated as unrelated cosmetic status changes.

## Working-hour examples and edge interpretation

| Chronological events | Interpretation | Working hours |
| --- | --- | ---: |
| 08:00 entry, 12:00 exit, 13:00 entry, 17:00 exit | First entry to final exit | 9.00 |
| Same events | Sum valid pairs | 8.00 |
| 08:00, 12:00, 13:00 with alternating types | Sum consecutive pairs | 4.00; final observation contributes no interval |
| 08:00 entry, 08:05 entry, 12:00 exit | Strict pairs | 4.00; repeated entry does not replace the pending entry |
| 22:00 entry, next-day 06:00 exit | First entry to final exit | 8.00; date boundary is included |

Strict first-entry/final-exit calculation finds those two event types independently. A final exit that occurs before the first entry can therefore yield negative elapsed hours in malformed input; the isolated arithmetic does not clamp that interval to zero. A missing first entry or final exit yields zero. Alternating calculation assumes at least one observation; callers must not invoke it on an empty group. Stored earliest/latest times used for late or early flags can differ from the last consumed pair when alternating pair mode has an unmatched final observation. Verify both hours and flags, not only hours.

Two intervals of fourteen seconds each round individually to 0.00 hour and total 0.00 hour. Combining their twenty-eight seconds first would round to 0.01 hour. Preserve the individual-interval operation; rounding once at the end is not equivalent for arbitrary short observations. Half ties also require the specified rounding policy and numeric representation to be held constant.

## Processing, access and failure contract

Automatic attendance processes only completed shift evidence behind the strict synchronization watermark. It groups night shifts by the nominal starting date, calculates measured presence, links all contributing clock events and then marks missing attendance through a separate employee-batch phase. If an attendance group fails validation, its group transaction is rolled back and the observations are marked to skip automatic attendance with an error explanation. Recovery requires correcting the cause and deliberately restoring processing eligibility; blindly rerunning the scheduler does not guarantee that a skipped group will succeed.

A shift assignment cannot be cancelled while matching clock observations or attendance exist in its interval. An open-ended assignment requires testing that the reference query correctly includes all affected future observations. A leave approver needs access to the specific request, permission to change protected approval fields and authority to submit. An employee's ability to create a request does not grant those capabilities. When a configured workflow replaces default self-approval checking, that workflow must enforce its intended separation of duties.

A replacement must coordinate approval, leave-ledger movement and attendance changes so a failed operation does not consume entitlement without recording the approved absence. This is an acceptance requirement on transaction behavior. Simultaneous leave requests, manual attendance correction during payroll and earned-entitlement retries require database execution before claiming concurrency equivalence.

## Leave calculation and reversal examples

For a five-calendar-day request containing one excluded full holiday and a half day on a nonholiday, consumption is 5 minus 1 minus 0.5, or 3.5 days. If the selected half-day date is the excluded holiday, the separate half-day subtraction does not apply, and consumption is 4.0 days. A single nonholiday request is valid if other policy gates pass, although a one-day allocation interval is rejected by the separate allocation rule.

Suppose an allocation grants 20 days, approved consumption is 6 and encashment is 3. Its remaining entitlement is 11 before expiry or carry adjustments. Cancelling the 3-day encashment restores those 3 days and reverses its payout route; cancelling the 6-day leave restores 6 days and cancels linked attendance. Reversals retain their distinct originating records. Carry-forward first expires the transferable unused balance in the earlier period and records the admitted quantity in the new period; cancelling one side must not leave both periods spendable for the same quantity.
