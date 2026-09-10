# External integrations

## Integration boundary

External services supply exchange rates, lead submissions, communications, telephony events, enrichment information, and structured business documents. Each integration must identify its external account, related local record, incoming or outgoing message identity, permitted operation, last outcome, and error evidence. A remote success, a queued local operation, and a committed business document are distinct outcomes. The following contracts describe reviewed customer-facing integrations; a complete connector inventory also requires the machine-readable source catalogs and further endpoint review.

In the combined application, contact, organisation, customer role, and product identity should be shared. The source's synchronisation logic is evidence of field ownership and conflict decisions. The replacement need not reproduce a separate internal transport between overlapping commercial modules, but it must preserve those decisions when importing external data or exposing compatible views.

## Product catalogue reconciliation

The reviewed catalogue coupling links each detailed stock product with its commercial catalogue product in both directions. Fields mirrored from the stock product include product name, standard rate, image, disabled state, and description. A price-list rate for the configured selling list and product stock unit is preferred over standard rate; standard rate is the fallback. An absent rate is normalised to zero before persistence. Updates compare candidate and current values and avoid an unnecessary write when unchanged.

Detailed-product-to-commercial-catalogue synchronisation is enabled only under its configured integration conditions. The reverse direction is an additional option because commercial catalogue records do not express all tax detail required by the detailed product model. In a unified implementation, this is a reason to keep authoritative tax and inventory attributes separate from a reduced sales-facing product view, not a reason to discard those attributes.

