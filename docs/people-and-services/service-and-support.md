# Service and support

The domain uses issue records, issue response agreements, conversation response agreements, maintenance schedules, maintenance visits and warranty cases. Their calculations and worked acceptance inputs are in [customer and service calculations](../calculations/README.md) and [customer and service acceptance cases](../calculations/README.md).

## Service records and identity

A support issue preserves subject, description, reporting person, customer, contact, lead, company, priority, state, assignments, communication timeline, response policy, and measured response and resolution dates. On customer-portal creation, record an incoming communication using the issue's subject, description, and reporter. Resolve the reporter's electronic mail to a lead, or to a contact and its customer association. Company may be derived from the lead or configured company default. An issue is not an invoice and recording a reply does not post accounting entries.

Portal listing has two relevant scopes. An authenticated website user linked through a contact to a customer sees that customer's issues. Otherwise the listing is restricted to issues raised by the user. Individual website permission also allows the reporter or customer-based access. Staff status changes require write permission. Automatically close replied issues whose modification timestamp is older than the configured number of days; zero disables that automatic closure.

## Preserve two kinds of response promise

The combined service domain needs both a customer-conversation response policy and an issue-resolution policy. The former measures first and rolling replies on leads or opportunities; the latter measures first response, resolution, holds, reopening, and fulfilment on issues or other eligible business documents. These are not redundant tables with different labels. They have different clocks and state transitions, which must remain explicit within a shared calendar and policy model.

A lead or opportunity keeps an already assigned conversation agreement. To assign one, select enabled agreements for that record kind with open or inclusive effective bounds against the evaluation time. A supplied communication priority must match a child priority row. Evaluate candidates in retrieval order. The first unconditioned candidate or candidate whose condition evaluates true wins. Saving a second default for the same record kind is rejected, including when the existing default is disabled. The lookup projects only the identifier and condition, and requests no sort order. Its attempted default-last step cannot see the default flag. Two overlapping eligible policies can therefore return different winners as retrieval order changes. For a predictable promise, set mutually exclusive conditions or explicitly select the intended agreement. With no match, an unassigned lead clears its first-response timestamp and duration.

For an issue, the tracking switch must be enabled. Filter agreements by enabled state, document kind, optional priority and inclusive business dates. A nondefault also needs an eligible entity and a satisfied condition. Rank these candidates by customer, customer group and its ancestors, territory and its ancestors, then unrestricted agreements. Append date-eligible defaults. Default selection uses the kind and priority filters without applying the nondefault entity and condition tests. An agreement already on the issue wins whenever it is still in this candidate list. Otherwise select the first candidate. For example, a still-applicable group agreement remains on an issue after a customer-specific agreement becomes eligible. A new issue for that customer takes the specific agreement. The ranking supplies no tie-break beyond retrieved order for candidates at equal specificity. If no agreement applies on reevaluation, clear the agreement, deadlines and performance state. A resolved document retains its outcome when it remains in a fulfilled status and its priority, agreement and clock origin have not changed.

## Business calendar mathematics

Represent weekly service availability as a mapping from weekday to one start/end interval, plus an explicit holiday-date set. Service windows include their start and exclude their end. For a conversation policy, elapsed response seconds are the number of one-second steps in the interval from beginning inclusive to ending exclusive that fall on a configured weekday, are not holidays, and are inside its service window. The elapsed-time rule counts one-second steps; replacing it with an interval intersection algorithm is acceptable only when the same rounding and boundary results are obtained.

To calculate a deadline from a positive duration, walk forward through service days. On an eligible day, begin at the later of current time and window opening. Consume the lesser of remaining target seconds and available seconds before window close. If the day has no remaining capacity, advance to the next day. Skip holidays and unconfigured weekdays. The stored target is a timestamp, not merely an integer number of days. A zero duration in the conversation calculator returns its starting timestamp without advancing.

For example, service hours Monday through Friday 09:00–17:00, with Monday a holiday. A two-hour target starting Friday 16:30 yields Tuesday 10:30. Elapsed service time from Friday 16:30 to Tuesday 10:00 is 90 minutes. An answer at the exact deadline fulfils the promise; an answer after it fails. An empty working calendar with a positive target requires a guarded configuration rejection in a replacement; the defined loops do not establish a safe terminating result for that configuration. Such rejection is a proposed robustness requirement, not a claimed current result.

