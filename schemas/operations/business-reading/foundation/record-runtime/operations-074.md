# Record lifecycle and persistence · operations 74

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Platform

<a id="op-26b9f04c8bb28c"></a>
### Respond as web page

`operation_foundation_binding_foundation_init_respond_as_web_page`

**Inputs** title, html, success = no value, http\_status\_code = no value, context = no value, indicator\_color = no value, primary\_action = “/”, primary\_label = no value, fullpage = false, width = no value, template = “message”.

**Local steps**

- Set local.message\_title from title.
- Set local.message from html.
- Set local.response at “type” from “page”.
- Set local.response at “route” from template.
- Set local.no\_cache from 1.
- If http\_status\_code.
  - Set local.response at “http\_status\_code” from http\_status\_code.
- If not context.
  - Set context from mapping().
- If not indicator\_color.
  - If success.
    - Set indicator\_color from “green”.
  - Otherwise.
    - If (http\_status\_code and http\_status\_code &gt; 300).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in http\_status\_code → http\_status\_code &gt; 300.
      - Set indicator\_color from “red”.
    - Otherwise.
      - Set indicator\_color from “blue”.
- Set context at “indicator\_color” from indicator\_color.
- Set context at “primary\_label” from primary\_label.
- Set context at “primary\_action” from primary\_action.
- Set context at “error\_code” from http\_status\_code.
- Set context at “fullpage” from fullpage.
- If width.
  - Set context at “card\_width” from width.
- Set local.response at “context” from context.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L40) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1496) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1472)

<a id="op-05a4db6009dbab"></a>
### Redirect

`operation_foundation_initialize_business_behavior_redirect`

**Inputs** url.

**Explicit failure paths** Redirect.

**Local steps**

- Bind dependencies Redirect.
- Set flags.redirect\_location from url.
- Raise Redirect.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L7444) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1749) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L491)

<a id="op-730571384f4ece"></a>
### Redirect to message

`operation_foundation_binding_foundation_init_redirect_to_message`

**Inputs** title, html, http\_status\_code = no value, context = no value, indicator\_color = no value.

**Explicit results** location.

**Local steps**

- Set message\_id from generate\_hash(length = 8).
- Set message from mapping(“context” → (context or mapping()), “http\_status\_code” → (http\_status\_code or 200)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in http\_status\_code → 200.
- Evaluate message at “context”.update(mapping(“header” → title, “title” → title, “message” → html)).
- If indicator\_color.
  - Evaluate message at “context”.update(mapping(“indicator\_color” → indicator\_color)).
- Evaluate cache.set\_value(formatted text message\_id:{message\_id}, message, expires\_in\_sec = 60).
- Set location from formatted text /message?id={message\_id}.
- If not getattr(local, “is\_ajax”, false).
  - Set local.response at “type” from “redirect”.
  - Set local.response at “location” from location.
- Otherwise.
  - Return location.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from generate\_hash(length = 8) · selected callable from getattr(local, “is\_ajax”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L39) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1495) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1471)

<a id="op-c628e04a27d865"></a>
### Build match conditions

`operation_foundation_initialize_business_behavior_build_match_conditions`

**Inputs** doctype, as\_condition = true.

**Explicit results** Platform.desk.reportview.build\_match\_conditions(doctype, as\_condition = as\_condition).

**Local steps**

- Bind dependencies Platform.desk.reportview.
- Return Platform.desk.reportview.build\_match\_conditions(doctype, as\_condition = as\_condition).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L7513) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1698) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L441)

<a id="op-c4d853b13437cf"></a>
### Get list

`operation_foundation_initialize_business_behavior_get_list`

**Inputs** doctype, remaining positional values args, remaining named values kwargs.

**Explicit results** Platform.model.qb\_query.DatabaseQuery(doctype).execute(expanded args, expanded names kwargs).

**Local steps**

- Bind dependencies Platform.model.qb\_query.
- Return Platform.model.qb\_query.DatabaseQuery(doctype).execute(expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L7606) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1712) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L455)

<a id="op-01c1db210d16e1"></a>
### Get all

`operation_foundation_initialize_business_behavior_get_all`

**Inputs** doctype, remaining positional values args, remaining named values kwargs.

**Explicit results** get\_list(doctype, expanded args, expanded names kwargs).

**Local steps**

- Set kwargs at “ignore\_permissions” from true.
- If “limit\_page\_length” does not belong to kwargs.
  - Set kwargs at “limit\_page\_length” from 0.
- Return get\_list(doctype, expanded args, expanded names kwargs).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L7716) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1707) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L450)

<a id="op-5166288842666f"></a>
### Get value

