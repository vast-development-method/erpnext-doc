# Integrations and service calls · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Handler

<a id="op-971ecab72ba7f2"></a>
### Get status updater url

`operation_relationships_integrations_exotel_handler_business_behavior_get_status_updater_resource_address`

**Inputs** no declared parameters.

**Record and data access** read “CRM Exotel Settings” via get\_single\_value.

**Explicit results** get\_url(formatted text api/method/crm.integrations.exotel.handler.handle\_request?key={webhook\_verify\_token}&amp;agent={Platform.session.user}).

**Local steps**

- Bind dependencies get\_url.
- Set webhook\_verify\_token from Platform.db.get\_single\_value(“CRM Exotel Settings”, “webhook\_verify\_token”).
- Return get\_url(formatted text api/method/crm.integrations.exotel.handler.handle\_request?key={webhook\_verify\_token}&amp;agent={Platform.session.user}).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Exotel Settings”, “webhook\_verify\_token”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1337) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1313)

<a id="op-61203c75b3bd20"></a>
### Get exotel settings

`operation_relationships_integrations_exotel_handler_business_behavior_get_exotel_settings`

**Inputs** no declared parameters.

**Record and data access** read “CRM Exotel Settings” via get\_single.

**Explicit results** Platform.get\_single(“CRM Exotel Settings”).

**Local steps**

- Return Platform.get\_single(“CRM Exotel Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L149) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1336) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1312)

<a id="op-f5523cc01c3d5e"></a>
### Validate request

`operation_relationships_integrations_exotel_handler_business_behavior_validate_request`

**Inputs** no declared parameters.

**Record and data access** read “CRM Exotel Settings” via get\_single\_value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Unauthorized request”.

**Local steps**

- Set webhook\_verify\_token from Platform.db.get\_single\_value(“CRM Exotel Settings”, “webhook\_verify\_token”).
- Set key from Platform.request.args.get(“key”).
- Set is\_valid from (key and key equals webhook\_verify\_token).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in key → key equals webhook\_verify\_token.
- If not is\_valid.
  - Call the validation error handler Platform.throw(translated “Unauthorized request”, exc = Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Exotel Settings”, “webhook\_verify\_token”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L200) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1343) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1319)

<a id="op-3691acd4ff7ac7"></a>
### Is integration enabled

`operation_relationships_integrations_exotel_handler_business_behavior_is_integration_enabled`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Exotel Settings” via get\_single\_value.

**Explicit results** Platform.db.get\_single\_value(“CRM Exotel Settings”, “enabled”, true).

**Local steps**

- Return Platform.db.get\_single\_value(“CRM Exotel Settings”, “enabled”, true).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Exotel Settings”, “enabled”, true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L416) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1339) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1315)

<a id="op-c53964b4614731"></a>
### Create call log

`operation_relationships_integrations_exotel_handler_business_behavior_create_call_log`

**Inputs** call\_id, from\_number, to\_number, medium, agent, status = “Ringing”, call\_type = “Incoming”.

**State and service calls** request new\_doc for “CRM Call Log” · call save on call\_log · commit.

**Explicit results** call\_log.

**Local steps**

- Set call\_log from Platform.new\_doc(“CRM Call Log”).
- Set call\_log.id from call\_id.
- Set call\_log.to from to\_number.
- Set call\_log.medium from medium.
- Set call\_log.type from call\_type.
- Set call\_log.status from status.
- Set call\_log.telephony\_medium from “Exotel”.
- Evaluate setattr(call\_log, “from”, from\_number).
- If call\_type equals “Incoming”.
  - Set call\_log.receiver from agent.
- Otherwise.
  - Set call\_log.caller from agent.
- Set contact\_number from from\_number when call\_type equals “Incoming”, otherwise to\_number.
  - Value choice on call\_type equals “Incoming” — true gives from\_number, false gives to\_number.
- Evaluate link(contact\_number, call\_log).
- Evaluate call\_log.save(ignore\_permissions = true).
- Evaluate Platform.db.commit().
- Return call\_log.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L503) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1331) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1307)

<a id="op-0a71fd766e8bc0"></a>
### Link

`operation_relationships_integrations_exotel_handler_business_behavior_link`

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

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L928) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1340) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1316)

<a id="op-4950e63fd7f5db"></a>
### Get call log

`operation_relationships_integrations_exotel_handler_business_behavior_get_call_log`

**Inputs** call\_payload.

**Record and data access** read “CRM Call Log” via exists · resolve a document from “CRM Call Log” via get\_doc.