Renaming checks for an unrelated target identity before cascading. Merging reuses the appropriate surviving linked record when it exists. A recursion guard prevents mutual rename or delete callbacks looping indefinitely. Deletion clears the reverse link before removing the related catalogue record. An unrelated product with a coincidentally matching new name must not be overwritten. Preserve those field ownership and conflict decisions even when one unified product record replaces internal mirroring. The [neutral integration record contract](#neutral-integration-record-contract) separates the business result from its transport attempt.

## Exchange-rate service

The rate service accepts source currency, destination currency, and optional date. Without date it requests the latest rate. Latest-rate caching includes today's date in the cache identity so that a subsequent day misses the previous daily cache. Historical requests use the supplied date. Source and destination currencies also participate in the cache identity.

Two configured free provider families can fall back to one another. Configured paid provider families fail explicitly instead of silently changing source. A provider requiring a key rejects missing credentials. Requests use bounded timeouts. Successful values are cached; failure produces an error with the requested pair and date. User-facing guidance can distinguish an administrator able to change provider settings from a salesperson who must ask a manager.

The opportunity stores the selected exchange rate and refreshes it when currency changes or its rate is absent. This snapshot matters: later external-rate changes must not silently rewrite historical forecast values. Equally, this sales-facing latest-rate service is not proof that accounting uses the same lookup date or provider policy. The [exchange-rate identity example](#exchange-rate-identity-example) fixes pair, direction, and date as separate lookup inputs; historical business snapshots do not inherit later provider changes.

## Lead acquisition service

An acquisition source has enabled state, source kind, credential, selected external page/form, interval setting, and last synchronised timestamp. Reject two enabled sources for the same external form. Manual synchronisation dispatches background work in normal operation. The worker maps configured external form questions to local lead fields, retains external form and lead identities, and records the acquisition source.

External fields with multiple values contribute their first value in the inspected worker. Duplicate detection compares mapped business fields plus form identity; it is not solely an external lead identifier check. Duplicate and failed creation outcomes are logged separately with retained incoming payload. A failed lead does not abort all remaining leads. The last-synchronised timestamp advances after processing the fetched batch, even if individual records failed. Recovery therefore depends on retrying failure records, not simply expecting the next incremental fetch to include them. The [acquisition checkpoint example](#acquisition-checkpoint-example) specifies how successful and failed records coexist with an advanced checkpoint, so recovery does not require re-reading an unavailable implementation.

The inspected fetch requests a large maximum count and does not implement subsequent-page traversal. Its incremental filter requests external creation timestamps strictly greater than the last local synchronisation time. This leaves pagination, clock skew, and equal-boundary arrivals as concrete compatibility and reliability gaps. A proposed reliable replacement uses external message identity for duplicate control, consumes every continuation page, and advances a replayable checkpoint only after every item has a durable outcome. Those improvements must be labelled additions rather than assertions about the current worker.

## Website enrichment

Enrichment is best effort and must not prevent a lead, organisation, or opportunity from being created. It is enabled by settings, record kind, automatic-enrichment preference, and a nonempty website. Work is queued after the originating record commits; automatic and manual requests share a per-record job identity that suppresses duplicate simultaneous work. The timeout is derived from maximum pages multiplied by request timeout plus sixty seconds. The job reports progress and outcome rather than implying immediate completion.

Copying enrichment from an already enriched organisation fills empty fields and preserves user-entered values. Independently created organisations and opportunities can each have an enrichment run; those runs are not proof of one atomic shared operation. A replacement should retain provenance, execution time, and override decisions for enrichment values. Detailed crawling permissions, website retrieval safety, extraction priorities, and every field mapping require further contract review. An enrichment failure is a separate operational outcome: retain the already committed lead or organisation and preserve its user-entered values. Proposed extra provenance fields must be identified as additions when the baseline does not retain them.

## Telephony and callback behaviour

Browser-based calling requires a configured telephony account and a phone identity associated with the caller. Missing phone identity returns a structured failure; an enabled integration alone does not make every user callable. Incoming or outgoing calls produce a call log, which links a matching contact number to a lead, opportunity, or contact as available. Subsequent events update duration, beginning and ending timestamps, call state, and recording location.

The inspected browser-telephony callback validation compares the supplied external account identifier, and for outgoing voice instructions an application identifier, against configuration. That check is observable, but it does not by itself establish cryptographic request-signature verification. Another telephony callback uses a configured shared verification token supplied with the request and rejects missing or mismatching values. Do not describe either callback as cryptographically authenticated beyond the actual check shown in its evidence. The [telephony status mapping](#telephony-status-mapping) defines the actual status normalization and overwrite rules. Account matching, shared-token checking, and cryptographic signature validation are different authentication contracts.

A call-log creation failure rolls back that attempt, records an error, and returns spoken failure instructions rather than issuing normal call instructions. Call-record updates can fetch provider state and preserve its duration and timestamps. Provider-specific statuses map to local display states, but a complete mapping and the ordering policy for delayed or duplicate callbacks require dedicated acceptance fixtures. Secret-bearing request fields must be excluded from ordinary audit displays as a proposed security requirement.

## Campaign communications

A scheduled campaign associates a campaign template, recipient kind and identity, sender, beginning, ending, and campaign state. Its ending date is beginning plus the maximum scheduled send delay. A campaign requires at least one schedule. The same campaign and recipient cannot have a second scheduled or in-progress instance. Future beginning means scheduled; beginning through ending inclusive means in progress; later means completed.

Sending selects in-progress campaigns and schedule entries whose relative send date equals today. For a mailing group, exclude unsubscribed members. For a lead or contact, require an electronic mail address. Templates render against the recipient or group context, and the operation creates communication evidence and queues delivery. The inspected flow processes failures per campaign and continues. It does not independently prove exactly-once delivery when the daily job is retried. Proposed acceptance must test duplicate scheduling and provider acknowledgements without treating queued mail as delivered. A campaign's scheduled send date, unsubscribe state, communication record, queue state, and observed delivery are separate facts. Re-running a daily schedule must be tested for repeated delivery; a completed campaign date range alone proves no exactly-once guarantee.

## Acceptance and unresolved connector coverage

Required integration tests include unavailable rate provider with permitted fallback, paid-provider failure without fallback, date-specific cache identity, conflicting product rename, unchanged mirrored values, repeated lead payload, partial lead failure, page continuation, late arrival at checkpoint, overlapping enrichment requests, missing caller phone identity, wrong callback account or token, repeated call-status event, and campaign unsubscribe.

This review did not call external providers or execute live delivery. Messaging channels beyond the reviewed telephony and electronic mail paths, external business document interchange, every payment or banking connector, and complete national invoice transports remain separate contract work items. They must be tracked rather than inferred from the presence of connector settings or a source file.

## Neutral integration record contract

Each connector's business contract separates configuration, transport event, processing attempt, and resulting business document.

| Information group | Required meaning |
| --- | --- |
| Configuration | Enabled capability, external account, company scope, endpoint, protected credential reference, mapping version |
| Incoming identity | External event or record identity, external creation time, received time, local acquisition source |
| Outgoing identity | Originating document reference, triggering business event, retained payload and destination |
| Attempt | Attempt number, start/end time, transport result, semantic outcome, failure classification |
| Business result | Created or updated local record identity, permitted no-op, rejected item, or unresolved acknowledgement |
| Checkpoint | Last processed acquisition boundary and recovery information for failed records |
| Privacy | Authorized payload fields, retained secret exclusions, attachment access, diagnostic exposure |

These are specification requirements for a complete connector contract, not a claim that every existing connector persists every field. Where the baseline retains less information, the replacement must declare how it resolves duplicate delivery and uncertain outcomes. A generic successful network response is insufficient evidence of a committed local or external financial transaction.

## Telephony status mapping

The browser-calling adapter converts provider status by replacing hyphens with spaces and capitalizing the words. Thus `in-progress` becomes In Progress and `no-answer` becomes No Answer; an absent status becomes an empty value. This is a string normalization contract, not a validated finite progression state machine.

The shared-token telephony adapter uses a more specific mapping:

| Direction or call condition | Provider state | Local state |
| --- | --- | --- |
| Outgoing initiated through the provider interface or dial operation | `completed` | Completed |
| Same outgoing conditions | `in-progress` | In Progress |
| Same outgoing conditions | `busy` | Ringing |
| Same outgoing conditions | `no-answer` | No Answer |
| Same outgoing conditions | `failed` | Failed |
| Incomplete call | `no-answer` | No Answer |
| Caller hung up | `canceled` | Canceled |
| Incomplete call | `failed` | Failed |
| Completed call kind | Any remaining state | Completed |
| Remaining call with busy state | `busy` | Ringing |
| Other incoming condition | Dial state when supplied, otherwise general state | Retain selected state |

Call lookup uses external call identity. An update can replace destination number because a call may be redirected; dialled destination takes priority over the ordinary destination. Duration prefers dial-call duration, then conversation duration, then zero. Recording location becomes empty when absent from the incoming update. Start and end times are set from the callback. These overwrite rules mean a later incomplete callback can remove previously known information; monotonic preservation of terminal state or nonempty recording is not an established baseline guarantee. Tests for reordered and repeated callbacks must therefore specify the intended compatibility or corrected policy explicitly.

## Acquisition checkpoint example

A fetched acquisition batch contains records A, B, and C. A and C create local leads; B fails a required-field check. The worker retains B's failed payload and can still advance its last-synchronized time after processing the batch. The next incremental fetch requests external creations strictly after that checkpoint and may never return B again. Operational recovery must therefore retry B from its retained failure information. Rewinding the checkpoint without duplicate handling can also replay A and C.

The baseline's first-value mapping for multivalued external fields loses subsequent values. A replacement that retains every supplied phone number must declare that richer mapping. Similarly, consuming all continuation pages and using external lead identity as durable duplicate protection are explicit reliability additions to the inspected acquisition worker, not behavior that can be inferred from a large page-size request.

## Exchange-rate identity example

Requesting source currency A to destination currency B for 15 January is a different cache identity from the same pair for 16 January, from B to A on 15 January, and from a latest-rate request after the calendar day changes. A provider failure under a paid configuration is not silently converted into another provider's rate. The stored opportunity exchange rate is a transaction input for its forecast; the accounting currency rules independently determine posting conversion and revaluation.

## Financial connector completion conditions

An integration that creates a payment, bank transaction, supplier invoice, or statutory filing must state who owns the external reference, whether repeated notification is a no-op or another event, which business service performs the mutation, how company/currency/amount are validated, and how pending, accepted, settled, rejected, reversed, and unknown acknowledgement differ. It must retain enough information to reconcile the local voucher to the external transaction.

These conditions link financial integrations to [treasury and reconciliation](../domains/treasury-and-reconciliation.md), [accounts payable](../domains/accounts-payable.md), and [regional capabilities](../domains/regional-and-specialised-capabilities.md). A connector entry lacking these details remains incomplete even if its endpoint and credentials are listed. Do not invent country-specific fiscal behavior from a generic network adapter.

## Callback and delivery acceptance

For each connector, provide fixtures for wrong credentials or account, disabled configuration, valid initial message, repeated message, unknown parent reference, partial mapping failure, out-of-order status, network timeout after acceptance, retry exhaustion, and recovery. A receiver that returns success before durable business processing must expose a later terminal outcome. If its acknowledgement is durable, deduplicate the repeated business reference before creating another financial effect. The outgoing retry schedule and commit boundary are defined in [background work and consistency](../runtime/background-work-and-consistency.md#retry-schedule-and-duplicate-boundaries).
