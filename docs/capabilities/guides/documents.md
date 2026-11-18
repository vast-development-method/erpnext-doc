# Document preparation and signing

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Bulk document rendition

Select record class, rendition layout, filters and an optional grouping field. Render the authorized result set and package successful outputs. Return each failed record identity and its reason alongside the downloadable members.

**Worked case.** The authorised selection spans several pages and contains 55 documents. Process the full selection with one render failure. The job returns 54 PDFs, one manifest error with a document ID and a partial completion status. Unicode group labels cannot collapse distinct group IDs, and the manifest records the language used for each PDF.

### Additional decisions

Create an export job with requester, site, document filter, authorised selection, ordering, print template, language policy and job ID. Enumerate all authorised pages against a consistent snapshot. Recheck access before printing and at download. Return a private artifact, manifest of completed document IDs, per-document errors and a final status of completed, partial, empty or failed. An all-failure result carries no download link. A repeated request for the same job returns its existing result.

Localise queue notifications and status text. Support a single requested print locale and an explicit per-recipient printing policy. Preserve the locale actually used for each PDF. Build portable, distinct archive paths with stable record IDs and Unicode-safe names. Decide group membership on the stored key. Distinct customers with the same translated name must stay separate.

### Detailed workflow and cases

<a id="bulk-document-rendition-2"></a>

#### Operating rules

- For a synthetic selection of 55 authorised invoices spanning several query pages, render 55 PDFs. One failure yields 54 files and one named manifest error. No successful renders yields a failed job with the 55 errors.
- Generate an invoice in German and another in simplified Chinese. The PDFs must render their intended scripts and the ZIP preserve both document IDs. Two customers whose labels sanitise to the same text get distinct folders.
- Revoke access before a queued PDF is rendered. Record a denial without its contents. A different user cannot download the requesting user’s completed archive.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/bulk_download.md).

## Milestone progress measurement

Choose a document class, effective date field and condition for each milestone. A successful transition writes its milestone identity, performer, instant and applicable completion percentage. Measure durations from defined event pairs.

**Worked case.** Under an absolute-percentage policy a document enters approved at 08:00 UTC and delivered at 15:03 UTC on the same day. Apply the delivered event twice. Current progress is 100%, elapsed time from approval is 423 minutes and the second delivery event adds no log. Renaming or translating the approved milestone does not change the stored interval or milestone identity.

### Additional decisions

Version a tracker definition with a target type, effective date, source date field, destination percentage field, milestone codes and explicitly selected percentage semantics. Express trigger conditions using typed field and status IDs. On a document transition, capture the triggering revision, matched milestone, evaluation time and actor, and atomically update the projection and event history. A repeated save without a new qualifying transition cannot create another elapsed-time interval. Report the first event relative to the configured starting instant, then each event relative to the previous one. Require an explicit time zone and time-of-day policy when the start field contains a date only.

### Detailed workflow and cases

<a id="milestone-progress-measurement-2"></a>

#### Operating rules

- With absolute-progress rules `approved = 40` and `delivered = 100`, a document moves from approved at 08:00 UTC to delivered at 15:03 UTC. Its latest progress is 100% and the interval is 423 minutes. Replaying the delivery event adds zero minutes and no second log.
- Two milestones are configured with overlapping conditions and equal priority. Reject the ambiguous definition, or surface a recorded conflict without silently advancing the document. A disabled tracker adds no new events.
- Allow editors to translate milestone titles and report headers. If “Approved” becomes “Goedgekeur” after the first event, a historical report must still identify the same milestone and 423-minute interval. Preserve time-zone conversion for presentation only.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/document_progress_tracker.md).

## Signed document dispatch

Identify the assigned signer, authenticate the signing request and retain the exact signed artifact. Download and email actions reuse that artifact under read permission. Dispatch and signing have different audit identities.

**Worked case.** An authorised user has signed the German version of an invoice and its artifact digest is recorded. Send two emails in different languages referencing that same signed file. Both attachment digests equal the archived signed digest. Neither dispatch creates a new signing event. Email language does not change the signed bytes or the signer identity.

### Additional decisions

An eligible business document has an immutable revision, print template/version, selected output language, intended signer and recipient. Render an unsigned PDF snapshot. A signing request references its digest, assigned signer and signing policy. The approved signing operation produces a new immutable artifact, associates a verification result and records the completion time and certificate identity. Use a protected signing credential reference. A downloaded copy and emailed attachment must refer to that exact signed artifact. Email-delivery success, retry and bounce remain separate from signature validity.

Keep the source document, rendered input and signed output distinct. The source can be amended, but the amendment must create a new PDF revision and signing request. Keep the old signed document retrievable with its prior audit record. If signing fails, identify the request and cause and leave the output unavailable for signed delivery.

