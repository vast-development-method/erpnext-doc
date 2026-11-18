# Shared value and file services · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Caching

<a id="op-40c843bb9daa1c"></a>
### Redis cache.wrapper

`operation_foundation_utils_caching_business_behavior_cache_service_cache_wrapper`

**Inputs** func = no value.

**Declared result** Callable.

**Explicit results** redis\_cache\_wrapper.

**Local steps**

- Set func\_key from formatted text {func.\_\_module\_\_}.{func.\_\_qualname\_\_}.
- Bind local operation clear\_cache for subsequent calls.
- Set func.clear\_cache from clear\_cache.
- Set func.ttl from ttl when not callable(ttl), otherwise 3600.
  - Value choice on not callable(ttl) — true gives ttl, false gives 3600.
- Bind local operation redis\_cache\_wrapper for subsequent calls.
- Return redis\_cache\_wrapper.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L73) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L940) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1565)

<a id="op-a659339d2ddad5"></a>
### Redis cache.wrapper.clear cache

`operation_foundation_utils_caching_business_behavior_cache_service_cache_wrapper_clear_cache`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.cache.delete\_keys(func\_key, user = user, shared = shared).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L1948) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L942) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1567)

<a id="op-4a6c4f60a278a7"></a>
### Redis cache.wrapper.redis cache wrapper

`operation_foundation_utils_caching_business_behavior_cache_service_cache_wrapper_cache_service_cache_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(func).

**Explicit results** cached\_val · Platform.cache.get\_value(func\_call\_key, user = user, shared = shared, use\_local\_cache = false) · val.

**Local steps**

- Set func\_call\_key from formatted text {func\_key}::{hash(\_\_generate\_request\_cache\_key(args, kwargs))}.
- Set cached\_val from Platform.cache.get\_value(func\_call\_key, user = user, shared = shared).
- If cached\_val is distinct from no value.
  - Return cached\_val.
- If Platform.cache.exists(func\_call\_key, user = user, shared = shared).
  - Return Platform.cache.get\_value(func\_call\_key, user = user, shared = shared, use\_local\_cache = false).
- Set val from func(expanded args, expanded names kwargs).
- Set ttl from getattr(func, “ttl”, 3600).
- Evaluate Platform.cache.set\_value(func\_call\_key, val, expires\_in\_sec = ttl, user = user, shared = shared).
- Return val.

**Values supplied outside this operation** selected callable from getattr(func, “ttl”, 3600).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L74) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L941) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1566)

<a id="op-b2ed2abaec315e"></a>
### Http cache

`operation_foundation_utils_caching_business_behavior_hypertext_transfer_protocol_cache`

**Inputs** public (named only, default false), max\_age (named only, default no value), stale\_while\_revalidate (named only, default no value).

**Declared result** Callable.

**Explicit results** outer.

**Local steps**

- Require isinstance(stale\_while\_revalidate, (int bitwise or NoneType)) or raise an assertion failure.
- Require isinstance(max\_age, (int bitwise or NoneType)) or raise an assertion failure.
- Set cache\_headers from list().
- If public.
  - Evaluate cache\_headers.append(“public”).
- Otherwise.
  - Evaluate cache\_headers.append(“private”).
- If max\_age is distinct from no value.
  - Evaluate cache\_headers.append(formatted text max-age={max\_age}).
- If stale\_while\_revalidate is distinct from no value.
  - Evaluate cache\_headers.append(formatted text stale-while-revalidate={stale\_while\_revalidate}).
- Set cache\_headers from “,”.join(cache\_headers).
- Bind local operation outer for subsequent calls.
- Return outer.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L2410) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L945) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1570)

<a id="op-0c0d115e97ff24"></a>
### Http cache.outer

`operation_foundation_utils_caching_business_behavior_hypertext_transfer_protocol_cache_outer`

**Inputs** func.

**Declared result** Callable.

**Explicit results** inner.

**Local steps**

- Set qualified\_name from formatted text {func.\_\_module\_\_}.{func.\_\_name\_\_}.
- Bind local operation inner for subsequent calls.
- Return inner.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L3030) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L946) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1571)

<a id="op-573ed5741c4091"></a>
### Http cache.outer.inner

`operation_foundation_utils_caching_business_behavior_hypertext_transfer_protocol_cache_outer_inner`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(func).

**Explicit results** ret.

**Local steps**

- Set ret from func(expanded args, expanded names kwargs).
- If (Platform.request and Platform.request.method equals “GET” and qualified\_name belongs to Platform.request.path).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.request → Platform.request.method equals “GET” → qualified\_name belongs to Platform.request.path.
  - Evaluate Platform.local.response\_headers.set(“Cache-Control”, cache\_headers).
- Return ret.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L3307) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L947) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1572)

<a id="op-90169b4bff174d"></a>
### Deprecated local cache

`operation_foundation_utils_caching_business_behavior_deprecated_local_cache`

**Inputs** namespace, key, generator, regenerate\_if\_none = false.

**Explicit results** Platform.local.cache at namespace at key.

**Local steps**

- If namespace does not belong to Platform.local.cache.
  - Set Platform.local.cache at namespace from mapping().
- If key does not belong to Platform.local.cache at namespace.
  - Set Platform.local.cache at namespace at key from generator().
- Otherwise.
  - If (Platform.local.cache at namespace at key is identical to no value and regenerate\_if\_none).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.local.cache at namespace at key is identical to no value → regenerate\_if\_none.
    - Set Platform.local.cache at namespace at key from generator().
- Return Platform.local.cache at namespace at key.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L3505) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L943) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1568)

## Service · Cdp connection

<a id="op-25c1e44f3c29bb"></a>
### CDPSocket Client.initialize

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_init`

