# Customer communications

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Outbound calling and call dispositions

An agent calls from an assigned number on a customer or sales activity. Retrieve call details and recordings with their external identity. Link the activity, dialled number, direction, disposition and duration to a single call record for reporting.

**Worked case.** A provider has acknowledged one outbound call, and its call ID appears on two overlapping log pages. Import both pages with final disposition answered and duration 48 seconds. The report shows one answered outbound call linked to its CRM activity, with duration 48 seconds. The translated disposition retains the same provider identifier, duration and dialled number.

### Additional decisions

A call intent has a site, initiating user, permitted CRM reference, source and destination telephone numbers, timestamp and correlation ID. Track provider acknowledgement, call detail and recording availability separately. Link incoming calls to contacts using normalised telephone numbers within the appropriate site. Where a number belongs to multiple contacts, retain the call as unmatched until an authorised user chooses the record. Repeated log pages update the same provider call rather than creating additional calls. Treat separate call legs explicitly if the selected provider feed exposes them.

Persist the original disposition and map it to a stable report code. Group calls by the explicitly selected reporting time zone and reporting period. An agent can see their own activities under the chosen policy. Access to reports and to recording contents are separate permissions. Keep provider authorization material outside logs and reports.

### Detailed workflow and cases

<a id="outbound-calling-and-call-dispositions-3"></a>

#### Acceptance cases

Translate the report captions and mapped dispositions. Keep the caller’s original free-text reason, telephone numbers, recording and provider IDs intact. Support language tags on notes and transcripts when present. Changing an agent’s language cannot alter the dialling prefix or decide the report’s time zone.

- For one acknowledged outbound intent, two overlapping call-log pages return the same provider ID with a final duration of 48 seconds. The report shows one outbound answered call, one linked activity and the latest duration.
- A selected agent has no configured source telephone number. Reject the intent before contacting the provider and return a message in that agent’s language. If the provider accepted a request but the reply was lost, reconcile its identity before initiating another call.
- Two contacts share the called number. A report reader sees the unresolved activity without receiving access to either party’s recording until an authorised match is made.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/call_integration.md).

## Device notification delivery

Associate each subscribed device with its user. An eligible notification fans out to active devices. Keep the dispatch, acknowledgement and retry state per destination.

**Worked case.** One recipient has two subscribed devices with Afrikaans and German message resources. An approval notification for PO-18 is dispatched, then the acknowledged dispatch is reprocessed. Each eligible device has one logical dispatch for PO-18 and the acknowledged dispatch is not resent. The message follows the device language; the document ID stays PO-18.

### Additional decisions

The public evidence does not establish current provider compatibility, token rotation, retry behavior or translation coverage of the marketplace build.

### Detailed workflow and cases

<a id="device-notification-delivery-2"></a>

#### Operating rules

| Acceptance example | Expected result |
|---|---|
| A recipient registers two devices with Afrikaans and German interfaces for an approval event on `PO-18`. | Each active device receives its language rendering and the same document reference. Reprocessing an acknowledged dispatch creates no new delivery attempt for it. |
| A notification transaction rolls back, or a device is unsubscribed before dispatch. | The rollback produces no dispatch. The unsubscribed device is skipped without suppressing delivery to the user's other active device. |
| Access to the order is removed between push delivery and opening the app. | The app denies the document read and uses a translated, non-disclosing message. Delivery does not grant document access. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/fcm_notification.md).

## Text message acceptance and delivery

An operator sends approved text to a contact’s stored number. Preserve recipient, template language, original text, gateway acknowledgement and any later delivery receipt as separate facts.

**Worked case.** Contact C17 prefers Afrikaans and an approved Afrikaans appointment reminder exists. An English-speaking operator requests that reminder and the gateway confirms submission only. Record one submitted SMS containing the approved Afrikaans text and appointment reference, with handset delivery still unconfirmed. The contact controls the message language and the operator controls the language of the status display.

