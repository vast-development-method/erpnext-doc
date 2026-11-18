# Workflow, automation and dispatch · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Core

<a id="op-6e2d8da438067c"></a>
### Assign To User.validate

`operation_foundation_binding_foundation_automation_engine_actions_core_assigntouser_validate`

**Inputs** self, params, doctype.

**Explicit failure paths** AutomationParamError(translated “At least one assignee is required”, fieldname = “assign\_to”).

**Local steps**

- If not \_as\_list(params.get(“assign\_to”)).
  - Raise AutomationParamError(translated “At least one assignee is required”, fieldname = “assign\_to”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L94) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L334) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L310)

<a id="op-60c8673845370b"></a>
### Assign To User.execute

`operation_foundation_binding_foundation_automation_engine_actions_core_assigntouser_execute`

**Inputs** self, doc, params, context.

**Explicit results** translated “Assigned to {0}”.format(“, ”.join(users)).

**Local steps**

- Bind dependencies add.
- Evaluate \_require\_doc(doc, self.label).
- Set users from \_as\_list(params.get(“assign\_to”)).
- Evaluate add(mapping(“doctype” → doc.doctype, “name” → doc.name, “assign\_to” → users, “description” → (render\_value(params.get(“description”), doc, context) or doc.doctype))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in render\_value(params.get(“description”), doc, context) → doc.doctype.
- Return translated “Assigned to {0}”.format(“, ”.join(users)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L93) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L333) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L309)

<a id="op-04650f4e929467"></a>
### Call Webhook.validate

`operation_foundation_binding_foundation_automation_engine_actions_core_callwebhook_validate`

**Inputs** self, params, doctype.

**Explicit failure paths** AutomationParamError(translated “URL is required”, fieldname = “url”) · AutomationParamError(translated “Unsupported HTTP method”, fieldname = “method”) · AutomationParamError(translated “Timeout must be between 1 and {0} seconds”.format(MAX\_WEBHOOK\_TIMEOUT), fieldname = “timeout”).

**Local steps**

- Set url from (params.get(“url”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“url”) → empty text.
- If not url.
  - Raise AutomationParamError(translated “URL is required”, fieldname = “url”).
- If “{{” does not belong to url.
  - Evaluate \_check\_url\_shape(url).
- If (params.get(“method”) or “POST”).upper() does not belong to HTTP\_METHODS.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“method”) → “POST”.
  - Raise AutomationParamError(translated “Unsupported HTTP method”, fieldname = “method”).
- If (cint(params.get(“timeout”)) &lt; 0 or cint(params.get(“timeout”)) &gt; MAX\_WEBHOOK\_TIMEOUT).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(params.get(“timeout”)) &lt; 0 → cint(params.get(“timeout”)) &gt; MAX\_WEBHOOK\_TIMEOUT.
  - Raise AutomationParamError(translated “Timeout must be between 1 and {0} seconds”.format(MAX\_WEBHOOK\_TIMEOUT), fieldname = “timeout”).
- Evaluate \_json\_param(params.get(“headers”), “headers”).
- Evaluate \_json\_param(params.get(“payload”), “payload”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L96) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L336) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L312)

<a id="op-7da355f094f56e"></a>
### Call Webhook.execute

`operation_foundation_binding_foundation_automation_engine_actions_core_callwebhook_execute`

**Inputs** self, doc, params, context.

**Explicit results** mapping(“detail” → translated “Would {0} {1} (not sent)”.format(method, url)) · mapping(“detail” → translated “{0} {1} returned {2}”.format(method, url, response.status\_code), “status\_code” → response.status\_code, “response” → body).

**Explicit failure paths** Platform.ValidationError(translated “{0} {1} returned {2}: {3}”.format(method, url, response.status\_code, body)).

**Local steps**

