# Integration and transport · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Api

<a id="op-a0bdebb30297b1"></a>
### Handle

`operation_foundation_application_interface_initialize_business_behavior_handle`

**Inputs** request.

**Record and data access** resolve a document from mapping(“doctype” → “API Request Log”, “path” → request.path, “user” → Platform.session.user, “method” → request.method) via get\_doc.

**Explicit results** data.

**Explicit failure paths** Platform.DoesNotExistError.

**Local steps**

- If Platform.get\_system\_settings(“log\_api\_requests”).
  - Set doc from Platform.get\_doc(mapping(“doctype” → “API Request Log”, “path” → request.path, “user” → Platform.session.user, “method” → request.method)).
  - Evaluate doc.deferred\_insert().
- Attempt the following.
  - Set tuple(endpoint, arguments) from API\_URL\_MAP.bind\_to\_environ(request.environ).match().
- On failure (NotFound).
  - Raise Platform.DoesNotExistError.
- Set data from endpoint(expanded names arguments).
- If isinstance(data, Response).
  - Return data.
- If data is distinct from no value.
  - Set Platform.response at “data” from data.
- Set data from build\_response(“json”).
- Within suppress(Exception).
  - Set method from (arguments.get(“method”) or Platform.form\_dict.get(“method”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in arguments.get(“method”) → Platform.form\_dict.get(“method”).
  - Set doctype from (arguments.get(“doctype”) or Platform.form\_dict.get(“doctype”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in arguments.get(“doctype”) → Platform.form\_dict.get(“doctype”).
  - If (method or doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in method → doctype.
    - Set app\_name from no value.
    - If doctype.
      - Set app\_name from get\_doctype\_app\_map().get(doctype).
    - Otherwise.
      - If (method and “.” belongs to method).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in method → “.” belongs to method.
        - Set app\_name from method.split(“.”, 1) at 0.
    - If app\_name.
      - Evaluate add\_data\_to\_monitor(app = app\_name).
      - Evaluate capture\_app\_heartbeat(app\_name).
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“log\_api\_requests”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L14) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L71) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L60)

<a id="op-f9fc471fc25f29"></a>
### Get api version

`operation_foundation_application_interface_initialize_business_behavior_get_application_programming_interface_version`

**Inputs** no declared parameters.

**Declared result** (ApiVersion bitwise or no value).

**Explicit results** no value · ApiVersion.V2 · ApiVersion.V1.

**Local steps**

- If not Platform.request.
  - Return no value.
- If Platform.request.path.startswith(formatted text /api/{ApiVersion.V2.value}).
  - Return ApiVersion.V2.
- Return ApiVersion.V1.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L4384) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L70) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L59)

## Service · App

<a id="op-ba521cb361eeb8"></a>
### Get after response callbacks

`operation_foundation_app_business_behavior_get_after_response_callbacks`

**Inputs** no declared parameters.

**Local steps**

- yield values from DEFAULT\_AFTER\_RESPONSE\_CALLBACKS.
- Set request from getattr(Platform.local, “request”, no value).
- If callback\_manager bound to getattr(request, “after\_response”, no value).
  - Set functions from callback\_manager.\_functions.
  - While functions.
    - yield functions.popleft().
- Otherwise.
  - Evaluate Platform.logger(“after\_response”).error(“No request or after\_response callback manager found”).