**Inputs** self, websocket\_url.

**Local steps**

- Set self.websocket\_url from websocket\_url.
- Set self.connection from no value.
- Set self.message\_id from 0.
- Set self.pending\_messages from mapping().
- Set self.listeners from mapping().
- Set self.listen\_task from no value.
- Set self.loop from asyncio.new\_event\_loop().
- Evaluate asyncio.set\_event\_loop(self.loop).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L75) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L145) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L233)

<a id="op-936e14972ce59d"></a>
### CDPSocket Client.connect

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_connect`

**Inputs** self.

**Local steps**

- Evaluate self.loop.run\_until\_complete(self.\_connect()).
- Set self.listen\_task from self.loop.create\_task(self.\_listen()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [connect](operations-007.md#op-593059097466cf), [listen](operations-007.md#op-667c74fc5a5f6a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L69) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L139) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L227)

<a id="op-593059097466cf"></a>
### CDPSocket Client.connect

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_connect_d2d9e584a549`

**Inputs** self.

The declaration is asynchronous.

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - Set self.connection from await websockets.connect(self.websocket\_url, max\_size = no value).
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Failed to connect to WebSocket:”, message = formatted text {Platform.get\_traceback()}).
  - Propagate the active failure.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L70) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L140) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L228)

<a id="op-667c74fc5a5f6a"></a>
### CDPSocket Client.listen

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_listen`

**Inputs** self.

The declaration is asynchronous.

**Local steps**

- Attempt the following.
  - Asynchronously iterate message in self.connection.
    - Evaluate self.\_handle\_message(Platform.json.loads(message)).
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “WebSocket listening error:”, message = formatted text {Platform.get\_traceback()}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [handle message](operations-007.md#op-e90f2b5a6ce0dd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L76) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L146) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L234)

<a id="op-e90f2b5a6ce0dd"></a>
### CDPSocket Client.handle message

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_handle_message`

**Inputs** self, response.

**Local steps**