- Set url from render\_value(params.get(“url”), doc, context).
- Set method from (params.get(“method”) or “POST”).upper().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“method”) → “POST”.
- Set headers from \_rendered\_json(params.get(“headers”), doc, context, “headers”).
- Set payload from \_rendered\_json(params.get(“payload”), doc, context, “payload”).
- Set timeout from (cint(params.get(“timeout”)) or DEFAULT\_WEBHOOK\_TIMEOUT).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(params.get(“timeout”)) → DEFAULT\_WEBHOOK\_TIMEOUT.
- If Platform.flags.get(“in\_automation\_trial”).
  - Evaluate \_guard\_url(url).
  - Return mapping(“detail” → translated “Would {0} {1} (not sent)”.format(method, url)).
- Set response from \_send\_guarded\_request(method, url, headers, payload, …).
- Set body from (response.text or empty text) at slice no value to WEBHOOK\_RESPONSE\_LIMIT.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in response.text → empty text.
- If response.status\_code ≥ 400.
  - Raise Platform.ValidationError(translated “{0} {1} returned {2}: {3}”.format(method, url, response.status\_code, body)).
- Return mapping(“detail” → translated “{0} {1} returned {2}”.format(method, url, response.status\_code), “status\_code” → response.status\_code, “response” → body).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L95) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L335) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L311)

<a id="op-8d3fddc7345a6a"></a>
### Run Script.validate

`operation_foundation_binding_foundation_automation_engine_actions_core_runscript_validate`

**Inputs** self, params, doctype.

**Explicit failure paths** AutomationParamError(translated “Pick a Server Script or write one here, not both”, fieldname = “script”) · AutomationParamError(translated “Server Scripts are disabled. Enable them from the bench configuration.”, fieldname = “script”).

**Local steps**

- Bind dependencies is\_safe\_exec\_enabled.
- Set name from (params.get(“server\_script”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“server\_script”) → empty text.
- Set script from (params.get(“script”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“script”) → empty text.
- If (name and script).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name → script.
  - Raise AutomationParamError(translated “Pick a Server Script or write one here, not both”, fieldname = “script”).
- If not is\_safe\_exec\_enabled().
  - Raise AutomationParamError(translated “Server Scripts are disabled. Enable them from the bench configuration.”, fieldname = “script”).
- If name.
  - Evaluate self.validate\_linked\_script(name).
- Otherwise.
  - Evaluate self.validate\_own\_script(script).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate linked script](operations-017.md#op-4587c6d7f54391), [validate own script](operations-017.md#op-c39d03ed92ff62).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L113) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L353) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L329)

<a id="op-4587c6d7f54391"></a>
### Run Script.validate linked script

`operation_foundation_binding_foundation_automation_engine_actions_core_runscript_validate_linked_script`

**Inputs** self, name.

**Record and data access** read “Server Script” via get\_value.

**Explicit failure paths** AutomationParamError(translated “Unknown Server Script”, fieldname = “server\_script”) · AutomationParamError(translated “Only an {0} Server Script can be run from a flow”.format(SCRIPT\_TYPE), fieldname = “server\_script”) · AutomationParamError(translated “That Server Script is disabled”, fieldname = “server\_script”).

**Local steps**

- Set script from Platform.db.get\_value(“Server Script”, name, list(“script\_type”, “disabled”), as\_dict = true).
- If not script.
  - Raise AutomationParamError(translated “Unknown Server Script”, fieldname = “server\_script”).
- If not Platform.flags.get(“in\_automation\_run”).
  - Evaluate Platform.has\_permission(“Server Script”, “read”, doc = name, throw = true).
- If script.script\_type differs from SCRIPT\_TYPE.
  - Raise AutomationParamError(translated “Only an {0} Server Script can be run from a flow”.format(SCRIPT\_TYPE), fieldname = “server\_script”).
- If script.disabled.
  - Raise AutomationParamError(translated “That Server Script is disabled”, fieldname = “server\_script”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Server Script”, “read”, doc = name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L114) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L354) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L330)

