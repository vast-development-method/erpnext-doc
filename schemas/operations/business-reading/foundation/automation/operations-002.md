# Workflow, automation and dispatch · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Api

<a id="op-d252fa2958e3d9"></a>
### Notification recipient options

`operation_foundation_binding_foundation_automation_engine_api_notification_recipient_options`

**Inputs** doctype, params, search\_text.

**Explicit results** (tokens + \_user\_options(doctype, params, search\_text)).

**Local steps**

- Bind dependencies recipient\_tokens.
- Set tokens from list of token for token drawn from recipient\_tokens() where \_matches\_search(token, search\_text).
  - Draw token from recipient\_tokens(), keep a combination only if (\_matches\_search(token, search\_text)).
- Return (tokens + \_user\_options(doctype, params, search\_text)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L132) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L372) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L348)

<a id="op-dbf04c1f317f7b"></a>
### Matches search

`operation_foundation_binding_foundation_automation_engine_api_matches_search`

**Inputs** token, search\_text.

**Explicit results** true · search\_text.lower() belongs to formatted text {token at “name”} {token at “full\_name”}.lower().

**Local steps**

- If not search\_text.
  - Return true.
- Return search\_text.lower() belongs to formatted text {token at “name”} {token at “full\_name”}.lower().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L131) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L371) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L347)

<a id="op-983b74d5d73137"></a>
### Trial run

`operation_foundation_binding_foundation_automation_engine_api_trial_run`

**Inputs** automation, docname = no value, branch\_overrides = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**State and service calls** savepoint TRIAL\_SAVEPOINT · rollback.

**Explicit results** \_trial\_result(row\_name, docname).

**Local steps**

- Set rule from \_trial\_target(automation, docname).
- Set overrides from \_branch\_overrides(rule, branch\_overrides).
- Evaluate Platform.db.savepoint(TRIAL\_SAVEPOINT).
- Attempt the following.
  - Within \_trial\_mode(overrides).
    - Set row\_name from \_trial\_queue\_row(rule, docname).
    - Evaluate execute\_automation(row\_name).
    - Return \_trial\_result(row\_name, docname).
- On exit, including pending return or failure.
  - Evaluate Platform.db.rollback(save\_point = TRIAL\_SAVEPOINT).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L138) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L378) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L354)

<a id="op-482583ca5e5760"></a>
### Trial mode

`operation_foundation_binding_foundation_automation_engine_api_trial_mode`

**Inputs** branch\_overrides.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Set original from Platform.db.commit.
- Set previous from Platform.flags.get(“in\_automation\_trial”).
- Set previous\_overrides from Platform.flags.get(“automation\_branch\_overrides”).
- Set Platform.db.commit from deferred anonymous expression.
- Set Platform.flags.in\_automation\_trial from true.
- Set Platform.flags.automation\_branch\_overrides from branch\_overrides.
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Set Platform.db.commit from original.
  - Set Platform.flags.in\_automation\_trial from previous.
  - Set Platform.flags.automation\_branch\_overrides from previous\_overrides.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L135) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L375) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L351)

<a id="op-bd764b38e69670"></a>
### Branch overrides

`operation_foundation_binding_foundation_automation_engine_api_branch_overrides`

**Inputs** rule, overrides.

**Declared result** dict.

**Explicit results** chosen.

**Explicit failure paths** validation helper — translated “Branch for step {0} must be If or Else”.format(idx) · validation helper — translated “Step {0} is not an If step”.format(idx).

**Local steps**

- Set overrides from Platform.parse\_json(overrides) when isinstance(overrides, str), otherwise (overrides or mapping()).
  - Value choice on isinstance(overrides, str) — true gives Platform.parse\_json(overrides), false gives (overrides or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in overrides → mapping().
- Set chosen from mapping().
- For each tuple(idx, arm) in overrides.items().
  - If arm does not belong to tuple(“If”, “Else”).
    - Call the validation error handler Platform.throw(translated “Branch for step {0} must be If or Else”.format(idx)).
  - If not rule.if\_step\_at(cint(idx)).
    - Call the validation error handler Platform.throw(translated “Step {0} is not an If step”.format(idx)).
  - Set chosen at str(cint(idx)) from arm.
- Return chosen.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L125) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L365) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L341)

<a id="op-27725a97c3e02f"></a>
### Trial target

`operation_foundation_binding_foundation_automation_engine_api_trial_target`

**Inputs** automation, docname.

**Record and data access** resolve a document from “Automation Flow” via get\_doc.

**Explicit results** rule.

**Explicit failure paths** validation helper — translated “Document-less automations do not accept a document name”.

**Local steps**