**Explicit results** Platform.get\_doc(“CRM Call Log”, call\_log\_id).

**Local steps**

- Set call\_log\_id from call\_payload.get(“CallSid”).
- If Platform.db.exists(“CRM Call Log”, call\_log\_id).
  - Return Platform.get\_doc(“CRM Call Log”, call\_log\_id).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L1256) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1333) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1309)

<a id="op-1a47ee1f656cae"></a>
### Get call agent

`operation_relationships_binding_crm_integrations_exotel_handler_get_call_agent`

**Inputs** call\_payload.

**Explicit results** agent · call\_log.receiver when call\_log.type equals “Incoming”, otherwise call\_log.caller.

**Local steps**

- If agent bound to (call\_payload.get(“AgentEmail”) or Platform.request.args.get(“agent”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in call\_payload.get(“AgentEmail”) → Platform.request.args.get(“agent”).
  - Return agent.
- If call\_log bound to get\_call\_log(call\_payload).
  - Return call\_log.receiver when call\_log.type equals “Incoming”, otherwise call\_log.caller.
    - Value choice on call\_log.type equals “Incoming” — true gives call\_log.receiver, false gives call\_log.caller.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L212) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L368) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L349)

<a id="op-d2fb4b2ccdaaec"></a>
### Normalize call status

`operation_relationships_binding_crm_integrations_exotel_handler_normalize_call_status`

**Inputs** status.

**Explicit results** no value · EXOTEL\_CALL\_STATUSES at status.

**Local steps**

- If not status.
  - Return no value.
- Set status from nested operand in the contract().lower().replace(“\_”, “-”).replace(one space, “-”).
- If status belongs to EXOTEL\_EMPTY\_STATUSES.
  - Return no value.
- If status does not belong to EXOTEL\_CALL\_STATUSES.
  - Evaluate Platform.log\_error(title = “Unknown Exotel call status”, message = formatted text Exotel sent call status {status}, which is not in EXOTEL\_CALL\_STATUSES).
  - Return no value.
- Return EXOTEL\_CALL\_STATUSES at status.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L213) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L369) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L350)

<a id="op-5fc01d5617cb63"></a>
### Get call log status

`operation_relationships_integrations_exotel_handler_business_behavior_get_call_log_status`

**Inputs** call\_payload, direction = “inbound”.

**Explicit results** status.

**Local steps**

- If (direction equals “outbound-api” or direction equals “outbound-dial”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in direction equals “outbound-api” → direction equals “outbound-dial”.
  - Set status from normalize\_call\_status(call\_payload.get(“Status”)).
  - If status equals “Busy”.
    - Set status from “Ringing”.
  - If status.
    - Return status.
- Set call\_type from call\_payload.get(“CallType”).
- Set status from normalize\_call\_status((call\_payload.get(“DialCallStatus”) or call\_payload.get(“Status”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in call\_payload.get(“DialCallStatus”) → call\_payload.get(“Status”).
- If call\_type equals “completed”.
  - Set status from “Completed”.
- Otherwise.
  - If status equals “Busy”.
    - Set status from “Ringing”.
- Return status.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L29) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1334) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1310)

<a id="op-1483237f7a9f6a"></a>
### Update call log

`operation_relationships_integrations_exotel_handler_business_behavior_update_call_log`

**Inputs** call\_payload, status = “Ringing”, call\_log = no value.

**State and service calls** call save on call\_log · commit.

**Explicit results** call\_log.

**Local steps**

- Set direction from call\_payload.get(“Direction”).
- Set call\_log from (call\_log or get\_call\_log(call\_payload)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in call\_log → get\_call\_log(call\_payload).
- Set status from get\_call\_log\_status(call\_payload, direction).
- Attempt the following.
  - If call\_log.
    - If status.
      - Set call\_log.status from status.
    - Set call\_log.to from (call\_payload.get(“DialWhomNumber”) or call\_payload.get(“To”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in call\_payload.get(“DialWhomNumber”) → call\_payload.get(“To”).
    - Set call\_log.duration from (call\_payload.get(“DialCallDuration”) or call\_payload.get(“ConversationDuration”) or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in call\_payload.get(“DialCallDuration”) → call\_payload.get(“ConversationDuration”) → 0.
    - Set call\_log.recording\_url from call\_payload.get(“RecordingUrl”) when call\_payload.get(“RecordingUrl”), otherwise empty text.
      - Value choice on call\_payload.get(“RecordingUrl”) — true gives call\_payload.get(“RecordingUrl”), false gives empty text.
    - Set call\_log.start\_time from call\_payload.get(“StartTime”).
    - Set call\_log.end\_time from call\_payload.get(“EndTime”).
    - If (direction equals “incoming” and call\_payload.get(“AgentEmail”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in direction equals “incoming” → call\_payload.get(“AgentEmail”).
      - Set call\_log.receiver from call\_payload.get(“AgentEmail”).
    - Evaluate call\_log.save(ignore\_permissions = true).
    - Evaluate Platform.db.commit().
    - Return call\_log.
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Error while updating call record”).
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L31) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1342) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1318)

## Service · Item

<a id="op-ac6fdc4b2f35ab"></a>
### Should sync

`operation_relationships_integrations_enterprise_application_item_business_behavior_should_sync`

**Inputs** doc.

**Declared result** bool.

**Explicit results** (should\_sync() and not doc.flags.get(“ignore\_crm\_sync”)).

**Local steps**

- Return (should\_sync() and not doc.flags.get(“ignore\_crm\_sync”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in should\_sync() → not doc.flags.get(“ignore\_crm\_sync”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L1702) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1282) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1258)

<a id="op-64ddc4a16be877"></a>
### Get item price rate

`operation_relationships_integrations_enterprise_application_item_business_behavior_get_item_price_rate`

**Inputs** item\_code, uom = no value.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit results** no value · row.price\_list\_rate when isinstance(row, dict), otherwise row at 1.

**Local steps**

- Bind dependencies get\_item\_price.
- Set price\_list from Platform.db.get\_single\_value(“Selling Settings”, “selling\_price\_list”).
- If not price\_list.
  - Return no value.
- Set pctx from Platform.\_dict(mapping(“price\_list” → price\_list, “uom” → uom, “transaction\_date” → Platform.utils.nowdate())).
- Set rows from get\_item\_price(pctx, item\_code).
- If not rows.
  - Return no value.
- Set row from rows at 0.
- Return row.price\_list\_rate when isinstance(row, dict), otherwise row at 1.
  - Value choice on isinstance(row, dict) — true gives row.price\_list\_rate, false gives row at 1.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Selling Settings”, “selling\_price\_list”) · clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L1786) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1279) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1255)

