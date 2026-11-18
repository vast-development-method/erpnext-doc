# Service and project operations

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Work tracking and time reporting

Track work items and time entries against projects. A project transfer can change a visible work key. Preserve its durable identity and former key in the transition history.

**Worked case.** A German-speaking member can complete OPS-7 and log 90 minutes of testing. The member saves the transition and an Afrikaans-speaking lead reads the project report. The report shows one completed item and exactly 90 minutes of testing. Workflow state and work-type identifiers remain stable behind translated labels.

### Additional decisions

Represent a work item with a project-scoped key, stable workflow state ID, assignee ID, optional sprint and revision. An authorized member provides the intended transition and the revision they saw. Store the accepted state change once. Treat logging time and posting a comment as separate commands. Record the instant and duration in a portable unit. Resolve a mention to an account before producing a project-scoped notification. A viewer's language must never determine the account associated with a mention.

Let a project administrator supply translations for state and work-type labels, including distinct names for custom states. Fall back to the project's original label if a translation is missing. Preserve the original language of work-item descriptions and comments and distinguish a requested translation from the author's words. Board, Gantt and report groupings all use the same underlying state key.

## Facility inspection measurements

Schedule a recurring inspection against a location, asset or common-area service. Record performer, supervisor, time and unit. A yes-or-no answer and a range-checked measurement use distinct result types.

**Worked case.** An inspection rule accepts temperatures from 2 through 8 °C inclusive. A German-speaking operator enters 8,1 °C and an Afrikaans-speaking supervisor reviews it. Exactly one observation of 8.1 °C is flagged as outside the range. Both reviewers see the same location, performer, time and underlying quantity.

### Additional decisions

A facilities coordinator defines a routine, frequency, location or asset, parameter set and effective revision. A scheduled occurrence identifies the task and its due period. The operator records each required observation, its unit and time. A supervisor reviews the same revision and, when needed, records the resolution of an exception. Store scheduled, performed and reviewed times separately so a dashboard can distinguish a missed check from a completed check with an out-of-range result.

Send the assigned operator the task instructions in their selected language and the supervisor the review notification in theirs. Translate the question, choice labels, exception summary and units at display. Keep asset ID, service location ID and canonical measurement independent of the captions. Preserve the language and original text of corrective notes. For missing task translations, show the approved source instruction and its language before accepting measurements.

## Incident investigation

A reporter attaches the initial evidence and identifies the incident. Route it to the responsible person, append investigation findings and link follow-up actions and due dates. Record notification attempts independently from report submission.

**Worked case.** A site reporter has an Afrikaans narrative, a photo and a German-speaking recipient. Submit the initial report twice with the same request ID and retry one failed notification. One report version and one photo reference exist; the notification has separate delivery attempts. The incident ID and original narrative survive notification-language changes.

## Facility access and visitor verification

Reception creates a visit and captures a photograph under its access policy. Verification uses a challenge sent to the registered email. Issue a pass only for a successfully verified visit and retain its unique reference.

**Worked case.** Reception is registering a visitor with an Arabic name who prefers email in English. Attempt to verify an expired challenge, then successfully verify a current one and repeat pass issuance. The expired challenge issues no pass; successful verification yields one pass for the visit. The original name is retained and the pass number is identical in either direction of text.

## Asset and service ticket resolution

A ticket can concern a general service or a specific asset. Record status changes, assignment and notifications. A turnaround report identifies whether it uses first resolution or final resolution following reopening.

**Worked case.** A general ticket opens at 08:00 UTC and first resolves at 09:30 UTC under an elapsed-time policy. Reopen at 10:00 UTC and finally resolve at 11:00 UTC on the same day. The first-resolution measure is 90 minutes and the opening-to-final-resolution measure is 180 minutes. Both interface languages show the same durations, states and ticket ID.

### Additional decisions

The intake command requires a facility, requester, original description and complaint kind. For an asset complaint, require an asset visible at the site. A general complaint may omit it. Issue one ticket ID and an opened timestamp. Each update appends actor, time, optional evidence and transition to a versioned history. Distinguish ticket resolution from delivery of the notification, so a mail failure does not reopen a resolved ticket.

## Rent collection and reminders

A collection view joins active leases to their invoices and posted payment allocations. Validate the tenant contact before preparing the reminder. Handing the text to a messaging channel neither allocates a receipt nor establishes delivery.

**Worked case.** A lease has one rent invoice for 900 and a posted allocation of 350. A German-speaking operator prepares an Afrikaans reminder for the tenant. The tenant sees 550 outstanding; opening the chat link records a handoff and creates no payment. The operator language and tenant template language preserve invoice identity and allocation.

### Additional decisions

Use separate immutable keys for property, unit, tenant, lease, charge period, invoice and allocation. Generate rent for an active lease by charge period and retain the invoice reference on rerun. Compute unpaid amounts from invoice allocations, credit adjustments and reversals. Prevent a cash-entry shortcut from marking a rent invoice settled until the payment is posted and allocated. Separate arrears ageing from lease expiry and maintenance status. Record the operator, time, target and individual result of each bulk action.

Resolve dashboard text in the operator's language and reminders in the tenant's preferred language. Validate every required placeholder against the message template revision. Preserve tenant names, unit identifiers, dates, amounts and currency codes across renderings. A sent agreement should retain its signed language and revision. A translation of legal terms is a separately approved document version. Provide a text label for every coloured payment status.

## Board issue and checklist synchronization

Map a board card to one service issue. Map each checklist to a parent task and each checklist entry to a child task. Store remote identities independently from revisable labels. Replayed changes update the same records.

**Worked case.** A board has an issue card with an Arabic checklist containing two entries. The same board webhook is received twice and a German-speaking member opens the ERP issue. Find one issue, one parent task and two linked subtasks with their original titles. The translated interface and board-list aliases never replace remote card, list or checklist identifiers.

## Visitor check-in and departure

Reception records visitor category, host, photograph and signature, then prints the visit pass. Locate a departure by visit identity or verified phone lookup. Record an optional hospitality rating independently from the checkout event.

**Worked case.** An Afrikaans-speaking client signs in at a German-speaking front desk and receives a pass. The client checks out by the printed pass identifier and submits the four hospitality ratings. One visit receives one departure time and four numeric ratings, and the next visitor starts at a cleared kiosk. Pass text and kiosk instructions can vary by language while the acknowledged rules revision, visit ID and rating values persist.

### Additional decisions

A front-desk session has a staff language. Each visitor can select a different language before entering details. Carry the selection into category prompts, camera instructions, privacy notices, validation, pass rules and checkout ratings. Store legal names, organization identifiers and signature evidence exactly as entered. Store the specific rules version and language shown at check-in. A new kiosk visit starts with a clean language chooser. Ensure translated category text and printed pass labels remain recognizable without badge color.
