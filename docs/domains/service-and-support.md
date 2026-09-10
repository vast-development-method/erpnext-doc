# Service and support

The domain uses [issue records](../../schemas/data/record-types/issue.json), [issue response agreements](../../schemas/data/record-types/service_level_agreement.json), [conversation response agreements](../../schemas/data/record-types/customer_relationship_service_level_agreement.json), [maintenance schedules](../../schemas/data/record-types/maintenance_schedule.json), [maintenance visits](../../schemas/data/record-types/maintenance_visit.json) and [warranty cases](../../schemas/data/record-types/warranty_claim.json). Their calculations and worked acceptance inputs are in [customer and service calculations](../../schemas/mathematics/customer-and-service-calculations.json) and [customer and service acceptance cases](../../schemas/mathematics/customer-and-service-acceptance-cases.json).

## Service records and identity

A support issue preserves subject, description, reporting person, customer, contact, lead, company, priority, state, assignments, communication timeline, response policy, and measured response and resolution dates. On customer-portal creation, record an incoming communication using the issue's subject, description, and reporter. Resolve the reporter's electronic mail to a lead, or to a contact and its customer association. Company may be derived from the lead or configured company default. An issue is not an invoice and recording a reply does not post accounting entries.

Portal listing has two relevant scopes. An authenticated website user linked through a contact to a customer sees that customer's issues. Otherwise the listing is restricted to issues raised by the user. Individual website permission also allows the reporter or customer-based access. Staff status changes require write permission. Automatically close replied issues whose modification timestamp is older than the configured number of days; zero disables that automatic closure.

## Preserve two kinds of response promise

The combined service domain needs both a customer-conversation response policy and an issue-resolution policy. The former measures first and rolling replies on leads or opportunities; the latter measures first response, resolution, holds, reopening, and fulfilment on issues or other eligible business documents. These are not redundant tables with different labels. They have different clocks and state transitions, which must remain explicit within a shared calendar and policy model.

A conversation policy is eligible when enabled for the record kind, within its optional effective dates, compatible with the communication priority, and its condition evaluates true. A policy can declare a default and there is validation against multiple defaults for the same record kind. The defined selection query retrieves name and condition but does not project the default marker used by its later attempt to put the default last. Consequently, deterministic default-last selection is not established by that routine alone and needs an acceptance decision when multiple policies match.

Issue-resolution selection is controlled by a support tracking setting. It filters enabled policies by record kind and priority, and can match a specified policy, customer, ancestor customer group, ancestor territory, or policies without a party restriction. Nondefault matching policies are condition-filtered, then defaults are appended. The first candidate wins. Preserve policy precedence explicitly; unspecified retrieval order is insufficient as a language-neutral promise where two candidates are equally eligible.

## Business calendar mathematics

Represent weekly service availability as a mapping from weekday to one start/end interval, plus an explicit holiday-date set. Service windows include their start and exclude their end. For a conversation policy, elapsed response seconds are the number of one-second steps in the interval from beginning inclusive to ending exclusive that fall on a configured weekday, are not holidays, and are inside its service window. The elapsed-time rule counts one-second steps; replacing it with an interval intersection algorithm is acceptable only when the same rounding and boundary results are obtained.

To calculate a deadline from a positive duration, walk forward through service days. On an eligible day, begin at the later of current time and window opening. Consume the lesser of remaining target seconds and available seconds before window close. If the day has no remaining capacity, advance to the next day. Skip holidays and unconfigured weekdays. The stored target is a timestamp, not merely an integer number of days. A zero duration in the conversation calculator returns its starting timestamp without advancing.

Example: service hours Monday through Friday 09:00–17:00, with Monday a holiday. A two-hour target starting Friday 16:30 yields Tuesday 10:30. Elapsed service time from Friday 16:30 to Tuesday 10:00 is 90 minutes. An answer at the exact deadline fulfils the promise; an answer after it fails. An empty working calendar with a positive target requires a guarded configuration rejection in a replacement; the defined loops do not establish a safe terminating result for that configuration. Such rejection is a proposed robustness requirement, not a claimed current result.

## Conversation first and rolling response

A conversation clock origin is set once when absent. A change in communication state away from its default waiting state records the first response if it has not already been recorded. The first response duration is calculated only when absent, preserving an actual zero duration distinctly from no value. It also seeds the last response measurements.

