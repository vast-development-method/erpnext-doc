# Service contracts

This document defines transport-independent services of the record platform. Domain services build on them to perform business operations such as invoice submission, stock transfer, payment allocation, payroll posting, and customer conversion. Service identity is a complete semantic name; a transport adapter can map that identity to its chosen route without placing implementation-module names in the business model.

## Shared invocation context

Every invocation has a tenant, acting identity, operation name, request arguments, effective configuration, and transaction context. Mutations may carry an expected modification timestamp. Responses distinguish a service return value, updated authorized documents, user-facing messages, errors, progress, and durable completion state. A void return is different from a missing record and different from an empty result set.

Errors need stable semantic categories: authentication required or expired, permission denied, record absent, invalid name or duplicate identity, missing required value, invalid reference, reference to a cancelled transaction, invalid structural transition, stale document, immutable submitted field, locked document, unsupported content, throttling, and unexpected failure. Do not reduce all domain errors to false or zero. A numeric helper returning zero for malformed input does not define the error behavior of an invoice service.

Evidence: source-artifact-4cd1b832463b23b11169 lines 24–170; source-artifact-ad3e1733ffa0140eec53 lines 22–110; source-artifact-d0463fd237b31eada484 lines 39–67.

## Record retrieval and discovery

**Read document.** Input is document type and identifier. Load the document, check read permission, apply field-level filtering and masking, and return its authorized representation including owned children. Where a reference is physically integral, the current transport normalizes certain link values to text. The caller must preserve identity as a value rather than accidentally formatting it as a number with thousands separators.

**List documents.** Inputs are document type, selected fields, filter object or filter list, ordering, offset, limit, optional grouping, and representation preference. Default offset is zero and default limit is twenty. Validate that selected fields are a list and that filters are a list or object. Build a permission-aware query. A document-specific query provider may modify it and must return an executable query or no replacement. Fetch one extra row, return at most the requested limit, and expose whether another page exists. Count is a separate operation and is not implied by the continuation flag.

**Read effective metadata.** Return the effective type declaration for an authenticated principal admitted to the general authenticated-user role. This operation is not the same as read permission on every record of that type. Discovery additionally lists registered callable capabilities and their declared arguments. A neutral catalogue describes their behavior; it need not expose executable source bodies or internal module paths.

Evidence: source-artifact-70f793c473898fecc4cc lines 24–189; source-artifact-70f793c473898fecc4cc lines 192–271; source-artifact-70f793c473898fecc4cc lines 568–651.

## Document creation, copy, update, and deletion

**Create document.** Inputs are a route-selected document type and field values. The route type is authoritative over a redundant type field. Construct a new document with defaults, accept a supplied textual or integral identifier through the naming-set path where supported, and invoke insertion with its permission, naming, validation, child persistence, and event semantics. The return value is the created document representation. The reviewed creation operation returns the insertion representation directly; it does not visibly call the same field-filtering routine used by read/update. This serialization difference must be tested and explicitly resolved where newly supplied secrets or restricted fields are involved.

**Copy document.** Check read permission and filter fields before producing a clean unsaved copy. It does not insert or submit the copy. The operation's option controlling no-copy fields defaults to ignoring those no-copy restrictions in the reviewed transport. A domain conversion, amendment, and simple copy are therefore different services; each needs its own field mapping and identity rules.

**Update document.** Lock and load the existing record, remove incoming internal execution flags, overlay submitted data, and invoke the ordinary save. Return the authorized saved representation. If the target is a child, the parent is also saved afterward. The source loads the latest stored record first: an explicit expected modification timestamp is needed if the caller wants stale-edit rejection against its earlier read. Patch semantics for child collections follow complete table membership as described in the lifecycle document.

**Delete document.** Invoke document deletion and its permissions, reference checks, domain deletion rules, and deletion events. The transport acknowledges acceptance with status 202. That status alone does not imply background deletion; this particular operation performs the call synchronously before returning. Submitted cancellation and deletion are distinct operations.

Evidence: source-artifact-70f793c473898fecc4cc lines 192–271; source-artifact-1c79c95fe9c8ab1bc9d4 lines 691–768; source-artifact-1c79c95fe9c8ab1bc9d4 lines 812–944.

## Business action invocation

**Invoke action on stored document.** Load by type and identifier, verify the method is exposed, enforce its allowed request methods, and require read permission for retrieval/query invocation or write permission for submission invocation. Execute the document event-aware method dispatcher. Return both the service result and an updated, field-filtered document. The action itself can require submit, cancel, or other stronger permissions; transport write permission is only the preliminary gate.

