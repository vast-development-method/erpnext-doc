# Workflow, automation and dispatch · operations 46

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Schema relationships

<a id="op-c8ee8923bea88c"></a>
### Ignored

`operation_foundation_binding_foundation_automation_engine_schema_relationships_ignored`

**Inputs** no declared parameters.

**Wrappers, in declaration order** request\_cache.

**Declared result** set.

**Explicit results** (IGNORED\_DOCTYPES bitwise or set((Platform.get\_hooks(“automation\_relationship\_ignore”) or list()))).

**Local steps**

- Return (IGNORED\_DOCTYPES bitwise or set((Platform.get\_hooks(“automation\_relationship\_ignore”) or list()))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“automation\_relationship\_ignore”) → list().

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“automation\_relationship\_ignore”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L85) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L567) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L543)

<a id="op-6c9a6235b58e38"></a>
### Deduplicate

`operation_foundation_binding_foundation_automation_engine_schema_relationships_deduplicate`

**Inputs** definitions.

**Declared result** list at dict.

**Explicit results** kept.

**Local steps**

- Set tuple(seen, kept) from tuple(set(), list()).
- For each definition in definitions.
  - If definition at “name” belongs to seen.
    - Continue with the next iteration or loop test.
  - Evaluate seen.add(definition at “name”).
  - Evaluate kept.append(definition).
- Return kept.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L80) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L562) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L538)

<a id="op-60ebabbb432633"></a>
### Derived

`operation_foundation_binding_foundation_automation_engine_schema_relationships_derived`

**Inputs** source\_doctype, relationship.

**Declared result** dict.

**Explicit results** definition.

**Explicit failure paths** validation helper — translated “Unknown derived relationship: {0}”.format(relationship).

**Local steps**

- For each definition in derived\_definitions(source\_doctype).
  - If definition at “name” equals relationship.
    - Return definition.
- Call the validation error handler Platform.throw(translated “Unknown derived relationship: {0}”.format(relationship)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L81) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L563) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L539)

<a id="op-93525ef2d6bef0"></a>
### References

`operation_foundation_binding_foundation_automation_engine_schema_relationships_references`

**Inputs** doctype, names.

**Declared result** list at dict.

**Explicit results** list of mapping(“doctype” → doctype, “name” → name) for name drawn from names where (doctype and name).

**Local steps**

- Return list of mapping(“doctype” → doctype, “name” → name) for name drawn from names where (doctype and name).
  - Draw name from names, keep a combination only if ((doctype and name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → name.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L89) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L571) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L547)

## Service · Server

<a id="op-ae13f3e8feb720"></a>
### Tolerant Manager.connect

`operation_foundation_realtime_server_business_behavior_tolerant_manager_connect`

**Inputs** self, eio\_sid, namespace.

The declaration is asynchronous.

**Declared result** (str bitwise or no value).

**Explicit results** (await super().connect(eio\_sid, namespace) or self.sid\_from\_eio\_sid(eio\_sid, namespace)).

**Local steps**

- Return (await super().connect(eio\_sid, namespace) or self.sid\_from\_eio\_sid(eio\_sid, namespace)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in await super().connect(eio\_sid, namespace) → self.sid\_from\_eio\_sid(eio\_sid, namespace).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L6800) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1627) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L313)

<a id="op-cd1ceccceac90a"></a>
### Create sio

`operation_foundation_realtime_server_business_behavior_create_sio`

**Inputs** no declared parameters.

**Declared result** socketio.AsyncServer.

**Explicit results** socketio.AsyncServer(async\_mode = “asgi”, cors\_allowed\_origins = “\*”, cors\_credentials = true, namespaces = “\*”, …).

**Local steps**

- Return socketio.AsyncServer(async\_mode = “asgi”, cors\_allowed\_origins = “\*”, cors\_credentials = true, namespaces = “\*”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L6932) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1617) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L303)

<a id="op-41e7169523fd3b"></a>
### Load handlers

`operation_foundation_realtime_server_business_behavior_load_handlers`

**Inputs** sites\_path = no value.

**Declared result** no value.

**Local steps**

- Bind dependencies Platform.realtime.flow\_handlers.
- Bind dependencies Platform.realtime.handlers.
- Bind dependencies discover\_app\_handlers.
- Evaluate discover\_app\_handlers(sites\_path = sites\_path).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L4) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1618) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L304)

<a id="op-f5cbbabd6a5b14"></a>
### Realtime Server.initialize

`operation_foundation_realtime_server_business_behavior_realtime_server_initialize`

**Inputs** self, config = no value, other\_asgi\_app = no value.

**Local steps**

