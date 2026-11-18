# Integration and transport · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Connected app

<a id="op-bf5146a735de2b"></a>
### Connected App.get openid configuration

`operation_foundation_integrations_record_definitions_connected_app_business_behavior_connected_application_get_openid_configuration`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L56) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1945) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L683)

<a id="op-0e5d9d19ef9e12"></a>
### Connected App.validate

`operation_foundation_integrations_record_definitions_connected_app_business_behavior_connected_application_validate`

**Inputs** self.

**Local steps**

- Set base\_url from Platform.utils.get\_url().
- Set callback\_path from (“/api/method/Platform.integrations.doctype.connected\_app.connected\_app.callback/” + self.name).
- Set self.redirect\_uri from urljoin(base\_url, callback\_path).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0247.json#L137) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1951) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L689)

<a id="op-7a305dcd2eb42b"></a>
### Connected App.get oauth2 session

`operation_foundation_integrations_record_definitions_connected_app_business_behavior_connected_application_get_delegated_authorization_2_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, user, init.

**Explicit result forms** the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0247.json#L264) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1944) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L682)

<a id="op-8f84ca55af15c2"></a>
### Connected App.initiate web application flow

`operation_foundation_integrations_record_definitions_connected_app_business_behavior_connected_application_initiate_web_application_flow`

**Inputs** self, user = no value, success\_uri = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Token Cache” · call save on token\_cache · commit.

**Explicit results** authorization\_url.

**Local steps**

- Set user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- If user differs from Platform.session.user.
  - Evaluate self.check\_permission(“write”).
- Set success\_uri from sanitize\_redirect(success\_uri) when getattr(Platform.local, “request”, no value), otherwise no value.
  - Value choice on getattr(Platform.local, “request”, no value) — true gives sanitize\_redirect(success\_uri), false gives no value.
- Set oauth from self.get\_oauth2\_session(user, init = true).
- Set query\_params from self.get\_query\_params().
- Set tuple(authorization\_url, state) from oauth.authorization\_url(self.authorization\_uri, expanded names query\_params).
- Set token\_cache from self.get\_token\_cache(user).
- If not token\_cache.
  - Set token\_cache from Platform.new\_doc(“Token Cache”).
  - Set token\_cache.user from user.
  - Set token\_cache.connected\_app from self.name.
- Set token\_cache.success\_uri from success\_uri.
- Set token\_cache.state from state.
- Evaluate token\_cache.save(ignore\_permissions = true).
- Evaluate Platform.db.commit().
- Return authorization\_url.

**Methods declared on this owner** [get oauth2 session](operations-006.md#op-7a305dcd2eb42b), [get query params](operations-006.md#op-06d2897629b11a), [get token cache](operations-006.md#op-aefe3a52886e9b).

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · selected callable from getattr(Platform.local, “request”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0247.json#L676) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1950) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L688)

<a id="op-d59d909c94f891"></a>
### Connected App.get user token

`operation_foundation_integrations_record_definitions_connected_app_business_behavior_connected_application_get_user_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, user, success\_uri.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0247.json#L1252) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1949) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L687)

<a id="op-aefe3a52886e9b"></a>
### Connected App.get token cache

`operation_foundation_integrations_record_definitions_connected_app_business_behavior_connected_application_get_token_cache`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, user.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0247.json#L1490) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1948) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L686)

<a id="op-5682f7c5f3577a"></a>
### Connected App.get scopes

`operation_foundation_integrations_record_definitions_connected_app_business_behavior_connected_application_get_scopes`

**Inputs** self.

**Explicit results** list of row.scope for row drawn from self.scopes.

**Local steps**

- Return list of row.scope for row drawn from self.scopes.
  - Draw row from self.scopes.

