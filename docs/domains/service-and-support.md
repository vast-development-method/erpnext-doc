# Service and support

## Service records and identity

A support issue preserves subject, description, reporting person, customer, contact, lead, company, priority, state, assignments, communication timeline, response policy, and measured response and resolution dates. On customer-portal creation, record an incoming communication using the issue's subject, description, and reporter. Resolve the reporter's electronic mail to a lead, or to a contact and its customer association. Company may be derived from the lead or configured company default. An issue is not an invoice and recording a reply does not post accounting entries. Evidence: `source-artifact-7d1950e0dae5a31dc840 lines 65–218`.

Portal listing has two relevant scopes. An authenticated website user linked through a contact to a customer sees that customer's issues. Otherwise the listing is restricted to issues raised by the user. Individual website permission also allows the reporter or customer-based access. Staff status changes require write permission. Automatically close replied issues whose modification timestamp is older than the configured number of days; zero disables that automatic closure. Evidence: `source-artifact-7d1950e0dae5a31dc840 lines 235–309`.

## Preserve two kinds of response promise

The combined service domain needs both a customer-conversation response policy and an issue-resolution policy. The former measures first and rolling replies on leads or opportunities; the latter measures first response, resolution, holds, reopening, and fulfilment on issues or other eligible business documents. These are not redundant tables with different labels. They have different clocks and state transitions, which must remain explicit within a shared calendar and policy model.

A conversation policy is eligible when enabled for the record kind, within its optional effective dates, compatible with the communication priority, and its condition evaluates true. A policy can declare a default and there is validation against multiple defaults for the same record kind. The inspected selection query retrieves name and condition but does not project the default marker used by its later attempt to put the default last. Consequently, deterministic default-last selection is not established by that routine alone and needs an acceptance decision when multiple policies match. Evidence: `source-artifact-86d9482da27aaff26937 lines 9–60`. Evidence: `source-artifact-4490d23452ee21a5e745 lines 12–145`.

Issue-resolution selection is controlled by a support tracking setting. It filters enabled policies by record kind and priority, and can match a specified policy, customer, ancestor customer group, ancestor territory, or policies without a party restriction. Nondefault matching policies are condition-filtered, then defaults are appended. The first candidate wins. Preserve policy precedence explicitly; source retrieval order is insufficient as a language-neutral promise where two candidates are equally eligible. Evidence: `source-artifact-a18b25de73c21aa2c3e9 lines 342–403`.

## Business calendar mathematics

Represent weekly service availability as a mapping from weekday to one start/end interval, plus an explicit holiday-date set. Service windows include their start and exclude their end. For a conversation policy, elapsed response seconds are the number of one-second steps in the interval from beginning inclusive to ending exclusive that fall on a configured weekday, are not holidays, and are inside its service window. The inspected implementation counts one-second steps; replacing it with an interval intersection algorithm is acceptable only when the same rounding and boundary results are obtained.

To calculate a deadline from a positive duration, walk forward through service days. On an eligible day, begin at the later of current time and window opening. Consume the lesser of remaining target seconds and available seconds before window close. If the day has no remaining capacity, advance to the next day. Skip holidays and unconfigured weekdays. The stored target is a timestamp, not merely an integer number of days. A zero duration in the conversation calculator returns its starting timestamp without advancing. Evidence: `source-artifact-733b02ac52ccc485b539 lines 74–357`.

Example: service hours Monday through Friday 09:00–17:00, with Monday a holiday. A two-hour target starting Friday 16:30 yields Tuesday 10:30. Elapsed service time from Friday 16:30 to Tuesday 10:00 is 90 minutes. An answer at the exact deadline fulfils the promise; an answer after it fails. An empty working calendar with a positive target requires a guarded configuration rejection in a replacement; the reviewed loops do not establish a safe terminating result for that configuration. Such rejection is a proposed robustness requirement, not a claimed current result.

## Conversation first and rolling response

A conversation clock origin is set once when absent. A change in communication state away from its default waiting state records the first response if it has not already been recorded. The first response duration is calculated only when absent, preserving an actual zero duration distinctly from no value. It also seeds the last response measurements.

When rolling responses are enabled, the first recorded response is appended to the response history with fulfilled or failed result. Subsequent nonwaiting communication-state changes record elapsed service time since the previous response, a new timestamp, and the result relative to the deadline. Returning to the waiting state calculates another target beginning at the current time. The history's elapsed interval and the new waiting interval are therefore related but not interchangeable measurements.

First-response status is fulfilled unless no response makes it first response due or lateness makes it failed. With rolling history, rolling status takes precedence: waiting makes it rolling response due, and lateness makes it failed. A missing rolling deadline does not fail the promise. The response deadline compares strictly earlier than actual response or current time, so equality is not late. Evidence: `source-artifact-733b02ac52ccc485b539 lines 74–357`.

## Issue response, holds, resolution, and reopening

The issue policy partitions its configured labels into open, hold, and fulfilled states. Every other label is treated as open by the inspected transition logic. Moving from open to a nonopen state, or processing the first reply event, records the first response when absent. Late first replies also record the assigned users responsible at that time.

| Transition | Required state effects |
| --- | --- |
| Open to hold | Record hold beginning; reset unresolved target timestamps as applicable |
| Hold to open | Add elapsed wall-clock hold seconds; clear hold beginning and resolution measurements |
| Open to fulfilled | Record resolution timestamp and calculate resolution measurements |
| Fulfilled to open | Treat elapsed time since resolution as hold time; clear resolution measurements |
| Fulfilled to hold | Accumulate time since resolution, begin another hold, reset outstanding targets |
| Hold to fulfilled | Accumulate hold duration; when resolution tracking applies, record resolution and measurements |