<a id="op-7b8b98a95a3b13"></a>
### Catalogue data

`operation_relationships_integrations_enterprise_application_item_business_behavior_catalogue_data`

**Inputs** doc.

**Declared result** dict.

**Explicit results** data.

**Local steps**

- Set data from mapping of f → doc.get(f) for f drawn from CATALOGUE\_FIELDS.
  - Draw f from CATALOGUE\_FIELDS.
- Set rate from get\_item\_price\_rate(doc.name, doc.get(“stock\_uom”)).
- If rate is distinct from no value.
  - Set data at “standard\_rate” from rate.
- Set data at “standard\_rate” from Platform.utils.flt(data at “standard\_rate”).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L2132) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1278) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1254)

<a id="op-46e54c6c2078a1"></a>
### After insert

`operation_relationships_integrations_enterprise_application_item_business_behavior_after_insert`

**Inputs** doc, method = no value.

**Record and data access** read “CRM Product” via get\_value · resolve a document from mapping(“doctype” → “CRM Product”, “product\_code” → doc.item\_code, “product\_name” → doc.item\_name, expand \_catalogue\_data(doc)) via get\_doc.

**State and service calls** call insert on product.

**Explicit results** no value.

**Local steps**

- If not \_should\_sync(doc).
  - Return no value.
- If Platform.db.get\_value(“CRM Product”, mapping(“Enterprise\_item\_code” → doc.name)).
  - Return no value.
- Set product from Platform.get\_doc(mapping(“doctype” → “CRM Product”, “product\_code” → doc.item\_code, “product\_name” → doc.item\_name, expand \_catalogue\_data(doc))).
- Set product.flags.ignore\_Enterprise\_sync from true.
- Evaluate product.insert(ignore\_permissions = true).
- Evaluate set\_links(doc.name, product.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L2384) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1275) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1251)

<a id="op-f923501863d3e0"></a>
### On update

`operation_relationships_integrations_enterprise_application_item_business_behavior_on_update`

**Inputs** doc, method = no value.

**Record and data access** read “CRM Product” via get\_value.

**State and service calls** request set\_value on “CRM Product”.

**Explicit results** no value.

**Local steps**

- If not \_should\_sync(doc).
  - Return no value.
- Set product\_name from Platform.db.get\_value(“CRM Product”, mapping(“Enterprise\_item\_code” → doc.name)).
- If not product\_name.
  - Return no value.
