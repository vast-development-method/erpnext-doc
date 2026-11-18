# Workflow, automation and dispatch · operations 35

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Push notification

<a id="op-7680517840fc80"></a>
### Push Notification.site port

`operation_foundation_push_notification_business_behavior_push_notification_site_port`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** str(site\_uri.port) · empty text.

**Local steps**

- Set site\_uri from urlparse(Platform.utils.get\_url()).
- If site\_uri.port is distinct from no value.
  - Return str(site\_uri.port).
- Return empty text.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1415) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L117)

<a id="op-12ada4b5b2f48b"></a>
### Auth webhook

`operation_foundation_push_notification_business_behavior_authentication_webhook`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** secret.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L142) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1403) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L105)

<a id="op-fbeca7b3ab9cfb"></a>
### Subscribe

`operation_foundation_push_notification_business_behavior_subscribe`

**Inputs** fcm\_token, project\_name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** mapping(“success” → success, “message” → message).

**Local steps**

- Set tuple(success, message) from PushNotification(project\_name).add\_token(Platform.session.user, fcm\_token).
- Return mapping(“success” → success, “message” → message).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L371) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1419) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L121)

<a id="op-5ba843c6101997"></a>
### Unsubscribe

`operation_foundation_push_notification_business_behavior_unsubscribe`

**Inputs** fcm\_token, project\_name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** mapping(“success” → success, “message” → message).

**Local steps**

- Set tuple(success, message) from PushNotification(project\_name).remove\_token(Platform.session.user, fcm\_token).
- Return mapping(“success” → success, “message” → message).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L558) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1420) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L122)

## Service · Queue

<a id="op-b2fe3a45b2bcc6"></a>
### Queue status

`operation_foundation_binding_foundation_automation_engine_queue_queue_status`

**Inputs** run\_after = no value.

**Declared result** str.

**Explicit results** “Scheduled” · “Pending”.

**Local steps**

- If (run\_after and get\_datetime(run\_after) &gt; now\_datetime()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in run\_after → get\_datetime(run\_after) &gt; now\_datetime().
  - Return “Scheduled”.
- Return “Pending”.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L211) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L451) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L427)

<a id="op-178d25d424c19a"></a>
### Effects key

`operation_foundation_binding_foundation_automation_engine_queue_effects_key`

**Inputs** row\_name.

**Declared result** str.

**Explicit results** formatted text automation\_effects::{row\_name}.

**Local steps**

- Return formatted text automation\_effects::{row\_name}.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L209) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L449) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L425)

<a id="op-34014b2aafea5d"></a>
### Mark effects delivered

`operation_foundation_binding_foundation_automation_engine_queue_mark_effects_delivered`

**Inputs** row\_name.

**Local steps**

- Evaluate Platform.cache.set\_value(effects\_key(row\_name), 1, expires\_in\_sec = EFFECTS\_TTL).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L210) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L450) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L426)

<a id="op-2a900ab0184727"></a>
### Effects delivered

`operation_foundation_binding_foundation_automation_engine_queue_effects_delivered`

**Inputs** row\_name.

**Declared result** bool.

**Explicit results** bool(Platform.cache.get\_value(effects\_key(row\_name), use\_local\_cache = false)).

**Local steps**

- Return bool(Platform.cache.get\_value(effects\_key(row\_name), use\_local\_cache = false)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L208) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L448) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L424)

<a id="op-33c0e12086b6c6"></a>
### Clear effects

`operation_foundation_binding_foundation_automation_engine_queue_clear_effects`

**Inputs** row\_name.

**Local steps**

- Evaluate Platform.cache.delete\_value(effects\_key(row\_name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L207) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L447) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L423)

## Service · Realtime

<a id="op-d0f5ec11c99a9d"></a>
### Publish progress

`operation_foundation_realtime_initialize_business_behavior_publish_progress`

**Inputs** percent, title = no value, doctype = no value, docname = no value, description = no value, task\_id = no value.

**Local steps**

