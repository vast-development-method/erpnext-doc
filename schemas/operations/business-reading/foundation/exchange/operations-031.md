# Integration and transport · operations 31

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Token cache

[Record definition](../../../../data/record-types/token_cache.json)

<a id="op-8b5e4285373ac3"></a>
### Token Cache.get expires in

`operation_foundation_integrations_record_definitions_token_cache_business_behavior_token_cache_get_expires_in`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0256.json#L2650) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L108) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L819)

<a id="op-75cc1967b3b66d"></a>
### Token Cache.is expired

`operation_foundation_integrations_record_definitions_token_cache_business_behavior_token_cache_is_expired`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a comparison result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0256.json#L2913) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L110) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L821)

<a id="op-9248a5e464329c"></a>
### Token Cache.get json

`operation_foundation_integrations_record_definitions_token_cache_business_behavior_token_cache_get_structured_data`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0256.json#L2976) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L109) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L820)

## Service · Tools

<a id="op-7ae762df5091c2"></a>
### Compact Json Schema.generate

`operation_foundation_binding_foundation_mcp_tools_init_compactjsonschema_generate`

**Inputs** self, schema, mode = “validation”.

**Explicit results** json\_schema.

**Local steps**

- Set json\_schema from super().generate(schema, mode).
- Evaluate json\_schema.pop(“title”, no value).
- Return json\_schema.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L98) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1554) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1530)

<a id="op-d37bc6789a3baf"></a>
### Compact Json Schema.field title should be set

`operation_foundation_binding_foundation_mcp_tools_init_compactjsonschema_field_title_should_be_set`

**Inputs** self, schema.

**Declared result** bool.

**Explicit results** false.

**Local steps**

- Return false.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L97) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1553) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1529)

<a id="op-8fc8c2dfe34b1b"></a>
### Compact Json Schema.nullable schema

`operation_foundation_binding_foundation_mcp_tools_init_compactjsonschema_nullable_schema`

**Inputs** self, schema.

**Explicit results** self.generate\_inner(schema at “schema”).

**Local steps**

- Return self.generate\_inner(schema at “schema”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L100) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1556) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1532)

<a id="op-0562de16175e97"></a>
### Compact Json Schema.default schema

`operation_foundation_binding_foundation_mcp_tools_init_compactjsonschema_default_schema`

**Inputs** self, schema.

**Explicit results** json\_schema.

**Local steps**

- Set json\_schema from super().default\_schema(schema).
- If json\_schema.get(“default”, ellipsis) is identical to no value.
  - Remove json\_schema at “default”.
- Return json\_schema.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L95) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1551) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1527)

<a id="op-0def34aa2b1b9b"></a>
### Compact Json Schema.list schema

`operation_foundation_binding_foundation_mcp_tools_init_compactjsonschema_list_schema`

**Inputs** self, schema.

**Explicit results** json\_schema.

**Local steps**

- Set json\_schema from super().list\_schema(schema).
- If json\_schema.get(“items”) equals mapping().
  - Remove json\_schema at “items”.
- Return json\_schema.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L99) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1555) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1531)

<a id="op-5aa006bb55771a"></a>
### Compact Json Schema.dict schema

`operation_foundation_binding_foundation_mcp_tools_init_compactjsonschema_dict_schema`

**Inputs** self, schema.

**Explicit results** json\_schema.

**Local steps**

- Set json\_schema from super().dict\_schema(schema).
- If json\_schema.get(“additionalProperties”) is identical to true.
  - Remove json\_schema at “additionalProperties”.
- Return json\_schema.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L96) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1552) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1528)

<a id="op-371c7ba9d83ae5"></a>
### Tool.input schema

`operation_foundation_binding_foundation_mcp_tools_init_tool_input_schema`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** dict.

**Explicit results** self.arguments.model\_json\_schema(schema\_generator = CompactJsonSchema).

**Local steps**

- Return self.arguments.model\_json\_schema(schema\_generator = CompactJsonSchema).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L107) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1563) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1539)

