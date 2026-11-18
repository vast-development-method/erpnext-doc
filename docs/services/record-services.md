# Requests, documents and policy

## Request identity, tenancy and admission

At request entry the configured site override has first priority, followed by the site selector supplied by the routing layer, then the resolved host. The application loads that site's configuration and opens its database before running the business operation. On a maintenance site, requests stop unless reads are enabled. In the latter mode, use the configured read replica or a read-only transaction. A commit requested against a read-only transaction resolves as rollback. A company belongs to the site's business data and can be the target of a link restriction. A company identifier cannot select the tenant or substitute for a tenant-scoped connection. An independent implementation must keep trust in the routing selector at the deployment boundary.

The optional site-wide limiter budgets elapsed processing time per fixed window. At entry compute the bucket as floor(epoch seconds / window seconds). Read consumed **microseconds**, compare against configured seconds × 1,000,000 and reject with 429 only when consumed is strictly greater. At equality the request still enters. Remaining time is clamped to zero and the advertised balance rounded to whole seconds expressed in microseconds. Reset and retry delay are in seconds until the next window. The after-request accounting adds elapsed time to the original bucket. Two concurrent requests may both enter before either charge posts. This counter measures processing time across the site. Endpoint-specific limits have their own policies.

## Record shape and ownership

| Record kind | Identity and write rule | Consequence for a service |
|---|---|---|
| Ordinary aggregate | Site, type and name identify one header. Its stored modification time supplies a version for an existing edit. | Load for update, verify write, check supplied version, resolve state transition and run controller validation before persisting changes. |
| Singleton | One logical record named for its type within a site. Fields have singleton storage. | Select singleton persistence even when the external payload resembles an ordinary header. |
| Owned row | Stable row name plus parent type, parent name and containing field identify its ownership. Position expresses order. | For a stored collection, remove missing row names only within that parent and field. Update retained rows and insert new rows. |
| Virtual aggregate or collection | An extension supplies persistence or computes the rows. | Generic child replacement skips a virtual parent or field. Accept different adapters for retrieval and persistence. |
| Amended record | A new record can refer back to a cancelled predecessor. | Verify the predecessor's persisted structural state and associate attachment records with the successor. Preserve original identity for historical references. |

The update adapter locks and loads the current aggregate before applying the supplied fields. A missing collection therefore retains the loaded rows. A supplied empty collection replaces the membership. A supplied subset removes its omitted members. Expected-version behavior differs between a client sending its prior modified time and a patch omitting that value. For example, two patches that omit the version can both succeed in order. An edit sending a stale value must fail before child replacement. Exposed patch input discards internal flags. Validate field-level read permissions on the response as well as write permission on entry.

## Read and mutation admission

For a concrete child request, resolve its stored parent type, parent field and parent name. The parent type must be a top-level type whose effective metadata declares this child type on that field. Check the containing field's permission level before delegating the requested right to the actual parent. Child selection at an elevated level uses the parent's accessible read levels. A type-level discovery request without a child must still identify a valid parent type. Site administrator access is short-circuited in the outer permission dispatcher. A role with read access to invoice headers and no access to an elevated payment-detail table must be denied when requesting one of those rows directly.

| Service | Parameters and prior state | Success and failure contract |
|---|---|---|
| Read document | Site, actor, type, name | Load, check record read, apply field visibility and serialize. Missing identity or denied record terminates the read. |
| List records | Fields, filters, group, sort, start default 0 and limit default 20 | Use a permission-aware query and allow the type's registered list customizer to refine it. Read up to limit + 1. Return at most limit, with a continuation flag when an extra row exists. An invalid customization result or failed query fails the call. Use deterministic ordering in comparison fixtures. |
| Call a named business operation | Operation, verb, actor and arguments | Resolve registered override and dispatch route. Ordinary registered methods require exposure and an allowed verb. A configured server-side service is a separate registration path. |
| Call a method on a stored document | Type, name, operation, read or write verb | Require a published operation and its admitted verb. The record-action adapter maps GET to record read and POST to write. Apply field-level visibility to the returned document. Domain checks can impose additional rights such as submit. |
| Existing ordinary mutation | Stored version, submitted version, current and target structural state, body, rights | Resolve draft-to-draft save, draft-to-submitted submit, submitted-to-submitted restricted update, or submitted-to-cancelled cancellation. Deny ordinary edits of cancelled records. A stale version fails before selecting the requested structural transition. |

## Transaction lifetime

A successful ordinary mutating request commits. A successful read rolls back incidental writes unless explicitly marked to commit. An exception in ordinary dispatch rolls back. Commit clears rollback watchers, invokes before-commit callbacks, commits, refreshes the transaction, clears value caches and invokes after-commit callbacks. Full rollback drops pending commit watchers and runs rollback callbacks around the database rollback. A rollback to a named savepoint clears cached values but leaves callback registrations intact. External resources need a corresponding compensation boundary. A failure after a durable commit cannot withdraw that committed invoice. Scope claims about atomicity to the actual transaction and explicitly account for services with intermediate commits.

For conformance, create the same local record identity in two isolated sites and grant access in only one. Run list, direct read, child read and worker lookup with each site's normal identity. Independently interleave two sessions editing a parent with two distinct child fields sharing one child type. Confirm that rejection preserves both fields, and that clearing one accepted field removes only its own rows. Record database state after commit as the oracle.
