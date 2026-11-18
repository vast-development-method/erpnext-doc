# Document Progress Tracker

[Business workflow and acceptance cases](../../../capabilities/guides/documents.md#milestone-progress-measurement).

Apoorv Soral lists version 15. A process owner selects a document type and defines milestone conditions and percentages. When a condition is met the app records a Document Progress Log and updates a progress field on the document. A report shows time spent moving between milestones. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/document_progress_tracker)

## Evidence from the publisher’s screens

The tracker setup screen shows the target document type, a tracker **date field**, a disabled flag and a table of milestones, conditions and percentages. It names the target progress field and says a custom field can be created when missing. A Sales Order example assigns percentages 10, 50, 30 and 10 to four conditions: a rebuild must establish whether values are increments, weights or absolute progress before comparing the resulting total to the vendor’s system. [Configuration screen](https://cloud.frappe.io/files/Screenshot%202024-07-19%20114659.webp)

A log displays the document, tracker, milestone, user, document date, milestone date/time, progress, and age in minutes and days. One captured Ticket log shows 423 minutes and 0.29375 days. The aging report shows current progress and average milestone age at the grouped level and the event-level progress and timestamps in detail. [Log example](https://cloud.frappe.io/files/Screenshot%202024-07-19%20114749.webp) · [Aging report](https://cloud.frappe.io/files/Screenshot%202024-07-19%20114856.webp)

## Proposed rebuild contract and acceptance

Exact rule evaluation order, overlapping conditions and field ownership after disabling a tracker remain to be established against a running build. [Publisher-named repository](https://github.com/asoral/document-progress-tracker)

[Read the consolidated acceptance cases](../../../capabilities/guides/documents.md#milestone-progress-measurement-2).