### Detailed workflow and cases

<a id="signed-document-dispatch-3"></a>

#### Acceptance cases

Resolve document language before rendering, including customer terms, signature captions, glyph-capable fonts and directionality. Preserve signer and recipient names as authored. An operator can dispatch an Arabic invoice from an English interface. Translate the email body independently of the attached signed bytes.

- A German invoice is signed and sent to two authorised recipients using different email languages. Each attachment's digest equals the stored signed digest. Downloading the archive later returns those same bytes.
- An Arabic version is requested after the German PDF was signed. Generate a separate Arabic document revision and obtain a new signature. The first signed copy and its verification result remain available.
- If a non-assigned user attempts signing, or the signing service reports an unusable credential, no signed artifact is published. Retrying an email delivery resends the stored attachment without creating a second signature.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/dsc.md).

## Multiple-signer agreement completion

Copy the agreement layout at dispatch, fix recipient and field assignments, and verify each mandatory field. Record explicit rejection separately from completion. Bind final signatures to the agreement bytes.

**Worked case.** Two signers receive the same Afrikaans agreement, one using German controls and the other English. Each completes their own required field. One finalized document records both assignments and the same agreement digest. The interface and invitation language cannot alter the agreement being signed.

### Additional decisions

Bind the envelope to the exact PDF bytes, template revision, page coordinates and required components. An authenticated assignee submits a value against an envelope revision and assigned field. Record signer, time, component ID, outcome and document digest. Finalise only when every required assignment is complete. Preserve rejected envelopes with the reason and outstanding actions. Treat certificate verification and applicable legal requirements as separate qualification steps.

Choose the document language and approved template variant before dispatch. The sender and signers may each use a different interface language. Translating navigation or reminder emails must leave the original signed text, glyph positions, names and bytes intact. For a missing agreement translation, require selection of an available approved variant before sending. A translation after signature creates a separately identified rendition.

### Detailed workflow and cases

<a id="multiple-signer-agreement-completion-2"></a>

#### Operating rules

| Acceptance example | Expected result |
|---|---|
| Two signers receive the same Afrikaans agreement, one using German controls and one English. Each signs their own field. | The editable template retains its original contents. One final document identifies the same signed agreement, both completed assignments and a digest; inbox labels follow each signer. |
| The first signer submits twice and attempts a field assigned to the second signer. | A retry cannot add a signing act; the other assignment stays pending and the document cannot finalise. |
| One signer rejects the assigned document and supplies a Chinese reason. | The reason is preserved verbatim, the preparer sees the translated rejection status, and no completed certificate is issued. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/esign_app.md).

## Bilingual document layout

An authorized designer binds document fields and report values to a layout. Preview the chosen single-language or bilingual rendition before download or delivery. Printed tax values and machine-readable payloads must match the submitted record.

**Worked case.** A bilingual invoice has a mixed-script customer name, two tax lines and a signed QR. An English-speaking clerk renders it with an Arabic/English format. Both headings render, the two posted tax amounts match and the scanned QR matches the original. Changing the editor language preserves the recipient language, tax values and signed payload.

### Additional decisions

Give each format a document/report type, revision, company scope, layout tree, allowed binding paths, translatable literal keys and supported output languages. Preserve an immutable revision for a sent artifact. A manager can fork a standard format, edit a draft and publish it after validating fields, image references and locale assets. A reader requests a render using a format revision, document identity or report filters, and recipient language. Recheck the reader's rights when resolving linked fields, child rows, attachments and report data. The author of a template cannot confer those rights on its reader. Validate suggested AI edits through the same draft path and leave the last valid revision available for undo.

Resolve the output language from the explicit recipient choice or recipient preference and record the effective language. Store the author's editor language separately. A bilingual layout assigns direction and language per block. Layout direction may change column order on the page, while numerical columns remain bound to the same field keys. Include the currency from the posted document when spelling out amounts. Render original names and signed QR bytes verbatim. Make an unavailable required translation visible to the sender before sending an external document.

### Detailed workflow and cases

<a id="bilingual-document-layout-1"></a>

#### Operating rules

| Proposed acceptance case | Expected result |
|---|---|
| An English-speaking clerk prints a bilingual invoice with a mixed-script customer name, two tax rows and a signed QR. | The heading appears in both languages, Arabic shapes correctly, each tax line uses the source amount and a scanner recovers the original QR content. |
| A format binds a protected field on a linked customer. Two users render the same invoice. | The restricted user's preview, PDF and email attachment omit the protected value. An artifact cached for the privileged user cannot satisfy the restricted request. |
| A report filtered to one company has Arabic labels exceeding one line. | Headers wrap, amounts and filter scope agree with the on-screen report and the company identity survives pagination. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/lumenpdf.md).
