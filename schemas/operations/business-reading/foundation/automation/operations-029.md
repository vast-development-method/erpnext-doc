# Workflow, automation and dispatch · operations 29

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Flow trigger

<a id="op-888507a03155c5"></a>
### Flow Trigger.before rename

`operation_foundation_binding_foundation_flow_doctype_flow_trigger_flow_trigger_flowtrigger_before_rename`

**Inputs** self, old, new, \_merge = false.

**Declared result** no value.

**Local steps**

- Evaluate block\_rename(self, old).
- Evaluate block\_slash\_in\_name(self, new).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L158) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1160) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1136)

<a id="op-e40cb1b0252ae5"></a>
### Flow Trigger.validate

`operation_foundation_binding_foundation_flow_doctype_flow_trigger_flow_trigger_flowtrigger_validate`

**Inputs** self.

**Local steps**

- Evaluate block\_slash\_in\_name(self).
- Evaluate validate\_immutable(self, tuple(“agent”, “event”, “target\_doctype”, “doc\_event”, …)).
- Evaluate self.\_validate\_event\_fields().
- Evaluate self.\_validate\_cron().
- Evaluate self.\_validate\_condition().
- Evaluate self.\_validate\_template().
- Evaluate self.\_validate\_run\_as().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate event fields](operations-029.md#op-7a461b13fbcacd), [validate cron](operations-029.md#op-3327b049bd1748), [validate condition](operations-029.md#op-ab5bc4475508c2), [validate template](operations-029.md#op-1d628271a3d4da), [validate run as](operations-029.md#op-215c6103595a4f).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L161) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1163) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1139)

<a id="op-1447f7d14dfe0d"></a>
### Flow Trigger.on change

`operation_foundation_binding_foundation_flow_doctype_flow_trigger_flow_trigger_flowtrigger_on_change`

**Inputs** self.

**Local steps**

- Evaluate clear\_trigger\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L159) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1161) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1137)

<a id="op-cf1ec8bd8da29e"></a>
### Flow Trigger.on trash

`operation_foundation_binding_foundation_flow_doctype_flow_trigger_flow_trigger_flowtrigger_on_trash`

**Inputs** self.

**Local steps**

- Evaluate block\_delete(self).
- Evaluate clear\_trigger\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L160) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1162) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1138)

<a id="op-215c6103595a4f"></a>
### Flow Trigger.validate run as

`operation_foundation_binding_foundation_flow_doctype_flow_trigger_flow_trigger_flowtrigger_validate_run_as`

**Inputs** self.

**Record and data access** read “User” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “You can only run a trigger as yourself.” · validation helper — translated “Run As must be an enabled user.” · validation helper — translated “{0} cannot use agent {1}.”.format(account, self.agent) · validation helper — translated “{0} cannot read {1}.”.format(account, translated self.target\_doctype).

**Local steps**

- If “System Manager” does not belong to Platform.get\_roles().
  - If (self.run\_as and self.run\_as differs from Platform.session.user).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.run\_as → self.run\_as differs from Platform.session.user.
    - Call the validation error handler Platform.throw(translated “You can only run a trigger as yourself.”, title = translated “Invalid Run As”).
  - Set self.run\_as from Platform.session.user.
- If not self.enabled.
  - Return no value.
- If (self.run\_as and (self.run\_as equals “Guest” or not Platform.db.get\_value(“User”, self.run\_as, “enabled”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.run\_as → (self.run\_as equals “Guest” or not Platform.db.get\_value(“User”, self.run\_as, “enabled”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.run\_as equals “Guest” → not Platform.db.get\_value(“User”, self.run\_as, “enabled”).
  - Call the validation error handler Platform.throw(translated “Run As must be an enabled user.”, title = translated “Invalid Run As”).
- Set account from (self.run\_as or self.owner).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.run\_as → self.owner.
- If not Platform.has\_permission(“Flow Agent”, “read”, self.agent, user = account).
  - Call the validation error handler Platform.throw(translated “{0} cannot use agent {1}.”.format(account, self.agent), title = translated “Invalid Run As”).
- If (self.event equals “DocType Event” and not Platform.has\_permission(self.target\_doctype, “read”, user = account)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.event equals “DocType Event” → not Platform.has\_permission(self.target\_doctype, “read”, user = account).
  - Call the validation error handler Platform.throw(translated “{0} cannot read {1}.”.format(account, translated self.target\_doctype), title = translated “Invalid Run As”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles(), Platform.has\_permission(“Flow Agent”, “read”, self.agent, user = account) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L165) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1167) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1143)

<a id="op-7a461b13fbcacd"></a>
### Flow Trigger.validate event fields

`operation_foundation_binding_foundation_flow_doctype_flow_trigger_flow_trigger_flowtrigger_validate_event_fields`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Target DocType is required for DocType Event triggers.” · validation helper — translated “Doc Event is required for DocType Event triggers.” · validation helper — translated “Invalid Doc Event: {0}”.format(self.doc\_event) · validation helper — translated “Cron Expression is required for Scheduled triggers.”.

**Local steps**

- If self.event equals “DocType Event”.
  - If not self.target\_doctype.
    - Call the validation error handler Platform.throw(translated “Target DocType is required for DocType Event triggers.”).
  - If not self.doc\_event.
    - Call the validation error handler Platform.throw(translated “Doc Event is required for DocType Event triggers.”).
  - If self.doc\_event does not belong to DOC\_EVENTS.
    - Call the validation error handler Platform.throw(translated “Invalid Doc Event: {0}”.format(self.doc\_event)).
- Otherwise.
  - If (self.event equals “Scheduled” and not self.cron\_expression).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.event equals “Scheduled” → not self.cron\_expression.
    - Call the validation error handler Platform.throw(translated “Cron Expression is required for Scheduled triggers.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L164) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1166) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1142)

<a id="op-3327b049bd1748"></a>
### Flow Trigger.validate cron

`operation_foundation_binding_foundation_flow_doctype_flow_trigger_flow_trigger_flowtrigger_validate_cron`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Invalid cron expression: {0}”.format(str(e)).

**Local steps**

- If (self.event differs from “Scheduled” or not self.cron\_expression).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.event differs from “Scheduled” → not self.cron\_expression.
  - Return no value.
- Bind dependencies CroniterBadCronError, croniter.
- Attempt the following.
  - Evaluate croniter(self.cron\_expression).
- On failure (tuple(CroniterBadCronError, ValueError)) bound to e.
  - Call the validation error handler Platform.throw(translated “Invalid cron expression: {0}”.format(str(e)), title = translated “Invalid Cron”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L163) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1165) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1141)