<a id="op-c39d03ed92ff62"></a>
### Run Script.validate own script

`operation_foundation_binding_foundation_automation_engine_actions_core_runscript_validate_own_script`

**Inputs** self, script.

**Explicit failure paths** AutomationParamError(translated “Pick a Server Script, or write one here”, fieldname = “server\_script”) · AutomationParamError(translated “Only a System Manager can write a script step”, fieldname = “script”).

**Local steps**

- If not script.
  - Raise AutomationParamError(translated “Pick a Server Script, or write one here”, fieldname = “server\_script”).
- Evaluate \_compile\_script(script).
- If (not Platform.flags.get(“in\_automation\_run”) and “System Manager” does not belong to Platform.get\_roles()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.flags.get(“in\_automation\_run”) → “System Manager” does not belong to Platform.get\_roles().
  - Raise AutomationParamError(translated “Only a System Manager can write a script step”, fieldname = “script”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L115) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L355) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L331)

<a id="op-a29b26c027996a"></a>
### Run Script.execute

`operation_foundation_binding_foundation_automation_engine_actions_core_runscript_execute`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, doc, params, context.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L111) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L351) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L327)

<a id="op-077ae1ac6797f2"></a>
### Run Script.source

`operation_foundation_binding_foundation_automation_engine_actions_core_runscript_source`

**Inputs** self, params, context.

**Declared result** tuple at tuple(str, str).

**Record and data access** resolve a document from “Server Script” via get\_cached\_doc.

**Explicit results** tuple((Platform.get\_cached\_doc(“Server Script”, name).script or empty text), name) · tuple((params.get(“script”) or empty text), formatted text automation\_{rule.name} when rule, otherwise “automation”).

**Local steps**

- Set name from params.get(“server\_script”).
- If name.
  - Return tuple((Platform.get\_cached\_doc(“Server Script”, name).script or empty text), name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_doc(“Server Script”, name).script → empty text.
- Set rule from context.get(“rule”) when context, otherwise no value.
  - Value choice on context — true gives context.get(“rule”), false gives no value.
- Return tuple((params.get(“script”) or empty text), formatted text automation\_{rule.name} when rule, otherwise “automation”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“script”) → empty text.
  - Value choice on rule — true gives formatted text automation\_{rule.name}, false gives “automation”.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Server Script”, name).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L112) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L352) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L328)

<a id="op-66a694b8c3ae15"></a>
### Check url shape

`operation_foundation_binding_foundation_automation_engine_actions_core_check_url_shape`

**Inputs** url.

**Explicit failure paths** AutomationParamError(translated “URL must be http or https”, fieldname = “url”) · AutomationParamError(translated “URL has no host”, fieldname = “url”).

**Local steps**

- Set parsed from urlparse(url).
- If parsed.scheme does not belong to ALLOWED\_SCHEMES.
  - Raise AutomationParamError(translated “URL must be http or https”, fieldname = “url”).
- If not parsed.hostname.
  - Raise AutomationParamError(translated “URL has no host”, fieldname = “url”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L97) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L337) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L313)

<a id="op-9584c7cd123c17"></a>
### Guard url

`operation_foundation_binding_foundation_automation_engine_actions_core_guard_url`

**Inputs** url.

**Explicit failure paths** AutomationParamError(translated “Could not resolve host: {0}”.format(hostname), fieldname = “url”) · AutomationParamError(translated “Requests to internal network addresses are not permitted”, fieldname = “url”).

**Local steps**

- Bind dependencies ipaddress.
- Bind dependencies socket.
- Evaluate \_check\_url\_shape(url).
- Set hostname from urlparse(url).hostname.
- Attempt the following.
  - Set addr\_info from socket.getaddrinfo(hostname, no value).
- On failure (socket.gaierror).
  - Raise AutomationParamError(translated “Could not resolve host: {0}”.format(hostname), fieldname = “url”).
