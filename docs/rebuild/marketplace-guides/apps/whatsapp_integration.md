# WhatsApp Integration

Akhilam Inc lists a v13 integration with Meta's WhatsApp Cloud API. It advertises document notifications on save, submit, update and field-value change, conditional sends, text templates and PDFs as media. The publisher's illustrated guide describes linking the business number and credentials, creating a matching template name in the ERP and Meta, selecting a language, mapping a PDF header when applicable and awaiting template approval. Its English-language example establishes one configuration. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/whatsapp_integration) · [Publisher setup and template guide](https://docs.google.com/document/d/1sm4lhX8w_WT4SFuQNbtJLpW36sTDNzO5129RBt_LSjg/mobilebasic)

## Replacement rule and message contract

| Component | Information to preserve | Operation |
|---|---|---|
| Notification rule | Tenant, record type, lifecycle event or changed field, typed old/new predicate, recipient resolver, permitted attachment and template key | Evaluate after commit. A field-change rule compares values before and after the change. An unrelated save cannot satisfy it. |
| Template variant | Provider account and template name, provider language code, approval state, typed variables and media header type | Choose an approved recipient-language variant. Validate fields and render the correct authorized document revision. |
| Delivery | Rule, triggering change, recipient, document version, language, message ID and status | Store one intent per event/recipient. Reconcile provider acknowledgements and surface failures in the operator's language. |

A sender's interface language does not choose the message language. A recipient's preferred language selects a reviewed template and the associated PDF print variant. Do not translate record identifiers or template parameter positions. Where the organization requires both message and attachment in a specified language, hold the send if either lacks a suitable variant. Keep the approval revision and the actual PDF revision for audit. The provider's business messaging documentation defines its own service capabilities and onboarding. [Meta business messaging](https://developers.facebook.com/documentation/business-messaging/whatsapp/about-the-platform)

## Acceptance examples

- When invoice status first changes from draft to submitted, a French-language recipient gets one approved French notification and the authorized French copy of that invoice. A later edit of internal notes does not satisfy the same field transition.
- An Arabic recipient has a matching message but no permitted Arabic document layout. A rule requiring a matching attachment holds the notice, explains the missing format to the English operator and sends no substitute PDF.
- A provider timeout leaves the attempt awaiting reconciliation. A retry with the same event identifier retains its link to the invoice. A company member who can see the invoice but lacks permission to distribute it cannot send an attachment.

The guide describes historical provider screens. Exact event ordering, provider version, retry semantics, locale fallback and the installed application source remain unverified.