When rolling responses are enabled, the first recorded response is appended to the response history with fulfilled or failed result. Subsequent nonwaiting communication-state changes record elapsed service time since the previous response, a new timestamp, and the result relative to the deadline. Returning to the waiting state calculates another target beginning at the current time. The history's elapsed interval and the new waiting interval are therefore related but not interchangeable measurements.

First-response status is fulfilled unless no response makes it first response due or lateness makes it failed. With rolling history, rolling status takes precedence: waiting makes it rolling response due, and lateness makes it failed. A missing rolling deadline does not fail the promise. The response deadline compares strictly earlier than actual response or current time, so equality is not late.

## Issue response, holds, resolution, and reopening

The issue policy partitions its configured labels into open, hold, and fulfilled states. Every other label is treated as open by the defined transition logic. Moving from open to a nonopen state, or processing the first reply event, records the first response when absent. Late first replies also record the assigned users responsible at that time.

| Transition | Required state effects |
| --- | --- |
| Open to hold | Record hold beginning; reset unresolved target timestamps as applicable |
| Hold to open | Add elapsed wall-clock hold seconds; clear hold beginning and resolution measurements |
| Open to fulfilled | Record resolution timestamp and calculate resolution measurements |
| Fulfilled to open | Treat elapsed time since resolution as hold time; clear resolution measurements |
| Fulfilled to hold | Accumulate time since resolution, begin another hold, reset outstanding targets |
| Hold to fulfilled | Accumulate hold duration; when resolution tracking applies, record resolution and measurements |

Response and resolution targets first use the working calendar. Accumulated hold duration is rounded to seconds and added to the target as wall-clock elapsed time. It is not consumed through the working calendar again. A replacement that adds only working hold hours would make different deadline decisions. First-response targets include hold only while first response remains absent; resolution targets include total hold time whenever present.

Resolution time is wall-clock seconds from the policy clock origin, or creation, to resolution. User resolution time subtracts selected communication waiting gaps: a received communication immediately following a sent communication contributes its positive elapsed gap. This measure is not the same as working-calendar elapsed time and is not simply resolution time minus the hold counter. Only positive gaps contribute. Because communications are sorted by creation, the first-entry comparison against the final array entry cannot contribute a positive gap in an ordinarily ordered stream. Equal timestamps likewise contribute no wait time.

When resolution tracking is enabled, agreement status is first response due until a response exists, then resolution due until resolved, then fulfilled when resolution is on or before its target, otherwise failed. In the response-only case, fulfilment compares first-response time to response deadline. This state computation does not itself mark every unresolved overdue issue failed; periodic evaluation and displayed overdue indicators must be tested separately.

The issue first-response helper has additional observable exceptions. It returns one second in several cases where no working time elapsed so that zero is not mistaken for an unset metric. Its same-day branch compares day-of-month components, rather than complete dates. Its reviewed support-hour calculation is not the same routine as the conversation calendar calculation. Keep these exceptions in compatibility evidence; using one mathematically cleaner calendar calculation everywhere is a proposed correction requiring explicit approval, not an evidence-backed equivalence claim.

The issue-policy clock uses the record owner's timezone when available, otherwise the system timezone. It converts the current universal timestamp to that zone and then removes timezone metadata. An invalid configured zone falls back to the universal timestamp. A replacement must preserve the chosen local-clock basis while making ambiguous or repeated local times explicit in its acceptance fixtures; it must not mix timezone-aware instants and unlabelled local timestamps without a conversion rule.

An authorised policy reset is controlled by a setting, stores an explanatory comment including the supplied reason and user, updates the clock origin, and saves the document. Incoming replies and outgoing first responses trigger the same status-transition and target-calculation machinery. A reset must remain auditable because it changes service performance evidence.

## Split conversation contract

Splitting an issue requires write access and a communication that actually appears on that issue's timeline. The timeline includes both directly referenced communications and communications attached through timeline links. Reject a communication from another issue before creating anything. Create the new issue with the requested subject, reference to the original issue, reset first-response values, new creation time, and reset applicable service measurements.

Move communications from the selected communication date onward, using communication date rather than ingestion or creation time. For direct references, move the issue reference. For timeline-only associations, move only the issue's timeline link while preserving the communication's unrelated primary reference. Equal communication dates are included. Record an informational link back to the original issue. This distinction matters for late-arriving electronic mail: chronological conversation order must not be substituted with arrival order.

