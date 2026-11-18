# Shared value and file services · operations 32

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Page

<a id="op-47bdd1da2cd69d"></a>
### Page.wait for load.start wait

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_wait_for_load_start_wait`

**Inputs** no declared parameters.

**Local steps**

- Evaluate self.session.wait\_for\_event(event, timeout).
- Evaluate self.session.remove\_listener(“Page.lifecycleEvent”, event).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L124) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L194) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L282)

<a id="op-f889923ce548c1"></a>
### Page.get element height

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_get_element_height`

**Inputs** self, selector = “body”.

**Explicit results** height.

**Local steps**

- If not self.is\_print\_designer.
  - Set selector from “.wrapper”.
- Set js from formatted text (function() {  var wrapper = document.querySelector('{selector}');  if (!wrapper) return 0;  var h = wrapper.getBoundingClientRect().height;.
- Attempt the following.
  - Set result from self.evaluate(js).
  - Set height from (result.get(“result”, mapping()).get(“value”, 0) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in result.get(“result”, mapping()).get(“value”, 0) → 0.
- On failure (Exception).
  - Attempt the following.
    - Evaluate self.send(“DOM.enable”).
    - Set tuple(doc\_result, \_err) from self.send(“DOM.getDocument”).
    - Set doc\_node\_id from doc\_result at “root” at “nodeId”.
    - Set tuple(result, \_err) from self.send(“DOM.querySelector”, mapping(“nodeId” → doc\_node\_id, “selector” → selector)).
    - Set node\_id from result at “nodeId”.
    - Set tuple(result, \_err) from self.send(“DOM.getBoxModel”, mapping(“nodeId” → node\_id)).
    - Set height from result at “model” at “height”.
  - On exit, including pending return or failure.
    - Evaluate self.send(“DOM.disable”).
- Return height.

**Methods declared on this owner** [evaluate](operations-031.md#op-2c79018ba0e0df), [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L104) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L174) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L262)

<a id="op-723267dc77689c"></a>
### Page.add page size css

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_add_page_size_css`

**Inputs** self.

**Explicit failure paths** RuntimeError(formatted text Error enabling DOM: {error}) · RuntimeError(formatted text Error enabling CSS: {error}) · RuntimeError(formatted text Error creating stylesheet: {error}) · RuntimeError(formatted text Error setting stylesheet text: {error}).

**Local steps**

- Set width from (str(self.options at “paperWidth”) + “in”).
- Set height from (str(self.options at “paperHeight”) + “in”).
- Set marginLeft from (str(self.options at “marginLeft”) + “in”).
- Set marginRight from (str(self.options at “marginRight”) + “in”).
- Set marginTop from (str(self.options at “marginTop”) + “in”).
- Set marginBottom from (str(self.options at “marginBottom”) + “in”).
- Set tuple(result, error) from self.send(“DOM.enable”).
- If error.
  - Raise RuntimeError(formatted text Error enabling DOM: {error}).
- Set tuple(result, error) from self.send(“CSS.enable”).
- If error.
  - Raise RuntimeError(formatted text Error enabling CSS: {error}).
- Set tuple(result, error) from self.send(“CSS.createStyleSheet”, mapping(“frameId” → self.\_ensure\_frame\_id())).
- If error.
  - Raise RuntimeError(formatted text Error creating stylesheet: {error}).
- Set style\_sheet\_id from result at “styleSheetId”.
- Set css\_rule from formatted text   @page {  size: {width} {height};  margin: {marginTop} {marginRight} {marginBottom} {marginLeft};  }.
- Set tuple(result, error) from self.send(“CSS.setStyleSheetText”, mapping(“styleSheetId” → style\_sheet\_id, “text” → css\_rule)).
- If error.
  - Raise RuntimeError(formatted text Error setting stylesheet text: {error}).
- Evaluate self.send(“CSS.disable”).
- Evaluate self.send(“DOM.disable”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315), [ensure frame id](operations-031.md#op-862155ea3107e4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L97) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L167) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L255)

<a id="op-dd6f18aa7d680d"></a>
### Page.set device metrics

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_set_device_metrics`

**Inputs** self, width = 1280, height = 720, scale\_factor = 1.

**Explicit failure paths** RuntimeError(formatted text Error setting device metrics: {error}).

**Local steps**

- Set tuple(\_result, error) from self.send(“Emulation.setDeviceMetricsOverride”, mapping(“width” → width, “height” → height, “deviceScaleFactor” → scale\_factor, “mobile” → false)).
- If error.
  - Raise RuntimeError(formatted text Error setting device metrics: {error}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L118) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L188) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L276)

<a id="op-0b80cdc587bb08"></a>
### Page.get content height

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_get_content_height`

**Inputs** self.

**Explicit results** ((result or mapping()).get(“result”, mapping()).get(“value”) or 0).

**Local steps**

- Set result from self.evaluate(multiline text in the contract).
- Return ((result or mapping()).get(“result”, mapping()).get(“value”) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (result or mapping()).get(“result”, mapping()).get(“value”) → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → mapping().

**Methods declared on this owner** [evaluate](operations-031.md#op-2c79018ba0e0df).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L103) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L173) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L261)

<a id="op-4e746fc88dd7f6"></a>
### Page.capture screenshot

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_capture_screenshot`

**Inputs** self, image\_format = “jpeg”, quality = 30.

**Explicit results** base64.b64decode(result at “data”).

**Explicit failure paths** RuntimeError(formatted text Error capturing screenshot: {error}).

**Local steps**

- Set params from mapping(“format” → image\_format, “captureBeyondViewport” → false).
- If image\_format belongs to tuple(“jpeg”, “webp”).
  - Set params at “quality” from quality.
- Set tuple(result, error) from self.send(“Page.captureScreenshot”, params).
- If error.
  - Raise RuntimeError(formatted text Error capturing screenshot: {error}).
- Return base64.b64decode(result at “data”).

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L98) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L168) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L256)

