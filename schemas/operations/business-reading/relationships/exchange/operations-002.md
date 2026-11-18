# Integrations and service calls · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Api

<a id="op-d8880b66aad7be"></a>
### Is call integration enabled

`operation_relationships_integrations_application_interface_business_behavior_is_call_integration_enabled`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Twilio Settings” via get\_single\_value · read “CRM Exotel Settings” via get\_single\_value.

**Explicit results** mapping(“integrations” → mapping(“twilio” → bool(Platform.db.get\_single\_value(“CRM Twilio Settings”, “enabled”)), “exotel” → bool(Platform.db.get\_single\_value(“CRM Exotel Settings”, “enabled”))), “default\_ ….

**Local steps**

- Return mapping(“integrations” → mapping(“twilio” → bool(Platform.db.get\_single\_value(“CRM Twilio Settings”, “enabled”)), “exotel” → bool(Platform.db.get\_single\_value(“CRM Exotel Settings”, “enabled”))), “default\_ ….

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Twilio Settings”, “enabled”), Platform.db.get\_single\_value(“CRM Exotel Settings”, “enabled”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1269) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1245)

<a id="op-62114bd518dc89"></a>
### Get user default calling medium

`operation_relationships_integrations_application_interface_business_behavior_get_user_default_calling_medium`

**Inputs** no declared parameters.

**Record and data access** read “CRM Telephony Agent” via exists · read “CRM Telephony Agent” via get\_value.

**Explicit results** no value · default\_medium.

**Local steps**

- If not Platform.db.exists(“CRM Telephony Agent”, Platform.session.user).
  - Return no value.
- Set default\_medium from Platform.db.get\_value(“CRM Telephony Agent”, Platform.session.user, “default\_medium”).
- If not default\_medium.
  - Return no value.
- Return default\_medium.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L205) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1268) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1244)

<a id="op-9e90c17b6131d5"></a>
### Set default calling medium

`operation_relationships_integrations_application_interface_business_behavior_set_default_calling_medium`

**Inputs** medium.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Telephony Agent” via exists · resolve a document from mapping(“doctype” → “CRM Telephony Agent”, “user” → Platform.session.user, “default\_medium” → medium) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Telephony Agent”, “user” → Platform.session.user, “default\_medium” → medium)) · request set\_value on “CRM Telephony Agent”.

**Explicit results** get\_user\_default\_calling\_medium().

**Local steps**

- If not Platform.db.exists(“CRM Telephony Agent”, Platform.session.user).
  - Evaluate Platform.get\_doc(mapping(“doctype” → “CRM Telephony Agent”, “user” → Platform.session.user, “default\_medium” → medium)).insert(ignore\_permissions = true).
- Otherwise.
  - Evaluate Platform.db.set\_value(“CRM Telephony Agent”, Platform.session.user, “default\_medium”, medium).
- Return get\_user\_default\_calling\_medium().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L371) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1274) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1250)

<a id="op-a3efa19c4dfe7d"></a>
### Add note to call log

`operation_relationships_integrations_application_interface_business_behavior_add_note_to_call_log`

**Inputs** call\_sid, note.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from mapping(“doctype” → “FCRM Note”, “title” → note.get(“title”, “Call Note”), “content” → note.get(“content”)) via get\_doc · resolve a document from “CRM Call Log” via get\_cached\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “FCRM Note”, “title” → note.get(“title”, “Call Note”), “content” → note.get(“content”))) · call save on call\_log.

**Explicit results** \_note.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If not Platform.has\_permission(“CRM Call Log”, “write”, call\_sid).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set \_note from no value.
- If not note.get(“name”).
  - Set \_note from Platform.get\_doc(mapping(“doctype” → “FCRM Note”, “title” → note.get(“title”, “Call Note”), “content” → note.get(“content”))).insert(ignore\_permissions = true).
- Otherwise.
  - Set \_note from Platform.set\_value(“FCRM Note”, note.get(“name”), “content”, note.get(“content”)).
- Set call\_log from Platform.get\_cached\_doc(“CRM Call Log”, call\_sid).
- Evaluate call\_log.link\_with\_reference\_doc(“FCRM Note”, \_note.name).
- Evaluate call\_log.save(ignore\_permissions = true).
- Return \_note.

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Call Log”, “write”, call\_sid) · configured or stored value from Platform.get\_cached\_doc(“CRM Call Log”, call\_sid).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L657) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1259) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1235)

