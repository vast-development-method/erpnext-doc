# Service and project operations

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Work tracking and time reporting

Track work items and time entries against projects. A project transfer can change a visible work key. Preserve its durable identity and former key in the transition history.

**Worked case.** A German-speaking member can complete OPS-7 and log 90 minutes of testing. The member saves the transition and an Afrikaans-speaking lead reads the project report. The report shows one completed item and exactly 90 minutes of testing. Workflow state and work-type identifiers remain stable behind translated labels.

### Additional decisions

Represent a work item with a project-scoped key, stable workflow state ID, assignee ID, optional sprint and revision. An authorized member provides the intended transition and the revision they saw. Store the accepted state change once. Treat logging time and posting a comment as separate commands. Record the instant and duration in a portable unit. Resolve a mention to an account before producing a project-scoped notification. A viewer's language must never determine the account associated with a mention.

Let a project administrator supply translations for state and work-type labels, including distinct names for custom states. Fall back to the project's original label if a translation is missing. Preserve the original language of work-item descriptions and comments and distinguish a requested translation from the author's words. Board, Gantt and report groupings all use the same underlying state key.

### Detailed workflow and cases

<a id="work-tracking-and-time-reporting-3"></a>

#### Operating rules

| Acceptance example | Expected result |
|---|---|
| A German-speaking member advances `OPS-7` to a configured completion state and records 90 minutes of testing. An Afrikaans-speaking lead opens the report. | Both users see the same completed item and the report counts exactly 90 minutes. State, work type and duration formatting follow the viewer. |
| Another teammate submits an older transition after the first change was accepted. | Return the current revision and applicable actions, without moving the item twice. The operator can reread and select an available transition. |
| A comment contains a display name shared by two users; only one account was selected and it has project access. | Preserve the comment in its original script. Deliver one notification to the selected account, using that recipient's message language. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/everest.md).

## Facility inspection measurements

Schedule a recurring inspection against a location, asset or common-area service. Record performer, supervisor, time and unit. A yes-or-no answer and a range-checked measurement use distinct result types.

**Worked case.** An inspection rule accepts temperatures from 2 through 8 °C inclusive. A German-speaking operator enters 8,1 °C and an Afrikaans-speaking supervisor reviews it. Exactly one observation of 8.1 °C is flagged as outside the range. Both reviewers see the same location, performer, time and underlying quantity.

### Additional decisions

A facilities coordinator defines a routine, frequency, location or asset, parameter set and effective revision. A scheduled occurrence identifies the task and its due period. The operator records each required observation, its unit and time. A supervisor reviews the same revision and, when needed, records the resolution of an exception. Store scheduled, performed and reviewed times separately so a dashboard can distinguish a missed check from a completed check with an out-of-range result.

Send the assigned operator the task instructions in their selected language and the supervisor the review notification in theirs. Translate the question, choice labels, exception summary and units at display. Keep asset ID, service location ID and canonical measurement independent of the captions. Preserve the language and original text of corrective notes. For missing task translations, show the approved source instruction and its language before accepting measurements.

### Detailed workflow and cases

<a id="facility-inspection-measurements-1"></a>

#### Operating rules

| Parameter | Stored value | Evaluation |
|---|---|---|
| Was the common-area light working? | Boolean plus observer and occurrence ID | An explicit negative remains a completed observation; an empty field remains missing. |
| What temperature was measured? | Decimal, unit, configured bounds and rule revision | For a policy defining an inclusive range of 2–8 °C, a result of 8.0 passes and 8.1 is flagged. The bounds and inclusivity belong to this fixture. |

| Acceptance example | Expected result |
|---|---|
| An operator using German enters `8,1` °C on the above task and an Afrikaans-speaking supervisor opens the dashboard. | Both see one out-of-range result for the same location. The stored quantity is 8.1 °C and the dashboard retains the original performer and observation time. |
| A daily task records an explicit “no”; another daily task is left unanswered. | Reports count one completed negative check and one missing check. Repeated submission of the first occurrence creates no second observation. |
| The next week's instructions change the allowed range. | A historical report evaluates the original occurrence against its original bounds and displays the language used for that occurrence. |

#### Occurrences, exceptions and the reporting denominator

