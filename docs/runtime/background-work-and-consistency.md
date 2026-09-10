# Background work and consistency

Business work can finish within a request or continue through a tracked background operation. The observable contract includes when work becomes eligible, which identity executes it, whether attempts can repeat, what commits together, how progress differs from completion, and how failures remain discoverable. Queue product, worker implementation, and deployment topology are outside this specification.

## Work envelope and eligibility

A queued operation carries tenant identity, initiating user, operation identity, event context, arguments, execution policy, and a job identifier. It may also declare a timeout and success/failure callbacks. The default behavior can enqueue immediately. An explicit after-commit option defers enqueueing until the current transaction commits. A document queue action defaults to after-commit enqueueing and takes a document lock before scheduling.

This distinction is financially important. A job that depends on a newly created invoice must not observe a record that later rolls back. After-commit eligibility addresses that ordering. It does not by itself establish a durable transactional outbox or guarantee that a process crash between commit and enqueue is recoverable. The reviewed generic scheduler registers a commit callback; no automatic persistent outbox guarantee is inferred from that mechanism.

Job identifiers are scoped to the tenant. Optional deduplication requires an explicit identifier. It suppresses enqueueing when an existing job is queued or running. A completed or otherwise existing job may be removed and re-enqueued with that identity. Thus this is active-work deduplication, not permanent exactly-once processing. Business operations such as posting a payroll payment or applying an external settlement need their own durable transaction-reference checks.

Evidence: source-artifact-b1ad771a8c35d6eebd3d lines 84–218; source-artifact-1c79c95fe9c8ab1bc9d4 lines 2317–2372.

## Execution and retry

A worker restores tenant context, connects, applies the captured user when present, establishes operation context, and executes before-job hooks. The operation runs in a transaction. Success commits and returns the result. An ordinary exception rolls back the business transaction, records failure information, commits the failure record where that path requires it, and rethrows. After-job hooks and after-job callbacks run during cleanup; they are not a substitute for a successful business commit.

The internal retry path handles a declared retry request and recognized deadlock or lock-wait timeout failures. It rolls back and retries while the retry counter is below five. The first attempt therefore permits up to five further attempts, with delays of one through five seconds. This is distinct from any separately configured queue-level retry policy. A caller cannot infer that an arbitrary validation error, permission error, or external-service failure will retry automatically.

The source contains a significant identity discrepancy on this internal retry branch. It destroys local context, then recursively executes without forwarding the original user argument; reconnect defaults to the administrative identity. Static analysis therefore indicates that a later attempt can run under a different user. This has not been dynamically reproduced. A replacement must record its deliberate decision: reproduce a measured compatibility requirement if truly necessary, or retain the initiating identity as an explicit security correction. Do not silently describe all retries as proven to preserve identity.

Evidence: source-artifact-b1ad771a8c35d6eebd3d lines 250–328; source-artifact-66f1c84f2539463cb381 lines 372–424; source-artifact-66f1c84f2539463cb381 lines 472–479.

## Tracked submission and document locking

The submission queue persists a reference to the document type and identifier, initiating user, queued time, background job identity, completion time, status, and failure detail. Its statuses are queued, finished, and failed. A second request for a document already marked queued returns information about the existing queue record rather than creating another submission.

Queueing locks the referenced document. A normal save checks the lock and rejects edits while the action is queued. The background submission records its actual job identity, performs the requested submit/cancel operation, rolls back the document transaction on failure, and stores a terminal queue outcome. It does not convert a failed submission into a successfully submitted document merely because the queue record itself was created successfully. A completed action produces a transient user notification when sufficiently recent, otherwise a persistent notification entry.

Manual unlocking exists, but the source comments identify a possible mismatch between a queue record and another submission lock for the same reference. A neutral contract should expose unlock as an administrative recovery operation with its own acceptance cases. It must not state that unlocking cancels work already executing. Recovering a stuck lock requires checking current document state, active job state, and whether any financial consequences committed.

Evidence: source-artifact-e609b7de6b102f041400 lines 58–192; source-artifact-1c79c95fe9c8ab1bc9d4 lines 2317–2372; source-artifact-1c79c95fe9c8ab1bc9d4 lines 812–944.

## Scheduled business work

Scheduled operation definitions include enabled/stopped state, frequency or calendar expression, target operation, last execution, next execution, and queue policy. Due work checks whether another instance is already queued and whether the owning capability is disabled. The next-execution calculation uses declared frequency and the last execution or creation time. Continuously scheduled work converts its configured interval from seconds to whole minutes, with a 240-second fallback. The reviewed code computes a tenant-dependent maintenance offset but returns a newly computed unshifted schedule time; therefore the computed offset must not be claimed as effective scheduling behavior without further verification. These are observable scheduling concepts; a replacement need not duplicate worker process names.

Scheduled effects must remain tied to their business definitions: recurring invoices, subscription periods, stock reposting, payroll-related reminders, scheduled reports, and notification dispatch are not interchangeable. A schedule firing twice must not create duplicate financial records when the domain defines a unique period or source reference. The generic scheduler's job deduplication alone cannot provide that guarantee.