- Set rule from Platform.get\_doc(“Automation Flow”, automation).
- Evaluate Platform.has\_permission(“Automation Flow”, “write”, doc = rule, throw = true).
- If (rule.document\_type and docname).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rule.document\_type → docname.
  - Evaluate Platform.has\_permission(rule.document\_type, “read”, doc = docname, throw = true).
- Otherwise.
  - If docname.
    - Call the validation error handler Platform.throw(translated “Document-less automations do not accept a document name”).
- Return rule.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Automation Flow”, “write”, doc = rule, throw = true), Platform.has\_permission(rule.document\_type, “read”, doc = docname, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L139) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L379) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L355)

<a id="op-1adc97e1803172"></a>
### Trial queue row

`operation_foundation_binding_foundation_automation_engine_api_trial_queue_row`

**Inputs** rule, docname.

**Declared result** str.

**Record and data access** resolve a document from mapping(“doctype” → QUEUE, “automation” → rule.name, “ref\_doctype” → rule.document\_type, “ref\_name” → docname, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → QUEUE, “automation” → rule.name, “ref\_doctype” → rule.document\_type, “ref\_name” → docname, …)).

**Explicit results** row.name.

**Local steps**

- Set row from Platform.get\_doc(mapping(“doctype” → QUEUE, “automation” → rule.name, “ref\_doctype” → rule.document\_type, “ref\_name” → docname, …)).insert(ignore\_permissions = true).
- Return row.name.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L136) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L376) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L352)

<a id="op-d266a394d30a7d"></a>
### Trial result

`operation_foundation_binding_foundation_automation_engine_api_trial_result`

**Inputs** row\_name, docname.

**Declared result** dict.

**Record and data access** read RUN via get\_value · resolve a document from RUN via get\_doc.

**Explicit results** mapping(“status” → “Failed”, “document” → docname, “steps” → list(), “branches” → mapping(), …) · mapping(“status” → run.status, “document” → docname, “steps” → run\_steps(run), “branches” → (state.get(“branches”) or mapping()), …).

**Local steps**

- Set name from Platform.db.get\_value(RUN, mapping(“queue\_row” → row\_name)).
- If not name.
  - Return mapping(“status” → “Failed”, “document” → docname, “steps” → list(), “branches” → mapping(), …).
- Set run from Platform.get\_doc(RUN, name).
- Set state from Platform.parse\_json(run.run\_state) when run.run\_state, otherwise mapping().
  - Value choice on run.run\_state — true gives Platform.parse\_json(run.run\_state), false gives mapping().
- Return mapping(“status” → run.status, “document” → docname, “steps” → run\_steps(run), “branches” → (state.get(“branches”) or mapping()), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in state.get(“branches”) → mapping().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L137) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L377) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L353)

<a id="op-6da764511d73d8"></a>
### Boot

`operation_foundation_binding_foundation_flow_api_api_boot`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, Any).

**Record and data access** read “Flow Agent” via get\_list · read “Flow Model” via get\_list · read “Flow Provider” via get\_all · read “User” via get\_value.

**Explicit results** mapping(“agents” → agents, “default\_agent” → next(generator of a.name for a drawn from agents where a.name equals ASSISTANT\_AGENT\_NAME, no value), “models” → models, “providers” → Platform.get\_all(“Flow Pr ….

**Local steps**

- Evaluate Platform.has\_permission(“Flow Session”, “read”, throw = true).
- Bind dependencies sync\_site\_provider.
- Bind dependencies ASSISTANT\_AGENT\_NAME.
- Bind dependencies unavailable\_tools.
- Bind dependencies FILE\_EXTENSIONS.
- Evaluate sync\_site\_provider().
- Set agents from Platform.get\_list(“Flow Agent”, filters = mapping(“enabled” → 1), fields = list(“name”, “title”, “model”)).
- Set short from list of agent.name.rpartition(“/”) at 2 for agent drawn from agents.
  - Draw agent from agents.
- For each tuple(agent, name) in zip(agents, short, strict = true).
  - Set app from agent.name.rpartition(“/”) at 0.
  - Set agent.title from formatted text {name} ({app}) when (app and short.count(name) &gt; 1), otherwise name.
    - Value choice on (app and short.count(name) &gt; 1) — true gives formatted text {name} ({app}), false gives name.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in app → short.count(name) &gt; 1.
- Evaluate agents.sort(key = deferred anonymous expression).
- Set models from Platform.get\_list(“Flow Model”, filters = mapping(“enabled” → 1, “embedding” → 0), fields = list(“name”, “title”, “model\_id”, “provider”, …), order\_by = “title”).
- Return mapping(“agents” → agents, “default\_agent” → next(generator of a.name for a drawn from agents where a.name equals ASSISTANT\_AGENT\_NAME, no value), “models” → models, “providers” → Platform.get\_all(“Flow Pr ….
  - Draw a from agents, keep a combination only if (a.name equals ASSISTANT\_AGENT\_NAME).
  - Draw doctype from SETTINGS\_DOCTYPES.
  - Draw ptype from tuple(“read”, “write”, “create”, “delete”), keep a combination only if (Platform.has\_permission(doctype, ptype)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Flow Session”, “read”, throw = true), Platform.has\_permission(doctype, ptype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L107) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L856) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L832)

<a id="op-1e92f64dd631e3"></a>
### Create session

`operation_foundation_binding_foundation_flow_api_api_create_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** agent, model, title, approval\_mode.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L112) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L861) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L837)

<a id="op-2b249a05d59669"></a>
### Session

`operation_foundation_binding_foundation_flow_api_api_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L129) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L878) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L854)