## Scheduled maintenance and visits

A maintenance schedule has customer, company, item rows, coverage date intervals, periodicity, number of visits, assigned salesperson, serial identity, and generated visit details. Generation is available while draft, replaces the generated schedule collection, and creates pending visits. Each detail references its originating item row. Submission requires generated schedules, validates serial coverage, updates maintenance expiry on serial records, and creates private calendar events for the responsible user's account or the schedule owner.

Visit spacing divides elapsed date difference between coverage end and start by visit count, then repeatedly advances that interval. A scheduled date falling on a holiday moves backwards through holidays and is capped at the coverage end. The calendar comes from the salesperson's employee when available, otherwise the company's default holiday list. This is not calendar-month addition. The end-date adjustment helper uses 7, 30, 91, 182, and 365 days for weekly, monthly, quarterly, half-yearly, and yearly periodicity; a separate minimum-span validation uses 7, 30, 90, 180, and 365. Preserve the distinction and test it instead of silently normalising both to one table.

A maintenance visit requires purpose rows and validates referenced serial numbers. Scheduled visits must fall inside the originating item's coverage interval. Completing a visit updates the schedule detail's completion state and actual date. Cancellation restores pending and clears actual date. Service visits can also update warranty-case progress, with fully completed work closing the case and partially completed work marking it in progress. Billing for chargeable maintenance, issued parts, and asset costs must be performed through their respective financial and inventory documents.

## Acceptance boundary

Required fixtures cover exact window opening and closing, holidays, weekend rollover, daylight and timezone interpretation, zero duration, absent calendar, first and rolling reply, target equality, hold and reopen sequences, reset audit, customer portal separation, same-timestamp split boundaries, holiday-adjusted visits, periodicity constants, and visit cancellation. These include proposed acceptance fixtures and specified compatibility exceptions; the application and its service tests were not executed. Provider delivery timing, timezone conversion, and simultaneous reply races remain runtime verification obligations.

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

1. Compare the day-of-month numbers of creation and first response. Equal numbers select the same-day branch even if month or year differs.
2. In that branch, if the creation weekday is not configured, return one second. If both timestamps are inside their configured support hours, return their elapsed seconds, rounded to two decimal places. If only creation is inside, count creation time to closing. If only response is inside, count opening to response time. If neither is inside, return one second.
3. In the different-day branch, sum full configured weekday windows between the two dates, then the eligible remainder of the creation date and elapsed part of the response date. Return the result when nonzero, otherwise one second.
4. This helper's inside-window comparison includes both opening and closing. It uses weekday windows and does not consult the holiday-date list in these branches.

Consequently, an issue raised at 18:00 and answered at 19:00 on an ordinary 09:00–17:00 support day records one second, whereas the conversation helper records zero. A response exactly at closing is inside the issue metric's window. Two dates one month apart with the same day number can take the same-day branch; that case must be carried as a compatibility exception or explicitly corrected by a versioned policy decision. A unified service domain can share calendar records while retaining distinct calculation profiles.

## Hold and reopen worked sequence

Suppose the calendar-derived resolution deadline is Tuesday 10:30. An issue spends two wall-clock hours on hold, resumes, and later resolves. Its adjusted resolution deadline is Tuesday 12:30. If the same two-hour hold crosses an overnight closure, the extension remains two hours; it is not recalculated as two business hours.

Suppose an issue resolved Monday 15:00 is reopened Tuesday 10:00. The interval since resolution is nineteen wall-clock hours and joins the accumulated hold counter before the resolution fields are cleared. Its next resolution target is based on the original clock origin and total hold adjustment, not a newly created issue timestamp. Reset is a separate authorised, audited command.

An issue may be unresolved after its deadline while the agreement result remains resolution due under the direct state computation. Present an overdue indicator from the deadline comparison without falsely asserting that this state computation already changed the result to failed. Once resolution is recorded, equality with target fulfils the promise and a later timestamp fails it.

## Split, portal and communication acceptance

The split command input includes the original issue, a communication identity and the new subject. Resolve the selected communication from the original issue's direct and timeline-linked communication set. Reject a nonexistent or unrelated communication before creating the new issue. The boundary is its communication date. Move every applicable communication at or after that date, including equal-date messages, and preserve unrelated primary associations for timeline-only entries.

