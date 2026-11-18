# Workflow, automation and dispatch · operations 34

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Model

<a id="op-7d25f611a6c0f4"></a>
### Litellm route

`operation_foundation_binding_foundation_flow_lib_model_litellm_route`

**Inputs** model\_id, api\_base.

**Declared result** tuple at tuple(str, (str bitwise or no value)).

**Explicit results** tuple(model\_id, api\_base) · grove\_route(model\_id, api\_base).

**Local steps**

- If not model\_id.startswith(formatted text {SITE\_PROVIDER}/).
  - Return tuple(model\_id, api\_base).
- Bind dependencies grove\_route.
- Return grove\_route(model\_id, api\_base).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L34) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1275) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1251)

## Service · Permissions

<a id="op-ff6718e68604d8"></a>
### Ensure flow role

`operation_foundation_binding_foundation_flow_permissions_ensure_flow_role`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** no value.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L115) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1356) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1332)

<a id="op-ef1b0651491fb4"></a>
### Has session permission

`operation_foundation_binding_foundation_flow_permissions_has_session_permission`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean true, a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L118) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1359) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1335)

<a id="op-bd37634d0bc474"></a>
### Session query conditions

`operation_foundation_binding_foundation_flow_permissions_session_query_conditions`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, doctype.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L122) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1363) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1339)

<a id="op-7ad7b65648e418"></a>
### Has memory permission

`operation_foundation_binding_foundation_flow_permissions_has_memory_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, user.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L116) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1357) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1333)

<a id="op-a25833dbb5a264"></a>
### Memory query conditions

`operation_foundation_binding_foundation_flow_permissions_memory_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L120) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1361) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1337)

<a id="op-9c13d2ba42a2d8"></a>
### Has role permission

`operation_foundation_binding_foundation_flow_permissions_has_role_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, user.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L117) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1358) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1334)

<a id="op-d9926077dd4695"></a>
### Role query conditions

`operation_foundation_binding_foundation_flow_permissions_role_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user, doctype.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L121) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1362) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1338)

<a id="op-52ab70d71a4cb7"></a>
### Has skill permission

`operation_foundation_binding_foundation_flow_permissions_has_skill_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, user.

**Explicit result forms** Boolean false, Boolean true, a value selected from the current context.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L119) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1360) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1336)

<a id="op-1af592d634a933"></a>
### Skill query conditions

`operation_foundation_binding_foundation_flow_permissions_skill_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L123) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1364) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1340)

## Service · Push notification

<a id="op-71c681c9c14f38"></a>
### Push Notification.initialize

`operation_foundation_push_notification_business_behavior_push_notification_initialize`

**Inputs** self, project\_name.

**Local steps**

- Set self.project\_name from project\_name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L4084) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1407) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L109)

<a id="op-c4258de146d966"></a>
### Push Notification.add token

`operation_foundation_push_notification_business_behavior_push_notification_add_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, user\_id, token.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L4143) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1404) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L106)

<a id="op-e8978ea625b947"></a>
### Push Notification.remove token

`operation_foundation_push_notification_business_behavior_push_notification_remove_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, user\_id, token.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L4318) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1409) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L111)

<a id="op-906cf91c474e2c"></a>
### Push Notification.add topic

`operation_foundation_push_notification_business_behavior_push_notification_add_topic`

**Inputs** self, topic\_name.

**Declared result** bool.

**Explicit results** data at “success”.

**Local steps**

- Set data from self.\_send\_post\_request(“notification\_relay.api.topic.add”, mapping(“topic\_name” → topic\_name)).
- Return data at “success”.