<a id="op-604d8a1d8dc54b"></a>
### Add task to call log

`operation_relationships_integrations_application_interface_business_behavior_add_task_to_call_log`

**Inputs** call\_sid, task.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from mapping(“doctype” → “CRM Task”, “title” → task.get(“title”), “description” → task.get(“description”), “assigned\_to” → task.get(“assigned\_to”), …) via get\_doc · resolve a document from “CRM Task” via get\_doc · resolve a document from “CRM Call Log” via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Task”, “title” → task.get(“title”), “description” → task.get(“description”), “assigned\_to” → task.get(“assigned\_to”), …)) · call save on \_task · call save on call\_log.

**Explicit results** \_task.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If not Platform.has\_permission(“CRM Call Log”, “write”, call\_sid).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set \_task from no value.
- If not task.get(“name”).
  - Set \_task from Platform.get\_doc(mapping(“doctype” → “CRM Task”, “title” → task.get(“title”), “description” → task.get(“description”), “assigned\_to” → task.get(“assigned\_to”), …)).insert(ignore\_permissions = true).
- Otherwise.
  - Set \_task from Platform.get\_doc(“CRM Task”, task.get(“name”)).
  - Evaluate \_task.update(mapping(“title” → task.get(“title”), “description” → task.get(“description”), “assigned\_to” → task.get(“assigned\_to”), “due\_date” → task.get(“due\_date”), …)).
  - Evaluate \_task.save(ignore\_permissions = true).
- Set call\_log from Platform.get\_doc(“CRM Call Log”, call\_sid).
- Evaluate call\_log.link\_with\_reference\_doc(“CRM Task”, \_task.name).
- Evaluate call\_log.save(ignore\_permissions = true).
- Return \_task.

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Call Log”, “write”, call\_sid).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L1221) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1260) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1236)

<a id="op-fdd564938e8038"></a>
### Get contact lead or deal from number

`operation_relationships_integrations_application_interface_business_behavior_get_contact_lead_or_deal_from_number`

**Inputs** number.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** tuple(docname, doctype) · tuple(no value, no value).

**Local steps**

- Set contact from get\_contact\_by\_phone\_number(number).
- If contact.get(“name”).
  - Set doctype from “Contact”.
  - Set docname from contact.get(“name”).
  - If contact.get(“lead”).
    - Set doctype from “CRM Lead”.
    - Set docname from contact.get(“lead”).
  - Otherwise.
    - If contact.get(“deal”).
      - Set doctype from “CRM Deal”.
      - Set docname from contact.get(“deal”).
  - Return tuple(docname, doctype).
- Return tuple(no value, no value).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L2156) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1264) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1240)

<a id="op-96a4f953e6619b"></a>
### Get contact by phone number

`operation_relationships_integrations_application_interface_business_behavior_get_contact_by_phone_number`

**Inputs** phone\_number.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_contact(number.get(“national\_number”), number.get(“country”)) · get\_contact(phone\_number, number.get(“country”), exact\_match = true).

**Local steps**

- Set number from parse\_phone\_number(phone\_number).
- If number.get(“is\_valid”).
  - Return get\_contact(number.get(“national\_number”), number.get(“country”)).
- Otherwise.
  - Return get\_contact(phone\_number, number.get(“country”), exact\_match = true).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L2503) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1263) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1239)

<a id="op-4ceb697d844537"></a>
### Resolve validated ip

`operation_relationships_integrations_application_interface_business_behavior_resolve_validated_internet_protocol`

**Inputs** hostname, port.

**Declared result** str.

**Explicit results** ips at 0.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Invalid recording URL” · validation helper with Platform.ValidationError — translated “Recording URL is not allowed”.

**Local steps**

- Attempt the following.
  - Set addrinfos from socket.getaddrinfo(hostname, port, proto = socket.IPPROTO\_TCP).
- On failure (socket.gaierror).
  - Call the validation error handler Platform.throw(translated “Invalid recording URL”, Platform.ValidationError).
- Set ips from list of info at 4 at 0 for info drawn from addrinfos.
  - Draw info from addrinfos.
- If not ips.
  - Call the validation error handler Platform.throw(translated “Invalid recording URL”, Platform.ValidationError).
- For each ip in ips.
  - If not ipaddress.ip\_address(ip).is\_global.
    - Call the validation error handler Platform.throw(translated “Recording URL is not allowed”, Platform.ValidationError).
- Return ips at 0.

