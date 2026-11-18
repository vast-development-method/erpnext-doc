# Integration and transport · operations 32

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Transport

<a id="op-bc362d84496f5e"></a>
### Check origin

`operation_foundation_binding_foundation_mcp_transport_check_origin`

**Inputs** request.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** McpError(protocol.INVALID\_REQUEST, “Request origin is not allowed”, status = 403).

**Local steps**

- Set origin from request.headers.get(“Origin”).
- If (not origin or origin equals request.host\_url.rstrip(“/”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not origin → origin equals request.host\_url.rstrip(“/”).
  - Return no value.
- Set allowed from (getattr(Platform.local, “allow\_cors”, no value) or Platform.conf.get(“allow\_cors”, list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(Platform.local, “allow\_cors”, no value) → Platform.conf.get(“allow\_cors”, list()).
- If (allowed equals “\*” or origin belongs to allowed when isinstance(allowed, list), otherwise list(allowed)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in allowed equals “\*” → origin belongs to allowed when isinstance(allowed, list), otherwise list(allowed).
  - Value choice on isinstance(allowed, list) — true gives allowed, false gives list(allowed).
  - Return no value.
- Raise McpError(protocol.INVALID\_REQUEST, “Request origin is not allowed”, status = 403).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “allow\_cors”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L116) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1572) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1548)

<a id="op-dcb1a101809dda"></a>
### Decode name

`operation_foundation_binding_foundation_mcp_transport_decode_name`

**Inputs** value.

**Declared result** (str bitwise or no value).

**Explicit results** no value · base64.b64decode(value at slice 9 to negative 2, validate = true).decode(“utf-8”) · value.

**Explicit failure paths** McpError(protocol.HEADER\_MISMATCH, “Mcp-Name header contains invalid characters”) · McpError(protocol.HEADER\_MISMATCH, “Mcp-Name header is not valid base64”).

**Local steps**

- If value is identical to no value.
  - Return no value.
- If (not value.isascii() or any(generator of (ord(char) &lt; 32 or ord(char) equals 127) for char drawn from value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not value.isascii() → any(generator of (ord(char) &lt; 32 or ord(char) equals 127) for char drawn from value).
  - Draw char from value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ord(char) &lt; 32 → ord(char) equals 127.
  - Raise McpError(protocol.HEADER\_MISMATCH, “Mcp-Name header contains invalid characters”).
- If (value.startswith(“=?base64?”) and value.endswith(“?=”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in value.startswith(“=?base64?”) → value.endswith(“?=”).
  - Attempt the following.
    - Return base64.b64decode(value at slice 9 to negative 2, validate = true).decode(“utf-8”).
  - On failure (tuple(binascii.Error, UnicodeDecodeError)).
    - Raise McpError(protocol.HEADER\_MISMATCH, “Mcp-Name header is not valid base64”) with cause no value.
- Return value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L117) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1573) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1549)

<a id="op-45de0a1a0140bf"></a>
### Json response

`operation_foundation_binding_foundation_mcp_transport_json_response`

**Inputs** body, status = 200.

**Declared result** Response.

**Explicit results** Response(json.dumps(body, default = json\_handler), status = status, mimetype = “application/json”).

**Local steps**

- Bind dependencies json\_handler.
- Return Response(json.dumps(body, default = json\_handler), status = status, mimetype = “application/json”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L120) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1576) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1552)

## Record · Unhandled email

[Record definition](../../../../data/record-types/unhandled_email.json)

<a id="op-dd4cd524d76f97"></a>
### Unhandled Email.clear old logs

`operation_foundation_email_record_definitions_unhandled_email_business_behavior_unhandled_email_clear_old_logs`

**Inputs** days = 30.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on “Unhandled Email”.

**Local steps**

- Evaluate Platform.db.delete(“Unhandled Email”, mapping(“creation” → tuple(“&lt;”, Platform.utils.add\_days(nested operand in the contract.utils.nowdate(), (negative 1 × days))))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0232.json#L6603) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1505) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L276)

## Service · Utils

<a id="op-5270e90ce51d6a"></a>
### Get port

`operation_foundation_email_utils_business_behavior_get_port`

**Inputs** doc.

**Explicit results** cint(doc.incoming\_port).

**Local steps**

- If not doc.incoming\_port.
  - If doc.use\_imap.
    - Set doc.incoming\_port from imaplib.IMAP4\_SSL\_PORT when doc.use\_ssl, otherwise imaplib.IMAP4\_PORT.
      - Value choice on doc.use\_ssl — true gives imaplib.IMAP4\_SSL\_PORT, false gives imaplib.IMAP4\_PORT.
  - Otherwise.
    - Set doc.incoming\_port from poplib.POP3\_SSL\_PORT when doc.use\_ssl, otherwise poplib.POP3\_PORT.
      - Value choice on doc.use\_ssl — true gives poplib.POP3\_SSL\_PORT, false gives poplib.POP3\_PORT.
- Return cint(doc.incoming\_port).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L1241) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1539) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L304)