- Set self.config from (config or get\_config()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in config → get\_config().
- Set self.sio from create\_sio().
- Set self.bridge from RedisBridge(self.sio, self.config.redis\_queue).
- Set self.app from socketio.ASGIApp(self.sio, other\_asgi\_app = other\_asgi\_app, on\_startup = self.\_on\_startup, on\_shutdown = self.\_on\_shutdown).
- Evaluate load\_handlers(self.config.sites\_path).
- Evaluate wire(self.sio, self.config).
- Set self.\_server from uvicorn.Server(self.\_get\_uvicorn\_config()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get uvicorn config](operations-046.md#op-1a5423b69e99dd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L7137) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1621) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L307)

<a id="op-941dc84767e630"></a>
### Realtime Server.run

`operation_foundation_realtime_server_business_behavior_realtime_server_run`

**Inputs** self.

**Declared result** no value.

**Local steps**

- If self.config.uds.
  - If os.path.exists(self.config.uds).
    - Evaluate os.remove(self.config.uds).
  - Evaluate logger.info(“Realtime service listening on UDS: %s”, self.config.uds).
- Otherwise.
  - Evaluate logger.info(“Realtime service listening on: ws://0.0.0.0:%s”, self.config.port).
- Evaluate self.\_server.run().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L7492) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1624) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L310)

<a id="op-b3cb1f2d278b2d"></a>
### Realtime Server.stop

`operation_foundation_realtime_server_business_behavior_realtime_server_stop`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.\_server.should\_exit from true.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L7702) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1625) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L311)

<a id="op-5f1cd20c4f3294"></a>
### Realtime Server.on startup

`operation_foundation_realtime_server_business_behavior_realtime_server_on_startup`

**Inputs** self.

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- If self.config.worker\_threads.
  - Evaluate asyncio.get\_running\_loop().set\_default\_executor(ThreadPoolExecutor(max\_workers = self.config.worker\_threads, thread\_name\_prefix = “realtime-worker”)).
- Evaluate self.bridge.start().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L7753) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1623) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L309)

<a id="op-f33d405ae1870b"></a>
### Realtime Server.on shutdown

`operation_foundation_realtime_server_business_behavior_realtime_server_on_shutdown`

**Inputs** self.

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Evaluate await self.bridge.stop().
- Evaluate await close\_clients().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L7892) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1622) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L308)

<a id="op-1a5423b69e99dd"></a>
### Realtime Server.get uvicorn config

`operation_foundation_realtime_server_business_behavior_realtime_server_get_uvicorn_configuration`

**Inputs** self.

**Declared result** uvicorn.Config.

**Explicit results** uvicorn.Config(self.app, log\_config = no value, access\_log = false, expanded names binding).

**Local steps**

- If self.config.uds.
  - Set binding from mapping(“uds” → self.config.uds).
- Otherwise.
  - Set binding from mapping(“host” → “0.0.0.0”, “port” → self.config.port).
- Return uvicorn.Config(self.app, log\_config = no value, access\_log = false, expanded names binding).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1620) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L306)

<a id="op-d63443db9df2c8"></a>
### Serve

`operation_foundation_realtime_server_business_behavior_serve`

**Inputs** config = no value.

**Declared result** no value.

**Local steps**

- Set config from (config or get\_config()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in config → get\_config().
- If os.path.isdir(“sites”).
  - Evaluate os.chdir(“sites”).
- Evaluate RealtimeServer(config).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L195) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1626) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L312)

<a id="op-ecde6e214edc85"></a>
### Main

`operation_foundation_realtime_server_business_behavior_main`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate logging.basicConfig(level = logging.WARNING, format = “%(asctime)s %(levelname)s %(name)s %(message)s”).
- Evaluate serve().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L358) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1619) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L305)

## Service · Session

<a id="op-0f7b923f9c86d9"></a>
### New session

`operation_foundation_binding_foundation_flow_lib_session_new_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** agent, model, title, source, approval\_mode.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup, record lookup, transaction control.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L76) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1317) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1293)

<a id="op-db131cdd447c3a"></a>
### Load session

`operation_foundation_binding_foundation_flow_lib_session_load_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** name, agent, model.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup, record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L66) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1307) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1283)

<a id="op-61da89edc81cbe"></a>
### Warn existing sessions

`operation_foundation_binding_foundation_flow_lib_session_warn_existing_sessions`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** agents.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L79) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1320) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1296)

<a id="op-436aa80179e0b3"></a>
### Block rename in chats

`operation_foundation_binding_foundation_flow_lib_session_block_rename_in_chats`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** old, agents.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L57) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1298) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1274)

<a id="op-e9d19cf9d6b5c7"></a>
### Flow server

`operation_foundation_binding_foundation_flow_lib_session_flow_server`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Observed service boundaries** validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L63) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1304) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1280)

<a id="op-fc5f258b982ce8"></a>
### Log Recorder.initialize

`operation_foundation_binding_foundation_flow_lib_session_logrecorder_init`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, session.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L72) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1313) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1289)

<a id="op-506abb541b17f3"></a>
### Log Recorder.record

`operation_foundation_binding_foundation_flow_lib_session_logrecorder_record`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, rows.

**Observed service boundaries** record mutation request.

**Local structure** 10 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L73) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1314) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1290)

<a id="op-1f7ca12fb51b52"></a>
### Log Recorder.start run

`operation_foundation_binding_foundation_flow_lib_session_logrecorder_start_run`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, run\_id.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L75) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1316) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1292)

<a id="op-0533337388437d"></a>
### Log Recorder.find or create run

`operation_foundation_binding_foundation_flow_lib_session_logrecorder_find_or_create_run`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L71) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1312) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1288)
