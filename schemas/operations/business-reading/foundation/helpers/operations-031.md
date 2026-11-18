# Shared value and file services · operations 31

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Oauth

<a id="op-ae9c0b5e0902cc"></a>
### Update oauth user

`operation_foundation_utils_delegated_authorization_business_behavior_update_delegated_authorization_user`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, data, provider.

**Explicit result forms** Boolean false.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0489.json#L2861) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1294) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L90)

<a id="op-99c33d86335f4a"></a>
### Get first name

`operation_foundation_utils_delegated_authorization_business_behavior_get_first_name`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** data.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0489.json#L3976) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1283) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L81)

<a id="op-7abbdc3751c449"></a>
### Get last name

`operation_foundation_utils_delegated_authorization_business_behavior_get_last_name`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** data.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0489.json#L4110) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1285) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L83)

<a id="op-46dbf6dfa3e81c"></a>
### Get email

`operation_foundation_utils_delegated_authorization_business_behavior_get_email`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** data.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0489.json#L4201) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1282) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L80)

<a id="op-7e6f25eece5084"></a>
### Redirect post login

`operation_foundation_utils_delegated_authorization_business_behavior_redirect_post_login`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** desk\_user, redirect\_to, provider.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0489.json#L4311) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1293) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L89)

## Service · Page

<a id="op-3d60ca53a4602e"></a>
### Read local resource

`operation_foundation_binding_foundation_utils_pdf_generator_page_read_local_resource`

**Inputs** url.

**Declared result** (tuple at tuple(str, (str bitwise or no value)) bitwise or no value).

**Explicit results** tuple(content, “image/svg+xml” when clean\_path.endswith(“.svg”), otherwise no value) · no value.

**Local steps**

- Bind dependencies os.
- Set parsed from urllib.parse.urlparse(url).
- Set clean\_path from urllib.parse.unquote(parsed.path).lstrip(“/”).
- Set query\_params from urllib.parse.parse\_qs(parsed.query).
- Set bench\_sites from os.path.abspath(os.path.join(Platform.utils.get\_bench\_path(), “sites”)).
- Set asset\_path from os.path.abspath(os.path.join(bench\_sites, “assets”)).
- Set site\_public\_root from os.path.realpath(Platform.utils.get\_site\_path(“public”)).
- Set site\_private\_files\_root from os.path.realpath(Platform.utils.get\_site\_path(“private/files”)).
- If clean\_path.startswith(“assets/”).
  - Set final\_system\_path from os.path.abspath(os.path.join(bench\_sites, clean\_path)).
  - Set is\_safe from os.path.commonpath(list(final\_system\_path, asset\_path)) equals asset\_path.
- Otherwise.
  - If clean\_path.startswith(“private/files/”).
    - Set can\_read from false.
    - If Platform.session.user equals “Administrator”.
      - Set can\_read from true.
    - Otherwise.
      - If Platform.session.user differs from “Guest”.
        - Set fid from query\_params.get(“fid”, list(no value)) at 0.
        - If find\_file\_by\_url((“/” + clean\_path), name = fid).
          - Set can\_read from true.
    - Set file\_path from clean\_path.removeprefix(“private/files/”).
    - Set final\_system\_path from os.path.realpath(os.path.join(site\_private\_files\_root, file\_path)).
    - Set is\_safe from (can\_read and os.path.commonpath(list(final\_system\_path, site\_private\_files\_root)) equals site\_private\_files\_root).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in can\_read → os.path.commonpath(list(final\_system\_path, site\_private\_files\_root)) equals site\_private\_files\_root.
  - Otherwise.
    - Set final\_system\_path from os.path.realpath(os.path.join(site\_public\_root, clean\_path)).
    - Set is\_safe from os.path.commonpath(list(final\_system\_path, site\_public\_root)) equals site\_public\_root.
- If (is\_safe and os.path.isfile(final\_system\_path)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_safe → os.path.isfile(final\_system\_path).
  - If content bound to Platform.read\_file(final\_system\_path, as\_base64 = true).
    - Return tuple(content, “image/svg+xml” when clean\_path.endswith(“.svg”), otherwise no value).
      - Value choice on clean\_path.endswith(“.svg”) — true gives “image/svg+xml”, false gives no value.
- Otherwise.
  - If clean\_path.
    - Evaluate Platform.log\_error(title = “Attempted Unauthorized File Access in PDF Generator”, message = formatted text Blocked access to: {clean\_path}  Resolved Path to: {final\_system\_path}).
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L125) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L195) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L283)

