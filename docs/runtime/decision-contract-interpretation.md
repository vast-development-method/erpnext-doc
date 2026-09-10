# Decision contract interpretation

This chapter defines how to read the ordered decision catalogs as language-neutral behavioral structures. It explains every retained value kind, action, operator, pattern, binding, and control boundary. The companion [decision semantics catalog](../../schemas/operational-source-artifacts/decision-semantics.json) supplies the same rules in a machine-readable registry.

These structures preserve decisions and their order, but they do not automatically implement every helper, object protocol, wrapper, query, permission rule, or external service. A translated branch becomes behaviorally complete only after its dependencies, effective configuration, record meaning, financial consequences, and acceptance outcome are resolved. Structural coverage and executed equivalence are different measurements.

## Authority and interpretation order

Read the applicable domain chapter and mathematical contract first to establish what the operation means. Resolve its record definitions and service boundary, then use the decision tree to inspect conditions, evaluation order, assignments, calls, and failure paths. A tree does not override a reviewed business invariant merely because it contains more nodes. Conversely, do not discard an unusual retained branch because a more conventional rule appears attractive. Resolve a specific conflict and document an intentional correction before claiming equivalence.

The catalog distinguishes operational behavior, acceptance support, and excluded reference behavior. A test helper, deployment choice, or historical operation does not become a required application service merely because its structure is retained. An empty decision list in an unmatched operation must not be interpreted as a successfully specified no-op; its unresolved-decision field is authoritative about that limitation.

The canonical data and operational foundations remain [persistence, identity, and values](../data/persistence-identity-and-values.md), [document lifecycle and transactions](document-lifecycle-and-transactions.md), [permissions](identity-permissions-and-tenancy.md), and [background work](background-work-and-consistency.md). Local evaluation does not replace those business contracts.

## References and catalog namespaces

Catalog manifests can have an empty main array while storing every entry in ordered partitions. Read their fragment list and concatenate the designated arrays in order. A partition path is relative to its manifest directory. Other semantic references use the operations catalog namespace rather than the physical directory of the individual fragment.

| Reference key | Resolution |
| --- | --- |
| `procedure_semantics` | Resolve relative to the operations catalog namespace. The value decision-semantics.json identifies this contract. |
| `semantics` | Resolve a catalog-level semantic reference relative to the operations catalog namespace. |
| `interpretation_contract` | Resolve the file relative to the operations catalog namespace, then select its named semantic section. |
| `operation_identifier` | Look up the exact identifier in operation-index.json and its ordered partitions; resolve the returned contract catalog path from the repository root. |
| `locally_resolved_operations` | Resolve each exact operation identifier through operation-index.json. A link identifies a declared body, not permission to bypass dynamic dispatch. |
| `component` | Resolve the exact component identifier through its published component context catalog. Load relevant module and behavior context; the identifier is not a filesystem path. |
| `context_bound_capabilities` | Names requiring explicit scope, dependency, receiver or adapter resolution. They are not automatically global built-ins. |
| `partitioning.fragments.path` | Resolve relative to the catalog manifest directory. Concatenate the declared entry arrays in fragment order; an empty manifest array does not mean an empty catalog. |

The final operation lookup manifest is `schemas/operations/operation-index.json`. Its entries identify the exact decision-contract partition and component for each operation. A semantic fragment such as `identifier_literals` selects the named top-level section of the semantics catalog. It is a repository-local definition, not a location in unavailable material.

## Values, absence, and truth

A decision value carries a kind. A `number` node containing the text `"2"` denotes numeric two; a `text` node containing `"2"` denotes a character string. An explicit absent value, an unbound local name, a missing mapping key, a field withheld by permissions, and an omitted argument have different meanings. An unbound required name or failed index lookup must not silently become zero or absence.

For primitive values, absence, false, numeric zero, and empty text, bytes, sequences, sets, and mappings are false-like. Nonempty text such as `"0"` and `"false"` remains true-like. Other primitive nonzero or nonempty values are true-like. Custom objects can provide their own truth or length protocol; an unbound custom protocol is a dependency, not permission to choose a convenient answer.

Primitive truth values can participate as numeric zero and one in ordinary numeric equality and arithmetic, although an external schema can reject that interchange before evaluation. This means a keyed or unique collection can treat numeric one and true as equal keys. Preserve their distinct serialized kinds even where their primitive comparison result is equal.

Generic evaluation must not copy the forgiving financial-helper coercion into every operator. Invalid numeric text becomes zero only when the actual called conversion helper has that documented contract. Addition of numeric two and three gives five; addition of text `"2"` and `"3"` gives `"23"`; mixed text-and-number addition fails without an explicit compatible provider. The same principle applies to dates, durations, records, and references.

The selected numeric profile supplies integral/fractional behavior, overflow, nonfinite values, and representation. Monetary decisions additionally require the domain's calculation sequence and rounding boundaries. Exact decimal arithmetic can be a sound replacement choice, but the retained tree alone does not prove that changing every intermediate representation preserves all boundary outcomes.

## Complete value-kind registry