<a id="op-0a8a57545c0346"></a>
### List sessions

`operation_foundation_binding_foundation_flow_api_api_list_sessions`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** query, limit, before.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L117) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L866) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L842)

<a id="op-8db90b7405c9b5"></a>
### Skills

`operation_foundation_binding_foundation_flow_api_api_skills`

**Inputs** session = no value, agent = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, Any).

**Record and data access** resolve a document from “Flow Agent” via get\_doc.

**Explicit results** mapping(“skills” → list of mapping(“name” → row at “command”, “description” → row at “description”) for row drawn from Platform.get\_doc(“Flow Agent”, agent).invocable\_skills()).

**Explicit failure paths** validation helper — translated “Session or agent is required.”.

**Local steps**

- If session.
  - Set agent from \_load\_session(session, “read”).agent.
- Otherwise.
  - If (isinstance(agent, str) and agent.strip()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(agent, str) → agent.strip().
    - Set agent from agent.strip().
    - Evaluate Platform.has\_permission(“Flow Agent”, “read”, agent, throw = true).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Session or agent is required.”, title = translated “Invalid Request”).
- Return mapping(“skills” → list of mapping(“name” → row at “command”, “description” → row at “description”) for row drawn from Platform.get\_doc(“Flow Agent”, agent).invocable\_skills()).
  - Draw row from Platform.get\_doc(“Flow Agent”, agent).invocable\_skills().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Flow Agent”, “read”, agent, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L138) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L887) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L863)

<a id="op-2ec3d418733235"></a>
### Run

`operation_foundation_binding_foundation_flow_api_api_run`

**Inputs** session, message, attachments = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, Any).

**Record and data access** read “Flow Run” via get\_value.

**Explicit results** mapping(“run” → run.name, “status” → “steered” when run.name equals active, otherwise “started”).

**Explicit failure paths** validation helper — translated “Message is required.”.

**Local steps**

- Set files from \_parse\_attachments(attachments).
- If (not isinstance(message, str) or not (message.strip() or files)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(message, str) → not (message.strip() or files).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in message.strip() → files.
  - Call the validation error handler Platform.throw(translated “Message is required.”, title = translated “Invalid Message”).
- Set doc from \_load\_session(session, “write”).
- Evaluate sync\_with\_retry(doc).
- Set active from Platform.db.get\_value(“Flow Run”, mapping(“session” → doc.name, “status” → “Running”), “name”, order\_by = “creation desc”).
- Set run from doc.chat(message, attachments = files).
- Return mapping(“run” → run.name, “status” → “steered” when run.name equals active, otherwise “started”).
  - Value choice on run.name equals active — true gives “steered”, false gives “started”.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L126) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L875) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L851)

<a id="op-b7206df5ae409b"></a>
### Resume

`operation_foundation_binding_foundation_flow_api_api_resume`

**Inputs** session, answers, approval\_seq = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“run” → run.name, “status” → “started”).

**Local steps**

- Set doc from \_load\_session(session, “write”).
- Set run from doc.resume(\_parse\_answers(answers), approval\_seq = (cint(approval\_seq) or no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(approval\_seq) → no value.
- Return mapping(“run” → run.name, “status” → “started”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L124) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L873) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L849)

<a id="op-78abde13c52360"></a>
### Screen result

`operation_foundation_binding_foundation_flow_api_api_screen_result`

**Inputs** session, token, screen = no value, error = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, bool).

**Explicit results** mapping(“delivered” → bool(daemon.tool\_result(doc.name, token, result).get(“delivered”))).

**Explicit failure paths** validation helper — translated “Token is required.” · validation helper — translated “A screen or an error is required.”.

**Local steps**

