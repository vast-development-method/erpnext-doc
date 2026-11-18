# Helpdesk Management

## Publisher evidence

Indictrans Tech lists version 13. A user can raise a general complaint or link the complaint to a particular entry in the asset register. The advertised capabilities include ticket attachments, a resolution workflow, email on updates, turnaround-time analysis, a dashboard and reports. The listing describes neither an exact state machine nor which periods contribute to turnaround. [Marketplace description](https://cloud.frappe.io/marketplace/apps/kf_shell) · [Listed repository](https://github.com/indictranstech/KF_Shell)

## Related publisher material

In a separate support-ticket product description, Indictrans lists ticket filtering, assignment, transfer, referral and service-level agreements. These are useful comparison points when specifying reassignment and timing policies. The brochure does not identify KF Shell, so it establishes neither the states in this app nor a service-level calendar for the listing. [Indictrans brochure, page 4](https://softwaresuggest-cdn.s3.amazonaws.com/brochures/1574420326_Brochure_Indictrans.pdf#page=4)

## Proposed rebuild contract

The intake command requires a facility, requester, original description and complaint kind. For an asset complaint, require an asset visible at the site. A general complaint may omit it. Issue one ticket ID and an opened timestamp. Each update appends actor, time, optional evidence and transition to a versioned history. Distinguish ticket resolution from delivery of the notification, so a mail failure does not reopen a resolved ticket.

Define the first-resolution measure as elapsed time from opening to first resolution. Define final resolution separately when tickets can reopen. For elapsed-clock policies use instants; for working-hour policies associate a named calendar, time zone and explicit pause rules. Return the metric definition and unit with every report. An auditor can reconstruct the reported duration from the same event history. The publisher's mention of TAT does not establish working hours, pause semantics or first-versus-final resolution.

## Multilingual operation and acceptance

| Example | Expected result |
|---|---|
| An English-speaking requester opens a general ticket at 08:00 UTC. A German-speaking agent resolves it at 09:30 UTC under the elapsed-clock policy. | First-resolution time is 90 minutes. Both views refer to the same ticket and workflow state, and the requester receives the English resolution notice. |
| The same ticket reopens at 10:00 UTC and reaches final resolution at 11:00 UTC | First resolution stays 90 minutes. The separately defined elapsed opening-to-final measure is 180 minutes. The report displays which measure was selected. |
| An asset complaint refers to an asset outside the requester’s facility | Reject that association without exposing asset details. A general complaint can still be submitted independently. |
| A German agent includes an Afrikaans note in the resolution | Preserve its original text and any language-tagged translation; use a stable status code for analytics. Format displayed time in each recipient’s zone with the zone visible. |

## Remaining evidence

Preserve a reference ticket, its timestamps, notifications and the vendor’s own report output to establish shipped timing rules. Asset-access scope, ticket visibility, attachment rights, translated content and notification recipient selection remain unverified.