<a id="op-80f115bd8a6fba"></a>
### Page.initialize

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_init`

**Inputs** self, session, browser\_context\_id, page\_type.

**Explicit failure paths** RuntimeError(formatted text Error attaching to target: {error}).

**Local steps**

- Set self.session from session.
- Set tuple(result, error) from self.session.send(“Target.createTarget”, mapping(“url” → empty text, “browserContextId” → browser\_context\_id)).
- If error.
  - Evaluate Platform.log\_error(title = “Error creating new page:”, message = formatted text {error}).
- Set self.target\_id from result at “targetId”.
- Set self.type from page\_type.
- Set tuple(result, error) from self.session.send(“Target.attachToTarget”, mapping(“targetId” → self.target\_id, “flatten” → true)).
- If error.
  - Raise RuntimeError(formatted text Error attaching to target: {error}).
- Set self.session\_id from result at “sessionId”.
- Evaluate self.send(“Page.enable”).
- Set self.frame\_id from no value.
- Evaluate self.get\_frame\_id\_on\_demand().
- Evaluate self.set\_media\_emulation(“print”).
- Evaluate self.set\_cookies().

If control reaches the end, it returns no value.

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315), [get frame id on demand](operations-031.md#op-0c6221a8ea4546), [set media emulation](operations-031.md#op-b74840f975b750), [set cookies](operations-031.md#op-06d4e16510600f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L108) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L178) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L266)

<a id="op-9e24e910341315"></a>
### Page.send

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_send`

**Inputs** self, method, params = no value, return\_future = false.

**Explicit results** self.session.send(method, params, self.session\_id, return\_future).

**Local steps**

- If params is identical to no value.
  - Set params from mapping().
- Return self.session.send(method, params, self.session\_id, return\_future).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L115) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L185) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L273)

<a id="op-0c6221a8ea4546"></a>
### Page.get frame id on demand

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_get_frame_id_on_demand`

**Inputs** self.

**Explicit results** self.frame\_id.

**Explicit failure paths** RuntimeError(formatted text Error fetching frameId: {error}) · propagate active failure.

**Local steps**

- If self.frame\_id.
  - Return self.frame\_id.
- Attempt the following.
  - Set tuple(result, error) from self.send(“Page.getFrameTree”).
  - If error.
    - Raise RuntimeError(formatted text Error fetching frameId: {error}).
  - Set frame\_tree from result at “frameTree”.
  - Set frame from frame\_tree at “frame”.
  - Set self.frame\_id from frame at “id”.
  - Return self.frame\_id.
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Error fetching frameId:”, message = formatted text {Platform.get\_traceback()}).
  - Propagate the active failure.

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L105) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L175) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L263)

<a id="op-862155ea3107e4"></a>
### Page.ensure frame id

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_ensure_frame_id`

**Inputs** self.

**Explicit results** self.frame\_id.

**Local steps**

- If not self.frame\_id.
  - Evaluate self.get\_frame\_id\_on\_demand().
- Return self.frame\_id.

