# Workflow, automation and dispatch · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Builtins

<a id="op-b116fc7b4bd762"></a>
### Api server script

`operation_foundation_binding_foundation_flow_tools_builtins_api_server_script`

**Inputs** path.

**Declared result** (str bitwise or no value).

**Explicit results** no value · get\_server\_script\_map().get(“\_api”, mapping()).get(Platform.override\_whitelisted\_method(path)).

**Local steps**

- If not isinstance(path, str).
  - Return no value.
- Return get\_server\_script\_map().get(“\_api”, mapping()).get(Platform.override\_whitelisted\_method(path)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L124) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1365) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1341)

<a id="op-4ff2b041311a3a"></a>
### Function title

`operation_foundation_binding_foundation_flow_tools_builtins_function_title`

**Inputs** path.

**Declared result** str.

**Explicit results** “: ”.join(generator of translated Platform.unscrub(part) for part drawn from path.split(“.”) at slice negative 2 to no value).

**Local steps**

- Return “: ”.join(generator of translated Platform.unscrub(part) for part drawn from path.split(“.”) at slice negative 2 to no value).
  - Draw part from path.split(“.”) at slice negative 2 to no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L154) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1395) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1371)

<a id="op-b1c7a3abd60112"></a>
### Request secret

`operation_foundation_binding_foundation_flow_tools_builtins_request_secret`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doctype, name, fieldname, reason, ctx.

**Explicit result forms** a structured result.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L173) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1414) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1390)

<a id="op-2970001cfa9196"></a>
### Secret field refusal

`operation_foundation_binding_foundation_flow_tools_builtins_secret_field_refusal`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doctype, name, fieldname.

**Explicit result forms** no value, the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L182) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1423) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1399)

<a id="op-a3702680a16ba7"></a>
### Save secret

`operation_foundation_binding_foundation_flow_tools_builtins_save_secret`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, args, password.

**Observed service boundaries** record lookup, record mutation request, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L180) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1421) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1397)

<a id="op-facb9f909008e5"></a>
### Secret key

`operation_foundation_binding_foundation_flow_tools_builtins_secret_key`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, doctype, name, fieldname.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L183) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1424) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1400)

<a id="op-a2553766618e62"></a>
### Sync builtin tools

`operation_foundation_binding_foundation_flow_tools_builtins_sync_builtin_tools`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Bind dependencies \_ensure\_tool.
- For each builtin in BUILTIN\_TOOLS.
  - Evaluate \_ensure\_tool(builtin).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L188) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1429) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1405)

## Service · Callback

<a id="op-1c406feddd9bf9"></a>
### Callback

`operation_foundation_binding_foundation_flow_daemon_callback_callback`

**Inputs** callback\_type, remaining named values payload.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true, methods = list(“POST”)).

**Declared result** dict.

**Explicit results** tool\_callback(expanded names payload) · run\_ended\_callback(expanded names payload).

**Explicit failure paths** validation helper — translated “Unknown callback type {0}.”.format(callback\_type).

**Local steps**

- Evaluate \_authenticate().
- Evaluate payload.pop(“cmd”, no value).
- If callback\_type equals “tool”.
  - Return tool\_callback(expanded names payload).
- If callback\_type equals “run\_ended”.
  - Return run\_ended\_callback(expanded names payload).
- Call the validation error handler Platform.throw(translated “Unknown callback type {0}.”.format(callback\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L160) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L909) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L885)

<a id="op-19a40103649cdd"></a>
### Tool callback

`operation_foundation_binding_foundation_flow_daemon_callback_tool_callback`

**Inputs** session\_id, tool, args = no value, mode = “execute”, user\_context = no value, result\_token = no value.

**Declared result** dict.

**Record and data access** read “Flow Session” via get\_value · read “Flow Agent Sub Agent” via exists · read “User” via get\_value.

**State and service calls** rollback.

