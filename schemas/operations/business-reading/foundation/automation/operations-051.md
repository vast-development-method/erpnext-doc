# Workflow, automation and dispatch · operations 51

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Tool

<a id="op-1bc528aff2985e"></a>
### Inline pydantic refs

`operation_foundation_binding_foundation_flow_lib_tool_inline_pydantic_refs`

**Inputs** schema.

**Declared result** dict at tuple(str, Any).

**Explicit results** schema · walk(schema).

**Local steps**

- Set defs from schema.pop(“$defs”, mapping()).
- If not defs.
  - Return schema.
- Set resolved from mapping().
- Bind local operation walk for subsequent calls.
- For each tuple(def\_name, def\_schema) in defs.items().
  - Set resolved at def\_name from walk(def\_schema).
- Return walk(schema).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L82) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1323) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1299)

<a id="op-85a4a328ed4474"></a>
### Inline pydantic refs.walk

`operation_foundation_binding_foundation_flow_lib_tool_inline_pydantic_refs_walk`

**Inputs** node.

**Declared result** Any.

**Explicit results** list of walk(item) for item drawn from node · node · resolved at def\_name · walk(defs at def\_name) · mapping(“type” → “object”) · 1 additional forms in the steps below.

**Local steps**

- If isinstance(node, list).
  - Return list of walk(item) for item drawn from node.
    - Draw item from node.
- If not isinstance(node, dict).
  - Return node.
- Set ref from node.get(“$ref”).
- If (isinstance(ref, str) and ref.startswith(“#/$defs/”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(ref, str) → ref.startswith(“#/$defs/”).
  - Set def\_name from ref.split(“/”) at negative 1.
  - If def\_name belongs to resolved.
    - Return resolved at def\_name.
  - If def\_name belongs to defs.
    - Return walk(defs at def\_name).
  - Return mapping(“type” → “object”).
- Return mapping of key → walk(value) for tuple(key, value) drawn from node.items().
  - Draw tuple(key, value) from node.items().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L83) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1324) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1300)

<a id="op-799c2517412730"></a>
### Enum schema

`operation_foundation_binding_foundation_flow_lib_tool_enum_schema`

**Inputs** values.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“type” → “string”, “enum” → values) · mapping(“type” → “boolean”, “enum” → values) · mapping(“type” → “integer”, “enum” → values) · mapping(“type” → “number”, “enum” → values) · mapping(“enum” → values).

**Local steps**

- Set value\_types from set of type(v) for v drawn from values.
  - Draw v from values.
- If value\_types equals set(str).
  - Return mapping(“type” → “string”, “enum” → values).
- If value\_types equals set(bool).
  - Return mapping(“type” → “boolean”, “enum” → values).
- If value\_types ≤ set(int).
  - Return mapping(“type” → “integer”, “enum” → values).
- If value\_types ≤ set(int, float).
  - Return mapping(“type” → “number”, “enum” → values).
- Return mapping(“enum” → values).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L81) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1322) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1298)

## Service · Trigger

<a id="op-c34267c7addb61"></a>
### Sync triggers

`operation_foundation_binding_foundation_flow_lib_trigger_sync_triggers`

**Inputs** \_app = no value.

**Declared result** no value.

**Record and data access** read “Flow Trigger” via get\_all.

**State and service calls** request set\_value on “Flow Run” · request delete\_doc for “Flow Trigger”.

**Local steps**

- Set declared from set().
- Set synced from set().
- For each path in Platform.get\_hooks(“flow\_triggers”).
  - Set triggers from no value.
  - Within skip\_if\_invalid(formatted text Flow Triggers of {path} skipped).
    - Set triggers from Platform.get\_attr(path)().
  - If triggers is identical to no value.
    - Set app from path.split(“.”, 1) at 0.
    - Evaluate declared.update(Platform.get\_all(“Flow Trigger”, mapping(“is\_system\_generated” → 1, “app” → app), pluck = “name”)).
    - Continue with the next iteration or loop test.
  - For each trigger in triggers.
    - Evaluate declared.add(trigger.name).
    - If trigger.name belongs to synced.
      - Evaluate log\_skipped(formatted text Flow Trigger {trigger.name} skipped, translated “Flow Trigger {0} is declared more than once.”.format(trigger.name)).
      - Continue with the next iteration or loop test.
    - Evaluate synced.add(trigger.name).
    - Within skip\_if\_invalid(formatted text Flow Trigger {trigger.name} skipped).
      - Evaluate trigger.sync().