**Values supplied outside this operation** service or queued work from socket.getaddrinfo(hostname, port, proto = socket.IPPROTO\_TCP).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L2727) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1272) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1248)

<a id="op-4ae8a6348398a0"></a>
### Pinned IPAdapter.initialize

`operation_relationships_integrations_application_interface_business_behavior_pinned_internet_protocol_adapter_initialize`

**Inputs** self, pinned\_ip, hostname, remaining named values kwargs.

**Local steps**

- Set self.\_pinned\_ip from pinned\_ip.
- Set self.\_hostname from hostname.
- Evaluate super().\_\_init\_\_(expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L3108) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1270) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1246)

<a id="op-774e7a0f557814"></a>
### Pinned IPAdapter.send

`operation_relationships_integrations_application_interface_business_behavior_pinned_internet_protocol_adapter_send`

**Inputs** self, request, remaining named values kwargs.

**Explicit results** super().send(request, expanded names kwargs).

**Local steps**

- Set parsed from urlparse(request.url).
- Set literal\_ip from formatted text &#91;{self.\_pinned\_ip}&#93; when ipaddress.ip\_address(self.\_pinned\_ip).version equals 6, otherwise self.\_pinned\_ip.
  - Value choice on ipaddress.ip\_address(self.\_pinned\_ip).version equals 6 — true gives formatted text &#91;{self.\_pinned\_ip}&#93;, false gives self.\_pinned\_ip.
- Set netloc from formatted text {literal\_ip}:{parsed.port} when parsed.port, otherwise literal\_ip.
  - Value choice on parsed.port — true gives formatted text {literal\_ip}:{parsed.port}, false gives literal\_ip.
- Set request.url from urlunparse(parsed.\_replace(netloc = netloc)).
- Set host from formatted text &#91;{parsed.hostname}&#93; when “:” belongs to parsed.hostname, otherwise parsed.hostname.
  - Value choice on “:” belongs to parsed.hostname — true gives formatted text &#91;{parsed.hostname}&#93;, false gives parsed.hostname.
- Set request.headers at “Host” from formatted text {host}:{parsed.port} when parsed.port, otherwise host.
  - Value choice on parsed.port — true gives formatted text {host}:{parsed.port}, false gives host.
- If parsed.scheme equals “https”.
  - Set self.poolmanager.connection\_pool\_kw at “server\_hostname” from self.\_hostname.
  - Set self.poolmanager.connection\_pool\_kw at “assert\_hostname” from self.\_hostname.
- Return super().send(request, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L3236) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1271) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1247)

<a id="op-18c1b9d20c2dce"></a>
### Safe get

`operation_relationships_integrations_application_interface_business_behavior_safe_get`

**Inputs** url, auth, headers.

**Explicit results** tuple(resp, session).

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Invalid recording URL”.

**Local steps**

- Set parsed from urlparse(url).
- If (parsed.scheme does not belong to tuple(“http”, “https”) or not parsed.hostname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parsed.scheme does not belong to tuple(“http”, “https”) → not parsed.hostname.
  - Call the validation error handler Platform.throw(translated “Invalid recording URL”, Platform.ValidationError).
- Set port from (parsed.port or 443 when parsed.scheme equals “https”, otherwise 80).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parsed.port → 443 when parsed.scheme equals “https”, otherwise 80.
  - Value choice on parsed.scheme equals “https” — true gives 443, false gives 80.
- Set pinned\_ip from \_resolve\_validated\_ip(parsed.hostname, port).
- Set session from requests.Session().
- Evaluate session.mount(formatted text {parsed.scheme}://, \_PinnedIPAdapter(pinned\_ip, parsed.hostname)).
- Set resp from session.get(url, auth = auth, headers = headers, stream = true, timeout = 30, …).
- Return tuple(resp, session).

**Values supplied outside this operation** service or queued work from requests.Session().

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L3772) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1273) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1249)

<a id="op-479d92aeabaefa"></a>
### Fetch recording

`operation_relationships_integrations_application_interface_business_behavior_fetch_recording`

**Inputs** url, auth, headers.

**Explicit results** resp.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Too many redirects while fetching recording”.

**Local steps**

