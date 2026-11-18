# Language, currency and document issuance

A receiving clerk enters a shipment in Afrikaans, a customer receives an invoice in German, and a colleague reconciles the payment in Chinese. They use the same shipment, invoice, posting, currency and settlement. Persist the identity and monetary facts independently of translated labels.

| Context | Selection and persistence |
|---|---|
| Signed-in view | Prefer a supported explicit selection, then the user's session preference, then the tenant's default. Return the resolved language with the view. |
| Guest view | Prefer a supported explicit selection, saved visitor preference, supported browser languages in order, then the tenant default. Try exact and parent language tags in the configured order. Key cached content by tenant, language and visibility. |
| Party document | On party selection, copy the party's document-language preference into the draft when the mapping applies. At issue, resolve the document's requested language, party preference and tenant default. Retain the actual approved rendition, selected template and language. An ordinary reprint uses the issued rendition. |
| Recipient or queued message | Resolve the intended recipient independently of the author and worker. Capture the selected template and language with the outbound event. A retry reuses them even after the recipient changes preference. |
| Template rendering | Temporarily select the print language, render and restore the prior language and template context on exit, including failures. A batch can mix recipients and languages. |
| Translated business text | Retain the tenant, record, field, original content revision, target language, translator, review status and approval. A source edit can mark the translation stale. Apply the original record's access checks to searchable variants. |
| Import, exchange and export | Use stable field identities, enumeration codes, decimal values, time instants, currency codes and unit identities. A human-readable export can include localized text with its language. Import must resolve an ambiguous decimal or date under an explicit input locale before posting. |

Resolve translations by message key and grammatical context. Combine common and regional dictionaries in configured capability order, then apply tenant-level language and regional overrides. A missing context-specific message falls back to its general form, then its base text. A language policy must specify when a fall back across script or regional varieties is acceptable. For instance, a request for Traditional Chinese in Hong Kong can prefer a Traditional Chinese variant ahead of a fallback using another script. Record the resolved language for issued content. When a regulated document requires an approved rendition, missing approval blocks issue.

Substitutions have named, typed arguments. Preserve the significant arguments across translated variants and apply output-specific escaping. An application can translate a failure message while preserving its stable failure category and arguments. When a screen, document or export changes language, the system retains exchange-rate direction, conversion date, currency precision, rounding, allocation and outstanding amounts. Locale, reporting time zone, currency and accounting policy are independent inputs.

For outbound collection notices, a German-speaking operator can issue an Afrikaans notice for sales order SO-1047. A later retry by a Chinese-speaking operator still uses the original Afrikaans wording and event identity. The [four-language examples](notice-examples.json) specify the expected event count and treatment of missing approved renditions.

For a fully settled invoice with total 276.00 and outstanding balance zero, translations can show “Sales Invoice”, “Verkoopsfaktuur”, “Ausgangsrechnung”, “销售发票” or “فاتورة مبيعات”. Each rendering must carry the same invoice number, party, posting state, currency, amount and settlement balance. Verify that glyphs, bidirectional identifiers, line breaks and reading order survive the selected delivery medium.
