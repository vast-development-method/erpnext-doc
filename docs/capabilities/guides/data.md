# Data transfer and entry

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Analytical dataset export

Map permitted record fields to destination columns. Filter and order incremental transfers by modification instant and stable record identity. Persist the confirmed cursor only after destination acknowledgement. Reprocessing a row must produce one destination identity.

**Worked case.** INV-001 and INV-002 share a modification timestamp and the export page size is one. The job stops after the first write before confirming its cursor, then restarts from a German interface. The destination contains exactly one row for each invoice ID. Translated captions never rename destination columns or change source row keys.

### Additional decisions

Keep the source site and canonical record type, projection, typed predicate, target table and immutable configuration revision on the export. A worker reads rows ordered by modification instant and then by row ID. Compare the whole pair with the committed cursor so records with equal timestamps cannot be skipped. Use the source site, type and document identity as the logical destination key. Commit the next cursor only after the destination acknowledges the page. A changed projection or narrower filter needs an explicit reconciliation decision, including what to do with records previously visible in the target.

Keep source field IDs and typed decimal, currency-code and datetime values stable when the operator changes language. Export translatable content as specifically selected columns or separate records keyed by document, field and language. Preserve Unicode values and their language tags. The dashboard presents translated dimension names and localized numbers; filters and groupings retain canonical values. An available-language fallback in the dashboard must not silently manufacture a missing translation in the warehouse.

## Multilingual chat composition

An administrator selects the text service and generation settings. Staff compose a turn and explicitly send it from their workspace. Preserve input-method composition and the requested reply language independently of the interface language.

**Worked case.** A user composing Chinese text has an active input-method composition in a German chat panel. Press Enter to confirm the character, finish the sentence and then explicitly send. Composition does not dispatch a turn; explicit send creates exactly one message with the composed text. The German UI and the requested answer language do not alter the user's original Chinese message.

### Additional decisions

A chat session belongs to a tenant and actor. Sending a turn requires that session ID, client message ID, ordered user text and an optional response-language preference. Track pending, completed or failed delivery on that turn. Store the provider response separately from the input so a retry cannot overwrite what the user wrote. Restrict any retained history to the owner or an expressly authorized role. Switching pages or closing the window preserves the chosen session until the explicit new-chat action or the site's configured expiry. Opening a record must not implicitly transmit its content to the provider.

## Hijri civil day conversion

A calendar selector displays the same civil day using Hijri or Gregorian notation. Record the chosen month-start convention and its valid range. Convert for display and entry while preserving the canonical civil day through a round trip.

**Worked case.** Use the Umm al-Qura month-start convention. Enter 1445-09-01 AH, switch to Gregorian, reopen the field and switch back. The canonical date is 2024-03-11 and the original Hijri day is restored. Changing language or numeral style does not change the selected day or calendar policy.

### Additional decisions

Model UI language, numeral system, calendar choice, version of the calendar table, and display zone independently. A civil date is stored as an ISO date. A timestamp additionally carries its instant and uses the chosen zone when deriving a local day. Calendar switching for a date-only field must never move the stored day through a UTC conversion. Display a clear calendar label and localize month names, field instructions and errors. If a label lacks a translation, retain the correct numeric date and calendar identifier.

## Nepali civil day conversion

Permit Nepali date entry in sales, purchasing, people and accounting documents. Convert to a canonical civil day for storage and filters, and retain the display calendar and numeral style as separate preferences.

**Worked case.** A purchase record is entered with 1 Baisakh 2081. A different user filters on Gregorian date 2024-04-13 and changes the display language. The filter returns the same record and switching the calendar back restores 1 Baisakh 2081. Language, numeral style and calendar preferences never change the stored civil day.

### Additional decisions

For each Date field, maintain one canonical civil date. Accept a calendar identifier, numeric year/month/day and a conversion-table revision. Validate the day against the selected calendar, convert once and save the canonical date with the business record. Rendering performs the inverse conversion for the viewer. Changing the picker view leaves an untouched record clean. Use the same canonical date for filters, comparisons, invoice ageing and payroll boundaries. A civil date has no time-of-day or UTC offset.

Treat language, numeral system and calendar as separate preferences. A Nepali-speaking clerk can choose Gregorian input, and an English-speaking clerk can choose Bikram Sambat input. Identify the calendar beside editable and ambiguous printed dates. If approved local month names are unavailable, use an explicitly labelled numeric format. Preserve the actual conversion-table range and report a localized error outside it. A fixed offset in years cannot perform the conversion across irregular month boundaries.

## Multilingual business record questions

Attach the original question, conversation history and permitted record context to a user-owned session. Persist the returned answer separately. Resolve document and field permissions before supplying business data.

**Worked case.** A German-interface user may read an invoice and its outstanding amount. The user asks about that invoice in Afrikaans and requests an Afrikaans answer. The reply uses Afrikaans, cites the source field, preserves the original question and leaves the invoice unchanged. Language choice cannot broaden the user’s access to invoices or private chat history.

### Additional decisions

Accept a question, private conversation ID, message ID, requested response language and optional record or workspace reference. Check access to that conversation and any business context before materializing history or forwarding context to a provider. Record only the approved disclosure scope. A successful answer records the original message, answer text, generated language, sources when available and provider outcome. An unavailable service leaves the message in a retryable state. A retry with the same message ID must attach to the original turn.

Keep the user's original words, document names and quoted excerpts. Store answer translations as derivatives tied to the original. Render navigation labels, language names and errors from a catalog. Distinguish the language used to ask a question from the language requested for its answer. Define unsupported-language and missing-source outcomes. Advice about a form should never itself post or approve that form.