| Kind | Interpretation and limits |
| --- | --- |
| `absence` | Produce an explicit absent value. Do not resolve a missing name or failed lookup to this value automatically.  |
| `truth_value` | Produce the encoded true or false value.  |
| `number` | Produce a numeric scalar from its retained numeric text; it is not an ordinary text value. Preserve integer versus fractional interpretation and the bound numeric profile. The textual encoding alone does not authorize a different rounding policy. |
| `complex_number` | Produce a complex value with the specified real and imaginary numeric components. Ordering and business-money interpretation are not defined for ordinary complex values; resolve the consuming capability. |
| `byte_sequence` | Produce an ordered sequence of byte values, each from zero through 255. It is distinct from character text.  |
| `unspecified_dimension` | Produce the distinguished unspecified-dimension marker used by a consuming indexing or type protocol. It is not absence or a wildcard match by itself.  |
| `text` | Produce retained character text; a text that looks numeric stays text. Candidate identifiers require consuming-context resolution under identifier_literals. |
| `symbolic_value` | Resolve a canonical semantic or identifier value according to identifier_literals. Do not use a canonical field spelling as an external wire spelling without its adapter contract. |
| `value_reference` | Read the named bound value using lexical scope. Unbound and explicitly absent values are different outcomes.  |
| `member_value` | Evaluate the owner once, then retrieve its declared member through the bound receiver protocol. Member access can calculate, mask, lazily load or raise; it is not automatically a dictionary lookup or database column read. Use retained nonrecord member spelling for external receivers under identifier_literals. Use retained nonrecord member spelling for external receivers under identifier_literals. Use retained nonrecord member spelling for external receivers under identifier_literals. |
| `combine_values` | Evaluate left then right once each, then apply the selected binary operator and compatible value protocol.  |
| `unary_value` | Evaluate the operand once and apply the selected unary operator.  |
| `short_circuit_choice` | Evaluate operands in order only as needed. first_false_or_last returns the first false-like operand or the final operand; first_true_or_last returns the first true-like operand or the final operand. Return the actual selected value, not merely its truth. Later operands can have no evaluation or side effects. |
| `ordered_comparison_chain` | Evaluate initial once, then each right operand only when the preceding comparison permits continuation. The previous right operand becomes the next left operand without reevaluation. Primitive comparisons yield truth values. A custom rich-comparison result can itself require truth evaluation and can be returned unchanged by the final or short-circuited comparison; resolve that protocol. |
| `conditional_value` | Evaluate when once; evaluate and return only the selected then or otherwise expression.  |
| `operation_result` | Resolve, bind and invoke under binding_and_calls. The result can be immediate, awaitable, iterable, mutating or failing. A linked declared operation body does not bypass wrappers or receiver overrides. |
| `indexed_value` | Evaluate collection then selection and retrieve the selected member under that collection protocol. For primitive sequences use zero-based indices and negative offsets from the end; out-of-range index fails. Mapping indices are keys, including negative numeric keys. Missing keys fail unless an explicit provider supplies a default. |
| `interval_selection` | Construct a slice selector with independently evaluated bounds and step. It does not itself select a collection. For a primitive sequence, omitted step is one, step zero fails, end is exclusive, negative bounds are relative to length, bounds clamp, and negative step reverses traversal. Omitted end under a negative step differs from an explicit negative-one end. |
| `ordered_collection` | Evaluate members and expansions in order into a mutable ordered collection. Retain shared object references; do not deep-copy nested values.  |
| `fixed_order_collection` | Evaluate members and expansions in order into a collection with fixed membership. Nested referenced objects can still be mutable.  |
| `unique_collection` | Evaluate members and expansions and retain one value for each primitive equality/hash identity. Requires admissible hashable keys; display or iteration ordering is not guaranteed by this node. True and numeric one can be equal keys under primitive numeric equality. |
| `keyed_collection` | Evaluate each entry key then value in order; expand_mapping merges the entry value as a mapping. Later equal keys replace earlier values. Keys must be admissible under the bound mapping protocol. An absent key with expand_mapping false is an actual absence key; expand_mapping true means expansion, not that key. |
| `collection_projection` | Apply iteration clauses as nested loops in declared order, binding each target and testing its where_all predicates in order before descending or emitting. ordered retains every value; unique deduplicates; keyed evaluates each key before value with later equal keys replacing prior values; lazy_ordered defers production. Iteration bindings have a projection-local scope, with captured outer values governed by lexical rules. |
| `local_mapping_rule` | Create a callable value capturing its defining scope and evaluated defaults; bind call arguments normally and return the declared value expression when invoked.  |
| `composed_text` | Evaluate and concatenate the already textual or formatted parts in order. Failure in a part stops later evaluation.  |
| `formatted_value` | Evaluate the value, evaluate any dynamic format specification, apply the selected conversion, then the bound formatting protocol. text is user-oriented text conversion; representation is diagnostic representation; escaped_representation escapes characters outside the basic seven-bit character set in that representation; default invokes formatting directly. Exact quoting, escaping and numeric formatting require a declared profile, not a generic object serialization guess. |
| `expand_collection` | Expand the referenced iterable into the enclosing collection, argument list or destructuring target. It is context-sensitive; as a binding target it captures remaining values rather than reading an iterable to emit. |
| `assign_and_use` | Evaluate value once, assign it to the declared binding target, and return the same value. The target obeys its lexical binding context.  |
| `await_completion` | Evaluate an awaitable value and suspend until its protocol supplies a result or failure. Suspension does not imply background-job creation, parallel execution, transaction commit or durable completion. |
| `emit_value` | Evaluate and yield the value to the consumer, suspending this operation. On resumption, this expression receives the sent value, or absence for ordinary advancement. Yielding is not returning or posting; generator state and pending cleanup remain live. |
| `emit_each` | Delegate yield/resumption interaction to the selected iterable or generator, exposing its values in order and preserving delegated completion. The delegated completion value can become the expression result. Sending, throwing and closing require the generator protocol; do not replace delegation with a simple collected list. |
| `relational_selection_template` | Retain lexical relational clauses and typed tokens for semantic review under relational_selection_templates. Not an executable query or a fully parsed relational tree; caller bindings, nested structure and database semantics remain required. |
| `inferred_from_completion_branches` | Metadata describing an undeclared result shape. Inspect completion, fall-through, yield and failure branches; this node does not evaluate to a business value.  |
| `unresolved_value_construct` | A value construct is retained but not interpreted. The dependent path cannot be considered complete until its meaning is defined.  |
| `configurable_address` | Produce the retained text only after each address slot has been bound to a real configured address appropriate to its use. Optional display-only addresses can be deliberately omitted by the experience contract; a live service address requires a resolved and tested external capability. Never invent a host by renaming an application term. |
| `type_union` | A shape declaration admitting any of the listed alternative shapes. This is not integral bit union, an eager conversion, or permission to treat all alternatives as the same record type. |
| `named_shape` | A named type or value-shape declaration resolved in its type/capability context. Names can denote scalar, collection, record or provider-specific shapes; their descriptive spelling does not implement validation. |
| `absent_value_shape` | The shape of an explicit absent value. It is metadata admitting absence, not a runtime absent value or an omitted required argument.  |
| `unspecified_shape` | No shape declaration is supplied. This does not mean that every value is business-valid.  |
| `forward_declared_shape` | A retained forward shape reference requiring the applicable declaring type context before resolution. Do not execute the shape as a business expression or assume its referenced record already exists. |
| `parameterized_shape` | A shape constructor applied to its ordered type/shape arguments, such as a collection shape with an element shape. Constructor semantics, parameter arity and variance require the resolved type provider; this does not index or construct a business collection. |
| `contextual_shape_expression` | A shape expression whose interpretation depends on the declaring annotation/type context. Its retained value structure is not an instruction to perform business side effects during ordinary data validation. |
| `invalid_address_fixture` | Retain malformed address text as an inert negative-input fixture. The consuming address validator supplies the declared rejection. Do not parse during catalog loading, repair the address, or turn it into a successful empty endpoint; invalid test input is not an instruction to contact a host. |
| `embedded_behavior_contract` | Retain a link to the exact repository-local neutral behavior identified by contract.catalog and contract.identifier. Resolve catalog from the repository root and identifier within its entries or partitions. The linked behavior is inert until the enclosing capability explicitly requests execution under its scope and restrictions. |
| `embedded_decision_definition` | Produce inert embedded definition data. A bound evaluation capability chooses ordered-action mode or expression-result mode and grants its environment explicitly. Never evaluate decision_steps and expression_result successively for one expression invocation. declared_bindings inventories names; it does not initialize them. incomplete_composed_capability_import is an incomplete excluded compatibility fragment requiring its composition and capability binding before evaluation. |
| `embedded_syntax_fixture` | Retain a malformed, incomplete, other-grammar or nested-execution fixture without retaining an implementation program. A required rejection must remain a failure, not an empty successful definition. Failure in the inspected grammar does not establish rejection in another runtime or after valid template composition. A depth-limited fixture remains unresolved until explicitly bound. |