- Set current\_url from url.
- Set current\_auth from auth.
- For each \_hop in range(5).
  - Set tuple(resp, session) from \_safe\_get(current\_url, current\_auth, headers).
  - If (resp.is\_redirect and resp.headers.get(“Location”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in resp.is\_redirect → resp.headers.get(“Location”).
    - Set current\_url from requests.compat.urljoin(current\_url, resp.headers at “Location”).
    - Set current\_auth from no value.
    - Evaluate resp.close().
    - Evaluate session.close().
    - Continue with the next iteration or loop test.
  - Set resp.\_pinned\_session from session.
  - Return resp.
- Call the validation error handler Platform.throw(translated “Too many redirects while fetching recording”, Platform.ValidationError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from requests.compat.urljoin(current\_url, resp.headers at “Location”).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L4224) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1261) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1237)

<a id="op-0e7d12471339e2"></a>
### Get recording url

`operation_relationships_integrations_application_interface_business_behavior_get_recording_resource_address`

**Inputs** call\_log\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Call Log” via exists · resolve a document from “CRM Call Log” via get\_doc.

**Explicit results** response.

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Call log not found” · validation helper with Platform.DoesNotExistError — translated “Recording URL not found”.

**Local steps**

- If (not call\_log\_name or not Platform.db.exists(“CRM Call Log”, call\_log\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not call\_log\_name → not Platform.db.exists(“CRM Call Log”, call\_log\_name).
  - Call the validation error handler Platform.throw(translated “Call log not found”, Platform.DoesNotExistError).
- Set log from Platform.get\_doc(“CRM Call Log”, call\_log\_name).
- Evaluate log.check\_permission(“read”).
- If not log.recording\_url.
  - Call the validation error handler Platform.throw(translated “Recording URL not found”, Platform.DoesNotExistError).
- Set auth from \_get\_recording\_credentials(log.telephony\_medium).
- Set req\_headers from mapping().
- Set range\_header from Platform.get\_request\_header(“Range”).
- If range\_header.
  - Set req\_headers at “Range” from range\_header.
- Set upstream from \_fetch\_recording(log.recording\_url, auth, req\_headers).
- Evaluate upstream.raise\_for\_status().
- Bind local operation \_stream for subsequent calls.
- Set response from Response(\_stream(), status = upstream.status\_code, mimetype = (upstream.headers.get(“Content-Type”) or “audio/mpeg”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in upstream.headers.get(“Content-Type”) → “audio/mpeg”.
- Set response.headers at “Accept-Ranges” from “bytes”.
- For each header in tuple(“Content-Length”, “Content-Range”).
  - If upstream.headers.get(header).
    - Set response.headers at header from upstream.headers at header.
- Return response.

**Values supplied outside this operation** effective access from log.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L4601) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1266) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1242)

<a id="op-3aada877c28fdb"></a>
### Get recording url.stream

`operation_relationships_integrations_application_interface_business_behavior_get_recording_resource_address_stream`

**Inputs** no declared parameters.

**Local steps**

- Attempt the following.
  - yield values from upstream.iter\_content(chunk\_size = (64 × 1024)).
- On exit, including pending return or failure.
  - Evaluate upstream.close().
  - Set session from getattr(upstream, “\_pinned\_session”, no value).
  - If session is distinct from no value.
    - Evaluate session.close().

On ordinary fall-through the sequence ends.

**Values supplied outside this operation** selected callable from getattr(upstream, “\_pinned\_session”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L5404) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1267) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1243)

<a id="op-30f9cd72149941"></a>
### Get contact

`operation_relationships_integrations_application_interface_business_behavior_get_contact`

**Inputs** phone\_number, country = “IN”, exact\_match = false.

**Record and data access** read “CRM Contacts” via exists · read “CRM Contacts” via get\_value.

**Explicit results** mapping(“mobile\_no” → phone\_number) · contact · lead · contacts at 0.

**Local steps**

- If not phone\_number.
  - Return mapping(“mobile\_no” → phone\_number).
- Set cleaned\_number from nested operand in the contract(nested operand in the contract, nested operand in the contract).replace(“(”, empty text).replace(“)”, empty text).replace(“+”, empty text).
- Set Contact from Platform.qb.DocType(“Contact”).
- Set ContactPhone from Platform.qb.DocType(“Contact Phone”).
- Set normalized\_phone from Replace(Replace(Replace(Replace(Replace(ContactPhone.phone, one space, empty text), “-”, empty text), “(”, empty text), “)”, empty text), “+”, empty text).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.parent ….
- Set contacts from query.run(as\_dict = true).
- If len(contacts).
  - For each contact in contacts.
    - If Platform.db.exists(“CRM Contacts”, mapping(“contact” → contact.name, “is\_primary” → 1)).
      - Set deal from Platform.db.get\_value(“CRM Contacts”, mapping(“contact” → contact.name, “is\_primary” → 1), “parent”).
      - If are\_same\_phone\_number(contact.matched\_phone, phone\_number, country, validate = not exact\_match).
        - Set contact at “deal” from deal.
        - Return contact.