- For each record in addr\_info.
  - Attempt the following.
    - Set address from ipaddress.ip\_address(record at 4 at 0).
  - On failure (tuple(ValueError, IndexError)).
    - Continue with the next iteration or loop test.
  - If not address.is\_global.
    - Raise AutomationParamError(translated “Requests to internal network addresses are not permitted”, fieldname = “url”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.getaddrinfo(hostname, no value).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L102) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L342) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L318)

<a id="op-3fa00b45eff901"></a>
### Send guarded request

`operation_foundation_binding_foundation_automation_engine_actions_core_send_guarded_request`

**Inputs** method, url, headers, payload, timeout.

**Explicit results** response.

**Explicit failure paths** AutomationParamError(translated “Too many redirects”, fieldname = “url”).

**Local steps**

- Bind dependencies requests.
- Set body from Platform.as\_json(payload) when payload, otherwise no value.
  - Value choice on payload — true gives Platform.as\_json(payload), false gives no value.
- Set headers from mapping(“Content-Type” → “application/json”, expand (headers or mapping())) when body, otherwise dict((headers or mapping())).
  - Value choice on body — true gives mapping(“Content-Type” → “application/json”, expand (headers or mapping())), false gives dict((headers or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in headers → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in headers → mapping().
- For each \_hop in range((MAX\_REDIRECTS + 1)).
  - Evaluate \_guard\_url(url).
  - Set response from requests.request(method = method, url = url, data = body, headers = headers, …).
  - Set location from response.headers.get(“Location”) when response.is\_redirect, otherwise no value.
    - Value choice on response.is\_redirect — true gives response.headers.get(“Location”), false gives no value.
  - If not location.
    - Return response.
  - Set url from urljoin(url, location).
  - If (response.status\_code belongs to tuple(301, 302, 303) and method differs from “HEAD”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in response.status\_code belongs to tuple(301, 302, 303) → method differs from “HEAD”.
    - Set tuple(method, body) from tuple(“GET”, no value).
- Raise AutomationParamError(translated “Too many redirects”, fieldname = “url”).

**Values supplied outside this operation** service or queued work from requests.request(method = method, url = url, data = body, headers = headers, …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L116) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L356) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L332)

<a id="op-92680cfb0b9783"></a>
### Json param

`operation_foundation_binding_foundation_automation_engine_actions_core_json_param`

**Inputs** value, fieldname.

**Explicit results** mapping() · value · parsed.

**Explicit failure paths** AutomationParamError(translated “{0} must be a JSON object”.format(fieldname), fieldname = fieldname).

**Local steps**

- If not value.
  - Return mapping().
- If isinstance(value, dict).
  - Return value.
- Set parsed from Platform.parse\_json(value).
- If not isinstance(parsed, dict).
  - Raise AutomationParamError(translated “{0} must be a JSON object”.format(fieldname), fieldname = fieldname).
- Return parsed.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L106) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L346) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L322)

<a id="op-ad7917512460c1"></a>
### Rendered json

`operation_foundation_binding_foundation_automation_engine_actions_core_rendered_json`

**Inputs** value, doc, context, fieldname.

**Explicit results** mapping of key → render\_value(item, doc, context) for tuple(key, item) drawn from \_json\_param(value, fieldname).items().

**Local steps**

- Return mapping of key → render\_value(item, doc, context) for tuple(key, item) drawn from \_json\_param(value, fieldname).items().
  - Draw tuple(key, item) from \_json\_param(value, fieldname).items().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L108) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L348) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L324)

<a id="op-47b62a0316bee2"></a>
### Compile script

`operation_foundation_binding_foundation_automation_engine_actions_core_compile_script`

**Inputs** script.

**Explicit failure paths** AutomationParamError(str(error), fieldname = “script”).

**Local steps**

- Bind dependencies compile\_restricted.
- Bind dependencies PlatformTransformer.
- Attempt the following.
  - Evaluate compile\_restricted(script, policy = PlatformTransformer).
