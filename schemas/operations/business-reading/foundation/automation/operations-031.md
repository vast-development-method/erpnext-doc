# Workflow, automation and dispatch · operations 31

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Knowledge

<a id="op-8fb60bddf3ee84"></a>
### Knowledge.add text

`operation_foundation_binding_foundation_flow_knowledge_knowledge_knowledge_add_text`

**Inputs** self, content, title (named only, default no value).

**Declared result** str.

**Explicit results** self.\_ingest(source\_type = “Text”, title = (title or \_snippet(content)), content = content).

**Local steps**

- Return self.\_ingest(source\_type = “Text”, title = (title or \_snippet(content)), content = content).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → \_snippet(content).

**Methods declared on this owner** [ingest](operations-031.md#op-fc9b4141c1753b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L229) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1231) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1207)

<a id="op-7d22c05060b09c"></a>
### Knowledge.add file

`operation_foundation_binding_foundation_flow_knowledge_knowledge_knowledge_add_file`

**Inputs** self, file\_url, title (named only, default no value).

**Declared result** str.

**Explicit results** self.\_ingest(source\_type = “File”, title = (title or file\_url), file = file\_url).

**Local steps**

- Return self.\_ingest(source\_type = “File”, title = (title or file\_url), file = file\_url).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → file\_url.

**Methods declared on this owner** [ingest](operations-031.md#op-fc9b4141c1753b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L227) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1229) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1205)

<a id="op-ed7efec8cb1cb0"></a>
### Knowledge.add local file

`operation_foundation_binding_foundation_flow_knowledge_knowledge_knowledge_add_local_file`

**Inputs** self, path, title (named only, default no value).

**Declared result** str.

**Explicit results** self.add\_text(text, title = (title or os.path.basename(path))).

**Local steps**

- Bind dependencies os.
- Bind dependencies \_extract\_by\_extension.
- Set extension from nested operand in the contract.splitext(path) at 1.lower().lstrip(“.”).
- Within open(path, “rb”) bound as handle.
  - Set text from \_extract\_by\_extension(handle.read(), extension).
- Return self.add\_text(text, title = (title or os.path.basename(path))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → os.path.basename(path).

**Methods declared on this owner** [add text](operations-031.md#op-8fb60bddf3ee84).

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L228) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1230) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1206)

<a id="op-d7a2fcb0120e1d"></a>
### Knowledge.add url

`operation_foundation_binding_foundation_flow_knowledge_knowledge_knowledge_add_url`

**Inputs** self, url, title (named only, default no value).

**Declared result** str.

**Explicit results** self.\_ingest(source\_type = “URL”, title = (title or url), url = url).

**Local steps**

- Return self.\_ingest(source\_type = “URL”, title = (title or url), url = url).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → url.

**Methods declared on this owner** [ingest](operations-031.md#op-fc9b4141c1753b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L230) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1232) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1208)

<a id="op-cae2edd84f3118"></a>
### Knowledge.add doctype

`operation_foundation_binding_foundation_flow_knowledge_knowledge_knowledge_add_doctype`

**Inputs** self, reference\_doctype, content\_fields (named only), filters (named only, default no value), title (named only, default no value), auto\_sync (named only, default false).

**Declared result** str.

**Explicit results** self.\_ingest(source\_type = “DocType”, title = (title or reference\_doctype), reference\_doctype = reference\_doctype, content\_fields = “, ”.join(content\_fields), …).

**Local steps**

- Return self.\_ingest(source\_type = “DocType”, title = (title or reference\_doctype), reference\_doctype = reference\_doctype, content\_fields = “, ”.join(content\_fields), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → reference\_doctype.
  - Value choice on filters — true gives Platform.as\_json(filters), false gives no value.

**Methods declared on this owner** [ingest](operations-031.md#op-fc9b4141c1753b).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L226) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1228) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1204)

<a id="op-fc9b4141c1753b"></a>
### Knowledge.ingest

`operation_foundation_binding_foundation_flow_knowledge_knowledge_knowledge_ingest`

**Inputs** self, remaining named values fields.

**Declared result** str.

**Record and data access** resolve a document from mapping(“doctype” → SOURCE\_DOCTYPE, “knowledge\_base” → self.name, expand fields) via get\_doc.

**State and service calls** call insert on source.

**Explicit results** source.name.

**Local steps**

- Bind dependencies ingest\_source.
- Set source from Platform.get\_doc(mapping(“doctype” → SOURCE\_DOCTYPE, “knowledge\_base” → self.name, expand fields)).
- Set source.flags.skip\_auto\_ingest from true.
- Evaluate source.insert().
- Evaluate ingest\_source(source.name).
- Return source.name.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L231) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1233) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1209)

<a id="op-c70fa970a28c0d"></a>
### Ensure kb

`operation_foundation_binding_foundation_flow_knowledge_knowledge_ensure_kb`

**Inputs** title, description.

**Declared result** str.

**Record and data access** read KB\_DOCTYPE via exists · resolve a document from mapping(“doctype” → KB\_DOCTYPE, “title” → title, “description” → description) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → KB\_DOCTYPE, “title” → title, “description” → description)).

