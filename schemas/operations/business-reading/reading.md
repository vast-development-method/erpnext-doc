# Read an operation

A workflow index lists records, reports and services. Open an operation range and locate the required entry by name or stable identifier. The closing links give the applicable procedure, the availability decision and the declaration receipt. The contract link selects the specific line where the operation begins. The receipt identifies the bound file, qualified name and occurrence.

| Question | How to read the entry |
|---|---|
| Which values enter? | Inputs appear in declaration order. A value following an equals sign supplies the default. Positional-only and named-only arguments retain their restrictions. Remaining positional or named values represent an open argument collection. The receiver, commonly `self` or `cls`, can supply record fields and settings independently of the explicit caller arguments. |
| Which outcomes appear? | Explicit results summarize distinct return expressions. Explicit failures identify locally raised exceptions and calls to the platform's validation-error helper. The ordered steps place each result under its actual condition. Routine completion can also depend on a called operation or context manager. |
| Which state is involved? | Record and data access identifies recognizable document and query calls. Passing an in-memory mapping to a document constructor can create an object without reading a stored row. State and service calls identify explicit handoffs, updates and transaction requests. A call such as `save` requires its receiver, authorization and transaction outcome to establish a durable write. |
| Which procedure handles the work? | Method links open declarations found on the same qualified owner in the same source file. Inheritance, hooks, fixtures, regional implementations or site configuration can select another implementation. The entry links specific calls that visibly consult identity, settings, queued work, time or selected callables. |
| What do the operands mean? | Stable field names, operator order, literal thresholds and selected record names identify the relevant business values. Presentation aliases such as `Platform` label the shared service namespace. Exact adapter symbols and literals are available from the decision contract and its evidence vocabulary. |

## Follow a branch

Read steps from top to bottom. Indentation places work inside a selected guard, iteration, context or handler. A guard with no printed alternative falls through to the next outer step when false. A return or propagated error ends the current normal path. A pending exit still passes through applicable cleanup. The same guard can run repeatedly on different rows.

- A value choice uses only its selected result. A conjunction stops at the first false-valued operand and a disjunction stops at the first true-valued operand. If all operands were needed, the final operand supplies the result. These constructs can return a value other than a Boolean.
- Additional substeps beneath an assignment, return or call describe evaluation of its operands before that action completes. Nested value choices, short circuits and collection filters apply only when evaluation reaches their containing expression. A lookup appearing in a skipped operand does not execute.
- A loop's normal-exhaustion alternative follows ordinary exhaustion or a false loop test. Breaking skips that alternative. Continuing resumes the iteration or test. A generator can defer yields, filtering and calls until a consumer requests another value.
- A protected block selects the first matching ordinary handler. An exception-group handler addresses the matching subgroup. The normal alternative follows a protected block that reaches its end without an exception or earlier exit. Cleanup runs for normal completion, return or failure and can replace a pending outcome. A context manager can suppress an exception.
- A pattern selection considers alternatives in order and evaluates the guard for a matching pattern. An assertion depends on assertion enforcement in the executing environment.

The local steps describe the declaration's structure. Feasibility of a path depends on the actual input values, effective settings, caller, current database rows and behavior of callees. Dynamic queries and adapters can produce additional errors or effects. Nested function and class definitions bind names in the outer operation. Read the separate binding for a nested callable to determine what happens when it is invoked. A default expression or decorator can have definition-time effects.

Long messages, literal queries, collection members and deeply nested operands can appear in abbreviated form. The linked decision contract preserves complete values and nesting. For an unchanged procedure, the retained contract supplies the applicable local logic. For a changed or additional procedure, the current contract supplies it. The status applies to the local procedure and its declaration. [Availability definitions](../current-decisions/README.md)

## Compare two inputs at a guard

A derived branch illustration holds the surrounding context fixed and varies one local value. The link beside the illustration opens the predicate and the immediate consequence. A sample that skips a rejection can still reach another validation later. Named values come from the owning record's declared choices, and a collection length describes the value seen at this point. Access and credential controls give a defensive account of the governing decision, exposed results and service boundaries.