## Arithmetic and collection operators

Evaluate the left operand and then the right operand once each, except where a containing conditional or short-circuit node prevents evaluation. Select the operator by the actual operand kinds and their bound protocols. A name such as add is not proof of numeric addition: collection concatenation, set operations, and keyed merges have different outcomes.

| Binary operator | Interpretation and limits |
| --- | --- |
| `add` | For numbers, arithmetic addition; for compatible text, byte sequences or ordered sequences, concatenation. No implicit conversion of numeric-looking text. A keyed collection does not gain addition merely because it has members. Custom protocols require binding. |
| `subtract` | For numbers, arithmetic subtraction; for sets under their bound protocol, set difference. Other kinds require a compatible declared protocol. |
| `multiply` | For numbers, arithmetic multiplication. A sequence and an integral repetition count repeat membership in order; a nonpositive count gives an empty sequence. Repetition repeats references to mutable elements rather than creating independent copies. Fractional repetition counts fail. |
| `divide` | Numeric quotient under the selected numeric profile. Zero denominator fails. A guarded division capability can define zero-on-zero-denominator only when explicitly called. |
| `floor_divide` | For ordinary real numbers, floor the quotient toward negative infinity. Zero denominator fails. Negative seven floor-divided by three is negative three, not negative two. Result numeric family and representation follow the bound profile. |
| `remainder_or_text_substitution` | For ordinary numbers, remainder consistent with floor division and divisor sign. For a text or byte template, perform the template substitution protocol. For nonzero positive divisor, the ideal remainder lies from zero inclusive to divisor exclusive; negative seven remainder three is two. Floating representation can affect boundary identities. Text substitution must resolve placeholder names, positional values, width, precision, conversion and escaping; it is not arithmetic. |
| `power` | Exponentiation under the compatible numeric or custom protocol. Negative powers, zero to negative power, fractional powers and complex results require the selected profile; do not impose financial rounding here. |
| `shift_bits_left` | Shift integral bits left by a nonnegative integral count. Reject a negative count; width and overflow follow the bound integral profile. |
| `shift_bits_right` | Arithmetic right shift of an ordinary signed integral value by a nonnegative integral count. For unbounded signed integral behavior this agrees with floor division by the corresponding power of two; fixed-width providers must declare their rule. |
| `bit_union` | Integral bit union; for sets, union; for compatible keyed collections, merge with right-side values replacing equal left keys. For type-shape values this can denote a union shape instead of business arithmetic. Resolve the operand kind. |
| `bit_exclusive_union` | Integral exclusive bit union or set symmetric difference under the compatible protocol.  |
| `bit_intersection` | Integral bit intersection or set intersection under the compatible protocol.  |
| `matrix_multiply` | Matrix multiplication under an explicitly bound dimensional numeric provider. The generic decision contract supplies no default matrix shape, broadcasting or storage implementation. |

For exact ordinary real arithmetic with nonzero divisor \(b\), floor division and remainder satisfy \(a=b\lfloor a/b\rfloor+r\). For positive \(b\), \(0\le r<b\); for negative \(b\), \(b<r\le0\). Thus negative seven divided downward by three is negative three, with remainder two. Truncation toward zero would give different results. Finite precision can affect boundary identities; the numerical acceptance profile must account for those effects.

Text substitution is a separate branch of `remainder_or_text_substitution`: placeholders select positional or named arguments, conversions, width, precision, and escaping. It is not numeric modulo and not unrestricted expression evaluation. Retain the template and resolve its formatting capability before claiming the output is defined. Likewise, a repeated sequence containing one mutable object holds repeated references to that same object; it does not create independent deep copies.

| Unary operator | Interpretation |
| --- | --- |
| `negate_truth` | Apply the truth decision and return its opposite as a truth value. |
| `negate_number` | Apply numeric sign negation or the bound custom unary protocol. |
| `affirm_number` | Apply unary numeric affirmation; do not interpret numeric-looking text as a number implicitly. |
| `invert_bits` | Invert integral bits. For unbounded signed integral behavior the result is negative operand minus one. Other providers require an explicit rule. |

## Short circuit and comparisons

`first_false_or_last` returns the first false-like operand, or the last operand if every earlier value is true-like. `first_true_or_last` returns the first true-like operand, or the last operand if every earlier value is false-like. The result is the selected operand itself. Zero followed by a mutating call under the first-false rule returns zero without making that call; it is not merely the Boolean false.

A conditional value evaluates only one result branch. A comparison chain evaluates the initial value once and each successive right value only while the chain continues. Each middle value is reused as the next comparison's left value. In a chain comparing one, a callable result of two, and three, the middle callable executes once. A false comparison prevents evaluation of subsequent operands. Primitive comparisons return truth values; custom comparison results can themselves need truth evaluation and can remain the returned comparison object.