<a id="op-fd4ff43490cdb4"></a>
### Make request

`operation_foundation_integrations_utils_business_behavior_make_request`

**Inputs** method, url, auth = no value, headers = no value, data = no value, json = no value, params = no value, session (named only, default no value), timeout (named only, default no value).

**Explicit results** parse\_qs(response.text) · response.json() · response.text · no value.

**Explicit failure paths** exc.

**Local steps**

- Set auth from (auth or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in auth → empty text.
- Set data from (data or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data → mapping().
- Set headers from (headers or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in headers → mapping().
- Attempt the following.
  - Set s from (session or get\_request\_session()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in session → get\_request\_session().
  - Set response, Platform.flags.integration\_request from s.request(method, url, data = data, auth = auth, headers = headers, json = json, …).
  - Evaluate response.raise\_for\_status().
  - If content\_type bound to response.headers.get(“content-type”).
    - If content\_type equals “text/plain; charset=utf-8”.
      - Return parse\_qs(response.text).
    - Otherwise.
      - If (content\_type.startswith(“application/”) and content\_type.split(“;”) at 0.endswith(“json”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in content\_type.startswith(“application/”) → content\_type.split(“;”) at 0.endswith(“json”).
        - Return response.json().
      - Otherwise.
        - If response.text.
          - Return response.text.
  - Return no value.
- On failure (Exception) bound to exc.
  - If Platform.flags.integration\_request\_doc.
    - Evaluate Platform.flags.integration\_request\_doc.log\_error().
  - Otherwise.
    - Evaluate Platform.log\_error().
  - Raise exc.

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L6785) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L188) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L884)

<a id="op-ff0b2fbf1924b2"></a>
### Make get request

`operation_foundation_integrations_utils_business_behavior_make_get_request`

**Inputs** url, remaining named values kwargs.

**Explicit results** make\_request(“GET”, url, expanded names kwargs).

**Local steps**

- Return make\_request(“GET”, url, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L7431) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L184) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L880)

<a id="op-b5d5391610f6ec"></a>
### Make post request

`operation_foundation_integrations_utils_business_behavior_make_post_request`

**Inputs** url, remaining named values kwargs.

**Explicit results** make\_request(“POST”, url, expanded names kwargs).

**Local steps**

- Return make\_request(“POST”, url, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L7506) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L186) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L882)

<a id="op-7c8c58531633f9"></a>
### Make put request

`operation_foundation_integrations_utils_business_behavior_make_put_request`

**Inputs** url, remaining named values kwargs.

**Explicit results** make\_request(“PUT”, url, expanded names kwargs).

**Local steps**

- Return make\_request(“PUT”, url, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L7581) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L187) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L883)

<a id="op-405a039730e057"></a>
### Make patch request

`operation_foundation_integrations_utils_business_behavior_make_patch_request`

**Inputs** url, remaining named values kwargs.

**Explicit results** make\_request(“PATCH”, url, expanded names kwargs).

**Local steps**

- Return make\_request(“PATCH”, url, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L7656) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L185) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L881)

<a id="op-045edfdbc17b3f"></a>
### Make delete request

`operation_foundation_integrations_utils_business_behavior_make_delete_request`

**Inputs** url, remaining named values kwargs.

**Explicit results** make\_request(“DELETE”, url, expanded names kwargs).

**Local steps**

- Return make\_request(“DELETE”, url, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L183) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L879)

<a id="op-534399d4e80769"></a>
### Create request log

`operation_foundation_integrations_utils_business_behavior_create_request_log`

**Inputs** data, integration\_type = no value, service\_name = no value, name = no value, error = no value, request\_headers = no value, output = no value, remaining named values kwargs.

**Record and data access** resolve a document from mapping(“doctype” → “Integration Request”, “integration\_request\_service” → service\_name, “request\_headers” → get\_json(request\_headers), “data” → get\_json(data), …) via get\_doc.

**State and service calls** call insert on integration\_request · commit.

**Explicit results** integration\_request.

**Local steps**

- If integration\_type equals “Remote”.
  - Set kwargs at “is\_remote\_request” from 1.
- Otherwise.
  - If integration\_type equals “Subscription Notification”.
    - Set kwargs at “request\_description” from integration\_type.