## Conversation first and rolling response

A conversation clock origin is set once when absent. A change in communication state away from its default waiting state records the first response if it has not already been recorded. The first response duration is calculated only when absent, preserving an actual zero duration distinctly from no value. It also seeds the last response measurements.

When rolling responses are enabled, the first recorded response is appended to the response history with fulfilled or failed result. Subsequent nonwaiting communication-state changes record elapsed service time since the previous response, a new timestamp, and the result relative to the deadline. Returning to the waiting state calculates another target beginning at the current time. The history's elapsed interval and the new waiting interval are therefore related but not interchangeable measurements.

First-response status is fulfilled unless no response makes it first response due or lateness makes it failed. With rolling history, rolling status takes precedence: waiting makes it rolling response due, and lateness makes it failed. A missing rolling deadline does not fail the promise. The response deadline compares strictly earlier than actual response or current time, so equality is not late.

## Issue response, holds, resolution, and reopening

The issue policy partitions its configured labels into open, hold, and fulfilled states. Every other label is treated as open by the defined transition logic. Moving from open to a nonopen state, or processing the first reply event, records the first response when absent. Late first replies also record the assigned users responsible at that time.

| Transition | Required state effects |
| --- | --- |
| Open to hold | Record the hold beginning and retain the existing deadline for the pause comparison |
| Hold to open | Add elapsed wall-clock hold seconds; clear hold beginning and resolution measurements |
| Open to fulfilled | Record resolution timestamp and calculate resolution measurements |
| Fulfilled to open | Treat elapsed time since resolution as hold time; clear resolution measurements |
| Fulfilled to hold | Accumulate time since resolution, clear resolution metrics and start a new hold |
| Hold to fulfilled | Accumulate hold duration; when resolution tracking applies, record resolution and measurements |

Response and resolution targets first consume the agreement's working calendar. Keep wall-clock time on hold for audit. To move a deadline, recover working seconds by which previous holds moved the saved target and add eligible working seconds of the hold that just ended. Count its overlap with nonholiday working windows only when the hold began before the previous deadline. A given hold that starts exactly at or after the deadline earns no extension. Reconstruct prior extensions using the previous agreement's calendar when available. Add the resulting working seconds through the current calendar. Once first response has been recorded, ending a hold adds no new time to that response deadline. The resolution deadline can still move.

Resolution time is wall-clock seconds from the policy clock origin, or creation, to resolution. User resolution time subtracts selected communication waiting gaps: a received communication immediately following a sent communication contributes its positive elapsed gap. This measure is not the same as working-calendar elapsed time and is not simply resolution time minus the hold counter. Only positive gaps contribute. Because communications are sorted by creation, the first-entry comparison against the final array entry cannot contribute a positive gap in an ordinarily ordered stream. Equal timestamps likewise contribute no wait time.

A missed response or applicable resolution deadline takes precedence over due and fulfilled states. Compare the deadline with the completed event time, otherwise the start of an ongoing hold, otherwise the current time. Only a strictly later value fails. With no missed deadline, a missing first response is First Response Due. Once responded, a tracked but missing resolution is Resolution Due. Otherwise the agreement is Fulfilled. An unresolved running issue whose deadline passed can therefore be Failed. A hold beginning at the deadline freezes the comparison at equality while the hold remains active.

The issue first-response metric uses complete civil dates to choose its same-day branch. It can return one second for an unworked interval to distinguish that case from an unset first-response measurement. The elapsed-response measurement and the deadline calculation have different calendar rules.

Issue transitions use the application clock in the site's timezone, or a supplied observation clock when one is set. The usual application timestamp carries local date and time with timezone information removed. A customer's display language or an assignee's personal timezone does not shift the agreement deadline. Use the same site calendar for the clock origin, staffing window and reported timestamps. Preserve explicit offsets when exchanging instants across sites.

An authorised policy reset is controlled by a setting, stores an explanatory comment including the supplied reason and user, updates the clock origin, and saves the document. Incoming replies and outgoing first responses trigger the same status-transition and target-calculation machinery. A reset must remain auditable because it changes service performance evidence.

## Split conversation contract

Splitting an issue requires write access and a communication that actually appears on that issue's timeline. The timeline includes both directly referenced communications and communications attached through timeline links. Reject a communication from another issue before creating anything. Create the new issue with the requested subject, reference to the original issue, reset first-response values, new creation time, and reset applicable service measurements.

