# Workflow, automation and dispatch · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Dispatch

<a id="op-f7099b6c8cbbbf"></a>
### Run in context

`operation_foundation_realtime_dispatch_business_behavior_run_in_context`

**Inputs** handler, socket, args.

**Declared result** object.

**Explicit results** handler.fn(socket, expanded args).

**Local steps**

- Within Platform\_context(socket.site, socket.user).
  - Return handler.fn(socket, expanded args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L115) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1564) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L250)

<a id="op-ad6f59d9119f77"></a>
### Call

`operation_foundation_realtime_dispatch_business_behavior_call`

**Inputs** handler, socket, args.

The declaration is asynchronous.

**Declared result** object.

**Explicit results** await handler.fn(socket, expanded args) · await asyncio.to\_thread(\_run\_in\_context, handler, sync\_socket, args) · result.

**Local steps**

- If is\_async\_callable(handler.fn).
  - Return await handler.fn(socket, expanded args).
- Set sync\_socket from SyncSocket(socket, asyncio.get\_running\_loop()).
- If handler.Platform\_context.
  - Return await asyncio.to\_thread(\_run\_in\_context, handler, sync\_socket, args).
- Set result from await asyncio.to\_thread(handler.fn, sync\_socket, expanded args).
- If inspect.isawaitable(result).
  - Set result from await result.
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L111) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1560) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L246)

<a id="op-09688431ba910b"></a>
### Run handlers

`operation_foundation_realtime_dispatch_business_behavior_run_handlers`

**Inputs** sio, event, namespace, sid, args.

The declaration is asynchronous.

**Declared result** object.

**Explicit results** no value · result.

**Local steps**

- Set handlers from realtime.handlers\_for(event).
- If not handlers.
  - Return no value.
- Attempt the following.
  - Set session from await sio.get\_session(sid, namespace = namespace).
- On failure (KeyError).
  - Return no value.
- Set socket from Socket(sio, sid, namespace, session).
- Set result from no value.
- For each handler in handlers.
  - If handler.app does not belong to socket.installed\_apps.
    - Continue with the next iteration or loop test.
  - If (socket.user equals “Guest” and not handler.allow\_guest).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in socket.user equals “Guest” → not handler.allow\_guest.
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set value from await \_call(handler, socket, args).
  - On failure (Exception).
    - Evaluate logger.exception(“handler error: event=%s app=%s”, event, handler.app).
    - Continue with the next iteration or loop test.
  - If value is distinct from no value.
    - Set result from value.
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L114) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1563) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L249)

<a id="op-54406e05076d7a"></a>
### Make dispatcher

`operation_foundation_realtime_dispatch_business_behavior_make_dispatcher`

**Inputs** sio, event.

**Declared result** Callable at tuple(ellipsis, Coroutine).

**Explicit results** dispatcher.

**Local steps**

- Bind local operation dispatcher for subsequent calls.
- Return dispatcher.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L112) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1561) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L247)

<a id="op-5bc812e41eaa23"></a>
### Make dispatcher.dispatcher

`operation_foundation_realtime_dispatch_business_behavior_make_dispatcher_dispatcher`

**Inputs** namespace, sid, remaining positional values args.

The declaration is asynchronous.

**Declared result** object.

**Explicit results** await \_run\_handlers(sio, event, namespace, sid, …).

**Local steps**

- Return await \_run\_handlers(sio, event, namespace, sid, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L113) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1562) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L248)

<a id="op-ac810e3c4cd260"></a>
### Wire

`operation_foundation_realtime_dispatch_business_behavior_wire`

**Inputs** sio, config.

**Declared result** no value.

**Local steps**

- Bind local operation connect for subsequent calls.
- Bind local operation disconnect for subsequent calls.
- Evaluate sio.on(“connect”, connect, namespace = “\*”).
- Evaluate sio.on(“disconnect”, disconnect, namespace = “\*”).
- For each event in list(realtime.events()).
  - If event belongs to RESERVED\_EVENTS.
    - Continue with the next iteration or loop test.
  - Evaluate sio.on(event, \_make\_dispatcher(sio, event), namespace = “\*”).
  - Evaluate logger.debug(“wired event %r (%d handler(s))”, event, len(realtime.handlers\_for(event))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L1411) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1565) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L251)

<a id="op-37315696501fc1"></a>
### Wire.connect

`operation_foundation_realtime_dispatch_business_behavior_wire_connect`

**Inputs** namespace, sid, environ, auth = no value.

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Set session from await authenticate(environ, namespace, config).
- Evaluate await sio.save\_session(sid, session, namespace = namespace).
- Evaluate await \_run\_handlers(sio, “connect”, namespace, sid, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L1992) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1566) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L252)

<a id="op-01ad9a5f766a09"></a>
### Wire.disconnect

`operation_foundation_realtime_dispatch_business_behavior_wire_disconnect`

**Inputs** namespace, sid, reason = no value.

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Evaluate await \_run\_handlers(sio, “disconnect”, namespace, sid, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L2194) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1567) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L253)

## Service · Drainer

<a id="op-8f426a9b8b74a9"></a>
### Drain