**Invoke action on supplied document.** Accept a structured document and argument object, construct it using permission checks appropriate to the request method, retain its modification timestamp, and check current-version consistency. Verify that the requested method is exposed and allowed for that transport method, validate accepted arguments, invoke it, and return its result plus authorized updated document. This supports unsaved document calculations as well as operations on existing state. An in-memory calculation must not be mistaken for a durable save; the invoked method decides persistence.

**Invoke named service.** Resolve the operation override, optionally select a configured server-side operation, verify exposure and allowed method, bind validated arguments, and invoke the service. Named operations do not inherit a universal record permission rule because they might span records or return calculations. Each must enforce its documented authorization. Registry membership supplies reachability, not complete business authorization.

Evidence: source-artifact-70f793c473898fecc4cc lines 24–189; source-artifact-70f793c473898fecc4cc lines 192–271; source-artifact-70f793c473898fecc4cc lines 568–651; source-artifact-66f1c84f2539463cb381 lines 580–655.

## Bulk modifications

Bulk update and deletion accept either one document type with multiple records or a list carrying type and identifier per item. Identifiers must be text or integers; integers are normalized to text. A bulk-update item contains identifier and changed fields; internal flags are removed. Each update loads with a write lock and uses the normal save; each deletion uses the ordinary deletion service with missing-record errors enabled.

The default asynchronous threshold is twenty items. The comparison is strictly greater than the threshold: twenty executes inline under the default, twenty-one is queued. Configuration can provide a global value or a per-document-type mapping, with a separate fallback entry for operations spanning types. Crossing the threshold returns an accepted status and job identifier, not a completed success list.

Inline or worker execution makes a savepoint per item and records success or failure. The result includes successful identifiers, failed items with errors, attempted total, success count, and failure count. Every attempted item belongs to exactly one result category. These operations permit partial success; they do not promise all-or-nothing behavior across the entire batch. Callback and external-effect behavior around savepoint rollback is specified in the background consistency document.

Evidence: source-artifact-70f793c473898fecc4cc lines 24–189; source-artifact-70f793c473898fecc4cc lines 274–562.

## Operational import

Operational import is a current application capability, separate from historical application migration. It accepts tabular source data, maps columns to effective record fields, forms complete document payloads including children, presents warnings, and supports insert, update, or insert-or-update behavior. Blocking warnings prevent execution. Tree imports can resolve aliases to generated parent identifiers and order parent records before dependent children.

Insert builds a new document, applies import values, uses normal insertion, and can submit after import for submittable types. Update loads the identified record, applies values, and saves only when changes exist; a strict update without changes can report an error, while insert-or-update allows a no-change existing record. Each successful document payload is committed and logged with its source row indexes. Failure rolls back that payload and records error details. Previously imported row groups can be skipped during continuation. A parent with several children is one payload; row count is not necessarily document count.

Import must retain an audit reference to its import record and distinguish insert from update outcomes. It must not bypass all permissions simply because it is a bulk operation. Generic outgoing-event suppression during import is an observable difference from interactive entry.

Evidence: source-artifact-831cef801a36881fee0d lines 132–284; source-artifact-831cef801a36881fee0d lines 355–444; source-artifact-ac9f4042fec42828bb99 lines 5–117.

## Report and attachment services

A report invocation takes report identity, filters, optional custom columns, tree information, and prepared-result preference. It checks report visibility, reference-type report permission, and filter permissions. A disabled report fails. A prepared report can return stored report data, status, and attachments; an ordinary report executes its calculation. Totals-row inclusion is controlled by report configuration and result flags. Viewing, printing, and exporting remain separate authorized capabilities.

Attachment creation takes target type, optional target identifier and field, filename, content or external location, privacy, folder, and optional upload processing. Default privacy is private. Upload can reuse an authorized existing file, create a temporary target attachment, or invoke an explicitly exposed custom upload handler. An intermediate chunk may return no completed file; only final assembly produces a saved attachment. An attachment is a business record with permissions and parent association, not merely a path on disk.

Evidence: source-artifact-e9e5a0c9d8b9908522c7 lines 27–88; source-artifact-e9e5a0c9d8b9908522c7 lines 279–333; source-artifact-9d66d61a7b7d9a437d11 lines 130–261.

## Acceptance obligations

A conforming adapter must demonstrate defaults, errors, and partial-success boundaries rather than merely exposing a matching list of names. Required scenarios include a twenty-one-item batch, stale update with and without an expected version, restricted child-field read, masked value round trip, unsaved calculation that does not persist, copy without insertion, forbidden submitted edit, import with one failed payload after successes, report access without export permission, and a multipart upload that returns no completed attachment before final assembly.

No generic service contract implies compatibility with every literal route or implementation identifier in the source. Literal transport renaming and behavioral compatibility are separate declarations. Domain operations must additionally describe their exact arguments, derivations, records written, accounting effects, preconditions, and acceptance scenarios.
