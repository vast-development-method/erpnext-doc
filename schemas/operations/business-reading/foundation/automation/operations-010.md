# Workflow, automation and dispatch · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Bridge

<a id="op-4b9e4575f447e5"></a>
### Realtime Event.from raw

`operation_foundation_realtime_bridge_business_behavior_realtime_event_from_raw`

**Inputs** cls, raw.

**Wrappers, in declaration order** classmethod.

**Declared result** RealtimeEvent.

**Explicit results** cls(event = data at “event”, message = data.get(“message”), room = data.get(“room”), namespace = data.get(“namespace”)).

**Local steps**

- Set data from json.loads(raw).
- Return cls(event = data at “event”, message = data.get(“message”), room = data.get(“room”), namespace = data.get(“namespace”)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L5842) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1557) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L243)

<a id="op-6f1b3e83efa628"></a>
### Redis Bridge.initialize

`operation_foundation_realtime_bridge_business_behavior_cache_service_bridge_initialize`

**Inputs** self, sio, redis\_url.

**Local steps**

- Set self.sio from sio.
- Set self.redis\_url from redis\_url.
- Set self.\_task from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L6063) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1552) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L238)

<a id="op-521b0e0ed923c0"></a>
### Redis Bridge.start

`operation_foundation_realtime_bridge_business_behavior_cache_service_bridge_start`

**Inputs** self.

**Declared result** asyncio.Task.

**Explicit results** self.\_task.

**Local steps**

- Set self.\_task from asyncio.create\_task(self.\_run()).
- Return self.\_task.

**Methods declared on this owner** [run](operations-010.md#op-dfef32025c175d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L6167) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1555) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L241)

<a id="op-d7622320d6f49e"></a>
### Redis Bridge.stop

`operation_foundation_realtime_bridge_business_behavior_cache_service_bridge_stop`

**Inputs** self.

The declaration is asynchronous.

**Declared result** no value.

**State and service calls** call cancel on self.\_task.

**Explicit results** no value.

**Local steps**

- If not self.\_task.
  - Return no value.
- Evaluate self.\_task.cancel().
- Within suppress(asyncio.CancelledError).
  - Evaluate await self.\_task.
- Set self.\_task from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L6258) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1556) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L242)

<a id="op-dfef32025c175d"></a>
### Redis Bridge.run

`operation_foundation_realtime_bridge_business_behavior_cache_service_bridge_run`

**Inputs** self.

The declaration is asynchronous.

**Declared result** no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- While true.
  - Attempt the following.
    - Evaluate await self.\_listen().
  - On failure (asyncio.CancelledError).
    - Propagate the active failure.
  - On failure (RedisError) bound to e.
    - Evaluate logger.warning(“Redis bridge connection lost (%s); reconnecting in %ss”, e, RECONNECT\_DELAY).
  - On failure (Exception).
    - Evaluate logger.exception(“Redis bridge crashed; reconnecting in %ss”, RECONNECT\_DELAY).
  - Evaluate await asyncio.sleep(RECONNECT\_DELAY).

If control reaches the end, it returns no value.