| Comparison | Interpretation and limits |
| --- | --- |
| `equal` | Primitive value equality. Numeric-looking text is not a number; compatible sequences compare their elements and sequence kinds; mappings compare key/value membership; sets compare membership. Custom equality and nonfinite numeric behavior require the value protocol. Primitive true and one can compare equal. |
| `not_equal` | Primitive inequality, with any custom inequality operation explicitly resolved.  |
| `less_than` | Strict order for compatible numbers or lexicographically ordered compatible primitive sequences/text; strict subset for sets. Incompatible kinds, ordinary mappings and complex values have no generic total order. |
| `less_than_or_equal` | Nonstrict compatible order or set subset, under the bound value protocol.  |
| `greater_than` | Strict reverse compatible order or strict set superset.  |
| `greater_than_or_equal` | Nonstrict reverse compatible order or set superset.  |
| `same_identity` | Whether both references designate the same runtime object or distinguished singleton. Not business-record-key equality. Two loaded representations of one record can have equal keys and different object identities. |
| `different_identity` | Whether the runtime object identities differ; it is not ordinary value inequality.  |
| `contained_in` | Membership of the left value in the right container: mapping keys, sequence/set members, or a text substring as applicable. The container membership or iteration protocol can be custom and can fail; it is not automatically a database query. |
| `not_contained_in` | Negate the membership decision after applying the same right-container membership protocol.  |

Runtime object identity is not business record identity. Two independently loaded representations of the same invoice can have equal record keys and different object identities. A singleton match for true also differs from numeric equality with one. Do not replace identity checks indiscriminately with value or database-key comparison.

## Indexing, intervals, and object sharing

Primitive sequence indexing begins at zero. A negative index counts from the end; an out-of-range index fails. Mapping indices are keys, so a negative numeric key does not select the last entry. Character-text indexing follows its declared character protocol, which must not be assumed to count user-perceived grapheme clusters. Custom record access can invoke computed or permission-aware properties.

An interval is a selector with independent start, exclusive end, and step. The omitted step is one and zero step is invalid. For a positive step, omitted start and end cover the beginning through the sequence length. For a negative step, omitted bounds select reverse traversal; an omitted reverse end is different from the explicit end negative one, which is first normalized relative to length. Bounds clamp under the primitive sequence protocol. The sequence `a, b, c` with absent bounds and step negative one returns `c, b, a`.

An ordered collection is mutable; a fixed-order collection has fixed membership, but either can refer to mutable objects. A unique collection removes equivalent members under its equality and hashing rules and supplies no guaranteed display order. A keyed construction evaluates each key and then its value; later equal keys replace earlier values. Primitive keyed collections retain first-insertion key order, and replacing a value does not move its key. Mapping expansion follows the supplied mapping iteration order. A keyed projection follows the same rule. An `expand_mapping` flag distinguishes merging a mapping from an actual absent-valued key.

## Identifiers and binding namespaces

A canonical record identifier, a canonical field identifier, a local variable binding, a public callable parameter, and an external payload key are different namespaces. A `symbolic_value` may identify its intended roles through `identifier_roles`; when used outside those roles, `text_when_not_used_as_identifier` preserves its ordinary text meaning. Ambiguous `canonical_identifier_candidates` require the actual consuming record or member context; selecting the first candidate would merge distinct identities.

Member access likewise distinguishes a canonical record field from an external object member. When `name_when_not_record_member` is present, use it for the appropriate nonrecord receiver under its capability contract. A normalized member name alone cannot establish that the receiver is a persisted business record.

When `canonical_member_candidates` is present, resolve the actual receiver's record definition before selecting a field. The `context_selected_member` marker is not a real field name and supplies no default choice. Imported-call resolution through `unconditional_import_or_unambiguous_reexport_subject_to_runtime_binding` similarly identifies a declared body without proving that module initialization, wrappers, or subsequent rebinding preserve that target.

Local collision suffixes distinguish bindings whose descriptive expansions would otherwise collide. Preserve them exactly. Resolve locals before captured enclosing bindings and module/shared contexts as applicable; a local parameter or assignment can shadow a declared helper. Reading a local before it is initialized is an error, not a fallback to a same-spelled global helper. A method's unqualified name is not automatically a sibling method from its enclosing behavior declaration.

Captured enclosing bindings remain live references; a later enclosing assignment can affect a closure when called. `bind_enclosing_values` declares that an operation accesses a module binding or an existing enclosing-operation binding. These are lexical scope rules, not instructions to create new business records or to copy current values.

## Call resolution and parameters

An `operation_identifier` links to a declared body. `resolution_basis` can establish lexical visibility or a receiver method subject to runtime override; `dispatch_requirement` remains binding. `locally_resolved_operations` therefore improves navigation without proving that every wrapper, receiver type, import alias, or module value is already available. Dynamic calls and `context_bound_capabilities` must be resolved explicitly.

Evaluate the callable value first, then positional arguments and their collection expansions in order, then named entries and mapping expansions in order. Resolve the actual callable, any bound receiver, and wrappers before applying its parameter declaration. A bound method supplies its receiver through the receiver protocol; it does not demand that a remote caller provide an extra business field named self.

| Parameter binding | Meaning |
| --- | --- |
| `positional_only` | Supplied by position; a same-spelled named argument cannot satisfy it |
| `positional_or_named` | Supplied once by position or named binding |
| `named_only` | Supplied by named binding or its declared default |
| `remaining_positional_values` | Collect excess positional values in order |
| `remaining_named_values` | Collect excess named values after ordinary parameter binding |

`required` means no retained default exists. An explicitly absent default is still a default, and an explicitly absent supplied argument is still supplied. Omission uses the default; supplying absence does not. Default expressions evaluate when the callable is defined, with the resulting default value retained for later invocations. A mutable default can consequently be shared across invocations; silently creating a fresh collection each time changes behavior.

`name` and `public_parameter_name` are collision-safe neutral parameter bindings. `external_parameter_text` preserves an incoming external keyword spelling. A resolved named argument uses its `binding_name` to select the exact declared callee parameter. `callee_public_name_requires_context_binding` requires the effective callable's parameter namespace; `expand_mapping_then_bind_at_callee` requires expansion followed by that same namespace resolution. A caller's local name is not an implicit callee parameter name.

Reject missing required parameters, duplicate supply of an ordinary parameter, duplicate named keys, unsupported excess positionals, and unsupported unknown names. Keyed collection merge accepts a later replacing key; call argument expansion rejects duplicate names. A positional-only name can be collected as an independent extra named value when a remaining-named parameter exists, but it still cannot satisfy the required positional value.