**Methods declared on this owner** [send post request](operations-034.md#op-b12f0acafef0c0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L4493) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1405) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L107)

<a id="op-adee50545f835f"></a>
### Push Notification.remove topic

`operation_foundation_push_notification_business_behavior_push_notification_remove_topic`

**Inputs** self, topic\_name.

**Declared result** bool.

**Explicit results** data at “success”.

**Local steps**

- Set data from self.\_send\_post\_request(“notification\_relay.api.topic.remove”, mapping(“topic\_name” → topic\_name)).
- Return data at “success”.

**Methods declared on this owner** [send post request](operations-034.md#op-b12f0acafef0c0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L4604) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1410) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L112)

<a id="op-f07e8db5917a43"></a>
### Push Notification.subscribe topic

`operation_foundation_push_notification_business_behavior_push_notification_subscribe_topic`

**Inputs** self, user\_id, topic\_name.

**Declared result** bool.

**Explicit results** data at “success”.

**Local steps**

- Set data from self.\_send\_post\_request(“notification\_relay.api.topic.subscribe”, mapping(“user\_id” → user\_id, “topic\_name” → topic\_name)).
- Return data at “success”.

**Methods declared on this owner** [send post request](operations-034.md#op-b12f0acafef0c0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L4715) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1417) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L119)

<a id="op-ff5416fc5cee27"></a>
### Push Notification.unsubscribe topic

`operation_foundation_push_notification_business_behavior_push_notification_unsubscribe_topic`

**Inputs** self, user\_id, topic\_name.

**Declared result** bool.

**Explicit results** data at “success”.

**Local steps**

- Set data from self.\_send\_post\_request(“notification\_relay.api.topic.unsubscribe”, mapping(“user\_id” → user\_id, “topic\_name” → topic\_name)).
- Return data at “success”.

**Methods declared on this owner** [send post request](operations-034.md#op-b12f0acafef0c0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L4854) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1418) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L120)

<a id="op-aeb4716a3d19b3"></a>
### Push Notification.send notification to user

`operation_foundation_push_notification_business_behavior_push_notification_send_notification_to_user`

**Inputs** self, user\_id, title, body, link = no value, icon = no value, data = no value, truncate\_body = true, strip\_html = true.

**Declared result** bool.

**Explicit results** response\_data at “success”.

**Explicit failure paths** Exception(“Body should be at max 1000 characters”).

**Local steps**

- If data is identical to no value.
  - Set data from mapping().
- If link.
  - Set data at “click\_action” from link.
- If icon.
  - Set data at “notification\_icon” from icon.
- Set body from cstr(body).
- If len(body) &gt; 1000.
  - If truncate\_body.
    - Set body from body at slice no value to 1000.
  - Otherwise.
    - Raise Exception(“Body should be at max 1000 characters”).
- If strip\_html.
  - Set body from Platform.utils.strip\_html(body).
- Set response\_data from self.\_send\_post\_request(“notification\_relay.api.send\_notification.user”, mapping(“user\_id” → user\_id, “title” → title, “body” → body, “data” → json.dumps(data))).
- Return response\_data at “success”.

**Methods declared on this owner** [send post request](operations-034.md#op-b12f0acafef0c0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L4993) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1412) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L114)

<a id="op-ea88da36ed95e4"></a>
### Push Notification.send notification to topic

`operation_foundation_push_notification_business_behavior_push_notification_send_notification_to_topic`

**Inputs** self, topic\_name, title, body, link = no value, icon = no value, data = no value, truncate\_body = true, strip\_html = true.

**Declared result** bool.

**Explicit results** response\_data at “success”.

**Explicit failure paths** Exception(“Body should be at max 1000 characters”).

**Local steps**

- If data is identical to no value.
  - Set data from mapping().
- If link.
  - Set data at “click\_action” from link.
- If icon.
  - Set data at “notification\_icon” from icon.
- Set body from cstr(body).
- If len(body) &gt; 1000.
  - If truncate\_body.
    - Set body from body at slice no value to 1000.
  - Otherwise.
    - Raise Exception(“Body should be at max 1000 characters”).
- If strip\_html.
  - Set body from Platform.utils.strip\_html(body).
- Set response\_data from self.\_send\_post\_request(“notification\_relay.api.send\_notification.topic”, mapping(“topic\_name” → topic\_name, “title” → title, “body” → body, “data” → json.dumps(data))).
- Return response\_data at “success”.

**Methods declared on this owner** [send post request](operations-034.md#op-b12f0acafef0c0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L5563) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1411) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L113)

<a id="op-a0105ca003c283"></a>
### Push Notification.is enabled

`operation_foundation_push_notification_business_behavior_push_notification_is_enabled`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Push Notification Settings” via get\_single\_value.

**Explicit results** sbool(Platform.db.get\_single\_value(“Push Notification Settings”, “enable\_push\_notification\_relay”)).

**Local steps**

- Return sbool(Platform.db.get\_single\_value(“Push Notification Settings”, “enable\_push\_notification\_relay”)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Push Notification Settings”, “enable\_push\_notification\_relay”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L6128) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1408) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L110)

<a id="op-67c5d499423600"></a>
### Push Notification.get credential

`operation_foundation_push_notification_business_behavior_push_notification_get_credential`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a structured result.

**Locally raised failures** Exception.

**Observed service boundaries** record lookup, record mutation request, transaction control.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L6217) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1406) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L108)

<a id="op-b12f0acafef0c0"></a>
### Push Notification.send post request

`operation_foundation_push_notification_business_behavior_push_notification_send_post_request`

**Inputs** self, method, params, use\_authentication = true.

**Explicit results** client.post\_api(method, params).

**Explicit failure paths** Exception(“Push Notification Relay is not enabled”).

**Local steps**

- If not self.is\_enabled().
  - Raise Exception(“Push Notification Relay is not enabled”).
- Set relay\_server\_endpoint from Platform.conf.get(“push\_relay\_server\_url”).
- If use\_authentication.
  - Set tuple(api\_key, api\_secret) from self.\_get\_credential().
  - Set client from PlatformClient(relay\_server\_endpoint, api\_key = api\_key, api\_secret = api\_secret).
- Otherwise.
  - Set client from PlatformClient(relay\_server\_endpoint).
- Set params at “project\_name” from self.project\_name.
- Set params at “site\_name” from self.\_site\_name.
- Return client.post\_api(method, params).

**Methods declared on this owner** [is enabled](operations-034.md#op-a0105ca003c283), [get credential](operations-034.md#op-67c5d499423600).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L6894) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1413) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L115)

<a id="op-569905f7bb6d69"></a>
### Push Notification.site name

`operation_foundation_push_notification_business_behavior_push_notification_site_name`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** urlparse(Platform.utils.get\_url()).hostname.

**Local steps**

- Return urlparse(Platform.utils.get\_url()).hostname.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L7244) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1414) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L116)

<a id="op-c7f6dc6246322e"></a>
### Push Notification.site protocol

`operation_foundation_push_notification_business_behavior_push_notification_site_protocol`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** urlparse(Platform.utils.get\_url()).scheme.

**Local steps**

- Return urlparse(Platform.utils.get\_url()).scheme.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L7323) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1416) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L118)
