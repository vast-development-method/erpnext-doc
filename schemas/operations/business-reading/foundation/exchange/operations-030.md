# Integration and transport · operations 30

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Receive

<a id="op-62709fdc724efa"></a>
### Inbound Mail.get email fields

`operation_foundation_email_receive_business_behavior_inbound_mail_get_email_fields`

**Inputs** doctype.

**Wrappers, in declaration order** staticmethod.

**Explicit results** fields.

**Local steps**

- Set fields from Platform.\_dict().
- Set email\_fields from list(“subject\_field”, “sender\_field”, “sender\_name\_field”, “recipient\_account\_field”).
- Set meta from Platform.get\_meta(doctype).
- For each field in email\_fields.
  - If hasattr(meta, field).
    - Set fields at field from getattr(meta, field).
- Return fields.

**Values supplied outside this operation** selected callable from getattr(meta, field).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L4898) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1131) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1563)

<a id="op-f620bfaa230523"></a>
### Inbound Mail.get document

`operation_foundation_email_receive_business_behavior_inbound_mail_get_document`

**Inputs** self, doctype, name.

**Wrappers, in declaration order** staticmethod.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** Platform.get\_doc(doctype, name) · no value.

**Local steps**

- Attempt the following.
  - Return Platform.get\_doc(doctype, name).
- On failure (Platform.DoesNotExistError).
  - Return no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L5121) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1130) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1562)

<a id="op-c4f865a01387fa"></a>
### Inbound Mail.as dict

`operation_foundation_email_receive_business_behavior_inbound_mail_as_mapping`

**Inputs** self.

**Explicit results** mapping(“subject” → self.subject, “content” → self.get\_content(), “text\_content” → self.text\_content, “sent\_or\_received” → “Received”, …).

**Local steps**

- Return mapping(“subject” → self.subject, “content” → self.get\_content(), “text\_content” → self.text\_content, “sent\_or\_received” → “Received”, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.mail.get(“To”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.mail.get(“CC”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.mail.get(“BCC”) → empty text.
  - Value choice on self.attachments — true gives 1, false gives 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.seen\_status → 0.

**Methods declared on this owner** [get content](operations-029.md#op-718c78847274da).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L5228) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1125) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1557)

## Service · Server

<a id="op-7430d9d3d7789d"></a>
### Dispatch

`operation_foundation_binding_foundation_mcp_server_dispatch`

**Inputs** method, params, version.

**Declared result** dict.

**Explicit results** initialize(params) · mapping() · mapping(“supportedVersions” → list(protocol.SUPPORTED\_VERSIONS), “capabilities” → mapping(“tools” → mapping()), expand server\_configuration(), “ttlMs” → 3600000, …) · mapping(“tools” → tools.definitions(), “ttlMs” → 3600000, “cacheScope” → “private”) · tools.call(params).

**Explicit failure paths** McpError(METHOD\_NOT\_FOUND, “Unknown MCP method: {0}”.format(method), status = 404).

**Local steps**

- If (method equals “initialize” and version equals protocol.LEGACY\_VERSION).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in method equals “initialize” → version equals protocol.LEGACY\_VERSION.
  - Return initialize(params).
- If method equals “ping”.
  - Return mapping().
- If (method equals “server/discover” and version equals protocol.LATEST\_VERSION).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in method equals “server/discover” → version equals protocol.LATEST\_VERSION.
  - Return mapping(“supportedVersions” → list(protocol.SUPPORTED\_VERSIONS), “capabilities” → mapping(“tools” → mapping()), expand server\_configuration(), “ttlMs” → 3600000, …).
- If method belongs to tuple(“tools/list”, “tools/call”).
  - Bind dependencies tools.
  - If method equals “tools/list”.
    - Return mapping(“tools” → tools.definitions(), “ttlMs” → 3600000, “cacheScope” → “private”).
  - Return tools.call(params).
- Raise McpError(METHOD\_NOT\_FOUND, “Unknown MCP method: {0}”.format(method), status = 404).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L77) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1533) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1509)

<a id="op-350db27a043c5b"></a>
### Initialize

`operation_foundation_binding_foundation_mcp_server_initialize`

**Inputs** params.

**Declared result** dict.

**Explicit results** mapping(“protocolVersion” → protocol.LEGACY\_VERSION, “capabilities” → mapping(“tools” → mapping(“listChanged” → false)), expand server\_configuration()).

**Explicit failure paths** McpError(INVALID\_PARAMS, “initialize requires protocolVersion, capabilities and clientInfo”).

**Local steps**

- If (not isinstance(params.get(“protocolVersion”), str) or not isinstance(params.get(“capabilities”), dict) or not valid\_identity(params.get(“clientInfo”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(params.get(“protocolVersion”), str) → not isinstance(params.get(“capabilities”), dict) → not valid\_identity(params.get(“clientInfo”)).
  - Raise McpError(INVALID\_PARAMS, “initialize requires protocolVersion, capabilities and clientInfo”).
- Return mapping(“protocolVersion” → protocol.LEGACY\_VERSION, “capabilities” → mapping(“tools” → mapping(“listChanged” → false)), expand server\_configuration()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L78) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1534) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1510)

<a id="op-e8bf4c447b6e37"></a>
### Server configuration

`operation_foundation_binding_foundation_mcp_server_server_configuration`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(“serverInfo” → protocol.server\_info(), “instructions” → protocol.server\_instructions()).

**Local steps**

- Return mapping(“serverInfo” → protocol.server\_info(), “instructions” → protocol.server\_instructions()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L79) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1535) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1511)