- Set method from response.get(“method”).
- Set params from response.get(“params”, mapping()).
- Set session\_id from response.get(“sessionId”).
- Set target\_id from params.get(“targetId”).
- Set frame\_id from params.get(“frameId”).
- Set message\_id from response.get(“id”).
- Set composite\_key from tuple(method, session\_id, target\_id, frame\_id).
- If (message\_id and message\_id belongs to self.pending\_messages).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in message\_id → message\_id belongs to self.pending\_messages.
  - Set future from self.pending\_messages.pop(message\_id).
  - If composite\_key belongs to self.pending\_messages.
    - Evaluate self.pending\_messages.pop(composite\_key).
  - Evaluate future.set\_result(response).
- Otherwise.
  - If method.
    - If composite\_key belongs to self.pending\_messages.
      - Set future from self.pending\_messages.pop(composite\_key).
      - Evaluate future.set\_result(response).
    - If method belongs to self.listeners.
      - For each tuple(callback, future, filters) in self.listeners at method.
        - If ((not session\_id or not filters at “sessionId” or filters at “sessionId” equals session\_id) and (not target\_id or not filters at “targetId” or filters at “targetId” equals target\_id) and (not frame\_id or n ….
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not session\_id or not filters at “sessionId” or filters at “sessionId” equals session\_id) → (not target\_id or not filters at “targetId” or filters at “targetId” equals target\_id) → (not frame\_id or not filters at “frameId” or filters at “frameId” equals frame\_id).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in not session\_id → not filters at “sessionId” → filters at “sessionId” equals session\_id.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in not target\_id → not filters at “targetId” → filters at “targetId” equals target\_id.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in not frame\_id → not filters at “frameId” → filters at “frameId” equals frame\_id.
          - Evaluate callback(future, response).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L74) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L144) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L232)

<a id="op-421dc074c06c9f"></a>
### CDPSocket Client.disconnect

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_disconnect`

**Inputs** self.

**State and service calls** call cancel on self.listen\_task · call cancel on task.

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - If self.listen\_task.
    - Evaluate self.listen\_task.cancel().
  - Evaluate self.loop.run\_until\_complete(self.\_disconnect()).
  - Set pending\_tasks from list of task for task drawn from asyncio.all\_tasks(self.loop) where not task.done().
    - Draw task from asyncio.all\_tasks(self.loop), keep a combination only if (not task.done()).
  - For each task in pending\_tasks.
    - Evaluate task.cancel().
    - Attempt the following.
      - Evaluate self.loop.run\_until\_complete(task).
    - On failure (asyncio.CancelledError).
      - Take no action here.
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Error while disconnecting:”, message = formatted text {Platform.get\_traceback()}).
  - Propagate the active failure.

If control reaches the end, it returns no value.

**Methods declared on this owner** [disconnect](operations-007.md#op-e57752783c5571).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L72) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L142) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L230)

<a id="op-e57752783c5571"></a>
### CDPSocket Client.disconnect

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_disconnect_9fcf39b1cbf7`

**Inputs** self.

The declaration is asynchronous.

**Local steps**

- Attempt the following.
  - If self.connection.
    - Evaluate await self.connection.close().
  - Set self.connection from no value.
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Error during WebSocket disconnection:”, message = formatted text {Platform.get\_traceback()}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L73) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L143) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L231)

<a id="op-3c9e4b1b4def3f"></a>
### CDPSocket Client.send

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_send`

**Inputs** self, method, params = no value, session\_id = no value, return\_future = false.

**Explicit results** asyncio.ensure\_future(self.\_send(method, params, session\_id, wait\_future\_fulfill = false), loop = self.loop) · self.\_destructure\_response(future.result()).

**Local steps**

- If return\_future.
  - Return asyncio.ensure\_future(self.\_send(method, params, session\_id, wait\_future\_fulfill = false), loop = self.loop).
- Set future from self.loop.run\_until\_complete(self.\_send(method, params, session\_id)).
- Return self.\_destructure\_response(future.result()).

**Methods declared on this owner** [send](operations-007.md#op-ec435136fc9e2d), [destructure response](operations-007.md#op-4f4b2bf7139000).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L78) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L148) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L236)

<a id="op-ec435136fc9e2d"></a>
### CDPSocket Client.send

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_send_ced3c8aa8601`

