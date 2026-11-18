# Language selection, item text and issued documents

The operator’s interface language, the business partner’s preferred language, the product master’s language and the language agreed for a particular document are independent. The five amounts on a 276.00 invoice rendered in five languages must still represent one receivable of 276.00 in its recorded currency.

| Record or relationship | Identity and stored facts | Business rule |
|---|---|---|
| Message variant | Message identity, grammatical context, language tag, named parameters, translation, review state | A contextual variant precedes its general message. A plural must have all required forms. Validate named parameters for each variant. |
| Product text translation | Product identity and exact language tag jointly identify at most one current translation. Name and description are independently optional. | Product identity remains stable across languages. An empty translation field preserves the current draft field in the interactive lookup. |
| Issued rendition | Document identity, issue occurrence, recipient identity, channel, language, approved layout revision, resolved text and issued artifact | A reprint retrieves the issued rendition. A corrected issue gets its own revision and links to the earlier issue. |
| Recipient communication | Business event, recipient, channel, effective language, layout revision, rendition identity, delivery status and attempts | A retry reuses the original rendition. A newly approved rendering is a distinct dispatch decision. |
| Searchable translated field | Tenant, entity identity, field identity, language, original revision, translation revision and approval | A source edit can make a translation stale. Search enforces access to the underlying field and identifies any fallback language. |

## Choosing language

1. For a signed-in request, honor an explicit supported choice, then session preference, then tenant default. For a visitor, use explicit choice, saved visitor preference, supported browser languages in order and the tenant default. Keep the resolved language in the response and in the cache key.
2. An ordinary message can fall back from a regional variant to a supported language and script, then its configured terminal language. Resolve site-specific overrides and their regional variants after shared translations. Retain the fallback reason. A document issuance policy may require an approved exact or script-compatible variant.
3. An invoice takes a suggested language from the party. At issue, use the explicitly selected document language, then party preference, then document default. Resolve layout and business terms in that language. An operator switching screens midway through issuance does not select a new recipient language.
4. Apply the print or notification language only to that rendition. Restore the previous working language on success and after an error. A batch containing two recipients can render in two different languages within the same job.
5. For integrations, keep codes, instants, currency, unit, record identity, enumerations and retry identifiers stable. Display labels, dates and decimal separators at the boundary. A currency amount is formatted using the currency on the record.

## Selecting or changing a product on a commercial document

The following decisions apply to quotations, customer and supplier orders, invoices, and dispatch notes. On item selection in the master language, preserve editable row text. For another language, look up the exact product and document-language pair. Copy only nonempty translated fields. On a change of print language with populated lines, request permission to refetch. Declining preserves the existing text. Confirmation of a switch to the master language reloads both master fields. Confirmation of another language refreshes each line, preserving current values for absent fields. A missing pair can raise a configured warning. A matching pair with an empty description does not raise the missing-pair warning.

| Draft scenario | Expected item name / description | Missing-pair warnings |
|---|---|---:|
| Select flour in Afrikaans with a full translation | Meel / Koringmeel | 0 |
| Confirm refetch from German to Afrikaans | Meel / Koringmeel | 0 |
| Decline refetch from German to Afrikaans | Mehl / Weizenmehl | 0 |
| Confirm Afrikaans with translated name only | Meel / Weizenmehl | 0 |
| Confirm Simplified Chinese with no exact pair and warnings on | Mehl / Weizenmehl | 1 |
| Repeat with warnings off | Mehl / Weizenmehl | 0 |
| Return from Afrikaans to master German and confirm | Mehl / Weizenmehl | 0 |
| Select the master language when the current row carries manual edits | Manual / Edited | 0 |

Quantity 2 and rate 35 give the same pre-tax line amount of 70 in every row. The product, unit of measure and currency do not change. A delayed lookup may only write back if its product and document language still match the row. Interactive entry, import and service entry share the declared issue policy. A document that requires a complete translation holds for review when a mixed-language preview fails that policy.

System administrators, inventory operators and accounting operators may maintain product translation rows under the applicable grants. System administrators and inventory managers may edit translation settings. Inventory and accounting operators can read those settings. Confirm effective company and field scope before allowing edits.

## Delivery examples

A clerk working in German issues a collection notice to an Afrikaans-speaking customer. Resolve the Afrikaans notice, record the order identity and preparation instant, and retain the exact bytes. If the channel times out, the delivery worker retries the same logical notice and records its second attempt. If the customer has requested Simplified Chinese and an approved rendition is mandatory but absent, hold the notice for a language decision before dispatching anything.

| Language | Customer invoice heading |
|---|---|
| English | Sales Invoice |
| Afrikaans | Verkoopsfaktuur |
| Deutsch | Ausgangsrechnung |
| 简体中文 | 销售发票 |
| العربية | فاتورة مبيعات |

For right-to-left layouts isolate identifiers, retain logical copy order, and use the reading order expected for the document language. Test mixed-script party names, translated unit labels, Arabic shaping, Chinese breaks, German compound words and Afrikaans diacritics in the actual delivery format. Signing fixes document bytes. A translated invitation or email may accompany the same signed document without modifying it.