- On failure (Exception) bound to error.
  - Raise AutomationParamError(str(error), fieldname = “script”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L98) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L338) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L314)

## Service · Dispatch

<a id="op-59261ff484ba7b"></a>
### Run automations

`operation_foundation_binding_foundation_automation_engine_dispatch_run_automations`

**Inputs** doc, method.

**Explicit results** no value.

**Local steps**

- Set trigger\_type from METHOD\_TRIGGER.get(method).
- If (not trigger\_type or not \_dispatch\_allowed()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not trigger\_type → not \_dispatch\_allowed().
  - Return no value.
- If (trigger\_type equals “Doc Updated” and doc.flags.get(“in\_insert”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in trigger\_type equals “Doc Updated” → doc.flags.get(“in\_insert”).
  - Return no value.
- Set rules from get\_automations\_for(doc.doctype).
- If not rules.
  - Return no value.
- Set matched from list of r for r drawn from rules where (r.trigger\_type equals trigger\_type and matches\_rule(r, doc)).
  - Draw r from rules, keep a combination only if ((r.trigger\_type equals trigger\_type and matches\_rule(r, doc))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in r.trigger\_type equals trigger\_type → matches\_rule(r, doc).
- If not matched.
  - Return no value.
- Set depth from (cint(Platform.flags.get(“automation\_depth”)) + 1).
- Set max\_depth from settings.get(“max\_depth”).
- If depth &gt; max\_depth.
  - Evaluate \_log\_depth\_refusal(doc, max\_depth).
  - Return no value.
- For each rule in matched.
  - Evaluate queue\_trigger(rule.name, doc.doctype, doc.name, depth = depth).
- Evaluate Platform.db.after\_commit.add(kick\_drainer).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L166) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L406) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L382)

<a id="op-66f8b042540e3a"></a>
### Dispatch allowed

`operation_foundation_binding_foundation_automation_engine_dispatch_dispatch_allowed`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** false · settings.is\_enabled().

**Local steps**

- Set flags from Platform.flags.
- If (flags.in\_install or flags.in\_patch or flags.in\_migrate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flags.in\_install → flags.in\_patch → flags.in\_migrate.
  - Return false.
- Return settings.is\_enabled().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L159) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L399) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L375)

<a id="op-f7e119d25c449f"></a>
### Log depth refusal

`operation_foundation_binding_foundation_automation_engine_dispatch_log_depth_refusal`

**Inputs** doc, max\_depth.

**Local steps**

- Set previous from Platform.flags.get(“skip\_automations”).
- Set Platform.flags.skip\_automations from true.
- Attempt the following.
  - Evaluate Platform.log\_error(title = “Automation Flow depth limit reached”, message = formatted text Skipped automations for {doc.doctype} {doc.name} at depth {max\_depth}).
- On exit, including pending return or failure.
  - Set Platform.flags.skip\_automations from previous.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L162) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L402) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L378)

<a id="op-212305b58f0f8c"></a>
### Matches rule

`operation_foundation_binding_foundation_automation_engine_dispatch_matches_rule`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** rule, doc.

**Explicit result forms** Boolean false, a value selected from the current context.

**Observed service boundaries** diagnostic or audit logging.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L163) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L403) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L379)

<a id="op-b0fbf9f2c5ca18"></a>
### Field changed

`operation_foundation_binding_foundation_automation_engine_dispatch_field_changed`

**Inputs** rule, doc.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Set before from doc.get\_doc\_before\_save().
- If not before.
  - Return false.
- Set tuple(old, new) from tuple(before.get(rule.trigger\_field), doc.get(rule.trigger\_field)).
- If old equals new.
  - Return false.
