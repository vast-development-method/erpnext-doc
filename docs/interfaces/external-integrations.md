# External integrations

## Integration boundary

External services supply exchange rates, lead submissions, communications, telephony events, enrichment information, and structured business documents. Each integration must identify its external account, related local record, incoming or outgoing message identity, permitted operation, last outcome, and error evidence. A remote success, a queued local operation, and a committed business document are distinct outcomes. The following contracts describe reviewed customer-facing integrations; a complete connector inventory also requires the machine-readable source catalogs and further endpoint review.

In the combined application, contact, organisation, customer role, and product identity should be shared. The source's synchronisation logic is evidence of field ownership and conflict decisions. The replacement need not reproduce a separate internal transport between overlapping commercial modules, but it must preserve those decisions when importing external data or exposing compatible views.

## Product catalogue reconciliation

The reviewed catalogue coupling links each detailed stock product with its commercial catalogue product in both directions. Fields mirrored from the stock product include product name, standard rate, image, disabled state, and description. A price-list rate for the configured selling list and product stock unit is preferred over standard rate; standard rate is the fallback. An absent rate is normalised to zero before persistence. Updates compare candidate and current values and avoid an unnecessary write when unchanged.

Detailed-product-to-commercial-catalogue synchronisation is enabled only under its configured integration conditions. The reverse direction is an additional option because commercial catalogue records do not express all tax detail required by the detailed product model. In a unified implementation, this is a reason to keep authoritative tax and inventory attributes separate from a reduced sales-facing product view, not a reason to discard those attributes.

Renaming checks for an unrelated target identity before cascading. Merging reuses the appropriate surviving linked record when it exists. A recursion guard prevents mutual rename or delete callbacks looping indefinitely. Deletion clears the reverse link before removing the related catalogue record. An unrelated product with a coincidentally matching new name must not be overwritten. Evidence: `source-artifact-70fb25057f33e3ea221c lines 1–120`. Evidence: `source-artifact-a936e6adbe0440c73bc8 lines 1–102`.

## Exchange-rate service

The rate service accepts source currency, destination currency, and optional date. Without date it requests the latest rate. Latest-rate caching includes today's date in the cache identity so that a subsequent day misses the previous daily cache. Historical requests use the supplied date. Source and destination currencies also participate in the cache identity.

Two configured free provider families can fall back to one another. Configured paid provider families fail explicitly instead of silently changing source. A provider requiring a key rejects missing credentials. Requests use bounded timeouts. Successful values are cached; failure produces an error with the requested pair and date. User-facing guidance can distinguish an administrator able to change provider settings from a salesperson who must ask a manager.

The opportunity stores the selected exchange rate and refreshes it when currency changes or its rate is absent. This snapshot matters: later external-rate changes must not silently rewrite historical forecast values. Equally, this sales-facing latest-rate service is not proof that accounting uses the same lookup date or provider policy. Evidence: `source-artifact-b0ff0e4c1a4c46dc7235 lines 1–156`. Evidence: `source-artifact-db8bdef1a4a17da375a2 lines 79–317`.

## Lead acquisition service

An acquisition source has enabled state, source kind, credential, selected external page/form, interval setting, and last synchronised timestamp. Reject two enabled sources for the same external form. Manual synchronisation dispatches background work in normal operation. The worker maps configured external form questions to local lead fields, retains external form and lead identities, and records the acquisition source.

External fields with multiple values contribute their first value in the inspected worker. Duplicate detection compares mapped business fields plus form identity; it is not solely an external lead identifier check. Duplicate and failed creation outcomes are logged separately with retained incoming payload. A failed lead does not abort all remaining leads. The last-synchronised timestamp advances after processing the fetched batch, even if individual records failed. Recovery therefore depends on retrying failure records, not simply expecting the next incremental fetch to include them. Evidence: `source-artifact-33acdf19cd7cfeda31c1 lines 33–69`. Evidence: `source-artifact-7e89aad25103a92a3c71 lines 35–140`.

