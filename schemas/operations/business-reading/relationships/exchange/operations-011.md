# Integrations and service calls · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Session

<a id="op-3a7386319fad98"></a>
### Get organizations

`operation_relationships_application_interface_session_business_behavior_get_organizations`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L4309) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L142) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L123)

## Service · Settings

<a id="op-4d1b9fe425e186"></a>
### Create email account

`operation_relationships_application_interface_settings_business_behavior_create_email_account`

**Inputs** data.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from mapping(“doctype” → “Email Account”, “email\_id” → data.get(“email\_id”), “email\_account\_name” → data.get(“email\_account\_name”), “service” → service, …) via get\_doc.

**State and service calls** call save on email\_doc.

**Explicit results** “Service not supported”.

**Explicit failure paths** validation helper — str(e).

**Local steps**

- Set service from data.get(“service”).
- Set service\_config from email\_service\_config.get(service).
- If not service\_config.
  - Return “Service not supported”.
- Attempt the following.
  - Set email\_doc from Platform.get\_doc(mapping(“doctype” → “Email Account”, “email\_id” → data.get(“email\_id”), “email\_account\_name” → data.get(“email\_account\_name”), “service” → service, …)).
  - If service equals “Platform Mail”.
    - Set email\_doc.api\_key from data.get(“api\_key”).
    - Set email\_doc.api\_secret from data.get(“api\_secret”).
    - Set email\_doc.Platform\_mail\_site from data.get(“Platform\_mail\_site”).
    - Set email\_doc.append\_to from “CRM Lead”.
  - Otherwise.
    - Evaluate email\_doc.append(“imap\_folder”, mapping(“append\_to” → “CRM Lead”, “folder\_name” → “INBOX”)).
    - Set email\_doc.password from data.get(“password”).
    - Evaluate email\_doc.get\_incoming\_server().
  - Evaluate email\_doc.save().
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(str(e)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L4466) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L146) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L127)

## Service · Todo

<a id="op-d5510e44b8f708"></a>
### Validate

`operation_relationships_application_interface_todo_business_behavior_validate`

**Inputs** doc, method.

**Record and data access** resolve a document from doc.reference\_type via get\_doc.

**Local steps**

- If (doc.is\_new() and doc.reference\_type belongs to list(“CRM Lead”, “CRM Deal”) and doc.reference\_name and not doc.flags.ignore\_permissions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.is\_new() → doc.reference\_type belongs to list(“CRM Lead”, “CRM Deal”) → doc.reference\_name → not doc.flags.ignore\_permissions.
  - Evaluate Platform.get\_doc(doc.reference\_type, doc.reference\_name).check\_permission(“write”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L5372) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L153) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L134)

<a id="op-5640ae0222e372"></a>
### After insert

`operation_relationships_application_interface_todo_business_behavior_after_insert`

**Inputs** doc, method.

**State and service calls** request set\_value on doc.reference\_type.

**Local steps**

- If (doc.reference\_type belongs to list(“CRM Lead”, “CRM Deal”) and doc.reference\_name and doc.allocated\_to).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_type belongs to list(“CRM Lead”, “CRM Deal”) → doc.reference\_name → doc.allocated\_to.
  - Set fieldname from “lead\_owner” when doc.reference\_type equals “CRM Lead”, otherwise “deal\_owner”.
    - Value choice on doc.reference\_type equals “CRM Lead” — true gives “lead\_owner”, false gives “deal\_owner”.
  - Evaluate Platform.db.set\_value(doc.reference\_type, doc.reference\_name, fieldname, doc.allocated\_to, update\_modified = false).
- If (doc.reference\_type belongs to list(“CRM Lead”, “CRM Deal”, “CRM Task”) and doc.reference\_name and doc.allocated\_to).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_type belongs to list(“CRM Lead”, “CRM Deal”, “CRM Task”) → doc.reference\_name → doc.allocated\_to.
  - Evaluate notify\_assigned\_user(doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L5556) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L147) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L128)