`operation_foundation_binding_foundation_automation_engine_drainer_drain`

**Inputs** batch\_size = DEFAULT\_BATCH\_SIZE, max\_batches = no value, executor = no value.

**Explicit results** no value.

**Local steps**

- If not settings.is\_enabled().
  - Return no value.
- Set executor from (executor or runner.execute\_automation).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in executor → runner.execute\_automation.
- Within read\_committed().
  - Evaluate promote\_due\_scheduled().
  - Set deadline from (time.monotonic() + drain\_time\_budget()).
  - Set batches from 0.
  - While true.
    - Set names from claim\_batch(batch\_size).
    - If not names.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Evaluate execute\_batch(executor, names).
    - Update batches using + 1.
    - If (max\_batches and batches ≥ max\_batches).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_batches → batches ≥ max\_batches.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - If time.monotonic() ≥ deadline.
      - Leave the innermost loop without its normal-exhaustion alternative.
- If \_has\_due\_pending().
  - Evaluate kick\_drainer().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L169) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L409) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L385)

<a id="op-98a0a8f36b8689"></a>
### Read committed

`operation_foundation_binding_foundation_automation_engine_drainer_read_committed`

**Inputs** no declared parameters.

**Wrappers, in declaration order** contextmanager.

**Explicit results** no value.

**Local steps**

- If Platform.db.db\_type does not belong to tuple(“mariadb”, “postgres”).
  - yield no value.
  - Return no value.
- Set previous from \_session\_isolation().
- Evaluate \_set\_session\_isolation(“READ COMMITTED”).
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Evaluate \_set\_session\_isolation(previous).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L182) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L422) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L398)

<a id="op-a70529b2543e0f"></a>
### Session isolation

`operation_foundation_binding_foundation_automation_engine_drainer_session_isolation`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L184) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L424) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L400)

<a id="op-7cabafae677ce4"></a>
### Set session isolation

`operation_foundation_binding_foundation_automation_engine_drainer_set_session_isolation`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** level.

**Explicit result forms** no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L185) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L425) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L401)

<a id="op-38b6d70c1c4b35"></a>
### Drain time budget

`operation_foundation_binding_foundation_automation_engine_drainer_drain_time_budget`

**Inputs** no declared parameters.

**Declared result** float.

**Explicit results** configured · ((get\_queues\_timeout().get(DRAIN\_QUEUE) or 300) × DRAIN\_TIME\_BUDGET).

**Local steps**

- Set configured from settings.get(“drain\_seconds”).
- If configured &gt; 0.
  - Return configured.
- Return ((get\_queues\_timeout().get(DRAIN\_QUEUE) or 300) × DRAIN\_TIME\_BUDGET).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_queues\_timeout().get(DRAIN\_QUEUE) → 300.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L171) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L411) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L387)

<a id="op-7481f208201d74"></a>
### Execute batch

`operation_foundation_binding_foundation_automation_engine_drainer_execute_batch`

**Inputs** executor, names.

**Local steps**

- Set size from max(1, cint(settings.get(“commit\_every”))).
- For each start in range(0, len(names), size).
  - Evaluate \_execute\_group(executor, names at slice start to (start + size)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L172) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L412) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L388)

<a id="op-03ceed392d5287"></a>
### Execute group

`operation_foundation_binding_foundation_automation_engine_drainer_execute_group`

**Inputs** executor, names.

**State and service calls** commit · rollback.

**Explicit results** no value.

**Local steps**

- For each tuple(position, name) in enumerate(names).
  - Evaluate \_execute\_in\_savepoint(executor, name, position).
- Attempt the following.
  - Evaluate Platform.db.commit().
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate Platform.log\_error(title = “Automation batch commit failed”, message = Platform.get\_traceback()).
  - Evaluate \_execute\_serially(executor, names).
  - Return no value.
- For each name in names.
  - Evaluate clear\_effects(name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L174) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L414) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L390)

<a id="op-136d947913617e"></a>
### Execute in savepoint

`operation_foundation_binding_foundation_automation_engine_drainer_execute_in_savepoint`

**Inputs** executor, name, position.

**State and service calls** savepoint savepoint · rollback.

**Explicit results** no value.

**Local steps**

- If effects\_delivered(name).
  - Evaluate \_fail\_delivered\_row(name).
  - Return no value.
- Set savepoint from formatted text auto\_row\_{position}.
- Evaluate Platform.db.savepoint(savepoint).
- Attempt the following.
  - Evaluate executor(name).
- On failure (Exception).
  - Evaluate Platform.db.rollback(save\_point = savepoint).
  - Evaluate Platform.log\_error(title = formatted text Automation run failed: {name}, message = Platform.get\_traceback()).
  - Evaluate \_settle\_escaped\_row(name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L175) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L415) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L391)

<a id="op-1ce621c965867d"></a>
### Settle escaped row

`operation_foundation_binding_foundation_automation_engine_drainer_settle_escaped_row`

**Inputs** name.

**Record and data access** read QUEUE via get\_value.

**State and service calls** request set\_value on QUEUE.

**Explicit results** \_fail\_delivered\_row(name).

**Local steps**

- If effects\_delivered(name).
  - Return \_fail\_delivered\_row(name).
