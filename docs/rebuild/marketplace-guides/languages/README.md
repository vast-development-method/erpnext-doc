# Language across the ERP

A warehouse operator can receive goods in Afrikaans, a German-speaking customer can receive the resulting invoice, and a Chinese-speaking colleague can reconcile the same transaction. The three readers need the same shipment, invoice and balance. Their screens, printed documents and correspondence can each use different languages. The [language and issuance contract](../../../capabilities/language-and-issuance.md) connects interface selection, item text and delivery. The observations below provide the lookup rules and evidence for those decisions.

## Reference behaviour

| Decision | Observed or traced behaviour |
|---|---|
| Request language | A recognized explicit request language takes priority. A signed-in request otherwise uses its session language. For guests, the resolver checks the preferred-language cookie, the ordered browser languages and then system language or English. The guest paths try the full tag and a parent. [Resolver](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/translate.py#L33-L106) |
| Regional and site catalogs | For a regional request, the framework merges app catalogs at the parent and regional levels, followed by site translations for the parent and region. Within each level app order matters, and a compiled message can override a CSV entry. A context-specific lookup can fall back to its general message and ultimately the source text. [Catalog merge](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/translate.py#L135-L188) · [Message lookup](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/utils/translations.py#L4-L49) |
| Party and transaction | The customer and sales invoice each have a language field. Party-detail mapping includes language among the values copied. [Customer field](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/doctype/customer/customer.json#L318) · [Invoice field](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/sales_invoice/sales_invoice.json#L1584) · [Party mapping](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/party.py#L370) |
| Printing and background work | The print-language scope saves the current language and template environment, then restores them on exit. A worker can have a job-user language distinct from the print language. [Print scope](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/translate.py#L953-L991) · [Background translation](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/utils/translations.py#L13-L25) |

### One invoice in five languages

The standard HTML print view rendered the same submitted invoice in five languages. Each rendered body contained its invoice number and the corresponding translated invoice title. After each print, the session returned to English. The database reads before and after all five renders agreed on the invoice ID, customer, document status, currency, total of NAD 276.00 and outstanding balance of zero. The German catalog also supplied the same five tested labels for a de-NA lookup. [Machine-readable observations](observed.json)

| Print language | Invoice title found in the rendered text |
|---|---|
| English | Sales Invoice |
| Afrikaans | Verkoopsfaktuur |
| Deutsch | Ausgangsrechnung |
| 简体中文 | 销售发票 |
| العربية | فاتورة مبيعات |

To reproduce, use the [integrated trading site fixture](../../live/README.md) with the two revisions recorded in the observations. Compile the shipped Afrikaans, German, Chinese and Arabic catalogs for both applications. Read a submitted non-return sales invoice and save the six persisted projection fields. As one signed-in reader with session language English, render its Standard print format inside each requested print-language scope. Inspect body text and read the projection again. For request negotiation, use the five guest/session/header combinations in the observations. The print check exercised server-rendered HTML. PDF fonts, visual ordering, third-party templates and delivered messages require their own output tests.

## Rebuild contract

| Surface | Selection and persistence |
|---|---|
| A signed-in screen | Honor an explicit supported choice for the view, then the user preference, then the tenant default. Keep the effective locale in the response. A language switch can reuse any still-authorized record reference. |
| A public page | Choose a supported explicit selection, saved visitor preference, then a supported browser language, then the tenant default. Report the actual content language. Cache public variants by language and the relevant site. |
| A document for a customer, supplier or worker | At issue time resolve the requested document language, then the party's preference and the tenant's document default. Choose an approved template for that document class, channel and language. Retain the chosen language, template revision and issued artifact for reprint. |
| A notification or a job | Resolve the intended recipient independently of the operator. Capture language choice and template revision when enqueuing. Retry the same outbound event using the same rendition. A deliberate resend or newly approved rendition has its own audit entry. |
| Editable translated content | Store each variant by tenant, content ID, field, language and source revision. Track draft, reviewed and stale variants. After a source edit, retain the old translation's provenance. A search result must reveal when it is showing another language. |
| Integration and reporting | Keep document IDs, enumeration codes, time instants, decimal values, currency/unit codes, accounts, provider IDs and idempotency keys stable. Emit human text alongside codes, with its language. Label machine exports separately from localized presentation exports. |
| Restricted text, signatures and evidence | Preserve submitted text and original file bytes. A translation references a source revision with its translator and review state. Signed or regulated output with no approved language variant returns an actionable outcome under its issuance policy. |

For ordinary interface copy, use a stable message key, grammatical context and named arguments. A translator can reorder arguments, choose a plural form or use a different grammatical construction. Enforce compatible parameter names/types for every variant and escape values for the output channel. An error carries a stable code and typed arguments, so a support worker can diagnose a failure seen in another language. Keep private source text under the same access control when searching or translating it. [Message and translation conventions](https://docs.frappe.io/framework/user/en/translations)

Use BCP 47 tags for the public contract. A deployment declares its supported variants, fallback sequence and a terminal available language for each surface. When script matters, preserve it in lookup: for a zh-Hant-HK request, first prefer an available zh-Hant variant. An organization can require an explicit permitted fallback before showing a document in a different script or language. The observed parent function splits at the first separator; it does not implement this complete script-aware policy. Publish the resolved language and fallback reason. [Language tag matching](https://www.rfc-editor.org/rfc/rfc4647) · [Reference parent function](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/translate.py#L83-L93)

Language, calendar, time zone and currency are independent settings. Format dates and amounts at the presentation boundary, with a known locale and explicit reporting zone or calendar when required. Parse human entry in its stated locale, validate ambiguity before posting, and transmit a canonical value. Each formatter consumes the record's currency or unit. Changing a user's language must never choose a different exchange rate or accounting policy. If two visible labels are identical, map the user's selection through the stable option ID. [Unicode number and currency formatting](https://www.unicode.org/reports/tr35/tr35-numbers.html)

### Layout, documents and evidence

Set the document's language in rendered HTML. Mark passages in other languages and apply appropriate direction to the layout. Isolate left-to-right account or invoice identifiers inside right-to-left labels, preserve identifiers when copied, and verify keyboard traversal and screen-reader order. Test PDF glyph coverage, long German labels, Afrikaans diacritics, Chinese line breaking and Arabic shaping in the actual delivery channel. SMS segmenting, template approval and truncation can differ by provider and script. Display the original customer or supplier name, retain any approved alias, and keep identity matching independent of the chosen display form. [W3C language markup](https://www.w3.org/International/questions/qa-html-language-declarations) · [W3C bidirectional text](https://www.w3.org/International/articles/inline-bidi-markup/)

### Acceptance example for an issued notice

A German-speaking operator issues a ready-for-collection notice to an Afrikaans-speaking customer. The same event can also be reproduced with a Simplified Chinese or English catalog. The [example exchange](notice.json) specifies the message, template versions, resolved recipient language, stable record reference and expected retransmission. A localized error in the same fixture exposes the missing approved language without creating a new approval or sending another copy. These are example requirements for a replacement implementation. The separate [observations](observed.json) describe the actual reference site.

### Publishing a translated guide

Use an immutable listing ID in links, examples, translation memory and data exports. The human title and summary can vary by language. Retain vendor product and record names where an operator must find that exact control; explain their purpose in the reader's language. A translated page carries the language, the source edition and a link to its evidence. Mark draft or missing detail in the interface and provide access to the original. Editing a translation never changes a source finding or converts a proposed contract into an observed outcome.
