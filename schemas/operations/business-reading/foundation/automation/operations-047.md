# Workflow, automation and dispatch · operations 47

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Session

<a id="op-5804ee8ecfffd3"></a>
### Log Recorder.add user message

`operation_foundation_binding_foundation_flow_lib_session_logrecorder_add_user_message`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, text, seq.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L69) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1310) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1286)

<a id="op-fb1b698d162b3c"></a>
### Log Recorder.add assistant message

`operation_foundation_binding_foundation_flow_lib_session_logrecorder_add_assistant_message`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, text, calls, seq.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L67) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1308) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1284)

<a id="op-6ca03f78dea634"></a>
### Log Recorder.rewind

`operation_foundation_binding_foundation_flow_lib_session_logrecorder_rewind`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, target\_seq.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L74) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1315) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1291)

<a id="op-f0d95212d44ce1"></a>
### Log Recorder.end run

`operation_foundation_binding_foundation_flow_lib_session_logrecorder_end_run`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, reason.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L70) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1311) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1287)

<a id="op-70b61a07615e73"></a>
### Log Recorder.add message

`operation_foundation_binding_foundation_flow_lib_session_logrecorder_add_message`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, role, content, fields.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L68) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1309) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1285)

<a id="op-ee83f95214dae9"></a>
### Fail running

`operation_foundation_binding_foundation_flow_lib_session_fail_running`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session\_name, error.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L62) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1303) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1279)

<a id="op-7b7ae220e4efa7"></a>
### Sync with retry

`operation_foundation_binding_foundation_flow_lib_session_sync_with_retry`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session.

**Observed service boundaries** transaction control.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L77) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1318) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1294)

<a id="op-3e3300741bd0e8"></a>
### Call on complete

`operation_foundation_binding_foundation_flow_lib_session_call_on_complete`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session.

**Explicit result forms** no value.

**Observed service boundaries** diagnostic or audit logging, record lookup, record mutation request, transaction control.

**Local structure** 2 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L58) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1299) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1275)

<a id="op-d6f6c5ccb47e16"></a>
### Latest run

`operation_foundation_binding_foundation_flow_lib_session_latest_run`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session\_name.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L64) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1305) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1281)

<a id="op-c7af2297bbf329"></a>
### Extract text

`operation_foundation_binding_foundation_flow_lib_session_extract_text`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** content.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L61) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1302) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1278)

<a id="op-ba6ed800f12e77"></a>
### Assistant text and tool calls

`operation_foundation_binding_foundation_flow_lib_session_assistant_text_and_tool_calls`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** content.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L56) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1297) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1273)

<a id="op-0b8cfe6f40dc40"></a>
### To openai tool calls

`operation_foundation_binding_foundation_flow_lib_session_to_openai_tool_calls`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** calls.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L78) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1319) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1295)

<a id="op-13ec1174b77738"></a>
### Add usage

`operation_foundation_binding_foundation_flow_lib_session_add_usage`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** total, row.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L55) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1296) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1272)

<a id="op-c06b769298958a"></a>
### Load

`operation_foundation_binding_foundation_flow_lib_session_load`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** value.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L65) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1306) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1282)

<a id="op-48da2cf32e5777"></a>
### Dump

`operation_foundation_binding_foundation_flow_lib_session_dump`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** value.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L60) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1301) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1277)

<a id="op-a6e3fbd351599b"></a>
### Default agent name

`operation_foundation_binding_foundation_flow_lib_session_default_agent_name`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L59) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1300) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1276)

## Service · Settings

<a id="op-a696bd555ab10b"></a>
### Settings

`operation_foundation_binding_foundation_automation_engine_settings_settings`

**Inputs** no declared parameters.

**Record and data access** resolve a document from SETTINGS via get\_cached\_doc.

**Explicit results** Platform.get\_cached\_doc(SETTINGS) · DEFAULTS.

**Local steps**

- Attempt the following.
  - Return Platform.get\_cached\_doc(SETTINGS).
- On failure (tuple(Platform.DoesNotExistError, Platform.db.TableMissingError, ImportError)).
  - Return DEFAULTS.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(SETTINGS).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L99) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L581) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L557)

<a id="op-0a7ef10081ae54"></a>
### Get

`operation_foundation_binding_foundation_automation_engine_settings_get`

**Inputs** fieldname.

**Explicit results** DEFAULTS at fieldname · value.

**Local steps**

- Set value from settings().get(fieldname).
- If (value belongs to tuple(no value, empty text) or (not value and fieldname does not belong to ZERO\_IS\_MEANINGFUL)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in value belongs to tuple(no value, empty text) → (not value and fieldname does not belong to ZERO\_IS\_MEANINGFUL).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not value → fieldname does not belong to ZERO\_IS\_MEANINGFUL.
  - Return DEFAULTS at fieldname.
- Return value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L97) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L579) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L555)

<a id="op-03c3232c780f9b"></a>
### Is enabled

`operation_foundation_binding_foundation_automation_engine_settings_is_enabled`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** false · not get(“disable\_automations”).

**Local steps**

- If Platform.flags.get(“skip\_automations”).
  - Return false.
- If Platform.conf.get(“automation\_disabled”).
  - Return false.
- Return not get(“disable\_automations”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L98) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L580) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L556)

<a id="op-c09b03723a6073"></a>
### Skip automations

`operation_foundation_binding_foundation_automation_engine_settings_skip_automations`

**Inputs** no declared parameters.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Set previous from Platform.flags.get(“skip\_automations”).
- Set Platform.flags.skip\_automations from true.
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Set Platform.flags.skip\_automations from previous.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L100) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L582) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L558)

## Service · Socket

<a id="op-43d0298751a04b"></a>
### Socket.initialize

`operation_foundation_realtime_socket_business_behavior_realtime_transport_initialize`

**Inputs** self, sio, sid, namespace, session.

**Local steps**

- Set self.\_sio from sio.
- Set self.sid from sid.
- Set self.namespace from namespace.
- Set self.\_session from session.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L439) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1632) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L318)

<a id="op-00ea559942f7ff"></a>
### Socket.site

`operation_foundation_realtime_socket_business_behavior_realtime_transport_site`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** self.\_session.site.

**Local steps**

- Return self.\_session.site.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L585) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1638) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L324)

<a id="op-aa57e066efa1ea"></a>
### Socket.user

`operation_foundation_realtime_socket_business_behavior_realtime_transport_user`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** self.\_session.user.

**Local steps**

- Return self.\_session.user.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L637) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1639) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L325)

<a id="op-d540c36c5d6f0a"></a>
### Socket.user type

`operation_foundation_realtime_socket_business_behavior_realtime_transport_user_type`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** (self.\_session.user\_type or empty text).

**Local steps**

- Return (self.\_session.user\_type or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_session.user\_type → empty text.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L689) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1641) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L327)