<a id="op-3829b68ccf1dbf"></a>
### On update

`operation_relationships_application_interface_todo_business_behavior_on_update`

**Inputs** doc, method.

**Local steps**

- If (doc.has\_value\_changed(“status”) and doc.status equals “Cancelled” and doc.reference\_type belongs to list(“CRM Lead”, “CRM Deal”, “CRM Task”) and doc.reference\_name and doc.allocated\_to).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.has\_value\_changed(“status”) → doc.status equals “Cancelled” → doc.reference\_type belongs to list(“CRM Lead”, “CRM Deal”, “CRM Task”) → doc.reference\_name → doc.allocated\_to.
  - Evaluate notify\_assigned\_user(doc, is\_cancelled = true).
  - Evaluate clear\_owner\_on\_unassign(doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L5875) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L152) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L133)

<a id="op-786b81e5d7a4b0"></a>
### Clear owner on unassign

`operation_relationships_application_interface_todo_business_behavior_clear_owner_on_unassign`

**Inputs** doc.

**State and service calls** request set\_value on doc.reference\_type.

**Explicit results** no value.

**Local steps**

- If doc.reference\_type does not belong to list(“CRM Lead”, “CRM Deal”).
  - Return no value.
- Set fieldname from “lead\_owner” when doc.reference\_type equals “CRM Lead”, otherwise “deal\_owner”.
  - Value choice on doc.reference\_type equals “CRM Lead” — true gives “lead\_owner”, false gives “deal\_owner”.
- Evaluate Platform.db.set\_value(doc.reference\_type, doc.reference\_name, fieldname, no value, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L6088) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L148) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L129)

<a id="op-b4d85b040dc614"></a>
### Notify assigned user

`operation_relationships_application_interface_todo_business_behavior_notify_assigned_user`

**Inputs** doc, is\_cancelled = false.

**Record and data access** resolve a document from doc.reference\_type via get\_doc · read “User” via get\_cached\_value.

**Local steps**

- Set \_doc from Platform.get\_doc(doc.reference\_type, doc.reference\_name).
- Set owner from Platform.get\_cached\_value(“User”, Platform.session.user, “full\_name”).
- Set notification\_text from get\_notification\_text(owner, doc, \_doc, is\_cancelled).
- Set message from translated “Your assignment on {0} {1} has been removed by {2}”.format(doc.reference\_type, doc.reference\_name, owner) when is\_cancelled, otherwise translated “{0} assigned a {1} {2} to you”.format(owner, d ….
  - Value choice on is\_cancelled — true gives translated “Your assignment on {0} {1} has been removed by {2}”.format(doc.reference\_type, doc.reference\_name, owner), false gives translated “{0} assigned a {1} {2} to you”.format(owner, doc.reference\_type, doc.reference\_name).
- Set tuple(redirect\_to\_doctype, redirect\_to\_name) from get\_redirect\_to\_doc(doc).
- Evaluate notify\_user(mapping(“owner” → Platform.session.user, “assigned\_to” → doc.allocated\_to, “notification\_type” → “Assignment”, “message” → message, …)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“User”, Platform.session.user, “full\_name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L6281) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L151) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L132)

<a id="op-faa9d59e16fc8f"></a>
### Get notification text

`operation_relationships_application_interface_todo_business_behavior_get_notification_text`

**Inputs** owner, doc, reference\_doc, is\_cancelled = false.

