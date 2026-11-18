# Whatsapp Plus

Emanuele Di Luzio lists this v14 connector for Meta's WhatsApp service. The publisher describes incoming and outgoing text and multimedia, downloadable attachments, text and media templates, matching the sender to a saved Customer, and replying to a received message. An operator can select customers individually, by group or across the customer database. The publisher attributes the Italian screenshots to the workstation language and says the interface adapts. No verified catalog identifies the precise installed locales or which parts of the UI translate. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/whatsapp_plus)

## Proposed conversation contract

| Operation | Inputs | Durable result |
|---|---|---|
| Receive a message | Authenticated event, business phone account, provider message ID, sender identity, text or media ID | Create one incoming message. Match an unambiguous Customer under the same tenant, or retain an unmatched conversation for authorized resolution. |
| Read or download media | Operator, conversation, message and provider media reference | Check the current operator's access. Return only the linked attachment and preserve the source caption and author. |
| Reply | Authorized operator, original conversation, selected sending number, content or approved template variant | Create an outbound message linked to the original. Verify the number is eligible for the desired message type under the current provider rules. |
| Send to an audience | Campaign ID, group or customer selection, allowed communication purpose and reviewed template family | Resolve the audience once, exclude ineligible contacts and record one disposition per recipient. Keep a restricted view of delivery state. |

The publisher describes registering a Meta webhook for incoming messages. A callback path supplied in the listing refers to a module named `frappe_whatsapp`. A shared module name alone cannot establish that another public WhatsApp application is the implementation of this listing. [Listing setup](https://cloud.frappe.io/marketplace/apps/whatsapp_plus) · [Provider documentation](https://developers.facebook.com/documentation/business-messaging/whatsapp/about-the-platform)

## Multilingual acceptance examples

- A customer sends “请发给我收据” and a document. An Italian-speaking agent sees interface labels in Italian plus the original Chinese message. Replying in Chinese retains the original customer, business number and conversation IDs. Opening the conversation in German leaves both messages intact.
- A German interface and an Arabic recipient preference coexist. A group notification chooses the approved Arabic variant for that recipient. Another recipient's selected English variant uses its own template variables. The audit captures both language codes and the exact outbound templates.
- Two customer records share the same sending number. The worker marks the incoming message as ambiguous and avoids automatic linking or disclosure to either customer. Duplicate delivery of the same provider event creates no extra message or attachment.
- An agent switches language and opens a media link belonging to a different tenant. Access is denied in the agent's interface language. Neither the reply function nor an audience-wide send can bypass conversation or contact eligibility.

The public description leaves incoming deduplication, contact matching precedence, broadcast consent, media retention, review of translations and exact roles unresolved.