### Detailed workflow and cases

<a id="text-message-acceptance-and-delivery-1"></a>

#### Operating rules

1. A communications administrator configures a tenant-specific sender, approved destinations, provider credential reference, and the character sets and length rules verified for that account.
2. An authorized operator requests a message against a business contact. Supply the contact ID, selected verified telephone number, text or versioned template, recipient language and an operation ID. Resolve the outgoing text before enqueueing.
3. Record one dispatch with a stable identity. A worker submits the body and destination to the configured gateway. Record the provider ID on acceptance, an explicit rejection on refusal or an uncertain result if the response is lost.
4. If the contracted gateway exposes delivery reports, correlate them to the provider ID. Display “accepted by gateway” until there is evidence of handset delivery. Locate an uncertain send before retrying it. Keep credentials out of operator logs.

<a id="text-message-acceptance-and-delivery-2"></a>

#### Operating rules

Treat an operator's language and a contact's language as separate preferences. Resolve a template in the contact's exact locale, then an approved fallback. Persist the text actually sent, template revision and resolved locale under the organization's access and retention rules. Preserve names, references and Unicode characters. Estimate segments using the encoding and limits for the chosen gateway route. If a route cannot carry the result, return the character or size problem before dispatch. Any transliterated variant must be separately approved. A phone prefix alone cannot identify the language its owner reads.

<a id="text-message-acceptance-and-delivery-3"></a>

#### Acceptance cases

| Scenario | Expected replacement result |
|---|---|
| English-speaking operator requests an Afrikaans appointment reminder for contact C17. | Render the approved Afrikaans version, insert the correct appointment reference, and send once. The operator sees the result in English and can inspect the selected template revision. |
| A recipient's approved German SMS preserves “Jürgen”. A gateway confirms only submission. | The outbound body retains the name. Store a gateway reference and show the submitted state. Delivery remains pending confirmation. |
| A Chinese template uses characters unavailable on the configured route or exceeds its configured segment limit. | Display the localized validation reason. The gateway receives zero requests and the contact preference is preserved. |
| A response times out after submission and the operator reopens the same operation. | Show the existing uncertain result for reconciliation. An additional billable text requires a confirmed retry decision. |

A provider-approved test account, concrete route specification and test deliveries are needed to establish which receipt, segment and retry semantics the listed integration actually supports.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/telenor_sms.md).

## Branching surveys and response aggregation

An author configures stable questions, options and branches. Publishing exposes a particular survey definition. A participant’s completion creates one answer set tied to that definition, its language and the selected branch.

**Worked case.** One survey option uses the stable ID delivery with German and Afrikaans labels. Two respondents select the option in their respective languages and complete the delivery follow-up. Store two answers and group both under delivery with the correct follow-up responses. Question and option identity outlive translated labels, while free-text responses retain their original language.

### Detailed workflow and cases

<a id="branching-surveys-and-response-aggregation-2"></a>

#### Acceptance cases

- A survey branches to delivery questions when the answer ID is `delivery`. A German respondent selects “Lieferung” and an Afrikaans respondent selects “Aflewering”. Both see their localized follow-up question. The analyst obtains two delivery responses in one group.
- A respondent opens revision 4 and starts typing a Chinese comment. An author changes the prompt and publishes revision 5. Submission retains the revision-4 prompt, locale and original comment. Refreshing the acknowledgement with the same submission ID creates no extra response.
- A hidden branch posts an unexpected answer or a public respondent attempts to read another submission. Reject the operation, retain other respondents' confidentiality and return a readable error in the selected locale.

Exact URL expiry, authentication of private surveys, concurrent editor saves, fallback behavior and anonymous answer retention require an installed-release check.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/tripetto_survey.md).

## Rule-based text reminders

Match a business event against message conditions. Resolve an approved text template and its placeholders for the recipient. Store the outgoing request and queue acknowledgement before reconciling actual delivery.