[Applicable decision contract](../../../foundation-decision-contracts/part-0247.json#L1659) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1947) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L685)

<a id="op-06d2897629b11a"></a>
### Connected App.get query params

`operation_foundation_integrations_record_definitions_connected_app_business_behavior_connected_application_get_query_parameters`

**Inputs** self.

**Explicit results** mapping of param.key → param.value for param drawn from self.query\_parameters.

**Local steps**

- Return mapping of param.key → param.value for param drawn from self.query\_parameters.
  - Draw param from self.query\_parameters.

[Applicable decision contract](../../../foundation-decision-contracts/part-0247.json#L1722) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1946) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L684)

<a id="op-1ccb694dae60f7"></a>
### Connected App.get active token

`operation_foundation_integrations_record_definitions_connected_app_business_behavior_connected_application_get_active_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, user.

**Explicit result forms** a value selected from the current context, no value.

**Observed service boundaries** diagnostic or audit logging, notification or queued-work request.

**Local structure** 4 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L55) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1942) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L680)

<a id="op-c69de0751cdfdd"></a>
### Connected App.get backend app token

`operation_foundation_integrations_record_definitions_connected_app_business_behavior_connected_application_get_backend_application_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, include\_client\_id.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record mutation request, transaction control.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0247.json#L2207) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1943) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L681)

<a id="op-b1e705257e04f8"></a>
### Callback

`operation_foundation_integrations_record_definitions_connected_app_business_behavior_callback`

**Inputs** code = no value, state = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”), allow\_guest = true).

**Record and data access** resolve a document from “Connected App” via get\_doc · resolve a document from “Token Cache” via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Invalid Parameters.” · validation helper — translated “Invalid token state! Check if the token has been created by the OAuth user.”.

**Local steps**

- If Platform.session.user equals “Guest”.
  - Set Platform.local.response at “type” from “redirect”.
  - Set Platform.local.response at “location” from (“/login?” + urlencode(mapping(“redirect-to” → Platform.request.url))).
  - Return no value.
- Set path from Platform.request.path at slice 1 to no value.split(“/”).
- If (len(path) differs from 4 or not path at 3).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(path) differs from 4 → not path at 3.
  - Call the validation error handler Platform.throw(translated “Invalid Parameters.”).
- Set connected\_app from Platform.get\_doc(“Connected App”, path at 3).
- Set token\_cache from Platform.get\_doc(“Token Cache”, ((connected\_app.name + “-”) + Platform.session.user)).
- If state differs from token\_cache.state.
  - Call the validation error handler Platform.throw(translated “Invalid token state! Check if the token has been created by the OAuth user.”).
- Set oauth\_session from connected\_app.get\_oauth2\_session(init = true).
- Set query\_params from connected\_app.get\_query\_params().
- Set token from oauth\_session.fetch\_token(connected\_app.token\_uri, code = code, client\_secret = connected\_app.get\_password(“client\_secret”), include\_client\_id = true, expanded names query\_params).
- Evaluate token\_cache.update\_data(token).
- Set Platform.local.response at “type” from “redirect”.
- Set Platform.local.response at “location” from (token\_cache.get(“success\_uri”) or connected\_app.get\_url()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in token\_cache.get(“success\_uri”) → connected\_app.get\_url().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0247.json#L2632) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1941) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L679)

<a id="op-19eb0a7bfa5f39"></a>
### Delete token cache

`operation_foundation_binding_foundation_integrations_doctype_connected_app_connected_app_delete_token_cache`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** name, modified.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L45) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1501) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1477)

<a id="op-86fb595a109719"></a>
### Has token