**Methods declared on this owner** [listen](operations-010.md#op-d897d1a6fa46e1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L6398) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1554) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L240)

<a id="op-d897d1a6fa46e1"></a>
### Redis Bridge.listen

`operation_foundation_realtime_bridge_business_behavior_cache_service_bridge_listen`

**Inputs** self.

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Set client from redis.asyncio.from\_url(self.redis\_url).
- Attempt the following.
  - Set pubsub from client.pubsub(ignore\_subscribe\_messages = true).
  - Evaluate await pubsub.subscribe(EVENTS\_CHANNEL).
  - Evaluate logger.info(“Redis bridge subscribed to %r on %s”, EVENTS\_CHANNEL, self.redis\_url).
  - Asynchronously iterate message in pubsub.listen().
    - If message.get(“type”) equals “message”.
      - Evaluate await self.\_handle(message.get(“data”)).
- On exit, including pending return or failure.
  - Within suppress(Exception).
    - Evaluate await client.aclose().

If control reaches the end, it returns no value.

**Methods declared on this owner** [handle](operations-010.md#op-e5bcb1a70f49d5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L6602) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1553) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L239)

<a id="op-e5bcb1a70f49d5"></a>
### Redis Bridge.handle

`operation_foundation_realtime_bridge_business_behavior_cache_service_bridge_handle`

**Inputs** self, raw.

The declaration is asynchronous.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Attempt the following.
  - Set evt from RealtimeEvent.from\_raw(raw).
- On failure (tuple(ValueError, TypeError, KeyError)) bound to e.
  - Evaluate logger.warning(“Redis bridge skipping malformed message (%s): %r”, e, raw).
  - Return no value.
- If evt.room.
  - If not evt.namespace.
    - Evaluate logger.warning(“Redis bridge skipping room message with no namespace: %r”, raw).
    - Return no value.
  - Evaluate await self.sio.emit(evt.event, evt.message, room = evt.room, namespace = (“/” + evt.namespace)).
- Otherwise.
  - For each ns in list(self.sio.manager.rooms.keys()).
    - Evaluate await self.sio.emit(evt.event, evt.message, namespace = ns).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L6948) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1551) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L237)

## Service · Builtins

<a id="op-360c25e9d4c61d"></a>
### Builtin name

`operation_foundation_binding_foundation_flow_tools_builtins_builtin_name`

**Inputs** slug.

**Declared result** str.

**Explicit results** formatted text Platform/{slug}.

**Local steps**

- Return formatted text Platform/{slug}.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L136) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1377) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1353)

<a id="op-447db8b4409545"></a>
### Tool call name

`operation_foundation_binding_foundation_flow_tools_builtins_tool_call_name`

**Inputs** name.

**Declared result** str.

**Explicit results** name.removeprefix(“Platform/”).replace(“/”, “\_\_”).

**Local steps**

- Return name.removeprefix(“Platform/”).replace(“/”, “\_\_”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L189) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1430) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1406)

<a id="op-009c8aa39108e3"></a>
### Server only tool

`operation_foundation_binding_foundation_flow_tools_builtins_server_only_tool`

**Inputs** no declared parameters.

**Declared result** no value.

**Explicit failure paths** RuntimeError(“This tool runs on the Flow server”).

**Local steps**

- Raise RuntimeError(“This tool runs on the Flow server”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L184) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1425) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1401)

<a id="op-c6416c0f729d30"></a>
### Read

`operation_foundation_binding_foundation_flow_tools_builtins_read`

**Inputs** path, offset = no value, limit = no value, ctx (named only).

**Wrappers, in declaration order** tool.

**Declared result** str.

**Local steps**

- Evaluate \_server\_only\_tool().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L166) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1407) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1383)

<a id="op-04cb7cf359e34e"></a>
### Grep

`operation_foundation_binding_foundation_flow_tools_builtins_grep`

**Inputs** pattern, path = “.”, include = no value, ctx (named only).

**Wrappers, in declaration order** tool.

**Declared result** str.

**Local steps**

- Evaluate \_server\_only\_tool().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L155) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1396) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1372)

<a id="op-a4658c4bd7093f"></a>
### Subagent

`operation_foundation_binding_foundation_flow_tools_builtins_subagent`

**Inputs** task, description, agent = no value, subagent\_id = no value, ctx (named only).

**Wrappers, in declaration order** tool.

**Declared result** str.

**Local steps**

- Evaluate \_server\_only\_tool().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L185) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1426) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1402)

<a id="op-50b6f9812b898b"></a>
### Web fetch

`operation_foundation_binding_foundation_flow_tools_builtins_web_fetch`

**Inputs** url, ctx (named only).