- Set reference\_doctype, reference\_docname from no value.
- If “reference\_doctype” does not belong to kwargs.
  - If isinstance(data, str).
    - Set data from json.loads(data).
  - Set reference\_doctype from data.get(“reference\_doctype”).
  - Set reference\_docname from data.get(“reference\_docname”).
- Set integration\_request from Platform.get\_doc(mapping(“doctype” → “Integration Request”, “integration\_request\_service” → service\_name, “request\_headers” → get\_json(request\_headers), “data” → get\_json(data), …)).
- If name.
  - Set integration\_request.flags.\_name from name.
- Evaluate integration\_request.insert(ignore\_permissions = true).
- Evaluate Platform.db.commit().
- Return integration\_request.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L81) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L179) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L875)

<a id="op-2a3c9853a051be"></a>
### Get json

`operation_foundation_integrations_utils_business_behavior_get_structured_data`

**Inputs** obj.

**Explicit results** obj when isinstance(obj, str), otherwise Platform.as\_json(obj, indent = 1).

**Local steps**

- Return obj when isinstance(obj, str), otherwise Platform.as\_json(obj, indent = 1).
  - Value choice on isinstance(obj, str) — true gives obj, false gives Platform.as\_json(obj, indent = 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L752) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L181) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L877)

<a id="op-919a1d311048b9"></a>
### Json handler

`operation_foundation_integrations_utils_business_behavior_structured_data_handler`

**Inputs** obj.

**Explicit results** str(obj).

**Local steps**

- If isinstance(obj, ((datetime.date bitwise or datetime.timedelta) bitwise or datetime.datetime)).
  - Return str(obj).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L847) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L189) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L885)

<a id="op-3b996c11ab5803"></a>
### Validate dynamic client metadata

`operation_foundation_integrations_utils_business_behavior_validate_dynamic_client_metadata`

**Inputs** client.

**Explicit results** “,\\n”.join(invalidation\_reasons) · no value.

**Local steps**

- Set invalidation\_reasons from list().
- If len(client.redirect\_uris) equals 0.
  - Evaluate invalidation\_reasons.append(“redirect\_uris is required”).
- If (client.grant\_types and not set(client.grant\_types).issubset(set(“authorization\_code”, “refresh\_token”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in client.grant\_types → not set(client.grant\_types).issubset(set(“authorization\_code”, “refresh\_token”)).
  - Evaluate invalidation\_reasons.append(“only 'authorization\_code' and 'refresh\_token' grant types are supported”).
- If (client.response\_types and not all(generator of rt equals “code” for rt drawn from client.response\_types)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in client.response\_types → not all(generator of rt equals “code” for rt drawn from client.response\_types).
  - Draw rt from client.response\_types.
  - Evaluate invalidation\_reasons.append(“only 'code' response\_type is supported”).
- If (not Platform.conf.developer\_mode and any(generator of not \_is\_secure\_redirect\_uri(uri) for uri drawn from client.redirect\_uris)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.developer\_mode → any(generator of not \_is\_secure\_redirect\_uri(uri) for uri drawn from client.redirect\_uris).
  - Draw uri from client.redirect\_uris.
  - Evaluate invalidation\_reasons.append(“redirect\_uris must be https”).
- If invalidation\_reasons.
  - Return “,\\n”.join(invalidation\_reasons).
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L951) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L190) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L886)

<a id="op-a139e03cc2bc5c"></a>
### Is secure redirect uri

`operation_foundation_integrations_utils_business_behavior_is_secure_redirect_resource_identifier`

**Inputs** uri.

**Declared result** bool.

**Explicit results** true · false · ipaddress.ip\_address((uri.host or empty text).strip(“&#91;&#93;”)).is\_loopback.

**Local steps**

- If uri.scheme equals “https”.
  - Return true.
- If uri.scheme differs from “http”.
  - Return false.
- If uri.host equals “localhost”.
  - Return true.
- Attempt the following.
  - Return ipaddress.ip\_address((uri.host or empty text).strip(“&#91;&#93;”)).is\_loopback.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in uri.host → empty text.
- On failure (ValueError).
  - Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L64) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L182) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L878)

<a id="op-87ee61a9a10060"></a>
### Create new oauth client

`operation_foundation_integrations_utils_business_behavior_create_new_delegated_authorization_client`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** client.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 9 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L63) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L178) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L874)

<a id="op-281ab47f7fb8cd"></a>
### Get oauth settings

`operation_foundation_integrations_utils_business_behavior_get_delegated_authorization_settings`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L2373) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L180) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L876)

## Service · V1

<a id="op-6c5080b7b99663"></a>
### Document list

`operation_foundation_application_interface_v1_business_behavior_document_list`

