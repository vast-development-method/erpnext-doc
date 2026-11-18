# Workflow, automation and dispatch · operations 27

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Flow session attachment

<a id="op-ce795d1edfc78a"></a>
### Session model

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_session_model`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L87) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1089) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1065)

<a id="op-4d34c482c51417"></a>
### Pasted files

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_pasted_files`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** text\_files, budget, skip, tables.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L78) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1080) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1056)

<a id="op-db3f60cd5a8d19"></a>
### Retrieval files

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_retrieval_files`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** text\_files, budget.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L83) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1085) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1061)

<a id="op-b4f11f05848dde"></a>
### Index

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_index`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, file, text.

**Observed service boundaries** diagnostic or audit logging, validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L74) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1076) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1052)

<a id="op-f5d2a74fbb9ac5"></a>
### File block

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_file_block`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** file\_doc, body.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L72) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1074) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1050)

<a id="op-4dc507dbaad731"></a>
### Preview

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_preview`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** file\_doc, text, readable.

**Explicit result forms** a value selected from the current context.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L79) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1081) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1057)

<a id="op-337c8987ed9344"></a>
### Table rows

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_table_rows`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** file\_doc.

**Explicit result forms** a structured result, no value.

**Local structure** 3 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L91) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1093) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1069)

<a id="op-6c05dc428f1f2e"></a>
### Csv lines

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_csv_lines`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** rows.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L68) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1070) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1046)

<a id="op-1285469cbb9ec1"></a>
### Extension

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_extension`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** file\_doc.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L70) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1072) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1048)

<a id="op-d85a7af2cd6efe"></a>
### Size text

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_size_text`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** size.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L88) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1090) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1066)

<a id="op-a8191e3100bf93"></a>
### Read attachment

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_read_attachment`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, file, offset, limit.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 8 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L80) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1082) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1058)

<a id="op-874bf93088dd75"></a>
### Session file named

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_session_file_named`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, held, file\_name.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L85) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1087) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1063)

<a id="op-18a3c68891192a"></a>
### Session files

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_session_files`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, held.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L86) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1088) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1064)

<a id="op-53c7ca1fbb4f38"></a>
### Hold sent files

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_hold_sent_files`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, files.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L73) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1075) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1051)

<a id="op-40c7aefe3c033f"></a>
### Release sent files

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_release_sent_files`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L82) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1084) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1060)

<a id="op-99d2189f4926cd"></a>
### Sending key

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_sending_key`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L84) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1086) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1062)

<a id="op-2efd86fb4cf183"></a>
### Attachment text

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_attachment_text`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, file\_doc.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L64) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1066) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1042)

<a id="op-4ca5ef96001884"></a>
### Excerpts

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_excerpts`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** query, session.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Observed service boundaries** diagnostic or audit logging, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L69) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1071) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1047)

<a id="op-3bbb5ebaf1f01b"></a>
### Xml attr

`operation_foundation_binding_foundation_flow_doctype_flow_session_attachment_flow_session_attachment_xml_attr`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** value.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L92) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1094) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1070)

## Record · Flow settings

<a id="op-287351dc0e4119"></a>
### Flow Settings.validate

`operation_foundation_binding_foundation_flow_doctype_flow_settings_flow_settings_flowsettings_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} needs a Search API Key.”.format(self.search\_provider).

**Local steps**

- If ((self.search\_provider or “DuckDuckGo”) differs from “DuckDuckGo” and not self.search\_api\_key).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.search\_provider or “DuckDuckGo”) differs from “DuckDuckGo” → not self.search\_api\_key.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.search\_provider → “DuckDuckGo”.
  - Call the validation error handler Platform.throw(translated “{0} needs a Search API Key.”.format(self.search\_provider), title = translated “Missing API Key”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L129) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1131) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1107)

## Record · Flow skill

<a id="op-11b2a7f50b5b49"></a>
### Flow Skill.before insert

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_flowskill_before_insert`

**Inputs** self.

**Local steps**

- Evaluate block\_insert(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L132) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1134) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1110)

<a id="op-c36fa857cce3ca"></a>
### Flow Skill.validate

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_flowskill_validate`

**Inputs** self.

**Local steps**

- Evaluate block\_slash\_in\_name(self).
- Evaluate self.\_validate\_description().
- Evaluate self.\_validate\_global\_limit().
- Evaluate self.\_validate\_command().
- Evaluate validate\_immutable(self, tuple(“description”, “instructions”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate description](operations-028.md#op-fe13d455162cb9), [validate global limit](operations-028.md#op-a1cdb9bab17abc), [validate command](operations-028.md#op-020ec0e7abf5bb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L135) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1137) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1113)

<a id="op-968af1fe392db3"></a>
### Flow Skill.on trash

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_flowskill_on_trash`

**Inputs** self.

**Local steps**

- Evaluate block\_delete(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L134) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1136) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1112)

<a id="op-82efa26e102223"></a>
### Flow Skill.before rename

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_flowskill_before_rename`

**Inputs** self, old, new, merge = false.

**Declared result** no value.

**Local steps**

- Evaluate block\_rename(self, old).
- Evaluate block\_slash\_in\_name(self, new).
- If not merge.
  - Evaluate self.\_validate\_command(new).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate command](operations-028.md#op-020ec0e7abf5bb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L133) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1135) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1111)