**Explicit results** title · Platform.get\_doc(mapping(“doctype” → KB\_DOCTYPE, “title” → title, “description” → description)).insert().name.

**Explicit failure paths** validation helper — translated “Knowledge base title is required.”.

**Local steps**

- Set title from (title or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → empty text.
- If not title.
  - Call the validation error handler Platform.throw(translated “Knowledge base title is required.”, title = translated “Invalid Knowledge Base”).
- If Platform.db.exists(KB\_DOCTYPE, title).
  - Return title.
- Return Platform.get\_doc(mapping(“doctype” → KB\_DOCTYPE, “title” → title, “description” → description)).insert().name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L225) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1227) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1203)

<a id="op-d2b9b7db6d56d0"></a>
### Snippet

`operation_foundation_binding_foundation_flow_knowledge_knowledge_snippet`

**Inputs** content.

**Declared result** str.

**Explicit results** (text at slice no value to \_TITLE\_LIMIT or “Text”).

**Local steps**

- Set text from one space.join((content or empty text).split()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in content → empty text.
- Return (text at slice no value to \_TITLE\_LIMIT or “Text”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in text at slice no value to \_TITLE\_LIMIT → “Text”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L233) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1235) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1211)

## Service · Launcher

<a id="op-bf5a3e44738702"></a>
### Add to page

`operation_foundation_binding_foundation_flow_launcher_add_to_page`

**Inputs** response, request.

**Explicit results** no value.

**Local steps**

- If (request.method differs from “GET” or response.status\_code differs from 200 or response.mimetype differs from “text/html” or request.path.split(“/”) at 1 does not belong to get\_app\_roots() or not Platform. ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in request.method differs from “GET” → response.status\_code differs from 200 → response.mimetype differs from “text/html” → request.path.split(“/”) at 1 does not belong to get\_app\_roots() → not Platform.has\_permission(“Flow Session”, “read”).
  - Return no value.
- Set tuple(head, body\_end, tail) from response.get\_data(as\_text = true).rpartition(“&lt;/body&gt;”).
- If body\_end.
  - Set assets from get\_assets\_json().
  - Set script from formatted text &lt;script src="{bundled\_asset(“flow\_launcher.bundle.js”)}" defer data-island="{assets.get(formatted text {ISLAND}.island.js, empty text)}" data-island-c.
  - Evaluate response.set\_data((((head + script) + body\_end) + tail)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Flow Session”, “read”).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L19) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1260) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1236)

<a id="op-38250c9e546a1b"></a>
### Get app roots

`operation_foundation_binding_foundation_flow_launcher_get_app_roots`

**Inputs** no declared parameters.

**Declared result** set at str.

**Explicit results** (((set of nested operand in the contract.split(“/”) at 0 for route drawn from routes bitwise or OWN\_ROOTS) − set(empty text)) − WITHOUT\_LAUNCHER).

**Local steps**

- Set routes from generator of (app.get(“route”) or empty text) for app drawn from Platform.get\_hooks(“add\_to\_apps\_screen”).
  - Draw app from Platform.get\_hooks(“add\_to\_apps\_screen”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app.get(“route”) → empty text.
- Return (((set of nested operand in the contract.split(“/”) at 0 for route drawn from routes bitwise or OWN\_ROOTS) − set(empty text)) − WITHOUT\_LAUNCHER).
  - Draw route from routes.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“add\_to\_apps\_screen”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L20) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1261) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1237)

## Service · Lifecycle

<a id="op-d80b585ef9ca60"></a>
### After install

`operation_foundation_binding_foundation_flow_daemon_lifecycle_after_install`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate provision\_site().
- Evaluate \_run\_or\_warn(ensure\_running).
- Evaluate \_run\_or\_warn(sync\_server\_tools).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L200) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L949) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L925)

<a id="op-eab6a3f518b72f"></a>
### After migrate

`operation_foundation_binding_foundation_flow_daemon_lifecycle_after_migrate`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate provision\_site().
- Evaluate \_run\_or\_warn(\_restart\_if\_needed).
- Evaluate \_run\_or\_warn(sync\_server\_tools).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L201) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L950) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L926)

<a id="op-691f5176815634"></a>
### Restart if needed

`operation_foundation_binding_foundation_flow_daemon_lifecycle_restart_if_needed`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- If not supervised().
  - Evaluate restart().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L221) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L970) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L946)

<a id="op-20d734ba6634d0"></a>
### Run or warn

`operation_foundation_binding_foundation_flow_daemon_lifecycle_run_or_warn`

**Inputs** step.

**Declared result** no value.

**Local steps**

- Attempt the following.
  - Evaluate step().
- On failure (tuple(OSError, RuntimeError)) bound to exc.
  - Evaluate click.secho(formatted text flow server not running: {exc}, fg = “yellow”).
  - Evaluate click.secho(“Run ′bench flow-server setup′ to finish setting it up.”, fg = “yellow”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L222) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L971) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L947)