- Set data from mapping(“product\_name” → doc.item\_name, expand \_catalogue\_data(doc)).
- Set current from (Platform.db.get\_value(“CRM Product”, product\_name, list(data.keys()), as\_dict = true) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“CRM Product”, product\_name, list(data.keys()), as\_dict = true) → mapping().
- If not payload\_differs(data, current).
  - Return no value.
- Evaluate Platform.db.set\_value(“CRM Product”, product\_name, data).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L2724) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1281) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1257)

<a id="op-e993b0bef6c278"></a>
### Before rename

`operation_relationships_integrations_enterprise_application_item_business_behavior_before_rename`

**Inputs** doc, method = no value, olddn = no value, newdn = no value, merge = false.

**Local steps**

- Evaluate validate\_rename\_conflict(“Item”, olddn, newdn, merge).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L3104) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1277) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1253)

<a id="op-65c578871eacdc"></a>
### After rename

`operation_relationships_integrations_enterprise_application_item_business_behavior_after_rename`

**Inputs** doc, method = no value, olddn = no value, newdn = no value, merge = false.

**Local steps**

- Evaluate cascade\_rename(“Item”, olddn, newdn, merge).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L3214) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1276) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1252)

<a id="op-36a4b17602fa41"></a>
### On trash

`operation_relationships_integrations_enterprise_application_item_business_behavior_on_trash`

**Inputs** doc, method = no value.

**Record and data access** read “CRM Product” via get\_value.

**State and service calls** request set\_value on “CRM Product” · request delete\_doc for “CRM Product”.

**Explicit results** no value.

**Local steps**

- If (in\_cascade() or not \_should\_sync(doc)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in in\_cascade() → not \_should\_sync(doc).
  - Return no value.
- Set product from Platform.db.get\_value(“CRM Product”, mapping(“Enterprise\_item\_code” → doc.name)).
- If not product.
  - Return no value.
- Evaluate Platform.db.set\_value(“CRM Product”, product, “Enterprise\_item\_code”, no value).
- Set Platform.flags at CASCADE\_FLAG from true.
- Attempt the following.
  - Evaluate Platform.delete\_doc(“CRM Product”, product, ignore\_permissions = true).
- On exit, including pending return or failure.
  - Set Platform.flags at CASCADE\_FLAG from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L3324) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1280) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1256)

## Service · Live demo

<a id="op-6c38e3706da9d2"></a>
### Login

`operation_relationships_application_interface_live_demo_business_behavior_login`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** no value.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L112) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L94)

<a id="op-ee55a6f5b88036"></a>
### Validate reset password

`operation_relationships_application_interface_live_demo_business_behavior_validate_reset_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doc, event.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L299) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L113) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L95)

<a id="op-507cc14da10e65"></a>
### Validate user

`operation_relationships_application_interface_live_demo_business_behavior_validate_user`

**Inputs** doc, event.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Password cannot be reset by Demo User {}”.format(Platform.bold(Platform.conf.demo\_username)).

**Local steps**

- If (Platform.conf.demo\_username and Platform.session.user equals Platform.conf.demo\_username and doc.new\_password).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.demo\_username → Platform.session.user equals Platform.conf.demo\_username → doc.new\_password.
  - Call the validation error handler Platform.throw(translated “Password cannot be reset by Demo User {}”.format(Platform.bold(Platform.conf.demo\_username)), Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0012.json#L483) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L114) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L96)

## Service · Mirror sync

<a id="op-c0372ac2250c8a"></a>
### Mirror Sync.initialize

`operation_relationships_integrations_enterprise_application_mirror_sync_business_behavior_mirror_sync_initialize`

**Inputs** self, doc, doctype\_field, value\_field, extra\_dedup = no value, extra\_mirror\_flags = no value.

**Local steps**

- Set self.doc from doc.
- Set self.DOCTYPE\_FIELD from doctype\_field.
- Set self.VALUE\_FIELD from value\_field.
- Set self.\_extra\_dedup from extra\_dedup.
- Set self.\_extra\_mirror\_flags from (extra\_mirror\_flags or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in extra\_mirror\_flags → mapping().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L3645) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1288) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1264)

<a id="op-7221debb3c3236"></a>
### Mirror Sync.sync active

`operation_relationships_integrations_enterprise_application_mirror_sync_business_behavior_mirror_sync_sync_active`

**Inputs** self.

**Declared result** bool.

**Explicit results** should\_sync().

**Local steps**

- Return should\_sync().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L3811) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1292) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1268)