**Methods declared on this owner** [get frame id on demand](operations-031.md#op-0c6221a8ea4546).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L100) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L170) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L258)

<a id="op-b74840f975b750"></a>
### Page.set media emulation

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_set_media_emulation`

**Inputs** self, media\_type = “print”.

**Explicit results** self.send(“Emulation.setEmulatedMedia”, mapping(“media” → media\_type)).

**Local steps**

- Return self.send(“Emulation.setEmulatedMedia”, mapping(“media” → media\_type)).

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L119) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L189) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L277)

<a id="op-06d4e16510600f"></a>
### Page.set cookies

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_set_cookies`

**Inputs** self.

**Explicit failure paths** RuntimeError(formatted text Error enabling network: {error}) · RuntimeError(formatted text Error setting cookie: {error}) · RuntimeError(formatted text Error disabling network: {error}).

**Local steps**

- If (Platform.session and Platform.session.sid and hasattr(Platform.local, “request”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session → Platform.session.sid → hasattr(Platform.local, “request”).
  - Set domain from Platform.utils.get\_host\_name().split(“:”, 1) at 0.
  - Set cookie from mapping(“name” → “sid”, “value” → Platform.session.sid, “domain” → domain, “sameSite” → “Strict”).
  - Set tuple(\_result, error) from self.send(“Network.enable”).
  - If error.
    - Raise RuntimeError(formatted text Error enabling network: {error}).
  - Set tuple(\_result, error) from self.send(“Network.setCookie”, cookie).
  - If error.
    - Raise RuntimeError(formatted text Error setting cookie: {error}).
  - Set tuple(\_result, error) from self.send(“Network.disable”).
  - If error.
    - Raise RuntimeError(formatted text Error disabling network: {error}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L117) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L187) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L275)

<a id="op-9d821506330b7b"></a>
### Page.intercept request and fulfill

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_intercept_request_and_fulfill`

**Inputs** self, url\_pattern.

**Explicit results** intercept\_and\_fulfill.

**Local steps**

- Set data from mapping().
- Bind local operation on\_request\_paused\_event for subsequent calls.
- Set event from self.session.start\_listener(“Fetch.requestPaused”, on\_request\_paused\_event, self.session\_id, self.target\_id, …).
- Evaluate self.send(“Fetch.enable”, mapping(“patterns” → list(mapping(“urlPattern” → url\_pattern)))).
- Bind local operation intercept\_and\_fulfill for subsequent calls.
- Return intercept\_and\_fulfill.

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L109) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L179) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L267)

<a id="op-cbb1c51a07e7e0"></a>
### Page.intercept request and fulfill.on request paused event

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_intercept_request_and_fulfill_on_request_paused_event`

**Inputs** future, response.

**Local steps**

- Set params from response.get(“params”).
- If (params and params.get(“requestId”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in params → params.get(“requestId”).
  - Set data at “request\_id” from params at “requestId”.
  - If not future.done().
    - Evaluate future.set\_result(data at “request\_id”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L111) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L181) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L269)

<a id="op-a51f3d50616cb4"></a>
### Page.intercept request and fulfill.intercept and fulfill

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_intercept_request_and_fulfill_intercept_and_fulfill`

**Inputs** no declared parameters.

**Local steps**

- Evaluate self.session.wait\_for\_event(event).
- Evaluate self.send(“Fetch.fulfillRequest”, mapping(“requestId” → event at 1.result(), “responseCode” → 200), return\_future = true).
- Evaluate self.session.remove\_listener(“Fetch.requestPaused”, event).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L110) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L180) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L268)

<a id="op-6631eb8f529e46"></a>
### Page.intercept request for local resources

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_intercept_request_for_local_resources`

**Inputs** self, url\_pattern = “\*”.

**Local steps**

- Set data from mapping().
- Bind local operation on\_request\_paused\_event for subsequent calls.
- Evaluate self.session.start\_listener(“Fetch.requestPaused”, on\_request\_paused\_event, self.session\_id, self.target\_id, …).
- Evaluate self.send(“Fetch.enable”, mapping(“patterns” → list(mapping(“urlPattern” → url\_pattern)))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L112) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L182) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L270)

<a id="op-7bc5621a84eaa9"></a>
### Page.intercept request for local resources.on request paused event

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_intercept_request_for_local_resources_on_request_paused_event`

**Inputs** future, response.

**Explicit results** no value.

**Local steps**

- Set params from response.get(“params”).
- If (params and params.get(“requestId”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in params → params.get(“requestId”).
  - Set data at “request\_id” from params at “requestId”.
  - Set url from params at “request” at “url”.
  - If (isinstance(url, str) and url.startswith(get\_host\_url())).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(url, str) → url.startswith(get\_host\_url()).
    - If resource bound to read\_local\_resource(url).
      - Set tuple(content, content\_type) from resource.
      - Evaluate self.send(“Fetch.fulfillRequest”, mapping(“requestId” → data at “request\_id”, “responseCode” → 200, “responseHeaders” → list(mapping(“name” → “Content-Type”, “value” → content\_type)) when content\_type, oth ….
        - Value choice on content\_type — true gives list(mapping(“name” → “Content-Type”, “value” → content\_type)), false gives list().
      - Return no value.
    - Otherwise.
      - If urllib.parse.urlparse(url).path.lstrip(“/”).
        - Evaluate self.send(“Fetch.failRequest”, mapping(“requestId” → data at “request\_id”, “errorReason” → “AccessDenied”), return\_future = true).
        - Return no value.
  - Evaluate self.send(“Fetch.continueRequest”, mapping(“requestId” → data at “request\_id”), return\_future = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L113) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L183) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L271)

<a id="op-51bdfc06f2925c"></a>
### Page.set tab url

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_set_tab_url`

**Inputs** self, url.

**Local steps**

- Set wait\_and\_fulfill from self.intercept\_request\_and\_fulfill(url).
- Set wait\_start from self.wait\_for\_load(wait\_for = “load”).
- Set page\_navigate from self.send(“Page.navigate”, mapping(“url” → url), return\_future = true).
- Evaluate wait\_and\_fulfill().
- Bind local operation wait\_for\_navigate for subsequent calls.
- Set self.wait\_for\_navigate from wait\_for\_navigate.

If control reaches the end, it returns no value.