<a id="op-c7462e1d909d66"></a>
### Tool.definition

`operation_foundation_binding_foundation_mcp_tools_init_tool_definition`

**Inputs** self.

**Declared result** dict.

**Explicit results** definition.

**Local steps**

- Set definition from mapping(“name” → self.name, “inputSchema” → self.input\_schema, “annotations” → self.annotations).
- If self.description.
  - Set definition at “description” from self.description.
- Return definition.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L106) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1562) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1538)

<a id="op-eacc4ad1dd96a2"></a>
### Registry

`operation_foundation_binding_foundation_mcp_tools_init_registry`

**Inputs** no declared parameters.

**Declared result** tuple at tuple(Tool, ellipsis).

**Explicit results** tuple(SEARCH\_DOCTYPES, GET\_DOCTYPE\_SCHEMA, SEARCH\_METHODS, GET\_METHOD\_SCHEMA, …).

**Local steps**

- Bind dependencies GET\_DOCTYPE\_SCHEMA, GET\_METHOD\_SCHEMA, LIST\_DOCUMENT\_METHODS, SEARCH\_DOCTYPES, SEARCH\_METHODS.
- Bind dependencies COUNT\_DOCUMENTS, CREATE\_DOCUMENT, DELETE\_DOCUMENT, GET\_DOCUMENT, LIST\_DOCUMENTS, UPDATE\_DOCUMENT.
- Bind dependencies CALL\_DOCUMENT\_METHOD, CALL\_METHOD.
- Return tuple(SEARCH\_DOCTYPES, GET\_DOCTYPE\_SCHEMA, SEARCH\_METHODS, GET\_METHOD\_SCHEMA, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L104) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1560) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1536)

<a id="op-ba7d0c192caca2"></a>
### Definitions

`operation_foundation_binding_foundation_mcp_tools_init_definitions`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list of tool.definition() for tool drawn from registry().

**Local steps**

- Return list of tool.definition() for tool drawn from registry().
  - Draw tool from registry().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L101) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1557) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1533)

<a id="op-e3f067bac1ed36"></a>
### Call

`operation_foundation_binding_foundation_mcp_tools_init_call`

**Inputs** params.

**Declared result** dict.

**Explicit results** error\_result(validation\_message(error)) · success\_result(tool.handler(expanded names Platform.form\_dict)).

**Explicit failure paths** McpError(INVALID\_PARAMS, “Tool name must be a string”) · McpError(METHOD\_NOT\_FOUND, “Unknown MCP tool: {0}”.format(name), status = 404).

**Local steps**

- Set name from params.get(“name”).
- If not isinstance(name, str).
  - Raise McpError(INVALID\_PARAMS, “Tool name must be a string”).
- Set tool from next(generator of tool for tool drawn from registry() where tool.name equals name, no value).
  - Draw tool from registry(), keep a combination only if (tool.name equals name).
- If tool is identical to no value.
  - Raise McpError(METHOD\_NOT\_FOUND, “Unknown MCP tool: {0}”.format(name), status = 404).
- Evaluate add\_data\_to\_monitor(mcp\_tool = name).
- Attempt the following.
  - Set arguments from tool.arguments.model\_validate(params.get(“arguments”, mapping())).
- On failure (ValidationError) bound to error.
  - Return error\_result(validation\_message(error)).
- Within form\_dict(arguments.model\_dump()).
  - Return success\_result(tool.handler(expanded names Platform.form\_dict)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L94) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1550) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1526)

<a id="op-6d346cb9af6623"></a>
### Form dict

`operation_foundation_binding_foundation_mcp_tools_init_form_dict`

**Inputs** arguments.

**Wrappers, in declaration order** contextmanager.

**Declared result** Iterator at dict.

**Local steps**

- Set original\_arguments from Platform.local.form\_dict.
- Set original\_response from Platform.local.response.
- Set Platform.local.form\_dict from Platform.\_dict(arguments).
- Set Platform.local.response from Platform.\_dict(mapping(“docs” → list())).
- Attempt the following.
  - yield Platform.local.form\_dict.