**Inputs** self, method, params = no value, session\_id = no value, wait\_future\_fulfill = true.

The declaration is asynchronous.

**Explicit results** future.

**Explicit failure paths** RuntimeError(“WebSocket connection is not open.”).

**Local steps**

- Update self.message\_id using + 1.
- Set message\_id from self.message\_id.
- Set message from mapping(“id” → message\_id, “method” → method, “params” → (params or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params → mapping().
- If session\_id.
  - Set message at “sessionId” from session\_id.
- If self.connection is identical to no value.
  - Raise RuntimeError(“WebSocket connection is not open.”).
- Set future from asyncio.Future().
- Set self.pending\_messages at message\_id from future.
- If any(list(method, session\_id, params.get(“targetId”) when params, otherwise no value, params.get(“frameId”) when params, otherwise no value)).
  - Value choice on params — true gives params.get(“targetId”), false gives no value.
  - Value choice on params — true gives params.get(“frameId”), false gives no value.
  - Set composite\_key from tuple(method, session\_id, params.get(“targetId”) when params, otherwise no value, params.get(“frameId”) when params, otherwise no value).
    - Value choice on params — true gives params.get(“targetId”), false gives no value.
    - Value choice on params — true gives params.get(“frameId”), false gives no value.
  - Set self.pending\_messages at composite\_key from future.
- Evaluate await self.connection.send(Platform.json.dumps(message)).
- If wait\_future\_fulfill.
  - Evaluate await future.
- Return future.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L79) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L149) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L237)

<a id="op-4f4b2bf7139000"></a>
### CDPSocket Client.destructure response

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_destructure_response`

**Inputs** self, response.

**Explicit results** tuple(result, error).

**Local steps**

- Set result from response.get(“result”, no value).
- Set error from response.get(“error”, no value).
- Return tuple(result, error).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L71) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L141) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L229)

<a id="op-3e8354f6080ea0"></a>
### CDPSocket Client.start listener

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_start_listener`

**Inputs** self, method, callback, session\_id = no value, target\_id = no value, frame\_id = no value.

**Explicit results** event.

**Local steps**

- If method does not belong to self.listeners.
  - Set self.listeners at method from list().
- Set future from self.loop.create\_future().
- Set event from tuple(callback, future, mapping(“sessionId” → session\_id, “targetId” → target\_id, “frameId” → frame\_id)).
- If event does not belong to self.listeners at method.
  - Evaluate self.listeners at method.append(event).
- Return event.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L80) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L150) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L238)

