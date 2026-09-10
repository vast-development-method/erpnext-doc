# Remote transport contracts

This blueprint describes the current record-oriented remote interface through neutral operation names. A replacement can select route spelling, host structure, and implementation technology. Renaming a route, request field, or signature header is a deliberate adapter change; it is not byte-for-byte compatibility with an existing consumer. Business equivalence means preserving authorization, validation, results, state transitions, and financial effects behind that adapter.

## Request envelope and method semantics

The current interface supports structured request bodies and query arguments. An object body becomes named arguments; a list body is available as a data collection. Other top-level argument types are invalid. Tenant context, session restoration, request language, cross-site request-forgery checks, and authentication are established before dispatch. Per-operation authorization follows dispatch.

| Operation category | Accepted transport meaning | Mutation expectation |
| --- | --- | --- |
| List collection | Retrieval or query | No ordinary commit |
| Read one document | Retrieval | No ordinary commit |
| Create document | Submission | Commit on success |
| Update document | Partial replacement or replacement | Commit on success |
| Delete document | Deletion | Commit on success |
| Invoke stored or supplied document action | Retrieval, submission, or query | Depends on allowed method and invoked action |
| Invoke named service | Methods explicitly registered for that service | Depends on method and service |
| Upload attachment | Submission | Commit completed attachment on success |
| Logout | Submission | Explicitly persists logout |

The generic exposed-operation registration defaults to retrieval, submission, replacement, deletion, and query when a method list is absent. Explicit retrieval also enables query. The base request layer classifies retrieval, head-only retrieval, options discovery, and query as safe; submission, replacement, deletion, and partial replacement are state-changing. Safe successful requests normally roll back incidental database writes. A method named calculate or get is not sufficient evidence of safety, and a broadly registered function is not necessarily appropriate for every admitted method. Each catalogue entry should retain the actual allowed-method set.

Evidence: source-artifact-187d5fd72469df5def58 lines 29–113; source-artifact-66f1c84f2539463cb381 lines 580–655; source-artifact-70f793c473898fecc4cc lines 568–651; source-artifact-d8764548dbbd91bf1e51 lines 362–448.

## Authentication and request integrity

A session cookie can establish a user. Credential-pair or bearer-token authorization and registered authentication hooks provide additional authentication paths. Credential pairs require an enabled principal and matching protected secret. Failed authorization does not become an anonymous success merely because an endpoint happens to exist. Guest access requires an explicit guest-enabled operation or route-specific policy.

A state-changing session request normally supplies the session's cross-site request-forgery token. The reviewed implementation also admits configured allowed referrers and has absence/bypass branches, so compatibility depends on the selected security profile. Transport adapters should give the token a fully named neutral field/header and document its mapping. User source-address restrictions and any delegated-identity rules apply independently from document permissions.

Only explicitly exposed document methods can be called remotely. The route also enforces the registered method set and read/write preliminary permission. Arbitrary internal helper names must not be callable by sending a method string. Incoming internal document flags are removed on generic update and bulk update so a caller cannot directly request ignored permissions through those paths.

Evidence: source-artifact-187d5fd72469df5def58 lines 29–113; source-artifact-187d5fd72469df5def58 lines 642–775; source-artifact-70f793c473898fecc4cc lines 192–271; source-artifact-70f793c473898fecc4cc lines 274–562; source-artifact-66f1c84f2539463cb381 lines 580–655.

## Listing, filtering, and pagination

The collection request accepts a list of selected fields, a filter list or object, ordering text, starting offset, maximum count, optional grouping, and object/list representation preference. The source validates the principal argument shapes before query construction. Permission-aware query building must validate fields, operators, and grouping rather than inserting caller-supplied expressions into unrestricted storage queries.

The default maximum count is twenty and default starting offset is zero. Fetching twenty-one rows internally for a twenty-row request establishes the continuation flag. The first twenty are returned; the extra row is not exposed twice. A separate count operation computes the permitted count. Stable ordering matters across pages: offset pagination does not guarantee a fixed snapshot while other users insert or change rows. A replacement must not claim cursor or snapshot semantics that this interface does not provide.

A document-specific query extension can replace the base query with a compatible executable query. Its failure is surfaced as an operation error. The extension must preserve authorization and the expected returned shape. Filters applied only in a browser cannot satisfy this contract.

Evidence: source-artifact-70f793c473898fecc4cc lines 24–189; source-artifact-70f793c473898fecc4cc lines 192–271.

## Success and failure representations

A normal nonempty service return is placed in a data member. Document-action invocations can also return an updated documents collection. Listing includes a next-page indicator. Bulk operations return a completed per-item result or an accepted job reference. A native file response can bypass ordinary object wrapping and provide content, media type, filename, and disposition.