Move communications from the selected communication date onward, using communication date rather than ingestion or creation time. For direct references, move the issue reference. For timeline-only associations, move only the issue's timeline link while preserving the communication's unrelated primary reference. Equal communication dates are included. Record an informational link back to the original issue. This distinction matters for late-arriving electronic mail: chronological conversation order must not be substituted with arrival order.

## Scheduled maintenance and visits

A maintenance schedule has customer, company, item rows, coverage date intervals, periodicity, number of visits, assigned salesperson, serial identity, and generated visit details. Generation is available while draft, replaces the generated schedule collection, and creates pending visits. Each detail references its originating item row. Submission requires generated schedules, validates serial coverage, updates maintenance expiry on serial records, and creates private calendar events for the schedule and available salesperson participants.

Visit spacing divides elapsed date difference between coverage end and start by visit count, then repeatedly advances that interval. A nominal holiday first moves backward, or forward if the backward choice crosses coverage start. The calendar comes from the salesperson's employee when available, otherwise the company's default holiday list. This is not calendar-month addition. The end-date adjustment helper uses 7, 30, 91, 182, and 365 days for weekly, monthly, quarterly, half-yearly, and yearly periodicity; a separate minimum-span validation uses 7, 30, 90, 180, and 365. Preserve the distinction and test it instead of silently normalising both to one table.

A maintenance visit requires purpose rows and validates referenced serial numbers. Any linked schedule detail enforces its originating item’s inclusive coverage dates. On submission or cancellation the detail reflects the surviving submitted work for that row. Service visits can also update warranty-case progress. Chargeable maintenance, issued parts and asset costs use their respective financial and inventory documents.

## Acceptance boundary

Required fixtures cover exact window opening and closing, holidays, weekend rollover, daylight and timezone interpretation, zero duration, absent calendar, first and rolling reply, target equality, hold and reopen sequences, reset audit, customer portal separation, same-timestamp split boundaries, holiday-adjusted visits, periodicity constants, and visit cancellation. Test actual delivery timing, time-zone conversion and simultaneous replies separately.

## Policy records and event measurements

| Record | Persisted values and meaning |
| --- | --- |
| Response policy | Full name, enabled marker, applicable record kind, optional effective dates, condition, default marker, optional party scope, priority rows and calendar |
| Priority row | Priority identity, first-response target duration, optional resolution target duration and default selection |
| Calendar window | Weekday, opening local time and closing local time; holiday exceptions use full local dates |
| Conversation measurement | Policy identity, clock origin, communication state, first deadline and reply timestamp/duration, last reply timestamp/duration and rolling history |
| Issue measurement | Policy identity, clock origin, first response, first-response target, resolution target, hold beginning, accumulated hold seconds, resolution timestamp and agreement result |
| Communication | Sender, recipients, direction, communication date, ingestion/creation date, subject/content, primary record association and additional timeline links |
| Policy reset audit | Acting user, supplied reason, reset time and explanatory record comment |

Absent timestamps and durations are not equivalent to zero. An immediate valid reply can consume zero service seconds in a conversation. Replacing that zero with an absent value would repeatedly record the first response. The issue-specific helper has the separate one-second exceptions below and must not be substituted for the conversation helper.

## Precise calendar algorithm

For a chosen local date, define available service as the interval from opening inclusive to closing exclusive, unless the date is a holiday or the weekday has no window. Intersect the requested elapsed interval with every available interval and sum the durations. When timestamps contain fractional seconds, the conversation behavior counts one-second steps from its initial timestamp; an optimised intersection calculation must match that step alignment rather than simply round arbitrary endpoints independently.

A positive-duration deadline consumes service capacity from the clock origin forward, including the opening instant. If the origin is before opening, move to opening; if it is at or after closing, continue with the next eligible date. Consuming exactly the remaining day's capacity returns that closing timestamp. This does not make closing a service second: it is the endpoint reached after consuming the preceding service seconds.

With a 09:00–17:00 window, a one-hour target starting at 16:00 ends at 17:00. A reply at 17:00 meets that deadline. A new one-hour target beginning at 17:00 consumes the next eligible day's 09:00–10:00 interval. With holidays on Monday and Tuesday, that new target skips both dates; it does not add two arbitrary multiples of twenty-four hours to a target already calculated for another calendar.