<a id="op-794aabd0f122ac"></a>
### CDPSocket Client.wait for event

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_wait_for_event`

**Inputs** self, event, timeout = 3.

**Local steps**

- If type(event) is identical to tuple.
  - Set event from event at 1.
- Attempt the following.
  - Evaluate self.loop.run\_until\_complete(asyncio.wait\_for(event, timeout)).
- On failure (TimeoutError).
  - Evaluate Platform.log\_error(title = “Timeout waiting for event”, message = formatted text {Platform.get\_traceback()}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L81) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L151) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L239)

<a id="op-fe397a76bbdc1d"></a>
### CDPSocket Client.remove listener

`operation_foundation_binding_foundation_utils_pdf_generator_cdp_connection_cdpsocketclient_remove_listener`

**Inputs** self, method, event.

**Local steps**

- Evaluate self.listeners at method.remove(event).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L77) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L147) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L235)

## Service · Change log

<a id="op-e21ae86cc3fd0e"></a>
### Get change log

`operation_foundation_utils_change_log_business_behavior_get_change_log`

**Inputs** user = no value.

**Record and data access** read “User” via get\_value.

**Explicit results** list() · change\_log.

**Local steps**

- If not user.
  - Set user from Platform.session.user.
- If not Platform.is\_setup\_complete().
  - Return list().
- Set last\_known\_versions from Platform.\_dict(json.loads((Platform.db.get\_value(“User”, user, “last\_known\_versions”) or “{}”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“User”, user, “last\_known\_versions”) → “{}”.
- Set current\_versions from get\_versions().
- If not last\_known\_versions.
  - Evaluate update\_last\_known\_versions().
  - Return list().
- Set change\_log from list().
- Bind local operation set\_in\_change\_log for subsequent calls.
- For each tuple(app, opts) in current\_versions.items().
  - If app differs from “Platform”.
    - Evaluate set\_in\_change\_log(app, opts, change\_log).
- If “Platform” belongs to current\_versions.
  - Evaluate set\_in\_change\_log(“Platform”, current\_versions at “Platform”, change\_log).
- Return change\_log.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L3822) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L959) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1584)

<a id="op-641a1bc3bd015e"></a>
### Get change log.set in change log

`operation_foundation_utils_change_log_business_behavior_get_change_log_set_in_change_log`

**Inputs** app, opts, change\_log.

**Local steps**

- Set from\_version from (last\_known\_versions.get(app, mapping()).get(“version”) or “0.0.1”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in last\_known\_versions.get(app, mapping()).get(“version”) → “0.0.1”.
- Set to\_version from opts at “version”.
- If from\_version differs from to\_version.
  - Set app\_change\_log from get\_change\_log\_for\_app(app, from\_version = from\_version, to\_version = to\_version).
  - If app\_change\_log.
    - Evaluate change\_log.append(mapping(“title” → opts at “title”, “description” → opts at “description”, “version” → to\_version, “change\_log” → app\_change\_log)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L4548) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L961) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1586)

<a id="op-414f8b5046898d"></a>
### Get change log for app

`operation_foundation_utils_change_log_business_behavior_get_change_log_for_application`

**Inputs** app, from\_version, to\_version.

**Explicit results** no value · list of list(cstr(d at 0), d at 1) for d drawn from app\_change\_log.

**Local steps**

- Set change\_log\_folder from os.path.join(Platform.get\_app\_path(app), “change\_log”).
- If not os.path.exists(change\_log\_folder).
  - Return no value.
- Set from\_version from Version(from\_version).
- Set to\_version from Version(to\_version).
- Set to\_version.prerelease from no value.
- Set major\_version\_folders from list of formatted text v{i} for i drawn from range(from\_version.major, (to\_version.major + 1)).
  - Draw i from range(from\_version.major, (to\_version.major + 1)).
- Set app\_change\_log from list().
- For each folder in os.listdir(change\_log\_folder).
  - If folder belongs to major\_version\_folders.
    - For each file in os.listdir(os.path.join(change\_log\_folder, folder)).
      - Set version from Version(nested operand in the contract.splitext(file) at 0 at slice 1 to no value.replace(“\_”, “.”)).
      - If from\_version &lt; version ≤ to\_version.
        - Compare adjacent operands in order, stopping at the first false comparison in from\_version &lt; version ≤ to\_version.
        - Set file\_path from os.path.join(change\_log\_folder, folder, file).
        - Set content from Platform.read\_file(file\_path).
        - Evaluate app\_change\_log.append(list(version, content)).
- Set app\_change\_log from sorted(app\_change\_log, key = deferred anonymous expression, reverse = true).
- Return list of list(cstr(d at 0), d at 1) for d drawn from app\_change\_log.
  - Draw d from app\_change\_log.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L4870) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L960) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1585)

<a id="op-cd7744ec94d019"></a>
### Update last known versions

`operation_foundation_utils_change_log_business_behavior_update_last_known_versions`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request set\_value on “User”.

**Local steps**

- Within suppress(Platform.QueryDeadlockError).
  - Evaluate Platform.db.set\_value(“User”, Platform.session.user, “last\_known\_versions”, json.dumps(get\_versions()), update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L5614) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L974) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1599)