A capability binding must identify its provider/receiver, argument meanings and defaults, result kind, failure taxonomy, relevant object protocols, tenant/actor, permission checks, transaction effects, repeat behavior, and configuration. If one of those dimensions is necessary to decide the path's outcome and is unresolved, the tree is not yet an executable behavioral contract for that path.

## Definitions, wrappers, and effective behavior

Creating a local operation defines a callable and its captured environment; its ordinary body does not execute at definition. Creating a behavior establishes an inheritance and member namespace and evaluates declarations in that context; it does not insert an application record. `named_class_options` can alter the behavior-construction capability and must be bound where used.

Evaluate definition-wrapper expressions when defining the operation or behavior. Apply them from the last listed wrapper toward the first. A wrapper can change authorization, caching, regional selection, capability availability, transaction handling, or even the returned callable. Its existence is part of the contract rather than optional descriptive decoration.

Declared argument/result shapes and type aliases are interpretation metadata, not automatic value coercion. Specialized annotation evaluation, type parameters, inheritance, descriptors, and custom behavior construction remain capability requirements when they affect observable behavior. Component contexts must supply module initialization values and dependency declarations; an operation body alone does not reconstruct that context.

Shape nodes have their own meaning. `type_union` admits any listed shape; it does not perform bit arithmetic. `parameterized_shape` applies a type constructor to shape arguments; it does not index or instantiate a business collection. `absent_value_shape` admits an explicit absent value, while `unspecified_shape` means no shape declaration was retained. `forward_declared_shape`, `named_shape`, and `contextual_shape_expression` require their declaring context. A missing shape declaration is not permission to bypass domain validation.

## Complete action registry

Action lists execute in order until an action requests completion, failure, iteration control, or suspension. The containing control action determines how that outcome propagates. Ordinary fall-through completes an operation with absence unless it is a suspended generator or another protocol defines its result.

| Action | Interpretation and limits |
| --- | --- |
| `declare_value_shape` | Record a type or shape declaration without assigning a business value. Do not create an initialized value from shape metadata alone; definition-time annotation machinery is a separate capability. |
| `set_values` | Evaluate value once, then assign to each target in declared order. Destructuring binds corresponding members and an expanded remainder where declared. For a member/index target evaluate its receiver and selector when that target is assigned. Preserve aliasing. An assignment failure need not undo earlier local assignments. |
| `update_value` | Resolve the target location and read its current value once, evaluate the right value, invoke its in-place operation when supported or the compatible binary operation otherwise, and assign the resulting value back. Do not duplicate target evaluation by expanding it into two textual expressions. An in-place mutation can be visible through aliases even if a subsequent target write fails. |
| `complete_with_value` | Evaluate the value and request completion of the current operation, after required cleanup. For a generator, completion terminates iteration and can convey its final result according to that generator protocol. |
| `evaluate` | Evaluate for its returned value or effects and discard the ordinary result. Failures and suspensions still propagate.  |
| `choose_branch` | Evaluate the condition once, execute only the selected action list, then continue with the enclosing list unless an abrupt outcome propagates.  |
| `for_each` | Evaluate over once, obtain its iterator, bind each yielded member and execute steps. A next-iteration outcome requests the next member. Execute after_natural_completion only on normal exhaustion, including an initially empty iterable; not after stop_iteration, operation completion or failure. Asynchronous iteration awaits its iterator protocol. |
| `repeat_while` | Reevaluate when before each iteration and execute steps while true-like. Execute after_natural_completion when the test naturally becomes false, including initially false; not after stop_iteration, return or failure. |
| `handle_failures` | Execute protected steps, select applicable failure handlers in order, run after_success only on normal fall-through with no protected failure, and run always on every exit. Failure taxonomy, group selection, cleanup priority and temporary failure bindings are defined in failure_and_cleanup. Failure handling alone does not roll back business transactions. |
| `use_scoped_resources` | Acquire resources in order, enter each scope, bind entry results when requested, execute the body, and exit successfully entered scopes in reverse order. Later acquisition or entry failure still cleans up prior entered scopes. Exit can suppress a failure or replace an outcome according to its bound protocol; asynchronous resources await entry and exit. |
| `fail` | Raise the evaluated failure or re-propagate the active failure when propagate_active_failure is true. An explicit absent cause suppresses displayed causal chaining; an omitted cause retains implicit active context. cause_present distinguishes them. An invalid absence failure does not mean successful completion. |
| `require_condition` | Evaluate condition; if false-like, evaluate the failure description and raise the applicable assertion failure. acceptance_assertion describes a check in an acceptance-support procedure. runtime_assertion is retained control behavior; execution environments that disable such checks must declare that policy. Assertions are not a substitute for public business validation. |
| `remove_values` | Remove bindings or selected object members in target order using their deletion protocols. It does not mean delete business document. Missing bindings or keys can fail; indexed collection deletion can shift later positions. |
| `stop_iteration` | Stop the nearest active loop and skip its after_natural_completion list; execute any intervening cleanup. An enclosing loop continues under its own rules.  |
| `next_iteration` | Advance the nearest active loop after required cleanup. Do not execute later actions in the current iteration.  |
| `no_effect` | Continue without an operation effect.  |
| `bind_enclosing_values` | Declare module or captured enclosing-operation binding scope for those names. It is a lexical resolution rule, not a runtime business mutation.  |
| `bind_capability_dependencies` | Bind named external or shared capabilities to their declared local names from the applicable component context. Dependency loading, initialization, wildcard expansion, aliases and public parameter namespaces require provider resolution; this action does not implement the provider. |
| `define_local_operation` | Create an operation value in the current scope, capturing enclosing bindings and evaluating defaults and definition wrappers at creation. Body executes on invocation or generator advancement, not merely because the definition was encountered. Apply wrappers in reverse listed application order. |
| `define_record_behavior` | Construct a behavior namespace from the declared inherited providers, execute declarations in that context, apply applicable construction options and wrappers, and bind the resulting behavior value. Inheritance resolution, descriptor lookup and custom construction are capability contracts. A behavior definition is not insertion of a business record. |
| `select_matching_pattern` | Evaluate subject once, try alternatives in order, and execute the first matching pattern with a true-like applicable guard. Use guard_present to distinguish no guard from an explicit absent-value guard. Match bindings, failure side effects and pattern protocols are defined in pattern_semantics. |
| `declare_type_alias` | Declare a named type or shape alias, not a persisted business value. Type parameters or deferred annotation evaluation require the type capability context where observably used. |
| `unresolved_statement` | Retain an unsupported action for review. Its dependent path cannot be treated as implemented or as no effect.  |