- Set attempt from (cint(Platform.db.get\_value(QUEUE, name, “attempt”)) + 1).
- Set exhausted from attempt ≥ cint(settings.get(“max\_attempts”)).
- Evaluate Platform.db.set\_value(QUEUE, name, mapping(“attempt” → attempt, “status” → “Failed” when exhausted, otherwise “Pending”), update\_modified = false).
  - Value choice on exhausted — true gives “Failed”, false gives “Pending”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L186) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L426) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L402)

<a id="op-518340b3f9c195"></a>
### Fail delivered row

`operation_foundation_binding_foundation_automation_engine_drainer_fail_delivered_row`

**Inputs** name.

**State and service calls** request set\_value on QUEUE.

**Local steps**

- Evaluate Platform.db.set\_value(QUEUE, name, “status”, “Failed”, update\_modified = false).
- Evaluate Platform.log\_error(title = formatted text Automation run not retried: {name}, message = “The run had already sent something outside the database when it failed, so it was failed rather than queued again.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L177) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L417) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L393)

<a id="op-3834e5e9070fd0"></a>
### Execute serially

`operation_foundation_binding_foundation_automation_engine_drainer_execute_serially`

**Inputs** executor, names.

**Local steps**

- For each name in names.
  - Evaluate execute\_claimed(executor, name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L176) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L416) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L392)

<a id="op-bbbf80a4b1e4aa"></a>
### Execute claimed

`operation_foundation_binding_foundation_automation_engine_drainer_execute_claimed`

**Inputs** executor, name.

**State and service calls** commit · rollback.

**Explicit results** no value.

**Local steps**

- If effects\_delivered(name).
  - Evaluate \_fail\_delivered\_row(name).
  - Evaluate Platform.db.commit().
  - Evaluate clear\_effects(name).
  - Return no value.
- Attempt the following.
  - Evaluate executor(name).
  - Evaluate Platform.db.commit().
  - Evaluate clear\_effects(name).
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate Platform.log\_error(title = formatted text Automation run failed: {name}, message = Platform.get\_traceback()).
  - Evaluate \_settle\_escaped\_row(name).
  - Evaluate Platform.db.commit().
  - Evaluate clear\_effects(name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L173) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L413) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L389)

<a id="op-a747bc4dab7689"></a>
### Promote due scheduled

`operation_foundation_binding_foundation_automation_engine_drainer_promote_due_scheduled`

**Inputs** no declared parameters.

**Local steps**

- Set queue from Platform.qb.DocType(QUEUE).
- Evaluate nested operand in the contract(nested operand in the contract).where(nested operand in the contract.notnull()).where(queue.run\_after ≤ now()).run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L180) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L420) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L396)

<a id="op-5e7314ef9112fc"></a>
### Claim batch

`operation_foundation_binding_foundation_automation_engine_drainer_claim_batch`

**Inputs** batch\_size = DEFAULT\_BATCH\_SIZE.

**Declared result** list at str.

**State and service calls** execute a supplied database query · commit.

**Explicit results** list() · names.

**Local steps**

- Set rows from Platform.db.sql(formatted text   SELECT name FROM ′tab{QUEUE}′  WHERE status IN %(waiting)s AND (run\_after IS NULL OR run\_after &lt;= %(now)s)  ORDER BY triggered\_at  LIMIT %(limit, mapping(“now” → now(), ….
- If not rows.
  - Return list().
- Set names from list of row.name for row drawn from rows.
  - Draw row from rows.
- Set queue from Platform.qb.DocType(QUEUE).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(queue.modified, now()).where(queue.name.isin(names)).run().
- Evaluate Platform.db.commit().
- Return names.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L168) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L408) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L384)

<a id="op-a4e64283867691"></a>
### Lock clause

`operation_foundation_binding_foundation_automation_engine_drainer_lock_clause`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** “FOR UPDATE SKIP LOCKED” when supports\_skip\_locked(), otherwise “FOR UPDATE”.

**Local steps**

- Return “FOR UPDATE SKIP LOCKED” when supports\_skip\_locked(), otherwise “FOR UPDATE”.
  - Value choice on supports\_skip\_locked() — true gives “FOR UPDATE SKIP LOCKED”, false gives “FOR UPDATE”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L179) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L419) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L395)

<a id="op-118242e0c61c20"></a>
### Supports skip locked

`operation_foundation_binding_foundation_automation_engine_drainer_supports_skip_locked`

**Inputs** no declared parameters.

**Declared result** bool.

**State and service calls** execute a supplied database query.

**Explicit results** true · tuple(generator of int(part) for part drawn from re.findall(“\\d+”, version) at slice no value to 3) ≥ tuple(10, 6).

**Local steps**

- If Platform.db.db\_type differs from “mariadb”.
  - Return true.
- Set version from Platform.db.sql(“SELECT VERSION()”) at 0 at 0.
- Return tuple(generator of int(part) for part drawn from re.findall(“\\d+”, version) at slice no value to 3) ≥ tuple(10, 6).
  - Draw part from re.findall(“\\d+”, version) at slice no value to 3.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L187) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L427) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L403)