The inspected fetch requests a large maximum count and does not implement subsequent-page traversal. Its incremental filter requests external creation timestamps strictly greater than the last local synchronisation time. This leaves pagination, clock skew, and equal-boundary arrivals as concrete compatibility and reliability gaps. A proposed reliable replacement uses external message identity for duplicate control, consumes every continuation page, and advances a replayable checkpoint only after every item has a durable outcome. Those improvements must be labelled additions rather than assertions about the current worker.

## Website enrichment

Enrichment is best effort and must not prevent a lead, organisation, or opportunity from being created. It is enabled by settings, record kind, automatic-enrichment preference, and a nonempty website. Work is queued after the originating record commits; automatic and manual requests share a per-record job identity that suppresses duplicate simultaneous work. The timeout is derived from maximum pages multiplied by request timeout plus sixty seconds. The job reports progress and outcome rather than implying immediate completion.

Copying enrichment from an already enriched organisation fills empty fields and preserves user-entered values. Independently created organisations and opportunities can each have an enrichment run; those runs are not proof of one atomic shared operation. A replacement should retain provenance, execution time, and override decisions for enrichment values. Detailed crawling permissions, website retrieval safety, extraction priorities, and every field mapping require further contract review. Evidence: `source-artifact-9471c93c1218226e7620 lines 100–155`. Evidence: `source-artifact-3e53fa8646ba204bfd0a lines 80–580`. Evidence: `source-artifact-db8bdef1a4a17da375a2 lines 79–317`.

## Telephony and callback behaviour

Browser-based calling requires a configured telephony account and a phone identity associated with the caller. Missing phone identity returns a structured failure; an enabled integration alone does not make every user callable. Incoming or outgoing calls produce a call log, which links a matching contact number to a lead, opportunity, or contact as available. Subsequent events update duration, beginning and ending timestamps, call state, and recording location.

The inspected browser-telephony callback validation compares the supplied external account identifier, and for outgoing voice instructions an application identifier, against configuration. That check is observable, but it does not by itself establish cryptographic request-signature verification. Another telephony callback uses a configured shared verification token supplied with the request and rejects missing or mismatching values. Do not describe either callback as cryptographically authenticated beyond the actual check shown in its evidence. Evidence: `source-artifact-992fe366322e35f9aa38 lines 1–185`. Evidence: `source-artifact-a8e8fac895b7caa5ddb5 lines 182–190`.

A call-log creation failure rolls back that attempt, records an error, and returns spoken failure instructions rather than issuing normal call instructions. Call-record updates can fetch provider state and preserve its duration and timestamps. Provider-specific statuses map to local display states, but a complete mapping and the ordering policy for delayed or duplicate callbacks require dedicated acceptance fixtures. Secret-bearing request fields must be excluded from ordinary audit displays as a proposed security requirement.

## Campaign communications

A scheduled campaign associates a campaign template, recipient kind and identity, sender, beginning, ending, and campaign state. Its ending date is beginning plus the maximum scheduled send delay. A campaign requires at least one schedule. The same campaign and recipient cannot have a second scheduled or in-progress instance. Future beginning means scheduled; beginning through ending inclusive means in progress; later means completed.

Sending selects in-progress campaigns and schedule entries whose relative send date equals today. For a mailing group, exclude unsubscribed members. For a lead or contact, require an electronic mail address. Templates render against the recipient or group context, and the operation creates communication evidence and queues delivery. The inspected flow processes failures per campaign and continues. It does not independently prove exactly-once delivery when the daily job is retried. Proposed acceptance must test duplicate scheduling and provider acknowledgements without treating queued mail as delivered. Evidence: `source-artifact-46c47e21ceb256d60219 lines 32–210`.

## Acceptance and unresolved connector coverage

Required integration tests include unavailable rate provider with permitted fallback, paid-provider failure without fallback, date-specific cache identity, conflicting product rename, unchanged mirrored values, repeated lead payload, partial lead failure, page continuation, late arrival at checkpoint, overlapping enrichment requests, missing caller phone identity, wrong callback account or token, repeated call-status event, and campaign unsubscribe.

This review did not call external providers or execute live delivery. Messaging channels beyond the reviewed telephony and electronic mail paths, external business document interchange, every payment or banking connector, and complete national invoice transports remain separate contract work items. They must be tracked rather than inferred from the presence of connector settings or a source file.