**Explicit results** formatted text                  &lt;div class="mb-2 leading-5 text-ink-gray-5"&gt;                     &lt;span&gt;{translated “Your assignment on {0} {1} has been removed by {2 · formatted text              &lt;div class="mb-2 leading-5 text-ink-gray-5"&gt;                 &lt;span class="font-medium text-ink-gray-9"&gt;{owner}&lt;/span&gt;                 &lt;sp · formatted text                  &lt;div class="mb-2 leading-5 text-ink-gray-5"&gt;                     &lt;span&gt;{translated “Your assignment on task {0} has been removed by {.

**Local steps**

- Set name from doc.reference\_name.
- Set doctype from doc.reference\_type.
- If doctype.startswith(“CRM ”).
  - Set doctype from doctype at slice 4 to no value.lower().
- If doctype belongs to list(“lead”, “deal”).
  - Set name from (reference\_doc.lead\_name or name) when doctype equals “lead”, otherwise (reference\_doc.organization or reference\_doc.lead\_name or name).
    - Value choice on doctype equals “lead” — true gives (reference\_doc.lead\_name or name), false gives (reference\_doc.organization or reference\_doc.lead\_name or name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in reference\_doc.lead\_name → name.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in reference\_doc.organization → reference\_doc.lead\_name → name.
  - If is\_cancelled.
    - Return formatted text                  &lt;div class="mb-2 leading-5 text-ink-gray-5"&gt;                     &lt;span&gt;{translated “Your assignment on {0} {1} has been removed by {2.
  - Return formatted text              &lt;div class="mb-2 leading-5 text-ink-gray-5"&gt;                 &lt;span class="font-medium text-ink-gray-9"&gt;{owner}&lt;/span&gt;                 &lt;sp.
- If doctype equals “task”.
  - If is\_cancelled.
    - Return formatted text                  &lt;div class="mb-2 leading-5 text-ink-gray-5"&gt;                     &lt;span&gt;{translated “Your assignment on task {0} has been removed by {.
  - Return formatted text              &lt;div class="mb-2 leading-5 text-ink-gray-5"&gt;                 &lt;span class="font-medium text-ink-gray-9"&gt;{owner}&lt;/span&gt;                 &lt;sp.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L6785) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L149) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L130)

<a id="op-f395e0562d50b6"></a>
### Get redirect to doc

`operation_relationships_application_interface_todo_business_behavior_get_redirect_to_record`

**Inputs** doc.

**Record and data access** resolve a document from doc.reference\_type via get\_doc.

**Explicit results** tuple(reference\_doc.reference\_doctype, reference\_doc.reference\_docname) · tuple(doc.reference\_type, doc.reference\_name).

**Local steps**

- If doc.reference\_type equals “CRM Task”.
  - Set reference\_doc from Platform.get\_doc(doc.reference\_type, doc.reference\_name).
  - Return tuple(reference\_doc.reference\_doctype, reference\_doc.reference\_docname).
- Return tuple(doc.reference\_type, doc.reference\_name).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0013.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L150) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L131)

## Service · Twilio handler

<a id="op-e47cb1e56aa266"></a>
### Twilio.initialize

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_initialize`

**Inputs** self, settings.

**Local steps**

- Set self.settings from settings.
- Set self.account\_sid from settings.account\_sid.
- Set self.application\_sid from settings.twiml\_sid.
- Set self.api\_key from settings.api\_key.
- Set self.api\_secret from settings.get\_password(“api\_secret”).
- Set self.twilio\_client from self.get\_twilio\_client().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get twilio client](operations-011.md#op-b1a2d0d8df1aab).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L7019) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1379) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1355)

<a id="op-6dc4cf0ff4a566"></a>
### Twilio.connect

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_connect`

**Inputs** cls.

**Wrappers, in declaration order** classmethod.

**Record and data access** resolve a document from “CRM Twilio Settings” via get\_doc.

**Explicit results** no value · Twilio(settings = settings).

**Local steps**

- Set settings from Platform.get\_doc(“CRM Twilio Settings”).
- If not (settings and settings.enabled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in settings → settings.enabled.
  - Return no value.
- Return Twilio(settings = settings).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L7218) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1369) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1345)

<a id="op-d0dcc09898e0c0"></a>
### Twilio.get phone numbers

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_get_phone_numbers`

**Inputs** self.

**Explicit results** list of n.phone\_number for n drawn from numbers.

**Local steps**

- Set numbers from self.twilio\_client.incoming\_phone\_numbers.list().
- Return list of n.phone\_number for n drawn from numbers.
  - Draw n from numbers.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L7346) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1375) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1351)

<a id="op-fe7529c3795a74"></a>
### Twilio.generate voice access token

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_generate_voice_access_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, identity, ttl.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L7438) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1373) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1349)

<a id="op-7370683a1cae49"></a>
### Twilio.safe identity

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_safe_identity`

**Inputs** cls, identity.

**Wrappers, in declaration order** classmethod.

**Explicit results** identity.replace(“@”, “(at)”).

**Local steps**

- Return identity.replace(“@”, “(at)”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1380) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1356)

<a id="op-633081a82bbc4f"></a>
### Twilio.emailid from identity

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_emailid_from_identity`

**Inputs** cls, identity.

**Wrappers, in declaration order** classmethod.

**Explicit results** identity.replace(“(at)”, “@”).

**Local steps**

- Return identity.replace(“(at)”, “@”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L81) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1370) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1346)

<a id="op-a5060378bceeee"></a>
### Twilio.get recording status callback url

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_get_recording_status_callback_resource_address`

**Inputs** self.

**Explicit results** get\_public\_url(url\_path).

**Local steps**

- Set url\_path from “/api/method/crm.integrations.twilio.api.update\_recording\_info”.
- Return get\_public\_url(url\_path).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L156) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1376) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1352)

