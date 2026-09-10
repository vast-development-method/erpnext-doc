# Document lifecycle and transactions

The transaction document is the common unit of business control. Its stored state is separate from descriptive statuses such as partly delivered, overdue, paid, closed, or rejected. Those business statuses are derived or maintained by domain logic; they cannot replace the structural state that governs saving, posting, cancellation, and amendment.

## Structural state machine

| Existing state | Requested state or action | Base outcome |
| --- | --- | --- |
| Draft, stored value zero | Save as draft | Ordinary save |
| Draft | Submit, stored value one | Allowed only for a submittable type and an authorized user |
| Draft | Cancel through ordinary save | Rejected |
| Submitted | Save as submitted | Restricted update after submission, requiring submit permission |
| Submitted | Cancel, stored value two | Authorized cancellation |
| Submitted | Return to draft | Rejected |
| Cancelled | Any ordinary save | Rejected |
| Draft | Discard | Separate operation: mark cancelled, with discard events rather than cancellation posting events |

Discard is significant. It closes a draft without pretending that posted accounting effects existed. It requires write permission and checks current version and lock state. It invokes before-discard, performs the state change through the direct-value path, then invokes after-discard. Already submitted or cancelled documents cannot be discarded. Recreating a cancelled transaction means creating an amendment or another explicitly defined document, not reviving the original identity.

