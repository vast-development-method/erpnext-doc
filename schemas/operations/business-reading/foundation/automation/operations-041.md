# Workflow, automation and dispatch · operations 41

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Runner

<a id="op-3cb45c63aded6a"></a>
### Error summary

`operation_foundation_binding_foundation_automation_engine_runner_error_summary`

**Inputs** status, steps.

**Declared result** (str bitwise or no value).

**Explicit results** no value · message.splitlines() at 0 at slice no value to 140 · detail.splitlines() at negative 1 at slice no value to 140 when detail, otherwise “Failed”.

**Local steps**

- If status does not belong to tuple(“Failed”, “Partially Failed”).
  - Return no value.
- Set failed from next(generator of step for step drawn from steps where step at “status” equals “Failed”, no value).
  - Draw step from steps, keep a combination only if (step at “status” equals “Failed”).
- Set message from (failed or mapping()).get(“message”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in failed → mapping().
- If message.
  - Return message.splitlines() at 0 at slice no value to 140.
- Set detail from \_first\_error\_detail(steps).
- Return detail.splitlines() at negative 1 at slice no value to 140 when detail, otherwise “Failed”.
  - Value choice on detail — true gives detail.splitlines() at negative 1 at slice no value to 140, false gives “Failed”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L12) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L494) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L470)

<a id="op-0f8410edae303a"></a>
### First error detail

`operation_foundation_binding_foundation_automation_engine_runner_first_error_detail`

**Inputs** steps.

**Declared result** (str bitwise or no value).

**Explicit results** (step at “detail” or “Failed”) · “Failed”.

**Local steps**

- For each step in steps.
  - If step at “status” equals “Failed”.
    - Return (step at “detail” or “Failed”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in step at “detail” → “Failed”.
- Return “Failed”.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L21) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L503) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L479)

<a id="op-77819126fa84eb"></a>
### Failure key

`operation_foundation_binding_foundation_automation_engine_runner_failure_key`

**Inputs** rule\_name.

**Declared result** str.

**Explicit results** formatted text automation\_failures::{Platform.local.site}::{rule\_name}.

**Local steps**

- Return formatted text automation\_failures::{Platform.local.site}::{rule\_name}.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L19) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L501) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L477)

<a id="op-a733b3e05a1874"></a>
### Record failure

`operation_foundation_binding_foundation_automation_engine_runner_record_failure`

**Inputs** rule.

**Local steps**

- Set threshold from settings.get(“failure\_threshold”).
- If Platform.cache.incr(\_failure\_key(rule.name)) ≥ threshold.
  - Evaluate \_trip\_breaker(rule, threshold).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L27) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L509) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L485)

<a id="op-bb2711c9ee7f82"></a>
### Reset failures

`operation_foundation_binding_foundation_automation_engine_runner_reset_failures`

**Inputs** rule.

**Local steps**

- Evaluate Platform.cache.delete(\_failure\_key(rule.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L28) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L510) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L486)

<a id="op-704278f12172bf"></a>
### Trip breaker

`operation_foundation_binding_foundation_automation_engine_runner_trip_breaker`

**Inputs** rule, threshold.

**State and service calls** request set\_value on “Automation Flow” · request set\_value on QUEUE.

**Local steps**

- Set reason from translated “Auto-disabled after {0} consecutive failures”.format(threshold).
- Evaluate Platform.db.set\_value(“Automation Flow”, rule.name, mapping(“enabled” → 0, “disabled\_reason” → reason), update\_modified = false).
- Evaluate Platform.db.set\_value(QUEUE, mapping(“automation” → rule.name, “status” → tuple(“in”, WAITING\_STATES)), “status”, “Skipped”, update\_modified = false).
- Evaluate clear\_automation\_cache(rule.document\_type).
- Evaluate Platform.cache.delete(\_failure\_key(rule.name)).
- Evaluate \_notify\_owner(rule, reason).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L51) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L533) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L509)

<a id="op-155008a76f0f94"></a>
### Notify owner

`operation_foundation_binding_foundation_automation_engine_runner_notify_owner`

**Inputs** rule, reason.

**Record and data access** read “Automation Flow” via get\_value · resolve a document from mapping(“doctype” → “Notification Log”, “for\_user” → owner, “type” → “Alert”, “subject” → translated “Automation Flow {0} was auto-disabled”.format(rule.title), …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Notification Log”, “for\_user” → owner, “type” → “Alert”, “subject” → translated “Automation Flow {0} was auto-disabled”.format(rule.title), …)).

**Explicit results** no value.

**Local steps**

- Set owner from Platform.db.get\_value(“Automation Flow”, rule.name, “owner”).
- If not owner.
  - Return no value.