**Explicit results** \_error(translated “Unknown session {0}.”.format(session\_id)) · \_error(translated “{0} is not a sub-agent of {1}.”.format(agent, session.agent)) · \_error(translated “The session's owner is disabled.”) · \_dispatch(session\_id, agent, tool, (args or mapping()), …) · \_error((str(exc).strip() or type(exc).\_\_name\_\_)).

**Explicit failure paths** validation helper — translated “Unknown callback mode {0}.”.format(mode).

**Local steps**

- If mode does not belong to tuple(“execute”, “confirm”).
  - Call the validation error handler Platform.throw(translated “Unknown callback mode {0}.”.format(mode)).
- Set session from Platform.db.get\_value(“Flow Session”, session\_id, list(“owner”, “agent”), as\_dict = true).
- If not session.
  - Return \_error(translated “Unknown session {0}.”.format(session\_id)).
- Set agent from ((user\_context or mapping()).get(“agent”) or session.agent).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (user\_context or mapping()).get(“agent”) → session.agent.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_context → mapping().
- If (agent differs from session.agent and not Platform.db.exists(“Flow Agent Sub Agent”, mapping(“parent” → session.agent, “agent” → agent))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in agent differs from session.agent → not Platform.db.exists(“Flow Agent Sub Agent”, mapping(“parent” → session.agent, “agent” → agent)).
  - Return \_error(translated “{0} is not a sub-agent of {1}.”.format(agent, session.agent)).
- If not Platform.db.get\_value(“User”, session.owner, “enabled”).
  - Return \_error(translated “The session's owner is disabled.”).
- Set user from Platform.session.user.
- Evaluate Platform.set\_user(session.owner).
- Attempt the following.
  - Return \_dispatch(session\_id, agent, tool, (args or mapping()), …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args → mapping().
- On failure (Exception) bound to exc.
  - Evaluate Platform.db.rollback().
  - Return \_error((str(exc).strip() or type(exc).\_\_name\_\_)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in str(exc).strip() → type(exc).\_\_name\_\_.
- On exit, including pending return or failure.
  - Evaluate Platform.set\_user(user).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L174) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L923) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L899)

<a id="op-5053732fb0f253"></a>
### Run ended callback

`operation_foundation_binding_foundation_flow_daemon_callback_run_ended_callback`

**Inputs** session\_id, terminal\_seq.

**Declared result** dict.

**Record and data access** resolve a document from “Flow Session” via get\_doc.

**Explicit results** mapping(“synced\_through” → session.last\_synced\_seq).

**Explicit failure paths** validation helper — translated “Terminal sequence is required.” · validation helper — translated “Unknown session {0}.”.format(session\_id) · validation helper — translated “The flow server did not expose terminal sequence {0}.”.format(terminal\_seq).

**Local steps**

- Attempt the following.
  - Set terminal\_seq from int(terminal\_seq).
- On failure (tuple(TypeError, ValueError)).
  - Set terminal\_seq from 0.
- If terminal\_seq &lt; 1.
  - Call the validation error handler Platform.throw(translated “Terminal sequence is required.”).
- Attempt the following.
  - Set session from Platform.get\_doc(“Flow Session”, session\_id).
- On failure (Platform.DoesNotExistError).
  - Call the validation error handler Platform.throw(translated “Unknown session {0}.”.format(session\_id)).
- Set user from Platform.session.user.
- Evaluate Platform.set\_user(session.owner).
- Attempt the following.
  - Evaluate sync\_with\_retry(session).
  - If session.last\_synced\_seq &lt; terminal\_seq.
    - Call the validation error handler Platform.throw(translated “The flow server did not expose terminal sequence {0}.”.format(terminal\_seq), title = translated “Flow Server”).
  - Evaluate call\_on\_complete(session).
  - Return mapping(“synced\_through” → session.last\_synced\_seq).
- On exit, including pending return or failure.
  - Evaluate Platform.set\_user(user).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L172) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L921) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L897)

<a id="op-0f4e1b02f5c6e5"></a>
### Authenticate

`operation_foundation_binding_foundation_flow_daemon_callback_authenticate`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Locally raised failures** AuthenticationError.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L159) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L908) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L884)

<a id="op-77d131b8b62a11"></a>
### Dispatch

`operation_foundation_binding_foundation_flow_daemon_callback_dispatch`

**Inputs** session\_id, agent, name, args, mode, result\_token.

**Declared result** dict.

**Record and data access** resolve a document from “Flow Agent” via get\_doc.