The structural action must be resolved before invoking posting events. The [mutation decision procedure](#mutation-decision-procedure) and [deletion contract](#deletion-and-recovery-contract) keep discard, cancellation, amendment, and deletion distinct.

## Creation order

Creation begins by identifying a new document, applying defaults, setting user and timestamps, and propagating its structural state. It checks create permission, validates the initial state transition, and validates references. The before-insert event runs before naming. Naming allocates parent and child identities and sets child ownership. Field-level write restrictions are applied before the ordinary pre-save event sequence.

For a draft creation, before-validate, validate, and before-save events run, followed by common metadata validation. The parent is inserted, then stored children are inserted, except where a virtual parent manages its own persistence. Computed child values are reset. After-insert runs; amendment lineage and attachment copying are handled where applicable. The ordinary post-save sequence then runs. The record is no longer marked locally new only after this work succeeds.

A failure after parent insertion is still a transaction failure. A replacement must not expose a half-created invoice merely because its header was already written before a child validation, attachment operation, or domain event failed. Domain controllers can add records during these events; those related writes belong to the same transaction unless a separately documented operation establishes another boundary.

The [failure boundary table](#failure-boundary-table) requires rollback of a partially inserted parent and its dependent effects when later creation work fails.

## Existing-document save order

An existing-document save checks the document's queue lock, applies defaults, restores masked fields from storage, and verifies write permission. It retains the submitted modification timestamp for concurrency comparison while assigning the new timestamp and modifying user. The current stored document is loaded with a write lock. Its modification timestamp must match the caller's original value; its state determines whether this operation is a draft save, submission, restricted update, or cancellation.

Child ownership and identities are normalized. Higher-level fields that the user cannot edit are restored to their prior or default values. Reference validation and the action-specific before events run. Common metadata validation runs except on cancellation. Restricted updates also compare immutable submitted fields against stored values. The parent is written, child tables are synchronized, computed child caches are reset, and the action-specific after events run.

Synchronizing a stored child table is replacement-by-membership, not blind append. Within the same parent type, parent identifier, and parent field, stored rows missing from the submitted existing-row identifier set are deleted. Each retained or new row is then updated or inserted. A partial client payload must distinguish omitting a table from explicitly replacing it with an empty table. Domain mapping operations that deliberately construct partial documents must use their defined service contract rather than accidental full-aggregate replacement.

The [child-membership example](#worked-concurrency-and-child-membership-cases) fixes the difference between omitted collections, explicit empty replacement, retained identities, and newly inserted rows.

## Event order and accounting consequence

| Action | Before persistence | After persistence |
| --- | --- | --- |
| Draft save | Before validate, validate, before save, common validation | After update |
| Submit | Before validate, validate, before submit, common validation | After update, after submit |
| Cancel | Before cancel | After cancel, then backward-reference checks |
| Update submitted record | Before update after submission, common validation, immutable-field comparison | After update after submission |

After the action-specific after events, normal processing clears caches, schedules document/list change notifications, updates global search, saves a version where configured, and invokes the change event. A declared event first executes the document's behavior and registered document-specific and wildcard event handlers; notification rules, outgoing event deliveries, and configured server-side document event rules are then considered. Event order affects account postings, stock postings, status updates, and user notifications. Reversing two apparently independent hooks can change which values a later hook reads.

Submission does not automatically imply a ledger posting for every document type. A sales order can create commitment and fulfillment consequences; an invoice can create receivables and accounting; a stock movement can create quantity and valuation consequences. The foundation invokes domain submission behavior; each domain specifies its own side effects. Cancellation runs the corresponding cancellation behavior and checks references. It must not be implemented as simply deleting the header or changing a status field.

Registered document event handlers run while transaction-control calls are disabled by the base dispatcher. This prevents those handlers from committing the enclosing business operation early. The document's own controller behavior and separately invoked services need their own review; this guard is not proof that every application path has one indivisible transaction.

The [financial closure invariant](#financial-closure-invariant) defines the complete fact set that must succeed or fail under the domain's transaction boundary; a lifecycle label alone cannot stand in for those consequences.

## Submitted immutability

A field not declared changeable after submission cannot change merely because the user has write permission. Parent scalar values are compared to stored values. For a table field, the parent comparison checks row count and child comparisons enforce each row's field restrictions. A new row is allowed to bypass its child immutable-field comparison when its containing table explicitly permits changes after submission. Computed fields are excluded from immutable-value comparison. Date and time representations are normalized where adapters return different forms of the same logical value.

These base checks are not a complete proof against every replacement or reordering of same-count rows. Domain tests must cover row identity, links from downstream transactions, and whether row ordering is financially significant. For example, replacing an invoiced order row with a different same-count row must be evaluated by order and invoicing rules. Preserve the actual base algorithm and add domain constraints only when supported by domain evidence or explicitly identified as a new requirement.

After-submission permission is field-specific and does not authorize unrelated monetary changes. Test a valid annotation combined with an invalid row change to ensure the entire invalid mutation follows its rejection contract.

## Transaction boundaries and concurrency

A successful state-changing web request normally commits the transaction after the operation completes. A successful read request rolls back incidental database changes unless the operation explicitly requests commit. An unhandled exception rolls back. After-request callbacks run after transaction synchronization and their failures are logged; they cannot safely turn a successful business response into an atomic failure. After-response callbacks run after the response has been sent.

Commit clears rollback callbacks, runs before-commit callbacks, commits, refreshes the transaction context, clears value caches, and runs after-commit callbacks. Full rollback clears commit callbacks, runs before-rollback callbacks, rolls back, clears caches, and runs after-rollback callbacks. Rolling back to a savepoint only restores database changes and clears the value cache; it does not invoke rollback watchers or undo external files. Therefore a service that uses per-item savepoints must separately account for external effects and deferred callback registrations.

Timestamp comparison is optimistic concurrency control; the write lock serializes access while validating and saving. The expected outcome for two editors is that the first committed edit succeeds and a second save carrying the old timestamp fails with a stale-document error. A generic update operation that reloads the latest record before applying fields can avoid a stale check if the client omits its original timestamp; it is not equivalent to a compare-and-swap request. Contracts must state whether caller-supplied version information is required.

The [concurrency example](#worked-concurrency-and-child-membership-cases) establishes the expected result for two editors with the same revision, while the [failure table](#failure-boundary-table) separates post-commit failure from rollback.

## Direct value changes and workflow transitions

The direct-value service writes selected fields, normally updates modification metadata, runs before-change and change events, and can optionally notify or commit. It does not invoke ordinary controller validation. It exists for trusted derived-state maintenance and specialized actions, and must remain separate from an unrestricted public edit operation. Callers cannot assume that it enforces submitted immutability, reference validation, or all business rules.

A workflow declares states, role-authorized transitions, optional conditions, and the structural state associated with each workflow state. Available transitions are calculated from the current stored record and the user's roles. Applying an action reloads the record, checks the action and self-approval policy, sets the next workflow state, applies an optional state update expression, executes synchronous transition tasks in the same transaction, and schedules asynchronous tasks only after commit. It then saves, submits, or cancels according to the structural transition. Invalid state combinations fail. Submission or cancellation may use a submission queue when enabled. A successful synchronous transition adds a workflow comment.

The generic save validator checks that a changed workflow state corresponds to an allowed transition, but the dedicated workflow action path also performs explicit self-approval checks. This difference requires acceptance tests for direct state-field updates; do not assume that the two paths have identical checks without those tests.

A direct-value maintenance action and a workflow transition are separate contracts. The [extension task table](extensibility-and-configuration.md#extension-registration-contract) specifies synchronous and after-commit task behavior.

## Acceptance obligations

- A domain submission that fails after creating ledger rows must leave no committed header state change or partial ledger effect.
- A cancellation blocked by a dependent submitted transaction must preserve the original transaction and its original committed consequences.
- A submitted record cannot become draft; a discarded draft must not execute financial cancellation events.
- Concurrent saves with the same original modification time must have at most one success unless the later operation deliberately reloads and reapplies changes under its specified contract.
- A post-commit notification must not precede commit, and an operation rollback must remove its queued commit notification.
- A permitted annotation change after submission must not permit a simultaneous unauthorized financial-field change.
- Dedicated and direct workflow transition paths must be tested with an owner lacking self-approval permission and with a nonowner authorized approver.

The reviewed evidence is static code and test-source inspection. It does not claim that these acceptance obligations have been executed against a running combined installation.

## Deletion and recovery contract

Deletion has a separate lifecycle from cancellation. For an ordinary stored record, acquire a nonwaiting write lock, check delete permission, and reject deletion of a submitted submittable document. An occupied lock produces a concurrency failure. Execute deletion and change behavior, inspect fixed and dynamic links, update any eligible last-used number series, delete the parent and stored owned children, execute after-delete behavior, and process attachment and protected-secret cleanup. In ordinary deletion, retain a deleted-document record containing the former type, identity, contents, and deleting actor. Explicit permanent deletion and definition reload can bypass this retained snapshot.

The link rules are not identical across actions. Cancellation's normal fixed-link check considers submitted dependants, excluding its declared exceptions and amendment linkage. The current fixed-link deletion collector can consider references regardless of their document state. Dynamic-link deletion checks exclude cancelled referencing documents. Preserve this distinction when implementing a compatibility profile; do not assume that every cancelled link permits deletion. A bounded linked-record preview must report when its limit was reached rather than assert that its truncated list proves no other blockers exist.

After-commit cleanup can remove secondary dynamic associations. It must not be confused with permission to delete business dependencies before reference checking. Virtual records provide their own deletion implementation while retaining permission and submitted-state checks. The trusted generic deletion helper can allow an already missing record as a no-op; exposed standard single-record and bulk deletion select the strict missing-record error policy.

Retaining a deleted-document snapshot does not prove that external effects or deleted attachments can all be reconstructed. Restoration requires its own checks for conflicting current identity, dependency validity, retained attachment content, secret material, and historical financial consequences. Cancellation or a business reversal remains the normal route for correcting a posted transaction.

## Mutation decision procedure

1. Resolve the trusted tenant and actor. Resolve effective metadata and the requested operation, including whether the target is an ordinary, singleton, child, or virtual record.
2. Check the operation's access gate. For an existing record, inspect its queue lock and acquire the applicable storage lock. Load the current persisted state.
3. Compare supplied expected modification information when the contract carries it. Resolve the structural transition independently of the business status label.
4. Normalize identity and child ownership. Restore masked and noneditable values from the current stored version where the save algorithm requires it.
5. Validate links and execute the ordered before-events. Apply metadata validation and domain-specific decisions for this action.
6. Persist the aggregate membership and execute the ordered after-events, including every dependent stock, financial, settlement, or operational write required by that domain.
7. Register permitted deferred work. Do not report submission complete while only its queued work record exists.
8. Commit at the service's defined boundary. On failure, apply full rollback or the explicitly documented per-item rollback contract; classify the failure for the caller.
9. Deliver notifications and refresh projections according to their completion contracts. An after-commit failure must not be reported as if the committed business transaction had been undone.

## Failure boundary table

| Failure point | Database outcome | Additional observation |
| --- | --- | --- |
| Before insert or common validation | No successful document mutation | Expose the field or business rule that failed |
| After parent insert but before child completion | Full operation rolls back | No visible half aggregate |
| After posting one of several ledger entries | Full operation rolls back | No unbalanced committed voucher |
| Cancellation blocked by a submitted dependant | Cancellation transaction rolls back | Original posting remains authoritative |
| Per-item bulk savepoint failure | That item's database changes roll back | Deferred callbacks and filesystem effects require separate verification |
| Commit succeeded, live notification lost | Business records remain committed | Permission-checked reload supplies the authoritative state |
| External delivery accepted, local acknowledgement lost | Local outcome can be uncertain | Reconcile by external/business identity before another financial operation |
| Administrative document unlock | Lock state can change | Does not cancel a worker already running or reverse its committed writes |

## Worked concurrency and child-membership cases

Two users read document revision time 10:00:00.100000. The first saves under a write lock and commits revision time 10:00:01.200000. The second submits the original revision and must receive a stale-document failure; its changes do not silently replace the first user's update. If a generic patch omits its expected revision and the service reloads the current record, it follows the overlay contract instead. That is a separate request behavior, not a successful test of stale-edit prevention.

A draft has children A and B in its item collection and child C in another collection of the same child type. Replacing the item collection with A and new row D deletes B, retains A's identity, inserts D, and leaves C untouched. Clearing the item collection with an explicit empty list removes its members subject to requiredness and business validation. Omitting the collection during an overlay preserves the loaded current list. Performing the same operation after submission must pass both table-level and child-field immutability rules and any downstream source-row constraints.

## Financial closure invariant

For a posting operation, define its affected fact set before implementation: document state, general ledger entries, stock entries, settlement entries, source progress, reservations, and dependent references. The operation's successful boundary requires the complete prescribed fact set, and its failed boundary requires no committed partial subset unless the domain explicitly defines independently committed work. Equality of debit and credit is necessary where a journal is produced, but does not prove correct account, company, currency, dimension, quantity, or reference selection. Those decisions belong to [cross-domain transactions](../domains/cross-domain-transactions.md).