Validate the calendar's usable positive capacity before promising finite completion. A missing calendar, inverted interval, unreachable future service date or impossible duration needs a named configuration error in a replacement. This is a required robustness addition, because the compatibility behavior does not supply a reliable terminating result for every malformed calendar.

## Issue first-response compatibility calculation

The issue first-response metric is deliberately specified independently from deadline arithmetic:

1. Compare the full local calendar dates of the agreement clock origin and first response. The origin falls back to issue creation when no agreement clock origin is recorded. Identical day numbers in different months take the multi-day branch.
2. In that branch, if the creation weekday is not configured, return one second. If both timestamps are inside their configured support hours, return their elapsed seconds, rounded to two decimal places. If only creation is inside, count creation time to closing. If only response is inside, count opening to response time. If neither is inside, return one second.
3. In the different-day branch, sum full configured weekday windows between the two dates, then the eligible remainder of the creation date and elapsed part of the response date. Return the result when nonzero, otherwise one second.
4. This helper's inside-window comparison includes both opening and closing. It uses weekday windows and does not consult the holiday-date list in these branches.

An issue raised at 18:00 and answered at 19:00 on the same ordinary 09:00–17:00 support day records one second. The conversation helper records zero for that interval. An issue response exactly at closing is inside the issue metric's window. From 10 September to 10 October the calculation includes qualifying intervening dates even though both dates have day number ten.

## Hold and reopen worked sequence

With weekday hours 09:00–17:00 and a base resolution deadline Tuesday 10:30, a hold on Monday from 14:00 to 16:00 records 7,200 elapsed and 7,200 working seconds. The adjusted deadline is Tuesday 12:30. A hold Monday 16:30 through Tuesday 09:30 records 17 wall-clock hours and one working hour. It moves the deadline to Tuesday 11:30 if it began before the original deadline.

An issue resolved Monday 15:00 and reopened Tuesday 10:00 accumulates nineteen hours in the hold counter. In this same calendar, three hours were working time. If the resolution began before the prior deadline, three hours are available to move the target. Clear the resolution fields on reopening, keep the original clock origin, and preserve earlier earned extensions. Reset is a separate authorised, audited command.

If an unresolved issue remains open after Tuesday 10:30 with no intervening eligible hold, its deadline comparison fails. If the issue instead entered hold at 10:30, the paused comparison is on time. On resumption a hold that began at the deadline earns zero extension, and the then-current time determines any missed deadline.

## Split, portal and communication acceptance

The split command input includes the original issue, a communication identity and the new subject. Resolve the selected communication from the original issue's direct and timeline-linked communication set. Reject a nonexistent or unrelated communication before creating the new issue. The boundary is its communication date. Move every applicable communication at or after that date, including equal-date messages, and preserve unrelated primary associations for timeline-only entries.

For example, a message received into the system on 12 June carries a communication date of 9 June. Splitting from a different message dated 10 June leaves the late-arriving 9 June message on the old issue. A second message dated exactly 10 June moves. Sorting by ingestion date would produce a different conversation and is incorrect for this command.

Customer portal access must test both list and individual records. A user linked to Customer East must not retrieve Customer West's issue by guessing its identity. A reporter without a customer association sees their own issues. Staff record-write permission still governs staff updates independently of portal visibility. A visible communication attached to multiple records must not grant permission to every unrelated record merely because one timeline is readable.

## Warranty and installation

A warranty case retains customer, company, complaint date and text, product, optional serial identity, warranty and maintenance-coverage expiry, progress, resolution details, responsible person and resolution time. Normal authenticated creation requires a customer. Closing a case fills the resolution timestamp if it is absent and the former state was not closed. Recording the case does not recognise an expense or revenue.

Cancellation is blocked while any noncancelled maintenance visit references the warranty case; the search checks the visit parent's lifecycle rather than a child row's lifecycle. Creating another maintenance visit from the warranty case is suppressed when a submitted fully completed visit already references it. When permitted, the generated visit keeps the warranty-case identity in its purpose row so that later completion updates the right case.

An installation record retains customer, company, installation date/time, optional project and delivery-linked product rows. It requires at least one row and rejects installation before the linked delivery date. A serial-tracked product requires serial identities; a nonserial product rejects them. Every serial identity must exist and, where the delivery row supplies its serial set, belong to that delivery row's set. Submission updates installed quantity and delivery installation progress; cancellation recalculates those quantities. Installation is an operational completion record, not another delivery or invoice.

