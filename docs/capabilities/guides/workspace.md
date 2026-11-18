# Workspace and permissions

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Branch-scoped access review

Scope grants by module, record class, action and permitted record value. Preview changed visibility before applying or deleting grants. Test actual access independently from access to the permissions editor.

**Worked case.** Two companies have branches displayed as Central, and an order reader has an explicit grant for only the first branch. The user lists orders after switching the interface language. Only orders for the first branch appear and the reader receives no approval right. Branch, document and role identifiers govern access even when their translated labels coincide.

### Additional decisions

A permission administrator defines a reusable profile of record restrictions, chooses the users to whom it applies and previews the resulting grants. Store the profile version, user, allowed record type and ID, applicable document type and optional default as separate fields. Keep permission to perform an action distinct from the record scope on which the action is allowed. A profile limiting sales orders to a branch cannot grant approval rights to someone who can only read orders.

## System resource monitoring

Expose authorized readings of processor, memory and storage usage with measurement time, host and units. Distinguish a current measurement from a cumulative value. Format stable quantities for the viewer.

**Worked case.** One host sample reports 62.5 percent memory utilization, a boot instant and a kernel release. Authorized operators open that sample in English and German. Both read the same utilization, release and boot instant. Only labels, decimal separator and display formatting change.

### Additional decisions

An infrastructure operator selects an authorized host. A read-only sampler produces host ID, observed timestamp, metric key, quantity, unit and availability. For a filesystem series, also record the mounted volume identifier. Distinguish unavailable frequency, a zero usage value, an old reading and a host that cannot be reached. A failed read of one metric need not discard the other measurements. Read operations do not alter host configuration or ERP business records.

Translate metric labels, status text, chart legends and accessible chart descriptions. Keep resource identifiers, OS release strings and unit semantics stable. Format timestamps for the viewer's chosen time zone and numbers in the viewer's locale. Record boot and sample times as instants so two translations yield the same uptime. Where a driver does not expose a sensor, use a translated “unavailable” label and leave the numeric value absent.

## Multilingual workspace search

Localize workspace labels and search aliases while applying role and document access before returning results. Keep fiscal calendar or alternate date displays separate from the stored civil day.

**Worked case.** One user can open Sales Invoice on an Arabic desk and another user's role cannot. Search for the English source name from each Arabic interface. Only the authorized user sees the translated result and can navigate to the same canonical record type. Translating the navigation label or switching direction grants no additional access.

## Split-view record editing

Pair the filtered list with its selected editable record. Preserve identity and pending changes when resizing or switching language. A record change with an unsaved edit requires a decision from the editor.

**Worked case.** Order 42 has an unsaved Arabic note in the split form. The user changes interface language, selects order 43, then chooses to stay. Order 42 remains selected and its original note is preserved while the prompt uses the active language. Stable selection and filter keys survive layout mirroring and label translation.

### Additional decisions

Persist the current record type, typed filters, sorting, selection ID, list scroll position and pane ratio separately from the document being edited. Selecting a clean row fetches its authorized form. On an unsaved edit, offer save, discard or stay; honour the operator's choice before replacing the form. A save carries the observed revision and changed fields. On success update the row, re-evaluate whether it still matches the filter and preserve a predictable selection. On conflict preserve the pending edits for comparison. Recheck document and field permissions on every load and save.

Drive layout from logical start/end positions. Translate menu names, prompts, tooltips, field labels, selection options and keyboard access hints through the active language's catalog. Use stable field and option keys in routes and filters. A user may switch language without renaming records, discarding text already typed or changing the meaning of a saved filter. Type-ahead may display localized names while selecting by record ID.

## Delegated support sessions

An authorized support operator can request a delegated session with an eligible target identity. Correlate initiator and target session audit entries. Deny delegation from a system manager to another system manager under this profile.

**Worked case.** An authorized support operator with English as their preference selects an ordinary user whose preference is Afrikaans. Start a support session for that user with a reason, then attempt a separate delegation from one System Manager to another. For the eligible target, correlate operator and target activity records under one operation. Reject the privileged target and create no successful target-login event. Translated role captions have no effect on the decision. Preserve the operator ID, target ID and original reason in the audit record.

## Short links and scannable destinations

Store the approved destination and assign a five-character case-sensitive token. Encode the resulting address in the scannable symbol. Optional artwork must preserve decoding and the stored destination.

**Worked case.** An editor has an approved destination with an encoded accented path and an ordered query string. Publish the short link, scan its QR code under an Arabic interface, then type the token under a German interface. Both methods resolve the same published token and lead to the exact stored destination including the escaped path and query. Keep token case and QR payload identical regardless of reading direction or label language.

## Accessible workspace navigation

Apply responsive presentation preferences and localized navigation under existing access grants. Keyboard focus and reading order must remain usable on small right-to-left screens.

**Worked case.** An authorized workspace route exists and the selected role cannot open the administration route. Switch from English to Arabic at a narrow viewport and navigate the workspace by keyboard. The allowed route remains reachable with visible focus and wrapped text. The administration route still rejects the restricted role. RTL placement and translated captions leave permission keys, route IDs and the user identity unchanged.

### Additional decisions

A site administrator publishes a versioned appearance configuration. Store theme ID, brand assets, design values and a known-good default. The application supplies each user with their authorized menu, current route, active language and writing direction. The theme renders that input. If a configuration fails validation, retain the previous published revision. If an individual asset cannot load, keep forms and navigation usable with default styles.

The user opens a workspace, follows a translated shortcut, then returns to the current list or document. Navigation entries use stable route keys. A localized caption belongs to the translation catalog, branding to the theme, and permission decisions to the ERP service. Screen-reader names, focus indicators, form errors and selected-item state should survive every theme variant.

## Translated field guidance

For each record class and field, define the help presentation, trigger, heading and body. Publish an approved translation pair per field. Refresh cached guidance and expose help only for fields the reader may see.

**Worked case.** A supplier field has an English default help popover and an approved Arabic header/body pair. Focus the field in Arabic, then request an Afrikaans version before and after its first approved translation is published. Arabic shows its full pair. Afrikaans shows the default pair first and the new localized pair after publication and cache refresh. No form value changes. Fallback operates on a complete header/body pair. Only visible fields expose help and the field key retains its canonical value.

### Additional decisions

Address a help definition by site, stable document type, field key and help revision. Store its display variant, supported event, logical placement and localized header/body pairs. An authorized editor previews a draft as a target user before publishing. Resolve published help when rendering a field the current user can see. Invalidate cached renderings of changed definitions across languages and revisions. A renamed or removed field leaves an orphaned definition for the editor to repair.

The renderer supplies a keyboard-accessible trigger and dismissal, escapes authored text according to the configured content format, and associates the help with its field for assistive technology. Resolve the header and body from the same chosen language or fallback together. Free-text field values and field identifiers never become translation keys.