- For each name in Platform.get\_all(“Flow Trigger”, mapping(“is\_system\_generated” → 1), pluck = “name”).
  - If name does not belong to declared.
    - Evaluate Platform.db.set\_value(“Flow Run”, mapping(“trigger” → name), “trigger”, no value, update\_modified = false).
    - Evaluate Platform.delete\_doc(“Flow Trigger”, name, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“flow\_triggers”), Platform.get\_attr(path).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L92) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1333) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1309)

<a id="op-ad802983a4c172"></a>
### Trigger.initialize

`operation_foundation_binding_foundation_flow_lib_trigger_trigger_init`

**Inputs** self, title (named only), agent (named only), prompt (named only), doctype (named only, default no value), doc\_event (named only, default no value), cron (named only, default no value), condition (named only, default no value), run\_as (named only, default no value).

**Local steps**

- Set self.app from nested operand in the contract.\_getframe(1).f\_globals at “\_\_name\_\_”.split(“.”, 1) at 0.
- Set self.name from formatted text {self.app}/{title}.
- Set self.agent from with\_app\_prefix(self.app, agent).
- Set self.prompt from prompt.
- Set self.doctype from doctype.
- Set self.doc\_event from doc\_event.
- Set self.cron from cron.
- Set self.condition from condition.
- Set self.run\_as from run\_as.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L93) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1334) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1310)

<a id="op-204e085ca501b4"></a>
### Trigger.sync

`operation_foundation_binding_foundation_flow_lib_trigger_trigger_sync`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Flow Agent” via exists · read “Flow Trigger” via exists · resolve a document from “Flow Trigger” via get\_doc · resolve a document from mapping(“doctype” → “Flow Trigger”, “title” → self.name, “app” → self.app, “enabled” → 1, …) via get\_doc.

**State and service calls** call save on doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Flow Trigger {0} needs a doctype or a cron, not both.”.format(self.name).

**Local steps**

- If (self.cron and self.doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.cron → self.doctype.
  - Call the validation error handler Platform.throw(translated “Flow Trigger {0} needs a doctype or a cron, not both.”.format(self.name), title = translated “Invalid Trigger”).
- If not Platform.db.exists(“Flow Agent”, self.agent).
  - Return no value.
- If Platform.db.exists(“Flow Trigger”, self.name).
  - Set doc from Platform.get\_doc(“Flow Trigger”, self.name).
- Otherwise.
  - Set doc from Platform.get\_doc(mapping(“doctype” → “Flow Trigger”, “title” → self.name, “app” → self.app, “enabled” → 1, …)).
- Evaluate doc.update(mapping(“agent” → self.agent, “event” → “Scheduled” when self.cron, otherwise “DocType Event”, “target\_doctype” → self.doctype, “doc\_event” → self.doc\_event, …)).
  - Value choice on self.cron — true gives “Scheduled”, false gives “DocType Event”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.run\_as → “Administrator”.
- Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L94) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1335) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1311)

## Service · Triggers

<a id="op-ee793f89a477f8"></a>
### Dispatch

`operation_foundation_binding_foundation_flow_triggers_triggers_dispatch`

**Inputs** doc, method = no value.

**Declared result** no value.

**State and service calls** enqueue with “Platform.flow.triggers.fire”.

**Explicit results** no value.

**Local steps**

- If method does not belong to DOC\_EVENTS.
  - Return no value.
- If doc.doctype belongs to set(“Flow Run”, “Flow Trigger”, “Flow Agent”, “Flow Tool”, …).
  - Return no value.
- If (Platform.flags.in\_install or Platform.flags.in\_migrate or Platform.flags.in\_install\_db).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_migrate → Platform.flags.in\_install\_db.
  - Return no value.
- Set triggers from \_doctype\_triggers(doc.doctype, method).
- Set deleted\_doc from doc.as\_dict() when (triggers and method equals “on\_trash”), otherwise no value.
  - Value choice on (triggers and method equals “on\_trash”) — true gives doc.as\_dict(), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in triggers → method equals “on\_trash”.
- For each trigger in triggers.
  - If not Platform.has\_permission(doc.doctype, “read”, doc, user = (trigger.run\_as or trigger.owner)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in trigger.run\_as → trigger.owner.
    - Continue with the next iteration or loop test.
  - Evaluate Platform.enqueue(“Platform.flow.triggers.fire”, enqueue\_after\_commit = true, trigger = trigger.name, target\_doctype = doc.doctype, target\_name = doc.name, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doc.doctype, “read”, doc, user = (trigger.run\_as or trigger.owner)) · service or queued work from Platform.enqueue(“Platform.flow.triggers.fire”, enqueue\_after\_commit = true, trigger = trigger.name, target\_doctype = doc.doctype, target\_name = doc.name, …).

**Boundaries to resolve** external or queued work, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L198) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1439) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1415)

