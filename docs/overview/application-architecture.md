# Application architecture

## Architectural model

The application is a metadata-governed system of documents and services. A record definition describes fields, relationships, parent-owned rows, presentation metadata, permissions and lifecycle capabilities. Business controllers and composed extensions add decisions that cannot be represented by field metadata alone. Screens, remote operations, scheduled jobs and integration handlers invoke these same domain operations, although their authentication and error envelopes differ.

A faithful replacement must distinguish these layers:

| Layer | Responsibility | Observable contract |
|---|---|---|
| Experience | Forms, lists, dashboards, workspaces, portals and mobile interactions | Available actions, field visibility, warnings, user tasks and progress |
| Transport | Requests, uploads, background submission and notifications | Authentication, argument handling, output shape and failure classification |
| Application service | Orchestrated use case and transaction ownership | Preconditions, permission checks, dependency order and success boundary |
| Domain policy | Calculation, validation, state and accounting decisions | Deterministic rules for the same effective inputs |
| Record runtime | Identity, metadata, persistence and lifecycle | Parent-child integrity, submitted-state restrictions and revision checking |
| Projection and processing | Balances, progress, reports, scheduled work and reconciliation | Timely derived state with visible pending and failed work |

These are logical responsibilities. The replacement may place them in one process or many without changing the business contract.

## Four distinct state families

Document lifecycle distinguishes draft, submitted and cancelled records, with additional discard and amendment operations where supported. Business status independently expresses states such as open, on hold, partly received or completed. Settlement state expresses unpaid, partly paid, paid, unreconciled or advance allocation conditions. Background processing state expresses queued, running, completed, retrying or failed work.

A submitted sales order can therefore be on hold, partly delivered, partly billed and partly paid at the same time. A cancelled invoice can retain reversal records. A received item can be awaiting final valuation. Combining these into one status loses information.

## Transaction architecture

A service operation validates identity and permissions, loads the authoritative record state, checks dependencies, calculates consequences, persists the document and dependent records, and schedules any after-commit work. The exact event order and transaction boundaries are specified in [document lifecycle and transactions](../runtime/document-lifecycle-and-transactions.md).

Inventory movement and financial movement are related but not identical. A reservation changes availability without posting an inventory movement. A purchase receipt can establish value and an accrued liability before an invoice exists. An invoice can recognise a party balance without moving stock when the movement already occurred. Payment can settle a party balance without changing revenue. See [cross-domain transactions](../domains/cross-domain-transactions.md).

## Metadata as active behaviour

Metadata can enforce required values, precision, allowed options, relationships, role permissions, workflow transitions and submitted-field editability. Presentation hints can be weaker than server validation; a hidden or read-only field is not automatically immutable in storage. Link targets can depend on another field, and child records are owned through both parent identity and parent collection. Single-instance settings records have different persistence from ordinary records.

Changing metadata can affect queries, forms, serialisation, permission checks and business validation. The replacement needs a coherent metadata publication boundary: all participating paths must agree on the active definition used for a transaction. The particular cache or distribution mechanism is an implementation choice.

## Extension composition

Current extensions add behaviour to employee, project, time record, payment, contact and communication records. Additional event handlers run on shared records. The unified model must compose these responsibilities instead of accidentally replacing the base financial or permission behaviour.

For example, a payment can update an employee expense claim; a journal cancellation can remove a payroll reference; a contact change can refresh lead phone details; a product change can synchronise a commercial product projection. The ordered composition and any uncertain application-order effects belong in acceptance tests. Evidence: source-artifact-1e30c9d20ea8e211402e lines 162–250, source-artifact-85bf1e834e4e4d148fa6 lines 154–220, source-artifact-84576302b4033b578065 lines 387–465.

## Reports and consistency

Transactional records, journals, stock movement records, party settlement records and change histories are facts. Outstanding amounts, projected quantities, progress percentages and many reports are derived from those facts and explicit policies. A replacement may materialise projections for performance, but must retain a way to reconcile them and expose unfinished recalculation rather than presenting stale results as final.

Do not infer that all source projections are maintained by one uniform mechanism. Some update synchronously, some through hooks and others through background processing. The relevant domain specification determines the required completion boundary.