**Inputs** doctype.

**Explicit results** Platform.call(Platform.client.get\_list, doctype, expanded names Platform.form\_dict).

**Local steps**

- If Platform.form\_dict.get(“fields”).
  - Set Platform.form\_dict at “fields” from json.loads(Platform.form\_dict at “fields”).
- If Platform.form\_dict.get(“expand”).
  - Set Platform.form\_dict at “expand” from json.loads(Platform.form\_dict at “expand”).
- Evaluate Platform.form\_dict.setdefault(“limit\_page\_length”, (Platform.form\_dict.limit or Platform.form\_dict.limit\_page\_length or 20)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.form\_dict.limit → Platform.form\_dict.limit\_page\_length → 20.
- For each param in list(“as\_dict”, “debug”).
  - Set param\_val from Platform.form\_dict.get(param).
  - If param\_val is distinct from no value.
    - Set Platform.form\_dict at param from sbool(param\_val).
- Return Platform.call(Platform.client.get\_list, doctype, expanded names Platform.form\_dict).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L16) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L74) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L63)

<a id="op-f3ad81f5528cb6"></a>
### Handle rpc call

`operation_foundation_application_interface_v1_business_behavior_handle_rpc_call`

**Inputs** method.

**Explicit results** Platform.handler.handle().

**Local steps**

- Bind dependencies Platform.handler.
- Set method from method.split(“/”) at 0.
- Set Platform.form\_dict.cmd from method.
- Return Platform.handler.handle().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L477) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L79) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L68)

<a id="op-c18c5a2c1752e0"></a>
### Create doc

`operation_foundation_application_interface_v1_business_behavior_create_record`

**Inputs** doctype.

**State and service calls** call insert on Platform.new\_doc(doctype, expanded names data) · request new\_doc for doctype.

**Explicit results** Platform.new\_doc(doctype, expanded names data).insert().copy\_with\_fieldlevel\_read\_permissions().

**Local steps**

- Set data from get\_request\_form\_data().
- Evaluate data.pop(“doctype”, no value).
- Return Platform.new\_doc(doctype, expanded names data).insert().copy\_with\_fieldlevel\_read\_permissions().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L15) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L72) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L61)

<a id="op-06d233544e07b0"></a>
### Update doc

`operation_foundation_application_interface_v1_business_behavior_update_record`

**Inputs** doctype, name.

**Record and data access** resolve a document from doctype via get\_doc · resolve a document from doc.parenttype via get\_doc.

**State and service calls** call save on doc · call save on Platform.get\_doc(doc.parenttype, doc.parent).

**Explicit results** doc.copy\_with\_fieldlevel\_read\_permissions().

**Local steps**

- Set data from get\_request\_form\_data().
- Set doc from Platform.get\_doc(doctype, name, for\_update = true).
- Evaluate doc.check\_permission(“write”).
- If “flags” belongs to data.
  - Remove data at “flags”.
- Evaluate doc.update(data).
- Evaluate doc.save().
- If doc.get(“parenttype”).
  - Evaluate Platform.get\_doc(doc.parenttype, doc.parent).save().
- Return doc.copy\_with\_fieldlevel\_read\_permissions().

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L18) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L81) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L70)

<a id="op-522653eaaa3458"></a>
### Delete doc

`operation_foundation_application_interface_v1_business_behavior_delete_record`

**Inputs** doctype, name.

**State and service calls** request delete\_doc for doctype.

**Explicit results** “ok”.

**Local steps**

- Evaluate Platform.delete\_doc(doctype, name, ignore\_missing = false).
- Set Platform.response.http\_status\_code from 202.
- Return “ok”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L1017) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L73) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L62)

<a id="op-f1142c9d98ed04"></a>
### Read doc

`operation_foundation_application_interface_v1_business_behavior_read_record`

**Inputs** doctype, name.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** execute\_doc\_method(doctype, name) · doc\_dict · doc.

**Local steps**

- If “run\_method” belongs to Platform.form\_dict.
  - Return execute\_doc\_method(doctype, name).
- Set doc from Platform.get\_doc(doctype, name).
- Evaluate doc.check\_permission(“read”).
- Evaluate doc.apply\_fieldlevel\_read\_permissions().
- If sbool(Platform.form\_dict.get(“expand\_links”)).
  - Set doc\_dict from doc.as\_dict().
  - Evaluate get\_values\_for\_link\_and\_dynamic\_link\_fields(doc\_dict).
  - Evaluate get\_values\_for\_table\_and\_multiselect\_fields(doc\_dict).
  - Return doc\_dict.
- Return doc.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L1130) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L80) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L69)