| Event | Input and resulting record | Failure or correction |
|---|---|---|
| Schedule an occurrence | Bind plan revision, site time zone, scheduled local slot and target asset or common-area location. Use one occurrence ID for its original slot. | If a supervisor moves the visit, retain the original slot and record the new due time, actor and reason. A scheduler retry reuses the occurrence. |
| Record a reading | Bind occurrence ID, parameter ID and revision, performer, observation instant, original value, unit and normalized value. Record binary answers separately from an empty response. | Reject an incompatible unit. A repeated observation ID with identical input returns its saved result. Conflicting input under that ID enters review. |
| Review the result | Record the supervisor’s disposition, reason and related corrective-work or incident reference if one is authorized. | Supersede an incorrect reading with a linked correction. Preserve the first reading and its original limit decision. Acknowledging an alert leaves the measured result intact. |
| Report the shift | Count each scheduled occurrence once. Report completion separately from conformance, excused occurrences and open exceptions. | Keep both the plan revision and reporting cutoff. Late entry can change a subsequent report without changing an already issued report. |

For a specified site policy, three inspections are due by 10:00. One records 8.0 °C against an inclusive maximum of 8.0 °C; the second records 8.1 °C; the third has no observation. At the cutoff, completion is 2/3 and conformance among completed inspections is 1/2. A supervisor opens one corrective task against the second occurrence. Redelivery of its alert leaves one task, two completed inspections and one missing inspection. A rescheduled visit retains its previous due time in the history. The source profile identifies which of these reporting and recurrence decisions are independently specified.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/green_checklist.md).

## Incident investigation

A reporter attaches the initial evidence and identifies the incident. Route it to the responsible person, append investigation findings and link follow-up actions and due dates. Record notification attempts independently from report submission.

**Worked case.** A site reporter has an Afrikaans narrative, a photo and a German-speaking recipient. Submit the initial report twice with the same request ID and retry one failed notification. One report version and one photo reference exist; the notification has separate delivery attempts. The incident ID and original narrative survive notification-language changes.

### Detailed workflow and cases

<a id="incident-investigation-3"></a>

#### Operating rules

1. A reporter submits the site, occurrence time, category, original account and optional evidence. Allocate one incident ID and one initial report version. Record the submission time separately from the occurrence time.
2. A dispatcher selects an owner and escalation policy. An escalation has a due instant, intended recipient, triggering condition and incident revision. Record outbound channel, delivery attempt and outcome separately from the assignment. A failed SMS must leave the report available to the responder.
3. A responder appends immediate action. An investigator links the detailed report, findings and preventive actions. Record the actor and time for each addition. Restrict photos and narratives to authorized incident participants. A summary can identify a location and event category without exposing every attachment.
4. A reviewer closes the investigation against its action evidence. An amendment retains the submitted narrative and the revision previously sent. Compute open and resolved counts from the incident lifecycle. Delivery retries do not increase either count.

| Acceptance example | Expected result |
|---|---|
| Submit report request R17 twice with a photograph, then retry one failed delivery | One incident, one photo reference, one initial report revision, two delivery attempts for that recipient |
| Reassign before the original escalation expires | The timer checks the live assignment revision and records the obsolete escalation without notifying the prior owner |
| A viewer outside the site opens the direct evidence link | Access is denied at the file boundary even when the viewer knows the incident number |

<a id="incident-investigation-4"></a>

#### Operating rules

Capture the reporter's original words and language. Attach a reviewed translation as a separate revision with its author. Use stable category and escalation codes for routing. Resolve notice templates in each recipient’s language, then the configured site fallback, keeping the incident ID identical in email and SMS. A German responder reading an Afrikaans report sees its source language and the original text if a translation is missing. Reprinting the FIR uses the archived template and evidence revision.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/incident_management.md).

## Facility access and visitor verification

Reception creates a visit and captures a photograph under its access policy. Verification uses a challenge sent to the registered email. Issue a pass only for a successfully verified visit and retain its unique reference.

**Worked case.** Reception is registering a visitor with an Arabic name who prefers email in English. Attempt to verify an expired challenge, then successfully verify a current one and repeat pass issuance. The expired challenge issues no pass; successful verification yields one pass for the visit. The original name is retained and the pass number is identical in either direction of text.

### Detailed workflow and cases

<a id="facility-access-and-visitor-verification-3"></a>

#### Operating rules

| Business operation | Proposed records and transition |
|---|---|
| Maintain a facility asset | Give each asset a stable asset ID, facility, current location and maintenance schedule. Link a breakdown to the asset and optionally to the relevant contract and complaint. Retain the location at the time of the event when an asset is later moved. |
| Close a complaint | Record the reporter, issue description, affected facility and optional asset. A technician attaches resolution evidence and records incurred cost with currency. Apply a configured review step, stamp the closing actor and time, then enqueue the status notification. Recording the cost of a repair is separate from posting its vendor invoice. |
| Verify a visit | Reception creates a visit and captures the visitor’s original name and photo. Link a short-lived verification challenge to that visit and email. After valid verification, issue a pass for the named site, visit and validity interval. Separate the pass identifier from the verification secret. |
| Report across modules | Count breakdowns by asset, complaints by status and passes by visit. A repair complaint linked to a breakdown is one complaint plus one breakdown. Joining multiple attachments must not inflate either count. |