<a id="op-ab5bc4475508c2"></a>
### Flow Trigger.validate condition

`operation_foundation_binding_foundation_flow_doctype_flow_trigger_flow_trigger_flowtrigger_validate_condition`

**Inputs** self.

**Local steps**

- Bind dependencies validate\_condition.
- Evaluate validate\_condition(self.condition).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L162) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1164) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1140)

<a id="op-1d628271a3d4da"></a>
### Flow Trigger.validate template

`operation_foundation_binding_foundation_flow_doctype_flow_trigger_flow_trigger_flowtrigger_validate_template`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Invalid Jinja template: {0}”.format(str(e)).

**Local steps**

- Bind dependencies TemplateSyntaxError.
- Bind dependencies SandboxedEnvironment.
- Attempt the following.
  - Evaluate SandboxedEnvironment().parse((self.prompt\_template or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.prompt\_template → empty text.
- On failure (TemplateSyntaxError) bound to e.
  - Call the validation error handler Platform.throw(translated “Invalid Jinja template: {0}”.format(str(e)), title = translated “Invalid Template”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L166) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1168) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1144)

## Service · Handlers

<a id="op-072be5829c1355"></a>
### User room

`operation_foundation_realtime_handlers_business_behavior_user_room`

**Inputs** user.

**Declared result** str.

**Explicit results** formatted text user:{user}.

**Local steps**

- Return formatted text user:{user}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L2305) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1586) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L272)

<a id="op-e3a3983f266f62"></a>
### Doctype room

`operation_foundation_realtime_handlers_business_behavior_record_type_room`

**Inputs** doctype.

**Declared result** str.

**Explicit results** formatted text doctype:{doctype}.

**Local steps**

- Return formatted text doctype:{doctype}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L2365) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1579) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L265)

<a id="op-0af96e33200349"></a>
### Doc room

`operation_foundation_realtime_handlers_business_behavior_record_room`

**Inputs** doctype, docname.

**Declared result** str.

**Explicit results** formatted text doc:{doctype}/{docname}.

**Local steps**

- Return formatted text doc:{doctype}/{docname}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L2425) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1577) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L263)

<a id="op-e442eb2c1e83b8"></a>
### Task room

`operation_foundation_realtime_handlers_business_behavior_task_room`

**Inputs** task\_id.

**Declared result** str.

**Explicit results** formatted text task\_progress:{task\_id}.

**Local steps**

- Return formatted text task\_progress:{task\_id}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L2512) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1583) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L269)

<a id="op-0a89caee6956c2"></a>
### Open doc room

`operation_foundation_realtime_handlers_business_behavior_open_record_room`

**Inputs** doctype, docname.

**Declared result** str.

**Explicit results** formatted text open\_doc:{doctype}/{docname}.

**Local steps**

- Return formatted text open\_doc:{doctype}/{docname}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L2572) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1572) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L258)

<a id="op-211e0ba6de7f6b"></a>
### On connect

`operation_foundation_realtime_handlers_business_behavior_on_connect`

**Inputs** socket.

**Wrappers, in declaration order** realtime.on(“connect”, allow\_guest = true).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Evaluate await socket.join(user\_room(socket.user)).
- Evaluate await socket.join(WEBSITE\_ROOM).
- If socket.user\_type equals “System User”.
  - Evaluate await socket.join(SITE\_ROOM).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.join(user\_room(socket.user)), socket.join(WEBSITE\_ROOM) and 1 further calls.

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L2659) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1569) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L255)