<a id="op-d70f27d88166fd"></a>
### Twilio.get update call status callback url

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_get_update_call_status_callback_resource_address`

**Inputs** self.

**Explicit results** get\_public\_url(url\_path).

**Local steps**

- Set url\_path from “/api/method/crm.integrations.twilio.api.update\_call\_status\_info”.
- Return get\_public\_url(url\_path).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L226) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1378) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1354)

<a id="op-6e105043d968c9"></a>
### Twilio.generate twilio dial response

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_generate_twilio_dial_response`

**Inputs** self, from\_number, to\_number.

**Explicit results** resp.

**Local steps**

- Set resp from VoiceResponse().
- Set dial from Dial(caller\_id = from\_number, record = self.settings.record\_calls, recording\_status\_callback = self.get\_recording\_status\_callback\_url(), recording\_status\_callback\_event = “completed”).
- Evaluate dial.number(to\_number, status\_callback\_event = “initiated ringing answered completed”, status\_callback = self.get\_update\_call\_status\_callback\_url(), status\_callback\_method = “POST”).
- Evaluate resp.append(dial).
- Return resp.

**Methods declared on this owner** [get recording status callback url](operations-011.md#op-a5060378bceeee), [get update call status callback url](operations-011.md#op-d70f27d88166fd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L296) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1372) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1348)

<a id="op-c17437d2b99320"></a>
### Twilio.get call info

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_get_call_info`

**Inputs** self, call\_sid.

**Explicit results** self.twilio\_client.calls(call\_sid).fetch().

**Local steps**

- Return self.twilio\_client.calls(call\_sid).fetch().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L549) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1374) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1350)

<a id="op-ad3166f579bd50"></a>
### Twilio.generate twilio client response

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_generate_twilio_client_response`

**Inputs** self, client, ring\_tone = “at”.

**Explicit results** resp.

**Local steps**

- Set resp from VoiceResponse().
- Set dial from Dial(ring\_tone = ring\_tone, record = self.settings.record\_calls, recording\_status\_callback = self.get\_recording\_status\_callback\_url(), recording\_status\_callback\_event = “completed”).
- Evaluate dial.client(client, status\_callback\_event = “initiated ringing answered completed”, status\_callback = self.get\_update\_call\_status\_callback\_url(), status\_callback\_method = “POST”).
- Evaluate resp.append(dial).
- Return resp.

**Methods declared on this owner** [get recording status callback url](operations-011.md#op-a5060378bceeee), [get update call status callback url](operations-011.md#op-d70f27d88166fd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L625) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1371) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1347)

<a id="op-b1a2d0d8df1aab"></a>
### Twilio.get twilio client

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_get_twilio_client`

**Inputs** self.

**Wrappers, in declaration order** classmethod.

**Record and data access** resolve a document from “CRM Twilio Settings” via get\_doc.

**Explicit results** client.

**Explicit failure paths** validation helper — translated “Please enable twilio settings before making a call.”.

**Local steps**

- Set twilio\_settings from Platform.get\_doc(“CRM Twilio Settings”).
- If not twilio\_settings.enabled.
  - Call the validation error handler Platform.throw(translated “Please enable twilio settings before making a call.”).
- Set auth\_token from get\_decrypted\_password(“CRM Twilio Settings”, “CRM Twilio Settings”, “auth\_token”).
- Set client from TwilioClient(twilio\_settings.account\_sid, auth\_token).
- Return client.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L872) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1377) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1353)

<a id="op-840089024e14c4"></a>
### Incoming Call.initialize

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_incoming_call_initialize`

**Inputs** self, from\_number, to\_number, meta = no value.

**Local steps**

- Set self.from\_number from from\_number.
- Set self.to\_number from to\_number.
- Set self.meta from meta.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L1092) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1361) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1337)