## Maintenance schedule generation details

Generated maintenance rows retain their item-row reference, product, serial details, date, responsible salesperson and completion state. Regeneration while draft replaces generated rows; it must not be represented as adding another contractual visit set. Submission requires those rows and validates serial coverage. For serial-and-batch selections, maintenance expiry is updated on each selected serial record.

Each calendar event starts at 10:00, is private and references its schedule. Each item obtains only the dates whose detail references that exact item row. Identical product codes across different item rows do not combine their dates. If the salesperson resolves to an email identity, include them as a participant. The event insert does not assign its owner to the salesperson. Cancelling a schedule deletes its events and restores each affected serial’s latest remaining coverage end across other submitted schedules for that product, or clears it if none survives.

| Periodicity | Days used when deriving or adjusting coverage end | Minimum inclusive coverage days |
| --- | --- | --- |
| Weekly | 7 | 7 |
| Monthly | 30 | 30 |
| Quarterly | 91 | 90 |
| Half-yearly | 182 | 180 |
| Yearly | 365 | 365 |

Random periodicity bypasses these periodic minimum rules. Other periodicities use inclusive coverage length when comparing visit counts, but actual visit spacing uses the exclusive difference between ending and beginning dates divided by visit count. For 1 June to 1 July with three visits, the interval is ten days and nominal visits are 11 June, 21 June and 1 July.

For a holiday, walk back to the nearest nonholiday. If this crosses the coverage start, resume at the nominal date and walk forward to the nearest nonholiday. Reject an adjusted date beyond the coverage end. A nominal date that overshoots the end without holiday adjustment is capped at the end. With a nominal 21 June holiday and a working 20 June inside coverage, choose 20 June. With coverage beginning on the 21st, choose the first subsequent nonholiday within coverage.

A header-level schedule detail takes precedence over purpose-row references. Any linked detail enforces inclusive coverage dates when its source item is present, regardless of visit type. For each affected schedule row on submit or cancel, lock surviving submitted visit rows ordered by visit date then creation, newest first. Prefer the newest fully completed visit, otherwise the newest surviving visit. Store its completion status and actual date. With no surviving visit store Pending and clear the actual date. For example, cancelling a 20 June visit leaves the earlier fully completed visit’s 12 June as the actual date, even if a partially completed visit occurred on 18 June.

For a warranty-linked purpose on a visit without a maintenance schedule, a fully completed visit closes the claim and a partially completed visit puts it in work. A nonfinal visit leaves the claim untouched if another submitted fully completed visit supersedes it. On cancellation select the first other submitted visit for the referenced identity in descending visit-name order. Restore its mapped status, visit date, responsible user and work details. With no match, reopen and clear those details.

## Financial boundary and operational reliability

Service response measurements, warranty registration, schedules, visits and installations do not post a receivable, payable or stock movement on their own. Chargeable labour uses a customer invoice or [time billing](projects-and-time-billing.md). Issued replacement parts use [inventory movement](../operations/README.md), and purchased services use [supplier payables](../transactions/README.md). Retain these financial document identities on the service case to explain the cost and revenue consequence without duplicating ledgers.

Acceptance must cover a reply and hold arriving concurrently, a reset attempted without authorisation, a split retried after its communications moved, duplicate maintenance event creation, and cancellation while another submitted visit remains. Assess the persisted effects after both concurrent operations and verify service communications against actual delivery receipts.

## Linked specifications

- **Record definitions** · [issue records](../../schemas/data/record-types/issue.json) · [issue response agreements](../../schemas/data/record-types/service_level_agreement.json) · [conversation response agreements](../../schemas/data/record-types/customer_relationship_service_level_agreement.json) · [maintenance schedules](../../schemas/data/record-types/maintenance_schedule.json) · [maintenance visits](../../schemas/data/record-types/maintenance_visit.json) · [warranty cases](../../schemas/data/record-types/warranty_claim.json)
- **Calculation and acceptance cases** · [customer and service calculations](../../schemas/mathematics/customer-and-service-calculations.json) · [customer and service acceptance cases](../../schemas/mathematics/customer-and-service-acceptance-cases.json)
- **Related decisions** · [inventory movement](../operations/inventory-and-valuation.md) · [supplier payables](../transactions/accounts-payable.md)
