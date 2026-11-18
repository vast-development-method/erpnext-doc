# WhatsApp Integration

[Business workflow and acceptance cases](../../../capabilities/guides/communications.md#translated-document-message-attachments).

Akhilam Inc lists a v13 integration with Meta's WhatsApp Cloud API. It advertises document notifications on save, submit, update and field-value change, conditional sends, text templates and PDFs as media. The publisher's illustrated guide describes linking the business number and credentials, creating a matching template name in the ERP and Meta, selecting a language, mapping a PDF header when applicable and awaiting template approval. Its English-language example establishes one configuration. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/whatsapp_integration) · [Publisher setup and template guide](https://docs.google.com/document/d/1sm4lhX8w_WT4SFuQNbtJLpW36sTDNzO5129RBt_LSjg/mobilebasic)

## Replacement rule and message contract

A sender's interface language does not choose the message language. A recipient's preferred language selects a reviewed template and the associated PDF print variant. Do not translate record identifiers or template parameter positions. Where the organization requires both message and attachment in a specified language, hold the send if either lacks a suitable variant. Keep the approval revision and the actual PDF revision for audit. The provider's business messaging documentation defines its own service capabilities and onboarding. [Meta business messaging](https://developers.facebook.com/documentation/business-messaging/whatsapp/about-the-platform)

[Read the consolidated workflow](../../../capabilities/guides/communications.md#translated-document-message-attachments-1).

## Acceptance examples

The guide describes historical provider screens. Exact event ordering, provider version, retry semantics, locale fallback and the installed application source remain unverified.

[Read the consolidated acceptance cases](../../../capabilities/guides/communications.md#translated-document-message-attachments-2).