**Explicit results** \_error(translated “The session's agent is disabled.”) · \_error(translated “Unknown tool {0}.”.format(name)) · mapping(“requires\_confirmation” → false) · mapping(“prompt” → confirm\_prompt(tool, args), expand mapping(“needs\_user” → true) when tool.needs\_user, otherwise mapping()) · \_enqueue(session\_id, agent, name, args, …) · 2 additional forms in the steps below.

**Local steps**

- Set agent\_doc from Platform.get\_doc(“Flow Agent”, agent).
- If not agent\_doc.enabled.
  - Return \_error(translated “The session's agent is disabled.”).
- Set tools from agent\_doc.client\_tools(session\_id).
- Set tool from next(generator of tool for tool drawn from tools where tool.name equals name, no value).
  - Draw tool from tools, keep a combination only if (tool.name equals name).
- If tool is identical to no value.
  - Return \_error(translated “Unknown tool {0}.”.format(name)).
- If mode equals “confirm”.
  - If not \_requires\_confirmation(tool, args).
    - Return mapping(“requires\_confirmation” → false).
  - Return mapping(“prompt” → confirm\_prompt(tool, args), expand mapping(“needs\_user” → true) when tool.needs\_user, otherwise mapping()).
    - Value choice on tool.needs\_user — true gives mapping(“needs\_user” → true), false gives mapping().
- If (result\_token and tool.background(args) when callable(tool.background), otherwise tool.background).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in result\_token → tool.background(args) when callable(tool.background), otherwise tool.background.
  - Value choice on callable(tool.background) — true gives tool.background(args), false gives tool.background.
  - Return \_enqueue(session\_id, agent, name, args, …).
- Set ctx from ToolContext(session\_id = session\_id, agent = agent, user = Platform.session.user, result\_token = result\_token).
- Set result from tool(expanded names args, ctx = ctx).
- If isinstance(result, Pending).
  - Return mapping(“pending” → true, “timeout” → result.timeout).
- Return mapping(“content” → \_text(result), “is\_error” → false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L165) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L914) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L890)

<a id="op-e9985badc0bb44"></a>
### Enqueue

`operation_foundation_binding_foundation_flow_daemon_callback_enqueue`

**Inputs** session\_id, agent, tool, args, result\_token.

**Declared result** dict.

**State and service calls** enqueue with “Platform.flow.daemon.callback.run\_background\_tool”.

**Explicit results** mapping(“pending” → true, “timeout” → ((START\_WITHIN + timeout) + 60)).

**Local steps**

- Set timeout from (Platform.conf.flow\_background\_tool\_timeout or JOB\_TIMEOUT).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.flow\_background\_tool\_timeout → JOB\_TIMEOUT.
- Evaluate Platform.enqueue(“Platform.flow.daemon.callback.run\_background\_tool”, queue = “long”, timeout = timeout, session\_id = session\_id, tool = tool, …).
- Return mapping(“pending” → true, “timeout” → ((START\_WITHIN + timeout) + 60)).

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.flow.daemon.callback.run\_background\_tool”, queue = “long”, timeout = timeout, session\_id = session\_id, tool = tool, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L166) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L915) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L891)

<a id="op-4867d84de624fd"></a>
### Run background tool

`operation_foundation_binding_foundation_flow_daemon_callback_run_background_tool`

**Inputs** session\_id, tool, args, user\_context, result\_token, start\_by.

**Declared result** no value.

**State and service calls** commit.

**Explicit results** no value.

**Local steps**

- Within DaemonClient.for\_site() bound as daemon.
  - If time.time() &gt; start\_by.
    - Set result from \_error(translated “The tool did not run: it waited too long for a background worker.”).
  - Otherwise.
    - If not daemon.tool\_waiting(session\_id, result\_token) at “waiting”.
      - Return no value.
    - Otherwise.
      - Set result from tool\_callback(session\_id, tool, args, user\_context = user\_context).
      - Evaluate Platform.db.commit().
  - Evaluate \_deliver(daemon, session\_id, result\_token, result).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L171) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L920) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L896)

<a id="op-44af7b9d8f33a6"></a>
### Deliver

`operation_foundation_binding_foundation_flow_daemon_callback_deliver`

**Inputs** daemon, session\_id, result\_token, result.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- For each tuple(attempt, delay) in enumerate(DELIVERY\_RETRY\_DELAYS, start = 1).
  - Evaluate time.sleep(delay).
  - Attempt the following.
    - Evaluate daemon.tool\_result(session\_id, result\_token, result).
    - Return no value.
  - On failure (DaemonError).
    - If attempt equals len(DELIVERY\_RETRY\_DELAYS).
      - Propagate the active failure.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L164) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L913) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L889)