- Evaluate Platform.get\_doc(mapping(“doctype” → “Notification Log”, “for\_user” → owner, “type” → “Alert”, “subject” → nested operand in the contract(nested operand in the contract).format(rule.title), …)).insert(igno ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L25) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L507) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L483)

<a id="op-f8390bd0c0e341"></a>
### Config.queue names

`operation_foundation_runner_business_behavior_configuration_queue_names`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** (list at str bitwise or no value).

**Explicit results** list of name.strip() for name drawn from self.queue.split(“,”) when self.queue, otherwise no value.

**Local steps**

- Return list of name.strip() for name drawn from self.queue.split(“,”) when self.queue, otherwise no value.
  - Value choice on self.queue — true gives list of name.strip() for name drawn from self.queue.split(“,”), false gives no value.
  - Draw name from self.queue.split(“,”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L2092) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1711) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L388)

<a id="op-48072fe76c8787"></a>
### Config.has restart limit

`operation_foundation_runner_business_behavior_configuration_has_restart_limit`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** bool.

**Explicit results** bool((self.restart\_after\_requests or self.restart\_after\_jobs or self.restart\_idle\_seconds)).

**Local steps**

- Return bool((self.restart\_after\_requests or self.restart\_after\_jobs or self.restart\_idle\_seconds)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.restart\_after\_requests → self.restart\_after\_jobs → self.restart\_idle\_seconds.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L2218) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1710) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L387)

<a id="op-341aceb3275f43"></a>
### Web Server.initialize

`operation_foundation_runner_business_behavior_web_server_initialize`

**Inputs** self, config, traffic.

**Local steps**

- Bind dependencies socket.
- Bind dependencies uvicorn.
- Set self.app from TrafficMiddleware.load(config, traffic).
- Set fd from systemd\_socket\_fd().
- Set self.sockets from list(socket.socket(fileno = os.dup(fd))) when fd is distinct from no value, otherwise no value.
  - Value choice on fd is distinct from no value — true gives list(socket.socket(fileno = os.dup(fd))), false gives no value.
- Set self.server from uvicorn.Server(uvicorn.Config(self.app, host = config.host, port = config.port, log\_config = no value, access\_log = false, …)).
- Set self.handle\_exit from self.server.handle\_exit.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.socket(fileno = os.dup(fd)).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L12) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1754) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L431)

<a id="op-90a136514c6822"></a>
### Web Server.serve

`operation_foundation_runner_business_behavior_web_server_serve`

**Inputs** self, on\_signal.

**Declared result** no value.

**Local steps**

- Set self.server.handle\_exit from on\_signal.
- Evaluate self.server.run(sockets = self.sockets).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L13) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1755) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L432)

<a id="op-145c0e53349bbd"></a>
### Web Server.stop

`operation_foundation_runner_business_behavior_web_server_stop`

**Inputs** self, sig, frame = no value.

**Declared result** no value.

**Local steps**

- Evaluate self.handle\_exit(sig, frame).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L2626) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1756) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L433)

<a id="op-056eb7f03ed637"></a>
### Web Server.close realtime

`operation_foundation_runner_business_behavior_web_server_close_realtime`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.app.close\_realtime().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L2701) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1753) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L430)

<a id="op-ad14c2060b8253"></a>
### Traffic Middleware.initialize

`operation_foundation_runner_business_behavior_traffic_middleware_initialize`

**Inputs** self, app, traffic.

**Local steps**

- Set self.app from app.
- Set self.traffic from traffic.
- Set self.loop from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L2756) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1749) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L426)

<a id="op-dc46443ca9063c"></a>
### Traffic Middleware.load

`operation_foundation_runner_business_behavior_traffic_middleware_load`

**Inputs** cls, config, traffic.

**Wrappers, in declaration order** classmethod.

**Declared result** TrafficMiddleware.

**Explicit results** cls(application, traffic).

**Local steps**

- If config.dev.
  - Set os.environ at “Platform\_SERVE\_ASSETS” from “1”.
- If config.web\_threads.
  - Set os.environ at “Platform\_WEB\_THREADS” from str(config.web\_threads).
- Evaluate Platform.init(site = empty text).
- Bind dependencies application.
- Return cls(application, traffic).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L2857) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1750) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L427)

<a id="op-c51bcabe4dfc46"></a>
### Traffic Middleware.invoke

`operation_foundation_runner_business_behavior_traffic_middleware_call`

**Inputs** self, scope, receive, send.

The declaration is asynchronous.

**Local steps**

- If scope at “type” equals “lifespan”.
  - Set self.loop from asyncio.get\_running\_loop().
  - Evaluate await self.app(scope, receive, send).
