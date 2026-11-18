# Calls, surveys and messages

English · [Afrikaans](../af/communications.md) · [Deutsch](../de/communications.md) · [简体中文](../zh-Hans/communications.md)

[All topics](README.md)

Each example describes an expected result for the rebuild. The application profile identifies what was observed in a running system, traced in source or described by a publisher.

## Tata Smartflo Call Integration

Start a Smartflo call from a CRM record and reconcile the resulting call details with the agent’s activity.

**Documented workflow**

An agent with a configured phone number initiates calls from the ERP. The publisher describes fetching Smartflo call logs and recordings, linking a call to its business record, and filtering reports by date, status or call type.

**Proposed acceptance example**

A provider has acknowledged one outbound call, and its call ID appears on two overlapping log pages. Import both pages with final disposition answered and duration 48 seconds. The report shows one answered outbound call linked to its CRM activity, with duration 48 seconds. The translated disposition retains the same provider identifier, duration and dialled number.

[Detailed profile in English](../../apps/call_integration.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/call_integration)

## FCM Notification

Deliver ERP notifications to subscribed devices in each recipient’s preferred language.

**Documented workflow**

The listing attaches a push action to Notification Log creation. Its instructions link a device to the intended user through User Device, then send a notification when the subscribed user’s event fires.

**Proposed acceptance example**

One recipient has two subscribed devices with Afrikaans and German message resources. An approval notification for PO-18 is dispatched, then the acknowledged dispatch is reprocessed. Each eligible device has one logical dispatch for PO-18 and the acknowledged dispatch is not resent. The message follows the device language; the document ID stays PO-18.

[Detailed profile in English](../../apps/fcm_notification.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/fcm_notification)

## Telenor Sms

Send an SMS to a contact through Telenor and distinguish acceptance by the gateway from confirmed delivery.

**Documented workflow**

The publisher describes ERP users sending outbound SMS messages to contacts through Telenor’s API. Its public support forum gives no details about delivery receipts, encoding or language selection.

**Proposed acceptance example**

Contact C17 prefers Afrikaans and an approved Afrikaans appointment reminder exists. An English-speaking operator requests that reminder and the gateway confirms submission only. Record one submitted SMS containing the approved Afrikaans text and appointment reference, with handset delivery still unconfirmed. The contact controls the message language and the operator controls the language of the status display.

[Detailed profile in English](../../apps/telenor_sms.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/telenor_sms)

## Tripetto Survey Integration

Publish a branching survey and group responses by the question and option selected in each participant’s language.

**Documented workflow**

An author opens the visual editor from a Survey, saves questions and branching rules, then publishes the survey to generate a form URL. When a participant submits the form, the ERP stores a Survey Answer.

**Proposed acceptance example**

One survey option uses the stable ID delivery with German and Afrikaans labels. Two respondents select the option in their respective languages and complete the delivery follow-up. Store two answers and group both under delivery with the correct follow-up responses. Question and option identity outlive translated labels, while free-text responses retain their original language.

[Detailed profile in English](../../apps/tripetto_survey.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/tripetto_survey)

## Ultramsg Whatsapp Integration

Send a plain-text WhatsApp reminder through UltraMsg when a business event satisfies the configured rule.

**Documented workflow**

An administrator configures an UltraMsg instance and token, event conditions and message templates with placeholders. The publisher describes automatic plain-text WhatsApp alerts for events such as overdue orders or payment reminders.

**Proposed acceptance example**

A French-speaking customer has an overdue order, an approved template and a valid destination. The overdue event is processed twice and UltraMsg places the first submission in its queue. Retain one queued reminder with the original order number and do not mark it delivered. The recipient selects the template language while the provider reference, order identity and queue state stay stable.

[Detailed profile in English](../../apps/ultramsg_whatsapp_integration.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/ultramsg_whatsapp_integration)

## Whatsapp App

Send personalized WATI templates to selected leads, opportunities or suppliers and review the outcome for each recipient.

**Documented workflow**

An administrator enables the WATI connection and maps a WATI template’s parameters to ERP fields. Operators select individual or multiple recipients from Lead, Opportunity or Supplier lists and can review messaging activity.

**Proposed acceptance example**

A German-speaking operator selects an Afrikaans-speaking supplier with a verified Namibian number. The operator sends a mapped WATI supplier update using the recipient’s approved variant. Queue one Afrikaans message addressed to the stored international number, with that supplier’s reference. The recipient’s language and telephone country code are independent of each other and of the operator’s language.

[Detailed profile in English](../../apps/whatsapp_app.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/whatsapp_app)

## WhatsApp Integration

Send an approved WhatsApp template with the correct document PDF when a configured field or document state changes.

**Documented workflow**

An administrator creates a matching template in the ERP and Meta, selects its language and maps any PDF header. The listing describes rules that send text or PDF notifications when a document is saved, submitted or updated, or when a field changes.

**Proposed acceptance example**

A submission rule requires an Arabic message and an Arabic PDF, but only the message variant exists. An English-speaking operator submits the matched invoice. Hold the notification, identify the missing layout and send no mismatched attachment. The PDF and approved provider template must satisfy the recipient language specified by the rule.

[Detailed profile in English](../../apps/whatsapp_integration.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/whatsapp_integration)

## Whatsapp Plus

Match incoming WhatsApp messages to customers, reply in context and send reviewed messages to eligible recipients.

**Documented workflow**

An operator can identify a saved Customer from an incoming WhatsApp message, reply, download media or send templates to selected customers or groups. The publisher says the interface adapts to the workstation language and illustrates it in Italian.

**Proposed acceptance example**

A known customer sends a Chinese message with a document to the business account. An Italian-speaking agent opens the conversation and replies in Chinese, then a German-speaking colleague reopens it. Keep both messages, the authorized attachment and one customer and conversation identity. Interface labels change independently of the original customer text, reply and media.

[Detailed profile in English](../../apps/whatsapp_plus.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/whatsapp_plus)