<a id="op-a45218a55e12aa"></a>
### Error

`operation_foundation_binding_foundation_flow_daemon_callback_error`

**Inputs** message.

**Declared result** dict.

**Explicit results** mapping(“content” → message at slice no value to ERROR\_LIMIT, “is\_error” → true).

**Local steps**

- Return mapping(“content” → message at slice no value to ERROR\_LIMIT, “is\_error” → true).

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L167) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L916) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L892)

<a id="op-0e618da6e69572"></a>
### Text

`operation_foundation_binding_foundation_flow_daemon_callback_text`

**Inputs** result.

**Declared result** str.

**Explicit results** result · empty text · json.dumps(result, default = str).

**Local steps**

- If isinstance(result, str).
  - Return result.
- If result is identical to no value.
  - Return empty text.
- Return json.dumps(result, default = str).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L173) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L922) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L898)

<a id="op-2056974108a034"></a>
### Requires confirmation

`operation_foundation_binding_foundation_flow_daemon_callback_requires_confirmation`

**Inputs** tool, args.

**Declared result** bool.

**Explicit results** true · bool(tool.requires\_confirmation(args)).

**Local steps**

- If not callable(tool.requires\_confirmation).
  - Return true.
- Attempt the following.
  - Return bool(tool.requires\_confirmation(args)).
- On failure (Exception).
  - Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L170) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L919) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L895)

<a id="op-ee6c1f63e40d1c"></a>
### Confirm prompt

`operation_foundation_binding_foundation_flow_daemon_callback_confirm_prompt`

**Inputs** tool, args.

**Declared result** str.

**Explicit results** formatted text {confirm\_title(tool.name, args)} {body}.

**Local steps**

- Set body from tool.confirm\_prompt(args) when tool.confirm\_prompt, otherwise json.dumps(args, indent = 2, default = str).
  - Value choice on tool.confirm\_prompt — true gives tool.confirm\_prompt(args), false gives json.dumps(args, indent = 2, default = str).
- Return formatted text {confirm\_title(tool.name, args)} {body}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L161) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L910) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L886)

<a id="op-a55fdbcdc476f5"></a>
### Confirm title

`operation_foundation_binding_foundation_flow_daemon_callback_confirm_title`

**Inputs** name, args.

**Declared result** str.

**Record and data access** read “DocType” via exists.

**Explicit results** \_count(“Create 1 {0} record”, “Create {0} {1} records”, args.get(“records”), doctype) · \_count(“Update 1 {0} record”, “Update {0} {1} records”, args.get(“names”), doctype) · \_count(“Delete 1 {0} record”, “Delete {0} {1} records”, args.get(“names”), doctype) · function\_title(args at “method”) · function\_title(action) · 4 additional forms in the steps below.

**Local steps**

- Set doctype from args.get(“doctype”) when isinstance(args.get(“doctype”), str), otherwise empty text.
  - Value choice on isinstance(args.get(“doctype”), str) — true gives args.get(“doctype”), false gives empty text.
- Set action from args.get(“action”) when isinstance(args.get(“action”), str), otherwise empty text.
  - Value choice on isinstance(args.get(“action”), str) — true gives args.get(“action”), false gives empty text.