- Otherwise.
  - If (scope at “type” equals “websocket” or scope at “path”.startswith(SOCKETIO\_PATH)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in scope at “type” equals “websocket” → scope at “path”.startswith(SOCKETIO\_PATH).
    - Evaluate self.traffic.count(“realtime”).
    - Evaluate await self.app(scope, receive, send).
  - Otherwise.
    - If scope at “path” belongs to HEALTH\_CHECK\_PATHS.
      - Evaluate await self.app(scope, receive, send).
    - Otherwise.
      - Evaluate await self.serve\_web(scope, receive, send).

If control reaches the end, it returns no value.

**Methods declared on this owner** [serve web](operations-041.md#op-db144b93c17de7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L3076) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1746) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L423)

<a id="op-db144b93c17de7"></a>
### Traffic Middleware.serve web

`operation_foundation_runner_business_behavior_traffic_middleware_serve_web`

**Inputs** self, scope, receive, send.

The declaration is asynchronous.

**Local steps**

- Set recorder from StatusRecorder(send).
- Within self.traffic.busy().
  - Attempt the following.
    - Evaluate await self.app(scope, receive, recorder).
  - On exit, including pending return or failure.
    - Evaluate self.traffic.count\_web(recorder.status).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L3469) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1751) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L428)

<a id="op-892785f64e9852"></a>
### Traffic Middleware.close realtime

`operation_foundation_runner_business_behavior_traffic_middleware_close_realtime`

**Inputs** self.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set sio from getattr(self.app, “engineio\_server”, no value).
- If (sio is identical to no value or self.loop is identical to no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sio is identical to no value → self.loop is identical to no value.
  - Return no value.
- Evaluate asyncio.run\_coroutine\_threadsafe(self.\_close\_realtime(sio), self.loop).

If control reaches the end, it returns no value.

**Methods declared on this owner** [close realtime](operations-041.md#op-775c5f76b24776).

**Values supplied outside this operation** selected callable from getattr(self.app, “engineio\_server”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L3655) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1747) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L424)

<a id="op-775c5f76b24776"></a>
### Traffic Middleware.close realtime

`operation_foundation_runner_business_behavior_traffic_middleware_close_realtime_2`

**Inputs** self, sio.

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Bind dependencies packet.
- Set open\_sockets from list of s for s drawn from list(sio.eio.sockets.values()) where not (s.closed or s.closing).
  - Draw s from list(sio.eio.sockets.values()), keep a combination only if (not (s.closed or s.closing)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in s.closed → s.closing.
- Evaluate logger.info(“realtime: disconnect %d client(s)”, len(open\_sockets)).
- For each socket in open\_sockets.
  - Evaluate await socket.send(packet.Packet(packet.NOOP)).
  - Evaluate await socket.close(wait = false, abort = true).
- Evaluate await sio.shutdown().

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.send(packet.Packet(packet.NOOP)), socket.close(wait = false, abort = true).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L3826) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1748) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L425)

<a id="op-09366997b4443c"></a>
### Status Recorder.initialize

`operation_foundation_runner_business_behavior_status_recorder_initialize`

**Inputs** self, send.

**Local steps**

- Set self.send from send.
- Set self.status from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L4124) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1733) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L410)

<a id="op-a9aa838be1406c"></a>
### Status Recorder.invoke

`operation_foundation_runner_business_behavior_status_recorder_call`

**Inputs** self, message.

The declaration is asynchronous.

**Local steps**

- If message at “type” equals “http.response.start”.
  - Set self.status from message at “status”.
- Evaluate await self.send(message).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L4195) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1732) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L409)

<a id="op-4b2957e2a190f2"></a>
### Traffic.initialize

`operation_foundation_runner_business_behavior_traffic_initialize`

**Inputs** self.

**Local steps**

- Set self.\_lock from threading.Lock().
- Set self.counts from mapping(“web” → 0, “realtime” → 0, “jobs” → 0).
- Set self.in\_flight from 0.
- Set self.last\_web\_request from time.monotonic().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L4322) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1745) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L422)

<a id="op-bb448e6f8fd83e"></a>
### Traffic.busy

`operation_foundation_runner_business_behavior_traffic_busy`

**Inputs** self.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Within self.\_lock.
  - Update self.in\_flight using + 1.
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Within self.\_lock.
    - Update self.in\_flight using − 1.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L4477) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1741) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L418)

<a id="op-ae3f169a4f9c2a"></a>
### Traffic.count

`operation_foundation_runner_business_behavior_traffic_count`

**Inputs** self, name.

**Declared result** no value.

**Local steps**

- Within self.\_lock.
  - Update self.counts at name using + 1.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L4605) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1742) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L419)
