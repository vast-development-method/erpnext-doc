# Workflow, automation and dispatch · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Client

<a id="op-eb804b9333e8ea"></a>
### Daemon Error.initialize

`operation_foundation_binding_foundation_flow_daemon_client_daemonerror_init`

**Inputs** self, status, detail.

**Local steps**

- Evaluate super().\_\_init\_\_(formatted text flow server {status}: {detail} when status, otherwise formatted text flow server unreachable: {detail}).
  - Value choice on status — true gives formatted text flow server {status}: {detail}, false gives formatted text flow server unreachable: {detail}.
- Set self.status from status.
- Set self.detail from detail.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L198) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L947) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L923)

<a id="op-d996ef53756cd4"></a>
### Daemon Client.initialize

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_init`

**Inputs** self, socket\_path, token = no value, site (named only, default no value), transport (named only, default no value).

**Local steps**

- Set headers from mapping(“Authorization” → formatted text Bearer {token}) when token, otherwise mapping().
  - Value choice on token — true gives mapping(“Authorization” → formatted text Bearer {token}), false gives mapping().
- If site.
  - Set headers at “X-Flow-Site” from site.
- Set self.\_http from httpx.Client(transport = (transport or httpx.HTTPTransport(uds = socket\_path)), base\_url = text in the contract, headers = headers).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in transport → httpx.HTTPTransport(uds = socket\_path).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from httpx.Client(transport = (transport or httpx.HTTPTransport(uds = socket\_path)), base\_url = text in the contract, headers = headers), httpx.HTTPTransport(uds = socket\_path).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L189) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L938) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L914)

<a id="op-85c20d8e54492d"></a>
### Daemon Client.for site

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_for_site`

**Inputs** cls.

**Wrappers, in declaration order** classmethod.

**Declared result** DaemonClient.

**Explicit results** cls(str(lifecycle.socket\_path()), Platform.conf.flow\_server\_secret, site = Platform.local.site).

**Explicit failure paths** DaemonError(no value, “this site is not provisioned; run ′bench flow-server setup′”).

**Local steps**

- Bind dependencies Platform.
- Bind dependencies lifecycle.
- If not Platform.conf.flow\_server\_secret.
  - Raise DaemonError(no value, “this site is not provisioned; run ′bench flow-server setup′”).
- Return cls(str(lifecycle.socket\_path()), Platform.conf.flow\_server\_secret, site = Platform.local.site).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L186) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L935) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L911)

<a id="op-31996474b57553"></a>
### Daemon Client.enter context

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_enter`

**Inputs** self.

**Declared result** DaemonClient.

**Explicit results** self.

**Local steps**

- Return self.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L183) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L932) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L908)

<a id="op-16e6d05ff3f734"></a>
### Daemon Client.exit context

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_exit`

**Inputs** self, remaining positional values exc.

**Declared result** no value.

**Local steps**

- Evaluate self.close().

If control reaches the end, it returns no value.

**Methods declared on this owner** [close](operations-014.md#op-86f07a45871a5a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L185) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L934) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L910)

<a id="op-86f07a45871a5a"></a>
### Daemon Client.close

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_close`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.\_http.close().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L179) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L928) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L904)

<a id="op-51ef0fbed834fb"></a>
### Daemon Client.call

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_call`

**Inputs** self, method, path, timeout (named only, default TIMEOUT), remaining named values request.

**Declared result** Any.

**Explicit results** response.json().

**Explicit failure paths** DaemonError(no value, formatted text {type(exc).\_\_name\_\_}: {exc}) · DaemonError(response.status\_code, \_detail(response)).

**Local steps**

- Attempt the following.
  - Set response from self.\_http.request(method, path, timeout = timeout, expanded names request).
- On failure (httpx.HTTPError) bound to exc.
  - Raise DaemonError(no value, formatted text {type(exc).\_\_name\_\_}: {exc}) with cause no value.
- If response.is\_error.
  - Raise DaemonError(response.status\_code, \_detail(response)).
- Return response.json().

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L176) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L925) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L901)