<a id="facility-access-and-visitor-verification-4"></a>

#### Acceptance cases

- A visitor supplies an Arabic name and prefers English email at a German-speaking facility. Send the appropriate template, preserve the name on the pass and isolate the pass number for legible mixed-direction printing. An expired challenge yields no pass; successful verification and a retry create only one.
- A technician records the original Afrikaans complaint and a German resolution note. Each carries its own language tag. Closure emails can localize status, amount and date while linking to the original evidence under the same permissions. Do not overwrite what either person wrote.
- A facility manager opens an asset’s breakdown history after a transfer. The historical facility remains the one recorded at the breakdown, even if a translation of either location’s display name changes.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/kf_city_2.md).

## Asset and service ticket resolution

A ticket can concern a general service or a specific asset. Record status changes, assignment and notifications. A turnaround report identifies whether it uses first resolution or final resolution following reopening.

**Worked case.** A general ticket opens at 08:00 UTC and first resolves at 09:30 UTC under an elapsed-time policy. Reopen at 10:00 UTC and finally resolve at 11:00 UTC on the same day. The first-resolution measure is 90 minutes and the opening-to-final-resolution measure is 180 minutes. Both interface languages show the same durations, states and ticket ID.

### Additional decisions

The intake command requires a facility, requester, original description and complaint kind. For an asset complaint, require an asset visible at the site. A general complaint may omit it. Issue one ticket ID and an opened timestamp. Each update appends actor, time, optional evidence and transition to a versioned history. Distinguish ticket resolution from delivery of the notification, so a mail failure does not reopen a resolved ticket.

### Detailed workflow and cases

<a id="asset-and-service-ticket-resolution-4"></a>

#### Acceptance cases

| Example | Expected result |
|---|---|
| An English-speaking requester opens a general ticket at 08:00 UTC. A German-speaking agent resolves it at 09:30 UTC under the elapsed-clock policy. | First-resolution time is 90 minutes. Both views refer to the same ticket and workflow state, and the requester receives the English resolution notice. |
| The same ticket reopens at 10:00 UTC and reaches final resolution at 11:00 UTC | First resolution stays 90 minutes. The separately defined elapsed opening-to-final measure is 180 minutes. The report displays which measure was selected. |
| An asset complaint refers to an asset outside the requester’s facility | Reject that association without exposing asset details. A general complaint can still be submitted independently. |
| A German agent includes an Afrikaans note in the resolution | Preserve its original text and any language-tagged translation; use a stable status code for analytics. Format displayed time in each recipient’s zone with the zone visible. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/kf_shell.md).

## Rent collection and reminders

A collection view joins active leases to their invoices and posted payment allocations. Validate the tenant contact before preparing the reminder. Handing the text to a messaging channel neither allocates a receipt nor establishes delivery.

**Worked case.** A lease has one rent invoice for 900 and a posted allocation of 350. A German-speaking operator prepares an Afrikaans reminder for the tenant. The tenant sees 550 outstanding; opening the chat link records a handoff and creates no payment. The operator language and tenant template language preserve invoice identity and allocation.

### Additional decisions

Use separate immutable keys for property, unit, tenant, lease, charge period, invoice and allocation. Generate rent for an active lease by charge period and retain the invoice reference on rerun. Compute unpaid amounts from invoice allocations, credit adjustments and reversals. Prevent a cash-entry shortcut from marking a rent invoice settled until the payment is posted and allocated. Separate arrears ageing from lease expiry and maintenance status. Record the operator, time, target and individual result of each bulk action.

Resolve dashboard text in the operator's language and reminders in the tenant's preferred language. Validate every required placeholder against the message template revision. Preserve tenant names, unit identifiers, dates, amounts and currency codes across renderings. A sent agreement should retain its signed language and revision. A translation of legal terms is a separately approved document version. Provide a text label for every coloured payment status.

### Detailed workflow and cases

<a id="rent-collection-and-reminders-1"></a>

#### Operating rules

| Proposed acceptance case | Expected result |
|---|---|
| A lease has one 900 invoice and a posted payment allocated for 350 in the invoice currency. A German-speaking manager prepares an Afrikaans reminder. | The outstanding amount is 550, in both views. The reminder uses the tenant's language. Opening WhatsApp records a handoff to the operator and creates no second payment or invoice. |
| Generate rent twice for the same unit, lease and period while one tenant in the bulk list has an invalid phone. | One invoice exists per eligible charge. The invalid contact receives an individual failure and no chat link. Other eligible tenants remain processable. |
| On the site-local expiry notification date, an open maintenance ticket exists for the same unit. | One expiry notice is associated with that lease and date. The ticket retains its own state and assignment. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/nexgen_pms.md).