- On exit, including pending return or failure.
  - Set Platform.local.form\_dict from original\_arguments.
  - Set Platform.local.response from original\_response.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L103) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1559) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1535)

<a id="op-f7aaf2c931c72a"></a>
### Success result

`operation_foundation_binding_foundation_mcp_tools_init_success_result`

**Inputs** value.

**Declared result** dict.

**Explicit results** mapping(“content” → list(mapping(“type” → “text”, “text” → text)), “structuredContent” → json.loads(text), “isError” → false).

**Local steps**

- Set structured from value when isinstance(value, dict), otherwise mapping(“result” → value).
  - Value choice on isinstance(value, dict) — true gives value, false gives mapping(“result” → value).
- Set text from json.dumps(structured, default = json\_handler, allow\_nan = false).
- Return mapping(“content” → list(mapping(“type” → “text”, “text” → text)), “structuredContent” → json.loads(text), “isError” → false).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L105) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1561) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1537)

<a id="op-9dc0d8438b315e"></a>
### Validation message

`operation_foundation_binding_foundation_mcp_tools_init_validation_message`

**Inputs** error.

**Declared result** str.

**Explicit results** “Invalid tool arguments: {0}”.format(“; ”.join(issues)).

**Local steps**

- Set issues from list().
- For each issue in error.errors(include\_input = false, include\_url = false, include\_context = false).
  - Set location from (“.”.join(generator of str(part) for part drawn from issue at “loc”) or “arguments”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in “.”.join(generator of str(part) for part drawn from issue at “loc”) → “arguments”.
    - Draw part from issue at “loc”.
  - Evaluate issues.append(formatted text {location}: {issue at “msg”}).
- Return “Invalid tool arguments: {0}”.format(“; ”.join(issues)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L108) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1564) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1540)

<a id="op-f1350e5d892bcd"></a>
### Error result

`operation_foundation_binding_foundation_mcp_tools_init_error_result`

**Inputs** message.

**Declared result** dict.

**Explicit results** mapping(“content” → list(mapping(“type” → “text”, “text” → strip\_html(message).strip())), “isError” → true).

**Local steps**

- Evaluate Platform.clear\_messages().
- Return mapping(“content” → list(mapping(“type” → “text”, “text” → strip\_html(message).strip())), “isError” → true).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L102) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1558) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1534)

## Service · Transport

<a id="op-a009da5323e173"></a>
### Handle request

`operation_foundation_binding_foundation_mcp_transport_handle_request`

**Inputs** request.

**Declared result** Response.

**Explicit results** Response(status = 202) · json\_response(protocol.result\_envelope(context.id, result, context.version)).

**Explicit failure paths** McpError(protocol.INVALID\_REQUEST, “Only POST is supported”, status = 405) · McpError(protocol.INVALID\_REQUEST, “Authentication required”, status = 401) · McpError(protocol.INVALID\_REQUEST, “MCP is only available to desk users”, status = 403) · McpError(protocol.INVALID\_REQUEST, “Content-Type must be application/json”, status = 415) · McpError(protocol.INVALID\_REQUEST, “Accept must allow application/json”, status = 406).

**Local steps**

- Set context, Platform.local.mcp\_request from RequestContext().
- If request.method differs from “POST”.
  - Raise McpError(protocol.INVALID\_REQUEST, “Only POST is supported”, status = 405).
- Evaluate check\_origin(request).
- If Platform.session.user equals “Guest”.
  - Raise McpError(protocol.INVALID\_REQUEST, “Authentication required”, status = 401).
- If SYSTEM\_USER\_ROLE does not belong to Platform.get\_roles().
  - Raise McpError(protocol.INVALID\_REQUEST, “MCP is only available to desk users”, status = 403).
- If not request.is\_json.
  - Raise McpError(protocol.INVALID\_REQUEST, “Content-Type must be application/json”, status = 415).
