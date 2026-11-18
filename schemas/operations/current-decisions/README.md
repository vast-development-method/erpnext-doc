# Find the applicable operation

Look up a stable identifier in the alphabetical ranges for its business area. Each range points to a table that gives the operation's availability, scope and current procedure. The [lookup reader](../../../docs/rebuild/checkpoint-corrections/README.md) performs these joins locally and can check the complete index.

| Area | Bindings |
|---|---|
| Enterprise transactions, inventory and accounting | [Enterprise](enterprise/README.md) |
| Shared records, access, services and runtime | [Foundation](foundation/README.md) |
| Employees, attendance and payroll | [Workforce](workforce/README.md) |
| Leads, opportunities and relationships | [Relationships](relationships/README.md) |

| Availability | Which detail to use |
|---|---|
| `retained_definition` | Read the existing body from the [operation index](../operation-index.json). The inspected implementation has the same declaration and ordered procedure after excluding source positions and documentary strings. Its effects can still depend on updated callees, settings and installed extensions. |
| `current_definition` | Open the named procedure file and find the exact identifier. This is the applicable record for that binding. It includes the call signature, wrappers and ordered decisions for a changed or additional definition. A dash in the procedure column means the availability row supplies the resolution. |
| `absent_at_binding` | The inspected implementation has no definition at that path, qualified name and occurrence. The older body remains available for interpreting existing data and research. A workflow may continue through a different binding. Establish that relationship from its caller, controller and business chapter. |
| `supporting_or_excluded` | The retained inventory classified the binding as a test, supporting evidence, migration or deployment procedure. It supplies no active business contract through this lookup. |

The comparison matches the original declarations to source files, qualified names and occurrence within each file. New bindings receive stable identifiers in their own area. The inventory includes additional functions in the four application packages, excluding test, fixture, benchmark and patch paths as defined by the comparison. The [coverage counts](coverage.json) are counts of declaration bindings. Runtime dispatch can select a subclass, hook, regional override or site configuration. See the [worked project costing case](../../../docs/transactions/project-costing.md) for an override that changes the currency column used.

## Read a current procedure

Every procedure has an identifier, parameter bindings, ordered wrappers, asynchronous flag, declared result shape and ordered steps. The [notation dictionary](notation.json) gives the ordered fields for each tagged array, including all entries in nested expressions. A named argument with an absent name unpacks a mapping. Positional defaults align to the final positional parameters. An absent keyword-only default means that argument is required. The tagged literal with a null value represents an explicit absent value. An untagged null can denote an omitted syntax operand.

| Construct | Evaluation |
|---|---|
| `branch`, `choose_value`, `short_circuit` | Evaluate the test first. Run the selected branch only. Conjunction and disjunction propagate the first deciding operand, or the final operand if none decides earlier. |
| `compare_in_sequence` | Evaluate adjacent operands in order. Each middle operand is evaluated once. Stop at the first false comparison. |
| `invoke`, `member`, `indexed_value` | Resolve the callable, attribute or indexed record in its bound context. Retain argument order, keyword names and collection expansions. A label used in external input or persisted data keeps its exact spelling. |
| `assign`, `update_in_place` | Evaluate the value and bind the targets according to the operation. An in-place update reads the selected target and writes its combined result. |
| `iterate`, `repeat_while` | Execute steps in order for each selected value or while the condition holds. A loop's final alternative runs on normal exhaustion. A break skips it. |
| `attempt`, `within_contexts` | Process matching failures in order, run the success block following a successful protected body and always run the finalization block. Enter contexts in order and unwind in reverse order, honoring failure suppression. |
| `complete`, `fail`, `emit` | Return a result, propagate failure or yield a value to the caller. An operation reaching the end normally completes with an absent value. |
| Wrappers and nested declarations | Evaluate wrapper expressions at definition time and apply them last to first. Nested operations are bound when their declaration executes. The enclosing class, module and installed capability supply external names. |

A tagged `adapter_term` contains a readable business label and a vocabulary key. Use the area's evidence vocabulary when an adapter needs the exact spelling of a callable, import, integration key or text value. The [source comparison reader](../../../docs/rebuild/verify/current-procedures.py) expands those terms and compares every published procedure operand, wrapper and branch with the recorded Git object. For example, run `python3 docs/rebuild/verify/current-procedures.py workforce ../hrms` from the repository root with the workforce source checkout available.

The tables describe structural decisions. Literal query text, field names and integration identifiers are operands of those decisions. The [decision interpretation](../decision-semantics.json), [business chapters](../../../docs/README.md), and [record dictionary](../../../schema/README.md) supply additional business meaning. The evidence indexes within each area locate the exact declaration used for comparison. Tests and observed postings have separate [qualification records](../../../docs/rebuild/qualification.json).