<a id="op-98d7734dfd312b"></a>
### Page.generate pdf

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_generate_pdf`

**Inputs** self, wait\_for\_pdf = true, raw = false.

**Explicit results** no value · self.get\_pdf\_from\_stream(result at “stream”, raw).

**Explicit failure paths** RuntimeError(formatted text Error generating PDF: {error}) · ValueError(“Stream handle not returned from Page.printToPDF”).

**Local steps**

- Evaluate self.add\_page\_size\_css().
- If not wait\_for\_pdf.
  - Set self.wait\_for\_pdf from self.send(“Page.printToPDF”, self.options, return\_future = true).
  - Return no value.
- Set tuple(result, error) from self.send(“Page.printToPDF”, self.options).
- If error.
  - Raise RuntimeError(formatted text Error generating PDF: {error}).
- If “stream” does not belong to result.
  - Raise ValueError(“Stream handle not returned from Page.printToPDF”).
- Return self.get\_pdf\_from\_stream(result at “stream”, raw).

**Methods declared on this owner** [add page size css](operations-032.md#op-723267dc77689c), [send](operations-031.md#op-9e24e910341315), [get pdf from stream](operations-032.md#op-d21607eec4ad83).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L102) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L172) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L260)

<a id="op-ba8d5c4dc3c1d8"></a>
### Page.get pdf stream id

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_get_pdf_stream_id`

**Inputs** self.

**Explicit results** response at “result” at “stream”.

**Explicit failure paths** RuntimeError(“Timed out waiting for the Page.printToPDF response”).

**Local steps**

- Evaluate self.session.wait\_for\_event(self.wait\_for\_pdf).
- Set response\_future from self.wait\_for\_pdf.result().
- Evaluate self.session.wait\_for\_event(response\_future, timeout = 30).
- If (not response\_future.done() or response\_future.cancelled()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not response\_future.done() → response\_future.cancelled().
  - Raise RuntimeError(“Timed out waiting for the Page.printToPDF response”).
- Set response from response\_future.result().
- Return response at “result” at “stream”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L107) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L177) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L265)