`operation_foundation_integrations_record_definitions_connected_app_business_behavior_has_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** connected\_app, connected\_user.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L57) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1952) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L690)

## Service · Discover

<a id="op-b839436edf561f"></a>
### Search doctypes

`operation_foundation_binding_foundation_mcp_tools_discover_search_doctypes`

**Inputs** query = no value, limit = SEARCH\_LIMIT.

**Declared result** list at str.

**Record and data access** read “DocType” via get\_all.

**Explicit results** Platform.get\_all(“DocType”, filters = mapping(“istable” → 0), or\_filters = list of tuple(“name”, “like”, formatted text %{text}%) for text drawn from (query or tuple()), pluck = “name”, order\_by = “name”, …).

**Local steps**

- If isinstance(query, str).
  - Set query from list(query).
- Return Platform.get\_all(“DocType”, filters = mapping(“istable” → 0), or\_filters = list of tuple(“name”, “like”, formatted text %{text}%) for text drawn from (query or tuple()), pluck = “name”, order\_by = “name”, …).
  - Draw text from (query or tuple()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query → tuple().

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L85) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1541) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1517)

<a id="op-5696e0788b4edf"></a>
### Search methods

`operation_foundation_binding_foundation_mcp_tools_discover_search_methods`

**Inputs** query.

**Declared result** list at dict.

**Explicit results** list of without(entry, “type”) for entry drawn from discovery.search(query) at “results”.

**Local steps**

- Return list of without(entry, “type”) for entry drawn from discovery.search(query) at “results”.
  - Draw entry from discovery.search(query) at “results”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L86) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1542) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1518)

<a id="op-74f9b7819b2347"></a>
### Method schema

`operation_foundation_binding_foundation_mcp_tools_discover_method_schema`

**Inputs** method, doctype = no value.

**Declared result** dict.

**Explicit results** without(discovery.doctype\_method(doctype, method), “type”, “kind”, “doctype”, …) · without(discovery.method(method), “type”, “kind”).

**Local steps**

- If doctype is distinct from no value.
  - Return without(discovery.doctype\_method(doctype, method), “type”, “kind”, “doctype”, …).
- Return without(discovery.method(method), “type”, “kind”).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L84) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1540) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1516)

<a id="op-d35f3ea5099ddd"></a>
### Document methods

`operation_foundation_binding_foundation_mcp_tools_discover_document_methods`

**Inputs** doctype.

**Declared result** list at dict.

**Explicit results** list of without(entry, “type”, “kind”, “doctype”) for entry drawn from discovery.doctype\_methods(doctype) at “methods”.

**Local steps**

- Return list of without(entry, “type”, “kind”, “doctype”) for entry drawn from discovery.doctype\_methods(doctype) at “methods”.
  - Draw entry from discovery.doctype\_methods(doctype) at “methods”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L82) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1538) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1514)

<a id="op-79dd85c892dbd6"></a>
### Doctype schema

`operation_foundation_binding_foundation_mcp_tools_discover_doctype_schema`

**Inputs** doctype.

**Declared result** dict.

**Explicit results** result.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set result from mapping(“module” → meta.module, “is\_submittable” → bool(meta.is\_submittable), “is\_single” → bool(meta.issingle), “is\_child\_table” → bool(meta.istable), …).
  - Draw field from meta.fields, keep a combination only if (field.fieldtype does not belong to LAYOUT\_FIELDTYPES).
  - Draw permission from PERMISSION\_TYPES.
  - Value choice on meta.istable — true gives false, false gives Platform.has\_permission(doctype, permission).
- Return result.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, permission).

**Boundaries to resolve** callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L81) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1537) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1513)

<a id="op-5698ffcc6a8785"></a>
### Field schema

`operation_foundation_binding_foundation_mcp_tools_discover_field_schema`

**Inputs** field.

**Declared result** dict.

**Explicit results** mapping of key → value for tuple(key, value) drawn from result.items() where value is distinct from no value.

**Local steps**

- Set result from mapping(“fieldname” → field.fieldname, “fieldtype” → field.fieldtype, “label” → field.label, “options” → field.options, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.permlevel → 0.
- Return mapping of key → value for tuple(key, value) drawn from result.items() where value is distinct from no value.
  - Draw tuple(key, value) from result.items(), keep a combination only if (value is distinct from no value).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L83) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1539) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1515)

<a id="op-e53ac1ae9d95c0"></a>
### Without

`operation_foundation_binding_foundation_mcp_tools_discover_without`

**Inputs** data, remaining positional values keys.

**Declared result** dict.

**Explicit results** mapping of key → value for tuple(key, value) drawn from data.items() where key does not belong to keys.

**Local steps**

- Return mapping of key → value for tuple(key, value) drawn from data.items() where key does not belong to keys.
  - Draw tuple(key, value) from data.items(), keep a combination only if (key does not belong to keys).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L87) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1543) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1519)

## Service · Discovery

<a id="op-9064a31faab99e"></a>
### Root

`operation_foundation_application_interface_discovery_business_behavior_root`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“type” → “discovery”, “resources” → mapping(“methods” → len(method\_index), “doctype\_methods” → len(doctype\_method\_index)), “links” → mapping(“self” → “/api/v2/discovery”, “search” → “/api/v2/discov ….

**Local steps**

- Evaluate Platform.only\_for(SYSTEM\_USER\_ROLE).
- Set method\_index from \_method\_index().
- Set doctype\_method\_index from \_doctype\_method\_index().
- Return mapping(“type” → “discovery”, “resources” → mapping(“methods” → len(method\_index), “doctype\_methods” → len(doctype\_method\_index)), “links” → mapping(“self” → “/api/v2/discovery”, “search” → “/api/v2/discov ….

**Values supplied outside this operation** effective access from Platform.only\_for(SYSTEM\_USER\_ROLE).

**Boundaries to resolve** callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L11) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L63) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L52)

<a id="op-2bfb272d2f62ee"></a>
### Search

`operation_foundation_application_interface_discovery_business_behavior_search`

**Inputs** q = no value.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“query” → (q or empty text), “results” → entries at slice no value to 50) · mapping(“query” → (q or empty text), “results” → matches at slice no value to 50).

**Local steps**

- Evaluate Platform.only\_for(SYSTEM\_USER\_ROLE).
- Set query from (q or empty text).strip().lower().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in q → empty text.
- Set index from \_search\_index().
- Set entries from list of entry for tuple(entry, \_haystack) drawn from index.
  - Draw tuple(entry, \_haystack) from index.
- If not query.
  - Return mapping(“query” → (q or empty text), “results” → entries at slice no value to 50).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in q → empty text.
- Set tokens from list of token for token drawn from query.split() where token.
  - Draw token from query.split(), keep a combination only if (token).
- Set matches from list().
- For each tuple(entry, haystack) in index.
  - If all(generator of token belongs to haystack for token drawn from tokens).
    - Draw token from tokens.
    - Evaluate matches.append(entry).
- Return mapping(“query” → (q or empty text), “results” → matches at slice no value to 50).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in q → empty text.

**Values supplied outside this operation** effective access from Platform.only\_for(SYSTEM\_USER\_ROLE).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L12) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L64) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L53)

<a id="op-d3a412d0b40af1"></a>
### Methods

`operation_foundation_application_interface_discovery_business_behavior_methods`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“type” → “method\_index”, “methods” → \_method\_index()).

**Local steps**

- Evaluate Platform.only\_for(SYSTEM\_USER\_ROLE).
- Return mapping(“type” → “method\_index”, “methods” → \_method\_index()).

**Values supplied outside this operation** effective access from Platform.only\_for(SYSTEM\_USER\_ROLE).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L8) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L55) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L44)

<a id="op-8ded5f08d4d408"></a>
### Method

`operation_foundation_application_interface_discovery_business_behavior_method`

**Inputs** method.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“type” → “method”, “kind” → “rpc”, “path” → method, “name” → server\_script, …) · \_method\_document(method, fn).

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Method {0} is not available for discovery”.format(method).

**Local steps**

- Evaluate Platform.only\_for(SYSTEM\_USER\_ROLE).
- Set method from Platform.override\_whitelisted\_method(method).
- Set server\_script from \_get\_api\_server\_scripts().get(method).
- If (server\_script and Platform.has\_permission(“Server Script”, “read”, doc = server\_script)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in server\_script → Platform.has\_permission(“Server Script”, “read”, doc = server\_script).
  - Return mapping(“type” → “method”, “kind” → “rpc”, “path” → method, “name” → server\_script, …).
- Set fn from \_get\_whitelisted\_method(method).
- If not fn.
  - Call the validation error handler Platform.throw(translated “Method {0} is not available for discovery”.format(method), Platform.DoesNotExistError).
- Return \_method\_document(method, fn).

**Values supplied outside this operation** effective access from Platform.only\_for(SYSTEM\_USER\_ROLE), Platform.has\_permission(“Server Script”, “read”, doc = server\_script).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L7) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L48) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L37)