- Set Lead from Platform.qb.DocType(“CRM Lead”).
- Set normalized\_phone from Replace(Replace(Replace(Replace(Replace(Lead.mobile\_no, one space, empty text), “-”, empty text), “(”, empty text), “)”, empty text), “+”, empty text).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.converted ….
- Set leads from query.run(as\_dict = true).
- If len(leads).
  - For each lead in leads.
    - If are\_same\_phone\_number(lead.mobile\_no, phone\_number, country, validate = not exact\_match).
      - Set lead at “lead” from lead.name.
      - Set lead at “full\_name” from lead.lead\_name.
      - Return lead.
- If (len(contacts) and are\_same\_phone\_number(contacts at 0.matched\_phone, phone\_number, country, validate = not exact\_match)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(contacts) → are\_same\_phone\_number(contacts at 0.matched\_phone, phone\_number, country, validate = not exact\_match).
  - Return contacts at 0.
- Return mapping(“mobile\_no” → phone\_number).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0050.json#L5565) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1262) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1238)

<a id="op-5fd0651e98af92"></a>
### Validate twilio request

`operation_relationships_integrations_twilio_application_interface_business_behavior_validate_twilio_request`

**Inputs** args, require\_application\_sid = false.

**Explicit results** twilio.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Twilio configuration is missing” · validation helper with Platform.PermissionError — translated “Invalid Twilio account” · validation helper with Platform.PermissionError — translated “Invalid Twilio application”.

**Local steps**

- Set twilio from Twilio.connect().
- If not twilio.
  - Call the validation error handler Platform.throw(translated “Twilio configuration is missing”, Platform.PermissionError).
- Set account\_sid from Platform.utils.cstr(args.get(“AccountSid”)).
- If (not account\_sid or account\_sid differs from Platform.utils.cstr(twilio.account\_sid)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not account\_sid → account\_sid differs from Platform.utils.cstr(twilio.account\_sid).
  - Call the validation error handler Platform.throw(translated “Invalid Twilio account”, Platform.PermissionError).
- If require\_application\_sid.
  - Set application\_sid from Platform.utils.cstr(args.get(“ApplicationSid”)).
  - If (not application\_sid or application\_sid differs from Platform.utils.cstr(twilio.application\_sid)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not application\_sid → application\_sid differs from Platform.utils.cstr(twilio.application\_sid).
    - Call the validation error handler Platform.throw(translated “Invalid Twilio application”, Platform.PermissionError).
- Return twilio.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L2626) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1355) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1331)

<a id="op-eee0d9908a0c36"></a>
### Is enabled

`operation_relationships_integrations_twilio_application_interface_business_behavior_is_enabled`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Twilio Settings” via get\_single\_value.

**Explicit results** Platform.db.get\_single\_value(“CRM Twilio Settings”, “enabled”).

**Local steps**

- Return Platform.db.get\_single\_value(“CRM Twilio Settings”, “enabled”).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Twilio Settings”, “enabled”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L3090) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1349) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1325)

<a id="op-f4670126a807fd"></a>
### Generate access token

