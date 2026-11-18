# Shared value and file services · operations 46

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Safe exec

<a id="op-97aeefb241b922"></a>
### Safe Doc.meta

`operation_foundation_utils_safe_exec_business_behavior_safe_record_meta`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L4407) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1823) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L605)

<a id="op-853d4bdc93a13e"></a>
### Safe Doc.get formatted

`operation_foundation_utils_safe_exec_business_behavior_safe_record_get_formatted`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, fieldname, doc, currency, absolute\_value, translated, format.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 7 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L4570) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1818) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L600)

<a id="op-8f020bb451e8d9"></a>
### Safe Doc.get label from fieldname

`operation_foundation_utils_safe_exec_business_behavior_safe_record_get_label_from_fieldname`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, fieldname.

**Explicit result forms** a value selected from the current context.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L5275) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1819) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L601)

<a id="op-3946d5afa74967"></a>
### Safe Doc.in format data

`operation_foundation_utils_safe_exec_business_behavior_safe_record_in_format_data`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, fieldname.

**Explicit result forms** Boolean true, a comparison result.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L5482) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1820) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L602)

<a id="op-95bf95fbffef9c"></a>
### Safe Doc.is print hide

`operation_foundation_utils_safe_exec_business_behavior_safe_record_is_print_hide`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, fieldname, df, for\_print.

**Explicit result forms** Boolean true, a value selected from the current context.

**Local structure** 7 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L5627) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1822) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L604)

<a id="op-a65011f76eba3d"></a>
### Get doc as dict

`operation_foundation_utils_safe_exec_business_behavior_get_record_as_mapping`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** args, kwargs.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L6082) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1786) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L568)

<a id="op-6d8f1de0f0ab2d"></a>
### Safer get last doc

`operation_foundation_utils_safe_exec_business_behavior_safer_get_last_record`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** args, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L6174) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1826) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L608)

<a id="op-e167657c302776"></a>
### Safer get cached doc

`operation_foundation_utils_safe_exec_business_behavior_safer_get_cached_record`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** args, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L6266) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1825) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L607)

<a id="op-f6efe614693e34"></a>
### Remove unsafe fields

`operation_foundation_utils_safe_exec_business_behavior_remove_unsafe_fields`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** fields.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L6358) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1807) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L589)

<a id="op-3d89fee5f1e83d"></a>
### Safe get list

`operation_foundation_utils_safe_exec_business_behavior_safe_get_list`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** args, kwargs.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L6430) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1815) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L597)

<a id="op-cee0aebc53a9a9"></a>
### Safe get all

`operation_foundation_utils_safe_exec_business_behavior_safe_get_all`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** args, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L6747) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1814) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L596)

<a id="op-043a4d67f85e5a"></a>
### Safer get meta

`operation_foundation_utils_safe_exec_business_behavior_safer_get_meta`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doctype, cached.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L6876) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1827) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L609)

<a id="op-09c34f54a64d51"></a>
### Safer log error

`operation_foundation_utils_safe_exec_business_behavior_safer_log_error`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** title, message, reference\_doctype, reference\_name, defer\_insert.

**Explicit result forms** a structured result.

**Observed service boundaries** diagnostic or audit logging.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L7038) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1829) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L611)

<a id="op-a668e021149440"></a>
### Safer get visible columns

`operation_foundation_utils_safe_exec_business_behavior_safer_get_visible_columns`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** data, \_table\_meta, df.

**Explicit result forms** a structured result, no value.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L7396) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1828) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L610)

<a id="op-93545ad59034cb"></a>
### Safe get value

`operation_foundation_utils_safe_exec_business_behavior_safe_get_value`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** args, kwargs.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L7658) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1817) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L599)

<a id="op-d8799571b05594"></a>
### Safe get single value

`operation_foundation_utils_safe_exec_business_behavior_safe_get_single_value`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** args, kwargs.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L7751) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1816) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L598)

<a id="op-1d40396c022840"></a>
### Safe render template

`operation_foundation_utils_safe_exec_business_behavior_safe_render_template`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** args, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L7844) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1824) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L606)

<a id="op-f0c190e526cc9e"></a>
### Validate request address

`operation_foundation_utils_safe_exec_business_behavior_validate_request_address`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** ip.

**Locally raised failures** BlockedRequest.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L7948) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1832) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L613)

<a id="op-a9ec2f98cd9fac"></a>
### Validate request url

`operation_foundation_utils_safe_exec_business_behavior_validate_request_resource_address`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** url.

**Locally raised failures** BlockedRequest.

**Local structure** 4 condition or selection sites, 1 statement loops and 2 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1833) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L614)

<a id="op-bdc495e9e3f4a4"></a>
### Get ssrf guarded adapter class

`operation_foundation_utils_safe_exec_business_behavior_get_server_side_request_forgery_guarded_adapter_class`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L526) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1788) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L570)

<a id="op-9d6a8c5323d753"></a>
### Get ssrf guarded adapter class.guarded connection

`operation_foundation_utils_safe_exec_business_behavior_get_server_side_request_forgery_guarded_adapter_class_guarded_connection`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** base.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L1130) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1789) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L571)

<a id="op-70b2f601a5f106"></a>
### Get ssrf guarded adapter class.guarded connection.Guarded Connection.new conn

`operation_foundation_utils_safe_exec_business_behavior_get_server_side_request_forgery_guarded_adapter_class_guarded_connection_guarded_connection_new_conn`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** active or constructed exception.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L1326) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1790) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L572)

<a id="op-8cb7204e81512b"></a>
### Get ssrf guarded adapter class.SSRFGuarded Adapter.init poolmanager

`operation_foundation_utils_safe_exec_business_behavior_get_server_side_request_forgery_guarded_adapter_class_server_side_request_forgery_guarded_adapter_initialize_poolmanager`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, args, kwargs.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L1484) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1791) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L573)

<a id="op-642720996effa1"></a>
### Get ssrf guarded adapter class.SSRFGuarded Adapter.send

`operation_foundation_utils_safe_exec_business_behavior_get_server_side_request_forgery_guarded_adapter_class_server_side_request_forgery_guarded_adapter_send`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, request, kwargs.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** BlockedRequest.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0501.json#L1611) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1792) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L574)
