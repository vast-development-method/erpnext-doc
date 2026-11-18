# Shared platform contracts

Use the [shared services](../../services/README.md), [runtime](../../runtime/README.md) and [interface contracts](../../interfaces/README.md) to trace how an authorized operation reaches storage, queues and externally visible results. The following fixtures identify the state before and after each decision.

| Context | A rebuild must be able to explain |
|---|---|
| [Requests, documents and policy](../../services/record-services.md) · [evidence](record-services.md) | Which actor, site, parent and version control a read or write? Which side effects survive failure? |
| [Approvals, routing and background work](../../services/work-dispatch.md) · [evidence](work-dispatch.md) | Which items commit independently? Who receives the next assignment? When may a worker re-enter? |
| [Durable event automation](../../services/automation.md) · [evidence](automation.md) | Which edits coalesce? What wins an event versus timeout race? What evidence survives a failed delivery? |
| [Files and reporting](../../services/files-and-reports.md) · [evidence](files-and-reports.md) | Who may reuse a private blob? Who owns a prepared result and how is it selected? |
| [Language selection and delivery](../marketplace-guides/languages/README.md) | Which language governs a signed-in view, a public page, an issued document and a queued message? How does a retry retain the chosen template revision? |
| [Application composition and recovery](site-operations.md) | Which extension wins? What belongs to a backup generation? How far may a failed update have progressed? |
| [Decision contracts](contracts.json), [contract schema](contracts.schema.json), [acceptance cases](acceptance.json) and [case schema](acceptance.schema.json) | Ordered rules with typed inputs, expected outcomes, exact source locations and examples. |
| [Verification](verification.md) | Re-evaluate each case independently of the reference service or run it against a replacement adapter. |
| [Isolated reference observations](source-observations.md) | Compare 28 independently specified outcomes with calls into six pinned upstream decision functions using controlled dependencies. |

A decision in this profile models one gate at a time. Passing an attachment controller gate, for example, still leaves the enclosing authorization policy in force. Prerequisites, calculation units and the meaning of each outcome are included in each contract. All example inputs are synthetic. The cases are deterministic contract checks. Upstream test files give additional evidence and are individually linked with their chapters. Live concurrency, authentic identity propagation and recovery from process failure require the multi-actor checks in the text.