The newer error representation is an errors collection containing a semantic type and associated user messages. Trace details are conditional on diagnostic policy; they are not guaranteed in ordinary production responses. Messages can exist independently of errors. Clients must not treat an informational message as a failed transaction or treat the absence of a stack trace as success.

| Failure class | Reviewed status number |
| --- | ---: |
| Authentication failure or expired session | 401 |
| Permission denied | 403 |
| Record absent | 404 |
| Invalid name or duplicate identity | 409 |
| Unsupported media | 415 |
| General business validation, including stale document and submitted-field violation | 417 |
| Invalid cross-site request-forgery token | 400 |
| Rate limit exceeded | 429 |
| Unavailable service or stopped session service | 503 |
| Unexpected unclassified failure | 500 |

The unusual validation status 417 is an observed compatibility detail. Replacing it with another status is possible, but must be declared as an adapter difference. Deadlock and timeout errors have additional specialized mappings; the exact classification depends on the exception path, and a generic server error must not automatically trigger an unbounded financial retry. A retry is safe only when the operation's transaction and idempotency contract permits it.

Evidence: source-artifact-ad3e1733ffa0140eec53 lines 22–110; source-artifact-d0463fd237b31eada484 lines 39–67; source-artifact-4cd1b832463b23b11169 lines 24–170; source-artifact-d8764548dbbd91bf1e51 lines 362–448.

## Upload assembly and attachment result

Upload accepts a target reference, target field, privacy flag, folder, filename, raw file content or file location, optional existing-file reference, and optional post-upload processing. It defaults to private. Guest upload requires explicit settings permission, optionally narrowed by a document-type allowlist. An authenticated upload verifies target write permission; library reuse also verifies access to the existing file.

Chunked upload supplies zero-based chunk index, total chunk count, byte offset, and total expected size. The reviewed implementation writes a temporary file based on the safe filename and privacy location. It returns early until accumulated size reaches the declared size and the current chunk is the final chunk. It then reads the assembled content and creates the file record. This is the observed assembly protocol, not a guarantee of resumable, independently addressable upload sessions. Concurrent same-name uploads, repeated chunks, interrupted finalization, and offset behavior need explicit tests before stronger guarantees are claimed.

An optional image optimization stage can change content. Guest and website-facing users have content-type restrictions. A custom upload operation must itself be exposed and valid for the request method. After-upload extensions run before the resulting attachment is saved. The completed response is a file record; an intermediate response does not establish an attachment association.

Evidence: source-artifact-9d66d61a7b7d9a437d11 lines 130–261.

## Real-time and asynchronous interaction

A background operation can return accepted status 202 with a job identifier. Clients then observe tracked job or submission status and reload the affected document on completion. An accepted response is not proof of successful submission. The generic bulk threshold defaults to more than twenty items; configuration can alter that threshold. Per-item completed results include successes, failures, and counts even when the outer request succeeds.

Live subscriptions distinguish document type, document, user, and task progress audiences. Document access is checked before joining a document channel. Ordinary document update messages follow commit, but progress can precede commit and live delivery can be lost. Clients must recover through permission-checked reads. The reviewed task channel does not provide the same ownership check as the document channel, so the interface cannot promise confidential task messages solely because a task identifier exists.

Outgoing event delivery is an independent interface. Its configured destination receives a serialized payload and optional signature. Retry can repeat a remotely accepted request. Both sides must use a durable business reference for operations where duplicate processing would change financial balances. Transport retry policy and business idempotency must be documented separately.

Evidence: source-artifact-70f793c473898fecc4cc lines 274–562; source-artifact-e609b7de6b102f041400 lines 58–192; source-artifact-3d8f5f8af4a5a70b7faf lines 31–136; source-artifact-af5a18ab59f29558dded lines 36–138; source-artifact-c92b91c9ae73e577a3db lines 155–352.

## Adapter acceptance obligations

The adapter must pass the same domain acceptance cases through remote and local service paths. Minimum transport cases are: unauthenticated access to an authenticated operation; valid credentials for a disabled user; a forbidden method on an exposed action; inaccessible fields in read and action responses; invalid filter shape; exact twenty-row pagination; duplicate identifier; stale modification timestamp; failed submitted edit; partial-success batch; asynchronous batch acceptance; intermediate upload; lost live completion event; and a retried external delivery accepted only once by its receiving business process.

Every changed literal route or field name belongs in an explicit mapping catalogue. The names in this document describe operations and do not require an implementation namespace, source application name, or programming language.