- If (name equals “create” and doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name equals “create” → doctype.
  - Return \_count(“Create 1 {0} record”, “Create {0} {1} records”, args.get(“records”), doctype).
- If (name equals “update” and doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name equals “update” → doctype.
  - Return \_count(“Update 1 {0} record”, “Update {0} {1} records”, args.get(“names”), doctype).
- If (name equals “delete” and doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name equals “delete” → doctype.
  - Return \_count(“Delete 1 {0} record”, “Delete {0} {1} records”, args.get(“names”), doctype).
- If (name equals “call\_api” and isinstance(args.get(“method”), str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name equals “call\_api” → isinstance(args.get(“method”), str).
  - Bind dependencies function\_title.
  - Return function\_title(args at “method”).
- If (name equals “run\_action” and action).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name equals “run\_action” → action.
  - Bind dependencies function\_title, is\_function\_path.
  - If is\_function\_path(action).
    - Return function\_title(action).
  - Set target from formatted text {\_list\_count\_or\_one(args.get(“names”))} {doctype} when doctype, otherwise translated “records”.
    - Value choice on doctype — true gives formatted text {\_list\_count\_or\_one(args.get(“names”))} {doctype}, false gives translated “records”.
  - Return translated “Run "{0}" on {1}”.format(\_humanize(action), target).
- If (name equals “request\_secret” and doctype and Platform.db.exists(“DocType”, doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name equals “request\_secret” → doctype → Platform.db.exists(“DocType”, doctype).
  - Set label from Platform.get\_meta(doctype).get\_label(args.get(“fieldname”)).
  - Return translated “Enter {0} for {1} {2}”.format(translated label, translated doctype, args.get(“name”)).
- If name equals “execute”.
  - Set description from args.get(“description”).
  - Return (description.strip() when isinstance(description, str), otherwise empty text or translated “Run Python code”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in description.strip() when isinstance(description, str), otherwise empty text → translated “Run Python code”.
    - Value choice on isinstance(description, str) — true gives description.strip(), false gives empty text.
- Return \_humanize(name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L162) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L911) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L887)

<a id="op-d85774543b22fe"></a>
### Count

`operation_foundation_binding_foundation_flow_daemon_callback_count`

**Inputs** one, many, value, doctype.

**Declared result** str.

**Explicit results** translated one.format(doctype) when n equals 1, otherwise translated many.format(n, doctype).

**Local steps**

- Set n from \_list\_count\_or\_one(value).
- Return translated one.format(doctype) when n equals 1, otherwise translated many.format(n, doctype).
  - Value choice on n equals 1 — true gives translated one.format(doctype), false gives translated many.format(n, doctype).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L163) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L912) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L888)

<a id="op-b915a2acbb5aa4"></a>
### List count or one

`operation_foundation_binding_foundation_flow_daemon_callback_list_count_or_one`

**Inputs** value.

**Declared result** int.

**Explicit results** len(value) when isinstance(value, list), otherwise 1.

**Local steps**

- Return len(value) when isinstance(value, list), otherwise 1.
  - Value choice on isinstance(value, list) — true gives len(value), false gives 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L169) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L918) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L894)

<a id="op-d6a3c7e4ecc99b"></a>
### Humanize

`operation_foundation_binding_foundation_flow_daemon_callback_humanize`

**Inputs** name.

**Declared result** str.

**Explicit results** (name at slice no value to 1.upper() + name at slice 1 to no value).

**Local steps**

- Set name from name.replace(“\_”, one space).
- Return (name at slice no value to 1.upper() + name at slice 1 to no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L168) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L917) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L893)

## Service · Chunker

<a id="op-e28788e485e055"></a>
### Chunk text

`operation_foundation_binding_foundation_flow_knowledge_chunker_chunk_text`

**Inputs** text, chunk\_size (named only), overlap (named only).

**Declared result** list at str.

**Explicit results** list() · list(text) · chunks.

**Explicit failure paths** ValueError(“chunk\_size must be &gt;= 1”) · ValueError(“overlap must be in &#91;0, chunk\_size)”).

**Local steps**

- If chunk\_size &lt; 1.
  - Raise ValueError(“chunk\_size must be &gt;= 1”).
- If (overlap &lt; 0 or overlap ≥ chunk\_size).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in overlap &lt; 0 → overlap ≥ chunk\_size.
  - Raise ValueError(“overlap must be in &#91;0, chunk\_size)”).
- Set text from text.strip().
- If not text.
  - Return list().
- If len(text) ≤ chunk\_size.
  - Return list(text).
- Set chunks from list().
- Set start from 0.
- Set length from len(text).
- While start &lt; length.
  - Set end from min((start + chunk\_size), length).
  - If end &lt; length.
    - Set boundary from max(text.rfind(one space, start, end), text.rfind(whitespace '\\n', start, end)).
    - If boundary &gt; start.
      - Set end from boundary.
  - Set chunk from text at slice start to end.strip().
  - If chunk.
    - Evaluate chunks.append(chunk).
  - If end ≥ length.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set start from max((end − overlap), (start + 1)).
- Return chunks.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L173) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1175) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1151)