Evidence: source-artifact-91af98c5f0f2b358f1ed lines 58–206.

## Real-time updates and progress

Events route to a tenant-wide internal audience, website audience, user, document type, individual document, or task progress channel. A normal document update is deferred until commit and carries document type, identifier, and modification time. List updates are also deferred. The commit queue suppresses identical event/message/room entries within the same local transaction log; rollback clears this log. This is local duplicate suppression, not replayable event sourcing.

Progress messages can publish before the business transaction commits. A task-scoped event forces immediate delivery even if a caller requested after-commit behavior. Clients must distinguish percent complete, finished operation, and durable committed outcome. A progress percentage of one hundred cannot alone prove that every associated ledger write has committed. Publication suppresses connection errors on the message channel, so a successfully committed change can lack a live notification. Reloading the authoritative document must recover the correct state.

Document and document-type subscriptions check access; task-progress subscriptions have the separate source limitation described in the identity document. Live messages are not authorization tokens. Any event containing a record reference must still lead to a permission-checked read.

Evidence: source-artifact-3d8f5f8af4a5a70b7faf lines 31–136; source-artifact-af5a18ab59f29558dded lines 36–138; source-artifact-1c79c95fe9c8ab1bc9d4 lines 1773–1960.

## Outgoing event delivery

Configured outgoing event deliveries select a document type, document event, condition, destination, request method, payload definition, headers, optional signing secret, timeout, queue, and retry count. Ordinary event dispatch queues delivery only after commit. Within that queue, repeated occurrences of the same configured delivery and document identity use the last document instance, preserving the final queued values. Import suppresses this generic outgoing-event path; it must not be assumed to emit the same external traffic as interactive creation.

Delivery prepares the destination and payload, sends the request, and records delivered, failed, or exhausted status. A workflow-transition delivery runs synchronously when selected as a synchronous task; failure is raised because the transition needs the outcome immediately. Ordinary failed delivery can schedule retry. The retry delays are five minutes, thirty minutes, two hours, five hours, and ten hours, with later attempts using ten hours. A retry reuses the stored destination, headers, and payload, and checks whether the delivery configuration remains enabled. The maximum retry count counts attempts after the initial delivery; changing configuration can therefore affect later attempts without rebuilding their payload.

An enabled signing option computes a keyed hash over the exact serialized payload and encodes the result for a signature header. The replacement must define serialization deterministically because semantically identical objects with different byte ordering or whitespace can produce different signatures. This blueprint uses a neutral signature-header name; it does not claim that renamed headers are byte-for-byte compatible with existing consumers.

External delivery can be duplicated even when a local job is deduplicated: a remote server might accept a request and the local client might time out before seeing the response. Receiver-side business reference deduplication is necessary for exactly-once business effects. It is an acceptance obligation for each integration, not a guarantee supplied by generic outgoing-event delivery.

Evidence: source-artifact-ac9f4042fec42828bb99 lines 5–117; source-artifact-c92b91c9ae73e577a3db lines 155–352; source-artifact-c92b91c9ae73e577a3db lines 20–25.

## Partial success and savepoint limitations

Bulk transport operations use a savepoint for each item and collect successes and failures. A failed item rolls back to its savepoint while later items can continue. The full request or worker transaction then commits surviving changes. An operational data import instead commits each successful document payload, retaining earlier successes when a later row group fails. Bulk workflow actions similarly commit successful documents individually. These three operations therefore have different crash and retry boundaries despite all being called bulk work.

Savepoint rollback does not invoke full-rollback callbacks or undo filesystem writes. A callback registered while processing an item may need separate cancellation if that item later fails. Acceptance testing must inspect resulting external events and attachments, not just table contents. The source's savepoint mechanism alone does not establish per-item atomicity for non-database effects.

Evidence: source-artifact-67374161a6df47b4eb7f lines 1190–1250; source-artifact-70f793c473898fecc4cc lines 274–562; source-artifact-831cef801a36881fee0d lines 132–284; source-artifact-c53dbe3cd685497ce317 lines 246–370.

## Acceptance obligations

1. Roll back a transaction that requested after-commit work and verify that the work is not newly enqueued.
2. Submit the same operation identifier twice while queued, then after completion; observe the difference between active deduplication and allowed re-execution.
3. Fail an operation after writing one ledger row and verify rollback before any retry; compare the acting identity on every attempt.
4. Simulate lost event delivery after a successful commit and verify that document reload gives the durable result.
5. Interrupt an import after several successful payloads; resume without duplicating those completed payloads.
6. Fail one bulk item after scheduling an outgoing event and verify whether that event survives the savepoint rollback. Record the measured behavior and any correction explicitly.
7. Make an outgoing receiver accept a request while the sender times out; verify that retry does not duplicate the receiving business transaction.
8. Force a queued submission to fail and verify failed tracking, unchanged submitted state, discoverable error, and recoverable lock behavior.