- If not request.accept\_mimetypes at “application/json”.
  - Raise McpError(protocol.INVALID\_REQUEST, “Accept must allow application/json”, status = 406).
- Set payload from parse\_body(request).
- Set context.id from payload.get(“id”).
- Set params from payload.get(“params”, mapping()).
- Set context.version from request\_version(request, params).
- If context.version equals protocol.LATEST\_VERSION.
  - Evaluate check\_headers(request, payload, params).
  - Evaluate check\_metadata(params).
- If “id” does not belong to payload.
  - Return Response(status = 202).
- Set context.method from payload at “method”.
- Set result from server.dispatch(context.method, params, context.version).
- Return json\_response(protocol.result\_envelope(context.id, result, context.version)).

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L119) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1575) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1551)

<a id="op-b3e1d39e31dab0"></a>
### Error response

`operation_foundation_binding_foundation_mcp_transport_error_response`

**Inputs** error.

**Declared result** Response.

**Explicit results** json\_response(protocol.result\_envelope(context.id, result, context.version)) · response.

**Local steps**

- Set context from Platform.local.mcp\_request.
- If not isinstance(error, McpError).
  - If context.method equals “tools/call”.
    - Bind dependencies error\_result.
    - Set result from error\_result((str(error) or type(error).\_\_name\_\_)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in str(error) → type(error).\_\_name\_\_.
    - Return json\_response(protocol.result\_envelope(context.id, result, context.version)).
  - Set status from getattr(error, “http\_status\_code”, 500).
  - Set message from str(error) when (status &lt; 500 and str(error)), otherwise “Internal error”.
    - Value choice on (status &lt; 500 and str(error)) — true gives str(error), false gives “Internal error”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in status &lt; 500 → str(error).
  - Set error from McpError(protocol.INTERNAL\_ERROR, message, status = status).
- Set response from json\_response(protocol.error\_envelope(context.id, error, context.version), error.http\_status\_code).
- If error.http\_status\_code equals 405.
  - Set response.headers at “Allow” from “POST”.
- Return response.

**Values supplied outside this operation** selected callable from getattr(error, “http\_status\_code”, 500).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L118) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1574) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1550)

<a id="op-b56a3a3da1374b"></a>
### Parse body

`operation_foundation_binding_foundation_mcp_transport_parse_body`

**Inputs** request.

**Declared result** dict at tuple(str, Any).

**Explicit results** payload.

**Explicit failure paths** McpError(protocol.PARSE\_ERROR, “Body is not valid JSON”) · McpError(protocol.INVALID\_REQUEST, “Body must be one JSON-RPC request or notification”) · McpError(protocol.INVALID\_REQUEST, “Request id must be a string or integer”).

**Local steps**

- Attempt the following.
  - Set payload from orjson.loads(request.get\_data()).
- On failure (tuple(ValueError, UnicodeDecodeError)).
  - Raise McpError(protocol.PARSE\_ERROR, “Body is not valid JSON”) with cause no value.
- If (not isinstance(payload, dict) or payload.get(“jsonrpc”) differs from “2.0” or not isinstance(payload.get(“method”), str) or not isinstance(payload.get(“params”, mapping()), dict) or “result” belongs to pa ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(payload, dict) → payload.get(“jsonrpc”) differs from “2.0” → not isinstance(payload.get(“method”), str) → not isinstance(payload.get(“params”, mapping()), dict) → “result” belongs to payload → “error” belongs to payload.
  - Raise McpError(protocol.INVALID\_REQUEST, “Body must be one JSON-RPC request or notification”).
- If (“id” belongs to payload and type(payload at “id”) does not belong to tuple(str, int)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “id” belongs to payload → type(payload at “id”) does not belong to tuple(str, int).
  - Raise McpError(protocol.INVALID\_REQUEST, “Request id must be a string or integer”).
- Return payload.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L121) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1577) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1553)

<a id="op-e2dc2b4f6f8aaf"></a>
### Request version

