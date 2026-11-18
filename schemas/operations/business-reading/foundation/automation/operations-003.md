# Workflow, automation and dispatch · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Api

<a id="op-db2b4f31300257"></a>
### Set model

`operation_foundation_binding_foundation_flow_api_api_set_model`

**Inputs** session, model.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, str).

**Explicit results** mapping(“model” → model.strip()).

**Explicit failure paths** validation helper — translated “Model is required.”.

**Local steps**

- If (not isinstance(model, str) or not model.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(model, str) → not model.strip().
  - Call the validation error handler Platform.throw(translated “Model is required.”, title = translated “Invalid Model”).
- Evaluate \_load\_session(session, “write”).set\_model(model.strip()).
- Return mapping(“model” → model.strip()).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L133) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L882) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L858)

<a id="op-23362d88398500"></a>
### Set title

`operation_foundation_binding_foundation_flow_api_api_set_title`

**Inputs** session, title.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, str).

**Explicit results** mapping(“title” → title).

**Explicit failure paths** validation helper — translated “Title is required.”.

**Local steps**

- Set title from (title or empty text).strip() at slice no value to TITLE\_LIMIT.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → empty text.
- If not title.
  - Call the validation error handler Platform.throw(translated “Title is required.”, title = translated “Invalid Title”).
- Evaluate \_load\_session(session, “write”).set\_title(title).
- Return mapping(“title” → title).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L135) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L884) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L860)

<a id="op-f2ca9519fcd0a0"></a>
### Set approval mode

`operation_foundation_binding_foundation_flow_api_api_set_approval_mode`

**Inputs** session, mode.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, str).

**Explicit results** mapping(“approval\_mode” → mode).

**Local steps**

- Evaluate \_load\_session(session, “write”).set\_approval\_mode(mode).
- Return mapping(“approval\_mode” → mode).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L131) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L880) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L856)

<a id="op-973712a6b9c8c0"></a>
### Set prefs

`operation_foundation_binding_foundation_flow_api_api_set_prefs`

**Inputs** prefs.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, Any).

**Explicit results** saved.

**Explicit failure paths** validation helper — translated “Invalid preference: {0}”.format(key).

**Local steps**

- Evaluate Platform.has\_permission(“Flow Session”, “read”, throw = true).
- For each tuple(key, value) in prefs.items().
  - Set allowed from USER\_PREFS.get(key).
  - If (not allowed or (value is distinct from no value and not any(generator of (nested operand in the contract equals nested operand in the contract and nested operand in the contract is identical to nested ope ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not allowed → (value is distinct from no value and not any(generator of (value equals a and nested operand in the contract(nested operand in the contract) is identical to nested operand in the contract(nested operand in ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value is distinct from no value → not any(generator of (value equals a and type(value) is identical to type(a)) for a drawn from allowed).
    - Draw a from allowed.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value equals a → type(value) is identical to type(a).
    - Call the validation error handler Platform.throw(translated “Invalid preference: {0}”.format(key), title = translated “Invalid Preference”).
- Set saved from mapping(expand \_user\_prefs(), expand prefs).
- Evaluate Platform.defaults.set\_user\_default(USER\_PREFS\_KEY, json.dumps(saved)).
- Return saved.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Flow Session”, “read”, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L134) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L883) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L859)

<a id="op-7180b6a9df9135"></a>
### User prefs

`operation_foundation_binding_foundation_flow_api_api_user_prefs`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping of key → value for tuple(key, value) drawn from saved.items() where key belongs to USER\_PREFS.

**Local steps**

- Set saved from Platform.parse\_json((Platform.defaults.get\_user\_default(USER\_PREFS\_KEY) or “{}”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.defaults.get\_user\_default(USER\_PREFS\_KEY) → “{}”.
- Return mapping of key → value for tuple(key, value) drawn from saved.items() where key belongs to USER\_PREFS.
  - Draw tuple(key, value) from saved.items(), keep a combination only if (key belongs to USER\_PREFS).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L143) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L892) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L868)

<a id="op-6ad27c694613a2"></a>
### Delete session

`operation_foundation_binding_foundation_flow_api_api_delete_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L113) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L862) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L838)

<a id="op-6d4255b199b3bd"></a>
### List shares

`operation_foundation_binding_foundation_flow_api_api_list_shares`

**Inputs** session.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict at tuple(str, Any).

**Explicit results** \_shares(\_load\_session(session, “share”)).

**Local steps**

- Return \_shares(\_load\_session(session, “share”)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L118) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L867) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L843)

<a id="op-d363bc76e82d0f"></a>
### Share session

`operation_foundation_binding_foundation_flow_api_api_share_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, user.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L136) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L885) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L861)

<a id="op-6ecb380e35fe00"></a>
### Unshare session

`operation_foundation_binding_foundation_flow_api_api_unshare_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L142) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L891) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L867)

<a id="op-5e186abd751462"></a>
### Set general access

`operation_foundation_binding_foundation_flow_api_api_set_general_access`

**Inputs** session, access.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** str.

**State and service calls** call db\_set on doc.

**Explicit results** access.

**Explicit failure paths** validation helper — translated “General access must be "Restricted" (only the people added) or "Everyone" (every Flow user).”.

**Local steps**

- Bind dependencies recheck\_live\_access.
- Set doc from \_load\_session(session, “share”).
- If access does not belong to nested operand in the contract.get\_meta(“Flow Session”).get\_options(“general\_access”).split(whitespace '\\n').
  - Call the validation error handler Platform.throw(translated “General access must be "Restricted" (only the people added) or "Everyone" (every Flow user).”, title = translated “Invalid Access”).
- If doc.general\_access differs from access.
  - Evaluate doc.db\_set(“general\_access”, access).
  - If access equals “Restricted”.
    - Evaluate recheck\_live\_access(doc.name).
- Return access.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L132) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L881) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L857)

<a id="op-b1aacb9dc76aba"></a>
### Find users

`operation_foundation_binding_foundation_flow_api_api_find_users`

**Inputs** query = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict at tuple(str, Any).

**Explicit results** \_flow\_users(text = query.strip() when isinstance(query, str), otherwise empty text).

**Local steps**

- Evaluate Platform.has\_permission(“Flow Session”, “create”, throw = true).
- Return \_flow\_users(text = query.strip() when isinstance(query, str), otherwise empty text).
  - Value choice on isinstance(query, str) — true gives query.strip(), false gives empty text.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Flow Session”, “create”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L115) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L864) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L840)

<a id="op-e80afaab848d87"></a>
### Sync session

`operation_foundation_binding_foundation_flow_api_api_sync_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L140) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L889) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L865)

