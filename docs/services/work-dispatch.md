# Approvals, routing and background work

An approval changes business state. An assignment records who should act. A scheduled operation decides when a command is eligible. A worker executes a particular attempt. These four identities and their evidence must remain separately queryable.

## Workflow actions

1. Reload the saved document. Check read access. Select transitions with the current workflow state, a role held by the actor and a passing optional condition. A new unsaved object has no available transitions.
2. Match the requested action in this qualified list. When selecting the action, iteration retains the last matching action if a configuration yields multiple candidates. Explicit action application requires that the actor be the administrator, the transition allow self-approval, or the actor differ from the document owner. This is a separate decision after discovery.
3. Set the next workflow state and evaluate the destination state's optional field update against the changed document. Retrieve enabled transition tasks in configured order. Run synchronous tasks first in their relative order. Register each asynchronous task for enqueue after commit.
4. Map the old/new structural states to save, submit, submitted update, or cancel. A configured background submit or cancel uses the submission queue when the scheduler is active and returns before the synchronous workflow-comment path. A queued response acknowledges intent. Check the actual structural state and resulting ledgers to establish posting.
5. Bulk admission uses input length before processing. Up to 19 entries execute inline, 20 through 500 enqueue, and more than 500 are rejected. Each successful item commits separately. A failing item rolls back and the operation continues. Keep mixed outcomes attached to the original document names. A later failure cannot undo an earlier item.

## Assignment selection

Process enabled rules for the document type in descending priority, filtered by applicable day. Existing assignments first undergo the unassign pass. Once clear, the first applicable rule that succeeds can allocate. Reload assignments before evaluating closing and reopening conditions. A task records reference type/name, assignee and status, so an invoice can be pending approval even when its assignment has closed.

| Selection | Decision and exact tie behavior |
|---|---|
| Round robin | Lock and read the last assignee from the persisted rule. Choose the next list member. At the end, with an empty previous identity or after a removed member, choose the first configured member. |
| Least loaded | Count open tasks per configured user **and reference type**. Choose smallest count, using configuration order for ties. Other document types and closed tasks do not increase this count. |
| Document field | Resolve the configured field on the current document. Accept it only if the referenced user exists. |
| Weighted distribution | Use eligible named rows in configuration order, with zero/unset weight treated as one. If total weight is nonpositive or there are no users, return no user. Lock the per-rule counter. Choose the first cumulative weight greater than counter modulo total, then advance the counter. Weights 2 and 1 with counter 0 allocate A,A,B,A,A,B. Interleaved decisions for unrelated rules have independent counters. |

## Queue and scheduler contracts

An asynchronous enqueue carries the site, actor, operation, arguments, queue and timeout. An optional stable job identifier belongs to the site. Deduplication requires an explicit identifier. A queued or started job with that identity suppresses a duplicate enqueue. A terminal prior job can be discarded and the identity reused. This is a job admission check, so a separately repeated payment or webhook still requires a business-level duplicate policy. Immediate execution and registered after-commit enqueue have different transaction timing. An after-commit enqueue can fail after the originating transaction is already durable.

On the first asynchronous execution, initialize the selected site and apply the queued identity when present. Ordinary success commits. An explicit retry signal or eligible database deadlock/lock timeout rolls back and can retry with delays of 1, 2, 3, 4 and 5 seconds. That is up to six attempts including the initial call. Other errors follow the failure path. Each retry must restore the initiating tenant and principal and apply current business permissions before repeating the operation.

Scheduled eligibility includes equality with next execution and suppresses queueing when the corresponding site job is already queued. On cold start the last-execution base falls back to the creation time. The calendar derives the next occurrence for the frequency. Maintenance frequencies also use a stable site-specific offset. Tick eligibility, queue admission and execution of the method each have separate outcomes.

A two-session acceptance run should allocate a weighted queue concurrently, include a duplicate bulk approval ID, and simulate a rolled-back enqueue. Capture the selected users and terminal states as well as pending job IDs. A second transition on the same document re-evaluates persisted state. It may legitimately fail after an earlier entry succeeded.