<a id="op-917a2fcbc5b16b"></a>
### Valid identity

`operation_foundation_binding_foundation_mcp_server_valid_identity`

**Inputs** value.

**Declared result** bool.

**Explicit results** (isinstance(value, dict) and all(generator of isinstance(value.get(key), str) for key drawn from tuple(“name”, “version”))).

**Local steps**

- Return (isinstance(value, dict) and all(generator of isinstance(value.get(key), str) for key drawn from tuple(“name”, “version”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, dict) → all(generator of isinstance(value.get(key), str) for key drawn from tuple(“name”, “version”)).
  - Draw key from tuple(“name”, “version”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L80) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1536) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1512)

## Record · Slack webhook url

<a id="op-cc382384a8c76a"></a>
### Send slack message

`operation_foundation_integrations_record_definitions_slack_webhook_resource_address_business_behavior_send_slack_message`

**Inputs** webhook\_url, message, reference\_doctype, reference\_name.

**Record and data access** read “Slack Webhook URL” via get\_value.

**Explicit results** “error” · “success”.

**Local steps**

- Set data from mapping(“text” → message, “attachments” → list()).
- Set tuple(slack\_url, show\_link) from Platform.db.get\_value(“Slack Webhook URL”, webhook\_url, list(“webhook\_url”, “show\_document\_link”)).
- If show\_link.
  - Set doc\_url from get\_url\_to\_form(reference\_doctype, reference\_name).
  - Set link\_to\_doc from mapping(“fallback” → translated “See the document at {0}”.format(doc\_url), “actions” → list(mapping(“type” → “button”, “text” → translated “Go to the document”, “url” → doc\_url, “style” → “primary”))).
  - Evaluate data at “attachments”.append(link\_to\_doc).
- Set r from requests.post(slack\_url, data = json.dumps(data)).
- If not r.ok.
  - Set message from error\_messages.get(r.status\_code, r.status\_code).
  - Evaluate Platform.log\_error(message, translated “Slack Webhook Error”).
  - Return “error”.
- Return “success”.

**Values supplied outside this operation** service or queued work from requests.post(slack\_url, data = json.dumps(data)).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0254.json#L3270) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L69) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L795)

## Service · Smtp

<a id="op-bc1c2a094b14ba"></a>
### SMTPServer.initialize

`operation_foundation_email_mail_transfer_business_behavior_simple_mail_transfer_protocol_server_initialize`

**Inputs** self, server, login = no value, email\_account = no value, password = no value, port = no value, use\_tls = no value, use\_ssl = no value, use\_oauth = 0, access\_token = no value, timeout = (2 × 60).

**State and service calls** msgprint with translated “Email Account not setup. Please create a new Email Account from Settings &gt; Email Account”.

**Local steps**

- Set self.login from login.
- Set self.email\_account from email\_account.
- Set self.password from password.
- Set self.\_server from server.
- Set self.\_port from port.
- Set self.use\_tls from use\_tls.
- Set self.use\_ssl from use\_ssl.
- Set self.use\_oauth from use\_oauth.
- Set self.access\_token from access\_token.
- Set self.\_session from no value.
- Set self.timeout from timeout.
- If not self.server.
  - Evaluate Platform.msgprint(translated “Email Account not setup. Please create a new Email Account from Settings &gt; Email Account”, raise\_exception = Platform.OutgoingEmailError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L5740) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1076) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1508)

<a id="op-f7f10328ac9eed"></a>
### SMTPServer.port

`operation_foundation_email_mail_transfer_business_behavior_simple_mail_transfer_protocol_server_port`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** cint(port).

**Local steps**

- Set port from (self.\_port or (self.use\_ssl and 465) or (self.use\_tls and 587)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_port → (self.use\_ssl and 465) → (self.use\_tls and 587).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.use\_ssl → 465.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.use\_tls → 587.
- Return cint(port).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L6140) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1078) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1510)

