# Customer communications

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Outbound calling and call dispositions

An agent calls from an assigned number on a customer or sales activity. Retrieve call details and recordings with their external identity. Link the activity, dialled number, direction, disposition and duration to a single call record for reporting.

**Worked case.** A provider has acknowledged one outbound call, and its call ID appears on two overlapping log pages. Import both pages with final disposition answered and duration 48 seconds. The report shows one answered outbound call linked to its CRM activity, with duration 48 seconds. The translated disposition retains the same provider identifier, duration and dialled number.

### Additional decisions

A call intent has a site, initiating user, permitted CRM reference, source and destination telephone numbers, timestamp and correlation ID. Track provider acknowledgement, call detail and recording availability separately. Link incoming calls to contacts using normalised telephone numbers within the appropriate site. Where a number belongs to multiple contacts, retain the call as unmatched until an authorised user chooses the record. Repeated log pages update the same provider call rather than creating additional calls. Treat separate call legs explicitly if the selected provider feed exposes them.

Persist the original disposition and map it to a stable report code. Group calls by the explicitly selected reporting time zone and reporting period. An agent can see their own activities under the chosen policy. Access to reports and to recording contents are separate permissions. Keep provider authorization material outside logs and reports.

## Device notification delivery

Associate each subscribed device with its user. An eligible notification fans out to active devices. Keep the dispatch, acknowledgement and retry state per destination.

**Worked case.** One recipient has two subscribed devices with Afrikaans and German message resources. An approval notification for PO-18 is dispatched, then the acknowledged dispatch is reprocessed. Each eligible device has one logical dispatch for PO-18 and the acknowledged dispatch is not resent. The message follows the device language; the document ID stays PO-18.

### Additional decisions

The public evidence does not establish current provider compatibility, token rotation, retry behavior or translation coverage of the marketplace build.

## Text message acceptance and delivery

An operator sends approved text to a contact’s stored number. Preserve recipient, template language, original text, gateway acknowledgement and any later delivery receipt as separate facts.

**Worked case.** Contact C17 prefers Afrikaans and an approved Afrikaans appointment reminder exists. An English-speaking operator requests that reminder and the gateway confirms submission only. Record one submitted SMS containing the approved Afrikaans text and appointment reference, with handset delivery still unconfirmed. The contact controls the message language and the operator controls the language of the status display.

## Branching surveys and response aggregation

An author configures stable questions, options and branches. Publishing exposes a particular survey definition. A participant’s completion creates one answer set tied to that definition, its language and the selected branch.

**Worked case.** One survey option uses the stable ID delivery with German and Afrikaans labels. Two respondents select the option in their respective languages and complete the delivery follow-up. Store two answers and group both under delivery with the correct follow-up responses. Question and option identity outlive translated labels, while free-text responses retain their original language.

## Rule-based text reminders

Match a business event against message conditions. Resolve an approved text template and its placeholders for the recipient. Store the outgoing request and queue acknowledgement before reconciling actual delivery.

**Worked case.** A French-speaking customer has an overdue order, an approved template and a valid destination. The overdue event is processed twice and the messaging provider places the first submission in its queue. Retain one queued reminder with the original order number and do not mark it delivered. The recipient selects the template language while the provider reference, order identity and queue state stay stable.

### Additional decisions

An administrator creates a rule keyed by company, event and condition, then binds a recipient field and versioned message variants. The posting process emits an event referencing a committed business document. A worker evaluates the rule against its allowed fields and records an outbound notification per rule, occurrence and recipient. Recheck cancellation or payment before dispatching a delayed reminder. A paid order should not generate an overdue notice just because it was overdue when the schedule was created.

## Personalized recipient messaging

Map approved template parameters to business fields and select individual or multiple leads, opportunities or suppliers. Retain one dispatch identity and recipient-specific substitutions per message.

**Worked case.** A German-speaking operator selects an Afrikaans-speaking supplier with a verified Namibian number. The operator sends a mapped supplier update using the recipient’s approved variant. Queue one Afrikaans message addressed to the stored international number, with that supplier’s reference. The recipient’s language and telephone country code are independent of each other and of the operator’s language.

### Additional decisions

Separate the sender account, normalized international destination, business record and language preference. The same contact may appear in two lists. A batch should carry a stable campaign ID, an allowed recipient selection and one delivery key per destination and intended message. Resolve duplicate selections before enqueueing. Check record access and communication permission per recipient. Return counts of queued, suppressed and rejected deliveries with details available only to authorized staff.

## Translated document message attachments

A rule can trigger on save, submission, update or a field transition. Resolve the approved message and any required document rendition in the selected language before dispatch. Record the exact attachment identity.

**Worked case.** A submission rule requires an Arabic message and an Arabic PDF, but only the message variant exists. An English-speaking operator submits the matched invoice. Hold the notification, identify the missing layout and send no mismatched attachment. The PDF and approved provider template must satisfy the recipient language specified by the rule.

## Incoming customer conversations

Associate an incoming message and media with the customer and conversation. An authorized agent can reply in context or send an approved message to selected customer groups. Keep original message text and media independent of the agent’s screen language.

**Worked case.** A known customer sends a Chinese message with a document to the business account. An Italian-speaking agent opens the conversation and replies in Chinese, then a German-speaking colleague reopens it. Keep both messages, the authorized attachment and one customer and conversation identity. Interface labels change independently of the original customer text, reply and media.