<a id="op-7e7afd41c2248f"></a>
### Dispatch scheduled

`operation_foundation_binding_foundation_flow_triggers_triggers_dispatch_scheduled`

**Inputs** no declared parameters.

**Declared result** no value.

**Record and data access** read “Flow Trigger” via get\_all.

**State and service calls** request set\_value on “Flow Trigger” · enqueue with “Platform.flow.triggers.fire”.

**Local steps**

- Bind dependencies CroniterBadCronError, croniter.
- Set now from Platform.utils.now\_datetime().
- Set triggers from Platform.get\_all(“Flow Trigger”, filters = mapping(“event” → “Scheduled”, “enabled” → 1), fields = list(“name”, “cron\_expression”, “last\_fired\_at”, “creation”)).
- For each t in triggers.
  - Set anchor from Platform.utils.get\_datetime((t.last\_fired\_at or t.creation)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in t.last\_fired\_at → t.creation.
  - Attempt the following.
    - Set nxt from croniter(t.cron\_expression, anchor).get\_next(datetime).
  - On failure (tuple(CroniterBadCronError, ValueError)).
    - Evaluate Platform.log\_error(title = formatted text Flow Trigger cron parse failed: {t.name}).
    - Continue with the next iteration or loop test.
  - If nxt ≤ now.
    - Evaluate Platform.db.set\_value(“Flow Trigger”, t.name, “last\_fired\_at”, now, update\_modified = false).
    - Evaluate Platform.enqueue(“Platform.flow.triggers.fire”, trigger = t.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now\_datetime() · service or queued work from Platform.enqueue(“Platform.flow.triggers.fire”, trigger = t.name).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L199) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1440) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1416)

<a id="op-69402ac3713338"></a>
### Fire

`operation_foundation_binding_foundation_flow_triggers_triggers_fire`

**Inputs** trigger, target\_doctype = no value, target\_name = no value, deleted\_doc = no value.

**Declared result** (str bitwise or no value).

**Record and data access** resolve a document from “Flow Trigger” via get\_doc · resolve a document from deleted\_doc via get\_doc · resolve a document from target\_doctype via get\_doc · resolve a document from “Flow Agent” via get\_doc.

**Explicit results** no value · run.name.

**Local steps**

- Set t from Platform.get\_doc(“Flow Trigger”, trigger).
- If not t.enabled.
  - Return no value.
- Set original\_user from Platform.session.user.
- Evaluate Platform.set\_user((t.run\_as or t.owner)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in t.run\_as → t.owner.
- Attempt the following.
  - Set doc from no value.
  - If deleted\_doc.
    - Set doc from Platform.get\_doc(deleted\_doc).
    - Set target\_doctype, target\_name from no value.
  - Otherwise.
    - If (target\_doctype and target\_name).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in target\_doctype → target\_name.
      - Attempt the following.
        - Set doc from Platform.get\_doc(target\_doctype, target\_name).
      - On failure (Platform.DoesNotExistError).
        - Return no value.
      - If not Platform.has\_permission(target\_doctype, “read”, doc).
        - Return no value.
  - If doc.
    - Evaluate doc.apply\_fieldlevel\_read\_permissions().
  - Set fields from \_Fields(doc.as\_dict()) when doc, otherwise no value.
    - Value choice on doc — true gives \_Fields(doc.as\_dict()), false gives no value.
  - If (fields and t.condition and not \_eval\_condition(t.condition, fields)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fields → t.condition → not \_eval\_condition(t.condition, fields).
    - Return no value.
  - Set prompt from SandboxedEnvironment(finalize = deferred anonymous expression).from\_string(t.prompt\_template).render(doc = fields, now = Platform.utils.now\_datetime()).
  - Set agent\_doc from Platform.get\_doc(“Flow Agent”, t.agent).
  - Set run from agent\_doc.run(prompt, source = “Trigger”, trigger = t.name, reference\_doctype = target\_doctype when doc, otherwise no value, reference\_name = target\_name when doc, otherwise no value).
    - Value choice on doc — true gives target\_doctype, false gives no value.
    - Value choice on doc — true gives target\_name, false gives no value.
  - Return run.name.
- On exit, including pending return or failure.
  - Evaluate Platform.set\_user(original\_user).

**Values supplied outside this operation** effective access from Platform.has\_permission(target\_doctype, “read”, doc) · clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L204) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1445) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1421)