<a id="op-89bf1791290e1e"></a>
### Ping

`operation_foundation_realtime_handlers_business_behavior_ping`

**Inputs** socket.

**Wrappers, in declaration order** realtime.on(“ping”, allow\_guest = true).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Evaluate await socket.emit(“pong”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.emit(“pong”).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L2847) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1573) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L259)

<a id="op-d338773b0ed0c9"></a>
### Doctype subscribe

`operation_foundation_realtime_handlers_business_behavior_record_type_subscribe`

**Inputs** socket, doctype.

**Wrappers, in declaration order** realtime.on(“doctype\_subscribe”, allow\_guest = true).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Set room from doctype\_room(doctype).
- If (socket.sid does not belong to socket.participants(room) and await socket.has\_permission(doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in socket.sid does not belong to socket.participants(room) → await socket.has\_permission(doctype).
  - Evaluate await socket.join(room).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.participants(room), socket.has\_permission(doctype) and 1 further calls · effective access from socket.has\_permission(doctype).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L2) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1580) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L266)

<a id="op-e8e3ce4aefd51f"></a>
### Doctype unsubscribe

`operation_foundation_realtime_handlers_business_behavior_record_type_unsubscribe`

**Inputs** socket, doctype.

**Wrappers, in declaration order** realtime.on(“doctype\_unsubscribe”, allow\_guest = true).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Evaluate await socket.leave(doctype\_room(doctype)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.leave(doctype\_room(doctype)).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L3089) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1581) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L267)

<a id="op-6fd3738026b89e"></a>
### Task subscribe

`operation_foundation_realtime_handlers_business_behavior_task_subscribe`

**Inputs** socket, task\_id.

**Wrappers, in declaration order** realtime.on(“task\_subscribe”, allow\_guest = true).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Evaluate await socket.join(task\_room(task\_id)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.join(task\_room(task\_id)).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L3209) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1584) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L270)

<a id="op-dba9c16a272b22"></a>
### Task unsubscribe

`operation_foundation_realtime_handlers_business_behavior_task_unsubscribe`

**Inputs** socket, task\_id.

**Wrappers, in declaration order** realtime.on(“task\_unsubscribe”, allow\_guest = true).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Evaluate await socket.leave(task\_room(task\_id)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.leave(task\_room(task\_id)).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L3329) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1585) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L271)

<a id="op-f9f94103a602a9"></a>
### Progress subscribe

`operation_foundation_realtime_handlers_business_behavior_progress_subscribe`

**Inputs** socket, task\_id.

**Wrappers, in declaration order** realtime.on(“progress\_subscribe”, allow\_guest = true).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Evaluate await socket.join(task\_room(task\_id)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.join(task\_room(task\_id)).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L3449) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1574) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L260)

<a id="op-176a01faa069f7"></a>
### Doc subscribe

`operation_foundation_realtime_handlers_business_behavior_record_subscribe`

**Inputs** socket, doctype, docname.

**Wrappers, in declaration order** realtime.on(“doc\_subscribe”, allow\_guest = true).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Set room from doc\_room(doctype, docname).
- If (socket.sid does not belong to socket.participants(room) and await socket.has\_permission(doctype, docname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in socket.sid does not belong to socket.participants(room) → await socket.has\_permission(doctype, docname).
  - Evaluate await socket.join(room).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.participants(room), socket.has\_permission(doctype, docname) and 1 further calls · effective access from socket.has\_permission(doctype, docname).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L117) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1578) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L264)

<a id="op-65b22a06172d07"></a>
### Doc unsubscribe

`operation_foundation_realtime_handlers_business_behavior_record_unsubscribe`

**Inputs** socket, doctype, docname.

**Wrappers, in declaration order** realtime.on(“doc\_unsubscribe”, allow\_guest = true).

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Evaluate await socket.leave(doc\_room(doctype, docname)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.leave(doc\_room(doctype, docname)).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L3738) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1582) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L268)

<a id="op-6f7e5483843f97"></a>
### Doc open

`operation_foundation_realtime_handlers_business_behavior_record_open`

**Inputs** socket, doctype, docname.

**Wrappers, in declaration order** realtime.on(“doc\_open”, allow\_guest = true).

The declaration is asynchronous.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set room from open\_doc\_room(doctype, docname).
- If socket.sid does not belong to socket.participants(room).
  - If not await socket.has\_permission(doctype, docname).
    - Return no value.
  - Evaluate await socket.join(room).
- Set tracked from socket.get(“subscribed\_documents”, list()).
- Set pair from list(doctype, docname).
- If pair does not belong to tracked.
  - Evaluate tracked.append(pair).
  - Evaluate await socket.set(“subscribed\_documents”, tracked).
- Evaluate await notify\_doc\_viewers(socket, doctype, docname).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.participants(room), socket.has\_permission(doctype, docname) and 3 further calls · effective access from socket.has\_permission(doctype, docname).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L116) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1576) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L262)