<a id="op-41a6822b598894"></a>
### Submit feedback

`operation_foundation_binding_foundation_flow_api_api_submit_feedback`

**Inputs** run\_name, rating, comment = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, Any).

**Record and data access** resolve a document from “Flow Run” via get\_doc.

**State and service calls** call db\_set on run · savepoint “flow\_feedback\_memory” · rollback.

**Explicit results** mapping(“rating” → no value, “forgotten” → forgotten) when forgotten, otherwise mapping(“rating” → no value) · result.

**Explicit failure paths** validation helper — translated “Run is required.” · validation helper — translated “Rating must be Up, Down, or None.” · validation helper — translated “Keep feedback under {0} characters.”.format(FEEDBACK\_COMMENT\_LIMIT) · validation helper — translated “Feedback applies to finished runs only (this run is {0}).”.format(run.status).

**Local steps**

- Bind dependencies forget\_feedback\_memory, save\_feedback\_memory.
- If (not isinstance(run\_name, str) or not run\_name.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(run\_name, str) → not run\_name.strip().
  - Call the validation error handler Platform.throw(translated “Run is required.”, title = translated “Invalid Run”).
- If rating does not belong to tuple(“Up”, “Down”, “None”).
  - Call the validation error handler Platform.throw(translated “Rating must be Up, Down, or None.”, title = translated “Invalid Rating”).
- Set comment from (comment or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in comment → empty text.
- If len(comment) &gt; FEEDBACK\_COMMENT\_LIMIT.
  - Call the validation error handler Platform.throw(translated “Keep feedback under {0} characters.”.format(FEEDBACK\_COMMENT\_LIMIT), title = translated “Feedback Too Long”).
- Set run from Platform.get\_doc(“Flow Run”, run\_name.strip()).
- Evaluate Platform.has\_permission(“Flow Run”, “read”, run, throw = true).
- Evaluate Platform.has\_permission(“Flow Session”, “write”, run.session, throw = true).
- If run.status does not belong to tuple(“Completed”, “Denied”, “Failed”).
  - Call the validation error handler Platform.throw(translated “Feedback applies to finished runs only (this run is {0}).”.format(run.status), title = translated “Run Not Finished”).
- If rating equals “None”.
  - Set forgotten from forget\_feedback\_memory(run).
  - Evaluate run.db\_set(mapping(“feedback\_rating” → empty text, “feedback\_comment” → no value)).
  - Return mapping(“rating” → no value, “forgotten” → forgotten) when forgotten, otherwise mapping(“rating” → no value).
    - Value choice on forgotten — true gives mapping(“rating” → no value, “forgotten” → forgotten), false gives mapping(“rating” → no value).
- Evaluate run.db\_set(mapping(“feedback\_rating” → rating, “feedback\_comment” → (comment or no value))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in comment → no value.
- Set memory from no value.
- If (rating equals “Down” and comment).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rating equals “Down” → comment.
  - Evaluate Platform.db.savepoint(“flow\_feedback\_memory”).
  - Attempt the following.
    - Set memory from save\_feedback\_memory(run, comment).
  - On failure (Exception).
    - Evaluate Platform.db.rollback(save\_point = “flow\_feedback\_memory”).
    - Evaluate Platform.log\_error(title = “Flow feedback memory failed”, reference\_doctype = “Flow Run”, reference\_name = run.name).
- Set result from mapping(“rating” → rating).
- If memory.
  - Evaluate result.update(memory = memory at “memory\_id”, memory\_scope = memory at “scope”).
- Return result.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Flow Run”, “read”, run, throw = true), Platform.has\_permission(“Flow Session”, “write”, run.session, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L139) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L888) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L864)