<a id="op-6ead108678945d"></a>
### Clear trigger cache

`operation_foundation_binding_foundation_flow_triggers_triggers_clear_trigger_cache`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Bind local operation forget for subsequent calls.
- Evaluate forget().
- Evaluate Platform.db.after\_commit.add(forget).
- Evaluate Platform.db.after\_rollback.add(forget).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L196) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1437) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1413)

<a id="op-d31603797c45ca"></a>
### Clear trigger cache.forget

`operation_foundation_binding_foundation_flow_triggers_triggers_clear_trigger_cache_forget`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.client\_cache.delete\_keys(CACHE\_PREFIX).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L197) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1438) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1414)

<a id="op-e976a4b26c9ba4"></a>
### Doctype triggers

`operation_foundation_binding_foundation_flow_triggers_triggers_doctype_triggers`

**Inputs** target\_doctype, doc\_event.

**Declared result** list.

**Explicit results** list of t for t drawn from triggers where t.doc\_event equals doc\_event.

**Local steps**

- Set triggers from Platform.client\_cache.get\_value(formatted text {CACHE\_PREFIX}{target\_doctype}, generator = deferred anonymous expression).
- Return list of t for t drawn from triggers where t.doc\_event equals doc\_event.
  - Draw t from triggers, keep a combination only if (t.doc\_event equals doc\_event).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L200) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1441) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1417)

<a id="op-8d356039ec34b3"></a>
### Enabled doctype triggers

`operation_foundation_binding_foundation_flow_triggers_triggers_enabled_doctype_triggers`

**Inputs** target\_doctype.

**Declared result** list.

**Record and data access** read “Flow Trigger” via get\_all.

**Explicit results** Platform.get\_all(“Flow Trigger”, filters = mapping(“event” → “DocType Event”, “target\_doctype” → target\_doctype, “enabled” → 1), fields = list(“name”, “doc\_event”, “condition”, “run\_as”, …)).

**Local steps**

- Return Platform.get\_all(“Flow Trigger”, filters = mapping(“event” → “DocType Event”, “target\_doctype” → target\_doctype, “enabled” → 1), fields = list(“name”, “doc\_event”, “condition”, “run\_as”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L201) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1442) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1418)

<a id="op-ddb97d6099edf0"></a>
### Fields.getattribute

`operation_foundation_binding_foundation_flow_triggers_triggers_fields_getattribute`

**Inputs** self, name.

**Explicit results** dict.\_\_getitem\_\_(self, name) · super().\_\_getattribute\_\_(name).

**Local steps**

- If dict.\_\_contains\_\_(self, name).
  - Return dict.\_\_getitem\_\_(self, name).
- Return super().\_\_getattribute\_\_(name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L203) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1444) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1420)

<a id="op-b072d1174d89dc"></a>
### Eval condition

`operation_foundation_binding_foundation_flow_triggers_triggers_eval_condition`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** condition, doc.

**Explicit result forms** Boolean false, the result of a delegated call.

**Observed service boundaries** diagnostic or audit logging.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L202) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1443) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1419)

## Service · Util

<a id="op-ed647c0aa8eb5f"></a>
### Read header

`operation_foundation_realtime_util_business_behavior_read_header`

**Inputs** environ, name.

**Declared result** (str bitwise or no value).

**Explicit results** environ.get((“HTTP\_” + name.upper().replace(“-”, “\_”))).

**Local steps**

- Return environ.get((“HTTP\_” + name.upper().replace(“-”, “\_”))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L3423) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1660) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L346)

<a id="op-b6d074a5502df4"></a>
### Get hostname

`operation_foundation_realtime_util_business_behavior_get_hostname`

**Inputs** url.

**Declared result** (str bitwise or no value).

**Explicit results** no value · urlsplit(url).hostname.

**Local steps**

- If not url.
  - Return no value.
- If “://” does not belong to url.
  - Set url from formatted text //{url}.
- Return urlsplit(url).hostname.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L3543) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1658) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L344)

<a id="op-3f4127d1267a5d"></a>
### Resolve site name

`operation_foundation_realtime_util_business_behavior_resolve_site_name`

**Inputs** environ, config.

**Declared result** (str bitwise or no value).

**Explicit results** get\_hostname(site\_header) · config.default\_site · get\_hostname(origin) · get\_hostname(host).

**Local steps**

