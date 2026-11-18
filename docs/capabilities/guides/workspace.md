# Workspace and permissions

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Branch-scoped access review

Scope grants by module, record class, action and permitted record value. Preview changed visibility before applying or deleting grants. Test actual access independently from access to the permissions editor.

**Worked case.** Two companies have branches displayed as Central, and an order reader has an explicit grant for only the first branch. The user lists orders after switching the interface language. Only orders for the first branch appear and the reader receives no approval right. Branch, document and role identifiers govern access even when their translated labels coincide.

### Additional decisions

A permission administrator defines a reusable profile of record restrictions, chooses the users to whom it applies and previews the resulting grants. Store the profile version, user, allowed record type and ID, applicable document type and optional default as separate fields. Keep permission to perform an action distinct from the record scope on which the action is allowed. A profile limiting sales orders to a branch cannot grant approval rights to someone who can only read orders.

### Detailed workflow and cases

<a id="branch-scoped-access-review-1"></a>

#### Operating rules

| Operation | Result |
|---|---|
| Preview change | Return grant rows to create, retain or revoke, plus conflicting defaults. Include the exact affected users and documents. |
| Apply approved preview | Resolve all references within the site, check administration rights, persist one change set and invalidate affected permission decisions. Reject a stale preview. |
| Remove profile grants | Remove rows owned by that profile. If a manual grant or second profile independently permits the same scope, preserve its provenance and effect. |

<a id="branch-scoped-access-review-2"></a>

#### Acceptance cases

Show localised role, branch and document-type captions beside the stable keys used to evaluate access. Preserve user-authored profile names and translated display names separately. The same branch name can legally appear under two companies or in two translations. Role membership, requested company and referenced record IDs must determine access.

- Create two branches, both displayed as “Central”, in separate companies. Apply a rule allowing only the first branch to an order reader. Both English and Afrikaans sessions return just the first branch’s orders. Switching the display language cannot confer an approval action.
- A second administrator changes the target rule after a bulk-deletion preview. Applying the old preview reports a conflict and changes zero grants. A fresh preview identifies the affected rows before application.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/branchy.md).

## System resource monitoring

Expose authorized readings of processor, memory and storage usage with measurement time, host and units. Distinguish a current measurement from a cumulative value. Format stable quantities for the viewer.

**Worked case.** One host sample reports 62.5 percent memory utilization, a boot instant and a kernel release. Authorized operators open that sample in English and German. Both read the same utilization, release and boot instant. Only labels, decimal separator and display formatting change.

### Additional decisions

An infrastructure operator selects an authorized host. A read-only sampler produces host ID, observed timestamp, metric key, quantity, unit and availability. For a filesystem series, also record the mounted volume identifier. Distinguish unavailable frequency, a zero usage value, an old reading and a host that cannot be reached. A failed read of one metric need not discard the other measurements. Read operations do not alter host configuration or ERP business records.

Translate metric labels, status text, chart legends and accessible chart descriptions. Keep resource identifiers, OS release strings and unit semantics stable. Format timestamps for the viewer's chosen time zone and numbers in the viewer's locale. Record boot and sample times as instants so two translations yield the same uptime. Where a driver does not expose a sensor, use a translated “unavailable” label and leave the numeric value absent.

### Detailed workflow and cases

<a id="system-resource-monitoring-1"></a>

#### Operating rules

| Acceptance example | Expected result |
|---|---|
| The sample contains memory usage 62.5 percent, a boot timestamp and a kernel release string. Administrators open it in English and German. | The same sample is reused. Decimal presentation and labels follow the viewer. The release string and numeric usage are unchanged. |
| The host exposes RAM and disk but supplies no CPU-frequency samples. | RAM and disk remain visible. The frequency series is marked unavailable without a fictitious zero point. |
| An employee can read sales dashboards but lacks host-monitor permission. | The request reveals no host metrics or machine details. Changing the interface language leaves this outcome unchanged. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/frappe_system_monitor.md).

## Multilingual workspace search

Localize workspace labels and search aliases while applying role and document access before returning results. Keep fiscal calendar or alternate date displays separate from the stored civil day.

**Worked case.** One user can open Sales Invoice on an Arabic desk and another user's role cannot. Search for the English source name from each Arabic interface. Only the authorized user sees the translated result and can navigate to the same canonical record type. Translating the navigation label or switching direction grants no additional access.

### Detailed workflow and cases

<a id="multilingual-workspace-search-2"></a>

#### Operating rules

