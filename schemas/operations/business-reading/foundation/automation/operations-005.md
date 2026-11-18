# Workflow, automation and dispatch · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Assistant

<a id="op-457e8a62759dec"></a>
### Ensure builtin assistant

`operation_foundation_binding_foundation_flow_assistant_assistant_ensure_builtin_assistant`

**Inputs** model.

**Declared result** no value.

**Record and data access** read “Flow Agent” via get\_value · read “Flow Model” via exists.

**Explicit results** no value.

**Local steps**

- Bind dependencies sync\_triggers.
- Set current from Platform.db.get\_value(“Flow Agent”, ASSISTANT\_AGENT\_NAME, “model”).
- If (current and Platform.db.exists(“Flow Model”, current)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in current → Platform.db.exists(“Flow Model”, current).
  - Return no value.
- Evaluate sync\_builtin\_assistant(model = model).
- Evaluate sync\_triggers().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L145) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L894) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L870)

<a id="op-7a51b03a7b0639"></a>
### Sync assistant skills

`operation_foundation_binding_foundation_flow_assistant_assistant_sync_assistant_skills`

**Inputs** \_app.

**Declared result** no value.

**Local steps**

- Evaluate sync\_builtin\_assistant().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L146) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L895) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L871)

<a id="op-3c627a37b1f129"></a>
### Sync builtin assistant

`operation_foundation_binding_foundation_flow_assistant_assistant_sync_builtin_assistant`

**Inputs** model = no value.

**Declared result** no value.

**Record and data access** read “Flow Model” via get\_value · read “Flow Agent” via exists · resolve a document from “Flow Agent” via get\_doc.

**Explicit results** no value.

**Local steps**

- Bind dependencies sync\_skills.
- Bind dependencies Knowledge.
- Bind dependencies Agent.
- Bind dependencies BUILTIN\_TOOLS, sync\_builtin\_tools.
- Evaluate sync\_builtin\_tools().
- Set skills from sync\_skills().
- Set model\_name from (model or Platform.db.get\_value(“Flow Model”, mapping(“enabled” → 1), “name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in model → Platform.db.get\_value(“Flow Model”, mapping(“enabled” → 1), “name”).
- If not model\_name.
  - Return no value.
- Set knowledge from list().
- If Platform.db.exists(“Flow Agent”, ASSISTANT\_AGENT\_NAME).
  - Set doc from Platform.get\_doc(“Flow Agent”, ASSISTANT\_AGENT\_NAME).
  - If not doc.is\_system\_generated.
    - Return no value.
  - Update skills using + list of row.skill for row drawn from doc.skills where row.skill does not belong to skills.
    - Draw row from doc.skills, keep a combination only if (row.skill does not belong to skills).
  - Set knowledge from list of Knowledge(row.knowledge\_base) for row drawn from doc.knowledge\_bases.
    - Draw row from doc.knowledge\_bases.
- Evaluate Agent(name = ASSISTANT\_AGENT\_TITLE, model = model\_name, instructions = ASSISTANT\_INSTRUCTIONS, tools = BUILTIN\_TOOLS, …).sync().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L147) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L896) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L872)

## Service · Attachment store

<a id="op-8ad86b853c3a84"></a>
### Ensure table

`operation_foundation_binding_foundation_flow_knowledge_attachment_store_ensure_table`

**Inputs** dimension.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** ValueError(formatted text Invalid embedding dimension: {dimension}).

**Local steps**

- If (not isinstance(dimension, int) or dimension &lt; 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(dimension, int) → dimension &lt; 1.
  - Raise ValueError(formatted text Invalid embedding dimension: {dimension}).
- Within \_connect(write = true) bound as db.
  - If \_shape(db, TABLE\_NAME) equals str(dimension).
    - Return no value.
  - Evaluate \_drop\_table(db, TABLE\_NAME).
  - Evaluate \_create\_table(db, TABLE\_NAME, “id integer primary key, session text, attachment text”, dimension).
  - Evaluate db.execute(formatted text create index {TABLE\_NAME}\_session on {TABLE\_NAME}(session)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L170) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1172) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1148)

<a id="op-3ee7a1d87b2448"></a>
### Add

`operation_foundation_binding_foundation_flow_knowledge_attachment_store_add`

**Inputs** session, attachment, chunks, vectors.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** ValueError(formatted text chunks/vectors length mismatch: {len(chunks)} != {len(vectors)}).

**Local steps**

- If len(chunks) differs from len(vectors).
  - Raise ValueError(formatted text chunks/vectors length mismatch: {len(chunks)} != {len(vectors)}).
- If not chunks.
  - Return no value.
- Within \_connect(write = true) bound as db.
  - Evaluate db.executemany(formatted text insert into {TABLE\_NAME}(session, attachment, content, vector) values (?, ?, ?, ?), list of tuple(session, attachment, content, \_vector\_bytes(vector)) for tuple(content, vecto ….
    - Draw tuple(content, vector) from zip(chunks, vectors, strict = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L167) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1169) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1145)

<a id="op-c51835f44ebe39"></a>
### Search

`operation_foundation_binding_foundation_flow_knowledge_attachment_store_search`

**Inputs** vector, session (named only), text (named only, default no value), limit (named only, default 8).

**Declared result** list at dict at tuple(str, Any).

**Explicit results** list() · list of mapping(“attachment” → attachment, “content” → content, “score” → score) for tuple(attachment, content, score) drawn from hits.

**Explicit failure paths** ValueError(“search requires a session scope”).

**Local steps**