<a id="op-7d44f9dead1edd"></a>
### Attach file

`operation_foundation_binding_foundation_flow_api_api_attach_file`

**Inputs** file, model = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, Any).

**Explicit results** stage\_attachment(file.strip(), model).

**Explicit failure paths** validation helper — translated “File is required.”.

**Local steps**

- If (not isinstance(file, str) or not file.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(file, str) → not file.strip().
  - Call the validation error handler Platform.throw(translated “File is required.”, title = translated “Invalid Attachment”).
- Evaluate Platform.has\_permission(“Flow Session”, “create”, throw = true).
- Bind dependencies stage\_attachment.
- Return stage\_attachment(file.strip(), model).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Flow Session”, “create”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L106) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L855) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L831)

<a id="op-bc2338ccfecc3e"></a>
### Cleanup attachments

`operation_foundation_binding_foundation_flow_api_api_cleanup_attachments`

**Inputs** session = no value, attachments = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, list at str).

**Record and data access** read “File” via get\_value · read “Flow Session Attachment” via exists.

**State and service calls** request delete\_doc for “File”.

**Explicit results** mapping(“removed” → removed).

**Local steps**

- If session.
  - Evaluate \_load\_session(session, “write”).
- Otherwise.
  - Evaluate Platform.has\_permission(“Flow Session”, “create”, throw = true).
- Set removed from list().
- For each file in \_parse\_attachments(attachments).
  - Set row from Platform.db.get\_value(“File”, file, list(“owner”, “attached\_to\_doctype”), as\_dict = true).
  - If (not row or row.owner differs from Platform.session.user or row.attached\_to\_doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row → row.owner differs from Platform.session.user → row.attached\_to\_doctype.
    - Continue with the next iteration or loop test.
  - If Platform.db.exists(“Flow Session Attachment”, mapping(“file” → file)).
    - Continue with the next iteration or loop test.
  - Evaluate Platform.delete\_doc(“File”, file, ignore\_permissions = true).
  - Evaluate removed.append(file).
- Return mapping(“removed” → removed).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Flow Session”, “create”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L109) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L858) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L834)

<a id="op-31e056453fceb6"></a>
### Load session