- Evaluate publish\_realtime(“progress”, mapping(“percent” → percent, “title” → title, “description” → description), user = no value when (doctype and docname), otherwise Platform.session.user, doctype = doctype, docn ….
  - Value choice on (doctype and docname) — true gives no value, false gives Platform.session.user.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → docname.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from publish\_realtime(“progress”, mapping(“percent” → percent, “title” → title, “description” → description), user = no value when (doctype and docname), otherwise Platform.session.user, doctype = doctype, docn ….

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L4432) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1600) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L286)

<a id="op-2f13017dd1b95f"></a>
### Publish realtime

`operation_foundation_realtime_initialize_business_behavior_publish_realtime`

**Inputs** event = no value, message = no value, room = no value, user = no value, doctype = no value, docname = no value, task\_id = no value, after\_commit = false.

**Local steps**

- If message is identical to no value.
  - Set message from mapping().
- If (not task\_id and hasattr(Platform.local, “task\_id”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not task\_id → hasattr(Platform.local, “task\_id”).
  - Set task\_id from Platform.local.task\_id.
- If event is identical to no value.
  - Set event from “task\_progress” when task\_id, otherwise “global”.
    - Value choice on task\_id — true gives “task\_progress”, false gives “global”.
- Otherwise.
  - If (event equals “msgprint” and not user).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in event equals “msgprint” → not user.
    - Set user from Platform.session.user.
  - Otherwise.
    - If event equals “list\_update”.
      - Set doctype from (doctype or message.get(“doctype”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → message.get(“doctype”).
      - Set room from get\_doctype\_room(doctype).
    - Otherwise.
      - If event equals “docinfo\_update”.
        - Set room from get\_doc\_room(doctype, docname).
- If not room.
  - If task\_id.
    - Set after\_commit from false.
    - If “task\_id” does not belong to message.
      - Set message at “task\_id” from task\_id.
    - Set room from get\_task\_progress\_room(task\_id).
  - Otherwise.
    - If user.
      - Set room from get\_user\_room(user).
    - Otherwise.
      - If (doctype and docname).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → docname.
        - Set room from get\_doc\_room(doctype, docname).
      - Otherwise.
        - Set room from get\_site\_room().
- If after\_commit.
  - If not hasattr(Platform.local, “\_realtime\_log”).
    - Set Platform.local.\_realtime\_log from list().
    - Evaluate Platform.db.after\_commit.add(flush\_realtime\_log).
    - Evaluate Platform.db.after\_rollback.add(clear\_realtime\_log).
  - Set params from list(event, message, room).
  - If params does not belong to Platform.local.\_realtime\_log.
    - Evaluate Platform.local.\_realtime\_log.append(params).
- Otherwise.
  - Evaluate emit\_via\_redis(event, message, room).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L4661) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1601) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L287)

<a id="op-e92e7221da208c"></a>
### Flush realtime log

`operation_foundation_realtime_initialize_business_behavior_flush_realtime_log`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- If not hasattr(Platform.local, “\_realtime\_log”).
  - Return no value.
- For each args in Platform.local.\_realtime\_log.
  - Evaluate Platform.realtime.emit\_via\_redis(expanded args).
- Evaluate clear\_realtime\_log().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L5689) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1589) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L275)

<a id="op-fc24d3d66a9f22"></a>
### Clear realtime log

`operation_foundation_realtime_initialize_business_behavior_clear_realtime_log`

**Inputs** no declared parameters.

**Local steps**

- If hasattr(Platform.local, “\_realtime\_log”).
  - Remove Platform.local.\_realtime\_log.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L5824) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1587) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L273)

<a id="op-2c9bc2089c2a08"></a>
### Emit via redis

`operation_foundation_realtime_initialize_business_behavior_emit_via_cache_service`

**Inputs** event, message, room.

**Local steps**

- Bind dependencies get\_redis\_connection\_without\_auth.
- Within suppress(redis.exceptions.ConnectionError).
  - Set r from get\_redis\_connection\_without\_auth().
  - Evaluate r.publish(“events”, Platform.as\_json(mapping(“event” → event, “message” → message, “room” → room, “namespace” → Platform.local.site))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L5894) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1588) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L274)