- Set doc from \_load\_session(session, “write”).
- If (not isinstance(token, str) or not token.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(token, str) → not token.strip().
  - Call the validation error handler Platform.throw(translated “Token is required.”, title = translated “Invalid Token”).
- If error.
  - Set result from mapping(“content” → str(error), “is\_error” → true).
- Otherwise.
  - If screen is distinct from no value.
    - Set content from screen when isinstance(screen, str), otherwise json.dumps(screen, default = str).
      - Value choice on isinstance(screen, str) — true gives screen, false gives json.dumps(screen, default = str).
    - Set result from mapping(“content” → content, “is\_error” → false).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “A screen or an error is required.”, title = translated “Invalid Screen”).
- Within DaemonClient.for\_site() bound as daemon.
  - Return mapping(“delivered” → bool(daemon.tool\_result(doc.name, token, result).get(“delivered”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L128) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L877) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L853)

<a id="op-339d680670409e"></a>
### Save secret

`operation_foundation_binding_foundation_flow_api_api_save_secret`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** session, call\_id, password.

**Explicit result forms** a structured result.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L127) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L876) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L852)

<a id="op-b2fa247cce97c1"></a>
### Waiting call

`operation_foundation_binding_foundation_flow_api_api_waiting_call`

**Inputs** doc, call\_id.

**Declared result** (dict at tuple(str, Any) bitwise or no value).

**Explicit results** no value · call.

**Local steps**

- Set rows from doc.entries(path = “active”) at “entries”.
- Set answered from set of row.get(“tool\_call\_id”) for row drawn from rows where row.get(“type”) equals “tool\_result”.
  - Draw row from rows, keep a combination only if (row.get(“type”) equals “tool\_result”).
- If call\_id belongs to answered.
  - Return no value.
- For each row in rows.
  - If row.get(“type”) equals “approval\_required”.
    - For each call in (row.get(“calls”) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“calls”) → list().
      - If call.get(“id”) equals call\_id.
        - Return call.
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L144) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L893) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L869)

<a id="op-7de4357feb6669"></a>
### Abort

`operation_foundation_binding_foundation_flow_api_api_abort`

**Inputs** session.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, str).

**Explicit results** mapping(“status” → \_load\_session(session, “write”).abort()).

**Local steps**

- Return mapping(“status” → \_load\_session(session, “write”).abort()).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L105) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L854) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L830)

<a id="op-cae0bf57a24ab1"></a>
### Cancel pending

`operation_foundation_binding_foundation_flow_api_api_cancel_pending`

**Inputs** session.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, str).

**Explicit results** mapping(“status” → \_load\_session(session, “write”).cancel\_pending()).

**Local steps**

- Return mapping(“status” → \_load\_session(session, “write”).cancel\_pending()).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L108) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L857) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L833)

<a id="op-310d7b8e5fbf9d"></a>
### Rewind

`operation_foundation_binding_foundation_flow_api_api_rewind`

**Inputs** session, target\_seq.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, str).

**Explicit results** mapping(“status” → \_load\_session(session, “write”).rewind(int(target\_seq))).

**Explicit failure paths** validation helper — translated “Rewind target must be a whole number.”.

**Local steps**

- If not str(target\_seq).isdecimal().
  - Call the validation error handler Platform.throw(translated “Rewind target must be a whole number.”, title = translated “Invalid Target”).
- Return mapping(“status” → \_load\_session(session, “write”).rewind(int(target\_seq))).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L125) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L874) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L850)

<a id="op-091003d7df2798"></a>
### Compact

`operation_foundation_binding_foundation_flow_api_api_compact`

**Inputs** session.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“run” → run.name, “status” → “started”).

**Local steps**

- Set run from \_load\_session(session, “write”).compact().
- Return mapping(“run” → run.name, “status” → “started”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L110) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L859) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L835)

<a id="op-08678c02d432d5"></a>
### Entries

`operation_foundation_binding_foundation_flow_api_api_entries`

**Inputs** session, since = 0, path = “active”.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, Any).

**Explicit results** \_load\_session(session, “read”).entries(since = cint(since), path = path).

**Explicit failure paths** validation helper — translated “Path must be active or all.”.

**Local steps**

- If path does not belong to tuple(“active”, “all”).
  - Call the validation error handler Platform.throw(translated “Path must be active or all.”, title = translated “Invalid Path”).
- Return \_load\_session(session, “read”).entries(since = cint(since), path = path).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L114) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L863) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L839)

<a id="op-803fb607a1ef54"></a>
### System prompt

`operation_foundation_binding_foundation_flow_api_api_system_prompt`

**Inputs** session.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (str bitwise or no value).

**Explicit results** no value · doc.system\_prompt().

**Local steps**

- Set doc from \_load\_session(session, “read”).
- If “System Manager” does not belong to Platform.get\_roles().
  - Return no value.
- Return doc.system\_prompt().

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L141) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L890) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L866)