`operation_foundation_binding_foundation_flow_api_api_load_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, ptype.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup, record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L119) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L868) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L844)

<a id="op-eaf8fce465cc57"></a>
### Session payload

`operation_foundation_binding_foundation_flow_api_api_session_payload`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doc.

**Explicit result forms** a structured result.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L130) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L879) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L855)

<a id="op-adb2420664e7b0"></a>
### Shares

`operation_foundation_binding_foundation_flow_api_api_shares`

**Inputs** doc.

**Declared result** list at dict at tuple(str, Any).

**Record and data access** read “DocShare” via get\_all · read “User” via get\_all.

**Explicit results** list() · Platform.get\_all(“User”, filters = mapping(“name” → tuple(“in”, users)), fields = list(“name”, “full\_name”, “user\_image”), order\_by = “full\_name asc”).

**Local steps**

- Set users from Platform.get\_all(“DocShare”, filters = mapping(“share\_doctype” → “Flow Session”, “share\_name” → doc.name, “everyone” → 0), pluck = “user”).
- If not users.
  - Return list().
- Return Platform.get\_all(“User”, filters = mapping(“name” → tuple(“in”, users)), fields = list(“name”, “full\_name”, “user\_image”), order\_by = “full\_name asc”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L137) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L886) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L862)

<a id="op-0562336a196251"></a>
### Flow users

`operation_foundation_binding_foundation_flow_api_api_flow_users`

**Inputs** text = empty text, user = no value.

**Declared result** list at dict at tuple(str, Any).

**Record and data access** read “User” via get\_all.

**Explicit results** Platform.get\_all(“User”, filters = filters, fields = list(“name”, “full\_name”, “user\_image”), distinct = true, order\_by = “full\_name asc”, …).

**Local steps**

- Set roles from list of p.role for p drawn from Platform.get\_meta(“Flow Session”).permissions where (p.create and not p.permlevel).
  - Draw p from Platform.get\_meta(“Flow Session”).permissions, keep a combination only if ((p.create and not p.permlevel)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in p.create → not p.permlevel.
- Set filters from list(list(“enabled”, “=”, 1), list(“user\_type”, “=”, “System User”), list(“Has Role”, “role”, “in”, roles)).
- If user.
  - Evaluate filters.append(list(“name”, “=”, user)).
- If text.
  - Set person from Platform.qb.DocType(“User”).
  - Evaluate filters.append((\_contains(person.name, text) bitwise or \_contains(person.full\_name, text))).
- Return Platform.get\_all(“User”, filters = filters, fields = list(“name”, “full\_name”, “user\_image”), distinct = true, order\_by = “full\_name asc”, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L116) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L865) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L841)

<a id="op-220888c917b3b4"></a>
### Notify share

`operation_foundation_binding_foundation_flow_api_api_notify_share`

**Inputs** doc, user.

**Declared result** no value.

**Record and data access** read “User” via get\_value.

**Local steps**

- Bind dependencies enqueue\_create\_notification.
- Evaluate enqueue\_create\_notification(Platform.db.get\_value(“User”, user, “email”), mapping(“type” → “Share”, “document\_type” → “Flow Session”, “document\_name” → doc.name, “subject” → translated “{0} shared the chat ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.title → translated “Untitled chat”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L120) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L869) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L845)

<a id="op-35bc6c63fbfe31"></a>
### Parse user

`operation_foundation_binding_foundation_flow_api_api_parse_user`

**Inputs** user.

**Declared result** str.

**Explicit results** user.strip().

**Explicit failure paths** validation helper — translated “User is required.”.

**Local steps**

- If (not isinstance(user, str) or not user.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(user, str) → not user.strip().
  - Call the validation error handler Platform.throw(translated “User is required.”, title = translated “Invalid User”).
- Return user.strip().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L123) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L872) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L848)

<a id="op-182989344e038b"></a>
### Contains

`operation_foundation_binding_foundation_flow_api_api_contains`

**Inputs** field, text.

**Declared result** Criterion.

**Explicit results** Locate(Lower(text), Lower(field)) &gt; 0.

**Local steps**

- Return Locate(Lower(text), Lower(field)) &gt; 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L111) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L860) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L836)

<a id="op-67b875d572fe85"></a>
### Parse attachments

`operation_foundation_binding_foundation_flow_api_api_parse_attachments`

**Inputs** attachments.

**Declared result** list at str.

**Explicit results** list() · list of f.strip() for f drawn from attachments.

**Explicit failure paths** validation helper — translated “Attachments must be a list of File names.”.

**Local steps**

- If attachments belongs to tuple(no value, empty text).
  - Return list().
- If isinstance(attachments, str).
  - Attempt the following.
    - Set attachments from json.loads(attachments).
  - On failure (ValueError).
    - Set attachments from no value.
- If (not isinstance(attachments, list) or not all(generator of (isinstance(f, str) and nested operand in the contract.strip()) for f drawn from attachments)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(attachments, list) → not all(generator of (isinstance(f, str) and f.strip()) for f drawn from attachments).
  - Draw f from attachments.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(f, str) → f.strip().
  - Call the validation error handler Platform.throw(translated “Attachments must be a list of File names.”, title = translated “Invalid Attachments”).
- Return list of f.strip() for f drawn from attachments.
  - Draw f from attachments.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L122) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L871) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L847)

<a id="op-b539e0345bab4f"></a>
### Parse answers

`operation_foundation_binding_foundation_flow_api_api_parse_answers`

**Inputs** answers.

**Declared result** dict at tuple(str, Any).

**Explicit results** answers.

**Explicit failure paths** validation helper — translated “Answers must be a JSON object.”.

**Local steps**

- If isinstance(answers, str).
  - Attempt the following.
    - Set answers from json.loads(answers).
  - On failure (ValueError).
    - Set answers from no value.
- If not isinstance(answers, dict).
  - Call the validation error handler Platform.throw(translated “Answers must be a JSON object.”, title = translated “Invalid Answers”).
- Return answers.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L121) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L870) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L846)