**Methods declared on this owner** [intercept request and fulfill](operations-031.md#op-9d821506330b7b), [wait for load](operations-031.md#op-5d87d48a42f953), [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L120) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L190) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L278)

<a id="op-0606f1c1dee927"></a>
### Page.set tab url.wait for navigate

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_set_tab_url_wait_for_navigate`

**Inputs** no declared parameters.

**Local steps**

- Evaluate self.session.wait\_for\_event(page\_navigate, 3).
- Evaluate wait\_start().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L121) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L191) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L279)

<a id="op-73e3867f2bb0e9"></a>
### Page.navigate

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_navigate`

**Inputs** self, url, wait\_for = no value.

**Explicit failure paths** RuntimeError(formatted text Error navigating to URL: {error}).

**Local steps**

- Set wait\_start from self.wait\_for\_load(wait\_for = (wait\_for or list(“load”, “DOMContentLoaded”, “networkIdle”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in wait\_for → list(“load”, “DOMContentLoaded”, “networkIdle”).
- Set tuple(\_result, error) from self.send(“Page.navigate”, mapping(“url” → url)).
- If error.
  - Raise RuntimeError(formatted text Error navigating to URL: {error}).
- Evaluate wait\_start().

If control reaches the end, it returns no value.

**Methods declared on this owner** [wait for load](operations-031.md#op-5d87d48a42f953), [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L114) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L184) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L272)

<a id="op-2c79018ba0e0df"></a>
### Page.evaluate

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_evaluate`

**Inputs** self, expression, await\_promise = false.

**Explicit results** result.

**Explicit failure paths** RuntimeError(formatted text Error evaluating expression: {error}).

**Local steps**

- Evaluate self.send(“Runtime.enable”).
- Set tuple(result, error) from self.send(“Runtime.evaluate”, mapping(“expression” → expression, “awaitPromise” → await\_promise)).
- If error.
  - For each \_i in range(3).
    - Evaluate print(formatted text Error evaluating expression: {error}. Retrying in 500ms).
    - Evaluate time.sleep(0.5).
    - Set tuple(result, error) from self.send(“Runtime.evaluate”, mapping(“expression” → expression, “awaitPromise” → await\_promise)).
    - If not error.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - Raise RuntimeError(formatted text Error evaluating expression: {error}).
- Evaluate self.send(“Runtime.disable”).
- Return result.

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L101) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L171) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L259)

<a id="op-949a43c5d7f038"></a>
### Page.set content

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_set_content`

**Inputs** self, html, wait\_for = no value.

**Local steps**

- If not wait\_for.
  - Set wait\_for from list(“load”, “DOMContentLoaded”).
- Evaluate self.intercept\_request\_for\_local\_resources().
- Set wait\_start from self.wait\_for\_load(wait\_for = wait\_for).
- Evaluate self.send(“Page.setDocumentContent”, mapping(“frameId” → self.\_ensure\_frame\_id(), “html” → html)).
- Set self.wait\_for\_set\_content from wait\_start.

If control reaches the end, it returns no value.

**Methods declared on this owner** [intercept request for local resources](operations-031.md#op-6631eb8f529e46), [wait for load](operations-031.md#op-5d87d48a42f953), [send](operations-031.md#op-9e24e910341315), [ensure frame id](operations-031.md#op-862155ea3107e4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L116) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L186) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L274)

<a id="op-5d87d48a42f953"></a>
### Page.wait for load

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_wait_for_load`

**Inputs** self, wait\_for, timeout = 60.

**Explicit results** start\_wait.

**Local steps**

- Evaluate self.send(“Page.setLifecycleEventsEnabled”, mapping(“enabled” → true)).
- Set status from mapping().
- If isinstance(wait\_for, str).
  - Set status at wait\_for from false.
- If isinstance(wait\_for, list).
  - For each event in wait\_for.
    - Set status at event from false.
- Bind local operation on\_lifecycle\_event for subsequent calls.
- Set event from self.session.start\_listener(“Page.lifecycleEvent”, on\_lifecycle\_event, self.session\_id, self.target\_id, …).
- Bind local operation start\_wait for subsequent calls.
- Return start\_wait.

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L122) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L192) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L280)

<a id="op-54a4a6a7a9cc52"></a>
### Page.wait for load.on lifecycle event

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_wait_for_load_on_lifecycle_event`

**Inputs** future, response.

**Local steps**

- Set params from response.get(“params”, mapping()).
- If params.get(“name”) belongs to status.keys().
  - Set status at params.get(“name”) from true.
  - If all(status.values()).
    - If not future.done().
      - Evaluate future.set\_result(response).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L123) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L193) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L281)