- Set site\_header from read\_header(environ, “X-Platform-Site-Name”).
- Set host from read\_header(environ, “Host”).
- Set origin from read\_header(environ, “Origin”).
- If site\_header.
  - Return get\_hostname(site\_header).
- If (config.default\_site and get\_hostname(host) belongs to tuple(“localhost”, “127.0.0.1”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in config.default\_site → get\_hostname(host) belongs to tuple(“localhost”, “127.0.0.1”).
  - Return config.default\_site.
- If origin.
  - Return get\_hostname(origin).
- Return get\_hostname(host).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L3691) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1661) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L347)

<a id="op-7c0fa3901d4551"></a>
### Get url

`operation_foundation_realtime_util_business_behavior_get_resource_address`

**Inputs** path, config.

**Declared result** str.

**Explicit results** (base + (path or empty text)).

**Local steps**

- Set base from (config.webserver\_host or “127.0.0.1”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in config.webserver\_host → “127.0.0.1”.
- Set port from config.webserver\_port.
- If “://” does not belong to base.
  - Set base from formatted command or address in the contract.
  - Set port from (port or 8000).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in port → 8000.
- Set parts from urlsplit(base).
- Set base from formatted text {parts.scheme}://{parts.netloc}.
- If (parts.port is identical to no value and port).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parts.port is identical to no value → port.
  - Set base from formatted text {base}:{port}.
- Return (base + (path or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in path → empty text.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L5) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1659) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L345)

## Record · Workflow

[Record definition](../../../../data/record-types/workflow.json)

<a id="op-e87ff6a3617814"></a>
### Workflow.validate

`operation_foundation_workflow_record_definitions_workflow_business_behavior_workflow_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_active().
- Evaluate self.validate\_docstatus().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set active](operations-052.md#op-af763f43d843cc), [validate docstatus](operations-052.md#op-028cfb3a549146).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L973) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L693) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1637)

<a id="op-142062fe46e65e"></a>
### Workflow.on update

`operation_foundation_workflow_record_definitions_workflow_business_behavior_workflow_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.create\_custom\_field\_for\_workflow\_state().
- Evaluate self.update\_default\_workflow\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create custom field for workflow state](operations-051.md#op-7e678cd3a88c01), [update default workflow status](operations-051.md#op-3fcef2169d6aa3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L1044) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L690) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1634)

<a id="op-b435a93c379c09"></a>
### Workflow.on trash

`operation_foundation_workflow_record_definitions_workflow_business_behavior_workflow_on_trash`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_cache(doctype = self.document\_type).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L1115) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L689) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1633)

<a id="op-7e678cd3a88c01"></a>
### Workflow.create custom field for workflow state

`operation_foundation_workflow_record_definitions_workflow_business_behavior_workflow_create_custom_field_for_workflow_state`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Custom Field”, “dt” → self.document\_type, “\_\_islocal” → 1, “fieldname” → self.workflow\_state\_field, …) via get\_doc.

**State and service calls** call save on Platform.get\_doc(mapping(“doctype” → “Custom Field”, “dt” → self.document\_type, “\_\_islocal” → 1, “fieldname” → self.workflow\_state\_field, …)) · msgprint with translated “Created Custom Field {0} in {1}”.format(self.workflow\_state\_field, self.document\_type).

**Local steps**

- Evaluate Platform.clear\_cache(doctype = self.document\_type).
- Set meta from Platform.get\_meta(self.document\_type).
- If not meta.get\_field(self.workflow\_state\_field).
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Custom Field”, “dt” → self.document\_type, “\_\_islocal” → 1, “fieldname” → self.workflow\_state\_field, …)).save().
  - Evaluate Platform.msgprint(translated “Created Custom Field {0} in {1}”.format(self.workflow\_state\_field, self.document\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L1178) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L688) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1632)

<a id="op-3fcef2169d6aa3"></a>
### Workflow.update default workflow status

`operation_foundation_workflow_record_definitions_workflow_business_behavior_workflow_update_default_workflow_status`

**Inputs** self.

**Local steps**

- Set docstatus\_map from mapping().
- Set states from self.get(“states”).
- Set TargetDocType from Platform.qb.DocType(self.document\_type).
- Set state\_field from getattr(TargetDocType, self.workflow\_state\_field).
- For each d in states.
  - If d.doc\_status does not belong to docstatus\_map.
    - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).where((nested operand in the contract() bitwise or nested operand in the contract equals nested operand in the ….run().
    - Set docstatus\_map at d.doc\_status from d.state.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(TargetDocType, self.workflow\_state\_field).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0542.json#L1635) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L692) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1636)