Example: a message received into the system on 12 September carries a communication date of 9 September. Splitting from a different message dated 10 September leaves the late-arriving 9 September message on the old issue. A second message dated exactly 10 September moves. Sorting by ingestion date would produce a different conversation and is incorrect for this command.

Customer portal access must test both list and individual records. A user linked to Customer East must not retrieve Customer West's issue by guessing its identity. A reporter without a customer association sees their own issues. Staff record-write permission still governs staff updates independently of portal visibility. A visible communication attached to multiple records must not grant permission to every unrelated record merely because one timeline is readable.

## Warranty and installation

A warranty case retains customer, company, complaint date and text, product, optional serial identity, warranty and maintenance-coverage expiry, progress, resolution details, responsible person and resolution time. Normal authenticated creation requires a customer. Closing a case fills the resolution timestamp if it is absent and the former state was not closed. Recording the case does not recognise an expense or revenue.

Cancellation is blocked while any noncancelled maintenance visit references the warranty case; the search checks the visit parent's lifecycle rather than a child row's lifecycle. Creating another maintenance visit from the warranty case is suppressed when a submitted fully completed visit already references it. When permitted, the generated visit keeps the warranty-case identity in its purpose row so that later completion updates the right case.

An installation record retains customer, company, installation date/time, optional project and delivery-linked product rows. It requires at least one row and rejects installation before the linked delivery date. A serial-tracked product requires serial identities; a nonserial product rejects them. Every serial identity must exist and, where the delivery row supplies its serial set, belong to that delivery row's set. Submission updates installed quantity and delivery installation progress; cancellation recalculates those quantities. Installation is an operational completion record, not another delivery or invoice.

## Maintenance schedule generation details

Generated maintenance rows retain their item-row reference, product, serial details, date, responsible salesperson and completion state. Regeneration while draft replaces generated rows; it must not be represented as adding another contractual visit set. Submission requires those rows and validates serial coverage. For serial-and-batch selections, maintenance expiry is updated on each selected serial record.

Each calendar event starts at 10:00 on its scheduled date and is private. The event owner is the salesperson's associated user when available, otherwise the schedule owner. The event creation selection groups scheduled rows by product within the schedule. If the same product appears in multiple schedule item rows, event multiplicity must be tested: the operation can select the same product's dates for each matching item row.

| Periodicity | Days used when deriving or adjusting coverage end | Minimum inclusive coverage days |
| --- | --- | --- |
| Weekly | 7 | 7 |
| Monthly | 30 | 30 |
| Quarterly | 91 | 90 |
| Half-yearly | 182 | 180 |
| Yearly | 365 | 365 |

Random periodicity bypasses these periodic minimum rules. Other periodicities use inclusive coverage length when comparing visit counts, but actual visit spacing uses the exclusive difference between ending and beginning dates divided by visit count. For 1 September to 1 October with three visits, the interval is ten days and nominal visits are 11 September, 21 September and 1 October.

Holiday adjustment walks backward, not forward. If 21 September is a holiday and 20 September is not, the adjusted visit is 20 September even if that is a weekend not listed as a holiday. The adjustment is bounded by the number of holiday rows and caps dates above the coverage end; it does not separately clamp a backward-adjusted date to coverage beginning. Duplicate dates and dates before coverage therefore need explicit schedule validation fixtures.

A scheduled visit can reference one schedule detail at the parent or details on its purpose rows. Validate its visit date inside the referenced item coverage. Submission records its completion status and actual date on the applicable details; cancellation restores pending and clears actual date. Warranty updates use completed versus partially completed visit status, while cancellation consults surviving related visits before recomputing case state.

## Financial boundary and operational reliability

Service response measurements, warranty registration, schedules, visits and installations do not post a receivable, payable or stock movement on their own. Chargeable labour uses a customer invoice or [time billing](projects-and-time-billing.md). Issued replacement parts use [inventory movement](inventory-and-valuation.md), and purchased services use [supplier payables](accounts-payable.md). Retain these financial document identities on the service case to explain the cost and revenue consequence without duplicating ledgers.

Acceptance must cover a reply and hold arriving concurrently, a reset attempted without authorisation, a split retried after its communications moved, duplicate maintenance event creation, and cancellation while another submitted visit remains. The rules above specify intended durable state after each command; runtime transaction ordering, provider delivery and retry outcomes remain separate verification gates.