**Wrappers, in declaration order** tool(requires\_confirmation = true).

**Declared result** str.

**Local steps**

- Evaluate \_server\_only\_tool().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L192) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1433) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1409)

<a id="op-85ac799df99d96"></a>
### Web search

`operation_foundation_binding_foundation_flow_tools_builtins_web_search`

**Inputs** query, ctx (named only).

**Wrappers, in declaration order** tool.

**Declared result** str.

**Local steps**

- Evaluate \_server\_only\_tool().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L193) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1434) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1410)

<a id="op-2a8c4b527fbcd1"></a>
### Summarize values

`operation_foundation_binding_foundation_flow_tools_builtins_summarize_values`

**Inputs** values.

**Declared result** str.

**Explicit results** json.dumps(display, indent = 2, default = str, ensure\_ascii = false).

**Local steps**

- Set display from mapping().
- For each tuple(k, v) in (values or mapping()).items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in values → mapping().
  - If (isinstance(v, str) and len(v) &gt; \_CONFIRM\_STR\_LIMIT).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(v, str) → len(v) &gt; \_CONFIRM\_STR\_LIMIT.
    - Set display at k from (v at slice no value to \_CONFIRM\_STR\_LIMIT + formatted text … ({len(v)} chars)).
  - Otherwise.
    - If (isinstance(v, list) and len(v) &gt; 6).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(v, list) → len(v) &gt; 6.
      - Set display at k from list(expanded v at slice no value to 6, formatted text … +{(len(v) − 6)} more).
    - Otherwise.
      - Set display at k from v.
- Return json.dumps(display, indent = 2, default = str, ensure\_ascii = false).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L187) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1428) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1404)

<a id="op-06cd5686048685"></a>
### Find doctypes

`operation_foundation_binding_foundation_flow_tools_builtins_find_doctypes`

**Inputs** search = no value, module = no value, limit = 40, ctx (named only).

**Wrappers, in declaration order** tool.

**Declared result** dict at tuple(str, Any).

**Record and data access** read “DocType” via get\_all.

**Explicit results** mapping(“total” → len(rows), “doctypes” → rows at slice no value to limit).

**Local steps**

- Set limit from min(max(int(limit), 1), MAX\_READ\_LIMIT).
- Set filters from mapping(“istable” → 0).
- If module.
  - Set filters at “module” from module.
- If search.
  - Set filters at “name” from list(“like”, formatted text %{search}%).
- Set rows from Platform.get\_all(“DocType”, filters = filters, fields = list(“name”, “module”), order\_by = “name”).
- If Platform.session.user differs from “Administrator”.
  - Set user from Platform.get\_user().
  - If not user.can\_read.
    - Evaluate user.build\_permissions().
  - Set readable from set(expanded user.can\_read, expanded user.all\_read).
  - Set rows from list of r for r drawn from rows where r at “name” belongs to readable.
    - Draw r from rows, keep a combination only if (r at “name” belongs to readable).
- Return mapping(“total” → len(rows), “doctypes” → rows at slice no value to limit).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L153) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1394) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1370)

<a id="op-01f7bb8d8a521e"></a>
### Describe

`operation_foundation_binding_foundation_flow_tools_builtins_describe`

**Inputs** doctype, name = no value, parent\_doctype = no value, ctx (named only).

**Wrappers, in declaration order** tool.

**Declared result** dict at tuple(str, Any).

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** result.

**Explicit failure paths** PermissionError(formatted text No permission to read {doctype}) · PermissionError(formatted text No permission to read {doctype} {name}).

**Local steps**

- Set parent\_doctype from \_parent\_doctype(doctype, parent\_doctype).
- If not Platform.has\_permission(doctype, “read”, parent\_doctype = parent\_doctype).
  - Raise PermissionError(formatted text No permission to read {doctype}).
