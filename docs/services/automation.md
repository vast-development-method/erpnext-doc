# Durable event automation

## Stored model and temporal identity

| Entity | Durable identity and fields | Purpose |
|---|---|---|
| Flow | Definition identity, enabled flag, trigger type, reference type, optional field/from/to condition and filter, execution identity policy, ordered actions, relationship definitions, revalidate-on-run and stop-on-error flags | Selects matching occurrences and defines a plan. |
| Trigger | Row identity, flow, reference type/name, state, trigger time, trigger actor, depth, payload, eligible time, optional resume-run ID and next step index | An admitted unit of work, committed with its triggering mutation. A plain reference identity can survive deletion of its target. |
| Run | Identity, trigger, flow, actor, start/end, depth, original action snapshot, relationships, retained step outputs/records/branch decisions, status and error summary | One execution across waits. The run persists when a trigger row is deleted. |
| Step | Parent run, sequence, stable step key, action, status, duration, condition/result, error and optional output | Records individual consequences. A run may contain both committed successful and unsuccessful steps. |
| Event subscription | Identity, event name, correlation key, run, step key, resume trigger, expiry, status and matched payload | Coordinates event and timeout contenders on a single waiting step. |
| External-effect marker | Site-scoped trigger-row key with a 24-hour lifetime outside the database transaction | Prevents automatically replaying a row known to have entered an externally acting step after a failed commit. |

## From a business edit to runnable work

1. Map creation, update, change, submit, cancellation or deletion hooks to their trigger type. Suppress an update trigger emitted as part of insertion. Suppress dispatch during installation, patching or migration. Request suppression and site disable settings also apply.
2. Filter enabled rules by event and referenced document. A field-change rule needs a stored before-image and a changed value. Supplied from/to qualifiers compare string forms. Evaluate the filter tree and optional condition. A matching error is logged and treated as no match.
3. Increment the current automation depth only for matched work. Greater than configured maximum refuses dispatch. The default is three. Within the document transaction, insert or refresh a pending/scheduled trigger and register a post-commit wake-up.
4. A fresh non-resume trigger for the same populated flow/type/name can coalesce with a waiting trigger. Retain the newest actor and trigger time, set the newest due time/status and retain the greatest depth. An absent payload leaves the previous payload intact on refresh. An explicitly empty object replaces it. New-row insertion serializes only a truthy payload, so a first empty object can be stored as absent. A running or resume trigger is a different case. Independent subjectless custom events receive generated occurrence identities.
5. Promote due scheduled work and claim waiting rows whose eligible time is absent or at most now. Order by trigger time, limit the batch and lock as part of selection. Mark claimed rows running and commit that claim before executing. Competing drainers must not obtain the same active claim. A stale running claim changes back to pending only when its last modification is **strictly older** than the configured cutoff.

## Plan execution and effects

At execution, reload the target. Missing referenced targets produce a skipped run. With revalidation selected, a changed document can cease matching between enqueue and claim. Snapshot the action order and parameters on first execution. A resumed run reuses the original run, prior steps and snapshot. The saved run state carries step outputs, resolved relationships and chosen branch arms. The runner still reads the flow for surrounding policy, so holding the action snapshot does not freeze every setting.

The identity policy uses the triggering user (falling back to flow owner), document owner where a target exists, or the configured automation user with administrator fallback. Check trigger read access under the chosen identity. Check target permission when resolving action targets. Leave the previous session intact after the run. Built-in actions cover setting a field, creating a document, incrementing a value, notifications, assignments, outgoing calls and configured scripts. An extension action's transactional declaration is part of its observable recovery contract.

A failed action rolls its changes back to its step savepoint. With stop-on-error the run fails on that step. With continuation the overall status can be partially failed even when later steps succeed. Successful earlier steps may persist. A delay creates a resume trigger; the original run remains waiting. Successful, partially failed and waiting outcomes remove the processed trigger row, while failed and skipped rows are retained for cleanup. Persist the run status independently of the trigger's continued existence.

The drainer groups claimed rows into transactions with per-row savepoints. A failed group commit rolls back and attempts serial settlement. Before a nontransactional call the runner records an external-effect marker. A replay seeing this marker settles as failed without repeating the external call. The marker cannot certify whether the remote system received a request or acted on it. It can expire or be lost; end-to-end exactly-once delivery would require cooperation from the recipient. After a successful group commit clear the markers. A separate periodic drain and stale-claim sweep recover from missing wake-ups.

## Event rendezvous

A wait needs an admitted event name, a nonempty rendered correlation key and a timeout. Create the timeout resume row and subscription together. Event emission validates its name and payload size, queues matching new flows and then considers **every** waiting subscription with the matching event name and key. Lock and reread each subscription. If the state already changed, count zero for that subscription. If expiry is strictly later than the current time, mark matched, store the payload, bring the existing resume row forward and count one. At or after expiry, mark timed out, leave the matched payload absent, bring the same resume row forward and count zero. At execution a still-waiting subscription belonging to a timeout resume becomes timed out. Duplicate delivery may create separate independent event flows but cannot resume an already settled wait a second time.

**Acceptance experiment.** Park two runs on the same event/key at 12:00 with expiry 12:05. Emit matching data at 12:04:59 in two concurrent transactions. The sum of successful subscription claims across both committed emissions is two. Each run resumes once on its existing timeout row. In a new experiment emit exactly at 12:05. Both count as timed out. In a rollback experiment withdraw the first emission before commit; the other transaction may then claim both. Use controlled time and durable run/step records as the oracle.