- If (rule.from\_value does not belong to tuple(no value, empty text) and cstr(old) differs from cstr(rule.from\_value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rule.from\_value does not belong to tuple(no value, empty text) → cstr(old) differs from cstr(rule.from\_value).
  - Return false.
- If (rule.to\_value does not belong to tuple(no value, empty text) and cstr(new) differs from cstr(rule.to\_value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rule.to\_value does not belong to tuple(no value, empty text) → cstr(new) differs from cstr(rule.to\_value).
  - Return false.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L160) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L400) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L376)

<a id="op-2877d8a8389b03"></a>
### Queue trigger

`operation_foundation_binding_foundation_automation_engine_dispatch_queue_trigger`

**Inputs** automation, doctype, docname, run\_after = no value, payload = no value, depth = 0.

**State and service calls** request new\_doc for QUEUE · call insert on row.

**Explicit results** \_touch\_row(existing, run\_after, payload, depth) · row.name · \_touch\_row(existing, run\_after, payload, depth) when existing, otherwise no value.

**Local steps**

- Set existing from \_pending\_row(automation, doctype, docname).
- If existing.
  - Return \_touch\_row(existing, run\_after, payload, depth).
- Set row from Platform.new\_doc(QUEUE).
- Evaluate row.update(mapping(“automation” → automation, “ref\_doctype” → doctype, “ref\_name” → docname, “status” → queue\_status(run\_after), …)).
  - Value choice on payload — true gives Platform.as\_json(payload), false gives no value.
- Attempt the following.
  - Evaluate row.insert(ignore\_permissions = true).
  - Return row.name.
- On failure (tuple(Platform.UniqueValidationError, Platform.DuplicateEntryError)).
  - Set existing from \_pending\_row(automation, doctype, docname).
  - Return \_touch\_row(existing, run\_after, payload, depth) when existing, otherwise no value.
    - Value choice on existing — true gives \_touch\_row(existing, run\_after, payload, depth), false gives no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L165) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L405) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L381)

<a id="op-d50c27bfa79652"></a>
### Pending row

`operation_foundation_binding_foundation_automation_engine_dispatch_pending_row`

**Inputs** automation, doctype, docname.

**Record and data access** read QUEUE via get\_value.

**Explicit results** Platform.db.get\_value(QUEUE, mapping(“automation” → automation, “ref\_doctype” → doctype, “ref\_name” → docname, “status” → tuple(“in”, WAITING\_STATES), …), list(“name”, “depth”), as\_dict = true).

**Local steps**

- Return Platform.db.get\_value(QUEUE, mapping(“automation” → automation, “ref\_doctype” → doctype, “ref\_name” → docname, “status” → tuple(“in”, WAITING\_STATES), …), list(“name”, “depth”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L164) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L404) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L380)

<a id="op-e548edcceca928"></a>
### Touch row

`operation_foundation_binding_foundation_automation_engine_dispatch_touch_row`

**Inputs** row, run\_after, payload = no value, depth = 0.

**State and service calls** request set\_value on QUEUE.

**Explicit results** row.name.

**Local steps**

- Set values from mapping(“triggered\_at” → now(), “triggered\_by” → Platform.session.user, “run\_after” → run\_after, “status” → queue\_status(run\_after), …).
- If payload is distinct from no value.
  - Set values at “event\_payload” from Platform.as\_json(payload).
- Evaluate Platform.db.set\_value(QUEUE, row.name, values, update\_modified = false).
- Return row.name.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L167) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L407) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L383)

<a id="op-e5c33c1183d686"></a>
### Kick drainer

`operation_foundation_binding_foundation_automation_engine_dispatch_kick_drainer`

**Inputs** no declared parameters.

**State and service calls** enqueue with “Platform.automation\_engine.drainer.drain”.

**Local steps**

- Evaluate Platform.enqueue(“Platform.automation\_engine.drainer.drain”, queue = DRAIN\_QUEUE, job\_id = formatted text automation\_drain::{Platform.local.site}, deduplicate = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.automation\_engine.drainer.drain”, queue = DRAIN\_QUEUE, job\_id = formatted text automation\_drain::{Platform.local.site}, deduplicate = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L161) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L401) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L377)