- Set meta from Platform.get\_meta(doctype).
- Set fields from list of mapping(“fieldname” → f.fieldname, “label” → f.label, “type” → f.fieldtype, “options” → f.options, …) for f drawn from meta.fields where f.fieldtype does not belong to LAYOUT\_FIELDTYPES.
  - Draw f from meta.fields, keep a combination only if (f.fieldtype does not belong to LAYOUT\_FIELDTYPES).
- Set permissions from mapping of p → bool(Platform.has\_permission(doctype, p, parent\_doctype = parent\_doctype)) for p drawn from tuple(“read”, “write”, “create”, “delete”).
  - Draw p from tuple(“read”, “write”, “create”, “delete”).
- Set result from mapping(“doctype” → doctype, “fields” → fields, “permissions” → permissions).
- If name.
  - If not Platform.has\_permission(doctype, “read”, name).
    - Raise PermissionError(formatted text No permission to read {doctype} {name}).
  - Set doc from Platform.get\_doc(doctype, name).
  - Set result at “name” from doc.name.
  - Set result at “docstatus” from int(doc.docstatus).
  - Set result at “actions” from \_doc\_actions(doc, meta).
- Return result.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, parent\_doctype = parent\_doctype), Platform.has\_permission(doctype, p, parent\_doctype = parent\_doctype) and 1 further calls.

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L145) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1386) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1362)

<a id="op-2a50d5d8ca7a36"></a>
### Find apis

`operation_foundation_binding_foundation_flow_tools_builtins_find_apis`

**Inputs** query, ctx (named only).

**Wrappers, in declaration order** tool.

**Declared result** list at dict at tuple(str, Any).

**Explicit results** discovery.search(query) at “results”.

**Local steps**

- Return discovery.search(query) at “results”.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L152) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1393) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1369)

<a id="op-2293f4f759cc29"></a>
### Describe api

`operation_foundation_binding_foundation_flow_tools_builtins_describe_api`

**Inputs** method, doctype = no value, ctx (named only).

**Wrappers, in declaration order** tool.

**Declared result** dict at tuple(str, Any).

**Record and data access** read “Server Script” via get\_value.

**Explicit results** found.

**Local steps**

- If doctype.
  - Set found from discovery.doctype\_method(doctype, method).
  - If method equals “rename”.
    - Set found at “params” from list(mapping(“name” → “new\_name”, “required” → true, “type” → “str”)).
    - Set found at “docstring” from “Rename the document to ′new\_name′.”.
    - Evaluate found.pop(“source”, no value).
  - Return found.
- Set found from discovery.method(method).
- Set script from \_api\_server\_script(method).
- If (script and Platform.has\_permission(“Server Script”, “read”, doc = script)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in script → Platform.has\_permission(“Server Script”, “read”, doc = script).
  - Set found at “source” from Platform.db.get\_value(“Server Script”, script, “script”).
- Set found at “read\_only” from is\_read\_function(method).
- Return found.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Server Script”, “read”, doc = script).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L146) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1387) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1363)

<a id="op-96a8098e79ab84"></a>
### Read records

`operation_foundation_binding_foundation_flow_tools_builtins_read_records`

**Inputs** doctype, filters = no value, fields = no value, limit = 20, order\_by = no value, parent\_doctype = no value, ctx (named only).

**Wrappers, in declaration order** tool.

**Declared result** dict at tuple(str, Any).

**Record and data access** read doctype via get\_list.

**Explicit results** mapping(“total” → len(records), “records” → records) · mapping(“total” → total, “records” → records at slice no value to limit).

**Local steps**

- If Platform.get\_meta(doctype).issingle.
  - Set records from \_read\_single(doctype, filters, fields).
  - Return mapping(“total” → len(records), “records” → records).
