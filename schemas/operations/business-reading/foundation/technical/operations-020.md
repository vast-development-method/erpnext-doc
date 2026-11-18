# Site operations and diagnostics · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-bc2dc0306767b7"></a>
### Debug timer

`operation_foundation_testing_utils_business_behavior_debug_timer`

**Inputs** func.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L7359) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1973) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L647)

<a id="op-52f44a8b9de0f0"></a>
### Debug timer.wrapper

`operation_foundation_testing_utils_business_behavior_debug_timer_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(func).

**Explicit results** result.

**Local steps**

- Set start\_time from time.monotonic().
- Set result from func(expanded args, expanded names kwargs).
- Set end\_time from time.monotonic().
- Evaluate logger.debug(formatted text  {func.\_\_name\_\_}  ⌛{(end\_time − start\_time)} seconds).
- Return result.

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L7607) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1974) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L648)