Response and resolution targets first use the working calendar. Accumulated hold duration is rounded to seconds and added to the target as wall-clock elapsed time. It is not consumed through the working calendar again. A replacement that adds only working hold hours would make different deadline decisions. First-response targets include hold only while first response remains absent; resolution targets include total hold time whenever present. Evidence: `source-artifact-a18b25de73c21aa2c3e9 lines 503–756`. Evidence: `source-artifact-a18b25de73c21aa2c3e9 lines 786–913`.

Resolution time is wall-clock seconds from the policy clock origin, or creation, to resolution. User resolution time subtracts selected communication waiting gaps: a received communication immediately following a sent communication contributes its positive elapsed gap. This measure is not the same as working-calendar elapsed time and is not simply resolution time minus the hold counter. Only positive gaps contribute. Because communications are sorted by creation, the first-entry comparison against the final array entry cannot contribute a positive gap in an ordinarily ordered stream. Equal timestamps likewise contribute no wait time. Evidence: `source-artifact-a18b25de73c21aa2c3e9 lines 503–756`.

When resolution tracking is enabled, agreement status is first response due until a response exists, then resolution due until resolved, then fulfilled when resolution is on or before its target, otherwise failed. In the response-only case, fulfilment compares first-response time to response deadline. This state computation does not itself mark every unresolved overdue issue failed; periodic evaluation and displayed overdue indicators must be tested separately. Evidence: `source-artifact-a18b25de73c21aa2c3e9 lines 985–1011`.

The issue first-response helper has additional observable exceptions. It returns one second in several cases where no working time elapsed so that zero is not mistaken for an unset metric. Its same-day branch compares day-of-month components, rather than complete dates. Its reviewed support-hour calculation is not the same routine as the conversation calendar calculation. Keep these exceptions in compatibility evidence; using one mathematically cleaner calendar calculation everywhere is a proposed correction requiring explicit approval, not an evidence-backed equivalence claim. Evidence: `source-artifact-7d1950e0dae5a31dc840 lines 364–429`.

The issue-policy clock uses the record owner's timezone when available, otherwise the system timezone. It converts the current universal timestamp to that zone and then removes timezone metadata. An invalid configured zone falls back to the universal timestamp. A replacement must preserve the chosen local-clock basis while making ambiguous or repeated local times explicit in its acceptance fixtures; it must not mix timezone-aware instants and unlabelled local timestamps without a conversion rule. Evidence: `source-artifact-a18b25de73c21aa2c3e9 lines 1022–1047`.

An authorised policy reset is controlled by a setting, stores an explanatory comment including the supplied reason and user, updates the clock origin, and saves the document. Incoming replies and outgoing first responses trigger the same status-transition and target-calculation machinery. A reset must remain auditable because it changes service performance evidence. Evidence: `source-artifact-a18b25de73c21aa2c3e9 lines 786–913`.

## Split conversation contract

Splitting an issue requires write access and a communication that actually appears on that issue's timeline. The timeline includes both directly referenced communications and communications attached through timeline links. Reject a communication from another issue before creating anything. Create the new issue with the requested subject, reference to the original issue, reset first-response values, new creation time, and reset applicable service measurements.

Move communications from the selected communication date onward, using communication date rather than ingestion or creation time. For direct references, move the issue reference. For timeline-only associations, move only the issue's timeline link while preserving the communication's unrelated primary reference. Equal communication dates are included. Record an informational link back to the original issue. This distinction matters for late-arriving electronic mail: chronological conversation order must not be substituted with arrival order. Evidence: `source-artifact-7d1950e0dae5a31dc840 lines 65–218`.

## Scheduled maintenance and visits

A maintenance schedule has customer, company, item rows, coverage date intervals, periodicity, number of visits, assigned salesperson, serial identity, and generated visit details. Generation is available while draft, replaces the generated schedule collection, and creates pending visits. Each detail references its originating item row. Submission requires generated schedules, validates serial coverage, updates maintenance expiry on serial records, and creates private calendar events for the responsible user's account or the schedule owner.

Visit spacing divides elapsed date difference between coverage end and start by visit count, then repeatedly advances that interval. A scheduled date falling on a holiday moves backwards through holidays and is capped at the coverage end. The calendar comes from the salesperson's employee when available, otherwise the company's default holiday list. This is not calendar-month addition. The end-date adjustment helper uses 7, 30, 91, 182, and 365 days for weekly, monthly, quarterly, half-yearly, and yearly periodicity; a separate minimum-span validation uses 7, 30, 90, 180, and 365. Preserve the distinction and test it instead of silently normalising both to one table. Evidence: `source-artifact-42c1faca32e03699af0b lines 50–221`.

A maintenance visit requires purpose rows and validates referenced serial numbers. Scheduled visits must fall inside the originating item's coverage interval. Completing a visit updates the schedule detail's completion state and actual date. Cancellation restores pending and clears actual date. Service visits can also update warranty-case progress, with fully completed work closing the case and partially completed work marking it in progress. Billing for chargeable maintenance, issued parts, and asset costs must be performed through their respective financial and inventory documents. Evidence: `source-artifact-b538d90358e468d7fb8b lines 49–145`.

## Acceptance boundary

Required fixtures cover exact window opening and closing, holidays, weekend rollover, daylight and timezone interpretation, zero duration, absent calendar, first and rolling reply, target equality, hold and reopen sequences, reset audit, customer portal separation, same-timestamp split boundaries, holiday-adjusted visits, periodicity constants, and visit cancellation. These include proposed acceptance fixtures and source-observed exceptions; the application and its service tests were not executed. Provider delivery timing, timezone conversion, and simultaneous reply races remain runtime verification obligations.
