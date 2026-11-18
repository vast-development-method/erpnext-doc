# Scope and evidence

The business index contains one reading for each of the 23,195 bindings that the applicability register marks `retained_definition` or `current_definition`. Each reading joins the stable identifier to its exact qualified declaration, occurrence and source span, and to the applicable decision body. A group follows the module, record, report or service of the bound declaration. Shared utilities, setup functions, diagnostics and framework services can participate in the same register as user-facing transactions. [Applicability register](../current-decisions/README.md)

The register also accounts for 4,605 declarations absent at their recorded bindings and 11,711 classified as supporting or excluded. A moved responsibility can have a different active declaration. The underlying inventory and receipts retain the earlier identifiers and classifications. [Complete resolver](../../../docs/rebuild/checkpoint-corrections/README.md)

## Local decisions

| Construct counted in the indexed local bodies | Sites |
|---|---:|
| Statement conditionals | 36,508 |
| Conditional value expressions | 3,734 |
| Short-circuit Boolean expressions | 14,929 |
| Chained comparison expressions with more than one comparison | 84 |
| Statement loops | 8,402 |
| Comprehensions and generator expressions | 4,984 |
| Protected blocks with handlers or cleanup | 1,345 |
| Pattern selections | 17 |
| Explicit return statements | 20,932 |
| Explicit raise statements | 742 |
| Direct validation-error helper statements | 4,439 |

Counts describe syntactic sites, independent of whether a particular run reaches them. Short circuits inside an ordinary guard count independently. Nested procedures have their own bindings. Combinations of inputs can be unbounded across loops, callbacks, interleaved requests or mutable site data.

## What the evidence establishes

| Evidence | Supported interpretation |
|---|---|
| Applicable contract and declaration receipt | The nominated callable has the listed local inputs, decisions and explicit outcomes. Ordered expressions and arguments in the contract retain details abbreviated in the reading. The contract comparison for a retained body excludes positions and documentary strings. |
| Direct stable-ID worked case | Thirteen stock-controller examples are attributed to the identical stable identifier with a retained local procedure. These are derived examples from the recovered contract. Their premises can include stored row state and caller behavior. |
| Worked reading across named operations | The separate examples follow specific calls and assumptions across record validation, notifications and persistence. Each calculation or selection can be checked against the linked local procedure. |
| Runtime observation | A recorded observation supplies evidence for the concrete transaction, actor, configuration and data it exercised. The area-level observation page identifies its scope. [Reference transactions](../../../docs/rebuild/live/README.md) · [Shared services](../../../docs/rebuild/platform-live/README.md) · [Warehouse fulfilment](../../../docs/rebuild/warehouse-fulfilment/README.md) |

## Boundaries that remain open

A record's entries name the visible call sites and identify the boundaries they use. Recognizable query and access calls show what must be supplied by the runtime. These lexical indicators can omit dependencies introduced through imports, helpers, aliases or overrides.

| Boundary | Bindings carrying the indicator | What the caller must resolve |
|---|---:|---|
| Effective access | 1,223 | Effective user, roles, grants, shares and the permission service's result for this document and action. |
| Database or record state | 8,726 | Record identity, returned rows, transaction visibility and database outcome. An empty result can select a different branch. |
| Late-bound calls | 11,573 | Receiver type, hook ordering, selected controller, or another callable resolved by an expression. |
| External or queued work | 364 | Provider acceptance, delivery, retries, worker execution and resulting state. |
| Wrapper behavior | 2,972 | Effective wrapper, registration, cache, authorization and order of application. |
| Time or generated values | 592 | Clock, timezone, generated identifier and any collision or ordering dependency. |
| File state | 227 | Presence, readable contents, permissions and result of file operations. |
| Operand abbreviation | 5,606 | Exact literal, collection contents or full nested expression from the contract. |
| Calls that can fail | 21,982 | Callee failures and propagation beyond exceptions explicitly handled or raised by this local body. |

A binding can appear in multiple rows. Each workflow remains responsible for interpreting the business consequences of its inputs and effects. [Read the local steps](reading.md)

## Derived branch illustrations

292 illustrations across 272 operations compare two concrete inputs at a specific local guard. They cover 106 numeric thresholds, 30 collection lengths, 74 document-lifecycle checks and 82 named record values. Each links directly to its guard in the local steps. Record-value examples use options declared on the owning record. Lifecycle examples use draft, submitted and cancelled states. A consequence applies when control has reached that guard. Other validations, caller preconditions, settings and transaction effects can still determine the outcome of the wider document.

The examples select an immediate local return, explicit failure, message request, control transfer or literal record assignment. Feasibility from an external entry point and the final transaction outcome depend on the surrounding workflow. The thirteen stable-ID worked cases in the evidence table have their own attribution. 1,233 identity, access, execution, validation and cryptography routines use control summaries covering their inputs, result forms, service boundaries and local decision structure. Counts in the local-decisions table include those routines.