| Operation | State and invariant |
|---|---|
| Resolve the home page | Intersect assigned role destinations with current workspace/document access. Resolve competing roles by configured priority. If the destination is unavailable, select a visible default. A translated route title never grants access. |
| Build menus and search | Index canonical object keys, source names, available translations and allowed aliases. Rank matches in the user's language and include useful source-language matches. Remove inaccessible workspaces and documents from all result surfaces and check permissions on navigation. |
| Apply translations | Store product pack, version, locale, key/context and text separately from tenant overrides. Apply tenant override first, followed by enabled product packs and configured base fallback. Disabling the pack removes only its contribution. A document's saved values and print format remain independently addressable. |
| Render the desk | Resolve language and direction before layout; keep codes, invoice numbers and numeric columns legible in mixed directional text. Show the alternate date using its named calendar. Persist favourites by object ID, and personal settings independently of company defaults and locks. |

<a id="multilingual-workspace-search-3"></a>

#### Acceptance cases

- On an Arabic desk, search for “Sales Invoice”. An authorized user sees the translated label and can navigate to the same canonical document type as on the English desk. A user without access receives no matching restricted route. Translating a workspace title preserves its favourites and visibility.
- Enable the optional Arabic glossary on a site with one reviewed tenant translation. The tenant wording remains visible. Disable the pack and that correction survives; keys supplied only by the pack revert to the configured fallback.
- Switch a posted invoice from English to Arabic with the Hijri overlay enabled. Navigation mirrors, the identifier remains readable, and the saved posting date, total and date filter are unchanged. A missing translation in a third offered language selects the configured fallback.
- A salesperson’s simplified form hides a tax field. The server continues to enforce its configured read/write permissions independently of the role-specific layout.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/lumen_theme.md).

## Split-view record editing

Pair the filtered list with its selected editable record. Preserve identity and pending changes when resizing or switching language. A record change with an unsaved edit requires a decision from the editor.

**Worked case.** Order 42 has an unsaved Arabic note in the split form. The user changes interface language, selects order 43, then chooses to stay. Order 42 remains selected and its original note is preserved while the prompt uses the active language. Stable selection and filter keys survive layout mirroring and label translation.

### Additional decisions

Persist the current record type, typed filters, sorting, selection ID, list scroll position and pane ratio separately from the document being edited. Selecting a clean row fetches its authorized form. On an unsaved edit, offer save, discard or stay; honour the operator's choice before replacing the form. A save carries the observed revision and changed fields. On success update the row, re-evaluate whether it still matches the filter and preserve a predictable selection. On conflict preserve the pending edits for comparison. Recheck document and field permissions on every load and save.

Drive layout from logical start/end positions. Translate menu names, prompts, tooltips, field labels, selection options and keyboard access hints through the active language's catalog. Use stable field and option keys in routes and filters. A user may switch language without renaming records, discarding text already typed or changing the meaning of a saved filter. Type-ahead may display localized names while selecting by record ID.

### Detailed workflow and cases

<a id="split-view-record-editing-1"></a>

#### Operating rules

| Proposed acceptance case | Expected result |
|---|---|
| Filter open orders, select order 42, edit its notes and save from a German form. | Only order 42 changes. The list retains the filter and displays its updated data without leaving the split view. |
| Start an unsaved Arabic note, switch the layout to right-to-left and select order 43. Choose to stay. | The prompt is in the active language, order 42 remains selected and its note preserves the entered characters and cursor context. |
| A colleague has saved a newer revision, or write access is revoked before save. | A stable conflict or denied result is rendered in the viewer's language. The server preserves the colleague's version and the user can recover their unsaved work. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/paneview.md).

## Delegated support sessions

An authorized support operator can request a delegated session with an eligible target identity. Correlate initiator and target session audit entries. Deny delegation from a system manager to another system manager under this profile.

**Worked case.** An authorized support operator with English as their preference selects an ordinary user whose preference is Afrikaans. Start a support session for that user with a reason, then attempt a separate delegation from one System Manager to another. For the eligible target, correlate operator and target activity records under one operation. Reject the privileged target and create no successful target-login event. Translated role captions have no effect on the decision. Preserve the operator ID, target ID and original reason in the audit record.

### Detailed workflow and cases

<a id="delegated-support-sessions-2"></a>

#### Operating rules

`beginSupportSession(targetId, reason, requestId)` derives the initiating principal from the authenticated session. Record actor ID, effective user ID, operation ID, reason, timestamps and outcome. Limit the resulting session to the target's ordinary record access. Tie its expiry to the originating authorization. Ending the session invalidates the delegated context and requires a valid operator context before privileged work can resume.

1. With an English-speaking authorized operator and an Afrikaans-speaking target, display the support banner in the active interface language, notify the target in their language, and preserve the submitted reason verbatim. Both activity events reference the same session and stable principal IDs.
2. Have one System Manager select another. The service denies the transition even if the displayed role names have been translated. The operator remains the active principal and no target-login success event exists.
3. End an authorized support session and revisit a target document. The expired delegated context grants no further access. Audit exports can be rendered in another language from the same actor, target and event codes.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/persona.md).