<a id="op-676a16ab17b6da"></a>
### Has permission

`operation_foundation_realtime_initialize_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, name, ptype.

**Explicit result forms** Boolean true.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L6115) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1599) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L285)

<a id="op-4679451b835480"></a>
### Get socketio secret

`operation_foundation_realtime_initialize_business_behavior_get_realtime_transport_secret`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L6278) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1590) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L276)

<a id="op-550b4028bd25ce"></a>
### Get user info

`operation_foundation_realtime_initialize_business_behavior_get_user_info`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Record and data access** read “User” via get\_cached\_value.

**Explicit results** mapping() · mapping(“user” → Platform.session.user, “user\_type” → user\_type, “installed\_apps” → Platform.get\_installed\_apps()).

**Local steps**

- Set user\_type from Platform.session.data.user\_type.
- Set trusted\_secret from get\_socketio\_secret().
- Set provided\_secret from Platform.get\_request\_header(“X-Platform-Socket-Secret”).
- If (not provided\_secret or not hmac.compare\_digest(trusted\_secret.encode(), provided\_secret.encode())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not provided\_secret → not hmac.compare\_digest(trusted\_secret.encode(), provided\_secret.encode()).
  - Return mapping().
- If not user\_type.
  - Set user\_type from Platform.get\_cached\_value(“User”, Platform.session.user, “user\_type”).
- Return mapping(“user” → Platform.session.user, “user\_type” → user\_type, “installed\_apps” → Platform.get\_installed\_apps()).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“User”, Platform.session.user, “user\_type”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L3) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1595) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L281)

<a id="op-d334c8b9fe32c5"></a>
### Get doctype room

`operation_foundation_realtime_initialize_business_behavior_get_record_type_room`

**Inputs** doctype.

**Explicit results** formatted text doctype:{doctype}.

**Local steps**

- Return formatted text doctype:{doctype}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L6836) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1592) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L278)

<a id="op-344cf796ada606"></a>
### Get doc room

`operation_foundation_realtime_initialize_business_behavior_get_record_room`

**Inputs** doctype, docname.

**Explicit results** formatted text doc:{doctype}/{cstr(docname)}.

**Local steps**

- Return formatted text doc:{doctype}/{cstr(docname)}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L6889) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1591) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L277)

<a id="op-cfbe7e2b635b57"></a>
### Get user room

`operation_foundation_realtime_initialize_business_behavior_get_user_room`

**Inputs** user.

**Explicit results** formatted text user:{user}.

**Local steps**

- Return formatted text user:{user}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L6979) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1596) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L282)

<a id="op-3b71d8e0a3a47d"></a>
### Get site room

`operation_foundation_realtime_initialize_business_behavior_get_site_room`

**Inputs** no declared parameters.

**Explicit results** “all”.

**Local steps**

- Return “all”.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L7032) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1593) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L279)

<a id="op-1eda37bd7252ac"></a>
### Get task progress room

`operation_foundation_realtime_initialize_business_behavior_get_task_progress_room`

**Inputs** task\_id.

**Explicit results** formatted text task\_progress:{task\_id}.

**Local steps**

- Return formatted text task\_progress:{task\_id}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L7061) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1594) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L280)

<a id="op-8ed484c08e98d4"></a>
### Get website room

`operation_foundation_realtime_initialize_business_behavior_get_website_room`

**Inputs** no declared parameters.

**Explicit results** “website”.

**Local steps**

- Return “website”.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L7114) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1597) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L283)

<a id="op-897e917e24832e"></a>
### Publish to user

`operation_foundation_realtime_initialize_business_behavior_publish_to_user`

**Inputs** user, event, message = no value, after\_commit (named only, default false).

**Local steps**

- Evaluate publish\_realtime(event, message, user = user, after\_commit = after\_commit).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from publish\_realtime(event, message, user = user, after\_commit = after\_commit).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L7148) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1607) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L293)
