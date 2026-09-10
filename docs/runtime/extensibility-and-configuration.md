# Extensibility and configuration

Extensibility is part of the application model. The reviewed system combines declarative record definitions with executable business behavior, event handlers, permission rules, naming rules, scheduled work, reports, and presentation definitions. A language-neutral replacement must preserve the extension points and their observable ordering without requiring any particular extension language.

## Effective metadata

The effective record definition is assembled from the base definition, added custom fields, property overrides, field caches and ordering, valid persistent columns, custom permissions, and custom links/actions. This order matters: a property override can alter a field added by customization, and permission evaluation must use effective metadata rather than a stale base file. The effective schema must be retrievable by the form and service layers.

A record declaration distinguishes stored root records, singleton settings, child rows, trees, and virtual records. Fields include data semantics and presentation semantics. A new field can therefore affect persistence, validation, permissions, form rendering, report selection, or all of them. A label change does not imply a new field identity. A replacement must track stable semantic identifiers separately from translated labels and display order.

Custom permission rows replace or augment the effective permission definition through their specific metadata mechanism. It is unsafe to concatenate every permission source without reproducing precedence. A property marked hidden or read-only in a form is not a sufficient server restriction; field permission levels and domain validation remain authoritative.

Evidence: source-artifact-444b5a1f4b08e77b3ae8 lines 145–224; source-artifact-1fd0d520ab1c4b24593c lines 8–96.

## Behavior replacement and composition

A record type has a base behavior provider. A configured replacement must retain the base provider's contract and, in the reviewed implementation, must derive from the original provider. When several replacements are registered for the same type, the last replacement wins. Declared behavior extensions are then composed in reverse registration order ahead of the selected base behavior. Later extensions therefore have earlier method resolution.

A neutral implementation can express this with ordered delegates, composition, or another suitable mechanism. It must preserve the ability to call inherited behavior, avoid accidentally suppressing a required base validation, and expose deterministic extension precedence. The exact order must be part of the combined system's capability map because workforce and customer-management extensions can alter shared employee, contact, communication, and transaction behavior.

Virtual records retain the document contract while supplying an alternative persistence provider. Required capabilities include load, insert, update, delete, list, count, and statistics. Computed child tables provide lazily evaluated collections that are reset after saving. Their declaration is not permission to materialize an arbitrary table and treat it as authoritative.

Evidence: source-artifact-0f25eaf4b484dd77cdbb lines 90–255; source-artifact-1369c9744914030ba553 lines 10–93.

## Event extensions

A document event runs its own behavior first. Document-specific registered handlers follow, then wildcard handlers for that event. Return objects are merged in order; a later key overwrites an earlier value. A non-object return replaces the accumulated return value. Handlers should therefore not be assumed to return an independent result list. Their primary business contract is usually mutations and side effects on the operation.

During registered event handlers, transaction-control calls are disabled so that an extension does not prematurely commit the business operation. The event dispatcher then processes notification rules, outgoing event delivery, and configured server-side document event rules. A business specification must identify whether an extension modifies values before validation, creates dependent records after submission, updates derived state after cancellation, or performs an external effect after commit.

New extension points must be named for the business event, with clear arguments, identity, transaction scope, error propagation, and permitted mutation. An unspecified generic callback after everything is complete cannot reproduce the distinction between before-validation and after-submission behavior.

Evidence: source-artifact-1c79c95fe9c8ab1bc9d4 lines 1645–1712; source-artifact-1c79c95fe9c8ab1bc9d4 lines 1773–1960; source-artifact-1c79c95fe9c8ab1bc9d4 lines 2060–2115.

## Named operations and authorization extensions

An exposed service operation must be explicitly registered. Registration declares guest access and allowed request methods. If no methods are supplied, the reviewed registration admits retrieval, submission, replacement, deletion, and query; a retrieval-enabled registration also admits query. Registration does not prove that an operation is read-only. The called operation still performs its own permission and business validation.

A named-operation override is resolved before the registered operation is invoked. A configured server-side operation can also replace a named target. Its outcome must conform to the published service contract if behavioral compatibility is required. Transport-facing operations cannot safely expose every public method of an internal service object.

