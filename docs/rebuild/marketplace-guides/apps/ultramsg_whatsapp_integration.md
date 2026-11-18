# Ultramsg Whatsapp Integration

Jet Software lists this notification app for versions 13 and 14. It requires a WhatsApp number or account and UltraMsg instance credentials. The publisher describes automatic order and payment reminders that use event conditions and placeholders. The published app supports plain-text content and identifies itself as under development. Inbound chat, media delivery and template-language negotiation are outside the documented feature set. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/ultramsg_whatsapp_integration)

## Proposed event and delivery contract

An administrator creates a rule keyed by company, event and condition, then binds a recipient field and versioned message variants. The posting process emits an event referencing a committed business document. A worker evaluates the rule against its allowed fields and records an outbound notification per rule, occurrence and recipient. Recheck cancellation or payment before dispatching a delayed reminder. A paid order should not generate an overdue notice just because it was overdue when the schedule was created.

Resolve the recipient's preferred language before expanding the template. Validate the placeholders declared by that variant, render dates in the recipient's locale and expose only fields the rules administrator is authorized to send. Treat order identifiers and telephone numbers as stable strings. Preserve script and punctuation in names. The provider's text service accepts a destination and body and documents queueing when an instance is unauthorized. An accepted or queued response is therefore insufficient to mark delivery to the recipient. [UltraMsg text message API](https://docs.ultramsg.com/api/post/messages/chat)

| Result | Required treatment |
|---|---|
| Configured condition is false | Record the suppressed occurrence and reason, with zero provider calls. |
| Recipient has an approved language variant | Save the rendered body, locale, template revision and outbound reference with controlled access. |
| No approved fallback, missing placeholder or unsupported rich content | Hold the notification for correction. Expose a localized reason to the operator. |
| Provider accepted the message into its queue | Link its reference to the original event. Reconcile before retrying an uncertain dispatch. |

## Acceptance examples

- An overdue order for “Élodie” uses a French template. Its number matches the source record, the translated due date is readable and all characters survive the plain-text transport. Saving the same ERP event twice produces one queued message.
- An Afrikaans variant refers to a missing due-date field. The English operator sees a correction request naming the faulty variant. No literal placeholder, HTML body or unapproved alternate language goes out.
- Payment arrives before the scheduled reminder is dispatched. Reevaluation cancels the send without disturbing the posted payment. A provider-side queue assembled earlier remains distinguishable from a message never dispatched.

The publisher does not publish matching-rule syntax, supported events, receipt callbacks, language catalogs or delayed-job behavior. These require a versioned test site and an UltraMsg test account.