## Board issue and checklist synchronization

Map a board card to one service issue. Map each checklist to a parent task and each checklist entry to a child task. Store remote identities independently from revisable labels. Replayed changes update the same records.

**Worked case.** A board has an issue card with an Arabic checklist containing two entries. The same board webhook is received twice and a German-speaking member opens the ERP issue. Find one issue, one parent task and two linked subtasks with their original titles. The translated interface and board-list aliases never replace remote card, list or checklist identifiers.

### Detailed workflow and cases

<a id="board-issue-and-checklist-synchronization-1"></a>

#### Operating rules

| ERP identity | Remote identity | Authority and consistency |
|---|---|---|
| Connection and local user | Authorized account and member ID | Scope the credential to the correct workspace. Store the verified member mapping after a username lookup. |
| Project board and stage | Board ID and list ID | Address stages by ID. Store their displayed names and any user-defined translation independently. Two boards may both have a list called “Done”. |
| Issue with title, due instant, assignees and stage | Card ID, due instant, member IDs and destination list ID | Persist the remote ID at creation. Validate target list ownership and membership before changing a card. |

<a id="board-issue-and-checklist-synchronization-2"></a>

#### Acceptance cases

- For a board with German “Offen” and English “Open” display aliases for the same remote list, create an Afrikaans-titled issue and move it under either interface language. One card moves to the configured list ID and its author-supplied title remains in Afrikaans.
- A French-speaking user assigns a card to a member whose name contains accents. Match the verified account ID. Keep diacritics in the displayed name and original card descriptions. Render the same due instant in the user's time zone and language.
- If a remote list was deleted and another list has since acquired the same title, leave the issue in synchronization conflict. Require an authorized user to remap the ID before retrying. A revoked token similarly stops the update without recording a successful move.
- Retry the same creation after a lost acknowledgement. Recover the prior mapping or show an unresolved creation. Do not create a second card solely because the operator changed interface language.

- Receive a card containing an Arabic checklist with two entries. Create one Issue, one group Task and two child tasks with stable remote IDs. Replaying the webhook preserves all links and original titles.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/trello.md).

## Visitor check-in and departure

Reception records visitor category, host, photograph and signature, then prints the visit pass. Locate a departure by visit identity or verified phone lookup. Record an optional hospitality rating independently from the checkout event.

**Worked case.** An Afrikaans-speaking client signs in at a German-speaking front desk and receives a pass. The client checks out by the printed pass identifier and submits the four hospitality ratings. One visit receives one departure time and four numeric ratings, and the next visitor starts at a cleared kiosk. Pass text and kiosk instructions can vary by language while the acknowledged rules revision, visit ID and rating values persist.

### Additional decisions

A front-desk session has a staff language. Each visitor can select a different language before entering details. Carry the selection into category prompts, camera instructions, privacy notices, validation, pass rules and checkout ratings. Store legal names, organization identifiers and signature evidence exactly as entered. Store the specific rules version and language shown at check-in. A new kiosk visit starts with a clean language chooser. Ensure translated category text and printed pass labels remain recognizable without badge color.

### Detailed workflow and cases

<a id="visitor-check-in-and-departure-2"></a>

#### Operating rules

Bind each capture to an expiring visitor draft. `CheckIn` requires a valid category, the associated required fields, host reference and completed captures. Return one active entry and badge identifier. `CheckOut` identifies an authorized active visit and records one departure instant. A shared mobile number can produce several matches. Require disambiguation by pass or assisted lookup without exposing other visitors' details at the kiosk. Store timestamps in a consistent time base and print in the site's configured zone.

<a id="visitor-check-in-and-departure-3"></a>

#### Acceptance cases

- An Afrikaans-speaking client checks in at a German-speaking desk. The rules and pass are rendered in Afrikaans, the stored host ID is unchanged and checkout by pass records a single departure. The four ratings preserve their numeric scale across language choices.
- A vendor leaves before signing. The idle reset clears the name, image preview, chosen language and lookup results from the shared screen. A second visitor cannot retrieve the abandoned capture. An incomplete sign-in produces no active pass.
- A receptionist reprints a previously issued pass in another language. It uses the original visitor identity and time, marks the rendering language and retains the language and rules version originally acknowledged.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/visitor_management.md).