<a id="op-d21607eec4ad83"></a>
### Page.get pdf from stream

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_get_pdf_from_stream`

**Inputs** self, stream\_id, raw = false.

**Explicit results** pdf\_data · PdfReader(BytesIO(pdf\_data)).

**Explicit failure paths** RuntimeError(formatted text Error reading PDF chunk: {error}) · RuntimeError(formatted text Error closing PDF stream: {error}).

**Local steps**

- Bind dependencies BytesIO.
- Bind dependencies PdfReader.
- Set chunks from list().
- Set offset from 0.
- While true.
  - Set tuple(chunk\_result, error) from self.send(“IO.read”, mapping(“handle” → stream\_id, “offset” → offset, “size” → (1024 × 1024))).
  - If error.
    - Raise RuntimeError(formatted text Error reading PDF chunk: {error}).
  - Set chunk\_data from chunk\_result at “data”.
  - If chunk\_result.get(“base64Encoded”, false).
    - Set chunk\_data from base64.b64decode(chunk\_data).
  - Evaluate chunks.append(chunk\_data).
  - Update offset using + len(chunk\_data).
  - If chunk\_result.get(“eof”, false).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Set pdf\_data from byte value.join(chunks).
- Evaluate chunks.clear().
- Set tuple(\_result, error) from self.send(“IO.close”, mapping(“handle” → stream\_id)).
- If error.
  - Raise RuntimeError(formatted text Error closing PDF stream: {error}).
- If raw.
  - Return pdf\_data.
- Return PdfReader(BytesIO(pdf\_data)).

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L106) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L176) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L264)

<a id="op-71f0410cd5311a"></a>
### Page.close

`operation_foundation_binding_foundation_utils_pdf_generator_page_page_close`

**Inputs** self.

**Explicit failure paths** RuntimeError(formatted text Error closing target: {error}).

**Local steps**

- Evaluate self.send(“Fetch.disable”).
- Set tuple(\_result, error) from self.send(“Target.closeTarget”, mapping(“targetId” → self.target\_id)).
- If error.
  - Raise RuntimeError(formatted text Error closing target: {error}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [send](operations-031.md#op-9e24e910341315).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L99) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L169) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L257)

## Service · Password

<a id="op-146f0b2d45af0d"></a>
### Get decrypted password

`operation_foundation_utils_password_business_behavior_get_decrypted_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doctype, name, fieldname, raise\_exception.

**Explicit result forms** no value, the result of a delegated call.

**Locally raised failures** e.

**Observed service boundaries** validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0489.json#L4612) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1613) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L399)

<a id="op-4f4c42b84ac396"></a>
### Set encrypted password

`operation_foundation_utils_password_business_behavior_set_encrypted_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doctype, name, pwd, fieldname.

**Locally raised failures** e.

**Observed service boundaries** record mutation request, validation or user-notification service.

**Local structure** 4 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1620) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L405)

<a id="op-9d79331d0eae83"></a>
### Remove encrypted password

`operation_foundation_utils_password_business_behavior_remove_encrypted_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doctype, name, fieldname.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0489.json#L5807) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1617) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L402)

<a id="op-988c158255908b"></a>
### Has password

`operation_foundation_binding_foundation_utils_password_has_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L62) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L132) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L220)

<a id="op-816e8ac17bf24b"></a>
### Check password

`operation_foundation_utils_password_business_behavior_check_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, pwd, doctype, fieldname, delete\_tracker\_cache.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** AuthenticationError.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L5) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1607) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L393)

<a id="op-c9580a6b0f8a2d"></a>
### Delete login failed cache

`operation_foundation_utils_password_business_behavior_delete_login_failed_cache`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0489.json#L6802) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1611) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L397)

<a id="op-4a922aa716bd2f"></a>
### Update password

`operation_foundation_utils_password_business_behavior_update_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, pwd, doctype, fieldname, logout\_all\_sessions.

**Observed service boundaries** record mutation request.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L7) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1621) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L406)

<a id="op-574a33e9779855"></a>
### Delete all passwords for

`operation_foundation_utils_password_business_behavior_delete_all_passwords_for`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doctype, name.

**Locally raised failures** active or constructed exception.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L686) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1610) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L396)

<a id="op-51dc47aaf69911"></a>
### Rename password

`operation_foundation_utils_password_business_behavior_rename_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doctype, old\_name, new\_name.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L853) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1618) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L403)

<a id="op-ec0c2c5fdad7c2"></a>
### Rename password field

`operation_foundation_utils_password_business_behavior_rename_password_field`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doctype, old\_fieldname, new\_fieldname.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L1020) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1619) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L404)

<a id="op-d8a920be690b34"></a>
### Create auth table

`operation_foundation_utils_password_business_behavior_create_authentication_table`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L1183) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1608) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L394)

<a id="op-a0ac14772de629"></a>
### Encrypt

`operation_foundation_utils_password_business_behavior_encrypt`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** txt, encryption\_key.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L1228) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1612) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L398)

<a id="op-192881345db3fe"></a>
### Decrypt

`operation_foundation_utils_password_business_behavior_decrypt`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** txt, encryption\_key, key.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L1437) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1609) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L395)

<a id="op-d17292c1c16614"></a>
### Get encryption key

`operation_foundation_utils_password_business_behavior_get_encryption_key`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L1783) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1614) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L400)