- Set limit from min(max(int(limit), 1), MAX\_READ\_LIMIT).
- If parent\_doctype bound to \_parent\_doctype(doctype, parent\_doctype).
  - If isinstance(filters, list).
    - Set filters from list(expanded filters, list(“parenttype”, “=”, parent\_doctype)).
  - Otherwise.
    - Set filters from mapping(expand (filters or mapping()), “parenttype” → parent\_doctype).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set query from mapping(“filters” → filters, “fields” → (fields or list(“name”)), “parent\_doctype” → parent\_doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fields → list(“name”).
- Set records from Platform.get\_list(doctype, expanded names query, limit = (limit + 1), order\_by = (order\_by or DefaultOrderBy)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in order\_by → DefaultOrderBy.
- Set total from \_count(doctype, query) when len(records) &gt; limit, otherwise len(records).
  - Value choice on len(records) &gt; limit — true gives \_count(doctype, query), false gives len(records).
- Return mapping(“total” → total, “records” → records at slice no value to limit).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L167) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1408) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1384)

<a id="op-d9da748c148399"></a>
### Read single

`operation_foundation_binding_foundation_flow_tools_builtins_read_single`

**Inputs** doctype, filters, fields.

**Declared result** list at dict at tuple(str, Any).

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** list() · list(mapping of f → values.get(f) for f drawn from fields when fields, otherwise values).

**Local steps**

- Set doc from Platform.get\_doc(doctype).
- Evaluate doc.check\_permission(“read”).
- Evaluate doc.apply\_fieldlevel\_read\_permissions().
- Set values from doc.as\_dict(no\_nulls = true).
- If (filters and not Platform.utils.evaluate\_filters(values, filters)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → not Platform.utils.evaluate\_filters(values, filters).
  - Return list().
- Return list(mapping of f → values.get(f) for f drawn from fields when fields, otherwise values).
  - Value choice on fields — true gives mapping of f → values.get(f) for f drawn from fields, false gives values.
  - Draw f from fields.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L169) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1410) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1386)

<a id="op-9ee8e5001486ec"></a>
### Parent doctype

`operation_foundation_binding_foundation_flow_tools_builtins_parent_doctype`

**Inputs** doctype, given.

**Declared result** (str bitwise or no value).

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all.

**Explicit results** no value · given · parents at 0.

**Explicit failure paths** ValueError(formatted text {doctype} is a child table; pass parent\_doctype, one of: {(“, ”.join(parents) or “none”)}).

**Local steps**

- If not Platform.get\_meta(doctype).istable.
  - Return no value.
- Set table from mapping(“fieldtype” → list(“in”, Platform.model.table\_fields), “options” → doctype).
- Set parents from sorted((set(Platform.get\_all(“DocField”, filters = table, pluck = “parent”)) bitwise or set(Platform.get\_all(“Custom Field”, filters = table, pluck = “dt”)))).
- If given belongs to parents.
  - Return given.
- If (not given and len(parents) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not given → len(parents) equals 1.
  - Return parents at 0.
- Raise ValueError(formatted text {doctype} is a child table; pass parent\_doctype, one of: {(“, ”.join(parents) or “none”)}).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “, ”.join(parents) → “none”.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L164) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1405) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1381)

<a id="op-3eeebaa555fad3"></a>
### Count

`operation_foundation_binding_foundation_flow_tools_builtins_count`

**Inputs** doctype, query.

**Declared result** int.

**Record and data access** read doctype via get\_list.

**Explicit results** Platform.call(get\_controller(doctype).get\_count, args = Platform.\_dict(query), expanded names query) · nested operand in the contract(nested operand in the contract).select(Count(“\*”)).run() at 0 at 0.

**Local steps**

- If Platform.get\_meta(doctype).is\_virtual.
  - Return Platform.call(get\_controller(doctype).get\_count, args = Platform.\_dict(query), expanded names query).
- Set rows from Platform.get\_list(doctype, expanded names query, order\_by = no value, run = false).
- Return nested operand in the contract(nested operand in the contract).select(Count(“\*”)).run() at 0 at 0.

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L142) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1383) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1359)