`operation_relationships_integrations_twilio_application_interface_business_behavior_generate_access_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a structured result.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L3173) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1346) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1322)

<a id="op-41df89f8245141"></a>
### Voice

`operation_relationships_integrations_twilio_application_interface_business_behavior_voice`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**State and service calls** rollback · commit.

**Explicit results** Response(resp.to\_xml(), mimetype = “text/xml”) · Response(\_call\_failed\_response().to\_xml(), mimetype = “text/xml”).

**Local steps**

- Bind local operation \_get\_caller\_number for subsequent calls.
- Set args from Platform.\_dict(kwargs).
- Set twilio from validate\_twilio\_request(args, require\_application\_sid = true).
- Set from\_number from \_get\_caller\_number(args.Caller).
- If not from\_number.
  - Set resp from VoiceResponse().
  - Evaluate resp.say(translated “Your account is not configured with a phone number. Please contact your administrator.”).
  - Return Response(resp.to\_xml(), mimetype = “text/xml”).
- Set call\_details from TwilioCallDetails(args, call\_from = from\_number).
- Attempt the following.
  - Evaluate create\_call\_log(call\_details).
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate Platform.log\_error(title = “Error while creating Twilio call log”).
  - Evaluate Platform.db.commit().
  - Return Response(\_call\_failed\_response().to\_xml(), mimetype = “text/xml”).
- Set resp from twilio.generate\_twilio\_dial\_response(from\_number, args.To).
- Return Response(resp.to\_xml(), mimetype = “text/xml”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L3463) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1356) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1332)

<a id="op-b7c19c6da7834e"></a>
### Voice.get caller number

`operation_relationships_integrations_twilio_application_interface_business_behavior_voice_get_caller_number`

**Inputs** caller.

**Record and data access** read “CRM Telephony Agent” via get\_value.

**Explicit results** Platform.db.get\_value(“CRM Telephony Agent”, user, “twilio\_number”).

**Local steps**

- Set identity from caller.replace(“client:”, empty text).strip().
- Set user from Twilio.emailid\_from\_identity(identity).
- Return Platform.db.get\_value(“CRM Telephony Agent”, user, “twilio\_number”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L4137) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1357) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1333)

<a id="op-0b33cadaedfa40"></a>
### Twilio incoming call handler

`operation_relationships_integrations_twilio_application_interface_business_behavior_twilio_incoming_call_handler`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**State and service calls** rollback · commit.

**Explicit results** Response(\_call\_failed\_response().to\_xml(), mimetype = “text/xml”) · Response(resp.to\_xml(), mimetype = “text/xml”).

**Local steps**

- Set args from Platform.\_dict(kwargs).
- Evaluate validate\_twilio\_request(args).
- Set call\_details from TwilioCallDetails(args).
- Attempt the following.
  - Evaluate create\_call\_log(call\_details).
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate Platform.log\_error(title = “Error while creating Twilio call log”).
  - Evaluate Platform.db.commit().
  - Return Response(\_call\_failed\_response().to\_xml(), mimetype = “text/xml”).
- Set resp from IncomingCall(args.From, args.To).process().
- Return Response(resp.to\_xml(), mimetype = “text/xml”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L4286) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1351) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1327)

<a id="op-b9d5c3f10d0ecb"></a>
### Call failed response

`operation_relationships_integrations_twilio_application_interface_business_behavior_call_failed_response`

**Inputs** no declared parameters.

**Explicit results** resp.

**Local steps**

- Set resp from VoiceResponse().
- Evaluate resp.say(translated “We're unable to connect your call right now. Please try again later.”).
- Return resp.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L4669) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1344) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1320)

<a id="op-5a223938d16908"></a>
### Create call log

`operation_relationships_integrations_twilio_application_interface_business_behavior_create_call_log`

**Inputs** call\_details.

**Record and data access** resolve a document from mapping(expand details, “doctype” → “CRM Call Log”, “telephony\_medium” → “Twilio”) via get\_doc.

**State and service calls** call save on call\_log · commit.

**Explicit results** call\_log.

**Local steps**

- Set details from call\_details.to\_dict().
- Set call\_log from Platform.get\_doc(mapping(expand details, “doctype” → “CRM Call Log”, “telephony\_medium” → “Twilio”)).
- Set contact\_number from details.get(“from”) when details.get(“type”) equals “Incoming”, otherwise details.get(“to”).
  - Value choice on details.get(“type”) equals “Incoming” — true gives details.get(“from”), false gives details.get(“to”).
- Evaluate link(contact\_number, call\_log).
- Evaluate call\_log.save(ignore\_permissions = true).
- Evaluate Platform.db.commit().
- Return call\_log.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L4757) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1345) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1321)

<a id="op-0e9215bd35d6d7"></a>
### Link

`operation_relationships_integrations_twilio_application_interface_business_behavior_link`

**Inputs** contact\_number, call\_log.

**Local steps**

- Set contact from get\_contact\_by\_phone\_number(contact\_number).
- If contact.get(“name”).
  - Set doctype from “Contact”.
  - Set docname from contact.get(“name”).
  - If contact.get(“lead”).
    - Set doctype from “CRM Lead”.
    - Set docname from contact.get(“lead”).
  - Otherwise.
    - If contact.get(“deal”).
      - Set doctype from “CRM Deal”.
      - Set docname from contact.get(“deal”).
  - Evaluate call\_log.link\_with\_reference\_doc(doctype, docname).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L5074) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1350) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1326)