`operation_foundation_initialize_business_behavior_get_value`

**Inputs** remaining positional values args, remaining named values kwargs.

**Explicit results** local.db.get\_value(expanded args, expanded names kwargs).

**Local steps**

- Return local.db.get\_value(expanded args, expanded names kwargs).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L7856) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1722) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L465)

<a id="op-01e063ffe20f71"></a>
### As json

`operation_foundation_initialize_business_behavior_as_structured_data`

**Inputs** obj, indent = 1, separators = no value, ensure\_ascii = true.

**Declared result** str.

**Explicit results** json.dumps(obj, indent = indent, sort\_keys = true, default = json\_handler, separators = separators, …) · json.dumps(sorted\_obj, indent = indent, default = json\_handler, separators = separators, ensure\_ascii = ensure\_ascii).

**Local steps**

- Bind dependencies json\_handler.
- If separators is identical to no value.
  - Set separators from tuple(“,”, “: ”).
- Attempt the following.
  - Return json.dumps(obj, indent = indent, sort\_keys = true, default = json\_handler, separators = separators, …).
- On failure (TypeError).
  - Set sorted\_obj from dict(sorted(obj.items(), key = deferred anonymous expression)).
  - Return json.dumps(sorted\_obj, indent = indent, default = json\_handler, separators = separators, ensure\_ascii = ensure\_ascii).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1697) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L440)

<a id="op-e664a55883fc1b"></a>
### Are emails muted

`operation_foundation_initialize_business_behavior_are_emails_muted`

**Inputs** no declared parameters.

**Explicit results** (flags.mute\_emails or cint(conf.get(“mute\_emails”, 0))).

**Local steps**

- Return (flags.mute\_emails or cint(conf.get(“mute\_emails”, 0))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flags.mute\_emails → cint(conf.get(“mute\_emails”, 0)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L376) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1696) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L439)

<a id="op-cddb61427db70e"></a>
### Task

`operation_foundation_initialize_business_behavior_task`

**Inputs** remaining named values task\_kwargs.

**Explicit results** decorator\_task.

**Local steps**

- Bind local operation decorator\_task for subsequent calls.
- Return decorator\_task.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L30) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1757) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L499)

<a id="op-3f97fb5260f0f0"></a>
### Task.decorator task

`operation_foundation_initialize_business_behavior_task_decorator_task`

**Inputs** f.

**Explicit results** f.

**Local steps**

- Set f.enqueue from deferred anonymous expression.
- Return f.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L31) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1758) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L500)

<a id="op-e2edbeab06b237"></a>
### Get doctype app

`operation_foundation_initialize_business_behavior_get_record_type_application`

**Inputs** doctype.

**Explicit results** local\_cache(“doctype\_app”, doctype, generator = \_get\_doctype\_app).

**Local steps**

- Bind local operation \_get\_doctype\_app for subsequent calls.
- Return local\_cache(“doctype\_app”, doctype, generator = \_get\_doctype\_app).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L678) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1717) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L460)

<a id="op-f658e2c25ee945"></a>
### Get doctype app.get doctype app

`operation_foundation_initialize_business_behavior_get_record_type_application_get_record_type_application`

**Inputs** no declared parameters.

**Explicit results** local.module\_app at scrub(doctype\_module).

**Local steps**

- Set doctype\_module from local.db.get\_value(“DocType”, doctype, “module”).
- Return local.module\_app at scrub(doctype\_module).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L838) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1718) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L461)

<a id="op-3344b10f2b279b"></a>
### Logger

`operation_foundation_initialize_business_behavior_logger`

**Inputs** module = no value, with\_more\_info = false, allow\_site = true, filter = no value, max\_size = 100000, file\_count = 20.

**Declared result** “Logger”.

**Explicit results** get\_logger(module = module, with\_more\_info = with\_more\_info, allow\_site = allow\_site, filter = filter, …).

**Local steps**

- Bind dependencies get\_logger.
- Return get\_logger(module = module, with\_more\_info = with\_more\_info, allow\_site = allow\_site, filter = filter, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L945) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1739) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L481)

<a id="op-bfdc01bb4ed113"></a>
### Get desk link

`operation_foundation_initialize_business_behavior_get_desk_link`

**Inputs** doctype, name, show\_title\_with\_name = false, open\_in\_new\_tab = false.

**Explicit results** html.format(doctype = quoted(slug(doctype)), name = name, encoded\_name = quote(cstr(name), safe = empty text), doctype\_local = translated doctype, …).

**Local steps**