<a id="op-c02fdf801d9666"></a>
### Provision site

`operation_foundation_binding_foundation_flow_daemon_lifecycle_provision_site`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- If not Platform.conf.flow\_server\_secret.
  - Evaluate update\_site\_config(“flow\_server\_secret”, Platform.generate\_hash(length = 48)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 48).

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L217) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L966) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L942)

<a id="op-71f8ae9893ff85"></a>
### Session root

`operation_foundation_binding_foundation_flow_daemon_lifecycle_session_root`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L225) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L974) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L950)

<a id="op-112313ee0bf04b"></a>
### Site extensions dir

`operation_foundation_binding_foundation_flow_daemon_lifecycle_site_extensions_dir`

**Inputs** no declared parameters.

**Declared result** Path.

**Explicit results** (site\_data\_dir() ÷ EXTENSIONS\_DIR).

**Local steps**

- Return (site\_data\_dir() ÷ EXTENSIONS\_DIR).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L227) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L976) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L952)

<a id="op-be2ff72adeec39"></a>
### Site data dir

`operation_foundation_binding_foundation_flow_daemon_lifecycle_site_data_dir`

**Inputs** no declared parameters.

**Declared result** Path.

**Explicit results** Path(Platform.get\_site\_path(“private”, “flow”)).resolve().

**Local steps**

- Return Path(Platform.get\_site\_path(“private”, “flow”)).resolve().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L226) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L975) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L951)

<a id="op-c34bf341eceef1"></a>
### App source prompt

`operation_foundation_binding_foundation_flow_daemon_lifecycle_app_source_prompt`

**Inputs** tools.

**Declared result** str.

**Explicit results** empty text · formatted text   APP SOURCE CODE Use {available} to inspect these installed apps: {paths}.

**Local steps**

- If not tools.
  - Return empty text.
- Set sources from app\_sources().
- If not sources.
  - Return empty text.
- Set paths from whitespace '\\n'.join(generator of formatted text - {app}: {root} for tuple(app, root) drawn from sources).
  - Draw tuple(app, root) from sources.
- Set available from “, ”.join(tools).
- Return formatted text   APP SOURCE CODE Use {available} to inspect these installed apps: {paths}.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L203) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L952) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L928)

<a id="op-e3540ae1dc32c2"></a>
### App sources

`operation_foundation_binding_foundation_flow_daemon_lifecycle_app_sources`

**Inputs** no declared parameters.

**Declared result** list at tuple at tuple(str, Path).

**Explicit results** list of tuple(app, Path(nested operand in the contract(nested operand in the contract)).resolve().parent) for app drawn from Platform.get\_installed\_apps(\_ensure\_on\_bench = true).

**Local steps**

- Return list of tuple(app, Path(nested operand in the contract(nested operand in the contract)).resolve().parent) for app drawn from Platform.get\_installed\_apps(\_ensure\_on\_bench = true).
  - Draw app from Platform.get\_installed\_apps(\_ensure\_on\_bench = true).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L204) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L953) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L929)

<a id="op-aa1c4992f3be91"></a>
### Callback url

`operation_foundation_binding_foundation_flow_daemon_lifecycle_callback_url`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** formatted text {\_callback\_base()}/api/method/Platform.flow.daemon.callback.callback.

**Local steps**

- Return formatted text {\_callback\_base()}/api/method/Platform.flow.daemon.callback.callback.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L206) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L955) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L931)

<a id="op-612cd3daac0ea5"></a>
### Callback base

`operation_foundation_binding_foundation_flow_daemon_lifecycle_callback_base`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** (conf.get(“flow\_server\_url”) or local).rstrip(“/”).

**Local steps**

- Set conf from Platform.get\_common\_site\_config().
- Set local from formatted command or address in the contract.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.get(“webserver\_port”) → 8000.
- Return (conf.get(“flow\_server\_url”) or local).rstrip(“/”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.get(“flow\_server\_url”) → local.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L205) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L954) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L930)

<a id="op-7f284ef7fba626"></a>
### Ensure running

`operation_foundation_binding_foundation_flow_daemon_lifecycle_ensure_running`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- If supervised().
  - Evaluate \_wait\_for\_supervisor().
  - Return false.
- Within filelock(LOCK, is\_global = true).
  - If healthy().
    - Return false.
  - Evaluate \_restart().
  - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L207) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L956) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L932)

<a id="op-1ca18f06ac6010"></a>
### Restart

`operation_foundation_binding_foundation_flow_daemon_lifecycle_restart`

**Inputs** no declared parameters.

**Declared result** no value.

**Explicit failure paths** RuntimeError(“the process manager restarts a supervised flow server”).

**Local steps**

- If supervised().
  - Raise RuntimeError(“the process manager restarts a supervised flow server”).
- Within filelock(LOCK, is\_global = true).
  - Evaluate \_restart().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L219) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L968) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L944)