`operation_foundation_binding_foundation_mcp_transport_request_version`

**Inputs** request, params.

**Declared result** str.

**Explicit results** protocol.LEGACY\_VERSION · version.

**Explicit failure paths** McpError(protocol.HEADER\_MISMATCH, “MCP-Protocol-Version header is required”) · McpError(protocol.UNSUPPORTED\_VERSION, “Unsupported MCP protocol version”, data = mapping(“supported” → list(protocol.SUPPORTED\_VERSIONS), “requested” → version)).

**Local steps**

- Set version from request.headers.get(“MCP-Protocol-Version”).
- Set meta from params.get(“\_meta”, mapping()).
- If not version.
  - If (isinstance(meta, dict) and meta.get(protocol.META\_VERSION) equals protocol.LATEST\_VERSION).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(meta, dict) → meta.get(protocol.META\_VERSION) equals protocol.LATEST\_VERSION.
    - Raise McpError(protocol.HEADER\_MISMATCH, “MCP-Protocol-Version header is required”).
  - Return protocol.LEGACY\_VERSION.
- If version does not belong to protocol.SUPPORTED\_VERSIONS.
  - Raise McpError(protocol.UNSUPPORTED\_VERSION, “Unsupported MCP protocol version”, data = mapping(“supported” → list(protocol.SUPPORTED\_VERSIONS), “requested” → version)).
- Return version.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L122) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1578) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1554)

<a id="op-101d8be2baefdf"></a>
### Check headers

`operation_foundation_binding_foundation_mcp_transport_check_headers`

**Inputs** request, payload, params.

**Declared result** no value.

**Explicit failure paths** McpError(protocol.HEADER\_MISMATCH, “Protocol version header must match request metadata”) · McpError(protocol.HEADER\_MISMATCH, “Mcp-Method header must match method”) · McpError(protocol.HEADER\_MISMATCH, “Mcp-Name header must match the tool name”).

**Local steps**

- Set meta from params.get(“\_meta”).
- If (not isinstance(meta, dict) or request.headers at “MCP-Protocol-Version” differs from meta.get(protocol.META\_VERSION)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(meta, dict) → request.headers at “MCP-Protocol-Version” differs from meta.get(protocol.META\_VERSION).
  - Raise McpError(protocol.HEADER\_MISMATCH, “Protocol version header must match request metadata”).
- If request.headers.get(“Mcp-Method”) differs from payload at “method”.
  - Raise McpError(protocol.HEADER\_MISMATCH, “Mcp-Method header must match method”).
- If payload at “method” equals “tools/call”.
  - If (decode\_name(request.headers.get(“Mcp-Name”)) differs from params.get(“name”) or “name” does not belong to params).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in decode\_name(request.headers.get(“Mcp-Name”)) differs from params.get(“name”) → “name” does not belong to params.
    - Raise McpError(protocol.HEADER\_MISMATCH, “Mcp-Name header must match the tool name”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L114) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1570) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1546)

<a id="op-2ed6cbb973eead"></a>
### Check metadata

`operation_foundation_binding_foundation_mcp_transport_check_metadata`

**Inputs** params.

**Declared result** no value.

**Explicit failure paths** McpError(protocol.INVALID\_PARAMS, “Client capabilities must be provided as an object”) · McpError(protocol.INVALID\_PARAMS, “Client identity requires a name and version”).

**Local steps**

- Set meta from params at “\_meta”.
- If not isinstance(meta.get(protocol.META\_CAPABILITIES), dict).
  - Raise McpError(protocol.INVALID\_PARAMS, “Client capabilities must be provided as an object”).
- If (protocol.META\_CLIENT belongs to meta and not server.valid\_identity(meta at protocol.META\_CLIENT)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in protocol.META\_CLIENT belongs to meta → not server.valid\_identity(meta at protocol.META\_CLIENT).
  - Raise McpError(protocol.INVALID\_PARAMS, “Client identity requires a name and version”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L115) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1571) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1547)