<a id="op-c0e85e7807b6ef"></a>
### Daemon Client.healthz

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_healthz`

**Inputs** self.

**Declared result** dict.

**Explicit results** self.\_call(“GET”, “/healthz”).

**Local steps**

- Return self.\_call(“GET”, “/healthz”).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L188) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L937) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L913)

<a id="op-1bdc4c80892a73"></a>
### Daemon Client.create session

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_create_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, config.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L181) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L930) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L906)

<a id="op-b9eba28e8e11d2"></a>
### Daemon Client.get session

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_get_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, sid.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L187) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L936) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L912)

<a id="op-3c72829b4765da"></a>
### Daemon Client.delete session

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_delete_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, sid.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L182) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L931) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L907)

<a id="op-ef79d0f087c67c"></a>
### Daemon Client.run

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_run`

**Inputs** self, sid, message, attachments (named only, default no value).

**Declared result** dict.

**Explicit results** self.\_call(“POST”, formatted text /sessions/{sid}/run, json = body).

**Local steps**

- Set body from mapping(“message” → message, “attachments” → (attachments or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in attachments → list().
- Return self.\_call(“POST”, formatted text /sessions/{sid}/run, json = body).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L193) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L942) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L918)

<a id="op-b33fcf288990ea"></a>
### Daemon Client.resume

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_resume`

**Inputs** self, sid, answers, approval\_seq (named only).

**Declared result** dict.

**Explicit results** self.\_call(“POST”, formatted text /sessions/{sid}/resume, json = body).

**Local steps**

- Set body from mapping(“approval\_seq” → approval\_seq, “answers” → answers).
- Return self.\_call(“POST”, formatted text /sessions/{sid}/resume, json = body).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L191) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L940) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L916)

<a id="op-4f33f03e0c2e60"></a>
### Daemon Client.abort

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_abort`

**Inputs** self, sid.

**Declared result** dict.

**Explicit results** self.\_call(“POST”, formatted text /sessions/{sid}/abort).

**Local steps**

- Return self.\_call(“POST”, formatted text /sessions/{sid}/abort).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L175) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L924) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L900)

<a id="op-ecfebd6d1dc3e1"></a>
### Daemon Client.cancel pending

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_cancel_pending`

**Inputs** self, sid.

**Declared result** dict.

**Explicit results** self.\_call(“POST”, formatted text /sessions/{sid}/cancel\_pending).

**Local steps**

- Return self.\_call(“POST”, formatted text /sessions/{sid}/cancel\_pending).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L177) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L926) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L902)

<a id="op-a1c23234133ce4"></a>
### Daemon Client.rewind

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_rewind`

**Inputs** self, sid, target\_seq.

**Declared result** dict.

**Explicit results** self.\_call(“POST”, formatted text /sessions/{sid}/rewind, json = mapping(“target\_seq” → target\_seq)).

**Local steps**

- Return self.\_call(“POST”, formatted text /sessions/{sid}/rewind, json = mapping(“target\_seq” → target\_seq)).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L192) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L941) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L917)

<a id="op-ee35e366d92c1f"></a>
### Daemon Client.compact

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_compact`

**Inputs** self, sid.

**Declared result** dict.

**Explicit results** self.\_call(“POST”, formatted text /sessions/{sid}/compact).

**Local steps**

- Return self.\_call(“POST”, formatted text /sessions/{sid}/compact).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L180) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L929) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L905)

<a id="op-b9f5bfdb565dbd"></a>
### Daemon Client.tool waiting

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_tool_waiting`

**Inputs** self, sid, token.

**Declared result** dict.

**Explicit results** self.\_call(“POST”, formatted text /sessions/{sid}/tool\_waiting, json = mapping(“token” → token)).

**Local steps**

