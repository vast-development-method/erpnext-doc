# Workflow, automation and dispatch · operations 26

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Flow session

<a id="op-5ebb87e2512103"></a>
### Flow Session.system prompt

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_system_prompt`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L118) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1120) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1096)

<a id="op-4aeb5b5114b511"></a>
### Flow Session.sync

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_sync`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, record mutation request, validation or user-notification service.

**Local structure** 6 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L117) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1119) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1095)

<a id="op-831ae193f03a2c"></a>
### Flow Session.lock

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_lock`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L106) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1108) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1084)

<a id="op-bce9e0bb6d6123"></a>
### Flow Session.active run

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_active_run`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L98) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1100) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1076)

<a id="op-249bbbaea17734"></a>
### Flow Session.paused run

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_flowsession_paused_run`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, approval\_seq.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L109) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1111) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1087)

<a id="op-fff8cc82be40f1"></a>
### On share removed

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_on_share_removed`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** share, method.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L124) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1126) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1102)

<a id="op-7f0e7263ed9ded"></a>
### Recheck live access

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_recheck_live_access`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, user.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L127) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1129) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1105)

<a id="op-f6281faa4a5450"></a>
### Publish access notice

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_publish_access_notice`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** notice.

**Explicit result forms** no value.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L125) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1127) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1103)

<a id="op-adbb220787f6ba"></a>
### Delete server session

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_delete_server_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** name.

**Locally raised failures** active or constructed exception.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L96) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1098) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1074)

<a id="op-01fad0f77bf222"></a>
### Delete runs

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_delete_runs`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** sessions.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L95) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1097) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1073)

<a id="op-77f458cda2fa7d"></a>
### Claim attachment file

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_claim_attachment_file`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, file.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L93) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1095) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1071)

<a id="op-04c68e6b854892"></a>
### Delete attachment files

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_delete_attachment_files`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** sessions.

**Observed service boundaries** diagnostic or audit logging, record lookup, record mutation request.

**Local structure** 1 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L94) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1096) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1072)

<a id="op-06712b5e239795"></a>
### Purge attachment chunks

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_purge_attachment_chunks`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session.

**Observed service boundaries** diagnostic or audit logging.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L126) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1128) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1104)

<a id="op-e23c366412ff69"></a>
### Row to message

`operation_foundation_binding_foundation_flow_doctype_flow_session_flow_session_row_to_message`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** row.

**Explicit result forms** a structured result, a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L128) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1130) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1106)

## Record · Flow session attachment

<a id="op-3c53d3b7461d42"></a>
### Build turn

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_build_turn`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, input, files.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** active or constructed exception.

**Observed service boundaries** validation or user-notification service.

**Local structure** 14 condition or selection sites, 2 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L65) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1067) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1043)

<a id="op-948cd72595e6a6"></a>
### Stage attachment

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_stage_attachment`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** file, model.

**Explicit result forms** a structured result.

**Observed service boundaries** record mutation request.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L89) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1091) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1067)

<a id="op-a38c8d56b2f1b2"></a>
### Cleanup indexed files

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_cleanup_indexed_files`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, files.

**Explicit result forms** no value.

**Observed service boundaries** diagnostic or audit logging.

**Local structure** 1 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L67) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1069) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1045)

<a id="op-d6685eaef78c4b"></a>
### Load attachment

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_load_attachment`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** file.

**Explicit result forms** a structured result.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L76) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1078) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1054)

<a id="op-d121eb7c6bbfd8"></a>
### Staged attachment

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_staged_attachment`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** file.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L90) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1092) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1068)

<a id="op-d26e07451511a2"></a>
### Readable file

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_readable_file`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** file.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup, record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L81) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1083) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1059)

<a id="op-7db8f548535522"></a>
### Extract

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_extract`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** file\_doc.

**Explicit result forms** a structured result.

**Observed service boundaries** validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L71) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1073) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1049)

<a id="op-39cd8123341adb"></a>
### Cache key

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_cache_key`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** file.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L66) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1068) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1044)

<a id="op-b05fa1fe7561fa"></a>
### Inline text budget

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_inline_text_budget`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L75) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1077) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1053)

<a id="op-c032c26004f263"></a>
### Model sees images

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_model_sees_images`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** model.

**Explicit result forms** Boolean true, a comparison result.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L77) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1079) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1055)
