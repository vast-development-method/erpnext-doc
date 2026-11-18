# Document Progress Tracker

Apoorv Soral lists version 15. A process owner selects a document type and defines milestone conditions and percentages. When a condition is met the app records a Document Progress Log and updates a progress field on the document. A report shows time spent moving between milestones. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/document_progress_tracker)

## Evidence from the publisher’s screens

The tracker setup screen shows the target document type, a tracker **date field**, a disabled flag and a table of milestones, conditions and percentages. It names the target progress field and says a custom field can be created when missing. A Sales Order example assigns percentages 10, 50, 30 and 10 to four conditions: a rebuild must establish whether values are increments, weights or absolute progress before comparing the resulting total to the vendor’s system. [Configuration screen](https://cloud.frappe.io/files/Screenshot%202024-07-19%20114659.webp)

A log displays the document, tracker, milestone, user, document date, milestone date/time, progress, and age in minutes and days. One captured Ticket log shows 423 minutes and 0.29375 days. The aging report shows current progress and average milestone age at the grouped level and the event-level progress and timestamps in detail. [Log example](https://cloud.frappe.io/files/Screenshot%202024-07-19%20114749.webp) · [Aging report](https://cloud.frappe.io/files/Screenshot%202024-07-19%20114856.webp)

## Proposed rebuild contract and acceptance

Version a tracker definition with a target type, effective date, source date field, destination percentage field, milestone codes and explicitly selected percentage semantics. Express trigger conditions using typed field and status IDs. On a document transition, capture the triggering revision, matched milestone, evaluation time and actor, and atomically update the projection and event history. A repeated save without a new qualifying transition cannot create another elapsed-time interval. Report the first event relative to the configured starting instant, then each event relative to the previous one. Require an explicit time zone and time-of-day policy when the start field contains a date only.

- With absolute-progress rules `approved = 40` and `delivered = 100`, a document moves from approved at 08:00 UTC to delivered at 15:03 UTC. Its latest progress is 100% and the interval is 423 minutes. Replaying the delivery event adds zero minutes and no second log.
- Two milestones are configured with overlapping conditions and equal priority. Reject the ambiguous definition, or surface a recorded conflict without silently advancing the document. A disabled tracker adds no new events.
- Allow editors to translate milestone titles and report headers. If “Approved” becomes “Goedgekeur” after the first event, a historical report must still identify the same milestone and 423-minute interval. Preserve time-zone conversion for presentation only.

Exact rule evaluation order, overlapping conditions and field ownership after disabling a tracker remain to be established against a running build. [Publisher-named repository](https://github.com/asoral/document-progress-tracker)