- Return self.\_call(“POST”, formatted text /sessions/{sid}/tool\_waiting, json = mapping(“token” → token)).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L196) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L945) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L921)

<a id="op-ccd409d27fcfaa"></a>
### Daemon Client.tool result

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_tool_result`

**Inputs** self, sid, token, result.

**Declared result** dict.

**Explicit results** self.\_call(“POST”, formatted text /sessions/{sid}/tool\_result, json = mapping(“token” → token, expand result)).

**Local steps**

- Return self.\_call(“POST”, formatted text /sessions/{sid}/tool\_result, json = mapping(“token” → token, expand result)).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L195) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L944) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L920)

<a id="op-8a2dc279be186e"></a>
### Daemon Client.set model

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_set_model`

**Inputs** self, sid, model, api\_key (named only, default no value), api\_base (named only, default no value), model\_params (named only, default no value).

**Declared result** dict.

**Explicit results** self.\_call(“POST”, formatted text /sessions/{sid}/model, json = body).

**Local steps**

- Set body from mapping(“model” → model, “api\_key” → api\_key, “api\_base” → api\_base).
- If model\_params.
  - Set body at “model\_params” from model\_params.
- Return self.\_call(“POST”, formatted text /sessions/{sid}/model, json = body).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L194) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L943) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L919)

<a id="op-bfef249d8b5f84"></a>
### Daemon Client.patch config

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_patch_config`

**Inputs** self, sid, title (named only, default no value), approval\_mode (named only, default no value), tools (named only, default no value), client\_tools (named only, default no value), confirm\_tools (named only, default no value).

**Declared result** dict.

**Explicit results** self.\_call(“PATCH”, formatted text /sessions/{sid}/config, json = body).

**Local steps**

- Set body from mapping(“title” → title, “approval\_mode” → approval\_mode).
- If tools is distinct from no value.
  - Set body at “tools” from tools.
- If client\_tools is distinct from no value.
  - Set body at “client\_tools” from client\_tools.
- If confirm\_tools is distinct from no value.
  - Set body at “confirm\_tools” from confirm\_tools.
- Return self.\_call(“PATCH”, formatted text /sessions/{sid}/config, json = body).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L190) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L939) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L915)

<a id="op-a009f75f0a0772"></a>
### Daemon Client.entries

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_entries`

**Inputs** self, sid, since (named only, default 0), path (named only, default “active”).

**Declared result** dict.

**Explicit results** self.\_call(“GET”, formatted text /sessions/{sid}/entries, params = mapping(“since” → since, “path” → path)).

**Local steps**

- Return self.\_call(“GET”, formatted text /sessions/{sid}/entries, params = mapping(“since” → since, “path” → path)).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L184) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L933) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L909)

<a id="op-b359e056ff7b29"></a>
### Daemon Client.upload attachments

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_upload_attachments`

**Inputs** self, sid, files.

**Declared result** dict.

**Explicit results** self.\_call(“POST”, formatted text /sessions/{sid}/attachments, files = parts).

**Local steps**

- Set parts from list of tuple(“files”, tuple(name, data, mime)) for tuple(name, data, mime) drawn from files.
  - Draw tuple(name, data, mime) from files.
- Return self.\_call(“POST”, formatted text /sessions/{sid}/attachments, files = parts).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L197) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L946) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L922)

<a id="op-4b4eababec00ec"></a>
### Daemon Client.cleanup attachments

`operation_foundation_binding_foundation_flow_daemon_client_daemonclient_cleanup_attachments`

**Inputs** self, sid, attachment\_ids.

**Declared result** dict.

**Explicit results** self.\_call(“DELETE”, formatted text /sessions/{sid}/attachments, json = body).

**Local steps**

- Set body from mapping(“attachments” → attachment\_ids).
- Return self.\_call(“DELETE”, formatted text /sessions/{sid}/attachments, json = body).

**Methods declared on this owner** [call](operations-014.md#op-51ef0fbed834fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L178) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L927) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L903)