<a id="op-8b801d4efdeac2"></a>
### SMTPServer.server

`operation_foundation_email_mail_transfer_business_behavior_simple_mail_transfer_protocol_server_server`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** cstr((self.\_server or empty text)).

**Local steps**

- Return cstr((self.\_server or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_server → empty text.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L6260) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1081) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1513)

<a id="op-997c6a4ed1d025"></a>
### SMTPServer.secure session

`operation_foundation_email_mail_transfer_business_behavior_simple_mail_transfer_protocol_server_secure_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, conn.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L6331) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1080) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1512)

<a id="op-16269cc2b3b1d6"></a>
### SMTPServer.session

`operation_foundation_email_mail_transfer_business_behavior_simple_mail_transfer_protocol_server_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** validation or user-notification service.

**Local structure** 7 condition or selection sites, 0 statement loops and 2 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L6438) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1082) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1514)

<a id="op-160a2c1af21cb7"></a>
### SMTPServer.enqueue connection closure

`operation_foundation_email_mail_transfer_business_behavior_simple_mail_transfer_protocol_server_enqueue_connection_closure`

**Inputs** self.

**Local steps**

- If (Platform.request and hasattr(Platform.request, “after\_response”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.request → hasattr(Platform.request, “after\_response”).
  - Evaluate Platform.request.after\_response.add(self.quit).
- Otherwise.
  - If Platform.job.
    - Evaluate Platform.job.after\_job.add(self.quit).
  - Otherwise.
    - If not Platform.in\_test.
      - Bind dependencies atexit.
      - Evaluate atexit.register(self.quit).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L7179) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1075) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1507)

<a id="op-70b2521f49a8f0"></a>
### SMTPServer.is session active

`operation_foundation_email_mail_transfer_business_behavior_simple_mail_transfer_protocol_server_is_session_active`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** Boolean false, a comparison result.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L7395) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1077) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1509)

<a id="op-b3a9bc967447fe"></a>
### SMTPServer.quit

`operation_foundation_email_mail_transfer_business_behavior_simple_mail_transfer_protocol_server_quit`

**Inputs** self.

**Local steps**

- Within suppress(TimeoutError).
  - If self.is\_session\_active().
    - Evaluate self.\_session.quit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is session active](operations-030.md#op-70b2521f49a8f0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L7620) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1079) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1511)

<a id="op-3bf144a02c4d49"></a>
### SMTPServer.throw invalid credentials exception

`operation_foundation_email_mail_transfer_business_behavior_simple_mail_transfer_protocol_server_throw_invalid_credentials_exception`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** cls, email\_account.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0238.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1083) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1515)

## Record · Social login key

[Record definition](../../../../data/record-types/social_login_key.json)

<a id="op-3f1ce063e073c7"></a>
### Social Login Key.autoname

`operation_foundation_integrations_record_definitions_social_login_key_business_behavior_social_login_key_autoname`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0254.json#L3841) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L71) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L797)

<a id="op-41245089df74ef"></a>
### Social Login Key.validate

`operation_foundation_integrations_record_definitions_social_login_key_business_behavior_social_login_key_validate`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 8 condition or selection sites, 0 statement loops and 2 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0254.json#L3913) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L74) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L800)

<a id="op-53cc23410c391c"></a>
### Social Login Key.set icon

`operation_foundation_integrations_record_definitions_social_login_key_business_behavior_social_login_key_set_icon`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0254.json#L4616) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L73) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L799)

<a id="op-cffbb5778b6b1e"></a>
### Social Login Key.get social login provider

`operation_foundation_integrations_record_definitions_social_login_key_business_behavior_social_login_key_get_social_login_provider`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, provider, initialize.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0254.json#L4853) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L72) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L798)

<a id="op-1f27db41547dd7"></a>
### Provider allows signup

`operation_foundation_integrations_record_definitions_social_login_key_business_behavior_provider_allows_signup`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** provider.

**Explicit result forms** a comparison result, a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0255.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L70) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L796)

## Record · Token cache

[Record definition](../../../../data/record-types/token_cache.json)

<a id="op-8af1aba157fd0b"></a>
### Token Cache.get auth header

`operation_foundation_integrations_record_definitions_token_cache_business_behavior_token_cache_get_authentication_header`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a structured result.

**Locally raised failures** DoesNotExistError.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0256.json#L1828) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L107) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L818)

<a id="op-5c1fbb06206bc8"></a>
### Token Cache.update data

`operation_foundation_integrations_record_definitions_token_cache_business_behavior_token_cache_update_data`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, data.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record mutation request, transaction control, validation or user-notification service.

**Local structure** 6 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0256.json#L1941) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L111) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L822)
