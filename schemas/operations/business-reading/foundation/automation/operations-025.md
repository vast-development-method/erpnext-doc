# Workflow, automation and dispatch · operations 25

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Flow run

<a id="op-daac69d8c32e7c"></a>
### Flow Run.mark failed

`operation_foundation_binding_foundation_flow_doctype_flow_run_flow_run_flowrun_mark_failed`

**Inputs** self, error.

**Declared result** no value.

**State and service calls** call save on self.

**Local steps**

- Set self.status from “Failed”.
- Set self.error from str(error) at slice no value to 5000.
- Evaluate self.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L58) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1060) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1036)

<a id="op-382bf950d8f370"></a>
### Json has items

`operation_foundation_binding_foundation_flow_doctype_flow_run_flow_run_json_has_items`

**Inputs** value.

**Declared result** bool.

**Explicit results** false · bool(parsed).

**Local steps**

- If not value.
  - Return false.
- Attempt the following.
  - Set parsed from json.loads(value) when isinstance(value, str), otherwise value.
    - Value choice on isinstance(value, str) — true gives json.loads(value), false gives value.
- On failure (tuple(TypeError, ValueError)).
  - Return false.
- Return bool(parsed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L63) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1065) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1041)

## Record · Flow session

<a id="op-37cbb29c7e5210"></a>
### Flow Session.before insert

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_before_insert`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L100) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1102) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1078)

<a id="op-01700db8a754e5"></a>
### Flow Session.validate

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_validate`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L120) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1122) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1098)

<a id="op-2a840cda4f200d"></a>
### Flow Session.on update

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_on_update`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L108) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1110) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1086)

<a id="op-2ae9e9be032a02"></a>
### Flow Session.on trash

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_on_trash`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L107) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1109) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1085)

<a id="op-99875c563b61fe"></a>
### Flow Session.validate share

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_validate_share`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, docshare.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L123) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1125) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1101)

<a id="op-f980e0518732a0"></a>
### Flow Session.validate model enabled

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_validate_model_enabled`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L122) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1124) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1100)

<a id="op-8c517e3298d89e"></a>
### Flow Session.validate agent unchanged

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_validate_agent_unchanged`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L121) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1123) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1099)

<a id="op-cdc0ab183f4d27"></a>
### Flow Session.clear old logs

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_clear_old_logs`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** days.

**Explicit result forms** no value.

**Observed service boundaries** diagnostic or audit logging, record lookup.

**Local structure** 0 condition or selection sites, 2 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L103) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1105) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1081)

<a id="op-571eb46ac91305"></a>
### Flow Session.transcript

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_transcript`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L119) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1121) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1097)

<a id="op-f487a390d2056d"></a>
### Flow Session.server config

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_server_config`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L113) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1115) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1091)

<a id="op-c9e9d6832332e3"></a>
### Flow Session.chat

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_chat`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, input, attachments, source, trigger, reference\_doctype, reference\_name, on\_complete.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** active or constructed exception.

**Observed service boundaries** record lookup, record mutation request, validation or user-notification service.

**Local structure** 7 condition or selection sites, 1 statement loops and 2 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L102) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1104) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1080)

<a id="op-3f00258017ccb6"></a>
### Flow Session.resume

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_resume`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, answers, approval\_seq.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record mutation request.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L110) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1112) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1088)

<a id="op-be1235788189b4"></a>
### Flow Session.abort

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_abort`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L97) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1099) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1075)

<a id="op-aeed49dd6cabc9"></a>
### Flow Session.cancel pending

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_cancel_pending`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L101) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1103) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1079)

<a id="op-54caef18847a56"></a>
### Flow Session.rewind

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_rewind`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, target\_seq.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L111) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1113) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1089)

<a id="op-cd0d5834ee63a2"></a>
### Flow Session.compact

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_compact`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L104) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1106) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1082)

<a id="op-fbf71b64a74325"></a>
### Flow Session.assert can run

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_assert_can_run`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** effective access lookup, record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L99) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1101) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1077)

<a id="op-b3be0c1b88e366"></a>
### Flow Session.set model

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_set_model`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, model.

**Observed service boundaries** record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L115) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1117) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1093)

<a id="op-b90b67043da6e3"></a>
### Flow Session.send model

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_send_model`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, model.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L112) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1114) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1090)

<a id="op-180bde30d4cd66"></a>
### Flow Session.set title

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_set_title`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, title.

**Observed service boundaries** record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L116) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1118) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1094)

<a id="op-68607590b2ff14"></a>
### Flow Session.set approval mode

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_set_approval_mode`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, mode.

**Observed service boundaries** record mutation request, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L114) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1116) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1092)

<a id="op-c68ee7dc0e8931"></a>
### Flow Session.entries

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_entries`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, since, path.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L105) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1107) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1083)
