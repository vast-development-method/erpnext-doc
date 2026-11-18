# Ultramsg Whatsapp Integration

[Business workflow and acceptance cases](../../../capabilities/guides/communications.md#rule-based-text-reminders).

Jet Software lists this notification app for versions 13 and 14. It requires a WhatsApp number or account and UltraMsg instance credentials. The publisher describes automatic order and payment reminders that use event conditions and placeholders. The published app supports plain-text content and identifies itself as under development. Inbound chat, media delivery and template-language negotiation are outside the documented feature set. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/ultramsg_whatsapp_integration)

## Proposed event and delivery contract

Resolve the recipient's preferred language before expanding the template. Validate the placeholders declared by that variant, render dates in the recipient's locale and expose only fields the rules administrator is authorized to send. Treat order identifiers and telephone numbers as stable strings. Preserve script and punctuation in names. The provider's text service accepts a destination and body and documents queueing when an instance is unauthorized. An accepted or queued response is therefore insufficient to mark delivery to the recipient. [UltraMsg text message API](https://docs.ultramsg.com/api/post/messages/chat)

[Read the consolidated workflow](../../../capabilities/guides/communications.md#rule-based-text-reminders-1).

## Acceptance examples

The publisher does not publish matching-rule syntax, supported events, receipt callbacks, language catalogs or delayed-job behavior. These require a versioned test site and an UltraMsg test account.

[Read the consolidated acceptance cases](../../../capabilities/guides/communications.md#rule-based-text-reminders-2).
