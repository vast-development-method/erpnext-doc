# Batch conversion, portal parties, calls and exchange codes

## Convert business documents in bulk

| Source | Draft targets in core |
|---|---|
| Quotation | Sales order, sales invoice |
| Sales order | Sales invoice, delivery note, payment entry |
| Sales invoice | Delivery note, payment entry |
| Delivery note | Sales invoice, packing slip |
| Supplier quotation | Purchase order |
| Purchase order | Purchase invoice, purchase receipt, payment entry |
| Purchase invoice | Purchase receipt, payment entry |
| Purchase receipt | Purchase invoice |

Require read permission on source kind, create permission on target kind, and read access to **each actual source identity before enqueuing anything**. Reject missing or non-string identities. Read current statuses from storage. Skip On Hold and Closed; return immediately if all are skipped. A background job processes the remainder with one savepoint per source. A converter returning a document sets its title and inserts a draft under the bulk-validation rules. Ordinary posting validations still belong to submission. A converter returning no object without raising can produce a Success log with no inserted target. An extension's mapper can replace an entire source's set of target mappings.

Within the batch roll back the failing source to its savepoint, preserve successful work, write source name, kinds, day, status and diagnostics, and expose complete/partial/failed outcome. A System Manager retry selects Failed entries by date with retried flag clear. If a success for the same source identity and kind pair was modified after the failure was created, mark the failure retried and keep its Failed status. Otherwise run the converter again at a savepoint. Mark success or failure and consume the retry flag. The retry input carries no original conversion arguments. Distinguish skip-on-later-success from a uniqueness guarantee under concurrent requests.

## Bind a portal identity

On role synchronization, look up the contact's primary email and inspect its typed party links to grant missing Customer/Supplier roles; reentry and migration bypass this path. On session creation consider only Website Users when the configured portal default is Customer or Supplier and the user actually has that role. If the contact resolved by primary email already links that party kind, leave it alone. Otherwise create an individual party using the full name, then a contact, a primary email row and typed link to that party. A user who also has the opposite party kind gets a suffixed contact display name. The existence predicate resolves one contact by email, so ambiguous duplicate contacts warrant an integration fixture. Website role, contact identity, party identity and authorization to individual transactions remain separate.

## Route calls and retain the service history

A communication medium owns a channel, provider, optional catch-all group and availability rows. Reject a slot with start at or after end; represent overnight coverage with separate day slots. On call insertion use incoming source or outgoing destination to locate contact/lead telephone matches. Add each matching contact and lead, customer links found via contacts, and the receiving employee for incoming calls. Deduplicate dynamic links. Normalize stored and incoming numbers to a bounded digit key before accepting a broad search match.

For an incoming call, popup recipients are the intersection of scheduled active employee users and destination-number matches. A destination change while the new state is nonterminal sends a missed notification to prior recipients and opens the new popup. A transition from nonterminal into No Answer, Completed, Busy or Failed sends an end notification to the old agent set even when its duty period has ended. A summary write requires read access plus either receipt by the current employee user or ordinary write access; an optional call type must be submitted. Add the saved summary to the timeline. The supplemental Employee-role record predicate permits a row if a receiver is assigned, if employee user equals caller, or if another eligible read role grants unrestricted access. It therefore does not implement a simple per-agent-only rule. Apply standard document authorization alongside this additional predicate.

## Resolve exchange codes by publisher and version

An exchange code list has a **canonical URI** shared across versions and a **canonical version URI** identifying a particular installed list. Keep each code's exact textual value, display fields and typed business-record mappings. The default code must belong to that list. Resolve an exact list identity first; otherwise retrieve versions for the canonical URI and choose the maximum using numeric segments (version 10 sorts above 3). An unresolvable list returns no matches. Within one list a business-record identity cannot map to competing codes. The same record may have a different code in another version. Forward lookup returns distinct code values; reverse lookup returns linked names in link-row order.

List import has two stages. Require permission to create code lists before accepting uploaded bytes or a readable local attachment. Identify the version, validate it against an existing selected document, extract metadata, save the list and attach the original file privately. Return column identifiers, preview values and low-cardinality filter choices. Stage two requires create access for common codes, read access to the named list and file, and a code column. Match rows satisfying **all** supplied column/value filters. Missing row code is an error. Re-import matches exact code text within the list and updates that row; case-distinct spellings can remain distinct. Preserve each row's source data, expose progress/count and leave rows absent from this import alone. List deletion clears the default reference and deletes the owned common codes. This dictionary translates identifiers; generating or transmitting an invoice is a separate operation.

## Seed country-specific setup

Country address template setup discovers built-in country formats, sets the default marker on the configured country and creates/updates each known country's template. A missing country is logged and skipped. Australia supplies six company-scoped category-to-template tax-rule seeds covering capital, import/GST free and domestic purchases, plus domestic, export and GST-free sales. These are configuration records: the actual rate and posting accounts belong to the selected company template. An empty country configuration creates no country-specific entries.