## Short links and scannable destinations

Store the approved destination and assign a five-character case-sensitive token. Encode the resulting address in the scannable symbol. Optional artwork must preserve decoding and the stored destination.

**Worked case.** An editor has an approved destination with an encoded accented path and an ordered query string. Publish the short link, scan its QR code under an Arabic interface, then type the token under a German interface. Both methods resolve the same published token and lead to the exact stored destination including the escaped path and query. Keep token case and QR payload identical regardless of reading direction or label language.

### Detailed workflow and cases

<a id="short-links-and-scannable-destinations-2"></a>

#### Operating rules

`publishLink(destination, optionalLogo, requestId)` requires permission to publish to the chosen site. Validate the destination against the site's allowed URI schemes, reserve a unique path atomically and produce a QR image from the actual public URL. Return the record ID, short URL and image reference together. A failed logo or image conversion leaves no live route. Public resolution accepts the exact route token and returns its stored destination. A paper QR remains valid until the route's configured retirement.

| Acceptance example | Observable outcome |
|---|---|
| The editor publishes a French-language destination with an encoded accented path and query string. | A German-speaking reader typing the short URL and an Arabic-speaking reader scanning it obtain the same stored address, including escaped bytes and query order. |
| Two simultaneous saves generate the same candidate path. | Exactly one destination obtains the path. The other operation selects another free path without replacing the first. |
| A transparent logo is supplied under the published logo profile. | The editor receives a localized validation message and can retry. The original destination text remains available for correction. |
| A requested link is missing or retired. | Return the appropriate stable resolution outcome. Localize the explanatory page and image alternative text while preserving the token's exact case and direction. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/pibicut.md).

## Accessible workspace navigation

Apply responsive presentation preferences and localized navigation under existing access grants. Keyboard focus and reading order must remain usable on small right-to-left screens.

**Worked case.** An authorized workspace route exists and the selected role cannot open the administration route. Switch from English to Arabic at a narrow viewport and navigate the workspace by keyboard. The allowed route remains reachable with visible focus and wrapped text. The administration route still rejects the restricted role. RTL placement and translated captions leave permission keys, route IDs and the user identity unchanged.

### Additional decisions

A site administrator publishes a versioned appearance configuration. Store theme ID, brand assets, design values and a known-good default. The application supplies each user with their authorized menu, current route, active language and writing direction. The theme renders that input. If a configuration fails validation, retain the previous published revision. If an individual asset cannot load, keep forms and navigation usable with default styles.

The user opens a workspace, follows a translated shortcut, then returns to the current list or document. Navigation entries use stable route keys. A localized caption belongs to the translation catalog, branding to the theme, and permission decisions to the ERP service. Screen-reader names, focus indicators, form errors and selected-item state should survive every theme variant.

### Detailed workflow and cases

<a id="accessible-workspace-navigation-2"></a>

#### Acceptance cases

1. Open the same authorized Users workspace in English and Arabic at a narrow viewport. Read a button label using keyboard focus, follow the same route, and return. Text wraps, logical start and end positions follow the page direction, and the stored user or document ID remains unchanged.
2. Apply a long German navigation label and a mixed-direction account identifier. Menus remain operable and the identifier retains its original order when copied.
3. With a restricted role, select a different theme or site language. A restricted management shortcut remains hidden where appropriate and the underlying route still enforces its access check. If a localized brand caption is missing, use the configured fallback for that caption without changing the route.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/rukntheme.md).

## Translated field guidance

For each record class and field, define the help presentation, trigger, heading and body. Publish an approved translation pair per field. Refresh cached guidance and expose help only for fields the reader may see.

**Worked case.** A supplier field has an English default help popover and an approved Arabic header/body pair. Focus the field in Arabic, then request an Afrikaans version before and after its first approved translation is published. Arabic shows its full pair. Afrikaans shows the default pair first and the new localized pair after publication and cache refresh. No form value changes. Fallback operates on a complete header/body pair. Only visible fields expose help and the field key retains its canonical value.

### Additional decisions

Address a help definition by site, stable document type, field key and help revision. Store its display variant, supported event, logical placement and localized header/body pairs. An authorized editor previews a draft as a target user before publishing. Resolve published help when rendering a field the current user can see. Invalidate cached renderings of changed definitions across languages and revisions. A renamed or removed field leaves an orphaned definition for the editor to repair.

The renderer supplies a keyboard-accessible trigger and dismissal, escapes authored text according to the configured content format, and associates the help with its field for assistive technology. Resolve the header and body from the same chosen language or fallback together. Free-text field values and field identifiers never become translation keys.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/snd_tooltip.md).