**Worked case.** A French-speaking customer has an overdue order, an approved template and a valid destination. The overdue event is processed twice and the messaging provider places the first submission in its queue. Retain one queued reminder with the original order number and do not mark it delivered. The recipient selects the template language while the provider reference, order identity and queue state stay stable.

### Additional decisions

An administrator creates a rule keyed by company, event and condition, then binds a recipient field and versioned message variants. The posting process emits an event referencing a committed business document. A worker evaluates the rule against its allowed fields and records an outbound notification per rule, occurrence and recipient. Recheck cancellation or payment before dispatching a delayed reminder. A paid order should not generate an overdue notice just because it was overdue when the schedule was created.

### Detailed workflow and cases

<a id="rule-based-text-reminders-1"></a>

#### Operating rules

| Result | Required treatment |
|---|---|
| Configured condition is false | Record the suppressed occurrence and reason, with zero provider calls. |
| Recipient has an approved language variant | Save the rendered body, locale, template revision and outbound reference with controlled access. |
| No approved fallback, missing placeholder or unsupported rich content | Hold the notification for correction. Expose a localized reason to the operator. |
| Provider accepted the message into its queue | Link its reference to the original event. Reconcile before retrying an uncertain dispatch. |

<a id="rule-based-text-reminders-2"></a>

#### Acceptance cases

- An overdue order for “Élodie” uses a French template. Its number matches the source record, the translated due date is readable and all characters survive the plain-text transport. Saving the same ERP event twice produces one queued message.
- An Afrikaans variant refers to a missing due-date field. The English operator sees a correction request naming the faulty variant. No literal placeholder, HTML body or unapproved alternate language goes out.
- Payment arrives before the scheduled reminder is dispatched. Reevaluation cancels the send without disturbing the posted payment. A provider-side queue assembled earlier remains distinguishable from a message never dispatched.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/ultramsg_whatsapp_integration.md).

## Personalized recipient messaging

Map approved template parameters to business fields and select individual or multiple leads, opportunities or suppliers. Retain one dispatch identity and recipient-specific substitutions per message.

**Worked case.** A German-speaking operator selects an Afrikaans-speaking supplier with a verified Namibian number. The operator sends a mapped supplier update using the recipient’s approved variant. Queue one Afrikaans message addressed to the stored international number, with that supplier’s reference. The recipient’s language and telephone country code are independent of each other and of the operator’s language.

### Additional decisions

Separate the sender account, normalized international destination, business record and language preference. The same contact may appear in two lists. A batch should carry a stable campaign ID, an allowed recipient selection and one delivery key per destination and intended message. Resolve duplicate selections before enqueueing. Check record access and communication permission per recipient. Return counts of queued, suppressed and rejected deliveries with details available only to authorized staff.

### Detailed workflow and cases

<a id="personalized-recipient-messaging-3"></a>

#### Acceptance cases

- A German-speaking operator sends a supplier update to an Afrikaans-speaking contact with a Namibian international number. The provider receives the configured Afrikaans template, that recipient's international number exactly once and that supplier's reference. A second German-speaking recipient receives the German variant.
- A lead and supplier share one number but have different references. Reject an ambiguous personalization unless the campaign defines one record-specific message for each authorized recipient context. Never substitute another record's name or invoice.
- A batch includes a missing translation and one accepted message. Record the held recipient separately. Retrying after publishing the missing variant submits only the outstanding delivery. Credentials and complete provider responses remain restricted in activity views.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/whatsapp_app.md).

## Translated document message attachments

A rule can trigger on save, submission, update or a field transition. Resolve the approved message and any required document rendition in the selected language before dispatch. Record the exact attachment identity.

**Worked case.** A submission rule requires an Arabic message and an Arabic PDF, but only the message variant exists. An English-speaking operator submits the matched invoice. Hold the notification, identify the missing layout and send no mismatched attachment. The PDF and approved provider template must satisfy the recipient language specified by the rule.