- If not session.
  - Raise ValueError(“search requires a session scope”).
- Set limit from max(1, min(int(limit), MAX\_SEARCH\_LIMIT)).
- Within \_connect() bound as db.
  - If \_shape(db, TABLE\_NAME) is identical to no value.
    - Return list().
  - Set hits from \_search(db, TABLE\_NAME, “attachment, content”, “session = ?”, …).
- Return list of mapping(“attachment” → attachment, “content” → content, “score” → score) for tuple(attachment, content, score) drawn from hits.
  - Draw tuple(attachment, content, score) from hits.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L171) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1173) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1149)

<a id="op-423d3170af0c45"></a>
### Delete

`operation_foundation_binding_foundation_flow_knowledge_attachment_store_delete`

**Inputs** session (named only, default no value), attachment (named only, default no value).

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** ValueError(“delete() requires session and/or attachment”).

**Local steps**

- If (session is identical to no value and attachment is identical to no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in session is identical to no value → attachment is identical to no value.
  - Raise ValueError(“delete() requires session and/or attachment”).
- If (isinstance(session, list) and not session).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(session, list) → not session.
  - Return no value.
- Set tuple(conditions, values) from tuple(list(), list()).
- If session is distinct from no value.
  - Set sessions from list(session) when isinstance(session, str), otherwise session.
    - Value choice on isinstance(session, str) — true gives list(session), false gives session.
  - Evaluate conditions.append(formatted text session in ({\_placeholders(sessions)})).
  - Evaluate values.extend(sessions).
- If attachment is distinct from no value.
  - Evaluate conditions.append(“attachment = ?”).
  - Evaluate values.append(attachment).
- Within \_connect(write = true) bound as db.
  - If \_shape(db, TABLE\_NAME) is distinct from no value.
    - Evaluate db.execute(formatted text delete from {TABLE\_NAME} where {“ and ”.join(conditions)}, values).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L168) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1170) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1146)

<a id="op-b1d3a01af4254c"></a>
### Drop table

`operation_foundation_binding_foundation_flow_knowledge_attachment_store_drop_table`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Within \_connect(write = true) bound as db.
  - Evaluate \_drop\_table(db, TABLE\_NAME).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L169) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1171) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1147)

<a id="op-5838595883726b"></a>
### Table exists

`operation_foundation_binding_foundation_flow_knowledge_attachment_store_table_exists`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** \_shape(db, TABLE\_NAME) is distinct from no value.

**Local steps**

- Within \_connect() bound as db.
  - Return \_shape(db, TABLE\_NAME) is distinct from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L172) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1174) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1150)

## Service · Auth

<a id="op-bc7d7aecabe9eb"></a>
### Credentials.headers

`operation_foundation_realtime_auth_business_behavior_credentials_headers`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a structured result.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L305) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1528) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L214)

<a id="op-101daab8619d68"></a>
### Session.get

`operation_foundation_realtime_auth_business_behavior_session_get`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, path, params.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L449) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1544) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L230)

<a id="op-1fb946025e1516"></a>
### Session.post

`operation_foundation_realtime_auth_business_behavior_session_post`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, path, body, params.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L560) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1546) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L232)

<a id="op-81d306891296ea"></a>
### Session.put

`operation_foundation_realtime_auth_business_behavior_session_put`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, path, body, params.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L704) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1547) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L233)

<a id="op-9e5a116ed2d0be"></a>
### Session.delete

`operation_foundation_realtime_auth_business_behavior_session_delete`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, path, params.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L848) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1543) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L229)

<a id="op-6b68bd1db70ba5"></a>
### Session.send request

`operation_foundation_realtime_auth_business_behavior_session_send_request`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, path, method, params, body.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L959) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1548) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L234)

<a id="op-5acc36b8a37455"></a>
### Session.has permission

`operation_foundation_realtime_auth_business_behavior_session_has_permission`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, doctype, name, ptype.

**Explicit result forms** Boolean false, the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L1120) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1545) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L231)

<a id="op-21e0143f038f95"></a>
### Authenticate

`operation_foundation_realtime_auth_business_behavior_authenticate`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** environ, namespace, config.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L1381) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1525) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L211)

<a id="op-f4fbb46e018a76"></a>
### Reject

`operation_foundation_realtime_auth_business_behavior_reject`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** reason, message.

**Locally raised failures** ConnectionRefusedError.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L1662) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1542) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L228)

<a id="op-45ea01ec4e1220"></a>
### Validate site

`operation_foundation_realtime_auth_business_behavior_validate_site`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** environ, namespace, config.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L1763) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1550) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L236)

<a id="op-195a1144215271"></a>
### Validate origin

`operation_foundation_realtime_auth_business_behavior_validate_origin`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** environ.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L1972) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1549) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L235)

<a id="op-845af08c0d36c2"></a>
### Read credentials

`operation_foundation_realtime_auth_business_behavior_read_credentials`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** environ.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L2222) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1540) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L226)

<a id="op-39699bb99c05a0"></a>
### Read sid

`operation_foundation_realtime_auth_business_behavior_read_session_identifier`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** cookie\_header.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L2495) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1541) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L227)

<a id="op-b9810d4de28f25"></a>
### Make request

`operation_foundation_realtime_auth_business_behavior_make_request`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** environ, credentials, config, site, secret.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L108) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1537) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L223)

<a id="op-79618383edeee5"></a>
### Make request.request

`operation_foundation_realtime_auth_business_behavior_make_request_request`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** path, method, params, body.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L109) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1538) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L224)