On ordinary fall-through the sequence ends.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “request”, no value), getattr(request, “after\_response”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0007.json#L3972) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L6) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L6)

<a id="op-54e72a8c6e5c6f"></a>
### Run after response callbacks

`operation_foundation_app_business_behavior_run_after_response_callbacks`

**Inputs** no declared parameters.

**Local steps**

- For each func in get\_after\_response\_callbacks().
  - Attempt the following.
    - Evaluate func().
  - On failure (Exception).
    - Evaluate Platform.logger(“after\_response”).error(formatted text Failed to run after response callback: {func}, exc\_info = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0007.json#L4164) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L14) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L13)

<a id="op-b22acec8f0632f"></a>
### After response wrapper

`operation_foundation_app_business_behavior_after_response_wrapper`

**Inputs** app.

**Explicit results** application.

**Local steps**

- Bind local operation application for subsequent calls.
- Return application.

[Applicable decision contract](../../../foundation-decision-contracts/part-0007.json#L4311) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L2)

<a id="op-c76edc5e42b2df"></a>
### After response wrapper.application

`operation_foundation_app_business_behavior_after_response_wrapper_application`

**Inputs** environ, start\_response.

**Wrappers, in declaration order** functools.wraps(app).

**Explicit results** ClosingIterator(app(environ, start\_response), tuple(run\_after\_response\_callbacks, Platform.destroy)).

**Local steps**

- Return ClosingIterator(app(environ, start\_response), tuple(run\_after\_response\_callbacks, Platform.destroy)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0007.json#L4446) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L3) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L3)

<a id="op-caec197ce1190f"></a>
### Application

`operation_foundation_app_business_behavior_application`

**Inputs** request.

**Wrappers, in declaration order** after\_response\_wrapper, Request.application.

**Record and data access** resolve a document from “Security Settings” via get\_doc.

**Explicit results** response.

**Explicit failure paths** NotFound.

**Local steps**

- Set response from no value.
- Attempt the following.
  - Evaluate init\_request(request).
  - Evaluate validate\_auth().
  - If request.method equals “OPTIONS”.
    - Set response from Response().
  - Otherwise.
    - If Platform.form\_dict.cmd.
      - Bind dependencies deprecation\_warning.
      - Evaluate record a compatibility advisory for the invoked interface.
      - Evaluate Platform.handler.handle().
      - Set response from Platform.utils.response.build\_response(“json”).
    - Otherwise.
      - If request.path.startswith(“/api/”).
        - Set response from Platform.api.handle(request).
      - Otherwise.
        - If request.path.startswith(“/backups”).
          - Set response from Platform.utils.response.download\_backup(request.path).
        - Otherwise.
          - If request.path.startswith(“/private/files/”).
            - Set response from Platform.utils.response.download\_private\_file(request.path).
          - Otherwise.
            - If (request.path equals “/.well-known/security.txt” and request.method equals “GET”).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in request.path equals “/.well-known/security.txt” → request.method equals “GET”.
              - If request.scheme differs from “https”.
                - Raise NotFound.
              - Set security\_settings from Platform.get\_doc(“Security Settings”).
              - Set response from Response(security\_settings.security\_txt, content\_type = “text/plain”).
            - Otherwise.
              - If (request.path.startswith(“/.well-known/”) and request.method equals “GET”).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in request.path.startswith(“/.well-known/”) → request.method equals “GET”.
                - Set response from handle\_wellknown(request.path).
              - Otherwise.
                - If request.method belongs to tuple(“GET”, “HEAD”, “POST”).
                  - Set response from get\_response().
                - Otherwise.
                  - Raise NotFound.
- On failure (Exception) bound to e.
  - Set response from e.get\_response(request.environ) when isinstance(e, HTTPException), otherwise handle\_exception(e).
    - Value choice on isinstance(e, HTTPException) — true gives e.get\_response(request.environ), false gives handle\_exception(e).
  - If db bound to getattr(Platform.local, “db”, no value).
    - Evaluate db.rollback(chain = true).
- When the protected block completes normally.
  - Evaluate sync\_database().
- On exit, including pending return or failure.
  - Attempt the following.
    - Evaluate run\_after\_request\_hooks(request, response).
  - On failure (Exception).
    - Evaluate Platform.logger().error(“Failed to run after request hook”, exc\_info = true).
- Evaluate log\_request(request, response).
- Evaluate process\_response(response).
- Return response.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “db”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0007.json#L4557) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L4) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L4)

<a id="op-deda4afe099483"></a>
### Run after request hooks

`operation_foundation_app_business_behavior_run_after_request_hooks`

**Inputs** request, response.

**Explicit results** no value.

**Local steps**

- If not getattr(Platform.local, “initialised”, false).
  - Return no value.
- For each after\_request\_task in Platform.get\_hooks(“after\_request”).
  - Evaluate Platform.call(after\_request\_task, response = response, request = request).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “initialised”, false), Platform.get\_hooks(“after\_request”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0007.json#L5705) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L13) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L12)

<a id="op-f8bf1c57050b96"></a>
### Init request

`operation_foundation_app_business_behavior_initialize_request`

**Inputs** request.

**Explicit failure paths** Platform.SessionStopped(“Session Stopped”).

**Local steps**

- Set site from (\_site or request.headers.get(“X-Platform-Site-Name”) or get\_site\_name(get\_request\_host(request))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_site → request.headers.get(“X-Platform-Site-Name”) → get\_site\_name(get\_request\_host(request)).
- Attempt the following.
  - Evaluate Platform.init(site, sites\_path = \_sites\_path, force = true, is\_request = true).
- On exit, including pending return or failure.
  - Set Platform.local.request from request.
  - Set request.after\_response from CallbackManager().
- Require (Platform.local.conf and Platform.local.conf.db\_name) or report “config should be loaded”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.local.conf → Platform.local.conf.db\_name.
- Set Platform.local.is\_ajax from request.headers.get(“X-Requested-With”) equals “XMLHttpRequest”.
- Evaluate Platform.connect(set\_admin\_as\_user = false).
- If Platform.local.conf.maintenance\_mode.
  - If Platform.local.conf.allow\_reads\_during\_maintenance.
    - Evaluate setup\_read\_only\_mode().
  - Otherwise.
    - Raise Platform.SessionStopped(“Session Stopped”).
- If request.path.startswith(“/api/method/upload\_file”).
  - Bind dependencies get\_max\_file\_size.
  - Set request.max\_content\_length from get\_max\_file\_size().
- Otherwise.
  - Set request.max\_content\_length from (cint(Platform.local.conf.get(“max\_file\_size”)) or ((25 × 1024) × 1024)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.local.conf.get(“max\_file\_size”)) → ((25 × 1024) × 1024).
- Evaluate make\_form\_dict(request).
- If request.method differs from “OPTIONS”.
  - Set Platform.local.http\_request from HTTPRequest().
- For each before\_request\_task in Platform.get\_hooks(“before\_request”).
  - Evaluate Platform.call(before\_request\_task).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“before\_request”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L3) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L9) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L8)

<a id="op-a144d5c82dfc9f"></a>
### Setup read only mode

`operation_foundation_app_business_behavior_setup_read_only_mode`

**Inputs** no declared parameters.

**Local steps**

- Set Platform.flags.read\_only from true.
- If Platform.conf.read\_from\_replica.
  - Evaluate Platform.connect\_replica().
- Otherwise.
  - Evaluate Platform.db.begin(read\_only = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0007.json#L6554) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L18) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L17)

<a id="op-0c9f6cc223f15f"></a>
### Log request

`operation_foundation_app_business_behavior_log_request`

**Inputs** request, response.

**Local steps**

- If (hasattr(Platform.local, “conf”) and Platform.local.conf.enable\_Platform\_logger).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(Platform.local, “conf”) → Platform.local.conf.enable\_Platform\_logger.
  - Evaluate Platform.logger(“Platform.web”, allow\_site = Platform.local.site).info(mapping(“site” → Platform.local.site, “remote\_addr” → getattr(request, “remote\_addr”, “NOTFOUND”), “pid” → os.getpid(), “user” → getat ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(request, “remote\_addr”, “NOTFOUND”), getattr(Platform.local.session, “user”, “NOTFOUND”) and 5 further calls.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L4) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L10) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L9)

<a id="op-8ebce7610d4aa7"></a>
### Process response

`operation_foundation_app_business_behavior_process_response`

**Inputs** response.

**Explicit results** no value.

**Local steps**

- If not response.
  - Return no value.
- Evaluate response.headers.setdefault(“Cache-Control”, NO\_CACHE\_HEADERS at “Cache-Control”).
- If hasattr(Platform.local, “rate\_limiter”).
  - Evaluate response.headers.update(Platform.local.rate\_limiter.headers()).
- If trace\_id bound to Platform.monitor.get\_trace\_id().
  - Evaluate response.headers.update(mapping(“X-Platform-Request-Id” → trace\_id)).
- If hasattr(Platform.local, “conf”).
  - Evaluate set\_cors\_headers(response).
- If (response.status\_code belongs to tuple(401, 403) and is\_oauth\_metadata\_enabled(“resource”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in response.status\_code belongs to tuple(401, 403) → is\_oauth\_metadata\_enabled(“resource”).
  - Evaluate set\_authenticate\_headers(response).
- Evaluate response.headers.update(Platform.local.response\_headers).
- Set public\_cache from any(generator of “public” belongs to h for h drawn from response.headers.getlist(“Cache-Control”)).
  - Draw h from response.headers.getlist(“Cache-Control”).
- If (hasattr(Platform.local, “cookie\_manager”) and not public\_cache).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(Platform.local, “cookie\_manager”) → not public\_cache.
  - Evaluate Platform.local.cookie\_manager.flush\_cookies(response = response).
- If Platform.\_dev\_server.
  - Evaluate response.headers.update(NO\_CACHE\_HEADERS).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0008.json#L6) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L12) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L11)

<a id="op-01326495acf067"></a>
### Set cors headers

`operation_foundation_app_business_behavior_set_cross_origin_resource_sharing_headers`

**Inputs** response.

**Explicit results** no value.

**Local steps**

- Set allowed\_origins from Platform.conf.allow\_cors.
- If hasattr(Platform.local, “allow\_cors”).
  - Set allowed\_origins from Platform.local.allow\_cors.
- If not (allowed\_origins and request bound to Platform.local.request and origin bound to request.headers.get(“Origin”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allowed\_origins → request bound to Platform.local.request → origin bound to request.headers.get(“Origin”).
  - Return no value.
- If allowed\_origins differs from “\*”.
  - If not isinstance(allowed\_origins, list).
    - Set allowed\_origins from list(allowed\_origins).
  - If origin does not belong to allowed\_origins.
    - Return no value.
- Set cors\_headers from mapping(“Access-Control-Allow-Credentials” → “true”, “Access-Control-Allow-Origin” → origin, “Vary” → “Origin”).
- If request.method equals “OPTIONS”.
  - Set cors\_headers at “Access-Control-Allow-Methods” from request.headers.get(“Access-Control-Request-Method”).
  - If allowed\_headers bound to request.headers.get(“Access-Control-Request-Headers”).
    - Set cors\_headers at “Access-Control-Allow-Headers” from allowed\_headers.
  - If not Platform.conf.developer\_mode.
    - Set cors\_headers at “Access-Control-Max-Age” from “86400”.
- Evaluate response.headers.update(cors\_headers).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0008.json#L610) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L17) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L16)

<a id="op-cb032213ff40cc"></a>
### Set authenticate headers

`operation_foundation_app_business_behavior_set_authenticate_headers`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** response.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0008.json#L1124) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L16) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L15)

<a id="op-a2c432ed7f9db6"></a>
### Make form dict

`operation_foundation_app_business_behavior_make_form_mapping`

**Inputs** request.

**Explicit failure paths** validation helper with Platform.DataError — translated “Invalid request body” · validation helper — translated “Invalid request arguments”.

**Local steps**

- Set request\_data from request.get\_data(as\_text = true).
- If (request\_data and request.is\_json).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in request\_data → request.is\_json.
  - Attempt the following.
    - Set args from orjson.loads(request\_data).
  - On failure (orjson.JSONDecodeError).
    - Call the validation error handler Platform.throw(translated “Invalid request body”, Platform.DataError).
- Otherwise.
  - Set args from mapping().
  - Evaluate args.update((request.args or mapping())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in request.args → mapping().
  - Evaluate args.update((request.form or mapping())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in request.form → mapping().
- If isinstance(args, dict).
  - Set Platform.local.form\_dict from Platform.\_dict(args).
  - Evaluate Platform.local.form\_dict.pop(“\_”, no value).
- Otherwise.
  - If isinstance(args, list).
    - Set Platform.local.form\_dict at “data” from args.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Invalid request arguments”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0008.json#L1242) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L11) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L10)

<a id="op-8db69c6deb15ac"></a>
### Handle exception

`operation_foundation_app_business_behavior_handle_exception`

**Inputs** e.

**Wrappers, in declaration order** handle\_does\_not\_exist\_error.

**Explicit results** response.

**Local steps**

- Set response from no value.
- Set http\_status\_code from getattr(e, “http\_status\_code”, 500).
- Set accept\_header from (Platform.get\_request\_header(“Accept”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_request\_header(“Accept”) → empty text.
- Set respond\_as\_json from ((Platform.get\_request\_header(“Accept”) and (Platform.local.is\_ajax or “application/json” belongs to accept\_header)) or (nested operand in the contract.local.request.path.startswith(“/api/”) and not accept ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (Platform.get\_request\_header(“Accept”) and (Platform.local.is\_ajax or “application/json” belongs to accept\_header)) → (Platform.local.request.path.startswith(“/api/”) and not accept\_header.startswith(“text”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_request\_header(“Accept”) → (Platform.local.is\_ajax or “application/json” belongs to accept\_header).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.is\_ajax → “application/json” belongs to accept\_header.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.local.request.path.startswith(“/api/”) → not accept\_header.startswith(“text”).
- If not Platform.session.user.
  - Set Platform.session.user from “Guest”.
- If getattr(Platform.local, “mcp\_request”, no value).
  - Bind dependencies error\_response.
  - Set response from error\_response(e).
- Otherwise.
  - If respond\_as\_json.
    - Set response from Platform.utils.response.report\_error(http\_status\_code).
  - Otherwise.
    - If isinstance(e, Platform.SessionStopped).
      - Set response from Platform.utils.response.handle\_session\_stopped().
    - Otherwise.
      - If (http\_status\_code equals 500 and (Platform.db and isinstance(e, Platform.db.InternalError)) and (Platform.db and (Platform.db.is\_deadlocked(e) or Platform.db.is\_timedout(e)))).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in http\_status\_code equals 500 → (Platform.db and isinstance(e, Platform.db.InternalError)) → (Platform.db and (Platform.db.is\_deadlocked(e) or Platform.db.is\_timedout(e))).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db → isinstance(e, Platform.db.InternalError).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db → (Platform.db.is\_deadlocked(e) or Platform.db.is\_timedout(e)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.is\_deadlocked(e) → Platform.db.is\_timedout(e).
        - Set http\_status\_code from 508.
      - Otherwise.
        - If http\_status\_code equals 401.
          - Set response from ErrorPage(http\_status\_code = http\_status\_code, title = translated “Session Expired”, message = translated “Your session has expired, please login again to continue.”).render().
        - Otherwise.
          - If http\_status\_code equals 403.
            - Set response from ErrorPage(http\_status\_code = http\_status\_code, title = translated “Not Permitted”, message = translated “You do not have enough permissions to complete the action”).render().
          - Otherwise.
            - If http\_status\_code equals 404.
              - Set response from ErrorPage(http\_status\_code = http\_status\_code, title = translated “Not Found”, message = translated “The resource you are looking for is not available”).render().
            - Otherwise.
              - If http\_status\_code equals 429.
                - Set response from Platform.rate\_limiter.respond().
              - Otherwise.
                - Set response from ErrorPage(http\_status\_code = http\_status\_code, title = translated “Server Error”, message = translated “Uncaught Exception”).render().
- If e.\_\_class\_\_ equals Platform.AuthenticationError.
  - If hasattr(Platform.local, “login\_manager”).
    - Evaluate Platform.local.login\_manager.clear\_cookies().
- If (http\_status\_code ≥ 500 or Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in http\_status\_code ≥ 500 → Platform.conf.developer\_mode.
  - Evaluate log\_error\_snapshot(e).
- If (Platform.conf.get(“developer\_mode”) and not respond\_as\_json).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.get(“developer\_mode”) → not respond\_as\_json.
  - Evaluate print(Platform.get\_traceback()).
- Return response.

**Values supplied outside this operation** selected callable from getattr(e, “http\_status\_code”, 500), getattr(Platform.local, “mcp\_request”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L2) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L8) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L7)

<a id="op-f0c832af43a902"></a>
### Sync database

`operation_foundation_app_business_behavior_sync_database`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Set db from getattr(Platform.local, “db”, no value).
- If not db.
  - Return no value.
- If (Platform.local.request.method belongs to UNSAFE\_HTTP\_METHODS or Platform.local.flags.commit).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.request.method belongs to UNSAFE\_HTTP\_METHODS → Platform.local.flags.commit.
  - Evaluate db.commit(chain = true).
- Otherwise.
  - Evaluate db.rollback(chain = true).
- If session bound to getattr(Platform.local, “session\_obj”, no value).
  - Evaluate Platform.request.after\_response.add(session.update).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “db”, no value), getattr(Platform.local, “session\_obj”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0008.json#L2959) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L19) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L18)

<a id="op-738f000cdd33ad"></a>
### Serve

`operation_foundation_app_business_behavior_serve`

**Inputs** port = 8000, profile = false, no\_reload = false, no\_threading = false, site = no value, sites\_path = “.”, proxy = false.

**Local steps**

- Use module bindings application, \_site, \_sites\_path.
- Set \_site from site.
- Set \_sites\_path from sites\_path.
- Bind dependencies run\_simple.
- If (profile or os.environ.get(“USE\_PROFILER”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in profile → os.environ.get(“USE\_PROFILER”).
  - Bind dependencies ProfilerMiddleware.
  - Set application from ProfilerMiddleware(application, sort\_by = tuple(“cumtime”, “calls”), restrictions = tuple(200)).
- If not os.environ.get(“NO\_STATICS”).
  - Set application from application\_with\_statics().
- If (proxy or os.environ.get(“USE\_PROXY”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in proxy → os.environ.get(“USE\_PROXY”).
  - Set application from ProxyFix(application, x\_for = 1, x\_proto = 1, x\_host = 1, x\_port = 1, …).
- Set application.debug from true.
- Set application.config from mapping(“SERVER\_NAME” → “127.0.0.1:8000”).
- Set log from logging.getLogger(“werkzeug”).
- Set log.propagate from false.
- Set in\_test\_env from os.environ.get(“CI”).
- If in\_test\_env.
  - Evaluate log.setLevel(logging.ERROR).
- Evaluate run\_simple(“0.0.0.0”, int(port), application, exclude\_patterns = list(“test\_\*”), use\_reloader = false when in\_test\_env, otherwise not no\_reload, use\_debugger = not in\_test\_env, use\_evalex = not in\_test\_env, …).
  - Value choice on in\_test\_env — true gives false, false gives not no\_reload.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L5) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L15) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L14)

<a id="op-c4dd60af264e4f"></a>
### Application with statics

`operation_foundation_app_business_behavior_application_with_statics`

**Inputs** no declared parameters.

**Explicit results** application.

**Local steps**

- Use module bindings application, \_sites\_path.
- Set application from SharedDataMiddleware(application, mapping(“/assets” → str(os.path.join(\_sites\_path, “assets”)))).
- Set application from StaticDataMiddleware(application, mapping(“/files” → str(os.path.abspath(\_sites\_path)))).
- Return application.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0008.json#L5471) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L5) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L5)

## Record · Auto email report

[Record definition](../../../../data/record-types/auto_email_report.json)

<a id="op-98c50b75c6c520"></a>
### Auto Email Report.autoname

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_autoname`

**Inputs** self.

**Record and data access** read “Auto Email Report” via exists.

**Local steps**

- Set self.name from translated self.report.
- If Platform.db.exists(“Auto Email Report”, self.name).
  - Set self.name from append\_number\_if\_name\_exists(“Auto Email Report”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L4627) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1147) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1579)

<a id="op-ce24023d244061"></a>
### Auto Email Report.validate

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_report\_count().
- Evaluate self.validate\_emails().
- Evaluate self.validate\_report\_format().
- Evaluate self.validate\_mandatory\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate report count](operations-001.md#op-00375962f8f925), [validate emails](operations-001.md#op-4b09024e243a31), [validate report format](operations-002.md#op-8f175e3ab9a80e), [validate mandatory fields](operations-002.md#op-0ebddefe4dbbc3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L4789) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1156) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1588)

<a id="op-cbf7be545a5b8f"></a>
### Auto Email Report.sender email

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_sender_email`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Email Account” via get\_value.

**Explicit results** Platform.db.get\_value(“Email Account”, self.sender, “email\_id”).

**Local steps**

- Return Platform.db.get\_value(“Email Account”, self.sender, “email\_id”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L4900) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1154) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1586)

<a id="op-4b09024e243a31"></a>
### Auto Email Report.validate emails

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_validate_emails`

**Inputs** self.

**Local steps**

- If “,” belongs to self.email\_to.
  - Evaluate self.email\_to.replace(“,”, whitespace '\\n').
- Set valid from list().
- For each email in self.email\_to.split().
  - If email.
    - Evaluate validate\_email\_address(email, true).
    - Evaluate valid.append(email).
- Set self.email\_to from whitespace '\\n'.join(valid).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L4985) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1157) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1589)

<a id="op-00375962f8f925"></a>
### Auto Email Report.validate report count

`operation_foundation_email_record_definitions_auto_email_report_business_behavior_auto_email_report_validate_report_count`

**Inputs** self.

**Record and data access** read “Auto Email Report” via count.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set count from Platform.db.count(“Auto Email Report”, mapping(“user” → self.user, “enabled” → 1)).
- Set max\_reports\_per\_user from (cint(Platform.local.conf.max\_reports\_per\_user) or cint(Platform.get\_system\_settings(“max\_auto\_email\_report\_per\_user”)) or 20).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.local.conf.max\_reports\_per\_user) → cint(Platform.get\_system\_settings(“max\_auto\_email\_report\_per\_user”)) → 20.
- If count &gt; (max\_reports\_per\_user + negative 1 when self.flags.in\_insert, otherwise 0).
  - Value choice on self.flags.in\_insert — true gives negative 1, false gives 0.
  - Set msg from translated “Only {0} emailed reports are allowed per user.”.format(max\_reports\_per\_user).
  - Update msg using + (one space + translated “To allow more reports update limit in System Settings.”).
  - Call the validation error handler Platform.throw(msg, title = translated “Report limit reached”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“max\_auto\_email\_report\_per\_user”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L5208) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1159) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1591)