### Detailed workflow and cases

<a id="translated-document-message-attachments-1"></a>

#### Operating rules

| Component | Information to preserve | Operation |
|---|---|---|
| Notification rule | Tenant, record type, lifecycle event or changed field, typed old/new predicate, recipient resolver, permitted attachment and template key | Evaluate after commit. A field-change rule compares values before and after the change. An unrelated save cannot satisfy it. |
| Template variant | Provider account and template name, provider language code, approval state, typed variables and media header type | Choose an approved recipient-language variant. Validate fields and render the correct authorized document revision. |
| Delivery | Rule, triggering change, recipient, document version, language, message ID and status | Store one intent per event/recipient. Reconcile provider acknowledgements and surface failures in the operator's language. |

<a id="translated-document-message-attachments-2"></a>

#### Acceptance cases

- When invoice status first changes from draft to submitted, a French-language recipient gets one approved French notification and the authorized French copy of that invoice. A later edit of internal notes does not satisfy the same field transition.
- An Arabic recipient has a matching message but no permitted Arabic document layout. A rule requiring a matching attachment holds the notice, explains the missing format to the English operator and sends no substitute PDF.
- A provider timeout leaves the attempt awaiting reconciliation. A retry with the same event identifier retains its link to the invoice. A company member who can see the invoice but lacks permission to distribute it cannot send an attachment.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/whatsapp_integration.md).

## Incoming customer conversations

Associate an incoming message and media with the customer and conversation. An authorized agent can reply in context or send an approved message to selected customer groups. Keep original message text and media independent of the agent’s screen language.

**Worked case.** A known customer sends a Chinese message with a document to the business account. An Italian-speaking agent opens the conversation and replies in Chinese, then a German-speaking colleague reopens it. Keep both messages, the authorized attachment and one customer and conversation identity. Interface labels change independently of the original customer text, reply and media.

### Detailed workflow and cases

<a id="incoming-customer-conversations-1"></a>

#### Operating rules

| Operation | Inputs | Durable result |
|---|---|---|
| Receive a message | Authenticated event, business phone account, provider message ID, sender identity, text or media ID | Create one incoming message. Match an unambiguous Customer under the same tenant, or retain an unmatched conversation for authorized resolution. |
| Read or download media | Operator, conversation, message and provider media reference | Check the current operator's access. Return only the linked attachment and preserve the source caption and author. |
| Reply | Authorized operator, original conversation, selected sending number, content or approved template variant | Create an outbound message linked to the original. Verify the number is eligible for the desired message type under the current provider rules. |
| Send to an audience | Campaign ID, group or customer selection, allowed communication purpose and reviewed template family | Resolve the audience once, exclude ineligible contacts and record one disposition per recipient. Keep a restricted view of delivery state. |

<a id="incoming-customer-conversations-2"></a>

#### Acceptance cases

- A customer sends “请发给我收据” and a document. An Italian-speaking agent sees interface labels in Italian plus the original Chinese message. Replying in Chinese retains the original customer, business number and conversation IDs. Opening the conversation in German leaves both messages intact.
- A German interface and an Arabic recipient preference coexist. A group notification chooses the approved Arabic variant for that recipient. Another recipient's selected English variant uses its own template variables. The audit captures both language codes and the exact outbound templates.
- Two customer records share the same sending number. The worker marks the incoming message as ambiguous and avoids automatic linking or disclosure to either customer. Duplicate delivery of the same provider event creates no extra message or attachment.
- An agent switches language and opens a media link belonging to a different tenant. Access is denied in the agent's interface language. Neither the reply function nor an audience-wide send can bypass conversation or contact eligibility.

The public description leaves incoming deduplication, contact matching precedence, broadcast consent, media retention, review of translations and exact roles unresolved.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/whatsapp_plus.md).