Permission extensions provide per-document restrictions and query conditions. The reviewed controller permission layer can deny but not directly grant a missing role permission, while explicit document sharing is evaluated afterward for supported rights. Query conditions and document checks must remain consistent enough that restricted documents cannot appear in counts, exports, reports, or lookup results through an alternate path.

Evidence: source-artifact-66f1c84f2539463cb381 lines 580–655; source-artifact-70f793c473898fecc4cc lines 24–189; source-artifact-c07b20c42194f0dc2edd lines 358–508; source-artifact-c07b20c42194f0dc2edd lines 82–348.

## Configurable workflow and rules

Workflow configuration declares an ordered state list, structural state per workflow state, allowed role per transition, action label, optional condition, self-approval rule, optional field update, and ordered transition tasks. Field-update values can be literal or evaluated expressions. Conditions and expressions execute against a restricted context with the document, selected record queries, session identity, and date/time utilities. A replacement must define the permitted expression operations; it must not embed an arbitrary unrestricted language evaluator simply to mimic syntax.

Synchronous transition tasks execute before the corresponding save, submit, or cancel and share its transaction. Asynchronous tasks are queued after commit. An external delivery used synchronously can fail the transition; the same delivery used as ordinary post-commit notification has a different failure contract. The task catalogue must retain that distinction.

Naming rules are also executable configuration. Enabled rules are ordered by priority and the first matching rule that establishes identity wins. Document-specific amendment rules can choose normal naming or a predecessor suffix. Explicit decimal precision, rounding policy, smallest currency fraction, and number-format selection are calculation inputs. They belong in reproducible business configuration, not only user presentation preferences.

Evidence: source-artifact-c53dbe3cd685497ce317 lines 43–230; source-artifact-c869f513562448905114 lines 144–286; source-artifact-c869f513562448905114 lines 512–592; source-artifact-444b5a1f4b08e77b3ae8 lines 960–985; source-artifact-91eb5c3685f0ea77eecb lines 1253–1392.

## Operational configuration boundary

The blueprint includes settings that change business decisions or observable behavior: session policy, role and field access, guest uploads, import permissions, queue thresholds, enabled schedules, report preparation, rounding, naming, workflow, outgoing-event retry, and document locks. It deliberately does not require a particular web server, database product, queue product, process supervisor, deployment script, or upgrade migration path.

A setting must have a declared type, default, scope, allowed values, precedence, and effect. A change that affects future documents must not silently rewrite historical financial values. Domain documents decide when historical calculations are frozen and when an explicit reposting or recalculation operation is supported. Caches must be invalidated when effective metadata, permission rules, or event configuration changes; cached decisions are not an independent source of authority.

Evidence: source-artifact-444b5a1f4b08e77b3ae8 lines 145–224; source-artifact-6e027c5d8c38cd20566f lines 551–557; source-artifact-b1ad771a8c35d6eebd3d lines 84–218; source-artifact-c92b91c9ae73e577a3db lines 155–352.

## Extension acceptance obligations

- Install two extensions for the same record behavior and verify deterministic order and preservation of the base validator.
- Add a custom field, change its effective property, and verify persistence, validation, forms, authorized serialization, and reporting agree on its definition.
- Register a wildcard handler and a document-specific handler for the same event and verify order, merged result, and transaction boundaries.
- Attempt an early commit inside a registered document event and verify that the enclosing business transaction remains protected.
- Change an active permission rule and verify the effective decision after cache invalidation for document reads, lists, counts, and exports.
- Evaluate an invalid workflow expression and fail the transition without partially updating fields or submitting the document.
- Disable an exposed capability and verify that its named operations and scheduled work no longer run through ordinary access paths.
- Round the same transaction under every explicitly supported policy and preserve the chosen policy in the reproducible scenario configuration.

The extension mechanism does not make arbitrary extension behavior compatible automatically. Every installed extension that changes domain behavior must supply its own evidence, contract changes, and acceptance cases in the combined system specification.