<a id="op-0f9f042dbc30ae"></a>
### Incoming Call.process

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_incoming_call_process`

**Inputs** self.

**Explicit results** resp · twilio.generate\_twilio\_dial\_response(self.from\_number, attender at “mobile\_no”) · twilio.generate\_twilio\_client\_response(twilio.safe\_identity(attender at “name”)).

**Local steps**

- Set twilio from Twilio.connect().
- Set owners from get\_twilio\_number\_owners(self.to\_number).
- Set attender from get\_the\_call\_attender(owners, self.from\_number).
- If not attender.
  - Set resp from VoiceResponse().
  - Evaluate resp.say(translated “Agent is unavailable to take the call, please call after some time.”).
  - Return resp.
- If attender at “call\_receiving\_device” equals “Phone”.
  - Return twilio.generate\_twilio\_dial\_response(self.from\_number, attender at “mobile\_no”).
- Otherwise.
  - Return twilio.generate\_twilio\_client\_response(twilio.safe\_identity(attender at “name”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L1197) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1362) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1338)

<a id="op-b6d3940dba1f0a"></a>
### Get twilio number owners

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_get_twilio_number_owners`

**Inputs** phone\_number.

**Record and data access** read “CRM Telephony Agent” via get\_all · read “User” via get\_all.

**Explicit results** merge\_dicts(user\_wise\_general\_settings, user\_wise\_voice\_settings).

**Local steps**

- Set phone\_number from empty text.join(list of c for c drawn from phone\_number where (c.isdigit() or c equals “+”)).
  - Draw c from phone\_number, keep a combination only if ((c.isdigit() or c equals “+”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in c.isdigit() → c equals “+”.
- Set user\_voice\_settings from Platform.get\_all(“CRM Telephony Agent”, filters = mapping(“twilio\_number” → phone\_number), fields = list(“name”, “call\_receiving\_device”)).
- Set user\_wise\_voice\_settings from mapping of user at “name” → user for user drawn from user\_voice\_settings.
  - Draw user from user\_voice\_settings.
- Set user\_general\_settings from Platform.get\_all(“User”, filters = list(list(“name”, “IN”, user\_wise\_voice\_settings.keys())), fields = list(“name”, “mobile\_no”)).
- Set user\_wise\_general\_settings from mapping of user at “name” → user for user drawn from user\_general\_settings.
  - Draw user from user\_general\_settings.
- Return merge\_dicts(user\_wise\_general\_settings, user\_wise\_voice\_settings).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L1528) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1360) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1336)
