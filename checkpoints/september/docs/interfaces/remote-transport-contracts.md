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

The [method admission matrix](#method-admission-matrix) specifies the exact admitted method tokens and the meaning of each successful result. Record update uses overlay semantics even when the method is replacement-shaped.

## Authentication and request integrity

A session cookie can establish a user. Credential-pair or bearer-token authorization and registered authentication hooks provide additional authentication paths. Credential pairs require an enabled principal and matching protected secret. Failed authorization does not become an anonymous success merely because an endpoint happens to exist. Guest access requires an explicit guest-enabled operation or route-specific policy.

A state-changing session request normally supplies the session's cross-site request-forgery token. The reviewed implementation also admits configured allowed referrers and has absence/bypass branches, so compatibility depends on the selected security profile. Transport adapters should give the token a fully named neutral field/header and document its mapping. User source-address restrictions and any delegated-identity rules apply independently from document permissions.

Only explicitly exposed document methods can be called remotely. The route also enforces the registered method set and read/write preliminary permission. Arbitrary internal helper names must not be callable by sending a method string. Incoming internal document flags are removed on generic update and bulk update so a caller cannot directly request ignored permissions through those paths.

The [permission decision inputs](../runtime/identity-permissions-and-tenancy.md#permission-decision-inputs) distinguish identity establishment, preliminary operation access, record authority, and field exposure. Exposed registration does not bypass those layers.

## Listing, filtering, and pagination

The collection request accepts a list of selected fields, a filter list or object, ordering text, starting offset, maximum count, optional grouping, and object/list representation preference. The source validates the principal argument shapes before query construction. Permission-aware query building must validate fields, operators, and grouping rather than inserting caller-supplied expressions into unrestricted storage queries.

The default maximum count is twenty and default starting offset is zero. Fetching twenty-one rows internally for a twenty-row request establishes the continuation flag. The first twenty are returned; the extra row is not exposed twice. A separate count operation computes the permitted count. Stable ordering matters across pages: offset pagination does not guarantee a fixed snapshot while other users insert or change rows. A replacement must not claim cursor or snapshot semantics that this interface does not provide.

A document-specific query extension can replace the base query with a compatible executable query. Its failure is surfaced as an operation error. The extension must preserve authorization and the expected returned shape. Filters applied only in a browser cannot satisfy this contract.

The [request normalization rules](#request-normalization-and-numeric-defaults) specify absent, zero, malformed, and string-valued inputs separately, including the twenty-row continuation boundary.

## Success and failure representations

A normal nonnull service return is placed in a data member, including zero, false, empty text, and empty collections. Document-action invocations can also return an updated documents collection. Listing includes a next-page indicator. Bulk operations return a completed per-item result or an accepted job reference. A native file response can bypass ordinary object wrapping and provide content, media type, filename, and disposition.

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

The [two compatibility profiles](#two-compatibility-profiles) define message-versus-data success wrapping and error-envelope differences. Additional concurrency and unavailable-service classifications are listed in the [failure mappings](#additional-failure-mappings).

## Upload assembly and attachment result

Upload accepts a target reference, target field, privacy flag, folder, filename, raw file content or file location, optional existing-file reference, and optional post-upload processing. It defaults to private. Guest upload requires explicit settings permission, optionally narrowed by a document-type allowlist. An authenticated upload verifies target write permission; library reuse also verifies access to the existing file.

Chunked upload supplies zero-based chunk index, total chunk count, byte offset, and total expected size. The reviewed implementation writes a temporary file based on the safe filename and privacy location. It returns early until accumulated size reaches the declared size and the current chunk is the final chunk. It then reads the assembled content and creates the file record. This is the observed assembly protocol, not a guarantee of resumable, independently addressable upload sessions. Concurrent same-name uploads, repeated chunks, interrupted finalization, and offset behavior need explicit tests before stronger guarantees are claimed.

An optional image optimization stage can change content. Guest and website-facing users have content-type restrictions. A custom upload operation must itself be exposed and valid for the request method. After-upload extensions run before the resulting attachment is saved. The completed response is a file record; an intermediate response does not establish an attachment association.

The [attachment assembly example](#attachment-assembly-boundary-example) defines the ordered chunk protocol and its intermediate result; arbitrary out-of-order replacement and duplicate-safe resumption are additional capabilities.

## Real-time and asynchronous interaction

A background operation can return accepted status 202 with a job identifier. Clients then observe tracked job or submission status and reload the affected document on completion. An accepted response is not proof of successful submission. The generic bulk threshold defaults to more than twenty items; configuration can alter that threshold. Per-item completed results include successes, failures, and counts even when the outer request succeeds.

Live subscriptions distinguish document type, document, user, and task progress audiences. Document access is checked before joining a document channel. Ordinary document update messages follow commit, but progress can precede commit and live delivery can be lost. Clients must recover through permission-checked reads. The reviewed task channel does not provide the same ownership check as the document channel, so the interface cannot promise confidential task messages solely because a task identifier exists.

Outgoing event delivery is an independent interface. Its configured destination receives a serialized payload and optional signature. Retry can repeat a remotely accepted request. Both sides must use a durable business reference for operations where duplicate processing would change financial balances. Transport retry policy and business idempotency must be documented separately.

Accepted work, task progress, committed mutation, and external delivery must remain separate outcomes. The [work-state table](../runtime/background-work-and-consistency.md#work-state-and-financial-meaning) defines their financial meaning.

## Adapter acceptance obligations

The adapter must pass the same domain acceptance cases through remote and local service paths. Minimum transport cases are: unauthenticated access to an authenticated operation; valid credentials for a disabled user; a forbidden method on an exposed action; inaccessible fields in read and action responses; invalid filter shape; exact twenty-row pagination; duplicate identifier; stale modification timestamp; failed submitted edit; partial-success batch; asynchronous batch acceptance; intermediate upload; lost live completion event; and a retried external delivery accepted only once by its receiving business process.

Every changed literal route or field name belongs in an explicit mapping catalogue. The names in this document describe operations and do not require an implementation namespace, source application name, or programming language.

## Method admission matrix

The following method tokens are standardized wire literals. They are retained exactly because spelling changes would change the protocol.

| Operation | Admitted methods in the newer record profile | Response meaning |
| --- | --- | --- |
| List collection | `GET`, `QUERY` | Permission-filtered collection and continuation flag |
| Create root | `POST` | Inserted document after successful service execution |
| Read document | `GET` | Authorized current representation |
| Copy document | `GET` | Unsaved document copy |
| Update document | `PATCH`, `PUT` | Both use the loaded-document overlay/save path |
| Delete document | `DELETE` | Status 202 after synchronous deletion call |
| Stored document action | `GET`, `POST`, `QUERY` | Exposed action result; action's own allowed-method check also applies |
| Supplied document action | `GET`, `POST`, `QUERY` | Result plus permitted modified in-memory document |
| Bulk update or delete | `POST` | Completed partial result or status 202 with job identity |
| Effective metadata | `GET` | Definition under metadata-discovery authorization |
| Count | `GET`, `QUERY` | Permitted count |
| Upload or logout | `POST` | Completed attachment, intermediate upload absence, or completed logout |
| Named service | Its explicitly registered methods | Domain-specific result and checks |

Calling `PUT` does not establish replacement-of-every-scalar semantics here: this implementation overlays the loaded document just as its `PATCH` path does. Sending a complete child collection still replaces that collection's membership. An adapter that chooses conventional full replacement for `PUT` must declare the difference.

## Two compatibility profiles

The system exposes an older resource profile and a newer document profile. They share business operations but are not interchangeable wire contracts.

| Behavior | Older resource profile | Newer document profile |
| --- | --- | --- |
| Named service return | Return value appears in a message member | Return value appears in a data member |
| Empty string, zero, false, or empty collection return | Preserved when return is not null | Preserved when return is not null |
| Null service return | Does not create the return-value member | Does not create the return-value member |
| List pagination | Offset and page-length parameters, default twenty | Starting offset and limit, default zero and twenty; fetches one extra for continuation |
| String Boolean query options | Explicit string-to-Boolean conversion for selected options | General truthiness for selected options, so a nonempty string such as `"false"` is truthy |
| Read link expansion | Optional expansion to authorized linked documents | Ordinary read keeps references, normalizing applicable integral fixed references to text |
| Update result | Returns document without the explicit newer post-save field-filter step | Explicitly applies field-level read filtering after save |
| Child deletion | Generic deletion path | Removes the row through its parent and saves the parent |
| Stored action result | Action's direct result | Action result plus authorized updated document collection |
| Error envelope | Error-type field with optional diagnostic text and messages | Errors collection with type, associated message, and conditional diagnostic detail |

Both exposed ordinary deletion profiles reject an absent record. In the newer child-deletion service, an inaccessible parent can deliberately surface as a missing child rather than reveal its existence through a permission error. A compatibility fixture must specify which profile it exercises.

## Request normalization and numeric defaults

A structured object request supplies named arguments. A structured list request becomes the request's data collection; this does not mean every operation accepts that list as its own required named argument. Unsupported top-level values fail request parsing. String-encoded fields and filters can be decoded according to the operation. A nonempty fields value must be a list, and nonempty filters must be an object or list. Empty values can bypass those shape checks and resolve through query defaults.

The newer list converts starting offset and limit through integral coercion. An absent offset becomes zero and an absent limit becomes twenty. Zero, negative, malformed, or exceptionally large supplied limits need profile-specific tests; the route does not impose a universal positive maximum in its own argument guard. A replacement may add bounded positive pagination as an explicit operational policy, but must not present that bound as a baseline fact.

For a requested limit of twenty, twenty permitted rows produce continuation false and twenty-one permitted rows produce twenty returned rows with continuation true. The denied rows do not count toward this determination. A result's continuation flag does not imply that the total is twenty-one, only that at least one additional permitted row existed for that query execution.

## Additional failure mappings

| Failure | Status number | Caller action |
| --- | ---: | --- |
| Classified query deadlock or lock-wait timeout | 508 | Retry only after applying the business operation's safe-repeat rules |
| Storage in read-only mode | 503 | Treat mutation as unavailable; do not infer successful posting |
| Queue overloaded | 503 | No successful queued-business completion can be inferred |
| Unsupported implemented capability | 501 | Surface a capability failure rather than a missing business record |

A raw storage exception that has not been converted to a classified concurrency exception can follow a different error branch. Thus 508 is a defined mapping for the classified errors, not a promise that every storage-layer failure uses it. Diagnostics are conditionally exposed; user-facing business messages must remain usable without diagnostic traces.

## Attachment assembly boundary example

A three-chunk upload carries chunk indices zero, one, and two, each with its declared offset, total chunk count three, and final expected byte size. The first chunk resets the temporary file; later chunks use append mode. Intermediate responses have no completed attachment result. Finalization requires both sufficient accumulated size and the final chunk index, after which assembled content is read and the attachment record is created.

Although offsets are supplied, append-mode writes do not establish arbitrary out-of-order chunk replacement. Repeating a later chunk can append bytes again, and simultaneous uploads sharing the same safe filename and privacy area can collide. The baseline is therefore an ordered assembly protocol. A stronger resumable protocol requires independently identified upload sessions, duplicate-chunk detection, total-size validation, and completion idempotency as explicit additions.

## Contract example for a completed batch

```json
{
  "data": {
    "updated": ["record-000001", "record-000003"],
    "failed": [
      {
        "name": "record-000002",
        "error": "Referenced warehouse does not exist"
      }
    ],
    "total": 3,
    "success_count": 2,
    "failure_count": 1
  }
}
```

The example preserves the newer profile's batch field spellings while using neutral identities and error wording. All input items have exactly one result category. Above the configured asynchronous threshold the result instead identifies accepted work; the client must await durable outcome before displaying those items as updated. The [service contract matrix](service-contracts.md#operation-contract-matrix) defines the transaction boundary independently of the response wrapper.