- Bind dependencies quote.
- Bind dependencies slug.
- Bind dependencies quoted.
- Set meta from get\_meta(doctype).
- Set title from get\_value(doctype, name, meta.get\_title\_field()).
- Set target\_attr from “ target="\_blank"” when open\_in\_new\_tab, otherwise empty text.
  - Value choice on open\_in\_new\_tab — true gives “ target="\_blank"”, false gives empty text.
- If (show\_title\_with\_name and name differs from title).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in show\_title\_with\_name → name differs from title.
  - Set html from text in the contract.
- Otherwise.
  - Set html from text in the contract.
- Return html.format(doctype = quoted(slug(doctype)), name = name, encoded\_name = quote(cstr(name), safe = empty text), doctype\_local = translated doctype, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L18) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1709) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L452)

<a id="op-717424168c3a54"></a>
### Get website settings

`operation_foundation_initialize_business_behavior_get_website_settings`

**Inputs** key.

**Explicit results** no value · local.website\_settings.get(key).

**Local steps**

- If not hasattr(local, “website\_settings”).
  - Attempt the following.
    - Set local.website\_settings from client\_cache.get\_doc(“Website Settings”).
  - On failure (DoesNotExistError).
    - Evaluate clear\_last\_message().
    - Return no value.
- Return local.website\_settings.get(key).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L1497) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1723) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L466)

<a id="op-ed966670e70f39"></a>
### Get active domains

`operation_foundation_initialize_business_behavior_get_active_domains`

**Inputs** no declared parameters.

**Explicit results** get\_active\_domains().

**Local steps**

- Bind dependencies get\_active\_domains.
- Return get\_active\_domains().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L1666) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1706) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L449)

<a id="op-e67dad1e820b20"></a>
### Is setup complete

`operation_foundation_initialize_business_behavior_is_setup_complete`

**Inputs** no declared parameters.

**Wrappers, in declaration order** request\_cache.

**Record and data access** read “Installed Application” via get\_all.

**Explicit results** setup\_complete.

**Local steps**

- Set setup\_complete from false.
- If not Platform.db.table\_exists(“Installed Application”).
  - Return setup\_complete.
- If all(Platform.get\_all(“Installed Application”, mapping(“app\_name” → tuple(“in”, list(“Platform”, “Enterprise”))), pluck = “is\_setup\_complete”)).
  - Set setup\_complete from true.
- Return setup\_complete.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L23) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1733) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L475)

<a id="op-e50bd49f7a276d"></a>
### Ping

`operation_foundation_initialize_business_behavior_ping`

**Inputs** no declared parameters.

**Wrappers, in declaration order** whitelist(allow\_guest = true).

**Explicit results** “pong”.

**Local steps**

- Return “pong”.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L1995) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1744) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L486)

<a id="op-394d368e692382"></a>
### Validate and sanitize search inputs

`operation_foundation_initialize_business_behavior_validate_and_sanitize_search_inputs`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** fn.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L32) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1759) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L501)

<a id="op-793984fb6b5ab9"></a>
### Validate and sanitize search inputs.wrapper

`operation_foundation_binding_foundation_init_validate_and_sanitize_search_inputs_wrapper`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** args, kwargs.

**Explicit result forms** a structured result, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L43) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1499) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1475)

<a id="op-eb836c4b8917f9"></a>
### Override whitelisted method

`operation_foundation_initialize_business_behavior_override_whitelisted_method`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** original\_method.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L2110) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1743) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L485)

## Service · Platformclient

<a id="op-5aff30a92bd1c9"></a>
### Platform Client.initialize

`operation_foundation_frappeclient_business_behavior_foundation_client_initialize`

**Inputs** self, url, username = no value, password = no value, verify = true, api\_key = no value, api\_secret = no value, Platform\_authorization\_source = no value.

**Local steps**

- Bind dependencies requests.
- Set self.headers from mapping(“Accept” → “application/json”, “content-type” → “application/x-www-form-urlencoded”).
- Set self.verify from verify.
- Set self.session from requests.session().
- Set self.url from url.
- Set self.api\_key from api\_key.
- Set self.api\_secret from api\_secret.
- Set self.Platform\_authorization\_source from Platform\_authorization\_source.
- Evaluate self.setup\_key\_authentication\_headers().
- If (username and password).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in username → password.
  - Evaluate self.\_login(username, password).

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup key authentication headers](operations-075.md#op-b845febdea48a5), [login](operations-075.md#op-add448e267054c).

**Values supplied outside this operation** service or queued work from requests.session().

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L1929) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1555) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L320)

<a id="op-191296f69a844f"></a>
### Platform Client.enter context

`operation_foundation_frappeclient_business_behavior_foundation_client_enter`

**Inputs** self.

**Explicit results** self.

**Local steps**

- Return self.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L2265) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1548) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L313)
