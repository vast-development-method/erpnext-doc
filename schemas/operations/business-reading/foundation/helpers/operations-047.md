# Shared value and file services · operations 47

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Safe exec

<a id="op-4369890cedec0b"></a>
### Get safe request session

`operation_foundation_utils_safe_exec_business_behavior_get_safe_request_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L1769) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1787) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L569)

<a id="op-cb1ec8b4fee871"></a>
### Make safe request

`operation_foundation_utils_safe_exec_business_behavior_make_safe_request`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** method, url, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L1935) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1803) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L585)

<a id="op-6cf97f11105026"></a>
### Make safe get request

`operation_foundation_utils_safe_exec_business_behavior_make_safe_get_request`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** url, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L2139) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1799) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L581)

<a id="op-307aa6a1814012"></a>
### Make safe post request

`operation_foundation_utils_safe_exec_business_behavior_make_safe_post_request`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** url, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L2214) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1801) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L583)

<a id="op-f76426e0f43136"></a>
### Make safe put request

`operation_foundation_utils_safe_exec_business_behavior_make_safe_put_request`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** url, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L2289) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1802) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L584)

<a id="op-ed1c639b47b5d5"></a>
### Make safe patch request

`operation_foundation_utils_safe_exec_business_behavior_make_safe_patch_request`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** url, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L2364) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1800) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L582)

<a id="op-ced0b9235b64de"></a>
### Make safe delete request

`operation_foundation_utils_safe_exec_business_behavior_make_safe_delete_request`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** url, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L2439) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1798) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L580)

<a id="op-0af9711b0ff279"></a>
### Render safe globals

`operation_foundation_utils_safe_exec_business_behavior_render_safe_globals`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L66) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1808) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L590)

<a id="op-bc58ae3041c0a9"></a>
### Exec safe globals

`operation_foundation_utils_safe_exec_business_behavior_exec_safe_globals`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L64) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1777) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L559)

<a id="op-420392447a5dd3"></a>
### Get keys for autocomplete

`operation_foundation_utils_safe_exec_business_behavior_get_keys_for_autocomplete`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** key, value, prefix, offset, meta, depth, max\_depth.

**Explicit result forms** no value.

**Local structure** 10 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L5318) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1784) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L566)

<a id="op-c30cae7cbe9ec6"></a>
### Is job queued

`operation_foundation_utils_safe_exec_business_behavior_is_job_queued`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** job\_name, queue.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L6171) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1795) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L577)

<a id="op-3395067bb2a7a5"></a>
### Safe enqueue

`operation_foundation_utils_safe_exec_business_behavior_safe_enqueue`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** function, kwargs.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** notification or queued-work request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L6343) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1810) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L592)

<a id="op-204bb1a4c9aae3"></a>
### Call whitelisted function

`operation_foundation_utils_safe_exec_business_behavior_call_whitelisted_function`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** function, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L6463) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1773) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L555)

<a id="op-78dfc2783ca5a5"></a>
### Run script

`operation_foundation_utils_safe_exec_business_behavior_run_script`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** script, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L6542) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1809) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L591)

<a id="op-20efead6f38284"></a>
### Call with form dict

`operation_foundation_utils_safe_exec_business_behavior_call_with_form_mapping`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** function, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L6644) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1774) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L556)

<a id="op-d3bdab03d9b7b7"></a>
### Flatten

`operation_foundation_utils_safe_exec_business_behavior_flatten`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** module.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L6838) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1778) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L560)

<a id="op-b7fcab94194441"></a>
### Get python builtins

`operation_foundation_utils_safe_exec_business_behavior_get_implementation_language_builtins`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L7027) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1783) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L565)

<a id="op-d781eb2c79a04c"></a>
### Get hooks

`operation_foundation_utils_safe_exec_business_behavior_get_hooks`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** hook, default, app\_name.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L7238) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1782) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L564)

<a id="op-3abb1d1561166c"></a>
### Read sql

`operation_foundation_utils_safe_exec_business_behavior_read_database_query`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** query, args, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L7395) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1806) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L588)

<a id="op-20faf4ce4b27b6"></a>
### Check safe sql query

`operation_foundation_utils_safe_exec_business_behavior_check_safe_database_query_query`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** query, throw.

**Explicit result forms** Boolean true, the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L63) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1775) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L557)

<a id="op-9e0c8d6ecc15d5"></a>
### Reject sql query

`operation_foundation_binding_foundation_utils_safe_exec_reject_sql_query`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** message, throw.

**Explicit result forms** Boolean false.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L206) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L276) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L364)

<a id="op-8e15c77aff92d8"></a>
### Getitem

`operation_foundation_utils_safe_exec_business_behavior_getitem`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** obj, key.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** SyntaxError.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L374) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1794) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L576)

<a id="op-19e8ce6f7aaaf1"></a>
### Getattr for safe exec

`operation_foundation_utils_safe_exec_business_behavior_getattr_for_safe_exec`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** object, name, default.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** SyntaxError.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L502) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1793) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L575)

<a id="op-781709b737e6c0"></a>
### Get attr for eval

`operation_foundation_utils_safe_exec_business_behavior_get_attr_for_evaluate`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** object, name, default.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L752) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1781) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L563)