## Assignment and transactional effects

`set_values` evaluates its value once and assigns targets in order. Destructuring distributes corresponding values; an expanded target captures the remaining ordered values. Member and indexed targets resolve their receiver and selector at assignment time. Assignment shares references and is not a deep copy.

`update_value` resolves and reads its target once, then evaluates its right value. Its in-place protocol may mutate an object visible through other aliases before a later target write fails. Replacing this with a duplicated textual target expression can invoke accessors twice and change the result. `remove_values` removes a binding or object member; it is not the business delete-document command.

None of these actions automatically saves a record, checks accounting periods, enforces workflow, writes balanced ledger rows, commits, rolls back, or emits a notification. An `operation_result` can invoke any of those effects only through its actual bound capability. Similarly, catching a failure is control flow and does not itself roll back storage or reverse an external payment. The transaction scope comes from the [document lifecycle contract](document-lifecycle-and-transactions.md#transaction-boundaries-and-concurrency).

## Iteration, projections, and natural completion

A `for_each` evaluates its iterable once, obtains its iterator, binds each yielded value, and executes the body. `repeat_while` reevaluates its test before each iteration. Both execute `after_natural_completion` only on exhaustion or a naturally false test, including an initially empty or false case. `stop_iteration` skips that completion branch. `next_iteration` continues the nearest loop after cleanup. Return or failure also skips natural completion.

Projection iteration clauses behave as nested loops. Each clause binds its target and evaluates its `where_all` filters in order before descending to the next clause or producing a value. Eager ordered, unique, and keyed projections finish their construction before returning; unique projections deduplicate and keyed projections replace earlier equal keys. Projection loop bindings belong to the projection scope rather than overwriting an ordinary surrounding loop variable.

Lazy projections defer values and filtering until consumed, while establishing the outermost iterator in the defining context at construction. Inner iterables are evaluated when their enclosing iterations reach them. Captured variables remain references. Assignment-and-use expressions follow their lexical target; they are not automatically converted into private projection-local bindings.

Mutating a collection while iterating it is not automatically safe or snapshot-based. The selected iterator can observe changes or fail. Financial operations that require a stable set of records must establish that through their query, lock, or snapshot contract rather than assume the iteration node supplies it.

## Failure handlers and unconditional cleanup

For ordinary failure handling, select the first matching handler under the bound failure taxonomy. `category_present` false denotes a catch-all handler. An explicit absent category is different and is not a valid catch-all. A named handler binding exists during the handler and is cleared afterward, including abrupt exit; do not assume an earlier same-spelled local value is restored.

`after_success` executes only after the protected body falls through normally, without a failure, handler, return, break, or continue. A failure in `after_success` is not caught by the same handler list. The `always` list executes after protected work, a handler, or the success branch on every exit. Normal cleanup preserves the pending outcome; a new cleanup failure or explicit completion can replace a pending return or failure. A return value computed before cleanup remains the pending value, although cleanup can still mutate an object that value references.

When `handles_failure_group` is true, handlers can process matching subgroups and several handlers can run for different failures. Unhandled and newly raised failures propagate together. This is not the ordinary first-handler-for-the-whole-failure rule and requires the group failure capability to be defined.

A `fail` action with `propagate_active_failure` rethrows the active failure; it does not create a new empty failure. `cause_present` distinguishes an omitted cause from an explicit absent cause. Omission preserves applicable implicit failure context; explicit absence suppresses displayed causal chaining. Failure display policy and business rollback remain separate.

For scoped resources, acquire and enter in order and clean up successfully entered resources in reverse order. If later acquisition fails, earlier entered resources still exit. An exit can suppress a pending failure under its provider protocol, or itself raise another failure. A resource can be a file, lock, identity override, or transaction scope; the generic scoped-resource node does not by itself promise commit or rollback.

Older translated entries without presence flags can conflate no guard with an absent guard, a catch-all with an explicit absent category, or an omitted cause with an explicitly absent cause. If that distinction affects an outcome, it remains unresolved until the entry is regenerated or a reviewed rule supplies the missing distinction.

## Pattern selection and captures

Evaluate a pattern-selection subject once. Try alternatives in order. After a pattern matches and captures are available, evaluate its guard if `guard_present` is true. No guard permits the matched alternative; an explicit absent guard is false-like and continues to the next alternative. Execute only the first body whose pattern and guard pass. If none passes, continue after the selection.

| Pattern | Interpretation and limits |
| --- | --- |
| `any_value` | Match any subject without imposing a value constraint.  |
| `equal_value` | Evaluate the pattern value and test matching equality with the subject under the applicable value protocol.  |
| `singleton` | Match the distinguished absence, true or false singleton by its singleton identity. A true singleton pattern must not match numeric one merely because numeric equality can compare them equal. |
| `ordered_sequence` | Match an admissible sequence by element patterns. Without a remaining-sequence pattern require exact length; with one, match fixed prefix/suffix and capture the intervening ordered values. Ordinary text and byte sequences do not participate as generic sequence patterns. Sequence matching eligibility is a type protocol. |
| `mapping` | Match required keys and their value patterns against a mapping; extra keys are allowed. Bind a new mapping of unmatched entries when bind_remainder is present. Missing required keys cause no match. Key lookup and equality require the mapping protocol and must not become an unrestricted record read. |
| `record_shape` | Require an instance compatible with the selected behavior/type, then match declared positional and named members. Positional-to-member correspondence comes from that type matching protocol. Member access can have effects; missing members can fail the match while other access failures can propagate. |
| `remaining_sequence` | Within a sequence pattern, match remaining members and bind them as an ordered collection if requested; absent bind discards them.  |
| `bind_matching_value` | Match its subpattern and, on match, bind the subject to the declared name when present. A nested any_value represents an unconditional capture or discard.  |
| `first_matching_alternative` | Try alternatives in order and use the first matching one. Alternative capture sets must be compatible. Pattern matching does not guarantee absence of side effects from earlier failed alternatives. |
| `unresolved_pattern` | Retain an unsupported pattern for review and block claims of complete dependent behavior.  |

Successful capture bindings belong to the enclosing operation, not a new block-only scope. A guard-false attempt may leave successful captures visible. Partial captures on failed patterns have no guaranteed portable rollback or survival; an implementation must not rely on a particular outcome without an explicit accepted fixture. Member access, equality, and type matching can invoke capabilities, so a failed alternative is not proof that it had no effects.

## Generators, asynchronous work, and suspension

An operation whose own body yields values is a generating operation. Merely constructing its generator does not execute the body. Yields inside a separate nested definition do not make the containing operation a generator. `emit_value` suspends with one value and receives a sent value on resumption, or absence for ordinary advancement. `emit_each` delegates consumption, resumption, failure, closing, and final result to its selected generator or iterable protocol; collecting all values into a list loses those semantics.

An asynchronous operation creates a deferred operation value under its asynchronous protocol. `await_completion` suspends until the awaited result, failure, or cancellation is available. Asynchronous iteration and resource scopes await their iterator, entry, and exit protocols while retaining declared order. These constructs do not automatically create parallel workers, persistent jobs, commits, or durable notifications.

Pending cleanup must run according to generator close, failure, cancellation, and completion protocols. Abandoning an unconsumed generator does not establish immediate deterministic cleanup. Durable business processing remains governed by [background work and consistency](background-work-and-consistency.md), not by the presence of an await or yield node.

## Relational selection templates

A `relational_selection_template` preserves lexical clauses and tokens from an embedded query. It is useful for identifying projections, input relations, predicates, grouping, sorting, parameters, and writes. It is not a fully parsed query, complete relational algebra, or executable prepared statement.

| Token role or modifier | Interpretation |
| --- | --- |
| `text` | A retained quoted token. quotation records single versus double quotation; preserve its doubled or backslash escape fragments until the selected dialect interprets them. Double quotation can denote a value or an identifier depending on that dialect. |
| `record_or_field` | A normalized quoted identifier candidate. Resolve it against canonical record and field definitions, aliases, and dynamic effective metadata; do not assume it is already a valid physical storage name. |
| `bound_parameter` | A named bound-value placeholder. external_parameter_text retains its external parameter spelling; resolve the canonical placeholder through the caller mapping and consuming context. |
| `number` | A textual encoding of a query numeric literal under the relational provider numeric rules. |
| `term` | A normalized unquoted token that can denote an identifier, alias, function, keyword, direction, type or other grammatical term. Determine its role through a full query contract. |
| `symbol` | A retained punctuation or operator token. Its role depends on surrounding query grammar. |
| `positional_parameter` | Zero-based ordinal of a positional bound-value placeholder within this template. Bind it to the corresponding supplied query value; do not infer ordinal from surrounding numeric literals. |
| `format_parameter` | A textual-format placeholder retained separately from bound query values. Resolve its formatting operation and grammar effect independently; it is not automatically a safe bound-value placeholder. |
| `qualifier` | Identifier qualifier retained separately from the final canonical member, commonly a relation or alias. Resolve its scope before choosing the record/field identity. |
| `quotation` | Single or double quotation metadata for a text token. Apply the selected dialect once; do not decode retained escaping twice. |
| `canonical_member_candidates` | Possible canonical identities of a member token. Resolve relation/alias context; no candidate is a permitted default. |
| `name_when_not_record_member` | Alternate member interpretation when the token is not a canonical business-record field; requires the consuming grammatical or capability context. |
| `external_parameter_text` | Retained named-placeholder spelling for matching the original caller parameter namespace; canonical field naming alone does not change this binding. |

| Clause role | Interpretation |
| --- | --- |
| `select` | Projection expressions and selected fields; duplicates and aggregates must be specified. |
| `from` | Input relation and aliases. |
| `where` | Pre-group filtering predicate. |
| `join` | Join relation; join kind and condition must be recovered from the complete contract. |
| `left_join` | Preserve unmatched left rows with absent right values under the relational rules. |
| `right_join` | Preserve unmatched right rows with absent left values under the relational rules. |
| `inner_join` | Retain matching combinations according to the join predicate. |
| `cross_join` | All combinations of the selected relations. |
| `on` | Join predicate; moving it to where can change outer-join behavior. |
| `group_by` | Grouping keys; aggregate measures require their own calculation and null rules. |
| `having` | Predicate applied to grouped or aggregated results. |
| `order_by` | Ordered sort expressions, direction, null positioning and tie behavior. |
| `limit` | Maximum-result or provider-specific limit expression. |
| `offset` | Result starting displacement under the query ordering. |
| `union` | Combine compatible result relations with duplicate removal according to the provider. |
| `union_all` | Combine result rows retaining duplicates. |
| `update` | Mutation target; requires explicit update service and authority. |
| `set` | Field assignments for a mutation, not an automatic local set_values action. |
| `delete` | Deletion relation and predicate; not equivalent to validated business-document cancellation. |
| `insert_into` | Insertion destination and optional destination columns. |
| `values` | Inserted or inline relation values. |
| `with` | Named subqueries or common relations with nested dependency context. |
| `for_update` | Requested locking read within its surrounding transaction. |
| `prefix` | Unclassified leading material. It must be interpreted or rejected before execution. |

Before implementing a query, resolve nested query boundaries, aliases, relation and field identity, bound parameters, joins, null-aware three-valued predicates, collation, numeric aggregates, dates, ordering, duplicates, limits, and lock scope. Moving a join predicate into a later filter can change outer-join results. Missing ordering does not create a deterministic valuation sequence. A direct storage query does not automatically acquire document permissions.

Quoted values are recognized before clause and comment tokens, so quoted clause keywords and comment-like text remain part of their literal token. Quotation and escape fragments remain available for the selected dialect, and named, positional, and textual-format placeholders retain different roles. The template still does not parse nested query scope, every multiword construct, or provider-specific grammar. When interpretation remains ambiguous, the reviewed domain/service contract must supply it or the query remains unresolved. Never concatenate normalized tokens into executable storage statements. Template node coverage alone does not prove report or mutation correctness.

## Configurable addresses

A `configurable_address` retains surrounding text and explicit named address slots. Bind each slot to a real electronic mail address or resource address appropriate to its declared use. Substitution resolves only the declared address slots; it must preserve other literal content and any separately defined formatting placeholders. An unresolved slot is a configuration dependency, not an empty successful endpoint.

An optional help or display address can be omitted only where its experience contract permits that choice. A live integration address requires an external capability contract covering destination, authentication, operation, response, failure, and retry. Never fabricate a hostname by replacing an application term. The `configurable_addresses` section of the semantics catalog supplies these interpretation rules for every referencing decision node.

## Embedded behavior and invalid syntax fixtures

An embedded behavior definition represents declarative behavior supplied as data to another operation. Loading or reading that literal must not execute its declarations, invoke its capabilities, or mutate records. Its consuming configuration or evaluation service decides whether it accepts a definition, evaluates a value expression, runs ordered actions, inspects the structure, or rejects the input. That service also defines the returned result or output namespace.

`embedded_behavior_contract` resolves its exact linked catalog and identifier within this repository. `embedded_decision_definition` retains ordered actions and can also retain `expression_result`. The consumer chooses statement mode or expression mode; it must not execute both representations for one invocation. `declared_bindings` inventories names without initializing them. An incomplete composed capability import cannot run alone and does not become a required business feature merely because an excluded compatibility fragment is retained.

Before evaluation, bind the explicitly permitted environment, arguments, record context, actor, capabilities, and failure policy. An embedded definition does not implicitly inherit unrestricted caller locals, administrative authority, arbitrary dependency loading, or transaction control. Its retained actions use the same interpretation rules as other decisions, but evaluation restrictions remain properties of the consuming service. A successful syntax interpretation proves neither permission nor business validity.

A negative syntax fixture records a syntax-rejection condition and its acceptance purpose. It must not become a valid empty definition or silently succeed. Preserve the declared rejection category, but do not infer intended runtime rejection solely because a fragment failed translation: incomplete templates or another expression grammar require their actual consuming context. Exact original spelling, line positions, and source-specific diagnostic text are not recoverable from a neutral structure; where those matter to an external consumer, they require an explicit compatibility decision rather than invented output. An ordinary text field that merely resembles a program must likewise remain governed by its actual consumer, not automatically execute because it was classified as a possible definition.

`invalid_address_fixture` is inert malformed-address test data. Catalog loading must not parse it, repair it, or contact a destination. Its actual consuming validator determines the declared rejection. `embedded_syntax_fixture` likewise preserves a malformed, incomplete, other-grammar, or unbound nested-execution case; the marker is not a successfully executable empty definition.

The common acceptance cases are: store an embedded definition without running it; evaluate a permitted pure expression under restricted bindings; reject a missing capability; reject an invalid definition; prevent an embedded action from acquiring privileges absent from its consumer; and roll back a failing business invocation according to the actual transaction contract. The same embedded structure can be inert configuration in one operation and evaluated behavior in another, so consumer context is a required input.

## Worked neutral decision example

This small acceptance procedure validates a positive conversion factor and computes stock quantity. It intentionally has no persistence effect. It illustrates numeric encoding, parameter binding, comparison, assertion, multiplication, and completion; the production transaction additionally requires the product, unit, precision, permissions, and lifecycle rules from the relevant domain.

```json
{
  "identifier": "example_positive_quantity_extension",
  "parameters": [
    {
      "name": "commercial_quantity",
      "public_parameter_name": "commercial_quantity",
      "binding": "positional_or_named",
      "required": true
    },
    {
      "name": "stock_units_per_commercial_unit",
      "public_parameter_name": "stock_units_per_commercial_unit",
      "binding": "positional_or_named",
      "required": true
    }
  ],
  "decision_steps": [
    {
      "action": "require_condition",
      "role": "acceptance_assertion",
      "when": {
        "kind": "ordered_comparison_chain",
        "initial": {
          "kind": "value_reference",
          "name": "stock_units_per_commercial_unit"
        },
        "comparisons": [
          {
            "operator": "greater_than",
            "right": {
              "kind": "number",
              "value": "0"
            }
          }
        ]
      },
      "failure_description": {
        "kind": "text",
        "value": "Stock units per commercial unit must be positive"
      }
    },
    {
      "action": "complete_with_value",
      "value": {
        "kind": "combine_values",
        "operator": "multiply",
        "left": {
          "kind": "value_reference",
          "name": "commercial_quantity"
        },
        "right": {
          "kind": "value_reference",
          "name": "stock_units_per_commercial_unit"
        }
      }
    }
  ],
  "example_inputs": {
    "commercial_quantity": 5,
    "stock_units_per_commercial_unit": 6
  },
  "expected_result": 30,
  "persistence_effect": "none; this example computes a quantity and does not save or submit a document"
}
```

For commercial quantity five and factor six, the result is thirty. A factor of zero or negative factor fails the acceptance condition. A text factor `"6"` does not become a numeric six merely because it looks numeric; the caller must supply the numeric type or invoke a specifically defined conversion before this procedure.

## Acceptance checklist with expected outcomes

| Scenario | Expected outcome |
| --- | --- |
| Numeric text remains text | Numeric add gives five; text add gives the two-character text 23; mixed add fails without an explicit compatible conversion. |
| Short circuit preserves chosen value | first_false_or_last returns numeric zero and does not evaluate the second operand. |
| Floor and remainder for negative dividend | {"floor_divide": -3, "remainder": 2} |
| Comparison evaluates middle once | The condition first less than middle less than last is true and invokes the middle-producing operation once. |
| Empty iteration natural completion | No loop body runs; after_natural_completion runs once. |
| Break suppresses natural completion | The second member is not visited and after_natural_completion does not run. |
| Explicit absence differs from default | The bound argument is absent, not five. Omission, rather than explicit absence, selects the retained default. |
| Mapping merge and argument expansion differ | A keyed_collection merge retains quantity two; passing duplicate named quantity arguments fails binding. |
| Negative-step omitted stop | ["c", "b", "a"] |
| Pattern singleton is identity based | The true singleton pattern does not match numeric one even though primitive numeric equality can compare them equal. |
| Cleanup preserves or replaces pending outcome | Normal always cleanup preserves result seven; a new cleanup failure propagates instead of that result. |
| Assignment does not post | The local assignment alone does not establish a submitted business transaction, valid workflow, or ledger posting. |

In addition, verify a shared mutable default across two invocations, a shadowed helper name, an overridden receiver method, a wrapper that denies access, an explicit absence guard, a temporary failure binding, a caught error without rollback, an external payment timeout after acceptance, and a query with a clause keyword inside a quoted value. These cases test the difference between retained structure and fully resolved behavior.

A completion claim must identify which operation paths have resolved capabilities and acceptance outcomes. Remaining unknown operations, unsupported value protocols, query-template ambiguities, or missing component initialization must remain visible. Describing those limits precisely prevents an implementation agent from treating a readable decision tree as proof of financial correctness.
